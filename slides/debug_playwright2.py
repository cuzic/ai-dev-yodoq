"""
Debug script to check Marp structure
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def debug_html():
    html_file = Path("/home/cuzic/ai-dev-yodoq/render/slides.html")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Load HTML
        await page.goto(f"file://{html_file.resolve()}")

        # Check for SVGs
        svgs = await page.query_selector_all("svg[data-marpit-svg]")
        print(f"Found {len(svgs)} SVG elements with data-marpit-svg")

        # Check first few SVGs
        for i, svg in enumerate(svgs[:3]):
            # Try to find foreignObject
            foreign_objects = await svg.query_selector_all("foreignObject")
            print(f"  SVG {i}: {len(foreign_objects)} foreignObject elements")

            for j, fo in enumerate(foreign_objects[:1]):
                # Find sections in foreignObject
                sections = await fo.query_selector_all("section")
                print(f"    foreignObject {j}: {len(sections)} section elements")

                if sections:
                    section = sections[0]
                    slide_id = await section.get_attribute("id")
                    classes = await section.get_attribute("class")
                    print(f"      Section: id={slide_id}, classes={classes}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_html())
