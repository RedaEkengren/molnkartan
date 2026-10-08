# Resultat — hela Sverige

Mätt 2026-10-08 15:41 UTC. 290 kommuner och 20 regioner.
Regler: METOD.md, e-postregel v2 och "Nationell körning".
Rådata: `data/ra-organisationer-sverige-2026-10-08T154137Z.json`. Tabellen återskapas med `python3 klassa_v2.py data/ra-organisationer-sverige-2026-10-08T154137Z.json`.

## Sammanfattning

| | Antal | Andel |
|---|---|---|
| E-post syns gå via Microsofts moln | 248 | 80 % |
| E-post hos Google | 10 | 3 % |
| Inga molnsignaler för e-post | 20 | 6 % |
| Okänd | 32 | 10 % |

Före DKIM-rättelsen (se nedan): Microsoft 245, okänd 35.
| **Har en Microsoft Entra-tenant** | **309** | **>99 %** |

Webb (`www.`-adressen): 284 hos svenska eller europeiska leverantörer, 16 bakom
Cloudflare, 5 hos Microsoft, 1 vardera hos Akamai, Google och AWS, 2 okända.

**Vad det betyder:** organisationerna är *anslutna till* tjänsterna. Det säger
ingenting om vilka uppgifter som behandlas där. Se README, "Vad det här inte visar".

## Rättelse 2026-10-08

Regeln för DKIM (S7) missade Microsofts nyare postformat (`*.dkim.mail.microsoft`).
Gotland, Sjöbo och Bromölla byter därför från okänd till Microsoft. Skälet och
effekten står i `METOD.md`, "Rättelse". Felet hittades av sidans animation.

## Iakttagelser

- **Östergötland avviker.** Fem kommuner (bland dem Linköping) har e-post hos
  Google, och fyra till saknar molnsignaler för e-post. Det är det enda län där
  Microsoft inte dominerar.
- **Google tar emot, Microsoft signerar.** Fem av de tio med e-post hos Google
  (Ödeshög, Ydre, Boxholm, Åtvidaberg, Vimmerby) har ändå DKIM-nycklar hos
  Microsoft. De tar emot e-post via Google men skickar troligen via Microsoft.
- **Gällivare** är den enda utan tenant. Domänen från Wikidata, `gellivare.se`,
  har ingen. `gallivare.se` har både tenant och e-post via Microsoft, och båda
  domänerna är i bruk. Metoden mäter en domän per organisation och missar det.
- **Region Östergötland och Region Kalmar län** saknar molnsignaler för e-post,
  som de enda två regionerna.

## Per län

| Län | Organisationer | Microsoft | Google | Inga molnsignaler | Okänd |
|---|---|---|---|---|---|
| Blekinge län | 6 | 4 | 0 | 0 | 2 |
| Dalarnas län | 16 | 16 | 0 | 0 | 0 |
| Gotlands län | 1 | 1 | 0 | 0 | 0 |
| Gävleborgs län | 11 | 8 | 0 | 0 | 3 |
| Hallands län | 7 | 6 | 0 | 0 | 1 |
| Jämtlands län | 9 | 8 | 0 | 0 | 1 |
| Jönköpings län | 14 | 12 | 0 | 1 | 1 |
| Kalmar län | 13 | 10 | 1 | 1 | 1 |
| Kronobergs län | 9 | 9 | 0 | 0 | 0 |
| Norrbottens län | 15 | 15 | 0 | 0 | 0 |
| Skåne län | 34 | 33 | 0 | 1 | 0 |
| Stockholms län | 27 | 19 | 1 | 2 | 5 |
| Södermanlands län | 10 | 7 | 1 | 2 | 0 |
| Uppsala län | 9 | 7 | 0 | 0 | 2 |
| Värmlands län | 17 | 12 | 0 | 0 | 5 |
| Västerbottens län | 16 | 14 | 0 | 1 | 1 |
| Västernorrlands län | 8 | 6 | 1 | 1 | 0 |
| Västmanlands län | 11 | 11 | 0 | 0 | 0 |
| Västra Götalands län | 50 | 35 | 1 | 7 | 7 |
| Örebro län | 13 | 12 | 0 | 0 | 1 |
| Östergötlands län | 14 | 3 | 5 | 4 | 2 |

