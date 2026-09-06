# Phase 4 Consolidated Patch Validation Record

Produced by `Faz4.4` (`Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md`).
This file is written as verdicts are produced, per that sub-plan's section 10 mitigation. An
item marked NOT YET RUN has not been attempted; it is not a pass and not a failure.

## 0. The artifact under validation

| Property | Value |
|---|---|
| Live HAL | `/odm/lib64/hw/camera.qcom.so`, md5 `fe0245a4720fb07b01d96deef47f5569` |
| Its canonical table | `ishtar-cam-modes/blobs/hal-fullres.patch`, 16 points |
| Reproducibility | `IMPL-65` applied that table to stock `c3fa63a86ee3ecaf9fbf02005d35f6b5` and recomputed `fe0245a4…` byte-identically, 0/16 stock-column mismatches |
| Module mode | `50mp` |
| Sensor | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` (stock) |
| AGC preferences | `pref_48m_key=0`, `pref_camera_resolution=full`, back derived `4096x3072` |

Under the user's 2026-09-05 "broad emission" ruling (`IMPL-66`), the consolidated artifact **is**
the canonical table unchanged. There is no third HAL state. Everything below is measured against
the state the device was already running; nothing was written to the device to produce it.

Evidence: `snapshots/20260905-2017__Faz4.4__F4401-cam3-d000abc-rows.txt`,
`snapshots/20260905-2017__Faz4.4__F4402-per-camera-array-and-counts.txt`.

## 1. F4.4-01 — Stream configuration surface (camera 3)

Sliced by tag-header boundary, never by line number.

Published counts: `d000a` `int32[508]`, `d000b` `int64[504]`, `d000c` `int64[120]`.
Parsed: 127 stream-configuration rows — **124 OUTPUT, 3 INPUT**.

Format census of `d000a`:

| Format | OUTPUT rows | INPUT rows | Name |
|---|---|---|---|
| 32 | 2 | 0 | RAW16 / RAW_SENSOR |
| 33 | 28 | 0 | BLOB (JPEG) |
| 34 | 30 | 1 | IMPLEMENTATION_DEFINED |
| 35 | 30 | 1 | YCbCr_420_888 |
| 36 | 2 | 0 | RAW_OPAQUE / RAW_PRIVATE |
| 37 | 2 | 0 | RAW10 |
| 54 | 30 | 1 | vendor format |

The complete emitted RAW entry set — recorded as it stands, **not** treated as spurious:

```
37 4096 3072 OUTPUT      32 4096 3072 OUTPUT      36 4096 3072 OUTPUT
37 4096 2304 OUTPUT      32 4096 2304 OUTPUT      36 4096 2304 OUTPUT
```

Six rows. Formats 32/36/37 at two resolutions. **Format 38 (RAW12) is not emitted at any
resolution.**

Every row at 8192x6144, all formats:

```
34 8192 6144 OUTPUT   34 8192 6144 INPUT
35 8192 6144 OUTPUT   35 8192 6144 INPUT
33 8192 6144 OUTPUT
54 8192 6144 OUTPUT   54 8192 6144 INPUT
```

**Verdict: RAW10 is ABSENT at 8192x6144.** No RAW-family format (32, 36, 37, 38) appears at
that resolution. The duration tables do carry 8192x6144 — `d000b` has four rows at
`66666666` ns and `d000c` one JPEG row at `327155712` ns (`IMPL-64`) — but there is no RAW
stream-configuration entry there for them to match.

This is not a regression and not a defect in the artifact. It is the direct and expected
consequence of the user's broad-emission ruling: RAW at 8192x6144 was produced only by
`hal-raw50-deneme.patch`, the widening that ruling rejected. It does mean the sub-plan's first
acceptance criterion, inherited verbatim from `Main-Planing.md`'s amended Phase 4 acceptance
signal, **cannot be satisfied by the artifact that ships**. Raised as `FIND-4.4-01`; see section 5.

The second half of the criterion holds in the form the artifact supports: every OUTPUT entry that
exists has a `d000b` row (`IMPL-64`, zero missing), and the six RAW rows have no `d000c` row —
the measured, unpatchable gap `IMPL-64` closed `Faz4.2` on.

## 2. F4.4-02 — Array entry count

Reported per camera id, on the `availableStreamConfigurations` (`d000a`) **int32 element count**.
No unqualified "508" is used as a baseline. **No reduction target applies** — `DEC-14` retired it
and forbade inventing a substitute.

| Camera id | `d000a` int32 | `d000b` int64 | `d000c` int64 | Delta vs 2026-09-05 19:46/19:54 bracket |
|---|---|---|---|---|
| camera.hal0 | 456 | 444 | 60 | 0 |
| camera.hal1 | 452 | 440 | 56 | 0 |
| camera.hal2 | 508 | 504 | 120 | 0 |
| camera.hal3 | 508 | 504 | 120 | 0 |
| camera.hal4 | 508 | 504 | 120 | 0 |
| camera.hal5 | 508 | 504 | 120 | 0 |
| camera.hal6 | 508 | **520** | 120 | 0 |
| camera.hal7 | 508 | 504 | 120 | 0 |
| camera.hal8 | 508 | 500 | 116 | 0 |
| camera.hal9 | 508 | 500 | 116 | 0 |
| camera.hal10 | 508 | 504 | 120 | 0 |
| camera.hal11 | 124 | absent | absent | 0 |
| camera.hal12 | 124 | absent | absent | 0 |

The baseline is the `Faz4.2` bracket taken in this same state on 2026-09-05, not a quoted figure.
Delta is zero on all thirteen ids: the artifact's surface is unchanged since Phase 3 closed, which
is the point — Phase 3 was measured on exactly this surface.

**The distribution fact `QAS-04` requires be visible, stated rather than omitted:** the shipped
surface is **broader** than the project once intended to ship. The narrowing that would have
reduced it is retired because `IMPL-49` measured it as preventing AGC from launching, 3/3 at two
independent bisection stages. Anyone distributing this patch is distributing the broad table
deliberately.

Two observations recorded, neither in this sub-plan's scope:

- `camera.hal6` publishes `d000b` `int64[520]` against `d000a` `int32[508]` — 130 duration rows
  for 127 stream-configuration rows. It is the only id where `d000b` exceeds `d000a`.
- `camera.hal11` and `camera.hal12` still publish `d000a` with no `d000b` and no `d000c` at all
  (`FIND-4.2-02`, open, undiagnosed).

## 3. F4.4-02b — `FIND-4.5-01` disposition

`activeArray` against `pixelArray` for **every** camera id under the consolidated artifact:

| Camera id | `activeArraySize` (f0000) | `pixelArraySize` (f0006) | Consistent? |
|---|---|---|---|
| camera.hal0 | `[0 0 4096 3072]` | `[4096 3072]` | yes |
| camera.hal1 | `[0 0 3264 2448]` | `[3264 2448]` | yes |
| camera.hal2 | `[0 0 4096 3072]` | `[4096 3072]` | yes |
| camera.hal3 | `[0 0 4096 3072]` | `[4096 3072]` | yes |
| camera.hal4 | `[0 0 4096 3072]` | `[4096 3072]` | yes |
| camera.hal5 | `[0 0 4096 3072]` | `[4096 3072]` | yes |
| camera.hal6 | `[0 0 4096 3072]` | `[4096 3072]` | yes |
| camera.hal7 | `[0 0 4096 3072]` | `[4096 3072]` | yes |
| camera.hal8 | `[0 0 3264 2448]` | `[3264 2448]` | yes |
| camera.hal9 | `[0 0 3264 2448]` | `[3264 2448]` | yes |
| camera.hal10 | `[0 0 4096 3072]` | `[4096 3072]` | yes |
| camera.hal11 | `[0 0 12000 9000]` | `[12000 9000]` | yes |
| camera.hal12 | `[0 0 12000 9000]` | `[12000 9000]` | yes |

**Ids where `activeArray` exceeds its own `pixelArray`: none. Thirteen of thirteen are
consistent.**

**Disposition of `FIND-4.5-01`: it does not arise on the consolidated artifact, measured rather
than assumed.** The front cameras `hal1`, `hal8` and `hal9` read `[0 0 3264 2448]`, not the
`[0 0 6528 4896]` the finding describes. The global raise the finding is about lives in
`agc-50mp-yama/hal-activearray-deneme.patch`, an experimental table that `IMPL-66` marked as an
experiment and that the shipped `hal-fullres.patch` does not contain. `hal0` likewise reads
`4096x3072`, not `8192x6144`, confirming the `f0000` write site is untouched by the shipped table.

No front-camera behavioural check is required to close it, because there is no inconsistency for a
consumer to break on. The finding is **not** closed as knowledge and **not** dismissed: it is
re-scoped as a **precondition on `Faz4.5`**, which is the sub-phase that would actually perform
the raise. If `Faz4.5` ever lands the `f0000` word, the per-camera-id consistency table above is
the before-state it must be re-measured against, and the front-camera behavioural question the
sub-plan specified becomes live at that point rather than this one.

This is a disposition, not a decision: no scoping change is proposed here and none is needed for
distribution of the current artifact.

## 3b. F4.4-04 — The AGC path, and F4.4-03 — the third-party consumer

Run 2026-09-05, user present, **two human shutter presses**, in one uninterrupted HAL state.
The HAL was `fe0245a4720fb07b01d96deef47f5569` throughout and no device write was made: the
20:25 opening bracket and both the 20:32 and 20:35 closing brackets diff to **zero lines** across
the 45-line deterministic region.

### Preconditions, audited by value rather than by presence

`prefs` md5 `21762bdcb09f107aad2f397351cf1337`, 12169 B, owner `u0_a450` mode `660` —
byte-identical to the state `Faz3.11` closed on. Inputs `pref_48m_key`=`0`,
`pref_camera_resolution`=`full`; derived back `4096x3072`, front `3264x2448`.

**Trap keys: 2 present, `pref_raw_key`=`0` and `pref_fix_resolution_key`=`0` — both inert.**
A bare `0/12` presence assertion would have failed here on a state that is measured harmless
(`FIND-3.7-02`); the per-key value audit is the correct check.

### F4.4-04 — AGC

Launched with `monkey … android.intent.category.LAUNCHER`, which arms nothing and takes no
photograph. The settings screen was not opened. Configured streams read before the shutter:

```
Stream[2]  Dims: 4096 x 3072, format 0x25   (RAW10)
Stream[3]  Dims: 4096 x 3072, format 0x23   (YUV_420_888)
```

That is the matching pair `Faz3.11` recorded as the correct configuration, on the open client
`org.codeaurora.snapcam` (device 2). Streams 0 and 1 are the 1440x1080 and 640x480 preview and
analysis readers.

| Measure | Result |
|---|---|
| File | `AGC_20260905_203001345.jpg`, md5 `4b53b325e0685b76e2c5001f596e272a`, 1141999 B |
| Dimensions | **3072x4096 = 12.58 MP** |
| Black fraction (`IMPL-40` method) | **0.0000** against the `< 0.01` threshold |
| Quadrants | `0.0000` / `0.0000` / `0.0000` / `0.0000` |

**Verdict: PASS.** Evidence `snapshots/20260905-2030__Faz4.4__F4404-agc-capture-ORIGINAL.jpg`.

### F4.4-03 — Open Camera

**The consumer had to be identified before it could be run, and the identification is the
durable result.** Open Camera is installed under the package name **`com.xiaomi.module.evaluation`**
— a disguised id — with activity `net.sourceforge.opencamera.MainActivity`. Its APK md5 is
`e4efeb07919bce10bc14f6f42e5b09f2`, **byte-identical** to the
`OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk` recorded in
`docs/reverse-engineering-toolchain.md` line 208. Version 1.55, installed 2026-08-20.

No `pm list packages` filter on "camera" or "open" finds it, and `pm path net.sourceforge.opencamera`
returns nothing. It was located through `dumpsys activity recents`, whose `baseIntent` carries the
`package/activity` pair. This falsifies `docs/raw-geometry-diagnosis.md` line 327, which records
Open Camera as "not run — `pm` keeps no record of the package after three `Success` installs";
`pm` does keep a record, under a name no search would reach. Raised as `FIND-4.4-02`.

Preferences read before the capture, unmodified: `preference_resolution` = `8192 6144`,
`camera_resolution_0` = `8192 6144`, `preference_photo_mode` = `std`, `preference_raw` = `no`,
`preference_quality` = `100`. The app opened **device 0** with a 1920x1440 preview stream.

| Measure | 20:34 capture | 20:30 capture |
|---|---|---|
| File | `IMG_20260905_203413.jpg`, 16816673 B | `IMG_20260905_203018.jpg`, 16026187 B |
| Dimensions | **8192x6144 = 50.33 MP** | **8192x6144 = 50.33 MP** |
| Black fraction | **0.0000** | **0.0000** |
| Quadrants | all `0.0000` | all `0.0000` |

**Verdict: PASS, measured numerically against the documented 50.3 MP and reproduced twice**, four
minutes apart, in the same HAL state. Evidence
`snapshots/20260905-2034__Faz4.4__F4403-opencamera-capture-ORIGINAL.jpg`.

**Capture accounting, stated with its limit.** `DCIM/Camera` went 214 -> 215 JPG with MP4 unchanged
at 6: one AGC photograph, no unplanned one. Open Camera writes to `DCIM/OpenCamera`, a folder the
accounting baseline did not cover, and two captures landed there (20:30 and 20:34). Both are the
user's deliberate presses and both are measured above; the accounting is therefore complete but was
not complete *at the time it was first asserted*, and the folder is named here so a later run
baselines both.

### The headline criterion

**`VAL-AGC` PASS — the coexistence criterion is met.** In one HAL state
`fe0245a4720fb07b01d96deef47f5569`, with zero field changes across the bracket:

- **AGC launches and captures a measured-clean 12.58 MP image** (black `0.0000`);
- **Open Camera captures 50.33 MP in the same state** (black `0.0000`, twice).

This is the criterion `IMPL-49` showed a count-only validation silently violates, and section 8 of
the sub-plan makes it the condition of distributability. It is satisfied on measurement.

## 4. Work items — ALL TEN COMPLETE

`F4.4-01`, `F4.4-02`, `F4.4-02b` in `IMPL-67`; `F4.4-03` and `F4.4-04` in `IMPL-68` (section 3b);
`F4.4-05` through `F4.4-09` in `IMPL-70`, 2026-09-06. Every item that needed the device got it,
and the five that needed a human action cost **five shutter/record presses in total** — three rear,
two front — because the ten-mode pass was run by the `Faz2.3` programmatic method rather than by eye.

| Item | Status | Where |
|---|---|---|
| F4.4-01 — stream configuration surface | done | section 1 |
| F4.4-02 — array entry count | done | section 2 |
| F4.4-02b — `FIND-4.5-01` disposition | done | section 3 |
| F4.4-03 — third-party consumer | done | section 3b |
| F4.4-04 — the AGC path | done | section 3b |
| F4.4-05 — stock camera and video, front and rear | done | section 5 |
| F4.4-06 — ten-mode surface | done | section 6 |
| F4.4-07 — exclusion-boundary transitions | done | section 7 |
| F4.4-08 — reboot persistence | done | section 8 |
| F4.4-09 — `CQ-07` | done | section 9 |

## 5. F4.4-05 — The stock camera and video path, front and rear

Run 2026-09-05 21:33 (rear) and 21:37 (front). App `com.android.camera/.Camera`, which is the
stock camera and is **not** AGC (`org.codeaurora.snapcam`, an AGC port under that package name)
and not Open Camera (`com.xiaomi.module.evaluation`). Section 11 of the sub-plan requires the
front camera here, and `FIND-3.7-03` records front-camera **image** behaviour as unmeasured
across all of Phase 3 — so the front rows below are the first in the project.

Method: JPEG dimensions from the **SOF marker**, video dimensions from `tkhd` and frame rate from
`stts`/`mdhd` in the **MP4 container**. Never from a filename or a UI label. Playback is the
user's verdict; every dimension is measured.

| # | Check | Rear | Front |
|---|---|---|---|
| 1 | Opens, live preview | **PASS** — Device 6, `Stream[0]` SurfaceTexture 1440x1080 fmt `0x22` State 4, crash buffer empty | **PASS** |
| 2 | Shutter completes | **PASS** — `3072x4096` = **12.58 MP**, black `0.0000`, all quadrants `0.0000` | **PASS** — `4896x6528` = **31.96 MP**, black `0.0002` |
| 3 | 1080p60 | **PASS** — container `1920x1080` @ **60.0 fps** (430 frames / 7.161 s) | **PASS** — container `1920x1080` @ **59.9 fps** (407 frames / 6.792 s) |
| 4 | 4K60 | **PASS** — container `3840x2160` @ **59.8 fps** (446 frames / 7.458 s) | **NOT OFFERED** — the front camera does not expose a 4K profile |
| 5 | Playback | **PASS** (user-confirmed) | **PASS** (user-confirmed) |

Compared against `docs/consumer-survey.md` rows 2, 4 and 5, whose recorded values are
`3072x4096` = 12.6 MP, `1920x1080 @ 60.1 fps` and `3840x2160 @ 60.0 fps`. **The rear rows match
the reference on all three.** Invariant 5 holds.

**Front 4K60 is recorded as a measured absence, not as a failure.** The profile is not offered by
the stock camera on the front sensor; no substitute profile was silently swapped in to manufacture
a pass. The 1080p row was captured from a profile the user read in the menu as *1080p50*, while
the container measures **59.9 fps**; the container is authoritative under this project's method, so
the capture passes and the discrepancy is recorded as a **UI-label question, not a capture defect**.
It is not raised as a finding because nothing in the artifact under validation is implicated.

**The front camera emits an image twice its reported array in each axis — see `FIND-4.4-04`.**
`activeArray` and `pixelArray` both read `[3264 2448]` on `hal1`/`hal8`/`hal9`, and the emitted
JPEG is `6528x4896`. That is exactly 2x per axis, the same relationship the rear shows
(`[4096 3072]` reported, Open Camera captures `8192x6144`). It is recorded, routed, and not acted on.

Evidence: `snapshots/20260905-2133__Faz4.4__F4405-rear-measurements.txt`,
`snapshots/20260905-2133__Faz4.4__F4405-rear-stockcam-ORIGINAL.jpg`,
`snapshots/20260905-2137__Faz4.4__F4405-front-measurements.txt`,
`snapshots/20260905-2137__Faz4.4__F4405-front-stockcam-ORIGINAL.jpg`.
The two rear videos and the front video are measured here but **not** stored under `snapshots/`
(62 MB combined, and no prior snapshot stores video); they remain on the device under
`/sdcard/DCIM/Camera/` as `VID_20260905_213308.mp4`, `VID_20260905_213321.mp4`,
`VID_20260905_213741.mp4`.

## 6. F4.4-06 — The ten-mode surface against the regression record

Run 2026-09-06 12:25-12:31 by the **`Faz2.3` rows 7-11 method**, which that pass
defines and validates: `setmode.sh` per mode over CLI, a smoke snapshot per mode,
then AGC launched with `monkey … LAUNCHER 1` (documented as arming no trap key and
taking no photograph), scored on the crash buffer, the resumed activity and a
`screencap` luminance sample over the central 50%. **No shutter press was spent.**
`F4.4-06`'s criterion is "layer state and camera open per mode"; it does not require a capture.

Every prediction in `docs/regression-v2.1.md` section 2 is compared, not just the ones that moved:
sensor md5, sensor variant, `hal.state`, `camera.hal0` streamcfg, and both mount counts.

| # | Mode | sensor md5 | variant | `hal.state` | `hal0` cfg | mounts | Resumed activity | Crash | Preview sample | Verdict vs reference |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `stock` | `9e4d0fe1…` | `stock` | `stock` | 440 | 1/1 | CameraLauncher | 0 | LIVE mean=119.5 sd=53.9 | **PASS** |
| 2 | `dcgA` | `d6f72a6d…` | `dcgA` | `stock` | 440 | 1/1 | CameraLauncher | 0 | LIVE mean=118.5 sd=54.0 | **PASS** |
| 3 | `dcgB` | `ee73da4e…` | `dcgB` | `stock` | 440 | 1/1 | CameraLauncher | 0 | LIVE mean=119.0 sd=54.3 | **PASS** |
| 4 | `ln2` | `8dbc3f52…` | `ln2` | `stock` | 440 | 1/1 | **DefaultErrorActivity** | **FATAL** | n/a - error screen, not a preview | **FAIL, reproduces `FIND-2.3-02`** |
| 5 | `ln4` | `fd959e19…` | `ln4` | `stock` | 440 | 1/1 | **DefaultErrorActivity** | **FATAL** | n/a - error screen, not a preview | **FAIL, reproduces `FIND-2.3-02`** |
| 6 | `ln2s` | `2a65a521…` | `ln2s` | `stock` | 440 | 1/1 | CameraLauncher | 0 | LIVE mean=115.1 sd=54.1 | **PASS** |
| 7 | `ln4s` | `4b7eb29d…` | `ln4s` | `stock` | 440 | 1/1 | CameraLauncher | 0 | LIVE mean=117.7 sd=53.4 | **PASS** |
| 8 | `ln2f` | `bf36d1df…` | `ln2f` | `stock` | 440 | 1/1 | CameraLauncher | 0 | LIVE mean=115.3 sd=52.0 | **PASS** |
| 9 | `ln4f` | `acae87e3…` | `ln4f` | `stock` | 440 | 1/1 | CameraLauncher | 0 | LIVE mean=119.9 sd=53.4 | **PASS** |
| 10 | `50mp` | `9e4d0fe1…` | `stock` | `**fullres**` | **456** | 1/1 | CameraLauncher | 0 | LIVE mean=120.5 sd=53.1 | **PASS** |

**All ten rows match the section 2 prediction table exactly** — every sensor md5, every
variant, every `hal.state`, every `hal0` streamcfg, and `sensor.mount.count` /
`hal.mount.count` both reading `1` in all ten. No mount stacking and no unapplied layer.

**`ln2` and `ln4` fail in AGC, and that is a reproduction rather than a regression.**
Both raise `FATAL EXCEPTION: 00UiWorker` in `org.codeaurora.snapcam` and resume
`com.agc.DefaultErrorActivity` instead of `CameraLauncher` — the identical signature
`docs/regression-v2.1.md` rows 2 and 8 recorded under `FIND-2.3-02`, which is already
routed to `Faz5.3`. The layer state for both modes is nonetheless exactly as predicted,
so the failure is in AGC's handling of those two blobs, not in the mode machinery.
**Nothing new is raised here and `FIND-2.3-02` is not re-raised.**

**A stated limitation of the luminance detector, so the table is not over-read.** On `ln2`
and `ln4` the sampler returned `mean=35.9 sd=29.0`, which its own thresholds
(`mean < 8 and sd < 6`) classify `LIVE` — but the frame it sampled is AGC's *error dialog*,
not a camera preview. The detector cannot tell a rendered error screen from a rendered
preview. **The resumed-activity check is what discriminates**, exactly as `Faz2.3` observed
when the same procedure caught these two rows. The preview column is recorded as `n/a` for
them rather than `LIVE`, and the luminance figures are omitted rather than quoted as a pass.

**Bracket.** Opening `snapshots/20260905-2130__Faz4.4__F4405-pre.txt`, closing
`snapshots/20260906-1231__Faz4.4__F4406-post.txt`. The comparable-region diff is
**zero lines across ten mode switches** — the device returned to the shipped `50mp` state
byte-identically. Per-mode snapshots are `snapshots/20260906-1225__Faz4.4__F4406-<mode>.txt`, ten files.

**The preference pin survived the whole pass untouched.** After ten mode switches and ten
AGC launches the preference file is **byte-identical** — md5 `21762bdcb09f107aad2f397351cf1337`,
12169 bytes — and the per-key trap audit still reads `pref_raw_key` `0` and
`pref_fix_resolution_key` `0`. This is `Faz3.10`'s stickiness result confirmed on an axis
that matrix did not cover, and it is evidence that **`FIND-3.10-02`'s unknown re-arming
route is not the CLI mode-switch path**. Capture accounting: 222 → 227 files, all five
attributable to `F4.4-05`; the `monkey` launches took no photograph, as documented.

## 7. F4.4-07 — Both exclusion-boundary transitions (invariant 4)

**Satisfied by measurement from the `F4.4-06` pass rather than by a separate run**, which is
stated plainly rather than glossed: the ten-mode sequence begins at `50mp` and ends at `50mp`,
so it crosses the boundary in both directions, and every snapshot records *both* layers.

| Transition | Direction | Sensor layer | HAL layer | Verdict |
|---|---|---|---|---|
| `50mp` → `stock` | HAL layer released | stays `stock` / `9e4d0fe1…`, mount 1 | `fullres` → `stock`, mount 1 | **PASS** |
| `ln4f` → `50mp` | sensor layer released | `ln4f` / `acae87e3…` → `stock` / `9e4d0fe1…`, mount 1 | `stock` → `fullres`, mount 1 | **PASS** |

**The invariant holds on all ten rows, not only on the two transitions.** Invariant 4 says the
layers exclude each other. Across the whole pass there is **no snapshot in which**
**`sensor.live.variant` is non-`stock` while `hal.state` is `fullres`**: `hal.state` reads
`fullres` in exactly one row (`50mp`), and in that row the sensor variant is `stock`; in the
nine rows where a sensor blob is applied, `hal.state` reads `stock` every time. Mount counts
are `1`/`1` throughout, so neither layer is stacking or silently absent.

`Faz4.3`'s consolidation did not change the control flow enforcing this — which was the risk
section 11 of the sub-plan named, and it is now measured rather than assumed.

## 8. F4.4-08 — Reboot persistence for the consolidated state

Run 2026-09-06 12:31 (pre) and 12:34 (post). The device was already at `50mp`, so the sub-plan's
"set `50mp`, reboot" reduces to the reboot. **The reboot is verified as real rather than assumed:**
`/proc/uptime` read **73.6 s** afterwards against roughly fifteen hours before, so `wait-for-device`
did not simply reconnect to the pre-reboot session — a failure mode that would have produced a
false pass here.

| Reading | Post-reboot value |
|---|---|
| `mode.file` | `50mp` |
| `hal.live.md5` | `fe0245a4720fb07b01d96deef47f5569` |
| `hal.state` | `fullres` |
| `hal.mount.count` | `1` |
| `sensor.live.md5` | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` (stock) |
| `sensor.mount.count` | `1` |
| `camera.hal0` | `streamcfg=456` |
| `agc.pref_48m` / `agc.pref_resolution` | `0` / `full` |
| `agc.photo_size.back` | `4096x3072` = 12.58 MP |

