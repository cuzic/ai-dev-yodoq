# Marpスライド用ダイアグラム作成

Marpスライドの特定レイアウトに最適化されたSVGダイアグラムを作成します。

## 目的

Marpスライド（ai-seminar テーマ）に埋め込むSVGダイアグラムを、以下の原則に従って作成します：

1. **レイアウトに適合**: レイアウトクラスに応じた最適な縦横比
2. **視覚的補完**: テキストをそのまま画像化するのではなく、理解を深める視覚表現
3. **情報の構造化**: 複雑な関係性やフローを一目で理解できる形式
4. **コンテキスト活用**: スライドのテーマと内容に適したダイアグラム形式

## ダイアグラムの役割

### ❌ 避けるべき（悪い例）

**単なるテキストの画像化:**
```
テキスト「AIの3原則は...」
↓
画像にそのまま同じテキストを書く
```
→ 理解が深まらない、冗長

### ✅ 推奨（良い例）

**視覚的な構造化と関係性の明示:**
```
テキスト「AIの3原則は...」
↓
3つの原則を図形で表現し、相互関係を矢印で示す
各原則の影響や結果を視覚的に配置
```
→ 理解が深まる、記憶に残る

## 前提条件の確認

### 1. ターゲットスライドの特定

**必須情報:**
- スライドファイル名（例: `day1_2.md`）
- スライド番号または見出し
- 使用するレイアウトクラス

**レイアウトクラスの確認方法:**
```markdown
<!-- _class: layout-diagram-only -->
# スライドタイトル

![ダイアグラム説明](../assets/diagrams/diagram_XX_name.svg)
```

### 2. レイアウトクラスごとの仕様

#### layout-diagram-only（全画面ダイアグラム）
- **使用頻度:** ★★★★★ (20回使用)
- **縦横比:** 2.05:1（かなり横長）
- **推奨viewBox:** 1250×610
- **表示領域:** スライドほぼ全体（1254px × 612px）
- **適したダイアグラム:**
  - 全体フロー図（5-STEPフローなど）
  - 複雑な関係図（相互依存関係）
  - タイムライン（時系列の流れ）
  - 大規模な構成図
- **情報量:** 30-50要素
- **注意:** かなり横長を活かしたレイアウト、横方向の流れを重視

#### layout-horizontal-right（右側ダイアグラム）
- **使用頻度:** ★★★★★ (23回使用)
- **縦横比:** 1.30:1（やや横長）
- **推奨viewBox:** 700×540
- **表示領域:** スライドの右側55%（694px × 540px）
- **適したダイアグラム:**
  - プロセス図（上から下の流れ）
  - 階層構造（トップダウン）
  - 状態遷移図
  - 概念図（関係性の表現）
- **情報量:** 15-25要素
- **注意:** やや横長だが、上から下への流れも活用可能

#### layout-horizontal-left（左側ダイアグラム）
- **使用頻度:** ★★★★★ (19回使用)
- **縦横比:** 1.30:1（やや横長）
- **推奨viewBox:** 700×540
- **表示領域:** スライドの左側55%（694px × 540px）
- **適したダイアグラム:** layout-horizontal-rightと同様
- **情報量:** 15-25要素
- **注意:** 右側のテキストとの対応を考慮

**注意:** layout-comparison、layout-callout、card-grid は主にテキストベースのレイアウトであり、通常は独立したSVGダイアグラムを使用しません。これらのレイアウトでは、HTMLやMarkdown内の装飾要素として視覚的な表現を行います。

### 3. ダイアグラムの種類と適用例

#### フローチャート（全体の流れ）
**適したレイアウト:** layout-diagram-only, layout-horizontal-right/left
**視覚的補完の例:**
- スライドのテキスト: 「5-STEPで開発を進めます」
- ダイアグラム: 5つのステップを矢印でつなぎ、各ステップの所要時間、成果物、注意点を視覚的に配置
- **補完効果:** 順序、タイミング、依存関係が一目でわかる

