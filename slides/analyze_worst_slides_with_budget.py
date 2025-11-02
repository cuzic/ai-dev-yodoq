"""
Analyze worst slides and calculate character counts to determine optimal compact level
"""
import json
from pathlib import Path

# Load measurement results
results_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/initial_results.json")
with open(results_file, "r") as f:
    data = json.load(f)

# Get worst FAIL slides
fail_slides = [s for s in data["slides"] if s["severity"] == "FAIL"]
fail_slides.sort(key=lambda x: x["viewport_overflow_px"], reverse=True)

# Character count thresholds from slidectl
thresholds = {
    "normal": (0, 100),
    "compact": (100, 150),
    "supercompact": (150, 250),
    "ultracompact": (250, 999999)
}

print("=" * 80)
print("WORST FAIL SLIDES ANALYSIS WITH SLIDECTL BUDGET")
print("=" * 80)
print()

# Analyze top 10
slide_numbers_to_check = [s["slide_number"] for s in fail_slides[:10]]

files = ["day1_1.md", "day1_2.md", "day1_3.md", "day2_1.md", "day2_2.md"]
slides_dir = Path("/home/cuzic/ai-dev-yodoq/slides")

slide_counter = 0
analysis = []

for filename in files:
    filepath = slides_dir / filename

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    slides = content.split("\n---\n")

    for i, slide in enumerate(slides):
        if i == 0 and slide.strip().startswith("---\nmarp:"):
            continue

        slide_counter += 1

        if slide_counter in slide_numbers_to_check:
            # Count characters (excluding class directives and comments)
            lines = slide.strip().split("\n")
            content_lines = [l for l in lines if l.strip() and not l.strip().startswith("<!--")]
            total_chars = sum(len(l.replace("#", "").replace("*", "").replace("-", "").strip()) for l in content_lines)

            # Get current class
            current_class = "normal"
            for line in lines:
                if "<!-- _class:" in line:
                    if "supercompact" in line:
                        current_class = "supercompact"
                    elif "compact" in line:
                        current_class = "compact"
                    elif "ultracompact" in line:
                        current_class = "ultracompact"
                    break

            # Determine recommended class based on character count
            recommended_class = "normal"
            for level, (min_chars, max_chars) in thresholds.items():
                if min_chars <= total_chars < max_chars:
                    recommended_class = level
                    break

            # Get overflow from results
            overflow = next((s["viewport_overflow_px"] for s in fail_slides if s["slide_number"] == slide_counter), 0)

            # Get layout
            layout = next((s["slide_classes"] for s in fail_slides if s["slide_number"] == slide_counter), "unknown")

            analysis.append({
                "slide_number": slide_counter,
                "file": filename,
                "overflow": overflow,
                "total_chars": total_chars,
                "current_class": current_class,
                "recommended_class": recommended_class,
                "layout": layout,
                "needs_action": overflow > 300  # Critical threshold
            })

# Print analysis
print(f"{'Slide':<8} {'Overflow':<12} {'Chars':<8} {'Current':<15} {'Recommended':<15} {'Action':<20}")
print("-" * 90)

for item in sorted(analysis, key=lambda x: x["overflow"], reverse=True):
    action = ""
    if item["overflow"] > 600:
        action = "SPLIT or MAJOR CUT"
    elif item["overflow"] > 300:
        action = "Upgrade + reduce"
    elif item["overflow"] > 100:
        action = "Upgrade class"
    else:
        action = "Minor optimization"

    print(f"{item['slide_number']:<8} {item['overflow']:<12.1f} {item['total_chars']:<8} {item['current_class']:<15} {item['recommended_class']:<15} {action:<20}")

print()
print("=" * 80)
print("RECOMMENDED ACTIONS:")
print("=" * 80)

critical = [a for a in analysis if a["overflow"] > 600]
high = [a for a in analysis if 300 < a["overflow"] <= 600]
medium = [a for a in analysis if 100 < a["overflow"] <= 300]

if critical:
    print(f"\n🔴 CRITICAL (>600px overflow): {len(critical)} slides")
    print("   → Split into multiple slides OR reduce content by 40-50%")
    for a in critical:
        print(f"   Slide {a['slide_number']}: {a['overflow']:.0f}px, {a['total_chars']} chars, {a['layout']}")

if high:
    print(f"\n🟠 HIGH (300-600px overflow): {len(high)} slides")
    print("   → Upgrade to ultracompact + reduce content by 30-40%")
    for a in high:
        print(f"   Slide {a['slide_number']}: {a['overflow']:.0f}px, {a['total_chars']} chars, {a['layout']}")

if medium:
    print(f"\n🟡 MEDIUM (100-300px overflow): {len(medium)} slides")
    print("   → Upgrade to supercompact/ultracompact + reduce content by 20-30%")
    for a in medium:
        print(f"   Slide {a['slide_number']}: {a['overflow']:.0f}px, {a['total_chars']} chars, {a['layout']}")
