# Faz 3.1 — Preference Trap Clearance and Phase Preconditions

## 1. Context

Main-Planing Phase 3 carries an explicit warning inside its description: "A known trap must be respected — leftover `pref_raw_key_N` / `pref_fix_resolution_key_N` preferences independently break Gcam initialization by triggering the port's `getFixResolutionList` width-cap, and have already caused one misattributed failure."

Autopsy escalates it from a warning to a structural requirement. Section 12 under Phase 3: "Add a precondition check for leftover `pref_raw_key_N` / `pref_fix_resolution_key_N` to every sub-plan in this phase." Section 11 lists it third among risks Step 2 must not ignore: "the `pref_raw_key` / `pref_fix_resolution_key` trap is a known landmine that has already cost one debugging cycle and must appear as a precondition check in every Phase 3 sub-plan, not as a footnote."

Project-Ontology records it as invariant 8, ending with an instruction in emphasis: "Check for and clear these before diagnosing anything else." Project-Comprehension records it as `EV-13`, confidence `confirmed`, with the isolation run described: "reverting the HAL then the APK did not fix it · deleting the prefs did."

This Step 2 run added a finding the earlier artifacts do not contain. Both `.agc` configuration files at the workspace root — `12mpx_agc_config.agc` and `50mpx_agc_config.agc` — contain the full key families: `pref_raw_key`, `pref_raw_key_0` through `pref_raw_key_4`, `pref_fix_resolution_key`, and `pref_fix_resolution_key_0` through `pref_fix_resolution_key_4`. The trap is not merely a residue of past experimentation; it is carried by the configuration files the workflow normally imports. Importing either configuration re-arms it.

## 2. Goal

Establish and verify the entry preconditions for the whole of Phase 3 — a clean preference state, a known device baseline, working disassembly capability, and an agreed attempt budget — so that every measurement in the phase attributes its result to the change under test rather than to a pre-existing condition.

## 3. Description

The problem this solves is misattribution, which has already cost this project a documented three-step debugging cycle. Phase 3 is a sequence of single-variable experiments against a closed binary, and a single-variable experiment is only valid if everything else is known and held.

It belongs first in Phase 3 because every later sub-plan in the phase depends on it, and because the cost of establishing it once is far below the cost of discovering mid-phase that a measurement was invalid.

The vibecoding slice strategy: the first useful slice is a preference audit and clearance procedure, which is cheap and closes the highest-cost failure mode. The second is confirming the other preconditions are satisfied — the baseline snapshot from Faz 2.2, the disassembler self-check from Faz 1.4, and version control from Faz 1.1. The fastest validation signal is the Faz 2.1 smoke script's preference field reporting nothing set.

What should not be over-planned: a general preference management scheme for the AGC port. The requirement is narrower — know which keys are set, be able to clear them, and confirm the clearance held.

The attempt budget is the other half of this sub-phase and is equally load-bearing. Autopsy `AUTOPSY-P1-03` states the problem: "Phase 3 has no stop condition … locating a write site in a 27 MB stripped binary is open-ended; without a bound, the token budget and the session both run out before a decision is reached." Section 11 requires Step 2 to give Phase 3 "an explicit bound: a number of located-address attempts, or a fallback decision point where the app-level patch is accepted as the answer." That bound is set here, before the search starts, because a bound agreed after a search has begun is not a bound.

A note on the phase's shape. Main-Planing describes Phase 3's risk honestly: "If `pixelArraySize` cannot be moved safely, the fallback is to raise the active array instead — but Faz 4 already showed that direction breaks AGC when raw is not raised with it. Both sides of the invariant must move together." This sub-phase records that both directions of the invariant are in play, so the search in Faz 3.2 is understood as targeting one of two viable sides rather than the only possible one.

## 4. Scope

