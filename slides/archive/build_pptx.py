#!/usr/bin/env python3
"""
Build script for AI Development Training PPTX with SVG support.
This script automates the entire build process:
1. Combine markdown files
2. Generate PPTX with Marp CLI
3. Replace PNG images with SVG files
"""

import os
import subprocess
import sys
import time
from pathlib import Path


# Color codes for terminal output
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    BOLD = "\033[1m"
    NC = "\033[0m"  # No Color


def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.NC}")
    print(f"{Colors.BLUE}{text:^60}{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.NC}\n")


def print_step(step_num, total_steps, text):
    """Print a formatted step."""
    print(f"{Colors.YELLOW}[{step_num}/{total_steps}] {text}{Colors.NC}")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.NC}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.NC}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}  {text}{Colors.NC}")


def check_dependencies():
    """Check if required dependencies are available."""
    print_step(0, 4, "Checking dependencies...")

    # Check for npx (Node.js)
    try:
        subprocess.run(["npx", "--version"], capture_output=True, check=True)
        print_success("Found npx")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("npx not found! Please install Node.js and npm")
        return False

    # Check for Python packages
    try:
        import xml.etree.ElementTree  # noqa: F401
        import zipfile  # noqa: F401

        print_success("Found required Python packages")
    except ImportError as e:
        print_error(f"Missing Python package: {e}")
        return False

    # Check for Chrome/Chromium
    chrome_path = os.environ.get("CHROME_PATH")
    if not chrome_path:
        # Try to find Chrome automatically
        possible_paths = [
            Path.home() / ".cache/ms-playwright/chromium-1194/chrome-linux/chrome",
            Path.home() / ".cache/puppeteer/chrome/*/chrome-linux64/chrome",
        ]

        for path_pattern in possible_paths:
            matches = list(Path(path_pattern.parent.parent).glob(path_pattern.name))
            if matches and matches[0].exists():
                chrome_path = str(matches[0])
                os.environ["CHROME_PATH"] = chrome_path
                break

        # Try system Chrome
        if not chrome_path:
            try:
                result = subprocess.run(["which", "chromium"], capture_output=True, text=True)
                if result.returncode == 0:
                    chrome_path = result.stdout.strip()
                    os.environ["CHROME_PATH"] = chrome_path
            except Exception:
                pass

        if not chrome_path:
            try:
                result = subprocess.run(["which", "google-chrome"], capture_output=True, text=True)
                if result.returncode == 0:
                    chrome_path = result.stdout.strip()
                    os.environ["CHROME_PATH"] = chrome_path
            except Exception:
                pass

    if chrome_path and Path(chrome_path).exists():
        print_success(f"Found Chrome: {chrome_path}")
    else:
        print_error("No suitable browser found!")
        print_info("Please install Chrome/Chromium or set CHROME_PATH")
        return False

    print()
    return True


def combine_markdown_files(markdown_files, output_file):
    """Combine multiple markdown files into one."""
    print_step(1, 4, "Combining markdown files...")

    combined_content = []
    for md_file in markdown_files:
        md_path = Path(md_file)
        if not md_path.exists():
            print_error(f"File not found: {md_file}")
            return False

        with open(md_path, encoding="utf-8") as f:
            combined_content.append(f.read())

    output_path = Path(output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(combined_content))

    # Count slides
    slide_count = combined_content[0].count("\n---\n")
    print_success(f"Combined {len(markdown_files)} files → {output_file}")
    print_info(f"Approximate slides: {slide_count}")
    print()

    return True


