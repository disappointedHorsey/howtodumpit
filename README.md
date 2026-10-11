# Bulky Item Disposal Guide (working title)
Dump it where it won't hurt our world.

Plain Python + Markdown static site.
- Content: content/**/*.md (YAML front matter; `listings:` renders where `<!--LISTINGS-->` appears; `verified:` date shown on page)
- Build: ./build.sh  -> public/
- Preview: cd public && python3 -m http.server 8000
- Deploy (not done): push repo to GitHub and connect Cloudflare Pages (build cmd `./build.sh`, output `public`), or use GitHub Pages via Actions.
Rule: every listing needs a `source:` URL to an official/primary page, checked on the `verified` date.
