# Faz 9.2 — Release Verification Checklist and Recovery Runbook

## 1. Context

Main-Planing Phase 9 asks for "a release checklist mapping each claimed capability to a proving command", and its target end state elaborates: "A release checklist tying each claimed capability to a command that proves it. Regression evidence recorded per release rather than per conversation."

Its acceptance signal names a property most checklists lack: "the smoke script correctly reports both a known-good and a known-bad state." A verification surface that only ever sees passing states has never been tested as a detector.

A second deliverable belongs here and comes from a different source. Project-Comprehension `QAS-01` describes the recoverability scenario: "a patch is written with a stale offset and the camera HAL is corrupted … the user can restore stock and reopen the camera without reflashing the ROM. Current state: the md5 guard should prevent the write, but if a write does land there is no documented recovery path." `ARC-11` records "Recovery from a broken module" as `absent`, and `CQ-09` — "Can the module brick the camera, and how is it recovered?" — is open.

Autopsy section 10 states the same gap with its timing: "What does not exist is a **documented recovery runbook for the case where the module itself is what broke**. On this device a corrupted camera HAL means no camera until reflash, so the recovery path deserves to be written down before it is needed rather than after."

Autopsy section 4 lists it under missing components: "A stock-restore runbook independent of `setmode.sh` (relevant precisely when `setmode.sh` is what went wrong)."

The two deliverables pair naturally: the checklist proves a release works, and the runbook covers what to do when one does not.

## 2. Goal

Produce a release verification checklist that maps every claimed capability to a proving command, validated by demonstrating that the verification surface detects a known-bad state, together with a recovery runbook that does not depend on the module being functional.

## 3. Description

The problem has two halves. The first is that this project's capability claims live in `module.prop`'s description field and in the journal, with no command attached to any of them — so a claim like "video 1080p60/4K60 unaffected" is verified when someone remembers to check. The second is that the recovery path exists only as a concept.

It belongs after the build script because a checklist verifies a release, and after Phases 4 and 5 because those change what is claimed.

The vibecoding slice strategy: derive the capability list from what the release actually claims, attach a proving command to each, then test the verification surface against a deliberately broken state. The fastest useful signal is the known-bad test, because it is the one thing that distinguishes a checklist from a ritual.

What should not be over-planned: a test framework, automated release gating, or continuous verification. Most of the checklist's items require the user's hands, which is a domain property rather than a deficiency.

The known-bad test needs a safe construction. The point is to prove the smoke script detects a wrong state, not to break the device. A deliberately mismatched checksum, a deliberately unmounted path, or a deliberately stale mode value each produce a detectable wrong state without risking the camera stack — and choosing among them is a design decision the sub-phase makes rather than improvising.

The recovery runbook has a constraint that shapes it entirely: it must work when the module is what broke. That rules out `setmode.sh`, `action.sh`, the tiles, and the web interface, since all of them are the module. What remains is the KernelSU module disable path, direct unmounting, and reflashing — and the runbook should establish which of these suffices for which failure.

## 4. Scope

- A capability list derived from what the release claims, sourced from `module.prop` and the target end state.
- A proving command for each claimed capability, distinguishing those the smoke script covers from those requiring the user.
- A known-good and known-bad demonstration proving the verification surface detects a wrong state.
- A recovery runbook covering: a corrupted HAL copy, a stuck mount, a module that fails at boot, and a camera that will not open.
- Explicit independence of the runbook from module-provided commands.
- A statement of which failures the module's own guards prevent, so the runbook covers what actually remains.
- A per-release evidence record format, so regression evidence lives with the release rather than in a conversation.
- Resolution of `CQ-09` and `ARC-11`.

## 5. Out of Scope

- The build script, which is Faz 9.1.
- Documentation consolidation, which is Faz 9.3.
- Any change to module behavior, guards, or recovery capability. This sub-phase documents and verifies what exists.
- Automated release gating or continuous verification.
- ROM reflash procedure, beyond naming it as the last resort. That is device vendor territory.
- Deliberately corrupting the device's camera HAL to test recovery. The known-bad test is constructed safely.
- Verification of the Android 16 build, which has its own registered check in Faz 7.2.

