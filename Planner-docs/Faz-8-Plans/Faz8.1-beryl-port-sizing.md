# Faz 8.1 — Beryl Port Sizing

## 1. Context

Main-Planing Phase 8's first vibecoding slice is a sizing exercise rather than a port: "Diff `device_ishtar` against the `beryl` reference tree to size the port before committing to it."

That framing is deliberate and this sub-plan follows it exactly. Autopsy section 11 states why: "Phase 8 (beryl) has no beryl-specific evidence in the tree at all and should not be decomposed until Phase 7 produces a working build environment."

Main-Planing section 9 reinforces the low-detail instruction: "Do not expand yet. Phases 7, 8, and 9 … H depends on G."

Project-Ontology section 2 records what is known about the target, which is very little: "`beryl` — A second Xiaomi device targeted for a future port. No device-specific files exist yet."

This sub-phase therefore produces a decision input rather than a port. Its output is an honest estimate of what the port would cost, made against real trees rather than intuition, so that committing to Phase 8 is an informed choice.

## 2. Goal

Produce an evidence-based estimate of what porting the device tree and the camera work to `beryl` would cost, so the decision to commit to the port is made against a measured scope rather than an assumption.

## 3. Description

The problem is that a second device is easy to underestimate. The camera work in this project is bound to one exact sensor, one exact HAL binary, and one exact set of byte offsets. Whether any of it transfers depends on facts nobody has checked, because no beryl-specific file exists in the workspace.

It belongs after Phase 7 because a port needs a build environment to be meaningful, and because Phase 7's outcome determines whether a second device is even reachable.

The vibecoding slice strategy is a single diff and an inventory. The fastest useful signal is whether `beryl` uses the same sensor — if it does not, the entire camera layer is new work rather than a port, and that answer alone may settle the decision.

What should not be over-planned: the port itself, its phases, or its schedule. Those follow the decision this sub-phase informs.

The estimate needs to separate three distinct bodies of work, because they have very different transferability. The device tree is configuration and may diff cleanly. The sensor layer depends on which sensor `beryl` carries and on whether the blob format matches — the tooling in `ishtar-cam-modes/tools/` reads a specific container format and a 23-entry mode table, and a different sensor means a different table. The HAL layer depends on whether the same vendor binary is present, and Project-Ontology invariant 10 makes that dependency absolute: every offset is bound to one exact build.

That third point deserves emphasis in the estimate. A different `camera.qcom.so` invalidates all twenty patch sites, and re-deriving them means repeating the disassembly work Phase 3 and Phase 4 consumed. The estimate should say so plainly rather than treating the HAL layer as portable.

## 4. Scope

- Acquisition of a `beryl` device tree reference, since none is in the workspace.
- A structural diff of `device_ishtar` against that tree, categorized by what differs.
- Determination of `beryl`'s main sensor and whether it matches the IMX989.
- Determination of whether `beryl` uses the same camera HAL binary, by build identity rather than by name.
- A three-part cost estimate covering the device tree, the sensor layer, and the HAL layer separately.
- An explicit statement of what would need re-derivation rather than porting, particularly the patch offsets.
- A recommendation on whether to commit to the port, routed to the user as a decision.
- Recording of `beryl` facts into Project-Ontology section 2, which currently has one line about it.

## 5. Out of Scope

- Performing any port. This sub-phase estimates.
- Building for `beryl` or acquiring a `beryl` device.
- The kernel LTS merge, which is Faz 8.2.
- Any change to the `ishtar` device tree, camera modules, or patch tables.
- Deriving any `beryl` patch offsets.
- Committing to a schedule for the port.
- Testing anything on hardware the project does not have.

## 6. Current Repository Evidence

No beryl-specific file exists anywhere in the workspace. This was established in Step 1.5 and remains true: Autopsy section 4 lists "`beryl` port (no beryl-specific files present)" under planned-but-unevidenced work, and Project-Ontology section 2 records "No device-specific files exist yet."

`refs/` holds five trees — `a16_ishtar`, `a16_sm8550`, `los_ishtar`, `los_sm8550`, and `neo_ishtar` — all for `ishtar` or its platform. None is a beryl reference, which means F8.1-01's acquisition step is a genuine prerequisite rather than a formality.

`device_ishtar/` is the diff baseline, carrying `Android.bp`, `Android.mk`, `BoardConfig.mk`, `device.mk`, `proprietary-files.txt`, and a `README.md`.

`common_sm8550/` is the shared platform tree. If `beryl` is also an SM8550 device, the platform layer may transfer entirely, which would be the single largest simplification available — and it is a fact to check rather than assume.

