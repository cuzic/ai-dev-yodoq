#!/usr/bin/env python3
"""
Analyze SVG files for horizontal text overlaps.
Detects cases where text elements overlap horizontally (same y-coordinate).
"""

import xml.etree.ElementTree as ET
import re
from pathlib import Path

def get_font_size(text_elem):
    """Extract font size from text element."""
    style = text_elem.get('style', '')
    font_size_match = re.search(r'font-size:\s*(\d+(?:\.\d+)?)', style)
    if font_size_match:
        return float(font_size_match.group(1))

    fs = text_elem.get('font-size')
    if fs:
        font_size_num = re.search(r'(\d+(?:\.\d+)?)', fs)
        if font_size_num:
            return float(font_size_num.group(1))

    return 16  # default

def estimate_text_width(text_content, font_size):
    """Estimate text width based on character count and font size."""
    # Rough estimate: average character width is ~0.5 * font_size for monospace
    # For proportional fonts, ~0.5-0.6 * font_size
    # Japanese characters are wider: ~1.0 * font_size

    char_count = len(text_content)

    # Count Japanese characters (wider)
    japanese_count = sum(1 for c in text_content if ord(c) > 0x3000)
    latin_count = char_count - japanese_count

    # Estimate width
    width = japanese_count * font_size * 1.0 + latin_count * font_size * 0.5

    return width

def analyze_svg_horizontal_overlap(svg_path):
    """Analyze SVG for horizontal text overlaps."""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Get viewBox
        viewBox = root.get('viewBox', '0 0 1000 800')
        viewBox_parts = viewBox.split()
        viewBox_width = float(viewBox_parts[2]) if len(viewBox_parts) >= 3 else 1000

        ns = {'svg': 'http://www.w3.org/2000/svg'}
        text_elements = root.findall('.//svg:text', ns) + root.findall('.//text')

        if not text_elements:
            return None

        # Collect text info
        text_info = []
        for text_elem in text_elements:
            x = text_elem.get('x')
            y = text_elem.get('y')

            if not x or not y:
                continue

            try:
                x = float(x)
                y = float(y)
            except ValueError:
                continue

            font_size = get_font_size(text_elem)
            text_content = ''.join(text_elem.itertext()).strip()

            if not text_content:
                continue

            text_width = estimate_text_width(text_content, font_size)

            text_info.append({
                'x': x,
                'y': y,
                'font_size': font_size,
                'text': text_content,
                'width': text_width,
                'end_x': x + text_width
            })

        # Sort by y then x
        text_info.sort(key=lambda t: (t['y'], t['x']))

        # Detect horizontal overlaps (same y coordinate)
        horizontal_overlaps = []

        for i in range(len(text_info) - 1):
            curr = text_info[i]
            next_elem = text_info[i + 1]

            # Check if on same horizontal line (within 10px y tolerance)
            y_diff = abs(curr['y'] - next_elem['y'])
            if y_diff > 10:
                continue

            # Check if horizontally overlapping
            # Current text ends at curr['end_x']
            # Next text starts at next_elem['x']
            gap = next_elem['x'] - curr['end_x']

            if gap < 0:
                # Overlap!
                overlap_amount = -gap
                overlap_severity = overlap_amount / min(curr['width'], next_elem['width'])

                horizontal_overlaps.append({
                    'curr_text': curr['text'][:50],
                    'next_text': next_elem['text'][:50],
                    'curr_x': curr['x'],
                    'next_x': next_elem['x'],
                    'y': curr['y'],
                    'overlap_amount': overlap_amount,
                    'severity': min(overlap_severity, 1.0),
                    'curr_width': curr['width'],
                    'gap': gap
                })

        # Detect excessively large fonts relative to viewBox
        large_fonts = []
        for info in text_info:
            # If font size is more than 10% of viewBox width, it's potentially too large
            if info['font_size'] > viewBox_width * 0.1:
                large_fonts.append({
                    'text': info['text'][:50],
                    'font_size': info['font_size'],
                    'viewBox_width': viewBox_width,
                    'ratio': info['font_size'] / viewBox_width
                })

            # If estimated text width exceeds viewBox width, it's definitely too wide
            if info['width'] > viewBox_width:
                large_fonts.append({
                    'text': info['text'][:50],
                    'font_size': info['font_size'],
                    'text_width': info['width'],
                    'viewBox_width': viewBox_width,
                    'overflow': info['width'] - viewBox_width
                })

        if horizontal_overlaps or large_fonts:
            return {
                'horizontal_overlaps': horizontal_overlaps,
                'large_fonts': large_fonts,
                'viewBox_width': viewBox_width
            }

        return None

    except Exception as e:
        return {'error': str(e)}

def main():
    diagrams_dir = Path('diagrams')

    if not diagrams_dir.exists():
        print("Error: diagrams/ directory not found")
        return

    svg_files = sorted(diagrams_dir.glob('diagram_*.svg'))

    print("=" * 80)
    print("SVG HORIZONTAL OVERLAP ANALYSIS")
    print("=" * 80)
    print()

    problematic_files = []

    for svg_path in svg_files:
        result = analyze_svg_horizontal_overlap(svg_path)

        if result:
            if 'error' in result:
                print(f"❌ {svg_path.name}: Error - {result['error']}")
                continue

            problematic_files.append((svg_path.name, result))

    if not problematic_files:
        print("✅ No horizontal overlap issues found!")
        return

    print(f"⚠️  Found {len(problematic_files)} files with potential issues:\n")

    for filename, result in problematic_files:
        print(f"{'=' * 80}")
        print(f"📄 {filename}")
        print(f"   ViewBox width: {result['viewBox_width']}px")
        print()

        if result['horizontal_overlaps']:
            print(f"   🔴 Horizontal overlaps: {len(result['horizontal_overlaps'])}")
            for i, overlap in enumerate(result['horizontal_overlaps'][:3], 1):
                print(f"      {i}. Text 1: \"{overlap['curr_text']}\"")
                print(f"         Position: x={overlap['curr_x']}, y={overlap['y']}")
                print(f"         Estimated width: {overlap['curr_width']:.1f}px")
                print(f"      → Text 2: \"{overlap['next_text']}\"")
                print(f"         Position: x={overlap['next_x']}, y={overlap['y']}")
                print(f"         Overlap: {overlap['overlap_amount']:.1f}px (severity: {overlap['severity']:.2f})")
                print()

            if len(result['horizontal_overlaps']) > 3:
                print(f"      ... and {len(result['horizontal_overlaps']) - 3} more overlaps")
                print()

        if result['large_fonts']:
            print(f"   ⚠️  Large fonts / Text overflow: {len(result['large_fonts'])}")
            for i, large in enumerate(result['large_fonts'][:3], 1):
                print(f"      {i}. \"{large['text']}\"")
                print(f"         Font size: {large['font_size']}px")
                if 'text_width' in large:
                    print(f"         Text width: {large['text_width']:.1f}px (exceeds viewBox by {large['overflow']:.1f}px)")
                elif 'ratio' in large:
                    print(f"         Ratio: {large['ratio']:.1%} of viewBox width")
                print()

            if len(result['large_fonts']) > 3:
                print(f"      ... and {len(result['large_fonts']) - 3} more issues")
                print()

        print()

    print("=" * 80)
    print(f"Summary: {len(problematic_files)} / {len(svg_files)} files need attention")
    print("=" * 80)

if __name__ == '__main__':
    main()
