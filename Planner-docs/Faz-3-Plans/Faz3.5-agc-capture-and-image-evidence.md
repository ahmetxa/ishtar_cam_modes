# Faz 3.5 — AGC Capture and Image Evidence

## 1. Context

This is the sub-phase the entire roadmap points at. Main-Planing's executive summary names it: "The most important next milestone is **a reproducible 50 MP capture that completes inside AGC**." Phase 3's desired end state is stated in one sentence: "A 50 MP photograph exists, taken with AGC, with the QuickSettings tile as the only switch."

Its acceptance signals are given precisely: "No `static_metadata.cc:667` rejection in logcat; `Gcam.Create` succeeds; a file lands in DCIM at full resolution; image content is inspected to determine whether the HAL delivers remosaiced Bayer or raw Quad-Bayer."

That last clause is a second deliverable hiding inside the first. Project-Ontology `OQ-02` asks "Does the HAL deliver remosaiced Bayer or raw Quad-Bayer at 8192x6144?" with status open and evidence "never captured — no successful full-res RAW frame yet." Project-Comprehension `H-03` states the hypothesis as remosaiced Bayer, confidence `tentative`, with the probe "Capture one DNG once H-02 passes; inspect the CFA pattern."

The answer matters beyond curiosity. If the sensor delivers raw Quad-Bayer, every downstream consumer expecting a standard Bayer pattern will produce incorrect colour, and a capture that lands as a file is not the same as a capture that produces a correct image. This is the difference between the mechanism working and the feature working.

The known failure being tested against is exact. `agc-50mp-yama/hal-raw50-deneme.patch` records it verbatim: `libgcam static_metadata.cc:667 / frame_raw_max (8192x6144) matches neither the active area size (4096x3072) nor pixel array size (4096x3072)`. With `pixelArraySize` confirmed at 8192x6144 by Faz 3.3, the condition libgcam checks should now be satisfied. Should is doing work in that sentence, and this sub-phase is where it is tested.

## 2. Goal

Produce a full-resolution photograph taken with the AGC port, driven only by the QuickSettings tile, and establish from the image itself whether the HAL delivers remosaiced Bayer or raw Quad-Bayer at 8192x6144.

## 3. Description

The problem is the last gap between a metadata surface that looks correct and an application that actually completes a capture. Two things can still go wrong: libgcam may reject for a reason other than the one recorded, or it may accept and the capture may fail further along, as it already does with the application-level patch alone where the symptom is `Stuck shot … HDR_PLUS`.

It belongs last in the phase's experimental sequence because it depends on everything before it: a cleared preference state, a confirmed write site, and a consumer survey that has not raised a blocking finding.

The vibecoding slice strategy is layered by cost. The first useful slice is initialization only — open AGC and check the log for the rejection, without attempting a shutter. That single check answers whether the invariant is now satisfied and costs one application launch. The second slice is the capture attempt. The third is the image inspection that answers `OQ-02`. Separating them means a failure at the first layer does not consume the effort of the other two, and a success at the first layer is recorded as progress even if the second fails.

The fastest validation signal is the absence of the `static_metadata.cc:667` line in the log after an AGC launch. It is a single grep against a known string.

What should not be over-planned: image quality tuning, HDR behavior, or comparison against the stock camera's processing. Those are questions for after a capture completes at all.

Two operational hazards are documented and must be respected. Project-Ontology invariant 8 records the preference trap, and Faz 3.1's checklist applies to this sub-phase as much as to the earlier ones. Project-Ontology section 5 records that changing the APK signature requires uninstalling, and that data preservation requires a specific sequence ending in `chcon -R` with the parent context rather than `restorecon -R`, because the latter discards per-application security categories and the application then fails. If any APK reinstallation is needed during this sub-phase, that sequence is the one to follow.

There is also a known non-HAL cause of a stuck shutter worth ruling out early. Project-Comprehension section 4 lists among observed failure modes: "Stuck shutter (Gcam init failure, or a permission dialog holding focus, or HDR+ still initialising)." A permission dialog holding focus is trivially confused with a capture failure and should be eliminated before any deeper diagnosis.

## 4. Scope

