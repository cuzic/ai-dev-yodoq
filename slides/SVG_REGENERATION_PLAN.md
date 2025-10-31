# SVG Regeneration Plan

## Status: Ready to Execute

This document outlines the plan to regenerate all 44 SVG diagrams with web-optimized designs.

## Problems with Current SVGs

1. **Font sizes too large**: 54-81px → unreadable when scaled down
2. **ViewBox mismatch**: 1170x1170 viewBox but 900x900 content → clipping issues
3. **Fixed layouts**: Designed for 1280x720 PPTX → doesn't scale to web
4. **Inconsistent styling**: Mix of inline styles and CSS classes

## Solution Approach

### Phase 1: Design System (COMPLETED)
- ✅ Created SVG_DESIGN_GUIDE.md with web-first principles
- ✅ Defined font hierarchy (24px/16px/14px)
- ✅ Standardized viewBox (800x600, 800x400, etc.)
- ✅ Created reusable templates for common patterns
- ✅ Generated example: diagram_01_ai_principles.svg

### Phase 2: Audit Current Diagrams (NEXT)

#### Diagram Categories

**1. Flow Diagrams (Horizontal)** - 800x400 viewBox
- diagram_03_5step_flow.svg
- diagram_08_er_to_code.svg
- diagram_24_incremental_timeline.svg
- diagram_25_ai_self_review_flow.svg
- diagram_27_refactoring_timing_in_tdd.svg

**2. Circular Diagrams** - 800x800 viewBox
- diagram_11_tdd_cycle.svg
- diagram_19_common_failures.svg (6 segments)

**3. Comparison Diagrams (Side-by-Side)** - 900x500 viewBox
- diagram_22_vibe_vs_production.svg
- diagram_41_mermaid_vs_svg.svg
- diagram_43_doc_automation_before_after.svg
- diagram_44_reverse_to_comprehensive_test.svg

**4. Matrix/Grid Diagrams** - 800x600 viewBox
- diagram_04_ai_memory.svg
- diagram_05_moscow.svg
- diagram_06_spec_structure.svg
- diagram_10_phase_breakdown.svg
- diagram_15_test_classification.svg
- diagram_18_fit_gap_analysis.svg
- diagram_28_claude_code_modes.svg
- diagram_30_prompt_patterns.svg
- diagram_31_user_story_mapping.svg
- diagram_32_nonfunctional_requirements.svg
- diagram_34_task_list_template.svg
- diagram_35_dependency_graph.svg
- diagram_38_jagged_intelligence_examples.svg
- diagram_39_reward_hacking_examples.svg

**5. Sequence Diagrams** - 800x600 viewBox
- diagram_09_sequence_login.svg
- diagram_14_scenario_to_code.svg

**6. Process Flow Diagrams** - 1000x700 viewBox
- diagram_12_reverse_engineering.svg
- diagram_13_impact_analysis.svg
- diagram_16_regression_prevention.svg
- diagram_17_workshop_workflow.svg
- diagram_26_test_coverage_80_rule.svg
- diagram_29_claudeignore_importance.svg
- diagram_37_five_step_detailed.svg
- diagram_40_transcript_approach.svg
- diagram_42_regression_mechanism.svg

**7. Summary/Overview Diagrams** - 1000x800 viewBox
- diagram_01_ai_principles.svg (DONE - example)
- diagram_02_role_change.svg
- diagram_07_er_diagram.svg
- diagram_20_2day_summary.svg
- diagram_21_learning_roadmap.svg
- diagram_23_security_best_practices.svg
- diagram_33_given_when_then.svg
- diagram_36_living_documentation.svg

### Phase 3: Generate AI Prompts

For each diagram, create a prompt like:

```markdown
Regenerate diagram_XX_name.svg as a web-optimized SVG.

**Pattern:** [Flow/Circular/Comparison/etc.]
**ViewBox:** 800x400
**Content:**
[Describe what the diagram shows]

**Elements:**
- [List all boxes, arrows, text]

**Requirements:**
- Font sizes: Title 24px, Body 16px, Labels 14px
- Colors: Navy (#00146E), Cyan (#00AFF0)
- CSS classes (no inline styles)
- Japanese text with Noto Sans JP
- Follows SVG_DESIGN_GUIDE.md patterns

Generate clean SVG code.
```

### Phase 4: Batch Generation

Create a script to:
1. Read each original SVG
2. Extract content structure
3. Apply appropriate template
4. Generate new web-optimized SVG
5. Save to diagrams-web/

### Phase 5: Validation

For each regenerated SVG:
- [ ] ViewBox matches content
- [ ] Font sizes 12-28px range
- [ ] No text clipping
- [ ] Colors accessible (WCAG AA)
- [ ] File size < 50KB
- [ ] Renders correctly in browser

### Phase 6: Integration

1. Test new SVGs in slides locally
2. Compare side-by-side with originals
3. Update all_slides.md to use diagrams-web/
4. Deploy to GitHub Pages
5. Verify on multiple devices

## Execution Strategy

### Option A: Manual (Slow but Accurate)
- Use AI to regenerate each diagram one-by-one
- Review each manually
- ~2-3 hours per diagram = 88-132 hours total

### Option B: Semi-Automated (Recommended)
1. Group by pattern (7 categories)
2. Create template for each pattern
3. Use AI to generate 5-6 examples per pattern
4. Batch-convert remaining with script
5. Manual review of ~30-40 diagrams
- ~30-40 hours total

### Option C: Fully Automated (Fast but Risky)
- Create conversion script
- Apply to all diagrams
- Review failures only
- ~10-15 hours total
- Risk: May need manual fixes

## Recommended: Option B (Semi-Automated)

**Week 1:**
- Days 1-2: Generate templates for 7 patterns (2 patterns/day)
- Days 3-5: Generate 2-3 example SVGs per pattern (15-20 total)

**Week 2:**
- Days 1-2: Create batch conversion script
- Days 3-4: Generate remaining 24 diagrams
- Day 5: Review, test, deploy

## Resources Needed

1. **AI Assistant** - For generating SVG code
2. **Browser** - For testing/validation
3. **Python** - For automation scripts
4. **Git** - For version control

## Success Metrics

- All 44 diagrams readable at 70% browser width
- Font sizes 12-28px (no larger)
- No clipping or overflow
- File sizes < 50KB each
- Consistent visual style
- Accessible colors (WCAG AA)

## Rollback Plan

If regeneration fails:
1. Keep original SVGs in diagrams/
2. New SVGs in diagrams-web/
3. Can switch back by updating image paths
4. Git history allows full revert

## Next Steps

1. **Decision Required**: Choose Option A, B, or C
2. **Resource Allocation**: Estimate time commitment
3. **Start with Examples**: Generate 5 more pattern examples
4. **Create Automation**: Build conversion scripts
5. **Batch Generate**: Process all 44 diagrams
6. **Test & Deploy**: Validate and push to production

## Appendix: Quick Start Command

```bash
# Generate all web-optimized SVGs
cd slides
python regenerate_all_svgs.py

# Preview locally
python3 -m http.server 8000

# Deploy to GitHub Pages
git add diagrams-web/ all_slides.md docs/
git commit -m "feat: Regenerate all SVGs with web-optimized designs"
git push
```

## Questions to Answer

1. Do we regenerate all 44 or start with top 10 most used?
2. Should we maintain both versions (PPTX and web)?
3. What's the acceptable time/quality tradeoff?
4. Can we parallelize with multiple AI sessions?

## References

- SVG_DESIGN_GUIDE.md - Design principles and patterns
- regenerate_svg_example.py - Example implementation
- diagrams-web/ - Output directory for new SVGs
