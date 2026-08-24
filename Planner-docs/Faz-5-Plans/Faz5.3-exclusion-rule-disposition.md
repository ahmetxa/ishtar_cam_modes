# Faz 5.3 — Exclusion Rule Disposition

## 1. Context

Project-Ontology invariant 4 states the rule and its expiry condition: "`50mp` and DCG/LN are mutually exclusive until `Kararlar #4` is executed and proven." Faz 5.2 executes and either proves or disproves it. This sub-phase acts on that result.

Autopsy identifies where the risk sits. Section 6, under "Unclear module boundaries": "the mutual-exclusion rule (`Kararlar #1`) is enforced by control flow in a 280-line shell script rather than by a checked invariant. When `Kararlar #4` removes that exclusion, this is where the change will be riskiest."

Project-Comprehension records the same as `ARC-03`: "Layer exclusion is a system rule — Enforced by control flow in a 280-line shell script, not by a checked invariant", status `divergent`. That divergence has been harmless while the rule held; it becomes material the moment the rule changes, because control-flow enforcement means the rule is expressed in several places rather than one.

Main-Planing's functional target names the outcome: "If the approved mode-0 12-bit experiment succeeds, 50 MP composes with LN2 and LN4 rather than excluding them."

This sub-phase runs in both outcomes, like Faz 3.6 does for its phase. On success it removes the exclusion and validates the enlarged mode space. On failure it records the negative result, confirms the exclusion remains correctly enforced, and closes the phase.

## 2. Goal

Act on the composition result: either remove the layer exclusion across every place it is enforced and validate the resulting mode space, or record the negative result and confirm the exclusion remains intact and correctly justified.

## 3. Description

The problem on the success path is that removing a rule enforced by control flow in several files is not a deletion — it is a redesign of the dispatch. Every place that assumes selecting `50mp` forces the sensor layer to stock must be found and changed consistently, and a partial change would produce a state where one code path composes and another does not.

The problem on the failure path is smaller but real: an experiment that produced a negative result leaves an updated ontology invariant, a candidate blob that should not ship, and a decision recorded rather than left implicit.

It belongs at the end of Phase 5 because it consumes Faz 5.2's outcome.

The vibecoding slice strategy on success: enumerate the enforcement points first, change them together, then validate the enlarged mode space against the Faz 2.3 regression record. The fastest validation signal is a composed mode switching and the camera opening — but the meaningful signal is the full mode surface still working, because the enlarged space includes every combination the old dispatch prevented.

What should not be over-planned on either path: a general layer composition framework, or new mode names for every combination. If composition works, the minimal change is to stop forcing the sensor layer to stock when `50mp` is selected. Whether the user interface gains new combined modes is a separate product question.

The mode space question is worth stating plainly, because it determines the validation cost. Today there are ten modes, one of which is the HAL layer and nine of which are sensor layer states. If the layers compose, the space becomes a product rather than a list, and validating it exhaustively would be substantially more work than Faz 2.3's ten-mode pass. The scope below deliberately limits validation to the combinations the target end state actually names — 50 MP with LN2 and with LN4 — rather than the full product.

## 4. Scope

On the success path:

- Enumeration of every place the exclusion is enforced, across `setmode.sh`, `post-fs-data.sh`, `action.sh`, the tile application, and the web interface.
- A consistent change removing the forcing behavior at every enumerated point.
- Placement of the candidate blob into `blobs/` as the mode 0 configuration, with its checksum recorded.
- Validation of the combinations the target end state names: 50 MP with LN2 and 50 MP with LN4.
- A regression pass over the existing ten modes, compared against the Faz 2.3 record.
- Reboot persistence for a composed state, since `post-fs-data.sh` reapplies through a separate path.
- Update of Project-Ontology invariant 4 and Project-Comprehension `ARC-03`.

On the failure path:

- Confirmation that the exclusion remains correctly enforced and that the test left no residue.
- Retirement of the candidate blob, with the generation record kept.
- Update of invariant 4 with the measured reason the exclusion stands.

Both paths:

- A recorded decision with reasoning.
- A phase closure entry in the ledger.

## 5. Out of Scope

- Adding new mode names or user interface entries for combined states. That is a product decision outside this experiment.
- Validating the full product of layer combinations. Only the named combinations are in scope.
- Any HAL-layer change.
- Bit-depth changes for modes other than mode 0.
- Converting the exclusion from control-flow enforcement to a checked invariant as a general refactor. If the exclusion is removed there is nothing left to check; if it stands, converting it is a separate improvement with its own justification.
- Release packaging, which is Phase 9.
- Re-running the composition experiment. Faz 5.2's result is the input.

## 6. Current Repository Evidence

`ishtar-cam-modes/setmode.sh` was read in this run. Its header states the exclusion and the reason. Its dispatch sets `HAL_WANT` alongside the sensor mode, and `restart_camera` applies the HAL layer inside the service-stopped window. This is one enforcement point.

