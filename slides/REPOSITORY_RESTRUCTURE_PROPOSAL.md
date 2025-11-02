# リポジトリ全体の再構成提案（トップレベル活用）

## 📋 現状の課題

### 重複・混在の問題

1. **diagrams/ の重複**
   - `/diagrams/` (49ファイル)
   - `/slides/diagrams/` (49ファイル) ← 同一内容

2. **ディレクトリの二重構造**
   - `/docs/` (GitHub Pages)
   - `/scripts/` (verify_layout.py)
   - 提案では `slides/docs/`, `slides/scripts/` も作る予定 → 混乱

3. **レポートファイルがトップに散在**
   - `FINAL_OVERFLOW_REPORT.md`
   - `OVERFLOW_FIX_COMPLETE.md`
   - `SVG_RECREATION_COMPLETE.md`
   - 等、6ファイル以上

---

## 🎯 提案する新構成

### 構成パターン: トップレベル活用型

```
ai-dev-yodoq/                    # リポジトリルート
│
├── slides/                      # スライドソース（Markdown）
│   ├── day1_1.md
│   ├── day1_2.md
│   ├── day1_3.md
│   ├── day2_1.md
│   ├── day2_2.md
│   ├── all_slides.md
│   └── backups/                 # バックアップ
│       ├── day1_1.md.backup
│       └── ...
│
├── assets/                      # 共有リソース（全プロジェクト用）
│   ├── diagrams/                # SVG図表（49ファイル）
│   ├── diagrams-web/            # Web用図表
│   ├── themes/                  # Marpテーマ
│   │   └── ai-seminar.css
│   └── templates/               # SVGテンプレート
│       └── svg_templates/
│
├── docs/                        # ドキュメント（GitHub Pages用、既存）
│   ├── index.html               # GitHub Pages
│   ├── diagram_prompts.md
│   ├── LAYOUT_GUIDE.md
│   ├── V4_NEW_TOPICS.md
│   ├── guides/                  # 追加：ガイド類
│   │   ├── SVG_DESIGN_GUIDE.md
│   │   └── SVG_ASPECT_RATIO_GUIDE.md
│   └── reports/                 # 追加：レポート類
│       ├── FINAL_OVERFLOW_REPORT.md
│       ├── SVG_RECREATION_COMPLETE.md
│       └── ...
│
├── scripts/                     # スクリプト（全プロジェクト用）
│   ├── slides/                  # スライド関連
│   │   ├── build_pptx.sh
│   │   └── validate_svg_bounds.py
│   └── validation/              # 検証関連
│       └── verify_layout.py
│
├── build/                       # ビルド成果物（既存、gitignore）
│   ├── slides/                  # スライドHTML/PPTX
│   └── docs/                    # ドキュメントビルド
│
├── archive/                     # アーカイブ（トップレベル）
│   ├── reports/                 # 旧レポート
│   ├── slides/                  # 旧スライド
│   └── scripts/                 # 旧スクリプト
│
├── .claude/                     # Claude Code設定
│   └── commands/
│
├── .github/                     # GitHub設定
├── .venv/                       # Python仮想環境（gitignore）
├── node_modules/                # Node依存関係（gitignore）
│
├── .gitignore
├── package.json
├── package-lock.json
├── pyproject.toml
├── .mise.toml
├── .nvmrc
├── .python-version
└── README.md
```

---

## 📂 各ディレクトリの役割

### 1. `slides/` - スライドソース（Markdown のみ）

**内容:**
- Markdownファイルのみ（6ファイル）
- バックアップ（5ファイル）

**メリット:**
- スライドソースが明確に分離
- ビルドリソース（diagrams, themes）はトップレベルの `assets/` に集約
- シンプルで見通しが良い

**パス:**
- `![図](../assets/diagrams/diagram_01.svg)` - 1階層上の assets/
- テーマ: `--theme-set ../assets/themes/`

---

### 2. `assets/` - 共有リソース（新規作成）

**内容:**
- `diagrams/` - SVG図表（49ファイル）
- `diagrams-web/` - Web用図表
- `themes/` - Marpテーマ（ai-seminar.css）
- `templates/svg_templates/` - SVGテンプレート

**メリット:**
- リソースが一箇所に集約
- スライド以外のプロジェクトからも参照可能
- `/diagrams/` と `/slides/diagrams/` の重複を解消

**移行:**
```bash
# slides/diagrams/ を削除（トップの diagrams/ が既にある）
rm -rf slides/diagrams/

# トップの diagrams/ を assets/ に移動
git mv diagrams/ assets/diagrams/
git mv diagrams-web/ assets/diagrams-web/
git mv slides/themes/ assets/themes/
git mv slides/svg_templates/ assets/templates/svg_templates/
```

