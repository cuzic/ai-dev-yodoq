#!/usr/bin/env python3
"""
Replace bitmap images in PPTX with SVG images.
This script extracts the PPTX, finds bitmap images that correspond to SVG files,
and replaces them with SVG format for better quality and smaller file size.
"""

import os
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def find_svg_for_image(image_name, svg_dir):
    """Find corresponding SVG file for an image."""
    # Extract potential diagram name from image filename
    # Example: image1.png might correspond to diagram_01_something.svg

    # Try to match by number
    match = re.search(r"image(\d+)", image_name)
    if match:
        img_num = int(match.group(1))
        # Look for SVG files in the directory
        svg_files = sorted(Path(svg_dir).glob("diagram_*.svg"))
        if 0 < img_num <= len(svg_files):
            return svg_files[img_num - 1]

    return None


def replace_images_with_svg(pptx_path, svg_dir, output_path):
    """Replace bitmap images in PPTX with SVG images."""

    print(f"Processing PPTX: {pptx_path}")
    print(f"SVG directory: {svg_dir}")

    # Create temporary directory for extraction
    temp_dir = Path("temp_pptx_extract")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()

    # Extract PPTX (which is a ZIP file)
    print("Extracting PPTX...")
    with zipfile.ZipFile(pptx_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

    # Find all slide XML files
    slides_dir = temp_dir / "ppt" / "slides"
    media_dir = temp_dir / "ppt" / "media"

    if not slides_dir.exists():
        print("No slides directory found!")
        return

    print(f"Found slides directory: {slides_dir}")

    # Get list of SVG files
    svg_files = sorted(Path(svg_dir).glob("*.svg"))
    print(f"Found {len(svg_files)} SVG files")

    # Map diagram names mentioned in markdown to SVG files
    # We need to track which images in PPTX correspond to which SVGs

    # Read all_slides.md to find SVG references
    markdown_path = Path(pptx_path).parent / "all_slides.md"
    svg_references = []

    if markdown_path.exists():
        print(f"Reading markdown file: {markdown_path}")
        with open(markdown_path, encoding="utf-8") as f:
            content = f.read()
            # Find all SVG references
            svg_refs = re.findall(r"!\[.*?\]\((diagrams/[^)]+\.svg)\)", content)
            svg_references = [Path(ref).name for ref in svg_refs]
            print(f"Found {len(svg_references)} SVG references in markdown:")
            for i, ref in enumerate(svg_references[:5]):
                print(f"  {i + 1}. {ref}")

    # Process each slide
    namespace = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }

    ET.register_namespace("p", "http://schemas.openxmlformats.org/presentationml/2006/main")
    ET.register_namespace("a", "http://schemas.openxmlformats.org/drawingml/2006/main")

    slide_files = sorted(slides_dir.glob("slide*.xml"))
    print(f"Processing {len(slide_files)} slides...")

    image_counter = 0
    replaced_count = 0

    for slide_file in slide_files:
        tree = ET.parse(slide_file)
        root = tree.getroot()

        # Find all image references in the slide
        for pic in root.findall(".//p:pic", namespace):
            blip = pic.find(".//a:blip", namespace)
            if blip is not None:
                rel_id = blip.get(
                    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
                )

                # Read slide relationships
                rel_file = slides_dir / "_rels" / f"{slide_file.name}.rels"
                if rel_file.exists():
                    rel_tree = ET.parse(rel_file)
                    rel_root = rel_tree.getroot()

                    ns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
                    for rel in rel_root.findall(".//r:Relationship", ns):
                        if rel.get("Id") == rel_id:
                            target = rel.get("Target")

                            if target and "../media/" in target:
                                image_file = Path(target).name

                                # Try to match with SVG
                                if image_counter < len(svg_references):
                                    svg_name = svg_references[image_counter]
                                    svg_path = Path(svg_dir) / svg_name

                                    if svg_path.exists():
                                        # Copy SVG to media directory
                                        svg_dest = media_dir / svg_name
                                        shutil.copy2(svg_path, svg_dest)

                                        # Update relationship to point to SVG
                                        new_target = f"../media/{svg_name}"
                                        rel.set("Target", new_target)

                                        # Update content type for SVG
                                        # This needs to be done in [Content_Types].xml

                                        print(
                                            f"  Slide {slide_file.name}: Replaced {image_file} with {svg_name}"
                                        )
                                        replaced_count += 1

                                image_counter += 1

                    # Write updated relationships
                    rel_tree.write(rel_file, encoding="utf-8", xml_declaration=True)

    # Update [Content_Types].xml to include SVG
    content_types_file = temp_dir / "[Content_Types].xml"
    if content_types_file.exists():
        print("Updating content types for SVG support...")
        ct_tree = ET.parse(content_types_file)
        ct_root = ct_tree.getroot()

        ns = {"ct": "http://schemas.openxmlformats.org/package/2006/content-types"}
        ET.register_namespace("", "http://schemas.openxmlformats.org/package/2006/content-types")

        # Check if SVG default already exists
        svg_exists = False
        for default in ct_root.findall(".//ct:Default", ns):
            if default.get("Extension") == "svg":
                svg_exists = True
                break

        if not svg_exists:
            # Add SVG content type
            svg_default = ET.Element(
                "{http://schemas.openxmlformats.org/package/2006/content-types}Default"
            )
            svg_default.set("Extension", "svg")
            svg_default.set("ContentType", "image/svg+xml")
            ct_root.insert(0, svg_default)
            ct_tree.write(content_types_file, encoding="utf-8", xml_declaration=True)

    # Create new PPTX
    print(f"Creating new PPTX: {output_path}")
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(temp_dir)
                zipf.write(file_path, arcname)

    # Clean up
    shutil.rmtree(temp_dir)

    print(f"\n✅ Complete! Replaced {replaced_count} images with SVG")
    print(f"Output: {output_path}")

    # Compare file sizes
    original_size = Path(pptx_path).stat().st_size / (1024 * 1024)
    new_size = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"Original size: {original_size:.2f} MB")
    print(f"New size: {new_size:.2f} MB")
    print(f"Size change: {new_size - original_size:+.2f} MB")


if __name__ == "__main__":
    pptx_path = "AI_Development_Training_2Days.pptx"
    svg_dir = "diagrams"
    output_path = "AI_Development_Training_2Days_SVG.pptx"

    replace_images_with_svg(pptx_path, svg_dir, output_path)
