# Metod — pilot: Stockholms län

Skriven 2026-10-08, **innan** någon data samlades in. Ändras inte i efterhand;
ändringar läggs till längst ner med datum och skäl.

## Fråga

Hur många av Stockholms läns 26 kommuner och Region Stockholm visar, i öppna
DNS- och HTTP-signaler, att de använder amerikanska molntjänster för e-post,
kontorsprogram och webb?

## Vad som INTE kan mätas

Utifrån syns vilka tjänster en organisation *är ansluten till*, inte vilka
uppgifter som ligger där. En Microsoft 365-tenant betyder inte att känsliga
personuppgifter behandlas i molnet. Rapporten får aldrig påstå det.

## Signaler och regler

Varje signal är binär och kan kontrolleras av vem som helst med `dig` eller
`curl`. Leverantörer: **MS** (Microsoft), **G** (Google), **AWS**, **SE/EU**,
**okänd**.

| # | Signal | Klassas som MS om | Klassas som G om |
|---|---|---|---|
| S1 | MX för domänen | slutar på `mail.protection.outlook.com` | slutar på `google.com` / `googlemail.com` |
| S2 | SPF (TXT `v=spf1`) | innehåller `spf.protection.outlook.com` | innehåller `_spf.google.com` |
| S3 | Verifierings-TXT | börjar med `MS=` | börjar med `google-site-verification=` |
| S4 | CNAME `autodiscover.<domän>` | pekar på `autodiscover.outlook.com` | — |
| S5 | Entra ID-tenant | `login.microsoftonline.com/<domän>/v2.0/.well-known/openid-configuration` svarar 200 | — |
| S6 | Webbhotell för `www.<domän>` | ASN tillhör Microsoft | ASN tillhör Google |

S6 klassas också som **AWS**, **Cloudflare** (CDN framför, ursprung okänt) eller
**SE/EU** efter ASN-ägare.

## Slutsatser per organisation

- **E-post i MS-molnet:** S1 = MS. Om S1 visar en säkerhetsgateway (t.ex.
  Proofpoint, Mimecast, Halon) räcker S2 = MS **och** S4 = MS.
- **MS-tenant finns:** S5 = MS. Svagare påstående: kontot finns, inte hur det används.
- **Inga signaler:** alla S1–S5 negativa. Rapporteras som "inget syns utifrån",
  inte som "använder inte amerikanska moln".

## Vad som avgör om det finns potential

Piloten ska visa om metoden ger **tydliga** svar, inte vilket svar det blir.

- **Lyckad:** minst 22 av 27 organisationer går att klassa entydigt för e-post.
- **Misslyckad:** fler än 5 hamnar i "okänd" eftersom gateways döljer
  bakomliggande tjänst. Då behövs andra signaler innan länet skalas till landet.

## Hygien

- Bara publika DNS-frågor och ett anrop per domän till Microsofts publika
  OpenID-ändpunkt. Ingen skanning av portar, inga inloggningsförsök.
- Rådata sparas med tidsstämpel i `data/`, så varje siffra kan spåras.

---

## Version 2 — tillägg 2026-10-08, efter piloten, före all Skåne-data

**Skäl:** piloten gav 9 "okänd" av 27 (`RESULTAT-pilot.md`). V2-reglerna är
skrivna med Stockholmsdatan framför oss och kan därför vara anpassade till den.
Stockholm räknas som **utvecklingsdata**. Det som avgör är **Skåne län**
(33 kommuner + Region Skåne), som inte mätts när detta skrivs.

### Nya signaler

| # | Signal | MS om | G om |
|---|---|---|---|
| S7 | DKIM `selector1._domainkey.<domän>` CNAME | pekar på `*.onmicrosoft.com` | — |
| S7 | DKIM `google._domainkey.<domän>` TXT | — | finns och börjar med `v=DKIM1` |
| S8 | CNAME `enterpriseregistration.<domän>` | `enterpriseregistration.windows.net` | — |
| S8 | CNAME `lyncdiscover.<domän>` | `webdir.online.lync.com` | — |

### E-postregel v2 (ersätter v1 för v2-körningar)

1. **MS:** alla MX = MS (S1), **eller** S2 = MS och minst en av S4, S7 = MS.
2. **G:** alla MX = G, **eller** S2 = G och S7 = G.
3. **Inga molnsignaler:** S2, S4 och S7 visar varken MS eller G. Räknas som
   entydigt svar om vad som *syns utifrån*, och rapporteras aldrig som
   "använder inte amerikanska moln".
4. **Okänd:** allt annat (t.ex. S2 = MS men varken S4 eller S7).

S8 används bara som tilläggsuppgift ("enheter/Teams kopplade till Microsoft"),
inte i e-postregeln.

### Kriterium v2

