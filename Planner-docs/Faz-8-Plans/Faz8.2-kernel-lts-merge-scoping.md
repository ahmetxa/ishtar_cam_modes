# Faz 8.2 — Kernel LTS Merge Scoping

## 1. Context

Main-Planing Phase 8 pairs two substantial pieces of work: "Port the device tree and the camera work to `beryl`, and merge GKI LTS into the kernel tree. Both are substantial and both depend on Phase 7." Its desired end state includes "the kernel tree is on a current LTS base" and its acceptance signal includes "kernel merge with no regressions in camera or sensor paths."

Main-Planing section 9 places this phase under "Do not expand yet", and Autopsy section 11 gates its decomposition on Phase 7 producing a working build environment. This sub-plan is therefore written at a scoping level: it establishes what the merge would involve and what it would risk, so that committing to it is an informed decision rather than an open-ended undertaking.

Three kernel checkouts sit in the workspace and none has been built. Main-Planing section 3 records them as "present for reading only (Windows/NTFS cannot build them)". Faz 7.1 removes that constraint, which is what makes this sub-phase possible at all.

The acceptance signal's second clause is the one that shapes this sub-plan. "No regressions in camera or sensor paths" is not a general stability requirement — it names the two subsystems this entire project modifies. A kernel merge that changes the camera driver behavior would interact with work the roadmap spent five phases on.

## 2. Goal

Establish what merging a current GKI LTS base into the kernel tree would involve and what it would risk for the camera and sensor paths, producing a scoped assessment that supports a commit-or-defer decision.

## 3. Description

The problem is that a kernel merge is easy to describe and hard to bound. The distance between the current base and a current LTS release is unknown, the conflict surface is unknown, and the effect on the camera path is unknown — and the camera path is where this project's value lives.

It belongs after Phase 7 because a merge that cannot be built cannot be evaluated, and after the camera consolidation because a kernel change during unresolved camera work would produce ambiguous attributions across two subsystems.

The vibecoding slice strategy is assessment before action. The first useful slice is establishing the distance: which base the tree is on, which LTS release is current, and how many changes separate them. The fastest useful signal is the conflict count in the camera and sensor subsystems specifically, because that number — rather than the total conflict count — is what determines whether this project's work survives the merge.

What should not be over-planned: the merge execution, conflict resolution strategy, or a schedule. Those follow the decision.

There is a specific technical concern worth naming, because the project has already met it. Project-Ontology invariant 3 records that the camera restart ordering matters because "killing the provider while a stream is live … leaves the QCOM kernel driver holding CSIPHY/CSID allocations". That is a kernel driver behavior the module works around in userspace. A kernel merge changes exactly that driver, and it could change the behavior the workaround depends on — in either direction. The assessment should identify whether the merge touches the CSIPHY and CSID allocation paths.

## 4. Scope

- Determination of which kernel base each of the three checkouts is on.
- Determination of which GKI LTS release is current and how far the base is from it.
- Identification of which checkout is the merge target, since three exist and their roles differ.
- An assessment of the conflict surface, separated into camera and sensor subsystems versus everything else.
- Specific identification of whether the merge touches the CSIPHY and CSID allocation paths that invariant 3 depends on.
- An assessment of whether the merge is a prerequisite for anything else in the roadmap or is independent value.
- A commit-or-defer recommendation routed to the user.
- Recording of the kernel base facts into Project-Ontology, which currently records the checkouts only as read-only reference.

## 5. Out of Scope

- Performing the merge or resolving any conflict.
- Building a kernel image, beyond what Faz 7.1's smoke test already established.
- Flashing a kernel to the device.
- Any beryl work, which is Faz 8.1.
- Any camera module, patch table, or device tree change.
- Upstreaming anything.
- Committing to a merge schedule.

## 6. Current Repository Evidence

Three kernel checkouts are present: `android_kernel_qcom_sm8550/`, `android_kernel_xiaomi_sm8550/`, and `common_sm8550/`. Main-Planing section 3 records all three as reference-only on this host. Their distinct roles are inferable from their names — a Qualcomm base, a Xiaomi device tree, and a common platform tree — but that inference has not been verified, which makes F8.2-03's target identification a real determination rather than a formality.

`kernel_clone.log` and `common_clone.log` are present at the workspace root and are the records of how these checkouts were obtained. They are the best available evidence of which branches and tags were fetched, and they should be the starting point rather than a fresh investigation of the trees themselves.

Autopsy section 3 records the checkouts as "three full kernel trees inside the workspace with known NTFS case-collisions, contributing most of the repository's byte size while being unbuildable on this host." Faz 1.1's measurement produced real sizes for them, and Faz 7.1 established whether fresh clones inside the Linux filesystem require the sparse-checkout exclusions the Windows copies needed.

