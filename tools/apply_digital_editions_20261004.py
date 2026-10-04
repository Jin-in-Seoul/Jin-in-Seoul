from pathlib import Path
from io import BytesIO
import html, re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter

ROOT = Path.cwd()
REG = '/usr/share/fonts/truetype/nanum/NanumMyeongjo.ttf'
BOLD = '/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf'
pdfmetrics.registerFont(TTFont('NM', REG))
pdfmetrics.registerFont(TTFont('NMB', BOLD))
W, H = A4
LEFT = 85.0339
RIGHT = 509.9636
WIDTH = RIGHT - LEFT
SIZE = 12.0
LEAD = 21.57642

P1_EN = ROOT / 'assets/downloads/a-dictionary-of-galactic-extinction/part-01/en/a-dictionary-of-galactic-extinction-part-01-en-20260929-ver-001.pdf'
P1_KO = ROOT / 'assets/downloads/a-dictionary-of-galactic-extinction/part-01/ko/a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.pdf'
P2_EN = ROOT / 'assets/downloads/a-dictionary-of-galactic-extinction/part-02/en/a-dictionary-of-galactic-extinction-part-02-en-20261004-ver-001.pdf'
P2_KO = ROOT / 'assets/downloads/a-dictionary-of-galactic-extinction/part-02/ko/a-dictionary-of-galactic-extinction-part-02-ko-20261004-ver-001.pdf'

def clean_html(s):
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).strip()

def read_entries(lang):
    out=[]
    for n in range(1,17):
        p=ROOT/f'a-dictionary-of-galactic-extinction/{lang}/part-02/entry-{n:02d}/index.html'
        src=p.read_text(encoding='utf-8')
        mt=re.search(r'<h1 class="entry-title">([\s\S]*?)</h1>',src)
        ma=re.search(r'<article class="prose">([\s\S]*?)</article>',src)
        if not mt or not ma: raise RuntimeError(f'Could not parse {p}')
        out.append((clean_html(mt.group(1)),[clean_html(x) for x in re.findall(r'<p>([\s\S]*?)</p>',ma.group(1))]))
    return out

def add_metadata(w,r):
    if r.metadata: w.add_metadata({k:str(v) for k,v in r.metadata.items() if v is not None})

def page_from_canvas(draw):
    buf=BytesIO(); c=canvas.Canvas(buf,pagesize=A4,pageCompression=1); draw(c); c.showPage(); c.save(); buf.seek(0); return PdfReader(buf).pages[0]

def ko_footer(c,n):
    c.setFont('Helvetica',10); c.drawCentredString(W/2,43.5,f'- {n} -')

def ko_colophon_page():
    def draw(c):
        c.setFont('NMB',14); c.drawString(LEFT,H-156.96+2,'은하 멸망 사전')
        c.setFont('NMB',14); c.drawString(LEFT,H-182.13+2,'A Dictionary of Galactic Extinction')
        c.setFont('NMB',12.9); c.drawString(LEFT,H-206.25+2,'제2부 - 역사편')
        lines=[
            ('Copyright © 2026 Jin-in-Seoul',250.17),('All rights reserved.',271.75),
            ('이 책의 저작권은 Jin-in-Seoul에게 있습니다.',293.32),
            ('저작권자의 허락 없이 이 책의 전부 또는 일부를 복제, 배포, 전송, 변형하거나',314.90),
            ('상업적으로 이용할 수 없습니다.',336.48),('First digital edition, 2026',358.05),
            ('Jin-in-Seoul 발행',379.63),('https://jin-in-seoul.com',401.20),
            ('* 이 디지털 판본은 무료로 배포됩니다. 무료 배포는 저작권의 포기 또는 양도',444.36),
            ('를 의미하지 않습니다.',465.93)]
        for text,y in lines: c.setFont('NM',12); c.drawString(LEFT,H-y+2,text)
        ko_footer(c,2)
    return page_from_canvas(draw)

def ko_renumber_overlay(page,n):
    def draw(c):
        c.setFillColorRGB(1,1,1); c.rect(0,25,W,40,fill=1,stroke=0); c.setFillColorRGB(0,0,0); ko_footer(c,n)
    page.merge_page(page_from_canvas(draw)); return page

