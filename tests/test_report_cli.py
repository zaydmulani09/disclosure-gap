import json

import httpx
import respx

from disclosure_gap import cli
from disclosure_gap.report import compare, ranked_missing, summarize
from disclosure_gap.sources import clean, parse_csv, read_text_list


def rec(domain, result, org="", parsed=None, path=None, error=None, html_200=False):
    return {"domain": domain, "org": org, "result": result, "parsed": parsed, "path": path,
            "error": error, "html_200": html_200, "http_status": 404 if result == "missing" else 200}


def good(**over):
    p = {"has_contact": True, "has_expires": True, "expires_valid": True, "expired": False,
         "expires_too_far": False, "has_canonical": False, "has_encryption": False,
         "has_policy": True, "has_languages": False, "signed": False, "expires": "2026-12-01T00:00:00Z",
         "contact": ["mailto:a@b"], "errors": []}
    p.update(over)
    return p


SCAN = {
    "country": "xx",
    "name": "Testland",
    "results": [
        rec("a.gov", "compliant", parsed=good(), path="/.well-known/security.txt"),
        rec("b.gov", "present", parsed=good(expired=True), path="/security.txt"),
        rec("c.gov", "missing", org="Dept A"),
        rec("d.gov", "missing", org="Dept B"),
        rec("e.gov", "missing", org="Dept B", html_200=True),
        rec("f.gov", "unreachable", error="dns"),
    ],
}


def test_summary_numbers():
    s = summarize(SCAN)
    assert s["total"] == 6
    assert s["reachable"] == 5
    assert s["with_file"] == 2
    assert s["compliant"] == 1
    assert s["adoption_pct_of_reachable"] == 40.0
    assert s["checks"]["expired"] == 1
    assert s["legacy_path_only"] == 1
    assert s["html_200_soft_404"] == 1
    assert s["unreachable_reasons"] == {"dns": 1}
    assert s["blocked_401_403_429"] == 0


def test_ranked_missing_groups_by_org():
    assert [r["domain"] for r in ranked_missing(SCAN)] == ["d.gov", "e.gov", "c.gov"]


def test_compare_same_country():
    later = json.loads(json.dumps(SCAN))
    later["results"][2] = rec("c.gov", "compliant", parsed=good())
    out = compare([SCAN, later])
    assert "Gained a file: 1" in out
    assert "+ c.gov" in out


def test_clean_and_lists():
    assert clean("HTTPS://Example.GOV/path") == "example.gov"
    assert clean("_dmarc.gov.uk") is None
    assert clean("*.gov.uk") is None
    assert [e["domain"] for e in read_text_list("a.gov\n# c\nb.gov\na.gov\n")] == ["a.gov", "b.gov"]
    uk = "Domain: Domain Name,\nfoo.gov.uk,\n_x.gov.uk,\nbar.gov.uk,\nnot-uk.com,\n"
    assert [e["domain"] for e in parse_csv(uk, None, None, ".gov.uk")] == ["foo.gov.uk", "bar.gov.uk"]
    us = "Domain name,Domain type,Organization name\nA.gov,Federal,Org A\n"
    assert parse_csv(us, "Domain name", "Organization name", ".gov") == [{"domain": "a.gov", "org": "Org A"}]


@respx.mock
def test_cli_scan_input_writes_reports(tmp_path, capsys):
    respx.get("https://a.gov/.well-known/security.txt").mock(
        return_value=httpx.Response(200, text="Contact: mailto:x@a.gov\nExpires: 2099-01-01T00:00:00Z\n",
                                    headers={"content-type": "text/plain"})
    )
    respx.get("https://b.gov/.well-known/security.txt").mock(return_value=httpx.Response(404))
    respx.get("https://b.gov/security.txt").mock(return_value=httpx.Response(404))
    f = tmp_path / "list.txt"
    f.write_text("a.gov\nb.gov\n")
    out = tmp_path / "res"
    rc = cli.main(["scan", "--input", str(f), "--label", "test", "--out", str(out), "--host-interval", "0"])
    assert rc == 0
    for name in ["scan.json", "summary.json", "results.csv", "report.md"]:
        assert (out / "test" / name).exists()
    assert (out / "SUMMARY.md").exists()
    s = json.loads((out / "test" / "summary.json").read_text())
    assert s["with_file"] == 1 and s["reachable"] == 2
    assert "b.gov" in (out / "test" / "report.md").read_text()
    rc = cli.main(["compare", str(out / "test" / "scan.json")])
    assert rc == 0
