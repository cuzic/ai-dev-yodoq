#!/usr/bin/env python3
"""
Preview slides locally and adjust font sizes until text fits properly.
"""

import http.server
import socketserver
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path


class SlidePreviewServer:
    def __init__(self, port=8000):
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        """Start HTTP server in background thread."""
        handler = http.server.SimpleHTTPRequestHandler

        class QuietHandler(handler):
            def log_message(self, format, *args):
                pass  # Suppress logs

        self.server = socketserver.TCPServer(("", self.port), QuietHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"✓ Server started at http://localhost:{self.port}")

    def stop(self):
        """Stop the server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()


def build_html():
    """Build HTML slides from markdown."""
    print("📦 Building HTML slides...")
    try:
        result = subprocess.run(
            [
                "npx",
                "-y",
                "@marp-team/marp-cli@latest",
                "all_slides.md",
                "--html",
                "--allow-local-files",
                "-o",
                "index.html",
            ],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=True,
        )
        print("✓ HTML slides built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e.stderr}")
        return False


def get_current_font_sizes():
    """Extract current font sizes from all_slides.md."""
    md_file = Path(__file__).parent / "all_slides.md"
    content = md_file.read_text(encoding="utf-8")

    sizes = {}
    for line in content.split("\n"):
        line = line.strip()
        if "font-size:" in line:
            if "section {" in content[max(0, content.index(line) - 100):content.index(line)]:
                if "section {" in content[max(0, content.index(line) - 50):content.index(line)]:
                    parts = line.split(":")
                    if len(parts) == 2:
                        size = parts[1].strip().rstrip(";")
                        if "section {" in content[max(0, content.index(line) - 100):content.index(line)]:
                            sizes["section"] = size
            if "h1 {" in content[max(0, content.index(line) - 50):content.index(line)]:
                parts = line.split(":")
                if len(parts) == 2:
                    sizes["h1"] = parts[1].strip().rstrip(";")
            if "h2 {" in content[max(0, content.index(line) - 50):content.index(line)]:
                parts = line.split(":")
                if len(parts) == 2:
                    sizes["h2"] = parts[1].strip().rstrip(";")

    return sizes


def update_font_sizes(section_size, h1_size, h2_size):
    """Update font sizes in all_slides.md."""
    md_file = Path(__file__).parent / "all_slides.md"
    content = md_file.read_text(encoding="utf-8")

    # Replace section font-size
    content = content.replace(
        "  section {\n    font-size: 20px;",
        f"  section {{\n    font-size: {section_size}px;"
    )

    # Replace h1 font-size
    content = content.replace(
        "  h1 {\n    font-size: 36px;",
        f"  h1 {{\n    font-size: {h1_size}px;"
    )

    # Replace h2 font-size
    content = content.replace(
        "  h2 {\n    font-size: 28px;",
        f"  h2 {{\n    font-size: {h2_size}px;"
    )

    # Also update horizontal layout sizes proportionally
    horizontal_size = int(section_size * 0.9)
    content = content.replace(
        "  section.layout-horizontal-left > :not(h1):not(img) {\n    font-size: 18px;",
        f"  section.layout-horizontal-left > :not(h1):not(img) {{\n    font-size: {horizontal_size}px;"
    )
    content = content.replace(
        "  section.layout-horizontal-right > :not(h1):not(img) {\n    font-size: 18px;",
        f"  section.layout-horizontal-right > :not(h1):not(img) {{\n    font-size: {horizontal_size}px;"
    )

    md_file.write_text(content, encoding="utf-8")
    print(f"✓ Updated font sizes: section={section_size}px, h1={h1_size}px, h2={h2_size}px")


def main():
    """Interactive slide preview with font adjustment."""
    slides_dir = Path(__file__).parent

    print("=" * 60)
    print("Slide Preview Tool")
    print("=" * 60)

    # Initial build
    if not build_html():
        sys.exit(1)

    # Start server
    server = SlidePreviewServer(port=8000)
    server.start()

    # Open browser
    time.sleep(1)
    url = "http://localhost:8000/index.html"
    print(f"\n🌐 Opening {url} in browser...")
    webbrowser.open(url)

    print("\n" + "=" * 60)
    print("Interactive Font Adjustment")
    print("=" * 60)
    print("Commands:")
    print("  s <size>  - Set section font size (e.g., 's 20')")
    print("  h1 <size> - Set h1 font size (e.g., 'h1 36')")
    print("  h2 <size> - Set h2 font size (e.g., 'h2 28')")
    print("  preset <name> - Apply preset (small/medium/large)")
    print("  show      - Show current font sizes")
    print("  rebuild   - Rebuild HTML with current settings")
    print("  quit      - Exit preview server")
    print("=" * 60)

    presets = {
        "small": {"section": 18, "h1": 32, "h2": 24},
        "medium": {"section": 20, "h1": 36, "h2": 28},
        "large": {"section": 24, "h1": 44, "h2": 36},
    }

    try:
        while True:
            cmd = input("\n> ").strip().lower()

            if cmd == "quit" or cmd == "q":
                break
            elif cmd == "show":
                sizes = get_current_font_sizes()
                print(f"Current sizes: {sizes}")
            elif cmd == "rebuild" or cmd == "r":
                if build_html():
                    print(f"✓ Reload {url} to see changes")
            elif cmd.startswith("preset "):
                preset_name = cmd.split()[1]
                if preset_name in presets:
                    p = presets[preset_name]
                    update_font_sizes(p["section"], p["h1"], p["h2"])
                    if build_html():
                        print(f"✓ Applied '{preset_name}' preset. Reload browser to see changes.")
                else:
                    print(f"✗ Unknown preset. Available: {', '.join(presets.keys())}")
            elif cmd.startswith("s "):
                try:
                    size = int(cmd.split()[1])
                    update_font_sizes(size, 36, 28)
                    if build_html():
                        print("✓ Reload browser to see changes")
                except (ValueError, IndexError):
                    print("✗ Invalid size. Usage: s <number>")
            elif cmd.startswith("h1 "):
                try:
                    size = int(cmd.split()[1])
                    update_font_sizes(20, size, 28)
                    if build_html():
                        print("✓ Reload browser to see changes")
                except (ValueError, IndexError):
                    print("✗ Invalid size. Usage: h1 <number>")
            elif cmd.startswith("h2 "):
                try:
                    size = int(cmd.split()[1])
                    update_font_sizes(20, 36, size)
                    if build_html():
                        print("✓ Reload browser to see changes")
                except (ValueError, IndexError):
                    print("✗ Invalid size. Usage: h2 <number>")
            elif cmd == "":
                continue
            else:
                print("✗ Unknown command. Type 'quit' to exit.")

    except KeyboardInterrupt:
        print("\n\nInterrupted.")

    finally:
        print("\n🛑 Stopping server...")
        server.stop()
        print("✓ Done")


if __name__ == "__main__":
    main()
