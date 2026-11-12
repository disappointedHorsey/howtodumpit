#!/usr/bin/env python3
"""Tiny static site generator: content/**/*.md (YAML front matter) -> public/.
Usage: .venv/bin/python build.py   (or ./build.sh)"""
import datetime, difflib, html, json, math, pathlib, re, shutil, string, urllib.parse
import markdown, yaml

ROOT = pathlib.Path(__file__).parent
CONTENT, OUT, TPL, STATIC = ROOT/"content", ROOT/"public", ROOT/"templates", ROOT/"static"
CFG = yaml.safe_load((ROOT/"site.yaml").read_text())
# Path prefix for hosting under a subpath (e.g. GitHub Pages project site); "" at a domain root.
PREFIX = urllib.parse.urlparse(CFG["base_url"]).path.rstrip("/")

# Full state names for breadcrumbs and the home-page city directory.
STATE_NAMES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DC": "District of Columbia",
    "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "IA": "Iowa", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "MA": "Massachusetts",
    "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota",
    "MO": "Missouri", "MS": "Mississippi", "MT": "Montana", "NC": "North Carolina",
    "ND": "North Dakota", "NE": "Nebraska", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NV": "Nevada", "NY": "New York", "OH": "Ohio",
    "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VA": "Virginia", "VT": "Vermont", "WA": "Washington",
    "WI": "Wisconsin", "WV": "West Virginia", "WY": "Wyoming",
}

# Approximate city-center coordinates (degrees) used only to pick the closest
# existing city guides for the Nearby Cities block. New cities can set `lat`
# and `lon` in front matter, or add a slug here. Values are standard city-center
# points, rounded to 4 decimal places.
CITY_COORDS = {
    "albuquerque-nm": (35.0844, -106.6504),
    "atlanta-ga": (33.7490, -84.3880),
    "austin-tx": (30.2672, -97.7431),
    "baltimore-md": (39.2904, -76.6122),
    "boston-ma": (42.3601, -71.0589),
    "cambridge-somerville-ma": (42.3736, -71.1097),
    "charlotte-nc": (35.2271, -80.8431),
    "chicago-il": (41.8781, -87.6298),
    "colorado-springs-co": (38.8339, -104.8214),
    "columbus-oh": (39.9612, -82.9988),
    "dallas-tx": (32.7767, -96.7970),
    "denver-co": (39.7392, -104.9903),
    "detroit-mi": (42.3314, -83.0458),
    "el-paso-tx": (31.7619, -106.4850),
    "fort-worth-tx": (32.7555, -97.3308),
    "fresno-ca": (36.7378, -119.7871),
    "houston-tx": (29.7604, -95.3698),
    "indianapolis-in": (39.7684, -86.1581),
    "jacksonville-fl": (30.3322, -81.6557),
    "kansas-city-mo": (39.0997, -94.5783),
    "las-vegas-nv": (36.1699, -115.1398),
    "los-angeles-ca": (34.0522, -118.2437),
    "louisville-ky": (38.2527, -85.7585),
    "memphis-tn": (35.1495, -90.0490),
    "mesa-az": (33.4152, -111.8315),
    "miami-fl": (25.7617, -80.1918),
    "milwaukee-wi": (43.0389, -87.9065),
    "nashville-tn": (36.1627, -86.7816),
    "new-york-ny": (40.7128, -74.0060),
    "oklahoma-city-ok": (35.4676, -97.5164),
    "omaha-ne": (41.2565, -95.9345),
    "philadelphia-pa": (39.9526, -75.1652),
    "phoenix-az": (33.4484, -112.0740),
    "portland-or": (45.5152, -122.6784),
    "raleigh-nc": (35.7796, -78.6382),
    "sacramento-ca": (38.5816, -121.4944),
    "san-antonio-tx": (29.4241, -98.4936),
    "san-diego-ca": (32.7157, -117.1611),
    "san-francisco-ca": (37.7749, -122.4194),
    "san-jose-ca": (37.3382, -121.8863),
    "seattle-wa": (47.6062, -122.3321),
    "tucson-az": (32.2226, -110.9747),
    "virginia-beach-va": (36.8529, -75.9780),
    "long-beach-ca": (33.7701, -118.1937),
    "washington-dc": (38.9072, -77.0369),
}
NEARBY_COUNT = 5

