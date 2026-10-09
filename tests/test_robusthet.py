"""Motprov från Codex granskning 2026-10-09 (issues #9–#18): mätfel får aldrig bli
ett säkert negativt svar, och spärrarna ska stoppa ofullständiga körningar.
Inga nätanrop: resolvrar, Chrome och API:er ersätts med påhittade svar."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import dns.resolver

ROT = Path(__file__).parent.parent
sys.path.insert(0, str(ROT))

import klassa  # noqa: E402
import klassa_v2  # noqa: E402
import matning  # noqa: E402


class FalskResolver:
    """Svarar med fel för alla uppslag, eller med poster ur en tabell."""

    def __init__(self, fel=None, poster=None):
        self.fel, self.poster = fel, poster or {}

    def resolve(self, namn, typ):
        if self.fel:
            raise self.fel
        if (namn, typ) not in self.poster:
            raise dns.resolver.NXDOMAIN()
        return [FalskPost(v) for v in self.poster[(namn, typ)]]


class FalskPost:
    def __init__(self, varde):
        self.varde = varde
        self.strings = [varde.encode()]

    def to_text(self):
        return self.varde


def klass(poster):
    return klassa_v2.epost(klassa_v2.signaler(poster))


class DnsFelBlirInteNegativt(unittest.TestCase):
    """#9"""

    def test_timeout_och_servfail_blir_kunde_inte_matas(self):
        for fel in (dns.resolver.LifetimeTimeout(), dns.resolver.NoNameservers()):
            poster = matning.dns_poster("exempel.se", FalskResolver(fel=fel))
            self.assertIn("mx", poster["dns_fel"])
            self.assertEqual(klass(poster), "kunde inte mätas", type(fel).__name__)

    def test_nxdomain_och_noanswer_ar_riktiga_svar(self):
        for fel in (dns.resolver.NXDOMAIN(), dns.resolver.NoAnswer()):
            poster = matning.dns_poster("exempel.se", FalskResolver(fel=fel))
            self.assertEqual(poster["dns_fel"], [])
            self.assertEqual(klass(poster), "inga molnsignaler", type(fel).__name__)

    def test_fel_i_spf_gor_negativt_svar_omatbart_men_inte_positivt(self):
        tabell = {("exempel.se", "MX"): ["10 mx.exempel.se."]}
        poster = matning.dns_poster("exempel.se", FalskResolver(poster=tabell))
        poster["dns_fel"] = ["txt"]
        self.assertEqual(klass(poster), "kunde inte mätas")
        ms = matning.dns_poster("exempel.se", FalskResolver(poster={("exempel.se", "MX"): ["0 exempel-se.mail.protection.outlook.com."]}))
        ms["dns_fel"] = ["txt"]
        self.assertEqual(klass(ms), "MS", "MX avgör, även om SPF-uppslaget misslyckades")

    def test_certifikatnamn_med_mätfel_räknas_inte_som_inaktiva(self):
        import certmatning
        with mock.patch.object(matning, "resolver", FalskResolver(fel=dns.resolver.LifetimeTimeout())):
            r = certmatning.summera("exempel.se", {"a.exempel.se", "b.exempel.se"})
        self.assertEqual((r["aktiva"], r["dns_fel"]), (0, 2))


class BlandadeSignaler(unittest.TestCase):
    """#17"""

    def poster(self, **f):
        bas = {"mx": ["10 gw.exempel.se."], "spf": [], "autodiscover_cname": [], "dkim_selector1_cname": [],
               "dkim_google_txt": [], "enterpriseregistration_cname": [], "lyncdiscover_cname": []}
        return {**bas, **f}

    def test_google_regeln_ses_aven_nar_spf_har_bada(self):
        p = self.poster(spf=["v=spf1 include:spf.protection.outlook.com include:_spf.google.com -all"],
                        dkim_google_txt=["v=DKIM1; k=rsa"])
        self.assertEqual(klass(p), "G")

    def test_bada_reglerna_uppfyllda_blir_bada(self):
        p = self.poster(spf=["v=spf1 include:spf.protection.outlook.com include:_spf.google.com -all"],
                        dkim_selector1_cname=["selector1-exempel-se._domainkey.exempel.onmicrosoft.com."],
                        dkim_google_txt=["v=DKIM1; k=rsa"])
        self.assertEqual(klass(p), "MS+G")

    def test_domangrans(self):
        self.assertEqual(klassa.lev_mx(["10 notgoogle.com."]), "gateway/egen")
        self.assertEqual(klassa.lev_mx(["10 aspmx.l.google.com."]), "G")
        self.assertEqual(klassa.lev_mx(["0 x.evilmail.protection.outlook.com.attacker.se."]), "gateway/egen")
        p = self.poster(spf=["v=spf1 include:notspf.protection.outlook.com.example -all"])
        self.assertEqual(klassa_v2.signaler(p)["S2"], "-")


if __name__ == "__main__":
    unittest.main()
