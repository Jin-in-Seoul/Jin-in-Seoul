#!/usr/bin/env python3
"""Read-only site SEO audit. Python standard library only.
Run: python3 scripts/audit_seo.py
Report: seo-audit-report.md (GitHub Actions artifact).
No source files are modified.
"""
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
HOST = "jin-in-seoul.com"
BASE = "https://" + HOST
REPORT = ROOT / "seo-audit-report.md"
ISSUES = []
PAGES = {}
def issue(level, code, path, detail):
    ISSUES.append((level, code, str(path), str(detail).replace("\n", " ")[:350]))
def local_path(url):
    if not url or "{{" in url or "{%" in url:
        return None
    parsed = urlsplit(url)
    if parsed.netloc and parsed.netloc != HOST:
        return None
    path = unquote(parsed.path)
    if not path.startswith("/"):
        return None
    return path
def page_url(path):
    return "/" if path == "index.html" else "/" + path.removesuffix("index.html")
class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.head = False
        self.title = ""
        self.in_title = False
        self.links = []
        self.metas = []
        self.html_lang = ""
        self.jsonld = 0
        self.refresh = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.html_lang = a.get("lang", "")
        if tag == "head":
            self.head = True
        if not self.head:
            return
        if tag == "title":
            self.in_title = True
        elif tag == "link":
            self.links.append(a)
        elif tag == "meta":
            self.metas.append(a)
            if a.get("http-equiv", "").lower() == "refresh":
                self.refresh = True
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.jsonld += 1
    def handle_data(self, data):
        if self.in_title:
            self.title += data
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.head = False

for file in sorted(ROOT.rglob("*.html")):
    if any(part in {".git", "_site", "vendor", "node_modules", "_includes", "_layouts"} for part in file.relative_to(ROOT).parts):
        continue
    path = file.relative_to(ROOT).as_posix()
    try:
        p = HeadParser()
        p.feed(file.read_text(encoding="utf-8"))
    except Exception as e:
        issue("ERROR", "HTML_PARSE", path, e)
        continue
    metas = {m.get("name", "").lower(): m.get("content", "") for m in p.metas}
    canonical = [x.get("href", "") for x in p.links if x.get("rel", "").lower() == "canonical"]
    alts = [(x.get("hreflang", ""), x.get("href", "")) for x in p.links if x.get("rel", "").lower() == "alternate" and x.get("hreflang")]
    noindex = "noindex" in metas.get("robots", "").lower()
    PAGES[page_url(path)] = dict(path=path, canonical=canonical, alts=alts, noindex=noindex, refresh=p.refresh, lang=p.html_lang)
    if p.refresh:
        if not noindex:
            issue("ERROR", "REDIRECT_INDEXABLE", path, "Meta-refresh page is indexable")
        continue
    if not p.title.strip():
        issue("ERROR", "MISSING_TITLE", path, "Missing HTML title")
    if not p.html_lang:
        issue("WARN", "MISSING_LANG", path, "Missing html lang")
    if not canonical and not noindex:
        issue("WARN", "MISSING_CANONICAL", path, "Indexable page without canonical")
    if len(canonical) > 1:
        issue("ERROR", "MULTIPLE_CANONICAL", path, canonical)
    for u in canonical:
        if local_path(u) is None or not u.startswith(BASE + "/"):
            issue("ERROR", "INVALID_CANONICAL", path, u)
        elif not noindex and local_path(u) != page_url(path):
            issue("WARN", "NON_SELF_CANONICAL", path, u)
    if not noindex:
        if not metas.get("description"):
            issue("WARN", "MISSING_DESCRIPTION", path, "No meta description")
        if not any(m.get("property", "").startswith("og:") for m in p.metas):
            issue("WARN", "MISSING_OG", path, "No Open Graph tags")
        if not any(m.get("name", "").startswith("twitter:") for m in p.metas):
            issue("INFO", "MISSING_TWITTER", path, "No Twitter card tags")
        if not p.jsonld:
            issue("INFO", "MISSING_JSONLD", path, "No JSON-LD")
    codes = [code for code, _ in alts]
    for code, count in Counter(codes).items():
        if count > 1:
            issue("ERROR", "DUPLICATE_HREFLANG", path, code)
    for code, url in alts:
        if not re.fullmatch(r"(?:en|fr|ja|ko|x-default)(?:-[A-Za-z]{2})?", code):
            issue("WARN", "UNEXPECTED_HREFLANG", path, code)
        if local_path(url) is None:
            issue("ERROR", "INVALID_HREFLANG_URL", path, code + " " + url)

