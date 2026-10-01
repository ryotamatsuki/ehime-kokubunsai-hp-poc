from __future__ import annotations

import html
import json
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parent


@dataclass
class Page:
    path: str
    title: str
    group: str
    summary: str
    status: str = "仮ページ"
    stage: str = "準備中"
    kind: str = "standard"
    tags: list[str] = field(default_factory=list)


GROUPS = {
    "home": {
        "label": "トップページ",
        "nav": "トップ",
        "path": "index.html",
        "description": "愛媛大会（仮）の世界観、主要導線、重要情報をまとめる入口です。",
        "image": "hero-ehime-culture-festival.jpg",
        "alt": "瀬戸内海を望む文化祭会場で、多世代の人々が芸能と工芸を楽しむ様子",
        "accent": "文化祭の世界観",
    },
    "common": {
        "label": "共通機能",
        "nav": "共通機能",
        "path": "common/search.html",
        "description": "検索、重要なお知らせ、アクセシビリティ支援など、全ページ共通の機能群です。",
        "image": "media-archive-workspace.jpg",
        "alt": "文化資料と端末が整えられた情報整理の作業卓",
        "accent": "迷わず使える導線",
    },
    "about": {
        "label": "愛媛大会（仮）とは",
        "nav": "大会とは",
        "path": "about/index.html",
        "description": "大会の意義、基本方針、国民文化祭と全国障害者芸術・文化祭の概要を伝えます。",
        "image": "culture-participation-workshop.jpg",
        "alt": "工芸や書を囲み、多世代の人々が文化活動に参加する様子",
        "accent": "愛媛で開く意味",
    },
    "news": {
        "label": "お知らせ",
        "nav": "お知らせ",
        "path": "news/index.html",
        "description": "重要なお知らせ、募集、報道発表、実行委員会からの案内を整理します。",
        "image": "media-archive-workspace.jpg",
        "alt": "広報資料や写真素材を整理する机上",
        "accent": "必要な情報をすぐに",
    },
    "events": {
        "label": "イベント情報",
        "nav": "イベント",
        "path": "events/calendar.html",
        "description": "日付、市町、ジャンル、バリアフリー対応などでイベントを探せるポータルです。",
        "image": "event-stage-lanterns.jpg",
        "alt": "海辺の屋外ステージで文化公演を楽しむ観客",
        "accent": "行きたい催しを探す",
    },
    "recruitment": {
        "label": "募集情報",
        "nav": "募集",
        "path": "recruitment/index.html",
        "description": "出演・出品、ボランティア、応援事業、入札など、参加の入口をまとめます。",
        "image": "culture-participation-workshop.jpg",
        "alt": "文化活動に参加する人々の手元と表情",
        "accent": "参加する",
    },
    "pr": {
        "label": "広報活動",
        "nav": "広報",
        "path": "pr/index.html",
        "description": "PR動画、広報素材、SNSキャンペーン、市町・企業向け広報協力を扱います。",
        "image": "media-archive-workspace.jpg",
        "alt": "写真・映像・印刷物などの広報素材を整理する様子",
        "accent": "伝える力をそろえる",
    },
    "sponsors": {
        "label": "協賛・応援企業",
        "nav": "協賛",
        "path": "sponsors/index.html",
        "description": "協賛、寄付、物品・サービス協力、関心表明の入口を設けます。",
        "image": "hero-ehime-culture-festival.jpg",
        "alt": "愛媛の文化祭を支える人々と海辺の会場",
        "accent": "企業と文化をつなぐ",
    },
    "tourism": {
        "label": "観光・周遊案内（仮）",
        "nav": "アクセス・観光",
        "path": "tourism/trip.html",
        "description": "県外来訪者や県内周遊者に向け、文化祭と愛媛観光を結びます。",
        "image": "ehime-travel-landscape.jpg",
        "alt": "瀬戸内海、島々、山並み、柑橘が重なる愛媛の風景",
        "accent": "文化と旅を結ぶ",
    },
    "contact": {
        "label": "お問い合わせ",
        "nav": "問い合わせ",
        "path": "contact/form.html",
        "description": "問い合わせ分類ごとに、適切な窓口とフォームへ誘導します。",
        "image": "media-archive-workspace.jpg",
        "alt": "問い合わせ資料と端末が整った明るい作業机",
        "accent": "迷わず相談する",
    },
    "access": {
        "label": "アクセス",
        "nav": "アクセス",
        "path": "access/flight.html",
        "description": "飛行機、電車、車、フェリー、バス、会場別アクセスを案内します。",
        "image": "ehime-travel-landscape.jpg",
        "alt": "海と島々を結ぶ愛媛の交通と風景",
        "accent": "会場へ向かう",
    },
    "accessibility": {
        "label": "アクセシビリティ・バリアフリー情報",
        "nav": "バリアフリー",
        "path": "accessibility/information-support.html",
        "description": "情報保障、会場バリアフリー、イベント別対応、相談窓口を整理します。",
        "image": "hero-ehime-culture-festival.jpg",
        "alt": "車椅子利用者を含む観客が文化公演に参加する様子",
        "accent": "誰もが参加できる",
    },
    "media": {
        "label": "報道・メディア向け",
        "nav": "報道",
        "path": "media/press.html",
        "description": "プレスリリース、取材申込、写真・動画素材、ロゴ使用を案内します。",
        "image": "media-archive-workspace.jpg",
        "alt": "写真・映像素材と広報資料を整理する机上",
        "accent": "正確に伝える",
    },
    "committee": {
        "label": "実行委員会・会議資料",
        "nav": "会議資料",
        "path": "committee/overview.html",
        "description": "実行委員会の体制、会議資料、基本構想、実施計画を公開します。",
        "image": "media-archive-workspace.jpg",
        "alt": "会議資料と記録写真を整理する公式資料の作業卓",
        "accent": "透明性を保つ",
    },
    "policy": {
        "label": "サイトポリシー",
        "nav": "ポリシー",
        "path": "policy/privacy.html",
        "description": "個人情報、著作権、免責事項、リンク、アクセシビリティ方針を示します。",
        "image": "media-archive-workspace.jpg",
        "alt": "公的文書と端末が整然と置かれた机",
        "accent": "安心して使う",
    },
    "archive": {
        "label": "会期後アーカイブ",
        "nav": "アーカイブ",
        "path": "archive/results.html",
        "description": "開催結果、写真、動画、記録集、協賛企業などを会期後に残します。",
        "image": "event-stage-lanterns.jpg",
        "alt": "夜の文化公演と観客の記録的な情景",
        "accent": "成果を未来へ残す",
    },
}


PAGES: list[Page] = []


def add(path: str, title: str, group: str, summary: str, **kwargs: object) -> None:
    PAGES.append(Page(path=path, title=title, group=group, summary=summary, **kwargs))


add(
    "index.html",
    "令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）",
    "home",
    "愛媛県で開催予定の国民文化祭・全国障害者芸術・文化祭の公式ホームページ案です。",
    status="未確定事項あり",
    stage="準備初期",
    kind="home",
    tags=["トップ", "大会概要", "イベント", "募集", "協賛", "アクセシビリティ"],
)

COMMON_PAGES = [
    ("common/accessibility-tool.html", "アクセシビリティ支援ツール", "文字サイズ、コントラスト、本文移動などの支援機能を想定した共通ページです。", "tool"),
    ("common/search.html", "サイト内検索", "ページ名、目的、タグから必要な情報を探すための検索ページです。", "search"),
    ("common/language.html", "言語切替（仮）", "多言語対応の範囲が決まるまで、やさしい日本語と主要情報への仮導線を置きます。", "language"),
    ("common/sns.html", "SNSリンク", "公式SNSアカウント決定後に掲載するリンク集の仮ページです。", "sns"),
    ("common/important.html", "重要なお知らせ表示", "会期前・会期中の緊急情報や重要案内を掲出するページです。", "important"),
]

ABOUT_PAGES = [
    ("about/index.html", "愛媛大会（仮）とは", "大会の目的、位置付け、愛媛らしさ、準備段階の考え方をまとめます。", "overview"),
    ("about/significance.html", "開催意義", "愛媛で全国規模の文化の祭典を開く意義を、文化・観光・共生社会の視点で伝えます。", "about"),
    ("about/policy.html", "基本方針", "公式性、来場者の使いやすさ、アクセシビリティ、愛媛らしさを軸にした方針を掲載します。", "about"),
    ("about/name.html", "大会名称", "正式名称・統一名称が決定するまで、仮名称と決定後の掲載方針を示します。", "placeholder"),
    ("about/catchphrase.html", "キャッチフレーズ", "キャッチフレーズ決定前の仮ページとして、掲載位置と使い方のイメージを示します。", "placeholder"),
    ("about/logo.html", "大会ロゴマーク", "公式ロゴ決定後の掲載・ダウンロード・使用条件のイメージを示します。", "downloads"),
    ("about/mascot.html", "マスコットキャラクター", "マスコット決定後にプロフィール、使用ルール、素材を掲載する想定ページです。", "placeholder"),
    ("about/organizers.html", "主催者", "主催者・実行委員会・関係団体を正式決定後に掲載するページです。", "standard"),
    ("about/schedule-venues.html", "会期・開催地", "会期、開催市町、主要会場を正式決定後に掲載するページです。", "standard"),
    ("about/programs.html", "事業構成", "実施計画策定後、主催事業・市町事業・協賛事業等を整理します。", "listing"),
    ("about/kokubunsai.html", "国民文化祭とは", "国民文化祭の趣旨と、愛媛大会（仮）との関係を分かりやすく紹介します。", "standard"),
    ("about/disability-arts-festival.html", "全国障害者芸術・文化祭とは", "全国障害者芸術・文化祭との一体開催の意味を紹介します。", "standard"),
    ("about/plan.html", "基本構想・実施計画", "基本構想、実施計画、関連資料への導線をまとめます。", "downloads"),
    ("about/downloads.html", "各種ダウンロード", "大会概要資料、基本構想、広報素材などのダウンロード導線を置きます。", "downloads"),
]

NEWS_PAGES = [
    ("news/index.html", "お知らせ一覧", "大会準備、イベント、募集、資料公開などのお知らせを一覧で掲載します。", "news-list"),
    ("news/detail.html", "お知らせ詳細", "個別のお知らせの見出し、本文、更新日、問い合わせ先を掲載する詳細ページ例です。", "news-detail"),
    ("news/important.html", "重要なお知らせ", "会期前・会期中の重要情報、変更・中止、緊急連絡を分かりやすく掲載します。", "important"),
    ("news/recruitment.html", "募集情報のお知らせ", "出演・出品、ボランティア、応援事業、入札など募集関連の案内を集約します。", "news-list"),
    ("news/press.html", "報道発表", "報道発表資料、発表日、問い合わせ先、関連資料への導線を掲載します。", "downloads"),
    ("news/committee.html", "実行委員会からのお知らせ", "会議開催、資料公開、方針決定など実行委員会からの案内を掲載します。", "news-list"),
]

