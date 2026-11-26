#!/usr/bin/env python3
"""Read-only Gray Note release planner. Prints a unified diff; never writes files.
Run from a local checkout: python3 _maintenance/plan_gray_note_release.py release.json
Input: {"number":"012","date":"2026-11-26","title":"Approved English title",
"subtitle":"Optional subtitle","editions":{"en":"/absolute/path/en.html","ko":"/absolute/path/ko.html"}}
Edition files must be complete, reviewed standalone HTML using the existing site
structure, outside the checkout. No translation, template migration or deployment.
Only new multilingual Gray Note entries, with English present, are supported.
For existing editions, photo diaries or other sections, use manual review.
"""
import argparse
import datetime as dt
import difflib
import html
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://jin-in-seoul.com"
LANG = {"en": "English", "ja": "Japanese", "fr": "French", "ko": "Korean"}
LABEL = {"en": "English", "ja": "日本語", "fr": "Français", "ko": "한국어"}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def insert_before(text, marker, addition):
    require(text.count(marker) == 1, "Missing or ambiguous anchor: " + marker)
    return text.replace(marker, addition + marker, 1)

def date_label(date):
    return date.strftime("%B") + " " + str(date.day) + ", " + str(date.year)

def join_names(names):
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]

def plan(root, spec, input_dir):
    number = spec["number"]
    require(isinstance(number, str) and re.fullmatch(r"[0-9]{3}", number), "Expected three-digit work number")
    date = dt.date.fromisoformat(spec["date"])
    title = html.escape(spec["title"].strip())
    subtitle = html.escape(spec.get("subtitle", "").strip())
    require(bool(title), "English title required")
    editions = spec["editions"]
    require(isinstance(editions, dict) and "en" in editions and set(editions) <= set(LANG), "English and supported languages required")
    langs = [lang for lang in LANG if lang in editions]
    require(not (root / "gray-note" / number).exists(), "Work already exists; no overwrite allowed")
    routes = {lang: f"/gray-note/{number}/{lang}/" for lang in langs}
    changes = {}
    for lang in langs:
        source = (input_dir / editions[lang]).resolve()
        require(not source.is_relative_to(root.resolve()), "Draft must be outside repository")
        raw = source.read_text(encoding="utf-8")
        require(raw.startswith("---\n") and '<article class="gray-note-post">' in raw, "Expected standalone Gray Note HTML")
        require(f'<html lang="{lang}">' in raw, "HTML language mismatch")
        require(f'<link rel="canonical" href="{DOMAIN}{routes[lang]}">' in raw, "Canonical mismatch")
        require('name="robots" content="index,follow' in raw, "Index policy mismatch")
        require("<h1" in raw and "</article>" in raw, "Missing article or title")
        head = raw.split("</head>", 1)[0]
        expected = {key: DOMAIN + value for key, value in routes.items()}
        expected["x-default"] = DOMAIN + routes["en"]
        found = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', head)
        require(len(found) == len(expected) and dict(found) == expected, "Incorrect hreflang: " + lang)
        require("noindex" not in head.lower(), "Unexpected noindex")
        changes[routes[lang].strip("/") + "/index.html"] = ("", raw)

    links = [f'<a href="{routes[l]}">{LABEL[l]}</a>' for l in langs]
    date_text = date_label(date)
    for path in ("gray-note/index.html", "index.html", "sitemap.xml", "publication-log/index.html"):
        original = (root / path).read_text(encoding="utf-8")
        require(all(route not in original for route in routes.values()), "Route already listed in " + path)
        updated = original
        if path == "gray-note/index.html":
            anchor = '      <article class="gray-note-list-item">'
            first = original.index(anchor)
            dates = re.findall(r'<time datetime="([0-9]{4}-[0-9]{2}-[0-9]{2})', original)
            require(bool(dates) and date >= dt.date.fromisoformat(dates[0]), "Backdated entry requires manual review")
            joined = '<span aria-hidden="true"> · </span>'.join(links)
            block = f'      <article class="gray-note-list-item">\n        <time datetime="{date}T00:00:00+09:00">{date_text}</time>\n        <h2><a href="{routes["en"]}">{title}</a></h2>\n'
            if subtitle:
                block += f'        <p class="gray-note-list-subtitle">{subtitle}</p>\n'
            block += f'        <p class="gray-note-language-links">{joined}</p>\n      </article>\n'
            updated = original[:first] + block + original[first:]
        elif path == "index.html":
            # Homepage features are an editorial selection, not an automatic archive.
            # Only create a proposal when explicitly requested.
            if not spec.get("feature_on_home", False):
                continue
            marker = '<div class="galactic-supplements" aria-label="Featured Gray Note writings">'
            joined = " · ".join(links)
            block = f'\n<section class="galactic-supplement">\n          <h2><a class="galactic-supplement-title-link" href="{routes["en"]}">{title}</a></h2>\n'
            if subtitle:
                block += f'          <p class="home-list-subtitle">{subtitle}</p>\n'
            block += f'          <p class="translation-principles-links">{joined}</p>\n        </section>'
            require(original.count(marker) == 1, "Homepage anchor ambiguous")
            updated = original.replace(marker, marker + block, 1)
        elif path == "sitemap.xml":
            block = "".join(f'  <url>\n    <loc>{DOMAIN}{routes[l]}</loc>\n  </url>\n' for l in langs)
            updated = insert_before(original, "</urlset>", block)
            xml = updated.split("---", 2)[-1].strip()
            # Existing Liquid may prevent source XML parsing. Never rewrite it.
            if "{%" not in xml and "{{" not in xml:
                ET.fromstring(xml)
        else:
            marker = '    <div class="publication-log">'
            dates = re.findall(r'<h2>([A-Za-z]+ [0-9]+, [0-9]{4})</h2>', original)
            require(bool(dates) and date >= dt.datetime.strptime(dates[0], "%B %d, %Y").date(), "Backdated log requires manual review")
            names = join_names([LANG[l] for l in langs])
            label = f"<em>{title}</em>" + (f" — <em>{subtitle}</em>" if subtitle else "")
            block = f'\n      <section>\n        <h2>{date_text}</h2>\n        <h3>Gray Note</h3>\n        <ul>\n          <li>{label} added in {names}</li>\n        </ul>\n      </section>\n'
            require(original.count(marker) == 1, "Publication Log anchor ambiguous")
            updated = original.replace(marker, marker + block, 1)
        require(updated != original, "No proposed change: " + path)
        changes[path] = (original, updated)
    return changes

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    try:
        spec_path = args.spec.resolve()
        changes = plan(ROOT, json.loads(spec_path.read_text(encoding="utf-8")), spec_path.parent)
        print("READ ONLY — proposed files:", file=sys.stderr)
        for path, (old, new) in changes.items():
            print("  " + path, file=sys.stderr)
            sys.stdout.writelines(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile="a/" + path if old else "/dev/null", tofile="b/" + path))
        print("No files written. Review SEO metadata, body, dates, search index and deployment before separate authorized publication.", file=sys.stderr)
    except (ValueError, KeyError, TypeError, OSError, ET.ParseError) as exc:
        parser.exit(1, f"STOP: {exc}\n")

if __name__ == "__main__":
    main()
