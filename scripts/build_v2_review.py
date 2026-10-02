#!/usr/bin/env python3
"""Build an offline review of the single v2 experience with its complete routes."""
from pathlib import Path
import base64
import json
ROOT=Path(__file__).resolve().parents[1]
LAB=ROOT/'design-lab'

def main():
    manifest=json.loads((LAB/'experience-manifest.json').read_text())
    pages={f:(LAB/f).read_text() for f in manifest['pages']}
    assets={}
    for directory,mime,suffix in [('assets/art','image/webp','*.webp'),('assets/legacy','image/webp','*.webp'),('assets/culture','image/webp','*.webp'),('assets/fonts','font/woff2','*.woff2')]:
        for f in (LAB/directory).glob(suffix):
            assets[f.relative_to(LAB).as_posix()]='data:'+mime+';base64,'+base64.b64encode(f.read_bytes()).decode()
    pack={'pages':pages,'css':(LAB/'experience.css').read_text(),'data':(LAB/'experience-data.js').read_text(),'ui':(LAB/'experience.js').read_text(),'painting':(LAB/'painting.js').read_text(),'culture':(LAB/'culture-experience.js').read_text(),'legacy':(LAB/'legacy-ui.js').read_text(),'search':(LAB/'site-search-data.js').read_text(),'assets':assets}
    bridge=r'''
document.addEventListener('click',event=>{
 const a=event.target.closest('a[href]');if(!a)return;const href=a.getAttribute('href');
 if(!href||href.startsWith('#')||href.startsWith('blob:')||a.hasAttribute('download'))return;
 const url=new URL(href,'https://offline.invalid/');const page=url.pathname.split('/').pop();
 if(window.__POC_PAGES__.includes(page)){event.preventDefault();window.parent.postMessage({type:'ehime-v2-nav',page,query:url.search,hash:url.hash,from:window.__POC_QUERY__},'*')}
 else if(/^https?:/.test(href)){a.target='_blank';a.rel='noopener'}
});
const resize=()=>window.parent.postMessage({type:'ehime-v2-height',height:document.documentElement.scrollHeight},'*');
if('ResizeObserver'in window)new ResizeObserver(resize).observe(document.body);addEventListener('load',resize);resize();
'''
    shell=r'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>愛媛を、ひらく。｜v2確認ファイル</title><style>
