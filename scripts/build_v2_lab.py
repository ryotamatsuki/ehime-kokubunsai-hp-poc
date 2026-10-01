#!/usr/bin/env python3
"""Build D2 prototypes without regenerating any v1 page."""
from pathlib import Path
import html
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "design-lab"
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="m16 16 5 5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
EVENTS = [
    dict(id="stage", title="瀬戸内文化ステージ（仮）", city="松山市", genre="舞台",
         support=["手話通訳"], image="event-stage-lanterns", alt="海辺の屋外ステージと、文化公演を楽しむ観客のイメージ",
         description="海辺の舞台を囲み、地域に受け継がれてきた表現に出会う催しのサンプルです。"),
    dict(id="craft", title="砥部焼とことばの工房（仮）", city="砥部町", genre="工芸",
         support=["親子向け"], image="tobe-ceramics-workshop", alt="工房で陶芸を楽しむ、多世代の参加者のイメージ",
         description="土に触れ、自分の手で形をつくる。工芸を通じて、世代を超えた会話が生まれる体験型の催しのサンプルです。"),
    dict(id="food", title="宇和海の食文化交流（仮）", city="宇和島市", genre="食文化",
         support=["車椅子席"], image="uwajima-sea-culture", alt="海辺で食文化を楽しむ人々のイメージ",
         description="土地の味わいと、それを伝える人に出会う。宇和海の食文化を楽しむ交流の催しのサンプルです。"),
    dict(id="literature", title="俳句とまち歩き（仮）", city="松山市", genre="文学",
         support=["やさしい日本語"], image="uchiko-ozu-townscape", alt="愛媛の歴史的な町並みを歩く人々のイメージ",
         description="街の景色を言葉にして、いつもと違う発見を楽しむ。文学とまち歩きをつなぐ催しのサンプルです。"),
]

def esc(value):
    return html.escape(str(value), quote=True)

def button(label, href, kind="solid"):
    return f'<a class="button button--{kind}" href="{esc(href)}">{esc(label)}{ARROW}</a>'

def photo(name, alt, sizes="(max-width: 759px) 90vw, 45vw", eager=False, attrs=""):
    with Image.open(ROOT / ("assets/" + name + ".jpg")) as source:
        width, height = source.size
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="assets/photos/{name}-960.webp" '
            f'srcset="assets/photos/{name}-480.webp 480w, assets/photos/{name}-960.webp 960w, assets/photos/{name}-1440.webp 1440w" '
            f'sizes="{esc(sizes)}" width="{width}" height="{height}" alt="{esc(alt)}" decoding="async" {loading} {attrs}>')

def header(direction="editorial"):
    home = "home-b.html" if direction == "poster" else "home-a.html"
    return f"""
<a class="skip" href="#main">本文へ移動</a>
<div class="prototype-note">デザイン検討用の仮ページです。大会名称、会期、催しの内容は未確定です。</div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="{home}" aria-label="愛媛大会（仮） トップページ">
      <img src="../assets/brand-mark.svg" alt="" width="37" height="37">
      <span><strong>愛媛大会（仮）</strong><small>国民文化祭・全国障害者芸術・文化祭</small></span>
    </a>
    <button class="menu-toggle" type="button" data-menu-toggle hidden aria-controls="main-navigation" aria-expanded="false">{MENU}<span data-menu-label>メニュー</span></button>
    <nav class="main-nav" id="main-navigation" aria-label="メインナビゲーション" data-main-nav>
      <a href="{home}#about">大会について</a><a href="{home}#join">参加・募集</a><a href="event-detail.html#support">バリアフリー</a><a href="documents.html">実行委員会・資料</a>
      <a class="nav-search" href="event-search.html">{SEARCH}イベントを探す</a>
    </nav>
  </div>
</header>
<aside class="notice" aria-label="重要なお知らせ">
  <div class="wrap"><strong>重要なお知らせ</strong><span class="notice-text">変更・中止などの情報は、ここでご案内します。</span><a href="{home}#news">お知らせを見る</a></div>
</aside>"""

