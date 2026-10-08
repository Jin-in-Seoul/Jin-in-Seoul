from pathlib import Path
import re

ROOT=Path(".")
css_path=ROOT/"assets/style.css"
css=css_path.read_text(encoding="utf-8")

block="""
/* Children's books book-style paragraph setting */
.children-prose p {
  margin: 0;
  text-indent: 1em;
}
.children-prose p.section-number,
.children-prose p[style*="text-align:center"],
.children-prose p[style*="text-align: center"] {
  text-indent: 0;
}
"""
if "/* Children's books book-style paragraph setting */" not in css:
    css=css.rstrip()+"\n\n"+block.strip()+"\n"
css_path.write_text(css,encoding="utf-8")

targets=sorted((ROOT/"childrens-books").glob("*/*/index.html"))
assert len(targets)==6, [p.as_posix() for p in targets]

for p in targets:
    s=p.read_text(encoding="utf-8")
    if '<article class="prose children-prose">' not in s:
        if '<article class="prose">' not in s:
            raise RuntimeError(f"prose marker missing: {p}")
        s=s.replace('<article class="prose">','<article class="prose children-prose">',1)
    s=re.sub(r'style\.css\?v=\d+', 'style.css?v=053', s)
    p.write_text(s,encoding="utf-8")

for p in targets:
    s=p.read_text(encoding="utf-8")
    assert '<article class="prose children-prose">' in s
    assert 'style.css?v=053' in s

print("UPDATED",len(targets))
for p in targets:
    print(p)