def ko_title_page():
    def draw(c):
        c.setFont('NMB',20); c.drawCentredString(W/2,H-228.04+3,'제2부 역사편'); ko_footer(c,7)
    return page_from_canvas(draw)

CLOSE=set('.,!?;:)]}〉》」』】’”·…。！？；：、）］｝》」』】')

def ko_wrap_chars(text,maxw):
    lines=[]; cur=''; i=0
    while i<len(text):
        ch=text[i]; trial=cur+ch
        if not cur or pdfmetrics.stringWidth(trial,'NM',SIZE)<=maxw: cur=trial; i+=1; continue
        if ch in CLOSE and cur:
            carry=cur[-1]; cur=cur[:-1]
            if cur: lines.append(cur)
            cur=carry+ch; i+=1
        else: lines.append(cur); cur=''
    if cur: lines.append(cur)
    return lines

def ko_para_records(text):
    indent=12.0; fl=ko_wrap_chars(text,WIDTH-indent); first=fl[0]; rest=text[len(first):]
    rec=[{'text':first,'indent':True,'para_start':True,'para_end':not rest}]
    if rest:
        rl=ko_wrap_chars(rest,WIDTH)
        for j,l in enumerate(rl): rec.append({'text':l,'indent':False,'para_start':False,'para_end':j==len(rl)-1})
    return rec

