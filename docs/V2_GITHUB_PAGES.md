# GitHub Pagesでの公開

## 配信元

- リポジトリ: `ryotamatsuki/ehime-kokubunsai-hp-poc`
- 公開方法: GitHub Pages / Deploy from a branch
- ブランチ: `main`
- フォルダー: `/ (root)`
- 入口: `index.html`
- `.nojekyll` により、生成済みHTML・画像・書体をそのまま配信する。
- サブディレクトリーからの配信を考慮し、内部リンクと素材URLは相対パスを使う。

すべての通常ページの冒頭・フッターに「個人制作によるデザインPoCです。愛媛県及び大会実行委員会の公式サイトではありません。」と表示する。
催しの架空の掲載例、確認済み情報、AI生成のイメージ、出典付きの実写記録を区別する。

## バージョン運用

`main` の更新をGitHub Pagesへ反映する。`v1-frozen` は `94df551e752129e45e7f21c3d38282d87c5690db` のまま変更しない。
保存版との比較は `design-lab/compare.html`、単独確認ファイルは `design-lab/review.html` を使う。

## 公開後の確認

公開URLの到達、画像と日本語Webフォント、主要な内部リンク、文化記録の切替、催し検索、文化帖、下層の補足表示を実ブラウザーで確認する。
静的参考画像・jsdomの記録と、公開URLで確認した実ブラウザーの記録を区別する。
公開設定と配信確認の結果は、確認後に本資料及び `V2_SELF_REVIEW.md` に追記する。
