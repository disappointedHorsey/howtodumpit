# Changelog

## 2026-10-11
- Shipped Chicago, IL mattress disposal guide (`content/mattress-disposal/chicago-il.md`): DSS bulk pickup via 311/ward sanitation (no extra fee for 1–4 unit homes), bed-bug set-out rule, Chicago Furniture Bank donation drop-off; linked from home index; seeded `BACKLOG.md`.
- Added GitHub Actions workflow `.github/workflows/pages.yml` to build (`./build.sh`, Python 3.13) and deploy `public/` to GitHub Pages.
- `site.yaml`: `base_url` temporarily set to https://disappointedhorsey.github.io/howtodumpit (custom domain not registered yet; no CNAME).
- `build.py`: derive a path prefix from `base_url` and prefix root-relative `href`/`src` links so the site works under a subpath.
- `build.sh` / `build.py` tracked as executable.
