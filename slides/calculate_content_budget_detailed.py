#!/usr/bin/env python3
"""
Calculate optimal content budget (character count) for each slide based on:
- Layout class (lead, card-grid, two-column, layout-horizontal, etc.)
- Font size class (normal, compact, supercompact, ultracompact)
- Slide dimensions (1280x720)
- Typography constraints (line height, padding, margins)
"""

import re
import json
from pathlib import Path

# Font size configurations (px)
FONT_SIZES = {
    'normal': 18,
    'compact': 16,
    'supercompact': 14,
    'ultracompact': 12
}

# Line height multipliers
LINE_HEIGHTS = {
    'normal': 1.6,
    'compact': 1.4,
    'supercompact': 1.3,
    'ultracompact': 1.2
}

# Slide dimensions
SLIDE_WIDTH = 1280
SLIDE_HEIGHT = 720

# Layout-specific usable areas (as percentage of slide)
LAYOUT_CONFIGS = {
    'lead': {
        'usable_width': 0.70,  # 70% width (centered)
        'usable_height': 0.60,  # 60% height (centered)
        'heading_ratio': 0.40,  # 40% for heading
        'text_ratio': 0.60,     # 60% for body text
        'avg_chars_per_line': 30  # Larger font
    },
    'title': {
        'usable_width': 0.70,
        'usable_height': 0.50,
        'heading_ratio': 0.50,
        'text_ratio': 0.50,
        'avg_chars_per_line': 35
    },
    'card-grid': {
        'usable_width': 0.90,
        'usable_height': 0.80,
        'sections': 4,  # Typically 4 cards
        'heading_ratio': 0.15,  # Small headings
        'text_ratio': 0.85,
        'avg_chars_per_line': 40
    },
    'two-column': {
        'usable_width': 0.90,
        'usable_height': 0.85,
        'columns': 2,
        'heading_ratio': 0.10,
        'text_ratio': 0.90,
        'avg_chars_per_line': 35  # Narrower columns
    },
    'layout-horizontal-left': {
        'usable_width': 0.45,  # 45% for text (image on right)
        'usable_height': 0.85,
        'heading_ratio': 0.10,
        'text_ratio': 0.90,
        'avg_chars_per_line': 30
    },
    'layout-horizontal-right': {
        'usable_width': 0.45,  # 45% for text (image on left)
        'usable_height': 0.85,
        'heading_ratio': 0.10,
        'text_ratio': 0.90,
        'avg_chars_per_line': 30
    },
    'layout-callout': {
        'usable_width': 0.75,
        'usable_height': 0.70,
        'heading_ratio': 0.20,
        'text_ratio': 0.80,
        'avg_chars_per_line': 40
    },
    'layout-diagram-only': {
        'usable_width': 0.90,
        'usable_height': 0.20,  # Mostly diagram, little text
        'heading_ratio': 0.30,
        'text_ratio': 0.70,
        'avg_chars_per_line': 50
    },
    'layout-comparison': {
        'usable_width': 0.90,
        'usable_height': 0.85,
        'sections': 2,  # Two comparison sections
        'heading_ratio': 0.10,
        'text_ratio': 0.90,
        'avg_chars_per_line': 35
    },
    'layout-timeline': {
        'usable_width': 0.90,
        'usable_height': 0.80,
        'sections': 5,  # Typically 5 timeline steps
        'heading_ratio': 0.15,
        'text_ratio': 0.85,
        'avg_chars_per_line': 35
    },
    'layout-code-focus': {
        'usable_width': 0.90,
        'usable_height': 0.75,
        'heading_ratio': 0.10,
        'text_ratio': 0.90,
        'avg_chars_per_line': 60  # Monospace code
    },
    'normal': {  # Default layout
        'usable_width': 0.85,
        'usable_height': 0.85,
        'heading_ratio': 0.10,
        'text_ratio': 0.90,
        'avg_chars_per_line': 45
    }
}

