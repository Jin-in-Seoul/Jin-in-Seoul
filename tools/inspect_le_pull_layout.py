from pathlib import Path
import fitz

doc=fitz.open("assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.pdf")
rows=[]
for pi in range(3,25):
    page=doc[pi]
    d=page.get_text("dict")
    rows.append(f"\n===== PAGE {pi+1} =====")
    for b in d["blocks"]:
        if "lines" not in b: continue
        for line in b["lines"]:
            spans=line["spans"]
            if not spans: continue
            text="".join(s["text"] for s in spans).strip()
            if not text: continue
            x0=min(s["bbox"][0] for s in spans)
            y0=min(s["bbox"][1] for s in spans)
            rows.append(f"x={x0:.1f}\ty={y0:.1f}\t{text}")
Path("tools/le-pull-layout-sample.txt").write_text("\n".join(rows),encoding="utf-8")
