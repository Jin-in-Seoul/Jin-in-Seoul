from pathlib import Path
import re, json, html
from urllib.parse import quote

ROOT=Path(".")
BASE="https://jin-in-seoul.com"
LANGS=("en","ja","fr","ko")

def url_for(path: Path):
    p=path.as_posix()
    if p=="index.html":
        return BASE+"/"
    assert p.endswith("/index.html")
    return BASE+"/"+p[:-10]

def clean_text(s):
    s=re.sub(r"<[^>]+>"," ",s)
    s=html.unescape(s)
    s=re.sub(r"\s+"," ",s).strip()
    return s

def title_of(s):
    m=re.search(r"<title>(.*?)</title>",s,re.S|re.I)
    return clean_text(m.group(1)) if m else "Jin-in-Seoul"

def h1_of(s):
    m=re.search(r"<h1(?:\s[^>]*)?>(.*?)</h1>",s,re.S|re.I)
    return clean_text(m.group(1)) if m else title_of(s).split(" - ")[0]

def lang_of(s):
    m=re.search(r'<html[^>]*\blang="([^"]+)"',s,re.I)
    return m.group(1) if m else "en"

def esc_attr(s):
    return html.escape(s, quote=True)

def desc_for(path,s,lang,title,h1):
    p=path.as_posix()
    # Core fiction works
    if p.startswith("sweater/"):
        if "/chapter-" in p:
            d={
              "en":f"{h1} — a chapter from Sweater, Jin-in-Seoul’s novel of a fourteen-year-old boy’s year of school, family, friendship, first love, books, and small discoveries.",
              "fr":f"{h1} — un chapitre de Le Pull, roman de Jin-in-Seoul sur l’année d’un garçon de quatorze ans, entre école, famille, amitié, premier amour et livres.",
              "ja":f"{h1} — Jin-in-Seoulの小説『セーター』の一章。十四歳の少年の一年を、学校、家族、友情、初恋、本、小さな発見とともに描く。"
            }
        else:
            d={
              "en":"Sweater is Jin-in-Seoul’s novel of a fourteen-year-old boy’s year of school, family, friendship, first love, books, and small discoveries.",
              "fr":"Le Pull est un roman de Jin-in-Seoul sur l’année d’un garçon de quatorze ans, entre école, famille, amitié, premier amour, livres et petites découvertes.",
              "ja":"『セーター』はJin-in-Seoulによる小説。十四歳の少年の一年を、学校、家族、友情、初恋、本、日々の小さな発見とともに描く。"
            }
        return d.get(lang,d.get("en"))
    if p.startswith("scarecrow-distance/"):
        names={"en":"Scarecrow Distance","fr":"Mal reçu","ja":"案山子の距離","ko":"소실점"}
        if "/chapter-" in p:
            d={
             "en":f"{h1} — a chapter from Scarecrow Distance, Jin-in-Seoul’s rough, desolate novel about two boys making their way from Sokcho to Mokpo.",
             "fr":f"{h1} — un chapitre de Mal reçu, roman âpre et désolé de Jin-in-Seoul sur deux garçons en route de Sokcho à Mokpo.",
             "ja":f"{h1} — Jin-in-Seoulの小説『案山子の距離』の一章。束草から木浦へ向かう二人の少年を描く、荒涼とした物語。",
             "ko":f"{h1} — Jin-in-Seoul의 장편소설 『소실점』의 한 장. 속초에서 목포로 향하는 두 소년의 거칠고 황량한 이야기."
            }
        else:
            d={
             "en":"Scarecrow Distance is a rough, desolate novel by Jin-in-Seoul about two boys making their way from Sokcho to Mokpo.",
             "fr":"Mal reçu est un roman âpre et désolé de Jin-in-Seoul sur deux garçons qui vont de Sokcho à Mokpo.",
             "ja":"『案山子の距離』はJin-in-Seoulによる長編小説。束草から木浦へ向かう二人の少年を描く、荒涼とした物語。",
             "ko":"『소실점』은 속초에서 목포로 향하는 두 소년을 그린 Jin-in-Seoul의 거칠고 황량한 장편소설."
            }
        return d.get(lang,d["en"])
    if p.startswith("short-stories/"):
        if re.search(r"/(en|ja|fr|ko)/index\.html$",p):
            d={
             "en":f"{h1} — a short story by Jin-in-Seoul, available as part of the multilingual fiction archive Jin-in-Seoul.",
             "fr":f"{h1} — une nouvelle de Jin-in-Seoul, publiée dans l’archive littéraire multilingue Jin-in-Seoul.",
             "ja":f"{h1} — Jin-in-Seoulによる短編小説。多言語フィクション・アーカイブ Jin-in-Seoul で公開。",
             "ko":f"{h1} — Jin-in-Seoul의 단편소설. 다국어 소설 아카이브 Jin-in-Seoul에서 공개."
            }
            return d.get(lang,d["en"])
        return "Short stories by Jin-in-Seoul, available to read in English, Japanese, French, and Korean."
    if p.startswith("a-dictionary-of-galactic-extinction/translation-principles/"):
        d={
         "en":"Translation principles for A Dictionary of Galactic Extinction: direct translation from the Korean original, preserving meaning, structure, repetition, terminology, and the work’s dry archival voice.",
         "fr":"Principes de traduction du Dictionnaire de l’extinction galactique : traduction directe depuis l’original coréen, en préservant sens, structure, répétitions, terminologie et voix documentaire.",
         "ja":"『銀河滅亡辞典』の翻訳原則。韓国語原文から直接翻訳し、意味、構造、反復、用語、乾いた記録文体を保つ。",
         "ko":"『은하 멸망 사전』 번역 원칙. 한국어 원문에서 직접 번역하며 의미, 구조, 반복, 용어와 건조한 기록 문체를 보존한다."
        }
        return d.get(lang,d["en"])
    if p.startswith("a-dictionary-of-galactic-extinction/"):
        if re.search(r"/entry-\d+/index\.html$",p):
            d={
             "en":f"{h1} — an entry from A Dictionary of Galactic Extinction, Jin-in-Seoul’s fragmented literary archive of light, energy, civilization, and extinction.",
             "fr":f"{h1} — une entrée du Dictionnaire de l’extinction galactique, archive littéraire fragmentaire de Jin-in-Seoul sur la lumière, l’énergie, la civilisation et l’extinction.",
             "ja":f"{h1} — Jin-in-Seoul『銀河滅亡辞典』の一項。光、エネルギー、文明、滅亡をめぐる断片的な文学アーカイブ。",
             "ko":f"{h1} — Jin-in-Seoul 『은하 멸망 사전』의 한 항목. 빛, 에너지, 문명과 멸망을 다루는 파편적 문학 아카이브."
            }
            return d.get(lang,d["en"])
        d={
         "en":"A Dictionary of Galactic Extinction is Jin-in-Seoul’s fragmented literary archive of light, energy, civilization, and extinction, told through physics, records, people, words, and documents.",
         "fr":"Dictionnaire de l’extinction galactique est l’archive littéraire fragmentaire de Jin-in-Seoul sur la lumière, l’énergie, la civilisation et l’extinction.",
         "ja":"『銀河滅亡辞典』はJin-in-Seoulによる、光、エネルギー、文明、滅亡をめぐる断片的な文学アーカイブ。",
         "ko":"『은하 멸망 사전』은 빛, 에너지, 문명과 멸망을 물리학, 기록, 인물, 단어와 문서로 구성한 Jin-in-Seoul의 파편적 문학 아카이브."
        }
        return d.get(lang,d["en"])
    # Multilingual one-URL sections
    if p=="gray-note/index.html":
        return "Gray Note: short multilingual essays by Jin-in-Seoul on small objects, passing moments, and ordinary things that are easy to overlook."
    if p=="music/index.html":
        return "Music by Jin-in-Seoul: songs growing out of scenes, emotions, and lines from fiction, with multilingual lyrics in English, Japanese, French, and Korean."
    if p.startswith("music/"):
        return f"{h1} — music and multilingual lyrics by Jin-in-Seoul in English, Japanese, French, and Korean."
    if p=="haiku/index.html":
        return "Haiku by Jin-in-Seoul: short poems presented in Japanese, English, French, and Korean."
    if p.startswith("haiku/"):
        return f"{h1} — a haiku by Jin-in-Seoul presented in Japanese, English, French, and Korean."
    if p=="downloads/index.html":
        return "Free PDF and EPUB digital editions of works published on Jin-in-Seoul, organized by work, part, language, and version."
    if p=="publication-log/index.html":
        return "Publication log for Jin-in-Seoul, recording new works, translations, chapters, and free digital editions added to the multilingual fiction archive."
    if p=="site-map/index.html":
        return "Site map for Jin-in-Seoul, a multilingual fiction archive with novels, short stories, essays, haiku, music, translation principles, and free digital editions."
    if p=="sweater/index.html":
        return "Choose a language for Sweater / Le Pull / セーター, Jin-in-Seoul’s novel available online in English, French, and Japanese."
    if p=="scarecrow-distance/index.html":
        return "Choose a language for Scarecrow Distance / Mal reçu / 案山子の距離 / 소실점, a serialized novel by Jin-in-Seoul."
    if p=="a-dictionary-of-galactic-extinction/index.html":
        return "Choose a language for A Dictionary of Galactic Extinction, a multilingual literary archive by Jin-in-Seoul."
    return f"{h1} — part of Jin-in-Seoul, a multilingual archive of fiction, essays, haiku, music, and digital editions."

