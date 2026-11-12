# HARD RULES: HOW WE WORK (Adam, 05/11/2026)

Adopted by Adam Wells, Executive Chairman, on 05/11/2026 as hard decisions for everything HowToDumpIt does from now on. They apply to every agent, executive, routine, report, email and page. Adam's earlier hard rules (truth to Adam, never guess money, phone number never public, dates and spelling, email rules, security) still apply, and where any of these conflict, truth and accuracy win.

**SOP meta-rule (Adam, 11/11/2026, 12:57 PM Sydney):** every new rule Adam creates must be added to the SOP manual Page, the PDF and the company rules files at the same time, automatically.

**Haulers first, generic businesses in small print (HARD RULE, Adam, 13/11/2026, 9:29 AM Sydney):** "Our haulers are always featured and must look fantastic; generic/national businesses only in one small-print block at the bottom; free listings smaller than Recommended." Every city guide opens with a prominent "Local Junk Removal Pros in [City]" panel (tap-to-call on every listing; Recommended gets clearly the most space; free Basic rows are compact, polished, labeled Not verified, with no website and nothing that looks paid). Any generic, national or big commercial business (national haulers such as 1-800-GOT-JUNK and LoadUp, private haulers, landfills or recyclers by brand such as Waste Management, retailer take-back such as Best Buy or Staples, mattress-recycling programs such as Bye Bye Mattress, marketplaces and apps) appears ONLY in the single small-print, muted, plain-text "Other options" block at the very bottom (front matter `other_options:`; no links, buttons, bold, headings or cards). Official city/county services and genuine nonprofits that are the real public route stay in the guide text as plain text rows, never business-style cards. A city's own contracted collector (e.g. WM for Oakland bulky pickup, Recology in San Francisco) may be named in the text as the official route, never as a card title. Enforced by `scripts/consistency_check.py` (haulers-first rules).

