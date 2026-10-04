from pathlib import Path
from bs4 import BeautifulSoup
from weasyprint import HTML
import fitz, html, uuid, zipfile, tempfile, shutil, hashlib

R=Path('.')
out=R/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/ja'
out.mkdir(parents=True,exist_ok=True)
pdf=out/'a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.pdf'
epub=out/'a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.epub'

chapters=[]
for i in range(1,10):
    p=R/f'a-dictionary-of-galactic-extinction/ja/part-01/entry-{i:02d}/index.html'
    s=BeautifulSoup(p.read_text(encoding='utf-8'),'lxml')
    title=s.find('h1',class_='entry-title').get_text(' ',strip=True)
    art=s.find('article',class_='prose')
    ul=art.find('ul',recursive=False)
    defs=[li.get_text(' ',strip=True) for li in ul.find_all('li',recursive=False)]
    paras=[]
    for q in art.find_all('p',recursive=False):
        for br in q.find_all('br'):
            br.replace_with('\n')
        paras.append(q.get_text().strip())
    if len(defs)!=3:
        raise RuntimeError(f'entry {i}: expected 3 definitions, got {len(defs)}')
    chapters.append((title,defs,paras))

cp_lines=[
    'Copyright © 2026 Jin-in-Seoul',
    'すべての権利を留保します。',
    '本書の著作権はJin-in-Seoulに帰属します。',
    '著作権者の許可なく、本書の全部または一部を複製、配布、送信、改変、または商業目的で利用することを禁じます。',
    '本デジタル版は無償で配布されています。',
    '無償での配布は、著作権の放棄または譲渡を意味するものではありません。',
    'デジタル初版、2026年',
    'Jin-in-Seoul 発行',
    'https://jin-in-seoul.com'
]

# PDF
css=r"""
@page { size:A4; margin:72pt 72pt 78pt 72pt; @bottom-center { content: "- " counter(page) " -"; font-family:"Noto Serif CJK JP"; font-size:9pt; } }
@page fixed { size:A4; margin:0; @bottom-center { content:none; } }
html,body { margin:0; padding:0; font-family:"Noto Serif CJK JP","Noto Serif JP",serif; color:#111; font-size:11.6pt; }
.fixed { page:fixed; position:relative; width:595.28pt; height:841.89pt; page-break-after:always; }
.cover .edition { position:absolute; left:72pt; top:70pt; font-weight:700; font-size:12pt; }
.cover .title { position:absolute; left:72pt; right:72pt; top:265pt; text-align:center; font-size:23pt; line-height:1.35; }
.cover .part { position:absolute; left:72pt; right:72pt; top:350pt; text-align:center; font-size:14pt; }
.copyright .chead { position:absolute; left:72pt; top:116pt; width:451pt; font-size:13pt; line-height:27pt; }
.copyright .chead p { margin:0; text-indent:0; }
.copyright .cbody { position:absolute; left:72pt; top:258pt; width:451pt; font-size:11.4pt; line-height:25pt; }
.copyright .cbody p { margin:0; text-indent:0; }
.epigraph .ebox { position:absolute; left:95pt; right:80pt; top:250pt; border-left:1.2pt solid #888; padding-left:18pt; font-size:12pt; line-height:24pt; }
.epigraph .src { margin-top:16pt; font-size:10.5pt; color:#555; }
.toc .ttitle { position:absolute; left:72pt; right:72pt; top:145pt; text-align:center; font-size:17pt; }
.toc .tlist { position:absolute; top:225pt; left:50%; width:340pt; transform:translateX(-50%); font-size:12pt; line-height:28pt; }
.partpage .ptitle { position:absolute; left:72pt; right:72pt; top:330pt; text-align:center; font-size:20pt; }
.entry { page-break-before:always; }
.entry-head { margin:0 0 28pt 0; }
.entry-title { font-size:19pt; line-height:1.4; margin:0 0 22pt; font-weight:600; }
.defs { margin:0 0 28pt 1.2em; padding:0; line-height:23pt; }
.defs li { margin:0 0 4pt 0; padding-left:.25em; }
.prose { font-size:11.6pt; line-height:23.5pt; }
.prose p { margin:0; text-indent:1.5em; text-align:justify; }
"""
cover='''<section class="fixed cover"><div class="edition">無料デジタル版</div><div class="title">銀河滅亡辞典</div><div class="part">第1部 — 滅亡の条件</div></section>'''
copyright='''<section class="fixed copyright"><div class="chead"><p>銀河滅亡辞典</p><p>A Dictionary of Galactic Extinction</p><p>第1部 — 滅亡の条件</p></div><div class="cbody">'''+''.join(f'<p>{html.escape(x)}</p>' for x in cp_lines)+'</div></section>'
epigraph='''<section class="fixed epigraph"><div class="ebox"><div>「いつになったら、大きさは重要ではないと分かるんだ？<br/>大切なものだからといって、<br/>とても、とても小さくないとは限らない。」</div><div class="src">— 映画 <em>Men in Black</em> より</div></div></section>'''
toc='''<section class="fixed toc"><div class="ttitle">目次</div><div class="tlist">'''+''.join(f'<div>・{html.escape(t)}</div>' for t,_,_ in chapters)+'</div></section>'
partpage='''<section class="fixed partpage"><div class="ptitle">第1部 — 滅亡の条件</div></section>'''
entries=[]
for title,defs,paras in chapters:
    d=''.join(f'<li>{html.escape(x)}</li>' for x in defs)
    ps=''.join('<p>'+'<br/>'.join(html.escape(z) for z in x.split('\n'))+'</p>' for x in paras)
    entries.append(f'<section class="entry"><div class="entry-head"><div class="entry-title">{html.escape(title)}</div><ul class="defs">{d}</ul></div><div class="prose">{ps}</div></section>')
