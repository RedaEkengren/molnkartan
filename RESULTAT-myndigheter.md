# Resultat — statliga myndigheter

Regler: METOD.md, "Mätning 3". 252 myndigheter ur SCB:s myndighetsregister,
202 unika e-postdomäner mätta; 11 nämnder saknar e-post och webb i registret.

- E-post och konton: `data/ra-organisationer-myndigheter-matning-2026-10-08T164214Z.json`
- Webbplatser: `data/webb-organisationer-myndigheter-matning-2026-10-08T164403Z.json`

## Utfall mot kriterierna

| | Krav | Utfall |
|---|---|---|
| E-post entydig | ≥85 % | 189/202 = 94 % |
| Tredjepartsvärdar med ASN | ≥95 % | 168/170 = 99 % |
| Mätbara webbplatser | ≥95 % | 193/202 = 96 % |

## Sammanfattning

| E-post | Antal domäner |
|---|---|
| Microsofts moln | 85 |
| Google | 1 |
| Inga molnsignaler | 103 |
| Okänd | 13 |

Microsoft Entra-tenant: 189 av 202.

| Webbplats före samtycke | Antal |
|---|---|
| US-nät före samtycke | 115 |
| bara EU/EES-nät före samtycke | 35 |
| ingen tredjepart | 35 |
| kunde inte mätas | 9 |
| annat nät före samtycke | 8 |

Google Analytics/Tag Manager före samtycke: 30: Arbetsgivarverket, Barnombudsmannen, Bokföringsnämnden, Centrala studiestödsnämnden, Ekobrottsmyndigheten, Etikprövningsmyndigheten, Folke bernadotteakademin, Forskningsrådet f miljö, areella näringar och samhällsbyggande, Försvarsmakten, Gentekniknämnden, Göteborgs universitet, Högskolan i halmstad, Karolinska institutet, Klimatpolitiska rådet, Kommerskollegium, Linnéuniversitetet, Mittuniversitetet, Moderna museet, Nationalmuseum, Patent- och registreringsverket, Polarforskningssekretariatet, Rättsmedicinalverket, Statens beredning för medicinsk och social utvärdering, Statens historiska museer, Statens museer för världskultur, Statens veterinärmedicinska anstalt, Svenska institutet, Trafikanalys, Upphandlingsmyndigheten, Vetenskapsrådet.

## Iakttagelser

- **Myndigheter skiljer sig från kommuner.** Hälften av domänerna har e-post
  utan molnsignaler, ofta på egna servrar, hos Sunet, Advania eller Nordlo.
  Sex domäner tar emot e-post via Skatteverkets servrar.
- **Skatteverket syns inte.** E-post utan molnsignaler, webbplats utan
  tredjeparter, men en Microsoft-tenant. Enligt Ekot används amerikanska
  molntjänster i stor skala. Mätningen ser inte det som sker bakom inloggning.
- **Stickprov:** Försvarsmakten laddar Google Tag Manager före samtycke,
  bekräftat i en vanlig Chrome via `performance.getEntriesByType("resource")`.
  Inga anrop till Google Analytics syntes.

## E-post per domän

