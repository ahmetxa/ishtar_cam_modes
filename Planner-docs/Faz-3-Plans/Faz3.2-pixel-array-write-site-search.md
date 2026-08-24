# Faz 3.2 — Pixel Array Size Write Site Search

## 1. Context

This is the gating unknown of the entire roadmap. Main-Planing prioritized next step 5 names it: "Locate the `android.sensor.info.pixelArraySize` write site in `camera.qcom.so`. *Type: implementation slice (Phase 3).* The gating unknown for the project's headline goal. Nine movz/movk sites and six rodata dwords are already mapped."

Phase 3's description sets the approach: "The cleanest fix is to make the HAL report `android.sensor.info.pixelArraySize` (tag `f0006`) as 8192x6144 — which is the IMX989's true physical array, so this corrects a misstatement rather than introducing one. Nine `movz`/`movk` references and six rodata dwords for that tag have already been located in the binary; the write site has not. This is the highest-uncertainty work in the project and should be sliced tightly: locate the write site, patch, measure `dumpsys`, then attempt a capture."

Project-Comprehension frames it as `CQ-05`, priority P0, still open, with the answer criterion stated precisely: "An address that, when patched, changes `dumpsys` output." That criterion is what separates a plausible candidate from a located write site, and this sub-phase stops at identifying candidates — the patch and the measurement belong to Faz 3.3.

Hypothesis `H-01` states the working theory: "`pixelArraySize` is written from one of the six rodata dwords, reachable from the nine movz/movk sites", confidence `tentative`, with the probe described as "Disassemble around each rodata dword; find which feeds a metadata `update`/`set` call. Static, no device needed."

That last phrase is why this sub-phase is separable and why it is cheaper than its risk band suggests. The search is entirely static. No device, no flash, no capture.

## 2. Goal

Identify, within the agreed attempt budget, which code path in `camera.qcom.so` writes the value reported as `android.sensor.info.pixelArraySize`, producing either a ranked set of candidate patch sites or an explicit budget-exhausted result.

## 3. Description

The problem is a value the HAL reports that must change, in a stripped 27 MB binary, where the tag identifier's references are known but the site that assigns the value is not.

It belongs here because Faz 3.3 cannot patch what has not been located, and because the alternative direction — raising the active array — is already known to fail. Main-Planing's risk note is explicit: "the fallback is to raise the active array instead — but Faz 4 already showed that direction breaks AGC when raw is not raised with it. Both sides of the invariant must move together." Project-Ontology invariant 6 states the same insight from the other side, describing the libgcam requirement as the single invariant that explains two failures from opposite directions.

The vibecoding slice strategy follows Main-Planing's first slice directly: "Disassemble around the six rodata dwords to find which one is consumed by the metadata emitter; confirm with a single-word patch and a `dumpsys` read before attempting any capture." This sub-phase performs the first half — disassemble and identify — and hands the confirmation to Faz 3.3. The split exists because a candidate identified in a static session and a candidate confirmed on the device are different states of knowledge, and conflating them is how a wrong address gets patched.

The fastest validation signal available without the device is structural: a candidate site is credible if the value it moves reaches a metadata update or set call for tag `f0006`, and not credible if the reference is merely a tag comparison. Distinguishing those two is the actual work.

What should not be over-planned: a general method for locating arbitrary metadata write sites. The target is one tag. A reusable method may emerge and is worth recording if it does, but it is a by-product rather than a goal.

The budget agreed in Faz 3.1 governs this sub-phase specifically. `AUTOPSY-P1-03` exists because this is the work that expands without bound, and the budget is the mechanism that prevents it.

Two recording rules apply throughout. Main-Planing `R10` requires every located address to be written into the ontology immediately rather than at session end, and Project-Comprehension `QAS-03` states that the ontology "must be updated *during* Phase 3, not after, or it decays into the same problem". This is not administrative overhead; it is the mitigation for the phase's dominant risk.

## 4. Scope

- Static disassembly around the six recorded rodata dwords, determining for each whether it participates in a metadata write for tag `f0006`.
- Static analysis of the nine recorded `movz` and `movk` sites, classifying each as a tag comparison, a tag emission, or a value assignment.
- Identification of the function or functions containing the credible candidates, by address range, in the manner Project-Ontology section 6 already records `InitializeScalerStaticCaps`.
- A ranked candidate list, each entry stating the address, what the code does there, and what a single-word patch at that site would change.
- Determination of whether the value is a constant in the binary or is derived at runtime from a sensor property, since those imply different patch strategies and one of them may make a static patch impossible.
- Immediate recording of every located address into Project-Ontology section 6 as it is found.
- An explicit budget-exhausted outcome if no credible candidate emerges, handed to Faz 3.6.

