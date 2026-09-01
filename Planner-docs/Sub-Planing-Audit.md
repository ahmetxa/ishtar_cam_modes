# Sub-Planing Audit

> Step 3 audit — ClaudeQB. Body language: English (default contract).
> The project's user-facing documents and module interface remain Turkish and English; that convention is unchanged.
>
> **This is the third audit.** It supersedes the 2026-09-01 audit of the thirty-three-sub-plan snapshot, which in turn superseded the 2026-08-24 audit of the thirty-two-sub-plan snapshot. It was triggered by two events since: the **execution** of `Faz4.5` (`IMPL-27` … `IMPL-30`), and the 2026-09-01 Step 2 Phase 4 re-plan run 6, which authored `Faz4.6`, amended `Faz4.4`, and amended the index. Twenty sub-plans are now complete, so the readiness table is a reconciliation against the ledger and the repository rather than a first assessment.

## 1. Audit Summary

**Overall audit status: PASS_WITH_WARNINGS.**

Structure is clean, and it is cleaner than at the previous audit. All nine master-plan phases have a folder; all **thirty-four** sub-plans carry the thirteen required sections in the required order, each with an Implementation Contract table whose `State` values all fall inside the allowed set; the index resolves in both directions at 34/34; numbering is contiguous within every phase; no non-ASCII, spaced, or duplicated filename exists; no contract path is absolute or uses `..` traversal; and the bundled validator reports **zero** secret findings across `Planner-docs/`.

**Six of the nine findings left open by the previous audit are now resolved**, and resolved properly — by editing the artifact that was wrong, not by restating the problem. `AUDIT-FIX-05` corrected the open-question count in the index and scoped it to the Step 2 moment. `AUDIT-FIX-06` is fully discharged: the ledger now carries planning-run rows 4, 5 and 6, the snapshot registry reads 34, and `Faz4.5` has a Sub-Plan Status Matrix row. `AUDIT-FIX-07` moved `Faz4.1` off `blocked`. `AUDIT-FIX-09` is repaired in `Faz4.4`, and repaired well — the sub-plan now refuses to quote a baseline at all and records that the two recorded figures disagree with each other rather than picking one. `AUDIT-FIX-10` is recorded in the index under Phase 4, extended to cover `DEC-13`(a). `AUDIT-FIX-12`'s malformed twelve-cell ledger row is now nine cells. `AUDIT-FIX-13`'s discharge banner sits at the head of section 4a.

`AUDIT-FIX-08` is also resolved, and this is the one worth naming, because it was the audit's structural finding rather than a clerical one: no sub-plan in the queue held write authority for `docs/phase3-preconditions.md`, so `FIND-3.4-03`'s crash-contamination rule could only ever be restated inline. `Faz4.6` now carries that file as `modified` and `F4.6-09` lands the item. The gap is closed at the mechanism, not at the symptom.

**Step 2 output is usable for Step 4.** No P0 or P1 audit finding exists. Sixteen findings are recorded: twelve `resolved` and four `open`, all open ones P2 or P3. One P1 **project** finding — `FIND-4.5-02`, the surviving image corruption — is open and is the point of the work queued next; it is not an audit finding and does not gate Step 4.

**Most important finding: `AUDIT-FIX-15`.** Every artifact of the 2026-09-01 execution and re-plan is uncommitted. `HEAD` is `947a01b`, "Faz 4.1 blocked at pre-execution review", which predates `IMPL-27` … `IMPL-30` entirely. Six `Planner-docs` files are modified, two sub-plans are untracked, and the eight `snapshots/` artifacts plus `agc-50mp-yama/hal-activearray-deneme.patch` — the measurement evidence the ledger cites for both confirmed write sites — exist only in the working tree. `R1` is the plan's own critical risk, and its mitigation currently does not cover the most expensive day of work in the project.

**Most important remediation action.** Commit the working tree before starting the next slice. This is not a Step 4 code change and needs no plan authority; it is the rollback point that `Faz4.6`'s first host-side slice should be able to fall back to.

## 2. Reviewed Sources

**Files read in full or by targeted section.**

- `Planner-docs/Main-Planing.md` — section 6 roadmap in full, sections 7, 8, 9 and 10 in full.
- `Planner-docs/Sub-Planing-Index.md` — sections 3, 4a, 4b, 6 and 7 in full; sections 1 and 2 by targeted extraction.
- `Planner-docs/Planing-Ledger.md` — sections 2, 3, 4 and 6 in full; sections 5, 7 and 8 by targeted extraction.
- `Planner-docs/Project-Comprehension.md` — section 8 hypothesis rows in full; the `EV-` register by identifier range and count.
- `Planner-docs/Project-Ontology.md` — competency-question status column by extraction.
- `Planner-docs/Sub-Planing-Audit.md` — the superseded revision, read in full before replacement so no finding was dropped silently.
- All **34** sub-plans — headings, H1 titles, Implementation Contract tables and `State` vocabulary checked mechanically across every file; sections 1, 9, 10 and the work breakdown read directly in `Faz4.1`, `Faz4.4`, `Faz4.5`, `Faz4.6`, `Faz1.1`, `Faz2.4`, `Faz6.2`, `Faz7.1`, `Faz7.2`, `Faz8.1`, `Faz8.2`, `Faz9.1` and `Faz9.3`.
- `references/Third-Planner.md` and the bundled `scripts/validate_planner_docs.py` vocabulary constants, read so reported values are checked against the allowed sets rather than against memory.

**Folders inspected.** `Planner-docs/` at depth 4; all nine `Faz-*-Plans/` folders; the repository root listing; `snapshots/` by name only.

**Important commands run.** `pwd`; `git branch --show-current`; `git status --short --branch`; `git log --oneline -n 10`; `git rev-list --count HEAD`; `git ls-files | wc -l`; `find Planner-docs -maxdepth 4 -type f | sort`; `wc -l` over every planner document; a per-file heading extraction comparing the thirteen required sections against the required order; a per-file naming, folder-number, H1-number, ASCII and duplicate scan; an empty-section scan; a contract-table header and `State`-vocabulary scan; an absolute-path and `..`-traversal scan over the contract tables; a placeholder scan for `TBD`, `FIXME`, `XXX`; a ledger row cell-count scan; and the bundled validator in `--mode step3-preflight --strict`.

**Validator execution.** The bundled validator ran successfully, from the installed plugin cache at `.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py`. Note for future runs: `python3` on this host is the Windows Store alias stub and fails; `python` resolves to the real CPython 3.14.7. The invocation must use `python`. This is the same fact `IMPL-07` recorded, restated here because the Step 3 prompt's literal command line does not work on this host.

**Counts, all reported from the source and never from memory.** Main-plan phases: 9. Phase folders: 9. Sub-plan files: 34. Index sub-plan references: 34 unique, resolving in both directions. Sub-plans with the full thirteen-section structure in order: 34/34. Sub-plans with exactly one Implementation Contract table: 34/34. Validator secret findings: 0. Validator warnings in `--mode step3-preflight --strict`: 11, promoted to 11 errors by `--strict`.

