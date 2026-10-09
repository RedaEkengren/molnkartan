Granskning av Molnkartan, 2026-10-09
=================================

Bedömning: huvudsiffrorna går att återskapa från de sparade observationerna.
Insamlingen och publiceringsspärrarna har däremot fel som kan ge både falska
positiva och falska negativa resultat. De starkare slutsatserna om faktiskt
användande, frånvaro och validering är inte tillräckligt belagda.

Granskningen omfattar projektets lokala Pythonkod, tester, arbetsflöde,
webbsidans logik, metod, rapporter och sparade data. Ingen Git/VCS-historik,
webbläsare, extern tjänst eller annan projektmapp har öppnats. Nätanrop och
Chrome simulerades i motproven. Implementationen har inte ändrats.
Extern källkontroll och verifiering av den påstådda förhandsregistreringen
ingår därför inte. P1 betyder bör åtgärdas före fortsatt tillit till berörd
slutsats eller automatisk publicering; P2 betyder konkret fel med snävare
eller villkorad påverkan.

**Kodfynd, i prioritetsordning**

1. **P1 — DNS-fel blir negativa observationer.**
   `matning.py:18–30` och `triangulering.py:63–73` returnerar samma tomma lista
   för timeout/SERVFAIL som för saknade poster. `klassa_v2.py:35–36` ger då
   `inga molnsignaler`, som dessutom räknas som ett entydigt svar.
   Motprov: låt samtliga DNS-frågor kasta `dns.resolver.LifetimeTimeout`;
   både huvudmätningen och T3 ger `inga molnsignaler`.
   `bygg_sida.py:79` väljer senaste DNS-fil utan kvalitetskontroll.
   I certifikatmätningen kan samma fel göra att namn räknas bort som inaktiva
   (`certmatning.py:99–101`). Skilj lyckat negativt svar från mätfel och
   bevara denna skillnad genom klassning, nämnare och publicering.
   Ett mätfel får inte förbättra andelen entydiga svar.

2. **P1 — En Chrome-krasch kan bli ”ingen tredjepart”.**
   `webbmatning.py:105–107` ignorerar processens returkod och ersätter en
   saknad nätverkslogg med en tom mängd. HTTP-status hämtas från ett separat
   urllib-anrop och återanvänds i resultatet (`webbmatning.py:126–143`).
   Motprov: urllib ger 200, Chrome avslutas med kod 1, tom standardutmatning
   och ingen logg. Resultatet blir status 200 och `ingen tredjepart`.
   Kontroller före körningen upptäcker inte en senare krasch för en enskild
   organisation. Kräv en verifierad sidladdning i själva webbläsaren, giltig
   logg och hanterat processresultat; annars `kunde inte mätas`.

3. **P1 — Triangulering kan godkännas vid nästan totalt bortfall.**
   `triangulering.py:148–154` tar bort obesvarade T1- och T4-kontroller innan
   andelarna räknas. Motprov med i övrigt godkända T2/T3: bara 1 av 512
   T1-frågor och 1 av 338 T4-frågor får svar. `godkand()` returnerar ändå
   `True`. Vid totalt bortfall riskeras division med noll.
   Kräv täckning över hela avsedda urvalet separat från överensstämmelse
   bland svaren. Rapportera båda andelarna och gör tomma underlag underkända.

4. **P1 — Påbörjade nätverksförsök redovisas som kontakt.**
   `webbmatning.py:90–97` använder bara `URL_REQUEST_START_JOB`. Varken
   anslutningsutfall, mottagen respons eller fel följs upp.
   Motprov: en sådan starthändelse följd av ett DNS-fel lämnar ändå
   `www.google-analytics.com` i listan över kontaktade värdar.
   Påståenden om att något laddats eller att IP-adress skickats till just
   mottagaren stöds inte av starthändelsen ensam. Följ nätverksförloppet eller
   benämn observationen som ett anropsförsök. Sparade W2-listor räcker inte
   för att i efterhand avgöra vilka befintliga observationer som påverkats.

