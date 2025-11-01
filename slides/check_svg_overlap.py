#!/usr/bin/env python3
"""
Check SVG files for text overlap issues.
Detects when text elements are too close to each other vertically.
"""

import re
from pathlib import Path
import xml.etree.ElementTree as ET

def analyze_svg_overlap(svg_path):
    """Analyze a single SVG file for text overlaps."""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Extract namespaces
        ns = {'svg': 'http://www.w3.org/2000/svg'}

        # Find all text elements
        text_elements = root.findall('.//svg:text', ns) + root.findall('.//text')

        if not text_elements:
            return None

        # Extract text positions and sizes
        text_info = []
        for text_elem in text_elements:
            x = text_elem.get('x')
            y = text_elem.get('y')

            if not x or not y:
                continue

            x = float(x)
            y = float(y)

            # Get font size
            font_size = 16  # default

            # Check style attribute
            style = text_elem.get('style', '')
            font_size_match = re.search(r'font-size:\s*(\d+(?:\.\d+)?)', style)
            if font_size_match:
                font_size = float(font_size_match.group(1))
            else:
                # Check direct font-size attribute
                fs = text_elem.get('font-size')
                if fs:
                    font_size_num = re.search(r'(\d+(?:\.\d+)?)', fs)
                    if font_size_num:
                        font_size = float(font_size_num.group(1))

            # Get text content
            text_content = ''.join(text_elem.itertext()).strip()

            # Get class for context
            elem_class = text_elem.get('class', '')

            text_info.append({
                'x': x,
                'y': y,
                'font_size': font_size,
                'text': text_content[:50],
                'class': elem_class
            })

        # Sort by y position
        text_info.sort(key=lambda t: (t['x'], t['y']))

        # Check for overlaps
        overlaps = []

        for i in range(len(text_info) - 1):
            curr = text_info[i]
            next_elem = text_info[i + 1]

            # Check if they are in similar x position (within 100px)
            x_diff = abs(curr['x'] - next_elem['x'])
            if x_diff > 100:
                continue

            # Check vertical distance
            y_diff = next_elem['y'] - curr['y']

            # Minimum safe distance is font_size * 1.2 (with some line-height)
            min_distance = max(curr['font_size'], next_elem['font_size']) * 1.2

            if 0 < y_diff < min_distance:
                overlap_severity = 1 - (y_diff / min_distance)  # 0-1, higher is worse
                overlaps.append({
                    'text1': curr['text'],
                    'text2': next_elem['text'],
                    'y1': curr['y'],
                    'y2': next_elem['y'],
                    'gap': y_diff,
                    'min_gap': min_distance,
                    'severity': overlap_severity,
                    'font_size1': curr['font_size'],
                    'font_size2': next_elem['font_size']
                })

        if overlaps:
            return {
                'total_texts': len(text_info),
                'overlaps': overlaps,
                'overlap_count': len(overlaps)
            }

        return None

    except Exception as e:
        print(f"Error analyzing {svg_path.name}: {e}")
        return None

def evaluate_overlap_severity(overlap_info):
    """Evaluate overlap severity and return a score (0-100)."""
    if not overlap_info:
        return 100

    overlaps = overlap_info['overlaps']

    # Calculate average severity
    avg_severity = sum(o['severity'] for o in overlaps) / len(overlaps)

    # Score calculation:
    # - No overlap: 100
    # - Minor overlap (severity < 0.3): 70-90
    # - Moderate overlap (severity 0.3-0.6): 40-70
    # - Severe overlap (severity > 0.6): 0-40

    if avg_severity < 0.1:
        return 100
    elif avg_severity < 0.3:
        return int(90 - avg_severity * 100)
    elif avg_severity < 0.6:
        return int(70 - (avg_severity - 0.3) * 100)
    else:
        return int(max(0, 40 - (avg_severity - 0.6) * 100))

def main():
    diagrams_web = Path(__file__).parent / '../diagrams-web'
    diagrams = Path(__file__).parent / 'diagrams'

    all_results = []

    for diagrams_dir in [diagrams_web, diagrams]:
        if not diagrams_dir.exists():
            continue

        svg_files = sorted(diagrams_dir.glob('*.svg'))

        for svg_file in svg_files:
            overlap_info = analyze_svg_overlap(svg_file)
            if overlap_info:
                score = evaluate_overlap_severity(overlap_info)
                all_results.append({
                    'file': svg_file.name,
                    'dir': diagrams_dir.name,
                    'info': overlap_info,
                    'score': score
                })

    print("=" * 80)
    print("SVG TEXT OVERLAP ANALYSIS")
    print("=" * 80)
    print()

    if not all_results:
        print("✅ No text overlaps detected in any SVG files!")
        return

    print(f"⚠️  Found {len(all_results)} SVG files with text overlap issues")
    print()

    # Sort by severity (lowest score first)
    all_results.sort(key=lambda x: x['score'])

    for result in all_results:
        info = result['info']
        print(f"📄 {result['dir']}/{result['file']}")
        print(f"   Overlap Score: {result['score']}/100")
        print(f"   Total text elements: {info['total_texts']}")
        print(f"   Overlapping pairs: {info['overlap_count']}")
        print()

        # Show worst overlaps
        worst_overlaps = sorted(info['overlaps'], key=lambda x: x['severity'], reverse=True)[:3]
        for overlap in worst_overlaps:
            print(f"   ⚠️  Overlap detected:")
            print(f"      Line 1 (y={overlap['y1']:.1f}, {overlap['font_size1']:.0f}px): \"{overlap['text1']}\"")
            print(f"      Line 2 (y={overlap['y2']:.1f}, {overlap['font_size2']:.0f}px): \"{overlap['text2']}\"")
            print(f"      Gap: {overlap['gap']:.1f}px (min recommended: {overlap['min_gap']:.1f}px)")
            print(f"      Severity: {overlap['severity']*100:.1f}%")
            print()

    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()
    print("For overlapping text:")
    print("1. Increase y-coordinate spacing between text elements")
    print("2. Reduce font size if appropriate")
    print("3. Reposition text elements to avoid crowding")
    print("4. Recommended minimum gap: font_size × 1.2")
    print()

if __name__ == '__main__':
    main()