**Things not verified in this run.** No sub-plan's technical claims were re-derived: addresses, md5 values, `dumpsys` counts and capture geometries are taken as reported by the implementation runs that measured them. No device was contacted. No binary was disassembled. The `snapshots/` artifacts were listed by name only and their contents were not opened. Whether `docs/phase3-preconditions.md`, `docs/recovery-runbook.md` and the other `docs/` deliverables match what the ledger says they contain was not checked — that is Step 4's business, not the audit's. The tile application's Java sources remain unread by any ClaudeQB run.

**Secrets.** The validator's redacted scan reports zero findings. An independent length-bounded pattern scan matched one file by name only, `Planner-docs/Sub-Planing-Audit.md`, on the *word* `password` appearing in `AUDIT-FIX` / `DEC-10` prose describing a hazard; no value is present and none was printed. That prose is carried forward in this revision.

## 3. Main Phase Coverage Analysis

| Main phase no | Main phase heading | Expected folder | Folder exists? | Sub-plan count | Coverage status | Notes |
|---|---|---|---|---|---|---|
| 1 | Workspace safety net | `Planner-docs/Faz-1-Plans/` | yes | 6 | OK | All six complete or verified. Phase closed in practice. |
| 2 | Ship and re-baseline v2.1 | `Planner-docs/Faz-2-Plans/` | yes | 4 | OK | Three verified; `Faz2.4` remains queued and is the only Phase 2 item nothing depends on. |
| 3 | 50 MP end-to-end in AGC | `Planner-docs/Faz-3-Plans/` | yes | 6 | OK | Closed 2026-09-01 by user decision at the `Faz3.6` gate, as PRIMARY SUCCESS. |
| 4 | Minimal correct HAL patch | `Planner-docs/Faz-4-Plans/` | yes | 6 | OK | Grew 4 → 5 → 6 across two scoped re-plans. Scope exceeds `Main-Planing.md` section 6 by three decision-backed work streams; recorded, not silent — see section 9 and `AUDIT-FIX-10`. |
| 5 | Mode-0 12-bit composition | `Planner-docs/Faz-5-Plans/` | yes | 3 | OK | Closed 2026-08-31. Disposition RETAIN, recorded as proven-not-adopted. |
| 6 | AON fix upstreaming | `Planner-docs/Faz-6-Plans/` | yes | 2 | OK | `Faz6.1`'s edit landed; its *effect* is unverifiable until Phase 7, and `Faz6.2` registers that verification rather than assuming it. |
| 7 | Android 16 build environment | `Planner-docs/Faz-7-Plans/` | yes | 2 | OK | Deliberately low-detail per Main-Planing section 9's "do not expand yet". Gated on host action the user must take. |
| 8 | beryl port and kernel LTS merge | `Planner-docs/Faz-8-Plans/` | yes | 2 | OK | Sizing and scoping only; neither sub-plan attempts the work itself. Correct given the Phase 7 gate. |
| 9 | Release engineering | `Planner-docs/Faz-9-Plans/` | yes | 3 | OK | `Faz9.2` is split: its recovery-runbook half was pulled forward and delivered by `IMPL-19`; its checklist half stays in Phase 9. |

No phase is missing, no folder exists without a corresponding main phase, and no phase was renamed or renumbered. The folder set is exactly `Faz-1-Plans` through `Faz-9-Plans`.

## 4. Sub-Plan File Inventory

All thirty-four files carry the thirteen required sections in the required order, an H1 whose phase number matches both the filename and the containing folder, and exactly one Implementation Contract table. Rather than repeat "sections OK, title matches" thirty-four times, that is stated once here and only the exceptions and the notable content observations are listed below. **There are no exceptions.**

**Phase 1 — `Faz-1-Plans/` (6 files).** `Faz1.1-version-control-bootstrap.md`, `Faz1.2-signing-key-containment.md`, `Faz1.3-patch-table-format-contract.md`, `Faz1.4-toolchain-procedure-record.md`, `Faz1.5-static-safety-probes.md`, `Faz1.6-workspace-readme-and-refs-index.md`. All complete or verified. Content quality high; `Faz1.3` and `Faz1.5` in particular produced findings that later phases depended on (`FIND-1.5-01` … `-03`, and the `hal_write` grammar `Faz4.5` encoded its patch words against).

**Phase 2 — `Faz-2-Plans/` (4 files).** `Faz2.1-device-smoke-script.md`, `Faz2.2-flash-v21-and-baseline-snapshot.md`, `Faz2.3-ten-mode-regression-pass.md`, `Faz2.4-tiles-hide-disposition.md`. `Faz2.1` is the highest-leverage document in the set: `scripts/smoke.sh` has bracketed every device change since, and every later measurement claim rests on it. `Faz2.4` is the only queued Phase 2 item; its section 10 states plainly that deferring it indefinitely is how it reached its third release unresolved, which is the right way to write a low-priority item.

**Phase 3 — `Faz-3-Plans/` (6 files).** `Faz3.1-preference-trap-clearance.md`, `Faz3.2-pixel-array-write-site-search.md`, `Faz3.3-single-word-patch-and-metadata-proof.md`, `Faz3.4-consumer-compatibility-check.md`, `Faz3.5-agc-capture-and-image-evidence.md`, `Faz3.6-fallback-decision-gate.md`. All verified. `Faz3.2` is a model of a bounded search: it set an attempt budget, spent 3 of 15, and contradicted its own hypothesis `H-01` rather than defending it.

**Phase 4 — `Faz-4-Plans/` (6 files).**

- `Faz4.1-fullres-dimension-guard.md` — amended by run 4 for `DEC-11`. Carries the format-32 extension across sections 4, 5, 7, 8, 10, 12 and 13, plus `F4.1-01b` and `F4.1-05b`. `F4.1-01` now names the camera id and the `streamcfg` int32 metric. Ledger row correctly `planned`.
- `Faz4.2-duration-rows.md` — unchanged since Step 2. Routes the bucketing consequence to the user as `DEC-09` rather than guessing it.
- `Faz4.3-patch-table-consolidation.md` — unchanged. Correctly constrained by `halpatch.sh`'s two-state (`fullres`/`stock`) assumption, which `IMPL-05` established.
- `Faz4.4-patch-compatibility-validation.md` — amended by run 6. Carries `FIND-4.5-01` as `F4.4-02b` with a per-camera-id consistency table and a front-camera behavioural check. The `AUDIT-FIX-09` repair is the best-executed change in this run: rather than pick one of two disagreeing recorded figures, section 1 records that `EV-16` says 508 → 868 while `IMPL-30` measured hal3 500 → 868, states that the discrepancy is unsettled, and forbids quoting a baseline at all in favour of reading one from a bracketed snapshot.
- `Faz4.5-active-array-raise.md` — **executed and verified.** Twelve of thirteen acceptance criteria met; the thirteenth, `FIND-3.5-01`'s closure, explicitly left open with what was learned attached, which the criterion permits. Both write sites confirmed by measurement, each on the first candidate examined. Its section 9 restates the seven-item checklist inline plus the eighth item, which is what `AUDIT-FIX-08` asked for as the interim measure.
- `Faz4.6-raw-payload-geometry-diagnosis.md` — new in run 6, 242 lines, the longest sub-plan in the set. Owns `FIND-4.5-02` (P1). Its first four work items are host-side, need neither the device nor the user, and may settle the diagnosis outright. `F4.6-07`, the DNG probe, is explicitly gated on `Faz4.1` landing format-32 emission per `EV-35` — the gate is stated in the sub-plan rather than discovered at execution. `F4.6-09` takes write authority for `docs/phase3-preconditions.md`.

