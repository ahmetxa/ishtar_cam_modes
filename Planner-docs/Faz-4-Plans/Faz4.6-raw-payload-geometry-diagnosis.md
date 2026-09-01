# Faz 4.6 — RAW Payload Geometry Diagnosis

## 1. Context

`DEC-13`, answered by the user on 2026-09-01, created this sub-plan and fixed its subject. `F4.5-05` established statically that the QTI vendor tag `org.codeaurora.qcamera3.quadra_cfa.activeArraySize` (`80340003`) has **no word to patch** — the constant occurs zero times as an aligned dword in the 27 MB binary and is never built as a `movz`/`movk` immediate, because a vendor tag's numeric id is assigned at runtime by the vendor-tag provider. `IMPL-30` then measured that it stays `[0 0 4096 3072]` while all three standard tags read full resolution, and that the capture is still corrupt. The user chose option (a): **leave `80340003` alone and pursue `FIND-4.5-02`'s stride hypothesis instead**, on the reasoning that spending a scope expansion on the vendor-tag provider before testing the stride model risks paying for the wrong diagnosis. That reasoning is settled and is not re-argued here.

This sub-plan is structurally the same object `DEC-12` produced when it created `Faz-4-Plans/Faz4.5-active-array-raise.md`: a decision that named work no existing sub-plan owned, an owner that Step 4 cannot author for itself, and a Step 2 run to write it. The difference is what it inherits. `Faz4.5` inherited a stated cause and a patch class; this sub-plan inherits a **refuted** stated cause and no patch class at all.

`FIND-4.5-02` (P1, open) is what it exists to answer, and the finding's own wording is the boundary: "`FIND-3.5-01`'s stated cause is incomplete. It named three tags; two are now demonstrably raised and the artifact survives, so the active-array tags are not the whole story." `FIND-3.5-01` itself is **not closed** and stays open until this sub-plan produces a cause that survives measurement.

The project's headline result is intact and is not in question here. `IMPL-23` cleared the libgcam gate, `IMPL-30` re-cleared it with all three standard tags raised, and AGC captured 6144x8192 = 50.3 MP with zero `static_metadata.cc:667`, zero `frame_raw_max … matches neither`, zero `Stuck shot` and an empty crash buffer. The resolution goal is met. **The image is not.** This sub-plan is about the image only.

## 2. Goal

Determine, by measurement rather than by inference, what actually produces the artifact in AGC's full-resolution frame — a cause specific enough that the next step is either a named patch, a named configuration change, or a stated determination that no change in this project's reach fixes it.

## 3. Description

The problem is that the project has spent two sub-plans on a diagnosis that has now been falsified by its own success. `FIND-3.5-01` said the frame was corrupt because the active-array tags disagreed with the buffer. Both patchable tags were raised, the disagreement was removed, and the frame is still wrong. Continuing to reason from tag values would be reasoning from a refuted premise.

**What replaces it is arithmetic on evidence the project already holds.** `EV-38` is the strongest measurement anyone has taken on this fault, because it is a measurement rather than a description: exactly **75.0%** of the frame is pure black at luminance 0.0, occupying three quarters of one axis at full extent on the other; the content sits in the remaining quarter as **two stacked strips with different colour casts**, upper red/pink and lower purple/magenta, plus a white band at the far edge. Four independent features — the exact fraction, the full extent on one axis, the doubling, and the two distinct casts — are four constraints, and a correct model has to satisfy all four rather than the first one.

The crop model satisfies only the first. `4096 x 3072` is exactly a quarter of the area of `8192 x 6144`, which is why `80340003` reads as the obvious suspect. But a crop to a `4096 x 3072` rect leaves a **rectangle** occupying half of each axis. It cannot leave a strip that runs the full extent of one axis, it cannot produce a doubling, and it cannot produce two different colour casts inside one exposure. The shape is the argument, and the shape argues against the suspect.

**A second model fits all four features, and stating it precisely is what makes this sub-plan a bounded job rather than an open investigation.** Suppose a payload of `4096 x 3072` pixels is written linearly into a raster that is read back at width `8192`. Then:

- the payload occupies `4096 x 3072 = 12,582,912` pixels of a `8192 x 6144 = 50,331,648` raster, which is **exactly 25%** — the measured content fraction, and therefore exactly 75.0% black;
- those pixels fill `12,582,912 / 8192 = 1536` complete raster rows out of 6144, which is **exactly a quarter of one axis at full extent on the other** — the measured shape;
- each raster row of 8192 consumes **two** source rows of 4096, so the content splits into **two halves along the long axis** — the measured doubling;
- and because consecutive Bayer rows carry opposite CFA phase, the half built from even source rows and the half built from odd source rows demosaic with **different colour casts** — the measured pair of tints, which a single phase flip does not produce and which `H-03`'s update already recorded as the reason the CFA-phase explanation got *weaker* rather than stronger.

