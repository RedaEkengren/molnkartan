"""Skriver in tabeller och siffror i docs/index.html och docs/myndigheter.html.

Sidorna ritas annars med JavaScript från data.json. Sökmotorer och AI-tjänster som
inte kör JavaScript ser då tomma tabeller. Skriptet laddar varje sida i headless
Chrome, tar innehållet i alla element märkta data-forrenderad och skriver in det
mellan markörerna <!--fr:id--> och <!--/fr:id-->. I webbläsaren tömmer sidans
JavaScript elementen och ritar om dem från samma data.

Körs efter bygg_sida.py:  python3 forrendera.py
"""

import functools
import html
import http.server
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

ROT = Path(__file__).parent
DOCS = ROT / "docs"
SIDOR = ["index.html", "myndigheter.html", "en/index.html", "en/myndigheter.html"]
CHROME = shutil.which("google-chrome") or shutil.which("google-chrome-stable") or "google-chrome"

UTDRAG = """<script>addEventListener("load", () => setTimeout(() => {
  const u = {};
  for (const e of document.querySelectorAll("[data-forrenderad]"))
    u[e.id] = e.tagName === "SELECT" ? [...e.options].slice(1).map(o => o.outerHTML).join("") : e.innerHTML;
  const p = document.createElement("pre"); p.id = "__forrenderat"; p.textContent = JSON.stringify(u); document.body.append(p);
}, 4000));</script>"""


def rendera(mapp, sida):
    """Innehållet i varje data-forrenderad-element efter att sidans JavaScript körts."""
    kopia = (mapp / sida).with_name("__" + Path(sida).name)
    kopia.write_text((DOCS / sida).read_text(encoding="utf-8").replace("</body>", UTDRAG + "</body>"), encoding="utf-8")
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(mapp)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with tempfile.TemporaryDirectory() as profil:
            dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox", f"--user-data-dir={profil}",
                                  "--virtual-time-budget=15000", "--dump-dom", f"http://127.0.0.1:{server.server_port}/{kopia.relative_to(mapp)}"],
                                 capture_output=True, text=True, timeout=120).stdout
    finally:
        server.shutdown()
        kopia.unlink()
    m = re.search(r'<pre id="__forrenderat">(.*?)</pre>', dom, re.S)
    if not m:
        sys.exit(f"{sida}: sidan ritades inte färdigt i Chrome")
    return json.loads(html.unescape(m.group(1)))


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def skriv_in(text, innehall):
    for ident, inre in innehall.items():
        text, n = re.subn(rf"(<!--fr:{ident}-->).*?(<!--/fr:{ident}-->)", lambda m: m.group(1) + inre + m.group(2), text, flags=re.S)
        if n != 1:
            sys.exit(f"markören fr:{ident} saknas")
    return text


def main():
    with tempfile.TemporaryDirectory() as tmp:
        mapp = Path(tmp) / "docs"
        shutil.copytree(DOCS, mapp)
        for sida in SIDOR:
            innehall = rendera(mapp, sida)
            tomma = [i for i, v in innehall.items() if not v.strip()]
            if tomma:
                sys.exit(f"{sida}: tomt efter rendering: {tomma}")
            fil = DOCS / sida
            fil.write_text(skriv_in(fil.read_text(encoding="utf-8"), innehall), encoding="utf-8")
            print(f"{sida}: {len(innehall)} delar förrenderade")


if __name__ == "__main__":
    main()
