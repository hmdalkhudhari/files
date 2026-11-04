#!/usr/bin/env python3
"""brandkit — shared drawing engine for posts, stories, carousels and music motion videos.
Needs only Pillow + numpy (+ ffmpeg for video). Arabic is shaped with raqm when Pillow has it,
otherwise with arabic_reshaper + python-bidi (pip install arabic-reshaper python-bidi).
"""
import json, os, re, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, features

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
RAQM = features.check("raqm") and os.environ.get("BRANDKIT_BASIC") != "1"
LAYOUT = {} if RAQM else {"layout_engine": ImageFont.Layout.BASIC}

FONT_FILES = {  # family -> (regular, bold, black)
    "Tajawal": ("Tajawal-Regular.ttf", "Tajawal-Bold.ttf", "Tajawal-Black.ttf"),
    "Cairo": ("Cairo-VF.ttf", "Cairo-VF.ttf", "Cairo-VF.ttf"),
    "IBM Plex Sans Arabic": ("IBMPlexSansArabic-Regular.ttf", "IBMPlexSansArabic-Bold.ttf", "IBMPlexSansArabic-Bold.ttf"),
}
SIZES = {"post": (1080, 1350), "story": (1080, 1920), "square": (1080, 1080), "reel": (1080, 1920)}


# ---------------------------------------------------------------- brand
def load_brand(path):
    with open(path, encoding="utf-8") as f:
        b = json.load(f)
    base = os.path.dirname(os.path.abspath(path))
    c = b.get("colors", {})
    fonts = b.get("fonts", {})
    logo = b.get("logo", {})
    return {
        "name": b.get("company_name", ""), "handle": b.get("handle", ""),
        "bg": c.get("background", "#101828"), "ink": c.get("text", "#FFFFFF"),
        "acc": c.get("accent", "#F2B33D"), "acc2": c.get("accent_dark", "#C98B18"),
        "mut": c.get("muted", "#98A2B3"), "paper": c.get("card", "#F6F3EC"),
        "font": fonts.get("main", "Tajawal"),
        "font_file": os.path.join(base, fonts["custom_font_file"]) if fonts.get("custom_font_file") else "",
        "pattern": b.get("motion", {}).get("background_pattern", "dots"),
        "logo_dark": os.path.join(base, logo.get("on_dark", "logo/logo-white.png")),
        "logo_light": os.path.join(base, logo.get("on_light", "logo/logo-dark.png")),
        "logo_show": logo.get("show", "cover_only"),
        "rules": b.get("house_rules", []),
    }


def font(brand, size, weight="bold"):
    if brand.get("font_file") and os.path.isfile(brand["font_file"]):
        return ImageFont.truetype(brand["font_file"], size, **LAYOUT)
    files = FONT_FILES.get(brand.get("font"), FONT_FILES["Tajawal"])
    f = files[{"regular": 0, "bold": 1, "black": 2}[weight]]
    ft = ImageFont.truetype(os.path.join(FONT_DIR, f), size, **LAYOUT)
    if f.endswith("-VF.ttf"):
        try:
            ft.set_variation_by_axes([{"regular": 400, "bold": 700, "black": 900}[weight]])
        except Exception:
            pass
    return ft


