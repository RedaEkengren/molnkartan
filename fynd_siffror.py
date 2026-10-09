"""Räknar fram varje siffra på fyndsidan från de filer sidan publicerar (samma val som bygg_sida.py).

python3 fynd_siffror.py          # skriver ut siffrorna
tests/test_fynd.py kontrollerar att docs/fynd.html innehåller exakt dessa siffror och namn.
Definitionerna står här, så att ingen siffra på sidan saknar en reproducerbar källa.
"""

import json
from collections import Counter
from pathlib import Path

import bygg_sida
from klassa_v2 import epost, signaler, stoder
from webb_klassa import har_ga, har_ga_insamling, klassa_v3, leverantor

ROT = Path(__file__).parent

# Fynden gäller en bestämd mätning. Filerna låses här, så att månadsmätningarna
# inte ändrar vad ett daterat fynd säger; korten och kartan följer senaste data.
FYND_KALLOR = {
    "ra_kommuner": "data/ra-organisationer-sverige-2026-10-08T154137Z.json",
    "ra_myndigheter": "data/ra-organisationer-myndigheter-matning-2026-10-08T164214Z.json",
    "webb_kommuner": "data/webb-organisationer-sverige-2026-10-08T162614Z.json",
    "webb_myndigheter": "data/webb-organisationer-myndigheter-matning-2026-10-08T164403Z.json",
    "triangulering": "data/triangulering-2026-10-08T165750Z.json",
    "sakerhet": "data/sakerhet-2026-10-09T004643Z.json",
    "cert": "data/cert-2026-10-08T204928Z.json",
    "t6": "data/triangulering-t6-2026-10-09T081527Z.json",
}

# Samtyckesverktyg (CMP): registrerade domäner för verktygen själva, inte för tjänster de styr.
SAMTYCKESVERKTYG = {
    "cookiebot.com": "Cookiebot", "cookiebot.eu": "Cookiebot", "usercentrics.eu": "Usercentrics",
    "consentmanager.net": "consentmanager", "cookieinformation.com": "Cookie Information",
    "cookietractor.com": "Cookie Tractor", "cookie-script.com": "Cookie-Script", "onetrust.com": "OneTrust",
    "cookielaw.org": "OneTrust", "cookieyes.com": "CookieYes", "kiprotect.com": "KIProtect (Klaro)",
}


def las(fil):
    return json.loads(Path(fil).read_text(encoding="utf-8"))


def us_varder(o):
    return [v for v in o.get("w2", []) if o["natverk"][v].get("nat") == "US"]


def ar_cmp(v):
    return any(v == d or v.endswith("." + d) for d in SAMTYCKESVERKTYG)


def cert_siffror(cert, t6):
    """Mätning 4: andel publika namn under organisationens domän som ligger på amerikanska nät.
    Ordningen följer listorna: 290 kommuner, 20 regioner, sedan myndighetsdomänerna."""
    import csv
    import statistics
    assert bygg_sida.cert_godkand(cert), "fynden får bara bygga på godkända körningar"
    typer = [r["typ"] for r in csv.DictReader(open(ROT / "organisationer-sverige.csv", encoding="utf-8"))]
    org = cert["organisationer"]
    grupper = {"kommuner": [o for o, t in zip(org, typer) if t == "kommun"],
               "regioner": [o for o, t in zip(org, typer) if t == "region"],
               "myndigheter": org[len(typer):]}
    ut = {}
    for namn, g in grupper.items():
        med = [o for o in g if o.get("aktiva")]
        aktiva = sum(o["aktiva"] for o in med)
        us = sum(o["nat"].get("US", 0) for o in med)
        andelar = [o["nat"].get("US", 0) / o["aktiva"] for o in med]
        storst = max(o["nat"].get("US", 0) for o in med)
        ut[f"cert_{namn}"] = {"org": len(med), "aktiva": aktiva, "us": us, "andel": round(100 * us / aktiva, 1),
                               "median": round(100 * statistics.median(andelar)), "noll": sum(a == 0 for a in andelar),
                               "minst_en": sum(a > 0 for a in andelar), "storsta_andel_av_us": round(100 * storst / us)}
    ut["cert_interna"] = cert["interna_totalt"]
    nat = Counter()
    for o in cert["organisationer"]:
        nat.update(o.get("nat", {}))
    ut["cert_nat"] = dict(nat)
    # #19: kontrollens avvikelser från nollkategorin (0 % i huvudkällan, >0 % i den andra).
    ut["t6_noll_till_positiv"] = [r["namn"] for r in t6["rader"]
                                  if r["andel_us_huvud"] == 0 and (r["andel_us_andra"] or 0) > 0]
    ut["t6"] = (sum(r["inom_15"] for r in t6["rader"]), len(t6["rader"]))
    return ut


