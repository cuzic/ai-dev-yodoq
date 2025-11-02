# slidectl カスタムスラッシュコマンド

`$HOME/slidectl`を使用してスライドの品質を体系的に向上させるためのカスタムスラッシュコマンド集です。

## 概要

slidectlは、Playwright-based DOM解析と機械学習を組み合わせた高度なスライド品質測定・最適化ツールです。これらのスラッシュコマンドは、slidectlの主要機能をClaude Codeから簡単に使えるようにします。

## 利用可能なコマンド

### 1. `/improve-slides` - 包括的な品質向上 ⭐ おすすめ

**用途:** すべてのスライドを体系的に改善したい場合

**機能:**
- 初期品質測定
- コンテンツバジェット分析
- 最適化戦略の立案
- 自動修正の適用
- 結果の検証とレポート

**実行時間:** 約30-40分

**使い方:**
```
/improve-slides
```

対話的なウィザード形式で、段階的に品質を向上させます。

**期待される結果:**
- FAIL スライド: 10-15 → 2-5 (-70%以上)
- 平均品質スコア: 75-80 → 85-90 (+10ポイント以上)
- OK スライド: 80% → 90%以上

---

### 2. `/measure-quality` - 品質測定

**用途:** 現在のスライドの品質状態を詳しく知りたい場合

**機能:**
- Playwright による DOM 解析
- Viewport overflow 検出 (1280x720)
- Safe area 侵入チェック (1216x656)
- Text density 計算
- Whitespace ratio 分析
- 違反の重症度判定 (FAIL/WARN/OK)

**実行時間:** 約5-10分

**使い方:**
```
/measure-quality
```

**出力例:**
```
📊 品質測定結果
================

Total: 168 slides
  ❌ FAIL: 12 slides (7.1%)   - 緊急対応必要
  ⚠️  WARN: 23 slides (13.7%) - 軽微な問題
  ✅ OK: 133 slides (79.2%)   - 問題なし

最も問題のあるスライド Top 5:
1. Slide 41: 4 violations (FAIL)
   - viewport_overflow: 234px bottom
   - text_density_high: 78%
   - safe_area_intrusion: bottom edge
   - container_overflow: 180px

2. Slide 73: 3 violations (FAIL)
   ...

一般的な問題:
  - Viewport overflow: 15 slides
  - 高いtext density: 8 slides
  - Safe area侵入: 6 slides
```

---

### 3. `/check-budget` - コンテンツバジェット確認

**用途:** 各レイアウトの最適な文字数・行数を知りたい場合

**機能:**
- レイアウト別の最大行数計算
- フォントサイズ別の文字数上限
- 現在のコンテンツとバジェットの比較
- バジェット超過スライドの特定
- 最適化提案 (compact適用、コンテンツ削減など)

**実行時間:** 約2-3分

**使い方:**
```
/check-budget
```

**出力例:**
```
📏 コンテンツバジェット
======================

Layout別バジェット:
┌──────────────────────┬────────┬─────────┬────────────┬──────────────┐
│ Layout               │ Font   │ Max行数 │ 文字/行    │ 総文字数     │
├──────────────────────┼────────┼─────────┼────────────┼──────────────┤
│ lead                 │ normal │ 8       │ 40         │ 320          │
│ lead                 │ compact│ 10      │ 45         │ 450          │
│ two-column           │ normal │ 15      │ 35         │ 525          │
│ two-column           │ compact│ 18      │ 40         │ 720          │
│ card-grid            │ normal │ 12      │ 38         │ 456          │
│ layout-horizontal-left│ normal│ 10      │ 30         │ 300          │
└──────────────────────┴────────┴─────────┴────────────┴──────────────┘

バジェット超過スライド: 23 (13.7%)
  Slide 41: 176% over (two-column normal)
    → 推奨: supercompact適用 + 20%削減
  Slide 73: 142% over (two-column normal)
    → 推奨: compact適用
```

---

### 4. `/optimize-slides` - 自動最適化

**用途:** 測定結果に基づいて自動的に最適化したい場合

**機能:**
- 品質スコアベースの反復最適化
- Compact class の自動適用提案
- コンテンツ削減ターゲット計算
- レイアウト変更提案
- 最適化効果の予測

**実行時間:** 約15-20分（3反復）

**使い方:**
```
/optimize-slides
```

**パラメータ:**
- `--target-score 85`: 目標品質スコア（デフォルト: 85）
- `--max-iterations 3`: 最大反復回数（デフォルト: 3）
- `--auto-apply`: 自動適用（要注意）

**最適化戦略:**
1. FAIL スライドを優先的に修正
2. Compact class 適用（情報損失なし）
3. Content reduction（必要最小限）
4. Layout 変更（要検証）

