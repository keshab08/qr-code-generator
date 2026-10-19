# Warehouse Shelf Label Generator

Generate printable PDF labels (Code128 barcode or QR code) for warehouse shelf names, so every shelf can be scanned and identified quickly.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

<!-- Add a screenshot of the generated PDF here, e.g. docs/preview.png -->
<!-- ![Preview of the generated labels](docs/preview.png) -->

## Motivation

At my workplace, the first shelf of a position is full, and additional products need extra storage space. The solution is a second shelf placed opposite the first one, but this extra shelf had **no numbering at all**, so it could not be identified or scanned in the logistics process.

The existing shelf is named like this:

```
ws-02-00-01-01-A
```

and the new opposite shelf continues the same scheme with a `-2` suffix:

```
ws-02-00-01-01-A-2
```

Writing and printing these labels by hand for hundreds of shelf positions is slow and error-prone, so this tool generates them automatically from a few settings and exports them as a ready-to-print PDF.

## Features

- Generates labels in sequence from a configurable naming pattern
- Two label styles:
  - **`barcode`**: Code128 "zebra stripes". Flat, wide and readable by practically every handheld warehouse scanner (recommended)
  - **`qr_flat`**: a QR code stretched into a flat rectangle
- Human-readable text under each code, so the shelf name is still readable if a scan fails
- Vector output: sharp at any print size
- Automatic grid layout with page breaks on A4
- Light cutting guide around each label

## Naming Pattern

```
<PREFIX>-<number>-<LETTER>-<SUFFIX>
```

| Part       | Description                                      | Example    |
|------------|--------------------------------------------------|------------|
| `PREFIX`   | Fixed start of every label                       | `WS-02-01` |
| `number`   | Counter from `START` to `END`, zero-padded       | `01` to `28` |
| `LETTER`   | One label per letter, for every number           | `A` to `F` |
| `SUFFIX`   | Fixed end of every label (marks the opposite shelf) | `2`     |

With the default settings the output is:

```
WS-02-01-01-A-2
WS-02-01-01-B-2
...
WS-02-01-01-F-2
WS-02-01-02-A-2
...
WS-02-01-28-F-2
```

That is 28 numbers x 6 letters = **168 labels**.

## Installation

Requires Python 3.8 or newer.

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python -m pip install -r requirements.txt
```

`requirements.txt`:

```
segno
reportlab
```

## Usage

1. Open `QR_Generator.py` and adjust the settings block at the top.
2. Run the script:

   ```bash
   python QR_Generator.py
   ```

3. Open the generated `labels.pdf` and print it at **100% scale** (do not use "fit to page", otherwise the codes get resized and may scan worse).

## Configuration

All settings are constants at the top of `QR_Generator.py`.

| Setting                 | Default          | Description                                           |
|-------------------------|------------------|-------------------------------------------------------|
| `MODE`                  | `"barcode"`      | `"barcode"` or `"qr_flat"`                            |
| `PREFIX`                | `"WS-02-01"`     | Fixed start of the label text                         |
| `START`, `END`          | `1`, `28`        | Number range (inclusive)                              |
| `LETTERS`               | `"ABCDEF"`       | Letters generated for each number                     |
| `SUFFIX`                | `"2"`            | Fixed end of the label text                           |
| `COLS`                  | `3`              | Labels per row                                        |
| `CELL_W`, `CELL_H`      | `65 mm`, `25 mm` | Size of one label cell                                |
| `BAR_HEIGHT`            | `14 mm`          | Barcode height (taller is easier to scan from afar)   |
| `BAR_WIDTH`             | `0.25 mm`        | Thinnest bar; below ~0.2 mm cheap scanners may struggle |
| `QR_W`, `QR_H`          | `40 mm`, `16 mm` | Flat QR size; `QR_W / QR_H` is the stretch factor     |
| `OUTPUT`                | `"labels.pdf"`   | Name of the generated file                            |

## Tips for Reliable Scanning

- **Test before printing everything.** Print one page and try it with your real scanners first. This matters most for `qr_flat`, since a stretched QR code is not guaranteed to be readable by every scanner. If scans are unreliable, lower the stretch factor to about 2.0 or switch to `barcode`.
- Keep the label surface clean and flat, and use matte label paper to avoid glare.
- The QR code uses error correction level M, so it survives some scratches and dirt.
- Do not remove the quiet zone (empty margin) around the codes.

## Project Structure

```
.
├── QR_Generator.py     # label generator
├── requirements.txt    # dependencies
└── README.md
```

## Built With

- [segno](https://github.com/heuer/segno) for QR code generation
- [ReportLab](https://www.reportlab.com/opensource/) for PDF layout and Code128 barcodes

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
