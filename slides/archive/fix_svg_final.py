#!/usr/bin/env python3
"""
Final SVG Text Overlap Fix Script - Optimized version
Only adjusts overlapping elements, not all subsequent elements
"""

import re
import subprocess
from typing import List, Tuple, Dict

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
        print(f"Error getting original: {e}")

    # Fallback to current file
    with open(f'/home/cuzic/ai-dev-yodoq/slides/{input_file}', 'r', encoding='utf-8') as f:
        return f.read()

def parse_text_elements(content: str) -> List[Dict]:
    """Parse all text elements with their positions and font sizes"""
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

        # Extract font-size
        font_size = 50.0  # default
        style_match = re.search(r'style="([^"]+)"', attrs)
        if style_match:
            style = style_match.group(1)
            fs_match = re.search(r'font-size:\s*(\d+)px', style)
            if fs_match:
                font_size = float(fs_match.group(1))

        elements.append({
            'full_text': match.group(0),
            'x': x,
            'y': y,
            'font_size': font_size,
            'text_content': text_content
        })

    return elements

def find_overlaps(elements: List[Dict]) -> List[Tuple[int, int]]:
    """Find pairs of overlapping text elements"""
    overlaps = []

    for i in range(len(elements)):
        for j in range(i + 1, len(elements)):
            elem1 = elements[i]
            elem2 = elements[j]

            # Check if in same column (x within 100px)
            if abs(elem1['x'] - elem2['x']) > 100:
                continue

            # Check if overlapping in y
            min_gap = max(elem1['font_size'], elem2['font_size']) * 1.3
            y_diff = abs(elem1['y'] - elem2['y'])

            if y_diff < min_gap:
                # Determine which one should be moved down
                if elem1['y'] < elem2['y']:
                    overlaps.append((i, j))
                else:
                    overlaps.append((j, i))

    return overlaps

def fix_overlaps_minimal(content: str) -> Tuple[str, List[Tuple[str, float, float]]]:
    """Fix only overlapping elements, minimize changes"""
    elements = parse_text_elements(content)
    overlaps = find_overlaps(elements)

    # Track adjustments
    adjustments = {}  # index -> new_y
    fix_examples = []

    # Process overlaps - only move the second element in each pair
    processed = set()
    for idx1, idx2 in overlaps:
        if idx2 in processed:
            continue

        elem1 = elements[idx1]
        elem2 = elements[idx2]

        # Get current y positions (with any previous adjustments)
        y1 = adjustments.get(idx1, elem1['y'])
        y2 = adjustments.get(idx2, elem2['y'])

        # Calculate required gap
        min_gap = max(elem1['font_size'], elem2['font_size']) * 1.3
        required_y2 = y1 + min_gap

        if y2 < required_y2:
            old_y = elem2['y']
            adjustments[idx2] = required_y2

            text_preview = elem2['text_content']
            if len(text_preview) > 50:
                text_preview = text_preview[:47] + "..."

            if len(fix_examples) < 10:
                fix_examples.append((text_preview, old_y, required_y2))

            processed.add(idx2)

    # Apply adjustments to content
    modified_content = content
    for idx, new_y in sorted(adjustments.items(), key=lambda x: -x[0]):  # Process in reverse order
        elem = elements[idx]
        old_text = elem['full_text']
        old_y_str = re.search(r'y="([^"]+)"', old_text).group(1)
        new_text = old_text.replace(f'y="{old_y_str}"', f'y="{new_y}"')
        modified_content = modified_content.replace(old_text, new_text, 1)

    return modified_content, fix_examples

def update_viewbox(content: str) -> Tuple[str, str, str]:
    """Update viewBox based on max y coordinate"""
    # Find max y
    max_y = 0
    for match in re.finditer(r'y="([^"]+)"', content):
        try:
            y = float(match.group(1))
            if y > max_y:
                max_y = y
        except ValueError:
            pass

    # Get current viewBox
    viewbox_match = re.search(r'viewBox="([^"]+)"', content)
    old_viewbox = viewbox_match.group(1) if viewbox_match else "0 0 1820 1105"

    # Calculate new height (max_y + padding)
    new_height = int(max_y + 100)

    # Update viewBox
    parts = old_viewbox.split()
    if len(parts) == 4:
        parts[3] = str(new_height)
        new_viewbox = ' '.join(parts)
        content = content.replace(f'viewBox="{old_viewbox}"', f'viewBox="{new_viewbox}"')
    else:
        new_viewbox = old_viewbox

    return content, old_viewbox, new_viewbox

def main():
    output_files = [
        '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_42_regression_mechanism.svg',
        '/home/cuzic/ai-dev-yodoq/slides/diagrams-web/diagram_42_regression_mechanism.svg'
    ]

    print("Loading original SVG from git...")
    original_content = get_original_svg()

    print("Analyzing text overlaps...")
    modified_content, fix_examples = fix_overlaps_minimal(original_content)

    print("Updating viewBox...")
    modified_content, old_viewbox, new_viewbox = update_viewbox(modified_content)

    # Write to output files
    for output_file in output_files:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)

    print(f"\n{'='*60}")
    print("SVG TEXT OVERLAP FIX - FINAL REPORT")
    print(f"{'='*60}")

    print(f"\n修正したテキスト要素の数: {len(fix_examples)}")

    print(f"\n修正前後のY座標の例:")
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
    for output_file in output_files:
        print(f"  - {output_file}")

    print(f"\n{'='*60}")
    print("修正完了！")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