**Phase 5 — `Faz-5-Plans/` (3 files).** `Faz5.1-twelve-bit-mode-zero-blob.md`, `Faz5.2-temporary-mount-composition-test.md`, `Faz5.3-exclusion-rule-disposition.md`. All verified; phase closed. `Faz5.2` required and obtained explicit user approval before any device action, which is the approval-gate pattern the rest of the project should copy.

**Phase 6 — `Faz-6-Plans/` (2 files).** `Faz6.1-symlink-entry-in-device-trees.md`, `Faz6.2-aon-module-disposition.md`. `Faz6.1`'s edit landed in both trees with CRLF preserved and the syntax cited from a reference tree; its effect is honestly recorded as unverified, because verifying it needs a build.

**Phase 7 — `Faz-7-Plans/` (2 files).** `Faz7.1-wsl2-provisioning.md`, `Faz7.2-first-aospa-build.md`. `Faz7.2` sets a stopping rule before attempting the build and marks three decisions (branch, platform tree, device tree scope) as open rather than guessing them.

**Phase 8 — `Faz-8-Plans/` (2 files).** `Faz8.1-beryl-port-sizing.md`, `Faz8.2-kernel-lts-merge-scoping.md`. Both deliberately low-detail. `Faz8.1` says so in its own section 10, and says why: the Phase 7 gate has not been passed. `Faz8.2` correctly records that it is independent of `Faz8.1`.

**Phase 9 — `Faz-9-Plans/` (3 files).** `Faz9.1-reproducible-release-build.md`, `Faz9.2-release-verification-checklist.md`, `Faz9.3-documentation-consolidation.md`. `Faz9.2` is `in_progress`: `IMPL-19` delivered `docs/recovery-runbook.md` and verified its central claim mechanically — no module script writes to `/odm` — rather than asserting it. `Faz9.3`'s section 10 resolves its circular dependency with `Faz9.2` explicitly instead of leaving it for the implementer to notice.

## 5. Naming and Sequencing Check

**No naming, numbering, or ordering issues were found in the sub-plan set.**

Every folder matches `Planner-docs/Faz-<number>-Plans/`. Every filename matches `Faz<phase>.<sub>-<ascii-lowercase-kebab-slug>.md`, checked by regex against every file. No filename contains a space or a non-ASCII character. No filename is duplicated and no `<phase>.<sub>` pair is duplicated. Every file's folder number equals its filename phase number, and every H1's `Faz X.Y` equals its filename's. Sub-plan numbering is contiguous from 1 within every phase: 1–6, 1–4, 1–6, 1–6, 1–3, 1–2, 1–2, 1–2, 1–3. No slug is generic; each names its own work.

Phase folder order preserves `Main-Planing.md` section 6 exactly, and no phase has been renumbered by any of the three planning runs that touched Phase 4.

**One ordering observation, in the ledger rather than in the sub-plans.** The Sub-Plan Status Matrix lists Phase 4 as `Faz4.1`, `Faz4.2`, `Faz4.3`, `Faz4.4`, `Faz4.6`, `Faz4.5` — neither numeric order nor queue order. Every other phase is in numeric order. Recorded as `AUDIT-FIX-16` (P3); it costs a reader a moment and nothing more.

## 6. Index Consistency Check

**The index resolves in both directions at 34/34.** Every sub-plan file on disk is referenced by `Sub-Planing-Index.md`, and every sub-plan path the index names resolves to an existing file. No reference is broken and no file is unindexed.

The phase count in the index matches `Main-Planing.md` at nine, and the per-phase counts in section 6 match the filesystem exactly: 6, 4, 6, 6, 3, 2, 2, 2, 3, total 34. Section 6 states these were counted from `find` on 2026-09-01 rather than from memory, and re-counting confirms them.

**Coverage-checklist honesty.** Every claim in section 6 was tested independently and every one holds, including the two that are easy to assert and tedious to verify: the thirteen-section structure in all 34 files, and the Implementation Contract table with the `Path` / `State` / `Purpose` / `Validation Command IDs` columns and allowed `State` values in all 34. One note for future auditors: the contract table is present in every file but is *labelled* "Implementation Contract" in only two (`Faz4.5`, `Faz4.6`). A search for the phrase finds 2 of 34; a search for the header row finds 34 of 34. The checklist claim is true; only the label is inconsistent, and it is not worth a finding.

**Execution order.** The recommended order is plausible and, unusually, is argued rather than asserted. Section 4b states the current Phase 4 order — `Faz4.6` host-side half → `Faz4.1` → `Faz4.6` gated half → `Faz4.2` → `Faz4.3` → `Faz4.4` — and gives three reasons for placing `Faz4.1` ahead of the rest of the diagnosis, including the deadlock argument that `Faz4.1`'s format-32 extension is what unlocks `F4.6-07`. That is the correct call and it is correctly justified.

**One structural note, not a defect.** `Faz4.6` appears twice in the recommended order, split into a host-side half and a gated half. This audit's section 12 emits **one** row for it, per the rule against conflicting rows for the same sub-plan; the split is a within-sub-plan sequencing instruction that Step 4 reads from the index and from `Faz4.6`'s own section 10, not a second queue entry.

**Previously flagged, now correct.** Section 2's competency-question count reads eleven open, one partially answered, four answered, and is scoped explicitly to the Step 2 moment (`AUDIT-FIX-05`, resolved). Section 3 records the Phase 4 scope divergence from `Main-Planing.md`, now covering all three additions (`AUDIT-FIX-10`, resolved). Section 4a carries its discharge banner (`AUDIT-FIX-13`, resolved).

## 7. Required Section Structure Check

**All 34 sub-plans were checked, not sampled.** Each file's `##` headings were extracted in document order and compared as an ordered sequence against the required thirteen. **34/34 match exactly.**

- Missing sections: none.
- Duplicated sections: none — no file has a repeated `##` heading.
- Wrong order: none.
- Empty sections: none. An automated scan for a `##` heading followed by no non-blank content before the next heading or EOF returned zero hits across all 34 files.
- Placeholder sections: none. A scan for `TBD`, `FIXME`, `XXX`, `Lorem` and placeholder brackets across all phase folders returned zero hits.
- Wrong phase number in title: none. Every H1 reads `# Faz X.Y — <Title>` with `X.Y` equal to the filename's.
- Filename/H1 mismatch: none.

Implementation Contract tables: 34/34 present, exactly one per file, with the header `| Path | State | Purpose | Validation Command IDs |`. The `State` column uses `existing` (94), `modified` (56), `proposed` (22), `external` (1) and `deferred` (1) — every value inside the allowed set of `existing`, `modified`, `proposed`, `generated`, `external`, `deferred`. No contract path is absolute and none uses `..` traversal.

## 8. Content Quality and Implementability Analysis

