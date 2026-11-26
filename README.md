# disclosure-gap

[![CI](https://github.com/zaydmulani09/disclosure-gap/actions/workflows/ci.yml/badge.svg)](https://github.com/zaydmulani09/disclosure-gap/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Dataset](https://img.shields.io/badge/dataset-Hugging%20Face-yellow)](https://huggingface.co/datasets/zaydmulani/disclosure-gap)

If you find a security bug on a government website, who do you tell?

[RFC 9116](https://www.rfc-editor.org/rfc/rfc9116) gives a simple answer: a plain text file at `/.well-known/security.txt` that lists a contact. `disclosure-gap` checks which government domains actually publish one, country by country, and writes a clean report for each.

## Results (November 2026)

Across 9,893 government domains on three national lists, 7,479 answered over HTTPS. Only **271 of them (3.6%) publish a security.txt file**, and only 104 pass the core RFC 9116 checks.

| Country | Domains | Reachable | With security.txt | Adoption (reachable) | Meets RFC MUSTs | Passing core checks | Expired | HTML 200 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Germany (federal) | 660 | 219 | 25 | 11.4% | 22 | 13 (5.9%) | 2 | 59 |
| United Kingdom (.gov.uk) | 7913 | 6334 | 199 | 3.1% | 130 | 71 (1.1%) | 28 | 649 |
| United States (federal .gov) | 1320 | 926 | 47 | 5.1% | 30 | 20 (2.2%) | 12 | 265 |

* Germany uses a community list from 2022, so many of its domains are retired and only 219 answered.
* Refused requests (403 and similar) are common: 1,328 UK and 161 US domains turned the tool away. With those left out, adoption is 4.0% for the UK and 6.1% for the US.
* 42 files across the three countries have an Expires date in the past.

Full per country reports: [US](results/us/report.md), [UK](results/uk/report.md), [Germany](results/de/report.md), [summary](results/SUMMARY.md). Raw data is also on [Hugging Face](https://huggingface.co/datasets/zaydmulani/disclosure-gap).

Scans ran on 26 November 2026 (UTC).

## What it does

For every domain in a list it makes one HTTPS GET to `/.well-known/security.txt`, and only if that is not a real file, one GET to the legacy `/security.txt`. That is all. Then it:

* parses the file, including PGP clearsigned files
* checks the RFC 9116 rules: Contact present, Expires present, valid, not in the past and not more than a year away, only one Expires, served over HTTPS
* records the optional fields: Canonical, Encryption, Policy, Preferred-Languages
* flags HTML pages served with status 200 that are not real security.txt files (soft 404s)
* writes JSON, CSV and a Markdown report per country, plus one summary table across countries

Built in country lists:

| Key | List | Publisher |
| --- | --- | --- |
| `us` | Federal .gov domains | [CISA dotgov-data](https://github.com/cisagov/dotgov-data) `current-federal.csv` |
| `uk` | All .gov.uk domains | [Cabinet Office, List of .gov.uk domain names](https://www.gov.uk/government/publications/list-of-gov-uk-domain-names) (latest CSV is picked automatically) |
| `de` | German federal domains | [robbi5/german-gov-domains](https://github.com/robbi5/german-gov-domains) `domains.federal.csv` (community maintained, CC0, last updated 2022) |

Germany has no official public list, so the community list is used and labelled as such. You can scan any other country by passing your own text file.

## Install

```
pip install git+https://github.com/zaydmulani09/disclosure-gap
```

Python 3.11 or newer. The only runtime dependency is `httpx`.

## Usage

```
disclosure-gap sources                      # show built in lists
disclosure-gap scan --country us            # one country
disclosure-gap scan --all                   # every built in list
disclosure-gap scan --input my-list.txt --label fr --name "France"
disclosure-gap report results               # rebuild reports from scan.json files
disclosure-gap compare results/us/scan.json old/us/scan.json
```

`scan` options:

| Option | Default | Meaning |
| --- | --- | --- |
| `--out` | `results` | output folder |
| `--concurrency` | `8` | domains checked at the same time |
| `--timeout` | `10` | seconds per request |
| `--host-interval` | `1` | minimum seconds between two requests to the same host |
| `--limit` | none | only the first N domains of each list |
| `--top` | `100` | missing domains listed in `report.md` |

An input file is one domain per line. Lines starting with `#` are ignored.

`compare` prints the summary table for any number of `scan.json` files. Given two scans of the same country it also lists which domains gained or lost a file between them.

## Output

```
results/
  SUMMARY.md          combined table across countries
  summary.json
  us/
    scan.json         every domain, raw result and parsed fields
    results.csv       one row per domain
    summary.json      the numbers in report.md
    report.md         adoption, compliance breakdown, expired files, ranked missing list
  uk/ ...
  de/ ...
```

Each domain gets one of four results:

* `compliant`: a security.txt that passes every core check
* `present`: a security.txt that fails at least one check
* `missing`: the host answered over HTTPS but has no security.txt (404, 403, an HTML page, and so on)
* `unreachable`: no HTTPS answer at all (DNS failure, timeout, TLS error, refused connection)

Adoption is counted against reachable domains, because a domain with no working HTTPS site has nothing to report bugs about. Reports also show the share of the whole list and the reasons domains were unreachable.

Limits worth knowing: only the exact domain in the list is checked, so a site that only answers on `www.` counts as unreachable. Some servers refuse automated clients with 403, so reports also give adoption with refused requests left out. TLS errors include servers whose certificate chain cannot be verified with the standard Python CA bundle.

The ranked list of missing domains puts organizations with the most missing domains first, then shorter (more top level) domains, so the largest gaps are at the top.

## Ethics

This is a passive check of a file that exists to be read by strangers.

* One GET per path, at most two paths per domain, at most three redirects. No crawling, no port scans, no exploitation, no login attempts, nothing else.
* Every request carries the User-Agent `disclosure-gap/0.1.0 (+https://github.com/zaydmulani09/disclosure-gap)` so site owners can see who is asking and why.
* Low concurrency, at least one second between requests to the same host, a 10 second timeout, and `Retry-After` is respected on 429 and 503.
* If a host does not answer the first request, the second path is skipped.
* Responses are capped at 64 KB.
* The tool never contacts anyone. Reports are files only.

## Related work

* [Pentest Partners, scanning for security.txt files](https://www.pentestpartners.com/security-blog/scanning-for-security-txt-files/) (2020): a one off scan of the .gov.uk list.
* [GDS, advocating security.txt across UK government](https://technology.blog.gov.uk/2023/08/10/advocating-security-txt-across-uk-government/) (2023): UK guidance and its own adoption push.
* [ScanGov](https://govfresh.com/signal/scangov-security-grades-scores): grades US federal and state sites on several headers including security.txt, US only.
* [Li et al., IMC 2021](https://faculty.cc.gatech.edu/~frankli/papers/li-imc2021-securitytxt.pdf) and [Findlay and Abdou, MADWeb 2022](https://scs.carleton.ca/~abdou/findlay2022_madweb_authors_copy.pdf): academic studies of security.txt across the top 1M sites.
* [URIports adoption follow ups](https://www.uriports.com/blog/security-txt-in-2025/): adoption and common mistakes across popular sites.
* [ExcelliumSA/SecurityTXT-Study](https://github.com/ExcelliumSA/SecurityTXT-Study): one off study of security.txt usage.
* General validators and scanners: [DigitalTrustCenter/sectxt](https://github.com/DigitalTrustCenter/sectxt), [eikendev/sectxt](https://github.com/eikendev/sectxt), [go-security-txt](https://github.com/tschmidtb51/go-security-txt), [disclose/diosts](https://github.com/disclose/diosts), [h4sh5/securitytxt-scan](https://github.com/h4sh5/securitytxt-scan) (made for Australian domains), [security-txt-toolkit](https://github.com/rhymeswithmogul/security-txt-toolkit).

What this adds: the validators above check a domain or a list you bring. The studies are one off and either cover one country or the general web. `disclosure-gap` fetches official national government domain lists itself, runs the same polite checks on each, and produces comparable per country reports and a cross country table that can be rerun at any time and diffed with `compare`.

## Development

```
pip install -e ".[test]"
pytest
```

Tests mock all HTTP with `respx`, so they never touch the network.

## License

MIT
