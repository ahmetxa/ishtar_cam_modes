# Faz 2.3 — Ten-Mode Regression Pass

## 1. Context

Main-Planing Phase 2 describes the work after the flash as "a full regression pass across all ten modes: tile synchronization, launcher icon rendering (the v2.1 fix), mode persistence across reboot, camera-stack restart without black preview, and 1080p60/4K60 video." Its acceptance signals are "Every mode switches and the camera opens; video unaffected; reboot persistence confirmed; a written regression record exists."

Autopsy section 8 converts the manual half into a named gate: "Gate 3 (device, manual): camera opens in the selected mode; preview is not black; shutter completes; 1080p60 and 4K60 record. This requires the user and should be an explicit checklist, not an assumption."

Two of the checks are not arbitrary. Project-Ontology invariant 5 states that 1080p60 and 4K60 must remain functional in every mode and calls it "a standing acceptance criterion, user-validated". Invariant 3 states that the camera restart order runs client before HAL, and that violating it "leaks CSIPHY/CSID allocations and blackens preview in every mode" — recoverable only by reboot. The black-preview check is therefore a direct test of a known, previously-broken invariant rather than a generic smoke test.

Project-Comprehension section 6 identifies where a regression is most likely: "Tiles and launcher visibility — touched in v1.4, v1.5, v1.7, v2.1. The most-revisited area, and every revisit was a read-path or synchronization issue. This is where the next UI regression is most likely."

## 2. Goal

Establish, with recorded evidence rather than recollection, that all ten modes switch correctly on the released build, that the camera opens with a live preview in each, that video remains functional, and that a mode survives reboot — producing the project's first written regression record.

## 3. Description

The problem is that the project's correctness evidence is distributed across a journal, a changelog field, and the user's memory of daily use. None of it is per-release. When Phase 3 or Phase 4 breaks something, there is no recorded state of "all ten modes worked on v2.1" to compare against.

It belongs after the flash and before any Phase 3 work because Phase 3 modifies the HAL layer, and a HAL change that breaks a sensor-layer mode would otherwise be indistinguishable from a pre-existing defect.

The vibecoding slice strategy has a deliberate ordering. The first useful slice is the four tile-driven main modes, because Project-Comprehension identifies tiles as the highest-risk area and because four modes exercise both layers — the `50mp` tile drives the HAL layer while the DCG and LN tiles drive the sensor layer. The second slice covers the remaining six sensor variants, which are lower-risk because they differ only in generated blob content. The third slice is the reboot persistence and video checks, which are slower and need the user.

The fastest validation signal per mode is the Faz 2.1 script plus one camera open: the script confirms the layer actually changed, and the camera open confirms the change is usable. A mode that reports correctly but shows a black preview has failed, and the two checks together catch that.

What not to over-plan: image quality assessment. Whether `dcgB` still delivers its measured noise advantage is a separate question from whether the mode works, and Project-Comprehension marks that measurement `EV-21` at `probable` confidence. This pass verifies function, not quality.

The layer exclusion rule is a correctness property this pass must exercise rather than assume. Project-Ontology invariant 4 states that `50mp` and the DCG and LN modes are mutually exclusive, and Autopsy section 6 notes the rule "is enforced by control flow in a 280-line shell script rather than by a checked invariant". Switching from `50mp` directly to `ln2` and back is exactly the transition that would expose a control-flow gap.

## 4. Scope

- All ten modes: `stock`, `50mp`, `dcgA`, `dcgB`, `ln2`, `ln4`, `ln2s`, `ln4s`, `ln2f`, `ln4f`.
- Per mode: a smoke snapshot confirming the correct layer state, and a camera open confirming a live preview.
- Tile synchronization: selecting one of the four tiles turns the others off, verified visually.
- Direct transitions across the exclusion boundary, in both directions, to exercise the rule rather than assume it.
- Reboot persistence for at least two modes, one from each layer.
- Video capture at 1080p60 and 4K60, verified by the user in at least the stock mode and one modified mode.
- Shutter completion in the stock camera application for each of the four main modes.
- A written regression record: one row per mode with the checks and their outcomes.
- Any failure recorded as a finding with the mode, the layer, and the observed symptom.

## 5. Out of Scope

- Image quality comparison, noise measurement, or detail assessment. Function only.
- Any AGC-specific behavior. The AGC path is Phase 3's subject and is not exercised here.
- The `tiles hide` option, which has its own decision gate in Faz 2.4.
- Fixing any regression discovered. A finding is recorded and routed; the fix is scheduled deliberately.
- The WebUI's full surface beyond confirming it reports the current mode consistently with the tiles.
- Any HAL patch state other than the two the module produces, stock and fullres.
- Long-run stability, thermal behavior, or battery impact.

## 6. Current Repository Evidence

`ishtar-cam-modes/setmode.sh` was read in this run. Its usage line enumerates the ten modes: `setmode.sh [stock|50mp|ln2|ln4|ln2s|ln4s|ln2f|ln4f|dcgA|dcgB]`, and it reports status when invoked with no argument. Its header comment states the two-layer split and the exclusion rule with the reason: sensor mode 0 is 10-bit while DCG pulls the global white level to 12-bit, which produced corrupted 50 MP output.

