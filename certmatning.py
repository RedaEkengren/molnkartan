"""Mätning 4 i METOD.md: hur stor del av en organisations publika tjänster som körs på amerikanska nät.

python3 certmatning.py organisationer-sverige.csv [organisationer-myndigheter-matning.csv ...]
python3 certmatning.py --t6        # Certspotter för 20 slumpvis valda, jämfört med senaste crt.sh-körningen
Sparar bara antal per organisation, aldrig värdnamn (gränsen i METOD.md).
"""

import csv
import glob
import ipaddress
import json
import random
import sys
import threading
import time
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from matning import fraga
from webbmatning import natverk

ROT = Path(__file__).parent
PLATTFORMAR = ("sharepoint.com", "azurewebsites.net", "cloudapp.azure.com", "azurefd.net", "trafficmanager.net",
               "amazonaws.com", "cloudfront.net", "elb.amazonaws.com", "herokuapp.com", "googleusercontent.com",
               "ghs.googlehosted.com", "github.io", "zendesk.com", "cloudflare.net", "netlify.app", "vercel-dns.com")


CGNAT = ipaddress.ip_network("100.64.0.0/10")
_interna = [0]
_interna_las = threading.Lock()


def hamta_json(url, forsok=4):
    for i in range(forsok):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "molnkartan (+https://github.com/RedaEkengren/molnkartan)"}), timeout=90) as svar:
                return json.load(svar)
        except Exception:
            time.sleep(8 * (i + 1))
    return None


def namn_crtsh(doman):
    d = hamta_json(f"https://crt.sh/?q={urllib.parse.quote('%.' + doman)}&output=json&exclude=expired")
    return None if d is None else {n for r in d for n in r["name_value"].lower().split()}


_takt = threading.Lock()
_senast = [0.0]


def certspotter_sida(url):
    with _takt:  # högst 100 anrop i timmen, delat mellan trådar
        vanta = _senast[0] + 37 - time.monotonic()
        if vanta > 0:
            time.sleep(vanta)
        _senast[0] = time.monotonic()
    return hamta_json(url, forsok=2)


def namn_certspotter(doman):
    namn, efter = set(), None
    while True:
        url = f"https://api.certspotter.com/v1/issuances?domain={doman}&include_subdomains=true&expand=dns_names"
        sida = certspotter_sida(url + (f"&after={efter}" if efter else ""))
        if sida is None:
            return None if not namn and efter is None else namn
        namn |= {n for r in sida for n in r["dns_names"]}
        if len(sida) < 100:
            return namn
        efter = sida[-1]["id"]


def namn_med_reserv(doman):
    namn = namn_crtsh(doman)
    if namn is not None:
        return namn, "crt.sh"
    namn = namn_certspotter(doman)
    return namn, ("certspotter" if namn is not None else None)


def summera(doman, namn):
    """Slår upp namnen och returnerar bara antal. Värdnamnen lämnar inte funktionen."""
    if namn is None:
        return {"status": "inget svar"}
    giltiga = sorted(n.rstrip(".") for n in namn if not n.startswith("*") and (n == doman or n.endswith("." + doman)))
    nat, plattform, aktiva = Counter(), Counter(), 0
    for n in giltiga:
        a = fraga(n, "A")
        if not a:
            continue
        ip = ipaddress.ip_address(a[0])
        if ip.is_private or ip.is_reserved or ip in CGNAT:
            with _interna_las:  # rättelse: inte en publik tjänst; bara totalen sparas
                _interna[0] += 1
            continue
        aktiva += 1
        nat[natverk(n).get("nat") or "okänt"] += 1
        mal = (fraga(n, "CNAME") or [""])[0].rstrip(".").lower()
        for p in PLATTFORMAR:
            if mal == p or mal.endswith("." + p):
                plattform[p] += 1
                break
    return {"status": "ok", "namn_i_loggar": len(giltiga), "aktiva": aktiva, "nat": dict(nat), "plattform": dict(plattform)}


def mat(rad, kalla=None):
    if kalla is None:
        namn, kalla_namn = namn_med_reserv(rad["domän"])
    else:
        namn, kalla_namn = kalla(rad["domän"]), kalla.__name__.removeprefix("namn_")
    return {"namn": rad["namn"], "domän": rad["domän"], "kalla": kalla_namn, **summera(rad["domän"], namn)}


def andel_us(r):
    return r["nat"].get("US", 0) / r["aktiva"] if r.get("aktiva") else None


def t6():
    senaste = sorted(glob.glob(str(ROT / "data" / "cert-*.json")))[-1]
    d = json.load(open(senaste, encoding="utf-8"))
    kandidater = sorted((o for o in d["organisationer"] if o.get("aktiva")), key=lambda o: o["domän"])
    urval = random.Random(20261008).sample(kandidater, 20)
    rader, lika = [], 0
    for o in urval:
        cs = mat(o, namn_crtsh if o.get("kalla") == "certspotter" else namn_certspotter)
        a, b = andel_us(o), andel_us(cs)
        ok = a is not None and b is not None and abs(a - b) <= 0.15
        lika += ok
        rader.append({"namn": o["namn"], "huvudkalla": o.get("kalla"), "andel_us_huvud": round(a, 3) if a is not None else None,
                      "andel_us_andra": round(b, 3) if b is not None else None, "andra_kalla": cs.get("kalla"), "inom_15": ok,
                      "aktiva_huvud": o["aktiva"], "aktiva_andra": cs.get("aktiva")})
        print(f"{o['namn'][:36]:36} {o.get('kalla')} {a:.0%} ({o['aktiva']})  {cs.get('kalla')} " +
              (f"{b:.0%} ({cs['aktiva']})" if b is not None else str(cs.get("status"))) + ("  ✓" if ok else "  ✗"))
        time.sleep(2)
    print(f"\nT6: inom 15 procentenheter för {lika}/20 (krav ≥16)")
    ut = ROT / "data" / f"triangulering-t6-{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}.json"
    ut.write_text(json.dumps({"kalla": str(Path(senaste).relative_to(ROT)), "rader": rader}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(ut.relative_to(ROT))


def main():
    if sys.argv[1:] == ["--t6"]:
        return t6()
    tid = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    rader = []
    for lista in sys.argv[1:]:
        rader += list(csv.DictReader(open(ROT / lista, encoding="utf-8")))
    with ThreadPoolExecutor(4) as pool:  # crt.sh är delad och ofta överbelastad; Certspotter-takten styrs av _takt
        resultat = list(pool.map(mat, rader))
    ut = ROT / "data" / f"cert-{tid}.json"
    ut.write_text(json.dumps({"matt": tid, "listor": sys.argv[1:], "interna_totalt": _interna[0], "organisationer": resultat},
                             ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(ut.relative_to(ROT))


if __name__ == "__main__":
    main()