Pilotens gränser (22/27 ≈ 81 %, 5/27 ≈ 19 %) skärpta och avrundade, tillämpade
på **Skåne**: minst 85 % entydiga
(MS, G eller inga molnsignaler) och högst 15 % okända. Utfallet för Stockholm
redovisas men räknas inte.

---

## Nationell körning — tillägg 2026-10-08, före mätningen

- **Lista:** `organisationer-sverige.csv`, 290 kommuner och 20 regioner.
  Gotland räknas en gång, som kommun 0980 med regionansvar.
  - Kommunkoder och namn från SCB:s API (BE0101A, variabeln Region): 290 st.
  - Domän från Wikidata (P856 officiell webbplats), matchad på kommunkod (P525).
    Underdomäner kortas till huvuddomänen.
  - Ängelholm: Wikidata anger `angelholm.se`, som har null-MX (`0 .`).
    E-postdomänen `engelholm.se` används i stället.
  - Regionernas domäner är handskrivna. Alla 310 domäner har en riktig MX-post.
- **E-postregel:** v2, oförändrad.
- **Webb:** Akamai och Fastly klassas nu som egna kategorier (amerikanska CDN,
  ursprung okänt), som Cloudflare. Det är en rättelse, inte en ny regel:
  Region Skåne hamnade i "okänd" i v2.
- **Inget godkänt/underkänt-kriterium.** Metoden validerades på Skåne. Den här
  körningen är beskrivande, och andelen "okänd" redovisas per län.

---

## Rättelse — 2026-10-08, efter den nationella körningen

**Vad:** S7 (DKIM) räknar nu även CNAME som slutar på `.dkim.mail.microsoft`
som Microsoft, utöver `*.onmicrosoft.com`.

**Skäl:** Microsoft har infört ett nytt format för DKIM-poster
(`selector1-<domän>._domainkey.<tenant>.<x>-v1.dkim.mail.microsoft`). Regeln
skrevs bara för det äldre formatet. Felet upptäcktes när webbsidans animation
visade Åtvidabergs DKIM-svar, som tydligt pekar på Microsoft, med signalen
"inget".

**Effekt:** 14 organisationer har det nya formatet. Tre byter klass, från
okänd till Microsoft: Gotland, Sjöbo och Bromölla. Fem som klassas som Google
(MX hos Google) signerar sin e-post via Microsoft, vilket redovisas som
iakttagelse men inte ändrar klassen, eftersom S1 avgör först.

Siffrorna före rättelsen står kvar i `RESULTAT-sverige.md`. Rådatan är
oförändrad; bara klassningen körs om.

---

# Mätning 2: Tredjepartstjänster på webbplatsen (issue #1)

Skriven 2026-10-08, före all mätning av webbplatser.

## Fråga

Vilka externa tjänster kontaktar en besökares webbläsare när kommunens eller
regionens startsida laddas, **innan** besökaren svarat på någon cookiebanner?

## Hur

- Startsidan `https://www.<domän>/` öppnas en gång i headless Chrome. Inget
  klickas. Sidan får 10 sekunder.
- Chromes nätverkslogg (`--log-net-log`) sparas. Bara anrop vars `initiator`
  är ett webbursprung räknas: de startades av sidan. Chromes egen
  bakgrundstrafik har `initiator: "not an origin"` och räknas inte.
- Användaragenten är vanlig Chrome utan ordet "Headless", eftersom
  samtyckesverktyg kan bete sig annorlunda mot robotar och mätningen ska visa
  vad en vanlig besökare får.
- **Tredjepart** = värdnamn vars registrerade domän skiljer sig från
  organisationens domän och från värdnamnet sidan hamnade på efter
  omdirigering.

## Signaler

| # | Signal |
|---|---|
| W1 | Tredjepartsvärdar i `src` för `script` och `iframe` i den renderade sidan |
| W2 | Tredjepartsvärdar som sidan kontaktade före samtycke |

Varje värd mappas via `leverantorer.csv` (domänsuffix → leverantör, land).
Värdar utan mappning redovisas som "okänd leverantör".

## Klassning per organisation

- **US före samtycke:** minst en W2-värd mappad till en leverantör med land US.
- **Google Analytics/Tag Manager före samtycke:** W2 innehåller
  `google-analytics.com`, `analytics.google.com` eller `googletagmanager.com`.
- **Bara EU/SE före samtycke:** alla mappade W2-värdar har land SE eller EU och
  inga okända.
- **Ingen tredjepart:** W2 är tom.
- **Kunde inte mätas:** sidan svarade inte, eller gav HTTP-fel.

## Falsifiering — måste hålla, annars publiceras inget

1. **Negativ kontroll:** en tom lokal sida mäts före varje körning. Den ska ge
   noll W2-värdar. Annars är filtret på `initiator` fel.
