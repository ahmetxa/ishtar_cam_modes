# Faz 4.4 — Consolidated Patch Compatibility Validation

## 1. Context

Main-Planing Phase 4's acceptance signals define exactly what this sub-phase measures: "`dumpsys media.camera` shows RAW10/RAW_SENSOR 8192x6144 present with correct duration rows and no spurious entries at other resolutions; third-party apps and AGC both still work."

Autopsy adds the quantitative requirement. Section 12 under Phase 4: "Require the array-size delta (currently 508 → 868 int32) as a measured acceptance number, not a qualitative claim."

**Amended 2026-09-01 (`AUDIT-FIX-09`). That quoted pair of numbers may not be used as a baseline without being qualified first, and this sub-plan is the worst place in the project for the ambiguity to survive, because reporting the count as a number is its entire job.** A bare "508" names neither a camera id nor a metric. `IMPL-25` identified it as **`camera.hal3` in the fullres state, on the `streamcfg` int32 element count**, against hal0's fullres figure of 456 — and `scripts/smoke.sh` prints hal0 **first**, because its output is sorted by id, so a reading taken from the top line does not compare against 508 at all. **The recorded figures also disagree with each other and this sub-plan must not paper over it:** `EV-16` and the `hal-raw50-deneme.patch` header record 508 → 868, while `IMPL-30`'s bracket recorded `camera.hal0` 440 → 800 and `camera.hal3` 500 → 868 under the seven-word stack built on the fullres base. Whether the 8-entry difference is a base-state difference, a transcription slip, or a real change is not settled by the record. **Therefore this sub-plan does not quote a baseline. It reads the baseline from a bracketed snapshot in the state it is comparing against, names the camera id and the metric with the number, and inherits its target from what `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` actually stated rather than re-deriving it from Autopsy's figure.**

**Amended 2026-09-01: this sub-plan also carries `FIND-4.5-01` (P2, open), routed here by `IMPL-28`.** The active-array raise is **global, not per-sensor**. Because the patched word sits in the shared `android.sensor.info.*` publishing routine rather than in a per-sensor path, the front cameras moved too — `hal1`, `hal8` and `hal9` went `[0 0 3264 2448]` -> `[0 0 6528 4896]`, exactly 2x — while `hal11` and `hal12` were unaffected, consistent with their selector not taking the binned branch. **The consequence is an internally inconsistent metadata pair on cameras this project never intended to touch:** the front cameras now advertise an `activeArray` *larger than their own `pixelArray`*. The wide camera does not have this problem, because `f0006` is raised alongside on it. Whether the raise needs scoping to the wide sensor, or is harmless because nothing consumes the front active array at full extent, is **not answered by any measurement taken so far** — and a patch intended for other people's devices cannot ship with that question open. This sub-plan is where it is answered.

This is the phase's closing validation and it differs from Faz 3.4's consumer survey in an important way. Faz 3.4 asked whether a single-word metadata change broke anything. This asks whether the complete, consolidated, shippable patch — narrowed emission, duration rows, and pixel array change together — is safe to distribute. The patch is intended for other people's devices, which is the argument Project-Comprehension `QAS-04` makes for narrowing in the first place: "the patch is intended for distribution."

The full ten-mode surface matters here too. Project-Ontology invariant 4 records that `50mp` and the DCG and LN modes are mutually exclusive, and Autopsy section 6 notes the rule is enforced by shell control flow rather than by a checked invariant. A consolidated patch that redefines the HAL state — which Faz 4.3's structural decision may do — touches exactly that control flow.

## 2. Goal

Establish by measurement that the consolidated patch delivers the intended stream configuration surface, preserves every capability the project already had, and is safe to distribute — with the array size expressed as a number rather than as a claim.

## 3. Description

The problem is that Phase 4 made three separate changes to a system binary and each was validated against its own narrow criterion. Narrowing was validated by array count, duration rows by table consistency, consolidation by checksum. None of those establishes that the whole is correct, and the whole is what ships.

It belongs at the end of Phase 4 because it validates the phase's product rather than any of its steps.

The vibecoding slice strategy: measure the stream configuration surface first, because it is automated and decisive — a wrong surface means nothing else needs checking. Then run the consumer set, then the ten-mode surface. The fastest validation signal is the array entry count against the Faz 4.1 target, which the smoke script already reports.

