#!/usr/bin/env python3
"""Unified comms & rationality check for the built site (public/).

Run after ./build.sh:   python3 scripts/consistency_check.py [public_dir]
Exits 1 if any page has a problem. Rules come from
/workspace/company/rules/comms-consistency.md (the glossary below must match it).

What it checks on every built page (redirect stubs skipped):
  dup-href      same link target twice in one content section (h2 to next h2)
  dup-text      same link text twice on a page (header nav, breadcrumbs and footer excluded)
  dup-heading   the same heading text twice on a page
  near-dup      two near-identical sentences in the page content
  term          banned or non-canonical terms (see GLOSSARY / BANNED)
  spelling      British spellings (colour, centre, tyre, specialise, ...)
  date          day-first dates (27/10/2026, 27 October 2026) on site pages
  self-link     a content link to the page itself (nav/footer self links must carry aria-current="page")
  dead-link     internal link to a page or #anchor that doesn't exist
Stdlib only, so it runs anywhere (CI, nightly routines, pre-push).
"""
import difflib, html, pathlib, re, sys, urllib.parse
from html.parser import HTMLParser

SITE_HOST = "howtodumpit.com"

# ---- Canonical terms (keep in sync with company/rules/comms-consistency.md) ----
# (regex, message). Matched case-sensitively against visible text, <title> and meta description.
BANNED = [
    (r"\b(?!HowToDumpIt\b)[Hh]ow[ -]?[Tt]o[ -]?[Dd]ump[ -]?[Ii]t\b(?!\.com|@)", 'brand name is "HowToDumpIt"'),
    (r"(?i)\bhaul-away\b", 'say "paid junk removal" (not "haul-away")'),
    (r"(?i)\bjunk-removal\b", 'write "junk removal" (no hyphen)'),
    (r"(?i)\bmattress disposal by city\b", 'the hub is "Junk Removal" (it covers every item, not just mattresses)'),
    (r"(?i)\bjunk pickup\b(?!.{0,40}san jos)", None),  # placeholder, filtered below
    (r"(?i)\b(we|our crews?|our trucks?) (will )?(haul|pick up|remove)s?\b(?! anything)", 'we are info-only: we never haul, pick up or remove anything'),
    (r"(?i)\bguarantee[ds]?\b", "never overpromise: no guarantees"),
    (r"(?i)\bper lead\b", 'pricing is "per call or email" (a tracked call of 60 seconds or more, or an email)'),
    (r"(?i)\bpremium (partner|listing)\b", 'partner tiers are "Basic Listing", "Verified Partner", "Featured Partner"'),
]
BANNED = [b for b in BANNED if b[1]]
# Official program names that legitimately contain an otherwise-banned phrase.
ALLOW_PHRASES = []

BRITISH = re.compile(r"(?i)\b(colour(s|ed|ful|ing)?|centres?|tyres?|specialis(e|ed|es|ing|t|ts)|analys(e|ed|ing)|favourites?|favourite|organis(e|ed|es|ing|ation|ations)|cancell(ed|ing)|labour|behaviour|licence|metres?|litres?|recognis(e|ed|es|ing)|apologis(e|ed|es|ing)|neighbour(s|hood|hoods)?|catalogue|travell(ed|ing)|modell(ed|ing)|fulfil(?!l))\b")

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
DATE_DMY_NUM = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b")
DATE_DMY_TXT = re.compile(rf"\b\d{{1,2}}(st|nd|rd|th)? (of )?({MONTHS}),? \d{{4}}\b")

# Link texts that may repeat on a page because each one cites a different official page.
REPEAT_OK_TEXT = {"source", "official page"}

