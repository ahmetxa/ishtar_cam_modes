# Project Ontology

> Durable project vocabulary and invariants for `ishtar`. Written by ClaudeQB Step 1.5.
> Purpose-built to survive context loss between sessions. Body language: English (default contract).

## 1. Purpose

This project modifies the camera stack of a Xiaomi 13 Ultra (`ishtar`) running AOSPA Android 15, to expose sensor capabilities the stock build does not advertise. The work is reverse engineering against closed vendor binaries, so its most valuable output is **knowledge**: exact addresses, exact tag identifiers, exact invariants, and exactly which hypotheses were tested and rejected.

That knowledge is expensive to reproduce — several findings here cost multi-hour disassembly sessions, and at least two were rediscovered after context loss. This file is the lookup surface. `50MP-Entegrasyon-Plani.md` remains the narrative history; this file is what a future session should read *first*.

Every value below was measured from a device or a binary, not inferred. Where something is unknown, it says so.

## 2. Domain Vocabulary

| Term | Meaning |
|---|---|
| `ishtar` | Xiaomi 13 Ultra, SM8550 (Snapdragon 8 Gen 2), released April 2023. Also the workspace name. |
| `beryl` | AOSPA's Android 16 branch, not a device. `ishtar` is built on it in Phase 7; `calcite` is the later branch. Corrected 2026-09-10: this entry previously read it as a second Xiaomi device. |
| IMX989 | Sony 1-inch main sensor. Physical pixel array 8192x6144 (50.3 MP). |
| QCFA | Quad Colour Filter Array. The sensor's native 2x2 binning arrangement; full resolution requires remosaic. |
| DCG | Dual Conversion Gain. A sensor readout mode; variants `dcgA` and `dcgB`, with `dcgB` measured better on device. |
| LN2 / LN4 | Low-noise binning modes, 2x and 4x. Variants carry `s` (slow) and `f` (fast) suffixes. |
| `stock` | Both a mode name (no modification) and the restore target. Two meanings — keep them distinct in prose. |
| `50mp` | A **mode name**. Enables the HAL layer and forces the sensor layer to stock. |
| `fullres` | The **HAL state** produced by the 16-point patch. Not a mode name. Distinct from `50mp`. |
| Mode | The single runtime state value; one of ten. Stored in `$MODDIR/mode`. |
| Patch table | A plain-text list of `<offset> <stock-escape> <patched-escape>` triples, guarded by md5 comments for both stock input and patched result. |
| Sensor layer | The IMX989 driver `.bin`, bind-mounted over `/odm/lib64/camera/`. Owns DCG/LN/bit-depth. |
| HAL layer | `/odm/lib64/hw/camera.qcom.so`, byte-patched in place. Owns advertised stream configurations. |
| Application layer | The AGC GCam port, patched at smali level. Owns which advertised configuration is selected. |
| AGC | The Google Camera port in use. Version 8.4.300 V9.6 is mandated by the config author. |
| AON | Always-On Sensing. The chain AON → CSS → NCS supplies aperture, OIS, laser AF, and face-scene providers. |
| Tile | A QuickSettings tile. Four exist; they are mutually exclusive. |
| Kitsune | A third-party module layout convention used by the upstream reference modules. |

## 3. Core Entities and Concepts

**Mode** — the central entity. Ten values: `stock`, `dcgA`, `dcgB`, `ln2`, `ln4`, `ln2s`, `ln4s`, `ln2f`, `ln4f`, `50mp`. Single-writer state in one file; read by `setmode.sh`, `action.sh`, the four tiles, and the WebUI. Lifecycle: *selected* → *camera stack stopped* → *layer applied* → *camera stack restarted* → *ready*. The transition is not complete until the camera is genuinely ready (a v1.7 correction).

**Patch table** — a self-verifying description of a binary modification. Two exist:

| File | Entries | Target | Effect |
|---|---|---|---|
| `ishtar-cam-modes/blobs/hal-fullres.patch` | 16 | `camera.qcom.so` | `LDR Wn,[Xm,#0x3d84]` → `MOV Wn,#0`; unlocks 8192x6144 in the standard scaler table |
| `agc-50mp-yama/hal-raw50-deneme.patch` | 4 | `camera.qcom.so` (fullres) | `cmp wN,#2` → `cmp wN,#5`; admits RAW10/RAW12/RAW_OPAQUE at full resolution |

The 27 MB HAL binary is never shipped. The device's own stock blob is patched in place, which is why the md5 guard is load-bearing rather than decorative.