def footer(direction="editorial"):
    home = "home-b.html" if direction == "poster" else "home-a.html"
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top"><div><p class="eyebrow">EHIME CULTURE FESTIVAL</p><p style="font-size:22px;font-weight:700;margin-top:9px">愛媛大会（仮）</p><p class="small" style="margin-top:9px">国民文化祭・全国障害者芸術・文化祭</p></div>
      <nav class="footer-links" aria-label="フッターナビゲーション"><a href="{home}#about">大会について</a><a href="event-search.html">イベント</a><a href="event-detail.html#support">バリアフリー</a><a href="documents.html">資料</a><a href="event-detail.html#contact">問い合わせ</a></nav>
    </div>
    <div class="footer-bottom"><p>掲載情報はサンプルです。写真は大会や会場を表すイメージです。</p><p class="eyebrow">CULTURE CONNECTS US.</p></div>
  </div>
</footer>"""

def page(filename, title, main, direction="editorial", lab=False):
    head = f"""<!doctype html>
<html lang="ja" data-direction="{direction}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | 愛媛大会（仮）</title>
<meta name="description" content="令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）のデザイン検討用ページです。">
<meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#173b35">
<script>document.documentElement.classList.add('js');if(new URLSearchParams(window.__INITIAL_QUERY__ || location.search).get('direction')==='poster') document.documentElement.dataset.direction='poster';</script>
<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="theme.css">
<script src="events-data.js" defer></script><script src="ui.js" defer></script>
</head><body>"""
    content = head + ("" if lab else header(direction)) + main + ("" if lab else footer(direction)) + "\n</body></html>\n"
    (LAB / filename).write_text(content, encoding="utf-8")

def event_card(event, search=False):
    supports = "".join(f'<span class="tag">{esc(x)}（例）</span>' for x in event["support"])
    href = "event-detail.html?id=" + event["id"]
    return f"""
<article class="event-card" data-event-card data-city="{esc(event["city"])}" data-genre="{esc(event["genre"])}" data-support="{esc("|".join(event["support"]))}" data-search="{esc(" ".join([event["title"],event["city"],event["genre"],*event["support"]]))}">
  <a class="photo-link event-card__photo" href="{href}" tabindex="-1" aria-hidden="true">{photo(event["image"], "", "(max-width: 759px) " + ("90vw" if search else "42vw") + ", (max-width: 1059px) 43vw, " + ("28vw" if search else "21vw"))}</a>
  <div class="event-card__body"><p class="card-meta"><span class="sample">サンプル</span><span>{esc(event["city"])}</span><span>{esc(event["genre"])}</span></p>
    <h3><a href="{href}">{esc(event["title"])}</a></h3><p class="event-card__date">日程は正式決定後に掲載</p><div class="tags">{supports}</div>
    {'<a class="text-link" href="'+href+'">詳しく見る'+ARROW+'</a>' if search else ''}
  </div>
</article>"""

def stories():
    items = [
        ("CRAFT & PEOPLE", "手から生まれる、<br>土地のものがたり。", "砥部焼をはじめ、暮らしに息づく手しごと。", "tobe-ceramics-workshop", EVENTS[1]["alt"], "event-detail.html?id=craft"),
        ("ART FOR EVERYONE", "その人だけの表現に、<br>出会う。", "障害のある人もない人も、表現を楽しむ場へ。", "inclusive-art-gallery", "明るいギャラリーで作品を鑑賞する人々のイメージ", "event-detail.html#support"),
        ("STAGE & TRADITION", "受け継ぐ文化が、<br>いま、舞台になる。", "地域に根ざした芸能と、新しい表現の出会い。", "event-stage-lanterns", EVENTS[0]["alt"], "event-detail.html?id=stage"),
    ]
    cards = ""
    for eyebrow, title, desc, image, alt, href in items:
        cards += f'<article class="story-card"><a class="photo-link" href="{href}" aria-hidden="true" tabindex="-1">{photo(image, "", "(max-width: 759px) 90vw, 30vw")}</a><p class="eyebrow">{eyebrow}</p><h3><a href="{href}">{title}</a></h3><p>{desc}</p></article>'
    return f"""
<section class="section" id="about"><div class="wrap">
  <div class="section-top"><div><p class="eyebrow eyebrow--accent">OUR CULTURE, OUR STORIES</p><h2 class="section-title">愛媛に息づく文化を、<br>一人ひとりの出会いへ。</h2></div>
    <p class="section-intro">瀬戸内海、宇和海、石鎚山。土地の風景のなかで育まれてきた文化を、県内各地から発信します。</p></div>
  <div class="story-grid">{cards}</div>
