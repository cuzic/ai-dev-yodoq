#!/usr/bin/env python3
"""
Analyze actual text width in slides to detect real overflow.
FIXED VERSION - addresses multiple bugs.
"""

import re
from pathlib import Path

def estimate_text_width_px(text, font_size=16):
    """
    Estimate text width in pixels.
    Japanese/Chinese/CJK chars: ~1.0x font size
    ASCII chars: ~0.55x font size
    Emojis: ~1.5x font size (wider than regular chars)
    """
    emoji_count = 0
    japanese_count = 0
    ascii_count = 0

    for c in text:
        code = ord(c)
        # Emoji ranges (common ones)
        if (0x1F300 <= code <= 0x1F9FF or  # Misc symbols, emoticons
            0x2600 <= code <= 0x27BF or     # Misc symbols
            0xFE00 <= code <= 0xFE0F):      # Variation selectors
            emoji_count += 1
        # CJK Unicode ranges
        elif (0x3040 <= code <= 0x30FF or  # Hiragana, Katakana
              0x4E00 <= code <= 0x9FFF or  # CJK Unified Ideographs
              0xFF00 <= code <= 0xFFEF or  # Fullwidth forms
              code > 0x10000):              # Supplementary chars
            japanese_count += 1
        else:
            ascii_count += 1

    width = (emoji_count * font_size * 1.5) + \
            (japanese_count * font_size * 1.0) + \
            (ascii_count * font_size * 0.55)
    return width

def is_css_or_style_line(line):
    """Check if line is CSS or style code (not slide content)."""
    # CSS selectors
    if re.match(r'^\s*(section\.|\.[\w-]+\s*\{|@|font-|display:|grid-|column)', line):
        return True
    # Style tags
    if '<style>' in line or '</style>' in line:
        return True
    # YAML frontmatter
    if re.match(r'^\w+:\s*[|>]?$', line):
        return True
    return False

def get_actual_layout(slide_text):
    """
    Get the actual layout, checking class attribute precisely.
    Avoid false positives from CSS or comments.
    """
    # Look for Marp class directive
    match = re.search(r'<!--\s*_class:\s*([\w-]+)\s*-->', slide_text)
    if match:
        layout_class = match.group(1)
        # Exact match, not substring
        if layout_class == 'three-column':
            return 'three-column', 400
        elif layout_class == 'two-column':
            return 'two-column', 600
        elif layout_class == 'card-grid':
            return 'card-grid', 350
        elif 'horizontal' in layout_class:
            # horizontal layouts typically have text in one column
            return layout_class, 500

    return 'default', 1100

def clean_markdown_text(text):
    """Remove markdown formatting for width calculation."""
    # Remove bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    # Remove italic
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove list markers
    text = re.sub(r'^[-*•]\s+', '', text)
    # Remove checkbox markers
    text = re.sub(r'^\s*-\s*\[\s*[x ]?\s*\]\s*', '', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def analyze_markdown_slides(md_path):
    """Analyze markdown slides for text that's too long."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = content.split('\n---\n')
    issues = []

    for idx, slide in enumerate(slides, 1):
        lines = slide.split('\n')

        # Get layout and column width
        layout, column_width = get_actual_layout(slide)

        # Get title
        title = "Untitled"
        for line in lines:
            if line.startswith('# '):
                title = line.replace('# ', '').strip()
                break

        # Skip CSS/style blocks entirely
        in_style_block = False

        # Check each line
        for line_num, line in enumerate(lines, 1):
            # Check for style block
            if '<style>' in line:
                in_style_block = True
            if '</style>' in line:
                in_style_block = False
                continue

            if in_style_block:
                continue

            clean_line = line.strip()

            # Skip empty lines, headings, code fences, HTML comments
            if not clean_line:
                continue
            if clean_line.startswith('#'):
                continue
            if clean_line.startswith('```'):
                continue
            if clean_line.startswith('<!--'):
                continue

            # Skip CSS/YAML lines
            if is_css_or_style_line(clean_line):
                continue

            # Skip image references
            if clean_line.startswith('!['):
                continue

            # Clean markdown formatting
            clean_text = clean_markdown_text(clean_line)

            if not clean_text or len(clean_text) < 3:
                continue

            # Determine font size
            font_size = 16  # Default
            if line.startswith('##'):
                font_size = 28
            elif line.startswith('###'):
                font_size = 24

            # Estimate width
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
    print("ANALYZING ACTUAL TEXT WIDTH (FIXED VERSION)")
    print("=" * 80)
    print()

    issues = analyze_markdown_slides(md_path)

    # Filter out "Untitled" slides (usually CSS blocks)
    real_issues = [i for i in issues if i['title'] != "Untitled"]

    if not real_issues:
        print("✅ No overflow issues detected in real slides!")
        print(f"   (Found {len(issues)} in CSS/style blocks - ignored)")
        return

    # Group by slide
    slides_with_issues = {}
    for issue in real_issues:
        slide_num = issue['slide']
        if slide_num not in slides_with_issues:
            slides_with_issues[slide_num] = []
        slides_with_issues[slide_num].append(issue)

    print(f"⚠️  Found {len(real_issues)} lines with overflow in {len(slides_with_issues)} real slides")
    if len(issues) > len(real_issues):
        print(f"   (Ignored {len(issues) - len(real_issues)} lines in CSS/style blocks)\n")

    # Show worst offenders
    for slide_num in sorted(slides_with_issues.keys())[:10]:  # Limit to 10
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
