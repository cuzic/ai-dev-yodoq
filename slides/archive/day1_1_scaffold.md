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
<!-- TODO: /slide-tdd で詳細化 -->
---
<!-- _class: two-column -->

# 本日の目標

## 🎯 1日目のゴール
**5-STEPフローを理解し、新規開発の基本を習得**

## ⏰ タイムテーブル
- 午前2時間（Part 1）：基礎+STEP1-2
- 午後2時間（Part 2）：STEP3-6
- 演習2時間（Part 3）：実践演習

## 📚 再現可能な開発手法の習得

**①プロンプトパターンの習得**
- 成功するAIへの指示方法
- Trust but Verify の実践

**②5-STEPフローのマスター**
- STEP1: 要件定義
- STEP2: 設計
- STEP3: タスク分解
- STEP4: 実装
- STEP5: 品質担保＆ドキュメント反映

**③AI制約への対応**
- Jagged Intelligence（得意/苦手の把握）
- Reward Hacking（手抜き防止）
- 忘れっぽさ（ドキュメント化）

## 🚀 効果
✅ 明日から実務で使える
✅ チーム展開可能
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
<!-- _class: layout-horizontal-left -->

# AI活用の3原則

![AI活用の3原則](diagrams/diagram_01_ai_principles.svg)

- **Jagged Intelligence**: 得意（コード生成・テスト・アーキテクチャ設計）、苦手（ビジネス要件の解釈・トレードオフ判断）
- **Trust but Verify**: AIにもエラーあり、AI自己レビューで品質向上
- **Guardrails**: ドキュメント駆動、受入条件で手戻り防止
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-horizontal-left -->

# Vibe Coding vs Production Engineering

![3つのアプローチ比較](diagrams/diagram_22_vibe_vs_production.svg)

- **Vibe Coding**: 速い（30分〜1時間）、品質バラバラ、プロトタイプ向き
- **Production Engineering**: 構造化、品質保証、本番向き
- **Vibe Coding with Guardrails**: 速さと品質両立、設計書で導く
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-horizontal-left -->

# 開発者の役割変化

![開発者の役割変化](diagrams/diagram_02_role_change.svg)

- **従来：運転手** - コード1行ずつ、全実装詳細把握
- **AI時代：ナビゲーター** - 方向指示、AIが実装
- **人間の役割**: ビジネス要件、設計判断、品質・セキュリティ
- **AIの役割**: コード生成、テスト、リファクタリング、ドキュメント
- **効果**: 本質的価値創造に集中
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-horizontal-right -->

# AIの制約①忘れっぽい（セッション制約）

![AIの外部メモリ](diagrams/diagram_04_ai_memory.svg)

- **セッション内のみ記憶**: ブラウザ閉じる→全忘却、20万トークン超過→古い情報忘却
- **問題**: 同じバグ繰り返し、成功方法忘却
- **対策**: ドキュメント化＝外部メモリ、architecture.md/README.mdに知見蓄積
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-diagram-only -->

# AIの制約②Reward Hacking（手抜き問題）

![Reward Hacking問題と対策](diagrams/diagram_39_reward_hacking_examples.svg)
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: two-column -->

# 環境準備

## ✅ 必須ツール

**📦 Claude Code**
- AI開発環境
- プロジェクト全体を扱うAIアシスタント
- **なぜ必要:** プロジェクト全体の文脈を理解、複数ファイル一括操作

**🔧 GitHub**
- バージョン管理
- 頻繁なコミットで暴走対策
- **なぜ必要:** AIの暴走から回復可能

**💻 VS Code**
- エディタ
- Mermaid Preview拡張推奨
- **なぜ必要:** 図の即座確認、開発体験向上

## 🌟 推奨ツール

**🐳 Dev Container**
- 環境統一化
- dangerously-skip-permissionsモードの安全利用
- **なぜ推奨:**
  - 環境の再現性（全員同じ環境）
  - 実験の安全性（コンテナ内で隔離）
  - チーム開発でのトラブル防止

## 📋 セットアップチェックリスト
- [ ] Claude Code インストール
- [ ] GitHub アカウント
- [ ] VS Code + Mermaid Preview
- [ ] (推奨) Dev Container
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
<!-- _class: layout-diagram-only -->

