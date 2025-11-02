---
description: Automatically optimize slides using slidectl's iterative optimization workflow
---

# Slide Optimization with slidectl

You are an expert at automatically optimizing slides using slidectl's intelligent optimization workflow. Use slidectl's measure-optimize-iterate cycle to systematically improve slide quality.

## Overview

slidectl's optimization workflow:
1. **Measure**: Analyze quality with Playwright DOM analysis
2. **Score**: Calculate quality scores and identify issues
3. **Propose**: Generate optimization suggestions (compact classes, content reduction)
4. **Apply**: Implement fixes automatically or manually
5. **Iterate**: Re-measure and repeat until target quality achieved

## Prerequisites

Ensure slidectl workspace is initialized:

```bash
# Check workspace
ls -la .state 2>/dev/null

# Initialize if needed
cd ~/slidectl && uv run slidectl init --ws /home/cuzic/ai-dev-yodoq
```

## Workflow

### STEP 1: Initial Quality Measurement

Run comprehensive quality measurement:

```bash
cd ~/slidectl
uv run slidectl measure --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html
```

This creates `.state/measure/results.json` with detailed quality metrics.

### STEP 2: Analyze Quality Scores

Extract quality summary:

```bash
cd /home/cuzic/ai-dev-yodoq
cat .state/measure/results.json | jq '{
  total: .slides | length,
  fail: [.slides[] | select(.severity == "FAIL")] | length,
  warn: [.slides[] | select(.severity == "WARN")] | length,
  ok: [.slides[] | select(.severity == "OK")] | length,
  avg_quality_score: ([.slides[].quality_score] | add / length)
}'
```

### STEP 3: Run Automatic Optimization

Execute slidectl optimize command:

```bash
cd ~/slidectl
uv run slidectl optimize --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html \
  --target-score 85 \
  --max-iterations 3
```

**Parameters:**
- `--target-score 85`: Stop when average quality score reaches 85/100
- `--max-iterations 3`: Maximum optimization cycles (default: 3)
- `--auto-apply`: Automatically apply suggested fixes (use with caution)

**What this does:**

**Iteration 1: Measure → Suggest → Apply**
1. Measures current quality
2. Identifies top 10 problematic slides
3. Generates optimization suggestions:
   - Add `compact` class for slides with viewport overflow >200px
   - Add `supercompact` class for slides with overflow >400px
   - Remove unnecessary whitespace
   - Suggest content reduction targets
4. Applies fixes (if `--auto-apply` enabled)
5. Rebuilds slides and re-measures

**Iteration 2-3:** Repeat for remaining issues

### STEP 4: Review Optimization Suggestions

If `--auto-apply` is NOT used, review suggestions manually:

```bash
cat .state/optimize/iteration_1_suggestions.json | jq '.suggestions[] | {
  slide: .slide_number,
  action: .action,
  reason: .reason,
  expected_improvement: .expected_improvement
}'
```

**Common suggestion types:**

1. **Add compact class**
   ```json
   {
     "slide": 41,
     "action": "add_compact_class",
     "current_class": "two-column",
     "suggested_class": "two-column compact",
     "reason": "viewport_overflow: 234px bottom",
     "expected_improvement": "Reduce overflow by ~25%"
   }
   ```

2. **Upgrade to supercompact**
   ```json
   {
     "slide": 73,
     "action": "upgrade_to_supercompact",
     "current_class": "two-column compact",
     "suggested_class": "two-column supercompact",
     "reason": "Still 156px overflow after compact",
     "expected_improvement": "Reduce overflow by ~40%"
   }
   ```

3. **Content reduction**
   ```json
   {
     "slide": 99,
     "action": "reduce_content",
     "current_lines": 18,
     "target_lines": 12,
     "reason": "text_density_high: 78%",
     "expected_improvement": "Reduce density to 60%"
   }
   ```

