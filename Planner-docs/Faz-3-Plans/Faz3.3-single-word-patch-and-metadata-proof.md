# Faz 3.3 — Single Word Patch and Metadata Proof

## 1. Context

Main-Planing Phase 3's first vibecoding slice ends with the confirmation step this sub-phase performs: "confirm with a single-word patch and a `dumpsys` read before attempting any capture."

Project-Comprehension `CQ-05` states the answer criterion that makes this the deciding sub-phase rather than Faz 3.2: "An address that, when patched, changes `dumpsys` output." A candidate identified by static analysis is a hypothesis. An address whose patch changes what the framework reports is a located write site. This sub-phase converts one into the other.

`H-02` is the hypothesis under test: "Raising `pixelArraySize` to 8192x6144 satisfies libgcam without breaking other consumers", confidence `tentative`, with the probe stated as "After H-01: patch one word, read `dumpsys` for tag `f0006`, then open the stock camera app before touching AGC."

That last clause matters and shapes the sub-phase boundary. This sub-plan proves the metadata changed and that the camera stack still functions at a basic level. The broader consumer question — `OQ-03`, "Can `pixelArraySize` be raised without breaking other consumers?" — is Faz 3.4's subject, and the AGC capture is Faz 3.5's. Three separate sub-phases for what could be one session, because Autopsy requires "a before/after state snapshot around every single-word patch" and because this project's history shows what happens when several variables move together.

Autopsy section 12 states that requirement directly under Phase 3: "Require a before/after state snapshot around every single-word patch."

## 2. Goal

Prove or disprove that the top candidate address controls the reported `android.sensor.info.pixelArraySize`, by applying the smallest possible patch and measuring the framework's reported metadata before and after.

## 3. Description

The problem is that static analysis can identify a plausible write site and be wrong, and the cost of being wrong compounds if the error is discovered after a capture attempt rather than before. A capture failure has many possible causes; a `dumpsys` value that did not change has exactly one.

It belongs immediately after the search because the confirmation is cheap relative to the search, and because a negative result here sends work back to Faz 3.2's next candidate rather than forward into more expensive territory.

The vibecoding slice strategy is the tightest in the roadmap: one address, one word, one measurement. Nothing else changes. The fastest validation signal is the reported tag value in the camera service dump — available within one camera restart of the patch being applied.

What should not be over-planned: the patch's permanent form. This is an experiment. It uses the existing patch-table mechanism because that mechanism already provides checksum-guarded application and reversal, but the entry is experimental and its consolidation into a shipped table is Faz 4.3's decision.

The reversal path is a first-class part of this sub-phase rather than an afterthought. `halpatch.sh` was read in this run and its design makes reversal deterministic: writes target a module-private copy under `active_hal/`, `hal_state` classifies the copy by checksum, and `hal_set` re-seeds from the device's stock binary when the state is unrecognized. An experimental entry changes the resulting checksum, which means the module will classify the patched copy as `unknown` and re-seed it — a behavior the implementer must understand before applying the patch, because it determines how the experiment is held in place and how it is undone.

If the candidate is confirmed, the value moved is one half of the libgcam invariant. Project-Ontology invariant 6 records that the requirement is for `frame_raw_max` to equal the active array size or the pixel array size, and that "Both sides must move together." Confirming that `pixelArraySize` reports 8192x6144 while raw is already advertised at 8192x6144 is the state in which the invariant is satisfied — but satisfying it in the dump is not the same as libgcam accepting it, and that acceptance is Faz 3.5's evidence.

## 4. Scope

- Application of a single-word patch at the top-ranked candidate address from Faz 3.2.
- A before snapshot and an after snapshot using the Faz 2.1 script, with the preference precondition from Faz 3.1 verified in both.
- Extraction of the reported `android.sensor.info.pixelArraySize` value for camera 3 before and after.
- Extraction of `android.sensor.info.activeArraySize` and `preCorrectionActiveArraySize` in the same reads, to confirm the patch moved the intended array and not an adjacent one.
- A basic camera-stack health check: the stock camera application opens with a live preview.
- Deterministic reversal to the pre-patch state, demonstrated rather than assumed.
- If the top candidate fails, an ordered retry against the next ranked candidate, within the Faz 3.1 budget.
- Recording of the confirmed address into Project-Ontology section 6 and resolution of `CQ-05`.

