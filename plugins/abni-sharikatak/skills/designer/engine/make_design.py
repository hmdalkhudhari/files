#!/usr/bin/env python3
"""Posts, stories and carousels from a small JSON spec, in the company's brand.

  python make_design.py spec.json

spec.json:
{
  "brand": "../brand/brand.json",          (path relative to the spec file)
  "format": "post" | "story" | "square",   (post = 1080x1350 carousel/feed, story = 1080x1920)
  "out": "out/my-carousel",                (folder for PNGs, relative to the spec file)
  "slides": [
    {"type": "cover",    "tag": "سر انستقرام", "title": "سطر *الكلمة المهمة* بلون التمييز", "sub": "سطر صغير", "image": "photo.jpg"},
    {"type": "point",    "num": "1", "title": "عنوان النقطة", "body": "شرح بسطرين", "image": "optional.jpg"},
    {"type": "stat",     "number": "63%", "label": "من العملاء…", "note": "المصدر: …"},
    {"type": "list",     "title": "٣ أشياء", "items": ["…", "…", "…"]},
    {"type": "quote",    "text": "جملة قوية", "by": "اسم"},
    {"type": "question", "title": "سؤال للستوري", "sub": "صوّت تحت"},   (story: leaves the sticker area empty)
    {"type": "cta",      "title": "عجبك؟", "keyword": "عرض", "line": "اكتب الكلمة بالتعليقات ويوصلك"}
  ]
}
Words between *stars* get the accent color.
"""
import json, os, sys
from PIL import Image, ImageDraw
import brandkit as bk


def safe_area(fmt, W, H):
    if fmt == "story":
        return 80, 260, W - 80, H - 360      # IG story top/bottom UI
    return 80, 150, W - 80, H - 110


def slide_cover(img, b, s, fmt):
    W, H = img.size
    x0, y0, x1, y1 = safe_area(fmt, W, H)
    has_img = bool(s.get("image")) and os.path.isfile(s.get("image", ""))
    y = y0 + (40 if fmt == "story" else 70)
    if s.get("tag"):
        y = bk.tag(img, b, s["tag"], (x1, y), 40) + 40
    title_h = int((y1 - y) * (0.42 if has_img else 0.6))
    ft = bk.fit_font(b, s["title"], x1 - x0, title_h, 150, 64)
    y = bk.draw_rich(img, s["title"], ft, (x0, y, x1, y1), b["ink"], b["acc"], line_gap=1.15)
    if s.get("sub"):
        y = bk.draw_rich(img, s["sub"], bk.font(b, 46, "bold"), (x0, y + 20, x1, y1), b["mut"], b["acc"]) + 10
    if has_img:
        top = y + 50
        h = min(y1 - top, int((x1 - x0) * 0.8))
        w = int(h * 1.15) if h * 1.15 < (x1 - x0) else x1 - x0
        bk.photo_card(img, s["image"], (x1 - w - 10, top, x1 - 10, top + h), tilt=-3)


def slide_point(img, b, s, fmt):
    W, H = img.size
    x0, y0, x1, y1 = safe_area(fmt, W, H)
    y = y0 + 60
    d = ImageDraw.Draw(img)
    if s.get("num"):
        nf = bk.font(b, 150, "black")
        d.text((x1, y - 20), str(s["num"]), font=nf, fill=bk.hexrgb(b["acc"]), anchor="ra")
        y += 170
    ft = bk.fit_font(b, s["title"], x1 - x0, 330, 96, 56)
    y = bk.draw_rich(img, s["title"], ft, (x0, y, x1, y1), b["ink"], b["acc"], line_gap=1.15) + 30
    if s.get("body"):
        y = bk.draw_rich(img, s["body"], bk.font(b, 50, "regular"), (x0, y, x1, y1), b["mut"], b["acc"], line_gap=1.45)
    if s.get("image") and os.path.isfile(s["image"]):
        top = y + 50
        if y1 - top > 250:
            bk.photo_card(img, s["image"], (x0 + 60, top, x1 - 60, min(y1, top + 620)), tilt=2)


