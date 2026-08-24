# Faz 4.2 — Minimum Frame and Stall Duration Rows

## 1. Context

Main-Planing Phase 4's second half is the duration rows, and it records that the user asked for them specifically: "Then add the `availableMinFrameDurations` and `availableStallDurations` rows the new entries require — the user has explicitly requested this, and it is also what makes the advertised configuration honest rather than merely accepted by the framework."

The target end state repeats it as a technical requirement: "RAW10 (37) and RAW_SENSOR (32) advertised at 8192x6144 only at the QCFA full-resolution dimension … with matching `availableMinFrameDurations` and `availableStallDurations` rows."

Autopsy notes the omission as part of `AUTOPSY-P2-02`: the experimental patch adds RAW formats "with no matching duration rows", and its Step 2 impact requires Phase 4's acceptance criteria to "require the duration rows the user explicitly asked for."

The phrase "honest rather than merely accepted" carries the actual argument. Project-Ontology invariant 7 records the mechanism that makes durations load-bearing on this device: `getOutputSizes` excludes any size whose minimum frame duration exceeds one twentieth of a second, and on camera 3, 8192x6144 measures 66,666,666 nanoseconds against 4096x3072's 33,333,333. Duration values are not decorative metadata on this platform — they are the input to the framework's own bucketing decision, and they were the original root cause of the AGC ceiling.

That gives this sub-phase a subtlety worth naming up front. Adding duration rows for the new entries makes the advertised configuration internally consistent, and the specific values chosen determine which framework list the size lands in. That is a behavior change, not merely a completeness fix.

## 2. Goal

Add matching `availableMinFrameDurations` and `availableStallDurations` rows for every stream configuration entry the narrowed patch introduces, so the advertised configuration is internally consistent, with the chosen duration values measured or justified rather than invented.

## 3. Description

The problem is an advertised capability with incomplete supporting metadata. A stream configuration entry without duration rows tells the framework a size is available without telling it what that size costs, and consumers that compute buffering, pipeline depth, or frame pacing from those tables have nothing to read.

It belongs after the narrowing because duration rows are added per entry, and adding them before narrowing would mean adding eighty-seven rows that are then removed. Sequencing this second is not cosmetic — it is the difference between three rows of work and ninety.

The vibecoding slice strategy: locate the two duration tables in the binary, determine how they are populated relative to the stream configuration table, add rows for one entry, and measure. The fastest validation signal is the camera service dump reporting the duration rows alongside the stream configuration rows for the same format and size.

What should not be over-planned: duration values for hypothetical future entries, or a general mechanism for keeping the three tables synchronized. Three entries need three pairs of rows.

The values themselves need care. Project-Ontology invariant 7 records a measured value for 8192x6144 on camera 3 — 66,666,666 nanoseconds — but that measurement was taken for an existing entry rather than for the newly added RAW formats. Whether the same value applies to RAW10 and RAW_SENSOR at that size is a question this sub-phase must answer rather than assume, because stall duration in particular differs by format: a format requiring remosaic or a reprocessing pass stalls differently from one that does not.

The remosaic question links directly to Faz 3.5's `OQ-02` outcome. If the HAL delivers remosaiced Bayer at full resolution, there is processing behind that frame and the stall duration should reflect it. If it delivers raw Quad-Bayer, the cost profile is different. This is a case where an earlier sub-phase's finding has a direct downstream use.

## 4. Scope

- Location of the `availableMinFrameDurations` and `availableStallDurations` emission sites in the binary, using the tag identifiers already recorded.
- Determination of how those tables are populated relative to the stream configuration table, since a shared loop and separate loops imply different patch strategies.
- Selection of duration values for RAW10 and RAW_SENSOR at 8192x6144, measured where possible and justified where measurement is not available.
- Application of the rows and verification that the camera service dump reports them alongside the matching stream configuration entries.
- Assessment of the framework bucketing consequence: which of the two size lists the entries land in given the chosen minimum frame duration.
- Consumer verification that the added rows did not change behavior for existing entries.
- Recording of the located table addresses into Project-Ontology section 6.

