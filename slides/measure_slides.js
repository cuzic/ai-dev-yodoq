#!/usr/bin/env node

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * Enhanced Playwright-based slide measurement tool
 * Measures: overflow, SVG embedding, whitespace ratio, density, overlaps
 * Inspired by slidectl's measure.py
 */

const SLIDE_WIDTH = 1280;
const SLIDE_HEIGHT = 720;

class SlideMeasurer {
  constructor() {
    this.results = [];
    this.summary = {
      totalSlides: 0,
      overflowSlides: 0,
      overlapSlides: 0,
      svgErrors: 0,
      avgDensity: 0,
      avgWhitespace: 0,
      avgOverlaps: 0
    };
  }

  async measure(htmlPath) {
    console.log('\n' + '='.repeat(80));
    console.log('Enhanced Slide Measurement Tool');
    console.log('='.repeat(80));
    console.log(`Testing: ${htmlPath}\n`);

    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width: SLIDE_WIDTH, height: SLIDE_HEIGHT }
    });
    const page = await context.newPage();

    // Track network errors for SVG loading
    const svgErrors = [];
    page.on('response', response => {
      if (!response.ok() && response.url().includes('.svg')) {
        svgErrors.push({
          url: response.url(),
          status: response.status()
        });
      }
    });

    await page.goto(`file://${path.resolve(htmlPath)}`);
    await page.waitForLoadState('networkidle');

    // Get all slides
    const slides = await page.$$('section');
    this.summary.totalSlides = slides.length;
    this.summary.svgErrors = svgErrors.length;

    console.log(`Found ${slides.length} slides to measure\n`);

    // Measure each slide
    for (let i = 0; i < slides.length; i++) {
      const metrics = await this.measureSlide(page, slides[i], i);
      this.results.push(metrics);

      // Print progress every 20 slides
      if ((i + 1) % 20 === 0) {
        console.log(`Progress: ${i + 1}/${slides.length} slides measured`);
      }
    }

    await browser.close();

    // Calculate summary statistics
    this.calculateSummary();

    // Print results
    this.printResults();

    // Save detailed results to file
    this.saveResults();

    return this.results;
  }

  async measureSlide(page, slideElement, index) {
    const metrics = {
      slideIndex: index,
      slideId: `slide_${String(index + 1).padStart(3, '0')}`,
      hasOverflow: false,
      overflowElements: [],
      overlaps: 0,
      overlapPairs: [],
      density: 0,
      whitespaceRatio: 0,
      svgCount: 0,
      svgLoadedCount: 0,
      textElements: 0,
      verdict: 'ok'
    };

    // Navigate to specific slide
    await page.evaluate((idx) => {
      const slides = document.querySelectorAll('section');
      if (slides[idx]) {
        slides[idx].scrollIntoView();
      }
    }, index);

    await page.waitForTimeout(100); // Small delay for rendering

    // Get slide bounding box
    const slideBox = await slideElement.boundingBox();
    if (!slideBox) {
      metrics.verdict = 'error';
      return metrics;
    }

    // Get all visible elements within slide
    const elements = await slideElement.$$('h1, h2, h3, h4, h5, h6, p, li, img, code, pre, span:not(:empty)');
    metrics.textElements = elements.length;

    const bboxes = [];
    const elementHandles = [];

    for (const element of elements) {
      const box = await element.boundingBox();
      if (!box) continue;

      const computedStyle = await element.evaluate(el => {
        const style = window.getComputedStyle(el);
        return {
          display: style.display,
          visibility: style.visibility,
          opacity: style.opacity,
          fontSize: style.fontSize,
          tagName: el.tagName.toLowerCase(),
          childCount: el.children.length,
          onlyChildIsImg: el.children.length === 1 && el.children[0].tagName === 'IMG'
        };
      });

      // Skip invisible elements
      if (computedStyle.visibility === 'hidden' || computedStyle.opacity === '0') {
        continue;
      }

      // Skip wrapper <p> tags that only contain an <img> (Marp wraps images in p tags)
      if (computedStyle.tagName === 'p' && computedStyle.onlyChildIsImg) {
        continue;
      }

      // Check if element is an SVG image
      const isSvg = computedStyle.tagName === 'img' && await element.evaluate(el => {
        return el.src && el.src.endsWith('.svg');
      });

      if (isSvg) {
        metrics.svgCount++;

        // Check if SVG loaded successfully
        const svgLoaded = await element.evaluate(el => {
          return el.complete && el.naturalWidth > 0;
        });

        if (svgLoaded) {
          metrics.svgLoadedCount++;
        }
      }

      // Convert to slide-relative coordinates
      const relativeBox = {
        x: box.x - slideBox.x,
        y: box.y - slideBox.y,
        width: box.width,
        height: box.height,
        element: computedStyle.tagName,
        fontSize: computedStyle.fontSize
      };

      bboxes.push(relativeBox);
      elementHandles.push(element);

      // Check for overflow
      const overflowRight = (relativeBox.x + relativeBox.width) > slideBox.width;
      const overflowBottom = (relativeBox.y + relativeBox.height) > slideBox.height;
      const overflowLeft = relativeBox.x < 0;
      const overflowTop = relativeBox.y < 0;

      if (overflowRight || overflowBottom || overflowLeft || overflowTop) {
        metrics.hasOverflow = true;
        metrics.overflowElements.push({
          element: computedStyle.tagName,
          overflowX: Math.max(0, (relativeBox.x + relativeBox.width) - slideBox.width),
          overflowY: Math.max(0, (relativeBox.y + relativeBox.height) - slideBox.height),
          direction: [
            overflowLeft ? 'left' : null,
            overflowRight ? 'right' : null,
            overflowTop ? 'top' : null,
            overflowBottom ? 'bottom' : null
          ].filter(Boolean).join(', ')
        });
      }
    }

    // Calculate density and whitespace
    if (bboxes.length > 0) {
      const slideArea = slideBox.width * slideBox.height;
      const totalElementArea = bboxes.reduce((sum, box) => sum + (box.width * box.height), 0);

      metrics.density = totalElementArea / slideArea;

      // Calculate union area using grid-based approach (like slidectl)
      const unionArea = this.calculateUnionArea(bboxes, slideBox.width, slideBox.height);
      metrics.whitespaceRatio = 1.0 - (unionArea / slideArea);
    } else {
      metrics.density = 0;
      metrics.whitespaceRatio = 1.0;
    }

    // Calculate overlaps
    const overlaps = this.calculateOverlaps(bboxes);
    metrics.overlaps = overlaps.length;
    metrics.overlapPairs = overlaps.slice(0, 5); // Store first 5 overlaps for reporting

    // Determine verdict
    if (metrics.hasOverflow || metrics.overlaps > 3 || metrics.density > 0.8) {
      metrics.verdict = 'ng';
    } else if (metrics.overlaps > 0 || metrics.density > 0.6) {
      metrics.verdict = 'warn';
    }

    return metrics;
  }

  calculateUnionArea(bboxes, slideWidth, slideHeight) {
    // Grid-based approximation for union area
    const gridSize = 10;
    const grid = new Set();

    for (const box of bboxes) {
      const startX = Math.floor(box.x / gridSize);
      const endX = Math.ceil((box.x + box.width) / gridSize);
      const startY = Math.floor(box.y / gridSize);
      const endY = Math.ceil((box.y + box.height) / gridSize);

      for (let x = startX; x < endX; x++) {
        for (let y = startY; y < endY; y++) {
          grid.add(`${x},${y}`);
        }
      }
    }

    return grid.size * (gridSize * gridSize);
  }

  calculateOverlaps(bboxes) {
    const overlaps = [];

    for (let i = 0; i < bboxes.length; i++) {
      for (let j = i + 1; j < bboxes.length; j++) {
        const box1 = bboxes[i];
        const box2 = bboxes[j];

        // Check if boxes intersect
        const xOverlap = Math.max(0, Math.min(box1.x + box1.width, box2.x + box2.width) - Math.max(box1.x, box2.x));
        const yOverlap = Math.max(0, Math.min(box1.y + box1.height, box2.y + box2.height) - Math.max(box1.y, box2.y));

        if (xOverlap > 0 && yOverlap > 0) {
          const overlapArea = xOverlap * yOverlap;
          const box1Area = box1.width * box1.height;
          const box2Area = box2.width * box2.height;

          // Only count significant overlaps (>5% of either element)
          if (overlapArea > 0.05 * Math.min(box1Area, box2Area)) {
            overlaps.push({
              element1: box1.element,
              element2: box2.element,
              area: Math.round(overlapArea)
            });
          }
        }
      }
    }

    return overlaps;
  }

  calculateSummary() {
    const totalDensity = this.results.reduce((sum, r) => sum + r.density, 0);
    const totalWhitespace = this.results.reduce((sum, r) => sum + r.whitespaceRatio, 0);
    const totalOverlaps = this.results.reduce((sum, r) => sum + r.overlaps, 0);

    this.summary.overflowSlides = this.results.filter(r => r.hasOverflow).length;
    this.summary.overlapSlides = this.results.filter(r => r.overlaps > 0).length;
    this.summary.avgDensity = totalDensity / this.results.length;
    this.summary.avgWhitespace = totalWhitespace / this.results.length;
    this.summary.avgOverlaps = totalOverlaps / this.results.length;
    this.summary.ngSlides = this.results.filter(r => r.verdict === 'ng').length;
    this.summary.warnSlides = this.results.filter(r => r.verdict === 'warn').length;
    this.summary.okSlides = this.results.filter(r => r.verdict === 'ok').length;
  }

  printResults() {
    console.log('\n' + '='.repeat(80));
    console.log('Summary Results');
    console.log('='.repeat(80));
    console.log(`Total slides:           ${this.summary.totalSlides}`);
    console.log(`SVG loading errors:     ${this.summary.svgErrors}`);
    console.log(`Slides with overflow:   ${this.summary.overflowSlides} (${(this.summary.overflowSlides / this.summary.totalSlides * 100).toFixed(1)}%)`);
    console.log(`Slides with overlaps:   ${this.summary.overlapSlides} (${(this.summary.overlapSlides / this.summary.totalSlides * 100).toFixed(1)}%)`);
    console.log(`Average density:        ${(this.summary.avgDensity * 100).toFixed(1)}%`);
    console.log(`Average whitespace:     ${(this.summary.avgWhitespace * 100).toFixed(1)}%`);
    console.log(`Average overlaps/slide: ${this.summary.avgOverlaps.toFixed(1)}`);
    console.log('');
    console.log(`Verdict breakdown:`);
    console.log(`  ✅ OK:       ${this.summary.okSlides} slides (${(this.summary.okSlides / this.summary.totalSlides * 100).toFixed(1)}%)`);
    console.log(`  ⚠️  WARNING: ${this.summary.warnSlides} slides (${(this.summary.warnSlides / this.summary.totalSlides * 100).toFixed(1)}%)`);
    console.log(`  ❌ NG:       ${this.summary.ngSlides} slides (${(this.summary.ngSlides / this.summary.totalSlides * 100).toFixed(1)}%)`);

    // Print problematic slides
    const problemSlides = this.results.filter(r => r.verdict === 'ng' || r.verdict === 'warn');

    if (problemSlides.length > 0) {
      console.log('\n' + '='.repeat(80));
      console.log('Problematic Slides (First 20)');
      console.log('='.repeat(80));

      for (const slide of problemSlides.slice(0, 20)) {
        const icon = slide.verdict === 'ng' ? '❌' : '⚠️';
        console.log(`\n${icon} Slide ${slide.slideIndex + 1} (${slide.slideId}):`);
        console.log(`   Density: ${(slide.density * 100).toFixed(1)}%, Whitespace: ${(slide.whitespaceRatio * 100).toFixed(1)}%`);

        if (slide.hasOverflow) {
          console.log(`   ⚠️  Overflow detected: ${slide.overflowElements.length} elements`);
          for (const overflow of slide.overflowElements.slice(0, 3)) {
            console.log(`      - ${overflow.element}: ${overflow.direction} (${overflow.overflowX}x${overflow.overflowY}px)`);
          }
        }

        if (slide.overlaps > 0) {
          console.log(`   ⚠️  Overlaps: ${slide.overlaps} pairs`);
          for (const overlap of slide.overlapPairs.slice(0, 3)) {
            console.log(`      - ${overlap.element1} ↔ ${overlap.element2} (${overlap.area}px²)`);
          }
        }

        if (slide.svgCount > 0 && slide.svgLoadedCount < slide.svgCount) {
          console.log(`   ⚠️  SVG loading issues: ${slide.svgLoadedCount}/${slide.svgCount} loaded`);
        }
      }

      if (problemSlides.length > 20) {
        console.log(`\n... and ${problemSlides.length - 20} more problematic slides (see detailed report)`);
      }
    }

    console.log('\n' + '='.repeat(80));
  }

  saveResults() {
    const reportPath = '/tmp/slide_measurement_report.json';
    const report = {
      timestamp: new Date().toISOString(),
      summary: this.summary,
      slides: this.results
    };

    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`Detailed report saved to: ${reportPath}`);

    // Also create a CSV for easy analysis
    const csvPath = '/tmp/slide_measurement_report.csv';
    const csvLines = [
      'slide_index,slide_id,verdict,has_overflow,overlaps,density,whitespace_ratio,svg_count,svg_loaded,elements'
    ];

    for (const slide of this.results) {
      csvLines.push([
        slide.slideIndex,
        slide.slideId,
        slide.verdict,
        slide.hasOverflow ? 1 : 0,
        slide.overlaps,
        slide.density.toFixed(4),
        slide.whitespaceRatio.toFixed(4),
        slide.svgCount,
        slide.svgLoadedCount,
        slide.textElements
      ].join(','));
    }

    fs.writeFileSync(csvPath, csvLines.join('\n'));
    console.log(`CSV report saved to: ${csvPath}`);
    console.log('='.repeat(80) + '\n');
  }
}

// Main execution
async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: node measure_slides.js <path-to-html>');
    console.error('Example: node measure_slides.js ../docs/index.html');
    process.exit(1);
  }

  const htmlPath = args[0];

  if (!fs.existsSync(htmlPath)) {
    console.error(`Error: File not found: ${htmlPath}`);
    process.exit(1);
  }

  const measurer = new SlideMeasurer();
  await measurer.measure(htmlPath);
}

main().catch(error => {
  console.error('Error during measurement:', error);
  process.exit(1);
});
