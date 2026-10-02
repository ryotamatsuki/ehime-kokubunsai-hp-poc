"""Source-based cultural reading, observations and a kana composition workshop."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / 'design-lab'
PHOTOS = {p['id']: p for p in json.loads((LAB/'assets/culture-sources.json').read_text())['images']}

FIELDS = [
    dict(id='niihama',region='東予',place='新居浜市',word='響き',title='担ぐのは、地域の記憶。',
         subject='新居浜太鼓祭り',date='1818–1830',dateLabel='文政年間の記録に「神輿太鼓」',
         lead='金糸の飾り、その下には、地域でつないできた時間がある。',
         paragraphs=['新居浜市の歴史解説は、太鼓台の記録が文政年間に現れることを紹介しています。起源の時期は、確かな資料では分かっていません。','瀬戸内の港町に太鼓台が広がった背景には、海上交通による物資と文化の交流があると考えられています。別子銅山による産業の発展と、飾りや大きさの変化も結び付いています。'],
         observation='金糸の輪郭と、担ぐ人々の並び。ひとつの飾りと、集団の動きの両方を見てみる。',
         photoNote='新居浜太鼓祭りの記録写真。2016年10月20日撮影。',
         source='https://www.city.niihama.lg.jp/soshiki/kankou/taikodairekishi.html',sourceLabel='新居浜市「太鼓台の歴史概説」',
         connection='舞台の催しを見る',page='event-search.html',suffix='?genre=舞台'),
    dict(id='matsuyama',region='中予',place='松山市',word='ことば',title='まちの途中に、十七音。',
         subject='俳都松山俳句ポスト',date='1968',dateLabel='松山城長者ヶ平に第1号を設置',
         lead='文学は、記念館の中だけにあるのではない。路面電車にも、ことばの入口がある。',
         paragraphs=['松山市は1968年、松山城長者ヶ平に第1号の俳句ポストを設けました。市の2026年8月の発表では、市内82か所に設置されています。','路面電車やフェリーにも置かれる俳句ポスト。移動の途中で感じた景色を、自分のことばで残す仕組みが、日々の暮らしと俳句をつないでいます。'],
         observation='窓の外の景色と、車内の小さなポスト。名所ではなく、移動の途中に目を向ける。',
         photoNote='伊予鉄道の車内にある俳句ポスト。2008年8月19日の記録写真。現在の車内設備を保証するものではありません。',
         source='https://www.city.matsuyama.ehime.jp/hodo/202608/R7nyuusennkusyuu.html',sourceLabel='松山市「令和7年度 俳都松山俳句ポスト入選句集」',
         connection='ことばの小さな工房へ',page='culture-literature.html',suffix='#word-workshop'),
    dict(id='uchiko',region='南予',place='内子町',word='舞台',title='舞台を残したのは、人の熱意。',
         subject='内子座',date='1916',dateLabel='町の人々が建てた芝居小屋',
         lead='客席も、花道も、舞台も。ここに集まる人のために、建物の時間が続いてきた。',
         paragraphs=['内子座は1916年、木蝋や生糸の生産で栄えた町に、芸術・芸能を愛する人々が建てた芝居小屋です。歌舞伎、人形芝居、落語、映画などの場になりました。','取り壊しの危機を町民の熱意によって越え、1985年に劇場として再出発。現在は保存修理のため休館しています。文化を受け継ぐことには、上演だけでなく、場所を守る営みも含まれます。'],
         observation='客席から舞台までの近さ、木の柱、花道。観る人と演じる人の位置関係をたどる。',
         photoNote='内子座の客席と舞台。2024年8月撮影。2024年9月から保存修理のため長期休館中。大会会場の案内ではありません。',
         source='https://www.town.uchiko.ehime.jp/site/uchikoza/132383.html',sourceLabel='内子町「内子座」',
         connection='舞台の催しを見る',page='event-search.html',suffix='?genre=舞台'),
    dict(id='uwajima',region='南予',place='宇和島市',word='祭礼',title='牛と鬼、その姿を受け継ぐ。',
         subject='牛鬼',date='1967',dateLabel='市民イベントとしての牛鬼まつり開始',
         lead='形を見て、由来を読む。ひとつの土地にも、まだ分からない歴史がある。',
         paragraphs=['宇和島市は、牛鬼を、牛に似た胴体と鬼のような顔、剣をかたどった尾を持つ練物として紹介しています。祭りでは、神輿の露払いとして地域をまわります。','うわじま牛鬼まつりは1967年に市民イベントとして始まりました。牛鬼そのものの起源は十分には解明されていません。伝承と、確かめられた記録を分けて読むことも、文化に出会う方法です。'],
         observation='顔、胴体、尾。その形の違いを、名前の「牛」と「鬼」に重ねてみる。',
         photoNote='写真は大阪の国立民族学博物館に展示された1978年製作の牛鬼。2014年1月25日撮影。宇和島での祭りの開催写真ではありません。',
         source='https://www.city.uwajima.ehime.jp/soshiki/3/mirai-kiji2026-6-12.html',sourceLabel='宇和島市「60年目のうわじま牛鬼まつり」',
         connection='宇和島の食文化へ',page='culture-food.html',suffix=''),
]

def esc(s):
    return html.escape(str(s), quote=True)

def photo(key, asset, eager=False):
    p=PHOTOS[key]
    variants={r['width']:r for r in p['deliveries']}
    return '<img src="'+asset('assets/culture/'+key+'-960.webp')+'" srcset="'+', '.join(asset(r['path'].removeprefix('design-lab/'))+' '+str(w)+'w' for w,r in variants.items())+'" sizes="(max-width:700px) 100vw, 58vw" alt="'+esc(p['title'])+'" width="'+str(p['width'])+'" height="'+str(p['height'])+'" loading="'+('eager' if eager else 'lazy')+'" decoding="async">'

def credit(key):
    p=PHOTOS[key]
    return '<span>写真：'+esc(p['author'])+' · '+esc(p['date'])+'</span> <a href="'+p['source']+'">原写真</a> · <a href="'+p['licenseUrl']+'">'+p['license']+'</a><span>表示用に縮小・WebP変換。画面に合わせてトリミング。</span>'

def atlas(route, asset, link, full=False):
    selectors=''.join('<a href="#field-'+r['id']+'" data-field-choice="'+r['id']+'"><span>'+r['region']+'</span>'+r['place']+'<small>'+r['word']+'</small></a>' for r in FIELDS)
    panels=[]
    for i,r in enumerate(FIELDS):
        paragraphs=''.join('<p>'+esc(p)+'</p>' for p in r['paragraphs']) if full else '<p>'+esc(r['paragraphs'][0])+'</p><details class="field-background"><summary>背景を、もう少し。</summary><p>'+esc(r['paragraphs'][1])+'</p></details>'
        panels.append('<article class="field-panel field-panel--'+r['id']+'" id="field-'+r['id']+'" data-field-panel="'+r['id']+'"><figure class="field-photo">'+photo(r['id'],asset)+'<figcaption>'+credit(r['id'])+'</figcaption></figure><div class="field-copy"><p class="label">'+r['subject']+' / '+r['place']+'</p><h3>'+r['title']+'</h3><p class="field-lead">'+r['lead']+'</p><div class="field-year"><strong>'+r['date']+'</strong><span>'+r['dateLabel']+'</span></div>'+paragraphs+'<details class="field-observation"><summary>写真の、どこを見よう。</summary><p>'+r['observation']+'</p><p class="small">'+r['photoNote']+'</p></details><div class="field-source"><a href="'+r['source']+'">'+r['sourceLabel']+' ↗</a><span>公開資料をもとに編集 · 2026年10月2日確認</span></div>'+link(r['connection'],r['page'],r['suffix'])+'</div></article>')
    notes='''<form class="field-note-form" data-field-note-form hidden><label for="field-observation-note">写真や背景から、あなたが気づいたこと<textarea id="field-observation-note" rows="2" maxlength="80" placeholder="気になった色、形、景色を、ひと言で。" data-field-note></textarea></label><button class="button button--primary" type="submit">ことばを文化帖に残す</button><p class="small">このブラウザー内に保存します。外部へ送信しません。</p><p class="sr-only" role="status" aria-live="polite" data-field-note-status></p></form>'''
    return '<section class="cultural-atlas'+(' cultural-atlas--full' if full else '')+'" id="discover" data-field-atlas><div class="container"><div class="section-heading"><div><p class="label">A CULTURE IS A CONNECTION.</p><h2>土地の時間に、<br>出会う。</h2></div><p>写真を見て、背景を読む。<br>東予、中予、南予の文化をたどります。</p></div><nav class="field-choices" aria-label="文化の記録を選ぶ" data-field-choices>'+selectors+'</nav><div class="field-panels">'+''.join(panels)+'</div>'+notes+('' if full else '<div class="atlas-more">'+link('文化の記録と、自分のことば','culture-atlas.html','','button button--line')+'</div>')+'<p class="field-editorial-note">実写と自治体の公開資料を使った文化紹介です。新たな現地取材・インタビューの記録ではありません。写真の文化行事と、本大会の催しの掲載例は別の情報です。</p></div></section>'

def word_workshop():
    inputs=''.join('<label for="haiku-'+str(i)+'"><span>'+str(i+1)+'句目 / '+str(n)+'音</span><input id="haiku-'+str(i)+'" data-haiku-line="'+str(i)+'" maxlength="40" value="'+v+'" autocomplete="off"><small data-haiku-count="'+str(i)+'">'+str(n)+'音</small></label>' for i,(n,v) in enumerate([(5,'あきのそら'),(7,'ことばひろって'),(5,'まちをゆく')]))
    return '''<section class="word-workshop" id="word-workshop" data-haiku-studio><div class="container word-workshop-grid"><div><p class="label">A MOMENT, IN SEVENTEEN SOUNDS.</p><h2>あなただけの、<br>十七音。</h2><p>景色から、一つの発見を。<br>ひらがな・カタカナで、五・七・五をつづります。</p><form class="haiku-form">'''+inputs+'''</form><p class="small">小さい「ゃ・ゅ・ょ」などは前の音と合わせ、「っ・ん・ー」は一音として数えます。かな以外を含むときは、読みを入力してください。音数は作例づくりの補助です。</p><div class="haiku-actions"><button type="button" class="button button--primary" data-haiku-export disabled>ことばを持ちかえる</button><button type="button" class="reset-button" data-haiku-reset disabled>作例に戻す</button></div><p class="haiku-status" role="status" aria-live="polite" data-haiku-status>五・七・五の作例です。このサイトで作成したことばで、既存の俳句の引用ではありません。</p></div><div class="haiku-paper" aria-label="ことばのプレビュー"><div class="haiku-preview" data-haiku-preview><p>あきのそら</p><p>ことばひろって</p><p>まちをゆく</p></div><div class="haiku-seventeen" aria-hidden="true">'''+''.join('<i></i>' for _ in range(17))+'''</div><p>MY EHIME / ことばの記録</p></div></div><div class="container haiku-context"><p>松山の俳句ポストは、まちで感じたことを残す入口。ここでの作例は、あなたの端末に保存する小さな体験です。</p><a href="https://www.city.matsuyama.ehime.jp/kanko/kankoguide/rekishibunka/haiku/kankohaikupost.html">実際の俳句ポストの案内へ ↗</a></div></section>'''

def field_journal():
    return '''<section class="container field-journal"><div class="section-heading"><div><p class="label">THE WORDS YOU FOUND</p><h2>土地から、見つけたことば。</h2></div></div><div data-field-journal-list></div><p data-field-journal-empty>文化の記録を読み、気づいたことを文化帖に残せます。</p><button type="button" class="button button--line" data-field-journal-export hidden>ことばの記録を持ちかえる</button><p role="status" aria-live="polite" class="sr-only" data-field-journal-status></p></section>'''
