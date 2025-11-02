---
marp: true
theme: ai-seminar
paginate: true
---

<!-- _class: title supercompact -->

# Day 2-1: 振り返り + リバースエンジニアリング + テストシナリオ + テストコード基礎

## (10:00-12:00)

---

<!-- _class: lead compact -->

## 1日目の振り返り（10分）

---

<!-- _class: card-grid -->

# 5-STEPフローの復習（AI制約への対応）

### STEP1: 要件定義
**Guardrails、曖昧さの排除**

### STEP2: 設計ドキュメント
**外部記憶としてのドキュメント化**

### STEP3: タスク分解
**計画の可視化で手戻り防止**

### STEP4: 実装
**小さく作る・TDD・自己レビュー**

### STEP5: 品質担保＆ドキュメント反映
**Trust but Verify自動化、外部メモリ更新**

---

<!-- _class: card-grid compact -->

# 昨日の演習での気づき共有

### 前工程の重要性を実感
**Guardrails設定で実装スムーズ**

### TDDでAIが自己完結
**テスト実行→修正→成功を自動化**

### AI自己レビューの効果
**ゼロコストで品質向上**

### インクリメンタル開発の安心感
**小さく確実に進め手戻り防止**

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: layout-timeline -->

# 2日目のゴール：既存システムへの高品質な機能追加

<div class="timeline">

<div class="step">
<div class="step-number">1</div>
<h3>リバースエンジニアリング</h3>
<p><strong>30分</strong></p>
<p>既存コードから仕様読み解き</p>
</div>

<div class="step">
<div class="step-number">2</div>
<h3>フィットギャップ分析<br>＆影響範囲調査</h3>
<p><strong>20分</strong></p>
<p>追加開発範囲明確化</p>
</div>

<div class="step">
<div class="step-number">3</div>
<h3>テストシナリオ作成</h3>
<p><strong>30分</strong></p>
<p>既存・新機能・デグレ防止網羅</p>
</div>

<div class="step">
<div class="step-number">4</div>
<h3>テストコード実装<br>＋機能追加</h3>
<p><strong>60分</strong></p>
<p>TDD、AI自己レビュー</p>
</div>

</div>

---
<!-- _class: two-column -->

<!-- _class: lead compact -->

## STEP1: リバースエンジニアリング（30分）

---

<!-- _class: layout-horizontal-right -->

# リバースエンジニアリングとは

![リバースエンジニアリングのプロセス](./assets/diagrams/diagram_12_reverse_engineering.svg)

**既存コードから仕様を読み解く技術**

**なぜ必要か:**
- AIは過去実装を記憶できない
- 仕様書なしで推測実装→デグレ

**基本原則:**
- コードが真実を語る
- ドキュメント化で次開発に活用

**効果:**
- 仕様正確把握
- デグレ防止
- 適切な機能追加

---

<!-- _class: card-grid compact -->

# リバースエンジニアリングの第一歩

### ソースコード読み込み
**プロジェクトルートで`claude`実行**

### .claudeignoreで除外（重要）
**トークン消費最小化**
- node_modules、.git、dist、*.log除外

### AIへの指示例
「プロジェクト構造を教えて」「主要ファイルの役割は？」「アーキテクチャパターンは？」

### 効果
全体像把握、ドキュメント生成準備

---

<!-- _class: layout-horizontal-right -->

# AIの制約を理解する（Jagged Intelligence）

![Jagged Intelligence実例](./assets/diagrams/diagram_38_jagged_intelligence_examples.svg)

**得意:** コード生成、パターン認識、テスト生成

**不得意:** ビジネス判断、設計判断、全体影響判断

**対策:** 明確な指示とGuardrails

---

<!-- _class: layout-horizontal-right -->

# ドキュメント自動生成（Guardrails構築）

![文字起こしアプローチ（トライアル知識の共有）](./assets/diagrams/diagram_40_transcript_approach.svg)

**APIドキュメント (OpenAPI):** 仕様明確化、API整合性保証
**DB定義書:** 正確SQL生成、デグレ防止
**JavaDoc/コメント:** 設計意図伝達、適切拡張
**インデックス (README/architecture.md):** 全体像把握、一貫性確保
**自動生成:** 「OpenAPI仕様書を生成」「テーブル定義書を生成」

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: layout-callout -->

<div class="icon">📋</div>

# 仕様書がない場合の対処法

<div class="message">

**問題:** ドキュメントがない既存システムへの機能追加
- AIが仕様を推測→デグレ、不整合が発生
- どこに何があるか分からない→影響範囲の判断不可

