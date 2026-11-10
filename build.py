#!/usr/bin/env python3
"""Tiny static site generator: content/**/*.md (YAML front matter) -> public/.
Usage: .venv/bin/python build.py   (or ./build.sh)"""
import datetime, difflib, html, pathlib, re, shutil, string, urllib.parse
import markdown, yaml

ROOT = pathlib.Path(__file__).parent
CONTENT, OUT, TPL, STATIC = ROOT/"content", ROOT/"public", ROOT/"templates", ROOT/"static"
CFG = yaml.safe_load((ROOT/"site.yaml").read_text())
# Path prefix for hosting under a subpath (e.g. GitHub Pages project site); "" at a domain root.
PREFIX = urllib.parse.urlparse(CFG["base_url"]).path.rstrip("/")

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

def partners_html(items):
    """Render Local Junk Removal & Donation Partners from front-matter `partners:`.

    Paid tiers (Recommended, Verified Partner) are large prominent cards and sort first.
    Free Basic Listings (companies and charities) are compact secondary "after runs"
    below any paid cards (Adam, 11/10/2026). Official drop-off `listings:` are unchanged.
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
            if phone:
                tel = html.escape(_tel_href(phone), quote=True)
                phone_esc = html.escape(phone)
                # Phone as plain text; Call Now is the single tel: link (avoids dup-href).
                bits.append(f'<p class="partner-phone">{phone_esc}</p>')
                bits.append(f'<p class="partner-cta"><a class="btn" href="{tel}">Call Now</a></p>')
            if website:
                href = html.escape(website, quote=True)
                label = html.escape(_website_label(website))
                bits.append(f'<p class="partner-web"><a href="{href}" rel="nofollow" target="_blank">{label}</a></p>')
        else:
            meta = []
            if phone:
                tel = html.escape(_tel_href(phone), quote=True)
                phone_esc = html.escape(phone)
                meta.append(f'<span class="partner-phone"><a href="{tel}">{phone_esc}</a></span>')
            if website:
                href = html.escape(website, quote=True)
                label = html.escape(_website_label(website))
                meta.append(f'<span class="partner-web"><a href="{href}" rel="nofollow" target="_blank">{label}</a></span>')
            if meta:
                sep = '<span class="partner-meta-sep" aria-hidden="true"> · </span>'
                bits.append('<p class="partner-meta">' + sep.join(meta) + "</p>")
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

AFFILIATE_CTA = (
    '<aside class="cta" aria-labelledby="cta-h"><h2 id="cta-h">Book Paid Junk Removal</h2>'
    '<p>Can\'t wait for the city, or can\'t carry it to the curb? A paid junk removal crew can haul it from inside your home.</p>'
    '<div class="cta-btns">'
    '<a class="btn" href="https://www.1800gotjunk.com/" rel="sponsored nofollow" target="_blank">1-800-GOT-JUNK &rarr;</a>'
    '<a class="btn btn-alt" href="https://goloadup.com/" rel="sponsored nofollow" target="_blank">LoadUp &rarr;</a></div>'
    '<p class="disclosure"><strong>Affiliate disclosure:</strong> HowToDumpIt is an information guide and does not haul anything. '
    'We may earn a commission if you book through these links, at no extra cost to you. Prices and service areas are set by the provider.</p></aside>')

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

def crumbs(u, title, titles):
    parts = [p for p in u.strip("/").split("/") if p]
    if not parts: return ""
    items = ['<li><a href="/">Home</a></li>']
    acc = "/"
    for i, part in enumerate(parts):
        acc += part + "/"
        name = html.escape(titles.get(acc, part.replace("-", " ").title()))
        items.append(f'<li aria-current="page">{name}</li>' if i == len(parts)-1 else f'<li><a href="{acc}">{name}</a></li>')
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + "".join(items) + "</ol></nav>"

def city_cards(pages):
    """Homepage city picker: a selectable dropdown (not a scrolling card grid)."""
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
            '</select></div>' + under)

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
            # CTA after the listings block (or at the end)
            i = body_html.find('<h2 id="mattresses"')
            if i < 0: i = body_html.find("<h2", body_html.find('class="listings"') if 'class="listings"' in body_html else 0)
            body_html = body_html[:i] + AFFILIATE_CTA + body_html[i:] if i > 0 else body_html + AFFILIATE_CTA
            # Partner cards at end of city guide (official drop-off `listings:` unchanged)
            body_html += partners_html(meta.get("partners") or [])
        hero = ""
        if u == "/":
            hero = ('<section class="hero"><div class="wrap"><h1>' + html.escape(meta.get("hero", meta["title"])) + '</h1><p>'
                    + html.escape(meta.get("description", "")) + '</p></div></section>')
        out = page_tpl.substitute(
            site_name=CFG["site_name"], title=html.escape(meta["title"]),
            description=html.escape(meta.get("description", "")),
            canonical=CFG["base_url"].rstrip("/") + u, body=body_html,
            hero=hero, crumbs=crumbs(u, meta["title"], titles),
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
