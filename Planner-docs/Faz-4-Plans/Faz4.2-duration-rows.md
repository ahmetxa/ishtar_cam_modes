# Faz 4.2 — Minimum Frame and Stall Duration Rows

## 1. Context

Main-Planing Phase 4's surviving second half is the duration rows. Quoted from the **amended** Phase 4 (`DEC-14`, 2026-09-03): "What remains in scope is the honest part of the original goal: add the `availableMinFrameDurations` and `availableStallDurations` rows the emitted entries require, and consolidate the accumulated experimental tables into one packageable artifact with a verified revert path." *(Until planning run 10 this line quoted a pre-`DEC-14` sentence — "the rows the **new** entries require … honest rather than merely accepted by the framework" — which no longer appears anywhere in `Main-Planing.md`. Two things survive it intact: the user's explicit request for the rows, which Autopsy records independently below, and the honesty argument, which the fourth paragraph of this section carries on its own evidence. What changed is the word **emitted**, and that word is the whole of this sub-plan's new size.)*

**Retired history, kept because it explains this sub-plan's original shape.** The pre-`DEC-14` target end state required RAW "advertised at 8192x6144 only at the QCFA full-resolution dimension … with matching `availableMinFrameDurations` and `availableStallDurations` rows". `Main-Planing.md` now carries the dimension half of that phrase **only** as the retired original plan, inside the amended Phase 4's description, immediately followed by "**`IMPL-48` through `IMPL-50` measured that this cannot be done**". The live target end state states the opposite: "The HAL keeps the **broad** RAW emission it currently carries." The duration-row half of the old requirement survives and is this sub-plan; the dimension half does not, and nothing here may be read as attributing it to the current master plan.

Autopsy notes the omission as part of `AUTOPSY-P2-02`: the experimental patch adds RAW formats "with no matching duration rows", and its Step 2 impact requires Phase 4's acceptance criteria to "require the duration rows the user explicitly asked for."

The phrase "honest rather than merely accepted" carries the actual argument. Project-Ontology invariant 7 records the mechanism that makes durations load-bearing on this device: `getOutputSizes` excludes any size whose minimum frame duration exceeds one twentieth of a second, and on camera 3, 8192x6144 measures 66,666,666 nanoseconds against 4096x3072's 33,333,333. Duration values are not decorative metadata on this platform — they are the input to the framework's own bucketing decision, and they were the original root cause of the AGC ceiling.

That gives this sub-phase a subtlety worth naming up front. Adding duration rows for the new entries makes the advertised configuration internally consistent, and the specific values chosen determine which framework list the size lands in. That is a behavior change, not merely a completeness fix.

**Amended 2026-09-03 by `DEC-14` (planning run 8). Narrowing is retired; this sub-plan's premise changes and its scope grows.** `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` is `superseded`, and with it the assumption that this sub-plan would run against a small, narrowed entry set. `IMPL-48` through `IMPL-50` measured that the narrowing cannot be done — it hits every numeric target and still prevents AGC from launching, 3/3 at two independent bisection stages, because the removed rows are load-bearing for gcam's initialisation. **So the table this sub-plan adds duration rows to is the broad one.** Three consequences, none of them cosmetic:

- **The row count is the ninety, not the three.** Section 3's original sequencing argument — "the difference between three rows of work and ninety" — is now a statement of this sub-plan's actual size. Whether every emitted entry needs a row, or only the ones a consumer reads, becomes a scoping decision this sub-plan must take explicitly rather than inherit.
- **The bucketing question changes from a nicety to the phase's main hazard.** `F4.2-05` was written to route a behaviour change for confirmation. Under `DEC-14` that behaviour change is `R12` itself: a minimum frame duration below one twentieth of a second moves `8192x6144` into `getOutputSizes`, where AGC's default largest-size selection would find it — and Phase 3 exists precisely to keep AGC off that path. `DEC-09` is no longer a marginal decision; it is the one that could undo Phase 3 from the HAL side without touching AGC.
- **The preservation criterion inverts.** The old criterion was that narrowing be preserved. The new one, which `IMPL-49` showed the old goal silently violated, is that **AGC still launches and still captures cleanly at 12.58 MP** after the rows are added.

