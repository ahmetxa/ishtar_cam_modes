# Consumer Compatibility Survey — `pixelArraySize` raised to 8192x6144

Faz 3.4. Answers `OQ-03`: *can `pixelArraySize` be raised without breaking other
consumers?* The answer names the consumers actually tested, so this file is a
table with a stated scope rather than a verdict sentence.

**The change under survey.** One word at `0x0166645c`, four-byte index
`5871895`, `ldr x1,[x4,#0x198]` -> `ldr x1,[x4,#0]`. Confirmed by `IMPL-20` to
move camera 3's `android.sensor.info.pixelArraySize` from `[4096 3072]` to
`[8192 6144]` while leaving `activeArraySize` and
`preCorrectionActiveArraySize` at `[0 0 4096 3072]`. Table:
`agc-50mp-yama/hal-pixelarray-deneme.patch`.

**Why the direction matters.** `OQ-03`'s own note records that the *opposite*
direction — raising the **active** array — is known to break AGC. This survey
therefore tested a change that had never been tried on this device.

**Bases tested.** The word was applied on **both** bases, because they are
different binaries and only the second is the configuration Phase 3 is aiming at:

| Base | md5 with the word | What it is |
|---|---|---|
| stock `c3fa63a8…` | `77083b7c099d4c68a9213476141c450d` | baseline plus one word |
| fullres `fe0245a4…` | `c539f04e6bbaedb907a5c987f16800ea` | the 50 MP HAL plus one word |

Both md5s were **predicted statically in `IMPL-20` and pre-committed into the
patch table before any device write**; both matched on application.

## 1. Results

Pre-change expectations are sourced from `docs/regression-v2.1.md`,
`snapshots/20260831-1607__faz2.2__post-flash-v2.1-baseline.txt` and `EV-04`.
All measurements are against AGC build `ce65f862…` installed (not opened —
see the exclusion below). JPEG dimensions are read from the **SOF marker** and
video dimensions and frame rates from the **MP4 container**, never from a
filename or a UI label.

| # | Consumer / surface | Pre-change expectation | Post-change result | Verdict |
|---|---|---|---|---|
| 1 | Stock camera — opens, live preview | Opens with live preview | Opens, live preview, on **both** bases. Crash buffer empty, no `DURDU:` line. | **PASS** |
| 2 | Stock camera — shutter, dimensions | No prior record | `3072x4096` = 12.6 MP in all three states (pre, stock+word, fullres+word) — **identical** | **PASS** |
| 3 | Open Camera — full-resolution capture | 50.3 MP (`EV-04`) | **`8192x6144` = 50.3 MP** on fullres+word. On stock+word it is `4096x3072` = 12.6 MP, the same as pre-change. | **PASS** |
| 4 | Video — 1080p60 | Records, output normal | `1920x1080 @ 60.1 fps` in **stock+word** and in **50mp+word**; user confirmed playback | **PASS** |
| 5 | Video — 4K60 | **No clean prior reading existed** | `3840x2160 @ 60.0 fps` in **stock+word** and in **50mp+word**; user confirmed playback. This row now has a baseline it never had. | **PASS** |
| 6 | Video — AGC video section | Already black before this change, in four states incl. plain `stock` | **Not tested — AGC is excluded by scope.** `FIND-2.3-03` stands; nothing here changes it. | **not tested** |
| 7 | Mode surface — sensor-layer mode | `dcgA`/`ln2s`/`ln4s`/`stock` all open | **`dcgA` opens with the word applied**, 0 crashes, live preview. **`dcgB` fails — but it fails identically WITHOUT the word, on stock HAL, on a fresh boot.** See `FIND-3.4-02`. | **PASS for `dcgA`; `dcgB` fails, not attributable** |
| 8 | Mode surface — HAL-layer `50mp` | Opens; `camera.hal0` 440 -> 456 rows | Opens; `streamcfg=456` **and** `pixelArray=[8192 6144]` together, and the 50.3 MP capture above came from this state | **PASS** |
| 9 | Framing / field of view | No controlled prior capture existed | **Controlled comparison achieved** — the phone was propped and not moved across the pre/post pair. Shelf edge, skirting line, plank seams and cable land at the same coordinates. Only auto-exposure differs. | **PASS — no FOV change** |

