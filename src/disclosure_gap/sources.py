import csv
import io
import re

import httpx

UK_CONTENT_API = "https://www.gov.uk/api/content/government/publications/list-of-gov-uk-domain-names"

SOURCES = {
    "us": {
        "name": "United States (federal .gov)",
        "url": "https://raw.githubusercontent.com/cisagov/dotgov-data/main/current-federal.csv",
        "publisher": "CISA dotgov-data (formerly GSA)",
        "column": "Domain name",
        "org_column": "Organization name",
        "suffix": ".gov",
    },
    "uk": {
        "name": "United Kingdom (.gov.uk)",
        "url": None,
        "publisher": "Cabinet Office, List of .gov.uk domain names (GOV.UK)",
        "column": None,
        "org_column": None,
        "suffix": ".gov.uk",
    },
    "de": {
        "name": "Germany (federal)",
        "url": "https://raw.githubusercontent.com/robbi5/german-gov-domains/master/data/domains.federal.csv",
        "publisher": "robbi5/german-gov-domains (community maintained, CC0)",
        "column": "Domain Name",
        "org_column": "Agency",
        "suffix": None,
    },
}

DOMAIN_RE = re.compile(r"^(?=.{1,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9-]{2,63}$")


def clean(domain):
    d = (domain or "").strip().lower().rstrip(".")
    d = re.sub(r"^https?://", "", d).split("/")[0]
    if not d or d.startswith("_") or "*" in d:
        return None
    try:
        d = d.encode("idna").decode("ascii")
    except UnicodeError:
        return None
    if not DOMAIN_RE.match(d):
        return None
    return d


def read_text_list(text):
    out = []
    seen = set()
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        d = clean(line.split(",")[0]) if line else None
        if d and d not in seen:
            seen.add(d)
            out.append({"domain": d, "org": ""})
    return out


def parse_csv(text, column, org_column=None, suffix=None):
    out = []
    seen = set()
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return out
    header = [h.strip() for h in rows[0]]
    if column and column in header:
        ci = header.index(column)
        oi = header.index(org_column) if org_column and org_column in header else None
        body = rows[1:]
    else:
        ci, oi = 0, None
        body = rows[1:] if rows[0] and ":" in rows[0][0] else rows
    for row in body:
        if len(row) <= ci:
            continue
        d = clean(row[ci])
        if not d or d in seen:
            continue
        if suffix and not (d == suffix[1:] or d.endswith(suffix)):
            continue
        seen.add(d)
        org = row[oi].strip() if oi is not None and len(row) > oi else ""
        out.append({"domain": d, "org": org})
    return out


def uk_latest_url(client):
    data = client.get(UK_CONTENT_API).json()
    for a in data.get("details", {}).get("attachments", []):
        url = a.get("url", "")
        if url.lower().endswith(".csv"):
            return url, a.get("title", "")
    raise RuntimeError("no CSV attachment found on the GOV.UK publication")


def fetch_source(key, client=None):
    src = SOURCES[key]
    own = client is None
    client = client or httpx.Client(timeout=30, follow_redirects=True)
    try:
        url = src["url"]
        title = src["name"]
        if key == "uk":
            url, title = uk_latest_url(client)
        resp = client.get(url)
        resp.raise_for_status()
        text = resp.content.decode("utf-8-sig", errors="replace")
    finally:
        if own:
            client.close()
    entries = parse_csv(text, src["column"], src["org_column"], src["suffix"])
    return {
        "country": key,
        "name": src["name"],
        "publisher": src["publisher"],
        "source_url": url,
        "source_title": title,
        "entries": entries,
    }
