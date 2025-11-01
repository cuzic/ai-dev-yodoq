# Layout Selection Guide

## Overview

This guide helps you choose the optimal layout for your Marp slides based on content type, bullet count, and visual requirements.

## Available Layouts

| Layout | Column Width | Best For | Bullet Range |
|--------|--------------|----------|--------------|
| `default` | 1100px | Title slides, separators, full-width content | N/A |
| `lead` | Full width | Cover slides, section dividers | N/A |
| `two-column` | 600px | Medium lists, balanced content | 8-18 bullets |
| `three-column` | 400px | Long lists, compact organization | 15-27 bullets |
| `layout-horizontal-left` | 536px | Image on left (55%), text on right (45%) | 5-8 bullets |
| `layout-horizontal-right` | 536px | Text on left (45%), image on right (55%) | 5-8 bullets |
| `layout-diagram-only` | Full width | Large diagrams, visual-only slides | N/A |
| `card-grid` | 350px | Card-based sections, 3-4 items | 3-4 sections |
| `image-top-compact` | Variable | Image above, compact text below | Variable |

## Selection Criteria

### 1. Default Layout

**Use when:**
- Creating title slides or section dividers
- Displaying full-width content without columns
- Showing large code blocks
- Content is minimal (1-4 items)

**Example:**
```markdown
---

# Section Title

Brief introduction text or single concept.

---
```

**Character limits:**
- Max ~110 chars per line (1100px width)
- Use for short, impactful statements

---

### 2. Lead Layout

**Use when:**
- Creating the cover slide
- Major section transitions
- Emphasizing key messages

**Example:**
```markdown
---

<!-- _class: lead -->

# Main Title

Subtitle or tagline

---
```

**Best practices:**
- Keep text minimal and centered
- Use for high-impact moments
- 1-3 lines of text maximum

---

### 3. Two-Column Layout

**Use when:**
- 8-18 bullet points need organization
- Content can be logically split into 2 groups
- Each bullet is moderately long (30-60 chars)

**Example:**
```markdown
---

<!-- _class: two-column -->

# Feature Comparison

**Left Category:**
- Point 1
- Point 2
- Point 3

**Right Category:**
- Point 4
- Point 5
- Point 6

---
```

**Character limits:**
- Max ~60 chars per line (600px column width)
- Ideal: 40-55 chars for comfortable reading

**Decision tree:**
- < 8 bullets → Use `default` layout
- 8-18 bullets → Use `two-column`
- > 18 bullets → Use `three-column`

---

### 4. Three-Column Layout

**Use when:**
- 15-27 bullet points need organization
- Content has 3 natural categories
- Space efficiency is important
- Each bullet is concise (20-40 chars)

**Example:**
```markdown
---

<!-- _class: three-column -->

# Comprehensive Feature List

**Column 1:**
- Feature A
- Feature B
- Feature C
- Feature D
- Feature E

**Column 2:**
- Feature F
- Feature G
- Feature H
- Feature I

**Column 3:**
- Feature J
- Feature K
- Feature L
- Feature M

---
```

**Character limits:**
- Max ~40 chars per line (400px column width)
- Ideal: 25-35 chars for comfortable reading
- Japanese/CJK: ~20-25 characters

**Warning signs:**
- If bullets exceed 40 chars → split text or use `two-column`
- If > 27 bullets → split into multiple slides

---

### 5. Horizontal Layouts (Left/Right)

**Use when:**
- Showing a diagram WITH explanatory text
- Image and text have equal importance
- Text complements the visual (5-8 bullets)
- Need side-by-side comparison

**Example (horizontal-left):**
```markdown
---

<!-- _class: layout-horizontal-left -->

# Diagram with Explanation

![Architecture Diagram](diagrams-web/diagram.svg)

- **Point 1:** Brief explanation
- **Point 2:** Another point
- **Point 3:** Key insight
- **Point 4:** Final note

---
```

**Character limits:**
- Max ~54 chars per line (536px column width)
- Ideal: 35-50 chars for comfortable reading
- Japanese/CJK: ~27-32 characters

**Layout choice:**
- `layout-horizontal-left`: Image takes visual priority (55% width)
- `layout-horizontal-right`: Text takes visual priority (55% width)

**Common mistakes:**
- ❌ Using horizontal layout without an image
- ❌ Adding > 8 bullets (makes text cramped)
- ❌ Lines > 536px (will overflow)

---

### 6. Layout-Diagram-Only

