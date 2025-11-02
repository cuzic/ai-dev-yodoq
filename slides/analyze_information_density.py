#!/usr/bin/env python3
"""
Analyze slides for information density issues.
Identifies slides with:
- Very low character count but aggressive compression (supercompact/ultracompact)
- Inappropriate layout classes for minimal content
- Excessive whitespace due to over-compression
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class Severity(Enum):
    CRITICAL = "CRITICAL"  # <50 chars with ultracompact/supercompact
    HIGH = "HIGH"          # <100 chars with ultracompact/supercompact
    MEDIUM = "MEDIUM"      # <200 chars with supercompact
    LOW = "LOW"            # Potential issues

@dataclass
class SlideAnalysis:
    slide_num: int
    line_start: int
    line_end: int
    layout_class: str
    compact_class: str
    content_chars: int
    element_count: int
    severity: Severity
    issue_description: str
    recommended_fix: str
    raw_content: str

def extract_slides(filepath: str) -> List[Tuple[int, int, int, str]]:
    """Extract slide boundaries from the markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    slides = []
    slide_num = 0
    current_start = 0

    for i, line in enumerate(lines, 1):
        if line.strip() == '---':
            if current_start > 0:
                slides.append((slide_num, current_start, i, ''.join(lines[current_start-1:i])))
            slide_num += 1
            current_start = i + 1

    # Add last slide
    if current_start <= len(lines):
        slides.append((slide_num, current_start, len(lines), ''.join(lines[current_start-1:])))

    return slides

def extract_class_info(content: str) -> Tuple[str, str]:
    """Extract layout and compact classes from slide content."""
    # Look for <!-- _class: ... --> comments
    class_match = re.search(r'<!--\s*_class:\s*([^-]+?)-->', content)
    if not class_match:
        return "none", "normal"

    classes = class_match.group(1).strip().split()

    # Identify layout class
    layout_classes = ['lead', 'layout-diagram-only', 'layout-horizontal-left',
                      'layout-horizontal-right', 'layout-comparison', 'layout-callout',
                      'two-column', 'layout-timeline', 'layout-code-focus', 'card-grid']
    layout = next((c for c in classes if c in layout_classes), "normal")

    # Identify compact class
    compact_classes = ['ultracompact', 'supercompact', 'compact', 'normal']
    compact = next((c for c in classes if c in compact_classes), "normal")

    return layout, compact

def count_content(content: str) -> Tuple[int, int]:
    """Count meaningful content characters and elements."""
    # Remove class directives
    content_clean = re.sub(r'<!--\s*_class:.*?-->', '', content, flags=re.DOTALL)
    # Remove separator lines
    content_clean = re.sub(r'^---\s*$', '', content_clean, flags=re.MULTILINE)
    # Remove marp directives
    content_clean = re.sub(r'marp:\s*true', '', content_clean)
    content_clean = re.sub(r'theme:\s*\w+', '', content_clean)
    content_clean = re.sub(r'paginate:\s*\w+', '', content_clean)

    # Count elements
    elements = 0
    elements += len(re.findall(r'^#+\s+.+$', content_clean, re.MULTILINE))  # Headings
    elements += len(re.findall(r'^[-*]\s+.+$', content_clean, re.MULTILINE))  # List items
    elements += len(re.findall(r'!\[.*?\]\(.*?\)', content_clean))  # Images
    elements += len(re.findall(r'^>\s+.+$', content_clean, re.MULTILINE))  # Blockquotes
    elements += len(re.findall(r'<div[^>]*>.*?</div>', content_clean, flags=re.DOTALL))  # Divs

    # Count actual text characters (excluding markdown syntax)
    text_only = re.sub(r'!\[.*?\]\(.*?\)', '', content_clean)  # Remove images
    text_only = re.sub(r'```.*?```', '', text_only, flags=re.DOTALL)  # Remove code blocks
    text_only = re.sub(r'`[^`]+`', '', text_only)  # Remove inline code
    text_only = re.sub(r'^\s*#+\s*', '', text_only, flags=re.MULTILINE)  # Remove heading markers
    text_only = re.sub(r'^\s*[-*]\s*', '', text_only, flags=re.MULTILINE)  # Remove list markers
    text_only = re.sub(r'\*\*([^*]+)\*\*', r'\1', text_only)  # Remove bold
    text_only = re.sub(r'__([^_]+)__', r'\1', text_only)  # Remove bold
    text_only = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text_only)  # Remove links, keep text
    text_only = re.sub(r'<[^>]+>', '', text_only)  # Remove HTML tags

    char_count = len(text_only.strip())

    return char_count, elements

