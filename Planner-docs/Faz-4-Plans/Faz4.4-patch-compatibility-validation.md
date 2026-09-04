# Faz 4.4 — Consolidated Patch Compatibility Validation

## 1. Context

Main-Planing Phase 4's acceptance signals define exactly what this sub-phase measures. Quoted from the **amended** Phase 4 (`DEC-14`, 2026-09-03): "`dumpsys media.camera` shows RAW10 at 8192x6144 with correct duration rows; Open Camera still captures 50.3 MP; **AGC still launches and captures cleanly at 12.58 MP** — the criterion `IMPL-49` showed the old narrowing goal silently violated." *(Until `AUDIT-FIX-17` this line quoted the pre-amendment wording, which named RAW_SENSOR and required "no spurious entries at other resolutions". Both clauses are retired; see the `DEC-14` amendment below and section 8.)*

Autopsy adds the quantitative requirement. Section 12 under Phase 4: "Require the array-size delta (currently 508 → 868 int32) as a measured acceptance number, not a qualitative claim."

**Amended 2026-09-01 (`AUDIT-FIX-09`). That quoted pair of numbers may not be used as a baseline without being qualified first, and this sub-plan is the worst place in the project for the ambiguity to survive, because reporting the count as a number is its entire job.** A bare "508" names neither a camera id nor a metric. `IMPL-25` identified it as **`camera.hal3` in the fullres state, on the `streamcfg` int32 element count**, against hal0's fullres figure of 456 — and `scripts/smoke.sh` prints hal0 **first**, because its output is sorted by id, so a reading taken from the top line does not compare against 508 at all. **The recorded figures also disagree with each other and this sub-plan must not paper over it:** `EV-16` and the `hal-raw50-deneme.patch` header record 508 → 868, while `IMPL-30`'s bracket recorded `camera.hal0` 440 → 800 and `camera.hal3` 500 → 868 under the seven-word stack built on the fullres base. Whether the 8-entry difference is a base-state difference, a transcription slip, or a real change is not settled by the record. **Therefore this sub-plan does not quote a baseline. It reads the baseline from a bracketed snapshot in the state it is comparing against, names the camera id and the metric with the number, and inherits its target from what `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` actually stated rather than re-deriving it from Autopsy's figure.** *(Superseded in its last clause by the `DEC-14` amendment immediately below: `Faz4.1` states no target any more, so the count is reported with a delta and no target. The baseline discipline this paragraph establishes is unaffected and still binds.)*

**Amended 2026-09-01: this sub-plan also carries `FIND-4.5-01` (P2, open), routed here by `IMPL-28`.** The active-array raise is **global, not per-sensor**. Because the patched word sits in the shared `android.sensor.info.*` publishing routine rather than in a per-sensor path, the front cameras moved too — `hal1`, `hal8` and `hal9` went `[0 0 3264 2448]` -> `[0 0 6528 4896]`, exactly 2x — while `hal11` and `hal12` were unaffected, consistent with their selector not taking the binned branch. **The consequence is an internally inconsistent metadata pair on cameras this project never intended to touch:** the front cameras now advertise an `activeArray` *larger than their own `pixelArray`*. The wide camera does not have this problem, because `f0006` is raised alongside on it. Whether the raise needs scoping to the wide sensor, or is harmless because nothing consumes the front active array at full extent, is **not answered by any measurement taken so far** — and a patch intended for other people's devices cannot ship with that question open. This sub-plan is where it is answered.

**Amended 2026-09-03 by `DEC-14` (planning run 8). The narrowing target this sub-plan was to measure against no longer exists, and its replacement is a behavioural criterion rather than a numeric one.** `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` is `superseded`: `IMPL-48`–`IMPL-50` measured that narrowing hits every numeric target and still prevents AGC from launching, 3/3 at two independent bisection stages. Three changes follow.

- **There is no "`Faz 4.1` stated target" to compare the array count against.** The count is still reported — per camera id, with the `streamcfg` int32 metric named, against a freshly bracketed baseline — but it is now reported as a *fact about the shipped surface*, not as a pass against a reduction goal. Do not invent a substitute target to fill the gap.
- **`QAS-04`'s blast-radius argument survives the narrowing's retirement and must be restated honestly.** The patch is still intended for other people's devices and it is now measurably **broader** than the project once intended to ship. That is a distribution consideration this sub-plan must report rather than omit, and it is now one of the strongest reasons `FIND-4.5-01`'s global-raise question must be answered here.
- **The headline criterion becomes coexistence.** `Main-Planing.md`'s amended Phase 4 names it: "`dumpsys media.camera` shows RAW10 at 8192x6144 with correct duration rows; Open Camera still captures 50.3 MP; **AGC still launches and captures cleanly at 12.58 MP** — the criterion `IMPL-49` showed the old narrowing goal silently violated."

