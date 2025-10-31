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

# Day 2-1: 振り返り + リバースエンジニアリング + テストシナリオ + テストコード基礎 (10:00-12:00)

---

<!-- _class: lead -->

## 1日目の振り返り（10分）

---

### 5-STEPフローの復習（AI制約への対応）
- STEP1: 要件定義（Guardrails、曖昧さの排除）
- STEP2: 設計ドキュメント（Guardrails、AIは忘れっぽい対策）
- STEP3: タスク分解（AIの思考を言語化、全体像把握）
- STEP4: 実装（小さく作る・TDD・AI自己レビュー必須）
- STEP5: 品質担保＆ドキュメント反映（Trust but Verify自動化、Living Documentation＝外部メモリ）

---

### 昨日の演習での気づき共有
- 前工程の重要性を実感（Guardrails設定の効果）
- TDDでAIが自己完結する様子を体験（Trust but Verify自動化）
- AI自己レビューの効果を確認（多くのバグを検出）
- インクリメンタル開発の安心感（AIは忘れっぽい対策）

---

### 2日目のゴール
- **既存システムへの機能追加を高品質に行う**

**保守開発の4ステップワークフロー:**
1. **リバースエンジニアリング（30分）:** 既存コードから仕様を読み解く
2. **フィットギャップ分析＆影響範囲調査（20分）:** 追加開発範囲の明確化
3. **テストシナリオ作成（30分）:** 既存機能・新機能・デグレ防止を網羅
4. **テストコード実装＋機能追加（60分）:** TDD、AI自己レビュー

---

---

<!-- _class: lead -->

## STEP1: リバースエンジニアリング（30分）

---

<!-- _class: layout-horizontal-right -->

### リバースエンジニアリングとは

![リバースエンジニアリングのプロセス](diagrams/diagram_12_reverse_engineering.svg)

- **既存コードから仕様を読み解く技術**
- **なぜ必要か:** AIは過去実装を記憶できない、仕様書なしで推測実装→デグレ
- **基本原則:** コードが真実を語る、ドキュメント化で次開発に活用
- **効果:** 仕様正確把握、デグレ防止、適切な機能追加

---

### リバースエンジニアリングの第一歩
- **ソースコード読み込み**
  - Claude Codeでプロジェクト全体を読み込む
  - プロジェクトルートで`claude`コマンド実行→自動的に全ファイルスキャン
- **.claudeignoreで不要ファイルを除外（重要）**
  - node_modules、.git、ビルド成果物、ログファイルを除外
  - トークン消費を最小化（コスト削減＋AIの集中力維持）
  - 例: `echo "node_modules/\ndist/\n.git/\n*.log" > .claudeignore`
- **AIへの指示例:**
  - 「このプロジェクトの構造を教えて」
  - 「主要なファイルとその役割をリストアップして」
  - 「アーキテクチャパターンは何を使っている？」
- **効果:** プロジェクト全体像の把握、次のステップ（ドキュメント生成）への準備

---

---

<!-- _class: layout-horizontal-left -->

### AIの制約を理解する（Jagged Intelligence）

![Jagged Intelligence実例](diagrams/diagram_38_jagged_intelligence_examples.svg)

- **AIの得意・不得意を理解**
  - 得意: コード生成、パターン認識、テスト生成
  - 不得意: ビジネス判断、設計判断、全体への影響判断
- **対策: 明確な指示とGuardrails**

---

---

<!-- _class: layout-horizontal-right -->

### ドキュメント自動生成（Guardrails構築）

![文字起こしアプローチ（トライアル知識の共有）](diagrams/diagram_40_transcript_approach.svg)

- **APIドキュメント（OpenAPI）:** 仕様明確化、既存API整合性保証
- **DB定義書:** 正確なSQL生成、デグレ防止
- **JavaDoc/コメント:** 設計意図伝達、適切な拡張
- **インデックス（README/architecture.md）:** 全体像把握、一貫性確保
- **自動生成:** 「OpenAPI仕様書を生成」「テーブル定義書を生成」

---

### 仕様書がない場合の対処法
- **問題:** ドキュメントがない既存システムへの機能追加
  - AIが仕様を推測→デグレ、不整合が発生
  - どこに何があるか分からない→影響範囲の判断不可
- **対策①: 内部仕様書の作成（技術視点）**
  - AIへの指示: 「このプロジェクトの内部仕様書を作成して」
  - 出力: アーキテクチャパターン、技術スタック、ディレクトリ構成、実装詳細
  - ファイル: docs/architecture.md に保存
- **対策②: 要件定義書相当の作成（ユーザー視点）**
  - AIへの指示: 「このシステムの要件定義書を作成して」
  - 出力: ユーザーストーリー、機能一覧、ビジネスロジック、画面フロー
  - ファイル: docs/requirements.md に保存
