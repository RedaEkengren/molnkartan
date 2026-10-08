# Resultat — säkerhetsgrunder (mätning 5)

Regler: METOD.md, "Mätning 5". Rådata: `data/sakerhet-2026-10-08T180801Z.json` (bara antal, se gränsen).
Kontroller före körningen höll: {'cloudflare.com DS': True, 'google.com DS': False, 'google.com DMARC': 'p=reject', 'google.com MTA-STS': True}.
DMARC, DNSSEC och SPF kontrollerades också via 9.9.9.9: samma värde för 512 av 512.

**Gräns:** redovisas bara per län och för myndigheterna som grupp, aldrig per
organisation.

| Signal | Kommuner och regioner | Myndighetsdomäner |
|---|---|---|
| DMARC `p=reject` (falska avsändare avvisas) | 132 av 310 (43 %) | 78 av 202 (39 %) |
| DMARC `p=quarantine` | 75 av 310 (24 %) | 57 av 202 (28 %) |
| DMARC `p=none` (bara övervakning) | 97 av 310 (31 %) | 49 av 202 (24 %) |
| DMARC saknas | 6 av 310 (2 %) | 18 av 202 (9 %) |
| SPF med `-all` | 242 av 310 (78 %) | 147 av 202 (73 %) |
| DNSSEC | 257 av 310 (83 %) | 154 av 202 (76 %) |
| MTA-STS | 34 av 310 (11 %) | 22 av 202 (11 %) |
| TLS-RPT | 50 av 310 (16 %) | 30 av 202 (15 %) |
| HSTS på webbplatsen | 184 av 310 (59 %) | 111 av 202 (55 %) |

## Per län

| Län | Organisationer | DMARC reject | DMARC none | DNSSEC | MTA-STS | HSTS |
|---|---|---|---|---|---|---|
| Blekinge län | 6 | 17 % | 33 % | 83 % | 33 % | 0 % |
| Dalarnas län | 16 | 38 % | 38 % | 100 % | 0 % | 69 % |
| Gävleborgs län | 11 | 55 % | 9 % | 100 % | 0 % | 55 % |
| Hallands län | 7 | 43 % | 43 % | 57 % | 14 % | 57 % |
| Jämtlands län | 9 | 33 % | 22 % | 89 % | 11 % | 44 % |
| Jönköpings län | 14 | 79 % | 14 % | 93 % | 7 % | 50 % |
| Kalmar län | 13 | 38 % | 38 % | 92 % | 23 % | 31 % |
| Kronobergs län | 9 | 22 % | 56 % | 100 % | 0 % | 44 % |
| Norrbottens län | 15 | 13 % | 33 % | 100 % | 20 % | 80 % |
| Skåne län | 34 | 56 % | 24 % | 76 % | 9 % | 62 % |
| Stockholms län | 27 | 33 % | 41 % | 78 % | 4 % | 74 % |
| Södermanlands län | 10 | 30 % | 40 % | 90 % | 20 % | 80 % |
| Uppsala län | 9 | 44 % | 33 % | 67 % | 11 % | 33 % |
| Värmlands län | 17 | 59 % | 18 % | 100 % | 29 % | 59 % |
| Västerbottens län | 16 | 69 % | 12 % | 88 % | 6 % | 50 % |
| Västernorrlands län | 8 | 25 % | 25 % | 88 % | 12 % | 75 % |
| Västmanlands län | 11 | 9 % | 73 % | 73 % | 36 % | 55 % |
| Västra Götalands län | 50 | 54 % | 24 % | 72 % | 6 % | 70 % |
| Örebro län | 13 | 15 % | 54 % | 62 % | 0 % | 46 % |
| Östergötlands län | 14 | 36 % | 36 % | 79 % | 14 % | 57 % |

## Vad det betyder

- **DMARC `p=none`** betyder att domänen talar om att den vill ha rapporter, men
  ber mottagare att ändå leverera e-post som utger sig för att komma från den.
  Det gäller nästan var tredje kommun.
- **MTA-STS** gör att e-post till domänen inte kan tvingas över okrypterade
  förbindelser. Ungefär var tionde har det.
- **DNSSEC** är vanligt, vilket stämmer med att .se var tidigt ute med det.
