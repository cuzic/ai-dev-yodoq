---
marp: true
theme: ai-seminar
paginate: true
header: 'AI活用研修：新規開発編 - Day 1 Part 1'
footer: '© 2024 AI Development Seminar'
---

<!-- _class: lead -->

# AI活用研修：新規開発編

## 2日間で学ぶ、生産性を劇的に向上させる体系的アプローチ

AI駆動開発で開発期間を大幅短縮

---
<!-- _class: layout-diagram-only -->

# 本日の目標

![本日の目標](../diagrams-web/slide_002_本日の目標.svg)

---

<!-- _class: layout-horizontal-left -->

# AI活用の3原則

![AI活用の3原則](diagrams/diagram_01_ai_principles.svg)

- **Jagged Intelligence**: 得意（コード生成・テスト・アーキテクチャ設計）、苦手（ビジネス要件の解釈・トレードオフ判断）
- **Trust but Verify**: AIにもエラーあり、AI自己レビューで品質向上
- **Guardrails**: ドキュメント駆動、受入条件で手戻り防止

---

<!-- _class: layout-horizontal-left -->

# Vibe Coding vs Production Engineering

![3つのアプローチ比較](diagrams/diagram_22_vibe_vs_production.svg)

- **Vibe Coding**: 速い（30分〜1時間）、品質バラバラ、プロトタイプ向き
- **Production Engineering**: 構造化、品質保証、本番向き
- **Vibe Coding with Guardrails**: 速さと品質両立、設計書で導く

---

<!-- _class: layout-horizontal-left -->

# 開発者の役割変化

![開発者の役割変化](diagrams/diagram_02_role_change.svg)

- **従来：運転手** - コード1行ずつ、全実装詳細把握
- **AI時代：ナビゲーター** - 方向指示、AIが実装
- **人間の役割**: ビジネス要件、設計判断、品質・セキュリティ
- **AIの役割**: コード生成、テスト、リファクタリング、ドキュメント
- **効果**: 本質的価値創造に集中

---

<!-- _class: layout-horizontal-left -->

# 5-STEPフロー全体像

![5-STEPフロー](diagrams/diagram_03_5step_flow.svg)

- **STEP1: 要件定義** - 何を作るか明確化（Guardrails構築）
- **STEP2: 設計** - どう作るか定義（AI外部メモリ）
- **STEP3: タスク分解** - 全体像を小さく分割（忘れっぽさ対策）
- **STEP4: 実装** - 小さく作る・TDD・AI自己レビュー
- **STEP5: 品質担保＆ドキュメント反映** - Trust but Verify自動化、Living Documentation
- **効果:** 手戻り防止、品質保証、開発期間短縮

---

<!-- _class: layout-horizontal-right -->

# AIの制約①忘れっぽい（セッション制約）

![AIの外部メモリ](diagrams/diagram_04_ai_memory.svg)

- **セッション内のみ記憶**: ブラウザ閉じる→全忘却、20万トークン超過→古い情報忘却
- **問題**: 同じバグ繰り返し、成功方法忘却
- **対策**: ドキュメント化＝外部メモリ、architecture.md/README.mdに知見蓄積

---

<!-- _class: layout-diagram-only -->

# AIの制約②Reward Hacking（手抜き問題）

![Reward Hacking問題と対策](diagrams/diagram_39_reward_hacking_examples.svg)

---
<!-- _class: layout-diagram-only -->

# 環境準備

![環境準備](../diagrams-web/slide_009_環境準備.svg)

---

<!-- _class: layout-horizontal-left compact -->

# セキュリティベストプラクティス（補足）

![セキュリティベストプラクティス](diagrams/diagram_36_security_best_practices.svg)

**AIに必ず指示すべきセキュリティ要件:**

**🔒 認証・認可:** bcrypt、JWT、環境変数

**🛡️ 入力検証:** SQLi/XSS対策、CSRF

**🔐 データ保護:** HTTPS、機密情報は環境変数

**📊 監視:** レート制限、異常検知

---

---

<!-- _class: lead -->

## Claude Code の使い方（10:30-10:50, 20分）

---

# Claude Code とは
- **概要:** プロジェクト全体を扱うAI開発アシスタント、ターミナルから直接コード生成・修正・テスト
- **なぜClaude Codeが重要か:**
  - プロジェクト全体の文脈を理解（複数ファイルの関係性を把握）
  - 単一ファイル編集ではなく、関連ファイルを一括操作
  - Git統合で安全性を確保（コミット履歴、ロールバック可能）
