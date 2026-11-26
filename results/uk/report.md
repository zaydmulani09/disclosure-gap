# security.txt report: United Kingdom (.gov.uk)

Source list: Cabinet Office, List of .gov.uk domain names (GOV.UK)  
List URL: https://assets.publishing.service.gov.uk/media/69cbd582024cdf09254f3f7d/List_of_.gov.uk_domain_names_as_of_31_March_2026_1.csv  
Scan window: 2026-11-26T17:41:01+00:00 to 2026-11-26T18:09:52+00:00 (UTC)  
Tool: disclosure-gap 0.1.0

## Headline

**3.1%** of reachable domains publish a security.txt file (199 of 6334). **1.1%** publish one that passes the core RFC 9116 checks (71 of 6334).

| Metric | Count | Share |
| --- | ---: | ---: |
| Domains in list | 7913 | |
| Reachable over HTTPS | 6334 | 80.0% of list |
| Unreachable | 1579 | 20.0% of list |
| security.txt found | 199 | 3.1% of reachable |
| Passes core RFC 9116 checks | 71 | 35.7% of files |
| No file | 6135 | 96.9% of reachable |
| HTML page served with 200 instead of a file | 649 | |
| Request refused (401, 403, 429 or 451) | 1328 | |
| Adoption if refused requests are left out | | 4.0% |
| File only at legacy /security.txt | 8 | |

Core checks: Contact present, exactly one Expires that is a valid date, not in the past and not more than a year away, file served over HTTPS. The one year limit is an RFC 9116 recommendation; the rest are MUSTs. The breakdown below shows each check on its own.

## Compliance breakdown (domains with a file)

| Field or check | Count | Share of files |
| --- | ---: | ---: |
| Contact present | 198 | 99.5% |
| Expires present | 188 | 94.5% |
| Expires is a valid date | 159 | 79.9% |
| Expires in the past | 28 | 14.1% |
| Expires more than a year away | 60 | 30.2% |
| Served over plain HTTP after a redirect | 1 | 0.5% |
| Meets RFC 9116 MUSTs | 130 | 65.3% |
| Canonical | 24 | 12.1% |
| Encryption | 14 | 7.0% |
| Policy | 143 | 71.9% |
| Preferred-Languages | 63 | 31.7% |
| PGP signed | 1 | 0.5% |

## Expired files (28)

| Domain | Expires |
| --- | --- |
| derbys-fire.gov.uk | 2023-02-01T11:37:00.000Z |
| lothian-vjb.gov.uk | 2023-03-31T22:59:00.000Z |
| hampshire-pcc.gov.uk | 2023-05-01T00:00:00.000Z |
| arun.gov.uk | 2023-10-27T23:00:00.000Z |
| linets.gov.uk | 2024-01-09T12:00:00.000Z |
| royal.gov.uk | 2024-02-01T23:59:59+00:00 |
| trade.gov.uk | 2024-07-01T00:00:00Z |
| cropwellbishop-pc.gov.uk | 2024-12-01T00:00:00.000Z |
| stratford.gov.uk | 2024-12-31T00:00:00.000Z |
| gamblingcommission.gov.uk | 2025-01-01T01:00:00.000Z |
| westlothian.gov.uk | 2025-01-01T15:00:00.000Z |
| londontribunals.gov.uk | 2025-03-20 13:43:25+0000 |
| lawcom.gov.uk | 2025-12-31T23:59:00.000Z |
| ppo.gov.uk | 2025-12-31T23:59:00.000Z |
| ccrc.gov.uk | 2025-12-31T23:59:00.000Z |
| judicialappointments.gov.uk | 2025-12-31T23:59:00.000Z |
| justiceinspectorates.gov.uk | 2025-12-31T23:59:00.000Z |
| prisonandprobationjobs.gov.uk | 2025-12-31T23:59:00.000Z |
| newfuturesnetwork.gov.uk | 2025-12-31T23:59:00.000Z |
| firescotland.gov.uk | 2026-03-31T22:59:00.000Z |
| scotlandscensus.gov.uk | 2026-06-01T11:00:00.000Z |
| tartanregister.gov.uk | 2026-06-01T11:00:00.000Z |
| calderdale.gov.uk | 2026-08-18T13:00:00.000Z |
| manchester.gov.uk | 2026-09-10T11:00:00.000Z |
| bassetlaw.gov.uk | 2026-10-14T10:27:00Z |
| grangeoversandstowncouncil.gov.uk | 2026-11-21T17:00:00.000Z |
| sedgwickparishcouncil.gov.uk | 2026-11-21T17:00:00.000Z |
| snh.gov.uk | 2026-11-26T12:00:00Z |

