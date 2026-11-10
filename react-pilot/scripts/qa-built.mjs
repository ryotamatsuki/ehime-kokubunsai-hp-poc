import {existsSync,readFileSync,writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
const root=resolve(import.meta.dirname,'..');
const base='/ehime-kokubunsai-hp-poc/react-pilot/';
const manifest=JSON.parse(readFileSync(resolve(root,'src/data/legacy-pages.json'),'utf8'));
const catalog=JSON.parse(readFileSync(resolve(root,'src/data/events.json'),'utf8'));
const routes=['', 'events', ...catalog.map(e=>'events/'+e.id), ...manifest.pages.map(p=>p.route)];
const unique=new Set(routes);
if(unique.size!==128||manifest.sourceCount!==128)throw new Error('Source-to-build route count does not match the 128-page inventory');
const failures=[];
const hrefs=new Set();
for(const route of routes){
  const path=resolve(root,'dist',route,'index.html');
  if(!existsSync(path)){failures.push('Missing generated page: '+route);continue}
  const html=readFileSync(path,'utf8');
  if(!html.includes('lang="ja"')||!/<h1\b/i.test(html)||!html.includes('noindex')){
    failures.push('Language/heading/PoC metadata incomplete: '+route);
  }
  for(const match of html.matchAll(/<a\b[^>]*\bhref=(["'])(.*?)\1/gi)){
    const href=match[2].replace(/&amp;/g,'&');
    if(!href||href.startsWith('#'))continue;
    let parsed;
    try{parsed=new URL(href,'https://ryotamatsuki.github.io'+base+route+'/')}catch{continue}
    if(parsed.pathname.startsWith(base)){
      const internal=parsed.pathname.slice(base.length).replace(/\/$/,'');
      hrefs.add(internal);
      if(!unique.has(internal))failures.push('Broken pilot link: '+route+' -> '+internal);
    }
  }
}
const result={sourceRoutes:manifest.sourceCount,generatedRoutes:routes.length,
  migratedReactSSR:manifest.pages.length,customReactRoutes:routes.length-manifest.pages.length,
  testedInternalLinks:hrefs.size,failures:[...new Set(failures)]};
console.log(JSON.stringify(result,null,2));
if(failures.length)process.exitCode=1;
