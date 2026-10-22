#!/usr/bin/env python3
"""Mobile responsiveness check for HowToDumpIt (permanent rule: run before every push).

Builds nothing by itself: run ./build.sh first. Serves public/ on a local port, opens
EVERY page in headless Chromium at 320, 375, 390, 412 and 1280px, and fails if:
  - the page has no <meta name="viewport" content="width=device-width...">
  - document.documentElement.scrollWidth > window.innerWidth (horizontal scroll)
  - (mobile widths) body text is under 16px, or a visible element sticks out past the screen edge
It also warns about tap targets (buttons, nav links, CTAs) smaller than 44px tall.

Usage (from the repo root):
  ./build.sh && /workspace/.mobile-venv/bin/python scripts/mobile_check.py
  options: --shots DIR    save a full-page PNG per page/width into DIR
           --pages / /portland-or/   only check these URLs
           --widths 375 412          only these widths
Setup once if needed:  python3 -m venv /workspace/.mobile-venv && /workspace/.mobile-venv/bin/pip install playwright
  (uses /usr/bin/google-chrome if present, else run: /workspace/.mobile-venv/bin/playwright install chromium)
Exit code 0 = all pass, 1 = at least one failure.
"""
import argparse, re, functools, http.server, os, pathlib, shutil, socketserver, sys, threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
WIDTHS = [320, 375, 390, 412, 1280]

JS = r"""(screenW) => {
  const vw = screenW;  // the phone's real screen width (innerWidth grows on phones when a page overflows)
  const meta = document.querySelector('meta[name=viewport]');
  const out = {vw, iw: window.innerWidth, sw: document.documentElement.scrollWidth,
    viewport: meta ? meta.content : null, bodyFont: parseFloat(getComputedStyle(document.body).fontSize),
    overflow: [], small: [], redirect: !!document.querySelector('meta[name=x-redirect-stub]')};
  for (const el of document.body.querySelectorAll('*')) {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    // ignore content that is intentionally inside a horizontal-scroll box
    let p = el.parentElement, inside = false;
    while (p && p !== document.body) { const o = getComputedStyle(p).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden') { inside = true; break; } p = p.parentElement; }
    if (!inside && (r.right > vw + 1 || r.left < -1) && !el.closest('.skip,.sr'))
      out.overflow.push(el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : '') + ' (' + Math.round(r.left) + '..' + Math.round(r.right) + 'px)');
  }
  for (const el of document.querySelectorAll('a.btn, .site-header nav a, .brand, .cta a, input:not([type=hidden]), select, button, .card a')) {
    const r = el.getBoundingClientRect(); if (!r.width) continue;
    if (r.height < 44) out.small.push((el.textContent || el.tagName).trim().slice(0, 30) + ' ' + Math.round(r.height) + 'px');
  }
  out.overflow = out.overflow.slice(0, 8);
  return out;
}"""

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    handler = functools.partial(Quiet, directory=str(PUBLIC))
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]

def all_pages():
    return sorted("/" + str(p.parent.relative_to(PUBLIC)).replace(".", "").strip("/") + ("/" if p.parent != PUBLIC else "")
                  for p in PUBLIC.rglob("index.html") if "static" not in p.parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots"); ap.add_argument("--pages", nargs="*"); ap.add_argument("--widths", nargs="*", type=int)
    a = ap.parse_args()
    if not PUBLIC.exists(): sys.exit("public/ missing: run ./build.sh first")
    from playwright.sync_api import sync_playwright
    pages = a.pages or all_pages(); widths = a.widths or WIDTHS
    httpd, port = serve()
    fails = warns = 0
    with sync_playwright() as pw:
        kw = {"executable_path": "/usr/bin/google-chrome"} if os.path.exists("/usr/bin/google-chrome") else {}
        br = pw.chromium.launch(**kw)
        for w in widths:
            mobile = w < 800
            ctx = br.new_context(viewport={"width": w, "height": 800}, device_scale_factor=2 if mobile else 1,
                                 is_mobile=mobile, has_touch=mobile)
            pg = ctx.new_page()
            for u in pages:
                html_text = (PUBLIC / u.strip("/") / "index.html").read_text()
                if 'http-equiv="refresh"' in html_text:
                    # redirect stub: check the stub itself, without following its meta refresh
                    pg.goto(f"http://127.0.0.1:{port}/robots.txt")
                    pg.set_content(re.sub(r'<meta http-equiv="refresh"[^>]*>', '<meta name="x-redirect-stub" content="1">', html_text))
                else:
                    pg.goto(f"http://127.0.0.1:{port}{u}", wait_until="load")
                r = pg.evaluate(JS, w)
                probs = []
                if not r["viewport"] or "width=device-width" not in r["viewport"]: probs.append("no viewport meta")
                if r["sw"] > w or r["iw"] > w: probs.append(f"horizontal scroll (scrollWidth {r['sw']} > {w})")
                if mobile and not r["redirect"] and r["bodyFont"] < 16: probs.append(f"body font {r['bodyFont']}px < 16")
                if mobile and r["overflow"]: probs.append("sticks out: " + "; ".join(r["overflow"]))
                small = r["small"] if mobile else []
                status = "FAIL" if probs else ("WARN" if small else "PASS")
                fails += bool(probs); warns += bool(small and not probs)
                print(f"{status} {w:>4}px {u}  scrollWidth={r['sw']}/{w}" + ("  " + " | ".join(probs) if probs else "")
                      + ("  small tap targets: " + ", ".join(small[:5]) if small else ""))
                if a.shots:
                    d = pathlib.Path(a.shots); d.mkdir(parents=True, exist_ok=True)
                    name = (u.strip("/").replace("/", "_") or "home") + f"_{w}.png"
                    pg.screenshot(path=str(d / name), full_page=True)
            ctx.close()
        br.close()
    httpd.shutdown()
    print(f"\n{len(pages)} pages x {len(widths)} widths: {fails} FAIL, {warns} WARN")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
