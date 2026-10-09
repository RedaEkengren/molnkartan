"""Tillämpar e-postregel v2 i METOD.md på en rådatafil: python3 klassa_v2.py data/ra-....json"""

import json
import sys
from collections import Counter

from klassa import lev_mx, under, webb


# Fält i rådatans dns_fel -> signalen som uppslaget gäller (#9).
FEL_TILL_SIGNAL = {"mx": "S1", "txt": "S2", "autodiscover": "S4", "dkim_selector1": "S7",
                   "dkim_google": "S7", "enterpriseregistration": "S8", "lyncdiscover": "S8"}


def har(lista, doman):
    return any(under(x, doman) for x in lista)


def leverantorer(ms, g):
    """En signal kan stödja båda leverantörerna (#17): "MS", "G", "MS+G" eller "-"."""
    return "+".join(p for p, ja in (("MS", ms), ("G", g)) if ja) or "-"


def stoder(signal, leverantor):
    return leverantor in signal.split("+")


def signaler(o):
    inkludera = {t.split(":", 1)[1].lower() for post in o["spf"] for t in post.split() if t.lower().startswith("include:")}
    return {
        "S1": lev_mx(o["mx"]),
        "S2": leverantorer("spf.protection.outlook.com" in inkludera, "_spf.google.com" in inkludera),
        "S4": "MS" if any(c.rstrip(".").lower() == "autodiscover.outlook.com" for c in o["autodiscover_cname"]) else "-",
        # dkim.mail.microsoft: Microsofts nyare DKIM-format, se rättelsen i METOD.md.
        "S7": leverantorer(har(o["dkim_selector1_cname"], "onmicrosoft.com") or har(o["dkim_selector1_cname"], "dkim.mail.microsoft"),
                           any(t.startswith("v=DKIM1") for t in o["dkim_google_txt"])),
        "S8": "MS" if har(o["enterpriseregistration_cname"], "enterpriseregistration.windows.net")
        or har(o["lyncdiscover_cname"], "webdir.online.lync.com") else "-",
        # Äldre rådata saknar dns_fel; där kan mätfel inte skiljas från saknade poster (#9).
        "fel": sorted({FEL_TILL_SIGNAL[f] for f in o.get("dns_fel", [])}),
    }


def epost(s):
    """E-postregel v2 med rättelserna för #9 (mätfel) och #17 (blandade signaler)."""
    if "S1" in s.get("fel", []):
        return "kunde inte mätas"
    if s["S1"] in ("MS", "G"):
        return s["S1"]
    ms = stoder(s["S2"], "MS") and (s["S4"] == "MS" or stoder(s["S7"], "MS"))
    g = stoder(s["S2"], "G") and stoder(s["S7"], "G")
    if ms and g:
        klass = "MS+G"  # båda reglerna uppfyllda: redovisas som båda, inte som den ena (#17)
    elif ms:
        klass = "MS"
    elif g:
        klass = "G"
    elif not any(stoder(s[x], p) for x in ("S2", "S4", "S7") for p in ("MS", "G")):
        klass = "inga molnsignaler"
    else:
        klass = "okänd"
    if klass in ("inga molnsignaler", "okänd") and set(s.get("fel", [])) & {"S2", "S4", "S7"}:
        return "kunde inte mätas"
    return klass


def main():
    fil = sys.argv[1]
    data = json.load(open(fil, encoding="utf-8"))
    print(f"Källa: {fil}\n")
    print("| Organisation | E-post v2 | S1 | S2 | S4 | S7 | S8 | MS-tenant | Webb |")
    print("|---|---|---|---|---|---|---|---|---|")
    rakna = Counter()
    for o in data:
        s = signaler(o)
        lev = epost(s)
        rakna[lev] += 1
        tenant = "ja" if o["entra_status"] == 200 else "nej"
        print(f"| {o['namn']} | {lev} | {s['S1']} | {s['S2']} | {s['S4']} | {s['S7']} | {s['S8']} | {tenant} | {webb(o['www_asn_namn'])} |")
    n = len(data)
    entydiga = n - rakna["okänd"]
    print(f"\nE-post: {dict(rakna)}")
    print(f"Entydiga {entydiga}/{n} = {entydiga / n:.0%}, okända {rakna['okänd']}/{n} = {rakna['okänd'] / n:.0%}")
    print("Kriterium v2:", "UPPFYLLT" if entydiga / n >= 0.85 and rakna["okänd"] / n <= 0.15 else "EJ UPPFYLLT")
    print(f"MS-tenant: {sum(o['entra_status'] == 200 for o in data)}/{n}")


if __name__ == "__main__":
    main()
