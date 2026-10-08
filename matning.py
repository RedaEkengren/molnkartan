"""Mäter öppna DNS/HTTP-signaler enligt METOD.md och sparar rådata i data/."""

import csv
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import dns.resolver

ROT = Path(__file__).parent
resolver = dns.resolver.Resolver()
resolver.lifetime = 8


def fraga(namn, typ):
    try:
        return [r.to_text().strip('"') for r in resolver.resolve(namn, typ)]
    except Exception:
        return []


def txt(namn):
    # TXT-poster kan vara uppdelade i flera strängar; slå ihop dem.
    try:
        return ["".join(s.decode() for s in r.strings) for r in resolver.resolve(namn, "TXT")]
    except Exception:
        return []


def asn_for_ip(ip):
    omvand = ".".join(reversed(ip.split(".")))
    rad = txt(f"{omvand}.origin.asn.cymru.com")
    if not rad:
        return None, None
    asn = rad[0].split("|")[0].strip().split()[0]
    namn = txt(f"AS{asn}.asn.cymru.com")
    return asn, (namn[0].split("|")[-1].strip() if namn else None)


def entra_tenant(doman):
    url = f"https://login.microsoftonline.com/{doman}/v2.0/.well-known/openid-configuration"
    try:
        with urllib.request.urlopen(url, timeout=10) as svar:
            return svar.status
    except urllib.error.HTTPError as fel:
        return fel.code
    except Exception as fel:
        return f"fel: {fel}"


def mat(doman):
    mx = sorted(fraga(doman, "MX"))
    alla_txt = txt(doman)
    spf = [t for t in alla_txt if t.lower().startswith("v=spf1")]
    # Bara vilken sorts verifiering som finns, inte själva koden.
    verifiering = sorted({t.split("=")[0] + "=" for t in alla_txt if t.startswith(("MS=", "google-site-verification="))})
    autodiscover = fraga(f"autodiscover.{doman}", "CNAME")
    www_ip = fraga(f"www.{doman}", "A") or fraga(doman, "A")
    asn, asn_namn = asn_for_ip(www_ip[0]) if www_ip else (None, None)
    return {
        "dkim_selector1_cname": fraga(f"selector1._domainkey.{doman}", "CNAME"),
        "dkim_google_txt": [t[:40] for t in txt(f"google._domainkey.{doman}")],
        "enterpriseregistration_cname": fraga(f"enterpriseregistration.{doman}", "CNAME"),
        "lyncdiscover_cname": fraga(f"lyncdiscover.{doman}", "CNAME"),
        "mx": mx,
        "spf": spf,
        "verifiering": verifiering,
        "autodiscover_cname": autodiscover,
        "www_ip": www_ip,
        "www_asn": asn,
        "www_asn_namn": asn_namn,
        # Tenant-ID sparas inte: bara om kontot finns behövs för slutsatserna.
        "entra_status": entra_tenant(doman),
    }


def main():
    lista = sys.argv[1] if len(sys.argv) > 1 else "organisationer.csv"
    tid = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    resultat = []
    with open(ROT / lista, encoding="utf-8") as f:
        for rad in csv.DictReader(f):
            print(rad["domän"], file=sys.stderr)
            resultat.append({**rad, "matt": tid, **mat(rad["domän"])})
    ut = ROT / "data" / f"ra-{Path(lista).stem}-{tid}.json"
    ut.write_text(json.dumps(resultat, ensure_ascii=False, indent=2), encoding="utf-8")
    print(ut)


if __name__ == "__main__":
    main()
