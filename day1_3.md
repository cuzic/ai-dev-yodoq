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
    font-size: 22px;
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
    font-size: 22px;
    grid-column: 1;
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
    column-gap: 30px;
  }
  section.three-column h1, section.three-column h2, section.three-column h3 {
    column-span: all;
  }
  section.three-column ul, section.three-column ol {
    break-inside: avoid-column;
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

# 1日目の振り返り
- **5-STEPフロー全体の確認**
  - 要件定義 → 設計 → タスク分解 → 実装 → 品質担保 → リファクタリング＆ドキュメント
- 各ステップを確実に実行することが成功の鍵

---

# よくある失敗①いきなりコード
- **なぜ失敗するか（Jagged Intelligence + Reward Hacking）**
  - AIは設計判断が苦手→曖昧なまま実装開始
  - Reward Hacking→手抜きで「とりあえず動く」を選択
  - 結果：何度も作り直し
- **急がば回れ：前工程を丁寧にやることが結果的に最速**
- STEP1-2で曖昧さを排除（Guardrails設定）

---

# よくある失敗②AI自己レビュースキップ
- **なぜ失敗するか（Trust but Verify原則違反）**
  - AIのエラー率10-60%→検証なしは危険
  - Reward Hacking + Jagged Intelligence→セキュリティ・品質が二の次
- **「このコードをレビューして」の習慣化で40-60%改善**
- 追加コストほぼゼロ

---

# よくある失敗③リファクタリング後回し
- **なぜ失敗するか（Reward Hacking）**
  - AIは「タスク完了」優先→リファクタリングは後回し
  - 「動くからいいや」で放置→技術的負債が蓄積
- テストがあれば安心してリファクタリングできる
- 早期解消が重要

---

# 1日目のキーメッセージ
- **①曖昧さの徹底排除（Guardrails）**
  - Jagged Intelligence対策：AIの弱点を補う
- **②AIの思考可視化（タスク分解）**
  - AIは忘れっぽい→計画で全体像を把握
- **③TDDによる自己完結（Trust but Verify自動化）**
  - テストがあればAIが自己完結
- **④リファクタリング＆知見の蓄積（Living Documentation）**
  - AIは忘れっぽい→ドキュメント＝外部メモリ
- これら4つを実践することで、AIとの協業効率が飛躍的に向上

---

# 演習課題の説明（TODOアプリ）
- TODOアプリを5-STEPで開発
- 要件定義 → 設計 → タスク分解 → 実装 → 品質担保 → リファクタリング＆ドキュメント反映を体験
- Spring Boot ベース

---

---

<!-- _class: lead -->

## 演習（115分 ≒ 2時間）

---

<!-- _class: two-column -->

# 演習の目的と課題

### 演習の目的
- 5-STEPフロー実践
- AI駆動開発の効果体感
- 前工程の重要性・TDD・AI自己レビュー効果実感

### 課題：TODOアプリ開発（Spring Boot）

**要件:**
- タスク追加・編集・削除・一覧
- Spring Boot、DB連携、バリデーション

**なぜTODOアプリ？**
- シンプルだが実用的、CRUD網羅
- 2時間で5-STEP全体体験可能

---

<!-- _class: two-column -->

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

#### 15:50-16:40（50分）：STEP4-5 実装・品質
- TDD（Red-Green-Refactor）
- インクリメンタル開発、セキュリティチェック
- AI自己レビュー
- ゴール: AI自己完結の体感

#### 16:40-17:00（20分）：STEP6 リファクタリング
- コード改善、ドキュメント生成
- ゴール: Living Documentation

---

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

<!-- _class: three-column -->

# つまずきポイントと対処法

### ① 要件が曖昧で手が止まる
- **原因：** AIに質問させていない
- **対処法：** 「曖昧な点を質問して」→AIが逆質問

### ② いきなり実装を始める
- **原因：** 前工程の重要性を忘れている
- **対処法：** STEP1-2必須実施、急がば回れ

### ③ テストを後回しにする
- **原因：** TDD重要性の理解不足
- **対処法：** Red-Green-Refactorサイクル厳守

### ④ AI自己レビューをスキップ
- **原因：** 時間がないと感じる
- **対処法：** 数秒で40-60%バグ検出、時間節約

### ⑤ トークン制限エラー
- **原因：** .claudeignore不十分
- **対処法：** node_modules等除外、/compact実行

### ⑥ AIが間違った方向に進む
- **原因：** 受け入れ条件が不明確
- **対処法：** こまめに確認・軌道修正

---

---

<!-- _class: lead -->

## 演習成功のチェックリスト

---

<!-- _class: three-column -->

# 演習成功のチェックリスト①

### STEP1-2: 要件定義・設計
- ✅ AIに質問させて曖昧さ排除
- ✅ ユーザーストーリー作成
- ✅ エラー・エッジケース洗い出し
- ✅ 受け入れ基準（Given-When-Then）
- ✅ Tech Stack Setup決定
- ✅ DBスキーマ設計
- ✅ API仕様定義

### STEP3: タスク分解
- ✅ タスク一覧をAI生成
- ✅ Phase分け確認
- ✅ タスク粒度調整（30分〜2時間）
- ✅ 依存関係可視化
- ✅ 計画レビュー・調整

---

<!-- _class: three-column -->

# 演習成功のチェックリスト②

### STEP4-5: 実装・品質担保
- ✅ TDD/BDD実装（Red-Green-Refactor）
- ✅ Given-When-Then形式テスト
- ✅ インクリメンタル開発
- ✅ 環境変数で秘密情報管理
- ✅ 入力値バリデーション
- ✅ AI自己レビュー実施
- ✅ カバレッジ80%以上
- ✅ 頻繁にコミット

### STEP6: リファクタリング＆ドキュメント
- ✅ 冗長・重複コード削除
- ✅ リファクタリング実施
- ✅ architecture.md生成
- ✅ README.md作成
- ✅ 知見を記録

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
- **After：** 40-60%バグ検出・修正
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

<!-- _class: two-column -->

# 1日目全体の振り返り

### 午前（Part 1）で学んだこと
- AI活用の3原則
- Claude Codeの使い方
- STEP1: 要件定義（曖昧さ排除）
- STEP2: 設計ドキュメント（Spec-Driven）

### 午後前半（Part 2）で学んだこと
- STEP3: タスク分解（AI思考言語化）
- STEP4: 実装（小さく・TDD・AI自己レビュー）
- STEP5: 品質担保（TDDとAI相乗効果）
- STEP6: リファクタリング＆ドキュメント

### 午後後半（Part 3）で体験したこと
- 5-STEPフロー全体実践
- 前工程の重要性、TDDの威力
- AI自己レビュー効果
- Living Documentationの価値

### キーメッセージ
1. **曖昧さ徹底排除:** STEP1-2を丁寧に
2. **AI思考可視化:** STEP3で計画作成
3. **TDD自己完結:** STEP4-5でAI自律
4. **知見蓄積:** STEP6でドキュメント化
5. **急がば回れ:** 前工程が結果的に最速

---

---

<!-- _class: lead -->

## 2日目への準備

### 2日目の内容（予告）
- リバースエンジニアリング（既存コードから仕様を読み解く）
- テストシナリオ一覧作成（モレ・ヌケ防止）
- デグレ防止（既存機能が壊れないことを保証）
- 既存システムへの機能追加（実プロジェクトベース）

### 1日目の復習推奨項目
- 5-STEPフローの各ステップの目的
- TDD/BDDのRed-Green-Refactorサイクル
- AI自己レビューの4つの観点
- Living Documentationの概念
- セキュリティベストプラクティス

### 宿題（任意）
- 演習で作成したTODOアプリに機能追加してみる
- 自分のプロジェクトで5-STEPフローを試してみる
- AI自己レビューを習慣化してみる
