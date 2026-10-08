from pathlib import Path
from zipfile import ZipFile
from bs4 import BeautifulSoup
import json, re

ROOT=Path(".")
out={}

# Le Pull EPUB vs current web paragraph structure
ep=ROOT/"assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.epub"
with ZipFile(ep) as z:
    names=z.namelist()
    chapter_files=[n for n in names if re.search(r"chapter-\d+\.xhtml$",n)]
    if not chapter_files:
        chapter_files=[n for n in names if re.search(r"(?:story|chapter)-\d+\.xhtml$",n)]
    epub_counts={}
    epub_samples={}
    for n in sorted(chapter_files):
        m=re.search(r"(\d+)\.xhtml$",n)
        if not m: continue
        ch=int(m.group(1))
        soup=BeautifulSoup(z.read(n).decode("utf-8"),"html.parser")
        box=soup.body
        ps=box.find_all("p")
        epub_counts[ch]=len(ps)
        if ch==3:
            epub_samples[ch]=[p.get_text(" ",strip=True) for p in ps[:35]]
    out["le_pull_epub"]={
      "size":ep.stat().st_size,
      "files":names,
      "p_counts":epub_counts,
      "sample_ch3":epub_samples.get(3,[])
    }

web_counts={}
for ch in range(1,13):
    p=ROOT/f"sweater/fr/chapter-{ch:02d}/index.html"
    soup=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
    box=soup.select_one(".sweater-prose")
    web_counts[ch]=len(box.find_all("p"))
out["le_pull_web_p_counts"]=web_counts
out["le_pull_count_mismatches"]={ch:{"epub":out["le_pull_epub"]["p_counts"].get(ch),"web":web_counts[ch]} for ch in range(1,13) if out["le_pull_epub"]["p_counts"].get(ch)!=web_counts[ch]}

# 007 site EPUB packaging
ep7=ROOT/"assets/downloads/adjunct-lecturer-k-007-briefcase/ko/adjunct-lecturer-k-007-briefcase-ko-20261007-ver-001.epub"
with ZipFile(ep7) as z:
    names=z.namelist()
    out["007_epub"]={
      "size":ep7.stat().st_size,
      "has_ncx":any(n.lower().endswith("toc.ncx") for n in names),
      "has_contents":any(n.lower().endswith("contents.xhtml") for n in names),
      "has_cover_svg":any(n.lower().endswith("cover.svg") for n in names),
      "has_cover_jpg":any(n.lower().endswith(("cover.jpg","cover.jpeg")) for n in names),
      "names":names
    }

Path("tools/download-audit.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({
 "le_pull_count_mismatches":out["le_pull_count_mismatches"],
 "007_epub":out["007_epub"]
},ensure_ascii=False,indent=2))