**Use when:**
- Diagram is self-explanatory
- No additional text needed
- Maximum visual impact desired
- Complex diagram needs full screen

**Example:**
```markdown
---

<!-- _class: layout-diagram-only -->

![Complex System Architecture](diagrams-web/large_diagram.svg)

---
```

**Best practices:**
- Diagram should be high resolution
- Include title in the diagram itself if needed
- Use for flow charts, architecture diagrams, process maps

---

### 7. Card-Grid Layout

**Use when:**
- Presenting 3-4 distinct sections/cards
- Each section has a title and 2-5 bullets
- Content is modular and independent
- Visual separation is important

**Example:**
```markdown
---

<!-- _class: card-grid -->

# Four Key Areas

### Area 1
- Point 1
- Point 2
- Point 3

### Area 2
- Point 1
- Point 2
- Point 3

### Area 3
- Point 1
- Point 2

### Area 4
- Point 1
- Point 2
- Point 3

---
```

**Character limits:**
- Max ~35 chars per line (350px card width)
- Ideal: 20-30 chars for comfortable reading

**Best practices:**
- Use `###` for card titles
- Keep cards balanced (similar content amounts)
- 3-4 cards is optimal (2 or 5+ may look unbalanced)

---

### 8. Image-Top-Compact

**Use when:**
- Image is primary, text is supplementary
- Need compact text below image
- Image doesn't need full width
- 2-6 bullets of context

**Example:**
```markdown
---

<!-- _class: image-top-compact -->

![Screenshot or Photo](diagrams-web/example.svg)

- Brief caption or explanation
- Additional context
- Related information

---
```

**Best practices:**
- Keep text minimal (2-6 lines)
- Image should be landscape orientation
- Use for screenshots, photos, UI mockups

---

## Decision Flow Chart

```
START
  │
  ├─ Is this a title/separator slide?
  │    └─ YES → Use `default` or `lead`
  │
  ├─ Is this diagram-only?
  │    └─ YES → Use `layout-diagram-only`
  │
  ├─ Do you have an image AND text?
  │    └─ YES → Is text 5-8 bullets?
  │         ├─ YES → Use `layout-horizontal-left/right`
  │         └─ NO → Use different layout
  │
  ├─ How many bullet points do you have?
  │    ├─ 1-7 bullets → Use `default`
  │    ├─ 8-18 bullets → Use `two-column`
  │    ├─ 15-27 bullets → Use `three-column`
  │    └─ 27+ bullets → SPLIT INTO MULTIPLE SLIDES
  │
  └─ Do you have 3-4 distinct sections?
       └─ YES → Use `card-grid`
```

---

## Character Limit Quick Reference

### By Language

**English/ASCII characters:**
- Width multiplier: 0.55x font size
- Default font: 16px
- Effective width per char: ~8.8px

**Japanese/CJK characters:**
- Width multiplier: 1.0x font size
- Default font: 16px
- Effective width per char: ~16px

**Emojis:**
- Width multiplier: 1.5x font size
- Default font: 16px
- Effective width per char: ~24px

### Practical Limits (16px font, with 40px margin)

| Layout | Column Width | Max English Chars | Max Japanese Chars | Max Mixed (50/50) |
|--------|--------------|-------------------|--------------------|--------------------|
| `default` | 1100px | ~110 | ~60 | ~85 |
| `two-column` | 600px | ~60 | ~33 | ~47 |
| `three-column` | 400px | ~40 | ~22 | ~31 |
| `layout-horizontal-*` | 536px | ~54 | ~30 | ~42 |
| `card-grid` | 350px | ~35 | ~19 | ~27 |

**Formula:**
```
Available Width = Column Width - Margin (40px)
Max Chars = Available Width / (char_width_multiplier * font_size)
```

---

## Common Mistakes and Solutions

### Mistake 1: Too Many Bullets in Two-Column

**Problem:**
```markdown
<!-- _class: two-column -->

# Long List
- Item 1
- Item 2
...
- Item 25  ❌ Too many!
```

**Solution:**
Use `three-column` or split into multiple slides.

---

### Mistake 2: Text Overflow in Horizontal Layout

**Problem:**
```markdown
<!-- _class: layout-horizontal-left -->

- This is a very long line with lots of technical details and explanations ❌ Overflow!
```

**Solution:**
Shorten text or split into multiple bullets:
```markdown
- Technical details summary
  - Sub-point with specifics
  - Another sub-point
```

---