- An AGC launch with a log check for the `static_metadata.cc:667` rejection and for `Gcam.Create` success or failure.
- A capture attempt at full resolution with the QuickSettings tile as the only switch, and no preference set.
- Confirmation that a file lands in the expected location at 8192x6144.
- Inspection of the captured image to determine the colour filter array pattern, answering `OQ-02` and `H-03`.
- Reproducibility: the capture is repeated to confirm it is not a single fortunate result.
- Elimination of the non-HAL stuck-shutter causes before any deeper diagnosis.
- Recording of the outcome against Project-Ontology invariant 6, since a success confirms the invariant's stated form and a failure refines it.
- If capture fails, a bounded diagnosis producing a symptom classification rather than an open investigation.

## 5. Out of Scope

- Image quality tuning, HDR behavior, or processing comparison against other applications.
- Narrowing the RAW emission or adding duration rows. Phase 4 owns those, and Main-Planing sequences them after this deliberately.
- Modifying the AGC port's smali beyond what is already applied, or building a new patched APK.
- Any change to the sensor layer, the mode dispatch, or the ten-mode surface.
- Composing 50 MP with LN modes, which is Phase 5 and is currently excluded by invariant 4.
- An unbounded diagnosis if capture fails. The diagnosis is bounded and its result routes to Faz 3.6.
- Consumer compatibility, which Faz 3.4 already covered.

## 6. Current Repository Evidence

`agc-50mp-yama/hal-raw50-deneme.patch` was read in this run and records the measured pre-change state completely: the experimental patch places `[37 8192 6144 OUTPUT]`, `[38 8192 6144 OUTPUT]`, and `[36 8192 6144 OUTPUT]` into `android.scaler.availableStreamConfigurations`, growing the array from 508 to 868 int32 entries; AGC sees this and `getImageReaderFormat` selects RAW10 at 8192x6144; and libgcam then rejects with the `static_metadata.cc:667` line. The header states plainly that this patch alone is insufficient and that the pixel array or the active array must be raised to match the raw resolution.

`agc-50mp-yama/README.md` was read in this run and documents the application-level patch: `getSupportedOutputSizes` is rewritten so that when `pref_48m_key` is non-zero the list comes from a new `allOutputSizes` method combining `getOutputSizes` and `getHighResolutionOutputSizes`, falling back to the former if the latter throws. The patch is gated behind `pref_48m_key`, so without that preference the APK behaves as stock. This is directly relevant: the capture path being tested here may be the HAL-driven one with no preferences at all, which the patch header describes as AGC selecting RAW10 8192x6144 unaided.

Project-Comprehension `EV-10` records that state as confirmed: "The four-instruction patch makes AGC select RAW10 8192x6144 unaided", evidenced by an AGC log line showing `getImageReaderFormat ... RAW10 8192x6144` with no preferences set.

`EV-05` records the current failure as confirmed: "AGC cannot yet complete a 50 MP capture", evidenced by "logcat `Stuck shot ... HDR_PLUS` plus the `static_metadata.cc:667` rejection".

Project-Ontology section 6 records the port's obfuscation map, which is what makes a deeper diagnosis feasible if needed: `Lhvg;` is ResolutionSetting, `Llvo;` is the hooked characteristics wrapper, `Lmip;->bs()` takes the maximum of a list, `Lmip;->bu()` converts a size array to a list, `Llig;->a` and `->b` are width and height, and `Llwp;->a` and `->b` are format and size.

`AGC8.4.300_V9.6_50MP_patched.apk` is at the workspace root and Autopsy section 3 records it as the currently installed build. `AGC8.4.300_V9.6_snap.apk` is the unpatched original and `AGC8.4.300_V14_snap.apk` is a second version, both present.

Autopsy section 4 records that both the experimental HAL patch and the APK patch are "currently reverted on the device", which is the state Faz 3.1's precondition check should confirm before this sub-phase changes it.

Project-Ontology section 6 records that logcat's 30 Hz `CAM_A: Can not update pitch roll indicator` spam rolled the buffer and hid evidence until the buffer was enlarged to 64 MB with tag filters applied. That operational detail applies directly to the log checks in this sub-phase.

## 7. Planned Work Breakdown

- F3.5-01 — Establish the capture-attempt state
  - Description: Confirm preferences are clear per Faz 3.1, the `pixelArraySize` patch is applied per Faz 3.3, the RAW emission patch is applied, and the mode is `50mp` set from the tile. Snapshot before anything else.
  - Output: A pre-attempt snapshot with all four conditions confirmed.
- F3.5-02 — Prepare the log capture
  - Description: Enlarge the log buffer and apply tag filters before launching, per the recorded operational detail, so the evidence is not lost to the known spam source.
  - Output: A log capture configuration that survives the attempt.