def _coords(slug, meta):
    """Return (lat, lon) from front matter, or the built-in table."""
    if meta.get("lat") is not None and meta.get("lon") is not None:
        try:
            return float(meta["lat"]), float(meta["lon"])
        except (TypeError, ValueError):
            pass
    return CITY_COORDS.get(slug)

def _haversine_km(a, b):
    lat1, lon1 = a
    lat2, lon2 = b
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(h), math.sqrt(1 - h))

def _slugify(s):
    s = html.unescape(str(s)).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "partner"

def _click_attr(name):
    return f' data-goatcounter-click="{html.escape(name, quote=True)}"'


def prefix_links(s):
    """Prepend PREFIX to root-relative href/src attributes (not protocol-relative //)."""
    return re.sub(r'(href|src)="/(?!/)', rf'\1="{PREFIX}/', s) if PREFIX else s

def load(p):
    raw = p.read_text()
    meta, body = {}, raw
    if raw.startswith("---"):
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    return meta, body

def url_for(p):
    rel = p.relative_to(CONTENT).with_suffix("")
    if rel.name == "index":
        rel = rel.parent
    return "/" + (str(rel).strip(".") + "/" if str(rel) != "." else "")

def us_date(v):
    """Format a verified date (YAML date or 'YYYY-MM-DD' string) as a US date, e.g. October 20, 2026."""
    try:
        d = v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v).strip())
    except ValueError:
        return str(v)
    return f"{d:%B} {d.day}, {d.year}"

def listings_html(items, heading="Options at a Glance"):
    if not items: return ""
    rows = []
    for it in items:
        src = f' <a class="src" href="{html.escape(it["source"])}" rel="nofollow">source</a>' if it.get("source") else ""
        rows.append(f'<li class="listing"><h3>{html.escape(it["name"])}</h3>'
                    f'<p><strong>Cost:</strong> {html.escape(str(it.get("cost","-")))} &middot; '
                    f'<strong>Type:</strong> {html.escape(it.get("type",""))}</p>'
                    f'<p>{html.escape(it.get("details",""))}{src}</p></li>')
    return f'<h3>{html.escape(heading)}</h3><ul class="listings">' + "".join(rows) + "</ul>"

# Partner tier cards (Basic / Verified / Recommended). Separate from official drop-off `listings:`.
# Internal key `featured` is kept as an alias of Recommended (C019, Adam 07/11/2026).
PARTNER_TIER_ORDER = {"featured": 0, "recommended": 0, "verified": 1, "basic": 2}
PARTNER_DISCLAIMER = (
    'These partners are independent businesses. HowToDumpIt is an independent information guide '
    'and does not haul anything or vouch for their work. Confirm pricing, licensing and reviews '
    'with them before you hire.'
)
RECOMMENDED_DISCLOSURE = (
    'Paid placement. We receive referral fees from this partner.'
)

def _tel_href(phone):
    """Build a tel: href from a display phone string (digits and leading + only)."""
    s = str(phone).strip()
    digits = re.sub(r"[^0-9+]", "", s)
    if digits.startswith("+"):
        return "tel:" + "+" + re.sub(r"[^0-9]", "", digits[1:])
    return "tel:" + re.sub(r"[^0-9]", "", digits)

def _website_label(url):
    """Prefer host+path so two partners on the same domain keep unique link text."""
    try:
        u = urllib.parse.urlparse(url)
        host = (u.netloc or "").removeprefix("www.")
        path = (u.path or "").rstrip("/")
        if host and path:
            return host + path
        if host:
            return host
    except Exception:
        pass
    return url

