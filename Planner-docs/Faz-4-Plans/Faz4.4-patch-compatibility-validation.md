# Faz 4.4 — Consolidated Patch Compatibility Validation

## 1. Context

Main-Planing Phase 4's acceptance signals define exactly what this sub-phase measures: "`dumpsys media.camera` shows RAW10/RAW_SENSOR 8192x6144 present with correct duration rows and no spurious entries at other resolutions; third-party apps and AGC both still work."

Autopsy adds the quantitative requirement. Section 12 under Phase 4: "Require the array-size delta (currently 508 → 868 int32) as a measured acceptance number, not a qualitative claim."

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
- The array entry count as a measured number compared against the Faz 4.1 target and the 508 baseline.
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

`agc-50mp-yama/hal-raw50-deneme.patch` records the pre-narrowing measurement this validation is compared against: the array grows from 508 to 868 int32 entries under the broad experimental patch. The 508 figure is the unpatched-for-RAW baseline and Faz 4.1's target is derived from it.

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
  - Description: Report the count as a number and compare against the Faz 4.1 target and the 508 baseline. Autopsy requires this to be a measured number rather than a qualitative claim.
  - Output: A numeric array count comparison.
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
- The array entry count is reported as a number and matches the Faz 4.1 target within an explained margin.
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
- `VAL-ARRAYCOUNT` (from Faz 4.1) — the numeric array count, the sub-phase's headline metric.
- `VAL-TABLES` (from Faz 4.2) — three-table consistency for the surviving entries.
- `VAL-MANUAL` (proposed) — the user checklist: Open Camera capture with a measured result, stock camera shutter, video at both profiles, ten-mode camera opens, and the AGC check. Autopsy's Gate 3 in full.
- `VAL-COMPARE` (proposed) — comparison of every verdict against the Faz 2.2 baseline, the Faz 2.3 regression record, and the Faz 3.4 consumer survey.
- `VAL-PERSIST` (from Faz 2.3) — reboot and re-snapshot for the consolidated state.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist.

Local versus live: entirely live. Security validation is not applicable at this stage; distribution safety in the packaging sense is Faz 9.1's assertion set. Ontology validation covers invariants 4, 5, and 7.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Per-mode and per-check state reporting. | VAL-SMOKE, VAL-ARRAYCOUNT, VAL-PERSIST |
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
- Risk (invariant 4): Faz 4.3's structural change broke the exclusion enforcement and it is not noticed because individual modes work. Impact: a state where both layers are active, which produced corrupted output historically. Mitigation: F4.4-07 exercises both transitions as a distinct work item.
- Risk: reboot persistence fails because `post-fs-data.sh` was not updated for a renamed HAL state. Impact: 50 MP works interactively and vanishes after every reboot. Mitigation: F4.4-08 tests the boot path specifically, which is separate from the interactive path.
- Risk: a failure is repaired inline because it looks small. Impact: the validation record describes a configuration that no longer exists, and the repair skips its owning sub-phase's checks. Mitigation: the out-of-scope section and the acceptance criteria both require routing.
- Risk: the ten-mode pass is compressed because it repeats Faz 2.3. Impact: a HAL-layer regression affecting sensor-layer modes goes undetected, which is precisely what a shared control flow makes possible. Mitigation: F4.4-06 compares against the recorded reference, making it a diff rather than a repetition.
- Risk: `CQ-07` is answered affirmatively without the duration rows being verified. Impact: the answer criterion is only half met. Mitigation: the criterion in Project-Comprehension names both conditions, and `VAL-TABLES` checks the second.

## 12. Desired End State

The consolidated patch is validated as a shippable artifact: the stream configuration surface carries exactly the intended entries with matching duration rows, the array count matches a pre-stated target as a measured number, every consumer the project has documented behaves as expected, all ten modes work, the exclusion rule holds in both directions, and the state survives a reboot. `CQ-07` is answered by the artifact.

The evidence an implementer should produce is the extracted stream and duration rows, the numeric array count, the measured Open Camera resolution, the ten-mode comparison, the two transition verdicts, and the persistence verdict.

The ledger summary Step 4 should append records: the measured array count against target, the consumer results, the ten-mode outcome, the invariants exercised, the `CQ-07` resolution, and any routed finding.

## 13. Next Sub-Phase Transition Criteria

- The stream configuration surface matches the intent with no spurious entries.
- The array count is a number matching the pre-stated target.
- Open Camera's resolution is measured and correct.
- All ten modes pass against the regression reference.
- Both exclusion transitions and reboot persistence are confirmed.
- `CQ-07` is resolved or its remaining gap is recorded.
- No unrouted failure remains, and Phase 9 has a validated artifact to package.
