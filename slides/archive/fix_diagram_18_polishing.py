#!/usr/bin/env python3
"""
Final polishing for diagram_18 - fix remaining legitimate overlaps.
These are subtitle texts that need slight adjustment.
"""

def polish_svg(input_path: str, output_paths: list):
    """Polish the SVG by fixing remaining overlaps."""

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The remaining overlaps are intentional design choices within the circles
    # where subtitles appear close to main titles. These are acceptable for
    # visual design reasons. However, we can make small adjustments:

    # 1. Circle titles and subtitles - slightly increase spacing
    # "AIができること" (y=180, 72px) → "(AI Capabilities)" (y=205, 28px)
    # Gap should be at least 94px
    content = content.replace(
        '<text x="180" y="205" class="circle-title" font-size="28">(AI Capabilities)</text>',
        '<text x="180" y="275" class="circle-title" font-size="28">(AI Capabilities)</text>'
    )

    content = content.replace(
        '<text x="540" y="205" class="circle-title" font-size="28">(Human Required)</text>',
        '<text x="540" y="275" class="circle-title" font-size="28">(Human Required)</text>'
    )

    # 2. Center overlap section - keep "(Sweet Spot)" but adjust bullet below it
    # Increase first bullet gap
    content = content.replace(
        '<text x="400" y="250" class="overlap-title" text-anchor="middle" font-size="28">(Sweet Spot)</text>',
        '<text x="400" y="260" class="overlap-title" text-anchor="middle" font-size="28">(Sweet Spot)</text>'
    )

    # Move "人とAIの協働" down
    content = content.replace(
        '<text x="400" y="280" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 60px; fill: white; text-anchor: middle; font-weight: bold;">\n    人とAIの協働\n  </text>',
        '<text x="400" y="340" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 60px; fill: white; text-anchor: middle; font-weight: bold;">\n    人とAIの協働\n  </text>'
    )

    # Move first bullet下
    content = content.replace(
        '<text x="400" y="305" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • 人が設計\n  </text>',
        '<text x="400" y="420" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • 人が設計\n  </text>'
    )

    # Adjust remaining bullets
    content = content.replace(
        '<text x="400" y="376" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • AIが実装\n  </text>',
        '<text x="400" y="491" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • AIが実装\n  </text>'
    )

    content = content.replace(
        '<text x="400" y="447" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • 人がレビュー\n  </text>',
        '<text x="400" y="562" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • 人がレビュー\n  </text>'
    )

    content = content.replace(
        '<text x="400" y="518" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • AIが改善\n  </text>',
        '<text x="400" y="633" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 54px; fill: white; text-anchor: middle;">\n    • AIが改善\n  </text>'
    )

    # 3. Bottom section - move "Gap（不足）" title down
    content = content.replace(
        '<text x="400" y="825" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 64px; fill: white; text-anchor: middle; font-weight: bold;">\n    Gap（不足）\n  </text>',
        '<text x="400" y="874" style="font-family: \'Noto Sans JP\', sans-serif; font-size: 64px; fill: white; text-anchor: middle; font-weight: bold;">\n    Gap（不足）\n  </text>'
    )

    # Fix the one remaining overlap in right circle
    # "(Human Required)" (y=205) → "• ビジネス判断" (y=240) needs more gap
    # Already fixed above by moving subtitle to y=275

    # Write output
    for output_path in output_paths:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print("=" * 80)
    print("FINAL POLISHING COMPLETE")
    print("=" * 80)
    print("\nAdjustments made:")
    print("  1. Circle subtitles moved down: y 205 → 275 (+70px)")
    print("  2. Center '(Sweet Spot)' moved: y 250 → 260 (+10px)")
    print("  3. Center '人とAIの協働' moved: y 280 → 340 (+60px)")
    print("  4. Center bullets repositioned with 71px spacing")
    print("  5. Bottom 'Gap（不足）' moved: y 825 → 874 (+49px)")
    print(f"\n✓ Files saved to:")
    for path in output_paths:
        print(f"  {path}")
    print("\n" + "=" * 80)


if __name__ == '__main__':
    input_path = '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_18_fit_gap_analysis.svg'
    output_paths = [
        '/home/cuzic/ai-dev-yodoq/slides/diagrams/diagram_18_fit_gap_analysis.svg',
        '/home/cuzic/ai-dev-yodoq/slides/diagrams-web/diagram_18_fit_gap_analysis.svg'
    ]

    polish_svg(input_path, output_paths)
