import os
import argparse
import traceback
from PIL import Image, UnidentifiedImageError


def scale_image(input_path, output_path, width, height, keep_aspect=False, force_upscale=True):
    """
    Scale image to width x height.
    - keep_aspect: if True, keep aspect ratio.
    - force_upscale: when keep_aspect=True, allow enlarging if True.
    """
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)

    print(f"INPUT:  {input_path}")
    print(f"OUTPUT: {output_path}")
    print(f"TARGET: {width} x {height}   keep_aspect={keep_aspect}  force_upscale={force_upscale}")

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    try:
        with Image.open(input_path) as img:
            print(f"Original: {img.format}, {img.mode}, {img.width}x{img.height}")

            # Normalize mode
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")
                print(f"Converted mode -> {img.mode}")

            orig_w, orig_h = img.width, img.height

            if keep_aspect:
                if (orig_w >= width and orig_h >= height) or not force_upscale:
                    img.thumbnail((width, height), Image.LANCZOS)
                    print(f"Thumbnail -> {img.width}x{img.height}")
                else:
                    scale = min(width / orig_w, height / orig_h)
                    new_w = max(1, int(round(orig_w * scale)))
                    new_h = max(1, int(round(orig_h * scale)))
                    img = img.resize((new_w, new_h), Image.LANCZOS)
                    print(f"Upscaled -> {img.width}x{img.height}")
            else:
                img = img.resize((width, height), Image.LANCZOS)
                print(f"Forced resize -> {img.width}x{img.height}")

            # Ensure output directory exists
            out_dir = os.path.dirname(output_path)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)

            # Save format by extension
            _, ext = os.path.splitext(output_path)
            ext = ext.lower().lstrip(".")
            save_kwargs = {}
            save_format = None

            if ext in ("jpg", "jpeg"):
                save_format = "JPEG"
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                save_kwargs["quality"] = 95
            elif ext == "png":
                save_format = "PNG"
                save_kwargs["optimize"] = True
            elif ext == "webp":
                save_format = "WEBP"
                save_kwargs["quality"] = 95
            elif ext == "bmp":
                save_format = "BMP"

            img.save(output_path, format=save_format, **save_kwargs)
            print(f"SAVED: {output_path}")
            return output_path

    except UnidentifiedImageError:
        print("ERROR: Invalid image file.")
        raise
    except Exception:
        print("ERROR during image processing:")
        traceback.print_exc()
        raise


def generate_icon_set(input_path, sizes=(16, 32, 64, 128, 256)):
    """
    Batch mode: generate multiple icon sizes.
    Output files are placed next to input image.
    """
    input_path = os.path.abspath(input_path)

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    base_dir = os.path.dirname(input_path)
    base_name, ext = os.path.splitext(os.path.basename(input_path))

    print("Batch icon mode enabled")
    print(f"Input: {input_path}")
    print(f"Sizes: {sizes}")

    for size in sizes:
        out_name = f"{base_name}_{size}{ext}"
        out_path = os.path.join(base_dir, out_name)

        print(f"\n--- Generating {size}x{size}")

        scale_image(
            input_path=input_path,
            output_path=out_path,
            width=size,
            height=size,
            keep_aspect=True,
            force_upscale=False
        )


def main():
    parser = argparse.ArgumentParser(description="Scale a single image (debug mode).")
    parser.add_argument("--in", required=True, dest="input_path", help="Input image path")
    parser.add_argument("--out", dest="output_path", default=None, help="Output image path")
    parser.add_argument("--w", type=int, default=None, help="Target width")
    parser.add_argument("--h", type=int, default=None, help="Target height")
    parser.add_argument("--keep-aspect", action="store_true", help="Keep aspect ratio")
    parser.add_argument("--no-upscale", action="store_true", help="Do not upscale smaller images")
    args = parser.parse_args()

    # Batch icon mode
    if args.w is None and args.h is None and args.output_path is None:
        generate_icon_set(args.input_path)
        return

    # Normal mode
    if args.output_path is None:
        raise ValueError("--out is required unless batch icon mode is used")

    if args.w is None or args.h is None:
        raise ValueError("--w and --h must both be specified in normal mode")

    scale_image(
        args.input_path,
        args.output_path,
        args.w,
        args.h,
        keep_aspect=args.keep_aspect,
        force_upscale=not args.no_upscale
    )


if __name__ == "__main__":
    main()
