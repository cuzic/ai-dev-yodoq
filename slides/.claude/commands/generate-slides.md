# Generate Slides - 原稿からスライド骨組み生成

原稿テキストからMarpスライドの骨組みを自動生成するコマンドです。適切な粒度でスライドを分割し、各スライドに最適なレイアウトを選択します。

**重要**: このコマンドは粗いスライド骨組みを生成し、その後 `/slide-tdd` で各スライドの詳細を作成することを前提としています。

## 🎯 目的

- 原稿テキスト（Markdown）からスライドの骨組みを自動生成
- 適切な粒度でスライドを分割
- 各スライドに最適なMarpレイアウトを自動選択
- `/slide-tdd` との緊密な連携で高品質スライドを作成

## 🔗 /slide-tdd との連携

```
/generate-slides → /slide-tdd (各スライド) → 完成
     ⬇️                ⬇️
  骨組み作成        詳細作成・品質向上
```

### ワークフロー

1. **`/generate-slides`**: 原稿から骨組み生成
   - スライドを分割
   - レイアウトを決定
   - 最小限の内容を配置
   - プレースホルダーを設定

2. **`/slide-tdd`**: 各スライドを詳細化
   - PLAN: 受入条件定義
   - RED: 判定処理作成
   - GREEN: SVG図表作成、内容充実
   - REFACTOR: 品質向上
   - VERIFY: 最終検証

### 連携のメリット

- ✅ 全体構造を先に決定できる
- ✅ 各スライドに集中して品質を高められる
- ✅ 一貫性のあるスライドセットを作成
- ✅ 段階的な品質向上が可能

---

## 📋 実行フロー

```
INPUT → ANALYZE → SPLIT → LAYOUT → SCAFFOLD → OUTPUT
 📄      🔍       ✂️      🎨       📝         📤
```

---

## Phase 1: INPUT 📄（原稿入力）

### ユーザーに確認

1. **原稿ソース**
   - 新規テキストを貼り付け
   - または既存ファイルパスを指定

2. **スライド枚数の指定（オプション）**
   - 枚数指定あり: その枚数を目標に分割
   - 枚数指定なし: 内容に応じて自動分割

3. **開始スライド番号**
   - `all_slides.md` の最後に追加する場合は自動計算
   - 特定の位置に挿入する場合は番号指定

### 原稿フォーマット

原稿は以下の形式を想定：

```markdown
# セクションタイトル

## トピック1のタイトル

内容の説明文。箇条書きがあればそのまま使用。

- 重要なポイント1
- 重要なポイント2
- 重要なポイント3

## トピック2のタイトル

別のトピックの説明。

---

## トピック3のタイトル

既に `---` で区切られている場合はそのまま尊重。
```

---

## Phase 2: ANALYZE 🔍（原稿解析）

### 構造の把握

1. **セクション構造の抽出**
   - H1（`# `）: セクションタイトル → lead スライド候補
   - H2（`## `）: トピックタイトル → 通常スライド候補
   - H3（`### `）: サブトピック → 同じスライド内に含める

2. **既存の分割マーカー検出**
   - `---` が既にあればその位置を記録
   - ユーザーの意図的な分割を尊重

3. **内容の分析**
   - 各トピックの文字数
   - 箇条書き項目数
   - コードブロックの有無
   - 画像・図表の参照

### 分析結果の表示

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 MANUSCRIPT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📄 Input: [ファイル名 or "pasted text"]
📏 Total: [XXXX] chars

📑 Structure Detected:
  - H1 sections: [N]
  - H2 topics: [N]
  - Existing `---`: [N]
  - Bullet lists: [N]
  - Images/Diagrams: [N]

🎯 Slide Count:
  - User target: [N] slides (or "auto")
  - Estimated: [N-M] slides

Continue? (yes/no)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 3: SPLIT ✂️（スライド分割）

### 分割戦略

#### 基本ルール

1. **既存の `---` を尊重**
   - ユーザーが明示的に分割した箇所を維持

2. **H1セクションタイトル → lead スライド**
   - セクション区切りは独立したスライド

3. **H2トピック → 1スライド（基本）**
   - ただし内容量に応じて調整