</div></section>"""

def rest_home(direction):
    cards = "".join(event_card(event) for event in EVENTS)
    return f"""
{stories()}
<section class="section section--wash"><div class="wrap">
  <div class="section-top"><div><p class="eyebrow eyebrow--accent">FIND YOUR EXPERIENCE</p><h2 class="section-title">あなたの「好き」から、<br>文化に出会う。</h2></div><a class="text-link" href="event-search.html">すべてのイベントを探す{ARROW}</a></div>
  <p class="small" style="margin-bottom:24px">以下は掲載イメージを示す架空の催しです。開催をお知らせする情報ではありません。</p>
  <div class="event-grid">{cards}</div>
</div></section>
<section class="section" id="news"><div class="wrap split-section">
  <div><p class="eyebrow eyebrow--accent">INFORMATION</p><h2 class="section-title">お知らせ</h2><p class="small" style="margin-top:16px">大会の準備、募集、<br>参加に関する情報をご案内します。</p></div>
  <ul class="news-list"><li><a href="documents.html"><span class="news-label">準備中</span><span>大会の準備と実行委員会に関する情報</span>{ARROW}</a></li><li><a href="#join"><span class="news-label">募集案内</span><span>出演・参加、ボランティア、協賛について</span>{ARROW}</a></li><li><a href="event-detail.html#support"><span class="news-label">参加支援</span><span>安心して参加するためのバリアフリー情報</span>{ARROW}</a></li></ul>
</div></section>
<section class="wrap invitation" id="join"><div><p class="eyebrow">BE PART OF THE FESTIVAL</p><h2>観る人も、つくる人も。<br>みんなが文化の担い手に。</h2></div><div><p>出演・出展、ボランティア、協賛など、さまざまな参加の方法をご案内します。募集の内容と開始時期は、正式決定後に掲載します。</p>{button("参加・募集の案内", "documents.html#participation", "light")}</div></section>"""

def build_homes():
    a = f"""
<main id="main">
<section class="wrap hero-a" aria-labelledby="home-title">
  <div class="hero-copy"><p class="eyebrow eyebrow--accent">EHIME CULTURE FESTIVAL · 2028</p><h1 id="home-title"><span>文化がひらく、</span><span>愛媛のこれから。</span></h1>
    <p class="lead">出会い、ふれあい、ともにつくる。<br>愛媛に息づく文化を、全国へ。そして次の世代へ。<br>一人ひとりの表現が、ここでつながります。</p>
    <div class="hero-actions">{button("イベントを探す", "event-search.html")}{button("大会について", "#about", "subtle")}</div>
    <p class="hero-footnote"><span class="year">2028</span><span>令和10年度 愛媛県開催予定<br>名称・会期は未定</span></p>
  </div>
  <div class="hero-visual"><figure class="hero-main">{photo("hero-ehime-culture-festival", "海を望む会場に、工芸と舞台芸術を楽しむ人々が集うイメージ", "(max-width: 759px) 78vw, 40vw", True)}</figure>
    <figure class="hero-inset">{photo("tobe-ceramics-workshop", EVENTS[1]["alt"], "(max-width: 759px) 40vw, 20vw")}</figure><span class="hero-caption" aria-hidden="true">A PLACE TO MEET. A CULTURE TO SHARE.</span><p class="image-disclaimer">写真はイメージです</p></div>
</section>
<nav class="wrap quick-paths" aria-label="目的から探す">
  <a href="event-search.html"><span class="number">01</span><span><strong>観る・体験する</strong><small>日程、市町、ジャンルから探す</small></span>{ARROW}</a>
  <a href="#join"><span class="number">02</span><span><strong>参加する・応援する</strong><small>出演、募集、協賛について</small></span>{ARROW}</a>
  <a href="event-detail.html#support"><span class="number">03</span><span><strong>安心して楽しむ</strong><small>バリアフリー、参加の支援</small></span>{ARROW}</a>
</nav>
{rest_home("editorial")}
</main>"""
    page("home-a.html", "文化がひらく、愛媛のこれから。", a)
    b = f"""
