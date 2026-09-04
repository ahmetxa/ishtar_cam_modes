# Faz 3.11 — Phase Closure: the Operator Configuration Record and the Retirement Note

## 1. Context

`Main-Planing.md`'s amended Phase 3 states its desired end state as a document as much as a device state: "A written, reproducible AGC configuration that yields a clean 12.58 MP capture with the 50 MP layer active, with the survival behaviour across reboot and mode switch measured rather than assumed, and with the failure mode (unpinned AGC selecting 50 MP) documented so a future reader recognises it immediately."

`Faz3.7` through `Faz3.10` produce the measurements. This sub-plan turns them into something an operator can act on without reading a ledger, and closes the phase's loose ends.

There is a second obligation, and it is the more important one. `DEC-14` ends with an instruction addressed to the future: "**The one thing a future reader must not do** is treat the retirement as untested pessimism — both walls (`d0014` non-static, no code cave) are measured negatives with recorded method, and reopening needs new evidence about one of them, not renewed effort against the same two." Risk `R4` is retained in the master plan for the same reason: "a future reader who meets the 50 MP idea again should find the measured negative attached to it."

That instruction currently lives only in planning artifacts. `R7` records why that is not enough: knowledge concentrated in long documents has already caused this project to rediscover solved problems and misattribute one root cause. The retirement note belongs where somebody who is about to try 50 MP in AGC again will actually meet it.

The phase also inherits findings that were routed to it under the previous objective and that nobody has re-homed since `DEC-14`. Closing a phase without disposing of them would leave them attached to a phase that no longer exists.

## 2. Goal

Leave the project with an operator-facing record that makes the 12.58 MP AGC configuration reproducible from scratch, makes its failure mode instantly recognisable, and attaches the measured negatives to the 50 MP idea where a future reader will meet them — and with every finding routed to Phase 3 either disposed of or re-routed to a phase that still exists.

## 3. Description

The problem is that this phase's value is entirely in its reproducibility. The configuration itself is one preference. Everything expensive about it is knowing which preference, on which base, what it looks like when it drifts, what breaks it, and why the obvious more-ambitious version of the goal is closed. None of that survives in a preference value.

It belongs last because it consumes every earlier sub-plan's output, and because writing it earlier would mean writing it twice.

**The vibecoding slice strategy.** The first useful slice is the configuration document's operational core: the exact preference, the exact expected values in a snapshot, and the two black-fraction reference numbers that distinguish a good capture from a folded one. That alone makes the phase reproducible. The second slice is the failure-mode section and the re-arming routes. The third is the retirement note and the findings disposition, which are lower urgency but are the part `R7` says is most likely to be lost. The fastest validation signal is a read-back test: can someone follow the document, produce the expected snapshot fields, and get a capture that measures under the threshold?

**This sub-plan takes write authority for one shared file, stated explicitly because the project has been careful about that before.** `docs/phase3-preconditions.md` carries the per-measurement checklist. Write authority for it was `Faz4.6`'s `F4.6-09`, which landed the eighth item and is discharged (`IMPL-31`). This sub-plan adds a ninth item — verify the AGC photo-size pin before recording any capture result — and no other sub-plan may write that file during this phase. The reason the item belongs there rather than in the new configuration document is that the checklist is what every *later* measurement in the project runs, including Phase 4's and Phase 9's, and `R12` is a live hazard for all of them.

**What must not be over-planned.** Not a rewrite of the engineering journal, and not a correction pass over every stale claim in the project — `Faz9.3` owns that and is still `planned`. This sub-plan writes one new document, adds one checklist item, adds one README line, and routes what it cannot close.

## 4. Scope

