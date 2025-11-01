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

# Day 1-2: タスク分解 + 実装 + 品質担保 + リファクタリング (13:00-14:50)

---

<!-- _class: lead -->

## STEP3: タスク分解（35分）

---
<!-- _class: layout-diagram-only -->

# STEP3 タスク分解とは

![STEP3 タスク分解とは](../diagrams-web/slide_003_STEP3_タスク分解とは.svg)

---
<!-- _class: layout-diagram-only -->

# タスク分解 = AIの思考を言語化（重要）

![タスク分解 = AIの思考を言語化（重要）](../diagrams-web/slide_004_タスク分解_AIの思考を言語化重要.svg)

---

# 計画書作成による可視化（重要）
- **早い段階での軌道修正が可能**
  - 実装後に修正するより、計画段階で修正する方が効率的
  - コスト削減・時間短縮の効果
- **Guardrailsとしての計画書**
  - AIが道を外れたら、計画書で元に戻せる
  - 手戻りコストを大幅に削減

---

<!-- _class: layout-horizontal-left -->

# Phase分け戦略（Phase 1-4）

![Phase分け戦略](diagrams/diagram_10_phase_breakdown.svg)

- **なぜPhase分けが必要か**
  - 全部一度に作ると依存関係が複雑化→AIが混乱（忘れっぽい）
  - 段階的に作れば各Phaseで動作確認→早期問題発見
- **Phase 1（基盤）:** DB接続・認証基盤・基本CRUD
- **Phase 2（コア機能）:** ビジネスロジック・主要API
- **Phase 3（拡張機能）:** 検索・フィルタ・通知
- **Phase 4（仕上げ）:** パフォーマンス最適化・E2Eテスト
- **効果:** リスク最小化、確実な進捗

---
<!-- _class: layout-diagram-only -->

# タスク粒度（30分〜2時間）

![タスク粒度（30分〜2時間）](../diagrams-web/slide_007_タスク粒度30分2時間.svg)

---

<!-- _class: layout-horizontal-right -->

# 依存関係の可視化

![タスク依存関係グラフ](diagrams/diagram_35_dependency_graph.svg)

- **なぜ依存関係の可視化が必要か**
  - 順序を間違えると手戻りが発生（DB未作成でAPI実装できない）
  - AIは依存関係の判断が苦手（タスク実行は得意だが順序判断は苦手）
- **並行作業可能なタスク:** フロントとバックを同時進行
- **順序が必要なタスク:** DB設計→マイグレーション→API実装
- **AIへの指示:** 「依存関係を明示してタスク一覧を作成して」
- **効果:** 効率的なスケジューリング、手戻り防止

---

<!-- _class: layout-horizontal-left -->

# タスク一覧テンプレート

![タスク一覧テンプレート](diagrams/diagram_34_task_list_template.svg)

- **必須項目:** Phase・タスク名・所要時間・依存関係・完了条件
- **なぜテンプレート化が必要か**
  - 曖昧な計画→AIが勝手に解釈（構造化タスクは得意だが自由形式は苦手）
  - 明確なフォーマット→AIが一貫した出力
- **進捗管理:** 一覧表でステータス可視化（未着手・進行中・完了）
- **チーム共有:** Markdown形式でGit管理、誰でも参照可能
- **AIへの指示:** 「このテンプレートでタスク一覧を作成して」

---

# AI活用でタスク自動生成
- **プロンプト例:** 「この設計書に基づいて、タスク一覧を作成して。Phase分けして、各タスクは30分〜2時間で完了できるようにして」
- **AIが自動生成する項目:** Phase・タスク名・所要時間・依存関係・完了条件
- **人間の役割:** レビュー・調整・優先順位づけ
- **生産性向上:** 計画作成時間が数時間→数分に短縮
- **Trust but Verify:** AI生成後、必ず人間が確認・調整

---
<!-- _class: layout-diagram-only -->

# STEP3のまとめ

![STEP3のまとめ](../diagrams-web/slide_011_STEP3のまとめ.svg)

---

<!-- _class: layout-horizontal-left -->

# STEP3 チェックリスト

![STEP3チェックリスト](diagrams/diagram_37_step3_checklist.svg)

**必ず確認:**
- [ ] タスク一覧AI生成
- [ ] Phase分け
- [ ] タスク粒度30分〜2時間
- [ ] 依存関係明示
- [ ] 完了条件記載
- [ ] 並行作業特定
- [ ] docs/tasks.md文書化

---

---

<!-- _class: lead -->

## STEP4: 実装（40分）

