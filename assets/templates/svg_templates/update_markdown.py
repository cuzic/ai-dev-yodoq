#!/usr/bin/env python3
"""
Update markdown files to reference generated SVG slides.
Replaces verbose content with SVG image references.
"""

import re
import os
import sys
from pathlib import Path


def extract_slides_with_positions(md_content):
    """
    Extract slides with their start/end positions in the file.

    Returns: List of (slide_index, start_pos, end_pos, slide_content) tuples
    """
    slides = []
    lines = md_content.split('\n')
    current_slide_lines = []
    current_slide_start = 0
    slide_index = 0

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if current_slide_lines:
                slides.append((
                    slide_index,
                    current_slide_start,
                    i,
                    '\n'.join(current_slide_lines)
                ))
                slide_index += 1
            current_slide_lines = []
            current_slide_start = i + 1
        else:
            current_slide_lines.append(line)

    # Add last slide
    if current_slide_lines:
        slides.append((
            slide_index,
            current_slide_start,
            len(lines),
            '\n'.join(current_slide_lines)
        ))

    return slides


def get_svg_filename_for_slide(slide_title, svg_dir):
    """
    Find SVG file for a given slide by matching title.

    Returns: SVG filename if found, None otherwise
    """
    import glob

    # Normalize title for matching
    normalized_title = slide_title.strip()
    normalized_title = re.sub(r'[^\w\s-]', '', normalized_title)
    normalized_title = re.sub(r'[-\s]+', '_', normalized_title)
    normalized_title = normalized_title[:30]  # Limit to 30 chars like in batch_convert

    # Try to find SVG with matching title in filename
    all_svgs = glob.glob(os.path.join(svg_dir, "slide_*.svg"))

    for svg_path in all_svgs:
        svg_name = os.path.basename(svg_path)
        # Check if normalized title is in the SVG filename
        if normalized_title and normalized_title in svg_name:
            return svg_name

    return None


def extract_title_and_class(slide_content):
    """
    Extract title and CSS class from slide content.

    Returns: (title, css_class) tuple
    """
    # Extract CSS class
    class_match = re.search(r'<!--\s*_class:\s*(.+?)\s*-->', slide_content)
    css_class = class_match.group(1) if class_match else None

    # Extract title (first # heading)
    title_match = re.search(r'^#\s+(.+)$', slide_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Untitled"

    return title, css_class


def create_svg_slide(title, svg_filename, original_class=None):
    """
    Create markdown for an SVG-based slide.

    Args:
        title: Slide title
        svg_filename: SVG filename (without path)
        original_class: Original CSS class (if any)

    Returns:
        Markdown string
    """
    # Use layout-diagram-only if no class specified
    css_class = original_class if original_class else "layout-diagram-only"

    # If original class was multi-column, change to diagram-only
    if css_class and ('column' in css_class or 'layout-' in css_class):
        css_class = "layout-diagram-only"

    markdown = f'<!-- _class: {css_class} -->\n\n'
    markdown += f'# {title}\n\n'
    markdown += f'![{title}](../diagrams-web/{svg_filename})\n'

    return markdown


def update_markdown_file(md_path, svg_dir, dry_run=True):
    """
    Update a markdown file to use SVG references.

    Args:
        md_path: Path to markdown file
        svg_dir: Directory containing SVG files
        dry_run: If True, print changes without modifying file

    Returns:
        Number of slides updated
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    lines = original_content.split('\n')
    slides = extract_slides_with_positions(original_content)

    updates = []

    for slide_idx, start_line, end_line, slide_content in slides:
        title, css_class = extract_title_and_class(slide_content)
        svg_filename = get_svg_filename_for_slide(title, svg_dir)

        if svg_filename:
            new_content = create_svg_slide(title, svg_filename, css_class)

            updates.append({
                'slide_idx': slide_idx,
                'start_line': start_line,
                'end_line': end_line,
                'old_content': slide_content,
                'new_content': new_content,
                'svg_filename': svg_filename
            })

            if dry_run:
                print(f"Slide {slide_idx}: {title} -> {svg_filename}")

    if not dry_run and updates:
        # Apply updates in reverse order to preserve line numbers
        for update in reversed(updates):
            start = update['start_line']
            end = update['end_line']
            lines[start:end] = update['new_content'].split('\n')

        # Write updated content
        new_content = '\n'.join(lines)
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return len(updates)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Update markdown files with SVG references')
    parser.add_argument('markdown_files', nargs='+', help='Markdown files to update')
    parser.add_argument('--svg-dir', default='../diagrams-web', help='Directory containing SVG files')
    parser.add_argument('--dry-run', action='store_true', help='Print changes without modifying files')

    args = parser.parse_args()

    total_updates = 0

    for md_file in args.markdown_files:
        print(f"\n{'='*60}")
        print(f"Processing: {md_file}")
        print(f"{'='*60}")

        num_updates = update_markdown_file(md_file, args.svg_dir, args.dry_run)
        total_updates += num_updates

        print(f"\nSlides to update: {num_updates}")

    print(f"\n{'='*60}")
    print(f"Total slides to update: {total_updates}")
    print(f"{'='*60}")

    if args.dry_run:
        print("\nThis was a dry run. Remove --dry-run to apply changes.")


if __name__ == '__main__':
    main()
