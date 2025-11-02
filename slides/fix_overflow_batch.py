#!/usr/bin/env python3
"""
Batch fix overflow slides by updating their _class directives.
"""

import re
import sys

# Map of slide numbers to their changes
# Format: slide_number: (current_class, new_class, layout_type, overflow_px, file)
SLIDE_CHANGES = {
    # Priority 1 - Large overflow (>200px), normal → compact/supercompact
    5: ("normal", "compact", "lead", 87, "day1_1.md"),
    34: ("normal", "compact", "layout-callout", 255, "day1_1.md"),
    36: ("normal", "compact", "two-column", 99, "day1_1.md"),
    38: ("normal", "compact", "layout-callout", 49, "day1_1.md"),
    52: ("normal", "compact", "card-grid", 204, "day1_2.md"),
    60: ("normal", "compact", "card-grid", 178, "day1_2.md"),
    61: ("normal", "compact", "layout-horizontal-right", 60, "day1_2.md"),
    66: ("normal", "compact", "layout-diagram-only", 145, "day1_2.md"),
    79: ("normal", "compact", "layout-horizontal-left", 92, "day1_2.md"),
    122: ("normal", "compact", "card-grid", 240, "day2_1.md"),
    126: ("normal", "compact", "card-grid", 246, "day2_1.md"),
    130: ("normal", "compact", "layout-horizontal-left", 242, "day2_1.md"),
    137: ("normal", "compact", "card-grid", 77, "day2_1.md"),
    139: ("normal", "supercompact", "layout-horizontal-left", 399, "day2_1.md"),
    143: ("normal", "compact", "card-grid", 231, "day2_1.md"),
    149: ("normal", "compact", "lead", 212, "day2_2.md"),
    151: ("normal", "supercompact", "layout-horizontal-right", 384, "day2_2.md"),
    165: ("normal", "supercompact", "layout-horizontal-right", 733, "day2_2.md"),
    167: ("normal", "supercompact", "card-grid", 417, "day2_2.md"),

    # Priority 3 - Already compact, upgrade to supercompact
    22: ("compact", "supercompact", "layout-diagram-only", 188, "day1_1.md"),
    26: ("compact", "supercompact", "layout-horizontal-right", 82, "day1_1.md"),
    81: ("compact", "supercompact", "two-column", 170, "day1_2.md"),
    89: ("compact", "supercompact", "lead", 80, "day1_2.md"),
    118: ("compact", "supercompact", "lead", 254, "day2_1.md"),
    125: ("compact", "supercompact", "layout-horizontal-right", 80, "day2_1.md"),
    131: ("compact", "supercompact", "lead", 64, "day2_1.md"),
    132: ("compact", "supercompact", "layout-horizontal-right", 38, "day2_1.md"),
    135: ("compact", "supercompact", "layout-callout", 122, "day2_1.md"),
    142: ("compact", "supercompact", "card-grid", 75, "day2_1.md"),
    150: ("compact", "supercompact", "card-grid", 286, "day2_2.md"),

    # Special cases - already supercompact (will handle manually)
    112: ("supercompact", "supercompact", "lead", 128, "day1_3.md"),
    123: ("supercompact", "supercompact", "layout-timeline", 77, "day2_1.md"),
}

def get_slide_file_map():
    """Determine which file each slide belongs to based on cumulative counts."""
    # Approximate slide counts per file
    file_ranges = [
        ("day1_1.md", 1, 45),
        ("day1_2.md", 46, 90),
        ("day1_3.md", 91, 117),
        ("day2_1.md", 118, 146),
        ("day2_2.md", 147, 177),
    ]

    slide_to_file = {}
    for filename, start, end in file_ranges:
        for slide_num in range(start, end + 1):
            slide_to_file[slide_num] = filename

    return slide_to_file

def find_slide_in_file(content, slide_number):
    """Find the slide section in the file content."""
    slides = content.split('\n---\n')

    if slide_number - 1 < len(slides):
        return slides[slide_number - 1]

    return None

