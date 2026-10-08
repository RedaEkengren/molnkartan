"""Tillämpar e-postregel v2 i METOD.md på en rådatafil: python3 klassa_v2.py data/ra-....json"""

import json
import sys
from collections import Counter

from klassa import lev_mx, webb


def har(lista, slut):
    return any(x.rstrip(".").lower().endswith(slut) for x in lista)


def signaler(o):
    spf = " ".join(o["spf"]).lower()
    return {
        "S1": lev_mx(o["mx"]),
        "S2": "MS" if "spf.protection.outlook.com" in spf else "G" if "_spf.google.com" in spf else "-",
        "S4": "MS" if har(o["autodiscover_cname"], "autodiscover.outlook.com") else "-",
        "S7": "MS" if har(o["dkim_selector1_cname"], ".onmicrosoft.com")
        else "G" if any(t.startswith("v=DKIM1") for t in o["dkim_google_txt"]) else "-",
        "S8": "MS" if har(o["enterpriseregistration_cname"], "enterpriseregistration.windows.net")
        or har(o["lyncdiscover_cname"], "webdir.online.lync.com") else "-",
    }


def epost(s):
    if s["S1"] in ("MS", "G"):
        return s["S1"]
    if s["S2"] == "MS" and "MS" in (s["S4"], s["S7"]):
        return "MS"
    if s["S2"] == "G" and s["S7"] == "G":
        return "G"
    if not {s["S2"], s["S4"], s["S7"]} & {"MS", "G"}:
        return "inga molnsignaler"
    return "okänd"


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
