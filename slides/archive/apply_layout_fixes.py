#!/usr/bin/env python3
"""
Apply recommended layout fixes from validation report.
"""

import re
from pathlib import Path

def add_layout_class(slide_text, layout_class):
    """Add or replace layout class in slide."""
    # Check if layout class already exists
    if re.search(r'<!--\s*_class:', slide_text):
        # Replace existing
        slide_text = re.sub(
            r'<!--\s*_class:\s*[\w-]+\s*-->',
            f'<!-- _class: {layout_class} -->',
            slide_text
        )
    else:
        # Add before first heading (any level)
        lines = slide_text.split('\n')
        new_lines = []
        inserted = False

        for i, line in enumerate(lines):
            if not inserted and re.match(r'^#{1,6}\s+', line):
                # Insert class directive before heading
                if new_lines and new_lines[-1].strip() == '':
                    # Remove trailing empty line
                    new_lines.pop()
                new_lines.append(f'<!-- _class: {layout_class} -->')
                new_lines.append('')
                new_lines.append(line)
                inserted = True
            else:
                new_lines.append(line)

        slide_text = '\n'.join(new_lines)
    return slide_text

def remove_layout_class(slide_text):
    """Remove layout class directive."""
    slide_text = re.sub(r'<!--\s*_class:\s*[\w-]+\s*-->\n*', '', slide_text)
    # Clean up extra newlines
    slide_text = re.sub(r'\n{3,}', '\n\n', slide_text)
    return slide_text

def apply_fixes(md_path):
    """Apply all recommended layout fixes."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into slides
    slides = content.split('\n---\n')

    fixes_applied = []

    # Define all changes
    changes = {
        # Priority 1: Default → Two-Column (12 slides)
        95: ('add', 'two-column'),
        114: ('add', 'two-column'),
        143: ('add', 'two-column'),
        148: ('add', 'two-column'),
        157: ('add', 'two-column'),
        159: ('add', 'two-column'),
        171: ('add', 'two-column'),
        172: ('add', 'two-column'),
        173: ('add', 'two-column'),
        186: ('add', 'two-column'),
        189: ('add', 'two-column'),
        212: ('add', 'two-column'),

        # Priority 1: Diagram-only → Horizontal (3 slides)
        33: ('replace', 'layout-horizontal-left'),
        46: ('replace', 'layout-horizontal-left'),
        61: ('replace', 'layout-horizontal-left'),

        # Priority 1: Diagram-only → Two-Column (2 slides)
        11: ('replace', 'two-column'),
        75: ('replace', 'two-column'),

        # Priority 1: Two-Column → Three-Column (1 slide)
        10: ('replace', 'three-column'),

        # Priority 1: Lead → Two-Column (1 slide)
        133: ('replace', 'two-column'),

        # Priority 2: Two-Column → Default (6 slides)
        52: ('remove', None),
        112: ('remove', None),
        170: ('remove', None),
        184: ('remove', None),
        190: ('remove', None),
        200: ('remove', None),

        # Priority 2: Horizontal → Diagram-Only (1 slide)
        42: ('replace', 'layout-diagram-only'),

        # Priority 3: Three-Column → Two-Column (1 slide)
        47: ('replace', 'two-column'),

        # Priority 3: Horizontal → Two-Column (1 slide)
        149: ('replace', 'two-column'),

        # Priority 3: Card-Grid → Two-Column (1 slide)
        99: ('replace', 'two-column'),
    }

    # Apply changes
    for slide_num, (action, layout) in sorted(changes.items()):
        if slide_num - 1 < len(slides):
            old_slide = slides[slide_num - 1]

            if action == 'add':
                new_slide = add_layout_class(old_slide, layout)
                fixes_applied.append(f"Slide {slide_num}: Added {layout}")
            elif action == 'replace':
                new_slide = add_layout_class(old_slide, layout)
                fixes_applied.append(f"Slide {slide_num}: Changed to {layout}")
            elif action == 'remove':
                new_slide = remove_layout_class(old_slide)
                fixes_applied.append(f"Slide {slide_num}: Removed layout class")

            slides[slide_num - 1] = new_slide

    # Reconstruct content
    new_content = '\n---\n'.join(slides)

    # Write back
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return fixes_applied

def main():
    md_path = Path(__file__).parent / 'all_slides.md'

    print("=" * 80)
    print("APPLYING LAYOUT FIXES")
    print("=" * 80)
    print()

    fixes = apply_fixes(md_path)

    print(f"✅ Applied {len(fixes)} fixes:\n")
    for fix in fixes:
        print(f"  • {fix}")

    print()
    print("=" * 80)
    print("COMPLETE - Run validate_layout_choices.py to verify")
    print("=" * 80)

if __name__ == '__main__':
    main()
