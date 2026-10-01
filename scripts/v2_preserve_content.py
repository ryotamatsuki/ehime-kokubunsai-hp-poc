"""Keep the fixed v1 body content in the v2 reading system and audit its mapping."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import html
import json
import posixpath
import re
import xml.etree.ElementTree as ET
import tinyhtml5
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / 'comparison/v1'
GROUPS = {
    'about':'大会について', 'events':'催しを探す', 'recruitment':'参加・募集',
    'sponsors':'協賛・応援', 'tourism':'観光・周遊', 'access':'交通・アクセス',
    'accessibility':'参加の支援', 'news':'お知らせ', 'committee':'実行委員会・資料',
    'pr':'広報・PR', 'media':'報道関係者の方へ', 'contact':'お問い合わせ',
    'archive':'記録・アーカイブ', 'common':'サイトの便利な機能',
    'policy':'利用方針', 'bids':'入札・契約',
}

def parse_file(path):
    return tinyhtml5.parse(path.read_text(encoding='utf-8'),namespace_html_elements=False)

def text(node):
    return ' '.join(''.join(node.itertext()).split())

def inventory():
    result={}
    for file in sorted(BASELINE.rglob('*.html')):
        tree=parse_file(file);main=tree.find('.//main')
        if main is None:continue
        h1=main.find('.//h1')
        rel=file.relative_to(BASELINE).as_posix()
        result[rel]={'title':text(h1),'group':rel.split('/')[0] if '/' in rel else 'home',
                     'text':text(main), 'sourceSha256':hashlib.sha256(file.read_bytes()).hexdigest()}
    return result

def norm_path(base,value):
    return posixpath.normpath(posixpath.join(posixpath.dirname(base),unquote(value)))

def render(source_rel,route,asset,canonical_to_lab,events,embedded=False):
    tree=parse_file(BASELINE/source_rel);main=tree.find('.//main')
    prefix='content-'+source_rel.replace('/','-').replace('.html','')+'-'
    parents={child:node for node in main.iter() for child in node}
    ids={node.get('id'):prefix+node.get('id') for node in main.iter() if node.get('id')}
    main_id=ids.get(main.get('id'),prefix+'body')
    by_title={e['title']:e for e in events if e.get('legacy')}
    for index,node in enumerate(list(main.iter())):
        attrs=node.attrib
        if node.get('id'):attrs['id']=ids[node.get('id')]
        for name in ['for','aria-controls','aria-labelledby','aria-describedby']:
            if attrs.get(name):attrs[name]=' '.join(ids.get(x,x) for x in attrs[name].split())
        if embedded and node.tag=='h1':node.tag='h2'
        if node.tag in ['input','select','textarea']:
            if not node.get('id'):attrs['id']=prefix+'field-'+str(index)
            parent=parents.get(node)
            while parent is not None and parent.tag!='label':parent=parents.get(parent)
            if parent is not None:parent.set('for',attrs['id'])
        if node.tag=='form':
            attrs['data-local-demo-form']='';attrs['action']='#';attrs['method']='dialog'
            for button in node.iter('button'):
                if button.get('type','submit')=='submit':button.set('disabled','');button.set('data-local-demo-submit','')
        if node.tag=='img' and node.get('src'):
            url=urlsplit(node.get('src'))
            if not url.scheme and not url.netloc:
                original=norm_path(source_rel,url.path);file=ROOT/original
                if file.exists():
                    with Image.open(file) as image:w,h=image.size
                    attrs.update({'width':str(w),'height':str(h),'loading':'lazy','decoding':'async'})
                    if file.suffix.lower() in ['.jpg','.png']:
                        stem=file.stem+'-'+file.suffix.lower().lstrip('.')
                        attrs['src']=asset('assets/legacy/'+stem+'-960.webp')
                        attrs['srcset']=', '.join(asset('assets/legacy/'+stem+'-'+str(size)+'.webp')+' '+str(size)+'w' for size in [480,960,1440])
                        attrs['sizes']='(max-width: 700px) 100vw, 50vw'
                    else:attrs['src']=asset('../'+original)
        if node.tag=='a' and node.get('href'):
            url=urlsplit(node.get('href'))
            if not url.scheme and not url.netloc:
                target=norm_path(source_rel,url.path) if url.path else source_rel
                if target in canonical_to_lab:
                    fragment=''
                    if url.fragment:
                        fragment='#'+(ids.get(url.fragment,url.fragment) if target==source_rel else url.fragment)
                    attrs['href']=route(canonical_to_lab[target])+('?' + url.query if url.query else '')+fragment
                elif target=='homepage_structure_document.html':
                    attrs['href']=asset('../homepage_structure_document.html')
        if 'data-event-card' in attrs:
            attrs.pop('data-event-card');attrs['data-legacy-event-card']=''
            title=node.find('.//h3');event=by_title.get(text(title))
            if event:
                attrs['data-id']=event['id']
                figure=ET.Element('figure',{'class':'legacy-event-image'})
                image=ET.SubElement(figure,'img',{'src':asset('assets/art/'+event['image']+'-480.webp'),
                    'srcset':', '.join(asset('assets/art/'+event['image']+'-'+str(size)+'.webp')+' '+str(size)+'w' for size in [480,960,1440]),
                    'sizes':'(max-width: 700px) 100vw, 30vw','width':'1536','height':'1024',
                    'alt':event['imageAlt'],'loading':'lazy','decoding':'async'})
                ET.SubElement(figure,'figcaption').text='AI生成イメージ'
                node.insert(0,figure)
                for anchor in node.iter('a'):anchor.set('href',route(event['page']))
        if 'data-filter-list' in attrs:attrs.pop('data-filter-list');attrs['data-legacy-filter']=''
        if node.tag=='section' and 'home-hero' in node.get('class','').split():
            attrs['style']='--hero-image:url('+asset('assets/art/festival-hero-1440.webp')+')'
    # Give every retained field an explicit label, including v1's search input.
    labelled={node.get('for') for node in main.iter('label') if node.get('for')}
    for node in list(main.iter()):
        if node.tag not in ['input','select','textarea'] or node.get('id') in labelled:continue
        parent=parents.get(node)
        if parent is None:continue
        label=ET.Element('label',{'for':node.get('id')})
        label.text='サイト内検索' if 'data-search-input' in node.attrib else node.get('aria-label') or node.get('placeholder') or '入力欄'
        parent.insert(list(parent).index(node),label)
        labelled.add(node.get('id'))
    body=''.join(ET.tostring(node,encoding='unicode',method='html') for node in main)
    return ('<section class="legacy-content'+(' legacy-content--embedded' if embedded else '')+'" id="'+html.escape(main_id)+'" data-content-source="'+html.escape(source_rel)+'">'
            '<div class="container legacy-context"><p>本欄には、未確定の掲載案・表示例を含みます。大会の正式名称・会期は大会概要でご確認ください。</p>'
            '<a class="text-link" href="'+route(canonical_to_lab['about/index.html'])+'">大会概要を確認</a></div>'+body+'</section>')

def report(routes,preserved_routes,events):
    pages=inventory();records=[]
    for source,row in pages.items():
        target=preserved_routes[source]
        records.append({'source':source,'target':target,'title':row['title'],'sourceSha256':row['sourceSha256'],
                        'sourceBodyCharacters':len(row['text'])})
    event_rows=[{'title':e['title'],'dateISO':e.get('dateISO'),'city':e['city'],'genre':e['genre'],
                 'fee':e['fee'],'supports':e['supports'],'target':routes[e['page']],'image':e['image']} for e in events if e.get('legacy')]
    return {'version':'2.0.0-alpha.5','baselineCommit':'94df551e752129e45e7f21c3d38282d87c5690db',
            'policy':'All v1 main-body text remains visible in v2; changed headings, routes and image delivery preserve content. The homepage body is on the linked festival guide.',
            'pages':records,'events':event_rows}
