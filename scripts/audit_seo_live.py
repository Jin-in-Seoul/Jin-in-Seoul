#!/usr/bin/env python3
"""Read-only deployed-site SEO audit. Standard library; no repository changes."""
import concurrent.futures
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
import re
import ssl
import xml.etree.ElementTree as ET

BASE = "https://jin-in-seoul.com"
OUT = Path("seo-live-report.md")
ISSUES = []
def record(level, code, url, detail):
    ISSUES.append((level, code, url, str(detail).replace("|", "/").replace("\n", " ")[:250]))
def fetch(url):
    try:
        req = Request(url, headers={"User-Agent": "Jin-in-Seoul-SEO-Audit/1.0 (+https://jin-in-seoul.com/)"})
        with urlopen(req, timeout=20) as resp:
            return resp.status, resp.url, resp.headers.get("Content-Type", ""), resp.read(3_000_000).decode("utf-8", "replace"), ""
    except HTTPError as e:
        return e.code, url, "", "", str(e)
    except (URLError, TimeoutError, OSError, ValueError) as e:
        return 0, url, "", "", str(e)

class Head(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.head = False
        self.title = ""
        self.in_title = False
        self.links = []
        self.metas = []
        self.lang = ""
        self.jsonld = 0
        self.refresh = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "head":
            self.head = True
        if not self.head:
            return
        if tag == "title":
            self.in_title = True
        if tag == "link":
            self.links.append(a)
        if tag == "meta":
            self.metas.append(a)
            if a.get("http-equiv", "").lower() == "refresh":
                self.refresh = True
        if tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.jsonld += 1
    def handle_data(self, data):
        if self.in_title:
            self.title += data
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "head":
            self.head = False

def same_url(a, b):
    return a.rstrip("/") == b.rstrip("/")
status, final, typ, body, err = fetch(BASE + "/sitemap.xml")
urls = []
if status != 200:
    record("ERROR", "SITEMAP_HTTP", BASE + "/sitemap.xml", f"HTTP {status} {err}")
else:
    try:
        root = ET.fromstring(body)
        urls = [x.text.strip() for x in root.iter() if x.tag.rsplit("}", 1)[-1] == "loc" and x.text]
    except ET.ParseError as e:
        record("ERROR", "SITEMAP_XML", BASE + "/sitemap.xml", str(e))
for u, n in Counter(urls).items():
    if n > 1:
        record("ERROR", "SITEMAP_DUPLICATE", u, str(n))
    if urlsplit(u).netloc != "jin-in-seoul.com":
        record("ERROR", "EXTERNAL_SITEMAP_URL", u, "Unexpected domain")

pages = {}
def inspect(url):
    status, final, typ, html, err = fetch(url)
    if status != 200:
        return url, status, final, err, None
    p = Head()
    try:
        p.feed(html)
    except Exception as e:
        return url, status, final, str(e), None
    return url, status, final, "", p

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for url, status, final, err, p in pool.map(inspect, urls):
        if status != 200:
            record("ERROR", "PAGE_HTTP", url, f"HTTP {status} {err}")
            continue
        if not same_url(url, final):
            record("WARN", "PAGE_REDIRECT", url, "Resolved to " + final)
        if p is None:
            record("ERROR", "HTML_PARSE", url, err)
            continue
        meta = {x.get("name", "").lower(): x.get("content", "") for x in p.metas}
        canon = [x.get("href", "") for x in p.links if x.get("rel", "").lower() == "canonical"]
        alts = [(x.get("hreflang", ""), x.get("href", "")) for x in p.links if x.get("rel", "").lower() == "alternate" and x.get("hreflang")]
        pages[url] = (p, alts)
        if not p.title.strip():
            record("ERROR", "TITLE_MISSING", url, "Missing title")
        if not p.lang:
            record("WARN", "LANG_MISSING", url, "Missing html lang")
        if "noindex" in meta.get("robots", "").lower():
            record("ERROR", "SITEMAP_NOINDEX", url, "URL in sitemap has noindex")
        if p.refresh:
            record("ERROR", "SITEMAP_META_REFRESH", url, "URL in sitemap is a redirect page")
        if len(canon) != 1 or not same_url(canon[0], url):
            record("WARN", "CANONICAL_MISMATCH", url, repr(canon))
        if not meta.get("description"):
            record("WARN", "DESCRIPTION_MISSING", url, "No description")
        if not any(x.get("property", "").startswith("og:") for x in p.metas):
            record("WARN", "OG_MISSING", url, "No OG tags")
        if not p.jsonld:
            record("INFO", "JSONLD_MISSING", url, "No JSON-LD")
        for lang, target in alts:
            if not re.fullmatch(r"(en|fr|ja|ko|x-default)(-[A-Za-z]{2})?", lang):
                record("WARN", "HREFLANG_CODE", url, lang)
            if urlsplit(target).netloc != "jin-in-seoul.com":
                record("ERROR", "HREFLANG_EXTERNAL", url, lang + " " + target)

for url, (p, alts) in pages.items():
    for lang, target in alts:
        target_entry = next((v for k, v in pages.items() if same_url(k, target)), None)
        if target_entry is None:
            # Alternate can be an intentionally unsitemapped page; don't assert broken.
            record("INFO", "HREFLANG_TARGET_NOT_AUDITED", url, lang + " " + target)
            continue
        tp, back = target_entry
        if lang != "x-default" and tp.lang and tp.lang.split("-")[0] != lang.split("-")[0]:
            record("ERROR", "HREFLANG_LANGUAGE", url, lang + " target lang=" + tp.lang)
        if lang != "x-default" and not any(same_url(back_url, url) for _, back_url in back):
            record("WARN", "HREFLANG_NONRECIPROCAL", url, lang + " " + target)

counts = Counter(x[0] for x in ISSUES)
lines = ["# Deployed SEO audit", "", f"Site: {BASE}", f"Sitemap HTTP: {status if not urls else '200'}", f"Sitemap entries: **{len(urls)}**", f"Fetched HTML: **{len(pages)}**", f"Findings: ERROR {counts['ERROR']}, WARN {counts['WARN']}, INFO {counts['INFO']}", "", "Only sitemap URLs are fetched. Search Console/Naver indexing is not checked.", "", "| Severity | Code | URL | Detail |", "|---|---|---|---|"]
for level, code, url, detail in sorted(ISSUES, key=lambda v: ({"ERROR":0,"WARN":1,"INFO":2}[v[0]], v[2], v[1])):
    lines.append(f"| {level} | {code} | {url} | {detail} |")
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"LIVE SEO: {len(urls)} sitemap URLs, {len(pages)} fetched, ERROR={counts['ERROR']} WARN={counts['WARN']} INFO={counts['INFO']}")
print("Report:", OUT)