4. **適切な粒度を保つ**
   - 1スライドあたり 3-8 箇条書き項目
   - 文字数 100-500 文字が目安
   - 多すぎる場合は分割、少なすぎる場合は統合

#### 枚数調整（指定がある場合）

- **目標より少ない**: トピックを細分化
- **目標より多い**: 関連トピックを統合

### 分割結果

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✂️  SPLIT RESULT: [N] slides
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Slide #42: [Section Title] (H1)
  Type: lead candidate
  Content: 1 title

Slide #43: [Topic 1]
  Type: content
  Content: 5 bullets, 320 chars

Slide #44: [Topic 2]
  Type: content + image
  Content: 4 bullets, 280 chars, 1 image

...

Looks good? (yes/no/adjust)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4: LAYOUT 🎨（レイアウト選択）

### 利用可能なレイアウト（全15種類）

**テーマファイル**: `themes/ai-seminar.css`

#### 既存レイアウト（10種類）
1. **lead** - タイトル・セクション区切り
2. **layout-horizontal-left** - 図左55%、テキスト右45%
3. **layout-horizontal-right** - テキスト左45%、図右55%
4. **layout-diagram-only** - 図のみ最大化
5. **two-column** - 2カラムテキスト（8-18 bullets）
6. **three-column** - 3カラムテキスト（15-27 bullets）
7. **compact** - フォントサイズ縮小（≥9 bullets or ≥800 chars）
8. **two-images-horizontal** - 画像2枚横並び比較
9. **image-top-compact** - 画像上、テキスト下
10. **card-grid** - カード型2列グリッド（3-4 sections）

#### 新規レイアウト（5種類）✨
11. **layout-comparison** - 2つの概念を左右対比（vs, Before/After）
12. **layout-callout** - 重要メッセージを紫グラデーション背景で強調
13. **layout-timeline** - 3-7ステップの手順を円形番号で横並び表示
14. **layout-code-focus** - コードブロック60%、説明2列
15. **layout-split-vertical** - 画像上60%、テキスト下40%

---

### 自動レイアウト選択ロジック

各スライドの内容を分析し、最適なレイアウトを自動選択：

#### 選択優先順位

