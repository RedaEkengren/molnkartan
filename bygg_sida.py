"""Bygger datafilen till GitHub Pages:
python3 bygg_sida.py <ra-fil> [<webb-fil>] [<utfil, standard docs/data.json>]
"""

import json
import sys
from pathlib import Path

from klassa import webb
from klassa_v2 import epost, signaler
from webb_klassa import har_ga, klassa_v3, leverantor

ROT = Path(__file__).parent


def main():
    fil = sys.argv[1]
    data = json.load(open(fil, encoding="utf-8"))
    webb_fil = sys.argv[2] if len(sys.argv) > 2 else None
    fore = {}
    if webb_fil:
        webb_data = json.load(open(webb_fil, encoding="utf-8"))
        for w in webb_data["organisationer"]:
            us = sorted(v for v in w.get("w2", []) if w["natverk"][v].get("nat") == "US")
            fore[w["domän"]] = {
                "klass": klassa_v3(w),
                "ga": har_ga(w),
                "us": us,
                "usLeverantorer": sorted({(leverantor(v) or {}).get("leverantor") or ".".join(v.split(".")[-2:]) for v in us}),
            }
    organisationer = []
    for o in data:
        s = signaler(o)
        organisationer.append({
            "namn": o["namn"],
            "typ": o["typ"],
            "lan": o.get("lan", ""),
            "antal": int(o.get("antal") or 1),
            "doman": o["domän"],
            "epost": epost(s),
            "tenant": o["entra_status"] == 200,
            "teams": s["S8"] == "MS",
            "webb": webb(o["www_asn_namn"]),
            "webbLeverantor": o["www_asn_namn"],
            "signaler": s,
            "fore_samtycke": fore.get(o["domän"]),
            # Riktiga svar till animationen "Så mäts en kommun".
            "svar": {
                "mx": [m.split()[-1].rstrip(".") for m in sorted(o["mx"], key=lambda m: int(m.split()[0]))],
                "spf": next((i for i in ("spf.protection.outlook.com", "_spf.google.com")
                             if any(i in x for x in o["spf"])), None),
                "dkim": (o["dkim_selector1_cname"] or [None])[0],
                "entra": o["entra_status"],
            },
        })
    ut = {"matt": data[0]["matt"], "kalla": fil, "organisationer": organisationer}
    if webb_fil:
        ut["webbMatt"], ut["webbKalla"] = webb_data["matt"], webb_fil
    utfil = ROT / (sys.argv[3] if len(sys.argv) > 3 else "docs/data.json")
    utfil.parent.mkdir(exist_ok=True)
    utfil.write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{utfil.relative_to(ROT)}: {len(organisationer)} organisationer, mätt {ut['matt']}")


if __name__ == "__main__":
    main()
