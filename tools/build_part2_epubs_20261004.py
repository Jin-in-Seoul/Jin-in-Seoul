from pathlib import Path
from bs4 import BeautifulSoup
from lxml import etree
import zipfile, shutil, uuid, re, html

ROOT=Path.cwd()
OUTROOT=ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-02'
DATE='20261004'
PART_LABEL={'en':'Part II — History','ko':'제2부 — 역사편'}
BOOK={'en':'A Dictionary of Galactic Extinction','ko':'은하 멸망 사전'}
TITLE_META={'en':'A Dictionary of Galactic Extinction — Part II — History','ko':'은하 멸망 사전 — 제2부 — 역사편'}

def read_site_entry(lang,n):
    p=ROOT/f'a-dictionary-of-galactic-extinction/{lang}/part-02/entry-{n:02d}/index.html'
    raw=p.read_text(encoding='utf-8')
    soup=BeautifulSoup(raw,'html.parser')
    title=soup.select_one('h1.entry-title')
    part=soup.select_one('p.deck.part-label')
    article=soup.select_one('article.prose')
    if not (title and article):
        raise RuntimeError(f'parse failure: {p}')
    title_txt=title.get_text(' ',strip=True)
    part_txt=part.get_text(' ',strip=True) if part else PART_LABEL[lang]
    inner=''.join(str(x) for x in article.contents).strip()
    inner=re.sub(r'<br\s*>','<br/>',inner,flags=re.I)
    paras=[x.get_text(' ',strip=True) for x in article.find_all(['p','li'],recursive=True)]
    return title_txt,part_txt,inner,paras

def xhtml(lang,title,body):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{lang}" lang="{lang}">
<head>
<meta charset="utf-8"/>
<title>{html.escape(title)}</title>
<link rel="stylesheet" type="text/css" href="../Styles/style.css"/>
</head>
<body class="">
{body}
</body>
</html>
'''

def build_title(lang):
    if lang=='en':
        body='''<section class="title-page">
<p class="edition">Free Digital Edition</p>
<p class="edition-note">This work consists of five parts in total, and this edition contains Part II only.</p>
<h1 class="book-title">A Dictionary of Galactic Extinction</h1>
<p class="book-subtitle">Part II — History</p>
</section>'''
    else:
        body='''<section class="title-page">
<p class="edition">무료 디지털판</p>
<p class="edition-note">이 작품은 총 5부로 이루어져 있으며, 이 판본에는 제2부만 수록되어 있습니다.</p>
<h1 class="book-title">은하 멸망 사전</h1>
<p>A Dictionary of Galactic Extinction</p>
<p class="book-subtitle">제2부 — 역사편</p>
</section>'''
    return xhtml(lang,BOOK[lang],body)

def build_copyright(lang):
    if lang=='en':
        body='''<section class="copyright">
<p class="book-title">A Dictionary of Galactic Extinction</p>
<p class="book-subtitle">Part II — History</p>
<p>Copyright © 2026 Jin-in-Seoul<br/>All rights reserved.</p>
<p>The copyright in this book belongs to Jin-in-Seoul.<br/>
No part of this book may be reproduced, distributed, transmitted, modified, or used commercially without the permission of the copyright holder.</p>
<p>This digital edition is distributed free of charge.<br/>Free distribution does not waive or transfer any copyright.</p>
<p>First digital edition, 2026<br/>Published by Jin-in-Seoul<br/>https://jin-in-seoul.com</p>
</section>'''
        title='Copyright'
    else:
        body='''<section class="copyright">
