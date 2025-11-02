#!/usr/bin/env python3
"""
Fix excessive whitespace by removing/reducing ultracompact and supercompact classes.
Processes individual slide files directly.
"""

import re
from pathlib import Path
from typing import Dict, Tuple

def count_words(text: str) -> int:
    """Count words in text, excluding HTML comments and image syntax"""
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Remove image syntax
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Count words
    return len(text.split())

def get_slide_content_after_class(lines, class_line_idx):
    """Get content after the _class directive until next --- or end of file"""
    content_lines = []
    for i in range(class_line_idx + 1, len(lines)):
        if lines[i].strip() == '---':
            break
        content_lines.append(lines[i])
    return '\n'.join(content_lines)

def should_remove_ultracompact(word_count: int) -> Tuple[bool, str]:
    """Determine if ultracompact should be removed"""
    if word_count < 50:
        return True, f"REMOVE (ultracompact → normal, {word_count} words)"
    return False, f"ultracompact → compact ({word_count} words, convert needed)"

def should_remove_supercompact(word_count: int) -> Tuple[bool, str]:
    """Determine if supercompact should be removed"""
    if word_count < 30:
        return True, f"REMOVE (supercompact → normal, {word_count} words)"
    elif word_count < 80:
        return False, f"supercompact → compact ({word_count} words, convert needed)"
    else:
        return False, f"NO CHANGE (supercompact kept, {word_count} words - content-heavy)"

def should_remove_compact(word_count: int) -> Tuple[bool, str]:
    """Determine if compact should be removed"""
    if word_count < 40:
        return True, f"REMOVE (compact → normal, {word_count} words)"
    return False, f"NO CHANGE (compact kept, {word_count} words - sufficient content)"

def fix_class_line(line: str, word_count: int) -> Tuple[str, str]:
    """
    Fix a single _class directive line.
    Returns: (new_line, change_description)
    """
    match = re.match(r'<!--\s*_class:\s*(.+?)\s*-->', line)
    if not match:
        return line, "NO CHANGE (no _class directive)"

    classes = match.group(1).strip().split()

    # Skip lead and title slides
    if 'lead' in classes or 'title' in classes:
        return line, "NO CHANGE (lead/title slide)"

    # Extract layout classes and compact classes
    layout_classes = []
    compact_classes = []

    for cls in classes:
        if cls in ['ultracompact', 'supercompact', 'compact']:
            compact_classes.append(cls)
        else:
            layout_classes.append(cls)

    if not compact_classes:
        return line, "NO CHANGE (no compact classes)"

    # Process each compact class
    changes = []
    new_compact = []

    if 'ultracompact' in compact_classes:
        remove, desc = should_remove_ultracompact(word_count)
        if not remove:
            # Convert ultracompact to compact
            new_compact.append('compact')
            changes.append(desc)
        else:
            changes.append(desc)

    if 'supercompact' in compact_classes:
        remove, desc = should_remove_supercompact(word_count)
        if not remove:
            # Check if we should convert to compact
            if word_count < 80:
                new_compact.append('compact')
            else:
                new_compact.append('supercompact')
        changes.append(desc)

    if 'compact' in compact_classes and 'ultracompact' not in compact_classes and 'supercompact' not in compact_classes:
        # Only process standalone compact
        remove, desc = should_remove_compact(word_count)
        if not remove:
            new_compact.append('compact')
        changes.append(desc)

    # If we had multiple compact modifiers, remove all and optionally add one
    if len(compact_classes) > 1:
        # Multiple compact classes - remove all duplicates
        new_compact = list(set(new_compact))

    # Build new class list
    result_classes = layout_classes + new_compact

    if not result_classes:
        new_line = '<!-- _class: -->'
    else:
        new_line = f'<!-- _class: {" ".join(result_classes)} -->'

    if new_line == line:
        return line, '; '.join(changes) if changes else "NO CHANGE"

    change_desc = '; '.join(changes)
    old_classes = ' '.join(classes)
    new_classes = ' '.join(result_classes) if result_classes else '(empty)'

    return new_line, f"{change_desc} | '{old_classes}' → '{new_classes}'"

def process_file(file_path: Path) -> Dict:
    """Process a single markdown file"""
    content = file_path.read_text()
    lines = content.split('\n')

    changes_made = 0
    changes_list = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this is a _class directive
        if '<!-- _class:' in line and ('ultracompact' in line or 'supercompact' in line or 'compact' in line):
            # Get content after this directive
            slide_content = get_slide_content_after_class(lines, i)
            word_count = count_words(slide_content)

            # Fix the class line
            new_line, change_desc = fix_class_line(line, word_count)

            if new_line != line:
                lines[i] = new_line
                changes_made += 1
                changes_list.append(f"  Line {i+1}: {change_desc}")

        i += 1

    # Write back if changes were made
    if changes_made > 0:
        file_path.write_text('\n'.join(lines))

    return {
        'file': file_path.name,
        'changes': changes_made,
        'details': changes_list
    }

def main():
    """Main execution"""
    slides_dir = Path('/home/cuzic/ai-dev-yodoq/slides')
    files = ['day1_1.md', 'day1_2.md', 'day1_3.md', 'day2_1.md', 'day2_2.md']

    print("Processing slide files...\n")

    total_changes = 0
    all_results = []

    for filename in files:
        file_path = slides_dir / filename
        if not file_path.exists():
            print(f"✗ {filename}: File not found")
            continue

        result = process_file(file_path)
        all_results.append(result)
        total_changes += result['changes']

        if result['changes'] > 0:
            print(f"✓ {filename}: {result['changes']} changes")
            for detail in result['details']:
                print(detail)
        else:
            print(f"○ {filename}: No changes needed")
        print()

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total files processed: {len(all_results)}")
    print(f"Total changes made: {total_changes}")
    print()

    # Regenerate all_slides.md
    print("Regenerating all_slides.md...")
    all_content = []
    for filename in files:
        file_path = slides_dir / filename
        if file_path.exists():
            all_content.append(file_path.read_text())

    all_slides_path = slides_dir / 'all_slides.md'
    all_slides_path.write_text('\n---\n\n'.join(all_content))

    print("✓ all_slides.md regenerated")
    print("\nDone!")

if __name__ == '__main__':
    main()