### Mistake 3: Using Horizontal Layout Without Image

**Problem:**
```markdown
<!-- _class: layout-horizontal-left -->

# Title

- Bullet 1
- Bullet 2
- Bullet 3
❌ No image!
```

**Solution:**
Use `two-column` or `default` layout instead.

---

### Mistake 4: Too Few Bullets in Multi-Column

**Problem:**
```markdown
<!-- _class: three-column -->

# Sparse Content

- Only 3 bullets total  ❌ Wasteful!
```

**Solution:**
Use `default` layout for < 8 bullets.

---

## Testing Your Layout

### 1. Run Overflow Detection

```bash
cd slides
python3 analyze_actual_text_width_fixed.py
```

This will show:
- Which slides have overflow
- Exact line width in pixels
- How much overflow (px over limit)

### 2. Visual Inspection

Build and preview:
```bash
npx @marp-team/marp-cli@latest all_slides.md -o index.html --html --no-stdin
# Open index.html in browser
```

Look for:
- Text cutting off at column edges
- Unbalanced columns (one much longer)
- Excessive white space
- Cramped appearance

### 3. Content Density Check

```bash
python3 comprehensive_layout_review.py
```

This shows:
- Layout usage statistics
- Slides with too many/few bullets for layout
- Suggestions for layout changes

---

## Layout Optimization Workflow

