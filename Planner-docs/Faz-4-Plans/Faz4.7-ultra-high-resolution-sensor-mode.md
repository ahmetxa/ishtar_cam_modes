# Faz 4.7 — Ultra-High-Resolution Sensor Mode

## 1. Context

`IMPL-46` found this sub-plan's reason for existing while doing something else. A write-authority scan across **all thirty-four** sub-plans for `MaximumResolution`, `d0014`, `d0015`, `d0016`, `ULTRA_HIGH_RESOLUTION` and `pixelMode` returned **zero hits**. The entire ultra-high-resolution line — the capability, the four `*MaximumResolution` sensor tags, the scaler tables and the `sensor.pixelMode` request key — has **no owning sub-plan**, yet two implementation runs have already landed work in it.

`IMPL-44` applied an eighteen-row HAL table and published the capability. `IMPL-45` built a Camera2 client, requested the mode and measured the result. Both ran as `F4.6-08` routed consequences at the user's direction. That is the same structural class as `AUDIT-FIX-08`, which `Faz4.6` closed by taking write authority for `docs/phase3-preconditions.md`: work was real, measured and correct, and no plan owned it. **This sub-plan takes that ownership** — retroactively for what has landed, and forward for what remains.

It also inherits a correction. Sections 22 and 23 of `docs/raw-geometry-diagnosis.md` both stated that filling `d0015`/`d0016` is "`Faz4.2`'s duration-row work". That is wrong and `IMPL-46` corrected it: `Faz4.2` scopes `d000b`/`d000c`, the **default-mode** duration tables, and its Out of Scope excludes changing which formats or resolutions are emitted. The `MaximumResolution` variants were never in its scope. This sub-plan is where they belong.

`FIND-4.5-02` (P1, open) is the finding this work serves, and `IMPL-46` split it cleanly into two independent faults. **Fault 1: the sensor reads out binned `4096x3072` when `8192x6144` is requested.** **Fault 2: that payload is then written into the full-size buffer without stride adaptation.** This sub-plan owns fault 1 only. Fault 2 is measured here as a control, not fixed.

## 2. Goal

Make a full-resolution `MAXIMUM_RESOLUTION` stream configurable on this device, request it, and produce a measured answer to the one question the project has never been able to ask: **does the IMX989 leave 2x2 binning when a client requests the unbinned mode at full size?**

The goal is a measurement, not a guaranteed positive. A capture in which `pixelMode` reads `MAXIMUM_RESOLUTION`, the stream is `8192x6144`, and `rawBinningFactorUsed` is **still true** is a complete and successful outcome of this sub-plan — it would establish that CamX's honouring of the mode does not extend to the sensor, which is currently unknown and unknowable.

## 3. Description

The problem is a table whose contents contradict the tags published beside it. `IMPL-44` opened a single bit-28 gate at eighteen sites and the whole ultra-high-resolution feature appeared: the capability on eleven cameras, `activeArraySizeMaximumResolution [0 0 8192 6144]`, `pixelArraySizeMaximumResolution [8192 6144]`, `binningFactor [2 2]`, and `sensor.pixelMode` as request key 136. What did not appear is a max-res stream table describing that geometry.

Camera 2's `d0014` is `int32[28]` — seven formats (33, 34, 35, 36, 37, 38, 54) at exactly **one** size, `1920x1080`. The camera service validates stream configuration against that table, so `IMPL-45`'s client could configure `1920x1080` in `MAXIMUM_RESOLUTION` and could not configure `8192x6144`, which failed at `isSessionConfigurationSupported` with *Invalid session configuration*. **No client can reach the unbinned geometry on this build**, however correct its code. That is the whole blocker, and it is table content rather than a gate.

`d0015` and `d0016` are absent for a different and already-diagnosed reason: after the NOP their third condition reads an entry count of zero at `[x23+0xd444]`, so their source arrays are empty data. The framework needs them to build a `StreamConfigurationMap`, which is why `get()` on the max-res map returns **null** rather than throwing — a behaviour `IMPL-45` measured and which any client here must handle.

The three tables are therefore one body of work: `d0014` needs correct rows, and `d0015`/`d0016` need rows for whatever `d0014` ends up carrying, or the framework-side map stays null even after `d0014` is right.