Nothing in the sub-plan's original purpose is retired: the duration rows are, in `Main-Planing.md`'s words for the amended Phase 4, "the honest part of the original goal".

**Amended 2026-09-04 by planning run 10 (`DEC-14` residue).** Run 8's amendment landed its new premise in this section and in sections 2, 3, 4, 5, 7, 8, 10 and 12, then verified itself by searching for `Faz 4.1` and `narrow`. Four pre-`DEC-14` premises survived because none of them contains either string. Repaired here, surgically: the two `Main-Planing.md` quotations opening this section — one no longer exists in the master plan, the other was attributed to the live target end state when the master plan carries it only as retired history; section 3's question of whether the recorded duration value "applies to RAW10 and RAW_SENSOR", which contradicted section 4's own statement that format 32 is never emitted; and the framing in sections 6, 7, 8 and 11 of "the target end state names only RAW10 (37) and RAW_SENSOR (32)" as a live discrepancy to resolve, when the amended target end state names no format set at all and requires the emission to stay broad. **No work item was added or removed, no acceptance criterion was weakened, and no substitute goal was invented** — what was a reconciliation against a named target becomes a scoping decision on its own merits, which is what `DEC-14` actually leaves behind. One line was added to section 13: section 8 has carried the AGC coexistence criterion since run 8 and the transition gate did not.

## 2. Goal

Add matching `availableMinFrameDurations` and `availableStallDurations` rows for the stream configuration entries the **broad** patch emits, so the advertised configuration is internally consistent, with the chosen duration values measured or justified rather than invented, and with the values chosen so that AGC's default selection is not moved onto the 50 MP path by a HAL edit.

## 3. Description

The problem is an advertised capability with incomplete supporting metadata. A stream configuration entry without duration rows tells the framework a size is available without telling it what that size costs, and consumers that compute buffering, pipeline depth, or frame pacing from those tables have nothing to read.

It originally belonged after the narrowing because duration rows are added per entry, and adding them before narrowing would have meant adding eighty-seven rows that were then removed. **`DEC-14` removed the narrowing, so that sequencing argument is void and the ninety is the real number.** The first scoping decision this sub-plan takes is therefore which of the emitted entries need rows at all — an entry no consumer reads may not justify a patched row, and the answer must be argued rather than assumed in either direction.

The vibecoding slice strategy: locate the two duration tables in the binary, determine how they are populated relative to the stream configuration table, add rows for one entry, and measure. The fastest validation signal is the camera service dump reporting the duration rows alongside the stream configuration rows for the same format and size.

What should not be over-planned: duration values for hypothetical future entries, or a general mechanism for keeping the three tables synchronized. **The "three entries need three pairs of rows" figure this paragraph used to carry was a narrowed-table figure and is retired with the narrowing;** the settled row set is `F4.2-01`'s output and may be considerably larger.

The values themselves need care. Project-Ontology invariant 7 records a measured value for 8192x6144 on camera 3 — 66,666,666 nanoseconds — but that measurement was taken for an existing entry rather than for the newly added RAW formats. Whether the same value applies to the RAW formats **actually emitted** at that size — RAW10 (37), RAW12 (38) and RAW_OPAQUE (36), and **not** RAW_SENSOR (32), which section 4 records as never emitted and therefore not row-eligible — is a question this sub-phase must answer rather than assume, because stall duration in particular differs by format: a format requiring remosaic or a reprocessing pass stalls differently from one that does not.

The remosaic question links directly to Faz 3.5's `OQ-02` outcome. If the HAL delivers remosaiced Bayer at full resolution, there is processing behind that frame and the stall duration should reflect it. If it delivers raw Quad-Bayer, the cost profile is different. This is a case where an earlier sub-phase's finding has a direct downstream use.

