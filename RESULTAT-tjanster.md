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
T6 jämför andelar mellan två läsare av samma certifikatloggar, med samma
nätklassning. Det prövar inte att namnlistan är fullständig.

## Utfall

| Grupp | Organisationer med namn | Aktiva namn | På amerikanska nät | Median per organisation | Inga namn på amerikanska nät hittade | Största organisationens andel av de amerikanska namnen |
|---|---|---|---|---|---|---|
| Kommuner | 289 | 5 342 | 837 (15,7 %) | 0 % | 150 | 25 % |
| Regioner | 20 | 1 187 | 315 (26,5 %) | 13 % | 1 | 44 % |
| Myndighetsdomäner | 200 | 14 032 | 961 (6,8 %) | 3 % | 87 | 16 % |

Andelen räknat på alla namn drivs av ett fåtal organisationer; medianen per
organisation är det robustare måttet.

## Vad det här inte visar

- **Nätägare, inte plats.** "Amerikanskt nät" betyder att adressen hör till ett
  nät registrerat i USA eller ägt av ett amerikanskt bolag, inklusive CDN som
  Cloudflare och Akamai och moln som Azure, även i svenska datacenter. Av alla
  namn ligger 18 418 på nät som ägs av europeiska bolag, 14 på nät i andra länder
  och 16 på nät som inte gick att identifiera; var servrarna står mäts inte.
- **Bara namn med eget certifikat** under organisationens domän syns. Namn som
  bara täcks av jokercertifikat syns inte; riktningen på det felet är inte
  undersökt.
- **Ingen hittad är inte ingen.** "Inga på amerikanska nät" betyder att inget
  sådant namn hittades i underlaget. T6 räcker inte för att pröva nollkategorin:
  för Grums hittade den andra källan namn på amerikanska nät (issue #19).
- **En A-post visar inte att en tjänst körs**, bara att namnet pekar på en adress.
- **Namn, inte användning.** Namnen omfattar allt med eget certifikat:
  webbplatser, e-tjänster, inloggning, e-postrelaterade namn med mera.
- Namn utan IPv4-adress räknas inte.
