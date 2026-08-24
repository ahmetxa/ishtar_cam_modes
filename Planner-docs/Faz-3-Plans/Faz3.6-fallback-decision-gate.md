# Faz 3.6 — Fallback Decision Gate

## 1. Context

This sub-phase exists because Autopsy demanded it. `AUTOPSY-P1-03` states the finding: "Phase 3 has no stop condition. Impact: locating a write site in a 27 MB stripped binary is open-ended; without a bound, the token budget and the session both run out before a decision is reached." Its Step 2 impact is stated as a requirement: "every Phase 3 sub-plan needs an explicit attempt budget and a named fallback (accept the app-level patch, or move the active array instead)."

Autopsy section 11 repeats it among the assumptions needing sharpening: "Phase 3 is described as high-risk and high-token, which is right, but the plan does not state a stop condition. Reverse-engineering phases without a stop condition are how token budgets disappear. Step 2 should give Phase 3 an explicit bound: a number of located-address attempts, or a fallback decision point where the app-level patch is accepted as the answer."

Faz 3.1 sets the budget and enumerates the options. This sub-phase is where they are used. It is deliberately a scheduled gate rather than an escape hatch invoked at the implementer's discretion, because a fallback that is only reached when someone gives up is not a stop condition.

It runs in both outcomes. If Phase 3 succeeded, this gate records what was achieved, resolves the phase's open questions, and hands Phase 4 a precise statement of what must be preserved. If Phase 3 did not succeed, it selects among the enumerated fallbacks. Running it only on failure would make it a failure ritual; running it always makes it the phase's closing act.

Main-Planing section 9 names a decision that lands here: "Whether Phase 5 still has priority given how much Phase 3 has grown." Phase 3's outcome is the main input to that judgment.

## 2. Goal

Close Phase 3 with a recorded decision: either the primary path succeeded and Phase 4 inherits a defined preservation requirement, or a named fallback is selected with its cost and consequences stated, and the roadmap's priorities are re-examined in light of what the phase cost.

## 3. Description

The problem this solves is drift. A reverse-engineering phase without a scheduled close does not end; it thins out, and the transition to the next phase happens by attention shifting rather than by decision. That leaves the project without a recorded answer to "what is the state of the headline goal", which is exactly the kind of gap that costs a future session a re-derivation.

It belongs at the end of Phase 3 for the obvious reason, and it belongs as a distinct sub-plan rather than a paragraph in Faz 3.5 for a less obvious one: a decision made inside the sub-phase whose outcome it evaluates is not independent. If Faz 3.5 fails, the person who just spent a session failing is the worst-positioned person to judge whether to continue.

The vibecoding slice strategy: assemble the phase's evidence, evaluate it against the budget and the enumerated options, decide, and record. There is no experimental component. The fastest validation signal is that every Phase 3 open question has a recorded state — a gate that leaves questions open has not closed the phase.

What should not be over-planned: a decision tree covering every possible partial outcome. The options were enumerated in Faz 3.1 with their costs; this sub-phase applies judgment to actual evidence, which is a human act rather than a procedure.

The fallback options themselves deserve restating in the terms the evidence has given them. The application-level patch is a real fallback with known properties: `agc-50mp-yama/README.md` describes it as gated behind `pref_48m_key` so the APK behaves as stock without that preference, and Project-Comprehension records that it makes the port see 8192x6144 and open a matching ImageReader while capture does not complete. Accepting it as the answer means accepting the current stuck state, so it is a fallback only if paired with a different diagnosis of the stuck shutter. Moving the active array instead is the second option, and Faz 4 evidence records that this direction breaks AGC when raw is not raised with it — but raw is now raised, which changes the conditions under which that evidence was gathered. Deferring the phase is the third, and it is the one that preserves the most optionality if the budget is exhausted without a decisive finding.

## 4. Scope

