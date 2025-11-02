const playwright = require('playwright');
const fs = require('fs');
const path = require('path');

const VIEWPORT_WIDTH = 1280;
const VIEWPORT_HEIGHT = 720;
const OUTPUT_DIR = path.join(__dirname, 'slides/.logs/screenshots');
const METRICS_FILE = path.join(__dirname, 'slides/.logs/visual_metrics.json');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function measureSlideContent(page, slideIndex) {
    return await page.evaluate((index) => {
        // Marp uses SVG foreignObject structure
        const slides = document.querySelectorAll('svg[data-marpit-svg] foreignObject section');
        const slide = slides[index];
        if (!slide) return null;

        const slideRect = slide.getBoundingClientRect();
        const slideArea = slideRect.width * slideRect.height;

        // Get all visible text elements
        const textElements = Array.from(slide.querySelectorAll('h1, h2, h3, h4, h5, h6, p, li, span, div, td, th, code, pre, blockquote'))
            .filter(el => {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                const text = el.textContent.trim();

                // Only count elements with actual text content and visible area
                return text.length > 0 &&
                       rect.width > 0 &&
                       rect.height > 0 &&
                       style.display !== 'none' &&
                       style.visibility !== 'hidden' &&
                       style.opacity !== '0';
            });

        // Get all visible images
        const images = Array.from(slide.querySelectorAll('img, svg'))
            .filter(el => {
                const rect = el.getBoundingClientRect();
                const style = window.getComputedStyle(el);
                return rect.width > 0 &&
                       rect.height > 0 &&
                       style.display !== 'none' &&
                       style.visibility !== 'hidden';
            });

        // Calculate bounding boxes
        const textBounds = textElements.map(el => {
            const rect = el.getBoundingClientRect();
            return {
                x: rect.left - slideRect.left,
                y: rect.top - slideRect.top,
                width: rect.width,
                height: rect.height,
                text: el.textContent.trim().substring(0, 100)
            };
        });

        const imageBounds = images.map(el => {
            const rect = el.getBoundingClientRect();
            return {
                x: rect.left - slideRect.left,
                y: rect.top - slideRect.top,
                width: rect.width,
                height: rect.height,
                type: el.tagName.toLowerCase()
            };
        });

        // Calculate content area (using bounding box union)
        const allBounds = [...textBounds, ...imageBounds];
        let contentArea = 0;

        if (allBounds.length > 0) {
            // Simple approach: sum all element areas (may overlap)
            contentArea = allBounds.reduce((sum, bound) => sum + (bound.width * bound.height), 0);
        }

        // Get slide classes
        const slideClasses = Array.from(slide.classList);

        // Count elements
        const elementCounts = {
            headings: slide.querySelectorAll('h1, h2, h3, h4, h5, h6').length,
            paragraphs: slide.querySelectorAll('p').length,
            lists: slide.querySelectorAll('ul, ol').length,
            listItems: slide.querySelectorAll('li').length,
            images: images.length,
            codeBlocks: slide.querySelectorAll('pre, code').length,
            tables: slide.querySelectorAll('table').length,
            cards: slide.querySelectorAll('.card').length
        };

        // Calculate text statistics
        const allText = slide.textContent.trim();
        const wordCount = allText.split(/\s+/).filter(w => w.length > 0).length;
        const charCount = allText.length;

        return {
            slideWidth: slideRect.width,
            slideHeight: slideRect.height,
            slideArea,
            contentArea,
            textBounds,
            imageBounds,
            slideClasses,
            elementCounts,
            wordCount,
            charCount
        };
    }, slideIndex);
}

async function screenshotAllSlides() {
    console.log('Launching browser...');
    const browser = await playwright.chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: VIEWPORT_WIDTH, height: VIEWPORT_HEIGHT }
    });
    const page = await context.newPage();

    const htmlPath = path.join(__dirname, 'index.html');
    console.log(`Loading ${htmlPath}...`);

    await page.goto(`file://${htmlPath}`);

    // Wait for Marp slides to be ready
    await page.waitForFunction(() => {
        return document.querySelectorAll('svg[data-marpit-svg] foreignObject section').length > 0;
    }, { timeout: 10000 });

    await page.waitForTimeout(1000); // Additional wait for complete rendering

    // Get total number of slides (Marp structure)
    const totalSlides = await page.evaluate(() => {
        return document.querySelectorAll('svg[data-marpit-svg] foreignObject section').length;
    });

    console.log(`Total slides: ${totalSlides}`);

    const metrics = [];

    for (let i = 0; i < totalSlides; i++) {
        const slideNumber = i + 1;
        console.log(`Processing slide ${slideNumber}/${totalSlides}...`);

        // Scroll to slide (Marp structure)
        await page.evaluate((index) => {
            const svgs = document.querySelectorAll('svg[data-marpit-svg]');
            if (svgs[index]) {
                svgs[index].scrollIntoView({ behavior: 'instant', block: 'start' });
            }
        }, i);

        // Wait for rendering
        await page.waitForTimeout(300);

        // Get the SVG element bounds for screenshot
        const svgBounds = await page.evaluate((index) => {
            const svg = document.querySelectorAll('svg[data-marpit-svg]')[index];
            if (!svg) return null;
            const rect = svg.getBoundingClientRect();
            return {
                x: rect.left,
                y: rect.top,
                width: rect.width,
                height: rect.height
            };
        }, i);

        // Take screenshot of the specific slide
        const screenshotPath = path.join(OUTPUT_DIR, `slide_${String(slideNumber).padStart(3, '0')}.png`);
        if (svgBounds) {
            await page.screenshot({
                path: screenshotPath,
                clip: {
                    x: Math.round(svgBounds.x),
                    y: Math.round(svgBounds.y),
                    width: Math.round(svgBounds.width),
                    height: Math.round(svgBounds.height)
                }
            });
        } else {
            await page.screenshot({ path: screenshotPath, fullPage: false });
        }

        // Measure content
        const slideMetrics = await measureSlideContent(page, i);

        if (slideMetrics) {
            const contentCoverage = (slideMetrics.contentArea / slideMetrics.slideArea) * 100;
            const whitespacePercentage = 100 - contentCoverage;

            metrics.push({
                slideNumber,
                screenshotPath: screenshotPath.replace(__dirname, '.'),
                ...slideMetrics,
                contentCoverage,
                whitespacePercentage
            });

            console.log(`  Slide ${slideNumber}: ${contentCoverage.toFixed(1)}% content, ${whitespacePercentage.toFixed(1)}% whitespace`);
        } else {
            console.log(`  Warning: Could not measure slide ${slideNumber}`);
        }
    }

    // Save metrics to JSON
    fs.writeFileSync(METRICS_FILE, JSON.stringify(metrics, null, 2));
    console.log(`\nMetrics saved to ${METRICS_FILE}`);
    console.log(`Screenshots saved to ${OUTPUT_DIR}`);

    await browser.close();

    return metrics;
}

// Run the script
screenshotAllSlides()
    .then(() => {
        console.log('\n✓ Screenshot capture complete!');
        process.exit(0);
    })
    .catch(error => {
        console.error('Error:', error);
        process.exit(1);
    });
