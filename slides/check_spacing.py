#!/usr/bin/env python3
import re
from pathlib import Path

def check_text_spacing(svg_path):
    """Check for text elements that are too close together."""
    content = svg_path.read_text(encoding='utf-8')
    
    # Extract all text elements with positions
    text_pattern = r'<text[^>]*x="([^"]*)"[^>]*y="([^"]*)"[^>]*>(.*?)</text>'
    texts = re.findall(text_pattern, content)
    
    issues = []
    
    # Group by approximate Y position
    y_groups = {}
    for x, y, content_text in texts:
        try:
            x_val = float(x)
            y_val = float(y)
            
            # Find texts at similar X but different Y (vertical stacking)
            for other_y in list(y_groups.keys()):
                if abs(x_val - y_groups[other_y]['x']) < 10:  # Same X position
                    spacing = abs(y_val - other_y)
                    if spacing < 15:  # Too close (less than 15px)
                        issues.append(f"  ⚠️  Text too close at x={x_val}: y={other_y} and y={y_val} (spacing={spacing:.0f}px)")
            
            y_groups[y_val] = {'x': x_val, 'content': content_text.strip()}
        except ValueError:
            pass
    
    return issues

print("Checking text spacing in all SVGs...")
print("=" * 70)

diagrams_dir = Path('../diagrams-web')
for svg_file in sorted(diagrams_dir.glob('*.svg')):
    issues = check_text_spacing(svg_file)
    if issues:
        print(f"\n{svg_file.name}:")
        for issue in issues:
            print(issue)
    else:
        print(f"✅ {svg_file.name} - Good spacing")
