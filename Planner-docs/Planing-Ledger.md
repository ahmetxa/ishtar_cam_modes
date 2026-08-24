# Planing Ledger

> Ledger v2 — ClaudeQB. Created by Step 2. Body language: English (default contract).

## 1. Purpose

This ledger is the durable record of planning and implementation continuity for `ishtar`. It exists so that a replanning run or a Step 4 implementation session can determine what was planned, what was applied, what was verified, and what remains blocked, without reconstructing that history from a conversation.

It is supporting evidence, not absolute truth. Where this ledger and the current repository state disagree, the repository wins and the ledger is corrected. Step 4 appends concise implementation summaries after verified slices or stop events; Step 2 and Step 3 update planning state.

The project's own history is the reason this file matters. Autopsy `AUTOPSY-P0-02` records a three-step misattribution caused by state not being captured before and after changes, and Project-Comprehension `QAS-03` records that findings deferred to later in a session are the ones lost to context truncation. A ledger that is written during work rather than after it is the countermeasure.

## 2. Planning Runs

| Run | Step | Date | Artifacts written | Outcome |
|---|---|---|---|---|
| 1 | Step 1 — First-Planner | 2026-08-23 | `Planner-docs/Main-Planing.md` | Completed. Nine-phase master roadmap produced from repository evidence and standing project history. |
| 2 | Step 1.5 — Autopsy-Planner | 2026-08-23 | `Planner-docs/Autopsy.md`, `Planner-docs/Project-Ontology.md`, `Planner-docs/Project-Comprehension.md` | Completed. Existing-project autopsy with thirteen priority findings, a durable ontology including the reverse-engineering address book, and an evidence-and-confidence comprehension model. |
| 3 | Step 2 — Second-Planner | 2026-08-24 | `Planner-docs/Sub-Planing-Index.md`, 32 sub-plan files across nine phase folders, this ledger | Completed. All nine phases decomposed. Bundled validator unavailable — no Python interpreter on the host — so equivalent all-file validation was performed and is reported as a fallback. |

Prior ClaudeQB history before run 1: none. `Planner-docs/` did not exist, so there was no ledger, ontology, or comprehension artifact to reconcile against.

## 3. Plan Snapshot Registry

| Snapshot ID | Source | Date | Phase count | Sub-plan count | Notes |
|---|---|---|---|---|---|
| SNAP-2026-08-23-MAIN | `Planner-docs/Main-Planing.md` | 2026-08-23 | 9 | not applicable | The master roadmap. Phase order is fixed by this snapshot and is not renumbered by Step 2. |
| SNAP-2026-08-23-AUTOPSY | `Planner-docs/Autopsy.md` | 2026-08-23 | not applicable | not applicable | Thirteen priority findings from `AUTOPSY-P0-01` through `AUTOPSY-P3-03`, treated as Step 2 feedback. |
| SNAP-2026-08-24-SUBPLANS | `Planner-docs/Sub-Planing-Index.md` and the nine phase folders | 2026-08-24 | 9 | 32 | The active sub-plan snapshot. Step 4 runs execute against this. If `Main-Planing.md` changes, this snapshot is superseded and replanning is required before further implementation. |

The active snapshot is `SNAP-2026-08-24-SUBPLANS`. Every row in section 4 belongs to it.

## 4. Sub-Plan Status Matrix