2. **Positiv kontroll:** en lokal sida som laddar `googletagmanager.com/gtag/js`
   mäts före varje körning. Den ska ge Google Analytics/Tag Manager. Annars ser
   mätningen inte det den letar efter.
3. **Upprepning:** Stockholms län mäts två gånger med minst 10 minuters
   mellanrum. "US före samtycke" ska ha samma värde för minst 25 av 27.
4. **Hållout:** `leverantorer.csv` byggs med Stockholm framför sig. Skåne mäts
   därefter utan att listan ändras: högst 10 % av Skånes unika
   tredjepartsvärdar får vara okända, och minst 32 av 34 ska gå att mäta.

## Vad det här inte visar

- En lyckad laddning i en headless webbläsare från en svensk IP-adress, vid ett
  tillfälle. Andra sidor än startsidan mäts inte.
- Att en tjänst kontaktas betyder inte att personuppgifter skickas, men IP-adress
  och webbläsarinformation följer med varje anrop.
- Om ett anrop är lagligt beror på rättslig grund och avtal, som inte syns utifrån.

### Precisering — 2026-10-08, efter Stockholm (utveckling), före Skåne

- **Land** i `leverantorer.csv` är där bolaget som driver tjänsten har sitt
  säte. För publika CDN:er som körs på en annan leverantörs nät (jsDelivr,
  unpkg, jQuery CDN) anges nätets ägare, eftersom det är dit anropet går.
- **EU** omfattar EES (Norge, Island, Liechtenstein).
- Ny klass **Annat land före samtycke:** inga US-värdar men minst en värd i ett
  land utanför EU/EES, t.ex. UK. Utan den klassen hamnade sådana organisationer
  ingenstans.
- Värden matchas mot listan på registrerad domän eller längre suffix.

Stickprov mot en vanlig Chrome (Claude in Chrome, nätverksloggen, ingen
cookiebanner besvarad): Huddinge laddade bara egna resurser (mätningen: inga
tredjeparter) och Danderyd laddade Google Fonts, Google Translate och gstatic
(mätningen: samma). Stickprov är inte en del av kriteriet.

## Mätning 2, version 2 — 2026-10-08, efter Skåne, före Västra Götaland

**Skäl:** hållout-testet på Skåne föll (51 % okända värdar mot kravet 10 %),
se `RESULTAT-webb.md`.

- `leverantorer.csv` utökas med leverantörerna från Skåne. Värdar som inte går
  att identifiera (t.ex. `analys.cloud`) lämnas omappade hellre än gissade.
- **Första part** omfattar nu även registrerade domäner med samma första del
  som organisationens domän (`helsingborg.io` för `helsingborg.se`).
- **Nytt hållout:** Västra Götalands län, 49 kommuner och Västra
  Götalandsregionen. Samma krav: högst 10 % okända unika tredjepartsvärdar och
  minst 95 % mätbara.
- Stockholm och Skåne är nu utvecklingsdata och räknas inte.

## Mätning 2, version 3 — 2026-10-08, efter två fallna hållout, före Norrland

**Skäl:** handskrivna leverantörslistor föll i Skåne (51 % okända) och Västra
Götaland (28 %). Klassningen byggs därför om kring **nätet** i stället för
bolaget, vilket går att slå upp för varje värd.

### Nätet bakom varje tredjepartsvärd

Under mätningen, direkt efter sidladdningen: värdens första IPv4-adress →
ASN och registreringsland via Team Cymru (`origin.asn.cymru.com`,
`asn.cymru.com`).

**US-nät** om registreringslandet är US, **eller** om AS-namnet innehåller
något av: AKAMAI, AMAZON, MICROSOFT, GOOGLE, CLOUDFLARE, FASTLY, DIGITALOCEAN,
ORACLE, LINODE, EDGECAST, EDGIO, STACKPATH, INCAPSULA, IMPERVA. Skäl: flera
amerikanska nätägare registrerar ASN genom europeiska dotterbolag (Akamai
International B.V. är registrerat i NL).

**EU/EES-nät:** registreringsland i EU/EES och inte US-nät enligt ovan.

### Klassning per organisation (v3)

- **US-nät före samtycke:** minst en tredjepartsvärd på US-nät.
- **Bara EU/EES-nät före samtycke:** alla tredjepartsvärdar på EU/EES-nät.
- **Annat nät före samtycke:** inga US-nät, minst ett utanför EU/EES.
- **Okänt nät:** inga US-nät, minst en värd utan ASN.
- **Ingen tredjepart** och **kunde inte mätas** som tidigare.

Leverantörsnamnet från `leverantorer.csv` visas som tillägg där det finns, men
påverkar inte klassen.

### Falsifiering v3

