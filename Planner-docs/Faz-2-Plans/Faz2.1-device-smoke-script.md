# Faz 2.1 — Device Smoke Script

## 1. Context

Main-Planing places the smoke script in Phase 9 but then contradicts that placement twice, and both contradictions point the same direction. Prioritized next step 2 says: "Write the device smoke script. *Type: validation action (Phase 9, pulled forward).* … Pays for itself across Phases 2–5." Risk `R5` says the mitigation is "Phase 9's smoke script, pulled forward to the start of Phase 2." Phase 9's own first vibecoding slice says "Write the smoke script first — it pays off immediately in Phases 2 through 5."

Autopsy makes it a prerequisite rather than a preference. Section 12 under Phase 2 states: "Make the smoke script a prerequisite of this phase, not a later deliverable." Section 13 files the underlying gap as `AUTOPSY-P0-02` — "No before/after state capture around device changes" — with the concrete cost recorded: "The sensor-7 Gcam failure was blamed on the HAL patch, then the APK patch, before being traced to leftover shared preferences — a three-step misattribution."

Project-Comprehension frames the trade explicitly in `QAS-02`: "writing the smoke script costs a day that could go to Phase 3 — but Phase 3's own history shows two days lost to misattribution, so the trade favours the script."

This sub-plan therefore places the smoke script at the head of Phase 2, which is the earliest point at which it can exist and the latest point at which it is still cheap.

## 2. Goal

Produce a single read-only command that reports the device's complete camera-modification state — active mode, both blob checksums, mount state, the camera 3 stream configuration rows, and the installed AGC build — so that every later change can be bracketed by a before and after snapshot.

## 3. Description

The problem is that this project's only verification surface is the device, and nothing captures it. Autopsy section 8 states it plainly: "almost nothing can be validated locally … This makes a device-side smoke script disproportionately valuable — it is effectively the *only* automatable validation surface."

It belongs at the head of Phase 2 because Faz 2.2 flashes a release and Faz 2.3 runs a ten-mode regression, and neither produces durable evidence without it. It reduces risk by making misattribution structurally harder: when a failure appears, the question "what changed" has a recorded answer rather than a reconstructed one.

The vibecoding slice strategy: the first useful slice is the cheap half — active mode, the two checksums, and mount state, which is four commands and answers `H-10` immediately. The second slice adds the stream configuration extraction, which is the part that needs parsing and is also the part Phases 3 and 4 depend on. The fastest validation signal is running the script twice around a single deliberate mode change and confirming the diff shows exactly that change and nothing else.

What not to over-plan: output format beyond something diffable, historical storage, trend analysis, or any notion of a test framework. The script's job is to print state. Comparison is done with a diff.

One design property matters more than the rest and should be fixed early: the script must be strictly read-only. It runs before and after changes including failed ones, so it must never itself alter state — no service restarts, no mode writes, no mounts.

## 4. Scope

- Active mode as reported by the module, read from the framework rather than from a cached value.
- The md5 of the live sensor driver at `/odm/lib64/camera/`, compared against the expected value.
- The md5 of the live camera HAL binary, classified as stock, fullres, or unrecognized using the constants `halpatch.sh` already defines.
- Bind mount state for both the sensor path and the HAL path.
- The camera 3 stream configuration rows from the camera service dump, extracted rather than dumped whole.
- The int32 entry count of the stream configuration array, since Faz 4.4 needs it as a measured acceptance number.
- The installed AGC package version and its checksum.
- The presence or absence of the `pref_raw_key` and `pref_fix_resolution_key` preference families, since Project-Ontology invariant 8 makes them a precondition for every Phase 3 measurement.
- Diffable output: stable ordering, one fact per line, no timestamps inside the comparable region.

## 5. Out of Scope

- Any write, mount, unmount, service stop or start, or force-stop. The script is read-only by design.
- Judging whether a state is correct. It reports; a human or a later checklist interprets.
- Image capture, image quality assessment, or anything requiring the shutter.
- Video recording verification, which requires the user's hands and belongs to Faz 2.3's manual gate.
- Host-side blob generation verification, which `tools/verify_ln.py` already covers.
- Continuous or scheduled execution. It runs when invoked, before and after a change.
- Automatic ledger writing. The operator records the output; the script does not.

## 6. Current Repository Evidence

There is no test, smoke, or verification artifact anywhere in the tree. Autopsy section 8 confirms this and Project-Comprehension records it as `EV-02`, confidence `confirmed`, evidenced by the absence of a tests directory, a CI configuration, a Makefile, a package manifest, and a Python project file.

