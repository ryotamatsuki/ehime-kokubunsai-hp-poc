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

### 刷新の方向性を確認する条件

2026-10-01の比較では、旧A・B案はv1との違いが小さく、方向性の要件に対して不合格となった。
技術検査が通っていても、この指摘を総合点で相殺しない。

D2を確定する前に、v1との比較で次を確認する。

- 最初の画面の構図、写真の役割、文字の組み方が変わっている。
- セクションの順序と情報を読むリズムが変わっている。
- 探す・参加するための操作が、画面の見せ方とつながっている。
- スマートフォンでも、v1との差と主要タスクへの到達性が残る。

これは単純なDOM差分や変更行数で合格を証明する条件ではない。
PCとスマートフォンの画面を比較して評価し、未確認の段階では方向性の判定を保留する。
配色、書体、角丸、写真の差し替えだけでは、この条件を満たしたと扱わない。

### v2.0の完成条件

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



## 8. Evidence required for scoring

各評価には、対象ページ、画面幅、確認方法、根拠ファイル、残った課題を付ける。
設計文書の存在だけで8点以上を付けない。
確認していない項目は「未確認」とし、全項目を確認するまで総合点を算定しない。

| 項目 | 8点の条件 | 9点の条件 | 10点の条件 |
| --- | --- | --- | --- |
| Concept & First Impression | 目的と次の行動がPCとスマホで伝わる | 写真、コピー、文字組が同じ考え方で揃う | 初見の利用者にも固有の意味が伝わることを確認した |
| Originality & Cultural Identity | 土地、作品、人を具体的に扱う | 複数ページで独自の編集ルールが成立する | 固有性を利用者と専門家の評価で確認した |
| Typography | 長い名称、本文、注記、数字が読める | 主要ページ型と拡大表示で文字組が揃う | 可読性と表現の完成度を第三者確認まで含めて裏付けた |
| Visual Composition & Art Direction | PCとスマホで階層と写真の構図が成立する | ページごとの強弱と素材の質が揃う | 全代表型で細部まで調整し、第三者の比較評価を得た |
| Motion & Micro-interaction | 状態の変化が分かり、低減設定で停止する | 速度と方向が統一され、操作を待たせない | 利用者の操作を助ける効果まで確認した |
| Structure & Navigation | 探す、確認する、参加方法へ進む操作を完了できる | 検索、戻る、関連情報、現在地が揃う | 複数の初見利用者で主要タスクの成功を確認した |
| Mobile Experience | 320pxと390pxで欠落と横はみ出しがない | 実機、拡大、縦横切替でも操作できる | 複数の実機と利用者で操作を確認した |
| Accessibility | 対象機能をキーボードと読み上げで利用できる | 拡大、低減設定、フォーム状態も確認した | 独立した手動確認を含め、対象範囲の適合確認を完了した |
| Performance & Technical Craft | 定めた環境で表示と操作の目標を満たす | ページ型と条件を変えても回帰がない | 運用時の測定も含め、安定した性能を確認した |
| Public-service Utility & Trust | 日時、会場、料金、申込、問い合わせの状態が明快 | 変更、中止、未公開、未確定の表示が揃う | 運用担当者による更新と内容確認まで実証した |

8点は完成水準の基準であり、今回のD2試作に付与した点数ではない。
D2の結果は `V2_D2_REVIEW.md` に記録する。

## 9. Measured gates and manual checks

アクセシビリティはWCAG 2.2 AAを設計上の目標とする。
自動検査と手動確認を組み合わせ、対象範囲を記録する。
静的HTMLの検査だけで適合を宣言しない。

- 主要な文字と地の色は4.5:1以上を確認する。
- 操作を識別する境界とフォーカスは3:1以上を確認する。
- サイトの操作部品は44pxを基本とする。
- 実ブラウザーで320px、390px、PC幅、200%拡大を確認する。
- キーボード、読み上げ、動きの低減設定を手動で確認する。

性能は通常配信版を対象に計測する。
D2では小画面向けの主要素材を500,000 bytes以内とする暫定予算を設定した。
この素材容量の確認を、描画速度の測定やCore Web Vitalsの合格に代用しない。

運用時の目標はLCP 2.5秒以下、INP 200ms以下、CLS 0.1以下とする。
フィールド評価はPCとスマホを分け、75パーセンタイルで判定する。
PoCでフィールドデータが得られない場合は、実ブラウザーでの試験結果と測定条件を記録する。

根拠資料:

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Google Web Vitals: https://web.dev/articles/vitals
