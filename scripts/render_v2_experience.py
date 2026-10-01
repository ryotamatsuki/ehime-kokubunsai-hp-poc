#!/usr/bin/env python3
"""Static review with WeasyPrint and enhanced DOM; not browser screenshots."""
from pathlib import Path
import argparse
import json
import logging
import re
import subprocess
import tempfile
from io import BytesIO
import fitz
import tinycss2
from PIL import Image
from weasyprint import HTML

ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/'design-lab'

def screen_css(text,width):
    output=[]
    for rule in tinycss2.parse_stylesheet(text,skip_comments=True,skip_whitespace=True):
        if rule.type=='at-rule' and rule.lower_at_keyword=='media':
            condition=tinycss2.serialize(rule.prelude)
            allowed=not any(x in condition for x in ['print','forced-colors','prefers-reduced-motion'])
            maximum=re.search(r'max-width:\s*(\d+)px',condition);minimum=re.search(r'min-width:\s*(\d+)px',condition)
            if maximum and width>int(maximum[1]):allowed=False
            if minimum and width<int(minimum[1]):allowed=False
            if allowed and rule.content:output.append(screen_css(tinycss2.serialize(rule.content),width))
        else:output.append(tinycss2.serialize([rule]))
    return '\n'.join(output)

def render(file,width,height,folder,query='',label=''):
    with tempfile.NamedTemporaryFile(suffix='.html') as domfile:
        subprocess.run(['node',str(ROOT/'scripts/snapshot_v2_dom.cjs'),file,str(width),domfile.name,query],check=True,capture_output=True)
        source=Path(domfile.name).read_text()
    css=screen_css((LAB/'experience.css').read_text(),width)
    gutter=16 if width<=360 else 20 if width<=700 else 32 if width<=1250 else 48
    css=css.replace('width:calc(100% - var(--gutter)*2)',f'width:{min(width-2*gutter,1344)}px')
    # WeasyPrint ignores aspect-ratio: substitute the native layout's image frame.
    content_width=min(width-2*gutter,1344)
    if width<=700:
        image_width=content_width
        image_height=image_width/1.19
    else:
        gap=50 if width>=1600 else 32 if width>1050 else 24
        image_width=(content_width-gap)*6/13
        image_height=image_width/.94
    css+=f'\n.opening-image>img{{height:{image_height}px;object-fit:cover}}'
    css+=f'\n.festival-panorama>img{{height:{content_width/(1.25 if width<=700 else 2)}px;object-fit:cover}}'
    css+='\n@page{size:'+str(width)+'px 18000px;margin:0}body{margin:0}'
    source=source.replace('<link rel="stylesheet" href="experience.css">','<style>'+css+'</style>')
    stem=file.removesuffix('.html')+'-'+str(width)+(('-'+label) if label else '')
    output=folder/(stem+'.png')
    document=HTML(string=source,base_url=LAB.as_uri()+'/',media_type='screen').render()
    geometry=[];control_geometry=[]
    for box in document.pages[0]._page_box.descendants():
        if type(box).__name__=='TextBox' and getattr(box,'text','').strip():
            if box.position_x < -1 or box.position_x+box.width>width+1:
                geometry.append({'text':box.text,'x':round(box.position_x,2),'width':round(box.width,2)})
        element=getattr(box,'element',None)
        if element is not None and element.tag in ['a','button','input','select'] and type(box).__name__ in ['BlockBox','InlineFlexBox','FlexBox','InlineBlockBox']:
            if box.position_x < -1 or box.position_x+box.border_width()>width+1:
                control_geometry.append({'tag':element.tag,'class':element.get('class',''),'x':round(box.position_x,2),'width':round(box.border_width(),2)})
    pdf=fitz.open(stream=document.write_pdf(),filetype='pdf')
    data=pdf[0].get_pixmap(matrix=fitz.Matrix(4/3,4/3),clip=fitz.Rect(0,0,width*.75,height*.75)).tobytes('png')
    with Image.open(BytesIO(data)) as frame:
        frame.load()
        if frame.size!=(width,height):raise ValueError('Unexpected reference dimensions')
    temporary=output.with_suffix('.png.pending')
    temporary.write_bytes(data);temporary.replace(output)
    return {'file':file,'width':width,'height':height,'query':query,'output':output.relative_to(ROOT).as_posix(),'textOutsidePage':geometry,'controlsOutsidePage':control_geometry,'renderer':'WeasyPrint 70 with jsdom-enhanced DOM, not a browser'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cycle',default='1');parser.add_argument('--all',action='store_true');parser.add_argument('--extended',action='store_true');args=parser.parse_args()
    logging.getLogger('weasyprint').setLevel(logging.ERROR)
    folder=LAB/'qa'/('cycle-'+args.cycle);folder.mkdir(parents=True,exist_ok=True)
    cases=[('index.html',1440,1100,'',''),('index.html',390,1700,'',''),('index.html',320,1700,'',''),('index.html',1440,6400,'','full')]
    if args.all:
        for file in ['culture-craft.html','culture-literature.html','event-search.html','event-craft.html','documents.html','notebook.html','participation.html','support.html']:
            for width,height in [(1440,2100),(390,2700),(320,2700)]:
                cases.append((file,width,height,'?saved=craft,art' if file=='notebook.html' else '',''))
    if args.extended:
        cases += [('index.html',width,1900,'','') for width in [768,1024,1250,1600]]
        cases += [('culture-craft.html',1440,3400,'','full'),('culture-craft.html',320,4300,'','full'),('documents.html',1024,2500,'',''),('notebook.html',1024,2500,'?saved=craft,art','')]
        for file in ['info-sponsors-partner-recruitment.html','info-tourism-courses.html','info-contact-form.html','info-common-search.html','site-map.html']:
            cases += [(file,1440,2700,'',''),(file,390,3300,'',''),(file,320,3300,'','')]
    results=[render(file,width,height,folder,query,label) for file,width,height,query,label in cases]
    (folder/'layout-references.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'cycle':args.cycle,'references':len(results),'textOutsidePage':sum(len(r['textOutsidePage']) for r in results),'controlsOutsidePage':sum(len(r['controlsOutsidePage']) for r in results),'folder':str(folder)}))
if __name__=='__main__':main()
