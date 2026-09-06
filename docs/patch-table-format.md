# Patch Table Format Contract

The format used by `ishtar-cam-modes/blobs/hal-fullres.patch` and
`agc-50mp-yama/hal-raw50-deneme.patch`.

This document is **descriptive**. The authoritative parser is `hal_write` in
`ishtar-cam-modes/halpatch.sh:66-77`; where this document and that function
disagree, the function is right and this document is a bug. Every rule below
was transcribed from the parser and round-tripped against real records.

## 1. Grammar

A table is a line-oriented text file. `hal_write` reads it with
`while read -r idx es ep` and applies three skip conditions:

| # | Rule | Parser site | Effect |
|---|---|---|---|
| 1 | A line whose first field is empty is skipped | `:70` `case "$idx" in '' \| '#'*)` | Blank and whitespace-only lines are ignored |
| 2 | A line whose first field begins with `#` is skipped | `:70`, same `case` | Comment lines are ignored. The `#` must begin the **first field**; a trailing `#` mid-line is not a comment |
| 3 | A line with fewer than three fields is skipped | `:71` `[ -n "$ep" ] \|\| continue` | A two-column record is **silently dropped**, not an error |

Rule 3 is the format's sharpest edge: a truncated record does not fail, it
disappears, and the only symptom is a result md5 that does not match. Any
generator must therefore emit all three columns or none.

A record is:

```
<index> <stock-escape> <patched-escape>
```

Fields are separated by whitespace (`read` default IFS). Because `read`
assigns the unconsumed remainder to the **last** variable, a fourth column
would land inside `$ep` — see §6.

## 2. The index column

The index is a **four-byte unit**, not a byte offset:

```
byte_offset = index * 4
```

`hal_write:74` issues `dd of="$HAL_ACT" bs=4 seek="$idx" count=1 conv=notrunc`.
The rationale is recorded at `halpatch.sh:64-65`: the target is ~27 MB, and
seeking 23 million single bytes with `bs=1` is avoidable when every patch site
is word-aligned anyway.

**The constraint this imposes.** Every patch site must be four-byte aligned and
exactly four bytes wide. This is free for AArch64 instruction patching — every
A64 instruction is a naturally aligned 4-byte word — but the format **cannot
express** a patch to an unaligned field, a 1/2/8-byte datum, or a run longer
than four bytes without splitting it across records. Recognise this before
choosing the format for non-instruction data.

Worked example, record 1 of `hal-fullres.patch`:
index `5963412` → byte offset `23,853,648` (`0x16BBBD0`).

## 3. The escape encoding

Both byte columns hold **ready-made octal escape sequences**, consumed by a
single `printf '%b'` at `hal_write:73`. Four escapes = four bytes, written
little-endian as they appear.

**The measured failure this replaced.** `halpatch.sh:56-62` records it: the
bytes were once produced by nested command substitution,
`printf "\$(printf '%03o' $b)"`. Under toybox `sh` the inner substitution was
**not resolved**, and printf's own literal text was written to the file —
corrupting **288 bytes instead of the intended 16 points**. The current form
uses one `printf '%b'` on an argument that already contains the escapes: no
nesting, and no `%` in the data to be misread as a conversion specifier.

Do not reintroduce nested substitution, and do not switch to `echo -e`
(not portable across the shells this module runs under).

## 4. Round-trip verification

Three records decoded by hand from `hal-fullres.patch`, confirming the grammar
predicts the actual instruction rewrite. All three are
`LDR Wd,[Xn,#0x3d84]` → `MOV Wd,#0`, preserving the destination register —
exactly what the table's own header comment at line 2 claims.

| Line | Index | Stock escapes | LE word | Disassembly | Patched escapes | LE word | Disassembly |
|---|---|---|---|---|---|---|---|
| 12 | 5963412 | `\021\207\175\271` | `0xB97D8711` | `LDR W17,[X24,#0x3d84]` | `\021\000\200\122` | `0x52800011` | `MOV W17,#0` |
| 14 | 5964136 | `\003\207\175\271` | `0xB97D8703` | `LDR W3,[X24,#0x3d84]` | `\003\000\200\122` | `0x52800003` | `MOV W3,#0` |
| 15 | 5964969 | `\221\205\175\271` | `0xB97D8591` | `LDR W17,[X12,#0x3d84]` | `\021\000\200\122` | `0x52800011` | `MOV W17,#0` |

