# SVG作成 (重なり防止版)

コンテキストに基づいて、テキストの重なりを防ぐSVGダイアグラムを作成します。

## 作成手順

### Step 1: 要件確認

以下の情報を確認してください：

1. **コンテンツ内容**
   - タイトル、見出し、本文テキストのリスト
   - 各テキストの重要度・優先順位
   - 必要な図形要素（矩形、矢印など）

2. **レイアウトタイプ**
   - フロー図（横/縦）
   - 比較表（2-3カラム）
   - 階層図
   - タイムライン
   - その他

3. **推奨viewBox**
   - シンプル図（要素5個以下）: 1000×600
   - 標準図（要素6-15個）: 1200×800
   - 複雑図（要素16個以上）: 1600×1000

### Step 2: レイアウト計算

以下の計算を**必ず実行**してください：

```python
# テキスト幅推定式
def estimate_text_width(text, font_size):
    japanese_chars = sum(1 for c in text if ord(c) > 0x3000)
    latin_chars = len(text) - japanese_chars
    # 日本語: 1.0倍、英数字: 0.5倍、安全マージン: 1.1倍
    return (japanese_chars * font_size * 1.0 +
            latin_chars * font_size * 0.5) * 1.1

# 最小間隔ルール
vertical_gap = max(font_size1, font_size2) * 1.4
horizontal_gap = max(10, font_size * 0.2)

# viewBox利用率チェック
safe_area_width = viewBox_width * 0.85  # 85%以内
safe_area_height = viewBox_height * 0.80  # 80%以内
```

### Step 3: フォントサイズ設定

viewBox幅に応じた推奨フォントサイズ：

**viewBox: 1000×600**
- タイトル: 48-54px
- 見出し: 32-40px
- 本文: 24-28px
- 注釈: 18-20px

**viewBox: 1200×800**
- タイトル: 56-64px
- 見出し: 40-48px
- 本文: 28-32px
- 注釈: 20-24px

**viewBox: 1600×1000**
- タイトル: 64-72px
- 見出し: 48-56px
- 本文: 32-40px
- 注釈: 24-28px

**制約**: 最大フォントサイズ ≤ viewBox幅 × 0.06

### Step 4: 配置ルール

#### 垂直配置
```
y座標の計算:
  次のy = 現在のy + 現在のfont_size × 1.4

セクション間隔:
  次のy = 現在のy + 80px (セクション区切り)
```

#### 水平配置（カラムレイアウト）
```
カラム数 n の場合:
  column_width = (viewBox_width * 0.85) / n
  column_gap = 40px

各カラムの開始x座標:
  column1_x = viewBox_width * 0.075  (左マージン)
  column2_x = column1_x + column_width + column_gap
  column3_x = column2_x + column_width + column_gap
```

#### テキスト配置前チェック
```
各テキスト要素について:
  1. 推定幅 = estimate_text_width(text, font_size)
  2. if 推定幅 > column_width:
       → 改行 OR フォントサイズ縮小 OR 省略
  3. if y座標 + font_size > viewBox_height * 0.8:
       → viewBox高さ拡張 OR コンテンツ削減
```

### Step 5: SVG生成

以下の構造でSVGを生成：

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 WIDTH HEIGHT">
  <defs>
    <style>
      .title { font-family: 'Noto Sans JP', sans-serif; font-size: XXpx; font-weight: bold; fill: #333; }
      .heading { font-family: 'Noto Sans JP', sans-serif; font-size: XXpx; font-weight: bold; fill: #00146E; }
      .text { font-family: 'Noto Sans JP', sans-serif; font-size: XXpx; fill: #333; }
      .note { font-family: 'Noto Sans JP', sans-serif; font-size: XXpx; fill: #666; }
    </style>
  </defs>

  <!-- Background -->
  <rect width="WIDTH" height="HEIGHT" fill="#FFFFFF"/>

  <!-- Title -->
  <text x="CENTER_X" y="60" class="title" text-anchor="middle">タイトル</text>

  <!-- Content (計算されたy座標を使用) -->
  <text x="X" y="Y" class="text">テキスト</text>

  <!-- ... -->
</svg>
```

### Step 6: 検証チェックリスト

SVG作成後、以下を確認：

- [ ] 全テキストがviewBox内（特にright端とbottom端）
- [ ] 垂直間隔: 最小 font_size × 1.4
- [ ] 水平間隔: 最小 10px または font_size × 0.2
- [ ] テキスト幅がカラム幅を超えていない
- [ ] viewBox利用率: 50-80% (空白・過密を回避)
- [ ] フォントサイズが viewBox幅 × 0.06 以下
- [ ] 長いテキストは適切に改行されている

## 重要な注意点

1. **計算を省略しない**: 必ず事前にテキスト幅と配置を計算
2. **余白を確保**: viewBoxの15-20%は余白として確保
3. **一貫性**: 同じ階層のテキストは同じフォントサイズ
4. **可読性優先**: 詰め込みすぎない（要素数が多い場合はviewBox拡張）
5. **日本語対応**: 日本語フォントを必ず指定 (Noto Sans JP)

## 出力

以下の2箇所にSVGファイルを保存：
1. `diagrams/diagram_XX_name.svg`
2. `diagrams-web/diagram_XX_name.svg`

作成後、必ず以下のコマンドで検証：
```bash
cd slides
python3 evaluate_slide_quality.py | grep "diagram_XX_name"
```

スコアが80/100以上であることを確認してください。
