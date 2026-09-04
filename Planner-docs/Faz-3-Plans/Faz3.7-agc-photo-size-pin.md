# Faz 3.7 — AGC Photo-Size Pin and Clean 12.58 MP Capture

## 1. Context

**This sub-plan opens the replacement Phase 3.** `Main-Planing.md` was amended on 2026-09-03 by user decision `DEC-14`: the objective "50 MP end-to-end in AGC" is **retired**, and the objective is now "AGC stable at 12.6 MP under 50 MP" — with the 50 MP HAL layer enabled, AGC launches, previews, captures and saves a clean 12.58 MP (`4096x3072`) image reproducibly, while Open Camera still captures 8192x6144 in the same HAL state. `SNAP-2026-08-24-SUBPLANS` was superseded by `SNAP-2026-09-03-MAIN`, which is why this sub-plan exists.

`Faz3.1` through `Faz3.6` remain `verified` and are **not** demoted. They are the history that produced the change: `IMPL-23` cleared the libgcam gate, `IMPL-43` produced the project's first 50 MP AGC file and located why it was unusable, and `IMPL-47` / `IMPL-49` / `IMPL-50` / `IMPL-51` measured the two walls that closed the route. Nothing in this sub-plan re-opens any of that.

The premise this sub-plan tests is small and already half-observed. `IMPL-43` established that `pref_camera_picturesize_back_key` is the **proximate** selector AGC honours — "with it at `4096x3072` AGC opened a `4096x3072` reader and matched cleanly at half resolution" — and that `pref_48m_key` is *not* the selector, only the switch that makes 50 MP appear in the list. `IMPL-40` then measured a clean AGC capture through that same stack: `3072x4096`, **12.58 MP, black fraction 0.0024**, against the fold signature of 0.7495–0.7498 that every mismatched capture carries. So a clean 12.58 MP AGC photograph is on record. What is *not* on record is that state being deliberately configured, verified by instrument rather than by eye, and reproduced.

Main-Planing's Phase 3 first vibecoding slice is exactly this sub-plan: "Read the current value of `pref_camera_picturesize_back_key` on device, set it to `4096x3072` if it is not already, take one bracketed capture, and measure the black fraction — this is a few minutes of work and it either confirms the whole phase's premise or falsifies it immediately."

## 2. Goal

Put AGC's photo size under deliberate control at `4096x3072` on a named 50 MP HAL base, and prove by measurement — not by appearance — that the resulting saved image is a clean 12.58 MP frame rather than a folded one, with the configured stream read back from the camera service while AGC is open.

## 3. Description

The problem this solves is that the project's one clean AGC capture was an accident of state. `IMPL-40` recorded it plainly: "The shot was **not `EV-44`** — AGC was in half-res mode." Nobody set that; it was where the app happened to be. A capability that exists only when the app happens to be configured correctly is not a capability, and under the broad HAL table AGC's default is to select the largest advertised size, which is the path that yields an unusable frame. That default is risk `R12`.

It belongs first in the replacement Phase 3 because it is the phase's premise and it is cheap. Every later sub-plan — the smoke detector, the coexistence bracket, the stickiness matrix — assumes a pinned size is achievable and produces a clean image. If it does not, the phase's shape changes immediately and at almost no cost.

**The vibecoding slice strategy.** The first useful slice is a read: what is `pref_camera_picturesize_back_key` set to right now, and what HAL md5 is live? That answers whether anything needs doing at all. The second slice is one pin plus one capture plus one black-fraction measurement. The fastest validation signal is `dumpsys media.camera` with AGC open, which `IMPL-43` established prints per-stream `Consumer name: ImageReader-<W>x<H>f<fmt>` and `Dims: W x H, format 0x..` — an instrument the project believed it did not have until that run.

**What must not be over-planned yet.** No preference-management scheme for AGC, no patch of any kind, and no attempt to make the pin *survive* anything. Survival is `Faz3.10`'s question and it is deliberately deferred, because a pin that cannot be set at all makes survival moot.

