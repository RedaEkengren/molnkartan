# Molnkartan

**Hur beroende är svenska kommuner och regioner av amerikanska molntjänster?
Mätt utifrån, med öppen data, för alla 290 kommuner och 20 regioner.**

| | Antal av 310 |
|---|---|
| E-post syns gå via Microsofts moln | 248 (80 %) |
| E-post hos Google | 10 (3 %) |
| Har en Microsoft Entra-tenant | 309 (>99 %) |
| Exchange Online hanterar domänen (oberoende kontroll) | 305 (98 %) |
| Webbplatsen kontaktar amerikanska nät innan besökaren samtyckt | 164 av 306 mätbara (54 %) |
| … varav Google Analytics/Tag Manager | 16 |

Samma mätningar för 252 statliga myndigheter (SCB:s myndighetsregister):
[`RESULTAT-myndigheter.md`](RESULTAT-myndigheter.md). Fynden, med hur varje
kontrollerades: [Fynd](https://redaekengren.github.io/molnkartan/fynd.html).

Mätt 2026-10-08. Sök och filtrera på **[redaekengren.github.io/molnkartan](https://redaekengren.github.io/molnkartan/)**,
eller läs hela tabellen i [`RESULTAT-sverige.md`](RESULTAT-sverige.md).

---

## Varför det här finns

I oktober 2026 avslöjade Ekot att Skatteverket införde amerikanska molntjänster
i stor skala trots att myndighetens egna dataskyddsombud avrådde. Det
väcker en fråga som ingen verkar ha svarat på: hur ser det ut i resten av
offentliga Sverige?

En del av svaret går att mäta utan att fråga någon. Organisationers e-post,
inloggning och webb lämnar spår i DNS som vem som helst kan slå upp. Det här
repot gör de uppslagen för alla kommuner och regioner, med regler som skrevs
ner innan datan hämtades.

## Vad det här inte visar

Läs det här innan du citerar en siffra.

- **Anslutning, inte innehåll.** En MX-post hos Microsoft visar att e-posten
  går genom Microsofts tjänst. Den säger ingenting om vilka uppgifter som
  ligger där, om de är sekretessbelagda, eller om organisationen gjort en
  konsekvensbedömning.
- **En tenant är ett konto.** Att en organisation har en Microsoft Entra-tenant
  betyder att kontot finns, inte hur mycket det används. Många har en enbart
  för Teams eller för enskilda tjänster.
- **"Inga molnsignaler" är inte "inget moln".** Det betyder att e-posten inte
  avslöjar någon leverantör utifrån. Flera av dem har andra signaler mot
  Microsoft, se kolumnen S8.
- **En domän per organisation.** Kommuner med flera domäner kan ha andra
  tjänster på de domäner som inte mättes. Gällivare är ett känt exempel, se
  `RESULTAT-sverige.md`.
- **Ett tillfälle.** DNS ändras. Mätningen gäller den tidsstämpel som står i
  rådatafilen.

## Hur det gick till

Metoden prövades i tre steg, och varje steg finns kvar i repot.

1. **Pilot, Stockholms län.** Regler skrivna före mätningen. Piloten
   **misslyckades** enligt sitt eget kriterium: 9 av 27 gick inte att avgöra,
   eftersom spamfilter framför e-posten döljer vad som finns bakom.
   [`RESULTAT-pilot.md`](RESULTAT-pilot.md)
2. **Version 2, prövad på ett annat län.** Nya signaler (DKIM, Teams,
   Entra-registrering) lades till med Stockholmsdatan framför sig. Därför fick
   Stockholm inte avgöra. Skåne, som inte hade mätts, användes som test: 94 %
   entydiga svar mot kravet 85 %. [`RESULTAT-v2.md`](RESULTAT-v2.md)
3. **Hela landet** med oförändrade regler. [`RESULTAT-sverige.md`](RESULTAT-sverige.md)

Allt prövades sedan med oberoende metoder, med krav skrivna i förväg:
[`RESULTAT-triangulering.md`](RESULTAT-triangulering.md).

Mätning 2, webbplatserna före samtycke, gick samma väg: negativ och positiv
kontroll före varje körning, upprepningstest, och två hållout-test (Skåne,
Västra Götaland) som **föll** för att en handskriven leverantörslista inte
hann ikapp. Version 3 klassar efter nätet bakom varje värd i stället och höll
på ett tredje hållout (Norrland). [`RESULTAT-webb.md`](RESULTAT-webb.md)

Reglerna, signalerna och alla ändringar med datum och skäl står i
[`METOD.md`](METOD.md). Ändringar läggs till längst ner; inget skrivs om i
efterhand.

## Kör själv

Python 3.10+ och [dnspython](https://www.dnspython.org/). Mätning 2 kräver även Google Chrome.

```bash
pip install dnspython
python3 matning.py organisationer-sverige.csv     # skriver data/ra-....json
python3 klassa_v2.py data/ra-organisationer-sverige-<tid>.json
python3 webbmatning.py organisationer-sverige.csv    # skriver data/webb-....json
python3 webb_klassa.py data/webb-organisationer-sverige-<tid>.json
```

En körning för hela landet tar ett par minuter. Den gör bara publika
DNS-uppslag och ett anrop per domän till Microsofts publika OpenID-ändpunkt.
Ingen portskanning, inga inloggningsförsök.

Varje påstående om en enskild organisation går att kontrollera med ett
kommando:

```bash
dig +short MX linkoping.se
dig +short CNAME selector1._domainkey.botkyrka.se
```

## Filer

| Fil | Vad |
|---|---|
| `METOD.md` | Frågan, signalerna, reglerna och alla ändringar |
| `organisationer-sverige.csv` | 290 kommuner (SCB-kod, domän från Wikidata) och 20 regioner |
| `organisationer-myndigheter.csv` | 252 myndigheter ur SCB:s myndighetsregister, med värdmyndighet för delade domäner |
| `organisationer-myndigheter-matning.csv` | 202 unika e-postdomäner, det som mäts |
| `organisationer.csv`, `organisationer-skane.csv`, `-vgr`, `-norrland` | Listorna för pilot och hållout |
| `matning.py` | Gör uppslagen och sparar rådata |
| `klassa.py`, `klassa_v2.py` | Tillämpar reglerna i pilot respektive v2 |
| `webbmatning.py`, `webb_klassa.py`, `leverantorer.csv` | Mätning 2: headless Chrome, nätverkslogg, ASN per värd |
| `data/` | Rådata med tidsstämpel, en fil per körning (`ra-` DNS, `webb-` webbplatser) |
| `triangulering.py` | T1–T4: oberoende kontroller av huvudpåståendena |
| `bygg_sida.py`, `docs/` | Webbsidan: `python3 bygg_sida.py <rådatafil>` skriver `docs/data.json` |

Rådatan sparar inte tenant-ID eller verifieringskoder. De är tekniskt publika
men behövs inte för någon slutsats.

## Fel i datan

Har en kommun fel domän, eller tolkas en signal fel? Öppna ett issue med
organisationen och ett `dig`-kommando som visar vad som borde stå. Rättelser
läggs till i `METOD.md` med datum, och mätningen körs om.

## Licens

Koden: MIT, se [`LICENSE`](LICENSE). Data och resultat:
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.sv). Ange
"Molnkartan" och mätdatum.
