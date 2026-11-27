#!/usr/bin/env python3
"""Add English lines under Arabic-only intro/note items (rule: steps AR+EN). Idempotent. Data: en_items.json"""
import re, json, html, pathlib, glob
H = pathlib.Path(__file__).parent; ROOT = H.parent
EN = json.load(open(H/'en_items.json', encoding='utf8'))
ST = 'display:block;margin-top:4px;color:#5A5F80;font-size:.9em;font-weight:500'
def tag(inner):
    en = EN.get(html.unescape(re.sub('<[^>]+>', '', inner)).strip())
    return inner + f'<span class="e" dir="ltr" style="{ST}">{html.escape(en)}</span>' if en else inner
n = 0
for f in sorted(glob.glob(str(ROOT/'*/index.html'))):
    t = open(f, encoding='utf8').read()
    if 'id="sub"' not in t or 'class="e" dir="ltr" style="display:block' in t: continue
    t2 = re.sub(r'(<li class="nt"><b>[^<]*</b><span>)(.*?)(</span></li>)', lambda m: m.group(1)+tag(m.group(2))+m.group(3), t, flags=re.S)
    t2 = re.sub(r'(<li class="card"><div class="top"><b class="n">[^<]*</b><h3 class="s">)(.*?)(</h3></div></li>)', lambda m: m.group(1)+tag(m.group(2))+m.group(3), t2, flags=re.S)
    if t2 != t: open(f, 'w', encoding='utf8').write(t2); n += 1; print('en added', f.split('/')[-2])
