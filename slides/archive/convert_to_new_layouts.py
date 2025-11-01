#!/usr/bin/env python3
"""
Convert slides to new layouts based on content analysis.
"""

import re
from pathlib import Path

def analyze_slide_for_comparison(slide_text):
    """Check if slide should use comparison layout."""
    # Look for vs, 比較, Before/After patterns
    has_vs = bool(re.search(r'\bvs\b|比較|Before|After', slide_text, re.I))
    has_two_sections = len(re.findall(r'^###\s+', slide_text, re.MULTILINE)) == 2

    # Check for two-column with comparison content
    has_two_column = '<!-- _class: two-column -->' in slide_text

    return has_vs and (has_two_sections or has_two_column)

def analyze_slide_for_callout(slide_text):
    """Check if slide should use callout layout."""
    # Look for title with 重要
    title_match = re.search(r'^#+ (.+)$', slide_text, re.MULTILINE)
    if title_match and '重要' in title_match.group(1):
        # Check if it's not too much content
        bullets = len(re.findall(r'^\s*[-*]\s+', slide_text, re.MULTILINE))
        return bullets <= 8
    return False

def analyze_slide_for_timeline(slide_text):
    """Check if slide should use timeline layout."""
    # Look for STEP or numbered flow
    has_step = 'STEP' in slide_text or 'フロー' in slide_text
    has_arrows = slide_text.count('→') >= 3

    # Check for numbered list items (1., 2., etc.)
    numbered_items = len(re.findall(r'^\s*\d+\.\s+', slide_text, re.MULTILINE))

    return (has_step or has_arrows) and numbered_items >= 3 and numbered_items <= 7

def analyze_slide_for_code_focus(slide_text):
    """Check if slide should use code-focus layout."""
    # Count code blocks
    code_blocks = len(re.findall(r'```', slide_text))
    bullets = len(re.findall(r'^\s*[-*]\s+', slide_text, re.MULTILINE))

    # Should have at least one code block and some explanation
    return code_blocks >= 2 and bullets >= 4

def convert_to_comparison_layout(slide_text):
    """Convert slide to comparison layout format."""
    # Remove existing layout class
    slide_text = re.sub(r'<!--\s*_class:\s*[\w-]+\s*-->\n*', '', slide_text)

    # Extract title
    title_match = re.search(r'^#+ (.+)$', slide_text, re.MULTILINE)
    title = title_match.group(0) if title_match else "# Comparison"

    # Try to split content into two sections
    sections = re.split(r'^###\s+', slide_text, flags=re.MULTILINE)
    if len(sections) >= 3:  # Title + 2 sections
        # Extract the two section contents
        section1_match = re.match(r'([^\n]+)\n(.*?)(?=\n###|$)', sections[1], re.DOTALL)
        section2_match = re.match(r'([^\n]+)\n(.*?)(?=\n###|$)', sections[2], re.DOTALL)

        if section1_match and section2_match:
            s1_title = section1_match.group(1).strip()
            s1_content = section1_match.group(2).strip()
            s2_title = section2_match.group(1).strip()
            s2_content = section2_match.group(2).strip()

            new_slide = f'''<!-- _class: layout-comparison -->

{title}

<div>

### {s1_title}

{s1_content}

</div>

<div>VS</div>

<div>

### {s2_title}

{s2_content}

</div>
'''
            return new_slide

    # Fallback: keep original
    return slide_text

def convert_to_callout_layout(slide_text):
    """Convert slide to callout layout format."""
    # Remove existing layout class
    slide_text = re.sub(r'<!--\s*_class:\s*[\w-]+\s*-->\n*', '', slide_text)

    # Extract title
    title_match = re.search(r'^#+ (.+)$', slide_text, re.MULTILINE)
    title = title_match.group(1) if title_match else "Important"

    # Extract first important message or bullet points
    bullets_match = re.findall(r'^\s*[-*]\s+(.+)$', slide_text, re.MULTILINE)

    # Create icon based on content
    icon = "💡"
    if "セキュリティ" in slide_text:
        icon = "🔒"
    elif "テスト" in slide_text or "TDD" in slide_text:
        icon = "✅"
    elif "AI" in title:
        icon = "🤖"

    # Extract key message (first bold text or first bullet)
    message_match = re.search(r'\*\*([^*]+)\*\*', slide_text)
    if message_match:
        key_message = message_match.group(1)
    elif bullets_match:
        key_message = bullets_match[0]
    else:
        key_message = "重要なポイント"

    # Get remaining bullets
    bullet_list = '\n'.join(f"- {b}" for b in bullets_match[:6])

    new_slide = f'''<!-- _class: layout-callout -->

<div class="icon">{icon}</div>

# {title}

<div class="message">
{key_message}
</div>

{bullet_list}
'''
    return new_slide

def apply_conversions(md_path):
    """Apply layout conversions to slides."""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = content.split('\n---\n')
    conversions = []

    # Specific slides to convert (from analysis)
    comparison_candidates = [5, 6, 16, 19, 23, 31, 41, 49, 56, 82, 89, 90, 94]
    callout_candidates = [53, 54, 68, 70, 73, 79, 96]

    for idx, slide in enumerate(slides, 1):
        if '<style>' in slide:
            continue

        # Skip if already has a special layout
        if any(layout in slide for layout in ['lead', 'layout-horizontal', 'layout-diagram-only', 'card-grid', 'image-top-compact']):
            continue

        original_slide = slide
        changed = False

        # Convert to comparison layout
        if idx in comparison_candidates and analyze_slide_for_comparison(slide):
            slide = convert_to_comparison_layout(slide)
            if slide != original_slide:
                conversions.append(f"Slide {idx}: Converted to layout-comparison")
                slides[idx - 1] = slide
                changed = True

        # Convert to callout layout
        if not changed and idx in callout_candidates and analyze_slide_for_callout(slide):
            slide = convert_to_callout_layout(slide)
            if slide != original_slide:
                conversions.append(f"Slide {idx}: Converted to layout-callout")
                slides[idx - 1] = slide
                changed = True

    # Write back
    new_content = '\n---\n'.join(slides)

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return conversions

def main():
    md_path = Path(__file__).parent / 'all_slides.md'

    print("=" * 80)
    print("CONVERTING SLIDES TO NEW LAYOUTS")
    print("=" * 80)
    print()

    conversions = apply_conversions(md_path)

    if conversions:
        print(f"✅ Converted {len(conversions)} slides:\n")
        for conversion in conversions:
            print(f"  • {conversion}")
    else:
        print("ℹ️  No automatic conversions applied")
        print("   Manual conversion may be needed for complex slides")

    print()
    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Review converted slides visually")
    print("2. Manually adjust content structure if needed")
    print("3. Build: npx @marp-team/marp-cli@latest all_slides.md -o index.html")
    print("=" * 80)

if __name__ == '__main__':
    main()
