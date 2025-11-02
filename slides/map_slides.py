#!/usr/bin/env python3
"""
Map slide numbers to source markdown files and line numbers
"""

import re

files = ['day1_1.md', 'day1_2.md', 'day1_3.md', 'day2_1.md', 'day2_2.md']
slides_to_find = [9, 112, 90, 58, 98, 135, 154, 81, 53, 116, 153, 146, 155, 141, 101]

slide_counter = 0
slide_map = {}

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, 1):
        # Detect slide separator
        if line.strip() == '---':
            slide_counter += 1
            slide_map[slide_counter] = {
                'file': filename,
                'line': line_num,
                'slide_num': slide_counter
            }

# Print mapping for slides we need to fix
print("="*80)
print("SLIDE NUMBER TO FILE MAPPING (Top 15 Worst Overflow)")
print("="*80)

for slide_num in slides_to_find:
    if slide_num in slide_map:
        info = slide_map[slide_num]
        print(f"Slide {slide_num}: {info['file']} around line {info['line']}")
    else:
        # Find the closest slide before this number
        closest = max([s for s in slide_map.keys() if s <= slide_num], default=None)
        if closest:
            info = slide_map[closest]
            print(f"Slide {slide_num}: Between slide {closest} in {info['file']} (line {info['line']})")

print("\n" + "="*80)
print("SLIDE DISTRIBUTION BY FILE")
print("="*80)

file_counts = {}
for info in slide_map.values():
    file_counts[info['file']] = file_counts.get(info['file'], 0) + 1

cumulative = 0
for filename in files:
    count = file_counts.get(filename, 0)
    start = cumulative + 1
    end = cumulative + count
    cumulative = end
    print(f"{filename}: Slides {start}-{end} ({count} slides)")
