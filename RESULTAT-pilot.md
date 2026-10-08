# Resultat — pilot Stockholms län

Mätt 2026-10-08 15:27 UTC. Rådata: `data/ra-2026-10-08T152724Z.json`.
Tabellen återskapas med `python3 klassa.py`.

## Utfall mot METOD.md

**Piloten misslyckades enligt kriteriet.** 18 av 27 klassades entydigt för
e-post (kravet var 22), och 9 hamnade i "okänd" (gränsen var 5).

| | Antal |
|---|---|
| E-post i Microsofts moln (S1, eller S2+S4) | 17 |
| E-post hos Google (S1) | 1 (Salem) |
| Okänd, säkerhetsgateway eller egen server framför | 9 |
| **Har en Microsoft Entra-tenant (S5)** | **27 av 27** |

S5 kontrollerades mot domäner utan Microsoft-konto (`benbo.se`, `invelle.se`,
en påhittad domän): de svarar 400, så signalen skiljer faktiskt ja från nej.

Webb: 17 hos SiteVision (SE), 5 bakom Cloudflare (US-bolag, ursprung okänt),
5 hos andra svenska leverantörer eller i egen drift.

## Varför "okänd" blev stor

Nio organisationer har en säkerhetsgateway (mailanyone/mx25, staysecuregroup)
eller egen server först i MX-kedjan. Sex av dem har ändå
`spf.protection.outlook.com` i SPF, men saknar autodiscover-CNAME, så regeln
S2 **och** S4 uppfylldes inte. Regeln ändras inte i efterhand för den här mätningen.

## Iakttagelser för nästa version (inte resultat)

- Sigtuna har egna `mailin`-servrar och autodiscover mot `ex.sigtuna.se`, vilket
  ser ut som Exchange i egen drift. Metoden saknar en kategori för det.
- Vallentuna har egen MX först och Microsoft som reserv (prioritet 40).
- Stockholm stad har `elastx.email` (svensk) i SPF bredvid Microsoft.
- Tre kommuner använder `powerspf.com`, som döljer SPF-innehållet.

Möjliga nya signaler: `enterpriseregistration`/`lyncdiscover`-CNAME (Entra-
anslutna enheter, Teams), DKIM-selektorerna `selector1`/`selector2`
(Microsoft 365 publicerar dem under kundens domän), samt offentliga källor:
upphandlingsbeslut och kommunernas egna konsekvensbedömningar.