## 5. Out of Scope

- Applying any patch. Faz 3.3 owns the first write.
- Any device interaction, flash, or measurement. This sub-phase is static.
- Any capture attempt or image inspection.
- Narrowing the RAW emission or adding duration rows, which are Phase 4.
- Investigating the active-array direction as a primary path. It is enumerated as a Faz 3.1 fallback and evaluated in Faz 3.6, not pursued here.
- Modifying `hal-fullres.patch` or `hal-raw50-deneme.patch`.
- Building a general-purpose metadata-tag locator.

## 6. Current Repository Evidence

Project-Ontology section 6 records the target under "`android.sensor.info.pixelArraySize`, tag `f0006`": nine `movz` and `movk` references at `0x004fe984`, `0x004fee94`, `0x004ffa5c`, `0x00d9ae24`, `0x00d9ae80`, `0x013b192c`, `0x013b1994`, `0x013b1a08`, `0x013b1a7c`; six rodata dwords at `0x0002c6ac`, `0x0038964c`, `0x003969b4`, `0x00396adc`, `0x00397fcc`, `0x0039c1f0`; and the statement "The write site has not been located."

The same section records the related tag identifiers the analysis will encounter: `android.scaler.availableStreamConfigurations` is `d000a`, `availableMinFrameDurations` is `d000b`, `availableStallDurations` is `d000c`, `android.sensor.info.activeArraySize` is `f0000`, and `preCorrectionActiveArraySize` is `f000a`. Distinguishing `f0006` from `f0000` and `f000a` matters, because the three are adjacent in the tag space and confusing them would target the wrong array.

The already-solved analogue provides both a method and a calibration. `InitializeScalerStaticCaps` is recorded at `0x16bf4c0` through `0x16c5a90`, 26 KB and 6,516 instructions, emitting 16-byte entries into an array at `[x?+0xb10]`. Its format gate is recorded instruction by instruction: `sub wN, wFmt, #0x22` then `cmp wN, #2` then `b.lo`. The four `cmp` sites are recorded with a transcription correction preserved: `0x16c2334` is the following `b.lo`, not the `cmp`. That correction is itself evidence about the precision this work requires.

`agc-50mp-yama/hal-raw50-deneme.patch` was read in this run and records the exact rejection text, naming both arrays as `4096x3072` while `frame_raw_max` is `8192x6144`. It also records the four patch indices `5965367`, `5965574`, `5965999`, `5966028`, which multiply by four to `0x16C18DC`, `0x16C1C18`, `0x16C22BC`, and `0x16C2330` — matching the four `cmp` sites in the ontology exactly. This confirms the four-byte index convention and gives the disassembly work a verified reference point.

`ishtar-cam-modes/blobs/hal-fullres.patch` records the stock binary's md5 as `c3fa63a86ee3ecaf9fbf02005d35f6b5` and `halpatch.sh` records `HAL_SIZE=27268688`, so the binary under analysis is identified exactly.

Project-Comprehension `EV-17` records that interactive disassemblers do not complete on this binary, confidence `confirmed`, with two runs at 300 and 60 seconds producing no output. The analysis must therefore be scripted, which Faz 1.4's toolchain procedure provides.

Project-Ontology `OQ-03` remains open: "Can `pixelArraySize` be raised without breaking other consumers?" — untested, with the note that the opposite direction is known to break AGC. That question is answered in Faz 3.4, not here.

## 7. Planned Work Breakdown

- F3.2-01 — Re-verify the address book before relying on it
  - Description: Confirm the four known `cmp` sites decode as recorded, using the Faz 1.4 self-check. A discrepancy means the address book or the binary has changed, and either finding must be resolved before the search proceeds.
  - Output: A verification result against four known-good addresses.
- F3.2-02 — Classify the nine tag references
  - Description: For each recorded `movz` and `movk` site, determine whether it participates in a comparison, an emission of the tag identifier, or an assignment of a value. Record the classification per address.
  - Output: A nine-row classification table.