## 6. Current Repository Evidence

`ishtar-cam-modes/module.prop` was read in this run and its description field is the de facto capability claim list. It claims: DCG and LN modes applied to the sensor driver; `dcgB` measured at roughly 25% less noise and double the detail with no shutter speed change and no property override required; four QuickSettings tiles with mutual exclusion; a corrected camera restart that no longer locks the camera; mode changes that complete only when the camera is genuinely ready; a bilingual interface independent of system locale; a live countdown during transitions; 50 MP full resolution added to the standard list so third-party applications capture at full resolution, measured at 50.3 MP in Open Camera; video at 1080p60 and 4K60 unaffected; the 27 MB binary not shipped; mutual exclusion between 50 MP and the sensor modes; and correct launcher icon rendering with status read from the framework.

That is thirteen distinct claims in one field, which is both the source for the checklist and, per `AUTOPSY-P3-01`, a documentation problem Faz 9.3 addresses separately.

Two claims are already known to need updating. Autopsy `AUTOPSY-P2-03` records that the v2.0 description states AGC remains at 12.6 to 15.2 MP because the GCam engine cannot select the 50 MP stream — a causal claim Faz 12 disproved and which `IMPL-23` and `IMPL-43` then disproved by measurement. The checklist should be built against corrected claims, and correcting them is Faz 9.3's work.

**Amended 2026-09-04 by planning run 10 (`AUDIT-FIX-18`, `DEC-14`).** The claim has two halves and only one of them is stale, so the checklist entry this evidence produces must be split accordingly. The **causal** half is false and `Faz9.3` corrects it. The **resolution figure** is now correct for a new reason: `DEC-14` retired the 50 MP-in-AGC objective and adopted 12.58 MP as AGC's pinned working resolution, so what this checklist must prove is not "AGC is stuck at 12.6 MP" and not "AGC reaches 50 MP", but that **AGC launches and captures cleanly at 12.58 MP in the same HAL state in which Open Camera captures 50.3 MP** — the coexistence claim. Its proving command and its expected values come from `Faz-3-Plans/Faz3.11-phase-closure-and-configuration-record.md` and the `docs/agc-12mp-configuration.md` record it produces, which state the expected pin, the expected configured stream, and the black-fraction reference numbers. Building this row against the pre-`DEC-14` framing would put a claim in the checklist that the shipped module is not trying to make.

`ishtar-cam-modes/halpatch.sh` was read in this run and documents the guards that bound what recovery must cover. `hal_seed` refuses to run while the target is mounted, requires the device binary's checksum to match the recorded stock value, and verifies the copy afterward. `hal_set` re-seeds when the state is unrecognized. `hal_umount_all` loops up to forty times because a single unmount is insufficient when mounts are stacked — a measured finding recorded in its comments, and directly relevant to the stuck-mount recovery case.

That stacked-mount behavior is the most useful recovery evidence in the tree: it documents a real failure mode where a single unmount reports success while the file remains patched, producing a false "restored to stock" conclusion.

`ishtar-cam-modes/customize.sh` aborts on a sensor driver checksum mismatch and warns without aborting on an unrecognized HAL checksum, disabling 50 MP while leaving the sensor modes functional. That degradation path is itself a recovery-relevant behavior.

`ishtar-cam-modes/post-fs-data.sh` maps any unrecognized mode value to stock across all three variables, which means a corrupted mode file self-heals at boot.

Project-Ontology invariant 1 records reversibility as a standing requirement: "Every modification is a bind-mount or an md5-guarded offset patch. A module that cannot be turned off is a bricked phone." Invariant 2 records the fail-closed ordering.

Faz 2.1's smoke script and Faz 2.3's regression record exist by this point and are the surfaces the checklist builds on.

## 7. Planned Work Breakdown

- F9.2-01 — Derive the capability list
  - Description: Extract the claims from `module.prop` and the target end state, using the corrected versions where Faz 9.3 has updated a stale claim. Count them explicitly rather than summarizing.
  - Output: An enumerated capability list.