EVENT_PAGES = [
    ("events/calendar.html", "イベントカレンダー", "日付、市町、ジャンル、バリアフリー対応などでイベントを探す一覧ページです。", "events"),
    ("events/calendar-detail.html", "イベントカレンダー詳細", "日別・月別のイベント表示や、当日の注意事項を掲載する詳細ページ例です。", "event-detail"),
    ("events/search.html", "検索結果一覧", "イベント検索の条件と結果を表示するページです。", "events"),
    ("events/during.html", "文化祭期間中のイベント", "会期中に開催される主催事業・市町事業等の入口です。", "events"),
    ("events/by-city.html", "市町別イベント一覧", "市町ごとにイベントを探せるページです。", "events"),
    ("events/by-genre.html", "ジャンル別イベント一覧", "音楽、舞台、工芸、食文化、文学などのジャンル別一覧です。", "events"),
    ("events/barrierfree.html", "バリアフリー対応イベント一覧", "車椅子席、手話通訳、字幕等の対応があるイベントを探せます。", "events"),
    ("events/family.html", "子ども・親子向けイベント", "子どもや親子で参加しやすい催しを集約します。", "events"),
    ("events/disability-art.html", "障がい者芸術・文化関連イベント", "障がい者芸術・文化に関する展示、公演、交流事業を掲載します。", "events"),
    ("events/free.html", "無料イベント一覧", "無料で参加・鑑賞できるイベントを掲載します。", "events"),
    ("events/reservation.html", "予約・申込が必要なイベント", "予約、事前申込、抽選が必要なイベントを掲載します。", "events"),
    ("events/open-call.html", "全国公募・募集を行うイベント", "全国から出演・出品等を募集するイベントの入口です。", "events"),
    ("events/open-call-info.html", "全国公募イベント情報", "公募イベントの募集要項、期間、申込方法を掲載します。", "downloads"),
    ("events/event-contacts.html", "各イベントの問い合わせ先", "イベントごとの担当窓口、主催者、問い合わせ先を整理します。", "contact-list"),
    ("events/general-contact.html", "全般的な問い合わせ先", "イベント全般に関する問い合わせ先を掲載します。", "contact-list"),
    ("events/latest.html", "新着イベント情報一覧", "追加・更新されたイベントを時系列で掲載します。", "events"),
    ("events/detail.html", "イベント詳細ページ", "イベント名、日時、会場、予約、バリアフリー対応、問い合わせ先を掲載する詳細ページ例です。", "event-detail"),
]

RECRUITMENT_PAGES = [
    ("recruitment/index.html", "募集情報一覧", "出演・出品者、ボランティア、応援事業、協賛企業、入札情報を一覧で掲載します。", "listing"),
    ("recruitment/performers.html", "出演・出品者募集", "出演者・出品者の募集要項、申込方法、締切、問い合わせ先を掲載します。", "downloads"),
    ("recruitment/volunteer.html", "スタッフ・ボランティア募集", "大会を支えるスタッフ・ボランティアの募集情報を掲載します。", "form"),
    ("recruitment/support-projects.html", "応援事業募集", "地域や団体が大会を盛り上げる応援事業の申請情報を掲載します。", "downloads"),
    ("recruitment/other-pref.html", "他県大会への出演募集", "他県開催大会への出演募集など関連募集を掲載します。", "listing"),
    ("recruitment/sponsors.html", "応援企業・協賛企業募集", "企業・団体向けの協賛、寄付、広報協力の募集情報へ誘導します。", "form"),
    ("recruitment/bids.html", "入札情報", "大会関連業務の入札・公募情報を掲載します。", "bid"),
]

PR_PAGES = [
    ("pr/index.html", "広報活動一覧", "PR動画、広報素材、SNS、アンバサダー、市町・企業向け協力を一覧にします。", "listing"),
    ("pr/video.html", "PR動画", "大会の魅力を伝えるPR動画の掲載ページです。", "video"),
    ("pr/video-accessible.html", "PR動画 字幕・手話あり", "字幕・手話付きPR動画の掲載を想定したページです。", "video"),
    ("pr/video-standard.html", "PR動画 字幕・手話なし", "通常版PR動画の掲載を想定したページです。", "video"),
    ("pr/ambassador.html", "広報大使・アンバサダー（仮）", "広報大使が決定後にプロフィールや活動予定を掲載します。", "placeholder"),
    ("pr/sns-campaign.html", "SNSキャンペーン（仮）", "SNSキャンペーン実施時の応募方法や注意事項を掲載します。", "sns"),
    ("pr/downloads.html", "広報素材ダウンロード", "ポスター、チラシ、バナー、SNS画像、写真素材等を掲載します。", "downloads"),
    ("pr/cooperation.html", "市町・企業向け広報協力のお願い", "掲示、配架、SNS発信、広報紙掲載などの協力依頼を掲載します。", "standard"),
]

SPONSOR_PAGES = [
    ("sponsors/index.html", "協賛・応援企業一覧", "協賛、寄付、協力企業・団体の総合一覧です。", "sponsor-list"),
    ("sponsors/sponsor-companies.html", "協賛企業一覧", "協賛金提供企業を正式な掲載順に沿って紹介します。", "sponsor-list"),
    ("sponsors/donation-companies.html", "寄付企業一覧", "寄付企業・団体の情報を掲載します。", "sponsor-list"),
    ("sponsors/partner-companies.html", "協力企業一覧", "物品、サービス、広報協力企業を掲載します。", "sponsor-list"),
    ("sponsors/partner-recruitment.html", "協賛パートナー募集", "協賛の趣旨、種類、特典、申込方法を掲載する募集ページです。", "sponsor-form"),
    ("sponsors/interest-form.html", "関心表明フォーム（仮）", "正式募集前の企業・団体向け関心表明フォームです。", "form"),
    ("sponsors/interviews.html", "協賛企業インタビュー（仮）", "協賛企業の地域貢献や文化支援の取組を紹介するページです。", "listing"),
]

TOURISM_PAGES = [
    ("tourism/trip.html", "愛媛への旅", "愛媛県の文化、自然、まち、食を概観し、来訪者を周遊へ誘導します。", "tourism"),
    ("tourism/courses.html", "モデルコース", "イベントと観光地を組み合わせた周遊ルート例を掲載します。", "tourism"),
    ("tourism/lodging.html", "宿泊案内", "宿泊情報、外部観光サイト、交通拠点への導線を掲載します。", "tourism"),
    ("tourism/food-culture.html", "食・土産・文化体験", "鯛めし、柑橘、砥部焼、今治タオルなどを紹介します。", "tourism"),
    ("tourism/travel-center.html", "トラベルセンター（仮）", "必要に応じて設置する旅行相談・案内窓口の仮ページです。", "placeholder"),
    ("tourism/city-links.html", "市町観光リンク集", "県内市町の観光サイトや関連リンクをまとめます。", "links"),
]

CONTACT_PAGES = [
    ("contact/form.html", "メールフォーム", "問い合わせ分類を選び、必要事項を入力するフォームの仮ページです。", "contact-form"),
    ("contact/notes.html", "お問い合わせ注意事項", "回答に時間を要する場合や個人情報の扱いなど、事前確認事項を掲載します。", "standard"),
    ("contact/contacts.html", "問い合わせ先一覧", "大会全般、イベント、募集、協賛、報道、アクセシビリティ等の窓口を整理します。", "contact-list"),
    ("contact/faq.html", "よくある質問", "準備段階から想定される質問と回答を掲載します。", "faq"),
]

ACCESS_PAGES = [
    ("access/flight.html", "飛行機でのアクセス", "松山空港など空路での来訪導線を掲載します。", "access"),
    ("access/train.html", "電車でのアクセス", "JR、伊予鉄道など鉄道での移動情報を掲載します。", "access"),
    ("access/car.html", "車でのアクセス", "高速道路、駐車場、交通規制の情報を掲載します。", "access"),
    ("access/ferry.html", "フェリーでのアクセス", "松山観光港、三津浜港、八幡浜港、東予港等の情報を掲載します。", "access"),
    ("access/bus.html", "バスでのアクセス", "高速バス、路線バス、シャトルバス（仮）情報を掲載します。", "access"),
    ("access/venues.html", "会場別アクセス", "各会場の所在地、最寄り交通、地図、注意事項を掲載します。", "access"),
    ("access/barrierfree-transport.html", "バリアフリー交通情報", "車椅子対応、福祉車両、駅・港・空港の配慮情報を掲載します。", "accessibility"),
]

ACCESSIBILITY_PAGES = [
    ("accessibility/information-support.html", "情報保障について", "手話、字幕、要約筆記、音声ガイド等の情報保障を説明します。", "accessibility"),
    ("accessibility/venue-barrierfree.html", "会場バリアフリー情報", "車椅子席、多目的トイレ、段差、休憩場所等を掲載します。", "accessibility"),
    ("accessibility/event-support.html", "イベント別対応一覧", "イベントごとのバリアフリー・情報保障対応を一覧にします。", "events"),
    ("accessibility/participation.html", "参加・鑑賞時の配慮事項", "介助者、休憩スペース、感覚過敏への配慮等を掲載します。", "accessibility"),
    ("accessibility/consultation.html", "相談窓口", "アクセシビリティに関する相談・問い合わせ先を掲載します。", "contact-form"),
    ("accessibility/easy-japanese.html", "やさしい日本語ページ（仮）", "主要情報をやさしい日本語で掲載する仮ページです。", "easy"),
]

MEDIA_PAGES = [
    ("media/press.html", "プレスリリース", "報道発表資料と関連資料を掲載します。", "downloads"),
    ("media/coverage.html", "取材申込", "取材申込フォーム、注意事項、受付条件を掲載します。", "form"),
    ("media/materials.html", "写真・動画素材提供", "使用条件付きの写真・動画素材を掲載します。", "downloads"),
    ("media/logo-usage.html", "ロゴ・名称使用について", "ロゴ、名称、キービジュアル等の使用規程を掲載します。", "policy"),
    ("media/contact.html", "問い合わせ先", "報道対応窓口、受付時間、取材時の連絡先を掲載します。", "contact-list"),
]

COMMITTEE_PAGES = [
    ("committee/overview.html", "実行委員会概要", "組織体制、規約、役割分担を掲載します。", "standard"),
    ("committee/general-assembly.html", "総会資料", "総会の議事次第、資料、議事概要を掲載します。", "downloads"),
    ("committee/committees.html", "専門委員会・部会資料", "各専門委員会・部会の資料を掲載します。", "downloads"),
    ("committee/concept-meeting.html", "基本構想検討会", "基本構想検討会の資料、議事概要を掲載します。", "downloads"),
    ("committee/concept.html", "基本構想", "基本構想PDFとHTML要約を掲載します。", "downloads"),
    ("committee/implementation-plan.html", "実施計画", "実施計画策定後に掲載する仮ページです。", "downloads"),
    ("committee/budget.html", "収支予算・事業計画", "公表範囲に応じて予算、事業計画を掲載します。", "downloads"),
]

BID_PAGE = Page(
    "bids/index.html",
    "入札・契約情報",
    "bids",
    "大会関連業務の入札・公募・契約情報を適切に公開します。",
    status="仮ページ",
    stage="実施計画策定期",
    kind="bid",
    tags=["入札", "契約", "公募", "仕様書"],
)
GROUPS["bids"] = {
    "label": "入札・契約情報",
    "nav": "入札",
    "path": "bids/index.html",
    "description": "入札公告、仕様書、質問回答、選定結果、契約結果を公開します。",
    "image": "media-archive-workspace.jpg",
    "alt": "仕様書や契約資料を整理する作業卓",
    "accent": "公平に公開する",
}