def analyze_slide(slide_num: int, line_start: int, line_end: int, content: str) -> SlideAnalysis:
    """Analyze a single slide for information density issues."""
    layout, compact = extract_class_info(content)
    char_count, elements = count_content(content)

    # Determine severity and issues
    severity = None
    issue_description = ""
    recommended_fix = ""

    # Skip section dividers (very minimal intentional slides)
    is_section_divider = (char_count < 30 and elements <= 2 and
                         (layout == "lead" or '##' in content))

    if is_section_divider:
        severity = Severity.LOW
        issue_description = "Section divider - intentionally minimal"
        recommended_fix = "No change needed - appropriate for section divider"

    # Check for over-compression issues
    elif compact == "ultracompact":
        if char_count < 50:
            severity = Severity.CRITICAL
            issue_description = f"ULTRA-compressed with only {char_count} chars - wasteful whitespace"
            recommended_fix = "Change to 'normal' or 'compact' - ultracompact is overkill"
        elif char_count < 100:
            severity = Severity.HIGH
            issue_description = f"Ultracompact with only {char_count} chars - unnecessary compression"
            recommended_fix = "Change to 'compact' or 'normal'"
        elif char_count < 200:
            severity = Severity.MEDIUM
            issue_description = f"Ultracompact with {char_count} chars - may be over-compressed"
            recommended_fix = "Consider changing to 'compact'"
        else:
            severity = Severity.LOW
            issue_description = f"Ultracompact with {char_count} chars - appropriate"
            recommended_fix = "No change needed"

    elif compact == "supercompact":
        if char_count < 50:
            severity = Severity.CRITICAL
            issue_description = f"SUPER-compressed with only {char_count} chars - wasteful whitespace"
            recommended_fix = "Change to 'normal' or 'compact'"
        elif char_count < 100:
            severity = Severity.HIGH
            issue_description = f"Supercompact with only {char_count} chars - unnecessary compression"
            recommended_fix = "Change to 'compact' or 'normal'"
        elif char_count < 200:
            severity = Severity.MEDIUM
            issue_description = f"Supercompact with {char_count} chars - may be over-compressed"
            recommended_fix = "Consider changing to 'compact'"
        else:
            severity = Severity.LOW
            issue_description = f"Supercompact with {char_count} chars - appropriate"
            recommended_fix = "No change needed"

    elif compact == "compact":
        if char_count < 50:
            severity = Severity.MEDIUM
            issue_description = f"Compact with only {char_count} chars - may be over-compressed"
            recommended_fix = "Consider changing to 'normal'"
        elif char_count < 100:
            severity = Severity.LOW
            issue_description = f"Compact with {char_count} chars - borderline"
            recommended_fix = "Consider changing to 'normal' if slide looks sparse"
        else:
            severity = Severity.LOW
            issue_description = f"Compact with {char_count} chars - appropriate"
            recommended_fix = "No change needed"

    else:  # normal
        if char_count < 30 and not is_section_divider:
            severity = Severity.LOW
            issue_description = f"Very minimal content ({char_count} chars) with normal spacing"
            recommended_fix = "Verify this is intentional"
        else:
            severity = Severity.LOW
            issue_description = f"Normal spacing with {char_count} chars - appropriate"
            recommended_fix = "No change needed"

    return SlideAnalysis(
        slide_num=slide_num,
        line_start=line_start,
        line_end=line_end,
        layout_class=layout,
        compact_class=compact,
        content_chars=char_count,
        element_count=elements,
        severity=severity,
        issue_description=issue_description,
        recommended_fix=recommended_fix,
        raw_content=content
    )