`ishtar-cam-modes/post-fs-data.sh` was inspected in this run and contains a second, independent enforcement point. Its case dispatch maps `50mp` to `SENSOR_MODE=stock` with the HAL wanted, maps the nine sensor modes to themselves with `HAL_WANT=stock`, and maps anything unrecognized to stock across all three. The forcing behavior is written into the boot path separately from the interactive path, which is exactly the multi-site enforcement Autopsy warns about.

`ishtar-cam-modes/customize.sh` prints "50MP ile DCG/LN birbirini disler: biri acilinca digeri kapanir" during installation — a third place the rule is expressed, this time as user-facing text rather than logic. Text that describes a removed rule is a smaller defect than logic that enforces it, but it is still a place the change must reach.

`ishtar-cam-modes/webroot/index.html` was partially read in this run. Its `build()` function constructs buttons from a `MAIN_MODES` list and an `extra` group, and its toggle handler passes `current === id ? 'stock' : id` — a two-state toggle per mode. Whether the interface encodes exclusivity beyond that toggle was not determined and should be established during enumeration.

`ishtar-cam-modes/module.prop` records in its v2.0 entry that the fourth QuickSettings tile was added for 50 MP and that "dort kutucuk birbirini disler, biri acilinca digerleri kapanir" — the four tiles are mutually exclusive. Tile exclusivity is a fourth enforcement surface, in the tile application's Java rather than in shell.

That gives at least four surfaces: the interactive dispatch, the boot dispatch, the installer text, and the tile application, plus the web interface pending enumeration. Project-Comprehension `TRACE-06` records that the tile application's Java sources have not been read by any ClaudeQB run, which means the fourth surface's enforcement mechanism is currently unknown.

Project-Ontology invariant 4 and Project-Comprehension `ARC-03` are the records that change on either path.

## 7. Planned Work Breakdown

- F5.3-01 — Enumerate every enforcement point
  - Description: Find every place the exclusion is enforced or described, across the interactive dispatch, the boot dispatch, the installer text, the tile application, and the web interface. Record the mechanism at each.
  - Output: An enforcement point inventory with a mechanism per entry.
- F5.3-02 — Decide the disposition
  - Description: On a successful composition, decide to remove the exclusion. On a failure, decide to retain it. Record the reasoning and the measured basis from Faz 5.2.
  - Output: A recorded decision.
- F5.3-03 — Apply the change consistently, on success
  - Description: Change every enumerated point together. A partial change produces a dispatch where the interactive path composes and the boot path does not, which is worse than either consistent state.
  - Output: A consistent dispatch across all enforcement points.
- F5.3-04 — Adopt the candidate blob, on success
  - Description: Place the verified candidate into `blobs/` as the mode 0 configuration and record its checksum where the module's guards can use it.
  - Output: An adopted blob with a recorded checksum.
- F5.3-05 — Validate the named combinations, on success
  - Description: Verify 50 MP with LN2 and 50 MP with LN4: layer states correct, camera opens, capture completes at full resolution.
  - Output: Two combination verdicts.
- F5.3-06 — Run the ten-mode regression, on success
  - Description: Confirm the existing ten modes still behave, compared against the Faz 2.3 record. Removing a forcing behavior changes the dispatch for every mode, not only the composed ones.
  - Output: Ten rows compared against the reference.
- F5.3-07 — Verify reboot persistence for a composed state, on success
  - Description: Set a composed state, reboot, and confirm both layers reapply through the boot path.
  - Output: A persistence verdict.
- F5.3-08 — Retire the candidate, on failure
  - Description: Keep the generation record and the measured negative result; do not ship the blob. Confirm the device carries no residue from the test.
  - Output: A retirement record.
- F5.3-09 — Update the invariant and close the phase
  - Description: Update Project-Ontology invariant 4 and Project-Comprehension `ARC-03` to reflect the outcome, and write the phase closure entry.
  - Output: Updated continuity artifacts and a ledger closure entry.

## 8. Acceptance Criteria

- The enforcement point inventory covers all surfaces, including the tile application, whose mechanism must be established rather than assumed.
- A disposition decision is recorded with its measured basis from Faz 5.2.
- On success: every enumerated enforcement point is changed, with none left partially enforcing.
- On success: the candidate blob is in `blobs/` with its checksum recorded where the guards read it.
- On success: both named combinations work — correct layer states, camera opens, full-resolution capture completes.
- On success: all ten existing modes pass against the Faz 2.3 record with no regression.
- On success: reboot persistence for a composed state is confirmed.
- On failure: the candidate is retired, the generation record is kept, and the device carries no residue.
- Project-Ontology invariant 4 reflects the outcome, and `ARC-03` is updated.
- The ledger carries a phase closure entry.

## 9. Validation and Test Approach

Validation differs sharply by path. The success path requires the most extensive device validation in Phase 5; the failure path requires only confirmation of restoration and correct records.

