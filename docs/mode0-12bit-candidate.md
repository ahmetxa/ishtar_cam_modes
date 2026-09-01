# Mode-0 12-bit candidate blob

Generation and verification record for **Faz 5.1**. Host-side only; no device
interaction occurred while producing anything in this file.

The candidate is the artifact **Faz 5.2** mounts temporarily. It is deliberately
**not** in `ishtar-cam-modes/blobs/`, so no mode switch can select it.

## 1. What this changes and why

Sensor mode 0 is the 50 MP full-resolution mode, 8192x6144. It is absent from
`FOTO_MODLARI` (`ishtar-cam-modes/tools/ln_multimode.py:235`), so **no shipped
variant has ever touched it**. Every DCG and `*f` LN variant nonetheless raises
the *global* white level from 1023/64 to 4095/256, because white and black level
live in `sensorDriverData` and are not per-mode fields.

The result is the state Project-Ontology invariant 4 describes: in `dcgB`, mode 0
still emits 10-bit under a 12-bit white level. That mismatch is why
`post-fs-data.sh:16-18` and `setmode.sh` force the sensor layer back to stock
whenever `50mp` is selected, and therefore why the two layers exclude each other.

This candidate moves mode 0 alone to 12-bit, making it coherent with the global
level `dcgB` already sets. Nothing else changes.

## 2. Base blob, and why it is `dcgB` rather than `stock`

| | |
|---|---|
| Base | `ishtar-cam-modes/blobs/dcgB.bin`, md5 `ee73da4e8f4f542161e7faa2a8a2141e` |
| Candidate | `ishtar-cam-modes/candidates/dcgB-m0-12bit.bin`, md5 `80b53215356c57b156f2bb2918cf067a` |
| Generator | `ishtar-cam-modes/tools/mode0_12bit.py` |
| Command | `python tools/mode0_12bit.py blobs/dcgB.bin candidates/dcgB-m0-12bit.bin` |

`Faz5.1` section 9 names `blobs/stock.bin` as the differential reference. It is
used as such below (section 6c), and it is what `VAL-BASELINE` ran against. The
**base** for generation is `dcgB.bin` instead, for a reason worth stating rather
than burying:

a `stock` + mode-0-12-bit blob would carry a 12-bit mode 0 under a **1023** white
level. It would be internally incoherent, and it would contain no DCG layer at
all, so mounting it alongside the `50mp` HAL would test nothing that plain
`stock` + `50mp` does not already test. `dcgB` is the variant the project
recommends (`Kullanim.txt:18-34`, ">>> ONERILEN <<<") and the one whose global
level creates the exclusion in the first place. Composing *that* with the 50 MP
HAL layer is what Phase 5 exists to attempt.

The deviation is confined to the choice of base. Every acceptance criterion in
`Faz5.1` section 8 is met against it, and section 6c below additionally proves
the candidate's delta from `stock` is exactly `dcgB`'s delta plus mode 0.

## 3. Bit-depth encoding, read from real blobs

Read on 2026-08-31 with `ln_multimode.Sensor`, not taken from the register
specification (`Faz5.1` acceptance criterion 2):

| | 10-bit | 12-bit |
|---|---|---|
| `0x0112` / `0x0113` | `0x0A` | `0x0C` |
| `streamConfiguration` +8 (`dt`) | `0x2B` (MIPI RAW10) | `0x2C` (MIPI RAW12) |
| `streamConfiguration` +28 (`bpp`) | 10 | 12 |

Sources: 10-bit from `stock` mode 0 and `dcgB` mode 0; 12-bit from `dcgB`
modes 1 and 14.

## 4. The implied register set, justified by comparison

`Faz5.1` F5.1-03 asks whether bit depth alone is enough. Comparing `dcgB` mode 0
(10-bit, untouched) against `dcgB` mode 1 (12-bit, patched) shows the patched
mode differs in more than the format registers — but **that comparison bundles
two transforms**: the 10-to-12-bit format change *and* the DCG enable
(`0x321C` 0 to 2) with its PLL retune (`0x0307`, `0x030D`, `0x030E`, `0x030F`).
Enabling DCG on mode 0 is not in scope; only the format change is.

