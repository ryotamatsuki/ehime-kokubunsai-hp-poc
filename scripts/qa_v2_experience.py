#!/usr/bin/env python3
"""Static structure, asset integrity, contrast, and budgets; no conformance claim."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib
import json
import re
import subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/'design-lab'

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__();self.tags=[];self.ids=[];self.labels=[];self.inputs=[];self.refs=[];self.headings=[];self.scripts=[];self.script=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append((tag,a))
        if 'id' in a:self.ids.append(a['id'])
        if tag=='label' and 'for' in a:self.labels.append(a['for'])
        if tag in ['input','select','textarea']:self.inputs.append(a.get('id'))
        for key in ['aria-controls','aria-describedby']:
            if key in a:self.refs.extend(a[key].split())
        if re.fullmatch('h[1-6]',tag):self.headings.append(int(tag[1]))
        if tag=='script':self.script={'attrs':a,'code':''}
    def handle_data(self,text):
        if self.script is not None:self.script['code']+=text
    def handle_endtag(self,tag):
        if tag=='script' and self.script is not None:self.scripts.append(self.script);self.script=None

def luminance(color):
    rgb=[int(color[i:i+2],16)/255 for i in [1,3,5]]
    linear=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return .2126*linear[0]+.7152*linear[1]+.0722*linear[2]

def contrast(a,b):
    hi,lo=sorted([luminance(a),luminance(b)],reverse=True)
    return (hi+.05)/(lo+.05)

def main():
    manifest=json.loads((LAB/'experience-manifest.json').read_text())
    tokens=json.loads((LAB/'tokens.json').read_text())
    files=[LAB/f for f in manifest['pages']]+[ROOT/p for f,p in manifest['canonicalRoutes'].items() if f!='components.html']
    pages=[];issues=[];cache={}
    def inspect(file):
        if file not in cache:
            inspector=Inspector();inspector.feed(file.read_text());cache[file]=inspector
        return cache[file]
    for file in files:
        ins=inspect(file);problems=[]
        if len(ins.ids)!=len(set(ins.ids)):problems.append('duplicate IDs')
        if ins.headings.count(1)!=1:problems.append('h1 count')
        if sum(tag=='main' for tag,_ in ins.tags)!=1:problems.append('main landmark')
        if any(id not in ins.labels for id in ins.inputs):problems.append('unlabelled control')
        if any(ref not in ins.ids for ref in ins.refs):problems.append('broken ARIA reference')
        for tag,a in ins.tags:
            if tag=='img' and any(key not in a for key in ['alt','width','height']):problems.append('image accessibility or sizing')
            reference=a.get('href') if tag in ['a','link'] else a.get('src') if tag in ['img','script'] else None
            if not reference:continue
            url=urlsplit(reference)
            if url.scheme:continue
            target=(file.parent/unquote(url.path)).resolve() if url.path else file
            if not target.exists():problems.append('missing file '+reference)
            elif url.fragment and target.suffix=='.html' and unquote(url.fragment) not in inspect(target).ids:problems.append('missing anchor '+reference)
        pages.append({'file':str(file.relative_to(ROOT)),'status':'FAIL' if problems else 'PASS','issues':problems})
        issues.extend(str(file.relative_to(ROOT))+': '+p for p in problems)
    palette=tokens['cssVariables']
    pairs=[('ink','paper',4.5),('muted','paper',4.5),('blue','paper',4.5),('white','blue',4.5),('paper','ink',4.5),('ink','green',4.5),('ink','peach',4.5),('blue','green',4.5),('blue','blue-light',4.5),('ink','blue-light',4.5),('muted','source',4.5),('strong-line','white',3),('strong-line','paper',3),('blue','paper',3),('paper','red',4.5)]
    colors=[]
    for fg,bg,minimum in pairs:
        ratio=contrast(palette[fg],palette[bg]);status='PASS' if ratio>=minimum else 'FAIL'
        colors.append({'foreground':fg,'background':bg,'ratio':round(ratio,3),'minimum':minimum,'status':status})
        if status=='FAIL':issues.append('contrast '+fg+'/'+bg)
    assets=[]
    original=json.loads((LAB/'assets/manifest.json').read_text())
    art=json.loads((LAB/'assets/art-manifest.json').read_text())
    for row in original['fonts']+art['images']:
        actual=hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()
        good=actual==row['sha256'];assets.append({'path':row['path'],'status':'PASS' if good else 'FAIL'})
        if not good:issues.append('asset hash '+row['path'])
    css=(LAB/'experience.css').read_text()
    actual_root=dict(re.findall(r'--([\w-]+):([^;]+);',re.search(r':root\{([^}]+)\}',css)[1]))
    if actual_root!=tokens['cssVariables']:issues.append('CSS differs from token source')
    version=dict(line.split('=',1) for line in (ROOT/'VERSION').read_text().splitlines() if '=' in line)
    if not (version['version']==tokens['version']==manifest['version']):issues.append('version metadata differs')
    css_flags={name:query in css for name,query in [('reducedMotion','prefers-reduced-motion'),('forcedColors','forced-colors'),('focusVisible',':focus-visible'),('print','@media print')]}
    if not all(css_flags.values()):issues.append('missing CSS access states')
    for file in ['experience.js','experience-data.js','painting.js']:
        subprocess.run(['node','--check',str(LAB/file)],check=True,capture_output=True)
    review=Inspector();review.feed((LAB/'review.html').read_text());pack=next(s for s in review.scripts if s['attrs'].get('id')=='pack')
    packed=json.loads(pack['code'])
    if set(packed['pages'])!=set(manifest['pages']):issues.append('offline pack page set')
    for file,source in packed['pages'].items():
        if source!=(LAB/file).read_text():issues.append('stale offline page '+file)
    shared=sum((LAB/name).stat().st_size for name in ['experience.css','experience-data.js','experience.js'])+sum(row['bytes'] for row in original['fonts'])
    budgets=[]
    for name,image_name in [('index.html','porcelain-hero'),('culture-craft.html','craft-hands'),('event-craft.html','craft-hands'),('event-search.html',None),('documents.html',None),('notebook.html',None)]:
        for width in [390,1440]:
            amount=shared+(LAB/name).stat().st_size
            if name=='culture-craft.html':amount+=(LAB/'painting.js').stat().st_size
            if image_name:
                image_width=480 if width==390 else 960
                amount+=(LAB/f'assets/art/{image_name}-{image_width}.webp').stat().st_size
            budgets.append({'page':name,'cssViewport':width,'dpr':1,'estimatedFirstViewBytes':amount,'limit':500000,'status':'PASS' if amount<=500000 else 'FAIL'})
            if amount>500000:issues.append('budget '+name)
    # Original v1 child pages still use these root fragment names.
    compatibility=[id for id in ['about','events','participation','support','news'] if id in inspect(ROOT/'index.html').ids]
    if len(compatibility)!=5:issues.append('missing legacy top fragment')
    layout_file=LAB/'qa/layout-references.json'
    frames=[]
    if layout_file.exists():
        for row in json.loads(layout_file.read_text()):
            path=ROOT/row['output']
            try:
                with Image.open(path) as frame:
                    frame.load()
                    good=frame.size==(row['width'],row['height'])
            except Exception:good=False
            frames.append({'path':row['output'],'status':'PASS' if good else 'FAIL'})
            if not good:issues.append('reference integrity '+row['output'])
    output={'version':'2.0.0-alpha.4','status':'FAIL' if issues else 'PASS','method':'static HTML and code checks; not WCAG conformance/browser/CWV confirmation','pages':pages,'contrast':colors,'assetHashes':assets,'cssStates':css_flags,'estimatedBudgets':budgets,'budgetLimits':'DPR1 estimate; excludes later/lazy requests, cache, response headers, real loading time','offlinePack':{'pages':len(packed['pages']),'assets':len(packed['assets']),'bytes':(LAB/'review.html').stat().st_size},'legacyTopFragments':compatibility,'issues':issues}
    output['staticReferenceIntegrity']=frames
    (LAB/'qa/static-checks.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':output['status'],'pages':len(pages),'contrastPairs':len(colors),'minimumTextContrast':min(c['ratio'] for c in colors if c['minimum']==4.5),'assets':len(assets),'largestEstimatedFirstView':max(b['estimatedFirstViewBytes'] for b in budgets),'issues':issues},ensure_ascii=False))
    if issues:raise SystemExit(1)
if __name__=='__main__':main()
