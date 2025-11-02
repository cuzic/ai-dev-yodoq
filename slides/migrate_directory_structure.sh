#!/bin/bash
set -e  # エラーで停止

echo "=== ディレクトリ構成の再構成を開始します ==="

# 作業ディレクトリの確認
if [ ! -f "all_slides.md" ]; then
    echo "エラー: slides/ ディレクトリで実行してください"
    exit 1
fi

echo "Step 1: ディレクトリ作成中..."
mkdir -p src/{day1,day2,backups}
mkdir -p assets/{diagrams,templates,themes}
mkdir -p scripts
mkdir -p docs/guides
mkdir -p output/{html,pptx,test}
mkdir -p work/{reports,logs,temp}

echo "Step 2: ファイル移動中..."
# スライドソース
git mv all_slides.md src/ 2>/dev/null || mv all_slides.md src/
git mv day1_1.md day1_2.md day1_3.md src/day1/ 2>/dev/null || mv day1_1.md day1_2.md day1_3.md src/day1/
git mv day2_1.md day2_2.md src/day2/ 2>/dev/null || mv day2_1.md day2_2.md src/day2/
git mv *.md.backup src/backups/ 2>/dev/null || mv *.md.backup src/backups/ 2>/dev/null || true

# リソース
git mv diagrams assets/ 2>/dev/null || mv diagrams assets/
git mv svg_templates assets/templates/ 2>/dev/null || mv svg_templates assets/templates/
git mv themes assets/ 2>/dev/null || mv themes assets/

# スクリプト（存在するファイルのみ）
for file in validate_svg_bounds.py build_pptx.sh; do
    if [ -f "$file" ]; then
        git mv "$file" scripts/ 2>/dev/null || mv "$file" scripts/
    fi
done

# ドキュメント
for file in QUICKSTART.md GITHUB_PAGES.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/ 2>/dev/null || mv "$file" docs/
    fi
done
for file in SVG_DESIGN_GUIDE.md SVG_ASPECT_RATIO_GUIDE.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/guides/ 2>/dev/null || mv "$file" docs/guides/
    fi
done
if [ -d "archive" ]; then
    git mv archive docs/ 2>/dev/null || mv archive docs/
fi

# 出力ファイル（git管理外）
mv *.html output/html/ 2>/dev/null || true
mv *.pptx output/pptx/ 2>/dev/null || true
mv compare_svgs.html test_svgs.html output/test/ 2>/dev/null || true

# 中間ファイル（git管理外）
mv *.json work/reports/ 2>/dev/null || true
mv *.txt work/logs/ 2>/dev/null || true

echo "Step 3: .gitignore 更新中..."
cat >> .gitignore << 'GITIGNORE_EOF'

# Build outputs
output/
*.html
*.pptx

# Working files
work/
*.json
*.txt
*.log
GITIGNORE_EOF

echo "Step 4: スライドファイル内のパス更新中..."
python3 << 'PYTHON_EOF'
import re
from pathlib import Path

def update_diagram_paths(file_path):
    """スライドファイル内の diagram パスを更新"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # diagrams/diagram_*.svg → ../assets/diagrams/diagram_*.svg
    content = re.sub(
        r'!\[([^\]]+)\]\(diagrams/([^)]+)\)',
        r'![\1](../assets/diagrams/\2)',
        content
    )

    # day1/, day2/ 配下に移動するファイルの場合
    if 'day1' in str(file_path) or 'day2' in str(file_path):
        # ../diagrams-web/ → ../../../diagrams-web/
        content = re.sub(
            r'!\[([^\]]+)\]\(\.\./diagrams-web/([^)]+)\)',
            r'![\1](../../../diagrams-web/\2)',
            content
        )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")

# src/day1/*.md を更新
for md_file in Path('src/day1').glob('*.md'):
    update_diagram_paths(md_file)

# src/day2/*.md を更新
for md_file in Path('src/day2').glob('*.md'):
    update_diagram_paths(md_file)

# src/all_slides.md を更新
all_slides = Path('src/all_slides.md')
if all_slides.exists():
    with open(all_slides, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(
        r'!\[([^\]]+)\]\(diagrams/([^)]+)\)',
        r'![\1](../assets/diagrams/\2)',
        content
    )
    content = re.sub(
        r'!\[([^\]]+)\]\(\.\./diagrams-web/([^)]+)\)',
        r'![\1](../../diagrams-web/\2)',
        content
    )
    with open(all_slides, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {all_slides}")

print("Path updates complete!")
PYTHON_EOF

echo "Step 5: Makefile・スクリプト更新中..."
if [ -f "Makefile" ]; then
    sed -i.bak 's|all_slides\.md|src/all_slides.md|g' Makefile
    sed -i.bak 's|day1_|src/day1/day1_|g' Makefile
    sed -i.bak 's|day2_|src/day2/day2_|g' Makefile
    sed -i.bak 's|themes/|assets/themes/|g' Makefile
    sed -i.bak 's|diagrams/|assets/diagrams/|g' Makefile
    rm Makefile.bak
fi

# スクリプトのパスを更新
find scripts/ -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null | while read script; do
    sed -i.bak 's|diagrams/|../assets/diagrams/|g' "$script"
    sed -i.bak 's|themes/|../assets/themes/|g' "$script"
    rm "${script}.bak"
done

echo "Step 6: 変更をステージング中..."
git add -A

echo ""
echo "=== 移行完了 ==="
echo ""
echo "次のコマンドでコミットしてください:"
echo "  git commit -m 'refactor: Reorganize directory structure by role'"
echo ""
echo "または、変更を確認してからコミット:"
echo "  git status"
echo "  git diff --cached"
echo "  git commit -m 'refactor: Reorganize directory structure by role'"
