#!/usr/bin/env python3
"""
Automatically fix overflow issues by adding appropriate layout classes.
"""

import re
from pathlib import Path
import sys

def count_list_items_in_slide(slide_text):
    """Count list items in a slide."""
    return len(re.findall(r'^[-*+]\s', slide_text, re.MULTILINE))

def has_image(slide_text):
    """Check if slide has an image."""
    return bool(re.search(r'!\[.*?\]\(.*?\)', slide_text))

def get_layout_class(slide_text):
    """Extract existing layout class if any."""
    match = re.search(r'<!--\s*_class:\s*([^>]+)\s*-->', slide_text)
    return match.group(1).strip() if match else None

def suggest_layout(slide_text, list_item_count, has_img):
    """Suggest appropriate layout based on content."""
    existing_layout = get_layout_class(slide_text)

    # Skip if already has diagram-only or horizontal layout
    if existing_layout and ('diagram-only' in existing_layout or 'horizontal' in existing_layout):
        return None

    # If has image and lots of text, use horizontal layout
    if has_img and list_item_count > 8:
        return 'layout-horizontal-right'

    # If has image, prefer diagram layouts
    if has_img:
        return None  # Already has image, likely OK

    # Many list items = need multi-column
    if list_item_count >= 20:
        return 'three-column'
    elif list_item_count >= 12:
        return 'two-column'
    elif list_item_count >= 8:
        return 'two-column'

    return None

def fix_markdown_file(md_path, dry_run=False):
    """Fix overflow issues in a markdown file."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by slide separators
    slides = content.split('\n---\n')

    fixed_count = 0
    changes = []

    new_slides = []
    for i, slide in enumerate(slides):
        slide_num = i + 1

        # Skip empty slides
        if not slide.strip():
            new_slides.append(slide)
            continue

        # Count list items
        list_count = count_list_items_in_slide(slide)
        has_img = has_image(slide)

        # Get title
        title_match = re.search(r'^#\s+(.+)$', slide, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Slide {slide_num}"

        # Suggest layout
        suggested = suggest_layout(slide, list_count, has_img)

        if suggested:
            existing_layout = get_layout_class(slide)

            if existing_layout:
                # Replace existing layout
                new_layout = f'<!-- _class: {suggested} -->'
                old_layout = f'<!-- _class: {existing_layout} -->'
                new_slide = slide.replace(old_layout, new_layout)
            else:
                # Add layout before title
                lines = slide.split('\n')
                # Find first non-empty, non-comment line
                insert_idx = 0
                for idx, line in enumerate(lines):
                    if line.strip() and not line.strip().startswith('<!--'):
                        insert_idx = idx
                        break

                lines.insert(insert_idx, f'<!-- _class: {suggested} -->\n')
                new_slide = '\n'.join(lines)

            new_slides.append(new_slide)
            fixed_count += 1
            changes.append({
                'slide': slide_num,
                'title': title[:50],
                'list_items': list_count,
                'layout': suggested
            })
        else:
            new_slides.append(slide)

    if fixed_count > 0 and not dry_run:
        # Write back
        new_content = '\n---\n'.join(new_slides)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return fixed_count, changes

def main():
    dry_run = '--dry-run' in sys.argv

    print("=" * 80)
    print("AUTO-FIXING OVERFLOW ISSUES")
    if dry_run:
        print("(DRY RUN - no changes will be made)")
    print("=" * 80)
    print()

    slides_dir = Path(__file__).parent
    md_files = [
        'day1_1.md',
        'day1_2.md',
        'day1_3.md',
        'day2_1.md',
        'day2_2.md'
    ]

    total_fixed = 0
    all_changes = []

    for md_file in md_files:
        md_path = slides_dir / md_file
        if not md_path.exists():
            continue

        print(f"📄 Processing {md_file}...")
        fixed, changes = fix_markdown_file(md_path, dry_run=dry_run)

        if fixed > 0:
            print(f"   ✅ Fixed {fixed} slides")
            for change in changes:
                print(f"      Slide {change['slide']}: {change['title']}")
                print(f"         {change['list_items']} items → {change['layout']}")
            total_fixed += fixed
            all_changes.extend(changes)
        else:
            print(f"   ℹ️  No changes needed")

        print()

    print("=" * 80)
    print(f"SUMMARY: Fixed {total_fixed} slides")
    if dry_run:
        print("Run without --dry-run to apply changes")
    print("=" * 80)

if __name__ == '__main__':
    main()
