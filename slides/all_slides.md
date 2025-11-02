---
marp: true
theme: ai-seminar
paginate: true
---

<!-- _class: lead compact -->

# AI活用研修：新規開発編

## 2日間で学ぶ、生産性を劇的に向上させる体系的アプローチ

AI駆動開発で開発期間を大幅短縮

---

<!-- _class: layout-diagram-only -->

# 本日の目標

![本日の目標](./assets/diagrams-web/slide_002_本日の目標.svg)

---

<!-- _class: layout-horizontal-left -->

# AI活用の3原則

![AI活用の3原則](./assets/diagrams/diagram_01_ai_principles.svg)

**Jagged Intelligence:** 得意（コード生成・テスト・設計）、苦手（ビジネス要件・判断）
**Trust but Verify:** AIにもエラーあり、AI自己レビューで品質向上
**Guardrails:** ドキュメント駆動、受入条件で手戻り防止

---

<!-- _class: layout-comparison -->

# Vibe Coding vs Production Engineering

<div>

### Vibe Coding
速い（30分〜1時間）、品質バラバラ、プロトタイプ向き

</div>

<div>VS</div>

<div>

### Production Engineering
構造化、品質保証、本番向き

</div>

**結論**: Vibe Coding with Guardrails で速さと品質を両立

---

<!-- _class: layout-horizontal-left -->

# 開発者の役割変化

![開発者の役割変化](./assets/diagrams/diagram_02_role_change.svg)

- **従来：運転手** - コード1行ずつ、全実装詳細把握
- **AI時代：ナビゲーター** - 方向指示、AIが実装
- **人間の役割**: ビジネス要件、設計判断、品質・セキュリティ
- **AIの役割**: コード生成、テスト、リファクタリング、ドキュメント
- **効果**: 本質的価値創造に集中

---

<!-- _class: layout-horizontal-left -->

# 5-STEPフロー全体像

![5-STEPフロー](./assets/diagrams/diagram_03_5step_flow.svg)

- **STEP1: 要件定義** - 何を作るか明確化（Guardrails構築）
- **STEP2: 設計** - どう作るか定義（AI外部メモリ）
- **STEP3: タスク分解** - 全体像を小さく分割（忘れっぽさ対策）
- **STEP4: 実装** - 小さく作る・TDD・AI自己レビュー
- **STEP5: 品質担保＆ドキュメント反映** - Trust but Verify自動化、Living Documentation
- **効果:** 手戻り防止、品質保証、開発期間短縮

---

<!-- _class: layout-horizontal-right -->

# AIの制約①忘れっぽい（セッション制約）

![AIの外部メモリ](./assets/diagrams/diagram_04_ai_memory.svg)

- **セッション内のみ記憶**: ブラウザ閉じる→全忘却、20万トークン超過→古い情報忘却
- **問題**: 同じバグ繰り返し、成功方法忘却
- **対策**: ドキュメント化＝外部メモリ、architecture.md/README.mdに知見蓄積

---

<!-- _class: layout-diagram-only -->

# AIの制約②Reward Hacking（手抜き問題）

![Reward Hacking問題と対策](./assets/diagrams/diagram_39_reward_hacking_examples.svg)

---

<!-- _class: two-column supercompact -->

# 環境準備

## 必須ツール

**Claude Code**
AI開発環境、プロジェクト全体文脈理解

**GitHub**
バージョン管理、頻繁commit、AI暴走から回復

**VS Code**
エディタ、Mermaid Preview、図の即座確認

## 推奨

**Dev Container**
環境統一化、再現性、安全性

## セットアップ
Claude Code、GitHub、VS Code + Mermaid、Dev Container推奨

---

<!-- _class: layout-diagram-only -->

# セキュリティベストプラクティス（補足）

![セキュリティベストプラクティス](./assets/diagrams/diagram_23_security_best_practices.svg)

---

<!-- _class: lead -->

## Claude Code の使い方（10:30-10:50, 20分）

---

<!-- _class: layout-callout -->

<div class="icon">💡</div>

# Claude Code とは

<div class="message">
プロジェクト全体を扱うAI開発アシスタント
</div>

- プロジェクト全体の文脈を理解（複数ファイルの関係性を把握）
- 単一ファイル編集ではなく、関連ファイルを一括操作
- Git統合で安全性を確保（コミット履歴、ロールバック可能）
- **効果**: プロジェクト全体の一貫性を保ちながら開発

