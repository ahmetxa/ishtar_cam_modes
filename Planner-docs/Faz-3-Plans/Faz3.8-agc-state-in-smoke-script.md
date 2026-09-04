# Faz 3.8 — AGC Photo-Size Visibility in the Smoke Script

## 1. Context

`Main-Planing.md`'s Phase 3 risk note states the mitigation this sub-plan implements, in one sentence: "the smoke script should report AGC's selected size alongside the HAL md5, so the state is visible without opening the app." Risk `R12`, raised by `DEC-14` as the replacement for the closed `R4`, states the failure it prevents: "AGC's default behaviour is to select the largest advertised size, which under the broad HAL table is the 8192x6144 path that yields an unusable frame. *Impact:* the user discovers the regression through a bad photograph rather than a check."

That impact is not hypothetical for this project. Risk `R5` describes the same feedback-loop failure generally — "regressions surface only when the user notices them, sometimes days later" — and Autopsy `AUTOPSY-P0-02` records a three-step misattribution caused by state not being captured before and after a change. The whole reason `scripts/smoke.sh` exists is that this project's validation surface is a device and a human eye, and the script is the one instrument that turns device state into a diffable text file.

`scripts/smoke.sh` was built by `Faz2.1` (`IMPL-04`) and has bracketed every device change since. Its application layer probe already reads `/data/data/<pkg>/shared_prefs/*.xml`, but it greps only the two trap key families (`pref_raw_key*`, `pref_fix_resolution_key*`) and reports `prefs.trap.count` and `prefs.trap.keys`. **The photo-size preference is not reported at all.** So the single state that decides whether AGC's next photograph is usable is currently invisible to the project's only instrument.

This sub-plan runs **after** `Faz3.7` deliberately. The field should be built against a preference layout that has been read on the device, not one inferred from a ledger sentence.

## 2. Goal

Make AGC's effective photo-size selection visible in every `scripts/smoke.sh` snapshot, inside the comparable region, so that a regression to the 50 MP path shows up as a one-line diff in a bracket rather than as a bad photograph days later — while preserving the script's read-only and byte-identical-on-no-change guarantees exactly.

## 3. Description

The problem is an unobservable state with a bad default. `R12`'s mitigation has three parts and this sub-plan owns the middle one: pin the size (`Faz3.7`), **report it** (here), re-verify after any AGC update or `.agc` import (`Faz3.10`, `Faz3.11`).

It belongs second in the phase because everything after it is a repeated measurement. `Faz3.9`'s coexistence bracket and `Faz3.10`'s four-axis stickiness matrix each take several snapshots, and a snapshot that cannot show the pin makes those runs depend on a separate ad-hoc read that nobody diffs. Building the instrument before the repeated measurements is the same reasoning that pulled the smoke script forward into Phase 2 in the first place.

**The vibecoding slice strategy.** The first useful slice is one added line in `probe_app` reporting `pref_camera_picturesize_back_key`'s raw value. That alone closes most of `R12`. The second slice adds `pref_48m_key` and a derived megapixel figure, so a reader who does not remember that `4096x3072` is 12.58 MP still sees the consequence. The fastest validation signal is the existing idempotence check: run the script twice with nothing changed and diff the comparable regions — they must be byte-identical, which is `VAL-IDEMPOTENT` from `IMPL-04`.

**What must not be over-planned.** The script must not start judging. Its own header states the contract: "It does NOT judge whether a state is correct. It reports; a human or a later checklist interprets." A field named `agc.photo_size` is a report. A field named `agc.photo_size.ok` would be a verdict, and it would be wrong the moment the target size changes. The derived megapixel figure is arithmetic on the reported value, not an assessment of it.

**Two constraints from the script's own design govern this change and are not negotiable.** First, read-only: `IMPL-04`'s `VAL-READONLY` was a per-command review establishing that every device-side command is one of `cat`, `ls`, `md5sum`, `stat`, `basename`, `grep`, `sed`, `cut`, `sort`, `tr`, `wc`, `echo`, `printf`, `dumpsys`, `pm list/path`. A new field must stay inside that set. Second, determinism: the region between `--- BEGIN COMPARABLE ---` and `--- END COMPARABLE ---` must be byte-identical across two runs with no intervening change, so the new field must have a stable representation when the preference is absent as well as when it is present.