def partners_html(items, city_slug=""):
    """Render Local Junk Removal & Donation Partners from front-matter `partners:`.

    Paid tiers (Recommended, Verified Partner) are large prominent cards and sort first.
    Free Basic Listings (companies and charities) are compact secondary "after runs"
    below any paid cards (Adam, 11/10/2026). Official drop-off `listings:` are unchanged.
    Paid tiers get a clickable website link (rel="sponsored nofollow"). Unreplied /
    free compact rows show only the name, a clickable phone number, and the
    "Not verified" label. They never show a website, not even as plain text
    (Adam, 11/11/2026; company 1c7ae6d). A website or ordinary note may stay
    in the YAML as a source record; they are not rendered on free compact rows.
    Exception: if `approved_wording` is set (a partner approved exact public
    copy, e.g. a free nonprofit city partner), that exact text is rendered on
    the free row. The row stays labeled Not verified and still never shows a
    website (Adam, 12/11/2026, Blue Star Recyclers).
    The section is inserted near the top of the city guide, just before the
    Mattresses heading. Returns an empty string when there are no partners, so
    cities with no listings get no empty box (Adam, 11/11/2026).
    """
    if not items: return ""
    ordered = sorted(
        items,
        key=lambda it: (PARTNER_TIER_ORDER.get(str(it.get("tier", "basic")).lower(), 99),
                        str(it.get("name", "")).lower()))
    paid, free = [], []
    for it in ordered:
        tier = str(it.get("tier", "basic")).lower().strip()
        if tier not in PARTNER_TIER_ORDER:
            tier = "basic"
        name = html.escape(str(it.get("name", "")).strip())
        phone = str(it.get("phone") or "").strip()
        website = str(it.get("website") or "").strip()
        note = str(it.get("note") or "").strip()
        checked = it.get("source_checked")
        if tier in ("featured", "recommended"):
            public_tier = "recommended"
        else:
            public_tier = tier
        classes = f"partner partner-{public_tier}"
        badge = ""
        if public_tier == "recommended":
            # Exclusive top spot: Recommended label + nearby paid-placement disclosure (FTC).
            # No verification wording on paid listings (Adam 07/11/2026).
            badge = (
                '<p class="partner-badge"><span class="partner-recommended-label">Recommended</span></p>'
                '<p class="partner-exclusive">Exclusive top spot for this city.</p>'
                f'<p class="partner-paid-disclosure">{RECOMMENDED_DISCLOSURE}</p>'
            )
        elif public_tier == "basic":
            badge = '<p class="partner-badge"><span class="partner-unverified-label">Not verified</span></p>'
        bits = [f'<li class="{classes}">{badge}<h3>{name}</h3>']
        if public_tier in ("verified", "recommended"):
            slug = _slugify(it.get("name") or "partner")
            if phone:
                tel = html.escape(_tel_href(phone), quote=True)
                phone_esc = html.escape(phone)
                # Phone as plain text; Call Now is the single tel: link (avoids dup-href).
                bits.append(f'<p class="partner-phone">{phone_esc}</p>')
                ev = f"tel-{city_slug}-{slug}" if city_slug else f"tel-{slug}"
                bits.append(f'<p class="partner-cta"><a class="btn" href="{tel}"{_click_attr(ev)}>Call Now</a></p>')
            if website:
                href = html.escape(website, quote=True)
                label = html.escape(_website_label(website))
                ev = f"web-{city_slug}-{slug}" if city_slug else f"web-{slug}"
                bits.append(f'<p class="partner-web"><a href="{href}" rel="sponsored nofollow" target="_blank"{_click_attr(ev)}>{label}</a></p>')
        else:
            meta = []
            slug = _slugify(it.get("name") or "partner")
            if phone:
                tel = html.escape(_tel_href(phone), quote=True)
                phone_esc = html.escape(phone)
                ev = f"tel-{city_slug}-{slug}" if city_slug else f"tel-{slug}"
                meta.append(f'<span class="partner-phone"><a href="{tel}"{_click_attr(ev)}>{phone_esc}</a></span>')
            # Free compact rows never show a website, not even as plain text.
            if meta:
                sep = '<span class="partner-meta-sep" aria-hidden="true"> · </span>'
                bits.append('<p class="partner-meta">' + sep.join(meta) + "</p>")
            approved = str(it.get("approved_wording") or "").strip()
            if approved:
                bits.append(
                    f'<p class="partner-note partner-approved-wording">{html.escape(approved)}</p>'
                )
        if public_tier in ("verified", "recommended"):
            if note:
                bits.append(f'<p class="partner-note">{html.escape(note)}</p>')
            if checked:
                bits.append(f'<p class="partner-checked">Checked {html.escape(us_date(checked))}</p>')
        bits.append("</li>")
        row = "".join(bits)
        if public_tier in ("verified", "recommended"):
            paid.append(row)
        else:
            free.append(row)
    lists = ""
    if paid:
        lists += '<ul class="partners-list partners-list-paid">' + "".join(paid) + "</ul>"
    if free:
        lists += '<ul class="partners-list partners-list-free">' + "".join(free) + "</ul>"
    return (
        '<section class="partners" aria-labelledby="partners-h">'
        '<h2 id="partners-h">Local Junk Removal &amp; Donation Partners</h2>'
        f'<p class="partner-disclaimer">{PARTNER_DISCLAIMER}</p>'
        + lists + "</section>"
    )


