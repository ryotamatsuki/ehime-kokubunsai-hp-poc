import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '../..');
const raw = readFileSync(resolve(root, 'design-lab/experience-data.js'), 'utf8').trim();
const match = raw.match(/^window\.EHIME_V2_DATA\s*=\s*(\{[\s\S]*\})\s*;?$/);
if (!match) throw new Error('Existing event catalog format has changed. Refusing to create a partial copy.');
const source = JSON.parse(match[1]);
if (!Array.isArray(source.events) || source.events.length !== 6) {
  throw new Error('Unexpected event count in original v2 data. Review the migration before rebuilding.');
}
const events = source.events.map((item) => {
  const {id, title, shortTitle, city, genre, kind, date, venue, fee,
    booking, status, description, page, image, imageAlt, supports,
    supportStatus, source: officialSource, dateNote} = item;
  if (!id || !title || !page || !['sample','verified'].includes(kind)) {
    throw new Error('Existing event record cannot be safely migrated: ' + JSON.stringify(item));
  }
  return {id,title,shortTitle,city,genre,kind,date,venue,fee,booking,
    status,description,page,image,imageAlt,supports,supportStatus,
    source:officialSource ?? '',dateNote:dateNote ?? ''};
});
const output = resolve(import.meta.dirname, '../src/data/events.json');
mkdirSync(resolve(import.meta.dirname, '../src/data'), {recursive:true});
writeFileSync(output, JSON.stringify(events, null, 2) + '\n');
console.log('Synced ' + events.length + ' events from existing v2 data; no events were invented.');
