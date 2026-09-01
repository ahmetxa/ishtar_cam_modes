#!/usr/bin/env python3
"""
IMX989 mod 0 (50MP) 12-bit adayi  (ishtar / Xiaomi 13 Ultra)  -- Faz 5.1

Mod 0, FOTO_MODLARI listesinde YOK: dcg/ln uretecleri ona hic dokunmuyor.
Sonuc olarak dcgB gibi bir blobda kuresel whiteLevel 4095'e (12-bit) cekilmis
ama mod 0 hala 10-bit cikis veriyor -- iki katmanin birbirini dislamasinin
sebebi bu (Project-Ontology degismez 4).

Bu arac YALNIZ mod 0'i 12-bit'e tasir. Tek amaclidir: basarisiz olursa
geri alinacak tek sey budur.

ln_multimode.apply_ln() DOGRUDAN KULLANILAMAZ. O yol fll'i FLL_MIN=3200'e
kirpiyor; yazildigi modlarin hepsi <=3072 satir oldugu icin bu guvenli.
Mod 0 ise 6144 satir -- 3200'e kirpmak kare uzunlugunu karenin kendisinden
kisa yapardi. Burada fll'e HIC dokunulmuyor (stok 8728 zaten 6144'ten buyuk).

Uygulanan degisiklikler (hepsi gercek bloblardan olculerek gerekcelendirildi):
  0x0112 / 0x0113   0x0A -> 0x0C     cikis formati 10-bit -> 12-bit
  streamConfiguration dt 0x2B -> 0x2C, bpp 10 -> 12
  0x0342 / 0x0343 + resolutionData[12]   llp *= 12/10, 16'ya yuvarlanir
        RAW12 akisinin MIPI'ye sigmasi icin; ln_multimode.py:196-199 bu
        gereksinimi cihazda dogrulanmis olarak kaydediyor.
  resolutionData[13] (fll)   DEGISMIYOR  -- yukariya bakiniz.

Dosya bicimi icin bkz. port_sensor_mod.py
"""
import struct, sys, os, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ln_multimode import Sensor, REG_FMT_HI, REG_FMT_LO, REG_LLP_HI, REG_LLP_LO  # noqa: E402

MODE = 0
DT_RAW10, BPP_RAW10 = 0x2B, 10
DT_RAW12, BPP_RAW12 = 0x2C, 12
FMT_10BIT, FMT_12BIT = 0x0A, 0x0C


def dims(s, m):
    o = s.base + s.eoff(s.sc[m])
    return (struct.unpack_from('<I', s.buf, o + 20)[0],
            struct.unpack_from('<I', s.buf, o + 24)[0])


def check(s, m):
    """Mod m bu donusumu kaldirabiliyor mu? Sorun listesi doner."""
    R = s.regs(m)
    bad = []
    for a in (REG_FMT_HI, REG_FMT_LO, REG_LLP_HI, REG_LLP_LO):
        if a not in R:
            bad.append('reg 0x%04X yok' % a)
    if bad:
        return bad, None
    for a in (REG_FMT_HI, REG_FMT_LO):
        v = s.u32(R[a][1])
        if v != FMT_10BIT:
            bad.append('0x%04X = 0x%02X (0x%02X bekleniyor)' % (a, v, FMT_10BIT))
    _, _, dt, bpp = s.stream0(m)
    if (dt, bpp) != (DT_RAW10, BPP_RAW10):
        bad.append('akis dt=0x%02X bpp=%d (RAW10 bekleniyor)' % (dt, bpp))
    llp_reg = (s.u32(R[REG_LLP_HI][1]) << 8) | s.u32(R[REG_LLP_LO][1])
    if s.res_field(m, 12) != llp_reg:
        bad.append('resolutionData llp %d != register %d' % (s.res_field(m, 12), llp_reg))
    fll, h = s.res_field(m, 13), dims(s, m)[1]
    if fll < h:
        bad.append('fll %d < yukseklik %d' % (fll, h))
    return bad, llp_reg


def apply_12bit(s, m):
    bad, llp_cur = check(s, m)
    if bad:
        raise RuntimeError('mod %d donusturulemez: %s' % (m, '; '.join(bad)))
    R = s.regs(m)
    llp_new = ((llp_cur * 12 // 10) + 15) // 16 * 16
    s.set_entry_value(R[REG_LLP_HI][1], (llp_new >> 8) & 0xFF)
    s.set_entry_value(R[REG_LLP_LO][1], llp_new & 0xFF)
    s.set_res_field(m, 12, llp_new)
    s.set_entry_value(R[REG_FMT_HI][1], FMT_12BIT)
    s.set_entry_value(R[REG_FMT_LO][1], FMT_12BIT)
    dtr, bppr, _, _ = s.stream0(m)
    s.write_data(dtr, struct.pack('<I', DT_RAW12), s.sc[m])
    s.write_data(bppr, struct.pack('<I', BPP_RAW12), s.sc[m])
    return llp_cur, llp_new


def main(src, dst):
    s = Sensor(src)
    w, h = dims(s, MODE)
    print('taban   %s  %d bayt  md5 %s' % (
        os.path.basename(src), len(s.buf), hashlib.md5(bytes(s.buf)).hexdigest()))
    print('mod %d   %dx%d  fll=%d (dokunulmuyor)' % (MODE, w, h, s.res_field(MODE, 13)))
    llp_cur, llp_new = apply_12bit(s, MODE)
    print('        llp %d -> %d  (0x0342=0x%02X 0x0343=0x%02X)'
          % (llp_cur, llp_new, (llp_new >> 8) & 0xFF, llp_new & 0xFF))
    print('        0x0112/0x0113 0x0A -> 0x0C, akis dt 0x2B -> 0x2C, bpp 10 -> 12')
    out = s.seal()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'wb').write(out)
    print('aday    %s  %d bayt  md5 %s  crc32 %08x'
          % (os.path.basename(dst), len(out), hashlib.md5(out).hexdigest(),
             struct.unpack('<I', out[-4:])[0]))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