```python
def select_layout(slide_content: str) -> str:
    """
    スライド内容に基づいてレイアウトを選択

    優先順位（上から順に判定）:
    1. lead: H1のみ、セクション区切り
    2. layout-callout: 重要メッセージ強調（キーワード検出）
    3. layout-comparison: 2つの概念比較（vs, Before/After）
    4. layout-timeline: 手順・フロー（3-7ステップ）
    5. layout-code-focus: コード例メイン
    6. layout-diagram-only: 図のみ（説明最小限）
    7. layout-horizontal-*: 図 + 説明（3-8 bullets）
    8. two-column / three-column: 箇条書き数に応じて
    9. card-grid: 3-4の独立セクション
    10. compact: 内容量多い（≥9 bullets）
    11. default: 標準
    """
    analysis = analyze_content(slide_content)

    # Rule 1: lead（セクションタイトル）
    if analysis['has_h1'] and not analysis['has_h2']:
        if analysis['bullet_count'] <= 3 and analysis['total_chars'] < 150:
            return 'lead'

    # Rule 2: layout-callout（重要メッセージ強調）
    # キーワード: "重要", "原則", "必須", "警告", "注意", "キーポイント"
    if has_callout_keywords(slide_content):
        if analysis['bullet_count'] <= 6 and not analysis['has_image']:
            return 'layout-callout'

    # Rule 3: layout-comparison（比較）
    # キーワード: "vs", "VS", "対", "Before", "After", "従来", "AI時代"
    # または H3が2つ並列している構造
    if has_comparison_structure(slide_content):
        if not analysis['has_image'] and 4 <= analysis['bullet_count'] <= 16:
            return 'layout-comparison'

    # Rule 4: layout-timeline（手順・フロー）
    # キーワード: "ステップ", "フロー", "手順", "サイクル"
    # または 番号付きリスト（3-7項目）
    if has_timeline_structure(slide_content):
        if 3 <= analysis['step_count'] <= 7:
            return 'layout-timeline'

    # Rule 5: layout-code-focus（コード重視）
    if analysis['has_code_block']:
        if analysis['code_lines'] >= 10:
            return 'layout-code-focus'

    # Rule 6: layout-diagram-only（図のみ）
    if analysis['has_image']:
        if analysis['bullet_count'] <= 2:
            return 'layout-diagram-only'

    # Rule 7: layout-horizontal-*（図 + 説明）
    if analysis['has_image'] and 3 <= analysis['bullet_count'] <= 8:
        # 左右の選択は画像の重要度で決定
        if analysis['image_is_primary']:
            return 'layout-horizontal-left'  # 図を左（55%）
        else:
            return 'layout-horizontal-right'  # 図を右（55%）

    # Rule 8: two-images-horizontal（2画像比較）
    if analysis['image_count'] == 2:
        if analysis['bullet_count'] <= 4:
            return 'two-images-horizontal'

    # Rule 9: card-grid（カード型グリッド）
    if has_card_structure(slide_content):
        if 3 <= analysis['section_count'] <= 4:
            return 'card-grid'

    # Rule 10: three-column（3カラム）
    if 15 <= analysis['bullet_count'] <= 27:
        return 'three-column'

    # Rule 11: two-column（2カラム）
    if 8 <= analysis['bullet_count'] <= 18:
        return 'two-column'

    # Rule 12: compact（コンテンツ量多い）
    if analysis['bullet_count'] >= 9 or analysis['total_chars'] >= 800:
        return 'compact'

    # Rule 13: image-top-compact（画像上、説明下）
    if analysis['has_image']:
        if 3 <= analysis['bullet_count'] <= 6:
            return 'image-top-compact'

    # Rule 14: layout-split-vertical（画像上60%、説明下40%）
    if analysis['has_large_image']:
        if analysis['bullet_count'] <= 5:
            return 'layout-split-vertical'

    # Rule 15: default（標準）
    return None  # Marpデフォルト
```

#### 検出ヘルパー関数

```python
def has_callout_keywords(content: str) -> bool:
    """重要メッセージ強調のキーワードを検出"""
    keywords = ['重要', '原則', '必須', '警告', '注意', 'キーポイント',
                '⚠️', '💡', '🔒', '✅', 'IMPORTANT', 'WARNING']
    return any(kw in content for kw in keywords)

def has_comparison_structure(content: str) -> bool:
    """比較構造を検出"""
    # キーワードベース
    comparison_keywords = ['vs', 'VS', '対', 'Before', 'After', '従来', 'AI時代']
    if any(kw in content for kw in comparison_keywords):
        return True

    # H3が2つ並列しているパターン
    h3_count = content.count('### ')
    return h3_count == 2

def has_timeline_structure(content: str) -> bool:
    """タイムライン・フロー構造を検出"""
    timeline_keywords = ['ステップ', 'STEP', 'フロー', '手順', 'サイクル',
                         'Phase', 'プロセス']
    return any(kw in content for kw in timeline_keywords)

def has_card_structure(content: str) -> bool:
    """カード型構造を検出"""
    # H3が3-4個あり、それぞれに箇条書きがある
    h3_count = content.count('### ')
    return 3 <= h3_count <= 4

def analyze_content(slide_content: str) -> dict:
    """スライド内容を詳細分析"""
    return {
        'has_h1': '# ' in slide_content,
        'has_h2': '## ' in slide_content,
        'has_image': '![' in slide_content,
        'has_code_block': '```' in slide_content,
        'image_count': slide_content.count('!['),
        'bullet_count': slide_content.count('\n- ') + slide_content.count('\n* '),
        'section_count': slide_content.count('### '),
        'step_count': count_numbered_steps(slide_content),
        'code_lines': count_code_lines(slide_content),
        'total_chars': len(slide_content),
        'has_large_image': 'height:' in slide_content or 'width:1000' in slide_content,
        'image_is_primary': estimate_image_importance(slide_content),
    }
