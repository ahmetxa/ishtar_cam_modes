# Faz 6.1 — SYMLINK Entry in Device Trees

## 1. Context

Main-Planing Phase 6's first vibecoding slice is unusually direct: "Add the single line to `device_ishtar/proprietary-files.txt` and mirror it to `refs/a16_ishtar/`. This is a one-line change and should not wait for Phase 7."

Autopsy agrees and elevates the scheduling point. Section 12 under Phase 6: "This is a one-line change per tree and is independent of every other phase; schedule it early rather than by phase order." It is filed as `AUTOPSY-P1-04` with the impact stated: "`ishtar-aon-fix` exists solely to work around a build-time defect that is one line to fix; every future build inherits the defect."

The evidence is unusually firm for this project. Both Step 1 and Step 1.5 ran `grep -c 'SYMLINK'` against `device_ishtar/proprietary-files.txt` and `refs/a16_ishtar/proprietary-files.txt` and both returned zero. Project-Comprehension records it as `EV-11`, confidence `confirmed`.

The root cause is equally firm. Project-Comprehension `TRACE-14` maps the domain concept "Device-tree defect" to `device_ishtar/proprietary-files.txt` with the core implementation described as "missing `;SYMLINK=`". Project-Ontology section 2 records what the AON chain supplies: aperture, OIS, laser autofocus, and face-scene providers.

This sub-phase is therefore the roadmap's clearest cost-to-value case: one line per tree, against a defect that currently requires a whole runtime module to work around.

## 2. Goal

Add the missing symlink declaration to both device trees so that a build creates the `aon_front.pb` path natively, removing the need for a runtime workaround on future builds.

## 3. Description

The problem is a contract mismatch between the device tree and the vendor blob's expectations. The blob expects a file at a path the build does not create, so the AON chain fails to initialize and four provider capabilities disappear. The runtime module compensates by creating the path after boot.

It belongs early rather than at phase 6's position in the numbered order, because it is independent of every other phase and because every build made before the fix inherits the defect. Both Main-Planing and Autopsy say so explicitly.

The vibecoding slice strategy is minimal by nature: determine the correct entry form, add it to both trees, and verify by reading it back. The fastest validation signal is that the grep which currently returns zero returns one.

What should not be over-planned: the build verification. Confirming that a build actually creates the path requires a working build environment, and there is none — WSL2 is not installed and Phase 7 exists to change that. This sub-phase makes the change and states plainly that its effect is unverified until a build exists. Faz 6.2 handles that deferral explicitly.

The entry form needs care rather than length. A proprietary-files entry with a symlink declaration has a specific syntax, and the correct form should be derived from how the extraction tooling in the device tree consumes the file, or from a comparable entry in one of the other reference trees, rather than from memory. Three other trees are present under `refs/` and at least one may carry symlink entries that demonstrate the syntax.

## 4. Scope

- Determination of the correct entry syntax, derived from tooling or from a comparable entry in another tree rather than assumed.
- Identification of the exact source path and target path for `aon_front.pb`, taken from what the runtime module creates.
- Addition of the entry to `device_ishtar/proprietary-files.txt`.
- Addition of the mirrored entry to `refs/a16_ishtar/proprietary-files.txt`.
- Verification that both files now carry exactly one symlink entry, changing the recorded zero counts.
- An explicit statement that the change's effect is unverified until a build exists, so the fix is not recorded as proven.
- A check of whether `refs/a16_sm8550/` or `common_sm8550/` also need the entry, since the Android 16 target spans two trees.
- Update of `EV-11` and `TRACE-14` to reflect the change.

## 5. Out of Scope

- Building anything. No build environment exists; Phase 7 provides it.
- Removing, disabling, or modifying the `ishtar-aon-fix` module. Its disposition is Faz 6.2.
- Any other device tree change, including unrelated proprietary-files corrections.
- Verifying that the AON chain works, which requires a build that includes the entry.
- Changes to `refs/los_ishtar`, `refs/los_sm8550`, or `refs/neo_ishtar`, which Autopsy identifies as comparison sources rather than build inputs.
- Upstreaming the change to any external project.
- Any camera HAL or sensor layer change.

## 6. Current Repository Evidence

`grep -c 'SYMLINK'` returns 0 for `device_ishtar/proprietary-files.txt` and 0 for `refs/a16_ishtar/proprietary-files.txt`. This was measured in the Step 1 run and independently re-measured in the Step 1.5 run, and Project-Comprehension records it as `EV-11` with confidence `confirmed`.