---
<!-- _class: layout-diagram-only -->

# 実装の3原則（AIの制約に対応）

![実装の3原則（AIの制約に対応）](../diagrams-web/slide_015_実装の3原則AIの制約に対応.svg)

---
<!-- _class: layout-diagram-only -->

# 実装の標準ワークフロー

![実装の標準ワークフロー](../diagrams-web/slide_016_実装の標準ワークフロー.svg)

---

<!-- _class: layout-horizontal-right -->

# TDD/BDD統合ワークフロー

![TDD Red-Green-Refactorサイクル](diagrams/diagram_11_tdd_cycle.svg)

- **なぜTDD/BDDが必要か**
  - テストなし→AIが作る→人間が手動テスト→エラー→修正（無限ループ）
  - テストあり→AIが作る→自動テスト→エラー→AI自己修正（自己完結）
- **Red（失敗するテストを書く）:** テストが仕様を定義
- **Green（最小実装）:** テストを通す最小コード
- **Refactor（改善）:** テストが保証するから安心してリファクタリング
- **BDD形式（Given-When-Then）:** 人間が読める仕様書になる

---

<!-- _class: layout-horizontal-left -->

# AIにTDD/BDDで実装させる

![Given-When-Then構造](diagrams/diagram_33_given_when_then.svg)

- **プロンプト例:** 「POST /api/register を TDD で実装して。Given-When-Then形式のテストを書き、正常系・異常系をカバー」
- **AIが自動で行うこと:**
  1. Given-When-Thenテストを先に書く
  2. 実装コードを書く
  3. テストを実行→失敗→修正→成功を繰り返す
- **人間の役割:** プロンプトで方向性を指示、結果をレビュー
- **効果:** バグが少なく設計が良くなる、AIが自己完結

---

<!-- _class: layout-horizontal-right -->

# セキュリティベストプラクティス（重要）

![セキュリティベストプラクティス](diagrams/diagram_23_security_best_practices.svg)

- **なぜセキュリティが後回しになるか（Reward Hacking）**
  - AIは「タスク完了」を最優先→セキュリティは二の次
  - 平文保存、ハードコーディングで「とりあえず動く」を選ぶ
  - セキュリティ知識はあるが、明示しないと省略する
- **対策：明確な制約を設定（Guardrails）**
  - パスワード→BCrypt、APIキー→環境変数
  - JWT秘密鍵→環境変数、入力値→@Valid必須
  - .env作成、.gitignore追加、.env.example用意

---
<!-- _class: layout-diagram-only -->

# パスワード・JWT認証の実装

![パスワード・JWT認証の実装](../diagrams-web/slide_020_パスワードJWT認証の実装.svg)

---

# セキュアなコードの指示方法（重要）
- **なぜ明確な指示が必要か**
  - AIは暗黙の前提を理解できない（明示的な指示には従えるが推測は苦手）
  - セキュリティ要件は明示しないと実装されない
- **プロンプト例:** 「ユーザー登録APIを実装。BCrypt、環境変数、@Valid、レート制限、Spring Security、HTTPS、エラーメッセージ一般化」
- 明確な制約＝AIが安全な実装を行う

---

<!-- _class: layout-horizontal-left -->

# インクリメンタル開発とは

![インクリメンタル開発タイムライン](diagrams/diagram_24_incremental_timeline.svg)

- **なぜ小さく作るべきか（AIは忘れっぽい対策）**
  - 全部一度に作る→完成まで動かない→問題発見が遅れる
  - 小さく作る→動かす→確認→早期発見
- **効果:** 進捗が見える、モチベーション維持、リスク低減

---

# インクリメンタル実装の実例
- **Increment 1: 一覧表示**
  - タスク一覧取得API実装→テスト→動作確認→コミット
- **Increment 2: 新規作成**
  - タスク作成API実装→テスト→動作確認→コミット
- **Increment 3: 完了チェック**
  - タスク完了API実装→テスト→動作確認→コミット
- **各Incrementで:** 動作確認→テスト実行→AI自己レビュー→コミット
- **効果:** 常に動く状態を維持、問題を早期発見

---

<!-- _class: layout-horizontal-right -->

# AI自己レビュー必須化（重要）

![AI自己レビューフロー](diagrams/diagram_25_ai_self_review_flow.svg)

- **なぜAI自己レビューが重要か（Trust but Verify）**
  - AIにもエラーあり→自己レビューで多くを検出
  - Reward Hacking→実装後に手抜きチェック
  - Reward Hackingで省略されるため、セキュリティ観点での検証必須
