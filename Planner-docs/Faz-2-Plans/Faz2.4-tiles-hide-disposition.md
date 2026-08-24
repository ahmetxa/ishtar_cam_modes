# Faz 2.4 — Tiles Hide Option Disposition

## 1. Context

Main-Planing Phase 2 lists as its final item: "Decide the fate of the `tiles hide` option, which is recorded as ineffective." Prioritized next step 10 restates it as a planning decision needing a human call: "fix, remove, or document as a known limitation."

Autopsy is more pointed about why a non-functional control is worse than an absent one. Section 5 classifies it as "**delivery-blocking in the reputational sense.** A visible control that silently does nothing is worse than an absent one." Section 13 files it as `AUTOPSY-P2-01` with the impact stated as "it erodes trust in the module's other status reporting" — which matters specifically because the module's other status reporting is what the operator relies on during Phase 3 debugging.

Project-Comprehension records the behavior as `EV-22`, confidence `probable`, evidenced by on-device observation with the note "the cause was never diagnosed". `OQ-11` in Project-Ontology asks "Why is the `tiles hide` option ineffective?" and remains open. Hypothesis `H-05` proposes that the failure is a framework-visibility issue rather than a module bug, and suggests comparing against the v2.1 fix that solved an adjacent symptom.

The connection `H-05` draws is the substantive one. `module.prop` records that v2.1 changed launcher visibility to be reapplied on every call with status read from the framework rather than from a cache. That is the same class of problem — a visibility state the module sets and the framework does not honor or does not report back — which makes it plausible that the fix pattern already exists in the codebase.

## 2. Goal

Reach and record a decision on the `tiles hide` option — repair, remove, or label as a known limitation — supported by enough diagnosis to make the decision informed rather than arbitrary.

## 3. Description

The problem is a control in the user interface that does nothing, with no diagnosis behind it. It has persisted across at least two releases and has been carried forward each time as a known oddity rather than resolved.

It belongs in Phase 2 because Phase 2 is the release-hygiene phase and because the decision affects what ships. It reduces risk in a narrow but real way: a user who learns one control lies has reason to doubt the status reporting that Phase 3's debugging depends on.

The vibecoding slice strategy is diagnosis-first with a bounded budget. The first useful slice is a time-boxed investigation testing `H-05` by reading the tile application and `service.sh` and comparing against the v2.1 launcher-visibility fix. The fastest validation signal is whether the same pattern applies — if the module sets tile visibility through a call whose result it never reads back from the framework, `H-05` is likely correct and the fix is probably small. If the mechanism is entirely different, the investigation stops and the decision is made from the remove-or-label options.

The bound matters. This is a low-priority cosmetic defect in a phase whose real purpose is the release baseline, and it sits immediately before the highest-uncertainty phase in the roadmap. An open-ended investigation here spends budget that Phase 3 needs. The investigation gets one bounded attempt, and if it does not produce a clear cause, the decision is made without one.

What not to over-plan: any redesign of tile management, and any change to how the four functional tiles behave. Those work and are out of scope entirely.

Between remove and label, remove is the stronger default. Autopsy's argument is that an absent control is better than a lying one, and removing it closes the finding permanently while labelling leaves it open in a document nobody reads at the moment they press the control. Labelling is appropriate only if removal turns out to be more invasive than the defect warrants.

## 4. Scope

- A bounded diagnostic investigation testing `H-05` against the tile application sources and `service.sh`.
- Comparison against the v2.1 launcher-visibility fix, to determine whether the same pattern applies.
- A decision among three options: repair, remove, or label as a known limitation.
- If repair: the change scoped and routed, with the four functional tiles explicitly protected from regression.
- If remove: the removal scoped, with confirmation that nothing else references the option.
- If label: the exact wording and its location, plus an entry recording that the finding is accepted rather than resolved.
- Resolution of `OQ-11` in Project-Ontology, either with a cause or with an explicit statement that the cause was not found within the bound.
- Update of `EV-22` and `H-05` in Project-Comprehension.

## 5. Out of Scope

- Any change to the four functional QuickSettings tiles or to their mutual exclusion behavior.
- Redesigning tile registration, or changing how tiles are added on first boot.
- The launcher visibility feature itself, which v2.1 fixed and which Faz 2.3 verifies.
- An unbounded investigation. One bounded attempt, then a decision.
- Implementing the chosen option, if it turns out to require Java changes and a rebuild of the tile application. In that case the implementation is routed to Phase 9's release work; this sub-phase produces the decision and its scope.
- The WebUI's own presentation of the option, beyond noting whether it also exposes it.

## 6. Current Repository Evidence