- An audit procedure that reports which preference keys are currently set for the AGC package, by key name.
- A clearance procedure that removes the two key families and a verification that the clearance held across an application restart.
- A statement that both root-level configuration files carry these key families, so importing either re-arms the trap, with that fact recorded where an operator will see it before importing.
- Confirmation of the four Phase 3 entry preconditions: version control exists, the disassembly self-check passed, the baseline snapshot exists and is named, and the regression record exists.
- The attempt budget for Faz 3.2's write-site search, expressed as a bounded quantity agreed in advance.
- The fallback options enumerated, so the decision gate in Faz 3.6 has its choices defined rather than improvised.
- A per-measurement checklist that every later Phase 3 sub-plan applies before recording any result.

## 5. Out of Scope

- Any disassembly or address search. That is Faz 3.2.
- Any HAL modification. That is Faz 3.3.
- Any capture attempt. That is Faz 3.5.
- Redesigning or repackaging the AGC port, or changing its preference handling.
- Deciding the fallback. This sub-phase enumerates the options; Faz 3.6 chooses among them if the primary path fails.
- Modifying either `.agc` configuration file. They are described, and the warning is recorded; editing them is a separate question with its own consequences.
- Any change to the four functional tiles or to the sensor layer.

## 6. Current Repository Evidence

Both root-level configuration files were inspected by key name in this run. `12mpx_agc_config.agc` and `50mpx_agc_config.agc` each contain `pref_raw_key`, `pref_raw_key_0`, `pref_raw_key_1`, `pref_raw_key_2`, `pref_raw_key_3`, `pref_raw_key_4`, `pref_fix_resolution_key`, `pref_fix_resolution_key_0`, `pref_fix_resolution_key_1`, `pref_fix_resolution_key_2`, `pref_fix_resolution_key_3`, and `pref_fix_resolution_key_4`. This is a new finding from this Step 2 run and is not recorded in the Step 1 or Step 1.5 artifacts.

Project-Ontology section 6 records the mechanism under "Channel selection": `LensSettings.getImageFormatArr()` returns `[pref_raw_key_<lens>]` if that key is set, and otherwise returns the default format order `[0x25 RAW10, 0x26 RAW12, 0x20 RAW_SENSOR, 0x23 YUV]`. `AGC.getImageReaderFormat()` then takes the first format with a non-empty size list and `Lmip;->bs()` takes its maximum size. A set `pref_raw_key_N` therefore replaces the entire format preference order with a single value.

Project-Ontology invariant 8 records the second mechanism: `pref_fix_resolution_key_N` triggers the port's `getFixResolutionList` width-cap, "which can shrink a sensor's RAW list to an odd size".

Project-Ontology section 6 also records the target for the phase: tag `f0006` for `android.sensor.info.pixelArraySize`, with nine `movz` and `movk` references at `0x004fe984`, `0x004fee94`, `0x004ffa5c`, `0x00d9ae24`, `0x00d9ae80`, `0x013b192c`, `0x013b1994`, `0x013b1a08`, and `0x013b1a7c`, plus six rodata dwords at `0x0002c6ac`, `0x0038964c`, `0x003969b4`, `0x00396adc`, `0x00397fcc`, and `0x0039c1f0`. The write site is explicitly not located.

`agc-50mp-yama/hal-raw50-deneme.patch` was read in this run and records the exact rejection: `libgcam static_metadata.cc:667`, `frame_raw_max (8192x6144) matches neither the active area size (4096x3072) nor pixel array size (4096x3072)`. Both arrays currently report the same value, which is why either side of the invariant is a candidate.

The patch header also records that the experimental patch is currently reverted on the device, alongside the APK patch. Autopsy section 4 states both are measured and both are reverted, so the device baseline should show neither applied.

## 7. Planned Work Breakdown

- F3.1-01 — Audit the current preference state
  - Description: Report which of the ten trap keys, if any, are currently set for the AGC package. Report by key name; values are not needed for the decision and printing them adds nothing.
  - Output: A preference audit result.
- F3.1-02 — Define and execute the clearance procedure
  - Description: Write the procedure that removes both key families, execute it, and verify the clearance survives an application restart. Verification matters because a preference written back on startup would defeat a one-shot clearance.
  - Output: A clearance procedure plus a post-restart verification result.