Every measured feature falls out of one assumption. That does not make it true — the arithmetic is consistent with the observation, which is a much weaker claim than causation — but it makes it **decisively testable without the device, without the user, and without a single byte written to a system binary**, which is the cheapest discriminating probe this project has ever had available. If the payload really is a `4096`-wide image folded into an `8192`-wide raster, then un-folding it — taking each raster row, splitting it at 4096, and emitting the two halves as consecutive rows — reconstructs a coherent `4096 x 3072` scene. If it does not reconstruct, the model is dead and the crop model and the pitch model are back on equal footing with a measurement between them.

**The viewfinder is the second lever and it is underused.** `EV-39` records that live preview was correct in the same state and in the same session that produced the corrupt still. That confines the fault to the still/RAW consumption path and excludes everything shared with preview — sensor readout as such, the CSI link, the metadata the preview stream also reads. It is the single most useful narrowing the project has, and any probe designed here that cannot exploit it is a weak probe. The corresponding control is cheap: Open Camera captured cleanly at 8192x6144 from the three-layer state (`EV-33`), but **has never been run against the five-word full stack** in which both active-array tags are also raised. Running it there separates "AGC's Gcam path is wrong" from "the raise broke the HAL's own still path", and it costs one shutter press.

The slice strategy is the one that has worked three times on this codebase — calibrate before searching, pre-commit before writing, measure one variable at a time. The first useful slice is entirely host-side and may settle the whole question on its own. The fastest validation signal is not a capture: it is whether the reconstruction produces a recognisable scene, which is a yes or a no obtainable from a file already on disk plus the original of it.

What must not be over-planned is the mechanism behind whatever the geometry turns out to be. If the payload is half-resolution, the next question — whether the sensor was still running a binned mode, whether the remosaic path was configured at half extent, whether the buffer stride was negotiated from a stale rect — is a **new** question with its own evidence needs, and answering it speculatively now would repeat exactly the error that `FIND-4.5-02` records. This sub-plan establishes *what* the frame is. It routes *why* rather than guessing.

## 4. Scope

- Recovery of the **original full-resolution** AGC artifact. The evidence file in `snapshots/` is a **512 x 682 downscale**, whose per-row structure has been destroyed by resampling; the reconstruction test is meaningless on it.
- Establishing the mapping between the JPEG's axes and the sensor raster's axes before any shape claim is interpreted, since the JPEG is `6144 x 8192` while the sensor array is `8192 x 6144` and the transform between them is not recorded anywhere.
- Numeric re-measurement of the artifact's structure on the original: the black region's exact bounds, the boundary between the two strips, the per-strip per-channel means that make "different colour casts" a number, and the white edge band's extent.
- The **row-pairing reconstruction test**: un-folding the content region on the hypothesis that a `4096`-wide payload was written into an `8192`-wide raster, and judging whether a coherent scene results.
- A consumer control against the **five-word full stack** — Open Camera and the stock camera at full resolution in the exact state that produced the artifact — exploiting `EV-39`'s preview/still split.
- Reading what the HAL actually configured for the capture request: the selected sensor mode, the binning state, and the negotiated buffer dimensions and stride, from logs rather than from metadata.
- A `RAW_SENSOR` / DNG probe, **explicitly gated** on `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` landing format-32 emission at full resolution, since `EV-35` establishes that no DNG is obtainable at full resolution before then.
- A stated verdict on `FIND-4.5-02` and on whether `FIND-3.5-01` can close, with the consequence routed rather than acted on.
- Landing the eighth per-measurement checklist item — `FIND-3.4-03`'s crash-contamination rule — in `docs/phase3-preconditions.md` itself, which no sub-plan in the queue has held write authority for.
- Immediate recording of every finding into the continuity artifacts during the session it is produced.

## 5. Out of Scope

- **Any pursuit of `80340003` by a non-word-patch mechanism.** `DEC-13` answered this and its reasoning is closed. If the evidence produced here changes the picture, that is a new decision routed to the user, not a scope expansion taken by the implementer.
- Narrowing RAW emission, and extending emission to format 32. Both are `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md`, by `DEC-11`. This sub-plan **consumes** the format-32 result for one gated probe; it does not produce it.
- Duration rows (`Faz4.2`), patch table consolidation (`Faz4.3`), and the consolidated compatibility survey (`Faz4.4`).
- Any change to the confirmed `f0006` write site at `0x0166645c`, or to the `f0000` / `f000a` words at indices `5867691` and `5871957`. All three are confirmed by measurement and are re-applied here unchanged, as the state under test.
- Modifying AGC — the APK, its smali, or its preferences beyond the `pref_48m_key` that `IMPL-30` already established is required for a full-resolution capture.
- Any change to the sensor layer, the mode blobs, or the ten-mode dispatch.
- Reopening Phase 3 or any of its closed questions. This sub-plan consumes Phase 3's evidence; it does not revise it.
- Writing image-processing tooling beyond what the two host-side tests need. One reconstruction script is not a library.
- Diagnosing the `hardware_buffer_map.cc:66 SABRE: Cannot get file descriptor from opaque_handle` line beyond recording whether it correlates with the artifact. It occurred 30x per shot in `IMPL-23`; whether it is cause, symptom, or noise is a question this sub-plan may raise but is not budgeted to answer.

## 6. Current Repository Evidence