1. Negativ och positiv kontroll som tidigare.
2. **Nätkontroll** före varje körning: `www.googletagmanager.com` ska ge US-nät
   och `www.hetzner.com` ska ge EU/EES-nät. Annars avbryts körningen.
3. **Hållout: Norrland** (Västernorrlands, Jämtlands, Västerbottens och
   Norrbottens län, 48 organisationer), inte mätt tidigare. Krav: minst 95 %
   av unika tredjepartsvärdar får ett ASN med land, och minst 95 % av
   organisationerna går att mäta.
4. Upprepningstestet på Stockholm (startat 16:22 UTC) gäller som tidigare.

### Rättelse v3 — 2026-10-08, efter första nationella körningen

1. **Landskoden `EU`.** Team Cymru anger ibland `EU` i stället för ett land för
   RIPE-registrerade nät (t.ex. Tele2 Sverige). Regeln kände inte igen koden,
   så sådana värdar hamnade felaktigt i "annat nät". `EU` räknas nu som EU/EES.
2. **Startsida utan `www`.** Enköping kunde inte mätas eftersom
   `www.enkoping.se` saknas i DNS. Om `https://www.<domän>/` inte går att nå
   prövas `https://<domän>/`.

Båda hittades vid granskning av den första nationella körningen
(`data/webb-organisationer-sverige-2026-10-08T162242Z.json`), som behålls.
Hela landet mäts om med rättelserna.

---

# Mätning 3: Statliga myndigheter (issue #5)

Skriven 2026-10-08, före all mätning av myndigheter.

## Lista

SCB:s allmänna myndighetsregister (myndighetsregistret.scb.se, nedladdat
2026-10-08): statliga förvaltningsmyndigheter (244), myndigheter under
riksdagen (5) och statliga affärsverk (3), totalt 252.
`organisationer-myndigheter.csv` har alla 252 med organisationsnummer.

- **E-postdomän** = domänen i registrets e-postadress. **Webb** = registrets
  webbadress. De mäts var för sig (Försvarsmakten: `mil.se` och
  `forsvarsmakten.se`).
- **Delad domän:** flera myndigheter med samma e-postdomän mäts **en** gång.
  Myndigheten vars webbadress är domänens rot räknas som värd; övriga
  redovisas som "värdas av". Där ingen är värd (t.ex. de 21 länsstyrelserna
  på `lansstyrelsen.se`) redovisas domänen som delad.
- 11 nämnder saknar både e-post och webb i registret och kan inte mätas.
- Mätenheten är unik e-postdomän: `organisationer-myndigheter-matning.csv`.

## Regler och kriterier

Oförändrade: e-postregel v2 med DKIM-rättelsen, mätning 2 version 3 med
rättelser. Kraven är desamma som för kommunerna: minst 85 % entydiga för
e-post, minst 95 % av unika tredjepartsvärdar med ASN och minst 95 % mätbara
webbplatser. Myndigheter är en annan population än kommuner; uppfylls inte
kraven redovisas det och siffrorna per myndighet publiceras inte.

### Stickprov i vanlig webbläsare — 2026-10-08

Nätverkslistan i en vanlig Chrome visar inte filer som hämtas ur cachen. Vid
stickprov används därför också `performance.getEntriesByType("resource")`, som
listar alla resurser sidan laddat. Upptäckt vid kontrollen av Försvarsmakten,
där `gtm.js` saknades i nätverkslistan men fanns i resurslistan.

---

# Triangulering — 2026-10-08, före körning

Varje huvudpåstående prövas med en metod som inte beror på den första.
Kraven gäller överensstämmelse; där de inte uppfylls redovisas det.

| # | Påstående | Oberoende metod | Krav |
|---|---|---|---|
| T1 | Microsoft-tenant (OpenID, 200/400) | `getuserrealm.srf`: `NameSpaceType` är `Managed` eller `Federated` | samma svar för ≥99 % |
| T2 | E-post i Microsofts moln (MX/SPF/DKIM) | Exchange Onlines autodiscover (`autodiscover.json`) omdirigerar till `outlook.office365.com` | ≥95 % av dem som klassats Microsoft får ja |
| T3 | E-postklassen | MX, SPF och DKIM frågas via 1.1.1.1, 9.9.9.9 och 8.8.8.8 i stället för systemets resolver | samma klass för ≥99 % |
| T4 | Nätet bakom tredjepartsvärdar (Team Cymru) | RIPEstat `network-info` för samma IP-adresser som sparades | samma ASN för ≥97 % |
| T5 | "Amerikanskt nät före samtycke" (headless Chrome) | Vanlig Chrome med annan profil och nätverk, `performance`-resurslistan, 15 slumpvis valda organisationer (frö 20261008), utan samtyckeskaka | samma klass för ≥13 av 15 |