def hexrgb(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def is_dark(h):
    r, g, b, _ = hexrgb(h)
    return (0.299 * r + 0.587 * g + 0.114 * b) < 140


# ---------------------------------------------------------------- arabic text
_AR = re.compile(r"[؀-ۿ]")


_HAS = {}


def _has_glyph(ft, ch):
    key = (getattr(ft, "path", id(ft)), ch)
    if key not in _HAS:
        _HAS[key] = ft.getmask(ch).getbbox() != ft.getmask("\uFFFF").getbbox()
    return _HAS[key]


def _shape(s, ft=None):
    """visual-order Arabic for Pillow without raqm; presentation forms the font lacks fall back to the base letter."""
    if RAQM or not _AR.search(s):
        return s
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
    except ImportError:
        return s
    out = get_display(arabic_reshaper.reshape(s))
    if ft is None:
        return out
    import unicodedata
    fixed = []
    for ch in out:
        if "\uFB50" <= ch <= "\uFEFF" and not _has_glyph(ft, ch):
            dec = unicodedata.normalize("NFKC", ch)
            fixed.append(dec[::-1] if len(dec) > 1 else dec)
        else:
            fixed.append(ch)
    return "".join(fixed)


def _kw(s):
    return {"direction": "rtl", "language": "ar"} if (RAQM and _AR.search(s)) else {}


def wlen(draw, s, ft):
    return draw.textlength(_shape(s, ft), font=ft, **_kw(s))


def parse_marked(text):
    """'كلام *مهم* هني' -> [(word, highlighted)]"""
    out = []
    for i, part in enumerate(re.split(r"\*", text)):
        for w in part.split():
            out.append((w, i % 2 == 1))
    return out


def wrap(draw, words, ft, max_w):
    lines, cur, cw = [], [], 0
    sp = wlen(draw, " ", ft)
    for w, hl in words:
        ww = wlen(draw, w, ft)
        if cur and cw + sp + ww > max_w:
            lines.append(cur); cur, cw = [], 0
        cur.append((w, hl, ww)); cw += (sp if cw else 0) + ww
    if cur:
        lines.append(cur)
    return lines


def draw_rich(img, text, ft, box, color, hl_color, align="right", line_gap=1.25, hl_style="color", rtl=True):
    """Draw text with *highlighted* words inside box=(x0,y0,x1,y1). Returns bottom y.
    hl_style: color | marker (box behind the word in hl_color, word in color)"""
    d = ImageDraw.Draw(img)
    x0, y0, x1, _ = box
    lines = wrap(d, parse_marked(text), ft, x1 - x0)
    asc, desc = ft.getmetrics()
    lh = int((asc + desc) * line_gap)
    sp = wlen(d, " ", ft)
    y = y0
    for ln in lines:
        total = sum(w[2] for w in ln) + sp * (len(ln) - 1)
        if align == "center":
            start = x0 + (x1 - x0 + total) / 2
        elif align == "left":
            start = x0 + total
        else:
            start = x1
        x = start  # RTL: first word at the right
        for w, hl, ww in (ln if rtl else ln):
            xl = x - ww
            if hl and hl_style == "marker":
                pad = int(ft.size * 0.12)
                d.rounded_rectangle((xl - pad, y + int(asc * 0.25), x + pad, y + asc + int(desc * 0.6)),
                                    radius=pad, fill=hexrgb(hl_color))
                d.text((xl, y), _shape(w, ft), font=ft, fill=hexrgb(color), **_kw(w))
            else:
                d.text((xl, y), _shape(w, ft), font=ft, fill=hexrgb(hl_color if hl else color), **_kw(w))
            x = xl - sp
        y += lh
    return y


def text_height(text, ft, width, line_gap=1.25):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    n = len(wrap(d, parse_marked(text), ft, width))
    a, b = ft.getmetrics()
    return int((a + b) * line_gap) * n


def fit_font(brand, text, width, max_h, start, minimum=40, weight="black", line_gap=1.2):
    s = start
    while s > minimum:
        ft = font(brand, s, weight)
        if text_height(text, ft, width, line_gap) <= max_h:
            return ft
        s -= 4
    return font(brand, minimum, weight)


# ---------------------------------------------------------------- backgrounds and pieces
def background(brand, size, pattern=None, glow=True, color=None):
    W, H = size
    bg = color or brand["bg"]
    img = Image.new("RGBA", size, hexrgb(bg))
    pat = pattern or brand.get("pattern", "dots")
    dark = is_dark(bg)
    dot = (255, 255, 255, 22) if dark else (0, 0, 0, 20)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if pat == "dots":
        for yy in range(18, H, 36):
            for xx in range(18, W, 36):
                d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=dot)
    elif pat == "grid":
        for xx in range(0, W, 72):
            d.line((xx, 0, xx, H), fill=dot, width=1)
        for yy in range(0, H, 72):
            d.line((0, yy, W, yy), fill=dot, width=1)
    img = Image.alpha_composite(img, layer)
    if glow:
        g = Image.new("RGBA", size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        r = int(W * 0.55)
        ac = hexrgb(brand["acc"], 60 if dark else 40)
        gd.ellipse((W * 0.75 - r, H * 0.15 - r, W * 0.75 + r, H * 0.15 + r), fill=ac)
        g = g.filter(ImageFilter.GaussianBlur(W // 5))
        img = Image.alpha_composite(img, g)
    return img


def paste_logo(img, brand, where="top-right", width_pct=0.16, margin=60):
    path = brand["logo_dark"] if is_dark(brand["bg"]) else brand["logo_light"]
    if not os.path.isfile(path):
        return
    lg = Image.open(path).convert("RGBA")
    w = int(img.width * width_pct)
    lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS)
    x = img.width - w - margin if "right" in where else margin
    y = margin if "top" in where else img.height - lg.height - margin
    img.alpha_composite(lg, (x, y))


def tag(img, brand, text, xy_right, size=38):
    """pill tag in accent color, anchored at its right edge (RTL)."""
    d = ImageDraw.Draw(img)
    ft = font(brand, size, "bold")
    tw = wlen(d, text, ft)
    pad = int(size * 0.6)
    x1, y = xy_right
    x0 = x1 - tw - 2 * pad
    h = int(size * 1.7)
    d.rounded_rectangle((x0, y, x1, y + h), radius=h // 2, fill=hexrgb(brand["acc"]))
    ink = brand["bg"] if not is_dark(brand["acc"]) else "#FFFFFF"
    d.text((x1 - pad - tw, y + (h - size * 1.25) / 2), _shape(text, ft), font=ft, fill=hexrgb(ink), **_kw(text))
    return y + h


def photo_card(img, path, box, tilt=0, tape=True, brand=None):
    """real photo on a white card with tape, fitted in box."""
    if not path or not os.path.isfile(path):
        return
    x0, y0, x1, y1 = box
    ph = Image.open(path).convert("RGB")
    bw, bh = x1 - x0, y1 - y0
    pad = 18
    iw, ih = bw - 2 * pad, bh - 2 * pad
    r = max(iw / ph.width, ih / ph.height)
    ph = ph.resize((int(ph.width * r), int(ph.height * r)), Image.LANCZOS)
    l, t = (ph.width - iw) // 2, (ph.height - ih) // 2
    ph = ph.crop((l, t, l + iw, t + ih))
    card = Image.new("RGBA", (bw, bh), (255, 255, 255, 255))
    card.paste(ph, (pad, pad))
    if tape:
        td = ImageDraw.Draw(card)
        td.rectangle((bw // 2 - 70, 0, bw // 2 + 70, 34), fill=(255, 240, 180, 200))
    if tilt:
        card = card.rotate(tilt, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 90), mask=card.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    img.alpha_composite(sh, (x0 + 8, y0 + 14))
    img.alpha_composite(card, (x0, y0))


def counter(img, brand, i, n, y=70, margin=60):
    if n <= 1:
        return
    d = ImageDraw.Draw(img)
    W = img.width
    seg_w = (W - 2 * margin - (n - 1) * 8) / n
    for k in range(n):
        x = margin + k * (seg_w + 8)
        on = k <= i
        d.rounded_rectangle((x, y, x + seg_w, y + 8), radius=4,
                            fill=hexrgb(brand["acc"] if on else brand["mut"], 255 if on else 90))
