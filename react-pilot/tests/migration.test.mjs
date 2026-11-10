import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('.',import.meta.url)),'../..');
const data=JSON.parse(readFileSync(resolve(root,'react-pilot/src/data/legacy-pages.json'),'utf8'));
test('All existing v2 routes are represented',()=>{
  assert.ok(data.sourceCount>=125, 'Full v2 page count has shrunk');
  assert.ok(data.pages.length>=118, 'Missing rendered pages');
  const keys=new Set(data.pages.map(p=>p.route));
  assert.equal(keys.size,data.pages.length,'Duplicate page routes');
  for(const p of data.pages){assert.ok(p.html.length>80,p.file+' blank');assert.ok(!/<script\b/i.test(p.html),p.file+' executable markup');}
  for(const route of ['culture/notebook','about','access/train','accessibility/information-support','committee/overview','recruitment','tourism/courses','site-map']){
    assert.ok(keys.has(route),route+' was lost');
  }
});
test('Original source remains intact',()=>{
  for(const path of ['index.html','design-lab/experience-data.js','events/search.html','culture/notebook.html'])
    assert.ok(existsSync(resolve(root,path)),path+' is missing');
});