---

<!-- _class: layout-horizontal-right -->

# セットアップ

![.claudeignoreの重要性](./assets/diagrams/diagram_29_claudeignore_importance.svg)

- **インストール:** `npm install -g @anthropic-ai/claude-code`
- **APIキー取得:** https://console.anthropic.com
- **初回起動:** `claude`（APIキー入力、.claudeignore設定）
- **.claudeignore必須:**
  - node_modules/, dist/, .git/, *.log を除外
  - トークン節約、コスト削減

---

<!-- _class: layout-horizontal-left -->

# 4つのモード比較

![Claude Codeモード比較](./assets/diagrams/diagram_28_claude_code_modes.svg)

- **通常:** 毎回確認、最も安全
- **YOLO（Shift+Tab）:** 自動実行、Git管理済み推奨
- **プラン（Shift+Tab×2）:** 計画→確認→実行
- **dangerously-skip:** 全スキップ（超危険）

---

<!-- _class: layout-diagram-only -->

# よくある問題と対処法

![よくある問題と対処法](./assets/diagrams-web/slide_017_よくある問題と対処法.svg)

---

<!-- _class: layout-horizontal-right -->

# 効率的な指示の出し方

![プロンプトパターン（良い例vs悪い例）](./assets/diagrams/diagram_30_prompt_patterns.svg)

- **❌ 悪い:** 「ログイン機能作って」
- **✅ 良い:**
  - 制約明示（bcrypt、環境変数）
  - 段階的（1機能ずつ）
  - 質問促す/AI自己レビュー
- **サイクル:** 指示→実装→レビュー→修正

---

---

<!-- _class: lead -->

## STEP1: 要件定義（10:50-11:30, 40分）

---

<!-- _class: layout-callout -->

<div class="icon">📋</div>

# STEP1 要件定義とは

<div class="message">
「何を作るか」を明確化し、AIへのGuardrailsを構築
</div>

- AIはJagged Intelligence（技術実装は得意だがビジネス要件の解釈は苦手）
- Reward Hacking→曖昧な仕様だと手抜き実装
- 明確な要件＝AIが道を外れない境界線
- **成果物**: docs/requirements.md（ユーザーストーリー、機能一覧、受け入れ基準）

---

<!-- _class: layout-diagram-only -->

# AIに質問させる手法

![AIに質問させる手法](./assets/diagrams-web/slide_022_AIに質問させる手法.svg)

---

<!-- _class: layout-horizontal-left -->

# 要件の引き出し方（文字起こしアプローチ）

![文字起こし→AI抽出フロー](./assets/diagrams/diagram_40_transcript_approach.svg)

## 🎯 なぜこの手法が強力か

**顧客の言葉をそのまま記録:**
- 解釈のズレゼロ
- 「言った/言わない」問題の解消
- 顧客の本当のニーズを捉える

**AIが要件構造化:**
- 漏れ・ヌケ防止
- 自動で優先順位付け
- **不明点リスト**も自動生成

---

<!-- _class: layout-horizontal-left -->

# MoSCoW 優先順位付け

![MoSCoW優先順位](./assets/diagrams/diagram_05_moscow.svg)

- **Must（必須）:** プロダクト成立に不可欠な機能 → Phase 1 (MVP)
- **Should（重要）:** あるべきだが、なくても動く → Phase 2
- **Could（あれば良い）:** あると嬉しい → Phase 3
- **Won't（今回はやらない）:** 将来的には考える、スコープ外
- **原則:** Mustは全体の20〜30%に絞る（欲張らない）
- **効果:** Phase分けで段階的リリース、開発期間短縮

---

<!-- _class: layout-diagram-only -->

# MoSCoW実践例（ToDoアプリ）

![MoSCoW実践例（ToDoアプリ）](./assets/diagrams/diagram_47_moscow_example.svg)

---

<!-- _class: layout-horizontal-right -->

# ユーザーストーリーマッピング

![ユーザーストーリーマッピング](./assets/diagrams/diagram_31_user_story_mapping.svg)

- **フォーマット:** `<誰が> <何をしたい> <なぜ>`
- **例:** タスク追加（忘れないため）
- **旅:** 1.管理 2.整理 3.進捗確認
- **効果:** AIが本質的価値を実装

---

