#!/usr/bin/env python3
"""
Directly fix overflow in all_slides.md by adding compact/supercompact classes
"""

import json
import re
from pathlib import Path

# Load measurement report
with open('/tmp/slide_measurement_report.json') as f:
    data = json.load(f)

# Read all_slides.md
with open('all_slides.md', 'r') as f:
    content = f.read()

slides = content.split('\n---\n')

print(f"Total slides in all_slides.md: {len(slides)}")
print(f"Measurement report has {len(data['slides'])} slides")

# Categorize slides by overflow
slides_to_fix = {}  # slide_index -> 'compact' or 'supercompact'

for s in data['slides']:
    if s['hasOverflow']:
        max_overflow = max([e['overflowY'] for e in s['overflowElements']] + [0])
        slide_idx = s['slideIndex']  # This is 0-based

        if max_overflow > 100:
            slides_to_fix[slide_idx] = 'supercompact'
        elif max_overflow > 30:
            slides_to_fix[slide_idx] = 'compact'
    elif s['density'] > 0.75:
        # High density even without overflow
        slide_idx = s['slideIndex']
        if slide_idx not in slides_to_fix:
            slides_to_fix[slide_idx] = 'compact'

print(f"\nSlides to fix: {len(slides_to_fix)}")
supercompact_count = sum(1 for v in slides_to_fix.values() if v == 'supercompact')
compact_count = sum(1 for v in slides_to_fix.values() if v == 'compact')
print(f"  - supercompact: {supercompact_count}")
print(f"  - compact: {compact_count}")

# Pattern to match class declaration
class_pattern = r'<!-- _class: ([^>]+) -->'

modified_count = 0

for slide_idx, target_class in slides_to_fix.items():
    if slide_idx >= len(slides):
        continue

    slide = slides[slide_idx]
    class_match = re.search(class_pattern, slide)

    if class_match:
        current_class = class_match.group(1).strip()

        # Check what we need to do
        has_supercompact = 'supercompact' in current_class
        has_compact = 'compact' in current_class

        if target_class == 'supercompact':
            if has_supercompact:
                continue  # Already has supercompact
            elif has_compact:
                # Upgrade compact to supercompact
                new_class = current_class.replace('compact', 'supercompact')
            else:
                # Add supercompact
                new_class = f"{current_class} supercompact"
        else:  # target_class == 'compact'
            if has_compact or has_supercompact:
                continue  # Already has compact or supercompact
            else:
                # Add compact
                new_class = f"{current_class} compact"

        # Replace in slide
        new_declaration = f"<!-- _class: {new_class} -->"
        old_declaration = class_match.group(0)
        slides[slide_idx] = slide.replace(old_declaration, new_declaration, 1)
        modified_count += 1

        if modified_count <= 10:
            print(f"Slide {slide_idx + 1}: {current_class} → {new_class}")

print(f"\nModified {modified_count} slides in all_slides.md")

# Write back
new_content = '\n---\n'.join(slides)
Path('all_slides.md').write_text(new_content)
print("Updated all_slides.md")