# セキュリティベストプラクティス（補足）

![セキュリティベストプラクティス](diagrams/diagram_36_security_best_practices.svg)

**AIに必ず指示すべきセキュリティ要件:**

**🔒 認証・認可:**
- bcrypt でパスワードハッシュ化
- JWT または セッション認証
- 環境変数で秘密鍵管理

**🛡️ 入力検証:**
- SQL injection 対策（PreparedStatement）
- XSS 対策（エスケープ処理）
- CSRF トークン

**🔐 データ保護:**
- HTTPS 必須
- 機密情報は環境変数
- ログに機密情報を出さない

**📊 監視:**
- ログイン失敗回数制限
- レート制限
- 異常アクセス検知
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---

<!-- TODO: /slide-tdd で詳細化 -->
---
<!-- _class: lead -->

## Claude Code の使い方（10:30-10:50, 20分）
<!-- TODO: /slide-tdd で詳細化 -->
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
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
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
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-horizontal-left -->

# 4つのモード比較

![Claude Codeモード比較](diagrams/diagram_28_claude_code_modes.svg)

- **通常モード:** 毎回確認 (y/n)、最も安全
- **YOLOモード（Shift+Tab）:** 自動実行、確認時間を大幅削減、Git管理済み推奨
- **プランモード（Shift+Tab×2）:** 計画→確認→実行、大規模タスク向き
- **dangerously-skip-permissions:** 全確認スキップ（超危険）
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
<!-- _class: two-column -->

# よくある問題と対処法

## 🚫 問題①「ファイルが多すぎる」

**症状:**
- Claude Codeが反応しない
- トークン制限エラー頻発

**原因:**
- node_modules等を読もうとする
- ビルド成果物を含んでいる

**✅ 対処法:**
```bash
# .claudeignore に追加
node_modules/
dist/
build/
.git/
*.log
```

## ⏱️ 問題②「トークン制限」

**症状:**
- 「コンテキストが満杯」エラー
- 処理が途中で止まる

**原因:**
- コンテキストウィンドウ超過
- 長いセッションの継続

**✅ 対処法:**
1. `/compact` コマンド実行
2. タスクを分割して新セッション
3. 不要なファイルを .claudeignore

## 🎯 問題③「AIが間違った方向」

**症状:**
- 意図しない実装
- 想定外のコード生成

**原因:**
- 曖昧な指示
- コンテキスト不足

**✅ 対処法:**
1. `n` で即座に止める
2. 明確に再指示（具体例を示す）
3. プランモード活用（確認→実行）
4. 「確認したいことはある?」と質問促す
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
<!-- _class: layout-horizontal-right -->

# 効率的な指示の出し方

![プロンプトパターン（良い例vs悪い例）](diagrams/diagram_30_prompt_patterns.svg)

- **❌ 悪い指示:** 「ログイン機能を作って」
- **✅ 良い指示:**
  - 制約を明示（bcrypt、環境変数、バリデーション、レート制限）
  - 段階的に進める（1機能ずつ）
  - 質問を促す（「確認したいことはある？」）
  - 自己レビュー依頼（実装後必ず）
- **毎回のサイクル:**
  - 指示 → 実装 → AI自己レビュー → 修正 → テスト → コミット
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---

<!-- TODO: /slide-tdd で詳細化 -->
---
<!-- _class: lead -->

## STEP1: 要件定義（10:50-11:30, 40分）
<!-- TODO: /slide-tdd で詳細化 -->
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
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
<!-- _class: two-column -->

# AIに質問させる手法

## ❌ 問題: AIは「良きに計らう」

**Jagged Intelligence（能力のギザギザ）:**
- ✅ 得意: コード生成、テスト作成、リファクタリング、技術設計
- ❌ 苦手: ビジネス要件の解釈、ステークホルダー間の優先順位判断、ドメイン固有ルール
- 結果: 曖昧な指示では勝手に推測して間違った方向へ

**具体例:**
- 「ログイン機能を作って」
  → AIが勝手にJWT選択
  → 実はセッション認証が要件だった
  → 手戻り発生

## ✅ 解決策: AIに質問させる

