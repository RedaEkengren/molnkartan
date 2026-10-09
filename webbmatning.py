"""Mätning 2 i METOD.md: vilka tredjeparter en startsida kontaktar före samtycke.

python3 webbmatning.py organisationer.csv   # skriver data/webb-<lista>-<tid>.json
Kräver google-chrome. Kör negativ och positiv kontroll först och avbryter om någon fallerar.
"""

import csv
import functools
import http.server
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from domaner import egna_domaner, registrerad
from matning import fraga, txt

ROT = Path(__file__).parent
VANTETID_MS = 10_000
PARALLELLA = 6

_version = re.search(r"(\d+)\.", subprocess.run(["google-chrome", "--version"], capture_output=True, text=True).stdout).group(1)
ANVANDARAGENT = f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{_version}.0.0.0 Safari/537.36"

CHROME_FLAGGOR = [
    "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run", "--no-default-browser-check",
    "--disable-background-networking", "--disable-component-update", "--disable-sync", "--disable-default-apps",
    "--disable-domain-reliability", "--disable-client-side-phishing-detection", "--safebrowsing-disable-auto-update",
    "--metrics-recording-only", "--no-pings",
    "--disable-features=Translate,OptimizationHints,AutofillServerCommunication,MediaRouter",
    f"--user-agent={ANVANDARAGENT}", f"--virtual-time-budget={VANTETID_MS}", "--dump-dom",
]


US_NATAGARE = ("AKAMAI", "AMAZON", "MICROSOFT", "GOOGLE", "CLOUDFLARE", "FASTLY", "DIGITALOCEAN", "ORACLE",
               "LINODE", "EDGECAST", "EDGIO", "STACKPATH", "INCAPSULA", "IMPERVA")
EU_EES = {"AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU",
          "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE", "NO", "IS", "LI",
          "EU"}  # Team Cymru anger ibland EU i stället för land, se rättelse v3


def natverk(vard):
    """Version 3: värdens första IPv4 -> ASN, registreringsland och AS-namn (Team Cymru)."""
    ip = (fraga(vard, "A") or [None])[0]
    if not ip:
        return {"ip": None}
    rad = txt(".".join(reversed(ip.split("."))) + ".origin.asn.cymru.com")
    if not rad:
        return {"ip": ip}
    asn = rad[0].split("|")[0].strip().split()[0]
    info = txt(f"AS{asn}.asn.cymru.com")
    falt = [f.strip() for f in info[0].split("|")] if info else []
    land, namn = (falt[1], falt[-1]) if len(falt) >= 5 else (None, None)
    us = land == "US" or any(n in (namn or "").upper() for n in US_NATAGARE)
    typ = "US" if us else "EU/EES" if land in EU_EES else "annat" if land else None
    return {"ip": ip, "asn": asn, "land": land, "namn": namn, "nat": typ}


class MatFel(Exception):
    """Sidan gick inte att mäta: Chrome kraschade, loggen saknas eller huvudsidan laddades inte (#10)."""


class Kallor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.varder = set()

    def handle_starttag(self, tagg, attr):
        if tagg in ("script", "iframe"):
            src = dict(attr).get("src") or ""
            if src.startswith(("http://", "https://", "//")):
                self.varder.add(urlparse(src if not src.startswith("//") else "https:" + src).hostname)


def las_natlogg(fil, vardar):
    """Läser Chromes nätverkslogg. Ger (anropsförsök, anrop med svar, huvudsidans HTTP-status).

    Ett anropsförsök är en URL_REQUEST_START_JOB som sidan själv startade (initiator är
    ett webbursprung); Chromes egen trafik har "not an origin" och räknas inte. Ett anrop
    fick svar om svarshuvuden lästes (#12). Huvudsidan är Chromes egen navigering till
    någon av vardar; utan ett 2xx-svar där räknas sidan som omätbar (#10)."""
    try:
        text = fil.read_text(errors="replace").rstrip()
        if not text.endswith("}"):  # Chrome kan avsluta loggen mitt i en lista
            text = text.rstrip(",") + "]}"
        logg = json.loads(text)
        typer = {v: k for k, v in logg["constants"]["logEventTypes"].items()}
    except (OSError, ValueError, KeyError) as fel:
        raise MatFel(f"nätverksloggen gick inte att läsa: {type(fel).__name__}") from fel
    kallor = {}
    for e in logg["events"]:
        k = kallor.setdefault(e["source"]["id"], {"url": None, "initiator": None, "status": []})
        typ, p = typer.get(e["type"], ""), e.get("params", {})
        if typ == "URL_REQUEST_START_JOB" and p.get("url", "").startswith("http"):
            k["url"] = k["url"] or p["url"]
            k["initiator"] = k["initiator"] or str(p.get("initiator", ""))
        if typ.endswith("READ_RESPONSE_HEADERS") and p.get("headers"):
            k["status"].append(p["headers"][0].split(" ")[1] if " " in p["headers"][0] else "")
    forsok, svar, huvud = set(), set(), None
    for k in kallor.values():
        if not k["url"]:
            continue
        vard = urlparse(k["url"]).hostname
        if k["initiator"].startswith(("http://", "https://")):
            forsok.add(vard)
            if k["status"]:
                svar.add(vard)
        elif vard in vardar and any(st.startswith("2") for st in k["status"]):
            huvud = next(st for st in k["status"] if st.startswith("2"))
    return forsok, svar, huvud


