# Before/After Examples - Information Density Fixes

## Example 1: Title Slide (Slide #116)
### Before (INAPPROPRIATE)
```markdown
<!-- _class: title supercompact -->

# Day 2-1: 振り返り + リバースエンジニアリング + テストシナリオ + テストコード基礎

## (10:00-12:00)
```
**Problem:** Only 63 characters but using supercompact (14px). Creates excessive whitespace.

### After (FIXED)
```markdown
<!-- _class: title -->

# Day 2-1: 振り返り + リバースエンジニアリング + テストシナリオ + テストコード基礎

## (10:00-12:00)
```
**Solution:** Changed to normal spacing. Title slide looks balanced and professional.

---

## Example 2: Section Divider (Slide #58)
### Before (INAPPROPRIATE)
```markdown
<!-- _class: lead ultracompact -->

## STEP4: 実装（40分）
```
**Problem:** Only 14 characters but using ultracompact (12px). Tiny text floating in whitespace.

### After (FIXED)
```markdown
<!-- _class: lead -->

## STEP4: 実装（40分）
```
**Solution:** Changed to normal spacing. Section divider now properly centered and readable.

---

## Example 3: Lead Slide (Slide #2)
### Before (INAPPROPRIATE)
```markdown
<!-- _class: lead compact -->

# AI活用研修：新規開発編

## 2日間で学ぶ、生産性を劇的に向上させる体系的アプローチ

AI駆動開発で開発期間を大幅短縮
```
**Problem:** Title slide with only 58 characters using compact class unnecessarily.

### After (FIXED)
```markdown
<!-- _class: lead -->

# AI活用研修：新規開発編

## 2日間で学ぶ、生産性を劇的に向上させる体系的アプローチ

AI駆動開発で開発期間を大幅短縮
```
**Solution:** Changed to normal spacing. Title properly displayed with good visual impact.

---

## Example 4: Section Header (Slide #128)
### Before (INAPPROPRIATE)
```markdown
<!-- _class: lead compact -->

## STEP2: フィットギャップ分析＆影響範囲調査

### （20分）
```
**Problem:** Only 30 characters but using compact class. Looks cramped.

### After (FIXED)
```markdown
<!-- _class: lead -->

## STEP2: フィットギャップ分析＆影響範囲調査

### （20分）
```
**Solution:** Changed to normal spacing. Better readability and visual balance.

---

## Visual Impact Summary

### Before Fixes
- ❌ 18 slides with unnecessary compression
- ❌ Tiny text floating in excessive whitespace
- ❌ Poor visual balance
- ❌ Inconsistent spacing across similar slide types

### After Fixes
- ✓ All 173 slides with appropriate spacing
- ✓ Consistent, professional appearance
- ✓ Better readability
- ✓ Proper visual hierarchy maintained

---

## Key Lesson Learned

**Compact classes should be used sparingly and only when truly needed:**
- Don't compress slides just because they're short
- Lead/title slides should almost always use normal spacing
- Section dividers look better with generous spacing
- Compression is for dense content, not sparse slides

**Rule of thumb:**
- <100 chars → Always use "normal"
- 100-200 chars → Consider "compact" only if multiple elements
- 200+ chars → May justify "supercompact" if very dense
- Never use compression on intentionally minimal slides