---

### 3. `docs/` - ドキュメント（既存、拡張）

**既存内容:**
- GitHub Pages用（index.html, _config.yml, .nojekyll）
- diagram_prompts.md, LAYOUT_GUIDE.md, V4_NEW_TOPICS.md

**追加内容:**
- `guides/` - ガイド類（SVG_DESIGN_GUIDE.md 等）
- `reports/` - レポート類（散在している *_REPORT.md を集約）

**メリット:**
- ドキュメントが一箇所に
- GitHub Pagesと共存
- トップに散在するレポートを整理

**移行:**
```bash
mkdir -p docs/guides docs/reports

# ガイド類を移動（slides/ から）
git mv slides/SVG_DESIGN_GUIDE.md docs/guides/
git mv slides/SVG_ASPECT_RATIO_GUIDE.md docs/guides/

# レポート類を移動（トップから）
git mv FINAL_OVERFLOW_REPORT.md docs/reports/
git mv OVERFLOW_FIX_COMPLETE.md docs/reports/
git mv OVERFLOW_FIX_FINAL_REPORT.md docs/reports/
git mv LAYOUT_REVIEW_SUMMARY.md docs/reports/
git mv REMAINING_OVERFLOW_FIXES.md docs/reports/
git mv SVG_RECREATION_COMPLETE.md docs/reports/
```

---

### 4. `scripts/` - スクリプト（既存、拡張）

**既存内容:**
- `verify_layout.py`

**追加内容:**
- `slides/` - スライド関連スクリプト
  - `build_pptx.sh`
  - `validate_svg_bounds.py`
- `validation/` - 検証関連スクリプト（既存の verify_layout.py）

**メリット:**
- スクリプトが一箇所に、用途別サブディレクトリで整理
- 実行時のパスが明確

**移行:**
```bash
mkdir -p scripts/slides scripts/validation

# スライド関連スクリプトを移動
git mv slides/build_pptx.sh scripts/slides/
git mv slides/validate_svg_bounds.py scripts/slides/

# 既存スクリプトを整理
git mv scripts/verify_layout.py scripts/validation/
```

---

### 5. `build/` - ビルド成果物（既存、gitignore）

**内容:**
- `slides/` - HTML, PPTX
- `docs/` - ドキュメントビルド

**メリット:**
- 既存の `build/` ディレクトリを活用
- すべてのビルド成果物が一箇所に
- `.gitignore` で除外済み

**Makefile 更新:**
```makefile
OUTPUT_DIR = build/slides

html:
	npx @marp-team/marp-cli slides/all_slides.md \
		--theme-set assets/themes/ \
		-o $(OUTPUT_DIR)/index.html \
		--html
```

---

### 6. `archive/` - アーカイブ（新規作成）

**内容:**
- `slides/archive/` を移動
- その他の古いファイル

**メリット:**
- アーカイブがトップレベルで明確に分離
- プロジェクト全体のアーカイブを一元管理

**移行:**
```bash
mkdir -p archive/slides
git mv slides/archive/* archive/slides/
```

---

## 🔧 Makefile・スクリプト更新

### Makefile

```makefile
# 新しいパス
SLIDES_DIR = slides
ASSETS_DIR = assets
OUTPUT_DIR = build/slides
SCRIPTS_DIR = scripts/slides

.PHONY: all clean html pptx validate

all: html pptx

html:
	npx @marp-team/marp-cli \
		--theme-set $(ASSETS_DIR)/themes/ \
		$(SLIDES_DIR)/all_slides.md \
		-o $(OUTPUT_DIR)/index.html \
		--html

pptx:
	bash $(SCRIPTS_DIR)/build_pptx.sh

validate:
	python3 $(SCRIPTS_DIR)/validate_svg_bounds.py

clean:
	rm -rf $(OUTPUT_DIR)/*
```

---

## 📋 移行手順

### Step 1: diagrams/ の重複解消

```bash
# slides/diagrams/ を削除（トップに同一内容がある）
rm -rf slides/diagrams/

# トップの diagrams/ を assets/ に移動
git mv diagrams assets/diagrams
git mv diagrams-web assets/diagrams-web
```

### Step 2: assets/ にリソース集約

```bash
mkdir -p assets/templates

# themes を移動
git mv slides/themes assets/themes

# svg_templates を移動
git mv slides/svg_templates assets/templates/svg_templates
```

### Step 3: docs/ にドキュメント集約

