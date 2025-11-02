#!/usr/bin/env python3
"""Analyze backup files to understand structure for /generate-slides"""

import re
from pathlib import Path

def analyze_file(filepath):
    """Analyze a single backup file"""
    content = filepath.read_text(encoding='utf-8')

    # Extract headings
    h1_pattern = r'^# (.+)$'
    h2_pattern = r'^## (.+)$'
    slide_separator = r'^---$'
    image_pattern = r'!\[.*?\]\((diagrams/.*?\.svg)\)'

    h1_headings = re.findall(h1_pattern, content, re.MULTILINE)
    h2_headings = re.findall(h2_pattern, content, re.MULTILINE)
    slide_count = len(re.findall(slide_separator, content, re.MULTILINE))
    images = re.findall(image_pattern, content)

    # Count bullet points
    bullet_pattern = r'^[\s]*[-*] .+$'
    bullets = re.findall(bullet_pattern, content, re.MULTILINE)

    # Count layout classes
    layout_classes = re.findall(r'<!-- _class: (.+?) -->', content)

    return {
        'filename': filepath.name,
        'total_lines': len(content.split('\n')),
        'total_chars': len(content),
        'h1_count': len(h1_headings),
        'h2_count': len(h2_headings),
        'slide_count': slide_count,
        'bullet_count': len(bullets),
        'image_count': len(images),
        'unique_images': len(set(images)),
        'layout_classes': layout_classes,
        'h1_headings': h1_headings[:10],  # First 10
        'h2_headings': h2_headings[:10],  # First 10
    }

def main():
    backup_files = sorted(Path('.').glob('day*.md.backup'))

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 MANUSCRIPT ANALYSIS - Backup Files")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    total_slides = 0
    total_h1 = 0
    total_h2 = 0
    total_images = 0

    for filepath in backup_files:
        result = analyze_file(filepath)
        total_slides += result['slide_count']
        total_h1 += result['h1_count']
        total_h2 += result['h2_count']
        total_images += result['image_count']

        print(f"📄 {result['filename']}")
        print(f"   Lines: {result['total_lines']}, Chars: {result['total_chars']}")
        print(f"   H1: {result['h1_count']}, H2: {result['h2_count']}")
        print(f"   Slides: {result['slide_count']}, Images: {result['image_count']}")
        print(f"   Bullets: {result['bullet_count']}")
        print(f"   Layouts: {', '.join(set(result['layout_classes']))}")
        print()

        if result['h1_headings']:
            print(f"   H1 Topics (first 10):")
            for i, h1 in enumerate(result['h1_headings'][:10], 1):
                print(f"   {i}. {h1}")
            print()

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 TOTAL SUMMARY")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Total files: {len(backup_files)}")
    print(f"Total slides: {total_slides}")
    print(f"Total H1 sections: {total_h1}")
    print(f"Total H2 topics: {total_h2}")
    print(f"Total images: {total_images}")
    print()

    print("🎯 Recommendations:")
    print(f"  - Current: {total_slides} slides across {len(backup_files)} files")
    print(f"  - Average: {total_slides // len(backup_files)} slides per file")
    print(f"  - Consider: Restructuring to reduce redundancy")
    print(f"  - Consider: Grouping related topics more tightly")

if __name__ == '__main__':
    main()
