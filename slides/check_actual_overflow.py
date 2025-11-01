#!/usr/bin/env python3
"""
Check for actual vertical overflow in rendered slides by analyzing HTML structure.
This checks if content exceeds the slide viewport height.
"""

import re
from pathlib import Path
from collections import defaultdict

def analyze_slide_structure(html_path):
    """Analyze HTML structure to detect potential overflow."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into slides - capture section element with its attributes
    slide_pattern = r'<section([^>]*?)>(.*?)</section>'
    slides = re.findall(slide_pattern, content, re.DOTALL)

    overflow_candidates = []

    for section_attrs, slide_content in slides:
        # Extract page number
        page_match = re.search(r'data-marpit-pagination="(\d+)"', section_attrs)
        if not page_match:
            continue
        page_num = page_match.group(1)

        # Extract slide title
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', slide_content, re.DOTALL)
        title = ""
        if title_match:
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()

        # Check class attribute on the section element itself
        section_class_match = re.search(r'class="([^"]*)"', section_attrs)
        classes = section_class_match.group(1) if section_class_match else ""

        # Count content elements
        h2_count = len(re.findall(r'<h2[^>]*>', slide_content))
        h3_count = len(re.findall(r'<h3[^>]*>', slide_content))
        h4_count = len(re.findall(r'<h4[^>]*>', slide_content))
        p_count = len(re.findall(r'<p[^>]*>', slide_content))
        li_count = len(re.findall(r'<li[^>]*>', slide_content))
        pre_count = len(re.findall(r'<pre[^>]*>', slide_content))
        img_count = len(re.findall(r'<img[^>]*>', slide_content))

        # Extract all list items
        list_items = re.findall(r'<li[^>]*>(.*?)</li>', slide_content, re.DOTALL)
        list_item_texts = []
        for item in list_items:
            clean = re.sub(r'<[^>]+>', '', item).strip()
            if clean:
                list_item_texts.append(clean)

        # Heuristic: Check if slide has too much content
        # Standard slide height is ~720px (Marp default)
        # Each element roughly takes:
        # - h1: 80-100px
        # - h2: 60-80px
        # - h3: 50-60px
        # - h4: 40-50px
        # - p: 30-40px per line
        # - li: 30-40px per item
        # - pre: 20px per line
        # - img: varies

        estimated_height = 0
        estimated_height += 100  # h1 title
        estimated_height += h2_count * 70
        estimated_height += h3_count * 55
        estimated_height += h4_count * 45
        estimated_height += p_count * 35
        estimated_height += li_count * 35
        estimated_height += pre_count * 100  # Average code block
        estimated_height += img_count * 300  # Average image

        # Check for two-column or three-column layouts
        is_multi_column = any(x in classes for x in ['two-column', 'three-column', 'card-grid'])
        is_diagram_only = 'layout-diagram-only' in classes or 'layout-horizontal' in classes
        is_compact = 'compact' in classes

        # Adjust for layout
        if is_compact:
            estimated_height *= 0.7  # Compact reduces font sizes and spacing significantly
        if is_multi_column:
            estimated_height *= 0.5  # Content is split across columns
        elif is_diagram_only:
            estimated_height *= 0.4  # Mostly just image

        # Standard Marp slide height is 720px, with ~50px margins = 670px usable
        max_height = 670

        risk_level = "OK"
        if estimated_height > max_height * 1.3:
            risk_level = "HIGH"
        elif estimated_height > max_height * 1.1:
            risk_level = "MEDIUM"
        elif estimated_height > max_height:
            risk_level = "LOW"

        if risk_level != "OK":
            overflow_candidates.append({
                'page': int(page_num),
                'title': title[:60],
                'risk': risk_level,
                'estimated_height': int(estimated_height),
                'max_height': max_height,
                'overflow': int(estimated_height - max_height),
                'h2': h2_count,
                'h3': h3_count,
                'h4': h4_count,
                'p': p_count,
                'li': li_count,
                'list_items': list_item_texts[:10],  # First 10 items
                'classes': classes,
                'is_multi_column': is_multi_column,
                'is_diagram_only': is_diagram_only
            })

    return overflow_candidates

def main():
    print("=" * 80)
    print("CHECKING SLIDES FOR VERTICAL OVERFLOW")
    print("=" * 80)
    print()

    html_path = Path(__file__).parent / 'index.html'
    if not html_path.exists():
        # Try all_slides.html
        html_path = Path(__file__).parent / 'all_slides.html'
        if not html_path.exists():
            print("❌ No HTML file found")
            return

    print(f"📄 Analyzing: {html_path.name}")
    print()

    candidates = analyze_slide_structure(html_path)

    if not candidates:
        print("✅ No overflow issues detected!")
        return

    # Group by risk level
    by_risk = defaultdict(list)
    for c in candidates:
        by_risk[c['risk']].append(c)

    total = len(candidates)
    high = len(by_risk['HIGH'])
    medium = len(by_risk['MEDIUM'])
    low = len(by_risk['LOW'])

    print(f"⚠️  Found {total} slides with potential overflow:")
    print(f"   🔴 HIGH risk: {high}")
    print(f"   🟡 MEDIUM risk: {medium}")
    print(f"   🟢 LOW risk: {low}")
    print()

    # Show HIGH risk slides first
    for risk in ['HIGH', 'MEDIUM', 'LOW']:
        if risk not in by_risk:
            continue

        print("=" * 80)
        print(f"{risk} RISK SLIDES")
        print("=" * 80)
        print()

        for slide in sorted(by_risk[risk], key=lambda x: x['overflow'], reverse=True):
            print(f"📍 Slide {slide['page']}: {slide['title']}")
            print(f"   Estimated height: {slide['estimated_height']}px (max: {slide['max_height']}px)")
            print(f"   Overflow: {slide['overflow']}px")
            print(f"   Content: {slide['h2']} h2, {slide['h3']} h3, {slide['h4']} h4, "
                  f"{slide['p']} paragraphs, {slide['li']} list items")

            if slide['is_multi_column']:
                print(f"   Layout: Multi-column")
            elif slide['is_diagram_only']:
                print(f"   Layout: Diagram-only")
            else:
                print(f"   Layout: Single column (HIGH RISK)")

            if slide['list_items']:
                print(f"   List items sample:")
                for i, item in enumerate(slide['list_items'][:5], 1):
                    print(f"      {i}. {item[:70]}{'...' if len(item) > 70 else ''}")

            print()

    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()
    print("For HIGH/MEDIUM risk slides:")
    print("1. Add layout class: <!-- _class: two-column --> or <!-- _class: layout-diagram-only -->")
    print("2. Split into multiple slides")
    print("3. Replace with SVG diagram")
    print("4. Reduce font sizes (last resort)")
    print()

if __name__ == '__main__':
    main()
