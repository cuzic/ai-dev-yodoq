#!/usr/bin/env python3
"""
Summary slide SVG template generator.
Converts markdown lists into 2-3 column SVG layouts.
"""

def generate_summary_svg(title, sections, viewbox="0 0 1280 720"):
    """
    Generate a summary slide SVG.

    Args:
        title: Slide title
        sections: List of dicts with {'title': str, 'items': [str]}
        viewbox: SVG viewBox dimensions

    Returns:
        SVG string
    """
    # Calculate layout
    num_sections = len(sections)
    total_items = sum(len(s['items']) for s in sections)

    # Determine column layout
    if total_items >= 25 or num_sections >= 5:
        num_columns = 3
        col_width = 380
        col_spacing = 70
    elif total_items >= 12 or num_sections >= 3:
        num_columns = 2
        col_width = 580
        col_spacing = 80
    else:
        num_columns = 1
        col_width = 1200
        col_spacing = 0

    # Start SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      text {{ font-family: 'Noto Sans JP', sans-serif; fill: #1a1a1a; }}
      .title {{ font-size: 32px; font-weight: 700; }}
      .section-title {{ font-size: 22px; font-weight: 700; fill: #1976d2; }}
      .item-text {{ font-size: 16px; }}
      .section-box {{ fill: #e3f2fd; stroke: #1976d2; stroke-width: 2; rx: 6; }}
    </style>
  </defs>

  <!-- Title -->
  <text x="640" y="45" class="title" text-anchor="middle">{title}</text>
'''

    # Distribute sections across columns
    sections_per_col = (num_sections + num_columns - 1) // num_columns

    y_offset = 90
    x_base = 40

    for col_idx in range(num_columns):
        x_pos = x_base + col_idx * (col_width + col_spacing)
        y_pos = y_offset

        start_sec = col_idx * sections_per_col
        end_sec = min((col_idx + 1) * sections_per_col, num_sections)

        for sec_idx in range(start_sec, end_sec):
            section = sections[sec_idx]

            # Section title
            svg += f'\n  <!-- Section: {section["title"]} -->\n'
            svg += f'  <g transform="translate({x_pos}, {y_pos})">\n'
            svg += f'    <text x="{col_width//2}" y="0" class="section-title" text-anchor="middle">{section["title"]}</text>\n'

            # Calculate box height
            item_height = 25
            box_height = 15 + len(section['items']) * item_height + 10

            svg += f'    <rect x="0" y="10" width="{col_width}" height="{box_height}" class="section-box"/>\n'

            # Items
            item_y = 35
            for item in section['items']:
                svg += f'    <text x="15" y="{item_y}" class="item-text">• {item}</text>\n'
                item_y += item_height

            svg += f'  </g>\n'

            y_pos += box_height + 30

    svg += '</svg>\n'
    return svg


def generate_from_markdown(md_text):
    """
    Parse markdown and generate SVG.

    Expected format:
    # Title

    ## Section 1
    - Item 1
    - Item 2

    ## Section 2
    - Item 3
    - Item 4
    """
    import re

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else "Summary"

    # Split by ## headers
    parts = re.split(r'\n##\s+', md_text)
    sections = []

    for part in parts[1:]:  # Skip first part (title area)
        lines = part.split('\n')
        section_title = lines[0].strip()

        # Extract items
        items = []
        for line in lines[1:]:
            item_match = re.match(r'[-*+]\s+(.+)', line.strip())
            if item_match:
                items.append(item_match.group(1).strip())

        if items:  # Only add if has items
            sections.append({
                'title': section_title,
                'items': items
            })

    return generate_summary_svg(title, sections)


if __name__ == '__main__':
    # Test
    test_md = '''# STEP2のまとめ

## 📋 設計の7ステップ

- Tech Stack Setup
- システムアーキテクチャ
- データベーススキーマ設計
- API仕様定義
- 受入条件詳細化
- セキュリティ設計
- docs/spec.md 作成

## 🎯 なぜこの順序か

- 大きな決定から小さな決定へ
- 手戻りを最小化
- AIが迷わない設計図

## 📊 効果

- AIが一貫性のある実装
- 手戻りなし
- セキュリティ・品質担保
'''

    svg = generate_from_markdown(test_md)
    print(svg)