- `VAL-SMOKE` (from Faz 2.1) — per-mode and per-combination state reporting.
- `VAL-COMBINATION` (proposed) — for each named combination: both layer states correct simultaneously, camera opens, capture completes at full resolution. This is the check that could not exist before.
- `VAL-COMPARE` (proposed) — the ten-mode pass compared against the Faz 2.3 regression record.
- `VAL-PERSIST` (from Faz 2.3) — reboot and re-snapshot for a composed state.
- `VAL-STATIC` (from Faz 1.5) — the enforcement point enumeration, which is source review across five surfaces.
- `VAL-DOCS` (proposed) — read back the decision, the updated invariant, and `ARC-03`.

Local versus live: enumeration is local; everything else on the success path is live. On the failure path validation is almost entirely document-level.

Security validation is not applicable. Ontology validation is central — invariant 4 is the record being changed.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/setmode.sh | modified | Interactive dispatch; forcing behavior removed on the success path. | VAL-STATIC, VAL-COMBINATION |
| ishtar-cam-modes/post-fs-data.sh | modified | Boot dispatch; the independent second enforcement point. | VAL-STATIC, VAL-PERSIST |
| ishtar-cam-modes/customize.sh | modified | Installer text describing the exclusion. | VAL-STATIC |
| ishtar-cam-modes/blobs/stock.bin | modified | Mode 0 configuration replaced by the adopted candidate on the success path. | VAL-COMBINATION |
| Planner-docs/Project-Ontology.md | modified | Invariant 4 updated to reflect the outcome. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 5.2 for the composition result and on Faz 5.1 for the verified candidate. Depends on Faz 2.3 for the ten-mode reference the success path compares against.

Blocks Phase 9's release work on the success path, since the release contents change materially: a new blob, a changed dispatch, and a changed capability claim.

Required decisions: the disposition, which follows from the measurement but should still be recorded as a decision rather than treated as automatic — particularly on a partial success, where the composition works but with a quality cost.

Required infrastructure: the device, the module, and on the success path the ability to modify and reinstall module scripts.

Required human actions: the combination captures, the ten-mode camera opens, and a reboot.

Fresh session token and context risk: low on the failure path, medium on the success path due to the regression pass volume.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk (`ARC-03`, Autopsy section 6): the exclusion is removed from the interactive dispatch but not from the boot dispatch. Impact: a composed state that works until reboot and then silently reverts, which is a worse failure than either consistent behavior because it is intermittent. Mitigation: F5.3-01 enumerates before changing, F5.3-03 requires a consistent change, and F5.3-07 tests the boot path specifically.
- Risk: the tile application's enforcement mechanism is unknown and is missed. Impact: the four tiles continue to exclude each other while the shell dispatch composes, producing an interface that cannot express the new capability. Mitigation: the enforcement inventory names the tile application explicitly, and the acceptance criteria require its mechanism to be established rather than assumed.
- Risk: removing a forcing behavior changes dispatch for modes that previously worked. Impact: a regression in the existing ten modes. Mitigation: F5.3-06 runs the full pass against the recorded reference.
- Risk: the composition works but with a quality cost that makes it undesirable. Impact: a capability is shipped that the user would not choose. Mitigation: F5.3-02 records the disposition as a decision informed by Faz 5.2's quality comparison, not as an automatic consequence of the mechanism working.
- Risk: the candidate blob replaces the shipped mode 0 configuration and a defect appears later. Impact: a sensor-layer regression affecting the mode most consumers use. Mitigation: version control from Faz 1.1 makes the previous blob recoverable, and the checksum guard detects an unexpected state.
- Risk: on the failure path the candidate is left in the tree unmarked. Impact: a future session mistakes it for a shipped variant. Mitigation: F5.3-08 requires an explicit retirement record while keeping the generation record.
- Risk: the mode space becomes a product and validation cost grows without anyone deciding it should. Impact: unbounded regression work. Mitigation: the scope limits validation to the combinations the target end state names.

## 12. Desired End State

Phase 5 closes with a decision. Either the exclusion is removed consistently across every enforcement point, the candidate blob is adopted, both named combinations work, the existing ten modes are unregressed, and a composed state survives a reboot — or the negative result is recorded, the exclusion is confirmed intact with its measured justification, and the candidate is retired.

The evidence an implementer should produce is the enforcement inventory, the decision record, and on the success path the two combination verdicts, the ten-row comparison, and the persistence verdict.

The ledger summary Step 4 should append the phase closure entry: the composition outcome, the disposition, the enforcement points changed, the validation results, and what Phase 9 inherits.

## 13. Next Sub-Phase Transition Criteria

- The enforcement inventory is complete, with the tile application's mechanism established.
- A disposition decision is recorded with its measured basis.
- On success: every enforcement point is consistently changed, both combinations work, the ten modes are unregressed, and reboot persistence holds.
- On failure: the candidate is retired and the exclusion is confirmed intact.
- Invariant 4 and `ARC-03` reflect the outcome.
- The ledger carries the phase closure entry.