#### 関係図（相互作用）
**適したレイアウト:** layout-diagram-only
**視覚的補完の例:**
- スライドのテキスト: 「AIの3つの制約と対策」
- ダイアグラム: 3つの制約を円で表現し、それぞれの影響を矢印で示し、対策をボックスで囲む
- **補完効果:** 制約間の相互関係、因果関係が明確になる

#### プロセス図（段階的な手順）
**適したレイアウト:** layout-horizontal-right/left
**視覚的補完の例:**
- スライドのテキスト: 「リバースエンジニアリングの手法」
- ダイアグラム: 縦方向に手順を配置し、各段階での入力・出力・判断ポイントを明示
- **補完効果:** 手順の流れ、分岐点、判断基準が視覚的に理解できる

#### 比較図（対比）
**適したレイアウト:** layout-comparison
**視覚的補完の例:**
- スライドのテキスト: 「TDDあり vs なし」
- ダイアグラム: 左右に分けて、開発フローの違いを視覚的に対比
- **補完効果:** 違いが明確に、選択の基準が理解しやすい

#### 概念図（抽象概念の具体化）
**適したレイアウト:** layout-horizontal-right/left, layout-callout
**視覚的補完の例:**
- スライドのテキスト: 「Living Documentation とは」
- ダイアグラム: ドキュメントとコードの循環関係を図示
- **補完効果:** 抽象的な概念が具体的にイメージできる

### 4. テキストと画像の適切な分担

#### ❌ 悪い例：テキストの単純な複製

**スライドのテキスト:**
```
STEP1: 要件定義
- 曖昧さの排除
- ユーザーストーリー作成
- 受け入れ条件の定義
```

**ダイアグラム（悪い例）:**
```svg
<text>STEP1: 要件定義</text>
<text>- 曖昧さの排除</text>
<text>- ユーザーストーリー作成</text>
<text>- 受け入れ条件の定義</text>
```
→ **問題点:** テキストと全く同じ、視覚的な価値がない、冗長

#### ✅ 良い例：視覚的な構造化と関係性の追加

**スライドのテキスト:**（同上）

**ダイアグラム（良い例）:**
```svg
<!-- STEP1を大きなボックスで表現 -->
<rect class="step-box"/>
<text class="step-title">STEP1: 要件定義</text>

<!-- 3つの活動を矢印で接続 -->
<rect class="activity">曖昧さ排除</rect>
  ↓ (矢印)
<rect class="activity">ユーザーストーリー</rect>
  ↓ (矢印)
<rect class="activity">受け入れ条件</rect>

<!-- 成果物を吹き出しで -->
<ellipse class="output">明確な仕様書</ellipse>

<!-- 注意点をアイコンで -->
<circle class="warning-icon">⚠️</circle>
<text>前工程を丁寧に</text>
```
→ **改善点:**
  - 活動の順序が視覚的に明確
  - 成果物が区別されている
  - 注意点がアイコンで強調されている
  - テキストを補完する情報を追加

## 作成手順

### Step 1: レイアウトクラスに基づく設定

スライドのレイアウトクラスを確認し、対応するviewBoxを選択：

```python
# レイアウトマッピング（SVGを使用するレイアウトのみ）
LAYOUT_SPECS = {
    'layout-diagram-only': {'viewBox': (1250, 610), 'aspect': '2.05:1'},
    'layout-horizontal-right': {'viewBox': (700, 540), 'aspect': '1.30:1'},
    'layout-horizontal-left': {'viewBox': (700, 540), 'aspect': '1.30:1'},
}

# 指定されたレイアウトから設定を取得
layout_class = 'layout-diagram-only'  # 例
spec = LAYOUT_SPECS[layout_class]
viewBox_width, viewBox_height = spec['viewBox']
```

### Step 2: コンテンツ要件の確認

