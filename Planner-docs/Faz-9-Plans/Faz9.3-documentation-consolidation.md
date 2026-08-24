# Faz 9.3 — Documentation Consolidation and Stale Claim Correction

## 1. Context

Main-Planing Phase 9 includes a documentation item: "Move the changelog out of `module.prop` `description` and into the journal or a `CHANGELOG.md`." Section 5 states the principle behind it: "`module.prop` `description` should stop being a second changelog — the journal owns history."

Autopsy raises three related findings that belong together. `AUTOPSY-P3-01` records the duplication: "an approximately 1,600-character `description` field carries the full v1.2→v2.1 history in a field meant for a module summary; it will diverge from the journal." `AUTOPSY-P2-03` records the correctness problem: "journal Faz 8 concludes AGC cannot exceed 15.2 MP; Faz 11 and 12 disprove it. `module.prop` v2.0 repeats the disproven causal claim. A future reader, including a future agent session, will act on stale conclusions." Autopsy's cross-cutting feedback adds: "Mark superseded conclusions in `50MP-Entegrasyon-Plani.md` (Faz 8's AGC ceiling) and correct the stale causal claim in `module.prop` v2.0's description."

Project-Comprehension `EV-23` records the stale claim as `contradicted` — the only row in that register with that confidence value — and `ARC-10` records "History lives in the journal — Duplicated into `module.prop` `description`" as `divergent`.

By this point Phase 3 has acted on the very conclusion the stale text denies, which makes the correction more than tidiness: the shipped module describes a limitation the project has spent a phase removing.

## 2. Goal

Consolidate the project's documentation so history lives in one place, superseded conclusions are marked rather than deleted, and the module's user-facing description states what is currently true.

## 3. Description

The problem is documentation that is unusually strong in content and weak in structure, with two specific consequences. History is duplicated between the journal and a module metadata field, which guarantees eventual divergence. And at least two places assert a conclusion the project has since disproved, which is worse than duplication because a future reader acts on it.

Autopsy section 6 names the second consequence's cost: "Neither is harmful today, but both will mislead." Project-Comprehension `QAS-03` describes the underlying quality attribute — knowledge durability — and notes that the ontology now satisfies it while the journal does not.

It belongs at the end of Phase 9 because the claims stop moving only after Phases 3, 4, and 5 settle, and because correcting a description before the capability it describes is final would mean correcting it twice.

The vibecoding slice strategy: correct the false claims first, because they actively mislead; then relocate the changelog, which is structural; then mark the journal's superseded sections. The fastest useful signal is that the description field no longer asserts something the project has disproved.

What should not be over-planned: restructuring the journal, adding a table of contents, or reorganizing its non-monotonic phase numbering. Autopsy notes the numbering drift as a signal worth reading rather than a defect worth fixing: "the 50 MP work grew beyond its original plan slot, which is worth noticing when scoping Phase 3."

Marking rather than deleting is the governing principle for the journal. Autopsy's cross-cutting item says "mark superseded, do not delete", and the reason is that the superseded reasoning is itself valuable — Project-Ontology's `OQ-13` and `OQ-14` are recorded as answered-negative precisely so the rejected hypotheses are not retested.

One decision from Main-Planing section 9 lands here: whether the AON module merges into `ishtar-cam-modes` or stays separate. Faz 6.2 makes that decision; this sub-phase reflects it in the documentation.

## 4. Scope

- Correction of the stale causal claim in `module.prop`'s description regarding the AGC resolution ceiling.
- Reduction of the description field to a module summary, with the changelog relocated.
- A changelog file carrying the version history that the description currently holds.
- Marking of superseded sections in `50MP-Entegrasyon-Plani.md`, without deleting them.
- A cross-reference from the journal to `Planner-docs/Project-Ontology.md` as the lookup surface, per that document's own stated purpose.
- Reflection of Faz 6.2's AON disposition in the user-facing documentation.
- Verification that the corrected description matches the capabilities Faz 9.2's checklist proves.
- Resolution of `ARC-10` and `EV-23`.

## 5. Out of Scope

- Restructuring the journal, adding a table of contents, or renumbering its phases.
- Deleting any superseded content.
- Translating the journal. The bilingual convention is deliberate per Main-Planing risk `R11`.
- The root README and reference index, which are Faz 1.6.
- The release checklist and recovery runbook, which are Faz 9.2.
- Any change to module behavior. Text only.
- Rewriting `Kullanim.txt` or the web interface strings beyond correcting a false claim if one appears there.
- Making the AON merge decision, which is Faz 6.2's.

## 6. Current Repository Evidence

`ishtar-cam-modes/module.prop` was read in full in this run. Its `description` field runs from the v1.2 entry through v2.1 in a single line and contains the stale claim verbatim within the v2.0 entry: it states that AGC remains at 12.6 to 15.2 MP because the GCam 8.4 engine cannot select the 50 MP stream. Project-Ontology invariant 7 records the actual cause — the framework's high-resolution bucket exclusion, where 8192x6144 measures 66,666,666 nanoseconds and is therefore omitted from the standard size list — and `OQ-15` records the same as answered.