def ko_paginate(records):
    first_y=H-202.52234; cont_y=H-111.72096; bottom=101.5
    first_cap=int((first_y-bottom)//LEAD)+1; cont_cap=int((cont_y-bottom)//LEAD)+1
    caps=[]; rem=len(records); first=True
    while rem:
        cap=first_cap if first else cont_cap; first=False; n=min(cap,rem); caps.append(n); rem-=n
    if len(caps)>1 and caps[-1]<7:
        need=7-caps[-1]
        for j in range(len(caps)-2,-1,-1):
            movable=max(0,caps[j]-7); take=min(need,movable); caps[j]-=take; caps[-1]+=take; need-=take
            if need==0: break
    chunks=[]; pos=0
    for n in caps: chunks.append(records[pos:pos+n]); pos+=n
    for j in range(len(chunks)-1):
        if chunks[j] and chunks[j][-1]['para_start'] and not chunks[j][-1]['para_end']: chunks[j+1].insert(0,chunks[j].pop())
        if len(chunks[j+1])>=2 and (not chunks[j+1][0]['para_start']) and chunks[j+1][0]['para_end'] and chunks[j+1][1]['para_start'] and len(chunks[j])>7: chunks[j+1].insert(0,chunks[j].pop())
    return chunks

def build_ko_part2(entries):
    P2_KO.parent.mkdir(parents=True,exist_ok=True); body_path=ROOT/'.part02_ko_body.pdf'
    c=canvas.Canvas(str(body_path),pagesize=A4,pageCompression=1); pageno=8
    title_y=H-115.10968; first_y=H-202.52234; cont_y=H-111.72096; indent=12.0
    for title,paras in entries:
        rec=[]
        for p in paras: rec.extend(ko_para_records(p))
        for ci,chunk in enumerate(ko_paginate(rec)):
            if ci==0: c.setFont('NMB',14); c.drawCentredString(W/2,title_y,title); y=first_y
            else: y=cont_y
            for r in chunk:
                x=LEFT+(indent if r['indent'] else 0); maxw=WIDTH-(indent if r['indent'] else 0)
                txt=r['text']; nat=pdfmetrics.stringWidth(txt,'NM',SIZE); c.setFont('NM',SIZE)
                if not r['para_end'] and len(txt)>1 and nat<maxw:
                    cs=(maxw-nat)/(len(txt)-1); t=c.beginText(x,y); t.setFont('NM',SIZE); t.setCharSpace(cs); t.textLine(txt); c.drawText(t)
                else: c.drawString(x,y,txt)
                y-=LEAD
            ko_footer(c,pageno); c.showPage(); pageno+=1
    c.save()
    ref=PdfReader(str(P1_KO)); body=PdfReader(str(body_path)); w=PdfWriter(); add_metadata(w,ref)
    w.add_page(ref.pages[0]); w.add_page(ko_colophon_page())
    for old_i,new_no in zip(range(1,5),range(3,7)): w.add_page(ko_renumber_overlay(ref.pages[old_i],new_no))
    w.add_page(ko_title_page())
    for p in body.pages: w.add_page(p)
    with P2_KO.open('wb') as f: w.write(f)
    body_path.unlink(missing_ok=True)

def en_colophon_page():
    def draw(c):
        c.setFont('NMB',14); c.drawString(LEFT,H-182.1,'A Dictionary of Galactic Extinction'); c.drawString(LEFT,H-207.3,'Part II — History')
        y=H-252.0
        lines=['Copyright © 2026 Jin-in-Seoul','All rights reserved.','The copyright in this book belongs to Jin-in-Seoul.','No part of this book may be reproduced, distributed, transmitted, modified,','or used commercially without the permission of the copyright holder.','This digital edition is distributed free of charge.','Free distribution does not waive or transfer any copyright.','First digital edition, 2026','Published by Jin-in-Seoul','https://jin-in-seoul.com']
        for t in lines: c.setFont('NM',12); c.drawString(LEFT,y,t); y-=LEAD
    return page_from_canvas(draw)

def en_part_title(text):
    def draw(c): c.setFont('NMB',20); c.drawCentredString(W/2,H-229,text)
    return page_from_canvas(draw)

def en_wrap_words(text):
    words=text.split(' '); lines=[]; cur=''
    for word in words:
        trial=word if not cur else cur+' '+word
        if pdfmetrics.stringWidth(trial,'NM',SIZE)<=WIDTH: cur=trial
        else:
            if cur: lines.append(cur)
            if pdfmetrics.stringWidth(word,'NM',SIZE)<=WIDTH: cur=word
            else:
                chunk=''
                for ch in word:
                    tr=chunk+ch
                    if not chunk or pdfmetrics.stringWidth(tr,'NM',SIZE)<=WIDTH: chunk=tr
                    else: lines.append(chunk); chunk=ch
                cur=chunk
    if cur: lines.append(cur)
    return lines

def en_paginate(lines):
    first_y=H-202.5; cont_y=H-111.7; bottom=95.0
    first_cap=int((first_y-bottom)//LEAD)+1; cont_cap=int((cont_y-bottom)//LEAD)+1
    caps=[]; rem=len(lines); first=True
    while rem:
        cap=first_cap if first else cont_cap; first=False; n=min(cap,rem); caps.append(n); rem-=n
    if len(caps)>1 and caps[-1]<7:
        need=7-caps[-1]
        for j in range(len(caps)-2,-1,-1):
            movable=max(0,caps[j]-7); take=min(need,movable); caps[j]-=take; caps[-1]+=take; need-=take
            if need<=0: break
    chunks=[]; pos=0
    for n in caps: chunks.append(lines[pos:pos+n]); pos+=n
    return chunks

def build_en_part2(entries):
    P2_EN.parent.mkdir(parents=True,exist_ok=True); body_path=ROOT/'.part02_en_body.pdf'
    c=canvas.Canvas(str(body_path),pagesize=A4,pageCompression=1)
    for title,paras in entries:
        lines=[]
        for p in paras: lines.extend(en_wrap_words(p))
        for ci,chunk in enumerate(en_paginate(lines)):
            if ci==0: c.setFont('NMB',14); c.drawCentredString(W/2,H-111.7,title); y=H-202.5
            else: y=H-111.7
            c.setFont('NM',SIZE)
            for line in chunk: c.drawString(LEFT,y,line); y-=LEAD
            c.showPage()
    c.save()
    ref=PdfReader(str(P1_EN)); body=PdfReader(str(body_path)); w=PdfWriter(); add_metadata(w,ref)
    w.add_page(ref.pages[0]); w.add_page(en_colophon_page()); w.add_page(ref.pages[1])
    for i in [2,3,4]: w.add_page(ref.pages[i])
    w.add_page(en_part_title('Part II — History'))
    for p in body.pages: w.add_page(p)
    with P2_EN.open('wb') as f: w.write(f)
    body_path.unlink(missing_ok=True)

def fix_en_part1():
    r=PdfReader(str(P1_EN))
    if len(r.pages)>=6 and 'Part I — Conditions of Extinction' in (r.pages[5].extract_text() or ''): return
    w=PdfWriter(); add_metadata(w,r)
    for i,p in enumerate(r.pages):
        if i==5: w.add_page(en_part_title('Part I — Conditions of Extinction'))
        w.add_page(p)
    tmp=P1_EN.with_suffix('.tmp.pdf')
    with tmp.open('wb') as f: w.write(f)
    tmp.replace(P1_EN)

def update_downloads():
    p=ROOT/'downloads/index.html'; s=p.read_text(encoding='utf-8')
    if 'data-part="part-02"' not in s:
        marker='''        <p class="download-note">
          This work consists of five parts. The currently available download contains Part I only.
        </p>'''
        block='''        <p class="download-part">Part II — History</p>

        <section class="download-language">
          <h3>English</h3>
          <ul class="download-files">
            <li><a download data-download-track data-work="a-dictionary-of-galactic-extinction" data-part="part-02" data-language="en" data-format="pdf" data-version="001" href="/assets/downloads/a-dictionary-of-galactic-extinction/part-02/en/a-dictionary-of-galactic-extinction-part-02-en-20261004-ver-001.pdf">a-dictionary-of-galactic-extinction-part-02-en-20261004-ver-001.pdf</a></li>
          </ul>
          <p class="download-meta">Updated: October 4, 2026 · Version 001</p>
        </section>

        <section class="download-language" lang="ko">
          <h3>한국어</h3>
          <ul class="download-files">
            <li><a download data-download-track data-work="a-dictionary-of-galactic-extinction" data-part="part-02" data-language="ko" data-format="pdf" data-version="001" href="/assets/downloads/a-dictionary-of-galactic-extinction/part-02/ko/a-dictionary-of-galactic-extinction-part-02-ko-20261004-ver-001.pdf">a-dictionary-of-galactic-extinction-part-02-ko-20261004-ver-001.pdf</a></li>
          </ul>
          <p class="download-meta">Updated: October 4, 2026 · Version 001</p>
        </section>

        <p class="download-note">
          This work consists of five parts. Free digital editions are released separately by part while the work is in progress.
        </p>'''
        if marker not in s: raise RuntimeError('downloads marker not found')
        p.write_text(s.replace(marker,block),encoding='utf-8')

def update_log():
    p=ROOT/'publication-log/index.html'; s=p.read_text(encoding='utf-8')
    if '<h2>October 4, 2026</h2>' not in s:
        block='''      <section>
        <h2>October 4, 2026</h2>
        <h3>A Dictionary of Galactic Extinction</h3>
        <ul>
          <li>Part II — free PDF editions added in English and Korean</li>
        </ul>
      </section>

'''
        marker='''    </div>

    {% include footer.html %}'''
        if marker not in s: raise RuntimeError('publication-log marker not found')
        p.write_text(s.replace(marker,block+marker),encoding='utf-8')

def validate():
    for p in [P1_EN,P2_EN,P2_KO]:
        r=PdfReader(str(p)); assert len(r.pages)>10; print(p,len(r.pages),p.stat().st_size)
    assert 'Part I — Conditions of Extinction' in (PdfReader(str(P1_EN)).pages[5].extract_text() or '')
    en_text=''.join((x.extract_text() or '') for x in PdfReader(str(P2_EN)).pages)
    ko_text=''.join((x.extract_text() or '') for x in PdfReader(str(P2_KO)).pages)
    for title,_ in read_entries('en'):
        if title not in en_text: raise RuntimeError('missing EN title '+title)
    for title,_ in read_entries('ko'):
        if title not in ko_text: raise RuntimeError('missing KO title '+title)

def main():
    en=read_entries('en'); ko=read_entries('ko')
    build_en_part2(en); build_ko_part2(ko); fix_en_part1(); update_downloads(); update_log(); validate()

if __name__=='__main__': main()
