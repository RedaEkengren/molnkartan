"""Bygger docs/data.json för GitHub Pages från en rådatafil: python3 bygg_sida.py data/ra-....json"""

import json
import sys
from pathlib import Path

from klassa import webb
from klassa_v2 import epost, signaler

ROT = Path(__file__).parent


def main():
    fil = sys.argv[1]
    data = json.load(open(fil, encoding="utf-8"))
    organisationer = []
    for o in data:
        s = signaler(o)
        organisationer.append({
            "namn": o["namn"],
            "typ": o["typ"],
            "lan": o["lan"],
            "doman": o["domän"],
            "epost": epost(s),
            "tenant": o["entra_status"] == 200,
            "teams": s["S8"] == "MS",
            "webb": webb(o["www_asn_namn"]),
            "webbLeverantor": o["www_asn_namn"],
            "signaler": s,
        })
    ut = {"matt": data[0]["matt"], "kalla": fil, "organisationer": organisationer}
    (ROT / "docs").mkdir(exist_ok=True)
    (ROT / "docs" / "data.json").write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"docs/data.json: {len(organisationer)} organisationer, mätt {ut['matt']}")


if __name__ == "__main__":
    main()