| Organisation | E-post v2 | S1 | S2 | S4 | S7 | S8 | MS-tenant | Webb |
|---|---|---|---|---|---|---|---|---|
| Kammarkollegiet | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Allmänna reklamationsnämnden | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Statens jordbruksverk | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Arbetsförmedlingen | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Arbetsgivarverket | MS | MS | MS | - | MS | MS | ja | Cloudflare |
| Arbetsmiljöverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Arvfondsdelegationen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Barnombudsmannen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Blekinge tekniska högskola | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Bokföringsnämnden | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Bolagsverket | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Boverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Brottsförebyggande rådet | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Brottsoffermyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | MS |
| Centrala studiestödsnämnden | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Diskrimineringsombudsmannen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| dom.se (delas av 7 myndigheter) | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| E-hälsomyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Ekobrottsmyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Elsäkerhetsverket | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Energimarknadsinspektionen | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Etikprövningsmyndigheten | okänd | gateway/egen | MS | - | - | MS | ja | okänd |
| Exportkreditnämnden | inga molnsignaler | gateway/egen | - | - | - | MS | ja | Cloudflare |
| Fastighetsmäklarinspektionen | MS | MS | MS | MS | MS | MS | ja | MS |
| Finansinspektionen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Finanspolitiska rådet | MS | gateway/egen | MS | MS | - | - | ja | SE/EU |
| Folke bernadotteakademin | MS | MS | MS | MS | MS | - | ja | MS |
| Folkhälsomyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | Akamai |
| Fondtorgsnämnden | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Forskarskattenämnden | inga molnsignaler | gateway/egen | - | - | - | - | nej | SE/EU |
| Forskningsrådet f miljö, areella näringar och samhällsbyggande | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Forskningsrådet för hälsa, arbetsliv och välfärd | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Fortifikationsverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Forum för levande historia | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Försvarets materielverk | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Försvarets radioanstalt | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Försvarshögskolan | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Försvarsmakten | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Försäkringskassan | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Gentekniknämnden | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Gymnastik- och idrottshögskolan (GIH) | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Göteborgs universitet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Harpsundsnämnden | inga molnsignaler | gateway/egen | - | - | - | - | nej | SE/EU |
| Havs- och vattenmyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Socialstyrelsen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Högskolan dalarna | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Högskolan i borås | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Högskolan i gävle | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Högskolan i halmstad | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Högskolan i skövde | MS | gateway/egen | MS | - | MS | - | ja | SE/EU |
| Högskolan kristianstad | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Högskolan väst | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Högskolans avskiljandenämnd | inga molnsignaler | gateway/egen | - | - | - | - | nej | SE/EU |
| regeringskansliet.se (delas av 3 myndigheter) | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Inspektionen för arbetslöshetsförsäkring | inga molnsignaler | gateway/egen | - | - | - | MS | ja | okänd |
| Inspektionen för socialförsäkringen | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Inspektionen för strategiska produkter | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Inspektionen för vård och omsorg | inga molnsignaler | gateway/egen | - | - | - | MS | ja | okänd |
| Institutet för arbetsmarknads-och utbildningspolitisk utvärdering | inga molnsignaler | gateway/egen | - | - | - | - | ja | okänd |
| Institutet för mänskliga rättigheter | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Institutet för rymdfysik | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Institutet för språk och folkminnen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Integritetsskyddsmyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Justitiekanslern | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Jämställdhetsmyndigheten | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Karlstads universitet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Karolinska institutet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Kemikalieinspektionen | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Klimatpolitiska rådet | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Kommerskollegium | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Konjunkturinstitutet | MS | gateway/egen | MS | MS | MS | - | ja | Cloudflare |
| Konkurrensverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Konstfack | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Konstnärsnämnden | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Konsumentverket | MS | MS | - | MS | MS | MS | ja | MS |
| Kriminalvården | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Kronofogdemyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Kungliga biblioteket | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Kungliga konsthögskolan | MS | MS | MS | MS | - | MS | ja | SE/EU |
| Kungliga musikhögskolan | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Kungliga tekniska högskolan | MS | gateway/egen | MS | - | MS | MS | ja | SE/EU |
| Kustbevakningen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Lantmäteriet | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Linköpings universitet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Linnéuniversitetet | MS | MS | MS | - | MS | MS | ja | Cloudflare |
| Livsmedelsverket | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Luleå tekniska universitet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Lunds universitet | MS | MS | - | - | MS | MS | ja | SE/EU |
| Läkemedelsverket | okänd | gateway/egen | MS | - | - | - | ja | Cloudflare |
| lansstyrelsen.se (delas av 21 myndigheter) | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Malmö universitet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Mediemyndigheten | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Medlingsinstitutet | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Migrationsverket | MS | MS | MS | - | - | - | ja | SE/EU |
| Mittuniversitetet | MS | blandat | MS | MS | MS | MS | ja | Cloudflare |
| Moderna museet | MS | gateway/egen | MS | MS | MS | MS | ja | Cloudflare |
| Myndigheten för civilt försvar | inga molnsignaler | gateway/egen | - | - | - | - | ja | Akamai |
| Myndigheten för delaktighet | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Myndigheten för digital förvaltning | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Myndigheten för familjerätt och föräldraskapsstöd | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Myndigheten för kulturanalys | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Myndigheten för psykologiskt försvar | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Myndigheten för säkerhet och integritetsskydd | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Myndigheten för tillgängliga medier | MS | MS | MS | MS | MS | MS | ja | MS |
| Myndigheten för tillväxtpolitiska utvärderingar och analyser | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Myndigheten för totalförsvarsanalys | inga molnsignaler | gateway/egen | - | - | - | - | nej | Cloudflare |
| Myndigheten för ungdoms-och civilsamhällesfrågor | okänd | gateway/egen | - | MS | - | MS | ja | Akamai |
| Myndigheten för vård- och omsorgsanalys | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Myndigheten för yrkeshögskolan | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Mälardalens universitet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Nationalmuseum | MS | MS | MS | MS | MS | MS | ja | Akamai |
| Naturhistoriska riksmuseet | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Naturvårdsverket | inga molnsignaler | gateway/egen | - | - | - | MS | ja | Cloudflare |
| Nordiska afrikainstitutet | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Nämnden för hemslöjdsfrågor | inga molnsignaler | gateway/egen | - | - | - | - | nej | SE/EU |
| Nämnden för prövning av oredlighet i forskning | okänd | gateway/egen | MS | - | - | - | nej | SE/EU |
| Nämnden mot Diskriminering | inga molnsignaler | gateway/egen | - | - | - | - | nej | okänd |
| Oljekrisnämnden | inga molnsignaler | gateway/egen | - | - | - | - | nej | okänd |
| Patent- och registreringsverket | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Patentombudsnämnden | inga molnsignaler | gateway/egen | - | - | - | - | nej | SE/EU |
| Pensionsmyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Polarforskningssekretariatet | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Polismyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Post- och telestyrelsen | MS | MS | MS | MS | MS | - | ja | okänd |
| Revisorsinspektionen | inga molnsignaler | gateway/egen | - | - | - | - | ja | MS |
| Riksantikvarieämbetet | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Riksarkivet | okänd | gateway/egen | - | MS | - | MS | ja | SE/EU |
| Riksgäldskontoret | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Rymdstyrelsen | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Rättsmedicinalverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Sameskolstyrelsen | G | G | G | - | - | - | ja | SE/EU |
| Sametinget | MS | blandat | MS | - | MS | - | ja | SE/EU |
| Sida | inga molnsignaler | gateway/egen | - | - | - | - | ja | AWS |
| Skatterättsnämnden | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Skatteverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Skogsstyrelsen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Skolforskningsinstitutet | MS | MS | MS | MS | - | MS | ja | SE/EU |
| Skolväsendets överklagandenämnd | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Specialpedagogiska skolmyndigheten | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Spelinspektionen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Statens beredning för medicinsk och social utvärdering | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Statens energimyndighet | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Statens fastighetsverk | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Statens geotekniska institut | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Statens haverikommission | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Statens historiska museer | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Statens inspektion för försvarsunderrättelseverksamheten (SIUN) | inga molnsignaler | gateway/egen | - | - | - | - | nej | SE/EU |
| Statens institutionsstyrelse | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Statens kulturråd | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Statens museer för maritim, transport- och försvarshistoria | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Statens museer för världskultur | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Statens musikverk | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Statens servicecenter | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Statens skolinspektion | okänd | gateway/egen | MS | - | - | MS | ja | SE/EU |
| Statens skolverk | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Statens tjänstepensions- och grupplivnämnd | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Statens veterinärmedicinska anstalt | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Statens väg- och transportforskningsinstitut | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Statistiska centralbyrån | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Statskontoret | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Stockholms konstnärliga högskola | MS | MS | MS | MS | - | MS | ja | MS |
| Stockholms universitet | okänd | gateway/egen | - | - | MS | - | ja | SE/EU |
| Strålsäkerhetsmyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Styrelsen för ackreditering och teknisk kontroll | inga molnsignaler | gateway/egen | - | - | - | MS | ja | AWS |
| Svenska esf-rådet | okänd | gateway/egen | MS | - | - | - | ja | SE/EU |
| Svenska institutet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Svenska institutet för europapolitiska studier | MS | MS | MS | MS | - | MS | ja | SE/EU |
| Sveriges författarfond | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Sveriges geologiska undersökning | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Sveriges lantbruksuniversitet | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Sveriges meteorologiska och hydrologiska institut | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Säkerhetspolisen | inga molnsignaler | gateway/egen | - | - | - | - | ja | okänd |
| Södertörns högskola | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Tandvårds-och läkemedelsförmånsverket, TLV | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Tillväxtverket | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Totalförsvarets forskningsinstitut, foi | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Totalförsvarets plikt- och prövningsverk | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Trafikanalys | MS | MS | MS | MS | MS | MS | ja | Cloudflare |
| Trafikverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Transportstyrelsen | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Tullverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | Akamai |
| Umeå universitet | MS | MS | MS | MS | MS | - | ja | SE/EU |
| Universitets- och högskolerådet | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Universitetskanslersämbetet | inga molnsignaler | gateway/egen | - | - | - | MS | nej | SE/EU |
| Upphandlingsmyndigheten | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Uppsala universitet | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Utbetalningsmyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | nej | SE/EU |
| Valmyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | Akamai |
| Verket för innovationssystem | MS | gateway/egen | MS | MS | MS | MS | ja | SE/EU |
| Vetenskapsrådet | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Åklagarmyndigheten | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |
| Örebro universitet | MS | MS | MS | - | MS | MS | ja | SE/EU |
| Överklagandenämnden för etikprövning | MS | MS | - | MS | MS | - | ja | SE/EU |
| Överklagandenämnden för högskolan | inga molnsignaler | gateway/egen | - | - | - | - | nej | SE/EU |
| Överklagandenämnden för studiestöd | MS | MS | MS | MS | - | MS | ja | SE/EU |
| riksdagen.se (delas av 2 myndigheter) | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Riksdagens ombudsmän | inga molnsignaler | gateway/egen | - | - | - | - | ja | okänd |
| Riksrevisionen | MS | MS | MS | MS | MS | MS | ja | SE/EU |
| Sveriges riksbank | MS | MS | MS | - | MS | MS | ja | Cloudflare |
| Luftfartsverket | inga molnsignaler | gateway/egen | - | - | - | - | ja | SE/EU |
| Sjöfartsverket | inga molnsignaler | gateway/egen | - | - | - | MS | ja | SE/EU |
| Svenska kraftnät | inga molnsignaler | gateway/egen | - | - | - | - | ja | Cloudflare |