`restart_camera()` in the same file implements the ordering invariant with the failure mode preserved in comments. The sequence is: stop `cameraserver` and wait for stopped; stop `vendor.camera-provider` and `vendor.camera-provider-2-7-ext` and wait; force-stop the camera applications; apply the HAL layer only at this point, because the binary is memory-mapped by running processes; then restart the providers and `cameraserver`. `CAM_APPS` is defined as `org.codeaurora.snapcam com.android.camera com.xiaomi.module.evaluation`.

The HAL write happens inside `restart_camera` between the service stop and start, guarded by `command -v hal_set`. On failure it prints a warning about a stock HAL md5 mismatch being normal after a system update, and continues rather than aborting — a deliberate degradation path worth verifying rather than assuming.

`ishtar-cam-modes/blobs/` contains nine sensor variants: `stock.bin`, `dcgA.bin`, `dcgB.bin`, `ln2.bin`, `ln2s.bin`, `ln2f.bin`, `ln4.bin`, `ln4s.bin`, `ln4f.bin`. The tenth mode, `50mp`, has no blob because it drives the HAL layer and forces the sensor layer to stock.

`ishtar-cam-modes/post-fs-data.sh` implements reboot persistence. Its dispatch reads the stored mode, maps `50mp` to `SENSOR_MODE=stock` with the HAL wanted, maps the nine sensor modes to themselves with the HAL left stock, and maps anything unrecognized to stock across all three.

`ishtar-cam-modes/module.prop` records the relevant fix history: v1.5 fixed tile synchronization, v1.6 fixed the mode-change camera lock by correcting the restart order, v1.7 made a mode change complete only when the camera is genuinely ready, and v2.1 fixed launcher icon rendering and made status read from the framework rather than a cache.

No regression record of any kind exists in the tree.

## 7. Planned Work Breakdown

- F2.3-01 — Define the per-mode check row
  - Description: Fix the columns before running: mode, expected sensor layer, expected HAL layer, smoke verdict, camera opens, preview live, shutter completes. A consistent row makes the record diffable across future releases.
  - Output: A regression record template.
- F2.3-02 — Run the four main tile-driven modes
  - Description: `50mp`, `dcgB`, `ln2`, `ln4` through their tiles. Per mode: snapshot, camera open, preview check, shutter. Confirm the other three tiles turn off.
  - Output: Four completed rows plus a tile synchronization verdict.
- F2.3-03 — Run the six remaining sensor variants
  - Description: `stock`, `dcgA`, `ln2s`, `ln2f`, `ln4s`, `ln4f` through the WebUI or the command interface. Per mode: snapshot and camera open.
  - Output: Six completed rows.
- F2.3-04 — Exercise the exclusion boundary in both directions
  - Description: Switch `50mp` to `ln2` and `ln2` to `50mp` directly, without passing through stock. Confirm the sensor layer returns to stock when the HAL layer engages, and the reverse.
  - Output: Two transition verdicts with snapshots on both sides.
- F2.3-05 — Verify reboot persistence for both layers
  - Description: Set a sensor mode, reboot, snapshot; set `50mp`, reboot, snapshot. Both layers reapply through a different code path than the interactive one, so both need checking.
  - Output: Two persistence verdicts.
- F2.3-06 — Verify video at both profiles
  - Description: Record 1080p60 and 4K60 in stock and in at least one modified mode, and confirm the files play. This is the user's action and tests Project-Ontology invariant 5.
  - Output: Four video verdicts.
- F2.3-07 — Assemble the regression record
  - Description: Collect every row, verdict, and snapshot reference into one document tied to the v2.1 build and the baseline snapshot identifier.
  - Output: The project's first written regression record.
- F2.3-08 — Route any failures
  - Description: For each failure, record the mode, the layer, the observed symptom, and the phase that owns the fix. Do not repair in place.
  - Output: A findings list with routing.

## 8. Acceptance Criteria

- All ten modes have a completed row; none is marked as assumed or skipped.
- For each mode, the smoke snapshot confirms the expected sensor and HAL layer state per the dispatch table in `post-fs-data.sh`.
- For each mode, the camera opens and the preview is live — a black preview is a failure, not a warning, because it is the documented symptom of the restart-ordering invariant being violated.
- Selecting any one of the four tiles turns the other three off, confirmed visually.
- Both exclusion-boundary transitions behave per Project-Ontology invariant 4, with snapshots on both sides.
- Reboot persistence is confirmed for one sensor-layer mode and for `50mp`.
- 1080p60 and 4K60 record and play back in stock and in at least one modified mode.
- The written regression record exists, is tied to the v2.1 build and the baseline snapshot identifier, and uses one consistent row shape.
- Every failure has a finding with a named owning phase; none is fixed inline.

## 9. Validation and Test Approach

This sub-phase is the project's first structured validation pass and mixes automated reporting with irreducibly manual checks. Both halves are recorded; neither substitutes for the other.

