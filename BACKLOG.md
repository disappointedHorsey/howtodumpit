# HowToDumpIt backlog

Last updated: 10/28/2026 (Memphis, TN guide; 10/27/2026: Baltimore, MD guide; 10/24/2026: Boston, MA guide; 10/23/2026: Las Vegas, NV guide; 10/22/2026: Oklahoma City, OK guide; 10/21/2026: San Francisco, CA guide; Indianapolis, IN guide; earlier: San Jose, CA; Fort Worth, TX; Charlotte, NC; Jacksonville, FL guides; build.py US date fix)

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
- [x] Las Vegas, NV general junk disposal guide (shipped 10/23/2026, commit 20a30bf)
- [x] Boston, MA general junk disposal guide (shipped 10/24/2026)
- [x] Detroit, MI general junk disposal guide (shipped 10/26/2026, commit 1f01274)
- [x] Baltimore, MD general junk disposal guide (shipped 10/27/2026, commit 5c1861c)
- [x] Memphis, TN general junk disposal guide (shipped 10/28/2026, commit ece7b56)

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
- [x] San Jose, CA junk disposal guide (shipped 10/20/2026 UTC / 10/21/2026 Sydney nightly)
- [x] Indianapolis, IN junk disposal guide (shipped 10/21/2026)
- [x] San Francisco, CA junk disposal guide (shipped 10/21/2026; first city in the nightly list below)
- [x] Oklahoma City, OK junk disposal guide (shipped 10/22/2026)
- [x] Boston, MA junk disposal guide (shipped 10/24/2026; separate from the Cambridge–Somerville guide)
- [ ] Next nightly cities, in order (largest uncovered with fetchable official pages; San Francisco, Oklahoma City, Las Vegas, Boston, El Paso, Detroit, Baltimore and Memphis done, do not rebuild): Milwaukee, WI (next), then Albuquerque, NM, Tucson, AZ, Fresno, CA. Check the official pages fetch before writing; if blocked, try the browser (Playwright) or skip to the next city.