```

### レイアウト選択結果

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 LAYOUT SELECTION (15 layouts available)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Slide #42: lead
  → H1のみ、セクション区切り

Slide #43: layout-callout ✨
  → 重要メッセージ強調 (キーワード: "原則" 検出)

Slide #44: layout-comparison ✨
  → 2つの概念比較 (キーワード: "vs" 検出, 12 bullets)

Slide #45: layout-timeline ✨
  → 手順フロー (5 steps 検出)

Slide #46: layout-code-focus ✨
  → コード重視 (25 code lines)

Slide #47: layout-horizontal-left
  → 画像 + 説明 (4 bullets, 1 image)

Slide #48: two-column
  → 2カラムテキスト (10 bullets)

Slide #49: compact
  → 箇条書き多数 (12 bullets, 650 chars)

Slide #50: (default)
  → 標準テキスト (5 bullets, 320 chars)

...

Summary:
  - lead: 1 slide
  - layout-callout: 2 slides ✨
  - layout-comparison: 3 slides ✨
  - layout-timeline: 2 slides ✨
  - layout-code-focus: 1 slide ✨
  - layout-horizontal-left: 4 slides
  - two-column: 3 slides
  - compact: 2 slides
  - default: 7 slides

New Layouts: 8 slides (32%)
Traditional Layouts: 17 slides (68%)

Layouts OK? (yes/no/adjust)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 5: SCAFFOLD 📝（骨組み生成）

### スライドの骨組み作成

各スライドの最小限の骨組みを生成：

#### lead スライド

```markdown
---

<!-- _class: lead -->

# [セクションタイトル]

## [サブタイトル（あれば）]

<!-- TODO: /slide-tdd で詳細化 -->

---
```

#### 通常スライド（default）

```markdown
---

# [スライドタイトル]

- [箇条書き項目1]
- [箇条書き項目2]
- [箇条書き項目3]

<!-- TODO: /slide-tdd で内容充実・SVG追加 -->

---
```

#### 画像付きスライド（horizontal-left）

```markdown
---

<!-- _class: layout-horizontal-left -->

# [スライドタイトル]

![width:900px](diagrams/diagram_XX_placeholder.svg)

- [箇条書き項目1]
- [箇条書き項目2]
- [箇条書き項目3]

<!-- TODO: /slide-tdd でSVG作成 -->
<!-- SVG内容: [図表の説明] -->

---
```

#### compact スライド

```markdown
---

<!-- _class: compact -->

# [スライドタイトル]

- [箇条書き項目1]
- [箇条書き項目2]
- [箇条書き項目3]
- [箇条書き項目4]
- [箇条書き項目5]
- [箇条書き項目6]
- [箇条書き項目7]
- [箇条書き項目8]
- [箇条書き項目9]

<!-- TODO: /slide-tdd で内容調整 -->

---
```

#### 比較スライド（layout-comparison）✨

```markdown
---

<!-- _class: layout-comparison -->

# [比較タイトル（例: Vibe Coding vs Production Engineering）]

<div>

### [左側の概念]
- [ポイント1]
- [ポイント2]
- [ポイント3]

</div>

<div>VS</div>

<div>

### [右側の概念]
- [ポイント1]
- [ポイント2]
- [ポイント3]

</div>

<!-- TODO: /slide-tdd で内容充実 -->

---
```

#### 強調メッセージスライド（layout-callout）✨

```markdown
---

<!-- _class: layout-callout -->

<div class="icon">💡</div>

# [重要な原則・メッセージ]

<div class="message">
[キーメッセージを1文で]
</div>

- [補足ポイント1]
- [補足ポイント2]
- [補足ポイント3]

<!-- TODO: /slide-tdd で詳細化 -->

---
```

#### タイムラインスライド（layout-timeline）✨

```markdown
---

<!-- _class: layout-timeline -->

# [手順・フローのタイトル]

<div class="timeline">

<div class="step">
<div class="step-number">1</div>
<h3>[ステップ名]</h3>
<p>[簡潔な説明]</p>
</div>

<div class="step">
<div class="step-number">2</div>
<h3>[ステップ名]</h3>
<p>[簡潔な説明]</p>
</div>

