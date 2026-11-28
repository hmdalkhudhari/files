#!/usr/bin/env python3
"""Shell injection for pages with their own design/CSS: adds the new profile bar + subscribe form (+ their CSS/JS) and keeps the page as is. Same URL."""
import re, sys, io, contextlib
import migrate as M
B = M.B; ROOT = M.ROOT
root_vars = re.search(r':root\{([^}]*)\}', B.CSS).group(1)
rules = []
for r in re.findall(r'[^{}]+\{[^{}]*\}', re.sub(r'@media[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}', '', B.CSS)):
    sel = r.split('{')[0]
    if re.search(r'(^|[\s,>+])(\.bar|\.me|\.menu|\.mp|\.sub|nav\.bar)\b', sel.strip()) and 'print' not in sel: rules.append(r.strip())
CSS = f'.bar,.sub{{{root_vars}}}\n' + '\n'.join(rules)
SUB = re.search(r'<form class="sub".*?</form>', B.page('x', 'x', 'x', 'x', [], '', 'x'), flags=re.S).group(0)
subjs = re.search(r"var SUB_ENDPOINT.*?(?=\n</script>)", B.JS, flags=re.S).group(0)
def inject(slug, where_form):
    t = M.old_html(slug)
    pg = t
    pg = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + B.BAR.replace('../../../library/', '../library/'), pg, count=1)
    pg = pg.replace('</head>', f'<style>{CSS}</style></head>', count=1)
    i = pg.rfind(where_form); assert i > -1, 'anchor'
    pg = pg[:i] + SUB + pg[i:]
    pg = pg.replace('</body>', f'<script>{subjs}</script></body>', count=1)
    (ROOT / slug / 'index.html').write_text(pg, encoding='utf8')
if __name__ == '__main__':
    inject(sys.argv[1], sys.argv[2])
