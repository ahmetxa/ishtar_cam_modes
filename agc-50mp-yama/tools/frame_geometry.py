#!/usr/bin/env python3
"""Faz 4.6 host-side frame geometry diagnosis (VAL-GEOMETRY).

Measures the structure of the AGC full-resolution artifact and tests the
row-pairing reconstruction hypothesis stated in Faz4.6 section 3: that a
4096-wide payload was written linearly into an 8192-wide raster.

Axis convention. The JPEG is stored rotated: SOF is 6144x8192 while EXIF
ImageWidth/ImageLength carry the sensor raster's 8192x6144. Every figure this
tool reports is in RASTER axes (8192 across a row, 6144 rows), because both the
model in section 3 and the HAL's buffer geometry are stated that way. The
--rot flag fixes the JPEG->raster rotation; run `identify` first to pick it.

Pure PIL, no numpy: profiles are computed with BOX resize, which averages in C.
A profile value of exactly 0.0 means every pixel in that line is 0, so it is a
sound test for "pure black" and not merely for "dark".

The reconstruction exploits an identity worth stating, because it is why this
probe is cheap: splitting every raster row at its midpoint and emitting the two
halves as consecutive rows leaves the linear byte stream untouched. Un-folding
is therefore just re-reading the same bytes at width 4096, which is one C call
rather than a per-row loop over 50 megapixels.

Usage:
  frame_geometry.py identify  <img>
  frame_geometry.py measure   <img> [--rot 90|270] [--fold-width N]
  frame_geometry.py unfold    <img> <out> [--rot 90|270] [--fold-width N]
  frame_geometry.py fold      <img> <out> --to-width N     (inverse control)
"""

import argparse
import struct

from PIL import Image, ImageStat

Image.MAX_IMAGE_PIXELS = None  # 50 MP is the subject, not a decompression bomb

PAYLOAD_W = 4096


def sof_size(path):
    """Read dimensions from the SOF marker, per VAL-CAPTURE.

    Never from the filename and never from a gallery label; those have been
    wrong in this project before.
    """
    d = open(path, "rb").read()
    i = 2
    while i < len(d) - 1:
        if d[i] != 0xFF:
            i += 1
            continue
        m = d[i + 1]
        if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        ln = struct.unpack(">H", d[i + 2:i + 4])[0]
        if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", d[i + 5:i + 9])
            return w, h, "SOF%X" % (m - 0xC0)
        if m == 0xDA:
            break
        i += 2 + ln
    raise SystemExit("no SOF marker in %s" % path)


def exif_raster(path):
    """EXIF ImageWidth/ImageLength, which AGC leaves in raster axes."""
    ex = Image.open(path).getexif()
    return ex.get(256), ex.get(257), ex.get(274)


def to_raster(im, rot):
    """Rotate a portrait JPEG into sensor raster orientation."""
    if rot == 0:
        return im
    return im.transpose(Image.ROTATE_90 if rot == 90 else Image.ROTATE_270)


def profile(im, axis):
    """Per-row (axis='row') or per-column mean luminance, via BOX resize."""
    g = im.convert("L")
    w, h = g.size
    if axis == "row":
        return list(g.resize((1, h), Image.BOX).getdata())
    return list(g.resize((w, 1), Image.BOX).getdata())


def runs(vals, pred):
    """Contiguous [start, end) spans where pred(value) holds."""
    out, s = [], None
    for i, v in enumerate(vals):
        if pred(v):
            if s is None:
                s = i
        elif s is not None:
            out.append((s, i))
            s = None
    if s is not None:
        out.append((s, len(vals)))
    return out


def content_band(im):
    """The first run of non-black raster rows, as ((start, end), cropped)."""
    w, h = im.size
    rows = profile(im, "row")
    spans = [r for r in runs(rows, lambda v: v > 0) if r[1] - r[0] >= 8]
    if not spans:
        raise SystemExit("no content band found")
    cs, ce = spans[0]
    return (cs, ce), im.crop((0, cs, w, ce))


def cmd_identify(a):
    w, h, sof = sof_size(a.img)
    ew, eh, orient = exif_raster(a.img)
    print("file            %s" % a.img)
    print("SOF             %s  %dx%d" % (sof, w, h))
    print("EXIF raster     %sx%s   orientation=%s" % (ew, eh, orient))
    if ew and eh and (ew, eh) != (w, h):
        print("axis mapping    encoded frame is rotated 90 deg from raster;")
        print("                JPEG height (%d) is the raster row direction," % h)
        print("                JPEG width  (%d) is the raster row count." % w)
    else:
        print("axis mapping    encoded frame already in raster axes")


