# Faz 3.10 — Pin Stickiness Across Reboot, Mode Switch, Cold Start and Camera Restart

## 1. Context

**Amended 2026-09-05 by planning run 13 (`AUDIT-FIX-26`, discharged against `IMPL-53` and `IMPL-54`; `AUDIT-FIX-29`'s `DEC-15` residue cleared here).** `F3.7-10` has reported. This sub-plan's four axes and its verdict discipline are unchanged; **what changed is the object being attacked and how the negative control produces the unpinned state**, and nothing else in this file was rewritten.

**The definition.** Throughout this sub-plan "the pin" now means the **configured derivation** — `pref_48m_key`=`0` together with `pref_camera_resolution`=`full`, which on the shipped `fullres` base `fe0245a4720fb07b01d96deef47f5569` derives `pref_camera_picturesize_back_key`=`4096x3072` — and **not** a direct write to the derived key. `IMPL-52` measured that a direct write to the derived key does not survive an AGC restart; `IMPL-53` measured the derivation and `IMPL-54` measured a clean 12.58 MP capture through it. `DEC-18` (2026-09-04) adopted `0` as the phase's configured state.

**Three consequences for the matrix.** (1) **Every axis reads all three keys, and the verdict is taken on the inputs.** The derived key is a cache of the last AGC start, so an axis could leave it transiently stale while the configuration is intact, or leave it correct while an input has already moved — both would be misread by a one-key verdict. A row whose inputs survived but whose derived key differs is a *self-healing* result and must be recorded as such, not as a failure. (2) **The negative control changes stimulus:** clearing the derived key is no longer a way to unpin anything, because AGC re-derives it correctly on the next start. `F3.10-07` now produces the unpinned state the way the device actually reaches it — through the input key — and `F3.10-08` restores through the same key. (3) **`FIND-3.7-03` adds a fifth value to watch:** `pref_camera_picturesize_front_key` re-derives too (`6528x4896` to `3264x2448` across the base transition, `IMPL-54`), so an axis that disturbs the front camera's derivation would be invisible to a rear-only matrix. Recording it costs one more field read per axis.

**`DEC-15` is answered** (2026-09-04, the shipped `fullres` artifact) and `IMPL-53` put the device on that base with the revert path exercised, so sections 10's dependency and its conditional are discharged.

**Amended 2026-09-05 by planning run 15 (`AUDIT-FIX-31` main body, `AUDIT-FIX-32`, `AUDIT-FIX-36`).** The seventh Step 3 audit measured that run 13's changes above reached sections 1, 6 and 7 and stopped there. Sections 4, 8 and 13 still scoped the negative control as "the pin cleared deliberately" — the stimulus `F3.10-07` declares invalid — still required the control to record one preference value where `F3.10-07` requires three, carried **no** criterion at all for the prediction `F3.10-07` requires to be stated in advance, and repeated an absolute trap-count rule that section 6's own `FIND-3.7-02` paragraph contradicts nine lines earlier. The front-key obligation existed only in the banner above. **No design changes here.** Every obligation was already decided by run 13; this run carries each one into the sections a Step 4 session is graded against, on this project's own convention that section 8 is what a run is graded on and that a work item with no criterion is an obligation a run can satisfy by skipping.

**The `FIND-3.7-03` branch is decided by carrying run 13's stated choice, not by re-opening it.** The front key is **included** — read per axis and on both halves of the control — because the banner above already reasoned it at one field read per axis, and excluding it now would be a new decision this amendment has no mandate to take. It is a *recorded value, not a fifth verdict axis*: no disturbance is added for it and a movement in it is routed as a finding rather than failing the row. Two extensions beyond the audit's enumerated sections are the same defect rather than new scope, and are recorded rather than folded in silently: `VAL-PREFPIN` in section 9, and the two absolutes in section 12.

`Main-Planing.md`'s amended Phase 3 names this sub-plan's question as the phase's real one: "The open question this phase must actually answer is **stickiness**, not feasibility: whether the pinned size survives a reboot, a QuickSettings mode switch, an AGC cold start, and a camera-stack restart — and what AGC does if it is left unpinned, since its default behaviour is to select the largest advertised size, which is the 50 MP path that produces an unusable frame."

The acceptance signals it lists include "the state is re-verified after one reboot and one tile switch", and the phase's desired end state requires "the survival behaviour across reboot and mode switch measured rather than assumed".

`R12` states the consequence of not knowing: "AGC re-selecting 50 MP after an update, a preference import, or a cold start, and the user discovering it through a bad photograph rather than a check." Persistence across reboot is also a standing property of this project's other state — Main-Planing's target end state requires the tile selection to persist across reboot, and `IMPL-13` verified that both layers do. The photo-size pin is a *different* kind of state, owned by an application rather than by the module, and nothing in the project's history establishes how it behaves.

`Faz3.7` established the pin. `Faz3.8` made it visible in a snapshot. `Faz3.9` established the coexistence state. This sub-plan attacks that state along four named axes and measures what survives.

## 2. Goal

Produce a measured survival matrix for the pinned photo size across four independent disturbances — a device reboot, a QuickSettings mode switch, an AGC cold start, and a camera-stack restart — together with a deliberate negative control establishing what AGC selects when left unpinned, so that `R12`'s exposure is a table of measured verdicts rather than an assumption.

## 3. Description

The problem is that a configuration whose durability is unknown is indistinguishable from one that works by accident. Every disturbance in the matrix is something that happens in ordinary use of this device: it reboots, the user switches tiles, the app is killed and relaunched, and the camera stack restarts every time a mode changes.

It belongs fourth because it needs a state to attack and an instrument to observe it with, and both now exist. It is also the sub-plan whose result actually decides the phase's shape: if the pin survives all four axes, the phase closes with a configuration record; if it does not, the phase closes with a documented failure mode plus whatever mitigation the surviving axes allow. Both are acceptable outcomes and neither is a fallback — that distinction matters, because the retired objective's `Faz3.6` was a fallback gate and this is not.

**The vibecoding slice strategy.** The axes are ordered by cost, cheapest first: AGC cold start (seconds), camera-stack restart (a mode re-selection), QuickSettings mode switch (two transitions), reboot (minutes and a re-verification of the whole layer state). Each axis is one disturbance, one snapshot, one verdict; a failed axis is recorded and the matrix continues, because knowing which three of four survive is far more useful than stopping at the first failure. The fastest validation signal is the `Faz3.8` field in the post-disturbance snapshot — no capture is needed to read a verdict for most axes.

**Captures are deliberately rationed.** A snapshot answers "did the pin survive"; only a capture answers "is the result still clean". Taking a capture on every axis would be eight or more shutter presses of the user's time for a question the pin field mostly answers. The rule adopted here: a snapshot per axis, and a capture only on the axes where the pin changed, plus one confirming capture at the end of the matrix. That keeps the user's involvement proportionate while keeping the strong claim — a clean image — anchored at the end.

**The negative control is part of the measurement, not an afterthought.** `R12` asserts AGC's default is the largest advertised size. That assertion is inference from `IMPL-43`'s observation that AGC "auto-selected `RAW10 8192x6144` with no preferences set at all". Clearing the pin deliberately and recording what AGC then selects converts the assertion into a measurement, and it produces the exact signature — the field value, the configured stream, and the fold fraction — that a future reader needs to recognise the regression instantly. It is run last, and the pin is restored and re-verified afterwards.

**What must not be over-planned.** No mechanism to *enforce* the pin. If an axis breaks it, the answer for this phase is to document the failure mode and report it in the smoke script, which `Faz3.8` already does. Building enforcement — a module that rewrites the preference, a boot hook — would put a root-privileged writer into an application's private data for a problem whose frequency is not yet known, and this project's guard model is deliberately conservative about writes.

## 4. Scope

- A survival verdict for the pinned photo size after an **AGC cold start** (force-stop then relaunch).
- A survival verdict after a **camera-stack restart** performed through the module's own sequence, which invariant 3 fixes as client before HAL.
- A survival verdict after a **QuickSettings mode switch** away from the 50 MP state and back, noting that invariant 4 forces the sensor layer during that transition.
- A survival verdict after a **device reboot**, with the layer state re-verified in the same snapshot.
- **All three preference keys read on every axis** — `pref_48m_key`, `pref_camera_resolution`, and the derived `pref_camera_picturesize_back_key` — **with the verdict taken on the two inputs.** A row whose inputs survived while the derived key differs is recorded as *self-healing* rather than as a failure, because the derived key is a cache of the last AGC start and is re-derived correctly on the next one (`IMPL-52`).
- **`pref_camera_picturesize_front_key` read on every axis and on both halves of the negative control** (`FIND-3.7-03`, `IMPL-54`: it re-derives too, `6528x4896` to `3264x2448` across the base transition), so an axis that disturbs the front camera's derivation is visible rather than invisible to a rear-only matrix. It is a **recorded value, not a fifth verdict axis**: no disturbance is added for it, no capture is taken through the front camera, and a movement in it is routed as a finding rather than failing the row it appears in.
- A negative control whose stimulus is **`pref_48m_key` set to `1`**, not the pin cleared: `F3.10-07` declares clearing the derived key invalid, because AGC re-derives it on the next start. AGC's own selection is recorded from all three preference keys plus the front key, from **both** configured streams with AGC open, and from one capture measured against a prediction stated in writing beforehand; then the pin is restored through the same input key and re-verified.
- One confirming capture at the end of the matrix, measured by the `IMPL-40` method, establishing that a surviving pin still yields a clean 12.58 MP image.
- A written matrix with one row per axis: disturbance, the three key values before, the three key values after, the front key before and after, verdict, and the snapshot filenames.
- Identification of any additional re-arming route observed during the matrix — an app update, a preference import, a settings-screen visit — recorded for `Faz3.11`'s operator instructions.

## 5. Out of Scope

- Building any enforcement mechanism for the pin: no boot hook, no module-side preference write, no watchdog. If an axis fails, this phase documents and reports rather than enforces.
- Importing either root `.agc` configuration file to test that route. Both carry all twelve trap keys, and importing one would re-arm the trap that independently breaks Gcam initialisation — the cost of that experiment exceeds its value, and the route is documented in `Faz3.11` as a warning instead.
- Installing or updating the AGC package to test the update route. That would change the APK md5 the whole phase is attributed against.
- Any HAL change on any axis. The HAL md5 is held constant across the entire matrix and is checked in every snapshot.
- Re-running the ten-mode regression. `Faz2.3` did that and is `verified`; the mode-switch axis here uses two transitions, not ten.
- Diagnosing why an axis fails, beyond classifying the symptom. A failed axis produces a recorded verdict and a routed finding, not an investigation.
- Any attempt to capture above 12.58 MP in AGC.

## 6. Current Repository Evidence

`IMPL-13` / `Faz2.3` measured persistence for the module's own state: both layers persist across reboot, tiles are exclusive after a cold boot, and mount counts never left 1 across roughly 17 mode transitions and 2 reboots. That is the reference for what "persists" looks like on this device — and it is about module state, not application state, which is exactly why the photo-size pin needs its own measurement.

Project-Ontology invariant 3 records the restart ordering as an invariant: client before HAL, because reversing it leaks CSIPHY/CSID allocations and blackens preview in every mode. The camera-restart axis uses the module's own sequence in `setmode.sh` rather than an ad-hoc `killall`, so the invariant is respected rather than tested. `FIND-2.3-04` records that `CSIPHYHw:4 AvailableResource=0` reads 0 on a clean boot too and is **not** diagnostic, so it must not be read as a leak signature during this matrix.

Project-Ontology invariant 4 records that selecting `50mp` forces the sensor layer to stock, enforced at `post-fs-data.sh:16-18` and `setmode.sh:177-192`, verified bracketed in both directions by `IMPL-13`. The mode-switch axis therefore changes two things at once by design — the HAL layer and the sensor layer — and the verdict must be stated as "survives a mode switch", not "survives a HAL change".

`IMPL-43` records the behaviour the negative control tests: under the seven-word stack "AGC auto-select[ed] `RAW10 8192x6144` with no preferences set at all", and with `pref_camera_picturesize_back_key` at `4096x3072` it "opened a `4096x3072` reader and matched cleanly at half resolution". The first half is the default this control measures; the second is the state it restores. **`IMPL-53` narrowed both halves on the shipped base and the control must be designed against the narrowed version.** The unpinned state is not reached by clearing the derived key — AGC re-derives that on every start — but by `pref_48m_key`=`1`, at which *Full resolution* derives `8192x6144`. And the resulting stream pair on the **shipped** base is **mismatched rather than uniformly large**: RAW10 stays at `4096x3072` while YUV goes to `8192x6144`, because the shipped base advertises no RAW10 row at `8192x6144`. That mismatch is the strongest available explanation of the fold signature, and confirming it with a capture is the one genuinely unmeasured thing left in this control.

`IMPL-43` also records the fold signature to expect from the negative control: `6144x8192` = 50.33 MP with black fraction **0.7497** and quadrant fractions 1.0000 / 1.0000 / 0.4994 / 0.4994 — content occupying exactly one quadrant. `IMPL-40` records the clean reference at **0.0024**. Those two numbers are what the control's capture is compared against.

`IMPL-16` records that AGC does **not** self-arm the trap keys across a plain launch and relaunch from an empty preference state. That result stands and is directly relevant, because the cold-start axis is exactly that disturbance. **It is narrowed rather than contradicted by `FIND-3.7-01`, and the narrowed version is what governs this matrix:** a plain launch arms nothing, but *opening AGC's settings screen* writes two trap keys, measured at value `0` and therefore inert. Re-arming is consequently known behaviour with a measured trigger and a measured inertness, not an automatically new finding. What would be new, and is worth routing: re-arming observed on an axis that never opened the settings screen, or any trap key appearing at a value other than `0`.

`scripts/smoke.sh` after `Faz3.8` reports the derived photo size, its two inputs (`pref_48m_key` and `pref_camera_resolution`), the derived megapixels, the HAL md5, both mount counts, the mode, all camera rows, and the trap count — which is every value each axis needs to be judged on, from one file. **`FIND-3.7-02` is a live caveat on the last of those:** `prefs.trap.count` counts key *presence*, not value, and `FIND-3.7-01` measured that AGC writes two trap keys at value `0` when its settings screen opens. Any axis in this matrix that involves opening AGC's settings will therefore move that line without anything harmful having changed, and the verdict rule written in `F3.10-01` must say so in advance rather than discovering it mid-matrix.

## 7. Planned Work Breakdown

- F3.10-01 — Fix the matrix and its verdict rule before running it
  - Description: Write the four axes plus the negative control, the disturbance procedure for each, and the rule that decides pass or fail, before the first disturbance. A verdict rule agreed after seeing a result is not a rule. **Three things the rule must pre-declare, because each is a reading that would otherwise be argued about at the moment it appears:** (a) the verdict is taken on the two **input** keys, and an inputs-survived/derived-stale row is a *self-healing pass*, not a failure; (b) `pref_camera_picturesize_front_key` is recorded per axis but is not a verdict, so a movement in it is routed as a finding against `FIND-3.7-03` rather than failing the row; (c) `FIND-3.7-02`'s exception — `prefs.trap.count` counts key **presence**, not value, and `FIND-3.7-01` measured AGC writing two trap keys at value `0` whenever its settings screen opens, so any axis involving that screen is expected to move the count with nothing harmful having changed, and the rule states in advance what is read instead (the two keys' **values**, which must be `0`).
  - Output: A written matrix skeleton with an explicit verdict rule carrying all three pre-declarations above.
