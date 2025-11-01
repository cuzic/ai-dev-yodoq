#!/usr/bin/env python3
"""
Batch conversion script to convert markdown slides to SVG.
Analyzes slide content and uses appropriate templates.
"""

import re
import os
import sys
from pathlib import Path

# Import templates
sys.path.insert(0, os.path.dirname(__file__))
from summary_template import generate_from_markdown as generate_summary
from checklist_template import generate_from_markdown as generate_checklist
from comparison_template import generate_from_markdown as generate_comparison
from workflow_template import generate_from_markdown as generate_workflow


def extract_slides(md_content):
    """Extract individual slides from markdown content."""
    # Split by slide separators (---) or h1 headers
    slides = []
    current_slide = []

    for line in md_content.split('\n'):
        if line.strip() == '---':
            if current_slide:
                slides.append('\n'.join(current_slide))
                current_slide = []
        else:
            current_slide.append(line)

    # Add last slide
    if current_slide:
        slides.append('\n'.join(current_slide))

    return slides


def detect_slide_type(slide_content):
    """
    Detect the type of slide based on content patterns.

    Returns: 'summary', 'checklist', 'comparison', 'workflow', or None
    """
    # Check for checklist pattern (has checkboxes)
    if re.search(r'[-*+]\s+\[.\]', slide_content):
        return 'checklist'

    # Check for comparison pattern (Before/After, Good/Bad)
    comparison_patterns = [
        r'\*\*(?:Before|After|前|後)[:：]?\*\*',
        r'\*\*(?:❌|✅|Good|Bad|良い|悪い)',
    ]
    for pattern in comparison_patterns:
        if re.search(pattern, slide_content):
            return 'comparison'

    # Check for workflow pattern (Step 1, Step 2, etc.) - must have at least 2 steps
    workflow_matches = re.findall(r'##\s+(?:Step\s+\d+|STEP\s*\d+)', slide_content, re.IGNORECASE)
    if len(workflow_matches) >= 2:
        return 'workflow'

    # Check for summary pattern (multiple ## sections with lists)
    sections = re.findall(r'##\s+.+', slide_content)
    lists = re.findall(r'[-*+]\s+.+', slide_content)
    if len(sections) >= 2 and len(lists) >= 5:
        return 'summary'

    return None


def should_convert_slide(slide_content):
    """
    Determine if a slide should be converted to SVG.

    Criteria:
    - Has high information density (many list items)
    - Is a specific pattern (checklist, comparison, workflow, summary)
    - Does not already have an image reference
    """
    # Skip if already has image
    if re.search(r'!\[.*?\]\(.*?\)', slide_content):
        return False

    # Skip title slides
    if re.match(r'^#\s+.+$\s*$', slide_content.strip(), re.MULTILINE):
        return False

    # Check if matches a pattern
    slide_type = detect_slide_type(slide_content)
    if slide_type:
        return True

    # Check for high density (15+ list items)
    list_count = len(re.findall(r'[-*+]\s+', slide_content))
    if list_count >= 15:
        return True

    return False


def generate_svg_filename(slide_title, index):
    """Generate a safe filename for the SVG."""
    # Extract title
    title_match = re.search(r'^#\s+(.+)$', slide_title, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        # Remove special characters
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        safe_title = safe_title[:30]  # Limit length
        return f"slide_{index:03d}_{safe_title}.svg"
    else:
        return f"slide_{index:03d}.svg"


def convert_slide_to_svg(slide_content, slide_type):
    """Convert a slide to SVG using the appropriate template."""
    try:
        if slide_type == 'summary':
            return generate_summary(slide_content)
        elif slide_type == 'checklist':
            return generate_checklist(slide_content)
        elif slide_type == 'comparison':
            return generate_comparison(slide_content)
        elif slide_type == 'workflow':
            return generate_workflow(slide_content)
        else:
            # Try summary as default for high-density content
            return generate_summary(slide_content)
    except Exception as e:
        print(f"Error converting slide: {e}")
        return None


def process_markdown_file(md_path, output_dir, dry_run=True):
    """
    Process a markdown file and generate SVG files for appropriate slides.

    Args:
        md_path: Path to markdown file
        output_dir: Directory to save SVG files
        dry_run: If True, only print what would be done

    Returns:
        List of (slide_index, svg_filename, slide_type) tuples
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    slides = extract_slides(content)
    conversions = []

    for idx, slide in enumerate(slides):
        if should_convert_slide(slide):
            slide_type = detect_slide_type(slide)
            svg_filename = generate_svg_filename(slide, idx)

            print(f"Slide {idx}: {slide_type or 'auto'} -> {svg_filename}")

            if not dry_run:
                svg_content = convert_slide_to_svg(slide, slide_type)
                if svg_content:
                    svg_path = os.path.join(output_dir, svg_filename)
                    with open(svg_path, 'w', encoding='utf-8') as f:
                        f.write(svg_content)
                    conversions.append((idx, svg_filename, slide_type))
            else:
                conversions.append((idx, svg_filename, slide_type))

    return conversions


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Batch convert markdown slides to SVG')
    parser.add_argument('markdown_files', nargs='+', help='Markdown files to process')
    parser.add_argument('--output-dir', default='../diagrams-web', help='Output directory for SVG files')
    parser.add_argument('--dry-run', action='store_true', help='Print what would be done without actually doing it')

    args = parser.parse_args()

    # Create output directory if needed
    os.makedirs(args.output_dir, exist_ok=True)

    total_conversions = 0

    for md_file in args.markdown_files:
        print(f"\n{'='*60}")
        print(f"Processing: {md_file}")
        print(f"{'='*60}")

        conversions = process_markdown_file(md_file, args.output_dir, args.dry_run)
        total_conversions += len(conversions)

        print(f"\nFound {len(conversions)} slides to convert")

    print(f"\n{'='*60}")
    print(f"Total slides to convert: {total_conversions}")
    print(f"{'='*60}")

    if args.dry_run:
        print("\nThis was a dry run. Use --no-dry-run to actually generate files.")


if __name__ == '__main__':
    main()