What should not be over-planned: a distribution readiness assessment covering packaging, documentation, and release process. Those are Phase 9. This sub-phase answers whether the patch is technically sound, not whether the release is ready.

The comparison baselines are already established and should be used rather than re-derived: the Faz 2.2 named baseline for pre-Phase-3 device state, the Faz 2.3 regression record for the ten-mode surface, and the Faz 3.4 consumer survey for post-pixel-array consumer behavior. Three recorded reference points exist precisely so this validation is a diff rather than a fresh investigation.

## 4. Scope

- The stream configuration surface: RAW10 and RAW_SENSOR present at 8192x6144, duration rows matching, and no spurious entries at other resolutions.
- The array entry count as a measured number, **stated with its camera id and its metric**, compared against the two targets `Faz 4.1` stated and against a baseline read from a bracketed snapshot rather than quoted from Autopsy.
- The front-camera consequence of the global active-array raise (`FIND-4.5-01`): whether `hal1`, `hal8` and `hal9` advertising `activeArray` larger than their own `pixelArray` is tolerable in a distributed patch, and what the disposition is.
- Open Camera at full resolution, with the result measured numerically against the documented 50.3 MP.
- The AGC path, per whatever state Faz 3.6 established as the phase 3 outcome.
- The stock camera application and the video path at 1080p60 and 4K60.
- The full ten-mode surface, comparing against the Faz 2.3 regression record.
- Both exclusion-boundary transitions, since Faz 4.3 may have altered the control flow that enforces the rule.
- Reboot persistence for the consolidated HAL state, since `post-fs-data.sh` reapplies it through a different path.
- `CQ-07` — "What is the smallest correct HAL patch?" — resolved with the answer being the artifact itself.

## 5. Out of Scope

- Any further patch modification. If validation fails, the finding routes back to the sub-phase that owns the affected change rather than being fixed here.
- Release packaging, build scripts, or distribution decisions. Phase 9 owns those.
- Image quality assessment beyond resolution and obvious correctness.
- Composing 50 MP with LN modes, which is Phase 5 and currently excluded by invariant 4.
- Long-run stability, thermal, or battery testing.
- Any change to the sensor blobs or the mode dispatch.
- Re-deriving addresses. Phase 4's disassembly work is complete by this point.

## 6. Current Repository Evidence

`agc-50mp-yama/hal-raw50-deneme.patch` records a pre-narrowing measurement of 508 to 868 int32 entries under the broad experimental patch. **That figure is used here only as provenance, never as the comparison baseline** — see the `AUDIT-FIX-09` amendment in section 1. It names no camera id and no metric, and it disagrees with `IMPL-30`'s bracketed reading of `camera.hal3` 500 -> 868 in an adjacent state. The comparison baseline is read fresh, per camera id, from a bracketed `scripts/smoke.sh` snapshot.

`Planner-docs/Project-Ontology.md` section 6 records the `FIND-4.5-01` measurement this sub-plan must dispose of: under the single `f0000` word alone, `hal1`, `hal8` and `hal9` moved `[0 0 3264 2448]` -> `[0 0 6528 4896]` while `hal11` and `hal12` did not, and `hal0` and `hal2`…`hal7` and `hal10` moved to `[0 0 8192 6144]`. Every `streamcfg` count and every `pixelArray` value was unchanged by that word, and the bracketed comparable-region diff was exactly thirteen lines. The front cameras' `pixelArray` did **not** move, which is what leaves them internally inconsistent.

The same file records the three entries that should be present at full resolution: `[37 8192 6144 OUTPUT]`, `[38 8192 6144 OUTPUT]`, and `[36 8192 6144 OUTPUT]`, subject to whatever format set Faz 4.2 settled.

Project-Comprehension `EV-04` records Open Camera measured at 50.3 MP with confidence `confirmed`, which is the numeric expectation for the third-party consumer check. `EV-16` records the 508-to-868 measurement with confidence `confirmed`.

`ishtar-cam-modes/halpatch.sh` records why third-party behavior is the sensitive signal: without the patch, Open Camera silently drops to 12.6 MP even when its menu offers 50 MP. A silent drop is the failure mode to watch for, and it is invisible without a numeric measurement.

