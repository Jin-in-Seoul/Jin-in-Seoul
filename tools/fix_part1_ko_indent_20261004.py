from pathlib import Path
from io import BytesIO
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

ROOT=Path.cwd()
PDF=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/ko/a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.pdf'
REG='/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'
pdfmetrics.registerFont(TTFont('NM',REG))
W,H=A4
LEFT=85.0339
INDENT=12.0
RIGHT=509.9636
TARGET='웜홀은 가장 중요한 예비 장치였다.'

doc=fitz.open(PDF)
hits=[]
for pi,page in enumerate(doc):
    d=page.get_text('dict')
    for b in d['blocks']:
        if 'lines' not in b: continue
        for line in b['lines']:
            txt=''.join(s['text'] for s in line['spans'])
            if TARGET in txt:
                s=line['spans'][0]
                hits.append((pi,txt,float(s['size']),tuple(s['origin']),tuple(line['bbox'])))
if len(hits)!=1:
    raise RuntimeError(f'target line count={len(hits)}')
pi,txt,size,origin,bbox=hits[0]

# The target is the first line of a paragraph: redraw with the standard 12pt first-line indent.
page=doc[pi]
rect=fitz.Rect(bbox); rect.x0-=1; rect.x1+=1; rect.y0-=1; rect.y1+=1
page.add_redact_annot(rect,fill=(1,1,1)); page.apply_redactions()
red=PDF.with_suffix('.redacted.pdf')
doc.save(red,garbage=4,deflate=True); doc.close()

x=LEFT+INDENT
avail=RIGHT-x
natural=pdfmetrics.stringWidth(txt,'NM',size)
cs=(avail-natural)/(len(txt)-1)

reader=PdfReader(str(red)); writer=PdfWriter()
if reader.metadata:
    writer.add_metadata({k:str(v) for k,v in reader.metadata.items() if v is not None})
for i,p in enumerate(reader.pages):
    if i==pi:
        buf=BytesIO(); c=canvas.Canvas(buf,pagesize=A4,pageCompression=1)
        y=H-origin[1]
        t=c.beginText(x,y); t.setFont('NM',size); t.setCharSpace(cs); t.textLine(txt)
        c.drawText(t); c.save(); buf.seek(0)
        p.merge_page(PdfReader(buf).pages[0])
    writer.add_page(p)
tmp=PDF.with_suffix('.tmp.pdf')
with tmp.open('wb') as f: writer.write(f)
tmp.replace(PDF); red.unlink(missing_ok=True)

# Verify exact page count, sentence, and first-line x position.
out=fitz.open(PDF)
assert len(out)==39
assert '\n'.join(p.get_text() for p in out).count(TARGET)==1
found=[]
for line in out[pi].get_text('dict')['blocks']:
    if 'lines' not in line: continue
    for ln in line['lines']:
        tx=''.join(s['text'] for s in ln['spans'])
        if TARGET in tx:
            found.append((tx,ln['bbox'][0],ln['bbox'][2]))
assert len(found)==1
assert abs(found[0][1]-(LEFT+INDENT)) < 1.5, found
print('page',pi+1,'x0',found[0][1],'x1',found[0][2],'pages',len(out),'target=1')
out.close()
