# Changelog

## 2026-10-12
- Redesign: new `templates/page.html` + `static/style.css` (mobile-first, system font stack, sticky header with wordmark, hero, footer, skip link). No external assets/trackers; tiny inline JS for city filter.
- `build.py`: breadcrumbs, OG/Twitter meta, city-card grid (`<!--CITY_GRID-->` and on `list_children` hub), "Book a junk pickup" affiliate CTA box on pages with `city:` front matter (placeholder 1-800-GOT-JUNK / LoadUp links, `rel="sponsored nofollow"`, disclosure). New front-matter keys: `city`, `state`, `item`, `short`, `hero`.
- Added mattress-disposal guides: New York City NY, Los Angeles CA, Houston TX, Phoenix AZ, Philadelphia PA, San Antonio TX, San Diego CA, Dallas TX, Austin TX, Seattle WA (official sources cited on each page, verified 2026-10-12).
- Home page rewritten around city search grid; Chicago/Columbus got `city`/`state` metadata.

## 2026-10-11
- Shipped Chicago, IL mattress disposal guide (`content/mattress-disposal/chicago-il.md`): DSS bulk pickup via 311/ward sanitation (no extra fee for 1–4 unit homes), bed-bug set-out rule, Chicago Furniture Bank donation drop-off; linked from home index; seeded `BACKLOG.md`.
- Added GitHub Actions workflow `.github/workflows/pages.yml` to build (`./build.sh`, Python 3.13) and deploy `public/` to GitHub Pages.
- `site.yaml`: `base_url` temporarily set to https://disappointedhorsey.github.io/howtodumpit (custom domain not registered yet; no CNAME).
- `build.py`: derive a path prefix from `base_url` and prefix root-relative `href`/`src` links so the site works under a subpath.
- `build.sh` / `build.py` tracked as executable.