## 4. Scope

- A new field in `probe_app` reporting the value of `pref_camera_picturesize_back_key` for the AGC package.
- A new field reporting `pref_48m_key`, since it decides whether the 50 MP entry is even offered and is therefore half of `R12`'s exposure.
- A derived megapixel field computed from the reported size, so the consequence is legible without arithmetic by the reader.
- A stable, explicit representation for the absent case — a preference that has never been written must produce a fixed token, not an empty value that varies with quoting.
- Preservation of the read-only command set and of the byte-identical comparable region.
- Placement of the new fields inside the comparable region and in a position that keeps existing diffs readable.
- A demonstration that the field actually changes when the state changes — a sensitivity check, matching the `VAL-SENSITIVITY` discipline `IMPL-04` used for the mode fields.
- A note in the script's comment block explaining why these fields exist, in the style of the existing invariant-8 comment above the trap-key grep.

## 5. Out of Scope

- Any verdict, threshold, or pass/fail judgment inside the script. It reports; the checklist interprets.
- Any write to the device, including setting the preference. `Faz3.7` sets it; this script only ever reads.
- Reporting other AGC preferences wholesale. A dump of `shared_prefs` would be large, unstable across app versions, and would put unrelated values into a diffable region — the opposite of what the instrument is for.
- Reporting preference **values** for the trap keys. The existing behaviour reports key names only and that is deliberate; this sub-plan does not change it.
- Restructuring `probe_app`, `probe_cameras`, or the snapshot format. New fields, not a redesign.
- Any change to Open Camera's state or to the sensor and HAL layer probes.
- Automating the check — running the script on a schedule, wiring it to CI, or alerting. The index records that no CI exists and none is planned.

## 6. Current Repository Evidence

`scripts/smoke.sh` is 210 lines. Its header states the read-only contract, the two-region output format, and the byte-identical requirement, all quoted above. `probe_app` occupies lines 98–114 and its last two emitted fields are `prefs.trap.count` and `prefs.trap.keys`, produced by a single `grep -hoE "pref_raw_key[a-z0-9_]*|pref_fix_resolution_key[a-z0-9_]*"` over `/data/data/$AGC/shared_prefs/*.xml`. The file set this sub-plan needs to read is therefore **already** being read; only the pattern and the emitted fields change.

The comment immediately above that grep is the house style for justifying a field: "Project-Ontology invariant 8: these keys break Gcam initialization independently and already caused one misattributed failure. Report the specific keys found, not a boolean, so Faz 3.1 knows which to clear." The new fields get a comparable comment citing `R12` and `DEC-14`.

The output field format is a fixed-width `name = value` produced by `echo "agc.versionCode                 = …"`, aligned to a common column. New fields follow it.

`IMPL-04` records the three validations this change must not break: `VAL-IDEMPOTENT` (byte-identical comparable region across two runs, 150 lines at the time), `VAL-SENSITIVITY` (a `dcgB` → `dcgA` transition produced a diff of exactly 3 lines), and `VAL-READONLY` (per-command review, no mutating command). The line count has grown since; the property, not the number, is what is preserved.

`IMPL-43` establishes that `pref_camera_picturesize_back_key` is the value worth reporting, and that `pref_48m_key` is necessary but not the selector. `IMPL-40` establishes that `4096x3072` corresponds to a clean 12.58 MP result and `8192x6144` to the folded 50.33 MP one, which is what makes the derived megapixel field meaningful rather than decorative.

`Faz3.7`'s `F3.7-01` and `F3.7-03` will have read the actual preference file layout on device — including whether the value is stored as a `<string>` element and exactly how the size is spelled — before this sub-plan is written. That reading is this sub-plan's input and is the reason for the ordering.

## 7. Planned Work Breakdown

- F3.8-01 — Confirm the storage layout from `Faz3.7`'s reading
  - Description: Take the observed preference file, element type, and value spelling from `Faz3.7` rather than re-deriving them. Confirm which file under `shared_prefs/` carries the key, since the existing grep spans all of them with `-h`.
  - Output: The exact key, file, and value format the new field must parse.
- F3.8-02 — Add the photo-size field
  - Description: Emit `agc.photo_size` with the raw preference value, using only commands from the reviewed read-only set. Choose and document the absent-value token.
  - Output: One new reported field with a defined absent case.
