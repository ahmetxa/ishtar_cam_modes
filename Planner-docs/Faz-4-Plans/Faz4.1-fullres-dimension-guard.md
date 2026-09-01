# Faz 4.1 — Full Resolution Dimension Guard

## 1. Context

Main-Planing Phase 4's goal is "Reduce the experimental patch to the smallest change that is also internally consistent." Its description identifies the specific excess: "The four-instruction experiment (`cmp wN,#2` → `cmp wN,#5` at four sites in `InitializeScalerStaticCaps`, 0x16bf4c0–0x16c5a90) currently adds RAW formats at *every* resolution, growing the stream-configuration array from 508 to 868 int32 entries. Narrow the emission to the QCFA full-resolution dimension only."

The experimental patch says the same thing about itself. Its header, read in this run, carries a warning in capitals: this patch adds raw formats not only at full resolution but at every resolution, growing the array by 360 int32 entries, and it needs narrowing.

Autopsy files it as `AUTOPSY-P2-02` — "Experimental HAL patch is over-broad" — with the impact stated as "a larger blast radius than the goal requires" and the Step 2 impact requiring "Phase 4 acceptance criteria must state the target array size and require the duration rows the user explicitly asked for."

Project-Comprehension frames the trade in `QAS-04`: "Narrowing costs additional reverse engineering in Phase 4; shipping broad costs unknown compatibility risk. Narrowing wins because the patch is intended for distribution." `CQ-07` — "What is the smallest correct HAL patch?" — is the open question this sub-phase begins to close.

The starting point is well characterized. Project-Ontology section 6 records the format gate instruction by instruction and gives the four `cmp` site addresses, and the experimental patch's own indices confirm them arithmetically.

## 2. Goal

Restrict the added RAW format emission to the sensor's full-resolution dimension only, reducing the stream configuration array growth to the minimum the goal requires, without disturbing whatever configuration made the AGC capture complete.

## 3. Description

The problem is that the working experiment widened a format range test, and a format range test does not know about resolution. Admitting formats 0x24 through 0x26 at every emitted resolution produces entries nobody asked for at sizes nobody will use, each of which is an advertised capability the framework and every consumer must reason about.

It belongs after Phase 3 because narrowing a patch whose effect has not been proven is premature — Main-Planing sequences it deliberately this way. It reduces risk in the concrete sense `QAS-04` describes: this patch is intended for distribution, and a broad patch's compatibility cost is unmeasurable across users who have applications the project has never tested.

The vibecoding slice strategy comes straight from Main-Planing: "Add a guard on the full-resolution dimension at one of the four sites and measure the array-size delta." One site, one measurement. If the delta moves in the expected direction and by roughly a quarter of the excess, the approach is validated and the remaining three sites follow. The fastest validation signal is the array entry count that the Faz 2.1 smoke script already reports as a number.

What should not be over-planned: the duration rows. Faz 4.2 owns those, and adding them while also narrowing the emission would bundle two changes into one measurement. The sequence matters: narrow first, so the duration rows are added only for entries that survive.

The preservation requirement from Faz 3.6 governs this sub-phase. If Phase 3 produced a working capture, this narrowing must not break it, and the AGC path becomes a required check rather than an optional one.

## 4. Scope

- Identification of where in `InitializeScalerStaticCaps` a resolution guard can be applied, given that the current gate tests format rather than size.
- A single-site guard applied first, with the array delta measured before the remaining sites are touched.
- Extension to the remaining sites once the approach is validated.
- A target array entry count stated numerically before the work, naming the camera id and the metric it is counted on, so success is measurable rather than qualitative.
- **Extending RAW emission to format 32 (`RAW_SENSOR`) at 8192x6144, per `DEC-11`.** The `0x22..0x26` gate cannot reach format 32 = `0x20`, which sits below its subtract base, so `RAW_SENSOR` was never emitted there and no narrowing can make it appear. Extending emission is what makes section 8's `RAW_SENSOR` criterion satisfiable, and it is the same change `OQ-02` and `FIND-3.5-02` need, since a full-resolution DNG is unobtainable without it.
- Verification that RAW10 remains advertised at 8192x6144 after narrowing and that `RAW_SENSOR` is newly advertised there after the format-32 extension, since removing the goal along with the excess is the obvious failure mode.
- Verification that the AGC path still behaves as Faz 3.5 established, per the Faz 3.6 preservation requirement — measured against the corrected geometry `Faz-4-Plans/Faz4.5-active-array-raise.md` produces, not against the corrupt frame.
- Recording of any newly located address into Project-Ontology section 6 during the session.