The `imm12` field decodes to `0xF61` = 3937 in all three; scaled by 4 for a
32-bit load that is `0x3D84`, matching the header comment exactly. Line 15
differs from line 12 in its **base** register (X12, not X24) while sharing a
destination — which is why the patched column repeats: the rewrite depends only
on `Rd`.

One record from `hal-raw50-deneme.patch`, confirming the same grammar on the
chained table:

| Line | Index | Stock | LE word | Disassembly | Patched | LE word | Disassembly |
|---|---|---|---|---|---|---|---|
| 25 | 5965367 | `\177\011\000\161` | `0x7100097F` | `CMP W11,#2` | `\177\025\000\161` | `0x7100157F` | `CMP W11,#5` |

`imm12` moves 2 → 5, matching that table's stated intent at its lines 3-5:
widening the accepted format range from `0x22..0x23` to `0x22..0x26`.

## 5. Verification and chaining

Each table records **two** md5 values in its header comments: the binary it
expects as input, and the binary it produces.

| Table | Base (input) md5 | Result (output) md5 |
|---|---|---|
| `ishtar-cam-modes/blobs/hal-fullres.patch` | `c3fa63a86ee3ecaf9fbf02005d35f6b5` (stock) | `fe0245a4720fb07b01d96deef47f5569` (fullres) |
| `agc-50mp-yama/hal-raw50-deneme.patch` | `fe0245a4720fb07b01d96deef47f5569` (fullres) | `8d0915ce520fadaf092d31ed675aa98a` |

**The second table's base is the first table's result.** This is a chain, and a
chain implies a mandatory application order: `hal-raw50-deneme.patch` is
meaningless applied to a stock binary, because its stock column holds the bytes
as they exist *after* the fullres patch. Nothing in `hal_write` enforces the
order — the parser has no notion of a base md5 at all (§7). The ordering is
enforced only by `hal_set:101` refusing to accept a result whose md5 is wrong.

**Where the checks actually run**, in order, on the boot path:

1. `post-fs-data.sh:102` — live `/odm` HAL md5 must equal `HAL_STOCK_MD5`, else nothing is mounted (OTA guard).
2. `hal_seed:109` — re-check the same before copying.
3. `hal_seed:115` — verify the copy after `cat`.
4. `hal_set:95` — skip the write entirely if already in the wanted state.
5. `hal_set:97-99` — re-seed if the copy is `unknown` or `none`.
6. `hal_set:101` — verify the copy's md5 equals the wanted value after writing.

Size is checked before checksum only on the **sensor** path
(`post-fs-data.sh:58-61`); the HAL path relies on a fixed-size in-place write,
so its size cannot change.

## 6. Extension rules

**Compatible** — existing consumers keep working:

- Adding, removing, or reordering records. `hal_write` applies them in file
  order with independent `dd` calls; order is irrelevant because no two records
  in either table overlap. The result md5 **must** be recomputed and the header
  updated.
- Adding comment lines anywhere.
- Changing the escape values of an existing record, with the result md5 updated.

**Breaking** — do not do these without changing the parser first:

- **Adding a fourth column.** `read -r idx es ep` assigns the remainder to
  `$ep`, so column 4 is appended to the patched escape. Today this happens to
  survive because `dd bs=4 count=1` truncates the output to four bytes, but
  that is an accident of the write, not a supported extension. Treat four
  columns as breaking.
- **Emitting a two-column record.** Silently skipped (§1, rule 3).
- **A patch site that is not four-byte aligned or not four bytes wide** (§2).
- **Changing the escape notation** (hex, raw bytes, `\x` form). `printf '%b'`
  understands `\0nnn` octal; other forms are not equivalent across the target
  shells.

## 7. Checksum constants: single source of truth

The stock and fullres md5 values appear in **three** places:

| Location | Role | Read by code? |
|---|---|---|
| `halpatch.sh:32-33` `HAL_STOCK_MD5`, `HAL_FULLRES_MD5` | **Enforcement.** Every guard and verification compares against these. | **Yes** |
| `hal-fullres.patch:9-10` header comments | **Provenance.** Records which binary this table was derived against and what it produces. | No — `hal_write:70` skips `#` lines |
| `customize.sh:37-38` `HAL_STOCK`, `HAL_FULLRES` | Display only; picks the install-time message at `:40-50`. | Yes, but no control flow depends on the value beyond which string is printed |

**Rule.** `halpatch.sh:32-33` is authoritative: it is the only copy with
runtime effect on what gets written or mounted. The table header is **not**
redundant with it and must not be deleted — it answers a different question
("what was this table derived against?"), and it is the copy that travels with
the table when a table is relocated. `customize.sh` is a display mirror.

**Consistency requirement.** A change to either md5 must update all three in
the same commit. There is no automated check for this today; the packaging
assertion specified by Faz 1.2 and the release checklist in Faz 9.2 are where
one belongs.

## 8. The write model and atomicity

**Writes never touch the live binary.** `HAL_ACT` is
`$MODDIR/active_hal/camera.qcom.so` (`halpatch.sh:30`), a module-private copy
seeded from the device's own stock binary. The live
`/odm/lib64/hw/camera.qcom.so` is exposed to the camera stack by a **bind
mount** of that copy (`post-fs-data.sh:127`). Changing modes therefore means
rewriting 16x4 bytes inside an already-mounted inode — the mount is never
touched, the same pattern the sensor layer uses (`post-fs-data.sh:63-64`).

**Atomicity, stated from evidence — this answers `OQ-05`.** Application is
**ordered, not atomic**: `hal_write` issues one `dd conv=notrunc` per record,
so power loss can leave any prefix of the 16 writes applied. This is safe, for
three reasons that must be stated together:

1. **The damage is confined.** The partially written file is the private copy,
   never the live binary. A stock `/odm` binary is still on disk untouched.
2. **The damage is detected.** `hal_state:80-87` md5-classifies the copy and
   returns `unknown` when it matches neither known value. There is no state in
   which a half-patched copy is mistaken for a good one.
3. **The damage is repaired.** `hal_set:97-99` calls `hal_seed` on `unknown` or
   `none`, which re-copies the stock binary from `/odm` and verifies it
   (`:106-116`). `post-fs-data.sh:110-118` does the same on every boot.

`hal_write:76` returns 0 unconditionally and discards `dd`'s stderr, so it
cannot itself report failure — but it has exactly one caller, `hal_set:100`,
which verifies the md5 on the very next line. The safety is provided by the
caller, not by the function's contract; keep it that way, or give `hal_write` a
real return value before adding a second caller.

One ordering constraint is **not** about atomicity and must not be confused
with it: the copy may only be rewritten while the camera services are stopped
(`halpatch.sh:90-91`, sequenced by `setmode.sh:47-91`). `camera.qcom.so` is
mmapped by a running process, and changing its contents underneath one crashes
the stack.

## 9. Location convention

Applies when Faz 4.3 relocates or consolidates tables.

| Kind | Location | Criteria |
|---|---|---|
| **Canonical** | `ishtar-cam-modes/blobs/` | Shipped in the release archive; referenced by `halpatch.sh` through `HAL_PATCH` (`:31`); its result md5 has a named constant in `halpatch.sh`; applied automatically on boot. |
| **Experimental** | `agc-50mp-yama/`, or another workspace directory outside the module | Not shipped — confirmed by `unzip -Z1`, which lists only `blobs/hal-fullres.patch`; no constant in `halpatch.sh`; applied by hand for measurement. |

**The rule.** A table is canonical when, and only when, its result md5 has a
named constant in `halpatch.sh` and `hal_state` can classify it. A table whose
result `hal_state` would report as `unknown` **must not** ship inside
`ishtar-cam-modes/blobs/`, because the boot path treats `unknown` as damage and
re-seeds over it (section 8, point 3). Promoting an experimental table
therefore means adding its constant and its `hal_state` arm in the same change
— not merely moving the file.