<p class="book-title">은하 멸망 사전</p>
<p>A Dictionary of Galactic Extinction</p>
<p class="book-subtitle">제2부 — 역사편</p>
<p>Copyright © 2026 Jin-in-Seoul<br/>All rights reserved.</p>
<p>이 책의 저작권은 Jin-in-Seoul에게 있습니다.<br/>
저작권자의 허락 없이 이 책의 전부 또는 일부를 복제, 배포, 전송, 변형하거나 상업적으로 이용할 수 없습니다.</p>
<p>First digital edition, 2026<br/>Jin-in-Seoul 발행<br/>https://jin-in-seoul.com</p>
<p class="free-note">이 디지털 판본은 무료로 배포됩니다.<br/>무료 배포는 저작권의 포기 또는 양도를 의미하지 않습니다.</p>
</section>'''
        title='저작권'
    return xhtml(lang,title,body)

def transform_contents(base_text,lang):
    soup=BeautifulSoup(base_text,'html.parser')
    sec=soup.select_one('section.toc')
    if not sec: raise RuntimeError('toc section missing')
    found=False
    for h2 in sec.find_all('h2'):
        ol=h2.find_next_sibling('ol')
        if not ol: continue
        txt=h2.get_text(' ',strip=True)
        is_part2=(txt==PART_LABEL[lang])
        if is_part2: found=True
        for i,li in enumerate(ol.find_all('li',recursive=False),1):
            label=li.get_text(' ',strip=True)
            li.clear()
            if is_part2:
                a=soup.new_tag('a',href=f'entry-{i:02d}.xhtml')
                a.string=label
                li.append(a)
            else:
                sp=soup.new_tag('span')
                sp['class']='unlinked'
                sp.string=label
                li.append(sp)
    if not found: raise RuntimeError('Part II not found in contents')
    title='Contents' if lang=='en' else '목차'
    return xhtml(lang,title,str(sec))

def build_nav(lang,base_text,titles):
    soup=BeautifulSoup(base_text,'html.parser')
    nav=soup.find('nav')
    if not nav: raise RuntimeError('nav missing')
    # Replace every entry link/span according to target part.
    for li in nav.find_all('li'):
        span=li.find('span',recursive=False)
        a=li.find('a',recursive=False)
        label=(span or a).get_text(' ',strip=True) if (span or a) else ''
        if label==PART_LABEL[lang]:
            sub=li.find('ol',recursive=False)
            if not sub: continue
            sub.clear()
            for i,t in enumerate(titles,1):
                nli=soup.new_tag('li')
                na=soup.new_tag('a',href=f'Text/entry-{i:02d}.xhtml')
                na.string=t
                nli.append(na); sub.append(nli)
        elif (lang=='en' and label.startswith('Part I')) or (lang=='ko' and label.startswith('제1부')):
            sub=li.find('ol',recursive=False)
            if sub:
                for cli in sub.find_all('li',recursive=False):
                    old=cli.get_text(' ',strip=True); cli.clear()
                    sp2=soup.new_tag('span'); sp2.string=old; cli.append(sp2)
    # copyright text remains valid.
    return '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'+str(soup.html)

def build_ncx(lang,titles,uid):
    ep='Epigraph' if lang=='en' else '제사'
    ct='Contents' if lang=='en' else '목차'
    cr='Copyright' if lang=='en' else '저작권'
    pts=[('title',BOOK[lang],'Text/title.xhtml'),('epigraph',ep,'Text/epigraph.xhtml'),('contents',ct,'Text/contents.xhtml')]
    pts += [(f'entry-{i:02d}',t,f'Text/entry-{i:02d}.xhtml') for i,t in enumerate(titles,1)]
    pts.append(('copyright',cr,'Text/copyright.xhtml'))
    nav=''.join(f'<navPoint id="{pid}" playOrder="{i}"><navLabel><text>{html.escape(label)}</text></navLabel><content src="{src}"/></navPoint>' for i,(pid,label,src) in enumerate(pts,1))
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head>
<meta name="dtb:uid" content="{uid}"/><meta name="dtb:depth" content="2"/>
<meta name="dtb:totalPageCount" content="0"/><meta name="dtb:maxPageNumber" content="0"/>
</head><docTitle><text>{html.escape(BOOK[lang])}</text></docTitle><navMap>{nav}</navMap></ncx>'''