## Webbplats per domän

| Organisation | Klass (v3) | Google Analytics/GTM | Värdar på US-nät | Leverantörer (där kända) |
|---|---|---|---|---|
| Kammarkollegiet | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Allmänna reklamationsnämnden | US-nät före samtycke | – | cdnjs.cloudflare.com, code.jquery.com, plus.browsealoud.com, policy.app.cookieinformation.com, www.browsealoud.com | Cloudflare, Cookie Information, Texthelp, jQuery CDN |
| Statens jordbruksverk | ingen tredjepart | – | – | – |
| Arbetsförmedlingen | annat nät före samtycke | – | – | Piwik PRO |
| Arbetsgivarverket | US-nät före samtycke | ja | script.hotjar.com, static.hotjar.com, www.googletagmanager.com | Google, Hotjar, Rek.ai |
| Arbetsmiljöverket | US-nät före samtycke | – | dl.episerver.net | Optimizely, ReadSpeaker |
| Arvfondsdelegationen | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Web Service Award |
| Barnombudsmannen | US-nät före samtycke | ja | cdn.matomo.cloud, consent.cookiebot.com, consentcdn.cookiebot.com, www.googletagmanager.com | Google, InnoCraft (Matomo Cloud), ReadSpeaker, Usercentrics (Cookiebot) |
| Blekinge tekniska högskola | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Bokföringsnämnden | US-nät före samtycke | ja | fonts.googleapis.com, fonts.gstatic.com, www.google-analytics.com, www.googletagmanager.com | Google, Vizzit |
| Bolagsverket | kunde inte mätas | – | – | – |
| Boverket | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Usercentrics (Cookiebot) |
| Brottsförebyggande rådet | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Brottsoffermyndigheten | US-nät före samtycke | – | 7157.global.siteimproveanalytics.io, dc.services.visualstudio.com, js.monitor.azure.com, siteimproveanalytics.com | Insipio, Microsoft, Siteimprove |
| Centrala studiestödsnämnden | US-nät före samtycke | ja | www.googletagmanager.com | Google |
| Diskrimineringsombudsmannen | US-nät före samtycke | – | policy.app.cookieinformation.com | Cookie Information, ReadSpeaker |
| dom.se (delas av 7 myndigheter) | ingen tredjepart | – | – | – |
| E-hälsomyndigheten | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com, js.monitor.azure.com, swedencentral-0.in.applicationinsights.azure.com | Microsoft, Rek.ai, Usercentrics (Cookiebot) |
| Ekobrottsmyndigheten | US-nät före samtycke | ja | region1.google-analytics.com, www.googletagmanager.com | Google, Vizzit |
| Elsäkerhetsverket | US-nät före samtycke | – | dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com, policy.app.cookieinformation.com, widget-api.netigate.se, widget.netigate.se, www.google.com, www.gstatic.com | Cookie Information, Google, Optimizely |
| Energimarknadsinspektionen | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Etikprövningsmyndigheten | US-nät före samtycke | ja | cdn-cookieyes.com, fonts.googleapis.com, log.cookieyes.com, region1.google-analytics.com, www.googletagmanager.com | Google |
| Exportkreditnämnden | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Usercentrics (Cookiebot) |
| Fastighetsmäklarinspektionen | annat nät före samtycke | – | – | Plausible Analytics |
| Finansinspektionen | US-nät före samtycke | – | cdn.cookietractor.com | Vizzit |
| Finanspolitiska rådet | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Folke bernadotteakademin | US-nät före samtycke | ja | consent.cookiebot.com, consentcdn.cookiebot.com, www.googletagmanager.com | Google, Usercentrics (Cookiebot) |
| Folkhälsomyndigheten | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Rek.ai, Usercentrics (Cookiebot) |
| Fondtorgsnämnden | bara EU/EES-nät före samtycke | – | – | – |
| Forskarskattenämnden | ingen tredjepart | – | – | – |
| Forskningsrådet f miljö, areella näringar och samhällsbyggande | US-nät före samtycke | ja | cdn.matomo.cloud, formas.matomo.cloud, region1.google-analytics.com, www.googletagmanager.com, www.gstatic.com | Google, InnoCraft (Matomo Cloud), ReadSpeaker |
| Forskningsrådet för hälsa, arbetsliv och välfärd | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Piwik PRO, Usercentrics (Cookiebot) |
| Fortifikationsverket | ingen tredjepart | – | – | – |
| Forum för levande historia | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp |
| Försvarets materielverk | US-nät före samtycke | – | fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Google, Vizzit |
| Försvarets radioanstalt | ingen tredjepart | – | – | – |
| Försvarshögskolan | ingen tredjepart | – | – | – |
| Försvarsmakten | US-nät före samtycke | ja | js.monitor.azure.com, northeurope-2.in.applicationinsights.azure.com, www.googletagmanager.com | Google, Microsoft |
| Försäkringskassan | ingen tredjepart | – | – | – |
| Gentekniknämnden | US-nät före samtycke | ja | a.nel.cloudflare.com, cdnjs.cloudflare.com, fonts.googleapis.com, fonts.gstatic.com, www.googletagmanager.com | Cloudflare, Google |
| Gymnastik- och idrottshögskolan (GIH) | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Göteborgs universitet | US-nät före samtycke | ja | 7340.global.siteimproveanalytics.io, p.typekit.net, siteimproveanalytics.com, use.typekit.net, www.googletagmanager.com | Adobe, Google, Siteimprove |
| Harpsundsnämnden | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google |
| Havs- och vattenmyndigheten | ingen tredjepart | – | – | – |
| Socialstyrelsen | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Högskolan dalarna | US-nät före samtycke | – | dl.episerver.net, ka-p.fontawesome.com, kit.fontawesome.com, maxcdn.bootstrapcdn.com | Fonticons (Font Awesome), Optimizely |
| Högskolan i borås | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com, www.google.com, www.gstatic.com | Google, Usercentrics (Cookiebot) |
| Högskolan i gävle | US-nät före samtycke | – | 7400.global.siteimproveanalytics.io, siteimproveanalytics.com | Piwik PRO, ReadSpeaker, Siteimprove |
| Högskolan i halmstad | US-nät före samtycke | ja | fonts.googleapis.com, fonts.gstatic.com, pagead2.googlesyndication.com, www.googletagmanager.com | Google, Rek.ai, Vizzit |
| Högskolan i skövde | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Högskolan kristianstad | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com, fonts.googleapis.com, fonts.gstatic.com | Google, Usercentrics (Cookiebot) |
| Högskolan väst | US-nät före samtycke | – | 8285.global.siteimproveanalytics.io, consent.cookiebot.com, consentcdn.cookiebot.com, siteimproveanalytics.com | Rek.ai, Siteimprove, Usercentrics (Cookiebot) |
| Högskolans avskiljandenämnd | US-nät före samtycke | – | p.typekit.net, plus.browsealoud.com, use.typekit.net, www.browsealoud.com | Adobe, Piwik PRO, Texthelp |
| regeringskansliet.se (delas av 3 myndigheter) | US-nät före samtycke | – | www.gstatic.com | Google, ReadSpeaker |
| Inspektionen för arbetslöshetsförsäkring | US-nät före samtycke | – | 7420.global.siteimproveanalytics.io, dl.episerver.net, siteimproveanalytics.com | Optimizely, Siteimprove |
| Inspektionen för socialförsäkringen | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Vizzit |
| Inspektionen för strategiska produkter | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Inspektionen för vård och omsorg | US-nät före samtycke | – | cdn.cookietractor.com, cdn.jsdelivr.net, code.jquery.com, fonts.googleapis.com, maxcdn.bootstrapcdn.com | Google, ReadSpeaker, jQuery CDN, jsDelivr |
| Institutet för arbetsmarknads-och utbildningspolitisk utvärdering | annat nät före samtycke | – | – | ReadSpeaker, Vizzit |
| Institutet för mänskliga rättigheter | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Institutet för rymdfysik | ingen tredjepart | – | – | – |
| Institutet för språk och folkminnen | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Integritetsskyddsmyndigheten | annat nät före samtycke | – | – | Plausible Analytics |
| Justitiekanslern | ingen tredjepart | – | – | – |
| Jämställdhetsmyndigheten | US-nät före samtycke | – | cdnjs.cloudflare.com, consent.cookiebot.com, consentcdn.cookiebot.com, siteimproveanalytics.com | Cloudflare, Siteimprove, Usercentrics (Cookiebot) |
| Karlstads universitet | ingen tredjepart | – | – | – |
| Karolinska institutet | US-nät före samtycke | ja | cdn.jsdelivr.net, region1.google-analytics.com, www.googletagmanager.com | Google, jsDelivr |
| Kemikalieinspektionen | US-nät före samtycke | – | 7477.global.siteimproveanalytics.io, siteimproveanalytics.com | Piwik PRO, Siteimprove |
| Klimatpolitiska rådet | US-nät före samtycke | ja | cdn.matomo.cloud, fonts.googleapis.com, formas.matomo.cloud, region1.google-analytics.com, www.googletagmanager.com | Google, InnoCraft (Matomo Cloud) |
| Kommerskollegium | US-nät före samtycke | ja | www.googletagmanager.com | Google |
| Konjunkturinstitutet | US-nät före samtycke | – | cdn.matomo.cloud, consent.cookiebot.com, consentcdn.cookiebot.com, fonts.googleapis.com, fonts.gstatic.com | Google, InnoCraft (Matomo Cloud), Usercentrics (Cookiebot) |
| Konkurrensverket | kunde inte mätas | – | – | – |
| Konstfack | bara EU/EES-nät före samtycke | – | – | – |
| Konstnärsnämnden | ingen tredjepart | – | – | – |
| Konsumentverket | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com, images.ctfassets.net | Google |
| Kriminalvården | US-nät före samtycke | – | cdn.matomo.cloud | InnoCraft (Matomo Cloud), ReadSpeaker |
| Kronofogdemyndigheten | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Kungliga biblioteket | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Kungliga konsthögskolan | US-nät före samtycke | – | hello.myfonts.net | Monotype |
| Kungliga musikhögskolan | US-nät före samtycke | – | w.soundcloud.com | – |
| Kungliga tekniska högskolan | ingen tredjepart | – | – | – |
| Kustbevakningen | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp |
| Lantmäteriet | ingen tredjepart | – | – | – |
| Linköpings universitet | ingen tredjepart | – | – | – |
| Linnéuniversitetet | US-nät före samtycke | ja | cdn-cookieyes.com, cdnjs.cloudflare.com, code.jquery.com, lnu.boost.ai, log.cookieyes.com, static.aim.front.ai, www.googletagmanager.com | Cloudflare, Google, Rek.ai, jQuery CDN |
| Livsmedelsverket | US-nät före samtycke | – | cdn.matomo.cloud, js.monitor.azure.com, swedencentral-0.in.applicationinsights.azure.com | InnoCraft (Matomo Cloud), Microsoft, ReadSpeaker |
| Luleå tekniska universitet | US-nät före samtycke | – | 7574.global.siteimproveanalytics.io, siteimproveanalytics.com | Piwik PRO, Siteimprove |
| Lunds universitet | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp |
| Läkemedelsverket | US-nät före samtycke | – | js.monitor.azure.com, northeurope-2.in.applicationinsights.azure.com | Microsoft, Vizzit, Web Service Award |
| lansstyrelsen.se (delas av 21 myndigheter) | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Malmö universitet | US-nät före samtycke | – | apiv2.imbox.io, cdn.botframework.com, customer.cludo.com, files.imbox.io, p.typekit.net, triggers-v3.imbox.io, use.typekit.net, widget-launcher.imbox.io, widget.imbox.io | Adobe, Cludo, Imbox |
| Mediemyndigheten | US-nät före samtycke | – | cdn.cookietractor.com, cdn.matomo.cloud, fast.fonts.net | InnoCraft (Matomo Cloud), Monotype |
| Medlingsinstitutet | bara EU/EES-nät före samtycke | – | – | – |
| Migrationsverket | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Mittuniversitetet | US-nät före samtycke | ja | cdn-cookieyes.com, clients1.google.com, cse.google.com, elfsightcdn.com, ep1.adtrafficquality.google, ep2.adtrafficquality.google, js.monitor.azure.com, log.cookieyes.com, pagead2.googlesyndication.com, swedencentral-0.in.applicationinsights.azure.com, www.google.com, www.googletagmanager.com | Google, Microsoft, Plausible Analytics, Rek.ai, Vizzit |
| Moderna museet | US-nät före samtycke | ja | region1.google-analytics.com, sentry.frojd.se, www.googletagmanager.com | Google |
| Myndigheten för civilt försvar | annat nät före samtycke | – | – | ReadSpeaker |
| Myndigheten för delaktighet | US-nät före samtycke | – | 6091227.global.siteimproveanalytics.io, dc.services.visualstudio.com, fonts.googleapis.com, fonts.gstatic.com, js.monitor.azure.com, policy.app.cookieinformation.com, siteimproveanalytics.com, www.youtube.com | Cookie Information, Google, Microsoft, ReadSpeaker, Siteimprove, Web Service Award |
| Myndigheten för digital förvaltning | ingen tredjepart | – | – | – |
| Myndigheten för familjerätt och föräldraskapsstöd | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Myndigheten för kulturanalys | US-nät före samtycke | – | cdn.matomo.cloud, fonts.googleapis.com, fonts.gstatic.com | Google, InnoCraft (Matomo Cloud) |
| Myndigheten för psykologiskt försvar | US-nät före samtycke | – | cdn.matomo.cloud, mpf.matomo.cloud | InnoCraft (Matomo Cloud), ReadSpeaker |
| Myndigheten för säkerhet och integritetsskydd | US-nät före samtycke | – | cdnjs.cloudflare.com, fonts.googleapis.com | Cloudflare, Google, ReadSpeaker |
| Myndigheten för tillgängliga medier | annat nät före samtycke | – | – | ReadSpeaker |
| Myndigheten för tillväxtpolitiska utvärderingar och analyser | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Myndigheten för totalförsvarsanalys | kunde inte mätas | – | – | – |
| Myndigheten för ungdoms-och civilsamhällesfrågor | ingen tredjepart | – | – | – |
| Myndigheten för vård- och omsorgsanalys | US-nät före samtycke | – | cdn.matomo.cloud, hello.myfonts.net, vardanalys.matomo.cloud | InnoCraft (Matomo Cloud), Monotype |
| Myndigheten för yrkeshögskolan | US-nät före samtycke | – | policy.app.cookieinformation.com | Cookie Information |
| Mälardalens universitet | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google, Piwik PRO, Rek.ai |
| Nationalmuseum | US-nät före samtycke | ja | cdnjs.cloudflare.com, cloud.typography.com, consent.cookiebot.com, consentcdn.cookiebot.com, p.typekit.net, use.typekit.net, www.googletagmanager.com | Adobe, Cloudflare, Google, Usercentrics (Cookiebot) |
| Naturhistoriska riksmuseet | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Naturvårdsverket | US-nät före samtycke | – | dc.services.visualstudio.com, dl.episerver.net, js.monitor.azure.com, p.typekit.net, policy.app.cookieinformation.com, use.typekit.net | Adobe, Cookie Information, Microsoft, Optimizely, Vizzit |
| Nordiska afrikainstitutet | US-nät före samtycke | – | p.typekit.net, use.typekit.net | Adobe |
| Nämnden för hemslöjdsfrågor | US-nät före samtycke | – | cdn.matomo.cloud, code.jquery.com, consent.cookiebot.com, consentcdn.cookiebot.com, dl.episerver.net, kulturradet.imagevault.app, plus.browsealoud.com, www.browsealoud.com, www.google.com, www.gstatic.com | Google, InnoCraft (Matomo Cloud), Optimizely, Texthelp, Usercentrics (Cookiebot), jQuery CDN |
| Nämnden för prövning av oredlighet i forskning | kunde inte mätas | – | – | – |
| Nämnden mot Diskriminering | US-nät före samtycke | – | app.termly.io | one.com |
| Oljekrisnämnden | kunde inte mätas | – | – | – |
| Patent- och registreringsverket | US-nät före samtycke | ja | cdn.cookietractor.com, netdna.bootstrapcdn.com, player.vimeo.com, prv.imagevault.media, www.googletagmanager.com | Google, Vimeo |
| Patentombudsnämnden | kunde inte mätas | – | – | – |
| Pensionsmyndigheten | ingen tredjepart | – | – | – |
| Polarforskningssekretariatet | US-nät före samtycke | ja | ajax.aspnetcdn.com, cdnjs.cloudflare.com, code.jquery.com, fonts.googleapis.com, fonts.gstatic.com, googleads.g.doubleclick.net, i.ytimg.com, region1.google-analytics.com, static.doubleclick.net, www.google.com, www.googletagmanager.com, www.youtube.com | Cloudflare, Google, jQuery CDN |
| Polismyndigheten | ingen tredjepart | – | – | – |
| Post- och telestyrelsen | ingen tredjepart | – | – | – |
| Revisorsinspektionen | US-nät före samtycke | – | dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com | Google, Optimizely |
| Riksantikvarieämbetet | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com, p.typekit.net, use.typekit.net | Adobe, Google |
| Riksarkivet | ingen tredjepart | – | – | – |
| Riksgäldskontoret | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Rymdstyrelsen | US-nät före samtycke | – | cdn.cookietractor.com, cdn.gtranslate.net, cdn.matomo.cloud | InnoCraft (Matomo Cloud) |
| Rättsmedicinalverket | US-nät före samtycke | ja | 7adcfd322329.w.hcaptcha.com, ajax.googleapis.com, cdnjs.cloudflare.com, js.hcaptcha.com, plus.browsealoud.com, www.browsealoud.com, www.googletagmanager.com | Cloudflare, Google, Texthelp |
| Sameskolstyrelsen | US-nät före samtycke | – | cdn-cookieyes.com, log.cookieyes.com | – |
| Sametinget | kunde inte mätas | – | – | – |
| Sida | US-nät före samtycke | – | api.openaid.se | Piwik PRO |
| Skatterättsnämnden | ingen tredjepart | – | – | – |
| Skatteverket | ingen tredjepart | – | – | – |
| Skogsstyrelsen | US-nät före samtycke | – | dl.episerver.net | Optimizely, Vizzit |
| Skolforskningsinstitutet | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp |
| Skolväsendets överklagandenämnd | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google, ReadSpeaker |
| Specialpedagogiska skolmyndigheten | US-nät före samtycke | – | cdn.cookietractor.com, dl.episerver.net, plus.browsealoud.com, www.browsealoud.com | Optimizely, Texthelp |
| Spelinspektionen | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google |
| Statens beredning för medicinsk och social utvärdering | US-nät före samtycke | ja | 20035.global.siteimproveanalytics.io, az416426.vo.msecnd.net, consent.cookiebot.com, consentcdn.cookiebot.com, dc.services.visualstudio.com, dl.episerver.net, fast.fonts.net, plus.browsealoud.com, siteimproveanalytics.com, www.browsealoud.com, www.googletagmanager.com | Google, Microsoft, Monotype, Optimizely, Siteimprove, Texthelp, Usercentrics (Cookiebot), Web Service Award |
| Statens energimyndighet | US-nät före samtycke | – | dc.services.visualstudio.com, dl.episerver.net, js.monitor.azure.com | Microsoft, Optimizely, ReadSpeaker |
| Statens fastighetsverk | US-nät före samtycke | – | p.typekit.net, use.typekit.net | Adobe |
| Statens geotekniska institut | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Usercentrics (Cookiebot), Vizzit |
| Statens haverikommission | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Statens historiska museer | US-nät före samtycke | ja | cdn.matomo.cloud, fonts.googleapis.com, fonts.gstatic.com, shm.matomo.cloud, www.googletagmanager.com | Google, InnoCraft (Matomo Cloud), ReadSpeaker |
| Statens inspektion för försvarsunderrättelseverksamheten (SIUN) | ingen tredjepart | – | – | – |
| Statens institutionsstyrelse | US-nät före samtycke | – | cdnjs.cloudflare.com, code.jquery.com, consent.cookiebot.com, consentcdn.cookiebot.com, fonts.googleapis.com, fonts.gstatic.com, js.monitor.azure.com, swedencentral-0.in.applicationinsights.azure.com | Cloudflare, Google, Microsoft, Usercentrics (Cookiebot), jQuery CDN |
| Statens kulturråd | US-nät före samtycke | – | cdn.matomo.cloud, code.jquery.com, consent.cookiebot.com, consentcdn.cookiebot.com, dl.episerver.net, kulturradet.imagevault.app, plus.browsealoud.com, www.browsealoud.com, www.google.com, www.gstatic.com | Google, InnoCraft (Matomo Cloud), Optimizely, Texthelp, Usercentrics (Cookiebot), jQuery CDN |
| Statens museer för maritim, transport- och försvarshistoria | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com, dl.episerver.net, fast.fonts.net, plus.browsealoud.com, www.browsealoud.com | Monotype, Optimizely, Texthelp, Usercentrics (Cookiebot) |
| Statens museer för världskultur | US-nät före samtycke | ja | ad.doubleclick.net, connect.facebook.net, dc.services.visualstudio.com, dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com, googleads.g.doubleclick.net, js.monitor.azure.com, region1.analytics.google.com, region1.google-analytics.com, stats.g.doubleclick.net, www.facebook.com, www.google.com, www.google.se, www.googleadservices.com, www.googletagmanager.com, xd-f1cf3d4fdb19408ea770fc6f80817dcb.ecs.us-east-1.on.aws | Google, Meta, Microsoft, Optimizely |
| Statens musikverk | US-nät före samtycke | – | ajax.googleapis.com, cdn.jsdelivr.net, use.typekit.net | Adobe, Google, ReadSpeaker, jsDelivr |
| Statens servicecenter | ingen tredjepart | – | – | – |
| Statens skolinspektion | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google, ReadSpeaker |
| Statens skolverk | ingen tredjepart | – | – | – |
| Statens tjänstepensions- och grupplivnämnd | ingen tredjepart | – | – | – |
| Statens veterinärmedicinska anstalt | US-nät före samtycke | ja | ajax.aspnetcdn.com, cdn.jsdelivr.net, cdnjs.cloudflare.com, fonts.gstatic.com, www.googletagmanager.com | Cloudflare, Google, Plausible Analytics, jsDelivr |
| Statens väg- och transportforskningsinstitut | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Statistiska centralbyrån | bara EU/EES-nät före samtycke | – | – | – |
| Statskontoret | ingen tredjepart | – | – | – |
| Stockholms konstnärliga högskola | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Usercentrics (Cookiebot) |
| Stockholms universitet | US-nät före samtycke | – | a.eu.silktide.com, analytics.silktide.com, cdn.matomo.cloud, su.matomo.cloud | InnoCraft (Matomo Cloud), Silktide |
| Strålsäkerhetsmyndigheten | US-nät före samtycke | – | code.jquery.com, dc.services.visualstudio.com, dl.episerver.net, fonts.gstatic.com, googleads.g.doubleclick.net, i.ytimg.com, js.monitor.azure.com, policy.app.cookieinformation.com, static.doubleclick.net, www.google.com, www.youtube.com | Cookie Information, Google, Microsoft, Optimizely, Piwik PRO, Web Service Award, jQuery CDN |
| Styrelsen för ackreditering och teknisk kontroll | US-nät före samtycke | – | cdn.jsdelivr.net | Rek.ai, jsDelivr |
| Svenska esf-rådet | US-nät före samtycke | – | fonts.googleapis.com, ka-p.fontawesome.com, kit.fontawesome.com, plus.browsealoud.com, www.browsealoud.com | Fonticons (Font Awesome), Google, Texthelp |
| Svenska institutet | US-nät före samtycke | ja | fonts.googleapis.com, fonts.gstatic.com, www.googletagmanager.com | Google |
| Svenska institutet för europapolitiska studier | US-nät före samtycke | – | f.vimeocdn.com, i.vimeocdn.com, player.vimeo.com, policy.app.cookieinformation.com | Cookie Information, Rek.ai, Vimeo |
| Sveriges författarfond | ingen tredjepart | – | – | – |
| Sveriges geologiska undersökning | US-nät före samtycke | – | dl.episerver.net, plus.browsealoud.com, www.browsealoud.com, www.google.com, www.gstatic.com | Google, Optimizely, Texthelp |
| Sveriges lantbruksuniversitet | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Sveriges meteorologiska och hydrologiska institut | US-nät före samtycke | – | cdn-cookieyes.com, log.cookieyes.com | – |
| Säkerhetspolisen | ingen tredjepart | – | – | – |
| Södertörns högskola | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Tandvårds-och läkemedelsförmånsverket, TLV | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Tillväxtverket | US-nät före samtycke | – | foq.youreurope.europa.eu | Vizzit |
| Totalförsvarets forskningsinstitut, foi | ingen tredjepart | – | – | – |
| Totalförsvarets plikt- och prövningsverk | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Trafikanalys | US-nät före samtycke | ja | dl.episerver.net, region-eu.cookiehub.net, region1.google-analytics.com, www.googletagmanager.com | Google, Optimizely, Rek.ai |
| Trafikverket | ingen tredjepart | – | – | – |
| Transportstyrelsen | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Tullverket | kunde inte mätas | – | – | – |
| Umeå universitet | bara EU/EES-nät före samtycke | – | – | – |
| Universitets- och högskolerådet | US-nät före samtycke | – | cdn.jsdelivr.net, dl.episerver.net | Optimizely, jsDelivr |
| Universitetskanslersämbetet | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Piwik PRO, Texthelp |
| Upphandlingsmyndigheten | US-nät före samtycke | ja | js.monitor.azure.com, policy.app.cookieinformation.com, region1.google-analytics.com, www.googletagmanager.com | Cookie Information, Google, Microsoft |
| Uppsala universitet | US-nät före samtycke | – | 8074.global.siteimproveanalytics.io, siteimproveanalytics.com | Rek.ai, Siteimprove |
| Utbetalningsmyndigheten | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Valmyndigheten | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Verket för innovationssystem | US-nät före samtycke | – | cdnjs.cloudflare.com, code.jquery.com, forms.apsisforms.com | Cloudflare, Rek.ai, jQuery CDN |
| Vetenskapsrådet | US-nät före samtycke | ja | www.googletagmanager.com | Google |
| Åklagarmyndigheten | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Örebro universitet | ingen tredjepart | – | – | – |
| Överklagandenämnden för etikprövning | US-nät före samtycke | – | fonts.googleapis.com | Google |
| Överklagandenämnden för högskolan | US-nät före samtycke | – | p.typekit.net, plus.browsealoud.com, use.typekit.net, www.browsealoud.com | Adobe, Piwik PRO, Texthelp |
| Överklagandenämnden för studiestöd | kunde inte mätas | – | – | – |
| riksdagen.se (delas av 2 myndigheter) | ingen tredjepart | – | – | – |
| Riksdagens ombudsmän | ingen tredjepart | – | – | – |
| Riksrevisionen | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Sveriges riksbank | US-nät före samtycke | – | js.monitor.azure.com, swedencentral-0.in.applicationinsights.azure.com | Microsoft, Vizzit |
| Luftfartsverket | US-nät före samtycke | – | dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com | Google, Optimizely |
| Sjöfartsverket | US-nät före samtycke | – | dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com | Google, Optimizely |
| Svenska kraftnät | US-nät före samtycke | – | js.monitor.azure.com, swedencentral-0.in.applicationinsights.azure.com | Microsoft |
