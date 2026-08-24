# Sub-Planing Audit

> Step 3 audit — ClaudeQB. Body language: English (default contract).
> The project's user-facing documents and module interface remain Turkish and English; that convention is unchanged.

## 1. Audit Summary

**Overall audit status: PASS_WITH_WARNINGS.**

Step 2's output is structurally complete and substantively strong. All nine master-plan phases have a folder, all thirty-two sub-plans carry the thirteen required sections in the required order with a machine-readable Implementation Contract table, the index resolves in both directions, numbering is contiguous with no gaps or duplicates, and no secret pattern appears anywhere under `Planner-docs/`. Phase order, phase names, vision, and target end state are preserved from `Main-Planing.md` without drift. Acceptance criteria are unusually good for a planning artifact: they are stated as measurable conditions with named commands, numeric targets, and explicit "record the negative result" branches rather than as intentions.

**Step 2 output is usable for Step 4.** No P0 or P1 finding exists. Five findings are recorded, two at P2 and three at P3, none of which blocks the start of implementation.

**Most important finding.** `AUTOPSY`-derived risk `R3` in `Main-Planing.md` states its mitigation as "add an explicit stock-restore path to the smoke script", and the target end state repeats it. Step 2 made `Faz-2-Plans/Faz2.1-device-smoke-script.md` strictly read-only by design — a defensible and well-argued choice — but then placed the only written recovery runbook in `Faz-9-Plans/Faz9.2-release-verification-checklist.md`, at position 13 of the recommended execution order. The consequence is that Phases 3, 4, and 5 patch a system binary on the user's daily-driver device with per-change reversal proven (`Faz3.3`, `Faz5.2`) but with no written recovery path for the case where the module itself is non-functional. This is a scheduling divergence from the master plan's own stated mitigation, not a defect in any individual sub-plan.

**Most important remediation action.** Before `Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md` executes, either pull the recovery-runbook portion of `Faz9.2` forward, or record in `Faz2.1` and `Faz3.3` that the master plan's `R3` mitigation is deliberately deferred and state what stands in its place. Step 4 may begin at `Faz-1-Plans/Faz1.1-version-control-bootstrap.md` without waiting for this.

## 2. Reviewed Sources

**Files inspected in full.** `Planner-docs/Main-Planing.md`; `Planner-docs/Sub-Planing-Index.md`; `Planner-docs/Planing-Ledger.md`; `Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md`; the competency-question register of `Planner-docs/Project-Ontology.md` section 8; sections 1 and 8 of `Planner-docs/Project-Comprehension.md`.

**Files inspected structurally and by extracted section.** All thirty-two sub-plan files. For every one of them, the heading set and order, the H1 title, the body length of all thirteen sections, the Goal, the Acceptance Criteria, the Dependencies and Sequencing text, and the Implementation Contract table were read. `Planner-docs/Autopsy.md` was used as an ID source and cross-reference target rather than re-read in full, since Step 2 recorded its feedback and this audit verified that record against the sub-plans.

**Folders inspected.** `Planner-docs/` and all nine `Planner-docs/Faz-<n>-Plans/` folders; the workspace root listing for evidence-claim checks.

**Important commands run.** `find Planner-docs -maxdepth 4 -type f | sort` (38 files); `find Planner-docs -name "*.md" -printf "%s\t%p\n"`; `git status --short` and `git branch --show-current` at the workspace root, both returning `fatal: not a git repository`; a cross-reference extraction of every `CQ-`, `EV-`, `TRACE-`, `ARC-`, `QAS-`, `H-`, `OQ-`, and `AUTOPSY-` identifier appearing in the sub-plans, compared against the identifiers defined in the continuity artifacts; per-identifier reverse routing lookups for `OQ-01` through `OQ-12`, `CQ-01` through `CQ-14`, and `H-01` through `H-10`; a length-bounded secret scan; and targeted scans for readiness overclaims, destructive or auto-merge operations, and premature publishing language.

**Validator status.** The bundled validator at `scripts/validate_planner_docs.py` could not be executed. No Python interpreter is available on this host: `python` and `python3` resolve only to the Windows Store alias stub and `py` is absent. This is the same limitation Step 2 recorded, and it is itself an evidenced project fact carried by `Faz-1-Plans/Faz1.4-toolchain-procedure-record.md` and `Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md`. Equivalent all-file validation was performed instead by a read-only reimplementation of the validator's `step2`, `step3-preflight`, `step3`, and `step4` modes, built from the bundled script's own rule set: required heading sets and order for every artifact type, duplicate-heading detection, fenced-code-aware heading parsing, phase-folder and filename conventions, folder-to-file phase matching, H1-to-filename matching, thirteen-section presence with the twenty-character minimum body length, placeholder-pattern detection, contiguous sub-plan numbering, bidirectional index reference resolution, repeated-body and repeated-sentence boilerplate detection, Implementation Contract header matching with allowed path states and repo-relative path safety, Ledger v2 status-matrix row rules, ontology and comprehension table rules, and the same length-bounded secret patterns. The fallback is reported here and in section 15.

**Preflight result.** The equivalent `step3-preflight --strict` run reported `planner_docs_validation=passed`, `error_count=0`, `warning_count=0`, `main_phase_count=9`, `phase_folder_count=9`, `subplan_count=32`, `index_reference_count=32`, `ledger_schema=v2`, `secret_findings=0`, and `audit_exists=false`.

**Things not verified.** The contents of any file outside `Planner-docs/` were not re-derived; where a sub-plan cites repository evidence, this audit checked internal consistency and plausibility against the Step 1 and Step 1.5 records rather than re-measuring the workspace. The bundled Python validator's behavior was reproduced from its source, not observed. No device, build, or network state was queried. No secret value was read; the signing keystore is referenced by path only, exactly as the sub-plans do.

## 3. Main Phase Coverage Analysis

Phase numbers and headings are taken from the roadmap table in section 6 of `Planner-docs/Main-Planing.md`, confirmed against the nine `### Phase <n>` headings in the same section. Counts are reported from the file listing, not from memory.

