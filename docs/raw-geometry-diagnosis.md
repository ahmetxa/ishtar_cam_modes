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
| `AGC_20260901_211031502.jpg` | **3072x4096** | five-word stack, 37 s before the primary |
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
| `AGC_..._211108200` (five-word) | 8192x6144 | 1539 rows | **4096x3078** | **yes** |
| `AGC_..._211031502` (five-word) | 4096x3072 | 770 rows | **2048x1540** | **yes** |
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
| `..._211108200` | five-word | 8192x6144 | **4096x3072** | 1/2 | **1/2** | 75% |
| `..._211031502` | five-word | 4096x3072 | **2048x1536** | 1/2 | **1/2** | 75% |

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
five-word captures differ in more than the two active-array words: different
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
| `F4.6-05` consumer control | Live. Needs the five-word stack re-applied, a camera restart, and shutter presses. | User approval and device |
| `F4.6-06` HAL configuration read | Live. Needs filtered logcat during a capture in the five-word stack. | User approval and device |
| `F4.6-07` DNG probe | Gated. `EV-35`: no full-resolution DNG exists before `Faz4.1` lands format-32 emission. | `Faz4.1` |

`F4.6-05` and `F4.6-06` are now **better specified** than when they were written:
`F4.6-06` should read the negotiated buffer **stride** and the **binning state**
specifically, because the model predicts a source width of exactly half the
buffer width, and that is a number the log either carries or does not.

Pre-existing captures were checked as free corroboration and are **not** the
`F4.6-05` control: the stock camera's 18:46 captures are 4896x6528, a different
mode, and the Open Camera 15:42 capture is the three-layer `EV-33` reference, not
the five-word stack.

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
