#!/usr/bin/env python3
"""Motion-graphics reel (1080x1920) from text scenes, on music or silent, in the company's brand.
No voice needed. Cuts land on the music beats.

  python make_motion.py spec.json

spec.json:
{
  "brand": "../brand/brand.json",
  "out": "out/my-motion.mp4",
  "music": "song.mp3",            (optional; without it the video is silent and music is added in the app)
  "music_start": 0,               (second in the song to start from)
  "beats_per_scene": 4,           (with music: each scene lasts this many beats, 2-8)
  "scenes": [
    {"lines": ["سطر صغير", "سطر *كبير* فيه الكلمة المهمة"]},
    {"number": "63%", "lines": ["من العملاء…"]},
    {"tag": "خطوة ١", "lines": ["…"], "image": "photo.jpg"},
    {"motion": "steps", "title": "...", "steps": ["...", "..."]},   (animated scene, see motions.py for ids/fields)
    {"end": true}                  (closing scene: logo + handle + comment box / follow, from brand.json)
  ],
  "seconds_per_scene": 2.5        (without music)
}
In "lines": the first line is drawn small (muted color) when there are 2+ lines; the last line is big.
"""
import json, os, sys, math, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw
import brandkit as bk
import motions as mo

FPS = 30
W, H = 1080, 1920


def ffmpeg_bin():
    p = shutil.which("ffmpeg")
    if p:
        return p
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ما فيه ffmpeg. ثبّته (أو: pip install imageio-ffmpeg) وعيد.")


