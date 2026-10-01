# ehime-kokubunsai-hp-poc

愛顔（えがお）えひめの文化祭2028のホームページのデザインPoCです。
第43回国民文化祭・第28回全国障害者芸術・文化祭を対象に、非公開リポジトリとして管理します。
公式公開サイトではありません。

## Versioning

- **v1**: 2026-04-26〜27に作成した静的HTMLモックの保存版。
- **v1-frozen**: v1完全版を固定保存するブランチ。今後変更しません。
- **main**: v2.0開発系列。現在は `2.0.0-alpha.4`（integrated-experience-review）。
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

方向を「愛媛を、ひらく。」に統合しました。
このコピーはPoCの提案であり、大会の正式なキャッチフレーズではありません。
白磁と藍を起点に、工芸・文学・食文化・表現の背景を読み、催しを探し、自分の文化帖へ集める体験です。
工芸ページには、任意のデジタル絵付けとSVGの持ち出しを実装しています。

`design-lab/review.html` は、22ページを一つに同梱した確認ファイルです。
画像と書体を同梱しており、このファイル単独で開けます。
表示幅は画面幅、390px、320pxから選べます。
トップ、文化の各章、検索、催しの案内、文化帖、参加の支援、資料まで内部リンクで巡れます。
文化帖の追加・削除と絵付け、SVGの持ち出しも操作できます。

通常配信の入口は、ルートの `index.html` です。
トップを含む21の実ルートに今回の設計を適用しました。
同内容の22ページを `design-lab/` に生成しています。
適用ルートの一覧は `design-lab/experience-manifest.json` に記録しています。
旧A/B比較は終了し、`home-a.html` と `home-b.html` は現在のトップへ案内します。
既存115ページすべての移行は未完了です。
v1-frozenは `94df551e752129e45e7f21c3d38282d87c5690db` のまま固定します。

大会の名称と会期は、[愛媛県の案内](https://www.pref.ehime.jp/page/155598.html)を2026-10-01に確認しました。
2028年10月22日から12月3日までの43日間です。
催しは確認済みのプレイベント1件と架空の掲載例4件を区別しています。
AI生成画像を実在の作品・会場の記録として扱いません。

設計と検証記録:

- `docs/V2_DESIGN_SYSTEM.md`
- `docs/V2_SELF_REVIEW.md`
- `docs/V2_ART_DIRECTION.md`
- `design-lab/qa/static-checks.json`
- `design-lab/qa/interaction-checks.json`
- `design-lab/qa/layout-references.json`

静的検査と25件の操作ロジック検査は通過しています。
配置の参考画像を使って9巡の自己レビューと修正を行いました。
参考画像はWeasyPrintによる静的描画であり、実ブラウザーのスクリーンショットではありません。
実ブラウザーの表示、読み上げ、実機操作、Core Web Vitalsは未確認です。
この環境のブラウザーはローカルプレビューを `ERR_BLOCKED_BY_CLIENT` で拒否しています。
v2.0の最終品質ゲートは保留としています。

## 再生成と検査

```bash
python scripts/build_v2_experience.py
python scripts/build_v2_art.py
python scripts/build_v2_review.py
python scripts/qa_v2_experience.py
npm install --prefix .cache/v2-qa jsdom@30.1.1
NODE_PATH="$PWD/.cache/v2-qa/node_modules" node scripts/qa_v2_experience.cjs
NODE_PATH="$PWD/.cache/v2-qa/node_modules" python scripts/render_v2_experience.py --all --extended --cycle review
```

Pythonの描画にはWeasyPrint 70、PyMuPDF、tinycss2、Pillowを使用します。
書体の再生成にはfonttoolsと、資産マニフェストで固定した元書体を使用します。
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
