from pathlib import Path
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT=Path.cwd()
P1EN=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/en/a-dictionary-of-galactic-extinction-part-01-en-20260929-ver-001.pdf'
P1KO=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/ko/a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.pdf'
P2EN=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-02/en/a-dictionary-of-galactic-extinction-part-02-en-20261004-ver-001.pdf'
P2KO=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-02/ko/a-dictionary-of-galactic-extinction-part-02-ko-20261004-ver-001.pdf'
REG='/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'
BOLD='/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf'
pdfmetrics.registerFont(TTFont('NM',REG)); pdfmetrics.registerFont(TTFont('NMB',BOLD))
W,H=A4; LEFT=85.0339; FOOT=43.5

def make_page(draw):
    b=BytesIO(); c=canvas.Canvas(b,pagesize=A4,pageCompression=1); draw(c); c.showPage(); c.save(); b.seek(0); return PdfReader(b).pages[0]

def footer_overlay(n):
    def d(c):
        c.setFillColorRGB(1,1,1); c.rect(0,20,W,55,fill=1,stroke=0)
        c.setFillColorRGB(0,0,0); c.setFont('Helvetica',10); c.drawCentredString(W/2,FOOT,f'- {n} -')
    return make_page(d)

def ko_title():
    def d(c):
        c.setFont('NMB',20); c.drawCentredString(W/2,H-225.0,'제2부 역사편')
        c.setFont('Helvetica',10); c.drawCentredString(W/2,FOOT,'- 6 -')
    return make_page(d)

def en_title():
    def d(c): c.setFont('NMB',20); c.drawCentredString(W/2,H-229.0,'Part II — History')
    return make_page(d)

def ko_colophon(n):
    def d(c):
        c.setFont('NMB',14); c.drawString(LEFT,H-154.96,'은하 멸망 사전')
        c.drawString(LEFT,H-180.13,'A Dictionary of Galactic Extinction')
        c.setFont('NMB',12.9); c.drawString(LEFT,H-204.25,'제2부 - 역사편')
        lines=[
            ('Copyright © 2026 Jin-in-Seoul',248.17),('All rights reserved.',269.75),
            ('이 책의 저작권은 Jin-in-Seoul에게 있습니다.',291.32),
            ('저작권자의 허락 없이 이 책의 전부 또는 일부를 복제, 배포, 전송, 변형하거나',312.90),
            ('상업적으로 이용할 수 없습니다.',334.48),('First digital edition, 2026',356.05),
            ('Jin-in-Seoul 발행',377.63),('https://jin-in-seoul.com',399.20),
            ('* 이 디지털 판본은 무료로 배포됩니다. 무료 배포는 저작권의 포기 또는 양도',442.36),
            ('를 의미하지 않습니다.',463.93)]
        for t,y in lines: c.setFont('NM',12); c.drawString(LEFT,H-y,t)
        c.setFont('Helvetica',10); c.drawCentredString(W/2,FOOT,f'- {n} -')
    return make_page(d)

def en_colophon():
    def d(c):
        c.setFont('NMB',14); c.drawString(LEFT,H-182.1,'A Dictionary of Galactic Extinction')
        c.drawString(LEFT,H-207.3,'Part II — History'); y=H-252.0
        lines=['Copyright © 2026 Jin-in-Seoul','All rights reserved.',
               'The copyright in this book belongs to Jin-in-Seoul.',
               'No part of this book may be reproduced, distributed, transmitted, modified,',
               'or used commercially without the permission of the copyright holder.',
               'This digital edition is distributed free of charge.',
               'Free distribution does not waive or transfer any copyright.',
               'First digital edition, 2026','Published by Jin-in-Seoul','https://jin-in-seoul.com']
        for t in lines: c.setFont('NM',12); c.drawString(LEFT,y,t); y-=21.57642
    return make_page(d)

def body_pages(reader, lang):
    start=None
    for i,p in enumerate(reader.pages):
        t=p.extract_text() or ''
        if lang=='en' and '1. First War' in t and 'The cause of the First War was control over the passages.' in t:
            start=i; break
        if lang=='ko' and '1. 제1차 전쟁' in t and '제1차 전쟁의 원인은 통로의 운영권이었다.' in t:
            start=i; break
    if start is None: raise RuntimeError(f'body start not found: {lang}')
    out=[]
    for p in reader.pages[start:]:
        t=p.extract_text() or ''
        if 'Copyright © 2026 Jin-in-Seoul' in t: continue
        out.append(p)
    if not out: raise RuntimeError(f'no body pages: {lang}')
    return out

def find_page_index(reader, required):
    for i,p in enumerate(reader.pages):
        t=p.extract_text() or ''
        if all(x in t for x in required):
            return i
    raise RuntimeError('page not found: '+repr(required))