POLICY_PAGES = [
    ("policy/privacy.html", "個人情報の取扱い", "個人情報の利用目的、管理、問い合わせ先を示します。", "policy"),
    ("policy/ssl.html", "SSL・暗号化通信について", "フォーム送信時等の通信保護方針を掲載します。", "policy"),
    ("policy/universal-design.html", "ユニバーサルデザインについて", "アクセシビリティ方針と今後の改善方針を掲載します。", "policy"),
    ("policy/sns.html", "SNSアカウント運用方針", "公式SNSの運用ルール、免責事項、返信方針を掲載します。", "policy"),
    ("policy/copyright.html", "著作権について", "写真、動画、ロゴ、文章等の権利と使用制限を掲載します。", "policy"),
    ("policy/disclaimer.html", "免責事項", "外部リンク、情報変更、利用環境等の免責事項を掲載します。", "policy"),
    ("policy/links.html", "リンクについて", "リンク可否、バナー利用、リンク時の注意事項を掲載します。", "policy"),
]

ARCHIVE_PAGES = [
    ("archive/results.html", "開催結果概要", "会期後に参加者数、来場者数、実施イベント数等を掲載します。", "archive"),
    ("archive/gallery.html", "写真ギャラリー", "会期後に写真ギャラリーを公開するページです。", "gallery"),
    ("archive/videos.html", "動画アーカイブ", "PR動画、記録映像、配信アーカイブ等を掲載します。", "video"),
    ("archive/report.html", "成果報告書", "成果報告書とHTML要約を掲載します。", "downloads"),
    ("archive/sponsors.html", "協賛企業・団体一覧", "会期後に協賛企業・団体の一覧をアーカイブします。", "sponsor-list"),
    ("archive/records.html", "記録集PDF", "記録集PDF、関連資料、次世代への継承メッセージを掲載します。", "downloads"),
]

for path, title, summary, kind in COMMON_PAGES:
    add(path, title, "common", summary, kind=kind, tags=["共通機能", title])
for path, title, summary, kind in ABOUT_PAGES:
    add(path, title, "about", summary, kind=kind, tags=["大会概要", title])
for path, title, summary, kind in NEWS_PAGES:
    add(path, title, "news", summary, kind=kind, tags=["お知らせ", title])
for path, title, summary, kind in EVENT_PAGES:
    add(path, title, "events", summary, kind=kind, tags=["イベント", title])
for path, title, summary, kind in RECRUITMENT_PAGES:
    add(path, title, "recruitment", summary, kind=kind, tags=["募集", title])
for path, title, summary, kind in PR_PAGES:
    add(path, title, "pr", summary, kind=kind, tags=["広報", title])
for path, title, summary, kind in SPONSOR_PAGES:
    add(path, title, "sponsors", summary, kind=kind, tags=["協賛", "応援企業", title])
for path, title, summary, kind in TOURISM_PAGES:
    add(path, title, "tourism", summary, kind=kind, tags=["観光", "周遊", title])
for path, title, summary, kind in CONTACT_PAGES:
    add(path, title, "contact", summary, kind=kind, tags=["お問い合わせ", title])
for path, title, summary, kind in ACCESS_PAGES:
    add(path, title, "access", summary, kind=kind, tags=["アクセス", "交通", title])
for path, title, summary, kind in ACCESSIBILITY_PAGES:
    add(path, title, "accessibility", summary, kind=kind, tags=["アクセシビリティ", "バリアフリー", title])
for path, title, summary, kind in MEDIA_PAGES:
    add(path, title, "media", summary, kind=kind, tags=["報道", "メディア", title])
for path, title, summary, kind in COMMITTEE_PAGES:
    add(path, title, "committee", summary, kind=kind, tags=["実行委員会", "会議資料", title])
PAGES.append(BID_PAGE)
for path, title, summary, kind in POLICY_PAGES:
    add(path, title, "policy", summary, kind=kind, tags=["サイトポリシー", title])
for path, title, summary, kind in ARCHIVE_PAGES:
    add(path, title, "archive", summary, kind=kind, tags=["アーカイブ", title])


TOP_NAV = [
    "about",
    "events",
    "recruitment",
    "sponsors",
    "tourism",
    "accessibility",
    "news",
    "contact",
]

IMAGE_META = {
    "hero-ehime-culture-festival.jpg": "瀬戸内海を望む文化祭会場で、多世代の人々が芸能と工芸を楽しむ様子",
    "culture-participation-workshop.jpg": "文化活動に参加する人々の手元と表情",
    "ehime-travel-landscape.jpg": "瀬戸内海、島々、山並みが重なる愛媛の風景",
    "event-stage-lanterns.jpg": "海辺の屋外ステージで文化公演を楽しむ観客",
    "media-archive-workspace.jpg": "文化資料と端末が整えられた情報整理の作業卓",
    "dogo-onsen-night.jpg": "道後温泉を思わせる温かな夜のまちなみと来訪者",
    "shimanami-cycling.jpg": "しまなみ海道を思わせる橋と海、サイクリングを楽しむ人々",
    "ishizuchi-mountain.jpg": "石鎚山を思わせる山並みと展望地を訪れる人々",
    "uchiko-ozu-townscape.jpg": "内子・大洲を思わせる歴史的な町並みと文化体験",
    "uwajima-sea-culture.jpg": "宇和海を望む港町で食文化と工芸に触れる人々",
    "tobe-ceramics-workshop.jpg": "砥部焼を思わせる陶芸工房で制作体験をする人々",
    "inclusive-art-gallery.jpg": "バリアフリーに配慮したギャラリーで作品を鑑賞する人々",
    "volunteer-information-desk.jpg": "文化祭の案内デスクで来場者を支えるボランティア",
    "sponsor-partnership.jpg": "海を望むラウンジで文化祭協賛について相談する企業担当者と運営者",
    "press-media-room.jpg": "報道資料、写真、映像素材を整理するメディア対応の作業風景",
    "transport-access-hub.jpg": "空港、駅、港をつなぐ交通案内拠点を思わせる明るい空間",
    "family-culture-workshop.jpg": "親子や多世代が文化体験ワークショップに参加する様子",
    "archive-digital-gallery.jpg": "会期後の写真や記録を整理するデジタルアーカイブの作業風景",
}

GROUP_IMAGE_SETS = {
    "home": ["hero-ehime-culture-festival.jpg", "shimanami-cycling.jpg", "inclusive-art-gallery.jpg"],
    "common": ["media-archive-workspace.jpg", "press-media-room.jpg", "volunteer-information-desk.jpg"],
    "about": ["hero-ehime-culture-festival.jpg", "ishizuchi-mountain.jpg", "tobe-ceramics-workshop.jpg"],
    "news": ["press-media-room.jpg", "media-archive-workspace.jpg", "archive-digital-gallery.jpg"],
    "events": ["event-stage-lanterns.jpg", "family-culture-workshop.jpg", "tobe-ceramics-workshop.jpg"],
    "recruitment": ["volunteer-information-desk.jpg", "family-culture-workshop.jpg", "culture-participation-workshop.jpg"],
    "pr": ["press-media-room.jpg", "hero-ehime-culture-festival.jpg", "archive-digital-gallery.jpg"],
    "sponsors": ["sponsor-partnership.jpg", "hero-ehime-culture-festival.jpg", "media-archive-workspace.jpg"],
    "tourism": ["shimanami-cycling.jpg", "dogo-onsen-night.jpg", "uwajima-sea-culture.jpg"],
    "contact": ["volunteer-information-desk.jpg", "media-archive-workspace.jpg", "transport-access-hub.jpg"],
    "access": ["transport-access-hub.jpg", "shimanami-cycling.jpg", "ehime-travel-landscape.jpg"],
    "accessibility": ["inclusive-art-gallery.jpg", "volunteer-information-desk.jpg", "family-culture-workshop.jpg"],
    "media": ["press-media-room.jpg", "archive-digital-gallery.jpg", "hero-ehime-culture-festival.jpg"],
    "committee": ["media-archive-workspace.jpg", "press-media-room.jpg", "archive-digital-gallery.jpg"],
    "bids": ["media-archive-workspace.jpg", "press-media-room.jpg", "transport-access-hub.jpg"],
    "policy": ["media-archive-workspace.jpg", "inclusive-art-gallery.jpg", "press-media-room.jpg"],
    "archive": ["archive-digital-gallery.jpg", "event-stage-lanterns.jpg", "inclusive-art-gallery.jpg"],
}

PAGE_IMAGE_OVERRIDES = {
    "about/significance.html": "ishizuchi-mountain.jpg",
    "about/schedule-venues.html": "ehime-travel-landscape.jpg",
    "about/mascot.html": "family-culture-workshop.jpg",
    "events/family.html": "family-culture-workshop.jpg",
    "events/disability-art.html": "inclusive-art-gallery.jpg",
    "events/by-city.html": "shimanami-cycling.jpg",
    "events/by-genre.html": "tobe-ceramics-workshop.jpg",
    "recruitment/volunteer.html": "volunteer-information-desk.jpg",
    "recruitment/sponsors.html": "sponsor-partnership.jpg",
    "sponsors/partner-recruitment.html": "sponsor-partnership.jpg",
    "sponsors/interest-form.html": "sponsor-partnership.jpg",
    "sponsors/interviews.html": "sponsor-partnership.jpg",
    "tourism/trip.html": "shimanami-cycling.jpg",
    "tourism/courses.html": "dogo-onsen-night.jpg",
    "tourism/food-culture.html": "uwajima-sea-culture.jpg",
    "tourism/city-links.html": "ehime-travel-landscape.jpg",
    "access/flight.html": "transport-access-hub.jpg",
    "access/ferry.html": "uwajima-sea-culture.jpg",
    "access/barrierfree-transport.html": "inclusive-art-gallery.jpg",
    "accessibility/information-support.html": "inclusive-art-gallery.jpg",
    "accessibility/venue-barrierfree.html": "inclusive-art-gallery.jpg",
    "media/press.html": "press-media-room.jpg",
    "archive/gallery.html": "archive-digital-gallery.jpg",
}

OFFICIAL_SOURCES = {
    "ehime_notice": ("愛媛県庁：国民文化祭愛媛開催の内定について", "https://www.pref.ehime.jp/page/100937.html"),
    "ehime_concept": ("愛媛県庁：令和10年度国民文化祭等基本構想検討会", "https://www.pref.ehime.jp/page/119263.html"),
    "ehime_office": ("愛媛県庁：国民文化祭推進室", "https://www.pref.ehime.jp/soshiki/286/"),
    "bunka_kokubunsai": ("文化庁：国民文化祭", "https://www.bunka.go.jp/seisaku/geijutsubunka/chiiki/kokubunsai/"),
    "iyokannet": ("愛媛県公式観光サイト いよ観ネット", "https://www.iyokannet.jp/"),
    "matsuyama_castle": ("いよ観ネット：松山城", "https://www.iyokannet.jp/spot/320/"),
    "dogo": ("いよ観ネット：道後温泉", "https://www.iyokannet.jp/feature/dogo"),
    "shimanami": ("いよ観ネット：しまなみ海道サイクリング", "https://www.iyokannet.jp/feature/shimanami"),
    "ishizuchi": ("いよ観ネット：石鎚山", "https://www.iyokannet.jp/spot/413"),
    "tobe": ("いよ観ネット：砥部焼伝統産業会館", "https://www.iyokannet.jp/spot/458"),
    "uchiko_ozu": ("いよ観ネット：内子座・大洲城周辺", "https://www.iyokannet.jp/spot/615"),
    "uwajima": ("いよ観ネット：宇和島城", "https://www.iyokannet.jp/spot/663"),
}

