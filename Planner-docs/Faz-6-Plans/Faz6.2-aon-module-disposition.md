# Faz 6.2 — AON Module Disposition and Build Verification

## 1. Context

Main-Planing Phase 6's description sets the module's intended future: "Add the entry so future builds create the path natively, and keep the runtime module only as a fallback for already-built ROMs." Its acceptance signals require a build to confirm: "The entry is present in both trees; on a build that includes it, the NCS providers for aperture, OIS, laser AF, and face-scene appear without `ishtar-aon-fix` installed."

That second signal cannot be met until Phase 7 produces a build environment, which makes this sub-phase structurally unusual: it must decide the module's disposition now while its verification is deferred.

Main-Planing section 9 lists the disposition among the four decisions needing human confirmation: "Whether the AON module merges into `ishtar-cam-modes` or stays separate." Phase 9's description repeats it as part of release engineering: "a decision on whether the AON module merges into the main module."

Project-Comprehension `ARC-06` records the divergence Faz 6.1 half-closed: "The AON fix belongs in the device tree — Implemented as a runtime module; the tree still lacks the entry." With the entry added but unverified, the divergence is in an intermediate state that should be recorded accurately rather than optimistically.

Autopsy section 3 records a property that argues for keeping the module: it "explicitly documents itself as *not* depending on KernelSU module mounting, which is a deliberate resilience choice worth preserving."

## 2. Goal

Decide the AON module's role given the device tree change, and define the verification that will confirm or refute the fix once a build environment exists — so the decision is made now and the proof is scheduled rather than forgotten.

## 3. Description

The problem is a workaround whose replacement is written but unproven. Removing the module before the fix is verified would break already-working devices. Keeping it indefinitely without a plan means the workaround becomes permanent by inertia, which is how `ARC-06` arose in the first place.

It belongs at the end of Phase 6 because it consumes Faz 6.1's change, and its verification component belongs to Phase 7 by necessity rather than by choice.

The vibecoding slice strategy: decide the role first, because that decision does not depend on the build; then write the verification procedure, because writing it while the reasoning is fresh is cheaper than reconstructing it during Phase 7. The fastest validation signal for the decision is that it accounts for both the already-built-ROM case and the future-build case, which are genuinely different situations.

What should not be over-planned: merging the module into `ishtar-cam-modes` as an implementation. The merge question is a decision with a recorded answer; performing the merge is release work and belongs to Phase 9 if the decision goes that way.

Three roles are available and each has a real argument. Keeping the module separate preserves the KernelSU independence Autopsy identifies as deliberate, and keeps a device-tree-independent fallback for users on ROMs built before the fix. Merging it into `ishtar-cam-modes` reduces the number of artifacts a user installs and is what Phase 9's consolidation goal points toward. Retiring it once the fix is verified is the endpoint the main plan describes — "keep the runtime module only as a fallback" implies eventual retirement is not planned, but the fallback's scope narrows over time as ROMs are rebuilt.

The verification procedure is the sub-phase's other deliverable and is worth specifying now. Confirming the fix means showing that the four provider capabilities appear on a build that includes the entry, with the module absent. That is a specific check against a specific build, and it should be written as a Phase 7 acceptance item rather than left as a general intention.

## 4. Scope

- A decision among the three roles: keep separate, merge into `ishtar-cam-modes`, or plan for retirement after verification.
- The reasoning, accounting for the already-built-ROM case, the future-build case, and the KernelSU independence property.
- A written verification procedure for Phase 7: what to check, on which build, with the module absent, and what result confirms the fix.
- Registration of that procedure as a Phase 7 acceptance item, so it is scheduled rather than remembered.
- A statement of what happens if the build shows the entry did not work, including whether the module's role changes.
- Update of `ARC-06` to its accurate intermediate state.
- If the decision is to merge, the merge is scoped and routed to Phase 9 rather than performed here.

## 5. Out of Scope

- Performing a merge. Scoping and routing only.
- Removing or disabling the module. No removal happens before verification.
- Building anything. Phase 7 owns the build environment.
- Any further device tree change. Faz 6.1 made the change.
- Investigating the AON chain's behavior beyond what the verification procedure specifies.
- The long-run AON defect hunt Autopsy section 4 lists under planned-but-unevidenced work; it is unrelated to this fix.
- Release packaging changes, which are Phase 9 even if the merge decision affects them.

## 6. Current Repository Evidence