<div class="step">
<div class="step-number">3</div>
<h3>[ステップ名]</h3>
<p>[簡潔な説明]</p>
</div>

<!-- 3-7ステップを配置 -->

</div>

<!-- TODO: /slide-tdd で詳細化 -->

---
```

#### コード重視スライド（layout-code-focus）✨

```markdown
---

<!-- _class: layout-code-focus -->

# [コード例のタイトル]

\`\`\`[言語]
[コード例を記載]
\`\`\`

<div class="notes">

<div>
<h3>[左側の説明]</h3>
- [ポイント1]
- [ポイント2]
</div>

<div>
<h3>[右側の説明]</h3>
- [ポイント1]
- [ポイント2]
</div>

</div>

<!-- TODO: /slide-tdd でコード例と説明を充実 -->

---
```

#### 上下分割スライド（layout-split-vertical）✨

```markdown
---

<!-- _class: layout-split-vertical -->

<div class="image-area">
![アーキテクチャ図](diagrams/diagram_XX_placeholder.svg)
</div>

<div class="content-area">

# [スライドタイトル]

- [ポイント1]
- [ポイント2]
- [ポイント3]

</div>

<!-- TODO: /slide-tdd でSVG作成 -->
<!-- SVG内容: [図表の説明] -->

---
```

### TODOコメントの活用

各スライドに以下の情報をTODOコメントとして記録：

- `/slide-tdd` で実施すべき作業
- SVG図表が必要な場合はその内容
- 重要なポイントや注意事項

---

## Phase 6: OUTPUT 📤（出力）

### all_slides.md への追加

