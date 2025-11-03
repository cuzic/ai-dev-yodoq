---
marp: true
theme: ai-seminar
paginate: true
---
<!-- _class: lead ultracompact -->

## Day 2-2
# 実践演習 + 成果発表 + まとめ
(13:00-17:00)

---

<!-- _class: lead supercompact -->

## 実践演習の説明（10分）

---

<!-- _class: card-grid -->

# 3つの演習課題から選択

### ①マスター追加（商品カテゴリマスタCRUD）
CREATE TABLE、CRUD機能実装、外部キー関連付け
**難易度: 中**（デグレリスク低）

### ②項目追加（顧客に電話番号カラム）
ALTER TABLE、関連画面・API修正、バリデーション追加
**難易度: 高**（影響大、デグレリスク高）

### ③検索条件追加（日付範囲指定検索）
WHERE句拡張、UI・API・SQL修正、境界値処理
**難易度: 中**（既存検索への影響あり）

---

<!-- _class: layout-horizontal-right compact -->

# 演習の進め方（ワークフロー）

![演習ワークフロー](./assets/diagrams/diagram_17_workshop_workflow.svg)

**保守開発の4ステップワークフロー:**
- **STEP1: リバースエンジニアリング（30分）** 仕様把握、Doc自動生成
- **STEP2: フィットギャップ分析＆影響範囲調査（20分）** 追加開発範囲明確化
- **STEP3: テストシナリオ作成（30分）** 既存・新機能・デグレ防止網羅
- **STEP4: テストコード実装＋機能追加（60分）** TDD、AI自己レビュー、Doc反映
- **効果:** 体系的高品質追加、実務再現可能

---

<!-- _class: card-grid -->

# 演習のゴール

### リバースエンジニアリング手法の習得
**既存コードから仕様読解**
- AIに「内部仕様書を作成して」と指示
- ドキュメント不在でも対応可能

### テストシナリオ作成でモレ・ヌケ防止
**正常系・異常系・境界値網羅**
- AIがシナリオ→テストコード自動生成
- 品質担保の仕組み化

### デグレを防ぐ実装手法の体得
**既存機能のテストシナリオ作成**
- デグレ防止テスト自動化
- 安心して機能追加できる体制構築

### 効果
実務で即実践、保守開発の生産性・品質向上

---

<!-- _class: lead compact -->

## 実践演習（3時間）

---

<!-- _class: layout-callout ultracompact -->

<div class="icon">🔍</div>

# STEP1: リバースエンジニアリング（30分）

<div class="message">

**AI指示**: 「内部仕様書作成」
**出力**: 技術スタック、アーキ、DB/API → docs/architecture.md
**効果**: 全体像把握、整合性保証

</div>

---

<!-- _class: card-grid compact -->

# STEP2: フィットギャップ分析＆影響範囲調査（20分）

### 既存機能の理解
- テーブル/API/画面定義・遷移図
- ロジック機能説明

### 影響範囲調査
- 変更ファイル、影響テーブル、連鎖、テスト箇所
- **AI:** 「電話番号追加の影響範囲調査」

### フィットギャップ分析
- 現状→要件比較→Fit/Gap明確化
- **出力:** Fit=既存CRUD、Gap=カラム/バリデ/画面

---

<!-- _class: lead compact -->

## STEP3: テストシナリオ一覧作成（30分）

---

<!-- _class: layout-callout -->

<div class="icon">✅</div>

# 既存機能のテストシナリオ作成

<div class="message">

**目的:** 既存機能が壊れていないことを保証（デグレ防止）

**対象:** 既存機能の主要な機能（ログイン、ユーザー登録、一覧、検索など）

**観点:** 正常系・異常系・境界値

**AI指示:** 「既存のログイン機能のテストシナリオを作成。正常系、異常系、境界値含む」

**出力:** Markdown形式

**効果:** デグレ防止、安心変更

</div>

---

<!-- _class: card-grid supercompact -->

# 新機能のテストシナリオ作成

### 目的
新機能が仕様通り動作することを保証

### 対象：全テストケース
正常系・異常系・境界値・例外処理を網羅

### AI指示
「〇〇機能のテストシナリオ作成」
「正常系、異常系、境界値、例外を網羅」

### 出力形式
Given-When-Then形式

### 効果
品質担保、バグ検出率向上

---

<!-- _class: layout-horizontal-right ultracompact -->

# デグレ防止のテストシナリオ

