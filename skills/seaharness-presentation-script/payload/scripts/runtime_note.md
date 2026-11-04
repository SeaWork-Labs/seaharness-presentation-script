Optional render scripts in this folder are debugging aids. They are not a shipping gate. Default visual check is Presentation Preview.

What actually runs here:
- `render_slides.py` rasterizes PDFs page by page (pypdfium2, bundled).
- `ensure_raster_image.py` rasterizes the first page of a PDF (pypdfium2, bundled).
- `create_montage.py` builds a contact sheet from raster images (Pillow, bundled).

What does not: PPTX rasterization needs a presentation renderer that the office runtime does not ship. `render_slides.py` says so and stops. Convert the deck to PDF with the tool that produced it if you need PNGs, or use Presentation Preview.
