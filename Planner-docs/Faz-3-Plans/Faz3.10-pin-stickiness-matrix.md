# Faz 3.10 — Pin Stickiness Across Reboot, Mode Switch, Cold Start and Camera Restart

## 1. Context

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
- A negative control: the pin cleared deliberately, AGC's own selection recorded from the preference field, the configured stream and one capture, then the pin restored and re-verified.
- One confirming capture at the end of the matrix, measured by the `IMPL-40` method, establishing that a surviving pin still yields a clean 12.58 MP image.
- A written matrix with one row per axis: disturbance, pin value before, pin value after, verdict, and the snapshot filenames.
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

`IMPL-43` records the behaviour the negative control tests: under the seven-word stack "AGC auto-select[ed] `RAW10 8192x6144` with no preferences set at all", and with `pref_camera_picturesize_back_key` at `4096x3072` it "opened a `4096x3072` reader and matched cleanly at half resolution". The first half is the default this control measures; the second is the state it restores.

`IMPL-43` also records the fold signature to expect from the negative control: `6144x8192` = 50.33 MP with black fraction **0.7497** and quadrant fractions 1.0000 / 1.0000 / 0.4994 / 0.4994 — content occupying exactly one quadrant. `IMPL-40` records the clean reference at **0.0024**. Those two numbers are what the control's capture is compared against.

`IMPL-16` records that AGC does **not** self-arm the trap keys, verified across an AGC restart from an empty preference state. That is relevant here because the cold-start axis is the same kind of disturbance, and it means an observed re-arming during this matrix would be a new finding rather than known behaviour.

`scripts/smoke.sh` after `Faz3.8` reports the pin, `pref_48m_key`, the derived megapixels, the HAL md5, both mount counts, the mode, all camera rows, and the trap count — which is every value each axis needs to be judged on, from one file.

## 7. Planned Work Breakdown

- F3.10-01 — Fix the matrix and its verdict rule before running it
  - Description: Write the four axes plus the negative control, the disturbance procedure for each, and the rule that decides pass or fail, before the first disturbance. A verdict rule agreed after seeing a result is not a rule.
  - Output: A written matrix skeleton with an explicit verdict rule.
- F3.10-02 — Axis 1: AGC cold start
  - Description: Force-stop AGC, relaunch it, snapshot, and read the pin. Cheapest axis and the one `R12` names explicitly.
  - Output: A verdict row with before/after pin values and the snapshot names.
- F3.10-03 — Axis 2: camera-stack restart
  - Description: Trigger the module's own camera-restart sequence, respecting the client-before-HAL ordering invariant 3 fixes, then snapshot and read the pin.
  - Output: A verdict row, plus confirmation that mount counts stayed at 1/1.
- F3.10-04 — Axis 3: QuickSettings mode switch
  - Description: Switch away from the 50 MP state and back through the tile, snapshot after each transition, and read the pin. Record that the sensor layer was forced by invariant 4 rather than chosen.
  - Output: Two snapshots and a verdict row naming both transitions.
- F3.10-05 — Axis 4: device reboot
  - Description: Reboot, wait for the camera stack, snapshot, and read the pin together with the full layer state, so layer persistence and pin persistence are judged from one file.
  - Output: A verdict row plus a layer-persistence confirmation.
- F3.10-06 — Confirming capture on the surviving state
  - Description: With the matrix complete and the pin at whatever value survived, take one capture and measure it by the `IMPL-40` method, so the matrix ends in an image result rather than a preference value.
  - Output: A measured triple against the stated threshold.
- F3.10-07 — Negative control: clear the pin and record AGC's own selection
  - Description: Clear `pref_camera_picturesize_back_key`, cold-start AGC, snapshot, read the pin field and the configured stream with AGC open, and take one capture. Measure it and compare against both the 0.0024 clean reference and the 0.7497 fold signature.
  - Output: The measured default-behaviour signature — field value, configured stream, and black fraction.
- F3.10-08 — Restore the pin and re-verify
  - Description: Restore `4096x3072`, cold-start AGC, snapshot, and confirm the field, the configured stream and a clean capture. The control must not be the state the device is left in.
  - Output: A restored-state confirmation with a closing bracket.
