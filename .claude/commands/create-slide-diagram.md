# Marpスライド用ダイアグラム並列作成

複数の専門エージェントを並列起動して、Marpスライドに必要なSVGダイアグラムを効率的に作成します。

## 概要

このコマンドは以下を自動実行します：

1. **不足SVGの特定**: スライドから参照されているが存在しないSVGをリストアップ
2. **エージェント分割**: SVGをグループ化し、複数のエージェントに割り当て
3. **並列作成**: Taskツールで複数エージェントを同時起動し、並列作成
4. **検証**: 各SVGのオーバーフロー・オーバーラップをチェック
5. **統合**: 作成結果をまとめてコミット

## 実行手順

### Step 1: 不足SVGの特定

```bash
# スライドから参照されている全SVGを抽出
grep -h "!\[.*\](.*\.svg)" slides/day*.md | \
  sed 's/.*(\(.*\))/\1/' | \
  sed 's/^\.\.\///' | \
  sort -u > /tmp/required_svgs.txt

# 存在しないSVGを特定
python3 << 'EOF'
from pathlib import Path

required = Path('/tmp/required_svgs.txt').read_text().splitlines()
missing = []

for svg_path in required:
    if not Path(svg_path).exists():
        missing.append(svg_path)

# グループ化（10-15個ずつ）
group_size = 12
for i in range(0, len(missing), group_size):
    group = missing[i:i+group_size]
    print(f"\n=== Group {i//group_size + 1} ({len(group)} SVGs) ===")
    for svg in group:
        basename = Path(svg).stem
        print(f"- {basename}")
EOF
```

### Step 2: グループごとのコンテキスト抽出

各グループのSVGについて、スライドから文脈を抽出：

```python
from pathlib import Path

def extract_svg_context(svg_filename):
    """SVGのコンテキストをスライドから抽出"""
    slides_dir = Path('slides')
    context = {}

    for slide_file in slides_dir.glob('day*.md'):
        content = slide_file.read_text()

        # SVG参照の前後10行を取得
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if svg_filename in line:
                start = max(0, i-10)
                end = min(len(lines), i+10)
                context_lines = lines[start:end]

                # レイアウトクラスを抽出
                layout_class = None
                for j in range(i, max(0, i-15), -1):
                    if '<!-- _class:' in lines[j]:
                        layout_class = lines[j].split('_class:')[1].split('-->')[0].strip()
                        break

                context = {
                    'file': slide_file.name,
                    'layout': layout_class,
                    'context_lines': context_lines,
                    'title': None
                }

                # タイトル抽出
                for line in context_lines:
                    if line.startswith('# '):
                        context['title'] = line[2:].strip()
                        break

                return context

    return None

# 使用例
# context = extract_svg_context('diagram_01_ai_principles.svg')
```

### Step 3: エージェント並列実行

**重要**: 以下のTaskツール呼び出しを**1つのメッセージで全て送信**してください（並列実行のため）。

```markdown
エージェント1-4を並列起動して、不足しているSVGダイアグラムを作成してください。

各エージェントは以下のガイドラインに従ってSVGを作成すること：

[エージェント共通ガイドラインを以下に記載]
```

### Step 4: 検証と統合

全エージェント完了後：

```bash
# 1. 全SVGの検証
cd assets
python ../scripts/slides/validate_svg_bounds.py

# 2. FAILがある場合は修正
# 3. 全PASS後にコミット
git add assets/diagrams/diagram_*.svg
git commit -m "feat: Add missing SVG diagrams (parallel generation)

- Created X SVGs for Marp slides
- All diagrams validated (no overflow/overlap)
- Optimized for layout-specific aspect ratios

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## エージェント共通ガイドライン

各エージェントは以下の仕様に従ってSVGを作成してください。

### レイアウト別仕様

#### layout-diagram-only（全画面ダイアグラム）
- **縦横比:** 2.05:1（かなり横長）
- **推奨viewBox:** 1250×610
- **表示領域:** 1254px × 612px
- **フォントサイズ:** base=40px → タイトル72px, 見出し56px, 本文40px, 注釈28px
- **適した内容:** 全体フロー図、複雑な関係図、タイムライン、大規模構成図
- **情報量:** 30-50要素

#### layout-horizontal-right（右側ダイアグラム）
- **縦横比:** 1.30:1（やや横長）
- **推奨viewBox:** 700×540
- **表示領域:** 694px × 540px
- **フォントサイズ:** base=22px → タイトル40px, 見出し31px, 本文22px, 注釈15px
- **適した内容:** プロセス図、階層構造、状態遷移図、概念図
- **情報量:** 15-25要素

#### layout-horizontal-left（左側ダイアグラム）
- **仕様:** layout-horizontal-rightと同じ
- **注意点:** 右側のテキストとの対応を考慮

### ダイアグラム作成原則

#### ✅ 推奨：視覚的補完

**良い例:**
```
スライドのテキスト: "AIの3原則は..."
↓
ダイアグラム: 3つの原則を図形で表現し、相互関係を矢印で示す
              各原則の影響や結果を視覚的に配置
