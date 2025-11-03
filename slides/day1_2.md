---
marp: true
theme: ai-seminar
paginate: true
---

# Day 1-2: タスク分解 + 実装 + 品質担保 + リファクタリング (13:00-14:50)

---

<!-- _class: lead -->

## STEP3: タスク分解（35分）

---

<!-- _class: layout-callout -->

<div class="icon">📋</div>

# STEP3 タスク分解とは

<div class="message">
大きな機能を実装可能な小さなタスクに分解 = AIの思考を言語化
</div>

- AIは忘れっぽい→全体像を把握しづらい
- Reward Hacking→いきなり実装すると手抜きしがち
- **計画書＝AIの思考を可視化**して、人間が軌道修正できる
- **効果**: 実装前に方向性確認、手戻り防止、開発リスク最小化

---

<!-- _class: layout-diagram-only -->

# タスク分解 = AIの思考を言語化（重要）

![タスク分解_AIの思考を言語化重要](./assets/diagrams-web/slide_004_タスク分解_AIの思考を言語化重要.svg)

---

<!-- _class: two-column -->

# 計画書作成による可視化

## 早期の軌道修正

- 計画段階で修正する方が効率的
- コスト削減・時間短縮

## Guardrails

- AIが道を外れたら計画書で元に戻す
- 手戻りコスト削減

## プロンプト例

```
「設計書に基づいて
実装タスク一覧を作成。

- Phase分けして
- 各30分〜2時間で完了
- 依存関係を明示
- 完了条件を具体的に」
```

---

<!-- _class: layout-horizontal-left -->

# Phase分け戦略

![Phase分け戦略](./assets/diagrams/diagram_10_phase_breakdown.svg)

**なぜ:** 依存関係複雑化防止、早期問題発見
**Phase 1:** DB接続・認証・基本CRUD | **Phase 2:** ビジネスロジック・主要API | **Phase 3:** 検索・フィルタ・通知 | **Phase 4:** 最適化・E2Eテスト
**効果:** リスク最小化、確実な進捗

---

<!-- _class: layout-diagram-only -->

# タスク粒度（30分〜2時間）

![タスク粒度30分2時間](./assets/diagrams-web/slide_007_タスク粒度30分2時間.svg)

---

<!-- _class: layout-horizontal-right -->

# 依存関係の可視化

![タスク依存関係グラフ](./assets/diagrams/diagram_35_dependency_graph.svg)

- **なぜ必要:** 順序間違い→手戻り、AIは順序判断苦手
- **並行可能:** フロント・バック同時
- **順序必須:** DB設計→マイグレ→API
- **AI指示:** 「依存関係明示してタスク一覧作成」
- **効果:** 効率化、手戻り防止

---

<!-- _class: layout-horizontal-left ultracompact -->

# タスク一覧テンプレート

![タスク一覧テンプレート](./assets/diagrams/diagram_34_task_list_template.svg)

**必須項目:** Phase・タスク名・所要時間・依存・完了条件

**なぜ必要:**
曖昧な計画→AI勝手解釈、明確なフォーマット→一貫出力

**進捗管理:** ステータス可視化（未着手・進行中・完了）

**チーム共有:** Markdown形式でGit管理

**AI指示:** 「このテンプレートでタスク一覧作成」

---

<!-- _class: two-column compact -->

# AI活用でタスク自動生成

## プロンプト例

```
「この設計書に基づいて、
タスク一覧を作成して。
Phase分けして、
各タスクは30分〜2時間で
完了できるようにして」
```

## AIが自動生成する項目

- Phase
- タスク名
- 所要時間
- 依存関係
- 完了条件

## 人間の役割

- レビュー
- 調整
- 優先順位づけ

## 生産性向上

計画作成時間が
**数時間 → 数分**に短縮

**Trust but Verify:**
AI生成後、必ず人間が確認・調整

---

<!-- _class: layout-diagram-only -->

# STEP3のまとめ

