/* Revision-specific source retention, forms and offline comparison checks. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require('jsdom');
const root=path.resolve(__dirname,'..'),lab=path.join(root,'design-lab'),read=name=>fs.readFileSync(path.join(lab,name),'utf8');
const results=[];
function test(name,fn){try{fn();results.push({name,status:'PASS'})}catch(error){results.push({name,status:'FAIL',error:error.message})}}
function dom(html,url='https://poc.example/index.html'){const d=new JSDOM(html,{url,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:new VirtualConsole()});d.window.matchMedia=()=>({matches:false,addEventListener(){}});d.window.scrollTo=()=>{};return d}
function page(name,query=''){const d=dom(read(name),'https://poc.example/'+name+query);for(const script of d.window.document.querySelectorAll('script:not([src])'))d.window.eval(script.textContent);d.window.eval(read('experience-data.js'));d.window.eval(read('experience.js'));d.window.eval(read('site-search-data.js'));d.window.eval(read('legacy-ui.js'));return d}
test('All six events have a unique generated photograph in listing and detail',()=>{
 const d=page('event-search.html'),cards=[...d.window.document.querySelectorAll('[data-event-card]')];assert.equal(cards.length,6);
 const images=cards.map(card=>card.querySelector('img').getAttribute('src'));assert.equal(new Set(images).size,6);
 const data=JSON.parse(read('content.json'));for(const event of data.events){assert.ok(read(event.page).includes('assets/art/'+event.image+'-960.webp'));assert.ok(event.imageAlt.includes('イメージ'))}d.window.close();
});
test('Notebook uses event images on a canonical route',()=>{
 const html=fs.readFileSync(path.join(root,'culture/notebook.html'),'utf8'),d=dom(html,'https://poc.example/culture/notebook.html?saved=stage,food');
 for(const script of d.window.document.querySelectorAll('script:not([src])'))d.window.eval(script.textContent);d.window.eval(read('experience-data.js'));d.window.eval(read('experience.js'));
 const imgs=[...d.window.document.querySelectorAll('.notebook-event-image')];assert.equal(imgs.length,2);assert.equal(imgs[0].src,'https://poc.example/design-lab/assets/art/event-stage-480.webp');assert.equal(imgs[1].src,'https://poc.example/design-lab/assets/art/event-food-480.webp');d.window.close();
});
test('All 114 original routes are discoverable through the site index',()=>{const d=page('info-common-search.html');assert.equal(d.window.EHIME_V2_SITE_INDEX.length,114);assert.equal(d.window.document.querySelectorAll('.search-result').length,114);d.window.close()});
test('Japanese site search reaches preserved tourism and form content',()=>{
 const d=page('info-common-search.html','?q=周遊'),input=d.window.document.querySelector('[data-search-input]');assert.ok(d.window.document.querySelectorAll('.search-result').length>0);assert.match(d.window.document.querySelector('[data-search-results]').textContent,/周遊/);
 input.value='お問い合わせ';input.dispatchEvent(new d.window.Event('input'));assert.ok(d.window.document.querySelector('a[href*="contact-form.html"]'));d.window.close();
});
test('Retained filters operate on the four v1 event cards',()=>{
 const d=page('info-events-by-city.html'),panel=d.window.document.querySelector('[data-legacy-filter]'),input=panel.querySelector('[data-filter-input]');assert.equal(panel.querySelectorAll('[data-legacy-event-card]').length,4);
 input.value='俳句';input.dispatchEvent(new d.window.Event('input'));const visible=[...panel.querySelectorAll('[data-legacy-event-card]')].filter(c=>!c.hidden);assert.equal(visible.length,1);assert.match(visible[0].textContent,/俳句とまち歩き/);d.window.close();
});
test('Prototype contact form stays local and announces its state',()=>{
 const d=page('info-contact-form.html'),form=d.window.document.querySelector('[data-local-demo-form]'),submit=form.querySelector('[data-local-demo-submit]');assert.equal(submit.disabled,false);
 const event=new d.window.Event('submit',{bubbles:true,cancelable:true});form.dispatchEvent(event);assert.equal(event.defaultPrevented,true);assert.match(form.querySelector('[role=status]').textContent,/送信は行われません/);d.window.close();
});
test('Comparison pack retains byte-identical v1 HTML and all paired routes',()=>{
 const d=dom(read('compare.html')),pack=JSON.parse(d.window.document.querySelector('#comparison-pack').textContent);assert.equal(Object.keys(pack.v2Routes).length,114);assert.equal(Object.keys(pack.v1Pages).length,115);
 for(const [name,source]of Object.entries(pack.v1Pages))assert.equal(source,fs.readFileSync(path.join(root,'comparison/v1',name),'utf8'));assert.equal(Object.keys(pack.v1Assets).length,19);d.window.close();
});
test('Comparison left pane is self-contained, interactive and paired with v2',()=>{
 const d=dom(read('compare.html'));for(const script of d.window.document.querySelectorAll('script:not([type])'))d.window.eval(script.textContent);
 const left=d.window.document.querySelector('#v1-preview'),right=d.window.document.querySelector('#v2-preview');assert.match(right.getAttribute('src'),/review.html#embedded=1&page=index.html/);
 const child=dom(left.srcdoc);assert.equal(child.window.document.querySelectorAll('script[src],link[rel=stylesheet]').length,0);for(const img of child.window.document.querySelectorAll('img'))assert.ok(img.getAttribute('src').startsWith('data:image/'));
 for(const script of child.window.document.querySelectorAll('script:not([type])'))child.window.eval(script.textContent);assert.ok(child.window.SITE_SEARCH_INDEX.length);child.window.close();
 d.window.pair('events/search.html');const events=dom(left.srcdoc);for(const script of events.window.document.querySelectorAll('script:not([type])'))events.window.eval(script.textContent);assert.equal(events.window.document.querySelectorAll('[data-event-card]').length,4);assert.match(right.getAttribute('src'),/page=event-search.html/);events.window.close();d.window.close();
});
test('Comparison offers full-width PC and a fixed 390px review',()=>{
 const d=dom(read('compare.html'));for(const script of d.window.document.querySelectorAll('script:not([type])'))d.window.eval(script.textContent);
 d.window.document.querySelector('button[data-mode=v2]').click();assert.equal(d.window.document.querySelector('.stage').dataset.mode,'v2');assert.equal(d.window.document.querySelector('button[data-mode=v2]').getAttribute('aria-pressed'),'true');
 d.window.document.querySelector('[data-mobile]').click();assert.equal(d.window.document.querySelectorAll('iframe.width-fixed').length,2);d.window.close();
});
const report={version:JSON.parse(read('content.json')).version,method:'jsdom content, local controls and offline source assembly; not a browser display test',passed:results.filter(r=>r.status==='PASS').length,total:results.length,results};
fs.writeFileSync(path.join(lab,'qa/revision-checks.json'),JSON.stringify(report,null,2)+'\n');process.stdout.write(JSON.stringify(report,null,2)+'\n');if(report.passed!==report.total)process.exitCode=1;