→ 理解が深まる、記憶に残る
```

#### ❌ 避ける：テキストの複製

**悪い例:**
```
スライドのテキスト: "STEP1: 要件定義"
↓
ダイアグラム: そのまま同じテキストを画像化
→ 理解が深まらない、冗長
```

### 必須計算式

#### テキスト幅推定

```python
def estimate_text_width(text, font_size):
    """日本語/英語を考慮したテキスト幅推定"""
    japanese_chars = sum(1 for c in text if ord(c) > 0x3000)
    latin_chars = len(text) - japanese_chars
    # 日本語: 1.0倍、英数字: 0.5倍、安全マージン: 1.15倍
    return (japanese_chars * font_size * 1.0 +
            latin_chars * font_size * 0.5) * 1.15
```

#### 垂直・水平間隔

```python
# 垂直間隔（テキスト行間）
vertical_gap = max(font_size_1, font_size_2) * 1.5

# 水平間隔（要素間）
horizontal_gap = max(15, font_size * 0.25)
```

#### 安全領域

```python
safe_area_ratio = {
    'layout-diagram-only': 0.90,      # 90%使用可
    'layout-horizontal-right': 0.85,  # 85%使用可
    'layout-horizontal-left': 0.85,   # 85%使用可
}

safe_width = viewBox_width * safe_area_ratio[layout]
safe_height = viewBox_height * safe_area_ratio[layout]
```

### SVGテンプレート

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
  <defs>
    <style>
      .title {
        font-family: 'Noto Sans JP', sans-serif;
        font-size: {title_size}px;
        font-weight: bold;
        fill: #00146E;
        text-anchor: middle;
      }
      .heading {
        font-family: 'Noto Sans JP', sans-serif;
        font-size: {heading_size}px;
        font-weight: bold;
        fill: #00146E;
      }
      .body {
        font-family: 'Noto Sans JP', sans-serif;
        font-size: {body_size}px;
        fill: #333333;
      }
      .note {
        font-family: 'Noto Sans JP', sans-serif;
        font-size: {note_size}px;
        fill: #666666;
      }
      .highlight {
        fill: #00AFF0;
        font-weight: bold;
      }
      .box {
        fill: #F0F8FF;
        stroke: #00146E;
        stroke-width: 2;
        rx: 5;
      }
      .arrow {
        stroke: #00146E;
        stroke-width: 3;
        fill: none;
        marker-end: url(#arrowhead);
      }
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#00146E" />
    </marker>
  </defs>

  <rect width="{width}" height="{height}" fill="#FFFFFF"/>

  <!-- コンテンツ（計算された座標を使用） -->
  <text x="{x}" y="{y}" class="title">タイトル</text>
  <!-- ... -->
</svg>
```

### カラーパレット（ai-seminarテーマ）

```css
/* プライマリ */
--color-primary: #00146E;      /* 濃紺（タイトル、重要要素） */
--color-secondary: #00AFF0;    /* 水色（強調、アクション） */

/* テキスト */
--color-text: #333333;         /* ダークグレー（本文） */
--color-text-light: #666666;   /* グレー（注釈） */

/* 背景 */
--color-bg: #FFFFFF;           /* 白（背景） */
--color-bg-accent: #F0F8FF;    /* アリスブルー（ボックス背景） */

/* ステータス */
--color-success: #228B22;      /* グリーン */
--color-warning: #FF8C00;      /* オレンジ */
--color-error: #DC143C;        /* 赤 */
--color-info: #4169E1;         /* ブルー */
```

### 検証方法

各SVG作成後、必ず検証：

```bash
cd assets
python ../scripts/slides/validate_svg_bounds.py
```

**期待される出力:**
```
✅ PASS (または WARNING以下)
```

**FAILの場合:**
- viewBoxを推奨サイズに拡大
- またはフォントサイズを縮小
- テキストを簡略化

### 命名規則

```
assets/diagrams/diagram_{番号}_{内容}.svg
```

例:
- `diagram_01_ai_principles.svg`
- `diagram_03_5step_flow.svg`
- `diagram_12_reverse_engineering.svg`

## 並列実行例

**1つのメッセージで全エージェントを起動**（これが重要）：

```
Task 1: diagram_01-12を作成
Task 2: diagram_13-24を作成
Task 3: diagram_25-36を作成
Task 4: diagram_37-48を作成
```

各Taskで以下を実行：
1. スライドからコンテキスト抽出
2. 適切なレイアウト判定
3. SVG作成（計算式使用）
4. 検証
5. 必要に応じて修正

## トラブルシューティング

### オーバーフロー発生
- viewBoxを10-20%拡大
- フォントサイズを縮小
- テキストを簡略化

### テキスト重なり
- 垂直間隔: `font_size × 1.5`以上確保
- 水平間隔: `max(15px, font_size × 0.25)`以上確保

### レイアウトに合わない
- レイアウトクラスを再確認
- 正しいviewBox仕様を使用

## 参考資料

- [ai-seminar.css](../assets/themes/ai-seminar.css) - テーマCSS定義
- [validate_svg_bounds.py](../scripts/slides/validate_svg_bounds.py) - SVG検証スクリプト
- [既存ダイアグラム](../assets/diagrams-web/) - 参考SVG例

## 成功基準

✅ 全SVGが以下を満たすこと：
- レイアウトに適した縦横比
- テキストと補完関係にある
- 視覚的に理解を深める
- オーバーフロー・オーバーラップなし
- 検証スクリプトでPASSまたはWARN以下
