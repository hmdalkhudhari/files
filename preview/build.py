import re, shutil, os
ROOT='/home/user/files'; OUT=f'{ROOT}/preview'
PAGES={'home':'site','consult':'consult','system':'system','kit':'media-kit'}
FONT='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap">'
for page,src in PAGES.items():
    d=f'{OUT}/{page}'; os.makedirs(d,exist_ok=True)
    s=open(f'{ROOT}/{src}/index.html',encoding='utf-8').read()
    V=str(int(__import__('time').time()))
    inject=FONT+'<link rel="stylesheet" href="../assets/ideas.css?v='+V+'"><meta name="robots" content="noindex">'
    s=re.sub(r'</head>', inject+'</head>', s, count=1)
    s=re.sub(r'</body>', f'<script src="../assets/ideas.js?v={V}" data-page="{page}"></script></body>', s, count=1)
    # strip netlify badge script if any
    s=re.sub(r'<script[^>]*netlify[^>]*>.*?</script>','',s,flags=re.S|re.I)
    # home: links to ../site/ -> ../home/
    s=s.replace('href="../site/"','href="../home/"')
    open(f'{d}/index.html','w',encoding='utf-8').write(s)
    if src=='media-kit':
        for f in os.listdir(f'{ROOT}/media-kit'):
            if f!='index.html' and not f.endswith('.pdf'): shutil.copy(f'{ROOT}/media-kit/{f}', f'{d}/{f}')
open(f'{OUT}/index.html','w',encoding='utf-8').write('<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=home/"><a href="home/">home</a>')
print('built')
