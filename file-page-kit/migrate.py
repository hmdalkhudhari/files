#!/usr/bin/env python3
"""Migrate old kit-style people-file pages to the new system (profile bar, jump menu, copy-for-Claude, share, subscribe form),
keeping the same URL. Reads the OLD page body, rebuilds via build2.page. Idempotent source: reads from git HEAD~ copy in /tmp/old/<slug>.html"""
import re, sys, io, json, pathlib, html, contextlib, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
with contextlib.redirect_stdout(io.StringIO()):
    import build2 as B
ROOT = pathlib.Path(__file__).parent.parent
OLD = pathlib.Path('/tmp/old'); OLD.mkdir(exist_ok=True)
KNOWN = set(re.findall(r'\.([a-zA-Z][\w-]*)', B.CSS))
SIMPLE = {'ikea-effect-ideas', 'shoot-and-post', 'instagram-hidden-secrets', 'my-ai-team'}
SKIP = {'chatgpt-shortcuts', 'anthropic-plugins', 'mowjaz-shortcuts', 'followers-7000', 'claude-sales-employee'}

def old_html(slug):
    p = OLD / f'{slug}.html'
    if not p.exists():
        src = subprocess.run(['git', 'show', f'origin/main:{slug}/index.html'], cwd=ROOT, capture_output=True, text=True, encoding='utf8').stdout
        p.write_text(src, encoding='utf8')
    return p.read_text(encoding='utf8')

def extra_css(old_css, miss):
    out = []
    for rule in re.findall(r'[^{}]+\{[^{}]*\}', re.sub(r'@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', old_css)):
        sel = rule.split('{')[0]
        if any(re.search(r'\.' + re.escape(m) + r'\b', sel) for m in miss): out.append(rule.strip())
    return '\n'.join(out)

def migrate(slug, title_override=None):
    t = old_html(slug)
    m = re.search(r'<main[^>]*>(.*)</main>', t, flags=re.S)
    simple = False
    if not m:
        m = re.search(r'</header>\s*<div class="wrap">(.*)</div>\s*(?:<script|</body>)', t, flags=re.S)
        if not m or slug not in SIMPLE: return None
        simple = True
    main = m.group(1)
    main = re.sub(r'<script\b.*?</script>', '', main, flags=re.S) if simple else main
    kick = re.search(r'<span class="kick">(.*?)</span>', t, flags=re.S); kick = html.unescape(re.sub('<[^>]+>', '', kick.group(1))) if kick else 'ملف مجاني'
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', t, flags=re.S).group(1)
    sub = re.search(r'</h1>\s*<p[^>]*>(.*?)</p>', t, flags=re.S); sub = html.unescape(re.sub('<[^>]+>', '', sub.group(1))) if sub else ''
    if simple:
        en = re.search(r'<div class="en">(.*?)</div></div></header>', t, flags=re.S)
        if en and not sub: sub = html.unescape(re.sub('<[^>]+>', '', en.group(1)))
    title = html.unescape(re.sub('<[^>]+>', '', re.search(r'<title>(.*?)</title>', t, flags=re.S).group(1))).split(' | ')[0]
    fine = re.search(r'<p class="fine">(.*?)</p>', t, flags=re.S); fine = html.unescape(re.sub('<[^>]+>', '', fine.group(1))) if fine else 'حمد الخضري @hmdalkhudhari'
    # drop any old subscribe/footers inside main
    scripts = re.findall(r'<script\b[^>]*>.*?</script>', t, flags=re.S)
    own_js = '\n'.join(s for s in scripts if "querySelectorAll('.cp')" not in s and 'navigator.clipboard' not in s and 'data-t' not in s[:400]) if False else ''
    # section ids from h2
    sects = []; n = [0]
    def addid(mo):
        n[0] += 1; sid = f's{n[0]}'
        txt = html.unescape(re.sub('<[^>]+>', '', mo.group(2))).strip()
        sects.append((sid, txt[:60])); return f'<h2{mo.group(1)} id="{sid}">{mo.group(2)}</h2>'
    main = re.sub(r'<h2([^>]*)>(.*?)</h2>', addid, main, flags=re.S)
    scrl = re.search(r'<a class="scrl".*?</a>', t, flags=re.S)
    cls = set(c for x in re.findall(r'class="([^"]*)"', main) for c in x.split())
    miss = cls - KNOWN
    if scrl: miss |= {'scrl', 'hide'}
    old_css = ''.join(re.findall(r'<style[^>]*>(.*?)</style>', t, flags=re.S))
    ecss = extra_css(old_css, miss) if miss else ''
    # interactive pages: keep their own scripts (those not the shared copy handler)
    keep = []
    for sc in scripts:
        inner = re.sub(r'^<script[^>]*>|</script>$', '', sc)
        inner = re.sub(r"^document\.querySelectorAll\('\.cp'\)\.forEach.*?1600\)\}\)\);?", '', inner.strip(), flags=re.S)
        inner = re.sub(r"^\s*document\.querySelectorAll\('\.mo'\)\.forEach.*?'اعرض كامل ▾'\}\}\)\);?", '', inner, flags=re.S)
        rest = inner.strip()
        if len(rest) > 40: keep.append('<script>' + rest + '</script>')
    pg = B.page(title, kick, h1, sub, sects, main, fine, slug=slug, cprompt=B.CPR(slug))
    pg = pg.replace('href="../../../library/"', 'href="../library/"')
    if not (ROOT / slug / f'{slug}.pdf').exists():
        pg = re.sub(r'<a href="[^"]*\.pdf" download>PDF</a>', '', pg)
    if simple or slug=='kuwaiti-skill':
        pg = pg.replace('</head>', '<style>main pre,main code,main textarea{white-space:pre-wrap;overflow-wrap:anywhere;max-width:100%}main pre{font-family:inherit}</style></head>', 1)
    if scrl: pg = pg.replace('</body>', scrl.group(0) + '</body>', 1)
    if ecss: pg = pg.replace('</head>', f'<style>{ecss}</style></head>', 1)
    if keep: pg = pg.replace('</body>', '\n'.join(keep) + '</body>', 1)
    (ROOT / slug / 'index.html').write_text(pg, encoding='utf8')
    return len(sects), sorted(miss)

if __name__ == '__main__':
    slugs = sys.argv[1:] or [f['slug'] for f in json.load(open(pathlib.Path(__file__).parent / 'library.json', encoding='utf8'))]
    for s in slugs:
        if s in SKIP: continue
        r = migrate(s); print(s, r)