def build_opf(lang,uid):
    items=''.join(f'<item id="entry{i:02d}" href="Text/entry-{i:02d}.xhtml" media-type="application/xhtml+xml"/>' for i in range(1,17))
    refs=''.join(f'<itemref idref="entry{i:02d}"/>' for i in range(1,17))
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{lang}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{uid}</dc:identifier>
<dc:title>{html.escape(TITLE_META[lang])}</dc:title>
<dc:creator>Jin-in-Seoul</dc:creator><dc:language>{lang}</dc:language><dc:publisher>Jin-in-Seoul</dc:publisher>
<dc:rights>Copyright © 2026 Jin-in-Seoul. All rights reserved.</dc:rights><dc:date>2026-10-04</dc:date>
<meta property="dcterms:modified">2026-10-04T03:00:00Z</meta>
</metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/><item id="css" href="Styles/style.css" media-type="text/css"/><item id="title" href="Text/title.xhtml" media-type="application/xhtml+xml"/><item id="epigraph" href="Text/epigraph.xhtml" media-type="application/xhtml+xml"/><item id="contents" href="Text/contents.xhtml" media-type="application/xhtml+xml"/>{items}<item id="copyright" href="Text/copyright.xhtml" media-type="application/xhtml+xml"/></manifest><spine toc="ncx"><itemref idref="title"/><itemref idref="epigraph"/><itemref idref="contents"/>{refs}<itemref idref="copyright"/></spine></package>'''

def normalize_text(s):
    return re.sub(r'\s+',' ',s).strip()

def build(lang):
    base=ROOT/f'assets/downloads/a-dictionary-of-galactic-extinction/part-01/{lang}/a-dictionary-of-galactic-extinction-part-01-{lang}-20260929-ver-001.epub'
    outdir=OUTROOT/lang; outdir.mkdir(parents=True,exist_ok=True)
    out=outdir/f'a-dictionary-of-galactic-extinction-part-02-{lang}-20261004-ver-001.epub'
    tmp=ROOT/f'_tmp_epub_{lang}'
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir()
    with zipfile.ZipFile(base) as z: z.extractall(tmp)

    # Remove Part I body files, keep structural files and styling.
    textdir=tmp/'EPUB/Text'
    for p in textdir.glob('entry-*.xhtml'): p.unlink()

    entries=[read_site_entry(lang,i) for i in range(1,17)]
    titles=[e[0] for e in entries]
    assert all(e[1]==PART_LABEL[lang] for e in entries), [(i+1,e[1]) for i,e in enumerate(entries) if e[1]!=PART_LABEL[lang]]

    (textdir/'title.xhtml').write_text(build_title(lang),encoding='utf-8')
    (textdir/'copyright.xhtml').write_text(build_copyright(lang),encoding='utf-8')
    base_contents=(tmp/'EPUB/Text/contents.xhtml').read_text(encoding='utf-8')
    (textdir/'contents.xhtml').write_text(transform_contents(base_contents,lang),encoding='utf-8')

    for i,(title,part,inner,paras) in enumerate(entries,1):
        body=f'<section class="entry"><p class="part-label">{html.escape(part)}</p><h1>{html.escape(title)}</h1><article>\n{inner}\n</article></section>'
        (textdir/f'entry-{i:02d}.xhtml').write_text(xhtml(lang,title,body),encoding='utf-8')

    uid='urn:uuid:'+str(uuid.uuid5(uuid.NAMESPACE_URL,f'https://jin-in-seoul.com/a-dictionary-of-galactic-extinction/part-02/{lang}/2026-10-04'))
    base_nav=(tmp/'EPUB/nav.xhtml').read_text(encoding='utf-8')
    (tmp/'EPUB/nav.xhtml').write_text(build_nav(lang,base_nav,titles),encoding='utf-8')
    (tmp/'EPUB/toc.ncx').write_text(build_ncx(lang,titles,uid),encoding='utf-8')
    (tmp/'EPUB/package.opf').write_text(build_opf(lang,uid),encoding='utf-8')

    # XML/XHTML parse validation.
    for p in list((tmp/'EPUB/Text').glob('*.xhtml'))+[tmp/'EPUB/nav.xhtml',tmp/'EPUB/package.opf',tmp/'EPUB/toc.ncx',tmp/'META-INF/container.xml']:
        etree.parse(str(p))

    # Source-vs-EPUB exact paragraph/list-item text validation.
    for i,e in enumerate(entries,1):
        src_paras=[normalize_text(x) for x in e[3]]
        ep=BeautifulSoup((textdir/f'entry-{i:02d}.xhtml').read_text(encoding='utf-8'),'html.parser')
        art=ep.find('article')
        got=[normalize_text(x.get_text(' ',strip=True)) for x in art.find_all(['p','li'],recursive=True)]
        assert got==src_paras, (lang,i,len(src_paras),len(got))
        assert ep.find('h1').get_text(' ',strip=True)==e[0]
        assert ep.select_one('.part-label').get_text(' ',strip=True)==PART_LABEL[lang]

    # TOC/link/spine validations.
    nav=BeautifulSoup((tmp/'EPUB/nav.xhtml').read_text(encoding='utf-8'),'html.parser')
    nav_links=[a.get('href') for a in nav.find_all('a') if (a.get('href') or '').startswith('Text/entry-')]
    assert nav_links==[f'Text/entry-{i:02d}.xhtml' for i in range(1,17)], nav_links
    cont=BeautifulSoup((textdir/'contents.xhtml').read_text(encoding='utf-8'),'html.parser')
    cont_links=[a.get('href') for a in cont.find_all('a') if (a.get('href') or '').startswith('entry-')]
    assert cont_links==[f'entry-{i:02d}.xhtml' for i in range(1,17)], cont_links
    opf=(tmp/'EPUB/package.opf').read_text(encoding='utf-8')
    for i in range(1,17):
        assert f'idref="entry{i:02d}"' in opf
    assert 'Part I — Conditions of Extinction' not in (textdir/'copyright.xhtml').read_text(encoding='utf-8')
    assert '제1부 — 멸망의 조건' not in (textdir/'copyright.xhtml').read_text(encoding='utf-8')
    if lang=='en':
        assert 'Published by Jin-in-Seoul' in (textdir/'copyright.xhtml').read_text(encoding='utf-8')
        assert 'Published independently' not in (textdir/'copyright.xhtml').read_text(encoding='utf-8')
    else:
        assert 'Jin-in-Seoul 발행' in (textdir/'copyright.xhtml').read_text(encoding='utf-8')
        assert 'Published independently' not in (textdir/'copyright.xhtml').read_text(encoding='utf-8')

    # Pack: mimetype first and uncompressed.
    if out.exists(): out.unlink()
    with zipfile.ZipFile(out,'w') as z:
        z.write(tmp/'mimetype','mimetype',compress_type=zipfile.ZIP_STORED)
        for p in sorted(tmp.rglob('*')):
            if p.is_file() and p.name!='mimetype':
                z.write(p,p.relative_to(tmp).as_posix(),compress_type=zipfile.ZIP_DEFLATED)

    with zipfile.ZipFile(out) as z:
        assert z.namelist()[0]=='mimetype'
        assert z.getinfo('mimetype').compress_type==zipfile.ZIP_STORED
        assert z.read('mimetype')==b'application/epub+zip'
        assert z.testzip() is None
        names=z.namelist()
        assert len([n for n in names if re.fullmatch(r'EPUB/Text/entry-\d\d.xhtml',n)])==16

    shutil.rmtree(tmp)
    print(lang,'OK','entries=16','epub=',out,'bytes=',out.stat().st_size)

for lang in ('en','ko'): build(lang)

# Update Downloads page only by adding EPUB line after each Part II PDF line.
dp=ROOT/'downloads/index.html'
d=dp.read_text(encoding='utf-8')
for lang in ('en','ko'):
    pdf=f'a-dictionary-of-galactic-extinction-part-02-{lang}-20261004-ver-001.pdf'
    epub=f'a-dictionary-of-galactic-extinction-part-02-{lang}-20261004-ver-001.epub'
    if epub not in d:
        pdfline=next(line for line in d.splitlines() if pdf in line)
        ep_line=pdfline.replace('data-format="pdf"','data-format="epub"').replace('.pdf','.epub')
        d=d.replace(pdfline,pdfline+'\n'+ep_line,1)
dp.write_text(d,encoding='utf-8')
assert d.count('a-dictionary-of-galactic-extinction-part-02-en-20261004-ver-001.epub')==2
assert d.count('a-dictionary-of-galactic-extinction-part-02-ko-20261004-ver-001.epub')==2

# Update October 4 Publication Log wording.
lp=ROOT/'publication-log/index.html'
s=lp.read_text(encoding='utf-8')
old='Part II — free PDF editions added in English and Korean'
new='Part II — free PDF and EPUB editions added in English and Korean'
assert old in s and new not in s
s=s.replace(old,new,1)
lp.write_text(s,encoding='utf-8')
print('downloads/log OK')