`ishtar-cam-modes/tile-app/` contains `AndroidManifest.xml`, `build.sh`, and `debug.keystore`. The Java sources are not present as files in the working tree at the top two levels; `ishtar-cam-modes/tile-app.apk` is the built artifact. Project-Comprehension `TRACE-06` records "Tiles and launcher visibility — `tile-app/` (Java) — not read this pass", so the tile application internals remain uninspected by any ClaudeQB run.

This is the first practical constraint on the investigation: if the Java sources are not in the tree, diagnosis must work from `service.sh`, from the manifest, and from observed behavior rather than from source. The investigation's bound should account for that.

`ishtar-cam-modes/service.sh` is 44 lines and handles late-boot work including launcher visibility, per Main-Planing section 3 and Project-Ontology section 5. It is a plausible location for tile visibility handling and has not been read by any ClaudeQB run.

`ishtar-cam-modes/module.prop` records the v1.4 entry describing three QuickSettings tiles with the note that the application does not appear in the drawer, and the v2.1 entry describing the launcher visibility fix: visibility is now reapplied on every call and status is read from the framework rather than from a cache. The v1.4 and v2.1 entries together suggest visibility control has been reworked at least twice.

`ishtar-cam-modes/webroot/index.html` was partially read in this run. Its `build()` function constructs buttons from `MAIN_MODES` and an `extra` group; whether a hide control appears in either was not determined and should be established during the investigation.

No diagnosis of the `tiles hide` failure exists anywhere in the tree or in the continuity artifacts.

## 7. Planned Work Breakdown

- F2.4-01 — Establish where the option is exposed
  - Description: Determine which surfaces present the control — QuickSettings, the WebUI, the action interface, or more than one. A control exposed in two places may fail in one and work in the other, which changes the diagnosis.
  - Output: An exposure map.
- F2.4-02 — Read `service.sh` and the tile manifest
  - Description: Read the 44-line late-boot script and the application manifest for visibility handling. Record whether tile visibility is set from shell, from Java, or from both.
  - Output: A mechanism description, or a statement that the mechanism is not determinable without the Java sources.
- F2.4-03 — Test `H-05` against the v2.1 fix pattern
  - Description: Compare the tile visibility mechanism against the launcher visibility mechanism that v2.1 corrected. Determine whether the same read-from-framework-rather-than-cache issue applies.
  - Output: `H-05` confirmed, contradicted, or undetermined within the bound.
- F2.4-04 — Close the investigation at the bound
  - Description: Stop the diagnosis at the agreed bound regardless of outcome, and record what was and was not established. An undetermined result is a valid outcome that still supports a decision.
  - Output: An investigation record with an explicit stop point.
- F2.4-05 — Make the decision
  - Description: Choose repair, remove, or label. Record the reasoning, including the Autopsy argument that an absent control beats a lying one. This is the user's call where a preference exists; the implementer proposes with a recommendation.
  - Output: A recorded decision with reasoning.
- F2.4-06 — Scope the chosen option
  - Description: Whichever option is chosen, write what it touches, what must not regress, and which phase implements it. If the option requires rebuilding the tile application, route it to Phase 9.
  - Output: A scoped change description with routing.
- F2.4-07 — Update the continuity artifacts
  - Description: Resolve `OQ-11` with either a cause or an explicit not-determined status, and update `EV-22` and `H-05`.
  - Output: Three updated rows.

## 8. Acceptance Criteria

- The exposure map names every surface that presents the option.
- The investigation is recorded with an explicit stop point, and its outcome is one of confirmed, contradicted, or undetermined — not left implicit.
- A decision exists among repair, remove, and label, with written reasoning.
- The decision's scope names what it touches and what must not regress, with the four functional tiles explicitly protected.
- If implementation requires rebuilding the tile application, it is routed to a named phase rather than attempted here.
- `OQ-11` in Project-Ontology section 8 no longer reads `open`; if the cause was not found, the status says so rather than remaining silent.
- `EV-22` and `H-05` in Project-Comprehension are updated to reflect the investigation's outcome.
- No change to the four functional tiles has been made in this sub-phase.

## 9. Validation and Test Approach

Validation is predominantly static source review plus a decision record. If a repair is chosen and implemented within this phase, a device check is added; otherwise there is no live component.

- `VAL-STATIC` (proposed) — read `service.sh` and the tile manifest; record the mechanism or the reason it cannot be determined from available sources.
- `VAL-DOCS` (proposed) — read back the decision record, the exposure map, and the three updated continuity rows; confirm the investigation's stop point is stated.
- `VAL-MANUAL` (proposed, conditional) — if a repair is implemented, the user confirms the control now behaves as labelled and that the four functional tiles are unaffected. Not applicable for the remove or label outcomes within this sub-phase.

