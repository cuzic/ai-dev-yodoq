# slides/ ディレクトリ再構成提案

## 📋 現状の課題

現在のslides/ディレクトリ（38ファイル + 8ディレクトリ）:
- ✅ スライドソース（.md）とビルド成果物（.html, .pptx）が混在
- ✅ スクリプトとドキュメントが混在
- ✅ 中間ファイル（.json, .txt）が散在
- ✅ 設定ファイルがルートに散在

## 🎯 提案する新構成

```
slides/
├── src/                    # ソースファイル
│   ├── all_slides.md       # 統合スライド
│   ├── day1/               # 1日目スライド
│   │   ├── day1_1.md
│   │   ├── day1_2.md
│   │   └── day1_3.md
│   ├── day2/               # 2日目スライド
│   │   ├── day2_1.md
│   │   └── day2_2.md
│   └── backups/            # オリジナルバックアップ
│       ├── day1_1.md.backup
│       ├── day1_2.md.backup
│       ├── day1_3.md.backup
│       ├── day2_1.md.backup
│       └── day2_2.md.backup
│
├── assets/                 # 静的リソース
│   ├── diagrams/           # SVG図表（54ファイル）
│   ├── templates/          # SVGテンプレート
│   │   └── svg_templates/
│   └── themes/             # Marpテーマ
│       └── ai-seminar.css
│
├── scripts/                # スクリプト
│   ├── validate_svg_bounds.py
│   ├── build_pptx.sh
│   └── README.md           # スクリプト説明
│
├── docs/                   # ドキュメント
│   ├── README.md           # メインREADME（シンボリックリンク）
│   ├── QUICKSTART.md
│   ├── GITHUB_PAGES.md
│   ├── guides/             # ガイド類
│   │   ├── SVG_DESIGN_GUIDE.md
│   │   └── SVG_ASPECT_RATIO_GUIDE.md
│   └── archive/            # 旧レポート・提案書
│       └── (85 archived files)
│
├── output/                 # ビルド成果物
│   ├── html/               # HTML出力
│   │   ├── all_slides.html
│   │   ├── index.html
│   │   └── AI_Development_Training_2Days.html
│   ├── pptx/               # PowerPoint出力
│   │   └── AI_Development_Training_2Days.pptx
│   └── test/               # テスト出力
│       ├── compare_svgs.html
│       └── test_svgs.html
│
├── work/                   # 中間ファイル・作業ディレクトリ
│   ├── reports/            # 検証レポート
│   │   ├── validation_report.json
│   │   ├── svg_bounds_report.json
│   │   ├── layout_recommendations.json
│   │   └── slide_quality_scores.json
│   ├── logs/               # ログファイル
│   │   ├── overflow_report.txt
│   │   └── layout_review.txt
│   └── temp/               # 一時ファイル
│       └── *.tmp
│
├── .config/                # 設定ファイル（隠しディレクトリ）
│   ├── .build.config
│   ├── .mise.toml
│   ├── .python-version
│   └── BUILD_FLOW.txt
│
├── .claude/                # Claude Code設定（既存）
│   └── commands/
│
├── .gitignore              # Git設定（ルート）
├── Makefile                # ビルド設定（ルート）
├── pyproject.toml          # Python設定（ルート）
└── README.md               # メインREADME（ルート）
```

---

## 📂 各ディレクトリの役割

### 1. `src/` - ソースファイル
**目的**: Markdownスライドのソース管理

```
src/
├── all_slides.md          # 統合版（本番用）
├── day1/                  # 1日目（3ファイル）
├── day2/                  # 2日目（2ファイル）
└── backups/               # オリジナルバックアップ（5ファイル）
```

**メリット**:
- ✅ スライドソースが一箇所に集約
- ✅ 日ごとにディレクトリ分割で管理しやすい
- ✅ バックアップも明確に分離

**gitignore**: なし（すべてバージョン管理）

---

### 2. `assets/` - 静的リソース
**目的**: 画像、テーマ、テンプレートの管理

```
assets/
├── diagrams/              # 54 SVGファイル
├── templates/             # SVGテンプレート
│   └── svg_templates/
└── themes/                # Marpテーマ
    └── ai-seminar.css     # 15レイアウト定義
```

**メリット**:
- ✅ リソースファイルが一箇所に
- ✅ ビルド時に参照しやすい
- ✅ 静的ファイルとして明確

**gitignore**: なし（すべてバージョン管理）

---

### 3. `scripts/` - スクリプト
**目的**: 自動化スクリプトの集約