**The artifact evidence on disk is a downscale, and this is the first thing that would waste a session if it were discovered mid-probe.** `snapshots/20260901-1811__Faz4.5__f4509-capture-artifact.png` is **512 x 682**, aspect `0.7507` against the frame's `6144/8192 = 0.75`. It is a faithful record of the *shape* — the 75% black region and the two strips are visible in it — and it is worthless for the reconstruction test, because resampling a 6144-wide image to 512 averages twelve source columns into each output column and destroys exactly the row-level structure the test reads. `IMPL-30` names the capture but the record does not state whether the original JPEG was pulled to the host or left on the device, so `F4.6-01` treats recovery as an open question with a re-capture fallback rather than as a lookup.

**The state that produced the artifact is fully recorded and reproducible.** `IMPL-30`: mode `50mp`, then the stack built on the fullres base by `dd` — raw50 (4 words) + pixelarray (1) + `f0000` (1) + `f000a` (1) = **seven words**, full-stack md5 `c094101de0184e9216a57020873bac0b`, pre-committed before any device write and matched. Tag state under it: `f0006` `[8192 6144]`, `f0000` `[0 0 8192 6144]`, `f000a` `[0 0 8192 6144]`, `80340003` `[0 0 4096 3072]`. `camera.hal0` `streamcfg` 440 -> 800, `hal3` 500 -> 868. `pref_48m_key=1` set with the user's approval and AGC preferences backed up first; the capture required both that preference **and** a camera restart, per `EV-32`. Reversal was proven byte-identical three times and the device is at `BASELINE-2026-08-31-V21`.

**The three patch tables exist on disk and compose without conflict.** `agc-50mp-yama/hal-raw50-deneme.patch`, `hal-pixelarray-deneme.patch`, and `hal-activearray-deneme.patch` (the last written by `IMPL-27` and carrying both words with their four-byte indices and encodings). Project-Ontology section 6 records that the tables **share no index** and that the composition is order-independent, and it records the calibration md5s for every intermediate stack. Nothing here needs to be re-derived.

**The measured artifact structure, from `EV-38`, is the specification the reconstruction is judged against.** Exactly 75.0% pure black at luminance 0.0 on three quarters of one axis at full extent on the other; content in the remaining quarter as two stacked strips with different casts, upper red/pink and lower purple/magenta; a white band at the extreme edge. `IMPL-30` also records that `IMPL-23` described "exactly half the frame black" from visual inspection where this run measured 75%, that no image from `IMPL-23` survives, and that **no regression is claimed** — the discrepancy is recorded rather than resolved. This sub-plan inherits that posture: it does not attempt to reconcile the two figures, because one of them was an estimate and the record cannot say which.

**`EV-39` is the narrowing.** The viewfinder was correct, user-observed, in the same state that produced the corrupt still. Preview and still diverge, so the fault is downstream of everything they share.

**`EV-33` gives the control's earlier reading and shows what has not yet been tested.** Open Camera captured 8192x6144 cleanly, with correct neutral colour and a full frame, from the **three-layer** state minutes apart from AGC's corrupt frames. It has not been run against the five-word stack. That gap is the cheapest new measurement available and it is `F4.6-05`.

**`EV-35` fixes the gate on the strongest probe.** On `camera.hal0` under the three-layer stack, format 32 appears only at `4096x2304` and `4096x3072`, byte-identical to stock, because `hal-raw50-deneme.patch` widens the format test to `0x22..0x26` = 34–38 and `RAW_SENSOR` is 32, below the subtract base. Formats 33/34/35/36/37/38/54 all gained an 8192x6144 row; 32 did not. **No DNG can be captured at full resolution by any application in this state**, which is why `F4.6-07` is gated rather than scheduled.

**`H-03` already recorded the consequence of `IMPL-30` for the colour explanation, and this sub-plan starts from that update rather than repeating it.** The CFA-phase account of the magenta cast is now *weaker*: the factor-of-two geometry fault it depended on was removed for both standard tags and the cast survived, in two different tints within one frame, which a single phase flip does not readily produce. `H-03` stays `probable` because its discriminating probe is still the full-resolution DNG and that is still unrunnable — the same gate `F4.6-07` sits behind.

**The measurement contract already exists and is not re-invented here.** `docs/phase3-preconditions.md` section 5 holds the seven-item per-measurement checklist, and `Faz4.5` section 9 restated it inline with an eighth item added for `FIND-3.4-03`. `AUDIT-FIX-08` recorded why the eighth item is not in the file: a write-authority search across all thirty-three Implementation Contracts found `docs/phase3-preconditions.md` as `proposed` only in `Faz3.1`, which is verified and closed, and `existing` everywhere else. **This sub-plan takes that write authority** and `F4.6-09` lands the item, which is the permanent fix the audit said "remains outstanding for Step 2 to route."

**A method caveat that cost this project two false results in one session, carried forward as a rule rather than a note.** `logcat | grep <pattern>` **counts your own command**, because `adbd` logs each incoming shell request verbatim and the request line contains the search string. This produced a **false provider abort** and a **false libgcam gate failure** in the `IMPL-28` / `IMPL-30` session, either of which a trusting reader would have recorded as real. Every log probe in this sub-plan must use `logcat -d | grep -v adbd | grep <pattern>`, or redirect to a file on the device and read that file. This binds `F4.6-05` and `F4.6-06` in particular, which are log probes by construction.

