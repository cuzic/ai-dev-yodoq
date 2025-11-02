#!/usr/bin/env python3
"""
全スライドファイルのfrontmatterを更新して、
インラインstyleをtheme: ai-seminarに置き換える
"""

import re
from pathlib import Path

# 対象ファイル
TARGET_FILES = [
    'all_slides.md',
    'day1_1.md', 'day1_2.md', 'day1_3.md',
    'day2_1.md', 'day2_2.md',
    'day1_1_scaffold.md', 'day1_2_scaffold.md', 'day1_3_scaffold.md',
    'day2_1_scaffold.md', 'day2_2_scaffold.md',
]

def update_frontmatter(file_path):
    """
    frontmatterを更新:
    - theme: ai-seminar を追加
    - style: | セクションを削除
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # frontmatterを抽出（最初の --- ... --- 部分）
    frontmatter_pattern = r'^---\n(.*?)\n---\n'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        print(f"❌ {file_path.name}: frontmatter not found")
        return False

    frontmatter = match.group(1)
    rest_content = content[match.end():]

    # frontmatterを行ごとに処理
    lines = frontmatter.split('\n')
    new_lines = []
    in_style_block = False

    for line in lines:
        # style: | ブロックの開始を検出
        if line.strip() == 'style: |':
            in_style_block = True
            continue

        # style ブロック内の行をスキップ
        if in_style_block:
            # インデントがない行（次のフィールド）に到達したらブロック終了
            if line and not line.startswith(' '):
                in_style_block = False
                new_lines.append(line)
            continue

        # theme: を ai-seminar に置き換え
        if line.startswith('theme:'):
            line = 'theme: ai-seminar'

        new_lines.append(line)

    # 新しいfrontmatterを構築
    new_frontmatter = '\n'.join(new_lines)
    new_content = f"---\n{new_frontmatter}\n---\n{rest_content}"

    # ファイルに書き戻し
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True

def main():
    slides_dir = Path('.')

    print("🔄 Updating frontmatter to use theme: ai-seminar\n")

    updated_count = 0
    for filename in TARGET_FILES:
        file_path = slides_dir / filename

        if not file_path.exists():
            print(f"⚠️  {filename}: file not found, skipping")
            continue

        # ファイルサイズ確認（前）
        size_before = file_path.stat().st_size

        if update_frontmatter(file_path):
            size_after = file_path.stat().st_size
            reduction = size_before - size_after
            reduction_pct = (reduction / size_before) * 100

            print(f"✅ {filename}: {size_before:,} → {size_after:,} bytes (-{reduction:,} bytes, -{reduction_pct:.1f}%)")
            updated_count += 1

    print(f"\n✨ Updated {updated_count}/{len(TARGET_FILES)} files")

    # 合計削減量を計算
    total_reduction = 0
    for filename in TARGET_FILES:
        file_path = slides_dir / filename
        if file_path.exists():
            # 概算: 187行 × 平均30文字 ≈ 5,610バイト削減/ファイル
            total_reduction += 5610

    print(f"💾 Estimated total reduction: ~{total_reduction:,} bytes (~{total_reduction/1024:.1f} KB)")

if __name__ == '__main__':
    main()
