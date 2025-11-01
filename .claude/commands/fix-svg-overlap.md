# SVG重なり修正

既存のSVGファイルのテキスト重なり問題を修正します。

## 修正手順

### Step 1: 問題診断

以下のコマンドで問題のあるSVGを特定：

```bash
cd slides
python3 evaluate_slide_quality.py | grep -A 5 "SVG Overlap"
```

または個別SVG分析：
```bash
python3 analyze_svg_horizontal_overlap.py
```

### Step 2: SVG読み込み

対象SVGファイルを読み込んで現状を把握：

```bash
# 例: diagram_03_5step_flow.svg
```

以下を確認：
1. viewBox サイズ
2. テキスト要素の数
3. フォントサイズ分布
4. 現在のy座標配置

### Step 3: 問題タイプの特定

**垂直重なり (v)**
- 症状: y座標の差が font_size × 1.4 未満
- 修正: y座標を調整、間隔を広げる

**水平重なり (h)**
- 症状: 同じy座標でテキストが横に重なる
- 修正: x座標調整、改行、またはフォントサイズ縮小

**oversized**
- 症状: テキスト幅が viewBox幅の90%超
- 修正: 改行、フォントサイズ縮小、またはviewBox拡張

### Step 4: 修正戦略

#### 戦略A: y座標調整（垂直重なりのみ）
```python
# 最小間隔を確保してy座標を再計算
min_gap = max(current_font_size, next_font_size) * 1.4
new_y = current_y + min_gap

# viewBox高さが不足する場合は拡張
if max_y > viewBox_height * 0.8:
    new_viewBox_height = max_y * 1.25  # 25%余白
```

#### 戦略B: レイアウト再設計（水平重なり含む）
```
1. テキスト幅を再計算
2. カラム幅を再定義
3. 長すぎるテキストを改行またはフォントサイズ縮小
4. x座標とy座標の両方を再配置
```

#### 戦略C: コンテンツ削減（oversized多数）
```
1. 重要度の低いテキストを削除
2. 冗長な説明を短縮
3. 箇条書きを簡潔化
```

### Step 5: 修正実装

修正する際の優先順位：

**優先度1: 構造変更なし（座標調整のみ）**
- y座標を増加させて垂直間隔を確保
- viewBox高さを拡張
- 最も簡単で安全

**優先度2: フォントサイズ調整**
- 大きすぎるフォントを縮小
- 階層を維持しながら全体的にスケールダウン

**優先度3: 改行追加**
- 長いテキストを複数行に分割
- `<text>` を `<text>` + `<tspan>` に変更

**優先度4: レイアウト再設計**
- カラム数変更
- 要素の配置順序変更
- 最も時間がかかるが最良の結果

### Step 6: 修正例

#### 例1: 垂直重なり修正
```xml
<!-- 修正前 -->
<text x="100" y="200" font-size="48px">項目1</text>
<text x="100" y="230" font-size="48px">項目2</text>  <!-- 間隔30px = NG -->

<!-- 修正後 -->
<text x="100" y="200" font-size="48px">項目1</text>
<text x="100" y="267" font-size="48px">項目2</text>  <!-- 間隔67px (48×1.4) = OK -->
```

#### 例2: 水平重なり修正
```xml
<!-- 修正前 -->
<text x="100" y="200" font-size="64px">長いテキストAAAAA</text>  <!-- 推定幅: 640px -->
<text x="400" y="200" font-size="48px">次のテキスト</text>      <!-- 重なる! -->

<!-- 修正後 (改行) -->
<text x="100" y="200" font-size="48px">長いテキスト</text>      <!-- フォント縮小 + 改行 -->
<text x="100" y="267" font-size="48px">AAAAA</text>
<text x="400" y="200" font-size="48px">次のテキスト</text>
```

#### 例3: viewBox拡張
```xml
<!-- 修正前 -->
<svg viewBox="0 0 1200 800">
  <!-- コンテンツが800pxを超える -->
</svg>

<!-- 修正後 -->
<svg viewBox="0 0 1200 1000">
  <!-- 高さ拡張で余裕確保 -->
</svg>
```

### Step 7: 検証

修正後、必ず検証：

```bash
cd slides
python3 -c "
from evaluate_slide_quality import SlideQualityEvaluator
from pathlib import Path

evaluator = SlideQualityEvaluator()
svg_path = Path('diagrams/diagram_XX_name.svg')

overlap_info = evaluator._check_svg_overlap(svg_path)
score = evaluator._evaluate_svg_overlap(overlap_info)

print(f'Score: {score}/100')
if overlap_info:
    print(f'Issues: v:{overlap_info.get(\"vertical\", 0)}, h:{overlap_info.get(\"horizontal\", 0)}, oversized:{overlap_info.get(\"oversized\", 0)}')
"
```

**目標スコア: 80/100以上**

### Step 8: 両方の場所に保存

修正したSVGを以下の2箇所に保存：

```bash
# 1. diagrams/
cp fixed.svg diagrams/diagram_XX_name.svg

# 2. diagrams-web/
cp fixed.svg diagrams-web/diagram_XX_name.svg
```

## 修正時の注意点

1. **元のデザイン意図を保持**: 色、レイアウト構造、視覚的階層を維持
2. **テキスト内容は変更しない**: 座標とサイズのみ調整
3. **段階的修正**: 一度に全部変えず、少しずつ修正して検証
4. **viewBox拡張は最終手段**: まずy座標調整を試す
5. **フォント一貫性**: 同じクラスのテキストは同じフォントサイズ

## トラブルシューティング

**Q: viewBox高さを1500pxにしても収まらない**
→ コンテンツが多すぎます。要素を削減するか、複数のSVGに分割

**Q: フォントサイズを小さくすると読めなくなる**
→ 最小18px以上を維持。それ以下なら改行や要素削減を検討

**Q: 水平重なりが解消できない**
→ カラム幅を見直すか、3カラム→2カラムに変更

**Q: スコアが50/100から上がらない**
→ 完全に再設計が必要。`/create-svg` で新規作成を検討
