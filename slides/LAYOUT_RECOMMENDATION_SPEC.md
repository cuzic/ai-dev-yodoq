# スライドレイアウト推奨システム 仕様 v1.0

## 目的
Markdownスライドのコンテンツを解析し、最適なMarpレイアウトクラスを自動判定する。

## 対応レイアウトクラス

### 1. `lead`
**用途**: タイトルスライド、セクション区切り
**特徴**: 中央揃え、大きいフォント

### 2. `layout-diagram-only`
**用途**: 図表・画像メイン
**特徴**: 図表を大きく表示、テキスト最小限

### 3. `layout-horizontal-left`
**用途**: 画像左、説明右
**特徴**: 画像とテキストを横並び配置（画像優先）

### 4. `layout-horizontal-right`
**用途**: 説明左、画像右
**特徴**: テキストと画像を横並び配置（テキスト優先）

### 5. `two-column`
**用途**: 2つの項目を並列比較
**特徴**: 左右均等に分割

### 6. `two-column compact`
**用途**: 2カラムでコンテンツ量が多い
**特徴**: フォントサイズ縮小、パディング削減

### 7. `compact`
**用途**: 単一カラムでコンテンツ量が多い
**特徴**: フォントサイズ縮小、行間縮小

### 8. デフォルト（クラス指定なし）
**用途**: 標準的なテキストスライド
**特徴**: 通常フォント、通常間隔

---

## 判定ルール（優先度順）

### Rule 1: `lead` 判定
**条件（以下のいずれか）:**
- H1のみ（他のコンテンツなし）
- H1 + 短い説明文（50文字以内）
- H1 + 箇条書き1-2項目（各項目30文字以内）

**除外条件:**
- 画像・図表を含む
- コードブロックを含む
- 表を含む

**判定ロジック:**
```python
if has_h1 and not has_image and not has_code:
    if content_lines <= 3 and total_chars < 100:
        return 'lead'
```

---

### Rule 2: `layout-diagram-only` 判定
**条件:**
- 画像/SVGが1つ以上存在
- テキスト量が少ない（箇条書き0-2項目、または本文50文字以内）
- タイトル（H1/H2）のみまたはタイトル+キャプション程度

**判定ロジック:**
```python
if has_image:
    text_lines = count_text_lines(exclude_title=True)
    if text_lines <= 3 and total_text_chars < 150:
        return 'layout-diagram-only'
```

---

### Rule 3: `layout-horizontal-left` / `layout-horizontal-right` 判定
**条件:**
- 画像/SVGが1つ存在
- テキスト量が中程度（箇条書き3-8項目、または本文150-500文字）
- タイトル + 説明文の構造

**左右の判定基準:**
- **layout-horizontal-left**: 画像が視覚的に重要（図表、グラフ、複雑なSVG）
- **layout-horizontal-right**: テキストが重要（説明メイン、画像は補足）

**ヒューリスティック:**
- SVGファイル名に `diagram_`, `flow_`, `chart_` を含む → `left`
- テキストの箇条書きが5項目以上 → `right`
- 画像アスペクト比が横長（width > height * 1.5） → `left`
- デフォルト → `right`

**判定ロジック:**
```python
if has_image and 3 <= bullet_count <= 8:
    if is_diagram_focused(image_path):
        return 'layout-horizontal-left'
    else:
        return 'layout-horizontal-right'
```

---

### Rule 4: `two-column` / `two-column compact` 判定
**条件:**
- 明示的な比較構造（「Before/After」「従来/改善」など）
- または、箇条書きが左右に分かれている
- または、2つのリストが並列関係

**compact判定:**
- 各カラムの箇条書きが5項目以上
- または、各カラムの文字数が200文字以上

**判定ロジック:**
```python
if has_comparison_keywords or has_two_lists:
    total_items = count_all_list_items()
    if total_items >= 10:
        return 'two-column compact'
    else:
        return 'two-column'
```

**比較キーワード:**
- Before/After, 従来/改善, 問題/解決, メリット/デメリット
- VS, 比較, 対比

---

### Rule 5: `compact` 判定（単一カラム）
**条件:**
- 箇条書きが9項目以上
- または、段落が5個以上
- または、総文字数が800文字以上
- または、コードブロック + 説明文が長い

**判定ロジック:**
```python
if bullet_count >= 9 or paragraph_count >= 5 or total_chars >= 800:
    if not is_two_column_candidate:
        return 'compact'
```

---

### Rule 6: デフォルト判定
**条件:**
- 上記のいずれにも該当しない
- 標準的なテキストスライド
- 箇条書き3-8項目
- 文字数100-500文字

---

## コンテンツ解析要素

### 1. 構造要素
- **H1タイトル**: `# タイトル`
- **H2サブタイトル**: `## サブタイトル`
- **箇条書き**: `- item`, `* item`
- **番号付きリスト**: `1. item`
- **段落**: 連続するテキスト行

### 2. メディア要素
- **画像**: `![alt](path.png)`, `![alt](path.jpg)`
- **SVG**: `![alt](path.svg)`
- **コードブロック**: ` ```language ... ``` `
- **表**: `| col1 | col2 |`

