import argparse
import shutil
from pathlib import Path
import sys


def copy_xml_keep_structure(src_dir: Path, dst_dir: Path):
    """
    Copy all XML files from src_dir to dst_dir,
    keeping the original directory structure.
    """
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {src_dir}")

    for xml_file in src_dir.rglob("*.xml"):
        relative_path = xml_file.relative_to(src_dir)
        target_file = dst_dir / relative_path

        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(xml_file, target_file)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Copy all XML files from source directory to destination directory, keeping structure."
    )
    parser.add_argument(
        "--src",
        required=True,
        help="Source directory containing XML files"
    )
    parser.add_argument(
        "--dst",
        required=True,
        help="Destination directory"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    src_dir = Path(args.src).resolve()
    dst_dir = Path(args.dst).resolve()

    try:
        copy_xml_keep_structure(src_dir, dst_dir)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"XML files copied from '{src_dir}' to '{dst_dir}' successfully.")


if __name__ == "__main__":
    main()