`ishtar-cam-modes/post-fs-data.sh` was inspected in this run. Its dispatch sets the HAL wanted state for `50mp` and stock for the nine sensor modes, with unrecognized values mapping to stock across all three variables. If Faz 4.3 changed the HAL state naming, this dispatch is directly affected and reboot persistence is the check that catches it.

`ishtar-cam-modes/setmode.sh` documents the exclusion rule in its header and implements it by setting `HAL_WANT` alongside the sensor mode. Its `restart_camera` applies the HAL change inside the service-stopped window.

`docs/regression-v2.1.md` from Faz 2.3 provides the ten-mode reference, and the Faz 2.2 baseline snapshot provides the device state reference. `docs/consumer-survey.md` from Faz 3.4 provides the consumer reference after the pixel array change but before narrowing.

Project-Comprehension `CQ-07` remains open at Phase 4's start: "What is the smallest correct HAL patch? Answer criterion: A patch adding RAW only at full resolution, with duration rows." That criterion is satisfied by this validation or it is not.

## 7. Planned Work Breakdown

- F4.4-01 — Measure the stream configuration surface
  - Description: Extract the RAW format rows and the matching duration rows for camera 3, and confirm full resolution is present with nothing spurious elsewhere.
  - Output: A stream configuration verdict with the extracted rows.
- F4.4-02 — Measure the array entry count
  - Description: Report the count as a number **with its camera id and its metric named** — the `streamcfg` int32 element count for a stated `camera.hal<id>` — and compare it against the two targets `Faz 4.1` stated and against a baseline read from a bracketed snapshot in the same state. Autopsy requires a measured number rather than a qualitative claim; `AUDIT-FIX-09` requires that the number be attributable. Do not quote 508 as a baseline, and note that `scripts/smoke.sh` sorts by id, so hal0 is the first line and is not hal3.
  - Output: A numeric array count comparison, per camera id, against a freshly read baseline and against `Faz 4.1`'s stated targets.
- F4.4-02b — Dispose of the global active-array raise (`FIND-4.5-01`)
  - Description: Measure `activeArray` and `pixelArray` for **every** camera id under the consolidated patch, not only the wide camera, and identify each id where `activeArray` now exceeds its own `pixelArray`. Then establish whether anything consumes the front cameras' active array at full extent — the stock camera's front path, the front video profiles, and any application in the Faz 3.4 consumer set that uses a front camera — and state a disposition: tolerable as-is, or requiring the raise to be scoped to the wide sensor. A scoping requirement is a **decision raised to the user with the evidence attached**, not a repair made here, per this sub-plan's out-of-scope rule — scoping the raise to one sensor is a fresh write-site question of the kind `Faz4.5` was created to hold, and it would need its own owner.
  - Output: A per-camera-id array consistency table, a front-camera behavioural verdict, and a stated disposition for `FIND-4.5-01`.
- F4.4-03 — Validate the third-party consumer
  - Description: Capture with Open Camera at full resolution and measure the result numerically against the documented 50.3 MP.
  - Output: An Open Camera verdict with a measured resolution.
- F4.4-04 — Validate the AGC path
  - Description: Confirm AGC behaves as the Faz 3.6 outcome established — a completing capture if Phase 3 succeeded, or the recorded fallback behavior if it did not.
  - Output: An AGC verdict against the recorded expectation.
- F4.4-05 — Validate the stock camera and video path
  - Description: Stock camera opens with a live preview and completes a shutter; 1080p60 and 4K60 record and play back. Tests invariant 5.
  - Output: Five verdicts.
- F4.4-06 — Run the ten-mode surface against the regression record
  - Description: Switch through all ten modes, confirming layer state and camera open per mode, compared against the Faz 2.3 record.
  - Output: Ten rows compared against the reference.
- F4.4-07 — Exercise both exclusion-boundary transitions
  - Description: Switch across the boundary in both directions, since Faz 4.3 may have changed the control flow enforcing invariant 4.
  - Output: Two transition verdicts.
- F4.4-08 — Verify reboot persistence for the consolidated state
  - Description: Set `50mp`, reboot, and confirm the HAL state reapplies through the boot path.
  - Output: A persistence verdict.
- F4.4-09 — Resolve the smallest-correct-patch question
  - Description: Answer `CQ-07` with the consolidated artifact as the answer, or record what remains unsatisfied.
  - Output: An updated comprehension question.

## 8. Acceptance Criteria

