#!/usr/bin/env python3
"""
スライド品質検証システム v2.0 - Pure Python Edition

仕様v1.1に基づいた厳密な検証（Playwright不要）
"""

import json
import sys
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

# 定数
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 720
SAFE_AREA_MARGIN = 24
EPSILON = 1.0  # 幾何誤差許容
DEFAULT_FONT_SIZE = 16

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

class FontMetrics:
    """フォント幅計算"""

    @staticmethod
    def estimate_text_width(text: str, font_size: float, font_family: str = 'Noto Sans JP') -> float:
        """テキストの推定幅（より正確な計算）"""
        if not text:
            return 0

        # 文字種別にカウント
        jp_count = sum(1 for c in text if ord(c) > 0x3000)  # 日本語
        latin_count = len(text) - jp_count

        # フォントごとの係数
        if 'monospace' in font_family.lower() or 'courier' in font_family.lower():
            jp_width = font_size * 1.0
            en_width = font_size * 0.6
        else:
            jp_width = font_size * 1.0
            en_width = font_size * 0.5

        # 安全マージン 1.15倍
        width = (jp_count * jp_width + latin_count * en_width) * 1.15

        return width

class SVGParser:
    """SVG要素の正確な境界計算"""

    def __init__(self, svg_root: ET.Element, svg_path: Path):
        self.root = svg_root
        self.svg_path = svg_path
        self.viewbox = self.parse_viewbox()
        self.styles = self.parse_styles()

    def parse_viewbox(self) -> Tuple[float, float, float, float]:
        """viewBox解析"""
        vb_str = self.root.get('viewBox', '0 0 800 600')
        parts = vb_str.split()
        return tuple(float(p) for p in parts)

    def parse_styles(self) -> Dict[str, Dict[str, str]]:
        """CSS解析"""
        styles = {}

        for style_elem in self.root.findall('.//{http://www.w3.org/2000/svg}style'):
            if not style_elem.text:
                continue

            # 簡易CSSパーサー
            css_text = style_elem.text
            for match in re.finditer(r'\.([a-z-]+)\s*\{([^}]+)\}', css_text):
                class_name = match.group(1)
                props_text = match.group(2)

                props = {}
                for prop_match in re.finditer(r'([a-z-]+):\s*([^;]+);?', props_text):
                    prop_name = prop_match.group(1)
                    prop_value = prop_match.group(2).strip()
                    props[prop_name] = prop_value

                styles[class_name] = props

        return styles

    def get_font_size(self, elem: ET.Element) -> float:
        """要素のfont-sizeを取得"""
        # インラインstyle
        style = elem.get('style', '')
        m = re.search(r'font-size:\s*(\d+(?:\.\d+)?)px', style)
        if m:
            return float(m.group(1))

        # font-size属性
        fs = elem.get('font-size')
        if fs:
            return float(fs.replace('px', ''))

        # class
        css_class = elem.get('class', '')
        for cls in css_class.split():
            if cls in self.styles and 'font-size' in self.styles[cls]:
                fs_str = self.styles[cls]['font-size']
                m = re.search(r'(\d+(?:\.\d+)?)px', fs_str)
                if m:
                    return float(m.group(1))

        return DEFAULT_FONT_SIZE

    def get_font_family(self, elem: ET.Element) -> str:
        """要素のfont-familyを取得"""
        style = elem.get('style', '')
        m = re.search(r'font-family:\s*([^;]+)', style)
        if m:
            return m.group(1)

        css_class = elem.get('class', '')
        for cls in css_class.split():
            if cls in self.styles and 'font-family' in self.styles[cls]:
                return self.styles[cls]['font-family']

        return 'Noto Sans JP'

    def parse_transform(self, elem: ET.Element) -> Tuple[float, float]:
        """transform属性から平行移動を抽出"""
        # 自要素のtransform
        transform = elem.get('transform', '')
        tx, ty = 0.0, 0.0

        m = re.search(r'translate\(\s*([\d.]+)\s*,\s*([\d.]+)\s*\)', transform)
        if m:
            tx += float(m.group(1))
            ty += float(m.group(2))

        # 親要素のtransformを辿る
        parent = self.find_parent(elem)
        while parent is not None:
            parent_transform = parent.get('transform', '')
            m = re.search(r'translate\(\s*([\d.]+)\s*,\s*([\d.]+)\s*\)', parent_transform)
            if m:
                tx += float(m.group(1))
                ty += float(m.group(2))
            parent = self.find_parent(parent)

        return tx, ty

    def find_parent(self, elem: ET.Element) -> Optional[ET.Element]:
        """親要素を探す"""
        for parent in self.root.iter():
            if elem in list(parent):
                return parent
        return None

    def get_text_bounds(self, text_elem: ET.Element) -> Dict:
        """テキスト要素の境界ボックス"""
        x = float(text_elem.get('x', 0))
        y = float(text_elem.get('y', 0))
        tx, ty = self.parse_transform(text_elem)

        abs_x = x + tx
        abs_y = y + ty

        font_size = self.get_font_size(text_elem)
        font_family = self.get_font_family(text_elem)
        text_content = text_elem.text or ''

        # tspan要素も考慮
        for tspan in text_elem.findall('{http://www.w3.org/2000/svg}tspan'):
            if tspan.text:
                text_content += tspan.text

        width = FontMetrics.estimate_text_width(text_content, font_size, font_family)
        height = font_size * 1.2  # line-height相当

        # text-anchor考慮
        anchor = text_elem.get('text-anchor', 'start')
        if anchor == 'middle':
            abs_x -= width / 2
        elif anchor == 'end':
            abs_x -= width

        return {
            'x': abs_x,
            'y': abs_y - font_size,  # baselineからtopへ調整
            'width': width,
            'height': height,
            'text': text_content,
            'font_size': font_size,
            'element': text_elem
        }

    def get_rect_bounds(self, rect_elem: ET.Element) -> Dict:
        """rect要素の境界"""
        x = float(rect_elem.get('x', 0))
        y = float(rect_elem.get('y', 0))
        width = float(rect_elem.get('width', 0))
        height = float(rect_elem.get('height', 0))

        tx, ty = self.parse_transform(rect_elem)

        return {
            'x': x + tx,
            'y': y + ty,
            'width': width,
            'height': height,
            'element': rect_elem
        }

