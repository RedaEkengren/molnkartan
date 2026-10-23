# Resultat — validering mot facit (#20)

Körd 2026-10-23 enligt METOD.md, "Validering mot facit". Frågan skickades
2026-10-09 till 43 kommuner och regioner; svar till och med 2026-10-23 räknas.

- Sammanställning (bara antal): `data/validering-2026-10-23.json`
- Skript: `facit.py` (facit), `facit.py jamfor` (jämförelse)
- De enskilda svaren publiceras inte; de kan innehålla namn på handläggare.

## Utfall

33 av 43 svarade (10 bortfall). Facit ur svarens tekniska huvuden.

| Klass i DNS-mätningen | Facit | Krav | Resultat |
|---|---|---|---|
| Microsoft via MX | 5 av 5 Microsoft | ≥90 % | **godkänd** (100 %) |
| Microsoft via SPF/DKIM/autodiscover | 5 av 7 Microsoft, 2 annat | ≥80 % | **underkänd** (71 %) |
| Google | 5 av 7 Google, 2 Microsoft | ≥80 % | **underkänd** (71 %) |
| Microsoft och Google | 1 Microsoft, 2 annat | inget | redovisas |
| Inga molnsignaler | 3 Microsoft, 3 annat | inget | redovisas |
| Oavgjord | 3 Microsoft, 2 annat | inget | redovisas |

## Vad det betyder

- **MX-regeln håller.** Där MX pekar på Microsoft svarade alla från Microsoft.
- **Konfiguration är inte placering.** SPF, DKIM eller autodiscover för Microsoft
  räcker inte för att säga att brevlådan ligger där: en av organisationerna skrev
  att de har egen drift.
- **Google-klassen** bygger på MX. Två av sju svarade från Microsoft, vilket
  stämmer med fyndet om kommuner som tar emot hos Google men har DKIM hos Microsoft.
- **"Inga molnsignaler" är inte "inget moln".** Hälften av dem med facit svarade
  från Microsoft.

## Textanteckningar (används inte som facit)

Där huvudena gav *annat* (ofta ärendesystem eller automatiska svar) skrev 4 att de
har egen drift och 1 att de använder Microsoft 365; övriga gav inget besked. Enligt
reglerna används texten bara där huvudena är tvetydiga, så de ändrar inte facit.

## Ändrat på sidan

- "har e-post som syns gå via Microsofts moln" → "har Microsoft i e-postens DNS".
- "har e-post hos Google" → "tar emot e-post hos Google (MX)".
- Varningen om anslutning säger nu "pekar på Microsoft i DNS".

## Förbehåll

- 7 svar per klass: ett enda svar flyttar resultatet med mer än 10 procentenheter.
- Svaret visar var den svarande brevlådan sitter, inte vilken server som tar emot först.
