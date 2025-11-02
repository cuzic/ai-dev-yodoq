---
description: Comprehensive slide quality improvement workflow using slidectl
---

# Comprehensive Slide Quality Improvement

You are an expert at improving slide quality using slidectl's complete workflow. This command orchestrates measurement, analysis, optimization, and validation to systematically enhance all slides.

## Overview

This workflow combines all slidectl capabilities:
1. **Measure**: Quality assessment with Playwright
2. **Budget**: Content capacity analysis
3. **Optimize**: Automated fix suggestions
4. **Validate**: Layout and content verification
5. **Report**: Comprehensive quality summary

## Quick Start

```bash
# Run complete quality improvement workflow
/improve-slides
```

The assistant will guide you through each phase and ask for approval before applying changes.

## Detailed Workflow

### Phase 1: Initial Assessment (5 minutes)

**1.1 Build Current Slides**
```bash
cd /home/cuzic/ai-dev-yodoq/slides
cat day1_1.md day1_2.md day1_3.md day2_1.md day2_2.md > all_slides.md
npx @marp-team/marp-cli all_slides.md --html --allow-local-files \
  --theme-set ../assets/themes/ai-seminar.css --theme ai-seminar \
  -o index.html
```

**1.2 Run Quality Measurement**
```bash
cd ~/slidectl
uv run slidectl measure --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html
```

**1.3 Analyze Results**
```bash
cat .state/measure/results.json | jq '{
  total: .slides | length,
  quality_summary: {
    fail: [.slides[] | select(.severity == "FAIL")] | length,
    warn: [.slides[] | select(.severity == "WARN")] | length,
    ok: [.slides[] | select(.severity == "OK")] | length
  },
  top_issues: [.slides[] | select(.violations | length > 0) |
    {slide: .slide_number, violations: .violations | length, severity: .severity}
  ] | sort_by(.violations) | reverse | .[0:10]
}'
```

**Present Initial Assessment:**
```
📊 Initial Quality Assessment
==============================

Total Slides: 168

Quality Distribution:
  ❌ FAIL: 12 slides (7.1%)   - Critical issues
  ⚠️  WARN: 23 slides (13.7%) - Minor issues
  ✅ OK: 133 slides (79.2%)   - No issues

Top 10 Problem Slides:
1. Slide 41: 4 violations (FAIL)
   - viewport_overflow: 234px
   - text_density_high: 78%
   - safe_area_intrusion: bottom
   - container_overflow: 180px

2. Slide 73: 3 violations (FAIL)
   ...

Common Issues:
  - Viewport overflow: 15 slides
  - High text density: 8 slides
  - Safe area intrusion: 6 slides
  - Layout misuse: 4 slides

Estimated fix time: 20-30 minutes
```

### Phase 2: Budget Analysis (3 minutes)

**2.1 Calculate Content Budgets**
```bash
cd ~/slidectl
uv run slidectl budget --ws /home/cuzic/ai-dev-yodoq \
  --analyze /home/cuzic/ai-dev-yodoq/slides/all_slides.md
```

**2.2 Review Budget Compliance**
```bash
cat .state/budget/usage_analysis.json | jq '{
  compliance_summary: {
    within_budget: [.slides[] | select(.compliance == "WITHIN_BUDGET")] | length,
    over_budget: [.slides[] | select(.compliance == "OVER_BUDGET")] | length,
    significantly_over: [.slides[] | select(.overflow_by.percentage > 50)] | length
  },
  worst_offenders: [.slides[] | select(.compliance == "OVER_BUDGET") |
    {slide: .slide_number, overflow: .overflow_by.percentage, layout: .layout}
  ] | sort_by(.overflow) | reverse | .[0:10]
}'
```

**Present Budget Analysis:**
```
📏 Content Budget Analysis
==========================

Budget Compliance:
  ✅ Within budget: 145 slides (86.3%)
  ❌ Over budget: 23 slides (13.7%)
  🔴 Significantly over (>50%): 8 slides

Worst Budget Offenders:
1. Slide 41: 176% of budget (two-column normal)
   → Recommendation: Apply supercompact + reduce 20%
2. Slide 73: 142% of budget (two-column normal)
   → Recommendation: Apply compact
...

Layout Distribution:
  two-column: 36 slides (21.4%)
  card-grid: 28 slides (16.7%)
  layout-horizontal: 39 slides (23.2%)
  lead: 25 slides (14.9%)
  normal: 40 slides (23.8%)
```

### Phase 3: Optimization Strategy (2 minutes)

