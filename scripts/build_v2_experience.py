#!/usr/bin/env python3
"""Build a single cultural editorial experience and its canonical site routes."""
from pathlib import Path
import html
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "design-lab"
DATA = json.loads((LAB / "content.json").read_text())
TOKENS = json.loads((LAB / "tokens.json").read_text())
CULTURES = {c["id"]: c for c in DATA["cultures"]}
EVENTS = {e["id"]: e for e in DATA["events"]}
ROUTES = {
    "index.html": "index.html", "culture-craft.html": "culture/craft.html",
    "culture-literature.html": "culture/literature.html", "culture-food.html": "culture/food.html",
    "culture-art.html": "culture/art.html", "event-search.html": "events/search.html",
    "event-pre2026.html": "events/pre2026.html", "event-craft.html": "events/craft.html",
    "event-literature.html": "events/literature.html", "event-food.html": "events/food.html",
    "event-art.html": "events/art.html", "event-detail.html": "events/detail.html",
    "notebook.html": "culture/notebook.html", "documents.html": "committee/overview.html",
    "participation.html": "recruitment/index.html", "support.html": "accessibility/information-support.html",
    "about.html": "about/index.html", "news.html": "news/index.html", "access.html": "access/train.html",
    "sponsors.html": "sponsors/index.html", "privacy.html": "policy/privacy.html",
    "components.html": "design-lab/components.html",
}
CURRENT = "index.html"
SITE = False
ARROW = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
SEARCH = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><circle cx="10" cy="10" r="6.2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="m15 15 6 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
BOOK = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M4 3h15v18H4zm4 0v18m5-14h3m-3 4h3" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
PLUS = '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M4 12h16M12 4v16" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'

def esc(value):
    return html.escape(str(value), quote=True)

def route(filename):
    if not SITE:
        return filename
    return Path(os.path.relpath(ROOT / ROUTES[filename], (ROOT / ROUTES[CURRENT]).parent)).as_posix()

def asset(path):
    if not SITE:
        return path
    return Path(os.path.relpath(LAB / path, (ROOT / ROUTES[CURRENT]).parent)).as_posix()

def link(label, filename, suffix="", kind="text-link"):
    if kind == 'next-culture-link':
        label = '<span>'+label+'</span>'
    return f'<a class="{kind}" href="{esc(route(filename) + suffix)}">{label}{ARROW}</a>'

def image(name, alt, sizes="(max-width: 700px) 100vw, 50vw", eager=False, cls=""):
    portrait = name == "porcelain-hero"
    width, height = (1122, 1402) if portrait else (1536, 1024)
    return (f'<img class="{cls}" src="{asset("assets/art/"+name+"-960.webp")}" '
            f'srcset="{asset("assets/art/"+name+"-480.webp")} 480w, {asset("assets/art/"+name+"-960.webp")} 960w, {asset("assets/art/"+name+"-1440.webp")} 1440w" '
            f'sizes="{sizes}" width="{width}" height="{height}" alt="{esc(alt)}" decoding="async" '
            + ('loading="eager" fetchpriority="high"' if eager else 'loading="lazy"') + '>')

def plate(key, decorative=True):
    """Editable original artwork. These are metaphors, not exhibited works or maps."""
    aria = 'aria-hidden="true"' if decorative else 'role="img" aria-label="文化を表すオリジナルの図形"'
    if key == "literature":
        dots = "".join(f'<circle cx="{x}" cy="{92+i*30}" r="8" fill="#f5f2ea"/>' for x,n in [(148,5),(212,7),(276,5)] for i in range(n))
        return f'<svg class="plate" viewBox="0 0 440 420" {aria}><rect width="440" height="420" fill="#183c9e"/><path d="M45 42h350v336H45z" fill="none" stroke="#8097d3" stroke-width="1"/><path d="M74 353h293" stroke="#f5f2ea" stroke-width="1"/>{dots}<text x="74" y="62" fill="#f5f2ea" font-size="11" font-family="sans-serif" letter-spacing="2">THE WORD</text><text x="332" y="316" fill="#f5f2ea" font-size="60" font-family="sans-serif" transform="rotate(-90 332 316)">17</text></svg>'
    if key == "food":
        return f'<svg class="plate" viewBox="0 0 440 420" {aria}><rect width="440" height="420" fill="#e9ad89"/><circle cx="219" cy="216" r="142" fill="#f5f2ea"/><circle cx="219" cy="216" r="117" fill="none" stroke="#a94b34" stroke-width="2"/><path d="M65 225c70-77 139 77 210 0s105 5 139-25M65 257c70-77 139 77 210 0s105 5 139-25" fill="none" stroke="#183c9e" stroke-width="9"/><path d="M158 156c31-38 90-42 129 0-39 42-98 38-129 0l-24-25v50z" fill="#183c9e"/><circle cx="265" cy="155" r="4" fill="#f5f2ea"/><text x="40" y="43" fill="#151d36" font-size="11" font-family="sans-serif" letter-spacing="2">THE TABLE / UWAJIMA</text></svg>'
    if key == "art":
        return f'<svg class="plate" viewBox="0 0 620 420" {aria}><rect width="620" height="420" fill="#dce5dd"/><path d="M162 319V125c0-102 142-102 142 0v194z" fill="#183c9e"/><path d="M304 101h129v218H304z" fill="#b33227"/><circle cx="432" cy="101" r="63" fill="#e9ad89"/><path d="M141 319h335" fill="none" stroke="#151d36" stroke-width="2"/><path d="M371 167h83v110h-83z" fill="#f5f2ea"/><path d="M84 59h452v304H84z" fill="none" stroke="#798a7e" stroke-width="1"/><text x="42" y="36" fill="#151d36" font-size="11" font-family="sans-serif" letter-spacing="2">EVERYONE HAS A VIEW</text></svg>'
    if key == "stage":
        return f'<svg class="plate" viewBox="0 0 620 420" {aria}><rect width="620" height="420" fill="#183c9e"/><path d="M126 328V164c0-146 368-146 368 0v164" fill="none" stroke="#f5f2ea" stroke-width="31"/><path d="M161 328V164c0-94 296-94 296 0v164" fill="none" stroke="#e9ad89" stroke-width="14"/><path d="M93 360h434" fill="none" stroke="#f5f2ea" stroke-width="1"/><text x="40" y="42" fill="#f5f2ea" font-size="11" font-family="sans-serif" letter-spacing="2">ROAD TO 2028</text></svg>'
    return ""