The correct comparator is `ln_multimode.py`'s existing `r12` variant
(`VARIANTS`, line 245): *"LN yok, yalnizca 12-bit cikis ... Zamanlamaya hic
dokunmaz."* Its `apply_ln(m, ln=None, twelve_bit=True)` path is the bit-depth
transform in isolation, already used in shipped tooling. It does three things:

| Change | Justification |
|---|---|
| `0x0112`/`0x0113` `0x0A`->`0x0C`, `dt` `0x2B`->`0x2C`, `bpp` 10->12 | The encoding measured in section 3. |
| `llp` scaled by 12/10, rounded up to a multiple of 16, written to `0x0342`/`0x0343` **and** `resolutionData` field 12 | A RAW12 stream needs 20% more line time to fit MIPI. `ln_multimode.py:196-199` records this as **verified on device**: without it the stream never arrives and preview stays black. |
| `fll` clamped to `FLL_MIN` = 3200 | **Rejected for mode 0 — see below.** |

**The `fll` clamp must not be applied to mode 0.** Every mode in `FOTO_MODLARI`
is at most 3,072 lines, so clamping frame length to 3,200 is safe there. Mode 0
is **6,144 lines**; 3,200 would be a frame length shorter than the frame itself.
Mode 0's stock `fll` of 8,728 already exceeds its height, so the correct action
is to leave field 13 untouched. `tools/mode0_12bit.py` does that, and guards it
with an explicit `fll < height` precondition check.

This is the one substantive finding of F5.1-03: reusing `apply_ln` unmodified on
mode 0 would have produced a structurally valid blob with corrupt frame timing —
passing every integrity check while being wrong.

## 5. Applied change set

Guards checked before applying, all passed: `0x0112`/`0x0113` both `0x0A`;
stream `dt` `0x2B` and `bpp` 10; `resolutionData` field 12 equal to the
register-derived `llp`; `fll` at least the frame height.

| Field | Before | After |
|---|---|---|
| `0x0112` | `0x0A` | `0x0C` |
| `0x0113` | `0x0A` | `0x0C` |
| `0x0342` (LINE_LENGTH_PCK hi) | `0x36` | `0x40` |
| `0x0343` (LINE_LENGTH_PCK lo) | `0x00` | `0xD0` |
| `resolutionData` field 12 (`llp`) | 13824 | 16592 |
| `streamConfiguration` +8 (`dt`) | `0x2B` | `0x2C` |
| `streamConfiguration` +28 (`bpp`) | 10 | 12 |
| `resolutionData` field 13 (`fll`) | 8728 | **8728, unchanged** |
| `sensorDriverData` white / black | 4095 / 256 | **4095 / 256, unchanged** |

`llp`: `ceil16(13824 * 12 / 10)` = 16592, a ratio of 1.2002.

## 6. Verification

### a. `VAL-BASELINE` and `VAL-BLOB`

`python tools/verify_ln.py` passes against `stock.bin` and all eight variants
before the candidate was judged. Its `parse()` asserts the header signature, the
`0x1C` size field, and the trailing CRC32 on every blob it loads.

Against the candidate, all three integrity checks pass:

| Check | Result |
|---|---|
| `QTI Chromatix Header` signature | OK |
| `0x1C` size field | OK, 1062246 equals len minus 4 |
| trailing CRC32 | OK, `c63d473f` |

### b. `VAL-SIZE`

**1,062,250 bytes**, exactly the figure `setmode.sh`'s `EXPECT_SIZE` and
`post-fs-data.sh` enforce.

### c. `VAL-DIFF` — changes confined to mode 0

**Per-mode snapshot, candidate vs `dcgB`.** One mode changed: `[0]`. Twenty-two
modes identical: `[1..22]`. Globals unchanged at 4095 / `[256,256,256,256]`.

