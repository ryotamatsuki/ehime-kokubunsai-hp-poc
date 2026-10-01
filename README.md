# ehime-kokubunsai-hp-poc

令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）の公式ホームページPoCです。非公開リポジトリとして管理します。

## Versioning

- **v1**: 2026-04-26〜27に作成した静的HTMLモックの保存版。
- **v1-frozen**: v1完全版を固定保存するブランチ。今後変更しません。
- **main**: v2.0開発系列。現在は `2.0.0-alpha.1`（design research / direction setting）。
- v2.0完成後は `v2-frozen` を作成し、その後の比較的小規模な改善は v2.1 / v2.2 として管理します。
- 情報設計・技術構成・体験設計を再び根本から作り直す場合は v3.0 とします。

## v2.0 design upgrade

v2.0では、v1の情報構成・掲載内容・主要機能を原則維持しつつ、Awwwards / The Webby Awards / FWA の受賞水準をベンチマークに、デザインと体験を全面的に再構築します。

賞の受賞可能性を自己判定することは目的にせず、受賞サイトに共通する「コンセプトの明確さ、視覚品質、タイポグラフィ、情報設計、インタラクション、技術品質、モバイル体験」を実装品質の基準として利用します。

関連資料:

- `docs/V2_DESIGN_BRIEF.md`
- `docs/V2_DESIGN_BENCHMARK.md`
- `docs/V2_QUALITY_GATE.md`

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