doc=f'<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>{css}</style></head><body>{cover}{copyright}{epigraph}{toc}{partpage}{"".join(entries)}</body></html>'
HTML(string=doc,base_url=str(R.resolve())).write_pdf(str(pdf))

must=['銀河滅亡辞典','A Dictionary of Galactic Extinction','第1部 — 滅亡の条件','Copyright © 2026 Jin-in-Seoul','本デジタル版は無償で配布されています。','Jin-in-Seoul 発行','1. 光子欠損','5. 維持費','9. 熱的死','それを時間が流れたと呼ぶ存在はいなかった。']
d=fitz.open(pdf)
alltext='\n'.join(p.get_text() for p in d)
for x in must:
    if x not in alltext:
        raise RuntimeError(f'PDF missing text: {x}')
if len(d)!=39:
    raise RuntimeError(f'PDF page count changed: {len(d)}')
if 'Copyright © 2026 Jin-in-Seoul' not in d[1].get_text():
    raise RuntimeError('PDF copyright not on page 2')
if 'A Dictionary of Galactic Extinction' not in d[1].get_text():
    raise RuntimeError('PDF English title missing')
if '目次' not in d[3].get_text():
    raise RuntimeError('PDF TOC not on page 4')
if '第2部 歴史篇' in alltext or '第2部　歴史篇' in alltext:
    raise RuntimeError('PDF stray Part II label')
d.close()

