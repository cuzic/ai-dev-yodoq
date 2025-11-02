const fs = require('fs');
const path = require('path');
const playwright = require('playwright');

const METRICS_FILE = path.join(__dirname, 'slides/.logs/visual_metrics.json');
const REPORT_FILE = path.join(__dirname, 'slides/.logs/visual_density_report.json');
const MD_REPORT_FILE = path.join(__dirname, 'slides/.logs/VISUAL_DENSITY_ANALYSIS.md');
const ANNOTATED_DIR = path.join(__dirname, 'slides/.logs/screenshots/annotated');

// Ensure annotated directory exists
if (!fs.existsSync(ANNOTATED_DIR)) {
    fs.mkdirSync(ANNOTATED_DIR, { recursive: true });
}

function calculateDensityScore(metrics) {
    const {
        contentCoverage,
        whitespacePercentage,
        slideClasses,
        elementCounts,
        wordCount,
        charCount,
        textBounds,
        imageBounds
    } = metrics;

    // Determine slide type
    const isLeadSlide = slideClasses.includes('lead') || slideClasses.includes('title-slide');
    const isCompact = slideClasses.includes('compact');
    const hasLayout = slideClasses.some(c => c.startsWith('layout-'));
    const isDiagram = slideClasses.includes('diagram-slide');

    // Base content density score (0-100)
    let densityScore = contentCoverage;

    // Adjust for slide type
    if (isLeadSlide) {
        // Lead slides should have 15-30% coverage
        if (contentCoverage >= 15 && contentCoverage <= 30) {
            densityScore = 100; // Perfect for lead slide
        } else if (contentCoverage < 15) {
            densityScore = (contentCoverage / 15) * 100; // Too sparse
        } else {
            densityScore = 100 - ((contentCoverage - 30) / 70) * 30; // Too dense for lead
        }
    } else if (isDiagram) {
        // Diagram slides should have 50-80% coverage (large images)
        if (contentCoverage >= 50 && contentCoverage <= 80) {
            densityScore = 100;
        } else if (contentCoverage < 50) {
            densityScore = (contentCoverage / 50) * 100;
        } else {
            densityScore = 100 - ((contentCoverage - 80) / 20) * 20;
        }
    } else {
        // Regular slides should have 40-70% coverage
        if (contentCoverage >= 40 && contentCoverage <= 70) {
            densityScore = 100;
        } else if (contentCoverage < 40) {
            densityScore = (contentCoverage / 40) * 100;
        } else {
            densityScore = 100 - ((contentCoverage - 70) / 30) * 20;
        }
    }

    // Information richness score (based on content variety)
    let richnessScore = 0;
    richnessScore += Math.min(elementCounts.headings * 10, 20);
    richnessScore += Math.min(elementCounts.paragraphs * 5, 20);
    richnessScore += Math.min(elementCounts.listItems * 2, 20);
    richnessScore += Math.min(elementCounts.images * 15, 30);
    richnessScore += Math.min(elementCounts.codeBlocks * 10, 20);
    richnessScore += Math.min(elementCounts.tables * 15, 20);
    richnessScore += Math.min(wordCount / 5, 20);

    richnessScore = Math.min(richnessScore, 100);

    // Combined quality score
    const qualityScore = (densityScore * 0.6) + (richnessScore * 0.4);

    // Determine severity
    let severity = 'OK';
    let issue = null;

    if (isLeadSlide) {
        if (contentCoverage < 10) {
            severity = 'CRITICAL';
            issue = 'Extremely sparse lead slide';
        } else if (contentCoverage > 40) {
            severity = 'MEDIUM';
            issue = 'Lead slide too dense';
        }
    } else {
        if (whitespacePercentage > 70) {
            severity = 'CRITICAL';
            issue = 'Excessive whitespace (>70%)';
        } else if (whitespacePercentage > 60) {
            severity = 'HIGH';
            issue = 'High whitespace (60-70%)';
        } else if (whitespacePercentage > 50) {
            severity = 'MEDIUM';
            issue = 'Moderate whitespace (50-60%)';
        } else if (contentCoverage < 20) {
            severity = 'HIGH';
            issue = 'Very low content density (<20%)';
        } else if (contentCoverage < 30) {
            severity = 'MEDIUM';
            issue = 'Low content density (20-30%)';
        }
    }

    return {
        densityScore: Math.round(densityScore * 10) / 10,
        richnessScore: Math.round(richnessScore * 10) / 10,
        qualityScore: Math.round(qualityScore * 10) / 10,
        severity,
        issue,
        slideType: isLeadSlide ? 'lead' : (isDiagram ? 'diagram' : 'regular'),
        isCompact
    };
}

