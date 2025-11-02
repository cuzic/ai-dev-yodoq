#!/usr/bin/env python3
"""
Upgrade 'compact' to 'supercompact' for slides with severe overflow (>100px)
"""

import json
import re
from pathlib import Path

# Load measurement report
with open('/tmp/slide_measurement_report.json') as f:
    data = json.load(f)

# Find slides with severe overflow (>100px)
slides_to_supercompact = set()
for s in data['slides']:
    if s['hasOverflow']:
        max_overflow = max([e['overflowY'] for e in s['overflowElements']] + [0])
        if max_overflow > 100:
            slides_to_supercompact.add(s['slideIndex'] + 1)

print(f"Found {len(slides_to_supercompact)} slides with severe overflow (>100px)")
print(f"Will upgrade 'compact' to 'supercompact' for these slides")

# Day file ranges (from previous script execution)
day_file_ranges = {
    'day1_1.md': (1, 45),
    'day1_2.md': (46, 90),
    'day1_3.md': (91, 117),
    'day2_1.md': (118, 146),
    'day2_2.md': (147, 177)
}

# Process each day file
day_files = ['day1_1.md', 'day1_2.md', 'day1_3.md', 'day2_1.md', 'day2_2.md']
total_modified = 0

for day_file in day_files:
    day_path = Path(day_file)
    content = day_path.read_text()
    original_content = content

    start_slide, end_slide = day_file_ranges[day_file]
    slides_in_file = [s for s in slides_to_supercompact if start_slide <= s <= end_slide]

    if not slides_in_file:
        continue

    print(f"\n{day_file}: {len(slides_in_file)} slides to upgrade")

    # Split by page separator
    slides_content = content.split('\n---\n')

    # Calculate which local slide indices need supercompact
    local_slides = [s - start_slide + 1 for s in slides_in_file]

    modified_count = 0

    for i, slide in enumerate(slides_content):
        local_slide_num = i + 1

        if local_slide_num in local_slides:
            # Replace 'compact' with 'supercompact'
            # Pattern: <!-- _class: ... compact -->
            pattern = r'<!-- _class: ([^>]*)\bcompact\b([^>]*) -->'

            def replace_compact(match):
                before = match.group(1).strip()
                after = match.group(2).strip()
                # Combine and clean up
                parts = [before, 'supercompact', after]
                class_attr = ' '.join([p for p in parts if p]).strip()
                return f"<!-- _class: {class_attr} -->"

            original_slide = slide
            slide_modified = re.sub(pattern, replace_compact, slide)

            if slide_modified != original_slide:
                modified_count += 1
                slides_content[i] = slide_modified

    # Reconstruct file
    new_content = '\n---\n'.join(slides_content)

    if new_content != original_content:
        day_path.write_text(new_content)
        print(f"  Modified {modified_count} slides")
        total_modified += modified_count

print(f"\n{'='*60}")
print(f"Total slides upgraded to supercompact: {total_modified}")
print(f"{'='*60}")
