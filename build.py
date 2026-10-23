#!/usr/bin/env python3
"""Tiny static site generator: content/**/*.md (YAML front matter) -> public/.
Usage: .venv/bin/python build.py   (or ./build.sh)"""
import datetime, html, pathlib, re, shutil, string, urllib.parse
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

AFFILIATE_CTA = (
    '<aside class="cta" aria-labelledby="cta-h"><h2 id="cta-h">Book a Junk Pickup</h2>'
    '<p>Can\'t wait for the city, or can\'t carry it to the curb? A paid junk-removal crew can haul it from inside your home.</p>'
    '<div class="cta-btns">'
    '<a class="btn" href="https://www.1800gotjunk.com/" rel="sponsored nofollow" target="_blank">1-800-GOT-JUNK &rarr;</a>'
    '<a class="btn btn-alt" href="https://goloadup.com/" rel="sponsored nofollow" target="_blank">LoadUp &rarr;</a></div>'
    '<p class="disclosure"><strong>Affiliate disclosure:</strong> HowToDumpIt is an information guide and does not haul anything. '
    'We may earn a commission if you book through these links, at no extra cost to you. Prices and service areas are set by the provider.</p></aside>')

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
    cards = []
    for cu, cm, _, _ in sorted(pages, key=lambda x: x[1].get("city", "")):
        if not cm.get("city"): continue
        label = f'{cm["city"]}, {cm["state"]}'
        cards.append(f'<li class="card" data-search="{html.escape(label.lower())} {html.escape(cm.get("slug_search",""))}">'
                     f'<a href="{cu}"><span class="card-city">{html.escape(label)}</span>'
                     f'<span class="card-item">Mattresses, couches, appliances &amp; more</span>'
                     f'<span class="card-go">Read Guide &rarr;</span></a></li>')
    return ('<div class="search"><label for="city-q" class="sr">Find Your City</label>'
            '<input id="city-q" type="search" placeholder="Search your city, e.g. Houston" autocomplete="off"></div>'
            '<ul class="cards" id="city-list">' + "".join(cards) + '</ul>'
            '<p id="no-match" class="no-match" hidden>No guide for that city yet. Check your city\'s official sanitation or 311 page.</p>')

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
    for u, meta, body, p in pages:
        body_html = markdown.markdown(body, extensions=["tables", "toc", "attr_list"])
        # wrap every table so wide tables scroll inside their own box on phones, not the whole page
        body_html = body_html.replace("<table>", '<div class="table-wrap" role="region" aria-label="Table (scroll sideways to see more)" tabindex="0"><table>').replace("</table>", "</table></div>")
        body_html = body_html.replace("<!--LISTINGS-->", listings_html(meta.get("listings"), meta.get("listings_title", "Options at a Glance")))
        body_html = body_html.replace("<!--CITY_GRID-->", city_cards(pages))
        if meta.get("list_children"):
            body_html += city_cards(pages)
        if meta.get("city"):
            # CTA after the listings block (or at the end)
            i = body_html.find('<h2 id="mattresses"')
            if i < 0: i = body_html.find("<h2", body_html.find('class="listings"') if 'class="listings"' in body_html else 0)
            body_html = body_html[:i] + AFFILIATE_CTA + body_html[i:] if i > 0 else body_html + AFFILIATE_CTA
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
            updated_line=f'<p class="updated">Last verified: {us_date(meta["verified"])}</p>' if meta.get("verified") and u != "/" else "",
            year=datetime.date.today().year)
        out = prefix_links(out)
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
