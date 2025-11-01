#!/usr/bin/env python3
"""
Analyze SVG files for text readability.
Checks font sizes and provides recommendations.
"""

import re
from pathlib import Path
import xml.etree.ElementTree as ET

def analyze_svg_file(svg_path):
    """Analyze a single SVG file for text sizes."""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # Extract namespaces
        ns = {'svg': 'http://www.w3.org/2000/svg'}

        # Find all text elements
        text_elements = root.findall('.//svg:text', ns) + root.findall('.//text')

        if not text_elements:
            return None

        font_sizes = []

        for text_elem in text_elements:
            # Check font-size in style attribute
            style = text_elem.get('style', '')
            font_size_match = re.search(r'font-size:\s*(\d+(?:\.\d+)?)', style)

            if font_size_match:
                font_sizes.append(float(font_size_match.group(1)))
            else:
                # Check direct font-size attribute
                font_size = text_elem.get('font-size')
                if font_size:
                    # Remove 'px' or other units
                    font_size_num = re.search(r'(\d+(?:\.\d+)?)', font_size)
                    if font_size_num:
                        font_sizes.append(float(font_size_num.group(1)))

        if not font_sizes:
            return None

        return {
            'min': min(font_sizes),
            'max': max(font_sizes),
            'avg': sum(font_sizes) / len(font_sizes),
            'count': len(font_sizes),
            'sizes': font_sizes
        }

    except Exception as e:
        print(f"Error analyzing {svg_path.name}: {e}")
        return None

def evaluate_svg_readability(stats):
    """Evaluate SVG text readability (0-100)."""
    if not stats:
        return 100  # No text = no problem

    min_size = stats['min']
    avg_size = stats['avg']

    # Thresholds for SVG text (SVG coordinates are different from CSS pixels)
    # For 1280x720 slides:
    # - Minimum readable: 16px
    # - Optimal minimum: 18px
    # - Optimal range: 18-28px

    MIN_READABLE = 16
    OPTIMAL_MIN = 18
    OPTIMAL_MAX = 32

    if min_size < MIN_READABLE:
        # Unreadable - critical issue
        return max(0, 30 - (MIN_READABLE - min_size) * 3)
    elif min_size < OPTIMAL_MIN:
        # Too small but readable
        ratio = (min_size - MIN_READABLE) / (OPTIMAL_MIN - MIN_READABLE)
        return int(50 + ratio * 30)
    elif avg_size <= OPTIMAL_MAX:
        # Optimal range
        return 100
    else:
        # Too large (less of a problem than too small)
        return max(80, 100 - (avg_size - OPTIMAL_MAX))

def main():
    diagrams_web = Path(__file__).parent / '../diagrams-web'
    diagrams = Path(__file__).parent / 'diagrams'

    all_results = []

    for diagrams_dir in [diagrams_web, diagrams]:
        if not diagrams_dir.exists():
            continue

        svg_files = sorted(diagrams_dir.glob('*.svg'))

        for svg_file in svg_files:
            stats = analyze_svg_file(svg_file)
            if stats:
                readability_score = evaluate_svg_readability(stats)
                all_results.append({
                    'file': svg_file.name,
                    'dir': diagrams_dir.name,
                    'stats': stats,
                    'score': readability_score
                })

    if not all_results:
        print("No SVG files with text found")
        return

    print("=" * 80)
    print("SVG TEXT READABILITY ANALYSIS")
    print("=" * 80)
    print()

    # Overall statistics
    avg_score = sum(r['score'] for r in all_results) / len(all_results)
    print(f"📊 Overall Statistics")
    print(f"   Total SVG files analyzed: {len(all_results)}")
    print(f"   Average readability score: {avg_score:.1f}/100")
    print()

    # Problem files
    problem_files = [r for r in all_results if r['score'] < 80]

    if problem_files:
        print("=" * 80)
        print(f"⚠️  SVG FILES WITH READABILITY ISSUES (Score < 80)")
        print("=" * 80)
        print()

        for result in sorted(problem_files, key=lambda x: x['score']):
            stats = result['stats']
            print(f"📄 {result['dir']}/{result['file']}")
            print(f"   Score: {result['score']}/100")
            print(f"   Font sizes: min={stats['min']:.1f}px, max={stats['max']:.1f}px, avg={stats['avg']:.1f}px")
            print(f"   Text elements: {stats['count']}")

            if stats['min'] < 16:
                print(f"   ⚠️  CRITICAL: Minimum font size too small ({stats['min']:.1f}px < 16px)")
            elif stats['min'] < 18:
                print(f"   ⚠️  WARNING: Minimum font size below optimal ({stats['min']:.1f}px < 18px)")

            print(f"   Recommendation: Increase minimum font size to at least 18px")
            print()
    else:
        print("✅ All SVG files have good text readability!")

    # Best practices
    good_files = [r for r in all_results if r['score'] >= 90]
    if good_files:
        print()
        print("=" * 80)
        print(f"✅ BEST PRACTICE EXAMPLES (Score >= 90)")
        print("=" * 80)
        print()

        for result in sorted(good_files, key=lambda x: x['score'], reverse=True)[:5]:
            stats = result['stats']
            print(f"✅ {result['dir']}/{result['file']}")
            print(f"   Score: {result['score']}/100 | Font range: {stats['min']:.1f}-{stats['max']:.1f}px (avg: {stats['avg']:.1f}px)")
            print()

if __name__ == '__main__':
    main()