The vibecoding slice strategy is to keep the expensive question last. Locate the source arrays and understand why `d0014` carries `1920x1080` before writing anything; add rows for **one** format at full resolution and confirm the service accepts a session; only then extend to the rest and take the capture. The instrument for the final measurement already exists and is committed — `tools/pixelmode-probe/` produces the result metadata directly, and `tools/pixelmode-probe/unfold_test.py` measures the delivered payload.

What should not be over-planned: a general mechanism for keeping the six stream and duration tables consistent, or duration values tuned for performance. Honest rows for the formats that matter are the deliverable.

One genuine unknown shapes the risk section rather than the work breakdown. There are **42 further bit-28 sites** outside the metadata region, in `0x17`/`0x18`/`0x19`, which are untouched and unexamined. They may be the runtime path that would actually reprogram the sensor. `IMPL-45` deliberately did not touch them, and this sub-plan does not either unless the measurement points there — at which point it is a routed decision, not a scope expansion taken by the implementer.

## 4. Scope

- Retroactive ownership of the landed ultra-high-resolution work: the eighteen-site patch, the published capability and tags, and the `IMPL-44`/`IMPL-45`/`IMPL-46` findings, so the record has an owner.
- Location of the source arrays behind `d0014`, `d0015` and `d0016`, and a determination of **why** `d0014` carries seven rows of `1920x1080` — whether that is a stub, a fallback, or a real table populated from a source that is itself wrong.
- Population of `d0014` with the unbinned geometry for the RAW formats that already appear at `8192x6144` in the default stream table.
- Population of `d0015` and `d0016` with duration rows for whatever `d0014` carries, sufficient for the framework to build a non-null `MAXIMUM_RESOLUTION` stream map.
- A full-resolution `MAXIMUM_RESOLUTION` capture through `tools/pixelmode-probe/`, reporting `SENSOR_PIXEL_MODE`, `SENSOR_RAW_BINNING_FACTOR_USED` and `SCALER_CROP_REGION` from the result.
- Measurement of the delivered payload with `tools/pixelmode-probe/unfold_test.py`, to state whether fault 2 persists, changes, or disappears once fault 1 is addressed.
- A stated verdict on whether the sensor leaves binning, and routing of the consequence — including the 42 untouched bit-28 sites — as a decision rather than an action.
- Recording of every located address into `Planner-docs/Project-Ontology.md` section 6 during the session that produces it.

## 5. Out of Scope

- **Fault 2, the stride error.** `IMPL-46` characterised it and it is a separate defect at a different boundary. This sub-plan measures whether it persists; it does not fix it, and a fix would be a new routed decision.
- `d000b` and `d000c`, the default-mode duration tables. Those are `Faz4.2`, and the boundary between the two sub-plans is exactly the `MaximumResolution` suffix.
- Narrowing RAW emission and the format-32 extension, which are `Faz4.1` by `DEC-11`.
- Patch table consolidation (`Faz4.3`) and the consolidated compatibility survey (`Faz4.4`).
- **Applying `agc-50mp-yama/hal-binsel-deneme.patch`.** It is an alternative strategy that removes the capability this sub-plan depends on.
- **Patching the 42 bit-28 sites in regions `0x17`/`0x18`/`0x19`.** They are untouched and unexamined, and touching them reflexively to force a positive result is explicitly forbidden. If the measurement implicates them, that is a routed decision.
- Any change to the sensor mode blobs, the ten-mode dispatch, or `com.qti.sensormodule.ishtar_semco_imx989_wide.bin`.
- Any change to the confirmed `f0006`, `f0000` and `f000a` write sites, which are re-applied unchanged as the state under test.
- Modifying AGC. This sub-plan's client is `tools/pixelmode-probe/`, and AGC is not ultra-high-resolution aware.
- Reopening the capability question. `IMPL-44` settled it and it is not re-argued.

## 6. Current Repository Evidence

Everything below is measured and committed, not assumed.