<main id="main">
<section class="poster-hero" aria-labelledby="home-title"><div class="wrap poster-grid">
  <div class="poster-copy"><p class="eyebrow">EHIME CULTURE FESTIVAL · 2028</p><h1 id="home-title"><span>ひらけ、</span><span>文化の可能性。</span></h1><p class="lead">観る。つくる。ともに楽しむ。<br>愛媛の文化をつなぐ、一人ひとりの表現へ。<br>文化の祭典が、県内各地にひろがります。</p><div class="hero-actions">{button("イベントを探す","event-search.html?direction=poster")}{button("大会について","#about","subtle")}</div><p class="hero-footnote"><span>令和10年度 愛媛県開催予定 ／ 名称・会期は未定</span></p></div>
  <div class="poster-photos"><figure class="poster-photo-1">{photo("family-culture-workshop","多世代が文化のワークショップを楽しむイメージ","(max-width: 759px) 78vw, 40vw",True)}</figure><figure class="poster-photo-2">{photo("inclusive-art-gallery","作品を囲み、芸術を楽しむ人々のイメージ","(max-width: 759px) 55vw, 25vw")}</figure><div class="poster-seal" aria-hidden="true"><strong>2028</strong><small>CULTURE FOR ALL</small></div></div>
</div></section>
<aside class="poster-ribbon"><div class="wrap"><strong>文化は、みんなのもの。</strong><span>障害のある人もない人も、ともに表現を楽しむ大会へ。</span><a href="event-detail.html?direction=poster#support">参加の支援を見る</a></div></aside>
{rest_home("poster")}
</main>"""
    page("home-b.html", "ひらけ、文化の可能性。", b, "poster")

def intro(eyebrow, title, desc, breadcrumb=None, note=True):
    crumb = breadcrumb or title
    return f"""
<section class="wrap page-intro"><nav class="breadcrumb" aria-label="現在位置"><a href="home-a.html">トップ</a><span aria-hidden="true">/</span><span aria-current="page">{esc(crumb)}</span></nav>
<p class="eyebrow eyebrow--accent">{eyebrow}</p><h1>{title}</h1><p class="intro">{desc}</p>
{'<p class="sample-note">掲載内容はサンプルです。実際の催し、日時、会場、料金などは正式決定後にご案内します。</p>' if note else ''}</section>"""

def build_search():
    main = f"""
<main id="main">
{intro("FIND YOUR EXPERIENCE","イベントを探す","気になる文化から、行きたい場所から。<br>自分に合った楽しみ方を見つけてください。")}
<div class="wrap">
<form class="filters" action="event-search.html" method="get" aria-label="イベントの絞り込み" data-event-filters>
  <div class="filter-grid"><label class="field" for="filter-q">キーワード<input id="filter-q" name="q" type="search" placeholder="催しの名前、地域など" autocomplete="off"></label>
    <label class="field" for="filter-city">市町<select id="filter-city" name="city"><option value="">すべて</option><option>松山市</option><option>砥部町</option><option>宇和島市</option></select></label>
    <label class="field" for="filter-genre">ジャンル<select id="filter-genre" name="genre"><option value="">すべて</option><option>舞台</option><option>工芸</option><option>食文化</option><option>文学</option></select></label>
    <label class="field" for="filter-support">参加の支援<select id="filter-support" name="support"><option value="">すべて</option><option>手話通訳</option><option>車椅子席</option><option>やさしい日本語</option><option>親子向け</option></select></label>
  </div>
  <div class="filter-bottom"><button class="button button--solid" type="submit" hidden data-js-only>この条件で探す{SEARCH}</button><button class="button button--subtle" type="button" data-reset-filters hidden data-js-only>条件をリセット</button><span class="small">日程と会場は正式決定後に掲載します。</span></div>
  <noscript><p class="sample-note">JavaScriptが無効のため絞り込みは利用できません。すべての催しを下の一覧からご覧ください。</p></noscript>
</form>
<div class="search-results-header"><h2 aria-live="polite" aria-atomic="true"><strong data-result-count>4</strong>件の催し</h2><p class="small">すべて架空のサンプルです</p></div>
<div class="event-grid search-grid" data-results>{''.join(event_card(e, True) for e in EVENTS)}</div>
<div class="empty-state" data-empty hidden><p class="eyebrow eyebrow--accent">NO RESULTS</p><h3>条件に合う催しはありません。</h3><p>キーワードを短くするか、市町やジャンルの条件を変更してみてください。</p><button class="button button--solid" data-reset-filters type="button">条件をリセット{ARROW}</button></div>
</div>
</main>"""
    page("event-search.html", "イベントを探す", main)

def build_detail():
    event = EVENTS[1]
    main = f"""