**One scoping question is raised here rather than assumed, and it is the reason this sub-plan has a decision routed to the user.** The device currently carries HAL `ce419bc901bea61945d166aee11e1ab0` — the broad RAW stack plus raised arrays plus the ultra-high-resolution capability gate — which is an *experimental* base built during the retired objective. The **shipped** 50 MP layer is `hal-fullres.patch`, md5 `fe0245a4720fb07b01d96deef47f5569`. The target end state is about the artifact that ships, so the reference base for this phase should be the shipped one; but the device is not on it, and the two bases advertise different tables (`IMPL-43` measured camera 2 carrying **no** RAW10 at 8192x6144 on the fullres base, against 32 RAW10 entries under the seven-word stack). This sub-plan measures the base it is actually on, **names its md5 in every result**, and routes the choice as `DEC-15` rather than silently adopting one.

## 4. Scope

- A read of AGC's current photo-size preference state: `pref_camera_picturesize_back_key`, `pref_48m_key`, and the twelve trap keys, by name and value, before anything is changed.
- A read of the live HAL md5 and mount state, so every result in this phase is attributable to a named base.
- Setting `pref_camera_picturesize_back_key` to `4096x3072` by the least invasive route that works, with the route recorded.
- Determination of whether the in-app settings screen (`pref_camera_resolution`, category `pref_category_resolution_camera`) and the preference key agree, since `IMPL-43` names the key and the AGC settings surface exposes the size as an ordinary visible `ListPreference` gated by no `dependency`.
- One bracketed capture with AGC open, with `dumpsys media.camera` read **while it is open** to record the configured stream dimensions and format.
- A black-fraction measurement of the saved original, against `IMPL-40`'s 0.0024 reference and the 0.7495–0.7498 fold signature.
- A statement of which HAL base the measurement was taken on, and the `DEC-15` routing of which base this phase adopts.
- Recording of the result in the ledger with the AGC build md5 named, per the `docs/phase3-preconditions.md` per-measurement checklist item 7.

## 5. Out of Scope

- Any HAL patch, any APK modification, any smali change. `DEC-14` makes this phase a *configuration* problem; nothing here is a code change to a binary.
- Turning `pref_48m_key` on. It is currently off, which makes the patched AGC behave identically to stock, and that is the state the objective wants preserved. Whether it may be on is `Faz3.10`'s negative-control question, not this one.
- Reverting, re-applying, or altering the live HAL. If `DEC-15` selects a different base, the change is a separate, bracketed action gated on that decision.
- Making the pin survive anything — reboot, mode switch, cold start, camera-stack restart. That is `Faz3.10`.
- Extending `scripts/smoke.sh`. That is `Faz3.8`, deliberately after this sub-plan so the instrument is built against a known-good observation rather than a hoped-for one.
- Open Camera. Coexistence is `Faz3.9`.
- Re-opening the retired 50 MP objective in any form, including "just to see".

## 6. Current Repository Evidence

`scripts/smoke.sh` exists (210 lines, Faz 2.1 / `IMPL-04`) and its `probe_app` function reports `agc.package`, `agc.installed`, `agc.versionName`, `agc.versionCode`, `agc.apk.md5`, `prefs.trap.count` and `prefs.trap.keys`. It reads `/data/data/<pkg>/shared_prefs/*.xml` already, but **greps only the two trap key families** — it does not report the photo-size preference. That gap is what makes `R12` invisible today and it is `Faz3.8`'s work, not this sub-plan's.

`docs/phase3-preconditions.md` exists and carries the eight-item per-measurement checklist (item 1 preferences clear, item 2 bracket taken, item 3 one variable, item 4 metadata republished, item 5 restorable, item 6 addresses recorded immediately, item 7 attribution stated, item 8 crash contamination cleared). Every measurement in this sub-plan runs it. Write authority for that file was `Faz4.6`'s `F4.6-09` and is discharged; this sub-plan reads it and does not edit it.

`agc-50mp-yama/` holds the experimental tables including `hal-raw50-deneme.patch`, `hal-pixelarray-deneme.patch`, `hal-activearray-deneme.patch`, `hal-uhrtags-deneme.patch`, `hal-uhrfull-deneme.patch`, `hal-binsel-deneme.patch`, and the four `f41-stage*.tbl` bisection tables. None of them is applied by this sub-plan; they are listed because the live HAL is a composition of several of them and its md5 must be attributed rather than described loosely.