## Domains missing a file (6135)

Reachable domains with no security.txt. Ranked by how many domains the same organization is missing, then by domain depth, so the largest gaps and top level sites come first.
Showing the first 100. The full list is in results.csv.

| # | Domain | Organization | HTTP status |
| ---: | --- | --- | ---: |
| 1 | abbasandtemplecombe-pc.gov.uk |  | 404 |
| 2 | abbertonandlangenhoeparish.gov.uk |  | 404 |
| 3 | abbeydoreandbactongroup-pc.gov.uk |  | 404 |
| 4 | abbeyhillparishcouncil.gov.uk |  | 403 |
| 5 | abbotskerswell-pc.gov.uk |  | 403 |
| 6 | abbotslangley-pc.gov.uk |  | 403 |
| 7 | abbotsleighparish.gov.uk |  | 404 |
| 8 | abbotsleyparishcouncil.gov.uk |  | 404 |
| 9 | abbotsripton-pc.gov.uk |  | 404 |
| 10 | abbottsann-pc.gov.uk |  | 200 |
| 11 | abbr-pc.gov.uk |  | 404 |
| 12 | abdonandheathparish.gov.uk |  | 200 |
| 13 | aberdeenshire.gov.uk |  | 404 |
| 14 | aberford-pc.gov.uk |  | 404 |
| 15 | abergavennytowncouncil.gov.uk |  | 404 |
| 16 | abertawe.gov.uk |  | 404 |
| 17 | abertilleryandllanhilleth-wcc.gov.uk |  | 404 |
| 18 | aberystwyth.gov.uk |  | 404 |
| 19 | abingdon.gov.uk |  | 403 |
| 20 | abinger-pc.gov.uk |  | 200 |
| 21 | abington-pc.gov.uk |  | 403 |
| 22 | abthorpeparish.gov.uk |  | 404 |
| 23 | acastermalbis-pc.gov.uk |  | 404 |
| 24 | accounts-commission.gov.uk |  | 200 |
| 25 | acklington-pc.gov.uk |  | 200 |
| 26 | acleparishcouncil.gov.uk |  | 404 |
| 27 | acol-pc.gov.uk |  | 200 |
| 28 | acombparish.gov.uk |  | 404 |
| 29 | activetravelengland.gov.uk |  | 404 |
| 30 | actonbridge-pc.gov.uk |  | 404 |
| 31 | actonburnell-pc.gov.uk |  | 404 |
| 32 | actonparishcouncil.gov.uk |  | 403 |
| 33 | actontrussellbednall-pc.gov.uk |  | 200 |
| 34 | actonturville-pc.gov.uk |  | 200 |
| 35 | adderburyparishcouncil.gov.uk |  | 404 |
| 36 | addingham-pc.gov.uk |  | 403 |
| 37 | addington-pc.gov.uk |  | 404 |
| 38 | addlethorpeparishcouncil.gov.uk |  | 404 |
| 39 | adisham-pc.gov.uk |  | 404 |
| 40 | adlington-pc.gov.uk |  | 404 |
| 41 | adlingtontowncouncil.gov.uk |  | 404 |
| 42 | admingtonparishcouncil.gov.uk |  | 404 |
| 43 | adstockparish.gov.uk |  | 403 |
| 44 | adur-worthing.gov.uk |  | 404 |
| 45 | ahmlr.gov.uk |  | 200 |
| 46 | ai.gov.uk |  | 403 |
| 47 | aib.gov.uk |  | 404 |
| 48 | aightonbaileyandchaigley-pc.gov.uk |  | 403 |
| 49 | ailsworth-pc.gov.uk |  | 404 |
| 50 | ainstable-pc.gov.uk |  | 403 |
| 51 | aintreevillageparishcouncil.gov.uk |  | 404 |
| 52 | aisi.gov.uk |  | 404 |
| 53 | aiskewleemingbar-pc.gov.uk |  | 404 |
| 54 | aislabyparishcouncil.gov.uk |  | 404 |
| 55 | akeleyparishcouncil.gov.uk |  | 403 |
| 56 | alberburywithcardestonparishcouncil.gov.uk |  | 200 |
| 57 | albrightondonington-pc.gov.uk |  | 403 |
| 58 | albrightonparishcouncil.gov.uk |  | 403 |
| 59 | alburgh-pc.gov.uk |  | 404 |
| 60 | alburyparishcouncil.gov.uk |  | 404 |
| 61 | alcester-tc.gov.uk |  | 404 |
| 62 | alconburyparishcouncil.gov.uk |  | 404 |
| 63 | alconburyweston-pc.gov.uk |  | 404 |
| 64 | alcshropshire.gov.uk |  | 404 |
| 65 | aldboroughandthurgarton-pc.gov.uk |  | 200 |
| 66 | aldbourne-pc.gov.uk |  | 403 |
| 67 | aldbroughstjohnparishcouncil.gov.uk |  | 404 |
| 68 | aldburyparishcouncil.gov.uk |  | 404 |
| 69 | aldeburghtowncouncil.gov.uk |  | 403 |
| 70 | aldebyparishcouncil.gov.uk |  | 404 |
| 71 | aldenham-pc.gov.uk |  | 403 |
| 72 | alderburyparishcouncil.gov.uk |  | 403 |
| 73 | alderleyedge-pc.gov.uk |  | 404 |
| 74 | aldermaston-pc.gov.uk |  | 404 |
| 75 | alderminster-pc.gov.uk |  | 404 |
| 76 | aldertonparishcouncil.gov.uk |  | 404 |
| 77 | aldertonsuffolk-pc.gov.uk |  | 404 |
| 78 | alderwasleyparishcouncil.gov.uk |  | 404 |
| 79 | aldhamsuffolk-pc.gov.uk |  | 404 |
| 80 | aldingbourne-pc.gov.uk |  | 404 |
| 81 | aldinghamparishcouncil.gov.uk |  | 403 |
| 82 | aldingtonandbonnington-pc.gov.uk |  | 403 |
| 83 | aldwickparishcouncil.gov.uk |  | 404 |
| 84 | aldwincleparishcouncil.gov.uk |  | 404 |
| 85 | aldworth-pc.gov.uk |  | 404 |
| 86 | alfoldparishcouncil.gov.uk |  | 404 |
| 87 | alfordtowncouncil.gov.uk |  | 403 |
| 88 | alfretontowncouncil.gov.uk |  | 403 |
| 89 | algarkirkparishcouncil.gov.uk |  | 404 |
| 90 | alkboroughwalcotparishcouncil.gov.uk |  | 403 |
| 91 | alkingtonparishcouncil.gov.uk |  | 401 |
| 92 | allbrook-pc.gov.uk |  | 404 |
| 93 | allcannings-pc.gov.uk |  | 404 |
| 94 | allendaleparish.gov.uk |  | 200 |
| 95 | allerparishcouncil.gov.uk |  | 404 |
| 96 | allerthorpeparishcouncil.gov.uk |  | 404 |
| 97 | allertonbywaterparishcouncil.gov.uk |  | 404 |
| 98 | allhallows-pc.gov.uk |  | 404 |
| 99 | allingtonboscombewilts-pc.gov.uk |  | 403 |
| 100 | allithwaiteandcartmel-pc.gov.uk |  | 403 |

## Unreachable domains by reason

| Reason | Count |
| --- | ---: |
| dns | 705 |
| timeout | 404 |
| tls | 321 |
| connect | 140 |
| too_many_redirects | 6 |
| readerror | 2 |
| remoteprotocolerror | 1 |

