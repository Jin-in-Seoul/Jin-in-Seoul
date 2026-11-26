#!/usr/bin/env python3
"""Read-only cross-collection publication planner (Python 3.10+).

Usage: python3 _maintenance/plan_release.py release.json
       python3 _maintenance/plan_release.py --self-test

Gray Note: {"family":"gray-note", ...existing Gray Note planner inputs...}
Other families: {"family":"short-stories","date":"2026-11-26",
 "pages":{"/short-stories/example/en/":"en.html"},
 "list_edits":[{"path":"short-stories/index.html","old":"exact approved anchor",
 "new":"exact replacement including new listing"}],
 "log_html":"<h3>Short Stories</h3><ul><li>Approved publication wording</li></ul>"}
Draft files and JSON must be outside the repository. List edits are explicit
approved snippets; the planner does not invent titles, translations or layout.
Existing edition expansion, multi-page new books and asset uploads need manual
review. This tool never writes files, runs Git commands or publishes anything.
"""
import argparse
import datetime as dt
import difflib
import html
import json
from pathlib import Path
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from plan_gray_note_release import plan as gray_plan

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://jin-in-seoul.com"
LANGS = ("en", "ja", "fr", "ko")
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
LANG = r"(?:en|ja|fr|ko)"
PATTERNS = {
    "a-dictionary-of-galactic-extinction": rf"/a-dictionary-of-galactic-extinction/{LANG}/part-[0-9]{{2}}/entry-[0-9]{{2}}/",
    "the-last-no-mercy-of-elian-mor": rf"/the-last-no-mercy-of-elian-mor/{LANG}/part-[0-9]{{2}}/entry-[0-9]{{2}}/",
    "scarecrow-distance": rf"/scarecrow-distance/{LANG}/chapter-[0-9]{{2}}/",
    "sweater": rf"/sweater/{LANG}/chapter-[0-9]{{2}}/",
    "short-stories": rf"/short-stories/{SLUG}/{LANG}/",
    "childrens-books": rf"/childrens-books/{SLUG}/{LANG}/",
    "tales-from-premodern-korea": rf"/tales-from-premodern-korea/{SLUG}/{LANG}/",
    "haiku": r"/haiku/[0-9]{4}/[0-9]{2}/[0-9]{2}/[0-9]{3}/",
    "music": rf"/music/{SLUG}/",
}
SINGLE = {"haiku", "music"}
SERIAL = {"a-dictionary-of-galactic-extinction", "scarecrow-distance", "sweater"}

def require(ok, msg):
    if not ok:
        raise ValueError(msg)

def read(root, path):
    p = root / path
    require(p.resolve().is_relative_to(root.resolve()) and p.is_file(), "Missing or unsafe file: " + path)
    return p.read_bytes().decode("utf-8")

def allowed_lists(family, routes):
    if family in SERIAL:
        return {family + "/" + r.split("/")[2] + "/index.html" for r in routes}
    if family == "the-last-no-mercy-of-elian-mor":
        return {"index.html"}
    return {family + "/index.html"}