- F3.8-03 — Add the 50 MP availability field
  - Description: Emit `agc.pref_48m` with its raw value, since it governs whether the 50 MP entry appears in AGC's list at all and is therefore the other half of `R12`'s exposure surface.
  - Output: One new reported field.
- F3.8-04 — Add the derived megapixel field
  - Description: Compute megapixels from the reported size on the host side, so a reader sees the consequence without arithmetic. Emit a fixed token when the size is absent or unparseable rather than emitting an empty or error value.
  - Output: One derived field whose absent and unparseable cases are both stable.
- F3.8-05 — Write the justification comment
  - Description: Add a comment above the new fields citing `R12` and `DEC-14`, explaining that the default is the largest advertised size and that this is the field which makes a silent revert visible.
  - Output: A comment in the style of the existing invariant-8 note.
- F3.8-06 — Re-run the idempotence check
  - Description: Two consecutive runs with no intervening change; diff the comparable regions; they must be byte-identical including the new fields.
  - Output: An idempotence result stated as a line count and a diff verdict.
- F3.8-07 — Run the sensitivity check
  - Description: Change the pin from `4096x3072` to another advertised size and back, taking a snapshot at each point. The diff must show exactly the new fields changing and nothing else.
  - Output: A sensitivity result stated as a diff line count with the changed lines named.
- F3.8-08 — Re-affirm the read-only property for the added commands
  - Description: Review each device-side command the new fields introduce against `IMPL-04`'s permitted set, and record the review rather than asserting the property.
  - Output: A per-command review covering only the additions.

## 8. Acceptance Criteria

- A `scripts/smoke.sh` snapshot reports AGC's photo-size preference, `pref_48m_key`, and a derived megapixel figure, all inside the comparable region.
- Two consecutive runs with no intervening change produce byte-identical comparable regions, including the new fields.
- Changing the pin and changing it back produces a diff containing **only** the new fields, with the count of changed lines stated as a number.
- With the preference absent, the fields emit a fixed documented token and the idempotence check still passes.
- Every device-side command the change introduces is one of the commands `IMPL-04`'s read-only review permits, and the review of the additions is recorded rather than asserted.
- The script emits no verdict: no field says whether the state is correct.
- The new fields carry a comment citing `R12` and `DEC-14`.
- A snapshot taken with AGC pinned at `4096x3072` and one taken with it at `8192x6144` are distinguishable by reading the file alone, without opening the app and without a capture.
- The existing fields — layer state, mount counts, camera rows, trap keys — are unchanged in name, order, and format.

## 9. Validation and Test Approach

Validation reuses `Faz2.1`'s own validation design, because the property being preserved is the one that sub-plan established. The distinguishing check is that a change to the instrument must not change what the instrument says about everything else.

- `VAL-IDEMPOTENT` (from Faz 2.1) — two consecutive runs, comparable regions diffed, byte-identical required.
- `VAL-SENSITIVITY` (from Faz 2.1) — pin changed and restored; the diff must be exactly the new fields.
- `VAL-READONLY` (from Faz 2.1) — per-command review of the added commands only, recorded.
- `VAL-ABSENT` (proposed) — the same two checks with the preference deliberately absent, to prove the absent-case token is stable rather than an empty string that varies.
- `VAL-SMOKE` (from Faz 2.1) — the script itself, used as the bracket for the sensitivity run.
- `VAL-PRECOND` (from Faz 3.1) — the per-measurement checklist for the live half.

Local versus live: the field design and the derived-megapixel arithmetic are host-side; the idempotence, sensitivity, absent-case and read-only checks all need the device. Security validation: the change reads a preference file it already reads and emits no credential; the trap keys continue to be reported by name only. Ontology and invariant validation: none of the eleven invariants is touched, and that is worth confirming explicitly rather than assuming, since the script is the thing that observes several of them.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | modified | Gains the AGC photo-size, 50 MP availability, and derived megapixel fields in `probe_app`. | VAL-IDEMPOTENT, VAL-SENSITIVITY, VAL-READONLY, VAL-ABSENT |
| snapshots/ | generated | The idempotence pair, the sensitivity pair, and the absent-case pair. | VAL-SMOKE |
| docs/phase3-preconditions.md | existing | The per-measurement checklist for the live half. Read, not edited. | VAL-PRECOND |
| Planner-docs/Planing-Ledger.md | modified | The field list, the three check results, and the recorded command review. | VAL-PRECOND |

