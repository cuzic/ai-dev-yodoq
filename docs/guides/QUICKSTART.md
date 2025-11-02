# Quick Start Guide

## Build PPTX in 3 Steps

### Step 1: Install Dependencies

```bash
# Install Python package
pip install python-pptx

# Verify Node.js is installed
node --version  # Should show v14 or higher
```

### Step 2: Build

```bash
# Option A: Using Make (recommended)
make build

# Option B: Using Python script
python3 build_pptx.py

# Option C: Using Bash script
./build_pptx.sh
```

### Step 3: Open Result

```bash
# Open the generated PPTX
open AI_Development_Training_2Days.pptx          # macOS
xdg-open AI_Development_Training_2Days.pptx      # Linux
start AI_Development_Training_2Days.pptx         # Windows
```

## Common Commands

```bash
# Clean all generated files
make clean

# Test dependencies
make test

# Rebuild from scratch
make clean build

# Show help
make help
```

## File Sizes

- **Input**: 5 Markdown files (~500 KB total)
- **Diagrams**: 40+ SVG files (~2 MB total)
- **Output**: 1 PPTX file (~36 MB)

## Build Time

- **First build**: 5-10 minutes
- **Subsequent builds**: 5-10 minutes (Marp is slow)
- **SVG replacement**: ~10 seconds

## What Gets Generated

1. `all_slides.md` - Combined markdown (intermediate)
2. `AI_Development_Training_2Days.pptx` - Final PPTX with SVG

## Troubleshooting

### "No suitable browser found"

Install Playwright Chromium:
```bash
npx playwright install chromium
```

### "python-pptx not found"

Install the package:
```bash
pip install python-pptx
```

### Build hangs or takes too long

This is normal for the first time. Marp CLI needs to render 200+ slides with high-resolution images. Be patient or reduce `--image-scale` to 1 in the script.

## Next Steps

- Edit markdown files in this directory
- Run `make build` to regenerate
- All diagrams automatically update

For more details, see [README.md](README.md)
