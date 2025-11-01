#!/usr/bin/env python3
"""
SVG境界検証システム v2.0
仕様v1.1に基づき、SVG内のテキストと要素が境界内に収まっているかを検証
"""

import re
import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple

@dataclass
class BoundViolation:
    """境界違反レコード"""
    rule_id: str
    severity: str  # 'FAIL' or 'WARN'
    element_type: str
    text_content: str
    position: Dict
    overflow: Dict
    message: str

@dataclass
class SVGResult:
    """SVG評価結果"""
    svg_path: str
    viewbox: Tuple[float, float, float, float]
    violations: List[BoundViolation]
    status: str
    max_overflow_x: float
    max_overflow_y: float

def estimate_text_width(text: str, font_size: float, anchor: str = 'start') -> float:
    """テキスト幅を推定（日本語/英語の文字幅を考慮）"""
    if not text:
        return 0

    # 日本語文字と英数字を分別
    japanese_count = sum(1 for c in text if ord(c) > 0x3000)
    english_count = len(text) - japanese_count

    # 幅の推定（日本語: 1.0em, 英数字: 0.5em）
    width = (japanese_count * font_size * 1.0 + english_count * font_size * 0.5) * 1.1

    return width

def get_font_size(element: ET.Element, styles: Dict[str, str]) -> float:
    """要素のフォントサイズを取得"""
    # インラインスタイルをチェック
    style = element.get('style', '')
    m = re.search(r'font-size:\s*(\d+(?:\.\d+)?)px', style)
    if m:
        return float(m.group(1))

    # font-size属性をチェック
    font_size_attr = element.get('font-size')
    if font_size_attr:
        return float(font_size_attr.replace('px', ''))

    # CSSクラスをチェック
    css_class = element.get('class', '')
    for cls in css_class.split():
        if cls in styles:
            m = re.search(r'font-size:\s*(\d+(?:\.\d+)?)px', styles[cls])
            if m:
                return float(m.group(1))

    return 16.0  # デフォルト

def extract_css_styles(root: ET.Element) -> Dict[str, str]:
    """SVGからCSSスタイルを抽出"""
    styles = {}

    for style_elem in root.findall('.//{http://www.w3.org/2000/svg}style'):
        if style_elem.text:
            # クラスごとにスタイルをパース
            class_pattern = r'\.([a-zA-Z0-9_-]+)\s*\{([^}]+)\}'
            for match in re.finditer(class_pattern, style_elem.text):
                class_name = match.group(1)
                class_style = match.group(2)
                styles[class_name] = class_style

    return styles

def get_element_transform(element: ET.Element) -> Tuple[float, float]:
    """要素のtransform属性からtranslate値を取得"""
    transform = element.get('transform', '')
    m = re.search(r'translate\(([\d.-]+)[,\s]+([\d.-]+)\)', transform)
    if m:
        return float(m.group(1)), float(m.group(2))
    return 0, 0