生成した骨組みを `all_slides.md` の適切な位置に追加：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 OUTPUT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Generated 25 slide scaffolds
📄 Added to: all_slides.md (slides #42-#66)

Layout Distribution:
  Traditional Layouts:
    - lead: 1 slide (#42)
    - layout-horizontal-left: 4 slides (#47, #51, #55, #59)
    - two-column: 3 slides (#48, #52, #62)
    - compact: 2 slides (#49, #63)
    - default: 7 slides (#50, #53, #57, #60, #64, #65, #66)

  New Layouts ✨:
    - layout-callout: 2 slides (#43, #56)
    - layout-comparison: 3 slides (#44, #54, #61)
    - layout-timeline: 2 slides (#45, #58)
    - layout-code-focus: 1 slide (#46)

  New Layout Coverage: 8/25 slides (32%)

📋 Next Steps:
  For each slide, run /slide-tdd to:
  1. Define acceptance criteria
  2. Create SVG diagrams (where needed)
  3. Refine content with new layouts
  4. Measure and improve quality

🎨 Theme: themes/ai-seminar.css (15 layouts available)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to start with /slide-tdd? (yes/no)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### TODO リストの生成

生成されたスライドのTODOリストを作成：

```markdown
## Slide Generation TODO List

### Slides Needing /slide-tdd

#### Section & New Layouts (High Priority)
- [ ] Slide #42: [セクションタイトル] (lead)
- [ ] Slide #43: [重要原則] (layout-callout) ✨ - **New layout**
- [ ] Slide #44: [比較] (layout-comparison) ✨ - **New layout**
- [ ] Slide #45: [手順] (layout-timeline) ✨ - **New layout**
- [ ] Slide #46: [コード例] (layout-code-focus) ✨ - **New layout**

#### Traditional Layouts with SVG
- [ ] Slide #47: [トピック1] (horizontal-left) - **SVG needed**
- [ ] Slide #51: [トピック2] (horizontal-left) - **SVG needed**
- [ ] Slide #55: [トピック3] (horizontal-left) - **SVG needed**
- [ ] Slide #59: [トピック4] (horizontal-left) - **SVG needed**

#### Content Slides
- [ ] Slide #48: [トピック5] (two-column)
- [ ] Slide #49: [トピック6] (compact)
- [ ] Slide #50: [トピック7] (default)
- [ ] Slide #52: [トピック8] (two-column)
- [ ] Slide #53: [トピック9] (default)

### Priority

1. **High**: New layout slides (#43-#46) - Learn and test new layouts
2. **High**: Section slides (#42) - Define overall structure
3. **Medium**: SVG diagram slides (#47, #51, #55, #59) - Time-consuming
4. **Normal**: Content slides - Standard refinement

### New Layout Focus

新規レイアウト（✨）のスライドは特に注意して作成：
- layout-callout: アイコンとメッセージの選定
- layout-comparison: 左右の対比を明確に
- layout-timeline: ステップ数を3-7に調整
- layout-code-focus: コード例の読みやすさ重視
```

---

## 🎯 /slide-tdd との連携フロー

### ステップ1: 骨組み生成

```bash
/generate-slides
```

→ 9スライドの骨組みが生成される

### ステップ2: 各スライドを詳細化

```bash
# Slide #42 (lead)
/slide-tdd

# Slide #43 (default)
/slide-tdd

# Slide #44 (horizontal-left, SVG needed)
/slide-tdd
# → PLAN: SVG内容を明確化
# → RED: 判定処理作成
# → GREEN: SVG作成
# → REFACTOR: 品質向上
# → VERIFY: 最終確認

# ... 以下同様に各スライドを処理
```

### ステップ3: 全体確認

```bash
# すべてのスライドの品質チェック
python3 validate_svg_bounds.py

# Marpでレンダリング
npx @marp-team/marp-cli all_slides.md -o index.html --html

# ブラウザで確認
open index.html
```

---

## 💡 ベストプラクティス

### 1. 段階的な作成

```
/generate-slides  (骨組み一括生成)
    ↓
/slide-tdd × N   (各スライドを個別に詳細化)
    ↓
全体調整         (一貫性チェック、最終調整)
```

### 2. 優先順位をつける

1. **セクションスライド（lead）を先に**
   - 全体構造が明確になる

2. **SVGが必要なスライドを次に**
   - 時間がかかるので早めに着手

3. **残りのスライドを順次処理**
   - コンテンツの流れに沿って作成

### 3. 一貫性を保つ

- 同じセクション内のスライドは連続して作成
- レイアウトの使い方を統一
- 用語・表現を統一

### 4. こまめにコミット

```bash
# 骨組み生成後
git add all_slides.md
git commit -m "feat: Generate slide scaffolds (#42-#50)"

# 各スライド完成後
git add all_slides.md diagrams/
git commit -m "feat: Complete slide #44 with SVG diagram"
```

---

## 🎯 使い方

### 基本的な使い方

```bash
/generate-slides
```

1. 原稿テキストを入力
2. スライド枚数を指定（オプション）
3. 分割・レイアウト選択を確認
4. 骨組みが生成される
5. `/slide-tdd` で各スライドを詳細化

### 使用例

#### 例1: 新規原稿から骨組み生成

```
User: /generate-slides

Assistant: I'll help you generate slide scaffolds. First, let me gather some information.

📄 Manuscript source:
🎯 Target slide count (optional):
#️⃣ Starting slide number:

User: Here's my text, please generate 5 slides starting from slide #42.

Assistant:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[After analysis and confirmation, scaffolds are generated]

📊 MANUSCRIPT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```

#### 例2: 既存ファイルから自動生成

```
User: /generate-slides

Assistant: Please provide the path to your manuscript file.

User: manuscript/chapter3.md

Assistant: I'll analyze manuscript/chapter3.md and generate slide scaffolds.

[Process continues as in Example 1]
```

---

## 📝 まとめ

### このコマンドの役割

`/generate-slides` は:
- ✅ 原稿から**骨組み**（scaffold）を生成
- ✅ 適切な粒度でスライドを分割
- ✅ 最適なレイアウトを自動選択
- ✅ `/slide-tdd` と緊密に連携

### 次のステップ

骨組み生成後は、各スライドに対して `/slide-tdd` を実行：

```bash
# 生成されたスライドごとに
/slide-tdd  # PLAN → RED → GREEN → REFACTOR → VERIFY
```

この2段階アプローチにより：
- 全体構造を先に決定
- 各スライドの品質を個別に向上
- 一貫性のある高品質なスライドセットを作成

---

**作成者**: Claude Code
**バージョン**: 1.0
**連携コマンド**: `/slide-tdd`
