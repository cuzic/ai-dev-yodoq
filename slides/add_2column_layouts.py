#!/usr/bin/env python3
"""Add two-column layout to slides with 8-14 bullets that have no layout."""

import re
from pathlib import Path

# Slides that need two-column layout added
FIXES_ADD_2COL = [
    (3, "本日の目標", 13),
    (14, "Claude Code とは", 10),
    (22, "STEP1 要件定義とは", 9),
    (30, "受け入れ基準（Given-When-Then）", 9),
    (36, "STEP2 設計ドキュメントとは", 9),
    (38, "Tech Stack Setup", 9),
    (40, "API仕様の明確化", 8),
    (44, "受け入れ条件の詳細化", 12),
    (72, "インクリメンタル実装の実例", 8),
    (78, "STEP5 品質担保＆ドキュメント反映とは", 9),
    (89, "自己レビューの実例", 8),
]

def add_2column_layouts(md_path):
    """Add two-column layout to specified slides."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slides = content.split('\n---\n')
    changes = []
    
    for slide_num, title, bullets in FIXES_ADD_2COL:
        if slide_num - 1 < len(slides):
            slide = slides[slide_num - 1]
            
            # Check if it has the title and no layout
            if title in slide and '<!-- _class:' not in slide:
                # Add two-column before the title
                new_slide = f'<!-- _class: two-column -->\n\n{slide}'
                slides[slide_num - 1] = new_slide
                changes.append(f"✓ Slide {slide_num}: {title} → added two-column ({bullets} bullets)")
    
    # Write back
    new_content = '\n---\n'.join(slides)
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return changes

def main():
    md_path = Path(__file__).parent / 'all_slides.md'
    
    print("=" * 70)
    print("ADDING TWO-COLUMN LAYOUTS")
    print("=" * 70)
    print()
    
    changes = add_2column_layouts(md_path)
    
    for change in changes:
        print(change)
    
    print()
    print(f"✅ Added {len(changes)} two-column layouts")
    print("=" * 70)

if __name__ == '__main__':
    main()
