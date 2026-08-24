# Faz 4.3 — Patch Table Consolidation and Relocation

## 1. Context

Main-Planing Phase 4's desired end state names this work: "A patch table of minimal size, with matching duration rows, folded into `ishtar-cam-modes/blobs/hal-fullres.patch` or a clearly separated successor."

Autopsy supplies the second half of the requirement — location. Section 3 records the boundary issue under Area 3: "`hal-raw50-deneme.patch` is a HAL-layer artifact living in an application-layer directory. Understandable while experimental; it must move to `ishtar-cam-modes/blobs/` when it stabilizes, or its location will mislead a future reader." Section 5 repeats it and section 12 makes it an acceptance criterion: "Make relocating `hal-raw50-deneme.patch` out of `agc-50mp-yama/` an acceptance criterion."

Project-Comprehension records it as architectural drift, `ARC-07`: "Application-layer patches live in `agc-50mp-yama` — True, except `hal-raw50-deneme.patch` (a HAL artifact) lives there", status `divergent`. The reading of the drift in that section is worth keeping in view: "each is a reasonable in-the-moment choice … The pattern is that structure has lagged behind capability."

By the time this sub-phase runs, three experimental tables exist: the original four-instruction range widening, the `pixelArraySize` entry from Faz 3.3, and the narrowing plus duration rows from Faz 4.1 and Faz 4.2. They chain from one another, and a chain of three experimental tables in two directories is not a shippable artifact.

## 2. Goal

Consolidate the proven experimental patch entries into a single canonical, correctly located patch table with accurate checksums, so the 50 MP capability is expressed as one shippable artifact rather than a chain of experiments across two directories.

## 3. Description

The problem is that experimentation produces chained artifacts and shipping requires a single one. The chaining is not incidental: `agc-50mp-yama/hal-raw50-deneme.patch` records `temel: fullres md5 fe0245a4720fb07b01d96deef47f5569`, meaning it applies to the output of `hal-fullres.patch` rather than to stock. Each additional experiment extends that chain, and each link is a state the module's checksum classifier does not recognize.

It belongs after the narrowing and the duration rows because consolidating an unfinished patch would mean consolidating twice.

The vibecoding slice strategy: decide the structure first — one table from stock, or a canonical base plus one successor — then rebuild the entries against that decision, then verify by checksum. The fastest validation signal is that applying the consolidated table to a stock binary produces the recorded result checksum, which is the format's own self-verification working as designed.

What should not be over-planned: a general patch composition mechanism. The project has one binary and two logical states, and the format contract from Faz 1.3 already covers what an extension may look like.

The structural decision is genuine and has consequences. A single table from stock is simpler to reason about and to verify, but it merges the 50 MP HAL capability with the full-resolution capability that already ships — and those are currently separable, which matters because `halpatch.sh` treats `fullres` and `stock` as the only two recognized states. A canonical base plus a successor preserves separability at the cost of a chain. The decision should be made against how `setmode.sh` dispatches modes, not in the abstract.

The checksum constants are the practical constraint. `halpatch.sh` hard-codes `HAL_STOCK_MD5` and `HAL_FULLRES_MD5` and classifies anything else as `unknown`, which triggers a re-seed. A consolidated table producing a third state requires that classifier to learn a third value, and Faz 1.3's contract already asked which copy of these constants is authoritative. This sub-phase is where that answer is used.

## 4. Scope

- The structural decision: one table from stock, or a canonical table plus a clearly separated successor.
- Rebuilding the proven entries — the narrowed emission, the duration rows, and the `pixelArraySize` change — into the chosen structure.
- Recomputing and recording accurate base and result checksums for the consolidated table.
- Relocating the artifact out of `agc-50mp-yama/` into `ishtar-cam-modes/blobs/`, closing `ARC-07`.
- Extending the checksum classifier in `halpatch.sh` to recognize the new state, so a correctly patched copy is not classified as damaged.
- Verification by application: applying the consolidated table to a stock binary produces the recorded result checksum.
- Updating the format contract from Faz 1.3 in the same slice, since Faz 1.3's risk section requires it.
- Removing or clearly marking the superseded experimental tables so no future reader applies a stale chain.

## 5. Out of Scope

- Changing which formats, resolutions, or duration values the patch carries. Those were settled in Faz 4.1 and Faz 4.2.
- The consumer compatibility validation, which is Faz 4.4.
- Any change to the sensor layer, the blobs, or the mode dispatch beyond the checksum classifier extension.
- Building a release archive, which is Faz 9.1.
- Changing how `setmode.sh` decides between layers, or altering the exclusion rule.
- Redesigning the patch format. The contract governs; this sub-phase applies it.
- Removing `agc-50mp-yama/` itself, which still holds the smali sources and remains an application-layer directory.

## 6. Current Repository Evidence

`ishtar-cam-modes/blobs/hal-fullres.patch` was read in this run. It carries 16 entries, a header describing the four-byte index format, and three recorded facts: `stok md5 c3fa63a86ee3ecaf9fbf02005d35f6b5`, `fullres md5 fe0245a4720fb07b01d96deef47f5569`, and `nokta 16`. This is the canonical table and the model the consolidated artifact should follow.