`ishtar-aon-fix/` contains exactly three files: `customize.sh`, `module.prop`, and `post-fs-data.sh`. Main-Planing section 3 describes it as "a three-file module that creates the missing `/vendor/lib64/camera/aon_front.pb` path, repairing the AON → CSS → NCS chain (aperture, OIS, laser AF, face-scene providers)". The module's `post-fs-data.sh` is the authoritative source for the exact path the build must produce, since it is what currently works.

Autopsy section 3 records that the module is "explicitly documented as independent of KernelSU module mounting", which is a deliberate resilience choice and is relevant to Faz 6.2's disposition rather than to this sub-phase.

Autopsy section 7 states the mismatch precisely: "It is a contract mismatch between the device tree and the vendor blob's expectations, currently patched at runtime instead of at build time."

`device_ishtar/` also contains `Android.bp`, `Android.mk`, `BoardConfig.mk`, `device.mk`, and a `README.md`, per Autopsy section 2. The extraction tooling that consumes `proprietary-files.txt` may be referenced from one of these or may live in the vendor tooling, and finding it is what establishes the correct syntax.

`refs/` holds five trees. Autopsy section 3 records that `a16_ishtar` and `a16_sm8550` are the Android 16 inputs while `los_*` and `neo_*` are comparison sources, with the caveat that "this is inferable only from naming". Faz 1.6's reference index resolves that inference, which is why this sub-phase benefits from it having run.

Project-Comprehension `ARC-06` records the architectural position: "The AON fix belongs in the device tree — Implemented as a runtime module; the tree still lacks the entry", status `divergent`. This sub-phase closes half of that divergence; Faz 6.2 closes the rest.

## 7. Planned Work Breakdown

- F6.1-01 — Establish the correct entry syntax
  - Description: Derive the symlink declaration form from the extraction tooling that consumes `proprietary-files.txt`, or from a comparable entry in another reference tree. Do not assume the syntax.
  - Output: The entry form with its source cited.
- F6.1-02 — Determine the source and target paths
  - Description: Read `ishtar-aon-fix/post-fs-data.sh` for the exact path the module creates, since that is the working reference, and identify the corresponding source file in the vendor image.
  - Output: A source and target path pair.
- F6.1-03 — Determine the tree scope
  - Description: Establish whether `refs/a16_sm8550/` or `common_sm8550/` also need the entry, given that the Android 16 target spans a device tree and a platform tree.
  - Output: A definitive list of files to change.
- F6.1-04 — Add the entry to the current device tree
  - Description: Add the declaration to `device_ishtar/proprietary-files.txt` in the correct section, following the file's existing ordering conventions.
  - Output: A one-line addition.
- F6.1-05 — Mirror to the Android 16 tree
  - Description: Add the same entry to `refs/a16_ishtar/proprietary-files.txt`, and to any additional file F6.1-03 identified.
  - Output: The mirrored addition or additions.
- F6.1-06 — Verify by re-measurement
  - Description: Re-run the count that previously returned zero and confirm it now returns the expected number in each file.
  - Output: Updated counts.
- F6.1-07 — Record the unverified status
  - Description: State explicitly that the entry's effect is unverified until a build includes it, so nobody reads the change as a proven fix.
  - Output: A status note carried into Faz 6.2 and Phase 7.
- F6.1-08 — Update the continuity artifacts
  - Description: Update `EV-11` to reflect the change and `TRACE-14` to show the defect addressed but unverified.
  - Output: Two updated rows.

## 8. Acceptance Criteria

- The entry syntax is derived from tooling or from a comparable existing entry, with the source cited — not assumed.
- The source and target paths match what `ishtar-aon-fix/post-fs-data.sh` creates.
- The tree scope decision states definitively which files need the entry and why the others do not.
- `device_ishtar/proprietary-files.txt` carries the entry.
- `refs/a16_ishtar/proprietary-files.txt` carries the mirrored entry.
- The count that previously returned zero now returns the expected value in each changed file.
- The unverified status is recorded explicitly, so the change is not treated as a proven fix.
- `EV-11` and `TRACE-14` are updated.
- No other line in either file is changed.

## 9. Validation and Test Approach

Validation is entirely static and document-level, and the sub-phase is explicit that this is a limitation rather than a completeness. The change is correct by construction and unproven by measurement until a build exists.

