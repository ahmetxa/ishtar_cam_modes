# Faz 7.1 — WSL2 Provisioning and Toolchain Smoke

## 1. Context

Main-Planing Phase 7's goal is "Reach the point where an AOSPA Android 16 build can actually be attempted", and its description names the single blocker: "Disk is no longer a blocker (C: 953 GB, 799 GB free, re-measured 2026-08-23). The remaining blocker is that **WSL2 is not installed**."

Its first vibecoding slice is stated as: "Install WSL2 and verify a trivial kernel `make defconfig` inside `~/`, before attempting a full ROM sync."

Risk `R9` records the constraint: "No WSL2; NTFS case-insensitivity already breaks kernel checkouts." The description elaborates: "the workspace's kernel checkouts already carry 14 case-collision paths and required a sparse-checkout trick excluding three DOS-reserved filenames. Sources must be cloned inside the WSL filesystem, never under `/mnt/c`."

Project-Ontology invariant 11 records the same as a durable constraint, and Project-Comprehension `EV-20` records the WSL2 absence with confidence `probable`, sourced from a user statement.

Main-Planing section 9 marks this phase for lower-detail planning: "Do not expand yet. Phases 7, 8, and 9. G is blocked on host-environment work the user must perform." This sub-plan is therefore scoped to the environment work and its smoke test, leaving the ROM build to Faz 7.2.

Main-Planing also notes: "This phase is largely environment work and depends on user action on the host machine."

## 2. Goal

Establish a Linux build environment on the host that can compile kernel sources, verified by a real build action rather than by the environment's existence, with sources located inside the Linux filesystem where the case-sensitivity constraint is satisfied.

## 3. Description

The problem is that this workspace cannot build what it is a workspace for. Three kernel checkouts and five device trees exist for reading, and neither the kernel nor AOSP will compile on Windows or NTFS. The evidence of the constraint is already concrete rather than theoretical: fourteen case-collision paths in the existing checkouts and three DOS-reserved filenames that had to be excluded by sparse checkout.

It belongs after the camera work because it opens a second front. Main-Planing's planning conclusion is explicit: "the project should stop widening and start consolidating … and only then open the Android 16 front."

The vibecoding slice strategy is Main-Planing's own: provision, then verify with a trivial kernel configuration step inside the Linux home directory. That single action tests the toolchain, the filesystem location, and the case-sensitivity constraint at once, and it costs minutes rather than the hours a ROM sync would.

What should not be over-planned: the AOSP source sync, build configuration, and device selection. Those belong to Faz 7.2 and depend on this sub-phase succeeding.

Two decisions are genuinely open and should be marked rather than resolved by planning. The first is which Linux distribution and version, which interacts with the AOSP build requirements more than with the kernel's. The second is where the sources live and how much space they need — the 799 GB free figure was measured on the Windows volume, and a Linux filesystem inside WSL2 draws from the same disk but through a virtual disk whose growth behavior is its own consideration.

## 4. Scope

- WSL2 installation on the host, which is the user's action.
- A distribution choice, marked as an open decision with the AOSP requirements as the deciding input.
- Verification that the Linux filesystem is case-sensitive and that sources placed there avoid the collisions the Windows checkouts hit.
- Installation of the kernel build toolchain.
- A trivial kernel configuration step executed inside the Linux home directory, as the smoke test.
- A deliberate confirmation that sources are not under the Windows mount, since Main-Planing states this as a hard constraint.
- A disk space assessment for the virtual disk, distinct from the Windows volume measurement already taken.
- Recording of the provisioning steps so the environment is reproducible, in the same spirit as Faz 1.4's toolchain procedure.
- Update of `EV-20` once WSL2 is present, changing it from a user statement to a measured fact.

## 5. Out of Scope

- The AOSP source sync and the first ROM build. Faz 7.2 owns those.
- Any beryl work, which is Phase 8.
- Merging GKI LTS into the kernel tree, which is Phase 8.
- Migrating the existing Windows kernel checkouts into the Linux filesystem. Fresh clones inside Linux are the correct approach given the collision history, and the existing checkouts remain for reading.
- Any camera, module, or device tree change.
- Building a kernel image. The smoke test is a configuration step, not a compile.
- Verifying the AON fix, which requires a ROM build and is registered against Faz 7.2.

## 6. Current Repository Evidence

Three kernel checkouts are present at the workspace root: `android_kernel_qcom_sm8550/`, `android_kernel_xiaomi_sm8550/`, and `common_sm8550/`. Main-Planing section 3 records them as "present for reading only (Windows/NTFS cannot build them)".