def siffror():
    f = {k: las(ROT / v) for k, v in FYND_KALLOR.items()}
    ra_k, ra_m, tri, sak = f["ra_kommuner"], f["ra_myndigheter"], f["triangulering"], f["sakerhet"]
    webb_k, webb_m = f["webb_kommuner"]["organisationer"], f["webb_myndigheter"]["organisationer"]
    assert bygg_sida.triangulering_godkand(tri) and sak["fel_andel"] <= 0.02, "fynden får bara bygga på godkända körningar"

    exo = {(r["grupp"], r["domän"]): r["t2_exo"] for r in tri["domaner"]}
    klass_k = {o["domän"]: epost(signaler(o)) for o in ra_k}
    exo_k = {d: exo[("kommuner", d)] for d in klass_k}
    klass_m = {o["domän"]: epost(signaler(o)) for o in ra_m}
    exo_m = {d: exo[("myndigheter", d)] for d in klass_m}

    matbara_k = [o for o in webb_k if klassa_v3(o) != "kunde inte mätas"]
    matbara_m = [o for o in webb_m if klassa_v3(o) != "kunde inte mätas"]
    ga_k = [o for o in matbara_k if har_ga(o)]
    ga_m = [o for o in matbara_m if har_ga(o)]

    cmp_org = [o for o in matbara_k if any(ar_cmp(v) for v in us_varder(o))]
    cmp_myndigheter = sum(any(ar_cmp(v) for v in us_varder(o)) for o in matbara_m)
    cmp_enda = [o for o in cmp_org if all(ar_cmp(v) for v in us_varder(o))]
    cmp_nat = Counter()
    for o in cmp_org:
        for v in us_varder(o):
            if ar_cmp(v):
                verktyg = next(n for d, n in SAMTYCKESVERKTYG.items() if v == d or v.endswith("." + d))
                cmp_nat[(verktyg, o["natverk"][v]["namn"].split(" - ")[-1].split(",")[0].split(" ")[0])] += 0
                cmp_nat[(verktyg, o["natverk"][v]["namn"].split(" - ")[-1].split(",")[0].split(" ")[0], o["domän"])] = 1

    lev_k = Counter()
    for o in matbara_k:
        for l in {(leverantor(v) or {}).get("leverantor") or ".".join(v.split(".")[-2:]) for v in us_varder(o)}:
            lev_k[l] += 1

    webbhotell = {o["domän"]: (o["www_asn_namn"] or "") for o in ra_k}
    ingen = [o for o in matbara_k if klassa_v3(o) == "ingen tredjepart"]
    ingen_us_hotell = [o["namn"] for o in ingen
                       if any(n in webbhotell[o["domän"]].upper() for n in ("CLOUDFLARE", "AMAZON", "MICROSOFT", "GOOGLE", "AKAMAI", "FASTLY"))]

    lan = {o["domän"]: o["lan"] for o in ra_k}
    g_ms = [o["namn"] for o in ra_k if klass_k[o["domän"]] == "G" and stoder(signaler(o)["S7"], "MS")]

    sak_k = Counter()
    for grupp, v in sak["per_grupp"].items():
        if grupp != "Statliga myndigheter":
            for signal, c in v.items():
                sak_k[signal + " " + max(c, key=c.get)] += 0  # säkerställer nycklar
                for varde, n in c.items():
                    sak_k[(signal, varde)] += n

    return {
        "kallor": FYND_KALLOR,
        "exo_kommuner": sum(v is True for v in exo_k.values()),
        "exo_okand": (sum(exo_k[d] is True for d, c in klass_k.items() if c == "okänd"), sum(c == "okänd" for c in klass_k.values())),
        "exo_inga": (sum(exo_k[d] is True for d, c in klass_k.items() if c == "inga molnsignaler"), sum(c == "inga molnsignaler" for c in klass_k.values())),
        "exo_google": (sum(exo_k[d] is True for d, c in klass_k.items() if c == "G"), sum(c == "G" for c in klass_k.values())),
        "exo_myndigheter": sum(v is True for v in exo_m.values()),
        "exo_myndigheter_dolda": sum(exo_m[d] is True for d, c in klass_m.items() if c != "MS"),
        "dns_ms_kommuner": sum(c == "MS" for c in klass_k.values()),
        "dns_ms_g_kommuner": [o["namn"] for o in ra_k if klass_k[o["domän"]] == "MS+G"],
        # #21: vilken regel som gav Microsoft. MX är direkt observation; övriga är konfiguration.
        "dns_ms_regel": dict(Counter("MX" if signaler(o)["S1"] == "MS" else "SPF+DKIM" if stoder(signaler(o)["S7"], "MS") else "SPF+autodiscover"
                                     for o in ra_k if klass_k[o["domän"]] == "MS")),
        "skatteverket_exo": exo_m.get("skatteverket.se"),
        "ga_kommuner": (len(ga_k), len(matbara_k)),
        "ga_kommuner_namn": [o["namn"] for o in ga_k],
        "ga_kommuner_insamling": [o["namn"] for o in ga_k if har_ga_insamling(o)],
        "ga_kommuner_bara_gtm": [o["namn"] for o in ga_k if not har_ga_insamling(o)],
        "ga_myndigheter": (len(ga_m), len(matbara_m)),
        "ga_myndigheter_insamling": sum(har_ga_insamling(o) for o in ga_m),
        "cmp_org": len(cmp_org),
        "cmp_enda": len(cmp_enda),
        "cmp_myndigheter": cmp_myndigheter,
        "cmp_nat": Counter((v, n) for (v, n, *d) in cmp_nat if d).most_common(),
        "topp_us_kommuner": lev_k.most_common(3),
        "ingen_tredjepart": [o["namn"] for o in ingen],
        "ingen_tredjepart_us_hotell": ingen_us_hotell,
        "google_tar_emot_ms_signerar": g_ms,
        "google_tar_emot_lan": Counter(lan[o["domän"]] for o in ra_k if o["namn"] in g_ms),
        "dmarc_none": sak_k[("DMARC", "p=none")], "dmarc_reject": sak_k[("DMARC", "p=reject")],
        "mta_sts": sak_k[("MTA-STS", "finns")], "dnssec": sak_k[("DNSSEC", "finns")],
        "sakerhet_lika_9999": sak.get("lika_9999"),
        "tenant": sum(o["entra_status"] == 200 for o in ra_k),
        **cert_siffror(f["cert"], f["t6"]),
    }


if __name__ == "__main__":
    for k, v in siffror().items():
        print(f"{k}: {v}")