# Cross-reference only URLs for which a concrete HTML file is present.
for own_url, p in PAGES.items():
    if p["refresh"]:
        continue
    for code, url in p["alts"]:
        target_url = local_path(url)
        if target_url is None:
            continue
        target = PAGES.get(target_url)
        if target is None:
            issue("WARN", "HREFLANG_TARGET_UNRESOLVED", p["path"], code + " " + url + " (may be generated by Jekyll)")
            continue
        if target["refresh"] or target["noindex"]:
            issue("WARN", "HREFLANG_TO_NONINDEX", p["path"], code + " " + url)
        if code != "x-default" and target["lang"] and target["lang"].split("-")[0] != code.split("-")[0]:
            issue("ERROR", "HREFLANG_LANG_MISMATCH", p["path"], code + " -> " + target["path"] + " lang=" + target["lang"])
        if code != "x-default" and not any(local_path(back) == own_url for _, back in target["alts"]):
            issue("WARN", "HREFLANG_NOT_RECIPROCAL", p["path"], code + " -> " + target["path"])

sitemap = ROOT / "sitemap.xml"
sitemap_urls = []
if sitemap.exists():
    raw = sitemap.read_text(encoding="utf-8")
    raw = re.sub(r"\A---\s*\n---\s*\n", "", raw)
    try:
        xml = ET.fromstring(raw)
        sitemap_urls = [x.text.strip() for x in xml.iter() if x.tag.endswith("}loc") or x.tag == "loc" if x.text]
    except ET.ParseError as e:
        issue("ERROR", "SITEMAP_XML", "sitemap.xml", e)
    for u, count in Counter(sitemap_urls).items():
        if count > 1:
            issue("ERROR", "SITEMAP_DUPLICATE", "sitemap.xml", u)
        path = local_path(u)
        if path is None or not u.startswith(BASE + "/"):
            issue("ERROR", "SITEMAP_INVALID_URL", "sitemap.xml", u)
        elif path in PAGES:
            if PAGES[path]["refresh"] or PAGES[path]["noindex"]:
                issue("ERROR", "SITEMAP_NONINDEX", "sitemap.xml", u)
        elif path != "/" and not (ROOT / path.lstrip("/") / "index.md").exists():
            # Jekyll _posts can generate routes absent from the source tree.
            if not path.startswith("/gray-note/"):
                issue("WARN", "SITEMAP_TARGET_UNRESOLVED", "sitemap.xml", u)
    sitemap_paths = {local_path(u) for u in sitemap_urls}
    for u, p in PAGES.items():
        if not p["refresh"] and not p["noindex"] and p["canonical"] and local_path(p["canonical"][0]) == u and u not in sitemap_paths:
            issue("WARN", "INDEXABLE_NOT_IN_SITEMAP", p["path"], BASE + u)
else:
    issue("ERROR", "MISSING_SITEMAP", "sitemap.xml", "File not found")

counts = Counter(level for level, *_ in ISSUES)
lines = ["# SEO source audit", "", f"HTML pages scanned: **{len(PAGES)}**", f"Sitemap URLs: **{len(sitemap_urls)}**", f"Findings: **{len(ISSUES)}** (ERROR {counts['ERROR']}, WARN {counts['WARN']}, INFO {counts['INFO']})", "", "Source-only check: HTTP status, deployed Jekyll output, and Google/Naver indexing are not verified.", "", "## Findings", "", "| Severity | Code | File | Detail |", "|---|---|---|---|"]
for level, code, path, detail in sorted(ISSUES, key=lambda x: ({"ERROR":0,"WARN":1,"INFO":2}[x[0]], x[2], x[1])):
    clean = lambda s: str(s).replace("|", "\\|").replace("`", "'")
    lines.append(f"| {level} | {code} | `{clean(path)}` | {clean(detail)} |")
if not ISSUES:
    lines.append("| OK | — | — | No findings |")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"SEO audit: {len(PAGES)} HTML, {len(sitemap_urls)} sitemap URLs; {dict(counts)}")
print("Report:", REPORT)
# Report-only mode: findings are reviewed before changing production pages.
sys.exit(0)