<main id="main">
<section class="wrap page-intro"><nav class="breadcrumb" aria-label="現在位置"><a href="home-a.html">トップ</a><span aria-hidden="true">/</span><a href="event-search.html">イベント</a><span aria-hidden="true">/</span><span aria-current="page">イベント詳細</span></nav>
  <p class="eyebrow eyebrow--accent">CULTURE EXPERIENCE</p><h1 data-detail-title>{esc(event["title"])}</h1><p class="intro" data-detail-description>{esc(event["description"])}</p><p class="sample-note">架空の催しを使った掲載例です。開催の告知ではありません。</p>
</section>
<div class="wrap detail-grid"><div class="detail-visual">
  <figure class="detail-media">{photo(event["image"],event["alt"],"(max-width: 759px) 90vw, 53vw",True,'data-detail-photo')}</figure><p class="detail-caption">写真はイメージです。実際の会場を表すものではありません。</p>
  </div><aside class="detail-aside" aria-label="催しの基本情報"><dl class="event-facts">
  <div><dt>開催日</dt><dd>未定<br><span class="small">正式決定後に掲載</span></dd></div><div><dt>市町</dt><dd data-detail-city>砥部町（サンプル）</dd></div><div><dt>会場</dt><dd>正式決定後に掲載</dd></div><div><dt>ジャンル</dt><dd data-detail-genre>工芸</dd></div><div><dt>料金</dt><dd>正式決定後に掲載</dd></div><div><dt>申込</dt><dd>募集開始前</dd></div>
  </dl>{button("参加の支援を確認","#support","subtle")}<p class="small">日時、会場、料金、申込方法は未確定です。</p><a class="text-link" href="event-search.html" style="margin-top:22px">イベント一覧へ戻る{ARROW}</a></aside>
  <div class="article-body"><section><h2>文化を、観る。ふれる。<br>ともに楽しむ。</h2><p>愛媛の多様な文化に出会い、一人ひとりが参加できる場へ。催しの内容や参加方法を、正式決定後にわかりやすくご案内します。</p></section>
  <section id="support"><p class="eyebrow eyebrow--accent">PARTICIPATION SUPPORT</p><h2 style="margin-top:12px">安心して参加するために</h2><p>参加の支援は、催しごとに対応内容を確認して掲載します。下記は情報の見せ方の例です。</p><ul class="support-list" data-detail-support><li class="support-item"><strong>親子向け（表示例）</strong><span>実際の対応は正式決定後に案内します。</span></li></ul></section>
  <section id="contact"><h2>問い合わせ</h2><p>催しの担当窓口と連絡先は、正式決定後に掲載します。現在、このページから申込や送信はできません。</p></section>
  <section><h2>参加についてよくある質問</h2><details><summary>申込方法はいつ案内されますか。</summary><p class="small" style="margin-top:12px">催しの内容と募集条件が決まり次第、申込方法と締切を掲載します。</p></details></section></div>
</div></main>"""
    page("event-detail.html", event["title"], main)

def build_documents():
    main = f"""
<main id="main">{intro("OFFICIAL INFORMATION","実行委員会・資料","大会の準備と運営に関する情報を掲載します。<br>会議資料や計画などを、項目ごとにご案内します。",note=False)}
<div class="wrap document-layout"><nav class="local-nav" aria-label="このページの内容"><a href="#overview">実行委員会の概要</a><a href="#documents">会議・計画資料</a><a href="#participation">参加・募集について</a></nav>
<article class="document-body"><section id="overview"><h2>実行委員会の概要</h2><p>愛媛大会（仮）の準備と運営に関する情報を、正式決定後に掲載します。</p><dl><div><dt>大会</dt><dd>令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）</dd></div><div><dt>会期</dt><dd>未定</dd></div><div><dt>体制</dt><dd>正式決定後に掲載</dd></div><div><dt>事務局</dt><dd>正式決定後に掲載</dd></div></dl></section>
<section id="documents"><h2>会議・計画資料</h2><p>公開する資料の名称、形式、ファイル容量、公開日を表示します。現在、ダウンロードできる資料はありません。</p>
<div style="margin-top:26px"><div class="doc-row"><span class="file-kind">PDF</span><div><strong>大会の基本構想</strong><small>ファイル容量、公開日は公開時に表示</small></div><span class="doc-status">準備中</span></div><div class="doc-row"><span class="file-kind">PDF</span><div><strong>実施計画</strong><small>ファイル容量、公開日は公開時に表示</small></div><span class="doc-status">準備中</span></div><div class="doc-row"><span class="file-kind">PDF</span><div><strong>実行委員会の会議資料</strong><small>会議ごとに資料を掲載</small></div><span class="doc-status">準備中</span></div></div>
</section><section id="participation"><h2>参加・募集について</h2><p>出演・出展、ボランティア、協賛などの参加方法と募集条件を、正式決定後に掲載します。</p><p class="sample-note">現在は募集開始前です。申込や問い合わせの連絡先は、正式な案内をご確認ください。</p></section></article></div></main>"""
    page("documents.html", "実行委員会・資料", main)

def build_components():
    tokens = json.loads((LAB / "tokens.json").read_text())
    swatches = "".join(f'<figure><div class="swatch" style="background:{tokens["base"][key]}"></div><figcaption>{key}<br>{tokens["base"][key]}</figcaption></figure>' for key in ["page","ink","accent","wash","muted","focus"])
    main = f"""
