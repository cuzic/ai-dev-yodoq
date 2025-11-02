#!/usr/bin/env python3
"""
Implement layout changes for slides with excessive whitespace.
This script modifies the day*.md files to apply the recommended layout classes.
"""

import re
import json
import sys
from pathlib import Path

def find_slide_in_files(slide_num, day_files):
    """Find which file contains a specific slide number."""
    current_slide = 0
    for day_file in day_files:
        with open(day_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count slides in this file
        slides = content.split('\n---\n')
        if current_slide + len(slides) >= slide_num:
            return day_file, slide_num - current_slide - 1  # Return file and local index
        current_slide += len(slides)

    return None, None

def update_slide_layout(slide_content, action, new_layout):
    """Update the layout class for a slide."""

    # Find existing class declaration
    class_match = re.search(r'<!--\s*_class:\s*([^-]*?)-->', slide_content)

    if action == 'add_two_column':
        if class_match:
            # Append to existing classes
            existing = class_match.group(1).strip()
            new_classes = f"{existing} two-column".strip()
            new_content = re.sub(
                r'<!--\s*_class:\s*[^-]*?-->',
                f'<!-- _class: {new_classes} -->',
                slide_content,
                count=1
            )
        else:
            # Add new class declaration at the start
            new_content = f'<!-- _class: two-column -->\n\n{slide_content}'
        return new_content

    elif action == 'add_card_grid':
        if class_match:
            existing = class_match.group(1).strip()
            new_classes = f"{existing} card-grid".strip()
            new_content = re.sub(
                r'<!--\s*_class:\s*[^-]*?-->',
                f'<!-- _class: {new_classes} -->',
                slide_content,
                count=1
            )
        else:
            new_content = f'<!-- _class: card-grid -->\n\n{slide_content}'
        return new_content

    elif action == 'add_horizontal':
        if class_match:
            existing = class_match.group(1).strip()
            new_classes = f"{existing} layout-horizontal-left".strip()
            new_content = re.sub(
                r'<!--\s*_class:\s*[^-]*?-->',
                f'<!-- _class: {new_classes} -->',
                slide_content,
                count=1
            )
        else:
            new_content = f'<!-- _class: layout-horizontal-left -->\n\n{slide_content}'
        return new_content

    elif action == 'change_to_two_column':
        if class_match:
            # Replace layout class but keep compact classes
            existing = class_match.group(1).strip()
            # Remove existing layout classes
            classes = existing.split()
            compact_classes = [c for c in classes if 'compact' in c.lower()]
            new_classes = 'two-column ' + ' '.join(compact_classes)
            new_content = re.sub(
                r'<!--\s*_class:\s*[^-]*?-->',
                f'<!-- _class: {new_classes.strip()} -->',
                slide_content,
                count=1
            )
        else:
            new_content = f'<!-- _class: two-column -->\n\n{slide_content}'
        return new_content

    elif action == 'change_to_horizontal':
        if class_match:
            existing = class_match.group(1).strip()
            classes = existing.split()
            compact_classes = [c for c in classes if 'compact' in c.lower()]
            new_classes = 'layout-horizontal-left ' + ' '.join(compact_classes)
            new_content = re.sub(
                r'<!--\s*_class:\s*[^-]*?-->',
                f'<!-- _class: {new_classes.strip()} -->',
                slide_content,
                count=1
            )
        else:
            new_content = f'<!-- _class: layout-horizontal-left -->\n\n{slide_content}'
        return new_content

    elif action == 'change_to_card_grid':
        if class_match:
            existing = class_match.group(1).strip()
            classes = existing.split()
            compact_classes = [c for c in classes if 'compact' in c.lower()]
            new_classes = 'card-grid ' + ' '.join(compact_classes)
            new_content = re.sub(
                r'<!--\s*_class:\s*[^-]*?-->',
                f'<!-- _class: {new_classes.strip()} -->',
                slide_content,
                count=1
            )
        else:
            new_content = f'<!-- _class: card-grid -->\n\n{slide_content}'
        return new_content

    elif action == 'remove_layout':
        if class_match:
            existing = class_match.group(1).strip()
            classes = existing.split()
            # Keep only compact classes
            compact_classes = [c for c in classes if 'compact' in c.lower()]
            if compact_classes:
                new_classes = ' '.join(compact_classes)
                new_content = re.sub(
                    r'<!--\s*_class:\s*[^-]*?-->',
                    f'<!-- _class: {new_classes} -->',
                    slide_content,
                    count=1
                )
            else:
                # Remove class declaration entirely
                new_content = re.sub(
                    r'<!--\s*_class:\s*[^-]*?-->\s*\n?',
                    '',
                    slide_content,
                    count=1
                )
            return new_content
        return slide_content

    elif action == 'remove_lead':
        if class_match:
            existing = class_match.group(1).strip()
            classes = existing.split()
            # Remove 'lead' but keep other classes
            other_classes = [c for c in classes if c.lower() != 'lead']
            if other_classes:
                new_classes = ' '.join(other_classes)
                new_content = re.sub(
                    r'<!--\s*_class:\s*[^-]*?-->',
                    f'<!-- _class: {new_classes} -->',
                    slide_content,
                    count=1
                )
            else:
                new_content = re.sub(
                    r'<!--\s*_class:\s*[^-]*?-->\s*\n?',
                    '',
                    slide_content,
                    count=1
                )
            return new_content
        return slide_content

    elif action == 'add_content':
        # Skip - needs manual intervention
        print(f"  SKIP: Needs content addition (manual intervention required)")
        return slide_content

    elif action == 'review_manual':
        # Skip - needs manual review
        print(f"  SKIP: Needs manual review")
        return slide_content

    else:
        print(f"  SKIP: Unknown action '{action}'")
        return slide_content

def main():
    # Load implementation plan
    with open('.logs/final_recommendations.json', 'r') as f:
        recommendations = json.load(f)

    # Filter to actionable items
    actionable = [r for r in recommendations if r['priority'] < 10]

    # Filter out 'add_content' and 'review_manual' actions for now
    implementable = [r for r in actionable if r['action'] not in ['add_content', 'review_manual']]

    print(f"Total actionable recommendations: {len(actionable)}")
    print(f"Implementable (excluding content additions): {len(implementable)}")
    print(f"\nWill implement top 50 layout changes...")
    print("="*80)

    day_files = ['day1_1.md', 'day1_2.md', 'day1_3.md', 'day2_1.md', 'day2_2.md']

    # Read all files
    file_contents = {}
    for day_file in day_files:
        with open(day_file, 'r', encoding='utf-8') as f:
            file_contents[day_file] = f.read()

    changes_made = 0
    skipped = 0

    for i, rec in enumerate(implementable[:50], 1):
        slide_num = rec['num']
        action = rec['action']

        print(f"\n{i}. Slide {slide_num} ({rec['whitespace']:.1f}% WS)")
        print(f"   Action: {action}")
        print(f"   Current: {rec['current_layout']}")
        print(f"   → New: {rec['new_layout']}")

        # Find the slide in files
        current_slide = 0
        found = False

        for day_file in day_files:
            slides = file_contents[day_file].split('\n---\n')

            if current_slide + len(slides) > slide_num:
                # This file contains our slide
                local_idx = slide_num - current_slide - 1

                if 0 <= local_idx < len(slides):
                    old_content = slides[local_idx]
                    new_content = update_slide_layout(old_content, action, rec['new_layout'])

                    if new_content != old_content:
                        slides[local_idx] = new_content
                        file_contents[day_file] = '\n---\n'.join(slides)
                        print(f"   ✓ Updated in {day_file}")
                        changes_made += 1
                        found = True
                    else:
                        print(f"   - No changes made")
                        skipped += 1
                    break

            current_slide += len(slides)

        if not found:
            print(f"   ! Slide {slide_num} not found")
            skipped += 1

    # Write back all modified files
    print(f"\n{'='*80}")
    print(f"Writing changes to files...")
    for day_file, content in file_contents.items():
        with open(day_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {day_file}")

    print(f"\n{'='*80}")
    print(f"SUMMARY:")
    print(f"  Changes made: {changes_made}")
    print(f"  Skipped: {skipped}")
    print(f"  Files modified: {len(day_files)}")
    print(f"\nNext step: Regenerate all_slides.md")

if __name__ == '__main__':
    main()
