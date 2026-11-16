#!/usr/bin/env python3
"""Submit changed URLs to IndexNow (Bing, Yandex, Seznam, Naver and others; not Google).

No account is needed: the key lives in site.yaml (`indexnow_key`) and build.py
publishes it at https://howtodumpit.com/<key>.txt. Run AFTER the deploy is live,
because the search engines fetch that key file to confirm we own the site.

Usage:
  python3 scripts/indexnow_submit.py URL [URL ...]      # specific pages (full URLs or /paths/)
  python3 scripts/indexnow_submit.py --since REV        # pages whose content/*.md changed since git REV
  python3 scripts/indexnow_submit.py --all              # every URL in public/sitemap.xml (use sparingly)
  add --dry-run to print the payload without sending.
Stdlib only. Exit code 0 when IndexNow answers 200 or 202.
"""
import json, pathlib, re, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENDPOINT = "https://api.indexnow.org/indexnow"


def cfg():
    txt = (ROOT / "site.yaml").read_text()
    get = lambda k: re.search(rf'^{k}:\s*"?([^"\n]+)"?', txt, re.M).group(1).strip()
    return get("base_url").rstrip("/"), get("indexnow_key")


def url_for(md, base):
    rel = md.relative_to(ROOT / "content").with_suffix("")
    if rel.name == "index":
        rel = rel.parent
    path = "/" if str(rel) == "." else f"/{rel.as_posix()}/"
    return base + path


def changed_since(rev, base):
    out = subprocess.run(["git", "diff", "--name-only", rev, "HEAD", "--", "content"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    urls = []
    for f in out:
        md = ROOT / f
        if md.suffix == ".md" and md.exists():
            head = md.read_text().split("---", 2)[1] if md.read_text().startswith("---") else ""
            if re.search(r"^(draft|redirect_to):", head, re.M):
                continue
            urls.append(url_for(md, base))
    return urls


def main(argv):
    base, key = cfg()
    dry = "--dry-run" in argv
    args = [a for a in argv if a != "--dry-run"]
    if not args:
        print(__doc__); return 2
    if args[0] == "--all":
        sm = (ROOT / "public" / "sitemap.xml").read_text()
        urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    elif args[0] == "--since":
        urls = changed_since(args[1], base)
    else:
        urls = [a if a.startswith("http") else base + "/" + a.strip("/") + ("/" if a.strip("/") else "") for a in args]
    urls = sorted(dict.fromkeys(u for u in urls if u.startswith(base)))
    if not urls:
        print("indexnow: nothing to submit"); return 0
    host = base.split("://", 1)[1]
    payload = {"host": host, "key": key, "keyLocation": f"{base}/{key}.txt", "urlList": urls[:10000]}
    if dry:
        print(json.dumps(payload, indent=2)); return 0
    req = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    print(f"indexnow: HTTP {code} for {len(urls)} URL(s)")
    for u in urls:
        print("  ", u)
    return 0 if code in (200, 202) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