```
scripts/
├── validate_svg_bounds.py  # SVG境界チェック
├── build_pptx.sh           # PPTX変換
├── build.sh                # 統合ビルドスクリプト
└── README.md               # 各スクリプトの説明
```

**メリット**:
- ✅ スクリプトが一箇所に
- ✅ `scripts/validate_svg_bounds.py` のように明確
- ✅ 実行権限の管理が簡単

**gitignore**: なし（バージョン管理）

**使用例**:
```bash
python3 scripts/validate_svg_bounds.py
bash scripts/build_pptx.sh
```

---

### 4. `docs/` - ドキュメント
**目的**: ドキュメント類の集約

```
docs/
├── README.md              # メイン（ルートへのシンボリックリンク）
├── QUICKSTART.md
├── GITHUB_PAGES.md
├── guides/                # ガイド類
│   ├── SVG_DESIGN_GUIDE.md
│   └── SVG_ASPECT_RATIO_GUIDE.md
└── archive/               # 旧archive/を移動
    └── (85 files)
```

**メリット**:
- ✅ ドキュメントが一箇所に
- ✅ ガイド類をサブディレクトリで整理
- ✅ GitHub Pagesとの親和性

**gitignore**: なし（バージョン管理）

---

### 5. `output/` - ビルド成果物
**目的**: ビルド結果の出力先

```
output/
├── html/                  # HTML出力
│   ├── all_slides.html
│   ├── index.html
│   └── AI_Development_Training_2Days.html
├── pptx/                  # PowerPoint出力
│   └── AI_Development_Training_2Days.pptx
└── test/                  # テスト出力
    ├── compare_svgs.html
    └── test_svgs.html
```

**メリット**:
- ✅ ビルド成果物が一箇所に
- ✅ 形式ごとにサブディレクトリ
- ✅ クリーンアップが簡単（`rm -rf output/`）

**gitignore**: ✅ **全て除外**（.gitignore に追加）
```gitignore
# Build outputs
output/
*.html
*.pptx
```

---

### 6. `work/` - 中間ファイル・作業ディレクトリ
**目的**: 一時ファイル、レポート、ログの管理

```
work/
├── reports/               # 検証レポート（JSON）
│   ├── validation_report.json
│   ├── svg_bounds_report.json
│   ├── layout_recommendations.json
│   └── slide_quality_scores.json
├── logs/                  # ログファイル（TXT）
│   ├── overflow_report.txt
│   └── layout_review.txt
└── temp/                  # 一時ファイル
    └── *.tmp
```

**メリット**:
- ✅ 中間ファイルが一箇所に
- ✅ レポート/ログで分類
- ✅ クリーンアップが簡単

**gitignore**: ✅ **全て除外**
```gitignore
# Working files
work/
*.json
*.txt
*.log
```

---

### 7. `.config/` - 設定ファイル（オプション）
**目的**: 隠し設定ファイルの集約

```
.config/
├── .build.config
├── .mise.toml
├── .python-version
└── BUILD_FLOW.txt
```

**代替案**: ルートに残す（一般的）
- `.build.config`, `.mise.toml`, `.python-version` はルートが標準
- `BUILD_FLOW.txt` は `docs/` に移動

**推奨**: **.config/ は不要、ルートに残す**

---

## 🔧 Makefile・ビルドスクリプトの調整

### Makefile の更新例

```makefile
# 新しいパス
SRC_DIR = src
ASSETS_DIR = assets
OUTPUT_DIR = output
SCRIPTS_DIR = scripts
WORK_DIR = work

# ビルドターゲット
.PHONY: all clean html pptx validate

all: html pptx

html:
	npx @marp-team/marp-cli \
		--theme-set $(ASSETS_DIR)/themes/ \
		$(SRC_DIR)/all_slides.md \
		-o $(OUTPUT_DIR)/html/index.html \
		--html

pptx:
	bash $(SCRIPTS_DIR)/build_pptx.sh

validate:
	python3 $(SCRIPTS_DIR)/validate_svg_bounds.py

clean:
	rm -rf $(OUTPUT_DIR)/* $(WORK_DIR)/*
```

---

## 📋 移行手順

### Step 1: ディレクトリ作成
```bash
mkdir -p src/{day1,day2,backups}
mkdir -p assets/{diagrams,templates,themes}
mkdir -p scripts
mkdir -p docs/guides
mkdir -p output/{html,pptx,test}
mkdir -p work/{reports,logs,temp}
```

