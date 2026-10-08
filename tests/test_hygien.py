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


class IngaVardnamnICertdata(unittest.TestCase):
    """Gränsen i METOD.md, mätning 4: certifikatdata får bara innehålla antal, aldrig värdnamn."""

    def test_inga_underdomaner(self):
        import json

        def strangar(x):
            if isinstance(x, dict):
                for k, v in x.items():
                    yield k
                    yield from strangar(v)
            elif isinstance(x, list):
                for v in x:
                    yield from strangar(v)
            elif isinstance(x, str):
                yield x

        for fil in sorted(ROT.glob("data/cert-*.json")):
            d = json.loads(fil.read_text(encoding="utf-8"))
            domaner = {o["domän"] for o in d["organisationer"]}
            lackor = [s for s in strangar(d) if any(s.endswith("." + dom) for dom in domaner)]
            self.assertEqual(lackor[:5], [], f"värdnamn i {fil.name}")


if __name__ == "__main__":
    unittest.main()