**`EV-17` still constrains method:** radare2 and rabin2 do not complete on this binary — two runs at 300 s and 60 s produced no output. Any static work in `F4.6-06` is scripted, per `docs/reverse-engineering-toolchain.md`.

**The budget.** `DEC-06` fixes 15 candidate sites across at most 2 implementation sessions; `IMPL-30` reconciled the total at **6 of 15 consumed, 9 remaining**. This sub-plan is a **diagnosis, not a write-site search**, so it is expected to consume none of that allowance: the allowance is spent per candidate examined to the point of a patch decision, and this sub-plan reaches no patch decision. If it does start examining candidates, that is a scope change and `F4.6-08` must say so.

## 7. Planned Work Breakdown

- F4.6-01 — Recover the original full-resolution artifact
  - Description: Locate the original AGC JPEG from the `IMPL-30` capture on the device and pull it to the host, verifying `6144x8192` from the SOF marker rather than from a filename. If it no longer exists, re-create the state — mode `50mp`, the seven-word stack at md5 `c094101de0184e9216a57020873bac0b` pre-committed and matched, `pref_48m_key=1`, camera restart — and capture again, which is a live slice under the full measurement contract. State explicitly which of the two routes was taken, because a re-capture is a second exposure of a different scene and is not pixel-comparable with the first.
  - Output: An original-resolution artifact file on the host, with its provenance stated and its dimensions read from the SOF marker.
- F4.6-02 — Establish the sensor-to-image axis mapping
  - Description: Determine how the JPEG's `6144x8192` frame maps onto the sensor's `8192x6144` raster — EXIF orientation, whether AGC rotated pixels or only tagged them, and which JPEG axis corresponds to the sensor's row direction. Every shape claim in `EV-38` is stated in JPEG axes and every model in section 3 is stated in raster axes; without this mapping the two cannot be compared and "full-extent strip" is ambiguous between two different faults.
  - Output: A stated axis mapping with its evidence, and `EV-38`'s shape restated in raster axes.
- F4.6-03 — Measure the artifact structure numerically on the original
  - Description: On the recovered original, measure the black region's exact pixel bounds and its fraction, the exact coordinate of the boundary between the two content strips, the per-strip per-channel means that turn "different colour casts" into two numbers, and the white edge band's extent. Compare each against the model's predictions: black fraction 0.750, content band 1536 raster rows of 6144, strip boundary at exactly 4096 along the raster's long axis.
  - Output: A measured structure table with each figure set against its predicted value, and an explicit note on any figure that does not land on the prediction.
- F4.6-04 — Test the row-pairing reconstruction
  - Description: Un-fold the content region on the hypothesis that a `4096`-wide payload was written into an `8192`-wide raster: split each raster row at column 4096 and emit the two halves as consecutive rows, yielding a candidate `4096x3072` image. Judge whether a coherent scene results — continuous edges across the fold, a single consistent colour cast, recognisable content. Run the inverse control as well (fold a known-good `4096x3072` image into `8192` width) so that a positive result is read against a reference rather than against expectation. **This is the decisive host-side probe and it consumes no device, no user, and no budget.**
  - Output: A reconstructed candidate image and a stated yes or no on coherence, with the control's output alongside it.
- F4.6-05 — Run the consumer control against the five-word stack
  - Description: In the exact state that produced the artifact, capture at full resolution through **Open Camera** and through the **stock camera**, and measure each result. `EV-33` establishes Open Camera clean under the three-layer stack; it has never been run with both active-array tags also raised. A clean result confines the fault to AGC's Gcam path; a corrupt result means the raise broke the HAL's own still path and changes what `Faz4.4` must survey. Record the preview behaviour in each application too, since `EV-39`'s preview/still split is the narrowing being exploited.
  - Output: Two measured consumer verdicts with resolutions read from the file, plus a preview observation for each, against the `EV-33` reference.
- F4.6-06 — Read what the HAL configured for the capture request
  - Description: From logs taken with the `adbd` filter in force, establish what the HAL actually configured for the full-resolution RAW stream: the selected sensor mode and its dimensions, the binning state, and the negotiated buffer width, height and stride — as distinct from the metadata the HAL *advertises*, which is what every measurement so far has read. Record whether the `hardware_buffer_map.cc:66 SABRE` line correlates with the artifact and at what count. If the log surface does not carry the stride, say so and stop rather than adding a static trace to reach it; a scripted trace of the buffer-negotiation path is a fallback to be proposed, not an assumed step.
  - Output: A configuration record for the capture request, or a stated determination that the log surface does not expose it.
- F4.6-07 — The `RAW_SENSOR` / DNG probe — **gated on `Faz4.1`**
  - Description: Once `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` has landed format-32 emission at 8192x6144, capture a full-resolution DNG through an application that writes one and inspect the payload directly: its declared dimensions, its actual valid extent, and its CFA phase. This is the probe that settles both this sub-plan's remaining ambiguity and `H-03`'s, and `EV-35` establishes it is impossible before then. **Do not attempt it earlier and do not substitute a JPEG for it.** If `F4.6-04` settles the model on its own, record here that the probe was not needed rather than running it for completeness.
  - Output: A DNG payload verdict, or a stated reason the probe was not run.