# ------------------------------------------------------------ beats
def beats(path, start, dur, ff):
    sr = 22050
    raw = subprocess.run([ff, "-v", "error", "-ss", str(start), "-t", str(dur + 2), "-i", path,
                          "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    if len(x) < sr:
        return None, []
    hop = 512
    n = len(x) // hop
    frames = x[: n * hop].reshape(n, hop)
    spec = np.abs(np.fft.rfft(frames * np.hanning(hop), axis=1))
    flux = np.maximum(0, np.diff(np.log1p(spec), axis=0)).sum(axis=1)
    flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    fps = sr / hop
    # tempo by autocorrelation in 70-180 bpm
    ac = np.correlate(flux, flux, "full")[len(flux) - 1:]
    lo, hi = int(fps * 60 / 180), int(fps * 60 / 70)
    lag = lo + int(np.argmax(ac[lo:hi]))
    period = lag / fps
    # phase: offset that best matches onsets
    best, phase = -1, 0
    for k in range(lag):
        sc = flux[k::lag].sum()
        if sc > best:
            best, phase = sc, k
    t0 = phase / fps
    bt = list(np.arange(t0, dur + period, period))
    return 60 / period, bt


# ------------------------------------------------------------ scene layout (static layers)
def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def build_scene(b, sc):
    """returns list of (layer RGBA full-frame, y_center, kind) drawn once."""
    layers = []
    x0, x1 = 90, W - 90
    top = 620
    if sc.get("end"):
        return build_end(b, sc)
    y = top
    if sc.get("tag"):
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        y2 = bk.tag(L, b, sc["tag"], (x1, y), 44)
        layers.append((L, "tag"))
        y = y2 + 50
    if sc.get("number"):
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(L)
        nf = bk.font(b, 280, "black")
        while d.textlength(sc["number"], font=nf) > x1 - x0 and nf.size > 120:
            nf = bk.font(b, nf.size - 20, "black")
        d.text((W // 2, y + nf.size // 2), sc["number"], font=nf, fill=bk.hexrgb(b["acc"]), anchor="mm")
        layers.append((L, "number"))
        y += nf.size + 40
    lines = sc.get("lines", [])
    for i, ln in enumerate(lines):
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        small = len(lines) > 1 and i == 0 and not sc.get("number")
        if small:
            ft = bk.font(b, 58, "bold")
            col = b["mut"]
        else:
            ft = bk.fit_font(b, ln, x1 - x0, 520, 120 if not sc.get("number") else 84, 56)
            col = b["ink"]
        y = bk.draw_rich(L, ln, ft, (x0, y, x1, H - 400), col, b["acc"],
                         align="center" if sc.get("number") else "right", line_gap=1.15) + 24
        layers.append((L, "line"))
    if sc.get("image") and os.path.isfile(sc["image"]):
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        top_i = y + 40
        h = min(H - 380 - top_i, 640)
        if h > 220:
            bk.photo_card(L, sc["image"], (x0 + 80, top_i, x1 - 80, top_i + h), tilt=-2)
            layers.append((L, "image"))
    return layers


def build_end(b, sc):
    layers = []
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    path = b["logo_dark"] if bk.is_dark(b["bg"]) else b["logo_light"]
    if os.path.isfile(path):
        lg = Image.open(path).convert("RGBA")
        lw = int(W * 0.34)
        lh = int(lg.height * lw / lg.width)
        if lh > 260:
            lw, lh = int(lw * 260 / lh), 260
        lg = lg.resize((lw, lh), Image.LANCZOS)
        L.alpha_composite(lg, ((W - lw) // 2, 780 - lh))
    layers.append((L, "logo"))
    end = sc.get("style") or b.get("end", "comment_box")
    word = sc.get("word") or b.get("comment_word", "")
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    y = 860
    if end == "comment_box" and word:
        bk.draw_rich(L, sc.get("line", "اكتب بالتعليقات"), bk.font(b, 56, "bold"), (90, y, W - 90, H), b["mut"], b["acc"], align="center")
        layers.append((L, "line"))
        layers.append(("TYPE", word))
    else:
        txt = sc.get("line") or b.get("cta", "تابعنا")
        bk.draw_rich(L, f"*{txt}*", bk.font(b, 110, "black"), (90, y, W - 90, H), b["ink"], b["acc"], align="center")
        layers.append((L, "line"))
    if b.get("handle"):
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(L)
        d.text((W // 2, 1380), b["handle"], font=bk.font(b, 48, "bold"), fill=bk.hexrgb(b["ink"]), anchor="mm")
        layers.append((L, "handle"))
    return layers


def comment_box(b, word, t):
    """typing comment box; t = seconds since start of typing"""
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    x0, x1, y = 150, W - 150, 1040
    d.rounded_rectangle((x0, y, x1, y + 130), radius=65, fill=(255, 255, 255, 240))
    n = min(len(word), int(t / 0.12) + 1) if t >= 0 else 0
    s = word[:n]
    ft = bk.font(b, 60, "bold")
    if s:
        tw = bk.wlen(d, s, ft)
        d.text((x1 - 60 - tw, y + 28), bk._shape(s, ft), font=ft, fill=(20, 20, 20, 255), **bk._kw(s))
    if int(t * 2) % 2 == 0 and n < len(word):
        cx = x1 - 60 - (bk.wlen(d, s, ft) if s else 0) - 8
        d.rectangle((cx, y + 35, cx + 4, y + 95), fill=(20, 20, 20, 255))
    if n >= len(word) and t > len(word) * 0.12 + 0.4:
        ft2 = bk.font(b, 44, "bold")
        d.rounded_rectangle((x0 + 60, y + 170, x1 - 60, y + 270), radius=30, fill=bk.hexrgb(b["acc"]))
        ink = b["bg"] if not bk.is_dark(b["acc"]) else "#FFFFFF"
        msg = "وصلتك بالخاص"
        d.text((W // 2, y + 220), bk._shape(msg, ft2), font=ft2, fill=bk.hexrgb(ink), anchor="mm", **bk._kw(msg))
    return L


# ------------------------------------------------------------ render
def render(spec_path):
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    base = os.path.dirname(os.path.abspath(spec_path))
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    bpath = rel(spec["brand"])
    b = bk.load_brand(bpath)
    raw = json.load(open(bpath, encoding="utf-8"))
    b["end"] = raw.get("motion", {}).get("end", "comment_box")
    b["comment_word"] = raw.get("outro", {}).get("comment_word", "")
    b["cta"] = raw.get("outro", {}).get("big_line", "تابعنا")
    ff = ffmpeg_bin()
    scenes = spec["scenes"]
    for sc in scenes:
        if sc.get("image"):
            sc["image"] = rel(sc["image"])

    # ---- timing
    music = rel(spec["music"]) if spec.get("music") else None
    bt, bpm = [], None
    if music and not os.path.isfile(music):
        print("⚠️ ملف الموسيقى مو موجود، بيطلع الفيديو بدون موسيقى:", music); music = None
    if music:
        est = len(scenes) * 3 + 4
        bpm, bt = beats(music, spec.get("music_start", 0), est, ff)
        if bpm is None:
            print("⚠️ ما قدرت أقرا ملف الموسيقى، بيطلع الفيديو بدون موسيقى."); music = None
    if bt:
        per = spec.get("beats_per_scene", 4)
        period = 60 / bpm
        while per * period < 1.6:
            per *= 2
        while per * period > 4.0 and per > 1:
            per //= 2
        bounds = [0.0]
        k = 0
        for i, sc in enumerate(scenes):
            k += per * (2 if sc.get("end") or sc.get("motion") else 1)
            bounds.append(bt[k] if k < len(bt) else bounds[-1] + per * period)
        beat_times = [t for t in bt if t <= bounds[-1]]
    else:
        sps = spec.get("seconds_per_scene", 2.5)
        bounds = [0.0]
        for sc in scenes:
            bounds.append(bounds[-1] + (sc.get("seconds") or (sps * 1.6 if sc.get("end") else (3.6 if sc.get("motion") else sps))))
        beat_times = []
    total = bounds[-1]
    nframes = int(round(total * FPS))

    # ---- static pieces
    bg = bk.background(b, (W, H), pattern=raw.get("motion", {}).get("background_pattern", "dots"),
                       glow=raw.get("motion", {}).get("glow", True))
    built = [[] if sc.get("motion") else build_scene(b, sc) for sc in scenes]
    corner_logo = None
    if b["logo_show"] == "corner":
        corner_logo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        bk.paste_logo(corner_logo, b, "top-left", 0.14, margin=110)

    out = rel(spec.get("out", "out/motion.mp4"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    silent = out[:-4] + "_silent.mp4"
    p = subprocess.Popen([ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                          "-preset", "medium", silent], stdin=subprocess.PIPE)
    for fi in range(nframes):
        t = fi / FPS
        si = max(0, min(len(scenes) - 1, next(i for i in range(len(scenes)) if t < bounds[i + 1] or i == len(scenes) - 1)))
        ts, te = bounds[si], bounds[si + 1]
        lt = t - ts
        frame = bg.copy()
        # beat pulse
        pulse = 0.0
        for bb in beat_times:
            if 0 <= t - bb < 0.18:
                pulse = 1 - (t - bb) / 0.18
        out_a = 1.0 if (te - t) > 0.18 or si == len(scenes) - 1 else (te - t) / 0.18
        layer = mo.draw(b, scenes[si], lt, te - ts) if scenes[si].get("motion") else Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for j, item in enumerate(built[si]):
            if item[0] == "TYPE":
                layer.alpha_composite(comment_box(b, item[1], lt - 0.6))
                continue
            L, kind = item
            st = 0.08 + j * 0.14
            e = ease_out((lt - st) / 0.45)
            if e <= 0:
                continue
            dy = int((1 - e) * 70)
            a = e * out_a
            piece = L if a >= 0.999 else Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 0)), L, a)
            if kind == "number" and e < 1:
                piece = piece.resize((W, H)).copy()
            layer.alpha_composite(piece, (0, dy))
        if pulse > 0:
            s = 1 + 0.025 * pulse
            big = layer.resize((int(W * s), int(H * s)), Image.BILINEAR)
            layer = big.crop(((big.width - W) // 2, (big.height - H) // 2, (big.width - W) // 2 + W, (big.height - H) // 2 + H))
        frame.alpha_composite(layer)
        if corner_logo is not None:
            frame.alpha_composite(corner_logo)
        p.stdin.write(frame.convert("RGB").tobytes())
    p.stdin.close()
    p.wait()

    if music:
        ms = spec.get("music_start", 0)
        subprocess.run([ff, "-y", "-v", "error", "-i", silent, "-ss", str(ms), "-t", f"{total:.3f}", "-i", music,
                        "-filter_complex", f"[1:a]afade=t=out:st={max(0, total - 1.2):.3f}:d=1.2,loudnorm=I=-14:TP=-1.5,apad,atrim=0:{total:.3f}[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out], check=True)
        os.remove(silent)
        print(f"✅ {out}  ({total:.1f}s, {bpm:.0f} BPM)" if bpm else f"✅ {out}")
    else:
        os.replace(silent, out)
        print(f"✅ {out}  ({total:.1f}s، بدون موسيقى، حط الصوت من التطبيق)")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    render(sys.argv[1])