Project-Ontology section 2 records `ishtar` as "Xiaomi 13 Ultra, SM8550 (Snapdragon 8 Gen 2), released April 2023" and IMX989 as the "Sony 1-inch main sensor. Physical pixel array 8192x6144 (50.3 MP)."

`ishtar-cam-modes/tools/verify_ln.py` was read in this run and confirms how specific the sensor tooling is: it asserts a `QTI Chromatix Header` signature, reads a mode table at a fixed offset with 60-byte entries, and tracks five specific register addresses. Project-Ontology section 3 records the blob as exactly 1,062,250 bytes with a 23-entry mode table. A different sensor means different values throughout.

`ishtar-cam-modes/halpatch.sh` records `HAL_SIZE=27268688` and `HAL_STOCK_MD5=c3fa63a86ee3ecaf9fbf02005d35f6b5`. Project-Ontology invariant 10 states the binding consequence directly.

Project-Ontology section 6 records the twenty patch sites across two tables, all inside `InitializeScalerStaticCaps` at `0x16bf4c0` through `0x16c5a90`. These addresses are the concrete measure of what a different binary would cost.

## 7. Planned Work Breakdown

- F8.1-01 — Acquire a beryl device tree reference
  - Description: Obtain a device tree for `beryl` from the same upstream sources the existing `refs/` trees came from, and place it alongside them under the naming convention Faz 1.6's index established.
  - Output: A beryl reference tree in the workspace.
- F8.1-02 — Establish the platform relationship
  - Description: Determine whether `beryl` is an SM8550 device sharing `common_sm8550`. If it is, the platform layer transfers; if not, the port is substantially larger.
  - Output: A platform relationship finding.
- F8.1-03 — Diff the device trees structurally
  - Description: Compare `device_ishtar` against the beryl reference, categorizing differences by file and by kind — configuration values, proprietary file lists, board settings.
  - Output: A categorized diff summary.
- F8.1-04 — Determine the sensor
  - Description: Establish which main sensor `beryl` carries and whether the blob format, size, and mode table structure match what the tooling expects.
  - Output: A sensor finding with the tooling implications stated.
- F8.1-05 — Determine the HAL binary identity
  - Description: Establish whether `beryl` ships the same `camera.qcom.so` build, by size and checksum rather than by filename. Invariant 10 makes this a binary question with no partial answer.
  - Output: A HAL identity finding.
- F8.1-06 — Produce the three-part estimate
  - Description: Estimate the device tree, sensor layer, and HAL layer separately, stating for each whether the work is a port, an adaptation, or a re-derivation.
  - Output: A three-part cost estimate.
- F8.1-07 — State the re-derivation cost explicitly
  - Description: If the HAL binary differs, state that all twenty patch sites require re-derivation and reference what that cost was on `ishtar` — the disassembly work Phases 3 and 4 consumed.
  - Output: A re-derivation cost statement grounded in the project's own history.
- F8.1-08 — Recommend and route the decision
  - Description: Recommend commit or defer, and route the decision to the user. A port to a second device is a scope expansion and belongs to them.
  - Output: A routed recommendation.
- F8.1-09 — Record beryl facts in the ontology
  - Description: Extend Project-Ontology section 2's one-line beryl entry with what this sub-phase established.
  - Output: An extended ontology entry.

## 8. Acceptance Criteria

- A beryl device tree reference exists in the workspace under the established naming convention.
- The platform relationship is determined, not assumed from the device name.
- The device tree diff is categorized by file and kind rather than presented as a raw comparison.
- The sensor is identified and the tooling implications are stated concretely, referencing the format assumptions in `verify_ln.py`.
- The HAL binary identity is determined by size and checksum, not by filename.
- The estimate separates the three layers and labels each as port, adaptation, or re-derivation.
- If the HAL differs, the re-derivation cost is stated with reference to what the equivalent work cost on `ishtar`.
- A recommendation exists and is routed to the user as a decision.
- Project-Ontology section 2's beryl entry carries the established facts.
- No port work was performed.

## 9. Validation and Test Approach

Validation is entirely static and comparative. This sub-phase produces an estimate, so its validation is that the estimate rests on measured facts rather than on inference from device names.

- `VAL-DIFF` (proposed) — the categorized device tree comparison, with the categorization checked for completeness against the file list.
- `VAL-IDENTITY` (proposed) — the sensor and HAL determinations, each made by a concrete identifier rather than by name. This is the check that keeps the estimate honest.
- `VAL-DOCS` (proposed) — read back the three-part estimate and confirm each part is labelled port, adaptation, or re-derivation, with a stated basis.