- F4.6-08 — State the verdict and route the consequence
  - Description: State what the frame is, with the evidence for it, and whether `FIND-4.5-02` closes. Then state what follows **as a routed item rather than as work taken here**: if the payload is half-resolution, the question of why — sensor mode, remosaic configuration, or stride negotiation — is a new question with its own evidence needs and its own owner. If that question reopens anything `DEC-13` settled, it is raised to the user as a new decision with the evidence attached; it is not decided by the implementer. Say explicitly whether `FIND-3.5-01` can close.
  - Output: A verdict on `FIND-4.5-02`, a disposition for `FIND-3.5-01`, and every consequence routed to a named owner or raised as a named decision.
- F4.6-09 — Land the eighth per-measurement checklist item
  - Description: Add `FIND-3.4-03`'s crash-contamination rule as an eighth item in `docs/phase3-preconditions.md` section 5 — after any camera-provider abort, reboot before the next reading; a reading taken after an abort without an intervening reboot is void and is retaken, not interpreted. `AUDIT-FIX-08` established that no sub-plan in the queue holds write authority for this file and that `Faz4.5` could only restate the rule inline. This sub-plan holds it. Add the `adbd` self-echo caveat from section 6 alongside it, since it is what makes a false abort look like a real one.
  - Output: `docs/phase3-preconditions.md` carrying an eighth checklist item and the `adbd` filter rule, with `AUDIT-FIX-08` recorded as permanently discharged.
- F4.6-10 — Record continuously
  - Description: Write every measurement, verdict and located address into `Planner-docs/Project-Ontology.md` section 6 and `Planner-docs/Project-Comprehension.md` during the session it is produced, per `R10` and `QAS-03`. This is a continuous work item, not a closing step. State the budget position explicitly even though this sub-plan is expected to consume none of it.
  - Output: Updated continuity artifacts read back before the session ends, and an explicit budget statement.

## 8. Acceptance Criteria

- The artifact under analysis is the **original full-resolution** frame, its dimensions read from the SOF marker, and its provenance is stated as either pulled or re-captured — a downscale is never analysed for structure.
- The sensor-to-image axis mapping is stated with its evidence, and `EV-38`'s shape is restated in raster axes before any model is judged against it.
- The measured structure table sets each figure against the model's predicted value, and any figure that misses its prediction is called out rather than rounded toward it.
- The row-pairing reconstruction was run, its control was run alongside it, and the result is a stated yes or no on coherence with the candidate image retained as evidence.
- Open Camera and the stock camera were captured in the **five-word stack** state, with measured resolutions and a preview observation each, compared against the `EV-33` reference.
- The capture request's configured sensor mode and buffer geometry are recorded, or the absence of that information in the log surface is stated as a determination rather than left blank.
- The DNG probe is either run against a format-32-enabled state with a payload verdict, or explicitly recorded as not needed or not yet reachable, with the reason.
- `FIND-4.5-02` carries an explicit verdict, and `FIND-3.5-01` is explicitly closed or explicitly left open with what was learned attached.
- Every consequence is routed to a named owner or raised as a named decision. Nothing that reopens `DEC-13`'s settled ground is acted on by the implementer.
- `docs/phase3-preconditions.md` carries the eighth checklist item and the `adbd` filter rule, and `AUDIT-FIX-08` is recorded as permanently discharged rather than restated inline for a third time.
- The full measurement contract in section 9 was satisfied for every live reading, including the reboot rule after any provider abort.
- Every reversal is proven byte-identical to the pre-attempt bracket in the comparable region, and the device is left at `BASELINE-2026-08-31-V21`.
- Every finding is in the continuity artifacts by the end of the session it was produced, not in a note to be transferred later.
- The budget position is stated explicitly, including a statement that no allowance was consumed if none was.

## 9. Validation and Test Approach

**The measurement contract is `docs/phase3-preconditions.md` section 5 plus the eighth item this sub-plan lands in `F4.6-09`.** Until that item is written to the file, it binds this sub-plan inline exactly as it bound `Faz4.5`, and `F4.6-09` is what stops it needing to be restated a fourth time.

1. **Preferences clear.** All twelve trap keys audited per-key, expecting 0/12, never by a single `scripts/smoke.sh` reading. The `FIND-5.2-01` caveat carries: smoke's `prefs.trap` field disagreed with a direct audit once; the per-key audit wins, the smoke field is the cross-check, and any disagreement is recorded rather than resolved silently. Note that `F4.6-01`'s re-capture route deliberately sets `pref_48m_key=1`, which is **not** a trap key — back the preferences up first and restore them, as `IMPL-30` did.
2. **Bracket taken.** `scripts/smoke.sh -o <UTC>__Faz4.6__<label>` before and after every device change, both committed.
3. **One variable.** Exactly one of {sensor layer, HAL layer, APK, preference} moved since the previous snapshot. If two moved, the measurement is not attributable and is redone.
4. **Metadata republished.** Per `FIND-2.3-01`, confirm the stream-config count reached its expected value, or that `wait_camera_list` completed, before reading any advertised row. RAW rows are read per resolution, never collapsed.
5. **Restorable.** The previous state is restorable by a named command and the restore is verified by snapshot diff, not assumed.
6. **Findings recorded immediately.** Every measurement and address goes into the continuity artifacts in the session it is produced. This project has lost address-book values to context truncation before.
7. **Attribution stated.** Every result names the AGC build it was measured against — currently the patched `ce65f862c990e2acc02be356f75a7122`, not stock.
8. **Crash contamination cleared.** After **any** camera-provider abort, reboot before the next reading. A reading taken after an abort without an intervening reboot is void and is retaken, not interpreted. **And the abort must be real:** `logcat | grep` matches `adbd`'s echo of your own command, which produced a false abort in the `IMPL-28` session. Always `logcat -d | grep -v adbd | grep <pattern>`, or redirect to a file on device first.

