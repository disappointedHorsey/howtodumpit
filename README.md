# HARD RULES: HOW WE WORK (Adam, 05/11/2026)

Adopted by Adam Wells, Executive Chairman, on 05/11/2026 as hard decisions for everything HowToDumpIt does from now on. They apply to every agent, executive, routine, report, email and page. Adam's earlier hard rules (truth to Adam, never guess money, phone number never public, dates and spelling, email rules, security) still apply, and where any of these conflict, truth and accuracy win.

1. **Role.** Be concise and high-signal. Optimize every reply for usefulness per word. Think carefully, but show only the result unless Adam asks for reasoning.
2. **Token policy.**
   - Start with the direct answer. Skip greetings, restating the request, and generic caveats.
   - Use the shortest format that fully solves the task: one sentence, bullets, table, or code.
   - Don't explain obvious steps. Don't repeat information already given.
   - Ask one precise question only when an answer is truly required to proceed; otherwise assume sensible defaults and state them in a few words.
   - Never pad with summaries, "next steps", alternatives, or examples unless asked.
   - Prefer concrete numbers, names, commands, and decisions over long prose.
3. **Research.** When facts may be current, search first. Return only the finding, date, and source link. Label verified facts and inference separately, in one short label each. Don't narrate the search.
4. **Writing.** Match Adam's language and tone. For drafts, give a ready-to-send version only. Plain language; headings only when they help scanning.
5. **Code.** Give the smallest working change. Include setup or explanation only if it's needed to run it. Point out a real risk only when it materially affects correctness or security.
6. **Format.** Default answer budget is 80 to 150 words. Go longer only for complex tasks, exact requested detail, or safety-critical topics. If Adam says "brief", keep it under 60 words.
7. **Decision rule.** Before replying, silently remove every sentence that doesn't change Adam's decision, action, or understanding.
8. **Task mode.** For multi-step work, give the finished result first, then only the essential actions. Don't simulate progress or describe internal deliberation. Use checklists only for real dependencies.
9. **Compression.** Compress hard: bullets instead of paragraphs, one shared label instead of repeated wording, a recommendation instead of vague advice. Keep quoted text, URLs, commands, and numbers exact.
10. **Uncertainty.** If unsure, say "I'm not sure" and name the one fact that would resolve it. Never fabricate details to make an answer feel complete.
11. **Commands.** When Adam asks for an action, give the exact command or click path first, plus one line of context only when it prevents a likely mistake.
12. **Final check.** Is it accurate, actionable, and as short as possible? If yes, send it.

---

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
Each city is ONE general junk guide at `content/<city-slug>.md` -> `/<city-slug>/` (e.g. `/chicago-il/`). Required front matter: `title` ("Junk Disposal in <City>, <ST>: Mattresses, Couches, Appliances, TVs & Paint"), `description`, `verified`, `city`, `state`, `short`, optional `listings` (+ `listings_title`), optional `partners` (see Partner-listing format below). Body sections, in order:
1. `# Junk Disposal in <City>, <ST>: Mattresses, Couches, Furniture, Appliances, TVs & Electronics, Paint & Hazardous Waste`
2. `## Quick Answer by Item` table (Mattress / Couch-furniture / Fridge-AC (freon) / TV-computer / Paint-chemicals)
3. `## Mattresses and Box Springs {#mattresses}` (with `<!--LISTINGS-->`). The "Book Paid Junk Removal" affiliate box is auto-inserted right before this heading.
4. `## Couches and Furniture {#furniture}`, `## Appliances (Fridges, Freezers, AC: Freon) {#appliances}`, `## TVs, Computers and Electronics (E-Waste) {#electronics}`, `## Paint and Household Hazardous Waste {#hazardous}`
Boroughs/counties rule (Adam, 31/10/2026): a guide covers the rules inside city limits. Where rules differ by borough, district or county within the city, state the difference in the relevant item section with its own official source. Every guide also gets a short `### Outside City Limits?` note (in the furniture section) naming the county/unincorporated-area or neighboring-city official page that applies, plus apartments/HOAs using a private hauler. Never assume a county rule matches the city's.
Rules: only facts verified on official city/county/solid-waste-authority pages, each with an inline source link; if an item can't be verified, say so and point to the official page / 311. Never invent fees, phones, addresses or rules.
Old `/mattress-disposal/<slug>/` URLs are kept as stubs (`redirect_to: "/<slug>/"` front matter -> meta-refresh + canonical page, excluded from sitemap). New cities do NOT need a stub. `/mattress-disposal/` is a hub listing all city guides.