- F3.10-02 — Axis 1: AGC cold start
  - Description: Force-stop AGC, relaunch it, snapshot, and read **all three** preference keys plus `pref_camera_picturesize_front_key`. Cheapest axis and the one `R12` names explicitly.
  - Output: A verdict row with all three key values and the front key before and after, and the snapshot names.
- F3.10-03 — Axis 2: camera-stack restart
  - Description: Trigger the module's own camera-restart sequence, respecting the client-before-HAL ordering invariant 3 fixes, then snapshot and read **all three** preference keys plus `pref_camera_picturesize_front_key`.
  - Output: A verdict row carrying all three keys and the front key, plus confirmation that mount counts stayed at 1/1.
- F3.10-04 — Axis 3: QuickSettings mode switch
  - Description: Switch away from the 50 MP state and back through the tile, snapshot after each transition, and read **all three** preference keys plus `pref_camera_picturesize_front_key` at each. Record that the sensor layer was forced by invariant 4 rather than chosen.
  - Output: Two snapshots and a verdict row naming both transitions, with all three keys and the front key recorded at each.
- F3.10-05 — Axis 4: device reboot
  - Description: Reboot, wait for the camera stack, snapshot, and read **all three** preference keys plus `pref_camera_picturesize_front_key` together with the full layer state, so layer persistence and pin persistence are judged from one file.
  - Output: A verdict row carrying all three keys and the front key, plus a layer-persistence confirmation.
