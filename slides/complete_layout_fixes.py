#!/usr/bin/env python3
"""
Complete the remaining layout changes that weren't fully applied.
"""

import re

# Define the specific changes needed
CHANGES = {
    88: {
        'from': 'card-grid',
        'to': 'two-column',
        'title': 'Part 2のキーポイント'
    },
    108: {
        'from': 'card-grid',
        'to': 'two-column',
        'title': '演習で体感できること'
    },
    123: {
        'from': 'layout-horizontal-left',
        'to': 'two-column',
        'title': 'AIの制約を理解する'
    },
    124: {
        'from': 'layout-horizontal-right',
        'to': 'two-column',
        'title': 'ドキュメント自動生成'
    },
    129: {
        'from': 'layout-horizontal-right',
        'to': 'two-column',
        'title': '影響範囲調査の手法'
    },
    134: {
        'from': 'layout-horizontal-right',
        'to': 'two-column',
        'title': 'デグレ防止の重要性'
    },
    139: {
        'from': 'card-grid',
        'to': 'two-column',
        'title': 'テストシナリオからテストコードへ'
    },
    143: {
        'from': 'lead',
        'to': 'normal',  # Just remove lead
        'title': 'Day 2-2: 実践演習'
    },
    162: {
        'from': 'card-grid',
        'to': 'two-column',
        'title': '代表者2-3名の成果発表'
    },
    163: {
        'from': 'card-grid',
        'to': 'two-column',
        'title': 'つまづいたポイント共有'
    }
}

def process_file(filename, start_slide):
    """Process a single markdown file."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by slide separators
    slides = content.split('\n---\n')
    modified = False

    # Track slide numbers
    slide_num = start_slide - 1  # Adjust for this file
    for i, slide in enumerate(slides):
        # Skip frontmatter
        if slide.strip().startswith('---\nmarp:'):
            continue

        slide_num += 1

        # Check if this slide needs changes
        if slide_num in CHANGES:
            change = CHANGES[slide_num]
            print(f"Processing slide {slide_num}: {change['title'][:40]}")

            # Find existing class
            class_match = re.search(r'<!-- _class: (.+?) -->', slide)

            if class_match:
                old_classes = class_match.group(1)
                print(f"  Current: {old_classes}")

                # Determine new classes
                if change['to'] == 'normal':
                    # Remove the class declaration
                    new_slide = re.sub(r'<!-- _class: .+? -->\n\n', '', slide)
                    slides[i] = new_slide
                    modified = True
                    print(f"  Changed: Removed class declaration")

                elif change['from'] in old_classes:
                    # Replace the old layout with new one
                    new_classes = re.sub(
                        r'\b' + re.escape(change['from']) + r'\b',
                        change['to'],
                        old_classes
                    )

                    # Also remove layout-horizontal-left/right patterns
                    new_classes = re.sub(r'\blayout-horizontal-(?:left|right)\b', change['to'], new_classes)

                    # Clean up duplicate classes
                    classes_list = new_classes.split()
                    seen = set()
                    clean_classes = []
                    for cls in classes_list:
                        if cls not in seen:
                            clean_classes.append(cls)
                            seen.add(cls)
                    new_classes = ' '.join(clean_classes)

                    new_slide = re.sub(
                        r'<!-- _class: .+? -->',
                        f'<!-- _class: {new_classes} -->',
                        slide
                    )
                    slides[i] = new_slide
                    modified = True
                    print(f"  Changed: {new_classes}")
                else:
                    print(f"  Warning: '{change['from']}' not found in classes")
            else:
                print(f"  Warning: No class declaration found")

    if modified:
        # Rejoin slides
        new_content = '\n---\n'.join(slides)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✓ {filename} updated")
        return True

    return False

def main():
    """Process all markdown files."""
    files = ['day1_1.md', 'day1_2.md', 'day1_3.md', 'day2_1.md', 'day2_2.md']

    print("=" * 80)
    print("COMPLETING REMAINING LAYOUT CHANGES")
    print("=" * 80)
    print()

    # Track cumulative slide count across files
    cumulative_slides = 0
    total_modified = 0

    for filename in files:
        filepath = f'slides/{filename}'

        # Count slides in this file to get starting position
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        slides_in_file = content.split('\n---\n')
        # Don't count frontmatter
        actual_slides = sum(1 for s in slides_in_file if not s.strip().startswith('---\nmarp:'))

        print(f"\nProcessing {filename} (slides {cumulative_slides + 1}-{cumulative_slides + actual_slides}):")

        if process_file(filepath, cumulative_slides + 1):
            total_modified += 1

        cumulative_slides += actual_slides

    print()
    print("=" * 80)
    print(f"COMPLETED: {len(CHANGES)} layout changes applied to {total_modified} files")
    print("=" * 80)

if __name__ == '__main__':
    main()