`agc-50mp-yama/hal-raw50-deneme.patch` was read in this run. It carries four entries and records `temel: fullres md5 fe0245a4720fb07b01d96deef47f5569` and `sonuc: md5 8d0915ce520fadaf092d31ed675aa98a`. It is explicitly named as an experiment and its header states that the patch alone is insufficient and needs narrowing. Both statements will be false of the consolidated artifact, which is one reason the experimental file should not simply be renamed.

`ishtar-cam-modes/halpatch.sh` was read in full in this run. `HAL_STOCK_MD5` and `HAL_FULLRES_MD5` are script constants. `hal_state` returns `fullres`, `stock`, or `unknown` by comparing against exactly those two values. `hal_set` accepts an argument of `fullres` or `stock` and selects `WANT_MD5` accordingly with a two-branch test. `hal_write` selects the stock or patched column by comparing its argument to `fullres`. Every one of these is a two-state assumption, and a third state requires touching all of them.

`ishtar-cam-modes/customize.sh` also carries both checksums, in its HAL classification block with three branches: stock, fullres, and unrecognized. A third state requires a fourth branch here or a redefinition of what fullres means.

`ishtar-cam-modes/setmode.sh` sets `HAL_WANT` and passes it to `hal_set` inside `restart_camera`, and `post-fs-data.sh` sets `HAL_WANT=stock` for the nine sensor modes and the full-resolution state for `50mp`. The dispatch is two-valued throughout.

This concentration of two-state assumptions is the strongest argument for the single-table structure: redefining `fullres` to mean the complete 50 MP capability changes one constant and no control flow, whereas adding a third state touches at least four files.

Project-Comprehension `ARC-05` records that patch tables are self-verifying with the checksum of both input and output recorded, status `convergent` — a property the consolidation must preserve.

## 7. Planned Work Breakdown

- F4.3-01 — Make the structural decision
  - Description: Choose between a single table from stock and a canonical base plus successor, evaluated against the two-state assumptions in `halpatch.sh`, `customize.sh`, `setmode.sh`, and `post-fs-data.sh`. Record the reasoning and the file count each option touches.
  - Output: A structural decision with its consequences enumerated.
- F4.3-02 — Rebuild the entries into the chosen structure
  - Description: Assemble the proven entries from the three experimental tables into the target structure, respecting the four-byte index convention and the format contract's extension rules.
  - Output: The consolidated table.
- F4.3-03 — Recompute and record the checksums
  - Description: Apply the consolidated table to a stock binary copy, compute the result checksum, and record both base and result in the table header per the format's convention.
  - Output: A table with verified checksums.
- F4.3-04 — Relocate the artifact
  - Description: Place the consolidated table under `ishtar-cam-modes/blobs/`, closing `ARC-07`.
  - Output: A correctly located artifact.
- F4.3-05 — Extend the checksum classifier
  - Description: Update `halpatch.sh` so a correctly patched copy is recognized rather than classified as unknown and re-seeded. Apply the same update to `customize.sh`'s classification block, and to any other two-state assumption the F4.3-01 analysis identified.
  - Output: Updated classification across the affected files.
- F4.3-06 — Verify by application
  - Description: Apply the consolidated table from stock and confirm the resulting checksum matches the recorded value, then confirm `hal_state` reports the intended state rather than unknown.
  - Output: A round-trip verification.
- F4.3-07 — Update the format contract
  - Description: Update the Faz 1.3 contract in this same slice, per its own risk mitigation, recording the new table's structure and any convention the consolidation established.
  - Output: An updated format contract.
- F4.3-08 — Retire the superseded experiments
  - Description: Remove or clearly mark the superseded experimental tables so no future reader applies a stale chain. Marking is preferable to deletion if the experiments carry findings the journal does not.
  - Output: Retired or marked experimental artifacts.

## 8. Acceptance Criteria

- The structural decision is recorded with the file count and control-flow impact of each option.
- The consolidated table carries every proven entry from the three experimental tables and no unproven ones.
- Base and result checksums are recomputed by application, not transcribed.
- Applying the consolidated table from a stock binary reproduces the recorded result checksum.
- The artifact resides under `ishtar-cam-modes/blobs/`, and `ARC-07` in Project-Comprehension is updated from `divergent`.
- `hal_state` reports the intended state for a correctly patched copy rather than `unknown`.
- Every file the F4.3-01 analysis identified as carrying a two-state assumption has been updated or explicitly determined not to need updating.
- The format contract is updated in the same slice as the table change.
- Superseded experimental tables are removed or marked so a stale chain cannot be applied by accident.
- The array entry count and duration rows from Faz 4.1 and Faz 4.2 are unchanged by the consolidation.

## 9. Validation and Test Approach

Validation is predominantly local and checksum-driven, with one live confirmation. This is the sub-phase where the patch format's self-verifying property does most of the work.