def update_class_directive(slide_content, old_class, new_class, layout_type):
    """Update the _class directive in slide content."""

    # Pattern to match _class directive
    # Handles: <!-- _class: layout-name --> or <!-- _class: layout-name old-class -->
    pattern = r'(<!--\s*_class:\s*)(' + re.escape(layout_type) + r')(\s+\w+)?\s*(-->)'

    def replace_func(match):
        prefix = match.group(1)
        layout = match.group(2)
        suffix = match.group(4)

        # If already has supercompact and we're trying to add supercompact, keep it
        if old_class == "supercompact" and new_class == "supercompact":
            return match.group(0)  # No change

        # Otherwise, add or replace the class
        return f"{prefix}{layout} {new_class} {suffix}"

    updated = re.sub(pattern, replace_func, slide_content)

    return updated

def process_file(filepath, slide_changes):
    """Process a single file and update all relevant slides."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into slides
    slides = content.split('\n---\n')

    # Determine starting slide number for this file
    filename = filepath.split('/')[-1]
    slide_to_file = get_slide_file_map()

    # Find first slide number for this file
    start_slide = None
    for slide_num, file in slide_to_file.items():
        if file == filename:
            start_slide = slide_num
            break

    if start_slide is None:
        print(f"Could not determine starting slide for {filename}")
        return 0

    changes_made = 0

    # Process each slide that needs updating
    for i, slide in enumerate(slides):
        current_slide_num = start_slide + i

        if current_slide_num in slide_changes:
            old_class, new_class, layout_type, overflow, _ = slide_changes[current_slide_num]

            # Skip if no change needed
            if old_class == new_class and old_class == "supercompact":
                continue

            updated_slide = update_class_directive(slide, old_class, new_class, layout_type)

            if updated_slide != slide:
                slides[i] = updated_slide
                changes_made += 1
                print(f"✓ Slide {current_slide_num}: {layout_type} {old_class} → {new_class} (overflow: {overflow}px)")
            else:
                print(f"✗ Slide {current_slide_num}: No change made (may need manual review)")

    if changes_made > 0:
        # Write back
        new_content = '\n---\n'.join(slides)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n✓ Updated {filepath}: {changes_made} slides changed\n")

    return changes_made

def main():
    base_path = "/home/cuzic/ai-dev-yodoq/slides"

    # Group changes by file
    files_to_process = {}
    for slide_num, (old_class, new_class, layout_type, overflow, filename) in SLIDE_CHANGES.items():
        if filename not in files_to_process:
            files_to_process[filename] = {}
        files_to_process[filename][slide_num] = (old_class, new_class, layout_type, overflow, filename)

    total_changes = 0
    normal_to_compact = 0
    compact_to_supercompact = 0

    print("=" * 80)
    print("BATCH OVERFLOW FIX - UPDATING SLIDE CLASSES")
    print("=" * 80)
    print()

    for filename in sorted(files_to_process.keys()):
        filepath = f"{base_path}/{filename}"
        print(f"Processing {filename}...")
        print("-" * 80)

        slide_changes = files_to_process[filename]
        changes = process_file(filepath, slide_changes)
        total_changes += changes

        # Count change types
        for slide_num, (old_class, new_class, _, _, _) in slide_changes.items():
            if old_class == "normal" and new_class in ["compact", "supercompact"]:
                normal_to_compact += 1
            elif old_class == "compact" and new_class == "supercompact":
                compact_to_supercompact += 1

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total slides updated: {total_changes}")
    print(f"Normal → Compact/Supercompact: {normal_to_compact}")
    print(f"Compact → Supercompact: {compact_to_supercompact}")
    print()
    print("Next steps:")
    print("1. Review slides 112 and 123 (already supercompact) for content reduction")
    print("2. Regenerate all_slides.md")
    print("3. Run overflow detection to verify improvements")
    print()

if __name__ == "__main__":
    main()
