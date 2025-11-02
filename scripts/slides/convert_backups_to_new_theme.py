#!/usr/bin/env python3
"""
バックアップファイル（.md.backup）を最新のai-seminarテーマに変換するスクリプト

変換内容:
1. frontmatter更新: theme: default → theme: ai-seminar
2. インラインCSSを削除
3. 図表パスを更新: diagrams/ → ../assets/diagrams/
4. 新しいレイアウトクラスを適用（適切な場所に）
"""

import re
from pathlib import Path

def update_frontmatter(content: str) -> str:
    """
    frontmatterを更新
    - theme: ai-seminar に変更
    - style: | セクションを削除
    """
    lines = content.split('\n')
    new_lines = []
    in_frontmatter = False
    in_style_block = False
    frontmatter_count = 0

    for i, line in enumerate(lines):
        # frontmatterの開始/終了を検出
        if line.strip() == '---':
            frontmatter_count += 1
            new_lines.append(line)
            if frontmatter_count == 1:
                in_frontmatter = True
            elif frontmatter_count == 2:
                in_frontmatter = False
            continue

        # frontmatter内の処理
        if in_frontmatter:
            # style: | の開始を検出
            if line.strip() == 'style: |':
                in_style_block = True
                continue

            # style blockの終了を検出
            if in_style_block:
                # インデントがなくなったら終了
                if line and not line.startswith(' ') and not line.startswith('\t'):
                    in_style_block = False
                else:
                    continue  # style block内なのでスキップ

            # theme行を変更
            if line.startswith('theme:'):
                new_lines.append('theme: ai-seminar')
            # header, footer行を削除
            elif line.startswith('header:') or line.startswith('footer:'):
                continue
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return '\n'.join(new_lines)

def update_diagram_paths(content: str) -> str:
    """
    図表パスを更新
    diagrams/ → ../assets/diagrams/
    """
    # diagrams/diagram_*.svg → ../assets/diagrams/diagram_*.svg
    content = re.sub(
        r'!\[([^\]]+)\]\(diagrams/([^)]+)\)',
        r'![\1](../assets/diagrams/\2)',
        content
    )

    return content

def enhance_with_new_layouts(content: str) -> str:
    """
    新しいレイアウトを適用できる箇所を検出して適用

    - layout-callout: 「〜とは」「重要」「原則」などのキーワード
    - layout-comparison: 「vs」「比較」などのキーワード
    """
    lines = content.split('\n')
    new_lines = []

    for i, line in enumerate(lines):
        # 「〜とは」のスライドを layout-callout に
        if line.startswith('# ') and ('とは' in line or '原則' in line):
            # 直前の _class を layout-callout に変更
            for j in range(len(new_lines) - 1, max(len(new_lines) - 5, -1), -1):
                if '<!-- _class:' in new_lines[j]:
                    new_lines[j] = '<!-- _class: layout-callout -->'
                    break

        new_lines.append(line)

    return '\n'.join(new_lines)

def convert_backup_file(backup_path: Path, output_path: Path):
    """
    バックアップファイルを最新テーマに変換
    """
    print(f"Converting: {backup_path.name} → {output_path.name}")

    # ファイル読み込み
    with open(backup_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 変換処理
    content = update_frontmatter(content)
    content = update_diagram_paths(content)
    content = enhance_with_new_layouts(content)

    # 出力
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✓ Converted successfully")

def main():
    # パス設定
    backup_dir = Path('/home/cuzic/ai-dev-yodoq/slides/backups')
    output_dir = Path('/home/cuzic/ai-dev-yodoq/slides')

    # 変換対象ファイル
    files_to_convert = [
        ('day1_2.md.backup', 'day1_2.md'),
        ('day1_3.md.backup', 'day1_3.md'),
        ('day2_1.md.backup', 'day2_1.md'),
        ('day2_2.md.backup', 'day2_2.md'),
    ]

    print("=== バックアップファイルを最新テーマに変換 ===\n")

    for backup_name, output_name in files_to_convert:
        backup_path = backup_dir / backup_name
        output_path = output_dir / output_name

        if not backup_path.exists():
            print(f"  ✗ Backup not found: {backup_name}")
            continue

        convert_backup_file(backup_path, output_path)

    print("\n=== 変換完了 ===")
    print("\n次のステップ:")
    print("  1. スライドを確認: npx @marp-team/marp-cli slides/day1_2.md --theme-set assets/themes/ -o build/slides/day1_2.html --html")
    print("  2. 問題なければコミット: git add slides/ && git commit -m 'refactor: Convert slides to ai-seminar theme'")

if __name__ == '__main__':
    main()