**Amended 2026-09-04 (`AUDIT-FIX-17`, Step 3.1).** The `DEC-14` amendment above reached this section and stopped, leaving four contradictions downstream of it. Sections 4 and 8 still required `RAW_SENSOR` (format 32) at 8192x6144, which `Faz 4.2`'s amended scope and `IMPL-50` establish is never emitted and has no additive route. Section 8 still required that "no RAW format entries exist at resolutions other than full resolution", which **is** the retired narrowing and which the broad table violates by construction — an implementer meeting that criterion in the distribution gate would have been pointed back at exactly the action `IMPL-49` measured as preventing AGC from launching. Sections 4, 7, 8 and 10 took the AGC expectation from `Faz 3.6`, the fallback gate of the retired objective. Section 12 and section 13 still spoke of the array count "matching the pre-stated target", when `DEC-14` removed the target and forbade inventing a replacement. All of it is repaired below; nothing else in the sub-plan changed, and no measurement, device or new decision was required.

This is the phase's closing validation and it differs from Faz 3.4's consumer survey in an important way. Faz 3.4 asked whether a single-word metadata change broke anything. This asks whether the complete, consolidated, shippable patch — broad emission, duration rows, and the array changes together — is safe to distribute.

The full ten-mode surface matters here too. Project-Ontology invariant 4 records that `50mp` and the DCG and LN modes are mutually exclusive, and Autopsy section 6 notes the rule is enforced by shell control flow rather than by a checked invariant. A consolidated patch that redefines the HAL state — which Faz 4.3's structural decision may do — touches exactly that control flow.

## 2. Goal

Establish by measurement that the consolidated patch delivers the intended stream configuration surface, preserves every capability the project already had, and is safe to distribute — with the array size expressed as a number rather than as a claim.

## 3. Description

The problem is that Phase 4 made several separate changes to a system binary and each was validated against its own narrow criterion — duration rows by table consistency, consolidation by checksum, the array raise by tag value. None of those establishes that the whole is correct, and the whole is what ships. `IMPL-49` is the standing proof of that gap: a HAL table change can satisfy every count it was measured on and still stop AGC from starting.

It belongs at the end of Phase 4 because it validates the phase's product rather than any of its steps.

The vibecoding slice strategy: measure the stream configuration surface first, because it is automated and decisive — a wrong surface means nothing else needs checking. Then run the consumer set, then the ten-mode surface. The fastest validation signal is now **an AGC launch verdict plus one measured capture**, which is cheap, and which `IMPL-49` established is the check no count substitutes for; the array entry count remains a reported fact from the same smoke snapshot.

What should not be over-planned: a distribution readiness assessment covering packaging, documentation, and release process. Those are Phase 9. This sub-phase answers whether the patch is technically sound, not whether the release is ready.

The comparison baselines are already established and should be used rather than re-derived: the Faz 2.2 named baseline for pre-Phase-3 device state, the Faz 2.3 regression record for the ten-mode surface, and the Faz 3.4 consumer survey for post-pixel-array consumer behavior. Three recorded reference points exist precisely so this validation is a diff rather than a fresh investigation.

## 4. Scope

- The stream configuration surface: RAW10 present at 8192x6144 with matching rows in both duration tables, and the emitted RAW entry set recorded as it actually stands. **`RAW_SENSOR` (format 32) is not part of it** — `Faz 4.2`'s amended scope establishes it is never emitted (the gate admits `0x22..0x26` = 34–38 and `0x20` sits below the subtract base) and `IMPL-50` measured the additive route as having no implementation on a binary with no code cave ≥ 16 bytes. **Entries at resolutions other than full resolution are expected and are not spurious;** removing them is the retired narrowing.
- The array entry count as a measured number, **stated with its camera id and its metric**, compared against a baseline read from a bracketed snapshot rather than quoted from Autopsy, and reported as a fact about the shipped surface rather than as a pass against a retired reduction target.
- The coexistence criterion measured on the consolidated artifact: AGC launches and captures cleanly at 12.58 MP, and Open Camera captures 50.3 MP, in the same HAL state.
- The front-camera consequence of the global active-array raise (`FIND-4.5-01`): whether `hal1`, `hal8` and `hal9` advertising `activeArray` larger than their own `pixelArray` is tolerable in a distributed patch, and what the disposition is.
- Open Camera at full resolution, with the result measured numerically against the documented 50.3 MP.
- The AGC path, per the configuration `Faz 3.9`, `Faz 3.10` and `Faz 3.11` establish as the Phase 3 outcome — a pinned 12.58 MP photo size that survives the disturbance set — and not the success-or-fallback branch `Faz 3.6` gated for the retired objective.
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

