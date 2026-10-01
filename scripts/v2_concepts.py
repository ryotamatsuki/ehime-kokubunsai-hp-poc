"""D2 reset: two different page grammars, rather than two color variations."""
from urllib.parse import urlencode

SIGN = '<svg class="festival-sign" viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="22" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 28h40M28 8v40M13 13l30 30M13 43l30-30" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="28" cy="28" r="7" fill="currentColor"/></svg>'
CONTOURS = '<svg class="atlas-contours" viewBox="0 0 1300 500" preserveAspectRatio="none" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1"><path d="M0 220C100 40 250 70 360 165S590 360 770 215 1030 60 1300 140"/><path d="M0 250C120 70 260 105 360 195S600 390 780 245 1050 90 1300 170"/><path d="M0 280C110 120 240 140 350 225S610 420 790 275 1080 120 1300 200"/><path d="M0 310C115 145 255 175 350 255S620 455 800 305 1100 150 1300 230"/><path d="M30 450C140 240 200 380 320 390S490 320 620 455"/><path d="M55 480C165 265 225 405 345 415S515 345 645 480"/></g></svg>'


def frame(main, direction, arrow, menu):
    home = "home-b.html" if direction == "poster" else "home-a.html"
    mode = "paper" if direction == "poster" else "sea"
    return f'''<a class="skip" href="#main">本文へ移動</a>
<div class="concept-note">デザイン試作／名称・会期・催しは未確定。写真はイメージです。</div>
<header class="c-header c-header--{mode}"><div class="c-header-inner">
<a class="c-brand brand" href="{home}" aria-label="愛媛大会（仮） トップ">{SIGN}<span><strong>EHIME <b>2028</b></strong><small>国民文化祭・全国障害者芸術・文化祭</small></span></a>
<a class="c-mini-search" href="event-search.html" aria-label="イベントを探す"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10" cy="10" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="m15 15 6 6" fill="none" stroke="currentColor" stroke-width="2"/></svg>探す</a>
<button class="menu-toggle c-menu" data-menu-toggle hidden type="button" aria-expanded="false" aria-controls="main-navigation">{menu}<span data-menu-label>メニュー</span></button>
<nav id="main-navigation" class="c-nav" data-main-nav aria-label="メインナビゲーション"><a href="#about">大会について</a><a href="#join">参加・募集</a><a href="event-detail.html#support">参加の支援</a><a href="#news">重要情報・お知らせ</a><a href="event-search.html" class="c-search">イベントを探す {arrow}</a></nav></div><a class="c-urgent" href="#news"><strong>重要なお知らせ</strong><span>変更・中止などの情報を見る {arrow}</span></a></header>
{main}
<footer class="c-footer"><div class="c-footer-top"><p>愛媛大会（仮）<br><span>令和10年度 愛媛県開催予定／名称・会期は未定</span></p><nav aria-label="フッターナビゲーション"><a href="event-search.html">イベント</a><a href="documents.html">実行委員会・資料</a><a href="event-detail.html#support">バリアフリー</a><a href="event-detail.html#contact">問い合わせ</a></nav></div><p class="c-footer-word" aria-hidden="true">EHIME 2028.</p><p class="c-footer-note">掲載する催し・募集・参加支援はサンプルです。正式情報は決定後に掲載します。</p></footer>'''


def information(arrow, poster=False):
    cls = "poster-information" if poster else "atlas-information"
    return f'''<section class="{cls}" id="news"><div class="info-title"><p class="c-kicker">INFORMATION</p><h2>大切な<br>お知らせ。</h2><p>変更・中止などの重要情報は<br>ここからご案内します。</p></div><div class="info-rows"><a href="documents.html"><span>準備中</span><strong>大会の準備・実行委員会の資料</strong>{arrow}</a><a href="documents.html#participation"><span>募集案内</span><strong>出演・出展・ボランティア・協賛</strong>{arrow}</a><a href="event-detail.html#support"><span>参加支援</span><strong>安心して楽しむための情報</strong>{arrow}</a></div></section>'''


