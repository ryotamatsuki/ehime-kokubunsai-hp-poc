#!/usr/bin/env python3
"""Build local responsive images and OFL font subsets for the D2 lab."""
import argparse
import hashlib
import json
from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools import subset

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "design-lab"
FONT_REF = "9710da1eacb3be272583c3224dcb70f9da6eadbb"
FONT_SOURCES = [
    ("zenkakugothicnew", "ZenKakuGothicNew-Regular.ttf", "b840cd07a67d89cacca44249ae49aa99ee7640eb5ce623be8d8983d6aabac801", "ehime-sans-regular.woff2", "Ehime Lab Sans"),
    ("zenkakugothicnew", "ZenKakuGothicNew-Bold.ttf", "0081cedabc4921982fcd061f845a005664ac7fb642af2dd34b4007bc63ccd235", "ehime-sans-bold.woff2", "Ehime Lab Sans"),
    ("manrope", "Manrope[wght].ttf", "3ae11c49db0455a3cc33e37d380f20fdb8c7f8b41dc07625c177e3d87a9d6ae6", "ehime-latin.woff2", "Ehime Lab Latin"),
]
PHOTOS = [
    "hero-ehime-culture-festival", "tobe-ceramics-workshop", "inclusive-art-gallery",
    "event-stage-lanterns", "family-culture-workshop", "uwajima-sea-culture", "uchiko-ozu-townscape",
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def build(font_dir):
    photo_dir = LAB / "assets/photos"
    font_out = LAB / "assets/fonts"
    photo_dir.mkdir(parents=True, exist_ok=True)
    font_out.mkdir(parents=True, exist_ok=True)
    font_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"version": "2.0.0-alpha.4", "photos": [], "fonts": [], "font_source_ref": FONT_REF}
    for name in PHOTOS:
        source = ROOT / ("assets/" + name + ".jpg")
        im = Image.open(source).convert("RGB")
        src_width, src_height = im.size
        for width in [480, 960, 1440]:
            height = round(src_height * width / src_width)
            output = photo_dir / f"{name}-{width}.webp"
            buffer = BytesIO()
            im.resize((width, height), Image.Resampling.LANCZOS).save(buffer, "WEBP", quality=78, method=6)
            data = buffer.getvalue()
            pending = output.with_suffix(".webp.pending")
            pending.write_bytes(data)
            pending.replace(output)
            manifest["photos"].append(dict(path=output.relative_to(ROOT).as_posix(), source=source.relative_to(ROOT).as_posix(), source_sha256=sha(source.read_bytes()), width=width, height=height, bytes=len(data), sha256=sha(data)))
    # Union of current v1 and D2 text. Characters added later use the system fallback.
    text = "".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("*.html") if p.name != "review.html")
    text += "".join(p.read_text(encoding="utf-8") for p in LAB.glob("*.js"))
    unicodes = sorted({ord(c) for c in text} | set(range(32, 127)))
    manifest["subset_character_count"] = len(unicodes)
    for directory, name, expected, dest, family in FONT_SOURCES:
        source = font_dir / name
        url = f"https://raw.githubusercontent.com/google/fonts/{FONT_REF}/ofl/{directory}/{name}"
        if not source.exists() or not source.stat().st_size:
            with urlopen(url.replace("[", "%5B").replace("]", "%5D"), timeout=30) as response:
                source.write_bytes(response.read())
        source_data = source.read_bytes()
        if sha(source_data) != expected:
            raise ValueError(f"Font source hash mismatch: {name}")
        font = TTFont(source, recalcTimestamp=False)
        options = subset.Options()
        options.flavor = "woff2"
        options.layout_features = ["*"]
        options.name_IDs = ["*"]
        options.name_legacy = True
        options.name_languages = ["*"]
        tool = subset.Subsetter(options=options)
        tool.populate(unicodes=unicodes)
        tool.subset(font)
        for record in font["name"].names:
            if record.nameID in [1, 4, 6, 16]:
                replacement = family.replace(" ", "") if record.nameID == 6 else family
                record.string = replacement.encode(record.getEncoding())
        font.flavor = "woff2"
        output = font_out / dest
        font.save(output)
        data = output.read_bytes()
        manifest["fonts"].append(dict(path=output.relative_to(ROOT).as_posix(), family=family, source_url=url, source_sha256=expected, bytes=len(data), sha256=sha(data), license="SIL Open Font License 1.1"))
    for directory, filename in [("zenkakugothicnew","ZenKakuGothicNew-OFL.txt"),("manrope","Manrope-OFL.txt")]:
        source = font_dir / filename
        if not source.exists():
            with urlopen(f"https://raw.githubusercontent.com/google/fonts/{FONT_REF}/ofl/{directory}/OFL.txt", timeout=30) as response:
                source.write_bytes(response.read())
        (font_out / filename).write_bytes(source.read_bytes())
    (LAB / "assets/manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"responsive_photos":len(manifest["photos"]),"photo_bytes":sum(p["bytes"] for p in manifest["photos"]),"font_bytes":sum(f["bytes"] for f in manifest["fonts"]),"subset_characters":len(unicodes)}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--font-source-dir", type=Path, default=ROOT / ".cache/v2-font-sources")
    args = parser.parse_args()
    build(args.font_source_dir)
