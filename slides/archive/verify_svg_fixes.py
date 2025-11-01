#!/usr/bin/env python3
"""Quick SVG overflow verification after fixes."""

import re
from pathlib import Path

diagrams_dir = Path(__file__).parent.parent / 'diagrams-web'

files_to_check = [
    'diagram_04_ai_memory.svg',
    'diagram_06_spec_structure.svg',
    'diagram_14_scenario_to_code.svg',
    'diagram_18_fit_gap_analysis.svg',
    'diagram_38_jagged_intelligence_examples.svg',
    'diagram_39_reward_hacking_examples.svg',
    'diagram_43_doc_automation_before_after.svg'
]

print("Verifying SVG fixes...\n")

for fname in files_to_check:
    fpath = diagrams_dir / fname
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if font-size overrides exist
    inline_styles = re.findall(r'style="[^"]*font-size:\s*(\d+)px[^"]*"', content)
    if inline_styles:
        sizes = [int(s) for s in inline_styles]
        print(f"✅ {fname}: Reduced font sizes: {sizes}")
    else:
        print(f"❌ {fname}: No inline font-size found")

print("\nDone!")