`common_clone.log` and `kernel_clone.log` are present at the root. These are the records of how the existing checkouts were obtained, including presumably the sparse-checkout exclusions, and they are the best available evidence of the collision problem's specifics.

Main-Planing Phase 7 records the collision detail: fourteen case-collision paths and three DOS-reserved filenames excluded by sparse checkout. Autopsy section 3 records the checkouts as "three full kernel trees inside the workspace with known NTFS case-collisions, contributing most of the repository's byte size while being unbuildable on this host."

Faz 1.1's measurement will have produced real sizes for these trees, which is directly relevant to the space assessment: the same content cloned inside the Linux filesystem occupies comparable space, in addition to what the Windows copies already use.

`refs/a16_ishtar/` and `refs/a16_sm8550/` are the Android 16 device tree inputs per Autopsy section 3, and Faz 6.1 has added the symlink entry to at least the first. They are inputs to Faz 7.2 rather than to this sub-phase.

Project-Comprehension `EV-20` records "WSL2 is not installed and blocks the Android 16 track" as `probable`, evidence type user-confirmed. It is one of the few claims in that register resting on a statement rather than a measurement, which this sub-phase changes.

Main-Planing records disk as re-measured on 2026-08-23 at 953 GB total and 799 GB free on the Windows volume.

`platform-tools/` holds a vendored Windows `adb`. Whether device access is needed from inside the Linux environment is a question Faz 7.2 raises when a build output needs flashing; it is not needed for this sub-phase.

## 7. Planned Work Breakdown

- F7.1-01 — Record the distribution decision as open
  - Description: State the choice as an open decision with the AOSP build requirements as the deciding input, rather than picking one and discovering a mismatch during Faz 7.2.
  - Output: An open decision entry with its deciding criterion named.
- F7.1-02 — Install WSL2
  - Description: The user's action on the host. Record the version installed and whether virtualization support required any host configuration.
  - Output: A working Linux environment with its version recorded.
- F7.1-03 — Verify case sensitivity in the Linux filesystem
  - Description: Confirm directly that the Linux filesystem distinguishes case, which is the property the Windows volume lacks and the reason for the whole arrangement.
  - Output: A case-sensitivity confirmation.
- F7.1-04 — Assess virtual disk space behavior
  - Description: Determine how much space is available to the Linux filesystem and how its virtual disk grows, since the 799 GB figure describes the Windows volume rather than what the Linux environment can consume.
  - Output: A space assessment distinct from the earlier measurement.
- F7.1-05 — Install the kernel build toolchain
  - Description: Install the compiler, build tools, and dependencies a kernel configuration and build require.
  - Output: A toolchain with its component versions recorded.
- F7.1-06 — Clone a kernel source inside the Linux filesystem
  - Description: Clone fresh inside the Linux home directory rather than migrating from the Windows copies, and confirm no sparse-checkout exclusion is needed. The absence of that need is itself the proof the constraint is satisfied.
  - Output: A complete checkout with no exclusions.
- F7.1-07 — Run the smoke test
  - Description: Execute a trivial kernel configuration step and confirm it completes. This is Main-Planing's stated first slice.
  - Output: A completed configuration step.
- F7.1-08 — Record the provisioning procedure
  - Description: Write the steps as a re-runnable procedure, in the same form as Faz 1.4's toolchain record, including any host configuration that was required.
  - Output: A provisioning procedure.
- F7.1-09 — Update the environment evidence
  - Description: Change `EV-20` from a user-statement claim to a measured fact, and update Project-Ontology invariant 11's statement that WSL2 is not installed.
  - Output: Two updated records.

## 8. Acceptance Criteria

- WSL2 is installed and its version is recorded.
- The Linux filesystem is confirmed case-sensitive by direct test.
- A kernel source is cloned inside the Linux filesystem with no sparse-checkout exclusions required, and the absence of exclusions is recorded as evidence the constraint is satisfied.
- The clone is confirmed not to reside under the Windows mount.
- The trivial kernel configuration step completes successfully.
- The space assessment reports what the Linux environment can consume, distinct from the Windows volume figure.
- The provisioning procedure is written and includes any host configuration required.
- The distribution decision is recorded as open with its deciding criterion, or as settled with its reasoning.
- `EV-20` and Project-Ontology invariant 11 are updated to reflect the new environment state.

## 9. Validation and Test Approach

Validation is environment-level and hinges on one executable smoke test. The design principle is that an environment's existence proves nothing; a build action proves something.

- `VAL-ENV` (proposed) — WSL2 version reported, and the Linux filesystem confirmed case-sensitive by creating two paths differing only in case.
- `VAL-CLONE` (proposed) — a complete kernel checkout inside the Linux filesystem with no exclusions, and confirmation of its location relative to the Windows mount.
- `VAL-DEFCONFIG` (proposed) — the trivial kernel configuration step completing. This is the smoke test and the sub-phase's decisive signal.
- `VAL-DOCS` (proposed) — read back the provisioning procedure and confirm it covers every step actually performed, including host configuration.

