# Layout Selection Cheat Sheet

## Quick Decision Matrix

| Bullets | Image? | Layout | Column Width |
|---------|--------|--------|--------------|
| 0-4 | No | `default` | 1100px |
| 0-4 | Yes | `layout-diagram-only` | Full |
| 5-7 | No | `default` | 1100px |
| 5-8 | Yes | `layout-horizontal-*` | 536px |
| 8-14 | No | `two-column` | 600px |
| 15-18 | No | `two-column` or `three-column` | 600px / 400px |
| 19-27 | No | `three-column` | 400px |
| 27+ | - | **SPLIT SLIDE** | - |
| 3-4 sections | No | `card-grid` | 350px |

## Character Limits (16px font)

| Layout | English | Japanese | Mixed |
|--------|---------|----------|-------|
| `default` | ~110 | ~60 | ~85 |
| `two-column` | ~60 | ~33 | ~47 |
| `three-column` | ~40 | ~22 | ~31 |
| `horizontal-*` | ~54 | ~30 | ~42 |
| `card-grid` | ~35 | ~19 | ~27 |

## Layout Syntax

```markdown
<!-- _class: LAYOUT_NAME -->
```

Available layouts:
- `default` (no class needed)
- `lead`
- `two-column`
- `three-column`
- `layout-horizontal-left` (image 55% left)
- `layout-horizontal-right` (image 55% right)
- `layout-diagram-only`
- `card-grid`
- `image-top-compact`

## Common Patterns

### Title Slide
```markdown
---
<!-- _class: lead -->
# Main Title
Subtitle
---
```

### Two-Column List
```markdown
---
<!-- _class: two-column -->
# Title

**Left:**
- Point 1
- Point 2

**Right:**
- Point 3
- Point 4
---
```

### Diagram with Text
```markdown
---
<!-- _class: layout-horizontal-left -->
# Title

![Diagram](diagrams-web/diagram.svg)

- Point 1
- Point 2
- Point 3
---
```

### Three-Column Dense
```markdown
---
<!-- _class: three-column -->
# Title

**Col 1:**
- Item 1
- Item 2
- Item 3

**Col 2:**
- Item 4
- Item 5
- Item 6

**Col 3:**
- Item 7
- Item 8
- Item 9
---
```

## Red Flags 🚩

- ❌ Horizontal layout without image → Use `two-column`
- ❌ > 18 bullets in `two-column` → Use `three-column`
- ❌ > 27 bullets in any layout → Split into multiple slides
- ❌ < 8 bullets in `three-column` → Use `two-column` or `default`
- ❌ Text > column width → Shorten or split line

## Testing Commands

```bash
# Check overflow
python3 analyze_actual_text_width_fixed.py

# Review layouts
python3 comprehensive_layout_review.py

# Build slides
npx @marp-team/marp-cli@latest all_slides.md -o index.html --html --no-stdin
```

## Width Calculation Formula

```
Effective Width = Column Width - 40px (margin)

Character Count ≈ Effective Width / Char Width
  - English: char_width = 8.8px (0.55 × 16px)
  - Japanese: char_width = 16px (1.0 × 16px)
  - Emoji: char_width = 24px (1.5 × 16px)
```

## When to Split a Slide

Split if ANY of these are true:
- More than 27 bullets
- Content covers multiple sub-topics
- Slide feels cramped visually
- Text overflows despite layout optimization
- Audience would need > 2 minutes to read

## Layout Priority Hierarchy

1. **Bullet count** (primary driver)
2. **Image presence** (horizontal if yes + 5-8 bullets)
3. **Content structure** (cards → card-grid, sections → columns)
4. **Text length** (long text needs wider columns)
5. **Visual hierarchy** (title/separator → lead/default)
