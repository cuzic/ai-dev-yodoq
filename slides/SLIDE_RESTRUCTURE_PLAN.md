# スライド再構成プラン

## 📊 現状分析

```
現在のスライド構成:
- day1_1.md.backup: 48 slides (AI基礎 + Claude Code + STEP1-2)
- day1_2.md.backup: 49 slides (STEP3-5)
- day1_3.md.backup: 33 slides (振り返り + 演習)
- day2_1.md.backup: 40 slides (リバースエンジニアリング + テスト)
- day2_2.md.backup: 47 slides (実践演習 + 総まとめ)

合計: 217 slides
```

### 問題点

1. **スライド数が多すぎる** (217枚)
   - 1日目だけで130枚
   - 集中力が続かない
   - 時間内に終わらない可能性

2. **冗長性がある**
   - 各セクションに「まとめ」「チェックリスト」
   - 重複する内容説明
   - 同じ概念の繰り返し

3. **レイアウト最適化の余地**
   - two-columnで詰め込める内容が単一スライドに
   - compactレイアウト未活用
   - テキストのみスライドが散在

---

## 🎯 改善方針

### 1. スライド総数の削減

**目標**: 217 slides → **120-140 slides** (40%削減)

**手法**:
- two-column レイアウト活用 (2枚 → 1枚)
- compact レイアウト活用 (箇条書き多数を1枚に)
- 冗長な「まとめ」スライドの統合

### 2. ファイル構成の最適化

**現在**: 5ファイル
**提案**: 4ファイル

```
day1_morning.md  (午前: 基礎 + STEP1-2)     → 35-40 slides
day1_afternoon.md (午後: STEP3-5 + 演習)    → 35-40 slides
day2_morning.md  (午前: リバース + テスト)  → 25-30 slides
day2_afternoon.md (午後: 実践 + まとめ)     → 25-30 slides

合計: 120-140 slides
```

### 3. レイアウト戦略

#### Phase 1-4: INPUT → ANALYZE → SPLIT → LAYOUT

**自動レイアウト選択ロジック適用**:

1. **lead**: セクション区切り (H1のみ、短い説明)
2. **layout-diagram-only**: 図表メイン
3. **two-column**: 比較・並列説明 (40-50%のスライドに適用)
4. **layout-horizontal-left**: 図表 + 説明 (3-8項目)
5. **compact**: 箇条書き9項目以上
6. **default**: 標準 (3-8項目)

---

## 📋 新しいスライド構成案

### Day 1 午前 (10:00-12:00) - `day1_morning.md`

**目標スライド数**: 35-40枚 (現在: 48枚)

#### セクション構成

1. **イントロダクション** (3 slides) ← lead
   - タイトル
   - 本日の目標 ← two-column
   - 2日間の全体像 ← layout-horizontal-left

2. **AI活用の基本原則** (6 slides)
   - AI活用の3原則 ← layout-horizontal-left
   - Jagged Intelligence詳細 ← layout-horizontal-left
   - Reward Hacking問題と対策 ← layout-diagram-only
   - Trust but Verify ← layout-horizontal-left
   - Vibe Coding vs Production ← layout-horizontal-left
   - 開発者の役割変化 ← layout-horizontal-left

3. **環境準備** (2 slides) ← two-column で統合
   - 必須ツール + 推奨ツール + チェックリスト

4. **Claude Code 使い方** (5 slides)
   - Claude Codeとは ← default
   - セットアップ + .claudeignore ← layout-horizontal-right
   - 4つのモード比較 ← layout-horizontal-left
   - よくある問題と対処法 ← two-column (3問題を1枚に)
   - 効率的な指示の出し方 ← layout-horizontal-right