**The comparable-region diff between the pre-reboot and post-reboot brackets is zero lines.**
The consolidated HAL state reapplies through `post-fs-data.sh` with no drift, and the mount count
of `1` shows the boot path applied the layer once rather than stacking it. The AGC pin survived
alongside it, and the per-key trap audit still reads `pref_raw_key` `0` and
`pref_fix_resolution_key` `0` with the preference file byte-identical at
`21762bdcb09f107aad2f397351cf1337`. Evidence:
`snapshots/20260906-1231__Faz4.4__F4406-post.txt` and
`snapshots/20260906-1234__Faz4.4__F4408-post-reboot.txt`.

## 9. F4.4-09 — `CQ-07`, the smallest correct HAL patch

**The first half of the answer criterion is recorded as SUPERSEDED rather than as a failure**, which
is what section 6 of the sub-plan requires. `CQ-07`'s criterion read "A patch adding RAW only at
full resolution, with duration rows". `DEC-14` retired the narrowing objective, and `IMPL-49`
*measured* why the retired form cannot be met: a patch adding RAW only at full resolution stops AGC
from launching, 3/3 at two independent bisection stages. Reporting a failure against that half would
be reporting a failure against a condition the project deliberately abandoned on evidence.

**The answer is `ishtar-cam-modes/blobs/hal-fullres.patch` — the canonical table, unchanged.**
Applied to stock `c3fa63a86ee3ecaf9fbf02005d35f6b5` it produces
`fe0245a4720fb07b01d96deef47f5569`, byte-identical to the HAL the device runs.