- F3.10-06 — Confirming capture on the surviving state
  - Description: With the matrix complete and the pin at whatever value survived, take one capture and measure it by the `IMPL-40` method, so the matrix ends in an image result rather than a preference value.
  - Output: A measured triple against the stated threshold.
- F3.10-07 — Negative control: unpin through the input key and record AGC's own selection
  - Description: Set `pref_48m_key` to `1` — the value the device carried for most of this project's history, and the one that makes the 50 MP entry expressible — cold-start AGC, snapshot, read **all three** preference keys plus `pref_camera_picturesize_front_key`, read the configured streams with AGC open, and take one capture. Clearing the derived key is **not** a valid stimulus: `IMPL-52` measured that AGC re-derives it on the next start, so a control built on it would measure nothing. Measure the capture against both the 0.0024 clean reference and the 0.7497 fold signature. **State before the capture which one is predicted and why**, so the result is falsifiable: `IMPL-53` measured the stream pair at this value as mismatched (RAW10 `4096x3072` beside YUV `8192x6144`), which predicts the fold, but no capture has been taken at that state on the shipped base and the prediction is therefore untested.
  - Output: The measured unpinned signature — all three preference values, the front key, both configured streams with their formats, and the black fraction, reported against the prediction stated in advance.
- F3.10-08 — Restore the pin and re-verify
  - Description: Restore `pref_48m_key` to `0` — the value `DEC-18` adopted — using an inode-preserving write (`IMPL-52`/`IMPL-53`: `sed -i` replaces the file and leaves it root-owned and mislabelled; `grep`/`sed` to a temp file then `cat` back into the original preserves owner `u0_a450`, mode `0660` and the SELinux label). Cold-start AGC, snapshot, and confirm all three fields plus `pref_camera_picturesize_front_key`, the configured streams and a clean capture. The control must not be the state the device is left in.
  - Output: A restored-state confirmation with a closing bracket, the derived key and the front key read back after the restart rather than immediately after the write.
