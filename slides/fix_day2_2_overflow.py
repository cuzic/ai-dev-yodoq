#!/usr/bin/env python3
"""
Fix overflow issues in day2_2.md slides
"""

from pathlib import Path

# Read the file
content = Path('/home/cuzic/ai-dev-yodoq/slides/day2_2.md').read_text()

# Split into slides
slides = content.split('\n---\n')

# Slide numbers to fix (user provided these) - ordered by severity
target_slides = {
    165: 471.4,
    150: 340.2,
    167: 282.4,
    151: 260.1,
    163: 148.8,
    156: 141.0,
    145: 115.5
}

print(f"Total slides in day2_2.md: {len(slides)}")
print(f"\nTarget slides to fix: {len(target_slides)}")
print("="*80)

# Output each target slide with its content
for slide_num in sorted(target_slides.keys(), key=lambda x: target_slides[x], reverse=True):
    overflow = target_slides[slide_num]
    # Slides are 1-indexed, array is 0-indexed
    # But day2_2.md starts from slide 144, so we need to adjust
    # Actually, the slides in day2_2.md are part of a larger presentation
    # Let me just output what we have
    slide_idx = slide_num - 144  # Assuming day2_2 starts around slide 144

    if 0 <= slide_idx < len(slides):
        slide_content = slides[slide_idx]

        # Extract first few lines to identify the slide
        lines = slide_content.strip().split('\n')

        print(f"\n{'='*80}")
        print(f"SLIDE {slide_num} (overflow: {overflow}px) - Index: {slide_idx}")
        print(f"{'='*80}")
        for i, line in enumerate(lines[:30]):  # Show more lines for context
            print(f"{i+1:3d}: {line}")
        print(f"\n... (total {len(lines)} lines)")
        print(f"{'='*80}")
