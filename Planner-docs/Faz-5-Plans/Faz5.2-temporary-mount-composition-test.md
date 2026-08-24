# Faz 5.2 — Temporary Mount Composition Test

## 1. Context

Main-Planing Phase 5's first vibecoding slice ends with the step this sub-phase performs: "test in a temporary bind-mount before committing it to `blobs/`."

Its acceptance signals define the two acceptable outcomes: "A 50 MP frame with LN active, compared against 50 MP alone for noise and detail; or a clean revert with the failure mode documented." Its desired end state says the same: "Either 50 MP + LN2/LN4 work together, or a written negative result explaining why not."

That symmetry is unusual in this roadmap and deliberate. Most sub-phases have a success condition and a failure to be diagnosed. Here a documented negative result is a complete outcome, because `OQ-04` — "Is the 10-bit/12-bit mismatch the *only* obstacle to 50 MP + LN composition?" — is genuinely open and either answer closes it.

Project-Comprehension `H-04` states the probe: "Generate a 12-bit mode-0 blob, verify with `verify_ln.py`, mount temporarily, switch to `ln2`, capture. Reverts cleanly if it fails." The revertibility is what makes the experiment affordable.

The temporary mount is the mechanism that keeps it single-purpose. Mounting without placing the blob in `blobs/` means the module's normal dispatch never selects it, and removing the mount returns the device to a known state without touching any shipped artifact.

## 2. Goal

Determine on the device whether a 12-bit mode 0 permits 50 MP and the LN modes to operate together, using a temporary mount that leaves no trace when removed, and record either the working composition or the specific failure mode.

## 3. Description

The problem is that the exclusion rule was introduced in response to an observed corruption, and the recorded cause — a bit-depth mismatch — has never been tested as the sole cause. Autopsy section 11 states the gap: "no measurement in the repository confirms that this is the *only* obstacle."

It belongs after the blob is generated and verified because a mount test of an unverified blob would confound container defects with configuration effects.

The vibecoding slice strategy: mount, verify the sensor layer reports the expected state, switch to an LN mode with 50 MP engaged, and capture. The fastest validation signal comes before the capture — whether the camera opens at all with both layers active, since the historical symptom was corrupted output rather than a failure to open. A camera that opens is not yet a success, but a camera that does not open ends the test cheaply.

What should not be over-planned: image quality methodology. The comparison Main-Planing asks for is 50 MP with LN against 50 MP alone, for noise and detail. That is a two-image comparison, and the project already has a precedent for this kind of judgment in the recorded `dcgB` result.

The exclusion rule itself is the operational obstacle. `setmode.sh` enforces it in control flow: selecting `50mp` forces the sensor layer to stock. Testing composition therefore requires bypassing the module's own dispatch, which is exactly what a manual temporary mount does. This must be done without editing `setmode.sh`, because editing the dispatch would make the experiment a change to the shipped module rather than a test alongside it. Faz 5.3 decides whether the dispatch changes.

There is a hazard specific to this sub-phase. Project-Ontology invariant 3 records that the camera restart order runs client before HAL and that violating it blackens preview in every mode, recoverable only by reboot. A manual mount sequence performed outside `setmode.sh` does not automatically get that ordering, and the operator must reproduce it deliberately.

## 4. Scope

- A temporary bind mount of the candidate blob over the sensor driver path, performed outside the module's dispatch.
- Correct camera stack restart ordering around the mount, reproducing what `setmode.sh` implements.
- Verification that the sensor layer reports the candidate blob's checksum and that the HAL layer is in its 50 MP state.
- A camera open check with both layers active.
- A capture at 50 MP with an LN mode active, if the camera opens.
- A comparison capture at 50 MP alone, for the noise and detail assessment.
- Removal of the temporary mount and confirmation that the device returns to its pre-test state.
- Resolution of `OQ-04` and `H-04` with either outcome.
- If the composition fails, classification of the failure mode against the historical corruption symptom.

## 5. Out of Scope

- Editing `setmode.sh`, `post-fs-data.sh`, or any dispatch logic. Faz 5.3 owns that decision.
- Placing the candidate blob in `blobs/`. That depends on this sub-phase's outcome and is Faz 5.3's call.
- Testing bit-depth changes for modes other than mode 0.
- Any HAL-layer change. Phase 4's artifact is fixed.
- A full ten-mode regression. Faz 5.3 runs that if the composition is adopted.
- Extended image quality analysis beyond the noise and detail comparison Main-Planing names.
- Diagnosing a failure beyond classifying its mode. A deeper investigation would be new work with its own decision.

## 6. Current Repository Evidence

`ishtar-cam-modes/setmode.sh` was read in this run and documents the exclusion in its header: `50mp` opens the HAL layer and forces the sensor layer to stock, while other modes patch the sensor layer and leave the HAL at stock, and the two therefore exclude each other because mode 0 remains 10-bit while DCG pulls the global white level to 12-bit, producing corrupted 50 MP output.