def build_homes(page, photo, events, arrow, menu):
    craft = events[1]
    # Each cultural entry remains a normal link if JavaScript is unavailable.
    lines = []
    names = [("craft", "手を動かす。", "工芸", "土に触れ、形をつくる。"),
             ("stage", "音に出会う。", "舞台", "土地の表現を、ともに楽しむ。"),
             ("literature", "言葉を歩く。", "文学", "まちの風景を、自分の言葉に。"),
             ("food", "味を分かち合う。", "食文化", "土地の味と、それを伝える人へ。")]
    for number, (eid, title, genre, desc) in enumerate(names, 1):
        event = next(e for e in events if e["id"] == eid)
        href = "event-search.html?" + urlencode({"genre": genre})
        lines.append(f'<a class="culture-line" href="{href}"><span class="culture-number">0{number}</span><span class="culture-word">{title}<small>{desc}</small></span><span class="culture-kind">{genre}</span><figure>{photo(event["image"], "", "(max-width: 759px) 22vw, 15vw")}</figure>{arrow}</a>')
    choices = ''.join(f'<button type="button" data-culture="{eid}" aria-pressed="{str(eid=="craft").lower()}" aria-controls="culture-preview"><span>0{i}</span>{genre}</button>' for i, (eid, _, genre, _) in enumerate(names, 1))
    a = f'''<main id="main" class="concept-a">
<section class="atlas" aria-labelledby="home-title">
<div class="atlas-heading"><p class="c-kicker">EHIME / A CULTURE ARCHIPELAGO</p><h1 id="home-title"><small>愛媛、</small>文化の群島。</h1><p class="atlas-lead">ひとつじゃない。だから、出会いに行こう。<br>海も、山も、まちも。表現でつながる文化の祭典へ。</p></div>
<div class="atlas-canvas">{CONTOURS}<p class="atlas-coordinate" aria-hidden="true">CRAFT / STAGE / WORDS / FOOD</p>
<figure class="atlas-island atlas-island--main">{photo(craft["image"],craft["alt"],"(max-width: 759px) 84vw, 52vw",True, 'data-culture-photo')}<figcaption><span data-culture-label>01 / 工芸</span><span>写真はイメージ</span></figcaption></figure>
<figure class="atlas-island atlas-island--stage" aria-hidden="true">{photo("event-stage-lanterns","","(max-width: 759px) 28vw, 18vw")}<figcaption>STAGE</figcaption></figure>
<figure class="atlas-island atlas-island--words" aria-hidden="true">{photo("uchiko-ozu-townscape","","(max-width: 759px) 33vw, 22vw")}<figcaption>WORDS</figcaption></figure>
<figure class="atlas-island atlas-island--people" aria-hidden="true">{photo("inclusive-art-gallery","","(max-width: 759px) 31vw, 21vw")}<figcaption>PEOPLE</figcaption></figure>
<div class="atlas-orbit" aria-hidden="true">{SIGN}<span>文化は、<br>つながっている。</span></div></div>
<div class="atlas-selector" data-js-only hidden><p>気になる文化を選ぶ</p><div class="culture-buttons" aria-label="文化の種類">{choices}</div></div>
<div class="atlas-preview" id="culture-preview"><div><p class="c-kicker">YOUR FIRST ENCOUNTER</p><h2 data-culture-title>手を動かす。<br>会話が生まれる。</h2></div><div class="atlas-preview-copy"><p data-culture-description>土に触れ、自分の手で形をつくる。工芸を入り口に、人と土地の物語に出会います。</p><a class="c-action" data-culture-search href="event-search.html?genre=工芸">工芸の催しを探す {arrow}</a><a class="c-secondary" data-culture-detail href="event-detail.html?id=craft">催しの掲載例を見る {arrow}</a></div></div><p class="sr-only" data-culture-announcement role="status" aria-live="polite"></p>
<div class="atlas-bottom"><span>令和10年度 愛媛県開催予定／名称・会期は未定</span><a href="event-detail.html#support">参加の支援を確認 {arrow}</a><a href="documents.html">資料を読む {arrow}</a></div>
</section>
<section class="journey" id="about"><div class="journey-intro"><p class="c-kicker">01 / CULTURE IS EVERYWHERE</p><h2>文化は、<br>暮らしの中にある。</h2><p>手しごと。まちの言葉。海辺の舞台。<br>誰かの日常が、誰かの新しい出会いになる。<br>国民文化祭・全国障害者芸術・文化祭が、<br>愛媛のさまざまな表現をつなぎます。</p></div><div class="journey-scene"><figure>{photo("uchiko-ozu-townscape","歴史的なまちなみを歩く人々のイメージ","(max-width: 759px) 100vw, 100vw")}</figure><div class="journey-caption"><span>WORDS & PLACE</span><h3>いつものまちに、<br>まだ知らない物語。</h3><a href="event-search.html?genre=文学">文学の催しを探す {arrow}</a></div></div></section>
<section class="culture-directory"><div class="directory-heading"><p class="c-kicker">02 / FIND YOUR CULTURE</p><h2>どの入口から、<br>出会いますか。</h2><p>以下の催しは掲載方法を示すサンプルです。</p></div><div class="culture-lines">{''.join(lines)}</div></section>
<section class="atlas-together" id="join"><p class="c-kicker">03 / EVERY EXPRESSION COUNTS</p><h2>あなたの表現も、<br>この群島のひとつ。</h2><div class="together-bottom"><p>観る人も、つくる人も、支える人も。<br>障害のある人もない人も、ともに楽しむ大会へ。<br>募集と参加支援は、正式決定後にご案内します。</p><div><a class="c-action" href="documents.html#participation">参加・募集の案内 {arrow}</a><a class="c-secondary" href="event-detail.html#support">バリアフリー・参加の支援 {arrow}</a></div></div><span class="together-word" aria-hidden="true">+ YOU.</span></section>
{information(arrow)}
</main>'''
    page("home-a.html", "愛媛、文化の群島。", frame(a,"editorial",arrow,menu), lab=True)
    b = f'''<main id="main" class="concept-b">
<section class="billboard" aria-labelledby="home-title"><div class="billboard-meta"><p class="c-kicker">EHIME CULTURE FESTIVAL / 2028</p><span>令和10年度 愛媛県開催予定</span></div><div class="billboard-title"><h1 id="home-title">文化を、<br><span>持ちよろう。</span></h1><div class="billboard-emblem" aria-hidden="true">{SIGN}<span>ALL<br>OF US.</span></div></div>
<p class="billboard-lead">観る。つくる。ともに楽しむ。<br>一人ひとりの「好き」が、愛媛をひらく。</p>
<div class="intent-tabs" data-js-only hidden aria-label="参加の入口"><button type="button" data-intent="watch" aria-pressed="true" aria-controls="intent-preview"><span>01 / DISCOVER</span><strong>観る<span aria-hidden="true">↗</span></strong><small>イベントを探す</small></button><button type="button" data-intent="make" aria-pressed="false" aria-controls="intent-preview"><span>02 / CREATE</span><strong>つくる<span aria-hidden="true">↗</span></strong><small>出演・出展・参加</small></button><button type="button" data-intent="together" aria-pressed="false" aria-controls="intent-preview"><span>03 / TOGETHER</span><strong>ともに<span aria-hidden="true">↗</span></strong><small>安心して楽しむ</small></button></div>
<div class="intent-preview" id="intent-preview" data-intent-panel="watch"><div class="intent-copy"><p class="c-kicker" data-intent-kicker>01 / DISCOVER</p><h2 data-intent-title>その「観たい」が、<br>旅のはじまり。</h2><p data-intent-description>舞台、工芸、文学、食文化。気になる表現から、あなたの体験を探してください。</p><a class="poster-action" data-intent-link href="event-search.html?direction=poster">イベントを探す {arrow}</a></div><div class="intent-art"><figure class="intent-main-photo">{photo("event-stage-lanterns",events[0]["alt"],"(max-width: 759px) 88vw, 44vw",True,'data-intent-photo')}</figure><div class="intent-stamp" aria-hidden="true"><span data-intent-word>観る</span></div><figure class="intent-small-photo" aria-hidden="true">{photo("family-culture-workshop","","(max-width: 759px) 36vw, 19vw")}</figure><p>写真はイメージ</p></div></div><p class="sr-only" role="status" aria-live="polite" data-intent-announcement></p><div class="billboard-footer"><span>国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）</span><span>名称・会期・募集の内容は未定</span></div></section>
<section class="poster-manifesto" id="about"><p class="c-kicker">CULTURE IS OPEN TO EVERYONE.</p><h2>文化に、<br>正解はひとつじゃない。</h2><div class="poster-manifesto-bottom"><p>上手にできるかより、やってみたいか。<br>知っているかより、出会ってみたいか。<br>それぞれの表現を持ち寄る文化の祭典を、愛媛で。</p><span class="poster-cross" aria-hidden="true">＋</span><p>国民文化祭と全国障害者芸術・文化祭。<br>障害のある人もない人も、<br>ともに表現を楽しむ場をつくります。</p></div></section>
<section class="poster-paths" id="join"><div class="poster-path-heading"><p class="c-kicker">CHOOSE YOUR WAY.</p><h2>参加のしかたも、<br>ひとつじゃない。</h2></div><a class="poster-path" href="event-search.html?direction=poster"><span>01</span><h3>観たい。</h3><p>市町・ジャンル・参加支援から<br>気になる催しを探す。</p>{arrow}</a><a class="poster-path" href="documents.html?direction=poster#participation"><span>02</span><h3>やってみたい。</h3><p>出演・出展・ボランティア・協賛。<br>募集内容と時期は正式決定後に掲載。</p>{arrow}</a><a class="poster-path" href="event-detail.html?direction=poster#support"><span>03</span><h3>一緒に楽しみたい。</h3><p>会場や情報のバリアフリー、<br>参加に必要な支援を確認する。</p>{arrow}</a></section>
<section class="poster-inclusion"><div class="poster-inclusion-word" aria-hidden="true">みんなの<br>ぶんか。</div><figure>{photo("inclusive-art-gallery","作品を囲み、芸術を楽しむ人々のイメージ","(max-width: 759px) 92vw, 52vw")}</figure><div class="poster-inclusion-copy"><p class="c-kicker">NO ONE IS JUST AN AUDIENCE.</p><h2>観る人も、<br>文化の担い手。</h2><a href="event-detail.html?direction=poster#support">参加の支援を確認する {arrow}</a><p>写真・対応内容は表示のイメージです。</p></div></section>
{information(arrow, True)}
</main>'''
    page("home-b.html", "文化を、持ちよろう。", frame(b,"poster",arrow,menu), "poster", lab=True)


