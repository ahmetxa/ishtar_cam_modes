# Faz 3.9 — Coexistence Bracket: AGC at 12.58 MP and Open Camera at 50.3 MP in One HAL State

## 1. Context

**Amended 2026-09-05 by planning run 13 (`AUDIT-FIX-26`, discharged against `IMPL-53` and `IMPL-54`; `AUDIT-FIX-29`'s `DEC-15` residue cleared here).** `F3.7-10` has reported and `Faz3.7` is `verified`. Two corrections and one definition follow, and nothing else in this file was rewritten.

**The definition, which rescues the rest of the file.** Throughout this sub-plan "the pin" now means the **configured derivation** — `pref_48m_key`=`0` together with `pref_camera_resolution`=`full`, which on the shipped `fullres` base derives `pref_camera_picturesize_back_key`=`4096x3072` — and **not** a direct write to the derived key, which `IMPL-52` measured does not survive an AGC restart. Every remaining occurrence of "the pin" and of "pinned `4096x3072`" in this file is to be read in that sense; the observable it names is unchanged, only its mechanism is. `DEC-18` (2026-09-04) adopted `0` as the phase's configured state, so the session runs at that value rather than establishing it.

**The two corrections.** (1) `DEC-15` **was answered on 2026-09-04** — the shipped `fullres` artifact `fe0245a4720fb07b01d96deef47f5569` — and `IMPL-53` transitioned the device onto it with the revert path exercised; sections 10 and 11 no longer describe it as an open precondition. (2) The out-of-scope bullet "Turning `pref_48m_key` on" rested on a premise `IMPL-52` measured false: the key was already **on** when that bullet was written. It now reads correctly against the adopted state. **`FIND-3.7-03` is new input for this sub-plan:** `pref_camera_picturesize_front_key` re-derives across a base change too (`6528x4896` to `3264x2448`, `IMPL-54`), so a session that opens either app on the **front** camera is not covered by this sub-plan's rear-camera evidence.

`DEC-14`'s replacement objective has two halves and this sub-plan proves the second one. `Main-Planing.md` section 4 states it: "In 50 MP mode, Open Camera produces a full-resolution image using the sensor's native 8192x6144 array, **and the AGC 8.4.300 V9.6 port keeps working normally at 12.58 MP (`4096x3072`) — it launches, previews, captures, and saves a clean image, in the same HAL state, without a crash or a corrupt frame.**"

The phrase carrying the work is **in the same HAL state**. Each half is already on record separately. `IMPL-22` measured Open Camera at 50.3 MP; `IMPL-40` measured a clean AGC 12.58 MP capture; `IMPL-15` even had both layers mounted simultaneously with Open Camera clean at 8192x6144. What has never been recorded is the two consumers measured **against one another in a single bracketed session with no HAL change between them**, which is the only form of evidence that supports the word "coexistence".

The distinction matters because this project has already been misled by results assembled from separate sessions. Autopsy `AUTOPSY-P0-02` records a three-step misattribution caused by state not being captured before and after changes, and `IMPL-40`'s own value came from a single log that happened to hold two sessions — the run says so explicitly: "The ring buffer still held `IMPL-35`'s session, so both are measured from one log and one device state." That was luck. This sub-plan makes it method.

`Faz3.7` establishes the pin and the clean AGC capture. `Faz3.8` makes the pin visible in a snapshot. This sub-plan uses both and adds the second consumer.

## 2. Goal

Demonstrate in one bracketed device session, with the HAL md5 identical at both ends and unchanged in the middle, that AGC saves a clean 12.58 MP image and Open Camera saves a clean 50.33 MP image — with both results measured on the pulled originals by the same method, and with the camera enumeration and the trap state unchanged throughout.

## 3. Description

The problem is that "coexistence" is a claim about a single state, and every piece of supporting evidence the project holds is a claim about a different state. Assembling them is inference; measuring them together is not.

It belongs third in the phase because it needs the pin (`Faz3.7`) and benefits enormously from the instrument (`Faz3.8`), and because it is the last sub-plan that establishes the state — `Faz3.10` then attacks that state to see whether it survives. Proving the state exists before testing whether it persists is the natural order and it is also the cheaper one, since a state that cannot be established at all needs no durability testing.

**The vibecoding slice strategy.** The first useful slice is the AGC half repeated from `Faz3.7` under a fresh bracket, which costs almost nothing and re-establishes the starting point. The second is the Open Camera capture in the same session with no intervening change, and the third is the closing bracket. The fastest validation signal is the comparable-region diff between the opening and closing snapshots: if the HAL md5, mount counts, camera rows, trap count and photo-size pin are all identical across a session that produced two captures, the word "same HAL state" is earned rather than asserted.

**What must not be over-planned.** Not a general consumer survey. `Faz3.4` already did that and is `verified` — stock camera, 1080p60, 4K60, `dcgA`, `50mp`, plus a controlled framing comparison, recorded in `docs/consumer-survey.md`. This sub-plan is narrow on purpose: two consumers, one state, one session. Widening it back into a survey would duplicate finished work and dilute the one property being established.

**Two known conditions are inputs, not tasks.** `FIND-2.3-02` records that `ln2` and `ln4` crash AGC, so the sensor layer for this session is whatever the chosen 50 MP state implies — and invariant 4 records that selecting `50mp` forces the sensor layer to stock, so the composed cases are not reachable here anyway. `FIND-2.3-03` records that AGC's video section is black in plain `stock` with sensor and HAL unmodified, so it is **not** module-caused and is **not** this sub-plan's to fix; if the video path is exercised at all, it is exercised through Open Camera, and the AGC video state is recorded as the standing condition it is.

## 4. Scope

- One continuous bracketed device session containing both captures, with an opening and a closing `scripts/smoke.sh` snapshot.
- The AGC capture at the pinned `4096x3072`, with the configured stream read from `dumpsys media.camera` while AGC is open.
- The Open Camera capture at `8192x6144`, with its configured stream read the same way while Open Camera is open.
- Measurement of both pulled originals by the `IMPL-40` method — PIL, grayscale, threshold < 4 — reporting dimensions, megapixels, and black fraction for each.
- Confirmation that the HAL md5, both mount counts, the mode, the camera enumeration count, the trap key count and the photo-size pin are identical in the opening and closing snapshots.
- An explicit statement of the sensor-layer state during the session and why it is what it is, given invariant 4.
- A record of AGC's launch behaviour: whether it launched first try, and whether any `gcam.Gcam.f()` NPE or `DefaultErrorActivity` appeared in the crash buffer.
- The standing conditions recorded rather than re-diagnosed: `FIND-2.3-03` (AGC video black in stock too) and any `Invalid mesh` or SABRE lines, which `IMPL-40` established are present alongside clean captures and are therefore not signals.

## 5. Out of Scope

- Any HAL change during the session. The whole point is that nothing changes between the two captures; a session that required a HAL change to satisfy both consumers has falsified the coexistence claim and must be reported as such rather than repaired.
- Re-running `Faz3.4`'s consumer survey. Stock camera, 1080p60, 4K60 and the framing comparison are `verified` and are not redone.
- Diagnosing `FIND-2.3-03` (AGC video black). It reproduces in plain `stock` and is not module-caused; it is recorded, not investigated.
- Diagnosing `FIND-2.3-02` (`ln2`/`ln4` crash AGC). Those modes are not reachable in a `50mp` state under invariant 4.
- Any attempt to make AGC capture above 12.58 MP, in any form. `DEC-14` retired that objective.
- Moving `pref_48m_key` off its adopted value of `0` (`DEC-18`). Its value is recorded in every result; changing it is `Faz3.10`'s negative control and `Faz3.8`'s sensitivity stimulus, not this sub-plan's business. **The original bullet read "Turning `pref_48m_key` on", which rested on a premise `IMPL-52` measured false — the key was already `1` at the time it was written.**
- Testing survival across reboot, mode switch, cold start or camera-stack restart. That is `Faz3.10` in full.
- Extending the smoke script. `Faz3.8` owns it.

## 6. Current Repository Evidence

`IMPL-22` / `Faz3.4` recorded Open Camera capturing **8192x6144 = 50.3 MP** on the fullres base with `f0006` raised, alongside a stock-camera pass, 1080p60 and 4K60 passes, and a controlled fixed-position comparison showing no field-of-view change. Its own scope statement is the reason this sub-plan is narrow: "Scope is three applications, two video profiles and two of ten modes — **not** a general compatibility claim."

`IMPL-15` / `Faz5.2` recorded the first simultaneous two-layer state on this device: sensor at the mode-0 12-bit candidate with the HAL at `fullres`, mount counts 1/1, "AGC opened (`CameraLauncher`, no `DefaultErrorActivity`, empty crash buffer), live preview confirmed visually, no `CONFIG failed`; OpenCamera captured **8192x6144 / 50.3 MP** with no corruption." That run demonstrates the session shape this sub-plan uses, and it also demonstrates the failure mode it must avoid: AGC's health there was established by opening and looking, not by a measured capture.

`IMPL-40` recorded the clean AGC reference — `3072x4096`, 12.58 MP, black fraction **0.0024** — and, in the same run, that the full 15 `MapFrameToTexture` SABRE failures and two `Invalid mesh: [4096,3072]` lines were present **alongside** the clean image. Both are therefore standing conditions and neither is a defect signal. That correction is an input here so the session does not stop on a log line that means nothing.

`IMPL-49` recorded AGC launching cleanly on the broad table — "launches at stage A (1/1, 2/2, 4/4 across two sessions)" — which is the launch behaviour this session expects, and `IMPL-50` recorded "13 camera devices back on every restart", which is the enumeration figure this sub-plan checks.

Project-Ontology invariant 4 records that `50mp` forces the sensor layer to stock, enforced at `post-fs-data.sh:16-18` and `setmode.sh:177-192`, verified bracketed in `IMPL-13`. Invariant 3 records the client-before-HAL restart ordering as an invariant, not a preference.

`OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk` is present at the workspace root and is the Open Camera build this project has measured with; invariant 7 records why it reaches 50.3 MP unaided — it reads both `getOutputSizes` and `getHighResolutionOutputSizes`, and the 8192x6144 entry at 66,666,666 ns lands only in the second.

`docs/consumer-survey.md` from `Faz3.4` is the existing record this sub-plan's result sits beside rather than replaces.

## 7. Planned Work Breakdown

- F3.9-01 — Establish and bracket the session's starting state
  - Description: Confirm the HAL md5 is `fe0245a4720fb07b01d96deef47f5569` (the base `DEC-15` selected), the mode is the 50 MP state, the trap count is 0/12, and enumeration is 13. Confirm the pin by reading **all three** of its keys, not only the last one: `pref_48m_key`=`0` and `pref_camera_resolution`=`full` are the inputs, and `pref_camera_picturesize_back_key`=`4096x3072` is what they derived at the last AGC start. Reading only the derived key would pass on a stale value that the next AGC start would overwrite. Take the opening snapshot.
  - Output: A named opening bracket with every value it will be compared against.
- F3.9-02 — Record the sensor-layer state and its reason
  - Description: State which sensor blob is live and why, citing invariant 4's forcing rule rather than describing the value as a choice.
  - Output: A one-line sensor-layer attribution.
- F3.9-03 — AGC capture and stream read
  - Description: Launch AGC, confirm it reached preview with no `DefaultErrorActivity` and an empty crash buffer, read `dumpsys media.camera` while it is open, take one capture, and pull the original.
  - Output: The configured stream lines, the launch verdict, and the pulled AGC original.
- F3.9-04 — Open Camera capture and stream read
  - Description: Without changing the HAL, the mode, the mounts, or any preference, launch Open Camera, read `dumpsys media.camera` while it is open, take one capture at full resolution, and pull the original.
  - Output: The configured stream lines and the pulled Open Camera original.
- F3.9-05 — Measure both originals by one method
  - Description: Run the `IMPL-40` measurement on both files: dimensions, megapixels, black fraction. Using one method for both is what makes the two numbers comparable to each other and to the historical references.
  - Output: Two measured triples.
- F3.9-06 — Close and diff the bracket
  - Description: Take the closing snapshot and diff the comparable regions. Enumerate every differing line and account for it; an unaccounted difference is a finding.
  - Output: A diff verdict with the differing lines named and explained.
- F3.9-07 — Record the standing conditions observed
  - Description: Note the SABRE failures, `Invalid mesh` lines, and AGC video-section state if observed, explicitly as standing conditions with their prior evidence cited, so a future reader does not treat them as new.
  - Output: A short standing-conditions note attached to the result.
- F3.9-08 — Write the coexistence result
  - Description: State the claim in the form the objective uses — both consumers, one HAL state, measured — with both md5s and both measured triples.
  - Output: A result an unrelated reader can check without re-running it.

## 8. Acceptance Criteria

- The HAL md5 in the opening and closing snapshots is identical, and no HAL write occurred during the session.
- The AGC original measures 12.58 MP with a black fraction comparable to `IMPL-40`'s 0.0024 reference, under the threshold `Faz3.7` stated in advance.
- The Open Camera original measures `8192x6144` = 50.33 MP and is clean by the same measurement, with its own pass threshold stated before the capture.
- Both captures are from the same continuous session, evidenced by one opening and one closing bracket with nothing between them but the two captures.
- `dumpsys media.camera` shows AGC configured at `4096 x 3072` and Open Camera configured at `8192 x 6144`, each read while its app is open.
- AGC launched without a `DefaultErrorActivity` and with no `gcam.Gcam.f()` NPE in the crash buffer.
- The camera enumeration is 13 devices, and the trap key count is 0/12, in both brackets.
- Every line differing between the opening and closing comparable regions is named and accounted for.
- The sensor-layer state is stated with its reason, citing invariant 4.
- The standing conditions are recorded as standing conditions, with their prior evidence cited, not as new observations.

## 9. Validation and Test Approach

Validation is live and comparative. The distinguishing property is that the *session* is the unit of evidence, not the capture — two good captures from two sessions would satisfy no criterion here.

- `VAL-SMOKE` (from Faz 2.1, extended by Faz 3.8) — the opening and closing brackets, whose comparable regions now include the photo-size pin.
- `VAL-DUMPSYS` (from Faz 3.7) — per-stream `Consumer name` and `Dims` lines read with each app open.
- `VAL-ARTIFACT` (from Faz 3.7, method fixed by `IMPL-40`) — PIL, grayscale, threshold < 4, on both pulled originals.
- `VAL-LAUNCH` (proposed) — AGC's launch verdict read from `dumpsys window` focus plus `logcat -b crash`, the method `IMPL-49` and `IMPL-50` used to drive launch/crash verdicts over `adb`.
- `VAL-PRECOND` (from Faz 3.1) — the eight-item per-measurement checklist, run once for the session rather than once per capture, since the session is the single variable.

Local versus live: only the artifact measurement is host-side. Live readiness is what this sub-plan establishes; it does not establish distribution readiness, which is `Faz4.4`'s. Security validation is not applicable. Ontology validation: invariant 4's forcing rule is observed rather than assumed, and invariant 3's restart ordering is not exercised here — `Faz3.10` exercises it.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | The opening and closing brackets, including the `Faz3.8` fields. | VAL-SMOKE |
| snapshots/ | generated | Both brackets, both pulled originals, and the measurement record. | VAL-SMOKE, VAL-ARTIFACT |
| docs/consumer-survey.md | existing | `Faz3.4`'s consumer reference, cited beside this result rather than rewritten. | VAL-DOCS |
| docs/phase3-preconditions.md | existing | The per-measurement checklist. Read, not edited. | VAL-PRECOND |
| Planner-docs/Planing-Ledger.md | modified | The coexistence result with both md5s and both measured triples. | VAL-PRECOND |

## 10. Dependencies and Sequencing

Depends on `Faz3.7` for the pin, the measurement method and the stated pass threshold, and on `Faz3.8` for a bracket that contains the pin. **Both dependencies on `DEC-15` are discharged:** it was answered on 2026-09-04 (the shipped `fullres` artifact `fe0245a4720fb07b01d96deef47f5569`), and `IMPL-53` put the device on that base with the live md5 read back at both ends and the revert path exercised. The reason the decision mattered is unchanged and still governs: running the session on the other base would produce a valid measurement of the wrong artifact, so the opening bracket verifies the md5 rather than assuming it.

Depends on `Faz2.1` for the script and `Faz2.2` for the baseline lineage.

Does **not** depend on `Faz4.1`, `Faz4.7`, or any Phase 4 work. Both of those are `superseded` and Phase 4's remaining sub-plans run after this phase.

Blocks `Faz3.10`, which attacks the state this sub-plan establishes, and contributes the central evidence `Faz3.11` records.

Required decisions: **none outstanding.** `DEC-15` (the base) and `DEC-18` (`pref_48m_key`=`0` as the configured state) were both answered by the user on 2026-09-04 and are recorded in the ledger. The session verifies both rather than deciding either.

Required credentials or live endpoints: none. Root through KernelSU, `adb`, and both applications installed.

Required human approvals: physical device access and two shutter presses. Confirmation of the base is no longer an approval — `DEC-15` is answered and the device is already on that base — but the opening bracket must still read the md5 back rather than trusting this sentence.

Fresh-session token and context risk: **low to medium**. Two captures, two dumpsys reads and two brackets; the volume risk is the dumpsys output, which should be filtered on the device as the smoke script already does rather than pulled whole.

Subagents are not recommended. The session is one stateful sequence.

## 11. Risks and Mitigations

- Risk: something changes mid-session — a mode switch, a mount, a preference write by an app — and the "same HAL state" claim is false without anyone noticing. Impact: the phase's central claim rests on a session that did not have the property it asserts. Mitigation: `F3.9-06` requires every differing line between the brackets to be named and accounted for, and an unaccounted difference is defined in advance as a finding.
- Risk: the Open Camera capture is taken at a size other than full resolution because its own setting was not checked. Impact: the 50 MP half is unproven while appearing proven. Mitigation: `F3.9-04` reads the configured stream from the service with the app open rather than trusting the app's UI.
- Risk: a standing condition — SABRE failures, `Invalid mesh` — is read as a defect and the session is aborted or the result is hedged. Impact: wasted device time and a weaker result than the evidence supports. Mitigation: `F3.9-07` records them as standing conditions with `IMPL-40`'s positive-control evidence cited.
- Risk: AGC fails to launch for an unrelated reason — a contaminated boot after a provider abort (`FIND-3.4-03`). Impact: a launch failure is attributed to coexistence. Mitigation: checklist item 8 requires a reboot after any provider abort before the session begins, and the session's opening bracket is taken after that reboot.
- Risk (`R12`): the pin drifted between `Faz3.7` and this session. Impact: the AGC capture is folded and the failure is attributed to coexistence rather than to the pin. Mitigation: the opening bracket now reports the pin (`Faz3.8`), so drift is visible before the capture instead of after.
- Risk: the session is run on the experimental base while the result is later read as a statement about the shipped module. Impact: a claim about an artifact that was never measured — the same risk `Faz3.7` raised. Mitigation: `DEC-15` is answered and the device is on the shipped base, verified live by `IMPL-53` and again by the opening bracket; both md5s appear in the result, and any figure carried from `IMPL-52` is labelled as measured on the experimental `ce419bc901bea61945d166aee11e1ab0`.
- Risk: the two captures are separated by a long gap and an unnoticed intervening event. Impact: a session in name only. Mitigation: the two captures are consecutive with no intervening command other than launching the second app, and the closing bracket is taken immediately.
- Risk (invariant 4): an attempt is made to compose a sensor mode with `50mp` to make the session more interesting. Impact: an unreachable state, a wasted session, and a result that answers no question the objective asks. Mitigation: the sensor-layer state is recorded as forced, not chosen, and composition is out of scope — `Faz5.3` already decided to retain the exclusion.

## 12. Desired End State

One recorded session in which the HAL md5 is identical at both ends, AGC saved a measured-clean 12.58 MP image, and Open Camera saved a measured-clean 50.33 MP image, with both configured streams read from the camera service while their apps were open, the enumeration at 13 devices and the trap count at 0/12 throughout, and every bracket difference accounted for.

That session is the evidence for the second half of `DEC-14`'s objective, and it is the state `Faz3.10` then tries to break.

The evidence an implementer should produce: the two bracket filenames and their diff, the two pulled originals with their measured triples, the two dumpsys stream extracts, the AGC launch verdict, and the standing-conditions note.

The ledger summary Step 4 should append records: the HAL md5 held constant, the sensor blob md5 and its forcing reason, both measured triples with the thresholds stated in advance, both configured stream readings, the launch verdict, the enumeration and trap counts at both ends, and the accounted-for bracket differences.

## 13. Next Sub-Phase Transition Criteria

- Both captures came from one session with an identical HAL md5 at both ends.
- Both originals measure clean by the same method against thresholds stated in advance.
- Both configured streams were read from the camera service with their apps open and agree with their apps' requests.
- Every bracket difference is named and accounted for.
- Enumeration is 13 and the trap count is 0/12 at both ends.
- The standing conditions are recorded with prior evidence cited.
- `Faz3.10` has a specific, reproducible state to attack.
