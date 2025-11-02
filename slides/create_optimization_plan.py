#!/usr/bin/env python3
"""
Create comprehensive optimization plan combining:
- Overflow measurements (visual overflow)
- Content budget analysis (character count vs capacity)
"""

import json
import re

def load_overflow_data():
    """Extract overflow data from quick_measure.js output."""
    # From the last measurement
    overflow_slides = {
        41: 1740,
        81: 579,
        73: 540,
        99: 403,
        155: 392,
        165: 363,
        139: 305,
        122: 240,
        143: 231,
        164: 214,
        149: 212,
        104: 140,
        112: 128,
        95: 122,
        135: 122,
        150: 100,
        138: 98,
        148: 86,
        137: 77,
        82: 72,
        118: 60,
        167: 40,
        123: 39
    }
    return overflow_slides

def load_budget_data():
    """Load content budget analysis."""
    with open('slides/.logs/content_budget_analysis.json', 'r') as f:
        data = json.load(f)

    budget_map = {}
    for item in data:
        budget_map[item['slide']] = item

    return budget_map

def get_slide_info(slide_num):
    """Get slide title and content from source files."""
    files = ['slides/day1_1.md', 'slides/day1_2.md', 'slides/day1_3.md',
             'slides/day2_1.md', 'slides/day2_2.md']

    current_slide = 0
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        slides = content.split('\n---\n')
        for slide in slides:
            if slide.strip().startswith('---\nmarp:'):
                continue

            current_slide += 1

            if current_slide == slide_num:
                # Extract title
                title_match = re.search(r'^#+\s+(.+)$', slide, re.MULTILINE)
                title = title_match.group(1) if title_match else 'NO TITLE'

                # Extract class
                class_match = re.search(r'<!-- _class: (.+?) -->', slide)
                layout_class = class_match.group(1) if class_match else 'normal'

                return {
                    'title': title,
                    'class': layout_class,
                    'file': filename
                }

    return None

def create_optimization_plan():
    """Create comprehensive optimization plan."""
    overflow = load_overflow_data()
    budget = load_budget_data()

    # Combine and prioritize
    all_slides = set(overflow.keys()) | set(budget.keys())

    priority_list = []

    for slide_num in all_slides:
        overflow_px = overflow.get(slide_num, 0)
        budget_info = budget.get(slide_num, {})
        slide_info = get_slide_info(slide_num)

        if not slide_info:
            continue

        # Calculate priority score
        # High overflow = high priority
        # Over budget = high priority
        priority_score = 0

        if overflow_px > 0:
            if overflow_px > 500:
                priority_score += 100
            elif overflow_px > 300:
                priority_score += 80
            elif overflow_px > 100:
                priority_score += 50
            else:
                priority_score += 20

        usage = budget_info.get('usage', 0)
        if usage > 120:
            priority_score += 70
        elif usage > 100:
            priority_score += 30

        # Determine action
        actions = []

        if overflow_px > 300:
            if 'compact' not in slide_info['class']:
                actions.append('Apply compact class')
            else:
                actions.append('Condense content significantly')
        elif overflow_px > 100:
            if 'compact' not in slide_info['class']:
                actions.append('Apply compact class')
            else:
                actions.append('Minor content reduction')
        elif overflow_px > 0:
            actions.append('Minor content adjustment')

        if usage > 120:
            actions.append('Reduce content by ~' + str(int(usage - 100)) + '%')
        elif usage > 100:
            actions.append('Minor content reduction')

        if not actions:
            continue

        priority_list.append({
            'slide': slide_num,
            'title': slide_info['title'][:60],
            'current_class': slide_info['class'],
            'file': slide_info['file'],
            'overflow_px': overflow_px,
            'budget_usage': round(usage, 1),
            'budget_total': budget_info.get('budget', 0),
            'current_chars': budget_info.get('current', 0),
            'priority_score': priority_score,
            'actions': actions
        })

    # Sort by priority
    priority_list.sort(key=lambda x: x['priority_score'], reverse=True)

    return priority_list

def main():
    """Generate and display optimization plan."""
    print("=" * 80)
    print("COMPREHENSIVE CONTENT OPTIMIZATION PLAN")
    print("=" * 80)
    print()

    plan = create_optimization_plan()

    # Save plan
    with open('slides/.logs/optimization_plan.json', 'w', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    # Categorize by priority
    critical = [p for p in plan if p['priority_score'] >= 150]
    high = [p for p in plan if 100 <= p['priority_score'] < 150]
    medium = [p for p in plan if 50 <= p['priority_score'] < 100]
    low = [p for p in plan if p['priority_score'] < 50]

    print(f"Total slides needing optimization: {len(plan)}")
    print(f"  CRITICAL priority: {len(critical)} slides")
    print(f"  HIGH priority:     {len(high)} slides")
    print(f"  MEDIUM priority:   {len(medium)} slides")
    print(f"  LOW priority:      {len(low)} slides")
    print()

    # Show critical slides
    if critical:
        print("=" * 80)
        print("CRITICAL PRIORITY SLIDES (Score >= 150)")
        print("=" * 80)
        print(f"{'Slide':<6} {'Score':<6} {'Overflow':<10} {'Budget%':<10} {'Current Class':<25} {'Title':<30}")
        print("-" * 80)

        for p in critical:
            print(f"{p['slide']:<6} {p['priority_score']:<6} {p['overflow_px']:<10} {p['budget_usage']:<10.1f} {p['current_class']:<25} {p['title'][:28]}")
            for action in p['actions']:
                print(f"       → {action}")
        print()

    # Show high priority slides
    if high:
        print("=" * 80)
        print("HIGH PRIORITY SLIDES (Score 100-149)")
        print("=" * 80)
        print(f"{'Slide':<6} {'Score':<6} {'Overflow':<10} {'Budget%':<10} {'Current Class':<25} {'Title':<30}")
        print("-" * 80)

        for p in high[:15]:  # Show top 15
            print(f"{p['slide']:<6} {p['priority_score']:<6} {p['overflow_px']:<10} {p['budget_usage']:<10.1f} {p['current_class']:<25} {p['title'][:28]}")
            for action in p['actions']:
                print(f"       → {action}")

        if len(high) > 15:
            print(f"       ... and {len(high) - 15} more high priority slides")
        print()

    # Summary of actions
    print("=" * 80)
    print("RECOMMENDED ACTIONS SUMMARY")
    print("=" * 80)
    print()

    need_compact = len([p for p in plan if 'compact' not in p['current_class'] and any('compact' in a for a in p['actions'])])
    need_condense = len([p for p in plan if any('content' in a.lower() for a in p['actions'])])

    print(f"📊 {need_compact} slides need compact class applied")
    print(f"📝 {need_condense} slides need content reduction/condensing")
    print()

    print("IMPLEMENTATION APPROACH:")
    print("1. Apply compact class to slides with heavy overflow (>300px)")
    print("2. Condense content for slides already using compact")
    print("3. For moderate overflow (100-300px), try compact first")
    print("4. For minor overflow (<100px), minor content adjustments")
    print()

    print("Detailed plan saved to: slides/.logs/optimization_plan.json")

if __name__ == '__main__':
    main()