<main id="main">{intro("DESIGN SYSTEM / D2","共通部品と状態の確認","色、文字組、ボタン、入力、検索結果、未確定情報を確認する、開発用の部品一覧です。",note=False)}
<div class="wrap">
<section class="component-section"><h2>色とコントラスト</h2><div class="component-colors">{swatches}</div><p class="small" style="margin-top:20px">A案とB案で本文と操作部品の構造を共有します。B案はURLに direction=poster を付けて確認できます。</p></section>
<section class="component-section"><h2>文字組</h2><p class="eyebrow eyebrow--accent">ZEN KAKU GOTHIC NEW / MANROPE</p><p style="font-size:clamp(30px,4vw,54px);font-weight:700;line-height:1.5;margin-top:18px">文化がひらく、愛媛のこれから。</p><h3 style="margin-top:24px">長い名称でも、内容を正確に伝える。</h3><p style="max-width:42rem">令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）。正式名称、会場名、注記などが長くなっても、省略せずに読める文字組を確認します。</p><p class="small" style="margin-top:14px">日程・会場・料金は未定です。0123456789 / EHIME 2028</p></section>
<section class="component-section"><h2>ボタンとフォーカス</h2><div class="component-row">{button("イベントを探す","event-search.html")}{button("詳細を見る","event-detail.html","subtle")}{button("A案を見る","home-a.html","accent")}<button class="button button--subtle" disabled>募集開始前</button></div><p class="small" style="margin-top:18px">Tabキーでフォーカスを移動し、輪郭の表示と操作順を確認できます。</p></section>
<section class="component-section"><h2>入力とエラー</h2><div class="component-form"><label class="field" for="component-search">キーワード<input id="component-search" type="search" placeholder="催しの名前など"></label><div class="field"><label for="component-email">メールアドレス（表示例）</label><input id="component-email" type="email" value="sample" aria-invalid="true" aria-describedby="component-error"><span class="field-error" id="component-error">メールアドレスの形式で入力してください。</span></div></div><p class="small" style="margin-top:18px">この部品一覧から入力情報を送信することはありません。</p></section>
<section class="component-section"><h2>タグと未確定情報</h2><div class="component-row"><span class="tag">手話通訳（例）</span><span class="tag">車椅子席（例）</span><span class="tag tag--soft">日程未定</span></div><p class="sample-note">名称、日時、会場、料金、申込方法は、正式決定後に掲載します。</p></section>
<section class="component-section"><h2>長いタイトルと検索の状態</h2><div class="component-note"><h3>東予・中予・南予の文化と、多世代の参加をつなぐ交流プログラム（タイトルの表示例）</h3><p>スマートフォン幅でも固定高さによる文字の切れが起きないか確認します。</p></div><div class="component-row" style="margin-top:22px">{button("検索結果がある状態","event-search.html?genre=工芸","subtle")}{button("検索結果が0件の状態","event-search.html?q=該当しない催し","subtle")}</div></section>
</div></main>"""
    page("components.html", "共通部品", main)

def build_index():
    main = f"""