**The accepted tension, stated rather than glossed.** The format-32 extension **widens** a gate inside a sub-plan whose entire purpose is narrowing what that gate emits. `DEC-11` put this to the user and it was accepted on the condition that the two effects never be reported as one figure: **the narrowing delta and the format-32 addition are separate numbers.** A single net array count would let one movement mask the other, and a narrowing that overshot could be hidden by an addition that overshot the other way.

## 5. Out of Scope

- Adding `availableMinFrameDurations` or `availableStallDurations` rows. Faz 4.2 owns those.
- Consolidating or relocating patch tables. Faz 4.3 owns that.
- The full consumer compatibility survey, which is Faz 4.4.
- Any change to `pixelArraySize`. The `f0006` write site at `0x0166645c` was settled in Phase 3, is confirmed by measurement, and must be preserved exactly — this sub-plan verifies it still reads `[8192 6144]` and does not touch it.
- **The active-array raise, which is a dependency rather than an exclusion.** `f0000`, `f000a` and `org.codeaurora.qcamera3.quadra_cfa.activeArraySize (80340003)` are raised from `[0 0 4096 3072]` by `Faz-4-Plans/Faz4.5-active-array-raise.md`, sequenced **before** this sub-plan by `DEC-12`. This sub-plan neither performs that work nor excludes it from Phase 4: it runs after it and inherits its result. The earlier text here read "settled in Phase 3 and must be preserved, not revisited", which contradicted `IMPL-24`'s preservation requirement and was the defect `IMPL-25` stopped on.
- Any change to the sensor layer, the blobs, or the ten-mode dispatch.
- Composing 50 MP with LN modes, which is Phase 5.
- Reopening the format range decision beyond the one addition `DEC-11` authorises. Formats 34 through 38 stay as the experiment decided them; format 32 is added because section 8 requires it and nothing else can supply it. No further format is admitted here.

## 6. Current Repository Evidence

Project-Ontology section 6 records the function and the gate precisely. `InitializeScalerStaticCaps` spans `0x16bf4c0` to `0x16c5a90`, 26 KB and 6,516 instructions, and emits 16-byte entries of the form `{format, width, height, direction}` into an array at `[x?+0xb10]`. The format gate is `sub wN, wFmt, #0x22` then `cmp wN, #2` then `b.lo`, admitting 0x22 and 0x23, with separate tests admitting 0x36 and 0x21. The four `cmp wN,#2` sites are `0x16c18dc`, `0x16c1c18`, `0x16c22bc`, and `0x16c2330`, with the recorded correction that `0x16c2334` is the following branch rather than the `cmp`.

`agc-50mp-yama/hal-raw50-deneme.patch` was read in this run and holds the four entries as four-byte indices: `5965367`, `5965574`, `5965999`, and `5966028`. Multiplied by four these give `0x16C18DC`, `0x16C1C18`, `0x16C22BC`, and `0x16C2330` — an exact match with the ontology, which confirms both records independently.

Each entry's byte pair shows the instruction change: `\177\011\000\161` becomes `\177\025\000\161`, `\377\010\000\161` becomes `\377\024\000\161`, and `\237\012\000\161` becomes `\237\026\000\161` at two sites. These are the encoded `cmp` immediates moving from 2 to 5.

The patch records the measured effect: the array grows from 508 to 868 int32 entries — a 360-entry increase — and the entries added at full resolution are `[37 8192 6144 OUTPUT]`, `[38 8192 6144 OUTPUT]`, and `[36 8192 6144 OUTPUT]`.

