# Faz 5.1 — Twelve Bit Mode Zero Blob Generation

## 1. Context

Main-Planing Phase 5 executes a user-approved experiment: "Sensor mode 0 (50 MP) is 10-bit while DCG raises the global white level to 12-bit, which is why the layers currently exclude each other. Decision `#4` approves moving mode 0 to 12-bit after everything else is stable. This is a sensor-blob edit using the existing `tools/` generation scripts, and it is explicitly single-purpose: if it fails, only this change is reverted."

Its first vibecoding slice is stated directly: "Generate the 12-bit mode-0 blob, verify with `verify_ln.py`, and test in a temporary bind-mount before committing it to `blobs/`."

This sub-phase performs the first two thirds of that slice — generate and verify on the host. The temporary mount test is Faz 5.2, and the exclusion rule disposition is Faz 5.3.

Autopsy raises a caution the main plan does not. Section 11: "Phase 5 (mode-0 12-bit) rests entirely on `Kararlar #4` and on the assumption that the 10-bit/12-bit mismatch is the sole cause of the exclusion; no measurement in the repository confirms that this is the *only* obstacle." Project-Ontology `OQ-04` records the same as an open question, and Project-Comprehension `H-04` marks the hypothesis `tentative`.

That caution shapes the sub-phase. The goal is a correct blob, not a proof that the blob solves the problem — and separating those is what keeps a negative result informative rather than confusing.

## 2. Goal

Generate a sensor blob in which mode 0 operates at 12-bit rather than 10-bit, and verify on the host that the blob is structurally sound and that mode 0 is the only mode changed.

## 3. Description

The problem is a bit-depth mismatch between two sensor configurations that the module currently resolves by refusing to run them together. Project-Ontology invariant 4 records the exclusion and its cause; `Kararlar #4` approves attempting to remove it.

It belongs after Phases 3 and 4 because Main-Planing conditions it on "after everything else is stable", and because a sensor-layer change during an unresolved HAL-layer investigation would produce ambiguous results across two layers.

The vibecoding slice strategy: generate, verify structurally, and diff against the current blob to confirm the change is confined to mode 0. The fastest validation signal is `verify_ln.py`, which already exists and already checks the properties that matter. This is the rare sub-phase in the project with a genuine host-side validation surface.

What should not be over-planned: bit-depth changes for other modes, or a general bit-depth parameterization of the generation tools. The experiment is single-purpose by explicit decision, and its revertibility depends on staying that way.

The tooling is well positioned. `verify_ln.py` was read in this run and validates the container's integrity — header signature, size field, and checksum — then reads the mode table and per-mode register values, and compares configurations across blobs. Its existing comparison capability is directly reusable: the check that a generated blob differs from the reference only where intended is structurally the same check it already performs between mode variants.

## 4. Scope

- Location of the bit-depth field for mode 0 within the sensor blob's mode table.
- Generation of a modified blob with mode 0 at 12-bit, using the existing `tools/` scripts.
- Structural verification with `verify_ln.py`: header signature, size field, and checksum integrity.
- A differential check confirming that only mode 0's configuration changed and the other twenty-two mode table entries are byte-identical.
- Confirmation that the generated blob is exactly 1,062,250 bytes, the size the module enforces.
- An assessment of which register values the bit-depth change implies, since a bit-depth field may not be the only value that must move for the mode to be coherent.
- Recording of the mode table layout details into Project-Ontology section 3, which currently describes the format at a high level.

## 5. Out of Scope

- Mounting or testing the blob on the device. Faz 5.2 owns that.
- Removing or relaxing the exclusion rule in `setmode.sh`. Faz 5.3 owns that.
- Any change to modes other than mode 0.
- Any HAL-layer change. Phase 4's artifact is fixed by this point.
- Regenerating the other nine blob variants.
- Committing the new blob to `blobs/` as a shipped variant — Main-Planing's slice explicitly places that after the mount test.
- Changing the generation tools' interfaces or adding parameterization.

## 6. Current Repository Evidence

`ishtar-cam-modes/tools/verify_ln.py` was read in this run. It asserts the file begins with `QTI Chromatix Header`, that the size field at offset `0x1C` equals the file length minus four, and that the trailing four bytes are the checksum of everything preceding. It then walks a mode table beginning at offset `0xD0` with 60-byte entries, reading a name field of up to 44 bytes followed by four unsigned integers, and resolves per-entry data through a base offset stored at `0xB8`. It tracks the register addresses `0x0112`, `0x0113`, `0x0342`, `0x0343`, and `0x31A4`, and locates `streamConfiguration` and `resolutionData` entries by name.