- `VAL-SMOKE` (from Faz 2.1) — per-mode state confirmation. Automated, read-only, run once per mode.
- `VAL-MANUAL` (proposed) — the user-performed checklist: camera opens, preview live, shutter completes, tiles synchronize, launcher entry renders, video records and plays. Autopsy's Gate 3, with the user as the named actor.
- `VAL-PERSIST` (proposed) — reboot, then a snapshot, for one mode per layer. Exercises the boot path rather than the interactive path.
- `VAL-DOCS` (proposed) — read back the regression record and confirm every mode has a row and every row has a verdict.

Local versus live: entirely live. No part of this pass has a host-side equivalent.

Security validation is not applicable. Ontology validation is: invariants 3, 4, and 5 are each exercised by a specific check in this pass, and the record should name which check covers which invariant.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Per-mode state reporter used ten times plus at each transition. | VAL-SMOKE, VAL-PERSIST |
| ishtar-cam-modes/setmode.sh | existing | Read-only context: the mode list and the restart ordering under test. | VAL-SMOKE, VAL-MANUAL |
| ishtar-cam-modes/post-fs-data.sh | existing | Read-only context: the boot dispatch that persistence testing exercises. | VAL-PERSIST |
| docs/regression-v2.1.md | proposed | The written regression record produced by this sub-phase. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 2.2 for a device running the released build and for the named baseline snapshot the record ties to. Depends on Faz 2.1 for the reporting surface.

Does not depend on Faz 2.4, and the two may run in either order — though running this pass first is preferable, since it may produce evidence about the `tiles hide` behavior that informs that decision.

Blocks every Phase 3 sub-plan. Phase 3 modifies the HAL layer, and without this record a Phase 3 regression cannot be distinguished from a pre-existing one.

Required human actions: every camera open, every shutter press, every video recording, every visual tile and launcher check, and two reboots. This is the most user-intensive sub-phase in Phase 2 and should be scheduled when the user has the device and time, not interleaved with automated work.

Required infrastructure: the device, KernelSU, `adb`, and enough storage for four video recordings.

Fresh session token and context risk: medium. Ten modes times two snapshots plus transitions is a large volume of short outputs. The mitigation is to record verdicts into the regression document as they are produced rather than accumulating raw output in the session.

Subagents are not recommended. The device is a single stateful resource and parallel access would corrupt the sequence.

## 11. Risks and Mitigations

- Risk: a mode reports the correct layer state but shows a black preview. Impact: without treating this as a failure, a violated restart-ordering invariant ships. Mitigation: the acceptance criteria classify black preview as a failure explicitly, and Project-Ontology invariant 3 documents the symptom so it is recognized rather than rationalized.
- Risk (`AUTOPSY-P0-02` pattern): the pass runs but verdicts are held in memory and written up afterward. Impact: partial or reconstructed evidence, which is what this whole phase exists to eliminate. Mitigation: F2.3-01 fixes the record shape before the pass starts, and verdicts are written per mode.
- Risk: the exclusion-boundary transitions are skipped because they seem redundant with the individual mode checks. Impact: the one rule enforced only by shell control flow goes untested, and Autopsy section 6 names this as where `Kararlar #4` will be riskiest. Mitigation: F2.3-04 is a distinct work item with its own acceptance criterion.
- Risk: the HAL write inside `restart_camera` fails silently in the degradation path and the mode reports success. Impact: a `50mp` mode that reports fine and delivers nothing. Mitigation: the smoke snapshot classifies the live HAL checksum independently of what the module reports, so the two can disagree visibly.
- Risk: video verification is deferred because it is slow. Impact: a standing user-validated acceptance criterion goes unverified on the released build. Mitigation: F2.3-06 is scoped to four recordings rather than a full matrix, which keeps it affordable.
- Risk: a failure is found and fixed immediately because it looks small. Impact: the fix lands without the owning phase's validation and the regression record describes a build that no longer exists. Mitigation: F2.3-08 routes rather than repairs, and the out-of-scope section states this.
- Risk: the six lower-risk sensor variants consume most of the session's budget through repetition. Impact: the higher-value checks get compressed. Mitigation: the slice ordering puts the four main modes first, so the highest-value evidence exists before fatigue sets in.

## 12. Desired End State

A written regression record exists for the v2.1 build, tied to the baseline snapshot, with one row per mode covering layer state, camera open, live preview, and shutter, plus verdicts for tile synchronization, both exclusion-boundary transitions, reboot persistence on both layers, and video at two profiles. Three Project-Ontology invariants have been exercised rather than assumed. Any failure is a routed finding.

The evidence an implementer should produce is the completed record with its ten rows and eight additional verdicts, plus the stored snapshots each row references.

The ledger summary Step 4 should append records: the record path, the pass and fail counts, which invariants were exercised, and which findings were routed where.

## 13. Next Sub-Phase Transition Criteria

- All ten modes have recorded verdicts and no row is marked assumed.
- No mode exhibits a black preview.
- Both exclusion-boundary transitions behave correctly with snapshots on both sides.
- Reboot persistence is confirmed for both layers.
- Video at 1080p60 and 4K60 is confirmed functional.
- The regression record is written and tied to the build and baseline identifiers.
- Any failure is routed with an owning phase, and Phase 3 does not begin while an unrouted failure exists.
