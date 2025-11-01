#!/usr/bin/env python3
"""
Analyze optimal SVG aspect ratios for each layout type.
Calculate based on available space and readability.
"""

import re
from pathlib import Path
from collections import defaultdict

def get_layout_specs():
    """Define layout specifications and available space."""
    return {
        'default': {
            'slide_width': 1280,
            'slide_height': 720,
            'padding': 100,  # 50px each side
            'title_height': 60,
            'content_area_width': 1180,
            'content_area_height': 620,
            'image_max_width_percent': 70,
            'image_max_height_vh': 45,
        },
        'layout-horizontal-left': {
            'slide_width': 1280,
            'slide_height': 720,
            'padding': 100,
            'title_height': 60,
            'image_column_width': 704,  # 55% of 1280
            'image_column_height': 620,
            'image_max_width_percent': 90,
            'image_max_height_vh': 55,
        },
        'layout-horizontal-right': {
            'slide_width': 1280,
            'slide_height': 720,
            'padding': 100,
            'title_height': 60,
            'image_column_width': 704,  # 55% of 1280
            'image_column_height': 620,
            'image_max_width_percent': 90,
            'image_max_height_vh': 55,
        },
        'layout-diagram-only': {
            'slide_width': 1280,
            'slide_height': 720,
            'padding': 100,
            'title_height': 60,
            'content_area_width': 1180,
            'content_area_height': 620,
            'image_max_width_percent': 75,
            'image_max_height_vh': 60,
        },
    }

def calculate_optimal_aspect_ratio(layout_name, specs):
    """Calculate optimal aspect ratio for a layout."""
    if layout_name == 'default':
        # For default layout
        max_width = specs['content_area_width'] * (specs['image_max_width_percent'] / 100)
        max_height = specs['slide_height'] * (specs['image_max_height_vh'] / 100)

    elif layout_name in ['layout-horizontal-left', 'layout-horizontal-right']:
        # For horizontal layouts
        max_width = specs['image_column_width'] * (specs['image_max_width_percent'] / 100)
        max_height = specs['slide_height'] * (specs['image_max_height_vh'] / 100)

    elif layout_name == 'layout-diagram-only':
        # For diagram-only layout
        max_width = specs['content_area_width'] * (specs['image_max_width_percent'] / 100)
        max_height = specs['slide_height'] * (specs['image_max_height_vh'] / 100)

    else:
        return None

    aspect_ratio = max_width / max_height

    return {
        'max_width': max_width,
        'max_height': max_height,
        'aspect_ratio': aspect_ratio,
        'recommended_width': int(max_width),
        'recommended_height': int(max_height),
    }