## 5. Out of Scope

- Any AGC interaction, capture attempt, or Gcam initialization check. Faz 3.5 owns those.
- A full consumer compatibility survey, which is Faz 3.4.
- Narrowing the RAW emission or adding duration rows, which are Phase 4.
- Any change to the sensor layer or to the ten modes.
- Consolidating the experimental entry into a shipped patch table.
- Photograph capture or image inspection of any kind.
- Investigating why a candidate failed beyond what is needed to move to the next one; deeper analysis returns to Faz 3.2.

## 6. Current Repository Evidence

`ishtar-cam-modes/halpatch.sh` was read in full in this run and provides the mechanism this sub-phase uses. `hal_write` applies entries from a table with `printf '%b' "$e" | dd of="$HAL_ACT" bs=4 seek="$idx" count=1 conv=notrunc`, writing to `$MODDIR/active_hal/camera.qcom.so` rather than to the live target. `hal_state` returns `fullres` for `fe0245a4720fb07b01d96deef47f5569`, `stock` for `c3fa63a86ee3ecaf9fbf02005d35f6b5`, and `unknown` for anything else. `hal_set` re-seeds from the device's stock binary when the state is `unknown` or `none`, and verifies the resulting checksum after writing.

The consequence for this sub-phase is specific: an experimental patch produces a checksum matching neither constant, so the module's own machinery will treat the result as damaged and rebuild it. The implementer must therefore either extend the recognized checksum set for the duration of the experiment or hold the patched copy outside the module's automatic reconciliation. Which approach is chosen should be recorded, because it determines the reversal procedure.

`setmode.sh` was read in this run and shows the constraint on when the HAL may be written. The comment at the HAL write site states that `camera.qcom.so` is memory-mapped by running processes and that changing its contents while services are up causes a crash; the write happens inside `restart_camera()` after all services are stopped and immediately before they start. Any manual patch application must respect the same window.

`agc-50mp-yama/hal-raw50-deneme.patch` records the state that makes this experiment meaningful: both arrays currently report `4096x3072` while `frame_raw_max` reports `8192x6144`. It also demonstrates the table format for a chained experimental patch, recording `temel: fullres md5 fe0245a4720fb07b01d96deef47f5569` and `sonuc: md5 8d0915ce520fadaf092d31ed675aa98a`.

Project-Ontology section 6 records the three tag identifiers this sub-phase reads: `f0006` for `pixelArraySize`, `f0000` for `activeArraySize`, and `f000a` for `preCorrectionActiveArraySize`.

`ishtar-cam-modes/blobs/hal-fullres.patch` records the four-byte index convention with the note that the index is the byte offset divided by four, which is how a located address is converted into a patch table entry.

## 7. Planned Work Breakdown

- F3.3-01 — Convert the candidate address into a patch entry
  - Description: Compute the four-byte index from the located byte offset, determine the stock word, and determine the replacement word that produces 8192x6144. Verify the address is four-byte aligned, per the constraint the format contract records.
  - Output: A one-entry experimental patch table with base and result checksums.
- F3.3-02 — Decide and record the experiment-holding approach
  - Description: Choose how the patched copy is held against the module's automatic reconciliation, and record the choice with its reversal implications.
  - Output: A holding and reversal procedure.
- F3.3-03 — Capture the before state
  - Description: Run the Faz 2.1 script, confirm the preference precondition, and extract the three array tag values for camera 3.
  - Output: A stored before snapshot with the three tag values.
- F3.3-04 — Apply the patch in the safe window
  - Description: Apply the single-word change with camera services stopped, following the ordering that `setmode.sh` documents, and verify the resulting checksum matches the table's recorded result.
  - Output: A confirmed patch application.