def check_svg_bounds(svg_path: Path) -> SVGResult:
    """SVGファイルの境界チェックを実行"""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()

        # ViewBox取得
        viewbox_str = root.get('viewBox', '0 0 800 600')
        vb_parts = viewbox_str.split()
        vb_x, vb_y, vb_width, vb_height = map(float, vb_parts)

        # CSSスタイル抽出
        styles = extract_css_styles(root)

        violations = []
        max_overflow_x = 0
        max_overflow_y = 0

        # すべてのテキスト要素をチェック
        for text_elem in root.iter('{http://www.w3.org/2000/svg}text'):
            x = float(text_elem.get('x', 0))
            y = float(text_elem.get('y', 0))
            anchor = text_elem.get('text-anchor', 'start')
            font_size = get_font_size(text_elem, styles)
            text_content = text_elem.text or ''

            # 親要素のtransformを考慮
            parent = None
            for elem in root.iter():
                for child in elem:
                    if child == text_elem:
                        parent = elem
                        break

            tx, ty = 0, 0
            if parent is not None and parent.tag != root.tag:
                tx, ty = get_element_transform(parent)

            # 絶対座標
            abs_x = x + tx
            abs_y = y + ty

            # テキスト幅を推定
            text_width = estimate_text_width(text_content, font_size, anchor)

            # 右端の位置を計算
            if anchor == 'start':
                right_edge = abs_x + text_width
                left_edge = abs_x
            elif anchor == 'middle':
                right_edge = abs_x + text_width / 2
                left_edge = abs_x - text_width / 2
            elif anchor == 'end':
                right_edge = abs_x
                left_edge = abs_x - text_width
            else:
                right_edge = abs_x + text_width
                left_edge = abs_x

            # 下端の位置
            bottom_edge = abs_y + font_size * 0.3  # ベースライン考慮
            top_edge = abs_y - font_size * 0.9

            # オーバーフロー計算
            overflow_left = max(0, vb_x - left_edge)
            overflow_right = max(0, right_edge - (vb_x + vb_width))
            overflow_top = max(0, vb_y - top_edge)
            overflow_bottom = max(0, bottom_edge - (vb_y + vb_height))

            total_overflow_x = overflow_left + overflow_right
            total_overflow_y = overflow_top + overflow_bottom

            max_overflow_x = max(max_overflow_x, total_overflow_x)
            max_overflow_y = max(max_overflow_y, total_overflow_y)

            # 閾値チェック（1px以上のオーバーフロー）
            if total_overflow_x > 1 or total_overflow_y > 1:
                severity = 'FAIL' if (total_overflow_x > 10 or total_overflow_y > 10) else 'WARN'

                violations.append(BoundViolation(
                    rule_id='R-BOUND-OVF' if severity == 'FAIL' else 'R-BOUND-TIGHT',
                    severity=severity,
                    element_type='text',
                    text_content=text_content[:50],
                    position={
                        'x': abs_x,
                        'y': abs_y,
                        'left': left_edge,
                        'right': right_edge,
                        'top': top_edge,
                        'bottom': bottom_edge
                    },
                    overflow={
                        'left': overflow_left,
                        'right': overflow_right,
                        'top': overflow_top,
                        'bottom': overflow_bottom,
                        'total_x': total_overflow_x,
                        'total_y': total_overflow_y
                    },
                    message=f'ViewBox超過: L={overflow_left:.0f}, R={overflow_right:.0f}, T={overflow_top:.0f}, B={overflow_bottom:.0f}'
                ))

        # すべてのrect要素もチェック
        for rect_elem in root.iter('{http://www.w3.org/2000/svg}rect'):
            x = float(rect_elem.get('x', 0))
            y = float(rect_elem.get('y', 0))
            width = float(rect_elem.get('width', 0))
            height = float(rect_elem.get('height', 0))

            # 親のtransform考慮
            parent = None
            for elem in root.iter():
                for child in elem:
                    if child == rect_elem:
                        parent = elem
                        break

            tx, ty = 0, 0
            if parent is not None and parent.tag != root.tag:
                tx, ty = get_element_transform(parent)

            abs_x = x + tx
            abs_y = y + ty
            right = abs_x + width
            bottom = abs_y + height

            overflow_left = max(0, vb_x - abs_x)
            overflow_right = max(0, right - (vb_x + vb_width))
            overflow_top = max(0, vb_y - abs_y)
            overflow_bottom = max(0, bottom - (vb_y + vb_height))

            total_overflow = overflow_left + overflow_right + overflow_top + overflow_bottom

            if total_overflow > 1:
                rect_id = rect_elem.get('id') or rect_elem.get('class') or 'rect'
                severity = 'FAIL' if total_overflow > 10 else 'WARN'

                violations.append(BoundViolation(
                    rule_id='R-BOUND-OVF' if severity == 'FAIL' else 'R-BOUND-TIGHT',
                    severity=severity,
                    element_type='rect',
                    text_content=rect_id,
                    position={'x': abs_x, 'y': abs_y, 'width': width, 'height': height},
                    overflow={
                        'left': overflow_left,
                        'right': overflow_right,
                        'top': overflow_top,
                        'bottom': overflow_bottom
                    },
                    message=f'Rect超過: L={overflow_left:.0f}, R={overflow_right:.0f}, T={overflow_top:.0f}, B={overflow_bottom:.0f}'
                ))

        # ステータス判定
        has_fail = any(v.severity == 'FAIL' for v in violations)
        has_warn = any(v.severity == 'WARN' for v in violations)

        if has_fail:
            status = 'FAIL'
        elif has_warn:
            status = 'WARN'
        else:
            status = 'PASS'

        return SVGResult(
            svg_path=str(svg_path),
            viewbox=(vb_x, vb_y, vb_width, vb_height),
            violations=violations,
            status=status,
            max_overflow_x=max_overflow_x,
            max_overflow_y=max_overflow_y
        )

    except Exception as e:
        print(f"⚠️  Error processing {svg_path}: {e}")
        return SVGResult(
            svg_path=str(svg_path),
            viewbox=(0, 0, 0, 0),
            violations=[],
            status='ERROR',
            max_overflow_x=0,
            max_overflow_y=0
        )