def analyze_current_svgs(md_path):
    """Analyze current SVG usage in slides."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = content.split('\n---\n')
    svg_usage = defaultdict(list)

    for idx, slide in enumerate(slides, 1):
        # Skip style blocks
        if '<style>' in slide:
            continue

        # Get layout
        layout_match = re.search(r'<!--\s*_class:\s*([\w-]+)\s*-->', slide)
        layout = layout_match.group(1) if layout_match else 'default'

        # Find SVG references
        svg_matches = re.findall(r'!\[([^\]]*)\]\(([^)]+\.svg)\)', slide)

        for alt_text, svg_path in svg_matches:
            svg_usage[layout].append({
                'slide': idx,
                'alt_text': alt_text,
                'path': svg_path,
            })

    return svg_usage

def get_svg_actual_size(svg_path):
    """Try to get actual SVG dimensions from file."""
    try:
        full_path = Path(__file__).parent / svg_path
        if full_path.exists():
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read(500)  # Read first 500 chars

            # Look for width/height attributes
            width_match = re.search(r'width="(\d+)"', content)
            height_match = re.search(r'height="(\d+)"', content)

            if width_match and height_match:
                width = int(width_match.group(1))
                height = int(height_match.group(1))
                return width, height, width / height

            # Look for viewBox
            viewbox_match = re.search(r'viewBox="[\d\s]+\s+([\d.]+)\s+([\d.]+)"', content)
            if viewbox_match:
                width = float(viewbox_match.group(1))
                height = float(viewbox_match.group(2))
                return width, height, width / height

    except Exception as e:
        pass

    return None, None, None

def main():
    md_path = Path(__file__).parent / 'all_slides.md'

    print("=" * 80)
    print("SVG ASPECT RATIO ANALYSIS")
    print("=" * 80)
    print()

    # Get layout specifications
    layout_specs = get_layout_specs()

    print("📐 OPTIMAL ASPECT RATIOS BY LAYOUT")
    print("-" * 80)
    print()

    optimal_ratios = {}

    for layout_name, specs in layout_specs.items():
        result = calculate_optimal_aspect_ratio(layout_name, specs)
        if result:
            optimal_ratios[layout_name] = result

            print(f"### {layout_name}")
            print(f"  Available space: {result['max_width']:.0f}px × {result['max_height']:.0f}px")
            print(f"  Optimal aspect ratio: {result['aspect_ratio']:.2f}:1")
            print(f"  Recommended SVG size: {result['recommended_width']}×{result['recommended_height']}")

            # Calculate common aspect ratios
            ratio = result['aspect_ratio']
            if 1.5 <= ratio <= 1.8:
                print(f"  → Close to 16:9 (1.78:1) - GOOD for widescreen diagrams")
            elif 1.3 <= ratio <= 1.5:
                print(f"  → Close to 4:3 (1.33:1) - GOOD for traditional diagrams")
            elif 2.0 <= ratio <= 2.5:
                print(f"  → Wide format (2:1 - 2.5:1) - GOOD for flowcharts")
            elif ratio < 1.0:
                print(f"  → Portrait format - Use for vertical flows")
            else:
                print(f"  → Ultra-wide format - Use sparingly")

            print()

    # Analyze current SVG usage
    print("\n" + "=" * 80)
    print("📊 CURRENT SVG USAGE ANALYSIS")
    print("=" * 80)
    print()

    svg_usage = analyze_current_svgs(md_path)

    for layout, svgs in sorted(svg_usage.items()):
        if layout not in optimal_ratios:
            continue

        print(f"\n### {layout} ({len(svgs)} SVGs)")
        print("-" * 80)

        optimal = optimal_ratios[layout]
        optimal_ratio = optimal['aspect_ratio']

        # Sample first 5 SVGs
        for svg_info in svgs[:5]:
            width, height, ratio = get_svg_actual_size(svg_info['path'])

            print(f"  Slide {svg_info['slide']}: {svg_info['alt_text']}")
            print(f"    Path: {svg_info['path']}")

            if ratio:
                print(f"    Current size: {width:.0f}×{height:.0f} (ratio: {ratio:.2f}:1)")

                # Compare with optimal
                ratio_diff = abs(ratio - optimal_ratio)
                if ratio_diff < 0.2:
                    print(f"    ✅ GOOD: Ratio matches optimal ({optimal_ratio:.2f}:1)")
                elif ratio_diff < 0.5:
                    print(f"    ⚠️  ACCEPTABLE: Close to optimal ({optimal_ratio:.2f}:1)")
                else:
                    print(f"    ❌ SUBOPTIMAL: Should be closer to {optimal_ratio:.2f}:1")

                    # Calculate recommended size
                    if ratio > optimal_ratio:
                        # Too wide, reduce width
                        new_width = height * optimal_ratio
                        print(f"    💡 Recommend: {new_width:.0f}×{height:.0f}")
                    else:
                        # Too tall, reduce height
                        new_height = width / optimal_ratio
                        print(f"    💡 Recommend: {width:.0f}×{new_height:.0f}")
            else:
                print(f"    ⚠️  Could not read SVG dimensions")

            print()

        if len(svgs) > 5:
            print(f"  ... and {len(svgs) - 5} more SVGs")
            print()

    print("\n" + "=" * 80)
    print("📋 SUMMARY RECOMMENDATIONS")
    print("=" * 80)
    print()

    print("## Optimal Aspect Ratios by Layout Type")
    print()
    print("| Layout | Optimal Ratio | Width×Height | Best For |")
    print("|--------|--------------|--------------|----------|")

    recommendations = {
        'default': ('1.43:1', '826×578', 'General diagrams, charts'),
        'layout-horizontal-left': ('1.10:1', '634×396', 'Compact diagrams in 55% column'),
        'layout-horizontal-right': ('1.10:1', '634×396', 'Compact diagrams in 55% column'),
        'layout-diagram-only': ('2.05:1', '885×432', 'Wide flowcharts, timelines'),
    }

    for layout, (ratio, size, use_case) in recommendations.items():
        if layout in optimal_ratios:
            actual = optimal_ratios[layout]
            print(f"| {layout} | {actual['aspect_ratio']:.2f}:1 | {actual['recommended_width']}×{actual['recommended_height']} | {use_case} |")

    print()
    print("\n## General Guidelines")
    print()
    print("1. **Default layout**: Use ~1.4:1 (close to 4:3)")
    print("   - Good for: Architecture diagrams, entity relationships")
    print("   - Avoid: Ultra-wide flowcharts (use diagram-only instead)")
    print()
    print("2. **Horizontal layouts**: Use ~1.1:1 (nearly square)")
    print("   - Good for: Compact diagrams, state machines, small flowcharts")
    print("   - Avoid: Wide timelines (won't fit in 55% column)")
    print()
    print("3. **Diagram-only layout**: Use ~2.0:1 (wide)")
    print("   - Good for: Process flows, timelines, multi-step sequences")
    print("   - Avoid: Tall hierarchies (use portrait 0.5:1 instead)")
    print()
    print("\n## Information Density Guidelines")
    print()
    print("For maximum readability with minimal whitespace:")
    print()
    print("- **Text size in SVG**: 12-16px (readable at 1280px width)")
    print("- **Line weight**: 2-3px for primary lines, 1px for secondary")
    print("- **Padding inside SVG**: 20-30px margins")
    print("- **Element spacing**: 15-20px between components")
    print("- **Max elements per SVG**: 10-15 (more = harder to read)")
    print()
    print("💡 **Key insight**: Match your SVG aspect ratio to the layout's")
    print("   available space to minimize whitespace and maximize content.")
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
