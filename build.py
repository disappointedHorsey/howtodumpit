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

def listings_html(items):
    if not items: return ""
    rows = []
    for it in items:
        src = f' <a class="src" href="{html.escape(it["source"])}" rel="nofollow">source</a>' if it.get("source") else ""
        rows.append(f'<li class="listing"><h3>{html.escape(it["name"])}</h3>'
                    f'<p><strong>Cost:</strong> {html.escape(str(it.get("cost","-")))} &middot; '
                    f'<strong>Type:</strong> {html.escape(it.get("type",""))}</p>'
                    f'<p>{html.escape(it.get("details",""))}{src}</p></li>')
    return '<h2>Options at a glance</h2><ul class="listings">' + "".join(rows) + "</ul>"

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
    for u, meta, body, p in pages:
        body_html = markdown.markdown(body, extensions=["tables", "toc"])
        body_html = body_html.replace("<!--LISTINGS-->", listings_html(meta.get("listings")))
        # simple child index for section pages
        if meta.get("list_children"):
            kids = [(cu, cm) for cu, cm, _, _ in pages if cu.startswith(u) and cu != u]
            body_html += "<ul>" + "".join(f'<li><a href="{cu}">{html.escape(cm["title"])}</a></li>' for cu, cm in kids) + "</ul>"
        out = page_tpl.substitute(
            site_name=CFG["site_name"], title=html.escape(meta["title"]),
            description=html.escape(meta.get("description", "")),
            canonical=CFG["base_url"].rstrip("/") + u, body=body_html,
            updated=meta.get("verified", ""), year=datetime.date.today().year)
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
