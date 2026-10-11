# Changelog

## 2026-10-11
- Added GitHub Actions workflow `.github/workflows/pages.yml` to build (`./build.sh`, Python 3.13) and deploy `public/` to GitHub Pages.
- `site.yaml`: `base_url` temporarily set to https://disappointedhorsey.github.io/howtodumpit (custom domain not registered yet; no CNAME).
- `build.py`: derive a path prefix from `base_url` and prefix root-relative `href`/`src` links so the site works under a subpath.
- `build.sh` / `build.py` tracked as executable.
