#!/usr/bin/env python3
import os
import subprocess
import argparse
import sys

def png_to_ico(input_png, output_ico, sizes=(16,32,48,64,128,256)):
    """
    Convert a PNG to a Windows-safe ICO using ImageMagick.
    
    Args:
        input_png (str): path to input PNG
        output_ico (str): path to output ICO
        sizes (tuple[int]): list of icon sizes to include
    """
    input_png = os.path.abspath(input_png)
    output_ico = os.path.abspath(output_ico)

    if not os.path.isfile(input_png):
        raise FileNotFoundError(f"Input PNG not found: {input_png}")

    # Build the ImageMagick command
    size_str = ",".join(str(s) for s in sizes)
    cmd = [
        "magick",
        input_png,
        "-define", f"icon:auto-resize={size_str}",
        "-background", "none",
        output_ico
    ]

    print(f"Running command:\n{' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
        print(f"ICO saved: {output_ico}")
        return output_ico
    except subprocess.CalledProcessError as e:
        print(f"Error: ImageMagick conversion failed with exit code {e.returncode}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Convert PNG to Windows ICO using ImageMagick")
    parser.add_argument("--in", dest="input_png", required=True, help="Input PNG file")
    parser.add_argument("--out", dest="output_ico", required=True, help="Output ICO file")
    parser.add_argument("--sizes", nargs="+", type=int, default=[16,32,48,64,128,256],
                        help="Icon sizes to include (default: 16 32 48 64 128 256)")

    args = parser.parse_args()

    png_to_ico(args.input_png, args.output_ico, sizes=tuple(args.sizes))


if __name__ == "__main__":
    main()