**プロンプトパターン:**
```
「ログイン機能を実装する前に、
確認したいことはある？」
```

**AIの反応:**
- 認証方式は？（セッション vs JWT）
- パスワードポリシーは？
- 多要素認証は必要？
- セッション期限は？

**対話で仕様を固める:**
- 人間が判断（ビジネス要件に基づく）
- AIが実装（技術的実現）

## 📊 効果

✅ 曖昧さ排除
✅ 人間が判断、AIが実装
✅ 手戻りゼロ
✅ 実装スピード大幅向上
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
<!-- _class: layout-horizontal-left -->

# 要件の引き出し方（文字起こしアプローチ）

![文字起こし→AI抽出フロー](diagrams/diagram_40_transcript_approach.svg)

## 🎯 なぜこの手法が強力か

**顧客の言葉をそのまま記録:**
- 解釈のズレゼロ
- 「言った/言わない」問題の解消
- 顧客の本当のニーズを捉える

**AIが要件構造化:**
- 漏れ・ヌケ防止
- 自動で優先順位付け
- **不明点リスト**も自動生成

## 🔄 4ステップワークフロー

**STEP1: 録音**
- Zoom/Google Meet録画
- 音声だけでもOK

**STEP2: 文字起こし**
- Whisper API（高精度）
- Google Docs音声入力
- Claude Codeに直接音声入力

**STEP3: AI抽出依頼**
```
「この文字起こしから
要件を抽出して」
```

**STEP4: AI出力確認**
- ユーザーストーリー
- 機能一覧（MoSCoW分類済み）
- **不明点リスト** → クライアント確認

## 💡 実践例

**顧客の言葉:**
「営業が顧客管理したい。スマホ対応。Excel同時編集で困ってる」

**AI抽出結果:**
- Must: 顧客CRUD、モバイル対応
- 不明点: 顧客項目定義？ステータス管理？
→ クライアント確認
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-diagram-only -->

# MoSCoW実践例（ToDoアプリ）

![MoSCoW実践例（ToDoアプリ）](diagrams/diagram_47_moscow_example.svg)
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-horizontal-left -->

# 非機能要件

![非機能要件チェックリスト](diagrams/diagram_32_nonfunctional_requirements.svg)

## 🎯 なぜ非機能要件が重要か

**機能要件だけでは本番で使えない:**
- 性能不足（遅い、落ちる）
- セキュリティ脆弱性
- 拡張性の欠如

**AIは明示しないと考慮しない:**
- Reward Hacking → 手抜き実装
- 非機能要件 = Guardrails

## 📊 4つの重要カテゴリ

**⚡ パフォーマンス**
- 1000件まで快適動作
- レスポンス200ms以内
- N+1クエリ禁止

**🔒 セキュリティ**
- JWT認証
- bcryptハッシュ化
- HTTPS必須
- OWASP Top 10対応

**📈 スケーラビリティ**
- 同時接続100人
- 将来1000人対応可能な設計
- 水平スケール考慮

**📱 モバイル対応**
- レスポンシブデザイン必須
- タッチ操作最適化
- オフライン対応考慮

## 💡 AIへの指示
**「非機能要件も満たして実装」と明示**
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-diagram-only -->

# エラー・エッジケース・制約の洗い出し

![エラー・エッジケース・制約の洗い出し](diagrams/diagram_45_error_edge_constraint.svg)
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
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
<!-- TODO: /slide-tdd で内容充実 -->
---
<!-- _class: two-column -->

# STEP1のまとめ

## 📋 要件定義の6ステップ

**STEP1-1: 要件引き出し**
- AIに質問させる手法
- 文字起こしアプローチ

**STEP1-2: 整理**
- MoSCoW優先順位付け
- Mustは20-30%に絞る

**STEP1-3: 構造化**
- ユーザーストーリーマッピング
- ジャーニーマップ

**STEP1-4: 非機能要件定義**
- ⚡ パフォーマンス
- 🔒 セキュリティ
- 📈 スケーラビリティ

**STEP1-5: エッジケース洗い出し**
- エラーケース
- エッジケース
- 制約条件
- Given-When-Then受け入れ基準

**STEP1-6: 可視化・文書化**
- Vibe Codingプロトタイプ
- docs/requirements.md作成

