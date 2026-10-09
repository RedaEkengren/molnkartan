"""Bygger datafilerna till GitHub Pages från de senaste mätningarna:

python3 bygg_sida.py kommuner      # docs/data.json
python3 bygg_sida.py myndigheter   # docs/myndigheter.json

Varje källa väljs som senaste fil av sitt slag i data/, så sidan och
animationerna aldrig visar äldre data än rapporterna.
"""

import json
import sys
from collections import Counter
from pathlib import Path

from klassa import webb
from klassa_v2 import epost, signaler
from triangulering import godkand as triangulering_godkand
from webb_klassa import godkand as webb_godkand
from webb_klassa import har_ga, har_ga_insamling, klassa_v3, leverantor

ROT = Path(__file__).parent

GRUPPER = {
    "kommuner": {"ra": "ra-organisationer-sverige-*.json", "webb": "webb-organisationer-sverige-*.json",
                 "ut": "docs/data.json", "sakerhet": lambda g: g != "Statliga myndigheter"},
    "myndigheter": {"ra": "ra-organisationer-myndigheter-matning-*.json",
                    "webb": "webb-organisationer-myndigheter-matning-*.json",
                    "ut": "docs/myndigheter.json", "sakerhet": lambda g: g == "Statliga myndigheter"},
}


def senaste(monster):
    filer = sorted((ROT / "data").glob(monster))
    return filer[-1] if filer else None


def senaste_godkanda(monster, godkand):
    for fil in sorted((ROT / "data").glob(monster), reverse=True):
        if godkand(json.loads(fil.read_text(encoding="utf-8"))):
            return fil
    return None


def cert_godkand(d):
    """Mätning 4: svar för minst 90 % av organisationerna och nät för minst 95 % av aktiva namn."""
    org = d["organisationer"]
    svar = [o for o in org if o.get("status") == "ok"]
    aktiva = sum(o["aktiva"] for o in svar)
    okanda = sum(o["nat"].get("okänt", 0) for o in svar)
    if not ("interna_totalt" in d and len(svar) / len(org) >= 0.9 and aktiva and (aktiva - okanda) / aktiva >= 0.95):
        return False
    # T6 måste ha hållit för just den här körningen.
    for t6 in (ROT / "data").glob("triangulering-t6-*.json"):
        k = json.loads(t6.read_text(encoding="utf-8"))
        if k["kalla"] != f"data/cert-{d['matt']}.json" or sum(r["inom_15"] for r in k["rader"]) < 16:
            continue
        # T6 version 2 (#19): nollkategorin prövas separat, krav skrivna före körningen.
        if k.get("version", 1) >= 2 and not (k["noll"]["av"] >= 5 and k["noll"]["lika"] / k["noll"]["av"] >= 0.9):
            continue
        return True
    return False


def senaste_godkanda_webb(monster):
    """Senaste webbmätning som klarar samma kvalitetskontroll som rapporten (#13).
    En körning som faller publiceras inte, men behålls i data/."""
    return senaste_godkanda(monster, webb_godkand)


def las(fil):
    return json.loads(fil.read_text(encoding="utf-8")) if fil else None


def relativ(fil):
    return str(fil.relative_to(ROT)) if fil else None


def triangulering_avser(tri, ra_fil, grupp):
    """Gäller trianguleringen samma DNS-fil som sidan visar? Annars är den en separat,
    daterad observation och får inte kallas bekräftelse (#18)."""
    return bool(tri and ra_fil and tri.get("kallor", {}).get(grupp) == relativ(ra_fil))


