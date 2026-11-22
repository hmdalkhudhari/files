#!/usr/bin/env python3
"""Preview: profile bar on top + real tabs for owner-kit and claude-montage-fx (AR + EN steps)."""
import re, pathlib, html
R = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
PHOTO = (R/'file-page-kit/photo.b64').read_text().strip()
BAR_CSS = """
.bar{background:#fff;border-bottom:1px solid #E4E2DC;position:sticky;top:0;z-index:30}
.bar .wrap{display:flex;align-items:center;justify-content:space-between;height:56px}
.bar .me{display:flex;align-items:center;gap:10px;text-decoration:none;color:#1E2A66;font-weight:800;font-family:'Tajawal',system-ui,sans-serif}
.bar .me img{border-radius:50%;object-fit:cover}
.bar .menu{position:relative}.bar .menu summary{list-style:none;cursor:pointer;font-size:24px;line-height:1;padding:6px 10px;color:#1E2A66}
.bar .menu summary::-webkit-details-marker{display:none}
.bar .mp{position:absolute;left:0;top:42px;min-width:170px;background:#fff;border:1px solid #E4E2DC;border-radius:12px;box-shadow:0 8px 24px rgba(30,42,102,.15);padding:6px;display:grid}
.bar .mp a{padding:10px 12px;border-radius:8px;color:#1E2A66;text-decoration:none;font-weight:700;font-family:'Tajawal',system-ui,sans-serif}
.tabbar{position:sticky;top:56px;z-index:20;background:#F6F5F1;border-bottom:1px solid #E4E2DC;margin:0 -16px;padding:0 16px}
.tabs{display:flex;gap:8px;overflow-x:auto;padding-block:10px;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tabs button{flex:none;display:flex;align-items:center;gap:7px;background:#fff;border:1px solid #E4E2DC;border-radius:999px;padding:6px 14px 6px 8px;color:#1E2A66;font:700 14px 'Tajawal',system-ui,sans-serif;cursor:pointer;direction:ltr}
.tabs button img{width:22px;height:22px;border-radius:6px;object-fit:contain}
.tabs button[aria-selected=true]{background:#1E2A66;border-color:#1E2A66;color:#fff}
.tabs button.ar{direction:rtl;padding:6px 16px}
.pc.off{display:none}
.en2{display:block;direction:ltr;text-align:left;font:600 13.5px 'Inter',system-ui,sans-serif;color:#5B5F73;margin-top:3px}
.guide .en2{color:#5B5F73}
.tabnote{margin:10px 0 0;color:#5B5F73;font-size:14px}
"""
BAR = f'''<nav class="bar"><div class="wrap"><a class="me" href="https://www.instagram.com/hmdalkhudhari/"><img src="data:image/jpeg;base64,{PHOTO}" alt="حمد الخضري" width="36" height="36"><b>حمد الخضري</b></a>
<details class="menu"><summary aria-label="القائمة">☰</summary><div class="mp"><a href="https://www.instagram.com/hmdalkhudhari/">انستقرام</a><a href="https://bznstatus.com/consult/">احجز استشارة</a></div></details></div></nav>'''
JS = """
<script>(function(){
var tabs=[].slice.call(document.querySelectorAll('.tabs button')),pcs=[].slice.call(document.querySelectorAll('article.pc'));
function show(t,keep){tabs.forEach(function(b){b.setAttribute('aria-selected',b===t)});
var ids=t.dataset.ids.split(',');pcs.forEach(function(p){p.classList.toggle('off',ids.indexOf(p.id)<0)});
if(!keep){var l=document.querySelector('.list');if(l){var y=l.getBoundingClientRect().top+scrollY-120;scrollTo({top:Math.min(y,scrollY>y?y:scrollY),behavior:'instant'})}}
var c=t.parentNode;c.scrollLeft+=t.getBoundingClientRect().left+t.offsetWidth/2-(c.getBoundingClientRect().left+c.offsetWidth/2);if(window.fit)try{fit()}catch(e){}
if(!keep&&history.replaceState)history.replaceState(null,'','#'+t.dataset.k)}
tabs.forEach(function(b){b.addEventListener('click',function(){show(b)})});
var h=location.hash.slice(1),f=tabs.filter(function(b){return b.dataset.k===h||b.dataset.ids.split(',').indexOf(h)>-1})[0]||tabs[0];show(f,true);
})();</script>"""

def common(s, body_mut):
    s = s.replace('</style>', BAR_CSS + '</style>', 1)
    s = s.replace('<body>', '<body>\n' + BAR, 1)
    s = body_mut(s)
    s = s.replace('</body>', JS + '\n</body>', 1)
    return s

