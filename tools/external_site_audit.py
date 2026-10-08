from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re, json, os, collections

ROOT=Path(".")
BASE="https://jin-in-seoul.com"

def is_public_html(p):
    s=p.as_posix()
    if not s.endswith(".html"): return False
    if s.startswith(("_includes/","_layouts/","_drafts/","tools/",".github/")): return False
    return True

html_files=sorted([p for p in ROOT.rglob("*.html") if is_public_html(p)])
all_files={p.as_posix() for p in ROOT.rglob("*") if p.is_file()}

def expected_url(p):
    s=p.as_posix()
    if s=="index.html": return BASE+"/"
    if s.endswith("/index.html"): return BASE+"/"+s[:-10]
    return BASE+"/"+s

def resolve_href(src, href):
    if not href or href.startswith(("#","mailto:","tel:","javascript:")): return None
    if "{{" in href or "{%" in href: return None
    pr=urlparse(href)
    if pr.scheme in ("http","https"):
        if pr.netloc not in ("jin-in-seoul.com","www.jin-in-seoul.com"): return None
        path=pr.path
    elif href.startswith("//"):
        return None
    elif href.startswith("/"):
        path=pr.path
    else:
        base=src.parent
        path=(base/pr.path).as_posix()
        # normalize
        parts=[]
        for x in Path(path).parts:
            if x=="..":
                if parts: parts.pop()
            elif x not in (".",""):
                parts.append(x)
        path="/".join(parts)
        if not path.startswith("/"): path="/"+path
    path=re.sub(r"/+","/",path)
    if path.endswith("/"): cand=path.lstrip("/")+"index.html"
    else:
        cand=path.lstrip("/")
        if "." not in Path(cand).name:
            cand=cand+"/index.html"
    return cand

broken=[]
canon_issues=[]
hreflang_issues=[]
seo_missing=[]
duplicate_meta=[]
suspicious=[]
prose_class_issues=[]

for p in html_files:
    raw=p.read_text(encoding="utf-8",errors="replace")
    soup=BeautifulSoup(raw,"html.parser")
    # links
    for tag in soup.find_all(["a","link","img","script","source"]):
        attr="href" if tag.name in ("a","link") else "src"
        href=tag.get(attr)
        cand=resolve_href(p,href)
        if cand and cand not in all_files:
            # Jekyll generated routes, external aladin ignored already
            if cand.startswith("gray-note/") and p.as_posix().startswith("_"): continue
            broken.append((p.as_posix(),href,cand))
    # canonical
    cans=soup.find_all("link",rel=lambda v: v and "canonical" in v)
    if len(cans)>1: duplicate_meta.append((p.as_posix(),"canonical",len(cans)))
    if cans:
        got=cans[0].get("href","")
        exp=expected_url(p)
        if got.rstrip("/")!=exp.rstrip("/"):
            canon_issues.append((p.as_posix(),got,exp))
    # hreflang
    for l in soup.find_all("link",attrs={"hreflang":True}):
        href=l.get("href","")
        cand=resolve_href(p,href)
        if cand and cand not in all_files:
            hreflang_issues.append((p.as_posix(),l.get("hreflang"),href,cand))
    # basic seo, only pages that already carry canonical as SEO-managed
    if cans:
        required=[
          ("title", bool(soup.title and soup.title.get_text(strip=True))),
          ("description", bool(soup.find("meta",attrs={"name":"description"}))),
          ("og:title", bool(soup.find("meta",attrs={"property":"og:title"}))),
          ("jsonld", bool(soup.find("script",attrs={"type":"application/ld+json"})))
        ]
        miss=[k for k,v in required if not v]
        if miss: seo_missing.append((p.as_posix(),miss))
    # suspicious editorial artifacts outside principles/admin
    if not p.as_posix().startswith("translation-principles/"):
        body=soup.get_text(" ",strip=True)
        for pat in [r"\bTODO\b",r"\bFIXME\b",r"ChatGPT",r"OpenAI",r"translation note",r"translator.?s note",r"AI-generated"]:
            if re.search(pat,body,re.I):
                suspicious.append((p.as_posix(),pat))
    # prose class expected
    sp=p.as_posix()
    expected=None
    if re.match(r"^sweater/(en|fr|ja)/chapter-\d\d/index\.html$",sp): expected="sweater-prose"
    elif re.match(r"^scarecrow-distance/(en|fr|ja|ko)/chapter-\d\d/index\.html$",sp): expected="scarecrow-prose"
    elif re.match(r"^short-stories/[^/]+/(en|fr|ja|ko)/index\.html$",sp): expected="short-story-prose"
    elif re.match(r"^childrens-books/[^/]+/(en|fr|ja|ko)/index\.html$",sp): expected="children-prose"
    elif re.match(r"^a-dictionary-of-galactic-extinction/(en|fr|ja|ko)/part-\d\d/entry-\d\d/index\.html$",sp): expected="galactic-prose"
    if expected and not soup.select_one("."+expected):
        prose_class_issues.append((sp,expected))