- `VAL-GREP` (proposed) — the count that previously returned zero, re-run against both files, confirming the entry is present.
- `VAL-DIFF` (proposed) — a diff of each changed file confirming exactly one line added and nothing else modified. Version control from Faz 1.1 makes this trivial and is a direct payoff of that sub-phase.
- `VAL-DOCS` (proposed) — read back the entry form with its cited source, the path pair, and the unverified status note.

Local versus live: entirely local, with the live dimension explicitly deferred to Phase 7. This asymmetry should be stated rather than glossed, because a change that cannot be verified is a different kind of deliverable from one that can.

Security validation is not applicable. Ontology validation applies to `ARC-06` and to the AON chain vocabulary in Project-Ontology section 2.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| device_ishtar/proprietary-files.txt | modified | The current device tree gains the missing symlink declaration. | VAL-GREP, VAL-DIFF |
| refs/a16_ishtar/proprietary-files.txt | modified | The Android 16 device tree gains the mirrored declaration. | VAL-GREP, VAL-DIFF |
| ishtar-aon-fix/post-fs-data.sh | existing | Authoritative source for the exact path the build must produce. | VAL-DOCS |
| Planner-docs/Project-Comprehension.md | modified | Update `EV-11` and `TRACE-14` to reflect the change and its unverified status. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 1.1 for version control, which makes the one-line diff verifiable and reversible. This is a weak dependency in principle and a strong one in practice: a one-line change to a file nobody has a baseline for is not obviously a one-line change.

Benefits from Faz 1.6's reference index, which resolves which `refs/` trees are build inputs rather than comparison sources — a question F6.1-03 must answer.

Does not depend on Phases 2 through 5 at all. Both Main-Planing and Autopsy recommend scheduling it early, out of numbered order.

Blocks Faz 6.2's disposition decision, which needs the entry to exist before the module's future can be decided.

Feeds Phase 7, which is where the change finally gets verified.

Required decisions: none. The syntax and paths are derivable.

Required credentials, infrastructure, live endpoints, or human approvals: none.

Fresh session token and context risk: low. Two one-line edits and a syntax derivation.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the entry syntax is wrong and the build silently ignores it. Impact: the defect persists and everyone believes it is fixed, which is worse than a known gap. Mitigation: F6.1-01 derives the syntax from tooling or a comparable entry rather than assuming it, and F6.1-07 records the change as unverified until a build proves it.
- Risk (`AUTOPSY-P1-04` residual): the change is made to the current tree but not mirrored to the Android 16 tree. Impact: the Android 16 track inherits the defect, which is precisely the impact the finding names. Mitigation: both files are named in the acceptance criteria and both are re-measured.
- Risk: the target path is taken from documentation rather than from the working module. Impact: the build creates a path the blob does not read. Mitigation: F6.1-02 reads `post-fs-data.sh`, which is the only artifact known to work.
- Risk: the platform tree also needs the entry and is missed. Impact: a partial fix that appears complete. Mitigation: F6.1-03 makes tree scope an explicit determination rather than an assumption.
- Risk: the change is recorded as closing the AON defect. Impact: `ARC-06` is marked convergent on the strength of an unverified edit. Mitigation: `TRACE-14` is updated to "addressed but unverified" rather than resolved, and the status note travels to Phase 7.
- Risk: the edit disturbs the file's ordering or grouping conventions. Impact: a merge conflict or an extraction failure for unrelated entries. Mitigation: F6.1-04 follows existing conventions and `VAL-DIFF` confirms exactly one line changed.
- Risk: the sub-phase is deferred because Phase 6 sits after five other phases in the numbered order. Impact: every build made in the meantime inherits a one-line defect. Mitigation: both Main-Planing and Autopsy recommend early scheduling, and the dependency section states it has no upstream blockers beyond version control.

## 12. Desired End State

Both device trees carry the missing symlink declaration, derived from a cited source rather than assumed, matching the path the working runtime module creates. The counts that previously returned zero now return the expected value. The change is explicitly marked unverified pending a build, and the continuity artifacts reflect both the change and its unproven status.

The evidence an implementer should produce is the cited syntax source, the path pair, the tree scope determination, the two re-measured counts, and the one-line diffs.

The ledger summary Step 4 should append records: which files were changed, the entry form and its source, the tree scope decision, and the explicit note that verification awaits Phase 7.

## 13. Next Sub-Phase Transition Criteria

- Both target files carry the entry and their counts have changed from zero.
- The syntax source is cited, not assumed.
- The tree scope determination is definitive.
- Each diff shows exactly one line added.
- The unverified status is recorded and travels to Faz 6.2 and Phase 7.
- `EV-11` and `TRACE-14` reflect the change without overstating it.