![デグレ防止の3層構造](./assets/diagrams/diagram_16_regression_prevention.svg)

**目的:** 既存と新機能の連携確認

**対象:**
既存機能、インターフェース、データ整合性

**具体例:**
既存登録動作、データ表示、新規保存

**AI指示:** 連携テストシナリオ作成

**効果:** デグレゼロ

---

<!-- _class: layout-horizontal-left ultracompact -->

# デグレ発生メカニズムとTDDによる予防

![デグレ発生メカニズムとTDD予防](./assets/diagrams/diagram_42_regression_mechanism.svg)

### デグレが起きる3つの原因
AIは忘れっぽい、影響範囲判断不可、新機能優先

### TDD予防
テストあれば→AI自動検証、デグレ大幅削減

### 効果
安心機能追加、品質保証

---

<!-- _class: lead -->

## STEP4: テストコード実装＋機能追加（60分）

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: layout-timeline -->

# テストコード実装（30分）

<div class="timeline">

<div class="step">
<div class="step-number">1</div>
<h3>AIへの指示</h3>
<p>「このテストシナリオ一覧に基づいて、JUnitテストコードを生成して」</p>
<p>「Given-When-Then形式で、Mockitoを使ってモックを作成して」</p>
</div>

<div class="step">
<div class="step-number">2</div>
<h3>生成されるテストコード</h3>
<p>シナリオ1つ→1テストメソッド</p>
<p>Given-When-Then構造化</p>
</div>

<div class="step">
<div class="step-number">3</div>
<h3>テストカバレッジ目標</h3>
<p>80%以上</p>
<p>JaCoCoで確認</p>
</div>

<div class="step">
<div class="step-number">4</div>
<h3>効果</h3>
<p>自動テスト</p>
<p>CI/CD統合</p>
<p>継続的品質保証</p>
</div>

</div>

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: layout-timeline -->

# 機能追加実装：TDDで実装（30分）

<div class="timeline">

<div class="step">
<div class="step-number">R</div>
<h3>Red</h3>
<p><strong>失敗するテストを書く</strong></p>
<p>テストシナリオ→テストコード作成</p>
<p>実装がないので当然失敗</p>
</div>

<div class="step">
<div class="step-number">G</div>
<h3>Green</h3>
<p><strong>最小実装</strong></p>
<p>テストが通る最小限のコード実装</p>
<p>「このテストが通るように実装して」</p>
</div>

<div class="step">
<div class="step-number">R</div>
<h3>Refactor</h3>
<p><strong>改善</strong></p>
<p>重複削除、可読性向上、最適化</p>
<p>「このコードをリファクタリングして」</p>
</div>

<div class="step">
<div class="step-number">✓</div>
<h3>AI自己レビュー</h3>
<p><strong>必須</strong></p>
<p>各ステップで「このコードをレビューして」</p>
<p>セキュリティ、エラー処理、エッジケース、ベストプラクティスチェック</p>
</div>

</div>

---

<!-- _class: card-grid compact -->

# テスト実行・デバッグ

### 全テスト実行
**一括実行**
- `mvn test` または `./gradlew test` で一括実行
- CI/CDで自動実行

### テスト失敗箇所の修正
**AIに依頼**
- 失敗エラーメッセージをAIに渡す
- 「このテスト失敗を修正して」

### AIが自己完結してデバッグ
**自動デバッグサイクル**
- エラーログ解析→原因特定→修正コード生成→再テスト

### テストカバレッジ確認
**不足箇所の特定**
- JaCoCo確認（`mvn jacoco:report`）
- 80%未満箇所特定→追加テスト

### 効果
自動デバッグ、品質担保、継続的改善

---
<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->


<!-- _class: layout-horizontal-right compact -->

# ドキュメント反映

![ドキュメント自動生成Before/After](./assets/diagrams/diagram_43_doc_automation_before_after.svg)

**architecture.md更新:** テーブル、API、画面記録
**README.md更新:** セットアップ、使い方記録
**知見の記録:** ハマった点、解決方法、ベストプラクティス
**Living Documentation:** ドキュメント＝AIの外部メモリ
**効果:** 知見蓄積、チーム共有、再現可能な開発

---

<!-- _class: lead supercompact -->

## 成果発表・ディスカッション（20分）

---

<!-- _class: two-column -->

# 代表者2-3名の成果発表

### 選択した課題と実装内容
どの課題を選んだか、何を実装したか