# EPUB
td=Path(tempfile.mkdtemp())
try:
    (td/'META-INF').mkdir()
    (td/'EPUB/Styles').mkdir(parents=True)
    (td/'EPUB/Text').mkdir(parents=True)
    (td/'mimetype').write_text('application/epub+zip',encoding='utf-8')
    (td/'META-INF/container.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',encoding='utf-8')
    ecss='''body{font-family:"Noto Serif CJK JP","Noto Serif JP",serif;line-height:1.75;margin:5%;}h1,h2{text-align:center;font-weight:400;}p{margin:0;text-indent:1.5em;}p.n{text-indent:0;}.c{text-align:center;text-indent:0;}.meta{margin:.2em 0;text-indent:0;}.defs{margin:1.5em 0 2em 1.2em;padding:0;}.defs li{margin:.2em 0;}.part{margin-top:35vh;text-align:center;font-size:1.4em;text-indent:0;}.epigraph{margin:20vh 8% 0 8%;padding-left:1em;border-left:1px solid #888;text-indent:0;}.src{margin-top:1em;text-indent:0;color:#555;}.entry-title{text-align:left;font-size:1.45em;margin:0 0 1em 0;}'''
    (td/'EPUB/Styles/style.css').write_text(ecss,encoding='utf-8')
    def page(title,body):
        return f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" lang="ja"><head><meta charset="utf-8"/><title>{html.escape(title)}</title><link rel="stylesheet" href="../Styles/style.css"/></head><body>{body}</body></html>'
    (td/'EPUB/Text/title.xhtml').write_text(page('銀河滅亡辞典','<p class="n">無料デジタル版</p><h1>銀河滅亡辞典</h1><p class="c">第1部 — 滅亡の条件</p>'),encoding='utf-8')
    cp_body='<p class="n">銀河滅亡辞典</p><p class="n">A Dictionary of Galactic Extinction</p><p class="n">第1部 — 滅亡の条件</p><br/>'+''.join(f'<p class="meta">{html.escape(x)}</p>' for x in cp_lines)
    (td/'EPUB/Text/copyright.xhtml').write_text(page('著作権',cp_body),encoding='utf-8')
    epi='<div class="epigraph">「いつになったら、大きさは重要ではないと分かるんだ？<br/>大切なものだからといって、<br/>とても、とても小さくないとは限らない。」<div class="src">— 映画 <em>Men in Black</em> より</div></div>'
    (td/'EPUB/Text/epigraph.xhtml').write_text(page('引用',epi),encoding='utf-8')
    toc_items=''.join(f'<li><a href="entry-{i:02d}.xhtml">{html.escape(t)}</a></li>' for i,(t,_,_) in enumerate(chapters,1))
    (td/'EPUB/Text/contents.xhtml').write_text(page('目次',f'<h1>目次</h1><ol>{toc_items}</ol>'),encoding='utf-8')
    (td/'EPUB/Text/part-01.xhtml').write_text(page('第1部 — 滅亡の条件','<p class="part">第1部 — 滅亡の条件</p>'),encoding='utf-8')
    for i,(title,defs,paras) in enumerate(chapters,1):
        defs_html='<ul class="defs">'+''.join(f'<li>{html.escape(x)}</li>' for x in defs)+'</ul>'
        ps=''.join('<p>'+'<br/>'.join(html.escape(z) for z in x.split('\n'))+'</p>' for x in paras)
        (td/f'EPUB/Text/entry-{i:02d}.xhtml').write_text(page(title,f'<h1 class="entry-title">{html.escape(title)}</h1>{defs_html}{ps}'),encoding='utf-8')
    uid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'https://jin-in-seoul.com/a-dictionary-of-galactic-extinction/ja/part-01/20261004/001'))
    items=['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>','<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>','<item id="css" href="Styles/style.css" media-type="text/css"/>','<item id="title" href="Text/title.xhtml" media-type="application/xhtml+xml"/>','<item id="copyright" href="Text/copyright.xhtml" media-type="application/xhtml+xml"/>','<item id="epigraph" href="Text/epigraph.xhtml" media-type="application/xhtml+xml"/>','<item id="contents" href="Text/contents.xhtml" media-type="application/xhtml+xml"/>','<item id="part01" href="Text/part-01.xhtml" media-type="application/xhtml+xml"/>']
    spine=['title','copyright','epigraph','contents','part01']
    for i in range(1,10):
        items.append(f'<item id="e{i}" href="Text/entry-{i:02d}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'e{i}')
    opf=f'<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">{uid}</dc:identifier><dc:title>銀河滅亡辞典 — 第1部 滅亡の条件</dc:title><dc:creator>Jin-in-Seoul</dc:creator><dc:language>ja</dc:language><dc:publisher>Jin-in-Seoul</dc:publisher><dc:rights>Copyright © 2026 Jin-in-Seoul. All rights reserved.</dc:rights><dc:date>2026-10-04</dc:date><meta property="dcterms:modified">2026-10-04T11:45:00Z</meta></metadata><manifest>{"".join(items)}</manifest><spine toc="ncx">{"".join(f"<itemref idref=\"{x}\"/>" for x in spine)}</spine></package>'
    (td/'EPUB/package.opf').write_text(opf,encoding='utf-8')
    navs=[('title','銀河滅亡辞典'),('copyright','著作権'),('epigraph','引用'),('contents','目次'),('part-01','第1部 — 滅亡の条件')]+[(f'entry-{i:02d}',t) for i,(t,_,_) in enumerate(chapters,1)]
    nav=''.join(f'<li><a href="Text/{x}.xhtml">{html.escape(y)}</a></li>' for x,y in navs)
    (td/'EPUB/nav.xhtml').write_text(f'<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="ja"><head><title>目次</title></head><body><nav epub:type="toc"><ol>{nav}</ol></nav></body></html>',encoding='utf-8')
    np=''.join(f'<navPoint id="n{i}" playOrder="{i}"><navLabel><text>{html.escape(y)}</text></navLabel><content src="Text/{x}.xhtml"/></navPoint>' for i,(x,y) in enumerate(navs,1))
    (td/'EPUB/toc.ncx').write_text(f'<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="{uid}"/></head><docTitle><text>銀河滅亡辞典 — 第1部 滅亡の条件</text></docTitle><navMap>{np}</navMap></ncx>',encoding='utf-8')
    with zipfile.ZipFile(epub,'w') as z:
        z.write(td/'mimetype','mimetype',compress_type=zipfile.ZIP_STORED)
        for p in td.rglob('*'):
            if p.is_file() and p.name!='mimetype':
                z.write(p,p.relative_to(td).as_posix(),compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(epub,'r') as z:
        if z.namelist()[0]!='mimetype': raise RuntimeError('EPUB mimetype not first')
        if z.getinfo('mimetype').compress_type!=zipfile.ZIP_STORED: raise RuntimeError('EPUB mimetype compressed')
        if z.testzip() is not None: raise RuntimeError('EPUB ZIP integrity failed')
        titlex=z.read('EPUB/Text/title.xhtml').decode('utf-8')
        if '<p class="n">無料デジタル版</p>' not in titlex: raise RuntimeError('EPUB free edition label not left aligned')
        text='\n'.join(z.read(n).decode('utf-8') for n in z.namelist() if n.endswith(('.xhtml','.opf','.ncx')))
        for x in must:
            if x not in text: raise RuntimeError(f'EPUB missing text: {x}')
        if '第2部 歴史篇' in text or '第2部　歴史篇' in text: raise RuntimeError('EPUB stray Part II label')
finally:
    shutil.rmtree(td,ignore_errors=True)

# Downloads page
p=Path('downloads/index.html')
s=p.read_text(encoding='utf-8')
if 'a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.pdf' not in s:
    anchor='''        <section class="download-language" lang="ko">
          <h3>한국어</h3>
          <ul class="download-files">
            <li><a download data-download-track data-work="a-dictionary-of-galactic-extinction" data-part="part-01" data-language="ko" data-format="pdf" data-version="001" href="/assets/downloads/a-dictionary-of-galactic-extinction/part-01/ko/a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.pdf">a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.pdf</a></li>
            <li><a download data-download-track data-work="a-dictionary-of-galactic-extinction" data-part="part-01" data-language="ko" data-format="epub" data-version="001" href="/assets/downloads/a-dictionary-of-galactic-extinction/part-01/ko/a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.epub">a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.epub</a></li>
          </ul>
          <p class="download-meta">Updated: September 29, 2026 · Version 001</p>
        </section>'''
    ja='''

        <section class="download-language" lang="ja">
          <h3>日本語</h3>
          <ul class="download-files">
            <li><a download data-download-track data-work="a-dictionary-of-galactic-extinction" data-part="part-01" data-language="ja" data-format="pdf" data-version="001" href="/assets/downloads/a-dictionary-of-galactic-extinction/part-01/ja/a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.pdf">a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.pdf</a></li>
            <li><a download data-download-track data-work="a-dictionary-of-galactic-extinction" data-part="part-01" data-language="ja" data-format="epub" data-version="001" href="/assets/downloads/a-dictionary-of-galactic-extinction/part-01/ja/a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.epub">a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.epub</a></li>
          </ul>
          <p class="download-meta">Updated: October 4, 2026 · Version 001</p>
        </section>'''
    if anchor not in s: raise RuntimeError('downloads anchor missing')
    p.write_text(s.replace(anchor,anchor+ja),encoding='utf-8')

# Publication log
p=Path('publication-log/index.html')
s=p.read_text(encoding='utf-8')
new='          <li>Part I — free PDF and EPUB editions added in Japanese</li>'
if new not in s:
    anchor='          <li>Japanese edition — Part I, Chapters 5–9 added</li>'
    if anchor not in s: raise RuntimeError('publication log anchor missing')
    p.write_text(s.replace(anchor,anchor+'\n'+new),encoding='utf-8')

# Sitemap
p=Path('sitemap.xml')
s=p.read_text(encoding='utf-8')
pdfurl='https://jin-in-seoul.com/assets/downloads/a-dictionary-of-galactic-extinction/part-01/ja/a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.pdf'
epuburl='https://jin-in-seoul.com/assets/downloads/a-dictionary-of-galactic-extinction/part-01/ja/a-dictionary-of-galactic-extinction-part-01-ja-20261004-ver-001.epub'
if pdfurl not in s:
    anchor='''  <url>
    <loc>https://jin-in-seoul.com/a-dictionary-of-galactic-extinction/ja/part-01/entry-09/</loc>
  </url>'''
    add=anchor+f'\n  <url>\n    <loc>{pdfurl}</loc>\n  </url>\n  <url>\n    <loc>{epuburl}</loc>\n  </url>'
    if anchor not in s: raise RuntimeError('sitemap anchor missing')
    p.write_text(s.replace(anchor,add),encoding='utf-8')

# Site validation
d=Path('downloads/index.html').read_text(encoding='utf-8')
l=Path('publication-log/index.html').read_text(encoding='utf-8')
sm=Path('sitemap.xml').read_text(encoding='utf-8')
pdfn=pdf.name
epubn=epub.name
assert d.count(pdfn)==2
assert d.count(epubn)==2
assert d.count('data-part="part-01" data-language="ja" data-format="pdf" data-version="001"')==1
assert d.count('data-part="part-01" data-language="ja" data-format="epub" data-version="001"')==1
assert l.count('Part I — free PDF and EPUB editions added in Japanese')==1
assert sm.count('/part-01/ja/'+pdfn)==1
assert sm.count('/part-01/ja/'+epubn)==1

print('PDF pages: 39')
print('PDF sha256:',hashlib.sha256(pdf.read_bytes()).hexdigest())
print('EPUB sha256:',hashlib.sha256(epub.read_bytes()).hexdigest())
print('PDF bytes:',pdf.stat().st_size)
print('EPUB bytes:',epub.stat().st_size)
print('All validations passed')
