import asyncio
from datetime import datetime, timezone

import httpx
import respx

from disclosure_gap import scanner
from disclosure_gap.scanner import USER_AGENT, retry_after_seconds, scan

NOW = datetime(2026, 6, 1, tzinfo=timezone.utc)
GOOD = "Contact: mailto:security@a.gov\nExpires: 2026-12-01T00:00:00Z\n"


def run(domains, **kw):
    return asyncio.run(scan(domains, concurrency=4, timeout=2, host_interval=0, now=NOW, **kw))


@respx.mock
def test_well_known_found():
    route = respx.get("https://a.gov/.well-known/security.txt").mock(
        return_value=httpx.Response(200, text=GOOD, headers={"content-type": "text/plain"})
    )
    [r] = run(["a.gov"])
    assert r["result"] == "compliant"
    assert r["path"] == "/.well-known/security.txt"
    assert route.calls[0].request.headers["user-agent"] == USER_AGENT


@respx.mock
def test_fallback_to_legacy_path():
    respx.get("https://b.gov/.well-known/security.txt").mock(return_value=httpx.Response(404))
    respx.get("https://b.gov/security.txt").mock(
        return_value=httpx.Response(200, text="Contact: x\n", headers={"content-type": "text/plain"})
    )
    [r] = run(["b.gov"])
    assert r["result"] == "present"
    assert r["path"] == "/security.txt"


@respx.mock
def test_html_200_is_not_a_file():
    html = "<!doctype html><html><body>Not found</body></html>"
    respx.get("https://c.gov/.well-known/security.txt").mock(
        return_value=httpx.Response(200, text=html, headers={"content-type": "text/html"})
    )
    respx.get("https://c.gov/security.txt").mock(
        return_value=httpx.Response(200, text=html, headers={"content-type": "text/html"})
    )
    [r] = run(["c.gov"])
    assert r["result"] == "missing"
    assert r["html_200"]


@respx.mock
def test_unreachable():
    respx.get("https://d.gov/.well-known/security.txt").mock(side_effect=httpx.ConnectError("boom"))
    respx.get("https://d.gov/security.txt").mock(side_effect=httpx.ConnectError("boom"))
    [r] = run(["d.gov"])
    assert r["result"] == "unreachable"
    assert r["error"] == "connect"


@respx.mock
def test_timeout_classified():
    respx.get("https://t.gov/.well-known/security.txt").mock(side_effect=httpx.ReadTimeout("slow"))
    respx.get("https://t.gov/security.txt").mock(side_effect=httpx.ReadTimeout("slow"))
    [r] = run(["t.gov"])
    assert r["error"] == "timeout"
    assert respx.calls.call_count == 1


@respx.mock
def test_redirect_followed():
    respx.get("https://e.gov/.well-known/security.txt").mock(
        return_value=httpx.Response(301, headers={"location": "https://www.e.gov/.well-known/security.txt"})
    )
    respx.get("https://www.e.gov/.well-known/security.txt").mock(
        return_value=httpx.Response(200, text=GOOD, headers={"content-type": "text/plain"})
    )
    [r] = run(["e.gov"])
    assert r["result"] == "compliant"
    assert r["redirects"] == 1
    assert r["final_url"] == "https://www.e.gov/.well-known/security.txt"


@respx.mock
def test_too_many_redirects_stops():
    for i in range(6):
        respx.get(f"https://r.gov/{i}").mock(return_value=httpx.Response(302, headers={"location": f"https://r.gov/{i + 1}"}))
    respx.get("https://r.gov/.well-known/security.txt").mock(
        return_value=httpx.Response(302, headers={"location": "https://r.gov/0"})
    )
    respx.get("https://r.gov/security.txt").mock(return_value=httpx.Response(404))
    [r] = run(["r.gov"])
    assert r["result"] == "missing"
    assert respx.calls.call_count <= 6


@respx.mock
def test_retry_after_respected(monkeypatch):
    sleeps = []
    real_sleep = asyncio.sleep

    async def fake_sleep(s):
        sleeps.append(s)
        await real_sleep(0)

    monkeypatch.setattr(scanner.asyncio, "sleep", fake_sleep)
    respx.get("https://f.gov/.well-known/security.txt").mock(
        side_effect=[
            httpx.Response(429, headers={"retry-after": "3"}),
            httpx.Response(200, text=GOOD, headers={"content-type": "text/plain"}),
        ]
    )
    [r] = run(["f.gov"])
    assert r["result"] == "compliant"
    assert 3 in sleeps


def test_retry_after_parse():
    assert retry_after_seconds("5") == 5
    assert retry_after_seconds(None) is None
    assert retry_after_seconds("junk") is None


@respx.mock
def test_order_preserved():
    for d in ["x.gov", "y.gov", "z.gov"]:
        respx.get(f"https://{d}/.well-known/security.txt").mock(return_value=httpx.Response(404))
        respx.get(f"https://{d}/security.txt").mock(return_value=httpx.Response(404))
    rs = run(["z.gov", "x.gov", "y.gov"])
    assert [r["domain"] for r in rs] == ["z.gov", "x.gov", "y.gov"]
    assert all(r["result"] == "missing" for r in rs)
