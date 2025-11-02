#!/usr/bin/env python3
"""
Review all slides with supercompact/ultracompact to ensure they're appropriate.
Provides a summary of compact class usage across all slides.
"""

import re
from typing import List, Tuple
from collections import Counter

def extract_slides(filepath: str) -> List[Tuple[int, int, int, str]]:
    """Extract slide boundaries from the markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    slides = []
    slide_num = 0
    current_start = 0

    for i, line in enumerate(lines, 1):
        if line.strip() == '---':
            if current_start > 0:
                slides.append((slide_num, current_start, i, ''.join(lines[current_start-1:i])))
            slide_num += 1
            current_start = i + 1

    # Add last slide
    if current_start <= len(lines):
        slides.append((slide_num, current_start, len(lines), ''.join(lines[current_start-1:])))

    return slides

def extract_class_info(content: str) -> Tuple[str, str]:
    """Extract layout and compact classes from slide content."""
    class_match = re.search(r'<!--\s*_class:\s*([^-]+?)-->', content)
    if not class_match:
        return "none", "normal"

    classes = class_match.group(1).strip().split()

    layout_classes = ['lead', 'layout-diagram-only', 'layout-horizontal-left',
                      'layout-horizontal-right', 'layout-comparison', 'layout-callout',
                      'two-column', 'layout-timeline', 'layout-code-focus', 'card-grid', 'title']
    layout = next((c for c in classes if c in layout_classes), "normal")

    compact_classes = ['ultracompact', 'supercompact', 'compact', 'normal']
    compact = next((c for c in classes if c in compact_classes), "normal")

    return layout, compact

def count_content_chars(content: str) -> int:
    """Count meaningful content characters."""
    content_clean = re.sub(r'<!--\s*_class:.*?-->', '', content, flags=re.DOTALL)
    content_clean = re.sub(r'^---\s*$', '', content_clean, flags=re.MULTILINE)
    content_clean = re.sub(r'marp:\s*true', '', content_clean)
    content_clean = re.sub(r'theme:\s*\w+', '', content_clean)
    content_clean = re.sub(r'paginate:\s*\w+', '', content_clean)

    text_only = re.sub(r'!\[.*?\]\(.*?\)', '', content_clean)
    text_only = re.sub(r'```.*?```', '', text_only, flags=re.DOTALL)
    text_only = re.sub(r'`[^`]+`', '', text_only)
    text_only = re.sub(r'^\s*#+\s*', '', text_only, flags=re.MULTILINE)
    text_only = re.sub(r'^\s*[-*]\s*', '', text_only, flags=re.MULTILINE)
    text_only = re.sub(r'\*\*([^*]+)\*\*', r'\1', text_only)
    text_only = re.sub(r'__([^_]+)__', r'\1', text_only)
    text_only = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text_only)
    text_only = re.sub(r'<[^>]+>', '', text_only)

    return len(text_only.strip())

def main():
    filepath = "/home/cuzic/ai-dev-yodoq/slides/all_slides.md"

    print("Reviewing compact class usage across all slides...")
    print("=" * 80)

    slides = extract_slides(filepath)

    # Statistics
    compact_counts = Counter()
    layout_counts = Counter()

    compact_slides = {
        'ultracompact': [],
        'supercompact': [],
        'compact': [],
        'normal': []
    }

    for slide_num, start, end, content in slides:
        layout, compact = extract_class_info(content)
        char_count = count_content_chars(content)

        compact_counts[compact] += 1
        layout_counts[layout] += 1

        compact_slides[compact].append((slide_num, char_count, layout))

    # Print summary statistics
    print(f"\nTotal slides: {len(slides)}")
    print("\nCompact class distribution:")
    for compact_type in ['ultracompact', 'supercompact', 'compact', 'normal']:
        count = compact_counts[compact_type]
        pct = (count / len(slides)) * 100
        print(f"  {compact_type:15s}: {count:3d} slides ({pct:5.1f}%)")

    # Review ultracompact and supercompact slides
    print("\n" + "=" * 80)
    print("ULTRACOMPACT SLIDES (should have >200 chars for dense content)")
    print("=" * 80)

    for slide_num, char_count, layout in sorted(compact_slides['ultracompact'], key=lambda x: x[1]):
        status = "✓ OK" if char_count > 200 else "⚠ Review" if char_count > 150 else "❌ Too sparse"
        print(f"  Slide #{slide_num:3d}: {char_count:4d} chars, layout={layout:25s} {status}")

    print("\n" + "=" * 80)
    print("SUPERCOMPACT SLIDES (should have >150 chars for dense content)")
    print("=" * 80)

    for slide_num, char_count, layout in sorted(compact_slides['supercompact'], key=lambda x: x[1]):
        status = "✓ OK" if char_count > 150 else "⚠ Review" if char_count > 100 else "❌ Too sparse"
        print(f"  Slide #{slide_num:3d}: {char_count:4d} chars, layout={layout:25s} {status}")

    # Summary recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)

    ultra_sparse = [s for s in compact_slides['ultracompact'] if s[1] < 200]
    super_sparse = [s for s in compact_slides['supercompact'] if s[1] < 150]

    print(f"\nUltracompact slides to review: {len(ultra_sparse)}")
    print(f"Supercompact slides to review: {len(super_sparse)}")

    if not ultra_sparse and not super_sparse:
        print("\n✓ All compressed slides have appropriate content density!")
        print("  No further action needed.")
    else:
        print("\nConsider reviewing slides marked with ⚠ or ❌ above.")

if __name__ == "__main__":
    main()