## Partner-listing format (city guides) — nightly routine
Optional front-matter `partners:` on a city guide renders a **Local Junk Removal & Donation Partners** section at the end of that guide. Official drop-off cards stay in `listings:` and are unchanged. Do not invent partners: only add entries the nightly run or an approved pitch reply has confirmed.

Each `partners:` entry is a YAML map with:
- `tier` (required): `basic` | `verified` | `featured` (case-insensitive). Featured sorts to the top; then Verified; then Basic. Only one Featured Partner per city.
- `name` (required): business or organization display name (Title Case for the card heading).
- `website` (required): full URL including `https://`.
- `phone` (optional on Basic; expected for Verified/Featured): display number shown on the card. Basic renders it as a plain `tel:` link; Verified and Featured show the number as text plus a **Call Now** button (`tel:`).
- `note` (optional): one short sentence (hours, items accepted, service area). Sentence case.
- `source_checked` (required): date the website/phone were last confirmed (`YYYY-MM-DD`). Shown on the card as a US date.

Example (Basic Listing only — free: name, phone and website):

```yaml
partners:
- tier: basic
  name: Example Junk Hauling
  phone: '(512) 555-0100'
  website: https://example.com/
  note: Serves Austin and nearby Travis County.
  source_checked: 2026-11-02
```

Example with all three tiers (Featured uses the paid label on the card):

```yaml
partners:
- tier: featured
  name: Top Spot Hauling
  phone: '(704) 555-0199'
  website: https://topspot.example/
  note: Same-day cleanouts inside city limits.
  source_checked: 2026-11-02
- tier: verified
  name: Verified Crew Co
  phone: '(704) 555-0188'
  website: https://verifiedcrew.example/
  source_checked: 2026-11-02
- tier: basic
  name: Neighborhood Reuse Center
  website: https://reuse.example/
  phone: '(704) 555-0177'
  source_checked: 2026-11-02
```

Card rules (enforced in `build.py`): Basic shows name, phone (`tel:` link) and website. Verified and Featured add a **Call Now** button. Featured gets a visible **Featured Partner (Paid)** label (brand #111111 / #FFC20E) and sorts first. A short disclaimer states partners are independent businesses and HowToDumpIt does not vouch for their work.

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

## Comms consistency rule (permanent, Adam 10/27/2026)
Every page must make sense to a first-time visitor: no repeated links, CTAs or sentences, one name per thing, and claims that match the rest of the site, pitch emails and reports. Full rules and glossary: `/workspace/company/rules/comms-consistency.md`.
- Automated: `python3 scripts/consistency_check.py` (run after `./build.sh`). Fails on duplicate links in a section, repeated internal links/CTAs or same link text for different targets, near-duplicate sentences, banned/non-canonical terms, British spellings, day-first dates, self-links and dead internal links. Its banned-term list must match the glossary in the rules doc.
- Pre-push: `scripts/prepush.sh` builds and runs the consistency check and the mobile check; both must exit 0. It is installed as the git pre-push hook (`git config core.hooksPath .githooks`), and the Pages workflow also runs the consistency check before deploying.
- The generator enforces two rules on every page, so nightly guides inherit them: a page is linked only once per section (repeats become plain text; repeated "(Source)" citations are dropped), and a listing card drops any sentence the guide text already says.
- Writing city guides: cite each official page once per section, don't copy listing `details` word for word into the body, and say "paid junk removal" (never "haul-away").
