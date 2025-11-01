#!/usr/bin/env python3
"""
Create a comprehensive fix plan for:
1. SVG aspect ratio mismatches
2. Over-reduced content  
3. Remaining overflow issues
4. Layout-content balance
"""

import re
from pathlib import Path

def analyze_all_issues(md_path):
    """Comprehensive analysis of all issues."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slides = content.split('\n---\n')
    
    issues = {
        'svg_mismatch': [],
        'over_reduced': [],
        'overflow': [],
        'layout_issues': []
    }
    
    # Check each slide
    for idx, slide in enumerate(slides, 1):
        title_match = re.search(r'^#\s+(.+)$', slide, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Slide {idx}"
        
        layout_match = re.search(r'<!--\s*_class:\s*([a-z-]+)\s*-->', slide)
        layout = layout_match.group(1) if layout_match else 'default'
        
        # Skip CSS slides
        if '<style>' in slide:
            continue
        
        # Count content
        bullets = len(re.findall(r'^\s*[-*•]\s+', slide, re.MULTILINE))
        
        # Check for SVGs with horizontal layout
        if 'horizontal' in layout:
            svgs = re.findall(r'diagrams-web/([^)]+\.svg)', slide)
            if svgs:
                issues['svg_mismatch'].append({
                    'slide': idx,
                    'title': title,
                    'layout': layout,
                    'svgs': svgs
                })
        
        # Check for empty or very sparse slides
        if bullets < 5 and 'lead' not in layout and '![' not in slide:
            issues['over_reduced'].append({
                'slide': idx,
                'title': title,
                'bullets': bullets,
                'layout': layout
            })
        
        # Check for potential overcrowding
        if layout == 'two-column' and bullets > 18:
            issues['layout_issues'].append({
                'slide': idx,
                'title': title,
                'issue': f'{bullets} bullets too many for 2-column',
                'suggestion': 'Use 3-column'
            })
        elif layout == 'three-column' and bullets > 27:
            issues['layout_issues'].append({
                'slide': idx,
                'title': title,
                'issue': f'{bullets} bullets too many for 3-column',
                'suggestion': 'Split into multiple slides'
            })
    
    return issues

def main():
    md_path = Path(__file__).parent / 'all_slides.md'
    
    print("=" * 80)
    print("COMPREHENSIVE ISSUES ANALYSIS")
    print("=" * 80)
    print()
    
    issues = analyze_all_issues(md_path)
    
    print("📍 SVG ASPECT RATIO MISMATCHES")
    print("-" * 80)
    if issues['svg_mismatch']:
        for item in issues['svg_mismatch'][:10]:
            print(f"  Slide {item['slide']}: {item['title']}")
            print(f"    Layout: {item['layout']}, SVGs: {', '.join(item['svgs'])}")
    else:
        print("  ✅ None")
    print()
    
    print("📍 OVER-REDUCED SLIDES (< 5 bullets, no images)")
    print("-" * 80)
    if issues['over_reduced']:
        for item in issues['over_reduced'][:10]:
            print(f"  Slide {item['slide']}: {item['title']} ({item['bullets']} bullets)")
    else:
        print("  ✅ None")
    print()
    
    print("📍 LAYOUT ISSUES (too much content)")
    print("-" * 80)
    if issues['layout_issues']:
        for item in issues['layout_issues'][:10]:
            print(f"  Slide {item['slide']}: {item['title']}")
            print(f"    Issue: {item['issue']}")
            print(f"    Suggestion: {item['suggestion']}")
    else:
        print("  ✅ None")
    print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"  SVG mismatches: {len(issues['svg_mismatch'])}")
    print(f"  Over-reduced slides: {len(issues['over_reduced'])}")
    print(f"  Layout issues: {len(issues['layout_issues'])}")

if __name__ == '__main__':
    main()