| Sub-plan Path | Status | Snapshot ID | Run ID | Validation Evidence | Blocker | Next Action | Superseded By | Updated At |
|---|---|---|---|---|---|---|---|---|
| Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Measure directory sizes, write ignore rules including the keystore, initialize, commit. | - | 2026-08-24 |
| Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Audit the five release archives by entry name; resolve OQ-09. | - | 2026-08-24 |
| Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Transcribe the grammar from halpatch.sh and round-trip three records. | - | 2026-08-24 |
| Planner-docs/Faz-1-Plans/Faz1.4-toolchain-procedure-record.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Write the ordered procedure and run both self-checks. | - | 2026-08-24 |
| Planner-docs/Faz-1-Plans/Faz1.5-static-safety-probes.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Close OQ-05, OQ-06, OQ-07, OQ-08, CQ-11, CQ-12 in one static batch. | - | 2026-08-24 |
| Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Write the root README, the refs index, and the artifact manifest. | - | 2026-08-24 |
| Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Build the read-only state reporter; prove idempotence and sensitivity. | - | 2026-08-24 |
| Planner-docs/Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Verify the archive, flash, and capture the named baseline. | - | 2026-08-24 |
| Planner-docs/Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Run all ten modes and produce the first written regression record. | - | 2026-08-24 |
| Planner-docs/Faz-2-Plans/Faz2.4-tiles-hide-disposition.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Bounded investigation, then decide repair, remove, or label. | - | 2026-08-24 |
| Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Clear the trap keys, confirm four preconditions, set the attempt budget. | - | 2026-08-24 |
| Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Classify nine references, trace six dwords, produce a ranked candidate list. | - | 2026-08-24 |
| Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Patch one word, read the three array tags, demonstrate reversal. | - | 2026-08-24 |
| Planner-docs/Faz-3-Plans/Faz3.4-consumer-compatibility-check.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Survey the stock camera, Open Camera, and the video path; answer OQ-03. | - | 2026-08-24 |
| Planner-docs/Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Attempt the capture; determine the colour filter pattern for OQ-02. | - | 2026-08-24 |
| Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Close the phase by decision; hand Phase 4 a preservation requirement. | - | 2026-08-24 |
| Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | State the array count target, guard one site, then extend. | - | 2026-08-24 |
| Planner-docs/Faz-4-Plans/Faz4.2-duration-rows.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Locate the two duration tables and add justified rows. | - | 2026-08-24 |
| Planner-docs/Faz-4-Plans/Faz4.3-patch-table-consolidation.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Decide the structure, consolidate, relocate, extend the classifier. | - | 2026-08-24 |
| Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Validate the consolidated artifact; report the array count as a number. | - | 2026-08-24 |
| Planner-docs/Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Generate the candidate and verify it host-side with the existing harness. | - | 2026-08-24 |
| Planner-docs/Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Mount temporarily, test composition, answer OQ-04, restore. | - | 2026-08-24 |
| Planner-docs/Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Enumerate enforcement points, then remove or retain the exclusion. | - | 2026-08-24 |
| Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Add the entry to both trees; record it as unverified pending a build. | - | 2026-08-24 |
| Planner-docs/Faz-6-Plans/Faz6.2-aon-module-disposition.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Decide the module role; register the verification against Phase 7. | - | 2026-08-24 |
| Planner-docs/Faz-7-Plans/Faz7.1-wsl2-provisioning.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Provision the Linux environment; verify with a kernel configuration step. | - | 2026-08-24 |
| Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Set a stopping rule, attempt the build, run the registered AON check. | - | 2026-08-24 |
| Planner-docs/Faz-8-Plans/Faz8.1-beryl-port-sizing.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Acquire a reference tree and produce the three-part cost estimate. | - | 2026-08-24 |
| Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Identify the bases and assess the camera-path conflict surface. | - | 2026-08-24 |
| Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Write the build script with packaging assertions proven to fail. | - | 2026-08-24 |
| Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Map capabilities to proving commands; demonstrate known-bad detection. | - | 2026-08-24 |
| Planner-docs/Faz-9-Plans/Faz9.3-documentation-consolidation.md | planned | SNAP-2026-08-24-SUBPLANS | - | - | - | Correct the stale claim everywhere; relocate the changelog. | - | 2026-08-24 |

## 5. Implementation Runs

No implementation run has occurred. Step 4 has not been invoked for this project, and no sub-plan has moved beyond `planned`.

When Step 4 runs, each verified slice or stop event appends a row here recording the sub-plan path, the slice performed, the validation evidence produced, and the resulting status change in section 4.

Two recording rules apply and both come from the project's own history rather than from convention. Every located binary address is written into `Planner-docs/Project-Ontology.md` during the session it is found, per Main-Planing risk `R10` and Project-Comprehension `QAS-03`. Every probe that resolves updates the confidence column in `Planner-docs/Project-Comprehension.md` and the corresponding question status in `Planner-docs/Project-Ontology.md` in the same session, per the recording rule stated in that document's section 8.

## 6. Current State Snapshot

**Repository.** Not under version control. `git status --short` and `git branch --show-current` both fail at the workspace root, re-confirmed during the Step 2 run. This is `AUTOPSY-P0-01` and is the first item in the execution order.

**Deliverables.** Three module directories exist: `ishtar-cam-modes/` at version v2.1 with versionCode 12, `ishtar-aon-fix/` at v1.1, and `agc-50mp-yama/` holding two smali sources and one experimental HAL patch table. Five release archives sit at the workspace root, none audited for the signing keystore.

**Device state.** Unknown to planning. The workspace `mode` file contains `stock`, but no ClaudeQB run has queried the device, so `EV-19` remains `tentative`. `ishtar-cam-modes-v2.1.zip` is recorded as built and never flashed, `EV-14`, confidence `probable`.

**Camera modification state.** The 16-point full-resolution HAL patch is the shipped capability. The four-instruction experimental RAW patch and the patched AGC build are both recorded as currently reverted on the device. The `pixelArraySize` write site is not located. The libgcam static-metadata invariant is the standing blocker for a capture inside the AGC port.

**Validation surface.** None exists. No test framework, no CI, no smoke script, `EV-02`, confidence `confirmed`. The one host-side verifier is `ishtar-cam-modes/tools/verify_ln.py`, which validates generated sensor blobs.

**Build environment.** Neither the kernel nor a ROM can be built on this host. WSL2 is not installed, `EV-20`, confidence `probable`. Disk is not a constraint at 799 GB free on the Windows volume as of 2026-08-23. No Python interpreter is available through the normal path, measured during the Step 2 run.

