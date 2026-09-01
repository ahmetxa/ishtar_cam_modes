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
| `beryl` | A second Xiaomi device targeted for a future port. No device-specific files exist yet. |
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
| `android_kernel_*`, `common_sm8550` | Kernel source, read-only on this host | — |

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
- **Publishing function** — begins `0x01661f40` (`paciasp`), prologue `stp x29, x30, [sp, #-0x60]!` at `0x01661f44`. Stripped: no symbol covers it, and the nearest preceding `STT_FUNC` (`ChiEntry`, `0x01655750` + `0x144`) does **not** contain it. It publishes the entire `android.sensor.info.*` family — `f0001` through `f000a` — in one sequence.
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

**Related metadata tags** — `android.scaler.availableStreamConfigurations` `d000a`; `availableMinFrameDurations` `d000b`; `availableStallDurations` `d000c`; `android.sensor.info.activeArraySize` `f0000`; `preCorrectionActiveArraySize` `f000a`.

**Vendor tables** — `org.codeaurora.qcamera3.quadra_cfa.availableStreamConfigurations` carries only 33/34/35 at 8192x6144. `xiaomi.scaler.availableStreamConfigurations` already carries `[37 8192 6144 0]`, `[32 8192 6144 0]`, `[36 8192 6144 0]` — the values exist in a vendor table but not in the standard one, which is the whole reason the HAL patch is needed.

**AGC port obfuscation map** (identical in V9.6 and V14) — `Lhvg;` ResolutionSetting; `Llvo;` the hooked characteristics wrapper (the only class overriding `x(I)`); `Llwe;` delegating base; `Lghx;` extends `Llwe;`; `Lmip;->bs()` max of list; `Lmip;->bu()` `Size[]`→`List<Llig;>`; `Lmip;->eU()` blocklist filter; `Lddl;->P/Q` the `blacklisted_resolutions_back/front` lists (**both empty** — a rejected hypothesis); `Llig;->a` width, `->b` height; `Llwp;->a` format, `->b` `Llig;`.

**`LAGC;->Forty8Strip(I)I` is `return p0`** — an identity stub in both builds. The port's 48M mechanism does not exist in this build; the UI's "Redmi K20 Pro / Mi9" note confirms it. A rejected hypothesis, recorded so it is not tested a third time.

**Channel selection** — there is no separate 12 MP / 50 MP channel. `LensSettings.getImageFormatArr()` returns `[pref_raw_key_<lens>]` if set, otherwise `[0x25 RAW10, 0x26 RAW12, 0x20 RAW_SENSOR, 0x23 YUV]`. `AGC.getImageReaderFormat()` takes the first format with a non-empty size list, then `Lmip;->bs()` takes its **maximum** size. AGC therefore already prefers the largest available size; it was stuck at 12.6 MP purely because RAW10's maximum was 4096x3072. Preview uses `Lgsf;->a()`, nearest-to-target, so widening the list does not disturb preview.

**Toolchain** — Temurin JDK 21; smali/baksmali **2.5.2** from the legacy `org/smali` Maven group (`org.jf.*` package names) plus dexlib2, util, guava 31.1-jre, failureaccess, antlr-runtime 3.5.2, jcommander 1.82, ST4; uber-apk-signer 1.3.0; capstone 5.0.7 and pyelftools on any working interpreter. Full procedure with ordered steps and self-checks: `docs/reverse-engineering-toolchain.md`. **Host state corrected 2026-08-30:** a real CPython **3.14.7** is installed (`python`, `py`); `python3` is a Store alias stub and must not be probed as the availability test. The **embeddable** Python 3.12.7 distribution is therefore a fallback for interpreter-less hosts, not a requirement here. `capstone`/`pyelftools` are not yet installed; `java` is absent from PATH, so the Java-path self-check is deferred rather than passed.

**Toolchain negative findings** (each cost real time): apktool's bundled smali `Main` classes are stripped stubs and cannot be invoked; `com.android.tools.smali` Maven paths return 404; the Bitbucket mirror returns 403; google/smali publishes no release binaries; **radare2 and rabin2 5.9.8 do not complete on this 27 MB binary** (no output in 300 s, from either shell).

