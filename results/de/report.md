# security.txt report: Germany (federal)

Source list: robbi5/german-gov-domains (community maintained, CC0)  
List URL: https://raw.githubusercontent.com/robbi5/german-gov-domains/master/data/domains.federal.csv  
Scan window: 2026-11-26T18:09:52+00:00 to 2026-11-26T18:12:28+00:00 (UTC)  
Tool: disclosure-gap 0.1.0

## Headline

**11.4%** of reachable domains publish a security.txt file (25 of 219). **5.9%** publish one that passes the core RFC 9116 checks (13 of 219).

| Metric | Count | Share |
| --- | ---: | ---: |
| Domains in list | 660 | |
| Reachable over HTTPS | 219 | 33.2% of list |
| Unreachable | 441 | 66.8% of list |
| security.txt found | 25 | 11.4% of reachable |
| Passes core RFC 9116 checks | 13 | 52.0% of files |
| No file | 194 | 88.6% of reachable |
| HTML page served with 200 instead of a file | 59 | |
| Request refused (401, 403, 429 or 451) | 11 | |
| Adoption if refused requests are left out | | 12.0% |
| File only at legacy /security.txt | 1 | |

Core checks: Contact present, exactly one Expires that is a valid date, not in the past and not more than a year away, file served over HTTPS. The one year limit is an RFC 9116 recommendation; the rest are MUSTs. The breakdown below shows each check on its own.

## Compliance breakdown (domains with a file)

| Field or check | Count | Share of files |
| --- | ---: | ---: |
| Contact present | 25 | 100.0% |
| Expires present | 24 | 96.0% |
| Expires is a valid date | 24 | 96.0% |
| Expires in the past | 2 | 8.0% |
| Expires more than a year away | 9 | 36.0% |
| Served over plain HTTP after a redirect | 0 | 0.0% |
| Meets RFC 9116 MUSTs | 22 | 88.0% |
| Canonical | 10 | 40.0% |
| Encryption | 17 | 68.0% |
| Policy | 6 | 24.0% |
| Preferred-Languages | 23 | 92.0% |
| PGP signed | 3 | 12.0% |

## Expired files (2)

| Domain | Expires |
| --- | --- |
| bibb.de | 2024-12-30T23:00:00.000Z |
| bundesamtsozialesicherung.de | 2025-10-29T14:10:29z |

## Domains missing a file (194)

Reachable domains with no security.txt. Ranked by how many domains the same organization is missing, then by domain depth, so the largest gaps and top level sites come first.
Showing the first 100. The full list is in results.csv.

