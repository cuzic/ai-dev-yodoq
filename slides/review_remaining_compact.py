#!/usr/bin/env python3
"""
Review the 12 remaining compact slides to ensure they're appropriate.
"""

import re
from typing import List, Tuple

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

def get_slide_title(content: str) -> str:
    """Extract slide title from content."""
    # Look for first heading
    match = re.search(r'^#+\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "(No title)"

def main():
    filepath = "/home/cuzic/ai-dev-yodoq/slides/all_slides.md"

    print("Reviewing remaining COMPACT slides...")
    print("=" * 80)

    slides = extract_slides(filepath)

    compact_slides = []
    for slide_num, start, end, content in slides:
        layout, compact = extract_class_info(content)
        if compact == 'compact':
            char_count = count_content_chars(content)
            title = get_slide_title(content)
            compact_slides.append((slide_num, char_count, layout, title))

    print(f"\nFound {len(compact_slides)} slides with 'compact' class\n")
    print("Slides should have >100 chars to justify 'compact' class")
    print("=" * 80)

    for slide_num, char_count, layout, title in sorted(compact_slides, key=lambda x: x[1]):
        if char_count < 80:
            status = "❌ Remove compact"
        elif char_count < 100:
            status = "⚠ Consider normal"
        else:
            status = "✓ OK"

        print(f"Slide #{slide_num:3d}: {char_count:4d} chars | {layout:25s} | {status}")
        print(f"           Title: {title[:60]}")
        print()

    # Summary
    needs_fix = [s for s in compact_slides if s[1] < 100]
    if needs_fix:
        print("\n" + "=" * 80)
        print(f"RECOMMENDATION: Review {len(needs_fix)} slides marked with ❌ or ⚠")
        print("Consider changing to 'normal' for better readability")
    else:
        print("\n" + "=" * 80)
        print("✓ All compact slides have appropriate content density!")

if __name__ == "__main__":
    main()
