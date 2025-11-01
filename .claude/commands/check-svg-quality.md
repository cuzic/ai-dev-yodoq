# SVG品質チェック

すべてのSVGの品質を確認し、修正が必要なファイルをリストアップします。

## 実行

```bash
cd slides
python3 evaluate_slide_quality.py
```

このコマンドは以下を評価します：

## 評価項目

### 1. SVGテキスト重なり (25%の重み)
- 垂直重なり: y座標の間隔が不足
- 水平重なり: 同じ行でテキストが重なる
- oversized: テキスト幅がviewBox幅の90%超

**スコアリング:**
- 100点: 重なりなし
- 80-99点: 軽微な問題（許容範囲）
- 50-79点: 修正推奨
- 0-49点: 修正必須

### 2. SVGテキスト可読性 (20%の重み)
- 最小フォントサイズが16px以上
- 推奨: 18px以上

### 3. オーバーフロー制御 (30%の重み)
- スライドコンテンツが720px高さ内に収まるか

### 4. その他 (25%の重み)
- 余白バランス (15%)
- フォント可読性 (5%)
- コンテンツ密度 (5%)

## 出力例

```
================================================================================
SLIDE QUALITY EVALUATION REPORT
================================================================================

📊 Overall Statistics
   Total slides: 210
   Average score: 91.8/100
   🟢 Excellent (90-100): 111 slides
   🔵 Good (70-89): 99 slides
   🟡 Fair (50-69): 0 slides
   🔴 Poor (<50): 0 slides

📈 Category Scores (Average)
   Overflow control: 100.0/100
   SVG text readability: 100.0/100
   SVG text overlap: 82.7/100
   Whitespace balance: 80.2/100
   Font readability: 100.0/100
   Content density: 85.0/100
```

## 問題のあるSVGを特定

詳細な問題リストを確認：

```bash
cd slides
python3 -c "
import json

with open('slide_quality_scores.json') as f:
    slides = json.load(f)

# SVG重なりスコア < 80 のスライドを抽出
problem_slides = [
    s for s in slides
    if s.get('svg_issues') and s['scores'].get('svg_overlap', 100) < 80
]

# スコア順にソート
problem_slides.sort(key=lambda x: x['scores'].get('svg_overlap', 100))

print(f'修正が必要なSVG: {len(problem_slides)}個\n')

for slide in problem_slides[:20]:
    print(f\"Slide {slide['page']}: {slide['title']}\")
    print(f\"  スコア: {slide['scores']['svg_overlap']}/100\")
    for issue in slide['svg_issues']:
        print(f\"    • {issue}\")
    print()
"
```

## 個別SVG詳細分析

特定のSVGを詳しく分析：

```bash
cd slides
python3 -c "
from evaluate_slide_quality import SlideQualityEvaluator
from pathlib import Path

evaluator = SlideQualityEvaluator()
svg_path = Path('diagrams/diagram_03_5step_flow.svg')

# 重なりチェック
overlap_info = evaluator._check_svg_overlap(svg_path)

if overlap_info:
    print(f'{svg_path.name}:')
    print(f'  Total issues: {overlap_info[\"count\"]}')
    print(f'  Vertical overlaps: {overlap_info.get(\"vertical\", 0)}')
    print(f'  Horizontal overlaps: {overlap_info.get(\"horizontal\", 0)}')
    print(f'  Oversized texts: {overlap_info.get(\"oversized\", 0)}')
    print(f'  Severity: {overlap_info[\"avg_severity\"]:.3f}')

    score = evaluator._evaluate_svg_overlap(overlap_info)
    print(f'  Score: {score}/100')
else:
    print(f'{svg_path.name}: No issues (100/100)')
"
```

## 水平重なり専用分析

```bash
cd slides
python3 analyze_svg_horizontal_overlap.py
```

このスクリプトは以下を検出：
- 水平方向のテキスト重なり
- viewBox幅を超える長いテキスト
- フォントサイズが大きすぎる要素

## 修正優先度の判断

### 優先度: 緊急 (スコア 0-49)
→ `/fix-svg-overlap` で即座に修正

### 優先度: 高 (スコア 50-79)
→ 時間があれば修正

### 優先度: 低 (スコア 80-99)
→ 許容範囲、余裕があれば改善

### 優先度: なし (スコア 100)
→ 修正不要

## 一括修正フロー

問題のあるSVGを一括で特定して修正：

```bash
# 1. 問題のあるSVGリストを生成
cd slides
python3 -c "
import json

with open('slide_quality_scores.json') as f:
    slides = json.load(f)

problem_svgs = set()
for slide in slides:
    if slide['scores'].get('svg_overlap', 100) < 50:
        for svg_file in slide.get('svg_files', []):
            problem_svgs.add(svg_file)

print('\n'.join(sorted(problem_svgs)))
" > problem_svgs.txt

# 2. リストを確認
cat problem_svgs.txt

# 3. 各SVGを順番に修正
# /fix-svg-overlap を使用
```

## 再ビルド＆再検証

修正後、スライドを再ビルドして検証：

```bash
# スライド再ビルド
cd slides
marp all_slides.md --html --allow-local-files -o index.html

# 品質チェック実行
python3 evaluate_slide_quality.py

# 改善確認
python3 -c "
import json

with open('slide_quality_scores.json') as f:
    slides = json.load(f)

avg_overlap = sum(s['scores'].get('svg_overlap', 100) for s in slides) / len(slides)
problem_count = len([s for s in slides if s['scores'].get('svg_overlap', 100) < 80])

print(f'SVG重なり平均スコア: {avg_overlap:.1f}/100')
print(f'問題のあるスライド数: {problem_count}/{len(slides)}')
"
```

## 目標基準

### 最低基準
- 平均スコア: 80/100以上
- SVG重なりスコア: 75/100以上
- スコア < 50 のスライド: 0個

### 推奨基準
- 平均スコア: 90/100以上
- SVG重なりスコア: 85/100以上
- スコア < 70 のスライド: 0個

### 理想基準
- 平均スコア: 95/100以上
- SVG重なりスコア: 95/100以上
- すべてのSVG: 90/100以上
