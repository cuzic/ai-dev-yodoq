#!/usr/bin/env python3
"""
Update slide classes based on overflow data.
This script is more flexible and searches for slides by number.
"""

import re
import os

# Slide updates: slide_number → desired_class
SLIDE_UPDATES = {
    # Priority 1 - Large overflow (>200px), normal → compact/supercompact
    165: "supercompact",
    167: "supercompact",
    139: "supercompact",
    151: "supercompact",
    34: "compact",
    126: "compact",
    130: "compact",
    122: "compact",
    143: "compact",
    149: "compact",
    52: "compact",

    # Priority 2 - Medium overflow (100-200px), normal → compact
    60: "compact",
    66: "compact",
    36: "compact",
    79: "compact",
    5: "compact",
    137: "compact",
    61: "compact",
    38: "compact",

    # Priority 3 - Already compact, upgrade to supercompact
    150: "supercompact",
    118: "supercompact",
    22: "supercompact",
    81: "supercompact",
    135: "supercompact",
    26: "supercompact",
    89: "supercompact",
    125: "supercompact",
    142: "supercompact",
    131: "supercompact",
    132: "supercompact",
}

def get_file_for_slide(slide_num):
    """Determine which file contains the given slide number."""
    if 1 <= slide_num <= 45:
        return "day1_1.md"
    elif 46 <= slide_num <= 90:
        return "day1_2.md"
    elif 91 <= slide_num <= 117:
        return "day1_3.md"
    elif 118 <= slide_num <= 146:
        return "day2_1.md"
    elif 147 <= slide_num <= 177:
        return "day2_2.md"
    return None

def get_slide_offset(slide_num, filename):
    """Get the 0-based index within the file for a slide number."""
    # Note: First section in each file is front matter (---...---), so we add 1 to offset
    if filename == "day1_1.md":
        return slide_num  # Front matter is slide 0, so slide 1 is at index 1
    elif filename == "day1_2.md":
        return slide_num - 45  # Slides 46+ in day1_2.md
    elif filename == "day1_3.md":
        return slide_num - 90  # Slides 91+ in day1_3.md
    elif filename == "day2_1.md":
        return slide_num - 117  # Slides 118+ in day2_1.md
    elif filename == "day2_2.md":
        return slide_num - 146  # Slides 147+ in day2_2.md
    return None

def update_slide_class(slide_content, target_class):
    """Update or add the class to the _class directive."""

    # Pattern to find _class directive
    class_pattern = r'<!--\s*_class:\s*([^>]+?)\s*-->'

    match = re.search(class_pattern, slide_content)
    if not match:
        # No _class directive found
        print(f"    ⚠ No _class directive found")
        return slide_content

    current_classes = match.group(1).strip()

    # Parse current classes
    class_parts = current_classes.split()

    # Remove existing compact/supercompact/normal
    filtered_classes = [c for c in class_parts if c not in ['compact', 'supercompact', 'normal']]

    # Add target class
    new_classes = ' '.join(filtered_classes + [target_class])

    # Replace in content
    new_directive = f'<!-- _class: {new_classes} -->'
    updated = slide_content.replace(match.group(0), new_directive)

    return updated, current_classes, new_classes

def process_file(filepath, updates):
    """Process a file and update specified slides."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into slides
    slides = content.split('\n---\n')

    changes_made = 0
    filename = os.path.basename(filepath)

    for slide_num, target_class in updates.items():
        offset = get_slide_offset(slide_num, filename)

        if offset is None or offset >= len(slides):
            continue

        slide_content = slides[offset]
        result = update_slide_class(slide_content, target_class)

        if isinstance(result, tuple):
            updated_content, old_classes, new_classes = result

            if updated_content != slide_content:
                slides[offset] = updated_content
                changes_made += 1
                print(f"  ✓ Slide {slide_num}: '{old_classes}' → '{new_classes}'")
        else:
            print(f"  ✗ Slide {slide_num}: Could not update")

    if changes_made > 0:
        # Write back
        new_content = '\n---\n'.join(slides)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\n✓ {filename}: {changes_made} changes saved\n")

    return changes_made

def main():
    base_path = "/home/cuzic/ai-dev-yodoq/slides"

    # Group updates by file
    files_to_update = {}
    for slide_num, target_class in SLIDE_UPDATES.items():
        filename = get_file_for_slide(slide_num)
        if filename:
            if filename not in files_to_update:
                files_to_update[filename] = {}
            files_to_update[filename][slide_num] = target_class

    print("=" * 80)
    print("UPDATING SLIDE CLASSES TO FIX OVERFLOW")
    print("=" * 80)
    print()

    total_changes = 0

    for filename in sorted(files_to_update.keys()):
        filepath = os.path.join(base_path, filename)
        updates = files_to_update[filename]

        print(f"Processing {filename} ({len(updates)} slides)...")
        print("-" * 80)

        changes = process_file(filepath, updates)
        total_changes += changes

    print()
    print("=" * 80)
    print(f"TOTAL: {total_changes} slides updated")
    print("=" * 80)
    print()

    # Count by type
    to_compact = sum(1 for c in SLIDE_UPDATES.values() if c == "compact")
    to_supercompact = sum(1 for c in SLIDE_UPDATES.values() if c == "supercompact")

    print(f"Updates to compact: {to_compact}")
    print(f"Updates to supercompact: {to_supercompact}")
    print()
    print("Next: Regenerate all_slides.md")

if __name__ == "__main__":
    main()
