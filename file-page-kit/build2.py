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
.back{display:inline-block;margin:14px 0 0;color:var(--soft);font-weight:700;font-size:14px;text-decoration:none}
.acts{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:14px}
.acts a,.acts button{display:block;text-align:center;border:1.5px solid var(--navy);background:#fff;color:var(--navy);font:800 14px 'Tajawal',sans-serif;padding:10px 4px;border-radius:12px;text-decoration:none;cursor:pointer}
.acts .cl{background:var(--y);border-color:var(--y)}
.acts .ok{background:#1FA855;color:#fff;border-color:#1FA855}
.sub{margin-top:34px;background:#F4F5FA;border:1px solid var(--line);border-radius:16px;padding:18px}
.sub h2{margin:0 0 4px;font-size:20px}.sub p{margin:0 0 12px;color:var(--soft);font-size:14.5px}
.sub input{display:block;width:100%;margin-top:8px;font:600 16px 'Tajawal',sans-serif;border:1px solid var(--line);border-radius:12px;padding:12px;background:#fff;color:var(--navy);direction:ltr;text-align:right}
.sub button{display:block;width:100%;margin-top:12px;border:0;background:var(--navy);color:#fff;font:800 16px 'Tajawal',sans-serif;padding:13px;border-radius:12px;cursor:pointer}
.sub .msg{margin-top:10px;font-weight:700;font-size:14px;color:#1FA855}
.sub .fn{font-size:12px;color:var(--soft);margin-top:8px}
@media print{.sub,.acts,.jump,.back{display:none!important}}
.hubq{width:100%;font:600 16px 'Tajawal',sans-serif;border:1px solid var(--line);border-radius:12px;padding:12px;margin-top:6px}
.chp{display:flex;gap:8px;overflow-x:auto;padding:12px 0;scrollbar-width:none}.chp button{flex:none;border:1px solid var(--line);background:#fff;color:var(--navy);font:800 14px 'Tajawal',sans-serif;padding:6px 14px;border-radius:999px;cursor:pointer}
.chp button.on{background:var(--navy);color:#fff;border-color:var(--navy)}
a.hc{display:block;text-decoration:none;color:inherit}.hc .card{display:grid;gap:4px}.hc b{font-size:17px;color:var(--navy)}.hc span.d{color:var(--soft);font-size:14px}.hc .tg{justify-self:start}
"""
CP = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>'
HUB='../../../library/'
BAR = f'''<nav class="bar"><div class="wrap"><a class="me" href="https://www.instagram.com/hmdalkhudhari/"><img src="data:image/jpeg;base64,{PHOTO}" alt="حمد الخضري" width="36" height="36"><b>حمد الخضري</b></a>
<details class="menu"><summary aria-label="القائمة">☰</summary><div class="mp"><a href="https://www.instagram.com/hmdalkhudhari/">انستقرام</a><a href="{HUB}">مكتبة الملفات المجانية</a><a href="https://bznstatus.com/consult/">احجز استشارة</a></div></details></div></nav>'''
JS = """<script>
document.querySelectorAll('.cp').forEach(b=>b.onclick=async()=>{const t=b.dataset.t;try{await navigator.clipboard.writeText(t)}catch(e){const x=document.createElement('textarea');x.value=t;document.body.appendChild(x);x.select();document.execCommand('copy');x.remove()}const l=b.querySelector('span'),o=l.textContent;b.classList.add('ok');l.textContent='انتسخ ✓';setTimeout(()=>{b.classList.remove('ok');l.textContent=o},1600)});
document.querySelectorAll('.mo').forEach(m=>{const pr=m.previousElementSibling,p=pr.querySelector('p');if(p.scrollHeight<=p.clientHeight+2){m.hidden=true;return}m.onclick=()=>{const o=pr.classList.toggle('open');m.textContent=o?'صغّره ▴':'اعرض كامل ▾'}});
const j=document.getElementById('jump');if(j)j.onchange=()=>{const s=document.getElementById(j.value);if(s)s.scrollIntoView({behavior:'auto'});j.selectedIndex=0};
var sh=document.getElementById('shr');if(sh)sh.onclick=()=>{const d={title:document.title,url:location.href.split('#')[0]};if(navigator.share)navigator.share(d).catch(()=>{});else{navigator.clipboard&&navigator.clipboard.writeText(d.url);sh.textContent='انتسخ الرابط ✓';setTimeout(()=>sh.textContent='مشاركة',1600)}};
var SUB_ENDPOINT='';
var f=document.getElementById('sub');if(f)f.onsubmit=function(e){e.preventDefault();var em=f.email.value.trim(),ph=f.phone.value.trim(),m=document.getElementById('submsg');m.hidden=false;
if(!em&&!ph){m.style.color='#C0392B';m.textContent='اكتب إيميلك أو رقمك.';return}
if(em&&!/^[^@ ]+@[^@ ]+[.][^@ ]+$/.test(em)){m.style.color='#C0392B';m.textContent='الإيميل مو صحيح.';return}
m.style.color='#1FA855';
if(!SUB_ENDPOINT){m.textContent='معاينة: الحفظ يشتغل بعد ربط الجدول.';return}
fetch(SUB_ENDPOINT,{method:'POST',mode:'no-cors',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams({kind:'subscriber',email:em,phone:ph,page:location.pathname})}).then(function(){m.textContent='تم، شكراً لك ✓';f.reset()}).catch(function(){m.style.color='#C0392B';m.textContent='صار خطأ، جرب مرة ثانية.'})};
</script>"""

BASEURL='https://hmdalkhudhari.github.io/files/'
def CPR(slug): return ('ساعدني أنفذ الخطوات اللي بهالصفحة خطوة خطوة، وانتظر مني بعد كل خطوة. اشرح لي بالعربي بشكل بسيط، وإذا علقت أرسل لك سكرين.\nHelp me follow the steps on this page one at a time and wait for me after each step. Explain in simple Arabic; if I get stuck I will send a screenshot.\n'+BASEURL+slug+'/')
def pbox(text, code=False):
    return (f'<div class="pr{" code" if code else ""}"><p dir="auto">{"<br>".join(E_(l) for l in text.split(chr(10)))}</p>'
            f'<button class="cp" type="button" data-t="{E_(text)}">{CP}<span>نسخ</span></button></div><button class="mo" type="button">اعرض كامل ▾</button>')
def steps(rows):
    return ''.join(f'<div class="stp"><b class="n">{i}</b><span class="a">{E_(a)}</span><i></i><span class="e" dir="ltr">{E_(e)}</span></div>' for i,(a,e) in enumerate(rows,1))
AR = lambda n: str(n).translate(str.maketrans('0123456789','٠١٢٣٤٥٦٧٨٩'))

def page(title, kicker, h1, sub, sects, body_sections, fine, slug='', cprompt=''):
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
<a class="back" href="../../../library/">→ مكتبة الملفات المجانية</a><br>
<span class="kick">{E_(kicker)}</span>
<h1>{h1}</h1><p>{E_(sub)}</p>
<div class="acts"><button class="cl cp" type="button" data-t="{E_(cprompt)}">{CP}<span>انسخ لكلود</span></button><a href="{slug}.pdf" download>PDF</a><button type="button" id="shr">مشاركة</button></div>
<a class="gl" href="https://bznstatus.com/consult/"><b>لكم خصم خاص<i>٢٥٪</i></b><span>اضغط هنا ←</span></a>
</div></header>
<div class="jump"><div class="wrap"><select id="jump" aria-label="قفز لقسم"><option>قفز لقسم ↓ ({len(sects)})</option>{opts}</select></div></div>
<main class="wrap">{body_sections}
<form class="sub" id="sub" novalidate><h2>توصلك آخر التحديثات والعروض</h2><p>اكتب إيميلك أو رقمك (أو الاثنين) وأرسل لك جديد الملفات والعروض. تقدر تلغي بأي وقت.</p>
<input type="email" name="email" placeholder="الإيميل · Email" autocomplete="email"><input type="tel" name="phone" placeholder="رقم الواتساب · WhatsApp number" autocomplete="tel">
<button type="submit">اشتراك</button><div class="msg" id="submsg" hidden></div><div class="fn">نستخدم بياناتك لإرسال التحديثات والعروض فقط، وما نشاركها مع أحد.</div></form></main>
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
  'الخطوات من المواقع نفسها. © حمد الخضري @hmdalkhudhari',slug='owner-kit',cprompt=CPR('owner-kit'))

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
  'طريقة التثبيت من code.claude.com/docs. التأثيرات جربناها كلها على فيديو حقيقي قبل لا نرسلها.',slug='claude-montage-fx',cprompt=CPR('claude-montage-fx'))
for name,pg in (('owner-kit',owner),('claude-montage-fx',mont)):
    d=OUT/name; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(pg,encoding='utf8'); print('wrote',d/'index.html',len(pg))

# ---------------- hub ----------------
FILES=[('claude-instagram-13','Claude يشتغل على انستقرامك: ١٣ أمر','ريل وكابشن وكاروسيل وخطة أسبوعك بأوامر جاهزة','Claude'),
('claude-montage-fx','لا تدفع للمونتير: ٢٢ تأثير','تأثيرات مونتاج بسطر واحد داخل Claude Code','Claude'),
('claude-code-plugins','٥ بلوقنز مجانية لـClaude Code','أوامر تنصيب جاهزة بزر نسخ','Claude'),
('unslop','سكيل unslop: شيل شكل الـAI','يدور علامات الـAI بتصميمك ويصلحها','Claude'),
('claude-3-sites-15min','Claude سوّى ٣ مواقع بـ١٥ دقيقة','من فكرة لموقع شغال خطوة بخطوة','Claude'),
('claude-cowork','١٠ مهام تعطيها Claude Cowork','مهام يومية يسويها لك','Claude'),
('claude-phone','خلّ Claude يتصل ويحجز عنك','٣ خطوات','Claude'),
('claude-speed','خل Claude يفحص جهازك ونتك','فحص سرعة بأمر واحد','Claude'),
('claude-watch-earshot','خل Claude يشوف ويسمع','يحلل فيديو وصوت','Claude'),
('kuwaiti-skill','كاتب المحتوى الكويتي','سكيل يكتب بلهجتك','Claude'),
('montage-skill','منتج فيديوك بـClaude','سكيل مونتاج جاهز','Claude'),
('claude-carousel','Claude يصمم كاروسيلك كامل','كاروسيل من فكرة لسلايدات','Claude'),
('claude-whatsapp','عطِ Claude رقم واتساب','يرد ويرتب لك','Claude'),
('arabic-rtl','خل ChatGPT يكتب عربي مرتب','أوامر تصلح اتجاه العربي','ChatGPT'),
('chatgpt-shortcuts','+1000 اختصار و٤٠ برومبت لـChatGPT','اختصارات جاهزة','ChatGPT'),
('chatgpt-memory','شوف شنو ChatGPT مخزن عنك','خصوصية وذاكرة','ChatGPT'),
('chatgpt-business-hub','سجّل مشروعك داخل ChatGPT','٥ خطوات','ChatGPT'),
('truth-prompt','خل ChatGPT يقول لك الحقيقة','برومبت يكشف المجاملة','ChatGPT'),
('face-lock','خلّ ChatGPT ما يغيّر ملامح وجهك','صور بنفس وجهك','ChatGPT'),
('products-hacker','خل ChatGPT يهكر لك المنتجات','أفكار منتجات رابحة','ChatGPT'),
('owner-kit','هدية الـ٤٠ ألف: خزينة ١٠ مواقع','مواقع لصاحب المشروع وصانع المحتوى','مشاريع'),
('profit','حسبة ربح القطعة الحقيقية','احسب ربحك صح','مشاريع'),
('sales-mistakes','٣ أخطاء تقتل مبيعات منتجك','وكيف تصلحها','مشاريع'),
('ad-templates','٥ قوالب تطلع لك إعلانك','قوالب جاهزة','مشاريع'),
('ai-agent-vs-automation','AI Agent ولا Automation؟','وش تختار لمشروعك','مشاريع')]
cats=['الكل','Claude','ChatGPT','مشاريع']
hbody=('<p class="lead" style="margin-top:22px">مكتبة الملفات المجانية بمكان واحد. ابحث أو اختر قسم.</p>'
 '<input class="hubq" id="hq" type="search" placeholder="ابحث · Search" autocomplete="off">'
 '<div class="chp" id="chp">'+''.join(f'<button type="button" class="{"on" if c=="الكل" else ""}" data-c="{c}">{c}</button>' for c in cats)+'</div>'
 '<ul id="hl">'+''.join(f'<li data-c="{c}" data-s="{E_(t+" "+d)}"><a class="hc" href="../../../{sl}/"><div class="card"><span class="tg">{c}</span><b>{E_(t)}</b><span class="d">{E_(d)}</span></div></a></li>' for sl,t,d,c in FILES)+'</ul>'
 '<script>(function(){var c="الكل",q="",li=[].slice.call(document.querySelectorAll("#hl li"));function ap(){li.forEach(function(x){x.hidden=!((c=="الكل"||x.dataset.c==c)&&(!q||x.dataset.s.toLowerCase().indexOf(q)>-1))})}'
 'document.getElementById("hq").oninput=function(){q=this.value.trim().toLowerCase();ap()};document.querySelectorAll("#chp button").forEach(function(b){b.onclick=function(){c=b.dataset.c;document.querySelectorAll("#chp button").forEach(function(z){z.classList.toggle("on",z===b)});ap()}})})()</script>')
hubp = page('مكتبة الملفات المجانية','ملفات مجانية','<em>مكتبة الملفات المجانية</em>','كل أوامرنا الجاهزة بزر نسخ، بمكان واحد.',[],hbody,'حمد الخضري @hmdalkhudhari',slug='hub',cprompt=CPR('hub'))

HUBCSS = """<style>
header{position:relative;overflow:hidden;color:#fff;border-bottom:0;background:#1E2A66}
header::before{content:"";position:absolute;inset:-40%;background:radial-gradient(40% 35% at 25% 30%,rgba(242,194,48,.55),transparent 70%),radial-gradient(45% 40% at 75% 25%,rgba(95,120,255,.55),transparent 70%),radial-gradient(50% 45% at 55% 85%,rgba(242,194,48,.28),transparent 70%);filter:blur(28px);animation:mesh 14s ease-in-out infinite alternate}
@keyframes mesh{to{transform:translate3d(6%,4%,0) rotate(12deg) scale(1.08)}}
header::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(14,20,64,.15),rgba(14,20,64,.55))}
header .wrap{position:relative;z-index:1}
header h1,header .back{color:#fff}header h1 em{background:none;color:#F2C230}header p,header .tag{color:#D9DBE6}
.logo{filter:brightness(0) invert(1)}.acts[hidden]{display:none}
.kick{box-shadow:0 0 24px rgba(242,194,48,.45)}
.hc .card{transition:transform .25s,box-shadow .25s,border-color .25s;opacity:0;animation:rise .55s forwards}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.hc:hover .card{transform:translateY(-3px);box-shadow:0 12px 28px rgba(30,42,102,.14);border-color:#F2C230}
#hl li:nth-child(2) .card{animation-delay:.05s}#hl li:nth-child(3) .card{animation-delay:.1s}#hl li:nth-child(4) .card{animation-delay:.15s}#hl li:nth-child(5) .card{animation-delay:.2s}#hl li:nth-child(n+6) .card{animation-delay:.25s}
@media (prefers-reduced-motion:reduce){header::before,.hc .card{animation:none;opacity:1}}
</style>"""
hubp = hubp.replace('</head>',HUBCSS+'</head>',1)
hubp = hubp.replace('<div class="acts">','<div class="acts" hidden>',1).replace('<a class="back" href="../../../library/">→ مكتبة الملفات المجانية</a><br>','').replace('<div class="jump">','<div class="jump" hidden>',1)
hubp = re.sub(r'<form class="sub".*?</form>','',hubp,flags=re.S) if False else hubp
(OUT/'hub').mkdir(parents=True,exist_ok=True); (OUT/'hub'/'index.html').write_text(hubp,encoding='utf8'); print('wrote hub')
