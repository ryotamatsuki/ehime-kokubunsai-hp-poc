from pathlib import Path
from textwrap import wrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ehime_kokubunsai_homepage_structure.pdf"

PAGE_W, PAGE_H = landscape(A3)
MARGIN = 11 * mm
FONT = "HeiseiKakuGo-W5"
FONT_MIN = "HeiseiMin-W3"


pdfmetrics.registerFont(UnicodeCIDFont(FONT))
pdfmetrics.registerFont(UnicodeCIDFont(FONT_MIN))


def fit_text(c, text, x, y, w, font=FONT, size=7.8, leading=9.4, max_lines=2, bold=False):
    c.setFont(font, size)
    avg = max(size * 0.58, 1)
    chars = max(1, int(w / avg))
    lines = []
    for part in str(text).split("\n"):
        lines.extend(wrap(part, chars) or [""])
    lines = lines[:max_lines]
    for i, line in enumerate(lines):
        c.drawString(x, y - i * leading, line)


def rect(c, x, y, w, h, label=None, sub=None, heavy=False, dashed=False, fill=colors.white):
    c.saveState()
    if dashed:
        c.setDash(3, 2)
    c.setStrokeColor(colors.black)
    c.setFillColor(fill)
    c.setLineWidth(1.4 if heavy else 0.65)
    c.rect(x, y, w, h, stroke=1, fill=1)
    c.restoreState()
    if label:
        c.setFillColor(colors.black)
        fit_text(c, label, x + 3.0 * mm, y + h - 5.2 * mm, w - 6 * mm, size=8.2, leading=9, max_lines=2)
    if sub:
        c.setFillColor(colors.Color(0.18, 0.18, 0.18))
        fit_text(c, sub, x + 3.0 * mm, y + 4.1 * mm, w - 6 * mm, size=6.2, leading=7, max_lines=2)


def header(c, title, meta):
    c.setLineWidth(1.2)
    c.line(MARGIN, PAGE_H - MARGIN - 10 * mm, PAGE_W - MARGIN, PAGE_H - MARGIN - 10 * mm)
    c.setFont(FONT, 16)
    c.drawCentredString(PAGE_W / 2, PAGE_H - MARGIN - 6.2 * mm, title)
    c.setFont(FONT, 7.4)
    for i, line in enumerate(meta.split("\n")):
        c.drawRightString(PAGE_W - MARGIN, PAGE_H - MARGIN - 2.5 * mm - i * 4 * mm, line)


def footer(c, page, label):
    c.setLineWidth(0.6)
    c.line(MARGIN, MARGIN + 5 * mm, PAGE_W - MARGIN, MARGIN + 5 * mm)
    c.setFont(FONT, 7.2)
    c.drawRightString(PAGE_W - MARGIN, MARGIN + 1.5 * mm, f"{page} / 4　{label}")


def section_title(c, x, y, w, no, title, count):
    c.setLineWidth(1.35)
    c.rect(x, y, w, 9 * mm, stroke=1, fill=0)
    c.setFont(FONT, 8.7)
    c.drawString(x + 2.2 * mm, y + 3.0 * mm, no)
    c.drawString(x + 11 * mm, y + 3.0 * mm, title)
    c.setFont(FONT, 6.7)
    c.drawRightString(x + w - 2.2 * mm, y + 3.15 * mm, count)


def draw_nodes(c, x, y, w, items, cols=2, row_h=12.5 * mm, gap=1.8 * mm):
    col_w = (w - gap * (cols - 1)) / cols
    for i, item in enumerate(items):
        col = i % cols
        row = i // cols
        xx = x + col * (col_w + gap)
        yy = y - row * (row_h + gap)
        label, sub, kind = item
        rect(
            c,
            xx,
            yy,
            col_w,
            row_h,
            label=label,
            sub=sub,
            heavy=kind == "key",
            dashed=kind == "draft",
            fill=colors.Color(0.965, 0.965, 0.965) if kind == "draft" else colors.white,
        )


def note(c, x, y, w, h, text):
    rect(c, x, y, w, h, fill=colors.Color(0.96, 0.96, 0.96))
    fit_text(c, text, x + 2.5 * mm, y + h - 4.8 * mm, w - 5 * mm, size=6.9, leading=8.0, max_lines=3)