- F9.2-02 — Attach a proving command to each capability
  - Description: For each claim, name the command or check that proves it, and classify it as smoke-script-covered or user-performed. A claim with no proving command is either unverifiable or not a capability.
  - Output: A capability-to-command map with a coverage classification.
- F9.2-03 — Design the known-bad construction
  - Description: Choose a safe way to produce a detectably wrong state — a mismatched checksum, an absent mount, or a stale mode value — without risking the camera stack.
  - Output: A known-bad construction with its safety rationale.
- F9.2-04 — Demonstrate known-good and known-bad detection
  - Description: Run the verification surface against both states and confirm it reports them differently. This is Main-Planing's own acceptance signal.
  - Output: Two verification runs with distinguishable results.
- F9.2-05 — Enumerate the failure modes the guards do not prevent
  - Description: Establish what the size and checksum guards already prevent, so the runbook covers what actually remains rather than restating what cannot happen.
  - Output: A residual failure mode list.
- F9.2-06 — Write the recovery runbook
  - Description: Cover a corrupted HAL copy, a stuck or stacked mount, a module failing at boot, and a camera that will not open. Every step must work without module-provided commands.
  - Output: A recovery runbook with four scenarios.
- F9.2-07 — Verify the runbook's independence
  - Description: Review every step and confirm none depends on `setmode.sh`, `action.sh`, the tiles, or the web interface, since the runbook is for when those are what broke.
  - Output: A per-step independence verdict.
- F9.2-08 — Define the per-release evidence record
  - Description: Specify the format that ties a release to its verification results, so regression evidence lives with the release. Faz 2.3's regression record is the precedent.
  - Output: An evidence record format.
- F9.2-09 — Resolve the recovery questions
  - Description: Answer `CQ-09` and update `ARC-11` from `absent`.
  - Output: Updated continuity artifacts.

## 8. Acceptance Criteria

- The capability list enumerates every claim the release makes, with a count reported after derivation rather than from memory.
- Every capability has a proving command, classified as smoke-covered or user-performed; any capability without one is explicitly marked unverifiable.
- The known-bad construction is safe, with its rationale recorded.
- The verification surface reports the known-good and known-bad states differently, demonstrated with real output.
- The residual failure mode list distinguishes what the guards prevent from what remains.
- The recovery runbook covers all four scenarios.
- Every runbook step is verified independent of module-provided commands.
- The stacked-mount behavior is covered, since a single unmount producing a false success is a documented real failure.
- The per-release evidence record format is defined and used for the current release.
- `CQ-09` is answered and `ARC-11` is updated from `absent`.

## 9. Validation and Test Approach

Validation includes a negative demonstration, which is what separates this sub-phase from writing a document. A checklist that has only ever seen a passing state is unproven as a detector.

- `VAL-KNOWNBAD` (proposed) — the verification surface run against a deliberately wrong state, confirming it reports differently from the good state. Main-Planing's acceptance signal.
- `VAL-SMOKE` (from Faz 2.1) — the good-state run and the coverage classification's basis.
- `VAL-COVERAGE` (proposed) — every capability confirmed to have a proving command or an explicit unverifiable marking.
- `VAL-INDEPENDENCE` (proposed) — the per-step review confirming the runbook does not depend on the module.
- `VAL-MANUAL` (proposed) — the user-performed checks in the checklist, exercised once to confirm they are executable as written.

Local versus live: the checklist derivation and the runbook are local; the known-good and known-bad demonstrations and the manual checks are live. Security validation is not applicable. Ontology validation applies to invariants 1 and 2, which the runbook operationalizes.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | The verification surface being proven as a detector. | VAL-KNOWNBAD, VAL-SMOKE |
| ishtar-cam-modes/module.prop | existing | Source of the capability claims the checklist is derived from. | VAL-COVERAGE |
| ishtar-cam-modes/halpatch.sh | existing | Read-only evidence of the guards and the stacked-mount behavior the runbook must cover. | VAL-INDEPENDENCE |
| docs/release-checklist.md | proposed | The capability-to-command map and the evidence record format. | VAL-COVERAGE, VAL-MANUAL |
| docs/recovery-runbook.md | proposed | The four-scenario recovery procedure, independent of the module. | VAL-INDEPENDENCE |