`snapshots/` holds the bracketed smoke history, most recently `20260903-1730__Faz4.1__F4107-post-revert.txt`. The naming convention is `<UTC>__<subplan>__<label>`; this sub-plan follows it.

Ledger `IMPL-43` records the instrument this sub-plan depends on: "`dumpsys media.camera` on an **open** camera prints per-stream `Consumer name: ImageReader-<W>x<H>f<fmt>` (the app-side reader) and `Dims: W x H, format 0x..` (the configured stream), plus the latest result metadata **with values**." It also records the correction this sub-plan is built on: "`pref_48m_key` is necessary but **not the selector** — it only makes the size available; `pref_camera_picturesize_back_key` is the proximate selector."

Ledger `IMPL-40` records the reference measurement: `21:27` original at `3072x4096`, **12.58 MP, black fraction 0.0024**, versus `19:31` at the same geometry with **0.7498**. Both were measured with PIL, grayscale, threshold < 4, on the originals — this sub-plan uses the identical method so the numbers are comparable.

Project-Ontology invariant 8 and `IMPL-16` record the trap keys as **0/12** and record that the app does not self-arm them; both root `.agc` configuration files still carry all twelve names, so importing either re-arms the trap. That is a precondition, not a task.

## 7. Planned Work Breakdown

- F3.7-01 — Read the entry state before touching anything
  - Description: Record the live HAL md5, both mount counts, the active mode, the AGC package md5, the trap key count, and the current value of `pref_camera_picturesize_back_key` and `pref_48m_key`. Take a `scripts/smoke.sh` snapshot as the pre-bracket.
  - Output: A named pre-state snapshot plus the two preference values read by name.
- F3.7-02 — Name the reference HAL base and route `DEC-15`
  - Description: State whether the measurement base is the shipped `fullres` artifact (`fe0245a4…`) or the experimental stack the device currently carries (`ce419bc9…`), with the consequence of each recorded. Route the choice to the user as `DEC-15`; do not change the base to answer it.
  - Output: A named base with its md5, and `DEC-15` raised with a recommended default.
- F3.7-03 — Determine the pin route
  - Description: Establish how `pref_camera_picturesize_back_key` is best set — through AGC's own settings screen (`pref_camera_resolution` under `pref_category_resolution_camera`, which `IMPL-43`'s reading says is visible and ungated) or by writing the shared preference directly. Record which route was used and whether the app rewrote the value on next start.
  - Output: A recorded pin route with its observed durability within the session.
- F3.7-04 — Pin the size to `4096x3072`
  - Description: Set the preference, restart AGC, and re-read it. A value that does not survive the app's own restart is not a pin and must be reported as such rather than retried until it sticks.
  - Output: A read-back confirming `4096x3072` after an AGC restart.
- F3.7-05 — Read the configured stream with AGC open
  - Description: With AGC open and previewing, capture `dumpsys media.camera` and extract the per-stream `Consumer name: ImageReader-…` and `Dims:` lines for the rear camera, plus `android.sensor.pixelMode` and `android.sensor.rawBinningFactorUsed` from the result metadata.
  - Output: The configured stream dimensions and format, read from the service rather than inferred from the preference.
- F3.7-06 — Take one capture and measure it
  - Description: Take a single photograph, pull the **original** file, and measure pixel dimensions, megapixels, and black fraction with the `IMPL-40` method (PIL, grayscale, threshold < 4). Do not judge by viewing.
  - Output: A measured triple — dimensions, MP, black fraction — comparable to the 0.0024 reference.
- F3.7-07 — Confirm the camera enumeration and the trap state are unchanged
  - Description: Confirm 13 camera devices still enumerate and the trap key count is still 0/12 after the capture, so the result is attributable to the pin and nothing else.
  - Output: A post-bracket snapshot diffed against the pre-bracket.
- F3.7-08 — Record the result with its attribution
  - Description: Write the result into the ledger naming the HAL md5, the AGC build md5, the preference value, and the measurement method, per checklist item 7.
  - Output: A ledger entry an unrelated reader can reproduce from.

## 8. Acceptance Criteria

