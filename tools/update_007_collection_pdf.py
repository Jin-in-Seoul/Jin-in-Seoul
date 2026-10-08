from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML
import html, fitz

ROOT=Path('.')
OUT=ROOT/'assets/downloads/adjunct-lecturer-k-007-briefcase/ko/adjunct-lecturer-k-007-briefcase-ko-20261007-ver-001.pdf'
WORKS=[
 ('오후만 있던 일요일','a-sunday-that-was-only-afternoon'),
 ('마리화나','marijuana'),
 ('논리학의 기초','the-basics-of-logic'),
 ('형의 인생','hyungs-life'),
 ('시간강사 K의 007 가방','adjunct-lecturer-k-007-briefcase'),
 ('여진','aftershock'),
 ('훔친 오후','a-stolen-afternoon'),
]
END_MARKERS={'-끝-','- 끝 -','— 끝 —','― 끝 ―','끝'}
def clean(s): return s.replace('\xa0',' ').strip()
def story(title,slug):
    p=ROOT/'short-stories'/slug/'ko/index.html'
    s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    art=s.find('article',class_='prose')
    if art is None: raise RuntimeError(f'prose missing {p}')
    items=[]
    for el in art.find_all('p',recursive=False):
        if el.get('aria-hidden')=='true': continue
        t=clean(el.get_text(' ',strip=True))
        if not t or t in END_MARKERS: continue
        cls='section-number' if 'section-number' in (el.get('class') or []) else ''
        items.append((cls,t))
    return {'title':title,'slug':slug,'items':items}
stories=[story(*w) for w in WORKS]
assert [len(x['items']) for x in stories]==[6,190,203,49,169,147,98]

css=r'''
@page { size:A4; margin: 25.4mm; @bottom-center { content: counter(page); font-family: Arial, sans-serif; font-size: 11pt; } }
@page fixed { size:A4; margin:0; @bottom-center { content: counter(page); font-family: Arial, sans-serif; font-size: 11pt; } }
html,body { margin:0; padding:0; color:#111; font-family:"Nanum Myeongjo",serif; font-size:12pt; }
.fixed { page:fixed; width:210mm; height:297mm; position:relative; page-break-after:always; }
.cover .edition { position:absolute; left:25.4mm; top:30.7mm; font-size:12pt; }
.cover .edition-note { position:absolute; left:25.4mm; top:38.0mm; font-size:12pt; }
.cover .title { position:absolute; left:20mm; right:20mm; top:81.5mm; text-align:center; font-size:20pt; line-height:1.4; }
.cover .subtitle { position:absolute; left:20mm; right:20mm; top:127.0mm; text-align:center; font-size:14pt; }
.copyright .box { position:absolute; left:25.4mm; right:25.4mm; top:52.0mm; font-size:12pt; line-height:1.72; }
.copyright .box p { margin:0 0 0; text-indent:0; text-align:left; }
.copyright .ctitle { font-family:"Nanum Myeongjo"; font-weight:700; margin-bottom:7.3mm !important; }
.copyright .gap { margin-top:7.3mm !important; }
.toc .tocbox { position:absolute; left:75.5mm; top:59.4mm; width:68mm; }
.toc .toctitle { text-align:center; font-size:16pt; font-weight:700; margin:0 0 14.7mm; }
.toc ul { list-style:disc; padding-left:8mm; margin:0; font-size:14pt; line-height:1.72; }
.story { page-break-before:always; }
.story h1 { font-size:16pt; text-align:center; font-weight:700; margin:5.5mm 0 32mm; }
.story p { margin:0 0 7.4pt; text-indent:11.4pt; line-height:26.9pt; text-align:justify; word-break:keep-all; }
.story p.section-number { text-indent:0; text-align:center; margin:0 0 26.9pt; font-weight:400; }
'''
cover='''<section class="fixed cover"><div class="edition">무료 디지털판</div><div class="edition-note">이 판본은 무료로 배포됩니다</div><div class="title">시간강사 K의 007 가방</div><div class="subtitle">단편소설집</div></section>'''
cp='''<section class="fixed copyright"><div class="box">
<p class="ctitle">시간강사 K의 007 가방</p>
<p>Copyright © 2026 Jin-in-Seoul All rights reserved.</p>
<p>이 책의 저작권은 Jin-in-Seoul에게 있습니다.</p>
<p>저작권자의 허락 없이 이 책의 전부 또는 일부를 복제, 배포, 전송, 변형하거나 상업적으로 이용할 수 없습니다.</p>
<p class="gap">First digital edition, 2026<br/>Published by Jin-in-Seoul<br/>https://jin-in-seoul.com</p>
<p class="gap">* 이 디지털 판본은 무료로 배포됩니다. 무료 배포는 저작권의 포기 또는 양도를 의미하지 않습니다.</p>
</div></section>'''
toc='''<section class="fixed toc"><div class="tocbox"><div class="toctitle">- 목 차 -</div><ul>'''+''.join(f'<li>{html.escape(s["title"])}</li>' for s in stories)+'</ul></div></section>'
secs=[]
for st in stories:
    ps=[]
    for cls,t in st['items']:
        c=' class="section-number"' if cls else ''
        ps.append(f'<p{c}>{html.escape(t)}</p>')
    secs.append(f'<section class="story"><h1>{html.escape(st["title"])}</h1>{"".join(ps)}</section>')
doc=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{css}</style></head><body>{cover}{cp}{toc}{"".join(secs)}</body></html>'
HTML(string=doc,base_url=str(ROOT.resolve())).write_pdf(str(OUT))

d=fitz.open(OUT)
txt='\n'.join(p.get_text() for p in d)
print('PAGES',len(d),'SIZE',OUT.stat().st_size)
assert len(d)==109, len(d)
assert '거실 소파에 누웠다.' in txt
assert all(x['title'] in txt for x in stories)
d.close()

dp=ROOT/'downloads/index.html'
s=dp.read_text(encoding='utf-8')
old='<p class="download-part">Complete edition</p>\n\n        <section class="download-language" lang="ko">'
new='<p class="download-part">Complete edition · Short-story collection · 7 stories</p>\n\n        <section class="download-language" lang="ko">'
anchor='<h2>Adjunct Lecturer K’s 007 Briefcase</h2>'
pos=s.find(anchor)
if pos<0: raise RuntimeError('download work missing')
tail=s[pos:]
if old not in tail: raise RuntimeError('download descriptor pattern missing')
tail=tail.replace(old,new,1)
s=s[:pos]+tail
dp.write_text(s,encoding='utf-8')

lp=ROOT/'publication-log/index.html'
s=lp.read_text(encoding='utf-8')
old='Korean short-story collection (<em>시간강사 K의 007 가방</em>) — free PDF and EPUB editions added'
new='Korean short-story collection (<em>시간강사 K의 007 가방</em>) — complete edition, 7 stories; free PDF and EPUB editions added'
if old not in s: raise RuntimeError('publication log entry missing')
s=s.replace(old,new,1)
lp.write_text(s,encoding='utf-8')
print('SITE TEXT UPDATED')