def page1(c):
    header(c, "令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮） ホームページ基本構成（案）", "作成日 2026年4月27日\n対象：ehime-kokubunsai-hp")

    top = PAGE_H - MARGIN - 15 * mm
    rect(c, MARGIN, top - 16 * mm, 125 * mm, 16 * mm, "構成概要", "既存HTML 114ページを、トップページからグローバルナビ、補助ナビ、各カテゴリ下層へ展開する構成として整理。")
    rect(c, MARGIN + 130 * mm, top - 16 * mm, PAGE_W - 2 * MARGIN - 130 * mm, 16 * mm, "凡例", "太枠：主要導線　通常枠：通常ページ　点線枠：仮ページ・正式決定後更新　→：直接導線")

    grid_y = top - 28 * mm
    tier_w = 32 * mm
    gap = 2.2 * mm
    col_w = (PAGE_W - 2 * MARGIN - tier_w - gap * 4) / 4
    headers = ["第0階層", "第1階層", "第2階層", "第3階層", "共通機能"]
    xs = [MARGIN, MARGIN + tier_w + gap, MARGIN + tier_w + gap + col_w + gap, MARGIN + tier_w + gap + (col_w + gap) * 2, MARGIN + tier_w + gap + (col_w + gap) * 3]
    widths = [tier_w, col_w, col_w, col_w, col_w]
    for x, w, h in zip(xs, widths, headers):
        rect(c, x, grid_y, w, 8 * mm, h, heavy=False, fill=colors.Color(0.9, 0.9, 0.9))

    y0 = grid_y - 16 * mm
    rect(c, xs[0], y0, widths[0], 24 * mm, "トップページ", "index.html", heavy=True)

    cats = [
        ("01　大会とは", "about / 14ページ"),
        ("02　イベント情報", "events / 17ページ"),
        ("03　募集情報", "recruitment / 7ページ"),
        ("04　協賛・応援企業", "sponsors / 7ページ"),
        ("05　アクセス・観光", "access + tourism / 13ページ"),
        ("06　アクセシビリティ", "accessibility / 6ページ"),
        ("07　お知らせ", "news / 6ページ"),
        ("08　問い合わせ", "contact / 4ページ"),
    ]
    roles = [
        ("公式情報の確認", "大会名称、基本方針、会期、開催地、事業構成、主催者、ロゴ等"),
        ("探す・選ぶ", "カレンダー、市町別、ジャンル別、バリアフリー、予約、無料、親子向け等"),
        ("参加する", "出演・出品、ボランティア、応援事業、他県大会、協賛、入札"),
        ("支援・協力する", "協賛企業、寄付企業、協力企業、募集、関心表明、インタビュー"),
        ("来場する", "飛行機、電車、バス、車、フェリー、会場別アクセス、旅、宿泊、モデルコース"),
        ("誰もが使える", "情報保障、会場情報、イベント別対応、相談、やさしい日本語"),
        ("更新情報を見る", "重要、報道発表、募集、実行委員会、詳細記事"),
        ("問い合わせる", "フォーム、FAQ、問い合わせ先一覧、注意事項"),
    ]
    ops = [
        ("仮情報の扱い", "正式決定前は「仮」「未定」「正式決定後掲載」を明示", "draft"),
        ("ページ間導線", "カテゴリ内ナビ、関連ページ、CTA、検索導線", ""),
        ("資料・PDF導線", "要項、申込書、委員会資料、記録集、広報素材", ""),
        ("協賛LP調デザイン", "協賛関連は sponsor LP のトーンを継承", "draft"),
        ("画像・ビジュアル", "愛媛の風景、文化活動、工芸、舞台、人物を各ページに配置", ""),
        ("支援ツール", "文字サイズ、コントラスト、検索、言語、SNS", ""),
        ("緊急表示", "会期前・会期中の変更、中止、交通規制等を掲出", ""),
        ("運用窓口", "総合、募集、協賛、報道、アクセシビリティ別に案内", ""),
    ]
    common = [
        ("ヘッダー", "グローバルナビ、補助ナビ、検索フォーム", ""),
        ("重要なお知らせ帯", "全ページ共通表示", ""),
        ("サイト内検索", "search-index.js と common/search.html", "key"),
        ("フッター", "主要カテゴリ、問い合わせ、運用情報", ""),
        ("ポリシー", "個人情報、著作権、免責、リンク、SNS、SSL、UD", ""),
        ("会期後アーカイブ", "結果、写真、動画、成果報告、協賛、記録集", "draft"),
    ]

    row_h = 16.3 * mm
    for i, (label, sub) in enumerate(cats):
        rect(c, xs[1], y0 - i * (row_h + 1.5 * mm), widths[1], row_h, label, sub, heavy=True)
        c.setFont(FONT, 11)
        c.drawCentredString(xs[0] + widths[0] + gap / 2, y0 + row_h / 2 - 2 * mm - i * (row_h + 1.5 * mm), "→")
    for i, (label, sub) in enumerate(roles):
        rect(c, xs[2], y0 - i * (row_h + 1.5 * mm), widths[2], row_h, label, sub)
    for i, (label, sub, kind) in enumerate(ops):
        rect(c, xs[3], y0 - i * (row_h + 1.5 * mm), widths[3], row_h, label, sub, dashed=kind == "draft", fill=colors.Color(0.965, 0.965, 0.965) if kind == "draft" else colors.white)
    for i, (label, sub, kind) in enumerate(common):
        rect(c, xs[4], y0 - i * (row_h + 1.5 * mm), widths[4], row_h, label, sub, heavy=kind == "key", dashed=kind == "draft", fill=colors.Color(0.965, 0.965, 0.965) if kind == "draft" else colors.white)

    footer(c, 1, "全体構成・グローバル導線")


