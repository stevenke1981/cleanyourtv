"""Local format checks/conversions; never generates art or calls a remote service.

Run from any directory with Python + scripts/requirements.txt. Use --help for CLI.
All outputs use exclusive creation; existing assets are never overwritten.
"""
import argparse
import hashlib
import io
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ICO_SIZES = (16, 24, 32, 48, 64, 128, 256)
MAX_WALLPAPER_BYTES = 300 * 1024


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_image(path):
    with Image.open(path) as image:
        if getattr(image, "n_frames", 1) != 1:
            raise ValueError("Use a single static image")
        image.load()
        return image.copy(), image.format


def write_new(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as target:
        target.write(data)


def encoded(image, fmt, **options):
    stream = io.BytesIO()
    image.save(stream, format=fmt, **options)
    return stream.getvalue()


def icon_image(path, minimum=160):
    image, fmt = read_image(path)
    if fmt != "PNG":
        raise ValueError("Icon master must be a PNG, not a renamed JPEG/ICO")
    if image.width != image.height or image.width < minimum:
        raise ValueError(f"Icon must be square and at least {minimum}px")
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    low, high = alpha.getextrema()
    if low != 0 or high == 0:
        raise ValueError("Icon needs genuinely transparent and visible pixels")
    if any(alpha.getpixel(p) != 0 for p in (
            (0, 0), (0, image.height - 1),
            (image.width - 1, 0), (image.width - 1, image.height - 1))):
        raise ValueError("Icon canvas corners must remain transparent")
    return rgba


def ico_entries(path):
    data = Path(path).read_bytes()
    if len(data) < 6:
        raise ValueError("Truncated ICO header")
    reserved, kind, count = struct.unpack_from("<HHH", data)
    if reserved != 0 or kind != 1 or count != len(ICO_SIZES):
        raise ValueError("Expected a real ICO with all seven requested entries")
    table_end = 6 + 16 * count
    if len(data) < table_end:
        raise ValueError("Truncated ICO directory")
    sizes, ranges = [], []
    for index in range(count):
        w, h, _, entry_reserved, _, _, length, offset = struct.unpack_from(
            "<BBBBHHII", data, 6 + 16 * index)
        w, h = w or 256, h or 256
        if entry_reserved or w != h or offset < table_end or not length or offset + length > len(data):
            raise ValueError("Invalid ICO dimensions or payload bounds")
        sizes.append(w)
        ranges.append((offset, offset + length))
    ordered = sorted(ranges)
    if any(a[1] > b[0] for a, b in zip(ordered, ordered[1:])):
        raise ValueError("Overlapping ICO payloads")
    if sorted(sizes) != list(ICO_SIZES):
        raise ValueError("Missing or duplicated ICO size")
    with Image.open(path) as image:
        if image.format != "ICO" or image.ico.sizes() != {(s, s) for s in ICO_SIZES}:
            raise ValueError("ICO decoder disagrees with directory")
        for size in ICO_SIZES:
            frame = image.ico.getimage((size, size)).convert("RGBA")
            frame.load()
            if frame.size != (size, size):
                raise ValueError("Decoded ICO frame has wrong dimensions")
            low, high = frame.getchannel("A").getextrema()
            if low != 0 or high == 0:
                raise ValueError("ICO frame lost transparent or visible pixels")
    return sizes


def white_contrast(image, dim=0):
    # Conservative whole-image screen, not a substitute for actual UI compositing.
    lut = [v / 255 / 12.92 if v / 255 <= 0.04045 else
           ((v / 255 + 0.055) / 1.055) ** 2.4 for v in range(256)]
    if not 0 <= dim <= 90:
        raise ValueError("Wallpaper dim must be between 0 and 90 percent")
    # Simulate the existing black wallpaper overlay; no image bytes are changed.
    factor = (255 - int(255 * dim / 100)) / 255
    maximum, location = -1, (0, 0)
    for index, (r, g, b) in enumerate(image.convert("RGB").getdata()):
        r, g, b = (int(value * factor + 0.5) for value in (r, g, b))
        luminance = 0.2126 * lut[r] + 0.7152 * lut[g] + 0.0722 * lut[b]
        if luminance > maximum:
            maximum, location = luminance, (index % image.width, index // image.width)
    ratio = 1.05 / (maximum + 0.05)
    return {"minimum_white_text_ratio": round(ratio, 3),
            "contrast_screen_status": "PASS" if ratio >= 4.5 else "FAIL",
            "brightest_pixel_xy": location, "simulated_wallpaper_dim_percent": dim,
            "scope": "whole image with simulated uniform black scrim; actual UI not measured"}


def check(path, kind, dim=0):
    path = Path(path)
    result = {"path": path.as_posix(), "kind": kind,
              "bytes": path.stat().st_size, "sha256": digest(path)}
    if kind == "ico":
        result["sizes"] = sorted(ico_entries(path))
    else:
        image, fmt = read_image(path)
        result.update(format=fmt, dimensions=image.size, mode=image.mode,
                      alpha_extrema=image.convert("RGBA").getchannel("A").getextrema())
        if kind == "icon":
            rgba = icon_image(path)
            result["alpha_bbox"] = rgba.getchannel("A").getbbox()
        elif kind == "launcher":
            if image.width != image.height or image.width < 160 or fmt != "PNG":
                raise ValueError("Expected square launcher PNG, at least 160px")
        elif kind == "wallpaper":
            if image.size != (1920, 1080) or fmt != "JPEG":
                raise ValueError("Prepared wallpaper must be a 1920x1080 JPEG")
            if path.stat().st_size > MAX_WALLPAPER_BYTES:
                raise ValueError("Wallpaper exceeds 300 KiB")
            result.update(white_contrast(image, dim))
        elif kind == "banner":
            allowed = {(160, 90), (240, 135), (320, 180), (480, 270), (640, 360)}
            if image.size not in allowed or fmt not in {"PNG", "JPEG"}:
                raise ValueError("Banner must use a documented 16:9 TV density size")
            result["text_and_locale_acceptance"] = "NOT_RUN: inspect the exact app name visually"
    result["status"] = "PASS"
    return result


def export_icon(source, output):
    image = icon_image(source, minimum=320)
    output = Path(output)
    names = ["cyt_icon_160.png", "cyt_icon_320.png", "cyt_icon.ico", "export.json"]
    if any((output / name).exists() for name in names):
        raise FileExistsError("Choose a new output directory; icon exports already exist")
    exports = []
    for size in (160, 320):
        target = output / f"cyt_icon_{size}.png"
        write_new(target, encoded(image.resize((size, size), Image.Resampling.LANCZOS), "PNG"))
        exports.append(check(target, "launcher"))
    target = output / "cyt_icon.ico"
    write_new(target, encoded(image, "ICO", sizes=[(s, s) for s in ICO_SIZES]))
    exports.append(check(target, "ico"))
    record = {"source": Path(source).as_posix(), "source_sha256": digest(source),
              "operation": "resize and encode only; no generation or alpha removal",
              "exports": exports, "visual_inspection": "NOT_RUN"}
    write_new(output / "export.json", (json.dumps(record, indent=2) + "\n").encode("utf-8"))
    return record


def wallpaper(source, target):
    target = Path(target)
    record_path = target.with_suffix(target.suffix + ".json")
    if target.exists() or record_path.exists():
        raise FileExistsError("Choose a new wallpaper path; output or record already exists")
    image, _ = read_image(source)
    if image.convert("RGBA").getchannel("A").getextrema()[0] < 255:
        raise ValueError("Wallpaper source must be opaque; do not silently flatten alpha")
    width, height = image.size
    ratio = 16 / 9
    crop_w, crop_h = (height * ratio, height) if width / height > ratio else (width, width / ratio)
    crop = ((width - crop_w) / 2, (height - crop_h) / 2,
            (width + crop_w) / 2, (height + crop_h) / 2)
    ready = ImageOps.fit(image.convert("RGB"), (1920, 1080), method=Image.Resampling.LANCZOS)
    for quality in range(90, 39, -5):
        data = encoded(ready, "JPEG", quality=quality, optimize=True)
        if len(data) <= MAX_WALLPAPER_BYTES:
            break
    else:
        raise ValueError("Could not meet 300 KiB; choose less detailed artwork")
    write_new(target, data)
    record = {"source": Path(source).as_posix(), "source_sha256": digest(source),
              "source_dimensions": image.size, "center_crop_box": crop,
              "upscaled": crop_w < 1920 or crop_h < 1080, "jpeg_quality": quality,
              "export": check(target, "wallpaper"), "visual_inspection": "NOT_RUN"}
    write_new(record_path, (json.dumps(record, indent=2) + "\n").encode("utf-8"))
    return record


def preview_icon(source, target):
    """Render actual ICO frames on test surfaces; this is inspection, not generated art."""
    ico_entries(source)
    cell_w, cell_h = 288, 310
    board = Image.new("RGB", (len(ICO_SIZES) * cell_w, 3 * cell_h + 32), "white")
    draw = ImageDraw.Draw(board)
    draw.text((12, 8), "ICO INSPECTION ONLY - actual decoded sizes; not a TV screenshot", fill="black")
    with Image.open(source) as ico:
        for row, label in enumerate(("light", "dark", "checkerboard")):
            for col, size in enumerate(ICO_SIZES):
                x, y = col * cell_w, row * cell_h + 32
                surface = Image.new("RGBA", (cell_w, cell_h), (248, 248, 248, 255) if row != 1 else (16, 20, 30, 255))
                painter = ImageDraw.Draw(surface)
                if row == 2:
                    for sy in range(0, cell_h, 16):
                        for sx in range(0, cell_w, 16):
                            if (sx // 16 + sy // 16) % 2:
                                painter.rectangle((sx, sy, sx + 15, sy + 15), fill=(190, 190, 190, 255))
                frame = ico.ico.getimage((size, size)).convert("RGBA")
                surface.alpha_composite(frame, ((cell_w - size) // 2, 36 + (256 - size) // 2))
                painter.text((10, 10), f"{label}: {size}px", fill="white" if row == 1 else "black")
                board.paste(surface.convert("RGB"), (x, y))
    write_new(target, encoded(board, "PNG"))
    return {"path": Path(target).as_posix(), "sha256": digest(target),
            "purpose": "deterministic ICO inspection sheet; visual acceptance not implied"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("check", help="Decode and check a prepared file")
    inspect.add_argument("path", type=Path)
    inspect.add_argument("--kind", required=True, choices=("icon", "launcher", "ico", "wallpaper", "banner"))
    inspect.add_argument("--dim", type=int, default=0, help="Simulated wallpaper black scrim, 0-90 percent")
    icons = sub.add_parser("export-icon", help="Export PNGs and a real multi-size ICO")
    icons.add_argument("source", type=Path)
    icons.add_argument("output", type=Path)
    walls = sub.add_parser("wallpaper", help="Prepare a 1920x1080 JPEG and conversion record")
    walls.add_argument("source", type=Path)
    walls.add_argument("target", type=Path)
    preview = sub.add_parser("preview-icon", help="Render decoded ICO sizes on light/dark/checkerboard surfaces")
    preview.add_argument("source", type=Path)
    preview.add_argument("target", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "check":
            if args.dim and args.kind != "wallpaper":
                raise ValueError("--dim applies only to wallpaper checks")
            result = check(args.path, args.kind, args.dim)
        elif args.command == "export-icon":
            result = export_icon(args.source, args.output)
        elif args.command == "preview-icon":
            result = preview_icon(args.source, args.target)
        else:
            result = wallpaper(args.source, args.target)
    except (OSError, ValueError, struct.error) as error:
        print(json.dumps({"status": "FAIL", "reason": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
