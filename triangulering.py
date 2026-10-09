"""Triangulering T1–T4 i METOD.md: prövar huvudpåståendena med oberoende metoder.

python3 triangulering.py   # läser senaste ra-/webb-filerna för kommuner och myndigheter
Sparar bara ja/nej och ASN; omdirigeringsadresser och tenantnamn sparas inte.
"""

import glob
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import dns.resolver

from klassa_v2 import epost, signaler

ROT = Path(__file__).parent
RESOLVRAR = {"cloudflare": "1.1.1.1", "quad9": "9.9.9.9", "google": "8.8.8.8"}


class IngenOmdirigering(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


oppna_utan_omdirigering = urllib.request.build_opener(IngenOmdirigering).open


def t1_realm(doman):
    url = "https://login.microsoftonline.com/getuserrealm.srf?" + urllib.parse.urlencode(
        {"login": f"molnkartan-test@{doman}", "json": 1})
    try:
        with urllib.request.urlopen(url, timeout=15) as svar:
            return json.load(svar).get("NameSpaceType") in ("Managed", "Federated")
    except Exception:
        return None


def t2_exchange_online(doman):
    url = "https://outlook.office365.com/autodiscover/autodiscover.json?" + urllib.parse.urlencode(
        {"Email": f"molnkartan-test@{doman}", "Protocol": "Autodiscoverv1"})
    try:
        with oppna_utan_omdirigering(url, timeout=15) as svar:
            # Rättelse T2: Exchange Online kan svara direkt med en Url i stället för att omdirigera.
            return urllib.parse.urlparse(json.load(svar).get("Url", "")).hostname == "outlook.office365.com"
    except urllib.error.HTTPError as fel:
        if fel.code in (301, 302, 307, 308):
            # Bara värdnamnet jämförs; adressen i övrigt sparas inte.
            return urllib.parse.urlparse(fel.headers.get("Location", "")).hostname == "outlook.office365.com"
        return None
    except Exception:
        return None


def dns_signaler(doman, server):
    r = dns.resolver.Resolver(configure=False)
    r.nameservers, r.lifetime = [server], 8

    def fraga(namn, typ):
        try:
            return [x.to_text().strip('"') for x in r.resolve(namn, typ)]
        except Exception:
            return []

    def txt(namn):
        try:
            return ["".join(s.decode() for s in x.strings) for x in r.resolve(namn, "TXT")]
        except Exception:
            return []

    return {
        "mx": fraga(doman, "MX"),
        "spf": [t for t in txt(doman) if t.lower().startswith("v=spf1")],
        "autodiscover_cname": fraga(f"autodiscover.{doman}", "CNAME"),
        "dkim_selector1_cname": fraga(f"selector1._domainkey.{doman}", "CNAME"),
        "dkim_google_txt": [t[:40] for t in txt(f"google._domainkey.{doman}")],
        "enterpriseregistration_cname": fraga(f"enterpriseregistration.{doman}", "CNAME"),
        "lyncdiscover_cname": fraga(f"lyncdiscover.{doman}", "CNAME"),
    }


def t4_ripe(ip):
    url = f"https://stat.ripe.net/data/network-info/data.json?resource={ip}&sourceapp=molnkartan"
    try:
        with urllib.request.urlopen(url, timeout=20) as svar:
            return json.load(svar)["data"]["asns"]
    except Exception:
        return None


def senaste(monster):
    # Relativ sökväg, så att lokala mappnamn inte hamnar i rådatan.
    return str(Path(sorted(glob.glob(str(ROT / "data" / monster)))[-1]).relative_to(ROT))


def t2_med_omforsok(doman):
    svar = t2_exchange_online(doman)
    return svar if svar is not None else t2_exchange_online(doman)


def domanprov(o):
    rad = {"namn": o["namn"], "domän": o["domän"], "epost": epost(signaler(o)), "tenant": o["entra_status"] == 200,
           "t1_realm": t1_realm(o["domän"])}
    for namn, server in RESOLVRAR.items():
        rad[f"t3_{namn}"] = epost(signaler(dns_signaler(o["domän"], server)))
    return rad


def main():
    tid = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    kallor = {"kommuner": senaste("ra-organisationer-sverige-*.json"),
              "myndigheter": senaste("ra-organisationer-myndigheter-matning-*.json")}
    webbkallor = [senaste("webb-organisationer-sverige-*.json"), senaste("webb-organisationer-myndigheter-matning-*.json")]
    domaner = []
    for grupp, fil in kallor.items():
        domaner += [{**o, "grupp": grupp} for o in json.load(open(ROT / fil, encoding="utf-8"))]
    with ThreadPoolExecutor(16) as pool:
        rader = list(pool.map(domanprov, domaner))
    with ThreadPoolExecutor(2) as pool:  # Exchange Online stryper vid fler parallella anrop
        for r, exo in zip(rader, pool.map(t2_med_omforsok, [o["domän"] for o in domaner])):
            r["t2_exo"] = exo
    for r, o in zip(rader, domaner):
        r["grupp"] = o["grupp"]

    ip_asn = {}
    for fil in webbkallor:
        for o in json.load(open(ROT / fil, encoding="utf-8"))["organisationer"]:
            for n in (o.get("natverk") or {}).values():
                if n.get("ip"):
                    ip_asn[n["ip"]] = n.get("asn")
    with ThreadPoolExecutor(8) as pool:
        ripe = dict(zip(ip_asn, pool.map(t4_ripe, ip_asn)))
    t4 = [{"ip": ip, "cymru": asn, "ripe": ripe[ip]} for ip, asn in ip_asn.items()]

    ut = ROT / "data" / f"triangulering-{tid}.json"
    ut.write_text(json.dumps({"matt": tid, "kallor": {**kallor, "webb": webbkallor}, "domaner": rader, "t4": t4},
                             ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(ut)


def godkand(d):
    """Kraven i METOD.md (T1, T2, T3, T4). En körning som faller publiceras inte."""
    rader = d["domaner"]
    t1 = [r for r in rader if r["t1_realm"] is not None]
    ms = [r for r in rader if r["epost"] == "MS"]
    t4 = [x for x in d["t4"] if x["ripe"] is not None and x["cymru"]]
    return (sum(r["t1_realm"] == r["tenant"] for r in t1) / len(t1) >= 0.99
            and sum(r["t2_exo"] is True for r in ms) / len(ms) >= 0.95
            and all(sum(r[f"t3_{n}"] == r["epost"] for r in rader) / len(rader) >= 0.99 for n in RESOLVRAR)
            and sum(x["cymru"] in x["ripe"] for x in t4) / len(t4) >= 0.97)


def rapport(fil):
    d = json.load(open(fil, encoding="utf-8"))
    rader, n = d["domaner"], len(d["domaner"])
    print(f"Källa: {fil}\n")

    t1 = [r for r in rader if r["t1_realm"] is not None]
    lika = sum(r["t1_realm"] == r["tenant"] for r in t1)
    print(f"T1 tenant: OpenID och getuserrealm lika för {lika}/{len(t1)} = {lika / len(t1):.1%} (krav ≥99 %); "
          f"olika: {[r['namn'] for r in t1 if r['t1_realm'] != r['tenant']]}")

    ms = [r for r in rader if r["epost"] == "MS"]
    ja = sum(r["t2_exo"] is True for r in ms)
    print(f"T2 Exchange Online bland klassade Microsoft: {ja}/{len(ms)} = {ja / len(ms):.1%} (krav ≥95 %); "
          f"nej/okänt: {[(r['namn'], r['t2_exo']) for r in ms if r['t2_exo'] is not True]}")
    for klass in ("G", "inga molnsignaler", "okänd"):
        for grupp in ("kommuner", "myndigheter"):
            g = [r for r in rader if r["epost"] == klass and r["grupp"] == grupp]
            if g:
                print(f"   info: {grupp}, klass {klass}: Exchange Online ja för {sum(r['t2_exo'] is True for r in g)}/{len(g)}")

    for namn in RESOLVRAR:
        lika = sum(r[f"t3_{namn}"] == r["epost"] for r in rader)
        print(f"T3 {namn}: samma e-postklass för {lika}/{n} = {lika / n:.1%} (krav ≥99 %); "
              f"olika: {[(r['namn'], r['epost'], r[f't3_{namn}']) for r in rader if r[f't3_{namn}'] != r['epost']]}")

    t4 = [x for x in d["t4"] if x["ripe"] is not None and x["cymru"]]
    lika = sum(x["cymru"] in x["ripe"] for x in t4)
    print(f"T4 ASN: Team Cymru och RIPEstat lika för {lika}/{len(t4)} = {lika / len(t4):.1%} (krav ≥97 %); "
          f"olika: {[(x['ip'], x['cymru'], x['ripe']) for x in t4 if x['cymru'] not in x['ripe']][:10]}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        rapport(sys.argv[1])
    else:
        main()