GROUP_SOURCE_KEYS = {
    "about": ["ehime_notice", "ehime_concept", "ehime_office", "bunka_kokubunsai"],
    "events": ["ehime_concept", "ehime_office", "iyokannet"],
    "recruitment": ["ehime_concept", "ehime_office"],
    "sponsors": ["ehime_notice", "ehime_concept", "ehime_office"],
    "tourism": ["iyokannet", "dogo", "matsuyama_castle", "shimanami", "ishizuchi", "tobe", "uchiko_ozu", "uwajima"],
    "access": ["iyokannet", "shimanami", "dogo"],
    "accessibility": ["ehime_concept", "ehime_office"],
    "media": ["ehime_notice", "ehime_concept", "ehime_office"],
    "committee": ["ehime_concept", "ehime_office"],
    "bids": ["ehime_office"],
    "archive": ["ehime_concept", "ehime_office"],
}

GROUP_CONTEXT = {
    "about": (
        "全国規模の文化の祭典が、愛媛へ。",
        "公式前提として、令和10年度に愛媛県で国民文化祭が開催内定しており、全国障害者芸術・文化祭と一体的に開催される想定です。名称、会期、ロゴ、キャッチフレーズ等は未確定として明示し、基本構想・実施計画の決定後に差し替える構成にします。",
        ["開催内定と未確定事項を分けて表示", "国民文化祭と全国障害者芸術・文化祭の関係を説明", "瀬戸内海、宇和海、石鎚山、四国遍路、お接待の心を主要な文脈として扱う"],
    ),
    "events": (
        "行きたい催しを、条件で迷わず探せる。",
        "会期や事業構成が決まるまではモデルイベントで見せ方を示し、会期前・会期中は日付、市町、ジャンル、予約要否、料金、バリアフリー対応をイベントカードと詳細ページに連動させます。",
        ["サムネイル、日時、市町、ジャンルをカードに表示", "無料、要申込、手話通訳、車椅子席などをタグ化", "詳細ページでは会場、交通、問い合わせ先まで一気通貫で掲載"],
    ),
    "recruitment": (
        "文化祭に参加する入口を、募集種別ごとに整理する。",
        "出演・出品、ボランティア、応援事業、協賛、入札等を一元化し、募集期間、対象、申込方法、要項・様式、問い合わせ先をHTML上でも確認できるようにします。",
        ["締切と状態を強調", "PDFだけに依存せず要点を本文化", "受付前でも制度設計中の内容を具体例として掲載"],
    ),
    "sponsors": (
        "協賛を、愛媛の文化への投資として伝える。",
        "協賛パートナー募集LPのトーンに合わせ、企業向けのブランドサイト風ファーストビュー、協賛価値、参画テーマ、協賛メニュー、使途、流れ、FAQ、関心表明フォームを公式サイト内でも展開します。",
        ["協賛金、寄付、物品、サービス、広報協力を分けて案内", "正式募集要項確定後掲載の事項を明示", "企業紹介は公平性を保ちロゴサイズと掲載順を統一"],
    ),
    "tourism": (
        "文化祭の体験を、愛媛の旅へ広げる。",
        "公式観光サイト等を確認しながら、松山・道後、しまなみ海道、石鎚山、内子・大洲、宇和島・宇和海、砥部焼、食文化などをイベント導線と接続します。",
        ["観光写真を大きく掲載", "イベント前後に回れるモデルコースを提示", "公式観光サイトへのリンクに頼りすぎず概要も本文で説明"],
    ),
    "access": (
        "会場までの行き方を、交通手段と会場の両面から示す。",
        "松山空港、JR松山駅、松山観光港等を主要起点として、飛行機、鉄道、車、フェリー、バス、会場別アクセス、バリアフリー交通情報を整理します。",
        ["主要起点、所要時間、乗換、最寄りを掲載", "交通規制や臨時便は重要情報と連動", "車椅子対応や駅・港・空港設備への導線を確保"],
    ),
    "accessibility": (
        "誰もが参加・鑑賞できる情報を先回りして届ける。",
        "手話、字幕、要約筆記、音声ガイド、車椅子席、多目的トイレ、休憩スペース、相談窓口などを、会場別・イベント別に確認できる形へ整理します。",
        ["未確定の配慮事項は調整中と明示", "イベント別対応一覧と詳細ページを連携", "相談窓口を各ページ下部に配置"],
    ),
    "media": (
        "報道機関が必要情報へすばやく到達できる。",
        "プレスリリース、取材申込、写真・動画素材、ロゴ・名称使用、問い合わせ先を簡潔に整理し、使用条件と更新日を明示します。",
        ["発表日、資料名、問い合わせ先を明示", "素材は使用条件付きで整理", "ロゴ・名称は正式決定後に規程へ差し替え"],
    ),
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def root_prefix(path: str) -> str:
    depth = len(Path(path).parts) - 1
    return "" if depth == 0 else "../" * depth


def page_image(page: Page) -> str:
    if page.path in PAGE_IMAGE_OVERRIDES:
        return PAGE_IMAGE_OVERRIDES[page.path]
    return GROUP_IMAGE_SETS.get(page.group, [GROUPS[page.group]["image"]])[0]


def page_images(page: Page) -> list[str]:
    images = [page_image(page)]
    for image in GROUP_IMAGE_SETS.get(page.group, []):
        if image not in images:
            images.append(image)
    for image in GROUP_IMAGE_SETS.get("home", []):
        if len(images) >= 4:
            break
        if image not in images:
            images.append(image)
    return images[:4]


def image_alt(image: str) -> str:
    return IMAGE_META.get(image, "愛媛大会の文化的なイメージ")


def source_keys(page: Page) -> list[str]:
    keys = ["ehime_notice", "ehime_concept", "ehime_office"]
    for key in GROUP_SOURCE_KEYS.get(page.group, []):
        if key not in keys:
            keys.append(key)
    if page.group in {"tourism", "access"}:
        for key in ["iyokannet", "dogo", "matsuyama_castle", "shimanami", "ishizuchi"]:
            if key not in keys:
                keys.append(key)
    return keys[:12]


def href(from_path: str, to_path: str) -> str:
    return root_prefix(from_path) + to_path


def page_by_path(path: str) -> Page:
    return next(page for page in PAGES if page.path == path)


def group_pages(group: str) -> list[Page]:
    return [page for page in PAGES if page.group == group and page.kind != "home"]


def icon_svg(name: str) -> str:
    icons = {
        "search": '<path d="M10.5 18a7.5 7.5 0 1 1 5.3-2.2L21 21l-1.8 1.8-5.2-5.2A7.5 7.5 0 0 1 10.5 18Zm0-2.5a5 5 0 1 0 0-10 5 5 0 0 0 0 10Z"/>',
        "arrow": '<path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "calendar": '<path d="M7 2v3M17 2v3M4 8h16M5 5h14a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 12h3v3H8zM13 12h3v3h-3z"/>',
        "people": '<path d="M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM17 12a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3 21a6 6 0 0 1 12 0M13 19a5 5 0 0 1 8 2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "document": '<path d="M6 2h9l5 5v15H6z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M14 2v6h6M9 13h7M9 17h7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "access": '<path d="M12 5a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM5 8l7-1 7 1M12 7v14M8 13l-3 8M16 13l3 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "mail": '<path d="M4 6h16v12H4z" fill="none" stroke="currentColor" stroke-width="2"/><path d="m4 7 8 6 8-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
        "download": '<path d="M12 3v11M7 10l5 5 5-5M5 20h14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        "menu": '<path d="M4 6h16M4 12h16M4 18h16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "wave": '<path d="M3 14c4-4 8-4 12 0 3 3 5 3 8 0M3 19c4-3 8-3 12 0 3 2 5 2 8 0M8 10l4-7 4 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    }
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{icons.get(name, icons["arrow"])}</svg>'


def header(current: Page) -> str:
    nav_links = "".join(
        f'<a href="{href(current.path, GROUPS[group]["path"])}">{esc(GROUPS[group]["nav"])}</a>'
        for group in TOP_NAV
    )
    utility_links = "".join(
        f'<a href="{href(current.path, target)}">{label}</a>'
        for label, target in [
            ("重要なお知らせ", "common/important.html"),
            ("支援ツール", "common/accessibility-tool.html"),
            ("Language", "common/language.html"),
            ("SNS", "common/sns.html"),
        ]
    )
    root = root_prefix(current.path)
    return f"""
    <a class="skip-link" href="#main">本文へ移動</a>
    <header class="site-header" data-header>
      <div class="site-header__inner">
        <a class="brand" href="{href(current.path, "index.html")}" aria-label="トップページへ">
          <span class="brand__mark" aria-hidden="true"><img src="{root}assets/brand-mark.svg" alt=""></span>
          <span class="brand__text">
            <strong>愛媛大会（仮）</strong>
            <small>国民文化祭・全国障害者芸術・文化祭</small>
          </span>
        </a>
        <nav class="utility-nav" aria-label="補助ナビゲーション">
          {utility_links}
        </nav>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="global-nav" data-nav-toggle>
          {icon_svg("menu")}<span class="sr-only">メニューを開閉</span>
        </button>
        <nav class="global-nav" id="global-nav" data-nav>
          {nav_links}
          <form class="header-search" role="search" data-site-search>
            <label class="sr-only" for="site-search-{abs(hash(current.path))}">サイト内検索</label>
            <input id="site-search-{abs(hash(current.path))}" name="q" type="search" placeholder="検索" autocomplete="off">
            <button type="submit" aria-label="検索">{icon_svg("search")}</button>
          </form>
        </nav>
      </div>
    </header>
    <div class="site-alert" role="status">
      <div class="container">
        <strong>現在、緊急のお知らせはありません。</strong>
        <span>会期前・会期中は、変更・中止・交通規制等をここでお知らせします。</span>
        <a href="{href(current.path, "common/important.html")}">重要情報を見る</a>
      </div>
    </div>
    <script>document.documentElement.dataset.root = "{root}";</script>
    """


def footer(current: Page) -> str:
    primary = "".join(
        f'<a href="{href(current.path, GROUPS[group]["path"])}">{esc(GROUPS[group]["label"])}</a>'
        for group in ["about", "events", "recruitment", "sponsors", "accessibility", "media", "committee", "policy"]
    )
    official = "".join(
        f'<a href="{url}" target="_blank" rel="noopener">{esc(label)}</a>'
        for label, url in [
            OFFICIAL_SOURCES["ehime_notice"],
            OFFICIAL_SOURCES["ehime_concept"],
            OFFICIAL_SOURCES["iyokannet"],
        ]
    )
    return f"""
    <footer class="site-footer">
      <div class="container site-footer__inner">
        <div>
          <p class="footer-title">令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）</p>
          <p>本サイトはブラッシュアップ版仕様書に基づく公式ホームページ案です。未確定事項は正式決定後に差し替える前提で仮表示しています。</p>
          <dl class="footer-meta">
            <div><dt>管理主体</dt><dd>実行委員会・担当部署は正式決定後掲載</dd></div>
            <div><dt>問い合わせ</dt><dd>総合窓口、募集、協賛、報道、アクセシビリティの分類別に掲載予定</dd></div>
          </dl>
        </div>
        <div class="footer-links">
          <nav aria-label="フッターナビゲーション">{primary}</nav>
          <nav aria-label="公式参考情報">{official}</nav>
        </div>
      </div>
    </footer>
    """


def layout(current: Page, body: str, description: str | None = None) -> str:
    root = root_prefix(current.path)
    desc = description or current.summary
    og_image = root + "assets/" + page_image(current)
    return f"""<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{esc(current.title)} | 愛媛大会（仮）</title>
    <meta name="description" content="{esc(desc)}">
    <meta name="theme-color" content="#18324A">
    <meta property="og:title" content="{esc(current.title)} | 愛媛大会（仮）">
    <meta property="og:description" content="{esc(desc)}">
    <meta property="og:image" content="{esc(og_image)}">
    <link rel="stylesheet" href="{root}style.css">
  </head>
  <body>
    {header(current)}
    <main id="main">
      {body}
    </main>
    {footer(current)}
    <script src="{root}search-index.js"></script>
    <script src="{root}script.js"></script>
  </body>
</html>
"""


def page_hero(page: Page) -> str:
    meta = GROUPS[page.group]
    hero_image = page_image(page)
    parent_link = href(page.path, meta["path"])
    if page.path == meta["path"]:
        parent = ""
    else:
        parent = f'<a href="{parent_link}">{esc(meta["label"])}</a><span aria-hidden="true">/</span>'
    return f"""
    <section class="page-hero" aria-labelledby="page-title">
      <div class="container page-hero__grid">
        <div class="page-hero__text">
          <nav class="breadcrumb" aria-label="現在位置">
            <a href="{href(page.path, "index.html")}">トップ</a><span aria-hidden="true">/</span>{parent}<span>{esc(page.title)}</span>
          </nav>
          <p class="eyebrow">{esc(meta["accent"])}</p>
          <h1 id="page-title">{esc(page.title)}</h1>
          <p class="page-lead">{esc(page.summary)}</p>
          <div class="status-row">
            <span>{esc(page.status)}</span>
            <span>{esc(page.stage)}</span>
          </div>
        </div>
        <figure class="page-hero__media">
          <img src="{href(page.path, "assets/" + hero_image)}" alt="{esc(image_alt(hero_image))}">
        </figure>
      </div>
    </section>
    """


def standard_points(page: Page) -> list[str]:
    by_group = {
        "common": ["全ページから迷わず到達できる導線", "会期前・会期中の情報更新に耐える構成", "アクセシビリティと検索性を重視したUI"],
        "about": ["大会の意義と愛媛らしさを短く伝える", "未確定事項は仮表示として明確に扱う", "基本構想・実施計画・資料への導線を残す"],
        "news": ["更新日、カテゴリ、問い合わせ先を明示する", "重要情報は通常のお知らせと分けて表示する", "募集・報道・会議資料への導線を併設する"],
        "events": ["日付、市町、ジャンルで探せる", "予約要否と料金を早い段階で確認できる", "バリアフリー対応をイベント単位で表示する"],
        "recruitment": ["募集期間、対象、申込方法を明確にする", "要項・様式への導線を確保する", "問い合わせ先をページ末尾に置く"],
        "pr": ["ロゴ・写真・動画の使用条件を明示する", "市町・企業が広報協力しやすい素材を整理する", "字幕・手話等の情報保障版を用意する"],
        "sponsors": ["協賛区分・掲載順は正式制度に基づく", "協賛金以外の参画方法も扱う", "関心表明から正式申込まで段階的に案内する"],
        "tourism": ["イベントと観光地を組み合わせる", "宿泊・交通など外部情報へ迷わず誘導する", "東予・中予・南予の多様性を示す"],
        "contact": ["問い合わせ分類で適切な窓口へ誘導する", "回答に関する注意事項を事前に示す", "個人情報の取扱いを明記する"],
        "access": ["交通手段別・会場別に整理する", "所要時間、最寄り、駐車場、交通規制を扱う", "バリアフリー交通情報と連携する"],
        "accessibility": ["情報保障と会場情報を分けて整理する", "イベント別の対応を一覧化する", "相談窓口を明確にする"],
        "media": ["報道発表資料と取材申込を分ける", "素材の使用条件を明示する", "問い合わせ先を明確にする"],
        "committee": ["会議名、掲載日、資料名を明示する", "古い資料と新しい資料を区別する", "個人情報や非公開情報の扱いに注意する"],
        "bids": ["公告、仕様書、質問回答、結果を一連で掲載する", "期限と提出先を明確にする", "公平性と透明性を担保する"],
        "policy": ["サイト管理者と問い合わせ先を明示する", "著作権・外部リンク・推奨環境を示す", "アクセシビリティ方針を掲載する"],
        "archive": ["会期後の成果を段階的に公開する", "写真・動画・記録集を整理して残す", "次世代への継承資料として活用する"],
    }
    return by_group.get(page.group, ["情報を整理して掲載します", "正式決定後に更新します", "問い合わせ導線を確保します"])


def card(title: str, text: str, icon: str = "arrow") -> str:
    return f"""
    <article class="info-card">
      <span class="info-card__icon">{icon_svg(icon)}</span>
      <h3>{esc(title)}</h3>
      <p>{esc(text)}</p>
    </article>
    """


def notice_block() -> str:
    return """
    <aside class="official-note">
      <strong>未確定情報の扱い</strong>
      <p>大会名称、会期、ロゴ、マスコット、協賛制度、募集開始日などは未確定事項を含みます。確定前の情報は「仮」「未定」「正式決定後掲載」と明示し、正式決定後に差し替える前提です。</p>
    </aside>
    """


def visual_story_block(page: Page) -> str:
    figures = "".join(
        f"""
        <figure class="visual-tile">
          <img src="{href(page.path, "assets/" + image)}" alt="{esc(image_alt(image))}">
          <figcaption>{esc(image_alt(image))}</figcaption>
        </figure>
        """
        for image in page_images(page)
    )
    return f"""
    <div class="visual-strip" aria-label="ページのビジュアルイメージ">
      {figures}
    </div>
    """


def source_links_block(page: Page) -> str:
    links = "".join(
        f"""
        <article class="source-card">
          <span>公式情報</span>
          <h3>{esc(OFFICIAL_SOURCES[key][0])}</h3>
          <a href="{OFFICIAL_SOURCES[key][1]}" target="_blank" rel="noopener">参照ページを開く</a>
        </article>
        """
        for key in source_keys(page)
        if key in OFFICIAL_SOURCES
    )
    return f"""
    <div class="source-block">
      <div class="section-heading">
        <p class="eyebrow">公式情報・参照元</p>
        <h2>記述内容の確認に使う公式情報</h2>
        <p>本ページ案の記述は、愛媛県庁の開催準備情報と、愛媛県公式観光サイト等で確認できる観光・文化資源をもとに整理しています。</p>
      </div>
      <div class="source-grid">{links}</div>
    </div>
    """


def page_examples(page: Page) -> list[tuple[str, str, str]]:
    specific = {
        "about/index.html": [
            ("開催概要", "令和10年度 愛媛県開催内定", "会期・統一名称・ロゴは正式決定後掲載とし、現時点では開催内定、基本構想検討中、全市町でのプログラム実施方向を分けて示します。"),
            ("制度説明", "国民文化祭と全国障害者芸術・文化祭を一体的に説明", "国民文化祭は全国規模の文化の祭典として、全国障害者芸術・文化祭は障がい者の芸術文化活動の発表・交流機会として紹介します。"),
            ("愛媛らしさ", "海、山、島、遍路、お接待を主要テーマに", "瀬戸内海、宇和海、石鎚山、四国遍路、お接待の心、東予・中予・南予の多様性を大会世界観の軸にします。"),
        ],
        "about/name.html": [
            ("表示例", "仮名称から正式名称へ差し替える運用", "公開初期は「愛媛大会（仮）」を用い、統一名称決定後はヘッダー、タイトル、OGP、資料名、検索インデックスを一括更新する想定です。"),
            ("掲載項目", "名称決定の告知、読み方、略称", "正式名称、統一名称、読み方、略称、使用開始日、旧仮称の扱いを表形式で掲載します。"),
            ("注意事項", "未確定の名称を固定化しない", "ページ内の注記で、仮名称であることと正式決定後に差し替えることを明示します。"),
        ],
        "about/catchphrase.html": [
            ("完成イメージ", "キャッチフレーズの掲出位置を整理", "決定後はトップヒーロー、広報素材、SNS画像、イベントパンフレットに展開できるよう、短いコピーと説明文を分けて掲載します。"),
            ("募集連携", "公募を行う場合の導線", "応募期間、応募資格、応募方法、審査、発表時期、著作権の扱いをHTMLと要項PDFで併記します。"),
            ("仮表示", "今はコンセプトコピーで代替", "ブラッシュアップ版仕様書のコアコンセプト「愛媛の文化を、全国へ。次の世代へ。」を仮の主コピーとして扱います。"),
        ],
        "about/mascot.html": [
            ("プロフィール", "マスコット決定後の紹介枠", "名前、由来、性格、モチーフ、活動予定、着ぐるみ・イラスト利用の条件を整理します。"),
            ("素材提供", "ダウンロードと使用申請", "画像素材、ポーズ集、利用規程、申請フォームへの導線を設け、過度なキャラクター露出を避けます。"),
            ("仮表示", "文化活動の参加風景を代替ビジュアルに", "正式キャラクターが決まるまでは、多世代参加や工芸体験の写真を使い、品位を保ちます。"),
        ],
        "events/detail.html": [
            ("イベント例", "瀬戸内文化ステージ（仮）", "日時、会場、出演、料金、予約、問い合わせ、交通、手話通訳、字幕、車椅子席を1ページで確認できる構成です。"),
            ("申込導線", "申込ページへ進む前に条件を確認", "対象年齢、定員、締切、キャンセル規定、荒天時対応を本文とカードで表示します。"),
            ("周遊導線", "イベント後の観光へ接続", "近隣の道後、松山城、商店街、公共交通の情報を外部公式サイトとあわせて案内します。"),
        ],
        "recruitment/volunteer.html": [
            ("活動例", "案内、受付、会場運営、情報保障補助", "来場者案内、受付、誘導、プログラム配布、観光・お接待、アクセシビリティ支援補助などを想定します。"),
            ("募集条件", "経験不問で参加しやすい見せ方", "対象、活動期間、説明会、保険、服装、交通費の扱い、未成年の参加条件を募集要項に整理します。"),
            ("安心設計", "できることから参加できる文化祭", "短時間参加、事前研修、困った時の連絡先を明記し、初参加でも動きやすくします。"),
        ],
        "recruitment/sponsors.html": [
            ("導線", "協賛パートナー募集ページへ集約", "募集情報側では概要と締切を示し、詳細は協賛LP調の「協賛パートナー募集」へ誘導します。"),
            ("対象", "企業、団体、金融機関、学校、地域事業者", "協賛金、寄付、物品、サービス、広報協力など、規模や業種に応じた参加方法を示します。"),
            ("未確定", "協賛区分・金額は正式募集要項確定後", "現段階では関心表明と相談導線を置き、正式制度の決定後に区分・金額・特典を差し替えます。"),
        ],
        "tourism/trip.html": [
            ("中予", "松山城・道後温泉・砥部焼", "城下町、温泉文化、俳句・文学、陶磁器体験を組み合わせ、イベント前後の半日周遊に接続します。"),
            ("東予", "しまなみ海道・今治・石鎚山", "サイクリング、島しょ部の景観、ものづくり、山岳信仰と自然を文化祭の体験導線に重ねます。"),
            ("南予", "内子・大洲・宇和島・宇和海", "歴史的町並み、城、里海、食文化、民俗芸能をめぐる滞在型の旅として紹介します。"),
        ],
        "tourism/courses.html": [
            ("1日目", "松山・道後と文学文化", "午前に松山城周辺、午後に文化イベント、夜は道後周辺を歩くモデルです。"),
            ("2日目", "しまなみ海道とものづくり", "今治方面へ移動し、サイクリング、タオル・工芸、島の景観を組み合わせます。"),
            ("3日目", "南予の歴史と食文化", "内子・大洲の町並み、宇和島の海文化、鯛めしなどをイベントと連携します。"),
        ],
        "tourism/food-culture.html": [
            ("食文化", "鯛めし、柑橘、じゃこ天など", "地域差のある食文化を紹介し、イベント会場周辺の飲食・土産情報へつなげます。"),
            ("工芸", "砥部焼、今治タオル、紙産業", "体験予約や工房見学ができる場合は、公式観光情報へ誘導します。"),
            ("表示方針", "写真と短い説明で選びやすく", "観光情報を一覧だけにせず、文化祭イベントとの組み合わせ例を示します。"),
        ],
        "accessibility/information-support.html": [
            ("情報保障", "手話、字幕、要約筆記、音声ガイド", "対応予定のイベントでは、イベントカードと詳細ページの両方で支援内容を確認できるようにします。"),
            ("事前相談", "必要な配慮を問い合わせやすく", "相談期限、相談方法、回答の目安、当日の連絡先を明記します。"),
            ("やさしい案内", "短い文と明確な導線", "やさしい日本語ページ、文字サイズ、コントラスト、本文移動などの支援ツールと連携します。"),
        ],
        "media/press.html": [
            ("発表資料", "資料名、発表日、更新日を明示", "報道発表はPDFだけでなく、概要、問い合わせ先、関連ページをHTML上にも掲載します。"),
            ("素材提供", "写真・動画・ロゴの使用条件", "使用目的、クレジット、改変可否、掲載期限を明確にします。"),
            ("取材", "申込と当日導線", "取材申込フォーム、受付条件、撮影可能範囲、当日の報道受付を整理します。"),
        ],
    }
    if page.path in specific:
        return specific[page.path]

    context = GROUP_CONTEXT.get(
        page.group,
        (
            "このページの完成形を具体的に示す。",
            "正式決定前の情報は未確定として扱いながら、利用者が何を確認できるページになるのかを具体例で示します。",
            ["掲載項目を明確にする", "更新日と問い合わせ先を示す", "関連ページへの導線を置く"],
        ),
    )
    return [
        ("役割", context[0], context[1]),
        ("掲載例", context[2][0], f"「{page.title}」では、{context[2][0]}ための情報を整理します。"),
        ("運用", context[2][1], "正式決定後は、この方針に沿って本文・資料リンク・問い合わせ先を更新します。"),
    ]


def concrete_examples_block(page: Page) -> str:
    items = "".join(
        f"""
        <article class="example-card">
          <span>{esc(label)}</span>
          <h3>{esc(title)}</h3>
          <p>{esc(text)}</p>
        </article>
        """
        for label, title, text in page_examples(page)
    )
    return f"""
    <div class="example-grid">
      {items}
    </div>
    """


def listing_block(page: Page) -> str:
    samples = {
        "news": [
            ("基本構想検討会の開催について", "準備初期", "資料公開後にPDFと概要を掲載します。"),
            ("協賛関心表明の受付開始（仮）", "協賛", "正式募集前の相談導線として設置します。"),
            ("イベント情報公開に向けた準備状況", "イベント", "実施計画策定後に順次追加します。"),
        ],
        "events": [
            ("瀬戸内文化ステージ（仮）", "松山市 / 舞台", "字幕・車椅子席対応を想定したイベント例です。"),
            ("南予の食と民俗芸能（仮）", "宇和島市 / 食文化", "地域文化と観光を結ぶモデルイベント例です。"),
            ("子ども工芸ワークショップ（仮）", "砥部町 / 工芸", "親子参加・事前申込ありのイベント例です。"),
        ],
        "recruitment": [
            ("出演・出品者募集", "正式決定後掲載", "募集要項、対象、申込様式を掲載予定です。"),
            ("ボランティア募集", "制度検討中", "活動内容、期間、説明会情報を掲載予定です。"),
            ("応援事業募集", "制度検討中", "地域団体の参加方法を掲載予定です。"),
        ],
        "sponsors": [
            ("協賛金", "正式制度決定後掲載", "協賛区分、金額、特典を掲載します。"),
            ("物品・サービス協賛", "相談受付想定", "輸送、広報、会場運営等の協力を想定します。"),
            ("広報協力", "仮導線", "掲示、配架、SNS発信等を想定します。"),
        ],
    }
    items = samples.get(page.group, [
        ("掲載項目1", "仮", "正式決定後、内容を掲載します。"),
        ("掲載項目2", "仮", "担当部署確認後に情報を更新します。"),
        ("掲載項目3", "仮", "関連資料への導線を設けます。"),
    ])
    rows = "".join(
        f'<article class="list-item"><span>{esc(label)}</span><h3>{esc(title)}</h3><p>{esc(text)}</p><a href="#contact-section">問い合わせ先を確認</a></article>'
        for title, label, text in items
    )
    return f'<div class="list-stack">{rows}</div>'


def event_filter_block(page: Page) -> str:
    events = [
        ("瀬戸内文化ステージ（仮）", "松山市", "舞台", "手話通訳あり", "無料", "2028-08-12"),
        ("砥部焼とことばの工房（仮）", "砥部町", "工芸", "親子向け", "要申込", "2028-08-18"),
        ("宇和海の食文化交流（仮）", "宇和島市", "食文化", "車椅子席あり", "有料", "2028-09-02"),
        ("俳句とまち歩き（仮）", "松山市", "文学", "やさしい日本語", "無料", "2028-09-09"),
    ]
    cards = "".join(
        f"""
        <article class="event-card" data-event-card data-city="{esc(city)}" data-genre="{esc(genre)}" data-text="{esc(title + city + genre + access)}">
          <span class="event-card__date">{esc(date)}</span>
          <h3>{esc(title)}</h3>
          <p>{esc(city)} / {esc(genre)} / {esc(access)}</p>
          <div class="pill-row"><span>{esc(price)}</span><span>{esc(access)}</span></div>
          <a class="text-link" href="{href(page.path, "events/detail.html")}">イベント詳細を見る</a>        </article>
        """
        for title, city, genre, access, price, date in events
    )
    return f"""
    <div class="filter-panel" data-filter-list>
      <div class="filter-panel__controls">
        <label>キーワード<input type="search" placeholder="イベント名・市町・ジャンル" data-filter-input></label>
        <label>市町<select data-filter-city><option value="">すべて</option><option>松山市</option><option>砥部町</option><option>宇和島市</option></select></label>
        <label>ジャンル<select data-filter-genre><option value="">すべて</option><option>舞台</option><option>工芸</option><option>食文化</option><option>文学</option></select></label>
      </div>
      <div class="event-grid">{cards}</div>
      <p class="filter-empty" data-filter-empty hidden>条件に一致するイベント例はありません。</p>
    </div>
    """


def form_block(page: Page, kind: str = "contact") -> str:
    sponsor = kind == "sponsor"
    select_options = (
        "<option>協賛金</option><option>物品協賛</option><option>サービス協賛</option><option>広報協力</option><option>未定・相談したい</option>"
        if sponsor
        else "<option>大会全般</option><option>イベント</option><option>募集</option><option>協賛</option><option>報道</option><option>アクセシビリティ</option><option>入札</option>"
    )
    select_label = "関心のある協賛方法" if sponsor else "問い合わせ分類"
    return f"""
    <form class="site-form" data-demo-form>
      <div class="field"><label for="name">氏名 <span>必須</span></label><input id="name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="org">所属・団体名</label><input id="org" name="org" autocomplete="organization"></div>
      <div class="field"><label for="email">メールアドレス <span>必須</span></label><input id="email" name="email" type="email" required autocomplete="email"></div>
      <div class="field"><label for="tel">電話番号</label><input id="tel" name="tel" type="tel" autocomplete="tel"></div>
      <div class="field field--full"><label for="category">{select_label} <span>必須</span></label><select id="category" required><option value="">選択してください</option>{select_options}</select></div>
      <div class="field field--full"><label for="message">内容 <span>必須</span></label><textarea id="message" rows="6" required></textarea></div>
      <label class="consent field--full"><input type="checkbox" required><span>個人情報の取扱いに同意します</span></label>
      <button class="button button--primary field--full" type="submit">{icon_svg("mail")}仮フォームを送信する</button>
      <p class="form-status" role="status" aria-live="polite" data-form-status></p>
    </form>
    """


def download_block(page: Page) -> str:
    docs = [
        ("大会概要資料", "PDF / 正式決定後掲載", "大会の目的、会期、事業構成をまとめる資料です。"),
        ("申込様式", "DOCX・PDF / 準備中", "募集や協賛の申込様式を掲載する想定です。"),
        ("広報素材", "画像・動画 / 使用条件あり", "ロゴ、写真、バナー、紹介文等を掲載します。"),
    ]
    return '<div class="download-grid">' + "".join(
        f"""
        <article class="download-card">
          <span>{icon_svg("download")}</span>
          <h3>{esc(title)}</h3>
          <p>{esc(text)}</p>
          <small>{esc(meta)}</small>
          <a href="#contact-section">公開予定を確認</a>
        </article>
        """
        for title, meta, text in docs
    ) + "</div>"


def faq_block() -> str:
    qs = [
        ("正式な会期は決まっていますか。", "現時点では未定です。正式決定後、トップページと会期・開催地ページに掲載します。"),
        ("イベント情報はいつ掲載されますか。", "実施計画の策定後、日付・市町・ジャンル・バリアフリー対応とあわせて順次掲載する想定です。"),
        ("協賛や広報協力の相談はできますか。", "正式募集前でも関心表明フォームを設け、協賛金、物品、サービス、広報協力の相談導線を用意します。"),
        ("アクセシビリティ情報はどこで確認できますか。", "情報保障、会場バリアフリー、イベント別対応一覧、相談窓口を分けて掲載します。"),
    ]
    return '<div class="faq-list">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in qs) + "</div>"


def access_table() -> str:
    rows = [
        ("飛行機", "松山空港から市内・各会場へ", "所要時間、空港連絡、バリアフリー情報を掲載"),
        ("電車", "JR・伊予鉄道等", "最寄駅、乗換、駅設備を掲載"),
        ("車", "高速道路・駐車場", "交通規制、駐車場、送迎導線を掲載"),
        ("フェリー", "松山観光港・三津浜港等", "港からの接続交通を掲載"),
        ("バス", "高速バス・路線バス・シャトルバス（仮）", "時刻、乗り場、臨時便を掲載"),
    ]
    return table(["交通手段", "想定ルート", "掲載項目"], rows)


def table(headers: list[str], rows: list[tuple[str, ...]]) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap" tabindex="0"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def sponsor_partnership_block(page: Page) -> str:
    values = [
        ("地域貢献の可視化", "文化芸術、伝統文化、若者の活動、障がい者芸術を支える姿勢を公式媒体で伝えます。"),
        ("ブランド発信", "会場掲出、公式サイト掲載、広報素材で文化祭を支えるパートナーとして紹介します。"),
        ("接点づくり", "県民、来場者、文化団体、市町、教育・福祉関係者との新しい接点をつくります。"),
        ("社員参加", "ボランティア、広報協力、地域イベント参加など、社内外の参加機会へつなげます。"),
        ("共生社会への貢献", "誰もが文化に参加できる大会づくりを、企業活動と結びます。"),
    ]
    value_cards = "".join(
        f'<article class="sponsor-value"><span>{i}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        for i, (title, text) in enumerate(values, 1)
    )
    menu = table(
        ["協賛方法", "想定内容", "正式決定後に掲載する事項"],
        [
            ("協賛金", "大会運営、広報、情報保障、地域プログラム等への支援", "区分、金額、特典、申込期限"),
            ("物品協賛", "飲料、備品、印刷物、展示資材、ノベルティ等", "受入条件、数量、納品方法"),
            ("サービス協賛", "輸送、警備、通訳、撮影、Web制作、会場運営等", "対象業務、役割分担、掲載可否"),
            ("広報協力", "ポスター掲出、チラシ配架、SNS発信、社内報掲載等", "素材、投稿ルール、掲出期間"),
        ],
    )
    flow = "".join(
        f'<li><span>{i}</span><strong>{esc(title)}</strong><p>{esc(text)}</p></li>'
        for i, (title, text) in enumerate(
            [
                ("関心表明", "正式募集前でも、協賛・寄付・物品・サービス・広報協力の関心を登録できます。"),
                ("個別相談", "企業規模、地域、支援テーマに応じて、参画方法を確認します。"),
                ("正式申込", "募集要項確定後、申込書、掲載可否、ロゴデータ等を提出します。"),
                ("掲載・実施", "公式サイト、会場、広報物等で、決定した範囲に基づき紹介します。"),
            ],
            1,
        )
    )
    companies = "".join(
        f"""
        <article class="sponsor-logo-card">
          <div aria-hidden="true">{esc(mark)}</div>
          <h3>{esc(name)}</h3>
          <p>{esc(text)}</p>
        </article>
        """
        for mark, name, text in [
            ("A", "協賛企業名（仮）", "文化芸術と次世代育成を支援する企業紹介の掲載例です。"),
            ("B", "地域パートナー（仮）", "会場運営、物品提供、広報協力などの掲載例です。"),
            ("C", "広報協力団体（仮）", "ポスター掲出、SNS発信、社内広報協力の掲載例です。"),
        ]
    )
    return f"""
    <div class="sponsor-suite">
      <section class="sponsor-lead">
        <figure><img src="{href(page.path, "assets/sponsor-partnership.jpg")}" alt="{esc(image_alt("sponsor-partnership.jpg"))}"></figure>
        <div>
          <p class="eyebrow">協賛パートナー募集</p>
          <h2>文化を支える企業が、愛媛の未来をつくる。</h2>
          <p>瀬戸内海、宇和海、石鎚山、四国遍路、お接待の心に育まれた愛媛の文化を全国へ発信し、次世代へつなぐ協賛パートナーを募集する想定です。協賛区分・金額・特典は正式募集要項確定後に掲載します。</p>
          <div class="hero__actions">
            <a class="button button--primary" href="{href(page.path, "sponsors/interest-form.html")}">{icon_svg("mail")}協賛について相談する</a>
            <a class="button button--secondary" href="{href(page.path, "sponsors/partner-recruitment.html")}">{icon_svg("document")}協賛詳細を見る</a>
          </div>
        </div>
      </section>
      <section>
        <div class="section-heading">
          <p class="eyebrow">協賛が生む価値</p>
          <h2>企業活動と文化祭を、地域貢献ストーリーとしてつなぐ。</h2>
        </div>
        <div class="sponsor-value-grid">{value_cards}</div>
      </section>
      <section>
        <div class="section-heading">
          <p class="eyebrow">協賛メニュー</p>
          <h2>協賛金だけでなく、物品・サービス・広報協力にも対応。</h2>
        </div>
        {menu}
      </section>
      <section>
        <div class="section-heading">
          <p class="eyebrow">協賛までの流れ</p>
          <h2>正式募集前は、関心表明から始められます。</h2>
        </div>
        <ol class="flow-list">{flow}</ol>
      </section>
      <section>
        <div class="section-heading">
          <p class="eyebrow">掲載イメージ</p>
          <h2>協賛企業・団体は公平なルールで紹介します。</h2>
        </div>
        <div class="sponsor-logo-grid">{companies}</div>
      </section>
      <section>
        <div class="section-heading">
          <p class="eyebrow">関心表明フォーム</p>
          <h2>相談内容を具体的に受け止める仮フォーム。</h2>
        </div>
        {form_block(page, "sponsor")}
      </section>
    </div>
    """


def specialized_block(page: Page) -> str:
    if page.group == "sponsors" or page.path == "recruitment/sponsors.html":
        return sponsor_partnership_block(page)
    if page.kind in {"events", "event-detail"}:
        return event_filter_block(page)
    if page.kind in {"form", "contact-form"}:
        return form_block(page)
    if page.kind == "sponsor-form":
        return form_block(page, "sponsor")
    if page.kind in {"downloads", "bid"}:
        return download_block(page)
    if page.kind in {"faq"}:
        return faq_block()
    if page.kind in {"access", "accessibility"}:
        return access_table() if page.group == "access" else accessibility_icons(page)
    if page.kind in {"search"}:
        return search_page_block()
    if page.kind in {"news-list", "listing", "sponsor-list", "tourism", "archive", "gallery", "links"}:
        return listing_block(page)
    if page.kind in {"policy"}:
        return policy_block(page)
    if page.kind in {"video"}:
        return video_block(page)
    if page.kind in {"contact-list"}:
        return contact_list_block()
    if page.kind in {"easy"}:
        return easy_japanese_block()
    if page.kind in {"important"}:
        return important_block()
    if page.kind in {"sns"}:
        return sns_block()
    if page.kind in {"tool"}:
        return tool_block()
    return listing_block(page)


def accessibility_icons(page: Page) -> str:
    items = [
        ("車椅子席あり", "客席や鑑賞位置の対応"),
        ("多目的トイレあり", "会場設備の事前確認"),
        ("手話通訳あり", "公演・案内の情報保障"),
        ("要約筆記あり", "講演・説明の文字支援"),
        ("字幕あり", "映像・舞台の字幕対応"),
        ("休憩スペースあり", "体調や感覚過敏への配慮"),
    ]
    return '<div class="icon-grid">' + "".join(card(title, text, "access") for title, text in items) + "</div>"


def policy_block(page: Page) -> str:
    rows = [
        ("サイト管理者", "正式決定後掲載"),
        ("個人情報の利用目的", "問い合わせ回答、申込受付、連絡のために利用します。"),
        ("著作権", "文章、写真、動画、ロゴ等の無断利用を制限します。"),
        ("外部リンク", "外部サイトの内容については各管理者に確認してください。"),
    ]
    return table(["項目", "記載イメージ"], rows)


def video_block(page: Page) -> str:
    return f"""
    <div class="video-placeholder">
      <div>{icon_svg("wave")}</div>
      <h3>PR動画は正式制作後に掲載予定です</h3>
      <p>字幕・手話あり版、通常版、広報用短尺版など、情報保障と広報用途に応じて整理します。</p>
    </div>
    """


def contact_list_block() -> str:
    rows = [
        ("総合問い合わせ", "大会全般", "正式決定後掲載"),
        ("イベント問い合わせ", "個別イベント", "各イベント詳細に掲載"),
        ("募集問い合わせ", "出演・出品、ボランティア等", "募集ページ末尾に掲載"),
        ("協賛問い合わせ", "協賛金、物品、サービス等", "協賛ページに掲載"),
        ("報道問い合わせ", "取材、素材提供等", "報道向けページに掲載"),
        ("アクセシビリティ問い合わせ", "配慮事項、情報保障等", "相談窓口に掲載"),
    ]
    return table(["分類", "内容", "窓口"], rows)


def easy_japanese_block() -> str:
    return """
    <div class="easy-panel">
      <h2>やさしい日本語での案内（仮）</h2>
      <p>このページでは、大会のこと、イベントのさがし方、会場への行き方、困ったときの相談先を、短い文でわかりやすく伝えます。</p>
      <ul>
        <li>大会は、令和10年度に愛媛県で開かれる予定です。</li>
        <li>くわしい日にちは、決まったあとにお知らせします。</li>
        <li>イベント、交通、バリアフリーの情報をこのサイトで見ることができます。</li>
      </ul>
    </div>
    """


def important_block() -> str:
    return """
    <div class="important-panel">
      <span>重要</span>
      <h2>現在、緊急のお知らせはありません</h2>
      <p>会期前・会期中は、イベント変更、中止、交通規制、災害・荒天時の案内をこの枠で掲出します。</p>
    </div>
    """


def sns_block() -> str:
    return """
    <div class="social-grid">
      <article><h3>公式X（仮）</h3><p>アカウント決定後に掲載します。</p></article>
      <article><h3>Instagram（仮）</h3><p>写真・動画による広報に活用します。</p></article>
      <article><h3>YouTube（仮）</h3><p>PR動画、記録映像、配信アーカイブを掲載します。</p></article>
    </div>
    """


def tool_block() -> str:
    return """
    <div class="tool-demo" data-access-tools>
      <button type="button" data-font-plus>文字を大きく</button>
      <button type="button" data-contrast>高コントラスト</button>
      <a href="#main">本文へ移動</a>
      <p>このデモは、実装時に全ページ共通の支援ツールとして配置する想定です。</p>
    </div>
    """


def search_page_block() -> str:
    return """
    <section class="search-page" data-search-page>
      <label class="search-page__box">検索キーワード
        <input type="search" data-search-input placeholder="例：協賛、イベント、バリアフリー">
      </label>
      <div class="search-results" data-search-results aria-live="polite"></div>
    </section>
    """


def sibling_nav(page: Page) -> str:
    siblings = group_pages(page.group)
    if not siblings:
        return ""
    links = "".join(
        f'<a {"aria-current=\"page\"" if p.path == page.path else ""} href="{href(page.path, p.path)}">{esc(p.title)}</a>'
        for p in siblings
    )
    return f'<nav class="sibling-nav" aria-label="{esc(GROUPS[page.group]["label"])}内のページ">{links}</nav>'


def contact_section(page: Page) -> str:
    return f"""
    <section class="section section--contact" id="contact-section" aria-labelledby="contact-title">
      <div class="container contact-strip">
        <div>
          <p class="eyebrow">問い合わせ導線</p>
          <h2 id="contact-title">このページに関する問い合わせ</h2>
          <p>担当部署、受付時間、メールアドレス等は正式決定後に掲載します。現段階では仮導線として総合問い合わせへ誘導します。</p>
        </div>
        <a class="button button--primary" href="{href(page.path, "contact/form.html")}">{icon_svg("mail")}お問い合わせへ</a>
      </div>
    </section>
    """


def render_standard_page(page: Page) -> str:
    points = "".join(card(title, "正式決定後、この方針に沿って具体的な情報を掲載します。", icon) for title, icon in zip(standard_points(page), ["document", "people", "access"]))
    body = f"""
    {page_hero(page)}
    <section class="section">
      <div class="container two-column">
        <div>
          <p class="eyebrow">ページの役割</p>
          <h2>{esc(GROUPS[page.group]["description"])}</h2>
          <p>{esc(page.summary)}</p>
        </div>
        {notice_block()}
      </div>
    </section>
    <section class="section section--visual">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">写真表現</p>
          <h2>ページの世界観を、具体的な場面で伝える</h2>
        </div>
        {visual_story_block(page)}
      </div>
    </section>
    <section class="section section--soft">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">掲載イメージ</p>
          <h2>このページで確認できること</h2>
        </div>
        <div class="card-grid">{points}</div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">完成形の具体例</p>
          <h2>正式公開時に近い内容イメージ</h2>
        </div>
        {concrete_examples_block(page)}
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">掲載内容の仮イメージ</p>
          <h2>正式決定前の表示例</h2>
        </div>
        {specialized_block(page)}
      </div>
    </section>
    <section class="section section--soft">
      <div class="container">
        {source_links_block(page)}
      </div>
    </section>
    <section class="section section--compact">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">同じ分類のページ</p>
          <h2>{esc(GROUPS[page.group]["label"])}</h2>
        </div>
        {sibling_nav(page)}
      </div>
    </section>
    {contact_section(page)}
    """
    return layout(page, body)


def render_home(page: Page) -> str:
    root = root_prefix(page.path)
    group_cards = "".join(
        f"""
        <article class="portal-card">
          <span>{esc(GROUPS[group]["accent"])}</span>
          <h3>{esc(GROUPS[group]["label"])}</h3>
          <p>{esc(GROUPS[group]["description"])}</p>
          <a href="{href(page.path, GROUPS[group]["path"])}">ページを見る {icon_svg("arrow")}</a>
        </article>
        """
        for group in ["about", "events", "recruitment", "sponsors", "tourism", "accessibility"]
    )
    news = "".join(
        f"""
        <article class="news-preview">
          <time datetime="2026-04-26">2026.04.26</time>
          <h3>{title}</h3>
          <p>{text}</p>
          <a href="{href(page.path, link)}">詳細を見る</a>
        </article>
        """
        for title, text, link in [
            ("公式ホームページ案を公開しました", "仕様書に基づき、未確定ページを含む全階層の仮ページを作成しています。", "news/detail.html"),
            ("協賛関心表明フォーム（仮）を設置", "正式募集前の相談導線として、企業・団体向けの入口を用意しました。", "sponsors/interest-form.html"),
            ("アクセシビリティ情報の仮ページを公開", "情報保障、会場情報、イベント別対応の整理イメージを掲載しました。", "accessibility/information-support.html"),
        ]
    )
    sitemap_groups = "".join(
        f'<a href="{href(page.path, GROUPS[group]["path"])}">{esc(GROUPS[group]["label"])}</a>'
        for group in [g for g in GROUPS if g != "home"]
    )
    body = f"""
    <section class="home-hero" aria-labelledby="home-title">
      <img src="{root}assets/hero-ehime-culture-festival.jpg" alt="{esc(GROUPS["home"]["alt"])}">
      <div class="home-hero__veil" aria-hidden="true"></div>
      <div class="container home-hero__content">
        <p class="status-pill">令和10年度 愛媛県開催内定 / 名称・会期は未定</p>
        <p class="home-hero__kicker">国民文化祭・全国障害者芸術・文化祭</p>
        <h1 id="home-title">愛媛の文化を、全国へ。<br>そして、次の世代へ。</h1>
        <p class="home-hero__lead">瀬戸内海、宇和海、石鎚山、四国遍路、お接待の心。愛媛に息づく多様な文化を県内各地から発信する、国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）が令和10年度に開催されます。</p>
        <div class="home-hero__actions">
          <a class="button button--primary" href="{href(page.path, "about/index.html")}">{icon_svg("arrow")}愛媛大会（仮）とは</a>
          <a class="button button--light" href="{href(page.path, "sponsors/partner-recruitment.html")}">{icon_svg("people")}協賛・応援について</a>
        </div>
        <div class="countdown" data-countdown="2028-04-01">
          <span>公開準備の目安</span>
          <strong data-countdown-days>---</strong>
          <small>令和10年度開始までの日数</small>
        </div>
      </div>
    </section>
    <section class="important-band" aria-label="重要なお知らせ">
      <div class="container">
        <strong>重要なお知らせ</strong>
        <p>現在、緊急のお知らせはありません。会期中は変更・中止・交通規制等をここに掲出します。</p>
        <a href="{href(page.path, "common/important.html")}">重要情報を見る</a>
      </div>
    </section>
    <section class="section intro-section">
      <div class="container intro-grid">
        <div>
          <p class="eyebrow">愛媛で開催する意義</p>
          <h2>全国規模の文化の祭典が、愛媛へ。</h2>
        </div>
        <p>このサイトは、世界観を伝えるブランドサイト、イベントを探せる実用ポータル、企業・団体・県民の参画を促す参加型プラットフォームを一体化する想定です。行政公式サイトとしての正確性と、文化祭らしい余白・写真表現を両立します。</p>
      </div>
    </section>
    <section class="section section--visual">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">愛媛らしさ</p>
          <h2>瀬戸内海、道後、しまなみ、石鎚、南予の文化を大きな写真で伝える。</h2>
        </div>
        {visual_story_block(page)}
      </div>
    </section>
    <section class="section section--soft">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">主要導線</p>
          <h2>目的からページを選ぶ</h2>
        </div>
        <div class="portal-grid">{group_cards}</div>
      </div>
    </section>
    <section class="section">
      <div class="container feature-split">
        <figure><img src="{root}assets/culture-participation-workshop.jpg" alt="{esc(GROUPS["about"]["alt"])}"></figure>
        <div>
          <p class="eyebrow">参加する文化祭</p>
          <h2>出演、出品、ボランティア、応援事業へ。</h2>
          <p>募集情報は、対象・期間・申込方法・要項をHTMLでも分かりやすく掲載し、PDFだけに依存しない設計にします。</p>
          <a class="button button--secondary" href="{href(page.path, "recruitment/index.html")}">{icon_svg("arrow")}募集情報を見る</a>
        </div>
      </div>
    </section>
    <section class="section section--dark">
      <div class="container feature-split feature-split--reverse">
        <figure><img src="{root}assets/event-stage-lanterns.jpg" alt="{esc(GROUPS["events"]["alt"])}"></figure>
        <div>
          <p class="eyebrow">安心して来場する</p>
          <h2>イベント、交通、バリアフリーを一つの流れで。</h2>
          <p>イベントごとに予約要否、料金、会場、交通、手話・字幕・車椅子席などの対応情報を確認できる構成です。</p>
          <a class="button button--light" href="{href(page.path, "accessibility/event-support.html")}">{icon_svg("access")}対応一覧を見る</a>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">お知らせ</p>
          <h2>準備状況と重要情報</h2>
        </div>
        <div class="news-grid">{news}</div>
      </div>
    </section>
    <section class="section section--soft">
      <div class="container feature-split">
        <figure><img src="{root}assets/dogo-onsen-night.jpg" alt="{esc(image_alt("dogo-onsen-night.jpg"))}"></figure>
        <div>
          <p class="eyebrow">観光・周遊</p>
          <h2>文化祭の体験を、愛媛の旅へ広げる。</h2>
          <p>道後温泉、しまなみ海道、内子・大洲、宇和島、石鎚山、砥部焼、柑橘、鯛めしなどをイベント情報と結びます。</p>
          <a class="button button--secondary" href="{href(page.path, "tourism/trip.html")}">{icon_svg("arrow")}旅の案内を見る</a>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">広報・公式発信</p>
          <h2>PR動画、SNS、広報素材も、正式決定後に整理して公開。</h2>
        </div>
        <div class="portal-grid">
          <article class="portal-card"><span>PR動画</span><h3>字幕・手話あり版も想定</h3><p>広報動画は通常版だけでなく、情報保障版や短尺版に分けて掲載します。</p><a href="{href(page.path, "pr/video.html")}">PR動画を見る {icon_svg("arrow")}</a></article>
          <article class="portal-card"><span>SNS</span><h3>公式発信を集約</h3><p>公式SNS決定後、更新情報、イベント紹介、交通・重要情報への導線として活用します。</p><a href="{href(page.path, "common/sns.html")}">SNSリンクを見る {icon_svg("arrow")}</a></article>
          <article class="portal-card"><span>関連リンク</span><h3>公式観光・県情報へ接続</h3><p>愛媛県庁、国民文化祭推進室、いよ観ネット等の公式情報へ誘導します。</p><a href="{OFFICIAL_SOURCES["iyokannet"][1]}" target="_blank" rel="noopener">いよ観ネットを開く {icon_svg("arrow")}</a></article>
        </div>
      </div>
    </section>
    <section class="section section--soft">
      <div class="container">
        {source_links_block(page)}
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">全ページ一覧</p>
          <h2>仕様書に基づくページ群</h2>
          <p>未確定ページも、内容のイメージをつかめる仮ページとして作成しています。</p>
        </div>
        <nav class="sitemap-strip" aria-label="大分類一覧">{sitemap_groups}</nav>
      </div>
    </section>
    """
    return layout(page, body)


def write_search_index() -> None:
    items = [
        {
            "title": page.title,
            "url": page.path,
            "group": GROUPS[page.group]["label"],
            "summary": page.summary,
            "tags": page.tags + [GROUPS[page.group]["label"], page.status],
        }
        for page in PAGES
    ]
    content = "window.SITE_SEARCH_INDEX = " + json.dumps(items, ensure_ascii=False, indent=2) + ";\n"
    (ROOT / "search-index.js").write_text(content, encoding="utf-8")


def write_assets() -> None:
    brand = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="愛媛大会仮ブランドマーク">
  <rect width="120" height="120" rx="18" fill="#18324A"/>
  <path d="M20 76c18-13 35-13 52-2 11 7 19 7 30-1" fill="none" stroke="#E89A3C" stroke-width="7" stroke-linecap="round"/>
  <path d="M27 89c19-9 39-8 58 1" fill="none" stroke="#E8F2F7" stroke-width="5" stroke-linecap="round"/>
  <path d="M37 64 60 28l23 36" fill="none" stroke="#F7F3EA" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="88" cy="34" r="10" fill="#C9A646"/>
</svg>
"""
    (ROOT / "assets" / "brand-mark.svg").write_text(brand, encoding="utf-8")


def main() -> None:
    write_assets()
    write_search_index()
    for page in PAGES:
        html_text = render_home(page) if page.kind == "home" else render_standard_page(page)
        out = ROOT / page.path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_text, encoding="utf-8")
    print(f"Generated {len(PAGES)} pages in {ROOT}")


if __name__ == "__main__":
    main()