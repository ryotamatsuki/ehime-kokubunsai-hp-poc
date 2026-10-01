# v1 snapshot

## Provenance

- 作成時期: 2026-04-26〜2026-04-27
- 対象: 令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）公式HPモック
- 元アーカイブ名: `ehime-kokubunsai-hp(2).zip`
- 元アーカイブサイズ: 51,933,213 bytes
- SHA-256: `e4e037bf836f240661cd479aacb3de3b241b067ff3a1f2cc767ec1eddd34ae26`
- 元アーカイブ内ファイル数: 162
- HTML数: 115（サイトページ114 + `homepage_structure_document.html`）
- 画像数: 39

## Freeze policy

この復元時点を `v1-frozen` ブランチとして固定する。今後のデザイン改修・情報設計変更・新機能追加は `main` または別ブランチで実施し、v1を上書きしない。

## Recovery status

GitHub上にv1の復元一式を収録済み。

- HTML 115ファイル
- CSS / JavaScript / 検索インデックス
- HTML生成スクリプト
- 仕様書・レビュー用README
- ラスター画像38点
- SVGブランドマーク1点

画像資産39点は `assets/` 配下に配置している。ラスター画像38点については、`assets/ASSET_MANIFEST.tsv` に記録した元ZIPのファイル名・バイト数とGitHub上のファイルが一致することを確認済み。

`scripts/restore_v1_assets.py` は、元ZIPから画像資産を再展開し、マニフェストに基づいて整合性を確認するための補助スクリプトとして保持する。

## Frozen revision

v1の内容確定後、画像資産を含む完全版を `v1-frozen` で固定する。
