"""Disassemble a virtual-address range of camera.qcom.so. Read-only.

usage: python region_dis.py <so> <start_vaddr_hex> <end_vaddr_hex> [grep]
"""
import sys

from capstone import CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN, Cs
from elftools.elf.elffile import ELFFile


def vaddr_to_off(path, vaddr):
    with open(path, "rb") as fh:
        elf = ELFFile(fh)
        for seg in elf.iter_segments():
            if seg["p_type"] != "PT_LOAD":
                continue
            va, fo, fsz = seg["p_vaddr"], seg["p_offset"], seg["p_filesz"]
            if va <= vaddr < va + fsz:
                return fo + (vaddr - va)
    raise SystemExit("vaddr 0x%x not in any PT_LOAD" % vaddr)


def main():
    path = sys.argv[1]
    start = int(sys.argv[2], 16)
    end = int(sys.argv[3], 16)
    needle = sys.argv[4] if len(sys.argv) > 4 else None

    off = vaddr_to_off(path, start)
    n = end - start
    data = open(path, "rb").read()[off:off + n]

    md = Cs(CS_ARCH_ARM64, CS_MODE_LITTLE_ENDIAN)
    for ins in md.disasm(data, start):
        line = "0x%08x  %-10s %s" % (ins.address, ins.mnemonic, ins.op_str)
        if needle is None or needle.lower() in line.lower():
            print(line)


if __name__ == "__main__":
    main()
