# Slide RED - Phase 2: 判定処理作成

スライドが完成しているかを自動判定する処理を作成します。最初は何もできていないので失敗します（RED）。

## 実行タスク

### 1. 判定スクリプトの作成

スライド検証用のPythonスクリプトを作成：

```python
#!/usr/bin/env python3
"""
Slide validation script for Slide #[番号]

Validates that the slide meets all acceptance criteria.
"""

import re
import sys
from pathlib import Path

def validate_slide_[番号]() -> dict:
    """
    Validate slide #[番号]

    Returns:
        dict: {
            'passed': bool,
            'errors': list[str],
            'warnings': list[str],
            'metrics': dict
        }
    """
    errors = []
    warnings = []
    metrics = {}

    # Load all_slides.md
    slides_path = Path('all_slides.md')
    if not slides_path.exists():
        errors.append("all_slides.md not found")
        return {'passed': False, 'errors': errors, 'warnings': warnings, 'metrics': metrics}

    content = slides_path.read_text(encoding='utf-8')

    # Extract slides
    slides = re.split(r'\n---\n', content)

    # Find target slide (slide #[番号])
    if len(slides) < [番号]:
        errors.append(f"Slide #{[番号]} not found (only {len(slides)} slides exist)")
        return {'passed': False, 'errors': errors, 'warnings': warnings, 'metrics': metrics}

    slide_content = slides[[番号] - 1]

    # 1. Check layout class
    expected_layout = "[レイアウト名]"
    layout_match = re.search(r'<!--\s*_class:\s*(.+?)\s*-->', slide_content)
    actual_layout = layout_match.group(1).strip() if layout_match else None

    if actual_layout != expected_layout:
        errors.append(f"Layout mismatch: expected '{expected_layout}', got '{actual_layout}'")
    else:
        metrics['layout'] = actual_layout

    # 2. Check title
    title_match = re.search(r'^#\s+(.+)$', slide_content, re.MULTILINE)
    if not title_match:
        errors.append("Title (H1) not found")
    else:
        title = title_match.group(1).strip()
        if len(title) < 5:
            warnings.append(f"Title too short: '{title}'")
        metrics['title'] = title

    # 3. Check bullet points
    bullet_count = len(re.findall(r'^[-*]\s+', slide_content, re.MULTILINE))
    metrics['bullet_count'] = bullet_count

    if bullet_count < 3:
        warnings.append(f"Only {bullet_count} bullet points (recommended: 3-8)")
    elif bullet_count > 8:
        warnings.append(f"Too many bullet points: {bullet_count} (recommended: 3-8)")

    # 4. Check SVG diagram (if needed)
    svg_required = [True/False]  # PLANフェーズで決定
    has_svg = bool(re.search(r'!\[.*?\]\(diagrams/.*?\.svg\)', slide_content))

    if svg_required and not has_svg:
        errors.append("SVG diagram required but not found")

    metrics['has_svg'] = has_svg

    # 5. Check SVG overflow (if SVG exists)
    if has_svg:
        # Extract SVG path
        svg_match = re.search(r'!\[.*?\]\((diagrams/.*?\.svg)\)', slide_content)
        if svg_match:
            svg_path = Path(svg_match.group(1))
            if svg_path.exists():
                # Run validate_svg_bounds.py on this specific SVG
                # (Simplified check - full implementation would use the actual validator)
                from validate_svg_bounds import check_svg_bounds
                result = check_svg_bounds(svg_path)
                overflow = result.max_overflow_x + result.max_overflow_y
                metrics['svg_overflow'] = overflow

                if overflow > 10:
                    errors.append(f"SVG overflow: {overflow:.0f}px (must be < 10px)")
            else:
                errors.append(f"SVG file not found: {svg_path}")

    # 6. Calculate text density (simplified)
    text_chars = len(slide_content)
    metrics['text_chars'] = text_chars

    if text_chars > 800:
        warnings.append(f"High text density: {text_chars} chars")

    # Final result
    passed = len(errors) == 0

    return {
        'passed': passed,
        'errors': errors,
        'warnings': warnings,
        'metrics': metrics
    }


if __name__ == '__main__':
    result = validate_slide_[番号]()

    print("━" * 60)
    print(f"SLIDE #{[番号]} VALIDATION")
    print("━" * 60)
    print()

    if result['passed']:
        print("✅ PASSED")
    else:
        print("❌ FAILED")

    print()
    print(f"📊 Metrics:")
    for key, value in result['metrics'].items():
        print(f"  {key}: {value}")

    if result['errors']:
        print()
        print("❌ Errors:")
        for error in result['errors']:
            print(f"  - {error}")

    if result['warnings']:
        print()
        print("⚠️  Warnings:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    print()
    print("━" * 60)

    sys.exit(0 if result['passed'] else 1)
```

### 2. 判定スクリプトの保存

`validate_slide_[番号].py` として保存

### 3. 初回実行（失敗確認）

判定スクリプトを実行し、失敗することを確認：

```bash
python3 validate_slide_[番号].py
```

期待される出力（RED状態）:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLIDE #[番号] VALIDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ FAILED

📊 Metrics:
  (none - slide not created yet)

❌ Errors:
  - Slide #[番号] not found (only [N] slides exist)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. TodoList更新

判定処理作成タスクを完了としてマーク。

## 確認ポイント

- ✅ 判定スクリプトが作成されたか
- ✅ スクリプトが失敗したか（期待通りのRED状態）
- ✅ エラーメッセージが明確で分かりやすいか
- ✅ 受入条件が適切にコード化されているか

## 次のフェーズへ

ユーザーの確認を得てから、次のフェーズ（GREEN）へ進む。

GREENフェーズでは、この判定処理がパスする最低限のスライドを作成します。