Validation identifiers:

- `VAL-GEOMETRY` (proposed) — the host-side structural measurement and the row-pairing reconstruction with its inverse control. Decisive, and it needs neither the device nor the user.
- `VAL-IMAGE` (from Faz 4.5) — the artifact check, described rather than scored, now measured on the original rather than on a downscale.
- `VAL-CAPTURE` (from Faz 3.5) — resolution read from the JPEG SOF marker, never from a filename or a gallery label.
- `VAL-CONSUMER` (proposed) — Open Camera and the stock camera at full resolution in the five-word stack, each with a measured resolution and a preview observation, against the `EV-33` reference.
- `VAL-STREAMLOG` (proposed) — the configured sensor mode and buffer geometry read from filtered logs, distinct from the advertised metadata every prior measurement has read.
- `VAL-DNG` (proposed, **gated**) — the full-resolution `RAW_SENSOR` payload inspection, unreachable until `Faz4.1` lands format-32 emission per `EV-35`.
- `VAL-LOG` (from Faz 3.5) — buffers raised and the crash buffer cleared before launch; `static_metadata.cc:667`, `frame_raw_max … matches neither` and `Stuck shot` counted rather than assumed absent, under the `adbd` filter.
- `VAL-CHECKSUM` (from Faz 3.3) — the predicted full-stack md5 committed before any device write and matched on apply and on revert.
- `VAL-METADATA` (from Faz 3.3) — confirmation that `f0006`, `f0000`, `f000a` and the RAW rows at 8192x6144 read as `IMPL-30` recorded them, so the state under test is the state that produced the artifact.
- `VAL-SMOKE` (from Faz 2.1) — the bracket.
- `VAL-REVERT` (from Faz 3.5) — reversal proven byte-identical in the comparable region.
- `VAL-PRECOND` (from Faz 3.1) — the eight-item contract above.
- `VAL-DOCS` (from Faz 3.2) — the continuity updates and the checklist edit read back before the session ends.

Local versus live: `F4.6-02`, `F4.6-03` and `F4.6-04` are entirely host-side once the artifact is in hand, and `F4.6-04` is the one that may settle the question. `F4.6-01` is host-side on the pull route and live on the re-capture route. `F4.6-05` and `F4.6-06` are live and need the user's hands. `F4.6-07` is live and gated on another sub-plan. `F4.6-09` is a documentation edit. Security validation is not applicable. Ontology validation is central, since the artifact model is what the address book and the comprehension register will carry forward.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| snapshots/20260901-1811__Faz4.5__f4509-capture-artifact.png | existing | The 512x682 downscaled record of the artifact. Establishes the shape; explicitly insufficient for the reconstruction test. | VAL-IMAGE |
| agc-50mp-yama/tools/frame_geometry.py | proposed | The host-side structural measurement and row-pairing reconstruction, with its inverse control. | VAL-GEOMETRY |
| docs/raw-geometry-diagnosis.md | proposed | The diagnosis record: measured structure, reconstruction result, consumer control, configuration reading, verdict, and routed consequences. | VAL-GEOMETRY, VAL-CONSUMER, VAL-STREAMLOG |
| docs/phase3-preconditions.md | modified | Land the eighth per-measurement checklist item and the `adbd` filter rule, discharging `AUDIT-FIX-08` permanently. | VAL-PRECOND, VAL-DOCS |
| agc-50mp-yama/hal-activearray-deneme.patch | existing | The two active-array words, re-applied unchanged as part of the state under test. | VAL-CHECKSUM, VAL-METADATA |
| agc-50mp-yama/hal-pixelarray-deneme.patch | existing | The confirmed `f0006` word, re-applied unchanged. | VAL-CHECKSUM, VAL-METADATA |
| agc-50mp-yama/hal-raw50-deneme.patch | existing | The RAW format gate words, re-applied unchanged. | VAL-CHECKSUM, VAL-METADATA |
| scripts/smoke.sh | existing | The bracket and the tag readings. | VAL-SMOKE, VAL-METADATA |
| docs/reverse-engineering-toolchain.md | existing | The scripted disassembly procedure, required by `EV-17` if `F4.6-06`'s fallback trace is proposed. | VAL-STREAMLOG |
| docs/recovery-runbook.md | existing | The recovery path if a live probe leaves the HAL unrecognized, as `IMPL-28` did. | VAL-REVERT |
| Planner-docs/Project-Ontology.md | modified | The artifact model, the configuration reading, and the `FIND-4.5-02` verdict. | VAL-DOCS |
| Planner-docs/Project-Comprehension.md | modified | New evidence rows for the measured structure and the reconstruction result; `H-03`'s state once the DNG probe resolves or is recorded unreachable. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on `Faz-4-Plans/Faz4.5-active-array-raise.md` for the artifact, the seven-word stack and its pre-committed md5, and the two confirmed active-array words. Depends on `Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md` for the capture procedure and the `EV-33` consumer reference, on `Faz-2-Plans/Faz2.1-device-smoke-script.md` for the bracket, and on `Faz-1-Plans/Faz1.3-patch-table-format-contract.md` for the table format the re-application follows. All are complete.