以下を明確にしてください：

**必須情報:**
1. ダイアグラムのタイトル
2. 主要な要素リスト（テキスト、図形）
3. 各要素の階層・重要度
4. 要素間の関係（矢印、グループ化など）

**推奨情報:**
5. カラースキーム（ai-seminar テーマに合わせる）
6. 強調すべきポイント
7. 参考となる既存ダイアグラム

### Step 3: レイアウト計算（重要）

**必ず以下の計算を実行してください:**

```python
# テキスト幅推定式（Noto Sans JP基準）
def estimate_text_width(text, font_size):
    japanese_chars = sum(1 for c in text if ord(c) > 0x3000)
    latin_chars = len(text) - japanese_chars
    # 日本語: 1.0倍、英数字: 0.5倍、安全マージン: 1.15倍
    return (japanese_chars * font_size * 1.0 +
            latin_chars * font_size * 0.5) * 1.15

# レイアウトごとの安全領域
safe_area_ratio = {
    'layout-diagram-only': 0.90,      # 90%使用可
    'layout-horizontal-right': 0.85,  # 85%使用可
    'layout-horizontal-left': 0.85,
    'layout-comparison': 0.80,        # 80%使用可
    'layout-callout': 0.75,           # 75%使用可
    'card-grid': 0.70,                # 70%使用可（小さいため余白重要）
}

safe_width = viewBox_width * safe_area_ratio[layout_class]
safe_height = viewBox_height * safe_area_ratio[layout_class]

# 垂直間隔の計算
def vertical_gap(font_size_1, font_size_2):
    return max(font_size_1, font_size_2) * 1.5

# 水平間隔の計算
def horizontal_gap(font_size):
    return max(15, font_size * 0.25)
```

### Step 4: フォントサイズの決定

viewBoxサイズに応じたフォントサイズ指定：

```python
# viewBox幅に基づく基本フォントサイズ
base_font_size = viewBox_width * 0.032  # 約3.2%

# 階層別フォントサイズ
FONT_SIZES = {
    'title': base_font_size * 1.8,      # タイトル
    'heading': base_font_size * 1.4,    # 見出し
    'body': base_font_size * 1.0,       # 本文
    'note': base_font_size * 0.7,       # 注釈
}

# 制約チェック
max_allowed_font = viewBox_width * 0.06
for key, size in FONT_SIZES.items():
    if size > max_allowed_font:
        FONT_SIZES[key] = max_allowed_font
```

**具体例:**
- **layout-diagram-only (1250×610)**: base=40px → タイトル72px, 見出し56px, 本文40px, 注釈28px
- **layout-horizontal-right (700×540)**: base=22px → タイトル40px, 見出し31px, 本文22px, 注釈15px
- **layout-horizontal-left (700×540)**: base=22px → タイトル40px, 見出し31px, 本文22px, 注釈15px

### Step 5: SVG構造の生成

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewBox_width} {viewBox_height}">
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
    </style>
  </defs>

  <!-- 背景 -->
  <rect width="{viewBox_width}" height="{viewBox_height}" fill="#FFFFFF"/>

  <!-- コンテンツ（計算された座標を使用） -->
  <text x="{x}" y="{y}" class="title">タイトル</text>
  <!-- ... -->
</svg>
```

### Step 6: 品質検証（必須）

SVG作成後、以下を実行：

```bash
# 1. オーバーフロー・オーバーラップチェック
python scripts/slides/validate_svg_bounds.py assets/diagrams/diagram_XX_name.svg

# 2. スライドに埋め込んで視覚確認
# day*.md に以下を追加
![テスト](../assets/diagrams/diagram_XX_name.svg)

# 3. Marpでレンダリング
cd slides
marp day1_2.md --html --allow-local-files -o test.html

