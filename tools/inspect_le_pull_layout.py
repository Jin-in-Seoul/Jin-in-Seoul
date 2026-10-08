from pathlib import Path
import fitz

pdf=Path("assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.pdf")
doc=fitz.open(pdf)
pages=[3,4,5,20,21,22,40,41,60,80,100,120,140,160,180]
out=[]
for pno in pages:
    if pno>=doc.page_count: continue
    p=doc[pno]
    out.append(f"\n===== PAGE {pno+1} =====")
    d=p.get_text("dict")
    for b in d["blocks"]:
        if "lines" not in b: continue
        for line in b["lines"]:
            txt="".join(span["text"] for span in line["spans"]).strip()
            if not txt: continue
            x0=min(span["bbox"][0] for span in line["spans"])
            y0=min(span["bbox"][1] for span in line["spans"])
            out.append(f"{x0:7.2f}\t{y0:7.2f}\t{txt}")
Path("tools/le-pull-layout-sample.txt").write_text("\n".join(out),encoding="utf-8")
print("written",len(out))