**The applied patch.** `agc-50mp-yama/hal-uhrfull-deneme.patch`, eighteen rows of `tbz wK,#0x1c,<skip> -> nop`, applied on the seven-word stack. Pre-committed host-side md5 `c094101de0184e9216a57020873bac0b` → **`ce419bc901bea61945d166aee11e1ab0`**, matched exactly on the device and re-verified at the head of `IMPL-45` and again in this session. The binning-selector precondition `[S+0x3d84] == 1` is untouched and satisfied.

**The published state**, from `dumpsys media.camera` bounded to camera 2's own static block. Capability list `[0, 9, 3, 7, 4, 5, 1, 6, 2, 16, 19, 18]` with `16 = ULTRA_HIGH_RESOLUTION_SENSOR`. `d0014` `int32[28]`, seven rows, all `1920x1080`. `d0017` `int32[12]`. `d0015` and `d0016` absent. `colorFilterArrangement` `BGGR`. Camera enumeration intact at 13 devices.

**The client and its results.** `tools/pixelmode-probe/` — a bare `classes.dex` run through `app_process` as the shell user, which holds `android.permission.CAMERA`. At `1920x1080` with `OutputConfiguration.addSensorPixelModeUsed(MAXIMUM_RESOLUTION)`: result `SENSOR_PIXEL_MODE = 1`, `SCALER_CROP_REGION = Rect(0, 0 - 8192, 6144)`, `SENSOR_RAW_BINNING_FACTOR_USED = true`. The DEFAULT control on the same session shape: `0`, `Rect(0, 0 - 4096, 3072)`, `true`. At `8192x6144`: session configuration refused.

**The payload measurement.** `IMPL-46` established that the delivered `8192x6144` RAW10 buffer carries exactly `4096x3072 = 12,582,912` pixels written contiguously, with `bayer_ratio` `0.98x` read at 8192 wide against **`15.66x`** read at 4096 wide, and black `0.0000` when un-folded against `0.7500` as delivered. Fault 2 is characterised; fault 1 is what this sub-plan attacks.

**The conflicting table.** `agc-50mp-yama/hal-binsel-deneme.patch`, 39 rows, prepared and committed but **never applied**. It zeroes `[S+0x3d84]`, three of whose sites are the precondition of these very emissions, and the capability filter tests the same selector with `cbz`. Applying it removes both the tags and the capability. The two tables are alternative strategies and must never be applied together.

**Method constraints that already cost time.** `radare2` and `rabin2` do not complete on this binary (`EV-17`), so static work is scripted per `docs/reverse-engineering-toolchain.md`. CamX log masks are inert on this build (`IMPL-42`), so no `SensorMode` dump line is reachable and the result metadata is the instrument. `logcat | grep` counts the command itself; redirect to a device file and read that.

## 7. Planned Work Breakdown

- F4.7-01 — Adopt the landed work into the record
  - Description: Record in this sub-plan and in the ledger that `IMPL-44`, `IMPL-45` and `IMPL-46`'s ultra-high-resolution findings now have an owner, and reconcile the corrected `Faz4.2` attribution so no later reader inherits it a fourth time.
  - Output: An ownership statement and a reconciled ledger, with no technical claim restated that the diagnosis document already carries.
- F4.7-02 — Locate the three table sources
  - Description: Find where `d0014`, `d0015` and `d0016` are populated, using the tag identifiers and the already-located emission region `0x1660000`-`0x16b0000`. Determine the relationship between them and the default `availableStreamConfigurations` emission, since a shared loop and separate loops imply different patch strategies.
  - Output: Three located sites with their population mechanism described, and the entry-count word at `[x23+0xd444]` confirmed or corrected.
- F4.7-03 — Explain the `1920x1080` rows
  - Description: Determine why `d0014` carries seven formats at exactly one size. Distinguish a hardcoded stub, a fallback path taken because a real source is empty, and a genuine table whose source array is wrong. The three cases have different fixes and only one of them is a row edit.
  - Output: A stated cause for the `1920x1080` content, with the evidence that discriminates it from the other two cases.
- F4.7-04 — Choose the row set and the duration values
  - Description: Select which formats get full-resolution max-res rows, preferring those already present at `8192x6144` in the default table, and choose minimum frame duration and stall duration for each. Cite the vendor tables or the recorded `66,666,666` nanosecond measurement rather than inventing values, and state where no reference exists.
  - Output: A row table and a duration table, each value justified or explicitly marked as derived.
