#!/usr/bin/env python3
"""
Fix overflow issues in day2_1.md slides
"""

from pathlib import Path

# Read the file
content = Path('/home/cuzic/ai-dev-yodoq/slides/day2_1.md').read_text()

# Split into slides
slides = content.split('\n---\n')

# Slide numbers to fix (user provided these)
target_slides = {
    123: 447.2,
    118: 298.8,
    139: 269.6,
    120: 264.9,
    126: 227.0,
    131: 177.3,
    135: 176.8,
    121: 169.7,
    125: 167.3,
    142: 160.5,
    122: 135.9,
    130: 112.6
}

print(f"Total slides in day2_1.md: {len(slides)}")
print(f"\nTarget slides to fix: {len(target_slides)}")
print("="*80)

# Output each target slide with its content
for slide_num in sorted(target_slides.keys()):
    overflow = target_slides[slide_num]
    # Slides are 1-indexed, array is 0-indexed
    slide_idx = slide_num - 1

    if slide_idx < len(slides):
        slide_content = slides[slide_idx]

        # Extract first few lines to identify the slide
        lines = slide_content.strip().split('\n')
        preview_lines = lines[:10]

        print(f"\n{'='*80}")
        print(f"SLIDE {slide_num} (overflow: {overflow}px)")
        print(f"{'='*80}")
        print('\n'.join(preview_lines))
        print(f"\n... (total {len(lines)} lines)")
        print(f"{'='*80}")
