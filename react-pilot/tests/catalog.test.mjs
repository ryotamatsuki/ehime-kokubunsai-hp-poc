import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
const dir = resolve(fileURLToPath(new URL('.', import.meta.url)), '../..');
const raw = readFileSync(resolve(dir, 'design-lab/experience-data.js'), 'utf8');
const m = raw.match(/^window\.EHIME_V2_DATA\s*=\s*(\{[\s\S]*\})\s*;?$/);
test('Source data is parseable and original listings are preserved', () => {
  assert.ok(m, 'Format must be reviewed if upstream data changes');
  const events = JSON.parse(m[1]).events;
  assert.equal(events.length, 6);
  assert.equal(events.filter(e => e.kind === 'verified').length, 1);
  assert.equal(events.filter(e => e.kind === 'sample').length, 5);
  for (const e of events) {
    assert.ok(e.id && e.title && e.page && e.image);
    assert.ok(existsSync(resolve(dir, 'design-lab/assets/art/' + e.image + '-960.webp')), 'Missing image ' + e.image);
  }
});
test('Legacy public pages remain untouched by the pilot', () => {
  for (const path of ['index.html','events/search.html','events/detail.html','design-lab/tokens.json'])
    assert.ok(existsSync(resolve(dir, path)), 'Missing original: ' + path);
});
