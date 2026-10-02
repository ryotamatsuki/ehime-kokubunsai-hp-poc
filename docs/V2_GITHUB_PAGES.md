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

公開入口: https://ryotamatsuki.github.io/ehime-kokubunsai-hp-poc/
v1比較: https://ryotamatsuki.github.io/ehime-kokubunsai-hp-poc/design-lab/compare.html

2026年10月2日にGitHub Pagesの公開とユーザーによる到達確認が完了した。
公開設定は `main` / `/ (root)`。HTTPSのトップ、画像、日本語Webフォント、比較画面をChromeで確認した。
最新版のCSS修正はコミット `bbf9fb0c3f7a2e2a8f340d39c58c98c022200050`、Pagesの実行 `36972093847` がcompleted / successである。
以後の検査資料の追記もmainへ保存する。静的な資産を含む公開元はGit treeで照合する。

主要15ページを、同じオリジンの通常配信HTML・CSS・画像・書体で320/390/1440px幅へ読み込み、45表示を確認した。
最終記録は最初の320px表示を含め46件。本文・操作の横はみ出し0、読み込み済み画像エラー0、全表示でWebフォントloadedと公式ではない旨の注意書きを確認した。
PCでは本文20px・主見出し94px・主画像上端約200px、小画面の本文は18pxである。

実操作では文化タブの矢印キー、観察の保存・削除とフォーカス、砥部町の催し検索、催しの保存・文化帖・削除、かなの五・七・五と縦書き、スマホ用メニューのEscapeと復帰を確認した。
比較画面でトップと催し検索の両版が対応することも確認した。
実行記録、途中の不合格と修正、PCの実画面を `design-lab/qa/browser/` に保存する。

検査幅はChromeのiframe内のCSS表示幅であり、実機のスマートフォンではない。
通信制限をかけず、キャッシュ再使用を含む。遅延画像は読み込み済みのみを数える。
LCP・CLS・Resource Timingはその条件の観測記録で、フィールドCore Web Vitalsや全入力のINPの合格判定ではない。
実機、200%拡大、読み上げ、低減設定、十分な性能測定、新規の現地取材と第三者評価は引き続き品質ゲートの対象である。
