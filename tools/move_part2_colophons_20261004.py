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

def find_colophon(r, lang):
    for i,p in enumerate(r.pages):
        t=(p.extract_text() or '')
        if 'Copyright © 2026 Jin-in-Seoul' in t:
            if lang=='en' and 'Part II — History' in t:
                return i
            if lang=='ko' and ('제2부' in t and '역사편' in t):
                return i
    raise RuntimeError(f'Part II colophon not found: {lang}')

def footer_overlay(n):
    b=BytesIO()
    c=canvas.Canvas(b,pagesize=A4,pageCompression=1)
    c.setFillColorRGB(1,1,1)
    c.rect(0,24,W,45,fill=1,stroke=0)
    c.setFillColorRGB(0,0,0)
    c.setFont('Helvetica',10)
    c.drawCentredString(W/2,43.5,f'- {n} -')
    c.showPage(); c.save(); b.seek(0)
    return PdfReader(b).pages[0]

def move_en():
    r=PdfReader(str(EN)); idx=find_colophon(r,'en')
    col=r.pages[idx]
    w=PdfWriter(); metadata_copy(w,r)
    for i,p in enumerate(r.pages):
        if i!=idx: w.add_page(p)
    w.add_page(col)
    tmp=EN.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(EN)
    v=PdfReader(str(EN))
    assert 'Copyright © 2026 Jin-in-Seoul' not in (v.pages[1].extract_text() or '')
    assert 'Copyright © 2026 Jin-in-Seoul' in (v.pages[-1].extract_text() or '')
    print('EN pages',len(v.pages),'colophon moved to',len(v.pages))

def move_ko():
    r=PdfReader(str(KO)); idx=find_colophon(r,'ko')
    col=r.pages[idx]
    ordered=[p for i,p in enumerate(r.pages) if i!=idx]
    ordered.append(col)
    w=PdfWriter(); metadata_copy(w,r)
    for page_no,p in enumerate(ordered,start=1):
        p.merge_page(footer_overlay(page_no))
        w.add_page(p)
    tmp=KO.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(KO)
    v=PdfReader(str(KO))
    assert 'Copyright © 2026 Jin-in-Seoul' not in (v.pages[1].extract_text() or '')
    assert 'Copyright © 2026 Jin-in-Seoul' in (v.pages[-1].extract_text() or '')
    assert f'- {len(v.pages)} -' in (v.pages[-1].extract_text() or '')
    print('KO pages',len(v.pages),'colophon moved to',len(v.pages))

move_en()
move_ko()
