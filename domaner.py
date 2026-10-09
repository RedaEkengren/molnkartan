"""Registrerade domäner enligt Public Suffix List, och organisationsalias med belägg (#16).

Listan ligger i data/public_suffix_list.dat (publicsuffix.org, MPL 2.0); versionen
står i filens huvud. Alias läses från organisationsalias.csv och kräver ett belägg.
"""

import csv
from functools import lru_cache
from pathlib import Path

ROT = Path(__file__).parent


@lru_cache(maxsize=1)
def _regler():
    regler, undantag = set(), set()
    for rad in (ROT / "data" / "public_suffix_list.dat").read_text(encoding="utf-8").splitlines():
        rad = rad.strip().lower()
        if not rad or rad.startswith("//"):
            continue
        (undantag if rad.startswith("!") else regler).add(rad.lstrip("!"))
    return regler, undantag


def registrerad(vard):
    """Den registrerbara domänen: ett led under det publika suffixet.
    Okända toppdomäner behandlas som suffix av ett led, som listans standardregel."""
    led = (vard or "").lower().rstrip(".").split(".")
    if len(led) < 2:
        return ".".join(led)
    regler, undantag = _regler()
    suffix_led = 1
    for i in range(len(led)):
        kandidat = ".".join(led[i:])
        if kandidat in undantag:
            suffix_led = len(led) - i - 1
            break
        if kandidat in regler or "*." + ".".join(led[i + 1:]) in regler:
            suffix_led = len(led) - i
            break
    if suffix_led >= len(led):
        return ".".join(led)
    return ".".join(led[-(suffix_led + 1):])


@lru_cache(maxsize=1)
def _alias():
    alias = {}
    fil = ROT / "organisationsalias.csv"
    if fil.exists():
        for r in csv.DictReader(open(fil, encoding="utf-8")):
            if r["belagg"].strip():
                alias.setdefault(r["doman"], set()).add(registrerad(r["alias"]))
    return alias


def egna_domaner(doman, *varder):
    """Organisationens egna registrerade domäner: e-postdomänen, webbplatsens värdar och alias med belägg."""
    egna = {registrerad(doman), *(registrerad(v) for v in varder if v)}
    return egna | _alias().get(doman, set())
