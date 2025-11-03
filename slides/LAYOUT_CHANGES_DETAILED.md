# Detailed Layout Changes - Slide by Slide

This document provides the complete details of all 21 layout changes implemented.

---

## Change Type 1: card-grid → two-column (9 slides)

**Rationale:** Card-grid layout requires 4+ distinct sections to display as cards. Slides with only 1-3 sections or checklists work better with two-column layout.

### Slide 108 (Whitespace: 88.9% → ~65%)
```diff
- <!-- _class: card-grid ultracompact -->
+ <!-- _class: two-column ultracompact -->

# 演習成功のチェックリスト①
```
**Content:** Checklist with 12 items across 3 sections
**Why:** Checklists work better in two-column format than card-grid

---

### Slide 88 (Whitespace: 81.5% → ~65%)
```diff
- <!-- _class: card-grid ultracompact supercompact -->
+ <!-- _class: two-column supercompact -->
```
**Content:** Sparse content without distinct card sections
**Why:** No clear sections - two-column more appropriate

---

### Slide 163 (Whitespace: 77.8% → ~65%)
```diff
- <!-- _class: card-grid supercompact -->
+ <!-- _class: two-column supercompact -->
```
**Content:** Only 1 main section with 7 words
**Why:** Single section doesn't justify card-grid layout

---

### Slide 162 (Whitespace: 71.9% → ~65%)
```diff
- <!-- _class: card-grid supercompact -->
+ <!-- _class: two-column supercompact -->
```
**Content:** 1 heading, 9 words, sparse structure
**Why:** Not enough sections for card-grid

---

### Slide 134 (Whitespace: 72.9% → ~65%)
```diff
- <!-- _class: layout-horizontal-right supercompact -->
+ <!-- _class: two-column supercompact -->
```
**Content:** No image found despite horizontal-right layout
**Why:** Horizontal layout without image is inappropriate

---

### Slide 135 (Whitespace: 71.8% → ~65%)
```diff
- <!-- _class: layout-horizontal-right supercompact -->
+ <!-- _class: two-column supercompact -->
```
**Content:** 6 paragraphs, no image
**Why:** Horizontal layout requires an image

---

### Slide 124 (Whitespace: 71.5% → ~65%)
```diff
- <!-- _class: layout-horizontal-right supercompact -->
+ <!-- _class: two-column supercompact -->
```
**Content:** 2 headings, no image detected
**Why:** Mismatched layout and content structure

---

### Slide 123 (Whitespace: 71.3% → ~65%)
```diff
- <!-- _class: layout-horizontal-left supercompact -->
+ <!-- _class: two-column supercompact -->
```
**Content:** 4 paragraphs, no image detected
**Why:** Horizontal layout inappropriate without image

---

### Slide 139 (Whitespace: 70.8% → ~65%)
```diff
- <!-- _class: card-grid supercompact -->
+ <!-- _class: two-column supercompact -->
```
**Content:** 5 headings but only 10 words total
**Why:** Too sparse for card-grid, needs two-column

---

## Change Type 2: two-column → layout-horizontal (7 slides)

**Rationale:** Slides with 1 image + text content should use horizontal layout (image on one side, text on other) rather than two-column layout.

### Slide 37 (Whitespace: 79.9% → ~65%)
```diff
- <!-- _class: two-column compact -->
+ <!-- _class: layout-horizontal-left compact -->
```
**Content:** 3 headings, 2 lists, 1 image
**Why:** Single image + text benefits from horizontal layout

---

### Slide 79 (Whitespace: 79.6% → ~65%)
```diff
- <!-- _class: two-column supercompact -->
+ <!-- _class: layout-horizontal-left supercompact -->
```
**Content:** 3 headings, 5 paragraphs, 2 lists, 1 image
**Why:** Image-text combination better with horizontal layout

---

### Slide 165 (Whitespace: 78.8% → ~65%)
```diff
- <!-- _class: two-column compact -->
+ <!-- _class: layout-horizontal-left compact -->
```
**Content:** 4 headings, 3 lists, 1 image
**Why:** Optimize for image + text display

---

### Slide 43 (Whitespace: 74.9% → ~65%)
```diff
- <!-- _class: two-column compact -->
+ <!-- _class: layout-horizontal-left compact -->
```
**Content:** 1 heading, 4 paragraphs, 4 lists, 2 images
**Why:** Better image display with horizontal layout

---

### Slide 29 (Whitespace: 74.3% → ~65%)
```diff
- <!-- _class: two-column compact -->
+ <!-- _class: layout-horizontal-left compact -->
```
**Content:** 3 headings, 6 paragraphs, 1 image
**Why:** Single image content works better horizontally

---

### Slide 35 (Whitespace: 72.9% → ~65%)
```diff
- <!-- _class: two-column compact -->
+ <!-- _class: layout-horizontal-left compact -->
```
**Content:** 4 headings, 3 paragraphs, 1 image
**Why:** Image positioning improved with horizontal layout

---

### Slide 41 (Whitespace: 71.5% → ~65%)
```diff
- <!-- _class: two-column compact -->
+ <!-- _class: layout-horizontal-left compact -->
```
**Content:** 4 headings, 1 paragraph, 2 lists, 2 images
**Why:** Better for image-heavy content

---

## Change Type 3: Add two-column (4 slides)

**Rationale:** Slides without layout classes that contain checklists, multiple sections, or structured content benefit from explicit two-column layout.

### Slide 44 (Whitespace: 95.4% → ~65%)
```diff
+ <!-- _class: two-column -->

## Part 1 振り返りチェックリスト
```
**Content:** 1 heading, 13 bullet points (checklist format)
**Why:** Long checklist needs two-column for better readability

---

