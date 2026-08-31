# Ten-Mode Regression Record — ishtar-cam-modes v2.1

> Faz 2.3. The project's first written regression record.
> Build under test: `ishtar-cam-modes` **v2.1 / versionCode 12**, flashed 2026-08-31.
> Baseline reference: **`BASELINE-2026-08-31-V21`** =
> `snapshots/20260831-1607__faz2.2__post-flash-v2.1-baseline.txt`.
>
> This record verifies **function, not image quality**. Quality was measured
> separately and is recorded in `ishtar-cam-modes/Kullanim.txt:18-34`; it is out
> of scope here and is not re-measured.

## 1. Session Start State

The device was **not** at the baseline when this pass began. Faz 2.2 closed with
the user exercising the `50mp` tile, so the start state is recorded explicitly
rather than assumed, as the sub-plan requires.

Start snapshot: `snapshots/20260831-1636__faz2.3__session-start.txt`

| Field | Baseline `BASELINE-2026-08-31-V21` | Faz 2.3 start | Same? |
|---|---|---|---|
| `module.version` / `versionCode` | v2.1 / 12 | v2.1 / 12 | yes |
| `mode.file` | *(absent)* | `50mp` | **no** — written by the user's tile tap |
| `sensor.live.md5` | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` | yes (`50mp` forces the sensor layer to stock) |
| `sensor.mount.count` | 1 | 1 | yes |
| `hal.state` | `stock` | **`fullres`** | **no** |
| `hal.mount.count` | 1 | 1 | yes |
| `camera.hal0` streamcfg | 440 | **456** | **no** — the fullres patch |
| `agc.apk.md5` | `ce65f862c990e2acc02be356f75a7122` | same | yes (patched build) |
| `prefs.trap.count` | 2 | 2 | yes — still armed; blocks Phase 3, not this pass |

The pass ends by returning the device to `stock`, i.e. to the baseline layer
state.

## 2. Expected State Per Mode

Fixed **before** the pass, so that each row is a comparison against a prediction
rather than a description of whatever was observed.

The nine on-device blobs in `/data/adb/modules/ishtar_cam_modes/blobs/` were
verified **byte-identical** to the nine tracked sources in
`ishtar-cam-modes/blobs/` (all nine md5s equal, 2026-08-31). The flashed module
therefore carries the sources this repository tracks, and the md5 column below
is a valid per-mode discriminator.

| Mode | Driving layer | Expected `sensor.live.md5` | Expected `sensor.live.variant` | Expected `hal.state` | Expected `camera.hal0` streamcfg |
|---|---|---|---|---|---|
| `stock` | sensor | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` | `stock` | `stock` | 440 |
| `50mp` | **HAL** | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` | `stock` | **`fullres`** | **456** |
| `dcgA` | sensor | `d6f72a6d2828093aa6dd57d6d3cc5a30` | `dcgA` | `stock` | 440 |
| `dcgB` | sensor | `ee73da4e8f4f542161e7faa2a8a2141e` | `dcgB` | `stock` | 440 |
| `ln2` | sensor | `8dbc3f526d1af9c77c3fdae0fcb4204a` | `ln2` | `stock` | 440 |
| `ln4` | sensor | `fd959e19366fc91ccff513e8eef676f3` | `ln4` | `stock` | 440 |
| `ln2s` | sensor | `2a65a52174e66b49f81249f7fbb2dfd6` | `ln2s` | `stock` | 440 |
| `ln4s` | sensor | `4b7eb29de71ca9e4eaa31d55406a305c` | `ln4s` | `stock` | 440 |
| `ln2f` | sensor | `bf36d1df17a8e7ce693c7858aaf019ac` | `ln2f` | `stock` | 440 |
| `ln4f` | sensor | `acae87e3018ce542ff26b50dfdfcc952` | `ln4f` | `stock` | 440 |

`sensor.mount.count` and `hal.mount.count` must read **1** in every row. A count
above 1 means mounts are stacking; a count of 0 means the layer is not applied.

### 2a. The RAW-depth discriminator — a prediction under test

`FIND-2.2-02` (closed in IMPL-12) established that the RAW format advertised on
`camera.hal0`'s `4096x2304` and `4096x3072` rows tracks **sensor blob content**,
not mount presence: format `37` is RAW10, format `38` is RAW12. It costs no
reboot and gives a second, independent per-mode discriminator.

This pass uses it as a **prediction to be tested**, not as an acceptance
criterion. A miss is recorded as evidence about the blob, not as a mode failure.

| Mode | Documented bit depth | Predicted format | Basis |
|---|---|---|---|
| `stock`, `50mp` | 10-bit | `37` | Observed at baseline and at session start. |
| `dcgA`, `dcgB` | 12-bit | `38` | `Kullanim.txt:18` — "12-bit cikis + DCG secici". |
| `ln2f`, `ln4f` | 12-bit | `38` | `Kullanim.txt:28,31` — "LN4 + 12-bit", same for LN2. |
| `ln2s`, `ln4s` | 10-bit | `37` | `Kullanim.txt:33` — "10-bit LN". |
| `ln2`, `ln4` | **not documented** | **no prediction** | `Kullanim.txt:36-38` patches sensor mode 1 only. Record the observed value. |

### 2b. Measured result — the prediction holds, but the discriminator does not

Five observations, all with the mounted blob's md5 verified in the same snapshot:

| # | Time (UTC) | Mode | Set by | Blob md5 verified | Advertised format |
|---|---|---|---|---|---|
| 1 | 16:36 | `50mp` (sensor stock) | tile (Faz 2.2) | `9e4d0fe1…` | `37` |
| 2 | 16:51 | `ln2f` | **tile**, AGC reopened by user | `bf36d1df…` | **`37`** |
| 3 | 16:54 | `dcgB` | CLI | `ee73da4e…` | `38` |
| 4 | 16:54 | `ln4f` | CLI | `acae87e3…` | `38` |
| 5 | 16:55 | `ln2f` | **CLI** | `bf36d1df…` | **`38`** |

**Rows 2 and 5 are the same blob, byte-identical, with `sensor.mount.count` = 1
in both, and they disagree.** The bit-depth prediction in section 2a is
therefore correct — every 12-bit mode measured over CLI advertises `38` — but
the advertisement is **not a pure function of the mounted blob**, which is what
`FIND-2.2-02` concluded and what this pass was told to rely on.

The one named difference between rows 2 and 5 is the path that set the mode: a
QuickSettings tile with the user subsequently reopening AGC, versus
`setmode.sh` over CLI. Two observations cannot isolate the cause, so this is
recorded as `FIND-2.3-01` (section 9) and a controlled re-test was run rather
than a mechanism being asserted.

**Controlled re-test — both obvious hypotheses eliminated.** Two further
snapshots were taken with `dcgB`, isolating one variable at a time:

| # | Time (UTC) | Mode | Set by | Camera app | Advertised format |
|---|---|---|---|---|---|
| 6 | 16:59 | `dcgB` | **tile** | **not opened** | `38` — correct |
| 7 | 17:01 | `dcgB` | tile | **open, session live** | `38` — correct |

Snapshot 6 eliminates *tile versus CLI*: the tile path republishes metadata
correctly. Snapshot 7 eliminates *a live camera client skewing `dumpsys`*: the
value is stable with a session held open. Neither of the two natural
explanations survives, and the anomaly did not reproduce.

The 16:51 reading is nonetheless real and is preserved in
`snapshots/20260831-1651__faz2.3__after-user-block1.txt`, where the `ln2f` md5
and the `37` rows sit in the same file. What remains untested is whether the
effect is specific to `ln2f`, or transient and tied to the rapid tile sequence
that preceded it. That single remaining hypothesis is folded into the tile
check in section 4 rather than chased separately — the sub-plan's section 11
names budget consumed by repetition as a risk to the higher-value checks.

**Consequence for this pass, stated plainly:** the RAW-format column is demoted
from a discriminator to an observation. Every row's SMOKE verdict rests on
`sensor.live.md5`, `sensor.live.variant`, the two mount counts and `hal.state` —
all of which are read directly off the live mount and none of which showed any
inconsistency. No row's verdict changes.

**Consequence beyond this pass:** `FIND-2.2-02` is qualified, not overturned.
Blob content does drive the advertisement; something else can also leave it
stale. Any Phase 3, 4 or 5 measurement that reads advertised metadata after a
mode change must establish that the metadata has republished, rather than
assuming the mount implies it.

### 2c. `ln2` splits the two rows — and it corroborates the documentation

Every mode measured before `ln2` moved both `4096` rows together: either both
`37` or both `38`. `ln2` is the first to **split them**:

| Row | `ln2` advertised format |
|---|---|
| `4096x2304` | `37` (RAW10) |
| `4096x3072` | `38` (RAW12) |

This is what `Kullanim.txt:36-38` predicts without saying so in these terms:
`ln2` and `ln4` are the legacy variants that patch **sensor mode 1 only**, where
every other variant patches a set of photo modes. A patch that reaches one
sensor mode should lift the bit depth on that mode's resolution and leave the
other alone — which is exactly the split observed. The documented requirement for
`overrideForceSensorMode=1`, and the pink banding when it is absent, follow from
the same single-mode scope.

Two consequences worth carrying forward. First, the RAW-depth reading must be
taken **per resolution row**, not collapsed to one value per mode; a check that
reported a single format for `ln2` would be wrong whichever value it picked.
Second, this is independent corroboration that the blob content genuinely drives
the advertisement in the normal case — which is what makes the unreproduced
16:51 reading in 2b anomalous rather than routine.

## 3. Per-Mode Rows

One row per mode. `SMOKE` is the automated verdict (md5, variant, mount counts,
HAL state all as predicted). `OPEN`, `PREVIEW` and `SHUTTER` are the user's.
A **black preview is a failure**, not a warning — it is the documented symptom
of Project-Ontology invariant 3 being violated.

Shutter is required for the four main modes only, per the sub-plan's scope.

| # | Mode | Driven by | Snapshot | SMOKE | RAW fmt | OPEN | PREVIEW | SHUTTER | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `50mp` | tile | `20260831-1636__faz2.3__session-start` | **PASS** — sensor `9e4d0fe1…`/`stock`, HAL `fullres`, hal0 **456**, mounts 1/1 | `37` (as predicted) | | | | |
| 2 | `ln2` | CLI | `20260831-1703__faz2.3__excl-50mp-to-ln2` | **PASS** — sensor `8dbc3f52…`/`ln2`, HAL `stock`, hal0 440, mounts 1/1 | **`37`@2304 / `38`@3072 — SPLIT** | **FAIL in AGC** (crash on launch); **opens in OpenCamera** | live in OpenCamera, no pink | n/a | **FAIL — `FIND-2.3-02`** |
| 3 | `50mp` (return) | tile (manual) + CLI (smoke) | `20260831-1702__faz2.3__excl-dcgB-to-50mp` | **PASS** — sensor `9e4d0fe1…`/`stock`, HAL `fullres`, hal0 **456**, mounts 1/1 | `37` | PASS | PASS | PASS | **PASS** |
| 4 | `dcgB` | tile (manual) + CLI (smoke) | `20260831-1654__faz2.3__mode-dcgB` | **PASS** — sensor `ee73da4e…`/`dcgB`, HAL `stock`, hal0 440, mounts 1/1 | `38` | PASS | PASS | PASS | **PASS** |
| 5 | `ln4f` | tile (manual) + CLI (smoke) | `20260831-1654__faz2.3__mode-ln4f` | **PASS** — sensor `acae87e3…`/`ln4f`, HAL `stock`, hal0 440, mounts 1/1 | `38` | PASS | PASS | PASS | **PASS** |
| 6 | `ln2f` | tile | `20260831-1651__faz2.3__after-user-block1` + `20260831-1655__faz2.3__mode-ln2f-cli-recheck` | **PASS** — sensor `bf36d1df…`/`ln2f`, HAL `stock`, hal0 440, mounts 1/1 in both | `37` tile / `38` CLI — see 2b, `FIND-2.3-01` | PASS | PASS | PASS | **PASS** |
| 7 | `dcgA` | CLI | `20260831-1729__faz2.3__mode-dcgA` | **PASS** — sensor `d6f72a6d…`/`dcgA`, HAL `stock`, mounts 1/1 | `38` | PASS — no fatal, `CameraLauncher` resumed | LIVE (mean 95.9, sd 58.2) | n/a | **PASS** |
| 8 | `ln4` | CLI | `20260831-1727__faz2.3__mode-ln4` | **PASS** — sensor `fd959e19…`/`ln4`, HAL `stock`, mounts 1/1 | **`37`@2304 / `38`@3072 — SPLIT** | **FAIL in AGC** — `FATAL EXCEPTION`, `DefaultErrorActivity` resumed | n/a (app never renders) | n/a | **FAIL — `FIND-2.3-02`** |
| 9 | `ln2s` | CLI | `20260831-1729__faz2.3__mode-ln2s` | **PASS** — sensor `2a65a521…`/`ln2s`, HAL `stock`, mounts 1/1 | `37` | PASS — no fatal, `CameraLauncher` resumed | LIVE (mean 91.7, sd 57.6) | n/a | **PASS** |
| 10 | `ln4s` | CLI | `20260831-1730__faz2.3__mode-ln4s` | **PASS** — sensor `4b7eb29d…`/`ln4s`, HAL `stock`, mounts 1/1 | `37` | PASS — no fatal, `CameraLauncher` resumed | LIVE (mean 99.3, sd 60.0) | n/a | **PASS** |
| 11 | `stock` | CLI | `20260831-1730__faz2.3__mode-stock` | **PASS** — sensor `9e4d0fe1…`/`stock`, HAL `stock`, mounts 1/1 | `37` | PASS — no fatal, `CameraLauncher` resumed | LIVE (mean 98.4, sd 59.2) | n/a | **PASS** |

**On the `OPEN` and `PREVIEW` columns for rows 7-11.** These were taken
programmatically rather than by eye: AGC was launched with `monkey`, the crash
buffer was read for `FATAL EXCEPTION`, the resumed activity was read from
`dumpsys activity`, and a raw `screencap` frame was sampled over the central 50%
of the display for mean luminance, standard deviation and non-black fraction.
A mode passes only if no fatal was logged, the resumed activity is AGC's
`CameraLauncher` rather than its `DefaultErrorActivity`, and the frame is not
black.

This is a **supporting** measure, not a replacement for `VAL-MANUAL`. It proves
the app reached a rendering state with varied content on screen; it does not
reproduce a human's judgement of a correct preview. Its discriminating power is
demonstrated in the opposite direction by rows 2 and 8, where the same procedure
caught the AGC failure that the layer-state check could not see. The detector's
`BLACK` branch was never triggered in this pass, so its sensitivity to a truly
black preview is asserted from its thresholds (`mean < 8` and `sd < 6`) rather
than exercised. The four main modes carry the user's direct visual confirmation
regardless.

Eleven rows for ten modes: `50mp` appears twice because it is both a mode row
and one side of the exclusion-boundary test in section 5.

### Recording gap in rows 2-5, and the `ln2` / `ln2f` correction

Rows 3, 4 and 5 carry the user's manual verdicts but **no smoke snapshot**: the
tile taps were made before each switch was bracketed, so only the end state
(`ln2f`, row 6) was captured. The manual half is real evidence and is kept; the
automated half is marked `missing` rather than inferred from the end state. Both
are re-run under brackets rather than reconstructed — this is exactly the
`AUTOPSY-P0-02` pattern the sub-plan's section 11 names, caught in the act.

Rows 4 and 5 therefore carry **split provenance**, and the table says so: the
`OPEN` / `PREVIEW` / `SHUTTER` verdicts come from the user's tile-driven run, the
`SMOKE` verdict from a later CLI-driven run of the same mode. This was justified
at the time by the layer state being produced by the same code either way — the
tile calls `action.sh`, which calls `setmode.sh`. Section 2b then found that
tile and CLI runs of `ln2f` disagreed on *advertised metadata* while agreeing
exactly on *layer state* (md5, variant, mount counts, `hal.state`). The split
provenance is sound for what the SMOKE column actually asserts, and unsound for
the RAW-format column — which is why that column is demoted to an observation in
2b and carries both readings for row 6.

**Row 2 was never run.** The QuickSettings button labelled **LN2 sets `ln2f`**,
not `ln2` — `Ln2Tile.java`'s `mode()` returns the string `ln2f`. Plain `ln2` is
unreachable from any tile and is CLI-only. The tap reported as "the ln2 button"
therefore produced row 6, not row 2, and `ln2` remains untested.

**One result survives the gap intact.** Five real mode transitions were made
through the tiles, including two crossings of the `50mp` exclusion boundary, and
`sensor.mount.count` and `hal.mount.count` both still read **1** afterwards.
Mount stacking is the specific failure section 5 exists to catch, and it did not
occur across five transitions. That is end-state evidence, not the bracketed
both-sides evidence F2.3-04 requires, so it supports the boundary test without
substituting for it.

**The camera application closing on every mode change is expected behaviour, not
a defect.** `setmode.sh:60-63` force-stops `CAM_APPS` — which includes
`org.codeaurora.snapcam` — as step 3 of `restart_camera`, after `cameraserver`
and the providers are already stopped. The comments at `setmode.sh:48-51` record
that force-stopping *before* `cameraserver` was the previous version's bug and
the cause of the black-preview lockup in invariant 3. The on-screen wait is
`wait_camera_list` plus a measured five-second margin (`setmode.sh:85-89`:
opening two seconds after restart silently fails, four seconds and later works).
The observed behaviour is therefore the invariant being honoured.

### Known-documented behaviour that is NOT a finding

Recorded here in advance so the pass does not misfile a documented defect as a
discovery:

- **`ln2` and `ln4` produce pink-banded photographs.** `Kullanim.txt:36-38`:
  they patch sensor mode 1 only and require `overrideForceSensorMode=1`, a
  **global** CamX setting that is not set. Marked "ESKI/REFERANS — Kullanmayin"
  (legacy/reference — do not use). Banding is expected; a **live** preview is
  still required, because banding is not blackness.
- **Video fails with `dcgB`, `ln4f`, `ln2f`.** `Kullanim.txt:43-45`. See
  section 6.
- **The `3360x2520` modes (12/13/20/21) are unpatched in `dcgB`** by design,
  `Kullanim.txt:47`.
- **`ln2s` / `ln4s` give no quality gain and are noisier than stock**,
  `Kullanim.txt:33`. Quality is out of scope; they must still switch and open.

## 4. Tile Synchronisation

Project-Comprehension section 6 names tiles as the highest-risk area: touched in
v1.4, v1.5, v1.7 and v2.1, and every revisit was a read-path or synchronisation
issue.

**The four tiles drive `50mp`, `dcgB`, `ln2f`, `ln4f`** — read directly from
`tile-app/java/com/ishtar/cammodes/{FullResTile,DcgTile,Ln2Tile,Ln4Tile}.java`,
whose `mode()` methods return exactly those strings. Plain `ln2` and `ln4` are
**not reachable from any tile** and are driven by CLI in this pass.

| Check | Expected | Observed | Verdict |
|---|---|---|---|
| `50mp` tile active | other three off | confirmed by user during the tile-driven run | **PASS** |
| `dcgB` tile active | other three off | confirmed by user, **after a cold boot** | **PASS** |
| `ln4f` tile active | other three off | confirmed by user during the tile-driven run | **PASS** |
| `ln2f` tile active | other three off | confirmed by user during the tile-driven run | **PASS** |
| Tile subtitle shows the active mode | yes | confirmed | **PASS** |
| Launcher entry renders (v2.1 fix, re-confirm) | icon visible | confirmed | **PASS** |
| WebUI agrees with the tiles | yes | **not checked** | not run |

The `dcgB` row is the strongest of these. It was read after the reboot in
section 7, with the tile state reconstructed from scratch rather than from
anything cached in a running process — which is the hardest case for the v2.1
change that made tile status read from the framework instead of a cache. Four
tiles, exclusive selection, correct after a cold boot.

The WebUI cross-check was not performed. It is one line of the sub-plan's scope
("confirming it reports the current mode consistently with the tiles") and is
recorded as not run rather than assumed; the tiles and the CLI agreed with the
live mount in every one of the eleven rows, which is the same underlying state
the WebUI reads.

## 5. Exclusion Boundary — Project-Ontology Invariant 4

`50mp` (HAL layer) and the sensor modes are mutually exclusive, enforced only by
shell control flow in `post-fs-data.sh:16-18` and `setmode.sh`. Both directions
are exercised **directly, without passing through `stock`**, which is the
transition that would expose a control-flow gap.

| Transition | Expected sensor | Expected HAL | Snapshot before | Snapshot after | Verdict |
|---|---|---|---|---|---|
| `dcgB` -> `50mp` | reverts to stock blob `9e4d0fe1…` | `fullres`, hal0 440 -> 456 | `20260831-1701__faz2.3__tile-dcgB-agc-open` | `20260831-1702__faz2.3__excl-dcgB-to-50mp` | **PASS** |
| `50mp` -> `ln2` | ln2 blob `8dbc3f52…` mounted | returns to `stock`, hal0 456 -> 440 | `20260831-1702__faz2.3__excl-dcgB-to-50mp` | `20260831-1703__faz2.3__excl-50mp-to-ln2` | **PASS** |

Both directions were crossed **directly**, without passing through `stock`, and
both are bracketed with a snapshot on each side. Every expected value moved and
nothing else did: the sensor blob reverted to stock exactly when the HAL layer
engaged and took the `ln2` blob exactly when it disengaged, `camera.hal0` tracked
440 <-> 456 with it, and `sensor.mount.count` and `hal.mount.count` both read
**1** in all four snapshots.

**Invariant 4 holds under direct transition in both directions.** The rule that
`Autopsy` section 6 flagged as "enforced by control flow in a 280-line shell
script rather than by a checked invariant" is, on this build, correctly
enforced. Mount stacking — the failure this test exists to catch — did not occur
here, nor across the five earlier tile-driven transitions in section 3.

The substitution of `dcgB` for the planned `ln2` on the first direction is
recorded rather than silent: the device was in `dcgB` when the bracket was
taken, and the transition tested is sensor-layer -> HAL-layer, for which any
sensor mode is an equivalent starting point. The second direction uses `ln2`
exactly as planned.

## 6. Video — Project-Ontology Invariant 5

Invariant 5 states 1080p60 and 4K60 must remain functional in every mode and
calls it a standing, user-validated acceptance criterion.

**Correction to how this defect was carried into the pass.** The Faz 2.3
briefing paraphrased `Kullanim.txt:43-45` as "video does not work — starting a
recording fails". The source does not say that. Its exact words are `VIDEO
calismiyor. dcgB / ln4f / ln2f aktifken video kaydi baslatinca **akis oluyor**`
— *smearing occurs* — followed by the parenthetical that names precisely which
sensor modes are unpatched: `SHDR 5/6/18/19, 8K 8, yavas cekim 9/22`.

The documented symptom is therefore **corrupted output on specific video sensor
modes**, not a refusal to record, and not all video. This distinction decides
what F2.3-06 must actually test: the at-risk profiles are the ones that select
an SHDR, 8K or high-frame-rate sensor mode, and a plain recording that avoids
them is expected to be clean.

| Mode | Profile | Consumer | Expected | Records? | Output clean? | Verdict |
|---|---|---|---|---|---|---|
| `dcgB` | 1080p (plain) | OpenCamera | clean — avoids the unpatched modes | **yes** | **yes, normal** | **PASS** |
| `dcgB` | video mode (any) | **AGC** | at risk | **no — cannot reach the recorder** | **preview black on entering the video section** | **FAIL** |
| `stock` | video mode (any) | **AGC** | works | **no** | **preview still black** | **FAIL** |
| `stock` | 1080p60 / 4K60 | AGC | works | *unreachable — see 6c* | | |
| `50mp` | video mode (any) | AGC | *unknown* | **no** | **black**, after reboot 2 | **FAIL** |
| `stock` | video mode (any) | AGC | works | **no** | **black**, after reboot 2 | **FAIL** |

The first row is already a meaningful result: recording in `dcgB` is **not**
categorically broken. That is a narrowing of the known defect, obtained by
testing a profile the documentation's parenthetical implies should be safe, and
finding that it is.

### 6a. The `dcgB` video failure, measured

Entering AGC's video section in `dcgB` blacks the preview and no recording can
be started. Evidence captured with the failure on screen
(`20260831-1740__faz2.3__reboot1-dcgB-persist` is the layer state; the log
extracts below are from the same minute):

- **The HAL rejected the stream configuration.** `camxhal3.cpp:2834
  configure_streams() HalOp: End CONFIG failed, logicalCameraId: 0, cameraId: 2`,
  preceded by `camxhal3.cpp:2781 … max_buffers : 0` twice. A failed
  `configure_streams` is a direct and sufficient explanation for a black
  preview: no stream was ever configured, so nothing can render.
- **The request was not a 60 fps one.** `camxhal3.cpp:2724 configure_streams()
  FPS: 14 ~ 30`. AGC's video section asked for a 14-30 range and was still
  refused, so this failure is not specific to the 60 fps profiles invariant 5
  names — it is broader than the criterion being tested.
- **`CSIPHYHw:4 AvailableResource = 0`**, with `CSIPHYHw:2` at 50 and the other
  four PHYs at 100. This string is the exact signature
  `Kullanim.txt:209-211` gives for the hardware-allocation leak. It is
  **ambiguous on its own**: a PHY legitimately in use by a live session also
  reads 0, so the value does not by itself distinguish a leak from normal
  allocation. It is disambiguated below.

**This is not the invariant 3 lockup.** That failure is defined by
`Kullanim.txt:207-208` as a black preview in **every** mode including `stock`,
recoverable only by reboot. Here the photo path in `dcgB` was working normally
minutes earlier and the failure appears only on entering the video section — a
mode-specific and section-specific failure, not a stack-wide one. The
disambiguation is the documented workaround itself: `Kullanim.txt:45` states
that `setmode.sh stock` restores video **without** a reboot. If video works in
`stock` with no reboot, the allocation was never leaked and `dcgB` is the cause;
if it stays black, the stack is locked and a reboot is required.

### 6c. The documented no-reboot workaround did not work

`Kullanim.txt:45` states, for the video limitation: `Video icin once "setmode.sh
stock" yapin -- yeniden baslatma GEREKMIYOR` — *for video, first run `setmode.sh
stock`; a reboot is NOT required.* That instruction was followed exactly, and
the snapshot `20260831-1744__faz2.3__video-workaround-stock` confirms the device
reached a clean `stock` state: sensor `stock`, HAL `stock`, both mount counts 1.

**AGC's video preview remained black.** The failure signature in `stock` is
byte-for-byte the same as in `dcgB`:

```
camxhal3.cpp:2724 configure_streams() FPS: 14 ~ 30
camxhal3.cpp:2781 configure_streams()   max_buffers  : 0
camxhal3.cpp:2834 configure_streams() HalOp: End CONFIG failed,
                                      logicalCameraId: 0, cameraId: 2
