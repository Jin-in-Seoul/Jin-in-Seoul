from pathlib import Path
import re

ROOT=Path(".")
css_path=ROOT/"assets/style.css"
css=css_path.read_text(encoding="utf-8")
block="""
/* Galactic Extinction book-style paragraph setting */
.galactic-prose p {
  margin: 0;
  text-indent: 1em;
}
.galactic-prose p.deck,
.galactic-prose p.part-label,
.galactic-prose p.section-number,
.galactic-prose p[style*="text-align:center"],
.galactic-prose p[style*="text-align: center"] {
  text-indent: 0;
}
"""
if "/* Galactic Extinction book-style paragraph setting */" not in css:
    css=css.rstrip()+"\n\n"+block.strip()+"\n"
css_path.write_text(css,encoding="utf-8")

root=ROOT/"a-dictionary-of-galactic-extinction"
entry_files=sorted(root.glob("*/part-*/entry-*/index.html"))
# Only actual prose entry pages, never landing/part/translation-principles pages.
assert entry_files, "no entry pages found"
langs={}
for p in entry_files:
    lang=p.parts[p.parts.index("a-dictionary-of-galactic-extinction")+1]
    langs[lang]=langs.get(lang,0)+1
    s=p.read_text(encoding="utf-8")
    if '<article class="prose galactic-prose">' not in s:
        if '<article class="prose">' not in s:
            raise RuntimeError(f"article marker missing: {p}")
        s=s.replace('<article class="prose">','<article class="prose galactic-prose">',1)
    s=re.sub(r'style\.css\?v=\d+', 'style.css?v=051', s)
    p.write_text(s,encoding="utf-8")

for p in entry_files:
    s=p.read_text(encoding="utf-8")
    assert '<article class="prose galactic-prose">' in s
    assert 'style.css?v=051' in s

print("UPDATED",len(entry_files),langs)
