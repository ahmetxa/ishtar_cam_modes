# Faz 3.7 — AGC Photo-Size Pin and Clean 12.58 MP Capture

## 1. Context

**Closed 2026-09-05 by planning run 13 (`AUDIT-FIX-27` and `AUDIT-FIX-28` discharged).** This sub-plan is `verified`. `F3.7-09` and `F3.7-10` ran as `IMPL-53` and `F3.7-06`/`07`/`08` as `IMPL-54`; **all ten acceptance criteria are satisfied on the shipped base** and `DEC-18` closed the `pref_48m_key` bracket by adoption at `0`. The headline results: at `pref_48m_key`=`0` on `fe0245a4720fb07b01d96deef47f5569`, *Full resolution* derives `4096x3072`; RAW10 and YUV are both configured at `4096x3072` and their `ImageReader` consumer names agree; the saved original measures `3072x4096`, 12.58 MP, black fraction **0.0027** against a `< 0.01` threshold stated before the capture.

**`AUDIT-FIX-27` — the missing failure route — is discharged by outcome, and the route is recorded anyway so the gap does not reappear.** The audit was right that sections 8 and 13 simultaneously required the pin to read `4096x3072` (criteria 1—3) and permitted the prediction to fail (criterion 10), leaving the sub-plan able to both pass and not close. **The prediction passed, so the contradiction resolved in the reachable direction** — criteria 1—3 were met by measurement, not waived. Had it failed, the route was and remains: stop at the end of `F3.7-10`, record the measured derivation with its base md5, do **not** retry the write, and route the phase's shape back to the user as a new decision, exactly as `IMPL-52` did when it hit the analogous wall. That is the `Faz3.6`-shaped gate the replacement generation lacked; it is written here rather than in a new sub-plan because the measurement that would have needed it has already been taken.

**`AUDIT-FIX-28` — four internal residues, all of the same class — is discharged in place.** Section 4's settings-screen bullet, section 9's closing evidence sentence, section 11's fifth risk and section 1's third paragraph each restated a fact this file had already corrected elsewhere. Each is corrected below with its superseding measurement named, following section 12's wording as the model.

