#!/usr/bin/env python3
"""
Checklist slide SVG template generator.
Creates clean, organized checklists with checkboxes.
"""

def generate_checklist_svg(title, groups, viewbox="0 0 1280 720"):
    """
    Generate a checklist slide SVG.

    Args:
        title: Slide title
        groups: List of dicts with {'title': str, 'items': [str]}
        viewbox: SVG viewBox dimensions

    Returns:
        SVG string
    """
    # Calculate layout
    total_items = sum(len(g['items']) for g in groups)

    # Determine columns
    if total_items >= 20:
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
      .group-title {{ font-size: 20px; font-weight: 700; fill: #388e3c; }}
      .item-text {{ font-size: 17px; }}
      .checkbox {{ fill: none; stroke: #388e3c; stroke-width: 2; }}
      .checkmark {{ fill: none; stroke: #388e3c; stroke-width: 3; }}
    </style>
  </defs>

  <!-- Title -->
  <text x="640" y="45" class="title" text-anchor="middle">{title}</text>
'''

    # Distribute groups across columns
    groups_per_col = (len(groups) + num_columns - 1) // num_columns

    y_offset = 90
    x_base = 40

    for col_idx in range(num_columns):
        x_pos = x_base + col_idx * (col_width + col_spacing)
        y_pos = y_offset

        start_group = col_idx * groups_per_col
        end_group = min((col_idx + 1) * groups_per_col, len(groups))

        for group_idx in range(start_group, end_group):
            group = groups[group_idx]

            # Group title
            svg += f'\n  <!-- Group: {group["title"]} -->\n'
            svg += f'  <g transform="translate({x_pos}, {y_pos})">\n'
            svg += f'    <text x="0" y="0" class="group-title">{group["title"]}</text>\n'

            # Items
            item_y = 30
            for item in group['items']:
                # Checkbox
                svg += f'    <rect x="0" y="{item_y - 14}" width="16" height="16" class="checkbox" rx="3"/>\n'
                # Optional checkmark (commented out - user fills in)
                # svg += f'    <path d="M 3 {item_y - 6} L 7 {item_y - 2} L 13 {item_y - 12}" class="checkmark"/>\n'

                # Item text
                svg += f'    <text x="25" y="{item_y}" class="item-text">{item}</text>\n'
                item_y += 28

            svg += f'  </g>\n'

            y_pos += 30 + len(group['items']) * 28 + 20

    svg += '</svg>\n'
    return svg


def generate_from_markdown(md_text):
    """
    Parse markdown and generate checklist SVG.

    Expected format:
    # Title

    **Group 1:**
    - [ ] Item 1
    - [ ] Item 2

    **Group 2:**
    - [ ] Item 3
    """
    import re

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else "Checklist"

    # Extract groups
    groups = []
    current_group = None

    for line in md_text.split('\n'):
        # Check for group title
        group_match = re.match(r'\*\*(.+?)[:：]?\*\*', line.strip())
        if group_match:
            if current_group and current_group['items']:
                groups.append(current_group)
            current_group = {
                'title': group_match.group(1).strip(),
                'items': []
            }
            continue

        # Check for list item
        item_match = re.match(r'[-*+]\s+\[.\]\s+(.+)', line.strip())
        if not item_match:
            item_match = re.match(r'[-*+]\s+(.+)', line.strip())

        if item_match and current_group:
            current_group['items'].append(item_match.group(1).strip())

    # Add last group
    if current_group and current_group['items']:
        groups.append(current_group)

    return generate_checklist_svg(title, groups)


if __name__ == '__main__':
    # Test
    test_md = '''# 演習成功のチェックリスト

**STEP1-2: 要件定義・設計**
- [ ] AIに質問させて曖昧さ排除
- [ ] ユーザーストーリー作成
- [ ] エラー・エッジケース洗い出し
- [ ] 受け入れ基準（Given-When-Then）
- [ ] Tech Stack Setup決定

**STEP3: タスク分解**
- [ ] タスク一覧をAI生成
- [ ] Phase分け確認
- [ ] タスク粒度調整（30分〜2時間）
- [ ] 依存関係可視化

**STEP4: 実装**
- [ ] TDD/BDD実装
- [ ] Given-When-Then形式テスト
- [ ] インクリメンタル開発
- [ ] 環境変数で秘密情報管理
'''

    svg = generate_from_markdown(test_md)
    print(svg)