Local versus live: entirely local, with no device involvement at all — the project does not have a `beryl` device. Security validation is not applicable. Ontology validation applies to section 2's beryl entry and to keeping the sensor, HAL, and application layer vocabulary consistent when describing what transfers.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| device_ishtar | existing | The diff baseline for the device tree comparison. | VAL-DIFF |
| refs/beryl_reference | proposed | The acquired beryl device tree reference. | VAL-DIFF, VAL-IDENTITY |
| ishtar-cam-modes/tools/verify_ln.py | existing | Read-only evidence of how sensor-specific the blob tooling is. | VAL-IDENTITY |
| ishtar-cam-modes/halpatch.sh | existing | Source of the HAL size and checksum the identity check compares against. | VAL-IDENTITY |
| Planner-docs/Project-Ontology.md | modified | Extend the beryl entry with the established facts. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 7.2's readiness statement. Autopsy gates Phase 8's decomposition on Phase 7 producing a working build environment, and this sub-plan is written at low detail precisely because that gate has not been passed.

Benefits from Faz 1.6's reference index for the naming convention the acquired tree should follow.

Blocks any actual port work, which is not planned here and would need its own decomposition after the decision.

Does not block Faz 8.2, which addresses the kernel merge and is independent of the beryl question.

Required decisions: the commit-or-defer recommendation is routed to the user.

Required infrastructure: network access to obtain the reference tree. No device.

Required human approvals: the commit decision.

Fresh session token and context risk: low for the sizing itself. Main-Planing bands Phase 8 as high, but that banding describes the port, not the estimate.

Subagents: Main-Planing section 9 makes one specific exception to its general advice against subagents — "Consider a bounded read-only explorer only for the Phase 8 device-tree diff." That exception applies to F8.1-03 and is the only place in this roadmap where a subagent is recommended.

## 11. Risks and Mitigations

- Risk: the estimate assumes camera work transfers because both devices are Xiaomi. Impact: a port is committed to on a false premise and the true cost surfaces after commitment. Mitigation: F8.1-04 and F8.1-05 determine sensor and HAL identity by concrete identifiers, and `VAL-IDENTITY` requires it.
- Risk (invariant 10): the HAL binary differs and the re-derivation cost is understated. Impact: the port's largest cost is invisible in the estimate. Mitigation: F8.1-07 requires the cost to be stated with reference to what the same work cost on `ishtar`, which the project has direct experience of.
- Risk: no beryl reference tree can be obtained. Impact: the sizing cannot be done and the phase stalls at its first step. Mitigation: this is a genuine external dependency; if it cannot be satisfied, that is itself the finding and the recommendation becomes defer.
- Risk: the sizing expands into exploratory port work because the diff is interesting. Impact: scope creep into a phase the user has not committed to. Mitigation: the out-of-scope section forbids any port work and the acceptance criteria require none was performed.
- Risk: the platform relationship is assumed from the device generation. Impact: the largest available simplification is either wrongly claimed or wrongly dismissed. Mitigation: F8.1-02 determines it rather than inferring it.
- Risk: the recommendation is made without routing, and the port begins by momentum. Impact: a scope expansion happens without the user deciding it. Mitigation: F8.1-08 routes the decision explicitly.
- Risk: the sub-phase runs before Phase 7 succeeds. Impact: an estimate for work that cannot be built, contrary to Autopsy's gate. Mitigation: the dependency on Faz 7.2's readiness statement is stated as the governing precondition.

## 12. Desired End State

An evidence-based estimate exists for the beryl port, resting on an acquired reference tree, a determined platform relationship, an identified sensor, and a HAL binary identity established by checksum. The estimate separates the device tree, sensor, and HAL layers and labels each as port, adaptation, or re-derivation, with the re-derivation cost stated against the project's own experience. A recommendation is routed to the user, and the ontology's beryl entry carries what was learned.

The evidence an implementer should produce is the acquired tree, the categorized diff, the two identity determinations, and the three-part estimate.

The ledger summary Step 4 should append records: the platform relationship, the sensor and HAL findings, the three-part estimate, and the routed recommendation.

## 13. Next Sub-Phase Transition Criteria

- A beryl reference tree exists in the workspace.
- The platform relationship, sensor, and HAL identity are all determined by concrete identifiers.
- The estimate separates three layers with a label and basis for each.
- The re-derivation cost is stated if the HAL differs.
- The recommendation is routed to the user.
- No port work has been performed, and the commit decision remains the user's.