- Assembly of Phase 3's complete evidence: the preference clearance, the search outcome, the patch confirmation or elimination, the consumer survey, and the capture attempt.
- Evaluation of budget consumed against the budget agreed in Faz 3.1.
- Confirmation that every Phase 3 open question and hypothesis has a recorded state.
- A decision among: primary path succeeded; select a named fallback; or defer the phase with the current state preserved.
- If the primary path succeeded: a precise statement of what Phase 4 must preserve while narrowing.
- If a fallback is selected: its cost, its consequences for the target end state, and what changes in the roadmap.
- Re-examination of Phase 5's priority in light of Phase 3's actual cost.
- A decision on the device's resting state: patched, reverted, or partially applied, recorded explicitly.
- Ledger entries closing the phase.

## 5. Out of Scope

- Any further search, patch, or capture attempt. The gate evaluates; it does not extend the phase.
- Implementing whichever fallback is chosen. Selection here, implementation in the phase that owns it.
- Narrowing the RAW emission or adding duration rows, which are Phase 4 regardless of the outcome.
- Re-opening the budget. If the budget is exhausted, that is the input to the decision rather than a parameter to adjust.
- Deciding Phase 6 through Phase 9 sequencing beyond the specific Phase 5 priority question.
- Any change to the sensor layer or the ten-mode surface.

## 6. Current Repository Evidence

The evidence this gate consumes is produced by the preceding five sub-phases, so this section records the pre-phase state against which their results are read.