**Two findings raised by `IMPL-54` are routed out of this sub-plan and are not defects in it:** `FIND-3.7-01` (P2 — `docs/phase3-preconditions.md` section 1 is false as written and its `sed -i` clearance is unsafe) is assigned to `Faz3.11`, the only sub-plan holding write authority for that file; `FIND-3.7-02` (P3 — the smoke script counts trap-key presence, not value) is assigned to `Faz3.8`. `FIND-3.7-03` (the **front** camera's size re-derives too, `6528x4896` to `3264x2448`) is assigned to `Faz3.10`.

**Amended 2026-09-04 by planning run 12 (`DEC-15`, `DEC-17`, and the measurements of `IMPL-52`).** `IMPL-52` ran `F3.7-01` … `F3.7-04` live and **falsified this sub-plan's own premise**: `pref_camera_picturesize_back_key` is a *derived* value, re-derived by AGC from `pref_camera_resolution` on every start, so none of the three in-scope pin routes survives an app restart, and with `pref_48m_key`=**1** the two-value settings surface derives only `8192x6144` or `1920x1440` — `4096x3072` is not expressible. Two recorded premises were contradicted by measurement: section 5 below said `pref_48m_key` was **off** (it is **on**, value `1`), and `Main-Planing.md` section 6's third Phase 3 fact said leaving it on does not force a 50 MP capture (it does). The master plan's fact was corrected by the same planning run under `SNAP-2026-09-04-MAIN`. **Three changes follow here, and nothing else in this file was rewritten:** (1) `pref_48m_key` becomes a **measured variable with its own bracket** rather than a constant — section 4 widened, section 5's prohibition withdrawn, acceptance criterion 10 rewritten, and two work items added; (2) the reference base is now **decided**, not routed — per `DEC-15` the experiment runs on the **shipped** `fullres` artifact, md5 `fe0245a4720fb07b01d96deef47f5569`, reached by a bracketed HAL transition; (3) **every figure `IMPL-52` produced is scoped to the experimental base `ce419bc901bea61945d166aee11e1ab0` and does not transfer** — the derivation behaviour must be re-measured on the shipped base before anything is concluded from it, because the two bases advertise different tables and AGC derives its size list from what the base advertises. The requirement that `pref_48m_key`'s value is recorded in **every** result is unchanged, and now applies to a variable rather than to a constant.

**This sub-plan opens the replacement Phase 3.** `Main-Planing.md` was amended on 2026-09-03 by user decision `DEC-14`: the objective "50 MP end-to-end in AGC" is **retired**, and the objective is now "AGC stable at 12.6 MP under 50 MP" — with the 50 MP HAL layer enabled, AGC launches, previews, captures and saves a clean 12.58 MP (`4096x3072`) image reproducibly, while Open Camera still captures 8192x6144 in the same HAL state. `SNAP-2026-08-24-SUBPLANS` was superseded by `SNAP-2026-09-03-MAIN`, which is why this sub-plan exists.

`Faz3.1` through `Faz3.6` remain `verified` and are **not** demoted. They are the history that produced the change: `IMPL-23` cleared the libgcam gate, `IMPL-43` produced the project's first 50 MP AGC file and located why it was unusable, and `IMPL-47` / `IMPL-49` / `IMPL-50` / `IMPL-51` measured the two walls that closed the route. Nothing in this sub-plan re-opens any of that.

The premise this sub-plan tests is small and already half-observed. `IMPL-43` established that `pref_camera_picturesize_back_key` is the **proximate** selector AGC honours — "with it at `4096x3072` AGC opened a `4096x3072` reader and matched cleanly at half resolution" — and that `pref_48m_key` is *not* the selector, only the switch that makes 50 MP appear in the list. **That last clause is superseded and is retained only as the reading this sub-plan started from — see the amendment banner above and `IMPL-53`.** `pref_48m_key` is not merely an availability switch: it selects **which pair of values** the two-value settings surface derives, `8192x6144` / `1920x1440` at `1` and `4096x3072` / `1920x1440` at `0`, and it is therefore the input the pin is written on. `pref_camera_picturesize_back_key` remains the proximate selector for what AGC opens, but it is an **output** — re-derived on every AGC start (`IMPL-52`) — and so is not a pin point. `IMPL-40` then measured a clean AGC capture through that same stack: `3072x4096`, **12.58 MP, black fraction 0.0024**, against the fold signature of 0.7495–0.7498 that every mismatched capture carries. So a clean 12.58 MP AGC photograph is on record. What is *not* on record is that state being deliberately configured, verified by instrument rather than by eye, and reproduced.

Main-Planing's Phase 3 first vibecoding slice is exactly this sub-plan: "Read the current value of `pref_camera_picturesize_back_key` on device, set it to `4096x3072` if it is not already, take one bracketed capture, and measure the black fraction — this is a few minutes of work and it either confirms the whole phase's premise or falsifies it immediately."

## 2. Goal

Put AGC's photo size under deliberate control at `4096x3072` on a named 50 MP HAL base, and prove by measurement — not by appearance — that the resulting saved image is a clean 12.58 MP frame rather than a folded one, with the configured stream read back from the camera service while AGC is open.

## 3. Description

The problem this solves is that the project's one clean AGC capture was an accident of state. `IMPL-40` recorded it plainly: "The shot was **not `EV-44`** — AGC was in half-res mode." Nobody set that; it was where the app happened to be. A capability that exists only when the app happens to be configured correctly is not a capability, and under the broad HAL table AGC's default is to select the largest advertised size, which is the path that yields an unusable frame. That default is risk `R12`.

It belongs first in the replacement Phase 3 because it is the phase's premise and it is cheap. Every later sub-plan — the smoke detector, the coexistence bracket, the stickiness matrix — assumes a pinned size is achievable and produces a clean image. If it does not, the phase's shape changes immediately and at almost no cost.

**The vibecoding slice strategy.** The first useful slice is a read: what is `pref_camera_picturesize_back_key` set to right now, and what HAL md5 is live? That answers whether anything needs doing at all. The second slice is one pin plus one capture plus one black-fraction measurement. The fastest validation signal is `dumpsys media.camera` with AGC open, which `IMPL-43` established prints per-stream `Consumer name: ImageReader-<W>x<H>f<fmt>` and `Dims: W x H, format 0x..` — an instrument the project believed it did not have until that run.

**What must not be over-planned yet.** No preference-management scheme for AGC, no patch of any kind, and no attempt to make the pin *survive* anything. Survival is `Faz3.10`'s question and it is deliberately deferred, because a pin that cannot be set at all makes survival moot.

**One scoping question was raised here rather than assumed, and it is the reason this sub-plan carried a decision routed to the user. It is now answered.** The device currently carries HAL `ce419bc901bea61945d166aee11e1ab0` — the broad RAW stack plus raised arrays plus the ultra-high-resolution capability gate — which is an *experimental* base built during the retired objective. The **shipped** 50 MP layer is `hal-fullres.patch`, md5 `fe0245a4720fb07b01d96deef47f5569`. The target end state is about the artifact that ships, so the reference base for this phase should be the shipped one; but the device is not on it, and the two bases advertise different tables (`IMPL-43` measured camera 2 carrying **no** RAW10 at 8192x6144 on the fullres base, against 32 RAW10 entries under the seven-word stack). This sub-plan measures on a named base and **names its md5 in every result**. **`DEC-15` was answered by the user on 2026-09-04: the reference base is the shipped `fullres` artifact, `fe0245a4720fb07b01d96deef47f5569`**, on the reasoning that the target end state is about the module that ships, and a claim measured on an experimental composition cannot be made about it. Two consequences are carried rather than assumed away. Reaching that base from the device's current `ce419bc901bea61945d166aee11e1ab0` is a **bracketed HAL transition**, not a no-op, and it is now this sub-plan's first live action. And **`IMPL-52`'s figures — the `full` / `medium` derivation to `8192x6144` / `1920x1440` — were all taken on the experimental base and must be re-measured on the shipped one**; they may be quoted as history, never as a statement about the shipped artifact.

## 4. Scope

- A read of AGC's current photo-size preference state: `pref_camera_picturesize_back_key`, `pref_48m_key`, and the twelve trap keys, by name and value, before anything is changed.
- A read of the live HAL md5 and mount state, so every result in this phase is attributable to a named base.
- Setting `pref_camera_picturesize_back_key` to `4096x3072` by the least invasive route that works, with the route recorded.
- ~~Determination of whether the in-app settings screen (`pref_camera_resolution`, category `pref_category_resolution_camera`) and the preference key agree.~~ **Answered 2026-09-04 by `IMPL-52` and re-measured on the shipped base by `IMPL-53`: they do not merely agree, one *derives* the other.** `pref_camera_resolution` is a separate two-value key (`full` / `medium`) that AGC reads at every start and from which it computes `pref_camera_picturesize_back_key`; which pair of values that computation can produce is set by `pref_48m_key`. What remains in scope is reading the derived value back after an AGC restart at each input value, which `VAL-PREFPIN` already requires.
- One bracketed capture with AGC open, with `dumpsys media.camera` read **while it is open** to record the configured stream dimensions and format.
- A black-fraction measurement of the saved original, against `IMPL-40`'s 0.0024 reference and the 0.7495–0.7498 fold signature.
- A statement of which HAL base every measurement was taken on. **The base is decided, not routed: the shipped `fullres` artifact, md5 `fe0245a4720fb07b01d96deef47f5569` (`DEC-15`, 2026-09-04).** Reaching it from the device's current `ce419bc901bea61945d166aee11e1ab0` is in scope as a bracketed HAL transition with a verified revert path.
- **`pref_48m_key` as a measured variable with its own bracket (`DEC-17`, answered yes 2026-09-04).** Its entry value is read before anything is written; it is then set to **0** inside its own bracket, with that bracket's pre- and post-state recorded, and restored afterwards unless a later sub-plan adopts the new value deliberately. One variable moves at a time: the key is never written in the same step that moves the HAL base.
- Re-measurement, **on the shipped base**, of the derivation `IMPL-52` established on the experimental one: which `pref_camera_picturesize_back_key` value each of *Full resolution* and *Medium resolution* derives, read back after an AGC restart, at `pref_48m_key`=1 and again at `pref_48m_key`=0.
- The reading of whether `4096x3072` becomes expressible at `pref_48m_key`=0 — the one experiment that reaches the phase objective, and the reason `DEC-17` was raised.
- Recording of the result in the ledger with the AGC build md5 named, per the `docs/phase3-preconditions.md` per-measurement checklist item 7.

## 5. Out of Scope

- Any HAL patch, any APK modification, any smali change. `DEC-14` makes this phase a *configuration* problem; nothing here is a code change to a binary.
- ~~Turning `pref_48m_key` on.~~ **Withdrawn 2026-09-04 (`DEC-17`).** The original bullet rested on a premise `IMPL-52` measured false — it said the key was currently **off**, and it is **on** (value `1`). Writing the key is now in scope as a bracketed measured variable (section 4). What stays out of scope is *leaving* it at a changed value without recording the change: the bracket restores the entry value unless a later sub-plan adopts the new one deliberately. Its behaviour under the four disturbance axes remains `Faz3.10`'s negative-control question, not this one.
- ~~Reverting, re-applying, or altering the live HAL.~~ **Narrowed 2026-09-04 (`DEC-15`).** The single transition from the experimental `ce419bc901bea61945d166aee11e1ab0` to the shipped `fe0245a4720fb07b01d96deef47f5569` is now in scope: bracketed, with a verified revert path, and performed **before** any preference work so that the two variables never move together. Every other HAL change — applying an experimental table, composing a new stack, altering the patch itself — stays out of scope and belongs to Phase 4.
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

**Status 2026-09-04.** `F3.7-01` … `F3.7-04` ran as `IMPL-52` on the **experimental** base and are complete as history: `F3.7-01` and `F3.7-02` pass, `F3.7-03` and `F3.7-04` **fail** — the pin route does not exist while `pref_48m_key`=1. Their results are scoped to `ce419bc901bea61945d166aee11e1ab0` and do not transfer. Work resumes at the two new items below, which run **first**; `F3.7-03` and `F3.7-04` are then re-attempted on the shipped base under the new variable, and `F3.7-05` … `F3.7-08` follow unchanged. Item numbers are not reused or renumbered, so existing ledger references stay resolvable.

- F3.7-09 — Transition to the shipped `fullres` base and re-measure the derivation there (`DEC-15`)
  - Description: Bracket the device, transition the live HAL from `ce419bc901bea61945d166aee11e1ab0` to the shipped `fe0245a4720fb07b01d96deef47f5569` with a verified revert path, then re-read — at the **unchanged** entry value of `pref_48m_key` — what `pref_camera_resolution`'s two settings derive on this base. One variable: the base moves and no preference is written in this item.
  - Output: A pre/post bracket around the transition, the live md5 read back rather than assumed, and the derivation table for *Full resolution* / *Medium resolution* measured on the shipped base instead of carried from `IMPL-52`.
- F3.7-10 — Bracket `pref_48m_key` as a measured variable (`DEC-17`)
  - Description: With the base fixed and named, record the entry value of `pref_48m_key`, set it to **0**, restart AGC, and re-read what *Full resolution* derives. The falsifiable prediction is stated before the write: `4096x3072`. If it derives anything else, that is the finding and the phase's premise changes again rather than the write being retried until it sticks. Restore the entry value at the end of the bracket unless a later sub-plan adopts the new one deliberately.
  - Output: The key's value before, during and after, each paired with the derived `pref_camera_picturesize_back_key` read back after an AGC restart, all under one named HAL md5.
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
- `DEC-15` is **answered** (2026-09-04, user: the shipped `fullres` base), and every result names `fe0245a4720fb07b01d96deef47f5569` as the base it was measured on. Any figure carried from `IMPL-52` is labelled as measured on `ce419bc901bea61945d166aee11e1ab0` and is never quoted as a statement about the shipped base.
- The pre- and post-brackets differ only on lines explained in the result.
- **`pref_48m_key` is a measured variable with its own bracket, not a constant (`DEC-17`, 2026-09-04).** Its value is recorded in **every** result — that requirement is unchanged, and now covers a value that moves. The criterion is met when: the entry value is read before anything is written; the key is changed inside a bracket that moves nothing else, with that bracket's pre- and post-state recorded; the derived `pref_camera_picturesize_back_key` is read back after an AGC restart at **each** value of the key; the prediction (`4096x3072` at `pref_48m_key`=0) is stated before the write and reported as pass or fail rather than retried; and the entry value is restored at the end of the bracket unless a later sub-plan adopts the new one deliberately. A result that does not name the key's value at the moment of measurement is not a result.

## 9. Validation and Test Approach

Validation is live, single-variable, and bracketed. The distinguishing property is that the headline result is a **measured number on a file**, not a visual judgment — this project has already paid once for a conclusion drawn from looking at an image.

- `VAL-SMOKE` (from Faz 2.1) — `scripts/smoke.sh -o <UTC>__Faz3.7__<label>` before and after, with the comparable regions diffed. This is the bracket the per-measurement checklist item 2 requires.
- `VAL-PREFPIN` (established by `IMPL-52`, which ran **five** reads rather than the three originally proposed) — reads of `pref_camera_picturesize_back_key` at every state change: before, after each write, and after each AGC restart. The count is not fixed at three; the rule is that no state transition goes unread, because the value is re-derived on every start and a value that does not survive the app's own restart is not a pin.
- `VAL-BASE` (proposed, `DEC-15`) — the HAL transition bracket: live md5 before, the transition, live md5 **read back** after rather than assumed, mount state, camera enumeration at both ends, and the revert path exercised at least once.
- `VAL-48MBRACKET` (proposed, `DEC-17`) — the `pref_48m_key` bracket: entry value, the write, an AGC restart, the derived size read back, and the restore — with a smoke pre/post pair around it. Exactly one variable moves inside this bracket, and the HAL base is not it.
- `VAL-DUMPSYS` (proposed, established by `IMPL-43`) — `dumpsys media.camera` with AGC open; extract the rear camera's per-stream `Consumer name` and `Dims` lines and the `pixelMode` / `rawBinningFactorUsed` result values.
- `VAL-ARTIFACT` (proposed, method fixed by `IMPL-40`) — PIL, grayscale, threshold < 4, on the pulled original: dimensions, megapixels, black fraction.
- `VAL-PRECOND` (from Faz 3.1) — the eight-item per-measurement checklist in `docs/phase3-preconditions.md`, run before the result is recorded.

Document validation applies to the result attribution — every figure named against the base it was measured on — and to the `DEC-15` answer being recorded rather than re-argued. `VAL-BASE` and `VAL-48MBRACKET` are the two brackets the amendment adds, and they run in that order: the base moves first and alone, then the preference. Local versus live: only `VAL-ARTIFACT` is host-side; everything else needs the device. Security validation is not applicable; no credential is read, and preference values are read by name and value because the value *is* the finding, unlike the trap keys where the name suffices. Ledger evidence for Step 4: the snapshot filenames of **both** bracket pairs — the one around the HAL transition and the one around the `pref_48m_key` write — a preference read at **every state change** rather than a fixed count (this is `VAL-PREFPIN`'s rule, stated nine lines above, and it governs; `IMPL-52` ran five reads and `IMPL-53` six), the dumpsys extract, and the measured triple.

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

Required decisions: **none outstanding.** `DEC-15` and `DEC-17` were both answered by the user on 2026-09-04 and are recorded in the ledger. `DEC-15`: the reference base is the shipped `fullres` artifact, `fe0245a4720fb07b01d96deef47f5569`; the cost the implementer flagged stands — reaching it from the current state is a bracketed HAL transition, not a no-op, and it is `F3.7-09`. `DEC-17`: `pref_48m_key` may be written, as a measured variable with its own bracket, and it is `F3.7-10`. **The two run as one bracketed sequence, base first and then the key** — never as two independent errands, since a result measured across a moving base *and* a moving preference attributes to neither.

Required credentials or live endpoints: none. Root through KernelSU and `adb` access to device `dc27e5d0`.

Required human approvals: physical device access for the capture, and the shutter itself. `DEC-15` is given, so the base transition is approved work rather than a gated one; `DEC-17` is given, so writing `pref_48m_key` inside its bracket is likewise approved.

Fresh-session token and context risk: **low**. This is a handful of reads, one preference write, one capture, and one host-side measurement. The high banding Main-Planing gave the old Phase 3 described a write-site search in a 27 MB stripped binary; nothing of that kind remains in this phase.

Subagents are not recommended. Device state is a single stateful resource and the whole sub-plan is one bracketed sequence.

## 11. Risks and Mitigations

- Risk (`R12`): the pin is set, the capture is clean, and the result is reported as "AGC works at 12.6 MP" without the qualification that it works *while pinned*. Impact: a future reader believes a property holds that only holds under a setting nothing enforces. Mitigation: every acceptance criterion in this sub-plan names the pinned preference as a condition, and `Faz3.10` exists specifically to test the condition's durability.
- Risk: the black fraction threshold for "clean" is chosen after seeing the number. Impact: an unfalsifiable pass. Mitigation: the criterion requires the threshold to be stated before the capture.
- Risk: the measurement is taken on the experimental HAL base and later read as a statement about the shipped module. Impact: a claim about an artifact that was never measured. Mitigation: `DEC-15` decided the base — the shipped `fullres` artifact — and `F3.7-09` transitions to it before anything is measured; every result carries the md5, and `IMPL-52`'s experimental-base figures are labelled as such wherever they appear.
- Risk (`EV-13`, invariant 8): a trap key is set at the moment of measurement and the failure is attributed to the pin. Impact: the three-step misattribution this project has already paid for once. Mitigation: checklist item 1 and the smoke script's independent `prefs.trap.count` view, checked before **and** after.
- Risk: AGC rewrites the preference on start, so the pin appears to work and silently does not. Impact: an intermittent regression that is harder to diagnose than a persistent one. Mitigation: `VAL-PREFPIN` requires a read after **every** AGC restart, not a particular numbered read — the count is not fixed, and the restart-read is the one that distinguishes a pin from a write that AGC will discard. `IMPL-52` measured exactly that failure on the derived key, which is why the pin is written on the input key instead.
- Risk: the direct preference write and the in-app settings screen disagree, and the app's own UI later overwrites the pin. Impact: the pin route chosen here is the wrong one for the long term. Mitigation: `F3.7-03` determines the route and records the observed behaviour rather than assuming the two surfaces are the same key.
- Risk: the capture is judged by looking at it. Impact: the fold signature at 0.75 is visually obvious, but a partial or subtler corruption is not, and this project's history contains a hypothesis that looked correct and was wrong. Mitigation: `VAL-ARTIFACT` is a number produced by a fixed method.
- Risk: a camera-provider abort during the session contaminates the boot (`FIND-3.4-03`). Impact: subsequent measurements in the same boot are unattributable. Mitigation: checklist item 8 requires a reboot after any provider abort before continuing.

## 12. Desired End State

AGC's photo size is deliberately pinned to `4096x3072` on a named 50 MP HAL base, and the state is proven three ways that agree with each other: the preference reads back after an app restart, the camera service reports the configured stream at `4096 x 3072` while AGC is open, and the saved original measures 12.58 MP with a black fraction comparable to the 0.0024 reference.

The evidence an implementer should produce: the smoke snapshots with their filenames, including the pair bracketing the HAL transition and the pair bracketing the `pref_48m_key` write; the live HAL md5 read back at both ends of the transition; a preference read at every state change rather than a fixed count of three, each paired with the value of `pref_48m_key` at that moment; the dumpsys stream extract; the pulled original and its measured triple; and the pre/post trap and enumeration counts.

The ledger summary Step 4 should append records: the reference HAL md5 and the AGC package md5; the preference values before and after; the pin route used and whether it survived an AGC restart; the configured stream dimensions from dumpsys; the measured dimensions, megapixels and black fraction with the threshold that was stated in advance; the HAL transition with the md5 read back at both ends and the revert path exercised; and `pref_48m_key`'s value at entry, during the bracket and at restore, each paired with what *Full resolution* derived at that value, with the `4096x3072` prediction reported as pass or fail against the statement made before the write.

## 13. Next Sub-Phase Transition Criteria

- The pin reads back as `4096x3072` after an AGC restart.
- The camera service and the app-side reader agree on `4096 x 3072` while AGC is open.
- The saved original measures 12.58 MP with a black fraction below the pre-stated threshold and comparable to 0.0024.
- Every recorded result names its HAL md5 and its AGC package md5.
- The shipped base `fe0245a4720fb07b01d96deef47f5569` is live and read back, and the derivation of *Full resolution* / *Medium resolution* is measured **on it** rather than carried from `IMPL-52`'s experimental-base figures.
- `pref_48m_key`'s value is recorded in every result, its bracket is closed, and what *Full resolution* derives at `pref_48m_key`=0 is a measured fact — whether or not it is the predicted `4096x3072`.
- The trap count is 0/12 and enumeration is 13 devices, before and after.
- `Faz3.8` has a real, read preference layout to build its smoke field against.
