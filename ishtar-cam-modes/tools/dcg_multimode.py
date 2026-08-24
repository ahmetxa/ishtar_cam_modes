#!/usr/bin/env python3
"""
IMX989 DCG (Dual Conversion Gain) cok-modlu tasiyicisi  (ishtar / Xiaomi 13 Ultra)

Orijinal mod DCG'yi sensor modu 3 ve 14'e koyuyor ve devreye girmesi icin
vendor.debug.camera.overrideForceSensorMode = 14 gerekiyor. O CamX ayari
KURESEL oldugu icin tek moda zorlamak kirilgan; bunun yerine yamayi
uyumlu TUM modlara uyguluyoruz (bkz. ln_multimode.py, ayni yaklasim).

Referans yama mod 14'ten cikarilir ve hedef modlara ADRES eslesmesiyle
uygulanir -- kayit indisleri modlar arasinda farkli olabiliyor.

DCG yamasi LN'den iki yonuyle ayriliyor:
  * Bazi kayitlarda REGISTER ADRESI de degisiyor
    (0x0220->0xFFFF, 0x0221->0x32F0, 0x0222->0x32F1)
  * Kuresel blokta yalniz whiteLevel degisiyor (1023 -> 16383);
    blackLevel 64 olarak KALIYOR.

Orijinal modda bulunan hata (burada tekrarlanmiyor):
  mod 3'un register'lari yamalanirken resolutionData'da mod 2'nin
  llp/fll'i degistirilmis -> mod 2'nin zamanlamasi bozuluyor, mod 3
  tutarsiz kaliyor.

Dosya bicimi icin bkz. port_sensor_mod.py
"""
import struct, sys, os, hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ln_multimode import Sensor, FOTO_MODLARI   # noqa: E402

MODDIR_DEFAULT = '13U-989-DCG16+LN2+LN4'
BINNAME = 'com.qti.sensormodule.ishtar_semco_imx989_wide.bin'
REF_MODE = 14                     # referans yamanin cikarildigi mod

WHITE_DCG = 16383                 # 14-bit; blackLevel'a DOKUNULMUYOR
DT_RAW14, BPP_RAW14 = 0x2D, 14    # streamConfiguration akis 0 hedefi
DT_RAW10, BPP_RAW10 = 0x2B, 10
RES_LLP_DCG = 52400               # orijinal modun mod 14 icin yazdigi deger
FLL_MIN = 3200


