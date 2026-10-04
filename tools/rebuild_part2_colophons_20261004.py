from pathlib import Path
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT=Path.cwd()
EN=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-02/en/a-dictionary-of-galactic-extinction-part-02-en-20261004-ver-001.pdf'
KO=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-02/ko/a-dictionary-of-galactic-extinction-part-02-ko-20261004-ver-001.pdf'
REG='/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'
BOLD='/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf'
pdfmetrics.registerFont(TTFont('NM',REG))
pdfmetrics.registerFont(TTFont('NMB',BOLD))
W,H=A4

def copy_meta(w,r):
    if r.metadata:
        w.add_metadata({k:str(v) for k,v in r.metadata.items() if v is not None})

def make_page(draw):
    b=BytesIO()
    c=canvas.Canvas(b,pagesize=A4,pageCompression=1)
    draw(c)
    c.showPage(); c.save(); b.seek(0)
    return PdfReader(b).pages[0]

def en_colophon():
    def draw(c):
        x=85.0
        y=H-180
        c.setFont('NMB',14)
        c.drawString(x,y,'A Dictionary of Galactic Extinction'); y-=26
        c.drawString(x,y,'Part II - History'); y-=48
        lines=[
            'Copyright © 2026 Jin-in-Seoul',
            'All rights reserved.',
            'The copyright in this book belongs to Jin-in-Seoul.',
            'No part of this book may be reproduced, distributed, transmitted, modified,',
            'or used commercially without the permission of the copyright holder.',
            'This digital edition is distributed free of charge.',
            'Free distribution does not waive or transfer any copyright.',
            'First digital edition, 2026',
            'Published by Jin-in-Seoul',
            'https://jin-in-seoul.com'
        ]
        c.setFont('NM',12)
        for line in lines:
            c.drawString(x,y,line); y-=22
    return make_page(draw)

def ko_colophon(final_page_no):
    def draw(c):
        x=85.0
        y=H-180
        c.setFont('NMB',14)
        c.drawString(x,y,'은하 멸망 사전'); y-=26
        c.drawString(x,y,'A Dictionary of Galactic Extinction'); y-=26
        c.drawString(x,y,'제2부 - 역사편'); y-=48
        lines=[
            'Copyright © 2026 Jin-in-Seoul',
            'All rights reserved.',
            '이 책의 저작권은 Jin-in-Seoul에게 있습니다.',
            '저작권자의 허락 없이 이 책의 전부 또는 일부를 복제, 배포, 전송, 변형하거나',
            '상업적으로 이용할 수 없습니다.',
            'First digital edition, 2026',
            'Jin-in-Seoul 발행',
            'https://jin-in-seoul.com',
            '',
            '* 이 디지털 판본은 무료로 배포됩니다. 무료 배포는 저작권의 포기 또는 양도를',
            '의미하지 않습니다.'
        ]
        c.setFont('NM',12)
        for line in lines:
            if line:
                c.drawString(x,y,line)
            y-=22
        c.setFont('Helvetica',10)
        c.drawCentredString(W/2,43.5,f'- {final_page_no} -')
    return make_page(draw)

def footer_overlay(n):
    def draw(c):
        c.setFillColorRGB(1,1,1)
        c.rect(0,20,W,55,fill=1,stroke=0)
        c.setFillColorRGB(0,0,0)
        c.setFont('Helvetica',10)
        c.drawCentredString(W/2,43.5,f'- {n} -')
    return make_page(draw)

def strip_all_colophon_pages(r):
    kept=[]
    removed=[]
    for i,p in enumerate(r.pages):
        t=(p.extract_text() or '')
        if 'Copyright © 2026 Jin-in-Seoul' in t:
            removed.append(i+1)
        else:
            kept.append(p)
    return kept, removed

def rebuild_en():
    r=PdfReader(str(EN))
    kept,removed=strip_all_colophon_pages(r)
    if not removed:
        raise RuntimeError('No English copyright page found to replace')
    w=PdfWriter(); copy_meta(w,r)
    for p in kept: w.add_page(p)
    w.add_page(en_colophon())
    tmp=EN.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(EN)

    v=PdfReader(str(EN))
    hits=[]
    for i,p in enumerate(v.pages):
        t=(p.extract_text() or '')
        if 'Copyright © 2026 Jin-in-Seoul' in t:
            hits.append((i+1,t))
    assert len(hits)==1, hits
    assert hits[0][0]==len(v.pages), hits[0][0]
    assert 'Part II - History' in hits[0][1]
    assert 'Part I - Conditions of Extinction' not in hits[0][1] && 'Part I — Conditions of Extinction' not in hits[0][1]
    assert 'Published by Jin-in-Seoul' in hits[0][1]
    print('EN removed copyright pages:',removed,'final:',len(v.pages))

def rebuild_ko():
    r=PdfReader(str(KO))
    kept,removed=strip_all_colophon_pages(r)
    if not removed:
        raise RuntimeError('No Korean copyright page found to replace')

    # append newly generated Part II colophon; renumber every remaining page sequentially
    final_count=len(kept)+1
    w=PdfWriter(); copy_meta(w,r)
    for page_no,p in enumerate(kept,start=1):
        p.merge_page(footer_overlay(page_no))
        w.add_page(p)
    w.add_page(ko_colophon(final_count))
    tmp=KO.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(KO)

    v=PdfReader(str(KO))
    hits=[]
    for i,p in enumerate(v.pages):
        t=(p.extract_text() or '')
        if 'Copyright © 2026 Jin-in-Seoul' in t:
            hits.append((i+1,t))
    assert len(hits)==1, hits
    assert hits[0][0]==len(v.pages), hits[0][0]
    assert '제2부 - 역사편' in hits[0][1]
    assert '제1부' not in hits[0][1]
    assert 'Jin-in-Seoul 발행' in hits[0][1]
    assert f'- {len(v.pages)} -' in hits[0][1]
    print('KO removed copyright pages:',removed,'final:',len(v.pages))

rebuild_en()
rebuild_ko()
