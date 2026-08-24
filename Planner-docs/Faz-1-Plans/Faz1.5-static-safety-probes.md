# Faz 1.5 — Static Safety Probes

## 1. Context

Project-Comprehension section 8 lists ten open hypotheses and closes with an explicit instruction: "Probes H-06 through H-09 are static, cheap, and answer P1/P2 questions — they should be batched into Phase 1 rather than deferred."

Four of those probes read a file and answer a question that is currently marked `tentative` or `open`. Between them they close `OQ-05`, `OQ-06`, `OQ-07`, and `OQ-08` in Project-Ontology section 8, and `CQ-11` and `CQ-12` in Project-Comprehension section 1. None requires the device, a build, or the user's hands.

Autopsy reinforces two of them as cross-cutting actions: "Read `webroot/index.html` for shell-injection exposure before the next release" and "Audit `post-fs-data.sh`, `halpatch.sh`, and `customize.sh` for the same fail-closed discipline `setmode.sh` demonstrates." Both are filed as security review, and both block Phase 2's release with confidence.

This Step 2 run already read several of these files while gathering evidence, which means some answers are partially known. Those partial answers are recorded in section 6 below and this sub-phase's job is to complete and formally record them, not to rediscover them.

## 2. Goal

Close the batch of cheap static questions about packaging hygiene, input handling, write discipline, and policy files, converting six open or tentative entries in the continuity artifacts into evidenced answers before any device work or release begins.

## 3. Description

The problem is a set of small unknowns that individually look deferrable and collectively block confident release. Each one is a single file read. Left open, they turn into assumptions, and Autopsy section 5 already shows what assumption-driven packaging costs — runtime state checked into the deliverable directory that nobody has confirmed gets normalized.

It belongs in Phase 1 because the answers are inputs to Phase 2's release decision and to Faz 1.3's atomicity section, and because the cost of answering is minutes while the cost of assuming has already been paid once in this project's history.

The vibecoding slice strategy: read the four files in one pass, record each answer where the question lives, and stop. The fastest validation signal is that every targeted question row in the continuity artifacts changes state in the same session. What should not be over-planned is remediation — several probes may reveal a defect, and fixing it is a separate decision that belongs where the defect lives, not here. This sub-phase produces findings; the fixes are scheduled after the findings exist.

One probe has a known constraint. `H-06` asks whether `customize.sh` normalizes the `mode` file at install time. Evidence gathered in this run suggests it does not, which makes `AUTOPSY-P3-03` a live packaging issue rather than a theoretical one. The probe must confirm this against the whole file rather than concluding from a partial read.

## 4. Scope

- `H-06` and `OQ-07`: whether `customize.sh` normalizes `mode` and `active/` at install, and what the packaged module actually ships as its initial state.
- `H-07`, `OQ-06`, and `CQ-11`: whether `webroot/index.html` passes any unsanitized value into a shell invocation through the WebUI bridge.
- `H-08`, `OQ-05`, and `CQ-12`: whether patch application is atomic against power loss, and what the recovery path is when it is not.
- `OQ-08`: whether `ishtar-cam-modes` ships its own policy rule file, which the reference modules do.
- A fail-closed discipline review across `post-fs-data.sh`, `halpatch.sh`, and `customize.sh`, comparing each against the size-then-checksum-then-write pattern `setmode.sh` demonstrates.
- Recording every answer in `Planner-docs/Project-Ontology.md` and `Planner-docs/Project-Comprehension.md` in the same session it is obtained.
- Raising any defect found as a finding routed to the phase that owns the affected file.

## 5. Out of Scope

- Fixing any defect discovered. Remediation is scheduled after the finding exists and belongs to the owning phase.
- Any device interaction, flash, or capture. Every probe here is a file read.
- Reading the tile application's Java sources or the three kernel checkouts.
- The four Python tools beyond confirming their dependency surface, which Faz 1.4 already covers.
- `H-01` through `H-05` and `H-10`, which need disassembly, the device, or the user's hands and belong to Phases 3, 5, and 2 respectively.
- Deciding the fate of the `tiles hide` option, which is a Phase 2 decision gate with a different owner.

## 6. Current Repository Evidence

Partial answers obtained during this Step 2 evidence pass, to be confirmed rather than repeated:

`ishtar-cam-modes/customize.sh` (78 lines) was read in full. It aborts when `ro.product.device` is not `ishtar`, aborts when the sensor driver md5 does not match `9e4d0fe1a8bf2eb4146c9917a0ac2c4c`, warns without aborting when the HAL md5 matches neither the stock nor the fullres value, and then calls `set_perm_recursive` plus five `set_perm` calls. It prints "Baslangic modu: ilk kurulumda stock; guncellemede mevcut mod". No statement in the file writes to the `mode` file. This is strong evidence that the packaged `mode` file's content is the initial install mode, which makes `AUTOPSY-P3-03` a real packaging concern.

