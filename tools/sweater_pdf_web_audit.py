from pathlib import Path
import fitz, re, unicodedata, json
from bs4 import BeautifulSoup

ROOT=Path(".")
PDFS={
 "en":ROOT/"assets/downloads/sweater/en/sweater-en-20260930-ver-001.pdf",
 "fr":ROOT/"assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.pdf",
 "ja":ROOT/"assets/downloads/sweater/ja/sweater-ja-20261003-ver-001.pdf",
}

def norm(s):
    s=s.replace("\uf09f","•").replace("\u00ad","")
    s=unicodedata.normalize("NFC",s)
    s=re.sub(r"-\s+","-",s)
    s=re.sub(r"\s+"," ",s).strip()
    return s

def compact(s):
    return re.sub(r"\s+","",norm(s))

def chapter_starts(doc):
    starts={}
    for pno,p in enumerate(doc):
        t=p.get_text("text")
        m=re.search(r"CHAPTER\s+(\d+)",t,re.I)
        if not m: m=re.search(r"CHAPITRE\s+(\d+)",t,re.I)
        if not m: m=re.search(r"第\s*(\d+)\s*章",t)
        if m: starts[int(m.group(1))]=pno
    return starts

def pdf_chapter_text(doc,starts,ch):
    p0=starts[ch]
    p1=starts.get(ch+1,doc.page_count)
    chunks=[]
    for pno in range(p0,p1):
        t=doc[pno].get_text("text")
        # strip obvious printed page-number-only lines
        lines=[ln for ln in t.splitlines() if not re.fullmatch(r"\s*\d+\s*",ln)]
        chunks.append("\n".join(lines))
    s="\n".join(chunks)
    # Remove chapter heading/month/title before first diary date by aligning against website first 40 chars later.
    return s

def web_text(lang,ch):
    p=ROOT/f"sweater/{lang}/chapter-{ch:02d}/index.html"
    soup=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
    box=soup.select_one(".sweater-prose")
    blocks=[]
    for x in box.find_all(["p","li"],recursive=True):
        # avoid nested li text being counted through parent lists; p/li have direct text only enough
        blocks.append(x.get_text(" ",strip=True))
    return " ".join(blocks), len(blocks)

results={}
for lang,pdf in PDFS.items():
    doc=fitz.open(pdf)
    starts=chapter_starts(doc)
    results[lang]={"starts":starts,"chapters":{}}
    for ch in range(1,13):
        wt,wblocks=web_text(lang,ch)
        pt=pdf_chapter_text(doc,starts,ch)
        wc=compact(wt)
        pc=compact(pt)
        # PDF includes chapter headers. Locate website content's beginning in PDF compact text.
        probe=wc[:80]
        pos=pc.find(probe)
        equal=False
        pdfslice=""
        if pos>=0:
            # compare exactly website compact length from located start
            pdfslice=pc[pos:pos+len(wc)]
            equal=(pdfslice==wc)
        # prefix if not equal
        pref=0
        if pos>=0:
            n=min(len(wc),len(pdfslice))
            while pref<n and wc[pref]==pdfslice[pref]: pref+=1
        results[lang]["chapters"][str(ch)]={
          "web_blocks":wblocks,"web_chars":len(wc),"pdf_start_found":pos>=0,
          "compact_equal":equal,"prefix":pref,
          "web_excerpt":wc[max(0,pref-80):pref+140] if not equal else "",
          "pdf_excerpt":pdfslice[max(0,pref-80):pref+140] if not equal else ""
        }

Path("tools/sweater-pdf-web-audit.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
for lang in results:
    print(lang, {ch:(v["web_blocks"],v["pdf_start_found"],v["compact_equal"],v["prefix"]) for ch,v in results[lang]["chapters"].items()})
