# Resultat — mätning 2: tredjeparter före samtycke

> **Granskning 2026-10-09 (issue #12):** mätningen registrerar anropsförsök i
> webbläsarens nätverkslogg, inte att kontakten lyckades. "Kontaktar" nedan
> ska läsas som "gjorde anrop till".

Regler: METOD.md, "Mätning 2". Klassning: `python3 webb_klassa.py <fil>`.

## Steg 1: Stockholm (utveckling) — 2026-10-08 16:11 UTC

`data/webb-organisationer-2026-10-08T161130Z.json`. Kontroller: tom sida gav
inga värdar, GA-sidan gav `www.googletagmanager.com`.

| Klass | Antal av 27 |
|---|---|
| US före samtycke | 11 |
| Bara EU/SE före samtycke | 13 |
| Ingen tredjepart | 3 |

Ingen laddade Google Analytics eller Tag Manager före samtycke. US-träffarna är
främst Google Fonts/Translate, Microsofts Application Insights och Optimizely.

## Steg 2: Skåne (hållout) — **kriteriet föll**

`data/webb-organisationer-skane-*.json`. 33 av 34 gick att mäta (krav 32);
Region Skåne svarar 403 på automatiska besök.

**30 av 59 unika tredjepartsvärdar (51 %) saknades i `leverantorer.csv`** (krav
högst 10 %). Listan var byggd på Stockholm och täckte inte leverantörer som är
vanliga i Skåne: Puzzel, Kundo, Cludo, Matomo Cloud, Silktide, Plausible,
Cruncho, Hoodin. Två av de "okända" är Helsingborgs egna andra domäner
(`helsingborg.io`, `api.helsingborg.se`), vilket regeln för första part inte
fångar (jfr issue #6).

Därför publiceras inga siffror per organisation för Skåne från den här körningen.

### En iakttagelse som kontrollerats separat

Hässleholm var den enda i Skåne där Google Analytics kontaktades före samtycke.
Det bekräftades i en vanlig Chrome med obesvarad cookiebanner:
`region1.analytics.google.com/g/collect` med `en=page_view`. Anropet har
parametern `gcd` som tyder på Googles Consent Mode, där "cookielösa" anrop
skickas före samtycke. IP-adress, webbläsare och sidadress följer ändå med.
Om det är förenligt med reglerna avgörs inte här.

## Nästa steg

Version 2 av leverantörslistan byggs med Stockholm och Skåne framför sig och
prövas på ett nytt hållout-län: Västra Götaland (50 organisationer).

## Steg 3: Västra Götaland (hållout v2) — **kriteriet föll igen**

`data/webb-organisationer-vgr-2026-10-08T161520Z.json`. 50 av 50 mätbara.
**16 av 58 unika tredjepartsvärdar (28 %) okända** (krav högst 10 %): bland
annat Usercentrics, Mediaflow, Boost.ai, Visitors Voice och en app på
`azurewebsites.net` (Microsoft, som listan alltså också missade).

**Slutsats efter två fall:** en handskriven leverantörslista hinner inte ikapp
den långa svansen av små leverantörer. Klassen "bara EU/SE före samtycke" kan
därför inte publiceras per organisation med den här metoden.

Det som håller oberoende av listan: en okänd värd kan bara flytta en
organisation *till* "US före samtycke", aldrig därifrån. "US före samtycke" och
"Google Analytics/GTM före samtycke" är därför nivåer som syns i den här mätningen, inte exakta tal.

## Steg 4: version 3, nätet bakom varje värd

**Falsifiering, alla uppfyllda:**

| Test | Krav | Utfall |
|---|---|---|
| Negativ kontroll | 0 värdar | 0 |
| Positiv kontroll | `www.googletagmanager.com` | hittad |
| Nätkontroll | Google = US, Hetzner = EU/EES | stämmer |
| Upprepning, Stockholm 16:11 och 16:21 UTC | ≥25/27 lika | 27/27 |
| Hållout Norrland (`data/webb-organisationer-norrland-2026-10-08T162106Z.json`) | ≥95 % värdar med ASN, ≥95 % mätbara | 99 %, 96 % |

## Hela Sverige — 2026-10-08 16:26 UTC

`data/webb-organisationer-sverige-2026-10-08T162614Z.json`. Rättelse v3 (landskoden `EU`, startsida utan `www`) tillämpad, se
METOD.md. Den första nationella körningen 16:22 behålls i `data/`.

| | Antal | Andel av mätbara |
|---|---|---|
| Kontaktar amerikanska nät före samtycke | 164 | 54 % |
| Kontaktar Google Analytics/Tag Manager före samtycke | 16 | 5 % |
| Kontaktar bara EU/EES-nät | 90 | 29 % |
| Annat nät (främst CDN77, Storbritannien) | 30 | 10 % |
| Ingen tredjepart | 20 | 7 % |
| Okänt nät | 2 | |
| Kunde inte mätas | 4 | |

306 av 310 gick att mäta; 244 av 248 unika tredjepartsvärdar fick ett ASN.

**Vanligast på amerikanska nät:** Google (Fonts, Translate, Analytics),
Texthelps uppläsningstjänst BrowseAloud (Amazon CloudFront), Microsoft
(Application Insights), Cloudflare och Font Awesome.

**Google Analytics/Tag Manager före samtycke:** Valdemarsvik, Jönköping, Emmaboda, Oskarshamn, Borgholm, Sölvesborg, Hässleholm, Dals-Ed, Färgelanda, Mellerud, Vänersborg, Åmål, Sunne, Norsjö, Storuman, Pajala.
Stickprov i vanlig Chrome bekräftade Hässleholm. Flera av dessa kan använda
Googles Consent Mode, där anrop utan kakor skickas före samtycke; IP-adress,
webbläsare och sidadress följer ändå med.

**Nätet är inte databasen.** BrowseAloud nås via Amazon CloudFront, ett CDN med
servrar över hela världen; besökaren svarar troligen en server i Europa. Var
tjänstens egna servrar och databaser står syns inte utifrån. "Amerikanskt nät"
betyder att anropet hanteras av ett amerikanskt bolags infrastruktur.

### Per län

| Län | US-nät | Annat nät | Bara EU/EES | Ingen tredjepart | Okänt nät | Kunde inte mätas |
|---|---|---|---|---|---|---|
| Blekinge län | 4 | 0 | 2 | 0 | 0 | 0 |
| Dalarnas län | 9 | 4 | 3 | 0 | 0 | 0 |
| Gotlands län | 0 | 1 | 0 | 0 | 0 | 0 |
| Gävleborgs län | 2 | 2 | 6 | 1 | 0 | 0 |
| Hallands län | 2 | 1 | 4 | 0 | 0 | 0 |
| Jämtlands län | 3 | 0 | 5 | 1 | 0 | 0 |
| Jönköpings län | 5 | 2 | 7 | 0 | 0 | 0 |
| Kalmar län | 10 | 1 | 1 | 0 | 0 | 1 |
| Kronobergs län | 7 | 1 | 1 | 0 | 0 | 0 |
| Norrbottens län | 8 | 1 | 2 | 2 | 0 | 2 |
| Skåne län | 16 | 4 | 8 | 5 | 0 | 1 |
| Stockholms län | 13 | 2 | 8 | 3 | 1 | 0 |
| Södermanlands län | 3 | 0 | 5 | 2 | 0 | 0 |
| Uppsala län | 6 | 2 | 1 | 0 | 0 | 0 |
| Värmlands län | 13 | 0 | 3 | 1 | 0 | 0 |
| Västerbottens län | 12 | 1 | 1 | 1 | 1 | 0 |
| Västernorrlands län | 5 | 0 | 2 | 1 | 0 | 0 |
| Västmanlands län | 7 | 2 | 2 | 0 | 0 | 0 |
| Västra Götalands län | 22 | 3 | 22 | 3 | 0 | 0 |
| Örebro län | 8 | 2 | 3 | 0 | 0 | 0 |
| Östergötlands län | 9 | 1 | 4 | 0 | 0 | 0 |

### Alla organisationer

| Organisation | Klass (v3) | Google Analytics/GTM | Värdar på US-nät | Leverantörer (där kända) |
|---|---|---|---|---|
| Upplands Väsby | ingen tredjepart | – | – | – |
| Vallentuna | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Österåker | annat nät före samtycke | – | – | ReadSpeaker, Rek.ai, Vizzit |
| Värmdö | US-nät före samtycke | – | unpkg.com | Piwik PRO, Rek.ai, unpkg |
| Järfälla | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Ekerö | US-nät före samtycke | – | fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Google, Piwik PRO |
| Huddinge | ingen tredjepart | – | – | – |
| Botkyrka | US-nät före samtycke | – | eur01.safelinks.protection.outlook.com, plus.browsealoud.com, www.browsealoud.com | Microsoft, Piwik PRO, Rek.ai, Tele2 (Artvise), Texthelp, Web Service Award |
| Salem | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google, Piwik PRO, ReadSpeaker, Rek.ai |
| Haninge | US-nät före samtycke | – | dc.services.visualstudio.com, dl.episerver.net, js.monitor.azure.com, www.browsealoud.com | Microsoft, Optimizely, Rek.ai, Texthelp, consentmanager |
| Tyresö | US-nät före samtycke | – | chat2.zisson.se, hello.myfonts.net, skravle.zisson.se | Monotype, ReadSpeaker, Rek.ai, Vizzit, Zisson |
| Upplands-Bro | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai, Tele2 (Artvise) |
| Nykvarn | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Täby | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Danderyd | US-nät före samtycke | – | cdn.jsdelivr.net, cdnjs.cloudflare.com, code.jquery.com, dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Cloudflare, Google, Optimizely, Vizzit, Web Service Award, jQuery CDN, jsDelivr |
| Sollentuna | US-nät före samtycke | – | apiv2.imbox.io, dc.services.visualstudio.com, dl.episerver.net, files.imbox.io, fonts.googleapis.com, js.monitor.azure.com, triggers-v3.imbox.io, widget-launcher.imbox.io, widget.imbox.io | Google, Imbox, Microsoft, Optimizely, Rek.ai, Vizzit |
| Stockholm | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Södertälje | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com, digitalfeedback.euro.confirmit.com, fonts.googleapis.com, fonts.gstatic.com | Forsta (Confirmit), Google, Insipio, Rek.ai, Usercentrics (Cookiebot) |
| Nacka | US-nät före samtycke | – | az416426.vo.msecnd.net, dc.services.visualstudio.com, dl.episerver.net | Microsoft, Optimizely, Rek.ai, Vizzit |
| Sundbyberg | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Web Service Award |
| Solna | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai, Vizzit |
| Lidingö | US-nät före samtycke | – | 7553.global.siteimproveanalytics.io, siteimproveanalytics.com | Rek.ai, Siteimprove |
| Vaxholm | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Norrtälje | US-nät före samtycke | – | app-script.monsido.com, dl.episerver.net, fast.fonts.net, heatmaps.monsido.com, policy.app.cookieinformation.com, tracking.monsido.com | Cookie Information, Monotype, Monsido, Optimizely, Vizzit |
| Sigtuna | US-nät före samtycke | – | s3-bestevent-prod.innocode.dev | Innocode, Piwik PRO, Rek.ai |
| Nynäshamn | okänt nät | – | – | Piwik PRO, Rek.ai, Sitevision, Vizzit |
| Håbo | US-nät före samtycke | – | fonts.gstatic.com, maxcdn.bootstrapcdn.com, se1.siteimprove.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Google, Siteimprove, Vizzit |
| Älvkarleby | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai |
| Knivsta | US-nät före samtycke | – | digitalfeedback.euro.confirmit.com, fonts.gstatic.com, plus.browsealoud.com, translate.google.com, translate.googleapis.com, www.browsealoud.com, www.gstatic.com | Forsta (Confirmit), Google, Piwik PRO, Rek.ai, Texthelp, Vizzit |
| Heby | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Tierp | annat nät före samtycke | – | – | Vizzit |
| Uppsala | US-nät före samtycke | – | cdn.jsdelivr.net | jsDelivr |
| Enköping | US-nät före samtycke | – | ajax.googleapis.com, fonts.googleapis.com, fonts.gstatic.com, maxcdn.bootstrapcdn.com, p.typekit.net, use.typekit.net | Adobe, Google, ReadSpeaker |
| Östhammar | US-nät före samtycke | – | service2.mtcaptcha.com | ReadSpeaker, Rek.ai, Vizzit |
| Vingåker | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Gnesta | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Nyköping | US-nät före samtycke | – | dc.services.visualstudio.com, fonts.googleapis.com, fonts.gstatic.com, js.monitor.azure.com | Google, Microsoft |
| Oxelösund | US-nät före samtycke | – | chimpstatic.com, eventcollector.mcf-prod.a.intuit.com, form-assets.mailchimp.com | Piwik PRO, Rek.ai |
| Flen | US-nät före samtycke | – | chat.kundo.se, org-1339.chat.kundo.se, static-chat.kundo.se | Kundo, Piwik PRO, ReadSpeaker |
| Katrineholm | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Eskilstuna | ingen tredjepart | – | – | – |
| Strängnäs | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Trosa | ingen tredjepart | – | – | – |
| Ödeshög | US-nät före samtycke | – | cdn.cookie-script.com | Vizzit |
| Ydre | US-nät före samtycke | – | cdn.cookie-script.com | Piwik PRO |
| Kinda | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai |
| Boxholm | US-nät före samtycke | – | cdn.cookie-script.com | Piwik PRO |
| Åtvidaberg | US-nät före samtycke | – | cdn.cookie-script.com | Piwik PRO |
| Finspång | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Valdemarsvik | US-nät före samtycke | ja | ajax.googleapis.com, cdnjs.cloudflare.com, d1azc1qln24ryf.cloudfront.net, fonts.googleapis.com, fonts.gstatic.com, helsingborg-stad.github.io, instant.page, region1.google-analytics.com, translate.google.com, translate.googleapis.com, www.google-analytics.com, www.google.com, www.googletagmanager.com, www.gstatic.com | Cloudflare, Google, ReadSpeaker |
| Linköping | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai, Web Service Award |
| Norrköping | US-nät före samtycke | – | 7674.global.siteimproveanalytics.io, ka-p.fontawesome.com, kit.fontawesome.com, siteimproveanalytics.com | Fonticons (Font Awesome), Siteimprove |
| Söderköping | US-nät före samtycke | – | ajax.googleapis.com, customer.cludo.com, maps.googleapis.com, scontent-arn2-1.xx.fbcdn.net, scontent.xx.fbcdn.net, static.xx.fbcdn.net, www.facebook.com | Cludo, Google, Meta, Vizzit, consentmanager |
| Motala | US-nät före samtycke | – | cdnjs.cloudflare.com, fonts.googleapis.com, fonts.gstatic.com, maxcdn.bootstrapcdn.com, policy.app.cookieinformation.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Cloudflare, Cookie Information, Google, Piwik PRO, Rek.ai |
| Vadstena | US-nät före samtycke | – | digitalfeedback.euro.confirmit.com | Forsta (Confirmit), ReadSpeaker |
| Mjölby | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Aneby | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Gnosjö | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Mullsjö | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Piwik PRO, Texthelp, Vizzit |
| Habo | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Gislaved | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Vaggeryd | US-nät före samtycke | – | 8085.global.siteimproveanalytics.io, connect.facebook.net, siteimproveanalytics.com | Meta, Piwik PRO, Rek.ai, Siteimprove |
| Jönköping | US-nät före samtycke | ja | cdn.kiprotect.com, www.googletagmanager.com | Google, Rek.ai |
| Nässjö | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai |
| Värnamo | US-nät före samtycke | – | api-ts.cruncho.co, cdnjs.cloudflare.com, varnamo.cruncho.co | Cloudflare, Cruncho, Vizzit |
| Sävsjö | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai |
| Vetlanda | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Eksjö | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Tranås | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Uppvidinge | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google, Piwik PRO, ReadSpeaker, Rek.ai |
| Lessebo | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai |
| Tingsryd | US-nät före samtycke | – | cdn.matomo.cloud, tingsryd.matomo.cloud | InnoCraft (Matomo Cloud) |
| Alvesta | US-nät före samtycke | – | cdnjs.cloudflare.com, fonts.googleapis.com, fonts.gstatic.com, kit.fontawesome.com, plus.browsealoud.com, www.browsealoud.com | Cloudflare, Fonticons (Font Awesome), Google, Texthelp |
| Älmhult | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai, Vizzit |
| Markaryd | US-nät före samtycke | – | fonts.gstatic.com, kenwheeler.github.io, plus.browsealoud.com, translate.google.com, translate.googleapis.com, www.browsealoud.com, www.gstatic.com | Google, Sitevision, Texthelp, Vizzit |
| Växjö | US-nät före samtycke | – | fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Google, Piwik PRO, Rek.ai |
| Ljungby | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Rek.ai, Texthelp |
| Högsby | kunde inte mätas | – | – | – |
| Torsås | US-nät före samtycke | – | use.fontawesome.com | Fonticons (Font Awesome) |
| Mörbylånga | US-nät före samtycke | – | cdn.jsdelivr.net, cdn.matomo.cloud, cdnjs.cloudflare.com, consent.cookiebot.com, consentcdn.cookiebot.com, fonts.gstatic.com, p.typekit.net, translate.google.com, translate.googleapis.com, use.typekit.net, www.gstatic.com | Adobe, Cloudflare, Google, InnoCraft (Matomo Cloud), ReadSpeaker, Usercentrics (Cookiebot), jsDelivr |
| Hultsfred | US-nät före samtycke | – | api-iam.intercom.io, js.intercomcdn.com, maps.google.com, maps.googleapis.com, res.cdn.office.net, widget.intercom.io | Google, Rek.ai |
| Mönsterås | US-nät före samtycke | – | ajax.googleapis.com, fonts.googleapis.com, fonts.gstatic.com, p.typekit.net, unpkg.com, use.fontawesome.com, use.typekit.net | Adobe, Fonticons (Font Awesome), Google, ReadSpeaker, unpkg |
| Emmaboda | US-nät före samtycke | ja | plus.browsealoud.com, region1.google-analytics.com, www.browsealoud.com, www.googletagmanager.com | Google, Rek.ai, Texthelp |
| Kalmar | US-nät före samtycke | – | cdn.raffle.ai, fonts.googleapis.com, fonts.gstatic.com, plus.browsealoud.com, searchcfg.raffle.ai, www.browsealoud.com | Google, Piwik PRO, Texthelp, Vizzit |
| Nybro | US-nät före samtycke | – | ajax.googleapis.com | Google |
| Oskarshamn | US-nät före samtycke | ja | api.rechanneld.com, dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com, widget.rechanneld.com, www.googletagmanager.com | Google, Optimizely, Vizzit, Web Service Award |
| Västervik | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Vimmerby | US-nät före samtycke | – | cdn.cookie-script.com | Rek.ai |
| Borgholm | US-nät före samtycke | ja | borgholmdevdev.wpenginepowered.com, cdn.cookie-script.com, cdnjs.cloudflare.com, fonts.gstatic.com, p.typekit.net, region1.google-analytics.com, translate.google.com, translate.googleapis.com, use.typekit.net, www.googletagmanager.com, www.gstatic.com | Adobe, Cloudflare, Google, ReadSpeaker, Rek.ai, Vizzit |
| Gotland | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai |
| Olofström | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Piwik PRO, Rek.ai, Texthelp |
| Karlskrona | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Ronneby | US-nät före samtycke | – | 7800.global.siteimproveanalytics.io, fonts.googleapis.com, fonts.gstatic.com, maps.googleapis.com, siteimproveanalytics.com, translate.google.com, translate.googleapis.com, www.google.com, www.gstatic.com | Google, Rek.ai, Siteimprove |
| Karlshamn | US-nät före samtycke | – | cdnjs.cloudflare.com, consent.cookiebot.com, consentcdn.cookiebot.com, plus.browsealoud.com, www.browsealoud.com | Cloudflare, Texthelp, Usercentrics (Cookiebot) |
| Sölvesborg | US-nät före samtycke | ja | fonts.googleapis.com, fonts.gstatic.com, policy.app.cookieinformation.com, translate.google.com, translate.googleapis.com, www.googletagmanager.com, www.gstatic.com | Cookie Information, Google, Vizzit |
| Svalöv | US-nät före samtycke | – | fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.google.com, www.gstatic.com | Google, Rek.ai, Vizzit |
| Staffanstorp | US-nät före samtycke | – | s3.cruncho.co | Cruncho |
| Burlöv | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com, use.fontawesome.com | Fonticons (Font Awesome), Google, Piwik PRO, Vizzit |
| Vellinge | US-nät före samtycke | – | cdn.jsdelivr.net, cdn.matomo.cloud, s3.cruncho.co, vellinge.cruncho.co, vellinge.matomo.cloud | Cruncho, InnoCraft (Matomo Cloud), Puzzel, jsDelivr |
| Östra Göinge | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Örkelljunga | US-nät före samtycke | – | api.helsingborg.se | Helsingborgs stad, Rek.ai |
| Bjuv | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Kävlinge | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Lomma | annat nät före samtycke | – | – | Plausible Analytics, Rek.ai |
| Svedala | US-nät före samtycke | – | ajax.googleapis.com, fonts.googleapis.com, fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Google, one.com |
| Skurup | US-nät före samtycke | – | chat.kundo.se, fonts.googleapis.com, fonts.gstatic.com, org-1780.chat.kundo.se, plus.browsealoud.com, static-chat.kundo.se, www.browsealoud.com | Google, Kundo, Piwik PRO, Texthelp |
| Sjöbo | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google, ReadSpeaker, Rek.ai, Vizzit |
| Hörby | bara EU/EES-nät före samtycke | – | – | Puzzel |
| Höör | bara EU/EES-nät före samtycke | – | – | – |
| Tomelilla | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Bromölla | US-nät före samtycke | – | connect.facebook.net, consent.cookiebot.com, consentcdn.cookiebot.com, images.citybreak.com, plus.browsealoud.com, scontent.xx.fbcdn.net, static.xx.fbcdn.net, translate.google.com, www.browsealoud.com, www.facebook.com | Citybreak (Visit Group), Google, Meta, Texthelp, Usercentrics (Cookiebot), Vizzit |
| Osby | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai |
| Perstorp | US-nät före samtycke | – | cdn.jsdelivr.net, perstorp.cruncho.co, plus.browsealoud.com, s3.cruncho.co, www.browsealoud.com | Cruncho, Rek.ai, Texthelp, jsDelivr |
| Klippan | US-nät före samtycke | – | api.cludo.com, customer.cludo.com, fonts.googleapis.com, fonts.gstatic.com | Cludo, Google, Piwik PRO, ReadSpeaker, Rek.ai |
| Åstorp | annat nät före samtycke | – | – | ReadSpeaker, Rek.ai, Vizzit |
| Båstad | US-nät före samtycke | – | bastadweb.matomo.cloud, cdn.matomo.cloud | InnoCraft (Matomo Cloud), Rek.ai |
| Malmö | ingen tredjepart | – | – | – |
| Lund | US-nät före samtycke | – | a.eu.silktide.com, analytics.silktide.com, api.cludo.com, customer.cludo.com, eventmanager-assets152928-production.fra1.cdn.digitaloceanspaces.com, fonts.googleapis.com, s3.cruncho.co | Cludo, Cruncho, DigitalOcean, Google, Silktide |
| Landskrona | ingen tredjepart | – | – | – |
| Helsingborg | bara EU/EES-nät före samtycke | – | – | Puzzel |
| Höganäs | annat nät före samtycke | – | – | ReadSpeaker, Rek.ai, Vizzit, Web Service Award |
| Eslöv | ingen tredjepart | – | – | – |
| Ystad | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Trelleborg | ingen tredjepart | – | – | – |
| Kristianstad | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Piwik PRO, Rek.ai, Usercentrics (Cookiebot) |
| Simrishamn | ingen tredjepart | – | – | – |
| Ängelholm | US-nät före samtycke | – | euwa.puzzel.com, fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Google, Piwik PRO, Puzzel |
| Hässleholm | US-nät före samtycke | ja | cdn.hoodin.com, region1.analytics.google.com, stats.g.doubleclick.net, www.google.se, www.googletagmanager.com | Google, Hoodin, Piwik PRO, Puzzel, ReadSpeaker, Rek.ai |
| Hylte | US-nät före samtycke | – | s3-bestevent-prod.innocode.dev | Innocode, Piwik PRO, ReadSpeaker, Rek.ai |
| Halmstad | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai, Vizzit |
| Laholm | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Falkenberg | US-nät före samtycke | – | cdnjs.cloudflare.com, code.jquery.com, connect.facebook.net, fonts.googleapis.com, fonts.gstatic.com | Cloudflare, Google, Meta, jQuery CDN |
| Varberg | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Kungsbacka | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Härryda | US-nät före samtycke | – | 974se.boost.ai | Insipio, Piwik PRO, Rek.ai, Vizzit |
| Partille | ingen tredjepart | – | – | – |
| Öckerö | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Stenungsund | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Rek.ai, Usercentrics (Cookiebot) |
| Tjörn | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Google, Piwik PRO, ReadSpeaker, Rek.ai, Vizzit |
| Orust | ingen tredjepart | – | – | – |
| Sotenäs | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Munkedal | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Tanum | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Rek.ai, Texthelp, Vizzit |
| Dals-Ed | US-nät före samtycke | ja | fonts.googleapis.com, region1.google-analytics.com, translate.google.com, translate.googleapis.com, www.googletagmanager.com, www.gstatic.com | Google |
| Färgelanda | US-nät före samtycke | ja | region1.google-analytics.com, translate.google.com, translate.googleapis.com, www.googletagmanager.com, www.gstatic.com | Google |
| Ale | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Vizzit |
| Lerum | US-nät före samtycke | – | s3-bestevent-prod.innocode.dev | Innocode, Piwik PRO, Rek.ai, Vizzit |
| Vårgårda | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Bollebygd | annat nät före samtycke | – | – | ReadSpeaker, Vizzit |
| Grästorp | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Essunga | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Piwik PRO, Texthelp |
| Karlsborg | US-nät före samtycke | – | p.typekit.net, use.typekit.net | Adobe, Rek.ai, Vizzit, Web Service Award |
| Gullspång | ingen tredjepart | – | – | – |
| Tranemo | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Bengtsfors | annat nät före samtycke | – | – | ReadSpeaker |
| Mellerud | US-nät före samtycke | ja | region1.google-analytics.com, translate.google.com, translate.googleapis.com, www.googletagmanager.com, www.gstatic.com | Google |
| Lilla Edet | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Mark | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Svenljunga | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Herrljunga | US-nät före samtycke | – | fonts.googleapis.com | Google |
| Vara | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Götene | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Tibro | US-nät före samtycke | – | apiv2.imbox.io, files.imbox.io, p.typekit.net, triggers-v3.imbox.io, use.typekit.net, widget-launcher.imbox.io, widget.imbox.io | Adobe, Imbox, Rek.ai, Vizzit |
| Töreboda | US-nät före samtycke | – | www.google.com, www.gstatic.com | Google, Piwik PRO |
| Göteborg | US-nät före samtycke | – | api.cludo.com, customer.cludo.com | Cludo, Rek.ai |
| Mölndal | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai, Vizzit |
| Kungälv | US-nät före samtycke | – | ajax.googleapis.com, cdnjs.cloudflare.com, dc.services.visualstudio.com, dl.episerver.net, js.monitor.azure.com, plus.browsealoud.com, policy.app.cookieinformation.com, use.fontawesome.com, www.browsealoud.com | Cloudflare, Cookie Information, Fonticons (Font Awesome), Google, Microsoft, Optimizely, Texthelp |
| Lysekil | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Uddevalla | US-nät före samtycke | – | cdnjs.cloudflare.com | Cloudflare, ReadSpeaker, Rek.ai, Vizzit |
| Strömstad | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Vänersborg | US-nät före samtycke | ja | www.googletagmanager.com | Google, Piwik PRO |
| Trollhättan | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Alingsås | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Borås | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Ulricehamn | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Åmål | US-nät före samtycke | ja | plus.browsealoud.com, region1.google-analytics.com, www.browsealoud.com, www.googletagmanager.com | Google, Texthelp |
| Mariestad | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Lidköping | US-nät före samtycke | – | fonts.googleapis.com, ka-p.fontawesome.com, kit.fontawesome.com | Fonticons (Font Awesome), Google, Piwik PRO |
| Skara | US-nät före samtycke | – | app-frontend-qh2ihd35f2je6.azurewebsites.net | Rek.ai, Vizzit |
| Skövde | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Usercentrics (Cookiebot) |
| Hjo | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Tidaholm | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Falköping | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Kil | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Eda | US-nät före samtycke | – | cdn.cookie-script.com, cdnjs.cloudflare.com, maxcdn.bootstrapcdn.com, stackpath.bootstrapcdn.com, translate.google.com, www.google.com | Cloudflare, Google, ReadSpeaker |
| Torsby | US-nät före samtycke | – | url41.mailanyone.net | Piwik PRO, ReadSpeaker, Rek.ai, Web Service Award |
| Storfors | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp |
| Hammarö | US-nät före samtycke | – | ace-knowledge-cdn.teliacompany.net, forshagakommun.humany.net, hammarokommun.humany.net, img.turid.visitvarmland.com | Piwik PRO, Rek.ai |
| Munkfors | US-nät före samtycke | – | cdn.cookie-script.com, consent.cookie-script.com | ReadSpeaker |
| Forshaga | US-nät före samtycke | – | ace-knowledge-cdn.teliacompany.net, forshagakommun.humany.net | Piwik PRO |
| Grums | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp, Vizzit |
| Årjäng | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Piwik PRO, ReadSpeaker, Texthelp |
| Sunne | US-nät före samtycke | ja | cdn.cookietractor.com, download-video-ak.vimeocdn.com, js.monitor.azure.com, player.vimeo.com, swedencentral-0.in.applicationinsights.azure.com, www.googletagmanager.com | Google, Microsoft, Rek.ai, Vimeo |
| Karlstad | US-nät före samtycke | – | img.turid.visitvarmland.com, karlstad.imagevault.app, turid.visitvarmland.com | Piwik PRO, Rek.ai |
| Kristinehamn | US-nät före samtycke | – | dc.services.visualstudio.com, dl.episerver.net, js.monitor.azure.com, unpkg.com | Microsoft, Optimizely, Vizzit, unpkg |
| Filipstad | ingen tredjepart | – | – | – |
| Hagfors | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Arvika | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Vizzit |
| Säffle | US-nät före samtycke | – | chat.kundo.se, org-1383.chat.kundo.se, static-chat.kundo.se | Kundo, Piwik PRO |
| Lekeberg | US-nät före samtycke | – | ajax.googleapis.com, fast.fonts.net, fonts.googleapis.com, plus.browsealoud.com, pro.fontawesome.com, www.browsealoud.com | Fonticons (Font Awesome), Google, Monotype, Piwik PRO, Rek.ai, Texthelp |
| Laxå | US-nät före samtycke | – | ajax.googleapis.com, cdnjs.cloudflare.com, fonts.googleapis.com, fonts.gstatic.com, googleads.g.doubleclick.net, i.ytimg.com, static.doubleclick.net, www.google.com, www.youtube.com, youtube.com | Cloudflare, Google, Piwik PRO |
| Hallsberg | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Piwik PRO, Texthelp |
| Degerfors | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com, translate.google.com, translate.googleapis.com, www.google.com, www.gstatic.com | Google, ReadSpeaker |
| Hällefors | US-nät före samtycke | – | c.ba.contentsquare.net, t.contentsquare.net | Piwik PRO |
| Ljusnarsberg | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Örebro | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Kumla | US-nät före samtycke | – | ace-knowledge-cdn.teliacompany.net, askersund.humany.net, kumla.humany.net | – |
| Askersund | US-nät före samtycke | – | acsbapp.com, cdn.acsbapp.com, plus.browsealoud.com, www.browsealoud.com | Piwik PRO, Texthelp |
| Karlskoga | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Nora | bara EU/EES-nät före samtycke | – | – | – |
| Lindesberg | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Skinnskatteberg | US-nät före samtycke | – | ajax.googleapis.com, cdnjs.cloudflare.com, fonts.googleapis.com, fonts.gstatic.com, maps.googleapis.com, meet.jit.si, use.fontawesome.com, www.google.com, www.gstatic.com | Cloudflare, Fonticons (Font Awesome), Google |
| Surahammar | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google, ReadSpeaker, Vizzit |
| Kungsör | annat nät före samtycke | – | – | ReadSpeaker, Vizzit |
| Hallstahammar | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Norberg | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com, plus.browsealoud.com, translate.google.com, translate.googleapis.com, www.browsealoud.com, www.gstatic.com | Google, Piwik PRO, Texthelp |
| Västerås | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Sala | annat nät före samtycke | – | – | ReadSpeaker |
| Fagersta | US-nät före samtycke | – | fonts.gstatic.com, www.google.com, www.gstatic.com | Google, Piwik PRO, ReadSpeaker, Rek.ai |
| Köping | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google, ReadSpeaker, Vizzit |
| Arboga | US-nät före samtycke | – | fonts.googleapis.com | Google, ReadSpeaker, Vizzit |
| Vansbro | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Piwik PRO, Texthelp |
| Malung-Sälen | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai, Vizzit |
| Gagnef | US-nät före samtycke | – | ajax.googleapis.com, analytics3.wpmudev.com, cdn.selma.se, images.citybreak.com, ka-f.fontawesome.com, kit.fontawesome.com | Citybreak (Visit Group), Fonticons (Font Awesome), Google, Rek.ai |
| Leksand | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Rättvik | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Orsa | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Älvdalen | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Smedjebacken | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Rek.ai, Texthelp |
| Mora | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker, Rek.ai |
| Falun | bara EU/EES-nät före samtycke | – | – | ReadSpeaker |
| Borlänge | US-nät före samtycke | – | 7145.global.siteimproveanalytics.io, cdnjs.cloudflare.com, code.jquery.com, images.citybreak.com, plus.browsealoud.com, siteimproveanalytics.com, www.browsealoud.com | Citybreak (Visit Group), Cloudflare, Siteimprove, Texthelp, jQuery CDN |
| Säter | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp |
| Hedemora | US-nät före samtycke | – | cdn.matomo.cloud, panang.matomo.cloud | InnoCraft (Matomo Cloud) |
| Avesta | US-nät före samtycke | – | api.cludo.com, consent.cookiebot.com, consentcdn.cookiebot.com, customer.cludo.com, fonts.googleapis.com, fonts.gstatic.com, images.citybreak.com, plus.browsealoud.com, www.browsealoud.com | Citybreak (Visit Group), Cludo, Google, Texthelp, Usercentrics (Cookiebot) |
| Ludvika | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Rek.ai, Texthelp, Vizzit |
| Ockelbo | annat nät före samtycke | – | – | Piwik PRO, ReadSpeaker |
| Hofors | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Vizzit |
| Ovanåker | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Nordanstig | annat nät före samtycke | – | – | ReadSpeaker, Rek.ai, Vizzit |
| Ljusdal | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Gävle | ingen tredjepart | – | – | – |
| Sandviken | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Söderhamn | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp, Vizzit |
| Bollnäs | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Hudiksvall | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Vizzit |
| Ånge | US-nät före samtycke | – | scontent-arn2-1.cdninstagram.com | ReadSpeaker, Vizzit |
| Timrå | US-nät före samtycke | – | 8042.global.siteimproveanalytics.io, ajax.googleapis.com, fonts.googleapis.com, fonts.gstatic.com, siteimproveanalytics.com | Google, Piwik PRO, Siteimprove |
| Härnösand | US-nät före samtycke | – | plus.browsealoud.com, se.sms-service.dk, www.browsealoud.com | Piwik PRO, Rek.ai, Texthelp, Vizzit |
| Sundsvall | ingen tredjepart | – | – | – |
| Kramfors | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Sollefteå | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Örnsköldsvik | US-nät före samtycke | – | e.clarity.ms, scripts.clarity.ms, www.clarity.ms | Microsoft, Piwik PRO |
| Ragunda | ingen tredjepart | – | – | – |
| Bräcke | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Krokom | bara EU/EES-nät före samtycke | – | – | Piwik PRO, Rek.ai |
| Strömsund | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com, www.klart.se | Google, ReadSpeaker, Vizzit |
| Åre | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Berg | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Rek.ai, Texthelp, Vizzit |
| Härjedalen | US-nät före samtycke | – | acsbapp.com, cdn.acsbapp.com | ReadSpeaker, Vizzit |
| Östersund | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Nordmaling | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp |
| Bjurholm | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Texthelp |
| Vindeln | ingen tredjepart | – | – | – |
| Robertsfors | okänt nät | – | – | – |
| Norsjö | US-nät före samtycke | ja | app.talkie.se, avatar.assets.talkie.se, cdn.socket.io, chat-widget-icon.assets.talkie.se, fonts.googleapis.com, js.widget.talkie.se, p.typekit.net, plus.browsealoud.com, use.typekit.net, widget.assets.talkie.se, www.browsealoud.com, www.google-analytics.com, www.googletagmanager.com | Adobe, Google, Texthelp |
| Malå | US-nät före samtycke | – | ajax.googleapis.com, cdn-cookieyes.com, cdn.gtranslate.net, log.cookieyes.com, use.fontawesome.com | Fonticons (Font Awesome), Google |
| Storuman | US-nät före samtycke | ja | fonts.googleapis.com, fonts.gstatic.com, use.fontawesome.com, www.google-analytics.com | Fonticons (Font Awesome), Google |
| Sorsele | US-nät före samtycke | – | www.youtube.com | Google |
| Dorotea | US-nät före samtycke | – | js.monitor.azure.com, swedencentral-0.in.applicationinsights.azure.com | Microsoft |
| Vännäs | US-nät före samtycke | – | plus.browsealoud.com, www.browsealoud.com | Rek.ai, Texthelp |
| Vilhelmina | US-nät före samtycke | – | cdn.matomo.cloud, js.monitor.azure.com, northeurope-2.in.applicationinsights.azure.com, plus.browsealoud.com, vilhelmina.matomo.cloud, www.browsealoud.com | InnoCraft (Matomo Cloud), Microsoft, Texthelp |
| Åsele | US-nät före samtycke | – | js.monitor.azure.com, swedencentral-0.in.applicationinsights.azure.com | Microsoft |
| Umeå | bara EU/EES-nät före samtycke | – | – | Insipio, Vizzit |
| Lycksele | US-nät före samtycke | – | fonts.googleapis.com, fonts.gstatic.com | Google |
| Skellefteå | US-nät före samtycke | – | api-ts.cruncho.co, p.typekit.net, plus.browsealoud.com, skelleftea.cruncho.co, use.typekit.net, www.browsealoud.com | Adobe, Cruncho, Piwik PRO, Rek.ai, Texthelp |
| Arvidsjaur | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Arjeplog | US-nät före samtycke | – | plus.browsealoud.com, www.arjeploglapland.se, www.browsealoud.com | Texthelp |
| Jokkmokk | annat nät före samtycke | – | – | Piwik PRO |
| Överkalix | US-nät före samtycke | – | cdn.cookietractor.com, cdn.jsdelivr.net, code.jquery.com, fonts.googleapis.com, fonts.gstatic.com, maps.googleapis.com | Google, ReadSpeaker, Rek.ai, jQuery CDN, jsDelivr |
| Kalix | US-nät före samtycke | – | acsbapp.com, api.cludo.com, cdn.acsbapp.com, cdn.cookietractor.com, code.jquery.com, customer.cludo.com, fonts.googleapis.com, fonts.gstatic.com, www.gstatic.com | Cludo, Google, Rek.ai, jQuery CDN |
| Övertorneå | ingen tredjepart | – | – | – |
| Pajala | US-nät före samtycke | ja | code.jquery.com, fonts.googleapis.com, maps.googleapis.com, plus.browsealoud.com, region1.google-analytics.com, www.browsealoud.com, www.googletagmanager.com | Google, Texthelp, jQuery CDN |
| Gällivare | kunde inte mätas | – | – | – |
| Älvsbyn | ingen tredjepart | – | – | – |
| Luleå | bara EU/EES-nät före samtycke | – | – | Rek.ai |
| Piteå | US-nät före samtycke | – | consent.cookiebot.com, consentcdn.cookiebot.com | Usercentrics (Cookiebot) |
| Boden | US-nät före samtycke | – | a.eu.silktide.com, boden.matomo.cloud, cdn-cookieyes.com, cdn.matomo.cloud, log.cookieyes.com | InnoCraft (Matomo Cloud), Rek.ai, Silktide |
| Haparanda | US-nät före samtycke | – | cdn.ontame.io, collector.ontame.io | Rek.ai |
| Kiruna | kunde inte mätas | – | – | – |
| Region Stockholm | ingen tredjepart | – | – | – |
| Region Uppsala | US-nät före samtycke | – | unpkg.com | unpkg |
| Region Sörmland | bara EU/EES-nät före samtycke | – | – | Vizzit |
| Region Östergötland | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Region Jönköpings län | US-nät före samtycke | – | fonts.gstatic.com, policy.app.cookieinformation.com, translate.google.com, translate.googleapis.com, www.gstatic.com | Cookie Information, Google |
| Region Kronoberg | US-nät före samtycke | – | cdn.matomo.cloud, dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com, plus.browsealoud.com, regionkronoberg.matomo.cloud, www.browsealoud.com | Google, InnoCraft (Matomo Cloud), Optimizely, Texthelp |
| Region Kalmar län | annat nät före samtycke | – | – | ReadSpeaker |
| Region Blekinge | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Region Skåne | kunde inte mätas | – | – | – |
| Region Halland | bara EU/EES-nät före samtycke | – | – | Piwik PRO |
| Västra Götalandsregionen | US-nät före samtycke | – | app.usercentrics.eu, consent-api.service.consent.usercentrics.eu, privacy-proxy.usercentrics.eu, uct.service.usercentrics.eu, v1.api.service.cmp.usercentrics.eu, web.cmp.usercentrics.eu | – |
| Region Värmland | US-nät före samtycke | – | ka-p.fontawesome.com, kit.fontawesome.com | Fonticons (Font Awesome), Piwik PRO |
| Region Örebro län | US-nät före samtycke | – | dc.services.visualstudio.com, fonts.gstatic.com, js.monitor.azure.com, www.google.com, www.gstatic.com | Google, Microsoft |
| Region Västmanland | US-nät före samtycke | – | regionvastmanland.matomo.cloud | InnoCraft (Matomo Cloud), ReadSpeaker |
| Region Dalarna | US-nät före samtycke | – | az416426.vo.msecnd.net, cdn.cookietractor.com, cdn.matomo.cloud, dc.services.visualstudio.com, plus.browsealoud.com, www.browsealoud.com | InnoCraft (Matomo Cloud), Microsoft, Texthelp |
| Region Gävleborg | US-nät före samtycke | – | ajax.googleapis.com, cdn.cookielaw.org, cdn.jsdelivr.net, dc.services.visualstudio.com, geolocation.onetrust.com, js.monitor.azure.com, maxcdn.bootstrapcdn.com | Google, Microsoft, jsDelivr |
| Region Västernorrland | US-nät före samtycke | – | cdn.jsdelivr.net, dl.episerver.net, fonts.googleapis.com, fonts.gstatic.com, plus.browsealoud.com, www.browsealoud.com | Google, Optimizely, Texthelp, jsDelivr |
| Region Jämtland Härjedalen | bara EU/EES-nät före samtycke | – | – | Rek.ai, Vizzit |
| Region Västerbotten | annat nät före samtycke | – | – | Insipio, Piwik PRO |
| Region Norrbotten | US-nät före samtycke | – | js.monitor.azure.com, swedencentral-0.in.applicationinsights.azure.com | Microsoft |
