#!/usr/bin/env python3
"""
Check rendered HTML slides for text overflow issues.
Opens the HTML file and analyzes actual text layout.
"""

import re
from pathlib import Path

def extract_slide_content(html_path):
    """Extract slide content sections from HTML."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all slide sections
    slide_pattern = r'<section[^>]*>(.*?)</section>'
    slides = re.findall(slide_pattern, content, re.DOTALL)

    issues = []

    for idx, slide in enumerate(slides, 1):
        # Check for list items (ul/ol)
        list_items = re.findall(r'<li>(.*?)</li>', slide, re.DOTALL)
        for item in list_items:
            clean_text = re.sub(r'<[^>]+>', '', item).strip()
            # Japanese/English mixed: ~1.5 chars per 1em with default font
            # At default slide width ~960px, max ~80 chars per line is safe
            if len(clean_text) > 80:
                issues.append({
                    'slide': idx,
                    'type': 'long_list_item',
                    'length': len(clean_text),
                    'text': clean_text[:60] + '...'
                })

        # Check paragraph text
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', slide, re.DOTALL)
        for para in paragraphs:
            clean_text = re.sub(r'<[^>]+>', '', para).strip()
            if len(clean_text) > 100:
                issues.append({
                    'slide': idx,
                    'type': 'long_paragraph',
                    'length': len(clean_text),
                    'text': clean_text[:60] + '...'
                })

        # Check for code blocks that might overflow
        code_blocks = re.findall(r'<code[^>]*>(.*?)</code>', slide, re.DOTALL)
        for code in code_blocks:
            lines = code.split('\n')
            for line_num, line in enumerate(lines, 1):
                clean_line = re.sub(r'<[^>]+>', '', line).strip()
                # Code typically uses monospace, stricter limit
                if len(clean_line) > 70:
                    issues.append({
                        'slide': idx,
                        'type': 'long_code_line',
                        'line': line_num,
                        'length': len(clean_line),
                        'text': clean_line[:60] + '...'
                    })

    return issues

def check_svg_dimensions():
    """Check SVG viewBox vs content dimensions."""
    diagrams_dir = Path(__file__).parent.parent / 'diagrams-web'
    svg_files = sorted(diagrams_dir.glob('diagram_*.svg'))

    issues = []

    for svg_file in svg_files:
        with open(svg_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract viewBox
        viewbox_match = re.search(r'viewBox="([^"]+)"', content)
        if not viewbox_match:
            continue

        vb_parts = viewbox_match.group(1).split()
        vb_width = float(vb_parts[2])
        vb_height = float(vb_parts[3])

        # Find all elements with x,y coordinates including transforms
        # Check for text elements
        text_elements = re.findall(
            r'<text[^>]*x="([^"]*)"[^>]*y="([^"]*)"[^>]*class="([^"]*)"[^>]*>(.*?)</text>',
            content, re.DOTALL
        )

        for x_str, y_str, class_name, text_content in text_elements:
            try:
                x = float(x_str)
                y = float(y_str)
                clean_text = re.sub(r'<[^>]+>', '', text_content).strip()

                if not clean_text:
                    continue

                # Get approximate font size from class
                font_size = 14  # default
                if 'title' in class_name:
                    font_size = 24
                elif 'subtitle' in class_name:
                    font_size = 18
                elif 'item' in class_name:
                    font_size = 13
                elif 'desc' in class_name:
                    font_size = 12

                # Estimate width more accurately
                # Japanese chars: ~0.9 * font_size, ASCII: ~0.6 * font_size
                # Average: ~0.75 * font_size
                est_char_width = font_size * 0.75
                est_width = len(clean_text) * est_char_width

                # Check with more strict margins (20px from edge)
                margin = 20
                if x + est_width > vb_width - margin:
                    overflow = x + est_width - (vb_width - margin)
                    issues.append({
                        'file': svg_file.name,
                        'type': 'text_overflow',
                        'x': x,
                        'y': y,
                        'text': clean_text[:50] + ('...' if len(clean_text) > 50 else ''),
                        'overflow': overflow,
                        'font_size': font_size,
                        'length': len(clean_text)
                    })

                if y > vb_height - margin:
                    issues.append({
                        'file': svg_file.name,
                        'type': 'vertical_overflow',
                        'y': y,
                        'text': clean_text[:50] + ('...' if len(clean_text) > 50 else '')
                    })

            except (ValueError, IndexError):
                continue

    return issues

def main():
    """Run all overflow checks."""
    print("=" * 80)
    print("CHECKING SVG DIAGRAMS FOR OVERFLOW")
    print("=" * 80)

    svg_issues = check_svg_dimensions()

    if svg_issues:
        print(f"\n⚠️  Found {len(svg_issues)} issues in SVG files:\n")

        current_file = None
        for issue in svg_issues:
            if issue['file'] != current_file:
                current_file = issue['file']
                print(f"\n📄 {current_file}")

            if issue['type'] == 'text_overflow':
                print(f"  ⚠️  OVERFLOW: {issue['overflow']:.0f}px beyond safe margin")
                print(f"     Text ({issue['length']} chars, font:{issue['font_size']}px): {issue['text']}")
                print(f"     Position: x={issue['x']:.0f}")
            elif issue['type'] == 'vertical_overflow':
                print(f"  ⚠️  VERTICAL OVERFLOW at y={issue['y']:.0f}")
                print(f"     Text: {issue['text']}")
    else:
        print("\n✅ No overflow issues found in SVG files!")

    print("\n" + "=" * 80)
    print("CHECKING HTML SLIDES FOR OVERFLOW")
    print("=" * 80)

    html_path = Path(__file__).parent / 'index.html'
    if not html_path.exists():
        print("❌ index.html not found in slides directory")
        return

    slide_issues = extract_slide_content(html_path)

    if slide_issues:
        print(f"\n⚠️  Found {len(slide_issues)} issues in HTML slides:\n")

        for issue in slide_issues:
            if issue['type'] == 'long_list_item':
                print(f"📍 Slide {issue['slide']}: Long list item ({issue['length']} chars)")
                print(f"   {issue['text']}")
            elif issue['type'] == 'long_paragraph':
                print(f"📍 Slide {issue['slide']}: Long paragraph ({issue['length']} chars)")
                print(f"   {issue['text']}")
            elif issue['type'] == 'long_code_line':
                print(f"📍 Slide {issue['slide']}: Long code line {issue['line']} ({issue['length']} chars)")
                print(f"   {issue['text']}")
    else:
        print("\n✅ No overflow issues found in HTML slides!")

    print("\n" + "=" * 80)
    print(f"TOTAL: {len(svg_issues) + len(slide_issues)} issues found")
    print("=" * 80)

if __name__ == '__main__':
    main()
