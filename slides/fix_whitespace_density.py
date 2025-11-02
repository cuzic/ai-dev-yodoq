#!/usr/bin/env python3
"""
Fix excessive whitespace in slides by adjusting CSS compact classes.
Processes the top 50 most problematic slides identified in ACTIONABLE_SLIDES.txt
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

# Define the conversion rules based on word count and current classes
def convert_classes(current_classes: str, word_count: int, has_image: bool) -> Tuple[str, str]:
    """
    Convert CSS classes based on content and word count.
    Returns: (new_classes, conversion_description)
    """
    classes = current_classes.strip().split()

    # Extract layout classes (preserve these)
    layout_classes = []
    compact_classes = []

    for cls in classes:
        if cls in ['ultracompact', 'supercompact', 'compact']:
            compact_classes.append(cls)
        else:
            layout_classes.append(cls)

    # Skip if no compact classes
    if not compact_classes:
        return current_classes, "NO_CHANGE (no compact classes)"

    # Skip if it's a lead slide
    if 'lead' in layout_classes or 'title' in layout_classes:
        return current_classes, "NO_CHANGE (lead/title slide)"

    # Determine the new compact class based on word count
    new_compact = None

    if 'ultracompact' in compact_classes:
        # ultracompact (12px) - Remove completely or convert
        if word_count < 50:
            new_compact = None  # Remove ultracompact
            conversion = f"ultracompact → REMOVE ({word_count} words)"
        else:
            new_compact = 'compact'
            conversion = f"ultracompact → compact ({word_count} words)"

    elif 'supercompact' in compact_classes:
        # supercompact (14px) - Remove or reduce
        if word_count < 30:
            new_compact = None  # Remove supercompact
            conversion = f"supercompact → REMOVE ({word_count} words)"
        elif word_count < 80:
            new_compact = 'compact'
            conversion = f"supercompact → compact ({word_count} words)"
        else:
            new_compact = 'supercompact'  # Keep if content-heavy
            conversion = f"NO_CHANGE (supercompact, {word_count} words - content-heavy)"

    elif 'compact' in compact_classes:
        # compact (16px) - Remove if content is minimal
        if word_count < 40:
            new_compact = None  # Remove compact
            conversion = f"compact → REMOVE ({word_count} words)"
        else:
            new_compact = 'compact'  # Keep if 40+ words
            conversion = f"NO_CHANGE (compact, {word_count} words - sufficient content)"

    # Build new class list
    result_classes = layout_classes.copy()
    if new_compact:
        result_classes.append(new_compact)

    new_class_str = ' '.join(result_classes) if result_classes else ''

    return new_class_str, conversion


def count_words_in_slide(slide_content: str) -> int:
    """Count words in slide content (excluding YAML frontmatter and HTML comments)"""
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', slide_content, flags=re.DOTALL)
    # Remove YAML frontmatter
    content = re.sub(r'^---\s*$.*?^---\s*$', '', content, flags=re.MULTILINE | re.DOTALL)
    # Remove image syntax
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    # Remove headings markers
    content = re.sub(r'^#+\s*', '', content, flags=re.MULTILINE)
    # Remove list markers
    content = re.sub(r'^\s*[-*]\s+', '', content, flags=re.MULTILINE)
    # Remove HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    # Count words
    words = content.split()
    return len(words)


def has_images(slide_content: str) -> bool:
    """Check if slide has images"""
    return bool(re.search(r'!\[.*?\]\(.*?\)', slide_content))


def find_slide_in_file(file_path: Path, slide_number: int) -> Tuple[int, int, str]:
    """
    Find a specific slide by number in a markdown file.
    Returns: (start_line, end_line, slide_content)
    """
    content = file_path.read_text()
    lines = content.split('\n')

    # Find slide boundaries
    slide_separators = [-1]  # Start before first slide
    for i, line in enumerate(lines):
        if line.strip() == '---':
            slide_separators.append(i)
    slide_separators.append(len(lines))  # End after last slide

    # Each file starts at slide 1
    if slide_number < 1 or slide_number > len(slide_separators) - 1:
        return -1, -1, ""

    start = slide_separators[slide_number - 1] + 1
    end = slide_separators[slide_number]

    slide_content = '\n'.join(lines[start:end])
    return start, end, slide_content


def get_slide_file_and_local_number(slide_number: int) -> Tuple[Path, int]:
    """
    Determine which file contains a given slide number and its local position.
    Returns: (file_path, local_slide_number)
    """
    slides_dir = Path('/home/cuzic/ai-dev-yodoq/slides')

    # Define file structure (order matters!)
    files = [
        'day1_1.md',
        'day1_2.md',
        'day1_3.md',
        'day2_1.md',
        'day2_2.md'
    ]

    current_slide = 0
    for filename in files:
        file_path = slides_dir / filename
        if not file_path.exists():
            continue

        content = file_path.read_text()
        slide_count = content.count('\n---\n') + 1

        if current_slide + slide_count >= slide_number:
            local_number = slide_number - current_slide
            return file_path, local_number

        current_slide += slide_count

    raise ValueError(f"Slide {slide_number} not found in any file")


def fix_slide_classes(slide_number: int) -> Tuple[bool, str]:
    """
    Fix CSS classes for a specific slide.
    Returns: (success, message)
    """
    try:
        # Find the file and local slide number
        file_path, local_number = get_slide_file_and_local_number(slide_number)

        # Read the file
        content = file_path.read_text()
        lines = content.split('\n')

        # Find slide boundaries
        start_line, end_line, slide_content = find_slide_in_file(file_path, local_number)

        if start_line == -1:
            return False, f"Slide {slide_number} not found in {file_path.name}"

        # Find _class directive
        class_pattern = r'<!--\s*_class:\s*([^>]+)\s*-->'
        match = re.search(class_pattern, slide_content)

        if not match:
            return False, f"Slide {slide_number}: No _class directive found"

        current_classes = match.group(1).strip()

        # Count words and check for images
        word_count = count_words_in_slide(slide_content)
        has_img = has_images(slide_content)

        # Convert classes
        new_classes, conversion_desc = convert_classes(current_classes, word_count, has_img)

        if current_classes == new_classes:
            return False, f"Slide {slide_number}: {conversion_desc}"

        # Replace in the original file
        old_directive = f'<!-- _class: {current_classes} -->'
        new_directive = f'<!-- _class: {new_classes} -->' if new_classes else '<!-- _class: -->'

        # Calculate absolute line numbers
        absolute_start = start_line
        slide_lines = lines[absolute_start:end_line]

        # Replace in the slide content
        for i, line in enumerate(slide_lines):
            if old_directive in line:
                slide_lines[i] = line.replace(old_directive, new_directive)
                break

        # Reconstruct file
        new_lines = lines[:absolute_start] + slide_lines + lines[end_line:]
        file_path.write_text('\n'.join(new_lines))

        return True, f"Slide {slide_number} ({file_path.name}): {conversion_desc} | '{current_classes}' → '{new_classes}'"

    except Exception as e:
        return False, f"Slide {slide_number}: ERROR - {str(e)}"


def main():
    """Main execution function"""

    # Top 50 slides to fix (from ACTIONABLE_SLIDES.txt)
    critical_slides = [
        44, 58, 89, 108, 170, 45, 13, 88, 149, 150,
        33, 37, 79, 165, 160, 73, 20, 47, 163, 74,
        115, 43, 29, 134, 35, 25, 84, 162, 135, 52,
        124, 41, 123, 136, 139, 122, 129, 3, 50
    ]

    high_priority_slides = [
        145, 49, 128, 80, 131, 23, 7, 38, 26, 106, 28
    ]

    all_slides = critical_slides + high_priority_slides

    print(f"Processing {len(all_slides)} slides...\n")

    # Track conversions
    stats = {
        'ultracompact_removed': 0,
        'supercompact_removed': 0,
        'compact_removed': 0,
        'ultracompact_to_compact': 0,
        'supercompact_to_compact': 0,
        'no_change': 0,
        'errors': 0
    }

    results = []

    for slide_num in sorted(all_slides):
        success, message = fix_slide_classes(slide_num)
        results.append((slide_num, success, message))

        # Update stats
        if not success:
            if 'NO_CHANGE' in message:
                stats['no_change'] += 1
            else:
                stats['errors'] += 1
        else:
            if 'ultracompact → REMOVE' in message:
                stats['ultracompact_removed'] += 1
            elif 'supercompact → REMOVE' in message:
                stats['supercompact_removed'] += 1
            elif 'compact → REMOVE' in message:
                stats['compact_removed'] += 1
            elif 'ultracompact → compact' in message:
                stats['ultracompact_to_compact'] += 1
            elif 'supercompact → compact' in message:
                stats['supercompact_to_compact'] += 1

    # Print results
    print("\n" + "="*80)
    print("CONVERSION RESULTS")
    print("="*80)

    for slide_num, success, message in results:
        status = "✓" if success else "○"
        print(f"{status} {message}")

    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    print(f"Total slides processed: {len(all_slides)}")
    print(f"✓ Successfully converted: {sum(1 for _, s, _ in results if s)}")
    print(f"○ No change needed: {stats['no_change']}")
    print(f"✗ Errors: {stats['errors']}")
    print()
    print("Class Conversions:")
    print(f"  • ultracompact removed: {stats['ultracompact_removed']}")
    print(f"  • ultracompact → compact: {stats['ultracompact_to_compact']}")
    print(f"  • supercompact removed: {stats['supercompact_removed']}")
    print(f"  • supercompact → compact: {stats['supercompact_to_compact']}")
    print(f"  • compact removed: {stats['compact_removed']}")
    print()

    # Estimate whitespace reduction
    total_converted = sum(1 for _, s, _ in results if s)
    avg_whitespace_reduction = 15  # Conservative estimate: 15% per slide

    print(f"Expected Impact:")
    print(f"  • Slides improved: {total_converted}")
    print(f"  • Avg whitespace reduction per slide: ~{avg_whitespace_reduction}%")
    print(f"  • Total effective area reclaimed: ~{total_converted * avg_whitespace_reduction / len(all_slides):.1f}% across target slides")
    print()
    print("="*80)

    # Regenerate all_slides.md
    print("\nRegenerating all_slides.md...")
    slides_dir = Path('/home/cuzic/ai-dev-yodoq/slides')
    files = ['day1_1.md', 'day1_2.md', 'day1_3.md', 'day2_1.md', 'day2_2.md']

    all_content = []
    for filename in files:
        file_path = slides_dir / filename
        if file_path.exists():
            all_content.append(file_path.read_text())

    all_slides_path = slides_dir / 'all_slides.md'
    all_slides_path.write_text('\n---\n\n'.join(all_content))

    print(f"✓ all_slides.md regenerated successfully")
    print("\nDone!")


if __name__ == '__main__':
    main()
