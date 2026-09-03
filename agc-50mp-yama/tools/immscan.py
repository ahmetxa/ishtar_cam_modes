"""Scan the whole binary for movz/movk instructions carrying a given 16-bit
immediate, and for str/ldr using it. Read-only.

ARM64 wide-move: sf(1) 10 100101 hw(2) imm16(16) Rd(5)
  MOVZ 32-bit = 0x52800000 | hw<<21 | imm16<<5 | Rd
  MOVK 32-bit = 0x72800000 | hw<<21 | imm16<<5 | Rd
  MOVZ 64-bit = 0xD2800000 ; MOVK 64-bit = 0xF2800000

usage: python immscan.py <so> <imm_hex>
"""
import struct
import sys

from elftools.elf.elffile import ELFFile


def loads(path):
    segs = []
    with open(path, "rb") as fh:
        elf = ELFFile(fh)
        for seg in elf.iter_segments():
            if seg["p_type"] == "PT_LOAD" and seg["p_flags"] & 1:  # executable
                segs.append((seg["p_vaddr"], seg["p_offset"], seg["p_filesz"]))
    return segs


def main():
    path = sys.argv[1]
    imm = int(sys.argv[2], 16)
    data = open(path, "rb").read()

    bases = {
        0x52800000: "movz w",
        0x72800000: "movk w",
        0xD2800000: "movz x",
        0xF2800000: "movk x",
    }
    targets = {}
    for base, name in bases.items():
        for hw in range(4):
            targets[base | (hw << 21) | (imm << 5)] = (name, hw)

    print("scanning for immediate 0x%x" % imm)
    hits = []
    for vaddr, off, size in loads(path):
        n = size // 4
        words = struct.unpack_from("<%dI" % n, data, off)
        for i, w in enumerate(words):
            key = w & 0xFFE0_0000 | (w & 0x001F_FFE0)
            if key in targets:
                name, hw = targets[key]
                rd = w & 0x1F
                hits.append((vaddr + i * 4, name, rd, hw))

    print("hits: %d" % len(hits))
    for addr, name, rd, hw in hits[:60]:
        print("  0x%08x  %s%d, #0x%x%s"
              % (addr, name, rd, imm, ", lsl #%d" % (hw * 16) if hw else ""))


if __name__ == "__main__":
    main()
