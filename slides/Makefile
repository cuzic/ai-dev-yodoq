.PHONY: all clean build test help

# Configuration
MARKDOWN_FILES := day1_1.md day1_2.md day1_3.md day2_1.md day2_2.md
COMBINED_MD := all_slides.md
FINAL_PPTX := AI_Development_Training_2Days.pptx
SVG_PPTX := AI_Development_Training_2Days_SVG.pptx
SVG_DIR := diagrams

# Default target
all: build

# Help target
help:
	@echo "AI Development Training - Build Targets"
	@echo "========================================"
	@echo ""
	@echo "  make build       - Build PPTX with SVG images (recommended)"
	@echo "  make clean       - Remove generated files"
	@echo "  make test        - Test dependencies"
	@echo "  make test-all    - Run comprehensive unit tests"
	@echo "  make combine     - Only combine markdown files"
	@echo "  make help        - Show this help message"
	@echo ""

# Test dependencies
test:
	@echo "Testing dependencies..."
	@command -v npx >/dev/null 2>&1 || (echo "✗ npx not found"; exit 1)
	@echo "✓ npx found"
	@command -v python3 >/dev/null 2>&1 || (echo "✗ python3 not found"; exit 1)
	@echo "✓ python3 found"
	@python3 -c "import zipfile" 2>/dev/null || (echo "✗ Python zipfile not available"; exit 1)
	@echo "✓ Python dependencies OK"
	@test -d "$(SVG_DIR)" || (echo "✗ SVG directory not found: $(SVG_DIR)"; exit 1)
	@echo "✓ SVG directory found"
	@echo ""
	@echo "All dependencies OK!"

# Combine markdown files
combine: $(COMBINED_MD)

$(COMBINED_MD): $(MARKDOWN_FILES)
	@echo "Combining markdown files..."
	@cat $(MARKDOWN_FILES) > $(COMBINED_MD)
	@echo "✓ Created $(COMBINED_MD)"

# Build PPTX with SVG (recommended)
build: $(FINAL_PPTX)

$(FINAL_PPTX): $(MARKDOWN_FILES) replace_with_svg.py
	@echo "Building PPTX with SVG support..."
	@python3 build_pptx.py

# Alternative: use bash script
build-bash: $(MARKDOWN_FILES) replace_with_svg.py
	@echo "Building PPTX with SVG support (bash)..."
	@./build_pptx.sh

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f $(COMBINED_MD)
	@rm -f $(FINAL_PPTX)
	@rm -f $(SVG_PPTX)
	@rm -f AI_Development_Training_2Days_temp.pptx
	@rm -rf temp_pptx_extract temp_pptx_working
	@rm -f marp.log
	@echo "✓ Cleaned"

# Run comprehensive unit tests
test-all:
	@echo "Running comprehensive unit tests..."
	@python3 test_build.py

# Watch mode (rebuild on markdown changes)
watch:
	@echo "Watching for changes... (Ctrl+C to stop)"
	@while true; do \
		inotifywait -q -e modify $(MARKDOWN_FILES) $(SVG_DIR)/*.svg 2>/dev/null && \
		echo "\nChange detected, rebuilding..." && \
		make build; \
	done
