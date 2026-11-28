#!/usr/bin/env python3
"""ad-templates (interactive generator) -> new system (kit light design), same URL."""
import re
import migrate as M
B = M.B; ROOT = M.ROOT
slug = 'ad-templates'
t = M.old_html(slug)
secs = re.findall(r'<section class="rv">(.*?)</section>', t, flags=re.S)
body = ''; sects = []
for i, s in enumerate(secs, 1):
    h = re.search(r'<div class="step"><span class="sn">[^<]*</span><h2>(.*?)</h2></div>', s, flags=re.S)
    s = s.replace(h.group(0), f'<h2 id="s{i}">{B.AR(i)}. {h.group(1)}</h2>')
    s = s.replace('class="btn gh"', 'class="abtn gh"').replace('class="btn" id="copy"', 'class="abtn" id="copy"').replace('class="acts"', 'class="aacts"').replace('class="two"', 'class="atwo"')
    sects.append((f's{i}', f'{B.AR(i)}. ' + h.group(1)))
    body += f'<section><div class="card">{s}</div></section>'
js = re.findall(r'<script>(.*?)</script>', t, flags=re.S)[0]
js = js[:js.index('var io=new IntersectionObserver')] + '})();'
CSS = """
.tpls{display:grid;gap:10px;margin-top:10px}
.tp{text-align:right;background:#fff;border:1.5px solid var(--line);border-radius:14px;padding:12px 14px;font-family:'Tajawal',sans-serif;cursor:pointer;color:var(--navy)}
.tp.on{border-color:var(--y);background:#FFF8E0;box-shadow:0 0 0 3px rgba(242,194,48,.25)}
.tp .tg{font-size:12px;font-weight:800;color:#8A6A00}.tp .nm{font-size:17px;font-weight:900}.tp .ex{font-size:13px;color:#5A5F80;margin-top:2px}
.q{margin-top:16px}.q.hid{display:none}.q label{display:block;font-weight:800;margin-bottom:8px;color:var(--navy)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font:700 14px 'Tajawal',sans-serif;background:#F4F5FA;border:1.5px solid var(--line);border-radius:999px;padding:8px 14px;color:var(--navy);cursor:pointer}
.chip.on{background:var(--navy);color:#fff;border-color:var(--navy)}
.q input{width:100%;margin-top:8px;font:500 15px 'Tajawal',sans-serif;border:1.5px solid var(--line);border-radius:12px;padding:12px;background:#fff;color:var(--navy)}
.q input.solo{margin-top:0}
.out{background:#F4F5FA;border:1px solid var(--line);border-radius:14px;padding:14px}
.out pre{white-space:pre-wrap;overflow-wrap:anywhere;font:500 14px/1.8 'Tajawal',sans-serif;margin:0;color:var(--navy)}
.miss{color:#C0392B;font-weight:800;margin-bottom:8px}.miss:empty{display:none}
.aacts{margin-top:12px;display:grid;gap:10px}.atwo{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.abtn{display:block;text-align:center;text-decoration:none;font:800 16px 'Tajawal',sans-serif;border:0;border-radius:12px;padding:13px;background:var(--y);color:var(--navy);cursor:pointer}
.abtn.gh{background:#fff;border:1.5px solid var(--navy)}.abtn.done{background:#1F9D55;color:#fff}
"""
pg = B.page('٥ قوالب تطلع لك إعلانك', 'ملف مجاني', '٥ قوالب <em>تطلع لك إعلانك</em>', 'اختار قالب، جاوب بضغطات، انسخ، والـAI يكتب لك ٣ صياغات.', sects, body, 'حمد الخضري @hmdalkhudhari', slug=slug, cprompt=B.CPR(slug))
pg = pg.replace('href="../../../library/"', 'href="../library/"')
pg = re.sub(r'<a href="[^"]*\.pdf" download>PDF</a>', '', pg)
pg = pg.replace('</head>', f'<style>{CSS}</style></head>', 1).replace('</body>', f'<script>{js}</script></body>', 1)
(ROOT / slug / 'index.html').write_text(pg, encoding='utf8'); print(len(sects))