The same file records the mount mechanism the manual test must reproduce: `MODDIR=/data/adb/modules/ishtar_cam_modes`, `BIN=com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, `TGT=/odm/lib64/camera/$BIN`, `ACT=$MODDIR/active/$BIN`, and a `mounted()` function testing the process 1 mount info for the target path. `EXPECT_SIZE=1062250` is the guard.

`restart_camera()` implements the ordering invariant with the reasoning preserved in comments: stop `cameraserver` and wait, stop both providers and wait, force-stop the camera applications, apply the HAL layer only in that window, then start the providers and `cameraserver`. The comments state explicitly that force-stopping applications before stopping `cameraserver` was the earlier wrong order and that killing the provider while a stream is live leaks kernel driver allocations.

`ishtar-cam-modes/post-fs-data.sh` reapplies the stored mode at boot and maps unrecognized values to stock across all three variables. A reboot during this test therefore returns the device to the module's normal dispatch, which is a useful safety property: the temporary mount does not survive a reboot.

Project-Comprehension `EV-21` records the `dcgB` measurement — roughly 25% less noise and about double the detail versus stock — with confidence `probable`, evidenced by on-device comparison. This is the precedent for how the project judges image quality, and the comparison in this sub-phase should be of the same kind.

Project-Ontology invariant 4 records the exclusion as standing until `Kararlar #4` is "executed and proven". This sub-phase is the proving step.

`ishtar-cam-modes/blobs/` currently holds nine variants and the candidate is deliberately not among them.

## 7. Planned Work Breakdown

- F5.2-01 — Establish the pre-test state
  - Description: Snapshot with the Faz 2.1 script, confirm the preference precondition, and record the current mode and both layer checksums.
  - Output: A pre-test snapshot.
- F5.2-02 — Write the manual mount and unmount procedure
  - Description: Write the sequence including the correct restart ordering, before executing anything. The ordering is an invariant with a documented recovery cost, so it should be written and reviewed rather than improvised.
  - Output: A reviewed procedure covering mount, restart, and unmount.
- F5.2-03 — Engage the 50 MP HAL state
  - Description: Set `50mp` through the module's normal path so the HAL layer is in its intended state, before the sensor layer is manipulated manually.
  - Output: A confirmed HAL state.
- F5.2-04 — Mount the candidate and restart correctly
  - Description: Bind mount the candidate over the sensor driver path following the written procedure, with the restart ordering reproduced exactly.
  - Output: A confirmed mount with the candidate's checksum reported at the target path.
- F5.2-05 — Check whether the camera opens
  - Description: Open the camera with both layers active. This is the cheap decisive check — a camera that does not open ends the test without a capture.
  - Output: A camera open verdict.
- F5.2-06 — Capture with LN active at 50 MP
  - Description: If the camera opens, capture at full resolution with an LN mode's sensor configuration active.
  - Output: A capture with its dimensions and a visual assessment.
- F5.2-07 — Capture the comparison frame
  - Description: Capture at 50 MP alone under comparable conditions, for the noise and detail comparison.
  - Output: A comparison capture.
- F5.2-08 — Unmount and confirm restoration
  - Description: Remove the temporary mount, restart correctly, and snapshot. The post-test snapshot must match the pre-test snapshot.
  - Output: A restoration verdict with matching snapshots.
- F5.2-09 — Record the outcome
  - Description: Resolve `OQ-04` and `H-04` with either the working composition or the classified failure mode. A negative result is recorded with the same care as a positive one.
  - Output: Updated continuity artifacts and a written outcome.

## 8. Acceptance Criteria

- The mount and unmount procedure is written and reviewed before execution, including the restart ordering.
- The pre-test snapshot confirms the preference precondition and records both layer states.
- The candidate's checksum is confirmed at the sensor driver target path while mounted.
- The camera open verdict is recorded regardless of outcome.
- If the camera opens, both captures exist and the noise and detail comparison is recorded.
- If the camera does not open, or output is corrupted, the failure mode is classified against the historical corruption symptom.
- The temporary mount is removed and the post-test snapshot matches the pre-test snapshot.
- `OQ-04` in Project-Ontology and `H-04` in Project-Comprehension are resolved, in either direction.
- The candidate blob was not placed in `blobs/` and no dispatch logic was edited.
- No black preview occurred, or if it did, the restart ordering is examined as the first suspect.

## 9. Validation and Test Approach

Validation is live with a manual capture component. The distinguishing property is that both outcomes are valid results, so the validation design must record a failure as precisely as a success.