# Paragraph structure comparison helpers
def p_signature(path, selector):
    p=ROOT/path
    if not p.exists(): return None
    soup=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
    box=soup.select_one(selector)
    if not box: return None
    ps=box.find_all("p",recursive=True)
    classes=[]
    for x in ps:
        c=x.get("class",[])
        if "entry-date" in c: classes.append("date")
        elif "section-number" in c: classes.append("section")
        else: classes.append("p")
    return {"count":len(ps),"classes":classes}

paragraph_groups=[]

# Sweater
for ch in range(1,13):
    vals={}
    for lang in ("en","fr","ja"):
        vals[lang]=p_signature(f"sweater/{lang}/chapter-{ch:02d}/index.html",".sweater-prose")
    paragraph_groups.append(("Sweater",f"chapter-{ch:02d}",vals))

# Scarecrow
for ch in range(1,5):
    vals={}
    for lang in ("en","fr","ja","ko"):
        vals[lang]=p_signature(f"scarecrow-distance/{lang}/chapter-{ch:02d}/index.html",".scarecrow-prose")
    paragraph_groups.append(("Scarecrow",f"chapter-{ch:02d}",vals))

# Short stories by actual work dirs
ssroot=ROOT/"short-stories"
if ssroot.exists():
    for work in sorted([x.name for x in ssroot.iterdir() if x.is_dir()]):
        vals={}
        for lang in ("en","fr","ja","ko"):
            vals[lang]=p_signature(f"short-stories/{work}/{lang}/index.html",".short-story-prose")
        if any(vals.values()): paragraph_groups.append(("ShortStory",work,vals))

# Galactic existing parallel entries
for part in range(1,4):
    for ent in range(1,17):
        vals={}
        for lang in ("en","fr","ja","ko"):
            vals[lang]=p_signature(f"a-dictionary-of-galactic-extinction/{lang}/part-{part:02d}/entry-{ent:02d}/index.html",".galactic-prose")
        present={k:v for k,v in vals.items() if v}
        if len(present)>=2: paragraph_groups.append(("Galactic",f"part-{part:02d}/entry-{ent:02d}",vals))

para_mismatches=[]
for work,item,vals in paragraph_groups:
    present={k:v for k,v in vals.items() if v}
    counts={k:v["count"] for k,v in present.items()}
    if len(set(counts.values()))>1:
        para_mismatches.append((work,item,counts))

# Intended titles
title_checks=[]
fixed={
  "sweater/en/index.html":"Sweater",
  "sweater/fr/index.html":"Le Pull",
  "sweater/ja/index.html":"セーター",
  "scarecrow-distance/en/index.html":"Scarecrow Distance",
  "scarecrow-distance/fr/index.html":"Mal reçu",
  "scarecrow-distance/ja/index.html":"案山子の距離",
  "scarecrow-distance/ko/index.html":"소실점",
}
for path,want in fixed.items():
    p=ROOT/path
    if p.exists():
        soup=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
        h1=soup.find("h1")
        got=h1.get_text(" ",strip=True) if h1 else ""
        if want not in got: title_checks.append((path,got,want))

