#!/usr/bin/env python3
"""
Correct SVG Text Overlap Fix
Properly spaces text elements vertically with minimum gap = font-size × 1.3
"""

import re
import subprocess
from typing import List, Dict, Tuple

def get_original_svg() -> str:
    """Get original SVG from git"""
    input_file = 'diagrams/diagram_42_regression_mechanism.svg'
    try:
        result = subprocess.run(
            ['git', 'show', f'HEAD:{input_file}'],
            cwd='/home/cuzic/ai-dev-yodoq/slides',
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout
    except Exception as e:
        print(f"Error: {e}")

    with open(f'/home/cuzic/ai-dev-yodoq/slides/{input_file}', 'r', encoding='utf-8') as f:
        return f.read()

def parse_text_elements(content: str) -> List[Dict]:
    """Parse text elements"""
    pattern = r'<text\s+([^>]+)>([^<]*)</text>'
    elements = []

    for idx, match in enumerate(re.finditer(pattern, content)):
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

        elements.append({
            'index': idx,
            'full_text': match.group(0),
            'x': x,
            'y': y,
            'font_size': font_size,
            'text_content': text_content
        })

    return elements

def group_by_column(elements: List[Dict]) -> Dict[int, List[Dict]]:
    """Group elements by x-coordinate (column)"""
    columns = {}

    for elem in elements:
        x = elem['x']
        found = False

        for col_x in list(columns.keys()):
            if abs(x - col_x) <= 100:  # Same column
                columns[col_x].append(elem)
                found = True
                break

        if not found:
            columns[int(x)] = [elem]

    return columns

def fix_column(column: List[Dict]) -> List[Tuple[Dict, float, float]]:
    """Fix overlaps in a single column"""
    # Sort by y-coordinate
    sorted_col = sorted(column, key=lambda e: e['y'])

    adjustments = []
    current_y = None

    for i, elem in enumerate(sorted_col):
        old_y = elem['y']
        font_size = elem['font_size']

        if current_y is None:
            # First element, keep as is
            current_y = old_y
        else:
            # Calculate minimum y position based on previous element
            min_y = current_y + (sorted_col[i-1]['font_size'] * 1.3)

            if old_y < min_y:
                # Need to adjust
                new_y = min_y
                adjustments.append((elem, old_y, new_y))
                current_y = new_y
            else:
                # No adjustment needed
                current_y = old_y

    return adjustments

def apply_fixes(content: str, all_adjustments: List[Tuple[Dict, float, float]]) -> Tuple[str, List]:
    """Apply all adjustments to content"""
    modified_content = content
    fix_examples = []

    # Sort by index in reverse order to avoid replacement conflicts
    sorted_adjustments = sorted(all_adjustments, key=lambda x: x[0]['index'], reverse=True)

    for elem, old_y, new_y in sorted_adjustments:
        old_text = elem['full_text']
        old_y_str = str(old_y)

        # Replace y attribute
        new_text = re.sub(r'y="[^"]+"', f'y="{new_y}"', old_text, count=1)
        modified_content = modified_content.replace(old_text, new_text, 1)

        # Add to examples
        if len(fix_examples) < 10:
            text_preview = elem['text_content']
            if len(text_preview) > 50:
                text_preview = text_preview[:47] + "..."
            fix_examples.append((text_preview, old_y, new_y))

    return modified_content, fix_examples

def update_viewbox(content: str) -> Tuple[str, str, str]:
    """Update viewBox"""
    max_y = 0
    for match in re.finditer(r'y="([^"]+)"', content):
        try:
            y = float(match.group(1))
            if y > max_y:
                max_y = y
        except ValueError:
            pass

    viewbox_match = re.search(r'viewBox="([^"]+)"', content)
    old_viewbox = viewbox_match.group(1) if viewbox_match else "0 0 1820 1105"

    new_height = int(max_y + 100)
    parts = old_viewbox.split()
    if len(parts) == 4:
        parts[3] = str(new_height)
        new_viewbox = ' '.join(parts)
        content = content.replace(f'viewBox="{old_viewbox}"', f'viewBox="{new_viewbox}"')
    else:
        new_viewbox = old_viewbox

    return content, old_viewbox, new_viewbox

def main():
    print("Loading original SVG...")
    content = get_original_svg()

    print("Parsing text elements...")
    elements = parse_text_elements(content)
    print(f"Found {len(elements)} text elements")

    print("Grouping by columns...")
    columns = group_by_column(elements)
    print(f"Found {len(columns)} columns")

    print("Fixing overlaps...")
    all_adjustments = []
    for col_x, column in columns.items():
        adjustments = fix_column(column)
        all_adjustments.extend(adjustments)
        if adjustments:
            print(f"  Column at x={col_x}: {len(adjustments)} adjustments")

    print("Applying fixes...")
    modified_content, fix_examples = apply_fixes(content, all_adjustments)

    print("Updating viewBox...")
    modified_content, old_viewbox, new_viewbox = update_viewbox(modified_content)

    # Write output files
    output_files = [
        '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_42_regression_mechanism.svg',
        '/home/cuzic/ai-dev-yodoq/slides/diagrams-web/diagram_42_regression_mechanism.svg'
    ]

    for output_file in output_files:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)

    # Report
    print(f"\n{'='*70}")
    print("SVG TEXT OVERLAP FIX - FINAL REPORT")
    print(f"{'='*70}")

    print(f"\n修正したテキスト要素の数: {len(all_adjustments)}")

    if fix_examples:
        print(f"\n修正前後のY座標の例 (最大5個):")
        for i, (text, old_y, new_y) in enumerate(fix_examples[:5], 1):
            adjustment = new_y - old_y
            print(f"\n{i}. テキスト: '{text}'")
            print(f"   修正前 Y座標: {old_y:.1f}px")
            print(f"   修正後 Y座標: {new_y:.1f}px")
            print(f"   調整量: +{adjustment:.1f}px")

    print(f"\n最終的なviewBoxのサイズ:")
    print(f"  修正前: {old_viewbox}")
    print(f"  修正後: {new_viewbox}")

    print(f"\n出力ファイル:")
    for f in output_files:
        print(f"  - {f}")

    print(f"\n{'='*70}")
    print("修正完了!")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    main()
