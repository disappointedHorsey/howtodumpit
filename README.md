# Bulky Item Disposal Guide (working title)
Dump it where it won't hurt our world.

Plain Python + Markdown static site.
- Content: content/**/*.md (YAML front matter; `listings:` renders where `<!--LISTINGS-->` appears; `verified:` date shown on page)
- Build: ./build.sh  -> public/
- Preview: cd public && python3 -m http.server 8000
- Deploy: GitHub Pages via Actions (see below).
Rule: every listing needs a `source:` URL to an official/primary page, checked on the `verified` date.

## Deploy (GitHub Pages)
- Repo: disappointedHorsey/howtodumpit. `.github/workflows/pages.yml` runs on push to `main` (or manually): Python 3.13 -> `./build.sh` -> deploys `public/` with actions/configure-pages, upload-pages-artifact, deploy-pages.
- One-time: Settings -> Pages -> Source = "GitHub Actions" (or API `POST /repos/disappointedHorsey/howtodumpit/pages` `{"build_type":"workflow"}`, needs Pages + Administration write).
- Live URL: https://howtodumpit.com (`base_url` in site.yaml is `https://howtodumpit.com`, so the path prefix is empty). build.py derives a path prefix from `base_url` and prepends it to root-relative `href`/`src` links.

## Content format (city guides) — nightly routine
Each city is ONE general junk guide at `content/<city-slug>.md` -> `/<city-slug>/` (e.g. `/chicago-il/`). Required front matter: `title` ("Junk Disposal in <City>, <ST>: Mattresses, Couches, Appliances, TVs & Paint"), `description`, `verified`, `city`, `state`, `short`, optional `listings` (+ `listings_title`). Body sections, in order:
1. `# Junk Disposal in <City>, <ST>: Mattresses, Couches, Furniture, Appliances, TVs & Electronics, Paint & Hazardous Waste`
2. `## Quick Answer by Item` table (Mattress / Couch-furniture / Fridge-AC (freon) / TV-computer / Paint-chemicals)
3. `## Mattresses and Box Springs {#mattresses}` (with `<!--LISTINGS-->`). The "Book a Junk Pickup" affiliate box is auto-inserted right before this heading.
4. `## Couches and Furniture {#furniture}`, `## Appliances (Fridges, Freezers, AC: Freon) {#appliances}`, `## TVs, Computers and Electronics (E-Waste) {#electronics}`, `## Paint and Household Hazardous Waste {#hazardous}`
Rules: only facts verified on official city/county/solid-waste-authority pages, each with an inline source link; if an item can't be verified, say so and point to the official page / 311. Never invent fees, phones, addresses or rules.
Old `/mattress-disposal/<slug>/` URLs are kept as stubs (`redirect_to: "/<slug>/"` front matter -> meta-refresh + canonical page, excluded from sitemap). New cities do NOT need a stub. `/mattress-disposal/` is a hub listing all city guides.

## Style rule (permanent)
Use American English spelling (color, center, tire, analyze, favorite, specialize) and US dates only (October 13, 2026 or 10/13/2026). Never DD/MM/YYYY. This applies to pages, pitch emails and reports.

## Pitch targeting rule (permanent)
Before drafting any pitch, confirm from the org's own website (address plus service-area page) that it actually serves that city. Skip orgs that don't serve it. The pitch must name the org's real location and coverage accurately. Record the verified location and source URL in PITCHES.md.

## Mobile rule (permanent, Adam 10/22/2026)
The site must work on iPhone and Android phones. **Every change must be checked at 320px, 375px (iPhone) and 412px (Android) before pushing**, plus a desktop glance at 1280px.
- Automated check (all pages in public/, at 320/375/390/412/1280px; fails on missing viewport tag, horizontal scroll, body text under 16px or anything sticking out past the screen edge; warns on tap targets under 44px):
  `cd /workspace/site && ./build.sh && /workspace/.mobile-venv/bin/python scripts/mobile_check.py`
  Add `--shots /tmp/shots` to save screenshots and look at them. Exit code must be 0 before you push.
  One-time setup if the venv is missing: `python3 -m venv /workspace/.mobile-venv && /workspace/.mobile-venv/bin/pip install -r scripts/requirements-dev.txt` (uses /usr/bin/google-chrome; otherwise `/workspace/.mobile-venv/bin/playwright install chromium`).
- CSS is mobile-first (static/style.css): base rules are for phones, `@media (min-width:...)` adds desktop. Don't add fixed pixel widths; images stay `max-width:100%`.
- Every template/page keeps `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">` (redirect stubs too, set in build.py).
- Markdown tables are auto-wrapped in a `.table-wrap` box (build.py) so wide tables scroll sideways inside the box, never the whole page.
- Form fields must be 16px+ text (or iOS zooms in) and buttons/links you tap at least 44px tall.
- When you change static/style.css, bump the `?v=` in templates/page.html so phones don't keep the old CSS.

## Capitalization rule (permanent, Adam 10/23/2026)
RULE (10/23/2026, Adam): Title Case for nav, headings, titles, buttons and table headers (e.g. 'For Haulers'); sentence case in body text; brand names as written. Check capitalization on every site change.
- Title Case covers: nav/menu items, header and footer links, buttons and calls to action, front-matter `title`/`short`/`listings_title`, listing names (card titles), the HTML <title>, H1/H2/H3 headings, breadcrumbs and table column headers. US Title Case: lowercase a, an, the, and, but, or, nor, for, as, at, by, in, of, on, per, to, via, vs unless first word, first word after a colon or "(", or last word; capitalize both parts of hyphenated words (Drop-Off, E-Waste, On-Demand).
- Keep brand names as written (QuoteIQ, HighLevel, GorillaDesk, Housecall Pro, Jobber, 1-800-GOT-JUNK, LoadUp, ReStore, HowToDumpIt), acronyms (ID, FAQ, HHW, DPW, LASAN) and city names. Slugs, URLs and file names stay lowercase.