`docs/regression-v2.1.md` from Faz 2.3 provides the ten-mode reference, and the Faz 2.2 baseline snapshot provides the device state reference. `docs/consumer-survey.md` from Faz 3.4 provides the consumer reference taken after the pixel array change and before the later experimental stack. `docs/agc-12mp-configuration.md` from `Faz3.11` provides the AGC reference — the expected pin, the expected configured stream, and the two black-fraction reference numbers — so this sub-plan measures AGC against a written expectation rather than re-deriving one.

Project-Comprehension `CQ-07` remains open at Phase 4's start: "What is the smallest correct HAL patch? Answer criterion: A patch adding RAW only at full resolution, with duration rows." **Its first half is retired by `DEC-14` and cannot be met:** `IMPL-49` measured that a patch adding RAW only at full resolution stops AGC from launching. `F4.4-09` must therefore record that half of the criterion as superseded and answer the question against the artifact that actually ships — the smallest patch that is *correct*, where correct now includes AGC launching — rather than report a failure against a condition the project deliberately abandoned. Amending `CQ-07`'s own wording belongs to `Project-Comprehension.md` and is not done here.

## 7. Planned Work Breakdown

- F4.4-01 — Measure the stream configuration surface
  - Description: Extract the RAW format rows and the matching duration rows for camera 3, confirm full resolution is present, and **record the entries at other resolutions as the shipped surface rather than as spurious** — section 4 and section 8 both establish that their removal is the retired narrowing, and `IMPL-49` measured it as preventing AGC from launching. *(Planning run 10: this item's "nothing spurious elsewhere" clause was the fifth instance of the `AUDIT-FIX-17` defect class and the one the run-9 repair did not enumerate; it contradicted this sub-plan's own sections 4, 8 and 13.)*
  - Output: A stream configuration verdict with the extracted rows.
- F4.4-02 — Measure the array entry count
  - Description: Report the count as a number **with its camera id and its metric named** — the `streamcfg` int32 element count for a stated `camera.hal<id>` — and compare it against a baseline read from a bracketed snapshot in the same state. Autopsy requires a measured number rather than a qualitative claim; `AUDIT-FIX-09` requires that the number be attributable. Do not quote 508 as a baseline, and note that `scripts/smoke.sh` sorts by id, so hal0 is the first line and is not hal3. **Under `DEC-14` there is no reduction target to pass:** report the delta from the baseline and state plainly that the shipped surface is broader than the project once intended, which is a distribution fact `QAS-04` requires be visible rather than a failure.
  - Output: A numeric array count per camera id with its delta from a freshly read baseline, and an explicit statement that no reduction target applies.
- F4.4-02b — Dispose of the global active-array raise (`FIND-4.5-01`)
  - Description: Measure `activeArray` and `pixelArray` for **every** camera id under the consolidated patch, not only the wide camera, and identify each id where `activeArray` now exceeds its own `pixelArray`. Then establish whether anything consumes the front cameras' active array at full extent — the stock camera's front path, the front video profiles, and any application in the Faz 3.4 consumer set that uses a front camera — and state a disposition: tolerable as-is, or requiring the raise to be scoped to the wide sensor. A scoping requirement is a **decision raised to the user with the evidence attached**, not a repair made here, per this sub-plan's out-of-scope rule — scoping the raise to one sensor is a fresh write-site question of the kind `Faz4.5` was created to hold, and it would need its own owner.
  - Output: A per-camera-id array consistency table, a front-camera behavioural verdict, and a stated disposition for `FIND-4.5-01`.
- F4.4-03 — Validate the third-party consumer
  - Description: Capture with Open Camera at full resolution and measure the result numerically against the documented 50.3 MP.
  - Output: An Open Camera verdict with a measured resolution.
- F4.4-04 — Validate the AGC path
  - Description: Confirm AGC behaves as the **amended** Phase 3 outcome established: it launches, and it captures a measured-clean 12.58 MP image with the photo-size pin in the state `Faz 3.9`'s bracket and `Faz 3.10`'s stickiness matrix recorded, read from `Faz 3.11`'s configuration record. `Faz 3.6`'s success-or-fallback branch gated the **retired** 50 MP objective and is not the expectation here.
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