**T2 för övriga klasser** (Google, inga molnsignaler, okänd) är inte ett test
utan ny information: hur många som ändå har Exchange Online bakom egna servrar
(hybrid). Den används inte för att ändra klasserna i efterhand.

**Gräns:** för T1 och T2 sparas bara ja/nej. Omdirigeringsadresser, tenantnamn
och underdomäner som svaren avslöjar sparas inte och publiceras inte.
Ett anrop per domän och tjänst, inga inloggningsförsök.

### Rättelse T2 — 2026-10-08, efter första trianguleringskörningen

Första körningen (`data/triangulering-2026-10-08T165533Z.json`, behålls) gav
86,5 % och föll mot kravet 95 %. Av de 45 avvikelserna var 43 "inget svar",
inte "nej". Två orsaker hittades vid kontroll av enskilda domäner:

1. **Implementationsfel:** Exchange Online svarar ibland direkt med
   `200 {"Url":"https://outlook.office365.com/…"}` i stället för att
   omdirigera. Koden räknade bara omdirigeringar. Båda svaren betyder att
   Exchange Online hanterar domänen och räknas nu som ja.
2. **Strypning:** 16 parallella anrop gav tomma svar. T2 körs nu med 2 parallella
   anrop och ett nytt försök vid tomt svar.

Kravet (≥95 %) ändras inte.

---

# Mätning 4: Var tjänsterna körs (issue #3)

Skriven 2026-10-08, före all mätning.

## Fråga

Hur stor del av en organisations publika tjänster (e-tjänster, bokning,
intranät och liknande på underdomäner) körs på amerikanska nät?

## Hur

- **Namn:** certifikatloggar via crt.sh (`%.<domän>`, utgångna certifikat
  exkluderade). Unika namn under organisationens e-postdomän, utan jokertecken.
- **Aktiva:** namn som har en A-post vid mätningen. Övriga räknas inte.
- **Nät:** första IPv4 → ASN via Team Cymru, med samma regler som mätning 2
  version 3 (US-nät, EU/EES-nät, annat, okänt).
- **Plattform:** om namnet har en CNAME räknas målets suffix för ett fåtal
  kända plattformar (t.ex. `sharepoint.com`, `azurewebsites.net`,
  `cloudapp.azure.com`, `amazonaws.com`, `cloudfront.net`).

## Gräns

**Inga värdnamn sparas och inga publiceras**, inte heller i rådatan. Per
organisation sparas bara antal: aktiva namn, antal per nättyp och antal per
plattformssuffix. Värdnamnen finns bara i minnet under körningen.
`tests/test_hygien.py` utökas så att CI fallerar om en `cert-`-fil innehåller
något värdnamn under en organisations domän.

## Mått och kriterier

- Per organisation: andel aktiva namn på US-nät.
- Krav: minst 90 % av organisationerna får svar från crt.sh (upp till fyra
  försök), och minst 95 % av aktiva namn får ASN och land.

## Falsifiering (T6)

20 slumpvis valda organisationer (frö 20261008) mäts också med Certspotter
(SSLMate) i stället för crt.sh, med samma uppslag i övrigt. Krav: andelen på
US-nät skiljer högst 15 procentenheter för minst 16 av 20.

## Vad det här inte visar

Bara tjänster med eget certifikat under organisationens domän syns. Tjänster
på leverantörens domän (t.ex. `kommun.leverantor.se`) eller utan certifikat
syns inte. Andelen gäller namn, inte hur mycket varje tjänst används.

### Tillägg — 2026-10-08, före all mätning 4-data

crt.sh svarade 502 på 15 av 15 försök (fem domäner, tre försök var) vid
provkörningen. Källordningen blir därför: crt.sh, och vid fel Certspotter
(SSLMate, `include_subdomains`, alla sidor). Källan sparas per organisation.
Certspotter tillåter 100 anrop i timmen utan konto, så körningen hålls under
den takten. T6 jämför fortfarande de två källorna på 20 slumpvis valda och
visar därmed om de går att blanda.

---

# Mätning 5: Säkerhetsgrunder (issue #4)

Skriven 2026-10-08, före all mätning.

## Signaler per e-postdomän

| Signal | Uppslag | Värden |
|---|---|---|
| DMARC | TXT `_dmarc.<domän>` | `p=reject`, `p=quarantine`, `p=none`, saknas |
| SPF | TXT `v=spf1` | slutar `-all`, `~all`, annat, saknas |
| MTA-STS | TXT `_mta-sts.<domän>` med `v=STSv1` | finns, saknas |
| TLS-RPT | TXT `_smtp._tls.<domän>` med `v=TLSRPTv1` | finns, saknas |
| DNSSEC | DS-post för domänen | finns, saknas |
| HSTS | Huvudet `Strict-Transport-Security` med `max-age` > 0 på webbplatsen | finns, saknas, kunde inte mätas |

