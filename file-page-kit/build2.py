#!/usr/bin/env python3
"""New-design builder for owner-kit and claude-montage-fx: kit style, profile bar, 'jump to a section' menu (like the reference), AR+EN steps.
usage: python3 build2.py   -> writes ../preview/file-kit-v2/{owner-kit,claude-montage-fx}/index.html"""
import json, re, html, pathlib
H = pathlib.Path(__file__).parent; ROOT = H.parent; OUT = ROOT/'preview/file-kit-v2'
E_ = lambda s: html.escape(s, quote=True)
CSS = (H/'style.css').read_text(encoding='utf8')
PHOTO = (H/'photo.b64').read_text().strip()
LOGO = ".logo{width:150px;height:42px;margin:0 auto 4px;background:url('data:image/png;base64,"+(H/'logo-navy.b64').read_text().strip()+"') center/contain no-repeat}"
CSS = CSS.replace(re.search(r"\.logo\{[^}]*\}", CSS).group(0), LOGO)
CSS += """
.jump{position:sticky;top:56px;z-index:4;background:#fff;border-bottom:1px solid var(--line);padding:10px 0}
.jump select{width:100%;font:800 15px 'Tajawal',sans-serif;color:var(--navy);background:#F4F5FA;border:1px solid var(--line);border-radius:12px;padding:10px 12px}
section{scroll-margin-top:120px}
.who{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.who span{background:#F1F0EC;border-radius:999px;font-size:12.5px;font-weight:700;color:var(--soft);padding:2px 10px}
.hl{margin:10px 0 0;font-size:17px;font-weight:800;line-height:1.5}
.bul{margin:8px 0 0;color:var(--soft);font-size:14.5px}
.lab{margin:16px 0 6px;font-weight:800;font-size:14px;color:var(--navy);border-inline-start:4px solid var(--y);padding-inline-start:8px}
.stp{display:grid;grid-template-columns:30px minmax(0,1fr) 1px minmax(0,1fr);gap:0 10px;align-items:center;padding:8px 0;border-top:1px solid var(--line)}
.stp:first-of-type{border-top:0}
.stp .n{width:26px;height:26px;font-size:13px}.stp .a{font-weight:700;font-size:15px}.stp .e{font-family:var(--fl);font-size:13px;color:var(--soft);text-align:left;font-weight:500;line-height:1.45}
.stp i{align-self:stretch;background:var(--line)}
.go{display:block;margin-top:12px;font-weight:800;color:var(--navy);text-decoration:none;border:1.5px solid var(--navy);border-radius:12px;padding:9px;text-align:center}
.card h3.s{font-family:'Tajawal',sans-serif;font-size:19px}
.en2{display:block;direction:ltr;text-align:left;font:600 13.5px var(--fl);color:var(--soft);margin-top:2px}
.tg{display:inline-block;font-size:12px;font-weight:800;background:var(--y);color:var(--navy);border-radius:999px;padding:1px 10px}
.eff{display:flex;align-items:center;gap:10px}.eff .t{flex:1;min-width:0}
.eff b.t1{display:block;font-family:var(--fl);font-size:16px;color:var(--navy)}
"""
CP = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>'
BAR = f'''<nav class="bar"><div class="wrap"><a class="me" href="https://www.instagram.com/hmdalkhudhari/"><img src="data:image/jpeg;base64,{PHOTO}" alt="حمد الخضري" width="36" height="36"><b>حمد الخضري</b></a>
<details class="menu"><summary aria-label="القائمة">☰</summary><div class="mp"><a href="https://www.instagram.com/hmdalkhudhari/">انستقرام</a><a href="https://bznstatus.com/consult/">احجز استشارة</a></div></details></div></nav>'''
JS = """<script>
document.querySelectorAll('.cp').forEach(b=>b.onclick=async()=>{const t=b.dataset.t;try{await navigator.clipboard.writeText(t)}catch(e){const x=document.createElement('textarea');x.value=t;document.body.appendChild(x);x.select();document.execCommand('copy');x.remove()}const l=b.querySelector('span'),o=l.textContent;b.classList.add('ok');l.textContent='انتسخ ✓';setTimeout(()=>{b.classList.remove('ok');l.textContent=o},1600)});
document.querySelectorAll('.mo').forEach(m=>{const pr=m.previousElementSibling,p=pr.querySelector('p');if(p.scrollHeight<=p.clientHeight+2){m.hidden=true;return}m.onclick=()=>{const o=pr.classList.toggle('open');m.textContent=o?'صغّره ▴':'اعرض كامل ▾'}});
const j=document.getElementById('jump');if(j)j.onchange=()=>{const s=document.getElementById(j.value);if(s)s.scrollIntoView({behavior:'auto'});j.selectedIndex=0};
</script>"""