- F3.10-09 — Write the matrix and route what failed
  - Description: Complete the table with one row per axis, and route any failed axis as a named finding with its symptom classified — not diagnosed.
  - Output: A complete survival matrix and zero or more routed findings.

## 8. Acceptance Criteria

- The matrix contains one row per axis — cold start, camera-stack restart, mode switch, reboot — each with the pin value before and after, a verdict, and the snapshot filenames.
- The verdict rule was written before the first disturbance and was not amended after a result was seen.
- The HAL md5 is identical in every snapshot in the matrix; an axis that changed it is invalid and is re-run.
- The negative control records AGC's own selection as three measured facts: the preference field value, the configured stream from `dumpsys` with AGC open, and the black fraction of a capture — with the last compared against both the 0.0024 and 0.7497 references.
- The pin is restored after the control, and the restored state is confirmed by a field read, a configured-stream read, and one clean capture.
- The confirming capture on the surviving state measures 12.58 MP and passes the threshold stated in `Faz3.7`.
- Mount counts read 1/1 in every snapshot; camera enumeration reads 13 in every snapshot; the trap count reads 0/12 in every snapshot.
- After the reboot axis, the module's own layer state is confirmed persistent in the same snapshot, so the two kinds of persistence are judged together.
- Any axis that fails is recorded with its symptom classified and routed as a finding; the matrix continues past it rather than stopping.
- No enforcement mechanism was built, and no `.agc` file was imported.

## 9. Validation and Test Approach

Validation is live and repetitive by design. The distinguishing property is that most verdicts come from a **text field in a snapshot**, not from a photograph — which is the entire point of building the instrument in `Faz3.8` before this sub-plan runs.

- `VAL-SMOKE` (from Faz 2.1, extended by Faz 3.8) — one snapshot per disturbance, comparable regions diffed against the previous snapshot in the sequence.
- `VAL-PREFPIN` (from Faz 3.7) — the pin read before and after each disturbance, independently of the smoke field, so the two views can be shown to agree.
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

Depends on `Faz3.9` for an established coexistence state to attack, on `Faz3.8` for a snapshot that contains the pin, and on `Faz3.7` for the pin, the measurement method and the pass threshold. Depends on `DEC-15` having been answered, since the matrix must run on the base the phase adopts.

Depends on `Faz2.3`'s persistence result as the reference for module-state persistence, so the reboot axis compares against something rather than judging in isolation.

Blocks `Faz3.11`, which records the matrix as operator-facing documentation and closes the phase.

Required decisions: none new, provided `DEC-15` is answered. If an axis fails and the user wants enforcement rather than documentation, that is a new decision and a new sub-plan — this one does not take it.

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

A written survival matrix with a verdict for each of the four disturbance axes, a measured signature for AGC's unpinned default behaviour, and a confirming clean 12.58 MP capture on the surviving state — with the HAL md5, mount counts, enumeration and trap count constant across every snapshot in the sequence.

`R12`'s exposure is then a known quantity: the project knows which ordinary events break the pin, knows what the broken state looks like in a snapshot and in an image, and has that state reported by the smoke script without opening the app.

The evidence an implementer should produce: nine or more snapshot filenames organised by axis, the pin value before and after each disturbance from two independent views, three measured originals with their thresholds, the configured-stream reads on the control and the restore, and the completed matrix.

The ledger summary Step 4 should append records: the verdict rule as written before the run; one line per axis with before/after pin values and verdict; the negative control's three measured facts; the restore confirmation; the confirming capture's measured triple; the constant values held across the matrix; and any routed finding with its symptom classified.

## 13. Next Sub-Phase Transition Criteria

- All four axes have a verdict produced under the pre-written rule.
- The negative control's signature is measured — field, configured stream, and black fraction — against both reference numbers.
- The pin is restored and the restored state is confirmed by field, stream and a clean capture.
- The HAL md5, mount counts, enumeration and trap count are constant across every snapshot in the sequence.
- Any failed axis is routed as a finding with its symptom classified, and the matrix is complete regardless.
- No enforcement mechanism was built and no `.agc` file was imported.
- `Faz3.11` has a matrix to turn into operator-facing instructions.
