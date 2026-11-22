#!/usr/bin/env python3
"""one-off: read the OLD owner-kit / claude-montage-fx pages into specs (text only) for the new kit design."""
import json, re, pathlib
from bs4 import BeautifulSoup
R = pathlib.Path(__file__).resolve().parents[1]
def soup(n): return BeautifulSoup((R/n/'index.html').read_text(encoding='utf8'),'html.parser')
def txt(e): return re.sub(r'\s+',' ',e.get_text(' ',strip=True)) if e else ''

# ---- owner-kit
b = soup('owner-kit'); sites=[]
for a in b.select('article.pc'):
    site=a.select_one('a.site'); 
    steps=[(txt(st.select_one('.s-ar')),txt(st.select_one('.s-en'))) for st in a.select('.flow .st')]
    prompts=[]
    labs=a.find_all('div',class_='lab')
    raws=a.select('textarea.raw')
    boxes=a.select('.box')
    plabs=[txt(l) for l in labs][2:]  # after 'أقوى شي فيه' + 'شلون تستخدمه'
    for i,r in enumerate(raws):
        prompts.append({'label':plabs[i] if i<len(plabs) else '', 'text':r.get_text().strip()})
    sites.append({'name':txt(site.select_one('.nm')),'url':site['href'],'headline':txt(a.select_one('.hl')),
      'who':[txt(w) for w in a.select('.who .w')],'bullets':[txt(l) for l in a.select('.ex li')],'steps':steps,'prompts':prompts,
      'go':txt(a.select_one('a.go')) if a.select_one('a.go') else ''})
json.dump(sites,open('specs/owner-kit.sites.json','w'),ensure_ascii=False,indent=1)
print('owner',len(sites),[len(s['prompts']) for s in sites],[len(s['steps']) for s in sites])

# ---- montage
m = soup('claude-montage-fx'); cards=[]
for a in m.select('article.pc'):
    t=a.select_one('h3'); go=a.select_one('a.go'); r=a.select_one('textarea.raw')
    hand=a.select_one('.hand span')
    cards.append({'title':txt(t),'tool':txt(a.select_one('.tl')),'hand':txt(hand),'go':(go['href'],txt(go)) if go else None,
      'text':r.get_text().strip() if r else '','sticker':txt(a.select_one('.stk')),'steps':[(txt(st.select_one('.s-ar')),txt(st.select_one('.s-en'))) for st in a.select('.flow .st')]})
guide=[txt(li.select_one('span')) for li in m.select('ol.guide')[0].select('li')]
before=[txt(li.select_one('span')) for li in m.select('section.where ol.guide li')]
hn=txt(m.select_one('section.where .hn'))
json.dump({'cards':cards,'guide':guide,'before':before,'note':hn},open('specs/montage.raw.json','w'),ensure_ascii=False,indent=1)
print('montage',len(cards),guide,before)
