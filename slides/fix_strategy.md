# Strategic Overflow Fixing - Quality Score Maximization

## Goal
Maximize overall quality score = Balance(overflow < 30px, density 0.5-0.7, readability, content richness)

## Current Status
- Total slides: 168
- Overflow slides: 48 (28.6%)
- Clean slides: 120 (71.4%)

## Overflow Categories

### Severe (>600px) - 6 slides - TOP PRIORITY
1. Slide 112 (879px): layout-code-focus - Code block + notes
2. Slide 90 (818px): card-grid - 5 key points
3. Slide 58 (770px): layout-timeline - 7 steps
4. Slide 98 (642px): card-grid - Exercise explanation
5. Slide 135 (641px): layout-callout - Test scenario explanation
6. Slide 154 (638px): card-grid - Multi-section content

**Strategy:**
- Use supercompact (14px) selectively
- Aggressive but intelligent condensing
- Preserve core educational value
- Target: Reduce to <200px or eliminate

### High (400-599px) - 3 slides
7. Slide 81 (590px): two-column - Refactoring
8. Slide 53 (582px): compact - Unknown content
9. Slide 9 (568px): two-column - Environment setup

**Strategy:**
- Use supercompact (14px)
- Moderate condensing
- Target: Reduce to <100px

### Moderate (200-399px) - 6 slides
10. Slide 116 (480px)
11. Slide 155 (438px)
12. Slide 141 (436px)
13. Slide 101 (432px)
14. Slide 82 (406px)
15. Slide 43 (350px)

**Strategy:**
- Keep compact (16px) if possible
- Smart condensing
- Target: Eliminate overflow

### Minor (30-199px) - 33 slides
**Strategy:**
- Keep compact (16px)
- Minor tweaks only
- Target: Eliminate overflow with minimal changes

## Quality Score Calculation
For each slide, evaluate:
- Overflow penalty: -10 points per 100px over 30px
- Density score: +100 points if 0.5-0.7, -50 if <0.4 or >0.8
- Readability score: +100 for compact, +50 for supercompact, 0 for ultracompact
- Content score: Subjective assessment of preserved educational value

**Target:** Maximize total score across all slides