function analyzeSlides() {
    console.log('Reading metrics...');
    const metrics = JSON.parse(fs.readFileSync(METRICS_FILE, 'utf8'));

    console.log(`Analyzing ${metrics.length} slides...`);

    const analyzed = metrics.map(slide => {
        const analysis = calculateDensityScore(slide);
        return {
            ...slide,
            ...analysis
        };
    });

    // Sort by quality score (worst first)
    const problematicSlides = analyzed
        .filter(s => s.severity !== 'OK')
        .sort((a, b) => a.qualityScore - b.qualityScore);

    // Get top 30 worst slides
    const top30 = problematicSlides.slice(0, 30);

    // Statistics
    const stats = {
        totalSlides: analyzed.length,
        problematicSlides: problematicSlides.length,
        criticalSlides: analyzed.filter(s => s.severity === 'CRITICAL').length,
        highSeverity: analyzed.filter(s => s.severity === 'HIGH').length,
        mediumSeverity: analyzed.filter(s => s.severity === 'MEDIUM').length,
        averageContentCoverage: analyzed.reduce((sum, s) => sum + s.contentCoverage, 0) / analyzed.length,
        averageWhitespace: analyzed.reduce((sum, s) => sum + s.whitespacePercentage, 0) / analyzed.length,
        averageQualityScore: analyzed.reduce((sum, s) => sum + s.qualityScore, 0) / analyzed.length
    };

    const report = {
        generatedAt: new Date().toISOString(),
        statistics: stats,
        top30ProblematicSlides: top30,
        allSlides: analyzed
    };

    // Save JSON report
    fs.writeFileSync(REPORT_FILE, JSON.stringify(report, null, 2));
    console.log(`Report saved to ${REPORT_FILE}`);

    return report;
}