### Step 2: ファイル移動
```bash
# スライドソース
git mv all_slides.md src/
git mv day1_1.md day1_2.md day1_3.md src/day1/
git mv day2_1.md day2_2.md src/day2/
git mv *.md.backup src/backups/

# リソース
git mv diagrams assets/
git mv svg_templates assets/templates/
git mv themes assets/

# スクリプト
git mv validate_svg_bounds.py build_pptx.sh scripts/

# ドキュメント
git mv QUICKSTART.md GITHUB_PAGES.md docs/
git mv SVG_DESIGN_GUIDE.md SVG_ASPECT_RATIO_GUIDE.md docs/guides/
git mv archive docs/

# 出力ファイル（git管理外なので mv）
mv *.html output/html/
mv *.pptx output/pptx/
mv compare_svgs.html test_svgs.html output/test/

# 中間ファイル（git管理外なので mv）
mv *.json work/reports/
mv *.txt work/logs/
```

### Step 3: .gitignore 更新
```bash
cat >> .gitignore << 'EOF'

# Build outputs
output/
*.html
*.pptx

# Working files
work/
*.json
*.txt
*.log
EOF
```

### Step 4: スライドファイル内のパス更新
```bash
# スライドファイル内の相対パスを更新（重要）
# diagrams/ への参照: diagrams/ → ../assets/diagrams/
# ../diagrams-web/ への参照: そのまま（親ディレクトリを参照）

python3 << 'EOF'
import re
from pathlib import Path

def update_diagram_paths(file_path):
    """スライドファイル内の diagram パスを更新"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # diagrams/diagram_*.svg → ../assets/diagrams/diagram_*.svg
    # (ただし ../diagrams-web/ は変更しない)
    content = re.sub(
        r'\!\[([^\]]+)\]\(diagrams/([^)]+)\)',
        r'![\1](../assets/diagrams/\2)',
        content
    )

    # ../diagrams-web/ は親ディレクトリにあるのでそのまま
    # (src/day1/ から見て ../../diagrams-web/ ではなく ../../../diagrams-web/)
    # しかし、親プロジェクトの diagrams-web は slides/ の外なので、
    # src/day1/ から見ると ../../diagrams-web/ ではなく ../../../diagrams-web/

    # day1/, day2/ 配下に移動するファイルの場合
    if 'day1' in str(file_path) or 'day2' in str(file_path):
        # ../diagrams-web/ → ../../../diagrams-web/
        content = re.sub(
            r'\!\[([^\]]+)\]\(\.\./diagrams-web/([^)]+)\)',
            r'![\1](../../../diagrams-web/\2)',
            content
        )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")
    else:
        print(f"No changes: {file_path}")

# src/day1/*.md を更新
for md_file in Path('src/day1').glob('*.md'):
    update_diagram_paths(md_file)

# src/day2/*.md を更新
for md_file in Path('src/day2').glob('*.md'):
    update_diagram_paths(md_file)

# src/all_slides.md を更新（これは src/ 直下なので diagrams のみ更新）
all_slides = Path('src/all_slides.md')
if all_slides.exists():
    with open(all_slides, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(
        r'\!\[([^\]]+)\]\(diagrams/([^)]+)\)',
        r'![\1](../assets/diagrams/\2)',
        content
    )
    # src/ から見て ../../diagrams-web/ に変更
    content = re.sub(
        r'\!\[([^\]]+)\]\(\.\./diagrams-web/([^)]+)\)',
        r'![\1](../../diagrams-web/\2)',
        content
    )
    with open(all_slides, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated: {all_slides}")

print("Path updates complete!")
EOF
```

### Step 5: Makefile・スクリプト更新
```bash
# Makefile のパスを更新
sed -i 's|all_slides\.md|src/all_slides.md|g' Makefile
sed -i 's|day1_|src/day1/day1_|g' Makefile
sed -i 's|day2_|src/day2/day2_|g' Makefile
sed -i 's|themes/|assets/themes/|g' Makefile
sed -i 's|diagrams/|assets/diagrams/|g' Makefile

# スクリプトのパスを更新
find scripts/ -type f -name "*.py" -o -name "*.sh" | while read script; do
    sed -i 's|diagrams/|../assets/diagrams/|g' "$script"
    sed -i 's|themes/|../assets/themes/|g' "$script"
done
```

### Step 6: コミット
```bash
git add -A
git commit -m "refactor: Reorganize directory structure by role"
```

---

## 🤖 自動移行スクリプト

上記の手順を自動化した完全なスクリプト：

### `migrate_directory_structure.sh`

```bash
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
```

### 実行方法

