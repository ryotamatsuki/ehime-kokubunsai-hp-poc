/* Estimate Unicode-range font selection from styled, enhanced DOM; no real browser timing. */
const fs=require('node:fs'),path=require('node:path'),{JSDOM,VirtualConsole}=require('jsdom'),tree=require('css-tree');
const root=path.resolve(__dirname,'..'),lab=path.join(root,'design-lab'),[file,widthText]=process.argv.slice(2),width=Number(widthText);
const manifest=JSON.parse(fs.readFileSync(path.join(lab,'assets/manifest.json'),'utf8')),tokens=JSON.parse(fs.readFileSync(path.join(lab,'tokens.json'),'utf8'));
const ast=tree.parse(fs.readFileSync(path.join(lab,'experience.css'),'utf8'));
function screen(nodes){return nodes.toArray().map(n=>{
 if(n.type==='Atrule'&&n.name==='media'){
  const q=tree.generate(n.prelude),max=q.match(/max-width:(\d+)px/),min=q.match(/min-width:(\d+)px/);
  if(/print|forced-colors|prefers-reduced-motion/.test(q)||(max&&width>Number(max[1]))||(min&&width<Number(min[1])))return '';
  return screen(n.block.children);
 }return tree.generate(n);
}).join('');}
const d=new JSDOM(fs.readFileSync(path.join(lab,file),'utf8'),{url:'https://poc.example/'+file,runScripts:'outside-only',pretendToBeVisual:true,virtualConsole:new VirtualConsole()}),w=d.window;
const style=w.document.createElement('style');style.textContent=screen(ast.children);w.document.head.append(style);
w.matchMedia=q=>({matches:q.includes('max-width')&&width<=700,addEventListener(){}});
for(const s of w.document.querySelectorAll('script:not([src])'))w.eval(s.textContent);
for(const name of ['experience-data.js','experience.js','legacy-ui.js'])w.eval(fs.readFileSync(path.join(lab,name),'utf8'));
if(w.document.querySelector('[data-field-atlas],[data-haiku-studio],[data-field-journal-list]'))w.eval(fs.readFileSync(path.join(lab,'culture-experience.js'),'utf8'));
const fontRows=manifest.fonts.map(r=>({...r,points:new Set(r.codepoints)})),used=new Set(),unknown=new Set(),cache=new Map();
const css=n=>{if(!cache.has(n))cache.set(n,w.getComputedStyle(n));return cache.get(n);};
function visible(node){for(let n=node;n&&n.nodeType===1;n=n.parentElement){if(n.hidden||['SCRIPT','STYLE','NOSCRIPT','SVG'].includes(n.tagName)||css(n).display==='none')return false;if(n.tagName==='DETAILS'&&!n.open){const summary=n.querySelector('summary');if(!summary?.contains(node))return false;}}return true;}
function inspect(node,text){
 if(!visible(node))return;let family=css(node).fontFamily,weight=css(node).fontWeight;
 for(let parent=node.parentElement;parent&&(!family||!weight);parent=parent.parentElement){const s=css(parent);if(!family)family=s.fontFamily;if(!weight)weight=s.fontWeight;}
 family=family.replace('var(--font)',tokens.cssVariables.font).replace('var(--display-font)',tokens.cssVariables['display-font']);
 const families=family.split(',').map(x=>x.trim().replace(/["']/g,'')),numeric=weight==='bold'?700:Number(weight)||400;
 for(const c of text){const cp=c.codePointAt(0);if(/\s/.test(c))continue;let chosen;
  for(const name of families){const matches=fontRows.filter(r=>r.cssFamily===name&&r.points.has(cp));if(!matches.length)continue;
   chosen=matches.find(r=>r.weight==='200 800'||Number(r.weight)===(name==='Ehime Sans'?(numeric<=500?400:700):500))||matches[0];break;
  }
  if(chosen)used.add(chosen.path);else if(cp>=0x3000&&cp<=0x9fff)unknown.add(cp);
 }
}
const walker=w.document.createTreeWalker(w.document.body,w.NodeFilter.SHOW_TEXT);for(let n=walker.nextNode();n;n=walker.nextNode())inspect(n.parentElement,n.textContent);
for(const input of w.document.querySelectorAll('input,textarea'))inspect(input,input.value||input.placeholder||'');
const selected=manifest.fonts.filter(r=>used.has(r.path));process.stdout.write(JSON.stringify({page:file,width,fonts:selected.map(r=>({path:r.path,bytes:r.bytes})),bytes:selected.reduce((a,r)=>a+r.bytes,0),unknownJapanese:[...unknown].map(n=>String.fromCodePoint(n)).join(''),method:'jsdom CSS and Unicode-range selection estimate, not network/browser measurement'})+'\n');w.close();
