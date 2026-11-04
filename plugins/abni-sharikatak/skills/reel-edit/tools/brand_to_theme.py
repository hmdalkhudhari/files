#!/usr/bin/env python3
"""brand.json -> theme.json (for the majed-video engine) + house.json (extra house settings).

Usage:
  python brand_to_theme.py <kit_folder> <work_folder>      write theme.json + logo.png + house.json into work_folder
  python brand_to_theme.py <kit_folder> --check            only check brand.json (colors, logo, font) and print problems
"""
import json, os, re, shutil, sys

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
CAP_STYLES = {"card", "shadow", "big", "underline", "bar", "type"}
BUILTIN_FONTS = {"Tajawal", "Cairo", "IBM Plex Sans Arabic", "Noto Kufi Arabic",
                 "Readex Pro", "Lalezar", "Aref Ruqaa", "Inter"}


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def load(kit):
    p = os.path.join(kit, "brand", "brand.json")
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"brand.json فيه غلط بالكتابة (سطر {e.lineno}): غالباً فاصلة أو علامة تنصيص ناقصة.")


def check(kit, b):
    probs, warns = [], []
    c = b.get("colors", {})
    for k in ("background", "text", "accent", "accent_dark", "muted"):
        if not HEX.match(str(c.get(k, ""))):
            probs.append(f"اللون {k} لازم يكون مثل #1A2B3C (الحين: {c.get(k)!r})")
    if not probs:
        if contrast(c["text"], c["background"]) < 4.5:
            warns.append("لون الكلام قريب من لون الخلفية، الكلام بيكون صعب ينقرا.")
        if contrast(c["accent"], c["background"]) < 3:
            warns.append("لون التمييز قريب من الخلفية، الكلمة المهمة ما بتبين.")
    logo = b.get("logo", {})
    for k in ("on_dark", "on_light"):
        p = os.path.join(kit, "brand", logo.get(k, ""))
        if not os.path.isfile(p):
            warns.append(f"ما لقيت الشعار {logo.get(k)} بمجلد brand (حطه PNG شفاف).")
    fonts = b.get("fonts", {})
    ff = fonts.get("custom_font_file", "")
    if ff:
        if not os.path.isfile(os.path.join(kit, "brand", ff)):
            probs.append(f"ملف الخط {ff} مو موجود بمجلد brand/fonts.")
    elif fonts.get("main") not in BUILTIN_FONTS:
        warns.append(f"الخط {fonts.get('main')} مو من الخطوط الجاهزة، حط ملف TTF بـ brand/fonts واكتب اسمه بـ custom_font_file.")
    if b.get("captions", {}).get("style") not in CAP_STYLES:
        probs.append(f"ستايل الكابشن لازم واحد من: {', '.join(sorted(CAP_STYLES))}")
    return probs, warns


def build(kit, work, b):
    c, f, cap, out, vid = b["colors"], b.get("fonts", {}), b.get("captions", {}), b.get("outro", {}), b.get("video", {})
    theme = {
        "bg": c["background"], "ink": c["text"], "acc": c["accent"],
        "clay": c["accent_dark"], "mut": c["muted"],
        "font": f.get("main", "Tajawal"),
        "handle": b.get("handle", ""),
        "logo": "logo.png",
        "grade": False,
        "badgeUntil": 0,
        "capStyle": cap.get("style", "card"),
    }
    if vid.get("pace") == "calm":
        theme["pace"] = "calm"
    t = out.get("type", "icons")
    if t == "card":
        theme["outro"] = {"cta": out.get("big_line", "تابعنا"), "l1": out.get("small_line", ""),
                          "word": out.get("comment_word", "")}
    os.makedirs(work, exist_ok=True)
    dark_bg = lum(c["background"]) < 0.4
    logo_rel = b.get("logo", {}).get("on_dark" if dark_bg else "on_light", "")
    src = os.path.join(kit, "brand", logo_rel)
    if os.path.isfile(src):
        shutil.copy(src, os.path.join(work, "logo.png"))
    ff = f.get("custom_font_file", "")
    if ff and os.path.isfile(os.path.join(kit, "brand", ff)):
        shutil.copy(os.path.join(kit, "brand", ff), os.path.join(work, os.path.basename(ff)))
    house = {k: b.get(k) for k in ("company_name", "logo", "intro", "outro", "video", "motion", "captions", "house_rules")}
    house["handwriting_font"] = f.get("handwriting", "Aref Ruqaa")
    house["custom_font_file"] = os.path.basename(ff) if ff else ""
    with open(os.path.join(work, "theme.json"), "w", encoding="utf-8") as fh:
        json.dump(theme, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(work, "house.json"), "w", encoding="utf-8") as fh:
        json.dump(house, fh, ensure_ascii=False, indent=2)
    return theme


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    kit = sys.argv[1]
    b = load(kit)
    probs, warns = check(kit, b)
    for w in warns:
        print("⚠️ ", w)
    for p in probs:
        print("❌ ", p)
    if probs:
        sys.exit(1)
    if sys.argv[2] == "--check":
        print("✅ brand.json تمام" + (" (فيه ملاحظات فوق)" if warns else ""))
        return
    theme = build(kit, sys.argv[2], b)
    print("✅ انكتب theme.json و house.json:", json.dumps(theme, ensure_ascii=False))


if __name__ == "__main__":
    main()