*{box-sizing:border-box}body{margin:0;background:#e8e8e4;color:#151d36;font-family:system-ui,sans-serif}.review-bar{display:flex;align-items:center;gap:9px;padding:12px 20px;border-bottom:1px solid #b4b8bd;background:#f5f2ea;flex-wrap:wrap}.review-bar strong{font-size:18px;margin-right:15px}.review-bar button{min-height:40px;padding:9px 12px;font:inherit;font-size:16px;background:transparent;border:1px solid #6b7283;color:#151d36;cursor:pointer}.review-bar button[aria-pressed=true]{background:#183c9e;color:#fffdf8;border-color:#183c9e}.review-bar button:focus-visible{outline:3px solid #183c9e;outline-offset:3px}.review-bar button:disabled{opacity:.4;cursor:default}.review-width{display:flex;gap:7px;margin-left:auto}.review-caption{font-size:16px;line-height:1.8;padding:12px 20px;max-width:1200px;margin:0}.review-stage{overflow:auto;padding:0 16px 24px}iframe{display:block;border:0;margin:auto;width:100%;height:1200px;background:#f5f2ea}.review-state{font-size:14px;color:#596073}@media(max-width:700px){.review-bar{padding:10px 12px;gap:7px}.review-bar strong{width:100%;margin:0}.review-width{margin-left:0}.review-stage{padding-inline:0}.review-caption{padding:10px 12px}.review-bar button{padding:8px 10px}}
</style></head><body><header class="review-bar"><strong>愛媛を、ひらく。 / v2.0 alpha.6</strong><button data-back disabled>戻る</button><button data-page="index.html" aria-pressed="true">トップ</button><button data-page="culture-atlas.html" aria-pressed="false">文化</button><button data-page="event-search.html" aria-pressed="false">催し</button><button data-page="notebook.html" aria-pressed="false">文化帖</button><button data-page="documents.html" aria-pressed="false">資料</button><div class="review-width" aria-label="表示幅"><button data-width="fluid" aria-pressed="true">画面幅</button><button data-width="390" aria-pressed="false">390px</button><button data-width="320" aria-pressed="false">320px</button></div></header><p class="review-caption">文化祭全体の主画像と、各催しの画像を生成しました。全129ページの本文・画像・書体を同梱。文化の記録写真と、催しのAI生成画像を区別しています。v1の全イベント・掲載情報を保持しています。 <span class="review-state" data-review-state>トップ</span></p><main class="review-stage"><iframe id="preview" title="愛媛大会 v2デザイン確認"></iframe></main><noscript><p>この確認ファイルはJavaScriptを利用します。通常配信の各ページでは、本文とリンクをJavaScriptなしでも読めます。</p></noscript><script id="pack" type="application/json">__PACK__</script><script>
const pack=JSON.parse(document.getElementById('pack').textContent);const preview=document.getElementById('preview');
let current='index.html',query='',hash='';const stack=[];let notebook=[],painting=[],fieldNotes={},kanaPoem=null;
try{notebook=JSON.parse(localStorage.getItem('ehime-v2-offline-notes')||'[]')}catch(_){}
try{painting=JSON.parse(localStorage.getItem('ehime-v2-offline-painting')||'[]')}catch(_){}
try{fieldNotes=JSON.parse(localStorage.getItem('ehime-v2-offline-field-notes')||'{}')}catch(_){}
try{kanaPoem=JSON.parse(localStorage.getItem('ehime-v2-offline-kana-poem')||'null')}catch(_){}
const bridge=__BRIDGE__;
const replaceAssets=text=>{for(const[name,url]of Object.entries(pack.assets))text=text.split(name).join(url);return text};const css=replaceAssets(pack.css);
function loadPage(page,qs='',anchor='',remember=true){
 if(!pack.pages[page])return;if(remember&&page!==current)stack.push({page:current,query,hash});
 current=page;const params=new URLSearchParams(qs);params.set('saved',notebook.join(','));query=params.toString()?'?'+params.toString():'';hash=anchor;
 let html=replaceAssets(pack.pages[page]);
 const globals='window.__POC_OFFLINE__=true;window.__POC_QUERY__='+JSON.stringify(query)+';window.__POC_NOTEBOOK__='+JSON.stringify(notebook)+';window.__POC_PAINTING__='+JSON.stringify(painting)+';window.__POC_FIELD_NOTES__='+JSON.stringify(fieldNotes)+';window.__POC_HAIKU__='+JSON.stringify(kanaPoem)+';window.__POC_PAGES__='+JSON.stringify(Object.keys(pack.pages))+';window.__POC_ASSET_URLS__='+JSON.stringify(Object.fromEntries(Object.entries(pack.assets).filter(([key])=>(key.includes('/event-')||key.includes('assets/culture/'))&&key.endsWith('-480.webp'))))+';';
 html=html.replace('<head>','<head><script>'+globals.replace(/</g,'\\u003c')+'<\/script>');html=html.replace(/<link rel="stylesheet" href="experience\.css(?:\?v=[a-f0-9]+)?">/g,'<style>'+css+'</style>');
 html=html.replace('<script src="experience-data.js" defer><\/script>','<script>'+pack.data+'<\/script>');html=html.replace('<script src="experience.js" defer><\/script>','');html=html.replace('<script src="legacy-ui.js" defer><\/script>','');html=html.replace('<script src="site-search-data.js" defer><\/script>','');
 const hasPainting=html.includes('<script src="painting.js" defer><\/script>');html=html.replace('<script src="painting.js" defer><\/script>','');
 const hasCulture=html.includes('<script src="culture-experience.js" defer><\/script>');html=html.replace('<script src="culture-experience.js" defer><\/script>','');
 const jump=anchor?'addEventListener("load",()=>document.getElementById('+JSON.stringify(anchor.slice(1))+')?.scrollIntoView());':'';
 html=html.replace('</body>','<script>'+pack.ui+pack.search+pack.legacy+(hasPainting?pack.painting:'')+(hasCulture?pack.culture:'')+bridge+jump+'<\/script></body>');preview.srcdoc=html;
 document.querySelectorAll('[data-page]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.page===page)));document.querySelector('[data-back]').disabled=!stack.length;
 document.querySelector('[data-review-state]').textContent=page;if(window.parent!==window)window.parent.postMessage({type:'ehime-review-page',page},'*');window.scrollTo({top:0,behavior:'auto'});
}
document.querySelectorAll('[data-page]').forEach(b=>b.addEventListener('click',()=>loadPage(b.dataset.page)));
document.querySelector('[data-back]').addEventListener('click',()=>{const p=stack.pop();if(p)loadPage(p.page,p.query,p.hash,false)});
document.querySelectorAll('[data-width]').forEach(b=>b.addEventListener('click',()=>{preview.style.width=b.dataset.width==='fluid'?'100%':b.dataset.width+'px';document.querySelectorAll('[data-width]').forEach(item=>item.setAttribute('aria-pressed',String(item===b)))}));
addEventListener('message',event=>{
 if(event.source!==preview.contentWindow||!event.data||typeof event.data!=='object')return;
 if(event.data.type==='ehime-field-notes'){fieldNotes=event.data.notes||{};try{localStorage.setItem('ehime-v2-offline-field-notes',JSON.stringify(fieldNotes))}catch(_){}return}
 if(event.data.type==='ehime-kana-poem'){kanaPoem=event.data.words;try{localStorage.setItem('ehime-v2-offline-kana-poem',JSON.stringify(kanaPoem))}catch(_){}return}
 if(event.data.type==='ehime-v2-nav'){query=event.data.from||query;loadPage(event.data.page,event.data.query,event.data.hash)}
 if(event.data.type==='ehime-v2-height'&&Number.isFinite(event.data.height))preview.style.height=Math.max(400,Math.min(30000,event.data.height))+'px';
 if(event.data.type==='ehime-v2-notebook'&&Array.isArray(event.data.ids)){notebook=event.data.ids;try{localStorage.setItem('ehime-v2-offline-notes',JSON.stringify(notebook))}catch(_){}}
 if(event.data.type==='ehime-v2-painting'&&Array.isArray(event.data.lines)){painting=event.data.lines;try{localStorage.setItem('ehime-v2-offline-painting',JSON.stringify(painting))}catch(_){}}
});const initial=new URLSearchParams(location.hash.slice(1));if(initial.get('embedded')==='1'){document.querySelector('.review-bar').hidden=true;document.querySelector('.review-caption').hidden=true;document.querySelector('.review-stage').style.padding='0';}loadPage(initial.get('page')||'index.html','','',false);addEventListener('hashchange',()=>{const params=new URLSearchParams(location.hash.slice(1));loadPage(params.get('page')||'index.html','','',false)});
</script></body></html>'''
    text=shell.replace('__PACK__',json.dumps(pack,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('__BRIDGE__',json.dumps(bridge,ensure_ascii=False).replace('</','<\\/'))
    (LAB/'review.html').write_text(text)
    print(json.dumps({'pages':len(pages),'bytes':len(text.encode()),'bundledAssets':len(assets)}))
if __name__=='__main__':main()