- F4.7-05 — Land one format and prove the session
  - Description: Apply rows for a single format at `8192x6144` under `IMPL-23` md5 discipline, and confirm with the probe that `isSessionConfigurationSupported` returns true and the framework's max-res stream map is no longer null. One format first, because a rejected session after a full table edit does not say which row was wrong.
  - Output: A configurable full-resolution max-res session, or a stated failure with the service's exact rejection.
- F4.7-06 — Extend to the chosen row set
  - Description: Apply the remaining rows, verify the camera service dump reports `d0014`, `d0015` and `d0016` consistently for the same formats and sizes, and confirm camera enumeration is still 13 devices.
  - Output: A dump verification showing the three tables mutually consistent, with enumeration intact.
- F4.7-07 — Take the measurement
  - Description: Capture at `8192x6144` with `pixelMode = MAXIMUM_RESOLUTION` and a DEFAULT control of the same session shape, and report `SENSOR_PIXEL_MODE`, `SENSOR_RAW_BINNING_FACTOR_USED` and `SCALER_CROP_REGION` from both results. Then measure both payloads with `unfold_test.py` and report the `bayer_ratio` and black fraction for each.
  - Output: The paired result metadata and the paired payload measurement, reported whichever way they come out.
- F4.7-08 — State the verdict and route the consequence
  - Description: State whether the sensor leaves binning, whether fault 2 persists independently of fault 1, and what `FIND-4.5-02` and `FIND-3.5-01` now stand at. Route any implication for the 42 untouched sites to the user as a decision. Record the located addresses into `Planner-docs/Project-Ontology.md` section 6.
  - Output: A verdict, a routed decision if one is implied, and an updated address book.

## 8. Acceptance Criteria

- The three table sources are located and their population mechanism is described, with the `1920x1080` content explained by a stated cause rather than by assumption.
- `d0014` carries at least one full-resolution row, and `d0015`/`d0016` carry matching duration rows, verified in the camera service dump for the same format and size.
- `CameraCharacteristics.get(SCALER_STREAM_CONFIGURATION_MAP_MAXIMUM_RESOLUTION)` returns a **non-null** map, and `isSessionConfigurationSupported` returns true for an `8192x6144` stream declaring `MAXIMUM_RESOLUTION`.
- A capture exists whose result reads `SENSOR_PIXEL_MODE = MAXIMUM_RESOLUTION` at `8192x6144`, paired with a DEFAULT control of the same session shape.
- `SENSOR_RAW_BINNING_FACTOR_USED` is reported for both captures and a verdict is stated on whether the sensor left binning. **A `true` reading satisfies this criterion**; the criterion is a measured answer, not a particular answer.
- The delivered payload is measured with `unfold_test.py` and the state of fault 2 is stated as persisting, changed, or absent.
- Camera enumeration is still 13 devices, and every HAL table carries a host-side md5 pre-committed before any device write.
- Every located address is written into `Planner-docs/Project-Ontology.md` section 6 during the session that produced it.
- No claim in the run record conflates a metadata verdict with an image verdict while `FIND-3.5-01` is open.

## 9. Validation and Test Approach

- `VAL-UHRMD5` — every HAL table's host-side md5 computed and committed **before** any device write, then matched on the device, per `IMPL-23` discipline. The live baseline is `ce419bc901bea61945d166aee11e1ab0`.
- `VAL-UHRTABLE` — `dumpsys media.camera` redirected to a device file and pulled, with `d0014`, `d0015`, `d0016` and `d0017` read from **camera 2's own static block**, bounded by the `device@1.1/vendor_qti/N` headers. `IMPL-45` established that an unbounded read attributes another device's rows to camera 2.
- `VAL-UHRSESSION` — `tools/pixelmode-probe/` reporting `isSessionConfigurationSupported` and whether the max-res stream map is null, at `8192x6144` with the mode declared.
- `VAL-UHRRESULT` — `SENSOR_PIXEL_MODE`, `SENSOR_RAW_BINNING_FACTOR_USED` and `SCALER_CROP_REGION` read from the `TotalCaptureResult` in the client, not from `dumpsys`, for both the max-res capture and its DEFAULT control.
- `VAL-UHRPAYLOAD` — `tools/pixelmode-probe/unfold_test.py` on the delivered buffer, reporting `bayer_ratio` at both widths plus the horizontal control, and the black fraction by PIL, grayscale, threshold `< 4`, on the original.
- `VAL-UHRENUM` — camera enumeration counted at 13 devices after every table change, since `IMPL-44` established that an inconsistent feature set can drop the camera list.
- `VAL-SMOKE` — `bash scripts/smoke.sh -o <UTC>__Faz4.7__<label>` before and after every measurement, with the comparable regions diffed.
- `VAL-DOCS` — the continuity updates read back before the session ends.
- `VAL-ONTOLOGY` — the located addresses present in `Planner-docs/Project-Ontology.md` section 6.

