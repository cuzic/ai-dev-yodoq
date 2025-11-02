#!/usr/bin/env python3
"""
スライドレイアウト推奨システム v1.0

仕様: LAYOUT_RECOMMENDATION_SPEC.md に基づく
"""

import re
import sys
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict

@dataclass
class ContentAnalysis:
    """コンテンツ解析結果"""
    has_h1: bool
    has_h2: bool
    bullet_count: int
    paragraph_count: int
    total_chars: int
    total_text_chars: int  # タイトル除く
    has_image: bool
    image_count: int
    images: List[str]
    has_code: bool
    code_block_count: int
    has_table: bool
    text_density: float
    has_comparison: bool
    is_two_list_structure: bool

@dataclass
class LayoutRecommendation:
    """レイアウト推奨結果"""
    slide_number: int
    title: str
    current_layout: Optional[str]
    recommended_layout: Optional[str]
    confidence: float
    reason: str
    metrics: Dict

def extract_slides(markdown_path: Path) -> List[Dict]:
    """Markdownからスライドを抽出"""
    with open(markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # スライド区切りで分割
    slides = re.split(r'\n---\n', content)

    result = []
    for i, slide_content in enumerate(slides, 1):
        # クラス指定を抽出
        class_match = re.search(r'<!--\s*_class:\s*(.+?)\s*-->', slide_content)
        current_layout = class_match.group(1).strip() if class_match else None

        # タイトルを抽出
        title_match = re.search(r'^#\s+(.+)$', slide_content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else 'Untitled'

        result.append({
            'number': i,
            'title': title,
            'content': slide_content,
            'current_layout': current_layout
        })

    return result

def count_paragraphs(content: str) -> int:
    """段落数をカウント"""
    # タイトル、箇条書き、コードブロック、空行を除いた段落
    lines = content.split('\n')
    paragraphs = 0
    in_code_block = False
    current_paragraph = []

    for line in lines:
        # コードブロックの開始/終了
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # 除外する行
        if (line.strip().startswith('#') or
            line.strip().startswith('-') or
            line.strip().startswith('*') or
            line.strip().startswith('|') or
            line.strip().startswith('![') or
            line.strip().startswith('<!--') or
            not line.strip()):
            if current_paragraph:
                paragraphs += 1
                current_paragraph = []
            continue

        current_paragraph.append(line)

    if current_paragraph:
        paragraphs += 1

    return paragraphs

def extract_images(content: str) -> List[str]:
    """画像パスを抽出"""
    pattern = r'!\[.*?\]\((.*?)\)'
    return re.findall(pattern, content)

def has_comparison_keywords(content: str) -> bool:
    """比較キーワードの存在チェック"""
    keywords = [
        'Before', 'After', 'before', 'after',
        '従来', '改善', '問題', '解決',
        'メリット', 'デメリット',
        'VS', 'vs', '比較', '対比'
    ]
    return any(keyword in content for keyword in keywords)

def is_two_list_structure(content: str) -> bool:
    """2つのリスト構造かチェック"""
    # 連続する箇条書きブロックが2つあるか
    lines = content.split('\n')
    list_blocks = 0
    in_list = False

    for line in lines:
        if line.strip().startswith(('-', '*', '1.', '2.', '3.', '4.', '5.')):
            if not in_list:
                list_blocks += 1
                in_list = True
        elif not line.strip():
            in_list = False

    return list_blocks >= 2

def is_diagram_focused(image_path: str) -> bool:
    """図表が重要かどうか判定"""
    diagram_keywords = ['diagram', 'flow', 'chart', 'graph', 'sequence', 'er']
    return any(keyword in image_path.lower() for keyword in diagram_keywords)

def analyze_content(content: str) -> ContentAnalysis:
    """コンテンツを解析"""
    # タイトルを除いたテキスト
    content_without_title = re.sub(r'^#\s+.+$', '', content, flags=re.MULTILINE)

    has_h1 = bool(re.search(r'^# ', content, re.M))
    has_h2 = bool(re.search(r'^## ', content, re.M))

    bullet_count = len(re.findall(r'^[-*]\s+', content, re.M))
    paragraph_count = count_paragraphs(content)

    total_chars = len(content)
    total_text_chars = len(content_without_title)

    images = extract_images(content)
    has_image = len(images) > 0
    image_count = len(images)

    has_code = bool(re.search(r'```', content))
    code_block_count = content.count('```') // 2

    has_table = bool(re.search(r'^\|', content, re.M))

    # テキスト密度計算
    items = bullet_count + paragraph_count
    text_density = total_text_chars / (items + 1) if items > 0 else total_text_chars

    return ContentAnalysis(
        has_h1=has_h1,
        has_h2=has_h2,
        bullet_count=bullet_count,
        paragraph_count=paragraph_count,
        total_chars=total_chars,
        total_text_chars=total_text_chars,
        has_image=has_image,
        image_count=image_count,
        images=images,
        has_code=has_code,
        code_block_count=code_block_count,
        has_table=has_table,
        text_density=text_density,
        has_comparison=has_comparison_keywords(content),
        is_two_list_structure=is_two_list_structure(content)
    )

def recommend_layout(analysis: ContentAnalysis) -> tuple[Optional[str], str, float]:
    """レイアウトを推奨（レイアウト、理由、確信度）"""

    # Rule 1: lead判定
    if analysis.has_h1 and not analysis.has_image and not analysis.has_code:
        content_items = analysis.bullet_count + analysis.paragraph_count
        if content_items <= 3 and analysis.total_text_chars < 100:
            return 'lead', 'タイトルのみまたは短い説明文のみのため', 0.95

    # Rule 2: diagram-only判定
    if analysis.has_image:
        text_items = analysis.bullet_count + analysis.paragraph_count
        if text_items <= 3 and analysis.total_text_chars < 150:
            return 'layout-diagram-only', '画像メイン、テキスト最小限のため', 0.90

    # Rule 4: two-column判定（Rule 3より優先）
    if analysis.has_comparison or analysis.is_two_list_structure:
        total_items = analysis.bullet_count + analysis.paragraph_count
        if total_items >= 10:
            return 'two-column compact', '比較構造でコンテンツ量が多いため', 0.85
        elif total_items >= 4:
            return 'two-column', '比較構造のため', 0.80

    # Rule 3: horizontal判定
    if analysis.has_image and analysis.image_count == 1:
        if 3 <= analysis.bullet_count <= 8:
            # 画像が図表かどうかで左右を判定
            if any(is_diagram_focused(img) for img in analysis.images):
                return 'layout-horizontal-left', '図表が重要で説明文が中程度のため', 0.75
            else:
                return 'layout-horizontal-right', 'テキスト説明が主で画像は補足のため', 0.75
        elif analysis.bullet_count > 8:
            return 'layout-horizontal-right compact', 'テキスト量が多く画像は補足のため', 0.80

    # Rule 5: compact判定
    if (analysis.bullet_count >= 9 or
        analysis.paragraph_count >= 5 or
        analysis.total_text_chars >= 800):
        if not (analysis.has_comparison or analysis.is_two_list_structure):
            return 'compact', 'コンテンツ量が多いため', 0.85

    # 特殊ケース: コードブロック
    if analysis.has_code:
        if analysis.code_block_count >= 2 or analysis.total_text_chars > 500:
            return 'compact', 'コードブロックと説明が多いため', 0.75

    # 特殊ケース: 表
    if analysis.has_table and analysis.total_text_chars > 400:
        return 'compact', '表と説明が多いため', 0.70

    # Rule 6: デフォルト
    if 3 <= analysis.bullet_count <= 8 and 100 <= analysis.total_text_chars <= 500:
        return None, '標準的なテキストスライドのため（デフォルト）', 0.60

    # その他
    return None, '明確な推奨なし（デフォルト）', 0.50

def main():
    """メイン処理"""
    markdown_path = Path('all_slides.md')

    if not markdown_path.exists():
        print(f"❌ Error: {markdown_path} not found")
        sys.exit(1)

    print("📊 スライドレイアウト推奨システム v1.0")
    print(f"📄 Target: {markdown_path}")
    print()

    # スライド抽出
    slides = extract_slides(markdown_path)
    print(f"📊 Total slides: {len(slides)}")
    print()

    recommendations = []
    match_count = 0
    mismatch_count = 0
    no_current_layout = 0

    for slide in slides:
        analysis = analyze_content(slide['content'])
        recommended, reason, confidence = recommend_layout(analysis)

        recommendation = LayoutRecommendation(
            slide_number=slide['number'],
            title=slide['title'],
            current_layout=slide['current_layout'],
            recommended_layout=recommended,
            confidence=confidence,
            reason=reason,
            metrics={
                'bullet_count': analysis.bullet_count,
                'paragraph_count': analysis.paragraph_count,
                'total_chars': analysis.total_chars,
                'image_count': analysis.image_count,
                'text_density': round(analysis.text_density, 1)
            }
        )

        recommendations.append(recommendation)

        # 一致/不一致カウント
        if slide['current_layout'] is None:
            no_current_layout += 1
        elif slide['current_layout'] == recommended:
            match_count += 1
        else:
            mismatch_count += 1

    # 不一致のみ表示
    print("⚠️  Layout Mismatches (current vs recommended):")
    print()

    for rec in recommendations:
        if rec.current_layout and rec.recommended_layout:
            if rec.current_layout != rec.recommended_layout:
                print(f"Slide {rec.slide_number}: {rec.title[:50]}")
                print(f"  Current:      {rec.current_layout}")
                print(f"  Recommended:  {rec.recommended_layout}")
                print(f"  Confidence:   {rec.confidence:.0%}")
                print(f"  Reason:       {rec.reason}")
                print(f"  Metrics:      bullets={rec.metrics['bullet_count']}, "
                      f"chars={rec.metrics['total_chars']}, "
                      f"images={rec.metrics['image_count']}")
                print()

    # サマリー
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"✅ Matches:        {match_count} slides")
    print(f"⚠️  Mismatches:     {mismatch_count} slides")
    print(f"📝 No layout:      {no_current_layout} slides")
    print()

    if match_count + mismatch_count > 0:
        accuracy = match_count / (match_count + mismatch_count) * 100
        print(f"🎯 Accuracy:       {accuracy:.1f}%")
    print()

    # JSON出力
    output = {
        'summary': {
            'total': len(slides),
            'matches': match_count,
            'mismatches': mismatch_count,
            'no_layout': no_current_layout,
            'accuracy': match_count / (match_count + mismatch_count) if (match_count + mismatch_count) > 0 else 0
        },
        'recommendations': [asdict(rec) for rec in recommendations]
    }

    output_path = Path('layout_recommendations.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"💾 Detailed report saved to: {output_path}")
    print()

if __name__ == '__main__':
    main()
