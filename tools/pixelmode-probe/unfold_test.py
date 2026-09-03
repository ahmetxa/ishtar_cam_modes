"""
F4.6-04 -- the row-pairing reconstruction test.

Faz4.6 scope: "un-folding the content region on the hypothesis that a 4096-wide
payload was written into an 8192-wide raster, and judging whether a coherent
scene results."

IMPL-45 established the premise numerically: the populated region of an
8192x6144 RAW10 capture is exactly 12,582,912 pixels (rows 0..1535 across the
full width), which is exactly 4096 x 3072. This script performs the un-fold and
judges coherence NUMERICALLY rather than by eye, as the project requires.

Method. The same pixel stream is read at two widths:

  A  8192 wide x 1536 tall   -- the raster as the buffer declares it
  B  4096 wide x 3072 tall   -- the raster the payload was actually written for

The discriminator is the Bayer signature, not scene smoothness. Camera 2 is
BGGR (android.sensor.info.colorFilterArrangement = BGGR), a 2x2 CFA, so in a
VALID raster adjacent rows carry different colour channels and differ strongly,
while rows two apart share phase and are smooth. The test statistic is therefore

    bayer_ratio = mean|I(y) - I(y+1)|  /  mean|I(y) - I(y+2)|

A true Bayer raster gives bayer_ratio >> 1. A reading at the wrong stride
destroys the alternation -- at double width, two true rows sit side by side in
one raster row and consecutive raster rows end up sharing phase -- giving
bayer_ratio ~ 1. Whichever width restores the alternation is the real geometry.

Scene smoothness was tried first and cannot discriminate here: the frame is dark
(mean gradients ~1.4/255), so noise dominates and both readings score alike. The
horizontal gradient is reported as a control -- a row-stride error does not
disturb horizontal structure, so it should stay near 1.0 between the readings.

usage: python unfold_test.py <file.raw> [out_prefix]
"""

import sys
from PIL import Image, ImageChops

SRC_W, SRC_H = 8192, 6144
ROW_STRIDE = 10240          # packed MIPI RAW10 row: 8192 * 10 / 8
POPULATED_ROWS = 1536       # measured by IMPL-45: last populated row is 1535


def unpack_raw10(data):
    """Exact 8-bit grayscale: in MIPI RAW10 bytes 0..3 of every 5 hold the high
    8 bits of 4 pixels, so dropping every 5th byte is lossless-to-8-bit."""
    n = len(data) // 5
    out = bytearray(4 * n)
    out[0::4] = data[0::5]
    out[1::4] = data[1::5]
    out[2::4] = data[2::5]
    out[3::4] = data[3::5]
    return bytes(out)


def mean_abs_diff(img, dx, dy):
    """Mean |I(x,y) - I(x+dx, y+dy)| computed through PIL (C speed)."""
    w, h = img.size
    a = img.crop((0, 0, w - dx, h - dy))
    b = img.crop((dx, dy, w, h))
    d = ImageChops.difference(a, b)
    hist = d.histogram()
    total = sum(hist)
    return sum(i * c for i, c in enumerate(hist)) / float(total)


def report(label, img):
    w, h = img.size
    v1 = mean_abs_diff(img, 0, 1)
    v2 = mean_abs_diff(img, 0, 2)
    h2 = mean_abs_diff(img, 2, 0)
    ratio = v1 / v2 if v2 else float("inf")
    print("  %-30s %5dx%-5d  adj(y,y+1)=%7.3f  same-phase(y,y+2)=%7.3f  "
          "BAYER RATIO=%6.2fx  horiz=%6.3f"
          % (label, w, h, v1, v2, ratio, h2))
    return ratio, h2


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    path = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else "unfold"

    data = open(path, "rb").read()
    expected = ROW_STRIDE * SRC_H
    if len(data) != expected:
        raise SystemExit("unexpected buffer size %d (want %d)" % (len(data), expected))

    gray = unpack_raw10(data)[: SRC_W * SRC_H]

    # The populated region only. Everything below row 1535 is black and would
    # dominate any gradient statistic with zeros.
    payload = gray[: SRC_W * POPULATED_ROWS]
    n = len(payload)
    print("payload pixels : %d" % n)
    print("4096 x 3072    : %d" % (4096 * 3072))
    print("match          : %s" % (n == 4096 * 3072))
    print("")

    a = Image.frombytes("L", (SRC_W, POPULATED_ROWS), payload)   # 8192 x 1536
    b = Image.frombytes("L", (4096, 3072), payload)              # 4096 x 3072

    print("BAYER SIGNATURE (a valid BGGR raster alternates between adjacent rows)")
    ra, ha = report("A  as declared (8192 wide)", a)
    rb, hb = report("B  un-folded  (4096 wide)", b)

    print("")
    print("VERDICT")
    print("  bayer_ratio  A = %6.2fx   B = %6.2fx" % (ra, rb))
    print("  horizontal control A / B = %.2fx  (should stay near 1.0)"
          % (ha / hb if hb else float("inf")))
    if rb > 4.0 and ra < 2.0:
        print("  -> B is the valid Bayer raster; A is not.")
        print("     CONFIRMED: the payload is a 4096-wide BGGR image written into")
        print("     an 8192-wide raster -- a pure row-stride error. The un-fold")
        print("     hypothesis of F4.6-04 HOLDS.")
    elif ra > 4.0 and rb < 2.0:
        print("  -> A is the valid Bayer raster. The un-fold hypothesis FAILS;")
        print("     the payload is genuinely 8192 wide and the fault is elsewhere.")
    else:
        print("  -> INCONCLUSIVE. Neither width shows a clean Bayer alternation.")

    a.resize((1024, 192), Image.NEAREST).point(lambda v: min(255, v * 3)) \
        .save(prefix + "-A-as-declared-8192.png")
    b.resize((768, 576), Image.NEAREST).point(lambda v: min(255, v * 3)) \
        .save(prefix + "-B-unfolded-4096.png")
    print("")
    print("wrote %s-A-as-declared-8192.png and %s-B-unfolded-4096.png"
          % (prefix, prefix))
    print("(DERIVED: downscaled + 3x gain for viewing; metrics above are from"
          " the full-resolution originals)")


if __name__ == "__main__":
    main()
