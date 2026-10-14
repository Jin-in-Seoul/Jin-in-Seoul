#!/usr/bin/env python3
"""Read-only audit of CSS links and language-specific typography wiring.

Run from repository root: python3 scripts/audit_css_links.py
Does not edit files or fetch remote resources.
"""
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
STYLE_LINK = re.compile(r'<link\b(?=[^>]*\brel=["\']stylesheet["\'])[^>]*\bhref=["\']([^"\']+)["\'][^>]*>', re.I)
BASE = "assets/style.css"
STORY_CSS = "short-stories/latin-first-paragraph.css"
CHILD_CSS = "childrens-books/latin-first-paragraph.css"
DICT = "a-dictionary-of-galactic-extinction"
issues = []
versions = defaultdict(Counter)
usage = Counter()
scanned = 0

def relpath(p):
    return p.relative_to(ROOT).as_posix()

for page in sorted(ROOT.rglob("*.html")):
    if ".git" in page.parts:
        continue
    scanned += 1
    rel = relpath(page)
    html = page.read_text(encoding="utf-8")
    hrefs = STYLE_LINK.findall(html)
    linked = set()
    for href in hrefs:
        u = urlsplit(href)
        if u.scheme or u.netloc or u.path.startswith("//"):
            continue
        target = (ROOT / u.path.lstrip("/")) if u.path.startswith("/") else (page.parent / u.path)
        target = target.resolve()
        if not target.is_relative_to(ROOT):
            issues.append(f"{rel}: CSS path escapes repository: {href}")
            continue
        resolved = relpath(target)
        linked.add(resolved)
        usage[resolved] += 1
        if not target.is_file():
            issues.append(f"{rel}: missing CSS: {href}")
        if resolved == BASE:
            versions[u.query or "(none)"] += 1
    bits = rel.split("/")
    if len(bits) == 4 and bits[0] in ("short-stories", "childrens-books") and bits[3] == "index.html":
        work, slug, lang, _ = bits
        expected = (STORY_CSS if work == "short-stories" else CHILD_CSS) if lang in ("en", "fr") else None
        if expected and expected not in linked:
            issues.append(f"{rel}: missing Latin-language CSS: {expected}")
        if not expected and (STORY_CSS in linked or CHILD_CSS in linked):
            issues.append(f"{rel}: Latin-language CSS linked from {lang}")

print(f"HTML files scanned: {scanned}")
print("CSS link targets (path: links):")
for target, count in sorted(usage.items()):
    print(f"  {target}: {count}")
print("Global CSS cache query variants:")
for query, count in sorted(versions.items()):
    print(f"  {query}: {count}")
print(f"Warnings: {len(issues)}")
for issue in issues:
    print(f"  WARNING: {issue}")
sys.exit(1 if issues else 0)
