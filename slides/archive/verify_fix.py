#!/usr/bin/env python3
"""
Verify the SVG fix by checking for overlaps
"""

import re

def parse_text_elements(file_path):
    """Parse text elements from SVG"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'<text\s+([^>]+)>([^<]*)</text>'
    elements = []

    for match in re.finditer(pattern, content):
        attrs = match.group(1)
        text_content = match.group(2).strip()

        x_match = re.search(r'x="([^"]+)"', attrs)
        y_match = re.search(r'y="([^"]+)"', attrs)

        if not x_match or not y_match:
            continue

        x = float(x_match.group(1))
        y = float(y_match.group(1))

        # Extract font-size
        font_size = 50.0
        style_match = re.search(r'style="([^"]+)"', attrs)
        if style_match:
            fs_match = re.search(r'font-size:\s*(\d+)px', style_match.group(1))
            if fs_match:
                font_size = float(fs_match.group(1))

        elements.append((x, y, font_size, text_content))

    return elements

def check_overlaps(elements):
    """Check for overlaps"""
    overlaps = []

    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            x1, y1, fs1, text1 = elements[i]
            x2, y2, fs2, text2 = elements[j]

            # Same column?
            if abs(x1 - x2) > 100:
                continue

            # Check spacing
            min_gap = max(fs1, fs2) * 1.3
            actual_gap = abs(y1 - y2)

            if actual_gap < min_gap:
                overlaps.append({
                    'text1': text1[:40],
                    'text2': text2[:40],
                    'y1': y1,
                    'y2': y2,
                    'fs1': fs1,
                    'fs2': fs2,
                    'gap': actual_gap,
                    'min_gap': min_gap
                })

    return overlaps

def main():
    file_path = '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_42_regression_mechanism.svg'

    print("Verifying SVG fix...")
    print(f"File: {file_path}\n")

    elements = parse_text_elements(file_path)
    print(f"Total text elements: {len(elements)}")

    overlaps = check_overlaps(elements)

    if overlaps:
        print(f"\n WARNING: Found {len(overlaps)} overlaps:\n")
        for i, overlap in enumerate(overlaps[:5], 1):
            print(f"{i}. '{overlap['text1']}' (y={overlap['y1']:.1f}, fs={overlap['fs1']:.0f})")
            print(f"   '{overlap['text2']}' (y={overlap['y2']:.1f}, fs={overlap['fs2']:.0f})")
            print(f"   Gap: {overlap['gap']:.1f}px (required: {overlap['min_gap']:.1f}px)\n")
    else:
        print("\n SUCCESS: No overlaps found!")
        print(" All text elements are properly spaced.\n")

if __name__ == '__main__':
    main()
