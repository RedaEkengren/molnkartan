"""Inget i repot får peka på en lokal dator: absoluta sökvägar till hemkataloger
eller monterade diskar avslöjar användarnamn och mappstruktur."""

import re
import subprocess
import unittest
from pathlib import Path

ROT = Path(__file__).parent.parent
LOKALT = re.compile(r"(?<![\w.])/(home|media|Users|tmp/claude)[-/]")


class IngaLokalaSokvagar(unittest.TestCase):
    def test_inga_lokala_sokvagar(self):
        filer = subprocess.run(["git", "ls-files"], cwd=ROT, capture_output=True, text=True, check=True).stdout.split()
        traffar = [f for f in filer if f != "tests/test_hygien.py"
                   and LOKALT.search((ROT / f).read_text(encoding="utf-8", errors="ignore"))]
        self.assertEqual(traffar, [], f"lokala sökvägar i {traffar}")


if __name__ == "__main__":
    unittest.main()
