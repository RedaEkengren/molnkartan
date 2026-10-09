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


class DnsFel(Exception):
    """Uppslaget misslyckades (timeout, SERVFAIL). Räknas som fel, aldrig som "saknas"."""


def txt(namn):
    try:
        return ["".join(s.decode() for s in r.strings) for r in res.resolve(namn, "TXT")]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return []
    except Exception as fel:
        raise DnsFel(str(fel)) from fel


def har_ds(doman):
    try:
        return len(res.resolve(doman, "DS")) > 0
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False
    except Exception as fel:
        raise DnsFel(str(fel)) from fel


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


def dns_signaler(d):
    varden = {}
    for signal, funktion in (("DMARC", lambda: dmarc(d)), ("SPF", lambda: spf(d)),
                             ("MTA-STS", lambda: "finns" if any(t.startswith("v=STSv1") for t in txt(f"_mta-sts.{d}")) else "saknas"),
                             ("TLS-RPT", lambda: "finns" if any(t.startswith("v=TLSRPTv1") for t in txt(f"_smtp._tls.{d}")) else "saknas"),
                             ("DNSSEC", lambda: "finns" if har_ds(d) else "saknas")):
        try:
            varden[signal] = funktion()
        except DnsFel:
            varden[signal] = "fel"
    return varden


def mat(rad):
    d = rad["domän"]
    webb = f"https://{rad['webb']}/" if rad.get("webb") else f"https://www.{d}/"
    return {**dns_signaler(d), "HSTS": hsts(webb)}


def kontroller():
    fakta = {"cloudflare.com DS": har_ds("cloudflare.com"), "google.com DS": har_ds("google.com"),
             "google.com DMARC": dmarc("google.com"), "google.com MTA-STS": any(t.startswith("v=STSv1") for t in txt("_mta-sts.google.com"))}
    if fakta != {"cloudflare.com DS": True, "google.com DS": False, "google.com DMARC": "p=reject", "google.com MTA-STS": True}:
        sys.exit(f"Kontroll fallerade: {fakta}")
    return fakta


def main():
    tid = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    fakta = kontroller()
    grupper = []
    kommuner = list(csv.DictReader(open(ROT / "organisationer-sverige.csv", encoding="utf-8")))
    storlek = Counter(r["lan"] for r in kommuner)
    # Gränsen: ett län med färre än 5 organisationer (Gotland, 1) skulle visa enskilda värden.
    # Det slås ihop med det minsta av de övriga länen.
    minsta = min((l for l in storlek if storlek[l] >= 5), key=lambda l: (storlek[l], l))
    sma = sorted(l for l in storlek if storlek[l] < 5)
    sammanslagen = " och ".join([minsta.removesuffix(" län")] + [l.removesuffix(" län") for l in sma]) + " län"
    for r in kommuner:
        grupper.append((sammanslagen if r["lan"] in sma or r["lan"] == minsta else r["lan"], r))
    for r in csv.DictReader(open(ROT / "organisationer-myndigheter-matning.csv", encoding="utf-8")):
        grupper.append(("Statliga myndigheter", r))
    with ThreadPoolExecutor(12) as pool:
        resultat = list(pool.map(mat, [r for _, r in grupper]))
    # Kontroll: DNS-signalerna igen via 9.9.9.9. Bara antal lika sparas, inga värden per organisation.
    res.nameservers = ["9.9.9.9"]
    with ThreadPoolExecutor(12) as pool:
        kontroll = list(pool.map(lambda r: dns_signaler(r["domän"]), [r for _, r in grupper]))
    res.nameservers = ["1.1.1.1"]
    lika = {s: sum(a[s] == b[s] for a, b in zip(resultat, kontroll)) for s in kontroll[0]}
    fel = sum(v == "fel" for r in resultat for v in r.values())
    summa = defaultdict(lambda: defaultdict(Counter))
    antal = Counter()
    for (grupp, _), varden in zip(grupper, resultat):
        antal[grupp] += 1
        for signal, varde in varden.items():
            summa[grupp][signal][varde] += 1
    ut = ROT / "data" / f"sakerhet-{tid}.json"
    ut.write_text(json.dumps({"matt": tid, "kontroller": fakta, "fel_andel": round(fel / (len(resultat) * 6), 4),
                              "lika_9999": lika, "antal": antal,
                              "per_grupp": {g: {s: dict(c) for s, c in v.items()} for g, v in summa.items()}},
                             ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(ut.relative_to(ROT))


if __name__ == "__main__":
    main()
