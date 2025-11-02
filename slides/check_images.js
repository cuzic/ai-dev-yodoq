#!/usr/bin/env node

const { chromium } = require('playwright');
const path = require('path');

async function checkImages(htmlPath) {
  console.log('='.repeat(80));
  console.log('Image Link Checker');
  console.log('='.repeat(80));
  console.log(`Testing: ${htmlPath}\n`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  const page = await context.newPage();

  // Track all network requests
  const imageRequests = [];
  const failedImages = [];
  const successfulImages = [];

  page.on('response', response => {
    const url = response.url();

    // Check if it's an image
    if (url.match(/\.(svg|png|jpg|jpeg|gif|webp)$/i)) {
      imageRequests.push({
        url: url,
        status: response.status(),
        ok: response.ok()
      });

      if (!response.ok()) {
        failedImages.push({
          url: url,
          status: response.status()
        });
      } else {
        successfulImages.push(url);
      }
    }
  });

  await page.goto(`file://${path.resolve(htmlPath)}`);
  await page.waitForLoadState('networkidle');

  // Get all img tags
  const images = await page.$$('img');
  const imageInfo = [];

  for (const img of images) {
    const info = await img.evaluate(el => ({
      src: el.src,
      alt: el.alt,
      complete: el.complete,
      naturalWidth: el.naturalWidth,
      naturalHeight: el.naturalHeight
    }));
    imageInfo.push(info);
  }

  await browser.close();

  // Report
  console.log(`Total images found: ${images.length}`);
  console.log(`Successful loads: ${successfulImages.length}`);
  console.log(`Failed loads: ${failedImages.length}\n`);

  if (failedImages.length > 0) {
    console.log('❌ FAILED IMAGES:');
    console.log('='.repeat(80));
    for (const fail of failedImages) {
      console.log(`  ${fail.status} - ${fail.url}`);
    }
    console.log();
  }

  // Check for images that didn't load properly (0 dimensions)
  const unloadedImages = imageInfo.filter(img =>
    img.complete && img.naturalWidth === 0 && !img.src.includes('twemoji')
  );

  if (unloadedImages.length > 0) {
    console.log('⚠️  IMAGES WITH ZERO DIMENSIONS:');
    console.log('='.repeat(80));
    for (const img of unloadedImages) {
      console.log(`  ${img.src}`);
      console.log(`    Alt: ${img.alt}`);
    }
    console.log();
  }

  // Categorize images by type
  const svgImages = imageInfo.filter(img => img.src.includes('.svg'));
  const diagramImages = svgImages.filter(img => img.src.includes('/diagrams/'));
  const diagramWebImages = svgImages.filter(img => img.src.includes('/diagrams-web/'));
  const emojiImages = imageInfo.filter(img => img.src.includes('twemoji'));

  console.log('IMAGE BREAKDOWN:');
  console.log('='.repeat(80));
  console.log(`  Diagram SVGs (diagrams/):     ${diagramImages.length}`);
  console.log(`  Diagram SVGs (diagrams-web/): ${diagramWebImages.length}`);
  console.log(`  Emojis (twemoji CDN):         ${emojiImages.length}`);
  console.log(`  Total SVG images:             ${svgImages.length}`);
  console.log();

  // List all unique diagram files referenced
  const diagramFiles = new Set();
  for (const img of diagramImages) {
    const filename = img.src.split('/').pop();
    diagramFiles.add(filename);
  }

  const diagramWebFiles = new Set();
  for (const img of diagramWebImages) {
    const filename = img.src.split('/').pop();
    diagramWebFiles.add(filename);
  }

  console.log(`UNIQUE DIAGRAM FILES:`);
  console.log(`  diagrams/: ${diagramFiles.size} files`);
  console.log(`  diagrams-web/: ${diagramWebFiles.size} files`);
  console.log();

  // Check if all images loaded successfully
  const allLoaded = failedImages.length === 0 && unloadedImages.length === 0;

  if (allLoaded) {
    console.log('✅ ALL IMAGES LOADED SUCCESSFULLY!');
  } else {
    console.log('❌ SOME IMAGES FAILED TO LOAD');
  }
  console.log('='.repeat(80));

  return {
    total: images.length,
    successful: successfulImages.length,
    failed: failedImages.length,
    unloaded: unloadedImages.length,
    allLoaded: allLoaded,
    failedImages: failedImages,
    unloadedImages: unloadedImages
  };
}

// Main execution
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error('Usage: node check_images.js <path-to-html>');
  console.error('Example: node check_images.js ../docs/index.html');
  process.exit(1);
}

const htmlPath = args[0];

checkImages(htmlPath).then(result => {
  if (!result.allLoaded) {
    process.exit(1);
  }
}).catch(error => {
  console.error('Error during image checking:', error);
  process.exit(1);
});