## 7. Invariants and Constraints

1. **Reversibility.** Every modification is a bind-mount or an md5-guarded offset patch. A module that cannot be disabled is a bricked phone.
2. **Fail closed.** Size check, then md5 check, then write. Never write on a mismatch.
3. **Restart ordering.** Client before HAL. Violating this leaks CSIPHY/CSID allocations and blackens preview in every mode. (Section 5.) **Holds under direct test (IMPL-13, 2026-08-31):** ~17 mode transitions and 2 reboots across all ten modes left the bind-mount count at exactly 1 on each path every time, with no leak symptom. Note that `CSIPHYHw:4 AvailableResource=0` — which `Kullanim.txt` presents as the leak signature — also reads 0 on a clean boot and is therefore **not diagnostic** (`FIND-2.3-04`).
4. **Layer exclusion.** `50mp` and DCG/LN are mutually exclusive **as the module ships, and this is now a deliberate retention rather than an untested assumption.** `Kararlar #4` was **executed and proven for DCG** (IMPL-15, 2026-08-31): composing the `fullres` HAL with `dcgB`+mode-0-12-bit produced a clean 50.3 MP capture with no corruption, so the constraint is **removable, not physical**. **Faz 5.3 decided to retain it anyway (IMPL-17, user decision).** Three reasons, all measured: the composed capture is **visually indistinguishable** from `50mp` alone, so there is no demonstrated benefit to ship; only **DCG** was proven, and the two combinations the roadmap names (`50mp`+`ln2`, `50mp`+`ln4`) cannot be validated because those modes crash AGC independently (`FIND-2.3-02`); and removal is a **state-model change**, not a dispatch edit — see `ARC-03` for the six-surface inventory. Enforcement as logic lives at `post-fs-data.sh:15-27` and `setmode.sh:177-192` only. The verified candidate `candidates/dcgB-m0-12bit.bin` (md5 `80b53215…`) is **kept and deliberately not in `blobs/`**, so adoption stays cheap if a benefit is ever demonstrated. Re-open this invariant only with new evidence of benefit, not of mechanism — mechanism is settled. **Holds under direct test (IMPL-13, 2026-08-31)**, in both directions and bracketed: selecting `50mp` reverted the sensor layer to stock (`9e4d0fe1…`) while the HAL went `fullres`. The enforcement sites are `post-fs-data.sh:16-18` and `setmode.sh`. **A consequence worth stating plainly: `50mp` combined with `ln2`/`ln4` has never been reachable on this device**, so no observed behaviour can be attributed to that combination. The mechanism is the global white level — see the sensor blob entry in section 3. Faz 5.1 generated the candidate that targets this invariant (`docs/mode0-12bit-candidate.md`); Faz 5.2 is what tests it, and until it does, this invariant stands unmodified.
5. **Video integrity.** 1080p60 and 4K60 must remain functional in every mode. A standing acceptance criterion, user-validated. **Unassessable on this build as of IMPL-13 (2026-08-31) — neither confirmed nor refuted.** AGC fails `configure_streams()` before any 60 fps profile can be selected, so the invariant's own precondition is unreachable through AGC. The failure is **not module-caused**: the video section is black in plain `stock` with sensor and HAL both unmodified, in four states before and after a reboot (`FIND-2.3-03`, routed to Phase 3). OpenCamera records plain 1080p cleanly in `dcgB`, so the camera path itself is not broken. Do not record this invariant as passing on the strength of that — OpenCamera at 1080p30 does not exercise it.
6. **Gcam static-metadata consistency.** `libgcam static_metadata.cc:667` requires `frame_raw_max` to equal the active array size **or** the pixel array size. Violation → `gcam.cc:274 Create … failed` → `NullPointerException: Gcam.f()`. **This single invariant explains two failures from opposite directions:** the Faz 4 wide patch raised the active array without raising raw; the Faz 12 RAW patch raised raw without raising the array. Both sides must move together.
7. **Android high-resolution bucket.** `getOutputSizes(fmt)` excludes any size whose minimum frame duration exceeds 1/20 s; those appear only via `getHighResolutionOutputSizes(fmt)`. On camera 3: 8192x6144 = 66,666,666 ns (15 fps) → excluded; 4096x3072 = 33,333,333 ns (30 fps) → kept. This was the original root cause of AGC's 12.6 MP ceiling, and it is why Open Camera — which reads both lists — reached 50.3 MP unaided.
8. **The preference trap.** `pref_raw_key_N` and `pref_fix_resolution_key_N` independently break Gcam initialization by triggering the port's `getFixResolutionList` width-cap, which can shrink a sensor's RAW list to an odd size. This already caused one misattributed failure. **Check for and clear these before diagnosing anything else.**
9. **Signing.** No signing key ships in any distributed artifact. **Verified empirically 2026-08-24 by Faz 1.2**, not merely asserted: all five released archives (`ishtar-cam-modes-v1.0/v1.9/v2.0/v2.1`, `ishtar-aon-fix-v1.1`) were listed by entry name and contain no `.keystore`, `.jks`, `.p12`, `.pem`, or `.key` entry, and no entry at the 2,664-byte size of the local `debug.keystore`. Three sub-rules now carry this invariant forward:
   - **9a — Packaging assertion (specification for Faz 9.1 to implement).** A release archive is rejected if any of three conditions holds: (i) it contains an entry whose name ends in `.keystore`, `.jks`, `.p12`, `.pem`, or `.key`; (ii) it contains an entry at or near 27,268,688 bytes, the size class of `camera.qcom.so`, which would mean a vendor HAL binary was packaged; (iii) it contains any `.apk` entry other than exactly one named `tile-app.apk`. Each condition must be proven to fail the build when deliberately introduced — an assertion never observed failing is not an assertion. The check is by entry name and entry size only; no entry is extracted.
   - **9b — Key location policy.** The signing key belongs outside the repository and outside the packaged module directory. Today `ishtar-cam-modes/tile-app/build.sh` sets it to `$HERE/debug.keystore`, which places it inside the directory that gets zipped — containment currently depends entirely on the `.gitignore` rule and on the packaging step never sweeping it in. The key should be referenced through an external path supplied by the environment, with no concrete credential location recorded in any planning file. The key is auto-generated on first build if absent, so relocating it costs nothing except signing identity: a regenerated key changes the tile application signature and breaks upgrade-in-place for existing installs.
   - **9c — The password is not contained, and is not really a secret.** `build.sh` hardcodes the keystore store-password, key-password, and alias in plaintext, and that script ships inside `ishtar-cam-modes-v1.9`, `v2.0`, and `v2.1`. The values are deliberately not reproduced here or anywhere in `Planner-docs/`; measured without printing, the password is a six-character all-lowercase word that already appears publicly elsewhere in the repository. The consequence is that removing it from `build.sh` would not make it secret — it is guessable on the first attempt whether or not the script ships. Nothing is exploitable today, because the keystore itself has never been distributed and a password without its keystore grants nothing. The real rule this yields: **if the key is ever relocated per 9b, reused for a signed public release, or regenerated, it must get a genuine password at that moment** — the current one protects only a locally regenerable debug key. Routed as `DEC-10`.
