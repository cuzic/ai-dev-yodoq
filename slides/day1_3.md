---
marp: true
theme: default
paginate: true
style: |
  /* デフォルト：上下レイアウト（図が大きい） */
  section img {
    max-width: 95%;
    max-height: 60vh;
    display: block;
    margin: 10px auto;
    object-fit: contain;
  }

  /* 左右レイアウト：図を左に */
  section.layout-horizontal-left {
    display: grid;
    grid-template-columns: 55% 45%;
    gap: 20px;
    align-items: start;
  }
  section.layout-horizontal-left h1 {
    grid-column: 1 / -1;
  }
  section.layout-horizontal-left img {
    max-width: 100%;
    max-height: 75vh;
    margin: 0;
  }
  section.layout-horizontal-left > :not(h1):not(img) {
    font-size: 19px;
  }
  section.layout-horizontal-left li {
    margin-bottom: 5px;
  }

  /* 左右レイアウト：図を右に */
  section.layout-horizontal-right {
    display: grid;
    grid-template-columns: 45% 55%;
    gap: 20px;
    align-items: start;
  }
  section.layout-horizontal-right h1 {
    grid-column: 1 / -1;
  }
  section.layout-horizontal-right img {
    max-width: 100%;
    max-height: 75vh;
    margin: 0;
    grid-column: 2;
    grid-row: 2;
  }
  section.layout-horizontal-right > :not(h1):not(img) {
    font-size: 19px;
    grid-column: 1;
  }
  section.layout-horizontal-right li {
    margin-bottom: 5px;
  }

  /* 図のみレイアウト：図を最大化 */
  section.layout-diagram-only img {
    max-width: 98%;
    max-height: 85vh;
  }

  /* 2カラムレイアウト：テキストのみのスライド向け */
  section.two-column {
    columns: 2;
    column-gap: 40px;
  }
  section.two-column h1, section.two-column h2, section.two-column h3 {
    column-span: all;
  }
  section.two-column ul, section.two-column ol {
    break-inside: avoid-column;
  }

  /* 3カラムレイアウト：チェックリスト、比較表など */
  section.three-column {
    columns: 3;
    column-gap: 25px;
    font-size: 18px;
  }
  section.three-column h1 {
    font-size: 32px;
    column-span: all;
  }
  section.three-column h2, section.three-column h3 {
    column-span: all;
    font-size: 22px;
  }
  section.three-column ul, section.three-column ol {
    break-inside: avoid-column;
  }
  section.three-column li {
    margin-bottom: 3px;
  }

  /* Compactレイアウト：オーバーフロー回避用 */
  section.compact {
    font-size: 16px;
    line-height: 1.4;
  }
  section.compact h1 {
    font-size: 28px;
    margin-bottom: 15px;
  }
  section.compact h2 {
    font-size: 20px;
    margin-top: 10px;
    margin-bottom: 8px;
  }
  section.compact h3 {
    font-size: 18px;
    margin-top: 8px;
    margin-bottom: 6px;
  }
  section.compact li {
    margin-bottom: 2px;
  }
  section.compact ul, section.compact ol {
    margin-top: 5px;
    margin-bottom: 5px;
  }

  /* 画像2枚横並び：Before/After、比較用 */
  section.two-images-horizontal {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    align-items: start;
  }
  section.two-images-horizontal h1 {
    grid-column: 1 / -1;
  }
  section.two-images-horizontal img {
    max-width: 100%;
    max-height: 70vh;
    margin: 0;
  }

  /* 画像上、テキスト下（コンパクト）：図の下に詳細説明を書く場合 */
  section.image-top-compact img {
    max-width: 95%;
    max-height: 40vh;
    display: block;
    margin: 10px auto;
    object-fit: contain;
  }

  /* カード型グリッド：選択肢、ツール比較、ユースケース並列表示 */
  section.card-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    align-items: start;
  }
  section.card-grid h1 {
    grid-column: 1 / -1;
  }
  section.card-grid > :not(h1) {
    background: #f8f9fa;
    border: 2px solid #dee2e6;
    padding: 20px;
    border-radius: 8px;
  }
  section.card-grid h3 {
    margin-top: 0;
    color: #0066cc;
  }

  section {
    font-size: 24px;
    padding: 40px 60px;
  }
  h1 {
    font-size: 44px;
    margin-bottom: 15px;
  }
  h2 {
    font-size: 36px;
  }
  ul, ol {
    margin: 8px 0;
  }
  li {
    margin: 6px 0;
    line-height: 1.4;
  }
---

# Day 1-3: まとめ + 演習 (15:00-17:00)

---

<!-- _class: lead -->

## まとめ（5分）

---

<!-- _class: layout-diagram-only -->

# 1日目の振り返り

![5-STEPフロー全体](diagrams/diagram_03_5step_flow.svg)

**5-STEPフロー:** 要件定義 → 設計 → タスク分解 → 実装 → 品質担保

**成功の鍵:** 各ステップを確実に実行、飛ばさない、AIの制約を理解

---
<!-- _class: layout-diagram-only -->

# よくある失敗①いきなりコード

![よくある失敗①いきなりコード](../diagrams-web/slide_004_よくある失敗①いきなりコード.svg)

---

# よくある失敗②AI自己レビュースキップ
- **なぜ失敗するか（Trust but Verify原則違反）**
  - AIにもエラーあり→検証なしは危険
  - Reward Hacking→明示されない品質要件を省略してしまう
- **「このコードをレビューして」の習慣化で品質改善**
- 追加コストほぼゼロ

---

# よくある失敗③リファクタリング後回し
- **なぜ失敗するか（Reward Hacking）**
  - AIは「タスク完了」優先→リファクタリングは後回し
  - 「動くからいいや」で放置→技術的負債が蓄積
