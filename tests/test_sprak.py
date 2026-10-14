"""Svenska och engelska sidor ska ha samma texter och samma siffror."""

import json
import re
import unittest
from pathlib import Path

ROT = Path(__file__).parent.parent


def siffror(text):
    text = re.sub(r"<[^>]+>|https?://\S+", " ", text)
    text = re.sub(r"(?<=\d)[  ,.](?=\d)", "", text)
    return sorted(re.findall(r"\d+", text))


class SprakenFoljs(unittest.TestCase):
    def setUp(self):
        self.sv = json.loads((ROT / "i18n" / "sv.json").read_text(encoding="utf-8"))
        self.en = json.loads((ROT / "i18n" / "en.json").read_text(encoding="utf-8"))

    def test_samma_nycklar(self):
        self.assertEqual(set(self.sv), set(self.en))

    def test_samma_siffror_i_varje_text(self):
        for k, v in self.sv.items():
            if k.startswith("js.") or '"@context"' in v:
                continue
            self.assertEqual(siffror(v), siffror(self.en[k]), k)

    def test_samma_platshallare_i_javascript(self):
        for k, v in self.sv.items():
            if k.startswith("js."):
                self.assertEqual(sorted(re.findall(r"\{\w+\}", v)), sorted(re.findall(r"\{\w+\}", self.en[k])), k)

    def test_sidorna_ar_byggda(self):
        for fil in (ROT / "sidor").glob("*.html"):
            for sprak, mapp in [("sv", ROT / "docs"), ("en", ROT / "docs" / "en")]:
                html = (mapp / fil.name).read_text(encoding="utf-8")
                self.assertIn(f'<html lang="{sprak}">', html, f"{sprak}/{fil.name}: kör python3 bygg_sprak.py")
                self.assertNotIn("{{", html)
                self.assertIn('class="sprakval"', html, f"{sprak}/{fil.name}: språkvalet saknas")


if __name__ == "__main__":
    unittest.main()