- F3.10-09 — Write the matrix and route what failed
  - Description: Complete the table with one row per axis, and route any failed axis as a named finding with its symptom classified — not diagnosed.
  - Output: A complete survival matrix and zero or more routed findings.

## 8. Acceptance Criteria

- The matrix contains one row per axis — cold start, camera-stack restart, mode switch, reboot — each with **all three** preference key values before and after (`pref_48m_key`, `pref_camera_resolution`, and the derived `pref_camera_picturesize_back_key`), `pref_camera_picturesize_front_key` before and after, a verdict, and the snapshot filenames.
- Every axis verdict is taken on the two **input** keys. A row whose inputs survived while the derived key differs is recorded as **self-healing**, not as a failure; a row failed on the derived key alone does not satisfy this criterion.
- `pref_camera_picturesize_front_key` is present in every axis row and on both halves of the negative control. If any axis moved it, that is routed as a finding against `FIND-3.7-03` with the axis named; if none did, the matrix says so explicitly — which is what `Faz3.11`'s `F3.11-08` needs in order to dispose of `FIND-3.7-03` against evidence rather than against a plan's intention.
- The verdict rule was written before the first disturbance and was not amended after a result was seen, and it pre-declares all three of `F3.10-01`'s items: the self-healing classification, the front key's non-verdict status, and the `FIND-3.7-02` trap-count exception.
- The HAL md5 is identical in every snapshot in the matrix; an axis that changed it is invalid and is re-run.
- The negative control's stimulus is `pref_48m_key`=`1`. A control performed by clearing the derived `pref_camera_picturesize_back_key` does **not** satisfy this criterion: `IMPL-52` measured that AGC re-derives that key on the next start, so such a control measures nothing.
- The negative control records AGC's own selection as **all three** preference key values plus the front key, **both** configured streams from `dumpsys` with AGC open with their formats, and the black fraction of a capture — with the last compared against both the 0.0024 and 0.7497 references.
- The fold-versus-clean prediction `F3.10-07` requires exists **in writing, with its reasoning, before the control's capture was taken**, and the measured black fraction is reported against it — including, and especially, when the prediction failed. A control whose prediction is absent, or written after the capture, does not satisfy this criterion whatever the capture showed: the control is graded on its falsifiability, not on its result.
- The pin is restored after the control through `pref_48m_key`=`0` by an inode-preserving write, and the restored state is confirmed by a read of all three fields plus the front key **after an AGC restart**, a configured-stream read, and one clean capture.
- The confirming capture on the surviving state measures 12.58 MP and passes the threshold stated in `Faz3.7`.
- Mount counts read 1/1 in every snapshot; camera enumeration reads 13 in every snapshot. **The trap count reads 0/12 in every snapshot except on an axis that opened AGC's settings screen**, where `FIND-3.7-02` and `FIND-3.7-01` make a movement expected rather than harmful: there the criterion is that the two keys AGC wrote read value `0`, and that `F3.10-01`'s verdict rule pre-declared the exception rather than it being granted after the reading appeared.
- After the reboot axis, the module's own layer state is confirmed persistent in the same snapshot, so the two kinds of persistence are judged together.
- Any axis that fails is recorded with its symptom classified and routed as a finding; the matrix continues past it rather than stopping.
- No enforcement mechanism was built, and no `.agc` file was imported.