| Main phase no | Main phase heading | Expected folder | Folder exists? | Sub-plan count | Coverage status | Notes |
|---|---|---|---|---|---|---|
| 1 | Workspace safety net | `Planner-docs/Faz-1-Plans` | Yes | 6 | OK | Covers version control, keystore containment, the patch-table contract, the toolchain record, the static probe batch, and the README. Every element of the master phase description is decomposed. |
| 2 | Ship and re-baseline v2.1 | `Planner-docs/Faz-2-Plans` | Yes | 4 | OK | Includes the smoke script pulled forward from Phase 9, which the master plan requests in three separate places. The pull-forward is documented in the index rather than performed silently. |
| 3 | 50 MP end-to-end in AGC | `Planner-docs/Faz-3-Plans` | Yes | 6 | OK | The critical path, sliced tightly as the master plan's risk `R4` and `R10` require: preconditions, static search, single-word proof, consumer survey, capture, decision gate. |
| 4 | Minimal correct HAL patch | `Planner-docs/Faz-4-Plans` | Yes | 4 | OK | Narrowing, duration rows, consolidation, validation. Ordering matches the master plan's requirement that narrowing precede duration rows. |
| 5 | Mode-0 12-bit composition | `Planner-docs/Faz-5-Plans` | Yes | 3 | OK | Host-side generation, temporary-mount test, exclusion disposition. The single-purpose revertibility the master plan demands is preserved. |
| 6 | AON fix upstreaming | `Planner-docs/Faz-6-Plans` | Yes | 2 | OK | The one-line symlink entry and the module disposition. Early scheduling is honored in the index execution order without renumbering the phase. |
| 7 | Android 16 build environment | `Planner-docs/Faz-7-Plans` | Yes | 2 | OK | Deliberately lower detail, matching `Main-Planing.md` section 9's "do not expand yet" instruction. |
| 8 | beryl port + kernel LTS | `Planner-docs/Faz-8-Plans` | Yes | 2 | OK | Scoping only, with both commit decisions routed to the user. The sub-plans state their own low-detail status and its reason. |
| 9 | Release engineering | `Planner-docs/Faz-9-Plans` | Yes | 3 | OK | Build script, verification checklist with recovery runbook, documentation consolidation. The smoke script's relocation to Phase 2 is accounted for. |

No phase is missing, no phase folder exists without a corresponding master phase, and no phase has zero sub-plans. Total sub-plan count: 32.

Element-level coverage was also checked against the master plan's section 8 prioritized next steps. All ten map to a named sub-plan: steps 1 and 6 to `Faz1.1` and `Faz1.2`, step 2 to `Faz2.1`, step 3 to `Faz2.2`, step 4 to `Faz6.1`, step 5 to `Faz3.2`, step 7 to `Faz4.1`, step 8 to `Faz1.6`, step 9 to `Faz1.4`, and step 10 to `Faz2.4`.

## 4. Sub-Plan File Inventory

Every file below was checked for H1 correctness, section structure, and content quality. "Structure OK" means all thirteen required sections are present, uniquely, in order, each with a substantive body.

**`Planner-docs/Faz-1-Plans/` — 6 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz1.1-version-control-bootstrap.md` | Faz 1.1 — Version Control Bootstrap | OK | OK | Strong | Read in full. Six work items, seven measurable acceptance criteria, five named risks each with impact and mitigation. The keystore ignore rule is correctly pulled into this sub-phase as the single ordering constraint inside Phase 1. |
| `Faz1.2-signing-key-containment.md` | Faz 1.2 — Signing Key Containment | OK | OK | Strong | Audits by entry name only; never reads key material. Correctly gates the remote decision. |
| `Faz1.3-patch-table-format-contract.md` | Faz 1.3 — Patch Table Format Contract | OK | OK | Strong | Acceptance requires a hand round-trip of three real records, which is a genuine proof rather than a review. |
| `Faz1.4-toolchain-procedure-record.md` | Faz 1.4 — Toolchain Procedure Record | OK | OK | Strong | Requires the four negative findings as explicit non-steps and a self-check that decodes the four recorded `cmp` sites. |
| `Faz1.5-static-safety-probes.md` | Faz 1.5 — Static Safety Probes | OK | OK | Strong | Batches six cheap static questions. Acceptance forbids sampling for the WebUI trace and forbids deferring write-up. |
| `Faz1.6-workspace-readme-and-refs-index.md` | Faz 1.6 — Workspace README and Reference Tree Index | OK | OK | Strong | Requires inferred `refs/` roles to be marked as inferred. See finding `AUDIT-FIX-04` on its scheduling. |

**`Planner-docs/Faz-2-Plans/` — 4 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz2.1-device-smoke-script.md` | Faz 2.1 — Device Smoke Script | OK | OK | Strong | Nine field groups, read-only by explicit design, idempotence and sensitivity both required as acceptance. See `AUDIT-FIX-01` and `AUDIT-FIX-02`. |
| `Faz2.2-flash-v21-and-baseline-snapshot.md` | Faz 2.2 — Flash v2.1 and Capture the Baseline Snapshot | OK | OK | Strong | Requires every diff line to have a written explanation, with "no change dismissed as noise" stated. |
| `Faz2.3-ten-mode-regression-pass.md` | Faz 2.3 — Ten-Mode Regression Pass | OK | OK | Strong | Treats a black preview as a failure, not a warning, tying it to the restart-ordering invariant. Forbids inline fixes. |
| `Faz2.4-tiles-hide-disposition.md` | Faz 2.4 — Tiles Hide Option Disposition | OK | OK | Strong | Bounded investigation with an explicit stop point; the four functional tiles are explicitly protected. |

**`Planner-docs/Faz-3-Plans/` — 6 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz3.1-preference-trap-clearance.md` | Faz 3.1 — Preference Trap Clearance and Phase Preconditions | OK | OK | Strong | Establishes four preconditions and the attempt budget once, rather than restating them in four sub-plans. |
| `Faz3.2-pixel-array-write-site-search.md` | Faz 3.2 — Pixel Array Size Write Site Search | OK | OK | Strong | Static, no device. Requires immediate ontology recording and treats budget exhaustion as a completed outcome. See `AUDIT-FIX-03`. |
| `Faz3.3-single-word-patch-and-metadata-proof.md` | Faz 3.3 — Single Word Patch and Metadata Proof | OK | OK | Strong | One word per attempt, three snapshots, reversal demonstrated rather than asserted. See `AUDIT-FIX-02`. |
| `Faz3.4-consumer-compatibility-check.md` | Faz 3.4 — Consumer Compatibility Check | OK | OK | Strong | Deliberately precedes the AGC capture so a success cannot mask an unmeasured consumer cost. The reasoning is stated. |
| `Faz3.5-agc-capture-and-image-evidence.md` | Faz 3.5 — AGC Capture and Image Evidence | OK | OK | Strong | Log filtering configured before launch; the tile is the only permitted switch, which is what makes the result HAL-driven. |
| `Faz3.6-fallback-decision-gate.md` | Faz 3.6 — Fallback Decision Gate | OK | OK | Strong | Runs regardless of outcome. Requires every tracked question to have a non-open state, with explicit "undetermined" allowed. See `AUDIT-FIX-01`. |

**`Planner-docs/Faz-4-Plans/` — 4 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz4.1-fullres-dimension-guard.md` | Faz 4.1 — Full Resolution Dimension Guard | OK | OK | Strong | Requires the target array count as a number before any patch, then one-site measurement before extending. |
| `Faz4.2-duration-rows.md` | Faz 4.2 — Minimum Frame and Stall Duration Rows | OK | OK | Strong | Forbids invented values; routes the bucketing consequence to the user as `DEC-09`. |
| `Faz4.3-patch-table-consolidation.md` | Faz 4.3 — Patch Table Consolidation and Relocation | OK | OK | Strong | Checksums recomputed by application, not transcribed. Superseded tables must be removed or marked. |
| `Faz4.4-patch-compatibility-validation.md` | Faz 4.4 — Consolidated Patch Compatibility Validation | OK | OK | Strong | Compares against three recorded references; failures are routed, not repaired here. |