```
dcgB   mod 0  8192x6144 dt=0x2B bpp=10 llp=13824 fll=8728  0x0112=0x0A 0x0113=0x0A 0x0342=0x36 0x0343=0x00 0x31A4=0
cand   mod 0  8192x6144 dt=0x2C bpp=12 llp=16592 fll=8728  0x0112=0x0C 0x0113=0x0C 0x0342=0x40 0x0343=0xD0 0x31A4=0
```

**Byte-range differential, candidate vs `dcgB` — 8 ranges, 16 bytes total.**
Every range is named:

| Range | Bytes | Before to after | Owner |
|---|---|---|---|
| `0x000C3C..0x000C3D` | 2 | `d140` to `4c00` | table #48 offset field, `0x0112` value redirect |
| `0x000CF0..0x000CF1` | 2 | `d140` to `4c00` | table #51 offset field, `0x0113` value redirect |
| `0x000E58..0x000E59` | 2 | `d940` to `1f01` | table #57 offset field, `0x0342` value redirect |
| `0x000F0C..0x000F0D` | 2 | `690c` to `5130` | table #60 offset field, `0x0343` value redirect |
| `0x0D494D..0x0D494E` | 2 | `0036` to `d040` | `#32 resolutionData`, mode 0 field 12 |
| `0x0D6475` | 1 | `2b` to `2c` | `#36 streamConfiguration`, `dt` |
| `0x0D6489` | 1 | `0a` to `0c` | `#36 streamConfiguration`, `bpp` |
| `0x103566..0x103569` | 4 | `017f13e1` to `c63d473f` | trailing CRC32 |

The `0x1C` size field is not in the list: the file length is unchanged, so
`seal()` rewrote the same value.

**Shared-entry check.** The four register changes are *offset redirections* of
table entries, not writes into the data region. A redirected entry shared with
another mode would silently change that mode too, which the 5-register snapshot
above would not catch. Checked directly: entries #48, #51, #57 and #60 are each
referenced by **mode 0 only**.

**Full per-mode comparison.** Every `regSetting` register of every mode, the
whole 304-byte `resolutionData` record, and the whole `streamConfiguration`
entry, compared across all 23 modes: **only mode 0 differs**. The 708-byte
`sensorDriverData` block is byte-identical.

**Decomposition against `stock`.** `stock` to `dcgB` is 84 byte ranges touching
modes `[1,2,7,10,14,15]`. `stock` to candidate is 91 ranges touching
`[0,1,2,7,10,14,15]`. The set difference is exactly `{0}`, and the 7 added
ranges are precisely the mode-0 ranges tabulated above. The candidate is
`dcgB` plus a mode-0 change and nothing else.

## 7. What this does not establish

- **Nothing here says the composition works.** `OQ-04` / `H-04` remain open:
  the bit-depth mismatch may not be the only obstacle. Faz 5.1's goal is a
  correct blob, not a working composition, so a structurally sound blob is a
  success here regardless of what Faz 5.2 finds.
- **No device has run this blob.** Every figure above is host-side.
- **This will not fix the AGC video regression.** `FIND-2.3-03` records the
  video section black in four states including plain `stock`, and `50mp` + LN
  has never been reachable on this device. Phase 5 must not be judged by it.
- The `fll` decision is reasoned from the frame geometry and guarded, but
  8,728 lines at the new 16,592-cycle line length has not been shown to be a
  valid readout timing on hardware. Faz 5.2 is where that becomes observable.

## 8. Faz 5.2 outcome — the composition works

Executed 2026-08-31 (IMPL-15) with the user's explicit approval, since the test
deliberately runs the camera in the combination the module forbids.

**Result: the two layers are not physically exclusive.** With the candidate
mounted under the `fullres` HAL, the camera opened, preview was live in both
AGC and OpenCamera, and OpenCamera captured **8192x6144 = 50.3 MP**. The
historical corruption symptom did not reproduce: no green cast, no pink
banding, no torn or repeated rows.