## 9. Validation and Test Approach

Validation is live and repetitive by design. The distinguishing property is that most verdicts come from a **text field in a snapshot**, not from a photograph — which is the entire point of building the instrument in `Faz3.8` before this sub-plan runs.

- `VAL-SMOKE` (from Faz 2.1, extended by Faz 3.8) — one snapshot per disturbance, comparable regions diffed against the previous snapshot in the sequence.
- `VAL-PREFPIN` (from Faz 3.7) — all three preference keys plus `pref_camera_picturesize_front_key` read before and after each disturbance, independently of the smoke field, so the two views can be shown to agree. **`Faz3.8`'s delivered field set is not guaranteed to carry the front key** — that sub-plan's section 10 leaves the rear-only question to its implementer — so this validation reads it directly from `/data/data/org.codeaurora.snapcam/shared_prefs/org.codeaurora.snapcam_preferences.xml` unless the snapshot as built already reports it.
- `VAL-DUMPSYS` (from Faz 3.7) — the configured stream, read with AGC open, on the negative control and on the restored state.
- `VAL-ARTIFACT` (from Faz 3.7, method fixed by `IMPL-40`) — the confirming capture, the control capture, and the restore capture.
- `VAL-PERSIST` (proposed) — the reboot axis specifically: layer state, mount counts, mode, and pin all read from the post-reboot snapshot, confirming module persistence and pin persistence together.
- `VAL-PRECOND` (from Faz 3.1) — the eight-item checklist, applied per axis, since each axis is its own single-variable measurement.