## Follow-ups
- [ ] Memphis, TN (10/28/2026) unverified: bulky pile size limit conflict (memphistn.gov Household Garbage page says 10 cubic yards; 2025 Clean City Guide says half a cubic yard; page shows both and says ask 311); Farrisview Convenience Center hours conflict (Solid Waste page Fri-Sun 9-3 vs. 10/31/2025 news release Mon-Fri 8-3); whether refrigerant must be removed before bulk pickup; whether TVs go out with bulk (HHW refuses TVs; Waste Wizard is in the app only); bed-bug/soiled mattress rule; landfill fees and South Shelby Landfill address conflict (5954 Malone Rd 38118 in Clean City Guide vs. 5494 Malone Rd 38119 in news release; page gives no address); City hazardous waste page lists older HHW hours (Tue/Sat 8:30-1) than the County (Tue/Thu/Sat 8-1). shelbycountytn.gov returns 403 to curl/WebFetch (read via Playwright browser; 2026 HHW brochure read via search index only). Prospects for later: Memphis Junk Removal (memjunk.com), Binghampton Development Corporation Hub Recycling (bdcmemphis.org).
- [ ] Baltimore, MD (10/27/2026) unverified: refrigerant (freon) removal rule or fee before bulk pickup or drop-off (City pages silent; page points to 311 and EPA); bed-bug or soiled-mattress wrapping rule for bulk trash; latex paint rule (HHW list names oil paint only); 311 Online also shows a 'Bulk Trash Pick Up-Weekday (No Appliances)' request type not described on the DPW bulk page (not used on our page); Quarantine Road hours conflict (mattress page 7:30 a.m.-3:30 p.m. vs. drop-off locations page 9 a.m.-3:30 p.m.; page says arrive after 9); HHW page says fluorescent bulbs at 'Northwest Residential Recycling Center' on HHW days while HHW is at Sisson Street (not used); 2027 HHW dates not yet published (program runs June-December). Prospects for later: Baltimore City Junk Removal, Madman Junk Removal, Maryland Junk Removal, Second Chance Inc.
- [ ] Las Vegas, NV (10/23/2026) unverified: fee for fridge/freezer/AC drop-off at Republic transfer stations/Apex (not published); resident transfer-station and landfill fees; whether non-freon appliances (washer/dryer) go out with every-other-week bulk; whether Clark County HHW drop-off is free/residents-only (2026 calendar lists no fee); bed-bug mattress rule beyond wrapping soiled mattresses in plastic; any official mattress recycling program (none found); LVMC 9.08 read via search index only (Municode blocks fetch); SNHD vs. Clark County guide conflict on dried-paint can lid (page avoids specifying); apartment/multifamily bulky handling (page says only individual curbside service). Re-check Opportunity Village for a published email (pitch skipped).
- [x] Verify freon-appliance disposal: Chicago (done 2026-10-14: DSS bulk + door removal; HCCRF no appliances/freon)
- [ ] Boston, MA (10/24/2026) unverified: whether City mattress and special item pickups have any fee (boston.gov pages list none; page says so and points to 311); City rule for non-freon appliances such as washers and dryers (not on the special item list; page says check the Trash Day app or 311); any furniture size or quantity limit for curbside trash (none published); 2027 Zero Waste Day dates (only the 11/21/2026 rescheduled event is listed). Re-check Boston Building Resources for a published email (pitch skipped).
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
- [ ] San Jose, CA: the City's Junk Pickup accepted-items list (sanjoseca.gov showpublisheddocument/69710) is dated May 27, 2020; confirm it's still current (sanjoseca.gov returns 403 to curl; WebFetch works). Reconcile the Residents FAQ ("unlimited junk pickups", "call your recycling collection company directly") with the Junk Pickup page (book via 311, up to 12 items per request).
- [ ] San Jose, CA: find an official rule for bed-bug or moldy mattresses (excluded from Junk Pickup; no alternative published) and for refrigerant/freon handling (City list is silent).
- [ ] San Jose, CA: confirm Goodwill of Silicon Valley's free mattress drop-off (1080 N. 7th St.; goodwillsv.org) on the Bye Bye Mattress locator (JS-only) before listing it as an option; check County HHW per-visit quantity limits (none on hhw.santaclaracounty.gov pages) and nearby landfill resident fees (SJEnvironment.org/Landfill-Transfer).
- [ ] San Francisco, CA: Recology's pages don't publish fridge prep rules (food out, doors taped/removed) or say whether window/portable AC units count as accepted "appliances"; no official bed-bug mattress rule found; no SF rule allowing dried latex paint in the black bin (page sends all paint to HHW/hardware stores); the Recology accepted-items help center (recologysf.zendesk.com) is gone; Transfer Station fees are Recology's posted schedule (re-check yearly).
- [ ] Indianapolis, IN: confirm whether freon appliance pickup (via Mayor's Action Center) has a fee or prep rules (door removal, food removed) and whether it counts toward the two-item heavy trash limit; none on indy.gov Trash 101 / Report a Trash Pickup Issue pages.
- [ ] Indianapolis, IN: find South Side Landfill resident rates (City says volume-based; pricing page not verified) and an official City rule for bed-bug mattresses; confirm ToxDrop is no-cost on an indy.gov page (only an Indy DPW social post says "no cost"); confirm the heavy trash service area (excluded towns such as Beech Grove, Lawrence, Speedway not checked); check RecycleForce TV size limits and donation fees on its own site (Squarespace, JS-heavy); no City latex-paint dry-out rule found (page uses IDEM guidance). indy.gov pages are JS-rendered (curl gets an empty shell); WebFetch renders them.
- [ ] Oklahoma City, OK: confirm whether TVs go out with curbside bulky waste (the Bulky Waste page doesn't list TVs/electronics; the Free Landfill Day page says "televisions are accepted" but also lists e-waste as not accepted; the What Goes Where tool is JS-only and okc.gov returns 403 to curl, so check it via browser); confirm whether the freon-appliance pickup has a fee or counts toward the 4-cubic-yard allowance; check the 2027 Free Landfill Day and spring Special Collection dates when posted; the City's Reuse and Repurpose list still shows an old HHW address (3738 SW 15th St.) and Radio Shack, so re-check retailer TV/computer programs and fees (Best Buy "fee required" amount not on the City page); no official mattress-specific recycling or donation option found.
- [ ] Reconcile README/CHANGELOG (still mention github.io base_url) with live howtodumpit.com setup

## Guides / hubs / tools
- [ ] Hot tub removal guide (national hub; added 10/26/2026 by weekly opportunity scan). Repeated Reddit asks (r/hottub, r/tampa, r/kelowna); high-value hauler job, so it suits Featured partner leads. Cover: drain and disconnect, give away free (Marketplace/Craigslist), dealer haul-away, junk removal, DIY cut-up + dumpster; link to city guides for local bulky/landfill rules. No price ranges unless from an official or vendor source.
- [ ] E-bike and scooter battery disposal guide (national hub; added 10/26/2026). Evidence: r/RadPowerBikes thread "NO ONE WILL TAKE THIS DAMN THING" (reddit.com/r/RadPowerBikes/comments/1uktxby), r/ebikes. Facts only from EPA (epa.gov/recycle/used-lithium-ion-batteries), The Battery Network (participating brands only; damaged batteries: isolate in sand/kitty litter, call manufacturer), and city pages (e.g. SF Environment: Recology free pickup for damaged batteries). Fire-safety angle; link to each city guide's HHW section.
- [ ] Propane tank disposal guide (national hub; added 10/26/2026). Evidence: r/homeowners thread, 231-upvote top answer "Tank exchange" (reddit.com/r/homeowners/comments/1uo8dcf). Cover tank exchange cages, propane suppliers, HHW size limits (e.g. Wake County up to 20 lb; StopWaste 5 gallons or smaller); 1 lb camping cylinders.
- [ ] Quality rule for all national hubs (Google spam policy on scaled content, developers.google.com/search/docs/essentials/spam-policies): original, fact-checked main content with sources and "Last verified"; no near-duplicate city templates.
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
- [ ] TODO: swap plain rel="nofollow" vendor homepage links on /for-haulers/software/ for tracked affiliate links (rel="sponsored nofollow") once QuoteIQ/Jobber/HighLevel/GorillaDesk/Housecall Pro approve. QuoteIQ: [x] done 10/23/2026 (Rewardful link ?via=d83c2c live). HighLevel: [x] done 10/25/2026 (?fp_ref=adam-3840d1 live). Jobber, GorillaDesk, Housecall Pro: still pending
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

- [ ] El Paso, TX follow-ups (unverified on official pages 10/25/2026): freon appliance handling/fee at special pickup and Collection Stations; Collection Station fees (none listed); full HHW accepted list; landfill resident fees; mattress bagging/bed-bug rule; latex paint dry-out rule; whether furniture can go with regular trash.
- [ ] Detroit, MI follow-ups (unverified or conflicting on official pages 10/26/2026): bed-bug/soiled mattress rule; who removes refrigerant and at what cost, and whether drop-off centers take fridges/AC units; DPW paid pickup rates (estimate only); latex paint dry-out rule; whether Recycle Here! takes furniture. Source conflicts: Davison Yard address (8221 vs 7901 W. Davison), drop-off volume limit (1 cu yd on drop-off page vs 2 cu yd in 2026 curbside PDF; page uses 1,000 lb/day), bulk frequency (weekly vs bi-weekly; page points to schedule tool), J. Fons Saturday hours (8-12 vs 8-1; page uses 8-12), HHW microwaves vs 'no appliances'.

- (added 10/26/2026, from Rules Agent run 4) National piano disposal hub: city bulky pickup and donation programs often refuse pianos (link our verified SF and Portland pages); high-value hauler job for Featured leads. Demand: reddit.com/r/askportland/comments/1w3uqjr/how_to_yeet_a_piano/ . Verify all rules on official sources before publishing.
- (added 10/26/2026, from Rules Agent run 4) Companion page: above-ground pool removal (e.g. Somerville, MA requires private disposal of metal pools: somervillema.gov/trash-and-recycling). Verify on official sources.
