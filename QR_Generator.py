"""Generate a printable PDF of shelf labels ( flat QR code)."""

import segno
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
MODE = "barcode"          # "barcode" or "qr_flat"

# Label text: <PREFIX>-<number>-<LETTER>-<SUFFIX>
PREFIX = "WS-02-01"
START, END = 1, 28        # number range, inclusive
LETTERS = "ABCDEF"
SUFFIX = "2"

# Page layout
COLS = 3                  # labels per row
CELL_W = 65 * mm          # size of one label cell
CELL_H = 25 * mm
FONT, FONT_SIZE = "Helvetica-Bold", 9
OUTPUT = "labels.pdf"

# Barcode mode
BAR_HEIGHT = 14 * mm
BAR_WIDTH = 0.25 * mm     # width of the thinnest bar

# Flat QR mode
QR_W = 40 * mm
QR_H = 16 * mm            # stretch factor = QR_W / QR_H


# ---------------------------------------------------------------------------
# Label text generation
# ---------------------------------------------------------------------------
def labels():
    """Yield the label texts in print order, e.g. WS-02-01-01-A-2.

    Outer loop = number, inner loop = letter, so all letters of one number
    come one after another (A, B, C, ... then the next number).
    """
    for n in range(START, END + 1):
        for letter in LETTERS:
            yield f"{PREFIX}-{n:02d}-{letter}-{SUFFIX}"  # :02d pads 1 -> 01


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------
def draw_flat_qr(c, text, x, y, w, h, border=2):
    """Draw a QR code stretched to a w x h rectangle (bottom-left at x, y).

    segno only provides the QR matrix (rows of True/False for dark/light
    modules). We draw each dark module as a small rectangle ourselves. Giving
    the modules a different width and height is what flattens the code.
    `border` is the empty quiet zone in modules; scanners need it.
    """
    matrix = segno.make(text, error="m").matrix
    modules = len(matrix) + 2 * border       # matrix size plus the border on both sides
    module_w, module_h = w / modules, h / modules

    c.setFillColorRGB(0, 0, 0)
    for r, row in enumerate(matrix):
        for col, is_dark in enumerate(row):
            if is_dark:
                # The matrix starts at the top-left, but the PDF origin is
                # bottom-left, so the y position is counted from the top down.
                c.rect(
                    x + (col + border) * module_w,
                    y + h - (r + border + 1) * module_h,
                    module_w,
                    module_h,
                    stroke=0,
                    fill=1,
                )


def main():
    page_w, page_h = A4

    # Center the grid horizontally and calculate how many rows fit on a page.
    margin_x = (page_w - COLS * CELL_W) / 2
    margin_top = 10 * mm
    rows_per_page = int((page_h - 2 * margin_top) // CELL_H)

    c = canvas.Canvas(OUTPUT, pagesize=A4)

    for i, text in enumerate(labels()):
        # Index of this label on the current page; a new page starts when it wraps to 0.
        pos = i % (COLS * rows_per_page)
        if i > 0 and pos == 0:
            c.showPage()

        # Convert the index into a grid position and the cell's bottom-left corner.
        row, col = divmod(pos, COLS)
        cell_x = margin_x + col * CELL_W
        cell_y = page_h - margin_top - (row + 1) * CELL_H
        center_x = cell_x + CELL_W / 2

        # Code, centered horizontally in the cell
        if MODE == "barcode":
            bc = code128.Code128(
                text, barHeight=BAR_HEIGHT, barWidth=BAR_WIDTH, quiet=True
            )
            bc.drawOn(c, center_x - bc.width / 2, cell_y + 8 * mm)
        else:
            draw_flat_qr(c, text, center_x - QR_W / 2, cell_y + 7 * mm, QR_W, QR_H)

        # Readable text below the code
        c.setFillColorRGB(0, 0, 0)
        c.setFont(FONT, FONT_SIZE)
        c.drawCentredString(center_x, cell_y + 3 * mm, text)

        # Light grey frame as a cutting guide (remove these 3 lines if not needed)
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.setLineWidth(0.3)
        c.rect(cell_x, cell_y, CELL_W, CELL_H)

    c.save()
    print(f"Saved {OUTPUT} ({MODE})")


if __name__ == "__main__":
    main()