**`Planner-docs/Faz-5-Plans/` — 3 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz5.1-twelve-bit-mode-zero-blob.md` | Faz 5.1 — Twelve Bit Mode Zero Blob Generation | OK | OK | Strong | Host-side only. Requires encodings read from real blobs rather than assumed, and an exact byte-count check. |
| `Faz5.2-temporary-mount-composition-test.md` | Faz 5.2 — Temporary Mount Composition Test | OK | OK | Strong | Temporary mount with a post-test snapshot required to match the pre-test snapshot. Revertibility is what justifies the risk. |
| `Faz5.3-exclusion-rule-disposition.md` | Faz 5.3 — Exclusion Rule Disposition | OK | OK | Strong | Requires the tile application's mechanism to be established rather than assumed — an honest acknowledgement that no run has read those sources. |

**`Planner-docs/Faz-6-Plans/` — 2 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz6.1-symlink-entry-in-device-trees.md` | Faz 6.1 — SYMLINK Entry in Device Trees | OK | OK | Strong | Syntax must be cited, not assumed; the unverified status is a required acceptance criterion. See `AUDIT-FIX-04`. |
| `Faz6.2-aon-module-disposition.md` | Faz 6.2 — AON Module Disposition and Build Verification | OK | OK | Strong | Decides now, schedules the proof against Phase 7. All three roles must be evaluated, not just the recommended one. |

**`Planner-docs/Faz-7-Plans/` — 2 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz7.1-wsl2-provisioning.md` | Faz 7.1 — WSL2 Provisioning and Toolchain Smoke | OK | OK | Good | Verified by a real build action rather than by the environment's existence. Case-sensitivity confirmed by direct test. |
| `Faz7.2-first-aospa-build.md` | Faz 7.2 — First AOSPA Build Attempt | OK | OK | Good | Stopping rule recorded before the build begins; reaching it is a bounded outcome, not a failure. See `AUDIT-FIX-04`. |

**`Planner-docs/Faz-8-Plans/` — 2 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz8.1-beryl-port-sizing.md` | Faz 8.1 — Beryl Port Sizing | OK | OK | Good | Sizing only. Carries the roadmap's single sanctioned subagent exception, correctly scoped to one work item. See `AUDIT-FIX-04`. |
| `Faz8.2-kernel-lts-merge-scoping.md` | Faz 8.2 — Kernel LTS Merge Scoping | OK | OK | Good | Requires a specific finding on the CSIPHY and CSID allocation paths rather than a general statement, tying it to invariant 3. |

**`Planner-docs/Faz-9-Plans/` — 3 files.**

| File | Detected H1 | Phase match | Structure | Content quality | Notes |
|---|---|---|---|---|---|
| `Faz9.1-reproducible-release-build.md` | Faz 9.1 — Reproducible Release Build | OK | OK | Strong | Packaging assertions must be proven to fail when their condition is introduced. Publishing is explicitly out of scope. See `AUDIT-FIX-01`. |
| `Faz9.2-release-verification-checklist.md` | Faz 9.2 — Release Verification Checklist and Recovery Runbook | OK | OK | Strong | Runbook steps must be verified independent of module-provided commands; the stacked-mount false-restore case is covered. See `AUDIT-FIX-02`. |
| `Faz9.3-documentation-consolidation.md` | Faz 9.3 — Documentation Consolidation and Stale Claim Correction | OK | OK | Strong | Corrects the `EV-23` contradicted claim across all four documentation surfaces; nothing in the journal is deleted. |

## 5. Naming and Sequencing Check

**No naming or ordering issues were found.**

Folder naming: all nine folders match `Faz-<n>-Plans` exactly, with `n` running 1 through 9. No invalid folder, no duplicate phase folder, no folder without a corresponding master phase.

Filename naming: all thirty-two filenames match `Faz<phase>.<sub>-<ascii-lowercase-kebab-slug>.md`. No spaces, no non-ASCII characters, no uppercase in any slug, no duplicate filename. Every slug is descriptive of the sub-phase's actual work — `version-control-bootstrap`, `pixel-array-write-site-search`, `twelve-bit-mode-zero-blob` — with no generic slugs such as `part1` or `misc`.

Folder-to-file phase agreement: every file's phase number matches its containing folder's number. No `Faz-2-Plans` file carries a `Faz3.x` name.

H1-to-filename agreement: every file's H1 matches the pattern `# Faz <n>.<m> — <Title>` and both numbers agree with the filename. No mismatch was found.

Numbering contiguity: Phase 1 has 1–6, Phase 2 has 1–4, Phase 3 has 1–6, Phase 4 has 1–4, Phase 5 has 1–3, Phase 6 has 1–2, Phase 7 has 1–2, Phase 8 has 1–2, Phase 9 has 1–3. No gaps, no duplicates.

Order consistency: the folder order preserves the master roadmap's phase order. The index's recommended execution order deliberately departs from numbered order in two places — the smoke script pulled forward from Phase 9 into Phase 2, and Phase 6 scheduled early — and both departures are explained in the index with their source in `Main-Planing.md` and `Autopsy.md`. Neither renumbers a phase. This is correct handling.

## 6. Index Consistency Check

`Planner-docs/Sub-Planing-Index.md` carries all seven required sections in order and resolves cleanly against the filesystem.

**Missing references: none.** All thirty-two sub-plan files are referenced from the index.

**Broken references: none.** All thirty-two index references resolve to an existing file. The reference count and the actual file count both equal 32.

**Unindexed files: none.**

**Phase count: matches.** The index reports 9, derived from the roadmap table rows and confirmed against the phase headings; the master plan has 9; nine folders exist.

**Coverage claims: accurate with one exception.** Every checkbox in section 6 of the index was independently verified and holds, including the per-phase counts (6, 4, 6, 4, 3, 2, 2, 2, 3 totalling 32), the contiguity claim, the Implementation Contract claim, and the secret-safety claim. The exception is in section 2, where the index states the ontology carries "sixteen competency questions of which ten were open at Step 2". Sixteen is correct; the open count is eleven, since `OQ-01` through `OQ-11` all read `open` and `OQ-12` reads `partially_answered`. Recorded as `AUDIT-FIX-05`.

