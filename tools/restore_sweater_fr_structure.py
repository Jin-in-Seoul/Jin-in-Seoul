from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter
import zipfile, tempfile, shutil, re, html, sys

ROOT=Path('.')
EPUB=ROOT/'assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.epub'
if not EPUB.exists():
    EPUB=ROOT/'assets/downloads/sweater/fr/sweater-fr-20260930-ver-001.epub'
if not EPUB.exists():
    raise SystemExit('French Sweater EPUB not found')

MONTHS=['mars','avril','mai','juin','juillet','août','septembre','octobre','novembre','décembre','janvier','février']
DAYS=['lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche']
date_re=re.compile(r'^(?:'+'|'.join(DAYS)+r')\s+\d{1,2}(?:er)?\s+(?:'+'|'.join(MONTHS)+r')(?:\s*\([^)]*\))?$',re.I)
num_re=re.compile(r'^\s*(\d+)\.\s+(.*)$',re.S)
word_re=re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿŒœ’'-]+|\d+",re.UNICODE)

def norm_words(text):
    words=[]
    for w in word_re.findall(text.replace('\u00a0',' ')):
        if w.isdigit():
            continue
        words.append(w.lower().replace('’',"'"))
    return words

def counter_distance(a,b):
    ca,cb=Counter(norm_words(a)),Counter(norm_words(b))
    missing=sum((ca-cb).values())
    extra=sum((cb-ca).values())
    total=max(1,sum(ca.values()))
    return (missing+extra)/total,missing,extra

tmp=Path(tempfile.mkdtemp())
try:
    with zipfile.ZipFile(EPUB) as z:
        z.extractall(tmp)
    src=None
    soup=None
    sections=None
    for cand in tmp.rglob('*.xhtml'):
        cs=BeautifulSoup(cand.read_text(encoding='utf-8'),'xml')
        ss=cs.find_all('section',class_=lambda c:c and 'chapter-heading' in c)
        if len(ss)==12:
            src=cand; soup=cs; sections=ss; break
    if src is None:
        raise RuntimeError('Could not locate XHTML containing all 12 chapters')
    print('source',src)

    for idx,sec in enumerate(sections,1):
        page=ROOT/f'sweater/fr/chapter-{idx:02d}/index.html'
        current=page.read_text(encoding='utf-8')
        cur_soup=BeautifulSoup(current,'lxml')
        cur_prose=cur_soup.find('section',class_='prose')
        if cur_prose is None:
            raise RuntimeError(f'No prose section in {page}')

        # EPUB body content after h1, preserving inline emphasis.
        nodes=[]
        for child in sec.children:
            if getattr(child,'name',None)=='h1':
                continue
            if getattr(child,'name',None)=='p':
                inner=''.join(str(x) for x in child.contents).strip()
                text=child.get_text(' ',strip=True)
                nodes.append(('p',inner,text))

        epub_text=' '.join(x[2] for x in nodes)
        current_text=cur_prose.get_text(' ',strip=True)
        dist,missing,extra=counter_distance(epub_text,current_text)
        # Structure corruption should not alter vocabulary. Permit tiny punctuation/tokenization drift.
        if dist>0.018:
            raise RuntimeError(f'Content drift too large in {page}: dist={dist:.4f}, missing={missing}, extra={extra}')

        out=[]
        i=0
        while i<len(nodes):
            _,inner,text=nodes[i]
            if date_re.match(text):
                out.append(f'<p class="entry-date">{inner}</p>')
                i+=1
                continue

            m=num_re.match(text)
            if m:
                items=[]
                while i<len(nodes):
                    _,iin,tt=nodes[i]
                    mm=num_re.match(tt)
                    if not mm:
                        break
                    # Remove visible numeric prefix from inner HTML, retain the item text.
                    clean=re.sub(r'^\s*\d+\.\s*','',iin,count=1)
                    items.append(f'<li>{clean}</li>')
                    i+=1
                out.append('<ol>\n'+'\n'.join(items)+'\n</ol>')
                continue

            out.append(f'<p>{inner}</p>')
            i+=1

        replacement='<section class="prose">\n'+'\n'.join(out)+'\n    </section>'
        new_current=re.sub(r'<section class="prose">[\s\S]*?</section>',replacement,current,count=1)
        if new_current==current:
            print(f'unchanged {page}')
        else:
            page.write_text(new_current,encoding='utf-8')
            print(f'fixed {page} dist={dist:.4f}')

    # Post-build checks: correct date counts and no obvious swallowed prose inside long list items.
    expected_dates=[31,30,31,30,31,31,30,31,30,31,31,28]
    for idx,n in enumerate(expected_dates,1):
        page=ROOT/f'sweater/fr/chapter-{idx:02d}/index.html'
        s=BeautifulSoup(page.read_text(encoding='utf-8'),'lxml')
        prose=s.find('section',class_='prose')
        dates=prose.find_all('p',class_='entry-date')
        if len(dates)!=n:
            raise RuntimeError(f'Date count mismatch {page}: {len(dates)} != {n}')
        for li in prose.find_all('li'):
            if len(li.get_text(' ',strip=True))>900:
                raise RuntimeError(f'Suspicious long list item in {page}')
finally:
    shutil.rmtree(tmp,ignore_errors=True)