- F3.2-03 — Trace each rodata dword to its consumer
  - Description: For each of the six dwords, determine what reads it and whether that path reaches a metadata update or set call for `f0006`. This is the direct test of `H-01`.
  - Output: A six-row trace table; `H-01` confirmed, contradicted, or undetermined.
- F3.2-04 — Determine constant versus runtime derivation
  - Description: Establish whether the reported value originates as a constant in the binary or is computed at runtime from a sensor property. A runtime derivation may make a static patch infeasible, which is a decisive finding for Faz 3.6.
  - Output: A stated origin with supporting evidence.
- F3.2-05 — Identify the containing function
  - Description: Establish the address range of the function or functions holding the credible candidates, recorded in the same form as `InitializeScalerStaticCaps`.
  - Output: One or more function ranges added to the address book.
- F3.2-06 — Produce the ranked candidate list
  - Description: Rank candidates by credibility, each entry stating the address, the instruction, what the code does there, and what a single-word patch would change. Faz 3.3 patches the top candidate first.
  - Output: A ranked candidate list with at least the top entry fully described.
- F3.2-07 — Record addresses into the ontology as they are found
  - Description: Write each located address into Project-Ontology section 6 during the session it is found, per `R10` and `QAS-03`. This is a continuous work item, not a closing step.
  - Output: An updated address book, current as of the session's end regardless of outcome.
- F3.2-08 — Declare the outcome against the budget
  - Description: State whether the search succeeded within budget, and if not, hand the budget-exhausted result to Faz 3.6 with everything learned attached.
  - Output: A budget verdict.

## 8. Acceptance Criteria

- The four known `cmp` sites decode as recorded, or a discrepancy is resolved before the search continues.
- All nine recorded tag references have a classification.
- All six rodata dwords have a trace verdict.
- `H-01` in Project-Comprehension is no longer `tentative` — it is confirmed, contradicted, or explicitly undetermined within budget.
- The constant-versus-runtime question has a stated answer with supporting evidence.
- If a credible candidate exists, the ranked list describes at least the top entry completely enough for Faz 3.3 to patch it without re-derivation.
- Every address located during the work appears in Project-Ontology section 6 by the end of the session, not in a note to be transferred later.
- The budget verdict is stated explicitly, and an exhausted budget is recorded as a completed outcome rather than an incomplete one.
- No patch has been applied and no device interaction has occurred.

## 9. Validation and Test Approach

Validation here is unusual: this sub-phase produces a hypothesis rather than a verified fact, and its acceptance criteria are about analytical completeness rather than about a working result. The verified fact arrives in Faz 3.3.

- `VAL-DISASM` (from Faz 1.4) — the scripted disassembly path, self-checked against the four known `cmp` sites before use. Scripted rather than interactive, per `EV-17`.
- `VAL-CALIBRATE` (proposed) — the F3.2-01 re-verification, which is the analysis equivalent of a control. If the known sites do not decode correctly, nothing else in the session is trustworthy.
- `VAL-DOCS` (proposed) — read back the classification table, the trace table, and the ontology additions; confirm every located address was recorded during the session.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist, applied even though this sub-phase is static, because it also covers the recording rule.

Local versus live: entirely local. This is the only Phase 3 sub-plan with no live dimension, which is why it can proceed without the user's hands.

Security validation is not applicable. Ontology validation is central: the address book is the artifact being extended, and its existing conventions — recording transcription corrections, distinguishing `cmp` from the following branch — must be followed.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| Planner-docs/Project-Ontology.md | modified | The address book extended with every located address during the session. | VAL-DOCS, VAL-DISASM |
| Planner-docs/Project-Comprehension.md | modified | Resolve `H-01` and update `CQ-05` from open to its measured state. | VAL-DOCS |
| docs/reverse-engineering-toolchain.md | existing | The scripted disassembly procedure and its self-check. | VAL-DISASM, VAL-CALIBRATE |
| ishtar-cam-modes/blobs/hal-fullres.patch | existing | Source of the stock binary checksum identifying the analysis target. | VAL-CALIBRATE |
| docs/phase3-preconditions.md | existing | The attempt budget this sub-phase is measured against. | VAL-PRECOND |

## 10. Dependencies and Sequencing

Depends on Faz 3.1 for the budget, the precondition verdicts, and the per-measurement checklist. Depends on Faz 1.4 for a working scripted disassembler and on Faz 1.1 so that ontology updates are versioned.

