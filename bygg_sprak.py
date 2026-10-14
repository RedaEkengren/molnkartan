"""Bygger sidorna på svenska (docs/) och engelska (docs/en/) från mallarna i sidor/.

Mallarna har {{t:nyckel}} där texten ska stå. Texterna finns i i18n/sv.json och
i18n/en.json; nycklar som börjar med "js." går till sidornas JavaScript som T.
Efter bygget förrenderas tabellerna (forrendera.py).

  python3 bygg_sprak.py
"""

import html
import json
import re
import sys
from pathlib import Path

ROT = Path(__file__).parent
MALLAR = ROT / "sidor"
BAS = "https://molnkartan.se/"
SPRAK = {
    "sv": {"ut": ROT / "docs", "rot": "", "bas": BAS, "locale": "sv_SE"},
    "en": {"ut": ROT / "docs" / "en", "rot": "../", "bas": BAS + "en/", "locale": "en_GB"},
}
ANDRA = {"sv": "en", "en": "sv"}
SPRAKNAMN = {"sv": "Svenska", "en": "English"}


def texter(sprak):
    return json.loads((ROT / "i18n" / f"{sprak}.json").read_text(encoding="utf-8"))


def kontrollera(alla):
    sv, en = set(alla["sv"]), set(alla["en"])
    if sv != en:
        sys.exit(f"nycklar saknas i en.json: {sorted(sv - en)[:10]}, i sv.json: {sorted(en - sv)[:10]}")


def sidurl(sprak, fil):
    return SPRAK[sprak]["bas"] + ("" if fil == "index.html" else fil)


def bygg(fil, sprak, t):
    s = SPRAK[sprak]
    mall = (MALLAR / fil).read_text(encoding="utf-8")
    # Texter i attribut måste citattecken-skyddas; övriga texter är HTML.
    mall = re.sub(r'="\{\{t:([\w.]+)\}\}"', lambda m: '="' + html.escape(t[m.group(1)], quote=True) + '"', mall)
    mall = re.sub(r"\{\{t:([\w.]+)\}\}", lambda m: t[m.group(1)], mall)
    annat = ANDRA[sprak]
    relativ_annan = ("en/" if sprak == "sv" else "../") + ("" if fil == "index.html" else fil)
    huvud = "".join(f'\n<link rel="alternate" hreflang="{k}" href="{sidurl(k, fil)}">' for k in SPRAK)
    huvud += f'\n<link rel="alternate" hreflang="x-default" href="{sidurl("sv", fil)}">'
    js = {k[3:]: v for k, v in t.items() if k.startswith("js.")}
    huvud += (f"\n<script>const SPRAK = {json.dumps(sprak)}, T = {json.dumps(js, ensure_ascii=False)};\n"
              "const t = (k, v = {}) => T[k].replace(/\\{(\\w+)\\}/g, (_, n) => v[n]);</script>")
    ut = (mall.replace("{{sprak}}", sprak).replace("{{rot}}", s["rot"]).replace("{{bas}}", s["bas"])
          .replace("{{bas_rot}}", BAS).replace('content="sv_SE"', f'content="{s["locale"]}"'))
    ut = ut.replace("</title>", "</title>" + huvud, 1)
    val = f'<a class="sprakval" href="{relativ_annan}" hreflang="{annat}" lang="{annat}" title="{SPRAKNAMN[annat]}">{annat.upper()}</a>'
    ut, n = re.subn(r'<button [^>]*class="temaknapp"', lambda m: val + m.group(0), ut, count=1)
    if n != 1:
        sys.exit(f"{sprak}/{fil}: hittade inte temaknappen för språkvalet")
    if "{{" in ut:
        sys.exit(f"{sprak}/{fil}: ersattes inte: {re.findall(r'{{[^}]*}}', ut)[:5]}")
    s["ut"].mkdir(exist_ok=True)
    (s["ut"] / fil).write_text(ut, encoding="utf-8")


if __name__ == "__main__":
    alla = {k: texter(k) for k in SPRAK}
    kontrollera(alla)
    for fil in sorted(p.name for p in MALLAR.glob("*.html")):
        for sprak in SPRAK:
            bygg(fil, sprak, alla[sprak])
    print("Sidorna byggda på", ", ".join(SPRAK))
    import forrendera
    forrendera.main()
