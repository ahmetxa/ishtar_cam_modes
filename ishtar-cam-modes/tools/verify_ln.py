#!/usr/bin/env python3
"""Uretilen LN bloblarini bagimsiz olarak dogrular.

- Her blobun CRC32 / boyut alani tutarli mi
- Her modun ilgili register + akis + resolutionData degerleri ne
- ln2f/ln4f'in MOD 1 yapilandirmasi, orijinal mod'un ln2/ln4 blobunun
  mod 1 yapilandirmasiyla BIREBIR ayni mi
"""
import struct, zlib, sys, os

TBL0, ENTSZ = 0xD0, 60
OFF_SZ, OFF_DB = 0x1C, 0xB8
ADDRS = (0x0112, 0x0113, 0x0342, 0x0343, 0x31A4)


def parse(path):
    b = open(path, 'rb').read()
    assert b[:20] == b'QTI Chromatix Header', path
    assert struct.unpack_from('<I', b, OFF_SZ)[0] == len(b) - 4, 'boyut alani: ' + path
    assert struct.pack('<I', zlib.crc32(b[:-4]) & 0xffffffff) == b[-4:], 'CRC32: ' + path
    base = struct.unpack_from('<I', b, OFF_DB)[0]
    ents, off = [], TBL0
    while off + ENTSZ <= len(b):
        nm = b[off:off + 44].split(b'\0')[0]
        if not nm or not all(32 <= c < 127 for c in nm):
            break
        o, s, i, n = struct.unpack_from('<4I', b, off + 44)
        ents.append((nm.decode(), o, s))
        off += ENTSZ
    return b, base, ents


def snapshot(path):
    b, base, ents = parse(path)
    d = lambda k: b[base + ents[k][1]:base + ents[k][1] + ents[k][2]]
    u = lambda k: struct.unpack('<I', d(k))[0] if ents[k][2] == 4 else None
    sc = [k for k, e in enumerate(ents) if e[0] == 'streamConfiguration']
    rd = [k for k, e in enumerate(ents) if e[0] == 'resolutionData'][0]
    n = len(sc)
    recsz = ents[rd][2] // n
    rdat = d(rd)
    rf = lambda m, i: struct.unpack_from('<I', rdat, m * recsz + i * 4)[0]
    sdd = [k for k, e in enumerate(ents) if e[0] == 'sensorDriverData'][0]
    g = d(sdd)
    out = {'white': struct.unpack_from('<I', g, 524)[0],
           'black': [struct.unpack_from('<I', g, o)[0] for o in (528, 532, 536, 540)],
           'modes': {}}
    for m in range(n):
        rs = rf(m, 31)
        regs = {}
        rb = d(rs)
        for r in range(0, len(rb), 40):
            f = struct.unpack_from('<10I', rb, r)
            regs[f[2]] = u(f[1])
        s0 = d(sc[m])
        out['modes'][m] = {
            'reg': {a: regs.get(a) for a in ADDRS},
            'dt': struct.unpack_from('<I', s0, 8)[0],
            'bpp': struct.unpack_from('<I', s0, 28)[0],
            'w': struct.unpack_from('<I', s0, 20)[0],
            'h': struct.unpack_from('<I', s0, 24)[0],
            'llp': rf(m, 12), 'fll': rf(m, 13),
        }
    return out


def fmt(md):
    r = md['reg']
    return ('%dx%d dt=0x%02X bpp=%-2d llp=%-6d fll=%-6d  '
            '0x0112=0x%02X 0x0113=0x%02X 0x0342=0x%02X 0x0343=0x%02X 0x31A4=%s'
            % (md['w'], md['h'], md['dt'], md['bpp'], md['llp'], md['fll'],
               r[0x0112], r[0x0113], r[0x0342], r[0x0343], r[0x31A4]))


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proj = os.path.dirname(root)
    mod = os.path.join(proj, '13U-989-DCG16+LN2+LN4')
    BN = 'com.qti.sensormodule.ishtar_semco_imx989_wide.bin'

    ref = {t: snapshot(os.path.join(mod, t, 'enable', BN)) for t in ('ln2', 'ln4')}
    new = {}
    for t in ('stock', 'ln2', 'ln4', 'ln2s', 'ln4s', 'ln2f', 'ln4f'):
        p = os.path.join(root, 'blobs', t + '.bin')
        if os.path.exists(p):
            new[t] = snapshot(p)

    print('--- kuresel seviyeler ---')
    for t, s in new.items():
        print('  %-6s whiteLevel=%-6d blackLevel=%s' % (t, s['white'], s['black']))

    print('\n--- MOD 1: orijinal mod ile karsilastirma ---')
    for a, bl in (('ln2', ('ln2', 'ln2f')), ('ln4', ('ln4', 'ln4f'))):
        r = ref[a]['modes'][1]
        print('  orijinal %-5s %s' % (a, fmt(r)))
        for t in bl:
            if t not in new:
                continue
            x = new[t]['modes'][1]
            same = (x['reg'] == r['reg'] and x['dt'] == r['dt']
                    and x['bpp'] == r['bpp'] and x['llp'] == r['llp']
                    and x['fll'] == r['fll'])
            print('  %-14s %s  %s' % (t, fmt(x), 'BIREBIR AYNI' if same else '*** FARKLI ***'))
        # kuresel seviyeler
        for t in bl:
            if t in new:
                sm = (new[t]['white'] == ref[a]['white']
                      and new[t]['black'] == ref[a]['black'])
                print('    %-12s kuresel seviye %s (%d / %s)'
                      % (t, 'AYNI' if sm else 'FARKLI', new[t]['white'], new[t]['black']))
        print()

    print('--- ln2f: yamalanan tum modlar ---')
    st = new['stock']
    for m in sorted(new['ln2f']['modes']):
        a, b2 = st['modes'][m], new['ln2f']['modes'][m]
        if a != b2:
            print('  mod %-3d %s' % (m, fmt(b2)))
    print('\n--- ln2f: DEGISMEYEN modlar (stok kalmali) ---')
    unchanged = [m for m in sorted(new['ln2f']['modes'])
                 if st['modes'][m] == new['ln2f']['modes'][m]]
    print('  ', unchanged)


if __name__ == '__main__':
    main()
