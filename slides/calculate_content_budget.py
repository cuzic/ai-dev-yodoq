#!/usr/bin/env python3
"""
Calculate appropriate character and line budgets for each layout class and compact level.
Goal: Balance overflow elimination with readability and content richness.
"""

# Marp slide dimensions
SLIDE_WIDTH = 1280
SLIDE_HEIGHT = 720

# Font size and line height for each compact level
FONT_CONFIGS = {
    'normal': {'font_size': 18, 'line_height': 1.5, 'h1': 32, 'h2': 24, 'h3': 20},
    'compact': {'font_size': 16, 'line_height': 1.4, 'h1': 28, 'h2': 20, 'h3': 18},
    'supercompact': {'font_size': 14, 'line_height': 1.3, 'h1': 24, 'h2': 18, 'h3': 16},
    'ultracompact': {'font_size': 12, 'line_height': 1.2, 'h1': 20, 'h2': 16, 'h3': 14},
}

# Layout-specific available space (percentage of slide)
LAYOUTS = {
    'full-content': {
        'width_ratio': 0.85,  # 85% of slide width
        'height_ratio': 0.75, # 75% of slide height (accounting for header/footer)
        'description': 'Standard full-content layout'
    },
    'two-column': {
        'width_ratio': 0.40,  # Each column is 40% of slide width
        'height_ratio': 0.75,
        'description': 'Two-column layout (per column)'
    },
    'card-grid': {
        'width_ratio': 0.42,  # Each card is ~42% of slide width (2 columns)
        'height_ratio': 0.35, # Each card is ~35% of slide height (2 rows)
        'description': 'Card grid layout (per card)'
    },
    'layout-horizontal-left': {
        'width_ratio': 0.48,  # Left side is ~48% of slide width
        'height_ratio': 0.70,
        'description': 'Horizontal split layout (left side)'
    },
    'layout-horizontal-right': {
        'width_ratio': 0.48,  # Right side is ~48% of slide width
        'height_ratio': 0.70,
        'description': 'Horizontal split layout (right side)'
    },
}

# Character width estimation (pixels per character)
CHAR_WIDTH = {
    'normal': 10.0,     # 18px font ~ 10px per char
    'compact': 9.0,     # 16px font ~ 9px per char
    'supercompact': 8.0, # 14px font ~ 8px per char
    'ultracompact': 7.0, # 12px font ~ 7px per char
}

def calculate_budget(layout_name, layout_config, compact_level, font_config):
    """Calculate character and line budget for a specific configuration."""

    # Available dimensions
    available_width = SLIDE_WIDTH * layout_config['width_ratio']
    available_height = SLIDE_HEIGHT * layout_config['height_ratio']

    # Calculate line budget
    line_height_px = font_config['font_size'] * font_config['line_height']
    max_lines = int(available_height / line_height_px)

    # Calculate character budget per line
    char_width = CHAR_WIDTH[compact_level]
    max_chars_per_line = int(available_width / char_width)

    # Total character budget (approximately)
    total_chars = max_lines * max_chars_per_line

    return {
        'layout': layout_name,
        'compact_level': compact_level,
        'max_lines': max_lines,
        'max_chars_per_line': max_chars_per_line,
        'total_chars': total_chars,
        'font_size': font_config['font_size'],
        'available_width_px': int(available_width),
        'available_height_px': int(available_height),
    }

def print_budget_table():
    """Print comprehensive budget table for all combinations."""

    print("=" * 120)
    print("CONTENT BUDGET CALCULATION - BALANCED APPROACH")
    print("Goal: Maximize quality score (readability + content richness + no overflow)")
    print("=" * 120)
    print()

    for layout_name, layout_config in LAYOUTS.items():
        print(f"\n{'='*120}")
        print(f"Layout: {layout_name} - {layout_config['description']}")
        print(f"{'='*120}")
        print(f"{'Compact Level':<20} {'Font':<8} {'Max Lines':<12} {'Chars/Line':<15} {'Total Chars':<15} {'Available Space':<20}")
        print('-' * 120)

        for compact_level, font_config in FONT_CONFIGS.items():
            budget = calculate_budget(layout_name, layout_config, compact_level, font_config)
            space_info = f"{budget['available_width_px']}x{budget['available_height_px']}px"
            print(f"{compact_level:<20} {budget['font_size']}px    {budget['max_lines']:<12} {budget['max_chars_per_line']:<15} {budget['total_chars']:<15} {space_info:<20}")

