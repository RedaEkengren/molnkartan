# Resultat — triangulering

> **Granskning 2026-10-09 (issue #22):** kontrollerna kallades först oberoende.
> Flera delar källa eller regler med huvudmätningen. Vad var och en kan och
> inte kan upptäcka:
>
> | # | Kan upptäcka | Delar med huvudmätningen |
> |---|---|---|
> | T1 | fel i tolkningen av OpenID-svaret | samma leverantör (Microsoft) |
> | T2 | att domänen inte är registrerad i Exchange Online | visar registrering, inte mottagning |
> | T3 | resolverberoende fel | samma DNS-poster och samma klassningsregler |
> | T4 | fel i ASN-registret | samma IP-adress; prövar inte vilken adress webbläsaren använde |
> | T5 | fel i den automatiska webbläsarkörningen | samma nätklassning; 15 organisationer, inte varje kategori |
>
> Ingen av dem prövar om klasserna är rätt mot ett facit (issue #20).

Regler: METOD.md, "Triangulering" och "Rättelse T2". Varje påstående prövat
med en oberoende metod.

| # | Påstående | Oberoende metod | Krav | Utfall |
|---|---|---|---|---|
| T1 | Microsoft-tenant | `getuserrealm.srf` | ≥99 % lika | **512/512** |
| T2 | E-post i Microsofts moln | Exchange Onlines autodiscover | ≥95 % ja | **331/333** (första körningen 86,5 %, föll; se rättelsen) |
| T3 | E-postklassen | Tre publika DNS-resolvrar | ≥99 % lika | **512/512** för alla tre |
| T4 | Nätet bakom värdar | RIPEstat i stället för Team Cymru | ≥97 % samma ASN | **338/338** |
| T5 | Amerikanskt nät före samtycke | Vanlig Chrome, 15 slumpvis valda | ≥13/15 lika | **14/15** |

Rådata: `data/triangulering-2026-10-08T165750Z.json`, `data/triangulering-t5-2026-10-08.json`.

## Vad T2 visade utöver testet

Exchange Online svarar för domänen hos **305 av 310 kommuner och regioner**
och **142 av 202 myndighetsdomäner**, också där MX pekar på egna servrar
eller spamfilter:

- alla 32 kommuner som klassats "gick inte att avgöra"
- 19 av 20 kommuner med "inga molnsignaler"
- 7 av 10 kommuner med e-post hos Google
- 47 av 103 myndighetsdomäner med "inga molnsignaler", bland dem Skatteverket

Det betyder att domänen är registrerad i en Exchange Online-organisation. Det
visar inte att e-post tas emot eller lagras där; att 7 av 10 Google-kommuner
också ger ja visar gränsen. T1 jämför två ändpunkter hos samma leverantör och
är därför en svag kontroll.

En senare körning från GitHub Actions (`triangulering-2026-10-08T191727Z`)
föll på T3 (93–96 % mot kravet 99 %, DNS-fel på GitHubs maskiner) och
publiceras inte. Klasserna i övriga resultat ändras inte i
efterhand; detta är en oberoende signal som visar att DNS-mätningen är en
nivå som syns utifrån.

Avvikelser i T2 bland de Microsoft-klassade: Gällivare (domänen `gellivare.se`,
se issue #6) och Migrationsverket.

## T5: avvikelsen

Hörby: en vanlig Chrome laddade `cdn.matomo.cloud` från ett amerikanskt nät,
vilket mätningen inte såg. Avvikelser åt det hållet stärker att "amerikanskt
nät före samtycke" är en nivå som syns utifrån.

## Utdata

```
Källa: data/triangulering-2026-10-08T165750Z.json

T1 tenant: OpenID och getuserrealm lika för 512/512 = 100.0% (krav ≥99 %); olika: []
T2 Exchange Online bland klassade Microsoft: 331/333 = 99.4% (krav ≥95 %); nej/okänt: [('Gällivare', False), ('Migrationsverket', False)]
   info: kommuner, klass G: Exchange Online ja för 7/10
   info: myndigheter, klass G: Exchange Online ja för 1/1
   info: kommuner, klass inga molnsignaler: Exchange Online ja för 19/20
   info: myndigheter, klass inga molnsignaler: Exchange Online ja för 47/103
   info: kommuner, klass okänd: Exchange Online ja för 32/32
   info: myndigheter, klass okänd: Exchange Online ja för 10/13
T3 cloudflare: samma e-postklass för 512/512 = 100.0% (krav ≥99 %); olika: []
T3 quad9: samma e-postklass för 512/512 = 100.0% (krav ≥99 %); olika: []
T3 google: samma e-postklass för 512/512 = 100.0% (krav ≥99 %); olika: []
T4 ASN: Team Cymru och RIPEstat lika för 338/338 = 100.0% (krav ≥97 %); olika: []
```
