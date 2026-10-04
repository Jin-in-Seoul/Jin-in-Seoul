from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, shutil, re

R=Path('.')
src=R/'assets/images/sisyphus.png'
dst=R/'assets/images/sisyphus-signature.png'
if not src.exists():
    raise RuntimeError('missing source banner')

# Build a separate banner asset so the original remains untouched and can be restored/swapped later.
im=Image.open(src).convert('RGBA')
W,H=im.size
draw=ImageDraw.Draw(im)

font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
if not Path(font_path).exists():
    raise RuntimeError('Noto Serif CJK font missing')

lines=[
    'These two hands of mine live by gnawing away at my memories.',
    '私のこの両手は、私の記憶を食い荒らしながら生きている。',
    'Mes deux mains vivent en rongeant mes souvenirs.',
    '나의 두 손은 내 기억을 파먹고 산다.',
]

maxw=int(W*0.47)
size=max(14,int(W*0.021))
while size>10:
    font=ImageFont.truetype(font_path,size=size,index=0)
    widths=[draw.textbbox((0,0),t,font=font)[2] for t in lines]
    if max(widths)<=maxw:
        break
    size-=1
font=ImageFont.truetype(font_path,size=size,index=0)
bbox=draw.textbbox((0,0),'Ag私한',font=font)
lineh=bbox[3]-bbox[1]
gap=max(8,int(lineh*0.78))
block_h=lineh*4+gap*3
x=int(W*0.025)
y=max(int(H*0.08),(H-block_h)//2)
fill=(45,45,45,235)
for t in lines:
    draw.text((x,y),t,font=font,fill=fill)
    y+=lineh+gap

im.convert('RGB').save(dst,quality=95,optimize=True)

p=R/'index.html'
s=p.read_text(encoding='utf-8')

old_intro='''      <p>
        <em>A Dictionary of Galactic Extinction</em> began with two images.
      </p>

      <p>
        One came from <em>Men in Black</em>: a tiny galaxy contained inside a bead
        hanging from a cat’s collar. The other came much later, from a simple question:
        what would happen if a candle burned inside a perfectly mirrored room and its
        light could never escape?
      </p>

      <p>
        Those two images gradually became questions about light, energy, civilization,
        and extinction. What interested me was not a story in which evil destroys
        civilization, but a more difficult problem: what happens when rational and
        well-intentioned people keep solving problems, and the accumulated consequences
        of those solutions eventually become catastrophic?
      </p>

      <p>
        The form of the novel grew from the same concern. Rather than tell the history
        of a vast civilization through a single protagonist and a single plot, I wanted
        the world to emerge through fragments of physics, history, people, words,
        records, and different kinds of documents.
      </p>

      <p>
        At first, I wanted to write a story about placing a galaxy inside a small object.
        In the end, it became something entirely different. I wanted to place human
        goodwill, desire, fear, language, and reason inside a galaxy, and see where they
        would lead if allowed to operate to their logical end.
      </p>

      <h3 class="serial-title">Serial Publication</h3>

      <p>
        <em>A Dictionary of Galactic Extinction</em> is currently being published
        online in serialized form in <strong>English, Japanese, French, and Korean</strong>.
      </p>
'''

new_intro='''      <p>
        <em>A Dictionary of Galactic Extinction</em> began with a simple question:
        what would happen if light could be trapped inside a perfectly mirrored room
        and never escape?
      </p>

      <p>
        From that question grew a fragmented history of light, energy, civilization,
        and extinction — told through physics, records, people, words, and documents
        rather than a single protagonist or plot.
      </p>
'''

if old_intro not in s:
    raise RuntimeError('dictionary intro block not found')
s=s.replace(old_intro,new_intro,1)

old_img='<img src="/assets/images/sisyphus.png" alt="A figure pushing a boulder uphill" loading="lazy">'
new_img='<img src="/assets/images/sisyphus-signature.png" alt="A figure pushing a boulder uphill with a multilingual signature line" loading="lazy">'
if old_img not in s:
    raise RuntimeError('sisyphus image tag not found')
s=s.replace(old_img,new_img,1)

css_anchor='''    .home-short-stories-list .work:first-child {
      padding-top: 0;
    }

'''
css_add='''    .home-short-stories-list .work:first-child {
      padding-top: 0;
    }

    .home-short-stories-list h3 a {
      text-decoration: none;
    }

    .home-short-stories-list h3 a:hover {
      text-decoration: underline;
      text-underline-offset: 4px;
    }

'''
if css_anchor not in s:
    raise RuntimeError('short story CSS anchor not found')
s=s.replace(css_anchor,css_add,1)

# Ensure Scarecrow Distance remains the agreed two-line form.
if 'A rough, desolate novel written in the language of abandoned stray dogs. <em>(Serialized online.)</em>' not in s:
    raise RuntimeError('Scarecrow Distance serial line not in expected form')
if '(Work in progress.)' in s:
    raise RuntimeError('old Work in progress label still present')

p.write_text(s,encoding='utf-8')

# Basic asset checks
chk=Image.open(dst)
if chk.size!=(W,H):
    raise RuntimeError('banner dimensions changed')
print('banner-size',W,H,'font-size',size)
print('home update checks passed')