`ishtar-cam-modes/halpatch.sh` was read in this run and already contains most of the primitives the script needs, which means the script is largely a composition rather than an invention. It defines `HAL_TGT=/odm/lib64/hw/camera.qcom.so`, `HAL_STOCK_MD5=c3fa63a86ee3ecaf9fbf02005d35f6b5`, `HAL_FULLRES_MD5=fe0245a4720fb07b01d96deef47f5569`, and `HAL_SIZE=27268688`. Its `hal_mounted` function tests mount state with a grep against the process 1 mount info, and `hal_state` classifies a checksum into `fullres`, `stock`, `unknown`, or `none`. The smoke script should read these constants from the module rather than duplicate them.

`ishtar-cam-modes/setmode.sh` defines the sensor side equivalently: `BIN=com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, `TGT=/odm/lib64/camera/$BIN`, `EXPECT_SIZE=1062250`, and a `mounted()` function using the same mount-info technique. It also documents that invoking it with no argument shows status, which is an existing partial capability the script can build on.

`ishtar-cam-modes/customize.sh` records the expected stock sensor driver md5 as `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` — the value the smoke script should compare the live driver against.

`agc-50mp-yama/hal-raw50-deneme.patch` records the measured array growth as 508 to 868 int32 entries, which establishes both the baseline and the units for the entry-count field.

Both `.agc` configuration files were confirmed in this run to contain `pref_raw_key`, `pref_raw_key_0` through `_4`, `pref_fix_resolution_key`, and `pref_fix_resolution_key_0` through `_4`. This is why the preference check belongs in the smoke output rather than in a Phase 3 checklist.

`platform-tools/` holds a vendored `adb`, which is the only host-to-device channel per Project-Ontology section 6.

## 7. Planned Work Breakdown

- F2.1-01 — Define the output contract before writing the script
  - Description: Fix the field list, the ordering, and the one-fact-per-line format. Decide where the invocation timestamp goes so it does not pollute a diff.
  - Output: A short output specification, agreed before implementation.
- F2.1-02 — Implement the cheap half
  - Description: Active mode, sensor driver checksum against the expected value, HAL checksum classified into the three known states, and both mount states. Source the module's own constants rather than duplicating them.
  - Output: A working script covering five fields; `H-10` and `EV-19` answered on first run.
- F2.1-03 — Implement the stream configuration extraction
  - Description: Extract the camera 3 stream configuration rows from the camera service dump and report the int32 entry count. Extraction rather than a whole dump, because the dump is large and the script must stay diffable.
  - Output: Stream rows plus a numeric entry count.
- F2.1-04 — Implement the application-layer fields
  - Description: Installed AGC package version and checksum, plus a presence check for the two preference key families.
  - Output: Three application-layer fields.
- F2.1-05 — Enforce the read-only property
  - Description: Review every command in the script and confirm none writes, mounts, unmounts, restarts a service, or force-stops a package. Record this review as a property of the script, since it will be run around failed changes where a side effect would be most damaging.
  - Output: A read-only review with a per-command verdict.
- F2.1-06 — Validate with a deliberate single-variable change
  - Description: Run the script, change exactly one thing, run it again, and confirm the diff shows exactly that change. This proves the script is sensitive enough to be useful and stable enough to be diffable.
  - Output: A before and after pair with a clean single-line diff.
- F2.1-07 — Establish the snapshot storage convention
  - Description: Decide where snapshots are kept and how they are named, so a snapshot from Faz 3.3 can be compared against the Faz 2.2 baseline weeks later.
  - Output: A naming and location convention.

## 8. Acceptance Criteria

- One invocation produces all nine field groups listed in the scope section.
- The script performs no write, mount, unmount, service transition, or force-stop, verified by the per-command review in F2.1-05.
- Running the script twice with no change between produces byte-identical output within the comparable region.
- Running it around a single deliberate mode change produces a diff whose changed lines correspond exactly to that change.
- The HAL checksum is classified into stock, fullres, or unrecognized using the module's own constants rather than hard-coded duplicates.
- The stream configuration entry count is reported as a number, so Faz 4.4 can use it as a measured acceptance value.
- The preference key families are reported as present or absent, so Faz 3.1 has its precondition available.
- `H-10` in Project-Comprehension section 8 and `EV-19`'s confidence are updated from the first real run.
- The snapshot naming convention is written down and used for the first snapshot.

## 9. Validation and Test Approach

This sub-phase is unusual in that it builds the validation surface the rest of the roadmap uses. Its own validation is therefore self-referential and must be explicit about it.

- `VAL-SMOKE` (proposed) — the script itself, once it exists. This identifier is referenced by every later device-facing sub-plan.
- `VAL-IDEMPOTENT` (proposed) — two consecutive invocations with no intervening change must produce identical comparable output. This is what makes the diff trustworthy.
- `VAL-SENSITIVITY` (proposed) — one invocation, one deliberate single-variable change, one invocation, one diff. Confirms the script detects what it claims to detect.
- `VAL-READONLY` (proposed) — the per-command review from F2.1-05, recorded as a written verdict rather than an assumption.

Local versus live: the script is entirely live — it requires a connected device. There is no local dimension, which is itself the finding Autopsy section 8 records. Document validation applies to the output contract and the storage convention. Security validation is minimal: the script must not print anything credential-bearing, and package checksums are not sensitive.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | proposed | The read-only device state reporter this sub-phase produces. | VAL-SMOKE, VAL-IDEMPOTENT, VAL-SENSITIVITY, VAL-READONLY |
| ishtar-cam-modes/halpatch.sh | existing | Source of the HAL path, size, and both checksum constants. | VAL-SMOKE |
| ishtar-cam-modes/setmode.sh | existing | Source of the sensor path, expected size, and mount-detection technique. | VAL-SMOKE |
| ishtar-cam-modes/customize.sh | existing | Source of the expected stock sensor driver checksum. | VAL-SMOKE |
| Planner-docs/Project-Comprehension.md | modified | Update `H-10` and the `EV-19` confidence from the first real run. | VAL-SMOKE |

## 10. Dependencies and Sequencing

Depends on Faz 1.1, so the script is versioned from its first line. It does not depend on any other Phase 1 sub-plan, and it may run in parallel with Faz 1.3 through Faz 1.6.

Blocks Faz 2.2, Faz 2.3, and every Phase 3 sub-plan. Autopsy section 12 makes the smoke script a mandatory bracket around every Phase 3 measurement, so this is a hard sequencing constraint rather than a preference.

Required infrastructure: a connected device with root access through KernelSU, and the vendored `adb`. Both already exist.

Required human approvals: the device must be connected and unlocked, which is the user's action. The script itself is read-only, so no approval is needed for what it does.

Required decisions: the output format and the storage convention, both of which the implementer can settle and record.

Fresh session token and context risk: low to medium. The camera service dump is large, so the extraction step must filter on the device rather than pulling the whole dump into context. This is the one place in the sub-phase where an unbounded command would be costly.

Subagents are not recommended. Device state is stateful and easy to corrupt with parallel access, and Main-Planing section 9 advises against subagents for this project generally.

## 11. Risks and Mitigations

- Risk: the script performs a side effect — a service restart to refresh a value, for instance — and is then run around a failed change. Impact: the script alters the state it is meant to observe, and the resulting evidence is wrong in the situation where evidence matters most. Mitigation: F2.1-05 reviews every command, and read-only status is an acceptance criterion rather than an intention.
- Risk: output includes a timestamp or a session-varying identifier inside the comparable region. Impact: every diff is noisy and the operator stops reading them. Mitigation: `VAL-IDEMPOTENT` requires byte-identical output across two unchanged runs, which fails immediately if this happens.
- Risk: the checksum constants are duplicated into the script and drift from `halpatch.sh` when a ROM update changes the HAL. Impact: the script reports `unrecognized` for a correct state or, worse, `stock` for a changed binary. Mitigation: F2.1-02 requires sourcing the module's constants.
- Risk: the stream configuration extraction pulls the whole camera service dump into the session. Impact: context exhaustion in a sub-phase that is supposed to be cheap, and the same problem recurs on every Phase 3 measurement. Mitigation: filtering happens on the device; only the extracted rows and the count return.
- Risk (`AUTOPSY-P0-02` residual): the script exists but is not actually run before and after changes. Impact: the misattribution failure mode returns despite the tooling. Mitigation: `VAL-SMOKE` is referenced as a required gate in every later device-facing sub-plan's contract table, not left as a suggestion.
- Risk: the preference check reports presence without naming which keys are set. Impact: Faz 3.1 cannot tell which of the ten keys to clear. Mitigation: the field reports the specific keys found, not a boolean.
- Risk: the script is written to judge correctness and gets it wrong. Impact: a false pass hides a real regression. Mitigation: the out-of-scope section restricts it to reporting; interpretation belongs to Faz 2.3's checklist.

## 12. Desired End State

A single read-only invocation reports the complete camera-modification state of the device across the sensor, HAL, and application layers, in a stable diffable form, with the preference-trap keys visible. Two runs with no change are identical; two runs around one change differ by exactly that change. The script sources its constants from the module rather than duplicating them, and a written convention says where snapshots live and how they are named.

The evidence an implementer should produce is the idempotence pair, the sensitivity diff, the read-only review verdict, and the first stored snapshot.

The ledger summary Step 4 should append records: the script path, the four validation results, the answer to `H-10` from the first run, and the snapshot naming convention adopted.

## 13. Next Sub-Phase Transition Criteria

- The script reports all nine field groups from one invocation.
- Idempotence and sensitivity have both been demonstrated with real output, not asserted.
- The read-only review is recorded with a per-command verdict.
- The snapshot storage convention exists and the first snapshot is stored under it.
- `H-10` is answered, so the workspace `mode` file's relationship to live device state is a fact rather than an assumption.
- Faz 2.2 has a working bracket available before the release is flashed.
