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

# Day 2-2: 実践演習 + 成果発表 + まとめ (13:00-17:00)

---

<!-- _class: lead -->

## 実践演習の説明（10分）

---

<!-- _class: card-grid -->

# 3つの演習課題から選択

### ①マスター追加（商品カテゴリマスタのCRUD）
- 新しいマスタテーブル追加（CREATE TABLE）
- CRUD機能実装（Controller、Service、Repository、Entity、View）
- 既存マスタとの関連付け（外部キー）
- **難易度: 中**（デグレリスク低）

### ②項目追加（顧客に電話番号カラム追加）
- 既存テーブルへのカラム追加（ALTER TABLE）
- 関連画面・API修正（登録、更新、一覧、詳細）
- バリデーション追加（電話番号形式チェック）
- **難易度: 高**（影響大、デグレリスク高）

### ③検索条件追加（日付範囲指定検索）
- 既存検索への条件追加（WHERE句拡張）
- UI・API・SQL修正（日付ピッカー、パラメータ、クエリ）
- 境界値処理（開始日・終了日チェック）
- **難易度: 中**（既存検索への影響あり）

---

---

<!-- _class: layout-horizontal-right -->

### 演習の進め方（ワークフロー）

![演習ワークフロー](diagrams/diagram_17_workshop_workflow.svg)

**保守開発の4ステップワークフロー:**
- **STEP1: リバースエンジニアリング（30分）** 仕様把握、ドキュメント自動生成
- **STEP2: フィットギャップ分析＆影響範囲調査（20分）** 追加開発範囲の明確化
- **STEP3: テストシナリオ作成（30分）** 既存機能・新機能・デグレ防止を網羅
- **STEP4: テストコード実装＋機能追加（60分）** TDD、Red-Green-Refactor、AI自己レビュー、ドキュメント反映
- **効果:** 体系的高品質追加、実務再現可能

---

---

<!-- _class: two-column -->

### 演習のゴール

#### リバースエンジニアリング手法の習得
- 既存コードから仕様読解
- AIに「内部仕様書を作成して」と指示
- ドキュメント不在でも対応可能

#### テストシナリオ作成でモレ・ヌケ防止
- 正常系・異常系・境界値網羅
- AIがシナリオ→テストコード自動生成
- 品質担保の仕組み化

#### デグレを防ぐ実装手法の体得
- 既存機能のテストシナリオ作成
- デグレ防止テスト自動化
- 安心して機能追加できる体制構築

**効果:** 実務で即実践、保守開発の生産性・品質向上

---

---

<!-- _class: lead -->

## 実践演習（3時間）

---

<!-- _class: three-column -->

### STEP1: リバースエンジニアリング（30分）

#### 既存コードから仕様を読み解く
- **AI指示:** 「内部仕様書作成」「要件定義書作成」
- **出力:** 技術スタック、アーキテクチャ、DB/API仕様
- **保存先:** docs/architecture.md、requirements.md
- **効果:** 全体像把握、整合性保証

---

---

### STEP2: フィットギャップ分析＆影響範囲調査（20分）

#### 既存機能の理解
- **テーブル:** 「全テーブル定義をMarkdown出力」
- **API:** 「全エンドポイントをOpenAPI出力」
- **画面:** 「画面一覧と遷移図作成」
- **ビジネスロジック:** 「○○機能を説明」

#### 影響範囲調査
- **目的:** 変更箇所・影響把握、デグレ防止
- **調査項目:** 変更ファイル、影響テーブル、連鎖影響、テスト箇所
- **AI指示:** 「電話番号カラム追加の影響範囲調査」

#### フィットギャップ分析
- **目的:** 追加開発範囲明確化
- **プロセス:** 現状確認→要件比較→Fit/Gap明確化
- **AI指示:** 「顧客管理と電話番号追加のフィットギャップ分析」
- **出力例:** Fit=既存CRUD流用、Gap=カラム追加/バリデーション/画面修正

---

---

### STEP3: テストシナリオ一覧作成（30分）

---

#### 既存機能のテストシナリオ作成
- **目的:** 既存機能が壊れていないことを保証（デグレ防止）
- **対象:** 既存機能の主要な機能をカバー
  - ログイン、ユーザー登録、データ一覧、検索など
  - よく使われる機能を優先
- **観点:** 正常系・異常系・境界値
- **AIへの指示:**
  - 「既存のログイン機能のテストシナリオを作成して」
  - 「正常系、異常系、境界値を含めて」
