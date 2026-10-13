# Changelog

## 2026-10-13 (Cambridge–Somerville, MA)
- Added Cambridge–Somerville, MA general junk guide (`content/cambridge-somerville-ma.md`, `/cambridge-somerville-ma/`) covering both cities side by side: Cambridge UTEC mattress pickup ($45/piece since July 20, 2026) vs. Somerville $55 Disposal Sticker + 311; furniture limits (1/week Cambridge, 2/week Somerville); Cambridge paid appliance permit vs. Somerville $25 White Goods Sticker; e-waste (Cambridge Recycling Center / 20-inch TV rule; Somerville DPW Yard drop-off + free 311 TV pickup); HHW days (Cambridge November 7, 2026; Somerville November 5 and 14, 2026) and paint rules. Official cambridgema.gov / somervillema.gov / mass.gov sources cited; verified 2026-10-13.

## 2026-10-12 (Denver, CO)
- Added Denver, CO general junk guide (`content/denver-co.md`): Large Item Pickup every 9 weeks (bagged/wrapped mattresses, max 5 large items), free Appliance Collection for freon appliances, E-cycle Coupon via Blue Star Recyclers, PaintCare + HHW At-Your-Door. Official denvergov.org sources cited; verified 2026-10-12.

## 2026-10-12 (Washington, DC)
- Added Washington, DC general junk guide (`content/washington-dc.md`): DPW bulk appointment (plastic-wrapped mattresses, max 7 items), Fort Totten self-haul, freon appliances, e-waste ban + Special Waste / eCYCLE DC, PaintCare + HHW events. Official sources cited; verified 2026-10-12.

## 2026-10-12 (restructure: general junk guides)
- City guides moved from `/mattress-disposal/<city>/` to `/<city-slug>/` and expanded into general junk guides: quick-answer table + sections for mattresses, couches/furniture, appliances (freon), TVs/electronics, paint/HHW, with official source links (city sites, SWACO, Dallas County HHW network via dallascityhall.com).
- Old `/mattress-disposal/<city>/` URLs now meta-refresh redirect stubs with canonical to the new URL (`redirect_to` front matter; excluded from sitemap).
- `/mattress-disposal/` is now a hub linking all city guides. Home hero/meta, nav, footer, card subtitles ("Mattresses, couches, appliances & more") generalized.
- `build.py`: redirect stubs, `listings_title`, `attr_list` markdown extension (section anchors), affiliate box placed before the Mattresses section.
- README/BACKLOG: nightly routine now uses the multi-item city format.

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
