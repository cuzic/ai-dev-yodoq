# SVG Design Guide for Web Slides

## Problem Statement

The original SVGs were designed for PowerPoint (1280x720px slides) and have several issues when displayed on web:

1. **Font sizes too large** - 54px, 64px, 74px, 81px designed for PPTX are unreadable in browser
2. **ViewBox mismatch** - viewBox="0 0 1170 1170" but content in 900x900 causes clipping
3. **Fixed positioning** - Absolute coordinates don't scale proportionally
4. **No responsive design** - Doesn't adapt to different screen sizes

## Design Principles for Web-Optimized SVGs

### 1. ViewBox and Dimensions
```xml
<!-- BAD: Large viewBox with smaller content -->
<svg viewBox="0 0 1170 1170">
  <rect width="900" height="900" fill="#FFF"/>
</svg>

<!-- GOOD: ViewBox matches content exactly -->
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="600" fill="#FFF"/>
</svg>
```

### 2. Font Sizing (Web-Optimized)
```css
/* Font size hierarchy for web */
.title        { font-size: 28px; }  /* Main title */
.subtitle     { font-size: 22px; }  /* Section headers */
.body-text    { font-size: 16px; }  /* Body content */
.label        { font-size: 14px; }  /* Labels, annotations */
.small        { font-size: 12px; }  /* Fine print */
```

**Never use:**
- 54px, 64px, 74px, 81px (PPTX sizes)
- Inline font-size overrides that break consistency

### 3. Responsive Scaling
```css
/* Use relative units and percentages */
.diagram-container {
  width: 100%;
  max-width: 800px;
  height: auto;
}

/* Text should scale with viewBox */
text {
  font-size: 16px;  /* Base size */
}
```

### 4. Layout Structure
```xml
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="600" fill="#FFFFFF"/>

  <!-- Content area: 90% width, centered -->
  <g transform="translate(40, 40)">
    <!-- Title area: top 15% -->
    <text x="360" y="30" class="title" text-anchor="middle">
      Diagram Title
    </text>

    <!-- Main content: middle 70% -->
    <g id="main-content" transform="translate(0, 80)">
      <!-- Content here -->
    </g>

    <!-- Footer: bottom 15% -->
    <g id="footer" transform="translate(0, 520)">
      <text x="360" y="20" class="label" text-anchor="middle">
        Additional notes
      </text>
    </g>
  </g>
</svg>
```

### 5. Color Palette (Accessible)
```css
/* Use high-contrast colors for readability */
--color-primary:    #00146E;  /* Navy blue */
--color-secondary:  #00AFF0;  /* Cyan */
--color-accent:     #003399;  /* Medium blue */
--color-success:    #27ae60;  /* Green */
--color-danger:     #e74c3c;  /* Red */
--color-text-dark:  #333333;  /* Near black */
--color-text-light: #666666;  /* Gray */
--color-bg:         #FFFFFF;  /* White */
--color-bg-alt:     #F6F8FA;  /* Light gray */
```

## SVG Template for Common Patterns

### Pattern 1: Flow Diagram (Horizontal)
```xml
<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .box { fill: #00146E; }
      .box-text { font-family: 'Noto Sans JP', sans-serif; font-size: 16px; fill: white; text-anchor: middle; }
      .arrow-text { font-family: 'Noto Sans JP', sans-serif; font-size: 12px; fill: #666; text-anchor: middle; }
    </style>
  </defs>

  <!-- Step 1 -->
  <rect x="50" y="100" width="120" height="80" rx="5" class="box"/>
  <text x="110" y="145" class="box-text">STEP1</text>

  <!-- Arrow -->
  <line x1="170" y1="140" x2="230" y2="140" stroke="#00146E" stroke-width="2"/>
  <polygon points="230,140 225,135 225,145" fill="#00146E"/>
  <text x="200" y="130" class="arrow-text">→</text>

  <!-- Step 2 -->
  <rect x="230" y="100" width="120" height="80" rx="5" class="box"/>
  <text x="290" y="145" class="box-text">STEP2</text>
</svg>
```

### Pattern 2: Circular Diagram
```xml
<svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .segment { font-size: 14px; fill: white; text-anchor: middle; }
      .center-text { font-size: 18px; fill: #00146E; text-anchor: middle; font-weight: bold; }
    </style>
  </defs>

  <!-- Center circle -->
  <circle cx="300" cy="300" r="60" fill="#E6E6E6"/>
  <text x="300" y="305" class="center-text">Core</text>

  <!-- Segment 1 (12 o'clock) -->
  <path d="M 300 150 L 350 250 A 60 60 0 0 1 250 250 Z" fill="#00146E"/>
  <text x="300" y="190" class="segment">Item 1</text>
</svg>
```