- 実装後必ず：「このコードをレビューして。セキュリティ・エラー処理・エッジケース・ベストプラクティスをチェック」
- 追加コストほぼゼロで品質大幅向上

---
<!-- _class: layout-diagram-only -->

# STEP4のまとめ

![STEP4のまとめ](../diagrams-web/slide_025_STEP4のまとめ.svg)

---

<!-- _class: layout-horizontal-left -->

# STEP4 チェックリスト

![STEP4チェックリスト](diagrams/diagram_38_step4_checklist.svg)

**必ず確認:**
- [ ] タスク30分〜2時間
- [ ] Given-When-Thenテスト先行
- [ ] 最小実装でテスト通過
- [ ] AI自己レビュー
- [ ] セキュリティ要件満たす
- [ ] エラーハンドリング
- [ ] コミット実施

---

---

<!-- _class: lead -->

## STEP5: 品質担保＆ドキュメント反映（40分）

---

# STEP5 品質担保＆ドキュメント反映とは
- **なぜ品質担保とドキュメント反映が必要か**
  - **品質担保（Trust but Verify）:** AIにもエラーあり→検証なしでは本番投入不可
  - **ドキュメント反映（Living Documentation）:** AIは忘れっぽい→外部メモリ化が必須
- **TDDとAI活用の相乗効果**
  - テストがあれば→AIが自分でバグに気づき→自分で修正→自己完結
  - テストなし→人間が手動確認→エラー報告→修正依頼（非効率）
- **Living Documentationの価値**
  - 実装と同期したドキュメント、AIが過去の知見を参照できる
- **効果:** 品質保証の自動化、知見の蓄積、次セッションでの再利用

---

# テスト駆動開発とAI活用の相乗効果（重要）
- **なぜTDDとAIが相性抜群か**
  - テストがあれば、AIが自分でバグに気づき自分で修正
  - Trust（AI実装）→ Verify（テスト実行）→ 修正を自動化
- **TDDなし:** 人間が実行→エラー確認→コピペ→AI伝達の無限ループ
- **TDDあり:** AIが自動でテスト実行→エラー検知→修正
- 生産性が飛躍的に向上

---

# E2Eテスト重視の戦略
- **なぜE2Eテストを重視すべきか**
  - 実装詳細のテスト→リファクタリングで壊れる
  - E2Eテスト→ユーザー体験を検証、リファクタリングに強い
- 本当の価値（ユーザー体験）を保証

---

# Playwright によるE2Eテスト
- **なぜPlaywrightか**
  - ユーザー視点のテスト自動化、実ブラウザで動作確認
  - AIが自動でテストコード生成可能
- **プロンプト例:** 「ログイン→ダッシュボード表示のPlaywrightテストを作成して」
- **AIが生成:** ブラウザ起動→ログインフォーム入力→送信→画面遷移確認
- **本番環境と同じ条件:** 実際のユーザー体験を検証
- **効果:** UIバグ・統合問題を自動検出

---

# ビジュアルリグレッションテスト
- **なぜビジュアルテストが必要か**
  - コードは正しくても見た目が崩れる場合がある
  - 人間の目視確認は漏れが発生しやすい
- スクリーンショット比較で自動検出、差分があれば警告

---

# MCP関連ツール
- **なぜMCPが必要か**
  - AIのカットオフ問題→古いライブラリ情報で実装してしまう
  - Context 7：2万以上の最新公式ドキュメントを参照
- Serena：大規模プロジェクト高速検索、Browser DevTools：コンソールエラー自動キャプチャ

---
<!-- _class: layout-diagram-only -->

# AI自己レビュー4種類の使い分け

![AI自己レビュー4種類の使い分け](../diagrams-web/slide_035_AI自己レビュー4種類の使い分け.svg)

---

# AI自己レビュー①一般レビュー
- **プロンプト:** 「このコードをレビューして。セキュリティ・エラー処理・エッジケース・ベストプラクティスをチェック」
- **検出:** ロジックエラー、エッジケース見落とし（null、空配列）、命名規則違反
- **効果:** バグ検出率向上

---

# AI自己レビュー②セキュリティ特化
- **プロンプト:** 「OWASP Top 10でセキュリティレビュー。SQL injection・XSS・CSRF・機密情報・認証認可・バリデーションをチェック」
- **検出:** SQL injection、XSS、CSRF、平文パスワード、ハードコーディングされたAPIキー
- **効果:** 脆弱性を大幅削減

---

