/* Remove retired selectors and earlier declarations superseded in the same scope. */
const fs=require('node:fs'),path=require('node:path'),csstree=require('css-tree');
const root=path.resolve(__dirname,'..'),lab=path.join(root,'design-lab'),file=path.join(lab,'experience.css');
const classes=new Set();
for(const name of fs.readdirSync(lab))if((name.endsWith('.html')&&!['review.html','compare.html'].includes(name))||name.endsWith('.js')){
 const text=fs.readFileSync(path.join(lab,name),'utf8');
 for(const m of text.matchAll(/class=["']([^"']+)["']/g))for(const c of m[1].split(/\s+/))classes.add(c);
 for(const m of text.matchAll(/['"]([a-zA-Z][\w-]*)['"]/g))classes.add(m[1]);
}
const raw=fs.readFileSync(file,'utf8'),ast=csstree.parse(raw),seen=new Map();let removedRules=0,removedDeclarations=0;
function removeNode(list,node){for(let item=list.head;item;item=item.next)if(item.data===node){list.remove(item);return;}}
function scope(list,key){
 const items=list.toArray().reverse();
 for(const node of items){
  if(node.type==='Atrule'&&node.block&&node.block.children){if(node.name==='media')scope(node.block.children,key+'|'+csstree.generate(node.prelude));continue;}
  if(node.type!=='Rule'||node.prelude.type!=='SelectorList')continue;
  node.prelude.children.forEach((selector,item,selectors)=>{
   let needed=true;csstree.walk(selector,n=>{if(n.type==='ClassSelector'&&!classes.has(n.name))needed=false;});
   if(!needed)selectors.remove(item);
  });
  if(node.prelude.children.isEmpty){removeNode(list,node);removedRules++;continue;}
  const selector=csstree.generate(node.prelude),id=key+'|'+selector;
  let declared=seen.get(id);if(!declared)seen.set(id,declared=new Set());
  const declarations=node.block.children.toArray().reverse();
  for(const d of declarations){if(d.type!=='Declaration')continue;const property=d.property+'|'+!!d.important;
   if(declared.has(property)){removeNode(node.block.children,d);removedDeclarations++;}
   else declared.add(property);
  }
 }
}
scope(ast.children,'root');const output=csstree.generate(ast)+'\n';fs.writeFileSync(file,output);
process.stdout.write(JSON.stringify({beforeBytes:Buffer.byteLength(raw),afterBytes:Buffer.byteLength(output),removedRules,removedDeclarations})+'\n');