1. **Write content first** (don't worry about layout)
2. **Count bullets** in your slide
3. **Check for images** (do you have diagrams?)
4. **Apply layout** based on decision tree above
5. **Run overflow detection** script
6. **Adjust text or layout** if needed
7. **Visual review** in browser
8. **Iterate** until perfect

---

## Real-World Examples from This Presentation

### Example 1: Perfect Two-Column (Slide 149)

```markdown
<!-- _class: two-column -->

# AIがドキュメント生成

**ドキュメント自動生成:**
- APIドキュメント (Swagger/OpenAPI)
- アーキテクチャ図 (Mermaid)
- READMEとセットアップ手順
- 運用マニュアル

**ドキュメント改善AI:**
- 既存ドキュメント読み込み→改善
- 一貫性チェック
- 翻訳（多言語対応）
```

**Why it works:**
- 12 bullets (perfect for two-column)
- Clear left/right categories
- Each line < 60 chars
- Balanced content distribution

---

### Example 2: Perfect Horizontal-Left (Slide 7)

```markdown
<!-- _class: layout-horizontal-left -->

# 5-STEPフロー全体像

![5-STEP全体フロー](diagrams-web/diagram_2_five_step_flow.svg)

- **1. Decompose（分解）:** 問題→小タスク
- **2. Implement:** AIに実装させる
- **3. Test:** TDD必須
- **4. Review:** AI自己レビュー
- **5. Knowledge:** 学習ループ
```

**Why it works:**
- Image on left (55% width) provides visual anchor
- 5 bullets on right (perfect for horizontal)
- Each line < 54 chars
- Text complements diagram

---

### Example 3: Perfect Three-Column (Slide 10)

```markdown
<!-- _class: three-column -->

# Decompose（分解）の具体例

**入力（曖昧な要望）:**
- 「ユーザー登録機能」

**AIによる分解結果:**
1. DB設計
2. バリデーション
3. パスワードハッシュ
4. メール送信
5. エラーハンドリング
6. テストコード
... (19 items total)
```

**Why it works:**
- 19 bullets (perfect for three-column)
- Natural 3-category split
- Each line < 40 chars
- Space-efficient

---

## Migration Guide

If you have existing slides with wrong layouts:

### From Default → Two-Column

**When:** 8-18 bullets, no layout specified

```markdown
# Before
---
# Title
- Bullet 1
- Bullet 2
...
- Bullet 12

# After
---
<!-- _class: two-column -->
# Title
- Bullet 1
- Bullet 2
...
- Bullet 12
```

### From Two-Column → Three-Column

**When:** > 18 bullets in two-column

```markdown
# Before
---
<!-- _class: two-column -->
# Title
(20 bullets)  ❌ Too many

# After
---
<!-- _class: three-column -->
# Title
(20 bullets)  ✅ Perfect fit
```

### From Horizontal → Two-Column

**When:** Horizontal layout without image

```markdown
# Before
---
<!-- _class: layout-horizontal-left -->
# Title
(No image, just bullets)  ❌ Wrong layout

# After
---
<!-- _class: two-column -->
# Title
(Same bullets)  ✅ Correct layout
```

---

## Summary

### Quick Rules of Thumb

1. **Bullet count drives layout:**
   - 1-7 → default
   - 8-18 → two-column
   - 15-27 → three-column
   - 27+ → split slide

2. **Image + text = horizontal layout**
   - Must have image
   - Keep text to 5-8 bullets
   - Each line < 536px

3. **Width limits matter:**
   - Always leave 40px margin
   - Test with overflow detection script
   - Japanese text takes 2x width of English

4. **When in doubt:**
   - Start with `default`
   - Add layout as content grows
   - Test early, test often

---

## Tools and Scripts

- `analyze_actual_text_width_fixed.py` - Detect overflow
- `comprehensive_layout_review.py` - Layout statistics
- `analyze_layout_fit.py` - Content vs layout analysis
- `check_svg_layout_mismatch.py` - SVG aspect ratio check

All scripts available in `/slides/` directory.

---

## Support

For issues or questions:
- Review this guide
- Run analysis scripts
- Check `LAYOUT_REVIEW_SUMMARY.md`
- See `OVERFLOW_DETECTION_BUGS_FIXED.md` for common pitfalls

---

## NEW: 4つの特殊レイアウト（2025-10-31追加）

### layout-comparison（比較レイアウト）

**用途:** 2つの概念を左右で対比表示

**最適:** Before/After、vs比較、アプローチ比較

**仕様:**
- 左右に色分け（青/オレンジ）
- 中央に「VS」表示
- 各側に独立した背景色

**使用例:**
```markdown
<!-- _class: layout-comparison -->

# タイトル

<div>
### 左側の内容
- Point 1
- Point 2
</div>

<div>VS</div>

<div>
### 右側の内容  
- Point 1
- Point 2
</div>
```

**Character limits:**
- 各側: ~30-40 chars per line
- 5-8 bullets per side

---

### layout-callout（強調メッセージレイアウト）

**用途:** 重要な原則・警告を大きく強調

**最適:** キーメッセージ、注意事項、重要原則

**仕様:**
- グラデーション背景（紫系）
- 大きなアイコン
- 白文字で視認性高

**使用例:**
```markdown
<!-- _class: layout-callout -->

<div class="icon">💡</div>

# タイトル

<div class="message">
重要なメッセージ
</div>

- Point 1
- Point 2
- Point 3
```

**Character limits:**
- Message: ~40-60 chars
- 最大6 bullets

---

### layout-timeline（タイムラインレイアウト）

**用途:** 手順・フローを横並びで表示

**最適:** 3-7ステップの手順、プロセス説明

**仕様:**
- ステップを円形番号で表示
- 横一列に矢印ラインで接続
- 各ステップに説明追加可能

**使用例:**
```markdown
<!-- _class: layout-timeline -->

# タイトル

<div class="timeline">

<div class="step">
<div class="step-number">1</div>
<h3>ステップ名</h3>
<p>説明</p>
</div>

<div class="step">
<div class="step-number">2</div>
<h3>ステップ名</h3>
<p>説明</p>
</div>

<!-- 3-7ステップ -->

</div>
```

**Step limits:**
- 最適: 3-7 steps
- 各ステップ: ~20 chars title + ~40 chars description

---

### layout-code-focus（コード重視レイアウト）

**用途:** コードを大きく表示し説明を添える

**最適:** コード例、プロンプト例、実装パターン

**仕様:**
- コードが画面の60%
- 下部に2列で説明
- シンタックスハイライト対応

**使用例:**
```markdown
<!-- _class: layout-code-focus -->

# タイトル

\`\`\`
コード例
\`\`\`

<div class="notes">

<div>
### 左側の説明
- Point 1
- Point 2
</div>

<div>
### 右側の説明
- Point 1
- Point 2
</div>

</div>
```

**Content limits:**
- Code: 最大20-30行
- 各説明側: 3-5 bullets

---

## 新レイアウト使い分けガイド

| 状況 | 推奨レイアウト |
|------|--------------|
| 2つの概念を対比したい | `layout-comparison` |
| 重要メッセージを印象的に | `layout-callout` |
| 3-7ステップの手順を示したい | `layout-timeline` |
| コード例を大きく見せたい | `layout-code-focus` |
| 2つ+画像を対比したい | `layout-horizontal-*` |
| 8-18 bullets | `two-column` |
| 15-27 bullets | `three-column` |

詳細な使用例は `NEW_LAYOUT_EXAMPLES.md` を参照してください。