# AI自己レビュー③パフォーマンス特化
- **プロンプト:** 「パフォーマンスレビュー。N+1クエリ・メモリリーク・キャッシュ・インデックス・非同期処理をチェック」
- **検出:** N+1クエリ、無駄な全件取得、キャッシュ未活用
- **効果:** N+1問題などを解消してレスポンス時間を大幅改善

---

<!-- _class: layout-horizontal-left -->

# AI自己レビュー④テストカバレッジ

![テストカバレッジ80%ルール](diagrams/diagram_26_test_coverage_80_rule.svg)

- **プロンプト:** 「テストレビュー。エッジケース・異常系・境界値・独立性・Given-When-Thenをチェック」
- **検出:** テストケース漏れ（null、空文字、MAX値）、異常系不足
- **効果:** テストカバレッジ向上

---

# 自己レビューの実例
- **Before（AIの初回実装）:**
  - 平文パスワード比較（セキュリティ脆弱）
  - APIキーハードコーディング（Git漏洩リスク）
  - バリデーションなし（不正入力で例外）
- **After（AI自己レビュー後）:**
  - BCrypt比較、環境変数管理、@Valid入力値検証
  - レート制限、@ControllerAdviceエラーハンドリング
- **改善率:** 多くのバグ検出、追加コストほぼゼロ

---
<!-- _class: layout-diagram-only -->

# STEP5のまとめ

![STEP5のまとめ](../diagrams-web/slide_041_STEP5のまとめ.svg)

---

<!-- _class: layout-horizontal-left compact -->

# STEP5 チェックリスト

![STEP5チェックリスト](diagrams/diagram_39_step5_checklist.svg)

**品質担保:**
- [ ] カバレッジ80%+
- [ ] E2Eテスト
- [ ] AI一般レビュー
- [ ] AIセキュリティレビュー

**リファクタリング:**
- [ ] 重複コード削除
- [ ] パターン適用

**ドキュメント:**
- [ ] architecture.md
- [ ] README.md
- [ ] CLAUDE.md

---

### リファクタリング（内部品質向上）

- **なぜリファクタリングが必要か（Reward Hacking対策）**
  - AIは「とりあえず動く」を優先→コピペで重複コード生成
  - 最適化提案は得意だが、トレードオフ判断（可読性 vs 性能）は苦手
- **リファクタリングの3観点:**
  1. **重複コード削除:** コピペで生成された重複を削減
  2. **デザインパターン適用:** if-else→Strategy、オブジェクト生成→Factory
  3. **ライブラリ活用:** 車輪の再発明を避ける
- **AIへの指示:** 「不要・冗長・重複コードを指摘して」
- **効果:** 保守コスト削減、バグリスク低減

---


### Living Documentation（AIの外部メモリ）

- **なぜLiving Documentationが必要か（AIは忘れっぽい）**
  - AIはセッション超えると全て忘れる→ドキュメント＝AIの外部メモリ
  - 従来：実装と乖離→誰も信用しない
  - Living：実装と同期→常に信頼できる
- **3種類のドキュメント:**
  - **①architecture.md:** システム全体像（構成・ディレクトリ・設計判断）
  - **②README.md:** セットアップ手順・使い方
  - **③CLAUDE.md:** 成功したプロンプトパターン蓄積
- **計画図面 vs 完成図面（重要）**
  - 計画図面（設計書）：作る前の理想
  - 完成図面（as-built）：実際に作った結果
  - 必ず差分が生まれる→実装で得られた知見を記録
- **効果:** 次のセッションのAIが過去の知見を参照、同じ失敗を繰り返さない

---

### 頻繁なコミット（重要）
- **なぜ頻繁なコミットが必要か**
  - AIの暴走対策：間違った方向に進んだらすぐに戻れる
  - 実験の安全性：失敗してもリスクゼロ
  - 引き継ぎ可能性：履歴があれば誰でも状況を把握できる
- **コミット頻度:** 1機能完了→コミット、テスト通過→コミット

---


---

<!-- _class: lead -->

## Part 2 全体のまとめ

---

<!-- _class: card-grid -->

# Part 2のキーポイント

### ①計画の可視化（STEP3）
タスク分解でAIの思考を言語化、早期軌道修正

### ②セキュリティファースト（STEP4）
BCrypt・環境変数・@Valid、明示しないとAIは手抜き

### ③TDDでAI自己完結（STEP4-5）
テストがあれば、AIが自分でデバッグ・修正

### ④AI自己レビュー必須（STEP5）
観点別レビューで検出率大幅向上

### ⑤リファクタリング＆ドキュメント（STEP6）
技術的負債の早期解消、Living Documentationで知見蓄積
