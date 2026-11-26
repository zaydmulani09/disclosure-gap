import asyncio
import time
from datetime import datetime, timezone
from urllib.parse import urlsplit

import httpx

from . import __version__
from .parse import is_security_txt, looks_like_html, parse

REPO_URL = "https://github.com/zaydmulani09/disclosure-gap"
USER_AGENT = f"disclosure-gap/{__version__} (+{REPO_URL})"
PATHS = ("/.well-known/security.txt", "/security.txt")
MAX_BYTES = 64 * 1024
MAX_RETRY_AFTER = 60


class HostLimiter:
    def __init__(self, interval):
        self.interval = interval
        self.last = {}
        self.locks = {}

    async def wait(self, host):
        lock = self.locks.setdefault(host, asyncio.Lock())
        async with lock:
            gap = self.last.get(host, 0) + self.interval - time.monotonic()
            if gap > 0:
                await asyncio.sleep(gap)
            self.last[host] = time.monotonic()


def classify_error(exc):
    text = str(exc).lower()
    if isinstance(exc, httpx.TimeoutException):
        return "timeout"
    if isinstance(exc, httpx.TooManyRedirects):
        return "too_many_redirects"
    if "certificate" in text or "ssl" in text or "tls" in text:
        return "tls"
    if "getaddrinfo" in text or "name or service" in text or "nodename" in text or "no address" in text:
        return "dns"
    if isinstance(exc, httpx.ConnectError):
        return "connect"
    return type(exc).__name__.lower()


def retry_after_seconds(value):
    if not value:
        return None
    try:
        return max(0, int(value.strip()))
    except ValueError:
        pass
    try:
        from email.utils import parsedate_to_datetime

        dt = parsedate_to_datetime(value)
        return max(0, int((dt - datetime.now(timezone.utc)).total_seconds()))
    except (TypeError, ValueError):
        return None


async def fetch(client, limiter, url):
    host = urlsplit(url).hostname or ""
    for attempt in range(2):
        await limiter.wait(host)
        async with client.stream("GET", url) as resp:
            if resp.status_code in (429, 503) and attempt == 0:
                wait = retry_after_seconds(resp.headers.get("retry-after"))
                if wait is not None and wait <= MAX_RETRY_AFTER:
                    await asyncio.sleep(wait)
                    continue
            chunks = []
            size = 0
            if resp.status_code == 200:
                async for chunk in resp.aiter_bytes():
                    chunks.append(chunk)
                    size += len(chunk)
                    if size >= MAX_BYTES:
                        break
            body = b"".join(chunks)[:MAX_BYTES]
            return {
                "status": resp.status_code,
                "final_url": str(resp.url),
                "redirects": len(resp.history),
                "content_type": resp.headers.get("content-type", ""),
                "body": body.decode(resp.encoding or "utf-8", errors="replace") if body else "",
            }
    return None


def blank(domain):
    return {
        "domain": domain,
        "result": "missing",
        "path": None,
        "url": None,
        "final_url": None,
        "http_status": None,
        "content_type": None,
        "redirects": 0,
        "html_200": False,
        "error": None,
        "parsed": None,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


async def check_domain(client, limiter, domain, now=None):
    record = blank(domain)
    reached = False
    errors = []
    for path in PATHS:
        url = f"https://{domain}{path}"
        try:
            got = await fetch(client, limiter, url)
        except Exception as exc:
            errors.append(classify_error(exc))
            continue
        if got is None:
            continue
        reached = True
        if record["http_status"] is None or got["status"] == 200:
            record.update(
                url=url,
                final_url=got["final_url"],
                http_status=got["status"],
                content_type=got["content_type"],
                redirects=got["redirects"],
            )
        if got["status"] != 200:
            continue
        if looks_like_html(got["body"], got["content_type"]):
            record["html_200"] = True
            continue
        parsed = parse(got["body"], now=now, plain_http=got["final_url"].startswith("http://"))
        if not is_security_txt(parsed):
            continue
        record.update(
            result="compliant" if parsed.compliant else "present",
            path=path,
            parsed=parsed.to_dict(),
            html_200=False,
        )
        return record
    if not reached:
        record["result"] = "unreachable"
        record["error"] = errors[0] if errors else "unknown"
    return record


async def scan(domains, concurrency=8, timeout=10.0, host_interval=1.0, progress=None, now=None):
    limiter = HostLimiter(host_interval)
    sem = asyncio.Semaphore(concurrency)
    limits = httpx.Limits(max_connections=concurrency * 2, max_keepalive_connections=0)
    headers = {"User-Agent": USER_AGENT, "Accept": "text/plain, */*;q=0.1"}
    results = []
    async with httpx.AsyncClient(
        headers=headers,
        timeout=httpx.Timeout(timeout),
        follow_redirects=True,
        max_redirects=3,
        limits=limits,
    ) as client:

        async def one(d):
            async with sem:
                try:
                    r = await asyncio.wait_for(
                        check_domain(client, limiter, d, now=now), timeout * 8 + MAX_RETRY_AFTER * 2
                    )
                except asyncio.TimeoutError:
                    r = blank(d)
                    r.update(result="unreachable", error="timeout")
                results.append(r)
                if progress:
                    progress(len(results), len(domains))

        await asyncio.gather(*(one(d) for d in domains))
    order = {d: i for i, d in enumerate(domains)}
    results.sort(key=lambda r: order[r["domain"]])
    return results