def plan(root, spec, input_dir):
    family = spec["family"]
    if family == "gray-note":
        return gray_plan(root, spec, input_dir)
    require(family in PATTERNS, "Unsupported family")
    date = dt.date.fromisoformat(spec["date"])
    pages = spec["pages"]
    require(isinstance(pages, dict) and pages, "Pages required")
    routes = list(pages)
    require(all(re.fullmatch(PATTERNS[family], r) for r in routes), "Route outside family rule")
    require(family not in SINGLE or len(routes) == 1, "Single-page collection")
    if family not in SINGLE:
        def locale(route):
            return route.split("/")[2 if family in SERIAL or family == "the-last-no-mercy-of-elian-mor" else 3]
        variants = {locale(r): r for r in routes}
        require(len(variants) == len(routes) and "en" in variants, "New work requires distinct locales including English")
        require(len({r.replace("/"+locale(r)+"/", "/{lang}/", 1) for r in routes}) == 1, "One work/entry per plan")
        expected = {l: DOMAIN + variants[l] for l in LANGS if l in variants}
        expected["x-default"] = DOMAIN + variants["en"]
    else:
        expected = {}
    if family == "haiku":
        require(routes[0].split("/")[2:5] == date.isoformat().split("-"), "Haiku date/route mismatch")
    changes = {}
    for route, source_name in pages.items():
        target = route.strip("/") + "/index.html"
        require(not (root / target).exists(), "Existing page: " + target)
        source = (input_dir / source_name).resolve()
        require(not source.is_relative_to(root.resolve()), "Draft must be outside checkout")
        raw = source.read_bytes().decode("utf-8")
        require(raw.startswith("---\n") and "</head>" in raw and "<h1" in raw, "Standalone HTML required")
        head = raw.split("</head>", 1)[0]
        require(f'<link rel="canonical" href="{DOMAIN}{route}">' in head, "Canonical mismatch: " + route)
        require('name="robots" content="index,follow' in head and "noindex" not in head.lower(), "Index policy mismatch")
        found = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', head)
        if family not in SINGLE:
            require(f'<html lang="{locale(route)}">' in head, "HTML language mismatch")
            require(len(found) == len(expected) and dict(found) == expected, "Hreflang mismatch")
        else:
            require(not found, "Single-page work must not advertise separate editions")
            marker = '<article class="' + family + '-post">'
            require(marker in raw, "Missing collection article")
            for lang in LANGS:
                marker = f'<section lang="{lang}">' if family == "haiku" else f'<section class="lyrics-section lyrics-{lang}" lang="{lang}">'
                require(marker in raw, "Missing language section: " + lang)
        # Ensure JSON-LD parses; detailed metadata remains subject to existing audit.
        scripts = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', head, re.S)
        require(bool(scripts), "Missing JSON-LD")
        for script in scripts:
            json.loads(script)
        changes[target] = ("", raw)

    required = allowed_lists(family, routes)
    edits = spec["list_edits"]
    require(isinstance(edits, list), "List edits must be explicit")
    touched = set()
    for edit in edits:
        path, old, new = edit["path"], edit["old"], edit["new"]
        require(path in required | {"index.html"}, "Unapproved listing path")
        require(old and old != new, "Empty/no-op listing edit")
        original, current = changes.get(path, (None, None))
        if original is None:
            original = current = read(root, path)
        require(current.count(old) == 1, "Missing or ambiguous listing anchor: " + path)
        changes[path] = (original, current.replace(old, new, 1))
        touched.add(path)
    require(required <= touched, "Missing required listing edit")
    # Check each edition is linked in its relevant listing, resolving relative links.
    from urllib.parse import urljoin
    for route in routes:
        relevant = allowed_lists(family, [route])
        require(any(any(urljoin(DOMAIN + "/" + p.removesuffix("index.html"), html.unescape(href)) == DOMAIN + route
                        for href in re.findall(r'href="([^"]+)"', changes[p][1]))
                    for p in relevant), "Missing proposed listing link: " + route)

    path = "sitemap.xml"
    original = read(root, path)
    require(original.count("</urlset>") == 1, "Unexpected sitemap structure")
    require(all(DOMAIN + r not in original for r in routes), "Already in sitemap")
    addition = "".join(f"  <url>\n    <loc>{DOMAIN}{r}</loc>\n  </url>\n" for r in routes)
    new = original.replace("</urlset>", addition + "</urlset>", 1)
    xml = new.split("---", 2)[-1].strip()
    if "{%" not in xml and "{{" not in xml:
        ET.fromstring(xml)
    changes[path] = (original, new)

    path = "publication-log/index.html"
    original = read(root, path)
    marker = '    <div class="publication-log">'
    require(original.count(marker) == 1, "Publication Log anchor ambiguous")
    dates = re.findall(r'<h2>([A-Za-z]+ [0-9]+, [0-9]{4})</h2>', original)
    require(dates and date >= dt.datetime.strptime(dates[0], "%B %d, %Y").date(), "Backdated release requires manual review")
    log = spec["log_html"]
    require(re.fullmatch(r"<h3>[^<]+</h3>\s*<ul>\s*<li>.*?</li>\s*</ul>", log, re.S), "Approved log heading and entry required")
    require(not re.search(r"<(?:script|style|section|h2)\b", log, re.I), "Unexpected log markup")
    label = date.strftime("%B") + " " + str(date.day) + ", " + str(date.year)
    block = f"\n      <section>\n        <h2>{label}</h2>\n        {log}\n      </section>\n"
    changes[path] = (original, original.replace(marker, marker + block, 1))
    return changes