def generate_pptx_with_marp(markdown_file, output_file, timeout=600):
    """Generate PPTX using Marp CLI."""
    print_step(2, 4, "Generating PPTX with Marp CLI...")
    print_info("This may take several minutes...")

    cmd = [
        "npx",
        "-y",
        "@marp-team/marp-cli@latest",
        markdown_file,
        "--pptx",
        "--allow-local-files",
        "--image-scale",
        "1",
        "-o",
        output_file,
    ]

    try:
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=True)

        elapsed_time = time.time() - start_time

        # Print Marp output
        if result.stdout:
            for line in result.stdout.split("\n"):
                if line.strip():
                    print_info(line)

        if result.stderr:
            for line in result.stderr.split("\n"):
                if line.strip() and "WARN" in line:
                    print(f"  {Colors.YELLOW}{line}{Colors.NC}")

        if not Path(output_file).exists():
            print_error("PPTX file was not created")
            return False

        file_size = Path(output_file).stat().st_size / (1024 * 1024)
        print_success(f"Generated {output_file} ({file_size:.2f} MB in {elapsed_time:.1f}s)")
        print()

        return True

    except subprocess.TimeoutExpired:
        print_error(f"Marp generation timed out after {timeout}s")
        return False
    except subprocess.CalledProcessError as e:
        print_error("Marp generation failed")
        print_info(f"Error: {e.stderr}")
        return False


def replace_with_svg(input_pptx, output_pptx, svg_dir, markdown_file):
    """Replace PNG images with SVG files."""
    print_step(3, 4, "Replacing bitmap images with SVG...")

    try:
        # Import the replacement function
        from replace_with_svg import replace_images_with_svg

        replace_images_with_svg(
            pptx_path=input_pptx,
            svg_dir=svg_dir,
            output_path=output_pptx,
            markdown_path=markdown_file,
        )

        return True

    except Exception as e:
        print_error(f"SVG replacement failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def cleanup_temp_files(*files):
    """Remove temporary files."""
    print_step(4, 4, "Cleaning up temporary files...")

    for file in files:
        file_path = Path(file)
        if file_path.exists():
            file_path.unlink()
            print_info(f"Removed {file}")

    print()


def print_summary(final_pptx):
    """Print build summary."""
    pptx_path = Path(final_pptx)

    if not pptx_path.exists():
        print_error("Final PPTX not found!")
        return

    # Get file info
    file_size = pptx_path.stat().st_size / (1024 * 1024)

    # Count SVG files
    try:
        import zipfile

        with zipfile.ZipFile(pptx_path, "r") as z:
            svg_count = sum(1 for name in z.namelist() if name.endswith(".svg"))
    except Exception:
        svg_count = "?"

    print_header("✅ BUILD COMPLETE!")
    print(f"Output file:  {Colors.GREEN}{final_pptx}{Colors.NC}")
    print(f"File size:    {Colors.GREEN}{file_size:.2f} MB{Colors.NC}")
    print(f"SVG images:   {Colors.GREEN}{svg_count}{Colors.NC}")
    print(f"\n{Colors.YELLOW}💡 Tip: Open in PowerPoint 2019+ for best SVG rendering{Colors.NC}\n")


def main():
    """Main build process."""
    print_header("AI Development Training - PPTX Build Script")

    # Configuration
    markdown_files = ["day1_1.md", "day1_2.md", "day1_3.md", "day2_1.md", "day2_2.md"]
    combined_md = "all_slides.md"
    temp_pptx = "AI_Development_Training_2Days_temp.pptx"
    final_pptx = "AI_Development_Training_2Days.pptx"
    svg_dir = "diagrams"

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    try:
        # Check dependencies
        if not check_dependencies():
            sys.exit(1)

        # Step 1: Combine markdown files
        if not combine_markdown_files(markdown_files, combined_md):
            sys.exit(1)

        # Step 2: Generate PPTX with Marp
        if not generate_pptx_with_marp(combined_md, temp_pptx):
            sys.exit(1)

        # Step 3: Replace with SVG
        if not replace_with_svg(temp_pptx, final_pptx, svg_dir, combined_md):
            sys.exit(1)

        # Step 4: Cleanup
        cleanup_temp_files(temp_pptx)

        # Print summary
        print_summary(final_pptx)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Build interrupted by user{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