<!-- _class: layout-horizontal-left -->

# 非機能要件

![非機能要件チェックリスト](./assets/diagrams/diagram_32_nonfunctional_requirements.svg)

## 🎯 重要性

**本番では不可欠:**
- 性能/セキュリティ/拡張性

**AIは明示必須:**
- 非機能要件 = Guardrails

---

<!-- _class: layout-diagram-only -->

# エラー・エッジケース・制約の洗い出し

![エラー・エッジケース・制約の洗い出し](./assets/diagrams/diagram_45_error_edge_constraint.svg)

---
<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->


<!-- _class: layout-horizontal-left -->

# 受け入れ基準（Given-When-Then）

![Given-When-Then形式](./assets/diagrams/diagram_33_given_when_then.svg)

**正常系:**
- Given: 登録済みユーザー | When: 正しいメール・パスワードでログイン | Then: トークン発行、ダッシュボードへリダイレクト

**異常系:**
- Given: 登録済みユーザー | When: 間違ったパスワードでログイン | Then: エラーメッセージ、5回失敗でロック

**効果:** 「完成の定義」を明確化

---

<!-- _class: two-column -->

# プロトタイプ駆動開発（Vibe Coding）

## 従来のアプローチ

文章 → 実装 → 「イメージと違う」

## Vibe Coding

ビジュアルで確認しながら調整

**ツール:** Claude Code（Thymeleaf/HTML/Bootstrap）

**指示例:**
```
「ToDoアプリのプロトタイプをThymeleafで作って。
タスク追加フォーム、一覧表示、削除ボタン。Bootstrap使用」
```

**ステップ:** 確認 → 修正指示 → 即座に反映 → OK!

**メリット:** クライアントとの認識合わせが簡単

---

<!-- _class: layout-diagram-only -->

# STEP1のまとめ

![STEP1のまとめ](./assets/diagrams-web/slide_031_STEP1のまとめ.svg)

---

---

<!-- _class: lead -->

## STEP2: 設計ドキュメント作成（11:30-12:00, 30分）

---

<!-- _class: layout-callout -->

<div class="icon">📐</div>

# STEP2 設計ドキュメントとは

<div class="message">
「どのように作るか」を明確にする設計図＝AIの外部メモリ
</div>

- AIは忘れっぽい→設計意図忘却
- Reward Hacking→手抜き実装
- **Spec-Driven Development**: Spec-First へ

---
<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->


<!-- _class: layout-horizontal-right -->

# 設計ドキュメントの構造

![設計ドキュメントの7要素](./assets/diagrams/diagram_06_spec_structure.svg)

- **1. 技術スタック:** フロント・バック・DB・ライブラリ（選定理由含む）
- **2. システムアーキテクチャ:** 3層構造、Mermaid図で可視化
- **3. データベーススキーマ:** テーブル定義・カラム・制約・インデックス
- **4. API仕様:** エンドポイント・メソッド・パラメータ・レスポンス
- **5. 受入条件（BDD形式）:** Given-When-Then
- **6. セキュリティ設計:** 認証・認可・入力検証・環境変数管理
- **7. 技術的決定事項:** ライブラリ選定理由・アーキテクチャ判断

---

<!-- _class: two-column -->

# Tech Stack Setup

## なぜ最初に固めるか

後から変更すると大幅な手戻り

## 例

**フロント:** Thymeleaf/JSP
**バック:** Spring Boot
**DB:** PostgreSQL/MySQL
**認証:** Spring Security+JWT
**日付:** Java 8 Date/Time API (標準ライブラリ)
**テスト:** JUnit 5+Mockito

## 重要

選定理由も明記→技術的判断の根拠を残す

---
<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->


<!-- _class: layout-horizontal-left -->

# データベーススキーマ設計

![ER図の例](./assets/diagrams/diagram_07_er_diagram.svg)

- **なぜスキーマ定義が必要か**
  - 後から変更すると影響範囲が非常に大きい
  - AIは明示的な指示がないと不適切な設計をする
- **スキーマ定義で得られる効果**
  - AIが正確なSQL・ORM実装ができる
  - カラム名・型・制約の一貫性が保たれる
  - マイグレーションの自動生成が可能

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: two-column -->

# API仕様の明確化

## なぜAPI仕様が必要か

- 仕様がないとAIがエンドポイントを勝手に決める
- フロントとバックで認識齟齬が発生