class DcgSensor(Sensor):
    def records(self, m):
        """[(kayit_no, adres, deger_girdisi, deger)] """
        blob = self.data(self.rs[m])
        out = []
        for r in range(0, len(blob), 40):
            f = struct.unpack_from('<10I', blob, r)
            out.append((r // 40, f[2], f[1], self.u32(f[1])))
        return out

    def addr_index(self, m):
        """adres -> kayit; ayni adres birden fazla ise None"""
        idx = {}
        for rec in self.records(m):
            idx[rec[1]] = None if rec[1] in idx else rec
        return idx

    def set_reg_addr(self, m, recno, addr):
        rel = self.eoff(self.rs[m]) + recno * 40 + 8
        self.write_data(rel, struct.pack('<I', addr), self.rs[m])


def extract(moddir):
    """Referans (disable, enable) ciftinden mod 14 yamasini cikar."""
    off = DcgSensor(os.path.join(moddir, 'dcg', 'disable', BINNAME))
    on = DcgSensor(os.path.join(moddir, 'dcg', 'enable', BINNAME))
    a, b = off.records(REF_MODE), on.records(REF_MODE)
    if len(a) != len(b):
        raise ValueError('referans ciftinde kayit sayisi farkli')
    patch = []
    for x, y in zip(a, b):
        if x[1] != y[1] or x[3] != y[3]:
            patch.append({'old_addr': x[1], 'old_val': x[3],
                          'new_addr': y[1], 'new_val': y[3]})
    llp_reg_new = None
    for p in patch:
        if p['old_addr'] == 0x0342:
            hi = p['new_val']
        if p['old_addr'] == 0x0343:
            lo = p['new_val']
    llp_reg_new = (hi << 8) | lo
    return patch, llp_reg_new


def check(s, m, patch):
    """Hedef mod bu yamayi kaldirabiliyor mu?"""
    idx = s.addr_index(m)
    problems = []
    for p in patch:
        rec = idx.get(p['old_addr'])
        if rec is None:
            problems.append('0x%04X yok/tekil degil' % p['old_addr'])
        elif rec[3] != p['old_val']:
            problems.append('0x%04X=%s (beklenen %s)' % (p['old_addr'], rec[3], p['old_val']))
        elif s.esize(rec[2]) != 4:
            problems.append('0x%04X deger girdisi 4 bayt degil' % p['old_addr'])
    _, _, dt, bpp = s.stream0(m)
    if (dt, bpp) != (DT_RAW10, BPP_RAW10):
        problems.append('akis dt=0x%02X bpp=%d (RAW10 bekleniyor)' % (dt, bpp))
    return problems


def apply_dcg(s, m, patch, llp_reg_new, bits=14, group=None):
    bad = check(s, m, patch)
    if bad:
        return 'ATLANDI (%s)' % '; '.join(bad[:3])
    dt_new, bpp_new = (DT_RAW14, BPP_RAW14) if bits == 14 else (0x2C, 12)
    idx = s.addr_index(m)
    naddr = 0
    npatch = 0
    for p in patch:
        if group is not None and p['old_addr'] not in group:
            continue
        npatch += 1
        rec = idx[p['old_addr']]
        v = p['new_val']
        # cikis formati register'lari istenen bit derinligine cekilir
        if p['old_addr'] in (0x0112, 0x0113):
            v = bits
        s.set_entry_value(rec[2], v)
        if p['new_addr'] != p['old_addr']:
            s.set_reg_addr(m, rec[0], p['new_addr'])
            naddr += 1
    dtr, bppr, _, _ = s.stream0(m)
    s.write_data(dtr, struct.pack('<I', dt_new), s.sc[m])
    s.write_data(bppr, struct.pack('<I', bpp_new), s.sc[m])
    acts = ['%d/%d register' % (npatch, len(patch)), 'RAW10->RAW%d' % bits]
    if naddr:
        acts.append('%d adres yonlendirme' % naddr)
    llp_old = s.res_field(m, 12)
    s.set_res_field(m, 12, RES_LLP_DCG)
    acts.append('llp %d->%d (reg %d)' % (llp_old, RES_LLP_DCG, llp_reg_new))
    fll = s.res_field(m, 13)
    if fll > FLL_MIN:
        s.set_res_field(m, 13, FLL_MIN)
        acts.append('fll %d->%d' % (fll, FLL_MIN))
    return ', '.join(acts)


# --- register gruplari: yesil goruntunun kaynagini daraltmak icin ---
G_CORE = {0x321C, 0x0112, 0x0113, 0x0342, 0x0343}       # DCG secici + format + satir uzunlugu
G_PLL = {0x0307, 0x030D, 0x030E, 0x030F}                 # PLL carpan/bolucu
G_VENDOR = {0x3805, 0x3891, 0x3895, 0x3897, 0x389B,      # satici zamanlama
            0x38B8, 0x38B9, 0x3170, 0x3172,
            0xB805, 0xB83D, 0xB875}
G_HDR = {0x0220, 0x0221, 0x0222}                         # SMIA HDR modu (adres yonlendirmeli)
G_ALL = G_CORE | G_PLL | G_VENDOR | G_HDR

# ad, bit derinligi, whiteLevel, blackLevel (None = dokunma), register grubu
VARIANTS = [
    ('dcgf',  14, 16383, None, G_ALL),                   # orijinal modun birebir dengi
    ('dcg12', 12,  4095,  256, G_ALL),                   # RAW14 yerine RAW12
    ('dcgA',  12,  4095,  256, G_CORE),                  # yalniz cekirdek
    ('dcgB',  12,  4095,  256, G_CORE | G_PLL),          # cekirdek + PLL
    ('dcgC',  12,  4095,  256, G_CORE | G_PLL | G_VENDOR),  # HDR adres yonlendirmesi haric
]


def main(src, outdir, moddir):
    patch, llp_reg_new = extract(moddir)
    print('referans mod %d yamasi: %d kayit, register llp -> %d'
          % (REF_MODE, len(patch), llp_reg_new))
    for name, bits, white, black, group in VARIANTS:
        s = DcgSensor(src)
        print('\n=== %s ===  DCG, %d-bit cikis, whiteLevel %d, blackLevel %s'
              % (name, bits, white, black if black else 'degismiyor'))
        ok = []
        for m in FOTO_MODLARI:
            r = apply_dcg(s, m, patch, llp_reg_new, bits, group)
            if not r.startswith('ATLANDI'):
                ok.append(m)
        print('   yamalanan modlar: %s' % ok)
        sdd = s.by_name('sensorDriverData')[0]
        s.write_data(s.eoff(sdd) + 524, struct.pack('<I', white), sdd)
        if black is not None:
            for o in (528, 532, 536, 540):
                s.write_data(s.eoff(sdd) + o, struct.pack('<I', black), sdd)
        out = s.seal()
        open(os.path.join(outdir, name + '.bin'), 'wb').write(out)
        print('   -> %s.bin  %d bayt  md5 %s  crc32 %08x'
              % (name, len(out), hashlib.md5(out).hexdigest(),
                 struct.unpack('<I', out[-4:])[0]))
        if not ok:
            print('   UYARI: hicbir mod yamalanamadi')


if __name__ == '__main__':
    src, outdir = sys.argv[1], sys.argv[2]
    moddir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(src)))), MODDIR_DEFAULT)
    main(src, outdir, moddir)