ABOUT = [
    ("愛媛大会（仮）とは", "about/index.html", "key"),
    ("国民文化祭とは", "about/kokubunsai.html", ""),
    ("全国障害者芸術・文化祭とは", "about/disability-arts-festival.html", ""),
    ("開催意義", "about/significance.html", ""),
    ("基本方針", "about/policy.html", ""),
    ("基本構想・実施計画", "about/plan.html", ""),
    ("事業構成", "about/programs.html", ""),
    ("会期・開催地", "about/schedule-venues.html", ""),
    ("大会名称", "about/name.html", "draft"),
    ("キャッチフレーズ", "about/catchphrase.html", "draft"),
    ("大会ロゴマーク", "about/logo.html", "draft"),
    ("マスコットキャラクター", "about/mascot.html", "draft"),
    ("主催者", "about/organizers.html", ""),
    ("各種ダウンロード", "about/downloads.html", ""),
]

EVENTS = [
    ("イベントカレンダー", "events/calendar.html", "key"),
    ("イベントカレンダー詳細", "events/calendar-detail.html", ""),
    ("検索結果一覧", "events/search.html", ""),
    ("イベント詳細ページ", "events/detail.html", ""),
    ("新着イベント情報一覧", "events/latest.html", ""),
    ("文化祭期間中のイベント", "events/during.html", ""),
    ("市町別イベント一覧", "events/by-city.html", ""),
    ("ジャンル別イベント一覧", "events/by-genre.html", ""),
    ("全国公募イベント情報", "events/open-call-info.html", ""),
    ("全国公募・募集イベント", "events/open-call.html", ""),
    ("障がい者芸術・文化関連イベント", "events/disability-art.html", ""),
    ("バリアフリー対応イベント一覧", "events/barrierfree.html", ""),
    ("子ども・親子向けイベント", "events/family.html", ""),
    ("無料イベント一覧", "events/free.html", ""),
    ("予約・申込が必要なイベント", "events/reservation.html", ""),
    ("各イベントの問い合わせ先", "events/event-contacts.html", ""),
    ("全般的な問い合わせ先", "events/general-contact.html", ""),
]

NEWS = [
    ("お知らせ一覧", "news/index.html", "key"),
    ("お知らせ詳細", "news/detail.html", ""),
    ("重要なお知らせ", "news/important.html", ""),
    ("報道発表", "news/press.html", ""),
    ("募集情報のお知らせ", "news/recruitment.html", ""),
    ("実行委員会からのお知らせ", "news/committee.html", ""),
]

COMMITTEE = [
    ("実行委員会概要", "committee/overview.html", "key"),
    ("基本構想検討会", "committee/concept-meeting.html", ""),
    ("基本構想", "committee/concept.html", ""),
    ("総会資料", "committee/general-assembly.html", ""),
    ("専門委員会・部会資料", "committee/committees.html", ""),
    ("実施計画", "committee/implementation-plan.html", ""),
    ("収支予算・事業計画", "committee/budget.html", ""),
]

