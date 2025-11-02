#!/usr/bin/env python3
"""
Apply content optimizations based on the optimization plan.
- Apply compact classes where needed
- Condense content for slides already using compact
"""

import json
import re

def load_optimization_plan():
    """Load the optimization plan."""
    with open('slides/.logs/optimization_plan.json', 'r') as f:
        return json.load(f)

def find_and_update_slide(slide_num, action_func):
    """Find a slide and apply an update function."""
    files = ['slides/day1_1.md', 'slides/day1_2.md', 'slides/day1_3.md',
             'slides/day2_1.md', 'slides/day2_2.md']

    current_slide = 0
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        slides = content.split('\n---\n')
        modified = False

        for i, slide in enumerate(slides):
            if slide.strip().startswith('---\nmarp:'):
                continue

            current_slide += 1

            if current_slide == slide_num:
                new_slide, changed = action_func(slide)
                if changed:
                    slides[i] = new_slide
                    modified = True

                    # Write back
                    new_content = '\n---\n'.join(slides)
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    return True

    return False

def apply_compact_class(slide):
    """Add compact class to a slide."""
    # Check if already has compact
    class_match = re.search(r'<!-- _class: (.+?) -->', slide)

    if class_match:
        current_class = class_match.group(1)

        # Check if already has compact/supercompact/ultracompact
        if 'compact' in current_class:
            return slide, False  # Already has compact

        # Add compact
        new_class = current_class + ' compact'
        new_slide = re.sub(
            r'<!-- _class: .+? -->',
            f'<!-- _class: {new_class} -->',
            slide
        )
        return new_slide, True
    else:
        # Add new class declaration
        new_slide = f'<!-- _class: compact -->\n\n{slide}'
        return new_slide, True

def upgrade_to_supercompact(slide):
    """Upgrade compact to supercompact."""
    class_match = re.search(r'<!-- _class: (.+?) -->', slide)

    if class_match:
        current_class = class_match.group(1)

        # Replace compact with supercompact
        if 'compact' in current_class and 'supercompact' not in current_class:
            new_class = current_class.replace('compact', 'supercompact')
            new_slide = re.sub(
                r'<!-- _class: .+? -->',
                f'<!-- _class: {new_class} -->',
                slide
            )
            return new_slide, True

    return slide, False

def condense_list_items(slide):
    """Condense list items by removing filler words and redundancy."""
    lines = slide.split('\n')
    modified = False

    for i, line in enumerate(lines):
        if line.strip().startswith('-') or line.strip().startswith('*'):
            # Remove common filler phrases
            original = line
            line = re.sub(r'することができます$', '', line)
            line = re.sub(r'することが重要です$', '', line)
            line = re.sub(r'する必要があります$', '', line)
            line = re.sub(r'していきます$', 'する', line)
            line = re.sub(r'を行います$', '', line)
            line = re.sub(r'を実施します$', '', line)

            # Condense common patterns
            line = re.sub(r'〜することで、', '→', line)
            line = re.sub(r'について理解する', '理解', line)
            line = re.sub(r'を確認する', '確認', line)

            if line != original:
                lines[i] = line
                modified = True

    if modified:
        return '\n'.join(lines), True

    return slide, False

def main():
    """Apply optimizations based on plan."""
    print("=" * 80)
    print("APPLYING CONTENT OPTIMIZATIONS")
    print("=" * 80)
    print()

    plan = load_optimization_plan()

    # Filter to slides that need action
    high_priority = [p for p in plan if p['priority_score'] >= 100]
    medium_priority = [p for p in plan if 50 <= p['priority_score'] < 100]

    print(f"Processing {len(high_priority)} high priority slides...")
    print(f"Processing {len(medium_priority)} medium priority slides...")
    print()

    results = {
        'compact_applied': [],
        'supercompact_applied': [],
        'content_condensed': [],
        'no_change': []
    }

    # Process high priority first
    for item in high_priority:
        slide_num = item['slide']
        title = item['title'][:50]
        overflow = item['overflow_px']
        current_class = item['current_class']

        print(f"Slide {slide_num}: {title}")
        print(f"  Overflow: {overflow}px, Class: {current_class}")

        # Decide action based on current state and overflow
        if overflow > 500:
            # Very high overflow - try supercompact or condense
            if 'compact' in current_class:
                # Already has compact, upgrade to supercompact
                if find_and_update_slide(slide_num, upgrade_to_supercompact):
                    print(f"  ✓ Upgraded to supercompact")
                    results['supercompact_applied'].append(slide_num)
                else:
                    print(f"  ✗ Could not upgrade to supercompact")
            else:
                # Apply compact
                if find_and_update_slide(slide_num, apply_compact_class):
                    print(f"  ✓ Applied compact class")
                    results['compact_applied'].append(slide_num)
                else:
                    print(f"  ✗ Could not apply compact")

        elif overflow > 100:
            # Moderate overflow - apply compact
            if 'compact' not in current_class:
                if find_and_update_slide(slide_num, apply_compact_class):
                    print(f"  ✓ Applied compact class")
                    results['compact_applied'].append(slide_num)
                else:
                    print(f"  ✗ Could not apply compact")
            else:
                # Try condensing content
                if find_and_update_slide(slide_num, condense_list_items):
                    print(f"  ✓ Condensed content")
                    results['content_condensed'].append(slide_num)
                else:
                    print(f"  ~ No automatic condensing available")
                    results['no_change'].append(slide_num)
        else:
            # Minor overflow - try compact
            if 'compact' not in current_class:
                if find_and_update_slide(slide_num, apply_compact_class):
                    print(f"  ✓ Applied compact class")
                    results['compact_applied'].append(slide_num)
                else:
                    print(f"  ✗ Could not apply compact")

        print()

    # Process medium priority
    print("Processing medium priority slides...")
    for item in medium_priority[:10]:  # Process top 10
        slide_num = item['slide']
        title = item['title'][:50]
        overflow = item['overflow_px']
        current_class = item['current_class']

        print(f"Slide {slide_num}: {title}")
        print(f"  Overflow: {overflow}px, Class: {current_class}")

        if overflow > 100 and 'compact' not in current_class:
            if find_and_update_slide(slide_num, apply_compact_class):
                print(f"  ✓ Applied compact class")
                results['compact_applied'].append(slide_num)
            else:
                print(f"  ✗ Could not apply compact")
        else:
            print(f"  ~ No action needed")
            results['no_change'].append(slide_num)

        print()

    # Summary
    print("=" * 80)
    print("OPTIMIZATION RESULTS")
    print("=" * 80)
    print()
    print(f"✅ Compact class applied:     {len(results['compact_applied'])} slides")
    print(f"✅ Supercompact applied:      {len(results['supercompact_applied'])} slides")
    print(f"✅ Content condensed:         {len(results['content_condensed'])} slides")
    print(f"⚠️  No automatic change:      {len(results['no_change'])} slides")
    print()

    if results['compact_applied']:
        print(f"Compact applied to slides: {', '.join(map(str, results['compact_applied']))}")
    if results['supercompact_applied']:
        print(f"Supercompact applied to slides: {', '.join(map(str, results['supercompact_applied']))}")
    if results['content_condensed']:
        print(f"Content condensed in slides: {', '.join(map(str, results['content_condensed']))}")

    print()
    print("Next step: Regenerate all_slides.md and rebuild HTML")

if __name__ == '__main__':
    main()