- `pref_camera_picturesize_back_key` reads `4096x3072` after an AGC restart, verified by read-back rather than by having been written.
- With AGC open, `dumpsys media.camera` shows the configured rear stream at `4096 x 3072`, and the app-side `ImageReader` consumer name agrees with it. A disagreement between the two is a finding, not a pass.
- The saved original measures `4096x3072` or `3072x4096` — 12.58 MP — with the orientation stated rather than assumed.
- The black fraction is comparable to `IMPL-40`'s **0.0024** reference and is nowhere near the 0.7495–0.7498 fold signature. The threshold for "comparable" is stated as a number before the capture, not chosen after seeing it.
- The measurement method is the `IMPL-40` method, named in the result, so the two numbers are actually comparable.
- Every result names the HAL md5 and the AGC package md5 it was measured under.
- The trap key count is 0/12 both before and after; camera enumeration is 13 devices both before and after.
- `DEC-15` is raised with a recommended default and is **not** resolved by this sub-plan acting unilaterally.
- The pre- and post-brackets differ only on lines explained in the result.
- `pref_48m_key` is unchanged by this sub-plan, and its value is recorded.

## 9. Validation and Test Approach

Validation is live, single-variable, and bracketed. The distinguishing property is that the headline result is a **measured number on a file**, not a visual judgment — this project has already paid once for a conclusion drawn from looking at an image.

- `VAL-SMOKE` (from Faz 2.1) — `scripts/smoke.sh -o <UTC>__Faz3.7__<label>` before and after, with the comparable regions diffed. This is the bracket the per-measurement checklist item 2 requires.
- `VAL-PREFPIN` (proposed) — three reads of `pref_camera_picturesize_back_key`: before the pin, after the pin, and after an AGC restart. Three, because a value that does not survive the app's own restart is not a pin.
- `VAL-DUMPSYS` (proposed, established by `IMPL-43`) — `dumpsys media.camera` with AGC open; extract the rear camera's per-stream `Consumer name` and `Dims` lines and the `pixelMode` / `rawBinningFactorUsed` result values.
- `VAL-ARTIFACT` (proposed, method fixed by `IMPL-40`) — PIL, grayscale, threshold < 4, on the pulled original: dimensions, megapixels, black fraction.
- `VAL-PRECOND` (from Faz 3.1) — the eight-item per-measurement checklist in `docs/phase3-preconditions.md`, run before the result is recorded.

Document validation applies to the `DEC-15` routing and the result attribution. Local versus live: only `VAL-ARTIFACT` is host-side; everything else needs the device. Security validation is not applicable; no credential is read, and preference values are read by name and value because the value *is* the finding, unlike the trap keys where the name suffices. Ledger evidence for Step 4: the two snapshot filenames, the three preference reads, the dumpsys extract, and the measured triple.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | The bracket. Read-only; this sub-plan does not extend it — `Faz3.8` does. | VAL-SMOKE |
| docs/phase3-preconditions.md | existing | The per-measurement checklist. Read, not edited; write authority was discharged by `F4.6-09`. | VAL-PRECOND |
| snapshots/ | generated | Pre- and post-brackets plus the pulled original and its measurement record. | VAL-SMOKE, VAL-ARTIFACT |
| docs/agc-12mp-configuration.md | deferred | The operator-facing configuration record. Deferred to `Faz3.11` so one sub-plan owns the file; this sub-plan produces its content, not the file. | VAL-DOCS |
| Planner-docs/Planing-Ledger.md | modified | The result with its HAL and AGC attribution. | VAL-PRECOND |

## 10. Dependencies and Sequencing

Depends on `Faz2.1` for `scripts/smoke.sh`, on `Faz3.1` for the per-measurement checklist and the cleared trap state, and on `Faz2.2` for a named baseline to attribute against. All three are `verified`.

Does **not** depend on `Faz4.1` or `Faz4.7`; both are `superseded` by `DEC-14` and must not be revived to unblock anything here.

Blocks `Faz3.8`, `Faz3.9`, `Faz3.10` and `Faz3.11`. `Faz3.8` in particular should be built after this sub-plan and not before, so the smoke field is designed around a preference layout that has actually been read rather than one that has been guessed.

Required decisions: `DEC-15`, the reference HAL base, which is the user's because it decides whether this phase certifies the shipped artifact or an experimental composition. The implementer proposes the shipped `fullres` base as the default and states the cost of that choice — reaching it from the current state is a bracketed HAL transition, not a no-op.

