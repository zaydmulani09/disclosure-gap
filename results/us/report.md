# security.txt report: United States (federal .gov)

Source list: CISA dotgov-data (formerly GSA)  
List URL: https://raw.githubusercontent.com/cisagov/dotgov-data/main/current-federal.csv  
Scan window: 2026-11-26T03:19:29+00:00 to 2026-11-26T03:22:40+00:00 (UTC)  
Tool: disclosure-gap 0.1.0

## Headline

**5.1%** of reachable domains publish a security.txt file (47 of 926). **2.2%** publish one that passes the core RFC 9116 checks (20 of 926).

| Metric | Count | Share |
| --- | ---: | ---: |
| Domains in list | 1320 | |
| Reachable over HTTPS | 926 | 70.2% of list |
| Unreachable | 394 | 29.8% of list |
| security.txt found | 47 | 5.1% of reachable |
| Passes core RFC 9116 checks | 20 | 42.6% of files |
| No file | 879 | 94.9% of reachable |
| HTML page served with 200 instead of a file | 265 | |
| Request refused (401, 403, 429 or 451) | 161 | |
| Adoption if refused requests are left out | | 6.1% |
| File only at legacy /security.txt | 12 | |

Core checks: Contact present, exactly one Expires that is a valid date, not in the past and not more than a year away, file served over HTTPS. The one year limit is an RFC 9116 recommendation; the rest are MUSTs. The breakdown below shows each check on its own.

## Compliance breakdown (domains with a file)

| Field or check | Count | Share of files |
| --- | ---: | ---: |
| Contact present | 46 | 97.9% |
| Expires present | 43 | 91.5% |
| Expires is a valid date | 43 | 91.5% |
| Expires in the past | 12 | 25.5% |
| Expires more than a year away | 10 | 21.3% |
| Served over plain HTTP after a redirect | 0 | 0.0% |
| Meets RFC 9116 MUSTs | 30 | 63.8% |
| Canonical | 13 | 27.7% |
| Encryption | 10 | 21.3% |
| Policy | 33 | 70.2% |
| Preferred-Languages | 19 | 40.4% |
| PGP signed | 0 | 0.0% |

## Expired files (12)

| Domain | Expires |
| --- | --- |
| va.gov | 2025-01-18T18:59:59.000Z |
| vets.gov | 2025-01-18T18:59:59.000Z |
| boem.gov | 2025-12-01T08:00:00.000Z |
| bsee.gov | 2025-12-01T08:00:00.000Z |
| cpsc.gov | 2025-12-31T08:00:00.000Z |
| hanford.gov | 2026-01-01T08:00:00.000Z |
| fws.gov | 2026-01-15T00:00:00.000Z |
| rivers.gov | 2026-01-15T00:00:00.000Z |
| usccr.gov | 2026-02-24T12:04:49-05:00 |
| 400yaahc.gov | 2026-09-30T00:00:00.000Z |
| gsa.gov | 2026-09-30T00:00:00.000Z |
| pbrb.gov | 2026-09-30T00:00:00.000Z |

## Domains missing a file (879)

Reachable domains with no security.txt. Ranked by how many domains the same organization is missing, then by domain depth, so the largest gaps and top level sites come first.
Showing the first 100. The full list is in results.csv.