def header():
    return f'''<a class="skip-link" href="#main">本文へ移動</a>
<div class="poc-banner"><div class="container"><span>DESIGN PoC / 2026.10.01</span><span>確認済み情報と、催しの掲載例を区別しています。</span></div></div>
<header class="masthead"><div class="container masthead-row">
<a class="brand" href="{route('index.html')}" aria-label="愛顔えひめの文化祭2028 トップ"><span class="brand-name">愛顔<span class="brand-reading">えがお</span><span class="brand-name-rest">えひめの文化祭<span class="brand-year">2028</span></span></span><span class="brand-sub">第43回国民文化祭 · 第28回全国障害者芸術・文化祭</span></a>
<nav class="main-navigation" id="main-navigation" aria-label="メインナビゲーション" data-navigation>
<a href="{route('index.html')}#discover">文化に出会う</a><a href="{route('participation.html')}">参加する</a><a href="{route('support.html')}">参加の支援</a><a href="{route('about.html')}">大会について</a></nav>
<div class="header-tools"><a class="book-link" href="{route('notebook.html')}" aria-label="文化帖。保存した催しを見る">{BOOK}<span class="book-link-label">文化帖</span><span class="book-count" data-book-count>0</span></a><a class="header-search" href="{route('event-search.html')}">{SEARCH}<span>探す</span></a><button class="menu-button" type="button" data-menu hidden aria-expanded="false" aria-controls="main-navigation"><span class="menu-symbol" aria-hidden="true">＋</span><span data-menu-label>メニュー</span></button></div>
</div></header>
<aside class="information-strip" aria-label="重要な情報"><div class="container"><strong>INFORMATION</strong><span>本大会は2028年開催。個別の催しは順次発表されます。</span><a href="{route('news.html')}">お知らせ{ARROW}</a></div></aside>'''

def footer():
    return f'''<footer class="footer"><div class="container"><div class="footer-top"><div><p class="label">CULTURE BEGINS WITH YOU.</p><p class="footer-phrase">つくる人も。<br>観る人も。あなたも。</p></div><div class="footer-festival"><p>愛顔（えがお）えひめの文化祭2028</p><p class="footer-date"><span>2028</span> 10.22 — 12.03</p>{link('大会の概要','about.html')}</div></div>
<nav class="footer-navigation" aria-label="フッター"><a href="{route('event-search.html')}">催しを探す</a><a href="{route('participation.html')}">参加・募集</a><a href="{route('sponsors.html')}">協賛</a><a href="{route('access.html')}">交通・アクセス</a><a href="{route('documents.html')}">実行委員会・資料</a><a href="{route('support.html')}">参加の支援</a><a href="{route('privacy.html')}">プライバシー</a><a href="https://www.pref.ehime.jp/soshiki/286/">県の担当窓口 ↗</a></nav>
<div class="footer-bottom"><p>デザインPoC。主画像はAI生成、図形はオリジナルの編集ビジュアルです。実在の作品・会場の記録ではありません。</p><p>EHIME CULTURE 2028</p></div></div></footer><div class="sr-only" role="status" aria-live="polite" aria-atomic="true" data-global-status></div>'''

def breadcrumb(title, parent=None):
    extra = f'<a href="{route(parent[1])}">{esc(parent[0])}</a><span aria-hidden="true">/</span>' if parent else ""
    return f'<nav class="breadcrumb" aria-label="現在位置"><a href="{route("index.html")}">トップ</a><span aria-hidden="true">/</span>{extra}<span aria-current="page">{esc(title)}</span></nav>'

def intro(label, title, desc, parent=None):
    return f'<section class="container page-intro">{breadcrumb(re.sub("<[^>]*>","",title),parent)}<p class="label">{label}</p><h1>{title}</h1><p class="page-lead">{desc}</p></section>'

def sample_tag(event):
    return '<span class="status status--verified">確認済み</span>' if event['kind']=='verified' else '<span class="status">催しの掲載例</span>'

def save(event):
    return f'<button class="save-button" data-save="{event["id"]}" aria-pressed="false" aria-label="{esc(event["title"])}を文化帖に追加" type="button" hidden>{PLUS}<span data-save-label>文化帖に追加</span></button>'

