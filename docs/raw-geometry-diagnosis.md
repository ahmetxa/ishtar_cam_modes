# RAW Payload Geometry Diagnosis

Owner: `Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md`
Produced by: Step 4 implementation session, 2026-09-01, `IMPL-31`
Tool: `agc-50mp-yama/tools/frame_geometry.py` (`VAL-GEOMETRY`)
AGC build under test: patched `ce65f862c990e2acc02be356f75a7122`, not stock (`VAL-PRECOND` item 7)

This document records what the corrupt AGC full-resolution frame **is**. It does
not record why the pipeline produces it; that question is routed in section 8
rather than answered, per `Faz4.6` section 5 and the `FIND-4.5-02` posture.

---

## 1. Verdict

**The row-pairing model is CONFIRMED.** The frame is a payload of **half the
negotiated buffer width** written linearly into a raster read back at the **full**
negotiated width, with the remainder of the buffer left at pure black.

It is confirmed on **three independent captures**, across **two different HAL
states** and **two different raster sizes**, and against an **inverse control**
that reproduces the artifact's signature from a known-good frame and round-trips
byte-identically. No measured feature is unexplained by the model.

`FIND-4.5-02` closes. `FIND-3.5-01` does **not** close — its stated cause is now
replaced by a measured one, but the fault itself is unfixed and no patch has been
identified. See section 8.

---

## 2. Provenance of the artifact under analysis (`F4.6-01`)

**Route taken: pulled, not re-captured.** The original survived on the device and
no new exposure was needed, so the analysis is pixel-comparable with the frame
`IMPL-30` described.

| | Value |
|---|---|
| Device path | `/sdcard/DCIM/Camera/AGC_20260901_211108200.jpg` |
| Host copy | `snapshots/20260901-1950__Faz4.6__f4509-capture-artifact-ORIGINAL.jpg` |
| Size on disk | 2,176,443 bytes |
| Dimensions | **6144x8192**, read from the SOF0 marker (`VAL-CAPTURE`) |
| EXIF DateTime | `2026:09:01 21:11:08` local, = 18:11 UTC |
| EXIF Software | `HDR+ 1.0.414775603ndh` |

The 18:11 UTC timestamp matches the `f4509` label on
`snapshots/20260901-1811__Faz4.5__f4509-capture-artifact.png` to the minute, which
is what ties this file to the `IMPL-30` capture. That PNG is the 512x682 downscale
and remains in the tree as the shape record only; **it was not analysed**, per the
`Faz4.6` scope rule.

Two further captures were recovered and analysed as corroboration:

| File | SOF | State at capture |
|---|---|---|
| `AGC_20260901_211031502.jpg` | **3072x4096** | seven-word stack, 37 s before the primary (see the correction note below) |
| `AGC_20260901_153736507.jpg` | **6144x8192** | three-layer stack, `IMPL-23` era |

Both are retained: the first as
`snapshots/20260901-1950__Faz4.6__halfres-capture-artifact-ORIGINAL.jpg`, the
second by its reconstruction only.

---

## 3. Axis mapping (`F4.6-02`)

The encoded frame is **rotated 90 degrees from the sensor raster**, and this is
established from the file rather than assumed:

- SOF0 declares **6144x8192** — the encoded pixels are portrait.
- EXIF `ImageWidth`=**8192**, `ImageLength`=**6144** — the raster is landscape.
- EXIF `Orientation`=**1**, so no viewer-side rotation is pending. AGC rotated the
  pixels themselves at encode and left the raster figures in the tags.

Therefore:

| JPEG axis | Sensor raster axis |
|---|---|
| height, 8192 | the **row direction** — 8192 samples across one raster row |
| width, 6144 | the **row count** — 6144 raster rows |

`EV-38` was stated in JPEG axes. Restated in raster axes it reads: the content
occupies the **first quarter of the raster rows**, at the **full 8192 extent**
along each of those rows, and the two colour-cast strips lie **side by side**
(left/right in raster axes), not stacked. Every figure below is in raster axes.

---

## 4. Measured structure against prediction (`F4.6-03`)

Primary artifact, `AGC_20260901_211108200.jpg`, raster 8192x6144:

| Feature | Predicted | Measured | Verdict |
|---|---|---|---|
| Pure-black fraction | 0.7500 | **0.7495** | hit, see note |
| Content band | rows 0..1535, 1536 rows | rows 0..1538, 1539 rows | hit, see note |
| Column extent of content | full, 0..8191 | **0..8191** | exact |
| Colour casts, left half | distinct | R/G=**1.475** B/G=**1.051** | two distinct triples |
| Colour casts, right half | distinct | R/G=**1.243** B/G=**1.353** | two distinct triples |
| White edge band | not predicted | rows 0..689, 690 rows | part of the scene |

**The 3-row overshoot is a lossy-encode artifact, not a model miss, and this was
tested rather than asserted.** Row-mean luminance across the boundary decays
monotonically:

```
row 1534  mean=115.000     row 1537  mean=  8.000
row 1535  mean= 25.000     row 1538  mean=  2.000
row 1536  mean= 16.000     row 1539  mean=  0.000
```

That is DCT ringing at a hard edge. True content ends at row 1534. The inverse
control in section 6, which is lossless PNG throughout, lands on **exactly**
4608/6144 = 0.7500 and **exactly** rows 0..1535 — so the deviation is attributable
to JPEG encoding and to nothing in the model.

The two colour casts are now numbers rather than adjectives: the left half is
red-dominant with neutral blue (R/G 1.475, B/G 1.051); the right half is
blue-dominant and less red (R/G 1.243, B/G 1.353). `EV-38`'s "upper red/pink,
lower purple/magenta" is the same observation in JPEG axes.

---

## 5. Reconstruction (`F4.6-04`)

The reconstruction re-reads the content band's bytes at half the raster width.
This is exact rather than approximate: splitting every raster row at its midpoint
and emitting the two halves as consecutive rows leaves the linear byte stream
untouched, so un-folding is a re-interpretation of the same bytes, not a
permutation of them.

**Result: YES, coherent, on all three captures.**

| Capture | Raster | Content band | Reconstructed | Coherent |
|---|---|---|---|---|
| `AGC_..._211108200` (seven-word) | 8192x6144 | 1539 rows | **4096x3078** | **yes** |
| `AGC_..._211031502` (seven-word) | 4096x3072 | 770 rows | **2048x1540** | **yes** |
| `AGC_..._153736507` (three-layer) | 8192x6144 | 3081 rows | **4096x6162** | **yes** |

Evidence retained:

- `snapshots/20260901-1950__Faz4.6__recon-fullres-payload.jpg`
- `snapshots/20260901-1950__Faz4.6__recon-halfres-payload.jpg`
- `snapshots/20260901-1950__Faz4.6__recon-preraise-payload.jpg`

Coherence is judged on continuity, not on impression: in each reconstruction the
scene edges run unbroken across the full reconstructed width, there is no seam at
the former fold column, and the scene is recognisable. The primary reconstruction
resolves to a wall, a desk edge and a cable; the half-resolution one to a room
interior with a ceiling, a wall and cushions; the pre-raise one to a room with a
ceiling, an arm and a chair, with handheld motion smear that is a property of the
exposure and not of the geometry.

**The two casts are per-payload-row, which is the fourth constraint discharged.**
Splitting the primary reconstruction into even and odd rows returns
R/G=1.475 B/G=1.051 and R/G=1.243 B/G=1.353 — the same two triples as the left and
right halves of the folded band, to the last digit. So the folded frame's two
side-by-side casts are alternate payload rows, which is what opposite CFA phase on
consecutive Bayer rows produces.

---

## 6. Inverse control (`F4.6-04`)

Required so a positive result is read against a reference rather than against
expectation.

Source: `IMG_20260901_154247.jpg`, the Open Camera capture behind `EV-33`, clean at
8192x6144, resampled to a known-good 4096x3072 payload. Folded to 8192 width and
padded into an 8192x6144 raster, then measured with the same code path as the
artifact.

| Feature | Control measured | Artifact measured |
|---|---|---|
| Pure-black fraction | **0.7500** | 0.7495 |
| Content band | rows 0..1535 (**1536**) | rows 0..1538 (1539) |
| Column extent | 0..8191 | 0..8191 |
| Visual signature | two side-by-side vertically-squashed copies | same |
| Left/right casts | R/G 1.097 / 1.097 — **identical** | 1.475 / 1.243 — **differ** |
| Unfold round-trip | **byte-identical**, 37,748,736 bytes | n/a |

Retained as `snapshots/20260901-1950__Faz4.6__control-folded-known-good.jpg`.

Two things the control establishes that the artifact alone could not:

1. The fold **is** the structure. A known-good frame folded this way is
   indistinguishable in shape from the artifact, and unfolding recovers it
   byte-for-byte.
2. The fold **does not** create the colour difference. The control's two halves
   have identical channel ratios, because a decoded RGB image carries no CFA
   phase. The artifact's halves differ. So the two casts arise in the **raw**
   domain, before demosaic — which is independent support for the model rather
   than a separate unexplained feature.

---

## 7. The scale relation, and what it rules out

Across the three captures the payload width is always **exactly half** the raster
width. The payload **height** is not constant:

| Capture | State | Raster | Payload | W ratio | H ratio | Black |
|---|---|---|---|---|---|---|
| `..._153736507` | three-layer | 8192x6144 | **4096x6144** | 1/2 | **1/1** | 50% |
| `..._211108200` | seven-word | 8192x6144 | **4096x3072** | 1/2 | **1/2** | 75% |
| `..._211031502` | seven-word | 4096x3072 | **2048x1536** | 1/2 | **1/2** | 75% |