### リバースエンジニアリングで分かったこと
既存システムの構造、特徴、課題

### テストシナリオ作成での工夫
どのような観点でシナリオを作成したか

### 実装での工夫
TDD、AI自己レビュー、デグレ防止の実践

---

<!-- _class: two-column -->

# つまづいたポイント共有

### どこでつまづいたか
具体的なつまづきポイント

### どう解決したか
解決方法、使ったプロンプト

### 学んだこと
この経験から得た学び

---

<!-- _class: card-grid ultracompact -->

# うまくいったポイント共有

### リバースエンジニアリング
効果的AI指示

### テストシナリオ作成
網羅手法

### AI活用方法
生産性プロンプト

### デグレ防止の工夫
既存機能保護

---

<!-- _class: card-grid ultracompact -->

# 全体ディスカッション

### 参加者質問
実装・解決方法

### 講師フィードバック
良い点・改善点

### ベストプラクティス
成功事例・プロンプト

---

<!-- _class: lead -->

## まとめ（30分）

---

<!-- _class: layout-diagram-only ultracompact -->

# 2日間の総まとめ

![2日間の学習構造](./assets/diagrams/diagram_20_2day_summary.svg)

### 1日目：新規開発の5-STEP
STEP1-2: 要件・設計（Guardrails、曖昧さ排除）| STEP3: タスク分解（AI思考言語化）| STEP4: 実装（TDD、AI自己レビュー）| STEP5: 品質担保＆Doc

### 2日目：保守開発の4ステップ
1.リバースエンジニアリング 2.フィットギャップ分析＆影響範囲調査 3.テストシナリオ作成 4.テストコード実装＋機能追加

---

<!-- _class: card-grid -->

# 実務での活用ポイント

### 曖昧さを排除
- STEP1-2を丁寧に実施
- AIに質問させる手法活用
- 受け入れ条件を明確化

### AIの思考を可視化
- タスク分解で計画作成
- 早期の軌道修正
- 計画図面と完成図面

### TDDで品質担保
- Red-Green-Refactor
- AIの自己完結性向上
- カバレッジ80%以上

### 知見を蓄積
- Living Documentation
- architecture.md、README
- CLAUDE.mdにプロンプト蓄積

---

<!-- _class: layout-horizontal-right -->

# よくある失敗と対策

![よくある失敗パターンと対策](./assets/diagrams/diagram_19_common_failures.svg)

### ①いきなりコード
- **失敗:** STEP1-2スキップ→何度も作り直し
- **対策:** 前工程丁寧に（10分要件+15分設計）

### ②セキュリティ後回し
- **失敗:** 本番脆弱性（平文、SQLi、XSS）
- **対策:** 最初から要件明記（bcrypt、HTTPS、OWASP）

### ③レビュースキップ
- **失敗:** バグ多発
- **対策:** 「このコードをレビューして」習慣化→多くのバグ検出

### ④タスク大きすぎ
- **対策:** 30分〜2時間粒度、Gitコミット単位

### ⑤ドキュメント未更新
- **対策:** Living Documentation習慣化

---

<!-- _class: card-grid -->

# 実務で明日から実践（Top 5）

①**AI自己レビュー**: 「コードをレビューして」習慣化
②**受入条件**: Given-When-Then形式で曖昧さ排除
③**環境変数**: .envで秘密管理、.env.exampleコミット
④**頻繁commit**: 1機能→即コミット、AI暴走防止
⑤**テスト先行**: シナリオ→コード、モレヌケ防止

---

<!-- _class: layout-horizontal-right -->

# 今後の学習ロードマップ

![学習ロードマップ](./assets/diagrams/diagram_21_learning_roadmap.svg)

### ステップ1: 小プロジェクト3つ
TODO/メモ/簡易ECなど、5-STEP実践、TDD習慣化

### ステップ2: 中規模プロジェクト
複数テーブル・画面、認証・認可、E2Eテスト

### ステップ3: 既存リファクタリング
リバースエンジニアリング、デグレ防止、技術的負債解消

### ステップ4: チーム開発
5-STEP運用、プロンプト共有、Living Documentation浸透

---

<!-- _class: layout-callout -->

<div class="icon">❓</div>

# 質疑応答

<div class="message">

**2日間の学びについての質問**

**実務での適用についての相談**

**今後の学習方針についてのアドバイス**

**その他、AIを活用した開発全般について**

</div>
