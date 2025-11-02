#!/usr/bin/env node
/**
 * Check actual GitHub Pages deployment for overflow issues
 */

const { chromium } = require('playwright');

async function checkGitHubPages() {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1280, height: 720 }
  });

  try {
    const url = 'https://cuzic.github.io/ai-dev-yodoq/';
    console.log(`Accessing: ${url}`);

    await page.goto(url, {
      waitUntil: 'networkidle',
      timeout: 30000
    });

    // Wait for slides to render
    await page.waitForTimeout(3000);

    // Check if CSS is loaded
    const cssLoaded = await page.evaluate(() => {
      const sections = document.querySelectorAll('section');
      if (sections.length === 0) return false;

      const firstSection = sections[0];
      const styles = window.getComputedStyle(firstSection);
      return styles.width !== '' && styles.height !== '';
    });

    console.log('CSS loaded:', cssLoaded);

    // Get basic info
    const info = await page.evaluate(() => {
      const sections = Array.from(document.querySelectorAll('section'));

      // Check for compact/supercompact/ultracompact classes
      const compactClasses = {
        compact: 0,
        supercompact: 0,
        ultracompact: 0,
        normal: 0
      };

      sections.forEach(section => {
        if (section.classList.contains('compact')) compactClasses.compact++;
        else if (section.classList.contains('supercompact')) compactClasses.supercompact++;
        else if (section.classList.contains('ultracompact')) compactClasses.ultracompact++;
        else compactClasses.normal++;
      });

      // Check first slide's computed styles
      const firstSlide = sections[0];
      const firstStyles = window.getComputedStyle(firstSlide);

      return {
        totalSlides: sections.length,
        compactClasses,
        firstSlideStyles: {
          fontSize: firstStyles.fontSize,
          lineHeight: firstStyles.lineHeight,
          width: firstStyles.width,
          height: firstStyles.height,
          padding: firstStyles.padding,
          classes: Array.from(firstSlide.classList)
        }
      };
    });

    console.log('\n=== Basic Info ===');
    console.log('Total slides:', info.totalSlides);
    console.log('Compact classes:', info.compactClasses);
    console.log('\nFirst slide styles:', info.firstSlideStyles);

    // Measure overflow
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
            overflowElements.push({ tag: el.tagName, class: el.className, right: Math.round(rightOverflow) });
          }
          if (bottomOverflow > 5) {
            maxOverflow = Math.max(maxOverflow, bottomOverflow);
            overflowElements.push({ tag: el.tagName, class: el.className, bottom: Math.round(bottomOverflow) });
          }
        });

        const compactClass = section.className.match(/\b(ultracompact|supercompact|compact)\b/)?.[1] || 'normal';
        const computedStyles = window.getComputedStyle(section);

        return {
          index: index + 1,
          overflow: Math.round(maxOverflow),
          hasOverflow: maxOverflow > 30,
          compactClass,
          fontSize: computedStyles.fontSize,
          lineHeight: computedStyles.lineHeight,
          overflowElements: overflowElements.slice(0, 3) // First 3 overflow elements
        };
      });
    });

    console.log('\n=== Overflow Analysis ===');
    const overflowSlides = results.filter(r => r.hasOverflow);
    console.log(`Total slides: ${results.length}`);
    console.log(`Overflow slides (>30px): ${overflowSlides.length} (${(overflowSlides.length/results.length*100).toFixed(1)}%)`);
    console.log(`Clean slides: ${results.length - overflowSlides.length} (${((results.length-overflowSlides.length)/results.length*100).toFixed(1)}%)`);

    if (overflowSlides.length > 0) {
      console.log('\n=== Top 10 Worst Overflow ===');
      overflowSlides
        .sort((a, b) => b.overflow - a.overflow)
        .slice(0, 10)
        .forEach((slide, idx) => {
          console.log(`${idx + 1}. Slide ${slide.index}: ${slide.overflow}px (${slide.compactClass}, fontSize: ${slide.fontSize})`);
          if (slide.overflowElements.length > 0) {
            console.log('   Overflow elements:', slide.overflowElements);
          }
        });
    }

    // Take screenshot of first overflow slide
    if (overflowSlides.length > 0) {
      const firstOverflow = overflowSlides.sort((a, b) => b.overflow - a.overflow)[0];
      await page.evaluate((slideIndex) => {
        const sections = document.querySelectorAll('section');
        if (sections[slideIndex - 1]) {
          sections[slideIndex - 1].scrollIntoView();
        }
      }, firstOverflow.index);

      await page.waitForTimeout(500);
      await page.screenshot({ path: 'slides/.logs/github_pages_overflow.png', fullPage: false });
      console.log('\nScreenshot saved: slides/.logs/github_pages_overflow.png');
    }

  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
}

checkGitHubPages().catch(console.error);