Based on measurement + budget analysis, create fix strategy:

**3.1 Categorize Fixes by Type**

```python
fixes = {
    "quick_wins": [
        # Apply compact class (low risk, high impact)
        "Slide 73: two-column → two-column compact",
        "Slide 99: layout-horizontal-left → layout-horizontal-left compact",
        ...
    ],
    "medium_effort": [
        # Apply supercompact or reduce content (medium risk)
        "Slide 41: Apply supercompact + reduce 15%",
        "Slide 81: Reduce content from 22 to 16 lines",
        ...
    ],
    "layout_changes": [
        # Change layout type (requires review)
        "Slide 88: two-column → card-grid (5 sections)",
        "Slide 120: two-column → lead (header only)",
        ...
    ],
    "manual_review": [
        # Complex issues needing human judgment
        "Slide 127: Safe area intrusion, review image positioning",
        ...
    ]
}
```

**Present Strategy:**
```
🎯 Optimization Strategy
========================

Fix Categories:
  ⚡ Quick Wins (15 slides): Apply compact class
     - Zero information loss
     - ~25% capacity increase
     - Estimated time: 5 minutes

  🔧 Medium Effort (8 slides): Content reduction + compact
     - Minor information adjustment
     - ~40% quality improvement
     - Estimated time: 15 minutes

  📐 Layout Changes (4 slides): Switch layout type
     - Better content organization
     - Requires validation
     - Estimated time: 10 minutes

  👁️ Manual Review (2 slides): Complex issues
     - Human judgment needed
     - Case-by-case fixes
     - Estimated time: 10 minutes

Total estimated time: 40 minutes
Expected outcome: 90%+ slides clean (OK status)
```

**Ask for approval:**
```
Shall I proceed with the optimization? I'll start with:
1. Quick Wins (15 slides, low risk)
2. Then Medium Effort (8 slides)
3. Layout Changes last (needs your review)

Type 'yes' to proceed, or specify which phase to start with.
```

### Phase 4: Apply Optimizations (15-20 minutes)

**4.1 Quick Wins - Apply Compact Classes**

```python
# slides to modify
quick_wins = [73, 99, 104, 112, 135, ...]

for slide_num in quick_wins:
    # Find slide in day*.md files
    # Add "compact" to _class declaration
    # Example: <!-- _class: two-column -->
    #       → <!-- _class: two-column compact -->
```

After applying:
```bash
cd /home/cuzic/ai-dev-yodoq/slides
cat day1_1.md day1_2.md day1_3.md day2_1.md day2_2.md > all_slides.md
npx @marp-team/marp-cli all_slides.md --html --allow-local-files \
  --theme-set ../assets/themes/ai-seminar.css --theme ai-seminar \
  -o index.html

# Re-measure
cd ~/slidectl
uv run slidectl measure --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html
```

**Report Quick Wins Results:**
```
✅ Quick Wins Applied (15 slides)
Results:
  - FAIL: 12 → 5 slides (-7)
  - WARN: 23 → 18 slides (-5)
  - OK: 133 → 145 slides (+12)
  - Quality improvement: +7.2%

Proceeding to Medium Effort fixes...
```

**4.2 Medium Effort - Content Reduction + Supercompact**

For each slide needing content reduction:
1. Calculate target line count (based on budget)
2. Analyze content structure
3. Apply reduction strategies:
   - Remove redundancy
   - Simplify expressions
   - Use abbreviations
   - Merge similar points
4. Apply supercompact if still needed

Use `/fix-overflow [slide-number]` for detailed content optimization.

**4.3 Layout Changes**

For each layout change:
1. Review current content structure
2. Validate new layout appropriateness
3. Update `<!-- _class: ... -->` declaration
4. Rebuild and verify

**Present before applying layout changes:**
```
📐 Layout Changes Recommended:

Slide 88: two-column → card-grid
  Current: 5 bold items in single column
  Problem: Short content, column2 empty
  Solution: Display as 5 balanced cards
  Approve? [y/n]

Slide 120: two-column → lead
  Current: Header only (35 chars)
  Problem: No body content for columns
  Solution: Centered section header
  Approve? [y/n]
```

### Phase 5: Validation & Reporting (5 minutes)

**5.1 Final Quality Measurement**
```bash
cd ~/slidectl
uv run slidectl measure --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html
```

**5.2 Generate Improvement Report**