Local versus live: everything except the artifact measurement is live. This sub-plan establishes live readiness for the objective; it does not establish distribution readiness. Security validation is not applicable — the negative control clears an application preference and restores it, touching no credential and no system file. Ontology validation: invariant 3 is respected by using the module's restart sequence, invariant 4's forcing is observed on the mode-switch axis, and the reboot axis re-confirms `IMPL-13`'s persistence result.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | The per-axis snapshot, including the `Faz3.8` pin fields. | VAL-SMOKE, VAL-PERSIST |
| snapshots/ | generated | One snapshot per axis, plus the control and restore brackets and three measured originals. | VAL-SMOKE, VAL-ARTIFACT |
| ishtar-cam-modes/setmode.sh | existing | The mode-switch and camera-restart disturbances use the module's own sequence; read as context, not modified. | VAL-PERSIST |
| docs/phase3-preconditions.md | existing | The per-measurement checklist, applied per axis. Read, not edited. | VAL-PRECOND |
| Planner-docs/Planing-Ledger.md | modified | The survival matrix, the control signature, and any routed findings. | VAL-PRECOND |

## 10. Dependencies and Sequencing

Depends on `Faz3.9` for an established coexistence state to attack, on `Faz3.8` for a snapshot that contains the pin, and on `Faz3.7` for the pin, the measurement method and the pass threshold. **The `DEC-15` dependency is discharged:** it was answered on 2026-09-04 (the shipped `fullres` artifact `fe0245a4720fb07b01d96deef47f5569`) and `IMPL-53` put the device on that base with the live md5 read back at both ends. The reason it mattered still governs — the matrix must run on the base the phase adopts — so every axis snapshot carries the md5 rather than assuming it.

