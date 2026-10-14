#!/usr/bin/env python3
"""Read-only site quality audit: links, accessibility heuristics, asset performance."""
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,urldefrag
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from pathlib import Path
import re,xml.etree.ElementTree as ET

BASE="https://jin-in-seoul.com"; HOST="jin-in-seoul.com"; findings=[]; pages={}
def flag(level,code,url,detail): findings.append((level,code,url,str(detail).replace("|","/").replace("\n"," ")[:230]))
def get(url):
 try:
  with urlopen(Request(url,headers={"User-Agent":"Jin-in-Seoul-QualityAudit/1.0"}),timeout=18) as r:
   b=r.read(3000000); return r.status,r.url,r.headers.get("Content-Type",""),b,""
 except (HTTPError,URLError,TimeoutError,OSError,ValueError) as e: return getattr(e,"code",0),url,"",b"",str(e)
class Page(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.links=[];self.ids=set();self.images=[];self.headings=[];self.inputs=[];self.labels=set();self.buttons=[];self.lang="";self.viewport=False;self.styles=[];self.scripts=[];self.current_heading=None;self.heading_text="";self.main=0;self.skip=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);v=a.get("id");self.ids.add(v) if v else None
  if tag=="html":self.lang=a.get("lang","")
  if tag=="a":self.links.append((a.get("href",""),a.get("aria-label",""),a.get("title","")))
  if tag=="img":self.images.append(a)
  if tag in ("h1","h2","h3","h4","h5","h6"):self.current_heading=tag;self.heading_text=""
  if tag=="input":self.inputs.append(a)
  if tag=="label" and a.get("for"):self.labels.add(a["for"])
  if tag=="button":self.buttons.append(a)
  if tag=="main":self.main+=1
  if tag=="meta" and a.get("name","").lower()=="viewport":self.viewport=True
  if tag=="link" and a.get("rel","").lower()=="stylesheet":self.styles.append(a.get("href",""))
  if tag=="script" and a.get("src"):self.scripts.append(a["src"])
 def handle_data(self,data):
  if self.current_heading:self.heading_text+=data
 def handle_endtag(self,tag):
  if tag==self.current_heading:self.headings.append((tag,self.heading_text.strip()));self.current_heading=None
def inspect(url):
 status,final,ct,body,err=get(url)
 if status!=200:return url,status,final,ct,None,err
 p=Page()
 try:p.feed(body.decode("utf-8","replace"))
 except Exception as e:return url,status,final,ct,None,str(e)
 return url,status,final,ct,p,""
s,_,_,xml,_=get(BASE+"/sitemap.xml")
urls=[]
if s==200:
 try:urls=[e.text.strip() for e in ET.fromstring(xml).iter() if e.tag.rsplit("}",1)[-1]=="loc" and e.text]
 except Exception as e:flag("ERROR","SITEMAP_PARSE",BASE,str(e))
else:flag("ERROR","SITEMAP_HTTP",BASE,str(s))
with ThreadPoolExecutor(max_workers=8) as pool:
 for url,status,final,ct,p,err in pool.map(inspect,urls):
  if status!=200 or p is None:flag("ERROR","PAGE_FETCH",url,f"{status} {err}");continue
  pages[url]=p
  if not p.lang:flag("WARN","HTML_LANG",url,"Missing lang")
  if not p.viewport:flag("WARN","VIEWPORT",url,"Missing viewport meta")
  if not p.headings or not any(h=="h1" for h,_ in p.headings):flag("WARN","NO_H1",url,"No h1")
  levels=[int(h[1]) for h,_ in p.headings]
  if any(b-a>1 for a,b in zip(levels,levels[1:])):flag("INFO","HEADING_SKIP",url,"Heading level jumps")
  if len([x for x in p.headings if x[0]=="h1"])>1:flag("INFO","MULTIPLE_H1",url,"Multiple h1")
  for i,img in enumerate(p.images):
   if "alt" not in img:flag("WARN","IMAGE_ALT_MISSING",url,img.get("src","")+" (image "+str(i)+")")
  for inp in p.inputs:
   if inp.get("type","").lower() not in ("hidden","submit","button","reset") and not (inp.get("aria-label") or inp.get("aria-labelledby") or (inp.get("id") and inp["id"] in p.labels)):flag("WARN","INPUT_LABEL_MISSING",url,inp.get("id",inp.get("name","input")))
  for a in p.buttons:
   if not (a.get("aria-label") or a.get("title")):flag("INFO","BUTTON_NAME_REVIEW",url,"Button accessible name may come from content")
internal={}
for url,p in pages.items():
 for href,aria,title in p.links:
  if not href or href.startswith(("mailto:","tel:","javascript:","data:")) or href=="#":continue
  absolute=urljoin(url,href);part=urlsplit(absolute)
  if part.netloc!=HOST:continue
  key=urldefrag(absolute)[0]
  internal.setdefault(key,[]).append((url,part.fragment))
checked={}
with ThreadPoolExecutor(max_workers=8) as pool:
 for target,status,final,ct,body,err in pool.map(lambda x:(x[0],*get(x[0])),internal):
  checked[target]=(status,final,ct)
  if status>=400 or status==0:
   refs=internal[target];flag("ERROR","BROKEN_INTERNAL_LINK",refs[0][0],f"{target} HTTP {status}; references {len(refs)}")
  elif urlsplit(final).netloc!=HOST:flag("WARN","LINK_EXTERNAL_REDIRECT",internal[target][0][0],f"{target} -> {final}")
for target,refs in internal.items():
 if target not in pages:continue
 ids=pages[target].ids
 for source,fragment in refs:
  if fragment and fragment not in ids and fragment not in ("top",):
   flag("WARN","MISSING_ANCHOR",source,f"{target}#{fragment}")
assets={}
for url,p in pages.items():
 for asset in p.styles+p.scripts+[i.get("src","") for i in p.images]:
  if not asset:continue
  a=urljoin(url,asset)
  if urlsplit(a).netloc==HOST:assets.setdefault(urldefrag(a)[0],[]).append(url)
with ThreadPoolExecutor(max_workers=8) as pool:
 for asset,status,final,ct,body,err in pool.map(lambda x:(x[0],*get(x[0])),assets):
  if status!=200:flag("ERROR","ASSET_FETCH",assets[asset][0],f"{asset} HTTP {status}")
  elif len(body)>500000:flag("INFO","LARGE_ASSET",assets[asset][0],f"{asset}: at least {len(body)} bytes (3MB cap)")
counts=Counter(x[0] for x in findings)
lines=["# Site quality audit (read-only)","",f"Pages in sitemap: {len(urls)}; HTML fetched: {len(pages)}; distinct internal targets: {len(internal)}; distinct assets: {len(assets)}",f"ERROR {counts['ERROR']}, WARN {counts['WARN']}, INFO {counts['INFO']}","", "This is a static HTML and HTTP audit, **not** a browser/mobile rendering, keyboard/screen-reader, or Core Web Vitals measurement.","", "| Severity | Code | Source page | Detail |","|---|---|---|---|"]
for row in sorted(findings,key=lambda r:({"ERROR":0,"WARN":1,"INFO":2}[r[0]],r[1],r[2])):lines.append("| "+" | ".join(row)+" |")
Path("site-quality-report.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"QUALITY pages={len(pages)} links={len(internal)} assets={len(assets)} ERROR={counts['ERROR']} WARN={counts['WARN']} INFO={counts['INFO']}")