*Smallest*, established structurally rather than asserted: `IMPL-65` verified all **16** stock-column
escapes against the stock binary with **0/16 mismatches** and recomputed both endpoints by
application rather than transcribing them; `IMPL-66` then established that consolidation adds
**zero** entries and produces **no third HAL state**, so the smallest correct patch is the one that
already ships. Nothing was added to it by Phase 4.

*Correct*, where correctness now includes the thing the retired criterion would have broken — AGC
launching — and is measured on nine axes rather than argued:

| Evidence | Result |
|---|---|
| AGC launches and captures | 12.58 MP, black `0.0000`, reproduced three times (`IMPL-61`, `IMPL-68`) |
| Open Camera, same HAL state | 50.33 MP, black `0.0000`, reproduced twice (`IMPL-68`) |
| Duration rows | every OUTPUT entry has its `d000b` row, zero missing (`IMPL-64`) |
| Stock camera, rear | opens, previews, 12.58 MP clean, 1080p60, 4K60 (section 5) |
| Stock camera, front | opens, 31.96 MP clean, 1080p60; 4K60 not offered (section 5) |
| Ten-mode surface | all ten match the section 2 prediction table (section 6) |
| Exclusion boundary | invariant 4 holds in both directions and on all ten rows (section 7) |
| Reboot persistence | zero-line diff across a verified real reboot (section 8) |
| Array consistency | 13/13 camera ids consistent, zero raised arrays (section 3) |