**対策①: 内部仕様書の作成（技術視点）**
- AIへの指示: 「このプロジェクトの内部仕様書を作成して」
- 出力: アーキテクチャパターン、技術スタック、ディレクトリ構成、実装詳細
- ファイル: docs/architecture.md に保存

**対策②: 要件定義書相当の作成（ユーザー視点）**
- AIへの指示: 「このシステムの要件定義書を作成して」
- 出力: ユーザーストーリー、機能一覧、ビジネスロジック、画面フロー
- ファイル: docs/requirements.md に保存

**効果:** AIに既存システムの仕様を理解させる、新機能との整合性を保つ

</div>

---

<!-- _class: layout-horizontal-left -->

# リバースエンジニアリング → 網羅的テスト生成（重要）

![リバースエンジニアリングから網羅的テスト生成](./assets/diagrams/diagram_44_reverse_to_comprehensive_test.svg)

### ❌ 従来（コード追認）
既存コード→直接テスト生成→実装済みのみカバー
**問題:** 既存バグ追認、エッジケース見落とし

### ✅ リバースエンジニアリング
既存コード→要件定義書逆生成→網羅的テストシナリオ
**効果:** あるべき仕様に基づくテスト、未実装検出

### 💡 核心的価値
「あるべき姿」に基づいたテスト、AIが網羅的に生成（正常系・異常系・境界値）、既存バグ・仕様外動作を発見

---

<!-- _class: lead compact -->

## STEP2: フィットギャップ分析＆影響範囲調査

### （20分）

---

<!-- _class: layout-horizontal-right -->

# 既存機能のフィットギャップ分析

![フィットギャップ分析](./assets/diagrams/diagram_18_fit_gap_analysis.svg)

**目的:** 既存vs新機能比較、追加開発範囲明確化

**分析:**
- **Fit:** そのまま使える機能
- **Gap:** 新規実装、拡張箇所
- **Impact:** 既存への影響

**指示:** 「既存○○と新規△△のフィットギャップ分析」

**効果:** 工数見積もり、効率的実装計画

---

<!-- _class: two-column -->

# 影響範囲調査の手法

![影響範囲調査の可視化](./assets/diagrams/diagram_13_impact_analysis.svg)

**なぜ必要:**
AIは局所変更のみ見る→全体影響見落とし→デグレ

**調査項目:**
- **変更ファイル:** Controller/Service/Repository/Entity/View
- **影響テーブル:** カラム追加、制約/インデックス変更
- **連鎖影響:** 他機能、API呼び出し元、画面表示
- **テスト箇所:** 単体/統合/E2Eテスト

**AIへの指示:**
「影響範囲調査。ファイル/テーブル/連鎖影響リストアップ」

**効果:**
デグレ防止、テストシナリオ基礎、安全な追加

---
<!-- _class: two-column -->

<!-- _class: lead compact -->

## STEP3: テストシナリオ一覧作成（30分）

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: layout-callout -->

<div class="icon">📝</div>

# テストシナリオとは

<div class="message">

**「何をテストすべきか」の一覧（Guardrails）**

**なぜ必要:** テストコード生成は得意、シナリオ網羅性は苦手

**役割:** AIへのGuardrails、抜け漏れ防止

**重要:** 実装前に作成

</div>

---

<!-- _class: layout-comparison -->

# テストシナリオとテストコードの違い

<div>

## テストシナリオ：企画書（What）

**「何をテストするか」を記述**

**人間が読みやすい形式**
- Markdown、Excelなど

**ビジネス要件との対応が明確**

**レビューが容易**

</div>

<div class="separator">VS</div>

<div>

## テストコード：実装物（How）

**「どうテストするか」を記述**

**実行可能なコード**
- JUnit、Mockitoなど

**CI/CDで自動実行**

**関係性:**
シナリオ（設計図）→ コード（実装）

</div>

---

<!-- _class: layout-horizontal-right -->

# テストシナリオ → テストコードの順序

![テストシナリオからテストコードへの流れ](./assets/diagrams/diagram_14_scenario_to_code.svg)

### テストシナリオを先に作成（Guardrails構築）
- 全体像を把握→AIは忘れっぽい対策
- モレ・ヌケを防止→Jagged Intelligence対策
- 明確な指針＝AIへのGuardrails

### テストコードを実装
- シナリオに基づいてAIが自動生成
- 確実にカバー

---

<!-- _class: two-column -->

# デグレ防止の重要性

![Reward Hacking実例](./assets/diagrams/diagram_39_reward_hacking_examples.svg)

**既存機能が壊れていないことを保証（Trust but Verify）**

**なぜデグレ:**
- AI忘れっぽい→既存仕様忘却
- 全体影響判断不可
- 新機能優先で既存軽視

**影響:**
本番障害、信頼喪失、修正コスト増