def ladda(url):
    """Öppnar url i en ny Chrome-profil. Ger (renderad DOM, anropsförsök, anrop med svar, huvudsidans status).
    Kraschar Chrome, saknas loggen eller laddas inte huvudsidan blir det MatFel, aldrig ett tomt resultat (#10)."""
    tmp = Path(tempfile.mkdtemp(prefix="molnkartan-"))
    try:
        logg = tmp / "net.json"
        korning = subprocess.run(["google-chrome", *CHROME_FLAGGOR, f"--user-data-dir={tmp / 'profil'}",
                                  f"--log-net-log={logg}", url], capture_output=True, text=True, timeout=60)
        if korning.returncode != 0:
            raise MatFel(f"Chrome avslutades med kod {korning.returncode}")
        if not logg.exists():
            raise MatFel("Chrome skrev ingen nätverkslogg")
        if not korning.stdout.strip() or "chrome-error://" in korning.stdout:
            raise MatFel("huvudsidan visades inte (tom sida eller Chromes felsida)")
        forsok, svar, huvud = las_natlogg(logg, {urlparse(url).hostname})
        if huvud is None:
            raise MatFel("huvudsidan gav inget 2xx-svar i webbläsaren")
        return korning.stdout, forsok, svar, huvud
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def slutadress(url):
    # Kakor sparas mellan omdirigeringar, som i en webbläsare. Utan dem fastnar anropet
    # i SiteVisions kakomdirigering för datacenteradresser (METOD.md, "Plats").
    oppna = urllib.request.build_opener(urllib.request.HTTPCookieProcessor()).open
    req = urllib.request.Request(url, headers={"User-Agent": ANVANDARAGENT})
    with oppna(req, timeout=20) as svar:
        return svar.status, svar.url


def mat(rad):
    doman = rad["domän"]
    # Myndigheter: registrets webbadress när den finns, annars www.<domän> (METOD.md, mätning 3).
    forsta = f"https://{rad['webb']}/" if rad.get("webb") else f"https://www.{doman}/"
    try:
        status, slut = slutadress(forsta)
    except Exception:
        try:  # rättelse v3: vissa saknar www
            status, slut = slutadress(f"https://{doman}/")
        except Exception as fel:
            return {**rad, "status": f"fel: {type(fel).__name__}: {fel}"[:200]}
    egna = egna_domaner(doman, urlparse(slut).hostname, urlparse(forsta).hostname)
    try:
        dom, forsok, svar, huvud = ladda(slut)
    except subprocess.TimeoutExpired:
        return {**rad, "status": "fel: sidan laddade inte klart inom 60 s", "slutadress": slut}
    except MatFel as fel:
        return {**rad, "status": f"fel: {fel}", "slutadress": slut}
    parser = Kallor()
    parser.feed(dom)
    tredje = lambda varder: sorted(v for v in varder if v and registrerad(v) not in egna)
    w2 = tredje(forsok)
    # status är huvudsidans svar i webbläsaren, inte urllib-anropet (#10).
    # w2 = anropsförsök, w2_svar = de av dem som fick svarshuvuden (#12).
    return {**rad, "status": int(huvud), "slutadress": slut, "w1": tredje(parser.varder), "w2": w2,
            "w2_svar": tredje(svar), "natverk": {v: natverk(v) for v in w2}}


def kontroller():
    """Negativ och positiv kontroll enligt METOD.md. Avbryter körningen om någon fallerar."""
    katalog = Path(tempfile.mkdtemp(prefix="molnkartan-kontroll-"))
    (katalog / "tom.html").write_text("<!doctype html><title>tom</title><p>tom</p>")
    (katalog / "ga.html").write_text('<!doctype html><title>ga</title>'
                                     '<script async src="https://www.googletagmanager.com/gtag/js?id=G-MOLNKARTAN"></script>')
    class Tyst(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    hanterare = functools.partial(Tyst, directory=str(katalog))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), hanterare)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    bas = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        _, tom, _, _ = ladda(f"{bas}/tom.html")
        _, ga, ga_svar, _ = ladda(f"{bas}/ga.html")
    finally:
        server.shutdown()
        shutil.rmtree(katalog, ignore_errors=True)
    tom = {v for v in tom if v != "127.0.0.1"}
    resultat = {"negativ": sorted(tom), "positiv": sorted(ga - {"127.0.0.1"})}
    if tom:
        sys.exit(f"Negativ kontroll fallerade, tom sida gav {sorted(tom)}")
    if "www.googletagmanager.com" not in ga or "www.googletagmanager.com" not in ga_svar:
        sys.exit(f"Positiv kontroll fallerade, GA-sidan gav {sorted(ga)} med svar från {sorted(ga_svar)}")
    natkontroll = {v: natverk(v)["nat"] for v in ("www.googletagmanager.com", "www.hetzner.com")}
    resultat["nat"] = natkontroll
    if natkontroll != {"www.googletagmanager.com": "US", "www.hetzner.com": "EU/EES"}:
        sys.exit(f"Nätkontroll fallerade: {natkontroll}")
    return resultat


def main():
    lista = sys.argv[1]
    tid = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    kontroll = kontroller()
    print(f"kontroller ok: {kontroll}", file=sys.stderr)
    with open(ROT / lista, encoding="utf-8") as f:
        rader = list(csv.DictReader(f))
    with ThreadPoolExecutor(PARALLELLA) as pool:
        resultat = list(pool.map(mat, rader))
    ut = ROT / "data" / f"webb-{Path(lista).stem}-{tid}.json"
    ut.write_text(json.dumps({"matt": tid, "chrome": _version, "kontroller": kontroll, "organisationer": resultat},
                             ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(ut)


if __name__ == "__main__":
    main()