5. **P2 — Webbens publiceringsspärr kontrollerar inte ASN-täckningen.**
   `bygg_sida.py:59–65` kontrollerar endast andelen mätbara sidor.
   Kravet på minst 95 procent värdar med ASN och land finns i
   `METOD.md:267–270, 311–315` och beräknas av `webb_klassa.py`, men används
   inte vid byggandet. Motprov: en fil med 100 procent mätbara sidor men
   0 procent identifierade nät godkänns. Även explicita underkända
   kontrollfält ignoreras av byggaren, även om den vanliga insamlaren ska
   avbryta innan sådana filer skrivs. Samla kvalitetskraven i en gemensam
   validerare för rapportering och publicering, inklusive populationens
   fullständighet.

6. **P2 — Certspotter kan lämna en ofullständig lista med status ”ok”.**
   `certmatning.py:75–77` returnerar redan hämtade namn om en senare sida
   misslyckas. `summera()` behandlar alla mängder som lyckade resultat.
   Motprov: första sidan ger 100 namn och nästa sida ger `None`; resultatet
   innehåller 100 namn och får status `ok`. Saknade namn kan ändra såväl
   US-andel som nollkategori utan att täckningskravet reagerar.
   Bevara en särskild status för ofullständig paginering och underkänn eller
   återuppta körningen. Detta är ett reproducerat kodfel; det är inte visat
   att den publicerade certifikatfilen faktiskt drabbats.

7. **P2 — Kartan visar ”Nej” när webbplatsen inte kunde mätas.**
   `docs/index.html:208–210` kontrollerar bara om `fore_samtycke` finns.
   Byggaren skapar objektet också för mätfel, med falska GA-flaggor.
   Den faktiska JavaScript-funktionen kördes lokalt mot `docs/data.json`:
   Högsby, Gällivare och Kiruna har `kunde inte mätas` men får kartetiketten
   `Nej` i vyn Google före samtycke. Visa `Ingen uppgift` vid mätfel före
   kontrollen av GA-flaggorna. Region Skåne har samma datatillstånd men
   regioner har ingen egen yta på kartan.

8. **P2 — Likadant domännamn används som bevis för samma part.**
   `webbmatning.py:67–68, 132–142` reducerar värdar till två etiketter och
   undantar dessutom andra toppdomäner med samma första etikett.
   Motprov: sidan `example.se` kontaktar `track.example.com`; anropet
   försvinner ur W2 och sidan klassas `ingen tredjepart` utan någon uppgift
   om gemensamt ägande. Tvåetikettsregeln kan också slå ihop separata
   webbplatser på delade suffix. Regeln finns i metoden men kan inte belägga
   vem som äger domänerna. Använd korrekt suffixhantering och en explicit,
   källbelagd lista över organisationens ytterligare domäner.

9. **P2 — Blandade leverantörssignaler och domängränser tappas.**
   `klassa_v2.py:18–22` väljer Microsoft framför Google i varje signal.
   Motprov: gateway-MX, SPF för både Microsoft och Google, Google-DKIM och
   ingen Microsoft-autodiscover blir `okänd`, trots att Googleregeln i
   `METOD.md:79` är uppfylld. Behåll en mängd leverantörer per signal och
   låt klassningsreglerna hantera kombinationerna.
   Dessutom ger `lev_mx(['10 notgoogle.com.'])` klassen `G` på grund av
   suffixmatchningen i `klassa.py:10–13`. Kräv exakt domän eller punkt före
   suffixet. Ingen av dessa avvikelser hittades i den oberoende omräkningen
   av de två ursprungliga nationella DNS-underlagen; detta är motprov som
   visar fel vid andra giltiga indata.

10. **P2 — Äldre triangulering kan presenteras som kontroll av nyare data.**
    `bygg_sida.py:79–83` väljer DNS-fil och godkänd trianguleringsfil
    oberoende av varandra, utan att jämföra trianguleringens `kallor`.
    Dagens publicerade DNS-data kommer från 18:46/19:05, medan den godkända
    trianguleringen avser DNS-filerna från 15:41/16:42. Huvudklasserna är
    desamma i de jämförda underlagen, så någon aktuell sifferförändring är
    inte visad. Vid framtida förändring kan däremot gamla EXO-svar blandas
    med nya e-postklasser och i animationen kallas ”Bekräftat av Exchange
    Online” (`docs/demo.js:154`). Sidan visar inte trianguleringens separata
    mätdatum (`docs/index.html:251`). Bind verifiering till dess underlag
    eller visa tydligt att det är en äldre, separat observation.

