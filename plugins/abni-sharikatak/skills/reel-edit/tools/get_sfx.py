#!/usr/bin/env python3
"""Download the free sound-effects library (Mixkit Free License: free for commercial videos, no credit needed).
Usage: python get_sfx.py <kit_folder>"""
import os, sys, urllib.request

SFX = {  # file name : mixkit id
    "hook-bass-hit.mp3": 2299, "reveal-riser.mp3": 790, "cut-camera-flash.mp3": 1430,
    "typing-keyboard.mp3": 1386, "text-pop.mp3": 2364, "zoom-swish.mp3": 168, "cta-bell.mp3": 586,
    "tr-shutter.mp3": 1430, "tr-data.mp3": 3122, "tr-glitch.mp3": 2951, "tr-whoosh.mp3": 1490,
}
kit = sys.argv[1] if len(sys.argv) > 1 else "."
out = os.path.join(kit, "sfx")
os.makedirs(out, exist_ok=True)
for name, i in SFX.items():
    dst = os.path.join(out, name)
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        continue
    url = f"https://assets.mixkit.co/active_storage/sfx/{i}/{i}-preview.mp3"
    try:
        urllib.request.urlretrieve(url, dst)
        print("✅", name)
    except Exception as e:
        print("❌", name, e)
print("خلصنا. الملفات بـ", out)