**Execution order: plausible and internally consistent.** Every dependency asserted in a sub-plan's section 10 is satisfied by the index's ordering. Spot checks: `Faz1.5` (position 5) precedes `Faz2.2` (position 6), which depends on its install-state answer; `Faz1.4` (position 8) precedes Phase 3 (position 9), which depends on its disassembler; `Faz1.2` (position 2) precedes `Faz1.4` (position 8), which depends on its key-location policy; `Faz1.3` (position 8) precedes `Faz4.3` (position 10), which it governs; `Faz9.1` and `Faz9.3` precede `Faz9.2`, resolving the stated two-way interaction between `Faz9.2` and `Faz9.3` in the direction both sub-plans recommend. No cycle exists. The one soft-ordering friction concerns `Faz1.6` and is recorded as `AUDIT-FIX-04`.

**Deferred-topic list: honest.** Section 5 names ten deferred topics, each with a reason, and each reason is traceable to `Main-Planing.md`, `Autopsy.md`, or a stated cost argument. Continuous integration is declined with an explicit justification rather than omitted silently.

## 7. Required Section Structure Check

All thirty-two sub-plans were checked programmatically, not sampled. The check was a fenced-code-aware heading parse followed by exact-string matching against the thirteen required headings in required order, plus a duplicate count and a body-length measurement per section.

**Missing sections: none.** Every one of the thirty-two files contains all thirteen required top-level sections.

**Wrong order: none.** In every file the thirteen headings appear in the required sequence, preceded by a conforming H1.

**Duplicated sections: none.** No required heading appears more than once in any file.

**Empty sections: none.** The shortest section body across the entire set is 175 characters, in `Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md` section 2, which is a complete and specific goal statement rather than a stub. The validator's threshold is 20 characters; no section is within an order of magnitude of it.

**Placeholder sections: none.** No `TODO`, `TBD`, `FIXME`, `lorem ipsum`, "to be filled", angle-bracket placeholder, or brace placeholder appears in any section body.

**Boilerplate: none detected.** No section 3 or section 7 body is repeated across three or more files, and no sentence of eighty characters or more recurs across five or more files outside the allowed safety-boilerplate fragments. The sub-plans are individually written, not templated.

**Implementation Contract tables: all present and valid.** Every sub-plan carries the table in section 9 with the required `Path`, `State`, `Purpose`, and `Validation Command IDs` headers. Across the thirty-two tables there are 152 rows: 82 `existing`, 49 `modified`, 19 `proposed`, 1 `external`, 1 `deferred`. Every state value is in the allowed set. Every path is repo-relative with no absolute path, no `..` traversal, no `.git` or `.env` component, and no `.key` or `.pem` suffix. Every row carries a non-empty purpose and at least one validation command identifier. Roughly seventy distinct `VAL-` identifiers are used, with `VAL-DOCS`, `VAL-SMOKE`, `VAL-MANUAL`, `VAL-STATIC`, `VAL-PRECOND`, and `VAL-DISASM` as the recurring backbone and the remainder specific to individual sub-phases.

## 8. Content Quality and Implementability Analysis

**The sub-plans are specific.** They name files, functions, addresses, byte counts, tag identifiers, and numeric targets. `Faz5.1` requires the candidate blob to be exactly 1,062,250 bytes. `Faz4.1` requires the target array entry count stated as a number before any patch is applied. `Faz3.3` defines a confirmed candidate precisely: `f0006` reports 8192x6144 after and 4096x3072 before, with `f0000` and `f000a` unchanged. This is not planning prose; it is a specification a coding agent can execute against.

**They are actionable and correctly sliced.** Every sub-plan decomposes into numbered work items with a stated output. The slices are small and reversible in the way the vibecoding contract asks: one word per patch attempt in `Faz3.3`, one guard site measured before the other three in `Faz4.1`, a temporary mount that must leave no residue in `Faz5.2`, a dry run before the first commit in `Faz1.1`. The fastest validation signal is named in most Description sections rather than left implicit.

**They preserve the main plan.** No sub-plan alters the vision, the target end state, the layer architecture, or the phase order. Where the master plan left a decision open, the sub-plan records it as open and routes it to the user — nine such decisions are carried in the ledger as `DEC-01` through `DEC-09`, and each traces to a sub-plan and to a master-plan or autopsy origin. Nothing was silently resolved by planning.

**Acceptance criteria are verifiable.** This is the strongest dimension of the set. Criteria are written as conditions that a command output or a recorded artifact either satisfies or does not, and negative outcomes are given explicit acceptable forms: "an explicitly undetermined state is acceptable, silence is not"; "an exhausted budget is recorded as a completed outcome rather than an incomplete one"; "if the cause was not found, the status says so rather than remaining silent". Several criteria are anti-criteria that constrain what must *not* have happened — "no patch has been applied and no device interaction has occurred", "no change to the four functional tiles has been made" — which is exactly what makes a sub-phase boundary enforceable.

**The validation approach is realistic for the domain.** The project has no test framework and no CI, and the sub-plans do not pretend otherwise. Validation is device measurement, host-side structural checks, checksum comparison, and diff review, with the smoke script as the one automatable surface. `Faz9.1` explicitly declines CI with a justification. `Faz1.1` states that local smoke, CI, and artifact validation are not applicable at its stage rather than inventing a gate.

**Dependencies are explicit.** Every section 10 names upstream dependencies, what the sub-phase blocks, required decisions, required credentials or infrastructure, required human approvals, token and context risk, and a subagent judgment. The dependency graph they describe is acyclic and consistent with the index's execution order.

**Token and context discipline is present and specific.** Risk bands are stated per sub-plan and justified. `Faz3.2` is banded high with the master plan's `R10` quoted as the reason and two structural mitigations named — scripted extraction with bounded output, and immediate ontology recording so a truncated session loses momentum rather than findings. `Faz2.1` identifies the camera service dump as the one place an unbounded command would be costly and requires on-device filtering. `Faz2.3` and `Faz4.4` identify verdict volume as the hazard and require verdicts to be written as produced. This is better than a generic band.

**Subagent guidance is consistent and correctly restrictive.** Thirty-one sub-plans say subagents are not recommended, each with a reason grounded in either the master plan's section 9 judgment or the stateful-device constraint. `Faz8.1` carries the single exception the master plan sanctions, scoped to one work item, with the parent retaining ownership of writes. `Faz3.2` permits a bounded read-only helper only if the parent's context is nearly exhausted, and still requires the parent to own every ontology write.

**Fresh-session suitability.** Each sub-plan states its outcome, its validation, its unchanged boundaries through the Out of Scope section, and its stop conditions through the transition criteria. A fresh Step 4 session can load one sub-plan and work from it without the rest.

**Weaknesses.** The set is verbose — thirty-two files averaging roughly 16 KB. That is defensible for a project whose stated central risk is knowledge loss between sessions, and Step 4's token discipline of loading one sub-plan at a time makes it workable, but it is a real cost. The identifier-routing gaps in `AUDIT-FIX-01` are the only place where the traceability discipline the plans otherwise maintain is incomplete.

