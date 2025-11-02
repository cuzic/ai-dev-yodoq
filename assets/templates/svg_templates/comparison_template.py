#!/usr/bin/env python3
"""
Comparison slide SVG template generator.
Creates side-by-side comparisons (Before/After, Good/Bad, etc.).
"""

def generate_comparison_svg(title, left_section, right_section, viewbox="0 0 1280 720"):
    """
    Generate a comparison slide SVG.

    Args:
        title: Slide title
        left_section: Dict with {'title': str, 'items': [str]}
        right_section: Dict with {'title': str, 'items': [str]}
        viewbox: SVG viewBox dimensions

    Returns:
        SVG string
    """
    # Determine visual style based on titles
    left_color = "#d32f2f"  # Red for negative/before
    right_color = "#388e3c"  # Green for positive/after

    # Check if titles contain positive/negative indicators
    left_title_lower = left_section['title'].lower()
    right_title_lower = right_section['title'].lower()

    if any(word in left_title_lower for word in ['良い', 'good', '✅', '推奨', 'after', '改善後']):
        left_color, right_color = right_color, left_color

    # Start SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      text {{ font-family: 'Noto Sans JP', sans-serif; fill: #1a1a1a; }}
      .title {{ font-size: 32px; font-weight: 700; }}
      .section-title {{ font-size: 24px; font-weight: 700; }}
      .item-text {{ font-size: 17px; }}
      .left-section {{ fill: {left_color}; }}
      .right-section {{ fill: {right_color}; }}
      .section-box {{ fill-opacity: 0.1; stroke-width: 3; }}
    </style>
  </defs>

  <!-- Title -->
  <text x="640" y="45" class="title" text-anchor="middle">{title}</text>

  <!-- Divider -->
  <line x1="640" y1="80" x2="640" y2="720" stroke="#cccccc" stroke-width="2" stroke-dasharray="8,4"/>

  <!-- Left Section -->
  <g transform="translate(40, 100)">
    <rect x="0" y="0" width="550" height="580" class="section-box left-section" stroke="{left_color}"/>
    <text x="275" y="35" class="section-title left-section" text-anchor="middle">{left_section['title']}</text>
'''

    # Left items
    item_y = 80
    for item in left_section['items']:
        svg += f'    <text x="20" y="{item_y}" class="item-text">• {item}</text>\n'
        item_y += 30

    svg += '  </g>\n\n'

    # Right Section
    svg += f'''  <!-- Right Section -->
  <g transform="translate(690, 100)">
    <rect x="0" y="0" width="550" height="580" class="section-box right-section" stroke="{right_color}"/>
    <text x="275" y="35" class="section-title right-section" text-anchor="middle">{right_section['title']}</text>
'''

    # Right items
    item_y = 80
    for item in right_section['items']:
        svg += f'    <text x="20" y="{item_y}" class="item-text">• {item}</text>\n'
        item_y += 30

    svg += '  </g>\n'
    svg += '</svg>\n'
    return svg


def generate_from_markdown(md_text):
    """
    Parse markdown and generate comparison SVG.

    Expected format:
    # Title

    **Before:** or **❌ 悪い例** or similar
    - Item 1
    - Item 2

    **After:** or **✅ 良い例** or similar
    - Item 3
    - Item 4
    """
    import re

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else "Comparison"

    # Extract sections (looking for **Label:** patterns)
    sections = []
    current_section = None

    for line in md_text.split('\n'):
        # Check for section header
        section_match = re.match(r'\*\*(.+?)[:：]?\*\*', line.strip())
        if section_match:
            if current_section and current_section['items']:
                sections.append(current_section)
            current_section = {
                'title': section_match.group(1).strip(),
                'items': []
            }
            continue

        # Check for list item
        item_match = re.match(r'[-*+]\s+(.+)', line.strip())
        if item_match and current_section:
            current_section['items'].append(item_match.group(1).strip())

    # Add last section
    if current_section and current_section['items']:
        sections.append(current_section)

    # Generate SVG with first two sections
    if len(sections) >= 2:
        return generate_comparison_svg(title, sections[0], sections[1])
    else:
        raise ValueError("Need at least 2 sections for comparison")


if __name__ == '__main__':
    # Test
    test_md = '''# AIプロンプト比較

**❌ 悪い例:**
- 曖昧な指示
- コンテキスト不足
- 期待値が不明確
- エラー処理なし

**✅ 良い例:**
- 具体的な要件定義
- 十分なコンテキスト
- 明確な成功基準
- エッジケース考慮
'''

    svg = generate_from_markdown(test_md)
    print(svg)
