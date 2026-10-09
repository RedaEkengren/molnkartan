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


TYPER = {"URL_REQUEST_START_JOB": 1, "HTTP_TRANSACTION_READ_RESPONSE_HEADERS": 2, "REQUEST_ALIVE": 3}


def natlogg(*anrop):
    """anrop: (källa, url, initiator, status eller None, net_error eller None)."""
    ev = []
    for kalla, url, initiator, status, fel in anrop:
        ev.append({"source": {"id": kalla}, "type": 1, "params": {"url": url, "initiator": initiator}})
        if status:
            ev.append({"source": {"id": kalla}, "type": 2, "params": {"headers": [f"HTTP/1.1 {status}"]}})
        if fel:
            ev.append({"source": {"id": kalla}, "type": 3, "params": {"net_error": fel}})
    return {"constants": {"logEventTypes": TYPER}, "events": ev}


class FalskChrome:
    def __init__(self, kod=0, dom="<html><body>sida</body></html>", logg=None):
        self.kod, self.dom, self.logg = kod, dom, logg

    def __call__(self, argv, **kw):
        if self.logg is not None:
            fil = next(a.split("=", 1)[1] for a in argv if a.startswith("--log-net-log="))
            Path(fil).parent.mkdir(parents=True, exist_ok=True)
            Path(fil).write_text(json.dumps(self.logg))
        return subprocess.CompletedProcess(argv, self.kod, self.dom, "")


class WebbMatfel(unittest.TestCase):
    """#10 och #12"""

    def mat(self, chrome):
        import webbmatning
        with mock.patch.object(webbmatning, "slutadress", return_value=(200, "https://www.exempel.se/")), \
             mock.patch.object(webbmatning, "natverk", return_value={"nat": "US"}), \
             mock.patch.object(webbmatning.subprocess, "run", chrome):
            return webbmatning.mat({"namn": "Exempel", "typ": "kommun", "domän": "exempel.se"})

    def test_krasch_ger_kunde_inte_matas(self):
        from webb_klassa import klassa_v3
        for chrome in (FalskChrome(kod=1), FalskChrome(logg=None), FalskChrome(dom="", logg=natlogg((1, "https://www.exempel.se/", "not an origin", 200, None))),
                       FalskChrome(dom="chrome-error://chromewebdata/", logg=natlogg()),
                       FalskChrome(logg=natlogg((1, "https://www.exempel.se/", "not an origin", None, -105)))):
            o = self.mat(chrome)
            self.assertEqual(klassa_v3(o), "kunde inte mätas", o["status"])

    def test_lyckad_sida_utan_tredjepart(self):
        from webb_klassa import klassa_v3
        o = self.mat(FalskChrome(logg=natlogg((1, "https://www.exempel.se/", "not an origin", 200, None),
                                              (2, "https://www.exempel.se/a.js", "https://www.exempel.se", 200, None))))
        self.assertEqual((o["status"], klassa_v3(o)), (200, "ingen tredjepart"))

    def test_anrop_utan_svar_ar_forsok_men_inte_kontakt(self):
        o = self.mat(FalskChrome(logg=natlogg((1, "https://www.exempel.se/", "not an origin", 200, None),
                                              (2, "https://www.google-analytics.com/g/collect", "https://www.exempel.se", None, -105),
                                              (3, "https://www.googletagmanager.com/gtm.js", "https://www.exempel.se", 200, None))))
        self.assertEqual(o["w2"], ["www.google-analytics.com", "www.googletagmanager.com"])
        self.assertEqual(o["w2_svar"], ["www.googletagmanager.com"])


class RegistreradDoman(unittest.TestCase):
    """#16"""

    def test_suffix_enligt_listan(self):
        from domaner import registrerad
        self.assertEqual(registrerad("a.b.example.co.uk"), "example.co.uk")
        self.assertEqual(registrerad("kommun.github.io"), "kommun.github.io")
        self.assertNotEqual(registrerad("x.github.io"), registrerad("y.github.io"))

    def test_samma_namn_annan_toppdoman_ar_tredjepart_utan_belagg(self):
        from domaner import egna_domaner, registrerad
        self.assertNotIn(registrerad("track.example.com"), egna_domaner("example.se", "www.example.se"))
        self.assertIn("helsingborg.io", egna_domaner("helsingborg.se", "helsingborg.se"), "alias med belägg")


class Sparrar(unittest.TestCase):
    """#11, #13, #14 och #18"""

    def tri(self, t1_svar, t4_svar, n=512, ip=338):
        rader = [{"epost": "MS", "tenant": True, "t1_realm": True if i < t1_svar else None, "t2_exo": True,
                  "t3_cloudflare": "MS", "t3_quad9": "MS", "t3_google": "MS"} for i in range(n)]
        t4 = [{"ip": f"10.0.0.{i}", "cymru": "1", "ripe": ["1"] if i < t4_svar else None} for i in range(ip)]
        return {"domaner": rader, "t4": t4}

    def test_triangulering_kraver_tackning(self):
        from triangulering import godkand
        self.assertTrue(godkand(self.tri(512, 338)))
        self.assertFalse(godkand(self.tri(1, 1)), "ett enda svar får inte räcka (#11)")
        self.assertFalse(godkand(self.tri(480, 338)), "under 95 % täckning i T1")
        self.assertFalse(godkand({"domaner": [], "t4": []}), "tomt underlag")

    def test_webbsparr_kraver_nat_och_kontroller(self):
        from webb_klassa import godkand
        ok_kontroller = {"negativ": [], "positiv": ["www.googletagmanager.com"],
                         "nat": {"www.googletagmanager.com": "US", "www.hetzner.com": "EU/EES"}}
        org = [{"status": 200, "w2": ["t.exempel.com"], "natverk": {"t.exempel.com": {"land": None}}} for _ in range(20)]
        self.assertFalse(godkand({"kontroller": ok_kontroller, "organisationer": org}), "0 % nät (#13)")
        for o in org:
            o["natverk"]["t.exempel.com"]["land"] = "US"
        self.assertTrue(godkand({"kontroller": ok_kontroller, "organisationer": org}))
        self.assertFalse(godkand({"kontroller": {}, "organisationer": org}), "saknade kontroller")
        self.assertFalse(godkand({"kontroller": ok_kontroller, "organisationer": []}), "tom population")

    def test_ofullstandig_paginering_ar_inte_ok(self):
        import certmatning
        sidor = iter([[{"id": i, "dns_names": [f"n{i}.exempel.se"]} for i in range(100)], None])
        with mock.patch.object(certmatning, "certspotter_sida", lambda url: next(sidor)):
            self.assertIsNone(certmatning.namn_certspotter("exempel.se"), "#14")
        sidor = iter([[{"id": 1, "dns_names": ["a.exempel.se"]}]])
        with mock.patch.object(certmatning, "certspotter_sida", lambda url: next(sidor)):
            self.assertEqual(certmatning.namn_certspotter("exempel.se"), {"a.exempel.se"})

    def test_aldre_triangulering_markeras(self):
        import bygg_sida
        ny_dns = ROT / "data" / "ra-organisationer-sverige-2099-01-01T000000Z.json"
        tri = {"kallor": {"kommuner": "data/ra-organisationer-sverige-2026-10-08T154137Z.json"}}
        self.assertFalse(bygg_sida.triangulering_avser(tri, ny_dns, "kommuner"), "#18")
        self.assertTrue(bygg_sida.triangulering_avser(tri, ROT / "data/ra-organisationer-sverige-2026-10-08T154137Z.json", "kommuner"))


if __name__ == "__main__":
    unittest.main()