Does not depend on Faz 2.2 or Faz 2.3, since it is static — but Faz 3.1 requires those preconditions anyway, because the phase as a whole needs them and gating them here rather than at Faz 3.3 keeps the sequence simple.

Blocks Faz 3.3 absolutely. Blocks Faz 3.6 in the sense that the decision gate needs this sub-phase's outcome, whether success or exhaustion.

Required decisions: none during the work. The budget was set in Faz 3.1.

Required credentials, infrastructure, live endpoints, or human approvals: none. This is the sub-phase the implementer can execute without the user present.

Fresh session token and context risk: high, and this is the highest-risk sub-phase in the roadmap for context specifically. Main-Planing `R10` states it: "Phase 3 involves disassembling a 27 MB stripped binary. *Impact:* long sessions, context exhaustion, repeated re-derivation." The mitigations are structural — scripted extraction with bounded output rather than interactive exploration, and immediate ontology recording so a truncated session loses momentum rather than findings.

Subagents: Main-Planing section 9 advises against subagents for this project and specifically notes "The work is deep rather than broad, the evidence is concentrated in a few large files the parent already holds." That reasoning applies here. A bounded read-only helper for a single mechanical extraction is defensible if the parent's context is nearly exhausted, but the parent must own every ontology write.

## 11. Risks and Mitigations

- Risk (`R4`, severity high): the write site does not exist as a patchable constant, because the value is derived at runtime. Impact: the project's headline goal stalls on this path. Mitigation: F3.2-04 tests this explicitly and early, so the finding arrives as a decisive answer rather than as an accumulation of failed attempts.
- Risk (`R10`): the session exhausts context mid-search and the located addresses are lost. Impact: the next session re-derives what was already found, which has happened before in this project. Mitigation: F3.2-07 is a continuous work item and the acceptance criteria require same-session recording.
- Risk (`AUTOPSY-P1-03`): the search runs past its budget because each next candidate feels close. Impact: Phases 4 and 5 lose their resources. Mitigation: the budget is a number set in Faz 3.1, and F3.2-08 requires an explicit verdict against it.
- Risk: tag `f0006` is confused with `f0000` or `f000a` during analysis. Impact: the active array is patched instead of the pixel array, which is the direction already known to break AGC. Mitigation: the scope requires distinguishing the three, and section 6 records all three identifiers so the distinction is available at the point of work.
- Risk: a plausible candidate is promoted to "located" without the `dumpsys` confirmation. Impact: Faz 3.3 patches a wrong address and the resulting failure is ambiguous. Mitigation: the sub-phase boundary is drawn precisely here — candidates are output, confirmation is Faz 3.3, and `CQ-05`'s answer criterion requires an address that changes `dumpsys` output.
- Risk: an interactive disassembler is attempted despite `EV-17`. Impact: 300 seconds of no output and a wasted session start. Mitigation: Faz 1.4's procedure records the symptom, and `VAL-DISASM` specifies the scripted path.
- Risk: the address book has drifted or the binary on hand differs from the one analyzed previously. Impact: every derived address is wrong and the error is discovered late. Mitigation: F3.2-01 calibrates against four known-good sites before any new work.

## 12. Desired End State

The write-site question has a definite state. Either a ranked candidate list exists with the top entry described completely enough to patch without re-derivation, or the budget is exhausted with everything learned recorded and handed to the decision gate. In both cases the nine tag references are classified, the six rodata dwords are traced, the constant-versus-runtime question is answered, and every address found during the work is in the ontology.

The evidence an implementer should produce is the calibration result against the four known sites, the classification and trace tables, the stated value origin, and the ranked candidate list or the budget verdict.

The ledger summary Step 4 should append records: the budget consumed, whether a candidate was identified, the `H-01` outcome, the addresses added to the ontology, and whether Faz 3.6 is being invoked.

## 13. Next Sub-Phase Transition Criteria

- The calibration against the four known sites passed, or its discrepancy was resolved.
- All nine references are classified and all six dwords are traced.
- `H-01` has a stated outcome and `CQ-05` reflects it.
- The constant-versus-runtime question is answered.
- Either a ranked candidate list exists for Faz 3.3, or a budget-exhausted verdict is handed to Faz 3.6.
- Every address located is in Project-Ontology section 6, recorded during the session it was found.
- No patch has been applied; the device is untouched.
