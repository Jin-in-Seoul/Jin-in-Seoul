from pathlib import Path
from zipfile import ZipFile

ep=Path("assets/downloads/sweater/fr/le-pull-fr-20260930-ver-001.epub")
with ZipFile(ep) as z:
    names=z.namelist()
    picks=["EPUB/Text/chapter-01.xhtml","EPUB/Text/title.xhtml","EPUB/Styles/style.css","EPUB/package.opf","EPUB/nav.xhtml","EPUB/toc.ncx"]
    out=[]
    for name in picks:
        out.append(f"\n===== {name} =====\n")
        out.append(z.read(name).decode("utf-8"))
Path("tools/le-pull-epub-inspect.txt").write_text("".join(out),encoding="utf-8")
print("ok")