![STEP3のまとめ](./assets/diagrams-web/slide_011_STEP3のまとめ.svg)

---

---

<!-- _class: lead ultracompact -->

## STEP4: 実装（40分）

---

<!-- _class: layout-callout supercompact -->

<div class="icon">⚡</div>

# 実装の3原則

<div class="message">
小さく作る・TDD・AI自己レビュー
</div>

**①小さく作る** - AIは忘れっぽい、常に動く状態維持

**②テスト駆動** - Trust but Verify、AI自己完結

**③AI自己レビュー** - 手抜き検出、40-60%バグ自動検出

---

<!-- _class: layout-timeline -->

# 実装の標準ワークフロー

<div class="timeline">
  <div class="step">
    <div class="step-number">1</div>
    <h3>タスク選択</h3>
  </div>
  <div class="step">
    <div class="step-number">2</div>
    <h3>テスト作成</h3>
    <p>Red</p>
  </div>
  <div class="step">
    <div class="step-number">3</div>
    <h3>実装</h3>
    <p>Green</p>
  </div>
  <div class="step">
    <div class="step-number">4</div>
    <h3>レビュー</h3>
    <p>Refactor</p>
  </div>
  <div class="step">
    <div class="step-number">5</div>
    <h3>修正</h3>
  </div>
  <div class="step">
    <div class="step-number">6</div>
    <h3>確認</h3>
    <p>E2E</p>
  </div>
  <div class="step">
    <div class="step-number">7</div>
    <h3>コミット</h3>
  </div>
</div>

---

<!-- _class: layout-horizontal-right -->

# TDD/BDD統合ワークフロー

![TDD Red-Green-Refactorサイクル](./assets/diagrams/diagram_11_tdd_cycle.svg)

**なぜTDD/BDD:**
- テストなし→無限ループ | テストあり→AI自己完結
**Red:** 失敗するテスト先書き（仕様定義）
**Green:** 最小実装でテスト通過
**Refactor:** 安心してリファクタリング
**BDD (Given-When-Then):** 人間が読める仕様書

---

<!-- _class: layout-horizontal-left -->

# AIにTDD/BDDで実装させる

![Given-When-Then構造](./assets/diagrams/diagram_33_given_when_then.svg)

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

![セキュリティベストプラクティス](./assets/diagrams/diagram_23_security_best_practices.svg)

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

![パスワードJWT認証の実装](./assets/diagrams-web/slide_020_パスワードJWT認証の実装.svg)

---

<!-- _class: layout-code-focus -->

# セキュアなコードの指示方法

```
「ユーザー登録API実装。必須:
BCrypt、JWT秘密鍵環境変数、.env使用、
.gitignore追加、@Validバリデ、
レート制限、エラー一般化」
```

**なぜ:** AI暗黙前提理解不可
**効果:** 明確な制約＝安全実装

---

<!-- _class: layout-horizontal-left -->

# インクリメンタル開発とは

![インクリメンタル開発タイムライン](./assets/diagrams/diagram_24_incremental_timeline.svg)

- **なぜ小さく作るべきか（AIは忘れっぽい対策）**
  - 全部一度に作る→完成まで動かない→問題発見が遅れる
  - 小さく作る→動かす→確認→早期発見
- **効果:** 進捗が見える、モチベーション維持、リスク低減

---

<!-- _class: layout-timeline -->

# インクリメンタル実装の実例

<div class="timeline">
  <div class="step">
    <div class="step-number">1</div>
    <h3>一覧表示</h3>
    <p>API実装→テスト→動作確認→コミット</p>
  </div>
  <div class="step">
    <div class="step-number">2</div>
    <h3>新規作成</h3>
    <p>API実装→テスト→動作確認→コミット</p>
  </div>
  <div class="step">
    <div class="step-number">3</div>
    <h3>完了チェック</h3>
    <p>API実装→テスト→動作確認→コミット</p>
  </div>
</div>

**各Incrementで:** 動作確認→テスト実行→AI自己レビュー→コミット