def event_row(event, number=None):
    support = '・'.join(event['supports']) + '（表示例）' if event['supports'] else '公式案内をご確認ください'
    return f'''<article class="event-row" data-event-card data-id="{event['id']}" data-city="{event['city']}" data-genre="{event['genre']}" data-kind="{event['kind']}" data-support="{'|'.join(event['supports'])}" data-search="{esc(' '.join([event['title'],event['city'],event['genre'],*event['supports']]))}">
<div class="event-row-meta">{sample_tag(event)}<p>{event['city']} / {event['genre']}</p></div><div class="event-row-main"><h3><a href="{route(event['page'])}"><span class="event-title">{esc(event['title'])}</span>{ARROW}</a></h3><p>{esc(event['date'])}</p><p class="event-support">参加の支援：{support}</p></div><div class="event-row-action">{save(event)}</div></article>'''

def culture_tile(c):
    artwork = image('craft-hands','白磁の器に藍を絵付けする手のAI生成イメージ','(max-width: 700px) 100vw, 55vw') if c['id']=='craft' else plate(c['id'])
    return f'''<a class="culture-tile culture-tile--{c['id']}" href="{route('culture-'+c['id']+'.html')}"><div class="culture-tile-image">{artwork}<span class="tile-number">{c['number']}</span></div><div class="culture-tile-caption"><div><span class="label">{c['english']}</span><h3>{c['title']}</h3><p>{c['place']} / {c['word']}</p></div><span class="round-arrow">{ARROW}</span></div></a>'''

def painting_studio():
    return '''<section class="painting-studio" data-paint-studio hidden><div class="container painting-grid"><div class="painting-copy"><p class="label">A SMALL DIGITAL WORKSHOP</p><h2>あなたの藍を、<br>一筆。</h2><p>白磁と藍に着想を得た、デジタルの絵付け。<br>図形を重ねるか、自分で線を描いてみてください。</p><p class="painting-note">砥部焼の製作工程を再現するものではありません。つくった図形は、このブラウザー内に保存します。</p><div class="paint-presets" aria-label="絵付けに加える図形"><button type="button" data-paint-preset="circle">円をひらく</button><button type="button" data-paint-preset="wave">波を重ねる</button><button type="button" data-paint-preset="line">線を引く</button></div><div class="paint-actions"><button type="button" data-paint-mode aria-pressed="false">自分で描く</button><button type="button" data-paint-undo>一筆戻す</button><button type="button" data-paint-clear>消す</button></div><button class="button button--primary" data-paint-export type="button">絵付けを持ちかえる<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.5"/></svg></button><p class="sr-only" data-paint-status role="status" aria-live="polite" aria-atomic="true"></p></div><div class="painting-canvas"><svg data-paint-board viewBox="0 0 600 540" aria-label="デジタル絵付けのプレビュー。図形の追加ボタンで、円・波・線を重ねられます。" role="img"><defs><radialGradient id="porcelain"><stop offset="0" stop-color="#fffdf8"/><stop offset=".84" stop-color="#efebe1"/><stop offset="1" stop-color="#dbd5c8"/></radialGradient><clipPath id="bowl-mask"><circle cx="300" cy="263" r="206"/></clipPath></defs><rect width="600" height="540" fill="#e9e4d8"/><ellipse cx="309" cy="298" rx="224" ry="220" fill="#d0c8b7"/><circle cx="300" cy="263" r="222" fill="#fffdf8"/><circle cx="300" cy="263" r="206" fill="url(#porcelain)"/><circle cx="300" cy="263" r="178" fill="none" stroke="#ddd6c8" stroke-width="1"/><g data-paint-lines clip-path="url(#bowl-mask)" fill="none" stroke-linecap="round" stroke-linejoin="round"></g><text x="31" y="516" fill="#183c9e" font-family="sans-serif" font-size="11" letter-spacing="2">YOUR BLUE / YOUR EXPRESSION</text></svg><p data-paint-instruction>図形を加えるボタンはキーボードでも操作できます。「自分で描く」を選ぶと、器の中に線を描けます。</p></div></div></section>'''