Required credentials or live endpoints: none. Root through KernelSU and `adb` access to device `dc27e5d0`.

Required human approvals: physical device access for the capture, and the shutter itself. `DEC-15` before any HAL base change.

Fresh-session token and context risk: **low**. This is a handful of reads, one preference write, one capture, and one host-side measurement. The high banding Main-Planing gave the old Phase 3 described a write-site search in a 27 MB stripped binary; nothing of that kind remains in this phase.

Subagents are not recommended. Device state is a single stateful resource and the whole sub-plan is one bracketed sequence.

## 11. Risks and Mitigations

- Risk (`R12`): the pin is set, the capture is clean, and the result is reported as "AGC works at 12.6 MP" without the qualification that it works *while pinned*. Impact: a future reader believes a property holds that only holds under a setting nothing enforces. Mitigation: every acceptance criterion in this sub-plan names the pinned preference as a condition, and `Faz3.10` exists specifically to test the condition's durability.
- Risk: the black fraction threshold for "clean" is chosen after seeing the number. Impact: an unfalsifiable pass. Mitigation: the criterion requires the threshold to be stated before the capture.
- Risk: the measurement is taken on the experimental HAL base and later read as a statement about the shipped module. Impact: a claim about an artifact that was never measured. Mitigation: `F3.7-02` names the base and `DEC-15` routes the choice; every result carries the md5.
- Risk (`EV-13`, invariant 8): a trap key is set at the moment of measurement and the failure is attributed to the pin. Impact: the three-step misattribution this project has already paid for once. Mitigation: checklist item 1 and the smoke script's independent `prefs.trap.count` view, checked before **and** after.
- Risk: AGC rewrites the preference on start, so the pin appears to work and silently does not. Impact: an intermittent regression that is harder to diagnose than a persistent one. Mitigation: `VAL-PREFPIN`'s third read is taken specifically after an AGC restart.
- Risk: the direct preference write and the in-app settings screen disagree, and the app's own UI later overwrites the pin. Impact: the pin route chosen here is the wrong one for the long term. Mitigation: `F3.7-03` determines the route and records the observed behaviour rather than assuming the two surfaces are the same key.
- Risk: the capture is judged by looking at it. Impact: the fold signature at 0.75 is visually obvious, but a partial or subtler corruption is not, and this project's history contains a hypothesis that looked correct and was wrong. Mitigation: `VAL-ARTIFACT` is a number produced by a fixed method.
- Risk: a camera-provider abort during the session contaminates the boot (`FIND-3.4-03`). Impact: subsequent measurements in the same boot are unattributable. Mitigation: checklist item 8 requires a reboot after any provider abort before continuing.

## 12. Desired End State

AGC's photo size is deliberately pinned to `4096x3072` on a named 50 MP HAL base, and the state is proven three ways that agree with each other: the preference reads back after an app restart, the camera service reports the configured stream at `4096 x 3072` while AGC is open, and the saved original measures 12.58 MP with a black fraction comparable to the 0.0024 reference.

The evidence an implementer should produce: two smoke snapshots with their filenames, three preference reads, the dumpsys stream extract, the pulled original and its measured triple, and the pre/post trap and enumeration counts.

The ledger summary Step 4 should append records: the reference HAL md5 and the AGC package md5; the preference values before and after; the pin route used and whether it survived an AGC restart; the configured stream dimensions from dumpsys; the measured dimensions, megapixels and black fraction with the threshold that was stated in advance; and the `DEC-15` routing with its recommended default.

## 13. Next Sub-Phase Transition Criteria

- The pin reads back as `4096x3072` after an AGC restart.
- The camera service and the app-side reader agree on `4096 x 3072` while AGC is open.
- The saved original measures 12.58 MP with a black fraction below the pre-stated threshold and comparable to 0.0024.
- Every recorded result names its HAL md5 and its AGC package md5.
- `DEC-15` is raised, with a recommended default, and its answer is not assumed by later sub-plans until the user gives it.
- The trap count is 0/12 and enumeration is 13 devices, before and after.
- `Faz3.8` has a real, read preference layout to build its smoke field against.
