#!/usr/bin/env python3
"""motions — animated scene types for make_motion.py (Pillow only, runs on the iPad without a browser).

A scene with "motion": "<id>" is drawn frame by frame here instead of the plain text scene.
`*word*` = accent colour. Numbers must be real (from the owner or a real source).

ids and fields:
  kinetic-words  words:[..]                      one big word at a time (hook)
  title-rise     kicker, line1, line2            small line + big line
  gold-box       text with #word#                accent box sweeps behind one word
  big-word       text                            one giant word
  typewriter     lines:[..]                      typed letter by letter
  countdown      from (3), end                   3-2-1 then a word
  steps          title, steps:[..]               numbered steps on a line
  checklist      title, items:[..]               items ticked one by one
  before-after   before_title, before, after_title, after
  counter        value, prefix, suffix, label    number counting up
  ring           value (0-100), label            circle filling to a percent
  bar-chart      title, bars:[{label,value,hi}], suffix
  stars          rating (1-5), label
  price-tag      old, now, currency, badge
  quote          text (lines split by |), author
  comment-cta    keyword, sent                   comment box typing the word + "sent" card
"""
import math
from PIL import Image, ImageDraw
import brandkit as bk

W, H = 1080, 1920
_CACHE = {}


def cl(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def P(t, a, b):
    return cl((t - a) / (b - a)) if b != a else (1.0 if t >= b else 0.0)


def out3(x):
    return 1 - (1 - cl(x)) ** 3


def out4(x):
    return 1 - (1 - cl(x)) ** 4


def inout(x):
    x = cl(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def expo(x):
    x = cl(x)
    return 1.0 if x >= 1 else 1 - 2 ** (-10 * x)


def pop(x):
    x = cl(x)
    s = 1.6
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def text_img(b, text, size, weight="black", color=None, hl=None, width=900, align="center", marker=False):
    key = ("t", text, size, weight, color, hl, width, align, marker)
    if key in _CACHE:
        return _CACHE[key]
    ft = bk.font(b, size, weight)
    h = bk.text_height(text, ft, width) + size
    img = Image.new("RGBA", (width + 40, h + 40), (0, 0, 0, 0))
    bk.draw_rich(img, text, ft, (20, 20, width + 20, h), color or b["ink"], hl or b["acc"], align=align,
                 hl_style="marker" if marker else "color")
    bb = img.getbbox()
    img = img.crop(bb) if bb else img
    _CACHE[key] = img
    return img


def fade(img, a):
    a = cl(a)
    if a >= 0.999:
        return img
    im = img.copy()
    al = im.getchannel("A").point(lambda v: int(v * a))
    im.putalpha(al)
    return im


def place(layer, img, cx, y, a=1.0, scale=1.0, dx=0, dy=0, anchor="center"):
    """put img with its top at y; cx = centre x (or right edge when anchor='right')."""
    if a <= 0.003 or img is None:
        return
    if abs(scale - 1) > 0.004:
        img = img.resize((max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.BILINEAR)
    img = fade(img, a)
    x = int(cx - img.width / 2) if anchor == "center" else int(cx - img.width)
    yy = int(y + dy)
    if anchor == "center" and scale != 1:
        yy = int(y + dy - (img.height - img.height / scale) / 2)
    layer.alpha_composite(img, (int(x + dx), yy)) if 0 <= x + dx and x + dx + img.width <= W and 0 <= yy and yy + img.height <= H \
        else _paste_clip(layer, img, int(x + dx), yy)


def _paste_clip(layer, img, x, y):
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmp.paste(img, (x, y), img)
    layer.alpha_composite(tmp)


def rise(layer, img, cx, y, t, a0, end, anchor="center"):
    k = out4(P(t, a0, a0 + 0.6))
    f = out3(P(t, a0, a0 + 0.4))
    o = inout(P(t, end - 0.3, end))
    place(layer, img, cx, y, min(f, 1 - o), dy=(1 - k) * 40 - o * 24, anchor=anchor)


def leave(t, end, ln=0.3):
    return inout(P(t, end - ln, end))


def card(b, w, h, r=30, color=None):
    key = ("c", w, h, r, color or "card")
    if key not in _CACHE:
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        c = color or _card_color(b)
        ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=r, fill=bk.hexrgb(c))
        _CACHE[key] = im
    return _CACHE[key]


def _card_color(b):
    r, g, bb, _ = bk.hexrgb(b["bg"])
    f = lambda v: int(v + (255 - v) * 0.09) if bk.is_dark(b["bg"]) else int(v * 0.93)
    return "#%02x%02x%02x" % (f(r), f(g), f(bb))


def circle(d, cx, cy, r, fill=None, outline=None, width=1):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=width)


AR = "٠١٢٣٤٥٦٧٨٩"


def ar_num(n):
    return "".join(AR[int(c)] if c.isdigit() else c for c in str(n))


# ------------------------------------------------------------------ the motions
def draw(b, sc, t, dur):
    """returns an RGBA layer W x H for local time t (0..dur)."""
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fn = MOTIONS.get(sc.get("motion"))
    if fn:
        fn(b, sc, t, dur, L)
    return L


def m_kinetic(b, sc, t, dur, L):
    words = sc.get("words", [])
    n = max(1, len(words))
    K = [0.1 + i * (dur - 0.5) / n for i in range(n)]
    i = max([j for j, s in enumerate(K) if t >= s], default=-1)
    if i < 0:
        return
    img = text_img(b, words[i], sc.get("size", 170), width=1000)
    k = P(t, K[i], K[i] + 0.18)
    o = leave(t, dur)
    place(L, img, W / 2, sc.get("y", 820), min(1, k * 4) * (1 - o), scale=1.4 - 0.4 * out3(k) + 0.025 * P(t, K[i], K[i] + 1))


def m_title(b, sc, t, dur, L):
    y = sc.get("y", 300)
    if sc.get("kicker"):
        place(L, text_img(b, sc["kicker"], 30, "bold", color=b["acc"]), W / 2, y, out3(P(t, 0, 0.4)) * (1 - leave(t, dur)))
    l1 = text_img(b, sc.get("line1", ""), 62, "regular")
    l2 = text_img(b, sc.get("line2", ""), sc.get("size", 100), width=1000)
    rise(L, l1, W / 2, y + 60, t, 0.05, dur)
    rise(L, l2, W / 2, y + 60 + l1.height + 24, t, 0.3, dur)


def m_goldbox(b, sc, t, dur, L):
    text = sc.get("text", "")
    parts = text.split("#")
    size = sc.get("size", 96)
    ft = bk.font(b, size, "black")
    d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    # measure pieces right-to-left
    segs = [(p.strip(), i % 2 == 1) for i, p in enumerate(parts) if p.strip()]
    sp = bk.wlen(d, " ", ft)
    widths = [bk.wlen(d, s, ft) + (size * 0.4 if hl else 0) for s, hl in segs]
    total = sum(widths) + sp * (len(segs) - 1)
    o = leave(t, dur)
    k = out4(P(t, 0, 0.6))
    a = min(out3(P(t, 0, 0.4)), 1 - o)
    y = sc.get("y", 1150) + (1 - k) * 40
    at = sc.get("at", 0.75)
    bx = out3(P(t, at, at + 0.3))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(layer)
    x = W / 2 + total / 2
    asc, desc = ft.getmetrics()
    for (s, hl), w in zip(segs, widths):
        xl = x - w
        col = b["ink"]
        if hl:
            pad = size * 0.2
            if bx > 0:
                dd.rounded_rectangle((x - w * bx, y - size * 0.16, x, y + asc + desc * 0.75), radius=14, fill=bk.hexrgb(b["acc"]))
            col = b["bg"] if bx > 0.5 else b["ink"]
            dd.text((xl + pad, y), bk._shape(s, ft), font=ft, fill=bk.hexrgb(col), **bk._kw(s))
        else:
            dd.text((xl, y), bk._shape(s, ft), font=ft, fill=bk.hexrgb(col), **bk._kw(s))
        x = xl - sp
    L.alpha_composite(fade(layer, a))


def m_bigword(b, sc, t, dur, L):
    p = P(t, 0, 0.35)
    o = leave(t, dur)
    img = text_img(b, sc.get("text", ""), sc.get("size", 250), width=1040)
    place(L, img, W / 2, sc.get("y", 760), out3(p) * (1 - o), scale=0.6 + 0.4 * cl(pop(p), 0, 1.1) + 0.04 * P(t, 0.35, dur))


def m_typewriter(b, sc, t, dur, L):
    lines = sc.get("lines", [])
    cps = sc.get("cps", 16)
    y = sc.get("y", 760)
    c = 0.15
    o = leave(t, dur)
    for i, ln in enumerate(lines):
        n = int(cl((t - c) * cps + 1, 0, len(ln)))
        if n > 0:
            s = ln[:n]
            img = text_img(b, s, sc.get("size", 76), "black" if i else "bold", color=b["acc"] if i else b["ink"], width=1000)
            place(L, img, W / 2, y, 1 - o)
        y += int(sc.get("size", 76) * 1.5)
        c += len(ln) / cps + 0.25


def m_countdown(b, sc, t, dur, L):
    fr = sc.get("from", 3)
    step = (dur - 0.6) / (fr + 1)
    i = int((t - 0.1) // step) if t >= 0.1 else -1
    if i < 0:
        return
    s = 0.1 + i * step
    k = P(t, s, s + 0.25)
    is_end = i >= fr
    txt = sc.get("end", "*يلا*") if is_end else ("*%s*" % ar_num(fr - i) if i == fr - 1 else ar_num(fr - i))
    a = out3(k) * (1 - leave(t, dur)) * (1 if is_end else 1 - P(t, s + step - 0.15, s + step))
    place(L, text_img(b, txt, sc.get("size", 300), width=1000), W / 2, sc.get("y", 720), a, scale=1.6 - 0.6 * out3(k))


def m_steps(b, sc, t, dur, L):
    steps = sc.get("steps", [])
    y0 = sc.get("y", 480)
    o = leave(t, dur, 0.4)
    gap = sc.get("gap", 0.65)
    rise(L, text_img(b, sc.get("title", ""), 76), W / 2, y0, t, 0, dur)
    top = y0 + 150
    d = ImageDraw.Draw(L)
    cx = 960 - 52
    n = len(steps)
    ln = inout(P(t, 0.6, 0.6 + (n - 1) * gap + 0.3))
    if n > 1 and ln > 0 and o < 1:
        d.rectangle((cx - 3, top + 52, cx + 2, top + 52 + (n - 1) * 160 * ln), fill=bk.hexrgb(b["acc"], int(255 * (1 - o))))
    for i, s in enumerate(steps):
        T = 0.5 + i * gap
        k = P(t, T, T + 0.4)
        e = expo(k)
        a = min(e, 1 - o)
        if a <= 0:
            continue
        y = top + i * 160
        on = P(t, T + 0.15, T + 0.4) > 0.5
        r = int(52 * cl(pop(k), 0, 1.2))
        dot = Image.new("RGBA", (130, 130), (0, 0, 0, 0))
        dd = ImageDraw.Draw(dot)
        circle(dd, 65, 65, r, fill=bk.hexrgb(b["acc"] if on else _card_color(b)), outline=bk.hexrgb(b["acc"]), width=4)
        if r > 20:
            num = text_img(b, ar_num(i + 1), 50, color=b["bg"] if on else b["acc"], width=100)
            dot.alpha_composite(num, (65 - num.width // 2, 65 - num.height // 2))
        place(L, dot, cx, y - 13, a, dx=(1 - e) * -60)
        place(L, text_img(b, s, 54, "bold", width=700, align="right"), cx - 90, y + 22, a, dx=(1 - e) * -60, anchor="right")


def m_checklist(b, sc, t, dur, L):
    items = sc.get("items", [])
    y0 = sc.get("y", 540)
    o = leave(t, dur, 0.4)
    rise(L, text_img(b, sc.get("title", ""), 76), W / 2, y0, t, 0, dur)
    for i, s in enumerate(items):
        T = 0.45 + i * 0.6
        e = expo(P(t, T, T + 0.4))
        a = min(e, 1 - o)
        if a <= 0:
            continue
        done = t > T + 0.35
        y = y0 + 160 + i * 130
        box = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
        dd = ImageDraw.Draw(box)
        dd.rounded_rectangle((3, 3, 86, 86), radius=20, fill=bk.hexrgb(b["acc"]) if done else None, outline=bk.hexrgb(b["acc"]), width=5)
        if done:
            dd.line([(24, 46), (40, 62), (68, 30)], fill=bk.hexrgb(b["bg"]), width=9, joint="curve")
        place(L, box, 920, y, a, dx=(1 - e) * -50, anchor="right")
        place(L, text_img(b, s, 54, "bold", width=700, align="right"), 800, y + 14, a, dx=(1 - e) * -50, anchor="right")


def m_before_after(b, sc, t, dur, L):
    o = leave(t, dur, 0.4)
    y = sc.get("y", 640)
    for j, (ttl, txt, good) in enumerate([(sc.get("before_title", "قبل"), sc.get("before", ""), False),
                                          (sc.get("after_title", "بعد"), sc.get("after", ""), True)]):
        c = card(b, 900, 210, 32).copy()
        dd = ImageDraw.Draw(c)
        if good:
            dd.rounded_rectangle((0, 0, 899, 209), radius=32, outline=bk.hexrgb(b["acc"]), width=5)
        circle(dd, 830, 105, 46, fill=bk.hexrgb(b["acc"]) if good else (255, 255, 255, 40))
        if good:
            dd.line([(808, 106), (824, 122), (852, 92)], fill=bk.hexrgb(b["bg"]), width=8)
        else:
            dd.line([(812, 87), (848, 123)], fill=bk.hexrgb(b["ink"]), width=7)
            dd.line([(848, 87), (812, 123)], fill=bk.hexrgb(b["ink"]), width=7)
        ti = text_img(b, ttl, 34, "bold", color=b["mut"], width=700, align="right")
        tx = text_img(b, txt, 48, "black", width=700, align="right")
        c.alpha_composite(ti, (750 - ti.width, 40))
        c.alpha_composite(tx, (750 - tx.width, 40 + ti.height + 14))
        if not good:
            a = min(expo(P(t, 0.1, 0.55)), 1 - o) * (1 - 0.45 * P(t, 1.4, 1.8))
            place(L, c, W / 2, y, a, dy=(1 - expo(P(t, 0.1, 0.55))) * 50)
        else:
            p = P(t, 1.4, 1.9)
            place(L, c, W / 2, y + 250, out3(p) * (1 - o), scale=cl(pop(p), 0, 1.08))


def m_counter(b, sc, t, dur, L):
    o = leave(t, dur)
    k = out4(P(t, 0.15, 1.6))
    v = sc.get("value", 0)
    dec = sc.get("decimals", 0)
    val = v * k
    s = (f"{val:,.{dec}f}" if dec else f"{round(val):,}")
    a = out3(P(t, 0, 0.3)) * (1 - o)
    num = text_img(b, "%s%s%s" % (sc.get("prefix", ""), s, sc.get("suffix", "")), sc.get("size", 230), color=b["acc"], width=1040)
    y = sc.get("y", 660)
    place(L, num, W / 2, y, a, scale=0.9 + 0.1 * out3(P(t, 0, 0.5)) + (0.03 if 1.6 < t < 1.8 else 0))
    rise(L, text_img(b, sc.get("label", ""), 62, "bold"), W / 2, y + num.height + 50, t, 0.5, dur)


def m_ring(b, sc, t, dur, L):
    o = leave(t, dur, 0.4)
    k = out4(P(t, 0.2, 1.8))
    v = sc.get("value", 0)
    y = sc.get("y", 560)
    R = 220
    ring = Image.new("RGBA", (520, 520), (0, 0, 0, 0))
    d = ImageDraw.Draw(ring)
    d.ellipse((40, 40, 480, 480), outline=(255, 255, 255, 30) if bk.is_dark(b["bg"]) else (0, 0, 0, 30), width=36)
    if k * v > 0:
        d.arc((40, 40, 480, 480), -90, -90 + 360 * v / 100 * k, fill=bk.hexrgb(b["acc"]), width=36)
    num = text_img(b, f"{round(v * k)}%", 140, width=500)
    ring.alpha_composite(num, (260 - num.width // 2, 260 - num.height // 2))
    place(L, ring, W / 2, y, out3(P(t, 0, 0.35)) * (1 - o), scale=0.85 + 0.15 * out3(P(t, 0, 0.5)))
    rise(L, text_img(b, sc.get("label", ""), 60, "bold"), W / 2, y + 570, t, 0.6, dur + 1)


def m_bars(b, sc, t, dur, L):
    o = leave(t, dur, 0.4)
    bars = sc.get("bars", [])
    mx = max([x.get("value", 0) for x in bars] or [1]) or 1
    y = sc.get("y", 520)
    rise(L, text_img(b, sc.get("title", ""), 72), W / 2, y, t, 0, dur)
    d = ImageDraw.Draw(L)
    for i, x in enumerate(bars):
        k = out4(P(t, 0.4 + i * 0.3, 1.4 + i * 0.3))
        yy = y + 150 + i * 150
        a = int(255 * (1 - o))
        lab = text_img(b, x.get("label", ""), 40, "bold", width=500, align="right")
        place(L, lab, 970, yy, 1 - o, anchor="right")
        val = text_img(b, f"{round(x.get('value', 0) * k)}{sc.get('suffix', '')}", 40, "bold",
                       color=b["acc"] if x.get("hi") else b["ink"], width=300, align="left")
        place(L, val, 110 + val.width, yy, 1 - o, anchor="right")
        d.rounded_rectangle((110, yy + 62, 970, yy + 112), radius=25, fill=(255, 255, 255, int(25 * (1 - o))))
        wbar = 860 * x.get("value", 0) / mx * k
        if wbar > 2:
            col = bk.hexrgb(b["acc"], a) if x.get("hi") else (255, 255, 255, int(190 * (1 - o)))
            d.rounded_rectangle((970 - wbar, yy + 62, 970, yy + 112), radius=25, fill=col)


def _star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def m_stars(b, sc, t, dur, L):
    o = leave(t, dur, 0.4)
    y = sc.get("y", 700)
    rating = sc.get("rating", 5)
    for i in range(5):
        T = 0.15 + i * 0.16
        p = P(t, T, T + 0.35)
        on = i < rating and t > T + 0.1
        st = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        _star(ImageDraw.Draw(st), 80, 84, 72, bk.hexrgb(b["acc"]) if on else (255, 255, 255, 40))
        place(L, st, W / 2 + (2 - i) * 170, y, out3(p) * (1 - o), scale=cl(pop(p), 0, 1.2))
    rise(L, text_img(b, sc.get("label", ""), 62, "bold"), W / 2, y + 210, t, 1.0, dur)


def m_price(b, sc, t, dur, L):
    o = leave(t, dur, 0.4)
    y = sc.get("y", 640)
    cur = sc.get("currency", "")
    old = text_img(b, f"{sc.get('old', '')} {cur}", 90, "bold", color=b["mut"])
    rise(L, old, W / 2, y, t, 0, dur)
    k = out4(P(t, 0.5, 0.8))
    if k > 0:
        d = ImageDraw.Draw(L)
        ym = y + old.height // 2 + 4
        x1 = W / 2 + old.width / 2 + 10
        d.rectangle((x1 - (old.width + 20) * k, ym - 4, x1, ym + 4), fill=bk.hexrgb(b["ink"], int(255 * (1 - o))))
    n = P(t, 0.9, 1.3)
    new = text_img(b, f"{sc.get('now', '')} {cur}", 200, color=b["acc"], width=1000)
    place(L, new, W / 2, y + old.height + 40, out3(n) * (1 - o), scale=cl(pop(n), 0, 1.12))
    if sc.get("badge"):
        bg = text_img(b, sc["badge"], 46, color=b["bg"], width=800)
        pill = Image.new("RGBA", (bg.width + 80, bg.height + 40), (0, 0, 0, 0))
        ImageDraw.Draw(pill).rounded_rectangle((0, 0, pill.width - 1, pill.height - 1), radius=pill.height // 2, fill=bk.hexrgb(b["acc"]))
        pill.alpha_composite(bg, (40, 20))
        p2 = P(t, 1.4, 1.8)
        place(L, pill, W / 2, y + old.height + new.height + 90, out3(p2) * (1 - o), dy=(1 - out3(p2)) * 30)


def m_quote(b, sc, t, dur, L):
    o = leave(t, dur, 0.4)
    y = sc.get("y", 640)
    p = P(t, 0, 0.4)
    place(L, text_img(b, "”", 240, color=b["acc"]), W / 2, y, out3(p) * (1 - o), scale=cl(pop(p), 0, 1.15))
    yy = y + 150
    for i, ln in enumerate(sc.get("text", "").split("|")):
        img = text_img(b, ln, 68, width=980)
        rise(L, img, W / 2, yy, t, 0.3 + i * 0.35, dur)
        yy += img.height + 24
    if sc.get("author"):
        rise(L, text_img(b, "— " + sc["author"], 38, "regular", color=b["mut"]), W / 2, yy + 30, t, 1.2, dur)


def m_comment(b, sc, t, dur, L):
    o = leave(t, dur, 0.4)
    y = sc.get("y", 1100)
    kw = sc.get("keyword", "")
    k = inout(P(t, 0, 0.45))
    T1 = 0.6
    T2 = T1 + max(0.35, len(kw) * 0.12)
    c = card(b, 900, 290, 32).copy()
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((30, 166, 870, 260), radius=47, outline=(255, 255, 255, 70), width=2)
    circle(d, 70, 213, 33, fill=bk.hexrgb(b["acc"]))
    typing = T1 <= t < T2 + 0.05
    if typing:
        n = min(len(kw), 1 + int((t - T1) / (T2 - T1) * len(kw)))
        tx = text_img(b, kw[:n], 42, "bold", width=600, align="right")
    else:
        tx = text_img(b, sc.get("placeholder", "أضف تعليق…"), 42, "regular", color=b["mut"], width=600, align="right")
    c.alpha_composite(tx, (830 - tx.width, 190))
    p = expo(P(t, T2 + 0.05, T2 + 0.4))
    if p > 0:
        circle(d, 830, 75, 31, fill=bk.hexrgb(b["acc"]))
        kimg = fade(text_img(b, kw, 56, color=b["acc"], width=600, align="right"), p)
        c.alpha_composite(kimg, (770 - kimg.width, 40 + int((1 - p) * 30)))
    place(L, c, W / 2, y, k * (1 - o), dy=(1 - k) * 90 - o * 60)
    dd = inout(P(t, T2 + 0.7, T2 + 1.0))
    if t > T2 + 0.7:
        s = card(b, 860, 130, 30).copy()
        sd = ImageDraw.Draw(s)
        sd.rounded_rectangle((760, 26, 838, 104), radius=22, fill=bk.hexrgb(b["acc"]))
        sd.line([(780, 66), (794, 80), (820, 50)], fill=bk.hexrgb(b["bg"]), width=8)
        st = text_img(b, sc.get("sent", "أرسلت لك").replace("✓", "").strip(), 44, "bold", width=700, align="right")
        s.alpha_composite(st, (730 - st.width, 65 - st.height // 2))
        place(L, s, W / 2, y + 330, dd * (1 - o), dy=(1 - dd) * 50 - o * 60)


MOTIONS = {
    "kinetic-words": m_kinetic, "title-rise": m_title, "gold-box": m_goldbox, "big-word": m_bigword,
    "typewriter": m_typewriter, "countdown": m_countdown, "steps": m_steps, "checklist": m_checklist,
    "before-after": m_before_after, "counter": m_counter, "ring": m_ring, "bar-chart": m_bars,
    "stars": m_stars, "price-tag": m_price, "quote": m_quote, "comment-cta": m_comment,
}