## 4. Scope

- Location of the `availableMinFrameDurations` and `availableStallDurations` emission sites in the binary, using the tag identifiers already recorded.
- Determination of how those tables are populated relative to the stream configuration table, since a shared loop and separate loops imply different patch strategies.
- Selection of duration values for the formats actually emitted at 8192x6144 — RAW10 (37), RAW12 (38) and RAW_OPAQUE (36) under the current gate — measured where possible and justified where measurement is not available. **RAW_SENSOR (32) is not among them:** the gate admits `0x22..0x26` = 34–38 and `0x20` sits below the subtract base, and `DEC-11`'s format-32 extension lived inside the now-`superseded` `Faz4.1`, where `IMPL-50` measured it as having no additive implementation on a binary with no code cave ≥ 16 bytes. A duration row for a format that is never emitted would be a row for nothing.
- Application of the rows and verification that the camera service dump reports them alongside the matching stream configuration entries.
- Assessment of the framework bucketing consequence: which of the two size lists the entries land in given the chosen minimum frame duration.
- Consumer verification that the added rows did not change behavior for existing entries.
- Recording of the located table addresses into Project-Ontology section 6.

## 5. Out of Scope

- Changing which formats or resolutions are emitted. `DEC-14` settled that by retiring the narrowing: the emission stays broad, and reducing it is not this sub-plan's to attempt.
- Tuning duration values for performance. The goal is honesty, not optimization.
- Consolidating patch tables, which is Faz 4.3.
- The full consumer survey, which is Faz 4.4.
- Any change to `pixelArraySize`, the active array, or the sensor layer.
- Adding duration rows for entries the vendor tables already carry, which are outside this patch's concern.
- Re-deriving the 30 and 15 frames-per-second measurements already recorded; they are inputs, not work.

## 6. Current Repository Evidence

Project-Ontology section 6 records the three relevant tag identifiers under "Related metadata tags": `android.scaler.availableStreamConfigurations` is `d000a`, `availableMinFrameDurations` is `d000b`, and `availableStallDurations` is `d000c`. Their adjacency in the tag space suggests they may be emitted near each other, which is a starting hypothesis for the search rather than a fact.

Invariant 7 records the measured durations that establish the platform behavior: on camera 3, 8192x6144 has a minimum frame duration of 66,666,666 nanoseconds and is therefore excluded from `getOutputSizes`, while 4096x3072 at 33,333,333 nanoseconds is kept. The same invariant records the consequence: this exclusion "was the original root cause of AGC's 12.6 MP ceiling, and it is why Open Camera — which reads both lists — reached 50.3 MP unaided."

That last point has a direct bearing on value selection. If a duration below the one-twentieth-second threshold were chosen for the new entries, they would appear in `getOutputSizes` rather than only in `getHighResolutionOutputSizes` — which would change AGC's behavior without touching AGC. Whether that is desirable is a question this sub-phase should raise rather than decide unilaterally. **Under `DEC-14` the application-level control it interacts with is Phase 3's photo-size pin, not the smali patch in `agc-50mp-yama/README.md` alone:** crossing the threshold puts `8192x6144` back where AGC's default largest-size selection finds it, which is `R12`, and `F4.2-05` is the gate that catches it.

`agc-50mp-yama/hal-raw50-deneme.patch` records the three entries needing rows: `[37 8192 6144 OUTPUT]`, `[38 8192 6144 OUTPUT]`, and `[36 8192 6144 OUTPUT]` — RAW10, RAW12, and RAW_OPAQUE, at full resolution. **Those three are the emitted set at that size, and there is no longer a competing named set to reconcile them against.** The pre-`DEC-14` target end state named RAW10 (37) and RAW_SENSOR (32); the amended one names no format set and requires instead that "the HAL keeps the **broad** RAW emission it currently carries". What survives as real work is therefore not a discrepancy but a scoping question — which of the entries the broad table emits, at full resolution and at every other resolution, justify a patched duration row. That is `F4.2-01`.

