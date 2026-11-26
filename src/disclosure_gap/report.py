import csv
import json
from collections import Counter
from pathlib import Path

CHECKS = [
    ("has_contact", "Contact present"),
    ("has_expires", "Expires present"),
    ("expires_valid", "Expires is a valid date"),
    ("expired", "Expires in the past"),
    ("expires_too_far", "Expires more than a year away"),
    ("plain_http", "Served over plain HTTP after a redirect"),
    ("meets_musts", "Meets RFC 9116 MUSTs"),
    ("has_canonical", "Canonical"),
    ("has_encryption", "Encryption"),
    ("has_policy", "Policy"),
    ("has_languages", "Preferred-Languages"),
    ("signed", "PGP signed"),
]

CSV_FIELDS = [
    "domain",
    "org",
    "result",
    "path",
    "http_status",
    "final_url",
    "content_type",
    "html_200",
    "error",
    "has_contact",
    "has_expires",
    "expires",
    "expired",
    "expires_too_far",
    "has_canonical",
    "has_encryption",
    "has_policy",
    "has_languages",
    "signed",
    "contact",
    "problems",
]


def pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def summarize(scan):
    rows = scan["results"]
    total = len(rows)
    by = Counter(r["result"] for r in rows)
    unreachable = by["unreachable"]
    reachable = total - unreachable
    with_file = by["present"] + by["compliant"]
    files = [r for r in rows if r["result"] in ("present", "compliant")]
    checks = {k: sum(1 for r in files if r["parsed"].get(k)) for k, _ in CHECKS}
    legacy = sum(1 for r in files if r["path"] == "/security.txt")
    blocked = sum(1 for r in rows if r["result"] == "missing" and r.get("http_status") in (401, 403, 429, 451))
    html_200 = sum(1 for r in rows if r["result"] == "missing" and r.get("html_200"))
    errors = Counter(r.get("error") or "unknown" for r in rows if r["result"] == "unreachable")
    return {
        "country": scan["country"],
        "name": scan["name"],
        "total": total,
        "reachable": reachable,
        "unreachable": unreachable,
        "unreachable_reasons": dict(errors.most_common()),
        "with_file": with_file,
        "compliant": by["compliant"],
        "missing": by["missing"],
        "html_200_soft_404": html_200,
        "blocked_401_403_429": blocked,
        "adoption_pct_excluding_blocked": pct(with_file, reachable - blocked),
        "legacy_path_only": legacy,
        "adoption_pct_of_reachable": pct(with_file, reachable),
        "adoption_pct_of_total": pct(with_file, total),
        "compliant_pct_of_files": pct(by["compliant"], with_file),
        "compliant_pct_of_reachable": pct(by["compliant"], reachable),
        "checks": checks,
        "started_at": scan.get("started_at"),
        "finished_at": scan.get("finished_at"),
    }


def ranked_missing(scan):
    missing = [r for r in scan["results"] if r["result"] == "missing"]
    org_counts = Counter(r.get("org") or "" for r in missing)

    def key(r):
        org = r.get("org") or ""
        return (-(org_counts[org] if org else 0), org.lower(), len(r["domain"].split(".")), r["domain"])

    return sorted(missing, key=key)


def flat(r):
    p = r.get("parsed") or {}
    return {
        "domain": r["domain"],
        "org": r.get("org", ""),
        "result": r["result"],
        "path": r.get("path") or "",
        "http_status": r.get("http_status") or "",
        "final_url": r.get("final_url") or "",
        "content_type": r.get("content_type") or "",
        "html_200": bool(r.get("html_200")),
        "error": r.get("error") or "",
        "has_contact": bool(p.get("has_contact")),
        "has_expires": bool(p.get("has_expires")),
        "expires": p.get("expires") or "",
        "expired": bool(p.get("expired")),
        "expires_too_far": bool(p.get("expires_too_far")),
        "has_canonical": bool(p.get("has_canonical")),
        "has_encryption": bool(p.get("has_encryption")),
        "has_policy": bool(p.get("has_policy")),
        "has_languages": bool(p.get("has_languages")),
        "signed": bool(p.get("signed")),
        "contact": " | ".join(p.get("contact") or []),
        "problems": " | ".join(p.get("errors") or []),
    }


def md_escape(s):
    return str(s).replace("|", "\\|")