# ---------- owner-kit ----------
def owner(s):
    m = re.search(r'<div class="chipwrap">.*?</div>(?=\n<section>)', s, re.S)
    nav = re.search(r'<nav class="chips" id="chips"[^>]*>(.*?)</nav>', m.group(0), re.S).group(1)
    items = re.findall(r'<a href="[^"]*"[^>]*>(<img[^>]*>)([^<]*)</a>', nav)
    btns = ''.join(f'<button type="button" role="tab" data-k="p{i}" data-ids="p{i}" aria-selected="false">{img}{html.escape(t)}</button>' for i,(img,t) in enumerate(items,1))
    new = f'<div class="tabbar"><div class="tabs" role="tablist" aria-label="المواقع">{btns}</div></div>'
    s = s.replace(m.group(0), new, 1)
    return s
# ---------- montage ----------
EN = {
 'ثبّت Claude Code: ماك':'Install Claude Code: Mac','ثبّت Claude Code: ويندوز':'Install Claude Code: Windows',
 'وبعدها: افتح مجلد الفيديو':'Then: open your video folder','جهّز المونتير (أول مرة بس)':'Set up the editor (first time only)',
 '/logo-orbit':'logos orbiting your shoulders','/claude-beside-me':'a Claude window pops out behind your head',
 '/typewriter-cut':'pages swap, one word stays fixed','/growth-chart':'3D bars and a counter','/before-after':'before and after with a wipe line',
 '/pixel-title':'a title made of dots','/reel-fan':'your reels fan out around your head','/grid-dive':'pull back to a grid wall and dive in',
 '/title-orbit':'your words orbit your head','/portal':'a portal opens behind you','/clone-room':'two copies of you','/cube-spin':'the screen spins as a cube',
 '/shatter':'the screen shatters','/head-pop-out':'your head pops above the card','/zoom-through':'fly through the words','/depth-ui':'order cards around you',
 '/apple-ui-toggles':'steps flip one by one','/liquid-glass-graph':'a glass card with a number and a chart','/phone-fan':'phones showing your clips',
 '/spotlight':'everything dims except you','/ribbon-wrap':'your business name wraps around you','/pull-back-reveal':'the whole video inside a phone'}
GUIDE_EN = ['Install Claude Code and put your video in a folder (items 1 to 3).','Paste the "set up the editor" message once (item 4).','Pick any effect, edit the yellow words, and paste it.']
BEFORE_EN = ['You need Claude Code on your computer, with a Claude plan (Pro or above) or a Claude Console account.','Film head and shoulders, leave space above your head; a plain background cuts out best.','Claude works on files on your computer and the video never leaves it. The first time takes a few minutes to set up the tools.']
def montage(s):
    n_all = len(re.findall(r'<article class="pc', s))
    def tabs():
        a = ','.join(f'p{i}' for i in range(0,4)); b = ','.join(f'p{i}' for i in range(4,n_all))
        return ('<div class="tabbar"><div class="tabs" role="tablist" aria-label="الأقسام">'
          f'<button class="ar" type="button" role="tab" data-k="setup" data-ids="{a}" aria-selected="false">١. التجهيز · Setup</button>'
          f'<button class="ar" type="button" role="tab" data-k="effects" data-ids="{b}" aria-selected="false">٢. التأثيرات · Effects ({n_all-4})</button></div></div>')
    s = re.sub(r'<nav class="chips" aria-label="الأدوات">.*?</nav>', tabs(), s, count=1, flags=re.S)
    # english lines for titles
    def h3(m):
        t = m.group(1); key = t.split(' · ')[0].strip()
        en = EN.get(key) or EN.get(t)
        full = f'{key}: {en}' if key.startswith('/') and en else en
        return f'<h3>{t}</h3>' + (f'<span class="en2">{html.escape(full or "")}</span>' if en else '')
    s = re.sub(r'<h3>(.*?)</h3>', h3, s)
    # english under guide steps
    def guide(block, en):
        it = iter(en)
        return re.sub(r'(<li><b>\d</b><span>.*?)(</span></li>)', lambda m: m.group(1)+f'<span class="en2">{html.escape(next(it))}</span>'+m.group(2), block, flags=re.S)
    g = re.search(r'(<ol class="guide">.*?</ol>)', s, re.S)
    s = s.replace(g.group(1), guide(g.group(1), GUIDE_EN), 1)
    w = re.search(r'(<section class="where">.*?<ol class="guide">.*?</ol>)', s, re.S)
    s = s.replace(w.group(1), guide(w.group(1), BEFORE_EN), 1)
    return s

for name, fn in (('owner-kit', owner), ('claude-montage-fx', montage)):
    src = (R/name/'index.html').read_text(encoding='utf8')
    d = OUT/name; d.mkdir(exist_ok=True)
    (d/'index.html').write_text(common(src, fn), encoding='utf8')
    print('wrote', d/'index.html')