BLOCK_TAGS = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "dd", "dt", "blockquote", "figcaption", "summary"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, attrs, region)
        self.links = []          # dict(href, text, region, section, attrs)
        self.blocks = []         # (region, tag, text)
        self.headings = []       # (tag, text)
        self.ids = set()
        self.title = ""
        self.meta_desc = ""
        self.refresh = False
        self.section = 0
        self._a = None
        self._blk = []           # stack of [tag, region, textparts]
        self._skip = 0
        self._in_title = False

    def region(self):
        return self.stack[-1][2] if self.stack else "head"

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag == "meta":
            if a.get("name") == "description": self.meta_desc = a.get("content", "")
            if (a.get("http-equiv") or "").lower() == "refresh": self.refresh = True
        if tag in ("script", "style"): self._skip += 1
        if tag == "title": self._in_title = True
        cls = (a.get("class") or "").split()
        reg = self.region()
        if tag == "header": reg = "header"
        elif tag == "footer": reg = "footer"
        elif tag == "nav" and "crumbs" in cls: reg = "crumbs"
        elif tag == "nav": reg = "nav"
        elif tag == "main" and reg not in ("header", "footer"): reg = "main"
        elif tag == "section" and "hero" in cls: reg = "hero"
        elif tag == "body" and reg == "head": reg = "body"
        if tag in ("h1", "h2") and reg == "main": self.section += 1
        if tag not in VOID:
            self.stack.append((tag, a, reg))
        if tag == "a":
            self._a = {"href": a.get("href", ""), "text": [], "region": reg, "section": self.section, "attrs": a}
        if tag in BLOCK_TAGS:
            self._blk.append([tag, reg, []])

    def handle_endtag(self, tag):
        if tag in ("script", "style"): self._skip = max(0, self._skip - 1)
        if tag == "title": self._in_title = False
        if tag == "a" and self._a is not None:
            self._a["text"] = norm("".join(self._a["text"]))
            self.links.append(self._a); self._a = None
        if tag in BLOCK_TAGS and self._blk and self._blk[-1][0] == tag:
            t, reg, parts = self._blk.pop()
            text = norm("".join(parts))
            if text:
                self.blocks.append((reg, t, text))
                if t.startswith("h"): self.headings.append((t, text, reg))
                if self._blk: self._blk[-1][2].append(" ")
        # pop to matching tag
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]; break

    def handle_data(self, d):
        if self._skip: return
        if self._in_title: self.title += d; return
        if self._a is not None: self._a["text"].append(d)
        if self._blk: self._blk[-1][2].append(d)
        elif d.strip() and self.region() in ("main", "hero", "footer", "header", "nav", "crumbs", "body"):
            self.blocks.append((self.region(), "text", norm(d)))


def norm(s):
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def page_url(path, root):
    rel = path.relative_to(root).parent.as_posix()
    return "/" if rel == "." else f"/{rel}/"


def resolve(href, here):
    """Return (path, fragment) for an internal link, or None for external/mailto."""
    if not href or href.startswith(("mailto:", "tel:", "javascript:")): return None
    u = urllib.parse.urlparse(urllib.parse.urljoin("https://" + SITE_HOST + here, href))
    if u.netloc and u.netloc.lower().removeprefix("www.") != SITE_HOST: return None
    return (u.path or "/"), u.fragment


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(])", text) if s.strip()]


def key(s):
    return re.sub(r"[^a-z0-9$ ]+", "", s.lower()).split()