def home():
    return f'''<main id="main"><section class="container opening"><div class="opening-copy"><p class="label">EHIME CULTURE FESTIVAL / 2028</p><h1><span>愛媛を、</span><span>ひらく。</span></h1><p class="opening-lead">土に、ことばに、音に、人に。<br>あなたの入口から、この土地の文化へ。</p><div class="opening-actions">{link('文化に出会う','index.html','#discover','button button--primary')}{link('催しを探す','event-search.html','','button button--line')}</div><div class="opening-date"><span class="label">FESTIVAL DATES</span><p><strong>10.22</strong><span class="date-connector">—</span><strong>12.03</strong></p><p class="date-note">2028年 / 日曜日から日曜日まで / 43日間</p></div></div><figure class="opening-image">{image('porcelain-hero','白磁の器と藍の筆跡。砥部焼に着想を得たAI生成の主画像。','(max-width: 700px) 100vw, 46vw',True)}<figcaption><span>01 / WHITE PORCELAIN, BLUE PIGMENT.</span><span>AI生成イメージ</span></figcaption><span class="image-note" aria-hidden="true">A PLACE.<br>MANY VOICES.</span></figure></section>
<section class="container editorial-intro" id="about"><div><p class="label">A CULTURE OF MANY VOICES</p><p class="editorial-index">01—04</p></div><h2>暮らしのなかに、<br>まだ知らない文化がある。</h2><div class="reading"><p>器に描かれた藍。まちを歩いて生まれたことば。<br>海から届く味わい。ひとりひとりの表現。</p><p>愛媛の文化は、日々の営みからひらきます。<br>国民文化祭と全国障害者芸術・文化祭を一体的に開催する43日間。あなたの「気になる」から、出会いを始めてください。</p>{link('愛顔えひめの文化祭2028とは','about.html')}</div></section>
<section class="container discovery" id="discover"><div class="section-heading"><div><p class="label">FOUR WAYS INTO EHIME</p><h2>文化の入口。</h2></div><p>読む、見つける、持ちかえる。<br>四つの視点から愛媛へ。</p></div><div class="culture-wall">{''.join(culture_tile(c) for c in DATA['cultures'])}</div><p class="art-credit">写真はAI生成。図形は俳句・食卓・多様な表現に着想を得た編集ビジュアルです。</p></section>
<section class="notebook-invitation"><div class="container notebook-invitation-grid"><div class="notebook-motif" aria-hidden="true"><span>MY</span><span>CULTURE</span><span>NOTES<span class="motif-dot">●</span></span><div class="motif-rule"></div><span class="label">EHIME / 2028</span></div><div><p class="label">MAKE IT YOURS</p><h2>気になる文化を、<br>一冊に。</h2><p>催しの案内から「文化帖に追加」。<br>集めた催しを見返し、一覧を持ちかえられます。<br>観たいもの、やってみたいことから、あなたの文化帖を。</p>{link('わたしの文化帖を開く','notebook.html','','button button--primary')}</div></div></section>
<section class="container featured" id="events"><div class="section-heading"><div><p class="label">ROAD TO 2028</p><h2>文化が集う、その前に。</h2></div>{link('催しの一覧へ','event-search.html')}</div>{event_row(EVENTS['pre2026'])}<div class="featured-sample"><h3>文化祭の楽しみ方を想定した掲載例</h3><p class="small">以下は架空の催しです。開催の告知ではありません。</p></div>{event_row(EVENTS['craft'])}{event_row(EVENTS['art'])}</section>
<section class="participation-band" id="participation"><span id="support" aria-hidden="true"></span><div class="container participation-band-grid"><p class="label">OPEN TO EVERYONE</p><h2>楽しみたい気持ちに、<br>入口をひらく。</h2><div><p>障害のある人もない人も。<br>会場の設備や情報の伝え方、参加に必要な支援を確認できるように。催しを探すところから、支援の情報につながります。</p>{link('参加の支援を確かめる','support.html','','button button--line')}</div></div></section>
<section class="container news-preview" id="news"><div class="section-heading"><div><p class="label">UPDATES</p><h2>お知らせ。</h2></div>{link('すべてのお知らせ','news.html')}</div>{news_rows()}</section></main>'''

def news_rows():
    rows = [
        ('2026.09.11','大会情報','大会名称と会期について','https://www.pref.ehime.jp/page/155598.html'),
        ('2026.09.11','開催準備','全国文化交流事業の開催地などの準備状況','https://www.pref.ehime.jp/page/158706.html'),
        ('2026.06.01','実行委員会','設立総会・第1回総会の開催概要','https://www.pref.ehime.jp/page/148406.html'),
    ]
    return '<div class="news-list">'+''.join(f'<a href="{url}"><time>{date}</time><span class="news-type">{tag}</span><span class="news-title">{title}<span class="external-symbol" aria-hidden="true">↗</span></span><span class="sr-only">（愛媛県サイト）</span></a>' for date,tag,title,url in rows)+'</div>'

def culture(c):
    artwork = image('craft-hands','器に藍を絵付けする手のAI生成イメージ','(max-width: 700px) 100vw, 65vw',True) if c['id']=='craft' else plate(c['id'])
    related = CULTURES[c['related']]
    return f'''<main id="main">{intro(c['english'],c['title'],c['intro'],('文化の入口','index.html'))}<section class="container culture-feature"><div class="culture-feature-art">{artwork}<p class="art-credit">{'AI生成イメージ。実在のつくり手・作品を表す写真ではありません。' if c['id']=='craft' else '文化に着想を得たオリジナルの編集図形。掲載作品ではありません。'}</p></div><div class="culture-feature-aside"><span class="culture-feature-number">{c['number']}</span><p class="label">FIELD NOTES</p><h2>{c['place']}<br>{c['word']}の文化</h2><div class="tags">{''.join('<span>'+tag+'</span>' for tag in c['tags'])}</div></div></section><section class="container story-grid"><div><p class="label">THE BACKGROUND</p><h2>出会いの、<br>その手前で。</h2></div><div class="story-copy">{''.join('<p>'+p+'</p>' for p in c['paragraphs'])}<div class="source-note"><p>文化の背景に関する出典</p><a href="{c['source']}">{c['sourceLabel']} ↗</a><span>2026年10月1日確認。大会での実施内容を示すものではありません。</span></div></div></section><section class="container culture-events"><div class="section-heading"><div><p class="label">FROM STORY TO EXPERIENCE</p><h2>この文化を、体験へ。</h2></div>{link(c['genre']+'の催しを探す','event-search.html','?genre='+c['genre'])}</div><p class="small">次の催しは、ページの使い方を確認するための架空の掲載例です。</p>{event_row(EVENTS[c['event']])}</section><section class="container next-culture"><p class="label">KEEP EXPLORING</p><p>{c['relatedReason']}</p>{link(related['title'],'culture-'+related['id']+'.html','','next-culture-link')}</section></main>'''

