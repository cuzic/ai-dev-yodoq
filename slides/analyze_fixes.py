"""
Analyze measurement results and generate fix strategies
"""
import json
from pathlib import Path
from collections import defaultdict

# Load results
results_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/initial_results.json")
with open(results_file, "r") as f:
    data = json.load(f)

# Categorize slides by severity and overflow
fail_slides = [s for s in data["slides"] if s["severity"] == "FAIL"]
warn_slides = [s for s in data["slides"] if s["severity"] == "WARN"]

print("=" * 70)
print("FIX STRATEGY ANALYSIS")
print("=" * 70)

# Categorize by overflow level
overflow_categories = {
    "critical": [],  # >300px
    "high": [],      # 100-300px
    "medium": [],    # 50-100px
    "low": [],       # <50px
}

for slide in fail_slides:
    overflow = slide["viewport_overflow_px"]
    if overflow > 300:
        overflow_categories["critical"].append(slide)
    elif overflow > 100:
        overflow_categories["high"].append(slide)
    elif overflow > 50:
        overflow_categories["medium"].append(slide)
    else:
        overflow_categories["low"].append(slide)

print("\nOVERFLOW CATEGORIZATION:")
print(f"  Critical (>300px): {len(overflow_categories['critical'])} slides")
print(f"  High (100-300px):  {len(overflow_categories['high'])} slides")
print(f"  Medium (50-100px): {len(overflow_categories['medium'])} slides")
print(f"  Low (<50px):       {len(overflow_categories['low'])} slides")

# Analyze by layout class
layout_stats = defaultdict(lambda: {"count": 0, "total_overflow": 0, "slides": []})

for slide in fail_slides:
    classes = slide["slide_classes"]
    layout_stats[classes]["count"] += 1
    layout_stats[classes]["total_overflow"] += slide["viewport_overflow_px"]
    layout_stats[classes]["slides"].append(slide["slide_number"])

print("\nFAIL SLIDES BY LAYOUT:")
for layout, stats in sorted(layout_stats.items(), key=lambda x: x[1]["count"], reverse=True):
    avg_overflow = stats["total_overflow"] / stats["count"]
    print(f"  {layout}: {stats['count']} slides, avg overflow={avg_overflow:.1f}px")
    print(f"    Slides: {stats['slides'][:10]}" + (" ..." if len(stats['slides']) > 10 else ""))

# Generate fix recommendations
print("\n" + "=" * 70)
print("RECOMMENDED FIX STRATEGY")
print("=" * 70)

print("\nPhase 1: Quick Wins (Low Risk)")
print("  Apply 'compact' class to High/Medium overflow slides (100-300px)")
print(f"  Target: {len(overflow_categories['high']) + len(overflow_categories['medium'])} slides")
print("  Expected: ~25% space reduction, minimal information loss")

if len(overflow_categories['high']) > 0:
    print("\n  High priority slides:")
    for slide in sorted(overflow_categories['high'], key=lambda x: x["viewport_overflow_px"], reverse=True)[:5]:
        print(f"    Slide {slide['slide_number']}: {slide['viewport_overflow_px']:.1f}px, {slide['slide_classes']}")

print("\nPhase 2: Aggressive Fixes (Medium Risk)")
print("  Apply 'supercompact' class to Critical overflow slides (>300px)")
print(f"  Target: {len(overflow_categories['critical'])} slides")
print("  Expected: ~40% space reduction, some information may be tight")

if len(overflow_categories['critical']) > 0:
    print("\n  Critical slides:")
    for slide in sorted(overflow_categories['critical'], key=lambda x: x["viewport_overflow_px"], reverse=True):
        print(f"    Slide {slide['slide_number']}: {slide['viewport_overflow_px']:.1f}px, {slide['slide_classes']}")

print("\nPhase 3: Manual Review (If Needed)")
print("  Slides that still FAIL after Phase 1 & 2")
print("  Consider: content reduction, layout changes, or split into 2 slides")

# Generate fix plan JSON
fix_plan = {
    "phase1_compact": [
        {"slide_number": s["slide_number"], "overflow": s["viewport_overflow_px"], "classes": s["slide_classes"]}
        for s in overflow_categories["high"] + overflow_categories["medium"]
    ],
    "phase2_supercompact": [
        {"slide_number": s["slide_number"], "overflow": s["viewport_overflow_px"], "classes": s["slide_classes"]}
        for s in overflow_categories["critical"]
    ],
    "phase3_manual": [
        {"slide_number": s["slide_number"], "overflow": s["viewport_overflow_px"], "classes": s["slide_classes"]}
        for s in overflow_categories["low"]
    ],
}

fix_plan_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/fix_plan.json")
with open(fix_plan_file, "w") as f:
    json.dump(fix_plan, f, indent=2)

print(f"\n\nFix plan saved to: {fix_plan_file}")