Local versus live: the investigation is local and static. The decision is a planning artifact. Only a repair introduces a live dimension, and that is explicitly conditional.

Security validation is not applicable. Ontology validation applies weakly: the decision record should use the Project-Ontology term "Tile" consistently and should not conflate tile visibility with launcher visibility, which are separate mechanisms that have been confused before.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/service.sh | existing | Late-boot visibility handling; primary read target for the mechanism. | VAL-STATIC |
| ishtar-cam-modes/tile-app/AndroidManifest.xml | existing | Tile registration and component declarations. | VAL-STATIC |
| ishtar-cam-modes/webroot/index.html | existing | Determines whether the option is also exposed in the web interface. | VAL-STATIC |
| Planner-docs/Project-Ontology.md | modified | Resolve `OQ-11` with a cause or an explicit not-determined status. | VAL-DOCS |
| Planner-docs/Project-Comprehension.md | modified | Update `EV-22` and `H-05` from the investigation outcome. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 2.2 only in that the decision should describe the released build's behavior. Benefits from running after Faz 2.3, since the regression pass exercises the tile surface and may surface incidental evidence about the option.

Does not block Phase 3. This is the one Phase 2 sub-plan that Phase 3 does not depend on, and if Phase 3 is time-critical this may be deferred — with the caveat that deferring it indefinitely is how it reached its third release unresolved.

Required decisions: the disposition itself, which Main-Planing section 9 lists among the decisions needing human confirmation. The implementer investigates and recommends; the user chooses.

Required credentials, infrastructure, or live endpoints: none for the investigation. A repair would need the Java toolchain from Faz 1.4 and the signing key policy from Faz 1.2.

Required human approvals: the disposition decision.

Fresh session token and context risk: low, and bounded by design. The investigation has an explicit stop point precisely so it cannot expand into Phase 3's budget.

Subagents are not recommended. The surface is two small files and a manifest.

## 11. Risks and Mitigations

- Risk: the investigation expands past its bound because a cause feels close. Impact: budget intended for Phase 3, the highest-uncertainty phase in the roadmap, is spent on a cosmetic defect. Mitigation: F2.4-04 makes stopping a work item with an outcome, so an undetermined result is a completion rather than a failure.
- Risk: the Java sources are absent and the mechanism cannot be determined. Impact: the diagnosis half of the sub-phase produces nothing. Mitigation: this is anticipated in section 6 and the decision path does not require a diagnosis — remove and label are both available without one.
- Risk (`AUTOPSY-P2-01` residual): the option is labelled rather than removed, and a user presses it anyway. Impact: the trust cost Autopsy describes is unchanged, because a label in a document does not reach the person pressing a control. Mitigation: the description section states removal as the stronger default and requires labelling to be justified by removal cost.
- Risk: a repair is attempted and breaks one of the four functional tiles. Impact: a working feature is traded for a cosmetic one, in the area Project-Comprehension identifies as the most regression-prone in the codebase. Mitigation: the scope explicitly protects the four tiles, and a repair carries a conditional manual verification.
- Risk: tile visibility and launcher visibility are conflated during diagnosis. Impact: the v2.1 fix is credited with solving a problem it did not touch, and the real cause is missed. Mitigation: the ontology validation note requires the two mechanisms to be kept distinct in the record.
- Risk: the decision is made but never implemented, and the option ships again. Impact: a fourth release with the same defect. Mitigation: F2.4-06 routes implementation to a named phase, and Faz 9.2's release checklist can carry it as a verifiable item.

## 12. Desired End State

The `tiles hide` option has a recorded disposition with written reasoning, supported by a bounded investigation whose outcome — including an undetermined outcome — is explicitly stated. `OQ-11` is closed one way or the other, the two comprehension rows are updated, and if implementation is needed it is scoped and routed to a named phase with the four functional tiles protected.

The evidence an implementer should produce is the exposure map, the investigation record with its stop point, and the decision record.

The ledger summary Step 4 should append records: the decision taken, whether a cause was established, where implementation was routed if applicable, and the fact that the four functional tiles were not modified.

## 13. Next Sub-Phase Transition Criteria

- The investigation has a recorded stop point and a stated outcome.
- A disposition decision exists with reasoning.
- `OQ-11` is no longer open, even if the resolution is that the cause was not determined within the bound.
- Implementation, if required, is routed to a named phase rather than left implicit.
- The four functional tiles are confirmed unmodified.
- Phase 2 is complete: the smoke surface exists, the release is flashed and baselined, the regression record is written, and this decision is made.