**出力例:**
```
🔧 最適化結果
=============

初期状態:
  FAIL: 12 slides (7.1%)
  平均スコア: 76.3/100

3回の反復後:
  FAIL: 2 slides (1.2%)    ↓ -83%
  平均スコア: 89.7/100     ↑ +13.4

適用した修正:
  ✅ Compact適用: 15 slides
  ✅ Supercompact適用: 5 slides
  ✅ コンテンツ削減: 8 slides
  ✅ レイアウト変更: 3 slides

目標達成: ✅ YES (目標: 85, 達成: 89.7)
```

## コマンド選択ガイド

### 初めて品質改善する場合
→ `/improve-slides` を使用
- 包括的なワークフロー
- 対話的なガイダンス
- 段階的な修正

### 現状を把握したい場合
→ `/measure-quality` を使用
- 詳細な問題分析
- 次のアクションの判断材料

### レイアウト設計時
→ `/check-budget` を使用
- 各レイアウトの容量を確認
- 適切なレイアウト選択

### 迅速な自動修正が必要な場合
→ `/optimize-slides` を使用
- 機械的な最適化
- 時間効率重視

## 典型的なワークフロー

### ワークフロー 1: 初回品質改善

```bash
# 1. 現状把握
/measure-quality

# 2. バジェット確認
/check-budget

# 3. 包括的改善
/improve-slides
```

### ワークフロー 2: 定期的なメンテナンス

```bash
# 1. 品質測定
/measure-quality

# 2. 問題があれば最適化
/optimize-slides --target-score 85

# 3. 結果確認
/measure-quality
```

### ワークフロー 3: 特定スライドの修正

```bash
# 1. 全体の品質測定
/measure-quality

# 2. 特定スライドを手動修正
/fix-overflow 41

# 3. 結果確認
/measure-quality
```

## 品質基準

### 優秀 (Excellent): 90-100点
- FAIL: 0%
- WARN: <5%
- OK: >95%
- すべてのスライドが適切に表示

### 良好 (Good): 80-89点
- FAIL: <2%
- WARN: <10%
- OK: >88%
- ほとんど問題なし

### 許容範囲 (Acceptable): 70-79点
- FAIL: <5%
- WARN: <20%
- OK: >75%
- 軽微な問題あり

### 要改善 (Needs Improvement): <70点
- FAIL: >5%
- WARN: >20%
- 品質改善が必要

## slidectl の主要機能

### 高度な品質測定

1. **Viewport Overflow Detection**
   - 1280x720 の境界を超えるコンテンツを検出
   - ピクセル単位の正確な測定

2. **Safe Area Check**
   - 1216x656 (margin 32px) の安全領域チェック
   - エッジに近すぎるコンテンツを警告

3. **Text Density Analysis**
   - テキストが占める面積の割合を計算
   - 高密度 (>70%) と低密度 (<20%) を検出

4. **Whitespace Analysis**
   - 余白の割合を計算
   - 過剰な余白 (>60%) を検出

5. **Container Overflow**
   - 親コンテナをはみ出すコンテンツを検出
   - Grid/Flex layout の問題を特定

### コンテンツバジェット計算

レイアウトとフォントサイズに基づいて、最適な文字数・行数を計算:

```python
budget = calculate_budget(layout="two-column", font_class="compact")
# {
#   "max_lines": 18,
#   "chars_per_line": 40,
#   "total_chars": 720,
#   "columns": 2,
#   "usable_width": 1094,
#   "usable_height": 612
# }
```

### 最適化エンジン

反復的な最適化ループ:

```
Measure → Score → Suggest → Apply → Re-measure
   ↑                                     ↓
   └─────────────────────────────────────┘
         (目標達成まで繰り返し)
```

## トラブルシューティング

### slidectl コマンドが見つからない

```bash
cd ~/slidectl
uv run slidectl --version
```

### ワークスペースが初期化されていない

```bash
cd ~/slidectl
uv run slidectl init --ws /home/cuzic/ai-dev-yodoq
```

### 測定が失敗する

```bash
# HTML ファイルが存在するか確認
ls -la /home/cuzic/ai-dev-yodoq/slides/index.html

# 存在しない場合は再ビルド
cd /home/cuzic/ai-dev-yodoq/slides
npx @marp-team/marp-cli all_slides.md --html --allow-local-files \
  --theme-set ../assets/themes/ai-seminar.css --theme ai-seminar \
  -o index.html
```

### Playwright のインストールエラー

```bash
cd ~/slidectl
mise run setup
```

## 参考資料

- slidectl README: `~/slidectl/README.md`
- slidectl ドキュメント: `~/slidectl/docs/`
- Marp 公式: https://marp.app/
- Playwright 公式: https://playwright.dev/

## コマンド作成日

2025-11-02

## 更新履歴

- 2025-11-02: 初版作成（4コマンド）
  - `/improve-slides`
  - `/measure-quality`
  - `/check-budget`
  - `/optimize-slides`