```python
# Compare initial vs final measurements
initial_results = load_json('.state/measure/initial_results.json')
final_results = load_json('.state/measure/results.json')

report = {
    "before": {
        "fail": count_by_severity(initial_results, "FAIL"),
        "warn": count_by_severity(initial_results, "WARN"),
        "ok": count_by_severity(initial_results, "OK"),
        "avg_score": avg_quality_score(initial_results)
    },
    "after": {
        "fail": count_by_severity(final_results, "FAIL"),
        "warn": count_by_severity(final_results, "WARN"),
        "ok": count_by_severity(final_results, "OK"),
        "avg_score": avg_quality_score(final_results)
    },
    "improvements": calculate_improvements(initial_results, final_results),
    "fixes_applied": list_applied_fixes()
}
```

**Present Final Report:**
```
🎉 Slide Quality Improvement Complete!
=======================================

Before Optimization:
  Total: 168 slides
  ❌ FAIL: 12 (7.1%)
  ⚠️  WARN: 23 (13.7%)
  ✅ OK: 133 (79.2%)
  Avg Score: 76.3/100

After Optimization:
  Total: 168 slides
  ❌ FAIL: 2 (1.2%)    ↓ -83% reduction
  ⚠️  WARN: 11 (6.5%)  ↓ -52% reduction
  ✅ OK: 155 (92.3%)   ↑ +16.5% increase
  Avg Score: 89.7/100  ↑ +13.4 points

Fixes Applied:
  ⚡ Compact classes: 15 slides
  🔧 Supercompact classes: 5 slides
  📝 Content reductions: 8 slides
  📐 Layout changes: 4 slides
  Total fixes: 32 slides

Remaining Issues (2 FAIL, 11 WARN):
  1. Slide 41: Still 52px overflow (was 234px) - Consider splitting
  2. Slide 127: Minor safe area intrusion (8px) - Image adjustment

Quality Grade: A (89.7/100)
Target Achieved: ✅ YES (target: 85+)

Time Spent: 38 minutes
Next Steps:
  - Review remaining 2 FAIL slides manually
  - Consider splitting Slide 41 into 2 slides
  - Adjust image positioning on Slide 127
  - Deploy to GitHub Pages
```

### Phase 6: Commit & Deploy (2 minutes)

**6.1 Create Commit**
```bash
git add slides/day*.md slides/all_slides.md slides/index.html
git commit -m "feat: Comprehensive slide quality improvement using slidectl

Applied slidectl-based optimization to improve overall slide quality.

Results:
- FAIL slides: 12 → 2 (-83%)
- WARN slides: 23 → 11 (-52%)
- OK slides: 133 → 155 (+16.5%)
- Quality score: 76.3 → 89.7 (+13.4 points)

Fixes:
- 15 slides: Applied compact class
- 5 slides: Applied supercompact class
- 8 slides: Content reduction
- 4 slides: Layout optimization

Quality grade: A (89.7/100)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**6.2 Push to GitHub**
```bash
git push
```

**6.3 Verify Deployment**
```bash
# Wait for GitHub Actions
gh run list --limit 1

# Check deployed site
curl -I https://cuzic.github.io/ai-dev-yodoq/
```

## Success Criteria

Optimization is successful when:
- ✅ FAIL slides < 5% (ideal: <2%)
- ✅ WARN slides < 15% (ideal: <10%)
- ✅ OK slides > 85% (ideal: >90%)
- ✅ Average quality score > 85
- ✅ No critical viewport overflow (>200px)
- ✅ No critical safe area violations

## Tips

- **Run measurement first**: Understand issues before fixing
- **Fix by priority**: FAIL before WARN, high overflow before low
- **Validate changes**: Re-measure after each major change batch
- **Preserve content**: Prefer compact classes over content reduction
- **Use version control**: Commit frequently for easy rollback
- **Review manually**: Some issues need human judgment

## Troubleshooting

**Issue**: slidectl command not found
```bash
cd ~/slidectl && uv run slidectl --version
```

**Issue**: Workspace not initialized
```bash
cd ~/slidectl && uv run slidectl init --ws /home/cuzic/ai-dev-yodoq
```

**Issue**: Measurement fails
```bash
# Check HTML file exists
ls -la /home/cuzic/ai-dev-yodoq/slides/index.html
# Rebuild if needed
cd /home/cuzic/ai-dev-yodoq/slides && npx @marp-team/marp-cli ...
```

## Related Commands

- `/measure-quality` - Quality measurement only
- `/optimize-slides` - Automated optimization
- `/check-budget` - Budget analysis only
- `/fix-overflow [slide]` - Single slide fix
