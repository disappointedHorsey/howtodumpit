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
