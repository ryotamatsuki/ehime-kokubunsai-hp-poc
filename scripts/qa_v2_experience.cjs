/* jsdom state/route checks. They do not prove browser or screen-reader behavior. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM}=require('jsdom');const root=path.resolve(__dirname,'..'),lab=path.join(root,'design-lab');
const read=f=>fs.readFileSync(path.join(lab,f),'utf8');const results=[];
function environment(file,query='',o={}){
 const dom=new JSDOM(read(file),{url:'https://poc.example/design-lab/'+file+query,runScripts:'outside-only',pretendToBeVisual:true});const w=dom.window;
 const media={matches:!!o.mobile,handlers:[],addEventListener(t,cb){this.handlers.push(cb)}};
 w.matchMedia=q=>q.includes('max-width')?media:{matches:!!o.reducedMotion,addEventListener(){}};
 for(const script of w.document.querySelectorAll('script:not([src])'))w.eval(script.textContent);
 if(o.storage)w.localStorage.setItem('ehime-v2-culture-notes',JSON.stringify(o.storage));
 if(o.blockStorage)Object.defineProperty(w,'localStorage',{get(){throw new Error('blocked')}});
 if(o.offline){w.__POC_OFFLINE__=true;w.__POC_QUERY__=query;w.__POC_NOTEBOOK__=o.saved||[]}
 w.eval(read('experience-data.js'));w.eval(read('experience.js'));w.eval(read('site-search-data.js'));w.eval(read('legacy-ui.js'));if(w.document.querySelector('[data-paint-studio]'))w.eval(read('painting.js'));return{dom,window:w,document:w.document,media};
}
async function test(name,fn){try{await fn();results.push({name,status:'PASS'})}catch(e){results.push({name,status:'FAIL',error:e.message})}}
const visible=d=>[...d.querySelectorAll('[data-event-card]')].filter(el=>!el.hidden);
async function main(){
await test('Culture -> sample event -> save -> notebook is one consistent choice',()=>{
 const a=environment('culture-craft.html');assert.equal(a.document.querySelector('[data-event-card] h3 a').getAttribute('href').split('?')[0],'event-craft.html');a.document.querySelector('[data-save="craft"]').click();assert.equal(a.document.querySelector('[data-book-count]').textContent,'1');
 const href=a.document.querySelector('.book-link').getAttribute('href');const b=environment('notebook.html','?'+href.split('?')[1]);assert.match(b.document.querySelector('[data-notebook-list]').textContent,/砥部焼とことば/);assert.equal(b.document.querySelector('[data-notebook-count]').textContent,'1');assert.match(b.document.querySelector('[data-notebook-list] h3 a').getAttribute('href'),/^event-craft.html\?saved=craft$/);a.dom.window.close();b.dom.window.close();
});
await test('Save toggle updates accessible names, announces action, and never duplicates',()=>{
 const e=environment('event-craft.html');const b=e.document.querySelector('[data-save]');b.click();assert.equal(b.getAttribute('aria-pressed'),'true');assert.match(b.getAttribute('aria-label'),/削除/);assert.match(e.document.querySelector('[data-global-status]').textContent,/追加/);b.click();assert.equal(b.getAttribute('aria-pressed'),'false');assert.equal(e.document.querySelector('[data-book-count]').textContent,'0');assert.deepEqual(JSON.parse(e.window.localStorage.getItem('ehime-v2-culture-notes')),[]);e.dom.window.close();
});
await test('Shared selections deduplicate, drop unknown IDs, preserve ordering',()=>{
 const e=environment('notebook.html','?saved=food,invalid,craft,food,<script>');assert.equal(e.document.querySelector('[data-notebook-count]').textContent,'2');assert.match(e.document.querySelector('[data-notebook-list] h3').textContent,/宇和海/);e.dom.window.close();
});
await test('Delete focus moves to the next item and then the empty-state action',()=>{
 const e=environment('notebook.html','?saved=craft,food');e.document.querySelector('[data-remove="craft"]').click();assert.equal(e.document.activeElement.dataset.remove,'food');e.document.querySelector('[data-remove="food"]').click();assert.equal(e.document.querySelector('[data-notebook-empty]').hidden,false);assert.equal(e.document.activeElement.tagName,'A');assert.equal(e.document.querySelector('[data-export]').disabled,true);e.dom.window.close();
});
await test('Storage failure keeps URL choices and explains persistence limit',()=>{
 const e=environment('notebook.html','?saved=craft',{blockStorage:true});assert.equal(e.document.querySelector('[data-notebook-count]').textContent,'1');assert.match(e.document.querySelector('[data-storage-status]').textContent,/保存を利用できません/);assert.match(e.document.querySelector('.header-search').getAttribute('href'),/saved=craft/);e.dom.window.close();
});
await test('Japanese AND keyword and city filters select the intended sample',()=>{
 const e=environment('event-search.html');const q=e.document.getElementById('filter-q');q.value='砥部 工芸';q.dispatchEvent(new e.window.Event('input'));assert.equal(visible(e.document).length,1);assert.equal(visible(e.document)[0].dataset.id,'craft');const city=e.document.getElementById('filter-city');city.value='松山市';city.dispatchEvent(new e.window.Event('change'));assert.equal(visible(e.document).length,0);assert.equal(e.document.querySelector('[data-empty]').hidden,false);e.dom.window.close();
});
await test('Verified filter excludes samples; sample support is not an official guarantee',()=>{
 const e=environment('event-search.html','?kind=verified');assert.equal(visible(e.document).length,1);assert.equal(visible(e.document)[0].dataset.id,'pre2026');assert.match(visible(e.document)[0].textContent,/公式案内/);const s=e.document.getElementById('filter-support');s.value='車椅子席';s.dispatchEvent(new e.window.Event('change'));assert.equal(visible(e.document).length,0);e.dom.window.close();
});
await test('URL support restores and reset retains notebook and input focus',()=>{
 const e=environment('event-search.html','?support=手話通訳&saved=craft');assert.deepEqual(visible(e.document).map(card=>card.dataset.id),['stage','art']);e.document.querySelector('[data-reset]').click();assert.equal(visible(e.document).length,6);assert.equal(e.document.activeElement.id,'filter-q');assert.equal(e.window.location.search,'?saved=craft');e.dom.window.close();
});
await test('Unknown URL selector recovers and HTML-like query remains inert',()=>{
 const e=environment('event-search.html','?city=not-a-city&kind=bad');assert.equal(visible(e.document).length,6);const q=e.document.getElementById('filter-q');q.value='<img src=x onerror=alert(1)>';q.dispatchEvent(new e.window.Event('input'));assert.equal(visible(e.document).length,0);assert.equal(e.document.querySelector('img[src=x]'),null);e.dom.window.close();
});
await test('Back-forward URL restoration synchronizes filter and notebook',()=>{
 const e=environment('event-search.html','?genre=文学');e.window.history.replaceState(null,'','?genre=工芸&saved=food');e.window.dispatchEvent(new e.window.PopStateEvent('popstate'));assert.equal(visible(e.document)[0].dataset.id,'craft');assert.equal(e.document.querySelector('[data-book-count]').textContent,'1');e.dom.window.close();
});
await test('Mobile menu opens; Escape returns focus; desktop resize restores navigation',()=>{
 const e=environment('index.html','',{mobile:true});const b=e.document.querySelector('[data-menu]'),n=e.document.querySelector('[data-navigation]');assert.equal(n.hidden,true);assert.equal(b.hidden,false);b.click();assert.equal(n.hidden,false);e.document.dispatchEvent(new e.window.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));assert.equal(n.hidden,true);assert.equal(e.document.activeElement,b);e.media.matches=false;e.media.handlers.forEach(cb=>cb());assert.equal(n.hidden,false);assert.equal(b.hidden,true);e.dom.window.close();
});
await test('Following mobile navigation closes disclosure without a modal focus trap',()=>{
 const e=environment('index.html','',{mobile:true});e.document.querySelector('[data-menu]').click();e.document.querySelector('[data-navigation] a').dispatchEvent(new e.window.MouseEvent('click',{bubbles:true,cancelable:true}));assert.equal(e.document.querySelector('[data-menu]').getAttribute('aria-expanded'),'false');assert.equal(e.document.querySelector('[role=dialog]'),null);e.dom.window.close();
});
await test('Reduced-motion setting suppresses save animation',()=>{
 const e=environment('event-craft.html','',{reducedMotion:true});const b=e.document.querySelector('[data-save]');b.click();assert.equal(b.classList.contains('is-updated'),false);e.dom.window.close();
});
await test('Offline pack retains notebook and hides unsupported share URL action',()=>{
 const e=environment('notebook.html','',{offline:true,saved:['craft','food']});assert.equal(e.document.querySelector('[data-notebook-count]').textContent,'2');assert.equal(e.document.querySelector('[data-share]').hidden,true);e.document.querySelector('[data-remove="food"]').click();assert.equal(e.window.__POC_QUERY__,'?saved=craft');assert.match(e.document.querySelector('.header-search').getAttribute('href'),/saved=craft/);e.dom.window.close();
});
await test('Clipboard failure presents a focused selectable link with the exact items',async()=>{
 const e=environment('notebook.html','?saved=art,craft');e.document.querySelector('[data-share]').click();await Promise.resolve();assert.equal(e.document.querySelector('[data-share-fallback]').hidden,false);assert.equal(e.document.activeElement.id,'share-url');assert.match(e.document.activeElement.value,/saved=art%2Ccraft$/);e.dom.window.close();
});
await test('SVG export contains selected events and statuses, excludes other events',async()=>{
 const e=environment('notebook.html','?saved=craft,pre2026');let blob,name;e.window.URL.createObjectURL=b=>{blob=b;return'blob:poc-export'};e.window.URL.revokeObjectURL=()=>{};e.window.HTMLAnchorElement.prototype.click=function(){name=this.download};e.document.querySelector('[data-export]').click();assert.equal(name,'ehime-culture-notes.svg');assert.equal(blob.type,'image/svg+xml;charset=utf-8');const reader=new e.window.FileReader();const body=await new Promise((resolve,reject)=>{reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsText(blob)});assert.match(body,/砥部焼とことば/);assert.match(body,/総合フェスティバル2026/);assert.match(body,/架空の掲載例/);assert.match(body,/受付終了/);assert.doesNotMatch(body,/宇和海から、食卓/);e.dom.window.close();
});
await test('No-JS pages expose cultural stories, all links, event facts, and source states',()=>{
 for(const f of ['index.html','culture-craft.html','event-craft.html','event-pre2026.html','documents.html']){const dom=new JSDOM(read(f));const d=dom.window.document;assert.ok(d.querySelector('main h1'));assert.ok(d.querySelector('[data-navigation] a'));assert.equal(d.querySelector('[data-navigation]').hasAttribute('hidden'),false);if(f.startsWith('event-'))assert.ok(d.querySelector('.event-facts dd'));dom.window.close()}
});
await test('Actual pre-event is clearly closed, without an application form',()=>{
 const dom=new JSDOM(read('event-pre2026.html'));const d=dom.window.document;assert.match(d.querySelector('.event-facts').textContent,/受付は終了/);assert.match(d.querySelector('.event-facts').textContent,/当日券の配付はありません/);assert.equal(d.querySelector('form'),null);assert.match(d.querySelector('.event-state').textContent,/公開情報/);dom.window.close();
});

await test('Keyboard painting presets add distinct strokes, undo and clear keep an accurate draft',()=>{
 const e=environment('culture-craft.html');const d=e.document;assert.equal(d.querySelector('[data-paint-studio]').hidden,false);for(const name of ['circle','wave','line'])d.querySelector('[data-paint-preset="'+name+'"]').click();assert.equal(d.querySelectorAll('[data-paint-lines] path').length,3);assert.equal(new Set([...d.querySelectorAll('[data-paint-lines] path')].map(p=>p.getAttribute('d'))).size,3);d.querySelector('[data-paint-undo]').click();assert.equal(d.querySelectorAll('[data-paint-lines] path').length,2);d.querySelector('[data-paint-clear]').click();assert.equal(d.querySelectorAll('[data-paint-lines] path').length,0);assert.equal(d.querySelector('[data-paint-export]').disabled,true);e.dom.window.close();
});
await test('Painting is opt-in for pointer input; cancel discards the unfinished line',()=>{
 const e=environment('culture-craft.html');const d=e.document,b=d.querySelector('[data-paint-board]');b.getBoundingClientRect=()=>({left:0,top:0,width:600,height:540});const event=(type,x,y)=>new e.window.MouseEvent(type,{clientX:x,clientY:y,bubbles:true,cancelable:true,button:0});const inactive=event('pointerdown',200,200);b.dispatchEvent(inactive);assert.equal(inactive.defaultPrevented,false);assert.equal(d.querySelectorAll('[data-paint-lines] path').length,0);d.querySelector('[data-paint-mode]').click();const active=event('pointerdown',200,200);b.dispatchEvent(active);assert.equal(active.defaultPrevented,true);b.dispatchEvent(event('pointermove',235,240));b.dispatchEvent(event('pointercancel',235,240));assert.equal(d.querySelectorAll('[data-paint-lines] path').length,0);e.dom.window.close();
});
await test('A completed drawn line is persisted; Escape exits painting and returns focus',()=>{
 const e=environment('culture-craft.html');const d=e.document,b=d.querySelector('[data-paint-board]'),m=d.querySelector('[data-paint-mode]');b.getBoundingClientRect=()=>({left:0,top:0,width:600,height:540});m.click();for(const[type,x,y]of [['pointerdown',200,200],['pointermove',250,240],['pointerup',250,240]])b.dispatchEvent(new e.window.MouseEvent(type,{clientX:x,clientY:y,bubbles:true,cancelable:true,button:0}));assert.equal(JSON.parse(e.window.localStorage.getItem('ehime-v2-blue-painting')).length,1);d.dispatchEvent(new e.window.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));assert.equal(m.getAttribute('aria-pressed'),'false');assert.equal(d.activeElement,m);e.dom.window.close();
});
await test('Painting has a bounded number of strokes and validates restored vector paths',()=>{
 const e=environment('culture-craft.html');const d=e.document;for(let i=0;i<33;i++)d.querySelector('[data-paint-preset="circle"]').click();assert.equal(d.querySelectorAll('[data-paint-lines] path').length,32);assert.match(d.querySelector('[data-paint-status]').textContent,/32筆まで/);const raw=read('culture-craft.html');const dom=new JSDOM(raw,{url:'https://poc.example/culture-craft.html',runScripts:'outside-only'});dom.window.localStorage.setItem('ehime-v2-blue-painting',JSON.stringify([{d:'M 1 2 L 4 5',width:4},{d:'<script>alert(1)</script>',width:8},{d:'M 1 2',width:999}]));dom.window.eval(read('painting.js'));assert.equal(dom.window.document.querySelectorAll('[data-paint-lines] path').length,1);dom.window.close();e.dom.window.close();
});
await test('Painting SVG export contains the authored strokes and mask, without scripts',async()=>{
 const e=environment('culture-craft.html');let blob,name;e.window.URL.createObjectURL=b=>{blob=b;return'blob:poc-blue'};e.window.URL.revokeObjectURL=()=>{};e.window.HTMLAnchorElement.prototype.click=function(){name=this.download};e.document.querySelector('[data-paint-preset="wave"]').click();e.document.querySelector('[data-paint-export]').click();assert.equal(name,'ehime-my-blue.svg');const reader=new e.window.FileReader();const source=await new Promise(resolve=>{reader.onload=()=>resolve(reader.result);reader.readAsText(blob)});assert.match(source,/clipPath/);assert.match(source,/stroke="#183c9e"/);assert.doesNotMatch(source,/<script/);e.dom.window.close();
});
await test('Notebook cultural mark updates both geometry and its readable theme description',()=>{
 const e=environment('notebook.html','?saved=craft,art');assert.match(e.document.querySelector('[data-notebook-themes]').textContent,/手ざわり、表現/);const before=e.document.querySelector('[data-notebook-pattern]').innerHTML;e.document.querySelector('[data-remove="craft"]').click();assert.notEqual(e.document.querySelector('[data-notebook-pattern]').innerHTML,before);assert.doesNotMatch(e.document.querySelector('[data-notebook-themes]').textContent,/手ざわり/);e.dom.window.close();
});
await test('Offline pack loads complete inline DOM, routes, assets, painting and notebook state',()=>{
 const shell=new JSDOM(read('review.html'),{url:'https://offline.example/review.html',runScripts:'outside-only'});const w=shell.window;w.scrollTo=()=>{};for(const script of w.document.querySelectorAll('script:not([type])'))w.eval(script.textContent);w.loadPage('culture-craft.html');const source=w.document.getElementById('preview').srcdoc;assert.match(source,/<\/main>/);const child=new JSDOM(source,{url:'https://offline.example/frame',runScripts:'outside-only',pretendToBeVisual:true});child.window.matchMedia=()=>({matches:false,addEventListener(){}});for(const script of child.window.document.querySelectorAll('script'))child.window.eval(script.textContent);assert.equal(child.window.document.querySelectorAll('script[src]').length,0);assert.equal(child.window.document.querySelector('[data-paint-studio]').hidden,false);assert.ok(child.window.document.querySelector('img').src.startsWith('data:image/webp'));child.window.document.querySelector('[data-paint-preset="wave"]').click();assert.equal(child.window.document.querySelectorAll('[data-paint-lines] path').length,1);child.window.close();shell.window.close();
});

const output={version:JSON.parse(read('content.json')).version,method:'jsdom state and route logic; not browser/screen-reader confirmation',passed:results.filter(r=>r.status==='PASS').length,total:results.length,results};fs.writeFileSync(path.join(lab,'qa','interaction-checks.json'),JSON.stringify(output,null,2)+'\n');process.stdout.write(JSON.stringify(output,null,2)+'\n');if(results.some(r=>r.status!=='PASS'))process.exitCode=1;
}
main();
