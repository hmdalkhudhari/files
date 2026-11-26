#!/usr/bin/env python3
"""Migrate old 'mast + article.pc' people-file pages (whatsapp, carousel, face-lock, sales-mistakes) to the new system, same URL."""
import re, sys, io, pathlib, html, contextlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import migrate as M
B = M.B; E_ = html.escape
ROOT = M.ROOT
strip = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def conv(slug):
    t = M.old_html(slug)
    kick = strip(re.search(r'<span class="kick">(.*?)</span>', t, flags=re.S).group(1))
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', t, flags=re.S).group(1)
    sub = strip(re.search(r'</h1>\s*<p[^>]*>(.*?)</p>', t, flags=re.S).group(1))
    title = strip(re.search(r'<title>(.*?)</title>', t, flags=re.S).group(1)).split(' | ')[0]
    body = ''; sects = []; n = 0
    # intro sections (guide lists)
    for sec in re.findall(r'<section[^>]*>(.*?)</section>', t, flags=re.S):
        if 'class="about"' in sec or 'class="list"' in sec: continue
        h2 = re.search(r'<h2>(.*?)</h2>', sec, flags=re.S)
        lis = re.findall(r'<li><b>[^<]*</b><span>(.*?)</span></li>', sec, flags=re.S)
        if not h2 or not lis: continue
        n += 1; sid = f's{n}'; sects.append((sid, strip(h2.group(1))))
        items = ''.join(f'<li class="card"><div class="top"><b class="n">{B.AR(i)}</b><h3 class="s">{E_(strip(x))}</h3></div></li>' for i, x in enumerate(lis, 1))
        hn = re.search(r'<p class="hn">(.*?)</p>', sec, flags=re.S)
        body += f'<section id="{sid}"><h2>{E_(strip(h2.group(1)))}</h2><ol>{items}</ol>' + (f'<p class="hint">{E_(strip(hn.group(1)))}</p>' if hn else '') + '</section>'
    # articles
    lst = re.search(r'<section[^>]*>\s*<h2>(.*?)</h2>(.*?)<div class="list">', t, flags=re.S)
    k = 0
    for art in re.findall(r'<article class="pc.*?</article>', t, flags=re.S):
        n += 1; k += 1; sid = f's{n}'
        h3 = strip(re.search(r'<h3>(.*?)</h3>', art, flags=re.S).group(1))
        tl = re.search(r'<span class="tl">(.*?)</span>', art, flags=re.S); tl = strip(tl.group(1)) if tl else ''
        sects.append((sid, h3))
        steps = [(strip(a), strip(e)) for a, e in re.findall(r'<span class="s-ar">(.*?)</span><span class="s-en"[^>]*>(.*?)</span>', art, flags=re.S)]
        raw = re.search(r'<textarea class="raw"[^>]*>(.*?)</textarea>', art, flags=re.S)
        hand = re.search(r'<div class="hand"><span>(.*?)</span>', art, flags=re.S)
        goes = re.findall(r'<a class="go" href="([^"]+)"[^>]*>(.*?)</a>', art, flags=re.S)
        inner = f'<span class="tg">{E_(tl)}</span>' if tl else ''
        if steps: inner += B.steps(steps)
        if raw: inner += (f'<div class="lab">{E_(strip(hand.group(1)))}</div>' if hand else '') + B.pbox(html.unescape(raw.group(1)).strip())
        if raw and '[' in raw.group(1): inner += '<p class="hint">بدّل اللي بين [ ] بمعلوماتك.</p>'
        inner += ''.join(f'<a class="go" href="{E_(u)}" target="_blank" rel="noopener">{E_(strip(x))}</a>' for u, x in goes)
        body += f'<section id="{sid}"><h2>{E_(h3)}</h2><div class="card">{inner}</div></section>'
    pg = B.page(title, kick, h1, sub, sects, body, 'حمد الخضري @hmdalkhudhari', slug=slug, cprompt=B.CPR(slug))
    pg = pg.replace('href="../../../library/"', 'href="../library/"')
    pg = re.sub(r'<a href="[^"]*\.pdf" download>PDF</a>', '', pg)
    (ROOT / slug / 'index.html').write_text(pg, encoding='utf8')
    return len(sects), len(re.findall(r'<article class="pc', t)), len(re.findall(r'data-t=', pg))

if __name__ == '__main__':
    for s in sys.argv[1:]: print(s, conv(s))