**効果:** 常に動く状態を維持、問題を早期発見

---

<!-- _class: layout-horizontal-right -->

# AI自己レビュー必須化（重要）

![AI自己レビューフロー](./assets/diagrams/diagram_25_ai_self_review_flow.svg)

- **なぜAI自己レビューが重要か（Trust but Verify）**
  - AIにもエラーあり→自己レビューで多くを検出
  - Reward Hacking→実装後に手抜きチェック
  - Reward Hackingで省略されるため、セキュリティ観点での検証必須
- 実装後必ず：「このコードをレビューして。セキュリティ・エラー処理・エッジケース・ベストプラクティスをチェック」
- 追加コストほぼゼロで品質大幅向上

---

<!-- _class: layout-diagram-only -->

# STEP4のまとめ

![STEP4のまとめ](./assets/diagrams-web/slide_025_STEP4のまとめ.svg)

---

---

<!-- _class: lead -->

## STEP5: 品質担保＆ドキュメント反映（40分）

---

<!-- _class: layout-callout supercompact -->

<div class="icon">✅</div>

# STEP5 品質担保＆ドキュメント反映とは

<div class="message">
Trust but Verify自動化 + Living Documentation
</div>

- **品質担保（Trust but Verify）:** AIにもエラーあり→検証なしでは本番投入不可
- **ドキュメント反映（Living Documentation）:** AIは忘れっぽい→外部メモリ化が必須
- **TDDとAI活用の相乗効果:** テストがあれば→AIが自分でバグに気づき→自分で修正→自己完結
- **効果:** 品質保証の自動化、知見の蓄積、次セッションでの再利用

---

<!-- _class: layout-comparison supercompact -->

# テスト駆動開発とAI活用の相乗効果

<div>

### TDDなし

人間が実行 → エラー確認 → コピペ → AI伝達

**無限ループ**

</div>

<div>VS</div>

<div>

### TDDあり

AIが自動テスト実行 → エラー検知 → 修正

**自己完結**

</div>

**結論:** テストがあれば、AIが自分でバグに気づき自分で修正、生産性が飛躍的に向上

---

<!-- _class: lead supercompact -->

# E2Eテスト重視の戦略

## なぜE2Eか

- **実装詳細テスト**→リファクタリングで壊れる
- **E2Eテスト**→ユーザー体験を保証

---

<!-- _class: card-grid supercompact -->

# Playwright活用

### なぜPlaywrightか
- ユーザー視点の自動化
- 実ブラウザで動作確認
- AIが自動生成可能

### プロンプト例
「ログイン→ダッシュボードの
Playwrightテストを作成」

### 効果
UIバグ・統合問題を自動検出

---

<!-- _class: two-column -->

# ビジュアルリグレッションテスト

## なぜビジュアルテストが必要か

- コードは正しくても見た目が崩れる場合がある
- 人間の目視確認は漏れが発生しやすい
- スクリーンショット比較で自動検出、差分があれば警告

## MCP関連ツール

**なぜMCPが必要か:**
- AIのカットオフ問題→古いライブラリ情報で実装してしまう
- **Context 7**: 2万以上の最新公式ドキュメントを参照
- **Serena**: 大規模プロジェクト高速検索
- **Browser DevTools**: コンソールエラー自動キャプチャ

---

<!-- _class: layout-diagram-only -->

# AI自己レビュー4種類の使い分け

![AI自己レビュー4種類の使い分け](./assets/diagrams-web/slide_035_AI自己レビュー4種類の使い分け.svg)

---

<!-- _class: card-grid -->

# AI自己レビューの4つの観点

### ①一般レビュー（毎回必須）
**検出:** ロジックエラー、エッジケース見落とし、命名規則違反

### ②セキュリティ特化
**検出:** SQLi・XSS・CSRF・平文PW・ハードコーディング

### ③パフォーマンス特化
**検出:** N+1クエリ、無駄な全件取得、キャッシュ未活用