Uppslagen görs via 1.1.1.1. Systemets resolver på mätdatorn returnerade inga
DS-poster alls, inte ens för domäner som bevisligen är signerade.

## Kontroller före varje körning

`cloudflare.com` ska ha DS, `google.com` ska sakna DS, och `google.com` ska ha
`p=reject` och MTA-STS. Annars avbryts körningen.

## Gräns

Resultatet sparas och redovisas **bara i aggregat**: per län för kommuner och
regioner, och för myndigheterna som grupp. Ingen fil i repot innehåller värden
per organisation.

---

## Plats: mätning från GitHubs maskiner — 2026-10-08

Första provkörningen av månadsmätningen i GitHub Actions
(`data/*-2026-10-08T18*`, `*T19*`) gav:

- **DNS-mätningarna oberoende av plats:** e-postklassen lika för 310 av 310
  kommuner och regioner, Exchange Online samma 305.
- **Webbmätningen föll:** 193 av 310 kommuner och regioner och 50 av 202
  myndighetsdomäner gick inte att mäta. 176 av felen är kommuner hos
  SiteVision, som svarar adresser i datacenter med en omdirigering som sätter en
  kaka; skriptets första anrop sparade inga kakor och fastnade i en slinga.
  Där mätningen lyckades var "amerikanskt nät före samtycke" lika med den
  svenska körningen för 116 av 117 respektive 152 av 152.

**Regel från och med nu:** en webbmätning som inte uppfyller kravet (minst
95 % mätbara) publiceras inte. `bygg_sida.py` väljer senaste godkända körning;
den fallna finns kvar i `data/`.

### Utfall och rättelse mätning 4 — 2026-10-08

Första körningen (`data/cert-2026-10-08T180702Z.json`, publicerades aldrig;
borttagen 2026-10-09 eftersom den hade interna antal per organisation, se
"Publicering och granskning"): svar för 511 av 512 (krav ≥90 %, uppfyllt), men **94,1 % av aktiva namn
fick nät (krav ≥95 %, föll)**. Ett stickprov på de två organisationerna med
flest namn utan nät visade att samtliga 165 pekade på privata IP-adresser:
interna system med publika DNS-namn, som inte går att nå från internet och
därför inte har något nät.

**Rättelse:** namn vars A-post är en privat, reserverad eller CGNAT-adress räknas
som "interna" och ingår inte i aktiva tjänster. Antalet interna sparas bara som
en total för hela körningen, inte per organisation, eftersom det är
säkerhetsrelevant. Kravet (≥95 %) ändras inte. Hela mätningen körs om.

`tests/test_hygien.py` gav falsklarm på organisationernas egna e-postdomäner
under andra organisationers domäner (`ifau.uu.se`, `nai.uu.se`) och undantar nu
fältet `domän`.

### T6 — första försöket föll, 2026-10-09

`data/triangulering-t6-2026-10-08T233344Z.json` (behålls): 6 av 20 inom 15
procentenheter, krav 16. 14 av 20 var "inget svar" från Certspotter, vars
timkvot (100 anrop) hade förbrukats av huvudkörningen strax innan. Där båda
källorna svarade var 6 av 6 inom kravet.

**Rättelse:** vid svar 429 väntar skriptet den tid Certspotter anger
(`Retry-After`, högst en timme) i stället för att ge upp. Alla 20 i samma urval
mäts om; kravet ändras inte. Mätning 4 publiceras inte förrän T6 håller.

---

# Publicering och granskning — 2026-10-09

## Spärrar

En körning publiceras bara om den klarar sina krav. `bygg_sida.py` väljer för
varje sort den senaste godkända körningen:

- **Webb:** minst 95 % mätbara.
- **Triangulering:** T1 ≥99 %, T2 ≥95 %, T3 ≥99 % för alla tre resolvrar,
  T4 ≥97 %.
- **Säkerhet:** högst 2 % DNS-fel. DNS-fel (timeout, SERVFAIL) räknas som fel,
  inte som saknade poster.

Fynden (`docs/fynd.html`) gäller en bestämd mätning. `fynd_siffror.py` låser
de filerna och räknar fram varje siffra; `tests/test_fynd.py` fallerar om sidan
och datan inte stämmer.

## Oberoende granskning

Före spridning lät vi en separat granskare, utan del i bygget och med bara
läsrätt, försöka motbevisa varje fynd mot rådatan. Den hittade och vi rättade:

1. Rubriken "Sexton kommuner kontaktar Google Analytics" var fel för fem som
   bara laddar Tag Manager (bekräftat i vanlig Chrome för Jönköping och Sunne).
   Nu: 16 laddar Analytics eller Tag Manager, varav 11 anropar Analytics.
   Samma uppdelning för myndigheterna: 30, varav 11.
2. Exchange Online-fyndet påstod att e-posten finns hos Microsoft. Autodiscover
   visar bara att domänen är registrerad i Exchange Online; 7 av 10
   Google-kommuner ger också ja. "Hybridlösning" var inte mätt och är struken.
3. Samtyckesverktyg på amerikanskt nät var 31, inte 28: listan över verktyg
   saknade CookieYes, Klaro och `cookiebot.eu`. Definitionen ligger nu i koden.
4. Två körningar från GitHub Actions som inte klarade kraven var publicerade:
   triangulering (T3 93–96 %) och säkerhet (DNS-fel räknade som saknade poster).
5. DMARC `p=none` beskrevs som att mottagare ombeds leverera förfalskad e-post.
   Det är övervakningsläge. MTA-STS mäts bara som publicerat, inte tillämpat.
6. Gotlands län, med en enda organisation, visade enskilda värden i
   säkerhetsresultatet. Län med färre än fem organisationer slås nu ihop.
7. Den fallna certifikatkörningen (`cert-2026-10-08T180702Z`) hade antal namn
   med privata adresser per organisation, i strid med gränsen. Den är
   borttagen ur `data/`, liksom säkerhetsfilerna i punkt 4 och 6.
8. DKIM-målen i sidans datafiler visade tenantnamn. Nu visas bara leverantören.
9. Mindre: "uppläsningstjänsten vanligast" (näst vanligast efter Google),
   Vimmerby ligger i Kalmar län, två av de tjugo utan tredjepart har webbplatsen
   bakom Cloudflare, "Sunet" på myndighetssidan, rådata saknades för tre
   kontroller (nu `data/webb-organisationer-sjalv-*`, `data/stickprov-*`, och
   9.9.9.9-kontrollen i `data/sakerhet-*`).

### T6 — andra försöket, 2026-10-09

Andra försöket med alla 20 gav 18 av 20 inom 15 procentenheter (krav 16), men
skriptet kraschade när resultatet skulle sparas (fel i hanteringen av
sökvägen). Resultatet finns därför bara som körningens utskrift. Felet är
rättat och T6 körs en tredje gång så att rådata sparas; det är den körningen
som gäller.

## Oberoende granskning av mätning 4 — 2026-10-09

En ny granskare med bara läsrätt räknade om allt från rådatan; alla siffror
stämde. Rättat i formuleringen före publicering:

1. "Medianen per kommun är 3 %" blandade in regionerna. Kommunernas median
   är 0 % (150 av 289 har inga namn på amerikanska nät), regionernas 13 %.
   Kommuner, regioner och myndigheter redovisas nu var för sig.
2. "Ligger i Sverige och Europa" påstod plats; metoden mäter nätägare.
3. Summan drivs av ett fåtal: en kommun står för 25 % av kommunernas namn på
   amerikanska nät. Medianen är huvudmåttet.
4. Jokercertifikat döljer namn och kan överskatta andelen; det står nu under
   "Vad det här inte visar".
5. T6 prövar bara att namnlistan är fullständig: båda källorna läser samma
   certifikatloggar.
6. Spärren: en certifikatkörning publiceras bara om T6 hållit för just den
   körningen. Hygientestet omfattar även T6-filerna.

## Granskning av Codex — 2026-10-09

En granskare från en annan AI-modell (Codex) granskade hela projektet och lade
upp ärenden #9–#23 med motprov. Påståendena kontrollerades mot data och kod
innan något ändrades; de som prövades stämde (Microsoft-klassningen 189 via MX,
52 via SPF och DKIM, 7 via SPF och autodiscover; Grums 0 % mot 14 % i T6; 14
namn på "annat" och 16 på "okänt" nät; tre omätbara webbplatser visade "Nej" på
kartan; `fraga()` gör DNS-fel till tomma svar).

**Rättat i text och visning 2026-10-09** (#12, #15, #19, #21, #22, #23, delar
av #18 och #20):

- Webbmätningen beskrivs som anropsförsök i webbläsarens nätverkslogg, inte
  som genomförd kontakt.
- Microsoft i e-postens DNS redovisas uppdelat på MX och konfiguration (SPF,
  DKIM, autodiscover). Exchange Online beskrivs som registrering; "Bekräftat"
  är struket. DKIM beskrivs som publicerad, inte som faktisk signering.
- Kontrollerna kallas inte längre oberoende; för var och en anges vad den kan
  upptäcka och vad den delar med huvudmätningen.
- Certifikatfyndet säger att inga namn på amerikanska nät *hittades*, redovisar
  "annat" och "okänt" nät och att T6 inte prövar nollkategorin (Grums).
- Det generella påståendet att alla siffror är lägsta nivåer är struket, och
  projektets fråga avgränsas till det som syns utifrån.
- Kartan visar "Kunde inte mätas" i stället för "Nej" vid mätfel.

**Kvar, i kod före mätningen 2026-11-01:** #9 (DNS-fel), #10 (Chrome-krasch),
#11 (täckning i trianguleringen), #13 (webbens spärr), #14 (paginering),
#16 (registrerad domän), #17 (blandade signaler), #18 (koppla triangulering
till rätt DNS-filer). **Större:** #20, en kontroll av klassningen mot facit.