```bash
# スクリプトに実行権限を付与
chmod +x migrate_directory_structure.sh

# 実行（ドライランではないので注意）
./migrate_directory_structure.sh

# 変更を確認
git status
git diff --cached

# 問題なければコミット
git commit -m "refactor: Reorganize directory structure by role"
```

---

## ✅ 移行後の検証

### 検証スクリプト

移行が正しく完了したかを確認するスクリプト：

```bash
#!/bin/bash
echo "=== ディレクトリ構成の検証 ==="

ERRORS=0

# 1. ディレクトリ構造の確認
echo "✓ ディレクトリ構造チェック..."
for dir in src/day1 src/day2 src/backups assets/diagrams assets/themes assets/templates scripts docs/guides output/html output/pptx work/reports work/logs; do
    if [ ! -d "$dir" ]; then
        echo "  ✗ 不足: $dir"
        ((ERRORS++))
    fi
done

# 2. 必須ファイルの確認
echo "✓ 必須ファイルチェック..."
for file in src/all_slides.md src/day1/day1_1.md src/day1/day1_2.md src/day1/day1_3.md src/day2/day2_1.md src/day2/day2_2.md assets/themes/ai-seminar.css; do
    if [ ! -f "$file" ]; then
        echo "  ✗ 不足: $file"
        ((ERRORS++))
    fi
done

# 3. パス更新の確認
echo "✓ パス更新チェック..."
if grep -r "diagrams/diagram_" src/*.md 2>/dev/null; then
    echo "  ✗ 古いパス 'diagrams/' が残っています"
    ((ERRORS++))
fi

# 4. ビルドテスト（Marp CLI が利用可能な場合）
if command -v marp &> /dev/null; then
    echo "✓ ビルドテスト..."
    if marp src/all_slides.md --theme-set assets/themes/ -o output/html/test.html --html 2>&1 | grep -i error; then
        echo "  ✗ ビルドエラー"
        ((ERRORS++))
    else
        echo "  ✓ ビルド成功"
        rm -f output/html/test.html
    fi
else
    echo "  ⚠ Marp CLI未インストール（ビルドテストスキップ）"
fi

# 結果
echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ 検証完了：問題なし"
    exit 0
else
    echo "❌ 検証失敗：$ERRORS 個のエラー"
    exit 1
fi
```

### 手動検証項目

1. **ディレクトリ構造**
   ```bash
   tree -L 2 -I 'node_modules|.git'
   ```
   期待される出力：
   ```
   slides/
   ├── src/
   │   ├── all_slides.md
   │   ├── day1/
   │   ├── day2/
   │   └── backups/
   ├── assets/
   │   ├── diagrams/
   │   ├── templates/
   │   └── themes/
   ├── scripts/
   ├── docs/
   ├── output/
   ├── work/
   ├── .claude/
   ├── Makefile
   ├── pyproject.toml
   └── README.md
   ```

2. **ビルドテスト**
   ```bash
   # HTML生成
   npx @marp-team/marp-cli src/all_slides.md \
       --theme-set assets/themes/ \
       -o output/html/test.html \
       --html

   # エラーがないことを確認
   echo $?  # 0 なら成功
   ```

3. **パス確認**
   ```bash
   # assets/diagrams/ への正しい相対パス
   grep "!\[.*\](.*assets/diagrams/" src/all_slides.md | head -3

   # diagrams-web/ への正しい相対パス
   grep "!\[.*\](.*diagrams-web/" src/all_slides.md | head -3
   ```

4. **Git状態確認**
   ```bash
   # すべての変更がステージングされているか
   git status

   # 変更の差分を確認
   git diff --cached --stat
   ```

---

## 🔄 ロールバック手順

万が一、移行後に問題が発生した場合のロールバック方法：

### 方法1: Git Reset（コミット前の場合）

```bash
# ステージングされた変更を取り消す
git reset --hard HEAD

# 追跡されていないファイル・ディレクトリを削除
git clean -fd

# 元の状態に戻ったことを確認
git status
```

### 方法2: Git Revert（コミット後の場合）

```bash
# 最新のコミットを取り消す
git revert HEAD

# または特定のコミットを取り消す
git log --oneline  # コミットハッシュを確認
git revert <commit-hash>
```

### 方法3: 手動ロールバック（バックアップがある場合）

```bash
# 事前にバックアップを取っていた場合
cp -r ../slides_backup/* .

# または特定のブランチに戻る
git checkout <branch-name>
```

### 推奨：移行前のバックアップ作成

