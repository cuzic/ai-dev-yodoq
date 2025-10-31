#!/usr/bin/env python3
"""
Fixed SVG overflow checker that properly handles:
- Inline style attributes with font-size
- Japanese character width (wider than ASCII)
- text-anchor="middle" positioning
"""

import re
from pathlib import Path

def get_text_width(text, font_size):
    """Calculate estimated text width in pixels."""
    # Count character types
    japanese_chars = len([c for c in text if ord(c) > 127])
    ascii_chars = len(text) - japanese_chars

    # Japanese chars are ~0.85 of font_size, ASCII ~0.6
    width = (japanese_chars * font_size * 0.85) + (ascii_chars * font_size * 0.6)
    return width

def extract_font_size(text_element):
    """Extract font size from style attribute or class."""
    # Check inline style first
    style_match = re.search(r'style="[^"]*font-size:\s*(\d+)px', text_element)
    if style_match:
        return int(style_match.group(1))

    # Check class name
    class_match = re.search(r'class="([^"]*)"', text_element)
    if class_match:
        class_name = class_match.group(1)
        if 'title' in class_name:
            return 24
        elif 'subtitle' in class_name or 'section-title' in class_name:
            return 18
        elif 'item' in class_name:
            return 13
        elif 'desc' in class_name:
            return 12

    return 14  # default

def extract_text_anchor(text_element):
    """Extract text-anchor attribute."""
    # Check inline style
    style_match = re.search(r'text-anchor:\s*(\w+)', text_element)
    if style_match:
        return style_match.group(1)

    # Check attribute
    attr_match = re.search(r'text-anchor="(\w+)"', text_element)
    if attr_match:
        return attr_match.group(1)

    return 'start'  # default

def check_svg_overflow(svg_path):
    """Check a single SVG file for text overflow."""
    issues = []

    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract viewBox
    viewbox_match = re.search(r'viewBox="([^"]+)"', content)
    if not viewbox_match:
        return []

    vb_parts = viewbox_match.group(1).split()
    vb_width = float(vb_parts[2])
    vb_height = float(vb_parts[3])

    # Find all text elements (more flexible regex)
    text_pattern = r'<text[^>]*>(.*?)</text>'
    text_elements = re.findall(text_pattern, content, re.DOTALL)

    # Find full text element tags
    full_pattern = r'(<text[^>]*>.*?</text>)'
    full_elements = re.findall(full_pattern, content, re.DOTALL)

    for full_elem in full_elements:
        # Extract x, y
        x_match = re.search(r'x="([^"]*)"', full_elem)
        y_match = re.search(r'y="([^"]*)"', full_elem)

        if not x_match or not y_match:
            continue

        try:
            x = float(x_match.group(1))
            y = float(y_match.group(1))
        except ValueError:
            continue

        # Get text content
        text_match = re.search(r'<text[^>]*>(.*?)</text>', full_elem, re.DOTALL)
        if not text_match:
            continue

        text_content = text_match.group(1)
        clean_text = re.sub(r'<[^>]+>', '', text_content).strip()
        clean_text = clean_text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')

        if not clean_text:
            continue

        # Get font size
        font_size = extract_font_size(full_elem)

        # Get text anchor
        text_anchor = extract_text_anchor(full_elem)

        # Calculate text width
        text_width = get_text_width(clean_text, font_size)

        # Adjust x based on text-anchor
        if text_anchor == 'middle':
            effective_x_start = x - (text_width / 2)
            effective_x_end = x + (text_width / 2)
        elif text_anchor == 'end':
            effective_x_start = x - text_width
            effective_x_end = x
        else:  # start
            effective_x_start = x
            effective_x_end = x + text_width

        # Check overflow with 10px margin
        margin = 10

        if effective_x_start < margin:
            issues.append({
                'type': 'left_overflow',
                'text': clean_text[:40] + ('...' if len(clean_text) > 40 else ''),
                'x': x,
                'y': y,
                'font_size': font_size,
                'text_anchor': text_anchor,
                'overflow_px': margin - effective_x_start
            })

        if effective_x_end > vb_width - margin:
            issues.append({
                'type': 'right_overflow',
                'text': clean_text[:40] + ('...' if len(clean_text) > 40 else ''),
                'x': x,
                'y': y,
                'font_size': font_size,
                'text_anchor': text_anchor,
                'width': text_width,
                'overflow_px': effective_x_end - (vb_width - margin)
            })

        if y > vb_height - margin:
            issues.append({
                'type': 'bottom_overflow',
                'text': clean_text[:40] + ('...' if len(clean_text) > 40 else ''),
                'y': y,
                'viewbox_height': vb_height
            })

    return issues

def main():
    """Check all SVG diagrams."""
    diagrams_dir = Path(__file__).parent.parent / 'diagrams-web'

    if not diagrams_dir.exists():
        print(f"Error: {diagrams_dir} not found")
        return

    svg_files = sorted(diagrams_dir.glob('diagram_*.svg'))

    print(f"Checking {len(svg_files)} SVG files for text overflow...\n")
    print("=" * 80)

    files_with_issues = 0
    total_issues = 0

    for svg_file in svg_files:
        issues = check_svg_overflow(svg_file)

        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"\n📄 {svg_file.name}")

            for issue in issues:
                if issue['type'] in ['left_overflow', 'right_overflow']:
                    direction = 'LEFT' if issue['type'] == 'left_overflow' else 'RIGHT'
                    print(f"  ⚠️  {direction} OVERFLOW: {issue['overflow_px']:.1f}px")
                    print(f"     Text: {issue['text']}")
                    print(f"     Position: x={issue['x']:.0f}, anchor={issue['text_anchor']}, font={issue['font_size']}px")
                elif issue['type'] == 'bottom_overflow':
                    print(f"  ⚠️  BOTTOM OVERFLOW")
                    print(f"     Text: {issue['text']}")
                    print(f"     Position: y={issue['y']:.0f} (viewBox height: {issue['viewbox_height']})")

    print(f"\n{'=' * 80}")
    print(f"Files checked: {len(svg_files)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total issues: {total_issues}")

    if files_with_issues == 0:
        print("\n✅ All SVG files look good!")
    else:
        print(f"\n⚠️  {files_with_issues} files have overflow issues")

if __name__ == '__main__':
    main()
