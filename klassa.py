"""Tillämpar reglerna i METOD.md på senaste rådatafilen i data/."""

import glob
import json
from collections import Counter


def under(varde, doman):
    """Exakt domän eller underdomän: notgoogle.com ligger inte under google.com (#17)."""
    varde = varde.rstrip(".").lower()
    return varde == doman or varde.endswith("." + doman)


def lev_mx(mx):
    vardar = [m.split()[-1] for m in mx]
    ms = [under(v, "mail.protection.outlook.com") for v in vardar]
    g = [under(v, "google.com") or under(v, "googlemail.com") for v in vardar]
    if vardar and all(ms):
        return "MS"
    if vardar and all(g):
        return "G"
    if any(ms):
        return "blandat"
    return "gateway/egen"


def epost(o):
    s1 = lev_mx(o["mx"])
    if s1 in ("MS", "G"):
        return s1, "S1"
    s2 = any("spf.protection.outlook.com" in s for s in o["spf"])
    s4 = any(c.rstrip(".").lower() == "autodiscover.outlook.com" for c in o["autodiscover_cname"])
    if s2 and s4:
        return "MS", "S2+S4"
    return "okänd", f"S1={s1} S2={'MS' if s2 else '-'} S4={'MS' if s4 else '-'}"


def webb(namn):
    namn = (namn or "").upper()
    for nyckel, lev in (("MICROSOFT", "MS"), ("GOOGLE", "G"), ("AMAZON", "AWS"), ("CLOUDFLARE", "Cloudflare"), ("AKAMAI", "Akamai"), ("FASTLY", "Fastly")):
        if nyckel in namn:
            return lev
    return "SE/EU" if namn.endswith((", SE", ", EU")) else "okänd"


def main():
    fil = sorted(glob.glob("data/ra-2026-*.json"))[-1]
    data = json.load(open(fil, encoding="utf-8"))
    print(f"Källa: {fil}\n")
    print(f"| Organisation | E-post | Grund | MS-tenant | Webb |\n|---|---|---|---|---|")
    rakna = Counter()
    for o in data:
        lev, grund = epost(o)
        rakna[lev] += 1
        tenant = "ja" if o["entra_status"] == 200 else "nej"
        print(f"| {o['namn']} | {lev} | {grund} | {tenant} | {webb(o['www_asn_namn'])} ({o['www_asn_namn']}) |")
    entydiga = rakna["MS"] + rakna["G"]
    print(f"\nE-post: {dict(rakna)}  entydiga={entydiga}/{len(data)}")
    print("Pilot enligt METOD.md:", "LYCKAD" if entydiga >= 22 and rakna["okänd"] <= 5 else "MISSLYCKAD")


if __name__ == "__main__":
    main()
