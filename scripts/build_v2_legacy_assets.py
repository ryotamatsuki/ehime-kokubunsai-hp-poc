"""Encode responsive delivery files for the original v1 raster assets in use."""
from pathlib import Path
import hashlib,json,re
from io import BytesIO
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]

def main():
    referenced=set()
    for page in (ROOT/'comparison/v1').rglob('*.html'):
        for name in re.findall(r'assets/([\w-]+\.(?:jpg|png))',page.read_text()):referenced.add(name)
    out=ROOT/'design-lab/assets/legacy';out.mkdir(parents=True,exist_ok=True);records=[]
    for name in sorted(referenced):
        source=ROOT/'assets'/name
        with Image.open(source) as opened:image=opened.convert('RGB')
        for width in [480,960,1440]:
            height=round(width*image.height/image.width);buf=BytesIO()
            image.resize((width,height),Image.Resampling.LANCZOS).save(buf,'WEBP',quality=78,method=6)
            file=out/(source.stem+'-'+source.suffix.lstrip('.')+'-'+str(width)+'.webp');data=buf.getvalue();file.write_bytes(data)
            records.append({'source':source.relative_to(ROOT).as_posix(),'path':file.relative_to(ROOT).as_posix(),
                            'width':width,'height':height,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    (ROOT/'design-lab/assets/legacy-manifest.json').write_text(json.dumps({'version':'2.0.0-alpha.5','method':'delivery resize and encoding; original imagery retained','images':records},indent=2)+'\n')
    print(json.dumps({'sourceImages':len(referenced),'deliveryImages':len(records),'bytes':sum(r['bytes'] for r in records)}))
if __name__=='__main__':main()