### Pattern 3: Comparison (Side-by-Side)
```xml
<svg viewBox="0 0 900 400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .title { font-size: 20px; font-weight: bold; text-anchor: middle; }
      .content { font-size: 14px; }
      .bad { fill: #fee; stroke: #e74c3c; }
      .good { fill: #efe; stroke: #27ae60; }
    </style>
  </defs>

  <!-- Left side: BAD -->
  <rect x="50" y="50" width="350" height="300" class="bad" stroke-width="2" rx="10"/>
  <text x="225" y="90" class="title" fill="#e74c3c">❌ Bad Practice</text>
  <text x="70" y="130" class="content">• Problem 1</text>
  <text x="70" y="160" class="content">• Problem 2</text>

  <!-- Right side: GOOD -->
  <rect x="500" y="50" width="350" height="300" class="good" stroke-width="2" rx="10"/>
  <text x="675" y="90" class="title" fill="#27ae60">✅ Good Practice</text>
  <text x="520" y="130" class="content">• Solution 1</text>
  <text x="520" y="160" class="content">• Solution 2</text>
</svg>
```

## AI Prompt Template for SVG Generation

```markdown
Create an SVG diagram optimized for web display with these specifications:

**Diagram Type:** [Flow/Circular/Comparison/Timeline/etc.]
**Purpose:** [Brief description of what this diagram shows]
**Content:**
- [List key elements]

**Technical Requirements:**
- ViewBox: 800x600 (or specify aspect ratio)
- Font sizes: Title 28px, Subtitle 22px, Body 16px, Labels 14px
- Use CSS classes (not inline styles)
- Colors: Navy (#00146E), Cyan (#00AFF0), Green (#27ae60), Red (#e74c3c)
- No text longer than 30 characters per line
- Include proper text-anchor (start/middle/end)
- All text in Japanese where appropriate
- Accessible contrast ratios (WCAG AA minimum)

**Layout:**
- 40px margin on all sides
- Center-aligned title at top
- Main content in middle 70%
- Footer notes if needed

Generate clean, semantic SVG code following these web-optimized patterns.
```

## Conversion Script: PPTX SVG → Web SVG

```python
#!/usr/bin/env python3
"""
Convert PPTX-designed SVGs to web-optimized versions.
"""
import re
from pathlib import Path

def convert_svg_for_web(svg_content):
    """Convert PPTX SVG to web-optimized SVG."""

    # 1. Scale down font sizes (divide by 3.5)
    def scale_font(match):
        size = int(match.group(1))
        new_size = max(12, int(size / 3.5))  # Minimum 12px
        return f'font-size: {new_size}px'

    svg_content = re.sub(r'font-size:\s*(\d+)px', scale_font, svg_content)
    svg_content = re.sub(r'font-size="(\d+)"',
                         lambda m: f'font-size="{max(12, int(int(m.group(1)) / 3.5))}"',
                         svg_content)

    # 2. Fix viewBox if content doesn't match
    viewbox_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_content)
    if viewbox_match:
        vb_width = int(viewbox_match.group(1))
        vb_height = int(viewbox_match.group(2))

        # Find actual content bounds
        rect_match = re.search(r'<rect[^>]*width="(\d+)"[^>]*height="(\d+)"', svg_content)
        if rect_match:
            content_width = int(rect_match.group(1))
            content_height = int(rect_match.group(2))

            if content_width < vb_width * 0.9:  # Significant mismatch
                # Scale to 800px width standard
                scale = 800 / content_width
                new_height = int(content_height * scale)
                svg_content = re.sub(
                    r'viewBox="0 0 \d+ \d+"',
                    f'viewBox="0 0 800 {new_height}"',
                    svg_content
                )

    # 3. Add responsive width/height
    if 'width=' not in svg_content and '<svg' in svg_content:
        svg_content = svg_content.replace(
            '<svg ',
            '<svg width="100%" height="auto" '
        )

    return svg_content

# Usage
for svg_file in Path('../diagrams').glob('*.svg'):
    content = svg_file.read_text(encoding='utf-8')
    converted = convert_svg_for_web(content)

    # Save to new location
    output_file = Path('../diagrams-web') / svg_file.name
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(converted, encoding='utf-8')
```

## Testing Checklist

- [ ] ViewBox matches content dimensions exactly
- [ ] Font sizes readable at 70% browser width
- [ ] All text visible (no clipping)
- [ ] Colors have 4.5:1 contrast ratio minimum
- [ ] Japanese text renders correctly (Noto Sans JP)
- [ ] No text overlaps
- [ ] Scales properly 50%-150% browser zoom
- [ ] Total file size < 50KB
- [ ] No inline styles (use CSS classes)
- [ ] Accessible for screen readers

## Reference: Original vs Optimized

### Original (PPTX-style):
- ViewBox: 1170x1170, Content: 900x900
- Fonts: 81px, 74px, 54px
- Total size: 9.8KB
- Readability: ❌ Poor on web

### Optimized (Web-style):
- ViewBox: 800x600, Content: 800x600
- Fonts: 28px, 22px, 16px
- Total size: 6.2KB
- Readability: ✅ Good on web

## Next Steps

1. Audit existing 44 SVG diagrams
2. Categorize by pattern type
3. Create conversion script for each pattern
4. Generate new web-optimized SVGs
5. Update all_slides.md to reference new diagrams
6. Test on multiple devices/browsers
