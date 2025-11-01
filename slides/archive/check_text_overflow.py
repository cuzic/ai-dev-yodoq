#!/usr/bin/env python3
"""
Check SVG diagrams for text overflow issues.
Detects text that may be cut off due to:
- Text extending beyond viewBox boundaries
- Text too long for container width
"""

import re
from pathlib import Path

def check_svg_overflow(svg_path):
    """Check a single SVG file for text overflow issues."""
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

    # Find all text elements with simple regex
    text_pattern = r'<text[^>]*x="([^"]*)"[^>]*y="([^"]*)"[^>]*>(.*?)</text>'
    texts = re.findall(text_pattern, content, re.DOTALL)

    for x_str, y_str, text_content in texts:
        try:
            x = float(x_str)
            y = float(y_str)

            # Remove XML tags from content
            clean_text = re.sub(r'<[^>]+>', '', text_content).strip()
            if not clean_text:
                continue

            # Estimate text width (rough approximation)
            # Japanese characters: ~0.8 of font size, ASCII: ~0.6
            font_size = 14  # default assumption
            char_width = font_size * 0.7
            estimated_width = len(clean_text) * char_width

            # Check horizontal overflow
            if x + estimated_width > vb_width:
                overflow = x + estimated_width - vb_width
                issues.append({
                    'type': 'horizontal_overflow',
                    'text': clean_text[:50] + ('...' if len(clean_text) > 50 else ''),
                    'x': x,
                    'y': y,
                    'overflow_px': overflow
                })

            # Check vertical overflow
            if y > vb_height:
                issues.append({
                    'type': 'vertical_overflow',
                    'text': clean_text[:50] + ('...' if len(clean_text) > 50 else ''),
                    'y': y
                })

            # Check for very long text
            if len(clean_text) > 100:
                issues.append({
                    'type': 'long_text',
                    'text': clean_text[:50] + '...',
                    'length': len(clean_text)
                })

        except (ValueError, IndexError):
            continue

    return issues

def main():
    """Check all SVG diagrams for overflow issues."""
    diagrams_dir = Path(__file__).parent.parent / 'diagrams-web'

    if not diagrams_dir.exists():
        print(f"Error: {diagrams_dir} not found")
        return

    svg_files = sorted(diagrams_dir.glob('diagram_*.svg'))

    print(f"Checking {len(svg_files)} SVG files for text overflow...\n")

    files_with_issues = 0
    total_issues = 0

    for svg_file in svg_files:
        issues = check_svg_overflow(svg_file)

        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"\n{svg_file.name}:")

            for issue in issues:
                if issue['type'] == 'horizontal_overflow':
                    print(f"  ⚠️  HORIZONTAL OVERFLOW ({issue['overflow_px']:.0f}px)")
                    print(f"      Text: {issue['text']}")
                    print(f"      At: x={issue['x']:.0f}, y={issue['y']:.0f}")

                elif issue['type'] == 'vertical_overflow':
                    print(f"  ⚠️  VERTICAL OVERFLOW")
                    print(f"      Text: {issue['text']}")
                    print(f"      At: y={issue['y']:.0f}")

                elif issue['type'] == 'long_text':
                    print(f"  ⚠️  LONG TEXT ({issue['length']} chars)")
                    print(f"      Text: {issue['text']}")

    print(f"\n{'='*60}")
    print(f"Files checked: {len(svg_files)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total issues: {total_issues}")

    if files_with_issues == 0:
        print("\n✅ All SVG files look good!")
    else:
        print(f"\n⚠️  {files_with_issues} files need attention")

if __name__ == '__main__':
    main()