**These sub-plans are specific, actionable, and suitable for Step 4 decomposition, and there is now direct evidence for that rather than an opinion.** Twenty of thirty-four have been executed. The ones that ran, ran against their own acceptance criteria and produced measurable verdicts, including negative ones: `Faz3.2` contradicted its own hypothesis; `Faz4.5` met twelve of thirteen criteria and recorded the thirteenth as deliberately unmet; `Faz5.3` decided RETAIN and recorded the composition as proven-not-adopted. A plan set that can produce a clean negative result is a plan set with real acceptance criteria.

**Acceptance criteria are verifiable.** They name commands, files, counts and comparisons: byte-identical snapshot diffs, md5 matches, SOF-marker resolution reads, `streamcfg` int32 element counts qualified by camera id, per-key preference audits expecting 0/12. The project's discipline of bracketing every device change with `scripts/smoke.sh` before and after gives almost every criterion a mechanical check.

**Validation approach is realistic and unusually well-layered.** Each sub-plan declares `VAL-` identifiers and each identifier names a concrete procedure. The distinction between host-side validation (which needs nothing) and device validation (which needs the phone, sometimes the user, and always a bracket) is drawn consistently. `Faz4.6` inherits the eight-item per-measurement checklist rather than restating a ninth variant of it, and `F4.6-09` exists specifically to stop the restating.

**Dependencies are explicit.** Every section 10 names its upstream sub-plans by path and states what it needs from each. Several go further and name what they *do not* depend on — `Faz2.4` says it does not block Phase 3; `Faz8.2` says it does not depend on `Faz8.1` — which is the more useful half of a dependency statement and is rarely written down.

**Suitability for small verified slices is high.** Every sub-plan opens with a host-side or otherwise reversible first slice. `Faz4.6` is the clearest example: four work items of arithmetic and structural measurement that need neither device nor user nor attempt budget, placed first precisely because they might settle the question before anything risky happens.

**Token/context risk and subagent usefulness are stated per phase** in the index and per sub-plan where it matters. Subagents are consistently marked "not recommended", with a reason that is correct for this project — the evidence is concentrated in a few large files and the device is a single stateful resource that parallel access would corrupt.

**Where the writing is weakest.** The documents are long — 34 sub-plans averaging 175 lines, plus a 480-line ledger, a 309-line ontology and a 251-line index. The amendment style compounds this: `Faz4.4` section 1 now carries a substantial amendment paragraph before its actual context, and the index has two dated amendment sub-sections, one of which is discharged and retained. This is defensible, and the project has explicitly chosen retention over deletion so that reasoning is not lost. But a Step 4 session must read the *current* instruction out of a document that also contains the superseded one, and `AUDIT-FIX-13` existed because exactly that went wrong once. The mitigation in place — discharge banners at the head of superseded blocks — works, and should be applied to every future amendment without waiting for an audit to ask.

**No sub-plan attempts to implement code.** Each stays at the level of work items, contracts and criteria.

## 9. Scope Drift and Architectural Consistency Analysis

**One drift exists, it is material, and it is recorded rather than silent.**

Phase 4's scope is `Main-Planing.md` section 6 **plus three decision-backed additions**: the `f0000`/`f000a` active-array raise (`DEC-12`, executed as `Faz4.5`, present in the master plan only as a Phase 3 *fallback* risk note); the format-32 / `RAW_SENSOR` emission extension (`DEC-11`, absent from the master plan entirely, and a widening inside a phase whose stated goal is narrowing); and the RAW payload geometry diagnosis (`DEC-13`(a), created after the master plan was written). All three trace to measured findings from `IMPL-23` and `IMPL-30`. All three are legitimate.

`Main-Planing.md` is deliberately not edited, for a stated reason: the ledger's section 7 makes editing it a replanning trigger that would supersede `SNAP-2026-08-24-SUBPLANS` and force a full re-decomposition mid-implementation. The divergence is instead recorded in `Sub-Planing-Index.md` section 3 under Phase 4, which is the first of the two options the previous audit offered. **This closes `AUDIT-FIX-10` and the closure is correct.** The residual risk is unchanged and is stated in the index itself: a future replanning run that reads the master plan first will under-scope Phase 4 by three work streams unless it also reads the index. The proper closure remains a deliberate Step 1 amendment plus a Step 2 and Step 3 re-run at the close of Phase 4.

**No other drift.** No phase was added, removed or renamed. No sub-plan silently changes the master vision. Ownership of state is consistent with `Project-Ontology.md` throughout: the sensor layer owns the blob, the HAL layer owns the patch table, the application layer owns the smali patch, and `mode` remains the single-file runtime state. The `fullres`-as-HAL-state versus `50mp`-as-mode-name distinction is preserved in every sub-plan that touches both.

**Documentation-only work is proportionate.** Phase 1 is six sub-plans of mostly documentation, but each produced an artifact that later phases consumed — the patch-table grammar `Faz4.5` encoded against, the toolchain record that made the disassembly reproducible, the `refs/` index three later sub-plans cite. That is scaffolding, not over-documentation.

**Ontology and comprehension consistency.** `Project-Ontology.md`'s vocabulary, eleven invariants and address book are preserved by the sub-plans and were *corrected* by them where measurement contradicted the record — `IMPL-18` rewrote the `f0006` address book after finding nine recorded addresses to be false positives, and invariant 6 was recorded as "necessary but not sufficient" after `IMPL-23`. `Project-Comprehension.md` has grown to 40 evidence rows and its hypothesis states are current: `H-01` contradicted, `H-02` confirmed with an explicit qualification that the raise alone is not sufficient, `H-03` and `H-04` `probable` with their remaining probes named. The comprehension model is being maintained as evidence arrives, which is the behaviour the ledger's `R10` mitigation asks for.

**Ledger staleness is the one real inconsistency.** `Planing-Ledger.md` section 6, "Current State Snapshot", contains two sub-sections that its own section 4 and `Project-Comprehension.md` contradict. See `AUDIT-FIX-14`.

## 10. Readiness Realism

**The planning language distinguishes the levels correctly, and does so more carefully than most projects manage.**

- **Docs versus implementation.** `Faz6.1` is recorded as `complete (edit) / unverified (effect)` — the edit landed, and whether it *works* needs a build that cannot happen until Phase 7. That is the honest label, and the project chose it over the convenient one.
- **Skeleton versus working runtime.** `Faz8.1` and `Faz8.2` are explicitly low-detail and say why. Neither claims to be a port or a merge plan; both claim to be sizing exercises.
- **Local versus live readiness.** Consistently maintained. Host-side work (`verify_ln.py`, the mode-0 generator, the geometry reconstruction in `F4.6-01` … `F4.6-04`) is never described as device-proven, and device work is never claimed without a bracketed snapshot.
- **Smoke tests versus production confidence.** `scripts/smoke.sh` is described as a state reporter, not a test suite. The ledger states plainly that there is still no test framework and no CI, and that both host verifiers are run by hand.
- **Examples versus real configs.** No config example is treated as working. The two root `.agc` files are, correctly, described as *hazards* — they still carry all twelve trap key names, so importing either re-arms the trap.

**Two overclaims to watch, both already fenced by the plans themselves.**

