# ehime-kokubunsai-hp-poc

愛顔（えがお）えひめの文化祭2028のホームページのデザインPoCです。
第43回国民文化祭・第28回全国障害者芸術・文化祭を対象に、公開リポジトリで管理し、GitHub Pagesで共有します。
個人制作によるデザインPoCです。愛媛県及び大会実行委員会の公式サイトではありません。

## Versioning

- **v1**: 2026-04-26〜27に作成した静的HTMLモックの保存版。
- **v1-frozen**: v1完全版を固定保存するブランチ。今後変更しません。
- **main**: v2.0開発系列。現在は `2.0.0-alpha.6`（cultural-editorial-review）。
- v2.0完成後は `v2-frozen` を作成し、その後の比較的小規模な改善は v2.1 / v2.2 として管理します。
- 情報設計・技術構成・体験設計を再び根本から作り直す場合は v3.0 とします。

## v2.0 design upgrade

v2.0では、v1の掲載情報と必要な機能を保ちながら、Awwwards / The Webby Awards / FWA の受賞水準をベンチマークに、情報構成・デザイン・体験を全面的に再構築します。

賞の受賞可能性を自己判定することは目的にせず、受賞サイトに共通する「コンセプトの明確さ、視覚品質、タイポグラフィ、情報設計、インタラクション、技術品質、モバイル体験」を実装品質の基準として利用します。

関連資料:

- `docs/V2_DESIGN_BRIEF.md`
- `docs/V2_DESIGN_BENCHMARK.md`
- `docs/V2_QUALITY_GATE.md`

## 現在のデザインと確認ファイル

トップは5:7の非対称構図で、大見出しと文化祭全体の画像を同じ高さから見せます。
丸みのある主見出しと落ち着いた本文書体に分け、本文はPC20px・小画面18pxを維持しています。
主画像の直後に土地の文化を置き、全6催しは短い一覧へ再編集しました。
元の4仮イベントを含む全6件の固有AI画像を保持しています。

新居浜太鼓祭り、松山の俳句ポスト、内子座、宇和島の牛鬼を、実写記録4点と自治体の一次資料で紹介します。
写真・背景から気づいたことを文化帖へ残し、文学の章では五・七・五のことばをつくってSVGとして持ちかえられます。
実写の撮影時期・著作者・CC BY-SA条件を表示します。新たな現地取材やインタビューを実施した記録ではありません。
下層は読む目的に応じて9種類の構成へ分け、元の本文を開閉できる補足も含めて保持します。

**最初に `design-lab/compare.html` を開いてください。**
v1固定版と現在のv2を、同じ114ページの組み合わせで比較できます。
「並べる」「v1のみ」「v2のみ」、390pxの表示を切り替えられます。
PC本来の文字と写真のバランスを見るときは「v2のみ」を使います。
比較画面の左右それぞれで内部リンクをたどると、対応するページへ移ります。

`design-lab/review.html` は129ページの本文・画像・書体を一つに同梱したv2確認ファイルです。
このファイル単独でも開けます。表示幅は画面幅、390px、320pxから選べます。
通常配信の入口はルートの `index.html` で、128の通常ルートに共通設計を適用しました。
全体案内は `site-map.html`、キーワード探索は `common/search.html` です。

元114サイトページの本文をすべて保持し、元トップの本文はリンクした `festival-guide.html` へ再配置しました。
元の基本構成資料1件と、画像・CSS・JavaScriptを含む161ファイルの固定版も `comparison/v1/` に同梱します。
内容対応表は `docs/V2_CONTENT_INVENTORY.json`、保持検査は `design-lab/qa/content-preservation.json` に記録します。
v1-frozenは `94df551e752129e45e7f21c3d38282d87c5690db` のまま固定します。

催しは確認済みプレイベント1件と架空の掲載例5件を区別しています。
元v1の全4仮イベントの名称・日付・地域・料金・支援を掲載例として保持しています。
その仮日付は本大会の会期より前であり、実際の開催告知ではありません。
確認済み催しの画像も概念イメージであり、実際の出演者・舞台・作品の記録写真として扱いません。
大会名称・会期の確認は `docs/V2_ART_DIRECTION.md` の一次出典に記録しています。

設計と検査記録:

- `docs/V2_DESIGN_BRIEF.md`
- `docs/V2_DESIGN_BENCHMARK.md`
- `docs/V2_DESIGN_SYSTEM.md`
- `docs/V2_ART_DIRECTION.md`
- `docs/V2_SELF_REVIEW.md`
- `docs/V2_CULTURAL_RESEARCH.md`
- `design-lab/assets/CULTURAL_PHOTO_LICENSES.md`
- `design-lab/qa/static-checks.json`
- `design-lab/qa/interaction-checks.json`
- `design-lab/qa/revision-checks.json`
- `design-lab/qa/culture-checks.json`
- `design-lab/qa/layout-references.json`

静的HTML、全本文の保持、画像・書体、操作ロジックを検査し、静的参考画像のレビューを繰り返しています。
WeasyPrintの参考画像とjsdomの操作検査は、実ブラウザーの表示・読み上げ・実機・Core Web Vitalsの確認とは区別しています。
GitHub Pagesの通常配信をChromeで確認し、主要15ページ×320/390/1440pxの45表示で本文・操作の横はみ出し0、読み込み済み画像のエラー0を確認しました。
文化のキーボード切替、観察の保存・削除、催しの検索・保存、五・七・五の入力、スマホメニューのEscapeとフォーカス復帰、v1比較のページ対応も実ブラウザーで確認しています。
実機、200%拡大、読み上げ、通信制限とフィールド性能、新規の現地取材・第三者評価は残るため、最終品質ゲートと総合点は保留しています。
配点と完成条件を下げず、2.0.0の完成版として固定しません。

公開入口: https://ryotamatsuki.github.io/ehime-kokubunsai-hp-poc/
公開した比較画面: https://ryotamatsuki.github.io/ehime-kokubunsai-hp-poc/design-lab/compare.html
配信方法と検証条件は `docs/V2_GITHUB_PAGES.md`、実ブラウザー記録は `design-lab/qa/browser/` にあります。

## 再生成と検査

```bash
python -m pip install -r scripts/v2-dev-requirements.txt
npm install --prefix .cache/v2-qa jsdom@30.1.1 css-tree@3.1.0
export NODE_PATH="$PWD/.cache/v2-qa/node_modules"
python scripts/build_v2_culture_assets.py
python scripts/build_v2_experience.py
python scripts/build_v2_art.py
python scripts/build_v2_legacy_assets.py
python scripts/build_v2_assets.py --font-source-dir /path/to/font-sources
node scripts/optimize_v2_css.cjs
python scripts/build_v2_review.py
python scripts/build_v2_compare.py
python scripts/qa_v2_content.py
python scripts/qa_v2_experience.py
node scripts/qa_v2_experience.cjs
node scripts/qa_v2_revision.cjs
node scripts/qa_v2_culture.cjs
python scripts/render_v2_experience.py --all --extended --cycle review
```

Pythonの描画にはWeasyPrint 70、PyMuPDF、tinycss2、Pillowを使用します。
本文の解析にはtinyhtml5、書体の再生成にはfonttoolsと固定した元書体を使用します。
WeasyPrintはUnicode範囲による書体選択と縦書きに未対応のため、静的参考描画には同じ元書体の全文字サブセットを使います。
参考画像は実ブラウザーの字形・縦書き・フォーム描画の確認を代替しません。
元書体のコミット、SHA-256、ライセンスは素材マニフェストに記録しています。
`build_v2_lab.py`、`qa_v2_lab.py`、`qa_v2_interactions.cjs`、`render_v2_layouts.py` は現在の各処理への互換入口です。

## v1 contents

元アーカイブは `ehime-kokubunsai-hp(2).zip`（51,933,213 bytes）です。

- ZIP SHA-256: `e4e037bf836f240661cd479aacb3de3b241b067ff3a1f2cc767ec1eddd34ae26`
- 元アーカイブ内: 162 files
- HTML: 115 files（サイトページ114 + 基本構成資料1）
- image assets: 39 files
- 静的 HTML / CSS / JavaScript
- HTML生成スクリプト
- ホームページ基本構成資料
- 仕様書・レビュー用README

## Raster asset note

ラスター画像38点はすべて `assets/` 配下に収録済みです。SVGの `assets/brand-mark.svg` と合わせ、v1の画像資産39点をGitHub上で保持しています。

`assets/ASSET_MANIFEST.tsv` には元ZIP内の画像ファイル名、サイズ、SHA-256を保存しています。GitHub上のラスター画像38点については、ファイル名とサイズが元マニフェストと一致することを確認済みです。

`scripts/restore_v1_assets.py` は、元ZIPから画像資産を再展開・検証するための復元用補助スクリプトとして残しています。

v1の詳細は `docs/V1_SNAPSHOT.md` を参照してください。