def schema_for(path):
    p=path.as_posix()
    if p.startswith("music/") and p!="music/index.html": return "MusicRecording"
    if p.startswith("haiku/") and p!="haiku/index.html": return "CreativeWork"
    if p.startswith("short-stories/") and re.search(r"/(en|ja|fr|ko)/index\.html$",p): return "CreativeWork"
    if p.startswith("sweater/") and re.search(r"/(en|ja|fr)/",p): return "Book"
    if p.startswith("scarecrow-distance/") and re.search(r"/(en|ja|fr|ko)/",p): return "CreativeWork"
    if p.startswith("a-dictionary-of-galactic-extinction/translation-principles/"): return "Article"
    if p.startswith("a-dictionary-of-galactic-extinction/") and re.search(r"/(en|ja|fr|ko)/",p): return "CreativeWork"
    if p in ("short-stories/index.html","music/index.html","haiku/index.html","downloads/index.html","publication-log/index.html"): return "CollectionPage"
    return "WebPage"

def group_key(path):
    p=path.as_posix()
    # /work/{lang}/...
    m=re.match(r"(sweater|scarecrow-distance|a-dictionary-of-galactic-extinction)/(en|ja|fr|ko)/(.*)",p)
    if m:
        return (m.group(1),m.group(3))
    # short-stories/{story}/{lang}/index.html
    m=re.match(r"short-stories/([^/]+)/(en|ja|fr|ko)/(.*)",p)
    if m:
        return ("short-stories/"+m.group(1),m.group(3))
    # translation principles
    m=re.match(r"a-dictionary-of-galactic-extinction/translation-principles/(en|ja|fr|ko)/(.*)",p)
    if m:
        return ("translation-principles",m.group(2))
    return None