The first is the one the project is currently living in: `Faz3.6` closed Phase 3 as **PRIMARY SUCCESS** on the strength of a reproducible 50.3 MP AGC capture, while the captured image is geometrically corrupt. That is a user decision, taken with the corruption on the record, and the ledger states it in both directions. It is not an overclaim as recorded. It becomes one the moment any downstream document says "50 MP works in AGC" without the qualifier, and `Faz9.3` exists to catch exactly that.

The second is `Faz4.1`. Its ledger row already carries the guard in bold: **"A passing `Faz4.1` is not an image fix, and must not be reported as one while `FIND-3.5-01` is open."** `Faz4.1` checks metadata integrity. It will pass on a corrupt frame. The guard is in the right place and must survive into the Step 4 run.

**No plan calls vague strategy "vibecoding".** The term appears where it means small reversible slices with fast validation, and every phase's "first useful slice" is a concrete, cheap, reversible action.

## 11. Security and Governance Findings

**Secret safety: clean.** The bundled validator's redacted scan reports zero findings across `Planner-docs/`. No token, credential, private key or local sensitive value appears in any planner document. The signing keystore is referenced by path only and its contents have never been read by any run. `IMPL-02` audited all five release archives by entry name and by keystore-size check and found all five clean.

**One open credential-hygiene item, carried and still correct.** `DEC-10` records a plaintext signing password in a shipped `build.sh`. It is recorded as a decision needing action, not as a value — the audit names the hazard and its location and nothing more. It should be closed by `Faz9.1`, which owns the build script.

**Command execution safety.** `Faz1.5`'s exhaustive WebUI trace is the model here: four `exec()` sites and two `run()` callers enumerated from source, ids constrained to source literals, with a whitelist backstop at `action.sh:108-114` before the `sh -c` interpolation at `:131`. That is a real trust-boundary analysis, not a gesture at one.

**Artifact integrity and root-privileged writes.** `R3` is the project's live risk: every module writes into `/odm` as root at `post-fs-data`. The mitigation is verified rather than assumed — `IMPL-19` established mechanically that **no write to `/odm` exists** in any module script; writes target module-private copies under `active/` and `active_hal/`, and `/odm` appears only as a bind-mount target or a read source. That makes disable-plus-reboot a complete restore for any module-caused failure, and it is documented in `docs/recovery-runbook.md` with four named failure scenarios and a per-step independence table.

**Fail-closed discipline is intact.** Size-plus-md5 guards precede every patch write; `hal_state` classifies a partial write as unrecognized; `hal_set` re-seeds from the device's stock binary; `hal_set:101` verifies md5 after every write. `Faz1.3` recorded two format hazards no code prevents — a two-column record is silently skipped, and a fourth column survives only by `dd` truncation — and routed them rather than leaving them latent.

**Approval gates.** Present where they belong and honoured in practice. `Faz5.2` required explicit user approval before mounting a candidate blob and obtained it before any device action. `DEC-13` is routed to the user rather than decided by a plan. `Faz2.4`, `Faz6.2`, `Faz7.2` and `Faz9.1` each name their required human decisions in section 10.

**Least privilege and boundaries.** Every sub-plan's Implementation Contract enumerates the exact paths it may write, with a `State` per path. That is the file-boundary mechanism the whole workflow rests on, and `AUDIT-FIX-08` was found precisely *because* the mechanism is enforced — no sub-plan held write authority for `docs/phase3-preconditions.md`, so the rule could not be landed, and the gap surfaced instead of being quietly violated. That is the boundary system working correctly.

**Local versus cloud.** Entirely local. No CI, no remote, no deploy path, no networked mutation. `DEC-01` (whether version control gains a remote) remains open and matters, because a remote changes what may be committed; it should be answered before any push, not after.

**One governance gap, new this run.** `AUDIT-FIX-15`: the measurement evidence for the project's two most recently confirmed write sites exists only in an uncommitted working tree. There is no rollback point covering it. This is a data-loss exposure against the plan's own `R1`, not a code-security issue.

## 12. Step 4 Readiness Assessment

Dependency state is assessed against the index's recommended execution order **as amended by sections 4a and 4b**, and reconciled against the ledger and the repository. `independent` means no upstream dependency. `satisfied` means every upstream dependency is either already complete in the repository or produced by an earlier row in this same queue. This is the convention the previous audit used and it is retained so the two tables compare directly.

**Twenty sub-plans are recorded COMPLETE and are not queued.** They are listed explicitly so Step 4 does not re-enter them — the Resume/Recovery protocol's "do not repeat a verified slice" rule depends on that list being visible.

**Queued rows appear in execution order.** `Faz4.6` heads the queue per `DEC-13`(a).

