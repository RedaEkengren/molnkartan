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
    def test_datafilerna_ar_byggda_med_dagens_regler_och_senaste_data(self):
        sys.path.insert(0, str(ROT))
        import bygg_sida
        for grupp, g in bygg_sida.GRUPPER.items():
            publicerad = json.loads((ROT / g["ut"]).read_text(encoding="utf-8"))
            with tempfile.TemporaryDirectory() as tmp:
                original = g["ut"]
                g["ut"] = str(Path(tmp) / "ut.json")
                try:
                    bygg_sida.bygg(grupp)
                finally:
                    g["ut"] = original
                ny = json.loads((Path(tmp) / "ut.json").read_text(encoding="utf-8"))
            self.assertEqual(publicerad, ny, f"{original} är inte ombyggd: kör python3 bygg_sida.py")

    def test_varje_exempel_i_animationen_finns_i_datan(self):
        org = json.loads((ROT / "docs" / "data.json").read_text(encoding="utf-8"))["organisationer"]
        # Samma villkor som EXEMPEL i docs/demo.js.
        self.assertTrue(any(o["epost"] == "MS" and o["signaler"]["S1"] == "MS" and o["signaler"]["S7"] == "MS" for o in org))
        self.assertTrue(any(o["epost"] == "G" and o["signaler"]["S1"] == "G" for o in org))
        self.assertTrue(any(o["epost"] == "MS" and o["signaler"]["S1"] == "gateway/egen"
                            and o["signaler"]["S2"] == "MS" and o["signaler"]["S7"] == "MS" for o in org))
        self.assertTrue(any(o["epost"] == "inga molnsignaler" and o["exo"] is True for o in org))


if __name__ == "__main__":
    unittest.main()