## 10. Dependencies and Sequencing

Depends on `Faz3.7` for the observed preference layout, the key spelling, and the value format — this is the ordering's whole purpose. Depends on `Faz2.1` for the script and for the three validation designs it reuses.

Does **not** depend on `DEC-15`. The field reports whatever base is live; which base the phase adopts changes the values, not the instrument.

Blocks `Faz3.9` and `Faz3.10` in practice rather than absolutely. Both could be run with ad-hoc preference reads, but both take several snapshots each and would then produce brackets that do not contain the state under test — which is precisely the defect `AUTOPSY-P0-02` records.

Required decisions: the absent-value token and the field names, both of which are the implementer's to choose and to document. No user decision is required.

Required credentials or live endpoints: none. Root through KernelSU and `adb` for the live checks.

Required human approvals: device access for the sensitivity run, which changes a preference and changes it back.

Fresh-session token and context risk: **low**. One function in a 210-line shell script, plus three bounded device checks.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the new field is non-deterministic — an unquoted empty value, a trailing space, or a locale-dependent number — and the comparable region stops being byte-identical. Impact: every future bracket in the project shows spurious diffs, which degrades the instrument that Phases 2 through 5 all depend on. Mitigation: `VAL-IDEMPOTENT` and `VAL-ABSENT` both run before the change is accepted, and the absent case gets an explicit token.
- Risk: a device-side command outside the reviewed set is introduced, and the script is no longer provably read-only. Impact: the script's central guarantee — that it can bracket a failed change without altering it — is lost, silently. Mitigation: `F3.8-08` reviews each added command individually and records the review.
- Risk: the field becomes a verdict. Impact: the script starts asserting correctness against a target that will change, and a future reader trusts a stale judgment. Mitigation: the acceptance criteria forbid a verdict field explicitly; the derived megapixel value is arithmetic on the reported value only.
- Risk: the preference lives in a different `shared_prefs` file than expected, or under a different key on a different AGC build, and the field silently reports absent forever. Impact: the `R12` detector reads clean while the state is bad — worse than having no detector, because it is trusted. Mitigation: `VAL-SENSITIVITY` requires the field to be observed **changing** with the state; a field that never changes has not been validated.
- Risk: the sensitivity run leaves the device pinned at the wrong size. Impact: the next measurement in the project starts contaminated. Mitigation: the run restores the pin and the post-bracket is diffed against the pre-bracket, per checklist item 5.
- Risk: reporting `pref_48m_key` is read as a recommendation to turn it on. Impact: someone arms the 50 MP entry and reintroduces the failure mode. Mitigation: the justification comment states that it is reported because it governs exposure, and that the objective's state is off.
- Risk (`R8`): a future AGC update renames the key and the field goes quietly absent. Impact: the detector degrades without notice. Mitigation: the absent token is explicit and visible in the diff, so an absent value is a change rather than a silence; `Faz3.11` records re-verification after any AGC update as an operator instruction.

## 12. Desired End State

`scripts/smoke.sh` reports AGC's effective photo-size selection, the 50 MP availability flag, and the derived megapixel figure in every snapshot, inside the comparable region, with a documented absent case. The script remains read-only by per-command review, remains byte-identical across two unchanged runs, and remains a reporter rather than a judge. A snapshot alone now answers the question "will AGC's next photograph be usable?" without opening the app.

The evidence an implementer should produce: the idempotence diff, the sensitivity diff with its changed lines named and counted, the absent-case pair, and the per-command review of the additions.

The ledger summary Step 4 should append records: the exact field names added, the absent-value token, the idempotence verdict with the comparable-region line count, the sensitivity diff line count, and the read-only review of each added command.

## 13. Next Sub-Phase Transition Criteria

- The three new fields appear in the comparable region of a real snapshot.
- Idempotence holds byte-identically with the new fields present.
- Sensitivity is demonstrated: the fields were observed changing with the state, and only those fields changed.
- The absent case emits a stable documented token.
- The read-only review of the added commands is recorded, not asserted.
- The device is left pinned where `Faz3.7` left it, confirmed by a post-bracket.
- `Faz3.9` and `Faz3.10` can bracket every run with a snapshot that contains the state under test.
