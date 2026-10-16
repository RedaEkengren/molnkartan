"""Facit för valideringen (#20): vilket system svaren från organisationerna skickades från.

Reglerna står i METOD.md, "Validering mot facit". Facit sätts bara från de tekniska
huvudena i svarsmejlen. Steget läser aldrig nyckel.csv; jämförelsen är ett eget steg.

  python3 facit.py            # sätt facit, skriv validering/svar/facit.csv
  python3 facit.py jamfor     # jämför facit med nyckel.csv (först efter 2026-10-23)
"""

import csv
import email
import email.policy
import re
import sys
from collections import Counter, defaultdict
from email.utils import parseaddr
from pathlib import Path

ROT = Path(__file__).parent
SVAR = ROT / "validering" / "svar"
URVAL = ROT / "validering" / "urval.csv"
NYCKEL = ROT / "validering" / "nyckel.csv"
UT = SVAR / "facit.csv"

VARD = re.compile(r"\b([a-z0-9-]+(?:\.[a-z0-9-]+)+)\b")


def under(vard, doman):
    return vard == doman or vard.endswith("." + doman)


def receivedvardar(meddelande):
    vardar = set()
    for rad in meddelande.get_all("Received") or []:
        vardar |= set(VARD.findall(str(rad).lower()))
    return vardar


def klassa_meddelande(meddelande):
    """Microsoft, Google, tvetydig eller annat, enligt huvudreglerna i METOD.md."""
    namn = [k.lower() for k in meddelande.keys()]
    vardar = receivedvardar(meddelande)
    ms = any(n.startswith("x-ms-exchange-") for n in namn) or any(under(v, "outlook.com") for v in vardar)
    g = any(n.startswith("x-google-") for n in namn) or any(under(v, "google.com") for v in vardar)
    if ms and g:
        return "tvetydig"
    return "Microsoft" if ms else "Google" if g else "annat"


def organisation(avsandardoman, urval):
    """Urvalsdomänen svaret hör till, och om kopplingen bara gick via namnet."""
    for r in urval:
        if under(avsandardoman, r["domän"]):
            return r["domän"], False
    etiketter = set(avsandardoman.split("."))
    for r in urval:
        if r["domän"].split(".")[0] in etiketter:
            return r["domän"], True
    return None, False


def sla_ihop(klasser):
    """Flera svar från samma organisation: ett entydigt svar räcker, motsägelser blir tvetydigt."""
    entydiga = {k for k in klasser if k in ("Microsoft", "Google")}
    if "tvetydig" in klasser or len(entydiga) > 1:
        return "tvetydig"
    return entydiga.pop() if entydiga else "annat"


def facit(svarsmapp=SVAR, urvalsfil=URVAL):
    urval = list(csv.DictReader(open(urvalsfil, encoding="utf-8")))
    per_org, namnkoppling, okopplade = defaultdict(list), set(), []
    for fil in sorted(svarsmapp.glob("*.eml")):
        m = email.message_from_bytes(fil.read_bytes(), policy=email.policy.default)
        avsandare = parseaddr(str(m["From"]))[1].lower().split("@")[-1]
        doman, via_namn = organisation(avsandare, urval)
        if not doman:
            okopplade.append(fil.name)
            continue
        if via_namn:
            namnkoppling.add(f"{avsandare} → {doman}")
        per_org[doman].append(klassa_meddelande(m))
    rader = [{"namn": r["namn"], "domän": r["domän"],
              "facit": sla_ihop(per_org[r["domän"]]) if per_org[r["domän"]] else "saknas",
              "antal_svar": len(per_org[r["domän"]])} for r in urval]
    return rader, sorted(namnkoppling), okopplade


# Gruppnamnen i nyckel.csv. Kraven: METOD.md, "Validering mot facit".
KRAV = {"ms_mx": ("Microsoft", 0.90), "ms_konfig": ("Microsoft", 0.80), "g": ("Google", 0.80)}


def jamfor(rader, nyckelfil=NYCKEL):
    grupp = {r["domän"]: r["grupp"] for r in csv.DictReader(open(nyckelfil, encoding="utf-8"))}
    per_grupp = defaultdict(Counter)
    for r in rader:
        per_grupp[grupp[r["domän"]]][r["facit"]] += 1
    for g, c in sorted(per_grupp.items()):
        med_facit = sum(n for k, n in c.items() if k != "saknas")
        krav = KRAV.get(g)
        if not krav:
            utfall = "redovisas, inget krav"
        elif med_facit < 5:
            utfall = "ej prövad (färre än 5 facit)"
        else:
            andel = c[krav[0]] / med_facit
            utfall = f"{andel:.0%} {krav[0]}, krav {krav[1]:.0%}: {'godkänd' if andel >= krav[1] else 'underkänd'}"
        print(f"{g:40} {dict(c)}  →  {utfall}")


if __name__ == "__main__":
    rader, namnkoppling, okopplade = facit()
    if sys.argv[1:] == ["jamfor"]:
        jamfor(rader)
        sys.exit()
    with open(UT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["namn", "domän", "facit", "antal_svar"])
        w.writeheader()
        w.writerows(rader)
    print("Facit:", dict(Counter(r["facit"] for r in rader)))
    print("Kopplade via namn, kontrollera:", namnkoppling or "inga")
    print("Svar som inte kunde kopplas:", okopplade or "inga")
    print(f"Skrivet till {UT.relative_to(ROT)}")
