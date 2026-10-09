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


class DnsFel(Exception):
    """Uppslaget misslyckades (timeout, SERVFAIL, nätfel). Ett mätfel, inte ett svar."""


SAKNAS = (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer)


def fraga(namn, typ, strikt=False, res=None):
    """Svarar med posterna, eller [] om posten inte finns. Vid mätfel: [] om inte
    strikt, annars DnsFel. Mätningar som klassar något ska använda strikt (#9)."""
    try:
        return [r.to_text().strip('"') for r in (res or resolver).resolve(namn, typ)]
    except SAKNAS:
        return []
    except Exception as fel:
        if strikt:
            raise DnsFel(f"{typ}: {type(fel).__name__}") from fel
        return []


def txt(namn, strikt=False, res=None):
    # TXT-poster kan vara uppdelade i flera strängar; slå ihop dem.
    try:
        return ["".join(s.decode() for s in r.strings) for r in (res or resolver).resolve(namn, "TXT")]
    except SAKNAS:
        return []
    except Exception as fel:
        if strikt:
            raise DnsFel(f"TXT: {type(fel).__name__}") from fel
        return []


def dns_poster(doman, res=None):
    """E-postens DNS-signaler. Fältnamn i dns_fel anger uppslag som misslyckades;
    värdnamn sparas inte där."""
    fel = []

    def hamta(falt, funktion):
        try:
            return funktion()
        except DnsFel:
            fel.append(falt)
            return []

    alla_txt = hamta("txt", lambda: txt(doman, True, res))
    return {
        "mx": sorted(hamta("mx", lambda: fraga(doman, "MX", True, res))),
        "spf": [t for t in alla_txt if t.lower().startswith("v=spf1")],
        # Bara vilken sorts verifiering som finns, inte själva koden.
        "verifiering": sorted({t.split("=")[0] + "=" for t in alla_txt if t.startswith(("MS=", "google-site-verification="))}),
        "autodiscover_cname": hamta("autodiscover", lambda: fraga(f"autodiscover.{doman}", "CNAME", True, res)),
        "dkim_selector1_cname": hamta("dkim_selector1", lambda: fraga(f"selector1._domainkey.{doman}", "CNAME", True, res)),
        "dkim_google_txt": [t[:40] for t in hamta("dkim_google", lambda: txt(f"google._domainkey.{doman}", True, res))],
        "enterpriseregistration_cname": hamta("enterpriseregistration", lambda: fraga(f"enterpriseregistration.{doman}", "CNAME", True, res)),
        "lyncdiscover_cname": hamta("lyncdiscover", lambda: fraga(f"lyncdiscover.{doman}", "CNAME", True, res)),
        "dns_fel": sorted(fel),
    }


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
    www_ip = fraga(f"www.{doman}", "A") or fraga(doman, "A")
    asn, asn_namn = asn_for_ip(www_ip[0]) if www_ip else (None, None)
    return {
        **dns_poster(doman),
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
