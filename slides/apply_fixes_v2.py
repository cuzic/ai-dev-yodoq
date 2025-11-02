"""
Apply supercompact to worst overflow slides - Version 2
Uses accurate slide counting
"""
import re
from pathlib import Path

# Target slides to fix with supercompact
target_slides = [
    (80, 'supercompact'),
    (72, 'supercompact'),
    (98, 'supercompact'),
    (86, 'supercompact'),
    (164, 'supercompact'),
    (138, 'supercompact'),
]

# File boundaries (start slide number, filename, num slides)
files_info = [
    (1, 'day1_1.md', 44),
    (45, 'day1_2.md', 45),
    (90, 'day1_3.md', 27),
    (117, 'day2_1.md', 29),
    (146, 'day2_2.md', 31),
]

# Create mapping of slide_number -> (filename, slide_index_in_file)
slide_map = {}
for start, filename, count in files_info:
    for i in range(count):
        global_slide_num = start + i
        slide_map[global_slide_num] = (filename, i)

print("=" * 70)
print("APPLYING SUPERCOMPACT TO WORST OVERFLOW SLIDES")
print("=" * 70)

modifications = {}

for slide_num, fix_class in target_slides:
    if slide_num not in slide_map:
        print(f"  WARNING: Slide {slide_num} not found in map")
        continue

    filename, file_slide_idx = slide_map[slide_num]
    filepath = Path(f"/home/cuzic/ai-dev-yodoq/slides/{filename}")

    print(f"\nProcessing Slide {slide_num} ({filename}, index {file_slide_idx})...")

    # Read file
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into slides
    slides = content.split("\n---\n")

    # Handle frontmatter offset
    if slides[0].strip().startswith("---\nmarp:"):
        # Has frontmatter, so slide indices are file_slide_idx + 1
        actual_idx = file_slide_idx + 1
    else:
        actual_idx = file_slide_idx

    if actual_idx >= len(slides):
        print(f"  ERROR: Index {actual_idx} out of range (file has {len(slides)} slides)")
        continue

    slide = slides[actual_idx]

    # Check if already has supercompact
    if 'supercompact' in slide:
        print(f"  Already has 'supercompact' class")
        continue

    # Apply fix
    modified = False
    if "<!-- _class:" in slide:
        # Has existing class directive
        class_match = re.search(r'<!-- _class: (.+?) -->', slide)
        if class_match:
            current_classes = class_match.group(1)

            # Upgrade compact to supercompact
            if 'compact' in current_classes and fix_class == 'supercompact':
                new_classes = current_classes.replace('compact', 'supercompact')
            else:
                new_classes = f"{current_classes} {fix_class}"

            slides[actual_idx] = re.sub(
                r'<!-- _class: .+? -->',
                f'<!-- _class: {new_classes} -->',
                slide
            )
            print(f"  Modified: '{current_classes}' -> '{new_classes}'")
            modified = True
    else:
        # No class directive, add one
        lines = slide.split("\n")
        # Find first non-empty line
        insert_pos = 0
        for i, line in enumerate(lines):
            if line.strip():
                if line.strip().startswith("#"):
                    insert_pos = i + 1
                else:
                    insert_pos = i
                break

        lines.insert(insert_pos, f"<!-- _class: {fix_class} -->")
        slides[actual_idx] = "\n".join(lines)
        print(f"  Added: {fix_class}")
        modified = True

    if modified:
        # Write back
        new_content = "\n---\n".join(slides)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        if filename not in modifications:
            modifications[filename] = []
        modifications[filename].append((slide_num, fix_class))

print("\n" + "=" * 70)
print("MODIFICATIONS SUMMARY")
print("=" * 70)

total = sum(len(mods) for mods in modifications.values())
print(f"Total modifications: {total}\n")

for filename, mods in modifications.items():
    print(f"{filename}:")
    for slide_num, fix_class in mods:
        print(f"  Slide {slide_num}: Applied '{fix_class}'")
