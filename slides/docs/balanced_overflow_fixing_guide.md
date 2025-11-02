# Balanced Overflow Fixing Guide

## Goal
Maximize overall slide quality score by balancing:
- ✅ Overflow elimination (<30px)
- ✅ Optimal density (0.50-0.70)
- ✅ Readability (preserve structure, clear language)
- ✅ Content richness (keep key information and examples)

## Content Budget by Layout and Compact Level

### Full-Content Layout
| Compact Level | Font | Max Lines | Chars/Line | Total Chars | Available Space |
|--------------|------|-----------|------------|-------------|-----------------|
| normal | 18px | 20 | 108 | 2160 | 1088x540px |
| compact | 16px | 24 | 120 | 2880 | 1088x540px |
| supercompact | 14px | 29 | 136 | 3944 | 1088x540px |
| ultracompact | 12px | 37 | 155 | 5735 | 1088x540px |

### Card-Grid Layout (per card)
| Compact Level | Font | Max Lines | Chars/Line | Total Chars | Available Space |
|--------------|------|-----------|------------|-------------|-----------------|
| normal | 18px | 9 | 53 | 477 | 537x251px |
| compact | 16px | 11 | 59 | 649 | 537x251px |
| supercompact | 14px | 13 | 67 | 871 | 537x251px |
| ultracompact | 12px | 17 | 76 | 1292 | 537x251px |

### Two-Column Layout (per column)
| Compact Level | Font | Max Lines | Chars/Line | Total Chars | Available Space |
|--------------|------|-----------|------------|-------------|-----------------|
| normal | 18px | 20 | 51 | 1020 | 512x540px |
| compact | 16px | 24 | 56 | 1344 | 512x540px |
| supercompact | 14px | 29 | 64 | 1856 | 512x540px |
| ultracompact | 12px | 37 | 73 | 2701 | 512x540px |

## Strategy by Overflow Severity

### Minor Overflow (30-80px)
- **Strategy**: Use `compact` class (16px font)
- **Content reduction**: 10-15%
- **Method**: Remove redundancy, simplify expressions
- **Keep**: Structure, headings, bullet points, key examples

### Moderate Overflow (80-150px)
- **Strategy**: Use `supercompact` class (14px font)
- **Content reduction**: 20-30%
- **Method**: Combine related points, use concise language
- **Keep**: Main structure, essential details, important context

### Severe Overflow (150-250px)
- **Strategy**: Use `supercompact` class + aggressive content reduction
- **Content reduction**: 35-45%
- **Method**: Restructure to compact format
- **Keep**: Key messages, essential information

### Critical Overflow (>250px)
- **Strategy**: Consider `ultracompact` class (12px) ONLY as last resort
- **Content reduction**: 40-50%
- **Method**: Major restructuring
- **Keep**: Core messages only
- **WARNING**: Use sparingly - readability suffers significantly at 12px

## Examples of Balanced Revisions

### Example 1: Card-Grid Checklist (Slide 104, day1_3.md)

**Original** (17 lines, overflowed):
```markdown
### STEP4: 実装
- ✅ TDD/BDD実装（Red-Green-Refactor）
- ✅ Given-When-Then形式テスト
- ✅ インクリメンタル開発
- ✅ 環境変数で秘密情報管理
- ✅ 入力値バリデーション
- ✅ AI自己レビュー実施
- ✅ 頻繁にコミット

### STEP5: 品質担保＆ドキュメント反映
- ✅ カバレッジ80%以上確認
- ✅ E2Eテスト実施
- ✅ AI観点別レビュー（一般・セキュリティ・パフォーマンス・テスト）
- ✅ 冗長・重複コード削除
- ✅ リファクタリング実施
- ✅ architecture.md生成
- ✅ README.md作成
- ✅ CLAUDE.md更新（成功パターン・ハマった点）
```

**Over-Aggressive (WRONG)** (2 lines, unreadable):
```markdown
**STEP4**: TDD/BDD, Given-When-Then, インクリメンタル, .env管理, バリデーション, AI自己レビュー, 頻繁commit
**STEP5**: カバレッジ80%+, E2E, AI観点別レビュー, リファクタ, Doc生成(arch.md/README/CLAUDE)
```

