"""Det förrenderade innehållet i sidorna ska bygga på samma data som publiceras."""

import json
import re
import unittest
from pathlib import Path

DOCS = Path(__file__).parent.parent / "docs"


class ForrendratFoljerDatan(unittest.TestCase):
    def test_tabellen_har_en_rad_per_organisation(self):
        for sida, data in [("index.html", "data.json"), ("myndigheter.html", "myndigheter.json"), ("en/index.html", "data.json"), ("en/myndigheter.html", "myndigheter.json")]:
            html = (DOCS / sida).read_text(encoding="utf-8")
            rader = re.search(r"<!--fr:rader-->(.*?)<!--/fr:rader-->", html, re.S).group(1)
            org = json.loads((DOCS / data).read_text(encoding="utf-8"))["organisationer"]
            self.assertEqual(rader.count("<tr>"), len(org), f"{sida}: kör python3 forrendera.py")
            for o in org:
                self.assertIn(f"<code>{o['doman']}</code>", rader, f"{sida}: {o['namn']} saknas")

    def test_matdatum_stammer(self):
        html = (DOCS / "index.html").read_text(encoding="utf-8")
        matt = json.loads((DOCS / "data.json").read_text(encoding="utf-8"))["matt"]
        tid = re.sub(r"T(\d\d)(\d\d)(\d\d)Z", r" \1:\2 UTC", matt)
        self.assertIn(f"E-post och konton mätta {tid}.", html)


if __name__ == "__main__":
    unittest.main()
