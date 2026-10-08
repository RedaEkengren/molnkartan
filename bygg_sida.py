"""Bygger datafilerna till GitHub Pages från de senaste mätningarna:

python3 bygg_sida.py kommuner      # docs/data.json
python3 bygg_sida.py myndigheter   # docs/myndigheter.json

Varje källa väljs som senaste fil av sitt slag i data/, så sidan och
animationerna aldrig visar äldre data än rapporterna.
"""

import json
import sys
from collections import Counter
from pathlib import Path

from klassa import webb
from klassa_v2 import epost, signaler
from webb_klassa import har_ga, klassa_v3, leverantor

ROT = Path(__file__).parent

GRUPPER = {
    "kommuner": {"ra": "ra-organisationer-sverige-*.json", "webb": "webb-organisationer-sverige-*.json",
                 "ut": "docs/data.json", "sakerhet": lambda g: g != "Statliga myndigheter"},
    "myndigheter": {"ra": "ra-organisationer-myndigheter-matning-*.json",
                    "webb": "webb-organisationer-myndigheter-matning-*.json",
                    "ut": "docs/myndigheter.json", "sakerhet": lambda g: g == "Statliga myndigheter"},
}


def senaste(monster):
    filer = sorted((ROT / "data").glob(monster))
    return filer[-1] if filer else None


def las(fil):
    return json.loads(fil.read_text(encoding="utf-8")) if fil else None


def relativ(fil):
    return str(fil.relative_to(ROT)) if fil else None


def bygg(grupp):
    g = GRUPPER[grupp]
    ra_fil, webb_fil = senaste(g["ra"]), senaste(g["webb"])
    tri_fil, sak_fil = senaste("triangulering-20*Z.json"), senaste("sakerhet-*.json")
    data, webb_data, tri, sak = las(ra_fil), las(webb_fil), las(tri_fil), las(sak_fil)

    fore = {}
    for w in (webb_data or {}).get("organisationer", []):
        varder = [{"v": v, "nat": w["natverk"][v].get("nat"),
                   "lev": (leverantor(v) or {}).get("leverantor")} for v in w.get("w2", [])]
        us = sorted(x["v"] for x in varder if x["nat"] == "US")
        fore[w["domän"]] = {
            "klass": klassa_v3(w),
            "ga": har_ga(w),
            "us": us,
            "usLeverantorer": sorted({(leverantor(v) or {}).get("leverantor") or ".".join(v.split(".")[-2:]) for v in us}),
            # Alla tredjepartsvärdar med nät, till animationen "Så mäts en webbplats".
            "varder": varder,
            "sida": w.get("slutadress"),
        }
    exo = {r["domän"]: r["t2_exo"] for r in (tri or {}).get("domaner", [])}

    organisationer = []
    for o in data:
        s = signaler(o)
        organisationer.append({
            "namn": o["namn"],
            "kod": o.get("kod"),
            "typ": o["typ"],
            "lan": o.get("lan", ""),
            "antal": int(o.get("antal") or 1),
            "doman": o["domän"],
            "epost": epost(s),
            "tenant": o["entra_status"] == 200,
            "exo": exo.get(o["domän"]),
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

    sakerhet = {}
    if sak:
        for namn, signaler_ in sak["per_grupp"].items():
            if g["sakerhet"](namn):
                for signal, varden in signaler_.items():
                    sakerhet.setdefault(signal, Counter()).update(varden)

    ut = {
        "matt": data[0]["matt"], "kalla": relativ(ra_fil),
        "webbMatt": webb_data and webb_data["matt"], "webbKalla": relativ(webb_fil),
        "trianguleringMatt": tri and tri["matt"], "trianguleringKalla": relativ(tri_fil),
        "sakerhetMatt": sak and sak["matt"], "sakerhetKalla": relativ(sak_fil),
        "sakerhet": {k: dict(v) for k, v in sakerhet.items()},
        "organisationer": organisationer,
    }
    utfil = ROT / g["ut"]
    utfil.parent.mkdir(exist_ok=True)
    utfil.write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{g['ut']}: {len(organisationer)} organisationer")


if __name__ == "__main__":
    for grupp in sys.argv[1:] or GRUPPER:
        bygg(grupp)
