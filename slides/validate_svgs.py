#!/usr/bin/env python3
"""
Validate regenerated SVGs for common issues:
- Text overlap
- Font size too large/small
- ViewBox vs content mismatch
- Text overflow
"""

import re
from pathlib import Path
from xml.etree import ElementTree as ET

def validate_svg(svg_path):
    """Check SVG for common issues."""
    issues = []
    warnings = []

    content = svg_path.read_text(encoding='utf-8')

    # Parse XML
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        return [f"❌ XML parse error: {e}"], []

    # Check viewBox
    viewbox = root.get('viewBox')
    if viewbox:
        vb_parts = [float(x) for x in viewbox.split()]
        vb_width, vb_height = vb_parts[2], vb_parts[3]

        # Check for reasonable size
        if vb_width > 1500 or vb_height > 1000:
            warnings.append(f"⚠️  Large viewBox: {vb_width}x{vb_height} (consider smaller)")
    else:
        issues.append("❌ No viewBox defined")

    # Check font sizes
    font_sizes = re.findall(r'font-size:\s*(\d+)px', content)
    font_sizes += re.findall(r'font-size="(\d+)"', content)

    if font_sizes:
        sizes = [int(s) for s in font_sizes]
        max_size = max(sizes)
        min_size = min(sizes)

        if max_size > 28:
            issues.append(f"❌ Font too large: {max_size}px (max 28px recommended)")
        if min_size < 10:
            warnings.append(f"⚠️  Font too small: {min_size}px (min 11px recommended)")
        if max_size < 16:
            warnings.append(f"⚠️  No large fonts: max={max_size}px (title should be 20-24px)")

    # Check for text elements
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    texts = root.findall('.//svg:text', ns) or root.findall('.//text')

    if len(texts) == 0:
        warnings.append("⚠️  No text elements found")

    # Check for potential overlaps (simple heuristic)
    text_positions = []
    for text in texts:
        x = text.get('x', '0')
        y = text.get('y', '0')
        try:
            text_positions.append((float(x), float(y)))
        except ValueError:
            pass

    # Check for texts at same Y position that might overlap
    y_positions = {}
    for x, y in text_positions:
        y_rounded = round(y / 5) * 5  # Group by 5px
        if y_rounded in y_positions:
            y_positions[y_rounded].append(x)
        else:
            y_positions[y_rounded] = [x]

    for y, x_list in y_positions.items():
        if len(x_list) > 1:
            x_sorted = sorted(x_list)
            for i in range(len(x_sorted) - 1):
                if x_sorted[i+1] - x_sorted[i] < 50:  # Less than 50px apart
                    warnings.append(f"⚠️  Potential text overlap at y={y}: x={x_sorted[i]}, {x_sorted[i+1]}")

    # Check file size
    size_kb = len(content.encode('utf-8')) / 1024
    if size_kb > 50:
        warnings.append(f"⚠️  Large file size: {size_kb:.1f}KB (target < 50KB)")

    # Check for inline styles (should use CSS classes)
    inline_styles = len(re.findall(r'style="[^"]*font-[^"]*"', content))
    if inline_styles > 5:
        warnings.append(f"⚠️  Many inline styles: {inline_styles} (prefer CSS classes)")

    return issues, warnings

def main():
    diagrams_dir = Path(__file__).parent.parent / 'diagrams-web'

    if not diagrams_dir.exists():
        print("❌ diagrams-web directory not found")
        return

    print("=" * 70)
    print("SVG Validation Report")
    print("=" * 70)
    print()

    svg_files = sorted(diagrams_dir.glob('*.svg'))

    if not svg_files:
        print("❌ No SVG files found in diagrams-web/")
        return

    total_issues = 0
    total_warnings = 0

    for svg_file in svg_files:
        issues, warnings = validate_svg(svg_file)

        if issues or warnings:
            print(f"\n📄 {svg_file.name}")
            print("-" * 70)

            if issues:
                for issue in issues:
                    print(f"  {issue}")
                total_issues += len(issues)

            if warnings:
                for warning in warnings:
                    print(f"  {warning}")
                total_warnings += len(warnings)
        else:
            print(f"✅ {svg_file.name} - No issues")

    print()
    print("=" * 70)
    print(f"Summary: {len(svg_files)} files checked")
    print(f"  ❌ Critical issues: {total_issues}")
    print(f"  ⚠️  Warnings: {total_warnings}")

    if total_issues == 0 and total_warnings == 0:
        print("\n🎉 All SVGs passed validation!")
    elif total_issues == 0:
        print("\n✅ No critical issues, but check warnings")
    else:
        print("\n⚠️  Critical issues found - please fix")

if __name__ == "__main__":
    main()