| Sub-Plan Path | Status | Finding IDs | Dependency State | Reason | Required Repair |
|---|---|---|---|---|---|
| Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md | READY | AUDIT-FIX-15 | independent | **First in the execution queue, per `DEC-13`(a).** Owns `FIND-4.5-02` (P1), the surviving image corruption, which is the project's live blocker. `F4.6-01` … `F4.6-04` are host-side, need neither device nor user nor attempt budget, and may settle the diagnosis outright. `F4.6-07` is correctly self-gated on `Faz4.1`; run the host-side half now and the gated half after `Faz4.1`. `F4.6-09` holds the write authority that closes `AUDIT-FIX-08` permanently. | Commit the working tree first (`AUDIT-FIX-15`) so this slice has a rollback point. The original full-resolution artifact must be recovered before structural measurement — the file in `snapshots/` is a 512x682 downscale and the sub-plan already says so. |
| Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | READY_WITH_WARNINGS | AUDIT-FIX-10 | satisfied | Unblocked: `Faz4.5` landed, and the sequencing question `DEC-12`'s half-delivered premise left open is decided in index section 4b. Runs after `Faz4.6`'s host-side half, because its format-32 extension is what unlocks `F4.6-07` and deferring it behind the whole diagnosis would deadlock the diagnosis. | Report the narrowing delta and the format-32 addition as **two numbers, never one net count**. A passing `Faz4.1` is not an image fix and must not be reported as one while `FIND-3.5-01` is open. |
| Planner-docs/Faz-4-Plans/Faz4.2-duration-rows.md | READY | none | satisfied | Depends on `Faz4.1`'s narrowed and extended entry set, which precedes it. Adds duration rows only for surviving entries. Routes the bucketing consequence to the user as `DEC-09`. | none |
| Planner-docs/Faz-4-Plans/Faz4.3-patch-table-consolidation.md | READY | none | satisfied | Depends on `Faz4.1`, `Faz4.2` and `Faz1.3`'s format contract; the first two precede it, the third is complete. Correctly constrained by `halpatch.sh`'s two-state assumption. | none |
| Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | READY | none | satisfied | Last in Phase 4. Compares against references produced earlier in the queue and by completed phases. Now also carries `FIND-4.5-01`, the global active-array raise, as `F4.4-02b` with a per-camera-id consistency table and a front-camera behavioural check. | none — `AUDIT-FIX-09` is repaired. Read the baseline from a bracketed snapshot per camera id; do not quote 508. |
| Planner-docs/Faz-2-Plans/Faz2.4-tiles-hide-disposition.md | READY | none | independent | The one Phase 2 item nothing depends on. Bounded investigation with an explicit stop point; `DEC-02` is the decision it exists to produce, not a precondition. | none |
| Planner-docs/Faz-6-Plans/Faz6.2-aon-module-disposition.md | READY | none | satisfied | `Faz6.1`'s edit is complete in both trees. Decides the module role and registers the effect verification against Phase 7 rather than deferring it silently. `DEC-04` is its output. | none |
| Planner-docs/Faz-7-Plans/Faz7.1-wsl2-provisioning.md | READY_WITH_WARNINGS | none | satisfied | Hard dependencies (`Faz1.1`, `Faz1.4`) are complete. Blocks `Faz7.2`, all of Phase 8, and the AON effect verification. | Largely host work the **user** must perform; an implementation session cannot install WSL2 unattended. Main-Planing section 9 also prefers Phases 1–5 substantively complete first, and Phase 4 is not — so schedule this after Phase 4 unless the user wants the environment front opened in parallel. |
| Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | READY | none | satisfied | Depends on `Faz7.1` absolutely, plus `Faz6.1` (complete) and `Faz6.2` (earlier in this queue). Sets a stopping rule before attempting the build. | Its three open decisions — branch, platform tree, device tree scope — are answerable only with sources in hand and must be answered at execution, not guessed beforehand. |
| Planner-docs/Faz-8-Plans/Faz8.1-beryl-port-sizing.md | READY_WITH_WARNINGS | none | satisfied | Depends on `Faz7.2`'s readiness statement, which precedes it. Sizing only; no port work is planned here. | Deliberately low-detail because the Phase 7 gate has not been passed. Expect it to require its own decomposition after the sizing decision — that is by design, not a defect. |
| Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md | READY | none | satisfied | Depends on `Faz7.1` for a Linux environment; independent of `Faz8.1`. Scoping only. | none |
| Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | READY | AUDIT-FIX-15 | satisfied | Depends on `Faz1.2`, `Faz1.5`, `Faz1.3` (all complete), on Phases 4 and 5 being settled, and on `Faz6.2`'s disposition — all either complete or earlier in this queue. Packaging assertions must be proven to fail before they are trusted; publishing is out of scope. | Close `DEC-10` here: the plaintext signing password in the shipped `build.sh` is this sub-plan's to remove. |
| Planner-docs/Faz-9-Plans/Faz9.3-documentation-consolidation.md | READY | none | satisfied | Depends on Phases 3, 4 and 5 for settled capability claims and on `Faz6.2`. Its section 10 resolves the circular dependency with `Faz9.2` by running first and performing the consistency check afterwards. | This is where the "50 MP works in AGC" claim must be corrected or qualified everywhere it appears. Do not run it before `FIND-3.5-01` and `FIND-4.5-02` have their answer. |
| Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | READY_WITH_WARNINGS | none | satisfied | Partially delivered: `IMPL-19` pulled the recovery-runbook half forward and completed `F9.2-05` … `F9.2-07`. The checklist half remains and depends on `Faz9.3`'s corrected claims and `Faz9.1`'s build script, both earlier in this queue. | Do not re-run the completed runbook items. `F9.2-04`'s known-bad demonstration needs the device and the user. |
| Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md | COMPLETE | none | satisfied | `IMPL-01`. All seven acceptance criteria pass. | none |
| Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md | COMPLETE | none | satisfied | `IMPL-02`. All five archives clean; zero keystore-class paths tracked. | none |
| Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | COMPLETE | none | satisfied | `IMPL-06`. `docs/patch-table-format.md`; four records round-tripped by hand. | none |
| Planner-docs/Faz-1-Plans/Faz1.4-toolchain-procedure-record.md | COMPLETE | AUDIT-FIX-11 | satisfied | `IMPL-07`. `docs/reverse-engineering-toolchain.md`; `VAL-TOOLCHAIN` deferred and recorded rather than reported as a pass. | none — `FIND-1.4-01`'s vocabulary work is tracked as `AUDIT-FIX-11`, not as a re-entry into this sub-plan. |
| Planner-docs/Faz-1-Plans/Faz1.5-static-safety-probes.md | COMPLETE | none | satisfied | `IMPL-05`. Exhaustive WebUI trace; three findings routed. | none |
| Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md | COMPLETE | none | satisfied | `IMPL-08`. All 36 root entries labelled, verified mechanically at 0 missing. | none |
| Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md | COMPLETE | none | satisfied | `IMPL-04`. All four validations pass on device `dc27e5d0`. | none |
| Planner-docs/Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md | COMPLETE | none | satisfied | `IMPL-09` … `IMPL-12`. All ten acceptance criteria met. | none |
| Planner-docs/Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md | COMPLETE | none | satisfied | `IMPL-13`. 10/10 layer state; 8/10 photo path, with `FIND-2.3-02` raised for the two failures. | none |
| Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md | COMPLETE | none | satisfied | `IMPL-16`. 0/12 trap keys across three runs; `FIND-3.1-01` later closed by `IMPL-18`. | none |
| Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | COMPLETE | none | satisfied | `IMPL-18`. Write site located; `H-01` contradicted; address book rewritten. | none |
| Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md | COMPLETE | none | satisfied | `IMPL-20`. Confirmed by measurement on the first attempt; reversal byte-identical. | none |
| Planner-docs/Faz-3-Plans/Faz3.4-consumer-compatibility-check.md | COMPLETE | none | satisfied | `IMPL-21`, `IMPL-22`. Survey complete on both bases; three findings raised, none attributable to the patch. | none |
| Planner-docs/Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md | COMPLETE | none | satisfied | `IMPL-23`. libgcam gate cleared; `FIND-3.5-01` raised and still open — owned now by `Faz4.6`. | none |
| Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md | COMPLETE | none | satisfied | `IMPL-24`. Phase 3 closed by user decision as PRIMARY SUCCESS, with the corruption on the record. | none |
| Planner-docs/Faz-4-Plans/Faz4.5-active-array-raise.md | COMPLETE | none | satisfied | `IMPL-27` … `IMPL-30`. Both write sites confirmed by measurement; twelve of thirteen criteria met, the thirteenth explicitly left open. Three items routed and none silently dropped. | none |
| Planner-docs/Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md | COMPLETE | none | satisfied | `IMPL-14`. All nine criteria met; generation deterministic. | none |
| Planner-docs/Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md | COMPLETE | none | satisfied | `IMPL-15`. Composition proven; user approval obtained before any device action. | none |
| Planner-docs/Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md | COMPLETE | none | satisfied | `IMPL-17`. Disposition RETAIN; `TRACE-06` closed. Phase 5 closed. | none |
| Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md | COMPLETE | none | satisfied | `IMPL-03`. Edit landed in both trees, CRLF preserved. **Effect unverified until Phase 7 — registered by `Faz6.2`, not assumed.** | none |

**Execution queue state: READY.** Fourteen rows are queued — four `READY_WITH_WARNINGS` free of any P0/P1 finding and ten `READY` — and twenty are `COMPLETE` and excluded. No global execution blocker, unsafe path, missing target or unresolved dependency applies. The queue is headed by `Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md`, host-side half.

## 13. Priority Fix List