def pbox(text, code=False):
    return (f'<div class="pr{" code" if code else ""}"><p dir="auto">{"<br>".join(E_(l) for l in text.split(chr(10)))}</p>'
            f'<button class="cp" type="button" data-t="{E_(text)}">{CP}<span>نسخ</span></button></div><button class="mo" type="button">اعرض كامل ▾</button>')
def steps(rows):
    return ''.join(f'<div class="stp"><b class="n">{i}</b><span class="a">{E_(a)}</span><i></i><span class="e" dir="ltr">{E_(e)}</span></div>' for i,(a,e) in enumerate(rows,1))
AR = lambda n: str(n).translate(str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩'))

def page(title, kicker, h1, sub, sects, body_sections, fine, extra_top=''):
    opts = ''.join(f'<option value="{i}">{E_(t)}</option>' for i,t in sects)
    return f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E_(title)} | حمد الخضري</title><meta property="og:title" content="{E_(title)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{BAR}
<header><div class="wrap">
<div class="logo" role="img" aria-label="Hamad Alkhudhari"></div><div class="tag">Business &amp; AI</div>
<span class="kick">{E_(kicker)}</span>
<h1>{h1}</h1><p>{E_(sub)}</p>
<a class="gl" href="https://bznstatus.com/consult/"><b>لكم خصم خاص<i>٢٥٪</i></b><span>اضغط هنا ←</span></a>
</div></header>
<div class="jump"><div class="wrap"><select id="jump" aria-label="قفز لقسم"><option>قفز لقسم ↓ ({len(sects)})</option>{opts}</select></div></div>
<main class="wrap">{body_sections}</main>
<footer><div class="wrap">
<h2>جربها وعطني رايك</h2><p>كل يوم أنزل شي جديد بالبزنس والـAI.</p>
<div class="btns"><a class="btn ig" href="https://www.instagram.com/hmdalkhudhari/">تابعني بانستقرام</a><a class="btn wa" href="https://wa.me/message/D6QAVYNNKNQZA1">كلمني واتساب</a></div>
<p class="fine">{E_(fine)}</p></div></footer>
{JS}</body></html>'''

# ---------------- owner-kit ----------------
sites = json.load(open(H/'specs/owner-kit.sites.json'))
secs=[]; body=''
for i,s in enumerate(sites,1):
    sid=f's{i}'; secs.append((sid, f'{AR(i)}. {s["name"]}'))
    pr=''.join(f'<div class="lab">{E_(p["label"])}</div>{pbox(p["text"])}<p class="hint">بدّل اللي بين [ ] بمعلوماتك.</p>' for p in s['prompts'])
    body+=(f'<section id="{sid}"><h2>{AR(i)}. {E_(s["name"])}</h2><div class="card">'
      f'<h3 class="hl" style="font-family:Tajawal;text-align:right">{E_(s["headline"])}</h3>'
      f'<div class="who">{"".join(f"<span>{E_(w)}</span>" for w in s["who"])}</div>'
      f'<p class="bul">{E_(" ".join(s["bullets"]))}</p>'
      f'<div class="lab">شلون تستخدمه · How to use it</div>{steps(s["steps"])}{pr}'
      f'<a class="go" href="{E_(s["url"])}" target="_blank" rel="noopener">{E_(s["go"] or "افتح الموقع ←")}</a></div></section>')
owner = page('هدية الـ٤٠ ألف: خزينة ١٠ مواقع','هدية الـ40,000 متابع','خزينة <em>١٠ مواقع</em> تحتاجها',
  'شكراً على الـ٤٠ ألف. ١٠ مواقع أستخدمها فعلاً، لكل واحد خطوات (عربي وإنجليزي) وبرومبت جاهز.',secs,
  '<p class="lead" style="margin-top:22px">ابدأ بالأول. ٨ منها مجانية. اختر الموقع من القائمة فوق.</p>'+body,
  'الخطوات من المواقع نفسها. © حمد الخضري @hmdalkhudhari')

# ---------------- montage ----------------
raw = json.load(open(H/'specs/montage.raw.json'))
EN = {'ثبّت Claude Code: ماك':'Install Claude Code: Mac','ثبّت Claude Code: ويندوز':'Install Claude Code: Windows','وبعدها: افتح مجلد الفيديو':'Then: open your video folder','جهّز المونتير (أول مرة بس)':'Set up the editor (first time only)',
 '/logo-orbit':'logos orbiting your shoulders','/claude-beside-me':'a Claude window pops out behind your head','/typewriter-cut':'pages swap, one word stays fixed','/growth-chart':'3D bars and a counter','/before-after':'before and after with a wipe line','/pixel-title':'a title made of dots','/reel-fan':'your reels fan out around your head','/grid-dive':'pull back to a grid wall and dive in','/title-orbit':'your words orbit your head','/portal':'a portal opens behind you','/clone-room':'two copies of you','/cube-spin':'the screen spins as a cube','/shatter':'the screen shatters','/head-pop-out':'your head pops above the card','/zoom-through':'fly through the words','/depth-ui':'order cards around you','/apple-ui-toggles':'steps flip one by one','/liquid-glass-graph':'a glass card with a number and a chart','/phone-fan':'phones showing your clips','/spotlight':'everything dims except you','/ribbon-wrap':'your business name wraps around you','/pull-back-reveal':'the whole video inside a phone'}
GEN = ['Install Claude Code and put your video in a folder (items 1 to 3).','Paste the "set up the editor" message once (item 4).','Pick any effect, edit the yellow words, and paste it.']
BEF = ['You need Claude Code on your computer, with a Claude plan (Pro or above) or a Claude Console account.','Film head and shoulders, leave space above your head; a plain background cuts out best.','Claude works on files on your computer and the video never leaves it. The first time takes a few minutes to set up the tools.']
def mcard(i,c):
    key=c['title'].split(' · ')[0].strip(); en=EN.get(key,'')
    code = i<3
    if c.get('steps'): cmd = steps(c['steps'])
    elif code: cmd = f'<div class="pr code"><p dir="ltr">{E_(c["text"])}</p><button class="cp" type="button" data-t="{E_(c["text"])}">{CP}<span>نسخ</span></button></div>'
    else: cmd = pbox(c['text'])
    hand = f'<p class="hint">{E_(c["hand"])}</p>' if c['hand'] else ''
    go = f'<a class="go" href="{E_(c["go"][0])}" target="_blank" rel="noopener">{E_(c["go"][1])}</a>' if c['go'] else ''
    return (f'<li class="card"><div class="top"><b class="n">{i+1}</b><h3 class="s">{E_(c["title"])}</h3></div>'
            f'{"<span class=en2>"+E_(en)+"</span>" if en else ""}{hand}{cmd}{go}</li>')
def lst(ar,en): return '<ol>'+''.join(f'<li class="card"><div class="bi"><span class="a">{E_(a)}</span><span class="e" dir="ltr">{E_(e)}</span></div></li>' for a,e in zip(ar,en))+'</ol>'
secs=[('how','١. شلون تستخدم الملف · How it works'),('before','٢. قبل لا تبدأ · Before you start'),('setup','٣. التجهيز · Setup'),('fx','٤. التأثيرات الـ٢٢ · The 22 effects')]
n=len(raw['cards'])
body=(f'<section id="how"><h2>شلون تستخدم هالملف؟</h2>{lst(raw["guide"],GEN)}</section>'
 f'<section id="before"><h2>قبل لا تبدأ: ٣ أشياء</h2>{lst(raw["before"],BEF)}<p class="hint">{E_(raw["note"])}</p></section>'
 f'<section id="setup"><h2>التجهيز (مرة وحدة)</h2><p class="lead">الأوامر ١ إلى ٣ حسب جهازك، و٤ للمونتير.</p><ol>{"".join(mcard(i,c) for i,c in enumerate(raw["cards"][:4]))}</ol></section>'
 f'<section id="fx"><h2>التأثيرات: سطر واحد لكل تأثير</h2><p class="lead">الكلام بين [ ] فراغ: امسحه واكتب معلومة مشروعك مكانه.</p><ol>{"".join(mcard(i,c) for i,c in enumerate(raw["cards"][4:],4))}</ol></section>')
mont = page('لا تدفع للمونتير: ٢٢ تأثير بسطر واحد','ملف مجاني','لا تدفع للمونتير: <em>٢٢ تأثير بسطر واحد</em>',
  'كل تأثير سطر تلصقه بـClaude Code ويمنتج فيديوك. بدون برنامج مونتاج.',secs,body,
  'طريقة التثبيت من code.claude.com/docs. التأثيرات جربناها كلها على فيديو حقيقي قبل لا نرسلها.')
for name,pg in (('owner-kit',owner),('claude-montage-fx',mont)):
    d=OUT/name; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(pg,encoding='utf8'); print('wrote',d/'index.html',len(pg))
