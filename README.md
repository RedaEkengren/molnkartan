# Molnkartan

**Hur beroende är svenska kommuner och regioner av amerikanska molntjänster?
Mätt utifrån, med öppen data, för alla 290 kommuner och 20 regioner.**

| | Antal av 310 |
|---|---|
| E-post syns gå via Microsofts moln | 245 (79 %) |
| E-post hos Google | 10 (3 %) |
| Har en Microsoft Entra-tenant | 309 (>99 %) |

Mätt 2026-10-08. Hela tabellen, per län och per organisation, finns i
[`RESULTAT-sverige.md`](RESULTAT-sverige.md).

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

Reglerna, signalerna och alla ändringar med datum och skäl står i
[`METOD.md`](METOD.md). Ändringar läggs till längst ner; inget skrivs om i
efterhand.

## Kör själv

Python 3.10+ och [dnspython](https://www.dnspython.org/).

```bash
pip install dnspython
python3 matning.py organisationer-sverige.csv     # skriver data/ra-....json
python3 klassa_v2.py data/ra-organisationer-sverige-<tid>.json
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
| `organisationer.csv`, `organisationer-skane.csv` | Listorna för pilot och test |
| `matning.py` | Gör uppslagen och sparar rådata |
| `klassa.py`, `klassa_v2.py` | Tillämpar reglerna i pilot respektive v2 |
| `data/` | Rådata med tidsstämpel, en fil per körning |

Rådatan sparar inte tenant-ID eller verifieringskoder. De är tekniskt publika
men behövs inte för någon slutsats.

## Fel i datan

Har en kommun fel domän, eller tolkas en signal fel? Öppna ett issue med
organisationen och ett `dig`-kommando som visar vad som borde stå. Rättelser
läggs till i `METOD.md` med datum, och mätningen körs om.

## Licens

Koden: Apache-2.0, se [`LICENSE`](LICENSE). Data och resultat:
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.sv). Ange
"Molnkartan" och mätdatum.