Local versus live: `F4.7-02`, `F4.7-03` and `F4.7-04` are entirely host-side static work and need neither the device nor the user. `F4.7-05`, `F4.7-06` and `F4.7-07` are live and involve HAL writes under md5 discipline. `F4.7-01` and `F4.7-08` are documentation. Security validation is not applicable. Ontology validation is central, because three table addresses are the durable output even if the measurement comes out negative.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| agc-50mp-yama/hal-uhrfull-deneme.patch | existing | The eighteen-site bit-28 table that publishes the capability and the tags. Re-applied unchanged as the state under test. | VAL-UHRMD5, VAL-UHRTABLE |
| agc-50mp-yama/hal-maxres-tables-deneme.patch | proposed | The `d0014` / `d0015` / `d0016` row edits, in the Faz1.3 patch table format. | VAL-UHRMD5, VAL-UHRTABLE, VAL-UHRENUM |
| tools/pixelmode-probe/PixelModeProbe.java | existing | The Camera2 client that declares the pixel mode and reports the result metadata. | VAL-UHRSESSION, VAL-UHRRESULT |
| tools/pixelmode-probe/unfold_test.py | existing | The payload geometry measurement that states whether fault 2 persists. | VAL-UHRPAYLOAD |
| tools/pixelmode-probe/measure_raw10.py | existing | The black-fraction measurement, on the original buffer. | VAL-UHRPAYLOAD |
| docs/raw-geometry-diagnosis.md | modified | The record: located sources, the `1920x1080` cause, the row set, the verdict, and the routed consequence. | VAL-UHRTABLE, VAL-UHRRESULT, VAL-DOCS |
| Planner-docs/Project-Ontology.md | modified | Section 6 address book entries for the three located table sources. | VAL-ONTOLOGY |
| agc-50mp-yama/hal-binsel-deneme.patch | existing | The conflicting alternative table. Present so the conflict stays visible; **never applied by this sub-plan**. | VAL-UHRTABLE |
| scripts/smoke.sh | existing | The bracket around every measurement. | VAL-SMOKE |
| docs/reverse-engineering-toolchain.md | existing | The scripted disassembly procedure required by `EV-17` for the static half. | VAL-UHRTABLE |

## 10. Dependencies and Sequencing

**Depends on** `IMPL-44`'s applied patch, which is live and verified by md5, and on `tools/pixelmode-probe/`, which is committed and working. Both are satisfied; this sub-plan starts with its instrument already built, which is unusual for this project and is the reason its first live slice is cheap.

**Independent of** `Faz4.1` and `Faz4.2`. This is worth stating because the surrounding phase is heavily ordered. `Faz4.1` narrows the **default** stream table and adds format 32 to it; `Faz4.2` adds duration rows to the **default** duration tables. Neither touches the `MaximumResolution` variants, and the `MaximumResolution` tables have their own emission sites. The boundary is the suffix. If `F4.7-02` finds that the max-res tables are populated from the same loop as the default ones, that independence is void and the sequencing must be re-decided — which is a finding to route, not a scope expansion.

**Sequencing within Phase 4.** This sub-plan does not displace the established order. `Faz4.1` remains the queue's next item, and this sub-plan's own host-side half — `F4.7-02` through `F4.7-04` — needs neither the device nor the user and can run in any gap. Its live half should follow `Faz4.1` so that only one sub-plan is writing HAL tables at a time, which the `hal-binsel` conflict makes a safety matter rather than a preference.