- `VAL-SMOKE` (from Faz 2.1) — the bracket, before and after, with the post-test snapshot required to match the pre-test one.
- `VAL-MOUNT` (proposed) — confirmation that the candidate's checksum is reported at the target path while mounted, and that the module's checksum is reported after unmounting.
- `VAL-MANUAL` (proposed) — the camera open, both captures, and the noise and detail comparison. The user's actions throughout.
- `VAL-REVERT` (from Faz 3.3) — the post-test snapshot matching the pre-test snapshot, demonstrating the experiment left no trace.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist.

Local versus live: entirely live. Security validation is not applicable, though the manual mount runs as root and the size guard the module enforces should be reproduced in the manual procedure rather than skipped.

Ontology validation covers invariants 3 and 4 — the restart ordering is exercised manually and the exclusion rule is deliberately bypassed under controlled conditions.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Pre-test and post-test bracket with restoration check. | VAL-SMOKE, VAL-REVERT |
| ishtar-cam-modes/setmode.sh | existing | Read-only reference for the mount mechanism and restart ordering the manual procedure reproduces. | VAL-MOUNT |
| docs/mode0-12bit-candidate.md | existing | The candidate blob's generation record and verification result. | VAL-MOUNT |
| Planner-docs/Project-Ontology.md | modified | Resolve `OQ-04` with the measured outcome. | VAL-MANUAL |
| Planner-docs/Project-Comprehension.md | modified | Resolve `H-04` and record the composition result. | VAL-MANUAL |

## 10. Dependencies and Sequencing

Depends on Faz 5.1 for a verified candidate blob, on Faz 2.1 for the bracket, and on Phase 4 for a stable HAL artifact.

Blocks Faz 5.3, which decides what to do with the result.

Required human actions: the captures and the visual comparison. The mount itself is a root command sequence that can be delegated, but the restart ordering makes it a sequence where an error costs a reboot, so it should be executed with the written procedure in hand.

Required infrastructure: the device with root, the module installed, and the candidate blob transferred to it.

Required approvals: the user's willingness to run their camera with a deliberately unsupported layer combination, which is the exact condition the exclusion rule exists to prevent. The revertibility of the temporary mount is what makes this reasonable.

Fresh session token and context risk: low. Two snapshots, a mount sequence, and two captures.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk (invariant 3): the manual restart sequence gets the ordering wrong. Impact: black preview in every mode including stock, recoverable only by reboot. Mitigation: F5.2-02 requires the procedure to be written and reviewed before execution, and the acceptance criteria name the ordering as the first suspect if a black preview occurs.
- Risk: the composition produces corrupted output, as the original observation recorded. Impact: none beyond the test, since this is one of the two anticipated outcomes. Mitigation: it is treated as a result rather than a failure, and F5.2-09 records it as the answer to `OQ-04`.
- Risk (`OQ-04` realized): the bit-depth change is insufficient and something else also blocks composition. Impact: the experiment does not deliver the capability. Mitigation: the failure mode classification distinguishes "corrupted as before" from a new symptom, and the distinction is what makes the negative result informative.
- Risk: the temporary mount is not removed and the device is left in an experimental state. Impact: the next measurement's baseline is wrong, and a reboot would restore the module's dispatch while a mounted candidate might not survive it — producing inconsistent behavior. Mitigation: `VAL-REVERT` requires matching snapshots, and the reboot behavior of `post-fs-data.sh` is a backstop rather than the plan.
- Risk: the manual mount skips the size guard the module enforces. Impact: a wrong-size file is mounted over a system path. Mitigation: the procedure reproduces the guard, and Faz 5.1 already confirmed the candidate's exact size.
- Risk: the comparison captures are taken under different conditions and the noise assessment is meaningless. Impact: an unusable quality verdict. Mitigation: F5.2-07 specifies comparable conditions, following the precedent of the recorded `dcgB` comparison.
- Risk: the candidate is placed in `blobs/` mid-test for convenience. Impact: the module's dispatch could select it, and the experiment stops being separable from the shipped artifact. Mitigation: the out-of-scope section and the acceptance criteria both forbid it.

## 12. Desired End State

The composition question is answered by measurement. Either 50 MP and LN operate together with a capture and a quality comparison to show for it, or the failure mode is classified and recorded. Either way the temporary mount is removed, the device matches its pre-test state, and `OQ-04` and `H-04` are resolved.

The evidence an implementer should produce is the written procedure, the pre-test and post-test snapshots, the mount checksum confirmation, the camera open verdict, and either the two captures with their comparison or the classified failure mode.

The ledger summary Step 4 should append records: the composition outcome, the failure mode if any, the `OQ-04` answer, and confirmation that the device was restored.

## 13. Next Sub-Phase Transition Criteria

- The camera open verdict is recorded.
- Either both captures exist with a comparison, or the failure mode is classified.
- The temporary mount is removed and the snapshots match.
- `OQ-04` and `H-04` are resolved in either direction.
- No dispatch logic was edited and the candidate remains outside `blobs/`.
- Faz 5.3 has a definite result to act on.
