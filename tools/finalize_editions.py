import os,re,html,uuid,zipfile,tempfile,shutil
from pathlib import Path
from bs4 import BeautifulSoup
import fitz
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

R=Path('.')
date_re=re.compile(r'^\s*\d{1,2}月\d{1,2}日(?:\s|　)')
chapters=[]
for i in range(1,13):
    s=BeautifulSoup((R/f'sweater/ja/chapter-{i:02d}/index.html').read_text(encoding='utf8'),'lxml')
    title=s.find('h1').get_text(' ',strip=True)
    sec=s.find('section',class_='prose')
    blocks=[]
    for p in sec.find_all(['p','blockquote'],recursive=False):
        for br in p.find_all('br'):
            br.replace_with('\n')
        t=p.get_text().strip()
        if t:
            blocks.append(t)
    chapters.append((title,blocks))

# Japanese PDF
font='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
bold='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
pdfmetrics.registerFont(TTFont('JP',font,subfontIndex=0))
pdfmetrics.registerFont(TTFont('JPB',bold,subfontIndex=0))
outdir=R/'assets/downloads/sweater/ja'
outdir.mkdir(parents=True,exist_ok=True)
pdfp=outdir/'sweater-ja-20261003-ver-001.pdf'
D=SimpleDocTemplate(str(pdfp),pagesize=A4,leftMargin=inch,rightMargin=inch,topMargin=inch,bottomMargin=inch)
base=ParagraphStyle('base',fontName='HeiseiMin-W3',fontSize=12,leading=20,spaceAfter=0)
center=ParagraphStyle('center',parent=base,alignment=TA_CENTER)
date=ParagraphStyle('date',parent=base,fontName='HeiseiKakuGo-W5',spaceBefore=12,spaceAfter=14,firstLineIndent=0)
body=ParagraphStyle('body',parent=base,firstLineIndent=36)
noindent=ParagraphStyle('noindent',parent=base,firstLineIndent=0)
story=[Spacer(1,20),Paragraph('無料デジタル版',center),Spacer(1,30),Paragraph('<font size="22">セーター</font>',center),Spacer(1,30),Paragraph('文芸小説',center),PageBreak()]
cp=['セーター','Copyright © 2026 Jin-in-Seoul','すべての権利を留保します。','本書の著作権はJin-in-Seoulに帰属します。','著作権者の許可なく、本書の全部または一部を複製、配布、送信、改変、または商業目的で利用することを禁じます。','本デジタル版は無償で配布されています。','無償での配布は、著作権の放棄または譲渡を意味するものではありません。','デジタル初版、2026年','Jin-in-Seoul 発行','https://jin-in-seoul.com']
story += [Paragraph(html.escape(x),noindent) for x in cp]
story += [PageBreak(),Paragraph('<font size="16">目次</font>',center),Spacer(1,16)]
for t,_ in chapters:
    story += [Paragraph('•　'+html.escape(t.replace('　',' — ',1)),noindent),Spacer(1,4)]
story += [PageBreak()]
for ci,(t,blocks) in enumerate(chapters,1):
    if ci>1:
        story.append(PageBreak())
    parts=t.split('　',1)
    story += [Paragraph(f'第{ci}章',center),Spacer(1,10),Paragraph(html.escape(parts[0]),center)]
    if len(parts)>1:
        story += [Spacer(1,6),Paragraph(html.escape(parts[1]),center)]
    story += [Spacer(1,28)]
    after=True
    for x in blocks:
        esc='<br/>'.join(html.escape(z) for z in x.split('\n'))
        isd=bool(date_re.match(x))
        st=date if isd else (noindent if after or re.match(r'^(?:\d+\.|―|「|『|\(|（)',x) else body)
        story.append(Paragraph(esc,st))
        after=isd
D.build(story)
chk=fitz.open(pdfp)
dc=sum(1 for p in chk for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) if date_re.match(''.join(s['text'] for s in l.get('spans',[])).strip()))
chk.close()
if dc<360:
    raise RuntimeError(f'Japanese date count {dc}')