## API仕様で得られる効果

- フロントエンドとバックエンドの並行開発が可能
- AIが仕様通りのエンドポイントを実装
- バリデーション・エラーハンドリングの一貫性
- 後からのAPI変更時に影響範囲が明確

---

<!-- _class: layout-horizontal-right -->

# Mermaid記法とSVG生成でビジュアル化

![Mermaid vs SVG使い分け](./assets/diagrams/diagram_41_mermaid_vs_svg.svg)

- **Mermaid**: テキストで図描画、Git管理可、AI自動生成、GitHub/VS Code表示
- **SVG生成magic word**: 「SVGで書いて」→AI生成→即可視化、記法不要
- **使い分け**: Mermaid=GitHub用、SVG=即可視化・プレゼン用

---

<!-- _class: layout-horizontal-left -->

# ER図が開発をスムーズにする理由

![ER図からコード生成](./assets/diagrams/diagram_08_er_to_code.svg)

- **AIの実装**: CREATE TABLE自動生成、JOIN処理、外部キー、ORMモデル
- **人間の恩恵**: 全体像一目把握、リレーション検証、正規化問題発見

---
<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->


<!-- _class: layout-horizontal-right -->

# シーケンス図がAI実装を助ける理由

![シーケンス図の例（ログインフロー）](./assets/diagrams/diagram_09_sequence_login.svg)

- **AIの実装**: 処理順序理解→正確コードフロー、エラー処理タイミング、依存関係、トランザクション境界
- **図なしの問題**: 処理順序推測ミス、ロールバック漏れ
- **効果**: 複雑処理も正確実装

---

<!-- _class: two-column compact -->

# 受け入れ条件の詳細化

## なぜ受け入れ条件が必要か

- AIは「タスク完了」を優先し、品質は二の次
- 明確な合格基準がないと手抜き実装になる
- 受け入れ条件 = AIの自己採点基準

## Given-When-Then形式の効果

- AIがテストケースを自動生成できる
- 実装が仕様を満たしているか自己チェック可能
- 異常系・エッジケースも明示できる

## 具体化の重要性

❌ 「バリデーション」だけでは曖昧
✅ 「パスワードは8文字以上、大文字小文字数字を含む」と明示

---
<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->

<!-- _class: layout-horizontal-left -->


<!-- _class: layout-diagram-only -->

# STEP2のまとめ

![STEP2のまとめ](./assets/diagrams/diagram_46_step2_summary.svg)

---
<!-- _class: two-column -->

<!-- _class: two-column -->

<!-- _class: two-column -->


<!-- _class: two-column compact -->

## Part 1 振り返りチェックリスト

**AI活用の基本:**
- [ ] AI活用の3原則を説明できる
- [ ] Reward Hacking対策を実践できる

**Claude Code:**
- [ ] セットアップができる
- [ ] 3つのモードを使い分けられる
- [ ] 効率的な指示の出し方を実践できる

**STEP1 要件定義:**
- [ ] AIに質問させる手法を使える
- [ ] MoSCoW優先順位付けができる
- [ ] エラー・エッジケースを洗い出せる
- [ ] 受け入れ基準を書ける

**STEP2 設計ドキュメント:**
- [ ] Spec-Driven Developmentを理解
- [ ] Tech Stack Setupを最初に固める
- [ ] Mermaid記法で設計図を作成できる
- [ ] 受け入れ条件を詳細化できる

---

**Part 1 終了 - 昼休憩（12:00-13:00）**
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

<!-- _class: layout-diagram-only supercompact -->

# ドキュメント自動生成Before/After

![ドキュメント自動生成Before/After](./assets/diagrams/diagram_43_doc_automation_before_after.svg)

---

<!-- _class: card-grid compact -->

# Living Documentation 3種類

### ①architecture.md

**内容:**
- システム全体像
- 構成・ディレクトリ
- 設計判断の理由

**効果:**
- 次のセッションのAIが全体像を把握

### ②README.md

**内容:**
- セットアップ手順
- 使い方
- トラブルシューティング

**効果:**
- 誰でもすぐに開発開始できる

### ③CLAUDE.md

**内容:**
- 成功したプロンプトパターン蓄積
- ハマった点と回避策

**効果:**
- 再現性の確保、同じ失敗を繰り返さない

---

<!-- _class: two-column -->