### Slide 115 (Whitespace: 77.3% → ~65%)
```diff
- <!-- _class: title -->
+ <!-- _class: title two-column -->
```
**Content:** 2 headings, 8 bullet points across sections
**Why:** Checklist structure needs two-column layout

---

### Slide 129 (Whitespace: 70.3% → ~65%)
```diff
- <!-- _class: layout-horizontal-right supercompact -->
+ <!-- _class: layout-horizontal-right supercompact two-column -->
```
**Content:** 5 paragraphs, 1 list, 8 bullets
**Why:** Structured list content benefits from columns

---

### Slide 80 (Whitespace: 69.3% → ~65%)
```diff
- <!-- _class: layout-horizontal-left supercompact -->
+ <!-- _class: layout-horizontal-left supercompact two-column -->
```
**Content:** 2 headings, 1 paragraph, 1 list, 8 bullets
**Why:** Multiple bullet points work better in columns

---

## Change Type 4: Remove inappropriate layout (2 slides)

**Rationale:** Some slides have layout classes that don't match their simple, single-topic content. Removing the layout class allows default styling which is more appropriate.

### Slide 73 (Whitespace: 78.5% → ~70%)
```diff
- <!-- _class: two-column ultracompact -->
+ <!-- _class: ultracompact -->
```
**Content:** 3 headings, 3 paragraphs, 2 lists, 14 words total
**Why:** Single topic doesn't need two-column layout

---

### Slide 49 (Whitespace: 69.9% → ~70%)
```diff
- <!-- _class: two-column ultracompact -->
+ <!-- _class: ultracompact -->
```
**Content:** 4 headings, 2 lists, 18 words
**Why:** Simple content - default layout sufficient

---

## Change Type 5: Remove lead class (1 slide)

**Rationale:** Lead class is for minimal section dividers (1-5 words). Slides with substantial content structure should not use lead.

### Slide 143 (Whitespace: 82.6% → ~65%)
```diff
- <!-- _class: lead -->
+
# テストシナリオからテストコードへ
```
**Content:** 5 headings with structured sections
**Why:** Too much content for lead (section divider) layout

---

## Change Type 6: Special case - two-column with image (1 slide)

### Slide 38 (Whitespace: 68.6% → ~65%)
```diff
- <!-- _class: layout-horizontal-right compact -->
+ <!-- _class: two-column compact -->
```
**Content:** 1 heading, 1 paragraph, 1 list
**Why:** No image detected - two-column more appropriate

---

## Summary Statistics

### By Whitespace Reduction Impact

**High Impact (>85% → ~65%):**
- Slide 44: 95.4% → ~65% (30pp reduction)
- Slide 108: 88.9% → ~65% (24pp reduction)

**Medium-High Impact (80-85% → ~65%):**
- Slide 143: 82.6% → ~65% (18pp reduction)
- Slide 88: 81.5% → ~65% (17pp reduction)

**Medium Impact (75-80% → ~65%):**
- Slides 37, 79, 165, 73, 163, 115: 75-80% → ~65% (10-15pp reduction)

**Lower Impact (70-75% → ~65%):**
- Slides 43, 29, 134, 35, 162, 135, 124, 41, 123, 139, 129, 49, 80, 38: 70-75% → ~65% (5-10pp reduction)

### By Content Type

**Checklists (4 slides):**
- Added or changed to two-column: 44, 108, 115, 80

**Image + Text (7 slides):**
- Changed to layout-horizontal: 37, 79, 165, 43, 29, 35, 41

**Wrong Card-Grid (6 slides):**
- Changed to two-column: 108, 88, 163, 162, 139

**Missing Image (4 slides):**
- Horizontal → two-column: 134, 135, 124, 123

---

## Visual Examples

### Before: Card-grid with only 2 sections
```markdown
<!-- _class: card-grid supercompact -->

# Section 1
Content here

# Section 2
Content here
```
**Problem:** Only 2 sections can't create proper card layout, results in excessive whitespace

### After: Two-column layout
```markdown
<!-- _class: two-column supercompact -->

# Section 1
Content here

# Section 2
Content here
```
**Solution:** Two-column properly handles 2-3 sections with better space utilization

---

### Before: Two-column with 1 image
```markdown
<!-- _class: two-column compact -->

# Feature Overview

![diagram](diagram.svg)

- Feature A
- Feature B
- Feature C
```
**Problem:** Image and text compete for column space, image too small

### After: Horizontal layout
```markdown
<!-- _class: layout-horizontal-left compact -->

# Feature Overview

![diagram](diagram.svg)

- Feature A
- Feature B
- Feature C
```
**Solution:** Image gets dedicated space on left, text flows naturally on right

---

## Files Modified

| File | Slides Changed | Changes |
|------|----------------|---------|
| `day1_1.md` | 7 | 44, 37, 43, 29, 35, 41, 38 |
| `day1_2.md` | 4 | 88, 79, 73, 80 |
| `day1_3.md` | 2 | 108, 115 |
| `day2_1.md` | 5 | 134, 135, 124, 123, 139, 129 |
| `day2_2.md` | 3 | 165, 163, 162 |

**Total:** 21 slides across 5 files

---

## Validation

To verify these changes:

1. **Regenerate visual density report:**
   ```bash
   npm run analyze:density
   ```

2. **Check specific slides:**
   ```bash
   grep -A 5 "slide 44" .logs/visual_density_report.json
   ```

3. **View slides in browser:**
   ```bash
   npm start
   # Navigate to changed slide numbers
   ```

---

## Next Steps

1. Review slides requiring content addition (12 slides)
2. Apply same methodology to remaining 67 problematic slides
3. Run validation to confirm whitespace improvements
4. Document layout selection guidelines for future slides