| # | Domain | Organization | HTTP status |
| ---: | --- | --- | ---: |
| 1 | arbeitderzukunft.de | Bundesministerium für Arbeit und Soziales | 200 |
| 2 | arbeitenviernull.de | Bundesministerium für Arbeit und Soziales | 404 |
| 3 | armutsbericht.de | Bundesministerium für Arbeit und Soziales | 404 |
| 4 | bmas.de | Bundesministerium für Arbeit und Soziales | 404 |
| 5 | csr-preis-bund.de | Bundesministerium für Arbeit und Soziales | 200 |
| 6 | csrindeutschland.de | Bundesministerium für Arbeit und Soziales | 200 |
| 7 | dates-esf-test.de | Bundesministerium für Arbeit und Soziales | 403 |
| 8 | dates-esf.de | Bundesministerium für Arbeit und Soziales | 404 |
| 9 | der-mindestlohn-kommt.de | Bundesministerium für Arbeit und Soziales | 404 |
| 10 | der-mindestlohn-wirkt.de | Bundesministerium für Arbeit und Soziales | 404 |
| 11 | einfachteilhaben.de | Bundesministerium für Arbeit und Soziales | 200 |
| 12 | equal.de | Bundesministerium für Arbeit und Soziales | 200 |
| 13 | esf-meine-geschichte.de | Bundesministerium für Arbeit und Soziales | 403 |
| 14 | esf.de | Bundesministerium für Arbeit und Soziales | 404 |
| 15 | fachkraeftewoche.de | Bundesministerium für Arbeit und Soziales | 200 |
| 16 | gda-psyche.de | Bundesministerium für Arbeit und Soziales | 403 |
| 17 | gemeinsam-einfach-machen.de | Bundesministerium für Arbeit und Soziales | 404 |
| 18 | generationpraktikum.de | Bundesministerium für Arbeit und Soziales | 440 |
| 19 | hartziv.de | Bundesministerium für Arbeit und Soziales | 404 |
| 20 | hinzuverdienstrechner.de | Bundesministerium für Arbeit und Soziales | 200 |
| 21 | ida.de | Bundesministerium für Arbeit und Soziales | 404 |
| 22 | initiative-neue-qualitaet-der-arbeit.de | Bundesministerium für Arbeit und Soziales | 404 |
| 23 | inqa-check.de | Bundesministerium für Arbeit und Soziales | 404 |
| 24 | inqa-pflege.de | Bundesministerium für Arbeit und Soziales | 403 |
| 25 | inqa.de | Bundesministerium für Arbeit und Soziales | 404 |
| 26 | leitfadeninklusion.de | Bundesministerium für Arbeit und Soziales | 200 |
| 27 | meincomeback.de | Bundesministerium für Arbeit und Soziales | 200 |
| 28 | meinmicrokredit.de | Bundesministerium für Arbeit und Soziales | 200 |
| 29 | meinmikrokredit.de | Bundesministerium für Arbeit und Soziales | 200 |
| 30 | neue-qualitaet-der-arbeit.de | Bundesministerium für Arbeit und Soziales | 404 |
| 31 | sgb2.info | Bundesministerium für Arbeit und Soziales | 404 |
| 32 | sozialbeirat.de | Bundesministerium für Arbeit und Soziales | 404 |
| 33 | tagderjobcenter.de | Bundesministerium für Arbeit und Soziales | 404 |
| 34 | tln-mobility.eu | Bundesministerium für Arbeit und Soziales | 404 |
| 35 | unternehmens-wert-mensch.de | Bundesministerium für Arbeit und Soziales | 200 |
| 36 | vier-punkt-null.de | Bundesministerium für Arbeit und Soziales | 200 |
| 37 | xenos-de.de | Bundesministerium für Arbeit und Soziales | 200 |
| 38 | xn--fachkrfteoffensive-qtb.de | Bundesministerium für Arbeit und Soziales | 404 |
| 39 | mobil.einfachteilhaben.de | Bundesministerium für Arbeit und Soziales | 200 |
| 40 | blickpunkt-bundestag.de | Bundestag | 200 |
| 41 | bundeshaus.de | Bundestag | 404 |
| 42 | bundestag.eu | Bundestag | 200 |
| 43 | bundestagsarena.de | Bundestag | 404 |
| 44 | bundestagspraesident.de | Bundestag | 200 |
| 45 | bundestagspraesidentin.de | Bundestag | 200 |
| 46 | bundesversammlung.de | Bundestag | 200 |
| 47 | das-parlament.de | Bundestag | 400 |
| 48 | datenhandbuch-bundestag.de | Bundestag | 200 |
| 49 | dbtg-newsletter.de | Bundestag | 200 |
| 50 | dbtg.eu | Bundestag | 200 |
| 51 | dbtg.tv | Bundestag | 200 |
| 52 | derbevoelkerung.de | Bundestag | 404 |
| 53 | deutscher-bundestag.de | Bundestag | 200 |
| 54 | deutscher-bundestag.eu | Bundestag | 200 |
| 55 | deutscherdom.de | Bundestag | 200 |
| 56 | deutsches-parlament.eu | Bundestag | 200 |
| 57 | dip21.de | Bundestag | 200 |
| 58 | kunst-im-bundestag.de | Bundestag | 200 |
| 59 | kuppel-kucker.de | Bundestag | 200 |
| 60 | kuppel-kucker.info | Bundestag | 200 |
| 61 | kuppel-kucker.org | Bundestag | 200 |
| 62 | marie-elisabeth-lueders-haus.de | Bundestag | 200 |
| 63 | mauer-mahnmal.de | Bundestag | 200 |
| 64 | ostseeparlamentarierkonferenz.de | Bundestag | 200 |
| 65 | parlamentsfernsehen.de | Bundestag | 200 |
| 66 | paul-loebe-haus.de | Bundestag | 200 |
| 67 | reichstag.eu | Bundestag | 200 |
| 68 | reichstagsgebaeude.de | Bundestag | 200 |
| 69 | reichstagsgebaeude.eu | Bundestag | 200 |
| 70 | wehrbeauftragter.de | Bundestag | 200 |
| 71 | cmsaf.eu | Deutscher Wetterdienst | 404 |
| 72 | deutsches-klimaportal.de | Deutscher Wetterdienst | 404 |
| 73 | dwd-shop.de | Deutscher Wetterdienst | 403 |
| 74 | dwd-shop.eu | Deutscher Wetterdienst | 403 |
| 75 | dwd.de | Deutscher Wetterdienst | 404 |
| 76 | flugwetter.de | Deutscher Wetterdienst | 404 |
| 77 | gruan.org | Deutscher Wetterdienst | 200 |
| 78 | met4aviation.com | Deutscher Wetterdienst | 403 |
| 79 | uv-index.de | Deutscher Wetterdienst | 200 |
| 80 | wettergefahren.de | Deutscher Wetterdienst | 404 |
| 81 | wettergefahren.eu | Deutscher Wetterdienst | 404 |
| 82 | wetterlexikon.eu | Deutscher Wetterdienst | 200 |
| 83 | bundesstelle-fuer-informationstechnik.de | Bundesverwaltungsamt | 404 |
| 84 | bundesverwaltungsamt.de | Bundesverwaltungsamt | 404 |
| 85 | dsd-weltweit.de | Bundesverwaltungsamt | 403 |
| 86 | government-site-builder.de | Bundesverwaltungsamt | 404 |
| 87 | wwwbund.de | Bundesverwaltungsamt | 200 |
| 88 | zuwes.de | Bundesverwaltungsamt | 200 |
| 89 | bva.bund.de | Bundesverwaltungsamt | 404 |
| 90 | bezuegerechner.bva.bund.de | Bundesverwaltungsamt | 404 |
| 91 | bundeskriminalamt.de | Bundeskriminalamt | 404 |
| 92 | deutsche-polizei.eu | Bundeskriminalamt | 404 |
| 93 | european-enet.org | Bundeskriminalamt | 404 |
| 94 | bundesfinanzministerium.de | Bundesministerium der Finanzen | 404 |
| 95 | finanzforscher.de | Bundesministerium der Finanzen | 200 |
| 96 | zoll.de | Bundesministerium der Finanzen | 404 |
| 97 | evergabe-online.info | Beschaffungsamt des Bundesministeriums des Innern | 404 |
| 98 | bescha.bund.de | Beschaffungsamt des Bundesministeriums des Innern | 404 |
| 99 | breitbandatlas.de | Bundesministerium für Verkehr und digitale Infrastruktur | 200 |
| 100 | radwegdeutscheeinheit.de | Bundesministerium für Verkehr und digitale Infrastruktur | 404 |

## Unreachable domains by reason

| Reason | Count |
| --- | ---: |
| dns | 245 |
| tls | 95 |
| timeout | 88 |
| connect | 12 |
| too_many_redirects | 1 |