### ④テストカバレッジ
**検出:** テストケース漏れ、異常系不足、境界値未検証

---
<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->


<!-- _class: layout-horizontal-left -->

# テストカバレッジ80%ルール

![テストカバレッジ80%ルール](./assets/diagrams/diagram_26_test_coverage_80_rule.svg)

**なぜ80%:** 100%非現実的（Getter/Setter不要）、80%で主要機能とエッジケースをカバー
**残り20%:** リスク低い箇所
**効果:** カバレッジ向上、リファクタリング安全性確保

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: layout-comparison -->

# 自己レビューの実例

<div>

### Before（初回実装）

- 平文パスワード比較（セキュリティ脆弱）
- APIキーハードコーディング（Git漏洩リスク）
- バリデーションなし（不正入力で例外）

</div>

<div>→</div>

<div>

### After（自己レビュー後）

- BCrypt比較
- 環境変数管理
- @Valid入力値検証
- レート制限
- @ControllerAdviceエラーハンドリング

</div>

**改善率:** 多くのバグ検出、追加コストほぼゼロ

---

<!-- _class: two-column supercompact -->

# リファクタリング（内部品質向上）

## なぜ必要か

**Reward Hacking対策:**
- AIは「動く」を優先
- コピペで重複生成

## 3つの観点

**①重複削除** - 保守コスト削減

**②パターン適用**
- if-else→Strategy
- 生成→Factory

**③ライブラリ活用** - 再発明回避

**AI指示:** 「不要・冗長・重複コード指摘」

---

<!-- _class: layout-horizontal-left supercompact -->

# Living Documentation
## AIの外部メモリ

![Living Documentation](./assets/diagrams/diagram_36_living_documentation.svg)

## なぜ必要か

- **AIは忘れっぽい** → セッション超えると全て忘れる
- **Living** → 実装と同期、常に信頼できる
- **ドキュメント＝AIの外部メモリ**

---

<!-- _class: layout-diagram-only ultracompact -->

# ドキュメント自動生成Before/After

![ドキュメント自動生成Before/After](./assets/diagrams/diagram_43_doc_automation_before_after.svg)

---

<!-- _class: card-grid supercompact -->

# Living Documentation 3種類

### architecture.md
システム全体像、構成・ディレクトリ、設計判断理由

**効果:** AIが全体像把握

### README.md
セットアップ手順、使い方、トラブルシューティング

**効果:** 誰でもすぐ開発開始

### CLAUDE.md
成功プロンプトパターン、ハマった点と回避策

**効果:** 再現性確保、失敗繰り返さない

---

<!-- _class: two-column supercompact -->

# 計画図面 vs 完成図面

## 計画図面（設計書）
作る前、理想設計、AIへのGuardrails

## 完成図面（as-built）
作った後、実際の結果、次セッション参照

## 必ず差分が生まれる
実装知見を記録

**例:** 変更理由、ハマった点と回避策

## Living Documentation
実装と同期

---

<!-- _class: two-column -->

# 頻繁なコミット（重要）

## なぜ頻繁なコミットが必要か

**AIの暴走対策:**
- 間違った方向に進んだらすぐに戻れる

**実験の安全性:**
- 失敗してもリスクゼロ

**引き継ぎ可能性:**
- 履歴があれば誰でも状況を把握できる

## コミット頻度

- 1機能完了→コミット
- テスト通過→コミット

## コミットメッセージ

明確な変更内容を記録

---

<!-- _class: layout-diagram-only supercompact -->

# STEP5のまとめ

![STEP5のまとめ](./assets/diagrams-web/slide_041_STEP5のまとめ.svg)

---

<!-- _class: card-grid -->

# Part 2 全体のまとめ：キーポイント

### ①計画可視化
タスク分解で思考言語化

### ②セキュリティ
BCrypt・環境変数・@Valid明示

### ③TDD自己完結
テストでAI自動デバッグ

### ④自己レビュー
観点別で検出率向上

### ⑤リファクタ&Doc
負債解消、知見蓄積