files=[p for p in ROOT.rglob("index.html") if ".git" not in p.parts and not p.as_posix().startswith("tools/")]
groups={}
for p in files:
    if p.as_posix()=="index.html": continue
    k=group_key(p)
    if k:
        groups.setdefault(k,[]).append(p)

def alt_lang_for(p):
    s=p.read_text(encoding="utf-8")
    return lang_of(s)

def alternates_for(path):
    k=group_key(path)
    if not k: return []
    members=groups.get(k,[])
    pairs=sorted(((alt_lang_for(p),url_for(p)) for p in members),key=lambda x: LANGS.index(x[0]) if x[0] in LANGS else 99)
    if pairs:
        default=next((u for l,u in pairs if l=="en"),pairs[0][1])
        pairs.append(("x-default",default))
    return pairs

def remove_owned(s):
    pats=[
      r'\n?\s*<meta name="description"[^>]*>',
      r'\n?\s*<meta name="robots"[^>]*>',
      r'\n?\s*<link rel="canonical"[^>]*>',
      r'\n?\s*<link rel="alternate" hreflang="[^"]+"[^>]*>',
      r'\n?\s*<meta property="og:type"[^>]*>',
      r'\n?\s*<meta property="og:title"[^>]*>',
      r'\n?\s*<meta property="og:description"[^>]*>',
      r'\n?\s*<meta property="og:url"[^>]*>',
      r'\n?\s*<meta property="og:site_name"[^>]*>',
      r'\n?\s*<meta name="twitter:card"[^>]*>',
      r'\n?\s*<meta name="twitter:title"[^>]*>',
      r'\n?\s*<meta name="twitter:description"[^>]*>',
      r'\n?\s*<script type="application/ld\+json" data-seo="(?:dictionary|site)">.*?</script>'
    ]
    for pat in pats:
        s=re.sub(pat,"",s,flags=re.S|re.I)
    return s

