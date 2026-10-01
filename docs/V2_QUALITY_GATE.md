# v2.0 Quality Gate

## 1. Purpose

「Awwwards / Webby / FWA級」という曖昧な目標を、実装時に判定できる内部品質ゲートへ変換する。

これは受賞可能性の予測ではない。受賞作に共通する高い完成度を、セルフレビューで継続的に要求するためのルールである。

## 2. 100-point rubric

各項目10点、合計100点。

### 1. Concept & First Impression
- 数秒でサイト固有の世界観が分かる
- 他県・他イベントへ容易に置換できない
- ファーストビューに目的と次の行動がある

### 2. Originality & Cultural Identity
- 愛媛固有の文化・土地性が表現される
- 安易な和風テンプレートや観光サイト記号に依存しない
- 独自の視覚モチーフまたは編集ルールがある

### 3. Typography
- 見出し、本文、注記、数字、英字、ラベルに体系がある
- 日本語本文の可読性が高い
- line-height、measure、letter-spacingが意図的

### 4. Visual Composition & Art Direction
- グリッドと余白に一貫性がある
- 写真の比率・トリミング・配置が意図的
- 重要度に応じた視覚階層が成立

### 5. Motion & Micro-interaction
- 動きに共通文法がある
- 状態変化が明確
- 演出が操作を遅らせない
- reduced-motionでも破綻しない

### 6. Structure & Navigation
- 現在地が分かる
- 重要タスクへ短い手数で到達
- 115ページ規模でも迷いにくい
- 検索、フィルター、パンくず、関連導線が整合

### 7. Mobile Experience
- PC版の縮小コピーではない
- タップ領域、文字サイズ、画像比率、ナビがモバイル向けに再設計
- 横スクロールや意図しないレイアウト崩れがない

### 8. Accessibility
- キーボード操作可能
- visible focus
- 十分なコントラスト
- semantic HTML
- alt text
- reduced motion
- フォームラベルとエラー表示
- 見出し階層が論理的

### 9. Performance & Technical Craft
- 不要なJSや画像を読み込まない
- レイアウトシフトを抑える
- インタラクションを阻害する重い処理がない
- animationはtransform/opacity中心
- progressive enhancementで基本情報が残る

### 10. Public-service Utility & Trust
- 重要なお知らせが埋もれない
- 日時、会場、料金、申込、問い合わせが明快
- 行政情報ページは演出より正確性を優先
- 仮情報・未確定情報の扱いが明確
- 外部リンク、PDF、問い合わせ先を認識しやすい

## 3. Pass threshold

v2.0候補は以下をすべて満たすまで完成扱いにしない。

- Total: **90 / 100以上**
- 各項目: **8 / 10以上**
- Accessibility: hard gate PASS
- Performance: hard gate PASS
- Public-service Utility & Trust: hard gate PASS

平均点が高くても、上記3項目のどれかに重大な問題があればFAIL。

## 4. Hard gates

### Accessibility hard gate
FAIL例:
- キーボードで主要機能を操作できない
- focusが見えない
- reduced-motionを無視
- 低コントラストの主要テキスト
- 画像だけで重要情報を伝える

### Performance hard gate
FAIL例:
- ファーストビュー表示を大幅に遅らせる動画・3D
- スクロールが継続的にカクつく
- 画面遷移やメニュー操作に明確な入力遅延
- 不要な巨大画像を無条件配信

### Public-service utility hard gate
FAIL例:
- 重要なお知らせが演出の後ろに隠れる
- イベント日時・会場・申込方法を即確認できない
- メニュー演出により通常のリンク動作が阻害される
- スマートフォンで検索・問い合わせが使いにくい

## 5. Self-review loop

各主要ステージで次の順番を繰り返す。

1. 実装
2. Desktop review
3. Mobile review
4. Keyboard / reduced-motion review
5. 100点rubric採点
6. 最低点の2項目を特定
7. 修正
8. 再採点

90点を一度超えただけで終了せず、重大な欠点がないか再レビューする。

## 6. Page-level review set

最低限、以下を毎回横断確認する。

- `index.html`
- `events/search.html`
- `events/detail.html`
- `recruitment/index.html`
- `sponsors/partner-recruitment.html`
- `accessibility/information-support.html`
- `tourism/courses.html`
- `access/train.html`
- `committee/overview.html`
- `policy/privacy.html`

「華やかなページ」と「行政実務ページ」の両方で品質が成立して初めてPASSとする。

## 7. Version gates

- `2.0.0-alpha.x`: デザイン方向・システム・代表ページを検証中
- `2.0.0-beta.x`: 全ページ展開後、回帰・モバイル・アクセシビリティ・性能監査中
- `2.0.0-rc.x`: 内容変更を止め、最終QAのみ
- `2.0.0`: 全ゲートPASS、v2-frozen作成
- `2.1.0`: v2の設計思想を維持した機能・ページ改善
- `2.1.1`: 軽微な修正
- `3.0.0`: 情報設計または体験・技術構成を根本再設計
