# HowToDumpIt backlog

Last updated: 10/20/2026 (Fort Worth, TX; Charlotte, NC; Jacksonville, FL guides; build.py US date fix)

## Done
- [x] Columbus, OH mattress disposal
- [x] Chicago, IL mattress disposal (shipped 2026-10-11)
- [x] New York City, NY mattress disposal (2026-10-12)
- [x] Los Angeles, CA mattress disposal (2026-10-12)
- [x] Houston, TX mattress disposal (2026-10-12)
- [x] Philadelphia, PA mattress disposal (2026-10-12)
- [x] Phoenix, AZ mattress disposal (2026-10-12)
- [x] San Antonio, TX mattress disposal (2026-10-12)
- [x] Dallas, TX mattress disposal (2026-10-12)
- [x] Austin, TX mattress disposal (2026-10-12)
- [x] San Diego, CA mattress disposal (2026-10-12)
- [x] Seattle, WA mattress disposal (2026-10-12)
- [x] Site redesign: sticky header, hero + city search, city cards, affiliate CTA, breadcrumbs, OG meta (2026-10-12)

## Priority unbuilt (city pages)
- [x] Chicago, IL couch disposal (covered in general Chicago guide)
- [ ] Philadelphia, PA couch disposal
- [x] Washington, DC junk disposal guide (shipped 2026-10-12)
- [x] Denver, CO junk disposal guide (shipped 2026-10-12)
- [x] Cambridge–Somerville, MA junk disposal guide (shipped 2026-10-13)
- [ ] Plano, TX paint disposal (note 2026-10-15: plano.gov is a JS-rendered CivicPlus site; curl/fetch return empty pages, so verify via browser before building)
- [x] Louisville, KY junk disposal guide incl. paint (shipped 2026-10-15)
- [x] Nashville, TN junk disposal guide (shipped 2026-10-16)
- [x] Portland, OR junk disposal guide (shipped 2026-10-17)
- [x] Fort Worth, TX junk disposal guide (shipped 10/20/2026; catch-up for missed 10/18 nightly)
- [x] Charlotte, NC junk disposal guide (shipped 10/20/2026; catch-up for missed 10/19 nightly)
- [x] Jacksonville, FL junk disposal guide (shipped 10/20/2026; catch-up for missed 10/20 nightly)
- [ ] Seattle, WA paint disposal

## Follow-ups
- [x] Verify freon-appliance disposal: Chicago (done 2026-10-14: DSS bulk + door removal; HCCRF no appliances/freon)
- [ ] Verify freon-appliance disposal: Los Angeles (household), Dallas, San Diego
- [ ] Verify furniture disposal option for San Diego (no city curbside bulky pickup)
- [ ] Re-check Phoenix HHW home-collection reservations (closed as of 2026-10-12)
- [ ] Confirm Dallas Home Chemical Collection Center hours (city page has dated holiday info)
- [ ] Austin, TX: confirm whether ARR on-demand bulk accepts mattresses (not on published accepted list); update page
- [ ] San Antonio, TX: verify curbside bulky accepted-items list for mattresses
- [ ] Cambridge, MA: confirm appliance/large-item permit fee (not shown on main City page; permit portal is JS-only) and add to page
- [ ] Replace placeholder affiliate URLs with real tracked links once programs approve
- [ ] Nashville, TN: find the Sheriff's Office Bulk Item Removal request phone on an official page (not on sheriff.nashville.gov/bulk-item-removal/); confirm AC/freon drop-off rule (2025 policy PDF says East Center, 1/month) and C&D limit (1 vs 2 cubic yards) with Waste Services
- [ ] Portland, OR: confirm with Metro (503-234-3000) whether Metro South takes mattresses free (only the Metro Central page lists free mattress drop-off); confirm the curbside bulky category for window/wall AC units (City rate sheet lists portable AC only); find an official City/Metro latex-paint dry-out rule (none found; page points to Metro HHW/PaintCare); re-check Metro transfer station fees (adjusted yearly)
- [x] build.py prints "Last verified" in US format (e.g. October 20, 2026) on every page (fixed 10/20/2026)
- [ ] Fort Worth, TX: confirm curbside bulk takes non-coolant appliances (washer/dryer); only the City Waste Wizard says so, the bulk page excludes coolant/gas/chemical appliances. The bulk schedule PDF and DOS FAQ PDF are WAF-blocked to curl; read via browser.
- [ ] Charlotte, NC: confirm whether City bulky collection has a fee or a per-pickup item limit (none listed on charlottenc.gov pages or the eligibility PDF; admin policy PDF is a scanned image)
- [ ] Jacksonville, FL: confirm bulk frequency in non-automated (City/Meridian) areas (Waste Wizard says garbage day; no explicit weekly statement found on a current page); find Trail Ridge Landfill resident fees on an official page
- [ ] Reconcile README/CHANGELOG (still mention github.io base_url) with live howtodumpit.com setup

## Guides / hubs / tools
- [ ] Mattress hub guide (expand)
- [ ] State mattress laws guide
- [ ] Cut-up-a-mattress guide
- [ ] Mattress donation guide
- [ ] LoadUp vs 1-800-GOT-JUNK compare
- [ ] City pickup vs junk removal compare
- [ ] New mattress with removal guide
- [ ] Latex paint disposal guide
- [ ] Couch hub
- [ ] Disposal quiz tool
- [ ] Fridge / AC disposal hub

## Candidates from social scan (2026-10-11)
Durable-intent only (not spam):
- [ ] Transfer-station mattress fee hikes (e.g. Hingham, MA fee jump coverage) — city/town fee-change explainers when an official fee schedule is published
- [ ] Illegal-dumping mattress city guides — how to report fly dumping + legal disposal alternatives (pair with strong 311/official enforcement pages)

## Notes
- New city pages use the multi-item format in README "Content format (city guides)": /<city-slug>/, sections for mattresses, couches/furniture, appliances (freon), TVs/electronics, paint/HHW, each with official source links.
- Remaining 'mattress'/'couch'/'paint' city items above should be built as (or merged into) the city's general guide, not separate pages.
- Publish one new page nightly when possible.
- Every listing needs a `source:` URL to an official/primary page and page-level `verified:` date.
- Never invent fees, phones, or addresses.

## Hauler section (/for-haulers/) — alternate with city guides in the nightly routine
Shipped 2026-10-12: hub, /for-haulers/software/, /for-haulers/pricing-calculator/, /for-haulers/dump-fees/
- [ ] TODO: swap plain rel="nofollow" vendor homepage links on /for-haulers/software/ for tracked affiliate links (rel="sponsored nofollow") once QuoteIQ/Jobber/HighLevel/GorillaDesk/Housecall Pro approve
- [ ] Verify Housecall Pro Essentials/MAX prices (not visible in page text 2026-10-12)
- [ ] Verify commercial (hauler) tipping fees per city; dump-fees page currently residential-only
- [x] Junk removal price sheet template (downloadable) (shipped 2026-10-15: /for-haulers/price-sheet-template/)
- [ ] Mattress & appliance surcharges for haulers (link mattress-disposal section)
- [ ] Best software for a one-truck junk removal startup (under $50/mo)
- [ ] Jobber alternatives for junk removal
- [ ] QuoteIQ review for junk haulers (hands-on with trial)
- [ ] How to quote junk removal from photos
- [ ] Starting a junk removal business: licensing, insurance, first-month checklist (US)
Rules: official vendor pages only, dated; no invented market rates; FTC disclosure on every page.

- [ ] Brisbane QLD (first Australian city; official Brisbane City Council sources only; demand: https://x.com/twtrrr/status/2108376410910068911)
