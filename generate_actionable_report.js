const fs = require('fs');
const data = require('./slides/.logs/visual_density_report.json');

// Filter for actionable problematic slides (not empty separators, not lead slides)
const actionable = data.allSlides.filter(s =>
  s.severity !== 'OK' &&
  s.wordCount > 0 &&
  s.slideType !== 'lead' &&
  s.whitespacePercentage > 60
).sort((a, b) => b.whitespacePercentage - a.whitespacePercentage);

let output = 'ACTIONABLE PROBLEMATIC SLIDES (Non-lead, with content, >60% whitespace)\n';
output += '='.repeat(80) + '\n';
output += `Total: ${actionable.length} slides\n\n`;

actionable.forEach((s, i) => {
  output += `${i+1}. SLIDE ${s.slideNumber} - ${s.severity}\n`;
  output += `   Whitespace: ${s.whitespacePercentage.toFixed(1)}% | Coverage: ${s.contentCoverage.toFixed(1)}% | Quality: ${s.qualityScore.toFixed(1)}/100\n`;
  output += `   Content: ${s.wordCount} words, ${s.elementCounts.headings}h + ${s.elementCounts.paragraphs}p + ${s.elementCounts.listItems}li + ${s.elementCounts.images}img\n`;
  output += `   Classes: ${s.slideClasses.join(', ') || 'none'}\n`;
  output += `   Screenshot: slides/.logs/screenshots/slide_${String(s.slideNumber).padStart(3, '0')}.png\n`;
  output += '\n';
});

fs.writeFileSync('./slides/.logs/ACTIONABLE_SLIDES.txt', output);
console.log(`Generated report: ${actionable.length} actionable slides found`);
console.log('\nTop 10 most problematic (excluding lead/separators):');
actionable.slice(0, 10).forEach((s, i) => {
  console.log(`  ${i+1}. Slide ${s.slideNumber}: ${s.whitespacePercentage.toFixed(1)}% whitespace (${s.wordCount} words, ${s.slideClasses.join(', ') || 'no classes'})`);
});
