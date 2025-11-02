#!/usr/bin/env node
/**
 * Quick slide measurement - simplified version with shorter timeout
 */

const { chromium } = require('playwright');
const path = require('path');

async function quickMeasure(htmlPath) {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1280, height: 720 }
  });

  try {
    const fullPath = path.resolve(htmlPath);
    await page.goto(`file://${fullPath}`, {
      waitUntil: 'domcontentloaded',
      timeout: 10000
    });

    // Wait a bit for rendering
    await page.waitForTimeout(2000);

    const results = await page.evaluate(() => {
      const sections = Array.from(document.querySelectorAll('section'));
      const slideWidth = 1280;
      const slideHeight = 720;

      return sections.map((section, index) => {
        const rect = section.getBoundingClientRect();
        const elements = Array.from(section.querySelectorAll('*'));

        let maxOverflow = 0;
        let overflowElements = [];

        elements.forEach(el => {
          const elRect = el.getBoundingClientRect();
          const rightOverflow = (elRect.left + elRect.width) - (rect.left + slideWidth);
          const bottomOverflow = (elRect.top + elRect.height) - (rect.top + slideHeight);

          if (rightOverflow > 5) {
            maxOverflow = Math.max(maxOverflow, rightOverflow);
            overflowElements.push({ tag: el.tagName, right: Math.round(rightOverflow) });
          }
          if (bottomOverflow > 5) {
            maxOverflow = Math.max(maxOverflow, bottomOverflow);
            overflowElements.push({ tag: el.tagName, bottom: Math.round(bottomOverflow) });
          }
        });

        const compactClass = section.className.match(/\b(ultracompact|supercompact|compact)\b/)?.[1] || 'normal';

        return {
          index: index + 1,
          overflow: Math.round(maxOverflow),
          hasOverflow: maxOverflow > 30,
          compactClass,
          overflowCount: overflowElements.length
        };
      });
    });

    console.log('='.repeat(80));
    console.log('QUICK SLIDE MEASUREMENT RESULTS');
    console.log('='.repeat(80));

    const overflowSlides = results.filter(r => r.hasOverflow);
    const totalSlides = results.length;

    console.log(`\nTotal slides: ${totalSlides}`);
    console.log(`Overflow slides (>30px): ${overflowSlides.length} (${(overflowSlides.length/totalSlides*100).toFixed(1)}%)`);
    console.log(`Clean slides: ${totalSlides - overflowSlides.length} (${((totalSlides-overflowSlides.length)/totalSlides*100).toFixed(1)}%)`);

    if (overflowSlides.length > 0) {
      console.log('\n' + '='.repeat(80));
      console.log('SLIDES WITH OVERFLOW (>30px):');
      console.log('='.repeat(80));
      console.log('Slide | Overflow | Compact Class | Elements');
      console.log('-'.repeat(80));

      overflowSlides
        .sort((a, b) => b.overflow - a.overflow)
        .forEach(slide => {
          console.log(
            `${String(slide.index).padStart(5)} | ${String(slide.overflow + 'px').padStart(8)} | ${slide.compactClass.padEnd(13)} | ${slide.overflowCount}`
          );
        });

      // Show top 15 worst
      console.log('\n' + '='.repeat(80));
      console.log('TOP 15 WORST OVERFLOW SLIDES (PRIORITY FIXES):');
      console.log('='.repeat(80));

      overflowSlides
        .sort((a, b) => b.overflow - a.overflow)
        .slice(0, 15)
        .forEach((slide, idx) => {
          console.log(`${idx + 1}. Slide ${slide.index}: ${slide.overflow}px overflow (${slide.compactClass})`);
        });
    } else {
      console.log('\n✅ All slides are within limits! No overflow issues found.');
    }

  } catch (error) {
    console.error('Error during measurement:', error.message);
  } finally {
    await browser.close();
  }
}

// Run
const htmlFile = process.argv[2] || 'index.html';
quickMeasure(htmlFile).catch(console.error);