changed=0
for path in files:
    if path.as_posix()=="index.html":
        continue  # preserve carefully tuned homepage + Naver verification
    s=path.read_text(encoding="utf-8")
    title=title_of(s); h1=h1_of(s); lang=lang_of(s); url=url_for(path)
    desc=desc_for(path,s,lang,title,h1)
    typ=schema_for(path)
    alts=alternates_for(path)

    s=remove_owned(s)
    schema={
      "@context":"https://schema.org",
      "@type":typ,
      "name":h1,
      "url":url,
      "inLanguage": (["en","ja","fr","ko"] if (path.as_posix().startswith("music/") or path.as_posix().startswith("haiku/") or path.as_posix()=="gray-note/index.html") else lang)
    }
    if typ in ("Book","CreativeWork","Article","MusicRecording"):
        schema["author"]={"@type":"Person","name":"Jin-in-Seoul","url":BASE+"/"}
    if "/chapter-" in path.as_posix() or "/entry-" in path.as_posix():
        # link chapters/entries back to their work-level language landing where possible
        parts=path.as_posix().split("/")
        if parts[0] in ("sweater","scarecrow-distance","a-dictionary-of-galactic-extinction") and len(parts)>2 and parts[1] in LANGS:
            schema["isPartOf"]={"@type":"CreativeWork","url":f"{BASE}/{parts[0]}/{parts[1]}/"}

    lines=[
      f'  <meta name="description" content="{esc_attr(desc)}">',
      '  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">',
      f'  <link rel="canonical" href="{url}">'
    ]
    lines += [f'  <link rel="alternate" hreflang="{l}" href="{u}">' for l,u in alts]
    lines += [
      f'  <meta property="og:type" content="{"music.song" if typ=="MusicRecording" else "article" if typ in ("CreativeWork","Book","Article") else "website"}">',
      f'  <meta property="og:title" content="{esc_attr(title)}">',
      f'  <meta property="og:description" content="{esc_attr(desc)}">',
      f'  <meta property="og:url" content="{url}">',
      '  <meta property="og:site_name" content="Jin-in-Seoul">',
      '  <meta name="twitter:card" content="summary">',
      f'  <meta name="twitter:title" content="{esc_attr(title)}">',
      f'  <meta name="twitter:description" content="{esc_attr(desc)}">',
      '  <script type="application/ld+json" data-seo="site">',
      json.dumps(schema,ensure_ascii=False,indent=2),
      '  </script>'
    ]
    block="\n".join(lines)
    m=re.search(r"<title>.*?</title>",s,re.S|re.I)
    if not m: raise RuntimeError(f"No title: {path}")
    s=s[:m.end()]+"\n"+block+s[m.end():]
    path.write_text(s,encoding="utf-8")
    changed+=1