def main():
    filepath = "/home/cuzic/ai-dev-yodoq/slides/all_slides.md"

    print("Analyzing slides for information density issues...")
    print("=" * 80)

    slides = extract_slides(filepath)
    analyses = [analyze_slide(num, start, end, content)
                for num, start, end, content in slides]

    # Filter and sort by severity
    severity_order = {
        Severity.CRITICAL: 0,
        Severity.HIGH: 1,
        Severity.MEDIUM: 2,
        Severity.LOW: 3
    }

    problematic = [a for a in analyses if a.severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM]]
    problematic.sort(key=lambda x: (severity_order[x.severity], x.content_chars))

    # Print summary
    print(f"\nTotal slides analyzed: {len(analyses)}")
    print(f"Problematic slides found: {len(problematic)}")
    print(f"  - CRITICAL: {sum(1 for a in problematic if a.severity == Severity.CRITICAL)}")
    print(f"  - HIGH: {sum(1 for a in problematic if a.severity == Severity.HIGH)}")
    print(f"  - MEDIUM: {sum(1 for a in problematic if a.severity == Severity.MEDIUM)}")

    # Print detailed report
    print("\n" + "=" * 80)
    print("DETAILED REPORT - Problematic Slides (sorted by severity)")
    print("=" * 80)

    for i, analysis in enumerate(problematic, 1):
        print(f"\n{i}. Slide #{analysis.slide_num} (lines {analysis.line_start}-{analysis.line_end})")
        print(f"   Severity: {analysis.severity.value}")
        print(f"   Current classes: layout='{analysis.layout_class}', compact='{analysis.compact_class}'")
        print(f"   Content: {analysis.content_chars} characters, {analysis.element_count} elements")
        print(f"   Issue: {analysis.issue_description}")
        print(f"   Fix: {analysis.recommended_fix}")

    # Save detailed report to file
    with open("/home/cuzic/ai-dev-yodoq/slides/density_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write("INFORMATION DENSITY ANALYSIS REPORT\n")
        f.write("=" * 80 + "\n")
        f.write(f"\nTotal slides analyzed: {len(analyses)}\n")
        f.write(f"Problematic slides found: {len(problematic)}\n\n")

        for i, analysis in enumerate(problematic, 1):
            f.write(f"\n{i}. Slide #{analysis.slide_num} (lines {analysis.line_start}-{analysis.line_end})\n")
            f.write(f"   Severity: {analysis.severity.value}\n")
            f.write(f"   Current classes: layout='{analysis.layout_class}', compact='{analysis.compact_class}'\n")
            f.write(f"   Content: {analysis.content_chars} characters, {analysis.element_count} elements\n")
            f.write(f"   Issue: {analysis.issue_description}\n")
            f.write(f"   Fix: {analysis.recommended_fix}\n")
            f.write(f"   Content preview:\n")
            f.write("   " + "-" * 76 + "\n")
            preview = analysis.raw_content[:500].replace("\n", "\n   ")
            f.write(f"   {preview}\n")
            f.write("   " + "-" * 76 + "\n")

    print("\n" + "=" * 80)
    print(f"Full report saved to: density_analysis_report.txt")

    # Return top problematic slides for fixing
    top_fixes = [a for a in problematic if a.severity in [Severity.CRITICAL, Severity.HIGH]][:15]

    print("\n" + "=" * 80)
    print(f"TOP {len(top_fixes)} SLIDES TO FIX:")
    print("=" * 80)

    for i, analysis in enumerate(top_fixes, 1):
        print(f"{i}. Slide #{analysis.slide_num}: {analysis.compact_class} -> "
              f"{analysis.recommended_fix.split('Change to ')[1].split(' ')[0] if 'Change to' in analysis.recommended_fix else 'review'}")

    # Save fixes mapping
    with open("/home/cuzic/ai-dev-yodoq/slides/density_fixes.txt", "w", encoding="utf-8") as f:
        f.write("SLIDES TO FIX (in priority order)\n")
        f.write("=" * 80 + "\n\n")
        for analysis in top_fixes:
            f.write(f"Slide #{analysis.slide_num} (lines {analysis.line_start}-{analysis.line_end}):\n")
            f.write(f"  Current: {analysis.compact_class}\n")
            f.write(f"  Fix: {analysis.recommended_fix}\n")
            f.write(f"  Content chars: {analysis.content_chars}\n\n")

    print(f"\nFix list saved to: density_fixes.txt")

if __name__ == "__main__":
    main()
