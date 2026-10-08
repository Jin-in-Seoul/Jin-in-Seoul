from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML
from lxml import etree
import html, zipfile, uuid, shutil, tempfile, re, hashlib

ROOT=Path('.')
OUTDIR=ROOT/'assets/downloads/adjunct-lecturer-k-007-briefcase/ko'
OUTDIR.mkdir(parents=True,exist_ok=True)
PDF=OUTDIR/'adjunct-lecturer-k-007-briefcase-ko-20261007-ver-001.pdf'
EPUB=OUTDIR/'adjunct-lecturer-k-007-briefcase-ko-20261007-ver-001.epub'

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

def clean_text(s):
    return s.replace('\xa0',' ').strip()

def get_story(display_title,slug):
    p=ROOT/'short-stories'/slug/'ko/index.html'
    raw=p.read_text(encoding='utf-8')
    soup=BeautifulSoup(raw,'html.parser')
    art=soup.find('article',class_='prose')
    if art is None: raise RuntimeError(f'prose missing: {p}')
    items=[]
    for el in art.find_all('p',recursive=False):
        if el.get('aria-hidden')=='true':
            continue
        txt=clean_text(el.get_text(' ',strip=True))
        if not txt or txt in END_MARKERS:
            continue
        cls='section-number' if 'section-number' in (el.get('class') or []) else ''
        items.append((cls,txt))
    if not items: raise RuntimeError(f'empty story: {p}')
    return {'title':display_title,'slug':slug,'items':items}

stories=[get_story(*w) for w in WORKS]
expected_counts=[6,190,203,49,169,148,98]
assert [len(s['items']) for s in stories]==expected_counts, [(s['title'],len(s['items'])) for s in stories]

css=r'''
@page { size:A4; margin: 25.4mm 25.4mm 25.4mm 25.4mm; @bottom-center { content: counter(page); font-family: Arial, sans-serif; font-size: 8.5pt; } }
@page fixed { size:A4; margin:0; @bottom-center { content: counter(page); font-family: Arial, sans-serif; font-size: 8.5pt; } }
html,body { margin:0; padding:0; color:#111; font-family:"Nanum Myeongjo","Noto Serif CJK KR",serif; font-size:12pt; }
.fixed { page:fixed; width:210mm; height:297mm; position:relative; page-break-after:always; }
.cover .edition { position:absolute; left:25mm; top:28mm; font-size:11pt; }
.cover .edition-note { position:absolute; left:25mm; top:40mm; font-size:10.5pt; }
.cover .title { position:absolute; left:20mm; right:20mm; top:96mm; text-align:center; font-size:22pt; line-height:1.4; }
.cover .subtitle { position:absolute; left:20mm; right:20mm; top:151mm; text-align:center; font-size:13pt; }
.copyright .box { position:absolute; left:25mm; right:25mm; top:58mm; font-size:10.8pt; line-height:1.75; }
.copyright .box p { margin:0 0 4.5mm; text-indent:0; text-align:left; }
.copyright .ctitle { font-size:12pt; margin-bottom:14mm !important; }
.toc .tocbox { position:absolute; left:61mm; top:67mm; width:88mm; }
.toc .toctitle { text-align:center; font-size:16pt; letter-spacing:.25em; margin:0 0 25mm; }
.toc ul { list-style:disc; padding-left:7mm; margin:0; font-size:12pt; line-height:1.9; }
.story { page-break-before:always; }
.story h1 { font-size:16pt; text-align:center; font-weight:600; margin:6mm 0 43mm; }
.story p { margin:0 0 16.5pt; text-indent:.95em; line-height:2.25; text-align:justify; word-break:keep-all; }
.story p.section-number { text-indent:0; text-align:center; margin:0 0 8mm; font-weight:600; }
.story.a-stolen-afternoon p:not(.section-number){margin-bottom:24pt;}
'''
cover='''<section class="fixed cover"><div class="edition">무료 디지털판</div><div class="edition-note">이 판본은 무료로 배포됩니다</div><div class="title">시간강사 K의 007 가방</div><div class="subtitle">단편소설집</div></section>'''
cp='''<section class="fixed copyright"><div class="box">
<p class="ctitle">시간강사 K의 007 가방</p>
<p>Copyright © 2026 Jin-in-Seoul All rights reserved.</p>
<p>이 책의 저작권은 Jin-in-Seoul에게 있습니다.</p>
<p>저작권자의 허락 없이 이 책의 전부 또는 일부를 복제, 배포, 전송, 변형하거나 상업적으로 이용할 수 없습니다.</p>
<p>First digital edition, 2026<br/>Published by Jin-in-Seoul<br/>https://jin-in-seoul.com</p>
<p>* 이 디지털 판본은 무료로 배포됩니다. 무료 배포는 저작권의 포기 또는 양도를 의미하지 않습니다.</p>
</div></section>'''
toc='''<section class="fixed toc"><div class="tocbox"><div class="toctitle">- 목 차 -</div><ul>'''+''.join(f'<li>{html.escape(s["title"])}</li>' for s in stories)+'</ul></div></section>'
sections=[]
for st in stories:
    body=[]
    for cls,txt in st['items']:
        c=' class="section-number"' if cls else ''
        body.append(f'<p{c}>{html.escape(txt)}</p>')
    sections.append(f'<section class="story {st["slug"]}"><h1>{html.escape(st["title"])}</h1>{"".join(body)}</section>')