Project-Ontology section 6 records that `xiaomi.scaler.availableStreamConfigurations` already carries `[37 8192 6144 0]`, `[32 8192 6144 0]`, and `[36 8192 6144 0]`. That vendor table may also carry corresponding duration rows, which would give measured reference values rather than invented ones — a check worth performing before choosing values.

Project-Ontology `OQ-02` and Project-Comprehension `H-03` concern whether the full-resolution delivery is remosaiced Bayer or raw Quad-Bayer. Faz 3.5 answers this, and the answer informs the stall duration value.

`ishtar-cam-modes/blobs/hal-fullres.patch` demonstrates that the existing 16-point patch does not touch the duration tables at all, so this is new territory within the binary rather than an extension of mapped ground.

## 7. Planned Work Breakdown

- F4.2-01 — Settle the format set and the row set
  - Description: Settle which formats and which entries the duration rows cover. **There is no target-versus-experiment discrepancy left to reconcile** — the amended target end state names no format set and requires the emission to stay broad — so this is a scoping decision taken on its own merits. Three things to settle and record: the emitted set at full resolution is RAW10 (37), RAW12 (38) and RAW_OPAQUE (36); RAW_SENSOR (32) is never emitted and cannot be given a row, which is a fact to state rather than a discrepancy to resolve; and **whether every emitted entry across the broad table gets a pair of rows, or only a justified subset does** — the question the retired narrowing would have answered by shrinking the table. Record the reasoning either way.
  - Output: A settled format set **and a settled row set**, both with reasoning.
- F4.2-02 — Check the vendor tables for reference values
  - Description: Read the vendor stream configuration table's corresponding duration rows, if any, for the same formats at 8192x6144. Measured vendor values are preferable to derived ones.
  - Output: A reference value set, or a statement that none exists.
- F4.2-03 — Locate the two duration emission sites
  - Description: Find where `d000b` and `d000c` tables are populated, and determine their relationship to the stream configuration emission.
  - Output: Two located sites with their population mechanism described.
- F4.2-04 — Select the duration values with justification
  - Description: Choose minimum frame duration and stall duration for each format in the settled set, citing the vendor reference, the recorded 66,666,666-nanosecond measurement, or the remosaic finding from Faz 3.5.
  - Output: A value table with per-value justification.
- F4.2-05 — Assess the bucketing consequence
  - Description: State which framework size list the entries will land in given the chosen minimum frame duration, and confirm this is the intended outcome given how the application-level patch works.
  - Output: A bucketing assessment routed for confirmation if it changes AGC behavior.
- F4.2-06 — Apply the rows and verify
  - Description: Add the rows and confirm the camera service dump reports them alongside the matching stream configuration entries for the same format and size.
  - Output: A dump verification showing all three tables consistent.
- F4.2-07 — Verify existing entries are unaffected
  - Description: Confirm the duration rows for pre-existing entries are unchanged, since a shared emission loop makes collateral change plausible.
  - Output: An unchanged-entries verdict.
- F4.2-08 — Record the located addresses
  - Description: Write the two table sites into Project-Ontology section 6 during the session.
  - Output: An updated address book.

## 8. Acceptance Criteria

