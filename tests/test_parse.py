from datetime import datetime, timezone

from disclosure_gap.parse import looks_like_html, parse, strip_pgp

NOW = datetime(2026, 6, 1, tzinfo=timezone.utc)

GOOD = """# hello
Contact: mailto:security@example.gov
Contact: https://example.gov/report
Expires: 2026-12-31T23:00:00.000Z
Encryption: https://example.gov/pgp.txt
Canonical: https://example.gov/.well-known/security.txt
Policy: https://example.gov/vdp
Preferred-Languages: en, fr
"""

SIGNED = """-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

Contact: mailto:security@example.gov
Expires: 2026-09-01T00:00:00Z
- -dash escaped comment
-----BEGIN PGP SIGNATURE-----

iQIzBAEBCAAdFiEE
-----END PGP SIGNATURE-----
"""


def test_good_file_is_compliant():
    p = parse(GOOD, now=NOW)
    assert p.compliant
    assert p.contact == ["mailto:security@example.gov", "https://example.gov/report"]
    assert p.has_canonical and p.has_encryption and p.has_policy and p.has_languages
    assert not p.signed
    assert p.errors == []


def test_expired():
    p = parse("Contact: mailto:a@b.gov\nExpires: 2025-01-01T00:00:00Z\n", now=NOW)
    assert p.expired
    assert not p.compliant


def test_too_far():
    p = parse("Contact: mailto:a@b.gov\nExpires: 2030-01-01T00:00:00Z\n", now=NOW)
    assert p.expires_too_far
    assert not p.compliant


def test_missing_expires_and_contact():
    p = parse("Policy: https://x.gov\n", now=NOW)
    assert not p.has_contact and not p.has_expires
    assert "missing Contact" in p.errors
    assert "missing Expires" in p.errors


def test_bad_date_and_no_timezone():
    assert not parse("Contact: x\nExpires: tomorrow\n", now=NOW).expires_valid
    assert not parse("Contact: x\nExpires: 2026-07-01T00:00:00\n", now=NOW).expires_valid


def test_multiple_expires():
    p = parse("Contact: x\nExpires: 2026-07-01T00:00:00Z\nExpires: 2026-08-01T00:00:00Z\n", now=NOW)
    assert p.multiple_expires
    assert not p.compliant


def test_case_insensitive_fields():
    p = parse("CONTACT: mailto:a@b.gov\nexpires: 2026-07-01T00:00:00+02:00\n", now=NOW)
    assert p.compliant


def test_pgp_signed():
    body, signed = strip_pgp(SIGNED)
    assert signed
    assert "-dash escaped comment" in body
    assert "SIGNATURE" not in body
    p = parse(SIGNED, now=NOW)
    assert p.signed and p.compliant


def test_html_detection():
    assert looks_like_html("<!DOCTYPE html><html><body>nope</body></html>")
    assert looks_like_html("whatever", "text/html; charset=utf-8")
    assert not looks_like_html(GOOD, "text/plain")


def test_unknown_fields_kept_separately():
    p = parse("Contact: x\nFoo: bar\n", now=NOW)
    assert p.unknown_fields == ["foo"]


def test_plain_http_fails_musts():
    p = parse("Contact: x\nExpires: 2026-07-01T00:00:00Z\n", now=NOW, plain_http=True)
    assert p.plain_http and not p.meets_musts and not p.compliant


def test_too_far_still_meets_musts():
    p = parse("Contact: x\nExpires: 2030-01-01T00:00:00Z\n", now=NOW)
    assert p.meets_musts and not p.compliant
