#!/usr/bin/env python3
"""
SVG Text Overlap Fix Script
Analyzes and fixes text overlap issues in SVG files
"""

import xml.etree.ElementTree as ET
import re
from typing import List, Tuple, Dict

def parse_svg(file_path: str) -> ET.ElementTree:
    """Parse SVG file and return ElementTree"""
    tree = ET.parse(file_path)
    return tree

def get_font_size(element: ET.Element, default: float = 50.0) -> float:
    """Extract font-size from element's style attribute or class"""
    style = element.get('style', '')
    match = re.search(r'font-size:\s*(\d+)px', style)
    if match:
        return float(match.group(1))
    return default

def get_text_elements(root: ET.Element) -> List[Tuple[ET.Element, float, float, float]]:
    """Get all text elements with their x, y coordinates and font-size"""
    text_elements = []
    for text in root.findall('.//{http://www.w3.org/2000/svg}text'):
        x = float(text.get('x', 0))
        y = float(text.get('y', 0))
        font_size = get_font_size(text)
        text_elements.append((text, x, y, font_size))
    return text_elements

def group_by_x_proximity(text_elements: List[Tuple[ET.Element, float, float, float]],
                         threshold: float = 100.0) -> Dict[int, List[Tuple[ET.Element, float, float, float]]]:
    """Group text elements by x-coordinate proximity"""
    groups = {}
    for elem, x, y, font_size in text_elements:
        # Find existing group within threshold
        group_key = None
        for key in groups.keys():
            if abs(x - key) <= threshold:
                group_key = key
                break

        if group_key is None:
            group_key = int(x)
            groups[group_key] = []

        groups[group_key].append((elem, x, y, font_size))

    return groups

def detect_overlaps(group: List[Tuple[ET.Element, float, float, float]]) -> List[Tuple[int, int, float]]:
    """Detect overlapping text elements in a group"""
    # Sort by y-coordinate
    sorted_group = sorted(group, key=lambda item: item[2])
    overlaps = []

    for i in range(len(sorted_group) - 1):
        _, _, y1, fs1 = sorted_group[i]
        _, _, y2, fs2 = sorted_group[i + 1]

        min_gap = max(fs1, fs2) * 1.3
        actual_gap = y2 - y1

        if actual_gap < min_gap:
            overlaps.append((i, i + 1, min_gap - actual_gap))

    return overlaps

def fix_overlaps(tree: ET.ElementTree) -> Tuple[int, List[Tuple[str, float, float]]]:
    """Fix all overlapping text elements"""
    root = tree.getroot()
    text_elements = get_text_elements(root)

    # Group by x-coordinate proximity
    groups = group_by_x_proximity(text_elements)

    total_fixes = 0
    fix_examples = []

    for group_key, group in groups.items():
        if len(group) < 2:
            continue

        # Sort by y-coordinate
        sorted_group = sorted(group, key=lambda item: item[2])

        # Detect and fix overlaps
        i = 0
        while i < len(sorted_group) - 1:
            elem1, x1, y1, fs1 = sorted_group[i]
            elem2, x2, y2, fs2 = sorted_group[i + 1]

            min_gap = max(fs1, fs2) * 1.3
            actual_gap = y2 - y1

            if actual_gap < min_gap:
                # Calculate new y position for elem2 and all following elements
                adjustment = min_gap - actual_gap

                for j in range(i + 1, len(sorted_group)):
                    elem_to_fix, x_fix, y_fix, fs_fix = sorted_group[j]
                    old_y = y_fix
                    new_y = y_fix + adjustment

                    elem_to_fix.set('y', str(new_y))

                    # Update in sorted_group for next iteration
                    sorted_group[j] = (elem_to_fix, x_fix, new_y, fs_fix)

                    # Record fix example
                    if len(fix_examples) < 5:
                        text_content = elem_to_fix.text or '(text in child element)'
                        if len(text_content) > 50:
                            text_content = text_content[:47] + "..."
                        fix_examples.append((text_content, old_y, new_y))

                    total_fixes += 1

            i += 1

    return total_fixes, fix_examples

def update_viewbox(tree: ET.ElementTree) -> Tuple[str, str]:
    """Update viewBox to accommodate adjusted content"""
    root = tree.getroot()
    text_elements = get_text_elements(root)

    if not text_elements:
        return "unchanged", "unchanged"

    # Find maximum y coordinate
    max_y = max(y + font_size for _, _, y, font_size in text_elements)

    # Add padding
    new_height = max_y + 50

    # Get current viewBox
    viewbox = root.get('viewBox', '0 0 1820 1105')
    parts = viewbox.split()
    old_viewbox = viewbox

    if len(parts) == 4:
        parts[3] = str(int(new_height))
        new_viewbox = ' '.join(parts)
        root.set('viewBox', new_viewbox)
        return old_viewbox, new_viewbox

    return old_viewbox, old_viewbox

def fix_svg_file(input_path: str, output_paths: List[str]) -> Dict[str, any]:
    """Main function to fix SVG file"""
    # Parse SVG
    tree = parse_svg(input_path)

    # Fix overlaps
    num_fixes, fix_examples = fix_overlaps(tree)

    # Update viewBox
    old_viewbox, new_viewbox = update_viewbox(tree)

    # Write to output paths
    for output_path in output_paths:
        tree.write(output_path, encoding='utf-8', xml_declaration=True)

    return {
        'num_fixes': num_fixes,
        'fix_examples': fix_examples,
        'old_viewbox': old_viewbox,
        'new_viewbox': new_viewbox
    }

if __name__ == '__main__':
    input_file = '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_42_regression_mechanism.svg'
    output_files = [
        '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_42_regression_mechanism.svg',
        '/home/cuzic/ai-dev-yodoq/slides/diagrams-web/diagram_42_regression_mechanism.svg'
    ]

    print("Analyzing and fixing SVG text overlaps...")
    print(f"Input: {input_file}")

    result = fix_svg_file(input_file, output_files)

    print(f"\n=== Fix Summary ===")
    print(f"Total text elements adjusted: {result['num_fixes']}")

    print(f"\n=== Y-coordinate Adjustments (Examples) ===")
    for i, (text, old_y, new_y) in enumerate(result['fix_examples'], 1):
        print(f"{i}. Text: '{text}'")
        print(f"   Old Y: {old_y:.1f}px -> New Y: {new_y:.1f}px (adjustment: +{new_y - old_y:.1f}px)")

    print(f"\n=== ViewBox Update ===")
    print(f"Old: {result['old_viewbox']}")
    print(f"New: {result['new_viewbox']}")

    print(f"\n=== Output Files ===")
    for output_file in output_files:
        print(f"- {output_file}")

    print("\nFix completed successfully!")
