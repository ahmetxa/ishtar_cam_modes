# Faz 3.4 — Consumer Compatibility Check

## 1. Context

Project-Ontology `OQ-03` asks the question this sub-phase answers: "Can `pixelArraySize` be raised without breaking other consumers?" Status: open. Evidence: "untested; the opposite direction (active array) is known to break AGC (Faz 4)."

That parenthetical is the whole reason this sub-phase exists as its own slice. The project has already changed one of the two array values and broken a consumer. Main-Planing Phase 3's risk note records it: "the fallback is to raise the active array instead — but Faz 4 already showed that direction breaks AGC when raw is not raised with it." Project-Ontology invariant 6 generalizes it: the Faz 4 wide patch raised the active array without raising raw; the Faz 12 RAW patch raised raw without raising the array; both violated the same libgcam requirement from opposite directions.

There is no prior evidence about what raising `pixelArraySize` does to consumers other than AGC, and `pixelArraySize` is not an obscure tag — the Android camera framework and applications that compute crop factors, field of view, or sensor-relative coordinates read it. A value that is physically correct can still be behaviorally disruptive if other code was written against the previously reported value.

Project-Comprehension `H-02` bundles this concern into its probe: "patch one word, read `dumpsys` for tag `f0006`, then open the stock camera app before touching AGC." Faz 3.3 performs the stock camera open as a minimal health check. This sub-phase widens that check into an actual survey, because a preview appearing is a much weaker signal than a set of applications behaving correctly.

Main-Planing's target end state names the outcome that depends on this: "Video at 1080p60 and 4K60 is unaffected in every mode", which Project-Ontology records as invariant 5 and which is a standing user-validated acceptance criterion.

## 2. Goal

Determine whether the confirmed `pixelArraySize` change breaks any camera consumer other than the one it was made for, covering the stock camera application, the third-party application already proven at full resolution, and the video path — before the change is carried into a shipped patch.

## 3. Description

The problem is blast radius. Project-Comprehension `QAS-04` states it as a quality scenario: "the 50 MP HAL patch ships and breaks an application the user has not tested … the patch is intended for distribution", and concludes that narrowing wins over shipping broad. Narrowing is Phase 4's work, but knowing what breaks is this sub-phase's, and the two answer different halves of the same concern.

It belongs between the metadata proof and the AGC capture for an ordering reason that is easy to get wrong. The temptation after Faz 3.3 confirms the write site is to go straight to the AGC capture, because that is the goal. But if the change breaks Open Camera or the video path, that is a finding which changes what Phase 4 must do, and discovering it after a successful AGC capture would mean the celebrated result came with an unmeasured cost.

The vibecoding slice strategy: the first useful slice is the two consumers with the strongest prior evidence — the stock camera application and Open Camera, which Project-Comprehension `EV-04` records at 50.3 MP with confidence `confirmed`. Those two give the fastest signal because their expected behavior is documented. The second slice is the video path, which is slower and needs the user. The fastest validation signal is Open Camera still reporting and delivering full resolution, because that consumer is known to read both size lists and is therefore sensitive to the exact metadata surface being changed.

What should not be over-planned: an exhaustive application survey. Three consumers with documented prior behavior are worth more than ten with none, because only the documented ones support a before-and-after comparison.

The comparison baseline is the Faz 2.2 named snapshot plus the Faz 2.3 regression record. Those exist precisely so a question like this one can be answered by diff rather than by recollection.

## 4. Scope

- The stock camera application: opens, preview is live, shutter completes, and the resulting image has plausible dimensions.
- Open Camera: full-resolution capture still produces the measured 50.3 MP result, since `EV-04` establishes the expected value.
- The video path: 1080p60 and 4K60 record and play back, testing Project-Ontology invariant 5.
- The ten-mode surface: a spot check that the sensor-layer modes still switch and open, since the HAL change is layer-independent in principle and this verifies it is so in practice.
- Field-of-view and crop behavior: whether any consumer's framing visibly changed, since `pixelArraySize` is an input to crop computation.
- Comparison against the Faz 2.2 baseline and the Faz 2.3 regression record rather than against recollection.
- Resolution of `OQ-03` with the consumers actually tested named, so the answer's scope is honest.

## 5. Out of Scope

- Any AGC or Gcam interaction. Faz 3.5 owns that entirely, and mixing it in here would defeat the ordering this sub-phase exists to enforce.
- Image quality assessment beyond dimensions and obvious framing changes.
- Narrowing the RAW emission or adding duration rows, which are Phase 4.
- A survey of applications with no documented prior behavior.
- Fixing any incompatibility discovered. A finding is recorded and routed; the response is decided with the Phase 4 scope in view.
- Long-run or thermal stability testing.
- Any change to the sensor blobs or to the ten-mode dispatch.

## 6. Current Repository Evidence

Project-Comprehension `EV-04` records "50 MP works for third-party applications", confidence `confirmed`, evidenced by "on-device Open Camera capture measured at 50.3 MP (journal Faz 8)". This is the strongest documented consumer expectation available and is why Open Camera anchors the survey.

`OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk` is present at the workspace root, so the tested build is on hand.

`ishtar-cam-modes/halpatch.sh` records why Open Camera is the sensitive consumer. Its header states that the stock HAL advertises 50 MP only under the `org.codeaurora.qcamera3.quadra_cfa` vendor tag, that third-party applications look at the standard list and therefore cannot see it, and that without the patch Open Camera silently drops to 12.6 MP even when its menu offers 50 MP. The application reads the metadata surface closely enough that a change to it is likely to show.

The same file records the prior consumer breakage explicitly: raising `activeArraySize` to 8192x6144 crashes AGC with a null pointer exception in `Gcam.f()`, "verified with six variants", and states that the narrow patch opens 50 MP while keeping AGC alive. That is direct evidence that array metadata changes have consumer-visible effects, from the project's own history.

`ishtar-cam-modes/setmode.sh` defines `CAM_APPS="org.codeaurora.snapcam com.android.camera com.xiaomi.module.evaluation"` and comments that `com.xiaomi.module.evaluation` is the Open Camera build capable of 50 MP capture. This gives the survey its package identifiers.

Project-Ontology invariant 5 records the video requirement as standing and user-validated. `module.prop` v2.0 states that video at 1080p60 and 4K60 is unaffected by the full-resolution patch, which establishes the pre-change expectation for the video half of the survey.

Project-Ontology invariant 7 records that `getOutputSizes` excludes sizes whose minimum frame duration exceeds one twentieth of a second, with 8192x6144 measured at 66,666,666 nanoseconds and 4096x3072 at 33,333,333. Open Camera reaches full resolution because it reads both lists. This mechanism is unchanged by a `pixelArraySize` patch, which gives the survey a prediction to test: Open Camera should be unaffected. A result contradicting that prediction would be significant.

## 7. Planned Work Breakdown

- F3.4-01 — Establish the pre-change consumer expectations
  - Description: Record, from the Faz 2.2 baseline and the Faz 2.3 regression record, what each surveyed consumer did before the change. A comparison needs both sides, and the earlier side already exists.
  - Output: A pre-change expectation table for the three consumers plus the mode surface.
- F3.4-02 — Survey the stock camera application
  - Description: Open, preview, shutter, and check the resulting image dimensions and framing. Compare against the pre-change expectation.
  - Output: A stock camera verdict.
- F3.4-03 — Survey Open Camera at full resolution
  - Description: Capture at full resolution and confirm the result still measures at the documented 50.3 MP. This is the highest-signal check in the sub-phase.
  - Output: An Open Camera verdict with the measured resolution.
- F3.4-04 — Survey the video path
  - Description: Record 1080p60 and 4K60 and confirm playback, in stock and in at least one modified mode. Tests invariant 5.
  - Output: Four video verdicts.
- F3.4-05 — Spot check the mode surface
  - Description: Switch through at least one mode per layer and confirm the camera opens, verifying the HAL change did not disturb the sensor layer.
  - Output: A mode surface verdict.
- F3.4-06 — Assess framing and crop behavior
  - Description: Compare framing between a pre-change and post-change capture from the same position where practical. A visible field-of-view change would indicate a consumer computing crop from the patched tag.
  - Output: A framing assessment, with its limitations stated if a controlled comparison was not possible.
- F3.4-07 — Resolve the consumer question
  - Description: Answer `OQ-03` with the consumers actually tested named, so the answer does not claim more coverage than it has.
  - Output: An updated ontology question with a scoped answer.
- F3.4-08 — Route any incompatibility
  - Description: For each break found, record the consumer, the symptom, and whether it argues for narrowing the patch, reverting the approach, or accepting the cost. Route to Phase 4 or to Faz 3.6.
  - Output: A findings list with routing.

## 8. Acceptance Criteria

- Each of the three named consumers has a recorded verdict compared against a documented pre-change expectation.
- Open Camera's post-change resolution is measured and stated numerically, not described as unchanged.
- Video records and plays at both profiles in at least two modes.
- The mode surface spot check confirms at least one sensor-layer mode and the HAL-layer mode still open the camera.
- The framing assessment states its own limitations if a controlled comparison was not achieved.
- `OQ-03` in Project-Ontology no longer reads `open`, and its answer names the consumers tested rather than claiming general compatibility.
- Every incompatibility found has a finding with a symptom and a routing decision.
- No AGC interaction occurred during this sub-phase.
- The device state at the end is recorded, patched or reverted.

## 9. Validation and Test Approach

Validation is live and comparative, with a heavy manual component. Autopsy's Gate 3 applies in full: this is user-performed verification with an explicit checklist.