- A new operator-facing document recording the reproducible 12.58 MP AGC configuration: the preference key and value, the HAL base and its md5, the expected `scripts/smoke.sh` field values, the expected `dumpsys` configured stream, and the two black-fraction reference numbers with the measurement method.
- A failure-mode section in that document: what an unpinned AGC selects, what its snapshot fields read, what its capture measures, and the quadrant signature — so the regression is recognisable from a snapshot, from an image, or from either alone.
- The re-arming routes recorded as warnings: importing either root `.agc` configuration file, an AGC package update, and any route the `Faz3.10` matrix observed.
- The survival matrix from `Faz3.10`, reproduced as a table with its verdicts.
- A ninth per-measurement checklist item in `docs/phase3-preconditions.md` requiring the pin to be verified before any capture result is recorded, with write authority for that file taken explicitly by this sub-plan.
- A one-line pointer in `README.md`'s operator-facing material, beside the existing `.agc` preference-trap warning.
- The retirement note: the measured negatives attached to the 50 MP-in-AGC idea, with their run ids, placed where a future reader meets the idea rather than only in the master plan.
- Disposition of the findings routed to Phase 3 that the objective change orphaned, each either closed, re-routed to an existing phase, or reclassified as knowledge with the user's confirmation where the call is theirs.
- A statement of what Phase 3 now claims, in the exact form `Faz9.2`'s release checklist and `Faz9.3`'s documentation correction will consume.

## 5. Out of Scope

- Editing `Planner-docs/Main-Planing.md`. It already carries the retirement in sections 1, 6 and 7, and editing it is the replanning trigger recorded in the ledger's section 7.
- The general stale-claim correction pass. `Faz9.3` owns it; this sub-plan supplies one corrected claim for it to consume.
- Rewriting `50MP-Entegrasyon-Plani.md`. The journal is history and the index records that restructuring it is deliberately deferred.
- Any device action beyond the read-back verification of the document.
- Any new measurement. Everything recorded here comes from `Faz3.7` through `Faz3.10`; a gap in the evidence is reported as a gap, not filled by a fresh run inside a closure sub-plan.
- Closing `FIND-3.5-01` or `FIND-4.5-02` on this sub-plan's own authority. Both are unresolved technical facts; their disposition under a retired objective is the user's call and is routed, not taken.
- Building enforcement for the pin, in any form.
- Deciding Phase 4's remaining scope or ordering. This sub-plan hands Phase 4 a claim, not a sequence.

## 6. Current Repository Evidence

`docs/phase3-preconditions.md` exists and carries five sections, the fifth being the per-measurement checklist with eight items: preferences clear, bracket taken, one variable, metadata republished, restorable, addresses recorded immediately, attribution stated, crash contamination cleared. The ninth item is appended to that list, in the same form.

`README.md` exists (179 lines, `Faz1.6` / `IMPL-08`) with an artifact manifest carrying fifteen checksums and a preference-trap warning on both `.agc` entries. It is the operator-facing surface where a pointer belongs, and its manifest is where an entry's hazard is already recorded — so the pattern to follow exists.

`docs/consumer-survey.md` (`Faz3.4`), `docs/regression-v2.1.md` (`Faz2.3`), `docs/recovery-runbook.md` (`Faz9.2` / `IMPL-19`) and `docs/raw-geometry-diagnosis.md` (`Faz4.6`) establish the house form for an operator-facing `docs/` record: a bounded document with numbered sections, measured values, and its producing sub-plan named.

Findings routed to Phase 3 that the objective change leaves without a home:

- `FIND-3.5-01` (active-array geometry) and `FIND-4.5-02` (the RAW payload geometry cause) are recorded **OPEN** as recently as `IMPL-51`. Both exist to explain why a full-resolution AGC frame is unusable — a question the retired objective asked. Under `DEC-14` neither blocks anything, and `IMPL-43` located `FIND-4.5-02`'s mechanism precisely enough that it is knowledge rather than a defect. Recommended disposition: reclassify both as knowledge attached to the retirement note, not closed as resolved. The call is the user's.
- `FIND-2.3-03` (AGC's video section black) was routed to Phase 3 "on its own merits" by `IMPL-13`, which also measured that it reproduces in plain `stock` with sensor and HAL unmodified, so it is **not** module-caused. It has no connection to the photo-size objective and must be re-routed rather than closed with the phase.
- `FIND-2.3-02` (`ln2`/`ln4` crash AGC) constrains what invariant 4 could ever compose and is referenced by `Faz5.3`'s retention decision. It is not this phase's, and its current routing should be stated rather than assumed.

Ledger `DEC-14` records the retirement's reasoning and its explicit instruction to future readers. `R4` in `Main-Planing.md` section 7 records the same, closed as a risk and retained as a record. The measured negatives to attach are `IMPL-47` and `IMPL-51` (`d0014` computed inside `InitializeScalerStaticCaps` behind a per-camera switch, not static data, no patchable row), `IMPL-50` (no contiguous free run ≥ 16 bytes anywhere in the binary's sole executable segment, longest run 12 bytes, 3 instances), and `IMPL-49` / `IMPL-50` (narrowing the broad RAW rows prevents AGC from launching, 3/3 at two independent bisection stages).