```bash
# 移行前に必ずバックアップを取る
cd ..
cp -r slides slides_backup_$(date +%Y%m%d_%H%M%S)

# または Git ブランチを作成
cd slides
git checkout -b backup-before-restructure
git add -A
git commit -m "backup: Before directory restructure"
git checkout main  # または元のブランチ
```

---

## 📊 Before/After 比較

### Before（現在）
```
slides/
├── (38 files)          # 混在
├── diagrams/
├── themes/
├── svg_templates/
└── archive/
```

### After（提案）
```
slides/
├── src/                # ソース（11 files）
├── assets/             # リソース（3 dirs）
├── scripts/            # スクリプト（3 files）
├── docs/               # ドキュメント（5 files + archive）
├── output/             # 成果物（gitignore）
├── work/               # 中間（gitignore）
├── .claude/            # 設定
├── Makefile
├── pyproject.toml
└── README.md
```

**メリット**:
- ✅ **役割ごとに明確に分離**
- ✅ **ビルド成果物・中間ファイルをgitignore**
- ✅ **クリーンアップが簡単**（`rm -rf output/ work/`）
- ✅ **スケーラブル**（ファイル増加に対応）
- ✅ **標準的なプロジェクト構成**

---

## 🎯 推奨構成サマリー

| ディレクトリ | 役割 | gitignore | ファイル数 |
|------------|------|----------|----------|
| `src/` | スライドソース | ❌ 管理対象 | 11 |
| `assets/` | 静的リソース | ❌ 管理対象 | ~60 |
| `scripts/` | スクリプト | ❌ 管理対象 | 3 |
| `docs/` | ドキュメント | ❌ 管理対象 | 5 + archive |
| `output/` | ビルド成果物 | ✅ 除外 | - |
| `work/` | 中間ファイル | ✅ 除外 | - |

---

## 💡 代替案・バリエーション

### 案A: シンプル構成（最小限）
```
slides/
├── slides/             # src/ の代わり
├── assets/
├── tools/              # scripts/ の代わり
├── docs/
└── dist/               # output/ の代わり
```

### 案B: モノレポ風
```
slides/
├── packages/
│   ├── slides/         # スライド本体
│   ├── themes/         # テーマパッケージ
│   └── diagrams/       # 図表パッケージ
├── scripts/
└── docs/
```

### 案C: 提案構成（推奨）
上記の詳細構成

---

## 🚀 次のアクション

このディレクトリ再構成を実施する準備ができました。以下のスクリプトが用意されています：

### 📦 提供されるファイル

1. **`DIRECTORY_RESTRUCTURE_PROPOSAL.md`** (本ドキュメント)
   - 詳細な提案書と手順

2. **`migrate_directory_structure.sh`** (実行可能)
   - 完全自動移行スクリプト
   - ディレクトリ作成、ファイル移動、パス更新、Git staging まで実行

3. **`validate_directory_structure.sh`** (実行可能)
   - 移行後の検証スクリプト
   - ディレクトリ構造、ファイル存在、パス更新、ビルドテストを自動チェック

### 実行方法

#### オプション1: 完全自動実行（推奨）

```bash
# 1. バックアップ作成（推奨）
git checkout -b backup-before-restructure
git add -A
git commit -m "backup: Before directory restructure"
git checkout main

# 2. 移行実行
./migrate_directory_structure.sh

# 3. 検証
./validate_directory_structure.sh

# 4. 確認してコミット
git status
git diff --cached
git commit -m "refactor: Reorganize directory structure by role"
```

#### オプション2: 段階的実行

```bash
# Step 1-2 のみ実行（ディレクトリ作成・ファイル移動）
# スクリプトを編集して必要な部分のみ実行

# または、手動で一部のみ移行
mkdir -p output work
mv *.html output/ 2>/dev/null || true
mv *.json work/ 2>/dev/null || true
```

#### オプション3: カスタマイズ

- `migrate_directory_structure.sh` を編集して構成を変更
- 例: `scripts/` を `tools/` に変更、`src/` を `slides/` のままに

#### オプション4: 現状維持

- 何もしない（提案のみ参照）

---

## 📝 まとめ

### 実施済み

✅ CSS一元化（`themes/ai-seminar.css` 作成済み）
✅ 15レイアウト対応（`/generate-slides` 更新済み）
✅ アーカイブ整理（23ファイル移動済み）

### 次のステップ（本提案）

🔜 ディレクトリ構造の役割別整理
🔜 ビルド成果物の分離（gitignore）
🔜 スケーラブルな構成への移行

---

**作成日**: 2025-11-02
**バージョン**: 1.1
**更新**: 自動移行スクリプト・検証スクリプト追加