No P0 or P1 audit finding was identified. Sixteen findings are listed: twelve `resolved` and four `open`. The resolved ones are retained so the trail is not lost, and because several were resolved by execution rather than by editing, which is worth being able to see.

| Finding ID | Severity | Status | Affected Files | Issue | Required Action |
|---|---|---|---|---|---|
| AUDIT-FIX-15 | P2 | open | (repository state; no single planner file) | Every artifact of the 2026-09-01 execution and re-plan is uncommitted. `HEAD` is `947a01b`, "Faz 4.1 blocked at pre-execution review", which predates `IMPL-27` … `IMPL-30`. Uncommitted: six modified `Planner-docs` files (`Faz4.1`, `Faz4.4`, the ledger, comprehension, ontology, index), two untracked sub-plans (`Faz4.5`, `Faz4.6`), `agc-50mp-yama/hal-activearray-deneme.patch`, a modified `agc-50mp-yama/README.md`, and eight `snapshots/` artifacts including the `f4509` capture. Those snapshots are the measurement evidence the ledger cites for **both** confirmed write sites. `R1` is the plan's own critical risk, and its mitigation currently does not cover the most expensive day of work in the project. The ledger's "the repository wins" rule keeps this from being *dangerous* to a fresh session, which reads the working tree — but a single overwrite or a bad revert loses it, and there is no point to fall back to. | Commit the working tree before the next slice begins. One commit for the Phase 4 execution evidence and one for the planning-run 6 documents, or a single commit — either is fine; having none is not. Do this before `Faz4.6` starts, so its host-side half has a rollback point. |
| AUDIT-FIX-14 | P2 | open | Planner-docs/Planing-Ledger.md | Section 6, "Current State Snapshot", carries claims its own section 4 and `Project-Comprehension.md` contradict. Its **Repository** paragraph reads "Branch `main`, one commit `ff6934e`, 86 tracked files, `size-pack` 455.20 KiB, clean working tree" — measured now: **24 commits**, HEAD `947a01b`, **143 tracked files**, working tree **not clean**. Its **Open hypotheses** paragraph reads "`H-01` through `H-10` are all `tentative`" — `Project-Comprehension.md` section 8 records `H-01` contradicted, `H-02` confirmed, `H-03` and `H-04` `probable`, each with the probe that moved it. The adjacent **Open ontology questions** paragraph is stale in the same way but is at least scoped by its own heading to "at the close of Step 2"; the other two are not scoped and read as current. Section 6 is the section a fresh Step 4 session reads to learn where the project is. | Re-measure and rewrite the Repository paragraph, or scope it to its date the way the ontology paragraph is scoped. Replace the Open hypotheses paragraph with a pointer to `Project-Comprehension.md` section 8 rather than a duplicated summary that will go stale again — a second copy of a fast-moving fact is what created this finding. |
| AUDIT-FIX-11 | P3 | open | Planner-docs/Project-Comprehension.md, Planner-docs/Planing-Ledger.md, Planner-docs/Project-Ontology.md | Carried, unchanged, and re-measured this run: the validator still reports **eleven** warnings, all vocabulary non-conformance in the continuity artifacts, each promoted to an error by `--strict`. Ontology question statuses: `answered (no)` twice and `partially_answered, and the previous answer is now in doubt` once, against `answered` / `partially_answered` / `open` / `contradicted`. Comprehension confidence values: `**contradicted**` — the correct word carrying bold markers — and `confirmed (as an edit) / unverified (as a fix)`, against `confirmed` / `probable` / `tentative` / `contradicted`. Ledger statuses: `complete` three times and `complete (edit) / unverified (effect)` once, against an allowed set containing `implemented` and `verified` but not `complete`. Two further warnings ask for direct evidence on `EV-03` and history evidence on `EV-14`. This is `FIND-1.4-01`. **The consequence that is not cosmetic:** the ledger parser skips to the next row on an unrecognized status, so those four rows are never checked for sub-plan path existence or path safety. Note also that the compound values are, in substance, *more* honest than any single allowed one. | Map each value to an allowed one and carry the nuance in the adjacent free-text column: `answered (no)` to `answered`; `partially_answered, …in doubt` to `partially_answered`; `**contradicted**` to `contradicted`; `confirmed (as an edit) / unverified (as a fix)` to `confirmed`; `complete` to `verified` or `implemented`; `complete (edit) / unverified (effect)` to `implemented`, with the effect caveat in Validation Evidence. Then re-run the validator and confirm the count drops to zero, so `FIND-1.4-01`'s baseline becomes zero rather than eleven. Run it as `python`, not `python3`. |
| AUDIT-FIX-16 | P3 | open | Planner-docs/Planing-Ledger.md | The Sub-Plan Status Matrix lists Phase 4 in the order `Faz4.1`, `Faz4.2`, `Faz4.3`, `Faz4.4`, `Faz4.6`, `Faz4.5` — neither numeric order nor execution order. Every other phase is in numeric order. `Faz4.5`, the only Phase 4 row that is complete, is last, and `Faz4.6`, the head of the whole execution queue, sits between `Faz4.4` and it. Nothing is wrong in content; a reader scanning for the current Phase 4 state has to read all six rows to be sure. | Move the `Faz4.5` row above `Faz4.6` so the phase reads in numeric order, matching the other eight phases. Cosmetic; do it during the next ledger update rather than as its own slice. |
| AUDIT-FIX-05 | P3 | resolved | Planner-docs/Sub-Planing-Index.md | Section 2 stated ten competency questions were open at Step 2; eleven were. | **Resolved 2026-09-01 by planning run 6.** Section 2 now reads eleven open, one partially answered, four answered, with a parenthetical recording the correction and scoping the sentence to the Step 2 moment. |
| AUDIT-FIX-06 | P2 | resolved | Planner-docs/Planing-Ledger.md | The 2026-09-01 re-plan had not updated the ledger: no planning-run row, snapshot count stale at 32, and no Sub-Plan Status Matrix row for `Faz4.5` at all. | **Resolved.** Section 2 now carries rows 4, 5 and 6. Section 3 reads 34 with both corrections narrated and the amend-rather-than-supersede reasoning stated. Section 4 carries a `Faz4.5` row, now at `verified`. |
| AUDIT-FIX-07 | P2 | resolved | Planner-docs/Planing-Ledger.md, Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | `Faz4.1`'s ledger row still read `blocked` after all three of its blocker conditions had landed. | **Resolved.** The row is `planned`, cites the re-plan as the discharging event, records the unblocking by `IMPL-27` … `IMPL-30`, and replaces the blocker text with the sequencing decision from index section 4b — including the guard that a passing `Faz4.1` is not an image fix. |
| AUDIT-FIX-08 | P2 | resolved | Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md, Planner-docs/Faz-4-Plans/Faz4.5-active-array-raise.md | `FIND-3.4-03`'s crash-contamination rule could not be landed in `docs/phase3-preconditions.md`, because no sub-plan in the queue held write authority for that file. | **Resolved at the mechanism, in two stages.** Interim: `Faz4.5` section 9 restated the rule inline as item 8, recorded that it is knowingly absent from the file, and barred `F4.5-07` from starting without it. Permanent: `Faz4.6` carries `docs/phase3-preconditions.md` as `modified` in its Implementation Contract and `F4.6-09` lands the item plus the `adbd` self-echo caveat. No further audit action; execution of `F4.6-09` closes it in the repository. |
| AUDIT-FIX-09 | P2 | resolved | Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | Three unqualified "508 baseline" references survived in the sub-plan whose entire job is reporting the array count as a number. | **Resolved, and better than the finding asked for.** All three are qualified or removed. Section 1 goes further and records that the two recorded figures *disagree* — `EV-16`'s 508 → 868 against `IMPL-30`'s hal3 500 → 868 — states that the eight-entry difference is unsettled, and forbids quoting any baseline in favour of reading one from a bracketed snapshot per camera id. |
| AUDIT-FIX-10 | P2 | resolved | Planner-docs/Sub-Planing-Index.md | Phase 4's scope had diverged from `Main-Planing.md` with no record of the divergence. | **Resolved by the first of the two options offered.** Index section 3 now states under Phase 4 that its scope is `Main-Planing.md` section 6 plus `DEC-11`, `DEC-12` and `DEC-13`(a), names all three additions, explains why the master plan is deliberately not edited, and records that a Step 1 amendment plus Step 2/3 re-run at the close of Phase 4 remains the correct final closure. |
| AUDIT-FIX-12 | P3 | resolved | Planner-docs/Planing-Ledger.md | The `Faz2.3` matrix row had twelve cells where the header defines nine. | **Resolved.** A cell-count scan over every matrix row now returns nine for all of them. |
| AUDIT-FIX-13 | P3 | resolved | Planner-docs/Sub-Planing-Index.md | Section 4a presented a discharged "revised next-up order" as the most recent-looking guidance in the index. | **Resolved.** A bold discharge banner heads section 4a, names both closures with their dates and run IDs, says "do not read this section as current guidance", points to section 4b and to this audit's section 12, and states why the amendment is retained rather than deleted. |
| AUDIT-FIX-01 | P2 | resolved | Planner-docs/Sub-Planing-Index.md, Planner-docs/Planing-Ledger.md, Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md, Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md, Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | `OQ-10`, `OQ-12`, `CQ-03`, `CQ-08` and `CQ-14` were unnamed by identifier in any sub-plan. | **Resolved by execution.** `IMPL-24` discharged the requirement at the `Faz3.6` gate with all nine tracked questions carrying non-open states. Retained from the 2026-08-24 audit. |
| AUDIT-FIX-02 | P2 | resolved | Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md, Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md, Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | `R3`'s stock-restore mitigation lived only in `Faz9.2` at queue position 13, behind three phases that patch a system binary. | **Resolved.** `IMPL-19` split the recovery-runbook half forward and delivered `docs/recovery-runbook.md` before `Faz3.3` executed, with its central claim verified mechanically. Retained from the 2026-08-24 audit. |
| AUDIT-FIX-03 | P3 | resolved | Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | `Faz3.2` named `CQ-05` and `H-01` but not `OQ-01`. | **Resolved.** `IMPL-18` answered `OQ-01` in place and updated the register in the session that produced the answer. Retained from the 2026-08-24 audit. |
| AUDIT-FIX-04 | P3 | resolved | Planner-docs/Sub-Planing-Index.md, Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md, Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, Planner-docs/Faz-8-Plans/Faz8.1-beryl-port-sizing.md | `Faz1.6` sat outside the numbered execution order while three later sub-plans depended on its `refs/` index. | **Resolved and closed in the ledger by `IMPL-08`.** `README.md` indexes five `refs/` trees with the basis quoted for each. Retained from the 2026-08-24 audit. |