- RAW10 and RAW_SENSOR are present at 8192x6144 with matching duration rows in both duration tables.
- No RAW format entries exist at resolutions other than full resolution.
- The array entry count is reported as a number **carrying its camera id and its metric**, matches the corresponding `Faz 4.1` target within an explained margin, and is compared against a baseline read from a bracketed snapshot rather than against a quoted figure. No unqualified "508" appears in the result.
- Every camera id has an `activeArray` and `pixelArray` reading under the consolidated patch, every id where the first exceeds the second is named, and `FIND-4.5-01` carries a stated disposition backed by a front-camera behavioural check rather than by assumption.
- Open Camera's full-resolution result is measured numerically and matches the documented value.
- The AGC path matches the expectation the Faz 3.6 outcome established.
- The stock camera opens, previews, and completes a shutter; video records and plays at both profiles.
- All ten modes have a verdict compared against the Faz 2.3 regression record, with no regression.
- Both exclusion-boundary transitions behave per invariant 4.
- Reboot persistence for the consolidated HAL state is confirmed.
- `CQ-07` is resolved, or what remains unsatisfied is recorded explicitly.
- Any failure is routed to the owning sub-phase rather than repaired here.

## 9. Validation and Test Approach

This is the phase's validation sub-phase, so its approach is the validation. The design principle is comparison against recorded references rather than fresh judgment.

- `VAL-SMOKE` (from Faz 2.1) — the state reporter, used per mode and around each check.
- `VAL-ARRAYCOUNT` (from Faz 4.1) — the numeric array count, the sub-phase's headline metric, reported per camera id with the `streamcfg` int32 metric named.
- `VAL-ARRAYCONSIST` (proposed) — `activeArray` against `pixelArray` for **every** camera id under the consolidated patch, which is what `FIND-4.5-01` needs and what no prior measurement has covered across the full id set.
- `VAL-TABLES` (from Faz 4.2) — three-table consistency for the surviving entries.
- `VAL-MANUAL` (proposed) — the user checklist: Open Camera capture with a measured result, stock camera shutter, video at both profiles, ten-mode camera opens, and the AGC check. Autopsy's Gate 3 in full.
- `VAL-COMPARE` (proposed) — comparison of every verdict against the Faz 2.2 baseline, the Faz 2.3 regression record, and the Faz 3.4 consumer survey.
- `VAL-PERSIST` (from Faz 2.3) — reboot and re-snapshot for the consolidated state.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist.

Local versus live: entirely live. Security validation is not applicable at this stage; distribution safety in the packaging sense is Faz 9.1's assertion set. Ontology validation covers invariants 4, 5, and 7.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Per-mode and per-check state reporting, and the per-camera-id `activeArray` / `pixelArray` readings. | VAL-SMOKE, VAL-ARRAYCOUNT, VAL-ARRAYCONSIST, VAL-PERSIST |
| Planner-docs/Project-Ontology.md | modified | Record the `FIND-4.5-01` disposition and the per-camera-id consistency result against the address book's existing raise entry. | VAL-ARRAYCONSIST |
| ishtar-cam-modes/blobs/hal-fullres.patch | existing | The consolidated artifact under validation; read, not modified. | VAL-TABLES |
| docs/regression-v2.1.md | existing | The ten-mode reference for comparison. | VAL-COMPARE |
| docs/consumer-survey.md | existing | The post-pixel-array consumer reference. | VAL-COMPARE |
| docs/patch-validation-phase4.md | proposed | The validation record produced by this sub-phase. | VAL-COMPARE, VAL-MANUAL |

## 10. Dependencies and Sequencing

Depends on Faz 4.3 for the consolidated artifact, and on Faz 2.2, Faz 2.3, and Faz 3.4 for the three recorded references every comparison uses.

Depends on Faz 3.6 for the AGC expectation, since what counts as correct AGC behavior differs between the success and fallback outcomes.

Blocks Phase 9's release work, which should not package a patch that has not passed this validation. Does not block Phase 5, though Main-Planing's ordering places Phase 5 after Phase 4 and the Faz 3.6 priority decision may have changed that.

Required human actions: every consumer check, every camera open, every video recording, and two reboots. This is a user-intensive sub-phase comparable to Faz 2.3.

Required infrastructure: the device, the Open Camera build, the AGC build, and storage for recordings.

Required approvals: running a patched HAL through the full application set.