`ishtar-cam-modes/webroot/index.html` (344 lines) was partially read. Line 123 defines `const ACT = 'sh ' + MODDIR + '/action.sh';`. Line 193 defines `function exec(cmd)` which delegates to `ksu.exec(cmd, ...)`. Line 300 calls `await exec(cmd)` where `cmd` is built by callers. The observed call sites build commands from a fixed mode identifier list and from a two-value language toggle. Three `innerHTML` assignments exist at lines 237, 276, and 314. The full trace of every `exec` call site has not been completed.

`ishtar-cam-modes/halpatch.sh` (116 lines) was read in full and answers `OQ-05` directly. `hal_write` applies entries sequentially with `dd conv=notrunc` and is therefore ordered rather than atomic. However the write target is `$MODDIR/active_hal/camera.qcom.so`, a module-private copy, not the live `/odm/lib64/hw/camera.qcom.so`. `hal_state` classifies a copy whose md5 matches neither known value as `unknown`, and `hal_set` re-seeds from the device's stock binary when the state is `unknown` or `none`. A power loss mid-write therefore leaves a detectable bad copy that is discarded, not a corrupted live binary.

`ishtar-cam-modes/post-fs-data.sh` (131 lines) was partially inspected. Its mode dispatch maps unrecognized values to `MODE=stock`, `SENSOR_MODE=stock`, `HAL_WANT=stock` — a fail-safe default.

`ishtar-cam-modes/` contains no file named `sepolicy.rule` in its top two directory levels, which bears on `OQ-08` but should be confirmed against the packaged archive as well as the source directory.

## 7. Planned Work Breakdown

- F1.5-01 — Confirm the install-time state normalization question
  - Description: Verify against the whole of `customize.sh` that no path writes the `mode` file, and determine whether the packaged archive ships `mode` and `active/` at all. If it does, `AUTOPSY-P3-03` becomes a confirmed packaging defect.
  - Output: `H-06` and `OQ-07` answered; a finding raised if the defect is confirmed.
- F1.5-02 — Trace every WebUI shell invocation
  - Description: Enumerate every call site that reaches `exec` and determine for each whether its argument is drawn from a fixed set or from user-controllable input. Also assess the three `innerHTML` assignments for whether any renders device-derived text.
  - Output: `H-07`, `OQ-06`, and `CQ-11` answered with the call sites enumerated.
- F1.5-03 — Record the atomicity finding formally
  - Description: State the answer to `OQ-05` as: writes are ordered but not atomic, applied to a module-private copy, with a partial result detected by md5 classification and recovered by re-seeding from the device's stock binary. Cite `hal_write`, `hal_state`, and `hal_set`.
  - Output: `OQ-05` and `CQ-12` answered; the text feeds Faz 1.3's atomicity section.
- F1.5-04 — Review fail-closed discipline across the three unaudited scripts
  - Description: Compare `post-fs-data.sh`, `halpatch.sh`, and `customize.sh` against the size-then-checksum-then-write pattern. Record for each whether every write is guarded and whether every failure path is closed rather than continuing.
  - Output: A three-script discipline table with any gap named.
- F1.5-05 — Resolve the policy rule file question
  - Description: Determine whether `ishtar-cam-modes` ships a policy rule file, checking both the source directory and the most recent release archive, since the two can differ.
  - Output: `OQ-08` answered.
- F1.5-06 — Update the continuity artifacts in the same session
  - Description: Write every answer into `Planner-docs/Project-Ontology.md` section 8 and `Planner-docs/Project-Comprehension.md` sections 1, 2, and 8 before the session ends, per the recording rule those documents state.
  - Output: Six or more updated rows with evidence cited.
- F1.5-07 — Route each finding to its owning phase
  - Description: For every defect discovered, name the phase and sub-plan that should remediate it, rather than absorbing the fix here.
  - Output: A findings-to-phase routing list.

## 8. Acceptance Criteria

- `OQ-05`, `OQ-06`, `OQ-07`, and `OQ-08` in Project-Ontology section 8 no longer read `open`, and each Evidence cell names the file and the specific function or line evidence.
- `H-06`, `H-07`, and `H-08` in Project-Comprehension section 8 are no longer `tentative`.
- `CQ-11` and `CQ-12` in Project-Comprehension section 1 no longer read `open`.
- The WebUI trace enumerates every `exec` call site rather than sampling; a conclusion of "no unsanitized input" is supported by an exhaustive list or is not stated.
- The fail-closed review covers all three scripts and states, for each, whether a gap exists.
- If `customize.sh` is confirmed not to normalize install state, a finding exists naming the owning phase for the fix.
- Every answer is recorded in the same session it is obtained; no answer is left as a note to write up later.
- No probe in this batch required the device, a build, or the user's physical action.

## 9. Validation and Test Approach

