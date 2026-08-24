#!/usr/bin/env python3
"""
IMX989 sensor surucu modu tasiyicisi (ishtar / Xiaomi 13 Ultra)

13U-989-DCG16+LN2+LN4 modundeki dcg/ln2/ln4 yamalarini, modun temel aldigi
eski stok blob'dan cikarip cihazdan cekilen GUNCEL surucuye tasir ve
QTI Chromatix CRC32'sini yeniden hesaplar.

Dosya bicimi (dogrulanmis):
  0x00  "QTI Chromatix Header"
  0x1C  u32  = dosya_boyutu - 4
  0xB8  u32  = veri bolgesi taban ofseti
  0xBC  u32  = veri bolgesi uzunlugu
  0xD0  parametre tablosu, 60 bayt/girdi:
          name[44] + offset(u32) + size(u32) + id(u32) + next(u32)
        'offset' veri bolgesine gorelidir
  son 4 bayt = zlib.crc32(data[:-4]), little-endian
"""
import struct, sys, zlib, os

TBL0   = 0xD0
ENTSZ  = 60
OFF_SZ = 0x1C
OFF_DB = 0xB8
OFF_DL = 0xBC


def parse(buf):
    if buf[:20] != b'QTI Chromatix Header':
        raise ValueError('QTI Chromatix Header imzasi yok')
    declared = struct.unpack_from('<I', buf, OFF_SZ)[0]
    if declared != len(buf) - 4:
        raise ValueError(f'0x1C boyut alani tutmuyor: {declared} != {len(buf)-4}')
    base = struct.unpack_from('<I', buf, OFF_DB)[0]
    dlen = struct.unpack_from('<I', buf, OFF_DL)[0]
    # tablo sonu = ilk gecersiz isim
    off, n = TBL0, 0
    while off + ENTSZ <= len(buf):
        raw = buf[off:off + 44]
        nm = raw.split(b'\0')[0]
        if not nm or not all(32 <= ch < 127 for ch in nm):
            break
        off += ENTSZ; n += 1
    return {'base': base, 'dlen': dlen, 'nent': n, 'tbl_end': off}


def crc_ok(buf):
    return struct.pack('<I', zlib.crc32(buf[:-4]) & 0xffffffff) == buf[-4:]


def seal(buf):
    """0x1C boyut alanini ve sondaki CRC32'yi tazele."""
    b = bytearray(buf)
    struct.pack_into('<I', b, OFF_SZ, len(b) - 4)
    b[-4:] = struct.pack('<I', zlib.crc32(bytes(b[:-4])) & 0xffffffff)
    return bytes(b)


def extract(stock, enable):
    """stock -> enable farkini (tablo yamalari, veri yamalari) olarak cikar."""
    if len(stock) != len(enable):
        raise ValueError('stok ve enable boyutlari farkli')
    m = parse(stock)
    tbl_patches, data_patches = {}, []
    diffs = [k for k in range(len(stock) - 4) if stock[k] != enable[k]]
    run = []
    for k in diffs:
        if k < m['tbl_end']:
            idx = (k - TBL0) // ENTSZ
            fo  = TBL0 + idx * ENTSZ + 44          # tum 4 alani birden al
            tbl_patches[idx] = (stock[fo:fo + 16], enable[fo:fo + 16])
        else:
            rel = k - m['base']
            if run and rel - run[-1] <= 3: run.append(rel)
            else:
                if run: data_patches.append(run)
                run = [rel]
    if run: data_patches.append(run)
    out = []
    for g in data_patches:
        a, b = g[0], g[-1] + 1
        out.append((a, stock[m['base'] + a:m['base'] + b],
                       enable[m['base'] + a:m['base'] + b]))
    return tbl_patches, out


def apply(target, tbl_patches, data_patches, label):
    m = parse(target)
    buf = bytearray(target)
    problems = []
    for idx, (old, new) in sorted(tbl_patches.items()):
        fo = TBL0 + idx * ENTSZ + 44
        if idx >= m['nent']:
            problems.append(f'tablo#{idx}: hedefte yok'); continue
        cur = bytes(buf[fo:fo + 16])
        if cur != old:
            problems.append(f'tablo#{idx}: beklenen {old.hex()} bulunan {cur.hex()}'); continue
        buf[fo:fo + 16] = new
    for rel, old, new in data_patches:
        fo = m['base'] + rel
        cur = bytes(buf[fo:fo + len(old)])
        if cur != old:
            problems.append(f'veri@rel{rel}: beklenen {old.hex()} bulunan {cur.hex()}'); continue
        buf[fo:fo + len(new)] = new
    if problems:
        raise RuntimeError(f'[{label}] {len(problems)} yama uygulanamadi:\n  ' + '\n  '.join(problems))
    return seal(bytes(buf))


def main():
    mod, target, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
    BIN = 'com.qti.sensormodule.ishtar_semco_imx989_wide.bin'
    stock = open(os.path.join(mod, 'dcg', 'disable', BIN), 'rb').read()
    cur   = open(target, 'rb').read()

    for nm, b in (('mod-stok', stock), ('guncel', cur)):
        p = parse(b)
        print(f'{nm:<9} boyut={len(b)} girdi={p["nent"]} veri_taban={p["base"]} veri_uzn={p["dlen"]} CRC={"OK" if crc_ok(b) else "HATALI"}')
    print()

    os.makedirs(outdir, exist_ok=True)
    # stok referans: cihazdan cekilen dosyanin aynisi
    open(os.path.join(outdir, 'stock.bin'), 'wb').write(cur)
    print(f'stock.bin  <- degistirilmemis guncel surucu  crc32={zlib.crc32(cur[:-4])&0xffffffff:08x}')

    for mode in ('dcg', 'ln2', 'ln4'):
        en = open(os.path.join(mod, mode, 'enable', BIN), 'rb').read()
        t, d = extract(stock, en)
        res = apply(cur, t, d, mode)
        assert len(res) == len(cur), 'boyut degisti'
        assert crc_ok(res), 'CRC dogrulanamadi'
        path = os.path.join(outdir, f'{mode}.bin')
        open(path, 'wb').write(res)
        nd = sum(1 for k in range(len(cur)) if cur[k] != res[k])
        print(f'{mode}.bin    <- {len(t):>2} tablo + {len(d):>2} veri yamasi, '
              f'{nd} bayt farkli, CRC {cur[-4:].hex()} -> {res[-4:].hex()}  [DOGRULANDI]')


if __name__ == '__main__':
    main()