- **出力形式:** Markdown形式でテストシナリオ一覧
- **効果:** デグレ防止、安心して変更可能

---

<!-- _class: two-column -->

#### 新機能のテストシナリオ作成

**目的:** 新機能が仕様通り動作することを保証

**対象:** 新規追加機能の全テストケース
- 正常系: 期待通りの動作確認
- 異常系: エラーハンドリング確認
- 境界値: 0、MAX、MINでの動作確認
- 例外処理: ネットワーク、DB接続エラー

**AIへの指示:**
- 「電話番号カラム追加機能のテストシナリオを作成して」
- 「正常系、異常系、境界値、例外処理を網羅して」

**出力形式:** Given-When-Then形式でシナリオ記述

**効果:** 新機能の品質担保、バグ検出率向上

---

<!-- _class: layout-horizontal-right -->

#### デグレ防止のテストシナリオ

![デグレ防止の3層構造](diagrams/diagram_16_regression_prevention.svg)

- **目的:** 既存と新機能の連携確認
- **対象:** 既存機能動作確認、インターフェース、データ整合性
- **具体例（電話番号追加）:** 既存顧客登録動作、既存データ表示、新規登録保存
- **AI指示:** 「顧客管理と電話番号カラムの連携テストシナリオ作成」
- **効果:** デグレゼロ、シームレス統合

---

<!-- _class: layout-horizontal-left -->

#### デグレ発生メカニズムとTDDによる予防

![デグレ発生メカニズムとTDD予防](diagrams/diagram_42_regression_mechanism.svg)

- **デグレが起きる3つの原因**
  - AIは忘れっぽい→既存仕様を忘れる
  - Jagged Intelligence→影響範囲を判断できない
  - Reward Hacking→新機能優先、既存機能軽視
- **TDDによる予防**
  - テストがあれば→AIが自動で検証
  - デグレを大幅削減
- **効果:** 安心して機能追加、品質保証

---

---

---

### STEP4: テストコード実装＋機能追加（60分）

---

<!-- _class: three-column -->

#### テストコード実装（30分）

**AIへの指示:**
- 「このテストシナリオ一覧に基づいて、JUnitテストコードを生成して」
- 「Given-When-Then形式で、Mockitoを使ってモックを作成して」

**生成されるテストコード:**
- シナリオ1つ→1テストメソッド
- Given（前提条件）: @BeforeEach、テストデータ準備
- When（実行）: テスト対象メソッド呼び出し
- Then（検証）: assertEquals、assertThrows

**テストカバレッジ目標:** 80%以上
- JaCoCoで確認
- 不足箇所特定→追加テスト作成

**効果:** 自動テスト、CI/CD統合、継続的品質保証

---

---

#### 機能追加実装（30分）

---

<!-- _class: two-column -->

#### TDDで実装

**Red（失敗するテストを書く）**
- テストシナリオ→テストコード作成
- 実装がないので当然失敗

**Green（最小実装）**
- テストが通る最小限のコード実装
- 「このテストが通るように実装して」

**Refactor（改善）**
- 重複削除、可読性向上、最適化
- 「このコードをリファクタリングして」

**AI自己レビュー必須**
- 各ステップで「このコードをレビューして」
- セキュリティ、エラー処理、エッジケース、ベストプラクティスチェック

**効果:** 高品質、バグ率低下、保守性向上

---

<!-- _class: two-column -->

#### テスト実行・デバッグ

**全テスト実行**
- `mvn test` または `./gradlew test` で一括実行
- CI/CDで自動実行

**テスト失敗箇所の修正**
- 失敗エラーメッセージをAIに渡す
- 「このテスト失敗を修正して」

**AIが自己完結してデバッグ**
- エラーログ解析→原因特定→修正コード生成→再テスト

**テストカバレッジ確認**
- JaCoCo確認（`mvn jacoco:report`）
- 80%未満箇所特定→追加テスト

**効果:** 自動デバッグ、品質担保、継続的改善

---

<!-- _class: layout-horizontal-right -->

#### ドキュメント反映

![ドキュメント自動生成Before/After](diagrams/diagram_43_doc_automation_before_after.svg)

- **architecture.md更新:** テーブル、API、画面記録
  - AI指示: 「変更内容をarchitecture.mdに反映して」
- **README.md更新:** セットアップ、使い方記録
  - AI指示: 「新機能の使い方をREADME.mdに追加」
