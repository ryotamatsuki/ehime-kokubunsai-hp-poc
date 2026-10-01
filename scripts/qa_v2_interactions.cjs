/* Run: NODE_PATH=/path/to/jsdom/node_modules node scripts/qa_v2_interactions.cjs */
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");
const { JSDOM } = require("jsdom");
const root = path.resolve(__dirname, "..");
const lab = path.join(root, "design-lab");
const read = file => fs.readFileSync(path.join(lab, file), "utf8");
const results = [];
function environment(file, query = "", mobile = false) {
  const dom = new JSDOM(read(file), {url: "https://lab.example/" + file + query, runScripts: "outside-only", pretendToBeVisual: true});
  const media = {matches: mobile, handlers: [], addEventListener(type, cb) { this.handlers.push(cb); }};
  dom.window.matchMedia = () => media;
  dom.window.eval(read("events-data.js"));
  dom.window.eval(read("ui.js"));
  return {dom, window:dom.window, document:dom.window.document, media};
}
function test(name, fn) {
  try { fn(); results.push({name,status:"PASS"}); }
  catch(error) { results.push({name,status:"FAIL",error:error.message}); }
}
const visible = doc => [...doc.querySelectorAll("[data-event-card]")].filter(card => !card.hidden);
test("Japanese keyword and city select identify the pottery sample", () => {
  const {window,document,dom}=environment("event-search.html");
  const input=document.getElementById("filter-q");input.value="砥部";input.dispatchEvent(new window.Event("input",{bubbles:true}));
  assert.equal(visible(document).length,1);assert.match(visible(document)[0].textContent,/砥部焼/);
  const select=document.getElementById("filter-city");select.value="松山市";select.dispatchEvent(new window.Event("change",{bubbles:true}));
  assert.equal(visible(document).length,0);assert.equal(document.querySelector("[data-empty]").hidden,false);
  dom.window.close();
});
test("URL state restores genre and accessibility selection",()=>{
  const {document,dom}=environment("event-search.html","?genre=舞台&support=手話通訳");
  assert.equal(document.getElementById("filter-genre").value,"舞台");
  assert.equal(visible(document).length,1);assert.match(visible(document)[0].textContent,/瀬戸内文化/);
  dom.window.close();
});
test("Unknown select values in a URL do not silently remove all results",()=>{
  const {document,dom}=environment("event-search.html","?city=不存在の市");
  assert.equal(document.getElementById("filter-city").value,"");assert.equal(visible(document).length,4);
  dom.window.close();
});
test("Reset restores four results and focuses the keyword input",()=>{
  const {window,document,dom}=environment("event-search.html","?q=該当しない催し&direction=poster");
  assert.equal(visible(document).length,0);
  document.querySelector("[data-empty] [data-reset-filters]").click();
  assert.equal(visible(document).length,4);assert.equal(document.querySelector("[data-empty]").hidden,true);
  assert.equal(document.activeElement.id,"filter-q");
  assert.equal(window.location.search,"?direction=poster");dom.window.close();
});
test("Multiple keyword terms use a conjunctive search and input stays plain text",()=>{
  const {window,document,dom}=environment("event-search.html");
  const input=document.getElementById("filter-q");input.value="松山市 文学";input.dispatchEvent(new window.Event("input"));
  assert.equal(visible(document).length,1);assert.match(visible(document)[0].textContent,/俳句/);
  input.value="<img src=x onerror=alert(1)>";input.dispatchEvent(new window.Event("input"));
  assert.equal(visible(document).length,0);assert.equal(document.querySelector('img[src="x"]'),null);
  dom.window.close();
});
test("Mobile disclosure opens, Escape closes, and focus returns to the trigger",()=>{
  const {window,document,dom}=environment("home-a.html","",true);
  const button=document.querySelector("[data-menu-toggle]");const nav=document.querySelector("[data-main-nav]");
  assert.equal(nav.hidden,true);assert.equal(button.hidden,false);
  button.click();assert.equal(nav.hidden,false);assert.equal(button.getAttribute("aria-expanded"),"true");
  document.dispatchEvent(new window.KeyboardEvent("keydown",{key:"Escape",bubbles:true}));
  assert.equal(nav.hidden,true);assert.equal(button.getAttribute("aria-expanded"),"false");
  assert.equal(document.activeElement,button);dom.window.close();
});
test("Returning from mobile to desktop leaves the navigation visible",()=>{
  const {document,media,dom}=environment("home-a.html","",true);
  media.matches=false;media.handlers.forEach(fn=>fn());
  assert.equal(document.querySelector("[data-main-nav]").hidden,false);
  assert.equal(document.querySelector("[data-menu-toggle]").hidden,true);dom.window.close();
});
test("Details stay consistent for each selected sample and unknown IDs",()=>{
  for(const [id,title,city] of [["stage","瀬戸内文化ステージ","松山市"],["craft","砥部焼とことば","砥部町"],["food","宇和海の食文化","宇和島市"],["literature","俳句とまち歩き","松山市"],["unknown","砥部焼とことば","砥部町"]]){
    const {document,dom}=environment("event-detail.html","?id="+id);
    assert.match(document.querySelector("[data-detail-title]").textContent,new RegExp(title));
    assert.match(document.querySelector("[data-detail-city]").textContent,new RegExp(city));
    assert.match(document.title,new RegExp(title));
    assert.ok(document.querySelector("[data-detail-support]").children.length>0);dom.window.close();
  }
});
test("Poster direction persists through search and detail navigation",()=>{
  const {document,dom}=environment("event-search.html","?direction=poster");
  assert.equal(document.documentElement.dataset.direction,"poster");
  const href=visible(document)[0].querySelector("h3 a").getAttribute("href");
  assert.match(href,/direction=poster/);assert.match(href,/id=stage/);
  assert.equal(document.querySelector(".brand").getAttribute("href"),"home-b.html");dom.window.close();
});
test("No JavaScript HTML keeps four sample events and complete default details",()=>{
  const search=new JSDOM(read("event-search.html"));
  assert.equal(visible(search.window.document).length,4);
  assert.equal(search.window.document.querySelectorAll("[data-js-only]:not([hidden])").length,0);
  assert.equal(search.window.document.querySelector("[data-main-nav]").hidden,false);
  const detail=new JSDOM(read("event-detail.html"));
  assert.match(detail.window.document.querySelector("[data-detail-title]").textContent,/砥部焼/);
  assert.match(detail.window.document.querySelector(".event-facts").textContent,/開催日/);
  assert.ok(detail.window.document.querySelector(".detail-aside").compareDocumentPosition(detail.window.document.querySelector(".article-body")) & detail.window.Node.DOCUMENT_POSITION_FOLLOWING);
  search.window.close();detail.window.close();
});
test("Offline bundle initializes each page and injects assets without external requests",()=>{
  const dom=new JSDOM(read("review.html"),{url:"https://offline.example/review.html",runScripts:"outside-only",pretendToBeVisual:true});
  dom.window.scrollTo=()=>{};
  const scripts=[...dom.window.document.querySelectorAll("script")].filter(s=>s.type!=="application/json");
  scripts.forEach(s=>dom.window.eval(s.textContent));
  const iframe=dom.window.document.getElementById("preview");
  for(const file of ["index.html","home-a.html","home-b.html","event-search.html","event-detail.html","documents.html","components.html"]){
    dom.window.document.querySelector('[data-page="'+file+'"]').click();
    const embedded=new JSDOM(iframe.srcdoc);
    const doc=embedded.window.document;
    assert.equal(doc.querySelectorAll("h1").length,1);
    assert.equal(doc.querySelectorAll("script[src],link[rel=stylesheet]").length,0);
    assert.ok([...doc.querySelectorAll("img")].every(img=>img.src.startsWith("data:")));
    embedded.window.close();
  }
  dom.window.document.querySelector('[data-width="390"]').click();
  assert.equal(iframe.style.width,"390px");dom.window.close();
});
test("Culture choice updates photograph, text, genre route and selected event together",()=>{
  const {document,window,dom}=environment("home-a.html");
  const button=document.querySelector('[data-culture="food"]');button.focus();button.click();
  assert.equal(button.getAttribute("aria-pressed"),"true");
  assert.equal(document.querySelectorAll('[data-culture][aria-pressed="true"]').length,1);
  assert.match(document.querySelector("[data-culture-photo]").src,/uwajima-sea-culture/);
  assert.match(document.querySelector("[data-culture-title]").textContent,/ひと皿/);
  const url=new URL(document.querySelector("[data-culture-search]").href);
  assert.equal(url.searchParams.get("genre"),"食文化");
  assert.match(document.querySelector("[data-culture-detail]").href,/id=food/);
  assert.match(document.querySelector("[data-culture-announcement]").textContent,/食文化/);
  assert.equal(document.activeElement,button);assert.match(window.location.search,/culture=food/);
  const search=environment("event-search.html",url.search);
  assert.equal(visible(search.document).length,1);assert.match(visible(search.document)[0].textContent,/宇和海/);
  search.dom.window.close();dom.window.close();
});
test("Culture URL restores a choice, unknown choices recover, and back navigation restores state",()=>{
  for(const [query,key] of [["?culture=literature","literature"],["?culture=unknown","craft"]]){
    const {document,window,dom}=environment("home-a.html",query);
    assert.equal(document.querySelector('[data-culture="'+key+'"]').getAttribute("aria-pressed"),"true");
    window.history.replaceState(null,"","?culture=stage");window.dispatchEvent(new window.PopStateEvent("popstate"));
    assert.equal(document.querySelector('[data-culture="stage"]').getAttribute("aria-pressed"),"true");
    assert.match(document.querySelector("[data-culture-detail]").href,/id=stage/);dom.window.close();
  }
});
test("Participation intent changes to the matching task without losing focus or direction",()=>{
  const {document,window,dom}=environment("home-b.html");
  for(const [key,path,fragment,image] of [["make","documents.html","#participation","family-culture-workshop"],["together","event-detail.html","#support","inclusive-art-gallery"],["watch","event-search.html","","event-stage-lanterns"]]){
    const button=document.querySelector('[data-intent="'+key+'"]');button.focus();button.click();
    const route=new URL(document.querySelector("[data-intent-link]").href);
    assert.equal(route.pathname,"/"+path);assert.equal(route.hash,fragment);assert.equal(route.searchParams.get("direction"),"poster");
    assert.match(document.querySelector("[data-intent-photo]").src,new RegExp(image));
    assert.equal(document.querySelectorAll('[data-intent][aria-pressed="true"]').length,1);
    assert.equal(document.activeElement,button);assert.match(window.location.search,new RegExp("intent="+key));
    assert.ok(document.querySelector("[data-intent-announcement]").textContent.length>0);
  }
  dom.window.close();
});
test("Participation URL and offline query restore the correct route",()=>{
  for(const key of ["together","unknown"]){
    const {document,dom}=environment("home-b.html","?intent="+key);
    assert.equal(document.querySelector('[data-intent="'+(key==="unknown"?"watch":key)+'"]').getAttribute("aria-pressed"),"true");dom.window.close();
  }
  const {document,window,dom}=environment("home-b.html");window.__INITIAL_QUERY__="?intent=make";
  window.dispatchEvent(new window.PopStateEvent("popstate"));
  assert.match(document.querySelector("[data-intent-link]").href,/#participation/);
  document.querySelector('[data-intent="together"]').click();assert.match(window.__INITIAL_QUERY__,/intent=together/);dom.window.close();
});
test("Both concepts keep all task routes and core information without JavaScript",()=>{
  for(const file of ["home-a.html","home-b.html"]){
    const dom=new JSDOM(read(file));const doc=dom.window.document;
    assert.equal(doc.querySelectorAll("[data-js-only]:not([hidden])").length,0);
    for(const id of ["about","join","news"])assert.ok(doc.getElementById(id));
    assert.ok(doc.querySelector('a[href*="event-search.html"]'));
    assert.ok(doc.querySelector('a[href*="#support"]'));
    assert.ok(doc.querySelector('a[href*="#participation"]'));
    if(file==="home-a.html")assert.equal(doc.querySelectorAll(".culture-line").length,4);
    else assert.equal(doc.querySelectorAll(".poster-path").length,3);
    dom.window.close();
  }
});
const report={scope:"jsdom logic regression; not browser layout, timing, screen reader or real key event certification",results,status:results.every(r=>r.status==="PASS")?"PASS":"FAIL"};
fs.mkdirSync(path.join(lab,"qa"),{recursive:true});
fs.writeFileSync(path.join(lab,"qa/interaction-checks.json"),JSON.stringify(report,null,2)+"\n");
console.log(JSON.stringify(report,null,2));
process.exitCode=report.status==="PASS"?0:1;
