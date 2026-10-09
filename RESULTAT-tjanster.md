# Resultat — var tjänsterna körs (mätning 4)

Regler: METOD.md, "Mätning 4" med tillägg och rättelser. Rådata:
`data/cert-2026-10-08T204928Z.json` (bara antal per organisation, aldrig
värdnamn; interna adresser bara som total, 1 268). Siffrorna räknas
fram av `fynd_siffror.py` (`cert_siffror`).

## Krav

| Krav | Utfall |
|---|---|
| Svar från certifikatloggar för ≥90 % av organisationerna | 512 av 512 |
| Nät för ≥95 % av aktiva namn | 99,9 % |
| T6: andra källan inom 15 procentenheter för ≥16 av 20 | 18 av 20 (`data/triangulering-t6-2026-10-09T081527Z.json`) |

Första körningen föll (94,1 % nät, namn med interna adresser räknades som
aktiva) och är borttagen. T6: första försöket föll på Certspotters timkvot
(6 av 20), det andra avbröts av ett fel vid sparandet (18 av 20, ej sparat).
T6 prövar bara att namnlistan är fullständig; båda källorna läser samma
certifikatloggar och nätklassningen är densamma.

## Utfall

| Grupp | Organisationer med namn | Aktiva namn | På amerikanska nät | Median per organisation | Inga på amerikanska nät | Största organisationens andel av de amerikanska namnen |
|---|---|---|---|---|---|---|
| Kommuner | 289 | 5 342 | 837 (15,7 %) | 0 % | 150 | 25 % |
| Regioner | 20 | 1 187 | 315 (26,5 %) | 13 % | 1 | 44 % |
| Myndighetsdomäner | 200 | 14 032 | 961 (6,8 %) | 3 % | 87 | 16 % |

Andelen räknat på alla namn drivs av ett fåtal organisationer; medianen per
organisation är det robustare måttet.

## Vad det här inte visar

- **Nätägare, inte plats.** "Amerikanskt nät" betyder att adressen hör till ett
  nät registrerat i USA eller ägt av ett amerikanskt bolag, inklusive CDN som
  Cloudflare och Akamai och moln som Azure, även i svenska datacenter. Övriga
  nät ägs av svenska eller europeiska bolag; var servrarna står mäts inte.
- **Bara namn med eget certifikat** under organisationens domän syns. Namn som
  bara täcks av jokercertifikat syns inte, vilket kan överskatta andelen på
  amerikanska nät, eftersom molnplattformar oftare utfärdar certifikat per namn.
- **Namn, inte användning.** Namnen omfattar allt med eget certifikat:
  webbplatser, e-tjänster, inloggning, e-postrelaterade namn med mera.
- Namn utan IPv4-adress räknas inte.
