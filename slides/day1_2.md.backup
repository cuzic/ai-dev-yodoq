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

# Day 1-2: タスク分解 + 実装 + 品質担保 + リファクタリング (13:00-14:50)

---

<!-- _class: lead -->

## STEP3: タスク分解（35分）

---

<!-- _class: two-column -->

# STEP3 タスク分解とは

## 🎯 目的
**大きな機能を実装可能な小さなタスクに分解**

## 🚨 なぜタスク分解が必要か

**AIの思考を言語化:**
- AIは忘れっぽい→全体像を把握しづらい
- Reward Hacking→いきなり実装すると手抜きしがち
- **計画書＝AIの思考を可視化**

**人間の役割:**
- AIの計画をレビュー
- 実装前に軌道修正
- 「あっ、そっちじゃない」が言える

## 📊 効果

✅ 実装前に方向性確認
✅ 手戻り防止
✅ 開発リスク最小化
✅ 進捗の可視化

---

<!-- _class: two-column -->

# タスク分解 = AIの思考を言語化（重要）

## 🧠 AIに計画を立てさせる理由

**Trust but Verify:**
- AIにもエラーあり
- 実装前に確認必須
- AIが「何をしようとしているか」を事前に把握

**人間の思考整理と同じ:**
- 人間：頭の中を整理してから実装
- AI：計画を立ててから実装
- **整理せずに実装 = 迷走**

## 💡 プロンプト例

```
「この設計書（docs/spec.md）に基づいて、
実装タスク一覧を作成してください。

- Phase分けして
- 各タスクは30分〜2時間で完了
- 依存関係を明示
- 完了条件を具体的に」
```

## 📊 効果

✅ AIの思考が可視化される
✅ 実装前に方向性確認
✅ 計画段階で軌道修正
✅ コスト削減・時間短縮

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

<!-- _class: two-column -->

# タスク粒度（30分〜2時間）

## 🎯 なぜ適切な粒度が重要か

**❌ 大きすぎるタスク:**
- 進捗が見えない
- AIが全体像を見失う
- 問題発見が遅れる
- モチベーション低下

**❌ 小さすぎるタスク:**
- 管理コストが増大
- オーバーヘッド増加
- タスク切り替えの手間

## ✅ 適切な粒度

**時間:** 30分〜2時間
**頻度:** 1日で3-5タスク程度
**判断基準:** 1回のコミットで完結できるか？

## 📋 良い例 vs 悪い例

**✅ 良い例（適切な粒度）:**
- ユーザー登録API実装
- ログイン機能のテスト作成
- パスワードリセットメール送信

**❌ 悪い例（大きすぎ）:**
- バックエンド全部
- 認証システム全体
- ユーザー管理機能一式

## 📊 効果

✅ モチベーション維持
✅ 問題の早期発見
✅ 進捗の可視化
✅ 達成感を継続的に得られる

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

<!-- _class: two-column -->

# STEP3のまとめ

## 📋 タスク分解の本質

**タスク分解＝AIの思考を言語化:**
- 計画を可視化
- 人間が軌道修正できる
- 実装前に「あっ、そっちじゃない」

## 🎯 5つのキーポイント

**①Phase分け戦略**
- Phase 1: 基盤
- Phase 2: コア機能
- Phase 3: 拡張機能
- Phase 4: 仕上げ

**②適切な粒度**
- 30分〜2時間で1タスク
- 1日で3-5タスク
- 進捗が見える

**③依存関係の明示**
- 手戻り防止
- 効率的なスケジューリング
- 並行作業の特定

**④タスク一覧テンプレート**
- Phase・タスク名・所要時間
- 依存関係・完了条件
- Markdown形式でGit管理

**⑤AI活用**
- 計画作成時間を大幅短縮
- 人間はレビューに集中

## 📊 効果

✅ 実装前に方向性確認
✅ リスク最小化
✅ 進捗の可視化
✅ 手戻り防止

---

<!-- _class: layout-diagram-only -->

# STEP3 チェックリスト

![STEP3チェックリスト](diagrams/diagram_37_step3_checklist.svg)

**必ず確認:**
- [ ] タスク一覧をAIに生成させた
- [ ] Phase分け（Phase 1-4）
- [ ] 各タスクは30分〜2時間
- [ ] 依存関係を明示
- [ ] 完了条件を具体的に記載
- [ ] 並行作業可能なタスクを特定
- [ ] テンプレート形式で記載
- [ ] docs/tasks.md に文書化