**Runs first in Phase 4's remaining queue, but only for its host-side half.** `F4.6-01` through `F4.6-04` need nothing that does not already exist, and `F4.6-04` may settle the question outright. Nothing is gained by deferring them.

**`F4.6-07` is gated on `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md`, and this is a real ordering interaction rather than a formality.** `EV-35` establishes that no application can obtain a full-resolution DNG until format-32 emission is extended, which is `DEC-11`'s work inside `Faz4.1`. So `Faz4.1` is not merely unblocked by `Faz4.5` — it is an **enabler** for this sub-plan's strongest probe. Deferring `Faz4.1` behind the whole of this sub-plan would deadlock the diagnosis at exactly the probe that discriminates best. `Faz4.1` therefore keeps its position and runs after this sub-plan's host-side half, with `F4.6-07` resumed afterwards if it is still needed. The precedent for splitting a sub-plan around a dependency is `IMPL-19`, which pulled the recovery-runbook half of `Faz9.2` forward and left the checklist half in place.

**What `DEC-12`'s premise now means, stated rather than left implicit.** `DEC-12` sequenced `Faz4.5` before `Faz4.1` so that `Faz4.1`'s preservation check would run against a good capture rather than certify that a corrupt frame is still corrupt. **That premise is half delivered.** The metadata is right — `f0006`, `f0000` and `f000a` all read full resolution — and the image is still wrong. `Faz4.1`'s check is nonetheless a **metadata integrity** check: it verifies that narrowing did not drop the full-resolution RAW rows and that format 32 was added, both of which are counts and rows in `dumpsys`, neither of which depends on the frame being beautiful. So `Faz4.1` runs on its own merits and its acceptance criteria stand unchanged, with one caveat that belongs in its run record rather than in its criteria: **a passing `Faz4.1` does not mean the image is fixed**, and nothing in Phase 4 may report it that way while `FIND-3.5-01` is open.

Blocks `Faz-4-Plans/Faz4.2-duration-rows.md`, `Faz4.3` and `Faz4.4` only through `Faz4.1`, which already precedes them.

Required decisions: none at entry. `DEC-13` is answered and is not reopened. If `F4.6-08` produces evidence that reopens the `80340003` question or points at the sensor-mode and remosaic configuration, that is raised to the user as a **new** decision with the evidence attached, not taken by the implementer.

Required infrastructure: the device, the module's patch machinery, a host-side image tool capable of reading a 50 MP JPEG, and a host-side md5 tool. Note that the reconstruction operates on a 50-megapixel image; a naive whole-image load is a real memory consideration on this host and the script should stream or tile rather than assume.

Required human approvals: re-applying the seven-word stack and restarting the camera, the shutter presses in `F4.6-01`'s re-capture route and in `F4.6-05`, and the preference change with its backup and restore.

Fresh session token and context risk: **medium**. Lower than `Faz4.5`, because there is no write-site search in a stripped 27 MB binary — the analysis is arithmetic on an image plus filtered log reads. The hazards are log volume, which the `adbd` filter and targeted patterns control, and the temptation to paste image data into the session, which must be avoided: the script reports numbers and writes files, and only the numbers enter the transcript.

Subagents are not recommended. The work is deep rather than broad and the evidence is concentrated in files the parent already holds. A bounded read-only helper for one mechanical extraction is defensible if the parent's context is nearly exhausted, but the parent owns every continuity write.

## 11. Risks and Mitigations

