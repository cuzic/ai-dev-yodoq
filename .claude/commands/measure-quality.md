---
description: Measure slide quality using slidectl with comprehensive DOM analysis
---

# Slide Quality Measurement with slidectl

You are an expert at analyzing slide quality using the slidectl tool. Use slidectl's advanced Playwright-based measurement capabilities to identify quality issues.

## Overview

slidectl provides comprehensive quality measurement including:
- Text density and whitespace analysis
- Viewport boundary overflow detection
- Safe area intrusion checks
- Container overflow detection
- Severity classification (FAIL/WARN)
- Content budget calculations per layout type

## Workflow

### STEP 1: Initialize slidectl Workspace (if needed)

Check if slidectl workspace exists in the current project:

```bash
# Check for .state directory
ls -la .state 2>/dev/null
```

If not found, initialize workspace:

```bash
cd ~/slidectl
uv run slidectl init --ws /home/cuzic/ai-dev-yodoq
```

### STEP 2: Render Current Slides

Ensure slides are built with the latest changes:

```bash
cd /home/cuzic/ai-dev-yodoq/slides
cat day1_1.md day1_2.md day1_3.md day2_1.md day2_2.md > all_slides.md
npx @marp-team/marp-cli all_slides.md --html --allow-local-files \
  --theme-set ../assets/themes/ai-seminar.css --theme ai-seminar \
  -o index.html
```

### STEP 3: Run Quality Measurement

Execute slidectl measure command:

```bash
cd ~/slidectl
uv run slidectl measure --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html
```

**What this does:**
- Launches Playwright with Chromium
- Analyzes each slide's DOM structure
- Measures text bounds, image positions, container sizes
- Detects viewport overflow (1280x720 boundary)
- Checks safe area intrusion (1216x656 safe zone)
- Calculates text density and whitespace ratios
- Assigns severity levels (FAIL/WARN/OK)

### STEP 4: Review Measurement Results

The results are saved to `.state/measure/results.json`. Extract key insights:

```bash
cd /home/cuzic/ai-dev-yodoq
cat .state/measure/results.json | jq '.slides[] | select(.violations | length > 0) | {slide: .slide_number, violations: .violations | length, severity: .severity}'
```

**Key metrics to review:**
- `violations[]`: List of quality violations
  - `viewport_overflow`: Content exceeds 1280x720
  - `safe_area_intrusion`: Content too close to edges
  - `container_overflow`: Content exceeds parent container
  - `text_density_high`: Too much text (>70% coverage)
  - `text_density_low`: Too little text (<20% coverage)
  - `whitespace_excessive`: Too much empty space (>60%)

- `severity`: Overall quality grade
  - `FAIL`: Critical issues requiring immediate fix
  - `WARN`: Minor issues that should be addressed
  - `OK`: No significant issues

### STEP 5: Generate Quality Report

Create a human-readable summary:

```bash
cd ~/slidectl
uv run slidectl measure --ws /home/cuzic/ai-dev-yodoq \
  --html /home/cuzic/ai-dev-yodoq/slides/index.html \
  --report
```

Or manually analyze the JSON:

```python
import json

with open('.state/measure/results.json', 'r') as f:
    data = json.load(f)

# Count by severity
fail_slides = [s for s in data['slides'] if s['severity'] == 'FAIL']
warn_slides = [s for s in data['slides'] if s['severity'] == 'WARN']
ok_slides = [s for s in data['slides'] if s['severity'] == 'OK']

print(f"Quality Summary:")
print(f"  FAIL: {len(fail_slides)} slides")
print(f"  WARN: {len(warn_slides)} slides")
print(f"  OK: {len(ok_slides)} slides")
print(f"  Total: {len(data['slides'])} slides")

# List FAIL slides
if fail_slides:
    print(f"\nFAIL Slides:")
    for slide in fail_slides:
        print(f"  Slide {slide['slide_number']}: {len(slide['violations'])} violations")
        for v in slide['violations'][:3]:  # Show first 3
            print(f"    - {v['type']}: {v['description']}")
```

### STEP 6: Identify Priority Fixes

Based on the measurement results, create a prioritized fix list:

1. **FAIL slides with viewport_overflow** - Critical, content not visible
2. **FAIL slides with safe_area_intrusion** - High priority, content cut off
3. **WARN slides with text_density issues** - Medium priority, readability
4. **WARN slides with whitespace issues** - Low priority, visual balance

Present the findings to the user with:
- Total slide count
- Quality distribution (FAIL/WARN/OK)
- Top 10 most problematic slides
- Recommended next steps

## Example Output Format

```
📊 Slide Quality Measurement Results
=====================================

Total Slides: 168
Quality Distribution:
  ✅ OK:   145 slides (86.3%)
  ⚠️  WARN: 18 slides (10.7%)
  ❌ FAIL:  5 slides (3.0%)

Top 5 Problem Slides:
1. Slide 41: 3 violations (FAIL)
   - viewport_overflow: Content exceeds viewport by 234px bottom
   - text_density_high: 78% text coverage (target: <70%)
   - container_overflow: List exceeds container by 180px

2. Slide 73: 2 violations (FAIL)
   - viewport_overflow: Content exceeds viewport by 156px bottom
   - safe_area_intrusion: Content within 12px of bottom edge

3. Slide 99: 2 violations (WARN)
   - text_density_high: 72% text coverage
   - whitespace_low: Only 28% whitespace (target: 30-40%)

...

Recommended Actions:
1. Apply compact class to slides 41, 73 (FAIL with overflow)
2. Reduce content on slide 99 (high text density)
3. Review layout for slides with safe area intrusion
```

## Tips

- **Run after every major content change** to catch quality regressions early
- **Compare before/after** by saving results.json with different filenames
- **Use with /optimize-slides** command for automated fixes
- **Export to PPTX** after quality issues are resolved

## Related Commands

- `/optimize-slides` - Automatically optimize based on measurement results
- `/check-budget` - Calculate content budgets per layout type
- `/fix-overflow [slide-number]` - Fix specific overflow issues
