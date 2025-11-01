#!/usr/bin/env python3
"""
Analyze if slide layouts match their content amount.
Recommend optimal layouts based on content density.
"""

import re
from pathlib import Path

def count_content_items(slide_text):
    """Count bullets, lines, and estimate content density."""
    lines = slide_text.split('\n')
    
    bullets = sum(1 for line in lines if re.match(r'^\s*[-*•]\s+', line))
    headings = sum(1 for line in lines if re.match(r'^#{2,4}\s+', line))
    text_lines = sum(1 for line in lines if line.strip() and not line.startswith('#') and not line.startswith('<!--'))
    images = sum(1 for line in lines if '![' in line or 'diagrams-web' in line)
    
    return {
        'bullets': bullets,
        'headings': headings,
        'text_lines': text_lines,
        'images': images,
        'total_lines': len([l for l in lines if l.strip()])
    }

def recommend_layout(content, current_layout, has_title):
    """Recommend optimal layout based on content."""
    bullets = content['bullets']
    images = content['images']
    headings = content['headings']
    
    # Skip lead slides (title slides)
    if current_layout == 'lead':
        return current_layout, None
    
    # Image-focused slides
    if images >= 1 and bullets <= 5:
        if current_layout.startswith('layout-horizontal'):
            return current_layout, None  # Keep as is
        return 'layout-horizontal-right', 'Has image + few bullets'
    
    # Heavy list content
    if bullets >= 15:
        if current_layout != 'three-column':
            return 'three-column', f'{bullets} bullets need 3 columns'
        return current_layout, None
    
    # Medium list content
    if bullets >= 8 and bullets < 15:
        if current_layout != 'two-column':
            return 'two-column', f'{bullets} bullets fit 2 columns'
        return current_layout, None
    
    # Card-style content (2-4 sections with headings)
    if headings >= 3 and bullets <= 12:
        if current_layout != 'card-grid':
            return 'card-grid', f'{headings} sections as cards'
        return current_layout, None
    
    # Light content
    if bullets <= 7 and images == 0:
        if current_layout not in ['two-column', 'default']:
            return 'two-column', 'Light content fits 2 columns'
        return current_layout, None
    
    return current_layout, None

def analyze_slides(md_path):
    """Analyze all slides and recommend layout changes."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    slides = content.split('\n---\n')
    
    recommendations = []
    
    for idx, slide in enumerate(slides, 1):
        # Extract title
        title_match = re.search(r'^#\s+(.+)$', slide, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled"
        
        # Extract layout
        layout_match = re.search(r'<!--\s*_class:\s*([a-z-]+)\s*-->', slide)
        current_layout = layout_match.group(1) if layout_match else 'default'
        
        # Skip CSS/style slides
        if '<style>' in slide or 'section.two-column' in slide:
            continue
        
        # Count content
        content_stats = count_content_items(slide)
        
        # Get recommendation
        recommended, reason = recommend_layout(content_stats, current_layout, title != "Untitled")
        
        if reason:  # Only show slides that need changes
            recommendations.append({
                'slide': idx,
                'title': title,
                'current': current_layout,
                'recommended': recommended,
                'reason': reason,
                'stats': content_stats
            })
    
    return recommendations

def main():
    md_path = Path(__file__).parent / 'all_slides.md'
    
    print("=" * 80)
    print("LAYOUT OPTIMIZATION ANALYSIS")
    print("=" * 80)
    print()
    
    recommendations = analyze_slides(md_path)
    
    if not recommendations:
        print("✅ All layouts are optimal for their content!")
        return
    
    print(f"⚠️  Found {len(recommendations)} slides that could benefit from layout changes\n")
    
    for rec in recommendations:
        print(f"📍 Slide {rec['slide']}: {rec['title']}")
        print(f"   Current: {rec['current']}")
        print(f"   Recommended: {rec['recommended']}")
        print(f"   Reason: {rec['reason']}")
        print(f"   Content: {rec['stats']['bullets']} bullets, {rec['stats']['images']} images, {rec['stats']['headings']} headings")
        print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    # Group by change type
    by_change = {}
    for rec in recommendations:
        change = f"{rec['current']} → {rec['recommended']}"
        by_change[change] = by_change.get(change, 0) + 1
    
    for change, count in sorted(by_change.items(), key=lambda x: -x[1]):
        print(f"{count:2d} slides: {change}")

if __name__ == '__main__':
    main()