- テストがあれば安心してリファクタリングできる
- 早期解消が重要

---

<!-- _class: layout-diagram-only -->

# 1日目のキーメッセージ

![1日目のキーメッセージ](diagrams/diagram_48_day1_key_messages.svg)

---
<!-- _class: layout-diagram-only -->

# 演習課題の説明（TODOアプリ）

![演習課題の説明（TODOアプリ）](../diagrams-web/slide_008_演習課題の説明TODOアプリ.svg)

---

---

<!-- _class: lead -->

## 演習（115分 ≒ 2時間）

---
<!-- _class: layout-diagram-only -->

# 演習の目的と課題

![演習の目的と課題](../diagrams-web/slide_011_演習の目的と課題.svg)

---

<!-- _class: two-column compact -->

### 演習の進め方（時間配分）

#### 15:05-15:15（10分）：環境セットアップ
- Claude Code環境確認、プロジェクト作成
- 課題要件確認

#### 15:15-15:35（20分）：STEP1-2 要件・設計
- AIに質問させて仕様確定
- 要件定義（ユーザーストーリー、エッジケース）
- 設計（Tech Stack、DBスキーマ、API仕様）
- ゴール: 曖昧さ完全排除

#### 15:35-15:50（15分）：STEP3 タスク分解
- タスク一覧作成（Phase分け、30分〜2時間粒度）
- ゴール: AI思考の可視化

#### 15:50-16:20（30分）：STEP4 実装
- TDD（Red-Green-Refactor）
- インクリメンタル開発、セキュリティチェック
- AI自己レビュー
- ゴール: AI自己完結の体感

#### 16:20-17:00（40分）：STEP5 品質担保＆ドキュメント反映
- テスト実行・カバレッジ確認
- リファクタリング（重複削減、パターン適用）
- ドキュメント生成（architecture.md、README.md、CLAUDE.md）
- ゴール: Trust but Verify自動化、Living Documentation

---

<!-- _class: two-column compact -->

### 演習のゴール
- **5-STEPの流れを体験する**
- **AIとの対話方法を習得する**
- **TDDの効果を実感する**
- **リファクタリングによる品質向上を体験する**
- **セキュアな実装の重要性を理解する**

### 講師サポート
- 各自のペースで進める（全ステップ完了は必須ではない）
- つまずいたら挙手して講師に質問
- 他の参加者と相談・情報共有OK
- 成功したプロンプトの共有を推奨

---

---

<!-- _class: lead -->

## 演習でよくあるつまずきポイントと対処法

---
<!-- _class: layout-diagram-only -->

# つまずきポイントと対処法

![つまずきポイントと対処法](../diagrams-web/slide_016_つまずきポイントと対処法.svg)

---

---

<!-- _class: lead -->

## 演習成功のチェックリスト

---

<!-- _class: layout-diagram-only -->

# 演習成功のチェックリスト①

![演習成功のチェックリスト①](../diagrams-web/slide_019_演習成功のチェックリスト①.svg)

---
<!-- _class: layout-diagram-only -->

# 演習成功のチェックリスト②

![演習成功のチェックリスト②](../diagrams-web/slide_020_演習成功のチェックリスト②.svg)

---

---

<!-- _class: lead -->

## 演習で体感できること

---

<!-- _class: two-column -->

# 演習で体感できること

### ① 前工程の重要性
- **STEP1-2丁寧実施：** スムーズ、手戻り少、完成早い
- **STEP1-2省略：** 迷う、手戻り多発、遅い

### ② TDDの威力
- **テストなし：** 人間実行→エラー確認→コピペ→AI伝達→修正（無限ループ）
- **テストあり：** AI自動テスト→検知→修正→成功（自己完結）

### ③ AI自己レビューの効果
- **Before：** バグだらけ
- **After：** 多くのバグ検出・修正
- **追加コスト：** ほぼゼロ（数秒）

### ④ インクリメンタル開発の安心感
- **全部一度：** 動くまで不安、原因特定困難
- **小さく作る：** 常に動作確認、原因特定容易、進捗見える

### ⑤ Living Documentationの価値
- **ドキュメントなし：** AIが忘れる、同じ間違い繰り返す
- **ドキュメントあり：** AI参照可能、間違い防止、引き継ぎ容易

---

---

<!-- _class: lead -->

## 演習の成果物

---

# 成果物：ディレクトリ構成

```
プロジェクトディレクトリ/
├── docs/               # 要件・設計・タスク・完成図面
├── src/
│   ├── main/java/      # 本番コード
│   └── test/java/      # テストコード
├── README.md
├── .env.example
└── .gitignore
```

---

<!-- _class: two-column -->

# 成果物：品質基準

**ドキュメント品質**
- 曖昧さがない（誰が読んでも同じ解釈）
- 受け入れ条件が明確（Given-When-Then形式）
- エラー・エッジケースを網羅
- 設計判断の理由を記録

**コード品質**
- テストカバレッジ80%以上
- セキュリティベストプラクティス適用
- 環境変数で秘密情報管理
- リファクタリング済み

---

---

<!-- _class: lead -->

## 1日目全体の振り返り

---
<!-- _class: layout-diagram-only -->

# 1日目全体の振り返り

![1日目全体の振り返り](../diagrams-web/slide_030_1日目全体の振り返り.svg)

---

---

<!-- _class: two-column compact -->

## 2日目への準備

**📅 2日目の内容**
- リバースエンジニアリング
- テストシナリオ作成
- デグレ防止

**📚 復習推奨**
- 5-STEP フロー
- AI制約対策
- TDD/BDD

**🏠 宿題**
- TODOアプリ機能追加
- 自プロジェクトで5-STEP
- AI自己レビュー習慣化
