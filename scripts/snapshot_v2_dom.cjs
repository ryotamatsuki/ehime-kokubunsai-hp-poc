/* Serialize enhanced DOM for static layout references. No browser rendering here. */
const fs=require('node:fs'),path=require('node:path');const {JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),lab=path.join(root,'design-lab');
const [file,width,out,query='']=process.argv.slice(2);
const html=fs.readFileSync(path.join(lab,file),'utf8');
const dom=new JSDOM(html,{url:'https://poc.example/'+file+query,runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window;w.matchMedia=q=>({matches:q.includes('max-width')?Number(width)<=700:false,addEventListener(){}});
for(const s of w.document.querySelectorAll('script:not([src])'))w.eval(s.textContent);
w.eval(fs.readFileSync(path.join(lab,'experience-data.js'),'utf8'));w.eval(fs.readFileSync(path.join(lab,'experience.js'),'utf8'));
if(w.document.querySelector('[data-search-page]'))w.eval(fs.readFileSync(path.join(lab,'site-search-data.js'),'utf8'));
w.eval(fs.readFileSync(path.join(lab,'legacy-ui.js'),'utf8'));
if(w.document.querySelector('[data-paint-studio]')){w.eval(fs.readFileSync(path.join(lab,'painting.js'),'utf8'));w.document.querySelector('[data-paint-preset="circle"]').click();w.document.querySelector('[data-paint-preset="wave"]').click()}
for(const input of w.document.querySelectorAll('input'))input.setAttribute('value',input.value);
for(const select of w.document.querySelectorAll('select'))for(const option of select.options){if(option.selected)option.setAttribute('selected','');else option.removeAttribute('selected')}
for(const element of w.document.querySelectorAll('noscript'))element.remove();
fs.writeFileSync(out,dom.serialize());dom.window.close();