- **知見の記録:** ハマった点、解決方法、ベストプラクティス
- **Living Documentation:** ドキュメント＝AIの外部メモリ
- **効果:** 知見蓄積、チーム共有、再現可能な開発

---

---

<!-- _class: lead -->

## 成果発表・ディスカッション（20分）

---

### 代表者2-3名の成果発表
- 選択した課題と実装内容
- リバースエンジニアリングで分かったこと
- テストシナリオ作成での工夫
- 実装での工夫

---

### つまづいたポイント共有
- どこでつまづいたか
- どう解決したか
- 学んだこと

---

### うまくいったポイント共有
- リバースエンジニアリングの成功事例
- テストシナリオ作成の工夫
- AIの活用方法
- デグレ防止の工夫

---

### 全体ディスカッション
- 他の参加者からの質問
- 講師からのフィードバック
- ベストプラクティスの共有

---

---

<!-- _class: lead -->

## まとめ（30分）

---

<!-- _class: image-top-compact -->

# 2日間の総まとめ

![2日間の学習構造](diagrams/diagram_20_2day_summary.svg)

### 1日目：新規開発の5-STEP
- STEP1-2: 要件・設計（Guardrails、曖昧さ排除）
- STEP3: タスク分解（AI思考言語化）
- STEP4: 実装（TDD、AI自己レビュー）
- STEP5: 品質担保＆ドキュメント反映（Trust but Verify、Living Documentation）

### 2日目：保守開発の4ステップ
1. リバースエンジニアリング（既存仕様読解）
2. フィットギャップ分析＆影響範囲調査（追加開発範囲明確化）
3. テストシナリオ作成（モレ・ヌケ防止）
4. テストコード実装＋機能追加（デグレ防止）

---

---

### 実務での活用ポイント

#### 曖昧さを排除
- STEP1-2を丁寧に実施
- AIに質問させる手法を活用
- 受け入れ条件を明確化

#### AIの思考を可視化
- タスク分解で計画を作成
- 早い段階での軌道修正
- 計画図面と完成図面

#### TDDで品質担保
- Red-Green-Refactorサイクル
- AIの自己完結性向上
- テストカバレッジ80%以上

#### 知見を蓄積
- Living Documentation
- architecture.md、README.md
- プロンプトパターンの蓄積（CLAUDE.md）

---

---

<!-- _class: layout-horizontal-right -->

### よくある失敗と対策

![よくある失敗パターンと対策](diagrams/diagram_19_common_failures.svg)

#### ①いきなりコード
- 失敗: STEP1-2スキップ→何度も作り直し
- 対策: 前工程丁寧に（10分要件+15分設計）

#### ②セキュリティ後回し
- 失敗: 本番脆弱性（平文、SQLi、XSS）
- 対策: 最初から要件明記（bcrypt、HTTPS、OWASP）

#### ③レビュースキップ
- 失敗: バグ多発
- 対策: 「このコードをレビューして」習慣化→多くのバグ検出

#### ④タスク大きすぎ
- 対策: 30分〜2時間粒度、Gitコミット単位

#### ⑤ドキュメント未更新
- 対策: Living Documentation習慣化

---

---

<!-- _class: two-column -->

### 実務で明日から実践できること（Top 5）

#### ①AI自己レビューの習慣化
- 実装後必ず「このコードをレビューして」
- バグ検出率向上

#### ②受け入れ条件の明確化
- Given-When-Then形式
- 曖昧さ排除→AI制約対策

#### ③環境変数管理の徹底
- .envで秘密情報管理
- .env.exampleをGitコミット

#### ④頻繁なコミット
- 1機能完了→コミット
- AI暴走対策

#### ⑤テストシナリオを先に作る
- シナリオ→テストコード
- モレ・ヌケ防止

---

---

<!-- _class: layout-horizontal-right -->

### 今後の学習ロードマップ

![学習ロードマップ](diagrams/diagram_21_learning_roadmap.svg)

#### ステップ1: 小プロジェクト3つ
- TODO/メモ/簡易ECなど、5-STEP実践、TDD習慣化

#### ステップ2: 中規模プロジェクト
- 複数テーブル・画面、認証・認可、E2Eテスト

#### ステップ3: 既存リファクタリング
- リバースエンジニアリング、デグレ防止、技術的負債解消

#### ステップ4: チーム開発
- 5-STEP運用、プロンプト共有、Living Documentation浸透

---

---

### 質疑応答
- 2日間の学びについての質問
- 実務での適用についての相談
- 今後の学習方針についてのアドバイス
- その他、AIを活用した開発全般について