## 7. Planned Work Breakdown

- F3.11-01 — Write the configuration core
  - Description: The preference key and value, the HAL base with its md5, the expected smoke field values, the expected `dumpsys` configured stream, and the two black-fraction references with the `IMPL-40` measurement method stated so the numbers are reproducible.
  - Output: The operational core of `docs/agc-12mp-configuration.md`.
- F3.11-02 — Write the failure-mode section
  - Description: The unpinned signature from `Faz3.10`'s negative control — snapshot fields, configured stream, measured black fraction, and the quadrant pattern `IMPL-43` recorded — so the regression is recognisable from any one of the three.
  - Output: A failure-mode section a reader can match against without re-deriving anything.
- F3.11-03 — Record the re-arming routes
  - Description: Importing either root `.agc` file (which also re-arms the twelve trap keys), an AGC package update, and anything the `Faz3.10` matrix observed. Each gets what to check afterwards, not just a warning.
  - Output: A re-arming section with a check per route.
- F3.11-04 — Reproduce the survival matrix
  - Description: The four axes with their verdicts and the confirming capture, as a table, so the durability claim is in the operator document rather than only in the ledger.
  - Output: The matrix table with its verdict rule stated.
- F3.11-05 — Add the ninth per-measurement checklist item
  - Description: Append to `docs/phase3-preconditions.md` an item requiring the AGC photo-size pin to be verified before any capture result is recorded, citing the smoke field as the check. State this sub-plan's write authority for the file and that `F4.6-09`'s authority is discharged.
  - Output: A ninth checklist item in the existing form.
- F3.11-06 — Add the README pointer
  - Description: One line in the operator-facing material beside the existing `.agc` warning, pointing at the configuration document.
  - Output: A README line, in the manifest's existing style.
- F3.11-07 — Write the retirement note
  - Description: In the configuration document, a section stating why 50 MP in AGC is not the objective, with the four measured negatives and their run ids, and `DEC-14`'s instruction that reopening needs new evidence about one of the two walls rather than renewed effort against the same two.
  - Output: A retirement note attached to the 50 MP idea where a reader meets it.
- F3.11-08 — Dispose of the orphaned findings
  - Description: For each of `FIND-3.5-01`, `FIND-4.5-02`, `FIND-2.3-03` and `FIND-2.3-02`, record a disposition: closed, re-routed to a named existing phase, or reclassified as knowledge. Route to the user the ones that are the user's call rather than taking them.
  - Output: A finding-disposition table with no finding left attached to a phase that is closing.
- F3.11-09 — State the claim Phase 9 will verify
  - Description: Write the sentence `Faz9.2`'s checklist and `Faz9.3`'s correction pass will consume: what the project claims about AGC, under what conditions, proved by which command.
  - Output: One claim with its proving command named.
- F3.11-10 — Read-back verification
  - Description: Have the document followed as written — set the state from scratch per its instructions, confirm the expected snapshot fields appear, and confirm one capture measures under the threshold. A configuration record that has not been followed once is a draft.
  - Output: A read-back result naming what the document got wrong, if anything, and the correction.

## 8. Acceptance Criteria