- Risk: the original artifact no longer exists on the device and the re-capture photographs a different scene. Impact: the reconstruction is judged on an image whose expected content is unknown, which makes "coherent" a judgement call rather than a measurement. Mitigation: `F4.6-01` requires the route to be stated, and the re-capture route should photograph a scene with strong straight edges and a flat neutral field, so that fold continuity and cast uniformity are readable rather than guessed at.
- Risk: the reconstruction is judged by eye and a near-miss is read as a hit because the model is attractive. Impact: a false diagnosis carried forward into a patch design, which is exactly the failure `FIND-4.5-02` exists to record. Mitigation: `F4.6-04` requires the inverse control — fold a known-good image and reconstruct it — so a positive result is read against a reference; and `F4.6-03` requires each measured figure to be set against its predicted value with misses called out.
- Risk: the model is wrong and the sub-plan ends with three refuted models and no cause. Impact: `FIND-3.5-01` stays open with the diagnosis no further forward. Mitigation: this is an admissible outcome and `F4.6-08` is written to accept it — the acceptance criteria require a verdict, not a fix. The measured structure table and the consumer control are durable evidence for whoever picks it up next, and `F4.6-05` narrows the fault domain regardless of which model survives.
- Risk: `F4.6-05` finds Open Camera **also** corrupt under the five-word stack. Impact: the raise broke the HAL's own still path, which contradicts the reading that this is Gcam-specific, and it changes what `Faz4.4` must survey. Mitigation: this is a valuable result rather than a setback and must be recorded as one; route it to `Faz4.4` immediately, alongside `FIND-4.5-01`, since both are consequences of the same raise.
- Risk: a log probe records a false positive from `adbd`'s echo of its own command. Impact: a fabricated abort or a fabricated gate failure, both of which happened in one session already. Mitigation: checklist item 8 makes the filter mandatory, `F4.6-06` restates it, and any abort must be confirmed by a second method before a reboot is treated as required.
- Risk: `F4.6-07` is attempted before `Faz4.1` lands format 32 and returns a 4096-wide DNG that is mistaken for evidence about the full-resolution path. Impact: a confident wrong answer on the discriminating probe. Mitigation: `EV-35` is quoted in the work item, the gate is stated in three places, and the DNG's declared dimensions are part of the verdict rather than an assumption.
- Risk: a live probe leaves the HAL at an unrecognized md5, as `IMPL-28` did when the permission gate interrupted it mid-sequence. Impact: `hal_seed` refuses to move an unrecognized HAL while mounted, so a mode switch fails until the word is reverted. Mitigation: `FIND-3.4-01`'s operational rule — revert before any mode switch — plus `docs/recovery-runbook.md`, whose central claim was verified mechanically by `IMPL-19`: no module script writes to `/odm`, so disable-plus-reboot is a complete restore.
- Risk (`R10`): the session exhausts context and the measured structure is lost. Impact: re-measurement of work already done, which has cost this project before. Mitigation: `F4.6-10` is continuous rather than a closing step, and the numbers are small enough to record as they are produced.
- Risk: scope drifts into the vendor-tag provider because `80340003` remains the visible odd one out. Impact: `DEC-13` is relitigated by drift rather than by decision. Mitigation: section 5 forbids it explicitly and `F4.6-08` requires any such consequence to be raised to the user as a new decision with evidence, not acted on.
- Risk (`R8`): a system update changes `camera.qcom.so` mid-diagnosis. Impact: every offset invalidates at once and the state under test cannot be rebuilt. Mitigation: unchanged project posture — the md5 guard is the detector, and the stack md5 is pre-committed and matched before every application.

## 12. Desired End State

The artifact has a cause stated with evidence, or the models that do not explain it are refuted with evidence and the remaining fault domain is narrowed to something a successor can act on. `FIND-4.5-02` carries a verdict. `FIND-3.5-01` is explicitly closed, or explicitly left open with what was learned attached — the same disposition `Faz4.5` was permitted and used.

Concretely, at the end of this sub-phase the project knows: what the frame actually is in raster axes rather than in JPEG axes; whether the content region reconstructs as a half-resolution payload folded into a full-resolution raster; whether the fault is confined to AGC's Gcam path or reaches the HAL's own still path; what the HAL configured for the capture request as opposed to what it advertised; and what the next step is, named and owned.

The evidence an implementer should produce is the recovered original with its provenance, the axis mapping, the measured structure table against predictions, the reconstruction output with its control, the two consumer verdicts with resolutions and preview observations, the configuration reading or the determination that it is unavailable, the DNG verdict or the stated reason it was not run, and the reversal diffs.

The ledger summary Step 4 should append records: which route recovered the artifact, the measured structure against the predicted figures, the reconstruction verdict, the consumer control result against `EV-33`, the configuration reading, the `FIND-4.5-02` verdict, the `FIND-3.5-01` disposition, every routed consequence and raised decision, whether `AUDIT-FIX-08` is permanently discharged, the budget position, and the restored state's checksum.

## 13. Next Sub-Phase Transition Criteria

- The artifact analysed is the original full resolution, its provenance stated, and its axis mapping fixed.
- The row-pairing reconstruction was run with its control, and the result is a stated yes or no.
- `FIND-4.5-02` has an explicit verdict and `FIND-3.5-01` has an explicit disposition.
- The consumer control against the five-word stack is recorded, and any result affecting the HAL's own still path is routed to `Faz4.4` alongside `FIND-4.5-01`.
- Every consequence is routed to a named owner or raised to the user as a named decision; nothing settled by `DEC-13` was acted on.
- `docs/phase3-preconditions.md` carries the eighth checklist item and the `adbd` filter rule, so no successor restates them inline.
- The device is at `BASELINE-2026-08-31-V21` with the reversal proven byte-identical in the comparable region.
- Every finding is in the continuity artifacts, and the budget position is stated.
- `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` may begin: it is unblocked by `Faz4.5`, its preservation check is a metadata-integrity check that does not require a correct image, and its format-32 extension is what `F4.6-07` is waiting for.
