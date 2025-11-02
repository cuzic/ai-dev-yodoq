# スライド再構成プラン V2 - スライド数維持版

## 📊 現状分析（再確認）

```
現在のスライド構成:
- day1_1.md.backup: 48 slides (AI基礎 + Claude Code + STEP1-2)
- day1_2.md.backup: 49 slides (STEP3-5)
- day1_3.md.backup: 33 slides (振り返り + 演習)
- day2_1.md.backup: 40 slides (リバースエンジニアリング + テスト)
- day2_2.md.backup: 47 slides (実践演習 + 総まとめ)

合計: 217 slides
```

---

## 🎯 改訂方針

### スライド数の扱い

**目標**: 217 slides → **200-210 slides** (削減率3-8%)

**方針**:
- ✅ 既存の `---` 区切りを最大限尊重
- ✅ スライドの統合は最小限（明らかな重複のみ）
- ✅ 各スライドに適切なレイアウトクラスを割り当て
- ✅ TODOコメントで `/slide-tdd` による改善箇所を明確化
- ✅ 内容の質的向上に注力

### レイアウト最適化戦略

既存のスライドに対して、**内容に基づいて最適なレイアウトクラスを割り当てる**：

1. **lead**: セクション区切り（H1のみ、短い説明）
2. **layout-diagram-only**: 図表メインのスライド
3. **two-column**: 比較・並列説明、複数の独立した内容
4. **layout-horizontal-left**: 図表（左）+ 説明（右）
5. **layout-horizontal-right**: 説明（左）+ 図表（右）
6. **compact**: 箇条書き9項目以上
7. **three-column**: チェックリスト、3項目の比較
8. **default**: 標準（3-8項目の箇条書き）

---

## 📋 新しいスライド構成案（スライド数維持版）

### Day 1-1: AI基礎 + Claude Code + STEP1-2 (10:00-12:00)

**目標スライド数**: 46-48枚 (現在: 48枚)

#### 詳細構成

1. **イントロダクション** (3 slides)
   - #1: タイトル ← `lead`
   - #2: 本日の目標 ← `two-column`
   - #3: 2日間の全体像 ← `layout-horizontal-left` (新規SVG)

2. **AI活用の基本原則** (6 slides)
   - #4: AI活用の3原則 ← `layout-horizontal-left`
   - #5: Vibe Coding vs Production ← `layout-horizontal-left`
   - #6: 開発者の役割変化 ← `layout-horizontal-left`
   - #7: 5-STEPフロー全体像 ← `layout-horizontal-left`
   - #8: AIの制約①忘れっぽい ← `layout-horizontal-right`
   - #9: AIの制約②Reward Hacking ← `layout-diagram-only`

3. **環境準備** (2 slides)
   - #10: 環境準備 ← `two-column`
   - #11: セキュリティベストプラクティス ← `layout-diagram-only`

4. **Claude Code 使い方** (8 slides)
   - #12: セクション区切り ← `lead`
   - #13: Claude Codeとは ← `default`
   - #14: セットアップ ← `layout-horizontal-right`
   - #15: 4つのモード比較 ← `layout-horizontal-left`
   - #16: モード詳細と使い分け ← `two-column`
   - #17: よくある問題①ファイルが多すぎる ← `two-column`
   - #18: よくある問題②③ ← `two-column`
   - #19: 効率的な指示の出し方 ← `layout-horizontal-right`

5. **STEP1: 要件定義** (14 slides)
   - #20: セクション区切り ← `lead`
   - #21: STEP1とは ← `default`
   - #22: AIに質問させる手法 ← `two-column`
   - #23: 要件の引き出し方（文字起こし） ← `layout-horizontal-left`
   - #24: MoSCoW優先順位付け ← `layout-horizontal-left`
   - #25: MoSCoW実践例 ← `layout-diagram-only`
   - #26: ユーザーストーリーマッピング ← `layout-horizontal-right`
   - #27: 非機能要件 ← `layout-horizontal-left`
   - #28: エラー・エッジケース・制約 ← `layout-diagram-only`
   - #29: 受け入れ基準（Given-When-Then） ← `default`
   - #30: Vibe Codingプロトタイプ ← `default`
   - #31: STEP1のまとめ ← `two-column`
   - #32: STEP1チェックリスト ← `layout-diagram-only`
   - #33: セクション区切り ← `lead`

