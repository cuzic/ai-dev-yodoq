/**
 * Marp HTML Validation Script
 *
 * Validates that the generated Marp HTML meets expected structure and content requirements.
 *
 * Usage:
 *   node validate_marp_html.js <html-file-path>
 *
 * Example:
 *   node validate_marp_html.js ../docs/index.html
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ANSI color codes for terminal output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  bold: '\x1b[1m'
};

// Test results tracking
const results = {
  passed: [],
  failed: [],
  warnings: []
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSection(title) {
  console.log('\n' + '='.repeat(80));
  log(title, 'bold');
  console.log('='.repeat(80));
}

function pass(testName, details = '') {
  results.passed.push(testName);
  log(`✅ PASS: ${testName}`, 'green');
  if (details) log(`   ${details}`, 'cyan');
}

function fail(testName, details = '') {
  results.failed.push(testName);
  log(`❌ FAIL: ${testName}`, 'red');
  if (details) log(`   ${details}`, 'yellow');
}

function warn(testName, details = '') {
  results.warnings.push(testName);
  log(`⚠️  WARN: ${testName}`, 'yellow');
  if (details) log(`   ${details}`, 'cyan');
}

async function validateMarpHTML(htmlPath) {
  logSection('Marp HTML Validation');
  log(`Testing: ${htmlPath}`, 'cyan');

  // Check file exists
  if (!fs.existsSync(htmlPath)) {
    fail('File existence check', `File not found: ${htmlPath}`);
    return;
  }
  pass('File existence check', `File found: ${htmlPath}`);

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // Track network errors
  const networkErrors = [];
  page.on('response', response => {
    if (!response.ok() && response.url().includes('.svg')) {
      networkErrors.push({ url: response.url(), status: response.status() });
    }
  });

  // Load the HTML file
  const htmlUrl = `file://${path.resolve(htmlPath)}`;
  await page.goto(htmlUrl, { waitUntil: 'networkidle' });

  logSection('1. Basic Structure Tests');

  // Test 1: Check Marp container exists
  const marpContainer = await page.$('#marp');
  if (marpContainer) {
    pass('Marp container exists', 'Found #marp element');
  } else {
    fail('Marp container exists', 'Missing #marp element - not a valid Marp HTML');
  }

  // Test 2: Count slides (section elements)
  const slideCount = await page.$$eval('section', sections => sections.length);
  if (slideCount > 1) {
    pass('Multiple slides exist', `Found ${slideCount} slides`);
  } else if (slideCount === 1) {
    fail('Multiple slides exist', `Only 1 slide found - page separators (---) may be missing`);
  } else {
    fail('Multiple slides exist', 'No slides found');
  }

  // Test 3: Check for expected minimum slides
  const expectedMinSlides = 50; // Based on day1_1.md through day2_2.md
  if (slideCount >= expectedMinSlides) {
    pass('Sufficient slide count', `${slideCount} slides >= ${expectedMinSlides} expected`);
  } else if (slideCount > 1) {
    warn('Sufficient slide count', `${slideCount} slides < ${expectedMinSlides} expected`);
  } else {
    fail('Sufficient slide count', `${slideCount} slides << ${expectedMinSlides} expected`);
  }

  logSection('2. SVG Diagram Tests');

  // Test 4: Count SVG images
  const svgImages = await page.$$eval('img[src*=".svg"]', imgs =>
    imgs.map(img => ({ src: img.src, alt: img.alt }))
  );

  if (svgImages.length > 0) {
    pass('SVG images present', `Found ${svgImages.length} SVG references`);
  } else {
    fail('SVG images present', 'No SVG images found in HTML');
  }

  // Test 5: Check for newly created diagrams (01-48)
  const diagramPattern = /diagram_(\d+)_.*\.svg/;
  const foundDiagrams = svgImages
    .map(img => img.src.match(diagramPattern))
    .filter(match => match)
    .map(match => parseInt(match[1]));

  const expectedDiagrams = Array.from({ length: 48 }, (_, i) => i + 1)
    .filter(n => n !== 22 && n !== 27 && n !== 37); // Skip missing numbers

  const missingDiagrams = expectedDiagrams.filter(n => !foundDiagrams.includes(n));

  if (missingDiagrams.length === 0) {
    pass('All expected diagrams present', `Found all ${expectedDiagrams.length} diagrams`);
  } else if (missingDiagrams.length < 10) {
    warn('All expected diagrams present',
      `Missing ${missingDiagrams.length} diagrams: ${missingDiagrams.slice(0, 5).join(', ')}${missingDiagrams.length > 5 ? '...' : ''}`);
  } else {
    fail('All expected diagrams present',
      `Missing ${missingDiagrams.length} diagrams: ${missingDiagrams.slice(0, 10).join(', ')}...`);
  }

  // Test 6: Check for SVG loading errors
  if (networkErrors.length === 0) {
    pass('SVG loading errors', 'No 404 errors for SVG files');
  } else {
    fail('SVG loading errors',
      `${networkErrors.length} SVG files failed to load:\n   ${networkErrors.slice(0, 5).map(e => `${e.status} ${e.url}`).join('\n   ')}`);
  }

  logSection('3. Layout and Theme Tests');

  // Test 7: Check for theme CSS
  const hasTheme = await page.evaluate(() => {
    const styles = Array.from(document.styleSheets);
    return styles.some(sheet => {
      try {
        return Array.from(sheet.cssRules).some(rule =>
          rule.cssText && rule.cssText.includes('ai-seminar')
        );
      } catch (e) {
        return false;
      }
    });
  });

  if (hasTheme) {
    pass('Theme CSS applied', 'Found ai-seminar theme');
  } else {
    warn('Theme CSS applied', 'ai-seminar theme may not be properly loaded');
  }

  // Test 8: Check for custom layout classes
  const layoutClasses = [
    'layout-horizontal-left',
    'layout-horizontal-right',
    'layout-diagram-only'
  ];

  const foundLayouts = await page.evaluate((classes) => {
    return classes.filter(cls => document.querySelector(`section.${cls}`));
  }, layoutClasses);

  if (foundLayouts.length === layoutClasses.length) {
    pass('Custom layout classes', `Found all ${layoutClasses.length} layout classes`);
  } else if (foundLayouts.length > 0) {
    warn('Custom layout classes',
      `Found ${foundLayouts.length}/${layoutClasses.length} layout classes: ${foundLayouts.join(', ')}`);
  } else {
    fail('Custom layout classes', 'No custom layout classes found');
  }

  logSection('4. Content Structure Tests');

  // Test 9: Check for headings
  const headingCount = await page.$$eval('section h1, section h2, section h3',
    headings => headings.length
  );

  if (headingCount > slideCount * 0.5) {
    pass('Heading distribution', `${headingCount} headings across ${slideCount} slides`);
  } else {
    warn('Heading distribution', `Only ${headingCount} headings for ${slideCount} slides`);
  }

  // Test 10: Check for list content
  const listItemCount = await page.$$eval('section li', items => items.length);

  if (listItemCount > 50) {
    pass('List content present', `Found ${listItemCount} list items`);
  } else {
    warn('List content present', `Only ${listItemCount} list items found`);
  }

  logSection('5. Navigation Tests');

  // Test 11: Check ARIA attributes for navigation
  const hasNavigation = await page.evaluate(() => {
    const sections = Array.from(document.querySelectorAll('section'));
    return sections.some(section =>
      section.hasAttribute('aria-label') || section.hasAttribute('id')
    );
  });

  if (hasNavigation) {
    pass('Navigation attributes', 'Slides have navigation attributes');
  } else {
    warn('Navigation attributes', 'Limited navigation attributes found');
  }

  // Test 12: Check viewport meta tag
  const hasViewport = await page.$('meta[name="viewport"]');
  if (hasViewport) {
    pass('Viewport meta tag', 'Mobile-responsive viewport configured');
  } else {
    warn('Viewport meta tag', 'Missing viewport meta tag');
  }

  logSection('6. File Structure Analysis');

  // Test 13: Analyze all_slides.md for page separators
  const allSlidesPath = path.join(path.dirname(htmlPath), '../slides/all_slides.md');
  if (fs.existsSync(allSlidesPath)) {
    const content = fs.readFileSync(allSlidesPath, 'utf-8');
    const separatorCount = (content.match(/^---$/gm) || []).length;
    const expectedSlides = separatorCount + 1; // Separators + 1 = total slides

    if (Math.abs(slideCount - expectedSlides) <= 2) {
      pass('Page separator conversion',
        `${separatorCount} separators in MD → ${slideCount} slides in HTML (expected ~${expectedSlides})`);
    } else if (separatorCount === 0) {
      fail('Page separator conversion',
        `No page separators (---) found in all_slides.md! This explains single-page output.`);
    } else {
      warn('Page separator conversion',
        `${separatorCount} separators in MD → ${slideCount} slides in HTML (expected ~${expectedSlides})`);
    }
  }

  await browser.close();

  // Summary
  logSection('Test Summary');
  log(`Total tests: ${results.passed.length + results.failed.length + results.warnings.length}`, 'bold');
  log(`✅ Passed: ${results.passed.length}`, 'green');
  log(`⚠️  Warnings: ${results.warnings.length}`, 'yellow');
  log(`❌ Failed: ${results.failed.length}`, 'red');

  if (results.failed.length === 0) {
    log('\n🎉 All critical tests passed!', 'green');
    return 0;
  } else {
    log('\n💥 Some tests failed. Please review the issues above.', 'red');
    return 1;
  }
}

// Main execution
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: node validate_marp_html.js <html-file-path>');
  console.error('Example: node validate_marp_html.js ../docs/index.html');
  process.exit(1);
}

const htmlPath = args[0];

validateMarpHTML(htmlPath)
  .then(exitCode => process.exit(exitCode))
  .catch(error => {
    console.error('Error running validation:', error);
    process.exit(1);
  });
