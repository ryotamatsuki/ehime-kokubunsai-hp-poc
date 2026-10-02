"""Verify credited record photographs and create responsive delivery copies."""
from pathlib import Path
from io import BytesIO
import hashlib,json
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[1];LAB=ROOT/'design-lab'

def main():
    source=LAB/'assets/culture-sources.json';data=json.loads(source.read_text())
    target=LAB/'assets/culture';target.mkdir(exist_ok=True)
    deliveries=[]
    for row in data['images']:
        original=ROOT/row['original']
        if hashlib.sha256(original.read_bytes()).hexdigest()!=row['sha256']:
            raise ValueError('Source photograph differs: '+row['id'])
        im=ImageOps.exif_transpose(Image.open(original)).convert('RGB')
        row['width'],row['height']=im.size;row['deliveries']=[]
        for key in [480,960,1440]:
            width=min(key,im.width);height=round(im.height*width/im.width)
            buffer=BytesIO();im.resize((width,height),Image.Resampling.LANCZOS).save(buffer,'WEBP',quality=78,method=6)
            raw=buffer.getvalue();file=target/(row['id']+'-'+str(key)+'.webp');file.write_bytes(raw)
            item=dict(path=file.relative_to(ROOT).as_posix(),width=width,height=height,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),source=row['original'],license=row['license'],licenseUrl=row['licenseUrl'])
            row['deliveries'].append(item);deliveries.append(item)
    source.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    (LAB/'assets/culture-manifest.json').write_text(json.dumps({'version':json.loads((LAB/'content.json').read_text())['version'],'images':deliveries},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'recordPhotographs':len(data['images']),'responsiveImages':len(deliveries),'deliveryBytes':sum(r['bytes'] for r in deliveries)}))

if __name__=='__main__':main()