# Gray Note post layout: dynamic canonical, description, OG, Article JSON-LD.
layout=ROOT/"_layouts/gray-note-post.html"
ls=layout.read_text(encoding="utf-8")
# Remove any prior owned dynamic SEO block
ls=re.sub(r'\n?\s*<!-- sitewide-gray-note-seo:start -->.*?<!-- sitewide-gray-note-seo:end -->',"",ls,flags=re.S)
m=re.search(r"<title>.*?</title>",ls,re.S)
if not m: raise RuntimeError("No title in Gray Note layout")
gblock=r'''
  <!-- sitewide-gray-note-seo:start -->
  <meta name="description" content="{{ page.title | append: ' — a multilingual Gray Note essay by Jin-in-Seoul on memory, places, objects, and passing moments.' | escape }}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <link rel="canonical" href="{{ page.url | absolute_url }}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{{ page.title | escape }} - Gray Note - Jin-in-Seoul">
  <meta property="og:description" content="{{ page.title | append: ' — a multilingual Gray Note essay by Jin-in-Seoul.' | escape }}">
  <meta property="og:url" content="{{ page.url | absolute_url }}">
  <meta property="og:site_name" content="Jin-in-Seoul">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{{ page.title | escape }} - Gray Note - Jin-in-Seoul">
  <script type="application/ld+json" data-seo="site">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": {{ page.title | jsonify }},
    "url": {{ page.url | absolute_url | jsonify }},
    "datePublished": {{ page.date | date_to_xmlschema | jsonify }},
    "inLanguage": ["en", "ja", "fr", "ko"],
    "author": {"@type": "Person", "name": "Jin-in-Seoul", "url": "https://jin-in-seoul.com/"}
  }
  </script>
  <!-- sitewide-gray-note-seo:end -->'''
ls=ls[:m.end()]+gblock+ls[m.end():]
layout.write_text(ls,encoding="utf-8")

# Sitemap: preserve any existing asset URLs, add every public index page and Gray Note post.
sm=ROOT/"sitemap.xml"
existing=sm.read_text(encoding="utf-8")
locs=set(re.findall(r"<loc>(.*?)</loc>",existing))
for p in files:
    locs.add(url_for(p))
# Jekyll permalink from _config.yml: /gray-note/:year/:month/:day/:title/
for p in (ROOT/"_posts").glob("*.md"):
    m=re.match(r"(\d{4})-(\d{2})-(\d{2})-(.+)\.md$",p.name)
    if m: locs.add(f"{BASE}/gray-note/{m.group(1)}/{m.group(2)}/{m.group(3)}/{m.group(4)}/")
ordered=sorted(locs,key=lambda u:(0 if u==BASE+"/" else 1,u))
body='---\n---\n<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
body+="".join(f"  <url>\n    <loc>{html.escape(u)}</loc>\n  </url>\n" for u in ordered)
body+="</urlset>\n"
sm.write_text(body,encoding="utf-8")

# Validation.
errors=[]
for path in files:
    s=path.read_text(encoding="utf-8")
    if path.as_posix()=="index.html": continue
    head=s.split("</head>",1)[0]
    checks={
      "description":head.count('name="description"'),
      "robots":head.count('name="robots"'),
      "canonical":head.count('rel="canonical"'),
      "og_title":head.count('property="og:title"'),
      "og_desc":head.count('property="og:description"'),
      "og_url":head.count('property="og:url"'),
      "jsonld":head.count('data-seo="site"')
    }
    bad={k:v for k,v in checks.items() if v!=1}
    if bad: errors.append((str(path),bad))
    for l,u in alternates_for(path):
        if f'hreflang="{l}" href="{u}"' not in head:
            errors.append((str(path),f"missing alternate {l}"))
if errors:
    raise RuntimeError(str(errors[:20]))
# Sitemap coverage
out=sm.read_text(encoding="utf-8")
for p in files:
    if f"<loc>{url_for(p)}</loc>" not in out:
        raise RuntimeError(f"Sitemap missing {p}")
print(f"SEO validated on {changed} HTML pages; sitemap contains {len(ordered)} URLs.")