That arithmetic gives the target. Each entry is four int32 values, so 360 int32 is 90 entries added, of which only three are wanted. A correctly narrowed patch should produce an array of roughly 520 int32 rather than 868 — twelve int32 above the 508 baseline. This number should be stated as the target before the work begins.

Project-Ontology section 6 also records the vendor table evidence explaining why the patch is needed at all: `org.codeaurora.qcamera3.quadra_cfa.availableStreamConfigurations` carries only formats 33, 34, and 35 at 8192x6144, while `xiaomi.scaler.availableStreamConfigurations` already carries `[37 8192 6144 0]`, `[32 8192 6144 0]`, and `[36 8192 6144 0]`. The values exist in a vendor table and not in the standard one.

`ishtar-cam-modes/blobs/hal-fullres.patch` shows what a narrow patch looks like in this codebase: 16 entries changing `LDR Wn,[Xm,#0x3d84]` to `MOV Wn,#0`, with the ontology noting the binary has 55 accesses to that offset in total. The existing patch already demonstrates selective application.

## 7. Planned Work Breakdown

- F4.1-01 — State the target array count before starting, against a named camera id and metric
  - Description: Compute and record the expected post-narrowing entry count. **The baseline must name a camera id and a metric, because 508 alone names neither and `IMPL-25` stopped on that ambiguity.** The metric is `scripts/smoke.sh`'s `streamcfg` field, which is the **int32** element count read from `android.scaler.availableStreamConfigurations (d000a)` — not an entry count, and each entry is four int32. **508 is hal3 in the fullres state, not hal0.** The recorded values are hal0: stock 440, fullres 456, three-layer 800; hal3: stock 500, fullres 508, three-layer 868. The patch header's "508 -> 868" is therefore hal3's row, and smoke prints hal0's row **first** because its output is sorted by id — so a reading taken from the top line is hal0's and does not compare against 508. State the target for hal0 and for hal3 explicitly, and state which one the acceptance criterion is judged on.
  - Output: A stated numeric target per camera id, on the named metric.
- F4.1-01b — State the format-32 addition as its own number
  - Description: Separately from the narrowing target, state how many int32 the format-32 extension is expected to add at 8192x6144, and on which camera ids. This is the `DEC-11` separation requirement expressed as a work item: two predictions before the work, so two deltas can be checked against them afterwards.
  - Output: A stated numeric addition, distinct from the narrowing target.
- F4.1-02 — Locate the resolution context at each emission site
  - Description: Determine what width and height values are available in registers or memory at each of the four gate sites, since a resolution guard requires the dimension to be reachable there.
  - Output: A per-site resolution availability assessment.
- F4.1-03 — Design the guard
  - Description: Choose the guard form given the four-byte alignment constraint the patch format imposes and the instruction budget available at each site. Record why the chosen form fits within a patch-table entry.
  - Output: A guard design with its constraints stated.
- F4.1-04 — Apply at one site and measure
  - Description: Apply the guard at a single site, restart the camera stack in the safe window, and read the array entry count. Compare against the prediction for a one-site change.
  - Output: A single-site delta measurement.
- F4.1-05 — Extend to the remaining sites
  - Description: Once the one-site result matches prediction, apply at the remaining three and measure again.
  - Output: A full-patch delta measurement against the stated target.
- F4.1-05b — Extend emission to format 32 and measure it separately
  - Description: Apply the `DEC-11` change that admits `RAW_SENSOR` (32 = `0x20`) at 8192x6144, in its own bracketed step after the narrowing has been measured and accepted. Read the resulting delta on its own. **The narrowing delta and this addition are reported as two numbers and are never summed into one net array count** — that condition is what the user accepted the widening under.
  - Output: A format-32 delta, stated separately from the narrowing delta.
- F4.1-06 — Verify the goal survived
  - Description: Confirm RAW10 is still advertised at 8192x6144, confirm `RAW_SENSOR` is now advertised there, and confirm no spurious entries remain at other resolutions — including that the format-32 extension did not reintroduce entries at the resolutions the narrowing removed.
  - Output: A stream configuration verdict, with the RAW10 and `RAW_SENSOR` rows quoted per resolution rather than collapsed.
