#!/usr/bin/env python3
"""
Validate that each slide follows the layout selection criteria.
Based on LAYOUT_SELECTION_GUIDE.md rules.
"""

import re
from pathlib import Path
from collections import defaultdict

def get_slide_info(slide_text, slide_num):
    """Extract key information from a slide."""
    # Get title
    title_match = re.search(r'^#\s+(.+)$', slide_text, re.MULTILINE)
    title = title_match.group(1) if title_match else f"Slide {slide_num}"

    # Get layout
    layout_match = re.search(r'<!--\s*_class:\s*([\w-]+)\s*-->', slide_text)
    layout = layout_match.group(1) if layout_match else 'default'

    # Count bullets
    bullets = len(re.findall(r'^\s*[-*•]\s+', slide_text, re.MULTILINE))

    # Check for images
    has_image = bool(re.search(r'!\[', slide_text))
    image_count = len(re.findall(r'!\[', slide_text))

    # Check for sections (### headers for card-grid)
    sections = len(re.findall(r'^###\s+', slide_text, re.MULTILINE))

    # Check if it's a style block
    is_style_block = '<style>' in slide_text

    # Count actual content lines (exclude empty, headers, directives)
    content_lines = [
        line for line in slide_text.split('\n')
        if line.strip()
        and not line.strip().startswith('#')
        and not line.strip().startswith('<!--')
        and not line.strip().startswith('![')
        and not '<style>' in line
    ]
    content_line_count = len(content_lines)

    return {
        'title': title,
        'layout': layout,
        'bullets': bullets,
        'has_image': has_image,
        'image_count': image_count,
        'sections': sections,
        'is_style_block': is_style_block,
        'content_lines': content_line_count
    }

def validate_layout(info):
    """
    Validate layout choice based on criteria.
    Returns: (is_valid, issues, recommended_layout)
    """
    layout = info['layout']
    bullets = info['bullets']
    has_image = info['has_image']
    sections = info['sections']

    issues = []
    recommended = None

    # Skip style blocks
    if info['is_style_block']:
        return True, [], None

    # Rule 1: Horizontal layouts must have image
    if 'horizontal' in layout and not has_image:
        issues.append(f"Horizontal layout without image (has {bullets} bullets)")
        if bullets <= 7:
            recommended = 'default'
        elif bullets <= 18:
            recommended = 'two-column'
        else:
            recommended = 'three-column'

    # Rule 2: Horizontal layouts should have 5-8 bullets
    if 'horizontal' in layout and has_image:
        if bullets > 8:
            issues.append(f"Horizontal layout with too many bullets ({bullets}, recommend ≤8)")
            recommended = 'two-column' if bullets <= 18 else 'three-column'
        elif bullets < 3 and info['content_lines'] < 5:
            issues.append(f"Horizontal layout with too few bullets ({bullets}, recommend ≥3)")
            recommended = 'default' if not has_image else 'layout-diagram-only'

    # Rule 3: Two-column should have 8-18 bullets
    if layout == 'two-column':
        if bullets > 18:
            issues.append(f"Two-column with too many bullets ({bullets}, recommend three-column)")
            recommended = 'three-column'
        elif bullets < 8:
            issues.append(f"Two-column with too few bullets ({bullets}, recommend default)")
            recommended = 'default'

    # Rule 4: Three-column should have 15-27 bullets
    if layout == 'three-column':
        if bullets > 27:
            issues.append(f"Three-column with too many bullets ({bullets}, recommend split slide)")
            recommended = 'SPLIT SLIDE'
        elif bullets < 15:
            issues.append(f"Three-column with too few bullets ({bullets}, recommend two-column)")
            recommended = 'two-column' if bullets >= 8 else 'default'

    # Rule 5: Default with many bullets should use columns
    if layout == 'default' and bullets >= 8:
        if has_image and bullets <= 8:
            issues.append(f"Default with {bullets} bullets and image (recommend horizontal)")
            recommended = 'layout-horizontal-left'
        elif bullets <= 18:
            issues.append(f"Default with {bullets} bullets (recommend two-column)")
            recommended = 'two-column'
        else:
            issues.append(f"Default with {bullets} bullets (recommend three-column)")
            recommended = 'three-column'

    # Rule 6: Card-grid should have 3-4 sections
    if layout == 'card-grid':
        if sections < 3:
            issues.append(f"Card-grid with too few sections ({sections}, recommend ≥3)")
            recommended = 'two-column' if bullets >= 8 else 'default'
        elif sections > 4:
            issues.append(f"Card-grid with too many sections ({sections}, recommend ≤4)")
            recommended = 'three-column' if bullets >= 15 else 'two-column'

    # Rule 7: Lead/diagram-only should have minimal text
    if layout in ['lead', 'layout-diagram-only']:
        if bullets > 3:
            issues.append(f"{layout} with {bullets} bullets (recommend ≤3)")
            if has_image and bullets <= 8:
                recommended = 'layout-horizontal-left'
            elif bullets <= 18:
                recommended = 'two-column'
            else:
                recommended = 'three-column'

    # Rule 8: Any layout with 27+ bullets should be split
    if bullets > 27:
        issues.append(f"Too many bullets ({bullets}, recommend split into multiple slides)")
        recommended = 'SPLIT SLIDE'

    is_valid = len(issues) == 0
    return is_valid, issues, recommended

