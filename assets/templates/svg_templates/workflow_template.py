#!/usr/bin/env python3
"""
Workflow slide SVG template generator.
Creates step-by-step process flows with arrows.
"""

def generate_workflow_svg(title, steps, viewbox="0 0 1280 720", orientation="horizontal"):
    """
    Generate a workflow slide SVG.

    Args:
        title: Slide title
        steps: List of dicts with {'title': str, 'description': str (optional)}
        viewbox: SVG viewBox dimensions
        orientation: 'horizontal' or 'vertical'

    Returns:
        SVG string
    """
    num_steps = len(steps)

    # Handle empty steps
    if num_steps == 0:
        raise ValueError("No steps found in workflow")

    # Start SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" preserveAspectRatio="xMidYMid meet">
  <defs>
    <style>
      text {{ font-family: 'Noto Sans JP', sans-serif; fill: #1a1a1a; }}
      .title {{ font-size: 32px; font-weight: 700; }}
      .step-number {{ font-size: 28px; font-weight: 700; fill: white; }}
      .step-title {{ font-size: 18px; font-weight: 700; fill: #1976d2; }}
      .step-desc {{ font-size: 15px; }}
      .step-circle {{ fill: #1976d2; }}
      .arrow {{ fill: none; stroke: #1976d2; stroke-width: 3; marker-end: url(#arrowhead); }}
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#1976d2"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="640" y="45" class="title" text-anchor="middle">{title}</text>
'''

    if orientation == "horizontal" and num_steps <= 4:
        # Horizontal layout
        step_width = 1200 // num_steps
        y_base = 150

        for idx, step in enumerate(steps):
            x_pos = 40 + idx * step_width + step_width // 2

            # Step circle
            svg += f'\n  <!-- Step {idx + 1} -->\n'
            svg += f'  <circle cx="{x_pos}" cy="{y_base}" r="35" class="step-circle"/>\n'
            svg += f'  <text x="{x_pos}" y="{y_base + 10}" class="step-number" text-anchor="middle">{idx + 1}</text>\n'

            # Step title
            svg += f'  <text x="{x_pos}" y="{y_base + 70}" class="step-title" text-anchor="middle">{step["title"]}</text>\n'

            # Step description (wrap text)
            if step.get('description'):
                desc_lines = wrap_text(step['description'], 20)
                desc_y = y_base + 100
                for line in desc_lines:
                    svg += f'  <text x="{x_pos}" y="{desc_y}" class="step-desc" text-anchor="middle">{line}</text>\n'
                    desc_y += 22

            # Arrow to next step
            if idx < num_steps - 1:
                next_x = x_pos + step_width
                svg += f'  <path d="M {x_pos + 40} {y_base} L {next_x - 40} {y_base}" class="arrow"/>\n'

    else:
        # Vertical layout for 5+ steps
        y_step = 550 // num_steps
        x_base = 200

        for idx, step in enumerate(steps):
            y_pos = 120 + idx * y_step

            # Step circle
            svg += f'\n  <!-- Step {idx + 1} -->\n'
            svg += f'  <circle cx="{x_base}" cy="{y_pos}" r="30" class="step-circle"/>\n'
            svg += f'  <text x="{x_base}" y="{y_pos + 8}" class="step-number" text-anchor="middle">{idx + 1}</text>\n'

            # Step title and description
            svg += f'  <text x="{x_base + 60}" y="{y_pos - 5}" class="step-title">{step["title"]}</text>\n'

            if step.get('description'):
                desc_lines = wrap_text(step['description'], 60)
                desc_y = y_pos + 20
                for line in desc_lines:
                    svg += f'  <text x="{x_base + 60}" y="{desc_y}" class="step-desc">{line}</text>\n'
                    desc_y += 20

            # Arrow to next step
            if idx < num_steps - 1:
                next_y = y_pos + y_step
                svg += f'  <path d="M {x_base} {y_pos + 35} L {x_base} {next_y - 35}" class="arrow"/>\n'

    svg += '</svg>\n'
    return svg


def wrap_text(text, max_chars):
    """Simple text wrapper"""
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= max_chars:
            current_line.append(word)
            current_length += len(word) + 1
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def generate_from_markdown(md_text):
    """
    Parse markdown and generate workflow SVG.

    Expected format:
    # Title

    ## Step 1: Title
    Description text

    ## Step 2: Title
    Description text
    """
    import re

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else "Workflow"

    # Extract steps
    steps = []
    parts = re.split(r'\n##\s+', md_text)

    for part in parts[1:]:  # Skip first part (title area)
        lines = part.split('\n')

        # Extract step title (may have "Step 1:" prefix)
        step_title = lines[0].strip()
        step_title = re.sub(r'^(?:Step\s+\d+[:：]?\s*|STEP\s*\d+[:：]?\s*)', '', step_title, flags=re.IGNORECASE)

        # Extract description
        description = ''
        for line in lines[1:]:
            line = line.strip()
            if line and not line.startswith('#'):
                description += line + ' '

        steps.append({
            'title': step_title.strip(),
            'description': description.strip()
        })

    # Determine orientation
    orientation = 'vertical' if len(steps) > 4 else 'horizontal'

    return generate_workflow_svg(title, steps, orientation=orientation)


if __name__ == '__main__':
    # Test
    test_md = '''# 5ステップ開発フロー

## STEP 1: 要件確認
AIに質問させて曖昧さを排除

## STEP 2: 設計
システムアーキテクチャとDB設計

## STEP 3: タスク分解
Phase分けと依存関係整理

## STEP 4: 実装
TDD/BDDでインクリメンタル開発

## STEP 5: テスト・レビュー
自動テストとAIレビュー
'''

    svg = generate_from_markdown(test_md)
    print(svg)
