# Layout Validation Report

**Date:** 2025-10-31
**Total Slides:** 220
**Valid:** 191 (86.8%)
**Invalid:** 29 (13.2%)

## Summary

29 slides don't follow the optimal layout selection criteria from `LAYOUT_SELECTION_GUIDE.md`. These issues are categorized below with recommended fixes.

## Issues by Category

### 1. Default Layout with 8+ Bullets (13 slides)

**Issue:** Default layout is inefficient for 8+ bullets. Should use columns.

| Slide | Bullets | Recommended |
|-------|---------|-------------|
| 95 | 13 | two-column |
| 114 | 9 | two-column |
| 143 | 12 | two-column |
| 148 | 12 | two-column |
| 157 | 11 | two-column |
| 159 | 11 | two-column |
| 171 | 8 | two-column |
| 172 | 9 | two-column |
| 173 | 11 | two-column |
| 186 | 11 | two-column |
| 189 | 10 | two-column |
| 212 | 12 | two-column |

**Impact:** Poor space utilization, excessive vertical scrolling

**Fix:** Add `<!-- _class: two-column -->` directive

---

### 2. Two-Column Layout with < 8 Bullets (6 slides)

**Issue:** Two-column layout is over-engineered for < 8 bullets.

| Slide | Title | Bullets | Recommended |
|-------|-------|---------|-------------|
| 52 | STEP3 タスク分解とは | 6 | default |
| 112 | 演習の目的と課題 | 7 | default |
| 170 | テストシナリオからテストコードへ | 3 | default |
| 184 | (Untitled) | 4 | default |
| 190 | (Untitled) | 6 | default |
| 200 | (Untitled) | 7 | default |

**Impact:** Excessive white space, unnecessary complexity

**Fix:** Remove `<!-- _class: two-column -->` directive

---

### 3. Layout-Diagram-Only with Bullets (5 slides)

**Issue:** Diagram-only layout should have minimal text (≤3 bullets).

| Slide | Title | Bullets | Recommended |
|-------|-------|---------|-------------|
| 11 | セキュリティベストプラクティス（補足） | 12 | two-column |
| 33 | STEP1 チェックリスト | 8 | layout-horizontal-left |
| 46 | STEP2 チェックリスト | 8 | layout-horizontal-left |
| 61 | STEP3 チェックリスト | 8 | layout-horizontal-left |
| 75 | STEP4 チェックリスト | 9 | two-column |

**Impact:** Text overlays or competes with diagram

**Fix:**
- Slides 33, 46, 61: Change to `layout-horizontal-left` (checklist + diagram)
- Slides 11, 75: Change to `two-column` (more bullets)

---

### 4. Horizontal Layout Issues (2 slides)

#### Slide 42: Too Few Bullets

| Slide | Title | Bullets | Image | Issue |
|-------|-------|---------|-------|-------|
| 42 | ER図が開発をスムーズにする理由 | 2 | Yes | Too few bullets (< 3) |

**Recommended:** `layout-diagram-only` (diagram is primary)

#### Slide 149: Too Many Bullets

| Slide | Bullets | Image | Issue |
|-------|---------|-------|-------|
| 149 | 10 | Yes | Too many bullets (> 8) |

**Recommended:** `two-column` (separate image from text or reduce bullets)

---

### 5. Other Layout Issues (4 slides)

#### Slide 10: Two-Column Overcrowded

| Slide | Title | Bullets | Current | Issue |
|-------|-------|---------|---------|-------|
| 10 | 環境準備 | 19 | two-column | Too many bullets |

**Recommended:** `three-column`

#### Slide 47: Three-Column Under-utilized

| Slide | Bullets | Current | Issue |
|-------|---------|---------|-------|
| 47 | 13 | three-column | Too few bullets (< 15) |

**Recommended:** `two-column`

#### Slide 99: Card-Grid Too Many Sections

