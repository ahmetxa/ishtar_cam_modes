#!/usr/bin/env python3
"""
IMX989 LN2/LN4 cok-modlu uygulayici  (ishtar / Xiaomi 13 Ultra)

Orijinal mod LN yamasini YALNIZ sensor modu 1'e koyuyor ve devreye girmesi icin
vendor.debug.camera.overrideForceSensorMode = 1 gerekiyor. O CamX ayari KURESEL
oldugu icin bu ROM'un cok kamerali oturumunu cokertiyor.

Bu arac ayni yamayi istenen TUM modlara uygular; boylece kamera hangi modu
secerse secsin LN devreye girer ve property'e hic gerek kalmaz.

Register anlamlari (regSetting blobundan cozuldu):
  0x0112/0x0113  cikis formati   0x0A0A = RAW10, 0x0C0C = RAW12
  0x0342/0x0343  LINE_LENGTH_PCK
  0x31A4         LN modu secici  0 = kapali, 1 = LN2, 2 = LN4

regSetting blobu 40 bayt/kayit:
  [0] slaveAddr degeri   [1] deger girdisinin tablo indisi   [2] REGISTER ADRESI
  [3] adres tipi         [4] delayUs girdisi                 [5] veri tipi
  [6] islem              [7] gecikme                         [9] sonraki girdi

Dosya bicimi icin bkz. port_sensor_mod.py
"""
import struct, zlib, sys, os, hashlib

TBL0, ENTSZ = 0xD0, 60
OFF_SZ, OFF_DB, OFF_DL = 0x1C, 0xB8, 0xBC

REG_FMT_HI, REG_FMT_LO = 0x0112, 0x0113
REG_LLP_HI, REG_LLP_LO = 0x0342, 0x0343
REG_LN_SEL = 0x31A4

LN_SEL_VALUE = {2: 1, 4: 2}      # 0x31A4 register degeri: LN2 -> 1, LN4 -> 2
LLP_MIN = {2: 19264, 4: 35488}   # LN2 / LN4 icin gereken en kucuk satir uzunlugu
FLL_MIN = 3200                   # resolutionData icindeki asgari kare uzunlugu

WHITE_OFF = 524                  # sensorDriverData icinde, u32
BLACK_OFFS = (528, 532, 536, 540)


class Bin(object):
    def __init__(self, path):
        self.buf = bytearray(open(path, 'rb').read())
        if self.buf[:20] != b'QTI Chromatix Header':
            raise ValueError('QTI Chromatix Header imzasi yok')
        if struct.unpack_from('<I', self.buf, OFF_SZ)[0] != len(self.buf) - 4:
            raise ValueError('0x1C boyut alani tutmuyor')
        if struct.pack('<I', zlib.crc32(bytes(self.buf[:-4])) & 0xffffffff) != bytes(self.buf[-4:]):
            raise ValueError('CRC32 tutmuyor')
        self.base = struct.unpack_from('<I', self.buf, OFF_DB)[0]
        self.dlen = struct.unpack_from('<I', self.buf, OFF_DL)[0]
        self.ents = []
        off = TBL0
        while off + ENTSZ <= len(self.buf):
            nm = bytes(self.buf[off:off + 44]).split(b'\0')[0]
            if not nm or not all(32 <= c < 127 for c in nm):
                break
            o, s, i, n = struct.unpack_from('<4I', self.buf, off + 44)
            self.ents.append([nm.decode(), o, s, i, n, off])
            off += ENTSZ

    def name(self, k):
        return self.ents[k][0]

    def eoff(self, k):
        return self.ents[k][1]

    def esize(self, k):
        return self.ents[k][2]

    def data(self, k):
        o, s = self.ents[k][1], self.ents[k][2]
        return bytes(self.buf[self.base + o:self.base + o + s])

    def u32(self, k):
        d = self.data(k)
        return struct.unpack('<I', d)[0] if len(d) == 4 else None

    def by_name(self, nm):
        return [k for k, e in enumerate(self.ents) if e[0] == nm]

    def _owners(self, lo, hi):
        out = []
        for k, e in enumerate(self.ents):
            o, s = e[1], e[2]
            if s and o < hi and o + s > lo:
                out.append(k)
        return out

    def write_data(self, rel, raw, owner):
        """Veri bolgesine dogrudan yaz -- yalnizca 'owner' girdisi kapsiyorsa."""
        extra = [k for k in self._owners(rel, rel + len(raw)) if k != owner]
        if extra:
            raise RuntimeError('rel%d baska girdiler de kapsiyor: %s'
                               % (rel, [(k, self.name(k)) for k in extra[:5]]))
        self.buf[self.base + rel:self.base + rel + len(raw)] = raw

    def _index_values(self):
        if hasattr(self, '_vidx'):
            return self._vidx
        idx = {}
        d = bytes(self.buf[self.base:self.base + self.dlen])
        for i in range(len(d) - 3):
            v = d[i] | (d[i + 1] << 8) | (d[i + 2] << 16) | (d[i + 3] << 24)
            if v <= 0xFFFF and v not in idx:
                idx[v] = i
        self._vidx = idx
        return idx

    def set_entry_value(self, k, value):
        """4 baytlik girdinin degerini ofset yonlendirerek degistir.
           Veri bolgesine hic bayt yazilmaz -> paylasilan degerler bozulmaz."""
        if self.esize(k) != 4:
            raise RuntimeError('#%d boyutu 4 degil' % k)
        if self.u32(k) == value:
            return False
        idx = self._index_values()
        if value not in idx:
            raise RuntimeError('veri bolgesinde 0x%08X degeri bulunamadi' % value)
        struct.pack_into('<I', self.buf, self.ents[k][5] + 44, idx[value])
        self.ents[k][1] = idx[value]
        return True

    def seal(self):
        struct.pack_into('<I', self.buf, OFF_SZ, len(self.buf) - 4)
        self.buf[-4:] = struct.pack('<I', zlib.crc32(bytes(self.buf[:-4])) & 0xffffffff)
        return bytes(self.buf)