```bash
mkdir -p docs/guides docs/reports

# ガイド類を移動
git mv slides/SVG_DESIGN_GUIDE.md slides/SVG_ASPECT_RATIO_GUIDE.md docs/guides/ 2>/dev/null || true

# レポート類を移動
git mv *_REPORT.md *_SUMMARY.md *_COMPLETE.md docs/reports/ 2>/dev/null || true
```

### Step 4: scripts/ にスクリプト集約

```bash
mkdir -p scripts/slides scripts/validation

# スライド関連スクリプトを移動
git mv slides/build_pptx.sh slides/validate_svg_bounds.py scripts/slides/ 2>/dev/null || true

# 検証スクリプトを整理
git mv scripts/verify_layout.py scripts/validation/ 2>/dev/null || true
```

### Step 5: archive/ 整理

```bash
mkdir -p archive/slides

# slides/archive/ を移動
git mv slides/archive/* archive/slides/ 2>/dev/null || true
rmdir slides/archive 2>/dev/null || true
```

### Step 6: スライドファイル内のパス更新

```bash
# slides/*.md のパスを更新
python3 << 'EOF'
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

    # ../diagrams-web/ はそのまま（既にトップレベル参照）

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")

for md_file in Path('slides').glob('*.md'):
    update_paths(md_file)
EOF
```

### Step 7: .gitignore 更新

```bash
cat >> .gitignore << 'EOF'

# Build outputs
build/
*.html
*.pptx

# Temporary files
*.json
*.txt
*.log
EOF
```

### Step 8: Makefile 更新

```bash
# Makefile のパスを更新
sed -i.bak 's|slides/themes/|assets/themes/|g' Makefile 2>/dev/null || true
sed -i.bak 's|slides/diagrams/|assets/diagrams/|g' Makefile 2>/dev/null || true
rm Makefile.bak 2>/dev/null || true
```

### Step 9: コミット

```bash
git add -A
git commit -m "refactor: Reorganize repository structure using top-level directories"
```

---

## 🤖 自動移行スクリプト

### `migrate_to_toplevel.sh`

```bash
#!/bin/bash
set -e

echo "=== リポジトリ全体の再構成を開始します ==="

# 作業ディレクトリの確認
if [ ! -d "slides" ] || [ ! -f "README.md" ]; then
    echo "エラー: リポジトリルートで実行してください"
    exit 1
fi

echo "Step 1: diagrams/ の重複解消..."
# slides/diagrams/ を削除（トップに同一内容がある）
rm -rf slides/diagrams/

# トップの diagrams/ を assets/ に移動
mkdir -p assets
git mv diagrams assets/diagrams 2>/dev/null || mv diagrams assets/diagrams
git mv diagrams-web assets/diagrams-web 2>/dev/null || mv diagrams-web assets/diagrams-web

echo "Step 2: assets/ にリソース集約..."
mkdir -p assets/templates

git mv slides/themes assets/themes 2>/dev/null || mv slides/themes assets/themes
git mv slides/svg_templates assets/templates/svg_templates 2>/dev/null || mv slides/svg_templates assets/templates/svg_templates

echo "Step 3: docs/ にドキュメント集約..."
mkdir -p docs/guides docs/reports

# ガイド類を移動
for file in slides/SVG_DESIGN_GUIDE.md slides/SVG_ASPECT_RATIO_GUIDE.md slides/QUICKSTART.md slides/GITHUB_PAGES.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/guides/ 2>/dev/null || mv "$file" docs/guides/
    fi
done

# レポート類を移動
for file in *_REPORT.md *_SUMMARY.md *_COMPLETE.md; do
    if [ -f "$file" ]; then
        git mv "$file" docs/reports/ 2>/dev/null || mv "$file" docs/reports/
    fi
done

echo "Step 4: scripts/ にスクリプト集約..."
mkdir -p scripts/slides scripts/validation

# スライド関連スクリプトを移動
for file in slides/build_pptx.sh slides/validate_svg_bounds.py; do
    if [ -f "$file" ]; then
        git mv "$file" scripts/slides/ 2>/dev/null || mv "$file" scripts/slides/
    fi
done

# 検証スクリプトを整理
if [ -f "scripts/verify_layout.py" ]; then
    git mv scripts/verify_layout.py scripts/validation/ 2>/dev/null || mv scripts/verify_layout.py scripts/validation/
fi

echo "Step 5: archive/ 整理..."
mkdir -p archive/slides

if [ -d "slides/archive" ]; then
    git mv slides/archive/* archive/slides/ 2>/dev/null || mv slides/archive/* archive/slides/
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
        print(f"Updated: {file_path}")

for md_file in Path('slides').glob('*.md'):
    if not md_file.name.endswith('.backup'):
        update_paths(md_file)

for md_file in Path('slides/backups').glob('*.md.backup'):
    update_paths(md_file)

print("Path updates complete!")
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
fi

echo "Step 8: Makefile 更新..."
if [ -f "Makefile" ]; then
    sed -i.bak 's|slides/themes/|assets/themes/|g' Makefile
    sed -i.bak 's|slides/diagrams/|assets/diagrams/|g' Makefile
    rm Makefile.bak 2>/dev/null || true
fi

# スクリプトのパスを更新
find scripts/ -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null | while read script; do
    sed -i.bak 's|slides/diagrams/|../assets/diagrams/|g' "$script"
    sed -i.bak 's|slides/themes/|../assets/themes/|g' "$script"
    rm "${script}.bak" 2>/dev/null || true
done

echo "Step 9: backups ディレクトリ作成..."
mkdir -p slides/backups
mv slides/*.backup slides/backups/ 2>/dev/null || true

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
```

