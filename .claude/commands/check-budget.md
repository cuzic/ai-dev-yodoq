---
description: Calculate optimal content budgets for each slide layout using slidectl
---

# Content Budget Calculation with slidectl

You are an expert at calculating optimal content budgets for slides. Use slidectl's budget command to determine the maximum lines and characters that fit within each layout type.

## Overview

slidectl calculates content budgets based on:
- Layout type (lead, two-column, card-grid, etc.)
- Font size class (normal, compact, supercompact, ultracompact)
- Viewport dimensions (1280x720)
- Typography constraints (line height, padding, margins)
- Safe area boundaries (1216x656)

## Workflow

### STEP 1: Calculate Budgets for All Layouts

Run budget calculation:

```bash
cd ~/slidectl
uv run slidectl budget --ws /home/cuzic/ai-dev-yodoq
```

This generates `.state/budget/layout_budgets.json` with budgets for all layout combinations.

### STEP 2: Review Budget Table

Display formatted budget table:

```bash
cat .state/budget/layout_budgets.json | jq -r '
  ["Layout", "Font", "Max Lines", "Chars/Line", "Total Chars"] as $headers |
  $headers, (["---"] * 5) |
  @tsv,
  (.budgets[] |
    [.layout, .font_class, .max_lines, .chars_per_line, .total_chars] |
    @tsv
  )
' | column -t -s $'\t'
```

**Example output:**
```
Layout                   Font          Max Lines  Chars/Line  Total Chars
---                      ---           ---        ---         ---
lead                     normal        8          40          320
lead                     compact       10         45          450
lead                     supercompact  12         52          624
two-column               normal        15         35          525
two-column               compact       18         40          720
two-column               supercompact  22         46          1012
card-grid                normal        12         38          456
card-grid                compact       14         43          602
layout-horizontal-left   normal        10         30          300
layout-horizontal-left   compact       12         34          408
layout-diagram-only      normal        5          50          250
layout-diagram-only      compact       6          56          336
```

### STEP 3: Analyze Current Slide Usage

Compare actual content against budgets:

```bash
cd ~/slidectl
uv run slidectl budget --ws /home/cuzic/ai-dev-yodoq \
  --analyze /home/cuzic/ai-dev-yodoq/slides/all_slides.md
```

This generates `.state/budget/usage_analysis.json` showing:
- Current line count per slide
- Current character count per slide
- Budget compliance (within/over budget)
- Suggested font class adjustments

**Example analysis:**

```json
{
  "slide_number": 41,
  "layout": "two-column",
  "font_class": "normal",
  "budget": {
    "max_lines": 15,
    "chars_per_line": 35,
    "total_chars": 525
  },
  "actual": {
    "lines": 22,
    "avg_chars_per_line": 42,
    "total_chars": 924
  },
  "compliance": "OVER_BUDGET",
  "overflow_by": {
    "lines": 7,
    "chars": 399
  },
  "suggestions": [
    {
      "action": "apply_compact",
      "new_budget": {
        "max_lines": 18,
        "total_chars": 720
      },
      "expected_compliance": "STILL_OVER"
    },
    {
      "action": "apply_supercompact",
      "new_budget": {
        "max_lines": 22,
        "total_chars": 1012
      },
      "expected_compliance": "WITHIN_BUDGET"
    },
    {
      "action": "reduce_content",
      "target_reduction": "30%",
      "target_chars": 650
    }
  ]
}
```

### STEP 4: Generate Budget Report for Specific Layout

Get detailed budget info for a specific layout:

```bash
cd ~/slidectl
uv run slidectl budget --ws /home/cuzic/ai-dev-yodoq \
  --layout two-column \
  --font-class compact
```

**Output:**
```
Content Budget: two-column + compact
====================================

Viewport: 1280x720
Safe Area: 1216x656
Usable Width: 90% (1094px)
Usable Height: 85% (612px)

Font Specifications:
  Font Size: 16px
  Line Height: 1.4 (22.4px)
  Columns: 2
  Column Gap: 40px

Capacity:
  Max Lines: 18 lines (27 lines per column × 2)
  Characters per Line: ~40 chars
  Total Character Budget: 720 chars

Padding & Margins:
  Top/Bottom Padding: 60px
  Left/Right Padding: 80px
  Content Area: 1094px × 612px

Recommended Usage:
  - Long text content (10+ lines)
  - Multiple paragraphs or lists
  - Natural column break points
  - No images or diagrams

Examples:
  ✅ Checklist with 12-18 items
  ✅ Multiple sections with text
  ✅ Comparison content
  ❌ Short content (5-6 lines) - use normal or different layout
  ❌ Content with images - use layout-horizontal
```

### STEP 5: Budget-Based Optimization Recommendations

Generate optimization recommendations based on budgets:

