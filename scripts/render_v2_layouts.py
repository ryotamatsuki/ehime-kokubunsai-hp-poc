#!/usr/bin/env python3
"""Render static layout references with WeasyPrint, not browser screenshots."""
from pathlib import Path
import argparse
import json
import logging
import re
import tempfile
import fitz
import tinycss2
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "design-lab"

def screen_css(css,width):
    result=[]
    for rule in tinycss2.parse_stylesheet(css,skip_comments=True,skip_whitespace=True):
        if rule.type=="at-rule" and rule.lower_at_keyword=="media":
            condition=tinycss2.serialize(rule.prelude).strip()
            allowed=True
            if "print" in condition or "forced-colors" in condition or "hover" in condition: allowed=False
            maximum=re.search(r"max-width:\s*(\d+)px",condition)
            minimum=re.search(r"min-width:\s*(\d+)px",condition)
            if maximum and width>int(maximum.group(1)): allowed=False
            if minimum and width<int(minimum.group(1)): allowed=False
            if allowed and rule.content: result.append(screen_css(tinycss2.serialize(rule.content),width))
        else:
            result.append(tinycss2.serialize([rule]))
    return "\n".join(result)

def render(file,width,height,output):
    source=(LAB/file).read_text()
    css=screen_css((LAB/"tokens.css").read_text()+"\n"+(LAB/"theme.css").read_text()+"\n"+(LAB/"concepts.css").read_text(),width)
    # WeasyPrint is paged, so viewport units are resolved to this reference width.
    css=re.sub(r"(\d*\.?\d+)vw",lambda m:f"{float(m.group(1))*width/100}px",css)
    css+="\n@page{size:"+str(width)+"px 18000px;margin:0} body{margin:0}"
    # Its CSS implementation does not evaluate all clamp/min functions.
    css=css.replace("width:min(100% - var(--gutter)*2,var(--content-max))",
                    f"width:{min(width-2*max(20,min(width*.04,64)),1280)}px")
    css=css.replace("var(--gutter)",f"{max(20,min(width*.04,64))}px")
    source=source.replace('<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="theme.css"><link rel="stylesheet" href="concepts.css">',"<style>"+css+"</style>")
    source=source.replace('loading="lazy"','loading="eager"')
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
        HTML(string=source,base_url=LAB.as_uri()+"/",media_type="screen").write_pdf(temp.name)
        pdf=fitz.open(temp.name)
        pdf[0].get_pixmap(matrix=fitz.Matrix(1,1),clip=fitz.Rect(0,0,width*.75,height*.75)).save(output)
    return {"file":file,"width":width,"height":height,"output":str(output.relative_to(ROOT)),"renderer":"WeasyPrint 70 static reference; not Chromium"}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--all",action="store_true")
    args=parser.parse_args()
    logging.getLogger("weasyprint").setLevel(logging.ERROR)
    out=LAB/"qa"
    out.mkdir(exist_ok=True)
    renders=[]
    files=["home-a.html","home-b.html"]
    if args.all: files+=["event-search.html","event-detail.html","documents.html"]
    for file in files:
        for name,width,height in [("desktop",1440,1000),("mobile",390,1200)]:
            output=out/f"layout-{file.removesuffix('.html')}-{name}.png"
            renders.append(render(file,width,height,output))
    (out/"layout-references.json").write_text(json.dumps(renders,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(renders,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