- `docs/agc-12mp-configuration.md` exists and contains: the preference key and value; the HAL base md5; the expected smoke field values; the expected `dumpsys` configured stream; both black-fraction references with the measurement method; the failure-mode signature; the re-arming routes with a check for each; the survival matrix; and the retirement note.
- The read-back verification was performed: the state was set from the document alone, the expected fields appeared, and one capture measured under the stated threshold. Any correction the read-back forced is recorded rather than silently applied.
- `docs/phase3-preconditions.md` has a ninth checklist item covering the photo-size pin, in the existing form, and the document names this sub-plan as its author.
- `README.md` carries a pointer to the configuration document beside the existing `.agc` warning.
- The retirement note names all four measured negatives with their run ids and states `DEC-14`'s reopening condition.
- Every finding routed to Phase 3 has a recorded disposition; none is left attached to the closing phase. Dispositions that are the user's call are routed as such rather than taken by the implementer.
- The Phase 9 claim is written as one sentence with the command that proves it named.
- No planning file outside `Planner-docs/` was written by this sub-plan except the three named files, and `Main-Planing.md` is not edited.
- Where the evidence from `Faz3.7`–`Faz3.10` has a gap, the document says so explicitly instead of filling it with an assumption.

## 9. Validation and Test Approach

Validation is primarily document validation with one live read-back, which is the only check that distinguishes a written configuration from a reproducible one.

- `VAL-DOCS` (from Faz 3.1) — read back every required section of the configuration document, the ninth checklist item, and the README pointer, confirming each cited value resolves to a recorded measurement rather than to a recollection.
- `VAL-READBACK` (proposed) — the live check: follow the document from a cold state, confirm the expected smoke fields, take one capture, measure it. Failures here are document defects, not device defects.
- `VAL-SMOKE` (from Faz 2.1, extended by Faz 3.8) — the bracket for the read-back.
- `VAL-ARTIFACT` (from Faz 3.7) — the read-back capture, measured by the `IMPL-40` method.
- `VAL-ROUTING` (proposed) — confirm each disposed finding's new home exists: a named phase that is not closing, or a recorded reclassification with the user's answer attached.
- `VAL-PRECOND` (from Faz 3.1) — the checklist, now including the ninth item this sub-plan adds, applied to the read-back capture. The ninth item's first use is on the run that creates it, which is the cheapest possible test of it.

Local versus live: the writing is local; the read-back is live. Security validation is not applicable — no credential, no key, and no secret value appears in any of the three files. Ontology validation: the retirement note's content belongs in `Project-Ontology.md` section 6 and against invariant 6 as well, and Step 4 should write it there in the same session it writes the document, per `R10`.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| docs/agc-12mp-configuration.md | proposed | The operator-facing configuration record, failure mode, re-arming routes, survival matrix and retirement note. | VAL-DOCS, VAL-READBACK |
| docs/phase3-preconditions.md | modified | Gains the ninth per-measurement checklist item. Write authority taken by this sub-plan explicitly. | VAL-DOCS, VAL-PRECOND |
| README.md | modified | One operator-facing pointer beside the existing `.agc` warning. | VAL-DOCS |
| scripts/smoke.sh | existing | The read-back bracket and the field values the document predicts. | VAL-SMOKE, VAL-READBACK |
| Planner-docs/Project-Ontology.md | modified | The retirement recorded against invariant 6 and the address book, so it survives context loss. | VAL-DOCS |
| Planner-docs/Planing-Ledger.md | modified | The phase closure, the finding dispositions, and the Phase 9 claim. | VAL-ROUTING |

## 10. Dependencies and Sequencing

Depends on `Faz3.7` for the pin and the thresholds, `Faz3.8` for the field names the document predicts, `Faz3.9` for the coexistence evidence, and `Faz3.10` for the survival matrix and the failure-mode signature. It cannot be written before them and should not be started early "to save time" — a configuration record written ahead of its measurements is a guess with a filename.

Depends on `DEC-15` having been answered, since the document names a base.

Blocks nothing technically, but Phase 9 consumes its output: `Faz9.2`'s release checklist needs the claim and its proving command, and `Faz9.3`'s correction pass needs the corrected claim about AGC's working resolution. `Faz9.3` is also where `EV-23`'s contradicted "AGC cannot exceed 15.2 MP" claim is corrected, and this phase's result is the current fact that replaces it.

Required decisions: the disposition of `FIND-3.5-01` and `FIND-4.5-02` under a retired objective, which is the user's. The implementer proposes reclassification as knowledge and does not take the decision.

Required credentials or live endpoints: none. Device access for the read-back only.

Required human approvals: device access and one shutter press for the read-back; the finding dispositions that are routed.

