"""
Marp slide quality measurement tool

Measures viewport overflow, safe area invasion, and text density for Marp slides.
Adapted from slidectl measure.py to work with Marp's SVG structure.
"""
import asyncio
import json
from pathlib import Path
from typing import List, Dict, Literal, Optional
from dataclasses import dataclass, asdict
from playwright.async_api import async_playwright

# Constants
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
SAFE_AREA_MARGIN = 24
EPSILON = 1.0


@dataclass
class Violation:
    """Quality violation"""
    rule_id: str
    severity: Literal["FAIL", "WARN"]
    element: str
    position: Dict[str, float]
    message: str
    slide_number: int


@dataclass
class SlideMetrics:
    """Slide quality metrics"""
    slide_number: int
    slide_id: str
    slide_classes: str
    viewport_overflow_px: float
    safe_area_invasion_px: float
    text_density: float
    violations: List[Violation]
    severity: Literal["OK", "WARN", "FAIL"]


async def check_viewport_overflow(section, slide_num: int) -> tuple[List[Violation], float]:
    """Check for viewport boundary overflow"""
    violations = []
    max_overflow = 0.0

    # Get all visible elements in the section
    elements = await section.query_selector_all("*")

    for elem in elements:
        try:
            box = await elem.bounding_box()
            if not box:
                continue

            # Check viewport overflow
            overflow_left = max(0, -box["x"])
            overflow_right = max(0, box["x"] + box["width"] - VIEWPORT_WIDTH)
            overflow_top = max(0, -box["y"])
            overflow_bottom = max(0, box["y"] + box["height"] - VIEWPORT_HEIGHT)

            total_overflow = overflow_left + overflow_right + overflow_top + overflow_bottom
            max_overflow = max(max_overflow, total_overflow)

            if total_overflow > EPSILON:
                tag_name = await elem.evaluate("el => el.tagName")
                elem_id = await elem.get_attribute("id") or "unknown"

                violations.append(Violation(
                    rule_id="R-BOUND-OVF",
                    severity="FAIL",
                    element=f"{tag_name}#{elem_id}",
                    position={
                        "left": overflow_left,
                        "right": overflow_right,
                        "top": overflow_top,
                        "bottom": overflow_bottom,
                    },
                    message=f"Viewport overflow: L={overflow_left:.1f}, R={overflow_right:.1f}, T={overflow_top:.1f}, B={overflow_bottom:.1f}",
                    slide_number=slide_num,
                ))
        except Exception:
            continue

    return violations, max_overflow


async def check_safe_area_invasion(section, slide_num: int) -> tuple[List[Violation], float]:
    """Check for safe area invasion"""
    violations = []
    max_invasion = 0.0

    safe_left = SAFE_AREA_MARGIN
    safe_right = VIEWPORT_WIDTH - SAFE_AREA_MARGIN
    safe_top = SAFE_AREA_MARGIN
    safe_bottom = VIEWPORT_HEIGHT - SAFE_AREA_MARGIN

    # Check text elements
    text_elements = await section.query_selector_all("h1, h2, h3, h4, h5, h6, p, li, span, div")

    for elem in text_elements:
        try:
            box = await elem.bounding_box()
            if not box:
                continue

            # Calculate invasion
            invade_left = max(0, safe_left - box["x"])
            invade_right = max(0, box["x"] + box["width"] - safe_right)
            invade_top = max(0, safe_top - box["y"])
            invade_bottom = max(0, box["y"] + box["height"] - safe_bottom)

            invasion = max(invade_left, invade_right, invade_top, invade_bottom)
            max_invasion = max(max_invasion, invasion)

            if invasion > 4:
                severity = "FAIL"
            elif invasion > EPSILON:
                severity = "WARN"
            else:
                continue

            text_content = await elem.text_content()
            if text_content:
                text_content = text_content[:30].strip()

            violations.append(Violation(
                rule_id="R-SAFE-INVADE",
                severity=severity,
                element=f'text: "{text_content}..."',
                position={
                    "left": invade_left,
                    "right": invade_right,
                    "top": invade_top,
                    "bottom": invade_bottom,
                },
                message=f"Safe Area invasion: {invasion:.1f}dp",
                slide_number=slide_num,
            ))
        except Exception:
            continue

    return violations, max_invasion


async def calculate_text_density(section) -> float:
    """Calculate text density as ratio of text area to slide area"""
    try:
        slide_area = VIEWPORT_WIDTH * VIEWPORT_HEIGHT

        # Get all text elements
        text_elements = await section.query_selector_all("h1, h2, h3, h4, h5, h6, p, li, span")

        total_text_area = 0.0
        for elem in text_elements:
            box = await elem.bounding_box()
            if box:
                total_text_area += box["width"] * box["height"]

        return total_text_area / slide_area if slide_area > 0 else 0.0
    except Exception:
        return 0.0