**次のステップ:**
→ STEP4: 実装へ

---

---

<!-- _class: lead -->

## STEP4: 実装（40分）

---

<!-- _class: two-column -->

# 実装の3原則（AIの制約に対応）

### ①小さく作る（Increment）
- **理由:** AIは忘れっぽいので小刻みに
- **方法:** 1タスク30分〜2時間で完了
- **効果:** 常に動く状態を維持、問題を早期発見

### ②テスト駆動（TDD/BDD）
- **理由:** Trust but Verify、AIが自己完結
- **方法:** Red-Green-Refactorサイクル
- **効果:** AIが自動でテスト→修正を繰り返す

### ③AI自己レビュー必須
- **理由:** Reward Hacking対策、手抜き検出
- **方法:** 「このコードをレビューして」と毎回指示
- **効果:** 多くのバグを自動検出

---

<!-- _class: two-column -->

# 実装の標準ワークフロー

## 🔄 1タスクごとの7ステップサイクル

**STEP1: タスク選択**
- タスク一覧から次のタスクを選ぶ
- 依存関係を確認

**STEP2: テスト作成（Red）**
- 失敗するテストを書く
- Given-When-Then形式

**STEP3: 実装（Green）**
- 最小実装でテストを通す
- 過剰実装しない

**STEP4: AI自己レビュー**
```
「このコードをレビューして」
```

**STEP5: 修正**
- レビュー指摘事項を修正
- セキュリティ・エッジケース対応

**STEP6: 動作確認**
- 実際に動かして確認
- E2Eテスト実行

**STEP7: コミット**
- Git管理
- 明確なコミットメッセージ

## 🔁 繰り返し

**1タスク完了 → 次のタスク**

このサイクルを繰り返すことで:
- ✅ 常に動く状態を維持
- ✅ 問題を早期発見
- ✅ 品質を継続的に保証

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

<!-- _class: two-column -->

# パスワード・JWT認証の実装

## ❌ NG例（Reward Hacking）

**AIが手抜きする典型例:**
- 平文パスワード保存
- APIキーをハードコーディング
- 「とりあえず動く」実装
- セキュリティ無視

**なぜこうなるか:**
- タスク完了を最優先（Reward Hacking）
- セキュリティへの報酬がない
- セキュリティベストプラクティスは知っているが、明示しないと省略

## ✅ ベストプラクティス

**パスワード処理:**
```java
// 登録時
String hashed = passwordEncoder.encode(password);
user.setPassword(hashed);

// ログイン時
boolean matches = passwordEncoder.matches(
  inputPassword,
  user.getPassword()
);
```

**JWT秘密鍵管理:**
```java
@Value("${jwt.secret}")
private String jwtSecret;
```

**.envファイル:**
```bash
JWT_SECRET=your-256-bit-secret-key
DATABASE_PASSWORD=secure-password
```

## 💡 プロンプトに必ず明記

```
「ユーザー登録APIを実装。
以下を必須で守ること:
- BCryptでパスワードハッシュ化
- JWT秘密鍵は環境変数から取得
- .envファイルを使用
- .gitignoreに.envを追加」
```

**明示しないとAIは手抜きする！**

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

<!-- _class: two-column -->

# STEP4のまとめ

## 🎯 実装の3原則

**①小さく作る（Increment）**
- AIは忘れっぽい対策
- 30分〜2時間で1タスク
- 常に動く状態を維持

**②テスト駆動（TDD/BDD）**
- Trust but Verify自動化
- AIが自己完結
- Red-Green-Refactorサイクル

**③AI自己レビュー必須**
- Reward Hacking対策
- 手抜き検出
- 40-60%のバグを自動検出

## 🔒 セキュリティファースト

**必須項目:**
- ✅ BCryptパスワードハッシュ化
- ✅ 環境変数で機密情報管理
- ✅ @Validバリデーション
- ✅ OWASP Top 10対応

**プロンプトに明示:**
```
「BCrypt・環境変数・@Valid必須」
```

## 🔄 標準ワークフロー

**7ステップサイクル:**
1. タスク選択
2. テスト作成（Red）
3. 実装（Green）
4. AI自己レビュー
5. 修正
6. 動作確認
7. コミット

## 📊 効果

✅ 早期問題発見
✅ セキュアな実装
✅ AIが自己完結
✅ 品質の自動保証

---

<!-- _class: layout-diagram-only -->

# STEP4 チェックリスト

![STEP4チェックリスト](diagrams/diagram_38_step4_checklist.svg)