- The format set and the row set are settled with recorded reasoning — which emitted entries receive duration rows, and why the rest do not. `RAW_SENSOR` (32) is recorded as never emitted rather than left unreconciled, and **no criterion requires the emitted set to be narrower**; narrowing it is the retired goal `IMPL-49` measured as preventing AGC from launching.
- Every entry in the settled format set has both a minimum frame duration row and a stall duration row.
- Each chosen value has a written justification citing a vendor reference, a prior measurement, or the remosaic finding — none is invented without a stated basis.
- The camera service dump reports the stream configuration, minimum frame duration, and stall duration rows consistently for the same format and size.
- Duration rows for pre-existing entries are unchanged.
- The bucketing consequence is stated, and if the chosen values would move an entry between framework size lists, that is routed for confirmation rather than applied silently.
- The two duration table sites are recorded in Project-Ontology section 6.
- Every measurement carries a smoke bracket and confirms the preference precondition.
- The broad emission is preserved: the stream-configuration entry count is unchanged apart from the duration tables, reported per camera id with the `streamcfg` int32 metric named.
- **AGC still launches and still captures cleanly at 12.58 MP with the rows applied** — the criterion `IMPL-49` showed the retired narrowing goal silently violated. Verified by the `Faz3.8` smoke fields plus one measured capture, not by the app opening.
- The chosen minimum frame durations do not move `8192x6144` into `getOutputSizes`, or if they do, that outcome was confirmed by the user under `DEC-09` with `R12`'s consequence stated in the request.

## 9. Validation and Test Approach

Validation is live and table-consistency driven. The distinguishing check is cross-table consistency rather than a single value.

- `VAL-SMOKE` (from Faz 2.1, extended by Faz 3.8) — the bracket, including the entry count per camera id and the AGC photo-size pin fields.
- `VAL-AGC` (from Faz 3.9 / Faz 3.10) — AGC launch verdict plus one measured capture after the rows are applied, since `IMPL-49` established that a HAL table edit can break AGC's initialisation without changing any count this sub-plan otherwise checks.
- `VAL-TABLES` (proposed) — extraction of all three tables for camera 3 and a consistency check: every stream configuration entry in the settled set has matching rows in both duration tables, with the same format and size.
- `VAL-UNCHANGED` (proposed) — comparison of pre-existing entries' duration rows against the pre-patch state, confirming no collateral change.
- `VAL-DISASM` (from Faz 1.4) — the static analysis locating the two emission sites.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist.

Local versus live: the site location and value selection are local; verification is live. Security validation is not applicable. Ontology validation applies to invariant 7, which this sub-phase interacts with directly, and to recording the two new table addresses.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Bracket and array count preservation check. | VAL-SMOKE |
| agc-50mp-yama/hal-raw50-deneme.patch | modified | Extended with the duration row entries alongside the broad emission. | VAL-TABLES, VAL-UNCHANGED |
| Planner-docs/Project-Ontology.md | modified | Record the two duration table sites and any interaction with invariant 7. | VAL-DISASM |
| docs/patch-table-format.md | existing | Extension rules governing how new entries join the table. | VAL-DISASM |

## 10. Dependencies and Sequencing

**No longer depends on `Faz4.1`, which is `superseded` by `DEC-14` and must not be revived to unblock this sub-plan.** The entry set is the broad one the live HAL already emits; it is stable because nothing is going to narrow it.

Depends on Phase 3 — specifically `Faz3.8` for a bracket that shows AGC's pin and `Faz3.9`/`Faz3.10` for the launch-and-capture verdict method — because `VAL-AGC` is now an acceptance criterion and there is no point in inventing a second way to measure it.

Depends on Faz 3.5 for the `OQ-02` answer, which informs the stall duration justification. If Faz 3.5 did not produce a capture, the stall value must be justified some other way and the weaker basis should be stated rather than hidden.

Depends on Faz 1.3 for the format contract's extension rules and Faz 1.4 for the disassembler.

Blocks Faz 4.3, which consolidates the completed patch, and Faz 4.4, which validates it.

Required decisions: the format set resolution in F4.2-01, and the bucketing consequence in F4.2-05 if it changes AGC behavior. The first is a technical judgment; the second may need the user, since it changes application behavior without touching the application.

Required infrastructure: the device, the module, and the disassembler.

Required human approvals: HAL patching and camera use; user confirmation if the bucketing changes.

