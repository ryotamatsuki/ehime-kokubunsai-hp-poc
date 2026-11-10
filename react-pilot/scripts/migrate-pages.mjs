import {readFileSync,writeFileSync,mkdirSync,readdirSync,existsSync} from 'node:fs';
import {resolve,relative,dirname,sep,extname} from 'node:path';

const root=resolve(import.meta.dirname,'../..');
const out=resolve(import.meta.dirname,'../src/data/legacy-pages.json');
const current='https://ryotamatsuki.github.io/ehime-kokubunsai-hp-poc/';
const originalEvents=['pre2026','stage','craft','literature','food','art'];
function originalToPilot(file) {
  if(file==='index.html') return '';
  if(file==='events/search.html') return 'events';
  if(file.startsWith('events/')&&originalEvents.includes(file.slice(7).replace(/\.html$/,''))) return 'events/'+file.slice(7,-5);
  return file.replace(/(?:\/index)?\.html$/,'');
}
function allPages(dir,depth=0) {
  if(depth>3) return [];
  return readdirSync(dir,{withFileTypes:true}).flatMap(item=>{
    if(item.name.startsWith('.')||['react-pilot','comparison','design-lab','node_modules','docs','scripts','assets'].includes(item.name))return [];
    const p=resolve(dir,item.name);
    if(item.isDirectory())return allPages(p,depth+1);
    return item.isFile()&&p.endsWith('.html')?[p]:[];
  });
}
function rewriteHref(href,file) {
  if(!href||href.startsWith('#')||/^(?:mailto:|tel:|data:|blob:)/i.test(href))return href;
  if(/^\s*javascript:/i.test(href))return '#';
  let url;
  try{url=new URL(href,current+file)}catch{return href}
  if(url.origin!==new URL(current).origin||!url.pathname.startsWith(new URL(current).pathname))return href;
  const rel=url.pathname.slice(new URL(current).pathname.length);
  if(rel.endsWith('.html'))return '/ehime-kokubunsai-hp-poc/react-pilot/'+originalToPilot(rel)+'/'+url.search+url.hash;
  return url.href;
}
function rewriteResource(href,file){
  if(!href||href.startsWith('#')||/^(?:data:|blob:)/i.test(href))return href;
  try{return new URL(href,current+file).href}catch{return href}
}
function rewriteHtml(html,file) {
  let out=html.replace(/<script\b[\s\S]*?<\/script\s*>/gi,'').replace(/\son[a-z]+\s*=\s*(?:"[^"]*"|'[^']*')/gi,'');
  out=out.replace(/\b(href|src|poster|action)\s*=\s*(["'])(.*?)\2/gi,(_,key,quote,value)=>{
    const newValue=key.toLowerCase()==='href'?rewriteHref(value,file):rewriteResource(value,file);
    return key+'='+quote+newValue.replace(/&/g,'&amp;')+quote;
  });
  out=out.replace(/\bsrcset\s*=\s*(["'])(.*?)\1/gi,(_,quote,value)=>{
    const changed=value.split(',').map(v=>{
      const m=v.trim().match(/^(\S+)(\s+.+)?$/);
      return m?rewriteResource(m[1],file)+(m[2]||''):'';
    }).join(', ');
    return 'srcset='+quote+changed+quote;
  });
  return out;
}
const entries=[];
const pages=allPages(root);
for(const page of pages){
  const file=relative(root,page).split(sep).join('/');
  const raw=readFileSync(page,'utf8');
  const main=raw.match(/<main\b[^>]*>([\s\S]*?)<\/main>/i);
  if(!main){
    if(file==='homepage_structure_document.html') continue; // ancillary design document, not a public route
    throw new Error('Missing <main> in '+file);
  }
  const title=(raw.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1]||file)
    .replace(/\s*\|\s*愛顔えひめの文化祭2028.*$/,'').trim();
  const route=originalToPilot(file);
  const routeEntries=raw.match(/window\.EHIME_V2_ROUTES\s*=\s*(\{[\s\S]*?\})\s*;/);
  const routeMap=routeEntries?Object.fromEntries(Object.entries(JSON.parse(routeEntries[1])).map(([k,v])=>[k,rewriteHref(v,file)])):{};
  entries.push({file,route,title,html:rewriteHtml(main[1],file),routeMap,
    originalPageName:raw.match(/data-page=["']([^"']+)/)?.[1]||file});
}
entries.sort((a,b)=>a.file.localeCompare(b.file));
const mapped=new Map();
for(const entry of entries){
  if(mapped.has(entry.route))throw new Error('Duplicate migrated URL: '+entry.route);
  mapped.set(entry.route,entry.file);
}
const skip=new Set(['','events',...originalEvents.map(x=>'events/'+x)]);
const legacy=entries.filter(x=>!skip.has(x.route));
if(entries.length<125)throw new Error('Unexpected incomplete content migration: '+entries.length+' routes');
if(legacy.length<118)throw new Error('Unexpected incomplete legacy conversion: '+legacy.length+' routes');
const expected=new Set(entries.map(x=>x.file));
if(!expected.has('culture/notebook.html')||!expected.has('accessibility/information-support.html'))throw new Error('Core pages missing');
mkdirSync(dirname(out),{recursive:true});
writeFileSync(out,JSON.stringify({source:'design-lab and original v2 pages',sourceCount:entries.length,
  migratedSpecific:[...skip],pages:legacy},null,0)+'\n');
console.log('Converted original v2: '+entries.length+' routes; '+legacy.length+' additional React-rendered archive pages; 8 custom React routes. No source files changed.');