10. **Blob binding.** Every offset is bound to one exact vendor build. Any ROM update that changes `camera.qcom.so` invalidates all offsets at once; the md5 guard is the detector.
11. **Host constraint.** Neither the kernel nor AOSP builds on Windows/NTFS. Sources must live inside the WSL filesystem, never under `/mnt/c`. Disk is no longer a constraint (799 GB free); WSL2 is not installed.

## 8. Open Ontology Questions

### Competency Questions

| ID | Question | Status | Evidence |
|---|---|---|---|
| OQ-01 | Where does `camera.qcom.so` write `android.sensor.info.pixelArraySize` (tag `f0006`)? | answered | **Located statically by IMPL-18 (Faz 3.2)** against stock HAL `c3fa63a8…`. The value is staged at `[x19+0x6550]` by `str` at `0x01666454` (or `0x01666460` on the `[S+0x3d84] == 1` path), copied from sensor-data offset `S+0x3c1c` (alt `S+0x3db4`) where `S = [x24+0x60]`, then published as tag `f0006` with count 2 by `bl 0x0166648c` into the CamX metadata publisher `0x1755430`. Containing function starts `0x01661f40`. **The value is runtime-derived, not a binary constant.** The nine previously recorded `movz`/`movk` sites are false positives and the six rodata dwords are tag-list interiors, not value sources; full detail and the ranked patch candidates are in the address book above. Faz 3.3 owns the confirming single-word patch and the `dumpsys` read. |
| OQ-02 | Does the HAL deliver remosaiced Bayer or raw Quad-Bayer at 8192x6144? | open | never captured — no successful full-res RAW frame yet |
| OQ-03 | Can `pixelArraySize` be raised without breaking other consumers? | answered | **Answered for the consumers actually tested (IMPL-22 / Faz 3.4), not in general.** With the word applied on both the stock and fullres bases: the stock camera opens with live preview and captures an unchanged `3072x4096`; Open Camera captures **`8192x6144` = 50.3 MP** on the fullres base, preserving `EV-04`; 1080p60 (`1920x1080 @ 60.1`) and 4K60 (`3840x2160 @ 60.0`) both record and play in two modes; `dcgA` and the HAL-layer `50mp` mode both open; and a controlled fixed-position comparison shows **no field-of-view change**. Scope is three applications, two video profiles and two of ten modes — **not** a general compatibility claim. The one failure seen (`dcgB`) reproduces **without** the change and is `FIND-3.4-02`. AGC was deliberately not tested; that is Faz 3.5. Record: `docs/consumer-survey.md`. |
| OQ-04 | Is the 10-bit/12-bit mismatch the *only* obstacle to 50 MP + LN composition? | answered | **Measured by IMPL-15 on 2026-08-31, and the answer is yes for DCG.** With `dcgB` + mode 0 moved to 12-bit mounted under the `fullres` HAL, the camera opened without a Gcam NPE, preview was live in both AGC and OpenCamera, and OpenCamera captured a valid **8192x6144 / 50.3 MP** frame with no corruption. Nothing beyond the bit-depth mismatch had to move. Two limits on the claim: the tested sensor layer is **DCG (`dcgB`), not LN** — `ln2`/`ln4` were not composed, and they independently crash AGC (`FIND-2.3-02`); and the composed frame is **visually indistinguishable** from the same shot at `50mp` alone, so the composition is *reachable* but showed no measured quality gain in a dark, flat scene. |
| OQ-05 | Is patch application atomic against power loss mid-write? | answered | No, and it does not need to be. `halpatch.sh:66-77` `hal_write` applies each entry with a separate `dd conv=notrunc`, so writes are **ordered, not atomic**. The target is `$MODDIR/active_hal/camera.qcom.so` (`halpatch.sh:30`), a module-private copy — never the live `/odm/lib64/hw/camera.qcom.so`. A partial write is **detected**: `hal_state` (`:80-87`) md5-classifies the copy and returns `unknown` when it matches neither known value. It is **recovered**: `hal_set` (`:97-99`) calls `hal_seed` on `unknown`/`none`, which re-copies the device's stock binary and verifies it (`:106-116`). `hal_set:101` re-verifies md5 after every write, so a failed `dd` cannot be reported as success. `hal_write` has exactly one caller (`:100`), which verifies. |
| OQ-06 | Does the WebUI pass any user input into a shell invocation? | answered | No. Exhaustive trace of `webroot/index.html`: exactly **four** `exec()` call sites — `:268` (`ACT + ' info'`), `:300` (`exec(cmd)` inside `run()`), `:332` (`ACT + ' lang ' + lang`), plus the definition at `:193`/`:204`. `run()` has exactly **two** callers: `:317` (`ACT + ' toggle ' + id`) and `:325` (`ACT + ' set ' + id`), where `id` iterates the source-literal arrays `MAIN_MODES` (`:187`) and `EXTRA` (`:188`). `lang` at `:330` reads `dataset.lang` from the two static buttons at `:98-99` (`en`/`tr`). `ACT`/`MODDIR` are string literals (`:122-123`). No `exec` argument has a user-controllable component. Backstop: `action.sh:108-114` `valid()` whitelists the mode against a fixed ten-element list before `:131` interpolates it into `sh -c`. |
| OQ-07 | Does `customize.sh` normalize `mode` and `active/` at install time? | answered | No — and the shipped archive makes it moot. `customize.sh` (78 lines, read in full) contains **zero** writes to `mode`; the only writer in the module is `setmode.sh:204`. But `unzip -Z1` on `ishtar-cam-modes-v2.1.zip` and `v2.0.zip` shows neither ships `mode`, `lang`, `active/`, or `active_hal/` — packaging already excludes runtime state. On first boot `post-fs-data.sh:14` reads an absent file, `MODE` is empty, and the `*)` arm at `:23-27` defaults to `stock`. **`AUTOPSY-P3-03` is contradicted for the shipped artifact.** The residual defect is the claim at `customize.sh:62` ("guncellemede mevcut mod"), which nothing implements — see FIND-1.5-01. |
| OQ-08 | Does `ishtar-cam-modes` ship its own `sepolicy.rule`? | answered | No. `find` over the source tree returns no `*sepolicy*` and no `*.rule` at any depth, and `unzip -Z1` confirms neither `v2.1` nor `v2.0` carries such an entry. The module relies on `chcon u:object_r:vendor_file:s0` applied to the bind-mount source instead (`post-fs-data.sh:70`, `halpatch.sh:114`, `setmode.sh:255`): the mounted file is relabelled to the context the camera stack already expects, so no policy rule is needed. |
| OQ-09 | Does any released zip already contain `debug.keystore`? | answered (no) | Faz 1.2 audit, 2026-08-24: all five archives listed by entry name; zero `.keystore`/`.jks`/`.p12`/`.pem`/`.key` entries and zero entries at the 2,664-byte keystore size. Adjacent finding: the keystore password ships in plaintext inside `tile-app/build.sh` in v1.9/v2.0/v2.1 (see invariant 9c, `DEC-10`). |
| OQ-10 | Does the device's live state match the workspace `mode` file (`stock`)? | answered (no) | Faz 2.1 smoke run 2026-08-30: device is on `dcgB`, workspace file says `stock`. The workspace file tracks the last host-side edit, not the device. |
| OQ-11 | Why is the `tiles hide` option ineffective? | open | observed ineffective; cause never diagnosed |
| OQ-12 | Which framework camera index maps to which physical sensor across all lenses? | partially_answered, and the previous answer is now in doubt | Faz 2.1 measurement 2026-08-30 contradicts the stored shorthand: `dumpsys media.camera` maps framework device 3 to HAL id 9, which is **Front**-facing at 3264x2448 and cannot be the rear main. The rear IMX989 array sits on HAL id 0 and ids 2-7 and 10. Full per-device table in section 3. See `OQ-17`. |
| OQ-13 | Are `Lddl;->P/Q` blocklists relevant to resolution filtering? | answered | **No** — both empty; hypothesis rejected |
| OQ-14 | Does the port have a working 48M mechanism? | answered | **No** — `Forty8Strip` is an identity stub; hypothesis rejected |
| OQ-15 | Why did AGC cap at 12.6 MP? | answered | `getOutputSizes()` high-resolution bucket exclusion (invariant 7), not a blocklist or a flag |
| OQ-16 | Why did the Faz 4 wide patch break AGC? | answered | same invariant as Faz 12, opposite direction (invariant 6) |
| OQ-17 | Which HAL camera id is the one the 16-point `fullres` patch actually modifies, and which one does AGC open? | partially_answered | Raised by the Faz 2.1 smoke run 2026-08-30; **answered by IMPL-12 on 2026-08-31** by the `fullres`-vs-baseline smoke diff it proposed. The patch modifies **all thirteen** camera ids, Front-facing included, not one — per-id deltas in section 3. Faz 4.1 must therefore size its guard for device-wide reach and cannot name a single target array count. **Which id AGC opens is still unmeasured** and stays open. Row updated by Faz 5.1, the first sub-plan since IMPL-12 whose boundary covers this file. |