- F3.3-05 — Capture the after state and compare
  - Description: Restart the camera stack, run the script, and extract the same three tag values. Compare against the before state.
  - Output: A stored after snapshot and a three-value comparison.
- F3.3-06 — Verify basic camera health
  - Description: Open the stock camera application and confirm a live preview. This is the minimum check that the patch did not break the stack, and it is the user's action.
  - Output: A camera health verdict.
- F3.3-07 — Demonstrate reversal
  - Description: Revert to the pre-patch state and confirm with a third snapshot that it matches the before state. Reversal is demonstrated, not assumed, because every later sub-phase depends on being able to return here.
  - Output: A third snapshot matching the first.
- F3.3-08 — Record the outcome
  - Description: If confirmed, record the address in Project-Ontology section 6 as the located write site and resolve `CQ-05` and `H-02`. If not, record the candidate as eliminated with what the measurement showed, and proceed to the next ranked candidate within budget.
  - Output: Updated continuity artifacts and a candidate verdict.

## 8. Acceptance Criteria

- Exactly one word is changed per attempt; no attempt bundles two changes.
- Before and after snapshots exist for every attempt, both confirming the preference precondition.
- The three array tag values are extracted in both snapshots, so a change to the wrong array is visible rather than invisible.
- A confirmed candidate is one where `f0006` reports 8192x6144 after the patch and reported 4096x3072 before, with `f0000` and `f000a` unchanged.
- The stock camera application opens with a live preview after the patch, or the failure is recorded as part of the candidate's verdict.
- Reversal is demonstrated by a third snapshot matching the first, not asserted.
- The patch application verified its resulting checksum against the table's recorded value, per the format's own guarantee.
- If confirmed, the address is recorded in Project-Ontology section 6 and `CQ-05` and `H-02` are updated in the same session.
- If all ranked candidates are eliminated, the result is handed to Faz 3.6 rather than expanded into further ad hoc searching.
- Attempts consumed are counted against the Faz 3.1 budget.

## 9. Validation and Test Approach

Validation is live and comparative. The measurement is the point of the sub-phase, and its design is what makes the result attributable.

- `VAL-SMOKE` (from Faz 2.1) — the bracket, run before, after, and after reversal. Three runs per attempt.
- `VAL-METADATA` (proposed) — extraction of the three array tag values for camera 3 from the camera service dump, in each of the three runs. This is the primary evidence.
- `VAL-CHECKSUM` (proposed) — verification that the patched copy's checksum matches the experimental table's recorded result, which proves the write landed where intended.
- `VAL-MANUAL` (proposed) — the stock camera open with live preview, the user's action.
- `VAL-REVERT` (proposed) — the third snapshot matching the first, demonstrating deterministic reversal.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist, applied to every attempt.

Local versus live: entirely live. Security validation is not applicable. Ontology validation applies to the recording of a confirmed address and to keeping the three array tags distinct.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | The three-run bracket per attempt. | VAL-SMOKE, VAL-METADATA, VAL-REVERT |
| ishtar-cam-modes/halpatch.sh | existing | Read-only context: the write window, checksum classification, and re-seed behavior. | VAL-CHECKSUM |
| agc-50mp-yama/hal-pixelarray-deneme.patch | proposed | The single-entry experimental patch table for the candidate under test. | VAL-CHECKSUM |
| Planner-docs/Project-Ontology.md | modified | Record the confirmed write site, or the eliminated candidates. | VAL-METADATA |
| Planner-docs/Project-Comprehension.md | modified | Resolve `CQ-05` and update `H-02` in the same session. | VAL-METADATA |

## 10. Dependencies and Sequencing

Depends on Faz 3.2 for the ranked candidate list, on Faz 3.1 for the budget and the per-measurement checklist, on Faz 2.1 for the bracket, and on Faz 2.2 for the baseline the snapshots are compared against.