def main():
    md_path = Path(__file__).parent / 'all_slides.md'

    print("=" * 80)
    print("LAYOUT VALIDATION REPORT")
    print("Checking all slides against LAYOUT_SELECTION_GUIDE.md criteria")
    print("=" * 80)
    print()

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = content.split('\n---\n')

    # Statistics
    layout_counts = defaultdict(int)
    valid_slides = 0
    invalid_slides = []

    for idx, slide in enumerate(slides, 1):
        info = get_slide_info(slide, idx)

        # Skip style blocks
        if info['is_style_block']:
            continue

        layout_counts[info['layout']] += 1

        is_valid, issues, recommended = validate_layout(info)

        if not is_valid:
            invalid_slides.append({
                'slide': idx,
                'info': info,
                'issues': issues,
                'recommended': recommended
            })
        else:
            valid_slides += 1

    # Print statistics
    total_slides = sum(layout_counts.values())
    print(f"📊 STATISTICS")
    print("-" * 80)
    print(f"Total slides: {total_slides}")
    print(f"Valid slides: {valid_slides} ({valid_slides/total_slides*100:.1f}%)")
    print(f"Invalid slides: {len(invalid_slides)} ({len(invalid_slides)/total_slides*100:.1f}%)")
    print()

    # Print layout distribution
    print(f"📋 LAYOUT DISTRIBUTION")
    print("-" * 80)
    for layout, count in sorted(layout_counts.items(), key=lambda x: -x[1]):
        pct = (count / total_slides * 100)
        print(f"  {layout:30s} {count:3d} slides ({pct:5.1f}%)")
    print()

    # Print invalid slides
    if invalid_slides:
        print("=" * 80)
        print(f"⚠️  LAYOUT ISSUES FOUND ({len(invalid_slides)} slides)")
        print("=" * 80)
        print()

        # Group by issue type
        by_issue_type = defaultdict(list)
        for item in invalid_slides:
            issue_key = item['issues'][0].split('(')[0].strip()
            by_issue_type[issue_key].append(item)

        for issue_type, items in sorted(by_issue_type.items()):
            print(f"### {issue_type} ({len(items)} slides)")
            print("-" * 80)

            for item in items[:10]:  # Show first 10
                info = item['info']
                print(f"  Slide {item['slide']}: {info['title']}")
                print(f"    Current: {info['layout']} "
                      f"(bullets: {info['bullets']}, image: {info['has_image']})")
                print(f"    Issues: {', '.join(item['issues'])}")
                if item['recommended']:
                    print(f"    ✅ Recommended: {item['recommended']}")
                print()

            if len(items) > 10:
                print(f"    ... and {len(items) - 10} more\n")

        # Summary recommendations
        print("=" * 80)
        print("📋 SUMMARY RECOMMENDATIONS")
        print("=" * 80)
        print()

        recommendations = defaultdict(list)
        for item in invalid_slides:
            if item['recommended']:
                key = f"{item['info']['layout']} → {item['recommended']}"
                recommendations[key].append(item['slide'])

        for change, slides in sorted(recommendations.items()):
            print(f"  {change}")
            print(f"    Slides: {', '.join(map(str, slides[:15]))}")
            if len(slides) > 15:
                print(f"    ... and {len(slides) - 15} more")
            print()

    else:
        print("✅ ALL SLIDES FOLLOW LAYOUT CRITERIA!")
        print()
        print("All slides have appropriate layouts based on:")
        print("  • Bullet count")
        print("  • Image presence")
        print("  • Content structure")
        print("  • Text density")

    print("=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    main()
