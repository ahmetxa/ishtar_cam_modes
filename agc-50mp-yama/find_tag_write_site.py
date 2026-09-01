#!/usr/bin/env python3
"""camera.qcom.so icinde bir metadata tag'inin YAZIM yerini bulur.

Faz 3.2 (IMPL-18) bu betikle `android.sensor.info.pixelArraySize` (tag f0006)
yazim yerini buldu. Betik saklaniyor cunku Project-Comprehension'daki EV-24,
EV-25 ve EV-26 kanit satirlari yeniden dogrulanabilir olmali.

Bulgu ozeti (stock HAL c3fa63a86ee3ecaf9fbf02005d35f6b5, 27.268.688 B):
  - Ontolojide f0006 icin kayitli DOKUZ movz/movk adresi YANLIS POZITIF.
  - ALTI rodata dword'u gercek ama deger kaynagi degil; tag listesi tablosu.
  - Gercek yazim: S = [x24+0x60], deger S+0x3c1c (veya [S+0x3d84]==1 ise
    S+0x3db4) adresinden [x19+0x6550] yuvasina kopyalanir, sonra
    bl 0x0166648c ile publisher 0x1755430 uzerinden count=2 yayinlanir.
  - Deger CALISMA ANINDA turetilir; ikilide sabit degildir.

Kullanim:
    python find_tag_write_site.py <camera.qcom.so> [tag_hex]
    python find_tag_write_site.py hal.so f0006

Gereksinim: capstone, pyelftools  (bkz. docs/reverse-engineering-toolchain.md)

DIKKAT: Bu betik salt-okunurdur. Hicbir yama uygulamaz.
"""
import struct
import sys

from capstone import CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN, Cs
from elftools.elf.elffile import ELFFile

# ARM64 genis-tasima kodlamalari: Rd=bit0-4, imm16=bit5-20, hw=bit21-22
WIDE = {0x52800000: ("movz", 0), 0x72800000: ("movk", 0),
        0xD2800000: ("movz", 1), 0xF2800000: ("movk", 1)}


def decode_wide(word):
    """Genis-tasima komutunu (movz/movk) coz; degilse None."""
    kind = WIDE.get(word & 0xFF800000)
    if kind is None:
        return None
    return kind[0], kind[1], (word >> 21) & 3, (word >> 5) & 0xFFFF, word & 0x1F


def sections(path):
    """.text ve .rodata icin (adres, offset, boyut) dondur.

    Bu ikilide dosya offset'i ile sanal adres .text ve .rodata icin ESITTIR;
    yalnizca .data/.bss 0x1000 fark tasir. Fark cikarsa uyarilir.
    """
    out = {}
    with open(path, "rb") as fh:
        elf = ELFFile(fh)
        for sec in elf.iter_sections():
            if sec.name in (".text", ".rodata"):
                addr, off = sec["sh_addr"], sec["sh_offset"]
                if addr != off:
                    print("UYARI: %s icin adres != offset (delta 0x%x)"
                          % (sec.name, addr - off))
                out[sec.name] = (addr, off, sec["sh_size"])
    return out


def scan_rodata_dwords(data, tag):
    """Dosyadaki 4-bayt hizali tum `tag` dword'lerini bul (tam kapsam)."""
    return [off for off in range(0, len(data) - 3, 4)
            if struct.unpack_from("<I", data, off)[0] == tag]


def scan_register_built(data, text, tag):
    """Registera `tag` yukleyen gercek movz+movk ciftlerini bul.

    f0006 gibi degerler ORR-immediate bitmask olarak kodlanamaz, bu yuzden
    movz(alt 16 bit) + movk(ust 16 bit, lsl #16) tek gecerli bicimdir.
    """
    lo, hi = tag & 0xFFFF, (tag >> 16) & 0xFFFF
    start, _, size = text
    pairs = []
    for off in range(start, start + size - 3, 4):
        dec = decode_wide(struct.unpack_from("<I", data, off)[0])
        if not dec or dec[0] != "movk" or dec[2] != 1 or dec[3] != hi:
            continue
        rd = dec[4]
        for back in range(1, 9):  # movz ile movk arasina komut serpistirilebilir
            prev = decode_wide(struct.unpack_from("<I", data, off - back * 4)[0])
            if prev and prev[0] == "movz" and prev[2] == 0 \
                    and prev[3] == lo and prev[4] == rd:
                pairs.append((off - back * 4, off, rd))
                break
    return pairs


def resolve_adrp_add(data, text):
    """Her adrp+add ciftinin hedef adresini coz -> {hedef: [komut adresleri]}."""
    start, _, size = text
    base, out = {}, {}
    for off in range(start, start + size - 3, 4):
        word = struct.unpack_from("<I", data, off)[0]
        if (word & 0x9F000000) == 0x90000000:  # ADRP
            imm = (((word >> 5) & 0x7FFFF) << 2) | ((word >> 29) & 3)
            if imm & (1 << 20):
                imm -= 1 << 21
            base[word & 0x1F] = (off & ~0xFFF) + imm * 0x1000
        elif (word & 0xFFC00000) == 0x91000000:  # ADD (imm, 64-bit, shift 0)
            rn = (word >> 5) & 0x1F
            if rn in base:
                out.setdefault(base[rn] + ((word >> 10) & 0xFFF), []).append(off)
    return out


def main():
    path = sys.argv[1]
    tag = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0xF0006
    data = open(path, "rb").read()
    secs = sections(path)
    text = secs[".text"]
    md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)

    print("ikili: %s  (%d bayt)" % (path, len(data)))
    print("tag  : 0x%05x\n" % tag)

    dwords = scan_rodata_dwords(data, tag)
    print("== hizali dword olarak tag: %d adet (dosya geneli, tam kapsam) ==" % len(dwords))
    for off in dwords:
        ctx = struct.unpack_from("<4I", data, off - 8)
        print("  0x%08x  komsular: %s" % (off, " ".join("%08x" % v for v in ctx)))

    targets = resolve_adrp_add(data, text)
    exact = [off for off in dwords if targets.get(off)]
    print("\n  bunlardan tam adrp+add ile adreslenen: %d" % len(exact))
    print("  (sifir ise: bu dword'ler tablo ici girdilerdir, deger kaynagi DEGIL)")

    pairs = scan_register_built(data, text, tag)
    print("\n== registera tag kuran gercek movz+movk ciftleri: %d ==" % len(pairs))
    for movz, movk, rd in pairs:
        print("\n  -- movz@0x%08x movk@0x%08x (reg %d) --" % (movz, movk, rd))
        for ins in md.disasm(data[movz - 12 * 4:movk + 12 * 4], movz - 12 * 4):
            mark = ">>" if ins.address in (movz, movk) else "  "
            print("  %s 0x%08x  %-8s %s" % (mark, ins.address, ins.mnemonic, ins.op_str))


if __name__ == "__main__":
    main()
