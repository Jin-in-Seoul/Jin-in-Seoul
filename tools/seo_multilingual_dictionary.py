from pathlib import Path
from bs4 import BeautifulSoup
import json, re

R=Path('.')
base='https://jin-in-seoul.com/a-dictionary-of-galactic-extinction'
langs=['en','ja','fr','ko']

root_desc={
'en':'A multilingual archival novel about light, energy, civilization, and extinction, told through physics, records, people, words, and documents.',
'ja':'光、エネルギー、文明、滅亡をめぐる多言語のアーカイブ小説。物理学、記録、人々、言葉、文書の断片を通して世界が立ち上がる。',
'fr':'Un roman-archive multilingue sur la lumière, l’énergie, la civilisation et l’extinction, raconté par la physique, les archives, les personnes, les mots et les documents.',
'ko':'빛, 에너지, 문명과 멸망을 다루는 다국어 아카이브 소설. 물리학, 기록, 사람, 단어와 문서의 파편을 통해 세계가 드러난다.'
}

part_names={
'en':'Part I — Conditions of Extinction',
'ja':'第1部 — 滅亡の条件',
'fr':'Première partie — Conditions de l’extinction',
'ko':'제1부 — 멸망의 조건'
}

def ensure_head_metadata(path, lang, url, desc, alternates, schema_type, schema_name, is_entry=False):
    p=R/path
    s=p.read_text(encoding='utf-8')
    soup=BeautifulSoup(s,'lxml')
    title=soup.title.get_text(strip=True)
    # Work directly on source text to preserve formatting/template tags.
    # Remove previous versions of tags we own.
    patterns=[
        r'\n?\s*<meta name="description"[^>]*>',
        r'\n?\s*<meta name="robots"[^>]*>',
        r'\n?\s*<link rel="canonical"[^>]*>',
        r'\n?\s*<link rel="alternate" hreflang="[^"]+"[^>]*>',
        r'\n?\s*<meta property="og:type"[^>]*>',
        r'\n?\s*<meta property="og:title"[^>]*>',
        r'\n?\s*<meta property="og:description"[^>]*>',
        r'\n?\s*<meta property="og:url"[^>]*>',
        r'\n?\s*<meta property="og:site_name"[^>]*>',
        r'\n?\s*<script type="application/ld\+json" data-seo="dictionary">.*?</script>'
    ]
    for pat in patterns:
        s=re.sub(pat,'',s,flags=re.S)

    alt_lines='\n'.join(
        f'  <link rel="alternate" hreflang="{code}" href="{href}">'
        for code,href in alternates
    )
    block=f'''  <meta name="description" content="{desc}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{url}">
{alt_lines}
  <meta property="og:type" content="{'article' if is_entry else 'website'}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="Jin-in-Seoul">
  <script type="application/ld+json" data-seo="dictionary">
{json.dumps({
  "@context":"https://schema.org",
  "@type":schema_type,
  "name":schema_name,
  "url":url,
  "inLanguage":lang,
  "author":{"@type":"Person","name":"Jin-in-Seoul","url":"https://jin-in-seoul.com/"},
  **({"isPartOf":{"@type":"CreativeWork","name":"A Dictionary of Galactic Extinction","url":f"{base}/{lang}/"}} if is_entry else {})
},ensure_ascii=False,indent=2)}
  </script>'''

    marker=re.search(r'(<title>.*?</title>)',s,flags=re.S)
    if not marker:
        raise RuntimeError(f'No title in {path}')
    s=s[:marker.end()]+'\n'+block+s[marker.end():]
    p.write_text(s,encoding='utf-8')

# Root pages: reciprocal 4-language hreflang + x-default.
for lang in langs:
    path=f'a-dictionary-of-galactic-extinction/{lang}/index.html'
    if not (R/path).exists():
        continue
    url=f'{base}/{lang}/'
    alternates=[(l,f'{base}/{l}/') for l in langs if (R/f'a-dictionary-of-galactic-extinction/{l}/index.html').exists()]
    alternates.append(('x-default',f'{base}/en/'))
    names={
      'en':'A Dictionary of Galactic Extinction',
      'ja':'銀河滅亡辞典',
      'fr':'Dictionnaire de l’extinction galactique',
      'ko':'은하 멸망 사전'
    }
    ensure_head_metadata(path,lang,url,root_desc[lang],alternates,'CreativeWork',names[lang],False)

# Part I entries 1-9. Add only alternates that actually exist.
for i in range(1,10):
    existing=[]
    for lang in langs:
        path=R/f'a-dictionary-of-galactic-extinction/{lang}/part-01/entry-{i:02d}/index.html'
        if path.exists():
            existing.append(lang)
    for lang in existing:
        rel=f'a-dictionary-of-galactic-extinction/{lang}/part-01/entry-{i:02d}/index.html'
        p=R/rel
        soup=BeautifulSoup(p.read_text(encoding='utf-8'),'lxml')
        h1=soup.find('h1',class_='entry-title')
        if not h1:
            raise RuntimeError(f'No entry title: {rel}')
        entry_title=h1.get_text(' ',strip=True)
        plain=re.sub(r'^\d+\.\s*','',entry_title)
        url=f'{base}/{lang}/part-01/entry-{i:02d}/'
        alternates=[(l,f'{base}/{l}/part-01/entry-{i:02d}/') for l in existing]
        if 'en' in existing:
            alternates.append(('x-default',f'{base}/en/part-01/entry-{i:02d}/'))
        descs={
          'en':f'{plain} — Entry {i} of {part_names["en"]} in A Dictionary of Galactic Extinction, a fragmented archive of light, energy, civilization, and extinction.',
          'ja':f'{plain} — 『銀河滅亡辞典』{part_names["ja"]}の第{i}項。光、エネルギー、文明、滅亡をめぐる断片的な記録。',
          'fr':f'{plain} — Entrée {i} de la {part_names["fr"]} du Dictionnaire de l’extinction galactique, archive fragmentaire de la lumière, de l’énergie, de la civilisation et de l’extinction.',
          'ko':f'{plain} — 『은하 멸망 사전』 {part_names["ko"]}의 {i}번째 항목. 빛, 에너지, 문명과 멸망을 다루는 파편적 기록.'
        }
        ensure_head_metadata(rel,lang,url,descs[lang],alternates,'CreativeWork',entry_title,True)

# Validate all updated pages.
for lang in langs:
    root=R/f'a-dictionary-of-galactic-extinction/{lang}/index.html'
    if root.exists():
        t=root.read_text(encoding='utf-8')
        assert t.count('rel="canonical"')==1
        assert 'hreflang="x-default"' in t
        assert 'name="description"' in t
        assert 'data-seo="dictionary"' in t

for i in range(1,10):
    for lang in langs:
        p=R/f'a-dictionary-of-galactic-extinction/{lang}/part-01/entry-{i:02d}/index.html'
        if p.exists():
            t=p.read_text(encoding='utf-8')
            assert t.count('rel="canonical"')==1
            assert 'name="description"' in t
            assert f'hreflang="{lang}"' in t
            assert 'data-seo="dictionary"' in t

print('multilingual dictionary SEO update validated')
