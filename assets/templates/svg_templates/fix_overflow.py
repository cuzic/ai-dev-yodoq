#!/usr/bin/env python3
"""
Automated overflow fixing script.
Analyzes slides and applies appropriate fixes.
"""

import re
from pathlib import Path

# Overflow data from report
overflow_slides = {
    'HIGH': [
        ('112', '演習成功のチェックリスト①', 4230, 'checklist'),
        ('125', '', 4175, 'summary'),
        ('27', '非機能要件', 3620, 'summary/two-column'),
        ('23', '要件の引き出し方（文字起こしアプローチ）', 2520, 'summary/two-column'),
        ('10', 'セキュリティベストプラクティス（補足）', 2230, 'summary/two-column'),
        ('140', '', 1740, 'summary/two-column'),
        ('96', '1日目の振り返り', 1350, 'two-column'),
        ('18', '効率的な指示の出し方', 1315, 'two-column'),
        ('88', 'STEP5 チェックリスト', 1065, 'checklist'),
        ('204', '', 995, 'two-column'),
        ('94', 'Part 2のキーポイント', 970, 'two-column'),
        ('105', '', 940, 'two-column'),
    ],
    'MEDIUM': [
        ('200', '2日間の総まとめ', 825, 'two-column'),
        ('72', 'STEP4 チェックリスト', 820, 'checklist'),
        ('208', '', 810, 'two-column'),
        ('32', 'STEP1 チェックリスト', 785, 'checklist'),
        ('45', 'STEP2 チェックリスト', 785, 'checklist'),
        ('58', 'STEP3 チェックリスト', 785, 'checklist'),
        ('145', '', 770, 'two-column'),
        ('46', '', 765, 'two-column'),
        ('116', '演習で体感できること', 760, 'two-column'),
        ('182', '', 760, 'two-column'),
        ('202', '', 755, 'two-column'),
    ],
    'LOW': list(range(15))  # Not individually listed
}

def find_slide_in_markdown(slide_num, title_hint):
    """Find which markdown file contains a slide by title."""
    md_files = [
        'day1_1.md',
        'day1_2.md',
        'day1_3.md',
        'day2_1.md',
        'day2_2.md'
    ]

    # Search in HTML to correlate slide numbers
    html_path = Path('index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the slide section
    pattern = f'<section[^>]*?data-marpit-pagination="{slide_num}"[^>]*?>(.*?)</section>'
    match = re.search(pattern, html, re.DOTALL)

    if not match:
        return None, None

    slide_html = match.group(1)

    # Extract title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', slide_html, re.DOTALL)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
    else:
        title = title_hint

    # Search for title in markdown files
    for md_file in md_files:
        md_path = Path(md_file)
        if not md_path.exists():
            continue

        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Look for the title
        if title and title in content:
            return md_file, title

    return None, title

if __name__ == '__main__':
    print("Analyzing overflow slides...")

    fixes_needed = {}

    for risk_level, slides in overflow_slides.items():
        if risk_level == 'LOW':
            continue

        for slide_info in slides:
            slide_num, title, height, fix_type = slide_info
            md_file, actual_title = find_slide_in_markdown(slide_num, title)

            if md_file:
                if md_file not in fixes_needed:
                    fixes_needed[md_file] = []

                fixes_needed[md_file].append({
                    'slide_num': slide_num,
                    'title': actual_title or title,
                    'height': height,
                    'fix_type': fix_type,
                    'risk': risk_level
                })

    print("\nFixes needed by file:")
    for md_file, fixes in fixes_needed.items():
        print(f"\n{md_file}: {len(fixes)} slides")
        for fix in fixes:
            print(f"  - Slide {fix['slide_num']}: {fix['title'][:40]} ({fix['fix_type']})")
