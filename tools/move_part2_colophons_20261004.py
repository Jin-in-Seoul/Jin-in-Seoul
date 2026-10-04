from pathlib import Path
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

ROOT=Path.cwd()
EN=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-02/en/a-dictionary-of-galactic-extinction-part-02-en-20261004-ver-001.pdf'
KO=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-02/ko/a-dictionary-of-galactic-extinction-part-02-ko-20261004-ver-001.pdf'
W,H=A4

def metadata_copy(w,r):
    if r.metadata:
        w.add_metadata({k:str(v) for k,v in r.metadata.items() if v is not None})

def colophon_indices(r, lang):
    out=[]
    for i,p in enumerate(r.pages):
        t=(p.extract_text() or '')
        if 'Copyright © 2026 Jin-in-Seoul' not in t:
            continue
        if lang=='en' and 'Part II — History' in t:
            out.append(i)
        elif lang=='ko' and ('제2부' in t and '역사편' in t):
            out.append(i)
    if not out:
        raise RuntimeError(f'Part II colophon not found: {lang}')
    return out

def footer_overlay(n):
    b=BytesIO()
    c=canvas.Canvas(b,pagesize=A4,pageCompression=1)
    c.setFillColorRGB(1,1,1)
    c.rect(0,22,W,50,fill=1,stroke=0)
    c.setFillColorRGB(0,0,0)
    c.setFont('Helvetica',10)
    c.drawCentredString(W/2,43.5,f'- {n} -')
    c.showPage(); c.save(); b.seek(0)
    return PdfReader(b).pages[0]

def move_en():
    r=PdfReader(str(EN))
    idxs=colophon_indices(r,'en')
    print('EN copyright pages before:', [i+1 for i in idxs])
    col=r.pages[idxs[0]]
    ordered=[p for i,p in enumerate(r.pages) if i not in idxs]
    ordered.append(col)
    w=PdfWriter(); metadata_copy(w,r)
    for p in ordered: w.add_page(p)
    tmp=EN.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(EN)
    v=PdfReader(str(EN))
    after=[i for i,p in enumerate(v.pages) if 'Copyright © 2026 Jin-in-Seoul' in (p.extract_text() or '') and 'Part II — History' in (p.extract_text() or '')]
    assert after == [len(v.pages)-1], after
    print('EN pages:',len(v.pages),'copyright final page:',after[0]+1)

def move_ko():
    r=PdfReader(str(KO))
    idxs=colophon_indices(r,'ko')
    print('KO copyright pages before:', [i+1 for i in idxs])
    col=r.pages[idxs[0]]
    ordered=[p for i,p in enumerate(r.pages) if i not in idxs]
    ordered.append(col)
    w=PdfWriter(); metadata_copy(w,r)
    for page_no,p in enumerate(ordered,start=1):
        p.merge_page(footer_overlay(page_no))
        w.add_page(p)
    tmp=KO.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(KO)
    v=PdfReader(str(KO))
    after=[i for i,p in enumerate(v.pages) if 'Copyright © 2026 Jin-in-Seoul' in (p.extract_text() or '') and ('제2부' in (p.extract_text() or '') and '역사편' in (p.extract_text() or ''))]
    assert after == [len(v.pages)-1], after
    assert f'- {len(v.pages)} -' in (v.pages[-1].extract_text() or '')
    print('KO pages:',len(v.pages),'copyright final page:',after[0]+1)

move_en()
move_ko()
