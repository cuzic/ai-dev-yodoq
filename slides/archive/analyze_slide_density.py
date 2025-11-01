#!/usr/bin/env python3
"""Analyze slide content density and identify overflow risks."""

import re
from pathlib import Path

def analyze_slides(md_path):
    """Analyze all slides for content density."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by slide separators
    slides = content.split('\n---\n')

    issues = []

    for idx, slide in enumerate(slides, 1):
        # Count content indicators
        has_svg = '![' in slide and '.svg)' in slide
        lines = slide.strip().split('\n')
        non_empty_lines = [l for l in lines if l.strip() and not l.strip().startswith('<!--')]

        # Count list items
        list_items = [l for l in lines if re.match(r'^\s*[-*•]\s+', l)]

        # Count headings
        headings = [l for l in lines if l.startswith('#')]

        # Detect text overflow risks
        long_lines = [l for l in lines if len(l) > 100 and not l.startswith('#')]

        # Risk score
        risk_score = 0
        risk_factors = []

        if has_svg and len(non_empty_lines) > 20:
            risk_score += 3
            risk_factors.append(f"SVG + {len(non_empty_lines)} lines")

        if len(list_items) > 15:
            risk_score += 2
            risk_factors.append(f"{len(list_items)} list items")

        if len(long_lines) > 5:
            risk_score += 2
            risk_factors.append(f"{len(long_lines)} long lines (>100 chars)")

        if len(headings) > 4:
            risk_score += 1
            risk_factors.append(f"{len(headings)} headings")

        if risk_score >= 3:
            # Extract title
            title = "Untitled"
            for line in lines:
                if line.startswith('# '):
                    title = line.replace('# ', '').strip()
                    break

            issues.append({
                'slide': idx,
                'title': title,
                'risk_score': risk_score,
                'factors': risk_factors,
                'has_svg': has_svg,
                'total_lines': len(non_empty_lines),
                'list_items': len(list_items)
            })

    return issues

def main():
    """Main analysis."""
    md_path = Path(__file__).parent / 'all_slides.md'

    if not md_path.exists():
        print(f"❌ {md_path} not found")
        return

    print("=" * 80)
    print("SLIDE CONTENT DENSITY ANALYSIS")
    print("=" * 80)

    issues = analyze_slides(md_path)

    if not issues:
        print("\n✅ All slides have reasonable content density!")
        return

    # Sort by risk score
    issues.sort(key=lambda x: x['risk_score'], reverse=True)

    print(f"\n⚠️  Found {len(issues)} slides with overflow risk:\n")

    for issue in issues:
        print(f"📍 Slide {issue['slide']}: {issue['title']}")
        print(f"   Risk Score: {issue['risk_score']}/10")
        print(f"   Factors: {', '.join(issue['factors'])}")
        print(f"   SVG: {'Yes' if issue['has_svg'] else 'No'} | Lines: {issue['total_lines']} | Lists: {issue['list_items']}")
        print()

    print("=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print()
    print("For high-risk slides:")
    print("1. Remove SVG if text content is comprehensive")
    print("2. Split into multiple slides")
    print("3. Use 2-column or 3-column layout")
    print("4. Reduce list items per slide (max 10-12)")
    print("5. Use `::: note` collapse boxes for optional details")

if __name__ == '__main__':
    main()