- **他ツールとの違い:**
  - ChatGPT: 単一会話、ファイル手動アップロード、コンテキスト限定的
  - Cursor: エディタ内、部分編集、ファイル単位
  - Claude Code: プロジェクト全体、複数ファイル一括、Git統合、長期文脈保持
- **効果:** プロジェクト全体の一貫性を保ちながら開発

---

<!-- _class: layout-horizontal-right -->

# セットアップ

![.claudeignoreの重要性](diagrams/diagram_29_claudeignore_importance.svg)

- **インストール:** `npm install -g @anthropic-ai/claude-code`
- **APIキー取得:** https://console.anthropic.com
- **初回起動:** `claude`（APIキー入力、.claudeignore設定）
- **.claudeignore必須:**
  - node_modules/, dist/, .git/, *.log を除外
  - トークン節約、コスト削減

---

<!-- _class: layout-horizontal-left -->

# 4つのモード比較

![Claude Codeモード比較](diagrams/diagram_28_claude_code_modes.svg)

- **通常モード:** 毎回確認 (y/n)、最も安全
- **YOLOモード（Shift+Tab）:** 自動実行、確認時間を大幅削減、Git管理済み推奨
- **プランモード（Shift+Tab×2）:** 計画→確認→実行、大規模タスク向き
- **dangerously-skip-permissions:** 全確認スキップ（超危険）

---

<!-- _class: two-column -->

# モード詳細と使い分け

**通常モード（デフォルト）**
- 毎回確認 (y/n)、初心者向け、安全第一

**YOLOモード（Shift+Tab）**
- 自動実行、確認作業を省略して効率化
- 条件: Git管理済み、タスク明確
- 使用例: プロトタイプ、新機能開発

**プランモード（Shift+Tab×2）**
- 計画→確認→実行の3段階
- 大規模タスク、複雑なリファクタリング向き

**dangerously-skip-permissionsモード**
- 全確認スキップ（超危険）
- 用途: CI/CD、デモ、最高速開発
- Dev Container推奨: コンテナ内→安全化

---
<!-- _class: layout-diagram-only -->

# よくある問題と対処法

![よくある問題と対処法](../diagrams-web/slide_017_よくある問題と対処法.svg)

---

<!-- _class: layout-horizontal-right compact -->

# 効率的な指示の出し方

![プロンプトパターン（良い例vs悪い例）](diagrams/diagram_30_prompt_patterns.svg)

**❌ 悪い:** 「ログイン機能を作って」

**✅ 良い:** 制約明示（bcrypt、環境変数、@Valid）、段階的実装、質問促す、AI自己レビュー

**サイクル:** 指示→実装→レビュー→テスト→コミット

---

---

<!-- _class: lead -->

## STEP1: 要件定義（10:50-11:30, 40分）

---

# STEP1 要件定義とは
- **目的:** 「何を作るか」を明確化
- **なぜ最初に要件定義が必要か（Guardrails）**
  - AIはJagged Intelligence（技術実装は得意だがビジネス要件の解釈は苦手）
  - Reward Hacking→曖昧な仕様だと手抜き実装
  - 明確な要件＝AIが道を外れない境界線
- **成果物:**
  - 要件定義ドキュメント（docs/requirements.md）
  - ユーザーストーリー、機能一覧、受け入れ基準
- **効果:** 後工程の手戻り防止

---
<!-- _class: layout-diagram-only -->

# AIに質問させる手法

![AIに質問させる手法](../diagrams-web/slide_022_AIに質問させる手法.svg)

---

<!-- _class: layout-horizontal-left -->

# 要件の引き出し方（文字起こしアプローチ）

![文字起こし→AI抽出フロー](diagrams/diagram_40_transcript_approach.svg)

## なぜ強力か

**顧客の言葉をそのまま記録:** 解釈のズレゼロ、「言った/言わない」問題の解消

**AIが要件構造化:** 漏れ・ヌケ防止、自動優先順位付け

## 4ステップ

**STEP1: 録音** Zoom/Google Meet録画

**STEP2: 文字起こし** Whisper API、Claude Code直接音声入力

**STEP3: AI抽出** 「この文字起こしから要件を抽出して」

**STEP4: 確認** ユーザーストーリー、MoSCoW分類、不明点確認

---

<!-- _class: layout-horizontal-left -->

# MoSCoW 優先順位付け

![MoSCoW優先順位](diagrams/diagram_05_moscow.svg)