- `VAL-SMOKE` (from Faz 2.1) — state confirmation before the survey and after, so the survey's own effects on state are visible.
- `VAL-MANUAL` (proposed) — the consumer checklist: stock camera open, preview, shutter, dimensions; Open Camera full-resolution capture with a measured result; video at both profiles with playback. The user is the actor throughout.
- `VAL-COMPARE` (proposed) — comparison of each verdict against the Faz 2.2 baseline and the Faz 2.3 regression record, which is what makes a verdict evidence rather than an impression.
- `VAL-DOCS` (proposed) — read back the resolved `OQ-03` and confirm its scope statement matches the consumers actually tested.

Local versus live: entirely live. Security validation is not applicable. Ontology validation applies to invariants 5 and 7, both of which this survey exercises.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | State confirmation bracketing the survey. | VAL-SMOKE |
| docs/regression-v2.1.md | existing | The pre-change expectation source for the mode surface and video checks. | VAL-COMPARE |
| ishtar-cam-modes/setmode.sh | existing | Read-only context: the camera package identifiers used in the survey. | VAL-MANUAL |
| Planner-docs/Project-Ontology.md | modified | Resolve `OQ-03` with the tested scope named. | VAL-DOCS |
| docs/consumer-survey.md | proposed | The survey record with per-consumer verdicts and comparisons. | VAL-COMPARE, VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 3.3 for a confirmed write site and a device held in the patched state. Depends on Faz 2.2 for the baseline and Faz 2.3 for the regression record, both of which supply the pre-change side of every comparison.

Blocks Faz 3.5 by design rather than by necessity. The AGC capture could technically run first, and the reason it does not is stated in the description: a successful capture would make an unmeasured consumer cost easy to overlook.

Feeds Phase 4 directly. If the survey shows breakage, that constrains what Faz 4.1's narrowing must achieve, and the finding should reach Phase 4 before its scope is fixed.

Required human actions: every check in this sub-phase. It is entirely user-performed and should be scheduled accordingly.

Required infrastructure: the device, the Open Camera build, and storage for video recordings.

Required approvals: the user's willingness to run their camera in a patched state through several applications.

Fresh session token and context risk: low to medium. The outputs are verdicts rather than dumps. The risk is session length rather than context volume, since the survey involves waiting on the user.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the survey runs after a successful AGC capture and its findings are discounted. Impact: a known consumer break ships because the headline result overshadowed it. Mitigation: the sequencing places this before Faz 3.5, and the out-of-scope section forbids AGC interaction here.
- Risk (`OQ-03` realized): raising `pixelArraySize` breaks a consumer that reads it for crop computation. Impact: the chosen side of the invariant is as problematic as the other side, and the project has no third option. Mitigation: F3.4-06 assesses framing specifically, and F3.4-08 routes the finding to Faz 3.6 where the fallback options include accepting the application-level patch instead.
- Risk: Open Camera is tested without measuring the result, and "it still works" is recorded. Impact: a silent drop from 50.3 MP to a lower resolution goes unnoticed, which is exactly the failure `halpatch.sh` documents happening without the patch. Mitigation: the acceptance criteria require a numeric measurement.
- Risk (invariant 5): video is deferred because it is slow, and a standing acceptance criterion goes unverified. Impact: a video regression ships. Mitigation: F3.4-04 is scoped to four recordings, which keeps it affordable.
- Risk: the framing comparison is uncontrolled and produces an ambiguous verdict. Impact: a real field-of-view change is dismissed as measurement noise. Mitigation: the acceptance criteria require the assessment to state its own limitations rather than assert a clean result.
- Risk: `OQ-03` is answered as a general "yes" from three consumers. Impact: a scoped result is recorded as an unscoped fact and misleads later work. Mitigation: F3.4-07 requires the answer to name the tested consumers.
- Risk: the survey's own application launches change device state in ways that confuse the following sub-phase. Impact: Faz 3.5 starts from an unknown position. Mitigation: `VAL-SMOKE` brackets the survey and the end state is recorded.

## 12. Desired End State

The consumer impact of the confirmed `pixelArraySize` change is measured rather than assumed, across the stock camera application, Open Camera at full resolution, the video path at both profiles, and the mode surface. Each verdict is compared against a documented pre-change expectation. `OQ-03` is answered with its scope stated honestly, and any incompatibility is a routed finding that reaches Phase 4 before Phase 4's scope is fixed.

The evidence an implementer should produce is the pre-change expectation table, the per-consumer verdicts with Open Camera's numeric result, the four video verdicts, and the framing assessment with its limitations.

The ledger summary Step 4 should append records: which consumers were surveyed, the measured Open Camera resolution, whether invariant 5 held, the `OQ-03` answer and its scope, and any finding routed to Phase 4.

## 13. Next Sub-Phase Transition Criteria

- All three consumers plus the mode surface have recorded verdicts with comparisons.
- Open Camera's resolution is a measured number.
- Video at both profiles is confirmed in at least two modes.
- `OQ-03` is answered with its tested scope named.
- Any incompatibility is routed, and Phase 4's scope has not been fixed while an unrouted one exists.
- No AGC interaction has occurred, leaving Faz 3.5 a clean single-variable experiment.
