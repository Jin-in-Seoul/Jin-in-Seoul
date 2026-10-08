from pathlib import Path
import fitz, re, unicodedata, difflib
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
    d=page.get_text("dict")
    arr=[]
    for b in d["blocks"]:
        if "lines" not in b: continue
        for line in b["lines"]:
            spans=line["spans"]
            if not spans: continue
            txt="".join(s["text"] for s in spans).strip()
            if not txt: continue
            x=min(s["bbox"][0] for s in spans)
            y=min(s["bbox"][1] for s in spans)
            arr.append((y,x,txt))
    arr.sort()
    return arr

doc=fitz.open(PDF)
chapter_pages={}
for pi in range(doc.page_count):
    texts=[t for _,_,t in page_lines(doc[pi])]
    for n in range(1,13):
        if f"CHAPITRE {n}" in texts:
            chapter_pages[n]=pi
assert len(chapter_pages)==12,chapter_pages

def join_line(cur,line):
    if not cur: return line
    # PDF line-wrap hyphen: retain hyphen and remove inserted whitespace.
    if cur.endswith("-") and line and line[0].islower():
        return cur+line
    return cur+" "+line

def extract_chapter(n):
    start=chapter_pages[n]
    end=chapter_pages.get(n+1,doc.page_count)
    paras=[]
    cur=""
    current_kind=None
    started_body=False
    for pi in range(start,end):
        lines=page_lines(doc[pi])
        # remove running page number
        lines=[(y,x,t) for y,x,t in lines if not (t.isdigit() and y>740)]
        for y,x,t in lines:
            # skip chapter heading area on first page until first date
            if pi==start and not started_body:
                if date_re.match(t):
                    started_body=True
                else:
                    continue
            if not started_body:
                continue
            is_date=bool(date_re.match(t))
            is_num=bool(re.match(r"^\d+\.\s",t))
            is_dash_heading=bool(re.match(r"^— .+ —$",t))
            is_dialogue=t.startswith("—")
            indented=x>85
            if is_date:
                if cur: paras.append((current_kind or "p",cur.strip()))
                paras.append(("date",t))
                cur=""
                current_kind=None
                continue
            if is_dash_heading:
                if cur: paras.append((current_kind or "p",cur.strip()))
                paras.append(("p",t))
                cur=""; current_kind=None
                continue
            if is_num:
                if cur: paras.append((current_kind or "p",cur.strip()))
                cur=t; current_kind="p"
                continue

            new_para=False
            if not cur:
                new_para=True
            elif is_dialogue:
                new_para=True
            elif indented:
                # In normal prose, first-line indent marks a new paragraph.
                # If current paragraph is a numbered list item, same x is a continuation unless another number starts.
                if not re.match(r"^\d+\.\s",cur):
                    new_para=True
            if new_para:
                if cur: paras.append((current_kind or "p",cur.strip()))
                cur=t; current_kind="p"
            else:
                cur=join_line(cur,t)
    if cur: paras.append((current_kind or "p",cur.strip()))
    return paras

rows=[]
all_ok=True
for n in range(1,13):
    pp=extract_chapter(n)
    html=(ROOT/f"chapter-{n:02d}"/"index.html").read_text(encoding="utf-8")
    soup=BeautifulSoup(html,"html.parser")
    prose=soup.select_one(".prose")
    hp=[p.get_text(" ",strip=True) for p in prose.find_all("p",recursive=False)]
    pdf_full=norm(" ".join(t for _,t in pp))
    html_full=norm(" ".join(hp))
    ratio=difflib.SequenceMatcher(None,pdf_full,html_full,autojunk=False).ratio()
    equal=pdf_full==html_full
    rows.append(f"CH{n:02d}\tpdf_paras={len(pp)}\thtml_paras={len(hp)}\tequal={equal}\tratio={ratio:.6f}\tpdf_chars={len(pdf_full)}\thtml_chars={len(html_full)}")
    if not equal:
        all_ok=False
        # report first differing window
        sm=difflib.SequenceMatcher(None,pdf_full,html_full,autojunk=False)
        for tag,i1,i2,j1,j2 in sm.get_opcodes():
            if tag!="equal":
                rows.append("  FIRST_DIFF "+repr(pdf_full[max(0,i1-120):i2+120]))
                rows.append("  HTML_DIFF  "+repr(html_full[max(0,j1-120):j2+120]))
                break

Path("tools/le-pull-compare-report.txt").write_text("\n".join(rows),encoding="utf-8")
print("\n".join(rows))
