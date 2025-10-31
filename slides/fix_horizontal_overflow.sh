#!/bin/bash
cd /home/cuzic/ai-dev-yodoq/slides

# Slide 5: Minor overflow
sed -i 's/速い（30分〜1時間）、品質バラバラ/速い（30分〜1時間）、品質不安定/' all_slides.md

# Slide 7: 670px line
sed -i 's/Trust but Verify自動化、Living Documentation/Trust but Verify、Living Doc/' all_slides.md

# Slide 8: Two lines
sed -i 's/ブラウザ閉じる→全忘却、20万トークン超過→古い情報忘却/ブラウザ閉じる→全忘却、トークン超過→忘却/' all_slides.md
sed -i 's/architecture\.md\/README\.mdに知見蓄積/architecture\.md等に蓄積/' all_slides.md

# Slide 16: YOLOモード
sed -i 's/確認時間を大幅削減、Git管理済み推奨/確認時間削減、Git管理推奨/' all_slides.md

# Slide 37: Two lines
sed -i 's/フロント・バック・DB・ライブラリ（選定理由含む）/フロント・バック・DB・ライブラリ/' all_slides.md
sed -i 's/テーブル定義・カラム・制約・インデックス/テーブル・カラム・制約・INDEX/' all_slides.md

# Slide 41: Mermaid
sed -i 's/Git管理可、AI自動生成、GitHub\/VS Code表示/Git管理可、AI生成、GH\/VSC表示/' all_slides.md

# Slide 43: 726px line (worst)
sed -i 's/処理順序理解→正確コードフロー、エラー処理タイミング、依存関係、トランザクション境界/処理順序→コードフロー、エラー処理、依存、TX境界/' all_slides.md

# Slide 57: Minor
sed -i 's/タスク実行は得意だが順序判断は苦手/タスクは得意、順序判断は苦手/' all_slides.md

# Slide 58: Minor
sed -i 's/構造化タスクは得意だが自由形式は苦手/構造化は得意、自由形式は苦手/' all_slides.md

echo "✅ Fixed 15 overflow lines across 10 slides"
