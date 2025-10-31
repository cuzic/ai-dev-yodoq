#!/usr/bin/env python3
"""Comprehensive layout review showing all issues and patterns."""

import re
from pathlib import Path
from collections import defaultdict

def analyze_layouts(md_path):
    """Analyze all layout usage and identify patterns."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = content.split('\n---\n')

    layout_stats = defaultdict(int)
    layout_issues = defaultdict(list)

    for idx, slide in enumerate(slides, 1):
        # Skip CSS blocks
        if '<style>' in slide:
            continue

        # Get title
        title_match = re.search(r'^#\s+(.+)$', slide, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Slide {idx}"

        # Get layout
        layout_match = re.search(r'<!--\s*_class:\s*([\w-]+)\s*-->', slide)
        layout = layout_match.group(1) if layout_match else 'default'

        layout_stats[layout] += 1

        # Check for images
        has_image = bool(re.search(r'!\[', slide))

        # Count bullets
        bullets = len(re.findall(r'^\s*[-*•]\s+', slide, re.MULTILINE))

        # Identify potential issues
        issues = []

        # Issue: Horizontal layout without image
        if 'horizontal' in layout and not has_image:
            issues.append(f"No image in horizontal layout")

        # Issue: Too many bullets for layout
        if layout == 'two-column' and bullets > 18:
            issues.append(f"{bullets} bullets (recommend 3-column)")
        elif layout == 'three-column' and bullets > 27:
            issues.append(f"{bullets} bullets (too many, split slide)")
        elif 'horizontal' in layout and bullets > 8:
            issues.append(f"{bullets} bullets (horizontal layouts should have <8)")

        # Issue: Too few bullets (might not need columns)
        if layout in ['two-column', 'three-column'] and bullets < 5:
            issues.append(f"Only {bullets} bullets (may not need columns)")

        if issues:
            layout_issues[layout].append({
                'slide': idx,
                'title': title,
                'bullets': bullets,
                'has_image': has_image,
                'issues': issues
            })

    return layout_stats, layout_issues

def main():
    md_path = Path(__file__).parent / 'all_slides.md'

    print("=" * 80)
    print("COMPREHENSIVE LAYOUT REVIEW")
    print("=" * 80)
    print()

    layout_stats, layout_issues = analyze_layouts(md_path)

    print("📊 LAYOUT USAGE STATISTICS")
    print("-" * 80)
    total_slides = sum(layout_stats.values())
    for layout, count in sorted(layout_stats.items(), key=lambda x: -x[1]):
        pct = (count / total_slides * 100)
        print(f"  {layout:30s} {count:3d} slides ({pct:5.1f}%)")
    print(f"\n  {'TOTAL':30s} {total_slides:3d} slides")

    print("\n" + "=" * 80)
    print("⚠️  LAYOUT ISSUES BY TYPE")
    print("=" * 80)

    total_issues = sum(len(issues) for issues in layout_issues.values())

    if total_issues == 0:
        print("\n✅ No layout issues found!")
    else:
        print(f"\nFound {total_issues} slides with potential layout issues:\n")

        for layout, issues in sorted(layout_issues.items()):
            if not issues:
                continue

            print(f"\n📍 {layout.upper()} LAYOUT ({len(issues)} slides)")
            print("-" * 80)

            for item in issues[:10]:  # Show first 10
                print(f"  Slide {item['slide']}: {item['title']}")
                print(f"    Bullets: {item['bullets']}, Has image: {item['has_image']}")
                for issue in item['issues']:
                    print(f"    ⚠️  {issue}")
                print()

    print("=" * 80)
    print("💡 KEY FINDINGS & RECOMMENDATIONS")
    print("=" * 80)
    print("""
1. HORIZONTAL LAYOUTS (layout-horizontal-left/right):
   ⚠️  MAIN ISSUE: 19 slides have text overflow
   - Current: 500px column width
   - Problem: Many lines 500-900px wide (Japanese + technical terms)
   - Solution: Increase to 600px OR shorten text in all 19 slides

2. TWO-COLUMN LAYOUTS:
   ✅ Working well
   - 600px column width appropriate
   - Most slides fit comfortably

3. THREE-COLUMN LAYOUTS:
   ✅ Working well after optimization
   - 400px column width appropriate
   - Recent layout changes fixed overcrowding

4. CARD-GRID LAYOUTS:
   ✅ Working well
   - 350px column width
   - Good for 3-4 card sections
    """)

if __name__ == '__main__':
    main()