| Slide | Title | Sections | Issue |
|-------|-------|----------|-------|
| 99 | Part 2のキーポイント | 5 | Too many sections (> 4) |

**Recommended:** `two-column` or split into 2 slides

#### Slide 133: Lead with Bullets

| Slide | Bullets | Current | Issue |
|-------|---------|---------|-------|
| 133 | 17 | lead | Lead layout should have ≤3 bullets |

**Recommended:** `two-column`

---

## Recommended Actions

### Priority 1: High Impact (19 slides)

These slides have significant layout inefficiency:

1. **Default → Two-Column (12 slides):** 95, 114, 143, 148, 157, 159, 171, 172, 173, 186, 189, 212
2. **Diagram-Only → Horizontal/Two-Column (5 slides):** 11, 33, 46, 61, 75
3. **Two-Column → Three-Column (1 slide):** 10
4. **Lead → Two-Column (1 slide):** 133

### Priority 2: Medium Impact (7 slides)

These slides are functional but not optimal:

1. **Two-Column → Default (6 slides):** 52, 112, 170, 184, 190, 200
2. **Horizontal → Diagram-Only (1 slide):** 42

### Priority 3: Low Impact (3 slides)

These need content restructuring:

1. **Three-Column → Two-Column (1 slide):** 47
2. **Horizontal → Two-Column (1 slide):** 149
3. **Card-Grid → Two-Column (1 slide):** 99

---

## Implementation Script

A script to automatically fix these layout issues:

```bash
#!/bin/bash
# fix_layout_issues.sh

# Priority 1: Default → Two-Column (12 slides)
for slide in 95 114 143 148 157 159 171 172 173 186 189 212; do
    # Add two-column class before first heading after slide separator
    sed -i "s/^# \(.*\)$/<!-- _class: two-column -->\n\n# \1/g" all_slides.md
done

# Priority 1: Layout-diagram-only → layout-horizontal-left (3 slides)
for slide in 33 46 61; do
    sed -i 's/layout-diagram-only/layout-horizontal-left/g' all_slides.md
done

# And so on...
```

**Note:** Manual review recommended after automated changes.

---

## Statistics by Layout Type

| Layout | Count | % | Status |
|--------|-------|---|--------|
| default | 90 | 40.9% | ⚠️ 13 need columns |
| two-column | 41 | 18.6% | ⚠️ 7 over-engineered |
| lead | 25 | 11.4% | ⚠️ 1 has content |
| layout-horizontal-right | 23 | 10.5% | ✅ Valid |
| layout-horizontal-left | 16 | 7.3% | ⚠️ 1 under-utilized |
| three-column | 12 | 5.5% | ⚠️ 1 under-utilized |
| layout-diagram-only | 6 | 2.7% | ⚠️ 5 have content |
| card-grid | 6 | 2.7% | ⚠️ 1 too many sections |
| image-top-compact | 1 | 0.5% | ✅ Valid |

---

## Expected Outcome After Fixes

- **191 → 220 valid slides (100%)**
- Improved space utilization
- Better visual balance
- Consistent layout patterns
- Easier content navigation

---

## Testing After Fixes

1. **Run validation:**
   ```bash
   python3 validate_layout_choices.py
   ```

2. **Check overflow:**
   ```bash
   python3 analyze_actual_text_width_fixed.py
   ```

3. **Visual review:**
   ```bash
   npx @marp-team/marp-cli@latest all_slides.md -o index.html --html
   ```

4. **Verify criteria:**
   - Default: 0-7 bullets ✓
   - Two-column: 8-18 bullets ✓
   - Three-column: 15-27 bullets ✓
   - Horizontal: 5-8 bullets + image ✓
   - Diagram-only: 0-3 bullets + image ✓

---

## Files

- `validate_layout_choices.py` - Validation script
- `LAYOUT_SELECTION_GUIDE.md` - Comprehensive criteria
- `LAYOUT_CHEATSHEET.md` - Quick reference
- `LAYOUT_VALIDATION_REPORT.md` - This file