# 計画図面 vs 完成図面（重要）

## 計画図面（設計書）

**タイミング:** 作る前

**内容:** 理想の設計

**目的:** AIへのGuardrails

## 完成図面（as-built）

**タイミング:** 作った後

**内容:** 実際に作った結果

**目的:** 次のセッションでの参照

## 必ず差分が生まれる

実装で得られた知見を記録

**例:**
- 「○○は△△の理由で××に変更」
- 「□□で30分ハマった、回避策は…」

## Living Documentationとして更新

実装と同期したドキュメント

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

<!-- _class: layout-diagram-only -->

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

<!-- _class: card-grid supercompact -->

# リバースエンジニアリングの第一歩

### ソースコード読み込み
プロジェクトルートで`claude`実行

### .claudeignoreで除外
node_modules、.git、dist、*.log除外

### AIへの指示例
「プロジェクト構造を教えて」「主要ファイルの役割は？」

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
<!-- _class: layout-horizontal-right ultracompact -->

# テストシナリオの分類

![テストシナリオの4分類](./assets/diagrams/diagram_15_test_classification.svg)

**正常系:** 想定入力→期待結果

**異常系:** 不正入力→エラー処理

**境界値:** 0/MAX/MIN確認

**例外処理:** ネットワーク/DB/タイムアウト

**効果:** 全観点網羅

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

<!-- _class: card-grid supercompact -->

# テストシナリオからテストコードへ

### なぜシナリオから？
全体像把握→モレ・ヌケ防止

### 変換プロセス
シナリオ1つ→テストメソッド1つ

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
---
marp: true
theme: ai-seminar
paginate: true
---
<!-- _class: lead supercompact -->

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

<!-- _class: layout-horizontal-right -->

# 演習の進め方（ワークフロー）

![演習ワークフロー](./assets/diagrams/diagram_17_workshop_workflow.svg)

**保守開発の4ステップワークフロー:**
- **STEP1: リバースエンジニアリング（30分）** 仕様把握、ドキュメント自動生成
- **STEP2: フィットギャップ分析＆影響範囲調査（20分）** 追加開発範囲の明確化
- **STEP3: テストシナリオ作成（30分）** 既存機能・新機能・デグレ防止を網羅
- **STEP4: テストコード実装＋機能追加（60分）** TDD、Red-Green-Refactor、AI自己レビュー、ドキュメント反映
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

<!-- _class: layout-callout supercompact -->

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

<!-- _class: card-grid -->

# 新機能のテストシナリオ作成

### 目的
**新機能が仕様通り動作することを保証**

### 対象：新規追加機能の全テストケース
- **正常系:** 期待通りの動作確認
- **異常系:** エラーハンドリング確認
- **境界値:** 0、MAX、MINでの動作確認
- **例外処理:** ネットワーク、DB接続エラー

### AIへの指示
- 「電話番号カラム追加機能のテストシナリオを作成して」
- 「正常系、異常系、境界値、例外処理を網羅して」

### 出力形式
Given-When-Then形式でシナリオ記述

### 効果
新機能の品質担保、バグ検出率向上

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

<!-- _class: layout-horizontal-left compact -->

# デグレ発生メカニズムとTDDによる予防

![デグレ発生メカニズムとTDD予防](./assets/diagrams/diagram_42_regression_mechanism.svg)

### デグレが起きる3つの原因
- AIは忘れっぽい→既存仕様を忘れる
- Jagged Intelligence→影響範囲を判断できない
- Reward Hacking→新機能優先、既存機能軽視

### TDDによる予防
- テストがあれば→AIが自動で検証
- デグレを大幅削減

### 効果
安心して機能追加、品質保証

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

<!-- _class: card-grid supercompact -->

# うまくいったポイント共有

### リバースエンジニアリング
効果的だったAIへの指示

### テストシナリオ作成
網羅性を高める方法

### AIの活用方法
生産性を上げたプロンプト

### デグレ防止の工夫
既存機能を守るテスト

---

<!-- _class: card-grid supercompact -->

# 全体ディスカッション

### 参加者からの質問
実装の工夫、解決方法

### 講師フィードバック
良かった点、改善ポイント

### ベストプラクティス
成功事例、効果的なプロンプト

---

<!-- _class: lead -->

## まとめ（30分）

---

<!-- _class: layout-diagram-only -->

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