**Oberoende metod- och projektbedömning**

**M1 — Certifikatfyndets frånvaropåstående motsägs av den egna kontrollens
kategori.** Rubriken i `docs/fynd.html:38` säger att hälften av kommunerna
inte har tjänster på amerikanska nät. Huvudmätningen hittar noll sådana namn
för Grums, men T6 hittar en andel 0,143 bland sju aktiva namn och godkänner
ändå jämförelsen (`data/triangulering-t6-2026-10-09T081527Z.json:165–172`).
Det är en positiv observation där huvudmätningen var negativ.

Skillnaden kan bero på källa eller mättid; det går inte att fastställa
vilket från de sparade aggregaten. Oavsett orsak visar den att ett godkänt
T6 inte styrker nollkategorin. Formulera fyndet som att huvudkällan inte
hittade US-klassade namn för 150 av 289 kommuner. Ett särskilt test måste
pröva övergången noll/till minst ett, om det är den som ska bli rubrik.

T6 testar dessutom skillnaden i andelar, inte namnlistans fullständighet
som det påstås i `RESULTAT-tjanster.md:19`. Exempelvis skulle listor med
1 respektive 100 namn godkännas om båda ger 0 procent US. Även perfekta
listor från båda källorna missar tjänster utanför den valda domänen och
namn som inte syns individuellt i certifikatunderlaget. Ett A-svar visar
heller inte ensamt att en tjänst faktiskt körs på adressen.

**M2 — Svarstäckning används som belägg för träffsäkerhet.** Skånetestet
godkänner minst 85 procent entydiga etiketter (`METOD.md:88–93`). Därmed
visas att reglerna ofta ger ett svar, inte hur ofta svaret beskriver
verkligheten korrekt. En metod som alltid svarar Microsoft får full
svarstäckning. Även det misslyckade DNS-motprovet får en entydig etikett.
Påståendet ”Metoden håller” i `RESULTAT-v2.md:22` går därför längre än
testet. En oberoende referens måste ge separat precision och känslighet
för varje påstående, inklusive negativa fall och organisationer bakom
gateways. Referensen får inte vara samma klassificerare på en annan resolver.

**M3 — De 248 Microsoft-klassningarna innehåller olika slags bevis.** Av de
248 kommunerna och regionerna har 189 Microsoft-MX. Resterande 59 kommer
från fallback: 52 via SPF + DKIM och 7 via SPF + autodiscover. Koden
observerar konfiguration; den observerar inte inkommande eller utgående
meddelanden. Tidigare konfiguration eller skilda system för in- och
utgående post kan därför ge samma signaler.

T2 löser inte detta: 7 av 10 Google-klassade kommuner ger också positivt
EXO-svar. Projektet har redan dokumenterat att svaret bara avser
registrering, men använder ändå T2 som validering av e-postklassen och
animationen säger ”Bekräftat”. Redovisa direkt MX och indirekta
konfigurationssignaler separat. Rubriken ”Google tar emot, Microsoft
signerar” (`docs/fynd.html:147`) behöver också begränsas till att
Microsoft-DKIM är publicerad, om faktiskt signerade meddelanden inte har
kontrollerats. Granskningen visar bristande bevis, inte att alla 59
indirekta klassningar är felaktiga.

**M4 — Trianguleringens oberoende måste knytas till rätt felkälla.** T1
jämför samma leverantörs register via två ändpunkter. T3 jämför samma
DNS-poster och samma klassificerare via andra resolvrar. T4 prövar ASN för
en given IP, inte om det var IP-adressen som webbläsaren faktiskt använde,
och inte slutsatsen om nätägarens land. T6 jämför två läsare av samma
certifikatunderlag och återanvänder nätklassningen. Dessa kontroller
undersöker åtkomst och reproducerbarhet men kan dela systematiska fel.
T5 ger starkare stöd för webbinsamlingen, men omfattar bara 15
organisationer och har en avvikelse. Dess 14/15 kan inte användas som
belägg för precisionen hos varje kategori eller organisation.

