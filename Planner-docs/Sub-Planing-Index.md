# Sub-Planing Index

> Step 2 sub-plan index — ClaudeQB. Body language: English (default contract).
> The project's user-facing documents and module interface remain Turkish and English; that convention is unchanged.

## 1. Purpose

This index maps the phases in `Planner-docs/Main-Planing.md` to the detailed sub-plan files generated in Step 2. It is the navigation surface for Step 3's audit and for Step 4's implementation runs.

Each phase in the master roadmap has a folder under `Planner-docs/` named `Faz-<n>-Plans`, and each folder holds sub-plan documents named `Faz<n>.<m>-<slug>.md`. Every sub-plan follows the thirteen-section structure the Step 2 contract requires and carries a machine-readable Implementation Contract table in its validation section.

The index does not replace `Main-Planing.md`, and no sub-plan changes the phase order, the vision, or the target end state. Where a sub-plan needed a decision the master plan left open, that decision is recorded as open and routed to the user rather than resolved by planning.

## 2. Source Main Plan

Source: `Planner-docs/Main-Planing.md`.

Detected phase count: 9. The count comes from the roadmap table under section 6 of the main plan, whose rows are numbered 1 through 9, and it is confirmed by the nine `### Phase <n>` headings in the same section.

Detected phase names, in the master plan's order:

| # | Phase name | Maturity target | Token/context risk (from Main-Planing) |
|---|---|---|---|
| 1 | Workspace safety net | M2 | low |
| 2 | Ship and re-baseline v2.1 | M4 | low |
| 3 | 50 MP end-to-end in AGC | M5 | high |
| 4 | Minimal correct HAL patch | M5 | medium |
| 5 | Mode-0 12-bit composition | M5 | medium |
| 6 | AON fix upstreaming | M4 | low |
| 7 | Android 16 build environment | M3 | medium |
| 8 | beryl port + kernel LTS | M5 | high |
| 9 | Release engineering | M6 | low |

Ambiguity or inconsistency found: none that blocks decomposition. Two points are worth recording rather than treating as defects.

First, the main plan places the device smoke script in Phase 9 and then contradicts that placement three times — in prioritized next step 2, in risk `R5`'s mitigation, and in Phase 9's own first vibecoding slice — each time saying it should be pulled forward to the start of Phase 2. Autopsy makes it a Phase 2 prerequisite. This decomposition follows the pull-forward, placing it as `Faz-2-Plans/Faz2.1-device-smoke-script.md`, and leaves the release build and checklist in Phase 9.

Second, the main plan's Phase 6 first slice states the symlink change "should not wait for Phase 7", and Autopsy recommends scheduling it "early rather than by phase order". The phase order is preserved in the folder structure; the recommended execution order in section 4 reflects the early scheduling.

**Supporting Sources.**

`Planner-docs/Autopsy.md` exists and was read in full. Its most important Step 2 feedback categories were: the absence of version control as a `P0` blocker that must precede any binary or patch-table work; the absence of before-and-after state capture as a second `P0` driving the smoke script into Phase 2; the signing keystore in the working tree with an unaudited release history; the built-but-unflashed v2.1 release; the absence of a stop condition for Phase 3; the missing symlink entry verified at zero occurrences in both device trees; the over-broad experimental HAL patch; unmarked superseded conclusions; the undocumented patch-table format; and runtime state checked into the packaged module directory.

`Planner-docs/Project-Ontology.md` exists and was read in full. Its key categories were: the domain vocabulary distinguishing the sensor, HAL, and application layers and separating `fullres` as a HAL state from `50mp` as a mode name; the mode and patch-table entities; the module and boundary map; the mode-switch and camera-restart workflows; the reverse-engineering address book in section 6, including the located function ranges, the four format-gate sites, the nine tag references and six rodata dwords for the pixel array tag, the AGC obfuscation map, and the toolchain with its negative findings; eleven invariants; and sixteen competency questions of which **eleven** were open at Step 2, one partially answered and four answered. (`AUDIT-FIX-05`, corrected 2026-09-01: the earlier "ten open" was reported from memory rather than from the source. `OQ-01` through `OQ-11` all read `open` at that moment, `OQ-12` was partially answered, and `OQ-13` through `OQ-16` were answered. This sentence describes the Step 2 moment; the register has since grown to seventeen questions.)

`Planner-docs/Project-Comprehension.md` exists and was read in full. Comprehension artifact used: yes.