def search():
    options = lambda values: '<option value="">すべて</option>'+''.join(f'<option>{v}</option>' for v in values)
    rows = ''.join(event_row(e) for e in DATA['events'])
    return f'''<main id="main">{intro('FIND YOUR CULTURE','催しを、探す。','文化から、場所から、参加の支援から。<br>あなたに合う入口を見つけてください。')}<div class="container search-layout"><form class="search-filters" action="{route('event-search.html')}" method="get" data-filters aria-label="催しの絞り込み"><div class="filter-heading"><span class="label">FILTER BY</span><h2>探す条件</h2></div><label for="filter-q">キーワード<input type="search" id="filter-q" name="q" autocomplete="off" placeholder="文化、まち、催しの名前"></label><div class="filter-fields"><label for="filter-city">地域<select id="filter-city" name="city">{options(['松山市','砥部町','宇和島市'])}</select></label><label for="filter-genre">文化<select id="filter-genre" name="genre">{options(['工芸','文学','食文化','美術','舞台'])}</select></label><label for="filter-support">参加の支援<select id="filter-support" name="support">{options(['親子向け','やさしい日本語','車椅子席','手話通訳'])}</select></label><label for="filter-kind">情報の種類<select id="filter-kind" name="kind"><option value="">すべて</option><option value="verified">確認済みの催し</option><option value="sample">架空の掲載例</option></select></label></div><p class="filter-note">支援の種類は掲載例を含みます。実施内容は詳細の状態表示で確認してください。</p><div class="filter-actions"><button type="submit" class="button button--primary" data-js-only hidden>この条件で探す{SEARCH}</button><button type="button" class="reset-button" data-reset hidden>条件をリセット</button></div><noscript><p class="nojs-note">絞り込みにはJavaScriptが必要です。すべての催しを一覧からご覧ください。</p></noscript></form><section class="search-results" aria-label="検索結果"><div class="results-heading"><h2><span data-count>5</span><small>件の催し</small></h2><p>確認済み1件 / 架空の掲載例4件</p></div><p class="sr-only" role="status" aria-live="polite" aria-atomic="true" data-result-status></p><div data-results>{rows}</div><div class="empty-state" data-empty hidden><span class="label">NO MATCH</span><h3>まだ、見つかりません。</h3><p>条件を一つ減らすか、短いことばで探してみてください。</p><button type="button" class="button button--primary" data-reset>条件をリセット{ARROW}</button></div></section></div></main>'''

def event(e):
    c = CULTURES[e['culture']]
    artwork = image('craft-hands','白磁の器に藍を絵付けする手のAI生成イメージ','(max-width: 700px) 100vw, 58vw',True) if e['id']=='craft' else plate('stage' if e['id']=='pre2026' else c['id'])
    note = '県の公開情報に基づく案内です。変更や詳細は、出典の公式案内をご確認ください。' if e['kind']=='verified' else 'この催しは架空の掲載例です。開催の告知ではなく、申込みはできません。'
    source = f'<a class="button button--primary" href="{e["source"]}">公式の案内を確認 ↗</a>' if e['kind']=='verified' else '<p class="unavailable-action">申込みはありません（掲載例）</p>'
    support = ''.join('<li>'+v+'（表示例）</li>' for v in e['supports']) or '<li>公式案内をご確認ください</li>'
    return f'''<main id="main">{intro(e['city']+' / '+e['genre'],e['title'],e['description'],('催しを探す','event-search.html'))}<div class="container event-state">{sample_tag(e)}<p>{note}</p></div><section class="container event-detail-grid"><div class="event-detail-art">{artwork}<p class="art-credit">{'AI生成イメージ。実際の作品・開催写真ではありません。' if e['id']=='craft' else 'オリジナルの編集図形。実際の作品・会場を表すものではありません。'}</p></div><aside class="event-facts" aria-label="開催情報"><p class="label">AT A GLANCE</p><h2>行く前に、確認。</h2><dl><div><dt>日時</dt><dd>{e['date']}</dd></div><div><dt>会場</dt><dd>{e['venue']}</dd></div><div><dt>料金</dt><dd>{e['fee']}</dd></div><div><dt>申込</dt><dd><span class="status">{e['status']}</span><p>{e['booking']}</p></dd></div></dl>{source}<div class="fact-save">{save(e)}</div></aside></section><section class="container story-grid" id="support"><div><p class="label">BEFORE YOU VISIT</p><h2>参加の支援。</h2></div><div class="story-copy"><p>{e['supportStatus']}</p><ul class="support-list">{support}</ul>{link('支援を確認するときのポイント','support.html')}<div class="source-note"><p>申込み・問い合わせについて</p><span>{'事前申込は受付終了です。問い合わせ先と最新の情報は県の公式案内に掲載されています。' if e['kind']=='verified' else 'この掲載例への申込み・個別の問い合わせは受け付けていません。'}</span><a href="{DATA['festival']['source']}">愛媛県の大会情報 ↗</a></div></div></section><section class="container next-culture"><p class="label">GO A LITTLE DEEPER</p><p>催しの向こうに、土地の文化。</p>{link(c['title'],'culture-'+c['id']+'.html','','next-culture-link')}{link('催しの一覧へ戻る','event-search.html')}</section></main>'''

