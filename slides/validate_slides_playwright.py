#!/usr/bin/env python3
"""
スライド品質検証システム v2.0 - Playwright Edition

仕様v1.1に基づき、実際のブラウザレンダリング結果を検証
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from playwright.sync_api import sync_playwright, Page, ElementHandle

# 定数
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
SAFE_AREA_MARGIN = 24
EPSILON = 1.0  # 幾何誤差許容

@dataclass
class Violation:
    """違反レコード"""
    rule_id: str
    severity: str  # 'FAIL' or 'WARN'
    element: str
    position: Dict
    message: str
    slide_number: int

@dataclass
class SlideResult:
    """スライド評価結果"""
    slide_number: int
    title: str
    violations: List[Violation]
    status: str  # 'PASS', 'WARN', 'FAIL'

class SlideValidator:
    """スライド品質検証"""

    def __init__(self, page: Page):
        self.page = page
        self.results: List[SlideResult] = []

    def get_bounding_box(self, element: ElementHandle) -> Optional[Dict]:
        """要素の実際のbounding boxを取得"""
        try:
            box = element.bounding_box()
            return box
        except:
            return None

    def check_viewport_overflow(self, slide_num: int) -> List[Violation]:
        """R-BOUND-OVF: ViewPort境界超過チェック"""
        violations = []

        # すべての可視要素を取得
        elements = self.page.query_selector_all('svg text, svg rect, svg circle, svg path, svg image')

        for elem in elements:
            box = self.get_bounding_box(elem)
            if not box:
                continue

            # ViewPort超過チェック
            overflow_left = max(0, -box['x'])
            overflow_right = max(0, box['x'] + box['width'] - VIEWPORT_WIDTH)
            overflow_top = max(0, -box['y'])
            overflow_bottom = max(0, box['y'] + box['height'] - VIEWPORT_HEIGHT)

            total_overflow = overflow_left + overflow_right + overflow_top + overflow_bottom

            if total_overflow > EPSILON:
                elem_id = elem.get_attribute('id') or elem.get_attribute('class') or 'unknown'
                tag_name = elem.evaluate('el => el.tagName')

                violations.append(Violation(
                    rule_id='R-BOUND-OVF',
                    severity='FAIL',
                    element=f'{tag_name}#{elem_id}',
                    position={
                        'left': overflow_left,
                        'right': overflow_right,
                        'top': overflow_top,
                        'bottom': overflow_bottom
                    },
                    message=f'ViewPort超過: L={overflow_left:.1f}, R={overflow_right:.1f}, T={overflow_top:.1f}, B={overflow_bottom:.1f}',
                    slide_number=slide_num
                ))

        return violations

    def check_safe_area(self, slide_num: int) -> List[Violation]:
        """R-SAFE-INVADE: Safe Area侵入チェック"""
        violations = []

        safe_left = SAFE_AREA_MARGIN
        safe_right = VIEWPORT_WIDTH - SAFE_AREA_MARGIN
        safe_top = SAFE_AREA_MARGIN
        safe_bottom = VIEWPORT_HEIGHT - SAFE_AREA_MARGIN

        elements = self.page.query_selector_all('svg text')

        for elem in elements:
            box = self.get_bounding_box(elem)
            if not box:
                continue

            # Safe Area侵入度を計算
            invade_left = max(0, safe_left - box['x'])
            invade_right = max(0, box['x'] + box['width'] - safe_right)
            invade_top = max(0, safe_top - box['y'])
            invade_bottom = max(0, box['y'] + box['height'] - safe_bottom)

            max_invade = max(invade_left, invade_right, invade_top, invade_bottom)

            if max_invade > 4:
                severity = 'FAIL'
            elif max_invade > EPSILON:
                severity = 'WARN'
            else:
                continue

            elem_text = elem.text_content()[:30]
            violations.append(Violation(
                rule_id='R-SAFE-INVADE',
                severity=severity,
                element=f'text: "{elem_text}..."',
                position={
                    'left': invade_left,
                    'right': invade_right,
                    'top': invade_top,
                    'bottom': invade_bottom
                },
                message=f'Safe Area侵入: {max_invade:.1f}dp',
                slide_number=slide_num
            ))

        return violations

    def check_text_overlap(self, slide_num: int) -> List[Violation]:
        """R-TEXT-OVERLAP: テキスト重なりチェック"""
        violations = []

        texts = self.page.query_selector_all('svg text')
        boxes = []

        for text_elem in texts:
            box = self.get_bounding_box(text_elem)
            if box and box['width'] > 0 and box['height'] > 0:
                text_content = text_elem.text_content()
                boxes.append((box, text_elem, text_content))

        # 全ペアをチェック
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                box1, elem1, text1 = boxes[i]
                box2, elem2, text2 = boxes[j]

                # 重複領域を計算
                overlap_x = max(0, min(box1['x'] + box1['width'], box2['x'] + box2['width']) - max(box1['x'], box2['x']))
                overlap_y = max(0, min(box1['y'] + box1['height'], box2['y'] + box2['height']) - max(box1['y'], box2['y']))
                overlap_area = overlap_x * overlap_y

                if overlap_x >= 2 and overlap_y >= 2 and overlap_area >= 8:
                    # 意図的オーバーラップかチェック
                    has_allow_overlap = (
                        elem1.get_attribute('class') and 'allow-overlap' in elem1.get_attribute('class') or
                        elem2.get_attribute('class') and 'allow-overlap' in elem2.get_attribute('class')
                    )

                    severity = 'WARN' if has_allow_overlap else 'FAIL'

                    violations.append(Violation(
                        rule_id='R-TEXT-OVERLAP',
                        severity=severity,
                        element=f'"{text1[:20]}..." ⇔ "{text2[:20]}..."',
                        position={
                            'overlap_width': overlap_x,
                            'overlap_height': overlap_y,
                            'overlap_area': overlap_area
                        },
                        message=f'テキスト重なり: {overlap_x:.1f}×{overlap_y:.1f}dp ({overlap_area:.0f}dp²)',
                        slide_number=slide_num
                    ))

        return violations

    def check_container_overflow(self, slide_num: int) -> List[Violation]:
        """R-BOX-OVF: コンテナからのはみ出しチェック"""
        violations = []

        # rect内のtextをチェック
        rects = self.page.query_selector_all('svg rect')

        for rect in rects:
            rect_box = self.get_bounding_box(rect)
            if not rect_box:
                continue

            # このrectの近くにあるテキストを探す
            rect_id = rect.get_attribute('id') or rect.get_attribute('class') or ''

            # 同じ親グループ内のテキストを探す
            parent = rect.evaluate('el => el.parentElement')
            if parent:
                texts = self.page.evaluate('''(parent) => {
                    const texts = parent.querySelectorAll('text');
                    return Array.from(texts).map(t => t.textContent);
                }''', parent)

                text_elements = self.page.query_selector_all('svg text')
                for text_elem in text_elements:
                    text_box = self.get_bounding_box(text_elem)
                    if not text_box:
                        continue

                    # テキストがrectの近くにあるかチェック
                    text_parent = text_elem.evaluate('el => el.parentElement')
                    if text_parent != parent:
                        continue

                    # パディング16dpを考慮したコンテナ内側
                    padding = 16
                    container_left = rect_box['x'] + padding
                    container_right = rect_box['x'] + rect_box['width'] - padding
                    container_top = rect_box['y'] + padding
                    container_bottom = rect_box['y'] + rect_box['height'] - padding

                    # はみ出し計算
                    overflow_left = max(0, container_left - text_box['x'])
                    overflow_right = max(0, text_box['x'] + text_box['width'] - container_right)
                    overflow_top = max(0, container_top - text_box['y'])
                    overflow_bottom = max(0, text_box['y'] + text_box['height'] - container_bottom)

                    max_overflow = max(overflow_left, overflow_right, overflow_top, overflow_bottom)

                    if max_overflow > EPSILON:
                        severity = 'FAIL' if max_overflow > 4 else 'WARN'
                        rule_id = 'R-BOX-OVF' if max_overflow > 4 else 'R-BOX-TIGHT'

                        text_content = text_elem.text_content()[:30]
                        violations.append(Violation(
                            rule_id=rule_id,
                            severity=severity,
                            element=f'text: "{text_content}..." in {rect_id}',
                            position={
                                'left': overflow_left,
                                'right': overflow_right,
                                'top': overflow_top,
                                'bottom': overflow_bottom
                            },
                            message=f'コンテナはみ出し: {max_overflow:.1f}dp',
                            slide_number=slide_num
                        ))

        return violations

    def validate_slide(self, slide_num: int, title: str) -> SlideResult:
        """スライドを検証"""
        all_violations = []

        # 各チェックを実行
        all_violations.extend(self.check_viewport_overflow(slide_num))
        all_violations.extend(self.check_safe_area(slide_num))
        all_violations.extend(self.check_text_overlap(slide_num))
        all_violations.extend(self.check_container_overflow(slide_num))

        # ステータス判定
        has_fail = any(v.severity == 'FAIL' for v in all_violations)
        has_warn = any(v.severity == 'WARN' for v in all_violations)

        if has_fail:
            status = 'FAIL'
        elif has_warn:
            status = 'WARN'
        else:
            status = 'PASS'

        return SlideResult(
            slide_number=slide_num,
            title=title,
            violations=all_violations,
            status=status
        )

def main():
    """メイン処理"""
    html_path = Path('index.html').resolve()

    if not html_path.exists():
        print(f"❌ Error: {html_path} not found")
        sys.exit(1)

    print("🚀 Starting Playwright-based slide validation...")
    print(f"📄 Target: {html_path}")
    print()

    with sync_playwright() as p:
        # ブラウザ起動
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': VIEWPORT_WIDTH, 'height': VIEWPORT_HEIGHT}
        )
        page = context.new_page()

        # HTMLを開く
        page.goto(f'file://{html_path}', timeout=60000)
        page.wait_for_load_state('load', timeout=60000)
        page.wait_for_timeout(1000)  # レンダリング完了待機

        validator = SlideValidator(page)

        # スライド数を取得
        slide_count = page.evaluate('''() => {
            const slides = document.querySelectorAll('section');
            return slides.length;
        }''')

        print(f"📊 Total slides: {slide_count}")
        print()

        results = []
        fail_count = 0
        warn_count = 0
        pass_count = 0

        # 各スライドを検証
        for i in range(slide_count):
            # スライドに移動（Marp CLIの出力形式に応じて調整が必要）
            page.evaluate(f'''(slideNum) => {{
                const slides = document.querySelectorAll('section');
                if (slides[slideNum]) {{
                    slides[slideNum].scrollIntoView();
                }}
            }}''', i)

            page.wait_for_timeout(100)  # レンダリング待機

            # タイトル取得
            title = page.evaluate(f'''(slideNum) => {{
                const slides = document.querySelectorAll('section');
                const slide = slides[slideNum];
                const h1 = slide ? slide.querySelector('h1') : null;
                return h1 ? h1.textContent : 'Untitled';
            }}''', i)

            # 検証実行
            result = validator.validate_slide(i + 1, title)
            results.append(result)

            # カウント
            if result.status == 'FAIL':
                fail_count += 1
                print(f"❌ Slide {i+1}: {title[:50]} - FAIL ({len(result.violations)} violations)")
            elif result.status == 'WARN':
                warn_count += 1
                print(f"⚠️  Slide {i+1}: {title[:50]} - WARN ({len(result.violations)} warnings)")
            else:
                pass_count += 1
                print(f"✅ Slide {i+1}: {title[:50]} - PASS")

        browser.close()

    # レポート生成
    print()
    print("=" * 80)
    print("VALIDATION REPORT")
    print("=" * 80)
    print()
    print(f"📊 Summary:")
    print(f"   ✅ PASS: {pass_count} slides")
    print(f"   ⚠️  WARN: {warn_count} slides")
    print(f"   ❌ FAIL: {fail_count} slides")
    print()

    # Fail詳細
    if fail_count > 0:
        print("❌ Failed Slides:")
        print()
        for result in results:
            if result.status == 'FAIL':
                print(f"  Slide {result.slide_number}: {result.title}")
                for v in result.violations:
                    if v.severity == 'FAIL':
                        print(f"    • {v.rule_id}: {v.message}")
                        print(f"      Element: {v.element}")
                print()

    # JSON出力
    output = {
        'summary': {
            'total': slide_count,
            'pass': pass_count,
            'warn': warn_count,
            'fail': fail_count
        },
        'slides': [
            {
                'slide_number': r.slide_number,
                'title': r.title,
                'status': r.status,
                'violations': [asdict(v) for v in r.violations]
            }
            for r in results
        ]
    }

    output_path = Path('validation_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"💾 Detailed report saved to: {output_path}")
    print()

    # 終了コード
    sys.exit(1 if fail_count > 0 else 0)

if __name__ == '__main__':
    main()
