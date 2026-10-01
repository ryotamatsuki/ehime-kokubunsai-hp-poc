"""Build a two-version review using the unchanged, hash-verified v1 snapshot."""
from pathlib import Path
import json,html,base64,mimetypes,re
import v2_preserve_content as preserved
ROOT=Path(__file__).resolve().parents[1];LAB=ROOT/'design-lab'

def main():
    manifest=json.loads((LAB/'experience-manifest.json').read_text())
    inventory=preserved.inventory();reverse={path:name for name,path in manifest['canonicalRoutes'].items()}
    pages={path:(ROOT/'comparison/v1'/path).read_text() for path in inventory}
    pages['homepage_structure_document.html']=(ROOT/'comparison/v1/homepage_structure_document.html').read_text()
    mapping={path:reverse[path] for path in inventory}
    options=[]
    for source,row in inventory.items():
        options.append('<option value="'+html.escape(source)+'">'+html.escape(preserved.GROUPS.get(row['group'],'トップ')+' / '+row['title'])+'</option>')
    baseline=ROOT/'comparison/v1'
    used=set()
    for source in inventory:
        for value in re.findall(r'(?:src|href)=[\"\']([^\"\']+)',pages[source]):
            if value.startswith(('https:','#','mailto:','tel:')):continue
            file=(baseline/source).parent/value.split('?')[0]
            if file.is_file() and file.suffix.lower() in ['.jpg','.png','.svg']:
                used.add(file.resolve())
    for value in re.findall(r'url\([\"\']?([^\"\')]+)',(baseline/'style.css').read_text()):
        file=baseline/value
        if file.is_file():used.add(file.resolve())
    assets={file.relative_to(baseline.resolve()).as_posix():'data:'+mimetypes.guess_type(file.name)[0]+';base64,'+base64.b64encode(file.read_bytes()).decode() for file in sorted(used)}
    payload={'v1Pages':pages,'v1Assets':assets,'v1CSS':(baseline/'style.css').read_text(),
             'v1Script':(baseline/'script.js').read_text(),'v1Search':(baseline/'search-index.js').read_text(),
             'v2Routes':mapping,'v2Canonical':manifest['canonicalRoutes'],
             'v1Commit':'94df551e752129e45e7f21c3d38282d87c5690db','version':manifest['version']}
    shell=r'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>v1・v2のデザイン比較｜愛顔えひめの文化祭2028</title><style>