6. **STEP2: 設計ドキュメント** (13 slides)
   - #34: STEP2とは ← `default`
   - #35: 設計ドキュメントの構造 ← `layout-horizontal-right`
   - #36: Tech Stack Setup ← `default`
   - #37: データベーススキーマ設計 ← `layout-horizontal-left`
   - #38: API仕様の明確化 ← `default`
   - #39: Mermaid vs SVG ← `layout-horizontal-right`
   - #40: ER図が開発をスムーズにする ← `layout-horizontal-left`
   - #41: シーケンス図がAI実装を助ける ← `layout-horizontal-right`
   - #42: 受け入れ条件の詳細化 ← `default`
   - #43: STEP2のまとめ ← `layout-diagram-only`
   - #44: STEP2チェックリスト ← `layout-diagram-only`
   - #45: Part 1振り返りチェックリスト ← `two-column`
   - #46: 休憩案内 ← `default`

**合計**: 46 slides (-2 from 48)

---

### Day 1-2: STEP3-5 (13:00-15:00)

**目標スライド数**: 48-49枚 (現在: 49枚)

#### 詳細構成

1. **セクション区切り** (2 slides)
   - #1: タイトル ← `default`
   - #2: STEP3セクション区切り ← `lead`

2. **STEP3: タスク分解** (13 slides)
   - #3: STEP3タスク分解とは ← `two-column`
   - #4: タスク分解 = AIの思考を言語化 ← `two-column`
   - #5: 計画書作成による可視化 ← `default`
   - #6: Phase分け戦略 ← `layout-horizontal-left`
   - #7: タスク粒度（30分〜2時間） ← `two-column`
   - #8: 依存関係の可視化 ← `layout-horizontal-right`
   - #9: タスク一覧テンプレート ← `layout-horizontal-left`
   - #10: AI活用でタスク自動生成 ← `default`
   - #11: STEP3のまとめ ← `two-column`
   - #12: STEP3チェックリスト ← `layout-diagram-only`
   - #13: セクション区切り ← `lead`

3. **STEP4: 実装** (16 slides)
   - #14: 実装の3原則 ← `two-column`
   - #15: 実装の標準ワークフロー ← `two-column`
   - #16: TDD/BDD統合ワークフロー ← `layout-horizontal-right`
   - #17: AIにTDD/BDDで実装させる ← `layout-horizontal-left`
   - #18: セキュリティベストプラクティス ← `layout-horizontal-right`
   - #19: パスワード・JWT認証 ← `two-column`
   - #20: セキュアなコードの指示方法 ← `default`
   - #21: インクリメンタル開発とは ← `layout-horizontal-left`
   - #22: インクリメンタル実装の実例 ← `default`
   - #23: AI自己レビュー必須化 ← `layout-horizontal-right`
   - #24: STEP4のまとめ ← `two-column`
   - #25: STEP4チェックリスト ← `layout-diagram-only`
   - #26: セクション区切り ← `lead`

4. **STEP5: 品質担保＆ドキュメント** (18 slides)
   - #27: STEP5とは ← `default`
   - #28: TDDとAI活用の相乗効果 ← `default`
   - #29: E2Eテスト重視の戦略 ← `default`
   - #30: Playwrightによるテスト ← `default`
   - #31: ビジュアルリグレッションテスト ← `default`
   - #32: MCP関連ツール ← `default`
   - #33: AI自己レビュー4種類 ← `two-column`
   - #34: AI自己レビュー①一般 ← `default`
   - #35: AI自己レビュー②セキュリティ ← `default`
   - #36: AI自己レビュー③パフォーマンス ← `default`
   - #37: AI自己レビュー④テストカバレッジ ← `layout-horizontal-left`
   - #38: 自己レビューの実例 ← `default`
   - #39: STEP5のまとめ ← `three-column`
   - #40: STEP5チェックリスト ← `layout-diagram-only`
   - #41: リファクタリング ← `default`
   - #42: Living Documentation ← `default`
   - #43: 頻繁なコミット ← `default`
   - #44: セクション区切り ← `lead`

5. **Part 2全体のまとめ** (3 slides)
   - #45: Part 2まとめ ← `lead`
   - #46: Part 2キーポイント ← `card-grid`
   - #47: 休憩案内 ← `default`

**合計**: 47 slides (-2 from 49)

---

### Day 1-3: 振り返り + 演習 (15:00-17:00)

**目標スライド数**: 32-33枚 (現在: 33枚)

#### 詳細構成

1. **セクション区切り** (1 slide)
   - #1: タイトル ← `default`

2. **1日目の振り返り** (7 slides)
   - #2: 1日目の振り返り ← `two-column`
   - #3: よくある失敗①いきなりコード ← `default`
   - #4: よくある失敗②AI自己レビュースキップ ← `default`
   - #5: よくある失敗③リファクタリング後回し ← `default`
   - #6: 1日目のキーメッセージ ← `layout-diagram-only`
   - #7: セクション区切り ← `lead`