def notebook():
    return f'''<main id="main">{intro('MY CULTURE NOTES','わたしの、文化帖。','「気になる」を持ちかえる。<br>集めた催しを、ここで見返せます。')}<section class="container notebook-layout"><aside class="notebook-cover" aria-label="文化帖の表紙"><p class="label">EHIME / 2028</p><h2>MY<br>CULTURE<br>NOTES<span class="motif-dot">●</span></h2><div class="notebook-pattern" data-notebook-pattern aria-hidden="true"></div><p class="notebook-themes" data-notebook-themes>気になる文化を集めると、表紙のしるしが変わります。</p><div class="cover-rule"></div><p class="notebook-count"><strong data-notebook-count>0</strong><span>気になる催し</span></p><p class="small">愛顔えひめの文化祭2028</p></aside><div class="notebook-content"><div class="notebook-tools" data-js-only hidden><button class="button button--line" type="button" data-export>文化帖を持ちかえる{ARROW}</button><button class="reset-button" type="button" data-share>リンクをコピー</button></div><div data-notebook-list></div><div class="empty-state" data-notebook-empty><p class="label">YOUR FIRST NOTE</p><h2>最初の「気になる」を。</h2><p>催しの案内から「文化帖に追加」を押すと、<br>ここに集まります。</p>{link('催しを探す','event-search.html','','button button--primary')}</div><div class="notebook-share-fallback" data-share-fallback hidden><label for="share-url">コピーするリンク<input id="share-url" readonly type="text"></label><p class="small">リンクを選択してコピーしてください。</p></div><noscript><p class="nojs-note">文化帖の保存にはJavaScriptが必要です。催しの各ページは、そのままご覧いただけます。</p></noscript><p class="notebook-footnote">文化帖は申込み・予約ではありません。開催情報は各催しの案内で確認してください。保存内容はお使いのブラウザー内に保持します。</p><p class="small" data-storage-status></p><p class="sr-only" role="status" data-notebook-status aria-live="polite" aria-atomic="true"></p></div></section></main>'''

def documents():
    return f'''<main id="main">{intro('GOVERNANCE & DOCUMENTS','実行委員会と、資料。','大会の方針と、開催に向けた取組を。<br>公開済みの資料を、出典から確認できます。')}<section class="container document-layout"><nav class="section-index" aria-label="このページの項目"><p class="label">ON THIS PAGE</p><a href="#published">公開済みの情報</a><a href="#upcoming">今後の案内</a><a href="#contact">担当窓口</a></nav><div><section class="document-section" id="published"><p class="label">PUBLISHED</p><h2>公開済みの情報</h2><p>資料の正式名称、更新日、ファイル形式は、県の出典ページで確認してください。</p><div class="document-list"><a href="https://www.pref.ehime.jp/page/155598.html"><span class="status status--verified">公開済み</span><div><h3>大会概要・基本構想</h3><p>県の案内ページ。基本構想のPDFなどを掲載。</p></div><span>県サイト ↗</span></a><a href="https://www.pref.ehime.jp/page/148406.html"><span class="status status--verified">公開済み</span><div><h3>実行委員会 設立総会・第1回総会</h3><p>2026年5月29日。開催概要と会議資料。</p></div><span>県サイト ↗</span></a><a href="https://www.pref.ehime.jp/page/158706.html"><span class="status status--verified">公開済み</span><div><h3>2028年に向けた準備状況</h3><p>全国文化交流事業の開催地などに関する発表。</p></div><span>県サイト ↗</span></a></div></section><section class="document-section" id="upcoming"><p class="label">UPCOMING</p><h2>今後の案内</h2><div class="pending-row"><span class="status">このPoCでは未掲載</span><h3>個別催しの募集要項・会場案内</h3><p>公開された情報を確認し、出典と公開日を付けて追加します。</p></div></section><section class="document-section" id="contact"><p class="label">CONTACT</p><h2>担当窓口</h2><p>大会についての正式な問い合わせ先は、愛媛県国民文化祭推進室のページをご確認ください。</p><a class="button button--primary" href="https://www.pref.ehime.jp/soshiki/286/">県の担当窓口へ ↗</a></section></div></section></main>'''

def participation():
    return f'''<main id="main">{intro('TAKE PART','文化をつくる、一人に。','出演、出展、支える活動。<br>あなたらしい関わり方を見つけてください。')}<section class="container participation-grid"><div class="participation-print" aria-hidden="true"><span>観る。</span><span>つくる。</span><span>支える。</span><div class="cover-rule"></div><small>YOU ARE PART OF CULTURE.</small></div><div class="participation-options"><h2>参加・募集の案内</h2><p>このPoCに個別の募集要項・申込窓口は設置していません。正式な募集の有無や受付期間は、県の公開情報をご確認ください。</p><div class="participation-option"><span class="label">01 / PERFORM & EXHIBIT</span><h3>出演・出展する</h3><p>発表や交流の場に、あなたの表現を。個別の条件は募集要項の公開後にご案内します。</p></div><div class="participation-option"><span class="label">02 / SUPPORT</span><h3>運営を支える</h3><p>ボランティアなどの募集情報は、正式な公開情報に基づいて掲載します。</p></div><div class="participation-option"><span class="label">03 / PARTNER</span><h3>協賛・協力する</h3><p>企業・団体としての関わり方。制度の確定状況と連絡先を確認できます。</p>{link('協賛・協力の案内','sponsors.html')}</div><a class="button button--primary" href="https://www.pref.ehime.jp/soshiki/286/">県の最新情報へ ↗</a></div></section></main>'''

def support():
    return f'''<main id="main">{intro('OPEN TO EVERYONE','参加の支援を、確かめる。','楽しみ方は、一人ひとり違うから。<br>必要な情報に、催しを探すところからつながります。')}<section class="container support-intro"><div>{plate('art')}</div><div><h2>表示があることと、<br>利用できることを分けて確認。</h2><p>このPoCの「手話通訳」「車椅子席」などの表示は、架空の催しで使う掲載例を含みます。実際の対応は、公式案内と主催者への確認が必要です。</p>{link('支援の条件から催しを探す','event-search.html','','button button--primary')}</div></section><section class="container story-grid"><div><p class="label">CHECK BEFORE YOU GO</p><h2>確認したい、<br>四つのこと。</h2></div><div class="support-checks"><article><span>01</span><h3>会場までの移動</h3><p>駅・停留所からの経路、入口の段差、駐車場、車椅子での移動について。</p></article><article><span>02</span><h3>会場の設備</h3><p>席の位置、トイレ、休憩スペース、介助者の同伴について。</p></article><article><span>03</span><h3>情報の受け取り方</h3><p>手話通訳、字幕、音声案内、やさしい日本語など、必要な支援について。</p></article><article><span>04</span><h3>事前の相談</h3><p>予約の要否、連絡方法、相談期限を、各催しの正式な窓口に確認してください。</p></article></div></section><section class="container next-culture"><p class="label">MANY WAYS TO EXPERIENCE</p><p>作品を観ることも、表すことも。</p>{link('それぞれの、見え方。','culture-art.html','','next-culture-link')}</section></main>'''