**M5 — Projektets breda fråga behöver ett tydligare mätobjekt.**
”Beroende” mäts här genom olika observationer: domänkonfiguration,
registrering, externa värdnamn och certifikatnamn per nät. Projektet mäter
inte betydelse för verksamheten, trafikmängd, kostnader eller möjligheten
att byta leverantör. Separata organisationsdomäner och dolda tjänster
saknas. Påståendet i `docs/fynd.html:73` att alla siffror är lägsta nivåer
är inte visat: det skulle kräva att positiva fel uteslutits. En andel med
ofullständig täljare och nämnare kan förskjutas i båda riktningar.

Även formuleringen att alla övriga tjänstenät är svenska/europeiska är
för stark (`docs/fynd.html:41`, `RESULTAT-tjanster.md:37–38`): rådatan
innehåller 14 namn i kategorin `annat` och 16 i `okänt`. Beskriv nät efter
den faktiska klassningen. Riktningen på urvalsbias från exempelvis
jokercertifikat är inte kvantifierad i projektet.

**Falsifiering som bör styra nästa version**

| Hypotes | Motprov som kan fälla den | Förutbestämt utfall |
|---|---|---|
| Mätfel blir aldrig frånvaropåståenden | Timeout, SERVFAIL, Chrome-krasch, tom logg och ofullständig API-paginering | Samtliga blir okända/underkända, aldrig negativa fynd |
| Klassificeraren följer reglerna | Blandade SPF/DKIM-signaler, blandade MX och vilseledande domänsuffix | Jämför med separat specificerade förväntade etiketter |
| Webbplatsen kontaktade mottagaren | Startat anrop som misslyckas före kontakt; omdirigering; olikhet mellan DNS-uppslag och faktisk motpart | Försök och bekräftad kontakt särredovisas |
| Noll US-namn är en stabil kategori | Kontrollera nollgruppen separat med ytterligare oberoende underlag | Varje 0→positiv avvikelse redovisas; ±15 procentenheter räcker inte |
| E-postklassningen beskriver verklig användning | Blindat, stratifierat urval med annan referens än samma DNS/EXO-signaler | Förhandsbestäm krav på precision och känslighet per kategori |
| Godkända körningar har tillräckligt stöd | Ta bort de flesta kontrollsvar eller ASN, lämna kvar några korrekta | Publicering ska stoppas och bortfallet visas |

Frys underlag, programversion, regelversion och acceptanskriterier före
nästa utvärdering. De redan undersökta fallen, inklusive Grums, hör till
utvecklingsunderlaget. Ett nytt godkänt test bör ske på ett orört urval.

**Genomförd verifiering och begränsningar**

14 befintliga tester passerade: 2 sidtester, 11 fyndtester och
certifikatdatans hygienkontroll. Hygientestet som kör `git ls-files` kördes
inte, för att respektera instruktionen att inte använda VCS.

```sh
python3 -B -m unittest -v tests/test_sida.py tests/test_fynd.py
python3 -B -m unittest -v tests.test_hygien.IngaVardnamnICertdata
```

Lokala motprov reproducerade kodfynd 1–9 med simulerade indata; kartans
funktion prövades även med Node direkt från den befintliga HTML-filen och
de publicerade JSON-datafilerna. Det bevisar kodens beteende, inte hur ofta
de simulerade felen inträffade under originalkörningen.

En separat regelimplementation och separata summeringar gav:

| Underlag | Återskapat utfall |
|---|---|
| Kommuner/regioner, DNS 15:41 | MS 248, Google 10, inga molnsignaler 20, okänd 32 |
| Myndigheter, DNS 16:42 | MS 85, Google 1, inga molnsignaler 103, okänd 13 |
| Kommuner/regioner, webb 16:26 | Mätbara 306, US-klassade 164, GA-värdar 11 |
| Myndigheter, webb 16:44 | Mätbara 193, US-klassade 115, GA-värdar 11 |
| Kommuner, certifikat | 289 med aktiva namn, 5 342 namn, 837 US, 150 med noll observerade US-namn, median 0 procent |

Projektets spårbara filer, uttryckliga begränsningar och redovisning av
misslyckade försök ger goda förutsättningar för rättelser. Tester av
siffersamband är användbara, men behöver kompletteras med tester av
mätfel och en referens som verkligen kan motsäga tolkningen.
