#!/usr/bin/env python3
"""
Analyze actual text width in slides to detect real overflow.
Accounts for Japanese characters being wider than ASCII.
"""

import re
from pathlib import Path

def estimate_text_width_px(text, font_size=16):
    """
    Estimate text width in pixels.
    Japanese/Chinese chars: ~1.0x font size
    ASCII chars: ~0.55x font size
    """
    japanese_count = sum(1 for c in text if ord(c) > 127)
    ascii_count = len(text) - japanese_count

    width = (japanese_count * font_size * 1.0) + (ascii_count * font_size * 0.55)
    return width

def analyze_markdown_slides(md_path):
    """Analyze markdown slides for text that's too long."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = content.split('\n---\n')

    # Marp slide width is typically 1280px
    # With 2-column: ~600px per column
    # With 3-column: ~400px per column

    issues = []

    for idx, slide in enumerate(slides, 1):
        lines = slide.split('\n')

        # Detect layout
        layout = 'default'
        if 'three-column' in slide:
            layout = 'three-column'
            column_width = 400
        elif 'two-column' in slide:
            layout = 'two-column'
            column_width = 600
        elif 'card-grid' in slide:
            layout = 'card-grid'
            column_width = 350
        else:
            column_width = 1100  # Single column with margins

        # Get title
        title = "Untitled"
        for line in lines:
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                break

        # Check each line
        for line_num, line in enumerate(lines, 1):
            clean_line = line.strip()

            # Skip empty lines, headings, code fences, HTML comments
            if not clean_line or clean_line.startswith('#') or clean_line.startswith('```') or clean_line.startswith('<!--'):
                continue

            # Remove markdown formatting
            clean_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_line)  # bold
            clean_text = re.sub(r'\*([^*]+)\*', r'\1', clean_text)  # italic
            clean_text = re.sub(r'`([^`]+)`', r'\1', clean_text)  # code
            clean_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_text)  # links
            clean_text = re.sub(r'^[-*•]\s+', '', clean_text)  # list markers
            clean_text = clean_text.strip()

            if not clean_text:
                continue

            # Estimate width
            # Headings are larger font
            if clean_line.startswith('##'):
                font_size = 28
            elif clean_line.startswith('###'):
                font_size = 24
            else:
                font_size = 16

            estimated_width = estimate_text_width_px(clean_text, font_size)

            # Check overflow (with 40px margin)
            margin = 40
            if estimated_width > column_width - margin:
                overflow = estimated_width - (column_width - margin)
                issues.append({
                    'slide': idx,
                    'title': title,
                    'layout': layout,
                    'line': clean_line[:80] + ('...' if len(clean_line) > 80 else ''),
                    'estimated_width': estimated_width,
                    'column_width': column_width,
                    'overflow': overflow,
                    'chars': len(clean_text)
                })

    return issues

def main():
    md_path = Path(__file__).parent / 'all_slides.md'

    if not md_path.exists():
        print(f"❌ {md_path} not found")
        return

    print("=" * 80)
    print("ANALYZING ACTUAL TEXT WIDTH IN RENDERED SLIDES")
    print("=" * 80)
    print()

    issues = analyze_markdown_slides(md_path)

    if not issues:
        print("✅ No overflow issues detected!")
        return

    # Group by slide
    slides_with_issues = {}
    for issue in issues:
        slide_num = issue['slide']
        if slide_num not in slides_with_issues:
            slides_with_issues[slide_num] = []
        slides_with_issues[slide_num].append(issue)

    print(f"⚠️  Found {len(issues)} lines with potential overflow in {len(slides_with_issues)} slides\n")

    # Show worst offenders
    for slide_num in sorted(slides_with_issues.keys()):
        slide_issues = slides_with_issues[slide_num]
        issue = slide_issues[0]

        print(f"📍 Slide {slide_num}: {issue['title']}")
        print(f"   Layout: {issue['layout']} (column width: {issue['column_width']}px)")
        print(f"   Issues: {len(slide_issues)} lines overflow")

        # Show worst 3 lines
        for i, line_issue in enumerate(sorted(slide_issues, key=lambda x: x['overflow'], reverse=True)[:3]):
            print(f"   {i+1}. {line_issue['line']}")
            print(f"      Width: {line_issue['estimated_width']:.0f}px (overflow: {line_issue['overflow']:.0f}px)")
        print()

    print("=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    print("1. Split long sentences into multiple lines")
    print("2. Use abbreviations where possible")
    print("3. Remove redundant words")
    print("4. For 3-column: max ~40 chars per line")
    print("5. For 2-column: max ~60 chars per line")

if __name__ == '__main__':
    main()