COMMON = [
    ("重要なお知らせ表示", "common/important.html", ""),
    ("アクセシビリティ支援ツール", "common/accessibility-tool.html", ""),
    ("言語切替", "common/language.html", "draft"),
    ("SNSリンク", "common/sns.html", ""),
    ("サイト内検索", "common/search.html", "key"),
]


def page2(c):
    header(c, "第1階層から第2階層への展開（大会情報・イベント・お知らせ）", "ホームページ基本構成（案）\nページ一覧ベース")
    top = PAGE_H - MARGIN - 17 * mm
    gap = 4 * mm
    col_w = (PAGE_W - 2 * MARGIN - gap * 3) / 4
    xs = [MARGIN + i * (col_w + gap) for i in range(4)]

    section_title(c, xs[0], top, col_w, "01", "大会とは", "about / 14ページ")
    draw_nodes(c, xs[0], top - 14 * mm, col_w, ABOUT, cols=2, row_h=11.6 * mm)
    note(c, xs[0], MARGIN + 8 * mm, col_w, 14 * mm, "役割：大会の公式性・背景・未確定事項の扱いを明確化し、基礎情報群として整理。")

    section_title(c, xs[1], top, col_w, "02", "イベント情報", "events / 17ページ")
    draw_nodes(c, xs[1], top - 14 * mm, col_w, EVENTS, cols=2, row_h=10.1 * mm)
    note(c, xs[1], MARGIN + 8 * mm, col_w, 14 * mm, "役割：日時・地域・ジャンル・支援対応からイベントを探せる実用導線。")

    section_title(c, xs[2], top, col_w, "07", "お知らせ", "news / 6ページ")
    draw_nodes(c, xs[2], top - 14 * mm, col_w, NEWS, cols=2, row_h=12.5 * mm)
    section_title(c, xs[2], top - 94 * mm, col_w, "09", "実行委員会・会議資料", "committee / 7ページ")
    draw_nodes(c, xs[2], top - 108 * mm, col_w, COMMITTEE, cols=2, row_h=11.5 * mm)
    note(c, xs[2], MARGIN + 8 * mm, col_w, 14 * mm, "役割：公式発表・会議資料・透明性確保のための情報を集約。")

    section_title(c, xs[3], top, col_w, "共通", "補助ナビ・サイト機能", "common / 5ページ")
    draw_nodes(c, xs[3], top - 14 * mm, col_w, COMMON, cols=2, row_h=12.8 * mm)
    section_title(c, xs[3], top - 88 * mm, col_w, "10", "入札・契約情報", "bids / 1ページ")
    draw_nodes(c, xs[3], top - 102 * mm, col_w, [("入札・契約情報", "bids/index.html", "key")], cols=1, row_h=15 * mm)
    note(c, xs[3], MARGIN + 8 * mm, col_w, 14 * mm, "役割：閲覧支援、検索、SNS、重要情報など全ページ共通の入口を担う。")

    footer(c, 2, "大会情報・イベント・お知らせ・委員会資料")


RECRUIT = [
    ("募集情報一覧", "recruitment/index.html", "key"),
    ("出演・出品者募集", "recruitment/performers.html", ""),
    ("スタッフ・ボランティア募集", "recruitment/volunteer.html", ""),
    ("応援事業募集", "recruitment/support-projects.html", ""),
    ("他県大会への出演募集", "recruitment/other-pref.html", ""),
    ("応援企業・協賛企業募集", "recruitment/sponsors.html", "draft"),
    ("入札情報", "recruitment/bids.html", ""),
]

SPONSORS = [
    ("協賛・応援企業一覧", "sponsors/index.html", "key"),
    ("協賛企業一覧", "sponsors/sponsor-companies.html", ""),
    ("寄付企業一覧", "sponsors/donation-companies.html", ""),
    ("協力企業一覧", "sponsors/partner-companies.html", ""),
    ("協賛パートナー募集", "sponsors/partner-recruitment.html", "key"),
    ("関心表明フォーム", "sponsors/interest-form.html", "draft"),
    ("協賛企業インタビュー", "sponsors/interviews.html", "draft"),
]

