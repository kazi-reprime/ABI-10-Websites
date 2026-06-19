"""Import + sanitize barbershop media into assets/showcase/{vid,img} with web-safe names."""
from __future__ import annotations
import re, shutil, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path("/Users/mkazi/Downloads/download (1)")
OUT_VID = ROOT / "assets" / "showcase" / "vid"
OUT_IMG = ROOT / "assets" / "showcase" / "img"
OUT_VID.mkdir(parents=True, exist_ok=True)
OUT_IMG.mkdir(parents=True, exist_ok=True)

TS = re.compile(r"_?202606190806(_\d+)?$")  # trailing export timestamp (+ optional dup marker)

def slugify(stem: str) -> str:
    stem = unicodedata.normalize("NFKD", stem).encode("ascii", "ignore").decode()  # drop unicode (…, etc.)
    stem = TS.sub("", stem)                       # strip export timestamp
    stem = re.sub(r"\.jpeg$|\.jpg$|\.png$", "", stem, flags=re.I)  # stray inner ext (e.g. img_8676.jpeg_...)
    stem = stem.lower()
    stem = re.sub(r"[^a-z0-9]+", "-", stem)        # everything non-alnum -> dash
    stem = re.sub(r"-+", "-", stem).strip("-")
    return stem or "media"

def unique(name: str, used: set) -> str:
    base, n = name, 2
    while name in used:
        name = f"{base}-{n}"; n += 1
    used.add(name)
    return name

def run():
    vids, imgs = {}, {}
    used_v, used_i = set(), set()
    for f in sorted(SRC.iterdir()):
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        if ext == ".mp4":
            name = unique(slugify(f.stem), used_v) + ".mp4"
            shutil.copy2(f, OUT_VID / name); vids[f.name] = name
        elif ext in (".jpeg", ".jpg", ".png"):
            name = unique(slugify(f.stem), used_i) + ".jpeg"
            shutil.copy2(f, OUT_IMG / name); imgs[f.name] = name
    print(f"videos: {len(vids)}  -> {OUT_VID}")
    for v in sorted(vids.values()): print("  vid", v)
    print(f"images: {len(imgs)}  -> {OUT_IMG}")
    for v in sorted(imgs.values()): print("  img", v)

if __name__ == "__main__":
    run()