pdf_html=f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{css}</style></head><body>{cover}{cp}{toc}{"".join(sections)}</body></html>'
HTML(string=pdf_html,base_url=str(ROOT.resolve())).write_pdf(str(PDF))

td=Path(tempfile.mkdtemp(prefix='epub007_'))
try:
    (td/'META-INF').mkdir()
    (td/'EPUB/Text').mkdir(parents=True)
    (td/'EPUB/Styles').mkdir(parents=True)
    (td/'EPUB/Images').mkdir(parents=True)
    (td/'mimetype').write_text('application/epub+zip',encoding='ascii')
    (td/'META-INF/container.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',encoding='utf-8')
    ecss='''body{font-family:serif;line-height:1.75;margin:5%;color:#111;}h1{font-size:1.5em;font-weight:600;text-align:center;margin:2.8em 0 2.2em;}p{margin:0 0 .85em;text-indent:1em;}p.section-number{text-indent:0;text-align:center;margin:2em 0 1.5em}.copyright{text-align:left}.copyright h1{text-align:left;margin:1.5em 0 2em;font-size:1.35em}.copyright p{text-indent:0;text-align:left;margin:0 0 1.2em}nav ol{line-height:2}nav a{color:inherit;text-decoration:none}.cover{margin:0;padding:0}.cover svg{width:100%;height:auto;display:block}'''
    (td/'EPUB/Styles/style.css').write_text(ecss,encoding='utf-8')
    svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1600"><rect width="1200" height="1600" fill="white"/><g fill="#111" font-family="serif"><text x="120" y="150" font-size="42">무료 디지털판</text><text x="120" y="215" font-size="34">이 판본은 무료로 배포됩니다</text><text x="600" y="650" font-size="68" text-anchor="middle">시간강사 K의 007 가방</text><text x="600" y="900" font-size="42" text-anchor="middle">단편소설집</text></g></svg>'''
    (td/'EPUB/Images/cover.svg').write_text(svg,encoding='utf-8')
    def page(title,body,cls=''):
        return f'''<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ko" lang="ko"><head><meta charset="utf-8"/><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="../Styles/style.css"/></head><body class="{cls}">{body}</body></html>'''
    coverx='''<div class="cover"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1600"><rect width="1200" height="1600" fill="white"/><g fill="#111" font-family="serif"><text x="120" y="150" font-size="42">무료 디지털판</text><text x="120" y="215" font-size="34">이 판본은 무료로 배포됩니다</text><text x="600" y="650" font-size="68" text-anchor="middle">시간강사 K의 007 가방</text><text x="600" y="900" font-size="42" text-anchor="middle">단편소설집</text></g></svg></div>'''
    (td/'EPUB/Text/cover.xhtml').write_text(page('표지',coverx),encoding='utf-8')
    cpbody='''<section class="copyright"><h1>시간강사 K의 007 가방</h1><p>Copyright © 2026 Jin-in-Seoul. All rights reserved.</p><p>이 책의 저작권은 Jin-in-Seoul에게 있습니다.</p><p>저작권자의 허락 없이 이 책의 전부 또는 일부를 복제, 배포, 전송, 변형하거나 상업적으로 이용할 수 없습니다.</p><p>First digital edition, 2026<br/>Published by Jin-in-Seoul<br/>https://jin-in-seoul.com</p><p>* 이 디지털 판본은 무료로 배포됩니다. 무료 배포는 저작권의 포기 또는 양도를 의미하지 않습니다.</p></section>'''
    (td/'EPUB/Text/copyright.xhtml').write_text(page('판권',cpbody,'copyright'),encoding='utf-8')
    story_files=[]
    for i,st in enumerate(stories,1):
        fn=f'story-{i:02d}.xhtml'; story_files.append(fn)
        parts=[f'<h1>{html.escape(st["title"])}</h1>']
        for cls,txt in st['items']:
            c=' class="section-number"' if cls else ''
            parts.append(f'<p{c}>{html.escape(txt)}</p>')
        (td/'EPUB/Text'/fn).write_text(page(st['title'],''.join(parts)),encoding='utf-8')
    navitems=''.join(f'<li><a href="Text/{fn}">{html.escape(st["title"])}</a></li>' for fn,st in zip(story_files,stories))
    nav=f'''<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ko"><head><title>목차</title><link rel="stylesheet" href="Styles/style.css" type="text/css"/></head><body><nav epub:type="toc" id="toc"><h1>목차</h1><ol>{navitems}</ol></nav></body></html>'''
    (td/'EPUB/nav.xhtml').write_text(nav,encoding='utf-8')
    uid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'https://jin-in-seoul.com/assets/downloads/adjunct-lecturer-k-007-briefcase/ko/20261007/001'))
    manifest=['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>','<item id="css" href="Styles/style.css" media-type="text/css"/>','<item id="coverimg" href="Images/cover.svg" media-type="image/svg+xml" properties="cover-image"/>','<item id="cover" href="Text/cover.xhtml" media-type="application/xhtml+xml"/>','<item id="copyright" href="Text/copyright.xhtml" media-type="application/xhtml+xml"/>']
    spine=['cover','copyright']
    for i,fn in enumerate(story_files,1):
        manifest.append(f'<item id="s{i}" href="Text/{fn}" media-type="application/xhtml+xml"/>'); spine.append(f's{i}')
    opf=f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="ko"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">{uid}</dc:identifier><dc:title>시간강사 K의 007 가방</dc:title><dc:language>ko</dc:language><dc:creator>Jin-in-Seoul</dc:creator><dc:publisher>Jin-in-Seoul</dc:publisher><dc:rights>Copyright © 2026 Jin-in-Seoul. All rights reserved.</dc:rights><dc:date>2026-10-07</dc:date><meta property="dcterms:modified">2026-10-07T15:00:00Z</meta></metadata><manifest>{''.join(manifest)}</manifest><spine>{''.join(f'<itemref idref="{x}"/>' for x in spine)}</spine></package>'''
    (td/'EPUB/package.opf').write_text(opf,encoding='utf-8')
    for p in list((td/'EPUB').rglob('*.xhtml'))+[td/'EPUB/package.opf',td/'META-INF/container.xml']:
        etree.parse(str(p))
    if EPUB.exists(): EPUB.unlink()
    with zipfile.ZipFile(EPUB,'w') as z:
        z.write(td/'mimetype','mimetype',compress_type=zipfile.ZIP_STORED)
        for p in sorted(td.rglob('*')):
            if p.is_file() and p.name!='mimetype': z.write(p,p.relative_to(td).as_posix(),compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(EPUB) as z:
        assert z.namelist()[0]=='mimetype' and z.getinfo('mimetype').compress_type==zipfile.ZIP_STORED and z.testzip() is None
        assert 'EPUB/Text/title.xhtml' not in z.namelist()
finally:
    shutil.rmtree(td,ignore_errors=True)

with zipfile.ZipFile(EPUB) as z:
    for i,st in enumerate(stories,1):
        sx=BeautifulSoup(z.read(f'EPUB/Text/story-{i:02d}.xhtml').decode('utf-8'),'html.parser')
        got=[clean_text(p.get_text(' ',strip=True)) for p in sx.find_all('p')]
        src=[t for _,t in st['items']]
        assert got==src,(st['title'],len(got),len(src))

try:
    import fitz
    d=fitz.open(PDF)
    txt='\n'.join(p.get_text() for p in d)
    assert len(d)>50
    for st in stories: assert st['title'] in txt
    assert '거실 소파에 누웠다.' in txt
    d.close()
except ImportError:
    pass

dp=ROOT/'downloads/index.html'; s=dp.read_text(encoding='utf-8')
pdfname=PDF.name; epubname=EPUB.name
if pdfname not in s:
    block=f'''\n\n      <section class="download-work">\n        <h2>Adjunct Lecturer K’s 007 Briefcase</h2>\n        <p class="download-part">Complete edition</p>\n\n        <section class="download-language" lang="ko">\n          <h3>한국어</h3>\n          <ul class="download-files">\n            <li><a download data-download-track data-work="adjunct-lecturer-k-007-briefcase" data-language="ko" data-format="pdf" data-version="001" href="/assets/downloads/adjunct-lecturer-k-007-briefcase/ko/{pdfname}">{pdfname}</a></li>\n            <li><a download data-download-track data-work="adjunct-lecturer-k-007-briefcase" data-language="ko" data-format="epub" data-version="001" href="/assets/downloads/adjunct-lecturer-k-007-briefcase/ko/{epubname}">{epubname}</a></li>\n          </ul>\n          <p class="download-meta">Updated: October 7, 2026 · Version 001</p>\n        </section>\n      </section>'''
    marker='\n    </div>\n\n    {% include footer.html %}'
    if marker not in s: raise RuntimeError('downloads insertion marker missing')
    s=s.replace(marker,block+marker,1)
    dp.write_text(s,encoding='utf-8')

lp=ROOT/'publication-log/index.html'; s=lp.read_text(encoding='utf-8')
needle='<h2>October 7, 2026</h2>'
entry='''\n        <h3>Adjunct Lecturer K’s 007 Briefcase</h3>\n        <ul>\n          <li>Korean short-story collection (<em>시간강사 K의 007 가방</em>) — free PDF and EPUB editions added</li>\n        </ul>\n'''
if 'Korean short-story collection (<em>시간강사 K의 007 가방</em>)' not in s:
    pos=s.find(needle)
    if pos<0: raise RuntimeError('October 7 log section missing')
    insert=pos+len(needle)
    s=s[:insert]+entry+s[insert:]
    lp.write_text(s,encoding='utf-8')

print('PDF',PDF,PDF.stat().st_size,hashlib.sha256(PDF.read_bytes()).hexdigest())
print('EPUB',EPUB,EPUB.stat().st_size,hashlib.sha256(EPUB.read_bytes()).hexdigest())
print('stories',[(x['title'],len(x['items'])) for x in stories])