# 4. ブラウザで確認
# test.html を開いて、レイアウト内での見え方を確認
```

## 出力先

**重要: 以下の両方に保存してください:**

```
assets/diagrams/diagram_XX_descriptive_name.svg
```

命名規則：
- `diagram_` で始まる
- 2桁の連番（01-99）
- アンダースコア区切り
- 内容を表す英語名（スネークケース）
- 例: `diagram_03_5step_flow.svg`, `diagram_48_day1_key_messages.svg`

## カラーパレット（ai-seminarテーマ）

```css
/* プライマリカラー */
--color-primary: #00146E;      /* 濃紺（タイトル、重要要素） */
--color-secondary: #00AFF0;    /* 水色（強調、アクション） */

/* テキストカラー */
--color-text: #333333;         /* ダークグレー（本文） */
--color-text-light: #666666;   /* グレー（注釈） */

/* 背景カラー */
--color-bg: #FFFFFF;           /* 白（背景） */
--color-bg-accent: #F0F8FF;    /* アリスブルー（ボックス背景） */

/* ステータスカラー */
--color-success: #228B22;      /* グリーン */
--color-warning: #FF8C00;      /* オレンジ */
--color-error: #DC143C;        /* 赤 */
--color-info: #4169E1;         /* ブルー */
```

## 検証チェックリスト

- [ ] レイアウトクラスに適した縦横比を使用
- [ ] すべてのテキストが安全領域内
- [ ] 垂直間隔: font_size × 1.5 以上
- [ ] 水平間隔: 15px または font_size × 0.25 以上
- [ ] viewBox利用率が適切（50-90%）
- [ ] フォントサイズがレイアウトに適切
- [ ] 日本語フォント（Noto Sans JP）を使用
- [ ] カラーパレットがai-seminarテーマに準拠
- [ ] `validate_svg_bounds.py` で検証済み
- [ ] Marpでレンダリングして視覚確認済み

## トラブルシューティング

### 問題: テキストがはみ出る

**原因:** viewBoxサイズの見積もり不足

**解決策:**
1. `estimate_text_width()` で幅を再計算
2. viewBoxを10-20%拡大
3. またはフォントサイズを縮小

### 問題: 情報が多すぎて入らない

**原因:** レイアウトに対してコンテンツが過剰

**解決策:**
1. レイアウトクラスを変更（より大きなものに）
2. コンテンツを削減・簡略化
3. 複数のダイアグラムに分割

### 問題: レイアウト内で小さく見える

**原因:** 縦横比の不一致

**解決策:**
1. レイアウトクラスに対応するviewBoxを再確認
2. LAYOUT_SPECSを参照して正しい縦横比を使用

## 使用例

### 例1: layout-diagram-only でフロー図を作成

```markdown
<!-- スライド: day1_2.md -->
<!-- _class: layout-diagram-only -->

# 5-STEPフロー全体

![5-STEPフロー](../assets/diagrams/diagram_03_5step_flow.svg)
```

**SVG仕様:**
- viewBox: 1250×610 (2.05:1)
- タイトル: 72px
- フロー要素: 5つのステップ + 矢印
- 各ステップ: 見出し56px、説明40px

### 例2: layout-horizontal-right でプロセス図を作成

```markdown
<!-- スライド: day2_1.md -->
<!-- _class: layout-horizontal-right -->

# リバースエンジニアリングのプロセス

![リバースエンジニアリングのプロセス](../assets/diagrams/diagram_12_reverse_engineering.svg)

**説明テキストがここに表示される（左側）**
```

**SVG仕様:**
- viewBox: 700×540 (1.30:1)
- タイトル: 40px
- プロセス要素: 3-4ステップ
- 各ステップ: 見出し31px、説明22px

## 参考資料

- [ai-seminar.css](/assets/themes/ai-seminar.css) - テーマのCSS定義
- [validate_svg_bounds.py](/scripts/slides/validate_svg_bounds.py) - SVG検証スクリプト
- [既存ダイアグラム](/assets/diagrams-web/) - 参考になるSVG例