Depends on `Faz2.3`'s persistence result as the reference for module-state persistence, so the reboot axis compares against something rather than judging in isolation.

Blocks `Faz3.11`, which records the matrix as operator-facing documentation and closes the phase.

Required decisions: **none outstanding.** `DEC-15` and `DEC-18` were both answered on 2026-09-04. If an axis fails and the user wants enforcement rather than documentation, that is a new decision and a new sub-plan — this one does not take it.

Required credentials or live endpoints: none. Root through KernelSU and `adb`.

Required human approvals: physical device access across a reboot and several transitions, and two to three shutter presses. This is the most user-time-expensive sub-plan in the phase and the capture rationing in section 3 exists to keep that proportionate.

Fresh-session token and context risk: **medium**. Not from analysis depth but from run count — nine or more snapshots and several transitions in one session. Record each axis's verdict into the matrix as it completes rather than at the end, per `R10` and `QAS-03`, which record that findings deferred to the end of a session are the ones lost.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the verdict rule is adjusted after a surprising result. Impact: an unfalsifiable matrix. Mitigation: `F3.10-01` fixes the rule first and the acceptance criteria require it to be unamended.
- Risk: an axis fails and the session stops to diagnose it. Impact: the remaining axes are never measured, and knowing that three of four survive is lost. Mitigation: the acceptance criteria require the matrix to continue past a failure with the symptom classified and routed.
- Risk: two things change on one axis and the verdict is ambiguous — most plausibly on the mode-switch axis, where invariant 4 forces the sensor layer at the same time. Impact: a verdict that cannot be attributed. Mitigation: the axis is stated as "survives a mode switch" with the forcing recorded, not as a claim about either layer alone.
- Risk (`R10`, `QAS-03`): the matrix is written up at the end of a long session and an early verdict is misremembered. Impact: a table that does not match what happened. Mitigation: each row is written as its axis completes, from the snapshot filenames.
- Risk: the negative control is left in place and the device is used with an unpinned AGC. Impact: the exact regression this phase exists to prevent, caused by the phase. Mitigation: `F3.10-08` restores and re-verifies with a field read, a stream read and a capture; the closing bracket is part of the acceptance criteria.
- Risk: the reboot axis is judged only on the pin and the module's own persistence is not checked in the same file. Impact: a regression in layer persistence goes unnoticed during a session that rebooted the device. Mitigation: `VAL-PERSIST` reads both from one snapshot.
- Risk (`FIND-3.4-03`): a camera-provider abort mid-matrix contaminates the boot and later axes are unattributable. Impact: several axes silently invalid. Mitigation: checklist item 8 requires a reboot after any provider abort; an axis run in a contaminated boot is re-run rather than recorded.
- Risk (`FIND-2.3-04`): `CSIPHYHw:4 AvailableResource=0` is read as a leak signature after the restart axis. Impact: a false failure and an investigation into a non-problem. Mitigation: the evidence section records that it reads 0 on a clean boot and is not diagnostic.
- Risk: the negative control's capture is clean, contradicting `R12`'s premise. Impact: none, if reported — this would be a *good* finding that weakens the risk. Mitigation: the control's result is recorded as measured whatever it shows; the matrix is not a search for a confirmation.

