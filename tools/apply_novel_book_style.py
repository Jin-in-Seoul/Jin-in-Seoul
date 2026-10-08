from pathlib import Path
import re

ROOT=Path(".")
css_path=ROOT/"assets/style.css"
css=css_path.read_text(encoding="utf-8")

block="""
/* Sweater book-style paragraph setting */
.sweater-prose p {
  margin: 0;
  text-indent: 1em;
}
.sweater-prose p.entry-date,
.sweater-prose p.section-number,
.sweater-prose p[style*="text-align:center"],
.sweater-prose p[style*="text-align: center"] {
  text-indent: 0;
}

/* Scarecrow Distance book-style paragraph setting */
.scarecrow-prose p {
  margin: 0;
  text-indent: 1em;
}
.scarecrow-prose p.section-number,
.scarecrow-prose p[style*="text-align:center"],
.scarecrow-prose p[style*="text-align: center"] {
  text-indent: 0;
}
"""
if "/* Sweater book-style paragraph setting */" not in css:
    css=css.rstrip()+"\n\n"+block.strip()+"\n"
css_path.write_text(css,encoding="utf-8")

targets=[]
targets += sorted((ROOT/"sweater").glob("*/chapter-*/index.html"))
targets += sorted((ROOT/"scarecrow-distance").glob("*/chapter-*/index.html"))

sweater=[p for p in targets if p.parts[0]=="sweater"]
scarecrow=[p for p in targets if p.parts[0]=="scarecrow-distance"]
assert len(sweater)==36, len(sweater)
assert len(scarecrow)==16, len(scarecrow)

for p in targets:
    s=p.read_text(encoding="utf-8")
    cls="sweater-prose" if p.parts[0]=="sweater" else "scarecrow-prose"
    old='<section class="prose">'
    new=f'<section class="prose {cls}">'
    if new not in s:
        if old not in s:
            raise RuntimeError(f"prose marker missing: {p}")
        s=s.replace(old,new,1)
    s=re.sub(r'style\.css\?v=\d+', 'style.css?v=052', s)
    p.write_text(s,encoding="utf-8")

for p in sweater:
    s=p.read_text(encoding="utf-8")
    assert '<section class="prose sweater-prose">' in s
    assert 'style.css?v=052' in s
for p in scarecrow:
    s=p.read_text(encoding="utf-8")
    assert '<section class="prose scarecrow-prose">' in s
    assert 'style.css?v=052' in s

print("SWEATER",len(sweater))
print("SCARECROW",len(scarecrow))
print("TOTAL",len(targets))