3. **演習課題** (24 slides)
   - #8: 演習課題の説明（TODOアプリ） ← `default`
   - #9: 演習の目的と課題 ← `two-column`
   - #10-#28: 演習の詳細、つまずきポイント、チェックリスト等
   - #29: 演習成功のチェックリスト① ← `two-column`
   - #30: 演習成功のチェックリスト② ← `two-column`
   - #31: 時間配分 ← `default`
   - #32: 質疑応答 ← `default`

**合計**: 32 slides (-1 from 33)

---

### Day 2-1: リバースエンジニアリング + テスト (10:00-12:00)

**目標スライド数**: 38-40枚 (現在: 40枚)

#### 詳細構成

1. **セクション区切り** (1 slide)
   - #1: タイトル ← `default`

2. **振り返り** (2 slides)
   - #2: Day 1振り返り ← `two-column`
   - #3: Day 2目標 ← `default`

3. **リバースエンジニアリング** (20 slides)
   - #4: セクション区切り ← `lead`
   - #5: リバースエンジニアリングとは ← `layout-horizontal-left`
   - #6-#22: 手順、実例、各ステップの詳細
   - #23: リバースエンジニアリングまとめ ← `two-column`

4. **テストシナリオ作成** (15 slides)
   - #24: テストシナリオ作成の実例 ← `layout-horizontal-left`
   - #25-#37: テストコード基礎、Given-When-Then実践等
   - #38: テストシナリオからテストコードへ ← `default`

5. **休憩** (1 slide)
   - #39: 休憩案内 ← `default`

**合計**: 39 slides (-1 from 40)

---

### Day 2-2: 実践演習 + 総まとめ (13:00-17:00)

**目標スライド数**: 45-47枚 (現在: 47枚)

#### 詳細構成

1. **セクション区切り** (1 slide)
   - #1: タイトル ← `default`

2. **実践演習** (20 slides)
   - #2: 演習の目的 ← `default`
   - #3: 3つの演習課題から選択 ← `layout-horizontal-left`
   - #4-#19: 各課題の詳細、進め方、チェックリスト等
   - #20: 演習開始 ← `default`

3. **成果発表** (6 slides)
   - #21-#26: 発表準備、テンプレート、共有ポイント等

4. **2日間の総まとめ** (19 slides)
   - #27: セクション区切り ← `lead`
   - #28: 2日間の総まとめ ← `three-column`
   - #29-#44: 学びの振り返り、よくある質問、追加リソース等
   - #45: 最終メッセージ ← `lead`
   - #46: アンケート ← `default`

**合計**: 46 slides (-1 from 47)

---

## 📊 改訂効果まとめ

### スライド数の変更

```
Before: 217 slides
After:  208 slides
削減率: 4% (9 slides削減のみ)

内訳:
- day1_1.md: 46 slides (-2)
- day1_2.md: 47 slides (-2)
- day1_3.md: 32 slides (-1)
- day2_1.md: 39 slides (-1)
- day2_2.md: 46 slides (-1)
```

### 改善の焦点

**スライド数はほぼ維持** → 既存の構成を尊重

**レイアウト最適化に注力**:
- 各スライドに最適なレイアウトクラスを割り当て
- 視認性・読みやすさの向上
- 図表とテキストのバランス最適化

**TODOコメント追加**:
- `/slide-tdd` で詳細化する箇所を明確化
- SVG作成が必要な箇所を明示
- 内容充実が必要な箇所を指摘

### レイアウト分布（概算）

- **lead**: 8-10% (セクション区切り)
- **layout-horizontal-left/right**: 35-40% (図表 + 説明)
- **layout-diagram-only**: 10-15% (図表メイン)
- **two-column**: 20-25% (比較・並列説明)
- **three-column**: 2-3% (3項目比較)
- **compact**: 5-8% (箇条書き多数)
- **default**: 20-25% (標準)

---

## 🎯 次のステップ

1. **この構成案をレビュー** - スライド数とレイアウト配分が適切か確認
2. **各ファイルの骨組みを生成**:
   - 既存の `---` 区切りを維持
   - 各スライドに適切なレイアウトクラスを設定
   - TODOコメントで改善箇所を明示
3. **SVGプレースホルダーの整理**:
   - 既存SVGを活用
   - 新規SVGが必要な箇所を明確化
4. **各スライドを `/slide-tdd` で詳細化**

---

## 💡 改善ポイント

✅ **スライド数をほぼ維持** (217 → 208枚、4%削減のみ)
✅ **既存構成を尊重** → 大幅な変更なし
✅ **レイアウト最適化** → 視認性向上、情報伝達効率化
✅ **TODOコメント明確化** → `/slide-tdd` での改善作業を明示
✅ **段階的改善** → 一度に全てを変えず、徐々に品質向上

---

**作成日**: 2025-11-02
**作成者**: Claude Code + /generate-slides 分析（改訂版）
**方針**: スライド数維持、レイアウト最適化に注力
