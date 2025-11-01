#!/usr/bin/env python3
"""Check if SVG aspect ratios match their slide layouts."""

import re
from pathlib import Path

def get_svg_dimensions(svg_path):
    """Extract viewBox dimensions from SVG."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    viewbox_match = re.search(r'viewBox="([^"]+)"', content)
    if viewbox_match:
        dims = viewbox_match.group(1).split()
        if len(dims) == 4:
            return int(dims[2]), int(dims[3])  # width, height
    return None, None

def analyze_svg_layout_match(md_path, svg_dir):
    """Find SVG-layout mismatches."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slides = content.split('\n---\n')
    mismatches = []
    
    for idx, slide in enumerate(slides, 1):
        # Get layout
        layout_match = re.search(r'<!--\s*_class:\s*([a-z-]+)\s*-->', slide)
        layout = layout_match.group(1) if layout_match else 'default'
        
        # Find SVG references
        svg_matches = re.findall(r'!\[[^\]]*\]\((diagrams-web/[^)]+\.svg)\)', slide)
        
        for svg_ref in svg_matches:
            svg_path = Path(__file__).parent.parent / svg_ref
            if svg_path.exists():
                width, height = get_svg_dimensions(svg_path)
                if width and height:
                    aspect = width / height
                    
                    # Determine expected aspect based on layout
                    expected_aspect = None
                    if 'horizontal' in layout:
                        expected_aspect = 1.6  # Wide aspect for horizontal layouts
                    elif layout in ['two-column', 'three-column']:
                        expected_aspect = 1.0  # Square-ish for column layouts
                    elif layout == 'diagram-only':
                        expected_aspect = 1.3  # Flexible
                    
                    if expected_aspect:
                        diff = abs(aspect - expected_aspect)
                        if diff > 0.5:  # Significant mismatch
                            mismatches.append({
                                'slide': idx,
                                'layout': layout,
                                'svg': svg_ref,
                                'aspect': aspect,
                                'expected': expected_aspect,
                                'dims': f"{width}x{height}"
                            })
    
    return mismatches

def main():
    md_path = Path(__file__).parent / 'all_slides.md'
    svg_dir = Path(__file__).parent.parent / 'diagrams-web'
    
    print("=" * 80)
    print("SVG ASPECT RATIO vs LAYOUT ANALYSIS")
    print("=" * 80)
    print()
    
    mismatches = analyze_svg_layout_match(md_path, svg_dir)
    
    if not mismatches:
        print("✅ All SVG aspect ratios match their layouts!")
        return
    
    print(f"⚠️  Found {len(mismatches)} SVG-layout mismatches\n")
    
    for m in mismatches:
        print(f"📍 Slide {m['slide']} ({m['layout']})")
        print(f"   SVG: {m['svg']}")
        print(f"   Dimensions: {m['dims']}")
        print(f"   Aspect: {m['aspect']:.2f} (expected ~{m['expected']:.2f})")
        print()

if __name__ == '__main__':
    main()
