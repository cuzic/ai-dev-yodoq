#!/usr/bin/env python3
"""
Replace PNG images in PPTX with corresponding SVG files.
Simpler approach: directly replace media files and update references.
"""

import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def extract_pptx(pptx_path, extract_dir):
    """Extract PPTX to directory."""
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir()

    with zipfile.ZipFile(pptx_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"✓ Extracted PPTX to {extract_dir}")


def create_pptx(source_dir, output_path):
    """Create PPTX from directory."""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(source_dir)
                zipf.write(file_path, arcname)

    print(f"✓ Created PPTX: {output_path}")


def get_svg_mapping_from_markdown(markdown_path):
    """Extract SVG file references from markdown in order."""
    if not markdown_path.exists():
        print(f"⚠ Markdown file not found: {markdown_path}")
        return []

    with open(markdown_path, encoding="utf-8") as f:
        content = f.read()

    # Find all SVG references in order
    svg_refs = re.findall(r"!\[.*?\]\(diagrams/([^)]+\.svg)\)", content)
    print(f"✓ Found {len(svg_refs)} SVG references in markdown")

    return svg_refs


def replace_images_with_svg(pptx_path, svg_dir, output_path, markdown_path):
    """Replace bitmap images with SVG files."""

    print(f"\n{'=' * 60}")
    print("PPTX SVG Replacement Tool")
    print(f"{'=' * 60}\n")

    svg_dir = Path(svg_dir)
    pptx_path = Path(pptx_path)
    output_path = Path(output_path)
    markdown_path = Path(markdown_path)

    # Get SVG mapping from markdown
    svg_refs = get_svg_mapping_from_markdown(markdown_path)

    if not svg_refs:
        print("❌ No SVG references found in markdown!")
        return

    # Extract PPTX
    extract_dir = Path("temp_pptx_working")
    extract_pptx(pptx_path, extract_dir)

    media_dir = extract_dir / "ppt" / "media"
    slides_dir = extract_dir / "ppt" / "slides"
    rels_dir = slides_dir / "_rels"

    # Get all PNG files in media directory
    png_files = sorted(media_dir.glob("Slide-*-image-*.png"))
    print(f"✓ Found {len(png_files)} PNG images in PPTX\n")

    replaced_count = 0
    svg_mapping = {}  # Map PNG filename to SVG filename

    # Match PNG files with SVG files based on slide order
    for png_file in png_files:
        # Extract slide number
        match = re.match(r"Slide-(\d+)-image-(\d+)\.png", png_file.name)
        if not match:
            continue

        slide_num = int(match.group(1))

        # Find which SVG should be on this slide
        # We need to count how many images appeared before this slide
        image_index = 0
        for pf in png_files:
            pm = re.match(r"Slide-(\d+)-image-(\d+)\.png", pf.name)
            if pm:
                sn = int(pm.group(1))
                if sn < slide_num:
                    image_index += 1
                elif sn == slide_num:
                    if pf == png_file:
                        break
                    image_index += 1

        # Get corresponding SVG
        if image_index < len(svg_refs):
            svg_name = svg_refs[image_index]
            svg_path = svg_dir / svg_name

            if svg_path.exists():
                svg_mapping[png_file.name] = svg_name
                print(f"  Slide {slide_num:3d}: {png_file.name:30s} → {svg_name}")
            else:
                print(f"  ⚠ Slide {slide_num:3d}: SVG not found: {svg_name}")
        else:
            print(
                f"  ⚠ Slide {slide_num:3d}: No matching SVG (index {image_index} >= {len(svg_refs)})"
            )

    print(f"\n✓ Mapped {len(svg_mapping)} images to SVG files\n")

    # Now replace the files and update references
    for png_name, svg_name in svg_mapping.items():
        svg_path = svg_dir / svg_name
        svg_dest = media_dir / svg_name

        # Copy SVG to media directory
        shutil.copy2(svg_path, svg_dest)

        # Find and update all slide relationship files that reference this PNG
        for rel_file in rels_dir.glob("slide*.xml.rels"):
            try:
                tree = ET.parse(rel_file)
                root = tree.getroot()

                ns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
                modified = False

                for rel in root.findall(".//r:Relationship", ns):
                    target = rel.get("Target")
                    if target and png_name in target:
                        # Update to point to SVG
                        new_target = target.replace(png_name, svg_name)
                        rel.set("Target", new_target)
                        modified = True
                        replaced_count += 1

                if modified:
                    # Write back the updated relationships
                    tree.write(rel_file, encoding="utf-8", xml_declaration=True)

            except Exception as e:
                print(f"  ⚠ Error processing {rel_file}: {e}")

    # Update [Content_Types].xml to register SVG MIME type
    content_types_file = extract_dir / "[Content_Types].xml"
    try:
        tree = ET.parse(content_types_file)
        root = tree.getroot()

        ns = {"ct": "http://schemas.openxmlformats.org/package/2006/content-types"}
        ET.register_namespace("", "http://schemas.openxmlformats.org/package/2006/content-types")

        # Check if SVG default exists
        svg_exists = any(
            default.get("Extension") == "svg" for default in root.findall(".//ct:Default", ns)
        )

        if not svg_exists:
            # Add SVG content type at the beginning
            svg_default = ET.Element(
                "{http://schemas.openxmlformats.org/package/2006/content-types}Default"
            )
            svg_default.set("Extension", "svg")
            svg_default.set("ContentType", "image/svg+xml")
            root.insert(0, svg_default)
            tree.write(content_types_file, encoding="utf-8", xml_declaration=True)
            print("✓ Added SVG content type to [Content_Types].xml")

    except Exception as e:
        print(f"⚠ Error updating content types: {e}")

    # Create new PPTX
    create_pptx(extract_dir, output_path)

    # Clean up
    shutil.rmtree(extract_dir)
    print("✓ Cleaned up temporary files")

    # Show results
    original_size = pptx_path.stat().st_size / (1024 * 1024)
    new_size = output_path.stat().st_size / (1024 * 1024)

    print(f"\n{'=' * 60}")
    print("✅ COMPLETE!")
    print(f"{'=' * 60}")
    print(f"Replaced {replaced_count} image references")
    print(f"Original size: {original_size:6.2f} MB")
    print(f"New size:      {new_size:6.2f} MB")
    print(f"Difference:    {new_size - original_size:+6.2f} MB")
    print(f"\nOutput file: {output_path}")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    replace_images_with_svg(
        pptx_path="AI_Development_Training_2Days.pptx",
        svg_dir="diagrams",
        output_path="AI_Development_Training_2Days_SVG.pptx",
        markdown_path="all_slides.md",
    )