The description also contains claims that remain true and should survive the reduction: `dcgB` measured at roughly 25% less noise and double the detail, the four mutually exclusive tiles, video at 1080p60 and 4K60 unaffected, and the 27 MB binary not being shipped.

`50MP-Entegrasyon-Plani.md` is roughly 1,300 lines with twelve phase sections plus a decisions section. Autopsy section 6 records its structural properties: no table of contents and non-monotonic phase numbering, with Faz 10 pending while Faz 11 and 12 are complete. Section 2 identifies the specific superseded section by its heading — the one concluding that AGC cannot exceed 15.2 MP.

`agc-50mp-yama/README.md` was read in this run and already states the correct explanation: it documents the `getOutputSizes` high-resolution exclusion with the measured frame durations in a table, and notes that `Forty8Strip` is an empty stub so the port's own mechanism is not the cause. This file is already correct and can serve as the source for the corrected description text rather than requiring fresh authoring.

Project-Comprehension `EV-23` is the only row in the evidence register marked `contradicted`, with the note "journal Faz 8 conclusion, superseded by EV-10".

`ishtar-cam-modes/Kullanim.txt` is a user-facing usage document that Step 1 catalogued but no ClaudeQB run has read. It may repeat the stale claim and should be checked.

`ishtar-cam-modes/webroot/index.html` was partially read in this run and contains user-facing mode descriptions in its translation tables. Whether any of them carries a stale claim was not determined.

`ishtar-aon-fix/module.prop` carries the AON module's own description, which Faz 6.2's disposition may change.

## 7. Planned Work Breakdown

- F9.3-01 — Locate every instance of the stale claim
  - Description: Search the user-facing documentation set — `module.prop`, `Kullanim.txt`, the web interface strings, and the journal — for the disproven causal statement. Correcting one instance while others persist is the failure mode to avoid.
  - Output: An instance list.
- F9.3-02 — Correct the claim using the existing correct text
  - Description: Replace the disproven cause with the correct one, drawing on `agc-50mp-yama/README.md`, which already states it accurately with measured values.
  - Output: Corrected text at every located instance.
- F9.3-03 — Reduce the description to a summary
  - Description: Rewrite `module.prop`'s description as what the field is for — a module summary — retaining the currently true capability statements and dropping the version history.
  - Output: A reduced description field.
- F9.3-04 — Create the changelog file
  - Description: Relocate the version history from the description into a dedicated changelog, preserving the entries as written since they record real measured findings.
  - Output: A changelog file.
- F9.3-05 — Mark the journal's superseded sections
  - Description: Add a marking to the section concluding the AGC ceiling, pointing forward to the sections that supersede it. Mark; do not delete.
  - Output: A marked superseded section.
- F9.3-06 — Add the ontology cross-reference
  - Description: Add a pointer from the journal to `Planner-docs/Project-Ontology.md` as the lookup surface, which is what that document states its own purpose to be.
  - Output: A cross-reference.
- F9.3-07 — Reflect the AON disposition
  - Description: Update the user-facing documentation to match Faz 6.2's decision on whether the AON module merges or stays separate.
  - Output: Documentation consistent with the disposition.
- F9.3-08 — Cross-check against the verification checklist
  - Description: Confirm every capability the corrected description claims has a proving command in Faz 9.2's checklist, and that the checklist contains no claim the description omits.
  - Output: A two-way consistency verdict.
- F9.3-09 — Resolve the documentation records
  - Description: Update `ARC-10` from `divergent` and record `EV-23`'s correction as propagated.
  - Output: Updated continuity artifacts.

## 8. Acceptance Criteria

- Every instance of the stale causal claim is located and corrected; the instance list shows the search covered all four documentation surfaces.
- The corrected text states the actual cause with its measured basis, drawn from the existing correct explanation rather than newly authored.
- `module.prop`'s description reads as a module summary and no longer carries the version history.
- Every currently true capability statement survives the reduction.
- A changelog file carries the relocated history with its entries preserved.
- The journal's superseded section is marked with a forward pointer and its content is intact.
- The journal carries a cross-reference to the ontology as the lookup surface.
- The AON disposition is reflected consistently in the user-facing documentation.
- The two-way consistency check between the description and Faz 9.2's checklist passes in both directions.
- `ARC-10` is updated from `divergent` and `EV-23` is recorded as propagated.

## 9. Validation and Test Approach

Validation is document-level and consistency-driven. The distinguishing check is bidirectional: a description claiming something the checklist cannot prove is as much a defect as a checklist proving something the description does not claim.

- `VAL-INSTANCES` (proposed) — the stale-claim search across all four surfaces, with the result showing coverage rather than a single hit.
- `VAL-CONSISTENCY` (proposed) — the two-way check between the corrected description and Faz 9.2's capability list.
- `VAL-PRESERVE` (proposed) — confirmation that the journal's superseded content is intact and that the changelog's relocated entries match what the description held.
- `VAL-DOCS` (proposed) — read back the reduced description, the changelog, and the cross-reference.
- `VAL-INSTALL` (proposed) — a module install showing the reduced description rendering correctly in the module list, since the field's display is its purpose.