## 5. Out of Scope

- Changing which formats or resolutions are emitted. Faz 4.1 settled that.
- Tuning duration values for performance. The goal is honesty, not optimization.
- Consolidating patch tables, which is Faz 4.3.
- The full consumer survey, which is Faz 4.4.
- Any change to `pixelArraySize`, the active array, or the sensor layer.
- Adding duration rows for entries the vendor tables already carry, which are outside this patch's concern.
- Re-deriving the 30 and 15 frames-per-second measurements already recorded; they are inputs, not work.

## 6. Current Repository Evidence

Project-Ontology section 6 records the three relevant tag identifiers under "Related metadata tags": `android.scaler.availableStreamConfigurations` is `d000a`, `availableMinFrameDurations` is `d000b`, and `availableStallDurations` is `d000c`. Their adjacency in the tag space suggests they may be emitted near each other, which is a starting hypothesis for the search rather than a fact.

Invariant 7 records the measured durations that establish the platform behavior: on camera 3, 8192x6144 has a minimum frame duration of 66,666,666 nanoseconds and is therefore excluded from `getOutputSizes`, while 4096x3072 at 33,333,333 nanoseconds is kept. The same invariant records the consequence: this exclusion "was the original root cause of AGC's 12.6 MP ceiling, and it is why Open Camera — which reads both lists — reached 50.3 MP unaided."

That last point has a direct bearing on value selection. If a duration below the one-twentieth-second threshold were chosen for the new entries, they would appear in `getOutputSizes` rather than only in `getHighResolutionOutputSizes` — which would change AGC's behavior without touching AGC. Whether that is desirable is a question this sub-phase should raise rather than decide unilaterally, since it interacts with the application-level patch described in `agc-50mp-yama/README.md`.

`agc-50mp-yama/hal-raw50-deneme.patch` records the three entries needing rows: `[37 8192 6144 OUTPUT]`, `[38 8192 6144 OUTPUT]`, and `[36 8192 6144 OUTPUT]` — RAW10, RAW12, and RAW_OPAQUE. Main-Planing's target end state names only RAW10 (37) and RAW_SENSOR (32) as wanted, which is a discrepancy this sub-phase must resolve: the experiment admits a range that includes formats the target does not name.

Project-Ontology section 6 records that `xiaomi.scaler.availableStreamConfigurations` already carries `[37 8192 6144 0]`, `[32 8192 6144 0]`, and `[36 8192 6144 0]`. That vendor table may also carry corresponding duration rows, which would give measured reference values rather than invented ones — a check worth performing before choosing values.

Project-Ontology `OQ-02` and Project-Comprehension `H-03` concern whether the full-resolution delivery is remosaiced Bayer or raw Quad-Bayer. Faz 3.5 answers this, and the answer informs the stall duration value.

`ishtar-cam-modes/blobs/hal-fullres.patch` demonstrates that the existing 16-point patch does not touch the duration tables at all, so this is new territory within the binary rather than an extension of mapped ground.

## 7. Planned Work Breakdown

- F4.2-01 — Resolve the format set discrepancy
  - Description: Reconcile the experiment's admitted range, which includes RAW12 and RAW_OPAQUE, against the target end state, which names RAW10 and RAW_SENSOR. Determine which formats the shipped patch should carry and record the reasoning.
  - Output: A settled format set for the duration rows.
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

- The format set discrepancy between the experiment's range and the target's named formats is resolved with recorded reasoning.
- Every entry in the settled format set has both a minimum frame duration row and a stall duration row.
- Each chosen value has a written justification citing a vendor reference, a prior measurement, or the remosaic finding — none is invented without a stated basis.
- The camera service dump reports the stream configuration, minimum frame duration, and stall duration rows consistently for the same format and size.
- Duration rows for pre-existing entries are unchanged.
- The bucketing consequence is stated, and if the chosen values would move an entry between framework size lists, that is routed for confirmation rather than applied silently.
- The two duration table sites are recorded in Project-Ontology section 6.
- Every measurement carries a smoke bracket and confirms the preference precondition.
- The Faz 4.1 narrowing result is preserved: the array entry count is unchanged apart from the duration tables.