## 12. Desired End State

A written survival matrix with a verdict for each of the four disturbance axes — each taken on the input keys and each carrying the front key — a measured signature for AGC's unpinned default behaviour reported against a prediction written before its capture, and a confirming clean 12.58 MP capture on the surviving state. The HAL md5, mount counts and enumeration are constant across every snapshot in the sequence; the trap count is constant at 0/12 **except** where a settings-screen visit moved it at value `0`, which `FIND-3.7-02` and `FIND-3.7-01` predict and which `F3.10-01`'s rule declares in advance.

`R12`'s exposure is then a known quantity: the project knows which ordinary events break the pin, knows what the broken state looks like in a snapshot and in an image, and has that state reported by the smoke script without opening the app.

The evidence an implementer should produce: nine or more snapshot filenames organised by axis, all three preference key values plus the front key before and after each disturbance from two independent views, the written prediction that preceded the control's capture, three measured originals with their thresholds, the configured-stream reads on the control and the restore, and the completed matrix.

The ledger summary Step 4 should append records: the verdict rule as written before the run, with its three pre-declarations; one line per axis with before/after values for all three keys and the front key, and the verdict, with any self-healing row labelled as such; the negative control's measured facts — three keys, front key, both streams, black fraction — beside the prediction written before its capture; the restore confirmation; the confirming capture's measured triple; the constant values held across the matrix, with any settings-screen trap-count movement noted as expected; and any routed finding with its symptom classified, including a front-key movement if one occurred.

## 13. Next Sub-Phase Transition Criteria

- All four axes have a verdict produced under the pre-written rule, taken on the two input keys, with any inputs-survived/derived-stale row labelled *self-healing* rather than failed.
- `pref_camera_picturesize_front_key` is recorded in every axis row and on both halves of the control, and the matrix states explicitly whether any axis moved it.
- The negative control's signature is measured — all three preference keys, the front key, both configured streams, and the black fraction — against both reference numbers **and** against the fold-versus-clean prediction written before the capture.
- The pin is restored through `pref_48m_key`=`0` and the restored state is confirmed by all three fields plus the front key, both streams, and a clean capture.
- The HAL md5, mount counts and enumeration are constant across every snapshot in the sequence; the trap count is 0/12 in every snapshot except where a settings-screen visit moved it, where the two written keys read value `0` and `F3.10-01`'s rule pre-declared the exception.
- Any failed axis is routed as a finding with its symptom classified, and the matrix is complete regardless.
- No enforcement mechanism was built and no `.agc` file was imported.
- `Faz3.11` has a matrix to turn into operator-facing instructions, and a stated front-key result to dispose of `FIND-3.7-03` against.
