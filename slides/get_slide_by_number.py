"""
Get full content of a specific slide by number
"""
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python get_slide_by_number.py <slide_number>")
    sys.exit(1)

target_slide = int(sys.argv[1])

files = ["day1_1.md", "day1_2.md", "day1_3.md", "day2_1.md", "day2_2.md"]
slides_dir = Path("/home/cuzic/ai-dev-yodoq/slides")

slide_counter = 0

for filename in files:
    filepath = slides_dir / filename

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    slides = content.split("\n---\n")

    for i, slide in enumerate(slides):
        if i == 0 and slide.strip().startswith("---\nmarp:"):
            continue

        slide_counter += 1

        if slide_counter == target_slide:
            print(f"=== Slide {target_slide} in {filename} ===\n")
            print(slide)
            print(f"\n=== End of Slide {target_slide} ===")
            sys.exit(0)

print(f"Slide {target_slide} not found")
