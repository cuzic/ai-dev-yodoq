#!/usr/bin/env python3
"""
Fix text overlap issues in diagram_18_fit_gap_analysis.svg
"""

import xml.etree.ElementTree as ET
import re
from typing import List, Tuple

def parse_svg_text_elements(svg_path: str) -> Tuple[ET.Element, List[dict]]:
    """Parse SVG and extract text elements with their positions and sizes."""
    tree = ET.parse(svg_path)
    root = tree.getroot()

    text_elements = []
    for text_elem in root.iter('{http://www.w3.org/2000/svg}text'):
        x = float(text_elem.get('x', 0))
        y = float(text_elem.get('y', 0))

        # Get font-size from style attribute or class
        font_size = 54  # default
        style = text_elem.get('style', '')
        if 'font-size:' in style:
            match = re.search(r'font-size:\s*(\d+)px', style)
            if match:
                font_size = int(match.group(1))

        # Check class for font-size
        class_name = text_elem.get('class', '')
        if 'circle-text' in class_name:
            font_size = 54
        elif 'circle-title' in class_name:
            font_size = 72
        elif 'overlap-title' in class_name:
            font_size = 74
        elif 'title' in class_name:
            font_size = 81

        # Override with inline font-size if present
        if 'font-size' in text_elem.attrib:
            font_size = int(text_elem.attrib.get('font-size'))

        text_elements.append({
            'element': text_elem,
            'x': x,
            'y': y,
            'font_size': font_size,
            'text': text_elem.text or ''
        })

    return root, text_elements

def find_overlaps(text_elements: List[dict], x_tolerance: float = 100) -> List[Tuple[dict, dict]]:
    """Find overlapping text elements."""
    overlaps = []

    for i, elem1 in enumerate(text_elements):
        for elem2 in text_elements[i+1:]:
            # Check if they are in similar x position (same column)
            if abs(elem1['x'] - elem2['x']) <= x_tolerance:
                # Calculate required spacing
                max_font = max(elem1['font_size'], elem2['font_size'])
                min_gap = max_font * 1.3

                # Check vertical spacing
                if elem1['y'] < elem2['y']:
                    actual_gap = elem2['y'] - elem1['y']
                    if actual_gap < min_gap:
                        overlaps.append((elem1, elem2, actual_gap, min_gap))

    return overlaps

def fix_overlaps(svg_path: str, output_paths: List[str]):
    """Fix text overlaps in SVG file."""
    root, text_elements = parse_svg_text_elements(svg_path)

    print("=== Initial Analysis ===")
    print(f"Total text elements: {len(text_elements)}")

    # Group text elements by x position (columns)
    x_groups = {}
    for elem in text_elements:
        x_key = round(elem['x'] / 50) * 50  # Group by 50px intervals
        if x_key not in x_groups:
            x_groups[x_key] = []
        x_groups[x_key].append(elem)

    # Sort each group by y position
    for x_key in x_groups:
        x_groups[x_key].sort(key=lambda e: e['y'])

    print(f"\nText element groups by x position: {len(x_groups)}")

    # Fix overlaps in each group
    modifications = []
    for x_key, group in sorted(x_groups.items()):
        if len(group) < 2:
            continue

        print(f"\n--- Group at x≈{x_key} ({len(group)} elements) ---")

        # Adjust y positions to prevent overlaps
        for i in range(len(group) - 1):
            current = group[i]
            next_elem = group[i + 1]

            max_font = max(current['font_size'], next_elem['font_size'])
            min_gap = max_font * 1.3
            actual_gap = next_elem['y'] - current['y']

            if actual_gap < min_gap:
                adjustment = min_gap - actual_gap
                print(f"  Overlap detected:")
                print(f"    '{current['text'][:30]}...' (y={current['y']}, size={current['font_size']})")
                print(f"    '{next_elem['text'][:30]}...' (y={next_elem['y']}, size={next_elem['font_size']})")
                print(f"    Gap: {actual_gap:.1f}px (required: {min_gap:.1f}px)")
                print(f"    Adjustment: +{adjustment:.1f}px")

                # Adjust all subsequent elements
                for j in range(i + 1, len(group)):
                    old_y = group[j]['y']
                    new_y = old_y + adjustment
                    group[j]['y'] = new_y
                    group[j]['element'].set('y', str(new_y))

                    modifications.append({
                        'text': group[j]['text'][:50],
                        'old_y': old_y,
                        'new_y': new_y
                    })

    # Calculate new viewBox height
    max_y = max(elem['y'] for elem in text_elements)
    max_font = max(elem['font_size'] for elem in text_elements)
    new_height = int(max_y + max_font * 1.5)

    # Update viewBox
    old_viewbox = root.get('viewBox', '0 0 1040 910')
    viewbox_parts = old_viewbox.split()
    new_viewbox = f"{viewbox_parts[0]} {viewbox_parts[1]} {viewbox_parts[2]} {new_height}"
    root.set('viewBox', new_viewbox)

    print(f"\n=== Modifications Summary ===")
    print(f"Total modifications: {len(modifications)}")
    for mod in modifications:
        print(f"  '{mod['text']}': y {mod['old_y']:.1f} → {mod['new_y']:.1f}")

    print(f"\n=== ViewBox Update ===")
    print(f"Old viewBox: {old_viewbox}")
    print(f"New viewBox: {new_viewbox}")

    # Write to output files
    tree = ET.ElementTree(root)
    for output_path in output_paths:
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        print(f"\nSaved: {output_path}")

    return len(modifications), new_viewbox

if __name__ == '__main__':
    svg_path = '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_18_fit_gap_analysis.svg'
    output_paths = [
        '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_18_fit_gap_analysis.svg',
        '/home/cuzic/ai-dev-yodoq/slides/diagrams-web/diagram_18_fit_gap_analysis.svg'
    ]

    num_fixes, new_viewbox = fix_overlaps(svg_path, output_paths)

    print("\n" + "="*60)
    print("FIX COMPLETE")
    print("="*60)
    print(f"Fixed {num_fixes} text elements")
    print(f"Final viewBox: {new_viewbox}")
