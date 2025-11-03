"""
Analyze FAIL slides from final measurement results
"""
import json
from pathlib import Path

# Load results
results_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/final_results.json")
with open(results_file, "r") as f:
    data = json.load(f)

# Extract FAIL slides
fail_slides = [s for s in data["slides"] if s["severity"] == "FAIL"]
fail_slides.sort(key=lambda x: x["viewport_overflow_px"], reverse=True)

print(f"Total FAIL slides: {len(fail_slides)}\n")
print("=" * 80)
print("TOP 20 WORST FAIL SLIDES")
print("=" * 80)
print(f"{'Rank':<6} {'Slide':<8} {'Overflow':<12} {'Layout':<30}")
print("-" * 80)

for i, slide in enumerate(fail_slides[:20], 1):
    slide_num = slide["slide_number"]
    overflow = slide["viewport_overflow_px"]
    layout = slide["slide_classes"]

    print(f"{i:<6} {slide_num:<8} {overflow:.1f}px{'':<6} {layout:<30}")

print("\n" + "=" * 80)

# Save to file for reference
output = {
    "total_fail": len(fail_slides),
    "top_20": [
        {
            "rank": i + 1,
            "slide_number": s["slide_number"],
            "overflow": s["viewport_overflow_px"],
            "layout_class": s["slide_classes"]
        }
        for i, s in enumerate(fail_slides[:20])
    ]
}

with open("/home/cuzic/ai-dev-yodoq/.state/measure/fail_analysis.json", "w") as f:
    json.dump(output, f, indent=2)

print("Saved detailed analysis to .state/measure/fail_analysis.json")