- F4.1-07 — Verify the Phase 3 preservation requirement
  - Description: Confirm the AGC path still behaves as Faz 3.5 established, per the requirement Faz 3.6 handed forward, and confirm `f0006` still reads `[8192 6144]`. Because `Faz-4-Plans/Faz4.5-active-array-raise.md` runs first, the frame this check preserves is the corrected one; a capture that is geometrically correct before this sub-plan and corrupt after it is a failure of this sub-plan, which is precisely the discrimination `DEC-12` sequenced the two in this order to obtain.
  - Output: A preservation verdict naming the image state before and after.
- F4.1-08 — Record addresses during the session
  - Description: Write any newly located address or instruction detail into Project-Ontology section 6 as it is found.
  - Output: An updated address book.

## 8. Acceptance Criteria

- The target array count is stated numerically before any patch is applied, and it **names a camera id and the metric it is counted on**. A bare number is not acceptable: 508 is hal3-in-fullres on the `streamcfg` int32 count, hal0's fullres figure is 456, and smoke prints hal0 first.
- The format-32 addition is stated as its own predicted number, before any patch is applied, distinct from the narrowing target.
- The single-site measurement is taken and compared against prediction before the remaining sites are touched.
- The final array count matches the stated target, within an explained margin, **reported as two separate deltas — the narrowing and the format-32 addition — and never as one net array count.** A result stated as a single net figure fails this criterion regardless of the figure's value.
- RAW10 remains advertised at 8192x6144 after narrowing.
- **`RAW_SENSOR` (format 32) is advertised at 8192x6144.** This criterion is satisfiable only through the `DEC-11` format-32 extension and **depends on that extension rather than on the narrowing**: the `0x22..0x26` gate admits formats 34–38, format 32 = `0x20` lies below its subtract base, and no narrowing of that gate can ever emit it. `IMPL-25` confirmed this from the patch header's own arithmetic. If the extension is not made, this criterion is unmet and must be reported as unmet rather than reinterpreted.
- No RAW format entries remain at resolutions other than the full-resolution dimension, the format-32 addition included.
- The Phase 3 preservation requirement is verified, not assumed, and `f0006` still reads `[8192 6144]`.
- The capture verified in F4.1-07 is compared against the geometry `Faz-4-Plans/Faz4.5-active-array-raise.md` established, not against the corrupt frame `FIND-3.5-01` described.
- Every measurement has a smoke snapshot bracket and confirms the preference precondition, per the Faz 3.1 checklist.
- Any newly located address is in Project-Ontology section 6 by the end of the session.
- The patch remains expressible as offset entries within the four-byte alignment constraint.

## 9. Validation and Test Approach

Validation is live and quantitative. The array entry count is the primary metric, which is unusual for this project and valuable precisely because it is a number rather than a judgment.

- `VAL-SMOKE` (from Faz 2.1) — the bracket, including the array entry count field that this sub-phase depends on.
- `VAL-ARRAYCOUNT` (proposed) — the stream configuration entry count read before and after each patch application, compared against the stated target.
- `VAL-STREAMROWS` (proposed) — extraction of the RAW format rows to confirm full resolution is present and other resolutions are clean.
- `VAL-AGC` (proposed) — the Phase 3 preservation check: AGC initializes and captures as Faz 3.5 established.
- `VAL-DISASM` (from Faz 1.4) — the static analysis supporting F4.1-02 and F4.1-03.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist.

Local versus live: the guard design is local; every measurement is live. Security validation is not applicable. Ontology validation applies to address recording and to keeping `fullres` distinct from `50mp`.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Bracket plus the array entry count metric. | VAL-SMOKE, VAL-ARRAYCOUNT |
| agc-50mp-yama/hal-raw50-deneme.patch | modified | The experimental table narrowed from four range widenings to guarded emission. | VAL-ARRAYCOUNT, VAL-STREAMROWS |
| Planner-docs/Project-Ontology.md | modified | Record the guard sites and any newly located instruction detail. | VAL-DISASM |
| docs/patch-table-format.md | existing | The alignment and extension constraints the guard must satisfy. | VAL-DISASM |