## 🎯 なぜこの順序か

**段階的に曖昧さを排除:**
1. 何を作るか（引き出し）
2. 優先順位（絞り込み）
3. ユーザー視点（構造化）
4. 品質基準（非機能要件）
5. 異常系（エッジケース）
6. 可視化（プロトタイプ）

**AIへのGuardrails構築:**
- 明確な要件 = AIが迷わない
- 受け入れ基準 = 手抜き防止

## 📊 効果

✅ 後工程の手戻り防止
✅ 開発期間短縮
✅ AIが正確に実装
✅ 品質の安定化
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
<!-- _class: layout-diagram-only -->

# STEP1 チェックリスト

![STEP1チェックリスト](diagrams/diagram_34_step1_checklist.svg)

**必ず確認:**
- [ ] 要件をAIに質問させて曖昧さを排除した
- [ ] MoSCoWで優先順位付け（Mustは20-30%）
- [ ] ユーザーストーリーマッピング作成
- [ ] 非機能要件（性能・セキュリティ・拡張性）定義
- [ ] エラー・エッジケースを洗い出した
- [ ] Given-When-Then受け入れ基準作成
- [ ] Vibe Codingでプロトタイプ確認
- [ ] docs/requirements.md に文書化

**次のステップ:**
→ STEP2: 設計ドキュメント作成へ
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---

<!-- TODO: /slide-tdd で詳細化 -->
---
<!-- _class: lead -->

## STEP2: 設計ドキュメント作成（11:30-12:00, 30分）
<!-- TODO: /slide-tdd で詳細化 -->
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
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
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
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
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
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で内容充実 -->
---
<!-- _class: layout-horizontal-right -->

# Mermaid記法とSVG生成でビジュアル化

![Mermaid vs SVG使い分け](diagrams/diagram_41_mermaid_vs_svg.svg)

- **Mermaid**: テキストで図描画、Git管理可、AI自動生成、GitHub/VS Code表示
- **SVG生成magic word**: 「SVGで書いて」→AI生成→即可視化、記法不要
- **使い分け**: Mermaid=GitHub用、SVG=即可視化・プレゼン用
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-horizontal-left -->

# ER図が開発をスムーズにする理由

![ER図からコード生成](diagrams/diagram_08_er_to_code.svg)

- **AIの実装**: CREATE TABLE自動生成、JOIN処理、外部キー、ORMモデル
- **人間の恩恵**: 全体像一目把握、リレーション検証、正規化問題発見
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-horizontal-right -->

# シーケンス図がAI実装を助ける理由

![シーケンス図の例（ログインフロー）](diagrams/diagram_09_sequence_login.svg)

- **AIの実装**: 処理順序理解→正確コードフロー、エラー処理タイミング、依存関係、トランザクション境界
- **図なしの問題**: 処理順序推測ミス、ロールバック漏れ
- **効果**: 複雑処理も正確実装
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
<!-- _class: layout-diagram-only -->

# STEP2のまとめ

![STEP2のまとめ](diagrams/diagram_46_step2_summary.svg)
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
---
<!-- _class: layout-diagram-only -->

# STEP2 チェックリスト

![STEP2チェックリスト](diagrams/diagram_35_step2_checklist.svg)

**必ず確認:**
- [ ] Tech Stack確定（フロント・バック・DB・ライブラリ）
- [ ] システムアーキテクチャ図作成（Mermaid/SVG）
- [ ] ER図作成（テーブル・カラム・制約・インデックス）
- [ ] API仕様定義（全エンドポイント）
- [ ] シーケンス図作成（複雑な処理フロー）
- [ ] 受入条件詳細化（具体的な値で）
- [ ] セキュリティ設計（認証・認可・入力検証）
- [ ] docs/spec.md 作成完了

**次のステップ:**
→ STEP3: タスク分解へ（Part 2）
<!-- TODO: /slide-tdd で確認、既存SVGを活用 -->
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
<!-- TODO: /slide-tdd で内容調整、compactレイアウト検討 -->
---
**Part 1 終了 - 昼休憩（12:00-13:00）**

**スライド数: 35枚**
<!-- TODO: /slide-tdd で詳細化 -->