PR = [
    ("広報活動一覧", "pr/index.html", "key"),
    ("広報大使・アンバサダー", "pr/ambassador.html", "draft"),
    ("広報素材ダウンロード", "pr/downloads.html", ""),
    ("SNSキャンペーン", "pr/sns-campaign.html", "draft"),
    ("市町・企業向け広報協力", "pr/cooperation.html", ""),
    ("PR動画", "pr/video.html", ""),
    ("PR動画 字幕・手話なし", "pr/video-standard.html", ""),
    ("PR動画 字幕・手話あり", "pr/video-accessible.html", ""),
]

MEDIA = [
    ("プレスリリース", "media/press.html", "key"),
    ("取材申込", "media/coverage.html", ""),
    ("写真・動画素材提供", "media/materials.html", ""),
    ("ロゴ・名称使用について", "media/logo-usage.html", ""),
    ("問い合わせ先", "media/contact.html", ""),
]

CONTACT = [
    ("メールフォーム", "contact/form.html", "key"),
    ("よくある質問", "contact/faq.html", ""),
    ("問い合わせ先一覧", "contact/contacts.html", ""),
    ("お問い合わせ注意事項", "contact/notes.html", ""),
]


def page3(c):
    header(c, "第1階層から第2階層への展開（募集・協賛・広報・報道）", "ホームページ基本構成（案）\n協賛関連はLP調のデザインを継承")
    top = PAGE_H - MARGIN - 17 * mm
    gap = 4 * mm
    col_w = (PAGE_W - 2 * MARGIN - gap * 3) / 4
    xs = [MARGIN + i * (col_w + gap) for i in range(4)]

    section_title(c, xs[0], top, col_w, "03", "募集情報", "recruitment / 7ページ")
    draw_nodes(c, xs[0], top - 14 * mm, col_w, RECRUIT, cols=2, row_h=13 * mm)
    note(c, xs[0], MARGIN + 8 * mm, col_w, 16 * mm, "役割：参加募集の入口。対象、期間、申込方法、要項、様式、問い合わせ先を整理。")

    section_title(c, xs[1], top, col_w, "04", "協賛・応援企業", "sponsors / 7ページ")
    draw_nodes(c, xs[1], top - 14 * mm, col_w, SPONSORS, cols=2, row_h=13 * mm)
    note(c, xs[1], MARGIN + 8 * mm, col_w, 16 * mm, "役割：協賛金、寄付、物品、サービス、広報協力を分けて案内。協賛LPのトーンを継承。")

    section_title(c, xs[2], top, col_w, "11", "広報活動", "pr / 8ページ")
    draw_nodes(c, xs[2], top - 14 * mm, col_w, PR, cols=2, row_h=12.2 * mm)
    note(c, xs[2], MARGIN + 8 * mm, col_w, 16 * mm, "役割：県民・市町・企業・報道が共通して使う広報素材を整理。")

    section_title(c, xs[3], top, col_w, "12", "報道・メディア向け", "media / 5ページ")
    draw_nodes(c, xs[3], top - 14 * mm, col_w, MEDIA, cols=2, row_h=13 * mm)
    section_title(c, xs[3], top - 91 * mm, col_w, "08", "問い合わせ", "contact / 4ページ")
    draw_nodes(c, xs[3], top - 105 * mm, col_w, CONTACT, cols=2, row_h=13 * mm)
    note(c, xs[3], MARGIN + 8 * mm, col_w, 16 * mm, "役割：報道対応と一般問い合わせを分離し、用途別の窓口を明示。")

    footer(c, 3, "募集・協賛・広報・報道・問い合わせ")


ACCESS = [
    ("会場別アクセス", "access/venues.html", "key"),
    ("飛行機でのアクセス", "access/flight.html", ""),
    ("電車でのアクセス", "access/train.html", ""),
    ("バスでのアクセス", "access/bus.html", ""),
    ("車でのアクセス", "access/car.html", ""),
    ("フェリーでのアクセス", "access/ferry.html", ""),
    ("バリアフリー交通情報", "access/barrierfree-transport.html", ""),
]

TOURISM = [
    ("愛媛への旅", "tourism/trip.html", "key"),
    ("宿泊案内", "tourism/lodging.html", ""),
    ("モデルコース", "tourism/courses.html", ""),
    ("食・土産・文化体験", "tourism/food-culture.html", ""),
    ("市町観光リンク集", "tourism/city-links.html", ""),
    ("トラベルセンター", "tourism/travel-center.html", "draft"),
]