4. **Layout change**
   ```json
   {
     "slide": 108,
     "action": "change_layout",
     "current_layout": "two-column",
     "suggested_layout": "card-grid",
     "reason": "Short content (5 items) better suited for card-grid",
     "expected_improvement": "Better space utilization"
   }
   ```

### STEP 5: Manual Fix Implementation (if needed)

If suggestions require manual intervention, apply them:

**For compact class additions:**
```bash
# Use the apply_content_optimizations.py script
python3 slides/apply_content_optimizations.py
```

**For content reduction:**
Use the `/fix-overflow [slide-number]` command for targeted content optimization.

**For layout changes:**
Manually edit the slide's `<!-- _class: ... -->` declaration.

### STEP 6: Rebuild and Re-measure

After applying fixes:

```bash
# Rebuild slides
cd /home/cuzic/ai-dev-yodoq/slides
cat day1_1.md day1_2.md day1_3.md day2_1.md day2_2.md > all_slides.md
npx @marp-team/marp-cli all_slides.md --html --allow-local-files \
  --theme-set ../assets/themes/ai-seminar.css --theme ai-seminar \
  -o index.html

# Re-measure quality
cd ~/slidectl
uv run slidectl measure --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html
```

### STEP 7: Iteration Until Target Quality

Repeat STEP 3-6 until:
- Target quality score is reached (e.g., avg score >85)
- No more FAIL slides
- Minimal WARN slides (<10%)

Track progress:

```bash
# Compare iteration results
jq '.summary' .state/optimize/iteration_*.json
```

### STEP 8: Generate Optimization Report

Create comprehensive report:

```bash
cd ~/slidectl
uv run slidectl optimize --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html \
  --report-only
```

This generates `.state/optimize/optimization_report.md` with:
- Before/after quality metrics
- Number of fixes applied per type
- Remaining issues
- Quality score improvement
- Iteration details

## Example Output Format

```
🔧 Slide Optimization Results
==============================

Initial State:
  Total Slides: 168
  FAIL: 12 slides (7.1%)
  WARN: 23 slides (13.7%)
  OK: 133 slides (79.2%)
  Avg Quality Score: 76.3/100

After Optimization (3 iterations):
  Total Slides: 168
  FAIL: 2 slides (1.2%)    ↓ -10 slides
  WARN: 15 slides (8.9%)   ↓ -8 slides
  OK: 151 slides (89.9%)   ↑ +18 slides
  Avg Quality Score: 87.5/100 ↑ +11.2 points

Fixes Applied:
  ✅ Added compact class: 15 slides
  ✅ Upgraded to supercompact: 5 slides
  ✅ Content reduction: 8 slides
  ✅ Layout changes: 3 slides

Remaining Issues:
  ⚠️  Slide 41: viewport_overflow (52px) - Manual review needed
  ⚠️  Slide 127: safe_area_intrusion (8px) - Minor adjustment

Quality Improvement: +14.8%
Target Achieved: ✅ YES (target: 85, achieved: 87.5)
```

## Optimization Strategies

slidectl uses intelligent optimization strategies:

1. **Priority-based fixing**: Tackle FAIL slides before WARN
2. **Incremental changes**: Apply compact before supercompact
3. **Layout-aware**: Different strategies per layout type
4. **Content preservation**: Minimize information loss
5. **Quality-score driven**: Focus on highest ROI fixes

## Safety Features

- **Dry-run mode**: Preview suggestions without applying
- **Backup creation**: Saves original files before modification
- **Rollback capability**: Can revert changes if quality degrades
- **Manual approval**: Human review for content reduction

## Tips

- **Start with `--dry-run`** to review suggestions first
- **Set realistic targets**: 85-90 score is excellent, 95+ is very hard
- **Monitor iterations**: Stop if quality plateaus
- **Combine with manual fixes**: Some issues need human judgment
- **Use version control**: Commit before optimization for easy rollback

## Related Commands

- `/measure-quality` - Run quality measurement only
- `/check-budget` - Calculate content budgets
- `/fix-overflow [slide]` - Manual fix for specific slide