def about():
    return f'''<main id="main">{intro('ABOUT THE FESTIVAL','愛媛で、文化をひらく。','愛顔（えがお）えひめの文化祭2028。<br>つくる人も観る人も、交流する43日間。')}<section class="container about-date"><p class="label">2028 / EHIME, JAPAN</p><p><strong>10.22</strong><span>—</span><strong>12.03</strong></p><p>2028年10月22日（日）から12月3日（日）まで</p></section><section class="container story-grid"><div><p class="label">TWO FESTIVALS, TOGETHER</p><h2>文化を通じて、<br>出会う。</h2></div><div class="story-copy"><p>{DATA['festival']['description']}</p><p>県内各地で、文化活動の発表、共演、交流の場をつくる文化の祭典です。地域の文化を受け継ぎ、新しい表現につなげていきます。</p><h3>国民文化祭</h3><p>さまざまな芸術文化活動を全国規模で発表・交流する文化の祭典。愛媛では1990年以来、2度目の開催です。</p><h3>全国障害者芸術・文化祭</h3><p>障害のある人の芸術文化活動への参加を広げ、社会参加や理解につなげる文化の祭典。愛媛では初めての開催です。</p><div class="source-note"><p>大会名称・会期・概要の出典</p><a href="{DATA['festival']['source']}">愛媛県の大会概要 ↗</a><span>2026年9月11日更新、2026年10月1日確認。</span></div></div></section></main>'''

def simple_page(kind):
    if kind == 'news':
        return f'<main id="main">{intro("UPDATES","お知らせ。","開催に向けた動きと、公開された情報を。") }<section class="container news-page"><h2>県の公開情報</h2><p class="small">各記事は愛媛県のページへ移動します。日時は出典ページの公開・更新日です。</p>{news_rows()}<div class="source-note"><p>個別催しの変更・中止について</p><span>このPoCでは、速報やリアルタイムの情報更新は行っていません。最新情報は公式案内をご確認ください。</span></div></section></main>'
    if kind == 'access':
        return f'<main id="main">{intro("TRAVEL & ACCESS","文化に会いに、愛媛へ。","会場への行き方を、参加の条件と一緒に。") }<section class="container story-grid"><div><p class="label">PLAN YOUR VISIT</p><h2>目的地を決めてから、<br>行き方を確認。</h2></div><div class="story-copy"><p>本大会の個別会場・日時は、各催しの正式発表後にご案内します。このページでは交通時刻や運賃を掲載していません。</p><h3>まず、催しの会場を確認</h3><p>公式の開催案内で、施設名、住所、入口、申込条件を確認してください。</p>{link('催しを探す','event-search.html')}<h3>次に、交通手段を確認</h3><p>運行日・時刻・バリアフリー設備は、利用する交通事業者の最新情報を確認してください。</p><h3>移動や会場に支援が必要なとき</h3><p>入口の段差、席の位置、介助者の同伴なども、会場への移動と合わせて確認できます。</p>{link('参加の支援','support.html')}</div></section></main>'
    if kind == 'sponsors':
        return f'<main id="main">{intro("PARTNER WITH CULTURE","文化の未来を、ともに。","企業・団体の皆さまへ。<br>協賛・協力に関する正式な情報へご案内します。") }<section class="container story-grid"><div><p class="label">PARTNERSHIP</p><h2>制度と窓口を、<br>確かめる。</h2></div><div class="story-copy"><p>このPoCでは、協賛制度、協賛金額、募集期間などの確定情報は掲載していません。</p><p>正式な募集の有無・条件は、愛媛県国民文化祭推進室の公開情報をご確認ください。</p><a class="button button--primary" href="https://www.pref.ehime.jp/soshiki/286/">県の担当窓口へ ↗</a><div class="source-note"><p>このページからの申込み・送信はありません</p><span>入力フォームは設けていません。公開された募集要項を確認し、指定された方法でご連絡ください。</span></div></div></section></main>'
    if kind == 'privacy':
        return f'<main id="main">{intro("PRIVACY IN THIS PoC","このPoCの、データの扱い。","文化帖の保存内容と、入力した検索条件について。") }<section class="container story-grid"><div><p class="label">YOUR DATA</p><h2>保存するもの、<br>公開するもの。</h2></div><div class="story-copy"><h3>文化帖</h3><p>追加した催しのIDを、お使いのブラウザーのローカルストレージに保存します。氏名・連絡先などの個人情報は入力しません。</p><p>文化帖のページで催しを削除すると、保存内容も更新されます。保存を利用できない場合は、ページ内の移動で選択を引き継ぎます。</p><h3>リンクのコピー</h3><p>コピーしたURLには、選んだ催しのIDが含まれます。相手に共有すると、その催しの組み合わせが伝わります。</p><h3>デジタル絵付け</h3><p>自分で描いた線や選んだ図形を、このブラウザーのローカルストレージに保存します。SVGファイルとして持ち出せます。文化帖の共有URLには、絵付けの内容を含めません。</p><h3>検索条件</h3><p>絞り込み条件はURLに含まれます。このPoCには検索内容を外部へ送信する処理やアクセス解析を実装していません。</p><h3>外部サイト</h3><p>県や市町のページなどに移動した後は、そのサイトのデータ取扱方針をご確認ください。</p></div></section></main>'
    return f'<main id="main">{intro("DESIGN SYSTEM","設計の、共通部品。","色と文字組、状態の表示を、同じ考え方で。") }<section class="container component-demo"><h2>状態と操作</h2><p><span class="status status--verified">確認済み</span> <span class="status">催しの掲載例</span> <span class="status">受付終了</span></p>{link("主な操作","event-search.html","","button button--primary")}{link("補助の操作","documents.html","","button button--line")}<label for="demo-input">入力ラベル<input id="demo-input" placeholder="日本語の入力例"></label><h2>長い見出し</h2><h3>第43回国民文化祭・第28回全国障害者芸術・文化祭の参加案内を確認する</h3><p>本文は読み幅と行間を確保します。英数字も日本語も、同じ情報の階層のなかに置きます。</p></section></main>'

