"""
Debug script to check what Playwright sees in the HTML
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

        # Check for sections
        sections = await page.query_selector_all("section")
        print(f"Found {len(sections)} section elements")

        # Check first few sections
        for i, section in enumerate(sections[:5]):
            slide_id = await section.get_attribute("id")
            classes = await section.get_attribute("class")
            print(f"  Section {i}: id={slide_id}, classes={classes}")

            # Check for SVG
            svg = await section.query_selector("svg")
            if svg:
                print(f"    Has SVG element")
            else:
                print(f"    No SVG element")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_html())