class SlideValidator:
    """スライド品質検証"""

    def __init__(self):
        self.violations: List[Violation] = []

    def check_viewport_overflow(self, svg_parser: SVGParser, slide_num: int) -> List[Violation]:
        """R-BOUND-OVF: ViewPort境界超過チェック"""
        violations = []
        vb_x, vb_y, vb_w, vb_h = svg_parser.viewbox

        # テキスト要素をチェック
        for text_elem in svg_parser.root.iter('{http://www.w3.org/2000/svg}text'):
            bounds = svg_parser.get_text_bounds(text_elem)

            right = bounds['x'] + bounds['width']
            bottom = bounds['y'] + bounds['height']

            overflow_left = max(0, vb_x - bounds['x'])
            overflow_right = max(0, right - vb_w)
            overflow_top = max(0, vb_y - bounds['y'])
            overflow_bottom = max(0, bottom - vb_h)

            total_overflow = overflow_left + overflow_right + overflow_top + overflow_bottom

            if total_overflow > EPSILON:
                violations.append(Violation(
                    rule_id='R-BOUND-OVF',
                    severity='FAIL',
                    element=f'text: "{bounds["text"][:30]}..."',
                    position={
                        'left': overflow_left,
                        'right': overflow_right,
                        'top': overflow_top,
                        'bottom': overflow_bottom,
                        'viewBox': f'{vb_w}×{vb_h}',
                        'content': f'{right:.0f}×{bottom:.0f}'
                    },
                    message=f'ViewBox超過: L={overflow_left:.1f}, R={overflow_right:.1f}, T={overflow_top:.1f}, B={overflow_bottom:.1f}',
                    slide_number=slide_num
                ))

        return violations

    def check_text_overlap(self, svg_parser: SVGParser, slide_num: int) -> List[Violation]:
        """R-TEXT-OVERLAP: テキスト重なりチェック"""
        violations = []

        text_bounds_list = []
        for text_elem in svg_parser.root.iter('{http://www.w3.org/2000/svg}text'):
            bounds = svg_parser.get_text_bounds(text_elem)
            if bounds['width'] > 0 and bounds['height'] > 0:
                text_bounds_list.append(bounds)

        # 全ペアをチェック
        for i in range(len(text_bounds_list)):
            for j in range(i + 1, len(text_bounds_list)):
                b1 = text_bounds_list[i]
                b2 = text_bounds_list[j]

                # 重複領域計算
                overlap_x = max(0, min(b1['x'] + b1['width'], b2['x'] + b2['width']) - max(b1['x'], b2['x']))
                overlap_y = max(0, min(b1['y'] + b1['height'], b2['y'] + b2['height']) - max(b1['y'], b2['y']))
                overlap_area = overlap_x * overlap_y

                if overlap_x >= 2 and overlap_y >= 2 and overlap_area >= 8:
                    # allow-overlap判定
                    has_allow = (
                        'allow-overlap' in (b1['element'].get('class', '')) or
                        'allow-overlap' in (b2['element'].get('class', ''))
                    )

                    severity = 'WARN' if has_allow else 'FAIL'

                    violations.append(Violation(
                        rule_id='R-TEXT-OVERLAP',
                        severity=severity,
                        element=f'"{b1["text"][:20]}..." ⇔ "{b2["text"][:20]}..."',
                        position={
                            'overlap_width': overlap_x,
                            'overlap_height': overlap_y,
                            'overlap_area': overlap_area
                        },
                        message=f'テキスト重なり: {overlap_x:.1f}×{overlap_y:.1f}dp ({overlap_area:.0f}dp²)',
                        slide_number=slide_num
                    ))

        return violations

    def check_container_overflow(self, svg_parser: SVGParser, slide_num: int) -> List[Violation]:
        """R-BOX-OVF: コンテナからのはみ出しチェック"""
        violations = []
        padding = 16

        # rect要素を取得
        rects = list(svg_parser.root.iter('{http://www.w3.org/2000/svg}rect'))

        for rect_elem in rects:
            rect_bounds = svg_parser.get_rect_bounds(rect_elem)

            # このrectと同じ親を持つtext要素を探す
            rect_parent = svg_parser.find_parent(rect_elem)
            if not rect_parent:
                continue

            for text_elem in rect_parent.iter('{http://www.w3.org/2000/svg}text'):
                text_bounds = svg_parser.get_text_bounds(text_elem)

                # コンテナ内側（padding考慮）
                container_left = rect_bounds['x'] + padding
                container_right = rect_bounds['x'] + rect_bounds['width'] - padding
                container_top = rect_bounds['y'] + padding
                container_bottom = rect_bounds['y'] + rect_bounds['height'] - padding

                # はみ出し計算
                overflow_left = max(0, container_left - text_bounds['x'])
                overflow_right = max(0, text_bounds['x'] + text_bounds['width'] - container_right)
                overflow_top = max(0, container_top - text_bounds['y'])
                overflow_bottom = max(0, text_bounds['y'] + text_bounds['height'] - container_bottom)

                max_overflow = max(overflow_left, overflow_right, overflow_top, overflow_bottom)

                if max_overflow > EPSILON:
                    severity = 'FAIL' if max_overflow > 4 else 'WARN'
                    rule_id = 'R-BOX-OVF' if max_overflow > 4 else 'R-BOX-TIGHT'

                    rect_id = rect_elem.get('id') or rect_elem.get('class') or 'rect'

                    violations.append(Violation(
                        rule_id=rule_id,
                        severity=severity,
                        element=f'text: "{text_bounds["text"][:30]}..." in {rect_id}',
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

    def validate_svg(self, svg_path: Path, slide_num: int) -> List[Violation]:
        """SVGファイルを検証"""
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()

            svg_parser = SVGParser(root, svg_path)
            violations = []

            violations.extend(self.check_viewport_overflow(svg_parser, slide_num))
            violations.extend(self.check_text_overlap(svg_parser, slide_num))
            violations.extend(self.check_container_overflow(svg_parser, slide_num))

            return violations
        except Exception as e:
            print(f"  ⚠️  Warning: Failed to parse {svg_path.name}: {e}")
            return []

def main():
    """メイン処理"""
    print("🚀 Starting Pure Python slide validation (v2.0)...")
    print()

    # SVGファイルを探す
    svg_dir = Path('diagrams')
    if not svg_dir.exists():
        print(f"❌ Error: {svg_dir} not found")
        sys.exit(1)

    svg_files = sorted(svg_dir.glob('diagram_*.svg'))
    print(f"📊 Found {len(svg_files)} SVG files")
    print()

    validator = SlideValidator()
    all_results = []
    fail_count = 0
    warn_count = 0
    pass_count = 0

    for i, svg_path in enumerate(svg_files, 1):
        violations = validator.validate_svg(svg_path, i)

        has_fail = any(v.severity == 'FAIL' for v in violations)
        has_warn = any(v.severity == 'WARN' for v in violations)

        if has_fail:
            status = 'FAIL'
            fail_count += 1
            print(f"❌ {svg_path.name}: FAIL ({len([v for v in violations if v.severity=='FAIL'])} failures)")
        elif has_warn:
            status = 'WARN'
            warn_count += 1
            print(f"⚠️  {svg_path.name}: WARN ({len([v for v in violations if v.severity=='WARN'])} warnings)")
        else:
            status = 'PASS'
            pass_count += 1
            print(f"✅ {svg_path.name}: PASS")

        all_results.append({
            'file': svg_path.name,
            'status': status,
            'violations': [asdict(v) for v in violations]
        })

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

    # Fail詳細
    if fail_count > 0:
        print("❌ Failed SVGs (Top 10):")
        print()
        fail_results = [r for r in all_results if r['status'] == 'FAIL']
        for result in fail_results[:10]:
            print(f"  {result['file']}:")
            fail_violations = [v for v in result['violations'] if v['severity'] == 'FAIL']
            for v in fail_violations[:3]:  # 最初の3件のみ
                print(f"    • {v['rule_id']}: {v['message']}")
            if len(fail_violations) > 3:
                print(f"    ... and {len(fail_violations) - 3} more")
            print()

    # JSON出力
    output = {
        'summary': {
            'total': len(svg_files),
            'pass': pass_count,
            'warn': warn_count,
            'fail': fail_count
        },
        'results': all_results
    }

    output_path = Path('validation_report_v2.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"💾 Detailed report saved to: {output_path}")
    print()

    sys.exit(1 if fail_count > 0 else 0)

if __name__ == '__main__':
    main()
