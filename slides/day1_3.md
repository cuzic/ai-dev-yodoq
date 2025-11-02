---
marp: true
theme: ai-seminar
paginate: true
---

<!-- _class: lead -->

## Day 1-3
# まとめ + 演習
(15:00-17:00)

---

<!-- _class: layout-diagram-only -->

# 1日目の振り返り（5分）

![5-STEPフロー全体](./assets/diagrams/diagram_03_5step_flow.svg)

## 🎯 5-STEPフロー全体の確認

**STEP1: 要件定義** → **STEP2: 設計** → **STEP3: タスク分解** → **STEP4: 実装** → **STEP5: 品質担保** → **STEP6: リファクタリング＆ドキュメント**

## 🔑 成功の鍵
各ステップを確実に実行（飛ばさない・急がば回れ・AIの制約を理解）

---

<!-- _class: layout-comparison compact -->

# よくある失敗①いきなりコード

<div>

## ❌ なぜ失敗するか

**Jagged Intelligence（能力のギザギザ）:**
- コード生成・技術設計は人間超え、だがビジネス要件の解釈は苦手
- 曖昧な要件のまま実装開始
- 勝手に推測して間違った方向

**Reward Hacking:**
- 手抜きで「とりあえず動く」を選択
- セキュリティ・品質は二の次

**結果:**
- 何度も作り直し
- 手戻り多発
- 時間がかかる

</div>

<div class="separator">VS</div>

<div>

## ✅ 正しいアプローチ

**急がば回れ:**
前工程を丁寧にやることが結果的に最速

**STEP1-2で曖昧さを排除:**
- 要件定義で「何を作るか」を明確化
- 設計で「どう作るか」を明確化
- Guardrails設定

## 📊 効果

✅ 手戻りゼロ
✅ 実装スピード大幅向上
✅ 品質の安定化

</div>

---

<!-- _class: layout-callout -->

<div class="icon">⚠️</div>

# よくある失敗②AI自己レビュースキップ

<div class="message">

**なぜ失敗するか（Trust but Verify原則違反）**
- AIにもエラーあり→検証なしは危険
- Reward Hacking→明示されない品質要件を省略してしまう

**「このコードをレビューして」の習慣化で品質改善**
- 追加コストほぼゼロ

</div>

---

<!-- _class: layout-callout -->

<div class="icon">⚠️</div>

# よくある失敗③リファクタリング後回し

<div class="message">

**なぜ失敗するか（Reward Hacking）**
- AIは「タスク完了」優先→リファクタリングは後回し
- 「動くからいいや」で放置→技術的負債が蓄積

**テストがあれば安心してリファクタリングできる**
- 早期解消が重要

</div>

---

<!-- _class: layout-diagram-only compact -->

# 1日目のキーメッセージ

![1日目のキーメッセージ](./assets/diagrams/diagram_48_day1_key_messages.svg)

---

<!-- _class: lead supercompact -->

## 演習課題の説明（TODOアプリ）

---

<!-- _class: card-grid supercompact -->

# 演習課題の説明（TODOアプリ）

### 🎯 課題内容

**TODOアプリを5-STEPで開発**

**フロー:** 1.要件定義 2.設計 3.タスク分解 4.実装 5.品質担保 6.リファクタ＆Doc

**技術:** Spring Boot、DB、バリデーション、TDD/BDD

### 📋 要件

**機能:** 追加・編集・削除・一覧

**品質:** BCrypt・環境変数・バリデーション・カバレッジ80%+

### ⏰ 時間（115分）

Setup10、STEP1-2:20、STEP3:15、STEP4:30、STEP5:40

---

<!-- _class: lead compact -->

## 演習（115分 ≒ 2時間）

---

<!-- _class: lead ultracompact -->

# 演習の目的

5-STEPフロー実践、AI駆動開発の効果体感、前工程の重要性・TDD・AI自己レビュー効果実感

---

<!-- _class: card-grid supercompact -->

# 課題：TODOアプリ開発

### 要件
- タスク追加・編集・削除・一覧
- Spring Boot、DB連携、バリデーション

### なぜTODOアプリ？
シンプルだが実用的、CRUD網羅

### 目標
2時間で5-STEP全体体験

---

<!-- _class: layout-timeline -->

# 演習の進め方（時間配分）

<div class="timeline">

<div class="step">
<div class="step-number">1</div>
<h3>環境セットアップ</h3>
<p><strong>15:05-15:15（10分）</strong></p>
<p>Claude Code環境確認、プロジェクト作成、課題要件確認</p>
</div>

<div class="step">
<div class="step-number">2</div>
<h3>STEP1-2 要件・設計</h3>
<p><strong>15:15-15:35（20分）</strong></p>
<p>AIに質問させて仕様確定、曖昧さ完全排除</p>
</div>

<div class="step">
<div class="step-number">3</div>
<h3>STEP3 タスク分解</h3>
<p><strong>15:35-15:50（15分）</strong></p>
<p>タスク一覧作成、AI思考の可視化</p>
</div>

<div class="step">
<div class="step-number">4</div>
<h3>STEP4 実装</h3>
<p><strong>15:50-16:20（30分）</strong></p>
<p>TDD、AI自己レビュー、AI自己完結の体感</p>
</div>

