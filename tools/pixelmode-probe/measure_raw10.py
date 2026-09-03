"""
Measure a MIPI RAW10 buffer captured by PixelModeProbe.

Reports the black fraction the same way IMPL-40/43/44 did -- PIL, grayscale,
threshold < 4, on the original -- and then answers the question that matters
for the ishtar RAW payload geometry diagnosis: is content spread across the
whole frame, or confined to one quadrant?

RAW10 layout (Android ImageFormat.RAW10, MIPI CSI-2): every 5 bytes hold 4
pixels. Bytes 0..3 are the HIGH 8 bits of pixels 0..3; byte 4 packs the 2 low
bits of each. So dropping every 5th byte yields an exact 8-bit grayscale image
-- no interpolation, no guessing -- which is precisely what the threshold-<4
convention wants. numpy is not installed on this host; strided slice assignment
does the de-interleave in C, so this stays fast on a 60 MB buffer.

usage: python measure_raw10.py <file.raw> <width> <height> <rowStride>
"""

import sys
from PIL import Image


def unpack_raw10_to_l(data, width, height, row_stride):
    """Return 8-bit grayscale bytes (width*height), dropping the 2 LSBs."""
    packed_row = width * 5 // 4
    if row_stride != packed_row:
        raise SystemExit(
            "row padding present (rowStride=%d, packed row=%d); "
            "this script assumes an unpadded buffer" % (row_stride, packed_row)
        )
    expected = row_stride * height
    if len(data) < expected:
        raise SystemExit("buffer too small: %d < %d" % (len(data), expected))
    body = data[:expected]

    n = len(body) // 5            # number of 4-pixel groups
    out = bytearray(4 * n)
    out[0::4] = body[0::5]
    out[1::4] = body[1::5]
    out[2::4] = body[2::5]
    out[3::4] = body[3::5]
    return bytes(out[: width * height])


def black_fraction(img, threshold=4):
    hist = img.histogram()
    total = sum(hist)
    return sum(hist[:threshold]) / float(total), total


def main():
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    path, width, height, stride = (
        sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    )

    with open(path, "rb") as fh:
        data = fh.read()

    print("file        : %s" % path)
    print("bytes       : %d" % len(data))
    print("geometry    : %dx%d  rowStride=%d" % (width, height, stride))

    gray = unpack_raw10_to_l(data, width, height, stride)
    img = Image.frombytes("L", (width, height), gray)

    frac, total = black_fraction(img)
    print("")
    print("BLACK FRACTION (PIL, grayscale, threshold < 4, on the original)")
    print("  black px  : %d / %d" % (int(round(frac * total)), total))
    print("  fraction  : %.4f" % frac)

    # Quadrant occupancy -- the decisive measurement. A folded payload puts all
    # content in one quadrant and leaves the other three at zero.
    print("")
    print("QUADRANT OCCUPANCY (each %dx%d)" % (width // 2, height // 2))
    hw, hh = width // 2, height // 2
    names = [("top-left", 0, 0), ("top-right", hw, 0),
             ("bottom-left", 0, hh), ("bottom-right", hw, hh)]
    for name, x, y in names:
        q = img.crop((x, y, x + hw, y + hh))
        qf, qtotal = black_fraction(q)
        mn, mx = q.getextrema()
        # mean without numpy
        qh = q.histogram()
        mean = sum(i * c for i, c in enumerate(qh)) / float(qtotal)
        print("  %-13s black=%.4f  min=%3d max=%3d mean=%7.3f"
              % (name, qf, mn, mx, mean))

    print("")
    print("VERDICT")
    quads = []
    for name, x, y in names:
        q = img.crop((x, y, x + hw, y + hh))
        qf, _ = black_fraction(q)
        quads.append((name, qf))
    live = [n for n, f in quads if f < 0.99]
    if len(live) == 1:
        print("  FOLDED: content confined to the %s quadrant only." % live[0])
    elif len(live) == 0:
        print("  EMPTY: every quadrant is black.")
    else:
        print("  SPREAD: content present in %d quadrants (%s)."
              % (len(live), ", ".join(live)))


if __name__ == "__main__":
    main()
