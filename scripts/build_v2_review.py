#!/usr/bin/env python3
"""Bundle all D2 pages into one offline review file; no network is needed."""
from pathlib import Path
import base64
import json
import mimetypes

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "design-lab"

def main():
    files = ["index.html","home-a.html","home-b.html","event-search.html","event-detail.html","documents.html","components.html"]
    pages = {f: (LAB / f).read_text(encoding="utf-8") for f in files}
    css = (LAB / "tokens.css").read_text() + "\n" + (LAB / "theme.css").read_text()
    events_js = (LAB / "events-data.js").read_text()
    ui_js = (LAB / "ui.js").read_text()
    assets = {}
    for file in list((LAB / "assets/photos").glob("*.webp")) + list((LAB / "assets/fonts").glob("*.woff2")) + [ROOT / "assets/brand-mark.svg"]:
        key = "../assets/brand-mark.svg" if file.name == "brand-mark.svg" else file.relative_to(LAB).as_posix()
        mime = "font/woff2" if file.suffix == ".woff2" else mimetypes.guess_type(file.name)[0]
        assets[key] = f"data:{mime};base64," + base64.b64encode(file.read_bytes()).decode()
    pack = json.dumps(dict(pages=pages,css=css,events=events_js,ui=ui_js,assets=assets),ensure_ascii=False,separators=(",",":")).replace("</", "<\\/")
    bridge = """
document.addEventListener('click',event=>{
 const anchor=event.target.closest('a[href]');if(!anchor)return;
 const href=anchor.getAttribute('href');if(href.startsWith('#'))return;
 const url=new URL(href,'https://design-lab.invalid/');
 if(url.origin!=='https://design-lab.invalid/')return;
 event.preventDefault();
 parent.postMessage({type:'ehime-review-nav',page:url.pathname.split('/').pop(),query:url.search,hash:url.hash},'*');
});
const reportSize=()=>parent.postMessage({type:'ehime-review-height',height:Math.ceil(document.body.getBoundingClientRect().height)},'*');
new ResizeObserver(reportSize).observe(document.body);
addEventListener('load',reportSize);document.fonts.ready.then(reportSize);
"""
    shell = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>愛媛大会 v2 D2 デザイン比較</title>
<style>*{box-sizing:border-box}body{margin:0;background:#e3e8e1;color:#173b35;font-family:system-ui,sans-serif}.review-bar{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid #c8d0c5;padding:12px 20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}.review-bar strong{font-size:14px;margin-right:12px}.review-bar button{min-height:40px;padding:8px 13px;background:#fff;border:1px solid #6c8078;border-radius:7px;font-size:12px;color:#173b35;cursor:pointer}.review-bar button[aria-pressed=true]{color:#fff;background:#173b35}.review-bar button:focus-visible{outline:3px solid #0069ba;outline-offset:3px}.review-size{display:flex;gap:7px;margin-left:auto}.review-caption{padding:12px 20px;font-size:12px;line-height:1.7;color:#52645f}.review-stage{padding:0 16px 24px;overflow:auto}iframe{display:block;width:100%;border:0;margin-inline:auto;background:#f7f4ed;box-shadow:0 2px 16px #173b3514}.review-title{display:none}@media(max-width:700px){.review-bar{padding:10px 12px;gap:7px}.review-bar strong{width:100%;margin:0}.review-bar button{font-size:11px;padding:7px 10px}.review-size{margin-left:0}.review-stage{padding-inline:0}.review-caption{padding:10px 12px}}</style></head><body>
<header class="review-bar"><strong>愛媛大会 v2.0 / D2</strong><button data-page="index.html" aria-pressed="true">比較</button><button data-page="home-a.html" aria-pressed="false">A案</button><button data-page="home-b.html" aria-pressed="false">B案</button><button data-page="event-search.html" aria-pressed="false">検索</button><button data-page="event-detail.html" aria-pressed="false">詳細</button><button data-page="documents.html" aria-pressed="false">資料</button><button data-page="components.html" aria-pressed="false">共通部品</button><div class="review-size" aria-label="表示幅"><button data-width="fluid" aria-pressed="true">画面幅</button><button data-width="390" aria-pressed="false">スマホ390px</button><button data-width="320" aria-pressed="false">スマホ320px</button></div></header>
<p class="review-caption">A案は写真と余白を生かす文化誌、B案は文字と色で伝えるポスターの方向です。ページと表示幅を切り替えて、操作も試せます。</p>
<main class="review-stage"><iframe id="preview" title="愛媛大会 デザイン試作" style="height:1200px"></iframe></main>
<noscript><p>この比較ファイルはJavaScriptを利用します。通常の各HTMLページでは、本文とリンクをJavaScriptなしでもご覧いただけます。</p></noscript>
<script id="review-pack" type="application/json">__PACK__</script><script>
const pack=JSON.parse(document.getElementById('review-pack').textContent);
const preview=document.getElementById('preview');
let current='index.html';let currentQuery='';let lastDirection='editorial';
const bridge=__BRIDGE__;
const replaceAssets=text=>{for(const [path,url] of Object.entries(pack.assets))text=text.split(path).join(url);return text};
const inlineCss=replaceAssets(pack.css);
function loadPage(page,query='',hash=''){
 if(!pack.pages[page])return;
 current=page;currentQuery=query;
 if(page==='home-a.html')lastDirection='editorial';
 else if(page==='home-b.html'||new URLSearchParams(query).get('direction')==='poster')lastDirection='poster';
 const params=new URLSearchParams(query);
 if(lastDirection==='poster'&&!['index.html','home-a.html','home-b.html'].includes(page))params.set('direction','poster');
 if(params.toString())currentQuery='?'+params.toString();
 let html=replaceAssets(pack.pages[page]);
 html=html.replace('<head>','<head><script>window.__INITIAL_QUERY__='+JSON.stringify(currentQuery)+';<\\/script>');
 html=html.replace('<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="theme.css">','<style>'+inlineCss+'</style>');
 html=html.replace('<script src="events-data.js" defer><\\/script>','<script>'+pack.events+'<\\/script>');
 html=html.replace('<script src="ui.js" defer><\\/script>','');
 const jump=hash?'addEventListener("load",()=>{document.getElementById('+JSON.stringify(hash.slice(1))+')?.scrollIntoView()});':'';
 html=html.replace('</body>','<script>'+pack.ui+bridge+jump+'<\\/script></body>');
 preview.srcdoc=html;
 document.querySelectorAll('[data-page]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.page===page)));
 window.scrollTo({top:0,behavior:'auto'});
}
document.querySelectorAll('[data-page]').forEach(button=>button.addEventListener('click',()=>loadPage(button.dataset.page)));
document.querySelectorAll('[data-width]').forEach(button=>button.addEventListener('click',()=>{
 preview.style.width=button.dataset.width==='fluid'?'100%':button.dataset.width+'px';
 document.querySelectorAll('[data-width]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
}));
addEventListener('message',event=>{
 if(event.source!==preview.contentWindow)return;
 if(event.data.type==='ehime-review-nav')loadPage(event.data.page,event.data.query,event.data.hash);
 if(event.data.type==='ehime-review-height'&&Number.isFinite(event.data.height))preview.style.height=Math.max(400,event.data.height)+'px';
});
loadPage('index.html');
</script></body></html>"""
    shell = shell.replace("__PACK__", pack).replace("__BRIDGE__", json.dumps(bridge,ensure_ascii=False).replace("</","<\\/"))
    (LAB / "review.html").write_text(shell,encoding="utf-8")
    print(f"Built offline review.html: {(LAB/'review.html').stat().st_size} bytes.")

if __name__ == "__main__":
    main()
