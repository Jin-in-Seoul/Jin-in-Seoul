from pathlib import Path
import fitz, re, html, unicodedata
from bs4 import BeautifulSoup

ROOT=Path(".")
PDF=ROOT/"assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.pdf"
WEEKDAYS=("Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche")
DATE_RE=re.compile(r"^(?:"+"|".join(WEEKDAYS)+r")\b")

def norm(s):
    s=s.replace("\uf09f","•")
    s=unicodedata.normalize("NFC",s)
    s=re.sub(r"\s+"," ",s).strip()
    return s

doc=fitz.open(PDF)

# Locate chapter page starts from printed headings.
starts={}
for pno,p in enumerate(doc):
    txt=p.get_text("text")
    m=re.search(r"CHAPITRE\s+(\d+)",txt)
    if m:
        starts[int(m.group(1))]=pno
assert set(starts)==set(range(1,13)), starts

def page_lines(pno):
    p=doc[pno]
    rows=[]
    d=p.get_text("dict")
    for b in d.get("blocks",[]):
        if "lines" not in b: continue
        for line in b["lines"]:
            spans=line.get("spans",[])
            if not spans: continue
            text="".join(sp["text"] for sp in spans).strip()
            if not text: continue
            x0=min(sp["bbox"][0] for sp in spans)
            y0=min(sp["bbox"][1] for sp in spans)
            # page number/footer
            if y0 > 765: continue
            rows.append((y0,x0,text))
    rows.sort()
    return rows

def pdf_paragraphs(ch):
    p0=starts[ch]
    p1=starts[ch+1] if ch<12 else doc.page_count
    paras=[]
    cur=None
    started=False
    after_date=False
    for pno in range(p0,p1):
        rows=page_lines(pno)
        for y,x,text in rows:
            # Skip chapter heading/title material until the first dated diary entry.
            if not started:
                if DATE_RE.match(text):
                    started=True
                else:
                    continue
            is_date=bool(DATE_RE.match(text))
            if is_date:
                if cur is not None:
                    paras.append(cur)
                cur={"text":text,"date":True}
                after_date=True
                continue

            # A first body paragraph after every date is a new paragraph even when unindented.
            newpara=False
            if cur is None:
                newpara=True
            elif after_date:
                paras.append(cur)
                cur=None
                newpara=True
                after_date=False
            elif x >= 90:
                newpara=True

            if newpara:
                if cur is not None:
                    paras.append(cur)
                cur={"text":text,"date":False}
            else:
                cur["text"] += " " + text
    if cur is not None:
        paras.append(cur)
    return paras

report=[]
for ch in range(1,13):
    path=ROOT/f"sweater/fr/chapter-{ch:02d}/index.html"
    raw=path.read_text(encoding="utf-8")
    m=re.search(r'(<section class="prose sweater-prose">\s*)(.*?)(\s*</section>)',raw,re.S)
    if not m:
        raise RuntimeError(f"prose section missing: {path}")
    section=m.group(2)

    soup=BeautifulSoup(section,"html.parser")
    ps=soup.find_all("p")
    # No inline semantic markup is expected in this edition; abort rather than silently flatten it.
    bad=[]
    for p in ps:
        if p.find(True):
            bad.append(str(p)[:200])
    if bad:
        raise RuntimeError(f"inline markup found in {path}: {bad[:3]}")

    html_flat=norm(" ".join(p.get_text(" ",strip=True) for p in ps))
    pdfps=pdf_paragraphs(ch)
    pdf_flat=norm(" ".join(x["text"] for x in pdfps))

    if html_flat != pdf_flat:
        # Give a useful mismatch location.
        n=min(len(html_flat),len(pdf_flat))
        i=0
        while i<n and html_flat[i]==pdf_flat[i]:
            i+=1
        raise RuntimeError(
            f"TEXT MISMATCH ch{ch:02d} at {i}\n"
            f"HTML: {html_flat[max(0,i-120):i+180]}\n"
            f"PDF : {pdf_flat[max(0,i-120):i+180]}"
        )

    # Use current website text as the textual source, and PDF only for paragraph boundaries.
    # Since normalized full texts are identical, normalized PDF paragraph lengths map exactly.
    rebuilt=[]
    pos=0
    for item in pdfps:
        target=norm(item["text"])
        seg=html_flat[pos:pos+len(target)]
        if seg != target:
            raise RuntimeError(f"boundary mapping failed ch{ch:02d} at {pos}: {seg[:80]!r} != {target[:80]!r}")
        esc=html.escape(seg,quote=False)
        if item["date"]:
            rebuilt.append(f'<p class="entry-date">{esc}</p>')
        else:
            rebuilt.append(f'<p>{esc}</p>')
        pos += len(target)
        # paragraphs are separated by exactly one normalized space in html_flat
        if pos < len(html_flat):
            if html_flat[pos] != " ":
                raise RuntimeError(f"expected separator ch{ch:02d} at {pos}")
            pos += 1
    if pos != len(html_flat):
        raise RuntimeError(f"length mapping mismatch ch{ch:02d}: {pos} != {len(html_flat)}")

    new_section=m.group(1)+"\n".join(rebuilt)+m.group(3)
    new_raw=raw[:m.start()]+new_section+raw[m.end():]
    path.write_text(new_raw,encoding="utf-8")

    # Final invariants
    check=path.read_text(encoding="utf-8")
    m2=re.search(r'(<section class="prose sweater-prose">\s*)(.*?)(\s*</section>)',check,re.S)
    soup2=BeautifulSoup(m2.group(2),"html.parser")
    final_flat=norm(" ".join(p.get_text(" ",strip=True) for p in soup2.find_all("p")))
    if final_flat != html_flat:
        raise RuntimeError(f"text changed in ch{ch:02d}")

    report.append((ch,len(ps),len(pdfps),sum(1 for x in pdfps if x["date"])))

print("Le Pull paragraph restoration complete")
for ch,oldn,newn,dates in report:
    print(f"CH{ch:02d}: old={oldn} PDF={newn} dates={dates}")