## 9. Scope Drift and Architectural Consistency Analysis

**No phase was added, removed, or renamed.** The index's phase table reproduces the master roadmap table's nine rows with identical names and maturity targets. No sub-plan introduces a capability the master plan does not name.

**Ownership of state is preserved.** The single-writer `mode` file design is respected everywhere; no sub-plan proposes a second writer. `Faz5.3` is the only sub-plan that would change dispatch behavior, and only on a measured success path, with the ten-mode regression record as its guard.

**Layer boundaries are respected.** The sensor, HAL, and application layers stay distinct across all thirty-two sub-plans. `Faz4.3`'s consolidation moves a patch table between directories but does not merge layers, and it explicitly surfaces the module's two-state (`fullres`/`stock`) assumption in `hal_state`, `hal_set`, and `hal_write` as the constraint governing the structural decision. That is boundary-aware, not boundary-blurring.

**Tool-versus-core confusion: none.** The AGC port is consistently treated as an application-layer consumer, not as project-owned code. `Faz3.5` requires the tile to be the only switch precisely so a success is attributable to the HAL rather than to application configuration.

**Premature live or production activation: none.** Publishing, uploading, and distributing a release are explicitly out of scope in `Faz9.1`. Adding a remote, pushing, and publishing are explicitly out of scope in `Faz1.1`, and `Faz1.2` states that a remote must not be added before the credential audit result is known. No sub-plan proposes an auto-merge, a force operation, or a destructive command; a targeted scan for such language found nothing.

**Over-documentation: borderline but justified.** Phase 1 is six sub-plans of which four produce documents. Given that `R7` names knowledge concentration as a medium-severity risk and that the project's own history records context loss causing rediscovery of solved problems, documentation work carries real engineering value here. Each of the four also produces a check, not only prose: a round-trip in `Faz1.3`, two self-checks in `Faz1.4`, an exhaustive call-site trace in `Faz1.5`, an on-disk correspondence check in `Faz1.6`.

**Security hardening: present, not missing.** Keystore containment is a dedicated sub-plan with a packaging assertion specification that `Faz9.1` must implement and prove by deliberate failure. The static probe batch covers shell-injection surface, fail-closed write discipline, and sepolicy.

**Ontology consistency: strong, with an identifier-linkage gap.** Every one of the 79 distinct continuity identifiers referenced across the sub-plans is defined in `Project-Ontology.md`, `Project-Comprehension.md`, or `Autopsy.md`; there are no dangling references. The vocabulary distinctions the master plan asked Step 2 to keep — sensor versus HAL versus application layer, `fullres` as a HAL state distinct from `50mp` as a mode name, `mode` as single-file runtime state, patch table as an offset-plus-checksum record — are used consistently throughout. All ten hypotheses `H-01` through `H-10` are routed to a sub-plan that tests them, and no sub-plan uses a tentative hypothesis as a premise. The gap is in the reverse direction: `OQ-10` and `OQ-12` in the ontology's register and `CQ-03`, `CQ-08`, and `CQ-14` in the comprehension register are not named by identifier in any sub-plan, even though the substance of each is covered. Because both continuity artifacts carry a recording rule requiring a resolving probe to update the corresponding register entry in the same session, an unnamed identifier is one whose status will silently go stale. Recorded as `AUTOPSY`-adjacent finding `AUDIT-FIX-01`.

**Planning-history continuity: correct.** The ledger uses the v2 schema with a populated Plan Snapshot Registry and a Sub-Plan Status Matrix seeded at `planned` for all thirty-two rows, each with a next action. Every matrix path resolves to an existing file. No sub-plan duplicates already-completed work, because no implementation run has occurred — the ledger states this plainly rather than leaving section 5 empty. The Replanning Inputs section names seven concrete triggers, each tied to a specific sub-plan outcome or artifact change, which is a usable contract rather than a generic statement.

## 10. Readiness Realism

**Documentation versus implementation is correctly distinguished.** No sub-plan describes a document as a working capability. `Faz1.3` produces a format contract and says so; the contract's value is that `Faz4.3` can apply it, which is stated as a dependency rather than as an accomplished fact.

**Skeleton versus working runtime is correctly distinguished.** `Faz6.1` adds a one-line device-tree entry and its acceptance criteria require the unverified status to be recorded explicitly "so the change is not treated as a proven fix", with the proof registered against Phase 7 by `Faz6.2`. This is the single best readiness-realism handling in the set: the change is made now, the claim is withheld until a build exists.

**Local versus live readiness is correctly distinguished.** `Faz5.1` generates and host-verifies a blob and forbids placing it in `blobs/` as a shipped variant; `Faz5.2` mounts it temporarily and requires the post-test snapshot to match the pre-test snapshot; only `Faz5.3`, on a measured success, ships it. `Faz1.1` states that local smoke, CI, and artifact validation are not applicable at its stage.

**Smoke tests versus production confidence is correctly distinguished.** `Faz2.1`'s script reports state and explicitly does not judge whether a state is correct — "it reports; a human or a later checklist interprets". `Faz9.2` then builds the interpreting checklist and validates it by demonstrating that it reports a known-bad state differently from a known-good one, which is the correct way to establish that a verification surface has sensitivity rather than merely output.

**Examples versus real configuration is correctly distinguished.** No sub-plan treats a configuration example as a working credential. `Faz1.4` states that its signing step is not executable without the key and that this is stated rather than worked around — the honest handling.

**Pilot versus production core is correctly distinguished.** The experimental HAL patch is consistently called experimental until `Faz4.4` validates the consolidated artifact, and `Faz4.4` frames the question as whether the complete patch "is safe to distribute" because the patch is intended for other people's devices.

**Overclaims found: none.** A targeted scan for "production ready", "fully tested", "guaranteed", and equivalent language across all thirty-two sub-plans returned nothing.

**Vibecoding language: not abused.** The term is used to mean small reversible slices with fast validation signals, and every sub-plan that invokes it names the slice and the signal. No sub-plan calls broad documentation or strategy work "vibecoding" without giving a concrete first slice and a validation gate.

**One realism gap.** The recovery dimension is asymmetric with the risk schedule. Per-change reversal is proven where it applies — `Faz3.3` requires a third snapshot matching the first, `Faz5.2` requires the mount to leave no residue — but the recovery path for the case where the module itself is non-functional does not exist in written form until `Faz9.2`, well after Phases 3 through 5 have patched a system binary on the user's daily device. The master plan's `R3` asks for that path earlier and names the smoke script as its home. Recorded as `AUDIT-FIX-02`.

## 11. Security and Governance Findings

