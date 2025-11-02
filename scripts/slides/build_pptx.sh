#!/bin/bash
set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MARKDOWN_FILES=("day1_1.md" "day1_2.md" "day1_3.md" "day2_1.md" "day2_2.md")
COMBINED_MD="all_slides.md"
TEMP_PPTX="AI_Development_Training_2Days_temp.pptx"
FINAL_PPTX="AI_Development_Training_2Days.pptx"
SVG_DIR="diagrams"
CHROME_PATH="${CHROME_PATH:-$HOME/.cache/ms-playwright/chromium-1194/chrome-linux/chrome}"

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}  AI Development Training - PPTX Build Script${NC}"
echo -e "${BLUE}======================================================${NC}\n"

# Step 1: Combine markdown files
echo -e "${YELLOW}[1/4] Combining markdown files...${NC}"
cat "${MARKDOWN_FILES[@]}" > "$COMBINED_MD"
SLIDE_COUNT=$(grep -c "^---$" "$COMBINED_MD" || true)
echo -e "${GREEN}✓ Combined ${#MARKDOWN_FILES[@]} files into $COMBINED_MD (approx. $SLIDE_COUNT slides)${NC}\n"

# Step 2: Check if Chrome/Chromium is available
echo -e "${YELLOW}[2/4] Checking browser availability...${NC}"
if [ -f "$CHROME_PATH" ]; then
    echo -e "${GREEN}✓ Found Chrome at: $CHROME_PATH${NC}\n"
    export CHROME_PATH
elif command -v chromium &> /dev/null; then
    export CHROME_PATH=$(command -v chromium)
    echo -e "${GREEN}✓ Found Chromium at: $CHROME_PATH${NC}\n"
elif command -v google-chrome &> /dev/null; then
    export CHROME_PATH=$(command -v google-chrome)
    echo -e "${GREEN}✓ Found Chrome at: $CHROME_PATH${NC}\n"
else
    echo -e "${RED}✗ No suitable browser found!${NC}"
    echo -e "${YELLOW}  Please install Chrome/Chromium or set CHROME_PATH environment variable${NC}"
    exit 1
fi

# Step 3: Generate PPTX with Marp
echo -e "${YELLOW}[3/4] Generating PPTX with Marp CLI...${NC}"
echo -e "${BLUE}  This may take several minutes...${NC}"

# Check if marp is available
if ! command -v npx &> /dev/null; then
    echo -e "${RED}✗ npx not found! Please install Node.js and npm${NC}"
    exit 1
fi

# Run marp with timeout
timeout 600 npx -y @marp-team/marp-cli@latest \
    "$COMBINED_MD" \
    --pptx \
    --allow-local-files \
    --image-scale 1 \
    -o "$TEMP_PPTX" \
    2>&1 | while IFS= read -r line; do
        echo "  $line"
    done

if [ ! -f "$TEMP_PPTX" ]; then
    echo -e "${RED}✗ Failed to generate PPTX${NC}"
    exit 1
fi

TEMP_SIZE=$(ls -lh "$TEMP_PPTX" | awk '{print $5}')
echo -e "${GREEN}✓ Generated temporary PPTX: $TEMP_PPTX ($TEMP_SIZE)${NC}\n"

# Step 4: Replace PNG images with SVG
echo -e "${YELLOW}[4/4] Replacing bitmap images with SVG...${NC}"

# Check if Python script exists
if [ ! -f "replace_with_svg.py" ]; then
    echo -e "${RED}✗ replace_with_svg.py not found!${NC}"
    exit 1
fi

# Install Python dependencies if needed
if ! python3 -c "import pptx" 2>/dev/null; then
    echo -e "${BLUE}  Installing python-pptx...${NC}"
    pip install python-pptx -q
fi

# Run Python script to replace images
python3 - <<'PYTHON_SCRIPT'
import sys
import os
sys.path.insert(0, os.getcwd())
from replace_with_svg import replace_images_with_svg

replace_images_with_svg(
    pptx_path="AI_Development_Training_2Days_temp.pptx",
    svg_dir="diagrams",
    output_path="AI_Development_Training_2Days.pptx",
    markdown_path="all_slides.md"
)
PYTHON_SCRIPT

if [ ! -f "$FINAL_PPTX" ]; then
    echo -e "${RED}✗ Failed to create final PPTX with SVG${NC}"
    exit 1
fi

# Clean up temporary PPTX
rm -f "$TEMP_PPTX"

# Final statistics
FINAL_SIZE=$(ls -lh "$FINAL_PPTX" | awk '{print $5}')
SVG_COUNT=$(unzip -l "$FINAL_PPTX" 2>/dev/null | grep -c "\.svg$" || echo "0")

echo -e "\n${BLUE}======================================================${NC}"
echo -e "${GREEN}✅ BUILD COMPLETE!${NC}"
echo -e "${BLUE}======================================================${NC}"
echo -e "Output file:  ${GREEN}$FINAL_PPTX${NC}"
echo -e "File size:    ${GREEN}$FINAL_SIZE${NC}"
echo -e "SVG images:   ${GREEN}$SVG_COUNT${NC}"
echo -e "Slides:       ${GREEN}~$SLIDE_COUNT${NC}"
echo -e "${BLUE}======================================================${NC}\n"

echo -e "${YELLOW}💡 Tip: Open in PowerPoint 2019+ for best SVG rendering${NC}\n"