- RAW10 is present at 8192x6144 with matching rows in both duration tables. `RAW_SENSOR` (format 32) is **not** required and its absence is not a failure: it is never emitted and has no additive route (`Faz 4.2` section 4, `IMPL-50`).
- The full emitted RAW entry set is recorded as it stands, per camera id. **No criterion requires it to be narrower.** Entries at resolutions other than full resolution are the shipped surface under `DEC-14`; `IMPL-49` measured their removal as preventing AGC from launching, 3/3 at two independent bisection stages — so a result reporting them is a pass, and a result that has removed them is a regression to route back to `Faz 4.3`.
- The array entry count is reported as a number **carrying its camera id and its metric**, with its delta from a baseline read from a bracketed snapshot rather than from a quoted figure. No unqualified "508" appears in the result, and no substitute reduction target is invented for the retired one.
- **AGC launches and captures a measured-clean 12.58 MP image against the consolidated artifact, and Open Camera captures 50.3 MP in the same HAL state.** This is the criterion `IMPL-49` showed a count-only validation silently violates, and it is the one that decides whether the artifact is distributable.
- Every camera id has an `activeArray` and `pixelArray` reading under the consolidated patch, every id where the first exceeds the second is named, and `FIND-4.5-01` carries a stated disposition backed by a front-camera behavioural check rather than by assumption.
- Open Camera's full-resolution result is measured numerically and matches the documented value.
- The AGC path matches the expectation the amended Phase 3 outcome established — `Faz 3.11`'s configuration record — and not `Faz 3.6`'s retired success-or-fallback branch.
- The stock camera opens, previews, and completes a shutter; video records and plays at both profiles.
- All ten modes have a verdict compared against the Faz 2.3 regression record, with no regression.
- Both exclusion-boundary transitions behave per invariant 4.
- Reboot persistence for the consolidated HAL state is confirmed.
- `CQ-07` is resolved, or what remains unsatisfied is recorded explicitly.
- Any failure is routed to the owning sub-phase rather than repaired here.

## 9. Validation and Test Approach

This is the phase's validation sub-phase, so its approach is the validation. The design principle is comparison against recorded references rather than fresh judgment.

- `VAL-SMOKE` (from Faz 2.1) — the state reporter, used per mode and around each check.
- `VAL-ARRAYCOUNT` (defined here, since `Faz4.1` is `superseded`) — the numeric array count, reported per camera id with the `streamcfg` int32 metric named and with its delta from a bracketed baseline. It is a reported fact, not a pass/fail metric.
- `VAL-AGC` (from Faz 3.9 / Faz 3.10) — the sub-phase's **headline** check: AGC's launch verdict plus one capture measured by the `IMPL-40` method, taken in the same HAL state as the Open Camera capture.
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

Depends on `Faz 3.9`, `Faz 3.10` and `Faz 3.11` for the AGC expectation: the bracketed coexistence result, the pin's measured survival across the four disturbance axes, and the operator-facing configuration record that states what a correct AGC reading looks like. **The former dependency on `Faz 3.6` is removed by `DEC-14`** — that gate decided between success and fallback for the retired 50 MP objective, and neither branch describes the configuration this sub-phase now validates.

Blocks Phase 9's release work, which should not package a patch that has not passed this validation. Does not block Phase 5, and the priority question that once qualified this sentence is closed: `DEC-03` was answered on 2026-08-31 and Phase 5 closed with `IMPL-17`.

Required human actions: every consumer check, every camera open, every video recording, and two reboots. This is a user-intensive sub-phase comparable to Faz 2.3.

Required infrastructure: the device, the Open Camera build, the AGC build, and storage for recordings.

Required approvals: running a patched HAL through the full application set.

