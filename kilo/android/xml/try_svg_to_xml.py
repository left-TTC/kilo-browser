import argparse
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ANDROID_NS = "http://schemas.android.com/apk/res/android"


def convert_svg_to_vector(svg_path: Path, xml_path: Path):
    """
    Convert a single SVG with one or more <path> elements to Android VectorDrawable XML.
    """
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # 解析 viewBox
    viewBox = root.attrib.get("viewBox")
    if viewBox:
        try:
            min_x, min_y, width, height = map(float, viewBox.strip().split())
        except Exception:
            raise ValueError(f"Invalid viewBox in {svg_path}")
    else:
        # fallback: use width/height
        width = float(root.attrib.get("width", "24"))
        height = float(root.attrib.get("height", "24"))
        min_x = 0
        min_y = 0

    # 创建 vector 根节点
    vector_root = ET.Element("vector", {
        f"{{{ANDROID_NS}}}width": f"{width}dp",
        f"{{{ANDROID_NS}}}height": f"{height}dp",
        f"{{{ANDROID_NS}}}viewportWidth": str(width),
        f"{{{ANDROID_NS}}}viewportHeight": str(height),
    })

    # 查找所有 path（递归，支持命名空间）
    PATH_TAG = f"{{{SVG_NS}}}path"
    path_elements = root.findall(f".//{PATH_TAG}")

    if not path_elements:
        raise ValueError(f"No <path> elements found in {svg_path}")

    for path in path_elements:
        d = path.attrib.get("d")
        if not d:
            continue
        fill = path.attrib.get("fill", "#000000")
        fill_rule = path.attrib.get("fill-rule")
        path_attrib = {
            f"{{{ANDROID_NS}}}pathData": d,
            f"{{{ANDROID_NS}}}fillColor": fill
        }
        if fill_rule == "evenodd":
            path_attrib[f"{{{ANDROID_NS}}}fillType"] = "evenOdd"
        ET.SubElement(vector_root, "path", path_attrib)

    # 创建输出目录
    xml_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入 XML
    ET.ElementTree(vector_root).write(xml_path, encoding="utf-8", xml_declaration=True)


def process_directory(src_dir: Path, dst_dir: Path):
    """
    Traverse src_dir recursively, convert all SVG files to VectorDrawable XML.
    """
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {src_dir}")

    converted = 0
    skipped = 0

    for svg_file in src_dir.rglob("*.svg"):
        relative_path = svg_file.relative_to(src_dir)
        xml_file = (dst_dir / relative_path).with_suffix(".xml")
        try:
            convert_svg_to_vector(svg_file, xml_file)
            print(f"Converted: {svg_file} -> {xml_file}")
            converted += 1
        except Exception as e:
            print(f"Skipped: {svg_file} ({e})", file=sys.stderr)
            skipped += 1

    return converted, skipped


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert SVG files to Android VectorDrawable XML recursively."
    )
    parser.add_argument("--src", required=True, help="Source directory with SVG files")
    parser.add_argument("--dst", required=True, help="Destination directory for XML output")
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

    print(f"Conversion finished: {converted} converted, {skipped} skipped.")


if __name__ == "__main__":
    main()