- F3.5-03 — Launch AGC and check initialization only
  - Description: Open the application without attempting a shutter. Check for the `static_metadata.cc:667` rejection and for `Gcam.Create` success. This is the cheapest decisive check in the phase.
  - Output: An initialization verdict.
- F3.5-04 — Eliminate the non-HAL stuck-shutter causes
  - Description: Confirm no permission dialog holds focus and that HDR processing has finished initializing before interpreting any shutter behavior.
  - Output: A cleared-causes verdict.
- F3.5-05 — Attempt the capture
  - Description: Take a photograph. Confirm whether a file lands and at what dimensions.
  - Output: A capture verdict with the file's dimensions.
- F3.5-06 — Confirm reproducibility
  - Description: Repeat the capture at least twice more, including once after a camera restart, so the result is established as reproducible rather than incidental.
  - Output: Additional capture verdicts.
- F3.5-07 — Inspect the image for the colour filter pattern
  - Description: Examine the captured file to determine whether the pattern is standard Bayer or Quad-Bayer, answering `OQ-02` and resolving `H-03`.
  - Output: A pattern determination with the evidence used.
- F3.5-08 — Record the invariant outcome
  - Description: Update Project-Ontology invariant 6 with the result. A success confirms the invariant as stated; a failure means the requirement is more complex than the recorded form and the refinement is itself valuable.
  - Output: An updated invariant record.
- F3.5-09 — Bounded diagnosis on failure
  - Description: If capture fails, classify the symptom against the known failure modes and stop at the bound. Route the result to Faz 3.6 rather than continuing to investigate.
  - Output: A symptom classification and a routing decision.

## 8. Acceptance Criteria

- The pre-attempt snapshot confirms clear preferences, both patches applied, and mode `50mp` set from the tile.
- The log capture is configured before the launch, so the initialization evidence exists regardless of outcome.
- The initialization check produces an explicit verdict on the `static_metadata.cc:667` rejection and on `Gcam.Create`.
- The non-HAL stuck-shutter causes are eliminated before any shutter behavior is interpreted.
- If capture succeeds, a file exists at 8192x6144 and the result is reproduced at least twice more, including once after a camera restart.
- The tile is the only switch used; no preference is set at any point, which is what makes the result a HAL-driven success rather than an application-configured one.
- `OQ-02` is answered with the colour filter pattern determined from the image, and `H-03` is updated.
- Project-Ontology invariant 6 is updated with the outcome, whether it confirms or refines the recorded form.
- If capture fails, the symptom is classified against the known failure modes and routed to Faz 3.6 without an open-ended investigation.

## 9. Validation and Test Approach

Validation is live, log-driven, and artifact-driven. This is the one sub-phase whose primary evidence is a produced file rather than a reported state.

- `VAL-SMOKE` (from Faz 2.1) — the pre-attempt and post-attempt bracket.
- `VAL-LOG` (proposed) — a filtered log check for the `static_metadata.cc:667` string, for `Gcam.Create`, and for `Stuck shot`. Filtered and buffered per the recorded operational detail so evidence survives.
- `VAL-CAPTURE` (proposed) — the produced file's existence and dimensions, plus reproduction across at least three attempts including one after a camera restart.
- `VAL-IMAGE` (proposed) — inspection of the captured file's colour filter pattern, which answers `OQ-02`.
- `VAL-MANUAL` (proposed) — the shutter press and the visual confirmation, the user's actions.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist, applied here as it is to every Phase 3 measurement.

Local versus live: entirely live for capture; the image inspection is host-side once the file is retrieved. Security validation is not applicable. Ontology validation is central — invariants 6 and 8 are both exercised, and `OQ-02` is closed.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Pre-attempt and post-attempt state confirmation. | VAL-SMOKE, VAL-PRECOND |
| agc-50mp-yama/hal-raw50-deneme.patch | existing | The RAW emission patch that must be applied alongside the pixel array change. | VAL-SMOKE |
| agc-50mp-yama/hal-pixelarray-deneme.patch | existing | The confirmed pixel array patch from Faz 3.3. | VAL-SMOKE |
| Planner-docs/Project-Ontology.md | modified | Close `OQ-02` and record the invariant 6 outcome. | VAL-IMAGE, VAL-LOG |
| Planner-docs/Project-Comprehension.md | modified | Resolve `H-03` and update `EV-05` from the measured result. | VAL-IMAGE, VAL-CAPTURE |

