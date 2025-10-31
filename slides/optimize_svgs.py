#!/usr/bin/env python3
"""
Optimize SVG diagrams for web display by reducing font sizes.
This reduces font-size attributes by 40% to make them more readable on web.
"""

import re
from pathlib import Path


def optimize_svg(svg_path):
    """Reduce font sizes in SVG for better web display."""
    content = svg_path.read_text(encoding="utf-8")
    original = content

    # Find all font-size declarations and reduce by 40%
    def reduce_font_size(match):
        size = int(match.group(1))
        new_size = int(size * 0.6)  # Reduce to 60% of original
        return f"font-size: {new_size}px"

    # Replace in style definitions
    content = re.sub(r'font-size:\s*(\d+)px', reduce_font_size, content)

    # Also replace inline font-size
    content = re.sub(r'font-size=[""](\d+)[""]',
                     lambda m: f'font-size="{int(int(m.group(1)) * 0.6)}"',
                     content)

    if content != original:
        svg_path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    diagrams_dir = Path(__file__).parent.parent / "diagrams"

    print("Optimizing SVG diagrams for web display...")
    print("Reducing font sizes to 60% of original...")
    print()

    count = 0
    for svg_file in sorted(diagrams_dir.glob("*.svg")):
        if optimize_svg(svg_file):
            print(f"✓ Optimized: {svg_file.name}")
            count += 1
        else:
            print(f"  Skipped:   {svg_file.name} (no changes)")

    print()
    print(f"✓ Optimized {count} SVG files")
    print()
    print("Next steps:")
    print("  1. Review the changes: git diff diagrams/")
    print("  2. Rebuild HTML: python adjust_fonts.py small")
    print("  3. Preview: cd slides && python3 -m http.server")
    print("  4. Commit: git add diagrams/ && git commit -m 'fix: Optimize SVG font sizes'")


if __name__ == "__main__":
    main()