Local versus live: entirely host-local. There is no device dimension in this sub-phase. Security validation is not applicable. Ontology validation applies to invariant 11, whose statement about WSL2 changes.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| docs/build-environment.md | proposed | The provisioning procedure produced by this sub-phase. | VAL-DOCS, VAL-ENV |
| kernel_clone.log | existing | Read-only record of how the Windows checkouts were obtained, including the exclusions. | VAL-CLONE |
| Planner-docs/Project-Ontology.md | modified | Invariant 11 updated once WSL2 is present. | VAL-ENV |
| Planner-docs/Project-Comprehension.md | modified | `EV-20` promoted from a user statement to a measured fact. | VAL-ENV |

## 10. Dependencies and Sequencing

Depends on Faz 1.1 for version control so the provisioning procedure is tracked, and benefits from Faz 1.4's toolchain record as a form to follow.

Depends on Main-Planing's sequencing judgment that the camera work should consolidate before this front opens. Phases 1 through 5 should be substantively complete.

Blocks Faz 7.2, Phase 8 entirely, and the AON verification registered by Faz 6.2.

Required decisions: the distribution, which is marked open with its criterion rather than resolved by planning.

Required infrastructure: host virtualization support, which may require configuration outside the operating system.

Required human actions: the installation itself, which is the user's action on their own machine. Main-Planing states this phase "depends on user action on the host machine", and that dependency is the phase's defining characteristic.

Fresh session token and context risk: medium. Provisioning produces long output, and the mitigation is to record verdicts and versions rather than transcripts.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: sources are placed under the Windows mount out of convenience. Impact: the case-collision problem recurs and the environment provides no benefit over the existing checkouts. Mitigation: F7.1-06 clones inside the Linux filesystem and the acceptance criteria require confirming the location, with the absence of sparse-checkout exclusions as positive evidence.
- Risk: the environment is provisioned and declared ready without a build action. Impact: a mismatch surfaces during Faz 7.2's ROM sync, when the cost of discovery is much higher. Mitigation: `VAL-DEFCONFIG` requires a real configuration step, which is Main-Planing's own stated slice.
- Risk (`R9`): host virtualization is unavailable or requires firmware changes the user is unwilling to make. Impact: Phases 7 and 8 are blocked indefinitely. Mitigation: this is a genuine external dependency rather than a planning gap; F7.1-02 records what host configuration was required so the obstacle is characterized rather than vague.
- Risk: the virtual disk fills during Faz 7.2's ROM sync because the space assessment measured the wrong thing. Impact: a failed sync after hours of work. Mitigation: F7.1-04 assesses the Linux environment's own capacity, explicitly distinct from the Windows volume figure.
- Risk: the distribution chosen is incompatible with the AOSP build requirements. Impact: rework at the start of Faz 7.2. Mitigation: F7.1-01 names the AOSP requirements as the deciding criterion rather than choosing on general preference.
- Risk: the provisioning steps are performed and not recorded. Impact: the environment becomes as fragile as the analysis toolchain was before Faz 1.4, which this project has already paid to reconstruct once. Mitigation: F7.1-08 is a work item and `VAL-DOCS` checks its completeness.
- Risk: the existing Windows kernel checkouts are migrated rather than re-cloned. Impact: the case collisions travel with them. Mitigation: the out-of-scope section states fresh clones as the approach and gives the reason.

## 12. Desired End State

A Linux build environment exists on the host, case-sensitive, with a kernel source cloned inside it requiring no exclusions, a toolchain installed, and a trivial kernel configuration step completing successfully. The space available to that environment is assessed on its own terms, the provisioning steps are recorded as a re-runnable procedure, and the two records asserting that WSL2 is absent are updated.

The evidence an implementer should produce is the environment version, the case-sensitivity test result, the exclusion-free clone with its location, the completed configuration step, and the space assessment.

The ledger summary Step 4 should append records: the environment and distribution installed, the toolchain versions, the smoke test result, the space available, and the updated evidence rows.

## 13. Next Sub-Phase Transition Criteria

- The Linux environment exists and is confirmed case-sensitive.
- A kernel source is cloned inside it with no exclusions, outside the Windows mount.
- The trivial configuration step completes.
- The space assessment covers the Linux environment specifically.
- The provisioning procedure is written and complete.
- `EV-20` and invariant 11 are updated.
- Faz 7.2 has an environment capable of attempting a ROM sync.
