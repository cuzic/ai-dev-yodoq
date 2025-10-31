#!/usr/bin/env python3
"""
Batch regenerate all SVGs for web display.
Uses simplified templates for common patterns.
"""

from pathlib import Path

# Simple SVG templates for quick generation
TEMPLATES = {
    "simple_box": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">
  <defs>
    <style>
      .title {{ font-family: 'Noto Sans JP', sans-serif; font-size: 24px; font-weight: bold; fill: #333; text-anchor: middle; }}
      .box {{ fill: #00146E; }}
      .box-text {{ font-family: 'Noto Sans JP', sans-serif; font-size: 16px; fill: white; text-anchor: middle; }}
      .note {{ font-family: 'Noto Sans JP', sans-serif; font-size: 14px; fill: #666; }}
    </style>
  </defs>
  <rect width="{width}" height="{height}" fill="#FFFFFF"/>
  {content}
</svg>""",
}

# Diagram specifications - to be filled in as we regenerate
DIAGRAMS = {
    "diagram_04_ai_memory.svg": {
        "viewBox": "800x400",
        "pattern": "matrix",
        "description": "AI memory constraints comparison"
    },
    "diagram_05_moscow.svg": {
        "viewBox": "600x400",
        "pattern": "priority",
        "description": "MoSCoW prioritization"
    },
    # Add more as we go...
}

def generate_simple_3box(title, boxes):
    """Generate 3-box horizontal layout."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300">
  <defs>
    <style>
      .title {{ font-family: 'Noto Sans JP', sans-serif; font-size: 24px; font-weight: bold; fill: #333; text-anchor: middle; }}
      .box {{ fill: #00146E; }}
      .box-text {{ font-family: 'Noto Sans JP', sans-serif; font-size: 16px; fill: white; text-anchor: middle; }}
    </style>
  </defs>
  <rect width="800" height="300" fill="#FFFFFF"/>
  <text x="400" y="40" class="title">{title}</text>
'''

    x_positions = [50, 300, 550]
    for i, (box_title, box_content) in enumerate(boxes):
        x = x_positions[i]
        svg += f'''
  <rect x="{x}" y="80" width="200" height="150" rx="8" class="box"/>
  <text x="{x+100}" y="115" class="box-text" font-weight="bold">{box_title}</text>
  <text x="{x+100}" y="145" class="box-text" font-size="14">{box_content}</text>
'''

    svg += '</svg>'
    return svg

# Generate remaining diagrams
def main():
    output_dir = Path(__file__).parent.parent / 'diagrams-web'
    output_dir.mkdir(exist_ok=True)

    print("Batch SVG Generation")
    print("=" * 60)
    print()
    print("Generated so far:")
    print("  ✓ diagram_01_ai_principles.svg")
    print("  ✓ diagram_02_role_change.svg")
    print("  ✓ diagram_03_5step_flow.svg")
    print()
    print("Remaining: 41 diagrams")
    print()
    print("This script provides templates for quick generation.")
    print("Customize the DIAGRAMS dict and run specific generators.")
    print()
    print("Next diagrams to generate:")
    for name, spec in list(DIAGRAMS.items())[:10]:
        print(f"  - {name}: {spec['description']}")

if __name__ == "__main__":
    main()
