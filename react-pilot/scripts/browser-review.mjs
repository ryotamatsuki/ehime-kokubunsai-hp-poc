import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, stat, mkdir, writeFile } from 'node:fs/promises';
import { resolve, extname, join, normalize } from 'node:path';

const repoRoot = resolve(import.meta.dirname, '../..');
const pilotRoot = resolve(repoRoot, 'react-pilot/dist');
const out = resolve(repoRoot, 'react-pilot/browser-review');
await mkdir(out, { recursive: true });
const prefix = '/ehime-kokubunsai-hp-poc/';
const mime = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8',
  '.css':'text/css; charset=utf-8','.json':'application/json','.png':'image/png',
  '.jpg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2','.svg':'image/svg+xml',
  '.ico':'image/x-icon','.txt':'text/plain; charset=utf-8'};
function getFile(pathname) {
  let p = decodeURIComponent(pathname).replace(/^\/+/, '');
  if (p.startsWith('ehime-kokubunsai-hp-poc/')) p=p.slice(prefix.length-1);
  let root=repoRoot;
  if (p.startsWith('react-pilot/')) {root=pilotRoot;p=p.slice('react-pilot/'.length)}
  if (p.endsWith('/')) p+='index.html';
  if (!extname(p)) p+='/index.html';
  const file=resolve(root,p);
  return file.startsWith(root+'/') ? file : null;
}
const server=createServer(async(req,res)=>{
  try {
    const file=getFile(new URL(req.url,'http://127.0.0.1').pathname);
    if (!file) {res.writeHead(403);res.end();return}
    const s=await stat(file);
    if (!s.isFile()) throw new Error('not file');
    res.writeHead(200,{'Content-Type':mime[extname(file)]||'application/octet-stream','Content-Length':s.size});
    res.end(await readFile(file));
  } catch(e) {res.writeHead(404);res.end('missing resource')}
});
await new Promise(resolve=>server.listen(8787,'127.0.0.1',resolve));
const base='http://127.0.0.1:8787'+prefix.replace(/\/$/,'');
const errors=[];
const pages=[
  ['home','/','/react-pilot/'],
  ['event-search','/events/search.html','/react-pilot/events/'],
  ['event-detail','/events/stage.html','/react-pilot/events/stage/']
];
const viewports=[{width:1440,height:900},{width:390,height:844},{width:320,height:720}];
let browser;
try {
  browser=await chromium.launch({headless:true,args:['--no-sandbox']});
  const results=[];
  for(const vp of viewports) {
    const context=await browser.newContext({viewport:vp,deviceScaleFactor:1,reducedMotion:'reduce'});
    await context.route('https://ryotamatsuki.github.io/ehime-kokubunsai-hp-poc/**',async route=>{
      const u=new URL(route.request().url);
      const pathname=u.pathname;
      const local=getFile(pathname);
      try{
        if (!local) throw new Error('not local');
        await route.fulfill({status:200,contentType:mime[extname(local)]||'application/octet-stream',body:await readFile(local)});
      }catch(e){await route.abort()}
    });
    for(const [name,v2Path,pilotPath] of pages) {
      for(const [version,pathname] of [['v2',v2Path],['react',pilotPath]]) {
        const page=await context.newPage();
        const failures=[];
        page.on('pageerror',err=>failures.push(err.message));
        const response=await page.goto(base+pathname,{waitUntil:'networkidle',timeout:45000});
        await page.evaluate(()=>document.fonts.ready);
        await page.screenshot({path:join(out,name+'-'+version+'-'+vp.width+'.png'),fullPage:true,animations:'disabled'});
        const stats=await page.evaluate(()=>({
          title:document.title,h1:document.querySelector('h1')?.innerText||'',
          docWidth:document.documentElement.scrollWidth,viewportWidth:window.innerWidth,
          bodyHeight:document.body.scrollHeight,images:[...document.images].length,
          brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src')).slice(0,10),
          activeFocusable:document.querySelectorAll('a[href],button:not([disabled]),input,select').length
        }));
        results.push({name,version,viewport:vp.width,http:response?.status(),...stats,jsErrors:failures});
        await page.close();
      }
    }
    if(vp.width===390) {
      const page=await context.newPage();
      await page.goto(base+'/react-pilot/events/',{waitUntil:'networkidle'});
      const input=page.getByLabel('キーワード');
      await input.fill('砥部');
      const filtered=await page.locator('.event-card').count();
      const countText=await page.getByRole('status').allTextContents();
      results.push({name:'interaction-filter',version:'react',viewport:390,filtered,countText});
      await page.getByLabel('キーワード').fill('存在しない催し名');
      results.push({name:'interaction-empty',version:'react',viewport:390,empty:await page.getByText('該当する催しはありません。').isVisible()});
      await page.close();
    }
    await context.close();
  }
  await writeFile(join(out,'report.json'),JSON.stringify(results,null,2));
  console.log('BROWSER_REVIEW_REPORT_BEGIN');
  console.log(JSON.stringify(results,null,2));
  console.log('BROWSER_REVIEW_REPORT_END');
  const fatal=results.filter(r=>r.http && (r.http!==200||r.docWidth>r.viewportWidth||r.jsErrors.length));
  if(fatal.length) {console.error('Browser review found failures:',JSON.stringify(fatal));process.exitCode=1}
} finally {if(browser) await browser.close();await new Promise(resolve=>server.close(resolve))}