- **効果:** AIに既存システムの仕様を理解させる、新機能との整合性を保つ

---

<!-- _class: layout-horizontal-left -->

### リバースエンジニアリング → 網羅的テスト生成（重要）

![リバースエンジニアリングから網羅的テスト生成](diagrams/diagram_44_reverse_to_comprehensive_test.svg)

- **❌ 従来のアプローチ（コード追認のみ）**
  - 既存コード→直接テスト生成→実装済み機能のみカバー
  - 問題: 既存バグも追認、エッジケース見落とし、仕様外の動作を検出できない
- **✅ リバースエンジニアリング（仕様逆生成）**
  - 既存コード→要件定義書・ユーザーストーリー逆生成→網羅的テストシナリオ
  - 効果: あるべき仕様に基づくテスト、未実装のエッジケースも検出、仕様外の動作を発見
- **💡 核心的価値:**
  - コードの追認ではなく「あるべき姿」に基づいたテストが可能
  - AIは仕様から網羅的にテストを生成（正常系・異常系・境界値すべて）
  - 既存コードのバグや仕様外の動作を発見できる

---

---

<!-- _class: lead -->

## STEP2: フィットギャップ分析＆影響範囲調査（20分）

---

<!-- _class: layout-horizontal-right -->

### 既存機能のフィットギャップ分析

![フィットギャップ分析](diagrams/diagram_18_fit_gap_analysis.svg)

- **目的:** 既存vs新機能比較、追加開発範囲明確化
- **分析項目:**
  - **Fit:** そのまま使える機能、流用コード
  - **Gap:** 新規実装、既存拡張、修正箇所
  - **Impact:** 既存への影響、連鎖的変更
- **AIへの指示:** 「既存○○と新規△△のフィットギャップ分析」
- **効果:** 工数見積もり、リスク管理、効率的実装計画

---

---

<!-- _class: layout-horizontal-right -->

### 影響範囲調査の手法

![影響範囲調査の可視化](diagrams/diagram_13_impact_analysis.svg)

- **なぜ必要:** AIは局所変更のみ見る→全体影響見落とし→デグレ
- **調査項目:**
  - **変更ファイル:** Controller/Service/Repository/Entity/View
  - **影響テーブル:** カラム追加、制約/インデックス変更
  - **連鎖影響:** 他機能、API呼び出し元、画面表示
  - **テスト箇所:** 単体/統合/E2Eテスト
- **AIへの指示:** 「影響範囲調査。ファイル/テーブル/連鎖影響リストアップ」
- **効果:** デグレ防止、テストシナリオ基礎、安全な追加

---

---

<!-- _class: lead -->

## STEP3: テストシナリオ一覧作成（30分）

---

### テストシナリオとは
- **「何をテストすべきか」の一覧（Guardrails）**
- **なぜ必要か**
  - テストコード生成は得意だが、テストシナリオの網羅性保証は苦手（見落とし多発）
  - シナリオなし→AIが推測でテスト作成→モレ・ヌケ、重複、偏り
  - シナリオあり→網羅的にテスト生成、品質担保
- **テストシナリオの役割:**
  - AIへのテスト設計のGuardrails（何をテストするか明示）
  - テストケースの抜け漏れ防止（正常系・異常系・境界値を網羅）
  - レビューのしやすさ（人間が確認しやすい形式）
- **重要:** 実装前に作成（実装後だと実装に引きずられる）
- **効果:** 高品質なテスト、バグ検出率向上、デグレ防止

---

---

### テストシナリオとテストコードの違い
- **テストシナリオ：企画書（What）**
  - 「何をテストするか」を記述（例: 「ログイン機能の正常系」）
  - 人間が読みやすい形式（Markdown、Excelなど）
  - ビジネス要件との対応が明確
  - レビューが容易（ステークホルダーも確認可能）
- **テストコード：実装物（How）**
  - 「どうテストするか」を記述（例: `@Test void testLoginSuccess() {...}`）
  - 実行可能なコード（JUnit、Mockitoなど）
  - CI/CDで自動実行
- **関係性:** テストシナリオ（設計図）→ テストコード（実装）
- **効果:** テストシナリオで全体像把握→AIがテストコード自動生成

---

---

<!-- _class: layout-horizontal-right -->

### テストシナリオ → テストコードの順序

![テストシナリオからテストコードへの流れ](diagrams/diagram_14_scenario_to_code.svg)

- **テストシナリオを先に作成（Guardrails構築）**
  - 全体像を把握→AIは忘れっぽい対策
  - モレ・ヌケを防止→Jagged Intelligence対策
  - 明確な指針＝AIへのGuardrails
- **テストコードを実装**
  - シナリオに基づいてAIが自動生成
  - 確実にカバー

---

---

<!-- _class: layout-horizontal-right -->

### デグレ防止の重要性

![Reward Hacking実例](diagrams/diagram_39_reward_hacking_examples.svg)