| # | Domain | Organization | HTTP status |
| ---: | --- | --- | ---: |
| 1 | 988.gov | Department of Health and Human Services | 403 |
| 2 | aanhpiheritage.gov | Department of Health and Human Services | 404 |
| 3 | acf.gov | Department of Health and Human Services | 202 |
| 4 | acl.gov | Department of Health and Human Services | 404 |
| 5 | aging.gov | Department of Health and Human Services | 403 |
| 6 | agingstats.gov | Department of Health and Human Services | 404 |
| 7 | ahcpr.gov | Department of Health and Human Services | 403 |
| 8 | ahrq.gov | Department of Health and Human Services | 403 |
| 9 | aids.gov | Department of Health and Human Services | 404 |
| 10 | alzheimers.gov | Department of Health and Human Services | 405 |
| 11 | aoa.gov | Department of Health and Human Services | 404 |
| 12 | arpa-h.gov | Department of Health and Human Services | 404 |
| 13 | arpah.gov | Department of Health and Human Services | 404 |
| 14 | aspr.gov | Department of Health and Human Services | 404 |
| 15 | birthcontrol.gov | Department of Health and Human Services | 200 |
| 16 | brain.gov | Department of Health and Human Services | 200 |
| 17 | cancer.gov | Department of Health and Human Services | 404 |
| 18 | cdc.gov | Department of Health and Human Services | 404 |
| 19 | childcare.gov | Department of Health and Human Services | 404 |
| 20 | childwelfare.gov | Department of Health and Human Services | 404 |
| 21 | clinicaltrials.gov | Department of Health and Human Services | 200 |
| 22 | cms.gov | Department of Health and Human Services | 404 |
| 23 | collegedrinkingprevention.gov | Department of Health and Human Services | 404 |
| 24 | cuidadodesalud.gov | Department of Health and Human Services | 404 |
| 25 | docline.gov | Department of Health and Human Services | 404 |
| 26 | drugabuse.gov | Department of Health and Human Services | 404 |
| 27 | eldercare.gov | Department of Health and Human Services | 404 |
| 28 | encuentraapoyo.gov | Department of Health and Human Services | 404 |
| 29 | everytrycounts.gov | Department of Health and Human Services | 200 |
| 30 | familyplanning.gov | Department of Health and Human Services | 200 |
| 31 | fatherhood.gov | Department of Health and Human Services | 403 |
| 32 | fda.gov | Department of Health and Human Services | 404 |
| 33 | findsupport.gov | Department of Health and Human Services | 404 |
| 34 | findtreatment.gov | Department of Health and Human Services | 200 |
| 35 | fitness.gov | Department of Health and Human Services | 404 |
| 36 | flu.gov | Department of Health and Human Services | 200 |
| 37 | foodsafety.gov | Department of Health and Human Services | 403 |
| 38 | fosteringthefuture.gov | Department of Health and Human Services | 404 |
| 39 | genome.gov | Department of Health and Human Services | 404 |
| 40 | getactive.gov | Department of Health and Human Services | 403 |
| 41 | globalhealth.gov | Department of Health and Human Services | 403 |
| 42 | gmta.gov | Department of Health and Human Services | 404 |
| 43 | grantsolutions.gov | Department of Health and Human Services | 404 |
| 44 | guideline.gov | Department of Health and Human Services | 403 |
| 45 | guidelines.gov | Department of Health and Human Services | 403 |
| 46 | headstart.gov | Department of Health and Human Services | 404 |
| 47 | health.gov | Department of Health and Human Services | 404 |
| 48 | healthcare.gov | Department of Health and Human Services | 404 |
| 49 | healthdata.gov | Department of Health and Human Services | 404 |
| 50 | healthfinder.gov | Department of Health and Human Services | 404 |
| 51 | healthit.gov | Department of Health and Human Services | 404 |
| 52 | healthypeople.gov | Department of Health and Human Services | 404 |
| 53 | hearttruth.gov | Department of Health and Human Services | 200 |
| 54 | hhs.gov | Department of Health and Human Services | 403 |
| 55 | hiv.gov | Department of Health and Human Services | 404 |
| 56 | hrsa.gov | Department of Health and Human Services | 403 |
| 57 | insurekidsnow.gov | Department of Health and Human Services | 404 |
| 58 | longtermcare.gov | Department of Health and Human Services | 404 |
| 59 | lowerdrugcosts.gov | Department of Health and Human Services | 404 |
| 60 | medicaid.gov | Department of Health and Human Services | 404 |
| 61 | medicalcountermeasures.gov | Department of Health and Human Services | 404 |
| 62 | medicamentosbajoprecio.gov | Department of Health and Human Services | 404 |
| 63 | medicare.gov | Department of Health and Human Services | 404 |
| 64 | medlineplus.gov | Department of Health and Human Services | 404 |
| 65 | menopause.gov | Department of Health and Human Services | 200 |
| 66 | mentalhealth.gov | Department of Health and Human Services | 404 |
| 67 | mesh.gov | Department of Health and Human Services | 200 |
| 68 | moms.gov | Department of Health and Human Services | 403 |
| 69 | nextlegends.gov | Department of Health and Human Services | 403 |
| 70 | nih.gov | Department of Health and Human Services | 404 |
| 71 | nlm.gov | Department of Health and Human Services | 404 |
| 72 | nnlm.gov | Department of Health and Human Services | 403 |
| 73 | opioids.gov | Department of Health and Human Services | 403 |
| 74 | organdonor.gov | Department of Health and Human Services | 403 |
| 75 | pubmed.gov | Department of Health and Human Services | 404 |
| 76 | realfood.gov | Department of Health and Human Services | 404 |
| 77 | recoverymonth.gov | Department of Health and Human Services | 404 |
| 78 | reproductivehealthservices.gov | Department of Health and Human Services | 200 |
| 79 | samhsa.gov | Department of Health and Human Services | 403 |
| 80 | selectagents.gov | Department of Health and Human Services | 404 |
| 81 | simplereport.gov | Department of Health and Human Services | 404 |
| 82 | smokefree.gov | Department of Health and Human Services | 404 |
| 83 | stopbullying.gov | Department of Health and Human Services | 403 |
| 84 | surgeongeneral.gov | Department of Health and Human Services | 403 |
| 85 | therealcost.gov | Department of Health and Human Services | 404 |
| 86 | thisfreelife.gov | Department of Health and Human Services | 404 |
| 87 | tox21.gov | Department of Health and Human Services | 404 |
| 88 | usphs.gov | Department of Health and Human Services | 404 |
| 89 | vaccines.gov | Department of Health and Human Services | 200 |
| 90 | whitehouseconferenceonaging.gov | Department of Health and Human Services | 404 |
| 91 | womenshealth.gov | Department of Health and Human Services | 404 |
| 92 | youth.gov | Department of Health and Human Services | 404 |
| 93 | acquisition.gov | General Services Administration | 404 |
| 94 | acquisitiongateway.gov | General Services Administration | 200 |
| 95 | afadvantage.gov | General Services Administration | 404 |
| 96 | benefits.gov | General Services Administration | 200 |
| 97 | buyamerican.gov | General Services Administration | 404 |
| 98 | cbca.gov | General Services Administration | 404 |
| 99 | cdo.gov | General Services Administration | 404 |
| 100 | cfo.gov | General Services Administration | 404 |

## Unreachable domains by reason

| Reason | Count |
| --- | ---: |
| dns | 244 |
| timeout | 82 |
| tls | 55 |
| readerror | 5 |
| too_many_redirects | 4 |
| connect | 3 |
| remoteprotocolerror | 1 |