<a class="skip" href="#main">本文へ移動</a><header class="lab-header"><div class="wrap"><p class="eyebrow eyebrow--accent">EHIME CULTURE FESTIVAL / V2 DESIGN LAB</p><h1>文化祭の表情を、2つの方向から。</h1><p>v2.0の共通設計を確かめるD2の試作です。A案は文化を伝える写真と余白、B案は祝祭感を生む文字と色を中心に組み立てています。</p></div></header>
<main id="main"><section class="section"><div class="wrap lab-directions">
<article class="lab-direction"><p class="eyebrow eyebrow--accent">DIRECTION A / EDITORIAL</p><h2>文化をひらく、<br>静かな力。</h2><p>やわらかな白、深い緑、温かな差し色。文化を担う人と作品を、写真と文字組で伝えます。</p><div class="lab-mood">{photo("hero-ehime-culture-festival","A案の写真イメージ","(max-width: 759px) 48vw, 25vw")}<div class="mood-type" aria-hidden="true">文化が<br>ひらく。</div></div>{button("A案のトップを見る","home-a.html")}<p class="small">共通設計の暫定推奨案。文化紹介と情報の探しやすさを揃える方向です。</p></article>
<article class="lab-direction lab-direction--poster"><p class="eyebrow eyebrow--accent">DIRECTION B / POSTER</p><h2>祝祭を伝える、<br>文字と色。</h2><p>土のような温かな色、大きな見出し、写真の重なり。文化祭の参加感を強く打ち出します。</p><div class="lab-mood">{photo("family-culture-workshop","B案の写真イメージ","(max-width: 759px) 48vw, 25vw")}<div class="mood-type" aria-hidden="true">ひらけ、<br>文化。</div></div>{button("B案のトップを見る","home-b.html","accent")}<p class="small">表現の強さを比較する案。検索と資料ページには共通の操作部品を使います。</p></article>
</div></section>
<section class="section section--wash"><div class="wrap"><p class="eyebrow eyebrow--accent">PROTOTYPES</p><h2 class="section-title" style="margin-bottom:28px">トップ以外でも、使いやすく。</h2><div class="prototype-links"><a href="event-search.html">イベント検索<span>絞り込み、結果、0件、リセット</span></a><a href="event-detail.html?id=craft">イベント詳細<span>日時、会場、料金、支援の情報</span></a><a href="documents.html">実行委員会・資料<span>長い文章、資料の状態、ページ内目次</span></a><a href="components.html">共通部品<span>文字、色、入力、エラー、フォーカス</span></a></div></div></section>
<section class="section"><div class="wrap"><p class="eyebrow eyebrow--accent">REVIEW SCOPE</p><h2 class="section-title" style="margin-bottom:28px">比較するポイント</h2><div class="lab-proofs"><section><h3>愛媛の文化が伝わるか</h3><p>写真、文字組、色が一つの表情になっているか。人や作品の魅力が届くか。</p></section><section><h3>必要な情報へ進めるか</h3><p>催しを探し、日時や支援の情報を確認するまでの流れ。資料ページの読みやすさ。</p></section><section><h3>スマホでも成立するか</h3><p>幅を変えて、文字の折り返し、写真の配置、タップ領域、メニューを確認できます。</p></section></div><p class="sample-note">D2は方向比較と共通部品の試作段階です。全ページ展開と最終品質ゲートの通過は、後続工程で確認します。</p></div></section></main>"""
    page("index.html", "v2デザイン比較", main, lab=True)

def build_tokens():
    tokens = json.loads((LAB / "tokens.json").read_text())
    fonts = '''
@font-face{font-family:"Ehime Lab Sans";src:url("assets/fonts/ehime-sans-regular.woff2") format("woff2");font-style:normal;font-weight:400;font-display:swap}
@font-face{font-family:"Ehime Lab Sans";src:url("assets/fonts/ehime-sans-bold.woff2") format("woff2");font-style:normal;font-weight:700;font-display:swap}
@font-face{font-family:"Ehime Lab Latin";src:url("assets/fonts/ehime-latin.woff2") format("woff2");font-style:normal;font-weight:200 800;font-display:swap}
'''
    declarations = lambda obj: "".join(f"--{name}:{value};" for name, value in obj.items())
    css = "/* Generated from tokens.json. */\n" + fonts + ":root{" + declarations(tokens["base"]) + "}\n"
    for name, values in tokens["directions"].items():
        css += f'[data-direction="{name}"]' + "{" + declarations(values) + "}\n"
    (LAB / "tokens.css").write_text(css, encoding="utf-8")

def main():
    LAB.mkdir(exist_ok=True)
    build_tokens()
    build_homes()
    build_search()
    build_detail()
    build_documents()
    build_components()
    build_index()
    (LAB / "events-data.js").write_text("window.EHIME_LAB_EVENTS = " + json.dumps(EVENTS, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
    print("Built 7 D2 pages. Existing v1 pages are untouched.")

if __name__ == "__main__":
    main()