def calculate_severity(violations: List[Violation], overflow_px: float, invasion_px: float) -> Literal["OK", "WARN", "FAIL"]:
    """Calculate overall severity"""
    has_fail = any(v.severity == "FAIL" for v in violations)
    has_warn = any(v.severity == "WARN" for v in violations)

    if has_fail or overflow_px > 100:
        return "FAIL"
    elif has_warn or overflow_px > 50 or invasion_px > 4:
        return "WARN"
    else:
        return "OK"


async def measure_slides(html_file: Path) -> List[SlideMetrics]:
    """Measure all slides in HTML file"""
    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Load HTML
        await page.goto(f"file://{html_file.resolve()}")

        # Find all SVG slides (Marp structure)
        svgs = await page.query_selector_all("svg[data-marpit-svg]")
        print(f"Found {len(svgs)} slides")

        for idx, svg in enumerate(svgs):
            try:
                # Get foreignObject > section
                foreign_object = await svg.query_selector("foreignObject")
                if not foreign_object:
                    continue

                section = await foreign_object.query_selector("section")
                if not section:
                    continue

                # Get slide info
                slide_id = await section.get_attribute("id") or f"slide-{idx + 1}"
                slide_classes = await section.get_attribute("class") or ""

                # Run checks
                overflow_violations, max_overflow = await check_viewport_overflow(section, idx + 1)
                invasion_violations, max_invasion = await check_safe_area_invasion(section, idx + 1)
                text_density = await calculate_text_density(section)

                # Combine violations
                all_violations = overflow_violations + invasion_violations

                # Calculate severity
                severity = calculate_severity(all_violations, max_overflow, max_invasion)

                # Create metrics
                metrics = SlideMetrics(
                    slide_number=idx + 1,
                    slide_id=slide_id,
                    slide_classes=slide_classes,
                    viewport_overflow_px=max_overflow,
                    safe_area_invasion_px=max_invasion,
                    text_density=text_density,
                    violations=all_violations,
                    severity=severity,
                )

                results.append(metrics)

                # Progress
                if (idx + 1) % 20 == 0:
                    print(f"  Measured {idx + 1}/{len(svgs)} slides...")

            except Exception as e:
                print(f"  Error measuring slide {idx + 1}: {e}")
                continue

        await browser.close()

    return results


def save_results(results: List[SlideMetrics], output_file: Path):
    """Save results to JSON file"""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Convert to dict for JSON serialization
    data = {
        "total_slides": len(results),
        "summary": {
            "fail": sum(1 for r in results if r.severity == "FAIL"),
            "warn": sum(1 for r in results if r.severity == "WARN"),
            "ok": sum(1 for r in results if r.severity == "OK"),
        },
        "slides": [
            {
                **asdict(slide),
                "violations": [asdict(v) for v in slide.violations]
            }
            for slide in results
        ]
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def print_summary(results: List[SlideMetrics]):
    """Print summary statistics"""
    total = len(results)
    fail_count = sum(1 for r in results if r.severity == "FAIL")
    warn_count = sum(1 for r in results if r.severity == "WARN")
    ok_count = sum(1 for r in results if r.severity == "OK")

    print(f"\n{'='*60}")
    print("SLIDE QUALITY MEASUREMENT RESULTS")
    print(f"{'='*60}")
    print(f"Total slides: {total}")
    print(f"  FAIL: {fail_count} ({fail_count/total*100:.1f}%)")
    print(f"  WARN: {warn_count} ({warn_count/total*100:.1f}%)")
    print(f"  OK:   {ok_count} ({ok_count/total*100:.1f}%)")
    print(f"{'='*60}\n")

    # Show worst offenders
    fail_slides = [r for r in results if r.severity == "FAIL"]
    if fail_slides:
        print("Top 10 FAIL slides (by viewport overflow):")
        fail_slides_sorted = sorted(fail_slides, key=lambda x: x.viewport_overflow_px, reverse=True)[:10]
        for slide in fail_slides_sorted:
            print(f"  Slide {slide.slide_number}: {slide.viewport_overflow_px:.1f}px overflow, classes={slide.slide_classes}")


async def main():
    html_file = Path("/home/cuzic/ai-dev-yodoq/render/slides.html")
    output_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/initial_results.json")

    print("Starting slide quality measurement...")
    results = await measure_slides(html_file)

    print("Saving results...")
    save_results(results, output_file)

    print_summary(results)

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