def calculate_budget(layout_class, font_class):
    """Calculate character budget for a slide configuration."""

    # Parse layout and font classes
    layout_type = 'normal'
    for layout in LAYOUT_CONFIGS.keys():
        if layout in layout_class:
            layout_type = layout
            break

    font_size_type = 'normal'
    if 'ultracompact' in font_class:
        font_size_type = 'ultracompact'
    elif 'supercompact' in font_class:
        font_size_type = 'supercompact'
    elif 'compact' in font_class:
        font_size_type = 'compact'

    # Get configuration
    layout_config = LAYOUT_CONFIGS[layout_type]
    font_size = FONT_SIZES[font_size_type]
    line_height = LINE_HEIGHTS[font_size_type]

    # Calculate usable area
    usable_width = SLIDE_WIDTH * layout_config['usable_width']
    usable_height = SLIDE_HEIGHT * layout_config['usable_height']

    # Calculate text area (excluding heading)
    text_height = usable_height * layout_config['text_ratio']

    # Calculate number of lines that fit
    line_height_px = font_size * line_height
    num_lines = int(text_height / line_height_px)

    # Calculate characters per line (Japanese + English mixed)
    # Japanese takes ~1.5x space of ASCII
    chars_per_line = layout_config['avg_chars_per_line']

    # Adjust for font size
    if font_size_type == 'compact':
        chars_per_line = int(chars_per_line * 1.125)  # +12.5%
    elif font_size_type == 'supercompact':
        chars_per_line = int(chars_per_line * 1.29)   # +29%
    elif font_size_type == 'ultracompact':
        chars_per_line = int(chars_per_line * 1.50)   # +50%

    # Total budget
    total_chars = num_lines * chars_per_line

    # Adjust for multi-section layouts
    if 'sections' in layout_config:
        # Distribute across sections
        per_section = total_chars // layout_config['sections']
        return {
            'total': total_chars,
            'per_section': per_section,
            'sections': layout_config['sections'],
            'lines': num_lines,
            'chars_per_line': chars_per_line,
            'font_size': font_size,
            'layout': layout_type,
            'font_class': font_size_type
        }

    if 'columns' in layout_config:
        per_column = total_chars // layout_config['columns']
        return {
            'total': total_chars,
            'per_column': per_column,
            'columns': layout_config['columns'],
            'lines': num_lines,
            'chars_per_line': chars_per_line,
            'font_size': font_size,
            'layout': layout_type,
            'font_class': font_size_type
        }

    return {
        'total': total_chars,
        'lines': num_lines,
        'chars_per_line': chars_per_line,
        'font_size': font_size,
        'layout': layout_type,
        'font_class': font_size_type
    }

def count_content(slide_text):
    """Count characters in slide content (excluding metadata)."""
    # Remove frontmatter and class declarations
    text = re.sub(r'---\nmarp:.*?---\n', '', slide_text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # Count headings separately
    headings = re.findall(r'^#+\s+(.+)$', text, re.MULTILINE)
    heading_chars = sum(len(h) for h in headings)

    # Remove headings from text
    text = re.sub(r'^#+\s+.+$', '', text, flags=re.MULTILINE)

    # Remove empty lines and whitespace
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())

    # Count body text
    body_chars = len(text.replace('\n', '').replace(' ', ''))

    return {
        'total': heading_chars + body_chars,
        'heading': heading_chars,
        'body': body_chars,
        'headings_count': len(headings)
    }