## Alla organisationer

S1 MX, S2 SPF, S4 autodiscover, S7 DKIM, S8 Entra-registrering/Teams.
"gateway/egen" betyder att en säkerhetstjänst eller egen server står först i MX.

| Organisation | E-post v2 | S1 | S2 | S4 | S7 | S8 | MS-tenant | Webb |
|---|---|---|---|---|---|---|---|---|
| Upplands Väsby | okänd | gateway/egen | G | - | - | MS | ja | SE/EU |
| Vallentuna | okänd | blandat | MS | - | - | MS | ja | SE/EU |
| Österåker | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Värmdö | MS | MS | - | - | MS | - | ja | SE/EU |
| Järfälla | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Ekerö | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Huddinge | MS | MS | - | - | MS | - | ja | SE/EU |
| Botkyrka | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Salem | G | G | G | - | G | - | ja | SE/EU |
| Haninge | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Tyresö | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Upplands-Bro | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Nykvarn | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Täby | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Danderyd | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Sollentuna | MS | gateway/egen | MS | - | MS | MS | ja | Cloudflare |
| Stockholm | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Södertälje | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Nacka | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Sundbyberg | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Solna | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lidingö | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Vaxholm | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Norrtälje | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Sigtuna | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Nynäshamn | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Håbo | MS | MS | - | MS | MS | - | ja | SE/EU |
| Älvkarleby | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Knivsta | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Heby | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Tierp | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Uppsala | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Enköping | okänd | gateway/egen | - | - | MS | MS | ja | SE/EU |
| Östhammar | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Vingåker | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Gnesta | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Nyköping | inga molnsignaler | gateway/egen | - | - | - | MS | ja | Cloudflare |
| Oxelösund | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Flen | G | G | G | - | G | - | ja | SE/EU |
| Katrineholm | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Eskilstuna | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Strängnäs | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Trosa | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Ödeshög | G | G | - | - | MS | - | ja | SE/EU |
| Ydre | G | G | - | - | MS | - | ja | SE/EU |
| Kinda | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Boxholm | G | G | - | - | MS | - | ja | SE/EU |
| Åtvidaberg | G | G | - | - | MS | - | ja | SE/EU |
| Finspång | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Valdemarsvik | inga molnsignaler | gateway/egen | - | - | - | MS | ja | okänd |
| Linköping | G | G | G | - | - | - | ja | SE/EU |
| Norrköping | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Söderköping | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Motala | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Vadstena | okänd | gateway/egen | MS | - | - | - | ja | AWS |
| Mjölby | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Aneby | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Gnosjö | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Mullsjö | MS | MS | MS | MS | - | MS | ja | SE/EU |
| Habo | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Gislaved | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Vaggeryd | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Jönköping | okänd | gateway/egen | - | - | MS | MS | ja | SE/EU |
| Nässjö | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Värnamo | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Sävsjö | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Vetlanda | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Eksjö | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Tranås | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Uppvidinge | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lessebo | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Tingsryd | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Alvesta | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Älmhult | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Markaryd | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Växjö | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Ljungby | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Högsby | MS | MS | MS | MS | - | - | ja | SE/EU |
| Torsås | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Mörbylånga | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Hultsfred | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Mönsterås | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Emmaboda | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Kalmar | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Nybro | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Oskarshamn | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Västervik | okänd | gateway/egen | - | - | MS | MS | ja | Cloudflare |
| Vimmerby | G | G | - | - | MS | - | ja | SE/EU |
| Borgholm | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Gotland | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Olofström | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Karlskrona | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Ronneby | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Karlshamn | MS | MS | - | - | MS | MS | ja | SE/EU |
| Sölvesborg | MS | MS | - | MS | MS | - | ja | SE/EU |
| Svalöv | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Staffanstorp | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Burlöv | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Vellinge | MS | blandat | MS | MS | MS | MS | ja | SE/EU |
| Östra Göinge | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Örkelljunga | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Bjuv | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Kävlinge | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lomma | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Svedala | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Skurup | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Sjöbo | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Hörby | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Höör | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Tomelilla | MS | MS | - | - | MS | MS | ja | SE/EU |
| Bromölla | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Osby | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Perstorp | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Klippan | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Åstorp | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Båstad | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Malmö | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lund | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Landskrona | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Helsingborg | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Höganäs | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Eslöv | MS | MS | - | - | MS | - | ja | SE/EU |
| Ystad | MS | MS | MS | - | MS | - | ja | SE/EU |
| Trelleborg | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Kristianstad | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Simrishamn | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Ängelholm | MS | MS | - | - | MS | - | ja | SE/EU |
| Hässleholm | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Hylte | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Halmstad | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Laholm | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Falkenberg | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Varberg | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Kungsbacka | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Härryda | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Partille | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Öckerö | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Stenungsund | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Tjörn | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Orust | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Sotenäs | MS | MS | MS | MS | MS | MS | ja | MS |
| Munkedal | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Tanum | okänd | gateway/egen | - | - | MS | MS | ja | SE/EU |
| Dals-Ed | G | G | G | - | G | - | ja | SE/EU |
| Färgelanda | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Ale | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lerum | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Vårgårda | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Bollebygd | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Grästorp | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Essunga | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Karlsborg | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Gullspång | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Tranemo | MS | MS | MS | - | MS | - | ja | SE/EU |
| Bengtsfors | MS | MS | - | MS | - | MS | ja | SE/EU |
| Mellerud | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lilla Edet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Mark | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Svenljunga | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Herrljunga | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Vara | okänd | gateway/egen | - | - | MS | - | ja | SE/EU |
| Götene | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Tibro | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Töreboda | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Göteborg | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Mölndal | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Kungälv | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Lysekil | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Uddevalla | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Strömstad | okänd | blandat | - | - | MS | MS | ja | SE/EU |
| Vänersborg | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Trollhättan | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Alingsås | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Borås | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Ulricehamn | MS | MS | MS | - | MS | - | ja | SE/EU |
| Åmål | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Mariestad | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Lidköping | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Skara | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Skövde | MS | MS | MS | - | MS | MS | ja | Cloudflare |
| Hjo | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Tidaholm | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Falköping | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Kil | okänd | gateway/egen | - | MS | MS | MS | ja | SE/EU |
| Eda | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Torsby | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Storfors | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Hammarö | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Munkfors | MS | gateway/egen | MS | - | MS | MS | ja | okänd |
| Forshaga | okänd | gateway/egen | - | MS | MS | MS | ja | SE/EU |
| Grums | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Årjäng | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Sunne | okänd | gateway/egen | - | - | MS | MS | ja | Cloudflare |
| Karlstad | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Kristinehamn | MS | MS | - | MS | MS | MS | ja | Cloudflare |
| Filipstad | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Hagfors | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Arvika | okänd | gateway/egen | - | MS | MS | MS | ja | SE/EU |
| Säffle | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Lekeberg | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Laxå | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Hallsberg | MS | MS | MS | - | MS | - | ja | SE/EU |
| Degerfors | MS | gateway/egen | MS | MS | - | MS | ja | SE/EU |
| Hällefors | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Ljusnarsberg | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Örebro | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Kumla | okänd | gateway/egen | - | MS | - | MS | ja | SE/EU |
| Askersund | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Karlskoga | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Nora | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lindesberg | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Skinnskatteberg | MS | MS | MS | MS | - | MS | ja | SE/EU |
| Surahammar | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Kungsör | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Hallstahammar | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Norberg | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Västerås | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Sala | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Fagersta | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Köping | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Arboga | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Vansbro | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Malung-Sälen | MS | MS | MS | MS | - | MS | ja | SE/EU |
| Gagnef | MS | MS | MS | MS | MS | MS | ja | MS |
| Leksand | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Rättvik | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Orsa | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Älvdalen | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Smedjebacken | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Mora | MS | MS | MS | MS | - | - | ja | SE/EU |
| Falun | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Borlänge | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Säter | MS | MS | MS | MS | MS | MS | ja | G |
| Hedemora | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Avesta | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Ludvika | MS | MS | MS | - | MS | - | ja | SE/EU |
| Ockelbo | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Hofors | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Ovanåker | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Nordanstig | MS | gateway/egen | MS | MS | - | MS | ja | SE/EU |
| Ljusdal | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Gävle | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Sandviken | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Söderhamn | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Bollnäs | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Hudiksvall | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Ånge | MS | MS | MS | MS | - | MS | ja | SE/EU |
| Timrå | G | gateway/egen | G | - | G | - | ja | SE/EU |
| Härnösand | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Sundsvall | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Kramfors | MS | MS | MS | - | - | MS | ja | SE/EU |
| Sollefteå | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Örnsköldsvik | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Ragunda | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Bräcke | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Krokom | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Strömsund | okänd | gateway/egen | - | - | MS | MS | ja | SE/EU |
| Åre | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Berg | MS | gateway/egen | MS | MS | - | - | ja | SE/EU |
| Härjedalen | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Östersund | MS | gateway/egen | MS | MS | - | MS | ja | SE/EU |
| Nordmaling | okänd | gateway/egen | - | - | MS | - | ja | SE/EU |
| Bjurholm | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Vindeln | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Robertsfors | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Norsjö | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Malå | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Storuman | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Sorsele | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Dorotea | MS | MS | MS | MS | MS | MS | ja | MS |
| Vännäs | MS | MS | - | - | MS | MS | ja | SE/EU |
| Vilhelmina | MS | MS | MS | MS | - | - | ja | MS |
| Åsele | MS | MS | MS | MS | MS | - | ja | MS |
| Umeå | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lycksele | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Skellefteå | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Arvidsjaur | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Arjeplog | MS | gateway/egen | MS | MS | - | - | ja | SE/EU |
| Jokkmokk | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Överkalix | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Kalix | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Övertorneå | MS | MS | MS | MS | - | MS | ja | SE/EU |
| Pajala | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Gällivare | MS | gateway/egen | MS | - | MS | - | nej | SE/EU |
| Älvsbyn | MS | gateway/egen | MS | MS | - | MS | ja | SE/EU |
| Luleå | MS | MS | - | MS | MS | MS | ja | SE/EU |
| Piteå | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Boden | MS | blandat | MS | MS | MS | MS | ja | SE/EU |
| Haparanda | MS | gateway/egen | MS | MS | - | MS | ja | SE/EU |
| Kiruna | MS | MS | MS | - | MS | - | ja | SE/EU |
| Region Stockholm | MS | gateway/egen | MS | MS | MS | MS | ja | Cloudflare |
| Region Uppsala | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Region Sörmland | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Region Östergötland | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Region Jönköpings län | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Region Kronoberg | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Region Kalmar län | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Region Blekinge | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Region Skåne | MS | MS | MS | - | MS | MS | ja | Akamai |
| Region Halland | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Västra Götalandsregionen | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Region Värmland | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Region Örebro län | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Region Västmanland | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Region Dalarna | MS | MS | MS | - | MS | MS | ja | Cloudflare |
| Region Gävleborg | MS | MS | MS | - | MS | - | ja | Cloudflare |
| Region Västernorrland | MS | MS | MS | - | - | MS | ja | SE/EU |
| Region Jämtland Härjedalen | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Region Västerbotten | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Region Norrbotten | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