def front_pages(reader, lang):
    if lang=='en':
        cover=find_page_index(reader,['Free Digital Edition','A Dictionary of Galactic Extinction'])
        quote=find_page_index(reader,['Men in Black'])
        toc=find_page_index(reader,['CONTENTS','PART I','PART II'])
    else:
        cover=find_page_index(reader,['무료 디지털판','은하 멸망 사전'])
        quote=find_page_index(reader,['맨 인 블랙'])
        toc=find_page_index(reader,['목 차','제1부 멸망의 조건','제2부 역사편'])
    return [reader.pages[cover],reader.pages[quote],reader.pages[toc],reader.pages[toc+1],reader.pages[toc+2]]

def rebuild_en():
    ref=PdfReader(str(P1EN)); old=PdfReader(str(P2EN)); body=body_pages(old,'en')
    w=PdfWriter()
    if old.metadata: w.add_metadata({k:str(v) for k,v in old.metadata.items() if v is not None})
    for p in front_pages(ref,'en'): w.add_page(p)
    w.add_page(en_title())
    for p in body: w.add_page(p)
    w.add_page(en_colophon())
    tmp=P2EN.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(P2EN)

def rebuild_ko():
    ref=PdfReader(str(P1KO)); old=PdfReader(str(P2KO)); body=body_pages(old,'ko')
    w=PdfWriter()
    if old.metadata: w.add_metadata({k:str(v) for k,v in old.metadata.items() if v is not None})
    for p in front_pages(ref,'ko'): w.add_page(p)
    w.add_page(ko_title())
    for page_no,p in enumerate(body,start=7):
        p.merge_page(footer_overlay(page_no)); w.add_page(p)
    final_no=len(w.pages)+1; w.add_page(ko_colophon(final_no))
    tmp=P2KO.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(P2KO)

def validate(path,lang):
    r=PdfReader(str(path)); texts=[p.extract_text() or '' for p in r.pages]
    if lang=='en':
        assert 'Free Digital Edition' in texts[0] and 'A Dictionary of Galactic Extinction' in texts[0]
        assert 'Men in Black' in texts[1]
        assert 'CONTENTS' in texts[2] and 'PART I' in texts[2] and 'PART II' in texts[2]
        assert 'PART III' in texts[3]
        assert 'APPENDIX' in texts[4] and 'Index for Those Lost in the Galaxy' in texts[4]
        assert 'Part II — History' in texts[5] and 'Copyright' not in texts[5]
        assert '1. First War' in texts[6] and 'The cause of the First War' in texts[6]
        hits=[i for i,t in enumerate(texts) if 'Copyright © 2026 Jin-in-Seoul' in t]
        assert hits==[len(texts)-1], hits
        assert 'Part II — History' in texts[-1] and 'Part I — Conditions of Extinction' not in texts[-1]
        assert 'Published by Jin-in-Seoul' in texts[-1]
        titles=['1. First War','2. Galactic Standard Time Accord','3. Declaration on the Right to Connection','4. Second War','5. Third War','6. Third Passage Mandate Act','7. First Observation of the Deficit','8. Return Eligibility Ruling','9. Energy Receivables Accounting Revision Proposal','10. Declaration of Extraterrestrial Intervention','11. Fourth War — Cold War','12. Closure of the Passages','13. Zero-Latency Disaster','14. Fifth and Sixth Wars','15. Connection of the Storage Space','16. Galactic Extinction Determination']
    else:
        assert '무료 디지털판' in texts[0] and '은하 멸망 사전' in texts[0]
        assert '맨 인 블랙' in texts[1]
        assert '목 차' in texts[2] and '제1부 멸망의 조건' in texts[2] and '제2부 역사편' in texts[2]
        assert '제3부 인물편' in texts[3]
        assert '부록' in texts[4] and '은하에서 길 잃은 자를 위한 색인' in texts[4]
        assert '제2부 역사편' in texts[5] and 'Copyright' not in texts[5]
        assert '- 6 -' in texts[5]
        assert '1. 제1차 전쟁' in texts[6] and '제1차 전쟁의 원인은 통로의 운영권이었다.' in texts[6]
        hits=[i for i,t in enumerate(texts) if 'Copyright © 2026 Jin-in-Seoul' in t]
        assert hits==[len(texts)-1], hits
        assert '제2부 - 역사편' in texts[-1] and '제1부 - 멸망의 조건' not in texts[-1]
        assert 'Jin-in-Seoul 발행' in texts[-1]
        assert f'- {len(texts)} -' in texts[-1]
        titles=['1. 제1차 전쟁','2. 은하표준시 협정','3. 연결권 선언','4. 제2차 전쟁','5. 제3차 전쟁','6. 제3통로 의무법','7. 최초 결손 관측','8. 귀환 가능자 판결','9. 미수에너지 회계 개정안','10. 외계 개입 선언','11. 제4차 전쟁 - 냉전','12. 통로 폐쇄','13. 무지연 참사','14. 제5·6차 전쟁','15. 저장공간 연결','16. 은하 멸망 판정']
    alltext='\n'.join(texts)
    for title in titles: assert title in alltext, title
    print(lang,'pages',len(texts),'copyright-page',hits[0]+1,'all 16 titles OK')

rebuild_en(); rebuild_ko(); validate(P2EN,'en'); validate(P2KO,'ko')