def build_index(page, arrow):
    main = f'''<a class="skip" href="#main">本文へ移動</a><header class="reset-header"><p class="c-kicker">V2 / D2 CONCEPT RESET / ALPHA.3</p><h1>画面の構成から、<br>つくり直す。</h1><p>旧A・B案を置き換えた、新しい2つの方向です。<br>文化を巡る入口と、参加のしかたを選ぶ入口を比べます。</p></header><main id="main"><section class="reset-options"><article class="reset-option reset-option--a"><span>A / CULTURE ARCHIPELAGO</span><h2>文化の群島。</h2><p>濃い海の色、群島のような写真、文化を選ぶ操作。<br>写真を鑑賞して終わらず、気になるジャンルの催しへ進みます。</p><div class="reset-preview reset-preview--a" aria-hidden="true"><span>文化の群島。</span><i></i><b>01 / CRAFT</b></div><a href="home-a.html">新A案を開く {arrow}</a></article><article class="reset-option reset-option--b"><span>B / PARTICIPATORY POSTER</span><h2>文化を、持ちよろう。</h2><p>青、黄、朱色と大胆な文字。<br>「観る・つくる・ともに」を選ぶと、写真・言葉・行き先が変わります。</p><div class="reset-preview reset-preview--b" aria-hidden="true"><span>文化を、<br>持ちよろう。</span><b>観る ／ つくる ／ ともに</b></div><a href="home-b.html">新B案を開く {arrow}</a></article></section><section class="reset-review"><h2>今回は、ここを比べます。</h2><ol><li>最初の画面で、旧v1と違う大会の顔になっているか。</li><li>写真や文字の大きさだけでなく、探す・参加する体験が変わったか。</li><li>下へ進んでも、同じカード一覧の繰り返しになっていないか。</li><li>スマートフォンでも、表現と情報の探しやすさが両立しているか。</li></ol><p>方向は未選定です。旧案への暫定推奨は撤回しました。<br>以下の下層ページは共通部品の試作であり、トップと同じ深さの再設計は後続工程で行います。</p><nav aria-label="共通部品の試作"><a href="event-search.html">検索 {arrow}</a><a href="event-detail.html">詳細 {arrow}</a><a href="documents.html">資料 {arrow}</a><a href="components.html">部品 {arrow}</a></nav></section></main>'''
    page("index.html", "v2構成からの再設計", main, lab=True)