**Sensor blob** — `com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, exactly 1,062,250 bytes. QTI Chromatix format with a `regSetting`/register map and a 23-entry mode table. Nine variants are pre-generated under `blobs/`; the tenth mode, `50mp`, is a HAL layer rather than a sensor blob. Blobs are generated output and are `.gitignore`d — the tools under `ishtar-cam-modes/tools/`, not the binaries, are the tracked artifact.

*Container layout*, re-verified by Faz 5.1 against all nine blobs (`verify_ln.py` asserts the first three on every load):

| Offset | Field |
|---|---|
| `0x00` | `QTI Chromatix Header`, 20 bytes |
| `0x1C` | u32, file size minus 4 |
| `0xB8` | u32, data-region base offset |
| `0xBC` | u32, data-region length |
| `0xD0` | parameter table, 60 B/entry: `name[44]` + `offset` + `size` + `id` + `next`. `offset` is relative to the data base, and 14,455 entries exist. |
| last 4 B | `zlib.crc32(file[:-4])`, little-endian |

*Mode table.* `resolutionData` holds one 304-byte record per mode, 23 records. Field 5 is the mode's `streamConfiguration` entry index, field 12 is LINE_LENGTH_PCK, field 13 is frame length lines, field 31 is the mode's `regSetting` entry index. Both back-links are asserted on load rather than inferred from entry order — entry ordering is *not* mode order (mode 0 uses `regSetting` #46, mode 1 uses #563). `regSetting` is 40 B/record, with `[1]` the value-entry index and `[2]` the register address. A register's value is changed by **redirecting the table entry's offset field**, never by writing into the data region, so shared values cannot be corrupted; the cost is that the desired value must already exist somewhere in the data region.

*Bit-depth encoding*, read from real blobs on 2026-08-31 rather than from the register specification:

| | 10-bit | 12-bit | 14-bit |
|---|---|---|---|
| `0x0112` / `0x0113` | `0x0A` | `0x0C` | `0x0E` |
| `streamConfiguration` +8 (`dt`) | `0x2B` | `0x2C` | `0x2D` |
| `streamConfiguration` +28 (`bpp`) | 10 | 12 | 14 |

The 10-bit and 12-bit columns are measured (`stock` mode 0 and `dcgB` modes 1/14). The 14-bit column is read from `dcg_multimode.py`'s constants, not from a blob — no 14-bit variant is present in `blobs/`.

*White and black levels are global, not per-mode.* They live in `sensorDriverData` at +524 (whiteLevel) and +528/532/536/540 (blackLevel): `stock` carries 1023/64, every DCG and `*f` LN variant carries 4095/256. **This is the mechanism behind invariant 4** — a variant raises the global level to 12-bit while `FOTO_MODLARI` (`ln_multimode.py:235`) deliberately excludes mode 0, so mode 0 keeps emitting 10-bit under a 12-bit white level.

*One hazard for any future per-mode work.* `ln_multimode.apply_ln()` clamps frame length to `FLL_MIN = 3200`. Every mode in `FOTO_MODLARI` is at most 3,072 lines, so the clamp is safe there. Mode 0 is **6,144 lines**; applying that path unmodified would set a frame length shorter than the frame itself. Faz 5.1's `tools/mode0_12bit.py` therefore leaves field 13 untouched.

**Stream configuration** — the framework-visible list of `{format, width, height, direction}` tuples. Emitted by `InitializeScalerStaticCaps`.

**"Camera 3" does not mean what this project used it to mean, and `OQ-17` is now answered (IMPL-12, 2026-08-31).** The Faz 2.1 smoke run measured every HAL camera device on the phone, and the shorthand this project has used does not survive contact with the dump. `dumpsys media.camera` maps framework device 3 to HAL id 9, and HAL id 9 is **Front**-facing with a 3264x2448 pixel array — it cannot be the IMX989. The rear IMX989 array (4096x3072 binned, 8192x6144 physical) sits on HAL id 0 and on ids 2 through 7 and 10. Measured on a stock HAL in mode `dcgB`:

| HAL id | Facing | availableStreamConfigurations | pixelArraySize |
|---|---|---|---|
| 0 | Back | 440 | 4096x3072 |
| 1 | Front | 372 | 3264x2448 |
| 2,3,4,5,6,7 | Back | 500 each | 4096x3072 |
| 8, 9 | Front | 432 each | 3264x2448 |
| 10 | Back | 500 | 4096x3072 |
| 11, 12 | Front | 120 each | 12000x9000 |

None of these is the 508 recorded by `EV-16`, which was measured under a `fullres` HAL, so that comparison was not like-for-like. `scripts/smoke.sh` reports **all thirteen** devices rather than committing to one, and prints full stream rows for the lowest Back-facing id (HAL 0) under an explicitly stated rule.

**`OQ-17` asked which HAL id the 16-point `fullres` patch modifies. The answer is: all thirteen.** IMPL-12 diffed a `fullres` smoke snapshot against the stock baseline. The per-id `availableStreamConfigurations` deltas are:

| HAL id | stock | fullres | delta |
|---|---|---|---|
| 0 | 440 | 456 | +16 |
| 1 (Front) | 372 | 452 | +80 |
| 2–7, 10 | 500 | 508 | +8 each |
| 8, 9 (Front) | 432 | 508 | +76 each |
| 11, 12 (Front) | 120 | 124 | +4 each |

**Front-facing ids move too**, which no document before IMPL-12 anticipated. The patch is not single-id; it edits a shared code path in `InitializeScalerStaticCaps` that every camera id runs. **Faz 4.1 must size its dimension guard for device-wide reach**, not for one id, and cannot state a single target array count as a number. Which id AGC actually opens remains separate and unmeasured — `FIND-2.3-03` records `logicalCameraId 0, cameraId 2` from a failing `configure_streams`, which is a hint, not a determination.

## 4. Module and Boundary Map

| Path | Owns | Depends on |
|---|---|---|
| `ishtar-cam-modes/` | Mode switching, UI, install, boot reapplication | KernelSU, camera framework, both vendor blobs |
| `ishtar-cam-modes/blobs/` | Ten sensor variants + the HAL patch table | — |
| `ishtar-cam-modes/tools/` | Blob generation and verification (Python, host-side) | — |
| `ishtar-cam-modes/tile-app/` | Four QuickSettings tiles + launcher entry (Java) | `action.sh` via the `mode` file |
| `ishtar-cam-modes/webroot/` | KernelSU WebUI, bilingual EN/TR | `action.sh` |
| `ishtar-aon-fix/` | Creates `/vendor/lib64/camera/aon_front.pb` | **Not** KernelSU module mounting — deliberate |
| `agc-50mp-yama/` | AGC smali patches; the experimental HAL table | The AGC APK |
| `device_ishtar/`, `common_sm8550/`, `refs/*` | AOSPA/LOS build inputs | — |
| `android_kernel_*` | Android 15 (`vauxite`, 5.15.178) kernel checkouts, read-only references; not the Android 16 build's kernel (`IMPL-93`) | — |
| `common_sm8550/` | A **device tree** (`AOSPA/android_device_xiaomi_sm8550-common` `vauxite`), not a kernel; corrected 2026-09-13 by `IMPL-93` | — |

**Layer exclusion rule.** `50mp` and the DCG/LN modes are mutually exclusive by decision `Kararlar #1`. Cause: sensor mode 0 (50 MP) is 10-bit, while DCG pulls the global white level to 12-bit; combined, 50 MP output was corrupted. `Kararlar #4` approves attempting to remove this exclusion by moving mode 0 to 12-bit, after everything else is stable.

## 5. Workflows and Lifecycles

**Mode switch.** Requested (tile, WebUI, action button, or `setmode.sh`) → `restart_camera()` → apply layer → verify md5 → write `mode` → notify. The user sees a per-second countdown; completion is signalled only when the camera is genuinely ready.

**Camera stack restart — ordering is an invariant, not a preference.** The correct order runs from client toward HAL:

1. `stop cameraserver`, wait for stopped — the framework closes all sessions itself.
2. `stop vendor.camera-provider` and `vendor.camera-provider-2-7-ext`, wait.
3. Force-stop camera applications, now that no session is open.
4. `start cameraserver`.

Reversing this — killing the provider while a stream is live — leaves the QCOM kernel driver holding CSIPHY/CSID allocations, producing a black preview in **every** mode including stock, recoverable only by reboot. This was a real defect, fixed in v1.6.

**Boot reapplication.** `post-fs-data.sh` reapplies the stored mode; `service.sh` handles late-boot work such as launcher visibility.

**AGC resign and reinstall.** Changing the APK signature requires uninstall. Data is preserved by: `tar` the app data → uninstall → install → untar → `chown -R <new uid>` → `chcon -R "$(stat -c '%C' <parent>)"` → `pm grant` the runtime permissions. Plain `restorecon -R` is **wrong**: it discards the per-app SELinux categories and the app then fails. Reusing the same signer allows later `install -r` without uninstalling.

## 6. Integrations and External Systems

- **KernelSU** — privilege and mounting. `ishtar-aon-fix` deliberately does not depend on module mounting.
- **Android camera framework** — `cameraserver`, `vendor.camera-provider`, `vendor.camera-provider-2-7-ext`. Restarted, never replaced.
- **Vendor blobs** — `/odm/lib64/hw/camera.qcom.so` (27,268,688 bytes) and `/odm/lib64/camera/<sensor>.bin` (1,062,250 bytes). Both guarded by exact size and md5.
- **`adb`** — the only host↔device channel. Vendored under `platform-tools/`.
- **No network integrations of any kind.** No API, no telemetry, no cloud dependency.

### Reverse-engineering address book

Recorded here deliberately: these values are expensive to re-derive and have been lost to context truncation before.

**`camera.qcom.so`, function `InitializeScalerStaticCaps`** — `0x16bf4c0` … `0x16c5a90` (26 KB, 6,516 instructions).

- Emits 16-byte entries `{format, width, height, direction}` into the array at `[x?+0xb10]`.
- Format gate: `sub wN, wFmt, #0x22` ; `cmp wN, #2` ; `b.lo` — admits 0x22 (34) and 0x23 (35). Separate tests admit `#0x36` (54) and `#0x21` (33).
- The four `cmp wN,#2` sites: `0x16c18dc`, `0x16c1c18`, `0x16c22bc`, `0x16c2330`. (Note: `0x16c2334` is the following `b.lo`, not the `cmp` — an earlier transcription error worth not repeating.)
- Changing those four to `cmp wN,#5` admits 0x22–0x26, which adds RAW10 (37), RAW12 (38), and RAW_OPAQUE (36) at 8192x6144. Array grows 508 → 868 int32.
- All 16 `hal-fullres.patch` sites are inside this function; the binary has 55 accesses to `+0x3d84` in total.

**`android.sensor.info.pixelArraySize`, tag `f0006`** — **the write site is LOCATED** (IMPL-18 / Faz 3.2; static analysis against stock HAL `c3fa63a86ee3ecaf9fbf02005d35f6b5`, 27,268,688 B).

*Address convention.* File offset **equals** virtual address for `.text` (`0x004f7000`, size `0x146a538`) and `.rodata` (`0x000280e0`, size `0x3d5d68`); only `.data`/`.bss` carry a `0x1000` delta. Every address below is therefore both.

- **Publisher routine** — `0x1755430`, the CamX static-metadata update call; 668 direct `bl` callers. As used here the arguments are `x0` = metadata context, `w1` = tag, `x2` = value pointer, `w3` = element count, `x4` = the string `camxContext` at `0x001d0090`, `w5` = 0, `w6` = -1.
- **Publishing function** — begins `0x01661f40` (`paciasp`), prologue `stp x29, x30, [sp, #-0x60]!` at `0x01661f44`. Stripped: no symbol covers it, and the nearest preceding `STT_FUNC` (`ChiEntry`, `0x01655750` + `0x144`) does **not** contain it. It publishes the entire `android.sensor.info.*` family in one sequence. **Corrected 2026-09-01 (IMPL-27 / Faz 4.5): the range is `f0000` through `f000a`, not `f0001` through `f000a`.** `f0000` was missed earlier because its tag is built by a *single* `movz w1, #0xf, lsl #16` at `0x01662338` rather than by the `movz`+`movk` pair every other tag uses, so a two-instruction scan does not see it.
- **The `f0006` publication** — `bl` at `0x0166648c` with `w3 = 2` (two int32: width, height). Value pointer `[x19+0x6550]`, built by `add x2, x19, #6, lsl #12` then `add x2, x2, #0x550`. Tag built by `movz w1, #6` at `0x01666468` and `movk w1, #0xf, lsl #16` at `0x01666478`.
- **The value write itself** — `0x0166643c` … `0x01666460`: `ldr x12, [x24, #0x60]` (sensor-data base, call it `S`) ; `mov w5, #0x3c1c` at **`0x01666440`** ; `add x4, x12, x5` ; `ldr w27, [x12, #0x3d84]` (selector) ; `ldr x17, [x4]` ; `str x17, [x19, #0x6550]` at `0x01666454` ; `b.ne` ; `ldr x1, [x4, #0x198]` ; `str x1, [x19, #0x6550]` at `0x01666460`. The published pair is **copied from `S+0x3c1c`, or from `S+0x3db4` when `[S+0x3d84] == 1`**. That selector field `+0x3d84` is the same one recorded above with 55 accesses binary-wide.
- **Second publication path** — `movz` `0x016664b4` / `movk` `0x016664c0`, tail-branching at `0x016664c8` to `0x1662098`; reached when `[[x19+0x68]+0x148] == 5`. Same tag, same count, same `[x19+0x6550]` slot.
- **Third genuine site is a lookup, not a write** — `movz` `0x01668ebc` / `movk` `0x01668ec0` feeding `bl 0x7d12b0` (tag-to-index resolution, 421 callers) inside a per-tag dispatch chain (`f0005` at `0x01668e8c`, `f0008` at `0x01668eec`).
- **Sibling offsets in `S`, same function** — `f0005` (count 2) from `S+0x3dac` (`bl` at `0x016663f8`); `f000a` (count 4) from `S+0x3d88` loaded via `q7` (`bl` at `0x01666588`). `[x19+0x6550]` is a staging slot reused across tags.
- **Origin of the value: RUNTIME-DERIVED from the sensor data structure, not a constant in the binary.** This answers F3.2-04 and is the decisive input to Faz 3.3's patch strategy.

**Two corrections to the earlier `f0006` address book, both established exhaustively (IMPL-18).**

- The **nine recorded `movz`/`movk` addresses are false positives** — not one of them builds `0xf0006`. `0x004fe984` and `0x004fee94` load the division magic constant `0xffe56cb1`; `0x013b192c`, `0x013b1994`, `0x013b1a08`, `0x013b1a7c` load the division magic constant `0xf83f630a`; `0x004ffa5c` builds a 64-bit literal consumed by a `stp`; `0x00d9ae24` and `0x00d9ae80` load hashed keys `0xf18e69c5` and `0xf18f69c5`. Do not spend budget on them again.
- The **six rodata dwords are genuine but are not value sources.** All six do hold `0x000f0006`, and they are the only six 4-byte-aligned dwords in the entire file with that value. But `0x0038964c` and `0x0039c1f0` sit inside strictly sequential tag-list runs (`000f0001` … `000f000a`), `0x0002c6ac` inside a shorter tag run, and `0x003969b4`, `0x00396adc`, `0x00397fcc` inside packed 16-bit tuning data. **No exact `adrp`+`add` pair computes the address of any of the six** — they are table interiors reached by indexing, holding the tag identifier rather than any dimension.
- Genuine register-built `f0006` sites in `.text` number **three**, not nine: the two publication sites and the one lookup site listed above.

**Ranked patch candidates handed to Faz 3.3** (none applied; Faz 3.2 is static by scope):

1. **`0x01666440`, `mov w5, #0x3c1c`** — one word whose `imm16` selects which 8-byte `(width, height)` pair in `S` is published as `pixelArraySize`. If any offset in `S` already holds `8192x6144`, redirecting this immediate publishes it with a genuine single-word change. Requires confirming the layout of `S` on device.
2. **`0x0166645c`, `ldr x1, [x4, #0x198]`** — one word; changes the alternate source offset. Only reachable when `[S+0x3d84] == 1`, so its effect is conditional.
3. **Overwrite the load/store block `0x0166644c` … `0x01666460`** with immediate construction of `0x0000180000002000` (8192, 6144). Multi-word and alters control flow; ranked last.

**Faz 3.3 / IMPL-20 — the layout of `S` is RESOLVED STATICALLY, and it changes the candidate ranking.**

The open design question ("which offset in `S` holds 8192x6144?") is answered without any runtime probe, by tracing the structure's **initializer** rather than its readers. Scanning `.text` for 32-bit accesses at the sibling offsets found a single write region, `0x016f0330` … `0x016f0830`, that populates all of them.

- **The fullres patch is exactly one idea, mechanically confirmed.** All sixteen `hal-fullres.patch` indices decode to `ldr wN, [xM, #0x3d84]` -> `movz wN, #0`; that is, *force the `+0x3d84` selector to zero throughout `InitializeScalerStaticCaps`*. Replaying the shipped table onto stock reproduces `fe0245a4720fb07b01d96deef47f5569` byte-exactly, which independently validates the index convention and the octal-escape decoding.
- **What the selector selects, in `InitializeScalerStaticCaps`** (`0x016bfa50`: `cmp w17,#1` ; `b.ne 0x16bfad4`): when the selector is **1**, one resolution is computed by dividing `[S+0x3dbc]` by `[S+0x3d7c]`; when it is **anything else**, the code walks the sensor mode table at `S+0` with stride `0x240`, count at `S+0x3c18`. Forcing the selector to 0 therefore emits the *whole mode list*, which is why the fullres HAL advertises seven 8192x6144 rows and why it touches all thirteen camera ids.
- **The binning factors are `S+0x3d7c` and `S+0x3d80`**, computed at `0x016f03a4` … `0x016f03bc` as `(int)sqrt([x27+8])` — so a 2x2 bin (`4`) yields `2` — and set to `1` at `0x016f0350` on the unbinned path.
- **`S+0x3dbc` / `S+0x3dc0`** are the *current mode's* active width/height less the four crop values (`str` at `0x016f04d8` and `0x016f0504`).
- **The decisive pair: `S+0x3c1c` / `S+0x3c20` hold the UNBINNED pixel array size, and `S+0x3db4` / `S+0x3db8` hold the BINNED one.** The initializer states the relation directly at `0x016f07c0` … `0x016f07fc`:
  `[S+0x3db4] = [S+0x3c1c] / [x21+0x160]` and `[S+0x3db8] = [S+0x3c20] / [S+0x3d80]`.
  The same block derives `[S+0x3d98]`/`[S+0x3d9c]` from `[S+0x3c54]`/`[S+0x3c58]` and `[S+0x3da0]`/`[S+0x3da4]` from `[S+0x3c5c]`/`[S+0x3c60]` by the same division. Note `0x3c1c + 0x198 = 0x3db4` exactly — candidate 2's displacement is precisely the unbinned-to-binned hop.
- **The live selector is `1`, established by measurement rather than assumed.** `f0006` reads `[4096 3072]`, which is the *binned* pair at `S+0x3db4`. Were the selector anything else, the publisher's default path would already be publishing `S+0x3c1c`. Therefore **`S+0x3c1c` already holds 8192x6144** and the value the project has been searching for is loaded into `x17` at `0x0166644c` on every call, then immediately overwritten by the binned pair.
- **The two publication paths need only one patch.** The second path (`0x016664b0` … `0x016664c8`) rebuilds the same tag and count and passes the *same* `[x19+0x6550]` staging slot to the trampoline at `0x1662098`; it derives no value of its own. Patching the value write therefore satisfies both paths by construction — a refinement of the earlier "a patch must satisfy BOTH paths" warning.

**Revised ranking.** Candidate 1 (`0x01666440`, `mov w5, #0x3c1c`) is **withdrawn**: its immediate already points at the unbinned pair, so changing it moves *away* from the answer. **Candidate 2 is promoted to first and is now determinate rather than conditional:** at `0x0166645c`, change `ldr x1, [x4, #0x198]` (`0xF940CC81`) to `ldr x1, [x4, #0]` (`0xF9400081`), so the selector-is-1 override reloads the unbinned pair instead of the binned one. Four-byte index `5871895`; control flow is untouched. Predicted md5 on a stock base `77083b7c099d4c68a9213476141c450d`, and on a fullres base `c539f04e6bbaedb907a5c987f16800ea`.

**CONFIRMED BY MEASUREMENT (IMPL-20 / Faz 3.3, 2026-09-01). The write site is no longer a hypothesis.**

Patching `0x0166645c` from `ldr x1, [x4, #0x198]` (`0xF940CC81`) to `ldr x1, [x4, #0]` (`0xF9400081`) — one word, four-byte index `5871895`, on a stock base — moved camera 3's `android.sensor.info.pixelArraySize` from `[4096 3072]` to **`[8192 6144]`**, while `activeArraySize` (`f0000`) and `preCorrectionActiveArraySize` (`f000a`) stayed at `[0 0 4096 3072]`. Reverting the same word restored `[4096 3072]` and produced a smoke snapshot byte-identical to the pre-patch one. Evidence: `snapshots/20260901-1055__faz3.3__*`; table: `agc-50mp-yama/hal-pixelarray-deneme.patch`.

This confirms, by measurement rather than inference, that **`S+0x3c1c` holds `8192x6144`** and that the live selector `[S+0x3d84]` is `1`. The whole layout derivation above is therefore validated end to end. Achieved md5 `77083b7c099d4c68a9213476141c450d` matched the prediction committed *before* the run. `CQ-05` is `answered`; the camera stack survived (user-confirmed live preview, empty crash buffer). One attempt consumed; four of fifteen candidate sites spent.

**`android.sensor.info.activeArraySize` `f0000` and `preCorrectionActiveArraySize` `f000a` — both write sites LOCATED** (IMPL-27 / Faz 4.5; static analysis against the same stock HAL `c3fa63a86ee3ecaf9fbf02005d35f6b5`, 27,268,688 B, re-verified by md5 before decoding). Calibration `F4.5-01` passed 5/5 before any address below was derived, and `.text`/`.rodata` offset==addr was re-confirmed on this binary.

- **The `f0000` publication** — `bl` at **`0x0166234c`** with `w3 = 4` (a four-int32 rect). Staging slot `[x19+0x6550]`, built by `add x2, x19, #6, lsl #12` + `add x2, x2, #0x550`. Tag built by the lone `movz w1, #0xf, lsl #16` at `0x01662338`.
- **The `f0000` value fill** — `0x01662290` … `0x016622bc`: `ldr x24, [x24, #0x60]` (`S`) ; `mov w1, #0x3c54` at `0x01662294` ; `ldr w0, [x24, #0x3d84]` (**the same selector**) ; `ldr q3, [x24, x1]` ; `cmp w0, #1` ; `str q3, [x19, #0x6550]` at `0x016622a4` ; `b.ne 0x1662328` at `0x016622a8` ; **`mov w9, #0x3d98` at `0x016622ac`** ; `ldr q4, [x24, x9]` at `0x016622b4` ; `str q4, [x19, #0x6550]` at `0x016622bc`. Published from **`S+0x3c54`, overwritten from `S+0x3d98` when `[S+0x3d84] == 1`**.
- **The `f000a` publication** — `bl` at **`0x01666588`** with `w3 = 4`, same staging slot; tag `movz w1, #0xa` at `0x01666564` + `movk w1, #0xf, lsl #16` at `0x01666574`.
- **The `f000a` value fill** — `0x01666538` … `0x0166655c`: `ldr x26, [x24, #0x60]` ; `mov w11, #0x3c24` at `0x0166653c` ; `ldr w10, [x26, #0x3d84]` ; `ldr q6, [x26, x11]` ; `str q6, [x19, #0x6550]` at `0x0166654c` ; `b.ne 0x1666560` ; **`mov w12, #0x3d88` at `0x01666554`** ; `ldr q7, [x26, x12]` ; `str q7, [x19, #0x6550]` at `0x0166655c`. Published from **`S+0x3c24`, overwritten from `S+0x3d88` when `[S+0x3d84] == 1`**.
- **Correction to the earlier sibling-offsets entry.** The line above recording "`f000a` (count 4) from `S+0x3d88` loaded via `q7`" is accurate but **incomplete in the way that matters**: `S+0x3d88` is the *conditional overwrite*, not the only source. The default is `S+0x3c24`. The same omission would have hidden `f0000`'s `S+0x3c54` entirely.
- **Origin of both rects: RUNTIME-DERIVED, and the unbinned full-resolution rect ALREADY EXISTS in `S`.** Re-derived from the initializer rather than taken from the earlier trace: `ldr w3, [x24, #0x3c54]` → `sdiv w22, w3, w9` → `str w22, [x20, #0x3d98]` (`0x016f077c` … `0x016f07a0`), and `ldr w6, [x16, #0x3c24]` → `sdiv w21, w6, w13` → `str w21, [x13, #0x3d88]` (`0x016f0888` … `0x016f08ac`). The `f0006` pair decodes identically at `0x016f07c0` … `0x016f07e4` and serves as the control. **So the `0x3c`-series offsets hold the unbinned values and the `0x3d`-series hold them divided by the binning factor** — the same relationship whose redirection moved `f0006` to `[8192 6144]`. `F4.5-04`'s question is therefore answered **YES**.
- **Patch candidates, both single-word `movz` immediate redirections** — structurally the same class of change as the confirmed `f0006` patch, and **provably in-bounds**: each makes the conditional `q` load read exactly the 16 bytes the unconditional `q` load in the same basic block already reads.

| tag | address | index (÷4) | stock word | patched word | change |
|---|---|---|---|---|---|
| `f0000` | `0x016622ac` | `5867691` | `0x5287B309` | `0x52878A89` | `mov w9, #0x3d98` -> `mov w9, #0x3c54` |
| `f000a` | `0x01666554` | `5871957` | `0x5287B10C` | `0x5287848C` | `mov w12, #0x3d88` -> `mov w12, #0x3c24` |

**MEASURED, 2026-09-01 (IMPL-28 / `F4.5-07`): the `f0000` patch works, and the pre-committed md5 matched on apply.** Applying the single word at index `5867691` to a stock base (md5 `c3fa63a86ee3ecaf9fbf02005d35f6b5` -> `c8ed89e8fed41e3928396e7f65c8f6ff`, predicted host-side before any device contact) moved `android.sensor.info.activeArraySize` from `[0 0 4096 3072]` to **`[0 0 8192 6144]`** on `camera.hal0` and on `hal2`…`hal7` and `hal10`. Every `streamcfg` count and every `pixelArray` value was unchanged; the bracketed comparable-region diff was exactly thirteen lines.

- **The raise is GLOBAL, not per-sensor (`FIND-4.5-01`, P2, open).** The front cameras moved too — `hal1`, `hal8`, `hal9` went `[0 0 3264 2448]` -> `[0 0 6528 4896]`, exactly 2x — because the patched word sits in the **shared** publishing routine rather than a per-sensor path. `hal11`/`hal12` were unaffected. **Consequence:** the front cameras now advertise an `activeArray` *larger than their own `pixelArray`*, an internally inconsistent pair. The wide camera will not have this once `f0006` is applied alongside. Routed to `Faz4.4`.
- **Raising `f0000` does NOT move `80340003`.** Measured on the same camera in the same state: `f0000` = `[0 0 8192 6144]` while `org.codeaurora.qcamera3.quadra_cfa.activeArraySize` = `[0 0 4096 3072]`. The vendor tag has an independent value source, confirming by measurement what `F4.5-05` established statically.

**MEASURED, 2026-09-01 (IMPL-30 / `F4.5-09`): all three standard tags raised together does NOT fix the image.** Full stack md5 `c094101de0184e9216a57020873bac0b` (pre-committed and matched) with `f0006` `[8192 6144]`, `f0000` `[0 0 8192 6144]`, `f000a` `[0 0 8192 6144]`, `80340003` `[0 0 4096 3072]`. AGC captured **6144x8192 = 50.3 MP** by SOF marker with the libgcam gate clear. **The frame is still unusable.**

- **`FIND-4.5-02` (P1, open): `FIND-3.5-01`'s stated cause is incomplete.** It named three tags; two are now demonstrably raised and the artifact survives, so the active-array tags are not the whole story.
- **The artifact's shape argues against the obvious suspect.** Measured: exactly **75.0%** of the frame is pure black, the left three quarters of the width at full height; content sits in the right quarter as **two vertically stacked strips with different colour casts** (upper red/pink, lower purple/magenta) plus a white edge band. `80340003` is the last unraised tag and `4096x3072` is exactly a quarter of `8192x6144`, which matches the content *fraction* — but a crop to the active array would leave a **rectangle**, not a full-height strip. The doubled, differently-tinted strips look more like a **buffer stride/pitch mismatch with chroma offset against luma**. Neither model is asserted; both need probing.
- **The viewfinder is correct while the still is corrupt**, which confines the fault to the still/RAW consumption path rather than the preview path.
- `IMPL-23` described the earlier artifact as "exactly half the frame black"; this run **measures** 75%. No image from `IMPL-23` survives, so **no regression is claimed** — the discrepancy is recorded rather than resolved.

**Method caveat, learned twice in one session and worth not relearning: `logcat | grep <pattern>` counts your own command.** `adbd` logs each incoming shell request verbatim, so a grep for `CSLAcquireHardwareHW` or `static_metadata.cc:667` matches the `adbd` line containing the search string. This produced a **false provider abort** and a **false libgcam gate failure** in this session, either of which a trusting reader would have recorded as a real result. Always filter: `logcat -d | grep -v adbd | grep <pattern>`, or redirect to a file on device first. Both true counts here were **zero**.

**QTI vendor tag `org.codeaurora.qcamera3.quadra_cfa.activeArraySize` `80340003` — NOT STATICALLY PATCHABLE. Explicit negative, recorded as a result** (`F4.5-05`). The constant `0x80340003` occurs **zero** times as a 4-byte-aligned dword anywhere in the 27 MB file, and is **never** built as a `movz`/`movk` immediate in `.text`. What the binary carries is the *name*: `org.codeaurora.qcamera3.quadra_cfa` at `0x002265af`, exactly once, sitting in a table of vendor **section-name** strings beside `org.codeaurora.qcamera3.bfw` and `com.xiaomi.camera.supportedfeatures`. That is the expected shape — a vendor tag's numeric id is assigned at runtime by the vendor-tag provider from the `0x80000000` base, so **there is no word to patch**. Whether raising `f0000` also moves `80340003` depends on whether `quadra_cfa` reads the same rect in `S`, which static analysis cannot settle; it is a live-measurement question for `F4.5-07`/`F4.5-08`.

**Related metadata tags** — `android.scaler.availableStreamConfigurations` `d000a`; `availableMinFrameDurations` `d000b`; `availableStallDurations` `d000c`; `android.sensor.info.activeArraySize` `f0000`; `preCorrectionActiveArraySize` `f000a`; `android.sensor.info.colorFilterArrangement` `f0002`; and the QTI vendor tag `org.codeaurora.qcamera3.quadra_cfa.activeArraySize` **`80340003`**.

**Three-layer experimental stack, established 2026-09-01 (IMPL-23 / Faz 3.5).** Faz 3.5 needs `hal-fullres.patch` **and** `hal-raw50-deneme.patch` **and** `hal-pixelarray-deneme.patch` applied together — the first time all three have coexisted. The tables share **no index**, and the result is order-independent.

| Stack | md5 | Status |
|---|---|---|
| stock | `c3fa63a86ee3ecaf9fbf02005d35f6b5` | 27,268,688 B |
| stock + fullres | `fe0245a4720fb07b01d96deef47f5569` | calibration, reproduced |
| stock + pixelarray | `77083b7c099d4c68a9213476141c450d` | calibration, reproduced |
| fullres + pixelarray | `c539f04e6bbaedb907a5c987f16800ea` | calibration, reproduced |
| fullres + raw50 | `8d0915ce520fadaf092d31ed675aa98a` | calibration, reproduced — **never calibrated before this run** |
| **fullres + raw50 + pixelarray** | **`c3db54b0b154dd19211f221e3d5046e7`** | pre-committed, matched on apply and on revert |

**Measured tag state under `c3db54b0…`** — `f0006` `[8192 6144]`; `f0000` `[0 0 4096 3072]`; `f000a` `[0 0 4096 3072]`; `80340003` `[0 0 4096 3072]`; `f0002` `BGGR`. `camera.hal0` `streamcfg` 456 -> 800. **The three active-array tags are the outstanding work** — see invariant 6's recorded outcome.

**Format-32 gap, measured.** `hal-raw50-deneme.patch` widens the format test to `0x22..0x26`, i.e. **34–38**. `RAW_SENSOR` is format **32** and is therefore never reached: it stays at `4096x2304` and `4096x3072`, identical to stock, while 33/34/35/36/37/38/54 all gain an 8192x6144 row. **No DNG can be captured at full resolution in this state by any application**, which is what blocks `OQ-02`.

**Vendor tables** — `org.codeaurora.qcamera3.quadra_cfa.availableStreamConfigurations` carries only 33/34/35 at 8192x6144. `xiaomi.scaler.availableStreamConfigurations` already carries `[37 8192 6144 0]`, `[32 8192 6144 0]`, `[36 8192 6144 0]` — the values exist in a vendor table but not in the standard one, which is the whole reason the HAL patch is needed.

**AGC port obfuscation map** (identical in V9.6 and V14) — `Lhvg;` ResolutionSetting; `Llvo;` the hooked characteristics wrapper (the only class overriding `x(I)`); `Llwe;` delegating base; `Lghx;` extends `Llwe;`; `Lmip;->bs()` max of list; `Lmip;->bu()` `Size[]`→`List<Llig;>`; `Lmip;->eU()` blocklist filter; `Lddl;->P/Q` the `blacklisted_resolutions_back/front` lists (**both empty** — a rejected hypothesis); `Llig;->a` width, `->b` height; `Llwp;->a` format, `->b` `Llig;`.

**`LAGC;->Forty8Strip(I)I` is `return p0`** — an identity stub in both builds. The port's 48M mechanism does not exist in this build; the UI's "Redmi K20 Pro / Mi9" note confirms it. A rejected hypothesis, recorded so it is not tested a third time.

**Channel selection** — there is no separate 12 MP / 50 MP channel. `LensSettings.getImageFormatArr()` returns `[pref_raw_key_<lens>]` if set, otherwise `[0x25 RAW10, 0x26 RAW12, 0x20 RAW_SENSOR, 0x23 YUV]`. `AGC.getImageReaderFormat()` takes the first format with a non-empty size list, then `Lmip;->bs()` takes its **maximum** size. AGC therefore already prefers the largest available size; it was stuck at 12.6 MP purely because RAW10's maximum was 4096x3072. Preview uses `Lgsf;->a()`, nearest-to-target, so widening the list does not disturb preview.

**Toolchain** — Temurin JDK 21; smali/baksmali **2.5.2** from the legacy `org/smali` Maven group (`org.jf.*` package names) plus dexlib2, util, guava 31.1-jre, failureaccess, antlr-runtime 3.5.2, jcommander 1.82, ST4; uber-apk-signer 1.3.0; capstone 5.0.7 and pyelftools on any working interpreter. Full procedure with ordered steps and self-checks: `docs/reverse-engineering-toolchain.md`. **Host state corrected 2026-08-30:** a real CPython **3.14.7** is installed (`python`, `py`); `python3` is a Store alias stub and must not be probed as the availability test. The **embeddable** Python 3.12.7 distribution is therefore a fallback for interpreter-less hosts, not a requirement here. `capstone`/`pyelftools` are not yet installed; `java` is absent from PATH, so the Java-path self-check is deferred rather than passed.

**Toolchain negative findings** (each cost real time): apktool's bundled smali `Main` classes are stripped stubs and cannot be invoked; `com.android.tools.smali` Maven paths return 404; the Bitbucket mirror returns 403; google/smali publishes no release binaries; **radare2 and rabin2 5.9.8 do not complete on this 27 MB binary** (no output in 300 s, from either shell).

### The emission sites inside `InitializeScalerStaticCaps` (IMPL-33 / Faz 4.1, 2026-09-02)

**Static analysis on the `fullres` base** `fe0245a4720fb07b01d96deef47f5569`, pulled read-only from `/odm/lib64/hw/camera.qcom.so`. The function disassembles to **6,516 instructions** over `0x16bf4c0` … `0x16c5a90`, which reproduces the recorded count exactly and confirms the bounds independently. All four patch-table indices decode to the recorded stock bytes at the recorded addresses, so the table and the binary confirm each other.

**The four `cmp wN,#2` sites are not four copies of one thing. They are two different arrays.**

| Site | Address | Writes to | Entry | Metric it moves |
|---|---|---|---|---|
| 1 | `0x16c18dc` | `[x?+0xb10]`, stride **16** | `{format, w27, w22, 0}` | `android.scaler.availableStreamConfigurations` |
| 2 | `0x16c1c18` | `[x?+0xb10]`, stride **16** | `{format, w27, w22, 0}` | same |
| 3 | `0x16c22bc` | `[x?+0x6f30]`, stride **32** | four 8-byte fields, one of them `1000000000 / x10` | a **duration** table |
| 4 | `0x16c2330` | `[x?+0x6f48…0x6f60]`, stride **32** | same shape | a **duration** table |

`0x3b9aca00` = 1e9 appears at `0x16c229c`/`0x16c22a0` and is divided by a per-mode value at `0x16c22a4` — a frame duration in nanoseconds. **Only sites 1 and 2 can move the `streamcfg` metric; sites 3 and 4 belong to `availableMinFrameDurations` / `availableStallDurations`, which is Faz 4.2's subject.** This is a live-testable prediction, not yet measured.

**F4.1-02 — the resolution IS reachable at the gate sites.** The emit block at `0x16c1a8c` writes the entry as `stp w0, w27, [x2]` ; `stp w22, wzr, [x2, #8]`, so **`w0` = format, `w27` = width, `w22` = height, `w0`…`w22` all live in registers at the gate**. Site 2's emit block at `0x16c1c30` is identical (`stp w12, w27` ; `stp w22, wzr`). The risk that "the resolution is not reachable at the gate sites, so a guard cannot be placed there" is **retired by measurement**. `w27`/`w22` are also read as divisors at `0x16c1908` and `0x16c1920`, confirming they carry the loop's current resolution rather than a scratch value.

**The gate has TWO predecessors, and a guard must sit where they converge.** Path A falls through `0x16c18d4`; path B is a logging call (`bl 0x19615a8` at `0x16c19e4`, with `w27`, `w22` pushed as varargs) that rejoins by `tbnz w14,#0, #0x16c18d8` at `0x16c1a00`. Path B is taken when `[x3+0x2a]` bit 0 is set **or** `[x25] == 0` — data-dependent, so it is not a cold path and cannot be ignored.

**Four instruction slots before each gate are dead — but only on the `fullres` base.** At site 1, `0x16c18c0` `mov w10,#0` is `hal-fullres.patch` index `5965360`; the next four instructions are `cmp w10,#1` ; `cset w25,ne` ; `orr w14,w25,w19` ; `tbz w14,#0`. With `w10` forced to 0 the `cset` is constant 1, so `w14` bit 0 is always 1 and the `tbz` is never taken. `w25` is redefined at `0x16c1904` and `w14` at `0x16c19fc` before any later read, so both are dead. Site 2 has the same shape at `0x16c1bfc` (index `5965567`), and path B has it at `0x16c19ec` (index `5965435`). **These slots exist because of the fullres patch. A guard built on them is valid on the `fullres` base only and must never be replayed onto stock.**

**F4.1-03 — the guard design, verified by encoding.** `ccmp` takes only a 5-bit immediate, so the 8192 test cannot be a `ccmp`; it must be a real `cmp`, which does reach 8192 as `#2, lsl #12`. That fixes the order: compute the format offset, `cmp` the width, `ccmp` the format range, branch.

| Slot | Instruction | Word | Escape |
|---|---|---|---|
| `0x16c18c8` | `sub  w11, w0, #0x22` | `5100880B` | `\013\210\000\121` |
| `0x16c18cc` | `cmp  w27, #2, lsl #12` | `71400B7F` | `\177\013\100\161` |
| `0x16c18d0` | `ccmp w11, #5, #2, eq` | `7A450962` | `\142\011\105\172` |
| `0x16c18d4` | `b.lo #0x16c1a8c` | `54000DC3` | `\303\015\000\124` |

Every word was round-tripped through capstone at its intended address; the branch offsets resolve to the intended targets. On the `eq` side (width 8192) the `ccmp` compares the format offset against 5, so `b.lo` admits `0x22`…`0x26`. On the `ne` side it forces `nzcv = 2`, i.e. `C = 1`, so `b.lo` is **not** taken and control falls into the untouched stock gate at `0x16c18d8` (`cmp w11,#2`), which keeps `0x22`…`0x23` at every resolution. **The stock `cmp` at `0x16c18dc` is therefore reverted to `#2`; the widening moves into the guarded block.** Path B needs the same four words plus `b #0x16c18d8` (`17FFFFB6`, `\266\377\377\027`) replacing its `tbnz`, and its `b.lo` is `54000483` (`\203\004\000\124`) from `0x16c19fc`.

**Site 2, located and patched live (`IMPL-48`, 2026-09-03).** Site 2 has the same
two-predecessor shape as site 1, which was not previously recorded. Path A falls
through `0x16c1c10`; path B is the logging call at `0x16c1d6c`, rejoining by
`tbnz w15,#0, #0x16c1c14` at `0x16c1d88`. The format register here is `w12`
(`ldr w12,[x21]`), not `w0`, and the range register is `w7`, not `w11` — the
reason a single `cmp w11,#2` word cannot be replayed across all four gate sites.
Dead slots: `0x16c1c04`…`0x16c1c10` on path A, `0x16c1d74`/`0x16c1d7c`…`0x16c1d88`
on path B. **`cset w16, ne` at `0x16c1c08` is dead** because `ldr x16,[sp,#0x1b0]`
at `0x16c1cac` redefines the register four instructions before its only read at
`0x16c1cb0` — this needed checking, since site 2's `cset` target is read later in
the function where site 1's is not.

| Slot | Instruction | Word | Escape |
|---|---|---|---|
| `0x16c1c04` | `sub  w7, w12, #0x22` | `51008987` | ` Q` |
| `0x16c1c08` | `cmp  w27, #2, lsl #12` | `71400B7F` | `@q` |
| `0x16c1c0c` | `ccmp w7, #5, #2, eq` | `7A4508E2` | `âEz` |
| `0x16c1c10` | `b.lo #0x16c1c30` | `54000103` | ` T` |
| `0x16c1d84` | `b.lo #0x16c1c30` | `54FFF563` | `cõÿT` |
| `0x16c1d88` | `b    #0x16c1c14` | `17FFFFA3` | `£ÿÿ` |

**Measured consequence, and it is not confined to `d000a`.** Applying the guard at
both sites moves `android.scaler.availableStreamConfigurationsMaximumResolution`
(`d0014`) from `int32[28]` to `int32[16]`, because the max-res rows are emitted by
the **same loop** through the **same format gate**. Site 1 broad contributes format
37 to `d0014`; site 2 broad contributes 36 and 38. Sites 3 and 4 do not feed it.
See `docs/raw-geometry-diagnosis.md` section 26.

**The design fits the patch-table format.** Every entry is a single 4-byte-aligned word replacement at a stated index, which is exactly what `docs/patch-table-format.md` allows; no instruction is inserted and no control flow is relocated. The table grows from 4 entries to roughly 10 per streamcfg site.

**One consequence to state rather than discover.** The guard compares against the literal 8192, so it narrows **every** camera id to RAW-at-8192x6144. The front cameras (`hal1`, `hal8`, `hal9`, pixel array `[3264 2448]`) have a different full-resolution dimension and would gain no RAW rows at all. That matches Phase 4's stated goal — the QCFA full-resolution dimension only — but it is a behavioural change on ids the project has never targeted, and Faz 4.4's per-camera-id consistency table is where it should be checked.

**Toolchain correction.** The address book records `capstone`/`pyelftools` as "not yet installed". Measured 2026-09-02: **capstone 5.0.7 and pyelftools are both installed** and the disassembly path runs. Also: do not name a disassembly helper script `dis.py` — it shadows the stdlib `dis` module that `capstone` imports through `inspect`, and the failure surfaces as a confusing circular-import `AttributeError` on `capstone.Cs`.

### The corrupt-frame geometry model (IMPL-31 / Faz 4.6, 2026-09-01)

**The artifact is a half-width payload written linearly into a full-width raster.** Confirmed on three captures across two HAL states and two raster sizes, with an inverse control that round-trips byte-identically. Full record: `docs/raw-geometry-diagnosis.md`. Tool: `agc-50mp-yama/tools/frame_geometry.py`.

**Axis rule, which every future shape claim must apply first.** The AGC JPEG is stored **rotated 90 degrees** from the sensor raster: SOF0 says 6144x8192, EXIF `ImageWidth`/`ImageLength` say 8192x6144, `Orientation`=1. JPEG height is the raster row direction; JPEG width is the raster row count. `EV-38` was recorded in JPEG axes and reads differently once transposed — the two colour strips are side by side in raster axes, not stacked.

| State | Raster | Payload | W ratio | H ratio | Black |
|---|---|---|---|---|---|
| three-layer (`IMPL-23` era) | 8192x6144 | 4096x**6144** | 1/2 | 1/1 | 50% |
| five-word (`IMPL-30`) | 8192x6144 | 4096x**3072** | 1/2 | 1/2 | 75% |
| five-word, smaller request | 4096x3072 | 2048x**1536** | 1/2 | 1/2 | 75% |

**Three consequences worth carrying forward rather than re-deriving.**

1. **The reconstruction is a re-read, not a permutation.** Splitting each raster row at its midpoint and emitting the halves as consecutive rows leaves the linear byte stream untouched, so un-folding is `Image.frombytes` at half the width — one call, no per-row loop over 50 megapixels. This is why the decisive probe cost nothing.
2. **`80340003` is removed as a candidate on evidence, not on cost.** The fault is *proportional* to the request; the vendor tag holds a *fixed* `[0 0 4096 3072]` and never moves (`EV-40`). A fixed rect cannot yield a 2048x1536 payload at a 4096x3072 raster, nor a height ratio that changes while the tag does not. `DEC-13` is vindicated by measurement.
3. **The `IMPL-23` / `IMPL-30` "50% vs 75%" discrepancy is reconciled.** Both figures were correct for their own state. The record was right to refuse to reconcile them from description alone. **Attribution of the height change to the active-array raise is NOT claimed** — the two states differ in session, scene and `pref_48m_key`, so the one-variable rule is unmet. That attribution is `F4.6-05`/`F4.6-06` work.

**The open question this leaves, stated so it is not confused with a settled one:** *why* the payload is half-width. Candidates are a 2x2-binned sensor delivery into a full-size buffer, a remosaic path configured at half extent, or a stride negotiated from a stale rect. Not answerable from an image; it needs the negotiated buffer stride and binning state from a filtered logcat during capture (`F4.6-06`).

**The `MaximumResolution` scaler tables, `d0014` / `d0015` / `d0016`** — located 2026-09-03 (`IMPL-47` / `Faz4.7`, `F4.7-02`) against the live HAL `ce419bc901bea61945d166aee11e1ab0`.

All four scaler stream/duration emissions read from one shared base object, `[x19 + 0xa6560 + 0x68]`:

| tag | name | count field | data | emission address |
|---|---|---|---|---|
| `d000a` | `availableStreamConfigurations` (default) | `base+0x6f28` | `ldr [base+0xb10]` — a **pointer** | `0x01665178` |
| `d0014` | `availableStreamConfigurationsMaximumResolution` | `base+0x6f2c` | `add base+0xb28` — **inline** | `0x0166536c` |
| `d0015` | `availableMinFrameDurationsMaximumResolution` | `base+0xd444` | `base+0x6f48` | `0x01664b84` |
| `d0016` | `availableStallDurationsMaximumResolution` | `base+0xe850` | `base+0xde50` | `0x01664bec` |
| `d000b` | `availableMinFrameDurations` (default) | `base+0xd440` | `ldr [base+0x6f30]` — a **pointer** | `0x01664ac0` |
| `d000c` | `availableStallDurations` (default) | `base+0xde48` | `add base+0xd448` — **inline** | `0x0166519c` |

- Each emission does `lsl w3, count, #2`, so the published element count is `count * 4` int32 — one 16-byte `{format, width, height, direction}` record per count unit. Camera 2's `d0014` count is **7**, giving the observed `int32[28]`.
- `d0014`'s emission additionally requires `[S+0x3d84] == 1` (the binning selector, untouched) and `[S+0x4968] == 0`, and its bit-28 gate at `0x01665354` is one of `hal-uhrfull-deneme.patch`'s eighteen NOPs.
- **The rows are not static data.** A whole-binary scan for `int32 1920` followed by `int32 1080` returns 20 aligned hits, none of them a stream-configuration record. The table is assembled at runtime.
- **The populator is `InitializeScalerStaticCaps`** — the same function recorded above for the default array and targeted by `Faz4.1`. At `0x016c5350`…`0x016c5368` it writes the default count and all three `MaximumResolution` counts in one consecutive store run, from values computed off a shared loop variable (`w24*2+2`, `w24+1`, `4`). A second writer touching the same fields is at `0x016bf7d4`.
- **Open:** whether the max-res rows are built in the same *loop* or merely the same *function*; where the `1920x1080` values originate; and whether `Faz4.1`'s `cmp #2` → `cmp #5` change reaches the max-res rows. The `0x016c5360` store writes `w24*2+2`, which cannot equal 7 for any integer `w24`, so that is **not** the path that produced camera 2's count and at least one other writer is involved.
- **The second writer, located and traced 2026-09-03 (host-side, `ce419bc9…`, no device write):** the block at `0x16bf788`…`0x16bf824` is the loop's *commit* — it stores eight already-computed stack values into the struct base `x8 = [x23]+[sp+0x210]`, one field per store, including `str w1,[x8,x14]` with `w14=0x6f2c`, i.e. `w1` (loaded from `[sp,#0x1f0]`) **is** `d0014`'s count. Control flow shows this commit sits at the loop's *low-address* end (compiler-hoisted latch), reached after a body that runs from roughly `0x16bf850` to `0x16c5490` once per iteration; the loop condition itself is `ldr w25,[x23,#0x9a0]; cmp w27,w25; b.hs <exit>` at `0x16bf834`, so `[x23+0x9a0]` is the iteration bound and `x23 = *[sp+0x218] = *(*[x28])`, fixed for the whole function (not re-derived per iteration).
- **`[sp,#0x1f0]` (the count feeding `d0014`) has no write anywhere before the read that commits it** — every store to that slot (`0x16c09c4`, `0x16c0b54`=zero, `0x16c1a74`, `0x16c1dfc`, `0x16c3f70`=zero, `0x16c4b4c`, `0x16c4d54`, `0x16c5490`) lies *after* the commit block's address but *before* it in execution order, i.e. inside the same loop body on the same iteration. This confirms the count is a genuine loop-computed result, not a literal, and narrows nothing about *which* of the eight sites is live for camera 2 — that requires walking the intervening conditionals.
- **The body's first branch point is a large switch on a per-camera-fixed field, not on the loop index.** Nine instructions after the commit's iteration boundary, `w17 = [x23+0x3b10]` (nothing per-iteration ORs into it) is compared against a run of 16-bit-pair constants (`0x40906`, `0x106ff`, `0x10500`, `0x10600`, `0x10605`, `0x503ff`, `0x50200`, …) via `mov`/`movk`/`cmp`/`b.eq`/`b.gt` — the standard lowering of a C `switch` on a sensor/format identifier. This gates which of several downstream computations runs, and is the most likely reason `d0014`'s count differs by camera family. The loop index `w27` itself is used only once directly (`sxtw x21,w27` at `0x16bf840`); the actual per-iteration record pointer is `x22 = [x23+0x9a8] + (x3*x6)`, with `w24 = [x22+0x8f8]` read as a per-record field at `0x16bf878` — so indexing does happen, through a computed stride rather than a `w27`-scaled address, and has not yet been resolved to a concrete source table.
- **Assessment:** two independent lines of evidence now agree that `d0014` is not a patchable static table: no byte pattern exists (`IMPL-47`), and its value is the tail of a per-camera loop whose first branch is a multi-way switch on a sensor/format identifier spanning most of a 6,516-instruction function. Resolving the exact literal source of `7` / `1920` / `1080` for camera 2 requires walking that switch's live branch and at least one more computed-stride array read — a materially larger static effort than locating an emission site, not yet attempted, and its payoff is unproven even if completed: `Faz4.1`'s `F4.1-05b` already showed this binary has no free code-cave space for an additive patch, so a located-but-unreachable source would still need a substitution rather than an addition.
- Tooling: `agc-50mp-yama/tools/region_dis.py` (disassemble a vaddr range) and `agc-50mp-yama/tools/immscan.py` (find `movz`/`movk` carrying a given 16-bit immediate). Both read-only.

**The default duration tables `d000b` / `d000c` — located and measured 2026-09-05 (`IMPL-64` / `Faz4.2`, `F4.2-02` / `F4.2-03`), against the live `fullres` HAL `fe0245a4720fb07b01d96deef47f5569` (host copy byte-identical to the device).** These are the two sites `Faz4.2` was written to find, and they complete the six-table set above.

- **Emission.** `d000b` publishes at `0x01664ac0` (count `base+0xd440`, data read as a pointer from `base+0x6f30`); `d000c` publishes at `0x0166519c` (count `base+0xde48`, data **inline** at `base+0xd448`). Each has a second emission path — `0x01664b20` and `0x01665200` — taken when `[[x19+0x68]] + 0x148 == 5`. Both do the same `lsl w3, count, #2` as the other four, so the published int64 count is `count * 4`: one 32-byte `{format, width, height, nanoseconds}` record per count unit.
- **The rows are written in the same function and the same per-entry block as the stream-configuration rows** — `InitializeScalerStaticCaps` — not by a separate loop, but with their own row counters on the stack. The `d000b` writer is `0x016c22a8`…`0x016c22b0` (`add x16, x13, x11, lsl #5` ; `stp x9, x19, [x16]` ; `stp x3, x5, [x16, #0x10]`), counter `[sp+0x18c]`. Its value is **computed, not stored**: `w2 = 0x3b9aca00` (1e9) `udiv` the per-mode frame rate at `0x016c22a4`, which is why every measured row is exactly `1000000000/30 = 33333333` or `1000000000/15 = 66666666`. The `d0015` max-res writer at `0x016c2318`…`0x016c2328` is the same shape in floating point (`fdiv` against the double `0x41cdcd6500000000` = 1e9).
- **Which of the two runs is decided by a `fullres` patch point.** The selector is `tbz w25, #0` at `0x016c2264`, where `w25 = cset(ne, cmp w8,#1) | [sp+0x1ac]` and `w8` comes from `0x016c2254` — `hal-fullres.patch` index `5965973`, `ldr w8,[x24,#0x3d84]` → `mov w8,#0`. Forced to 0, `w25` bit 0 is always 1 and control always takes the **default** (`d000b`) path rather than the `MaximumResolution` (`d0015`) one.
- **`agc-50mp-yama/hal-raw50-deneme.patch` is a four-point patch and two of its points are these duration gates.** Indices `5965999` and `5966028` are `0x016c22bc` and `0x016c2330` — verified byte-for-byte against this base: both hold `9f0a0071` = `cmp w20, #2` and both become `cmp w20, #5`. Only indices `5965367`/`5965574` (`0x016c18dc`/`0x016c1c18`) touch `d000a`. This **resolves the prediction recorded above** that “sites 3 and 4 belong to `availableMinFrameDurations` / `availableStallDurations`” — confirmed statically, and the patch already covers them, which no planning document had recorded.
- **The stall-duration writer hardcodes one format.** At `0x016c3284`…`0x016c32dc` the record is `{w22, width, height, fcvtzs(s18*s11)}` with `w22 = #0x21` set as an immediate at `0x016c3290` — BLOB/JPEG. There is no format loop and no range gate to widen. The `d0016` writer at `0x016c32e0` is identical with `w12 = #0x21`. **Adding a stall row for another format is therefore additive, not substitutive**, and `F4.1-05b` already measured that this binary has no code cave ≥ 16 bytes; changing the immediate would *replace* JPEG's stall rows rather than add RAW ones.
- **Measured baseline, camera 3, live `fullres`, `pref_48m=0` / `pref_resolution=full`** (`snapshots/20260905-1953__Faz4.2__F4206-cam3-three-tables.txt`): `d000a` `int32[508]` = 127 rows (124 OUTPUT, 3 INPUT); `d000b` `int64[504]` = 126 rows; `d000c` `int64[120]` = 30 rows. **Every OUTPUT stream-configuration entry already has a minimum-frame-duration row — zero missing.** `d000b` carries two rows with no OUTPUT counterpart, `[33 320 240]` and `[33 176 144]`. `d000c` carries **format 33 only**. The RAW emission on this base is `32`/`36`/`37` at `4096x3072` and `4096x2304` — none at `8192x6144` — each with a `d000b` row and **no** `d000c` row.
- **No vendor duration table exists to take reference values from** (`F4.2-02`). `xiaomi.scaler.availableStreamConfigurations` (`81850000`, `int32[2136]`) and `org.codeaurora.qcamera3.quadra_cfa.availableStreamConfigurations` (`80340002`) have no duration counterparts anywhere in camera 3's dump. The only format-specific duration tables present are `android.heic.*` (`1c0001`/`1c0002`, `int64[120]`) and `android.jpegr.*` (`210001`/`210002`, `int64[112]`).
- **Cameras 11 and 12 publish `d000a` `int32[124]` with no `d000b` and no `d000c` at all** — the only two of the thirteen where the duration tables are absent rather than merely incomplete (`snapshots/20260905-1953__Faz4.2__F4201-per-camera-duration-census.txt`). Recorded as `FIND-4.2-02`.

- **Open Camera ships under a disguised package name and no obvious search finds it** (`IMPL-68`, `Faz4.4`). The third-party consumer this project measures 50.3 MP with is installed as **`com.xiaomi.module.evaluation`**, activity **`net.sourceforge.opencamera.MainActivity`**, version 1.55, APK md5 `e4efeb07919bce10bc14f6f42e5b09f2` — byte-identical to the `OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk` recorded in `docs/reverse-engineering-toolchain.md`. **No `pm list packages` filter on "camera", "open" or "sourceforge" reaches it, and `pm path net.sourceforge.opencamera` returns nothing.** Locate it through `dumpsys activity recents`, whose `baseIntent` carries the real `package/activity` pair, or launch it directly with `am start -n com.xiaomi.module.evaluation/net.sourceforge.opencamera.MainActivity`. It writes to **`/sdcard/DCIM/OpenCamera/`**, not `DCIM/Camera`, so a capture-accounting baseline must cover both folders. This falsifies `docs/raw-geometry-diagnosis.md` line 327, which records the consumer as unrunnable because "`pm` keeps no record of the package" (`FIND-4.4-02`, routed to `Faz9.3`).
- **The coexistence criterion is measured and it holds** (`IMPL-68`, `Faz4.4`). In one HAL state `fe0245a4720fb07b01d96deef47f5569`, with a zero-line smoke bracket across the whole run: AGC captured **12.58 MP at black `0.0000`** with configured streams `4096x3072` on RAW10 `0x25` and YUV `0x23`, and Open Camera captured **8192x6144 = 50.33 MP at black `0.0000`**, twice, four minutes apart. Under the consolidated artifact all thirteen camera ids have `activeArray` equal to their own `pixelArray` — **no id is internally inconsistent**, so `FIND-4.5-01`'s front-camera problem does not arise on the shipped table and is a property of the experimental `hal-activearray-deneme.patch` alone.

### Kernel trees the Android 16 build consumes (IMPL-93 / Faz 8.2, 2026-09-13)

- **Which tree is the kernel.** AOSPA `beryl` `build.sh:221` builds `kernel_platform` with `KERNEL_VARIANT=gki`. The boot `Image` comes from `kernel_platform/common` = `xiaomi-8550/android_kernel_qcom_sm8550` `beryl` `b11e560`, `Makefile` 5.15.185. `kernel_platform/msm-kernel` = `xiaomi-8550/android_kernel_xiaomi_sm8550` `beryl` `1c509b3`, 5.15.189, builds only vendor modules and dtbs (`build.config.msm.gki`, `KMI_ENFORCED=1`). Both are `KMI_GENERATION=8`.
- **ACK position.** Newest contained `android13-5.15` tag: `2025-07_r1` in `common`, `2025-09_r4` in `msm-kernel`. The newest tag at measurement, `android13-5.15-2026-06_r4` (5.15.206), is 4472 and 3798 commits ahead, with 1 and 16 `git merge-tree` conflicts.
- **Where the camera driver lives (invariant 3).** CSIPHY (`drivers/cam_sensor_module/cam_csiphy`) and CSID (`drivers/cam_isp/isp_hw_mgr/isp_hw/ife_csid_hw`) are out of tree, in `AOSPA/vendor_qcom_opensource_camera-kernel` `xiaomi-8550` (tip `2ad2fde` when read), brought in by the barista beans and built as a DLKM against the KMI (`TARGET_KERNEL_DLKM_CAMERA_OVERRIDE`). A core-kernel change reaches the CSIPHY/CSID allocation code only through the kernel interfaces that module includes.
- **Method note.** `android.googlesource.com` refuses fetch-by-id of unadvertised objects, so a blobless clone cannot lazily fetch ACK blobs; fetch the needed blobs through gitiles `?format=TEXT` and verify each with `git hash-object` before relying on `merge-tree`.

## 7. Invariants and Constraints

1. **Reversibility.** Every modification is a bind-mount or an md5-guarded offset patch. A module that cannot be disabled is a bricked phone.
2. **Fail closed.** Size check, then md5 check, then write. Never write on a mismatch.
3. **Restart ordering.** Client before HAL. Violating this leaks CSIPHY/CSID allocations and blackens preview in every mode. (Section 5.) **Holds under direct test (IMPL-13, 2026-08-31):** ~17 mode transitions and 2 reboots across all ten modes left the bind-mount count at exactly 1 on each path every time, with no leak symptom. Note that `CSIPHYHw:4 AvailableResource=0` — which `Kullanim.txt` presents as the leak signature — also reads 0 on a clean boot and is therefore **not diagnostic** (`FIND-2.3-04`).
4. **Layer exclusion.** `50mp` and DCG/LN are mutually exclusive **as the module ships, and this is now a deliberate retention rather than an untested assumption.** `Kararlar #4` was **executed and proven for DCG** (IMPL-15, 2026-08-31): composing the `fullres` HAL with `dcgB`+mode-0-12-bit produced a clean 50.3 MP capture with no corruption, so the constraint is **removable, not physical**. **Faz 5.3 decided to retain it anyway (IMPL-17, user decision).** Three reasons, all measured: the composed capture is **visually indistinguishable** from `50mp` alone, so there is no demonstrated benefit to ship; only **DCG** was proven, and the two combinations the roadmap names (`50mp`+`ln2`, `50mp`+`ln4`) cannot be validated because those modes crash AGC independently (`FIND-2.3-02`); and removal is a **state-model change**, not a dispatch edit — see `ARC-03` for the six-surface inventory. Enforcement as logic lives at `post-fs-data.sh:15-27` and `setmode.sh:177-192` only. The verified candidate `candidates/dcgB-m0-12bit.bin` (md5 `80b53215…`) is **kept and deliberately not in `blobs/`**, so adoption stays cheap if a benefit is ever demonstrated. Re-open this invariant only with new evidence of benefit, not of mechanism — mechanism is settled. **Holds under direct test (IMPL-13, 2026-08-31)**, in both directions and bracketed: selecting `50mp` reverted the sensor layer to stock (`9e4d0fe1…`) while the HAL went `fullres`. The enforcement sites are `post-fs-data.sh:16-18` and `setmode.sh`. **A consequence worth stating plainly: `50mp` combined with `ln2`/`ln4` has never been reachable on this device**, so no observed behaviour can be attributed to that combination. The mechanism is the global white level — see the sensor blob entry in section 3. Faz 5.1 generated the candidate that targets this invariant (`docs/mode0-12bit-candidate.md`); Faz 5.2 is what tests it, and until it does, this invariant stands unmodified.
5. **Video integrity.** 1080p60 and 4K60 must remain functional in every mode. A standing acceptance criterion, user-validated. **Unassessable on this build as of IMPL-13 (2026-08-31) — neither confirmed nor refuted.** AGC fails `configure_streams()` before any 60 fps profile can be selected, so the invariant's own precondition is unreachable through AGC. The failure is **not module-caused**: the video section is black in plain `stock` with sensor and HAL both unmodified, in four states before and after a reboot (`FIND-2.3-03`, routed to Phase 3). OpenCamera records plain 1080p cleanly in `dcgB`, so the camera path itself is not broken. Do not record this invariant as passing on the strength of that — OpenCamera at 1080p30 does not exercise it.
6. **Gcam static-metadata consistency.** `libgcam static_metadata.cc:667` requires `frame_raw_max` to equal the active array size **or** the pixel array size. Violation → `gcam.cc:274 Create … failed` → `NullPointerException: Gcam.f()`. **This single invariant explains two failures from opposite directions:** the Faz 4 wide patch raised the active array without raising raw; the Faz 12 RAW patch raised raw without raising the array. Both sides must move together.

   **Outcome recorded 2026-09-01 (IMPL-23 / Faz 3.5). The invariant is CONFIRMED exactly as stated, and it is now known to be NECESSARY BUT NOT SUFFICIENT.** Satisfying it through the *pixel array* branch works: with `pixelArraySize=[8192 6144]` and RAW10 8192x6144 both live, `static_metadata.cc:667` stopped occurring entirely, `Gcam` initialised, and AGC completed three reproducible 50.3 MP captures. That is the first time this gate has ever been passed on this device.
   **The refinement:** passing the gate does not produce a correct image. Every full-resolution AGC frame is geometrically corrupt — content fills only the active-array extent of a full-size buffer, leaving exactly half the frame black, with a magenta cast over the rest. The gate compares `frame_raw_max` against *either* array, but the imaging pipeline downstream still lays out geometry from the **active** array. So satisfying invariant 6 via `f0006` alone leaves `f0000`, `f000a` and the QTI vendor tag `org.codeaurora.qcamera3.quadra_cfa.activeArraySize (80340003)` — all three still `[0 0 4096 3072]` — inconsistent with the buffer. Open Camera is unaffected, because its frames come from the HAL's own ISP path rather than from Gcam's RAW consumption.
   **Consequence for Phase 4:** whatever narrowing Phase 4 performs must preserve the raised `f0006` *and* must additionally raise the three active-array tags together, or the corruption stands. Raising `f0006` on its own is a metadata fix, not an imaging fix.

   **Superseded in its diagnosis 2026-09-01 (IMPL-30, then IMPL-31 / Faz 4.6). The invariant itself stands; the account of the corruption above does not.** Both patchable active-array tags were raised to `[0 0 8192 6144]` and **the frame stayed corrupt** (`EV-37`), which refutes "content fills only the active-array extent" as the mechanism. The measured mechanism is a **half-width payload written linearly into a full-width raster** (`EV-42`), and it is *proportional to the request* rather than pegged to any array value (`EV-45`) — so no tag value explains it and the vendor tag `80340003` is excluded on evidence. Two corrections follow for anyone reading the paragraph above: "exactly half the frame black" was the **three-layer** state and 75% is the five-word state, both correct (`EV-44`); and the magenta cast is **alternate payload rows** carrying opposite CFA phase, not a single flip (`H-03`). The preservation requirement in the previous paragraph is unaffected and still binds Phase 4.
   **Phase 3 closure recorded 2026-09-05 (IMPL-52 ... IMPL-61 / Faz 3.7-Faz 3.11). The invariant stands and the objective it served is retired.** `DEC-14` retired "50 MP end-to-end in AGC" on 2026-09-03 and replaced it with "AGC stable at 12.6 MP under 50 MP", which Phase 3 then delivered and measured: `pref_48m_key`=`0` with `pref_camera_resolution`=`full` derives `pref_camera_picturesize_back_key`=`4096x3072` on the shipped `fullres` base `fe0245a4720fb07b01d96deef47f5569`, and AGC captures cleanly there (12.58 MP, black fraction 0.0000-0.0027 across five captures in four sessions; threshold `< 0.01`). **The derived key is a cache of the last AGC start, not a setting** (`IMPL-52`): writing it does not survive a restart, the derived keys lag an input write by one AGC start, and the configured streams lag by one further start (`FIND-3.10-04`). The configuration survived cold start, camera-stack restart, QuickSettings mode switch and reboot with zero field changes (`IMPL-61`, four axes). Operator record: `docs/agc-12mp-configuration.md`.

   **The four measured negatives that close the 50 MP route, attached here so they travel with the invariant.** `d0014` is not static data - an exhaustive scan of all 27,268,688 bytes finds no `[fmt, 1920, 1080, 0]` quadruple run (`IMPL-47`); its value is computed as the tail of a per-camera loop in `InitializeScalerStaticCaps` behind a multi-way switch (`IMPL-51`); the binary's sole executable `PT_LOAD` segment contains no free run of >=16 bytes, longest 12 bytes in 3 instances, so an additive patch has nowhere to live (`IMPL-50`); and narrowing the broad RAW rows prevents AGC from launching, 3/3 at two independent bisection stages (`IMPL-49`, `IMPL-50`). **Reopening needs new evidence about one of those walls, not renewed effort against the same two** (`DEC-14`).

   **One measured exception, recorded and not resolved (`FIND-3.10-03`, 2026-09-05).** On the shipped `fullres` base with `pref_48m_key`=`1` and the mismatched stream pair (RAW10 `4096x3072`, YUV `8192x6144`), AGC produced a **clean** 6144x8192 / 50.33 MP image with black fraction `0.0000`, twice, against a prediction of a fold at ~0.75 committed in writing before the capture existed. The fold that `IMPL-43` measured at `0.7497` did not occur. The user ruled 2026-09-05 that `DEC-14` stands: this is a capture result, not new evidence about either wall, it is unexplained, and it has been reproduced twice within one session and zero times across sessions. It is the project's most interesting open question and is **not** a capability claim.

7. **Android high-resolution bucket.** `getOutputSizes(fmt)` excludes any size whose minimum frame duration exceeds 1/20 s; those appear only via `getHighResolutionOutputSizes(fmt)`. On camera 3: 8192x6144 = 66,666,666 ns (15 fps) → excluded; 4096x3072 = 33,333,333 ns (30 fps) → kept. This was the original root cause of AGC's 12.6 MP ceiling, and it is why Open Camera — which reads both lists — reached 50.3 MP unaided.
8. **The preference trap.** `pref_raw_key_N` and `pref_fix_resolution_key_N` independently break Gcam initialization by triggering the port's `getFixResolutionList` width-cap, which can shrink a sensor's RAW list to an odd size. This already caused one misattributed failure. **Check for and clear these before diagnosing anything else.**
   **Refined 2026-09-05 (IMPL-53, IMPL-54, IMPL-61 / Faz 3.7-Faz 3.11). Presence is not the fault; VALUE is.** Both keys were measured **inert at value `0`** - identical stream configuration with them present and absent - so a bare `0/12` presence assertion now fails on a state that is measured harmless. Audit the twelve keys by value.

   **AGC does self-arm two of them, and the earlier claim that it never does was measured against a weaker test.** Opening `CameraSettingsActivity` writes `pref_raw_key` and `pref_fix_resolution_key` at value `0` (`FIND-3.7-01`, `IMPL-54`); a plain `monkey ... LAUNCHER` start arms nothing (`IMPL-61`). The 2026-08-31 audit that concluded "the app does not self-arm the trap" used a plain launch from an empty first-run state, which is exactly the case that still arms nothing. **At least one further route exists and is unidentified** (`FIND-3.10-02`): the count moved `0 -> 2` in a session where no settings screen was opened. Corrected in `docs/phase3-preconditions.md` section 1 and in `README.md`.

9. **Signing.** No signing key ships in any distributed artifact. **Verified empirically 2026-08-24 by Faz 1.2**, not merely asserted: all five released archives (`ishtar-cam-modes-v1.0/v1.9/v2.0/v2.1`, `ishtar-aon-fix-v1.1`) were listed by entry name and contain no `.keystore`, `.jks`, `.p12`, `.pem`, or `.key` entry, and no entry at the 2,664-byte size of the local `debug.keystore`. Three sub-rules now carry this invariant forward:
   - **9a — Packaging assertion (specification for Faz 9.1 to implement).** A release archive is rejected if any of three conditions holds: (i) it contains an entry whose name ends in `.keystore`, `.jks`, `.p12`, `.pem`, or `.key`; (ii) it contains an entry at or near 27,268,688 bytes, the size class of `camera.qcom.so`, which would mean a vendor HAL binary was packaged; (iii) it contains any `.apk` entry other than exactly one named `tile-app.apk`. Each condition must be proven to fail the build when deliberately introduced — an assertion never observed failing is not an assertion. The check is by entry name and entry size only; no entry is extracted.
   - **9b — Key location policy.** The signing key belongs outside the repository and outside the packaged module directory. Today `ishtar-cam-modes/tile-app/build.sh` sets it to `$HERE/debug.keystore`, which places it inside the directory that gets zipped — containment currently depends entirely on the `.gitignore` rule and on the packaging step never sweeping it in. The key should be referenced through an external path supplied by the environment, with no concrete credential location recorded in any planning file. The key is auto-generated on first build if absent, so relocating it costs nothing except signing identity: a regenerated key changes the tile application signature and breaks upgrade-in-place for existing installs.
   - **9c — The password is not contained, and is not really a secret.** `build.sh` hardcodes the keystore store-password, key-password, and alias in plaintext, and that script ships inside `ishtar-cam-modes-v1.9`, `v2.0`, and `v2.1`. The values are deliberately not reproduced here or anywhere in `Planner-docs/`; measured without printing, the password is a six-character all-lowercase word that already appears publicly elsewhere in the repository. The consequence is that removing it from `build.sh` would not make it secret — it is guessable on the first attempt whether or not the script ships. Nothing is exploitable today, because the keystore itself has never been distributed and a password without its keystore grants nothing. The real rule this yields: **if the key is ever relocated per 9b, reused for a signed public release, or regenerated, it must get a genuine password at that moment** — the current one protects only a locally regenerable debug key. Routed as `DEC-10`.
10. **Blob binding.** Every offset is bound to one exact vendor build. Any ROM update that changes `camera.qcom.so` invalidates all offsets at once; the md5 guard is the detector. **Updated 2026-11-16 (planning run 21): realised.** The 2026-11-13 HyperOS 4 observation showed that the system update changed the HAL: its md5 `2a955e68…` differs from `HAL_STOCK_MD5`, while the sensor module still matches `EXPECT_MD5`. Under `DEC-33` the 50 MP HAL layer stays off on HyperOS 4 and is not re-derived for now; the sensor layer continues (`Faz10.2`).
11. **Host constraint.** Neither the kernel nor AOSP builds on Windows/NTFS, and WSL2 will not be installed (`DEC-24`, 2026-09-10). Android 16 builds run on a rented Hetzner Cloud server — Ubuntu 22.04 LTS on a CCX53, 32 vCPU / 128 GB / 600 GB NVMe (`DEC-22`, `DEC-25`) — from inputs pinned on GitHub beforehand (`ahmetxa/android_local_manifests`), and the server is deleted at the end of each session (`docs/build-environment.md`). The Windows host keeps the analysis and repackaging toolchain only (`docs/reverse-engineering-toolchain.md` section 7). **Rewritten 2026-09-11 by `IMPL-91` (`Faz7.1` `F7.1-12`)**; the retired text read: "Sources must live inside the WSL filesystem, never under `/mnt/c`. Disk is no longer a constraint (799 GB free); WSL2 is not installed." **Updated 2026-11-16 (planning run 21, `AUDIT-FIX-57`): retired.** No Hetzner server was ever rented: `DEC-26` moved the rental after Hetzner's new-account limit blocked the CCX53, and `DEC-28` (2026-11-13) abandoned the ROM build, so no Android 16 build runs on any server. The host part stands: the Windows host keeps the analysis and repackaging toolchain.

## 8. Open Ontology Questions

### Competency Questions

| ID | Question | Status | Evidence |
|---|---|---|---|
| OQ-01 | Where does `camera.qcom.so` write `android.sensor.info.pixelArraySize` (tag `f0006`)? | answered | **Located statically by IMPL-18 (Faz 3.2)** against stock HAL `c3fa63a8…`. The value is staged at `[x19+0x6550]` by `str` at `0x01666454` (or `0x01666460` on the `[S+0x3d84] == 1` path), copied from sensor-data offset `S+0x3c1c` (alt `S+0x3db4`) where `S = [x24+0x60]`, then published as tag `f0006` with count 2 by `bl 0x0166648c` into the CamX metadata publisher `0x1755430`. Containing function starts `0x01661f40`. **The value is runtime-derived, not a binary constant.** The nine previously recorded `movz`/`movk` sites are false positives and the six rodata dwords are tag-list interiors, not value sources; full detail and the ranked patch candidates are in the address book above. Faz 3.3 owns the confirming single-word patch and the `dumpsys` read. |
| OQ-02 | Does the HAL deliver remosaiced Bayer or raw Quad-Bayer at 8192x6144? | partially_answered | **2026-09-01 (IMPL-23 / Faz 3.5).** Indirect evidence points to remosaiced Bayer: the HAL declares `colorFilterArrangement (f0002) = BGGR`, and Open Camera's 8192x6144 capture is colour-correct. Not settled, because both facts concern the HAL's ISP output rather than the RAW10 buffer itself, and AGC's magenta cast is equally explained by the geometry fault. **The intended probe is unrunnable in this patch state and that is now a measured fact, not a failure to try:** a DNG requires `RAW_SENSOR` (format 32), advertised only at 4096x2304 and 4096x3072; `hal-raw50-deneme.patch` widens the format gate to 0x22..0x26 (34–38) and never reaches 32. Closing this needs emission extended to format 32 — Phase 4. See `H-03`, `EV-34`, `EV-35`. |
| OQ-03 | Can `pixelArraySize` be raised without breaking other consumers? | answered | **Answered for the consumers actually tested (IMPL-22 / Faz 3.4), not in general.** With the word applied on both the stock and fullres bases: the stock camera opens with live preview and captures an unchanged `3072x4096`; Open Camera captures **`8192x6144` = 50.3 MP** on the fullres base, preserving `EV-04`; 1080p60 (`1920x1080 @ 60.1`) and 4K60 (`3840x2160 @ 60.0`) both record and play in two modes; `dcgA` and the HAL-layer `50mp` mode both open; and a controlled fixed-position comparison shows **no field-of-view change**. Scope is three applications, two video profiles and two of ten modes — **not** a general compatibility claim. The one failure seen (`dcgB`) reproduces **without** the change and is `FIND-3.4-02`. AGC was deliberately not tested; that is Faz 3.5. Record: `docs/consumer-survey.md`. |
| OQ-04 | Is the 10-bit/12-bit mismatch the *only* obstacle to 50 MP + LN composition? | answered | **Measured by IMPL-15 on 2026-08-31, and the answer is yes for DCG.** With `dcgB` + mode 0 moved to 12-bit mounted under the `fullres` HAL, the camera opened without a Gcam NPE, preview was live in both AGC and OpenCamera, and OpenCamera captured a valid **8192x6144 / 50.3 MP** frame with no corruption. Nothing beyond the bit-depth mismatch had to move. Two limits on the claim: the tested sensor layer is **DCG (`dcgB`), not LN** — `ln2`/`ln4` were not composed, and they independently crash AGC (`FIND-2.3-02`); and the composed frame is **visually indistinguishable** from the same shot at `50mp` alone, so the composition is *reachable* but showed no measured quality gain in a dark, flat scene. |
| OQ-05 | Is patch application atomic against power loss mid-write? | answered | No, and it does not need to be. `halpatch.sh:66-77` `hal_write` applies each entry with a separate `dd conv=notrunc`, so writes are **ordered, not atomic**. The target is `$MODDIR/active_hal/camera.qcom.so` (`halpatch.sh:30`), a module-private copy — never the live `/odm/lib64/hw/camera.qcom.so`. A partial write is **detected**: `hal_state` (`:80-87`) md5-classifies the copy and returns `unknown` when it matches neither known value. It is **recovered**: `hal_set` (`:97-99`) calls `hal_seed` on `unknown`/`none`, which re-copies the device's stock binary and verifies it (`:106-116`). `hal_set:101` re-verifies md5 after every write, so a failed `dd` cannot be reported as success. `hal_write` has exactly one caller (`:100`), which verifies. |
| OQ-06 | Does the WebUI pass any user input into a shell invocation? | answered | No. Exhaustive trace of `webroot/index.html`: exactly **four** `exec()` call sites — `:268` (`ACT + ' info'`), `:300` (`exec(cmd)` inside `run()`), `:332` (`ACT + ' lang ' + lang`), plus the definition at `:193`/`:204`. `run()` has exactly **two** callers: `:317` (`ACT + ' toggle ' + id`) and `:325` (`ACT + ' set ' + id`), where `id` iterates the source-literal arrays `MAIN_MODES` (`:187`) and `EXTRA` (`:188`). `lang` at `:330` reads `dataset.lang` from the two static buttons at `:98-99` (`en`/`tr`). `ACT`/`MODDIR` are string literals (`:122-123`). No `exec` argument has a user-controllable component. Backstop: `action.sh:108-114` `valid()` whitelists the mode against a fixed ten-element list before `:131` interpolates it into `sh -c`. |
| OQ-07 | Does `customize.sh` normalize `mode` and `active/` at install time? | answered | No — and the shipped archive makes it moot. `customize.sh` (78 lines, read in full) contains **zero** writes to `mode`; the only writer in the module is `setmode.sh:204`. But `unzip -Z1` on `ishtar-cam-modes-v2.1.zip` and `v2.0.zip` shows neither ships `mode`, `lang`, `active/`, or `active_hal/` — packaging already excludes runtime state. On first boot `post-fs-data.sh:14` reads an absent file, `MODE` is empty, and the `*)` arm at `:23-27` defaults to `stock`. **`AUTOPSY-P3-03` is contradicted for the shipped artifact.** The residual defect is the claim at `customize.sh:62` ("guncellemede mevcut mod"), which nothing implements — see FIND-1.5-01. |
| OQ-08 | Does `ishtar-cam-modes` ship its own `sepolicy.rule`? | answered | No. `find` over the source tree returns no `*sepolicy*` and no `*.rule` at any depth, and `unzip -Z1` confirms neither `v2.1` nor `v2.0` carries such an entry. The module relies on `chcon u:object_r:vendor_file:s0` applied to the bind-mount source instead (`post-fs-data.sh:70`, `halpatch.sh:114`, `setmode.sh:255`): the mounted file is relabelled to the context the camera stack already expects, so no policy rule is needed. |
| OQ-09 | Does any released zip already contain `debug.keystore`? | answered | Faz 1.2 audit, 2026-08-24: all five archives listed by entry name; zero `.keystore`/`.jks`/`.p12`/`.pem`/`.key` entries and zero entries at the 2,664-byte keystore size. Adjacent finding: the keystore password ships in plaintext inside `tile-app/build.sh` in v1.9/v2.0/v2.1 (see invariant 9c, `DEC-10`). |
| OQ-10 | Does the device's live state match the workspace `mode` file (`stock`)? | answered | Faz 2.1 smoke run 2026-08-30: device is on `dcgB`, workspace file says `stock`. The workspace file tracks the last host-side edit, not the device. |
| OQ-11 | Why is the `tiles hide` option ineffective? | answered | **Faz 2.4 / IMPL-71, 2026-09-06, static.** The cause is recorded in the tree in three independent places and needed no new measurement. `tiles hide` is not a Tile control at all: `action.sh:240-243` writes the marker `hide_launcher` and calls `launcher_sync()` (`action.sh:86-90`), which runs `pm disable com.ishtar.cammodes/.Launcher` against the **activity-alias** declared at `tile-app/AndroidManifest.xml:57-68`. The four Tile services (`:71`, `:82`, `:93`, `:104`) are never touched. The component disable **succeeds** at the package-manager layer; the failure is one layer further out — AOSPA Launcher3 keeps the drawer entry regardless, measured on device and recorded at `action.sh:73-82` and `Kullanim.txt:59-67`, including after a fresh install, so it is not a stale launcher cache. The only effect of the disable is to leave the drawer entry **dead**: tapping it opened Android Uygulama Bilgisi instead of the WebUI. Hence the v2.0 auto-hide rule was withdrawn and the default became visible. Note the vocabulary trap this question carried: the option is named for Tiles but operates on Launcher visibility, and those are separate mechanisms (invariant: do not conflate them). |
| OQ-12 | Which framework camera index maps to which physical sensor across all lenses? | partially_answered | Faz 2.1 measurement 2026-08-30 contradicts the stored shorthand: `dumpsys media.camera` maps framework device 3 to HAL id 9, which is **Front**-facing at 3264x2448 and cannot be the rear main. The rear IMX989 array sits on HAL id 0 and ids 2-7 and 10. Full per-device table in section 3. See `OQ-17`. **The previously recorded answer is in doubt, and that is why this reads `partially_answered` rather than `answered`:** the mapping this project relied on is contradicted by measurement and its replacement is not yet complete across all lenses. This cell carried that caveat in its status column until `AUDIT-FIX-11`; the status is now vocabulary-conformant and the caveat lives here. |
| OQ-13 | Are `Lddl;->P/Q` blocklists relevant to resolution filtering? | answered | **No** — both empty; hypothesis rejected |
| OQ-14 | Does the port have a working 48M mechanism? | answered | **No** — `Forty8Strip` is an identity stub; hypothesis rejected |
| OQ-15 | Why did AGC cap at 12.6 MP? | answered | `getOutputSizes()` high-resolution bucket exclusion (invariant 7), not a blocklist or a flag |
| OQ-16 | Why did the Faz 4 wide patch break AGC? | answered | same invariant as Faz 12, opposite direction (invariant 6) |
| OQ-17 | Which HAL camera id is the one the 16-point `fullres` patch actually modifies, and which one does AGC open? | partially_answered | Raised by the Faz 2.1 smoke run 2026-08-30; **answered by IMPL-12 on 2026-08-31** by the `fullres`-vs-baseline smoke diff it proposed. The patch modifies **all thirteen** camera ids, Front-facing included, not one — per-id deltas in section 3. Faz 4.1 must therefore size its guard for device-wide reach and cannot name a single target array count. **Which id AGC opens is still unmeasured** and stays open. Row updated by Faz 5.1, the first sub-plan since IMPL-12 whose boundary covers this file. |