**必ず確認:**
- [ ] 1タスク30分〜2時間で完了
- [ ] Given-When-Thenテストを先に作成
- [ ] 最小実装でテストを通した
- [ ] AI自己レビュー実施
- [ ] セキュリティ要件を満たした（BCrypt・環境変数・@Valid）
- [ ] エラーハンドリング実装
- [ ] エッジケース対応
- [ ] 動作確認完了
- [ ] コミット実施

**次のステップ:**
→ STEP5: 品質担保＆ドキュメント反映へ

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

<!-- _class: two-column -->

# AI自己レビュー4種類の使い分け

**なぜ観点別レビューが必要か**
- 一般レビューだけでは専門的な問題を見落とす
- 観点別レビューで検出率が大幅向上

**①一般**
- 実装直後（毎回必須）
- ロジックエラー、エッジケース、命名規則

**②セキュリティ**
- 認証・データ処理時
- SQL injection、XSS、CSRF、平文パスワード

**③パフォーマンス**
- DB操作・大量データ処理時
- N+1問題、インデックス欠如、メモリリーク

**④テスト**
- テストコード作成後
- テストカバレッジ、境界値、モック不備

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

<!-- _class: three-column -->

# STEP5のまとめ

## 🎯 品質担保の核心

**TDDとAI活用の相乗効果:**
- AIが自己完結
- 人間の負担が劇的に軽減
- テスト→エラー検知→修正を自動化

## 🧪 4つのテスト戦略

**①ユニットテスト（TDD）**
- Given-When-Then形式
- Red-Green-Refactor

**②E2Eテスト**
- Playwright使用
- ユーザー視点の検証

**③ビジュアルリグレッション**
- スクリーンショット比較
- UI崩れ自動検出

**④MCP関連ツール**
- Context 7: 最新ドキュメント参照
- Serena: 高速検索
- Browser DevTools: エラー自動キャプチャ

## 🔍 AI自己レビュー4種類

**①一般レビュー**
- 実装直後（毎回必須）
- ロジックエラー・エッジケース

**②セキュリティ特化**
- OWASP Top 10チェック
- 脆弱性大幅削減

**③パフォーマンス特化**
- N+1問題・メモリリーク
- レスポンス大幅改善（N+1解消など）

**④テストカバレッジ**
- エッジケース・異常系
- テストカバレッジ向上

## 🔧 リファクタリング3つの観点

**①重複コード削除**
- コピペで生成された重複を削減
- 保守コスト削減

**②デザインパターン適用**
- if-else → Strategy
- オブジェクト生成 → Factory
- 拡張容易な構造に

**③ライブラリ活用**
- 車輪の再発明を避ける
- エッジケーステスト済み
- セキュリティパッチ自動適用

## 📚 Living Documentation

**なぜ必要か:**
- AIは忘れっぽい
- ドキュメント＝AIの外部メモリ
- 実装と同期（常に信頼できる）

**3種類のドキュメント:**

**①architecture.md**
- システム全体像
- 構成・ディレクトリ
- 設計判断の理由

**②README.md**
- セットアップ手順
- 使い方
- トラブルシューティング

**③CLAUDE.md**
- 成功したプロンプトパターン
- ハマった点と回避策
- 再現性の確保

## 📊 効果

✅ Trust but Verify自動化
✅ 技術的負債の早期解消
✅ AIの外部メモリとして機能
✅ 知見の蓄積

---

<!-- _class: layout-diagram-only -->

# STEP5 チェックリスト

![STEP5チェックリスト](diagrams/diagram_39_step5_checklist.svg)

**品質担保:**
- [ ] ユニットテストカバレッジ80%以上
- [ ] E2Eテスト（Playwright）実施
- [ ] ビジュアルリグレッションテスト実施
- [ ] AI一般レビュー実施
- [ ] AIセキュリティレビュー実施（OWASP Top 10）
- [ ] AIパフォーマンスレビュー実施（N+1チェック）
- [ ] AIテストカバレッジレビュー実施
- [ ] 全テスト通過確認

**リファクタリング＆ドキュメント:**
- [ ] 重複コード削除
- [ ] デザインパターン適用検討
- [ ] ライブラリ活用検討
- [ ] architecture.md 更新（システム全体像）
- [ ] README.md 更新（セットアップ・使い方）
- [ ] CLAUDE.md 更新（成功パターン・ハマった点）
- [ ] 頻繁にコミット実施

**完了:**
→ 1つの機能開発サイクル完了！

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
