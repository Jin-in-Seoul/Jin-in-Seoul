#!/usr/bin/env python3
"""One-time, conservative, metadata-only terminology cleanup (2026-11-16)."""
from pathlib import Path
import re
import json
import sys

ROOT = Path(".")
PAT = re.compile(r"(?i)experimental|expériment(?:al|ale|aux|ales)|실험적|実験的")
META = re.compile(r'<meta\s+(?:name="(?:description|twitter:description)"|property="og:description")\s+content="([^"]*)"', re.I)
DESC_JSON = re.compile(r'("description"\s*:\s*")((?:[^"\\]|\\.)*)(")')
GENRE_JSON = re.compile(r'(?i),?\s*"Experimental [Ll]iterature"\s*,?')
GROUPS = {
  "en": ("A Dictionary of Galactic Extinction", " (Book 1 of 10)"),
  "ko": ("《은하 멸망 사전》", "(총 10권 중 제1권)"),
  "ja": ("『銀河滅亡辞典』", "（全10巻中第1巻）"),
  "fr": ("Dictionnaire de l’extinction galactique", " (livre 1 sur 10)"),
}

def cleanup(description, lang, novel):
    orig = description
    description = description.replace("an experimental literary novel", "a novel")
    description = description.replace("an experimental novel", "a novel")
    description = description.replace("experimental literary fiction", "literary fiction")
    description = description.replace("experimental literature", "literature")
    description = description.replace("Experimental literature", "Literature")
    description = description.replace("experimental literary", "literary")
    description = description.replace("experimental ", "")
    description = description.replace("실험적 장편소설", "장편소설")
    description = description.replace("실험적인 장편소설", "장편소설")
    description = description.replace("실험적 ", "")
    description = description.replace("実験的な長編小説", "長編小説")
    description = description.replace("実験的な長編文学作品", "長編文学作品")
    description = description.replace("実験的な", "")
    description = description.replace("roman littéraire expérimental", "roman")
    description = description.replace("roman expérimental", "roman")
    description = description.replace("littérature expérimentale", "littérature")
    description = description.replace("expérimental ", "")
    if novel and lang in GROUPS:
        title, label = GROUPS[lang]
        if title in description and label not in description:
            description = description.replace(title, title + label, 1)
    return description

def process(path, raw):
    name = path.as_posix()
    head, sep, tail = raw.partition("</head>")
    if not sep:
        return raw, 0, []
    lang = None
    if name.startswith("a-dictionary-of-galactic-extinction/"):
        bits = name.split("/")
        if len(bits) > 2 and bits[1] in GROUPS:
            lang = bits[1]
    novel = bool(lang and (name.endswith(f"/{lang}/index.html") or "/part-" in name and "/entry-" in name or "/appendix/" in name))
    changes = 0
    warnings = []
    old_meta = [m.group(1) for m in META.finditer(head)]
    description_map = {}
    for desc in old_meta:
        newdesc = cleanup(desc, lang, novel)
        if newdesc != desc:
            description_map[desc] = newdesc
    if name == "index.html":
        old_long = "Jin-in-Seoul is an author's literary website publishing novels, short fiction, and experimental literature. In particular, A Dictionary of Galactic Extinction is a work of experimental literary fiction using science-fiction themes and dictionary and archival forms, not an SF setting guide or a serialized web novel."
        new_long = "Jin-in-Seoul is an author's literary website publishing novels, short stories, and essays. A Dictionary of Galactic Extinction is a ten-book novel series told through science-fiction themes, dictionary entries, records, and archival documents."
        if old_long in head:
            description_map[old_long] = new_long
    for before, after in description_map.items():
        if before in head:
            head = head.replace(before, after)
            changes += 1
    # JSON-LD descriptions not shared with meta descriptions
    def sub_json(match):
        global nothing
        nonlocal_changes[0] += 0
        val = match.group(2)
        if '\\' in val:
            return match.group(0)
        clean = cleanup(val, lang, novel)
        if name == "index.html":
            clean = clean.replace("novels, short fiction, and literature", "novels, short stories, and essays")
            clean = clean.replace("a work of literary fiction using science-fiction themes and dictionary and archival forms, not an SF setting guide or a serialized web novel", "a ten-book novel series using science-fiction themes, dictionary entries, records, and archival documents")
        return match.group(1) + clean + match.group(3)
    nonlocal_changes = [0]
    head = DESC_JSON.sub(sub_json, head)
    head = re.sub(r',\s*"Experimental Literature"', "", head)
    head = re.sub(r'"Experimental Literature"\s*,\s*', "", head)
    head = re.sub(r',\s*"Experimental literature"', "", head)
    head = re.sub(r'"Experimental literature"\s*,\s*', "", head)
    if name == "index.html":
        head = head.replace("Experimental Literature", "Essays")
        tail = tail.replace("A Literary Site for Novels, Short Stories &amp; Experimental Literature", "A Literary Site for Novels, Short Stories &amp; Essays")
        tail = tail.replace("A Literary Site for Novels, Short Stories & Experimental Literature", "A Literary Site for Novels, Short Stories & Essays")
    new = head + sep + tail
    # Never remove 'experiment' from body prose or Thought Experiment Notes.
    if name != "index.html" and tail != raw.partition("</head>")[2]:
        raise ValueError("Body changed in " + name)
    if new != raw:
        changes += 1
    if PAT.search(head):
        context = [head[max(0,m.start()-55):m.end()+65] for m in PAT.finditer(head)]
        warnings.extend(context[:3])
    return new, changes, warnings

changed = []
warnings = []
for path in sorted(ROOT.rglob("*.html")):
    raw = path.read_text(encoding="utf-8")
    updated, count, warn = process(path,raw)
    if count:
        path.write_text(updated, encoding="utf-8")
        changed.append(path.as_posix())
    if warn:
        warnings.append((path.as_posix(), warn))
print("Modified files:",len(changed))
for p in changed:
    print("CHANGED",p)
print("Remaining terminology in HEAD:",len(warnings))
for p,w in warnings[:30]:
    print("REVIEW",p,w)
if warnings:
    sys.exit("Refusing commit until remaining HEAD descriptions have been inspected")