CSIPHYHw : 4, AvailableResource = 0
```

The camera provider's PID changed from `1559` to `24545` between the two
readings, so `restart_camera` did genuinely tear down and rebuild the provider;
the failure survived that. `Kullanim.txt:212` says exactly this of the leak
state — `COZUM: YENIDEN BASLATMA. Kamera servislerini oldurmek yetmiyor.`
(*Solution: reboot. Killing the camera services is not enough.*)

**Two hypotheses remain, and one reboot separates them.** Either the stack is in
the documented leaked-allocation state, entered at some point during this pass
and not clearable by a service restart — in which case a reboot restores video
and `dcgB` is exonerated as the cause; or AGC's video path is broken on this
device independently of the module, in which case video stays black in `stock`
after a reboot and the module is not implicated at all.

Note that the second hypothesis has never been excluded by this project's
records: every video claim in `Kullanim.txt` concerns *mode-dependent*
corruption, and no entry states that AGC video was ever verified working on this
build. The reboot in section 7 is sequenced to answer this.

### 6d. Resolution — the module is not the cause

The full matrix, four cells, all measured:

| Layer state | Reboot | AGC video preview |
|---|---|---|
| `dcgB` | after reboot 1 | black |
| `stock` | same session, workaround applied | black |
| `50mp` | after reboot 2 | black |
| `stock` | after reboot 2 | black |

**Both hypotheses from 6c are refuted, and the leak one is refuted twice over.**
On a fresh boot — uptime 1824 s, camera provider at its boot PID `1590` — the
signature is unchanged: `configure_streams() HalOp: End CONFIG failed,
logicalCameraId: 0, cameraId: 2`, with `FPS: 14 ~ 30`. A reboot is the
documented cure for the leaked-allocation state and it changed nothing.

**A correction to the project's own troubleshooting guide.**
`Kullanim.txt:209` presents `CSIPHYHw:4 AvailableResource=0` as the log
signature of the leak. That value was read **on a clean boot with the failure
present**, alongside `CSIPHYHw:2` at 50 and the remaining four PHYs at 100. It
is the normal steady-state reading for that PHY on this device, not evidence of
a leak. Anyone following that guidance would misdiagnose this failure — and
would reboot, as this pass did, to no effect. Routed to Faz 9.3.

**The failure is real, is a regression, and is not attributable to the module.**
The user confirms AGC video has worked on this phone previously, so this is a
change from a known-good earlier state rather than something that never worked.
But it reproduces identically in `stock` — the unmodified sensor blob with the
unmodified HAL, both mount counts at 1 — which is the module's own no-op
configuration. Nothing the module does distinguishes the failing states from the
passing ones, because `stock` fails too.

**The preference trap was investigated and excluded.** Both trap keys exist in
`org.codeaurora.snapcam_preferences.xml` and both read `0`:
`<string name="pref_fix_resolution_key">0</string>` and
`<string name="pref_raw_key">0</string>`. They are present but inactive, so they
are **not** a supported explanation for this failure, and this record does not
route them as one. `Faz 3.1` still owns clearing them for its own reasons. The
same file shows AGC configured for `pref_video_resolution=RES_1080P` and
`pref_video_fps_cm_key=FPS_30`, consistent with the `FPS: 14 ~ 30` in the log:
AGC is requesting an ordinary 1080p30 stream and being refused.

**What is not established.** The actual cause. Candidates that this pass did not
test, listed so Phase 3 does not have to rediscover them: the patched AGC build
itself (`ce65f862…`, a 50MP smali patch, never validated against the video
path); the `pref_camera_resolution=full` setting; and whatever makes AGC's video
use case select `cameraId 2` under `logicalCameraId 0`. Stock AGC
(`fa4066eb…`) is present in the workspace and would be the cheapest first
control, but installing it is a Phase 3 action, not a Faz 2.3 one.

**User impact is low and should be stated as such.** The user does not use AGC's
video section and intends to record with `mcpro24fps` — which is **not currently
installed** on the device (`pm list packages` returns no match), so that path is
unverified. OpenCamera records 1080p normally, including in `dcgB`, so video
capture on this device works; it is AGC's video path specifically that does not.

### 6b. The automated preview check would have missed this

The screencap detector described in section 3 was run against the black video
preview and returned **`LIVE`** — `mean=8.1`, `sd=33.5`, `nonblack_frac=0.099`.
The frame was roughly 90% black, but AGC's bright control chrome around the dead
preview surface pushed the standard deviation above the `sd < 6` threshold.

This is recorded rather than quietly fixed, for two reasons. It bounds what the
automated column in section 3 is worth: it can confirm a *working* app reached a
rendering state, and it caught the `ln2`/`ln4` crashes through the crash buffer
and resumed-activity checks, but it is **not** a reliable black-preview
detector and must not be presented as one. And it is the concrete justification
for keeping `VAL-MANUAL` user-performed, exactly as the sub-plan specifies —
the one black preview in this entire pass was found by the user's eyes and
missed by the instrument.

The `50mp` pair is an addition to the sub-plan's required four. It is worth the
two extra recordings: `50mp` is the **HAL** layer, the documented video defect is
a **sensor**-layer one, and IMPL-12 showed the fullres HAL patch reaches all
thirteen camera ids. Whether video survives the HAL layer is therefore both
untested and directly relevant to Phases 3 and 4.

## 7. Reboot Persistence — Both Layers

The boot path (`post-fs-data.sh`) is a different code path from the interactive
one (`setmode.sh`), so both layers are checked across a reboot.

| Layer | Mode set before reboot | Expected after boot | Snapshot | Verdict |
|---|---|---|---|---|
| sensor | `dcgB` | dcgB blob mounted, HAL `stock`, mount counts 1 | `20260831-1740__faz2.3__reboot1-dcgB-persist` | **PASS** — `mode.file` `dcgB`; sensor `ee73da4e…`/`dcgB`, size 1062250/1062250; HAL `stock`; mounts 1/1; RAW 38/38 |
| HAL | `50mp` | sensor stock, HAL `fullres`, hal0 456, mount counts 1 | `20260831-1817__faz2.3__reboot2-50mp-persist` | **PASS** — `mode.file` `50mp`; sensor forced to `9e4d0fe1…`/`stock`; HAL `fullres` `fe0245a4…`; hal0 **456**; mounts 1/1 |

Both layers reapply correctly through the boot path, which is a different code
path from the interactive one. The `50mp` row additionally confirms that the
boot path honours the exclusion rule — it forced the sensor layer to stock while
engaging the HAL layer, matching `post-fs-data.sh:16-18` — and that `hal_seed`
re-established the 27 MB HAL bind mount from the device's own stock binary
without the module shipping one.

### 7a. `FIND-1.5-03` — this pass owns it

`FIND-1.5-03` states that `post-fs-data.sh:66` copies the blob without verifying
it before bind-mounting. Reading both paths in this run sharpens the finding
into an **asymmetry between two code paths that do the same thing**:

- `setmode.sh:262-270` copies, `sync`s, then **re-reads the mounted target and
  compares its md5 to the source**, aborting with `HATA: dogrulama basarisiz` on
  a mismatch. The interactive path is verified.
- `post-fs-data.sh:66` runs `cat "$SRC" > "$ACT"`, checks only the shell exit
  status, sets ownership and context, and bind-mounts at line 72. **No md5
  comparison exists on the boot path.** The pre-copy guards at lines 54-61 check
  the *source* blob's presence and size, not the *result* of the copy.

The consequence is bounded, not alarming: a truncated or partial `$ACT` at boot
would be mounted silently, and the module would report the mode it intended
rather than the bytes actually in place. Nothing observed so far indicates this
has ever happened.

The reboot checks in this section are the measurement: `scripts/smoke.sh` reads
the **live** `sensor.live.md5` off the mounted target, which is precisely the
verification the boot path omits. If both post-reboot md5s match their expected
blob, the finding is confirmed as a latent robustness gap with no present
symptom. The code change itself is **not** made here — F2.3-08 routes it.

## 8. Invariant Coverage

| Invariant | What exercises it | Verdict |
|---|---|---|
| 3 — camera restart order runs client before HAL; violation blackens preview in every mode | The PREVIEW column of all eleven rows in section 3 | **HOLDS for the photo path.** No mode produced a black photo preview across ~15 transitions and 2 reboots. The black preview found in section 6 is confined to AGC's video section and appears in `stock` too, so it is not the invariant-3 symptom, which is defined as stack-wide. |
| 4 — `50mp` and the sensor modes are mutually exclusive | Both transitions in section 5, plus the `50mp` reboot in section 7 | **HOLDS.** Both direct transitions correct and bracketed; the boot path enforces it independently. |
| 5 — 1080p60 and 4K60 functional in every mode | Section 6 | **CANNOT BE ASSESSED — and that is itself the finding.** The 60 fps profiles were never reachable: AGC's video section fails `configure_streams` before any profile can be selected, in `stock` as well as `dcgB`. Invariant 5 is neither confirmed nor refuted for AGC on this build. `dcgB` 1080p in OpenCamera did record cleanly. |

## 9. Findings Routed

Failures are recorded and routed; none is repaired in place, per the sub-plan's
Out of Scope section.

| ID | Mode | Layer | Symptom | Owning phase | Status |
|---|---|---|---|---|---|
| FIND-1.5-03 | all | sensor (boot path) | `post-fs-data.sh:66` bind-mounts an unverified copy; `setmode.sh:262-270` verifies the same operation | *(to be set at F2.3-08)* | measurement pending section 7 |
| **FIND-2.3-01** | `ln2f` observed; scope unknown | HAL metadata | The advertised RAW format on `camera.hal0`'s `4096` rows is **not a pure function of the mounted blob**. The identical `ln2f` blob (`bf36d1df…`, mount count 1 in both snapshots) advertised `37` at 16:51 after a tile-driven change and `38` at 16:55 after a CLI-driven change. Qualifies `FIND-2.2-02`, which this pass was instructed to rely on as a no-reboot discriminator. | *(to be set at F2.3-08; candidate Faz 3.1, which owns measurement preconditions)* | **open** — controlled re-test in progress |

| **FIND-2.3-02** | `ln2`, `ln4` | sensor blob / GCam consumer | Both legacy modes **crash AGC on launch** with `java.lang.NullPointerException: Attempt to invoke virtual method 'boolean com.google.googlex.gcam.Gcam.f()' on a null object reference`, landing on `com.agc.DefaultErrorActivity`. Both are also the only two modes that advertise a **split** RAW format (`37`@4096x2304, `38`@4096x3072). OpenCamera opens and captures normally in `ln2`, so the camera stack itself is healthy. | **Phase 3** (owns the AGC/libgcam path) | **open** |

### The correlation, stated exactly

Across all ten modes, metadata consistency and AGC survival correlate perfectly:

| Advertised RAW rows | Modes | AGC on launch |
|---|---|---|
| **Unified** (both rows same format) | `stock`, `50mp`, `dcgA`, `dcgB`, `ln2s`, `ln4s`, `ln2f`, `ln4f` — 8 modes | opens, preview live — **8/8** |
| **Split** (`37`@2304, `38`@3072) | `ln2`, `ln4` — 2 modes | `Gcam.f()` NPE — **2/2** |

**What this is worth, and what it is not.** Eight-for-eight and two-for-two is a
clean correlation on the whole population of modes, not a sample. The mechanism
is also plausible on independent grounds: `Project-Ontology` records the libgcam
static-metadata invariant as this project's standing blocker, and an
`ImageReader`-style consumer that assumes one RAW format per camera is exactly
what a split set would break. But this pass did **not** manipulate the split
independently of the blob, so the causal claim is unproven — `ln2` and `ln4`
differ from the other eight in more than their advertised format.

**Why it is nonetheless a real asset.** Phase 3's whole difficulty is that
libgcam rejects metadata sets for reasons that are hard to observe. `ln2` and
`ln4` are a **reproducible, one-command negative control** for that invariant:
a state where GCam demonstrably refuses to initialise, reachable in about twelve
seconds, with a clear log signature. Phase 3 can use it to tell "my patch is
wrong" apart from "GCam is unhappy for an unrelated reason".

**Priority is low despite the failure.** `Kullanim.txt:36-38` marks both modes
`ESKI/REFERANS` and `Kullanmayin` — legacy, requiring a global CamX property
that is not set (confirmed here: `overrideForceSensorMode` reads empty). No user
is expected to select them. The value is diagnostic, not corrective; nothing
should be repaired to make `ln2` work in AGC.

**One documentation refinement.** `Kullanim.txt:38` predicts pink banding for
these modes. In `ln2`, OpenCamera's preview *and* a captured photo showed **no**
pink tint. That is consistent rather than contradictory — the patch touches
sensor mode 1 only, so banding appears only when the consumer actually lands on
that mode. The documented symptom is **conditional on the consumer's chosen
sensor mode**, not universal. Routed to Faz 9.3 with the rest of the
documentation work.

| **FIND-2.3-03** | all (module-independent) | AGC video path | AGC's video section shows a **black preview and cannot record**, in `stock` as well as `dcgB` and `50mp`, before and after a reboot — 4/4 cells. `configure_streams() End CONFIG failed, logicalCameraId: 0, cameraId: 2` with `FPS: 14 ~ 30`. A regression against a known-good earlier state, but reproduces in the module's no-op `stock` configuration, so not attributable to the module. Preference trap excluded (both keys read `0`). Cause not established; first control should be stock AGC `fa4066eb…`. | **Phase 3** (owns the AGC path) | **open**, P2 — real regression, low user impact |
| **FIND-2.3-04** | n/a | documentation | `Kullanim.txt:209` gives `CSIPHYHw:4 AvailableResource=0` as the log signature of the hardware-allocation leak. Measured on a clean boot with an unrelated failure present, that PHY reads `0` as its normal steady state. The stated signature is not diagnostic and would cause a misdiagnosis. | **Faz 9.3** | open, P3 |
| **FIND-2.3-05** | `ln2`, `ln4` | documentation | `Kullanim.txt:38` predicts pink banding for these modes unconditionally. In `ln2`, OpenCamera's preview and a captured photo showed no pink tint. The banding is conditional on the consumer selecting sensor mode 1, which the patch is scoped to. | **Faz 9.3** | open, P3 |
| **FIND-2.3-06** | n/a | documentation | `Kullanim.txt:45` states `setmode.sh stock` restores video with no reboot required. Applied exactly, with a verified clean `stock` state, it did not restore AGC video. The claim is unsupported on this build. Related to `FIND-2.3-03` and may resolve with it. | **Faz 9.3** | open, P3 |

`FIND-2.3-01` does not change any mode's verdict: every SMOKE verdict rests on
values read directly off the live mount, and none of those was ever
inconsistent. Its cost is to measurement *method* in later phases, where reading
advertised metadata after a mode change is a core technique.

**`FIND-1.5-03` is resolved as a measurement and stays open as a code change.**
Both reboots in section 7 mounted a byte-exact blob — `ee73da4e…` at
1062250/1062250 bytes for `dcgB`, and the correct stock blob under `50mp`. The
boot path's missing verification is therefore a latent robustness gap with no
observed symptom, exactly as predicted from source. Routed to **Faz 9.1** with
the other module-hardening work; the one-line fix is to mirror
`setmode.sh:262-270`'s md5 comparison into `post-fs-data.sh` before the
`mount --bind` at line 72. Not repaired here, per this sub-plan's Out of Scope.

## 10. Pass Summary

| Metric | Value |
|---|---|
| Modes with a completed row | **10 / 10** — none assumed, none skipped |
| Modes passing SMOKE (layer state) | **10 / 10** — every mode landed on its exact expected blob md5 |
| `sensor.mount.count` / `hal.mount.count` deviating from 1 | **0**, across ~17 transitions and 2 reboots |
| Modes passing OPEN + PREVIEW (photo path) | **8 / 10** — `ln2` and `ln4` fail in AGC |
| Black previews, photo path | **0** |
| Black previews, AGC video path | **4 / 4 states tested**, including `stock` |
| Exclusion transitions passing | **2 / 2**, bracketed on both sides |
| Reboot persistence passing | **2 / 2**, one per layer |
| Tile exclusivity checks passing | **6 / 7** — WebUI cross-check not run |
| Video verdicts | **5 recorded**; the 1080p60 / 4K60 profiles were **unreachable** in AGC |
| New findings routed | **6** — `FIND-2.3-01` … `FIND-2.3-06` |
| Pre-existing findings resolved | **1** — `FIND-1.5-03` measured |

**Overall verdict: the module passes; two defects were found outside it.**

Everything the module itself controls is correct. All ten sensor and HAL layer
states are exactly right, the exclusion rule holds in both directions and
through the boot path, mounts never stacked, both layers survive a reboot, the
tiles are exclusive and correct after a cold boot, and the photo path has a live
preview in every mode that AGC can open.

The two failures are at the edges. `ln2` and `ln4` crash AGC — two modes the
documentation already marks `Kullanmayin`, and the failure hands Phase 3 a
reproducible negative control for the libgcam invariant that has been blocking
it. AGC's video section is black in every state including `stock`, which is a
real regression but reproduces in the module's no-op configuration and so is not
the module's doing.

**Phase 3 is not blocked by an unrouted failure.** Every failure above has an
owning phase. `FIND-2.3-03` is the one Phase 3 must handle first, since it
concerns the same application Phase 3 measures in — but it affects the video
path, and Phase 3's subject is still capture.

**Comparison basis established.** This record is the first per-release
correctness evidence in the project. A Phase 3 or Phase 4 change that breaks a
sensor mode can now be distinguished from a pre-existing defect by diffing
against the eleven rows in section 3 and the snapshots they name.