## 10. Dependencies and Sequencing

**Blocked by `Faz-4-Plans/Faz4.5-active-array-raise.md`, by `DEC-12`.** That sub-plan raises `f0000`, `f000a` and `80340003`, and it runs first so that F4.1-07 preserves a good capture rather than certifying that a half-black frame is still half-black. Do not execute this sub-plan before it lands.

Depends on Faz 3.6 for the preservation requirement and for the decision that Phase 4 should proceed at all. Depends on Faz 1.3 for the format contract's alignment and extension rules, and on Faz 1.4 for the disassembler.

Blocks Faz 4.2, because duration rows should be added only for the entries that survive narrowing. Blocks Faz 4.3 and Faz 4.4, which consolidate and validate the result.

Required decisions: the guard form, which is a technical judgment the implementer records.

Required infrastructure: the device, the module with the patch machinery, and the disassembler.

Required human approvals: applying a HAL patch and running the camera; if the Phase 3 preservation check includes a capture, the user's shutter press.

Fresh session token and context risk: medium. Less than Faz 3.2 because the function is already mapped and the four sites are known, but it is still disassembly work in a 26 KB function.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the resolution is not reachable at the gate sites, so a guard cannot be placed there. Impact: the narrowing approach fails and a different mechanism is needed. Mitigation: F4.1-02 tests this before any design work, so the finding arrives early.
- Risk: the guard removes the three wanted entries along with the eighty-seven unwanted ones. Impact: the patch narrows to nothing and 50 MP regresses. Mitigation: F4.1-06 is a distinct acceptance criterion, and the array count target would also be missed, giving two independent signals.
- Risk (`QAS-04` inverted): narrowing breaks the AGC capture that Phase 3 achieved. Impact: the project trades its headline result for blast-radius reduction. Mitigation: F4.1-07 verifies the preservation requirement explicitly, and the requirement itself was defined in Faz 3.6 for exactly this purpose.
- Risk: all four sites are patched at once and the measurement is ambiguous. Impact: a partial failure cannot be localized. Mitigation: F4.1-04 requires a single-site measurement first, which is Main-Planing's own stated first slice.
- Risk: the guard needs more instruction space than a four-byte-aligned patch entry allows. Impact: the change cannot be expressed in the existing patch format. Mitigation: F4.1-03 checks the constraint at design time, and the format contract from Faz 1.3 states it explicitly.
- Risk: the array count target is set after the measurement to match the result. Impact: the acceptance criterion becomes unfalsifiable. Mitigation: F4.1-01 requires the target before any patch is applied.
- Risk (`R8`): the guard sites are derived and recorded but the underlying binary changes with a system update. Impact: all offsets invalidate together. Mitigation: unchanged from the project's existing posture — the checksum guard is the detector, and the disassembly method is documented so offsets can be re-derived.

## 12. Desired End State

The RAW format emission is restricted to the full-resolution dimension only. The stream configuration array carries the wanted entries and none of the excess, at counts matching the two targets stated before the work began — the narrowing target and the format-32 addition, reported separately. RAW10 remains advertised at 8192x6144 and `RAW_SENSOR` is now advertised there for the first time, the Phase 3 result is preserved and verified, and every located address is in the ontology.

The evidence an implementer should produce is the stated target, the single-site delta, the final delta, the stream configuration rows, and the preservation verdict.

The ledger summary Step 4 should append records: the target count, the measured count, the sites guarded, whether the Phase 3 result survived, and the addresses added.

## 13. Next Sub-Phase Transition Criteria

- The final array entry count matches the pre-stated target within an explained margin.
- RAW10 is confirmed still at 8192x6144 and `RAW_SENSOR` is confirmed newly at 8192x6144, with no spurious entries elsewhere.
- The narrowing delta and the format-32 addition are on record as two numbers.
- The Phase 3 preservation requirement is verified by measurement.
- The narrowed patch is expressible within the four-byte alignment constraint.
- Newly located addresses are recorded in the ontology.
- Faz 4.2 has a stable entry set to add duration rows for.