def slide_stat(img, b, s, fmt):
    W, H = img.size
    x0, y0, x1, y1 = safe_area(fmt, W, H)
    d = ImageDraw.Draw(img)
    cy = (y0 + y1) // 2 - 150
    nf = bk.font(b, 300, "black")
    while d.textlength(s["number"], font=nf) > x1 - x0 and nf.size > 120:
        nf = bk.font(b, nf.size - 20, "black")
    d.text((W // 2, cy), s["number"], font=nf, fill=bk.hexrgb(b["acc"]), anchor="mm")
    y = cy + nf.size // 2 + 40
    y = bk.draw_rich(img, s.get("label", ""), bk.fit_font(b, s.get("label", ""), x1 - x0, 260, 72, 44, "bold"),
                     (x0, y, x1, y1), b["ink"], b["acc"], align="center")
    if s.get("note"):
        bk.draw_rich(img, s["note"], bk.font(b, 34, "regular"), (x0, y + 30, x1, y1), b["mut"], b["acc"], align="center")


def slide_list(img, b, s, fmt):
    W, H = img.size
    x0, y0, x1, y1 = safe_area(fmt, W, H)
    y = y0 + 60
    ft = bk.fit_font(b, s.get("title", ""), x1 - x0, 260, 92, 56)
    y = bk.draw_rich(img, s.get("title", ""), ft, (x0, y, x1, y1), b["ink"], b["acc"], line_gap=1.15) + 40
    d = ImageDraw.Draw(img)
    items = s.get("items", [])
    room = (y1 - y) // max(1, len(items))
    isz = max(40, min(60, room // 3))
    for it in items:
        d.ellipse((x1 - 26, y + isz * 0.45, x1, y + isz * 0.45 + 26), fill=bk.hexrgb(b["acc"]))
        y = bk.draw_rich(img, it, bk.font(b, isz, "bold"), (x0, y, x1 - 50, y1), b["ink"], b["acc"], line_gap=1.3) + 24


def slide_quote(img, b, s, fmt):
    W, H = img.size
    x0, y0, x1, y1 = safe_area(fmt, W, H)
    d = ImageDraw.Draw(img)
    d.text((x1, y0 + 40), "”", font=bk.font(b, 260, "black"), fill=bk.hexrgb(b["acc"]), anchor="ra")
    ft = bk.fit_font(b, s["text"], x1 - x0, int((y1 - y0) * 0.55), 100, 52)
    y = bk.draw_rich(img, s["text"], ft, (x0, y0 + 300, x1, y1), b["ink"], b["acc"], line_gap=1.25)
    if s.get("by"):
        bk.draw_rich(img, "— " + s["by"], bk.font(b, 42, "bold"), (x0, y + 30, x1, y1), b["mut"], b["acc"])


def slide_question(img, b, s, fmt):
    W, H = img.size
    x0, y0, x1, y1 = safe_area(fmt, W, H)
    y = y0 + 60
    if s.get("tag"):
        y = bk.tag(img, b, s["tag"], (x1, y), 40) + 40
    ft = bk.fit_font(b, s["title"], x1 - x0, 420, 110, 60)
    y = bk.draw_rich(img, s["title"], ft, (x0, y, x1, y1), b["ink"], b["acc"], line_gap=1.15)
    if s.get("sub"):
        bk.draw_rich(img, s["sub"], bk.font(b, 44, "bold"), (x0, y + 20, x1, y1), b["mut"], b["acc"])
    # sticker area left empty on purpose (poll / question sticker is added in the app)
    d = ImageDraw.Draw(img)
    sy = int(H * 0.56)
    d.rounded_rectangle((x0 + 60, sy, x1 - 60, sy + 300), radius=40, outline=bk.hexrgb(b["mut"], 70), width=3)


def slide_cta(img, b, s, fmt):
    W, H = img.size
    x0, y0, x1, y1 = safe_area(fmt, W, H)
    y = y0 + 120
    ft = bk.fit_font(b, s.get("title", ""), x1 - x0, 300, 110, 60)
    y = bk.draw_rich(img, s.get("title", ""), ft, (x0, y, x1, y1), b["ink"], b["acc"], align="center", line_gap=1.15) + 50
    d = ImageDraw.Draw(img)
    if s.get("keyword"):
        kf = bk.font(b, 120, "black")
        kw = s["keyword"]
        tw = bk.wlen(d, kw, kf)
        bw = tw + 140
        d.rounded_rectangle((W / 2 - bw / 2, y, W / 2 + bw / 2, y + 190), radius=40, fill=bk.hexrgb(b["acc"]))
        ink = b["bg"] if not bk.is_dark(b["acc"]) else "#FFFFFF"
        d.text((W / 2 - tw / 2, y + 10), bk._shape(kw, kf), font=kf, fill=bk.hexrgb(ink), **bk._kw(kw))
        y += 240
    if s.get("line"):
        bk.draw_rich(img, s["line"], bk.font(b, 48, "bold"), (x0, y, x1, y1), b["mut"], b["acc"], align="center")
    if b.get("handle"):
        hf = bk.font(b, 40, "bold")
        d.text((W // 2, y1 - 20), b["handle"], font=hf, fill=bk.hexrgb(b["ink"]), anchor="ms")


DRAW = {"cover": slide_cover, "point": slide_point, "stat": slide_stat, "list": slide_list,
        "quote": slide_quote, "question": slide_question, "cta": slide_cta}


def render(spec_path):
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    base = os.path.dirname(os.path.abspath(spec_path))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    b = bk.load_brand(rel(spec["brand"]))
    fmt = spec.get("format", "post")
    size = bk.SIZES[fmt]
    out = rel(spec.get("out", "out"))
    os.makedirs(out, exist_ok=True)
    slides = spec["slides"]
    files = []
    for i, s in enumerate(slides):
        s = dict(s)
        if s.get("image"):
            s["image"] = rel(s["image"])
        img = bk.background(b, size, pattern=spec.get("pattern"), glow=s["type"] in ("cover", "cta", "stat"))
        DRAW[s["type"]](img, b, s, fmt)
        if fmt == "post" and len(slides) > 1 and s["type"] != "cover":
            bk.counter(img, b, i, len(slides))
        show = b["logo_show"]
        if (show == "corner") or (show in ("cover_only", "intro") and i == 0):
            bk.paste_logo(img, b, "top-left" if fmt != "story" else "top-left", 0.16,
                          margin=60 if fmt != "story" else 120)
        p = os.path.join(out, f"{i + 1:02d}.png")
        img.convert("RGB").save(p, quality=95)
        files.append(p)
    print("✅", len(files), "صور بـ", out)
    return files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    render(sys.argv[1])