Project-Comprehension section 1 lists the Phase 3 questions that must have a recorded state by the time this gate runs: `CQ-05` ("Where does the HAL write `pixelArraySize`?", P0, open at phase start) and `CQ-07` ("What is the smallest correct HAL patch?", P1, open — though that one is Phase 4's to close). `CQ-01` and `CQ-04` were already answered before the phase began, which is why the phase could be planned this precisely.

Project-Ontology section 8 lists the questions the phase touches: `OQ-01` (the write site, open at phase start), `OQ-02` (remosaiced Bayer or Quad-Bayer, open, never captured), and `OQ-03` (can `pixelArraySize` be raised without breaking other consumers, open, untested).

Project-Comprehension section 8 lists the hypotheses: `H-01` (the rodata dword theory), `H-02` (raising the value satisfies libgcam without breaking consumers), and `H-03` (remosaiced Bayer). All three were `tentative` at phase start and all three should have a resolved or explicitly-undetermined state by this gate.

Main-Planing's phase table bands Phase 3's token and context risk as high — the only phase so banded alongside Phase 8. Section 9 confirms it: "Phase 3: high — budget for it explicitly and checkpoint after every located address by writing it into the ontology before continuing."

Main-Planing section 9 also records the four decisions needing human confirmation, one of which lands squarely here: whether Phase 5 retains its priority given Phase 3's growth. The others — the AON module's disposition, the `tiles hide` fate, and the version control remote question — belong to Faz 9.3, Faz 2.4, and Faz 1.1 respectively.

`agc-50mp-yama/README.md` documents the application-level patch's exact gating: rewritten `getSupportedOutputSizes` drawing from a new `allOutputSizes` method when `pref_48m_key` is non-zero, with stock behavior otherwise. This is the fallback option's real shape and it is a partial solution rather than a complete one.

Project-Ontology invariant 6 records the insight the whole phase rests on, including its own history: the same libgcam requirement explains both the Faz 4 failure and the Faz 12 failure, from opposite directions. Whatever this gate decides, that invariant's record should reflect what the phase learned about it.

## 7. Planned Work Breakdown

- F3.6-01 — Assemble the phase evidence
  - Description: Collect the outputs of Faz 3.1 through Faz 3.5 into one view: precondition verdicts, search outcome, patch result, consumer verdicts, capture verdicts.
  - Output: A phase evidence summary.
- F3.6-02 — Reconcile budget consumed against budget agreed
  - Description: State how much of the Faz 3.1 budget was used and on what. This is what makes the budget mechanism real rather than ceremonial.
  - Output: A budget reconciliation.
- F3.6-03 — Confirm every open question has a state
  - Description: Check `OQ-01`, `OQ-02`, `OQ-03`, `CQ-05`, `H-01`, `H-02`, and `H-03`. Each must read as answered, contradicted, or explicitly undetermined — not open.
  - Output: A seven-item question audit.
- F3.6-04 — Make the decision
  - Description: Choose among primary success, a named fallback, or deferral, based on the assembled evidence. Record the reasoning, including what was ruled out and why.
  - Output: A recorded decision with reasoning.
- F3.6-05 — Define Phase 4's preservation requirement, on success
  - Description: If the primary path succeeded, state precisely which patch entries and which metadata values Phase 4's narrowing must preserve. Phase 4 changes the RAW emission and adds duration rows; it must not disturb whatever made the capture complete.
  - Output: A preservation requirement handed to Faz 4.1.
- F3.6-06 — State the fallback's consequences, on selection
  - Description: If a fallback is selected, state what changes in the target end state. Main-Planing's functional target says both Open Camera and the AGC port produce a full-resolution image; a fallback that does not deliver that changes the target and the change should be explicit rather than quiet.
  - Output: A revised target statement for the user's confirmation.
- F3.6-07 — Re-examine Phase 5's priority
  - Description: Judge whether the mode-0 12-bit experiment retains its position given what Phase 3 cost and achieved. This is the user's decision; the implementer supplies the evidence and a recommendation.
  - Output: A priority recommendation with the decision routed to the user.
- F3.6-08 — Decide and record the device resting state
  - Description: Determine whether the device is left patched, reverted, or partially applied, and record it. An unrecorded resting state makes the next phase's first measurement ambiguous.
  - Output: A recorded device state.
- F3.6-09 — Close the phase in the ledger
  - Description: Write the phase closure entry: what was achieved, what was not, what was decided, and what the next phase inherits.
  - Output: A ledger phase-closure entry.

## 8. Acceptance Criteria

- The phase evidence summary covers all five preceding sub-phases with their actual outputs, not their intended ones.
- The budget reconciliation states consumption against the agreed figure.
- All seven tracked questions and hypotheses have a state that is not `open`; an explicitly undetermined state is acceptable, silence is not.
- A decision exists among the three options, with written reasoning naming what was ruled out.
- On success: Phase 4's preservation requirement is specific enough that Faz 4.1 can verify it has not been violated.
- On fallback: the consequences for the target end state are stated and routed to the user for confirmation, rather than absorbed silently.
- The Phase 5 priority question has a recommendation and is routed to the user as a decision.
- The device's resting state is recorded explicitly.
- The ledger carries a phase-closure entry.
- No search, patch, or capture attempt occurred during this gate.

## 9. Validation and Test Approach

This sub-phase produces decisions and records rather than measurements, so its validation is verification of completeness and traceability.

- `VAL-DOCS` (proposed) — read back the evidence summary, the budget reconciliation, the question audit, the decision, and the ledger entry; confirm each claim traces to a preceding sub-phase's recorded output rather than to recollection.
- `VAL-QUESTIONS` (proposed) — check each of the seven tracked questions and hypotheses in the continuity artifacts and confirm none reads `open`. This is a mechanical check with a binary outcome.
- `VAL-SMOKE` (from Faz 2.1) — one final snapshot establishing the recorded resting state as a fact rather than an intention.

Local versus live: predominantly local, with one live snapshot for the resting state. Security validation is not applicable. Ontology validation applies: invariant 6 should reflect what the phase learned, and the address book should carry every address located.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Final snapshot establishing the recorded device resting state. | VAL-SMOKE |
| Planner-docs/Project-Ontology.md | modified | Confirm `OQ-01`, `OQ-02`, and `OQ-03` are closed and invariant 6 reflects the phase's learning. | VAL-QUESTIONS |
| Planner-docs/Project-Comprehension.md | modified | Confirm `CQ-05`, `H-01`, `H-02`, and `H-03` have states. | VAL-QUESTIONS |
| Planner-docs/Planing-Ledger.md | modified | The phase-closure entry recording achievement, decision, and inheritance. | VAL-DOCS |
| docs/phase3-preconditions.md | existing | The budget and fallback options this gate evaluates against. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 3.1 through Faz 3.5 for their outputs. It runs regardless of whether they succeeded, which is what distinguishes it from a contingency.

Blocks Phase 4 in the sense that Faz 4.1's scope depends on this gate's preservation requirement or its fallback selection. Fixing Phase 4's scope before this gate runs would mean planning against an unknown starting point.

Feeds Phase 5's scheduling through the priority question, and feeds Phase 9 if the target end state is revised, since the release checklist maps claimed capabilities to proving commands and a revised target changes what is claimed.

Required decisions: the primary decision itself and the Phase 5 priority question, both of which involve the user. Main-Planing lists the second among the four decisions needing human confirmation.

Required credentials, infrastructure, or live endpoints: only device access for the final snapshot.

Required human approvals: the decision and any revision to the target end state.

Fresh session token and context risk: low. This is a synthesis sub-phase reading recorded outputs. Deliberately so — placing a low-cost decision gate at the end of the highest-cost phase means the decision is not made under budget pressure.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the gate is skipped on success, because a successful phase feels self-closing. Impact: Phase 4 inherits no preservation requirement and may narrow away the thing that made the capture work. Mitigation: the description states the gate runs in both outcomes, and F3.6-05 exists specifically for the success path.
- Risk: the decision is made by the implementer who just completed the phase, under the influence of sunk effort. Impact: a fallback that should be selected is not, and the budget is quietly extended. Mitigation: the Phase 5 priority question and the fallback consequences are both routed to the user, which introduces an independent judgment.
- Risk: a question is left `open` because its answer was undetermined. Impact: the phase closes with a gap that looks like an oversight to a future reader, and the distinction between "not attempted" and "attempted without result" is lost. Mitigation: `VAL-QUESTIONS` accepts an explicit undetermined state and rejects silence.
- Risk (`AUTOPSY-P1-03` residual): the budget is exceeded and the gate adjusts the budget instead of deciding. Impact: the stop condition never binds, which is the exact failure the finding predicts. Mitigation: the out-of-scope section forbids re-opening the budget; exhaustion is an input, not a parameter.
- Risk: the target end state is quietly revised when a fallback is selected. Impact: Main-Planing's functional target and the shipped reality diverge without anyone deciding that they should. Mitigation: F3.6-06 routes the revision to the user for confirmation.
- Risk: the device is left in a partially applied state and nobody records it. Impact: Phase 4's first measurement has an unknown baseline. Mitigation: F3.6-08 plus a final smoke snapshot make the resting state a recorded fact.
- Risk: the ledger entry summarizes intentions rather than results. Impact: the closure record repeats the plan instead of the outcome, and a future replanning run reads it as evidence. Mitigation: `VAL-DOCS` requires every claim to trace to a preceding sub-phase's recorded output.

## 12. Desired End State

Phase 3 is closed by decision rather than by attrition. The evidence is assembled, the budget is reconciled, all seven tracked questions carry a state, and a recorded decision names either a success with a preservation requirement for Phase 4, or a fallback with its stated consequences, or a deferral with the current state preserved. The Phase 5 priority question is with the user. The device's resting state is a recorded fact.

The evidence an implementer should produce is the phase evidence summary, the budget reconciliation, the seven-item question audit, the decision record, and the final snapshot.

The ledger summary Step 4 should append the phase-closure entry itself: what was achieved, what was not, what was decided, what Phase 4 inherits, and where the two routed user decisions stand.

## 13. Next Sub-Phase Transition Criteria

- All seven tracked questions and hypotheses have a non-open state.
- A decision is recorded with reasoning, in whichever of the three forms applies.
- On success, Phase 4 has a specific preservation requirement it can verify against.
- On fallback, the target end state revision is with the user rather than assumed.
- The Phase 5 priority recommendation is routed.
- The device resting state is recorded and confirmed by a snapshot.
- The ledger carries the phase-closure entry, and Phase 4 does not begin before it exists.