function generateMarkdownReport(report) {
    const { statistics, top30ProblematicSlides } = report;

    let md = '# Visual Density Analysis Report\n\n';
    md += `Generated: ${new Date(report.generatedAt).toLocaleString()}\n\n`;

    md += '## Executive Summary\n\n';
    md += `- **Total Slides Analyzed:** ${statistics.totalSlides}\n`;
    md += `- **Problematic Slides:** ${statistics.problematicSlides} (${((statistics.problematicSlides / statistics.totalSlides) * 100).toFixed(1)}%)\n`;
    md += `- **Critical Issues:** ${statistics.criticalSlides}\n`;
    md += `- **High Severity:** ${statistics.highSeverity}\n`;
    md += `- **Medium Severity:** ${statistics.mediumSeverity}\n`;
    md += `- **Average Content Coverage:** ${statistics.averageContentCoverage.toFixed(1)}%\n`;
    md += `- **Average Whitespace:** ${statistics.averageWhitespace.toFixed(1)}%\n`;
    md += `- **Average Quality Score:** ${statistics.averageQualityScore.toFixed(1)}/100\n\n`;

    md += '## Severity Levels\n\n';
    md += '- **CRITICAL:** >70% whitespace or extremely sparse lead slides (<10% coverage)\n';
    md += '- **HIGH:** 60-70% whitespace or very low content density (<20%)\n';
    md += '- **MEDIUM:** 50-60% whitespace or low content density (20-30%)\n';
    md += '- **OK:** Acceptable content density for slide type\n\n';

    md += '## Top 30 Problematic Slides\n\n';
    md += '| Rank | Slide | Severity | Quality Score | Whitespace % | Content % | Type | Issue | Recommendations |\n';
    md += '|------|-------|----------|---------------|--------------|-----------|------|-------|----------------|\n';

    top30ProblematicSlides.forEach((slide, index) => {
        const recommendations = generateRecommendations(slide);
        md += `| ${index + 1} | **${slide.slideNumber}** | ${slide.severity} | ${slide.qualityScore.toFixed(1)} | ${slide.whitespacePercentage.toFixed(1)}% | ${slide.contentCoverage.toFixed(1)}% | ${slide.slideType} | ${slide.issue || 'N/A'} | ${recommendations} |\n`;
    });

    md += '\n## Detailed Analysis\n\n';

    top30ProblematicSlides.forEach((slide, index) => {
        md += `### ${index + 1}. Slide ${slide.slideNumber} - ${slide.severity}\n\n`;
        md += `- **Quality Score:** ${slide.qualityScore.toFixed(1)}/100\n`;
        md += `- **Content Coverage:** ${slide.contentCoverage.toFixed(1)}%\n`;
        md += `- **Whitespace:** ${slide.whitespacePercentage.toFixed(1)}%\n`;
        md += `- **Density Score:** ${slide.densityScore.toFixed(1)}/100\n`;
        md += `- **Richness Score:** ${slide.richnessScore.toFixed(1)}/100\n`;
        md += `- **Type:** ${slide.slideType} ${slide.isCompact ? '(compact)' : ''}\n`;
        md += `- **Classes:** ${slide.slideClasses.join(', ')}\n`;
        md += `- **Word Count:** ${slide.wordCount}\n`;
        md += `- **Elements:** ${slide.elementCounts.headings}h + ${slide.elementCounts.paragraphs}p + ${slide.elementCounts.listItems}li + ${slide.elementCounts.images}img\n`;
        md += `- **Screenshot:** \`${slide.screenshotPath}\`\n`;
        md += `- **Issue:** ${slide.issue || 'N/A'}\n\n`;

        const recommendations = generateRecommendations(slide);
        md += `**Recommendations:**\n${recommendations}\n\n`;
        md += '---\n\n';
    });

    md += '## Content Coverage Distribution\n\n';
    const ranges = [
        { label: '0-10%', min: 0, max: 10 },
        { label: '10-20%', min: 10, max: 20 },
        { label: '20-30%', min: 20, max: 30 },
        { label: '30-40%', min: 30, max: 40 },
        { label: '40-50%', min: 40, max: 50 },
        { label: '50-60%', min: 50, max: 60 },
        { label: '60-70%', min: 60, max: 70 },
        { label: '70-80%', min: 70, max: 80 },
        { label: '80-90%', min: 80, max: 90 },
        { label: '90-100%', min: 90, max: 100 }
    ];

    ranges.forEach(range => {
        const count = report.allSlides.filter(s =>
            s.contentCoverage >= range.min && s.contentCoverage < range.max
        ).length;
        const bar = '█'.repeat(Math.round(count / 5));
        md += `- **${range.label}:** ${count} slides ${bar}\n`;
    });

    fs.writeFileSync(MD_REPORT_FILE, md);
    console.log(`Markdown report saved to ${MD_REPORT_FILE}`);
}

function generateRecommendations(slide) {
    const recs = [];

    if (slide.slideType === 'lead') {
        if (slide.contentCoverage < 10) {
            recs.push('Add subtitle or key message');
        } else if (slide.contentCoverage > 40) {
            recs.push('Reduce content - lead slides should be minimal');
        }
    } else {
        if (slide.whitespacePercentage > 60) {
            if (slide.elementCounts.listItems === 0) {
                recs.push('Add bullet points to fill space');
            }
            if (slide.elementCounts.images === 0) {
                recs.push('Add supporting diagram or image');
            }
            if (slide.wordCount < 50) {
                recs.push('Expand text content with more details');
            }
            if (slide.isCompact) {
                recs.push('Remove "compact" class to increase font sizes');
            }
        }

        if (slide.contentCoverage < 20) {
            recs.push('Consider merging with adjacent slide');
        }

        if (slide.elementCounts.headings > 0 && slide.elementCounts.paragraphs === 0 && slide.elementCounts.listItems === 0) {
            recs.push('Add body content below heading');
        }
    }

    if (recs.length === 0) {
        recs.push('Review layout and spacing');
    }

    return recs.join('; ');
}

