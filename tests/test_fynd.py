"""Fyndsidan får inte påstå något som rådatan inte visar.

Varje siffra och varje namn i docs/fynd.html räknas fram av fynd_siffror.py från
samma filer som sidan publicerar. Ändras datan eller texten så att de inte
längre stämmer, fallerar testet.
"""

import re
import sys
import unittest
from pathlib import Path

ROT = Path(__file__).parent.parent
sys.path.insert(0, str(ROT))

import fynd_siffror  # noqa: E402

ORD = {4: "Fyra", 5: "Fem", 11: "elva"}


def artikel(html, ident):
    m = re.search(rf'<article class="fynd" id="{ident}">(.*?)</article>', html, re.S)
    if not m:
        raise AssertionError(f"fynd {ident} saknas")
    return re.sub(r"\s+", " ", m.group(1))


class FyndenStammerMedDatan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = fynd_siffror.siffror()
        cls.html = (ROT / "docs" / "fynd.html").read_text(encoding="utf-8")

    def innehaller(self, ident, *texter):
        a = artikel(self.html, ident)
        for t in texter:
            self.assertIn(str(t), a, f"fynd {ident}: väntade '{t}'")

    def test_exchange_online(self):
        s = self.s
        self.innehaller("exchange-online", f"{s['exo_kommuner']} av 310", f"{s['dns_ms_kommuner']} kommuner",
                        f"alla {s['exo_okand'][1]}", f"{s['exo_inga'][0]} av {s['exo_inga'][1]}",
                        f"{s['exo_google'][0]} av {s['exo_google'][1]}", f"{s['exo_myndigheter']} av 202")
        self.assertEqual(s["exo_okand"][0], s["exo_okand"][1], "texten säger 'alla'")

    def test_skatteverket(self):
        self.assertTrue(self.s["skatteverket_exo"])
        self.innehaller("skatteverket", "registrerad i Exchange Online")

    def test_myndigheter_google(self):
        n, av = self.s["ga_myndigheter"]
        ins = self.s["ga_myndigheter_insamling"]
        self.innehaller("myndigheter-ga", f"{n} av {av}", f"{ins} av dem", f"övriga {n - ins}")

    def test_samtyckesverktyg(self):
        self.innehaller("samtyckesverktyget", f"{self.s['cmp_org']} kommuner och regioner", f"För {ORD[self.s['cmp_enda']]} av dem")

    def test_google_analytics(self):
        s = self.s
        self.innehaller("google-analytics", f"{s['ga_kommuner'][0]} av {s['ga_kommuner'][1]}",
                        f"{ORD[len(s['ga_kommuner_insamling'])].capitalize()} kommuner", f"{ORD[len(s['ga_kommuner_bara_gtm'])]} laddar bara",
                        *s["ga_kommuner_insamling"], *s["ga_kommuner_bara_gtm"])
        self.assertEqual(len(s["ga_kommuner_insamling"]) + len(s["ga_kommuner_bara_gtm"]), s["ga_kommuner"][0])

    def test_browsealoud(self):
        (forst, n1), (andra, n2) = self.s["topp_us_kommuner"][:2]
        self.assertEqual((forst, andra), ("Google", "Texthelp"))
        self.innehaller("browsealoud", f"{n2} kommuner", f"Google ({n1})", "näst vanligast")

    def test_ingen_tredjepart(self):
        s = self.s
        self.innehaller("ingen-tredjepart", f"{len(s['ingen_tredjepart'])} kommuner", *s["ingen_tredjepart"])
        self.innehaller("ingen-tredjepart", *s["ingen_tredjepart_us_hotell"])

    def test_sakerhetsgrunder(self):
        s = self.s
        lika = s["sakerhet_lika_9999"].values()
        self.innehaller("sakerhetsgrunder", f"{s['dmarc_none']} av 310", f"{s['dmarc_reject']} har", f"{s['mta_sts']} har publicerat",
                        f"hos {s['dnssec']}", f"{min(lika)}–{max(lika)} av 512")

    def test_google_tar_emot(self):
        s = self.s
        namn = s["google_tar_emot_ms_signerar"]
        self.innehaller("google-tar-emot", f"{len(namn)} kommuner", *namn,
                        f"{ORD[s['google_tar_emot_lan']['Östergötlands län']]} av dem ligger i Östergötland")

    def test_tjanster(self):
        k, r, m = self.s["cert_kommuner"], self.s["cert_regioner"], self.s["cert_myndigheter"]
        sv = lambda x: f"{x:,}".replace(",", " ")
        pc = lambda x: str(x).replace(".", ",")
        self.innehaller("tjanster", f"{k['noll']} av {k['org']} kommuner", f"medianen per kommun är {k['median']} %",
                        f"{pc(k['andel'])} %", sv(k["aktiva"]), f"står för {k['storsta_andel_av_us']} %",
                        f"{r['minst_en']} av {r['org']}", f"medianen är {r['median']} %", f"medianen {m['median']} %",
                        f"{self.s['t6'][0]} av {self.s['t6'][1]}", sv(self.s["cert_interna"]))
        self.assertGreaterEqual(self.s["t6"][0], 16, "T6 ska hålla för att fyndet får publiceras")
        self.assertGreaterEqual(2 * k["noll"], k["org"] - 1, "rubriken säger 'hälften'")

    def test_tenant(self):
        self.innehaller("tenant", f"{self.s['tenant']} av 310")


if __name__ == "__main__":
    unittest.main()