*{box-sizing:border-box}body{margin:0;background:#e8e8e4;color:#151d36;font:18px/1.7 system-ui,sans-serif}button,select{font:inherit;color:inherit}button{min-height:48px;padding:10px 16px;cursor:pointer;border:1px solid #6b7283;background:#fffdf8}button[aria-pressed=true]{background:#183c9e;color:#fffdf8;border-color:#183c9e}button:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #183c9e;outline-offset:4px}.toolbar{background:#f5f2ea;border-bottom:1px solid #b4b8bd;padding:18px 24px}.toolbar h1{font-size:26px;line-height:1.5;margin:0 0 8px}.toolbar p{margin:0;font-size:16px}.controls{display:flex;gap:12px;align-items:end;flex-wrap:wrap;margin-top:18px}label{display:grid;gap:6px;flex:1;min-width:240px;font-size:16px}select{width:100%;min-height:48px;padding:10px;max-width:660px}.mode-controls,.quick-links{display:flex;gap:10px;flex-wrap:wrap}.quick-links{margin-top:12px}.quick-links button{font-size:16px;padding:9px 14px}.stage{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;padding:12px}.pane{min-width:0;overflow:auto;background:#f5f2ea}.pane h2{font-size:20px;line-height:1.5;margin:0;padding:14px 18px;background:#fffdf8;border-bottom:1px solid #b4b8bd}.pane h2 span{display:block;font-size:16px;color:#596073;font-weight:400}.pane iframe{display:block;width:100%;height:calc(100vh - 390px);min-height:680px;border:0;background:#f5f2ea}.stage[data-mode=v1],.stage[data-mode=v2]{grid-template-columns:minmax(0,1fr)}.stage[data-mode=v1] .v2-pane,.stage[data-mode=v2] .v1-pane{display:none}.status{padding:0 24px 18px;font-size:16px}.footer-note{font-size:16px;padding:10px 24px 28px;max-width:1100px;margin:0}.footer-note a{color:#183c9e;text-decoration:underline}.pane iframe.width-fixed{width:390px;margin:auto}@media(max-width:700px){.toolbar{padding:16px}.toolbar h1{font-size:22px}.stage{padding:8px;gap:8px}.pane iframe{min-height:900px}.mode-controls button{font-size:16px;padding:10px 12px}.controls{gap:10px}.stage[data-mode=both]{grid-template-columns:minmax(0,1fr);}.footer-note,.status{padding-inline:16px}}
</style></head><body><header class="toolbar"><h1>同じ情報で、v1とv2を見比べる。</h1><p>v1は固定保存版。v2は文化祭全体を主景にした改訂版です。全案内を選べます。PC全幅で読むときは「v2のみ」を選んでください。</p><div class="controls"><label for="page-choice">比較するページ<select id="page-choice">__OPTIONS__</select></label><div class="mode-controls" aria-label="比較の表示"><button data-mode="both" aria-pressed="true">並べる</button><button data-mode="v1" aria-pressed="false">v1のみ</button><button data-mode="v2" aria-pressed="false">v2のみ</button></div><button data-mobile aria-pressed="false">390pxで見る</button></div><div class="quick-links"><button data-pair="index.html">トップ</button><button data-pair="events/search.html">イベント</button><button data-pair="recruitment/index.html">募集</button><button data-pair="sponsors/partner-recruitment.html">協賛</button><button data-pair="committee/overview.html">資料</button></div></header><main class="stage" data-mode="both"><section class="pane v1-pane"><h2>v1 <span>v1-frozen / 保存版</span></h2><iframe id="v1-preview" title="v1の比較画面"></iframe></section><section class="pane v2-pane"><h2>v2 <span>2.0.0-alpha.5 / 改訂版</span></h2><iframe id="v2-preview" title="v2の比較画面"></iframe></section></main><p class="status" data-comparison-status aria-live="polite"></p><p class="footer-note">ZIPをすべて展開してご覧ください。v1の本文・画像・CSS・JavaScriptは固定版と一致するファイルを同梱しています。v2の通常配信は <a href="../index.html">トップページ</a>、単独の確認用ファイルは <a href="review.html">v2レビュー</a> から開けます。</p><script id="comparison-pack" type="application/json">__PACK__</script><script>
const pack=JSON.parse(document.getElementById('comparison-pack').textContent),left=document.getElementById('v1-preview'),right=document.getElementById('v2-preview'),choice=document.getElementById('page-choice');
let current='index.html',currentV2='index.html',initialising=false;
const base=new URL('../comparison/v1/',location.href);const esc=s=>String(s).replace(/[&"<>]/g,c=>({'&':'&amp;','"':'&quot;','<':'&lt;','>':'&gt;'}[c]));
function showV1(page,query=''){
 if(!pack.v1Pages[page])return;current=page;
 const url=new URL(page,base);let source=pack.v1Pages[page];
 source=source.replace('<head>','<head><base href="'+esc(url.href)+'">');
 const replaceV1Assets=text=>{for(const[name,data]of Object.entries(pack.v1Assets)){text=text.split('../'+name).join(data);text=text.split(name).join(data)}return text};
 source=replaceV1Assets(source).replace(/<link[^>]+href="(?:\.\.\/)?style\.css"[^>]*>/g,'<style>'+replaceV1Assets(pack.v1CSS)+'</style>').replace(/<script[^>]+src="(?:\.\.\/)?(?:script|search-index)\.js"[^>]*><\/script>/g,'');
 const bridge=`document.addEventListener('click',event=>{const a=event.target.closest('a[href]');if(!a)return;const raw=a.getAttribute('href');if(!raw||raw.startsWith('#'))return;const target=new URL(raw,document.baseURI),base=${JSON.stringify(base.href)};if(target.href.startsWith(base)){event.preventDefault();parent.postMessage({type:'ehime-v1-page',page:decodeURIComponent(target.pathname.slice(new URL(base).pathname.length)),query:target.search},'*')}else if(/^https?:/.test(raw)){a.target='_blank';a.rel='noopener'}});document.addEventListener('submit',event=>{const f=event.target;if(f.matches('[data-site-search]')){event.preventDefault();event.stopImmediatePropagation();parent.postMessage({type:'ehime-v1-page',page:'common/search.html',query:'?q='+encodeURIComponent(f.querySelector('input')?.value||'')},'*')}},true);`;
 const queryState='window.__POC_V1_QUERY__='+JSON.stringify(query)+';';
 const searchScript=pack.v1Script.replace('window.location.search','window.__POC_V1_QUERY__ || window.location.search');
 source=source.replace('</body>','<script>'+queryState+pack.v1Search+searchScript+bridge+'<\/script></body>');left.srcdoc=source;
 choice.value=page;document.querySelector('[data-comparison-status]').textContent='比較中：'+(choice.selectedOptions[0]?.textContent||page);
}
function showV2(page){
 currentV2=page;right.src='review.html#embedded=1&page='+encodeURIComponent(page);
}
function pair(page){showV1(page);showV2(pack.v2Routes[page]||'index.html')}
choice.addEventListener('change',()=>pair(choice.value));document.querySelectorAll('[data-pair]').forEach(b=>b.addEventListener('click',()=>pair(b.dataset.pair)));
document.querySelectorAll('[data-mode]').forEach(b=>{if(b.tagName!=='BUTTON')return;b.addEventListener('click',()=>{document.querySelector('.stage').dataset.mode=b.dataset.mode;document.querySelectorAll('button[data-mode]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)))})});
document.querySelector('[data-mobile]').addEventListener('click',event=>{const button=event.currentTarget;const on=button.getAttribute('aria-pressed')!=='true';button.setAttribute('aria-pressed',String(on));button.textContent=on?'画面幅に戻す':'390pxで見る';[left,right].forEach(frame=>frame.classList.toggle('width-fixed',on))});
addEventListener('message',event=>{
 if(event.source===left.contentWindow&&event.data?.type==='ehime-v1-page'){const page=event.data.page;if(pack.v1Pages[page]){showV1(page,event.data.query||'');showV2(pack.v2Routes[page]||'index.html')}}
 if(event.source===right.contentWindow&&event.data?.type==='ehime-review-page'){
  const page=event.data.page;currentV2=page;const canonical=pack.v2Canonical[page];
  if(pack.v1Pages[canonical]&&canonical!==current)showV1(canonical);
  else if(canonical?.startsWith('events/')&&!pack.v1Pages[canonical]&&current!=='events/detail.html')showV1('events/detail.html');
 }
});pair('index.html');if(innerWidth<900)document.querySelector('button[data-mode=v2]').click();
</script></body></html>'''
    content=shell.replace('__OPTIONS__',''.join(options)).replace('__PACK__',json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
    (LAB/'compare.html').write_text(content)
    print(json.dumps({'comparisonPairs':len(mapping),'v1Pages':len(pages),'bytes':len(content.encode())}))
if __name__=='__main__':main()