All validation here is static source review plus document verification. The distinguishing property of this batch is that nothing requires live readiness — that is precisely why it is scheduled in Phase 1.

- `VAL-STATIC` (proposed) — read each targeted file in full and record the specific evidence, by function name or line number, that supports each answer.
- `VAL-DOCS` (proposed) — read back the updated rows in both continuity artifacts; confirm each cites evidence rather than asserting a conclusion.
- `VAL-SEC` (proposed) — the WebUI input-handling trace and the three-script fail-closed review, both treated as security review outputs rather than as general code reading.

Local smoke, live readiness, CI, and artifact validation are not applicable. Ontology consistency is the primary secondary check: every answer must use the vocabulary in Project-Ontology section 2, keeping the sensor, HAL, and application layers distinct.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/customize.sh | existing | Probe target for install-time state normalization and abort discipline. | VAL-STATIC, VAL-SEC |
| ishtar-cam-modes/webroot/index.html | existing | Probe target for the shell-invocation and rendering surface. | VAL-SEC |
| ishtar-cam-modes/halpatch.sh | existing | Probe target for write atomicity and checksum-guarded recovery. | VAL-STATIC |
| ishtar-cam-modes/post-fs-data.sh | existing | Probe target for boot-time fail-closed discipline. | VAL-STATIC, VAL-SEC |
| Planner-docs/Project-Ontology.md | modified | Record the four resolved ontology questions with evidence. | VAL-DOCS |
| Planner-docs/Project-Comprehension.md | modified | Update hypothesis confidence and the two resolved comprehension questions. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 1.1 in the weak sense that recording answers into a versioned tree is preferable, but the probes themselves have no prerequisite.

Feeds three consumers. Faz 1.3 consumes the atomicity answer for its contract section. Faz 2.2 consumes the install-state answer before flashing, because flashing a module that ships developer state is exactly the kind of surprise a baseline snapshot should not contain. Faz 9.1 consumes the packaging findings.

Should run before Faz 2.2. If a packaging defect is confirmed, the user should know it before the release is flashed rather than after.

Required decisions: none to run the probes. Any defect found creates a scheduling decision, which the routing list in F1.5-07 makes explicit rather than implicit.

Required credentials, infrastructure, live endpoints, or approvals: none.

Fresh session token and context risk: low. Four files totalling roughly 670 lines, three of which have already been read in part. Subagents are not recommended — the files are small, the parent holds the context, and splitting the review across agents would fragment the findings.

## 11. Risks and Mitigations

- Risk: the WebUI trace samples call sites rather than enumerating them and concludes there is no injection surface. Impact: a false clean verdict on the one component that accepts user input. Mitigation: the acceptance criteria require an exhaustive enumeration or no conclusion at all.
- Risk: a probe reveals a defect and the fix is absorbed into this sub-phase because it looks small. Impact: scope creep in a phase meant to be cheap, and the fix lands without the owning phase's validation. Mitigation: F1.5-07 routes findings rather than fixing them, and the out-of-scope section states this explicitly.
- Risk (`AUTOPSY-P3-03`): the install-state finding is confirmed but treated as cosmetic. Impact: a release ships the developer's last-used mode, and a user's first boot applies a mode they did not choose. Mitigation: the finding is routed to a packaging sub-plan and gates Faz 2.2's flash.
- Risk: answers are gathered and written up "later in the session". Impact: exactly the loss Project-Comprehension section 8 warns about — findings deferred within a session are the ones lost to context truncation. Mitigation: F1.5-06 is a work item, and the acceptance criteria require same-session recording.
- Risk: the atomicity answer is recorded as "not atomic" without the mitigating detail that writes target a private copy. Impact: a future reader over-estimates the risk and plans unnecessary work. Mitigation: F1.5-03 requires the full mechanism, including the re-seed recovery path.
- Risk: the policy rule file check inspects only the source directory. Impact: a discrepancy between source and shipped archive goes unnoticed. Mitigation: F1.5-05 checks both.

## 12. Desired End State

Six previously open or tentative entries across the two continuity artifacts are answered with cited evidence. The project knows whether its installer normalizes state, whether its only user-input surface can reach a shell, what happens to a patch interrupted by power loss, and whether it ships a policy rule file. Every script that writes as root at boot has been reviewed against the same fail-closed standard, and any gap is named.

The evidence an implementer should produce is the set of updated rows in both continuity artifacts, the enumerated WebUI call-site list, and the three-script discipline table.

The ledger summary Step 4 should append records: which questions were closed, which findings were raised, and which phase each finding was routed to.

## 13. Next Sub-Phase Transition Criteria

- All six targeted question rows have changed state and cite evidence.
- The WebUI call-site enumeration is complete, not sampled.
- The fail-closed review covers all three scripts with a per-script verdict.
- Every finding has a named owning phase, and none has been silently fixed here.
- Faz 2.2 has the install-state answer available before any flash is attempted.