# Specific rules
rule_issues=[]
pub=(ROOT/"publication-log/index.html")
if pub.exists():
    txt=BeautifulSoup(pub.read_text(encoding="utf-8"),"html.parser").get_text(" ",strip=True)
    if "Gray Note" in txt: rule_issues.append(("Publication Log","Gray Note appears but should not be logged"))
# haiku burger king exact phrase presence somewhere Japanese haiku pages
ja_haiku=" ".join(p.read_text(encoding="utf-8",errors="ignore") for p in ROOT.glob("haiku/**/*.html"))
if ja_haiku and "バーガーキング" not in ja_haiku:
    rule_issues.append(("Haiku","バーガーキング not found in Japanese haiku corpus"))
# scarecrow banned framing words in homepage/landing descriptions only
for path in ["index.html","scarecrow-distance/index.html","scarecrow-distance/en/index.html","scarecrow-distance/fr/index.html","scarecrow-distance/ja/index.html","scarecrow-distance/ko/index.html"]:
    p=ROOT/path
    if p.exists():
        txt=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser").get_text(" ",strip=True)
        bad=[]
        for word in ["road trip","journey","adventure"]:
            if re.search(r"\b"+re.escape(word)+r"\b",txt,re.I): bad.append(word)
        if bad: rule_issues.append((path,"banned framing: "+", ".join(bad)))

# CSS core
css=(ROOT/"assets/style.css").read_text(encoding="utf-8")
css_checks={}
for cls in ["short-story-prose","galactic-prose","sweater-prose","scarecrow-prose","children-prose"]:
    m=re.search(r"\."+re.escape(cls)+r" p\s*\{([^}]*)\}",css,re.S)
    css_checks[cls]=m.group(1).strip() if m else "MISSING"

# Downloads page links
download_issues=[]
dp=ROOT/"downloads/index.html"
if dp.exists():
    soup=BeautifulSoup(dp.read_text(encoding="utf-8"),"html.parser")
    for a in soup.find_all("a",href=True):
        href=a["href"]
        if href.lower().endswith((".pdf",".epub")):
            cand=resolve_href(dp,href)
            if cand not in all_files: download_issues.append((href,cand))

# sitemap rough coverage
sitemap=(ROOT/"sitemap.xml").read_text(encoding="utf-8") if (ROOT/"sitemap.xml").exists() else ""
sitemap_missing=[]
for p in html_files:
    sp=p.as_posix()
    # Skip source-only utility pages if clearly not indexed? record only pages with canonical
    soup=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
    can=soup.find("link",rel=lambda v:v and "canonical" in v)
    if can:
        url=can.get("href","")
        if url and url not in sitemap:
            sitemap_missing.append((sp,url))

report={
 "summary":{
   "public_html_pages":len(html_files),
   "broken_internal_links":len(broken),
   "canonical_issues":len(canon_issues),
   "hreflang_issues":len(hreflang_issues),
   "seo_missing":len(seo_missing),
   "prose_class_issues":len(prose_class_issues),
   "paragraph_mismatch_groups":len(para_mismatches),
   "download_issues":len(download_issues),
   "sitemap_missing":len(sitemap_missing),
   "suspicious_editorial_artifacts":len(suspicious),
   "rule_issues":len(rule_issues),
 },
 "broken_internal_links":broken[:200],
 "canonical_issues":canon_issues[:100],
 "hreflang_issues":hreflang_issues[:100],
 "seo_missing":seo_missing[:100],
 "prose_class_issues":prose_class_issues[:100],
 "paragraph_mismatches":para_mismatches,
 "title_checks":title_checks,
 "rule_issues":rule_issues,
 "download_issues":download_issues,
 "sitemap_missing":sitemap_missing[:200],
 "suspicious":suspicious[:100],
 "css_checks":css_checks,
}
Path("tools/site-audit-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report["summary"],ensure_ascii=False,indent=2))
print("PARAGRAPH MISMATCHES")
for x in para_mismatches: print(x)
print("RULE ISSUES",rule_issues)