def main():
    """メイン処理"""
    diagrams_dir = Path('diagrams')

    if not diagrams_dir.exists():
        diagrams_dir = Path('../diagrams')

    if not diagrams_dir.exists():
        print("❌ Error: diagrams directory not found")
        sys.exit(1)

    print("🔍 SVG Bounds Validation System v2.0")
    print(f"📁 Scanning: {diagrams_dir}")
    print()

    svg_files = sorted(diagrams_dir.glob('diagram_*.svg'))

    if not svg_files:
        print("❌ No SVG files found")
        sys.exit(1)

    print(f"📊 Found {len(svg_files)} SVG files")
    print()

    results = []
    fail_count = 0
    warn_count = 0
    pass_count = 0

    for svg_file in svg_files:
        result = check_svg_bounds(svg_file)
        results.append(result)

        if result.status == 'FAIL':
            fail_count += 1
            print(f"❌ {svg_file.name}: FAIL ({len(result.violations)} violations, max overflow: X={result.max_overflow_x:.0f}px, Y={result.max_overflow_y:.0f}px)")
        elif result.status == 'WARN':
            warn_count += 1
            print(f"⚠️  {svg_file.name}: WARN ({len(result.violations)} warnings, max overflow: X={result.max_overflow_x:.0f}px, Y={result.max_overflow_y:.0f}px)")
        else:
            pass_count += 1
            # print(f"✅ {svg_file.name}: PASS")

    # レポート
    print()
    print("=" * 80)
    print("VALIDATION REPORT")
    print("=" * 80)
    print()
    print(f"📊 Summary:")
    print(f"   ✅ PASS: {pass_count} SVGs")
    print(f"   ⚠️  WARN: {warn_count} SVGs")
    print(f"   ❌ FAIL: {fail_count} SVGs")
    print()

    if fail_count > 0:
        print("❌ Failed SVGs (sorted by overflow):")
        print()
        failed = [r for r in results if r.status == 'FAIL']
        failed.sort(key=lambda r: -(r.max_overflow_x + r.max_overflow_y))

        for result in failed[:20]:  # Top 20
            print(f"  {Path(result.svg_path).name}")
            print(f"    ViewBox: {result.viewbox[2]:.0f}×{result.viewbox[3]:.0f}")
            print(f"    Overflow: X={result.max_overflow_x:.0f}px, Y={result.max_overflow_y:.0f}px")
            print(f"    推奨ViewBox: {result.viewbox[2] + result.max_overflow_x + 50:.0f}×{result.viewbox[3] + result.max_overflow_y + 50:.0f}")

            # トップ3の違反を表示
            for v in result.violations[:3]:
                if v.severity == 'FAIL':
                    print(f"      • {v.element_type}: \"{v.text_content}\"")
                    print(f"        {v.message}")
            print()

    # JSON出力
    output = {
        'summary': {
            'total': len(results),
            'pass': pass_count,
            'warn': warn_count,
            'fail': fail_count
        },
        'results': [
            {
                'svg_path': r.svg_path,
                'viewbox': r.viewbox,
                'status': r.status,
                'max_overflow_x': r.max_overflow_x,
                'max_overflow_y': r.max_overflow_y,
                'violations': [asdict(v) for v in r.violations]
            }
            for r in results
        ]
    }

    output_path = Path('svg_bounds_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"💾 Detailed report saved to: {output_path}")
    print()

    sys.exit(1 if fail_count > 0 else 0)

if __name__ == '__main__':
    main()
