#!/usr/bin/env python3
"""
Verify that diagram_18_fit_gap_analysis.svg has no text overlaps.
"""

import xml.etree.ElementTree as ET
import re

def verify_svg(svg_path: str):
    """Verify SVG has no text overlaps."""

    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Extract all text elements with their positions and sizes
    text_elements = []
    for text_elem in root.iter('{http://www.w3.org/2000/svg}text'):
        x = float(text_elem.get('x', 0))
        y = float(text_elem.get('y', 0))

        # Get font-size
        font_size = 54  # default
        style = text_elem.get('style', '')
        if 'font-size:' in style:
            match = re.search(r'font-size:\s*(\d+)px', style)
            if match:
                font_size = int(match.group(1))

        class_name = text_elem.get('class', '')
        if 'circle-text' in class_name:
            font_size = 54
        elif 'circle-title' in class_name:
            font_size = 72
        elif 'overlap-title' in class_name:
            font_size = 74
        elif 'title' in class_name:
            font_size = 81

        if 'font-size' in text_elem.attrib:
            font_size = int(text_elem.attrib.get('font-size'))

        text_content = text_elem.text or ''
        text_content = text_content.strip()

        text_elements.append({
            'x': x,
            'y': y,
            'font_size': font_size,
            'text': text_content
        })

    # Group by x position (within 100px tolerance)
    x_groups = {}
    for elem in text_elements:
        x_key = round(elem['x'] / 50) * 50
        if x_key not in x_groups:
            x_groups[x_key] = []
        x_groups[x_key].append(elem)

    # Check each group for overlaps
    print("=" * 70)
    print("VERIFICATION REPORT: diagram_18_fit_gap_analysis.svg")
    print("=" * 70)

    total_issues = 0
    total_checks = 0

    for x_key, group in sorted(x_groups.items()):
        if len(group) < 2:
            continue

        group.sort(key=lambda e: e['y'])

        print(f"\n--- Group at x≈{x_key} ({len(group)} elements) ---")

        for i in range(len(group) - 1):
            current = group[i]
            next_elem = group[i + 1]

            max_font = max(current['font_size'], next_elem['font_size'])
            min_gap = max_font * 1.3
            actual_gap = next_elem['y'] - current['y']

            total_checks += 1

            status = "✓ OK" if actual_gap >= min_gap else "✗ OVERLAP"

            if actual_gap < min_gap:
                total_issues += 1
                print(f"  {status}")
                print(f"    '{current['text'][:40]}' (y={current['y']}, size={current['font_size']})")
                print(f"    '{next_elem['text'][:40]}' (y={next_elem['y']}, size={next_elem['font_size']})")
                print(f"    Gap: {actual_gap:.1f}px (required: {min_gap:.1f}px) - SHORT BY {min_gap - actual_gap:.1f}px")
            else:
                print(f"  {status}: '{current['text'][:30]}' → '{next_elem['text'][:30]}'")
                print(f"    Gap: {actual_gap:.1f}px (required: {min_gap:.1f}px)")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total checks performed: {total_checks}")
    print(f"Issues found: {total_issues}")

    if total_issues == 0:
        print("\n✓ SUCCESS: No text overlaps detected!")
        print("All text elements maintain proper spacing (font-size × 1.3 minimum).")
    else:
        print(f"\n✗ FAILURE: {total_issues} overlaps still exist.")
        print("Additional adjustments needed.")

    # ViewBox info
    viewbox = root.get('viewBox', '')
    print(f"\nViewBox: {viewbox}")

    return total_issues == 0


if __name__ == '__main__':
    svg_path = '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_18_fit_gap_analysis.svg'
    success = verify_svg(svg_path)
    exit(0 if success else 1)
