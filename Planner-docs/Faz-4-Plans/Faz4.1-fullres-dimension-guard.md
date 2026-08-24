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
- A target array entry count stated numerically before the work, so success is measurable rather than qualitative.
- Verification that RAW10 and RAW_SENSOR remain advertised at 8192x6144 after narrowing, since removing the goal along with the excess is the obvious failure mode.
- Verification that the AGC path still behaves as Faz 3.5 established, per the Faz 3.6 preservation requirement.
- Recording of any newly located address into Project-Ontology section 6 during the session.

## 5. Out of Scope

- Adding `availableMinFrameDurations` or `availableStallDurations` rows. Faz 4.2 owns those.
- Consolidating or relocating patch tables. Faz 4.3 owns that.
- The full consumer compatibility survey, which is Faz 4.4.
- Any change to `pixelArraySize` or to the active array. Those were settled in Phase 3 and must be preserved, not revisited.
- Any change to the sensor layer, the blobs, or the ten-mode dispatch.
- Composing 50 MP with LN modes, which is Phase 5.
- Reopening the format range decision. Which formats are admitted was decided by the experiment; this sub-phase constrains where they are emitted.

## 6. Current Repository Evidence

Project-Ontology section 6 records the function and the gate precisely. `InitializeScalerStaticCaps` spans `0x16bf4c0` to `0x16c5a90`, 26 KB and 6,516 instructions, and emits 16-byte entries of the form `{format, width, height, direction}` into an array at `[x?+0xb10]`. The format gate is `sub wN, wFmt, #0x22` then `cmp wN, #2` then `b.lo`, admitting 0x22 and 0x23, with separate tests admitting 0x36 and 0x21. The four `cmp wN,#2` sites are `0x16c18dc`, `0x16c1c18`, `0x16c22bc`, and `0x16c2330`, with the recorded correction that `0x16c2334` is the following branch rather than the `cmp`.

`agc-50mp-yama/hal-raw50-deneme.patch` was read in this run and holds the four entries as four-byte indices: `5965367`, `5965574`, `5965999`, and `5966028`. Multiplied by four these give `0x16C18DC`, `0x16C1C18`, `0x16C22BC`, and `0x16C2330` — an exact match with the ontology, which confirms both records independently.

Each entry's byte pair shows the instruction change: `\177\011\000\161` becomes `\177\025\000\161`, `\377\010\000\161` becomes `\377\024\000\161`, and `\237\012\000\161` becomes `\237\026\000\161` at two sites. These are the encoded `cmp` immediates moving from 2 to 5.

The patch records the measured effect: the array grows from 508 to 868 int32 entries — a 360-entry increase — and the entries added at full resolution are `[37 8192 6144 OUTPUT]`, `[38 8192 6144 OUTPUT]`, and `[36 8192 6144 OUTPUT]`.

That arithmetic gives the target. Each entry is four int32 values, so 360 int32 is 90 entries added, of which only three are wanted. A correctly narrowed patch should produce an array of roughly 520 int32 rather than 868 — twelve int32 above the 508 baseline. This number should be stated as the target before the work begins.

Project-Ontology section 6 also records the vendor table evidence explaining why the patch is needed at all: `org.codeaurora.qcamera3.quadra_cfa.availableStreamConfigurations` carries only formats 33, 34, and 35 at 8192x6144, while `xiaomi.scaler.availableStreamConfigurations` already carries `[37 8192 6144 0]`, `[32 8192 6144 0]`, and `[36 8192 6144 0]`. The values exist in a vendor table and not in the standard one.

`ishtar-cam-modes/blobs/hal-fullres.patch` shows what a narrow patch looks like in this codebase: 16 entries changing `LDR Wn,[Xm,#0x3d84]` to `MOV Wn,#0`, with the ontology noting the binary has 55 accesses to that offset in total. The existing patch already demonstrates selective application.

## 7. Planned Work Breakdown

- F4.1-01 — State the target array count before starting
  - Description: Compute and record the expected post-narrowing entry count from the 508 baseline plus the three wanted entries. This makes the acceptance criterion a number rather than a direction.
  - Output: A stated numeric target.
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
- F4.1-06 — Verify the goal survived
  - Description: Confirm RAW10 and RAW_SENSOR are still advertised at 8192x6144 and that no spurious entries remain at other resolutions.
  - Output: A stream configuration verdict.
- F4.1-07 — Verify the Phase 3 preservation requirement
  - Description: Confirm the AGC path still behaves as Faz 3.5 established, per the requirement Faz 3.6 handed forward.
  - Output: A preservation verdict.
- F4.1-08 — Record addresses during the session
  - Description: Write any newly located address or instruction detail into Project-Ontology section 6 as it is found.
  - Output: An updated address book.

## 8. Acceptance Criteria

- The target array entry count is stated numerically before any patch is applied.
- The single-site measurement is taken and compared against prediction before the remaining sites are touched.
- The final array entry count matches the stated target, within an explained margin.
- RAW10 and RAW_SENSOR remain advertised at 8192x6144 after narrowing.
- No RAW format entries remain at resolutions other than the full-resolution dimension.
- The Phase 3 preservation requirement is verified, not assumed.
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

The RAW format emission is restricted to the full-resolution dimension only. The stream configuration array carries the three wanted entries and none of the excess, at a count matching a target stated before the work began. RAW10 and RAW_SENSOR remain advertised at 8192x6144, the Phase 3 result is preserved and verified, and every located address is in the ontology.

The evidence an implementer should produce is the stated target, the single-site delta, the final delta, the stream configuration rows, and the preservation verdict.

The ledger summary Step 4 should append records: the target count, the measured count, the sites guarded, whether the Phase 3 result survived, and the addresses added.

## 13. Next Sub-Phase Transition Criteria

- The final array entry count matches the pre-stated target within an explained margin.
- RAW10 and RAW_SENSOR are confirmed at 8192x6144 with no spurious entries elsewhere.
- The Phase 3 preservation requirement is verified by measurement.
- The narrowed patch is expressible within the four-byte alignment constraint.
- Newly located addresses are recorded in the ontology.
- Faz 4.2 has a stable entry set to add duration rows for.