class Sensor(Bin):
    def __init__(self, path):
        Bin.__init__(self, path)
        self.sc = self.by_name('streamConfiguration')
        self.rd = self.by_name('resolutionData')[0]
        self.nmodes = len(self.sc)
        self.RECSZ = self.esize(self.rd) // self.nmodes
        # Mod -> regSetting baglantisi resolutionData'nin kendi isaretcisinden
        # okunur (alan 31); girdi listesinin sirasina guvenilmez.
        self.rs = [self.res_field(m, 31) for m in range(self.nmodes)]
        for m, k in enumerate(self.rs):
            if self.name(k) != 'regSetting':
                raise ValueError('mod %d -> #%d regSetting degil (%s)'
                                 % (m, k, self.name(k)))
        # Mod -> streamConfiguration baglantisi da ayni sekilde dogrulanir (alan 5)
        for m in range(self.nmodes):
            if self.res_field(m, 5) != self.sc[m]:
                raise ValueError('mod %d streamConfiguration baglantisi tutmuyor: '
                                 '%d != %d' % (m, self.res_field(m, 5), self.sc[m]))

    def regs(self, m):
        """mod m icin {register_adresi: (kayit_no, deger_girdisi)}"""
        d = self.data(self.rs[m])
        out = {}
        for r in range(0, len(d), 40):
            f = struct.unpack_from('<10I', d, r)
            out[f[2]] = (r // 40, f[1])
        return out

    def res_field(self, m, i):
        rel = self.eoff(self.rd) + m * self.RECSZ + i * 4
        return struct.unpack_from('<I', self.buf, self.base + rel)[0]

    def set_res_field(self, m, i, v):
        rel = self.eoff(self.rd) + m * self.RECSZ + i * 4
        self.write_data(rel, struct.pack('<I', v), self.rd)

    def stream0(self, m):
        o = self.eoff(self.sc[m])
        dt = struct.unpack_from('<I', self.buf, self.base + o + 8)[0]
        bpp = struct.unpack_from('<I', self.buf, self.base + o + 28)[0]
        return o + 8, o + 28, dt, bpp

    def apply_ln(self, mode, ln, twelve_bit):
        R = self.regs(mode)
        for a in (REG_FMT_HI, REG_FMT_LO, REG_LLP_HI, REG_LLP_LO, REG_LN_SEL):
            if a not in R:
                return 'ATLANDI (reg 0x%04X yok)' % a
        ksel = R[REG_LN_SEL][1]
        if ln is not None and self.u32(ksel) != 0:
            return 'ATLANDI (0x31A4 zaten %d)' % self.u32(ksel)
        khi, klo = R[REG_LLP_HI][1], R[REG_LLP_LO][1]
        llp_cur = (self.u32(khi) << 8) | self.u32(klo)
        if self.res_field(mode, 12) != llp_cur:
            return 'ATLANDI (resolutionData llp %d != register %d)' % (
                self.res_field(mode, 12), llp_cur)
        if twelve_bit:
            for a in (REG_FMT_HI, REG_FMT_LO):
                if self.u32(R[a][1]) != 0x0A:
                    return 'ATLANDI (reg 0x%04X = 0x%02X)' % (a, self.u32(R[a][1]))
            dtr, bppr, dt, bpp = self.stream0(mode)
            if dt != 0x2B or bpp != 10:
                return 'ATLANDI (akis dt=0x%02X bpp=%d)' % (dt, bpp)

        acts = []
        if ln is None:
            # LN yok. Yine de RAW12 akisinin MIPI'ye sigmasi icin satir uzunlugu
            # 12/10 orasinda buyutulmeli; buyutulmezse akis hic gelmiyor
            # (onizleme siyah kaliyor) -- cihazda dogrulandi.
            llp_new = ((llp_cur * 12 // 10) + 15) // 16 * 16 if twelve_bit else llp_cur
            acts.append('LN kapali, yalniz format')
        else:
            self.set_entry_value(ksel, LN_SEL_VALUE[ln])
            acts.append('0x31A4=%d' % LN_SEL_VALUE[ln])
            llp_new = max(llp_cur, LLP_MIN[ln])
        if llp_new != llp_cur:
            self.set_entry_value(khi, (llp_new >> 8) & 0xFF)
            self.set_entry_value(klo, llp_new & 0xFF)
            self.set_res_field(mode, 12, llp_new)
            acts.append('llp %d->%d' % (llp_cur, llp_new))
        else:
            acts.append('llp %d (yeterli)' % llp_cur)
        fll = self.res_field(mode, 13)
        if fll > FLL_MIN:
            self.set_res_field(mode, 13, FLL_MIN)
            acts.append('fll %d->%d' % (fll, FLL_MIN))
        if twelve_bit:
            self.set_entry_value(R[REG_FMT_HI][1], 0x0C)
            self.set_entry_value(R[REG_FMT_LO][1], 0x0C)
            dtr, bppr, dt, bpp = self.stream0(mode)
            self.write_data(dtr, struct.pack('<I', 0x2C), self.sc[mode])
            self.write_data(bppr, struct.pack('<I', 12), self.sc[mode])
            acts.append('RAW10->RAW12')
        return ', '.join(acts)

    def set_levels(self, white, black):
        sdd = self.by_name('sensorDriverData')[0]
        self.write_data(self.eoff(sdd) + WHITE_OFF, struct.pack('<I', white), sdd)
        for b in BLACK_OFFS:
            self.write_data(self.eoff(sdd) + b, struct.pack('<I', black), sdd)
        return 'whiteLevel=%d blackLevel=%d' % (white, black)


# 4096x3072 / 4096x2304 / 3360x2520 -- fotograf cekiminde kullanilabilecek modlar.
# 0 (50MP), 5/6/18/19 (SHDR video), 8 (8K), 9/22 (yuksek fps), 11 disarida.
FOTO_MODLARI = [1, 2, 3, 4, 7, 10, 12, 13, 14, 15, 16, 17, 20, 21]

VARIANTS = [
    # ad      LN  12bit  kuresel_seviye  modlar
    ('ln2s',  2,  False, False, FOTO_MODLARI),
    ('ln4s',  4,  False, False, FOTO_MODLARI),
    ('ln2f',  2,  True,  True,  FOTO_MODLARI),
    ('ln4f',  4,  True,  True,  FOTO_MODLARI),
    # LN yok, yalnizca 12-bit cikis: kazancin LN'den mi bit derinliginden mi
    # geldigini ayirt etmek icin. Zamanlamaya hic dokunmaz.
    ('r12',   None, True, True,  FOTO_MODLARI),
]


def main(src, outdir):
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    for name, ln, tb, lev, modes in VARIANTS:
        s = Sensor(src)
        print('=== %s ===  %s, %s cikis, %s' % (
            name, ('LN%d' % ln) if ln else 'LN yok', '12-bit' if tb else '10-bit',
            'kuresel seviye 4095/256' if lev else 'kuresel seviye SABIT (1023/64)'))
        ok = 0
        for m in modes:
            r = s.apply_ln(m, ln, tb)
            if not r.startswith('ATLANDI'):
                ok += 1
            print('   mod %-3d %s' % (m, r))
        if lev:
            print('   kuresel  %s' % s.set_levels(4095, 256))
        out = s.seal()
        p = os.path.join(outdir, name + '.bin')
        open(p, 'wb').write(out)
        print('   -> %s  %d mod yamalandi  %d bayt  md5 %s  crc32 %08x\n'
              % (name + '.bin', ok, len(out), hashlib.md5(out).hexdigest(),
                 struct.unpack('<I', out[-4:])[0]))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