**Secret safety: clean.** A length-bounded scan across every file under `Planner-docs/` using the bundled validator's own pattern set — OpenRouter and OpenAI key shapes, GitHub classic and fine-grained tokens, AWS access key identifiers, private key headers, and Slack tokens — returned zero matches. `secret_findings=0`. The signing keystore is referenced by path and role only in every sub-plan that mentions it; no content, no fingerprint, no passphrase. `Faz1.2` performs its audit by archive entry name only, which is the correct technique for answering "is the credential present" without reading it. `Faz1.1`'s `VAL-SEC` is explicitly name-only output.

**Least privilege: respected.** The project's modules necessarily run as root at `post-fs-data`; no sub-plan widens that. `Faz2.1` narrows it in the one place it can, by making the only new tool read-only with a per-command review as an acceptance criterion.

**Approval gates: present and correctly placed.** Every sub-plan that touches the device names the required human approvals separately from the required infrastructure. The established boundary — read-only inspection delegated, anything touching the phone is the user's action — is restated where it applies rather than assumed. Nine open decisions are routed to the user with an owner and a blocking relationship recorded in the ledger. The two Phase 8 commit decisions and the Phase 5 priority decision are all routed rather than pre-empted by planning.

**Command execution safety: addressed.** `Faz1.5` traces every `exec` call site in the WebUI and its acceptance criterion forbids a sampled conclusion: "a conclusion of 'no unsanitized input' is supported by an exhaustive list or is not stated". `Faz1.3` and `Faz1.5` together answer the atomicity question from `halpatch.sh` rather than assuming it.

**Path and artifact integrity: addressed.** Every Implementation Contract path is repo-relative and safe. `Faz4.3` requires checksums to be recomputed by application rather than transcribed, and requires superseded experimental tables to be removed or marked so a stale chain cannot be applied by accident. `Faz9.1`'s release manifest binds the release to the checksums of the patch tables, the sensor blobs, the tile application, and the archive.

**Review, CI, merge, and deploy boundaries: explicit.** No CI is proposed and its absence is justified. No merge, push, or publish operation appears anywhere. `Faz1.2` gates the remote decision on the credential audit, which is the correct dependency direction.

**Local versus cloud boundary: clean.** The project has no network surface and no sub-plan introduces one. Network access appears only where it is unavoidable and stated: obtaining a beryl reference tree in `Faz8.1`, determining the current LTS target in `Faz8.2`, and the source sync in `Faz7.2`.

**Destructive or risky operations: bounded.** The riskiest planned operations are HAL patching on a daily-driver device and a temporary sensor-blob mount. Both carry mandatory reversal demonstration, both are bracketed by before-and-after snapshots, and both are preceded by a precondition checklist. No sub-plan proposes an irreversible operation without a stated reversal path — with the runbook-scheduling caveat in `AUDIT-FIX-02`.

**Secure-by-design expectations where code changes are planned.** The three sub-plans that produce executable artifacts — `Faz2.1`'s smoke script, `Faz9.1`'s build script, `Faz9.2`'s runbook — each carry a safety property as an acceptance criterion: read-only verified per command, packaging assertions proven to fail on their condition, and runbook steps verified independent of module-provided commands.

**Ledger and ontology assumptions: safe.** No sub-plan treats a `tentative` evidence item or hypothesis as an implementation premise. The index enumerates the confidence-sensitive assumptions explicitly and names the sub-plan that converts each into a measured fact.

## 12. Step 4 Readiness Assessment

Dependency state is assessed against the index's recommended execution order. `independent` means the sub-plan has no upstream dependency; `satisfied` means every upstream dependency it names is produced by an earlier sub-plan in the same queue, so the prerequisite exists at the moment Step 4 reaches the row. No sub-plan depends on an artifact, environment, or decision that the queue itself cannot produce.

| Sub-Plan Path | Status | Finding IDs | Dependency State | Reason | Required Repair |
|---|---|---|---|---|---|
| Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md | READY | none | independent | First slice in the roadmap; no upstream dependency, seven measurable acceptance criteria, no device interaction. | none |
| Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md | READY | none | satisfied | Depends only on Faz1.1's ignore rule; the archive audit itself is independent and read-only. | none |
| Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | READY | none | satisfied | Weak dependency on Faz1.1; consumes Faz1.5's atomicity answer or performs the read itself, which the sub-plan states. | none |
| Planner-docs/Faz-1-Plans/Faz1.4-toolchain-procedure-record.md | READY | none | satisfied | Depends on Faz1.2 for the key-location policy, which precedes it in the queue. | none |
| Planner-docs/Faz-1-Plans/Faz1.5-static-safety-probes.md | READY | none | satisfied | Static batch with no device, build, or user action required; runs before Faz2.2 as its own text requires. | none |
| Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md | READY_WITH_WARNINGS | AUDIT-FIX-04 | satisfied | Content is complete and checkable; only its queue position relative to three beneficiaries is questioned. | Confirm the position or move it ahead of Faz6.1. |
| Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md | READY_WITH_WARNINGS | AUDIT-FIX-01, AUDIT-FIX-02 | satisfied | The one automatable validation surface; strong acceptance criteria. Carries two non-blocking findings. | Name OQ-10 and CQ-03; record the R3 restore-path decision. |
| Planner-docs/Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md | READY | none | satisfied | Depends on Faz2.1's bracket and Faz1.5's install-state answer, both earlier in the queue. | none |
| Planner-docs/Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md | READY | none | satisfied | Depends on Faz2.2's flashed device and named baseline. User-intensive but fully specified. | none |
| Planner-docs/Faz-2-Plans/Faz2.4-tiles-hide-disposition.md | READY | none | satisfied | Bounded investigation with an explicit stop point; the only Phase 2 item Phase 3 does not depend on. | none |
| Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md | READY | none | satisfied | Gate sub-phase; collects the attempt budget rather than waiting on it. All five upstream dependencies precede it. | none |
| Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | READY_WITH_WARNINGS | AUDIT-FIX-03 | satisfied | Static, executable without the user, with budget exhaustion defined as a completed outcome. | Name OQ-01 alongside CQ-05 in the recording criterion. |
| Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md | READY_WITH_WARNINGS | AUDIT-FIX-02 | satisfied | Reversal is mandatory and demonstrated. First on-device HAL patch, so the recovery-path question lands here. | Resolve the R3 restore-path deferral before executing. |
| Planner-docs/Faz-3-Plans/Faz3.4-consumer-compatibility-check.md | READY | none | satisfied | Depends on a confirmed write site from Faz3.3 and the Faz2.2/Faz2.3 references. | none |
| Planner-docs/Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md | READY | none | satisfied | Log filtering configured before launch; failure is classified and routed rather than investigated open-endedly. | none |
| Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md | READY_WITH_WARNINGS | AUDIT-FIX-01 | satisfied | Runs regardless of upstream outcome; requires every tracked question to reach a non-open state. | Add OQ-12 and CQ-14 to the tracked-question set. |
| Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | READY | none | satisfied | Depends on Faz3.6's preservation requirement and the proceed decision, both produced in-queue. | none |
| Planner-docs/Faz-4-Plans/Faz4.2-duration-rows.md | READY | none | satisfied | Depends on Faz4.1's narrowed entry set; routes the bucketing consequence to the user as DEC-09. | none |
| Planner-docs/Faz-4-Plans/Faz4.3-patch-table-consolidation.md | READY | none | satisfied | Depends on Faz4.1, Faz4.2, Faz3.3, and Faz1.3's format contract, all earlier in the queue. | none |
| Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | READY | none | satisfied | Compares against three recorded references produced earlier in the queue. | none |
| Planner-docs/Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md | READY | none | satisfied | Host-side only. Needs the Python environment from Faz1.4 and the go-ahead from Faz3.6; both precede it. | none |
| Planner-docs/Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md | READY | none | satisfied | Depends on Faz5.1's verified candidate and Faz2.1's bracket; the mount leaves no residue. | none |
| Planner-docs/Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md | READY | none | satisfied | Depends on Faz5.2's measured result and Faz2.3's ten-mode reference. | none |
| Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md | READY_WITH_WARNINGS | AUDIT-FIX-04 | satisfied | Two one-line edits with the unverified status required as an acceptance criterion. | Resolve the refs-role question or move Faz1.6 earlier. |
| Planner-docs/Faz-6-Plans/Faz6.2-aon-module-disposition.md | READY | none | satisfied | Depends on Faz6.1's entry; registers its verification against Phase 7 rather than deferring silently. | none |
| Planner-docs/Faz-7-Plans/Faz7.1-wsl2-provisioning.md | READY | none | satisfied | Verified by a real build action. Host installation is the user's action, which is this phase's stated nature. | none |
| Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | READY_WITH_WARNINGS | AUDIT-FIX-04 | satisfied | Stopping rule recorded before the build; reaching it is a bounded outcome. | Confirm the refs index is available or derive it here. |
| Planner-docs/Faz-8-Plans/Faz8.1-beryl-port-sizing.md | READY_WITH_WARNINGS | AUDIT-FIX-04 | satisfied | Sizing only, deliberately low detail. Carries the roadmap's single sanctioned subagent exception. | Confirm the refs naming convention source. |
| Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md | READY | none | satisfied | Independent of Faz8.1; needs the Linux environment from Faz7.1, which precedes it. | none |
| Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | READY_WITH_WARNINGS | AUDIT-FIX-01 | satisfied | Packaging assertions must be proven to fail; publishing is explicitly out of scope. | Name CQ-08 in the contents-specification criterion. |
| Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | READY_WITH_WARNINGS | AUDIT-FIX-02 | satisfied | Owns the recovery runbook. Its queue position is the substance of the finding. | Split the runbook forward or record the deferral. |
| Planner-docs/Faz-9-Plans/Faz9.3-documentation-consolidation.md | READY | none | satisfied | Runs before Faz9.2 per the index order, resolving the stated two-way interaction. | none |

