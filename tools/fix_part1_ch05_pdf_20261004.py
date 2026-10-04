from pathlib import Path
from io import BytesIO
import os, re
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

ROOT=Path.cwd()
REG='/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'
pdfmetrics.registerFont(TTFont('NM',REG))
W,H=A4

FILES=[
    {
      'lang':'ko',
      'path':ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/ko/a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.pdf',
      'old':'웜홀은 가장 예비 장치였다.',
      'new':'웜홀은 가장 중요한 예비 장치였다.'
    },
    {
      'lang':'en',
      'path':ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/en/a-dictionary-of-galactic-extinction-part-01-en-20260929-ver-001.pdf',
      'old':'Wormholes were the ultimate backup systems.',
      'new':'Wormholes were the most important backup systems.'
    }
]

def patch_one(item):
    path=item['path']; lang=item['lang']; old=item['old']; new=item['new']
    doc=fitz.open(path)
    original_pages=len(doc)
    hit=None
    for pi,page in enumerate(doc):
        d=page.get_text('dict')
        for b in d['blocks']:
            if 'lines' not in b: continue
            for line in b['lines']:
                text=''.join(s['text'] for s in line['spans'])
                if old in text:
                    if hit is not None:
                        raise RuntimeError(f'multiple PDF hits for {lang}')
                    span=line['spans'][0]
                    hit=(pi,text,float(span['size']),tuple(span['origin']),tuple(line['bbox']))
    if hit is None:
        raise RuntimeError(f'target sentence not found in {lang} PDF')

    pi,oldline,size,origin,bbox=hit
    newline=oldline.replace(old,new,1)

    page=doc[pi]
    rect=fitz.Rect(bbox)
    rect.x0-=0.5; rect.x1+=0.5; rect.y0-=0.5; rect.y1+=0.5
    page.add_redact_annot(rect, fill=(1,1,1))
    page.apply_redactions()

    redacted=path.with_suffix('.redacted.pdf')
    doc.save(redacted, garbage=4, deflate=True)
    doc.close()

    reader=PdfReader(str(redacted))
    writer=PdfWriter()
    if reader.metadata:
        writer.add_metadata({k:str(v) for k,v in reader.metadata.items() if v is not None})

    for i,p in enumerate(reader.pages):
        if i==pi:
            buf=BytesIO()
            c=canvas.Canvas(buf,pagesize=A4,pageCompression=1)
            x=origin[0]; y=H-origin[1]
            t=c.beginText(x,y)
            t.setFont('NM',size)
            if lang=='ko':
                # Preserve the original justified line width exactly.
                right=509.963623046875
                avail=right-x
                natural=pdfmetrics.stringWidth(newline,'NM',size)
                charspace=(avail-natural)/(len(newline)-1)
                t.setCharSpace(charspace)
            else:
                # English Part I is ragged-right. The replacement fits inside the body width.
                t.setCharSpace(0)
            t.textLine(newline)
            c.drawText(t)
            c.save(); buf.seek(0)
            p.merge_page(PdfReader(buf).pages[0])
        writer.add_page(p)

    tmp=path.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f:
        writer.write(f)
    tmp.replace(path)
    redacted.unlink(missing_ok=True)

    # Structural/text validation
    out=fitz.open(path)
    if len(out)!=original_pages:
        raise RuntimeError(f'page count changed for {lang}')
    alltext='\n'.join(p.get_text() for p in out)
    if alltext.count(old)!=0:
        raise RuntimeError(f'old sentence remains in {lang}')
    if alltext.count(new)!=1:
        raise RuntimeError(f'new sentence count != 1 in {lang}: {alltext.count(new)}')
    target_page=out[pi].get_text()
    if new not in target_page:
        raise RuntimeError(f'new sentence not on target page in {lang}')
    out.close()
    print(f'{lang}: pages={original_pages}, changed_page={pi+1}, old=0, new=1')

for item in FILES:
    patch_one(item)