5. **STEP1: 要件定義** (11 slides)
   - STEP1とは ← default
   - AIに質問させる手法 ← two-column
   - 文字起こしアプローチ ← layout-horizontal-left
   - MoSCoW優先順位 ← layout-horizontal-left
   - MoSCoW実践例 ← layout-diagram-only
   - ユーザーストーリーマッピング ← layout-horizontal-right
   - 非機能要件 ← layout-horizontal-left
   - エラー・エッジケース洗い出し ← layout-diagram-only
   - 受け入れ基準 (Given-When-Then) ← default
   - Vibe Codingプロトタイプ ← default
   - STEP1まとめ + チェックリスト ← two-column

6. **STEP2: 設計ドキュメント** (10 slides)
   - STEP2とは ← default
   - 設計ドキュメント7要素 ← layout-horizontal-right
   - Tech Stack Setup ← default
   - データベーススキーマ設計 ← layout-horizontal-left
   - ER図の重要性 ← layout-horizontal-left
   - API仕様の明確化 ← default
   - Mermaid vs SVG ← layout-horizontal-right
   - シーケンス図 ← layout-horizontal-right
   - 受け入れ条件の詳細化 ← default
   - STEP2まとめ + チェックリスト ← two-column

**合計**: 37 slides (-11 from 48)

---

### Day 1 午後 (13:00-17:00) - `day1_afternoon.md`

**目標スライド数**: 38-42枚 (現在: 82枚 from day1_2 + day1_3)

#### セクション構成

1. **STEP3: タスク分解** (8 slides)
   - STEP3とは ← two-column
   - タスク分解 = AIの思考を言語化 ← two-column
   - Phase分け戦略 ← layout-horizontal-left
   - タスク粒度 (30分〜2時間) ← two-column
   - 依存関係の可視化 ← layout-horizontal-right
   - タスク一覧テンプレート ← layout-horizontal-left
   - AI活用でタスク自動生成 ← default
   - STEP3まとめ + チェックリスト ← two-column

2. **STEP4: 実装** (10 slides)
   - 実装の3原則 ← two-column
   - 実装の標準ワークフロー ← two-column
   - TDD/BDD統合ワークフロー ← layout-horizontal-right
   - AIにTDD/BDDで実装させる ← layout-horizontal-left
   - Given-When-Then構造 ← layout-horizontal-left
   - セキュリティベストプラクティス ← layout-horizontal-right
   - パスワード・JWT認証 ← two-column
   - インクリメンタル開発 ← layout-horizontal-left
   - AI自己レビュー必須化 ← layout-horizontal-right
   - STEP4まとめ + チェックリスト ← two-column

3. **STEP5: 品質担保＆ドキュメント** (9 slides)
   - STEP5とは ← default
   - TDDとAI活用の相乗効果 ← default
   - E2Eテスト重視 + Playwright ← two-column
   - ビジュアルリグレッション + MCP ← two-column
   - AI自己レビュー4種類 ← two-column compact
   - セキュリティ特化レビュー ← default
   - パフォーマンス特化 + テストカバレッジ ← two-column
   - リファクタリング3観点 + Living Documentation ← two-column compact
   - STEP5まとめ + チェックリスト ← two-column

4. **1日目振り返り** (4 slides)
   - 振り返り + よくある失敗 ← two-column compact
   - 5-STEPフロー全体の流れ ← layout-diagram-only
   - キーメッセージ ← layout-diagram-only
   - Part 1 チェックリスト ← two-column

5. **演習課題** (7 slides)
   - 演習の目的と課題 ← two-column
   - TODOアプリ要件 ← default
   - 演習の進め方 ← default
   - つまずきポイントと対処法 ← two-column compact
   - 成功のチェックリスト ← two-column compact
   - 時間配分 ← default
   - 質疑応答 ← default

**合計**: 38 slides (-44 from 82)

---

### Day 2 午前 (10:00-12:00) - `day2_morning.md`

**目標スライド数**: 28-32枚 (現在: 40枚)

#### セクション構成

1. **振り返り** (2 slides) ← two-column
   - Day 1 振り返り
   - Day 2 目標

