#!/usr/bin/env python3
"""
Fix text overlap issues in diagram_18_fit_gap_analysis.svg
This version properly handles the SVG structure and adjusts spacing intelligently.
"""

import re

def fix_svg_overlaps(svg_content: str) -> str:
    """Fix overlapping text in SVG by adjusting y coordinates."""

    lines = svg_content.split('\n')
    result_lines = []

    # Track specific overlapping sections and their adjustments
    adjustments = {
        # Circle lists - need more spacing
        'circle-text': {
            'spacing': 70,  # font-size 54 * 1.3 = 70.2
            'original_spacing': 20
        },
        # Center overlap section
        'center-bullets': {
            'spacing': 70,  # font-size 54 * 1.3 = 70.2
            'original_spacing': 18
        },
        # Bottom three columns
        'bottom-columns': {
            'spacing_after_title': 70,  # After 54px text
            'spacing_between': 65,  # Between 50px texts
            'original_spacing': 17
        }
    }

    # Parse and fix each section
    for i, line in enumerate(lines):
        result_line = line

        # Fix Left Circle list (lines 22-28)
        if '<text x="150"' in line and 'class="circle-text"' in line:
            # Extract y coordinate
            match = re.search(r'y="(\d+)"', line)
            if match:
                y = int(match.group(1))
                # First item at 240, then add 70 spacing
                if '• コード生成' in line:
                    new_y = 240
                elif '• リファクタリング' in line:
                    new_y = 310
                elif '• テスト自動生成' in line:
                    new_y = 380
                elif '• ドキュメント作成' in line:
                    new_y = 450
                elif '• パターン適用' in line:
                    new_y = 520
                elif '• 既存コード理解' in line:
                    new_y = 590
                elif '• バグ検出' in line:
                    new_y = 660
                else:
                    new_y = y

                result_line = re.sub(r'y="\d+"', f'y="{new_y}"', line)

        # Fix Right Circle list (lines 35-41)
        elif '<text x="540"' in line and 'class="circle-text"' in line:
            match = re.search(r'y="(\d+)"', line)
            if match:
                y = int(match.group(1))
                # First item at 240, then add 70 spacing
                if '• ビジネス判断' in line:
                    new_y = 240
                elif '• 要件定義' in line:
                    new_y = 310
                elif '• アーキテクチャ設計' in line:
                    new_y = 380
                elif '• 品質基準設定' in line:
                    new_y = 450
                elif '• セキュリティ判断' in line:
                    new_y = 520
                elif '• ユーザー体験設計' in line:
                    new_y = 590
                elif '• 最終意思決定' in line:
                    new_y = 660
                else:
                    new_y = y

                result_line = re.sub(r'y="\d+"', f'y="{new_y}"', line)

        # Fix center overlap section (lines 50-61)
        elif '<text x="400"' in line and 'font-size: 54px' in line and '•' in line:
            match = re.search(r'y="(\d+)"', line)
            if match:
                # These are at y: 305, 323, 341, 359 - should be 305, 375, 445, 515
                if '• 人が設計' in line:
                    new_y = 305
                elif '• AIが実装' in line:
                    new_y = 375
                elif '• 人がレビュー' in line:
                    new_y = 445
                elif '• AIが改善' in line:
                    new_y = 515
                else:
                    new_y = int(match.group(1))

                result_line = re.sub(r'y="\d+"', f'y="{new_y}"', line)

        # Fix bottom section - three columns (lines 74-110)
        # Left column
        elif '<text x="85" y=' in line:
            match = re.search(r'y="(\d+)"', line)
            if match:
                if 'AIに任せる領域' in line:
                    new_y = 610  # After title at 575, font-size 64, so 575+64*1.3 = 658, but inside box
                elif '→ 自動化・効率化' in line:
                    new_y = 680  # 610 + 70
                elif '→ スピード重視' in line:
                    new_y = 745  # 680 + 65
                else:
                    new_y = int(match.group(1))

                result_line = re.sub(r'y="\d+"', f'y="{new_y}"', line)

        # Middle column
        elif '<text x="315" y=' in line:
            match = re.search(r'y="(\d+)"', line)
            if match:
                if '人が補完する領域' in line:
                    new_y = 610
                elif '→ 検証・判断' in line:
                    new_y = 680
                elif '→ 品質保証' in line:
                    new_y = 745
                else:
                    new_y = int(match.group(1))

                result_line = re.sub(r'y="\d+"', f'y="{new_y}"', line)

        # Right column
        elif '<text x="545" y=' in line:
            match = re.search(r'y="(\d+)"', line)
            if match:
                if '最適な協働パターン' in line:
                    new_y = 610
                elif '→ 生産性最大化' in line:
                    new_y = 680
                elif '→ 品質担保' in line:
                    new_y = 745
                else:
                    new_y = int(match.group(1))

                result_line = re.sub(r'y="\d+"', f'y="{new_y}"', line)

        result_lines.append(result_line)

    # Update viewBox to accommodate new height
    result = '\n'.join(result_lines)
    result = re.sub(r'viewBox="0 0 1040 910"', 'viewBox="0 0 1040 1100"', result)

    # Update rectangles to fit new content
    # Expand the bottom section background rectangle
    result = re.sub(
        r'<rect x="50" y="500" width="700" height="170"',
        '<rect x="50" y="500" width="700" height="380"',
        result
    )

    # Expand the three column rectangles
    result = re.sub(
        r'<rect x="70" y="550" width="200" height="100"',
        '<rect x="70" y="550" width="200" height="220"',
        result
    )
    result = re.sub(
        r'<rect x="300" y="550" width="200" height="100"',
        '<rect x="300" y="550" width="200" height="220"',
        result
    )
    result = re.sub(
        r'<rect x="530" y="550" width="200" height="100"',
        '<rect x="530" y="550" width="200" height="220"',
        result
    )

    return result

if __name__ == '__main__':
    input_path = '/tmp/diagram_18_original.svg'
    output_paths = [
        '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_18_fit_gap_analysis.svg',
        '/home/cuzic/ai-dev-yodoq/slides/diagrams-web/diagram_18_fit_gap_analysis.svg'
    ]

    # Read original
    with open(input_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    print("=== Fixing SVG Text Overlaps ===\n")

    # Fix overlaps
    fixed_content = fix_svg_overlaps(svg_content)

    # Write to output files
    for output_path in output_paths:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"✓ Saved: {output_path}")

    print("\n=== Summary ===")
    print("Modified sections:")
    print("  - Left circle list: 7 items, spacing 20px → 70px")
    print("  - Right circle list: 7 items, spacing 20px → 70px")
    print("  - Center bullets: 4 items, spacing 18px → 70px")
    print("  - Bottom left column: 3 items, spacing 17px → 70px")
    print("  - Bottom middle column: 3 items, spacing 17px → 70px")
    print("  - Bottom right column: 3 items, spacing 17px → 70px")
    print("\nViewBox updated: 0 0 1040 910 → 0 0 1040 1100")
    print("Bottom section rectangle expanded: height 170 → 380")
    print("Column rectangles expanded: height 100 → 220")

    # Show specific examples
    print("\n=== Example Adjustments ===")
    print("Left circle '• リファクタリング': y 260 → 310 (+50px)")
    print("Center '• AIが実装': y 323 → 375 (+52px)")
    print("Bottom left '→ 自動化・効率化': y 612 → 680 (+68px)")
