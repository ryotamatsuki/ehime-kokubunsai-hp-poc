#!/usr/bin/env python3
"""Static checks and measured budgets, deliberately not a browser audit."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "design-lab"
REPORT = LAB / "qa"

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.tags = []
        self.references = []
        self.labels = []
        self.controls = []
        self.headings = []
        self.images = []
        self.scripts = []
        self.script = None
    def handle_starttag(self,tag,attrs):
        a = dict(attrs)
        self.tags.append((tag,a))
        if "id" in a: self.ids.append(a["id"])
        for key in ["aria-controls","aria-describedby"]:
            if key in a: self.references.extend(a[key].split())
        if tag == "label" and "for" in a: self.labels.append(a["for"])
        if tag in ["input","select","textarea"]: self.controls.append(a)
        if tag in ["h1","h2","h3","h4","h5","h6"]: self.headings.append(int(tag[1]))
        if tag == "img": self.images.append(a)
        if tag == "script":
            self.script = {"attrs":a,"code":""}
    def handle_data(self,data):
        if self.script is not None: self.script["code"] += data
    def handle_endtag(self,tag):
        if tag == "script" and self.script is not None:
            self.scripts.append(self.script)
            self.script = None

def luminance(color):
    rgb = [int(color[i:i+2],16)/255 for i in [1,3,5]]
    linear = [x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
    return .2126*linear[0] + .7152*linear[1] + .0722*linear[2]

def contrast(a,b):
    x,y = sorted([luminance(a),luminance(b)],reverse=True)
    return (x+.05)/(y+.05)

def main():
    REPORT.mkdir(exist_ok=True)
    issues = []
    pages = []
    for page in sorted(LAB.glob("*.html")):
        if page.name == "review.html": continue
        ins = Inspector()
        ins.feed(page.read_text())
        local = []
        if len(ins.ids) != len(set(ins.ids)): local.append("duplicate IDs")
        if ins.headings.count(1) != 1: local.append("h1 count")
        if sum(tag=="main" for tag,_ in ins.tags) != 1: local.append("main landmark")
        if any(tag=="img" and "alt" not in attrs for tag,attrs in ins.tags): local.append("missing alt")
        if any(not img.get("width") or not img.get("height") for img in ins.images): local.append("image dimensions")
        if any(ref not in ins.ids for ref in ins.references): local.append("broken ARIA ID reference")
        if any(control.get("id") not in ins.labels for control in ins.controls): local.append("unlabelled input")
        for tag,attrs in ins.tags:
            ref = attrs.get("href") if tag in ["a","link"] else attrs.get("src") if tag in ["img","script"] else None
            if not ref or ref.startswith("data:"): continue
            parts = urlsplit(ref)
            if parts.scheme: continue
            path = page if not parts.path else (page.parent / unquote(parts.path)).resolve()
            if not path.exists():
                local.append("missing file: "+ref)
            elif parts.fragment and path.suffix == ".html":
                target = Inspector()
                target.feed(path.read_text())
                if unquote(parts.fragment) not in target.ids: local.append("missing anchor: "+ref)
        pages.append({"page":page.relative_to(ROOT).as_posix(),"h1":ins.headings.count(1),"images":len(ins.images),"status":"FAIL" if local else "PASS","issues":local})
        issues.extend(f"{page.name}: {x}" for x in local)

    tokens=json.loads((LAB/"tokens.json").read_text())
    pairs=[("ink","page",4.5),("muted","page",4.5),("muted","wash",4.5),("accent","page",4.5),("white","ink",4.5),("white","accent",4.5),("control-line","surface",3),("focus","page",3)]
    contrasts=[]
    for direction in ["editorial","poster"]:
        colors=dict(tokens["base"],white="#ffffff")
        colors.update(tokens["directions"].get(direction,{}))
        for fg,bg,minimum in pairs:
            ratio=contrast(colors[fg],colors[bg])
            row={"direction":direction,"foreground":fg,"background":bg,"ratio":round(ratio,3),"minimum":minimum,"status":"PASS" if ratio>=minimum else "FAIL"}
            contrasts.append(row)
            if ratio<minimum: issues.append(f"contrast {direction} {fg}/{bg}: {ratio:.3f}")
    concept_pairs=[("sea-text","sea",4.5),("sea-copy","sea",4.5),("sea-muted","sea",4.5),
                   ("sea","lime",4.5),("cobalt","yellow",4.5),("cobalt","paper",4.5),
                   ("cobalt","coral",4.5),("paper","cobalt",4.5),("white","blue",4.5),
                   ("signal-focus","sea",3),("signal-focus","blue",3),("signal-focus","cobalt",3),
                   ("focus","paper",3),("focus","yellow",3),("focus","coral",3)]
    colors=dict(tokens["base"],white="#ffffff")
    for fg,bg,minimum in concept_pairs:
        ratio=contrast(colors[fg],colors[bg])
        contrasts.append({"direction":"concept-reset","foreground":fg,"background":bg,"ratio":round(ratio,3),"minimum":minimum,"status":"PASS" if ratio>=minimum else "FAIL"})
        if ratio<minimum: issues.append(f"concept contrast {fg}/{bg}: {ratio:.3f}")
    manifest=json.loads((LAB/"assets/manifest.json").read_text())
    hashes=[]
    for row in manifest["photos"]+manifest["fonts"]:
        path=ROOT/row["path"]
        good=hashlib.sha256(path.read_bytes()).hexdigest()==row["sha256"]
        hashes.append({"path":row["path"],"status":"PASS" if good else "FAIL"})
        if not good: issues.append("asset hash mismatch: "+row["path"])
    css=(LAB/"theme.css").read_text()+"\n"+(LAB/"concepts.css").read_text()
    css_checks={
        "reduced_motion_override": "@media(prefers-reduced-motion:reduce)" in css and "animation:none!important" in css,
        "visible_focus_style": ":focus-visible" in css,
        "hidden_attribute_respected": "[hidden]{display:none!important}" in css,
        "minimum_control_height": "min-height:44px" in css,
        "mobile_layout_rule": "@media(max-width:759px)" in css,
    }
    for name,good in css_checks.items():
        if not good: issues.append("CSS missing: "+name)
    core_bytes=sum((LAB/f).stat().st_size for f in ["tokens.css","theme.css","concepts.css","ui.js","events-data.js"])
    fonts=sum(f["bytes"] for f in manifest["fonts"])
    budgets=[]
    first_view={"home-a.html":["tobe-ceramics-workshop","event-stage-lanterns","uchiko-ozu-townscape","inclusive-art-gallery"],"home-b.html":["event-stage-lanterns","family-culture-workshop"]}
    for name,first_images in first_view.items():
        images=sum((LAB/f"assets/photos/{image}-480.webp").stat().st_size for image in first_images)
        total=(LAB/name).stat().st_size+core_bytes+fonts+images+(ROOT/"assets/brand-mark.svg").stat().st_size
        row={"page":name,"condition":"320–390 CSS px / DPR 1 / first-view image set at 480w / uncompressed asset estimate; excludes below-fold and subsequently selected images","first_view_images":first_images,"bytes":total,"limit_bytes":500000,"status":"PASS" if total<=500000 else "FAIL"}
        budgets.append(row)
        if total>500000: issues.append("mobile transfer budget: "+name)
    review=Inspector();review.feed((LAB/"review.html").read_text())
    inline_scripts=[x for x in review.scripts if x["attrs"].get("type")!="application/json"]
    review_syntax=[]
    for i,script in enumerate(inline_scripts):
        temp=REPORT/f".review-check-{i}.js"
        temp.write_text(script["code"])
        result=subprocess.run(["node","--check",str(temp)],capture_output=True,text=True)
        temp.unlink()
        review_syntax.append({"script":i,"status":"PASS" if result.returncode==0 else "FAIL"})
        if result.returncode: issues.append("offline review syntax: "+result.stderr)
    if len(review.scripts)!=2: issues.append("offline review script boundary")
    out={
        "scope":"D2 static checks; browser layout, screen reader, real keyboard, CWV and user testing are not certified",
        "pages":pages,"contrasts":contrasts,"css_checks":css_checks,"asset_hashes":hashes,"mobile_asset_budgets":budgets,"offline_review_scripts":review_syntax,
        "status":"PASS" if not issues else "FAIL","issues":issues,
    }
    (REPORT/"static-checks.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"status":out["status"],"pages":len(pages),"contrast_pairs":len(contrasts),"assets":len(hashes),"mobile_asset_budgets":budgets,"issues":issues},ensure_ascii=False,indent=2))
    raise SystemExit(bool(issues))

if __name__=="__main__":
    main()