- `VAL-CHECKSUM` (proposed) — apply the consolidated table to a stock binary copy on the host or the device and confirm the result matches the recorded checksum. This is the format's own guarantee exercised.
- `VAL-CLASSIFY` (proposed) — confirm `hal_state` reports the intended state, and that `customize.sh`'s classification block does not report the patched copy as unrecognized.
- `VAL-SMOKE` (from Faz 2.1) — a live confirmation that the consolidated patch produces the same array entry count and duration rows as the chain it replaces.
- `VAL-DOCS` (proposed) — read back the updated format contract and confirm it describes the new structure.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist for the live confirmation.

Local versus live: consolidation and checksum verification are local; the equivalence confirmation is live. Security validation is not applicable. Ontology validation applies to `ARC-07` and to keeping the `fullres` HAL state distinct from the `50mp` mode name, which becomes more important if the structural decision redefines what `fullres` means.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/blobs/hal-fullres.patch | modified | The canonical table, extended or superseded per the structural decision. | VAL-CHECKSUM, VAL-SMOKE |
| agc-50mp-yama/hal-raw50-deneme.patch | deferred | Superseded experimental table; retired or marked rather than carried forward. | VAL-DOCS |
| ishtar-cam-modes/halpatch.sh | modified | Checksum classifier extended to recognize the consolidated state. | VAL-CLASSIFY |
| ishtar-cam-modes/customize.sh | modified | Install-time HAL classification block updated for the new state. | VAL-CLASSIFY |
| docs/patch-table-format.md | modified | Contract updated in the same slice as the table change. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 4.1 and Faz 4.2 for a complete, proven entry set, on Faz 3.3 for the `pixelArraySize` entry, and on Faz 1.3 for the format contract that governs the structure.

Blocks Faz 4.4, which validates the consolidated artifact rather than the experimental chain. Blocks Faz 9.1, since a release build script needs one artifact to package.

Required decisions: the structural choice in F4.3-01. It is a technical judgment with a clear evaluation criterion — the number of files and control-flow branches each option touches — so the implementer can decide and record it.

Required infrastructure: a stock binary copy for the checksum verification, plus the device for the live equivalence confirmation.

Required human approvals: HAL patching and camera use for the live confirmation.

Fresh session token and context risk: low to medium. No new disassembly; this is assembly of already-derived entries plus small script edits.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: a third HAL state is introduced and only `halpatch.sh` is updated. Impact: `customize.sh` reports the state as unrecognized at install and disables 50 MP, or `post-fs-data.sh` fails to reapply it at boot. Mitigation: F4.3-01 enumerates every file carrying a two-state assumption, and the acceptance criteria require each to be updated or explicitly cleared.
- Risk (`ARC-07` residual): the table is renamed in place rather than relocated. Impact: the boundary violation persists under a new name and Autopsy's acceptance criterion is not met. Mitigation: F4.3-04 requires the destination directory explicitly.
- Risk: checksums are transcribed from the experimental tables rather than recomputed. Impact: the self-verifying property becomes self-referential and a mismatch goes undetected. Mitigation: F4.3-03 and `VAL-CHECKSUM` both require application-derived values.
- Risk: the consolidated patch is not equivalent to the chain it replaces. Impact: a working configuration is silently altered during a step meant to be purely structural. Mitigation: `VAL-SMOKE` compares array entry count and duration rows against the pre-consolidation state.
- Risk: the superseded experimental tables are left in place unmarked. Impact: a future session applies a stale chain and produces an unrecognized state. Mitigation: F4.3-08 requires removal or marking, with marking preferred where the file carries findings.
- Risk: the format contract is not updated and diverges immediately. Impact: exactly the failure Faz 1.3's risk section predicts. Mitigation: F4.3-07 is a work item and the acceptance criteria require same-slice updating.
- Risk: redefining `fullres` to mean the complete capability makes the term ambiguous against its ontology definition. Impact: vocabulary drift in a project whose ontology exists to prevent it. Mitigation: whichever structure is chosen, Project-Ontology section 2's entry for `fullres` is updated in the same slice.

## 12. Desired End State

The 50 MP HAL capability is one canonical patch table, correctly located under `ishtar-cam-modes/blobs/`, with checksums recomputed by application, recognized by the module's classifier, and equivalent to the experimental chain it replaces. Every two-state assumption in the module has been addressed. The format contract describes the result, and the superseded experiments cannot be applied by accident.

The evidence an implementer should produce is the structural decision record, the round-trip checksum verification, the classifier confirmation, and the live equivalence comparison.

The ledger summary Step 4 should append records: the structure chosen, the files touched, the recorded checksums, the `ARC-07` closure, and confirmation that the consolidated patch is equivalent to the chain.

## 13. Next Sub-Phase Transition Criteria

- The consolidated table reproduces its recorded checksum when applied from stock.
- The module's classifier recognizes the patched state rather than re-seeding it.
- Every two-state assumption identified in F4.3-01 is resolved.
- The artifact is located under `ishtar-cam-modes/blobs/` and `ARC-07` is updated.
- The format contract and the ontology vocabulary entry are updated in the same slice.
- Superseded experimental tables are retired or marked.
- Faz 4.4 has one artifact to validate rather than a chain.