- F3.1-03 — Record the configuration-file finding where it will be seen
  - Description: Record that both root configuration files carry the trap key families, and place that warning in the artifact manifest from Faz 1.6 and in the per-measurement checklist, not only in a planning document.
  - Output: A warning recorded in at least two operator-facing locations.
- F3.1-04 — Confirm the four entry preconditions
  - Description: Verify version control exists and the tree is clean, the Faz 1.4 disassembly self-check passed against the four known `cmp` sites, the Faz 2.2 baseline snapshot exists and is named, and the Faz 2.3 regression record exists with no unrouted failures.
  - Output: A four-item precondition verdict.
- F3.1-05 — Set the attempt budget for the write-site search
  - Description: Agree a bounded quantity for Faz 3.2 before the search begins — expressed in terms of candidate sites examined or sessions spent, whichever the implementer and user prefer. Record it as a number, not as an intention.
  - Output: A written budget with the unit stated.
- F3.1-06 — Enumerate the fallback options
  - Description: List the alternatives available if the write-site search does not succeed within budget: accept the application-level patch as the answer; move the active array instead, with the Faz 4 evidence about that direction attached; or defer the phase. Each option gets its known cost and known risk.
  - Output: A fallback option set consumed by Faz 3.6.
- F3.1-07 — Write the per-measurement checklist
  - Description: The short list every later Phase 3 sub-plan runs before recording a result: preferences clear, smoke snapshot taken, single variable changed, previous state restorable. This is what makes each measurement attributable.
  - Output: A checklist referenced by Faz 3.2 through Faz 3.5.

## 8. Acceptance Criteria

- The preference audit reports each of the ten trap keys as set or unset by name.
- After clearance, a subsequent audit reports all ten unset, and the result holds across an application restart.
- The Faz 2.1 smoke script's preference field agrees with the audit, confirming the two independent views match.
- The configuration-file warning appears in at least two operator-facing locations, one of which is the artifact manifest.
- All four entry preconditions have an explicit pass verdict; a phase that starts with a failed precondition is a finding, not a proceed.
- The attempt budget is recorded as a number with its unit before Faz 3.2 begins.
- The fallback option set enumerates at least the three options named in F3.1-06, each with cost and risk.
- The per-measurement checklist exists and is referenced by name from the later Phase 3 sub-plans.
- The device baseline confirms neither the experimental HAL patch nor the patched APK is currently applied, matching the reverted state Autopsy records.

## 9. Validation and Test Approach

Validation combines a live device check with document verification. The distinguishing property is that this sub-phase validates readiness rather than a change.

- `VAL-PREFS` (proposed) — the preference audit, run before clearance, after clearance, and after an application restart. Three runs, because a clearance that does not survive a restart is not a clearance.
- `VAL-SMOKE` (from Faz 2.1) — an independent confirmation of the preference state through the smoke script's preference field, plus confirmation that the HAL is in its stock or fullres state rather than the experimental one.
- `VAL-PRECOND` (proposed) — the four-item precondition check, each item verified against its producing sub-phase's evidence rather than assumed from its existence.
- `VAL-DOCS` (proposed) — read back the budget, the fallback options, the checklist, and both warning placements.

Local versus live: the precondition confirmations are local; the preference audit and clearance are live. Security validation is not applicable, though the audit deliberately reports key names rather than values.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Independent view of preference state and HAL classification. | VAL-SMOKE |
| 50mpx_agc_config.agc | existing | Carries the trap key families; described and warned about, not modified. | VAL-DOCS |
| 12mpx_agc_config.agc | existing | Second configuration carrying the same key families. | VAL-DOCS |
| docs/phase3-preconditions.md | proposed | The budget, fallback options, and per-measurement checklist. | VAL-DOCS, VAL-PRECOND |
| README.md | modified | Artifact manifest gains the configuration-file trap warning. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 1.1 for version control, Faz 1.4 for the working disassembler, Faz 2.1 for the smoke script, Faz 2.2 for the named baseline, and Faz 2.3 for the regression record. This is the sub-phase with the most upstream dependencies in the roadmap, and that is intentional — it is the gate where Phase 1 and Phase 2 pay off.