Main-Planing Phase 7 records the collision detail: fourteen case-collision paths and three DOS-reserved filenames. Those exclusions matter here because a merge against a checkout missing three files would produce false conflicts or silent omissions — which is a direct argument for merging against a Linux-side clone rather than the Windows copies.

Project-Ontology invariant 3 records the CSIPHY and CSID allocation behavior in the QCOM camera kernel driver, discovered through a real defect and fixed in module version 1.6. Project-Comprehension `EV-12` records it as confirmed, evidenced by reproducing a black preview in every mode including stock when the order was reversed.

Project-Ontology invariant 10 records that the camera HAL patches are bound to one exact vendor build. A kernel merge does not change `camera.qcom.so`, which is a userspace vendor blob — so the HAL patches are not directly at risk. The sensor driver blob is likewise userspace. The risk is behavioral rather than binary: a changed kernel driver could alter how those userspace components behave without changing them.

Project-Comprehension `TRACE-04` maps the camera restart concept to `setmode.sh`'s `restart_camera()` and `wait_svc()`, with its tests column empty and its documentation given as "in-line comments (excellent)". The workaround is well documented and entirely unverified by any automated check — which by this point in the roadmap is no longer true, since Faz 2.1's smoke script and Faz 2.3's regression record exist and would detect a regression here.

## 7. Planned Work Breakdown

- F8.2-01 — Read the clone logs
  - Description: Extract the branch, tag, and revision information from `kernel_clone.log` and `common_clone.log` rather than investigating the trees directly. The logs are the cheapest source.
  - Output: A per-checkout base identification.
- F8.2-02 — Determine the current LTS target
  - Description: Establish which GKI LTS release is current for this kernel generation and how far the identified base is from it, expressed in a concrete measure rather than as a version gap.
  - Output: A distance assessment.
- F8.2-03 — Identify the merge target
  - Description: Determine which of the three checkouts is the merge target and what the other two are for. Verify the role inference rather than accepting it from naming.
  - Output: A verified role assignment for all three checkouts.
- F8.2-04 — Assess the conflict surface
  - Description: Estimate the conflict surface, separated into the camera and sensor subsystems versus everything else. The separation is the point: a large total with a clean camera path is a very different proposition from the reverse.
  - Output: A two-part conflict assessment.
- F8.2-05 — Check the CSIPHY and CSID allocation paths
  - Description: Determine specifically whether the merge touches the allocation behavior invariant 3 depends on. This is the single most consequential technical question in the sub-phase.
  - Output: A finding on the allocation paths.
- F8.2-06 — Assess independence
  - Description: Determine whether the merge is a prerequisite for anything else in the roadmap or delivers independent value. Nothing in Phases 1 through 7 requires it, which bears on its priority.
  - Output: A dependency and value assessment.
- F8.2-07 — Recommend and route
  - Description: Recommend commit or defer with reasoning, and route the decision to the user. A kernel merge is a scope expansion.
  - Output: A routed recommendation.
- F8.2-08 — Record the kernel facts
  - Description: Add the base identification and role assignment to Project-Ontology, which currently records the checkouts only as read-only reference with no version detail.
  - Output: An extended ontology entry.

## 8. Acceptance Criteria

- Each of the three checkouts has an identified base, sourced from the clone logs where possible.
- The current LTS target is named and the distance from the base is expressed concretely.
- The merge target is identified and all three checkout roles are verified rather than inferred from naming.
- The conflict assessment separates the camera and sensor subsystems from everything else.
- The CSIPHY and CSID allocation question has a specific finding, not a general statement about driver changes.
- The independence assessment states whether anything in the roadmap requires this merge.
- A recommendation exists and is routed to the user.
- Project-Ontology carries the base identification and role assignment.
- No merge was attempted and no conflict was resolved.
- The assessment is performed against a Linux-side clone rather than the Windows copies, or the limitation of using the Windows copies is stated.

## 9. Validation and Test Approach

Validation is static and assessment-level. This sub-phase produces a scoped estimate, so its validation is that the estimate rests on read evidence rather than on version-number reasoning.

- `VAL-LOGS` (proposed) — the base identification traced to the clone logs, with any checkout whose base could not be determined from them named explicitly.
- `VAL-SURFACE` (proposed) — the conflict assessment, checked for the required separation between camera and sensor subsystems and everything else.
- `VAL-INVARIANT` (proposed) — the CSIPHY and CSID finding, stated as a specific answer about those paths rather than a general observation.
- `VAL-DOCS` (proposed) — read back the role assignment, the independence assessment, and the recommendation.

