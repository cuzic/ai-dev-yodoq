#!/usr/bin/env python3
"""
Adjust font sizes in slides and rebuild HTML.
Usage:
    python adjust_fonts.py                    # Show current sizes
    python adjust_fonts.py small              # Apply small preset
    python adjust_fonts.py medium             # Apply medium preset
    python adjust_fonts.py large              # Apply large preset
    python adjust_fonts.py 18 32 24           # Custom: section h1 h2
"""

import subprocess
import sys
from pathlib import Path


PRESETS = {
    "small": {"section": 18, "h1": 32, "h2": 24, "horizontal": 16},
    "medium": {"section": 20, "h1": 36, "h2": 28, "horizontal": 18},
    "large": {"section": 24, "h1": 44, "h2": 36, "horizontal": 22},
}


def get_current_sizes():
    """Extract current font sizes from all_slides.md."""
    md_file = Path(__file__).parent / "all_slides.md"
    content = md_file.read_text(encoding="utf-8")

    sizes = {}
    lines = content.split("\n")

    for i, line in enumerate(lines):
        if "section {" in line and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if "font-size:" in next_line:
                size = next_line.split(":")[1].strip().rstrip(";")
                sizes["section"] = size

        if "h1 {" in line and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if "font-size:" in next_line:
                size = next_line.split(":")[1].strip().rstrip(";")
                sizes["h1"] = size

        if "h2 {" in line and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if "font-size:" in next_line:
                size = next_line.split(":")[1].strip().rstrip(";")
                sizes["h2"] = size

    return sizes


def update_font_sizes(section_size, h1_size, h2_size, horizontal_size=None):
    """Update font sizes in all_slides.md."""
    if horizontal_size is None:
        horizontal_size = int(section_size * 0.9)

    md_file = Path(__file__).parent / "all_slides.md"
    content = md_file.read_text(encoding="utf-8")

    # Get current sizes to replace
    current = get_current_sizes()

    # Replace section font-size
    content = content.replace(
        f"  section {{\n    font-size: {current.get('section', '20px')};",
        f"  section {{\n    font-size: {section_size}px;",
    )

    # Replace h1 font-size
    content = content.replace(
        f"  h1 {{\n    font-size: {current.get('h1', '36px')};",
        f"  h1 {{\n    font-size: {h1_size}px;",
    )

    # Replace h2 font-size
    content = content.replace(
        f"  h2 {{\n    font-size: {current.get('h2', '28px')};",
        f"  h2 {{\n    font-size: {h2_size}px;",
    )

    # Update horizontal layout sizes
    content = content.replace(
        "section.layout-horizontal-left > :not(h1):not(img) {\n    font-size: 18px;",
        f"section.layout-horizontal-left > :not(h1):not(img) {{\n    font-size: {horizontal_size}px;",
    )
    content = content.replace(
        "section.layout-horizontal-right > :not(h1):not(img) {\n    font-size: 18px;",
        f"section.layout-horizontal-right > :not(h1):not(img) {{\n    font-size: {horizontal_size}px;",
    )

    md_file.write_text(content, encoding="utf-8")
    print(
        f"✓ Updated: section={section_size}px, h1={h1_size}px, h2={h2_size}px, horizontal={horizontal_size}px"
    )


def build_html():
    """Build HTML slides from markdown."""
    print("📦 Building HTML slides...")
    try:
        subprocess.run(
            [
                "npx",
                "-y",
                "@marp-team/marp-cli@latest",
                "all_slides.md",
                "--html",
                "--allow-local-files",
                "-o",
                "index.html",
            ],
            cwd=Path(__file__).parent,
            check=True,
            capture_output=True,
            text=True,
        )
        # Copy to docs
        subprocess.run(
            ["cp", "index.html", "../docs/"],
            cwd=Path(__file__).parent,
            check=True,
        )
        print("✓ HTML slides built: slides/index.html and docs/index.html")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e.stderr}")
        return False


def main():
    if len(sys.argv) == 1:
        # Show current sizes
        sizes = get_current_sizes()
        print("Current font sizes:")
        print(f"  Section: {sizes.get('section', 'unknown')}")
        print(f"  H1:      {sizes.get('h1', 'unknown')}")
        print(f"  H2:      {sizes.get('h2', 'unknown')}")
        print("\nAvailable presets:", ", ".join(PRESETS.keys()))
        print("Usage:")
        print("  python adjust_fonts.py small              # Apply small preset")
        print("  python adjust_fonts.py 18 32 24           # Custom sizes")
        return

    arg1 = sys.argv[1]

    if arg1 in PRESETS:
        # Apply preset
        preset = PRESETS[arg1]
        print(f"Applying '{arg1}' preset...")
        update_font_sizes(
            preset["section"], preset["h1"], preset["h2"], preset["horizontal"]
        )
        build_html()
        print(f"\n✓ Done! Preview at: http://localhost:8000/index.html")
        print("  (Run: cd slides && python3 -m http.server)")
    elif len(sys.argv) == 4:
        # Custom sizes: section h1 h2
        try:
            section = int(sys.argv[1])
            h1 = int(sys.argv[2])
            h2 = int(sys.argv[3])
            print(f"Applying custom sizes: section={section}, h1={h1}, h2={h2}")
            update_font_sizes(section, h1, h2)
            build_html()
            print(f"\n✓ Done! Preview at: http://localhost:8000/index.html")
            print("  (Run: cd slides && python3 -m http.server)")
        except ValueError:
            print("✗ Invalid sizes. Use numbers only.")
            sys.exit(1)
    else:
        print("✗ Invalid arguments.")
        print("Usage:")
        print("  python adjust_fonts.py                    # Show current")
        print("  python adjust_fonts.py small              # Preset")
        print("  python adjust_fonts.py 18 32 24           # Custom")
        sys.exit(1)


if __name__ == "__main__":
    main()