def print_guidelines():
    """Print content reduction guidelines."""

    print("\n" + "="*120)
    print("CONTENT REDUCTION GUIDELINES - BALANCED APPROACH")
    print("="*120)

    guidelines = """
OVERFLOW SEVERITY AND STRATEGY:

1. MINOR OVERFLOW (30-80px):
   - Strategy: Use 'compact' class (16px font)
   - Content reduction: 10-15% (remove redundancy, simplify expressions)
   - Keep: Structure, headings, bullet points, key examples
   - Example: "これは重要なポイントです" → "重要なポイント"

2. MODERATE OVERFLOW (80-150px):
   - Strategy: Use 'supercompact' class (14px font)
   - Content reduction: 20-30% (combine related points, use concise language)
   - Keep: Main structure, essential details, important context
   - Example:
     Before: "### タイミング: 実装直後\\n**プロンプト:** XXX\\n**検出:** YYY"
     After: "**タイミング**(実装直後): **プロンプト** XXX | **検出** YYY"

3. SEVERE OVERFLOW (150-250px):
   - Strategy: Use 'supercompact' class + aggressive content reduction
   - Content reduction: 35-45% (restructure to compact format)
   - Keep: Key messages, essential information
   - Consider: Restructuring content hierarchy

4. CRITICAL OVERFLOW (>250px):
   - Strategy: Consider 'ultracompact' class (12px font) ONLY as last resort
   - Content reduction: 40-50% (major restructuring)
   - Keep: Core messages only
   - WARNING: Use sparingly - readability suffers significantly at 12px

QUALITY TARGETS:
- Overflow: < 30px (strict requirement)
- Density: 0.50-0.70 (optimal: 0.60 - slide should feel "full but not crowded")
- Whitespace: 0.30-0.50 (optimal: 0.40 - breathing room for readability)
- Overlaps: 0 (no overlapping elements)

CONTENT PRESERVATION PRIORITIES:
1. Key concepts and main messages (MUST keep)
2. Important examples and context (SHOULD keep)
3. Structure (headings, bullets) for scannability (SHOULD keep)
4. Explanatory text and details (CAN reduce/simplify)
5. Redundant phrases and filler words (SHOULD remove)

AVOID:
- ❌ Excessive abbreviations that harm comprehension
- ❌ Removing all structure (turning lists into comma-separated text)
- ❌ Eliminating important examples that aid understanding
- ❌ Using ultracompact (12px) as default solution
- ❌ Focusing only on overflow without considering density/readability

PREFER:
- ✅ Concise but complete language
- ✅ Combining related points intelligently
- ✅ Restructuring for efficiency while keeping meaning
- ✅ Balancing all quality metrics (overflow, density, readability)
- ✅ Using compact/supercompact progressively based on severity
"""

    print(guidelines)

if __name__ == '__main__':
    print_budget_table()
    print_guidelines()

    print("\n" + "="*120)
    print("EXAMPLE: Card-grid layout with supercompact (common scenario)")
    print("="*120)
    budget = calculate_budget('card-grid', LAYOUTS['card-grid'], 'supercompact', FONT_CONFIGS['supercompact'])
    print(f"Available space: {budget['available_width_px']}x{budget['available_height_px']}px")
    print(f"Max lines: {budget['max_lines']} lines")
    print(f"Max chars/line: {budget['max_chars_per_line']} characters")
    print(f"Total budget: ~{budget['total_chars']} characters")
    print(f"\nThis means you can fit approximately:")
    print(f"  - {budget['max_lines']} bullet points (if 1 line each)")
    print(f"  - {budget['max_lines']//2} bullet points (if 2 lines each)")
    print(f"  - 1 heading + {budget['max_lines']-2} lines of content")
    print()