**What remains unsatisfied is recorded explicitly rather than folded into the answer.**

- **`ln2` and `ln4` fail in AGC.** Pre-existing, reproduced identically, `FIND-2.3-02`, already
  routed to `Faz5.3`. Their layer state is exactly as predicted, so the failure is AGC's handling
  of those two sensor blobs and is **not attributable to the HAL patch** this question is about.
- **RAW10 is absent at `8192x6144`.** `FIND-4.4-01`. This falsifies the *wording* of an acceptance
  criterion, not the artifact: the criterion was written when Phase 4's product was expected to be
  the `raw50` widening, and the user's broad-emission ruling selected the canonical table instead.
- **`hal11`/`hal12` publish `d000a` with no `d000b` and no `d000c`.** `FIND-4.2-02`, undiagnosed,
  unchanged by this phase.
- **Scope.** One device, one ROM, one HAL state. The answer is not claimed beyond that.

**`CQ-07` moves from `open` to `answered`.** `Project-Comprehension.md` is updated with the answer
and with the supersession, which is where amending the question's own wording belongs.

## 10. Findings raised

**`FIND-4.4-01` (P2, open, routed to the user).** `Main-Planing.md`'s amended Phase 4 acceptance
signal — "`dumpsys media.camera` shows RAW10 at 8192x6144 with correct duration rows" — and this
sub-plan's first acceptance criterion, which quotes it, are **falsified against the artifact the
user's own broad-emission ruling selected**. Section 1 measures zero RAW-family entries at
8192x6144 on camera 3. The criterion was written when Phase 4's product was expected to be the
`raw50` widening; `IMPL-66` established the product is the canonical table unchanged, which never
carried those rows.