def render_markdown(scan, s, top=100):
    lines = []
    lines.append(f"# security.txt report: {s['name']}")
    lines.append("")
    lines.append(f"Source list: {scan.get('publisher', '')}  ")
    lines.append(f"List URL: {scan.get('source_url', '')}  ")
    lines.append(f"Scan window: {s['started_at']} to {s['finished_at']} (UTC)  ")
    lines.append(f"Tool: disclosure-gap {scan.get('tool_version', '')}")
    lines.append("")
    lines.append("## Headline")
    lines.append("")
    lines.append(
        f"**{s['adoption_pct_of_reachable']}%** of reachable domains publish a security.txt file "
        f"({s['with_file']} of {s['reachable']}). "
        f"**{s['compliant_pct_of_reachable']}%** publish one that passes the core RFC 9116 checks "
        f"({s['compliant']} of {s['reachable']})."
    )
    lines.append("")
    lines.append("| Metric | Count | Share |")
    lines.append("| --- | ---: | ---: |")
    lines.append(f"| Domains in list | {s['total']} | |")
    lines.append(f"| Reachable over HTTPS | {s['reachable']} | {pct(s['reachable'], s['total'])}% of list |")
    lines.append(f"| Unreachable | {s['unreachable']} | {pct(s['unreachable'], s['total'])}% of list |")
    lines.append(f"| security.txt found | {s['with_file']} | {s['adoption_pct_of_reachable']}% of reachable |")
    lines.append(f"| Passes core RFC 9116 checks | {s['compliant']} | {s['compliant_pct_of_files']}% of files |")
    lines.append(f"| No file | {s['missing']} | {pct(s['missing'], s['reachable'])}% of reachable |")
    lines.append(f"| HTML page served with 200 instead of a file | {s['html_200_soft_404']} | |")
    lines.append(f"| Request refused (401, 403, 429 or 451) | {s['blocked_401_403_429']} | |")
    lines.append(f"| Adoption if refused requests are left out | | {s['adoption_pct_excluding_blocked']}% |")
    lines.append(f"| File only at legacy /security.txt | {s['legacy_path_only']} | |")
    lines.append("")
    lines.append("Core checks: Contact present, exactly one Expires that is a valid date, not in the past and not more than a year away, file served over HTTPS. "
                 "The one year limit is a RFC 9116 recommendation; the rest are MUSTs. The breakdown below shows each check on its own.")
    lines.append("")
    lines.append("## Compliance breakdown (domains with a file)")
    lines.append("")
    lines.append("| Field or check | Count | Share of files |")
    lines.append("| --- | ---: | ---: |")
    for k, label in CHECKS:
        lines.append(f"| {label} | {s['checks'][k]} | {pct(s['checks'][k], s['with_file'])}% |")
    lines.append("")
    expired = [r for r in scan["results"] if r.get("parsed") and r["parsed"].get("expired")]
    lines.append(f"## Expired files ({len(expired)})")
    lines.append("")
    if expired:
        lines.append("| Domain | Expires |")
        lines.append("| --- | --- |")
        for r in sorted(expired, key=lambda r: r["parsed"].get("expires") or ""):
            lines.append(f"| {r['domain']} | {md_escape(r['parsed'].get('expires'))} |")
    else:
        lines.append("None.")
    lines.append("")
    missing = ranked_missing(scan)
    lines.append(f"## Domains missing a file ({len(missing)})")
    lines.append("")
    lines.append(
        "Reachable domains with no security.txt. Ranked by how many domains the same organization "
        "is missing, then by domain depth, so the largest gaps and top level sites come first."
    )
    if len(missing) > top:
        lines.append(f"Showing the first {top}. The full list is in results.csv.")
    lines.append("")
    if missing:
        lines.append("| # | Domain | Organization | HTTP status |")
        lines.append("| ---: | --- | --- | ---: |")
        for i, r in enumerate(missing[:top], 1):
            lines.append(f"| {i} | {r['domain']} | {md_escape(r.get('org') or '')} | {r.get('http_status') or ''} |")
    lines.append("")
    if s["unreachable_reasons"]:
        lines.append("## Unreachable domains by reason")
        lines.append("")
        lines.append("| Reason | Count |")
        lines.append("| --- | ---: |")
        for k, v in s["unreachable_reasons"].items():
            lines.append(f"| {k} | {v} |")
        lines.append("")
    return "\n".join(lines)


def summary_table(summaries):
    lines = []
    lines.append("| Country | Domains | Reachable | With security.txt | Adoption (reachable) | Meets RFC MUSTs | Passing core checks | Expired | HTML 200 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for s in summaries:
        lines.append(
            f"| {s['name']} | {s['total']} | {s['reachable']} | {s['with_file']} | "
            f"{s['adoption_pct_of_reachable']}% | {s['checks']['meets_musts']} | {s['compliant']} ({s['compliant_pct_of_reachable']}%) | "
            f"{s['checks']['expired']} | {s['html_200_soft_404']} |"
        )
    return "\n".join(lines)


def load_scan(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_country(scan, outdir, top=100):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    s = summarize(scan)
    (outdir / "summary.json").write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
    with open(outdir / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for r in scan["results"]:
            w.writerow(flat(r))
    (outdir / "report.md").write_text(render_markdown(scan, s, top=top) + "\n", encoding="utf-8")
    return s


def write_summary(summaries, outdir):
    outdir = Path(outdir)
    text = ["# disclosure-gap summary", "", summary_table(summaries), ""]
    text.append("Adoption is the share of domains that answered over HTTPS and served a security.txt file. "
                "Passing core checks means Contact present, a single valid Expires that is not past and not more than a year away, and the file served over HTTPS.")
    text.append("")
    (outdir / "SUMMARY.md").write_text("\n".join(text), encoding="utf-8")
    (outdir / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n", encoding="utf-8")


def compare(scans):
    summaries = [summarize(s) for s in scans]
    out = [summary_table(summaries)]
    if len(scans) == 2 and scans[0]["country"] == scans[1]["country"]:
        a = {r["domain"]: r["result"] for r in scans[0]["results"]}
        b = {r["domain"]: r["result"] for r in scans[1]["results"]}
        has = {"present", "compliant"}
        gained = sorted(d for d in b if b[d] in has and a.get(d) not in has and d in a)
        lost = sorted(d for d in a if a[d] in has and b.get(d) not in has and d in b)
        out.append("")
        out.append(f"Gained a file: {len(gained)}")
        out.extend(f"  + {d}" for d in gained)
        out.append(f"Lost a file: {len(lost)}")
        out.extend(f"  - {d}" for d in lost)
    return "\n".join(out)
