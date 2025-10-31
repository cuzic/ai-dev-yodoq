#!/bin/bash

# Slide 4: Still overflowing
sed -i 's/得意（コード生成・テスト）、苦手（ビジネス要件・判断）/得意:コード・テスト、苦手:要件・判断/' all_slides.md

# Slide 7: Minor overflow
sed -i 's/Trust but Verify、Living Doc/TbV・Living Doc/' all_slides.md

# Slide 66: Very minor
# Skip - only 8px overflow, acceptable

# Slide 67: 908px - very long
sed -i 's/「POST \/api\/register を TDD で実装して。Given-When-Then形式のテストを書き、正常系・異常系をカバーして」/「POST \/api\/register を TDD で実装。GWT形式、正常・異常系カバー」/' all_slides.md

# Slide 73: 858px - very long
sed -i 's/「このコードをレビューして。セキュリティ・エラー処理・エッジケース・ベストプラクティスをチェック」/「コードレビュー。セキュリティ・エラー・エッジ・ベストプラクティス」/' all_slides.md

# Slide 88: 752px - long
sed -i 's/「テストレビュー。エッジケース・異常系・境界値・独立性・Given-When-Thenをチェック」/「テストレビュー。エッジ・異常・境界・独立性・GWT」/' all_slides.md

# Slide 121: Already fixed earlier, but revert happened
sed -i 's/CLAUDE\.md更新（成功パターン・ハマった点）/CLAUDE\.md更新（パターン・知見）/' all_slides.md

echo "✅ Fixed remaining 6 overflow lines"