Relevant IDs carried into the sub-plans: `CQ-01`, `CQ-02`, `CQ-03`, `CQ-04`, `CQ-05`, `CQ-06`, `CQ-07`, `CQ-08`, `CQ-09`, `CQ-10`, `CQ-11`, `CQ-12`, `CQ-13`, `CQ-14`; `EV-01`, `EV-02`, `EV-04`, `EV-05`, `EV-10`, `EV-11`, `EV-12`, `EV-13`, `EV-14`, `EV-15`, `EV-16`, `EV-17`, `EV-18`, `EV-19`, `EV-20`, `EV-21`, `EV-22`, `EV-23`; `TRACE-04`, `TRACE-06`, `TRACE-08`, `TRACE-13`, `TRACE-14`; `ARC-03`, `ARC-05`, `ARC-06`, `ARC-07`, `ARC-08`, `ARC-10`, `ARC-11`; `QAS-01`, `QAS-02`, `QAS-03`, `QAS-04`, `QAS-05`; and hypotheses `H-01` through `H-10`.

Confidence-sensitive assumptions that must not be promoted into implementation facts:

- `EV-18` (the workspace holds roughly 465 MB) is `tentative`; the whole-tree measurement did not complete. `Faz-1-Plans/Faz1.1-version-control-bootstrap.md` requires a real measurement rather than reusing the estimate.
- `EV-19` (the device's live mode matches the workspace `mode` file) is `tentative`; the device was not queried. `Faz-2-Plans/Faz2.1-device-smoke-script.md` answers it on the smoke script's first run.
- `EV-14` (v2.1 has never been flashed) is `probable`, resting on an absence of evidence. `Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md` resolves it.
- `EV-20` (WSL2 is not installed) is `probable`, sourced from a user statement. `Faz-7-Plans/Faz7.1-wsl2-provisioning.md` converts it to a measured fact.
- `EV-21` (the `dcgB` noise and detail measurement) and `EV-22` (the `tiles hide` option is ineffective) are `probable`; neither is treated as a verified baseline.
- `EV-23` (AGC cannot exceed 15.2 MP) is `contradicted` and is corrected in `Faz-9-Plans/Faz9.3-documentation-consolidation.md`.
- `H-01` through `H-10` are all `tentative`. Each is routed to a sub-plan that tests it rather than assuming it; none is used as a premise.

`Planner-docs/Planing-Ledger.md` did not exist before this run. Step 2 created it using the Ledger v2 headings, with the Sub-Plan Status Matrix seeded at `planned` for every generated sub-plan. There was therefore no prior planning or implementation history to reconcile.

## 3. Phase and Sub-Plan Map

**Phase 1 — Workspace safety net.** Make the workspace recoverable and the reverse-engineering toolchain reproducible. Folder: `Faz-1-Plans`. Recommended execution order is the numbered order, with one hard constraint: the keystore ignore rule must be in place before the first commit. First useful implementation slice: measure directory sizes, write the ignore rules, initialize, and commit the three deliverable directories plus the journal. Fresh-session token risk: low. Subagents: not recommended.

- `Faz-1-Plans/Faz1.1-version-control-bootstrap.md`
- `Faz-1-Plans/Faz1.2-signing-key-containment.md`
- `Faz-1-Plans/Faz1.3-patch-table-format-contract.md`
- `Faz-1-Plans/Faz1.4-toolchain-procedure-record.md`
- `Faz-1-Plans/Faz1.5-static-safety-probes.md`
- `Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md`

**Phase 2 — Ship and re-baseline v2.1.** Close the gap between the released artifact and the validated device state, and build the project's only automatable validation surface. Folder: `Faz-2-Plans`. Execution order is numbered, with the smoke script strictly first. First useful slice: the cheap half of the smoke script — active mode, both checksums, and mount state. Fresh-session token risk: low for 2.1 and 2.2, medium for 2.3 due to verdict volume. Subagents: not recommended; device state is a single stateful resource.

- `Faz-2-Plans/Faz2.1-device-smoke-script.md`
- `Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md`
- `Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md`
- `Faz-2-Plans/Faz2.4-tiles-hide-disposition.md`

**Phase 3 — 50 MP end-to-end in AGC.** The project's critical path and highest-uncertainty work. Folder: `Faz-3-Plans`. Execution order is strictly numbered; each sub-plan is a precondition for the next. First useful slice: the preference audit and clearance, which closes the highest-cost failure mode before any measurement. Fresh-session token risk: high — this is the phase Main-Planing bands high and `R10` describes. Subagents: not recommended; a bounded read-only helper for a single mechanical extraction is defensible in `Faz3.2` if the parent's context is nearly exhausted, but the parent must own every ontology write.

- `Faz-3-Plans/Faz3.1-preference-trap-clearance.md`
- `Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md`
- `Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md`
- `Faz-3-Plans/Faz3.4-consumer-compatibility-check.md`
- `Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md`
- `Faz-3-Plans/Faz3.6-fallback-decision-gate.md`

**Phase 4 — Minimal correct HAL patch.** Reduce the working experiment to the smallest internally consistent change and consolidate it into a shippable artifact. Folder: `Faz-4-Plans`. **Execution order is NOT the numbered order.** `Faz4.5` ran first per `DEC-12` and is complete and verified (`IMPL-27` … `IMPL-30`). **The current order is `Faz4.6` (host-side half) → `Faz4.1` → `Faz4.6` (gated half) → `Faz4.2` → `Faz4.3` → `Faz4.4`.** Within the numbered four, narrowing must still precede duration rows so rows are added only for surviving entries. First useful slice: `F4.6-01`…`F4.6-04`, the host-side geometry reconstruction, which needs neither the device nor the user and may settle the diagnosis outright. Fresh-session token risk: medium across all of Phase 4's remaining work; `Faz4.5`'s high banding described a write-site search that is now complete, and `Faz4.6` is arithmetic and filtered log reads rather than a search. Subagents: not recommended.

- ~~`Faz-4-Plans/Faz4.5-active-array-raise.md`~~ — **complete and verified 2026-09-01.** Both write sites confirmed by measurement; both active-array tags raised; **the image is not fixed**, so `FIND-3.5-01` did not close and `FIND-4.5-02` was raised.
- `Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md` — **runs first, per `DEC-13`(a)**, for `F4.6-01` … `F4.6-04`
- `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` — runs next, and its format-32 extension is what unlocks `F4.6-07`
- `Faz-4-Plans/Faz4.2-duration-rows.md`
- `Faz-4-Plans/Faz4.3-patch-table-consolidation.md`
- `Faz-4-Plans/Faz4.4-patch-compatibility-validation.md` — also carries `FIND-4.5-01` and the `AUDIT-FIX-09` repair

**Phase 4's scope is `Main-Planing.md` section 6 *plus* `DEC-11`, `DEC-12` and `DEC-13`(a) — recorded here rather than by editing the master plan (`AUDIT-FIX-10`).** Three decision-backed additions are not in `Main-Planing.md`'s Phase 4 description: the `f0000` / `f000a` active-array raise (`DEC-12`, executed as `Faz4.5`, appearing in the master plan only as a Phase 3 *fallback* risk note); the format-32 / `RAW_SENSOR` emission extension (`DEC-11`, absent entirely, and a widening inside a narrowing phase); and the RAW payload geometry diagnosis (`DEC-13`(a), created after the master plan was written). All three are legitimate and fully traceable to measured findings from `IMPL-23` and `IMPL-30`. **`Main-Planing.md` is deliberately not edited**, because the ledger's section 7 makes editing it a replanning trigger that would supersede `SNAP-2026-08-24-SUBPLANS`; the divergence is recorded here so a future replanning run reading the master plan first does not under-scope Phase 4 by three work streams. A deliberate Step 1 amendment plus a Step 2 and Step 3 re-run remains the correct closure, at the natural boundary, which is the close of Phase 4.

**Phase 5 — Mode-0 12-bit composition.** Execute the user-approved experiment to let the sensor and HAL layers coexist. Folder: `Faz-5-Plans`. Execution order is numbered. First useful slice: generate the candidate blob and verify it with the existing host-side harness, which is the only substantial local validation surface in the project. Fresh-session token risk: low for 5.1 and 5.2, medium for 5.3 on the success path. Subagents: not recommended.

- `Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md`
- `Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md`
- `Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md`

**Phase 6 — AON fix upstreaming.** Remove the need for the runtime workaround by fixing the device-tree defect. Folder: `Faz-6-Plans`. Execution order is numbered, and both Main-Planing and Autopsy recommend scheduling this phase early rather than by numbered position. First useful slice: the one-line symlink entry in `device_ishtar/proprietary-files.txt`, mirrored to the Android 16 tree. Fresh-session token risk: low. Subagents: not recommended.

- `Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md`
- `Faz-6-Plans/Faz6.2-aon-module-disposition.md`

**Phase 7 — Android 16 build environment.** Reach the point where a build can be attempted. Folder: `Faz-7-Plans`. Execution order is numbered; the environment must exist before a build is attempted. First useful slice: provision the Linux environment and verify with a trivial kernel configuration step inside the Linux home directory. Fresh-session token risk: medium; build output volume is the hazard. Subagents: not recommended. This phase is planned at lower detail per Main-Planing section 9 and depends on user action on the host machine.

- `Faz-7-Plans/Faz7.1-wsl2-provisioning.md`
- `Faz-7-Plans/Faz7.2-first-aospa-build.md`

**Phase 8 — beryl port and kernel LTS merge.** Two independent scoping exercises, neither committed to. Folder: `Faz-8-Plans`. The two sub-plans are independent and may run in either order. First useful slice: acquire a beryl reference tree and determine whether the device shares the SM8550 platform, since that single fact governs most of the estimate. Fresh-session token risk: low for the sizing work; Main-Planing's high banding describes the port itself, which is not planned here. Subagents: Main-Planing section 9 makes its one exception for the Phase 8 device-tree diff, which applies to `Faz8.1` work item three. This phase is planned at lower detail and Autopsy gates its decomposition on Phase 7's outcome.

- `Faz-8-Plans/Faz8.1-beryl-port-sizing.md`
- `Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md`

**Phase 9 — Release engineering.** Make releases reproducible, verifiable, and honestly documented. Folder: `Faz-9-Plans`. Execution order: the build script first, then documentation correction, then the checklist — because the checklist verifies claims and the claims must be corrected before they are verified. First useful slice: enumerate the archive contents and write the build script that assembles exactly that. Fresh-session token risk: low to medium. Subagents: not recommended.

- `Faz-9-Plans/Faz9.1-reproducible-release-build.md`
- `Faz-9-Plans/Faz9.2-release-verification-checklist.md`
- `Faz-9-Plans/Faz9.3-documentation-consolidation.md`

## 4. Priority Detailing Order

The master plan's phase order is preserved in the folder structure. The execution order below reflects Main-Planing's own prioritized next steps and Autopsy's scheduling feedback, both of which move certain work out of numbered order.

1. **`Faz-1-Plans/Faz1.1-version-control-bootstrap.md`** — security and recoverability hardening first. `AUTOPSY-P0-01` requires it before any sub-plan that modifies a binary or a patch table, and Phase 3 is where an unrecoverable mistake is most likely.
2. **`Faz-1-Plans/Faz1.2-signing-key-containment.md`** — the credential question, gating any decision to add a remote.
3. **`Faz-2-Plans/Faz2.1-device-smoke-script.md`** — real local validation, pulled forward from Phase 9 as the main plan itself recommends three times. It is the only automatable validation surface the project can have.
4. **`Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md`** — scheduled out of order per Autopsy. One line per tree, verified absent, independent of everything else, and every build made before it inherits the defect.
5. **`Faz-1-Plans/Faz1.5-static-safety-probes.md`** — the cheap static batch, whose install-state answer gates the flash in step 6.
6. **`Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md`** — establishes the origin every later comparison is diffed against.
7. **`Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md`** — the reference record Phase 3 and Phase 4 compare against.
8. **`Faz-1-Plans/Faz1.3-patch-table-format-contract.md`** and **`Faz-1-Plans/Faz1.4-toolchain-procedure-record.md`** — both are Phase 3 preconditions: the contract governs Phase 4's extensions and the toolchain is what makes Phase 3's search possible at all.
9. **`Faz-3-Plans/Faz3.1-preference-trap-clearance.md`** through **`Faz-3-Plans/Faz3.6-fallback-decision-gate.md`** — the core control-plane work of this project, in strict sequence, under the attempt budget set in the first of them.
10. **`Faz-4-Plans/Faz4.5-active-array-raise.md` first**, then **`Faz-4-Plans/Faz4.1-fullres-dimension-guard.md`** through **`Faz-4-Plans/Faz4.4-patch-compatibility-validation.md`** — the P1 image fix before the blast-radius reduction that precedes distribution. `DEC-12` fixed this order on 2026-09-01: `Faz4.5` raises `f0000`, `f000a` and `80340003`, which is what makes the 50.3 MP capture usable, and running it first gives `Faz4.1`'s preservation check a good frame to preserve. The sub-plan is numbered 4.5 rather than 3.7 so that Phase 3 stays closed; its position in the folder is not its position in the queue. **Superseded for Phase 4 by amendment 4b below; `Faz4.5` is complete and the premise it rested on was only half delivered.**
11. **`Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md`** through **`Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md`** — subject to the priority re-examination that `Faz-3-Plans/Faz3.6-fallback-decision-gate.md` routes to the user.
12. **`Faz-6-Plans/Faz6.2-aon-module-disposition.md`** — the disposition decision, whose verification is registered against Phase 7.
13. **`Faz-9-Plans/Faz9.1-reproducible-release-build.md`**, **`Faz-9-Plans/Faz9.3-documentation-consolidation.md`**, then **`Faz-9-Plans/Faz9.2-release-verification-checklist.md`** — release engineering, once the contents stop moving.
14. **`Faz-7-Plans/Faz7.1-wsl2-provisioning.md`** and **`Faz-7-Plans/Faz7.2-first-aospa-build.md`** — the second front, opened only after the camera work consolidates, per the main plan's own conclusion.
15. **`Faz-8-Plans/Faz8.1-beryl-port-sizing.md`** and **`Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md`** — scoping only, gated on Phase 7's outcome, with both commit decisions routed to the user.

### 4a. Priority amendment, 2026-08-31 — Phase 5 raised, `DEC-03` answered

> **DISCHARGED, and retained only as the record of how `DEC-03` was answered (`AUDIT-FIX-13`, 2026-09-01).** Every sub-plan in this amendment's "revised next-up order" is now verified and closed: Phase 5 closed 2026-08-31 (`IMPL-17`), Phase 3 closed 2026-09-01 (`IMPL-24`). **Do not read this section as current guidance.** The current queue is section 4b below, and the authoritative execution queue is `Planner-docs/Sub-Planing-Audit.md` section 12. This amendment is not deleted, because its reasoning is the only place `DEC-03`'s answer is argued.

**This amendment supersedes positions 9 and 11 above for the near term. The numbered list is left intact as the original reasoning.**

`DEC-03` asked whether Phase 5 retains its priority given how much Phase 3 has grown, and routed the question to the user via `Faz-3-Plans/Faz3.6-fallback-decision-gate.md`. **The user answered it directly on 2026-08-31: Phase 5 has priority.** The stated goal is to run the 50 MP HAL layer and an LN sensor mode at the same time. The decision no longer needs to wait for `Faz 3.6`, which was only the default place it would have been asked.

The revised next-up order is:

1. **`Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md`** — host-side only, no device, no risk. Generates the candidate mode-0 12-bit blob and verifies it with `ishtar-cam-modes/tools/verify_ln.py`. Nothing downstream can be judged until this artifact exists.
2. **`Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md`** — the sub-plan that actually answers whether the two layers can coexist. Temporary mount, revertible, bracketed by `scripts/smoke.sh`.
3. **`Faz-3-Plans/Faz3.1-preference-trap-clearance.md`** — kept close behind because it is cheap and because it owns the per-measurement checklist that `FIND-2.3-01` has now made mandatory for every later measurement.
4. **`Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md`** — only after `Faz 5.2` produces a result.

**A dependency deviation is being taken deliberately, and is recorded rather than hidden.** `Faz5.1` section 10 states "Depends on Phase 4 being complete, per Main-Planing's *after everything else is stable* condition", and `Faz5.2` section 10 states "Depends on ... Phase 4 for a stable HAL artifact". Neither sub-plan file is edited by this amendment, so both still say that.

The justification for proceeding anyway is that the condition's *purpose* is already met. It exists so the composition test is not run against a moving HAL. The HAL under test is frozen: `ishtar-cam-modes` v2.1 is flashed, its fullres artifact is pinned at md5 `fe0245a4720fb07b01d96deef47f5569`, and `IMPL-13` has now characterised it across all ten modes with per-mode snapshots. Phase 4 reduces and consolidates that patch; it does not make it more stable than a frozen, regression-tested artifact already is. Running `Faz 5.2` against v2.1 measures composition against a known, recorded baseline.

**What this amendment does not claim.** It does not resolve the textual conflict inside the two `Faz-5-Plans` files; doing that properly would require a Step 2 re-plan of both, which the user declined in favour of the cheaper index-level change. A session reading those sub-plans will see the Phase 4 dependency and must read this amendment alongside it. It also does not change any phase number, does not edit `Planner-docs/Main-Planing.md`, and therefore does **not** supersede `SNAP-2026-08-24-SUBPLANS` or require a Step 3 re-audit.

**The AGC video regression is explicitly not the reason for this amendment.** The user's stated link between the video fault and the layer merge is not supported by measurement: `IMPL-13` recorded AGC's video section black in four states including plain `stock`, with sensor and HAL both unmodified, and the `50mp` + LN combination has never been reachable on this device because `post-fs-data.sh:16-18` and `setmode.sh` force the sensor layer to stock whenever `50mp` is selected — verified in `IMPL-13`'s bracketed `dcgB` -> `50mp` transition. `FIND-2.3-03` stays open and routed to Phase 3 on its own merits. Raising Phase 5 will not fix it, and Phase 5 must not be judged by whether it does.

The remaining Phase 1 and Phase 2 items — `Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md` and `Faz-2-Plans/Faz2.4-tiles-hide-disposition.md` — are low-priority and may run whenever convenient. The first absorbs outputs from the other Phase 1 sub-plans and benefits from running last within its phase; the second is the only Phase 2 sub-plan that Phase 3 does not depend on.

### 4b. Priority amendment, 2026-09-01 — `DEC-13`(a) answered, Phase 4 resequenced

**This amendment supersedes position 10 above. It does not touch any other position, and it changes no phase number.**

`Faz-4-Plans/Faz4.5-active-array-raise.md` executed end to end and is `verified` (`IMPL-27` … `IMPL-30`). It succeeded at what it set out to do and failed at what the project wanted. Both write sites were located and both patch words are confirmed by measurement, each independently and each on the first candidate examined. With `f0006`, `f0000` and `f000a` all at full resolution simultaneously — a state that had never existed — AGC captured 6144x8192 = 50.3 MP with the libgcam gate completely clear. **The image is still corrupt**, so `FIND-3.5-01` did not close and `FIND-4.5-02` (P1) was raised: the finding's stated cause named three tags, two are now demonstrably raised, and the artifact survives.

`DEC-13` was answered by the user on 2026-09-01 as option (a): **leave the QTI vendor tag `80340003` alone** — `F4.5-05` established it has no word to patch — **and pursue `FIND-4.5-02`'s stride hypothesis instead**, which the artifact's shape actually fits. That decision created `Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md`, which this Step 2 run authored. The reasoning is recorded in the ledger's section 8 and is not relitigated.

The revised Phase 4 order is:

1. **`Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md`, work items `F4.6-01` … `F4.6-04`.** Host-side, no device, no user, no attempt budget. `F4.6-04`'s reconstruction test may settle the diagnosis on its own, and nothing is gained by deferring free work behind live work.
2. **`Faz-4-Plans/Faz4.1-fullres-dimension-guard.md`**, in full.
3. **`Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md`, work items `F4.6-05` onward**, including `F4.6-07`, which is gated on step 2.
4. **`Faz4.2` → `Faz4.3` → `Faz4.4`**, unchanged.

**The `Faz4.1` sequencing question is decided here explicitly rather than left implicit, because `DEC-12`'s premise is now only half delivered.** `DEC-12` put `Faz4.5` first so that `Faz4.1`'s preservation check would run against a good capture rather than certify that a corrupt frame is still corrupt. The metadata is now right and the image is still wrong, so that premise is not satisfied. **`Faz4.1` runs anyway, in the position above, for three reasons.**

- **Its check is a metadata-integrity check, not an image-quality check.** `Faz4.1` verifies that narrowing did not drop the full-resolution RAW rows and that format 32 was added. Both are counts and rows in `dumpsys`. Neither depends on the frame being correct, so a corrupt image does not make the check vacuous — it makes one sentence of `DEC-12`'s rationale wrong, which is a different thing.
- **`Faz4.1` is an enabler for the diagnosis, not merely unblocked by it.** `EV-35` establishes that no application can obtain a full-resolution DNG until format-32 emission is extended, which is `DEC-11`'s work inside `Faz4.1`. The DNG is the probe that discriminates best in `Faz4.6` and it is also `H-03`'s outstanding probe. Deferring `Faz4.1` behind the whole of `Faz4.6` would deadlock the diagnosis at exactly the measurement that settles it.
- **Its own value is independent.** Narrowing is blast-radius reduction ahead of distribution (`QAS-04`), and the patch is intended for other people's devices whether or not AGC's image is fixed.

**The one thing that must not happen:** `Faz4.1` passing must never be reported as the image being fixed. While `FIND-3.5-01` is open, no Phase 4 result may conflate a metadata verdict with an image verdict. That constraint is written into `Faz4.6` section 10 and belongs in `Faz4.1`'s run record.

**Splitting a sub-plan around a dependency has precedent on this project** and is not an irregularity: `IMPL-19` pulled the recovery-runbook half of `Faz-9-Plans/Faz9.2-release-verification-checklist.md` forward and left the checklist half in Phase 9, and the audit's section 12 records that split as `READY_WITH_WARNINGS` with a resume point rather than as a defect.

## 5. Out-of-Scope or Deferred Topics

- **The beryl port itself.** Only sizing is planned. No beryl-specific file exists in the workspace and Autopsy gates decomposition on Phase 7's outcome. The commit decision is routed to the user.
- **The kernel LTS merge itself.** Only scoping is planned, for the same reason. Its effect on the CSIPHY and CSID allocation behavior that invariant 3 depends on is an assessment rather than a resolved question.
- **Continuous integration.** No CI exists and none is planned. A single-maintainer workflow with a manual flash step does not justify it, and the device is the only meaningful validation surface.
- **Signing key rotation.** Conditional work in `Faz-1-Plans/Faz1.2-signing-key-containment.md`, triggered only if the release archive audit finds the credential already distributed.
- **The version control remote.** Recorded as open in `Faz-1-Plans/Faz1.1-version-control-bootstrap.md` and gated on the credential audit, because a remote changes what may be committed and the AGC redistribution question becomes live once history leaves the machine.
- **Restructuring the engineering journal.** Its non-monotonic phase numbering is read as a signal rather than a defect. Only the superseded section is marked, and nothing is deleted.
- **New mode names for composed layer states.** If Phase 5 succeeds, the minimal change is to stop forcing the sensor layer to stock. Whether the interface gains combined modes is a separate product question.
- **Exhaustive validation of the composed mode space.** If the layers compose, the space becomes a product rather than a list. Validation is limited to the combinations the target end state names.
- **Converting the layer exclusion to a checked invariant.** `ARC-03` records the divergence. If the exclusion is removed there is nothing left to check; if it stands, converting it is a separate improvement needing its own justification.
- **A general patch composition mechanism or metadata-tag locator.** The project has one binary and a small number of tags. Reusable tooling is not justified by the current surface.
- **Deep diagnosis of any Phase 3 failure beyond symptom classification.** Bounded by the attempt budget, with the result routed to the decision gate rather than expanded into open investigation.

## 6. Coverage Check

- [x] Every main phase from `Planner-docs/Main-Planing.md` has a folder. Nine phases detected; nine folders present: `Faz-1-Plans` through `Faz-9-Plans`.
- [x] Every main phase has at least one sub-plan. Counts per phase: Phase 1 has 6, Phase 2 has 4, Phase 3 has 6, Phase 4 has **6**, Phase 5 has 3, Phase 6 has 2, Phase 7 has 2, Phase 8 has 2, Phase 9 has 3. Total: **34**. Counted from `find Planner-docs -type f -name 'Faz*.md'` on 2026-09-01, not from memory. Phase 4 grew from 5 to 6 in this run with `Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md`, and from 4 to 5 in the 2026-09-01 re-plan with `Faz4.5`.
- [x] Sub-plan numbering is contiguous within each phase, starting at 1 with no gaps.
- [x] Sub-plan filenames follow the `Faz<phase>.<sub>-<ascii-lowercase-kebab-slug>.md` convention, with no spaces and no non-ASCII characters.
- [x] No duplicate filenames and no duplicate phase-and-subphase numbers.
- [x] Every sub-plan file is referenced from this index, and every reference in this index resolves to an existing file.
- [x] Every sub-plan uses the required thirteen-section structure in the required order.
- [x] Every sub-plan carries an Implementation Contract table in section 9 with the `Path`, `State`, `Purpose`, and `Validation Command IDs` columns, repo-relative paths, and allowed state values.
- [x] Generated documents follow the language contract: English body, English headings.
- [x] No source code file was modified. Only files under `Planner-docs/` were created or updated.
- [x] No secret, token, credential, private key, or local sensitive environment value was written. The signing keystore is referenced by path only; its contents were never read.

## 7. Repository Review Notes

**Commands run.** `git status --short` and `git branch --show-current` at the workspace root, both returning `fatal: not a git repository`; `ls` at the root; `find Planner-docs -maxdepth 2 -type f`; `find ishtar-cam-modes -maxdepth 2 -type f`; `find agc-50mp-yama -type f`; `find ishtar-aon-fix -type f`; `sed -n` over `Main-Planing.md`, `Autopsy.md`, `Project-Ontology.md`, and `Project-Comprehension.md`; `cat` over `halpatch.sh`, `customize.sh`, `hal-raw50-deneme.patch`; `head` over `hal-fullres.patch`, `setmode.sh`, `verify_ln.py`, `module.prop`, `agc-50mp-yama/README.md`; `wc -l` over the two patch tables; `grep -n` over `post-fs-data.sh` for mode handling and over `webroot/index.html` for the shell-invocation surface; `grep -o` over both `.agc` configuration files for preference key names; `which` and version checks for a Python interpreter; and reads of the bundled validator and workflow-quality reference.

**Important files inspected.** `Planner-docs/Main-Planing.md` in full; `Planner-docs/Autopsy.md` in full; `Planner-docs/Project-Ontology.md` in full; `Planner-docs/Project-Comprehension.md` in full; `ishtar-cam-modes/halpatch.sh` in full; `ishtar-cam-modes/customize.sh` in full; `ishtar-cam-modes/setmode.sh` first 80 lines including the header and `restart_camera`; `ishtar-cam-modes/blobs/hal-fullres.patch` header and entries; `agc-50mp-yama/hal-raw50-deneme.patch` in full; `agc-50mp-yama/README.md` first 50 lines; `ishtar-cam-modes/tools/verify_ln.py` first 40 lines; `ishtar-cam-modes/module.prop`; `ishtar-cam-modes/post-fs-data.sh` mode dispatch; `ishtar-cam-modes/webroot/index.html` partial.

**New findings from this run, not present in the Step 1 or Step 1.5 artifacts.**

- Both root-level configuration files, `12mpx_agc_config.agc` and `50mpx_agc_config.agc`, contain the complete preference trap key families: `pref_raw_key` with suffixes 0 through 4, and `pref_fix_resolution_key` with suffixes 0 through 4. Project-Ontology invariant 8 identifies these as the trap that already caused one misattributed failure. Importing either configuration re-arms it. This is recorded in `Faz-3-Plans/Faz3.1-preference-trap-clearance.md` and routed to the artifact manifest in `Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md`.
- `ishtar-cam-modes/customize.sh` contains no statement that writes the `mode` file. It sets permissions and prints an intent message, but the packaged file supplies the post-install mode. This bears directly on `H-06` and `AUTOPSY-P3-03`, confirming the packaging concern is live rather than theoretical, and makes the build script in `Faz-9-Plans/Faz9.1-reproducible-release-build.md` the correct place to normalize.
- `agc-50mp-yama/hal-raw50-deneme.patch`'s four indices multiply by four to exactly the four `cmp` site addresses recorded in Project-Ontology section 6, independently confirming both records and the four-byte index convention.
- `ishtar-cam-modes/halpatch.sh` answers `OQ-05` directly: writes are ordered rather than atomic, but they target a module-private copy under `active_hal/` rather than the live binary, a partial result is classified as unrecognized by `hal_state`, and `hal_set` recovers by re-seeding from the device's stock binary. The mitigating detail matters as much as the bare answer.
- `halpatch.sh` also carries the module's two-state assumption throughout — `hal_state`, `hal_set`, and `hal_write` each test against exactly `fullres` and `stock` — which is the constraint governing the structural decision in `Faz-4-Plans/Faz4.3-patch-table-consolidation.md`.
- `hal_umount_all` loops up to forty times because a single unmount is insufficient when mounts are stacked, producing a false restored-to-stock conclusion. This is recorded as a required recovery scenario in `Faz-9-Plans/Faz9.2-release-verification-checklist.md`.
- No Python interpreter is available on this host through the normal path; `python` resolves to the Windows Store alias stub and `py` is absent. This makes the embeddable distribution a requirement rather than a preference for `Faz-1-Plans/Faz1.4-toolchain-procedure-record.md`, and a hard dependency for `Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md`, whose verification harness is Python.

**Assumptions made.** That the roadmap table in section 6 of the main plan is the authoritative phase list, confirmed by the matching phase headings. That Autopsy's scheduling feedback — pulling the smoke script into Phase 2 and the symlink entry early — is intended as execution-order guidance rather than as a renumbering of phases, so the folder structure preserves the master order while section 4 reflects the guidance. That the `refs/` tree roles are as Autopsy infers, with `Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md` tasked with verifying the inference before Phase 7 relies on it.

**Not verified in this run.** The tile application's Java sources, which no ClaudeQB run has read and whose tile-exclusivity mechanism is therefore an open question in `Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md`. The full `webroot/index.html` call-site set, left to `Faz-1-Plans/Faz1.5-static-safety-probes.md`. `ishtar-cam-modes/Kullanim.txt`, `action.sh`, and `service.sh` beyond line counts. The three kernel checkouts beyond their presence. The contents of any release archive, left to the audit in `Faz-1-Plans/Faz1.2-signing-key-containment.md`. The device's live state, which no planning step can establish and which `Faz-2-Plans/Faz2.1-device-smoke-script.md` resolves on its first run.

**Validator status.** The bundled validator at `scripts/validate_planner_docs.py` could not be executed: no Python interpreter is available on this host. Equivalent all-file validation was performed instead, checking every generated file for the filename convention, the folder-to-phase number match, the thirteen required sections in the required order, heading uniqueness, contiguous sub-plan numbering, index reference resolution in both directions, Implementation Contract table presence with the required headers and allowed state values, and length-bounded secret patterns by file name only. This fallback is stated explicitly here and in the Step 2 completion report.

**Second Phase 4 re-plan run, 2026-09-01 (`DEC-13`(a)).** Scope: author the sub-plan `DEC-13`(a) requires and reconcile the ordering around it. Files written: `Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md` (new, thirteen sections), `Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md` (amended to carry `FIND-4.5-01` and to repair `AUDIT-FIX-09`), this index (sections 2, 3, 4, 4a, 4b, 6, 7), and `Planner-docs/Planing-Ledger.md` (planning-run row, snapshot count, status matrix row, `DEC-13` action closure). No sub-plan outside Phase 4 was read or changed, and `Main-Planing.md` was not edited. Findings discharged in this run: `AUDIT-FIX-05` (the "ten open" count in section 2), `AUDIT-FIX-09` (the three unqualified "508 baseline" references in `Faz4.4`), `AUDIT-FIX-10` (the `Main-Planing` scope divergence, recorded in section 3 under Phase 4 by the first of the two options the audit offered), and `AUDIT-FIX-13` (section 4a marked discharged without deleting its reasoning). `AUDIT-FIX-08`'s permanent fix — landing the eighth per-measurement checklist item in `docs/phase3-preconditions.md` — is **routed** by this run rather than discharged: `Faz4.6` takes write authority for that file and `F4.6-09` lands the item, which is what the audit said "remains outstanding for Step 2 to route." `AUDIT-FIX-11` remains open and is the `FIND-1.4-01` vocabulary work.

**Two things this run did not do, stated so they are not assumed.** It did not re-derive any of the `Faz4.5` evidence, which is taken as reported from `IMPL-27` … `IMPL-30`. It did not add evidence rows to `Project-Comprehension.md` or address-book entries to `Project-Ontology.md`, because those record measurement and this run measured nothing — `EV-37` through `EV-40` and the section 6 entries were written by the Step 4 run that produced them, which is the correct boundary.

**Validator status amendment, 2026-09-01 (Phase 4 re-plan run).** A Python interpreter is now available on this host, and the bundled validator was executed for this run rather than emulated. It reports **11** warnings in `--mode step2 --strict`, and that is the correct baseline for a Step 2 run at commit `947a01b`. The **12**-warning figure recorded in `IMPL-24` and `IMPL-25` is the `--mode step3` / `--mode step4` baseline: those modes read `Sub-Planing-Audit.md` and add one further warning, `step4_has_nonblocking_warnings=P2:2,P3:3`, which no Step 2 run can produce. The eleven are unchanged in identity and count before and after this run's edits, so the `FIND-1.4-01` baseline is held; the mode, not the baseline, is what differs.