**Blocks nothing.** No other sub-plan waits on this one. `FIND-4.5-02` waits on it, but a finding is not a sub-plan.

## 11. Risks and Mitigations

- **The `1920x1080` rows are not a stub, and there is no row to edit.** This is the `F4.5-05` failure mode repeating: the project has already spent a slice discovering that `80340003` has no patchable word. Mitigation: `F4.7-03` exists specifically to answer this **before** any patch is designed, and its three candidate causes have different fixes. If the answer is "no patchable row", that is a negative result to record and route, and the sub-plan stops rather than escalating to the 42 sites.
- **Filling the tables does not move the sensor.** The mode may be honoured only in the crop domain, exactly as `IMPL-45` measured at `1920x1080`. Mitigation: this is named in section 2 as an acceptable outcome, and the acceptance criteria are written so that `rawBinningFactorUsed = true` **satisfies** them. The risk is to the project's hopes, not to the sub-plan's validity.
- **An inconsistent feature set drops the camera list.** `IMPL-44` recorded exactly why it applied eighteen sites rather than four: publishing a capability without its supporting tables breaks `getStreamConfigurationMap` and can drop enumeration. Adding stream rows without duration rows is the same hazard in a smaller form. Mitigation: `VAL-UHRENUM` after every table change, and `F4.7-05` lands one format with all three tables together rather than one table at a time.
- **The temptation to patch the 42 sites.** A negative result at `F4.7-07` makes them look like the obvious next move. Mitigation: they are in Out of Scope, the handoff record already forbids patching them reflexively to force a positive, and `F4.7-08` routes rather than acts.
- **Applying `hal-binsel-deneme.patch` by accident.** It is committed, it looks relevant, and it would silently remove the capability this sub-plan depends on. Mitigation: it appears in the Implementation Contract as `existing` with "never applied by this sub-plan" in its purpose, so a reader of the contract meets the conflict before the file.
- **Duration values invented rather than measured.** `Faz4.2`'s own description warns that stall duration in particular differs by format. Mitigation: `F4.7-04` requires each value to cite a vendor reference or the recorded measurement, or be explicitly marked derived.
- **A device write with no rollback point.** Mitigation: the revert chain is recorded and each step md5-verified — `ce419bc9` reverts to `c094101d` via the `hal-uhrfull` table's stock column, and `c094101d` to `fe0245a4` via `revertstack.sh` — and `VAL-SMOKE` brackets every measurement.

## 12. Desired End State

The three `MaximumResolution` table sources are located, named in the ontology address book, and their contents explained. Either `d0014`, `d0015` and `d0016` carry consistent full-resolution rows and a `MAXIMUM_RESOLUTION` session at `8192x6144` configures and captures — or there is a recorded, evidenced reason why they cannot on this build.

In the first case the project has its answer to the question it has been unable to ask since `IMPL-43`: a paired capture, at full size, with `SENSOR_RAW_BINNING_FACTOR_USED` read from the result for both pixel modes, and a payload measurement saying whether the stride fault survives independently. In the second case the project has a negative result with a located cause, which is worth more than an untested hypothesis and is what `F4.5-05` produced for the vendor tag.

Either way the ultra-high-resolution line has an owner, the record no longer misattributes it to `Faz4.2`, and the device is left in a state whose md5 is recorded and whose revert path is verified.

## 13. Next Sub-Phase Transition Criteria

This sub-plan is complete when `F4.7-08` has stated a verdict on whether the sensor leaves binning and recorded the located addresses. It transitions to `Faz4.3` for patch table consolidation, since any table it lands becomes a candidate for the consolidated artifact and `Faz4.3` is where the two-state `halpatch.sh` assumption is reconciled.

It transitions **out of Phase 4 entirely** only if the verdict is that no change within this project's reach makes the sensor read out unbinned. That is a `FIND-3.5-01` closure condition and a routed decision for the user, not a determination this sub-plan makes alone.

If `F4.7-03` finds the max-res tables share an emission loop with the default ones, this sub-plan pauses and the Phase 4 ordering is re-decided, because the independence claimed in section 10 would be void.
