#!/usr/bin/env python3
"""
Unit tests for the build system.
Run with: python3 test_build.py
"""

import re
import sys
from pathlib import Path


class Colors:
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"


def test_result(passed, message):
    """Print test result."""
    if passed:
        print(f"  {Colors.GREEN}✓{Colors.NC} {message}")
        return True
    else:
        print(f"  {Colors.RED}✗{Colors.NC} {message}")
        return False


def test_suite():
    """Run all tests."""

    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.NC}")
    print(f"{Colors.BLUE}Build System Unit Tests{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.NC}\n")

    passed = 0
    failed = 0

    # Test 1: Source files exist
    print(f"{Colors.YELLOW}[1] Testing source files...{Colors.NC}")
    markdown_files = ["day1_1.md", "day1_2.md", "day1_3.md", "day2_1.md", "day2_2.md"]
    for md_file in markdown_files:
        if test_result(Path(md_file).exists(), f"{md_file} exists"):
            passed += 1
        else:
            failed += 1

    # Test 2: Build scripts exist
    print(f"\n{Colors.YELLOW}[2] Testing build scripts...{Colors.NC}")
    scripts = ["build_pptx.py", "build_pptx.sh", "replace_with_svg.py", "Makefile"]
    for script in scripts:
        if test_result(Path(script).exists(), f"{script} exists"):
            passed += 1
        else:
            failed += 1

    # Test 3: Documentation exists
    print(f"\n{Colors.YELLOW}[3] Testing documentation...{Colors.NC}")
    docs = ["README.md", "QUICKSTART.md", "BUILD_SUMMARY.md", "BUILD_FLOW.txt"]
    for doc in docs:
        if test_result(Path(doc).exists(), f"{doc} exists"):
            passed += 1
        else:
            failed += 1

    # Test 4: Python dependencies
    print(f"\n{Colors.YELLOW}[4] Testing Python dependencies...{Colors.NC}")
    dependencies = [
        ("zipfile", "zipfile module"),
        ("xml.etree.ElementTree", "XML parser"),
        ("pathlib", "Path library"),
        ("re", "Regular expressions"),
        ("shutil", "File operations"),
    ]
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            test_result(True, f"{description} available")
            passed += 1
        except ImportError:
            test_result(False, f"{description} missing")
            failed += 1

    # Test 5: SVG directory
    print(f"\n{Colors.YELLOW}[5] Testing SVG directory...{Colors.NC}")
    svg_dir = Path("diagrams")
    if test_result(svg_dir.exists() and svg_dir.is_dir(), "diagrams/ directory exists"):
        passed += 1

        svg_files = list(svg_dir.glob("*.svg"))
        if test_result(len(svg_files) > 0, f"Found {len(svg_files)} SVG files"):
            passed += 1
        else:
            failed += 1

        # Check for key diagrams
        key_diagrams = [
            "diagram_03_5step_flow.svg",
            "diagram_20_2day_summary.svg",
            "diagram_44_reverse_to_comprehensive_test.svg",
        ]
        for diagram in key_diagrams:
            diagram_path = svg_dir / diagram
            if test_result(diagram_path.exists(), f"{diagram} exists"):
                passed += 1
            else:
                failed += 1
    else:
        failed += 1

    # Test 6: Markdown structure
    print(f"\n{Colors.YELLOW}[6] Testing markdown structure...{Colors.NC}")
    combined_content = []
    for md_file in markdown_files:
        md_path = Path(md_file)
        if md_path.exists():
            with open(md_path, encoding="utf-8") as f:
                combined_content.append(f.read())

    content = "\n".join(combined_content)

    # Count slides
    slide_count = content.count("\n---\n")
    if test_result(slide_count > 100, f"Found {slide_count} slides (expected >100)"):
        passed += 1
    else:
        failed += 1

    # Count SVG references
    svg_refs = re.findall(r"!\[.*?\]\(diagrams/([^)]+\.svg)\)", content)
    if test_result(len(svg_refs) > 40, f"Found {len(svg_refs)} SVG references (expected >40)"):
        passed += 1
    else:
        failed += 1

    # Test 7: Module imports
    print(f"\n{Colors.YELLOW}[7] Testing module imports...{Colors.NC}")
    try:
        sys.path.insert(0, ".")
        from replace_with_svg import replace_images_with_svg  # noqa: F401

        test_result(True, "Successfully imported replace_with_svg")
        passed += 1
    except ImportError as e:
        test_result(False, f"Failed to import replace_with_svg: {e}")
        failed += 1

    # Test 8: File permissions
    print(f"\n{Colors.YELLOW}[8] Testing file permissions...{Colors.NC}")
    executables = ["build_pptx.py", "build_pptx.sh"]
    for exe in executables:
        exe_path = Path(exe)
        if exe_path.exists():
            is_executable = exe_path.stat().st_mode & 0o111
            if test_result(is_executable, f"{exe} is executable"):
                passed += 1
            else:
                failed += 1
        else:
            test_result(False, f"{exe} not found")
            failed += 1

    # Print summary
    total = passed + failed
    percentage = (passed / total * 100) if total > 0 else 0

    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.NC}")
    print(f"{Colors.BLUE}Test Summary{Colors.NC}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.NC}")
    print(f"Total tests:  {total}")
    print(f"{Colors.GREEN}Passed:       {passed}{Colors.NC}")
    if failed > 0:
        print(f"{Colors.RED}Failed:       {failed}{Colors.NC}")
    else:
        print(f"Failed:       {failed}")
    print(f"Success rate: {percentage:.1f}%")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.NC}\n")

    if failed == 0:
        print(f"{Colors.GREEN}✅ All tests passed! Build system is ready.{Colors.NC}\n")
        return 0
    else:
        print(f"{Colors.RED}❌ Some tests failed. Please fix the issues above.{Colors.NC}\n")
        return 1


if __name__ == "__main__":
    sys.exit(test_suite())
