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
RIGHT=509.9636
TARGET='웜홀은 가장 중요한 예비 장치였다.'

doc=fitz.open(PDF)
hit=None
for pi,page in enumerate(doc):
    for b in page.get_text('dict')['blocks']:
        if 'lines' not in b: continue
        for ln in b['lines']:
            txt=''.join(s['text'] for s in ln['spans'])
            if TARGET in txt:
                if hit is not None: raise RuntimeError('multiple target lines')
                s=ln['spans'][0]
                hit=(pi,txt,float(s['size']),tuple(s['origin']),tuple(ln['bbox']))
if hit is None: raise RuntimeError('target not found')

pi,txt,size,origin,bbox=hit
# Normalize to the original Part I convention: exactly two leading spaces, no extra x-offset.
txt='  '+txt.lstrip()

page=doc[pi]
rect=fitz.Rect(bbox); rect.x0-=1; rect.x1+=1; rect.y0-=1; rect.y1+=1
page.add_redact_annot(rect,fill=(1,1,1)); page.apply_redactions()
red=PDF.with_suffix('.redacted.pdf')
doc.save(red,garbage=4,deflate=True); doc.close()

natural=pdfmetrics.stringWidth(txt,'NM',size)
cs=(RIGHT-LEFT-natural)/(len(txt)-1)

reader=PdfReader(str(red)); writer=PdfWriter()
if reader.metadata:
    writer.add_metadata({k:str(v) for k,v in reader.metadata.items() if v is not None})
for i,p in enumerate(reader.pages):
    if i==pi:
        buf=BytesIO(); c=canvas.Canvas(buf,pagesize=A4,pageCompression=1)
        y=H-origin[1]
        t=c.beginText(LEFT,y); t.setFont('NM',size); t.setCharSpace(cs); t.textLine(txt)
        c.drawText(t); c.save(); buf.seek(0)
        p.merge_page(PdfReader(buf).pages[0])
    writer.add_page(p)

tmp=PDF.with_suffix('.tmp.pdf')
with tmp.open('wb') as f: writer.write(f)
tmp.replace(PDF); red.unlink(missing_ok=True)

# Validate exact original-style indentation geometry.
out=fitz.open(PDF)
assert len(out)==39
assert '\n'.join(p.get_text() for p in out).count(TARGET)==1
found=None
for b in out[pi].get_text('rawdict')['blocks']:
    if 'lines' not in b: continue
    for ln in b['lines']:
        chars=[]
        for sp in ln['spans']: chars += sp.get('chars',[])
        text=''.join(ch['c'] for ch in chars)
        if TARGET in text:
            found=(ln,chars,text)
assert found
ln,chars,text=found
assert text.startswith('  웜홀은'), repr(text[:12])
first_nonspace=next(ch for ch in chars if ch['c']!=' ')
x_line=ln['bbox'][0]
x_glyph=first_nonspace['bbox'][0]
assert abs(x_line-LEFT)<1.0,(x_line,LEFT)
assert 96.0 < x_glyph < 98.2,x_glyph
print('page',pi+1,'line_x0',x_line,'first_glyph_x',x_glyph,'line_x1',ln['bbox'][2],'pages',len(out))
out.close()