Local versus live: almost entirely local, with one live check that the reduced description renders as intended. Security validation is not applicable. Ontology validation applies to invariant 7, whose mechanism the corrected text must state accurately, and to `ARC-10`.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/module.prop | modified | Description reduced to a summary with the stale claim corrected. | VAL-INSTANCES, VAL-CONSISTENCY, VAL-INSTALL |
| CHANGELOG.md | proposed | The relocated version history. | VAL-PRESERVE, VAL-DOCS |
| 50MP-Entegrasyon-Plani.md | modified | Superseded section marked with a forward pointer; content preserved. | VAL-PRESERVE |
| agc-50mp-yama/README.md | existing | The already-correct explanation used as the source for the corrected text. | VAL-INSTANCES |
| ishtar-cam-modes/Kullanim.txt | existing | User-facing document to check for the stale claim; no ClaudeQB run has read it. | VAL-INSTANCES |

## 10. Dependencies and Sequencing

Depends on Phases 3, 4, and 5 for settled capability claims. Correcting the description before the AGC capability question resolves would mean correcting it twice.

Depends on Faz 6.2 for the AON disposition.

Interacts with Faz 9.2 in both directions: that sub-phase needs corrected claims to build a checklist against, and this one needs the checklist for the consistency check. Running this sub-phase first and performing the consistency check after Faz 9.2 completes resolves the ordering.

Depends on Faz 1.1 for version control, which makes the description edit reviewable — a 1,600-character single-line field is otherwise difficult to diff meaningfully.

Blocks nothing, but a release should not ship with a description asserting a disproven claim.

Required decisions: none. The AON disposition was decided in Faz 6.2 and this sub-phase reflects it.

Required infrastructure: the device for the render check.

Required human approvals: none beyond the install for the render check.

Fresh session token and context risk: low to medium. The journal is roughly 1,300 lines, and the mitigation is targeted searching rather than a full read, since only the superseded section needs locating.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk (`AUTOPSY-P2-03`): one instance of the stale claim is corrected and others persist. Impact: the inconsistency is worse than the original uniform error, because a reader cannot tell which statement is current. Mitigation: F9.3-01 searches all four surfaces and `VAL-INSTANCES` requires the result to show coverage.
- Risk: the journal's superseded section is deleted rather than marked. Impact: the rejected reasoning is lost, and this project's history shows rejected hypotheses being retested when their records disappear. Mitigation: the scope states marking as the principle and `VAL-PRESERVE` confirms content is intact.
- Risk: the description reduction drops a currently true capability. Impact: a real capability becomes undocumented. Mitigation: `VAL-CONSISTENCY` checks in both directions, so a claim present in the checklist and absent from the description is caught.
- Risk: the corrected text is newly authored and states the mechanism imprecisely. Impact: a new inaccuracy replacing an old one. Mitigation: F9.3-02 draws on `agc-50mp-yama/README.md`, which already states it with measured values.
- Risk (`ARC-10` residual): the changelog is created and the description continues to accumulate history in the next release. Impact: the duplication returns. Mitigation: `ARC-10`'s update records the changelog as the owner, and Faz 9.2's checklist can carry the description's role as a verifiable item.
- Risk: `Kullanim.txt` or the web interface strings carry the stale claim and are missed because no ClaudeQB run has read them. Impact: the correction is incomplete in the surfaces users actually see. Mitigation: both are named explicitly in F9.3-01's search scope.
- Risk: the reduced description renders poorly in the module list. Impact: a formatting regression in the field's actual display. Mitigation: `VAL-INSTALL` checks the rendering rather than only the text.
- Risk: this sub-phase runs before the capability claims settle. Impact: rework. Mitigation: the dependency on Phases 3 through 5 is stated, matching Main-Planing section 9's guidance that Phase 9 be decomposed only after those settle.

## 12. Desired End State

The project's documentation states what is currently true. The disproven causal claim is corrected everywhere it appeared, using the explanation that already exists correctly in the tree. The module description is a summary and the version history lives in a changelog. The journal's superseded conclusion is marked with a forward pointer and its reasoning is preserved. The journal points to the ontology as the lookup surface, the AON disposition is reflected consistently, and the description and the release checklist agree in both directions.

The evidence an implementer should produce is the instance list, the corrected text at each instance, the reduced description, the changelog, the marked journal section, and the two-way consistency verdict.

The ledger summary Step 4 should append records: the instances corrected, the changelog created, the journal section marked, the consistency check result, and the `ARC-10` and `EV-23` updates.

## 13. Next Sub-Phase Transition Criteria

- Every located instance of the stale claim is corrected across all four surfaces.
- The description is a summary and the changelog carries the history.
- The journal's superseded section is marked with its content preserved.
- The two-way consistency check with Faz 9.2's checklist passes.
- The AON disposition is reflected consistently.
- `ARC-10` and `EV-23` are updated, and Phase 9 is complete.