A11Y = [
    ("情報保障について", "accessibility/information-support.html", "key"),
    ("会場バリアフリー情報", "accessibility/venue-barrierfree.html", ""),
    ("イベント別対応一覧", "accessibility/event-support.html", ""),
    ("参加・鑑賞時の配慮事項", "accessibility/participation.html", ""),
    ("相談窓口", "accessibility/consultation.html", ""),
    ("やさしい日本語ページ", "accessibility/easy-japanese.html", "draft"),
]

ARCHIVE = [
    ("開催結果概要", "archive/results.html", "draft"),
    ("写真ギャラリー", "archive/gallery.html", "draft"),
    ("動画アーカイブ", "archive/videos.html", "draft"),
    ("成果報告書", "archive/report.html", "draft"),
    ("協賛企業・団体一覧", "archive/sponsors.html", "draft"),
    ("記録集PDF", "archive/records.html", "draft"),
]

POLICY = [
    ("個人情報の取扱い", "policy/privacy.html", ""),
    ("著作権について", "policy/copyright.html", ""),
    ("免責事項", "policy/disclaimer.html", ""),
    ("リンクについて", "policy/links.html", ""),
    ("SNSアカウント運用方針", "policy/sns.html", ""),
    ("SSL・暗号化通信について", "policy/ssl.html", ""),
    ("ユニバーサルデザインについて", "policy/universal-design.html", ""),
]

INVENTORY = [
    ("about", "14", ""), ("events", "17", ""), ("recruitment", "7", ""),
    ("sponsors", "7", ""), ("access", "7", ""), ("tourism", "6", ""),
    ("accessibility", "6", ""), ("news", "6", ""), ("committee", "7", ""),
    ("pr", "8", ""), ("media", "5", ""), ("contact", "4", ""),
    ("common", "5", ""), ("policy", "7", ""), ("archive", "6", ""),
    ("bids", "1", ""), ("top", "1", ""),
]


def page4(c):
    header(c, "第1階層から第2階層への展開（来場・支援・アーカイブ・サイトポリシー）", "ホームページ基本構成（案）\n公開前から会期後までを想定")
    top = PAGE_H - MARGIN - 17 * mm
    gap = 5 * mm
    col_w = (PAGE_W - 2 * MARGIN - gap) / 2
    xs = [MARGIN, MARGIN + col_w + gap]

    section_title(c, xs[0], top, col_w, "05-A", "アクセス", "access / 7ページ")
    draw_nodes(c, xs[0], top - 14 * mm, col_w, ACCESS, cols=3, row_h=12.4 * mm)
    section_title(c, xs[0], top - 69 * mm, col_w, "05-B", "観光・宿泊", "tourism / 6ページ")
    draw_nodes(c, xs[0], top - 83 * mm, col_w, TOURISM, cols=3, row_h=12.4 * mm)

    section_title(c, xs[1], top, col_w, "06", "アクセシビリティ・バリアフリー", "accessibility / 6ページ")
    draw_nodes(c, xs[1], top - 14 * mm, col_w, A11Y, cols=3, row_h=12.4 * mm)
    section_title(c, xs[1], top - 69 * mm, col_w, "13", "会期後アーカイブ", "archive / 6ページ")
    draw_nodes(c, xs[1], top - 83 * mm, col_w, ARCHIVE, cols=3, row_h=12.4 * mm)

    bottom_top = top - 136 * mm
    section_title(c, xs[0], bottom_top, col_w, "14", "サイトポリシー", "policy / 7ページ")
    draw_nodes(c, xs[0], bottom_top - 14 * mm, col_w, POLICY, cols=3, row_h=12.4 * mm)

    section_title(c, xs[1], bottom_top, col_w, "一覧", "ページ数内訳", "HTML 114ページ")
    draw_nodes(c, xs[1], bottom_top - 14 * mm, col_w, INVENTORY, cols=6, row_h=11.2 * mm)
    note(c, xs[1], MARGIN + 8 * mm, col_w, 16 * mm, "運用方針：公開前は仮ページで完成イメージを示し、正式情報の確定後に本文、資料リンク、問い合わせ先、申込導線を差し替える。")

    footer(c, 4, "アクセス・観光・アクセシビリティ・アーカイブ・ポリシー")


def main():
    c = canvas.Canvas(str(OUT), pagesize=landscape(A3))
    c.setTitle("令和10年度 愛媛大会（仮） ホームページ基本構成（案）")
    for maker in (page1, page2, page3, page4):
        maker(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()