"""Verify complete visible v1 content, event details, imagery and frozen snapshot."""
from pathlib import Path
import hashlib,json,re
import tinyhtml5
from fontTools.ttLib import TTFont
import v2_preserve_content as preservation
ROOT=Path(__file__).resolve().parents[1];LAB=ROOT/'design-lab'

def main():
    inventory=json.loads((ROOT/'docs/V2_CONTENT_INVENTORY.json').read_text())
    baseline=json.loads((ROOT/'comparison/v1-manifest.json').read_text())
    data=json.loads((LAB/'content.json').read_text());pages=[];issues=[]
    for item in baseline['files']:
        file=ROOT/'comparison/v1'/item['path'];raw=file.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if actual!=item['git_blob_sha1']:issues.append('changed v1 snapshot: '+item['path'])
    for row in inventory['pages']:
        source=preservation.parse_file(ROOT/'comparison/v1'/row['source']).find('.//main')
        target=preservation.parse_file(ROOT/row['target'])
        retained=next((n for n in target.iter() if n.get('data-content-source')==row['source']),None)
        if retained is None:issues.append('missing retained content: '+row['source']);continue
        rendered=preservation.text(retained)
        chunks=[' '.join(chunk.split()) for chunk in source.itertext() if chunk.strip()]
        missing=[chunk for chunk in chunks if chunk not in rendered]
        if missing:issues.append('omitted content: '+row['source']+' '+str(missing[:3]))
        hidden=[n for n in retained.iter() if n.get('hidden') is not None and n.tag not in ['button']]
        # Filter empty states are progressively controlled; actual content is visible.
        hidden=[n for n in hidden if 'data-filter-empty' not in n.attrib]
        if hidden:issues.append('hidden retained information: '+row['source'])
        pages.append({'source':row['source'],'target':row['target'],'sourceTextChunks':len(chunks),
                      'retainedTextChunks':len(chunks)-len(missing),'status':'PASS' if not missing else 'FAIL'})
    expected={
        '瀬戸内文化ステージ（仮）':('2028-08-12','松山市','舞台','無料','手話通訳'),
        '砥部焼とことばの工房（仮）':('2028-08-18','砥部町','工芸','要申込','親子向け'),
        '宇和海の食文化交流（仮）':('2028-09-02','宇和島市','食文化','有料','車椅子席'),
        '俳句とまち歩き（仮）':('2028-09-09','松山市','文学','無料','やさしい日本語'),
    }
    events=[]
    for title,(date,city,genre,fee,support) in expected.items():
        event=next((e for e in data['events'] if e['title']==title),None)
        good=event is not None and event['dateISO']==date and event['city']==city and event['genre']==genre and fee in event['fee'] and support in event['supports']
        if not good:issues.append('v1 event changed or missing: '+title)
        events.append({'title':title,'status':'PASS' if good else 'FAIL'})
    generated=json.loads((LAB/'assets/event-image-prompts.json').read_text())
    known={r['id']:r for r in generated['images']}
    for event in data['events']:
        image=known.get(event['image'])
        if image is None:issues.append('no generated master: '+event['id']);continue
        page=(LAB/event['page']).read_text()
        if 'assets/art/'+event['image']+'-960.webp' not in page:issues.append('missing detail image: '+event['id'])
        if not all((LAB/'assets/art'/f"{event['image']}-{width}.webp").is_file() for width in [480,960,1440]):issues.append('missing delivery image: '+event['id'])
        master=ROOT/image['master']
        if hashlib.sha256(master.read_bytes()).hexdigest()!=image['sha256']:issues.append('generated master hash: '+event['id'])
    home=(LAB/'index.html').read_text()
    if 'assets/art/festival-hero-960.webp' not in home:issues.append('festival-wide hero absent')
    if 'porcelain-hero' in home:issues.append('craft still dominates homepage hero')
    if not (LAB/'compare.html').exists():issues.append('comparison viewer absent')
    manifest=json.loads((LAB/'experience-manifest.json').read_text())
    characters=set()
    for filename in manifest['pages']:
        body=preservation.parse_file(LAB/filename).find('.//body')
        characters.update(ord(c) for c in ''.join(body.itertext()) if '\u3000'<=c<='\u9fff')
    font_coverage=[]
    for name in ['ehime-sans-regular.woff2','ehime-sans-bold.woff2']:
        missing=characters-set(TTFont(LAB/'assets/fonts'/name).getBestCmap())
        font_coverage.append({'font':name,'japaneseCharacters':len(characters),'missingCharacters':len(missing)})
        if missing:issues.append('missing font characters: '+name+' '+''.join(chr(c) for c in sorted(missing)))
    report={'version':data['version'],'status':'FAIL' if issues else 'PASS','method':'all visible source text chunks, source hashes, v1 event fields and generated asset linkage',
            'v1SnapshotFiles':len(baseline['files']),'v1SitePages':len(pages),'preservedTextChunks':sum(p['retainedTextChunks'] for p in pages),
            'sourceTextChunks':sum(p['sourceTextChunks'] for p in pages),'v1Events':events,'allEvents':len(data['events']),
            'generatedImages':len(generated['images']),'japaneseFontCoverage':font_coverage,'pages':pages,'issues':issues}
    (LAB/'qa/content-preservation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['pages','v1Events']},ensure_ascii=False))
    if issues:raise SystemExit(1)
if __name__=='__main__':main()
