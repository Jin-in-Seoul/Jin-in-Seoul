from pathlib import Path
import re

ROOT=Path(".")
css_path=ROOT/"assets/style.css"
css=css_path.read_text(encoding="utf-8")

block = """
/* Short-story book-style paragraph setting */
.short-story-prose p {
  margin: 0;
  text-indent: 1em;
}
.short-story-prose p.section-number,
.short-story-prose p[style*="text-align:center"],
.short-story-prose p[style*="text-align: center"] {
  text-indent: 0;
}
"""

if "/* Short-story book-style paragraph setting */" not in css:
    css = css.rstrip() + "\n\n" + block.strip() + "\n"
css_path.write_text(css, encoding="utf-8")

files=sorted((ROOT/"short-stories").glob("*/*/index.html"))
story_files=[p for p in files if re.fullmatch(r"short-stories/[^/]+/(en|fr|ja|ko)/index\.html", p.as_posix())]
assert len(story_files)==22, [p.as_posix() for p in story_files]

changed=[]
for p in story_files:
    s=p.read_text(encoding="utf-8")
    if '<article class="prose short-story-prose">' not in s:
        if '<article class="prose">' not in s:
            raise RuntimeError(f"article marker missing: {p}")
        s=s.replace('<article class="prose">','<article class="prose short-story-prose">',1)
    s=re.sub(r'style\.css\?v=\d+', 'style.css?v=050', s)
    p.write_text(s,encoding="utf-8")
    changed.append(p.as_posix())

# Safety checks: content paragraphs untouched except article class and stylesheet query.
for p in story_files:
    s=p.read_text(encoding="utf-8")
    assert '<article class="prose short-story-prose">' in s
    assert 'style.css?v=050' in s

print("UPDATED", len(changed))
for p in changed: print(p)
