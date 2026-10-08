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