def self_test():
    with tempfile.TemporaryDirectory() as temp:
        parent = Path(temp)
        root = parent / "repo"
        root.mkdir()
        for family in PATTERNS:
            if family in SINGLE:
                route = "/haiku/2026/11/26/999/" if family == "haiku" else "/music/test-release/"
            elif family in SERIAL or family == "the-last-no-mercy-of-elian-mor":
                route = "/" + family + "/en/" + ("chapter-99/" if family in {"sweater","scarecrow-distance"} else "part-01/entry-99/")
            else:
                route = "/" + family + "/test-release/en/"
            listing = next(iter(allowed_lists(family, [route])))
            for p, value in [(listing, "ANCHOR"), ("sitemap.xml", "<urlset></urlset>"), ("publication-log/index.html", '    <div class="publication-log"><h2>November 25, 2026</h2></div>')]:
                target = root / p
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(value, encoding="utf-8")
            canonical = f'<link rel="canonical" href="{DOMAIN}{route}">'
            alt = "" if family in SINGLE else "".join(f'<link rel="alternate" hreflang="{l}" href="{DOMAIN}{route}">' for l in ("en","x-default"))
            body = '<h1>Test</h1>'
            if family in SINGLE:
                body += '<article class="' + family + '-post">'
                for lang in LANGS:
                    body += f'<section lang="{lang}"></section>' if family == "haiku" else f'<section class="lyrics-section lyrics-{lang}" lang="{lang}"></section>'
                body += "</article>"
            draft = parent / "draft.html"
            draft.write_text('---\n---\n<html lang="en"><head>'+canonical+alt+'<meta name="robots" content="index,follow"><script type="application/ld+json">{}</script></head>'+body, encoding="utf-8")
            spec = {"family":family,"date":"2026-11-26","pages":{route:str(draft)},"list_edits":[{"path":listing,"old":"ANCHOR","new":f'<a href="{route}">Test</a>'}],"log_html":"<h3>Test</h3><ul><li>Test added</li></ul>"}
            before = {p.relative_to(root):p.read_bytes() for p in root.rglob("*") if p.is_file()}
            result = plan(root,spec,parent)
            require(len(result)==4 and all(p.read_bytes()==v for k,v in before.items() for p in [root/k]), "Unexpected plan or write")
            spec["list_edits"][0]["old"]="MISSING"
            try:
                plan(root,spec,parent)
            except ValueError:
                pass
            else:
                raise AssertionError("Missing anchor accepted")
            print("PASS",family)
    print("SELF-TEST PASS (synthetic fixtures; not a deployment test)")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            return
        require(args.spec is not None, "Specification required")
        p = args.spec.resolve()
        require(not p.is_relative_to(ROOT), "Specification must be outside checkout")
        changes = plan(ROOT, json.loads(p.read_text(encoding="utf-8")), p.parent)
        for path, (old,new) in changes.items():
            sys.stdout.writelines(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile="a/"+path if old else "/dev/null",tofile="b/"+path))
        print("READ ONLY: review listing snippets, metadata, assets, search index, language order and all diffs before publication.",file=sys.stderr)
    except (ValueError, KeyError, TypeError, OSError, ET.ParseError) as exc:
        parser.exit(1, f"STOP: {exc}\n")

if __name__ == "__main__":
    main()