## 10. Dependencies and Sequencing

Depends on Faz 3.3 for a confirmed and applied `pixelArraySize` patch, on Faz 3.4 for a consumer survey with no blocking finding, and on Faz 3.1 for the preference precondition and the per-measurement checklist.

Blocks nothing inside Phase 3 except Faz 3.6, which consumes its outcome. Feeds Phase 4 substantially: Faz 4.1's narrowing must preserve whatever made the capture work, so a success here defines what Phase 4 must not break.

Feeds Phase 5 conditionally. Main-Planing section 9 lists among decisions needing human confirmation: "Whether Phase 5 still has priority given how much Phase 3 has grown." The outcome here is the main input to that decision.

Required human actions: the shutter press, the visual confirmation, and the judgment about image content. Every capture is the user's action.

Required infrastructure: the device, the AGC build, both HAL patches applied, and a means of retrieving the captured file for inspection.

Required approvals: running the user's camera application in a patched state and taking photographs with it.

Fresh session token and context risk: medium to high. Log output is the main hazard, which is why F3.5-02 configures filtering before the launch rather than after. Unfiltered log capture on this device is documented as producing 30 Hz spam.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: libgcam still rejects, for a reason other than the recorded one. Impact: the phase's central hypothesis is wrong and the fallback options become live. Mitigation: F3.5-03 checks initialization before any capture effort, so the answer arrives at the lowest possible cost, and F3.5-08 treats a refined invariant as a valuable outcome rather than a failure.
- Risk: the log evidence is lost to the documented 30 Hz spam. Impact: a failure with no diagnosable trace, and the attempt has to be repeated. Mitigation: F3.5-02 configures the buffer and filters before the launch, using the setting already recorded as sufficient.
- Risk: a stuck shutter is attributed to the HAL when the cause is a permission dialog or unfinished HDR initialization. Impact: exactly the misattribution pattern this phase is built to prevent. Mitigation: F3.5-04 eliminates those causes before any interpretation.
- Risk (invariant 8): a preference is set at some point during the attempts and contaminates a result. Impact: a correct configuration is recorded as failing. Mitigation: `VAL-PRECOND` applies per attempt and the pre-attempt snapshot confirms the state.
- Risk: a single successful capture is reported as the milestone. Impact: an incidental success is mistaken for a working feature, and the regression appears later. Mitigation: F3.5-06 requires reproduction across at least three attempts including one after a camera restart.
- Risk (`OQ-02` realized): the capture completes but delivers raw Quad-Bayer, producing incorrect colour. Impact: the mechanism works and the feature does not. Mitigation: F3.5-07 makes the pattern determination a required output rather than an optional follow-up, so this cannot be discovered after the milestone is declared.
- Risk: a capture failure triggers an open-ended debugging session. Impact: the budget set in Faz 3.1 is consumed here rather than reserved for the decision gate. Mitigation: F3.5-09 bounds the diagnosis to a symptom classification and routes to Faz 3.6.
- Risk: an APK reinstall becomes necessary and the security context is restored with the wrong command. Impact: the application fails afterward, per the recorded finding about per-application categories. Mitigation: the description names the correct sequence and the incorrect one explicitly.

## 12. Desired End State

Either the project's headline milestone exists — a reproducible full-resolution photograph taken with AGC, driven by the tile alone, with no preference set, and with the colour filter pattern determined — or the attempt has produced a precisely classified failure that refines Project-Ontology invariant 6 and hands the decision gate a concrete result.

The evidence an implementer should produce is the pre-attempt snapshot, the filtered initialization log, at least three capture verdicts with dimensions, the colour filter pattern determination, and the updated invariant record.

The ledger summary Step 4 should append records: whether initialization succeeded, whether capture completed and reproduced, the file dimensions, the `OQ-02` answer, the invariant 6 outcome, and whether Faz 3.6 is being invoked.

## 13. Next Sub-Phase Transition Criteria

- The initialization verdict is explicit on both the rejection line and `Gcam.Create`.
- If capture succeeded, it is reproduced at least three times including once after a camera restart.
- `OQ-02` is answered from the image, not inferred.
- Project-Ontology invariant 6 carries the outcome, confirming or refining its recorded form.
- No preference was set at any point during the attempts.
- If capture failed, the symptom is classified and routed to Faz 3.6 without an open investigation.
- Phase 4 has a clear statement of what its narrowing must preserve.
