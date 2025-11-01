# Slide REFACTOR - Phase 4: 品質向上

slidectl の測定機能を使ってスライドの品質をさらに向上させます。

## 実行タスク

### 1. 詳細な品質測定

#### SVG境界の精密測定

```bash
python3 validate_svg_bounds.py
```

該当するSVGのオーバーフロー状況を確認：
- max_overflow_x: X軸方向のオーバーフロー
- max_overflow_y: Y軸方向のオーバーフロー
- 推奨ViewBoxサイズ

#### 判定スクリプトでの現状確認

```bash
python3 validate_slide_[番号].py
```

現在のメトリクスを記録：
- SVG overflow
- Text density
- Bullet count
- その他の警告

### 2. 改善方針の決定

メトリクスに基づいて改善方針を決定：

#### Case 1: SVGオーバーフロー > 10px

**問題**: SVGがViewBoxからはみ出している

**解決策**:
1. ViewBoxを拡大
   ```svg
   <!-- Before -->
   <svg viewBox="0 0 1400 800">

   <!-- After -->
   <svg viewBox="0 0 1600 900">
   ```

2. 長いテキストを複数行に分割
   ```svg
   <!-- Before -->
   <text>このテキストは非常に長くてViewBoxからはみ出してしまいます</text>

   <!-- After -->
   <text y="100">このテキストは非常に長くて</text>
   <text y="140">ViewBoxからはみ出してしまいます</text>
   ```

3. フォントサイズを縮小
   ```svg
   <!-- Before -->
   <text font-size="56px">

   <!-- After -->
   <text font-size="48px">
   ```

#### Case 2: テキスト密度 > 80%

**問題**: スライドに文字が詰め込まれすぎ

**解決策**:
1. レイアウトを `compact` に変更
   ```markdown
   <!-- _class: compact -->
   ```

2. 箇条書き項目を削減
   - 冗長な項目を統合
   - 最重要項目のみ残す
   - 詳細は別スライドに分割

3. フォントサイズを縮小（慎重に）
   - 読みやすさとのバランスを考慮

#### Case 3: 箇条書き項目数 > 8

**問題**: 項目が多すぎて読みにくい

**解決策**:
1. レイアウトを `compact` に変更
2. 項目を2つのスライドに分割
3. `two-column` レイアウトで横に並べる

#### Case 4: 余白が少ない

**問題**: スライドが窮屈に見える

**解決策**:
1. 箇条書き項目を削減
2. SVGのサイズを縮小（width指定を調整）
3. レイアウトを変更

### 3. 改善の実施

決定した改善方針に基づいて修正を実施：

#### 3.1 SVG図表の調整

```bash
# SVGファイルを編集
# - ViewBox拡大
# - テキスト分割
# - フォントサイズ調整
```

#### 3.2 スライドマークダウンの調整

```bash
# all_slides.md を編集
# - レイアウトクラス変更
# - 箇条書き項目調整
# - width指定変更
```

### 4. 継続的な測定とフィードバック

各変更後に判定処理を実行し、改善を確認：

```bash
# 1回目の改善
python3 validate_slide_[番号].py

# 2回目の改善（必要な場合）
python3 validate_slide_[番号].py

# 3回目の改善（必要な場合）
python3 validate_slide_[番号].py
```

**改善ループの例**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 REFACTORING ITERATION #1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Before:
  - SVG overflow: 45px
  - Text density: 320 chars
  - Bullet count: 7
  - Warnings: 1

🔨 Applied Changes:
  1. Expanded ViewBox: 1400x800 → 1600x900
  2. Split long title into 2 lines
  3. Reduced font size: 56px → 48px

📊 After:
  - SVG overflow: 8px ✅
  - Text density: 320 chars ✅
  - Bullet count: 7 ✅
  - Warnings: 0 ✅

✅ Improvement: SVG overflow 45px → 8px
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5. スコアリング（オプション）

slidectl の品質測定機能を使用（利用可能な場合）：

```bash
cd $HOME/slidectl
uv run slidectl measure --slide [番号] --html /home/cuzic/ai-dev-yodoq/slides/index.html
```

総合スコアを確認し、目標（85/100以上）を達成。

### 6. 視覚的確認

ブラウザで `index.html` を開いて視覚的に確認：

```bash
# index.html を再生成
npx @marp-team/marp-cli all_slides.md -o index.html --html

# ブラウザで開いて確認
# - 文字の読みやすさ
# - SVG図表のバランス
# - 全体の見た目
```

### 7. TodoList更新

品質向上タスクを完了としてマーク。

## 確認ポイント

- ✅ 品質メトリクスが改善されたか
- ✅ すべての警告が解消されたか（または許容範囲内か）
- ✅ 視覚的なバランスが良いか
- ✅ 判定処理が引き続きパスしているか

## 改善目標

以下を目指します：

- **SVG overflow**: < 10px（理想は < 5px）
- **Text density**: < 80%（理想は 50-70%）
- **Bullet count**: 3-8項目
- **Total score**: 85/100以上（slidectl使用時）

## 次のフェーズへ

ユーザーの確認を得てから、次のフェーズ（VERIFY）へ進む。

VERIFYフェーズでは、前後のコンテキストと受入条件を踏まえて最終確認を行います。