**Always upsell, friendly but persuasive (HARD RULE, Adam, 12/11/2026, 1:20 PM Sydney; strengthened 13/11/2026, 8:20 AM Sydney):** the upsell must be strong and prominent in every partner or prospect email, never softened to one line, even after they decline the paid Recommended spot. Opt-outs still get no upsell. Every reply or email — including free-listing confirmations, nonprofit or charity partners, wording approvals, check-ins, and a reply after a decline — must carry the full upsell block from the company template (the exclusive top spot; 12 times the calls; "$14.99 per real customer call, less than you'd pay for a single shared lead on Thumbtack, and a fraction of what Google ads charge."; "Trying it carries no risk. Your first 3 calls are free, you only pay for real calls, emails and website clicks we send you, and you can stop anytime."; close "Recommended spots tend to get taken quickly, so if you want to be the company [City] sees first, flick me a quick reply. I'll send you the full rate card."). Charities use the donor-call variant. Never use banned phrases. Exception: never upsell anyone who opted out or is suppressed. Canonical SOP: company `rules/outreach-operations.md` and `outreach/TEMPLATE-prospect-pitch.md`.

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
Each city is ONE general junk guide at `content/<city-slug>.md` -> `/<city-slug>/` (e.g. `/chicago-il/`). Required front matter: `title` ("Junk Disposal in <City>, <ST>" — the HTML `<title>` is `$title | HowToDumpIt` and must be 60 characters or fewer, so keep this short), `description` (160 characters or fewer, natural, keep the keyword "Junk disposal in <City>"), `verified`, `city`, `state`, `short`, optional `lat` and `lon` (city-center coordinates for the Nearby Cities block; if omitted, add the slug to `CITY_COORDS` in `build.py`), optional `listings` (+ `listings_title`), optional `partners` (see Partner-listing format below). Body sections, in order:
1. `# Junk Disposal in <City>, <ST>: Mattresses, Couches, Furniture, Appliances, TVs & Electronics, Paint & Hazardous Waste`
2. `## Quick Answer by Item` table (Mattress / Couch-furniture / Fridge-AC (freon) / TV-computer / Paint-chemicals)
3. `## Mattresses and Box Springs {#mattresses}` (with `<!--LISTINGS-->`). If the city has `partners:`, the **Local Junk Removal & Donation Partners** section is auto-inserted at the top of the page, immediately after the intro and before Quick Answer (paid tiers first, then free compact rows; Adam, 13/11/2026). Cities with no partners get no section and no empty box. Official `listings:` cards in the mattress (and other item) sections may only be public, government or nonprofit options (the city's bulky pickup, official drop-off sites, nonprofit reuse). Do not put commercial generic or national companies (1-800-GOT-JUNK, LoadUp, unnamed "private mattress haulers", and similar) in those cards; untagged national links are removed. After the official mattress listings, the generator adds one plain sentence: "If you want a hauler to come get the mattress, use one of the local junk removal companies listed above." Item sections that recommend hiring a hauler must point to those local partners, never to a generic paid service or "the box above". At the very bottom of every city guide (after Nearby Cities and the city-request box), the generator adds ONE small-print, muted "Other options" block: the plain-text strings from optional front matter `other_options:` (generic, national or commercial businesses by brand, retailer take-back, mattress-recycling programs, marketplaces) followed by "Prefer a national company? 1-800-GOT-JUNK and LoadUp also serve this area." No hyperlink, button, box, bold, heading or card. Never name those businesses anywhere else on the page; in the guide text write "(see Other options at the bottom of this page)" (HARD RULE, Adam, 13/11/2026). Do not add a national haul-away booking box or link unless Adam has approved a tracked affiliate link.
4. `## Couches and Furniture {#furniture}`, `## Appliances (Fridges, Freezers, AC: Freon) {#appliances}`, `## TVs, Computers and Electronics (E-Waste) {#electronics}`, `## Paint and Household Hazardous Waste {#hazardous}`
Boroughs/counties rule (Adam, 31/10/2026): a guide covers the rules inside city limits. Where rules differ by borough, district or county within the city, state the difference in the relevant item section with its own official source. Every guide also gets a short `### Outside City Limits?` note (in the furniture section) naming the county/unincorporated-area or neighboring-city official page that applies, plus apartments/HOAs using a private hauler. Never assume a county rule matches the city's.
Rules: only facts verified on official city/county/solid-waste-authority pages, each with an inline source link; if an item can't be verified, say so and point to the official page / 311. Never invent fees, phones, addresses or rules.
Old `/mattress-disposal/<slug>/` URLs are kept as stubs (`redirect_to: "/<slug>/"` front matter -> meta-refresh + canonical page, excluded from sitemap). New cities do NOT need a stub. `/mattress-disposal/` is a hub listing all city guides.

The generator adds these to every city guide automatically, including future nightly pages: a breadcrumb (`Home › State › City`, state is plain text because there is no state landing page) with matching BreadcrumbList JSON-LD; a Nearby Cities block with links to the 5 geographically closest city guides (3–6); and `data-goatcounter-click` names on every partner `tel:` link (`tel-<city-slug>-<partner-slug>`) and every paid partner website link (`web-<city-slug>-<partner-slug>`). FAQPage JSON-LD is emitted only when the page already has a visible FAQ or Frequently Asked Questions section with question headings; never add schema for content that is not on the page. The home page (and the Junk Removal hub) keep the city dropdown and also get a plain HTML list of every city guide, grouped by state, so search engines have `<a>` links to follow.


## Partner-listing format (city guides) — nightly routine
Optional front-matter `partners:` on a city guide renders a **Local Junk Removal & Donation Partners** section at the top of that guide, immediately after the intro and before Quick Answer (Adam, 13/11/2026). Paid tiers come first, then free compact rows. Official drop-off cards stay in `listings:` and may only be public, government or nonprofit options; commercial generic or national companies must not appear as listing cards. After official mattress listings, a plain sentence points haul-away to the local partners listed above. Cities with no `partners:` get no section (do not leave an empty box). Do not invent partners: only add entries the nightly run or an approved pitch reply has confirmed. Generic/national businesses go only in the bottom small-print `other_options:` block, which always ends with the plain-text 1-800-GOT-JUNK and LoadUp line (no hyperlink). The partner section heading is "Local Junk Removal Pros in [City]"; free rows show name, Not verified and a tap-to-call link only. Do not add national haul-away booking links unless Adam has approved a tracked affiliate link.

Each `partners:` entry is a YAML map with:
- `tier` (required): `basic` | `verified` | `featured` or `recommended` (case-insensitive). `featured` is an alias of Recommended. Recommended sorts to the top; then Verified; then Basic. Only one Recommended Partner per city.
- `name` (required): business or organization display name (Title Case for the card heading).
- `website` (required): full URL including `https://`.
- `phone` (optional on Basic; expected for Verified/Recommended): display number shown on the card. Basic renders it as a plain `tel:` link; Verified and Recommended show the number as text plus a **Call Now** button (`tel:`).
- `note` (optional): one short sentence (hours, items accepted, service area). Sentence case.
- `source_checked` (required): date the website/phone were last confirmed (`YYYY-MM-DD`). Shown on the card as a US date.

Example (Basic Listing is free and shows only name, phone and Not verified; website in YAML is a source record, not shown):

```yaml
partners:
- tier: basic
  name: Example Junk Hauling
  phone: '(512) 555-0100'
  website: https://example.com/
  note: Serves Austin and nearby Travis County.
  source_checked: 2026-11-02
```

Example with all three tiers (Recommended uses the exclusive top-spot label and a nearby paid-placement disclosure on the card):

```yaml
partners:
- tier: recommended
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

Card rules (enforced in `build.py`): Basic shows only the name, phone (`tel:` link) and a **Not verified** label. It never shows a website, not even as plain text. A `website` field may stay in the YAML as a source record. Verified and Recommended add a **Call Now** button and a clickable website link (`rel="sponsored nofollow"`). Paid listings do not show verification wording. Recommended sorts first, is visually the exclusive top spot, is labeled **Recommended**, and has a nearby paid-placement disclosure: "Paid placement. We receive referral fees from this partner." (brand #111111 / #FFC20E). A short disclaimer states partners are independent businesses and HowToDumpIt does not vouch for their work.

### Listing presentation rule (permanent, Adam 11/10/2026)
Free (non-paying) company and charity listings stay on the page but are compact secondary **"after runs"**: smaller type, tighter rows, and less real estate than paid cards, always placed below any Recommended or Verified Partner. Recommended and Verified Partner listings get the large, prominent card treatment. Official city drop-off cards (`listings:`) are unchanged. Keep the **Not verified** label on every free Basic Listing and keep all existing sponsored/affiliate and paid-placement disclosures. Free compact rows never show a website, not even as plain text (Adam, 11/11/2026; company 1c7ae6d). Paid Recommended and Verified listings get a clickable website link, at $1.49 per real click once click tracking is live. The Become a Recommended Partner CTA stays in the footer and on /become-a-featured-partner/ only (no second partner CTA on city guides). Shared CSS classes in `static/style.css` (`.partner-basic`, `.partner-verified`, `.partner-recommended`, `.partners-list-paid`, `.partners-list-free`) plus `partners_html()` in `build.py` apply this to every city guide and every future partner or charity card. Pages with only free listings should still look complete and useful; do not leave an empty paid slot.

## Style rule (permanent)
Use American English spelling (color, center, tire, analyze, favorite, specialize) and US dates only (October 13, 2026 or 10/13/2026). Never DD/MM/YYYY. This applies to pages, pitch emails and reports.

## Prospect listing lifecycle and city restart loop (permanent, Adam 11/11/2026)
Build and nightly work must follow this. Full SOP: company `rules/outreach-operations.md`.

1. Do not publish a new city guide, and do not pitch a city, until **4 free local listings** are live on that page. Each must be checked on the organisation's own website as serving that city. Their cards use the free Basic treatment and stay labeled **Not verified**. If four cannot be found, hold the city back — do not publish or pitch it.
2. Unreplied prospects stay as compact free "after runs" rows (name, phone `tel:` link and **Not verified** only, with no website, below any paid cards) through the first pitch and up to **3 nudges**, sent at least 7 days apart.
3. The three outcomes (do not skip any) and the remove loop:
   - They reply and pay: upgrade the entry to `tier: verified` ($8) or `tier: recommended` ($14.99).
   - They opt out or ask us to stop: remove the listing from the city page immediately, keep a minimal suppression record, and never contact them again. Then find the next best verified local haulier in that city (not previously pitched or suppressed, verified on its own site), add it as a free Not verified listing (name and phone only), and run the full onboarding (pitch drafted for Adam's approval, then the reminder and 3-nudge loop). The page never drops below 4 listings. The Pitch reply watch routine detects opt-outs and does this.
   - Every prospect in the city has had the pitch plus 3 nudges, the last one 7 or more days ago, and none replied: **remove** all of those listings from the page, mark them **discarded, city restart**, and never contact them again. Add 4 new verified local hauliers as free Basic Listings, then queue pitches for Adam's approval. **Repeat this remove-and-replace loop** until someone in the city replies. Do not restart a city without first removing the old listings.
4. Any reply at all stops the restart for that city; flag it to Adam.

## Opt-out replacement (permanent, Adam 11/11/2026, 12:57 PM Sydney)
If any haulier or prospect in any city unsubscribes or opts out, remove them from the site immediately and keep a minimal suppression record. Then find the next best verified local haulier in that city (not previously pitched or suppressed, verified on its own site), add it as a free Not verified listing (name and phone only), and run the full onboarding: pitch drafted for Adam's approval, then the reminder and 3-nudge loop. The page never drops below 4 listings. The Pitch reply watch routine detects opt-outs and carries this out. Full SOP: company `rules/outreach-operations.md`.

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