# Japanese EPUB
ep=outdir/'sweater-ja-20261003-ver-001.epub'
td=Path(tempfile.mkdtemp())
try:
    (td/'META-INF').mkdir()
    (td/'EPUB/Styles').mkdir(parents=True)
    (td/'EPUB/Text').mkdir(parents=True)
    (td/'mimetype').write_text('application/epub+zip')
    (td/'META-INF/container.xml').write_text('<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
    css='body{font-family:serif;line-height:1.75;margin:5%}h1,h2{text-align:center;font-weight:normal}p{margin:0 0 .65em;text-indent:1.5em}p.date{font-weight:bold;text-indent:0;margin:1.3em 0}p.n{text-indent:0}.c{text-align:center;text-indent:0}'
    (td/'EPUB/Styles/style.css').write_text(css)
    def page(title,b):
        return f'<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja"><head><meta charset="utf-8"/><title>{html.escape(title)}</title><link rel="stylesheet" href="../Styles/style.css"/></head><body>{b}</body></html>'
    (td/'EPUB/Text/title.xhtml').write_text(page('セーター','<p class="c">無料デジタル版</p><h1>セーター</h1><p class="c">文芸小説</p>'))
    cbody='<h1>セーター</h1>'+''.join(f'<p class="n">{html.escape(x)}</p>' for x in cp)
    (td/'EPUB/Text/copyright.xhtml').write_text(page('著作権',cbody))
    toc=''.join(f'<li><a href="chapter-{i:02d}.xhtml">{html.escape(t.replace("　"," — ",1))}</a></li>' for i,(t,_) in enumerate(chapters,1))
    (td/'EPUB/Text/contents.xhtml').write_text(page('目次',f'<h1>目次</h1><ul>{toc}</ul>'))
    for i,(t,blocks) in enumerate(chapters,1):
        ps=t.split('　',1)
        b=f'<p class="c">第{i}章</p><h1>{html.escape(ps[0])}</h1>'+(f'<h2>{html.escape(ps[1])}</h2>' if len(ps)>1 else '')
        after=True
        for x in blocks:
            isd=bool(date_re.match(x))
            cls='date' if isd else ('n' if after or re.match(r'^(?:\d+\.|―|「|『|\(|（)',x) else '')
            b += f'<p class="{cls}">'+'<br/>'.join(html.escape(z) for z in x.split('\n'))+'</p>'
            after=isd
        (td/f'EPUB/Text/chapter-{i:02d}.xhtml').write_text(page(t,b))
    uid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,'https://jin-in-seoul.com/sweater/ja/20261003/001'))
    items=['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>','<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>','<item id="css" href="Styles/style.css" media-type="text/css"/>','<item id="title" href="Text/title.xhtml" media-type="application/xhtml+xml"/>','<item id="copyright" href="Text/copyright.xhtml" media-type="application/xhtml+xml"/>','<item id="contents" href="Text/contents.xhtml" media-type="application/xhtml+xml"/>']
    spine=['title','copyright','contents']
    for i in range(1,13):
        items.append(f'<item id="c{i}" href="Text/chapter-{i:02d}.xhtml" media-type="application/xhtml+xml"/>')
        spine.append(f'c{i}')
    refs=''.join('<itemref idref="'+x+'"/>' for x in spine)
    opf=f'<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">{uid}</dc:identifier><dc:title>セーター</dc:title><dc:creator>Jin-in-Seoul</dc:creator><dc:language>ja</dc:language><dc:publisher>Jin-in-Seoul</dc:publisher><dc:rights>Copyright © 2026 Jin-in-Seoul. All rights reserved.</dc:rights><dc:date>2026-10-03</dc:date><meta property="dcterms:modified">2026-10-03T05:00:00Z</meta></metadata><manifest>{"".join(items)}</manifest><spine toc="ncx">{refs}</spine></package>'
    (td/'EPUB/package.opf').write_text(opf)
    navs=[('title','セーター'),('copyright','著作権'),('contents','目次')]+[(f'chapter-{i:02d}',t.replace('　',' — ',1)) for i,(t,_) in enumerate(chapters,1)]
    nav=''.join(f'<li><a href="Text/{x}.xhtml">{html.escape(y)}</a></li>' for x,y in navs)
    (td/'EPUB/nav.xhtml').write_text(f'<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><body><nav epub:type="toc"><ol>{nav}</ol></nav></body></html>')
    np=''.join(f'<navPoint id="n{i}" playOrder="{i}"><navLabel><text>{html.escape(y)}</text></navLabel><content src="Text/{x}.xhtml"/></navPoint>' for i,(x,y) in enumerate(navs,1))
    (td/'EPUB/toc.ncx').write_text(f'<?xml version="1.0"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="{uid}"/></head><docTitle><text>セーター</text></docTitle><navMap>{np}</navMap></ncx>')
    with zipfile.ZipFile(ep,'w') as z:
        z.write(td/'mimetype','mimetype',compress_type=zipfile.ZIP_STORED)
        for p in td.rglob('*'):
            if p.is_file() and p.name!='mimetype':
                z.write(p,p.relative_to(td).as_posix(),compress_type=zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(ep) as z:
        if z.testzip():
            raise RuntimeError('EPUB invalid')
finally:
    shutil.rmtree(td,ignore_errors=True)

# Galactic PDF and EPUB
for lang in ('en','ko'):
    p=R/f'assets/downloads/a-dictionary-of-galactic-extinction/part-01/{lang}/a-dictionary-of-galactic-extinction-part-01-{lang}-20260929-ver-001.pdf'
    d=fitz.open(p)
    last=len(d)-1
    if 'Copyright © 2026 Jin-in-Seoul' not in d[last].get_text():
        raise RuntimeError(f'copyright end page missing {lang}')
    d.select([0,last]+list(range(1,last)))
    if lang=='ko':
        for i,pg in enumerate(d,1):
            hits=[]
            for n in range(1,len(d)+2):
                hits += pg.search_for(f'- {n} -')
            if hits:
                r=hits[0]
                for h in hits:
                    pg.add_redact_annot(h,fill=(1,1,1))
                pg.apply_redactions()
                pg.insert_text((r.x0,r.y1-2),f'- {i} -',fontsize=10,fontname='helv')
    tmp=str(p)+'.tmp'
    d.save(tmp,garbage=4,deflate=True)
    d.close()
    os.replace(tmp,p)
    q=fitz.open(p)
    if 'Copyright © 2026 Jin-in-Seoul' not in q[1].get_text() or 'Copyright © 2026 Jin-in-Seoul' in q[-1].get_text():
        raise RuntimeError(f'PDF reorder failed {lang}')
    q.close()

    e=R/f'assets/downloads/a-dictionary-of-galactic-extinction/part-01/{lang}/a-dictionary-of-galactic-extinction-part-01-{lang}-20260929-ver-001.epub'
    td=Path(tempfile.mkdtemp())
    try:
        with zipfile.ZipFile(e) as z:
            z.extractall(td)
        op=td/'EPUB/package.opf'
        s=op.read_text()
        s=s.replace('<itemref idref="copyright"/>','')
        s=s.replace('<spine toc="ncx"><itemref idref="title"/>','<spine toc="ncx"><itemref idref="title"/><itemref idref="copyright"/>')
        op.write_text(s)
        label='저작권' if lang=='ko' else 'Copyright'
        navp=td/'EPUB/nav.xhtml'
        ns=navp.read_text()
        ns=re.sub(r'<li><a href="Text/copyright.xhtml">.*?</a></li>','',ns)
        ns=ns.replace('</a></li>',f'</a></li><li><a href="Text/copyright.xhtml">{label}</a></li>',1)
        navp.write_text(ns)
        nc=td/'EPUB/toc.ncx'
        cs=nc.read_text()
        cs=re.sub(r'<navPoint id="copyright".*?</navPoint>','',cs,flags=re.S)
        pos=cs.find('</navPoint>')+len('</navPoint>')
        cs=cs[:pos]+f'<navPoint id="copyright" playOrder="2"><navLabel><text>{label}</text></navLabel><content src="Text/copyright.xhtml"/></navPoint>'+cs[pos:]
        k=[0]
        def renum(m):
            k[0]+=1
            return f'playOrder="{k[0]}"'
        cs=re.sub(r'playOrder="\d+"',renum,cs)
        nc.write_text(cs)
        tmp=str(e)+'.tmp'
        with zipfile.ZipFile(tmp,'w') as z:
            z.write(td/'mimetype','mimetype',compress_type=zipfile.ZIP_STORED)
            for x in td.rglob('*'):
                if x.is_file() and x.name!='mimetype':
                    z.write(x,x.relative_to(td).as_posix(),compress_type=zipfile.ZIP_DEFLATED)
        os.replace(tmp,e)
    finally:
        shutil.rmtree(td,ignore_errors=True)

# Downloads page
dp=R/'downloads/index.html'
s=dp.read_text()
if 'data-language="ja"' not in s:
    fr=s.index('<section class="download-language" lang="fr">')
    end=s.index('</section>',fr)+len('</section>')
    ja='''

        <section class="download-language" lang="ja">
          <h3>日本語 — <em>セーター</em></h3>
          <ul class="download-files">
            <li><a download data-download-track data-work="sweater" data-language="ja" data-format="pdf" data-version="001" href="/assets/downloads/sweater/ja/sweater-ja-20261003-ver-001.pdf">sweater-ja-20261003-ver-001.pdf</a></li>
            <li><a download data-download-track data-work="sweater" data-language="ja" data-format="epub" data-version="001" href="/assets/downloads/sweater/ja/sweater-ja-20261003-ver-001.epub">sweater-ja-20261003-ver-001.epub</a></li>
          </ul>
          <p class="download-meta">Updated: October 3, 2026 · Version 001</p>
        </section>'''
    dp.write_text(s[:end]+ja+s[end:])