**Open ontology questions at the close of Step 2.** `OQ-01` through `OQ-11` are open or partially answered, and `OQ-12` is partially answered. `OQ-13` through `OQ-16` are answered. Each open question is routed to a named sub-plan.

**Open hypotheses.** `H-01` through `H-10` are all `tentative`. None is used as a premise in any sub-plan; each is routed to the sub-plan that tests it.

## 7. Replanning Inputs

Replanning is required if any of the following changes:

- `Planner-docs/Main-Planing.md` is edited. The active sub-plan snapshot is derived from it, and a changed master plan supersedes `SNAP-2026-08-24-SUBPLANS`.
- The Phase 3 outcome recorded by `Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md` selects a fallback rather than the primary path. That gate may revise the target end state, which changes what Phase 9 claims and verifies.
- The Phase 5 priority decision, routed to the user by the same gate, defers or cancels Phase 5.
- The Phase 7 build outcome recorded by `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md` shows the Android 16 track is not viable, which removes the precondition for both Phase 8 sub-plans.
- Either Phase 8 commit decision is taken, since neither the beryl port nor the kernel merge is decomposed beyond scoping.
- The vendor blobs change through a system update. Project-Ontology invariant 10 records that every patch offset is bound to one exact build and that a change invalidates all of them at once; the checksum guard is the detector.
- The signing key audit in `Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md` returns a dirty result, which raises a rotation decision and blocks the version control remote question.

Inputs that do not require replanning: routine sub-plan completion, question and hypothesis resolution, and address book growth. Those are recorded in sections 4 and 5 and in the continuity artifacts.

## 8. Open Decisions and Follow-Ups

| ID | Decision | Owner | Raised by | Blocks | Status |
|---|---|---|---|---|---|
| DEC-01 | Whether version control stays local-only or gains a remote. A remote changes what may be committed, because the AGC port redistribution question becomes live once history leaves the machine. | User | Main-Planing section 9; `Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md` | Publishing history | Open. Gated on the DEC-05 audit result. |
| DEC-02 | The `tiles hide` option's disposition: repair, remove, or label as a known limitation. Removal is the recommended default because an absent control is better than one that silently does nothing. | User | Main-Planing prioritized step 10; `Planner-docs/Faz-2-Plans/Faz2.4-tiles-hide-disposition.md` | Nothing; it is the one Phase 2 item Phase 3 does not depend on | Open. |
| DEC-03 | Whether Phase 5 retains its priority given how much Phase 3 has grown. | User | Main-Planing section 9; routed by `Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md` | Phase 5 scheduling | Open. Decided at the Phase 3 gate. |
| DEC-04 | Whether the AON module merges into `ishtar-cam-modes` or stays a separate artifact, preserving its deliberate independence from module mounting. | User | Main-Planing section 9; `Planner-docs/Faz-6-Plans/Faz6.2-aon-module-disposition.md` | Release contents in Phase 9 | Open. |
| DEC-05 | Whether the signing keystore appears in any already-released archive, and if so whether to rotate the key and withdraw the affected releases. | User, on the audit result | `AUTOPSY-P1-01`; `Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md` | DEC-01 | Open. The audit itself is planned work, not a decision. |
| DEC-06 | The attempt budget for the Phase 3 write-site search, expressed as a number with its unit before the search begins. | User | `AUTOPSY-P1-03`; set in `Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md` | All Phase 3 measurement work | Open. Must be set before `Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md` starts. |
| DEC-07 | Whether to commit to the beryl port, given the three-part cost estimate and particularly the patch re-derivation cost if the HAL binary differs. | User | `Planner-docs/Faz-8-Plans/Faz8.1-beryl-port-sizing.md` | Any beryl work | Open. Gated on Phase 7's outcome. |
| DEC-08 | Whether to commit to the kernel LTS merge, given its conflict surface in the camera and sensor subsystems and the finding on the CSIPHY and CSID allocation paths that invariant 3 depends on. | User | `Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md` | Any merge work | Open. Gated on Phase 7's outcome. |
| DEC-09 | Whether a duration value chosen in Phase 4 that would move an entry between the framework's two size lists is the intended behavior, since it changes AGC's behavior without touching AGC. | User | `Planner-docs/Faz-4-Plans/Faz4.2-duration-rows.md` | The duration row values | Open. Raised only if the chosen values cross the bucketing threshold. |

Follow-ups that are planned work rather than decisions: the tile application's Java sources have never been read by any ClaudeQB run, which leaves the tile-exclusivity mechanism unknown and is a stated gap in `Planner-docs/Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md`; and `ishtar-cam-modes/Kullanim.txt` has never been read, which is why it appears in the stale-claim search scope of `Planner-docs/Faz-9-Plans/Faz9.3-documentation-consolidation.md`.