Registers `0x0112` and `0x0113` are the standard sensor pixel format registers on this class of sensor — they encode bit depth. Their presence in the tool's tracked address set means the verification harness already reads the field this experiment changes, which is a substantial head start.

The tool's docstring states its three checks: container integrity per blob, per-mode register and stream and resolution values, and an equality comparison of the fast variants' mode 1 configuration against the corresponding base variant. That third check is a cross-blob differential, which is the mechanism F5.1-04 needs.

`ishtar-cam-modes/tools/` also holds `dcg_multimode.py` (192 lines), `ln_multimode.py` (274 lines), and `port_sensor_mod.py` (140 lines). Project-Comprehension `TRACE-08` records these as the blob generation path with `verify_ln.py` as its only test, and notes this is the single row in the trace map with any test coverage at all.

`ishtar-cam-modes/setmode.sh` defines `EXPECT_SIZE=1062250` and Project-Ontology section 3 records the same figure with the note that the blob is "QTI Chromatix format with a `regSetting`/register map and a 23-entry mode table".

`ishtar-cam-modes/blobs/` holds nine variants including `stock.bin`, which is the reference the generated blob should be diffed against.

Project-Ontology invariant 4 records the exclusion and its cause: mode 0 is 10-bit while DCG pulls the global white level to 12-bit, and combined, 50 MP output was corrupted.

No Python interpreter is available on this host by default, as measured in this run. Faz 1.4's toolchain procedure covers this, and `verify_ln.py` imports only the standard library, so the embeddable distribution is sufficient without capstone or pyelftools.

## 7. Planned Work Breakdown

- F5.1-01 — Confirm the tooling runs
  - Description: Execute `verify_ln.py` against the existing `stock.bin` and confirm it passes, establishing that the harness works before it is used to judge a new artifact.
  - Output: A baseline verification pass.
- F5.1-02 — Locate the bit-depth field for mode 0
  - Description: Using the mode table walk `verify_ln.py` already implements, read mode 0's values for registers `0x0112` and `0x0113` and confirm they encode 10-bit. Compare against a 12-bit mode's values from an existing DCG variant to establish the target encoding.
  - Output: The current and target field values, read from real blobs rather than assumed.
- F5.1-03 — Assess the implied register set
  - Description: Determine whether changing bit depth requires other values to move for the mode to be coherent — line length, frame length, or output data format fields. Compare mode 0 against a known 12-bit mode across the tracked register set to see what else differs.
  - Output: A register change set with each entry justified by comparison.
- F5.1-04 — Generate the modified blob
  - Description: Produce the blob using the existing generation scripts, applying only the assessed register changes to mode 0.
  - Output: A candidate blob.
- F5.1-05 — Verify structural integrity
  - Description: Run `verify_ln.py` against the candidate. Header signature, size field, and checksum must all pass, and the file must be exactly 1,062,250 bytes.
  - Output: A structural verification result.
- F5.1-06 — Differential check against the reference
  - Description: Confirm that mode 0's configuration changed as intended and that the other twenty-two mode table entries are byte-identical to the reference.
  - Output: A differential report naming every changed byte range.
- F5.1-07 — Record the mode table details
  - Description: Write the mode table layout, the bit-depth register addresses, and the observed 10-bit and 12-bit encodings into Project-Ontology section 3, which currently describes the format only in outline.
  - Output: An extended ontology entry.

## 8. Acceptance Criteria

- `verify_ln.py` passes against the existing reference blob before the candidate is judged.
- The current and target bit-depth encodings are read from real blobs, not assumed from the register specification.
- The implied register set is justified by comparison against a known 12-bit mode rather than by reasoning alone.
- The candidate blob passes all three `verify_ln.py` integrity checks.
- The candidate blob is exactly 1,062,250 bytes.
- The differential check confirms changes confined to mode 0, with every changed byte range named.
- The mode table layout and bit-depth encodings are recorded in Project-Ontology section 3.
- The candidate is not placed in `blobs/` as a shipped variant during this sub-phase.
- No device interaction has occurred.

## 9. Validation and Test Approach

This is the only sub-phase in the roadmap whose validation is substantially host-side, which makes it unusually cheap to iterate. That property should be used: generate and verify as many times as needed before anything touches the device.

- `VAL-BLOB` (proposed) — `verify_ln.py` against the candidate, checking header signature, size field, and checksum.
- `VAL-SIZE` (proposed) — byte-exact size confirmation against the 1,062,250 figure the module enforces.
- `VAL-DIFF` (proposed) — the differential against the reference blob, confirming changes are confined to mode 0.
- `VAL-BASELINE` (proposed) — `verify_ln.py` against the existing reference first, establishing the harness works before it judges new work.
- `VAL-DOCS` (proposed) — read back the ontology addition and confirm the recorded encodings match what was read from the blobs.