**The single most important row is 8 combined with 3.** This is the first time
`frame_raw_max` and `pixelArraySize` have both read `8192x6144` at the same
time, which is the state Project-Ontology invariant 6 describes — and Open
Camera still captured a clean 50.3 MP frame from it. Whether **libgcam**
accepts that state is Faz 3.5's question and is *not* answered here.

**A correction to this file's own earlier draft.** `F3.4-01` recorded row 3's
expectation as a flat 50.3 MP citing `EV-04`. That was imprecise: `EV-04` was
measured under the **fullres** HAL. At stock HAL, Open Camera captures
`4096x3072`, both before and after the change. The 50.3 MP figure is a property
of the fullres HAL, not of Open Camera, and the row is now split accordingly.

## 2. Findings

- **`FIND-3.4-01` (P2, open) — an unrecognized HAL md5 strands the HAL layer.**
  Once `active_hal/camera.qcom.so` carries a third md5, **no runtime mode switch
  can change the HAL layer in either direction**. `hal_state` returns `unknown`,
  which is the only path that calls `hal_seed`, and `hal_seed` refuses while the
  target is bind-mounted. Observed twice, in both directions (`50mp` and
  `dcgB`). The module **warns loudly** rather than failing silently, and the
  sensor layer still switches correctly because that is a content rewrite
  needing no seeding — so the failure mode is a **state mismatch**, not
  corruption: `mode` reads `50mp` while the HAL is not `fullres`.
  Confirmed mechanism: once the word was reverted to a *recognized* md5,
  `hal_set` succeeded immediately.
  **Operational rule: revert the experimental word before any mode switch.**
  Recovery is a reboot. This disappears once Phase 4 consolidates the patch into
  a table whose result md5 is a recognized constant. Routed to Phase 4 and to
  `docs/recovery-runbook.md`.
- **`FIND-3.4-02` (P2, open) — `dcgB` crashes the camera provider, independent
  of this change.** With `dcgB` mounted and the HAL at plain **stock**, no
  experimental word, on a **fresh boot**, both `com.android.camera` and Open
  Camera produce a black preview and a provider abort at
  `CSLAcquireHardwareHW+1540` -> `CamX::IFENode::AcquireResources` ->
  `Pipeline::StreamOn`. `dcgA` on the same boot is clean, so this is
  `dcgB`-specific rather than a sensor-layer-wide fault.
  `docs/regression-v2.1.md` row 4 records `dcgB` as PASS, but that row tested
  **AGC**, not these two consumers — so this is a previously untested
  combination, not a contradiction of the record. **Not attributable to Faz 3.3's
  change**, which was not present. Routed to Phase 9; deeper diagnosis is out of
  Faz 3.4's scope by its own section 5.
- **`FIND-3.4-03` (P3, method) — a provider crash contaminates the whole boot.**
  After the first abort, *every* subsequent measurement in *any* mode — including
  plain `stock` — showed a black preview and the same
  `CSLAcquireHardwareHW` signature until a reboot. Two readings in this session
  were initially misattributed before this was recognised, and one intermediate
  conclusion had to be withdrawn. **Any Phase 3 or Phase 4 measurement taken
  after a provider crash must be discarded and re-taken on a fresh boot.**
  This belongs in the `Faz 3.1` per-measurement checklist.

## 3. Consumers deliberately excluded

- **AGC / Gcam.** Faz 3.5 owns it entirely. No AGC interaction occurred in this
  sub-phase; the acceptance criterion requiring that is met.
- **Applications with no documented prior behaviour**, since a verdict would be
  unfalsifiable.

## 4. Scope statement for `OQ-03`

**Answered, for these consumers only:** raising `pixelArraySize` to `8192x6144`
did **not** break the stock camera, Open Camera, the 1080p60 or 4K60 video
paths, the `dcgA` sensor-layer mode, or the `50mp` HAL-layer mode; it did not
change captured dimensions where they were already correct, it preserved the
50.3 MP full-resolution capture, and it produced no field-of-view change in a
controlled comparison.

This is **not** a general compatibility claim. Three applications, two video
profiles and two of ten modes were tested. The one failure observed
(`dcgB`) reproduces without the change and is therefore outside this question.
AGC — the consumer the whole phase exists for — was deliberately not tested
here.