2. **リバースエンジニアリング** (12 slides)
   - リバースエンジニアリングとは ← layout-horizontal-left
   - なぜリバースエンジニアリングが重要か ← two-column
   - リバースエンジニアリングの手順 ← layout-horizontal-left
   - コードベース把握 ← layout-horizontal-right
   - テストシナリオ洗い出し ← layout-horizontal-left
   - 優先順位付け (MoSCoW) ← layout-horizontal-left
   - テスト作成 (TDD) ← layout-horizontal-left
   - リグレッション防止 ← layout-horizontal-left
   - リファクタリング安全化 ← layout-horizontal-right
   - 影響分析 ← layout-horizontal-left
   - リバースエンジニアリング実例 ← layout-diagram-only
   - まとめ ← two-column

3. **テストシナリオ作成** (8 slides)
   - テストシナリオとは ← default
   - テストシナリオ作成の実例 ← layout-horizontal-left
   - ユーザーストーリーからシナリオへ ← layout-horizontal-left
   - エッジケース洗い出し ← layout-horizontal-left
   - テストコード基礎 (復習) ← two-column
   - Given-When-Then実践 ← layout-horizontal-left
   - テストシナリオからコードへ ← layout-horizontal-left
   - まとめ ← two-column

4. **休憩時間配分** (1 slide) ← default

**合計**: 23 slides (-17 from 40)

---

### Day 2 午後 (13:00-17:00) - `day2_afternoon.md`

**目標スライド数**: 30-34枚 (現在: 47枚)

#### セクション構成

1. **実践演習** (8 slides)
   - 演習の目的 ← default
   - 3つの演習課題 ← layout-horizontal-left
   - 課題①: リバースエンジニアリング ← default
   - 課題②: 既存機能拡張 ← default
   - 課題③: 新機能追加 ← default
   - 演習の進め方 ← two-column
   - つまずきポイントと対処法 ← two-column compact
   - 成功のチェックリスト ← two-column

2. **成果発表** (4 slides)
   - 発表の流れ ← default
   - 発表テンプレート ← default
   - 共有ポイント ← two-column
   - フィードバック ← default

3. **2日間の総まとめ** (12 slides)
   - 2日間の学び全体像 ← layout-diagram-only
   - Day 1の振り返り ← two-column compact
   - Day 2の振り返り ← two-column compact
   - 5-STEPフロー再確認 ← layout-diagram-only
   - AI活用の3原則再確認 ← layout-horizontal-left
   - Trust but Verify実践 ← layout-horizontal-left
   - Guardrails構築 ← layout-horizontal-left
   - 明日からの実践 ← two-column compact
   - よくある質問 ← two-column compact
   - 追加リソース ← two-column
   - 最終メッセージ ← lead
   - アンケート ← default

**合計**: 24 slides (-23 from 47)

---

## 📊 改善効果まとめ

### スライド数削減

```
Before: 217 slides
After:  122 slides
削減率: 44% (95 slides削減)

内訳:
- day1_morning.md:   37 slides (-11)
- day1_afternoon.md: 38 slides (-44)
- day2_morning.md:   23 slides (-17)
- day2_afternoon.md: 24 slides (-23)
```

### レイアウト活用

- **two-column**: 30-40% (並列比較、まとめ、FAQ等)
- **compact**: 10-15% (箇条書き多数)
- **layout-horizontal-left/right**: 30-35% (図表 + 説明)
- **layout-diagram-only**: 5-10% (図表メイン)
- **lead**: 2-3% (セクション区切り)
- **default**: 15-20% (標準)

### 改善ポイント

✅ スライド数44%削減 → 集中力維持
✅ 冗長性排除 → 情報密度向上
✅ レイアウト最適化 → 視認性向上
✅ ファイル構成明確化 → 管理しやすい
✅ 時間配分に余裕 → 質疑応答時間確保

---

## 🎯 次のステップ

1. この構成案をレビュー・調整
2. `/generate-slides` 的なアプローチで骨組み生成
3. 各スライドを `/slide-tdd` で詳細化
4. 全体の整合性チェック
5. 最終レビュー

---

**作成日**: 2025-11-02
**作成者**: Claude Code + /generate-slides 分析
