#!/usr/bin/env python3
"""
Refined SVG Text Overlap Fix Script
Fixes text overlap issues while preserving original SVG formatting
"""

import re
from typing import List, Tuple

def parse_svg_text_elements(content: str) -> List[Tuple[int, str, float, float, float]]:
    """Parse text elements from SVG content"""
    # Pattern to match text elements with their attributes
    pattern = r'<text\s+([^>]+)>([^<]*)</text>'

    elements = []
    for match in re.finditer(pattern, content):
        attrs = match.group(1)
        text_content = match.group(2).strip()

        # Extract x, y coordinates
        x_match = re.search(r'x="([^"]+)"', attrs)
        y_match = re.search(r'y="([^"]+)"', attrs)

        if not x_match or not y_match:
            continue

        x = float(x_match.group(1))
        y = float(y_match.group(1))

        # Extract font-size from style attribute
        font_size = 50.0  # default
        style_match = re.search(r'style="([^"]+)"', attrs)
        if style_match:
            style = style_match.group(1)
            fs_match = re.search(r'font-size:\s*(\d+)px', style)
            if fs_match:
                font_size = float(fs_match.group(1))

        # Store: line number, full match, x, y, font_size
        elements.append((match.start(), match.group(0), x, y, font_size))

    return elements

def group_elements_by_column(elements: List[Tuple[int, str, float, float, float]]) -> dict:
    """Group text elements by x-coordinate (columns)"""
    columns = {}

    for pos, text, x, y, fs in elements:
        # Find or create column
        col_key = None
        for key in columns.keys():
            if abs(x - key) <= 100:  # Within 100px = same column
                col_key = key
                break

        if col_key is None:
            col_key = x
            columns[col_key] = []

        columns[col_key].append((pos, text, x, y, fs))

    return columns

def fix_column_overlaps(column: List[Tuple[int, str, float, float, float]]) -> List[Tuple[str, str, float, float]]:
    """Fix overlaps within a column, return list of (old_text, new_text, old_y, new_y)"""
    # Sort by y coordinate
    sorted_col = sorted(column, key=lambda item: item[3])

    replacements = []
    adjustments = {}  # y position -> cumulative adjustment

    for i in range(len(sorted_col) - 1):
        pos1, text1, x1, y1, fs1 = sorted_col[i]

        # Apply previous adjustments
        if y1 in adjustments:
            y1 = adjustments[y1]

        for j in range(i + 1, len(sorted_col)):
            pos2, text2, x2, y2, fs2 = sorted_col[j]

            # Apply previous adjustments
            original_y2 = y2
            if y2 in adjustments:
                y2 = adjustments[y2]

            min_gap = max(fs1, fs2) * 1.3
            actual_gap = y2 - y1

            if actual_gap < min_gap:
                # Need to adjust y2
                adjustment = min_gap - actual_gap
                new_y2 = y2 + adjustment

                # Find old y value in text2
                old_y_str = re.search(r'y="([^"]+)"', text2).group(1)
                new_text2 = text2.replace(f'y="{old_y_str}"', f'y="{new_y2}"')

                replacements.append((text2, new_text2, float(old_y_str), new_y2))

                # Update for next iteration
                sorted_col[j] = (pos2, new_text2, x2, new_y2, fs2)
                adjustments[original_y2] = new_y2

                # Update y1 for comparing with next element
                y1 = new_y2
                fs1 = fs2

    return replacements

def fix_svg_content(content: str) -> Tuple[str, List[Tuple[str, float, float]], str, str]:
    """Fix SVG content and return modified content plus statistics"""
    elements = parse_svg_text_elements(content)
    columns = group_elements_by_column(elements)

    all_replacements = []
    fix_examples = []

    for col_x, column in columns.items():
        replacements = fix_column_overlaps(column)
        all_replacements.extend(replacements)

    # Apply replacements to content
    modified_content = content
    for old_text, new_text, old_y, new_y in all_replacements:
        modified_content = modified_content.replace(old_text, new_text, 1)

        if len(fix_examples) < 5:
            # Extract text content for reporting
            text_match = re.search(r'>([^<]*)</text>', new_text)
            text_content = text_match.group(1).strip() if text_match else "(unknown)"
            if len(text_content) > 50:
                text_content = text_content[:47] + "..."
            fix_examples.append((text_content, old_y, new_y))

    # Update viewBox
    old_viewbox_match = re.search(r'viewBox="([^"]+)"', modified_content)
    old_viewbox = old_viewbox_match.group(1) if old_viewbox_match else "0 0 1820 1105"

    # Find max y coordinate in modified content
    max_y = 0
    for match in re.finditer(r'y="([^"]+)"', modified_content):
        try:
            y = float(match.group(1))
            if y > max_y:
                max_y = y
        except ValueError:
            pass

    # Add padding and update viewBox
    new_height = int(max_y + 100)
    parts = old_viewbox.split()
    if len(parts) == 4:
        parts[3] = str(new_height)
        new_viewbox = ' '.join(parts)
        modified_content = modified_content.replace(f'viewBox="{old_viewbox}"', f'viewBox="{new_viewbox}"')
    else:
        new_viewbox = old_viewbox

    return modified_content, fix_examples, old_viewbox, new_viewbox

def main():
    input_file = '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_42_regression_mechanism.svg'
    output_files = [
        '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_42_regression_mechanism.svg',
        '/home/cuzic/ai-dev-yodoq/slides/diagrams-web/diagram_42_regression_mechanism.svg'
    ]

    # Read original SVG
    with open(input_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Check if already modified by ElementTree (has ns0: prefix)
    if 'ns0:' in original_content:
        print("Note: SVG was previously modified by ElementTree. Reading original...")
        # Try to read from git
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'show', f'HEAD:{input_file.replace("/home/cuzic/ai-dev-yodoq/slides/", "")}'],
                cwd='/home/cuzic/ai-dev-yodoq/slides',
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                original_content = result.stdout
                print("Successfully loaded original from git")
        except Exception as e:
            print(f"Could not load from git: {e}")
            print("Proceeding with current version...")

    print("Analyzing and fixing SVG text overlaps...")
    print(f"Input: {input_file}")

    modified_content, fix_examples, old_viewbox, new_viewbox = fix_svg_content(original_content)

    # Write to output files
    for output_file in output_files:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)

    print(f"\n=== Fix Summary ===")
    print(f"Total text elements adjusted: {len(fix_examples)}")

    print(f"\n=== Y-coordinate Adjustments (Examples) ===")
    for i, (text, old_y, new_y) in enumerate(fix_examples, 1):
        print(f"{i}. Text: '{text}'")
        print(f"   Old Y: {old_y:.1f}px -> New Y: {new_y:.1f}px (adjustment: +{new_y - old_y:.1f}px)")

    print(f"\n=== ViewBox Update ===")
    print(f"Old: {old_viewbox}")
    print(f"New: {new_viewbox}")

    print(f"\n=== Output Files ===")
    for output_file in output_files:
        print(f"- {output_file}")

    print("\nFix completed successfully!")

if __name__ == '__main__':
    main()
