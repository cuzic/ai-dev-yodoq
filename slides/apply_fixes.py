"""
Apply compact/supercompact classes to slides based on fix plan
"""
import json
import re
from pathlib import Path
from typing import List, Dict

# Load fix plan
fix_plan_file = Path("/home/cuzic/ai-dev-yodoq/.state/measure/fix_plan.json")
with open(fix_plan_file, "r") as f:
    fix_plan = json.load(f)

# Create slide number to fix mapping
slide_fixes = {}

for slide in fix_plan["phase1_compact"]:
    slide_fixes[slide["slide_number"]] = "compact"

for slide in fix_plan["phase2_supercompact"]:
    slide_fixes[slide["slide_number"]] = "supercompact"

print(f"Total slides to fix: {len(slide_fixes)}")
print(f"  Compact: {len(fix_plan['phase1_compact'])}")
print(f"  Supercompact: {len(fix_plan['phase2_supercompact'])}")

# Process each markdown file
files = ["day1_1.md", "day1_2.md", "day1_3.md", "day2_1.md", "day2_2.md"]
slide_counter = 0
modifications = {}

for filename in files:
    filepath = Path(f"/home/cuzic/ai-dev-yodoq/slides/{filename}")
    print(f"\nProcessing {filename}...")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by slides
    slides = content.split("\n---\n")
    modified_slides = []
    file_mods = []

    for i, slide in enumerate(slides):
        # Skip frontmatter (first slide if it starts with ---)
        if i == 0 and slide.strip().startswith("---\nmarp:"):
            modified_slides.append(slide)
            continue

        slide_counter += 1

        # Check if this slide needs fixing
        if slide_counter in slide_fixes:
            fix_type = slide_fixes[slide_counter]

            # Check if slide already has the class
            if fix_type in slide:
                print(f"  Slide {slide_counter}: Already has '{fix_type}' class")
                modified_slides.append(slide)
                continue

            # Apply fix based on current structure
            if "<!-- _class:" in slide:
                # Has existing class directive
                class_match = re.search(r'<!-- _class: (.+?) -->', slide)
                if class_match:
                    current_classes = class_match.group(1)

                    # Check if already compact/supercompact
                    if "compact" in current_classes and fix_type == "supercompact":
                        # Upgrade compact to supercompact
                        new_classes = current_classes.replace("compact", "supercompact")
                        modified_slide = re.sub(
                            r'<!-- _class: .+? -->',
                            f'<!-- _class: {new_classes} -->',
                            slide
                        )
                        file_mods.append((slide_counter, "upgrade", f"{current_classes} -> {new_classes}"))
                    else:
                        # Add new class
                        new_classes = f"{current_classes} {fix_type}"
                        modified_slide = re.sub(
                            r'<!-- _class: .+? -->',
                            f'<!-- _class: {new_classes} -->',
                            slide
                        )
                        file_mods.append((slide_counter, "add", f"{current_classes} -> {new_classes}"))

                    modified_slides.append(modified_slide)
                else:
                    modified_slides.append(slide)
            else:
                # No class directive, add one after first line (usually # Title)
                lines = slide.split("\n")
                if len(lines) > 1 and lines[0].startswith("#"):
                    # Insert after title
                    lines.insert(1, f"<!-- _class: {fix_type} -->")
                    modified_slide = "\n".join(lines)
                    modified_slides.append(modified_slide)
                    file_mods.append((slide_counter, "insert", fix_type))
                else:
                    # Insert at beginning
                    modified_slide = f"<!-- _class: {fix_type} -->\n{slide}"
                    modified_slides.append(modified_slide)
                    file_mods.append((slide_counter, "insert", fix_type))
        else:
            modified_slides.append(slide)

    # Save modifications for this file
    if file_mods:
        modifications[filename] = file_mods

        # Write modified content
        new_content = "\n---\n".join(modified_slides)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"  Applied {len(file_mods)} fixes")

# Print summary
print("\n" + "=" * 70)
print("MODIFICATIONS SUMMARY")
print("=" * 70)

total_mods = sum(len(mods) for mods in modifications.values())
print(f"Total modifications: {total_mods}")

for filename, mods in modifications.items():
    print(f"\n{filename} ({len(mods)} changes):")
    for slide_num, action, detail in mods[:5]:
        print(f"  Slide {slide_num}: {action} - {detail}")
    if len(mods) > 5:
        print(f"  ... and {len(mods) - 5} more")

print("\n" + "=" * 70)