**Execution queue state: READY.** Twenty-two rows are `READY` and ten are `READY_WITH_WARNINGS`; all thirty-two are queued. No row is `NEEDS_REPAIR`, `BLOCKED`, `COMPLETE`, `SUPERSEDED`, or `DEFERRED`. No `READY` or `READY_WITH_WARNINGS` row has a `blocked` or `unknown` dependency state, and no `READY_WITH_WARNINGS` row references a P0 or P1 finding, because none exists. The first item in the execution queue is `Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md`.

## 13. Priority Fix List

No P0 or P1 finding was identified. The five findings below are quality and traceability issues. None blocks the start of Step 4; two carry an execution-order condition that Step 4 must respect as it advances through the queue.

| Finding ID | Severity | Status | Affected Files | Issue | Required Action |
|---|---|---|---|---|---|
| AUDIT-FIX-01 | P2 | open | Planner-docs/Sub-Planing-Index.md, Planner-docs/Planing-Ledger.md, Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md, Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md, Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | The ledger's section 6 states "Each open question is routed to a named sub-plan", and the index makes the equivalent claim. Five open or partially answered register entries are not named by identifier in any sub-plan: ontology `OQ-10` and `OQ-12`, and comprehension `CQ-03`, `CQ-08`, and `CQ-14`. The substance of each is covered — `OQ-10` and `CQ-03` by Faz2.1, `CQ-08` by Faz9.1, `CQ-14` by the Faz3.6 priority decision, `OQ-12` by nothing — but both continuity artifacts carry a recording rule requiring a resolving probe to update the corresponding register entry in the same session. An identifier no sub-plan names is one whose status will silently go stale, which is the exact failure mode QAS-03 and R10 exist to prevent. | Add the missing identifiers to the acceptance criteria of the sub-plans that already do the work: `OQ-10` and `CQ-03` to Faz2.1, `CQ-08` to Faz9.1, `CQ-14` and `OQ-12` to Faz3.6's tracked-question set. If `OQ-12` is genuinely not addressed anywhere, either route it or mark it deferred in the ontology. Correct the routing claim in the ledger and the index to match. |
| AUDIT-FIX-02 | P2 | open | Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md, Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md, Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md, Planner-docs/Sub-Planing-Index.md | Main-Planing risk `R3` (severity high) states its mitigation as adding an explicit stock-restore path to the smoke script, and the operational target repeats it. Step 2 made Faz2.1 strictly read-only — a well-argued design choice — and placed the only written recovery runbook in Faz9.2, at position 13 of the recommended execution order. Phases 3, 4, and 5 patch a system binary on the user's daily-driver device before that. Per-change reversal is proven (Faz3.3's third snapshot, Faz5.2's residue check) and the module's own `hal_set stock` path exists, but Faz9.2's own acceptance criterion requires runbook steps verified independent of module-provided commands, which is precisely the case not covered before Phase 9. | Before Faz3.3 executes, either split the recovery-runbook portion of Faz9.2 into an early sub-phase or a Phase 1 addendum, or record explicitly in Faz2.1 and Faz3.3 that the `R3` mitigation is deliberately deferred, naming what stands in its place and who accepted the residual risk. Do not begin Faz3.3 with this unresolved. Faz1.1 through Faz3.2 may proceed. |
| AUDIT-FIX-03 | P3 | open | Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | Faz3.2 is the sub-plan that resolves the project's central open question — where `camera.qcom.so` writes `pixelArraySize`. It names comprehension `CQ-05` and hypothesis `H-01` in its acceptance criteria but not ontology `OQ-01`, which is the same question in the ontology's register. `OQ-01` is named only in Faz3.6, three sub-phases later, so the recording rule requiring a same-session register update will not fire where the answer is actually produced. Faz3.6's requirement that every tracked question reach a non-open state is a real mitigation, which is why this is P3 rather than P2. | Add `OQ-01` to Faz3.2's recording acceptance criterion alongside `CQ-05`, so the ontology register is updated in the session that produces the answer rather than at the phase gate. |
| AUDIT-FIX-04 | P3 | open | Planner-docs/Sub-Planing-Index.md, Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md, Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, Planner-docs/Faz-8-Plans/Faz8.1-beryl-port-sizing.md | The index's section 4 places Faz1.6 outside the numbered execution order as low-priority work that "may run whenever convenient", while three later sub-plans state they benefit from its reference-tree index: Faz6.1 at position 4 needs to know which `refs/` trees are build inputs rather than comparison sources, and Faz7.2 and Faz8.1 make the same statement. These are soft dependencies and each affected sub-plan can derive the answer itself, so nothing is blocked — but the same question would then be answered three or four times, which is the duplication Faz1.6 exists to prevent. | Either move Faz1.6 ahead of Faz6.1 in the index's recommended execution order, or state in the index that the three beneficiaries derive the refs-role answer independently and that Faz1.6 consolidates it afterwards. |
| AUDIT-FIX-05 | P3 | open | Planner-docs/Sub-Planing-Index.md | Section 2 of the index states that Project-Ontology carries "sixteen competency questions of which ten were open at Step 2". Sixteen is correct. The open count is eleven: `OQ-01` through `OQ-11` all read `open`, and `OQ-12` reads `partially_answered`. The ledger's section 6 states the same fact correctly. This is a transcription error in a supporting sentence with no downstream consequence, but the project's own discipline is that counts are reported from the source rather than from memory. | Correct the sentence in the index to eleven open, one partially answered, and four answered. |