<div class="step">
<div class="step-number">5</div>
<h3>STEP5 品質担保</h3>
<p><strong>16:20-17:00（40分）</strong></p>
<p>テスト実行、リファクタリング、ドキュメント生成</p>
</div>

</div>

---

<!-- _class: card-grid -->

# 演習のゴール

### 🎯 5-STEPの流れを体験する
各ステップの重要性と効果を実感

### 💬 AIとの対話方法を習得する
効果的なプロンプトとレビュー手法

### 🧪 TDDの効果を実感する
Red-Green-Refactorサイクルの威力

### 🔧 リファクタリングによる品質向上を体験する
テストの安心感と継続的改善

### 🔒 セキュアな実装の重要性を理解する
セキュリティベストプラクティスの適用

### 👥 講師サポート
- 各自のペースで進める（全ステップ完了は必須ではない）
- つまずいたら挙手して講師に質問
- 他の参加者と相談・情報共有OK
- 成功したプロンプトの共有を推奨

---

<!-- _class: lead -->

## 演習でよくあるつまずきポイントと対処法

---

<!-- _class: card-grid compact -->

# つまずきポイントと対処法

### ① 要件が曖昧で手が止まる
**原因：** AIに質問させていない
**対処法：** 「曖昧な点を質問して」→AIが逆質問

### ② いきなり実装を始める
**原因：** 前工程の重要性を忘れている
**対処法：** STEP1-2必須実施、急がば回れ

### ③ テストを後回しにする
**原因：** TDD重要性の理解不足
**対処法：** Red-Green-Refactorサイクル厳守

### ④ AI自己レビューをスキップ
**原因：** 時間がないと感じる
**対処法：** 数秒で多くのバグ検出、時間節約

### ⑤ トークン制限エラー
**原因：** .claudeignore不十分
**対処法：** node_modules等除外、/compact実行

### ⑥ AIが間違った方向に進む
**原因：** 受け入れ条件が不明確
**対処法：** こまめに確認・軌道修正

---

<!-- _class: lead compact -->

## 演習成功のチェックリスト

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: card-grid compact -->

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

<!-- _class: card-grid -->

# 演習成功チェックリスト②

**STEP4: 実装**
- ✅ TDD/BDD (Red-Green-Refactor)
- ✅ Given-When-Then形式テスト
- ✅ インクリメンタル開発、頻繁commit
- ✅ 環境変数管理、入力値バリデーション
- ✅ AI自己レビュー実施

**STEP5: 品質担保＆Doc**
- ✅ カバレッジ80%+、E2Eテスト
- ✅ AI観点別レビュー4観点
- ✅ リファクタリング実施
- ✅ Doc生成 (arch/README/CLAUDE)

---

<!-- _class: lead compact -->

## 演習で体感できること

---

<!-- _class: card-grid -->

# 演習で体感できること

### ①前工程の重要性
丁寧にやる→スムーズ、省略→迷う・手戻り

### ②TDDの威力
テストあり→AI自己完結、なし→無限ループ

### ③AI自己レビュー効果
数秒で多数バグ検出、コストゼロ

### ④インクリメンタル開発
小さく→常に動作確認、全部→不安

### ⑤Living Documentation
AIが参照可能、忘れない、間違い防止

---

<!-- _class: lead compact -->

## 演習の成果物

---

<!-- _class: layout-code-focus compact -->

# 成果物：ディレクトリ構成

```
project/
├── docs/     # 要件・設計
├── src/
│   ├── main/ # 本番
│   └── test/ # テスト
├── README.md
├── .env.example
└── .gitignore
```

**📄 Doc:** Given-When-Then、エッジケース網羅
**💻 Code:** カバレッジ80%+、セキュリティ、環境変数

---

<!-- _class: lead compact -->

## 1日目全体の振り返り

---

<!-- _class: card-grid ultracompact -->

# 1日目全体の振り返り

### 午前: 基礎
AI活用3原則、要件定義、設計

### 午後前半: 実践
タスク分解、実装、品質担保

### 午後後半: 演習
5-STEPフロー、TDD、Living Doc

### キーメッセージ
曖昧さ排除、AI思考可視化、急がば回れ

---

<!-- _class: lead -->

## 2日目への準備

---

<!-- _class: card-grid compact -->

# 2日目への準備

### 📅 2日目の内容（予告）

**既存システム改修:**
- リバースエンジニアリング（既存コードから仕様読み解き）
- テストシナリオ一覧作成（モレ・ヌケ防止）
- デグレ防止（既存機能保証）
- 機能追加（実プロジェクトベース）

**1日目との違い:**
1日目は新規開発、2日目は既存改修（理解→追加）

### 📚 1日目の復習推奨

**重要概念:**
✅ 5-STEPフロー各ステップ目的 ✅ AI制約（Jagged Intelligence、Reward Hacking、忘れっぽさ） ✅ Trust but Verify原則

**実践手法:**
✅ TDD/BDD Red-Green-Refactor ✅ AI自己レビュー4観点 ✅ Living Documentation ✅ セキュリティベストプラクティス

### 🏠 宿題（任意）

**Lv1:** TODOアプリ機能追加 **Lv2:** 自分のプロジェクトで5-STEP実践 **Lv3:** AI自己レビュー習慣化、成功プロンプトをCLAUDE.mdに記録