Two consequences, both load-bearing.

**(a) It reconciles a discrepancy the record left open.** `IMPL-23` described
"exactly half the frame black" and `IMPL-30` measured 75%; `IMPL-30` recorded the
disagreement, declined to resolve it, and claimed no regression. Both figures are
now confirmed correct **for their own state**: 50% before the active-array raise,
75% after. The record was right to refuse to reconcile them from description
alone.

**(b) It removes `80340003` as a candidate on evidence, not on decision.** The
vendor tag holds a **fixed** rect `[0 0 4096 3072]`. The fault is **proportional**:
at a 4096x3072 raster the payload is 2048x1536, which a fixed 4096x3072 rect cannot
produce. A fixed crop also cannot produce a payload whose height ratio changes
between two states while the tag is unchanged. `DEC-13`'s choice not to spend a
scope expansion on the vendor-tag provider is therefore **vindicated by
measurement**, which is a stronger position than the one it was taken from.

**The height change is an observation, not an attribution.** The three-layer and
seven-word captures differ in more than the two active-array words: different
session, different scene, and `IMPL-30` set `pref_48m_key=1`. The one-variable rule
in `docs/phase3-preconditions.md` section 5 item 3 is not satisfied, so this
document does **not** claim the raise halved the payload height. It records that
the payload height ratio differs between the two states and routes the attribution
to a live probe. See section 8.

---

## 8. Routed consequences (`F4.6-08`)

Nothing below is acted on here. Each item names an owner or is raised as a
decision, per `Faz4.6` section 5.

| # | Item | Disposition |
|---|---|---|
| 1 | **`FIND-4.5-02` verdict** | **CLOSED.** The frame is a half-width payload linearly written into a full-width raster. Confirmed on three captures with an inverse control. |
| 2 | **`FIND-3.5-01` disposition** | **REMAINS OPEN.** Its stated cause is replaced by a measured one and its three-tag account is superseded, but the image is still wrong and no patch is identified. It closes when the payload fills the buffer. |
| 3 | **The new question: why is the payload half-width?** | **NEW, unowned.** Candidates: the sensor is delivering a 2x2-binned frame while the buffer is configured full-size; the remosaic path is configured at half extent; or the stride is negotiated from a stale rect. This is `F4.6-06`'s target and is not answerable from an image. **Raised to the user as a new decision on scope**, since it may require a write-site search and `DEC-06`'s allowance stands at 9 of 15. |
| 4 | **Payload height ratio differs between HAL states** | **ROUTED to `F4.6-05`/`F4.6-06`.** Must be established under the one-variable rule before any attribution to the active-array raise. If the raise did halve the payload height, that is a regression and belongs alongside `FIND-4.5-01` in `Faz4.4`. |
| 5 | **`80340003` / vendor-tag provider** | **CLOSED by evidence.** Section 7(b). Do not reopen without a measurement that contradicts the proportionality. |
| 6 | **CFA phase (`H-03`)** | **STRENGTHENED, not settled.** The two casts are alternate payload rows and the control shows the fold alone cannot create them. The discriminating probe is still the full-resolution DNG, still gated on `Faz4.1` per `EV-35`. |
| 7 | **Preview/still split (`EV-39`)** | **CONSISTENT.** A preview stream negotiates a small buffer that a half-size payload fills, so preview is correct while the still is folded. Supports the model; not independent evidence for it. |

---

## 9. Work items not run in this session

| Item | Why | Gate |
|---|---|---|
| `F4.6-05` consumer control | Live. Needs the seven-word stack re-applied, a camera restart, and shutter presses. | User approval and device |
| `F4.6-06` HAL configuration read | Live. Needs filtered logcat during a capture in the seven-word stack. | User approval and device |
| `F4.6-07` DNG probe | Gated. `EV-35`: no full-resolution DNG exists before `Faz4.1` lands format-32 emission. | `Faz4.1` |

`F4.6-05` and `F4.6-06` are now **better specified** than when they were written:
`F4.6-06` should read the negotiated buffer **stride** and the **binning state**
specifically, because the model predicts a source width of exactly half the
buffer width, and that is a number the log either carries or does not.

Pre-existing captures were checked as free corroboration and are **not** the
`F4.6-05` control: the stock camera's 18:46 captures are 4896x6528, a different
mode, and the Open Camera 15:42 capture is the three-layer `EV-33` reference, not
the seven-word stack.

---

## 10. Budget and device state

**`DEC-06` allowance consumed: none.** It stands at **6 of 15 consumed, 9
remaining**, exactly as `IMPL-30` left it. This session reached no patch decision
and examined no candidate write site, so no allowance was spendable.

**Device state unchanged.** Every device operation in this session was a
read-only `adb pull`. No patch was applied, no preference was written, no camera
was restarted, and no reboot occurred. The device remains at
`BASELINE-2026-08-31-V21`. No `scripts/smoke.sh` bracket was required, because
`docs/phase3-preconditions.md` section 5 item 2 brackets device **changes**, and
there was none.


---

## 11. Correction: the artifact state is the SEVEN-word stack (`IMPL-33`, 2026-09-02)

This document originally labelled the `21:10` and `21:11` captures as the
*five-word* stack. That label is **wrong**, and it is corrected above.

The evidence is the bracket ordering, not a recollection. `IMPL-30`'s reverts
after `f0000` and after `f000a` are bracketed at `1756` and `1759`; the **full**
stack is bracketed at `1803__Faz4.5__full-stack.txt` carrying
`hal.live.md5 = c094101de0184e9216a57020873bac0b`; the teardown is at `1816`.
Both captures fall inside `[18:03, 18:16]` with **no intervening revert bracket**,
and the measurement contract requires a bracket around every device change. So
both were taken in the full stack.

The arithmetic agrees: raw50 (4 words) + pixelarray (1) + activearray (2) = **7**,
which is what `IMPL-30` recorded and what `IMPL-33` reproduced to the same md5. A
genuine five-word state (raw50 + pixelarray, no active-array raise) is coherent
and may have existed earlier in that session, but **no capture in hand belongs to
it**.

**Nothing in sections 1-10 changes.** Section 7(a)'s reconciliation still holds,
because the 50%/full-height reading comes from the *three-layer* capture, which is
genuinely pre-raise. Only the name on the two post-raise captures was wrong. The
correction matters because a reader reproducing "the five-word stack" would build
the wrong HAL and measure the wrong thing.

---

## 12. Live results (`F4.6-05`, `F4.6-06`) -- `IMPL-33`, 2026-09-02

State under test reproduced bit-for-bit: `fe0245a4...` (fullres) + 7 words ->
`c094101de0184e9216a57020873bac0b`, the md5 `IMPL-30` pre-committed. Trap cleared
to 0/12 before the captures. AGC build `ce65f862...`.

### `F4.6-05` -- the consumer control

| Consumer | Result | Black fraction | Extent |
|---|---|---|---|
| **Stock camera** | **CLEAN** | **0.0000** | rows 0..6143, cols 0..8191 of 8192x6144 |
| **AGC** | folded, as modelled | **0.7490** (0.7500 predicted) | content rows 0..770 of 4096x3072 |
| Open Camera | **not run** | -- | `pm` keeps no record of the package after three `Success` installs |

**The stock camera is clean at full 8192x6144 in the exact stack that folds AGC's
frame.** This is the result the sub-plan was written to obtain, and it is stronger
than `EV-33`: that reference only ever tested the three-layer stack, whereas this
tests the seven-word one. **The active-array raise did not break the HAL's own
still path, and the fault is confined to AGC's Gcam path.**

The AGC capture reproduces the fold **proportionally at a half-size raster**:
0.7490 black against 0.7500 predicted, content rows 0..770 against 768 predicted --
the same 3-row DCT overshoot section 5 characterises -- and unfolding at column
2048 gives a coherent **2048x1542** against 2048x1536 predicted. It came out at
4096x3072 rather than 8192x6144 because `pref_48m_key` was not set; `IMPL-23`
established AGC will not emit full resolution without it.

### `F4.6-06` -- what the HAL configured

**The stride is not on the log surface.** `stride` occurs **0** times in a
213,466-line all-buffer capture. Per this sub-plan's own instruction that is
recorded as a determination, and a scripted trace of the buffer-negotiation path
is **proposed, not assumed**.

What the log does carry:

| Reading | Value |
|---|---|
| Negotiated YUV (format 35) buffers | **8192x6144** (clean stock capture), **4096x3072** (folded AGC capture), 1440x1080 and 640x480 preview |
| QCFA / remosaic | `prepareNormalCapture: qcfa = false` on the clean 50MP stock capture |
| `static_metadata.cc:667` | 0 |
| `Stuck shot` | 0 |
| `libgcam` / `HdrPlusSession` | 32 / 2 |

**New, unrecorded, and the strongest lead this session produced:**

```
E native : mesh_warper_utils.cc:86] Invalid mesh: [4096,3072]
```

Twice, at 17:00:35.340 -- seconds after the AGC capture, **at exactly the buffer
dimensions that capture negotiated**. Gcam builds a warp mesh at the buffer size
and rejects it as invalid. This is a Gcam-internal rejection at the same
dimensions the fold is measured against, and it is the first evidence pointing at
*why* the payload is half-width rather than merely confirming *that* it is.

### What this does not settle

`EV-44` remains open. Attributing the payload-height halving to the active-array
raise still needs a **full-resolution** AGC capture in the seven-word stack, which
requires `pref_48m_key=1`. The one-variable rule forbids the attribution without
it.