def legacy_detail():
    return f'<main id="main">{intro("CHOOSE AN EVENT","催しの案内を、選ぶ。","それぞれのページで、日時・会場・申込の状態を確認できます。") }<section class="container legacy-events"><h2>催しの一覧</h2>{"".join(event_row(e) for e in DATA["events"])}</section></main>'

def write(filename, title, builder, site=False):
    global CURRENT, SITE
    CURRENT, SITE = filename, site
    main = builder()
    if filename == 'culture-craft.html':
        main = main.replace('<section class="container culture-events">',painting_studio()+'<section class="container culture-events">')
    routes = {name: route(name) for name in ROUTES}
    paint_script = f'<script src="{asset("painting.js")}" defer></script>' if filename=='culture-craft.html' else ''
    body = f'''<!doctype html><html lang="ja" data-experience="hiraku" data-page="{filename}" data-asset-base="{asset('')}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | 愛顔えひめの文化祭2028・デザインPoC</title><meta name="description" content="愛媛を、ひらく。愛顔えひめの文化祭2028のデザインPoC。文化の背景、催し、参加の支援を一つの体験につなぎます。"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#f5f2ea"><link rel="stylesheet" href="{asset('experience.css')}"><script>window.EHIME_V2_ROUTES={json.dumps(routes,ensure_ascii=False,separators=(',',':'))};</script><script src="{asset('experience-data.js')}" defer></script><script src="{asset('experience.js')}" defer></script>{paint_script}</head><body>{header()}{main}{footer()}</body></html>\n'''
    destination = ROOT / ROUTES[filename] if site else LAB / filename
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(body)

def main():
    if TOKENS['version'] != DATA['version']:
        raise ValueError('Content and token versions differ')
    token_css = ':root{' + ''.join('--'+key+':'+value+';' for key,value in TOKENS['cssVariables'].items()) + '}\n'
    (LAB/'tokens.css').write_text('/* Generated by build_v2_experience.py from tokens.json. */\n'+token_css)
    css = (LAB/'experience.css').read_text()
    css, count = re.subn(r':root\{[^}]*\}',lambda _:token_css.rstrip(),css,count=1)
    if count != 1:
        raise ValueError('Expected one root token block')
    (LAB/'experience.css').write_text(css)
    pages = [('index.html','愛媛を、ひらく。',home)]
    pages += [('culture-'+c['id']+'.html',c['title'],lambda c=c:culture(c)) for c in DATA['cultures']]
    pages += [(e['page'],e['title'],lambda e=e:event(e)) for e in DATA['events']]
    pages += [
        ('event-search.html','催しを探す',search),('event-detail.html','催しの案内',legacy_detail),
        ('notebook.html','わたしの文化帖',notebook),('documents.html','実行委員会・資料',documents),
        ('participation.html','参加・募集',participation),('support.html','参加の支援',support),
        ('about.html','大会について',about),
    ]
    pages += [(kind+'.html',title,lambda kind=kind:simple_page(kind)) for kind,title in [('news','お知らせ'),('access','交通・アクセス'),('sponsors','協賛'),('privacy','データの扱い'),('components','共通部品')]]
    for name,title,builder in pages:
        write(name,title,builder)
        if name != 'components.html':
            write(name,title,builder,True)
    (LAB/'experience-data.js').write_text('window.EHIME_V2_DATA='+json.dumps(DATA,ensure_ascii=False,separators=(',',':'))+';\n')
    manifest = {'version':DATA['version'],'direction':'hiraku','pages':[name for name,_,_ in pages],'canonicalRoutes':ROUTES,'legacyV1Pages':'remain available; not yet all migrated','v1Frozen':'94df551e752129e45e7f21c3d38282d87c5690db'}
    (LAB/'experience-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    for old in ['home-a.html','home-b.html']:
        (LAB/old).write_text('<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url=index.html"><title>新しいデザインへ</title><p>A/B比較を終了しました。<a href="index.html">愛媛を、ひらく。</a>をご覧ください。</p></html>\n')
    print(json.dumps({'version':DATA['version'],'labPages':len(pages),'canonicalPages':len(pages)-1,'direction':'hiraku','routes':ROUTES},ensure_ascii=False))

if __name__ == '__main__':
    main()