def bygg(grupp):
    g = GRUPPER[grupp]
    ra_fil, webb_fil = senaste(g["ra"]), senaste_godkanda_webb(g["webb"])
    # Bara körningar som klarar sina krav (METOD.md, "Publicering").
    tri_fil = senaste_godkanda("triangulering-20*Z.json", triangulering_godkand)
    cert_fil = senaste_godkanda("cert-*.json", cert_godkand)
    sak_fil = senaste_godkanda("sakerhet-*.json", lambda d: d.get("fel_andel", 1) <= 0.02)
    data, webb_data, tri, sak = las(ra_fil), las(webb_fil), las(tri_fil), las(sak_fil)
    cert = {o["domän"]: o for o in (las(cert_fil) or {}).get("organisationer", [])}

    fore = {}
    for w in (webb_data or {}).get("organisationer", []):
        varder = [{"v": v, "nat": w["natverk"][v].get("nat"),
                   "lev": (leverantor(v) or {}).get("leverantor")} for v in w.get("w2", [])]
        us = sorted(x["v"] for x in varder if x["nat"] == "US")
        fore[w["domän"]] = {
            "klass": klassa_v3(w),
            "ga": har_ga(w),
            "gaInsamling": har_ga_insamling(w),
            "us": us,
            "usLeverantorer": sorted({(leverantor(v) or {}).get("leverantor") or ".".join(v.split(".")[-2:]) for v in us}),
            # Alla tredjepartsvärdar med nät, till animationen "Så mäts en webbplats".
            "varder": varder,
            "sida": w.get("slutadress"),
        }
    exo = {r["domän"]: r["t2_exo"] for r in (tri or {}).get("domaner", [])}

    organisationer = []
    for o in data:
        s = signaler(o)
        organisationer.append({
            "namn": o["namn"],
            "kod": o.get("kod"),
            "typ": o["typ"],
            "lan": o.get("lan", ""),
            "antal": int(o.get("antal") or 1),
            "doman": o["domän"],
            "epost": epost(s),
            "tenant": o["entra_status"] == 200,
            "exo": exo.get(o["domän"]),
            "teams": s["S8"] == "MS",
            "webb": webb(o["www_asn_namn"]),
            "webbLeverantor": o["www_asn_namn"],
            "signaler": s,
            "fore_samtycke": fore.get(o["domän"]),
            # Mätning 4: antal publika tjänstenamn och hur många av dem som ligger på amerikanska nät.
            "tjanster": ({"aktiva": cert[o["domän"]]["aktiva"], "us": cert[o["domän"]]["nat"].get("US", 0)}
                         if cert.get(o["domän"], {}).get("aktiva") else None),
            # Riktiga svar till animationen "Så mäts en kommun".
            "svar": {
                "mx": [m.split()[-1].rstrip(".") for m in sorted(o["mx"], key=lambda m: int(m.split()[0]))],
                "spf": next((i for i in ("spf.protection.outlook.com", "_spf.google.com")
                             if any(i in x for x in o["spf"])), None),
                # Bara leverantörens del: hela målet innehåller tenantnamnet, som inte publiceras.
                "dkim": next((s for s in ("onmicrosoft.com", "dkim.mail.microsoft")
                              if any(c.rstrip(".").endswith(s) for c in o["dkim_selector1_cname"])),
                             "annan" if o["dkim_selector1_cname"] else None),
                "entra": o["entra_status"],
            },
        })

    sakerhet = {}
    if sak:
        for namn, signaler_ in sak["per_grupp"].items():
            if g["sakerhet"](namn):
                for signal, varden in signaler_.items():
                    sakerhet.setdefault(signal, Counter()).update(varden)

    ut = {
        "matt": data[0]["matt"], "kalla": relativ(ra_fil),
        "webbMatt": webb_data and webb_data["matt"], "webbKalla": relativ(webb_fil),
        "trianguleringMatt": tri and tri["matt"], "trianguleringKalla": relativ(tri_fil),
        "trianguleringAvserSammaDns": triangulering_avser(tri, ra_fil, grupp),
        "sakerhetMatt": sak and sak["matt"], "sakerhetKalla": relativ(sak_fil),
        "certKalla": relativ(cert_fil), "certMatt": las(cert_fil)["matt"] if cert_fil else None,
        "sakerhet": {k: dict(v) for k, v in sakerhet.items()},
        "organisationer": organisationer,
    }
    utfil = ROT / g["ut"]
    utfil.parent.mkdir(exist_ok=True)
    utfil.write_text(json.dumps(ut, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{g['ut']}: {len(organisationer)} organisationer")


if __name__ == "__main__":
    for grupp in sys.argv[1:] or GRUPPER:
        bygg(grupp)