## 9. Validation and Test Approach

Validation is live and table-consistency driven. The distinguishing check is cross-table consistency rather than a single value.

- `VAL-SMOKE` (from Faz 2.1) — the bracket, including the array entry count to confirm Faz 4.1's result is preserved.
- `VAL-TABLES` (proposed) — extraction of all three tables for camera 3 and a consistency check: every stream configuration entry in the settled set has matching rows in both duration tables, with the same format and size.
- `VAL-UNCHANGED` (proposed) — comparison of pre-existing entries' duration rows against the pre-patch state, confirming no collateral change.
- `VAL-DISASM` (from Faz 1.4) — the static analysis locating the two emission sites.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist.

Local versus live: the site location and value selection are local; verification is live. Security validation is not applicable. Ontology validation applies to invariant 7, which this sub-phase interacts with directly, and to recording the two new table addresses.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Bracket and array count preservation check. | VAL-SMOKE |
| agc-50mp-yama/hal-raw50-deneme.patch | modified | Extended with the duration row entries alongside the narrowed emission. | VAL-TABLES, VAL-UNCHANGED |
| Planner-docs/Project-Ontology.md | modified | Record the two duration table sites and any interaction with invariant 7. | VAL-DISASM |
| docs/patch-table-format.md | existing | Extension rules governing how new entries join the table. | VAL-DISASM |

## 10. Dependencies and Sequencing

Depends on Faz 4.1 for a stable, narrowed entry set. Adding rows before narrowing would mean adding ninety of them.

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
- Risk: the format set discrepancy is left unresolved and the patch carries RAW12 and RAW_OPAQUE rows the target end state does not want. Impact: the narrowing achieved in Faz 4.1 is partly undone by carrying unwanted formats forward. Mitigation: F4.2-01 is the first work item.
- Risk: `OQ-02` was not answered because Faz 3.5 did not produce a capture, and the stall duration is justified on a weaker basis. Impact: a value chosen on incomplete grounds. Mitigation: the dependency section requires the weaker basis to be stated rather than concealed, so a later capture can revisit it.
- Risk: the duration tables are not patchable within the four-byte alignment constraint. Impact: the rows cannot be expressed in the existing patch format. Mitigation: F4.2-03 assesses the mechanism before design, and the format contract states the constraint.
- Risk (`R8`): two more sets of offsets are added, all bound to one vendor build. Impact: a larger surface invalidated by any system update. Mitigation: unchanged posture — checksum guard as detector, documented method for re-derivation.

## 12. Desired End State

Every stream configuration entry the patch introduces has matching minimum frame duration and stall duration rows, with values that have a stated basis. The camera service dump shows all three tables consistent for the same formats and sizes. Pre-existing entries are unchanged, the narrowing from Faz 4.1 is preserved, and the framework bucketing consequence is stated and confirmed.

The evidence an implementer should produce is the settled format set with reasoning, the value table with justifications, the three-table consistency extraction, and the unchanged-entries comparison.

The ledger summary Step 4 should append records: the format set decided, the duration values and their bases, the located table addresses, the bucketing outcome, and confirmation that existing entries were unaffected.

## 13. Next Sub-Phase Transition Criteria

- Every entry in the settled format set has both duration rows.
- Every value has a written justification.
- The three tables are confirmed consistent in the camera service dump.
- Pre-existing entries' duration rows are unchanged.
- The bucketing consequence is stated and, if behavior-changing, confirmed.
- The two table sites are recorded in the ontology.
- Faz 4.3 has a complete patch to consolidate.
