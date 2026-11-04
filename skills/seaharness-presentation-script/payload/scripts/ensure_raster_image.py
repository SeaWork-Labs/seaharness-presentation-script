#!/usr/bin/env python3
"""Ensures input images are rasterized, converting to PNG when needed. Primarily used to
preview image assets extracted from PowerPoint files.

Dependencies used by this tool:
- Pillow: raster input validation and PNG normalization
- pypdfium2: PDF rasterization (first page)

Formats that need a converter the office runtime does not ship raise RuntimeError
instead of shelling out to a missing binary: EMF/WMF/EMZ/WMZ, SVG/SVGZ, JPEG XR,
HEIF, and EPS/PS.
"""

import argparse
from os import listdir, makedirs
from os.path import basename, dirname, expanduser, isfile, join, splitext

import pypdfium2 as pdfium

RASTER_EXTS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".webp",
}

# Formats this runtime recognises but cannot rasterize.
UNSUPPORTED_HINT = {
    ".emf": "No EMF/WMF converter is bundled with the office runtime.",
    ".wmf": "No EMF/WMF converter is bundled with the office runtime.",
    ".emz": "No EMF/WMF converter is bundled with the office runtime.",
    ".wmz": "No EMF/WMF converter is bundled with the office runtime.",
    ".svg": "No SVG rasterizer (sharp) is bundled with the office runtime.",
    ".svgz": "No SVG rasterizer (sharp) is bundled with the office runtime.",
    ".wdp": "No JPEG XR decoder (JxrDecApp) is bundled with the office runtime.",
    ".jxr": "No JPEG XR decoder (JxrDecApp) is bundled with the office runtime.",
    ".heic": "No HEIF decoder (heif-convert) is bundled with the office runtime.",
    ".heif": "No HEIF decoder (heif-convert) is bundled with the office runtime.",
    ".pdf": "PDF rasterization requires pypdfium2.",
    ".eps": "No EPS/PS converter is bundled with the office runtime.",
    ".ps": "No EPS/PS converter is bundled with the office runtime.",
}

CONVERTIBLE_EXTS = set(UNSUPPORTED_HINT) | {".pdf"}

SUPPORTED_EXTS = RASTER_EXTS | CONVERTIBLE_EXTS

PDF_RASTER_DPI = 200


def _rasterize_pdf_first_page(src_path: str, dst_path: str) -> None:
    document = pdfium.PdfDocument(src_path)
    try:
        if len(document) < 1:
            raise RuntimeError("No PDF pages were rendered: " + src_path)
        page = document[0]
        try:
            image = page.render(scale=PDF_RASTER_DPI / 72.0).to_pil()
        finally:
            page.close()
        image.save(dst_path, format="PNG")
    finally:
        document.close()


def _unsupported_format(path: str, reason: str) -> None:
    raise RuntimeError(f"Unsupported image format for rasterization: {path}. {reason}")


def ensure_raster_image(path: str, out_dir: str | None = None) -> str:
    """Return a raster image path for the given input, converting when needed.

    - Known raster formats are returned as-is
    - PDFs are rasterized (first page) via the bundled pypdfium2
    - Formats whose converter is not bundled raise RuntimeError

    Raises ValueError if the extension is not supported.
    """
    base, ext = splitext(path)
    ext_lower = ext.lower()
    out_dir = out_dir or dirname(path)
    out_path = join(out_dir, basename(base) + ".png")

    if ext_lower == ".pdf":
        makedirs(out_dir, exist_ok=True)
        _rasterize_pdf_first_page(path, out_path)
        if isfile(out_path):
            return out_path
        raise RuntimeError("PDF rasterization succeeded but output file not found: " + out_path)

    if ext_lower in UNSUPPORTED_HINT:
        _unsupported_format(path, UNSUPPORTED_HINT[ext_lower])

    if ext_lower in RASTER_EXTS:
        return path

    raise ValueError(f"Unsupported image format for montage: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=("Ensure input images are rasterized; convert to PNG if needed.")
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input_files", nargs="+", help="List of input image file paths")
    group.add_argument("--input_dir", help="Directory containing input images")
    parser.add_argument(
        "--output_dir",
        default=None,
        help=(
            "Directory to write converted PNGs. If omitted, converted files are written next to inputs."
        ),
    )
    args = parser.parse_args()

    if args.input_files:
        paths = [expanduser(p) for p in args.input_files]
    else:
        input_dir = expanduser(args.input_dir)
        names = listdir(input_dir)
        paths = [
            join(input_dir, f)
            for f in names
            if isfile(join(input_dir, f)) and splitext(f)[1].lower() in SUPPORTED_EXTS
        ]
        if not paths:
            raise SystemExit("No files with supported extensions in input_dir")

    out_dir = expanduser(args.output_dir) if args.output_dir else None
    converted_paths = []
    for p in paths:
        if ensure_raster_image(p, out_dir) != p:
            converted_paths.append(p)

    if converted_paths:
        print("Converted the following files to PNG:\n" + "\n".join(converted_paths))


if __name__ == "__main__":
    main()