```bash
cd ~/slidectl
uv run slidectl budget --ws /home/cuzic/ai-dev-yodoq \
  --analyze /home/cuzic/ai-dev-yodoq/slides/all_slides.md \
  --recommend
```

This creates `.state/budget/optimization_recommendations.json`:

```json
{
  "summary": {
    "total_slides": 168,
    "within_budget": 145,
    "over_budget": 23,
    "compliance_rate": 86.3
  },
  "recommendations": [
    {
      "slide": 41,
      "priority": "HIGH",
      "current_overflow": "76% over budget",
      "actions": [
        {
          "type": "apply_supercompact",
          "cost": "low",
          "effectiveness": "85%",
          "side_effects": "Smaller font (14px)"
        },
        {
          "type": "reduce_content_30%",
          "cost": "medium",
          "effectiveness": "90%",
          "side_effects": "Information loss"
        }
      ],
      "recommended": "apply_supercompact + reduce_content_10%"
    },
    {
      "slide": 73,
      "priority": "MEDIUM",
      "current_overflow": "42% over budget",
      "actions": [
        {
          "type": "apply_compact",
          "cost": "low",
          "effectiveness": "70%",
          "side_effects": "Smaller font (16px)"
        }
      ],
      "recommended": "apply_compact"
    }
  ]
}
```

### STEP 6: Validate Layout Selection

Check if current layout is optimal based on content:

```bash
cd ~/slidectl
uv run slidectl budget --ws /home/cuzic/ai-dev-yodoq \
  --validate-layouts /home/cuzic/ai-dev-yodoq/slides/all_slides.md
```

**Example validation output:**

```
Layout Validation Report
========================

Slide 88: "Part 2のキーポイント"
  Current: two-column
  Content: 5 bold sections, 240 chars
  Issue: Too short for two-column (only fills 1 column)
  Recommendation: Change to card-grid
  Reason: 4-5 sections better displayed as cards

Slide 120: "STEP1: リバースエンジニアリング"
  Current: two-column compact
  Content: Header only, 35 chars
  Issue: No body content for columns
  Recommendation: Change to lead compact
  Reason: Section headers should use lead layout
```

## Budget Calculation Methodology

slidectl uses the following formula:

```python
# Base calculations
viewport_width = 1280
viewport_height = 720
safe_width = 1216  # 32px margin on each side
safe_height = 656  # 32px margin top/bottom

# Layout-specific usable area
usable_width = safe_width * layout.width_ratio  # e.g., 0.90 for two-column
usable_height = safe_height * layout.height_ratio  # e.g., 0.85

# Font metrics
font_size = get_font_size(font_class)  # normal=18px, compact=16px, etc.
line_height = font_size * get_line_height_multiplier(font_class)  # 1.4-1.6

# Capacity calculation
max_lines = usable_height / line_height
chars_per_line = (usable_width / font_size) * char_width_ratio  # ~2.2 for mixed JP/EN

# For multi-column layouts
if layout.columns > 1:
    column_width = (usable_width - (layout.columns - 1) * gap) / layout.columns
    chars_per_line = (column_width / font_size) * char_width_ratio

total_char_budget = max_lines * chars_per_line
```

## Layout-Specific Budget Guidelines

### lead (Section Headers)
- **Purpose**: Title slides, section separators
- **Budget**: 8-12 lines, 40-50 chars/line
- **Font**: Large (24-48px for titles)
- **Best for**: Minimal content, centered text

### two-column (Text Columns)
- **Purpose**: Long text, lists, multiple paragraphs
- **Budget**: 15-22 lines, 35-46 chars/line
- **Font**: normal/compact/supercompact
- **Best for**: Content that naturally splits into 2 columns

### card-grid (Section Cards)
- **Purpose**: 4-5 distinct topics
- **Budget**: 12-16 lines total, 3-4 lines per card
- **Font**: normal/compact
- **Best for**: Summary points, feature lists

### layout-horizontal-left/right (Diagram + Text)
- **Purpose**: Image with accompanying text
- **Budget**: 8-12 lines (image takes 55% width)
- **Font**: normal/compact
- **Best for**: Explanatory diagrams with bullet points

### layout-diagram-only (Diagram Focus)
- **Purpose**: Large diagram with minimal text
- **Budget**: 3-6 lines caption text
- **Font**: normal
- **Best for**: Complex diagrams, architecture diagrams

## Tips

- **Check budgets before creating slides**: Know the limits upfront
- **Use compact strategically**: Only when content is over budget
- **Prefer content reduction over ultra-small fonts**: Readability matters
- **Validate layout choice**: Ensure layout matches content volume
- **Monitor budget compliance**: Regular checks prevent overflow

## Related Commands

- `/measure-quality` - Measure actual quality issues
- `/optimize-slides` - Automatic optimization based on budgets
- `/fix-overflow [slide]` - Fix specific over-budget slide
