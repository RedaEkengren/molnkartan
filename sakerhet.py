"""Mätning 5 i METOD.md: säkerhetsgrunder, redovisade bara i aggregat.

python3 sakerhet.py   # kommuner/regioner per län och myndigheter som grupp
Värden per organisation finns bara i minnet; filen i data/ har bara antal.
"""

import csv
import json
import sys
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import dns.resolver

from webbmatning import ANVANDARAGENT

ROT = Path(__file__).parent
res = dns.resolver.Resolver(configure=False)
res.nameservers, res.lifetime = ["1.1.1.1"], 8


def txt(namn):
    try:
        return ["".join(s.decode() for s in r.strings) for r in res.resolve(namn, "TXT")]
    except Exception:
        return []


def har_ds(doman):
    try:
        return len(res.resolve(doman, "DS")) > 0
    except Exception:
        return False


def dmarc(doman):
    for t in txt(f"_dmarc.{doman}"):
        if t.lower().startswith("v=dmarc1"):
            p = [d.split("=", 1)[1].strip().lower() for d in t.split(";") if d.strip().lower().startswith("p=")]
            return f"p={p[0]}" if p and p[0] in ("reject", "quarantine", "none") else "felaktig"
    return "saknas"


def spf(doman):
    poster = [t for t in txt(doman) if t.lower().startswith("v=spf1")]
    if not poster:
        return "saknas"
    slut = poster[0].strip().split()[-1].lower()
    return slut if slut in ("-all", "~all") else "annat"


def hsts(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ANVANDARAGENT})
        with urllib.request.urlopen(req, timeout=20) as svar:
            varde = svar.headers.get("Strict-Transport-Security", "")
        alder = [d.split("=", 1)[1] for d in varde.replace(" ", "").split(";") if d.lower().startswith("max-age=")]
        return "finns" if alder and alder[0].isdigit() and int(alder[0]) > 0 else "saknas"
    except Exception:
        return "kunde inte mätas"


def mat(rad):
    d = rad["domän"]
    webb = f"https://{rad['webb']}/" if rad.get("webb") else f"https://www.{d}/"
    return {
        "DMARC": dmarc(d),
        "SPF": spf(d),
        "MTA-STS": "finns" if any(t.startswith("v=STSv1") for t in txt(f"_mta-sts.{d}")) else "saknas",
        "TLS-RPT": "finns" if any(t.startswith("v=TLSRPTv1") for t in txt(f"_smtp._tls.{d}")) else "saknas",
        "DNSSEC": "finns" if har_ds(d) else "saknas",
        "HSTS": hsts(webb),
    }


def kontroller():
    fakta = {"cloudflare.com DS": har_ds("cloudflare.com"), "google.com DS": har_ds("google.com"),
             "google.com DMARC": dmarc("google.com"), "google.com MTA-STS": any(t.startswith("v=STSv1") for t in txt("_mta-sts.google.com"))}
    if fakta != {"cloudflare.com DS": True, "google.com DS": False, "google.com DMARC": "p=reject", "google.com MTA-STS": True}:
        sys.exit(f"Kontroll fallerade: {fakta}")
    return fakta


def main():
    tid = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    kontroll = kontroller()
    grupper = []
    for r in csv.DictReader(open(ROT / "organisationer-sverige.csv", encoding="utf-8")):
        grupper.append((r["lan"], r))
    for r in csv.DictReader(open(ROT / "organisationer-myndigheter-matning.csv", encoding="utf-8")):
        grupper.append(("Statliga myndigheter", r))
    with ThreadPoolExecutor(12) as pool:
        resultat = list(pool.map(mat, [r for _, r in grupper]))
    summa = defaultdict(lambda: defaultdict(Counter))
    antal = Counter()
    for (grupp, _), varden in zip(grupper, resultat):
        antal[grupp] += 1
        for signal, varde in varden.items():
            summa[grupp][signal][varde] += 1
    ut = ROT / "data" / f"sakerhet-{tid}.json"
    ut.write_text(json.dumps({"matt": tid, "kontroller": kontroll, "antal": antal,
                              "per_grupp": {g: {s: dict(c) for s, c in v.items()} for g, v in summa.items()}},
                             ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(ut.relative_to(ROT))


if __name__ == "__main__":
    main()