**Finding status consistency.** Four findings are `open`, two P2 and two P3; twelve are `resolved`. No P0 or P1 audit finding exists in either state. Per the contract this yields `PASS_WITH_WARNINGS`, and the four open findings must remain visible throughout the Step 4 implementation run.

**A note on the one open P1 in the project.** `FIND-4.5-02`, the surviving image corruption, is a P1 **project** finding, not an audit finding. It is open, it is the reason `Faz4.6` exists, and it is the head of the execution queue. It does not gate Step 4 — it *is* Step 4's next work. Do not confuse it with an audit P1, which would block.

## 14. Recommended Next Command / Prompt

**Audit status is `PASS_WITH_WARNINGS` with only P2 and P3 findings open, so the Step 4 prompt is printed.**

First in the implementation queue: **`Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md`**, host-side half, work items `F4.6-01` … `F4.6-04`. It needs neither the device nor the user, has no attempt budget attached, and may settle `FIND-4.5-02` outright.

**Before the first slice, commit the working tree** (`AUDIT-FIX-15`). This is repository hygiene, not a plan change, and it gives the first slice a rollback point.

Copy the following into a fresh Claude Code session:

```text
/claudeqb:claudeqb Read and return the exact canonical handoff from references/handoffs/run-step4.md, then execute it.
```

**Queue continuation.** Step 4 must work through the READY / READY_WITH_WARNINGS queue in this audit's section 12 continuously, in small verified slices, checkpointing after each rather than stopping after the first success. Fourteen rows are queued; twenty are `COMPLETE` and must not be re-entered.

**Token and context discipline.** Do not load all thirty-four sub-plans. Navigate by this audit's section 12 and the index; read only the active sub-plan, plus only the `Project-Comprehension.md` `CQ`/`TRACE`/`ARC`/`HYP` rows relevant to the active slice. Phase 4 is banded medium; `Faz4.6` is arithmetic and filtered log reads rather than a search, which is why it is cheaper than `Faz4.5` was. Refresh queue status from this audit between slices.

**Carry these four open findings visibly through the run:** `AUDIT-FIX-15` (commit the tree), `AUDIT-FIX-14` (ledger section 6 is stale), `AUDIT-FIX-11` (eleven validator vocabulary warnings), `AUDIT-FIX-16` (Phase 4 ledger row order).

## 15. Audit Result

**Final status: PASS_WITH_WARNINGS.**

**Confidence: high.** Every structural claim in this audit was produced by a command run in this session against the files on disk — heading sequences, filename patterns, folder/H1 number agreement, contract-table headers and `State` vocabulary, empty-section and placeholder scans, index reference resolution in both directions, ledger row cell counts, git commit and tracked-file counts, and the bundled validator in `--mode step3-preflight --strict`. No count in this document is reported from memory. Confidence is high on structure, coverage, index accuracy and readiness sequencing. It is necessarily lower on the technical correctness of the measurements the sub-plans record — addresses, md5 values, capture geometries — because those were taken as reported rather than re-derived, which is the correct boundary for an audit step.

**Only `Planner-docs/Sub-Planing-Audit.md` was modified by this Step 3 run.**

**Unexpected modifications: none introduced by this run.** The working tree was already dirty when the audit began, from the 2026-09-01 Phase 4 execution and planning run 6 — six modified `Planner-docs` files, two untracked sub-plans, and untracked evidence under `snapshots/` and `agc-50mp-yama/`. That pre-existing state is recorded as `AUDIT-FIX-15` rather than treated as an anomaly of this run, and nothing in it was touched.

**Step 4 can safely begin,** at `Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md`, host-side half, after the working tree is committed.