Blocks Faz 3.4 and Faz 3.5. Neither can proceed without a confirmed write site, and attempting the AGC capture against an unconfirmed patch is exactly the multi-variable situation this phase is structured to avoid.

Feeds Faz 3.6 with either a confirmation or an elimination result.

Required human actions: the camera health check needs the user's eyes, and applying a HAL patch on a device the user depends on is their decision to permit. The reversal demonstration reduces that cost, which is part of why it is mandatory.

Required infrastructure: the device with root, and the module installed so `active_hal/` and the patch machinery are present.

Fresh session token and context risk: medium. Each attempt is three snapshots and a small diff. The risk grows if several candidates are attempted in one session, which is where the Faz 3.1 budget applies.

Subagents are not recommended. This is a stateful device sequence with a patch applied to a system binary.

## 11. Risks and Mitigations

- Risk: the patch is applied while camera services are running. Impact: a crash, per the constraint `setmode.sh` documents about the binary being memory-mapped. Mitigation: F3.3-04 requires the safe window explicitly, following the ordering the module already implements.
- Risk: the module's reconciliation re-seeds the patched copy mid-experiment and the measurement reflects an unpatched binary. Impact: a false negative that eliminates a correct candidate. Mitigation: F3.3-02 decides and records the holding approach before the first attempt, and `VAL-CHECKSUM` confirms what is actually in place at measurement time.
- Risk: the patch changes `f0000` or `f000a` instead of `f0006`. Impact: the active array is raised, which Faz 4 evidence shows breaks AGC — the wrong side of the invariant. Mitigation: all three tags are extracted in every snapshot, so the wrong-array case is immediately visible.
- Risk (`R3`): a wrong offset corrupts the HAL and the camera stops working. Impact: no camera until recovery. Mitigation: writes target the module-private copy rather than the live binary, the table records base and result checksums, and F3.3-07 demonstrates reversal before the experiment is considered complete.
- Risk: a candidate is eliminated on a measurement taken with a preference set. Impact: the `EV-13` misattribution pattern repeats, this time eliminating a correct answer. Mitigation: `VAL-PRECOND` applies to every attempt and the before snapshot confirms the preference state.
- Risk: several candidates are attempted in one session and the results blur. Impact: an ambiguous outcome that has to be repeated. Mitigation: the acceptance criteria require a complete three-run bracket per attempt, which makes each attempt self-contained.
- Risk: the metadata changes but libgcam still rejects it. Impact: the confirmation succeeds while the goal does not. Mitigation: this is anticipated rather than mitigated — it is precisely why Faz 3.5 is a separate sub-phase, and a confirmed write site remains valuable even if acceptance fails.
- Risk: reversal is skipped because the patch appears to work. Impact: the device is left in an experimental state and the next measurement's baseline is wrong. Mitigation: `VAL-REVERT` is an acceptance criterion.

## 12. Desired End State

The write site question is resolved by measurement. Either an address is confirmed — patching it moves `f0006` from 4096x3072 to 8192x6144 while leaving `f0000` and `f000a` unchanged, with the camera stack still functional and reversal demonstrated — or every ranked candidate is eliminated with its measurement recorded and the result handed to the decision gate.

The evidence an implementer should produce is, per attempt, three snapshots with the three tag values in each, the checksum verification, the camera health verdict, and the reversal match.

The ledger summary Step 4 should append records: attempts consumed against budget, the confirmed address or the elimination list, the `CQ-05` and `H-02` outcomes, and confirmation that the device was returned to its pre-patch state.

## 13. Next Sub-Phase Transition Criteria

- A candidate is confirmed by measurement, or all ranked candidates are eliminated and Faz 3.6 is invoked.
- Every attempt has a complete three-run bracket with all three array tags extracted.
- Reversal has been demonstrated at least once, with a snapshot matching the pre-patch state.
- A confirmed address is recorded in the ontology and `CQ-05` reflects it.
- The device is in a known state, patched or reverted, and which one is recorded.
- No AGC interaction has occurred; Faz 3.5 has not started.