def cmd_measure(a):
    im = to_raster(Image.open(a.img), a.rot)
    w, h = im.size
    fold = a.fold_width
    print("raster size     %dx%d" % (w, h))

    rows = profile(im, "row")
    black = runs(rows, lambda v: v == 0)
    nblack = sum(e - s for s, e in black)
    content = [r for r in runs(rows, lambda v: v > 0) if r[1] - r[0] >= 8]

    print("")
    print("-- black region (raster rows whose mean luminance is exactly 0) --")
    print("pure-black rows %d of %d   fraction %.4f   predicted 0.7500"
          % (nblack, h, nblack / h))
    for s, e in [r for r in black if r[1] - r[0] >= 8][:6]:
        print("  black span    rows %d..%d  (%d rows)" % (s, e - 1, e - s))

    print("")
    print("-- content band --")
    for s, e in content[:6]:
        print("  content span  rows %d..%d  (%d rows)   predicted 1536 rows"
              % (s, e - 1, e - s))
    if not content:
        print("  none")
        return

    (cs, ce), band = content_band(im)
    bh = ce - cs

    # Does the content run the full width of the raster, as the model requires?
    cols = profile(band, "col")
    lit = runs(cols, lambda v: v > 0)
    span = "%d..%d" % (lit[0][0], lit[-1][1] - 1) if lit else "none"
    print("  column extent %s of 0..%d   predicted full extent" % (span, w - 1))

    # The fold predicts the two halves of every raster row demosaic with
    # opposite CFA phase, so measure each half separately rather than the band
    # as a whole. "Different colour casts" becomes two triples.
    print("")
    print("-- per-half channel means (the two colour casts, as numbers) --")
    halves = (("left  (cols 0..%d)" % (fold - 1), (0, 0, fold, bh)),
              ("right (cols %d..%d)" % (fold, w - 1), (fold, 0, w, bh)))
    for name, box in halves:
        st = ImageStat.Stat(band.crop(box))
        r, g, b = st.mean[:3]
        print("  %-24s R=%7.2f G=%7.2f B=%7.2f   R/G=%.3f B/G=%.3f"
              % (name, r, g, b, r / g if g else 0, b / g if g else 0))

    print("")
    print("-- fold boundary --")
    print("  tested at column %d   (payload width predicted by the model)" % fold)

    print("")
    print("-- white edge band --")
    whites = runs(rows, lambda v: v >= 250)
    for s, e in whites[:4]:
        print("  white span    rows %d..%d  (%d rows)" % (s, e - 1, e - s))
    if not whites:
        print("  none at row mean >= 250")


def cmd_unfold(a):
    """Re-read the content band's bytes at the payload width.

    See the module docstring: this is the whole reconstruction, because the
    fold is a linear write and un-folding it is a re-interpretation of the
    same byte stream rather than a permutation of it.
    """
    im = to_raster(Image.open(a.img), a.rot).convert("RGB")
    (cs, ce), band = content_band(im)
    bw, bh = band.size
    if bw % a.fold_width:
        raise SystemExit("band width %d is not a multiple of %d"
                         % (bw, a.fold_width))
    factor = bw // a.fold_width
    out = Image.frombytes("RGB", (a.fold_width, bh * factor), band.tobytes())
    out.save(a.out)
    print("content band    raster rows %d..%d  (%dx%d)" % (cs, ce - 1, bw, bh))
    print("reconstructed   %dx%d  ->  %s" % (out.size[0], out.size[1], a.out))


def cmd_fold(a):
    """Inverse control: fold a known-good image into a wider raster."""
    im = Image.open(a.img).convert("RGB")
    w, h = im.size
    if a.to_width % w:
        raise SystemExit("target width %d is not a multiple of %d"
                         % (a.to_width, w))
    factor = a.to_width // w
    if h % factor:
        raise SystemExit("height %d is not divisible by %d" % (h, factor))
    out = Image.frombytes("RGB", (a.to_width, h // factor), im.tobytes())
    out.save(a.out)
    print("folded          %dx%d  ->  %dx%d  ->  %s"
          % (w, h, out.size[0], out.size[1], a.out))


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("identify")
    q.add_argument("img")
    q.set_defaults(fn=cmd_identify)

    q = sub.add_parser("measure")
    q.add_argument("img")
    q.add_argument("--rot", type=int, default=90, choices=(0, 90, 270))
    q.add_argument("--fold-width", type=int, default=PAYLOAD_W)
    q.set_defaults(fn=cmd_measure)

    q = sub.add_parser("unfold")
    q.add_argument("img")
    q.add_argument("out")
    q.add_argument("--rot", type=int, default=90, choices=(0, 90, 270))
    q.add_argument("--fold-width", type=int, default=PAYLOAD_W)
    q.set_defaults(fn=cmd_unfold)

    q = sub.add_parser("fold")
    q.add_argument("img")
    q.add_argument("out")
    q.add_argument("--to-width", type=int, required=True)
    q.set_defaults(fn=cmd_fold)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