- **Must（必須）:** プロダクト成立に不可欠な機能 → Phase 1 (MVP)
- **Should（重要）:** あるべきだが、なくても動く → Phase 2
- **Could（あれば良い）:** あると嬉しい → Phase 3
- **Won't（今回はやらない）:** 将来的には考える、スコープ外
- **原則:** Mustは全体の20〜30%に絞る（欲張らない）
- **効果:** Phase分けで段階的リリース、開発期間短縮

---

<!-- _class: layout-diagram-only -->

# MoSCoW実践例（ToDoアプリ）

![MoSCoW実践例（ToDoアプリ）](diagrams/diagram_47_moscow_example.svg)

---

<!-- _class: layout-horizontal-right -->

# ユーザーストーリーマッピング

![ユーザーストーリーマッピング](diagrams/diagram_31_user_story_mapping.svg)

- **フォーマット:** `<誰が> <何をしたい> <なぜ>`
- **例:** ユーザーとして、タスクを追加したい（忘れないため）
- **ユーザーの旅:**
  1. タスク管理（追加・完了・削除）
  2. タスク整理（カテゴリ・優先度）
  3. 進捗確認（完了数・期限）
- **効果:** AIが「なぜ」を理解→本質的な価値を実装

---

<!-- _class: layout-horizontal-left compact -->

# 非機能要件

![非機能要件チェックリスト](diagrams/diagram_32_nonfunctional_requirements.svg)

**なぜ重要か:** 機能要件だけでは本番で使えない（性能・セキュリティ・拡張性）

**⚡ パフォーマンス:** 1000件快適、200ms以内

**🔒 セキュリティ:** JWT、bcrypt、HTTPS

**📈 スケーラビリティ:** 同時100人

**📱 モバイル:** レスポンシブ

---

<!-- _class: layout-diagram-only -->

# エラー・エッジケース・制約の洗い出し

![エラー・エッジケース・制約の洗い出し](diagrams/diagram_45_error_edge_constraint.svg)

---

# 受け入れ基準（Given-When-Then）
- **正常系:**
  - Given: 登録済みユーザー
  - When: 正しいメール・パスワードでログイン
  - Then: トークン発行、ダッシュボードへリダイレクト
- **異常系:**
  - Given: 登録済みユーザー
  - When: 間違ったパスワードでログイン
  - Then: エラーメッセージ、5回失敗でロック
- **効果:** 「完成の定義」を明確化

---

# プロトタイプ駆動開発（Vibe Coding）
- **従来:** 文章 → 実装 → 「イメージと違う」
- **Vibe Coding:** ビジュアルで確認しながら調整
- **ツール:** Claude Code（Thymeleaf/HTML/Bootstrap）
- **指示例:**
  ```
  「ToDoアプリのプロトタイプをThymeleafで作って。
  タスク追加フォーム、一覧表示、削除ボタン。Bootstrap使用」
  ```
- **ステップ:** 確認 → 修正指示 → 即座に反映 → OK!
- **メリット:** クライアントとの認識合わせが簡単

---
<!-- _class: layout-diagram-only -->

# STEP1のまとめ

![STEP1のまとめ](../diagrams-web/slide_031_STEP1のまとめ.svg)

---

<!-- _class: layout-horizontal-left -->

# STEP1 チェックリスト

![STEP1チェックリスト](diagrams/diagram_34_step1_checklist.svg)

**必ず確認:**
- [ ] AIに質問させて曖昧さ排除
- [ ] MoSCoW優先順位付け
- [ ] ユーザーストーリー作成
- [ ] 非機能要件定義
- [ ] エラー・エッジケース洗い出し
- [ ] Given-When-Then基準作成
- [ ] docs/requirements.md文書化

---

---

<!-- _class: lead -->

## STEP2: 設計ドキュメント作成（11:30-12:00, 30分）

---

# STEP2 設計ドキュメントとは
- **目的:** 「どのように作るか」を明確にする設計図
- **なぜ設計書が必要か（Guardrails + 忘れっぽさ対策）**
  - AIは忘れっぽい→セッション超えると設計意図を忘れる
  - Reward Hacking→設計がないと手抜き実装
  - 設計書＝AIが何度でも参照できる道しるべ
- **Spec-Driven Development:**
  - Code-First → Spec-First へ
  - 設計書がAIのガードレール
- **効果:** AIが設計に従って実装、一貫性のある構造

---

<!-- _class: layout-horizontal-right -->

# 設計ドキュメントの構造

![設計ドキュメントの7要素](diagrams/diagram_06_spec_structure.svg)

