# Resultat — version 2

Mätt 2026-10-08 ca 15:37 UTC. Regler: METOD.md, "Version 2", skrivna innan
Skåne mättes.

- Stockholm: `data/ra-organisationer-2026-10-08T153724Z.json`
- Skåne: `data/ra-organisationer-skane-2026-10-08T153730Z.json`
- Tabellerna återskapas med `python3 klassa_v2.py <fil>`

## Utfall

| | Skåne (avgör) | Stockholm (utveckling) |
|---|---|---|
| E-post i Microsofts moln | 31 | 19 |
| E-post hos Google | 0 | 1 |
| Inga molnsignaler för e-post | 1 | 2 |
| Okänd | 2 | 5 |
| **Entydiga** | **32/34 = 94 %** | 22/27 = 81 % |
| **Kriterium v2 (≥85 %, ≤15 % okända)** | **uppfyllt** | ej uppfyllt (räknas inte) |
| Microsoft Entra-tenant (S5) | 34/34 | 27/27 |

**Metoden håller på data den inte utvecklats på.** Den håller sämre i
Stockholm, där fler kommuner har egen e-postinfrastruktur framför.

## Vad som kan sägas

- 50 av 61 organisationer har e-post som syns gå via Microsofts moln.
- Alla 61 har en Microsoft Entra-tenant.
- Det säger ingenting om vilka uppgifter som ligger där.

## Förbehåll

- **"Inga molnsignaler" betyder inte "inget moln".** Järfälla och Tyresö har
  ingen e-postsignal mot Microsoft, men S8 (Teams eller Entra-anslutna enheter)
  pekar dit.
- **Webbklassningen missar Akamai.** Region Skåne ligger bakom Akamai, ett
  amerikanskt CDN som Cloudflare, men klassas som "okänd" eftersom ASN:et är
  registrerat i NL. Rättas före nästa körning.
- **Kommundomäner skrevs för hand.** Alla 61 har NS-poster, men det är inte
  verifierat mot ett officiellt register.
