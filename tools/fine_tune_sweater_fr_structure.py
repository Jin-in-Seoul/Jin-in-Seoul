from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT=Path('.')

def replace_p_with_texts(soup,p,parts):
    for piece in parts:
        piece=piece.strip()
        if not piece:
            continue
        tag=soup.new_tag('p')
        tag.string=piece
        p.insert_before(tag)
    p.decompose()

for idx in range(1,13):
    path=ROOT/f'sweater/fr/chapter-{idx:02d}/index.html'
    text=path.read_text(encoding='utf-8')
    m=re.search(r'<section class="prose">([\s\S]*?)</section>',text)
    if not m:
        raise RuntimeError(f'No prose section: {path}')

    frag=BeautifulSoup('<div id="root">'+m.group(1)+'</div>','lxml')
    root=frag.find('div',id='root')

    for p in list(root.find_all('p',recursive=False)):
        if 'entry-date' in (p.get('class') or []):
            continue
        txt=p.get_text(' ',strip=True)

        # Each timestamped log line is an independent beat in the Korean master.
        times=list(re.finditer(r'\b\d{2}\s*h\s*\d{2}\.?',txt))
        if len(times)>=2:
            parts=[]
            if times[0].start()>0:
                intro=txt[:times[0].start()].strip()
                if intro:
                    parts.append(intro)
            for j,mm in enumerate(times):
                end=times[j+1].start() if j+1<len(times) else len(txt)
                parts.append(txt[mm.start():end].strip())
            replace_p_with_texts(frag,p,parts)
            continue

        # Multiple bullet entries collapsed into a single paragraph.
        marks=list(re.finditer(r'[•]',txt))
        if len(marks)>=2:
            parts=[]
            if marks[0].start()>0:
                intro=txt[:marks[0].start()].strip()
                if intro:
                    parts.append(intro)
            for j,mm in enumerate(marks):
                end=marks[j+1].start() if j+1<len(marks) else len(txt)
                parts.append(txt[mm.start():end].strip())
            replace_p_with_texts(frag,p,parts)
            continue

        # Heading + first bullet collapsed together.
        if len(marks)==1 and txt.startswith('—'):
            mm=marks[0]
            replace_p_with_texts(frag,p,[txt[:mm.start()],txt[mm.start():]])
            continue

        # April packing list: note after item 15 is not part of the item.
        if idx==2 and txt.startswith('15. Écouteurs * Ce qui n’est finalement pas rentré'):
            a,b=txt.split(' * ',1)
            replace_p_with_texts(frag,p,[a,'* '+b])
            continue

    new_inner=root.decode_contents()
    new_text=text[:m.start(1)]+new_inner+text[m.end(1):]
    path.write_text(new_text,encoding='utf-8')
    print('fine-tuned',path)

# Assertions for known problem areas.
checks={
  2:['<p>15. Écouteurs</p>','<p>* Ce qui n’est finalement pas rentré'],
  4:['<p>07 h 40 Réveil.</p>','<p>07 h 50 Hee-jeong appelle'],
  6:['<p>06 h 00 Réveil tout seul.</p>','<p>07 h 00 Papa me secoue'],
  10:['<p>• Voiture 1.','<p>• Voiture 2.','<p>• Voiture 3.','<p>07 h 00. Tout le monde se retrouve'],
}
for idx,needles in checks.items():
    c=(ROOT/f'sweater/fr/chapter-{idx:02d}/index.html').read_text(encoding='utf-8')
    for needle in needles:
        if needle not in c:
            raise RuntimeError(f'Missing expected structure in chapter {idx}: {needle}')