- **1. 技術スタック:** フロント・バック・DB・ライブラリ（選定理由含む）
- **2. システムアーキテクチャ:** 3層構造、Mermaid図で可視化
- **3. データベーススキーマ:** テーブル定義・カラム・制約・インデックス
- **4. API仕様:** エンドポイント・メソッド・パラメータ・レスポンス
- **5. 受入条件（BDD形式）:** Given-When-Then
- **6. セキュリティ設計:** 認証・認可・入力検証・環境変数管理
- **7. 技術的決定事項:** ライブラリ選定理由・アーキテクチャ判断

---

# Tech Stack Setup
- **最初に固める理由:** 後から変更すると大幅な手戻り
- **例:**
  - フロントエンド: Thymeleaf / JSP
  - バックエンド: Spring Boot
  - データベース: PostgreSQL / MySQL
  - 認証: Spring Security + JWT
  - 日付処理: Java 8 Date/Time API（理由: 標準ライブラリ）
  - テスト: JUnit 5 + Mockito
- **選定理由も明記:** 技術的判断の根拠を残す

---

<!-- _class: layout-horizontal-left -->

# データベーススキーマ設計

![ER図の例](diagrams/diagram_07_er_diagram.svg)

- **なぜスキーマ定義が必要か**
  - 後から変更すると影響範囲が非常に大きい
  - AIは明示的な指示がないと不適切な設計をする
- **スキーマ定義で得られる効果**
  - AIが正確なSQL・ORM実装ができる
  - カラム名・型・制約の一貫性が保たれる
  - マイグレーションの自動生成が可能
- **AIへの指示:** テーブル構造を明確に文書化

---

# API仕様の明確化
- **なぜAPI仕様が必要か**
  - 仕様がないとAIがエンドポイントを勝手に決める
  - フロントとバックで認識齟齬が発生
- **API仕様で得られる効果**
  - フロントエンドとバックエンドの並行開発が可能
  - AIが仕様通りのエンドポイントを実装
  - バリデーション・エラーハンドリングの一貫性
  - 後からのAPI変更時に影響範囲が明確

---

<!-- _class: layout-horizontal-right -->

# Mermaid記法とSVG生成でビジュアル化

![Mermaid vs SVG使い分け](diagrams/diagram_41_mermaid_vs_svg.svg)

- **Mermaid**: テキストで図描画、Git管理可、AI自動生成、GitHub/VS Code表示
- **SVG生成magic word**: 「SVGで書いて」→AI生成→即可視化、記法不要
- **使い分け**: Mermaid=GitHub用、SVG=即可視化・プレゼン用

---

<!-- _class: layout-horizontal-left -->

# ER図が開発をスムーズにする理由

![ER図からコード生成](diagrams/diagram_08_er_to_code.svg)

- **AIの実装**: CREATE TABLE自動生成、JOIN処理、外部キー、ORMモデル
- **人間の恩恵**: 全体像一目把握、リレーション検証、正規化問題発見

---

<!-- _class: layout-horizontal-right -->

# シーケンス図がAI実装を助ける理由

![シーケンス図の例（ログインフロー）](diagrams/diagram_09_sequence_login.svg)

- **AIの実装**: 処理順序理解→正確コードフロー、エラー処理タイミング、依存関係、トランザクション境界
- **図なしの問題**: 処理順序推測ミス、ロールバック漏れ
- **効果**: 複雑処理も正確実装

---

# 受け入れ条件の詳細化
- **なぜ受け入れ条件が必要か**
  - AIは「タスク完了」を優先し、品質は二の次
  - 明確な合格基準がないと手抜き実装になる
  - 受け入れ条件 = AIの自己採点基準
- **Given-When-Then形式の効果**
  - AIがテストケースを自動生成できる
  - 実装が仕様を満たしているか自己チェック可能
  - 異常系・エッジケースも明示できる
- **具体化の重要性**
  - 「バリデーション」だけでは曖昧
  - 「パスワードは8文字以上、大文字小文字数字を含む」と明示
  - AIは具体的な条件をそのままコード化できる

---

<!-- _class: layout-diagram-only -->

# STEP2のまとめ

![STEP2のまとめ](diagrams/diagram_46_step2_summary.svg)

---

<!-- _class: layout-horizontal-left -->

# STEP2 チェックリスト

![STEP2チェックリスト](diagrams/diagram_35_step2_checklist.svg)

**必ず確認:**
- [ ] Tech Stack確定
- [ ] アーキテクチャ図作成
- [ ] ER図作成
- [ ] API仕様定義
- [ ] シーケンス図作成
- [ ] 受入条件詳細化
- [ ] セキュリティ設計
- [ ] docs/spec.md作成

---

<!-- _class: two-column -->

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

**スライド数: 35枚**
