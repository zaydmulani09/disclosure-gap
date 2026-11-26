import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta, timezone

KNOWN_FIELDS = {
    "acknowledgments",
    "canonical",
    "contact",
    "encryption",
    "expires",
    "hiring",
    "policy",
    "preferred-languages",
    "csaf",
}

PGP_BEGIN = "-----BEGIN PGP SIGNED MESSAGE-----"
PGP_SIG = "-----BEGIN PGP SIGNATURE-----"
FIELD_RE = re.compile(r"^([A-Za-z0-9-]+)\s*:\s*(.*)$")
HTML_RE = re.compile(r"<\s*(!doctype\s+html|html|head|body|script|meta|title)\b", re.I)


@dataclass
class Parsed:
    signed: bool = False
    fields: dict = field(default_factory=dict)
    unknown_fields: list = field(default_factory=list)
    contact: list = field(default_factory=list)
    expires: str | None = None
    expires_valid: bool = False
    expired: bool = False
    expires_too_far: bool = False
    multiple_expires: bool = False
    has_canonical: bool = False
    has_encryption: bool = False
    has_policy: bool = False
    has_languages: bool = False
    has_contact: bool = False
    has_expires: bool = False
    plain_http: bool = False
    meets_musts: bool = False
    compliant: bool = False
    errors: list = field(default_factory=list)

    def to_dict(self):
        return asdict(self)


def strip_pgp(text):
    if not text.lstrip().startswith(PGP_BEGIN):
        return text, False
    lines = text.lstrip().splitlines()
    i = 1
    while i < len(lines) and lines[i].strip():
        i += 1
    body = []
    for line in lines[i + 1:]:
        if line.strip() == PGP_SIG:
            break
        body.append(line[2:] if line.startswith("- ") else line)
    return "\n".join(body), True


def parse_datetime(value):
    v = value.strip()
    if v.endswith("Z") or v.endswith("z"):
        v = v[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(v)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return None
    return dt


def looks_like_html(text, content_type=""):
    if "html" in (content_type or "").lower():
        return True
    head = text[:4096]
    return bool(HTML_RE.search(head))


def parse(text, now=None, plain_http=False):
    now = now or datetime.now(timezone.utc)
    body, signed = strip_pgp(text)
    p = Parsed(signed=signed, plain_http=plain_http)
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = FIELD_RE.match(line)
        if not m:
            p.errors.append(f"unparsable line: {line[:80]}")
            continue
        name = m.group(1).lower()
        value = m.group(2).strip()
        if name not in KNOWN_FIELDS:
            p.unknown_fields.append(name)
            continue
        p.fields.setdefault(name, []).append(value)
    p.contact = p.fields.get("contact", [])
    p.has_contact = bool(p.contact)
    expires = p.fields.get("expires", [])
    p.has_expires = bool(expires)
    p.multiple_expires = len(expires) > 1
    if expires:
        p.expires = expires[0]
        dt = parse_datetime(expires[0])
        if dt is None:
            p.errors.append("expires is not a valid RFC 3339 date-time")
        else:
            p.expires_valid = True
            p.expired = dt <= now
            p.expires_too_far = dt > now + timedelta(days=366)
    p.has_canonical = "canonical" in p.fields
    p.has_encryption = "encryption" in p.fields
    p.has_policy = "policy" in p.fields
    p.has_languages = "preferred-languages" in p.fields
    if not p.has_contact:
        p.errors.append("missing Contact")
    if not p.has_expires:
        p.errors.append("missing Expires")
    if p.multiple_expires:
        p.errors.append("Expires appears more than once")
    if p.expired:
        p.errors.append("Expires is in the past")
    if p.expires_too_far:
        p.errors.append("Expires is more than a year away")
    if p.plain_http:
        p.errors.append("served over plain HTTP after a redirect")
    p.meets_musts = (
        p.has_contact
        and p.expires_valid
        and not p.expired
        and not p.multiple_expires
        and not p.plain_http
    )
    p.compliant = p.meets_musts and not p.expires_too_far
    return p


def is_security_txt(parsed):
    return bool(parsed.fields)