This is the same sentence `AUDIT-FIX-30` and `AUDIT-FIX-35` are already pending on, and the same
one `FIND-4.2-01` bears on through its "plus matching duration rows" clause. It is recorded here
rather than repaired: `Main-Planing.md` is not edited without the user's instruction, and the
three now converge on a single edit.

**Nothing in the measured artifact fails.** The finding is against the criterion's wording, not
against the patch.

**`FIND-4.4-02` (P3, open, routed to `Faz9.3`).** `docs/raw-geometry-diagnosis.md` line 327 records
Open Camera as "**not run** — `pm` keeps no record of the package after three `Success` installs".
Measured false: the package exists as `com.xiaomi.module.evaluation` with activity
`net.sourceforge.opencamera.MainActivity` and APK md5 `e4efeb07919bce10bc14f6f42e5b09f2`, and it
captured 50.33 MP twice in this session. The claim is a stale operator-facing statement of exactly
the class `Faz9.3`'s documentation pass owns; it is not corrected here because
`docs/raw-geometry-diagnosis.md` is `Faz4.6`'s output and this sub-plan routes rather than repairs.
The disguised package name itself is written into `Project-Ontology.md` so no later session repeats
the search that failed.


**`FIND-4.4-04` (P3, open, routed to `Faz4.5`).** The front camera emits a **31.96 MP**
(`4896x6528`) JPEG while `activeArray` and `pixelArray` both read `[3264 2448]` on `hal1`, `hal8`
and `hal9` — the output is exactly **2x the reported array in each axis**. The rear shows the same
relationship: reported `[4096 3072]`, and Open Camera captures `8192x6144`. **Full-resolution
capture is therefore not gated on the active-array raise**, which is direct evidence bearing on
`Faz4.5`, the sub-phase that would land the `f0000` word, and on the precondition `IMPL-67`
re-scoped onto it when it disposed of `FIND-4.5-01`. Measured, not acted on: `Faz4.4` routes rather
than repairs, and whether the raise is still worth landing is `Faz4.5`'s decision with its own owner.
The images are clean at both ends (rear black `0.0000`, front black `0.0002`), so nothing here is a
defect — it is a constraint on how `Faz4.5`'s premise should be read.
