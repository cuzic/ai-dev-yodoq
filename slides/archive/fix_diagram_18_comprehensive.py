#!/usr/bin/env python3
"""
Comprehensive fix for diagram_18 - handles all overlaps properly.
Uses 71px spacing for 54px fonts to ensure proper clearance.
"""

def fix_svg_comprehensive(input_path: str, output_paths: list):
    """Comprehensive SVG fix."""

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modifications = []

    # Use 71px spacing for 54px fonts (54 × 1.3 = 70.2, round up to 71)
    # Use 66px spacing for 50px fonts (50 × 1.3 = 65.0, round up to 66)

    # 1. Left Circle list - spacing 20px → 71px
    replacements = [
        ('<text x="150" y="260" class="circle-text">• リファクタリング</text>',
         '<text x="150" y="311" class="circle-text">• リファクタリング</text>'),
        ('<text x="150" y="280" class="circle-text">• テスト自動生成</text>',
         '<text x="150" y="382" class="circle-text">• テスト自動生成</text>'),
        ('<text x="150" y="300" class="circle-text">• ドキュメント作成</text>',
         '<text x="150" y="453" class="circle-text">• ドキュメント作成</text>'),
        ('<text x="150" y="320" class="circle-text">• パターン適用</text>',
         '<text x="150" y="524" class="circle-text">• パターン適用</text>'),
        ('<text x="150" y="340" class="circle-text">• 既存コード理解</text>',
         '<text x="150" y="595" class="circle-text">• 既存コード理解</text>'),
        ('<text x="150" y="360" class="circle-text">• バグ検出</text>',
         '<text x="150" y="666" class="circle-text">• バグ検出</text>'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)
        modifications.append(f"Left circle: {old.split('>')[1].split('<')[0]}")

    # 2. Right Circle list - spacing 20px → 71px
    replacements = [
        ('<text x="540" y="260" class="circle-text">• 要件定義</text>',
         '<text x="540" y="311" class="circle-text">• 要件定義</text>'),
        ('<text x="540" y="280" class="circle-text">• アーキテクチャ設計</text>',
         '<text x="540" y="382" class="circle-text">• アーキテクチャ設計</text>'),
        ('<text x="540" y="300" class="circle-text">• 品質基準設定</text>',
         '<text x="540" y="453" class="circle-text">• 品質基準設定</text>'),
        ('<text x="540" y="320" class="circle-text">• セキュリティ判断</text>',
         '<text x="540" y="524" class="circle-text">• セキュリティ判断</text>'),
        ('<text x="540" y="340" class="circle-text">• ユーザー体験設計</text>',
         '<text x="540" y="595" class="circle-text">• ユーザー体験設計</text>'),
        ('<text x="540" y="360" class="circle-text">• 最終意思決定</text>',
         '<text x="540" y="666" class="circle-text">• 最終意思決定</text>'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)
        modifications.append(f"Right circle: {old.split('>')[1].split('<')[0]}")

    # 3. Center overlap section - increase spacing to 71px
    replacements = [
        ('<text x="400" y="323" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • AIが実装\n  </text>',
         '<text x="400" y="376" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • AIが実装\n  </text>'),
        ('<text x="400" y="341" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • 人がレビュー\n  </text>',
         '<text x="400" y="447" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • 人がレビュー\n  </text>'),
        ('<text x="400" y="359" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • AIが改善\n  </text>',
         '<text x="400" y="518" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • AIが改善\n  </text>'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)
        modifications.append(f"Center: {old.split('>')[1].split('<')[0].strip()}")

    # 4. Move bottom section down to avoid overlapping with circles
    # Current: y=500 for background rect, y=530 for title
    # Move to y=750 for background, y=780 for title

    content = content.replace(
        '<rect x="50" y="500" width="700" height="380"',
        '<rect x="50" y="750" width="700" height="380"'
    )

    content = content.replace(
        '<text x="400" y="530" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 72px; fill: #00146E; text-anchor: middle; font-weight: bold;">\n    ギャップ分析の活用\n  </text>',
        '<text x="400" y="780" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 72px; fill: #00146E; text-anchor: middle; font-weight: bold;">\n    ギャップ分析の活用\n  </text>'
    )

    # 5. Move column rectangles down
    content = content.replace(
        '<rect x="70" y="550" width="200" height="220"',
        '<rect x="70" y="800" width="200" height="220"'
    )
    content = content.replace(
        '<rect x="300" y="550" width="200" height="220"',
        '<rect x="300" y="800" width="200" height="220"'
    )
    content = content.replace(
        '<rect x="530" y="550" width="200" height="220"',
        '<rect x="530" y="800" width="200" height="220"'
    )

    # 6. Move column titles down
    replacements = [
        ('<text x="170" y="575" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 64px; fill: white; text-anchor: middle; font-weight: bold;">\n    Fit（適合）\n  </text>',
         '<text x="170" y="825" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 64px; fill: white; text-anchor: middle; font-weight: bold;">\n    Fit（適合）\n  </text>'),
        ('<text x="400" y="575" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 64px; fill: white; text-anchor: middle; font-weight: bold;">\n    Gap（不足）\n  </text>',
         '<text x="400" y="825" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 64px; fill: white; text-anchor: middle; font-weight: bold;">\n    Gap（不足）\n  </text>'),
        ('<text x="630" y="575" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 64px; fill: white; text-anchor: middle; font-weight: bold;">\n    戦略的役割分担\n  </text>',
         '<text x="630" y="825" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 64px; fill: white; text-anchor: middle; font-weight: bold;">\n    戦略的役割分担\n  </text>'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)
        modifications.append(f"Column title: {old.split('>')[1].split('<')[0].strip()}")

    # 7. Bottom columns - spacing 71px/66px
    replacements = [
        # Left column
        ('<text x="85" y="595" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white;">\n    AIに任せる領域\n  </text>',
         '<text x="85" y="860" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white;">\n    AIに任せる領域\n  </text>'),
        ('<text x="85" y="612" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 自動化・効率化\n  </text>',
         '<text x="85" y="931" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 自動化・効率化\n  </text>'),
        ('<text x="85" y="628" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → スピード重視\n  </text>',
         '<text x="85" y="997" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → スピード重視\n  </text>'),

        # Middle column
        ('<text x="315" y="595" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white;">\n    人が補完する領域\n  </text>',
         '<text x="315" y="860" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white;">\n    人が補完する領域\n  </text>'),
        ('<text x="315" y="612" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 検証・判断\n  </text>',
         '<text x="315" y="931" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 検証・判断\n  </text>'),
        ('<text x="315" y="628" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 品質保証\n  </text>',
         '<text x="315" y="997" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 品質保証\n  </text>'),

        # Right column
        ('<text x="545" y="595" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white;">\n    最適な協働パターン\n  </text>',
         '<text x="545" y="860" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white;">\n    最適な協働パターン\n  </text>'),
        ('<text x="545" y="612" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 生産性最大化\n  </text>',
         '<text x="545" y="931" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 生産性最大化\n  </text>'),
        ('<text x="545" y="628" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 品質担保\n  </text>',
         '<text x="545" y="997" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 50px; fill: white;">\n    → 品質担保\n  </text>'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)
        modifications.append(f"Bottom: {old.split('>')[1].split('<')[0].strip()}")

    # 8. Update viewBox to accommodate all content
    content = content.replace('viewBox="0 0 1040 910"', 'viewBox="0 0 1040 1200"')

    # Write output files
    for output_path in output_paths:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    return len(modifications)


if __name__ == '__main__':
    input_path = '/tmp/diagram_18_original.svg'
    output_paths = [
        '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_18_fit_gap_analysis.svg',
        '/home/cuzic/ai-dev-yodoq/slides/diagrams-web/diagram_18_fit_gap_analysis.svg'
    ]

    num_mods = fix_svg_comprehensive(input_path, output_paths)

    print("=" * 80)
    print("COMPREHENSIVE SVG FIX - FINAL REPORT")
    print("=" * 80)
    print(f"\nTotal modifications: {num_mods}")
    print("\n--- Key Changes ---")
    print("1. Circle bullet spacing: 20px → 71px (54px × 1.32)")
    print("2. Center bullet spacing: 18px → 71px")
    print("3. Bottom section moved down: y 500 → y 750 (+250px)")
    print("4. Column text spacing: 71px for 54px fonts, 66px for 50px fonts")
    print("5. ViewBox expanded: height 910 → 1200 (+290px)")
    print(f"\n✓ Files saved:")
    for path in output_paths:
        print(f"  {path}")
    print("\n" + "=" * 80)
