"""Klassar mätning 2 enligt METOD.md.

python3 webb_klassa.py data/webb-....json             # tabell, sammanfattning, okända värdar
python3 webb_klassa.py data/webb-A.json data/webb-B.json   # upprepningstest: jämför "US före samtycke"
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROT = Path(__file__).parent
GA = ("google-analytics.com", "analytics.google.com", "googletagmanager.com")


def lista():
    with open(ROT / "leverantorer.csv", encoding="utf-8") as f:
        return sorted(csv.DictReader(f), key=lambda r: -len(r["suffix"]))


LEVERANTORER = lista()


def leverantor(vard):
    for r in LEVERANTORER:
        if vard == r["suffix"] or vard.endswith("." + r["suffix"]):
            return r
    return None


def klassa(o):
    if not isinstance(o.get("status"), int) or o["status"] >= 400:
        return "kunde inte mätas", [], []
    traffar = [(v, leverantor(v)) for v in o["w2"]]
    okanda = [v for v, r in traffar if r is None]
    lander = {r["land"] for _, r in traffar if r}
    if not o["w2"]:
        klass = "ingen tredjepart"
    elif "US" in lander:
        klass = "US före samtycke"
    elif lander - {"SE", "EU"}:
        klass = "annat land före samtycke"
    elif okanda:
        klass = "okänd leverantör"
    else:
        klass = "bara EU/SE före samtycke"
    leverantorer = sorted({f"{r['leverantor']} ({r['land']})" for _, r in traffar if r})
    return klass, leverantorer, okanda


def har_ga(o):
    return any(v == d or v.endswith("." + d) for v in o.get("w2", []) for d in GA)


def klassa_v3(o):
    """Version 3 i METOD.md: klass efter nätet bakom varje tredjepartsvärd."""
    if not isinstance(o.get("status"), int) or o["status"] >= 400:
        return "kunde inte mätas"
    if not o["w2"]:
        return "ingen tredjepart"
    nat = [o["natverk"][v].get("nat") for v in o["w2"]]
    if "US" in nat:
        return "US-nät före samtycke"
    if None in nat:
        return "okänt nät"
    if "annat" in nat:
        return "annat nät före samtycke"
    return "bara EU/EES-nät före samtycke"


def rapport_v3(fil):
    d = json.load(open(fil, encoding="utf-8"))
    print(f"Källa: {fil} · mätt {d['matt']} · Chrome {d['chrome']} · kontroller {d['kontroller']}\n")
    print("| Organisation | Klass (v3) | Google Analytics/GTM | Värdar på US-nät | Leverantörer (där kända) |")
    print("|---|---|---|---|---|")
    rakna, varder, utan_asn = Counter(), set(), set()
    for o in d["organisationer"]:
        klass = klassa_v3(o)
        rakna[klass] += 1
        us = sorted(v for v in o.get("w2", []) if o["natverk"][v].get("nat") == "US")
        for v in o.get("w2", []):
            varder.add(v)
            if not o["natverk"][v].get("land"):
                utan_asn.add(v)
        lev = sorted({f"{r['leverantor']}" for v in o.get("w2", []) if (r := leverantor(v))})
        print(f"| {o['namn']} | {klass} | {'ja' if har_ga(o) else '–'} | {', '.join(us) or '–'} | {', '.join(lev) or '–'} |")
    n = len(d["organisationer"])
    matbara = n - rakna["kunde inte mätas"]
    tackning = 1 - len(utan_asn) / len(varder) if varder else 1
    print(f"\nKlasser: {dict(rakna)}")
    print(f"Google Analytics/GTM före samtycke: {sum(har_ga(o) for o in d['organisationer'])}/{n}")
    print(f"Mätbara: {matbara}/{n} = {matbara / n:.0%}")
    print(f"Unika värdar med ASN och land: {len(varder) - len(utan_asn)}/{len(varder)} = {tackning:.0%}; utan: {sorted(utan_asn)}")
    print("Kriterium v3:", "UPPFYLLT" if tackning >= 0.95 and matbara / n >= 0.95 else "EJ UPPFYLLT")


def rapport(fil):
    d = json.load(open(fil, encoding="utf-8"))
    print(f"Källa: {fil} · mätt {d['matt']} · Chrome {d['chrome']} · kontroller {d['kontroller']}\n")
    print("| Organisation | Klass | Google Analytics/GTM | Leverantörer före samtycke | Okända värdar |")
    print("|---|---|---|---|---|")
    rakna, alla_varder, okanda_varder = Counter(), set(), set()
    for o in d["organisationer"]:
        klass, lev, ok = klassa(o)
        rakna[klass] += 1
        alla_varder |= set(o.get("w2", []))
        okanda_varder |= set(ok)
        print(f"| {o['namn']} | {klass} | {'ja' if har_ga(o) else '–'} | {', '.join(lev) or '–'} | {', '.join(ok) or '–'} |")
    n = len(d["organisationer"])
    matbara = n - rakna["kunde inte mätas"]
    print(f"\nKlasser: {dict(rakna)}")
    print(f"Google Analytics/GTM före samtycke: {sum(har_ga(o) for o in d['organisationer'])}/{n}")
    print(f"Mätbara: {matbara}/{n}")
    andel = len(okanda_varder) / len(alla_varder) if alla_varder else 0
    print(f"Okända unika värdar: {len(okanda_varder)}/{len(alla_varder)} = {andel:.0%}: {sorted(okanda_varder)}")


def upprepning(a, b):
    def us(fil):
        return {o["namn"]: klassa(o)[0] == "US före samtycke"
                for o in json.load(open(fil, encoding="utf-8"))["organisationer"]}
    ua, ub = us(a), us(b)
    lika = [n for n in ua if ua[n] == ub.get(n)]
    print(f"Upprepning: 'US före samtycke' lika för {len(lika)}/{len(ua)}")
    for n in ua:
        if ua[n] != ub.get(n):
            print(f"  olika: {n}: {ua[n]} -> {ub.get(n)}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        upprepning(sys.argv[1], sys.argv[2])
    elif any("natverk" in o for o in json.load(open(sys.argv[1], encoding="utf-8"))["organisationer"]):
        rapport_v3(sys.argv[1])
    else:
        rapport(sys.argv[1])