def analyze_all_slides():
    """Analyze all slides and calculate budgets."""
    files = ['slides/day1_1.md', 'slides/day1_2.md', 'slides/day1_3.md',
             'slides/day2_1.md', 'slides/day2_2.md']

    results = []
    slide_num = 0

    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        slides = content.split('\n---\n')

        for slide in slides:
            if slide.strip().startswith('---\nmarp:'):
                continue

            slide_num += 1

            # Extract class
            class_match = re.search(r'<!-- _class: (.+?) -->', slide)
            layout_class = class_match.group(1) if class_match else 'normal'

            # Extract title
            title_match = re.search(r'^#+\s+(.+)$', slide, re.MULTILINE)
            title = title_match.group(1)[:50] if title_match else 'NO TITLE'

            # Calculate budget
            budget = calculate_budget(layout_class, layout_class)

            # Count current content
            current = count_content(slide)

            # Calculate usage percentage
            usage = (current['total'] / budget['total'] * 100) if budget['total'] > 0 else 0

            # Determine status
            if usage > 120:
                status = 'OVER'
            elif usage > 100:
                status = 'FULL'
            elif usage > 80:
                status = 'GOOD'
            elif usage > 50:
                status = 'OK'
            else:
                status = 'SPARSE'

            results.append({
                'slide': slide_num,
                'title': title,
                'layout': budget['layout'],
                'font_class': budget['font_class'],
                'budget': budget['total'],
                'current': current['total'],
                'usage': round(usage, 1),
                'status': status,
                'lines': budget['lines'],
                'chars_per_line': budget['chars_per_line'],
                'overflow': current['total'] - budget['total'],
                'heading_chars': current['heading'],
                'body_chars': current['body']
            })

    return results

def main():
    """Main analysis and reporting."""
    print("=" * 80)
    print("CONTENT BUDGET ANALYSIS")
    print("=" * 80)
    print()

    results = analyze_all_slides()

    # Save detailed results
    with open('slides/.logs/content_budget_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Statistics
    over = [r for r in results if r['status'] == 'OVER']
    full = [r for r in results if r['status'] == 'FULL']
    good = [r for r in results if r['status'] == 'GOOD']
    ok = [r for r in results if r['status'] == 'OK']
    sparse = [r for r in results if r['status'] == 'SPARSE']

    print(f"Total slides analyzed: {len(results)}")
    print()
    print(f"OVER (>120%):   {len(over):3d} slides - Need content reduction or compact class")
    print(f"FULL (100-120%): {len(full):3d} slides - At capacity, good")
    print(f"GOOD (80-100%):  {len(good):3d} slides - Well balanced")
    print(f"OK (50-80%):     {len(ok):3d} slides - Could add more content")
    print(f"SPARSE (<50%):   {len(sparse):3d} slides - Too sparse, need content")
    print()

    # Show worst offenders
    print("=" * 80)
    print("TOP 20 SLIDES EXCEEDING BUDGET (Highest overflow)")
    print("=" * 80)
    print(f"{'Slide':<6} {'Usage':<8} {'Overflow':<10} {'Layout':<20} {'Title':<40}")
    print("-" * 80)

    over_sorted = sorted(results, key=lambda x: x['overflow'], reverse=True)[:20]
    for r in over_sorted:
        if r['overflow'] > 0:
            print(f"{r['slide']:<6} {r['usage']:>6.1f}% {r['overflow']:>8} {r['layout']:<20} {r['title'][:38]}")

    print()
    print("=" * 80)
    print("TOP 20 SPARSE SLIDES (Need more content)")
    print("=" * 80)
    print(f"{'Slide':<6} {'Usage':<8} {'Shortage':<10} {'Layout':<20} {'Title':<40}")
    print("-" * 80)

    sparse_sorted = sorted(results, key=lambda x: x['usage'])[:20]
    for r in sparse_sorted:
        shortage = r['budget'] - r['current']
        print(f"{r['slide']:<6} {r['usage']:>6.1f}% {shortage:>8} {r['layout']:<20} {r['title'][:38]}")

    print()
    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()

    if over:
        print(f"📝 {len(over)} slides exceed budget:")
        print("   → Option 1: Apply compact/supercompact class")
        print("   → Option 2: Condense content (remove redundancy)")
        print("   → Option 3: Split into multiple slides")
        print()

    if sparse:
        print(f"📝 {len(sparse)} slides are too sparse:")
        print("   → Add examples, explanations, or details")
        print("   → Add visual elements (diagrams, images)")
        print("   → Consider removing compact classes")
        print()

    print(f"✅ {len(good) + len(full)} slides are well-balanced")
    print()
    print("Detailed results saved to: slides/.logs/content_budget_analysis.json")

if __name__ == '__main__':
    main()