Local versus live: entirely local. There is no live dimension, and that separation is what makes Faz 5.2's mount test a clean single-variable experiment.

Security validation is not applicable. Ontology validation applies to the mode table documentation.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/tools/verify_ln.py | existing | The verification harness; run against reference and candidate. | VAL-BLOB, VAL-BASELINE |
| ishtar-cam-modes/blobs/stock.bin | existing | The reference blob for the differential and the baseline check. | VAL-DIFF, VAL-BASELINE |
| ishtar-cam-modes/tools/port_sensor_mod.py | existing | Generation tooling used to produce the candidate. | VAL-BLOB |
| Planner-docs/Project-Ontology.md | modified | Record the mode table layout and the bit-depth encodings. | VAL-DOCS |
| docs/mode0-12bit-candidate.md | proposed | The generation record with the register change set and differential report. | VAL-DIFF, VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 1.4 for a working Python environment, since none is available on this host by default and `verify_ln.py` cannot run without one.

Depends on Faz 3.6's priority decision. Main-Planing section 9 lists "Whether Phase 5 still has priority given how much Phase 3 has grown" among the decisions needing human confirmation, and Faz 3.6 routes it. Phase 5 should not start before that question is answered.

Depends on Phase 4 being complete, per Main-Planing's "after everything else is stable" condition.

Blocks Faz 5.2, which mounts what this sub-phase generates.

Required decisions: none during the work; the go-ahead decision belongs to Faz 3.6.

Required infrastructure: a Python interpreter and the existing tools. No device.

Required human approvals: none for host-side generation.

Fresh session token and context risk: low. Small scripts, structured binary reads, and short outputs.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk (`OQ-04`, `H-04`): the bit-depth change is not the only obstacle to composition, so a correct blob still does not enable it. Impact: the experiment produces a negative result that looks like a generation failure. Mitigation: this sub-phase's goal is explicitly a correct blob rather than a working composition, so a structurally sound blob is a success here regardless of what Faz 5.2 finds.
- Risk: the bit-depth change requires other register values to move and only the depth field is changed. Impact: an incoherent mode that produces corrupted output, which is exactly the symptom the exclusion rule exists to prevent. Mitigation: F5.1-03 compares against a known 12-bit mode across the tracked register set rather than reasoning about which fields matter.
- Risk: the checksum or size field is not recomputed after the edit. Impact: the module's install guard rejects the blob, or worse, accepts a structurally broken one. Mitigation: `verify_ln.py` checks both, and F5.1-01 confirms the harness works before it is trusted.
- Risk: the generation changes more than mode 0 as a side effect of how the tools rewrite the container. Impact: the single-purpose property that makes the experiment revertible is lost. Mitigation: `VAL-DIFF` names every changed byte range.
- Risk: the candidate is placed in `blobs/` before the mount test. Impact: an unproven variant becomes shippable and could be selected by a mode switch. Mitigation: the out-of-scope section and the acceptance criteria both forbid it, following Main-Planing's own slice ordering.
- Risk: no Python interpreter is available and the sub-phase stalls. Impact: the only host-side validation surface in the project is unusable. Mitigation: the dependency on Faz 1.4 is explicit, and the finding that this host lacks a system interpreter is already recorded there.
- Risk: the register encodings are assumed from general sensor knowledge rather than read. Impact: a plausible but wrong value. Mitigation: F5.1-02 requires reading both encodings from real blobs.

## 12. Desired End State

A candidate sensor blob exists in which mode 0 operates at 12-bit, structurally verified by the existing harness, exactly the required size, and differentially confirmed to change nothing but mode 0. The register changes are justified by comparison against a known 12-bit mode, and the mode table layout with its bit-depth encodings is recorded in the ontology.

The evidence an implementer should produce is the baseline verification pass, the read encodings, the justified register change set, the candidate's verification result, and the differential report.

The ledger summary Step 4 should append records: the register values changed, the differential outcome, the verification result, and confirmation that the candidate was not placed in `blobs/`.

## 13. Next Sub-Phase Transition Criteria

- The harness passes against the reference before judging the candidate.
- The candidate passes all three integrity checks at exactly 1,062,250 bytes.
- The differential confirms changes confined to mode 0.
- The register change set is justified by comparison, not by reasoning alone.
- The mode table details are recorded in the ontology.
- The candidate remains outside `blobs/`, ready for a temporary mount in Faz 5.2.
