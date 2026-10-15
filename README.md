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
- Temporary URL: https://disappointedhorsey.github.io/howtodumpit/ (`base_url` in site.yaml). build.py derives a path prefix from `base_url` and prepends it to root-relative `href`/`src` links, so the site works under `/howtodumpit/`.
- When howtodumpit.com is registered: set `base_url: "https://howtodumpit.com"` (prefix becomes empty), add the custom domain in Pages settings (or a `static/CNAME`), and set DNS.

## Content format (city guides) — nightly routine
Each city is ONE general junk guide at `content/<city-slug>.md` -> `/<city-slug>/` (e.g. `/chicago-il/`). Required front matter: `title` ("Junk disposal in <City>, <ST>: mattresses, couches, appliances, TVs & paint"), `description`, `verified`, `city`, `state`, `short`, optional `listings` (+ `listings_title`). Body sections, in order:
1. `# Junk disposal in <City>, <ST>: mattresses, couches, furniture, appliances, TVs & electronics, paint & hazardous waste`
2. `## Quick answer by item` table (Mattress / Couch-furniture / Fridge-AC (freon) / TV-computer / Paint-chemicals)
3. `## Mattresses and box springs {#mattresses}` (with `<!--LISTINGS-->`). The "Book a junk pickup" affiliate box is auto-inserted right before this heading.
4. `## Couches and furniture {#furniture}`, `## Appliances (fridges, freezers, AC: freon) {#appliances}`, `## TVs, computers and electronics (e-waste) {#electronics}`, `## Paint and household hazardous waste {#hazardous}`
Rules: only facts verified on official city/county/solid-waste-authority pages, each with an inline source link; if an item can't be verified, say so and point to the official page / 311. Never invent fees, phones, addresses or rules.
Old `/mattress-disposal/<slug>/` URLs are kept as stubs (`redirect_to: "/<slug>/"` front matter -> meta-refresh + canonical page, excluded from sitemap). New cities do NOT need a stub. `/mattress-disposal/` is a hub listing all city guides.

## Style rule (permanent)
Use American English spelling (color, center, tire, analyze, favorite, specialize) and US dates only (October 13, 2026 or 10/13/2026). Never DD/MM/YYYY. This applies to pages, pitch emails and reports.

## Pitch targeting rule (permanent)
Before drafting any pitch, confirm from the org's own website (address plus service-area page) that it actually serves that city. Skip orgs that don't serve it. The pitch must name the org's real location and coverage accurately. Record the verified location and source URL in PITCHES.md.
