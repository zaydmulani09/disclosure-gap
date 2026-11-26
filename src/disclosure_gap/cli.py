import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .report import compare, load_scan, write_country, write_summary
from .scanner import USER_AGENT, scan
from .sources import SOURCES, fetch_source, read_text_list


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def progress_printer(label):
    def show(done, total):
        if done == total or done % 50 == 0:
            print(f"  {label}: {done}/{total}", file=sys.stderr, flush=True)

    return show


def run_scan(meta, args):
    entries = meta["entries"][: args.limit] if args.limit else meta["entries"]
    domains = [e["domain"] for e in entries]
    orgs = {e["domain"]: e.get("org", "") for e in entries}
    print(f"scanning {len(domains)} domains for {meta['name']}", file=sys.stderr)
    started = now_iso()
    results = asyncio.run(
        scan(
            domains,
            concurrency=args.concurrency,
            timeout=args.timeout,
            host_interval=args.host_interval,
            progress=progress_printer(meta["country"]),
        )
    )
    for r in results:
        r["org"] = orgs.get(r["domain"], "")
    out = {
        "country": meta["country"],
        "name": meta["name"],
        "publisher": meta.get("publisher", ""),
        "source_url": meta.get("source_url", ""),
        "source_title": meta.get("source_title", ""),
        "tool_version": __version__,
        "user_agent": USER_AGENT,
        "settings": {
            "concurrency": args.concurrency,
            "timeout": args.timeout,
            "host_interval": args.host_interval,
            "max_redirects": 3,
        },
        "started_at": started,
        "finished_at": now_iso(),
        "results": results,
    }
    folder = Path(args.out) / meta["country"]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "scan.json"
    path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {path}", file=sys.stderr)
    return path


def cmd_scan(args):
    metas = []
    if args.input:
        text = Path(args.input).read_text(encoding="utf-8-sig")
        label = args.label or Path(args.input).stem
        metas.append({"country": label, "name": args.name or label, "publisher": "local file",
                      "source_url": str(args.input), "entries": read_text_list(text)})
    keys = list(SOURCES) if args.all else (args.country or [])
    for k in keys:
        if k not in SOURCES:
            print(f"unknown country {k}, choose from {', '.join(SOURCES)}", file=sys.stderr)
            return 2
        metas.append(fetch_source(k))
    if not metas:
        print("nothing to scan: pass --input, --country or --all", file=sys.stderr)
        return 2
    for m in metas:
        run_scan(m, args)
    if not args.no_report:
        return cmd_report(argparse.Namespace(results=args.out, top=args.top))
    return 0


def cmd_report(args):
    root = Path(args.results)
    scans = sorted(root.glob("*/scan.json"))
    if not scans:
        print(f"no */scan.json under {root}", file=sys.stderr)
        return 1
    summaries = []
    for p in scans:
        s = write_country(load_scan(p), p.parent, top=args.top)
        summaries.append(s)
        print(f"{s['name']}: {s['with_file']}/{s['reachable']} reachable domains have security.txt "
              f"({s['adoption_pct_of_reachable']}%), {s['compliant']} pass core checks")
    write_summary(summaries, root)
    print(f"wrote {root / 'SUMMARY.md'}")
    return 0


def cmd_compare(args):
    print(compare([load_scan(p) for p in args.scans]))
    return 0


def cmd_sources(args):
    for k, v in SOURCES.items():
        print(f"{k}\t{v['name']}\t{v['publisher']}")
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="disclosure-gap", description="Check government domains for security.txt (RFC 9116).")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("scan", help="scan domains and write results")
    s.add_argument("--input", help="text file with one domain per line")
    s.add_argument("--label", help="folder name for --input results")
    s.add_argument("--name", help="display name for --input results")
    s.add_argument("--country", action="append", help=f"built-in list: {', '.join(SOURCES)} (repeatable)")
    s.add_argument("--all", action="store_true", help="scan every built-in list")
    s.add_argument("--out", default="results", help="output folder (default: results)")
    s.add_argument("--concurrency", type=int, default=8, help="parallel domains (default: 8)")
    s.add_argument("--timeout", type=float, default=10.0, help="request timeout in seconds (default: 10)")
    s.add_argument("--host-interval", type=float, default=1.0, help="minimum seconds between requests to one host (default: 1)")
    s.add_argument("--limit", type=int, help="only scan the first N domains of each list")
    s.add_argument("--top", type=int, default=100, help="missing domains listed in report.md (default: 100)")
    s.add_argument("--no-report", action="store_true", help="skip writing reports after the scan")
    s.set_defaults(func=cmd_scan)

    r = sub.add_parser("report", help="write JSON, CSV and Markdown reports from scan results")
    r.add_argument("results", nargs="?", default="results")
    r.add_argument("--top", type=int, default=100)
    r.set_defaults(func=cmd_report)

    c = sub.add_parser("compare", help="compare scan.json files side by side")
    c.add_argument("scans", nargs="+")
    c.set_defaults(func=cmd_compare)

    l = sub.add_parser("sources", help="list built-in domain lists")
    l.set_defaults(func=cmd_sources)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
