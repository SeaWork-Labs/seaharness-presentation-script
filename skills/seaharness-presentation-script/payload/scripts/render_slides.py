#!/usr/bin/env python3
# Copyright (c) OpenAI. All rights reserved.
"""Rasterize PDFs to per-page PNGs. Optional debugging aid, not a shipping gate.

PPTX input needs a presentation renderer that this runtime does not ship; the
error message says so and points at Presentation Preview instead.
"""

import argparse
import xml.etree.ElementTree as ET
from os import makedirs
from os.path import abspath, expanduser, join, splitext
from typing import Sequence
from zipfile import ZipFile

import pypdfium2 as pdfium

EMU_PER_INCH: int = 914_400
PRESENTATION_EXTS = (".pptx", ".ppsx", ".potx", ".pptm", ".ppsm", ".potm")


def calc_dpi_via_ooxml(input_path: str, max_w_px: int, max_h_px: int) -> int:
    """Calculate DPI from OOXML `ppt/presentation.xml` slide size (cx/cy in EMUs)."""
    with ZipFile(input_path, "r") as zf:
        xml = zf.read("ppt/presentation.xml")
    root = ET.fromstring(xml)
    ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
    sld_sz = root.find("p:sldSz", ns)
    if sld_sz is None:
        raise RuntimeError("Slide size not found in presentation.xml")
    cx = int(sld_sz.get("cx") or 0)
    cy = int(sld_sz.get("cy") or 0)
    if cx <= 0 or cy <= 0:
        raise RuntimeError("Invalid slide size values in presentation.xml")
    width_in = cx / EMU_PER_INCH
    height_in = cy / EMU_PER_INCH
    return round(min(max_w_px / width_in, max_h_px / height_in))


def calc_dpi_via_pdf(input_path: str, max_w_px: int, max_h_px: int) -> int:
    """Compute DPI from the first PDF page size (points, 1/72 inch)."""
    document = pdfium.PdfDocument(input_path)
    try:
        if len(document) < 1:
            raise RuntimeError("PDF has no pages: " + input_path)
        page = document[0]
        try:
            width_pts, height_pts = page.get_size()
        finally:
            page.close()
    finally:
        document.close()

    width_in = width_pts / 72.0
    height_in = height_pts / 72.0
    if width_in <= 0 or height_in <= 0:
        raise RuntimeError("Invalid PDF page size values.")
    return round(min(max_w_px / width_in, max_h_px / height_in))


def _pptx_not_renderable(input_path: str) -> RuntimeError:
    return RuntimeError(
        "PPTX rasterization needs a presentation renderer that the office runtime "
        "does not ship, so this script cannot render "
        + input_path
        + ".\n"
        "Use Presentation Preview for the visual check. If you still need PNGs, convert "
        "the deck to PDF with the tool that produced it and pass that PDF to this script; "
        "PDF rasterization works."
    )


def rasterize(
    input_path: str,
    out_dir: str,
    dpi: int,
) -> Sequence[str]:
    """Rasterise a PDF to PNG files placed in out_dir and return the image paths."""
    makedirs(out_dir, exist_ok=True)
    input_path = abspath(input_path)

    if input_path.lower().endswith(PRESENTATION_EXTS):
        raise _pptx_not_renderable(input_path)

    if not input_path.lower().endswith(".pdf"):
        raise RuntimeError("Rasterization is supported for PDF inputs only.")

    scale = dpi / 72.0
    document = pdfium.PdfDocument(input_path)
    final_paths = []
    try:
        for index in range(len(document)):
            page = document[index]
            try:
                image = page.render(scale=scale).to_pil()
            finally:
                page.close()
            dst_path = join(out_dir, f"slide-{index + 1}.png")
            image.save(dst_path, format="PNG")
            final_paths.append(dst_path)
    finally:
        document.close()

    return final_paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Render PDF slides to images.")
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to the input PDF file.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help=(
            "Output directory for the rendered images. "
            "Defaults to a folder next to the input named after the input file (without extension)."
        ),
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1600,
        help=(
            "Approximate maximum width in pixels after isotropic scaling (default 1600). "
            "The actual value may exceed slightly."
        ),
    )
    parser.add_argument(
        "--height",
        type=int,
        default=900,
        help=(
            "Approximate maximum height in pixels after isotropic scaling (default 900). "
            "The actual value may exceed slightly."
        ),
    )
    args = parser.parse_args()

    input_path = abspath(expanduser(args.input_path))
    out_dir = abspath(expanduser(args.output_dir)) if args.output_dir else splitext(input_path)[0]
    if input_path.lower().endswith(PRESENTATION_EXTS):
        raise _pptx_not_renderable(input_path)
    dpi = calc_dpi_via_pdf(input_path, args.width, args.height)
    rasterize(input_path, out_dir, dpi)
    print("Slides rendered to " + out_dir)


if __name__ == "__main__":
    main()
