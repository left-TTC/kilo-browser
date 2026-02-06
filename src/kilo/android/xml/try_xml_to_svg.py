import argparse
import sys
from pathlib import Path
import xml.etree.ElementTree as ET


ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def is_vector_drawable(xml_path: Path) -> bool:
    """
    Check whether the XML file is an Android VectorDrawable.
    """
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        return root.tag == "vector"
    except Exception:
        return False


def convert_vector_xml_to_svg(xml_path: Path, svg_path: Path):
    """
    Convert a single Android VectorDrawable XML to SVG.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    viewport_width = root.attrib.get(f"{ANDROID_NS}viewportWidth")
    viewport_height = root.attrib.get(f"{ANDROID_NS}viewportHeight")

    if not viewport_width or not viewport_height:
        raise ValueError("Missing viewportWidth / viewportHeight")

    svg_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg"',
        f'     viewBox="0 0 {viewport_width} {viewport_height}"',
        f'     width="{viewport_width}"',
        f'     height="{viewport_height}">',
    ]

    path_found = False

    for path in root.findall("path"):
        path_data = path.attrib.get(f"{ANDROID_NS}pathData")
        if not path_data:
            continue

        path_found = True

        fill_color = path.attrib.get(f"{ANDROID_NS}fillColor", "#000000")
        fill_type = path.attrib.get(f"{ANDROID_NS}fillType")

        line = f'  <path d="{path_data}" fill="{fill_color}"'
        if fill_type == "evenOdd":
            line += ' fill-rule="evenodd"'
        line += "/>"

        svg_lines.append(line)

    svg_lines.append("</svg>")

    if not path_found:
        raise ValueError("No valid <path> found")

    svg_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path.write_text("\n".join(svg_lines), encoding="utf-8")


def process_directory(src_dir: Path, dst_dir: Path):
    """
    Traverse src_dir, convert all VectorDrawable XML files to SVG,
    keep directory structure, skip non-convertible files.
    """
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {src_dir}")

    converted = 0
    skipped = 0

    for xml_file in src_dir.rglob("*.xml"):
        if not is_vector_drawable(xml_file):
            skipped += 1
            continue

        relative_path = xml_file.relative_to(src_dir)
        svg_file = (dst_dir / relative_path).with_suffix(".svg")

        try:
            convert_vector_xml_to_svg(xml_file, svg_file)
            converted += 1
        except Exception:
            skipped += 1

    return converted, skipped


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert Android VectorDrawable XML files to SVG recursively."
    )
    parser.add_argument(
        "--src",
        required=True,
        help="Source directory containing XML files"
    )
    parser.add_argument(
        "--dst",
        required=True,
        help="Destination directory for SVG output"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    src_dir = Path(args.src).resolve()
    dst_dir = Path(args.dst).resolve()

    try:
        converted, skipped = process_directory(src_dir, dst_dir)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Conversion finished.")
    print(f"  Converted: {converted}")
    print(f"  Skipped:   {skipped}")


if __name__ == "__main__":
    main()