Fresh-session token and context risk: **low to medium**. The risk is breadth rather than depth — this sub-plan touches four earlier sub-plans' outputs plus three files. Read the ledger rows for `Faz3.7`–`Faz3.10` rather than re-reading the sub-plans themselves.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the configuration document is written from the ledger and never followed. Impact: a reproducibility claim that has not been tested, which is the same defect as an assertion never observed failing. Mitigation: `VAL-READBACK` requires the document to be followed from a cold state, and its corrections recorded.
- Risk (`R7`): the retirement note goes only into planning artifacts, and a future reader meets the 50 MP idea somewhere else and starts again. Impact: weeks of measured negative work repeated. Mitigation: the note goes into `docs/`, is pointed at from `README.md`, and is recorded against ontology invariant 6 — three surfaces, chosen because that is where readers of this project actually land.
- Risk: the retirement note reads as discouragement rather than as evidence, and a genuinely new idea is suppressed by it. Impact: the opposite failure, and a real cost. Mitigation: the note states `DEC-14`'s reopening condition explicitly — new evidence about one of the two walls reopens it; renewed effort against the same two does not.
- Risk: a finding is closed to tidy the phase rather than because it is resolved. Impact: an unresolved technical fact disappears from the register, which is exactly what `AUDIT-FIX-14` was raised about in a different form. Mitigation: `F3.11-08` allows three dispositions and requires the user's answer for the two that are theirs; "closed" is not the default.
- Risk: two sub-plans end up writing `docs/phase3-preconditions.md`. Impact: the file-ownership discipline the project has kept since `Faz3.5` breaks. Mitigation: write authority is stated in section 3, in the work item, and in the Implementation Contract, and `F4.6-09`'s discharge is cited.
- Risk: the document records a value that came from a different base than the one it names. Impact: an operator follows it on the shipped module and gets a result the document does not predict. Mitigation: `DEC-15` is a precondition and the read-back is performed on the named base.
- Risk: `Faz9.3` later restates the claim differently. Impact: two live descriptions of what the project does, which is the condition `R7` describes. Mitigation: `F3.11-09` writes the claim once, in the form Phase 9 consumes, rather than leaving Phase 9 to paraphrase.
- Risk: the phase is recorded as closed while a `Faz3.10` axis failed and was routed. Impact: a closure that overstates the result. Mitigation: the desired end state requires the closure statement to carry the matrix's failures, and the Phase 9 claim to be conditioned on what actually survived.

## 12. Desired End State

Phase 3 is closed with a written, followed, operator-facing record: `docs/agc-12mp-configuration.md` makes the 12.58 MP AGC configuration reproducible from a cold state, makes its failure mode recognisable from a snapshot or from an image, lists the routes that break it with a check for each, carries the survival matrix, and attaches the four measured negatives to the 50 MP idea with `DEC-14`'s reopening condition.

The per-measurement checklist has a ninth item that protects every later measurement in the project from `R12`. `README.md` points at the record. Every finding routed to the old Phase 3 has a disposition. Phase 9 has one sentence to verify and one corrected claim to propagate.

The evidence an implementer should produce: the document itself, the read-back result with any corrections it forced, the ninth checklist item, the README line, the finding-disposition table with the user's answers where required, and the Phase 9 claim with its proving command.

The ledger summary Step 4 should append records: the phase closure with the matrix's verdicts carried into it including any failures; the finding dispositions and who decided each; the read-back result; the three files written; and the claim Phase 9 inherits.

## 13. Next Sub-Phase Transition Criteria

- The configuration document exists, contains every required section, and has been followed once from a cold state with its corrections recorded.
- The ninth checklist item is in `docs/phase3-preconditions.md` and was applied to the read-back capture.
- `README.md` points at the record.
- The retirement note names all four measured negatives with run ids and states the reopening condition.
- Every finding routed to Phase 3 has a disposition, with the user's answer attached where the call was theirs.
- The Phase 9 claim is one sentence with its proving command named, and it is conditioned on what the survival matrix actually showed.
- Phase 4's remaining sub-plans — `Faz4.2`, `Faz4.3`, `Faz4.4` — can proceed against a phase whose result is written down rather than remembered.
