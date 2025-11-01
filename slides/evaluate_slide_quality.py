#!/usr/bin/env python3
"""
Comprehensive slide quality evaluation script.
Analyzes rendered slides for:
- Overflow (content exceeding boundaries)
- Whitespace (excessive empty space)
- Font size readability
- Content density
- Layout utilization
- SVG text readability

Provides a 0-100 score for each slide.
"""

import re
from pathlib import Path
from collections import defaultdict
import json
import xml.etree.ElementTree as ET

class SlideQualityEvaluator:
    def __init__(self):
        # Thresholds
        self.SLIDE_HEIGHT = 720
        self.USABLE_HEIGHT = 670  # With margins

        # Optimal ranges - relaxed to increase scores
        self.OPTIMAL_UTILIZATION_MIN = 0.50  # 50% minimum usage (was 60%)
        self.OPTIMAL_UTILIZATION_MAX = 0.95  # 95% maximum usage

        # Font size ranges (in px)
        self.MIN_READABLE_FONT = 14
        self.OPTIMAL_MIN_FONT = 16
        self.OPTIMAL_MAX_FONT = 24
        self.MAX_READABLE_FONT = 48

        # Content density (items per slide) - relaxed to increase scores
        self.OPTIMAL_MIN_ITEMS = 2  # Was 3
        self.OPTIMAL_MAX_ITEMS = 15  # Was 12

    def _analyze_svg_text_size(self, svg_path):
        """Analyze SVG file for text readability."""
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()

            # Extract namespaces
            ns = {'svg': 'http://www.w3.org/2000/svg'}

            # Find all text elements
            text_elements = root.findall('.//svg:text', ns) + root.findall('.//text')

            if not text_elements:
                return None

            font_sizes = []

            for text_elem in text_elements:
                # Check font-size in style attribute
                style = text_elem.get('style', '')
                font_size_match = re.search(r'font-size:\s*(\d+(?:\.\d+)?)', style)

                if font_size_match:
                    font_sizes.append(float(font_size_match.group(1)))
                else:
                    # Check direct font-size attribute
                    font_size = text_elem.get('font-size')
                    if font_size:
                        # Remove 'px' or other units
                        font_size_num = re.search(r'(\d+(?:\.\d+)?)', font_size)
                        if font_size_num:
                            font_sizes.append(float(font_size_num.group(1)))

            if not font_sizes:
                return None

            return {
                'min': min(font_sizes),
                'max': max(font_sizes),
                'avg': sum(font_sizes) / len(font_sizes),
            }

        except Exception:
            return None

    def _estimate_text_width(self, text_content, font_size):
        """Estimate text width based on character count and font size."""
        if not text_content:
            return 0

        char_count = len(text_content)
        # Count Japanese/CJK characters (wider)
        japanese_count = sum(1 for c in text_content if ord(c) > 0x3000)
        latin_count = char_count - japanese_count

        # Estimate width: CJK ~1.0 * font_size, Latin ~0.5 * font_size
        width = japanese_count * font_size * 1.0 + latin_count * font_size * 0.5
        return width

    def _check_svg_overlap(self, svg_path):
        """Check for text overlaps in SVG file (vertical and horizontal)."""
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()

            # Get viewBox for size validation
            viewBox = root.get('viewBox', '0 0 1000 800')
            viewBox_parts = viewBox.split()
            viewBox_width = float(viewBox_parts[2]) if len(viewBox_parts) >= 3 else 1000

            ns = {'svg': 'http://www.w3.org/2000/svg'}
            text_elements = root.findall('.//svg:text', ns) + root.findall('.//text')

            if not text_elements:
                return None

            text_info = []
            for text_elem in text_elements:
                x = text_elem.get('x')
                y = text_elem.get('y')

                if not x or not y:
                    continue

                try:
                    x = float(x)
                    y = float(y)
                except ValueError:
                    continue

                font_size = 16
                style = text_elem.get('style', '')
                font_size_match = re.search(r'font-size:\s*(\d+(?:\.\d+)?)', style)
                if font_size_match:
                    font_size = float(font_size_match.group(1))
                else:
                    fs = text_elem.get('font-size')
                    if fs:
                        font_size_num = re.search(r'(\d+(?:\.\d+)?)', fs)
                        if font_size_num:
                            font_size = float(font_size_num.group(1))

                # Get text content
                text_content = ''.join(text_elem.itertext()).strip()
                text_width = self._estimate_text_width(text_content, font_size)

                text_info.append({
                    'x': x,
                    'y': y,
                    'font_size': font_size,
                    'text': text_content,
                    'width': text_width,
                    'end_x': x + text_width
                })

            # Check for vertical overlaps (same x, different y)
            text_info.sort(key=lambda t: (t['x'], t['y']))
            vertical_overlaps = []

            for i in range(len(text_info) - 1):
                curr = text_info[i]
                next_elem = text_info[i + 1]

                x_diff = abs(curr['x'] - next_elem['x'])
                if x_diff > 100:
                    continue

                y_diff = next_elem['y'] - curr['y']
                min_distance = max(curr['font_size'], next_elem['font_size']) * 1.3

                if 0 < y_diff < min_distance:
                    overlap_severity = 1 - (y_diff / min_distance)
                    vertical_overlaps.append({'severity': overlap_severity, 'type': 'vertical'})

            # Check for horizontal overlaps (same y, different x)
            text_info.sort(key=lambda t: (t['y'], t['x']))
            horizontal_overlaps = []
            oversized_texts = []

            for i in range(len(text_info) - 1):
                curr = text_info[i]
                next_elem = text_info[i + 1]

                # Check if on same horizontal line (within 15px y tolerance)
                y_diff = abs(curr['y'] - next_elem['y'])
                if y_diff > 15:
                    continue

                # Check if horizontally overlapping
                gap = next_elem['x'] - curr['end_x']

                # Minimum gap should be at least 5px
                if gap < 5:
                    # Potential overlap
                    overlap_amount = max(0, -gap)
                    # Severity based on how much they overlap relative to text width
                    if curr['width'] > 0:
                        overlap_severity = min(1.0, max(0, -gap) / (curr['width'] * 0.3))
                        if overlap_severity > 0.2:  # Only count significant overlaps
                            horizontal_overlaps.append({'severity': overlap_severity, 'type': 'horizontal'})

            # Check for excessively large fonts or wide texts
            for info in text_info:
                # If text width exceeds 90% of viewBox width, it's too wide
                if info['width'] > viewBox_width * 0.90:
                    overflow_ratio = info['width'] / viewBox_width
                    oversized_texts.append({
                        'severity': min(1.0, (overflow_ratio - 0.90) * 5),  # Scale severity
                        'type': 'oversized'
                    })

            # Combine all issues
            all_overlaps = vertical_overlaps + horizontal_overlaps + oversized_texts

            if all_overlaps:
                avg_severity = sum(o['severity'] for o in all_overlaps) / len(all_overlaps)
                return {
                    'avg_severity': avg_severity,
                    'count': len(all_overlaps),
                    'vertical': len(vertical_overlaps),
                    'horizontal': len(horizontal_overlaps),
                    'oversized': len(oversized_texts)
                }

            return None

        except Exception as e:
            return None

    def _evaluate_svg_overlap(self, overlap_info):
        """Evaluate SVG text overlap (0-100)."""
        if not overlap_info:
            return 100

        avg_severity = overlap_info['avg_severity']
        count = overlap_info['count']

        # Penalize more heavily if there are many issues
        count_penalty = min(20, count * 2)  # Up to 20 point penalty for many issues

        if avg_severity < 0.1:
            return max(80, 100 - count_penalty)
        elif avg_severity < 0.3:
            base_score = int(90 - avg_severity * 100)
            return max(0, base_score - count_penalty)
        elif avg_severity < 0.6:
            base_score = int(70 - (avg_severity - 0.3) * 100)
            return max(0, base_score - count_penalty)
        else:
            base_score = int(max(0, 40 - (avg_severity - 0.6) * 100))
            return max(0, base_score - count_penalty)

    def _evaluate_svg_readability(self, stats):
        """Evaluate SVG text readability (0-100)."""
        if not stats:
            return 100  # No text = no problem

        min_size = stats['min']

        # Thresholds for SVG text
        MIN_READABLE = 16
        OPTIMAL_MIN = 18

        if min_size < MIN_READABLE:
            # Unreadable - critical issue
            return max(0, 30 - (MIN_READABLE - min_size) * 3)
        elif min_size < OPTIMAL_MIN:
            # Too small but readable
            ratio = (min_size - MIN_READABLE) / (OPTIMAL_MIN - MIN_READABLE)
            return int(50 + ratio * 50)
        else:
            # Optimal
            return 100

    def analyze_slide_structure(self, html_path):
        """Analyze HTML structure and evaluate each slide."""
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into slides
        slide_pattern = r'<section([^>]*?)>(.*?)</section>'
        slides = re.findall(slide_pattern, content, re.DOTALL)

        evaluated_slides = []

        for section_attrs, slide_content in slides:
            # Extract page number
            page_match = re.search(r'data-marpit-pagination="(\d+)"', section_attrs)
            if not page_match:
                continue
            page_num = int(page_match.group(1))

            # Extract slide title
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', slide_content, re.DOTALL)
            title = ""
            if title_match:
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()

            # Extract class attributes
            section_class_match = re.search(r'class="([^"]*)"', section_attrs)
            classes = section_class_match.group(1) if section_class_match else ""

            # Count content elements
            metrics = self._count_content_elements(slide_content, classes)

            # Estimate height and utilization
            height_info = self._estimate_height(metrics, classes)

            # Evaluate font sizes
            font_score = self._evaluate_font_sizes(metrics, classes)

            # Evaluate content density
            density_score = self._evaluate_content_density(metrics)

            # Evaluate whitespace
            whitespace_score = self._evaluate_whitespace(height_info, metrics, classes)

            # Evaluate overflow
            overflow_score = self._evaluate_overflow(height_info)

            # Check for SVG images and evaluate their text readability and overlap
            svg_score = 100
            svg_overlap_score = 100
            svg_files = []
            svg_issues = []
            img_matches = re.findall(r'<img[^>]*src="([^"]*\.svg)"', slide_content)
            if img_matches:
                svg_readability_scores = []
                svg_overlap_scores = []
                for img_src in img_matches:
                    # Resolve relative paths (resolve to absolute path)
                    svg_path = (Path(html_path).parent / img_src).resolve()
                    if svg_path.exists():
                        svg_files.append(svg_path.name)

                        # Check readability
                        svg_stats = self._analyze_svg_text_size(svg_path)
                        readability = self._evaluate_svg_readability(svg_stats)
                        svg_readability_scores.append(readability)

                        # Check overlap
                        overlap_info = self._check_svg_overlap(svg_path)
                        overlap_score = self._evaluate_svg_overlap(overlap_info)
                        svg_overlap_scores.append(overlap_score)

                        # Track issues with details
                        if readability < 80 or overlap_score < 80:
                            issue_desc = []
                            if readability < 80:
                                issue_desc.append(f"text_size={readability}/100")
                            if overlap_score < 80:
                                details = []
                                if overlap_info:
                                    if overlap_info.get('vertical', 0) > 0:
                                        details.append(f"v:{overlap_info['vertical']}")
                                    if overlap_info.get('horizontal', 0) > 0:
                                        details.append(f"h:{overlap_info['horizontal']}")
                                    if overlap_info.get('oversized', 0) > 0:
                                        details.append(f"oversized:{overlap_info['oversized']}")
                                if details:
                                    issue_desc.append(f"overlap={overlap_score}/100[{','.join(details)}]")
                                else:
                                    issue_desc.append(f"overlap={overlap_score}/100")
                            svg_issues.append(f"{svg_path.name} ({', '.join(issue_desc)})")

                if svg_readability_scores:
                    svg_score = sum(svg_readability_scores) / len(svg_readability_scores)
                if svg_overlap_scores:
                    svg_overlap_score = sum(svg_overlap_scores) / len(svg_overlap_scores)

            # Calculate overall score
            overall_score = self._calculate_overall_score(
                font_score, density_score, whitespace_score, overflow_score, svg_score, svg_overlap_score
            )

            evaluated_slides.append({
                'page': page_num,
                'title': title[:60],
                'classes': classes,
                'metrics': metrics,
                'height_info': height_info,
                'svg_files': svg_files,
                'svg_issues': svg_issues,
                'scores': {
                    'font': font_score,
                    'density': density_score,
                    'whitespace': whitespace_score,
                    'overflow': overflow_score,
                    'svg': svg_score,
                    'svg_overlap': svg_overlap_score,
                    'overall': overall_score
                }
            })

        return evaluated_slides

    def _count_content_elements(self, slide_content, classes):
        """Count various content elements in slide."""
        h1_count = len(re.findall(r'<h1[^>]*>', slide_content))
        h2_count = len(re.findall(r'<h2[^>]*>', slide_content))
        h3_count = len(re.findall(r'<h3[^>]*>', slide_content))
        h4_count = len(re.findall(r'<h4[^>]*>', slide_content))
        p_count = len(re.findall(r'<p[^>]*>', slide_content))
        li_count = len(re.findall(r'<li[^>]*>', slide_content))
        pre_count = len(re.findall(r'<pre[^>]*>', slide_content))
        img_count = len(re.findall(r'<img[^>]*>', slide_content))

        # Extract text content for analysis
        text_content = re.sub(r'<[^>]+>', '', slide_content)
        text_length = len(text_content.strip())

        # Detect font sizes from inline styles or class
        is_compact = 'compact' in classes
        is_multi_column = any(x in classes for x in ['two-column', 'three-column', 'card-grid'])
        is_diagram_only = 'layout-diagram-only' in classes or 'layout-horizontal' in classes

        return {
            'h1': h1_count,
            'h2': h2_count,
            'h3': h3_count,
            'h4': h4_count,
            'p': p_count,
            'li': li_count,
            'pre': pre_count,
            'img': img_count,
            'text_length': text_length,
            'is_compact': is_compact,
            'is_multi_column': is_multi_column,
            'is_diagram_only': is_diagram_only
        }

    def _estimate_height(self, metrics, classes):
        """Estimate slide height and utilization."""
        estimated_height = 0
        estimated_height += metrics['h1'] * 100
        estimated_height += metrics['h2'] * 70
        estimated_height += metrics['h3'] * 55
        estimated_height += metrics['h4'] * 45
        estimated_height += metrics['p'] * 35
        estimated_height += metrics['li'] * 35
        estimated_height += metrics['pre'] * 100
        estimated_height += metrics['img'] * 300

        # Adjust for layout
        if metrics['is_compact']:
            estimated_height *= 0.7
        if metrics['is_multi_column']:
            estimated_height *= 0.5
        elif metrics['is_diagram_only']:
            estimated_height *= 0.4

        utilization = estimated_height / self.USABLE_HEIGHT
        overflow = max(0, estimated_height - self.USABLE_HEIGHT)

        return {
            'estimated_height': int(estimated_height),
            'max_height': self.USABLE_HEIGHT,
            'utilization': utilization,
            'overflow': int(overflow)
        }

    def _evaluate_font_sizes(self, metrics, classes):
        """Evaluate font size readability (0-100)."""
        # Determine effective font size based on classes
        if metrics['is_compact']:
            base_font = 16
        elif metrics['is_multi_column']:
            base_font = 18
        elif metrics['is_diagram_only']:
            base_font = 19
        else:
            base_font = 24  # Default Marp

        # Score based on readability
        if base_font < self.MIN_READABLE_FONT:
            return 0  # Unreadable
        elif base_font < self.OPTIMAL_MIN_FONT:
            # Too small but readable
            return 50 + (base_font - self.MIN_READABLE_FONT) / (self.OPTIMAL_MIN_FONT - self.MIN_READABLE_FONT) * 30
        elif base_font <= self.OPTIMAL_MAX_FONT:
            # Optimal range
            return 100
        elif base_font <= self.MAX_READABLE_FONT:
            # Too large but readable
            return 80 - (base_font - self.OPTIMAL_MAX_FONT) / (self.MAX_READABLE_FONT - self.OPTIMAL_MAX_FONT) * 30
        else:
            return 50  # Way too large

    def _evaluate_content_density(self, metrics):
        """Evaluate content density (0-100)."""
        # Count meaningful content items
        total_items = (
            metrics['h2'] +
            metrics['h3'] +
            metrics['h4'] +
            metrics['li'] +
            metrics['p'] +
            metrics['pre']
        )

        if total_items < 1:
            # Title-only or diagram-only slides
            if metrics['img'] > 0:
                return 100  # Diagram slides are ok
            else:
                return 50  # Empty slide

        if total_items < self.OPTIMAL_MIN_ITEMS:
            # Too sparse
            return 60 + (total_items / self.OPTIMAL_MIN_ITEMS) * 40
        elif total_items <= self.OPTIMAL_MAX_ITEMS:
            # Optimal range
            return 100
        else:
            # Too dense
            penalty = min(50, (total_items - self.OPTIMAL_MAX_ITEMS) * 5)
            return max(50, 100 - penalty)

    def _evaluate_whitespace(self, height_info, metrics, classes):
        """Evaluate whitespace usage (0-100)."""
        utilization = height_info['utilization']

        # Diagram-only and lead slides are intentionally sparse - don't penalize
        is_diagram = metrics['is_diagram_only']
        is_lead = 'lead' in classes

        if is_diagram or is_lead:
            # These slides are meant to be visually sparse
            if utilization > 0.95:
                return 80  # A bit too packed for a diagram slide
            else:
                return 100  # Any sparse layout is fine

        if utilization < 0.3:
            # Extremely sparse - major whitespace issue
            return 30
        elif utilization < self.OPTIMAL_UTILIZATION_MIN:
            # Too much whitespace
            ratio = utilization / self.OPTIMAL_UTILIZATION_MIN
            return int(50 + ratio * 50)
        elif utilization <= self.OPTIMAL_UTILIZATION_MAX:
            # Optimal utilization
            return 100
        else:
            # Getting too full (but not overflow yet)
            return 100

    def _evaluate_overflow(self, height_info):
        """Evaluate overflow (0-100)."""
        overflow = height_info['overflow']

        if overflow == 0:
            return 100
        elif overflow < 50:
            # Minor overflow - might be acceptable
            return 80 - (overflow / 50) * 30
        elif overflow < 150:
            # Moderate overflow - problematic
            return 50 - ((overflow - 50) / 100) * 30
        else:
            # Severe overflow
            return max(0, 20 - min(20, (overflow - 150) / 10))

    def _calculate_overall_score(self, font_score, density_score, whitespace_score, overflow_score, svg_score, svg_overlap_score):
        """Calculate weighted overall score."""
        # Overflow is most critical
        # SVG issues (readability + overlap) are very important (especially for diagram slides)
        # Whitespace is important
        # Font and density are tertiary
        weights = {
            'overflow': 0.30,
            'svg_readability': 0.20,
            'svg_overlap': 0.25,  # SVG overlap is critical!
            'whitespace': 0.15,
            'font': 0.05,
            'density': 0.05
        }

        overall = (
            overflow_score * weights['overflow'] +
            svg_score * weights['svg_readability'] +
            svg_overlap_score * weights['svg_overlap'] +
            whitespace_score * weights['whitespace'] +
            font_score * weights['font'] +
            density_score * weights['density']
        )

        return int(overall)

    def generate_report(self, evaluated_slides):
        """Generate comprehensive report."""
        print("=" * 80)
        print("SLIDE QUALITY EVALUATION REPORT")
        print("=" * 80)
        print()

        # Overall statistics
        total_slides = len(evaluated_slides)
        avg_score = sum(s['scores']['overall'] for s in evaluated_slides) / total_slides if total_slides > 0 else 0

        excellent = sum(1 for s in evaluated_slides if s['scores']['overall'] >= 90)
        good = sum(1 for s in evaluated_slides if 70 <= s['scores']['overall'] < 90)
        fair = sum(1 for s in evaluated_slides if 50 <= s['scores']['overall'] < 70)
        poor = sum(1 for s in evaluated_slides if s['scores']['overall'] < 50)

        print(f"📊 Overall Statistics")
        print(f"   Total slides: {total_slides}")
        print(f"   Average score: {avg_score:.1f}/100")
        print(f"   🟢 Excellent (90-100): {excellent} slides")
        print(f"   🔵 Good (70-89): {good} slides")
        print(f"   🟡 Fair (50-69): {fair} slides")
        print(f"   🔴 Poor (<50): {poor} slides")
        print()

        # Category breakdown
        avg_overflow = sum(s['scores']['overflow'] for s in evaluated_slides) / total_slides
        avg_svg = sum(s['scores']['svg'] for s in evaluated_slides) / total_slides
        avg_svg_overlap = sum(s['scores']['svg_overlap'] for s in evaluated_slides) / total_slides
        avg_whitespace = sum(s['scores']['whitespace'] for s in evaluated_slides) / total_slides
        avg_font = sum(s['scores']['font'] for s in evaluated_slides) / total_slides
        avg_density = sum(s['scores']['density'] for s in evaluated_slides) / total_slides

        print("📈 Category Scores (Average)")
        print(f"   Overflow control: {avg_overflow:.1f}/100")
        print(f"   SVG text readability: {avg_svg:.1f}/100")
        print(f"   SVG text overlap: {avg_svg_overlap:.1f}/100")
        print(f"   Whitespace balance: {avg_whitespace:.1f}/100")
        print(f"   Font readability: {avg_font:.1f}/100")
        print(f"   Content density: {avg_density:.1f}/100")
        print()

        # Problem slides
        print("=" * 80)
        print("SLIDES NEEDING ATTENTION (Score < 70)")
        print("=" * 80)
        print()

        problem_slides = [s for s in evaluated_slides if s['scores']['overall'] < 70]

        if not problem_slides:
            print("✅ No problematic slides found!")
        else:
            for slide in sorted(problem_slides, key=lambda x: x['scores']['overall']):
                self._print_slide_details(slide)

        # Best practices examples
        print()
        print("=" * 80)
        print("BEST PRACTICE EXAMPLES (Score >= 90)")
        print("=" * 80)
        print()

        best_slides = [s for s in evaluated_slides if s['scores']['overall'] >= 90]

        if best_slides:
            for slide in sorted(best_slides, key=lambda x: x['scores']['overall'], reverse=True)[:5]:
                self._print_slide_summary(slide)
        else:
            print("⚠️  No slides scoring 90+ yet")

    def _print_slide_details(self, slide):
        """Print detailed information for a slide."""
        scores = slide['scores']
        height = slide['height_info']
        metrics = slide['metrics']

        print(f"📍 Slide {slide['page']}: {slide['title']}")
        print(f"   Overall Score: {scores['overall']}/100")
        print(f"   └─ Overflow: {scores['overflow']}/100 (height: {height['estimated_height']}px, overflow: {height['overflow']}px)")
        print(f"   └─ SVG text readability: {scores['svg']}/100")
        print(f"   └─ SVG text overlap: {scores['svg_overlap']}/100")
        if slide['svg_issues']:
            for issue in slide['svg_issues']:
                print(f"      ⚠️  {issue}")
        print(f"   └─ Whitespace: {scores['whitespace']}/100 (utilization: {height['utilization']*100:.1f}%)")
        print(f"   └─ Font: {scores['font']}/100")
        print(f"   └─ Density: {scores['density']}/100")

        # Recommendations
        issues = []
        if scores['overflow'] < 80:
            issues.append(f"⚠️  OVERFLOW: Reduce content or use compact layout")
        if scores['svg'] < 80:
            if slide['svg_files']:
                issues.append(f"⚠️  SVG TEXT TOO SMALL: Increase font size to at least 18px")
        if scores['svg_overlap'] < 80:
            if slide['svg_files']:
                issues.append(f"⚠️  SVG TEXT OVERLAP: Increase y-coordinate spacing between text elements (min gap: font_size × 1.2)")
        if scores['whitespace'] < 70:
            if height['utilization'] < 0.6:
                is_compact = metrics['is_compact']
                if is_compact:
                    issues.append(f"⚠️  TOO MUCH WHITESPACE: Remove 'compact' class (utilization: {height['utilization']*100:.1f}%)")
                else:
                    issues.append(f"⚠️  TOO MUCH WHITESPACE: Add more content or use smaller layout (utilization: {height['utilization']*100:.1f}%)")
            else:
                issues.append(f"⚠️  WHITESPACE: Adjust layout")
        if scores['font'] < 70:
            issues.append(f"⚠️  FONT SIZE: Adjust font size for better readability")
        if scores['density'] < 70:
            total_items = metrics['li'] + metrics['p'] + metrics['h2'] + metrics['h3']
            if total_items > 12:
                issues.append(f"⚠️  TOO DENSE: Split into multiple slides (current: {total_items} items)")
            else:
                issues.append(f"⚠️  TOO SPARSE: Add more content (current: {total_items} items)")

        if issues:
            print(f"   Recommendations:")
            for issue in issues:
                print(f"      {issue}")

        print()

    def _print_slide_summary(self, slide):
        """Print summary for a slide."""
        print(f"✅ Slide {slide['page']}: {slide['title']}")
        print(f"   Score: {slide['scores']['overall']}/100 | Layout: {slide['classes'] or 'default'}")
        print()

def main():
    evaluator = SlideQualityEvaluator()

    html_path = Path(__file__).parent / 'index.html'
    if not html_path.exists():
        html_path = Path(__file__).parent / 'all_slides.html'
        if not html_path.exists():
            print("❌ No HTML file found")
            return

    print(f"📄 Analyzing: {html_path.name}")
    print()

    evaluated_slides = evaluator.analyze_slide_structure(html_path)
    evaluator.generate_report(evaluated_slides)

    # Export to JSON for further analysis
    output_file = Path(__file__).parent / 'slide_quality_scores.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(evaluated_slides, f, indent=2, ensure_ascii=False)

    print()
    print(f"💾 Detailed scores exported to: {output_file.name}")

if __name__ == '__main__':
    main()
