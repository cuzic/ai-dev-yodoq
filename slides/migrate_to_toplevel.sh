#!/bin/bash
set -e

echo "=== リポジトリ全体の再構成を開始します ==="

# 作業ディレクトリの確認
if [ ! -d "slides" ] || [ ! -f "README.md" ]; then
    echo "エラー: リポジトリルートで実行してください"
    echo "現在のディレクトリ: $(pwd)"
    echo "期待: /home/cuzic/ai-dev-yodoq/"
    exit 1
fi

echo "Step 1: diagrams/ の重複解消..."
# slides/diagrams/ を削除（トップに同一内容がある）
if [ -d "slides/diagrams" ]; then
    echo "  slides/diagrams/ を削除（トップに同一内容があります）"
    rm -rf slides/diagrams/
fi

# トップの diagrams/ を assets/ に移動
mkdir -p assets
if [ -d "diagrams" ]; then
    git mv diagrams assets/diagrams 2>/dev/null || mv diagrams assets/diagrams
    echo "  diagrams/ → assets/diagrams/"
fi
if [ -d "diagrams-web" ]; then
    git mv diagrams-web assets/diagrams-web 2>/dev/null || mv diagrams-web assets/diagrams-web
    echo "  diagrams-web/ → assets/diagrams-web/"
fi

echo "Step 2: assets/ にリソース集約..."
mkdir -p assets/templates

if [ -d "slides/themes" ]; then
    git mv slides/themes assets/themes 2>/dev/null || mv slides/themes assets/themes
    echo "  slides/themes/ → assets/themes/"
fi
if [ -d "slides/svg_templates" ]; then
    git mv slides/svg_templates assets/templates/svg_templates 2>/dev/null || mv slides/svg_templates assets/templates/svg_templates
    echo "  slides/svg_templates/ → assets/templates/svg_templates/"
fi

echo "Step 3: docs/ にドキュメント集約..."
mkdir -p docs/guides docs/reports

# ガイド類を移動
for file in slides/SVG_DESIGN_GUIDE.md slides/SVG_ASPECT_RATIO_GUIDE.md slides/QUICKSTART.md slides/GITHUB_PAGES.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/guides/ 2>/dev/null || mv "$file" docs/guides/
        echo "  $(basename $file) → docs/guides/"
    fi
done

# レポート類を移動（トップレベルから）
cd .. 2>/dev/null || true
for file in *_REPORT.md *_SUMMARY.md *_COMPLETE.md; do
    if [ -f "$file" ] && [ "$file" != "*_REPORT.md" ]; then
        git mv "$file" docs/reports/ 2>/dev/null || mv "$file" docs/reports/
        echo "  $file → docs/reports/"
    fi
done
cd slides 2>/dev/null || true

echo "Step 4: scripts/ にスクリプト集約..."
mkdir -p scripts/slides scripts/validation

# スライド関連スクリプトを移動
for file in slides/build_pptx.sh slides/validate_svg_bounds.py; do
    if [ -f "$file" ]; then
        git mv "$file" scripts/slides/ 2>/dev/null || mv "$file" scripts/slides/
        echo "  $(basename $file) → scripts/slides/"
    fi
done

# 検証スクリプトを整理
if [ -f "scripts/verify_layout.py" ]; then
    git mv scripts/verify_layout.py scripts/validation/ 2>/dev/null || mv scripts/verify_layout.py scripts/validation/
    echo "  verify_layout.py → scripts/validation/"
fi

echo "Step 5: archive/ 整理..."
mkdir -p archive/slides

if [ -d "slides/archive" ]; then
    if [ "$(ls -A slides/archive 2>/dev/null)" ]; then
        git mv slides/archive/* archive/slides/ 2>/dev/null || mv slides/archive/* archive/slides/
        echo "  slides/archive/* → archive/slides/"
    fi
    rmdir slides/archive 2>/dev/null || true
fi

echo "Step 6: スライドファイル内のパス更新..."
python3 << 'PYTHON_EOF'
import re
from pathlib import Path

def update_paths(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # diagrams/ → ../assets/diagrams/
    content = re.sub(
        r'!\[([^\]]+)\]\(diagrams/([^)]+)\)',
        r'![\1](../assets/diagrams/\2)',
        content
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {file_path}")

slides_dir = Path('slides')
if slides_dir.exists():
    for md_file in slides_dir.glob('*.md'):
        if not md_file.name.endswith('.backup'):
            update_paths(md_file)

backups_dir = Path('slides/backups')
if backups_dir.exists():
    for md_file in backups_dir.glob('*.md.backup'):
        update_paths(md_file)

print("  Path updates complete!")
PYTHON_EOF

echo "Step 7: .gitignore 更新..."
if ! grep -q "^build/" .gitignore 2>/dev/null; then
    cat >> .gitignore << 'GITIGNORE_EOF'

# Build outputs
build/
*.html
*.pptx

# Temporary files
*.json
*.txt
*.log
GITIGNORE_EOF
    echo "  .gitignore に build/, *.html, *.pptx を追加"
fi

echo "Step 8: Makefile 更新..."
if [ -f "Makefile" ]; then
    sed -i.bak 's|slides/themes/|assets/themes/|g' Makefile
    sed -i.bak 's|slides/diagrams/|assets/diagrams/|g' Makefile
    rm Makefile.bak 2>/dev/null || true
    echo "  Makefile のパスを更新"
fi

# スクリプトのパスを更新
find scripts/ -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null | while read script; do
    sed -i.bak 's|slides/diagrams/|../assets/diagrams/|g' "$script"
    sed -i.bak 's|slides/themes/|../assets/themes/|g' "$script"
    rm "${script}.bak" 2>/dev/null || true
done

echo "Step 9: backups ディレクトリ作成..."
mkdir -p slides/backups
if ls slides/*.backup 1> /dev/null 2>&1; then
    mv slides/*.backup slides/backups/ 2>/dev/null || true
    echo "  *.backup → slides/backups/"
fi

echo "Step 10: 変更をステージング..."
git add -A

echo ""
echo "=== 移行完了 ==="
echo ""
echo "次のコマンドでコミットしてください:"
echo "  git commit -m 'refactor: Reorganize repository structure using top-level directories'"
echo ""
echo "または、変更を確認してからコミット:"
echo "  git status"
echo "  git diff --cached"
