from pathlib import Path
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from bs4 import BeautifulSoup
import tempfile, shutil, re, hashlib

ROOT=Path(".")
EPUB=ROOT/"assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.epub"
tmp=Path(tempfile.mkdtemp(prefix="lepull_epub_"))
with ZipFile(EPUB,"r") as z:
    z.extractall(tmp)

def web_inner(ch):
    p=ROOT/f"sweater/fr/chapter-{ch:02d}/index.html"
    soup=BeautifulSoup(p.read_text(encoding="utf-8"),"html.parser")
    box=soup.select_one(".sweater-prose")
    if box is None:
        raise RuntimeError(f"missing sweater-prose in {p}")
    return box.decode_contents()

def norm_text(soupish):
    if isinstance(soupish,str):
        soup=BeautifulSoup(soupish,"html.parser")
    else:
        soup=soupish
    return re.sub(r"\s+"," ",soup.get_text(" ",strip=True)).strip()

report=[]
for ch in range(1,13):
    xp=tmp/f"EPUB/Text/chapter-{ch:02d}.xhtml"
    raw=xp.read_text(encoding="utf-8")
    soup=BeautifulSoup(raw,"xml")
    sec=soup.find("section",class_=lambda x:x and "chapter-heading" in x)
    if sec is None:
        raise RuntimeError(f"chapter section missing {xp}")
    h1=sec.find("h1")
    if h1 is None:
        raise RuntimeError(f"h1 missing {xp}")

    # Remove only the old body content after the preserved chapter heading.
    for node in list(h1.next_siblings):
        node.extract()

    frag=BeautifulSoup(web_inner(ch),"html.parser")
    for node in list(frag.contents):
        sec.append(node)

    new='<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'+str(soup.html)
    xp.write_text(new,encoding="utf-8")

    # Exact text-content invariant against current web prose.
    xsoup=BeautifulSoup(new,"html.parser")
    xsec=xsoup.find("section",class_=lambda x:x and "chapter-heading" in x)
    xh1=xsec.find("h1")
    epub_body=" ".join(str(n) for n in list(xh1.next_siblings))
    web=web_inner(ch)
    if norm_text(epub_body)!=norm_text(web):
        raise RuntimeError(f"text mismatch after rebuild ch{ch:02d}")
    ep_count=len(BeautifulSoup(epub_body,"html.parser").find_all("p"))
    web_count=len(BeautifulSoup(web,"html.parser").find_all("p"))
    if ep_count!=web_count:
        raise RuntimeError(f"paragraph count mismatch ch{ch:02d}: epub={ep_count} web={web_count}")
    report.append((ch,web_count))

# Keep the existing EPUB package, metadata, title, copyright, TOC and stylesheet intact.
# Repackage with EPUB-required mimetype first and uncompressed.
out=EPUB.with_suffix(".epub.new")
with ZipFile(out,"w") as z:
    mt=tmp/"mimetype"
    z.write(mt,"mimetype",compress_type=ZIP_STORED)
    for p in sorted(tmp.rglob("*")):
        if p.is_dir() or p==mt:
            continue
        z.write(p,p.relative_to(tmp).as_posix(),compress_type=ZIP_DEFLATED)

with ZipFile(out,"r") as z:
    first=z.infolist()[0]
    if first.filename!="mimetype" or first.compress_type!=ZIP_STORED:
        raise RuntimeError("invalid EPUB mimetype packaging")
    for ch,count in report:
        name=f"EPUB/Text/chapter-{ch:02d}.xhtml"
        s=BeautifulSoup(z.read(name).decode("utf-8"),"html.parser")
        sec=s.find("section",class_=lambda x:x and "chapter-heading" in x)
        h1=sec.find("h1")
        body=" ".join(str(n) for n in list(h1.next_siblings))
        if len(BeautifulSoup(body,"html.parser").find_all("p"))!=count:
            raise RuntimeError(f"final zip paragraph check failed ch{ch:02d}")

out.replace(EPUB)
print("Rebuilt", EPUB)
print("Size", EPUB.stat().st_size)
print("SHA256", hashlib.sha256(EPUB.read_bytes()).hexdigest())
for ch,count in report:
    print(f"CH{ch:02d}: {count} paragraphs")