Fresh session token and context risk: medium. High verdict volume, low per-verdict cost. The mitigation is the same as Faz 2.3's — write verdicts into the record as they are produced.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: Open Camera is checked without measuring and a silent resolution drop goes unnoticed. Impact: the exact failure `halpatch.sh` documents as happening without the patch, now happening with a defective one. Mitigation: F4.4-03 and the acceptance criteria both require a numeric measurement.
- Risk: the array count is reported qualitatively rather than as an attributable number. Impact: Autopsy's explicit requirement is unmet and the shipped surface's actual size is not on record. Mitigation: F4.4-02 requires a number with its camera id, its metric, and its delta from a bracketed baseline.
- Risk (`IMPL-49`): the artifact passes every count and table check and AGC does not start. Impact: the exact failure the retired narrowing goal produced, shipped this time. Mitigation: `VAL-AGC` is the headline criterion, not a supplementary one, and section 8 makes a clean 12.58 MP capture a condition of distributability.
- Risk (`AUDIT-FIX-09`): the count is compared against the unqualified 508 figure. Impact: a comparison against the wrong camera — 508 is hal3 in fullres, hal0's figure is 456, and smoke prints hal0 first — producing a confident wrong verdict on the sub-plan's headline metric. Mitigation: section 1's amendment forbids quoting the figure, F4.4-02 requires the camera id and the metric alongside the number, and the baseline is read from a bracketed snapshot in the comparison state.
- Risk (`FIND-4.5-01`): the front cameras' inconsistent array pair is checked only by reading metadata, and a consumer that actually breaks on it is not exercised. Impact: a patch ships that is internally inconsistent on three camera ids nobody tested, on other people's devices. Mitigation: F4.4-02b requires a behavioural check on the front path, not only a metadata table, and F4.4-05's stock-camera and video checks are run on the front camera as well as the rear.
- Risk (invariant 4): Faz 4.3's structural change broke the exclusion enforcement and it is not noticed because individual modes work. Impact: a state where both layers are active, which produced corrupted output historically. Mitigation: F4.4-07 exercises both transitions as a distinct work item.
- Risk: reboot persistence fails because `post-fs-data.sh` was not updated for a renamed HAL state. Impact: 50 MP works interactively and vanishes after every reboot. Mitigation: F4.4-08 tests the boot path specifically, which is separate from the interactive path.
- Risk: a failure is repaired inline because it looks small. Impact: the validation record describes a configuration that no longer exists, and the repair skips its owning sub-phase's checks. Mitigation: the out-of-scope section and the acceptance criteria both require routing.
- Risk: the ten-mode pass is compressed because it repeats Faz 2.3. Impact: a HAL-layer regression affecting sensor-layer modes goes undetected, which is precisely what a shared control flow makes possible. Mitigation: F4.4-06 compares against the recorded reference, making it a diff rather than a repetition.
- Risk: `CQ-07` is answered affirmatively without the duration rows being verified. Impact: the answer criterion is only half met. Mitigation: the criterion in Project-Comprehension names both conditions, and `VAL-TABLES` checks the second.

## 12. Desired End State

The consolidated patch is validated as a shippable artifact: the stream configuration surface carries the intended entries with matching duration rows, the array count is on record as an attributable measured number with its delta from a bracketed baseline **and no target attached**, AGC and Open Camera coexist in one HAL state at 12.58 MP and 50.3 MP, every consumer the project has documented behaves as expected, all ten modes work, the exclusion rule holds in both directions, and the state survives a reboot. `CQ-07` is answered by the artifact.

`FIND-4.5-01` is disposed of rather than carried into a release: every camera id's `activeArray` and `pixelArray` are recorded, the ids where the pair is inconsistent are named, and the front-camera behaviour under that inconsistency is measured rather than assumed harmless.

The evidence an implementer should produce is the extracted stream and duration rows, the numeric array count with its camera id and metric, the per-camera-id array consistency table, the measured Open Camera resolution, the ten-mode comparison, the two transition verdicts, and the persistence verdict.

The ledger summary Step 4 should append records: the measured array count per camera id with its delta and no target, the coexistence verdict, the consumer results, the ten-mode outcome, the invariants exercised, the `CQ-07` resolution, and any routed finding.

## 13. Next Sub-Phase Transition Criteria

- The stream configuration surface matches the intent: RAW10 at 8192x6144 with matching rows in both duration tables, and the broad emission recorded rather than treated as spurious.
- The array count is a number carrying its camera id and its metric, with its delta from a bracketed baseline and no target claimed against it.
- AGC launches and captures a measured-clean 12.58 MP image against the consolidated artifact, in the same HAL state in which Open Camera captures 50.3 MP.
- `FIND-4.5-01` has a stated disposition backed by a per-camera-id table and a front-camera behavioural check, and any scoping requirement is raised to the user rather than repaired here.
- Open Camera's resolution is measured and correct.
- All ten modes pass against the regression reference.
- Both exclusion transitions and reboot persistence are confirmed.
- `CQ-07` is resolved or its remaining gap is recorded.
- No unrouted failure remains, and Phase 9 has a validated artifact to package.