# Modest end-of-guide mention only. No href, button, box, heading or color
# block. Plain text because there is no tracked affiliate tag (Adam, 11/11/2026).
NATIONAL_NOTE = (
    '<p class="national-note">Prefer a national company? '
    '1-800-GOT-JUNK and LoadUp also serve this area.</p>'
)

A_TAG = re.compile(r'(\s?)<a\b([^>]*?)href="([^"]+)"([^>]*)>(.*?)</a>', re.S)

def dedupe_links(body_html):
    """Comms rule: link each target once per section (h2 to next h2).
    A repeat link to the same page in the same section becomes plain text; a repeat citation
    in brackets, e.g. "(City of X: Trash)", or a repeat listing "source" link is dropped.
    Keeps pages free of duplicate links for nightly guides too."""
    parts = re.split(r'(?=<h2[\s>])', body_html)
    out = []
    for part in parts:
        seen = set()
        def fix(m):
            sp, pre, href, post, text = m.groups()
            k = href.split("#")[0].rstrip("/") if not href.startswith("#") else href
            if k not in seen:
                seen.add(k); return m.group(0)
            if re.sub(r"<[^>]+>", "", text).strip().lower() == "source":
                return ""
            return sp + "\x00" + text.replace("(", "\x03").replace(")", "\x04") + "\x01"
        part = A_TAG.sub(fix, part)
        def paren(pm):
            inner = pm.group(1)
            inner = re.sub(r"(,|;| and)\s*\x00[^\x00\x01]*\x01", "", inner)
            inner = re.sub(r"^\s*\x00[^\x00\x01]*\x01\s*(,|;|and)\s*", "", inner)
            if re.fullmatch(r"\s*\x00[^\x00\x01]*\x01\s*", inner): return "\x02"
            return "(" + inner + ")"
        part = re.sub(r"\(([^()]*\x00[^()]*)\)", paren, part)
        part = re.sub(r"\s*\x02", "", part)
        part = part.replace("\x00", "").replace("\x01", "").replace("\x03", "(").replace("\x04", ")")
        out.append(part)
    return "".join(out)