---

## 📊 Before/After 比較

### Before（現在）

```
ai-dev-yodoq/
├── diagrams/              # 49ファイル
├── diagrams-web/
├── slides/
│   ├── diagrams/          # 49ファイル（重複）
│   ├── themes/
│   ├── svg_templates/
│   ├── *.md               # 混在
│   └── archive/
├── docs/                  # GitHub Pages
├── scripts/               # 1ファイルのみ
├── *_REPORT.md            # 6ファイル散在
└── ...
```

### After（提案）

```
ai-dev-yodoq/
├── slides/                # Markdownのみ（6+5ファイル）
│   ├── *.md
│   └── backups/
├── assets/                # 共有リソース
│   ├── diagrams/          # 49ファイル（一元化）
│   ├── diagrams-web/
│   ├── themes/
│   └── templates/
├── docs/                  # ドキュメント（拡張）
│   ├── guides/            # 4ファイル
│   └── reports/           # 6ファイル（整理）
├── scripts/               # スクリプト（整理）
│   ├── slides/            # 2ファイル
│   └── validation/        # 1ファイル
├── build/                 # ビルド成果物（既存活用）
└── archive/               # アーカイブ（整理）
```

**メリット:**
- ✅ **重複解消** - `diagrams/` を一箇所に
- ✅ **役割明確化** - トップレベルで機能分離
- ✅ **スケーラブル** - プロジェクト拡大に対応
- ✅ **既存活用** - `docs/`, `scripts/`, `build/` を活用
- ✅ **整理整頓** - レポート・ガイド・アーカイブを集約

---

## 💡 代替案

### 案A: slides/ をサブプロジェクトとして独立（現在の提案との比較）

現在の提案（`DIRECTORY_RESTRUCTURE_PROPOSAL.md`）:
```
slides/
├── src/                   # スライドソース
├── assets/                # スライド専用リソース
├── scripts/               # スライド専用スクリプト
├── docs/                  # スライド専用ドキュメント
├── output/                # スライド専用出力
└── work/                  # スライド専用作業
```

**メリット:**
- スライドが完全に独立
- `slides/` 内で完結

**デメリット:**
- トップレベルとの重複（`docs/`, `scripts/`）
- リソースの共有が困難

### 案B: トップレベル活用（本提案）✅

```
ai-dev-yodoq/
├── slides/                # スライドソースのみ
├── assets/                # 共有リソース
├── docs/                  # 共有ドキュメント
├── scripts/               # 共有スクリプト
└── build/                 # 共有ビルド
```

**メリット:**
- 重複なし
- リソース共有容易
- トップレベル既存構造を活用

**デメリット:**
- スライド以外のプロジェクトが増えた場合、構成変更が必要

---

## 🚀 次のアクション

### オプション1: トップレベル活用（本提案、推奨）

```bash
# バックアップ作成
git checkout -b backup-before-toplevel-restructure
git add -A
git commit -m "backup: Before top-level restructure"
git checkout main

# 移行実行
chmod +x migrate_to_toplevel.sh
./migrate_to_toplevel.sh

# コミット
git status
git commit -m "refactor: Reorganize repository structure using top-level directories"
```

### オプション2: slides/ 内完結（前回提案）

```bash
# slides/ ディレクトリ内で完結させる
./slides/migrate_directory_structure.sh
```

### オプション3: カスタマイズ

スクリプトを編集して独自の構成に

---

**作成日**: 2025-11-02
**バージョン**: 2.0（トップレベル活用版）