- **既存機能が壊れていないことを保証（Trust but Verify）**
- **なぜデグレ:** AI忘れっぽい→既存仕様忘却、全体影響判断不可、新機能優先で既存軽視
- **影響:** 本番障害、信頼喪失、修正コスト増
- **対策:** 既存主要シナリオをテストに含める、自動テストで継続検証
- **効果:** 安心追加、品質保証、障害防止

---

---

<!-- _class: layout-horizontal-right -->

### テストシナリオの分類

![テストシナリオの4分類](diagrams/diagram_15_test_classification.svg)

- **正常系（Happy Path）:** 想定入力→期待結果（最重要、最頻使用）
- **異常系（Error Handling）:** 不正入力→エラー処理確認（本番障害多発箇所）
- **境界値（Boundary）:** 0/MAX/MIN確認（バグ多発ポイント）
- **例外処理（Exception）:** ネットワーク/DB/タイムアウトエラー確認
- **効果:** 全観点網羅→本番障害大幅削減

---

<!-- _class: card-grid -->

# テストシナリオ作成の実例

### ①既存機能（デグレ防止）
- **目的:** 既存機能動作確認
- **対象:** 主要機能Happy Path
- **例:** ログイン、ユーザー登録、一覧、検索

### ②新機能（品質担保）
- **目的:** 新機能仕様通り動作確認
- **対象:** 正常系・異常系・境界値・例外
- **例:** パスワードリセット全テストケース

### ③デグレ防止（連携確認）
- **目的:** 既存と新機能の連携確認
- **対象:** インターフェース、データ整合性
- **例:** ユーザー管理とパスワードリセット連携

---

---

<!-- _class: lead -->

## STEP4: テストコード実装＋機能追加（60分）

### テストコード基礎（復習）

---

<!-- _class: two-column -->

# テストコード基礎（復習）

### TDD/BDD
- **Red**: 失敗するテスト先書き
- **Green**: 最小実装でテスト通過
- **Refactor**: 品質向上（重複削除、可読性）

### Given-When-Then形式
- **Given**: テストデータ準備（前提条件）
- **When**: テスト対象メソッド実行
- **Then**: 期待結果アサーション

### テストの独立性
- 各テスト独立実行可能（順序依存NG）
  - 他のテストに影響を与えない（副作用NG）
  - @BeforeEach、@AfterEachで初期化・クリーンアップ
- **テストカバレッジ**
  - 80%以上を目標（100%は非現実的）
  - 重要なビジネスロジックを優先
- **効果:** 品質保証、リファクタリングの安全性、ドキュメントとしての価値

---

<!-- _class: two-column -->

# テストシナリオからテストコードへ

### なぜシナリオから始める？
- 全体像把握→モレ・ヌケ防止
- 設計書としてAIがコード生成
- 人間がレビューしやすい

### 変換プロセス
1. シナリオ1つ→テストメソッド1つ
2. Given-When-Then形式で記述
3. トレーサビリティ確保

### AIへの指示
「このテストシナリオ一覧に基づいてJUnitテストコード生成」

### 効果
漏れなく実装、品質担保、保守性向上

---

### テストコードの構造（Given-When-Then）
- **なぜGiven-When-Then形式が重要か**
  - テストの意図が明確になる
  - AIがテストシナリオからテストコードを自動生成できる
  - 人間が読んでも理解しやすく、仕様書としても機能する
- **各セクションの役割**
  - Given: 前提条件（AIがセットアップコード生成）
  - When: 実行する操作（AIがメソッド呼び出し生成）
  - Then: 期待する結果（AIがアサーション生成）

---

### テストカバレッジの考え方（80%以上）
- **なぜ80%以上が目標か**
  - 100%は非現実的（Getter/Setterまでテスト不要）
  - 80%で主要な機能とエッジケースをカバー
  - 残り20%はリスクの低い箇所
- **カバレッジツールの価値（Trust but Verify）**
  - AIが見落としたテストケースを発見
  - AIのエラーを可視化
  - 不足箇所を可視化→AIに追加テスト生成を依頼
- リファクタリング時の安全性確保、デグレ防止の証拠

---

### AIによるテストコード自動生成
- **テストシナリオがあることの重要性（Guardrails）**
  - シナリオなし: AIが推測で作る（Jagged Intelligence）→漏れ発生
  - シナリオあり: 明確な指針→AIが網羅的に生成→漏れなし
- **AIへの指示方法**
  - 「このテストシナリオ一覧に基づいて、JUnitテストコードを生成して」
  - AIがシナリオを1つずつテストメソッドに変換
  - Given-When-Then形式で自動生成
- **人間の役割（Trust but Verify）**
  - テストシナリオの作成（全体像の把握）
  - 生成されたテストコードのレビュー
  - 不足しているケースの追加指示