### 3. 計測指標
- **total_chars**: 総文字数（タイトル除く）
- **bullet_count**: 箇条書き項目数
- **paragraph_count**: 段落数
- **image_count**: 画像数
- **code_block_count**: コードブロック数
- **table_count**: 表の数

### 4. テキスト密度指標
```python
text_density = total_chars / (bullet_count + paragraph_count + 1)

# 低密度: < 100 chars/item → lead候補
# 中密度: 100-300 chars/item → デフォルト
# 高密度: > 300 chars/item → compact候補
```

---

## 特殊ケース処理

### Case 1: 複数画像
**条件**: 画像が2つ以上
**判定**:
- 画像が2-3個 + 説明が短い → `layout-diagram-only`
- 画像が2個 + 説明が長い → `two-column` or デフォルト
- 画像が4個以上 → デフォルト or `card-grid`（グリッドレイアウト）

### Case 2: コードブロック含む
**条件**: コードブロックが1つ以上
**判定**:
- コード + 短い説明（3行以内） → デフォルト
- コード + 長い説明（4行以上） → `compact`
- コード + 画像 → `layout-horizontal-right`（コード左、画像右）

### Case 3: 表を含む
**条件**: Markdown表が存在
**判定**:
- 表が主コンテンツ → デフォルト
- 表 + 長い説明 → `compact`
- 表が大きい（5行以上） → `compact`

---

## 実装アルゴリズム（疑似コード）

```python
def recommend_layout(slide_content: str) -> str:
    # 1. コンテンツ解析
    analysis = analyze_content(slide_content)

    # 2. Rule 1: lead判定
    if is_lead(analysis):
        return 'lead'

    # 3. Rule 2: diagram-only判定
    if is_diagram_only(analysis):
        return 'layout-diagram-only'

    # 4. Rule 4: two-column判定（Rule 3より優先）
    two_col = check_two_column(analysis)
    if two_col:
        return two_col  # 'two-column' or 'two-column compact'

    # 5. Rule 3: horizontal判定
    horizontal = check_horizontal_layout(analysis)
    if horizontal:
        return horizontal  # 'layout-horizontal-left' or 'layout-horizontal-right'

    # 6. Rule 5: compact判定
    if is_compact(analysis):
        return 'compact'

    # 7. Rule 6: デフォルト
    return None  # クラス指定なし

def analyze_content(content: str) -> dict:
    return {
        'has_h1': bool(re.search(r'^# ', content, re.M)),
        'has_h2': bool(re.search(r'^## ', content, re.M)),
        'bullet_count': len(re.findall(r'^[-*] ', content, re.M)),
        'paragraph_count': count_paragraphs(content),
        'total_chars': len(content),
        'has_image': bool(re.search(r'!\[.*?\]\(.*?\)', content)),
        'image_count': len(re.findall(r'!\[.*?\]\(.*?\)', content)),
        'has_code': bool(re.search(r'```', content)),
        'has_table': bool(re.search(r'^\|', content, re.M)),
        'images': extract_images(content),
        'text_density': calculate_density(content),
        'has_comparison': has_comparison_keywords(content)
    }
```

---

## 検証指標

### 1. 適合率（Precision）
既存のレイアウト指定と推奨レイアウトの一致率

### 2. カバレッジ
全スライドのうち、明確な推奨を出せる割合

### 3. 視覚的バランス
- テキスト量とレイアウトの整合性
- 画像サイズと配置の適切性

---

## 出力形式

### 1. 推奨レイアウト
```json
{
  "slide_number": 10,
  "title": "スライドタイトル",
  "current_layout": "layout-horizontal-left",
  "recommended_layout": "layout-horizontal-right",
  "confidence": 0.85,
  "reason": "テキスト量が多く（5項目）、画像は補足的な役割のため",
  "metrics": {
    "bullet_count": 5,
    "total_chars": 320,
    "image_count": 1,
    "text_density": 64.0
  }
}
```

### 2. 不一致レポート
現在のレイアウトと推奨レイアウトが異なるスライドのリスト

### 3. 統計サマリー
- 一致率
- レイアウト別の使用頻度
- 改善候補スライド数

---

## 拡張性

### 将来対応
1. **機械学習モデル**: 過去の良いレイアウト例から学習
2. **A/Bテスト**: 複数のレイアウト候補を提示
3. **ユーザーフィードバック**: 推奨を採用/却下した履歴を学習
4. **コンテキスト考慮**: 前後のスライドとの一貫性
5. **テーマ最適化**: 使用テーマに応じたレイアウト調整

---

## 制約事項

1. **Marp固有**: Marp CLIの仕様に依存
2. **日本語前提**: 文字数計算は日本語を想定
3. **手動調整必要**: 推奨は参考、最終判断は人間
4. **画像内容不明**: 画像の実際の内容は解析しない（ファイル名のみ）

---

**バージョン**: 1.0
**作成日**: 2025-11-01
**対象**: Marp Markdownスライド
