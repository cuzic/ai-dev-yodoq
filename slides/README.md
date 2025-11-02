# AI Development Training - Slide Build System

This directory contains the slide materials for the 2-day AI Development Training and automated build scripts to generate PPTX presentations with native SVG support.

## 📁 Structure

```
slides/
├── day1_1.md              # Day 1 Part 1: Fundamentals & STEP1-2
├── day1_2.md              # Day 1 Part 2: STEP3-5
├── day1_3.md              # Day 1 Part 3: Summary & Exercises
├── day2_1.md              # Day 2 Part 1: Reverse Engineering & Testing
├── day2_2.md              # Day 2 Part 2: Exercises & Summary
├── diagrams/              # SVG diagram files (symlink to ../diagrams)
├── build_pptx.py          # Python build script (recommended)
├── build_pptx.sh          # Bash build script (alternative)
├── replace_with_svg.py    # SVG replacement utility
├── Makefile               # Make-based build system
└── README.md              # This file
```

## 🚀 Quick Start

### Option 1: Using Make (Simplest)

```bash
# Build PPTX with SVG support
make build

# Clean generated files
make clean

# Test dependencies
make test

# Show help
make help
```

### Option 2: Using Python Script

```bash
# Run the build script
python3 build_pptx.py

# Or make it executable and run directly
chmod +x build_pptx.py
./build_pptx.py
```

### Option 3: Using Bash Script

```bash
# Run the build script
bash build_pptx.sh

# Or make it executable and run directly
chmod +x build_pptx.sh
./build_pptx.sh
```

## 📋 Prerequisites

### Required Software

1. **mise** - Modern dev tool version manager (recommended)
   ```bash
   # Install mise: https://mise.jdx.dev/
   curl https://mise.run | sh

   # Or use package manager
   # Debian/Ubuntu: apt install mise
   # macOS: brew install mise
   ```

2. **Node.js & npm** - For Marp CLI
   ```bash
   # Will be installed automatically by mise
   # Or check if installed: node --version
   ```

3. **Python 3.12+** - For SVG replacement
   ```bash
   # Will be installed automatically by mise
   # Or check if installed: python3 --version
   ```

4. **Chrome/Chromium** - For rendering slides
   ```bash
   # The script will auto-detect from:
   # - ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome
   # - System chromium/google-chrome

   # Or set manually:
   export CHROME_PATH=/path/to/chrome
   ```

### Python Dependencies

```bash
# Using mise (recommended)
mise install          # Install Python & Node
mise run install      # Install Python packages with uv

# Or manually
pip install python-pptx

# Dev dependencies (for linting/type checking)
mise run install
uv pip install ruff pyright
```

## 🔧 Build Process

The build system performs the following steps:

1. **Combine Markdown Files** → `all_slides.md`
   - Concatenates all 5 markdown files in order
   - Approximately 200+ slides

2. **Generate PPTX with Marp CLI** → `AI_Development_Training_2Days_temp.pptx`
   - Uses Marp CLI to convert markdown to PPTX
   - Renders diagrams as high-resolution bitmaps (PNG)

3. **Replace Bitmaps with SVG** → `AI_Development_Training_2Days.pptx`
   - Extracts PPTX (which is a ZIP file)
   - Replaces PNG images with corresponding SVG files
   - Updates all references and content types
   - Repackages as PPTX

4. **Cleanup**
   - Removes temporary files
   - Displays build summary

## 📊 Output

### Generated Files

- **`AI_Development_Training_2Days.pptx`** (Final, ~36 MB)
  - Contains native SVG images
  - Best quality, vector graphics
  - Recommended for PowerPoint 2019+

- **`all_slides.md`** (Intermediate)
  - Combined markdown source
  - Can be used directly with Marp

### File Sizes

- Original with PNG: ~40 MB
- With SVG replacement: ~36 MB
- HTML version: ~1.7 MB

### SVG Benefits

✅ Vector graphics (infinite scalability)
✅ Smaller file size
✅ Better rendering quality
✅ Easier to edit diagrams
✅ PowerPoint 2019+ native support

## 🎨 Customization

### Modifying Slides

