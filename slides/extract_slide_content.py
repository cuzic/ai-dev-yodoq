"""
Extract content for specific slides to analyze
"""
import json
from pathlib import Path

# Target slides (top 10 worst)
target_slides = [72, 98, 86, 164, 138, 121, 142, 163, 148, 80]

# Map slide numbers to files
files = ["day1_1.md", "day1_2.md", "day1_3.md", "day2_1.md", "day2_2.md"]
slides_dir = Path("/home/cuzic/ai-dev-yodoq/slides")

slide_counter = 0
slide_info = {}

for filename in files:
    filepath = slides_dir / filename

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by slides
    slides = content.split("\n---\n")

    for i, slide in enumerate(slides):
        # Skip frontmatter
        if i == 0 and slide.strip().startswith("---\nmarp:"):
            continue

        slide_counter += 1

        if slide_counter in target_slides:
            # Extract title (first # line)
            lines = slide.strip().split("\n")
            title = ""
            for line in lines:
                if line.startswith("#"):
                    title = line.strip()
                    break

            # Count lines and chars
            content_lines = [l for l in lines if l.strip() and not l.strip().startswith("<!--")]
            num_lines = len(content_lines)
            num_chars = sum(len(l) for l in content_lines)

            slide_info[slide_counter] = {
                "file": filename,
                "title": title,
                "num_lines": num_lines,
                "num_chars": num_chars,
                "content": slide[:500]  # First 500 chars for preview
            }

# Print summary
print("=" * 80)
print("TOP 10 WORST FAIL SLIDES - CONTENT ANALYSIS")
print("=" * 80)

for slide_num in target_slides:
    if slide_num in slide_info:
        info = slide_info[slide_num]
        print(f"\nSlide {slide_num} ({info['file']})")
        print(f"  Title: {info['title']}")
        print(f"  Lines: {info['num_lines']}, Chars: {info['num_chars']}")
        print(f"  Preview: {info['content'][:100]}...")

# Save detailed info
output_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/slide_content_analysis.json")
with open(output_file, "w") as f:
    json.dump(slide_info, f, indent=2, ensure_ascii=False)

print(f"\nDetailed analysis saved to {output_file}")
