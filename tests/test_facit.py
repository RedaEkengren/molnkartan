"""Facitreglerna (#20) prövade på påhittade mejl, utan riktiga svar."""

import email
import email.policy
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import facit  # noqa: E402


def mejl(fran, *huvuden):
    text = f"From: {fran}\nSubject: Sv: Fråga\n" + "".join(h + "\n" for h in huvuden) + "\nHej\n"
    return email.message_from_string(text, policy=email.policy.default)


MS = "Received: from SV0P279MB0123.NORP279.PROD.OUTLOOK.COM (2603:10a6::1) by mail.protonmail.ch"
G = "Received: from mail-sor-f41.google.com (mail-sor-f41.google.com [209.85.220.41]) by mail.protonmail.ch"
EGEN = "Received: from smtp.exempel.se (smtp.exempel.se [192.0.2.1]) by mail.protonmail.ch"


class Huvudregler(unittest.TestCase):
    def test_microsoft_via_received_och_x_ms(self):
        self.assertEqual(facit.klassa_meddelande(mejl("a@exempel.se", MS)), "Microsoft")
        self.assertEqual(facit.klassa_meddelande(mejl("a@exempel.se", EGEN, "X-MS-Exchange-Organization-AuthAs: Internal")), "Microsoft")

    def test_google(self):
        self.assertEqual(facit.klassa_meddelande(mejl("a@exempel.se", G)), "Google")
        self.assertEqual(facit.klassa_meddelande(mejl("a@exempel.se", EGEN, "X-Google-Smtp-Source: abc")), "Google")

    def test_annat_och_tvetydig(self):
        self.assertEqual(facit.klassa_meddelande(mejl("a@exempel.se", EGEN)), "annat")
        self.assertEqual(facit.klassa_meddelande(mejl("a@exempel.se", MS, G)), "tvetydig")

    def test_domangrans(self):
        falsk = "Received: from mail.notoutlook.com.exempel.se (x [192.0.2.2]) by mail.protonmail.ch"
        self.assertEqual(facit.klassa_meddelande(mejl("a@exempel.se", falsk)), "annat")
        self.assertEqual(facit.klassa_meddelande(mejl("a@exempel.se", "Received: from x.fakegoogle.com by y")), "annat")

    def test_flera_svar(self):
        self.assertEqual(facit.sla_ihop(["annat", "Microsoft"]), "Microsoft")
        self.assertEqual(facit.sla_ihop(["Microsoft", "Google"]), "tvetydig")
        self.assertEqual(facit.sla_ihop(["annat", "annat"]), "annat")


class Koppling(unittest.TestCase):
    def test_avsandare_till_organisation(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "urval.csv").write_text("namn,domän,epost\nExempel,exempel.se,x@exempel.se\nAnnan,annan.se,y@annan.se\n", encoding="utf-8")
            (d / "1.eml").write_bytes(mejl("kc@post.exempel.se", MS).as_bytes())
            (d / "2.eml").write_bytes(mejl("auto@exempel.mail.onmicrosoft.com", MS).as_bytes())
            (d / "3.eml").write_bytes(mejl("x@okand.se", EGEN).as_bytes())
            rader, namnkoppling, okopplade = facit.facit(d, d / "urval.csv")
        self.assertEqual({r["domän"]: (r["facit"], r["antal_svar"]) for r in rader},
                         {"exempel.se": ("Microsoft", 2), "annan.se": ("saknas", 0)})
        self.assertEqual(namnkoppling, ["exempel.mail.onmicrosoft.com → exempel.se"])
        self.assertEqual(okopplade, ["3.eml"])


if __name__ == "__main__":
    unittest.main()
