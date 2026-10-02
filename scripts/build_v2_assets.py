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
    ("zenmarugothic", "ZenMaruGothic-Medium.ttf", "3cfdb98a13571ede17fcc769f5093a97c38b80a7b9b2ab754a26b4d822092b3b", "ehime-display-medium.woff2", "Ehime Festival Display"),
]
PHOTOS = [
    "hero-ehime-culture-festival", "tobe-ceramics-workshop", "inclusive-art-gallery",
    "event-stage-lanterns", "family-culture-workshop", "uwajima-sea-culture", "uchiko-ozu-townscape",
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unicode_ranges(points):
    ranges=[];start=previous=None
    for point in points:
        if start is None:start=previous=point
        elif point==previous+1:previous=point
        else:ranges.append('U+'+format(start,'X')+('-'+format(previous,'X') if previous!=start else ''));start=previous=point
    if start is not None:ranges.append('U+'+format(start,'X')+('-'+format(previous,'X') if previous!=start else ''))
    return ','.join(ranges)

def build(font_dir):
    photo_dir = LAB / "assets/photos"
    font_out = LAB / "assets/fonts"
    photo_dir.mkdir(parents=True, exist_ok=True)
    font_out.mkdir(parents=True, exist_ok=True)
    font_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"version": json.loads((LAB/'content.json').read_text())['version'], "photos": [], "fonts": [], "referenceFonts": [], "font_source_ref": FONT_REF}
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
    text = "".join(p.read_text(encoding="utf-8") for p in ROOT.rglob("*.html") if p.name not in ["review.html","compare.html"])
    text += "".join(p.read_text(encoding="utf-8") for p in LAB.glob("*.js"))
    unicodes = sorted({ord(c) for c in text} | set(range(32, 127)))
    manifest["subset_character_count"] = len(unicodes)
    import tinyhtml5
    home=tinyhtml5.parse((LAB/'index.html').read_text(),namespace_html_elements=False).find('.//body')
    common_text=''.join(''.join(n.itertext()) for n in home if n.tag!='script')
    common_regular={ord(c) for c in common_text}|set(range(32,127))
    common_bold={ord(c) for n in home.iter() if n.tag in ['h3','strong','button'] or any(c in n.get('class','').split() for c in ['brand-name','status','label','button','header-search','text-link']) for c in ''.join(n.itertext())}|set(range(32,127))
    common_display={ord(c) for n in home.iter() if n.tag in ['h1','h2','h3','summary'] for c in ''.join(n.itertext())}|set(range(32,127))
    headings=''.join(''.join(n.itertext()) for p in LAB.glob('*.html') if p.name not in ['review.html','compare.html'] for n in tinyhtml5.parse(p.read_text(),namespace_html_elements=False).iter() if n.tag in ['h1','h2','h3','summary'])
    display_unicodes={ord(c) for c in headings}|set(range(32,127))
    font_css=[]
    reference_out=LAB/'qa/reference-fonts';reference_out.mkdir(parents=True,exist_ok=True)
    for stale in font_out.glob('*-extended*.woff2'):stale.unlink()
    for directory, name, expected, dest, family in FONT_SOURCES:
        source = font_dir / name
        url = f"https://raw.githubusercontent.com/google/fonts/{FONT_REF}/ofl/{directory}/{name}"
        if not source.exists() or not source.stat().st_size:
            with urlopen(url.replace("[", "%5B").replace("]", "%5D"), timeout=30) as response:
                source.write_bytes(response.read())
        source_data = source.read_bytes()
        if sha(source_data) != expected:
            raise ValueError(f"Font source hash mismatch: {name}")
        # WeasyPrint does not implement browser Unicode-range face selection.
        # Its static references use one equivalent full subset per weight.
        reference=TTFont(source,recalcTimestamp=False)
        options=subset.Options();options.flavor='woff2';options.layout_features=['*'];options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
        tool=subset.Subsetter(options=options);tool.populate(unicodes=unicodes);tool.subset(reference)
        for record in reference['name'].names:
            if record.nameID in [1,3,4,6,16]:
                value=dest.removesuffix('.woff2')+'-reference' if record.nameID in [3,6] else family+' Reference '+dest.removesuffix('.woff2')
                record.string=value.encode(record.getEncoding())
        reference.flavor='woff2';ref_file=reference_out/dest;reference.save(ref_file)
        css_family='Ehime Latin' if directory=='manrope' else 'Ehime Festival Display' if directory=='zenmarugothic' else 'Ehime Sans'
        weight='200 800' if directory=='manrope' else '500' if directory=='zenmarugothic' else '700' if 'Bold' in name else '400'
        manifest['referenceFonts'].append(dict(path=ref_file.relative_to(ROOT).as_posix(),cssFamily=css_family,weight=weight,bytes=ref_file.stat().st_size,sha256=sha(ref_file.read_bytes()),source_sha256=expected,method='WeasyPrint-only equivalent full subset; not a browser delivery font'))
        partitions=[('common',common_display,display_unicodes-common_display)] if directory=='zenmarugothic' else [('common',common_bold if 'Bold' in name else common_regular,set(unicodes)-(common_bold if 'Bold' in name else common_regular))]
        if directory=='manrope':partitions=[('all',set(unicodes),set())]
        for partition,first,rest in partitions:
            remaining=sorted(rest)
            pieces=[(partition,first)]+[('extended-'+str(i//64+1),set(remaining[i:i+64])) for i in range(0,len(remaining),64)]
            for part,codepoints in pieces:
                if not codepoints:continue
                font = TTFont(source, recalcTimestamp=False)
                options = subset.Options();options.flavor='woff2';options.layout_features=['*'];options.name_IDs=['*'];options.name_legacy=True;options.name_languages=['*']
                tool=subset.Subsetter(options=options);tool.populate(unicodes=sorted(codepoints));tool.subset(font)
                filename=dest if not part.startswith('extended') else dest.replace('.woff2','-'+part+'.woff2')
                # Separate PostScript identities prevent glyph-index collisions when
                # multiple Unicode shards are embedded in the same PDF or document.
                for record in font['name'].names:
                    if record.nameID in [1,3,4,6,16]:
                        replacement=filename.removesuffix('.woff2') if record.nameID in [3,6] else family+' '+filename.removesuffix('.woff2')
                        record.string=replacement.encode(record.getEncoding())
                font.flavor='woff2';output=font_out/filename;font.save(output)
                raw=output.read_bytes();cmap=sorted(font.getBestCmap());ranges=unicode_ranges(cmap)
                css_family='Ehime Latin' if directory=='manrope' else 'Ehime Festival Display' if directory=='zenmarugothic' else 'Ehime Sans'
                weight='200 800' if directory=='manrope' else '500' if directory=='zenmarugothic' else '700' if 'Bold' in name else '400'
                font_css.append('@font-face{font-family:"'+css_family+'";src:url("assets/fonts/'+filename+'") format("woff2");font-weight:'+weight+';font-style:normal;font-display:swap;unicode-range:'+ranges+'}')
                manifest['fonts'].append(dict(path=output.relative_to(ROOT).as_posix(),family=family,cssFamily=css_family,weight=weight,partition=part,unicodeRanges=ranges,codepoints=cmap,source_url=url,source_sha256=expected,bytes=len(raw),sha256=sha(raw),license='SIL Open Font License 1.1'))
    for directory, filename in [("zenkakugothicnew","ZenKakuGothicNew-OFL.txt"),("manrope","Manrope-OFL.txt"),("zenmarugothic","ZenMaruGothic-OFL.txt")]:
        source = font_dir / filename
        if not source.exists():
            with urlopen(f"https://raw.githubusercontent.com/google/fonts/{FONT_REF}/ofl/{directory}/OFL.txt", timeout=30) as response:
                source.write_bytes(response.read())
        (font_out / filename).write_bytes(source.read_bytes())
    (LAB / "assets/manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    import re
    css=(LAB/'experience.css').read_text();css=re.sub(r'@font-face\{[^}]*\}\s*','',css)
    (LAB/'experience.css').write_text('\n'.join(font_css)+'\n'+css)
    print(json.dumps({"responsive_photos":len(manifest["photos"]),"photo_bytes":sum(p["bytes"] for p in manifest["photos"]),"font_bytes":sum(f["bytes"] for f in manifest["fonts"]),"subset_characters":len(unicodes)}))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--font-source-dir", type=Path, default=ROOT / ".cache/v2-font-sources")
    args = parser.parse_args()
    build(args.font_source_dir)