Blocks Faz 3.2, Faz 3.3, Faz 3.4, and Faz 3.5 absolutely. Autopsy requires the precondition check in every Phase 3 sub-plan, and this sub-phase is where that requirement is made concrete once rather than restated four times.

Required decisions: the attempt budget, which is the user's call because it is a budget. The implementer proposes a value with reasoning.

Required credentials or live endpoints: none. Device access with root through KernelSU is needed for the preference audit.

Required human approvals: the budget, and physical device access for the audit and clearance.

Fresh session token and context risk: low for this sub-phase itself, but it exists to protect a high-risk phase. Main-Planing bands Phase 3 as high and `R10` recommends recording every located address into the ontology immediately rather than at session end. The per-measurement checklist should carry that recording rule.

Subagents are not recommended. Main-Planing section 9 advises against them for this project, and device state is a single stateful resource.

## 11. Risks and Mitigations

- Risk (`EV-13` recurrence): a measurement in Faz 3.2 through Faz 3.5 runs with a preference set and its failure is attributed to the HAL. Impact: exactly the three-step misattribution the project has already paid for once. Mitigation: the per-measurement checklist makes the preference check a precondition of recording a result, and the smoke script reports it independently.
- Risk: the configuration files are imported mid-phase for an unrelated reason and silently re-arm the trap. Impact: a clean phase becomes contaminated between measurements. Mitigation: F3.1-03 places the warning in the artifact manifest, which is where an operator looks before using a root-level file.
- Risk (`AUTOPSY-P1-03`): the attempt budget is set but treated as advisory once the search feels close. Impact: the budget provides no protection and Phase 3 consumes the resources Phases 4 and 5 need. Mitigation: the budget is recorded as a number before the search starts, and Faz 3.6 is a scheduled decision gate rather than a fallback invoked at the implementer's discretion.
- Risk: a precondition is marked pass because the producing artifact exists rather than because its evidence was checked. Impact: Phase 3 starts on an unverified foundation. Mitigation: `VAL-PRECOND` requires verification against each producing sub-phase's evidence.
- Risk: the clearance procedure works once and the preference is rewritten on the next application start. Impact: an intermittent contamination that is harder to diagnose than a persistent one. Mitigation: `VAL-PREFS` requires a post-restart audit as a third run.
- Risk: the fallback options are enumerated abstractly and Faz 3.6 has to define them anyway. Impact: the decision gate improvises under pressure. Mitigation: each option carries its known cost and known risk here, including the Faz 4 evidence that the active-array direction breaks AGC when raw is not raised with it.
- Risk: the phase begins with an unrouted Faz 2.3 failure outstanding. Impact: a pre-existing regression is mistaken for a Phase 3 effect. Mitigation: the fourth precondition requires the regression record to have no unrouted failures.

## 12. Desired End State

Phase 3 has a verified entry state: no trap preference is set, the clearance is confirmed to survive a restart, both configuration files are flagged where an operator will see the flag, all four upstream preconditions have checked verdicts, a numeric attempt budget is agreed, the fallback options are enumerated with costs, and a per-measurement checklist exists that the following four sub-plans reference by name.

The evidence an implementer should produce is the three preference audit runs, the smoke snapshot confirming a stock or fullres HAL and clear preferences, the four precondition verdicts, and the written budget.

The ledger summary Step 4 should append records: the preference state before and after clearance, the four precondition verdicts, the agreed budget with its unit, and confirmation that the configuration-file warning was placed.

## 13. Next Sub-Phase Transition Criteria

- All ten trap keys are confirmed unset, including after an application restart.
- The smoke script's independent preference view agrees with the audit.
- All four entry preconditions pass with checked evidence.
- The attempt budget is a recorded number, agreed before any search begins.
- The fallback options are enumerated with cost and risk, ready for Faz 3.6.
- The per-measurement checklist is written and referenced from Faz 3.2 onward.
