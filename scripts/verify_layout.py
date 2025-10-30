#!/usr/bin/env python3
"""
Marpスライドのレイアウト問題を検証するスクリプト
修正後のスライドをチェックして、オーバーフローが解消されたか確認
"""

import re
import os
from pathlib import Path
from datetime import datetime

# スライドディレクトリ
SLIDE_DIR = Path(__file__).parent.parent / "slides"

# レイアウトごとの推奨行数
MAX_LINES = {
    "default": 12,  # デフォルトレイアウト（テキストのみ）
    "layout-horizontal-left": 8,  # 画像左、テキスト右
    "layout-horizontal-right": 8,  # テキスト左、画像右
    "two-column": 25,  # 2カラムレイアウト（多めに許容）
    "three-column": 35,  # 3カラムレイアウト（さらに多く許容）
    "card-grid": 30,  # カード型グリッド（2カラム自動分割）
    "image-top-compact": 15,  # 画像コンパクト＋詳細説明
    "two-images-horizontal": 10,  # 画像2枚横並び
}

# 1行あたりの高さ（ピクセル）
LINE_HEIGHT = 35

# 利用可能な高さ（ピクセル）
AVAILABLE_HEIGHT = {
    "default": 600,
    "layout-horizontal-left": 450,
    "layout-horizontal-right": 450,
    "two-column": 600,
    "three-column": 600,
    "card-grid": 600,
    "image-top-compact": 450,  # 画像40vh + テキストエリア
    "two-images-horizontal": 500,
}


def parse_markdown_slides(file_path):
    """Markdownファイルからスライドを解析"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # YAML frontmatterを除去
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # スライド区切り（---）で分割
    slides = content.split('\n---\n')

    return slides


def analyze_slide(slide_content, slide_num):
    """スライドを解析して問題を検出"""
    lines = slide_content.strip().split('\n')

    # レイアウトクラスを検出
    layout = "default"
    for line in lines:
        if "_class:" in line:
            if "layout-horizontal-left" in line:
                layout = "layout-horizontal-left"
            elif "layout-horizontal-right" in line:
                layout = "layout-horizontal-right"
            elif "three-column" in line:
                layout = "three-column"
            elif "two-column" in line:
                layout = "two-column"
            elif "card-grid" in line:
                layout = "card-grid"
            elif "image-top-compact" in line:
                layout = "image-top-compact"
            elif "two-images-horizontal" in line:
                layout = "two-images-horizontal"
            break

    # 画像の有無
    has_image = bool(re.search(r'!\[.*?\]\(.*?\)', slide_content))

    # タイトル（#で始まる行）を検出
    title_match = re.search(r'^#+ (.+)$', slide_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "(タイトルなし)"

    # コンテンツ行数をカウント（タイトル、画像、空行、コメントを除く）
    content_lines = []
    for line in lines:
        stripped = line.strip()
        # 除外: 空行、コメント、レイアウト指定、区切り線、画像
        if (stripped and
            not stripped.startswith('<!--') and
            not stripped.startswith('#') and
            not stripped.startswith('---') and
            not stripped.startswith('![')):
            content_lines.append(line)

    content_line_count = len(content_lines)

    # オーバーフローの計算
    max_lines = MAX_LINES.get(layout, 12)
    available_height = AVAILABLE_HEIGHT.get(layout, 600)

    if layout in ["layout-horizontal-left", "layout-horizontal-right"] and has_image:
        # 画像がある場合はテキストエリアが狭い
        estimated_height = content_line_count * LINE_HEIGHT
        overflow = max(0, estimated_height - available_height)
    else:
        # テキストのみの場合
        estimated_height = content_line_count * LINE_HEIGHT
        overflow = max(0, estimated_height - available_height)

    # 問題の判定
    is_problematic = content_line_count > max_lines or overflow > 0

    return {
        "slide_num": slide_num,
        "title": title,
        "layout": layout,
        "has_image": has_image,
        "content_lines": content_line_count,
        "max_lines": max_lines,
        "overflow": overflow,
        "is_problematic": is_problematic
    }


def main():
    """メイン処理"""
    print("=" * 70)
    print("スライドレイアウト検証")
    print("=" * 70)
    print(f"検証日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}")
    print(f"対象ディレクトリ: {SLIDE_DIR}")
    print()

    # 対象ファイル
    target_files = [
        "day1_1.md",
        "day1_2.md",
        "day1_3.md",
        "day2_1.md",
        "day2_2.md"
    ]

    total_problems = 0

    for filename in target_files:
        file_path = SLIDE_DIR / filename
        if not file_path.exists():
            print(f"⚠️  {filename} が見つかりません")
            continue

        print(f"\n{'='*70}")
        print(f"📄 {filename}")
        print(f"{'='*70}")

        slides = parse_markdown_slides(file_path)
        problems = []

        for i, slide in enumerate(slides, 1):
            if not slide.strip():
                continue

            result = analyze_slide(slide, i)
            if result["is_problematic"]:
                problems.append(result)

        if problems:
            print(f"\n❌ 問題スライド: {len(problems)}個\n")
            for prob in problems:
                print(f"  スライド {prob['slide_num']}: {prob['title']}")
                print(f"    レイアウト: {prob['layout']}")
                print(f"    画像: {'あり' if prob['has_image'] else 'なし'}")
                print(f"    コンテンツ行数: {prob['content_lines']} (推奨: {prob['max_lines']}行以下)")
                if prob['overflow'] > 0:
                    print(f"    オーバーフロー: {prob['overflow']}px")
                print()
            total_problems += len(problems)
        else:
            print(f"\n✅ 問題なし！すべてのスライドが適切です")

    print("\n" + "="*70)
    print(f"検証結果: 合計 {total_problems} 個の問題スライドが検出されました")
    print("="*70)

    return total_problems


if __name__ == "__main__":
    exit_code = main()
    exit(0 if exit_code == 0 else 1)