def _skey(x):
    return " ".join(re.sub(r"[^a-z0-9$ ]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x)).lower()).split())

def _sents(x):
    return [t for t in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(])", x) if t.strip()]

def trim_listing_repeats(body_html):
    """Comms rule: say each thing once. A listing card sentence that the guide text below
    already says word for word is dropped from the card (name, cost, type and source stay)."""
    m = re.search(r'<ul class="listings">.*?</ul>', body_html, re.S)
    if not m: return body_html
    rest = body_html[:m.start()] + body_html[m.end():]
    rest_text = re.sub(r"<[^>]+>", " ", rest)
    rest_keys = {_skey(t) for blk in re.split(r"\n|  +", rest_text) for t in _sents(blk)}
    rest_keys |= {_skey(t) for t in _sents(" ".join(rest_text.split()))}
    seen = set()
    def fix_p(pm):
        inner, src = pm.group(1), pm.group(2) or ""
        keep = []
        for t in _sents(inner):
            k = _skey(t)
            if len(k.split()) >= 4 and (k in rest_keys or k in seen or any(
                    difflib.SequenceMatcher(None, k.split(), r.split(), autojunk=False).ratio() >= 0.85
                    for r in rest_keys if abs(len(r) - len(k)) < len(k) * 0.4)): continue
            seen.add(k); keep.append(t)
        txt = " ".join(keep)
        if not txt and not src: return ""
        return "<p>" + txt + src + "</p>"
    ul = re.sub(r'<p>((?:(?!<strong>Cost).)*?)( <a class="src"[^>]*>source</a>)?</p>', fix_p, m.group(0))
    return body_html[:m.start()] + ul + body_html[m.end():]

# Residents and towns asking for a new city guide (home page and the end of every city guide).
# Haulers have their own route (Become a Recommended Partner), so this box never mentions listings for businesses.
CITY_REQUEST = (
    '<aside class="callout" aria-labelledby="ask-h"><h2 id="ask-h">Want Your City or Town Listed?</h2>'
    '<p>Just drop me a message at <a href="mailto:adam@howtodumpit.com">adam@howtodumpit.com</a>. '
    'I read and answer all emails!</p></aside>')

def mark_current(out, u):
    """Nav and footer links to the page you're on get aria-current="page" (no silent self-links)."""
    def fix(m):
        block = m.group(0)
        return block.replace(f'<a href="{u}">', f'<a href="{u}" aria-current="page">')
    return re.sub(r'<(nav aria-label="Main"|footer).*?</(nav|footer)>', fix, out, flags=re.S)

def crumbs(u, title, titles, city_meta=None):
    """Visible breadcrumb trail. City guides use Home › State › City (state is
    plain text: there is no state landing page). Other pages stay path-based."""
    if city_meta and city_meta.get("city"):
        state_abbr = str(city_meta.get("state") or "").strip()
        state_name = html.escape(STATE_NAMES.get(state_abbr, state_abbr or "United States"))
        city_name = html.escape(str(city_meta["city"]))
        return (
            '<nav class="crumbs" aria-label="Breadcrumb"><ol>'
            '<li><a href="/">Home</a></li>'
            f'<li>{state_name}</li>'
            f'<li aria-current="page">{city_name}</li>'
            "</ol></nav>"
        )
    parts = [p for p in u.strip("/").split("/") if p]
    if not parts: return ""
    items = ['<li><a href="/">Home</a></li>']
    acc = "/"
    for i, part in enumerate(parts):
        acc += part + "/"
        name = html.escape(titles.get(acc, part.replace("-", " ").title()))
        items.append(f'<li aria-current="page">{name}</li>' if i == len(parts)-1 else f'<li><a href="{acc}">{name}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(items) + "</ol></nav>"

def city_directory(pages):
    """Plain HTML list of every city guide, grouped by state. Crawlers can
    follow these <a> links; the homepage dropdown is unchanged."""
    cities = []
    for cu, cm, _, _ in pages:
        if not cm.get("city"):
            continue
        label = f'{cm["city"]}, {cm["state"]}'
        cities.append((str(cm.get("state") or ""), str(cm["city"]), cu, label))
    if not cities:
        return ""
    by_state = {}
    for st, city, url, label in cities:
        name = STATE_NAMES.get(st, st)
        by_state.setdefault(name, []).append((city, url, label))
    blocks = []
    for st_name in sorted(by_state):
        items = sorted(by_state[st_name], key=lambda x: x[0].casefold())
        lis = "".join(
            f'<li><a href="{html.escape(url, quote=True)}">{html.escape(label)}</a></li>'
            for _, url, label in items
        )
        blocks.append(
            f'<div class="city-dir-state">'
            f'<h3 class="city-dir-state-name">{html.escape(st_name)}</h3>'
            f'<ul>{lis}</ul></div>'
        )
    return (
        '<nav class="city-directory" aria-labelledby="city-dir-h">'
        '<h2 id="city-dir-h">All City Guides</h2>'
        '<div class="city-dir-states">' + "".join(blocks) + "</div></nav>"
    )

def city_cards(pages):
    """Homepage city picker: a selectable dropdown (not a scrolling card grid),
    plus a plain linked list of every city guide."""
    opts = ['<option value="">Select your city or town</option>']
    for cu, cm, _, _ in sorted(pages, key=lambda x: x[1].get("city", "")):
        if not cm.get("city"): continue
        label = f'{cm["city"]}, {cm["state"]}'
        opts.append(f'<option value="{html.escape(cu)}">{html.escape(label)}</option>')
    # Keep the existing request callout wording clearly under the dropdown.
    under = ('<p class="city-not-here">Your city/town not here? '
             '<a href="mailto:adam@howtodumpit.com">Drop us a line</a>&hellip;</p>')
    return ('<div class="city-picker" id="city-list">'
            '<label for="city-select">Your city or town</label>'
            '<select id="city-select" name="city" autocomplete="address-level2">'
            + "".join(opts) +
            '</select></div>' + under + city_directory(pages))

def nearby_cities_html(current_url, pages):
    """3–6 links to the geographically closest city guides (default 5)."""
    current = None
    candidates = []
    for cu, cm, _, _ in pages:
        if not cm.get("city"):
            continue
        slug = cu.strip("/")
        loc = _coords(slug, cm)
        row = (cu, cm, loc)
        if cu == current_url:
            current = row
        else:
            candidates.append(row)
    if not current or not current[2]:
        slug = current_url.strip("/")
        print(f"WARNING: no coordinates for {slug or '/'} ; skipping Nearby Cities.")
        return ""
    with_coords = [(cu, cm, loc) for cu, cm, loc in candidates if loc]
    if not with_coords:
        return ""
    here = current[2]
    ranked = sorted(with_coords, key=lambda row: _haversine_km(here, row[2]))
    take = ranked[: max(3, min(NEARBY_COUNT, 6))]
    # If fewer than 3 other geocoded cities exist, show however many we have.
    if not take:
        return ""
    lis = []
    for cu, cm, _ in take:
        label = f'{cm["city"]}, {cm["state"]}'
        lis.append(f'<li><a href="{html.escape(cu, quote=True)}">{html.escape(label)}</a></li>')
    return (
        '<aside class="nearby-cities" aria-labelledby="nearby-h">'
        '<h2 id="nearby-h">Nearby Cities</h2>'
        '<ul>' + "".join(lis) + "</ul></aside>"
    )

def _visible_text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()

def faq_pairs(body_html):
    """Visible FAQ Q&A only. A heading whose text is FAQ or Frequently Asked
    Questions starts the section; each following h3 is a question. Returns
    nothing when the page has no such section, so we never invent FAQ schema."""
    heading = re.search(
        r"<h([23])[^>]*>\s*(?:Frequently Asked Questions|FAQ)\s*</h\1>",
        body_html, flags=re.I | re.S)
    if not heading:
        return []
    rest = body_html[heading.end():]
    nxt = re.search(r"<h2\b", rest, flags=re.I)
    if nxt:
        rest = rest[:nxt.start()]
    parts = re.split(r"(<h3[^>]*>.*?</h3>)", rest, flags=re.I | re.S)
    pairs = []
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            q = _visible_text(parts[i])
            a = _visible_text(parts[i + 1] if i + 1 < len(parts) else "")
            if q and a:
                pairs.append((q, a))
    return pairs

def structured_data_html(canonical, city_meta, body_html):
    """JSON-LD for city guides: BreadcrumbList always, FAQPage only when a
    visible FAQ section already exists on the page."""
    state_abbr = str(city_meta.get("state") or "").strip()
    state_name = STATE_NAMES.get(state_abbr, state_abbr or "United States")
    city_name = str(city_meta.get("city") or "")
    crumbs = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": CFG["base_url"].rstrip("/") + "/"},
            {"@type": "ListItem", "position": 2, "name": state_name},
            {"@type": "ListItem", "position": 3, "name": city_name, "item": canonical},
        ],
    }
    blocks = [crumbs]
    pairs = faq_pairs(body_html)
    if pairs:
        blocks.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in pairs
            ],
        })
    payload = {"@context": "https://schema.org", "@graph": blocks} if len(blocks) > 1 else {
        "@context": "https://schema.org", **crumbs
    }
    dumped = json.dumps(payload, ensure_ascii=True, separators=(",", ":"))
    return f'<script type="application/ld+json">{dumped}</script>\n'

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    if STATIC.exists(): shutil.copytree(STATIC, OUT/"static")
    (OUT/"CNAME").write_text("howtodumpit.com\n")
    page_tpl = string.Template((TPL/"page.html").read_text())
    pages = []
    for p in sorted(CONTENT.rglob("*.md")):
        meta, body = load(p)
        if meta.get("draft"): continue
        u = url_for(p)
        pages.append((u, meta, body, p))
    titles = {u: m.get("short", m["title"]) for u, m, _, _ in pages}
    redirects = [x for x in pages if x[1].get("redirect_to")]
    pages = [x for x in pages if not x[1].get("redirect_to")]
    for u, meta, _, _ in redirects:
        tgt = CFG["base_url"].rstrip("/") + meta["redirect_to"]
        dest = OUT / u.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(prefix_links(
            f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'<title>{html.escape(meta.get("title",""))}</title>'
            f'<link rel="canonical" href="{tgt}">'
            f'<meta http-equiv="refresh" content="0; url={meta["redirect_to"]}">'
            f'<style>body{{font:16px/1.6 system-ui,sans-serif;margin:0;padding:24px max(16px,env(safe-area-inset-left))}}a{{color:#111111;text-decoration-color:#FFC20E;text-decoration-thickness:3px;overflow-wrap:anywhere}}</style></head>'
            f'<body><p>This guide moved to <a href="{meta["redirect_to"]}">{tgt}</a>.</p></body></html>'))
    # a city list is as current as its newest guide, not the date its intro was written
    newest = max((str(m["verified"]) for _, m, _, _ in pages if m.get("city") and m.get("verified")), default="")
    for u, meta, body, p in pages:
        body_html = markdown.markdown(body, extensions=["tables", "toc", "attr_list"])
        # wrap every table so wide tables scroll inside their own box on phones, not the whole page
        body_html = body_html.replace("<table>", '<div class="table-wrap" role="region" aria-label="Table (scroll sideways to see more)" tabindex="0"><table>').replace("</table>", "</table></div>")
        body_html = body_html.replace("<!--LISTINGS-->", listings_html(meta.get("listings"), meta.get("listings_title", "Options at a Glance")))
        body_html = body_html.replace("<!--CITY_GRID-->", city_cards(pages))
        if meta.get("list_children"):
            body_html += city_cards(pages)
        body_html = trim_listing_repeats(body_html)
        body_html = dedupe_links(body_html)
        if meta.get("city"):
            # Local partners near the top, just before the Mattresses heading.
            # No empty section when a city has no partners. Official drop-off
            # `listings:` are unchanged.
            # After the guide and Nearby Cities, a single small plain-text line
            # may mention 1-800-GOT-JUNK and LoadUp. No link, button, box,
            # heading or color block (Adam, 11/11/2026). Do not add a national
            # booking link unless Adam has approved a tracked affiliate link.
            partner_block = partners_html(meta.get("partners") or [], city_slug=u.strip("/"))
            if partner_block:
                i = body_html.find('<h2 id="mattresses"')
                if i < 0:
                    listings_at = body_html.find('class="listings"')
                    i = body_html.find("<h2", listings_at if listings_at >= 0 else 0)
                if i > 0:
                    body_html = body_html[:i] + partner_block + body_html[i:]
                else:
                    body_html = partner_block + body_html
            body_html += nearby_cities_html(u, pages)
            body_html += NATIONAL_NOTE
        hero = ""
        if u == "/":
            hero = ('<section class="hero"><div class="wrap"><h1>' + html.escape(meta.get("hero", meta["title"])) + '</h1><p>'
                    + html.escape(meta.get("description", "")) + '</p></div></section>')
        json_ld = ""
        if meta.get("city"):
            json_ld = structured_data_html(
                CFG["base_url"].rstrip("/") + u, meta, body_html)
        out = page_tpl.substitute(
            site_name=CFG["site_name"], title=html.escape(meta["title"]),
            description=html.escape(meta.get("description", "")),
            canonical=CFG["base_url"].rstrip("/") + u, body=body_html,
            hero=hero, crumbs=crumbs(u, meta["title"], titles, city_meta=meta if meta.get("city") else None),
            json_ld=json_ld,
            og_type="website" if u == "/" else "article",
            after=CITY_REQUEST if (u == "/" or meta.get("city")) else "",
            updated_line=(f'<p class="updated">Last updated: {us_date(newest)}</p>' if meta.get("list_children")
                          else f'<p class="updated">Last verified: {html.escape(meta["verified_note"])}</p>' if meta.get("verified_note")
                          else f'<p class="updated">Last verified: {us_date(meta["verified"])}</p>' if meta.get("verified") and u != "/" else ""),
            year=datetime.date.today().year)
        out = prefix_links(mark_current(out, u))
        dest = OUT / u.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{CFG['base_url'].rstrip('/')}{u}</loc></url>" for u, *_ in pages]
    (OUT/"sitemap.xml").write_text("\n".join(sm + ["</urlset>"]))
    (OUT/"robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {CFG['base_url'].rstrip('/')}/sitemap.xml\n")
    print(f"Built {len(pages)} pages -> {OUT}")

if __name__ == "__main__":
    main()
