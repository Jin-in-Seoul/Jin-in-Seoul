from pathlib import Path
import re, json, html

ROOT=Path(".")
labels={
    "en": lambda n: f"Chapter {n}",
    "fr": lambda n: f"Chapitre {n}",
    "ja": lambda n: f"第{n}章",
    "ko": lambda n: f"{n}장",
}

def get_lang(s):
    m=re.search(r'<html[^>]*\blang="([^"]+)"',s,re.I)
    return m.group(1) if m else "en"

def get_h1(s):
    m=re.search(r'<h1(?:\s[^>]*)?>(.*?)</h1>',s,re.S|re.I)
    if not m: return None
    t=re.sub(r'<[^>]+>',' ',m.group(1))
    t=html.unescape(re.sub(r'\s+',' ',t)).strip()
    return t

def replace_meta_content(s, selector, new_content):
    pat=rf'(<meta\s+{selector}\s+content=")[^"]*(">)'
    return re.sub(pat, lambda m:m.group(1)+html.escape(new_content,quote=True)+m.group(2), s, count=1)

def replace_json_name(s, new_name):
    # only inside our JSON-LD block
    m=re.search(r'(<script type="application/ld\+json" data-seo="site">\s*)(\{.*?\})(\s*</script>)',s,re.S)
    if not m: return s
    try:
        obj=json.loads(m.group(2))
    except Exception:
        return s
    obj["name"]=new_name
    js=json.dumps(obj,ensure_ascii=False,indent=2)
    return s[:m.start(2)]+js+s[m.end(2):]

changed=[]
weak=[]
for p in ROOT.rglob("index.html"):
    if ".git" in p.parts or p.as_posix().startswith("tools/"):
        continue
    s=p.read_text(encoding="utf-8")
    h1=get_h1(s)
    if h1 and re.fullmatch(r'\d+',h1):
        weak.append(p.as_posix())
        lang=get_lang(s)
        n=int(h1)
        prefix=labels.get(lang,labels["en"])(n)

        # Replace title only when it begins with the bare numeric chapter marker.
        tm=re.search(r'<title>(.*?)</title>',s,re.S|re.I)
        if tm:
            old_title=html.unescape(re.sub(r'<[^>]+>',' ',tm.group(1))).strip()
            new_title=re.sub(r'^\d+\s*-\s*',prefix+" - ",old_title,count=1)
            if new_title==old_title:
                new_title=f"{prefix} - {old_title}"
            s=s[:tm.start(1)]+html.escape(new_title,quote=False)+s[tm.end(1):]

            # Description: replace leading bare number with localized chapter label.
            dm=re.search(r'<meta name="description" content="([^"]*)">',s,re.I)
            if dm:
                old_desc=html.unescape(dm.group(1))
                new_desc=re.sub(rf'^{n}\s*—',prefix+" —",old_desc,count=1)
                s=replace_meta_content(s,'name="description"',new_desc)

            # OG/Twitter titles should mirror improved title.
            s=replace_meta_content(s,'property="og:title"',new_title)
            s=replace_meta_content(s,'name="twitter:title"',new_title)

            # Mirror improved description into OG/Twitter descriptions if present.
            dm2=re.search(r'<meta name="description" content="([^"]*)">',s,re.I)
            if dm2:
                desc_now=html.unescape(dm2.group(1))
                s=replace_meta_content(s,'property="og:description"',desc_now)
                s=replace_meta_content(s,'name="twitter:description"',desc_now)

            s=replace_json_name(s,prefix)

            p.write_text(s,encoding="utf-8")
            changed.append((p.as_posix(),new_title,prefix))

# Validate: no HTML page should retain a bare-numeric H1 with bare-numeric SEO title/name.
errors=[]
for pth,new_title,prefix in changed:
    s=(ROOT/pth).read_text(encoding="utf-8")
    if f"<title>{html.escape(new_title,quote=False)}</title>" not in s:
        errors.append((pth,"title"))
    if f'"name": "{prefix}"' not in s:
        errors.append((pth,"jsonld name"))
    if re.search(r'<meta name="description" content="\d+\s*—',s):
        errors.append((pth,"description"))
if errors:
    raise RuntimeError(errors)

print("Weak numeric-only H1 pages found:",len(weak))
for x in weak: print(" -",x)
print("SEO metadata refined:",len(changed))