Naming: `hal-<capability>.patch` for canonical, `hal-<capability>-deneme.patch`
for experimental, matching what both existing files already do.

### Faz 4.3 outcome, 2026-09-05 (`IMPL-65` / `IMPL-66`)

**Faz 4.3 consolidated nothing, and that is the result rather than an omission.**
The user settled the reading of Main-Planing's "one consolidated table carrying
the broad emission" on 2026-09-05: **broad** means the un-narrowed emission the
shipped `fullres` base already carries, not the `raw50` widening. Under that
reading the consolidated canonical table **is**
`ishtar-cam-modes/blobs/hal-fullres.patch`, unchanged, and no third HAL state is
produced — so `halpatch.sh`'s and `customize.sh`'s two-state classifiers stay
correct and §7's three-copy consistency requirement is untouched.

**Verified by application, not by transcription** (`IMPL-65`). All 16 stock-column
escapes were compared against a stock binary before writing: **0 mismatches**.
Applying the table to `c3fa63a86ee3ecaf9fbf02005d35f6b5` produces
`fe0245a4720fb07b01d96deef47f5569`, **byte-identical** to the live HAL the device
runs and on which Phase 3's result and the Phase 9 claim were measured.

**A convention this established, worth keeping.** Verify the **stock column
against the base binary before writing anything**. The parser cannot do this —
§7 records that it has no notion of a base md5 — and a stock-column mismatch is
the one defect a result md5 detects only *after* the file has been modified. A
pre-write column check turns a chained table applied to the wrong base from a
corrupted output into a refusal. `hal_set:101`'s post-write md5 remains the
enforcement; this is the cheaper check that precedes it.

**`ARC-07` is resolved by this section, not by moving a file.** Project-Comprehension
read "a HAL artifact living in an application-layer directory" as architectural
drift. The rule above says otherwise: the directory follows *canonical versus
experimental*, not *layer*. `hal-raw50-deneme.patch`'s result has no named
constant in `halpatch.sh`, so `hal_state` classifies it `unknown`, and moving it
into `blobs/` would put a table the boot path treats as damage where the boot
path looks — the re-seed in §8 point 3 would run over it. **Moving it was the
unsafe act; leaving it is the correct one.**

**Every experimental table is now marked in place** (`IMPL-66`), per the amended
Phase 4's requirement that superseded experiments be "clearly marked as
experiments rather than deleted": the seven `.patch` files and four `f41-*.tbl`
bisection stages under `agc-50mp-yama/` each carry a `DURUM` header stating
whether they are a live experiment or dead, and why. **The marking is
comment-only and was verified behaviour-neutral** — record lines, per-table match
counts and every applied result md5 are byte-for-byte identical before and after
(§1 rule 2: the parser skips `#` lines). `hal-raw50-deneme.patch`'s marking also
corrects the two claims in its own header that `DEC-14` falsified, rather than
leaving them to be read as current.

## 10. Applicability to sensor blobs

Sensor modes do **not** use this format. They are whole-file replacements:
`blobs/<mode>.bin`, copied over the active file and bind-mounted
(`post-fs-data.sh:53-72`, `setmode.sh:195-197, 252`).

**Their guard is weaker than the HAL path's.** The only pre-write check is a
size comparison against `EXPECT_SIZE=1062250` (`post-fs-data.sh:9,58`;
`setmode.sh:18,197`). There is **no expected-md5 constant for any sensor blob**.
`setmode.sh:258-263` does verify after writing, but it compares the live file
against an md5 it just computed from the source — which proves the copy
succeeded, not that the source was the right file. A corrupted blob of the
correct size passes every check.

**What converting them would require**, stated so the cost is visible and not
paid by accident: nine blobs times the number of differing words. These are
1,062,250-byte register tables, not instruction streams, and their diffs are
large and not word-aligned by construction — section 2's alignment constraint
likely rules the format out. The cheap improvement is not conversion but
**recording a per-blob expected md5** alongside `EXPECT_SIZE`, closing the gap
above at the cost of nine constants. Neither is done here; both are noted for
Faz 9.1 and Faz 9.2.
