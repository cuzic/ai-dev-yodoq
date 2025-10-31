#!/usr/bin/env python3
"""Test cases to identify bugs in overflow detection."""

# Test the character width calculation
def estimate_text_width_px(text, font_size=16):
    japanese_count = sum(1 for c in text if ord(c) > 127)
    ascii_count = len(text) - japanese_count
    width = (japanese_count * font_size * 1.0) + (ascii_count * font_size * 0.55)
    return width

# Test cases
test_cases = [
    ("Hello World", 16),  # All ASCII
    ("こんにちは", 16),  # All Japanese
    ("Hello世界", 16),  # Mixed
    ("section.three-column h1, section.three-column h2", 16),  # CSS
    ("📍 Slide 1:", 16),  # Emojis
    ("- **概要:** プロジェクト全体", 16),  # With markdown
]

print("Testing character width calculations:")
print("=" * 70)
for text, font_size in test_cases:
    width = estimate_text_width_px(text, font_size)
    jp_count = sum(1 for c in text if ord(c) > 127)
    ascii_count = len(text) - jp_count
    print(f"Text: {text}")
    print(f"  Chars: {len(text)} ({jp_count} Japanese, {ascii_count} ASCII)")
    print(f"  Width: {width:.1f}px")
    print()

# Test specific issues
print("\n" + "=" * 70)
print("Potential bugs identified:")
print("=" * 70)

print("\n1. EMOJI DETECTION:")
emoji_text = "📍 Slide 1:"
jp_count = sum(1 for c in emoji_text if ord(c) > 127)
print(f"   Text: '{emoji_text}'")
print(f"   Japanese chars detected: {jp_count}")
print(f"   → Emojis counted as Japanese (4-byte Unicode)")

print("\n2. CSS IN SLIDES:")
css_text = "section.three-column h1"
width = estimate_text_width_px(css_text, 16)
print(f"   Text: '{css_text}'")
print(f"   Width: {width:.1f}px")
print(f"   → CSS code treated as slide content")

print("\n3. LAYOUT DETECTION:")
print(f"   'three-column' in 'layout-horizontal-left': {'three-column' in 'layout-horizontal-left'}")
print(f"   → substring matching may cause false positives")

print("\n4. MARKDOWN FORMATTING:")
import re
text_with_md = "- **概要:** プロジェクト全体"
cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', text_with_md)
cleaned = re.sub(r'^[-*•]\s+', '', cleaned)
print(f"   Original: '{text_with_md}'")
print(f"   Cleaned: '{cleaned}'")
print(f"   → Markdown syntax removed but colons remain")

print("\n5. MULTI-LINE TEXT:")
print(f"   Script processes line-by-line")
print(f"   → Doesn't handle text that wraps across columns")