1. Edit any of the 5 markdown files (`day1_*.md`, `day2_*.md`)
2. Run `make build` to regenerate PPTX
3. All diagrams will be automatically updated

### Adding New Diagrams

1. Add SVG file to `../diagrams/` directory
2. Reference in markdown: `![Description](../assets/diagrams/your_diagram.svg)`
3. Run `make build`

### Build Configuration

Edit variables in `build_pptx.py` or `Makefile`:

```python
# In build_pptx.py
markdown_files = ['day1_1.md', 'day1_2.md', ...]  # Source files
svg_dir = 'diagrams'                               # SVG directory
final_pptx = 'AI_Development_Training_2Days.pptx'  # Output name
```

## 🔍 Troubleshooting

### Issue: "No suitable browser found"

**Solution:**
```bash
# Option 1: Install Playwright Chromium
npx playwright install chromium

# Option 2: Set CHROME_PATH
export CHROME_PATH=/usr/bin/chromium

# Option 3: Install system Chrome
sudo apt install chromium-browser  # Debian/Ubuntu
brew install chromium               # macOS
```

### Issue: "Marp generation timed out"

**Solution:**
- Increase timeout in `build_pptx.py`:
  ```python
  generate_pptx_with_marp(markdown_file, output_file, timeout=1200)  # 20 min
  ```

### Issue: "SVG not found" warnings

**Solution:**
- Check if all referenced SVGs exist in `diagrams/`
- Verify symlink: `ls -la diagrams`
- Re-create symlink if needed:
  ```bash
  rm diagrams
  ln -s ../diagrams diagrams
  ```

### Issue: "python-pptx not found"

**Solution:**
```bash
pip install python-pptx
```

## 📖 Technical Details

### SVG Replacement Algorithm

1. **Extract PPTX structure** (unzip)
2. **Parse markdown** to get SVG reference order
3. **Map PNG files to SVG files** based on slide order
4. **Copy SVG files** to `ppt/media/` directory
5. **Update slide relationships** (`_rels/*.xml.rels`)
6. **Register SVG MIME type** in `[Content_Types].xml`
7. **Repackage as PPTX** (zip)

### File Format Support

- Input: Markdown (Marp syntax)
- Diagrams: SVG (Scalable Vector Graphics)
- Output: PPTX (Office Open XML)

## 🛠️ Development

### Code Quality Tools

The project uses modern Python tooling via **mise**:

```bash
# Lint code with ruff
mise run lint

# Format code with ruff
mise run format

# Type check with pyright
mise run typecheck

# Run all checks
mise run check

# Run unit tests
mise run test
```

### Testing Changes

```bash
# Test dependency check
make test

# Run comprehensive unit tests
make test-all

# Clean and rebuild
make clean build

# Build with bash script (alternative)
make build-bash
```

### Code Style

- **Formatter**: ruff (Black-compatible)
- **Linter**: ruff (replaces flake8, isort, pyupgrade)
- **Type Checker**: pyright
- **Line Length**: 100 characters
- **Python Version**: 3.12+

Configuration in `pyproject.toml` and `.mise.toml`.

### Adding New Build Targets

Edit `Makefile`:

```makefile
# Example: Build HTML version
build-html: $(COMBINED_MD)
	npx -y @marp-team/marp-cli@latest \
		$(COMBINED_MD) \
		--html \
		--allow-local-files \
		-o AI_Development_Training.html
```

Or add to `.mise.toml`:

```toml
[tasks.build-html]
description = "Build HTML version"
run = "npx -y @marp-team/marp-cli@latest all_slides.md --html --allow-local-files -o output.html"
```

## 📝 Notes

- **PowerPoint Version**: SVG images require PowerPoint 2019 or later
- **Build Time**: Initial build takes 5-10 minutes
- **Diagram Count**: 40+ SVG diagrams
- **Slide Count**: 200+ slides across 2 days

## 🤝 Contributing

When modifying slides:

1. Keep diagram references in sync
2. Test build after changes: `make build`
3. Verify SVG rendering in PowerPoint
4. Update this README if adding new features

## 📄 License

See parent directory for license information.