| Check | Result |
|---|---|
| Both layers active together | sensor `80b53215…` + HAL `fe0245a4…` `fullres`, mount counts 1 / 1 |
| `camera.hal0` | 456 rows, all seven 8192x6144 entries present |
| AGC opens | `topResumedActivity=CameraLauncher`, crash buffer empty, no `CONFIG failed` |
| Preview | live, confirmed visually |
| Capture | `IMG_20260831_221747.jpg`, 8192x6144, 50.3 MP, clean |
| Comparison at `50mp` alone | `IMG_20260831_221904.jpg`, 8192x6144, visually indistinguishable |
| Restoration | post-test snapshot differs from pre-test on two `prefs.trap.*` lines only |

**What it does not show.** The sensor layer tested was **DCG, not LN** —
`ln2`/`ln4` crash AGC independently (`FIND-2.3-02`), so composing them would
confound the result. And the composed frame is indistinguishable from `50mp`
alone (file sizes 2,669,862 vs 2,674,023 bytes, 0.16% apart) in a dark, flat
scene: the composition is *reachable*, not yet shown to be *better*.

### The procedure, as reviewed before execution

The mount is a **content rewrite, not a second bind mount**: `setmode.sh:251`
changes the contents of the already-mounted inode `$MODDIR/active/$BIN` and
leaves the mount alone. Reproducing that keeps the mount count at 1 and makes
restoration a rewrite. The helper reproduced `setmode.sh`'s `EXPECT_SIZE`
guard, its post-write md5 verification, and the client-before-HAL restart
ordering of `setmode.sh:47-91` (invariant 3), and did **not** touch the HAL.

```
setmode.sh 50mp                  # HAL -> fullres; sensor forced to stock
                                 # (this is the exclusion, observed live)
push candidate -> /data/local/tmp/cand.bin ; verify md5 + size on device
compose.sh apply /data/local/tmp/cand.bin
    guard: size == 1062250, bind mount present
    cat cand > $MODDIR/active/$BIN ; chown/chmod/chcon ; sync
    verify md5 at /odm/lib64/camera/<bin> == candidate, abort on mismatch
    restart: stop cameraserver -> stop providers -> force-stop cam apps
             -> start providers -> start cameraserver -> wait list -> sleep 5
setmode.sh stock                 # restore both layers through tested code
```

Because `mode.file` still read `50mp` for the whole test, a reboot alone would
have re-asserted the stock blob through `post-fs-data.sh:16-18`. The experiment
self-heals, which is what made it reasonable to run at all.

## 9. Faz 5.3 disposition — proven, deliberately not adopted

Decided 2026-08-31 (IMPL-17), by the user, on the evidence in section 8.

**The exclusion rule stays.** This candidate is **not** promoted into
`ishtar-cam-modes/blobs/`, so no mode switch can select it, and no dispatch
logic was changed. Three measured reasons:

1. **No demonstrated benefit** — the composed frame is visually
   indistinguishable from `50mp` alone (0.16% file-size difference).
2. **DCG only** — the combinations the roadmap names, `50mp`+`ln2` and
   `50mp`+`ln4`, cannot be validated because those modes crash AGC on their own
   (`FIND-2.3-02`).
3. **Removal is a state-model change, not a dispatch edit.** The exclusion is
   enforced as *logic* in only two of six surfaces (`post-fs-data.sh:15-27`,
   `setmode.sh:177-192`). The other four assume it: `action.sh:94-104`
   `active()` is HAL-first and would report a composed state as `50mp` without
   ever reading the sensor layer, and both UIs render "on" by string equality
   against a single current-mode value. A six-line edit would produce a
   capability the system **misreports** — see `ARC-03`.

**This is not a retirement.** The candidate and `tools/mode0_12bit.py` are kept
precisely so adoption stays cheap. What is settled is the *mechanism*: the
layers compose and produce a clean 50.3 MP frame. What is missing is a
demonstrated *benefit*. **Re-open invariant 4 on new evidence of benefit, not of
mechanism.**

A useful next probe, if the question is revisited: compose `ln2f`/`ln4f` with
mode 0 at 12-bit and capture through **OpenCamera**, which does not use Gcam and
so is not subject to the `ln2`/`ln4` AGC crash. That would test the LN half of
`H-04` without the confound.
