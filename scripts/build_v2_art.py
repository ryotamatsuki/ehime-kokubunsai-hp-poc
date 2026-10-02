#!/usr/bin/env python3
"""Encode web delivery sizes from new original imagegen masters; no creative edits."""
from pathlib import Path
from io import BytesIO
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'design-lab'

def main():
    out = LAB / 'assets/art'
    out.mkdir(parents=True,exist_ok=True)
    manifest = {'version':json.loads((ROOT/'design-lab/content.json').read_text())['version'],'method':'built-in image_gen; delivery encoding only','images':[]}
    for name in ['porcelain-hero','craft-hands']+[r['id'] for r in json.loads((LAB/'assets/event-image-prompts.json').read_text())['images']]:
        source = LAB / ('assets/art-masters/'+name+'.png')
        image = Image.open(source).convert('RGB')
        for width in [480,960,1440]:
            height = round(width*image.height/image.width)
            buf = BytesIO()
            image.resize((width,height),Image.Resampling.LANCZOS).save(buf,'WEBP',quality=82,method=6)
            data = buf.getvalue()
            destination = out / f'{name}-{width}.webp'
            temporary = destination.with_suffix('.webp.pending')
            temporary.write_bytes(data); temporary.replace(destination)
            manifest['images'].append({'path':destination.relative_to(ROOT).as_posix(),'source':source.relative_to(ROOT).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'width':width,'height':height,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    (LAB/'assets/art-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'responsiveArt':len(manifest['images']),'bytes':sum(i['bytes'] for i in manifest['images'])}))

if __name__=='__main__':main()
