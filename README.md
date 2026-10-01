# ehime-kokubunsai-hp-poc

令和10年度 国民文化祭・全国障害者芸術・文化祭 愛媛大会（仮）の公式ホームページPoCです。非公開リポジトリとして管理します。

## Versioning

- **v1**: 2026-04-26〜27に作成した静的HTMLモックの保存版。
- v1の固定点は `v1-frozen` ブランチで保持します。
- 今後の改修は `main` で行い、`v1-frozen` は変更しません。

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

ChatGPT Library から GitHub connector へバイナリを直接転送できないため、ラスター画像38点はこの復元コミットには含めていません。SVGの `assets/brand-mark.svg` は収録済みです。

元ZIPの完全性を確認できるよう `assets/ASSET_MANIFEST.tsv` に元画像のサイズとSHA-256を保存しています。元ZIPを取得できれば、次のコマンドで正確なパスへ復元できます。

```bash
python scripts/restore_v1_assets.py /path/to/ehime-kokubunsai-hp.zip
```

詳細は `docs/V1_SNAPSHOT.md` を参照してください。
