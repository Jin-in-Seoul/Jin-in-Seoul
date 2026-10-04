from pathlib import Path
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT=Path.cwd()
PDF=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/en/a-dictionary-of-galactic-extinction-part-01-en-20260929-ver-001.pdf'
REG='/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'
BOLD='/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf'
pdfmetrics.registerFont(TTFont('NM',REG))
pdfmetrics.registerFont(TTFont('NMB',BOLD))
W,H=A4

def title_page():
    b=BytesIO()
    c=canvas.Canvas(b,pagesize=A4,pageCompression=1)
    c.setFont('NMB',20)
    c.drawCentredString(W/2,H-229,'Part I — Conditions of Extinction')
    c.showPage(); c.save(); b.seek(0)
    return PdfReader(b).pages[0]

r=PdfReader(str(PDF))
kept=[]
for p in r.pages:
    t=(p.extract_text() or '').strip()
    # remove only the standalone mistakenly inserted part-title page
    if 'Part I — Conditions of Extinction' in t and len(t) < 120:
        continue
    kept.append(p)

insert_at=None
for i,p in enumerate(kept):
    t=(p.extract_text() or '')
    if '1. Photon Deficit' in t and 'The phenomenon in which a photon' in t:
        insert_at=i
        break

if insert_at is None:
    raise RuntimeError('Could not locate first Photon Deficit body page')

w=PdfWriter()
if r.metadata:
    w.add_metadata({k:str(v) for k,v in r.metadata.items() if v is not None})

for i,p in enumerate(kept):
    if i==insert_at:
        w.add_page(title_page())
    w.add_page(p)

tmp=PDF.with_suffix('.tmp.pdf')
with tmp.open('wb') as f:
    w.write(f)
tmp.replace(PDF)

# verify exact sequence around insertion
v=PdfReader(str(PDF))
idx=None
for i,p in enumerate(v.pages):
    t=(p.extract_text() or '')
    if '1. Photon Deficit' in t and 'The phenomenon in which a photon' in t:
        idx=i
        break
assert idx is not None and idx>0
prev=(v.pages[idx-1].extract_text() or '').strip()
assert 'Part I — Conditions of Extinction' in prev
assert len(prev) < 120
print('fixed pages=',len(v.pages),'body_index=',idx+1,'title_index=',idx)