Local versus live: entirely local. No device, no build beyond what Faz 7.1 established, no flash. Security validation is not applicable. Ontology validation applies to invariant 3, whose kernel-side dependency this sub-phase examines, and to the checkout role records.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| kernel_clone.log | existing | Primary source for the kernel checkout base identification. | VAL-LOGS |
| common_clone.log | existing | Primary source for the platform tree base identification. | VAL-LOGS |
| ishtar-cam-modes/setmode.sh | existing | Read-only context: the userspace workaround whose kernel dependency is being assessed. | VAL-INVARIANT |
| Planner-docs/Project-Ontology.md | modified | Record the kernel bases, the role assignment, and any invariant 3 implication. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 7.1 for a Linux environment capable of working with kernel sources, and benefits from Faz 7.2's outcome for context on whether the Android 16 track is viable.

Does not depend on Faz 8.1. The beryl port and the kernel merge are independent within Phase 8, and either could proceed without the other.

Blocks nothing in the current roadmap. F8.2-06 assesses this explicitly, and the likely finding is that the merge delivers independent value rather than unblocking anything — which is itself a relevant input to the priority decision.

Required decisions: the commit-or-defer recommendation, routed to the user.

Required infrastructure: the Linux environment from Faz 7.1 and network access to determine the current LTS target.

Required human approvals: the commit decision.

Fresh session token and context risk: medium. Kernel trees are large, and the mitigation is to work from the clone logs and targeted subsystem queries rather than broad tree exploration. The general caution in `R10` about scripted extraction over interactive exploration applies here as much as it does to binary analysis.

Subagents: Main-Planing section 9's exception covers the Phase 8 device-tree diff specifically, which is Faz 8.1's work. For this sub-phase the general advice against subagents applies.

## 11. Risks and Mitigations

- Risk (invariant 3): the merge changes the CSIPHY and CSID allocation behavior the camera restart workaround depends on. Impact: a documented, hard-won fix stops working, and the symptom — black preview in every mode — is severe and reboot-recoverable only. Mitigation: F8.2-05 makes this a specific finding rather than a general concern, and the regression surface from Faz 2.1 and Faz 2.3 now exists to detect it if the merge proceeds.
- Risk: the conflict surface is assessed in aggregate and the camera path's state is invisible. Impact: a merge is committed to on a total that hides the relevant detail. Mitigation: F8.2-04 requires the two-part separation and `VAL-SURFACE` checks for it.
- Risk: the assessment is performed against the Windows checkouts, which are missing three excluded files. Impact: false conflicts or silent omissions in the estimate. Mitigation: the acceptance criteria require either a Linux-side clone or an explicit statement of the limitation.
- Risk: the checkout roles are assumed from their names. Impact: the merge target is wrong and the whole assessment describes the wrong tree. Mitigation: F8.2-03 requires verification rather than inference.
- Risk: the merge is committed to because it is on the roadmap, without the independence question being asked. Impact: substantial work that unblocks nothing, at a point where Main-Planing's own conclusion is that the project should consolidate rather than widen. Mitigation: F8.2-06 makes independence an explicit assessment and F8.2-07 routes the decision.
- Risk: the sub-phase expands into exploratory merge work. Impact: scope creep into a phase the user has not committed to. Mitigation: the out-of-scope section forbids any merge attempt and the acceptance criteria require none was made.
- Risk: the base cannot be determined from the clone logs. Impact: a more expensive investigation than the sub-phase is scoped for. Mitigation: `VAL-LOGS` requires naming any checkout whose base could not be determined, which bounds the work rather than expanding it silently.

## 12. Desired End State

A scoped assessment exists for the kernel LTS merge: each checkout's base is identified from its clone log, the current LTS target and the distance to it are named, the merge target and all three checkout roles are verified, the conflict surface is separated into camera and sensor subsystems versus everything else, the CSIPHY and CSID allocation question has a specific finding, and the merge's independence from the rest of the roadmap is stated. A recommendation is routed to the user and the ontology carries the kernel facts.

The evidence an implementer should produce is the base identifications with their log sources, the distance assessment, the verified role assignment, the two-part conflict assessment, and the allocation path finding.

The ledger summary Step 4 should append records: the identified bases, the merge target, the conflict assessment, the allocation finding, the independence conclusion, and the routed recommendation.

## 13. Next Sub-Phase Transition Criteria

- All three checkouts have an identified base or are named as undetermined.
- The merge target and the three roles are verified rather than inferred.
- The conflict assessment carries the required separation.
- The CSIPHY and CSID question has a specific finding.
- The independence assessment states what, if anything, the merge unblocks.
- The recommendation is routed to the user.
- No merge was attempted, and the commit decision remains the user's.
