#!/usr/bin/env python3
"""Simplify three-column to two-column for slides with 8-13 bullets."""

import re
from pathlib import Path

# Slides using 3-column but should use 2-column
FIXES_SIMPLIFY = [
    (17, "モード詳細と使い分け", 9),
    (84, "AI自己レビュー4種類の使い分け", 10),
    (117, "つまずきポイントと対処法", 12),
    (120, "演習成功のチェックリスト①", 12),
    (184, "Untitled", 4),
    (196, "Untitled", 8),
]

def simplify_to_2col(md_path):
    """Change three-column to two-column for specified slides."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slides = content.split('\n---\n')
    changes = []
    
    for slide_num, title_hint, bullets in FIXES_SIMPLIFY:
        if slide_num - 1 < len(slides):
            slide = slides[slide_num - 1]
            
            # Change three-column to two-column
            if '<!-- _class: three-column -->' in slide:
                new_slide = slide.replace(
                    '<!-- _class: three-column -->',
                    '<!-- _class: two-column -->'
                )
                slides[slide_num - 1] = new_slide
                title = title_hint if title_hint != "Untitled" else f"Slide {slide_num}"
                changes.append(f"✓ {title} → two-column ({bullets} bullets)")
    
    # Write back
    new_content = '\n---\n'.join(slides)
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return changes

def main():
    md_path = Path(__file__).parent / 'all_slides.md'
    
    print("=" * 70)
    print("SIMPLIFYING THREE-COLUMN TO TWO-COLUMN")
    print("=" * 70)
    print()
    
    changes = simplify_to_2col(md_path)
    
    for change in changes:
        print(change)
    
    print()
    print(f"✅ Simplified {len(changes)} layouts")
    print("=" * 70)

if __name__ == '__main__':
    main()