---

## 13. `pref_48m_key` is necessary but not sufficient (`IMPL-35`, 2026-09-02)

`IMPL-33` left `EV-44` owed a full-resolution AGC capture in the seven-word
stack, because its AGC frame came out at 4096x3072 with `pref_48m_key` unset.
This run set the key and repeated the capture. **`EV-44` is still not
satisfied, and the reason is now measured rather than suspected.**

State under test, reproduced bit-for-bit again: `fe0245a4...` (fullres) + 7
words -> `c094101de0184e9216a57020873bac0b`. Trap cleared to **0/12** by per-key
audit immediately before the capture. `pref_48m_key=1` added as
`<string name="pref_48m_key">1</string>`, matching how the sibling keys
(`pref_raw_key`, `pref_fix_resolution_key`) are stored; `AGC;->
getSupportedOutputSizes` reads it through `AdvancedSettings.get48m()I` and
branches on `if-eqz`, so any non-zero value opens the patched path.

### The request reached full resolution. The output did not.

| Stage | Evidence | Result |
|---|---|---|
| AGC stream selection | `getImageReaderFormat ImageReaderFormat{ImageFormat=RAW10, Size=8192x6144}`, x4 | **8192x6144** |
| cameraserver configuration | `Bypass roundBufferDimensionNearest for privilegedClient YUV streams width 8192 height 6144 for format 35` | **8192x6144** |
| Photo size preference | `pref_camera_picturesize_back_key` = `8192x6144`, and it **held** across the session | **8192x6144** |
| libgcam frame acceptance | `shot_process.cc:392  PrepShot: Bad frame with all-zero green pixels` | **15 of 15 rejected** |
| Saved JPEG | SOF0, measured | **3072x4096 = 12.6 MP** |

**This is a real advance over `IMPL-33` and a real wall.** The application-side
blockage `IMPL-23` described is open: with the key set, AGC asks for RAW10 at
8192x6144 and cameraserver configures that stream without clamping it. The
metadata gate is also still clear — `static_metadata.cc:667`, `frame_raw_max`,
`matches neither` and `Stuck shot` all occur **0** times in 44,246 lines. What
fails is neither the request nor the metadata but the **frame content**: every
one of the fifteen candidate frames is rejected as all-zero green.

### The fallback output carries the same fold

Measured with `frame_geometry.py`, raster axes:

- pure-black rows **2302 of 3072**, fraction **0.7493** against 0.7500 predicted
- content confined to rows **0..769**, column extent full
- unfolding at column 2048 gives a coherent **2048x1540**

That is `IMPL-33`'s artifact reproduced, not escaped. The fallback path does not
recover a clean image; it produces the same half-width-payload fold at the
smaller raster. The user's description of the result was "blurry, about 12 MP",
which is what a 4096x3072 frame whose content occupies one quarter of the raster
looks like when viewed whole.

### `Invalid mesh: [4096,3072]` is reframed, not confirmed

The `IMPL-33` handoff flagged this as the first evidence for *why* the payload
is half-width. It is not. The message appears **twice in this capture and twice
in `IMPL-33`'s** — in the full-resolution-request run and in the half-resolution
run alike — and `[4096,3072]` is exactly
`org.codeaurora.qcamera3.quadra_cfa.activeArraySize (80340003)`, read live during
this session as `[0 0 4096 3072]`. That vendor tag is the one array the
seven-word stack does **not** raise: the stack raises `f0000`, `f0006` and
`f000a`, and `IMPL-30` recorded `80340003` staying at half. **The mesh error
tracks the un-raised vendor tag, and is a standing consequence of it rather than
a symptom of the payload halving.** It belongs to `FIND-4.5-01` and `F4.4-02b`,
not to the geometry diagnosis.

### What is not yet discriminated

`lib_aion_buffer.so` fails to load (`aion.cc:791`), which makes
`GetFileDescriptors not loaded` and then
`MapFrameToTexture: SABRE: Cannot get file descriptor from opaque_handle`, 15
times — once per frame. **`SABRE` appears in `IMPL-33`'s log excerpt too**, so it
is a standing condition of this AGC port and not something this run introduced.
Whether the all-zero-green verdict is caused by the payload layout or by frames
that were never successfully mapped is **not settled by this evidence**, and the
two are not separable from the log surface alone.

Honesty about the comparison: `IMPL-33`'s log survives only as a 37-line targeted
excerpt, which contains no `all-zero green` line. That is **not** evidence the
condition was absent then — the excerpt was filtered for other patterns. The
claim "all-zero green is new at full resolution" is **not** supported and is not
made here.

### Trap re-arm, observed a second time

`2/12` before -> `0/12` cleared -> **`2/12` after the capture session**
(`pref_raw_key`, `pref_fix_resolution_key`). This independently reproduces the
`IMPL-33` finding that the trap re-arms across an AGC session, and confirms the
sub-plan's rule that the per-key audit must be re-run immediately before every
measurement rather than trusted from an earlier reading. `pref_48m_key` itself
**survived** AGC's rewrite of the preference file.

`FIND-3.5-01` and `FIND-4.5-02` both remain **OPEN**. Nothing in this run is an
image fix.

## 14. The all-zero-green verdict is not caused by the SABRE mapping failure (`IMPL-36`, 2026-09-02)

Section 13 left one question explicitly undecided: whether the fifteen
`all-zero green` rejections were caused by the payload layout or by frames that
were never successfully mapped, `lib_aion_buffer.so` having failed to load. It
recorded that the two were "not separable from the log surface alone." **They
are separable, and they are now separated.** No new capture was required.

### `lib_aion_buffer.so` is absent from the port by construction

`libgcastartup.so` carries the literal dlopen name `lib_aion_buffer.so` next to
`wireless/android/camera/common/lib_aion/aion.cc`, `aion_context.cc` and
`scoped_power_boost.cc`, plus the two GPU consumers
`googlex/gcam/gpu/gles/aion_mapped_hardware_buffer.cc` and
`googlex/gcam/gpu/opencl/android/aion_mapped_image.cc`. The library itself ships
in **none** of the three APKs on hand — `AGC8.4.300_V9.6_50MP_patched`,
`V9.6_snap` and `V14_snap` carry 20, 20 and 21 `.so` files respectively for
`arm64-v8a`, and zero of them are an aion buffer library.

So `aion.cc:791` is a **standing deficiency of the port**, not a consequence of
any HAL patch, not something `IMPL-35` introduced, and not repairable from the
HAL side. This confirms the `IMPL-35` reading that `SABRE` is a standing port
condition, and supplies the reason.

### The verdict is a stored statistic, merely reported at `shot_process.cc:392`

