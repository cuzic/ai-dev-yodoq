#!/usr/bin/env python3
"""
Automatically add 'compact' class to slides that need it based on measurement report
"""

import json
import re
from pathlib import Path

# Load measurement report
with open('/tmp/slide_measurement_report.json') as f:
    data = json.load(f)

# Load all_slides.md to map slide numbers to content
with open('all_slides.md', 'r') as f:
    content = f.read()

slides_content = content.split('\n---\n')

# Find slides needing compact class
slides_to_fix = set()
for s in data['slides']:
    max_overflow = 0
    if s['hasOverflow']:
        max_overflow = max([e['overflowY'] for e in s['overflowElements']] + [0])

    # Add compact if overflow > 50px or density > 70%
    if max_overflow > 50 or s['density'] > 0.70:
        slides_to_fix.add(s['slideIndex'] + 1)

print(f"Found {len(slides_to_fix)} slides needing compact class")

# Map slides to day files (approximate boundaries)
def get_day_file_and_range(slide_num):
    """Get the day file and approximate slide range for a given slide number"""
    # These are approximate - will need to count actual slides
    if slide_num <= 36:
        return 'day1_1.md', (1, 36)
    elif slide_num <= 72:
        return 'day1_2.md', (37, 72)
    elif slide_num <= 108:
        return 'day1_3.md', (73, 108)
    elif slide_num <= 144:
        return 'day2_1.md', (109, 144)
    else:
        return 'day2_2.md', (145, 168)

# Process each day file
day_files = ['day1_1.md', 'day1_2.md', 'day1_3.md', 'day2_1.md', 'day2_2.md']

# First, we need to accurately map slides to day files by counting
slide_counter = 0
day_file_ranges = {}
current_day_start = 1

for day_file in day_files:
    day_content = Path(day_file).read_text()
    # Count slides (page separators) in this file
    slide_count = day_content.count('\n---\n')
    day_file_ranges[day_file] = (current_day_start, current_day_start + slide_count)
    current_day_start += slide_count + 1

print(f"\nDay file ranges:")
for day_file, (start, end) in day_file_ranges.items():
    print(f"  {day_file}: slides {start}-{end}")

# Now process each day file
total_modified = 0

for day_file in day_files:
    day_path = Path(day_file)
    content = day_path.read_text()
    original_content = content

    start_slide, end_slide = day_file_ranges[day_file]
    slides_to_fix_in_file = [s for s in slides_to_fix if start_slide <= s <= end_slide]

    if not slides_to_fix_in_file:
        print(f"\n{day_file}: No slides to fix")
        continue

    print(f"\n{day_file}: {len(slides_to_fix_in_file)} slides to fix")

    # We need to be more selective - only add compact to slides we identified
    # Split by page separator to work slide-by-slide
    slides_in_file = content.split('\n---\n')

    # Calculate which local slide indices need compact
    local_slides_to_fix = [s - start_slide + 1 for s in slides_to_fix_in_file]

    # Pattern to match: <!-- _class: xxx -->
    pattern = r'<!-- _class: ([^-][^>]+?) -->'

    modified_count = 0

    for i, slide in enumerate(slides_in_file):
        # Slide numbers are 1-based, but list is 0-based
        # First slide in file is at index 0
        local_slide_num = i + 1

        if local_slide_num in local_slides_to_fix:
            # This slide needs compact
            def add_compact(match):
                class_attr = match.group(1).strip()
                # Check if compact already exists
                if 'compact' in class_attr:
                    return match.group(0)  # Already has compact
                # Add compact
                return f"<!-- _class: {class_attr} compact -->"

            original_slide = slide
            slide_modified = re.sub(pattern, add_compact, slide)
            if slide_modified != original_slide:
                modified_count += 1
            slides_in_file[i] = slide_modified

    # Reconstruct file
    new_content = '\n---\n'.join(slides_in_file)

    if new_content != original_content:
        day_path.write_text(new_content)
        print(f"  Modified {modified_count} slides")
        total_modified += modified_count
    else:
        print(f"  No changes made (slides may already have compact)")

print(f"\n{'='*60}")
print(f"Total slides modified: {total_modified}")
print(f"{'='*60}")
print("\nNext steps:")
print("  1. Regenerate all_slides.md")
print("  2. Rebuild HTML")
print("  3. Re-measure to verify improvements")