**対策:**
既存主要シナリオをテストに含める、自動テストで継続検証

**効果:**
安心追加、品質保証、障害防止

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: layout-horizontal-right compact -->

# テストシナリオの分類

![テストシナリオの4分類](./assets/diagrams/diagram_15_test_classification.svg)

**正常系（Happy Path）:**
想定入力→期待結果（最重要、最頻使用）

**異常系（Error Handling）:**
不正入力→エラー処理確認（本番障害多発箇所）

**境界値（Boundary）:**
0/MAX/MIN確認（バグ多発ポイント）

**例外処理（Exception）:**
ネットワーク/DB/タイムアウトエラー確認

**効果:**
全観点網羅→本番障害大幅削減

---

<!-- _class: card-grid supercompact -->

# テストシナリオ作成の実例

### ①既存機能（デグレ防止）
**目的:** 既存機能動作確認
**対象:** 主要機能Happy Path
**例:** ログイン、ユーザー登録、一覧、検索

### ②新機能（品質担保）
**目的:** 新機能仕様通り動作確認
**対象:** 正常系・異常系・境界値・例外
**例:** パスワードリセット全テストケース

### ③デグレ防止（連携確認）
**目的:** 既存と新機能の連携確認
**対象:** インターフェース、データ整合性
**例:** ユーザー管理とパスワードリセット連携

---

<!-- _class: lead compact -->

## STEP4: テストコード実装＋機能追加（60分）

### テストコード基礎（復習）

---

<!-- _class: card-grid compact -->

# テストコード基礎（復習）

### TDD/BDD
**Red-Green-Refactorサイクル**
- **Red**: 失敗するテスト先書き
- **Green**: 最小実装でテスト通過
- **Refactor**: 品質向上（重複削減、可読性）

### Given-When-Then形式
**テストの構造化**
- **Given**: テストデータ準備（前提条件）
- **When**: テスト対象メソッド実行
- **Then**: 期待結果アサーション

### テストの独立性
**各テスト独立実行可能**
- 順序依存NG
- 他のテストに影響を与えない（副作用NG）
- @BeforeEach、@AfterEachで初期化・クリーンアップ

### テストカバレッジ
**80%以上を目標**
- 100%は非現実的
- 重要なビジネスロジックを優先

### 効果
品質保証、リファクタリングの安全性、ドキュメントとしての価値

---

<!-- _class: two-column supercompact -->

# テストシナリオからテストコードへ

### なぜシナリオから始める？
**全体像把握→モレ・ヌケ防止**

### 変換プロセス
**シナリオ1つ→テストメソッド1つ**
Given-When-Then形式で記述

### AIへの指示
「シナリオからJUnitテスト生成」

### 効果
漏れなく実装、品質担保

---

<!-- _class: layout-callout -->

<div class="icon">💡</div>

# テストコードの構造（Given-When-Then）

<div class="message">

**なぜGiven-When-Then形式が重要か:**
- テストの意図が明確になる
- AIがテストシナリオからテストコードを自動生成できる
- 人間が読んでも理解しやすく、仕様書としても機能する

**各セクションの役割:**
- **Given:** 前提条件（AIがセットアップコード生成）
- **When:** 実行する操作（AIがメソッド呼び出し生成）
- **Then:** 期待する結果（AIがアサーション生成）

</div>

---

<!-- _class: card-grid -->

# テストカバレッジの考え方（80%以上）

### なぜ80%以上が目標か
**現実的な品質目標**
- 100%は非現実的（Getter/Setterまでテスト不要）
- 80%で主要な機能とエッジケースをカバー
- 残り20%はリスクの低い箇所

### カバレッジツールの価値（Trust but Verify）
**AIのエラーを可視化**
- AIが見落としたテストケースを発見
- AIのエラーを可視化
- 不足箇所を可視化→AIに追加テスト生成を依頼

### 効果
リファクタリング時の安全性確保、デグレ防止の証拠

---

<!-- _class: layout-callout -->

<div class="icon">🤖</div>

# AIによるテストコード自動生成

<div class="message">

**テストシナリオがあることの重要性（Guardrails）:**
- シナリオなし: AIが推測で作る（Jagged Intelligence）→漏れ発生
- シナリオあり: 明確な指針→AIが網羅的に生成→漏れなし

**AIへの指示方法:**
- 「このテストシナリオ一覧に基づいて、JUnitテストコードを生成して」
- AIがシナリオを1つずつテストメソッドに変換
- Given-When-Then形式で自動生成

**人間の役割（Trust but Verify）:**
- テストシナリオの作成（全体像の把握）
- 生成されたテストコードのレビュー
- 不足しているケースの追加指示

</div>
