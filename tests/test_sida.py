"""Sidan får inte visa något annat än klassningen: docs/data.json ska vara byggd
från senaste nationella rådatan med dagens regler i klassa_v2.py."""

import glob
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROT = Path(__file__).parent.parent


class SidanFoljerReglerna(unittest.TestCase):
    def test_data_json_ar_byggd_med_dagens_regler(self):
        senaste = sorted(glob.glob(str(ROT / "data" / "ra-organisationer-sverige-*.json")))[-1]
        webb = sorted(glob.glob(str(ROT / "data" / "webb-organisationer-sverige-*.json")))[-1]
        publicerad = json.loads((ROT / "docs" / "data.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            kopia = Path(tmp)
            for f in ("bygg_sida.py", "klassa.py", "klassa_v2.py", "webb_klassa.py", "leverantorer.csv"):
                (kopia / f).write_bytes((ROT / f).read_bytes())
            subprocess.run([sys.executable, "bygg_sida.py", senaste, webb], cwd=kopia, check=True, capture_output=True)
            ny = json.loads((kopia / "docs" / "data.json").read_text(encoding="utf-8"))
        self.assertEqual(publicerad["organisationer"], ny["organisationer"],
                         "docs/data.json är inte ombyggd: kör python3 bygg_sida.py <senaste ra-fil> <senaste webb-fil>")

    def test_myndigheter_json_ar_byggd_med_dagens_regler(self):
        ra = sorted(glob.glob(str(ROT / "data" / "ra-organisationer-myndigheter-matning-*.json")))[-1]
        webb = sorted(glob.glob(str(ROT / "data" / "webb-organisationer-myndigheter-matning-*.json")))[-1]
        publicerad = json.loads((ROT / "docs" / "myndigheter.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            kopia = Path(tmp)
            for f in ("bygg_sida.py", "klassa.py", "klassa_v2.py", "webb_klassa.py", "leverantorer.csv"):
                (kopia / f).write_bytes((ROT / f).read_bytes())
            subprocess.run([sys.executable, "bygg_sida.py", ra, webb, "docs/myndigheter.json"], cwd=kopia, check=True, capture_output=True)
            ny = json.loads((kopia / "docs" / "myndigheter.json").read_text(encoding="utf-8"))
        self.assertEqual(publicerad["organisationer"], ny["organisationer"], "docs/myndigheter.json är inte ombyggd")

    def test_varje_exempel_i_animationen_finns_i_datan(self):
        org = json.loads((ROT / "docs" / "data.json").read_text(encoding="utf-8"))["organisationer"]
        # Samma villkor som EXEMPEL i docs/demo.js.
        self.assertTrue(any(o["epost"] == "MS" and o["signaler"]["S1"] == "MS" and o["signaler"]["S7"] == "MS" for o in org))
        self.assertTrue(any(o["epost"] == "G" and o["signaler"]["S1"] == "G" for o in org))
        self.assertTrue(any(o["epost"] == "MS" and o["signaler"]["S1"] == "gateway/egen"
                            and o["signaler"]["S2"] == "MS" and o["signaler"]["S7"] == "MS" for o in org))


if __name__ == "__main__":
    unittest.main()