## 10. Dependencies and Sequencing

Depends on Faz 9.1 for a script-produced release to verify, on Faz 2.1 for the smoke script, and on Faz 2.3 for the regression record precedent.

Depends on Faz 9.3 for corrected capability claims, or must note which claims it verified against stale text. The two sub-phases interact and running Faz 9.3 first is preferable.

Depends on Phases 4 and 5 for a settled capability set.

Blocks nothing, but a release should not ship without it, since it is what turns the release from an artifact into a verified one.

Required decisions: the known-bad construction, which the implementer designs and records.

Required infrastructure: the device, and a release produced by Faz 9.1's script.

Required human actions: the user-performed checks and the known-bad demonstration.

Fresh session token and context risk: low to medium. Thirteen or more capabilities each with a check, at low per-item cost.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the checklist is written and never tested against a bad state. Impact: a verification surface that cannot detect failure, which is worse than none because it produces false confidence. Mitigation: `VAL-KNOWNBAD` is the sub-phase's headline validation and Main-Planing names it as the acceptance signal.
- Risk: the known-bad construction damages the camera stack. Impact: the test causes the failure it was meant to detect. Mitigation: F9.2-03 requires a safe construction with a recorded rationale, and three safe options are named.
- Risk (`ARC-11`, `QAS-01`): the runbook depends on module commands. Impact: it fails precisely in the case it exists for. Mitigation: F9.2-07 reviews every step and `VAL-INDEPENDENCE` requires a per-step verdict.
- Risk: the stacked-mount case is missed. Impact: a recovery that reports success while the file remains patched — a documented real failure in this codebase, recorded in `halpatch.sh`'s own comments. Mitigation: the acceptance criteria name it explicitly.
- Risk (`AUTOPSY-P2-03`): the checklist verifies a stale claim, such as the disproven statement about the AGC ceiling. Impact: a proving command that proves something the project no longer believes. Mitigation: the dependency on Faz 9.3 is stated, with a requirement to note any claim verified against uncorrected text.
- Risk: a capability has no practical proving command and is quietly dropped. Impact: an unverified claim ships as if verified. Mitigation: `VAL-COVERAGE` requires an explicit unverifiable marking rather than omission.
- Risk: the runbook is written but never exercised. Impact: a procedure with defects discovered at the worst moment. Mitigation: the known-bad demonstration exercises at least the detection half, and the residual failure mode list keeps the runbook scoped to what can actually happen.
- Risk: per-release evidence is defined and then not produced for the current release. Impact: the format exists and the practice does not. Mitigation: the acceptance criteria require it to be used for the current release.

## 12. Desired End State

Every capability the release claims has a proving command, classified by whether it is automated or user-performed. The verification surface has been demonstrated to distinguish a good state from a deliberately wrong one. A recovery runbook covers four failure scenarios with every step independent of the module, including the stacked-mount case that produces false success. Regression evidence has a per-release format and the current release uses it. `CQ-09` is answered and `ARC-11` is no longer absent.

The evidence an implementer should produce is the enumerated capability list with its coverage map, the two distinguishable verification runs, the residual failure mode list, the runbook with its per-step independence verdicts, and the current release's evidence record.

The ledger summary Step 4 should append records: the capability count, the coverage classification, the known-bad result, the runbook scenarios covered, and the `CQ-09` and `ARC-11` updates.

## 13. Next Sub-Phase Transition Criteria

- Every capability has a proving command or an explicit unverifiable marking.
- The known-bad demonstration shows the verification surface detecting a wrong state.
- The runbook covers four scenarios with every step verified module-independent.
- The stacked-mount case is covered.
- The per-release evidence record exists for the current release.
- `CQ-09` and `ARC-11` are resolved.