## 14. Recommended Next Command / Prompt

The audit status is `PASS_WITH_WARNINGS` with no open P0 or P1 finding, so implementation may begin. Under the workflow's finding-status rules, open P2 and P3 findings require `PASS_WITH_WARNINGS` and must remain visible during implementation; they do not gate the start of Step 4.

**First item in the implementation queue:** `Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md` — Phase 1, Workspace safety net. It is the only row with dependency state `independent`, it is the master plan's own first prioritized next step, and it is the precondition for every sub-plan that later writes a binary or a patch table.

**Two conditions Step 4 must carry through the queue.**

First, `AUDIT-FIX-02` must be resolved before `Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md` executes, because that is the first on-device system-binary patch. Everything from `Faz1.1` through `Faz3.2` may proceed without it.

Second, the identifier-routing corrections in `AUDIT-FIX-01` and `AUDIT-FIX-03` should be applied to each affected sub-plan's acceptance criteria before that sub-plan runs, so the continuity registers stay current in the session that produces each answer.

**Copy-ready Step 4 prompt for a fresh Claude Code session:**

```text
/claudeqb:claudeqb Read and return the exact canonical handoff from references/handoffs/run-step4.md, then execute it.
```

**Token-use and queue-continuation reminder.** Do not load all thirty-two sub-plans at once. Read `Planner-docs/Sub-Planing-Audit.md` and `Planner-docs/Sub-Planing-Index.md` first, build the ordered queue from the `READY` and `READY_WITH_WARNINGS` rows in section 12 using the index's section 4 execution order, then load only the active sub-plan plus the repository files that slice needs. Read `Planner-docs/Project-Ontology.md` and `Planner-docs/Planing-Ledger.md` only as the active slice requires. After each verified slice, append a concise implementation summary to `Planner-docs/Planing-Ledger.md` and update the Sub-Plan Status Matrix row, then continue to the next acceptance criterion or the next queued sub-plan rather than stopping. Record every located binary address into `Planner-docs/Project-Ontology.md` section 6 in the session it is found, per `R10` and `QAS-03`. Stop on the sub-plan's own stop gates: a failed precondition, a failed validation, a missing required file, a needed user decision or physical device action, an unsafe external mutation, or context pressure. `Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md` is banded high for context risk and should use scripted extraction with bounded output rather than interactive exploration.

Do not run this prompt from the current session; open a fresh one.

## 15. Audit Result

**Final status: PASS_WITH_WARNINGS.**

**Confidence: high.** The structural conclusions rest on a complete programmatic check of all thirty-eight files under `Planner-docs/`, not on sampling. The content conclusions rest on reading the master plan, the index, and the ledger in full, one sub-plan in full, and the Goal, Acceptance Criteria, Dependencies, and Implementation Contract of all thirty-two sub-plans, plus a full cross-reference of every continuity identifier in both directions. Confidence is high rather than absolute in one respect: the sub-plans' citations of repository evidence outside `Planner-docs/` were checked for internal consistency and plausibility against the Step 1 and Step 1.5 records rather than re-measured against the workspace.

**Counts, reported from measurement.** Nine master phases. Nine phase folders. Thirty-two sub-plan files. Thirty-two index references, resolving in both directions. Four hundred sixteen required sub-plan sections, all present, unique, ordered, and non-empty. One hundred fifty-two Implementation Contract rows, all with valid states and safe repo-relative paths. Seventy-nine distinct continuity identifiers referenced, all defined. Zero secret findings. Five audit findings: zero P0, zero P1, two P2, three P3.

**Files modified by this audit: one.** `Planner-docs/Sub-Planing-Audit.md` was created. No sub-plan, no index, no ledger, no continuity artifact, and no file outside `Planner-docs/` was written. This was verified by comparing a file listing with modification timestamps captured before the write against the listing after it: thirty-eight files before, thirty-nine after, with the single new path being the audit itself and every pre-existing timestamp unchanged. The workspace is not a git repository — `git status --short` and `git branch --show-current` both return `fatal: not a git repository`, which is finding `AUTOPSY-P0-01` and the reason `Faz1.1` is first in the queue — so the timestamp comparison stands in place of `git status` and `git diff`. This limitation disappears once `Faz1.1` runs.

**Unexpected modifications detected: none.**

**Validator execution: unavailable, with an equivalent fallback performed.** The bundled `scripts/validate_planner_docs.py` could not run because this host has no Python interpreter. Equivalent all-file validation was performed by a read-only reimplementation of the validator's rule set, described in section 2. The `step3-preflight --strict` equivalent passed with zero errors and zero warnings. The `step3` and `step4` equivalents, run after this file was written, report `audit_status=PASS_WITH_WARNINGS`, `execution_queue_state=READY`, `p0_findings=0`, `p1_findings=0`, `p2_findings=2`, `p3_findings=3`, and no readiness-row, dependency-state, finding-severity, finding-status, or path-safety error. Under `--strict` the run exits non-zero solely because the non-blocking `step4_has_nonblocking_warnings` signal is promoted to an error by the strict flag; the workflow's gating conditions for Step 4 are an audit status of `BLOCKED` or the presence of P0/P1 findings, and neither holds.

**Can Step 4 safely begin: yes.** Start at `Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md`, carry the two P2 findings visibly, and resolve `AUDIT-FIX-02` before `Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md`.
