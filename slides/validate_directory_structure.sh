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