def check_page(path, root, pages_ids):
    raw = path.read_text(encoding="utf-8")
    p = Page(); p.feed(raw)
    if p.refresh: return []
    here = page_url(path, root)
    probs = []
    add = lambda kind, msg: probs.append(f"{here}  [{kind}] {msg}")

    content_links = [l for l in p.links if l["region"] in ("main", "hero")]
    # dup-href per content section
    seen = {}
    for l in content_links:
        h = l["href"].rstrip("/") or "/"
        if h.startswith("#"): h = here + h
        k = (l["section"], h)
        if k in seen:
            add("dup-href", f'"{l["text"]}" and "{seen[k]}" both link to {l["href"]} in the same section')
        else:
            seen[k] = l["text"]
    # dup-text across the page content.
    #  - the same text pointing to different places is always a problem (except citation markers);
    #  - internal page links and CTA buttons (class btn / rel sponsored) may appear only once per page;
    #  - an external official source or the contact email may be cited again in a later item section
    #    (each item section answers on its own); repeats inside one section are caught by dup-href.
    cnt = {}
    for l in content_links:
        t = l["text"].lower().rstrip(" →").strip()
        if not t: continue
        cnt.setdefault(t, []).append(l)
    for t, ls in cnt.items():
        if len(ls) < 2: continue
        hrefs = sorted({l["href"] for l in ls})
        if len(hrefs) > 1:
            if t not in REPEAT_OK_TEXT:
                add("dup-text", f'link text "{t}" is used for {len(hrefs)} different targets ({", ".join(hrefs)})')
            continue
        l0 = ls[0]
        is_cta = "btn" in (l0["attrs"].get("class") or "") or "sponsored" in (l0["attrs"].get("rel") or "")
        if is_cta or resolve(l0["href"], here) is not None:
            add("dup-text", f'{"CTA" if is_cta else "internal link"} "{t}" appears {len(ls)} times (-> {l0["href"]})')
    # dup headings
    hs = {}
    for tag, text, reg in p.headings:
        if reg not in ("main", "hero"): continue
        hs[text.lower()] = hs.get(text.lower(), 0) + 1
    for t, n in hs.items():
        if n > 1: add("dup-heading", f'heading "{t}" appears {n} times')
    # near-duplicate sentences in content
    sents = []
    for reg, tag, text in p.blocks:
        if reg not in ("main", "hero") or tag in ("td", "th") or tag.startswith("h"): continue
        for s in sentences(text):
            k = key(s)
            # skip pure citations "(Source name)" and listing fact lines "Cost: ... Type: ..."
            if s.startswith("(") and s.rstrip(".").endswith(")") or s.startswith("Cost:"): continue
            if len(k) >= 6: sents.append((s, k))
    uniq = {}
    for s, k in sents: uniq.setdefault(" ".join(k), (s, k))
    items = list(uniq.values())
    for (s, k), n in ((it, sum(1 for x in sents if x[1] == it[1])) for it in items):
        if n > 1: add("near-dup", f'sentence repeated {n} times: "{s[:110]}"')
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i][1], items[j][1]
            if abs(len(a) - len(b)) > max(len(a), len(b)) * 0.3: continue
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            if sm.ratio() < 0.85: continue
            # parallel lines that differ only in a number ("$8 per call" / "$12 per call") are fine
            diff = [w for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal" for w in a[i1:i2] + b[j1:j2]]
            if diff and all(re.fullmatch(r"\$?[0-9][0-9,.]*", w) for w in diff): continue
            if True:
                add("near-dup", f'near-identical sentences: "{items[i][0][:90]}" / "{items[j][0][:90]}"')
    # text checks: visible text + title + description
    texts = [t for _, _, t in p.blocks] + [p.title, p.meta_desc]
    # only leaf blocks are needed, but duplicates of nested text are harmless for regex checks
    blob = "\n".join(dict.fromkeys(texts))
    for rx, msg in BANNED:
        for m in re.finditer(rx, blob):
            ctx = blob[max(0, m.start() - 40): m.end() + 40].replace("\n", " ")
            if any(a in ctx for a in ALLOW_PHRASES): continue
            add("term", f'"{m.group(0)}": {msg}  (…{ctx}…)')
    for m in BRITISH.finditer(blob):
        add("spelling", f'British spelling "{m.group(0)}" (use American spelling)')
    for m in DATE_DMY_NUM.finditer(blob):
        d, mo = int(m.group(1)), int(m.group(2))
        if d > 12 and mo <= 12:
            add("date", f'day-first date "{m.group(0)}": US pages use MM/DD/YYYY or "October 27, 2026"')
    for m in DATE_DMY_TXT.finditer(blob):
        add("date", f'day-first date "{m.group(0)}": write "Month D, YYYY"')
    # self links and dead links
    for l in p.links:
        r = resolve(l["href"], here)
        if not r: continue
        tpath, frag = r
        if not tpath.endswith("/") and "." not in tpath.rsplit("/", 1)[-1]: tpath += "/"
        if tpath == here and not frag and not l["href"].startswith("#"):
            if l["region"] in ("main", "hero", "crumbs"):
                add("self-link", f'"{l["text"]}" links to this page itself')
            elif l["attrs"].get("aria-current") != "page" and "brand" not in (l["attrs"].get("class") or ""):
                add("self-link", f'{l["region"]} link "{l["text"]}" points to this page but lacks aria-current="page"')
        if tpath.endswith("/"):
            if tpath not in pages_ids:
                add("dead-link", f'"{l["text"]}" -> {l["href"]} (no such page)')
            elif frag and frag not in pages_ids[tpath]:
                add("dead-link", f'"{l["text"]}" -> {l["href"]} (no #{frag} on that page)')
        else:
            if not (root / tpath.lstrip("/")).exists():
                add("dead-link", f'"{l["text"]}" -> {l["href"]} (missing file)')
    return probs


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "public")
    files = sorted(root.rglob("index.html"))
    if not files:
        print(f"consistency_check: no pages in {root}; run ./build.sh first"); return 2
    pages_ids = {}
    for f in files:
        pp = Page(); pp.feed(f.read_text(encoding="utf-8"))
        pages_ids[page_url(f, root)] = pp.ids
    probs = []
    for f in files:
        probs += check_page(f, root, pages_ids)
    for x in probs: print("FAIL", x)
    print(f"consistency_check: {len(files)} pages, {len(probs)} problem(s)")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