**Balanced (CORRECT)** (12 lines, readable):
```markdown
**STEP4: 実装**
- ✅ TDD/BDD (Red-Green-Refactor)
- ✅ Given-When-Then形式テスト
- ✅ インクリメンタル開発、頻繁commit
- ✅ 環境変数管理、入力値バリデーション
- ✅ AI自己レビュー実施

**STEP5: 品質担保＆Doc**
- ✅ カバレッジ80%+、E2Eテスト
- ✅ AI観点別レビュー4観点
- ✅ リファクタリング実施
- ✅ Doc生成 (arch/README/CLAUDE)
```
- Changed: ultracompact → supercompact (12px → 14px)
- Preserved: Structure (headings, bullets)
- Combined: Related items intelligently
- Fits: 12 lines in 13-line budget

### Example 2: Card-Grid Review Types (Slide 75, day1_2.md)

**Original** (4 detailed slides, ~60 lines total):
```markdown
# AI自己レビュー①一般レビュー
- **プロンプト:** 「このコードをレビューして。セキュリティ・エラー処理・エッジケース・ベストプラクティスをチェック」
- **検出:** ロジックエラー、エッジケース見落とし（null、空配列）、命名規則違反
- **効果:** バグ検出率向上
[...3 more similar slides...]
```

**Over-Aggressive (WRONG)** (4 lines, lost details):
```markdown
①**一般**(実装直後): セキュリティ・エラー処理・エッジケース・BP
②**セキュリティ**(認証・データ): OWASP Top10, SQLi・XSS・CSRF
③**パフォーマンス**(DB・大量データ): N+1・キャッシュ・インデックス
④**テストカバレッジ**(テスト後): エッジケース・異常系・境界値
```

**Balanced (CORRECT)** (9 lines, informative):
```markdown
### ①一般レビュー（毎回必須）
**検出:** ロジックエラー、エッジケース見落とし、命名規則違反

### ②セキュリティ特化
**検出:** SQLi・XSS・CSRF・平文PW・ハードコーディング

### ③パフォーマンス特化
**検出:** N+1クエリ、無駄な全件取得、キャッシュ未活用

### ④テストカバレッジ
**検出:** テストケース漏れ、異常系不足、境界値未検証
```
- Changed: ultracompact → supercompact
- Preserved: Section headings (###), key detection examples
- Fits: 9 lines in 13-line budget with room to spare

## Content Preservation Priorities

1. **Key concepts and main messages** (MUST keep)
2. **Important examples and context** (SHOULD keep)
3. **Structure** (headings, bullets) for scannability (SHOULD keep)
4. **Explanatory text and details** (CAN reduce/simplify)
5. **Redundant phrases and filler words** (SHOULD remove)

## What to AVOID

- ❌ Excessive abbreviations that harm comprehension
- ❌ Removing all structure (turning lists into comma-separated text)
- ❌ Eliminating important examples that aid understanding
- ❌ Using ultracompact (12px) as default solution
- ❌ Focusing only on overflow without considering density/readability

## What to PREFER

- ✅ Concise but complete language
- ✅ Combining related points intelligently
- ✅ Restructuring for efficiency while keeping meaning
- ✅ Balancing all quality metrics (overflow, density, readability)
- ✅ Using compact/supercompact progressively based on severity

## Compact Class Usage Guidelines

### When to use COMPACT (16px)
- Minor overflow (30-80px)
- Simple content that needs slight reduction
- Layouts with ample space (full-content, two-column)

### When to use SUPERCOMPACT (14px)
- Moderate to severe overflow (80-200px)
- Card-grid layouts with detailed content
- When combining items intelligently
- **DEFAULT CHOICE for most overflow situations**

### When to use ULTRACOMPACT (12px)
- Critical overflow (>250px) ONLY
- As absolute last resort
- When all other strategies fail
- **WARNING**: Readability suffers - use sparingly!

## Quality Metrics Targets

- **Overflow**: < 30px (strict requirement)
- **Density**: 0.50-0.70 (optimal: 0.60 - "full but not crowded")
- **Whitespace**: 0.30-0.50 (optimal: 0.40 - breathing room)
- **Overlaps**: 0 (no overlapping elements)

## Summary

The goal is NOT just to eliminate overflow, but to **maximize overall slide quality**. This means:

1. Calculate appropriate content budget for the layout and compact level
2. Choose the right compact level based on overflow severity
3. Reduce content intelligently while preserving structure and key information
4. Verify that density and readability are maintained
5. Prefer supercompact over ultracompact in most cases

Remember: **Readability and content value are just as important as fitting content on the slide!**