Fresh session token and context risk: medium. Two new emission sites to locate in a large binary, though the tag identifiers give a strong starting point.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: duration values are invented to satisfy the table rather than derived from anything. Impact: the configuration becomes internally consistent and externally false, which is worse than incomplete because it is no longer visibly incomplete. Mitigation: F4.2-04 requires a per-value justification and the acceptance criteria enforce it.
- Risk (invariant 7): a chosen minimum frame duration moves the entries into `getOutputSizes`, changing AGC's behavior as a side effect. Impact: an application-level behavior change arrives from a HAL metadata edit, which is exactly the kind of coupling that produces misattributed failures later. Mitigation: F4.2-05 makes the bucketing consequence an explicit assessment and routes it for confirmation.
- Risk: the duration tables share an emission loop with the stream configuration table and the patch changes rows for existing entries. Impact: a regression in sizes that currently work. Mitigation: F4.2-03 establishes the population mechanism before patching, and `VAL-UNCHANGED` checks for collateral change.
- Risk: the row set is never settled and rows are added wherever they are easy to add rather than where an entry justifies one. Impact: duration rows for entries nobody decided to ship, enlarging the patch surface `R8` describes for no stated benefit — and under `DEC-14` the candidate surface is the broad table's ninety rather than the narrowed three, so drifting costs more than it once did. Mitigation: F4.2-01 is the first work item and decides the row set on its own merits. **Carrying RAW12 and RAW_OPAQUE rows is not itself the defect:** the amended target end state names no format set and requires the emission to stay broad, so the old "formats the target does not name" framing no longer identifies anything wrong.
- Risk (`R12`, `DEC-09`): a chosen minimum frame duration moves `8192x6144` into `getOutputSizes`, AGC's default finds it, and Phase 3's result is undone from the HAL side without AGC being touched. Impact: the project's headline behaviour regresses through a metadata edit made for a completeness reason. Mitigation: `F4.2-05` is now a gate rather than a note — the bucketing outcome is stated before the rows are applied, and a threshold-crossing value needs the user's confirmation with `R12` named in the request.
- Risk: `OQ-02` was not answered because Faz 3.5 did not produce a capture, and the stall duration is justified on a weaker basis. Impact: a value chosen on incomplete grounds. Mitigation: the dependency section requires the weaker basis to be stated rather than concealed, so a later capture can revisit it.
- Risk: the duration tables are not patchable within the four-byte alignment constraint. Impact: the rows cannot be expressed in the existing patch format. Mitigation: F4.2-03 assesses the mechanism before design, and the format contract states the constraint.
- Risk (`R8`): two more sets of offsets are added, all bound to one vendor build. Impact: a larger surface invalidated by any system update. Mitigation: unchanged posture — checksum guard as detector, documented method for re-derivation.

## 12. Desired End State

Every stream configuration entry in the settled row set has matching minimum frame duration and stall duration rows, with values that have a stated basis. The camera service dump shows all three tables consistent for the same formats and sizes. Pre-existing entries are unchanged, the broad emission is preserved with its count reported per camera id, **AGC still launches and captures cleanly at 12.58 MP**, and the framework bucketing consequence is stated and — where it crosses the threshold — confirmed under `DEC-09` with `R12` named.

The evidence an implementer should produce is the settled format set with reasoning, the value table with justifications, the three-table consistency extraction, and the unchanged-entries comparison.

The ledger summary Step 4 should append records: the format set decided, the duration values and their bases, the located table addresses, the bucketing outcome, and confirmation that existing entries were unaffected.

## 13. Next Sub-Phase Transition Criteria

- Every entry in the settled format set has both duration rows.
- Every value has a written justification.
- The three tables are confirmed consistent in the camera service dump.
- Pre-existing entries' duration rows are unchanged.
- The bucketing consequence is stated and, if behavior-changing, confirmed.
- AGC still launches and captures cleanly at 12.58 MP with the rows applied, measured rather than inferred from the app opening. *(Added by planning run 10: section 8 has carried this criterion since run 8, but the transition gate did not, so the sub-plan could have been closed without it.)*
- The two table sites are recorded in the ontology.
- Faz 4.3 has a complete patch to consolidate.