### Rättelser i kod efter Codex granskning — 2026-10-09

**#9 Mätfel i DNS.** Uppslag skiljer nu mellan "posten finns inte" (NXDOMAIN,
NoAnswer) och mätfel (timeout, SERVFAIL, nätfel). Mätfel sparas per fält i
`dns_fel` (fältnamn, inga värdnamn). E-postklassen blir "kunde inte mätas" om
MX-uppslaget misslyckades, eller om resultatet annars blivit "inga
molnsignaler" eller "okänd" och något av SPF-, autodiscover- eller
DKIM-uppslagen misslyckades. Samma uppslag används i trianguleringen.
Certifikatmätningen räknar misslyckade uppslag separat (`dns_fel`) i stället
för som inaktiva namn. **Begränsning:** rådata från före rättelsen saknar
`dns_fel`; där går mätfel inte att skilja från saknade poster.

**#17 Blandade signaler och domängränser.** SPF och DKIM kan nu stödja båda
leverantörerna. När både Microsoft-regeln (SPF + autodiscover eller DKIM) och
Google-regeln (SPF + DKIM) är uppfyllda och MX inte avgör, blir klassen
"Microsoft och Google". Den gamla koden valde tyst Microsoft. Det gäller
Sollentuna, Norrköping och Halmstad i oktobermätningen, som därmed går från
Microsoft till Microsoft och Google: Microsoft-klassade kommuner och regioner
blir 245 i stället för 248. Domänmatchning kräver exakt domän eller punkt före
suffixet (`notgoogle.com` är inte Google), och SPF läses som `include:`-poster
i stället för som fritext.

**#10 Chrome-krasch.** En webbmätning räknas bara om Chrome avslutades
normalt, skrev en nätverkslogg som går att läsa, visade en sida som inte är
Chromes felsida, och om huvudsidan fick ett 2xx-svar *i webbläsaren*. Status
tas från webbläsarens logg, inte från det separata urllib-anropet. Annars
"kunde inte mätas".

**#12 Anropsförsök och svar.** `w2` är som förut anropsförsök som sidan
startade. Nytt fält `w2_svar`: de av dem där webbläsaren läste svarshuvuden.
Klassningen bygger fortfarande på försöken; texterna säger "anrop", och
genomförd kontakt påstås bara där `w2_svar` eller en kontroll i vanlig
webbläsare visar det. Rådata från före rättelsen saknar `w2_svar`.

**#16 Registrerad domän och alias.** Registrerad domän bestäms med Public
Suffix List (`data/public_suffix_list.dat`, version 2026-10-07, commit
3929462), inte som de två sista leden. Undantaget "samma namn under annan
toppdomän" är borttaget; i stället gäller uttryckliga alias med belägg i
`organisationsalias.csv` (i dag `helsingborg.io` för Helsingborgs stad).

**#11 Täckning i trianguleringen.** Godkännande kräver att minst 95 % av
urvalet fått svar i T1, T2 och T4, utöver överensstämmelse bland svaren.
Tomt underlag underkänns.

**#13 Webbens spärr.** Rapport och publicering använder samma kontroll:
minst 95 % mätbara, minst 95 % av tredjepartsvärdarna med nät, och godkända
negativa, positiva och nätkontroller. Tom population underkänns.

**#14 Paginering.** Om en senare sida från Certspotter fallerar efter alla
försök räknas organisationen som ej mätt, inte som ett fullständigt svar.

**#18 Kontrollens datum.** Exchange Online-uppgiften visas med kontrollens
datum. Sidan anger i datafilen om kontrollen gäller samma DNS-mätning som
visas (`trianguleringAvserSammaDns`).

**#19 T6 version 2, för nästa certifikatmätning (skrivet före körning).**
Utöver kravet 16 av 20 inom 15 procentenheter: bland urvalets organisationer
med 0 % i huvudkällan ska den andra källan också ge 0 % för minst 90 %, och
det ska finnas minst 5 sådana. Annars publiceras inte nästa certifikatmätning.
Oktobermätningen gjordes med T6 version 1 och redovisar avvikelsen (Grums).
