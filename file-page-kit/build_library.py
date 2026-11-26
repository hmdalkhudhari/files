#!/usr/bin/env python3
"""Library of all free people-files -> ../library/index.html  (data: library.json). To add a file: add a line in library.json, run this."""
import json, re, pathlib, html, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build2 as B
H = pathlib.Path(__file__).parent; ROOT = H.parent
E_ = html.escape
FILES = json.load(open(H/'library.json', encoding='utf8'))
cats = ['الكل'] + list(dict.fromkeys(f['cat'] for f in FILES))
cnt = {c: (len(FILES) if c == 'الكل' else sum(1 for f in FILES if f['cat'] == c)) for c in cats}
body = ('<p class="lead" style="margin-top:22px">كل الملفات اللي نرسلها للناس بمكان واحد. ابحث أو اختر قسم. أي ملف جديد ينضاف هنا.</p>'
 '<input class="hubq" id="hq" type="search" placeholder="ابحث · Search" autocomplete="off">'
 '<div class="chp" id="chp">' + ''.join(f'<button type="button" class="{"on" if c=="الكل" else ""}" data-c="{E_(c)}">{E_(c)} ({B.AR(cnt[c])})</button>' for c in cats) + '</div>'
 '<ul id="hl">' + ''.join(
   f'<li data-c="{E_(f["cat"])}" data-s="{E_(f["title"]+" "+f["desc"])}"><a class="hc" href="../{f["slug"]}/"><div class="card"><span class="tg">{E_(f["cat"])}{" · جديد" if f.get("new") else ""}</span><b>{E_(f["title"])}</b><span class="d">{E_(f["desc"])}</span></div></a></li>' for f in FILES) + '</ul>'
 '<script>(function(){var c="الكل",q="",li=[].slice.call(document.querySelectorAll("#hl li"));function ap(){li.forEach(function(x){x.hidden=!((c=="الكل"||x.dataset.c==c)&&(!q||x.dataset.s.toLowerCase().indexOf(q)>-1))})}'
 'document.getElementById("hq").oninput=function(){q=this.value.trim().toLowerCase();ap()};document.querySelectorAll("#chp button").forEach(function(b){b.onclick=function(){c=b.dataset.c;document.querySelectorAll("#chp button").forEach(function(z){z.classList.toggle("on",z===b)});ap()}})})()</script>')
pg = B.page('مكتبة الملفات المجانية', 'ملفات مجانية', '<em>مكتبة الملفات المجانية</em>', 'كل أوامرنا وأدواتنا الجاهزة بمكان واحد.', [], body,
            'حمد الخضري @hmdalkhudhari', slug='library', cprompt='')
pg = pg.replace('</head>', B.HUBCSS + '</head>', 1)
pg = pg.replace('<div class="acts">', '<div class="acts" hidden>', 1).replace('<div class="jump">', '<div class="jump" hidden>', 1)
pg = re.sub(r'<a class="back"[^>]*>[^<]*</a><br>', '', pg)
pg = pg.replace('href="../../../library/"', 'href="./"')
out = ROOT/'library'; out.mkdir(exist_ok=True); (out/'index.html').write_text(pg, encoding='utf8'); print('wrote', out/'index.html', len(FILES), 'files')
