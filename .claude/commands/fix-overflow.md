---
description: Fix slide overflow by intelligently reducing content while maintaining quality
---

# Slide Overflow Fixer

You are an expert at optimizing slide content to eliminate overflow while maintaining information quality and achieving high slide quality scores.

## Input Parameters

The user will provide a slide number. If not provided, ask which slide number to fix.

## Workflow

Execute the following 4-step workflow:

### STEP 1: PLAN - Analyze and Calculate Target Metrics

1. **Read the slide content**:
   - Extract the slide from `slides/all_slides.md` (split by `\n---\n`)
   - Identify layout class, heading, content structure

2. **Measure current state**:
   ```bash
   cd slides
   npx @marp-team/marp-cli all_slides.md --html --allow-local-files --no-stdin --theme-set ../assets/themes/ai-seminar.css -o ../docs/index.html
   node measure_slides.js ../docs/index.html
   ```
   Extract metrics for the target slide from `/tmp/slide_measurement_report.json`:
   - Current overflow (px)
   - Current density
   - Current whitespace_ratio
   - Content element count

3. **Calculate target metrics**:
   Based on the layout class and current overflow:

   - **Character budget per line**:
     - `compact`: ~80 chars/line
     - `supercompact`: ~90 chars/line
     - `ultracompact`: ~100 chars/line

   - **Line budget** (based on layout):
     - `layout-diagram-only`: 3-5 lines of text max
     - `layout-horizontal-left/right`: 5-8 bullet points max
     - `layout-callout`: 4-6 lines max
     - `card-grid`: 3-4 items per card, 2-3 lines per item
     - `lead`: 5-7 lines total

   - **Reduction target**:
     - If overflow > 300px: reduce content by 50%+
     - If overflow 200-300px: reduce content by 40%
     - If overflow 100-200px: reduce content by 30%
     - If overflow 50-100px: reduce content by 20%

4. **Create reduction plan**:
   - List specific bullets/paragraphs to shorten
   - Identify redundant phrases to remove
   - Note which key information must be preserved
   - Calculate target: X lines, Y characters per line

   **Output the plan clearly** before proceeding.

### STEP 2: REFACTOR - Reduce Content Intelligently

1. **Apply content reduction strategies** (in priority order):

   a. **Remove redundancy**:
      - Eliminate repeated concepts
      - Merge similar bullet points
      - Remove filler words (「重要」「非常に」など)

   b. **Simplify expressions**:
      - 「〜することができる」→「〜できる」
      - 「〜を実行する」→「〜する」
      - Long explanations → concise phrases

   c. **Use abbreviations and symbols**:
      - 「ドキュメント」→「Doc」
      - 「コミット」→「commit」
      - Lists: use shorter forms

   d. **Prioritize essential information**:
      - Keep: Core concepts, specific examples, actionable items
      - Remove: Background context, obvious statements, excessive detail

2. **Preserve slide quality**:
   - Maintain parallel structure in lists
   - Keep key terminology consistent
   - Ensure logical flow
   - Don't sacrifice clarity for brevity

3. **Edit the slide file**:
   - Use the Edit tool to update the specific slide in the appropriate `day*.md` file
   - Maintain exact formatting (markdown, class declarations, image links)
   - Stay within target line/character counts

### STEP 3: VERIFY - Confirm Overflow is Fixed

1. **Regenerate all_slides.md**:
   ```python
   from pathlib import Path

   output = ["---", "marp: true", "theme: ai-seminar", "paginate: true", "---", ""]
   day_files = ['day1_1.md', 'day1_2.md', 'day1_3.md', 'day2_1.md', 'day2_2.md']

   for day_file in day_files:
       content = Path(day_file).read_text()
       lines = content.split('\n')
       in_frontmatter = False
       frontmatter_count = 0
       content_lines = []

       for line in lines:
           if line.strip() == '---':
               frontmatter_count += 1
               if frontmatter_count == 1:
                   in_frontmatter = True
                   continue
               elif frontmatter_count == 2:
                   in_frontmatter = False
                   continue
           if not in_frontmatter and frontmatter_count >= 2:
               content_lines.append(line)

       output.extend(content_lines)
       output.append("")

   Path('all_slides.md').write_text('\n'.join(output))
   ```