`ishtar-aon-fix/` contains three files: `customize.sh`, `module.prop`, and `post-fs-data.sh`. It is packaged as `ishtar-aon-fix-v1.1.zip` at the workspace root.

Main-Planing section 3 records its function: it "creates the missing `/vendor/lib64/camera/aon_front.pb` path, repairing the AON → CSS → NCS chain (aperture, OIS, laser AF, face-scene providers). Packaged as `ishtar-aon-fix-v1.1.zip`. Explicitly independent of KernelSU module mounting."

Autopsy section 3 assesses its maturity as medium-high and identifies the boundary issue: "it is a workaround for a device-tree defect (the missing `;SYMLINK=` entry), so its correct long-term home is `device_ishtar/`, not a runtime module. Ownership is currently in the wrong layer by necessity, not by design."

Project-Ontology section 4 records the module's dependency line as "**Not** KernelSU module mounting — deliberate", and Project-Comprehension `TRACE-13` maps the AON repair to `ishtar-aon-fix/post-fs-data.sh` with its tests column empty and its documentation given as "memory + module description".

That empty tests column is worth noting: the module works, and nothing verifies that it works. The verification procedure this sub-phase writes is the first check the AON capability has ever had, and it is worth writing so that it can also verify the module itself, not only the device tree fix.

Main-Planing Phase 7 states that WSL2 is not installed and that neither the kernel nor AOSP builds on Windows or NTFS. Project-Comprehension `EV-20` records this as `probable`, from a user statement. This is the blocker that defers verification.

`refs/a16_ishtar/` and `refs/a16_sm8550/` are present as Android 16 build inputs, per Autopsy section 3, and Faz 6.1 has added the entry to at least the first of them.

## 7. Planned Work Breakdown

- F6.2-01 — Enumerate the affected populations
  - Description: Distinguish the already-built-ROM case, where the module remains the only fix, from the future-build case, where the device tree entry should suffice. The two populations coexist for as long as anyone runs an older build.
  - Output: A population analysis informing the role decision.
- F6.2-02 — Evaluate the three roles
  - Description: Assess keep-separate, merge, and plan-for-retirement against the population analysis, the KernelSU independence property, and Phase 9's consolidation goal.
  - Output: A three-option evaluation with a recommendation.
- F6.2-03 — Record the decision
  - Description: Make the disposition decision. Main-Planing lists this among the decisions needing human confirmation, so the implementer recommends and the user chooses.
  - Output: A recorded decision routed to the user.
- F6.2-04 — Write the verification procedure
  - Description: Specify what confirms the fix: which build, which providers checked, with the module absent, and what result is conclusive. Write it while the reasoning is current.
  - Output: A verification procedure specification.
- F6.2-05 — Register the procedure as a Phase 7 acceptance item
  - Description: Add the verification to Phase 7's expectations so it is scheduled rather than remembered, and reference it from Faz 7.2.
  - Output: A registered Phase 7 item.
- F6.2-06 — Specify the negative-result response
  - Description: State what happens if the build shows the entry did not work — whether the entry is corrected, the module's role changes, or both.
  - Output: A contingency statement.
- F6.2-07 — Extend the procedure to cover the module itself
  - Description: Since `TRACE-13` shows the module has never been verified either, write the check so it can validate the module's own effect as well as the device tree fix.
  - Output: A procedure covering both mechanisms.
- F6.2-08 — Update the architectural record
  - Description: Update `ARC-06` to its accurate intermediate state: the entry exists, its effect is unverified, and the module remains in place pending confirmation.
  - Output: An updated architecture row.

## 8. Acceptance Criteria

- The population analysis distinguishes already-built ROMs from future builds and states how long both persist.
- All three roles are evaluated with reasoning, not just the recommended one.
- The disposition decision is recorded and routed to the user, since Main-Planing names it as needing human confirmation.
- The verification procedure names the specific providers to check and states what result is conclusive.
- The procedure is registered as a Phase 7 acceptance item and referenced from Faz 7.2.
- The negative-result response is specified before the build exists.
- The procedure covers the module's own effect as well as the device tree fix.
- `ARC-06` reflects the intermediate state accurately, neither claiming resolution nor ignoring the change.
- No merge was performed and no module was removed.

## 9. Validation and Test Approach

This sub-phase produces decisions and a deferred procedure, so its validation is completeness and traceability rather than measurement. That is an honest description of what it can achieve without a build environment.