Static reading of `libgcastartup.so` places the log site inside a reporter, not
inside a test. At `0x1ed882c` the emitting block is entered only by:

    ldr  w8, [x26, #0x708]
    cmp  w8, #3
    b.ne <skip>

`[x26+0x708]` is a small enum, bounded to `0..3` by the jump table at
`0x1ed81b8` (`cmp w13,#3 / b.hi`), read together with siblings at `+0x70c`,
`+0x710`, `+0x714` and `+0x718` behind a validity flag at `+0x71c`. The same
function reports, from the same block and all attributed to `PrepShot` in
`shot_process.cc`, this family of verdicts:

- `Non-empty frame with unknown sharpness score`
- `Non-empty frame with unknown sharpness measurement`
- `Non-empty frame with invalid sharpness measurement`
- `Overexposed frame with all green pixels saturated`
- `Bad frame with all-zero green pixels`

with the jump table's own case labels being `all_white`, `all_black` and
`invalid`. Every sibling is a **CPU-side statistic over the raw payload** —
sharpness, black level, white level, green level. The verdict is computed
upstream and stored; `PrepShot` only prints it.

### The ordering settles it

`IMPL-35`'s full 44,246-line log was still present on the device at
`/data/local/tmp/f46-agc.log`. Read-only extraction — no capture, no patch, no
preference touched — gives all fifteen of each line rather than the excerpt's
three and one:

| | count | log lines | timestamps | thread |
|---|---|---|---|---|
| `all-zero green` | 15 | 6027..6041 | **all** at `19:31:01.122` | **2946** |
| `MapFrameToTexture: SABRE` | 15 | 6173..6799 | `19:31:01.341` .. `19:31:02.415` | **2949** |

**Every green verdict precedes every mapping failure**, the smallest gap being
219 ms, and the two run on different threads. The green verdicts further share a
single millisecond — a batch evaluation over the whole payload burst — while the
SABRE failures are spread across 1.07 s, one per frame, as the merge stage walks
the burst. `aion.cc:791` itself is at `19:30:55.118`, six seconds earlier, at
library-load time.

A verdict rendered before any frame has been mapped cannot have been caused by
the mapping failing. **`SABRE` is excluded as the cause of the rejection.**

### What this establishes, and what it does not

Established: the fifteen frames are rejected by a CPU-side read of the raw
payload that finds the green channel zero. The rejection is about **frame
content**, which is where `IMPL-35` located the wall, and it is not an artifact
of the missing aion library. `EV-44` remains owed; this does not obtain it.

Not established: *where* in the raster the green statistic samples. The fold
measured in section 13 leaves roughly three quarters of the raster black —
content confined to rows `0..769` of 3072 — so a statistic sampling anywhere
outside that band would read zero green from a frame whose payload is merely
mis-strided rather than empty. That is the natural next question and it is
answerable statically, by locating the producer of `[x26+0x708]`. It is **not**
answered here, and the causal link from the fold to the green verdict is
therefore a **hypothesis, not a measurement**.

`SABRE` remains a real port deficiency and is still expected to matter to the
merge stage downstream of selection. It is simply not the reason the frames are
rejected.

`FIND-3.5-01` and `FIND-4.5-02` both remain **OPEN**. Nothing in this run is an
image fix.

## 15. The producer is `MeasureSharpnessRaw`, and the verdict is literally `all_black` (`IMPL-37`, 2026-09-02)

Section 14 excluded `SABRE` and left one question open: *where* the statistic
samples. That is not answered here either, but the producer is now identified,
the enum is decoded, and the sampling mechanism is located — which narrows the
open question from "what computes this" to a single remaining hop.

### The enum is a frame classification, and value 3 is `all_black`

The jump table at `0x889908` holds `[0x00, 0x19, 0x08, 0x0f]`, indexing from
`0x1ed81e4`. Each case builds a libc++ short string whose leading byte is the
SSO size field (`size << 1`):

| value | case target | size byte | label |
|---|---|---|---|
| 0 | `0x1ed81e4` | `0x0e` -> 7 | `invalid` |
| 1 | `0x1ed8248` | `0x0a` -> 5 | `valid` |
| 2 | `0x1ed8204` | `0x12` -> 9 | `all_white` |
| 3 | `0x1ed8220` | `0x12` -> 9 | **`all_black`** |

So `[frame+0x708] == 3` is not a bespoke "green" verdict at all. It is the
frame-content classification **`all_black`**, and `shot_process.cc:392` phrases
it as "all-zero green pixels" because green is the channel the classifier reads.
The sibling report at `0x1ed86e8` fires on value 2, `all_white`, and is phrased
"all green pixels saturated" for the same reason.

**gcam is not reporting a green-specific anomaly. It is reporting that the frame
is black.** Section 13 measured the raster as **74.93 % pure black**. Those two
statements are consistent, and their connection is the open question.

### The writer, and the producer

`PrepShot`'s reporting loop (section 14) walks a vector of frame pointers,
`x26 = [x8 + x23*8]`. The field is written earlier, at `0x1ed3d24`:

    add  x4, x3, #0x708      ; prior stats passed in
    bl   #0x1f63148          ; <- producer, sret in x8 = sp+0x20
    ldr  q0, [sp, #0x20]     ; 16 bytes back
    ldr  w11, [sp, #0x30]    ; 5th int32
    add  x9, x8, #0x708
    str  q0, [x9]            ; +0x708 .. +0x714
    str  w11, [x9, #0x10]    ; +0x718
    strb w9, [x8, #0x71c]    ; validity := 1

The five int32s at `+0x708..+0x718` are written as one block from the returned
struct, then the validity flag is set — exactly the layout the reader consumes.

`0x1f63148` is **`MeasureSharpnessRaw`**, in
`googlex/gcam/hdrplus/base_frame/sharpness.cc`. It carries the guard string
*"MeasureSharpnessRaw called with non-Bayer image, which is not supported"* and
tests the image layout at entry (`bl 0x2c8aa0c; cmp w0,#1; b.ne <error>`).

This closes section 14's inference with a name: the classification is produced by
a **Bayer-aware CPU measurement over the raw image**. It is not a GPU path, not a
texture read, and cannot involve the missing aion library.

### The sampling region is an explicit rectangle, and it is not per-frame

`MeasureSharpnessRaw` takes a region of interest as argument `x1` — four int32 —
and intersects it with the full image rect built from the image's own width and
height (`0x2c8a954`, `0x2c8a9b0`), rejecting an empty intersection:

    ldp  w8, w10, [x25]      ; ROI x0, y0
    ldp  w11, w12, [x25, #8] ; ROI x1, y1
    cmp  w8, w0  / csel ...  ; clamp against image bounds

At the call site the ROI is `ldr q0, [x27]` with `x27 = x19 + 0x16d8` — a
**persistent field of the shot context**, not recomputed per frame. No direct
store to `+0x16d8` exists anywhere in `.text` on a non-`SP` base, so it is
populated by a bulk struct initialisation or through a pointer to an inner
parameter block. Resolving that is one further hop and was not taken here.

### What this establishes, and what it does not

Established: the verdict is `all_black`, produced by `MeasureSharpnessRaw` from
the Bayer raw image on the CPU, over an explicit ROI held in the shot context and
clamped to the image bounds.

Not established: the ROI's actual value, and therefore whether the fold explains
the verdict. The mechanism is now plausible in a specific way rather than a
general one — a frame whose content is confined to rows `0..769` of 3072 is black
across the remaining 74.93 % of its raster, so any ROI not concentrated in that
top band reads black. The centre row of a 3072-row frame is 1536, which the
measured fold leaves black. **That remains a hypothesis.** Confirming it requires
the ROI value, which is the next slice and is still host-side.

`EV-44` still owed. `FIND-3.5-01` and `FIND-4.5-02` remain **OPEN**. Nothing in
this run is an image fix.

## 16. Correction: the rejected frames were half-resolution frames (`IMPL-38`, 2026-09-02)

Sections 13 to 15 all rest on a premise taken from `IMPL-35`: that the capture
which libgcam rejected 15/15 was running on a stream configured at 8192x6144.
**That premise is wrong, and `IMPL-35`'s own log disproves it.** No new capture
was needed to establish this — only reading the whole log in order rather than
by pattern.

### The configure line `IMPL-35` cited postdates the capture

`IMPL-35` paired its `getImageReaderFormat RAW10 8192x6144` with a cameraserver
line reading `width 8192 height 6144` and concluded the stream was configured at
full resolution without clamping. In chronological order the log reads:

| log line | time | event |
|---|---|---|
| 1033 | `19:30:54.631` | AGC `getImageReaderFormat RAW10 8192x6144` |
| 1084 | `19:30:54.689` | cameraserver configures **4096x3072** |
| 5368 | `19:30:59.731` | AGC `startShotCaptureInternal` — **the only shot in the log** |
| 5421 | `19:30:59.788` | libgcam `BuildPayloadBurstSpec` |
| 6027..6041 | `19:31:01.122` | 15x `all-zero green` |
| 6173..6799 | `19:31:01.341`..`19:31:02.415` | 15x `MapFrameToTexture: SABRE` |
| 11219 | `19:31:51.552` | AGC restarts, requests 8192x6144 again |
| 11250 | `19:31:51.573` | cameraserver configures **8192x6144** — *first time* |
| 15176 | `19:32:02.794` | cameraserver configures 8192x6144 |
| 17660 | `19:32:04.198` | cameraserver configures 8192x6144 |

The stream in force for the capture was the one configured at `19:30:54.689`:
**4096x3072**. The earliest 8192x6144 configuration is at `19:31:51.573`, **fifty
seconds after** the frames were already rejected, and belongs to a later AGC
session.

### No shot was ever taken on the full-resolution stream

`startShotCaptureInternal` occurs **exactly once** in 44,246 lines, at
`19:30:59.731`. `BuildPayloadBurstSpec` likewise occurs once. After each of the
three 8192x6144 configurations the log shows only `setCameraCaptureSession`
lines — session setup and preview. There is no shot marker, no payload burst and
no verdict of any kind after `19:31:02`.

**So the run never captured a photo on an 8192x6144-configured stream.** The one
capture it did take ran at 4096x3072 and was rejected.

### The same shape occurs in an earlier, undocumented session

`/data/local/tmp/f46c.log` covers `16:55`–`17:05`, a session with no snapshot in
the repository, sitting between `IMPL-33`'s 14:20 revert and the 17:40 bracket.
It contains the identical sequence:

- `17:00:18.499` — AGC `getImageReaderFormat RAW10 8192x6144`
- `17:00:18.542` — cameraserver configures **4096x3072**
- `17:00:32.616` — 15x `all-zero green`
- `17:00:32.873`..`17:00:33.979` — 15x `MapFrameToTexture: SABRE`

Two independent sessions, two and a half hours apart, produce the same request,
the same clamp to 4096x3072, and the same 15/15 `all_black` rejection.

This discharges the first caveat carried into this run. The concern was that
`IMPL-33`'s surviving 37-line excerpt contained no `all-zero green` line and so
could not show whether the condition predated full resolution. It did predate it:
the condition is present in a half-resolution-configured session, and in fact
**every** rejection on record was measured on a 4096x3072 stream. The claim
"all-zero green is new at full resolution" is not merely unsupported — the
evidence runs the other way.

### What this corrects, and what it leaves standing

Corrected: `IMPL-35`'s statement that "cameraserver configures that stream
without clamping" is not supported by its own log. The clamp to 4096x3072 did
occur, for the only capture taken. The saved **3072x4096 = 12.6 MP** JPEG is
therefore not a *fallback* from a full-resolution attempt — it is the ordinary
output of a capture configured at 4096x3072, and needs no fallback to explain it.

Left standing: sections 14 and 15 are unaffected in their mechanics. `SABRE` is
still excluded by ordering and by thread; the verdict is still `all_black`
produced by `MeasureSharpnessRaw` from the Bayer raw on the CPU. What changes is
only *which frames* were classified — half-resolution ones.

Also left standing, and now sharper: the fold. Section 13 measured the artifact's
content as confined to rows `0..769` of 3072 with the raster **74.93 %** black.
That measurement was made on a 4096x3072 frame, which is exactly the geometry the
capture actually ran at, so the fold and the `all_black` verdict describe the same
frames rather than two different populations.

**`EV-44` is not merely still owed. The experiment it names — an AGC capture on a
stream actually configured at 8192x6144 — has never been performed.** The request
side reaches full resolution; the configuration side has not, on any capture on
record.

Not established: why cameraserver clamps to 4096x3072 at configure time despite
the request, and whether `pref_48m_key` bears on it. The 17:00 session already
requested 8192x6144, which is evidence against `pref_48m_key` being what opens
the request — but the preference state at 17:00 is **not recorded** in the
repository (the brackets track only the trap keys), so that comparison is not
sound yet and no claim is made from it here.

`FIND-3.5-01` and `FIND-4.5-02` remain **OPEN**. Nothing in this run is an image
fix.

## 17. The AGC stream is not restricted — no capture was ever taken on the full one (`IMPL-39`, 2026-09-02)

The question this section was opened to answer was why cameraserver gives the
stock camera an 8192x6144 stream but clamps AGC to 4096x3072. **The premise is
false. AGC obtained an 8192x6144 stream in three separate sessions.** What never
happened is a shutter press in one of them.

### First, a precision correction to section 16

Section 16 read the cameraserver line

    Bypass roundBufferDimensionNearest for privilegedClient YUV streams
    width W height H for format 35

as reporting the capture stream. **`format 35` is `YUV_420_888`.** AGC requests
`RAW10` (`getImageReaderFormat ... ImageFormat=RAW10`, and `setShasta rawFormat =
RAW10(37)` at shot time). So this line reports a **YUV** stream and is silent
about the RAW10 stream.

That cuts both ways, and against `IMPL-35` more sharply than against section 16:

- `IMPL-35` cited an 8192x6144 line as proof the *RAW* stream was configured at
  full resolution. It is not proof: wrong format, and 50 s after the capture.
- Section 16's *conclusion* — the capture's session carried a 4096x3072 stream
  and no 8192x6144 stream of any kind — is correct and is strengthened below.
  Its *wording* was imprecise in not saying which stream, and is corrected here.

**The RAW10 stream's configured dimensions are never logged.** `CamX` emits only
`configure_streams()` errors (`initAperture`, `customeEnable`, `FPS`), and
`Camera3-Device` only `configureStreamsLocked: Unable to get tag`. No stream
inventory is printed by either. So no log on hand can say what size AGC's RAW
stream was.

### The correlation across the whole day is exact

`f46.log` (534,971 lines, `16:55`–`20:18`) is a superset of both other logs and
contains **exactly two** `startShotCaptureInternal` events.

| session | start | YUV streams configured | capture? | outcome |
|---|---|---|---|---|
| AGC (pid 7223) | `17:00:18` | **4096x3072** + 640x480 | **yes**, `17:00:31` | 15/15 `all_black` |
| AGC (pid 7664) | `17:00:37` | **4096x3072** + 640x480 | no | — |
| AGC (pid 2814) | `19:30:54` | **4096x3072** + 640x480 | **yes**, `19:30:59` | 15/15 `all_black` |
| AGC (pid 2814) | `19:31:51` | **8192x6144** + 640x480 | no | — |
| AGC (pid 2814) | `19:32:02` | **8192x6144** + 640x480 | no | — |
| AGC (pid 6203) | `19:32:04` | **8192x6144** + 640x480 | no | — |
| MiuiCamera (pid 2350) | `16:56:10` | **8192x6144** x2 | **yes**, `16:56:10` | `IMG_20260902_165610.jpg`, 8192x6144 |

Both AGC captures on record were taken in a session configured at 4096x3072.
Every AGC session configured at 8192x6144 ended without a shutter press. The one
capture on an 8192x6144 session in the whole log is the stock camera's, and it
succeeded.

**AGC is therefore not clamped by cameraserver.** It reached the same 8192x6144
figure the stock camera did, three times, on the same device state.

### What differs between AGC's own sessions

Within a single process (pid 2814) the first session was 4096x3072 and the next
two were 8192x6144, so this is not a per-process or per-client property. At
`17:00`, before `pref_48m_key` was set, both sessions were 4096x3072; from
`19:30` onward, with the key set, sessions after the first were 8192x6144.

The consistent reading is that AGC's full-resolution output size **is not in
force on the session that exists at launch** and takes hold on a later session —
either after AGC re-reads its preferences or after the user touches the
resolution control. The log cannot distinguish those two, and the user's UI
actions are not recorded, so **the trigger is not established**. What is
established is that the first session after launch was 4096x3072 in all three
launches on record, and that both captures were taken in exactly that session.

### The stock camera's 8192x6144 is a different mechanism

MiuiCamera does not take a full-resolution RAW path. It runs the vendor
quad-CFA usecase — `chxextensionmodule.cpp GetNumOfPixelsPerColor() [XCFA]` —
and receives `createCaptureSession: imageFormat: 35, width: 8192, height: 6144`,
a **YUV** session, then reprocesses through
`VirtualCameraReprocessor: createReprocessSession >> input[8192x6144]
output[8192x6144@256]`. Its buffer queue is literally named `BQ_8192x6144_35`.

So the stock camera's 50 MP is a vendor remosaic delivering YUV, while AGC wants
RAW10 at the same dimensions and runs its own HDR+ merge. They are not the same
request, and the stock camera's success does not by itself prove the RAW path
works. It does prove the sensor and vendor stack deliver 8192x6144 frames on this
device state.

### Consequence

**`EV-44` may be obtainable with no further HAL work.** The experiment it names
has never been attempted: get AGC into a session in which the 8192x6144 stream is
configured — which the log shows happens from the second session after launch —
and *then* press the shutter. Both existing captures pre-empted that by firing in
the first session.

This does not predict success. The `all_black` verdict of sections 14–16 was
measured only on 4096x3072-configured sessions, so whether it persists at full
resolution is untested in either direction. It does mean the cheapest remaining
experiment is a capture, not a patch.

Not established: the RAW10 stream size in any session; what triggers AGC's switch
to the 8192x6144 output size; and whether `pref_48m_key` is that trigger — the
17:00 sessions requested 8192x6144 through `getImageReaderFormat` while
configuring 4096x3072, so the request and the configuration move independently.

`FIND-3.5-01` and `FIND-4.5-02` remain **OPEN**. Nothing in this run is an image
fix.

## 18. The positive control: the fault is a request/delivery mismatch (`IMPL-40`, 2026-09-02)

The user took a photo at `21:26:59`. It was **not** `EV-44` — AGC was in
half-resolution mode and requested `RAW10 4096x3072`, not `8192x6144`. It is
something the project had never obtained and needed more: **a successful AGC
capture through the same stack, logged the same way.** It closes the diagnosis.

### The comparison

The logcat ring buffer was dumped immediately after the shot and still contained
`IMPL-35`'s session, so both captures are measured from one log, one device
state, one instrumentation.

| capture | AGC `getImageReaderFormat` | cameraserver YUV | match | `all_black` | saved JPEG |
|---|---|---|---|---|---|
| `17:00:31` | RAW10 **8192x6144** | 4096x3072 | **no** | **15/15** | folded |
| `19:30:59` | RAW10 **8192x6144** | 4096x3072 | **no** | **15/15** | folded |
| **`21:26:59`** | RAW10 **4096x3072** | 4096x3072 | **yes** | **0** | **clean** |

Measured on the JPEGs themselves (PIL, grayscale, threshold < 4):

- `19:31` artifact — 3072x4096, 12.6 MP, black pixels **0.7498**
- `21:27` artifact — 3072x4096, 12.6 MP, black pixels **0.0024**

Identical dimensions and identical megapixels. The only variable that moved is
whether the requested reader size matched the delivered buffer.

### The mechanism, now closed

`1 - 1/4 = 0.75`. A `4096x3072` payload placed into a raster the consumer
believes is `8192x6144` fills exactly one quarter of it — `12.58` MP of `50.33`
MP — leaving **three quarters black**. The measured `0.7498` is that number.

So the chain runs:

1. AGC opens a `RAW10` `ImageReader` at `8192x6144`.
2. The stack delivers `4096x3072` buffers regardless.
3. gcam reads the payload at the `8192`-wide stride it was promised, so the
   content lands in one quarter of the raster and the rest is zero.
4. `MeasureSharpnessRaw` (section 15) reads the Bayer green channel on the CPU,
   finds it zero, and returns **`all_black`**.
5. `PrepShot` rejects 15 of 15 candidate frames (section 14).
6. The saved image carries the fold.

**The fault is not full resolution. It is the mismatch.** Ask for what the stack
actually delivers and the same pipeline, on the same device state, produces a
clean 12.6 MP photograph.

### Two earlier findings confirmed by positive control

Both had rested on ordering or on absence of evidence. The successful capture
converts them into direct observations:

- **`SABRE` is irrelevant to the verdict.** The `21:26` session logged **15**
  `MapFrameToTexture: SABRE: Cannot get file descriptor from opaque_handle`
  (`21:27:01.315`–`21:27:01.610`) — the full complement — and produced **zero**
  rejections and a clean image. Section 14 excluded `SABRE` by timestamp and
  thread; this settles it by outcome. `lib_aion_buffer.so` remains missing and
  remains harmless to frame acceptance.
- **`Invalid mesh: [4096,3072]` is a standing condition, not a symptom.** It
  appears twice in the successful capture (`21:27:01.993`), exactly as it does in
  the failed ones. `IMPL-35` reframed it as tracking the un-raised
  `quadra_cfa.activeArraySize`; a clean photo carrying the same message confirms
  that reading.

### What this means for the work

**The target moves from the request side to the delivery side.** AGC can already
ask for `8192x6144` — it did so in six sessions across three launches. Nothing in
the app or its preferences needs further opening. What has never happened is the
stack **delivering** an `8192x6144` RAW buffer. Until it does, every
full-resolution attempt will fold and be rejected in exactly this way, and the
rejection is a faithful report rather than a bug in gcam.

That is precisely what the HAL stream-configuration work targets, so `Faz4.1` and
its successors are aimed at the right layer. `EV-44` remains the acceptance test,
and it is now sharply defined: **a capture in which `getImageReaderFormat` reads
`8192x6144` and the delivered payload is also `8192x6144`.** Neither of the two
folded captures met the second half, and the clean one did not attempt the first.

Not established: why the stack delivers `4096x3072` for a `RAW10` reader opened
at `8192x6144` rather than failing configuration outright, and at which layer
that substitution happens. The RAW stream's configured dimensions are still never
logged (section 17), so this needs the HAL side rather than another capture.

`FIND-3.5-01` and `FIND-4.5-02` remain **OPEN** — but `FIND-4.5-02`, the image
corruption, now has a mechanism rather than a description.

## 19. Direction A settled host-side: `tempBinning` is temporal, and a full-resolution sensor mode exists (`IMPL-41`, 2026-09-02)

Section 18 moved the target to the delivery side and left one lead attached to
it: AGC's `tempBinning: true`, logged once per capture and true in both the
folded `19:30` shot and the clean `21:26` one. The handoff recorded it honestly
as a lead rather than a finding — it did not discriminate the two captures, and
whether it was thermal, causal, or merely AGC reporting sensor state was open.

This section closes it. **No device was used, no preference touched, no capture
taken.** Everything below is static analysis of files already in the repository.

### `tempBinning` is `ShotParams.allow_temporal_binning`, not a sensor readout mode

The string `tempBinning:` is emitted from exactly one place in
`AGC8.4.300_V9.6_50MP_patched.apk`, `classes2.dex`, in
`LHdrPlusSessionImpl;->startShotCaptureInternal`. Its immediate neighbourhood
settles what it is:

```
012a: invoke  LAGC;->getTemporalBinning
012e: const-string "tempBinning:"
0130: invoke  Lcom/agc/Log;->d                          <- the logged line
0135: invoke  GcamModuleJNI;->ShotParams_allow_temporal_binning_set
```

The value that is logged is the value that is then written into gcam's
`ShotParams.allow_temporal_binning`. Its source is a menu preference:

```
LAGC;->getTemporalBinning:
  const-string "pref_temporal_binning_key"
  const/4 v1, 0                                         <- default
  invoke  Lcom/Utils/Pref;->MenuValue
```

**Temporal binning is frame stacking — a burst/merge parameter inside gcam.** It
is a different mechanism from spatial sensor binning, which has its own separate
vocabulary in the same APK (`com.google.internal.SensorBinningMode`,
`ApplySensorBinning__SWIG_0/1`). `tempBinning: true` therefore means the port's
temporal binning preference is on. **It has no path to the sensor readout mode
and cannot cause the stack to deliver `4096x3072`.** The lead is refuted, not
merely undischarged.

### AGC's only sensor-binning control is a Pixel tag it cannot use here

The genuine sensor-binning surface does exist in the APK, and it is inert on this
device. `Lghy;-><clinit>` builds two `CaptureRequest$Key` objects, the second
being `com.google.internal.SensorBinningMode`. The only consumer of that field is
`Lgwh;->get`, and it is guarded:

```
017c: Set->iterator                    <- the device's available request keys
018c: CaptureRequest$Key->getName
0190: sfield Lghy;->b                  (com.google.internal.SensorBinningMode)
0196: String->equals                   <- capability guard
019c: sfield Lghy;->b
019e: Integer->valueOf
01a2: invoke Lfcy;->i                  <- the write, reached only on a match
```

AGC enumerates the keys the device advertises and writes `SensorBinningMode`
**only if the device advertises it.** Supporting measurement: a string scan of
both vendor HAL binaries (`enable` and `disable`, and the module's `root/odm`
copy) returns **zero** occurrences of `com.google.internal` — the tag namespace
is absent from CamX entirely, not merely this one key.

That scan covers `camera.qcom.so` only. A vendor tag could in principle be
published by a separate tag-provider library, so this is strong evidence rather
than proof; confirming it costs one `dumpsys media.camera` grep on the device and
has not been spent. Either way the write is conditional, so **the worst case is
that AGC sets a binning mode it was already able to set** — it is not a silent
forced-binning path.

**Consequence: AGC does not and cannot select the sensor readout mode.** The
binned delivery is decided entirely below the application. This is the app-side
half of section 18's open question, and it closes in the same direction section
17 pointed: nothing further is to be gained by opening the app.

### The sensor has exactly one full-resolution mode, and it is mode 0

Parsed from `com.qti.sensormodule.ishtar_semco_imx989_wide.bin` using the format
recovered in the 2026-08-16 session: parameter table at `0xD0`, 60 bytes per
entry, offsets relative to the data base at `0xB8`. The file holds 14,454
entries, one `resolutionData` of 6,992 bytes (23 records of 304), and 23
`streamConfiguration` entries. Within a 60-byte stream configuration, `u32[5]`,
`u32[6]` and `u32[7]` are width, height and bit depth.

| mode | stream configurations | line_length_pck | frame_length_lines | cfg count |
|---|---|---|---|---|
| **0** | **8192x6144/10** | 13824 | 8728 | **1** |
| 1 | 4096x3072/10, 4096x768/10 | 11168 | 12680 | 2 |
| 2 | 4096x2304/10, 4096x576/10 | 11168 | 12672 | 2 |
| 3 | 4096x3072/10, 2048x768/10 | 21536 | 6576 | 2 |
| 4 | 4096x2304/10, 2048x576/10 | 21536 | 6567 | 2 |
| 5 | 4096x3072/10 x3, 4096x768/10 | 11168 | 4224 | 4 |
| 6 | 4096x2304/10 x3, 4096x576/10 | 11168 | 4224 | 4 |
| 7 | 4096x2304/10, 4096x576/10 | 11168 | 6336 | 2 |
| 8 | 7680x4320/10, 3840x1080/10 | 21536 | 6792 | 2 |
| 9 | 1920x1080/10, 1920x270/10 | 5440 | 1392 | 2 |
| 10 | 4096x2304/10, 4096x576/10 | 11168 | 12672 | 2 |
| 11 | 4096x2304/10 x2, 4096x576/10 | 11168 | 6336 | 3 |
| 12 | 3360x2520/10, 3360x630/10 | 11168 | 13104 | 2 |
| 13 | 3360x2520/10, 1680x630/10 | 21536 | 6792 | 2 |
| 14-19 | replicate modes 1-6 on these fields | | | |
| 20, 21 | replicate modes 12, 13 on these fields | | | |
| 22 | 1280x720/10, 1280x180/10 | 5440 | 1680 | 2 |

**Mode 0 is the only `8192x6144` entry in the table**, and it is structurally
unlike every other mode: it is the sole record carrying a *single* stream
configuration, and the sole record whose `u32[8]` field reads `1` where every
other mode reads 2, 3 or 4.

A note on the replication rows, because it refines an earlier session's claim
rather than confirming it. Measured on the resolution and timing fields, modes
14-19 replicate modes 1-6 and modes 20-21 replicate modes 12-13 — not 14-21
replicating 1-8. No two of the 23 records are byte-identical, because each
carries its own `streamConfiguration` and `regSetting` entry indices; the earlier
"bit-identical" observation was about the register blocks those indices point to,
which this measurement does not test either way.

So the full-resolution mode is present in the sensor configuration. **The part is
not pinned to a binned mode by its own driver data**; a `50.33` MP `RAW10`
readout exists and is described. What remains unproven is whether CamX ever
*selects* mode 0 for a still capture — the delivery question restated one layer
lower, and now with a concrete object to look at.

One instrument found while reading the HAL, never used by this project and free:
CamX carries the format string

```
[ DUMP] SensorMode: numPixelsPerLine:%d numLinesPerFrame:%d maxFps:%f
        Binning_H:%d Binning_V:%d WxH:%d X %d
```

That line names the selected mode's binning factors and dimensions directly.
Section 17 established that the RAW *stream's* configured dimensions are never
logged; this is a different statement, from the sensor layer rather than the
stream layer, and it would answer which mode was chosen without any patch.

### The vendor's own high-resolution switch is a 228-byte HAL diff

`Module_Highres_13U_Switcher_A14/mod/` ships two complete HAL binaries of
identical size (31,004,560 bytes, both dated 2024-03-08):

- `enable/camera.qcom.so` — md5 `f6b4fbd0d5e7403292070c2dad3c4df6`
- `disable/camera.qcom.so` — md5 `35194d60e7e8a246b05de64a11b9ff7c`, byte-identical
  to the module's own `root/odm/lib64/hw/camera.qcom.so`

They differ in **228 bytes across 66 regions**, and the differences are a small
set of repeated, legible patterns:

1. **About 45 sites of `ldr wN, [xM, #0x3d84]` becoming `mov wN, #0`.** One fixed
   structure field, read through many different base registers, forced to zero in
   the high-resolution variant.
2. **A second cluster forcing `ldr wN, [x16, #0x0 / #0x4 / #0x8]` to `mov wN, #0`**,
   around file offsets `0x019caa70`–`0x019cad04`.
3. **Four bounds raised by exactly one:** `cmp wN, #4` becomes `cmp wN, #5`
   (registers `w7`, `w9`, `w13`, `w16`).
4. **One guard neutralised:** `cmp w0, #2` / `b.eq` becomes `cmp w0, w0` / `b.ne`
   at file offset `0x019ca490`, a branch that can now never be taken.
5. **One 64-bit constant halved**, via a `movk` into bits 63:48: `0x41cd` becomes
   `0x41bd`, which as the high half of a double is `9.73e8` becoming `4.87e8`.

Symbol attribution is not available for these sites: the nearest preceding
exported symbol is hundreds of kilobytes away, so the containing functions are
local and stripped. Do not quote a function name for them.

**These offsets are not transferable.** Both binaries are from the A14 Highres
switcher module and are a different build from the device's current
`/odm/lib64/hw/camera.qcom.so` (`fe0245a4720fb07b01d96deef47f5569`, the
full-resolution base). The *patterns* carry; the addresses do not, and would have
to be re-derived against the live build before anything is written.

### What this establishes, and what it does not

**Established.** `tempBinning` is temporal binning driven by an AGC preference and
is unrelated to sensor readout. AGC's sensor-binning control is a Pixel vendor
tag guarded by an availability check the device fails, so the app cannot select
the readout mode. The IMX989 driver data contains exactly one full-resolution
mode, mode 0 at `8192x6144` `RAW10`, structurally distinct from all 22 others. A
vendor-built high-resolution HAL for this exact device exists in the repository
and differs from its own disabled counterpart by 228 bytes in five recognisable
patterns.

**Not established.** Whether CamX selects mode 0 for a still capture, and what
chooses it. What the field at `[xM, #0x3d84]` is. Whether the `cmp #4` to `cmp #5`
bound concerns stream counts, mode indices or something else. Whether the halved
constant is a rate limit. Whether any one of the five patterns is what makes the
stack **deliver** `8192x6144`, or whether they are five parts of a single switch.
Nothing here has been tested on the device, and the vendor binaries are a
different build.

**Direction A is answered in the negative for the app and the sensor data, and it
has produced a better object than the one it went looking for.** The question is
no longer "is the sensor forced to bin" — it is not — but "what in CamX picks the
mode, and is the vendor's own 228-byte switch the answer". `EV-44` is unchanged
as the acceptance test. `FIND-3.5-01` and `FIND-4.5-02` remain **OPEN**.

## 20. The `SensorMode` dump line cannot be enabled on this build; what the attempt established instead (`IMPL-42`, 2026-09-02)

Section 19 named the CamX dump line

```
[ DUMP] SensorMode: numPixelsPerLine:%d numLinesPerFrame:%d maxFps:%f
        Binning_H:%d Binning_V:%d WxH:%d X %d
```

as a free instrument that would say which sensor mode CamX selects. The user
chose to spend the device on it. **It could not be enabled.** The negative is
reported first because it is the result; the positives below are things the
attempt turned up on the way, and two of them are worth more than the line was.

The device was returned to its exact prior state: the bracket pair
`20260902-2216__Faz4.6__IMPL42-pre-logmask` and
`20260902-2228__Faz4.6__IMPL42-post-revert` compare **byte-identical** in their
comparable regions, the live HAL is still `fe0245a4720fb07b01d96deef47f5569`,
and the AGC preference trap is unchanged at 2/12. Nothing was written to any
partition — `/vendor` and `/odm` are read-only erofs and stayed that way.

### The negative: CamX log masks are inert on this build

`camxoverridesettings.txt` is read and applied — that was proven, see below —
but the three logging masks are not. At every attempt CamX printed:

```
camxoverridesettingsfile.cpp:805 Initialize() logInfoMask    = 0
camxoverridesettingsfile.cpp:805 Initialize() logVerboseMask = 0
camxoverridesettingsfile.cpp:805 Initialize() logCoreCfgMask = 0
```

Five variations were tried, each with a full camera-stack restart:

1. `logInfoMask` / `logCoreCfgMask` appended at the end of the file, `0xFFFFFFFF`.
2. The same settings placed at the **top** of the file, `0x7FFFFFFF`.
3. Decimal `2147483647`.
4. **In-place replacement of the vendor's own line** rather than a second one.
5. A clean 32-bit literal `0xFFFFFFF`, testing whether the vendor's value was
   the problem.

The fourth and fifth deserve emphasis. **The vendor's own file already sets
`logInfoMask=0x1000000006010098`** — a 64-bit literal — alongside
`overrideLogLevels=0x1F` and `enableTxtLogging=1`, and CamX reports that setting
as `0` too. So this is not a rejection of *our* value; the mask reads zero no
matter who writes it, including Xiaomi. The natural reading is that logging is
compiled down in this production build and `Initialize()` prints the effective
zero. `SENSOR`-group line counts in logcat stayed flat across every attempt
(674, 677, 682, 687), and `/data/vendor/camera/offlinelog` is empty, so
`enableTxtLogging=1` is not routing them to a file either.

**Do not spend another session on CamX log masks on this build.** The
`[ DUMP] SensorMode` line, the `[ VERB] currentSensorMode=%d for Node name` line,
and the `[CORE_CFG] ModeSwitch: ... SensorMode %d settings applied successfully`
line are all unreachable by this route.

### Positive 1: the settings file CamX reads is the ODM copy, not the vendor one

There are two `camxoverridesettings.txt` on the device and **they are
byte-identical** (`md5 0fbd24739df68bf8837176c1d0e1aa3d`):

- `/vendor/etc/camera/camxoverridesettings.txt`
- `/odm/etc/camera/camxoverridesettings.txt`

Being identical, no static inspection can say which one is read. A marker
discriminates: change `maxDigitalZoom=120.0` to `119.0` in one copy at a time and
read the value back out of CamX's own `DumpData()` output.

| modified copy | CamX reported `maxDigitalZoom` | conclusion |
|---|---|---|
| `/vendor/etc/camera/…` | **120.0** | not read |
| `/odm/etc/camera/…` | **119.0** | **this is the one** |

**A future session that edits the `/vendor` copy will change nothing and get no
error.** That is a silent-failure trap of exactly the kind this project has been
bitten by before, and it is now closed.

### Positive 2: override settings are live-editable, reversibly, without a reboot

Both partitions are read-only erofs, but the file can be replaced by a bind
mount from a writable path:

```
cp /odm/etc/camera/camxoverridesettings.txt /data/local/tmp/cxo-odm.txt
# edit /data/local/tmp/cxo-odm.txt
chown 0:0 …; chmod 644 …; chcon u:object_r:vendor_configs_file:s0 …
mount -o bind /data/local/tmp/cxo-odm.txt /odm/etc/camera/camxoverridesettings.txt
# restart the camera stack: cameraserver first, then the providers
```

Reverted with `umount`. No partition remount, no module edit, no reboot. The
`chcon` matters — without the `vendor_configs_file` context the provider cannot
read it. Verified end to end by the `119.0` marker above, and verified clean on
revert by md5 against the backups and by the identical bracket pair.

This is a general capability the project did not have: **any CamX override
setting can now be changed for one measurement and taken back.** The masks
happen to be inert, but the mechanism is not.

### Positive 3: CamX independently confirms the full-resolution mode, and names AGC's camera

`dumpsys media.camera` prints vendor static metadata **with values**, and carries

```
org.quic.camera2.sensormode.info.SensorModeTable (803a0000): int32[71]
  [23 3 8192 6144 ] [30 4096 3072 30 ] [4096 2304 30 4096 ] …
```

`71 = 2 + 23 x 3`: a count of **23 modes**, three fields each, and the **first
entry is 8192x6144**. This is section 19's mode-0 finding reproduced through a
completely independent channel — framework metadata rather than a hand-parse of
`com.qti.sensormodule.ishtar_semco_imx989_wide.bin` — and it shows the mode is
not merely present in driver data but **advertised upward by CamX**.

Five camera ids carry the `int32[71]` table — **0, 2, 6, 7, 10** — which matches
the earlier finding that one IMX989 feeds five logical camera ids. The others
carry shorter tables (`int32[20]`, `[29]`, `[38]`).

And CamX's `dumpState` retains a configure-streams ring that names the pipeline:

```
09-02 21:26:52  Pipeline[RealTimeFeatureZSLPreviewRawForThirdPartyApp_0_cam_0]
09-02 21:27:11  Pipeline[RealTimeFeatureZSLPreviewRawForThirdPartyApp_0_cam_0]
```

**AGC runs on `cam_0`**, and `cam_0` is one of the five ids whose table contains
`8192x6144`. Those two timestamps are the successful `21:26` capture from section
18. The ring gives pipeline names and timings only — no stream dimensions and no
sensor mode — so it does not answer the delivery question, but it does fix which
camera the question is about.

### What this establishes, and what it does not

**Established.** The CamX log-mask route is closed on this build, for anyone,
including the vendor. The settings file that matters is the ODM copy. Override
settings can be changed live and reverted without touching a partition. CamX
advertises a 23-mode table whose first entry is `8192x6144`, on the five camera
ids the IMX989 feeds, and AGC uses `cam_0`, one of them.

**Not established — unchanged from section 19.** Whether CamX *selects* mode 0
for a still capture. The instrument chosen for that question turned out to be
unavailable, and no substitute was run.

**Better instrument for the next attempt, found while failing at this one.** The
metadata table at `/data/vendor/camera/metadata/metadatatable.txt` lists
`TagID e0021  SensorRawBinningFactorUsed` — the standard
`android.sensor.rawBinningFactorUsed` **result** key. It states the binning
factor of a delivered frame, per capture, and it is read from a `CaptureResult`
by an ordinary camera client rather than from a HAL log. That sidesteps the mask
problem entirely. Also present and unexamined: `PropertyIDUsecaseSensorModes`
(`50000000`, 83,600 bytes), `PropertyIDSensorModeSwitched` (`30000045`),
`com.xiaomi.SensorMode.sensorModeMask` (`81150000`), and the untested properties
`persist.vendor.camera.logstate=3` and `vendor.camera.sensor.logsystem=3`.

`EV-44` is unchanged. `FIND-3.5-01` and `FIND-4.5-02` remain **OPEN**.

## 21. `EV-44` performed: the stream reaches full resolution, the sensor readout does not (`IMPL-43`, 2026-09-02)

`EV-44` had never been attempted. It has now been performed, and it **passes its
first half and fails its second**. The result relocates the fault a layer below
where section 18 put it, and it corrects section 18's model on a point the model
itself predicted.

### The instrument section 17 said did not exist

Section 17 concluded that "the RAW10 stream's configured dimensions are never
logged anywhere". **That is true of logcat and false of `dumpsys`.** With a
camera open, `dumpsys media.camera` prints, per stream:

```
Stream[2]: Output
  Consumer name: ImageReader-8192x6144f25m37-18510-2
  Dims: 8192 x 6144, format 0x25, dataspace 0x1
  Frames produced: 2104
```

The consumer name carries the **app-side `ImageReader` geometry and format**, and
`Dims:` carries the **configured stream geometry**. Both halves of `EV-44` are
therefore readable directly, without a log mask, without a patch, and without the
`[ DUMP] SensorMode` line that section 20 established is unreachable. The same
dump also prints the latest result metadata with values.

### Baseline: RAW10 at full resolution was never published

On the live fullres base (`fe0245a4720fb07b01d96deef47f5569`, no stack), for
camera 2 — the device AGC opens — `android.scaler.availableStreamConfigurations`
contains **127 rows**, and its only RAW10 (format 37) entries are:

```
[37 4096 3072 OUTPUT ]   [37 4096 2304 OUTPUT ]
```

At `8192x6144` it publishes formats 33, 34, 35 and 54 — **no RAW10**. The vendor's
own `xiaomi.scaler.availableStreamConfigurations` (`81850000`) *does* carry
`[37 8192 6144 0]`, so the HAL knows about RAW10 at 50 MP internally; it simply is
not published in the AOSP table the framework validates client streams against.

**That is why the stack delivered a binned buffer.** It is not a sensor-binning
decision and never was: a RAW10 reader opened at `8192x6144` had no matching
published configuration, and the session ended up on the `4096x3072` RAW10 stream.

### With the seven-word stack the stream reaches full resolution

Applying the pre-committed stack — `md5 c094101de0184e9216a57020873bac0b`, 7
words, in `applyfull.sh`'s documented safe window — changes the published table:

| | rows in `availableStreamConfigurations` | RAW10 entries | `[37 8192 6144 OUTPUT]` |
|---|---|---|---|
| fullres base | 127 | 2 | absent |
| **+ seven-word stack** | **217** | **32** | **present** |

With `pref_48m_key=1`, the trap cleared to 0/12, and
`pref_camera_picturesize_back_key=8192x6144`, AGC then configures:

```
Stream[1]  ImageReader-8192x6144f23m22   Dims: 8192 x 6144  format 0x23 (YUV)
Stream[2]  ImageReader-8192x6144f25m37   Dims: 8192 x 6144  format 0x25 (RAW10)
```

**Request and configuration agree at full resolution.** `EV-44`'s first half —
never previously achieved — is satisfied.

A correction to the carried claim while we are here: `pref_48m_key` is
**necessary but not sufficient, and it is not the selector**. It only makes the
50 MP size appear in AGC's list. The proximate selector is
`pref_camera_picturesize_back_key`; with `pref_48m_key=1` but that key still
reading `4096x3072`, AGC opened a `4096x3072` RAW10 reader and the session matched
cleanly at half resolution.

### The capture: 50 MP for the first time, and still exactly three quarters black

Shutter fired at `22:42` (`input keyevent 27`), producing
`AGC_20260902_224207399.jpg`.

| capture | JPEG | MP | black fraction |
|---|---|---|---|
| `21:26` clean reference | 3072x4096 | 12.58 | **0.0024** |
| `19:31` folded reference | 3072x4096 | 12.58 | 0.7498 |
| **`22:42` full-res stream** | **6144x8192** | **50.33** | **0.7497** |

This is **the first 50.33 MP image the project has produced**. It is also still
folded, and `PrepShot` still rejected **15 of 15** frames with `all-zero green`.

Quadrant measurement on the 22:42 artifact (stored rotated, so 6144x8192):

```
top-left     black 1.0000      top-right     black 0.4994
bottom-left  black 1.0000      bottom-right  black 0.4994
```

The left half is entirely black and the right half is half black: **content
occupies exactly one quadrant**, `(1.0+0.4994+1.0+0.4994)/4 = 0.7497`. A
`4096x3072` content region inside an `8192x6144` raster, which is the same
arithmetic section 18 closed — but now with the stream itself at `8192x6144`.

### What this corrects in section 18

Section 18 concluded that `all_black` tracks a **request/delivery mismatch**, and
predicted that making the requested reader size match the delivered buffer would
yield a clean image. **The prediction is now falsified in the direction that
matters.** Here the app request, the configured stream, and the saved image are
all `8192x6144`, and the fold is unchanged at `0.7497`.

The mismatch is real but was mislocated. It is not *app request vs stream
configuration* — that now agrees. It is **buffer geometry vs sensor readout
geometry**. The stream is `8192x6144`; the sensor is still reading out binned
`4096x3072` and its content lands in one quarter of the buffer.

Section 18's clean `21:26` capture is still explained: there the buffer was
`4096x3072` *and* the readout was `4096x3072`, so they agreed. Agreement, not
resolution, was the operative variable — the refinement is only that the second
term is the **readout**, not the configuration.

### The located cause: the camera does not advertise ultra-high-resolution

Read live from the capture's own result metadata:

```
android.sensor.pixelMode (e0020):            [DEFAULT ]
android.sensor.rawBinningFactorUsed (e0021): [FALSE ]
```

And from camera 2's static characteristics:

```
android.request.availableCapabilities (c000c): byte[11]
  [BACKWARD_COMPATIBLE CONSTRAINED_HIGH_SPEED_VIDEO RAW YUV_REPROCESSING
   PRIVATE_REPROCESSING READ_SENSOR_SETTINGS MANUAL_SENSOR BURST_CAPTURE
   MANUAL_POST_PROCESSING STREAM_USE_CASE DYNAMIC_RANGE_TEN_BIT ]
```

**`ULTRA_HIGH_RESOLUTION_SENSOR` is absent**, and the
`activeArraySizeMaximumResolution`, `pixelArraySizeMaximumResolution`,
`preCorrectionActiveArraySizeMaximumResolution` and `binningFactor` static tags
appear only in key *lists*, carrying no values.

Without that capability a client cannot legally request
`android.sensor.pixelMode = MAXIMUM_RESOLUTION`, CamX stays in `DEFAULT` pixel
mode, and `DEFAULT` on this quad-Bayer part is the 2x2 binned readout. That is
exactly what the metadata reports and exactly what the quadrant measurement
shows.

This also reconciles the stock camera, which does reach 50 MP: `IMPL-39` recorded
that MiuiCamera gets there through the vendor quad-CFA remosaic **YUV** usecase,
not through RAW and not through `pixelMode`. The two paths are independent, and
only the RAW path needs the capability.

### What this establishes, and what it does not

**Established.** `dumpsys media.camera` reads both halves of `EV-44` directly and
is the instrument section 20 went looking for. On the base HAL, RAW10 at
`8192x6144` is not published in the AOSP stream-configuration table, which is the
mechanical reason a full-resolution RAW request was served a binned buffer. The
seven-word stack publishes it (127 -> 217 rows, 2 -> 32 RAW10 entries) and AGC
then configures a genuine `8192x6144` RAW10 stream. A capture on that stream
produces a 50.33 MP image — a first — that is still folded into one quadrant,
with 15/15 `all_black`. The cause is that the sensor readout stays binned because
camera 2 does not advertise `ULTRA_HIGH_RESOLUTION_SENSOR`, so
`pixelMode` cannot leave `DEFAULT`.

**Not established.** Whether adding the capability and populating the four
`*MaximumResolution` tags is sufficient to make CamX switch the sensor to mode 0,
or whether the sensor-mode selection needs separate work. Whether the vendor's
remosaic path can be reached from a RAW request at all. Nothing was patched
toward either — the stack applied here is the project's own pre-committed one and
nothing new was written.

**`EV-44` verdict: first half PASS, second half FAIL.** `FIND-3.5-01` and
`FIND-4.5-02` remain **OPEN**, and `FIND-4.5-02` now has a *located* mechanism
rather than an inferred one.

### Device state left by this run

The stack is **still applied** (`c094101d…`) and the preferences are still set to
50 MP, because that is the state in which the next experiment runs. To restore
the pre-session state:

```
sh /data/local/tmp/revertstack.sh        # -> fe0245a4720fb07b01d96deef47f5569
tar -xf /data/local/tmp/agc-shared_prefs.bak-20260902-2240.tar \
    -C /data/data/org.codeaurora.snapcam
```

Brackets: `20260902-2228__Faz4.6__IMPL42-post-revert` (before) and
`20260902-2245__Faz4.6__IMPL43-post-EV44-stack-applied` (after).