async function createAnnotatedScreenshots(report) {
    console.log('\nCreating annotated screenshots for top 10 worst slides...');

    const top10 = report.top30ProblematicSlides.slice(0, 10);

    const browser = await playwright.chromium.launch({ headless: true });
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    const page = await context.newPage();

    const htmlPath = path.join(__dirname, 'index.html');
    await page.goto(`file://${htmlPath}`);
    await page.waitForTimeout(2000);

    for (const slide of top10) {
        console.log(`Annotating slide ${slide.slideNumber}...`);

        // Navigate to slide (Marp structure)
        await page.evaluate((index) => {
            const svgs = document.querySelectorAll('svg[data-marpit-svg]');
            if (svgs[index - 1]) {
                svgs[index - 1].scrollIntoView({ behavior: 'instant', block: 'start' });
            }
        }, slide.slideNumber);

        await page.waitForTimeout(500);

        // Draw annotations
        await page.evaluate((slideData) => {
            // Create canvas overlay
            const canvas = document.createElement('canvas');
            canvas.width = 1280;
            canvas.height = 720;
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.zIndex = '9999';
            canvas.style.pointerEvents = 'none';
            document.body.appendChild(canvas);

            const ctx = canvas.getContext('2d');

            // Draw content bounding boxes in green
            ctx.strokeStyle = 'rgba(0, 255, 0, 0.8)';
            ctx.lineWidth = 2;

            [...slideData.textBounds, ...slideData.imageBounds].forEach(bound => {
                ctx.strokeRect(bound.x, bound.y, bound.width, bound.height);
            });

            // Calculate and draw whitespace areas in red (simplified: just show coverage info)
            ctx.fillStyle = 'rgba(255, 0, 0, 0.1)';
            ctx.fillRect(0, 0, 1280, 720);

            // Add metrics overlay
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(10, 10, 400, 120);

            ctx.fillStyle = 'white';
            ctx.font = 'bold 16px Arial';
            ctx.fillText(`Slide ${slideData.slideNumber} - ${slideData.severity}`, 20, 35);

            ctx.font = '14px Arial';
            ctx.fillText(`Content Coverage: ${slideData.contentCoverage.toFixed(1)}%`, 20, 60);
            ctx.fillText(`Whitespace: ${slideData.whitespacePercentage.toFixed(1)}%`, 20, 80);
            ctx.fillText(`Quality Score: ${slideData.qualityScore.toFixed(1)}/100`, 20, 100);
            ctx.fillText(`Type: ${slideData.slideType}`, 20, 120);
        }, slide);

        // Take screenshot with annotations
        const annotatedPath = path.join(ANNOTATED_DIR, `slide_${String(slide.slideNumber).padStart(3, '0')}_annotated.png`);
        await page.screenshot({ path: annotatedPath, fullPage: false });

        // Remove canvas
        await page.evaluate(() => {
            const canvas = document.querySelector('canvas');
            if (canvas) canvas.remove();
        });

        console.log(`  Saved to ${annotatedPath}`);
    }

    await browser.close();
    console.log('✓ Annotated screenshots created!');
}

// Run analysis
async function main() {
    const report = analyzeSlides();
    generateMarkdownReport(report);
    await createAnnotatedScreenshots(report);

    console.log('\n' + '='.repeat(80));
    console.log('VISUAL DENSITY ANALYSIS COMPLETE');
    console.log('='.repeat(80));
    console.log(`\nTop 30 problematic slides identified out of ${report.statistics.totalSlides} total.`);
    console.log(`\nReports generated:`);
    console.log(`  - JSON: ${REPORT_FILE}`);
    console.log(`  - Markdown: ${MD_REPORT_FILE}`);
    console.log(`  - Annotated screenshots: ${ANNOTATED_DIR}`);
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error('Error:', error);
        process.exit(1);
    });
