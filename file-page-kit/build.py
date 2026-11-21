#!/usr/bin/env python3
"""يبني صفحة ملف ناس من specs/<name>.json  ->  ../<slug>/index.html  (+ PDF اختياري)
الاستخدام:  python3 build.py specs/claude-code-plugins.json [--pdf]
"""
import json, re, sys, html, pathlib
H = pathlib.Path(__file__).parent
ROOT = H.parent
ar = (ROOT/'arabic-rtl/index.html').read_text(encoding='utf8')  # نأخذ شعار حمد من القالب المعتمد
LOGO = re.search(r'\.logo\{[^}]*\}', ar).group(0)
CSS = (H/'style.css').read_text(encoding='utf8')
PHOTO = (H/'photo.b64').read_text().strip()
CP = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/></svg>'
E_ = lambda s: html.escape(s, quote=True)
SPEC = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf8'))
S = SPEC

def copy_box(text, code=False):
    return (f'<div class="pr{" code" if code else ""}"><p{" dir=ltr" if code else ""}>{E_(text)}</p>'
            f'<button class="cp" type="button" data-t="{E_(text)}">{CP}<span>نسخ</span></button></div>')

cards = []
for i, it in enumerate(S['items'], 1):
    cmds = (f'<p class="hint">{E_(it["where"])}</p>' if it.get('where') else '') + ''.join(copy_box(c, True) for c in it['cmds'])
    note = f'<div class="warn">{E_(it["note"])}</div>' if it.get('note') else ''
    cards.append(
        f'<li class="card"><div class="top"><b class="n">{i}</b><h3 dir="ltr">{E_(it["name"])}</h3></div>'
        f'<div class="bi"><span class="a">{E_(it["ar"])}</span><span class="e" dir="ltr">{E_(it["en"])}</span></div>'
        f'{cmds}{note}<a class="src" href="{E_(it["src"])}"><span>المصدر الرسمي: {E_(it["src_label"])}</span></a></li>')

steps = ''.join(f'<div><b>{n}</b>{E_(t)}</div>' for n, t in enumerate(S['claude_steps'], 1))
pdf = f'<a class="pdf" href="{E_(S["slug"])}.pdf" download>حمّل الملف PDF</a>' if S.get('pdf') else ''
fix = ''
if S.get('fixes'):
    rows = ''.join(f'<li class="card"><div class="bi"><span class="a">{E_(a)}</span><span class="e" dir="ltr">{E_(b)}</span></div></li>' for a, b in S['fixes'])
    fix = f'<h2>إذا ما اشتغل</h2><ul>{rows}</ul>'
srcs = ''.join(f'<li><a class="src" href="{E_(u)}"><span>{E_(t)}</span></a></li>' for t, u in S['sources'])

page = f'''<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E_(S["title"])} | حمد الخضري</title>
<meta property="og:title" content="{E_(S["title"])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
<style>
{CSS.replace(re.search(r".logo\{[^}]*\}", CSS).group(0), LOGO) if re.search(r".logo\{[^}]*\}", CSS) else CSS}
</style></head><body>
<nav class="bar"><div class="wrap"><a class="me" href="https://www.instagram.com/hmdalkhudhari/"><img src="data:image/jpeg;base64,{PHOTO}" alt="حمد الخضري" width="36" height="36"><b>حمد الخضري</b></a>
<details class="menu"><summary aria-label="القائمة">☰</summary><div class="mp"><a href="https://www.instagram.com/hmdalkhudhari/">انستقرام</a><a href="https://wa.me/message/D6QAVYNNKNQZA1">واتساب</a><a href="https://bznstatus.com/consult/">احجز استشارة</a></div></details></div></nav>
<header><div class="wrap">
<div class="logo" role="img" aria-label="Hamad Alkhudhari"></div><div class="tag">Business &amp; AI</div>
<span class="kick">{E_(S["kicker"])}</span>
<h1>{S["h1_html"]}</h1>
<p>{E_(S["sub"])}</p>
<a class="gl" href="https://bznstatus.com/consult/"><b>لكم خصم خاص<i>٢٥٪</i></b><span>اضغط هنا ←</span></a>
<button class="big" type="button" data-t="{E_(S["claude_prompt"])}">{CP}<span>انسخ لكلود</span></button>
<div class="three">{steps}</div>
</div></header>
<main class="wrap">
<h2>{E_(S["list_title"])}</h2>
<p class="lead">{E_(S["list_lead"])}</p>
<ol>{''.join(cards)}</ol>
{fix}
<h2>المصادر</h2>
<ul>{srcs}</ul>
{pdf}
</main>
<footer><div class="wrap">
<h2>جربها وعطني رايك</h2><p>كل يوم أنزل شي جديد بالبزنس والـAI.</p>
<div class="btns"><a class="btn ig" href="https://www.instagram.com/hmdalkhudhari/">تابعني بانستقرام</a><a class="btn wa" href="https://wa.me/message/D6QAVYNNKNQZA1">كلمني واتساب</a></div>
<p class="fine">{E_(S["fine"])}</p>
</div></footer>
<script>document.querySelectorAll('.cp,.big').forEach(b=>b.onclick=async()=>{{try{{await navigator.clipboard.writeText(b.dataset.t)}}catch(e){{const t=document.createElement('textarea');t.value=b.dataset.t;document.body.appendChild(t);t.select();document.execCommand('copy');t.remove()}}const l=b.querySelector('span'),o=l.textContent;b.classList.add('ok');l.textContent='انتسخ ✓';setTimeout(()=>{{b.classList.remove('ok');l.textContent=o}},1600)}});</script>
</body></html>'''
out = ROOT/S['slug']; out.mkdir(exist_ok=True)
(out/'index.html').write_text(page, encoding='utf8')
print('wrote', out/'index.html', len(page))
if '--pdf' in sys.argv:
    import subprocess
    subprocess.run(['node', str(H/'pdf.js'), str(out/'index.html'), str(out/(S['slug']+'.pdf'))], check=True)
    print('wrote pdf')
