from pathlib import Path
import re, html, tempfile, shutil, zipfile, os
from bs4 import BeautifulSoup
from weasyprint import HTML

R=Path('.')
OUT=R/'assets/downloads/sweater/ja'
PDF=OUT/'sweater-ja-20261003-ver-001.pdf'
EPUB=OUT/'sweater-ja-20261003-ver-001.epub'

date_re=re.compile(r'^\\s*\\d{1,2}月\\d{1,2}日(?:\\s|　)')
chapters=[]
for i in range(1,13):
    s=BeautifulSoup((R/f'sweater/ja/chapter-{i:02d}/index.html').read_text(encoding='utf-8'),'lxml')
    title=s.find('h1').get_text(' ',strip=True)
    sec=s.find('section',class_='prose')
    blocks=[]
    for p in sec.find_all(['p','blockquote'],recursive=False):
        for br in p.find_all('br'): br.replace_with('\\n')
        t=p.get_text().strip()
        if t: blocks.append(t)
    chapters.append((title,blocks))

css=r'''
@page { size: A4; margin: 72pt; }
@page fixed { size: A4; margin: 0; }
html,body { margin:0; padding:0; font-family:'JinJP',serif; font-size:12pt; color:#111; }
.fixed { page: fixed; position:relative; width:595.28pt; height:841.89pt; page-break-after:always; }
.cover .edition { position:absolute; left:72pt; top:70pt; font-weight:700; line-height:16pt; }
.cover .title { position:absolute; left:72pt; right:72pt; top:278pt; text-align:center; font-size:20pt; font-weight:400; line-height:24pt; }
.cover .genre { position:absolute; left:72pt; right:72pt; top:508pt; text-align:center; font-size:12pt; font-weight:400; line-height:16pt; }

.copyright .ctitle { position:absolute; left:72pt; top:222pt; font-size:16pt; line-height:20pt; }
.copyright .cbody { position:absolute; left:72pt; top:279pt; width:451pt; font-size:12pt; line-height:25.9pt; }
.copyright .cbody p { margin:0; padding:0; text-indent:0; }

.toc .ttitle { position:absolute; left:72pt; right:72pt; top:160pt; text-align:center; font-size:16pt; line-height:20pt; }
.toc .tlist { position:absolute; top:263pt; left:50%; width:290pt; transform:translateX(-50%); font-size:12pt; line-height:25.9pt; }
.toc .tlist div { margin:0; }

.chapter { page-break-before:always; }
.chapter:first-of-type { page-break-before:auto; }
.chapter-head { height:193pt; position:relative; text-align:center; }
.chapter-num { position:absolute; top:0; left:0; right:0; line-height:16pt; }
.chapter-month { position:absolute; top:55pt; left:0; right:0; line-height:16pt; }
.chapter-sub { position:absolute; top:83pt; left:0; right:0; line-height:16pt; }

.prose { font-size:12pt; line-height:27.6pt; }
.prose p { margin:0; padding:0; text-indent:36pt; }
.prose p.noindent { text-indent:0; }
.prose p.date { text-indent:0; font-family:'JinJP',serif; font-weight:700; margin-top:0; margin-bottom:27.6pt; }
'''

cover='''<section class="fixed cover">
<div class="edition">無料デジタル版</div>
<div class="title">セーター</div>
<div class="genre">文芸小説</div>
</section>'''

cp_lines=[
'すべての権利を留保します。',
'本書の著作権はJin-in-Seoulに帰属します。',
'著作権者の許可なく、本書の全部または一部を複製、配布、送信、改変、または商業目的で利用することを禁じます。',
'本デジタル版は無償で配布されています。',
'無償での配布は、著作権の放棄または譲渡を意味するものではありません。',
'デジタル初版、2026年',
'Jin-in-Seoul 発行',
'https://jin-in-seoul.com'
]
copyright='''<section class="fixed copyright"><div class="ctitle">セーター</div><div class="cbody">
<p>Copyright © 2026 Jin-in-Seoul</p>''' + ''.join('<p>'+html.escape(x)+'</p>' for x in cp_lines) + '</div></section>'

toc_items=[]
for t,_ in chapters:
    toc_items.append('<div>・'+html.escape(t.replace('　',' — ',1))+'</div>')
toc='<section class="fixed toc"><div class="ttitle">目次</div><div class="tlist">'+''.join(toc_items)+'</div></section>'

chapter_html=[]
for ci,(t,blocks) in enumerate(chapters,1):
    ps=t.split('　',1)
    head=f'''<div class="chapter-head"><div class="chapter-num">第{ci}章</div><div class="chapter-month">{html.escape(ps[0])}</div>'''
    if len(ps)>1:
        head+=f'<div class="chapter-sub">{html.escape(ps[1])}</div>'
    head+='</div>'
    body=[]
    after_date=False
    for x in blocks:
        is_date=bool(date_re.match(x))
        noindent=after_date or bool(re.match(r'^(?:\d+\.|―|「|『|\(|（)',x))
        cls='date' if is_date else ('noindent' if noindent else '')
        txt='<br/>'.join(html.escape(z) for z in x.split('\\n'))
        body.append(f'<p class="{cls}">{txt}</p>')
        after_date=is_date
    chapter_html.append(f'<section class="chapter">{head}<div class="prose">{"".join(body)}</div></section>')

document=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{css}</style></head><body>{cover}{copyright}{toc}{"".join(chapter_html)}</body></html>'''
HTML(string=document,base_url=str(R.resolve())).write_pdf(str(PDF))

# EPUB: keep existing content/navigation, replace typography/layout CSS.
td=Path(tempfile.mkdtemp())
try:
    with zipfile.ZipFile(EPUB,'r') as z: z.extractall(td)
    style=td/'EPUB/Styles/style.css'
    epub_css='''body{font-family:"Noto Serif CJK JP","Noto Serif JP",serif;line-height:1.75;margin:5%}
h1,h2{text-align:center;font-weight:400}
p{margin:0 0 .65em;text-indent:1.5em}
p.date{font-family:"Noto Sans CJK JP","Noto Sans JP",sans-serif;font-weight:700;text-indent:0;margin:1.3em 0 2.75em 0}
p.n{text-indent:0}.c{text-align:center;text-indent:0}
'''
    style.write_text(epub_css,encoding='utf-8')
    tmp=str(EPUB)+'.tmp'
    with zipfile.ZipFile(tmp,'w') as z:
        z.write(td/'mimetype','mimetype',compress_type=zipfile.ZIP_STORED)
        for p in td.rglob('*'):
            if p.is_file() and p.name!='mimetype':
                z.write(p,p.relative_to(td).as_posix(),compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(tmp) as z:
        if z.testzip() is not None: raise RuntimeError('EPUB ZIP verification failed')
    os.replace(tmp,EPUB)
finally:
    shutil.rmtree(td,ignore_errors=True)

print('rebuilt',PDF,EPUB)
