from pathlib import Path
import zipfile, tempfile, os, shutil

ROOT=Path.cwd()
FILES=[
    {
        'lang':'ko',
        'path':ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/ko/a-dictionary-of-galactic-extinction-part-01-ko-20260929-ver-001.epub',
        'old':'웜홀은 가장 예비 장치였다.',
        'new':'웜홀은 가장 중요한 예비 장치였다.'
    },
    {
        'lang':'en',
        'path':ROOT/'assets/downloads/a-dictionary-of-galactic-extinction/part-01/en/a-dictionary-of-galactic-extinction-part-01-en-20260929-ver-001.epub',
        'old':'Wormholes were the ultimate backup systems.',
        'new':'Wormholes were the most important backup systems.'
    }
]

def patch_epub(item):
    path=item['path']; old=item['old']; new=item['new']; lang=item['lang']
    with zipfile.ZipFile(path,'r') as z:
        names=z.namelist()
        if not names or names[0] != 'mimetype':
            raise RuntimeError(f'{lang}: mimetype is not first')
        before={name:z.read(name) for name in names}
        target='EPUB/Text/entry-05.xhtml'
        if target not in before:
            raise RuntimeError(f'{lang}: {target} missing')
        text=before[target].decode('utf-8')
        if text.count(old)!=1:
            raise RuntimeError(f'{lang}: old sentence count {text.count(old)}')
        if new in text:
            raise RuntimeError(f'{lang}: new sentence already present')
        after_target=text.replace(old,new,1).encode('utf-8')

    tmp=path.with_suffix('.tmp.epub')
    with zipfile.ZipFile(tmp,'w') as out:
        for i,name in enumerate(names):
            zi=None
            with zipfile.ZipFile(path,'r') as src:
                src_info=src.getinfo(name)
                zi=zipfile.ZipInfo(filename=src_info.filename,date_time=src_info.date_time)
                zi.comment=src_info.comment
                zi.extra=src_info.extra
                zi.internal_attr=src_info.internal_attr
                zi.external_attr=src_info.external_attr
                zi.create_system=src_info.create_system
                zi.create_version=src_info.create_version
                zi.extract_version=src_info.extract_version
                zi.flag_bits=src_info.flag_bits
                zi.volume=src_info.volume
            data=after_target if name==target else before[name]
            if name=='mimetype':
                zi.compress_type=zipfile.ZIP_STORED
            else:
                zi.compress_type=zipfile.ZIP_DEFLATED
            out.writestr(zi,data)

    # validate new archive
    with zipfile.ZipFile(tmp,'r') as z:
        assert z.testzip() is None
        assert z.namelist()==names
        assert z.getinfo('mimetype').compress_type==zipfile.ZIP_STORED
        after={name:z.read(name) for name in names}
        changed=[name for name in names if before[name]!=after[name]]
        assert changed==[target], (lang,changed)
        t=after[target].decode('utf-8')
        assert t.count(old)==0
        assert t.count(new)==1
        assert after['mimetype']==b'application/epub+zip'
    tmp.replace(path)
    print(f'{lang}: changed={target}, old=0, new=1, files={len(names)}')

for item in FILES:
    patch_epub(item)