2. **Rebuild HTML and measure**:
   ```bash
   npx @marp-team/marp-cli all_slides.md --html --allow-local-files --no-stdin --theme-set ../assets/themes/ai-seminar.css -o ../docs/index.html
   node measure_slides.js ../docs/index.html
   ```

3. **Verify success**:
   - Check target slide in `/tmp/slide_measurement_report.json`
   - Overflow should be < 30px (acceptable) or 0px (perfect)
   - If still overflowing > 30px, return to STEP 2 with more aggressive reduction

4. **Report verification results**:
   - Before: X px overflow, Y% density
   - After: X px overflow, Y% density
   - Status: ✅ FIXED / ⚠️ IMPROVED / ❌ STILL OVERFLOWING

### STEP 4: IMPROVE - Optimize for Quality Score

1. **Analyze quality metrics**:
   From the measurement report:
   - `density`: Content area / Slide area (target: 0.45-0.65)
   - `whitespaceRatio`: Empty space ratio (target: 0.35-0.55)
   - `overlaps`: Element overlaps (target: 0)
   - Overall verdict: ok / warn / ng

2. **Calculate quality score** (slidectl-style):
   ```
   Quality Score = (density * 0.4) + (whitespaceRatio * 0.3) + ((1 - overlaps/10) * 0.3)

   Ideal ranges:
   - density: 0.5-0.7 (50-70% of slide filled)
   - whitespaceRatio: 0.3-0.5 (30-50% empty space)
   - overlaps: 0 (no overlapping elements)
   ```

3. **Apply improvement strategies** based on metrics:

   a. **If density too low (<0.4)** - Add content:
      - Expand abbreviated terms slightly
      - Add 1-2 supporting bullet points
      - Include brief examples

   b. **If density too high (>0.7)** - Reduce more:
      - Further condense bullet points
      - Remove less critical items
      - Use more abbreviations

   c. **If whitespaceRatio too low (<0.3)** - Reduce content:
      - Remove 1-2 bullet points
      - Shorten text lines
      - Increase information density per line

   d. **If whitespaceRatio too high (>0.5)** - Add content:
      - Expand key concepts
      - Add examples or details
      - Unabbreviate some terms

4. **Fine-tune and rebuild**:
   - Make targeted edits to the day*.md file
   - Regenerate all_slides.md
   - Rebuild HTML
   - Re-measure

5. **Report final results**:
   ```
   Slide X Quality Report
   =====================
   Overflow: [before] → [after]
   Density: [before] → [after]
   Whitespace: [before] → [after]
   Quality Score: [score]/100
   Verdict: [ok/warn/ng]

   Improvements made:
   - [list specific changes]
   ```

## Important Guidelines

1. **Preserve meaning**: Never sacrifice accuracy for brevity
2. **Maintain structure**: Keep the slide's logical organization
3. **Test incrementally**: After each major change, rebuild and measure
4. **Document changes**: Explain what was reduced and why
5. **Respect limits**: Stay within the calculated character/line budgets
6. **Balance metrics**: Don't optimize one metric at the expense of others

## Example Reduction Patterns

**Before** (verbose):
```
- **AI時代のナビゲーター**: 方向を指示して、AIが実際の実装を行う
```

**After** (concise):
```
- **AI時代**: 方向指示、AIが実装
```

**Before** (redundant):
```
- コード生成を行う
- テストを実行する
- リファクタリングを実施する
- ドキュメントを作成する
```

**After** (consolidated):
```
- コード生成、テスト、リファクタリング、Doc作成
```

## Error Handling

- If slide number out of range: report error and ask for valid number
- If measurement fails: check that HTML was built correctly
- If overflow persists after 3 iterations: recommend manual content restructuring
- If quality score doesn't improve: revert to previous version and try different strategy

## Success Criteria

- ✅ Overflow < 30px
- ✅ Density: 0.45-0.65
- ✅ Whitespace: 0.35-0.55
- ✅ Overlaps: 0
- ✅ Content remains accurate and useful

Now, ask the user which slide number they want to fix, then execute the 4-step workflow.