Fresh session token and context risk: medium. High verdict volume, low per-verdict cost. The mitigation is the same as Faz 2.3's — write verdicts into the record as they are produced.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: Open Camera is checked without measuring and a silent resolution drop goes unnoticed. Impact: the exact failure `halpatch.sh` documents as happening without the patch, now happening with a defective one. Mitigation: F4.4-03 and the acceptance criteria both require a numeric measurement.
- Risk: the array count is reported qualitatively as reduced. Impact: Autopsy's explicit requirement is unmet and the narrowing's success is unfalsifiable. Mitigation: F4.4-02 requires a number compared against a pre-stated target.
- Risk (`AUDIT-FIX-09`): the count is compared against the unqualified 508 figure. Impact: a comparison against the wrong camera — 508 is hal3 in fullres, hal0's figure is 456, and smoke prints hal0 first — producing a confident wrong verdict on the sub-plan's headline metric. Mitigation: section 1's amendment forbids quoting the figure, F4.4-02 requires the camera id and the metric alongside the number, and the baseline is read from a bracketed snapshot in the comparison state.
- Risk (`FIND-4.5-01`): the front cameras' inconsistent array pair is checked only by reading metadata, and a consumer that actually breaks on it is not exercised. Impact: a patch ships that is internally inconsistent on three camera ids nobody tested, on other people's devices. Mitigation: F4.4-02b requires a behavioural check on the front path, not only a metadata table, and F4.4-05's stock-camera and video checks are run on the front camera as well as the rear.
- Risk (invariant 4): Faz 4.3's structural change broke the exclusion enforcement and it is not noticed because individual modes work. Impact: a state where both layers are active, which produced corrupted output historically. Mitigation: F4.4-07 exercises both transitions as a distinct work item.
- Risk: reboot persistence fails because `post-fs-data.sh` was not updated for a renamed HAL state. Impact: 50 MP works interactively and vanishes after every reboot. Mitigation: F4.4-08 tests the boot path specifically, which is separate from the interactive path.
- Risk: a failure is repaired inline because it looks small. Impact: the validation record describes a configuration that no longer exists, and the repair skips its owning sub-phase's checks. Mitigation: the out-of-scope section and the acceptance criteria both require routing.
- Risk: the ten-mode pass is compressed because it repeats Faz 2.3. Impact: a HAL-layer regression affecting sensor-layer modes goes undetected, which is precisely what a shared control flow makes possible. Mitigation: F4.4-06 compares against the recorded reference, making it a diff rather than a repetition.
- Risk: `CQ-07` is answered affirmatively without the duration rows being verified. Impact: the answer criterion is only half met. Mitigation: the criterion in Project-Comprehension names both conditions, and `VAL-TABLES` checks the second.

## 12. Desired End State

The consolidated patch is validated as a shippable artifact: the stream configuration surface carries exactly the intended entries with matching duration rows, the array count matches a pre-stated target as a measured number, every consumer the project has documented behaves as expected, all ten modes work, the exclusion rule holds in both directions, and the state survives a reboot. `CQ-07` is answered by the artifact.

`FIND-4.5-01` is disposed of rather than carried into a release: every camera id's `activeArray` and `pixelArray` are recorded, the ids where the pair is inconsistent are named, and the front-camera behaviour under that inconsistency is measured rather than assumed harmless.

The evidence an implementer should produce is the extracted stream and duration rows, the numeric array count with its camera id and metric, the per-camera-id array consistency table, the measured Open Camera resolution, the ten-mode comparison, the two transition verdicts, and the persistence verdict.

The ledger summary Step 4 should append records: the measured array count against target, the consumer results, the ten-mode outcome, the invariants exercised, the `CQ-07` resolution, and any routed finding.

## 13. Next Sub-Phase Transition Criteria

- The stream configuration surface matches the intent with no spurious entries.
- The array count is a number carrying its camera id and metric, matching the pre-stated target.
- `FIND-4.5-01` has a stated disposition backed by a per-camera-id table and a front-camera behavioural check, and any scoping requirement is raised to the user rather than repaired here.
- Open Camera's resolution is measured and correct.
- All ten modes pass against the regression reference.
- Both exclusion transitions and reboot persistence are confirmed.
- `CQ-07` is resolved or its remaining gap is recorded.
- No unrouted failure remains, and Phase 9 has a validated artifact to package.