- `VAL-DOCS` (proposed) — read back the population analysis, the three-option evaluation, the decision, the verification procedure, and the contingency statement; confirm each is specific enough to act on.
- `VAL-REGISTER` (proposed) — confirm the verification procedure appears as a Phase 7 acceptance item and is referenced from Faz 7.2, so registration is verified rather than assumed.
- `VAL-BUILD` (deferred, Phase 7) — the actual verification: the four providers present on a build including the entry, with the module absent. Named here, executed in Phase 7.

Local versus live: entirely local. The live and build dimensions are deferred, and this sub-phase's contribution is to make that deferral explicit and scheduled rather than open-ended.

Security validation is not applicable. Ontology validation applies to `ARC-06` and to the AON chain vocabulary.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-aon-fix/post-fs-data.sh | existing | The working mechanism the verification procedure must also be able to validate. | VAL-DOCS |
| ishtar-aon-fix/module.prop | existing | Read-only context for the module's declared independence from module mounting. | VAL-DOCS |
| docs/aon-verification.md | proposed | The verification procedure and the contingency statement. | VAL-DOCS, VAL-REGISTER |
| Planner-docs/Project-Comprehension.md | modified | Update `ARC-06` to its accurate intermediate state. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 6.1 for the device tree entry, without which there is nothing to decide about.

Feeds Phase 7 with a registered acceptance item, and feeds Phase 9 if the merge decision goes that way.

Does not depend on Phases 2 through 5 and, like Faz 6.1, can run out of numbered order.

Required decisions: the disposition, routed to the user per Main-Planing section 9.

Required credentials, infrastructure, or live endpoints: none.

Required human approvals: the disposition decision.

Fresh session token and context risk: low. This is analysis and specification over a three-file module.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the module is removed or merged before verification. Impact: users on already-built ROMs lose four camera capabilities with no fallback. Mitigation: the out-of-scope section forbids removal before verification, and F6.2-01 makes the affected population explicit.
- Risk: the verification procedure is deferred without being registered, and Phase 7 does not run it. Impact: the fix stays unverified indefinitely and `ARC-06` never resolves — the same inertia that created the divergence. Mitigation: F6.2-05 registers it as a Phase 7 acceptance item and `VAL-REGISTER` confirms the registration exists.
- Risk (`AUTOPSY-P1-04` residual): the entry turns out not to work and there is no plan for that case. Impact: an unproductive discovery during Phase 7, when attention is on the build itself. Mitigation: F6.2-06 specifies the response before the build exists.
- Risk: the merge decision is made on tidiness grounds and discards the KernelSU independence. Impact: a deliberate resilience property is lost as a side effect of consolidation. Mitigation: F6.2-02 evaluates that property explicitly, and Autopsy records it as deliberate rather than incidental.
- Risk: `ARC-06` is marked convergent because the entry now exists. Impact: an unverified edit is recorded as an architectural fix. Mitigation: F6.2-08 requires the intermediate state, and Faz 6.1's unverified status note travels here.
- Risk (`TRACE-13`): the verification procedure covers only the device tree fix, leaving the module itself as the one mechanism nothing checks. Impact: a capability with no verification at all, which is where it started. Mitigation: F6.2-07 extends the procedure to both.
- Risk: the decision is recorded but the user never confirms it. Impact: Phase 9 plans release contents against an unconfirmed assumption. Mitigation: the routing is explicit and the decision is one of the four Main-Planing already flagged for confirmation.

## 12. Desired End State

The AON module has a decided role, recorded with reasoning that accounts for both user populations and the module's deliberate independence property. A verification procedure exists that can confirm the device tree fix and the module's own effect, registered as a Phase 7 acceptance item with a specified response if it fails. `ARC-06` records the intermediate state accurately, and no module has been removed or merged on the strength of an unverified edit.

The evidence an implementer should produce is the population analysis, the three-option evaluation, the recorded decision, the verification procedure, and the registration confirmation.

The ledger summary Step 4 should append records: the disposition decided, where the verification is registered, the contingency specified, and the accurate `ARC-06` state.

## 13. Next Sub-Phase Transition Criteria

- The disposition decision is recorded and routed to the user.
- The verification procedure names specific providers and a conclusive result.
- The procedure is registered as a Phase 7 acceptance item and referenced from Faz 7.2.
- The negative-result response is specified.
- The procedure covers the module as well as the device tree fix.
- `ARC-06` reflects the intermediate state without overstating it.
- No removal or merge has occurred, and Phase 6 is complete pending Phase 7's verification.
