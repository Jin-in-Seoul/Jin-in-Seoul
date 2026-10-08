from pathlib import Path
import fitz, re, json

pdf=Path("assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.pdf")
doc=fitz.open(pdf)
out=[]
out.append(f"PAGES\t{doc.page_count}")
for i,p in enumerate(doc):
    text=p.get_text("text")
    # compact page report preserving line/blank patterns
    lines=[ln.rstrip() for ln in text.splitlines()]
    out.append(f"\n===== PAGE {i+1} =====")
    out.extend(lines)
Path("tools/le-pull-pdf-extract.txt").write_text("\n".join(out),encoding="utf-8")
print("pages",doc.page_count)
