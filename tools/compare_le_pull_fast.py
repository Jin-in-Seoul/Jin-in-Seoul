from pathlib import Path
import fitz, re, unicodedata, hashlib
from bs4 import BeautifulSoup

PDF=Path("assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.pdf")
ROOT=Path("sweater/fr")
DAYS=r"(?:Lundi|Mardi|Mercredi|Jeudi|Vendredi|Samedi|Dimanche)"
date_re=re.compile(rf"^{DAYS}\b")

def norm(s):
    s=unicodedata.normalize("NFKC",s).replace("\u00a0"," ")
    s=s.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"')
    s=re.sub(r"\s+"," ",s).strip()
    return s

def page_lines(page):
    d=page.get_text("dict"); arr=[]
    for b in d["blocks"]:
        if "lines" not in b: continue
        for line in b["lines"]:
            spans=line["spans"]
            if not spans: continue
            txt="".join(s["text"] for s in spans).strip()
            if txt:
                arr.append((min(s["bbox"][1] for s in spans),min(s["bbox"][0] for s in spans),txt))
    arr.sort(); return arr

doc=fitz.open(PDF)
chapter_pages={}
for pi in range(doc.page_count):
    texts=[t for _,_,t in page_lines(doc[pi])]
    for n in range(1,13):
        if f"CHAPITRE {n}" in texts: chapter_pages[n]=pi
assert len(chapter_pages)==12, chapter_pages

def join_line(cur,line):
    if not cur: return line
    if cur.endswith("-") and line and line[0].islower(): return cur+line
    return cur+" "+line

def extract_chapter(n):
    start=chapter_pages[n]; end=chapter_pages.get(n+1,doc.page_count)
    paras=[]; cur=""; started=False
    for pi in range(start,end):
        for y,x,t in page_lines(doc[pi]):
            if t.isdigit() and y>740: continue
            if pi==start and not started:
                if date_re.match(t): started=True
                else: continue
            if not started: continue
            if date_re.match(t):
                if cur: paras.append(("p",cur.strip()))
                paras.append(("date",t)); cur=""; continue
            if re.match(r"^— .+ —$",t):
                if cur: paras.append(("p",cur.strip()))
                paras.append(("p",t)); cur=""; continue
            if re.match(r"^\d+\.\s",t):
                if cur: paras.append(("p",cur.strip()))
                cur=t; continue
            indented=x>85
            dialogue=t.startswith("—")
            if not cur:
                cur=t
            elif dialogue or (indented and not re.match(r"^\d+\.\s",cur)):
                paras.append(("p",cur.strip())); cur=t
            else:
                cur=join_line(cur,t)
    if cur: paras.append(("p",cur.strip()))
    return paras

rows=[]
for n in range(1,13):
    pp=extract_chapter(n)
    html=(ROOT/f"chapter-{n:02d}"/"index.html").read_text(encoding="utf-8")
    soup=BeautifulSoup(html,"html.parser")
    prose=soup.select_one(".prose")
    hp=[p.get_text(" ",strip=True) for p in prose.find_all("p",recursive=False)]
    a=norm(" ".join(t for _,t in pp)); b=norm(" ".join(hp))
    i=0; m=min(len(a),len(b))
    while i<m and a[i]==b[i]: i+=1
    equal=a==b
    rows.append(f"CH{n:02d}\tpdf_paras={len(pp)}\thtml_paras={len(hp)}\tequal={equal}\tprefix={i}\tpdf_chars={len(a)}\thtml_chars={len(b)}")
    if not equal:
        rows.append(" PDF "+repr(a[max(0,i-120):i+220]))
        rows.append(" HTML "+repr(b[max(0,i-120):i+220]))
Path("tools/le-pull-compare-fast.txt").write_text("\n".join(rows),encoding="utf-8")
print("\n".join(rows))
