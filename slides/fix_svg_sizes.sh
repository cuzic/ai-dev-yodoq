#!/bin/bash

# Fix SVG display sizes in all_slides.md by adding width specifications

# diagram_03 - ViewBox: 2400x450 -> display at 1100px width
sed -i 's|!\[5-STEPフロー\](diagrams/diagram_03_5step_flow.svg)|![width:1100px](diagrams/diagram_03_5step_flow.svg)|g' all_slides.md
sed -i 's|!\[5-STEPフロー全体\](diagrams/diagram_03_5step_flow.svg)|![width:1100px](diagrams/diagram_03_5step_flow.svg)|g' all_slides.md

# diagram_07 - ViewBox: 1400x1000 -> display at 900px width
sed -i 's|!\[ER図の例\](diagrams/diagram_07_er_diagram.svg)|![width:900px](diagrams/diagram_07_er_diagram.svg)|g' all_slides.md

# diagram_08 - ViewBox: 1800x545 -> display at 1000px width
sed -i 's|!\[ER図からコード生成\](diagrams/diagram_08_er_to_code.svg)|![width:1000px](diagrams/diagram_08_er_to_code.svg)|g' all_slides.md

# diagram_12 - ViewBox: 2200x700 -> display at 1100px width
sed -i 's|!\[リバースエンジニアリングのプロセス\](diagrams/diagram_12_reverse_engineering.svg)|![width:1100px](diagrams/diagram_12_reverse_engineering.svg)|g' all_slides.md

# diagram_17 - ViewBox: 2200x860 -> display at 1100px width
sed -i 's|!\[演習ワークフロー\](diagrams/diagram_17_workshop_workflow.svg)|![width:1100px](diagrams/diagram_17_workshop_workflow.svg)|g' all_slides.md

# diagram_26 - ViewBox: 1800x1650 -> display at 900px width
sed -i 's|!\[テストカバレッジ80%ルール\](diagrams/diagram_26_test_coverage_80_rule.svg)|![width:900px](diagrams/diagram_26_test_coverage_80_rule.svg)|g' all_slides.md

# diagram_36 - ViewBox: 2550x1270 -> display at 1100px width
sed -i 's|!\[Living Documentation構造\](diagrams/diagram_36_living_documentation.svg)|![width:1100px](diagrams/diagram_36_living_documentation.svg)|g' all_slides.md

# diagram_43 - ViewBox: 2100x1300 -> display at 1100px width
sed -i 's|!\[ドキュメント自動生成Before/After\](diagrams/diagram_43_doc_automation_before_after.svg)|![width:1100px](diagrams/diagram_43_doc_automation_before_after.svg)|g' all_slides.md

# diagram_46 - ViewBox: 1950x740 -> display at 1000px width
sed -i 's|!\[STEP2のまとめ\](diagrams/diagram_46_step2_summary.svg)|![width:1000px](diagrams/diagram_46_step2_summary.svg)|g' all_slides.md

echo "✅ Fixed SVG display sizes in all_slides.md"
