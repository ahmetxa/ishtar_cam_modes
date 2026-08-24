# Faz 2.2 — Flash v2.1 and Capture the Baseline Snapshot

## 1. Context

Main-Planing Phase 2 exists to close one specific gap: "`ishtar-cam-modes-v2.1.zip` was built on 2026-08-22 and has never been flashed." Its first vibecoding slice is "Flash, then capture a single `dumpsys` + `md5` state snapshot as the baseline all later work is diffed against."

Autopsy section 10 states the consequence directly: "The artifact a user would install has therefore never run. This is the clearest local-vs-live readiness gap in the project and it is cheap to close." It is filed as `AUTOPSY-P1-02`. Project-Comprehension records it as `EV-14`, confidence `probable` — probable rather than confirmed because the evidence is a zip dated 2026-08-22 with no flash recorded in the journal, which is an absence of evidence rather than direct evidence.

There is a second reason this sub-phase matters beyond closing that gap. Every later measurement in Phases 3, 4, and 5 is a comparison, and comparisons need an origin. This is where the origin is established: a known-good device state, recorded with the Faz 2.1 script, from a build that is byte-identical to what a user would install.

## 2. Goal

Bring the device to a known state produced by the actual released artifact, and capture a durable baseline snapshot against which every subsequent change in the roadmap is diffed.

## 3. Description

The problem is a fork between two things that are assumed to be the same: the validated state, which came from an incrementally modified working tree, and the shipped state, which came from a zip nobody has installed. Any regression discovered later will be ambiguous until this fork is closed, because "it worked before" refers to a state that was never the released one.

It belongs immediately after the smoke script because the snapshot is the smoke script's first real product, and immediately before the regression pass because Faz 2.3 needs a starting state it can trust.

The vibecoding slice strategy: capture the pre-flash snapshot first, flash, reboot, capture the post-flash snapshot, and diff. That sequence is itself the validation — if the diff shows something unexpected, that is a finding about the release rather than a failure of the procedure. The fastest validation signal is the two-snapshot diff, available within minutes of the reboot.

What should not be over-planned: the regression matrix. Faz 2.3 owns mode-by-mode verification. This sub-phase verifies exactly one thing — that the release installs and the device reaches a coherent state — and stops there.

Two preconditions come from elsewhere and are non-negotiable. Faz 2.1 must have produced a working script, because flashing without a bracket reproduces `AUTOPSY-P0-02` in the very sub-phase meant to establish evidence discipline. Faz 1.5 must have answered whether `customize.sh` normalizes install state, because evidence gathered in this Step 2 run suggests it does not, which means the archive's packaged `mode` file determines the post-install mode. Flashing without knowing that value means not knowing what state the device will be in afterward.

## 4. Scope

- A pre-flash snapshot captured with the Faz 2.1 script and stored under the convention that sub-phase established.
- Verification of the archive before installation: its checksum, and confirmation of what its packaged `mode` file contains.
- The flash itself through KernelSU, which is the user's physical action.
- A reboot and a post-flash snapshot.
- A diff of the two snapshots, with every changed line accounted for.
- Confirmation that the module reports itself as v2.1 with versionCode 12 after installation.
- Confirmation that the four QuickSettings tiles are present and that the launcher entry renders, since the launcher icon fix is v2.1's headline change.
- Resolution of `EV-14`'s confidence from `probable` to a measured fact.
- The baseline snapshot marked as such, so later sub-phases reference it unambiguously.

## 5. Out of Scope

- The ten-mode regression pass, video verification, and reboot persistence across modes. All belong to Faz 2.3.
- The `tiles hide` decision, which is Faz 2.4.
- Any HAL or sensor modification beyond what installing the release performs.
- Building a new release. This sub-phase installs the existing artifact; if the artifact is found defective, that is a finding routed to Phase 9, not a rebuild here.
- Any Phase 3 measurement or preference-trap clearing.
- Recovery procedure authoring, which `QAS-01` identifies as a gap and which Faz 9.2 owns.

## 6. Current Repository Evidence

`ishtar-cam-modes-v2.1.zip` exists at the workspace root alongside `ishtar-cam-modes-v1.0.zip`, `ishtar-cam-modes-v1.9.zip`, and `ishtar-cam-modes-v2.0.zip`.

`ishtar-cam-modes/module.prop` was read in this run and reports `version=v2.1`, `versionCode=12`, `id=ishtar_cam_modes`. Its `description` field carries the full changelog from v1.2 through v2.1, and the v2.1 entry describes the two changes to verify after installation: the launcher icon now renders correctly rather than using the tile tint on a white background, and launcher visibility is reapplied on every call with status read from the framework rather than from a cache.

`ishtar-cam-modes/customize.sh` was read in full in this run. It aborts if the device is not `ishtar`, aborts if the live sensor driver md5 differs from `9e4d0fe1a8bf2eb4146c9917a0ac2c4c`, and warns without aborting if the live HAL md5 matches neither `c3fa63a86ee3ecaf9fbf02005d35f6b5` (stock) nor `fe0245a4720fb07b01d96deef47f5569` (fullres). It prints "Ilk kurulumdan sonra bir kez yeniden baslat" — the reboot after first install is expected by the installer itself. No statement in the file writes the `mode` file.

`ishtar-cam-modes/mode` in the working tree contains `stock`. If the archive carries the same file, the post-install mode is `stock`, which is the benign case. This must be confirmed against the archive rather than the working tree, since the two were built at different times.

`ishtar-cam-modes/post-fs-data.sh` maps any unrecognized mode value to `stock` across all three variables, so even an unexpected packaged value fails safe at boot.

Project-Comprehension records `EV-19` — that the device's live mode matches the workspace `mode` file — as `tentative`, noting the device was not queried. The Faz 2.1 pre-flash snapshot resolves that before this sub-phase changes anything.

## 7. Planned Work Breakdown

- F2.2-01 — Verify the archive before installing it
  - Description: Record the archive's checksum and inspect its packaged `mode` file and its `module.prop` version fields by entry name and content, so the post-install state is predicted before it is produced.
  - Output: An archive verification record including the predicted post-install mode.
- F2.2-02 — Capture and store the pre-flash snapshot
  - Description: Run the Faz 2.1 script against the current device state and store the output under the established naming convention. This snapshot also resolves `EV-19`.
  - Output: A stored pre-flash snapshot; `EV-19` confidence updated.
- F2.2-03 — Flash the release
  - Description: Install `ishtar-cam-modes-v2.1.zip` through KernelSU. This is the user's physical action. Record the installer's output, including which of the three HAL classification branches `customize.sh` reports.
  - Output: Installer transcript with the HAL branch recorded.
- F2.2-04 — Reboot and capture the post-flash snapshot
  - Description: Reboot as the installer instructs, then run the script again and store the result.
  - Output: A stored post-flash snapshot.
- F2.2-05 — Diff and account for every change
  - Description: Compare the two snapshots. Every changed line must have an explanation; an unexplained change is a finding, not noise.
  - Output: An annotated diff with a per-line account.
- F2.2-06 — Verify the v2.1 surface changes
  - Description: Confirm the module reports v2.1 and versionCode 12, that four tiles are present, and that the launcher entry renders rather than appearing blank. The launcher check needs the user's eyes.
  - Output: A verification record for the three v2.1 claims.
- F2.2-07 — Mark the baseline
  - Description: Designate the post-flash snapshot as the roadmap baseline and record its identifier where later sub-plans can reference it.
  - Output: A named baseline reference.
- F2.2-08 — Resolve the never-flashed question
  - Description: Update `EV-14` in Project-Comprehension from `probable` to a measured state, and record the flash date.
  - Output: An updated evidence row.

## 8. Acceptance Criteria

- The archive's checksum and its packaged `mode` file content are recorded before installation.
- A pre-flash snapshot exists, is stored under the Faz 2.1 convention, and resolves `EV-19`.
- The installer completed without aborting, and the HAL classification branch it reported is recorded.
- A post-flash snapshot exists and is stored under the same convention.
- Every line in the two-snapshot diff has a written explanation; no change is dismissed as noise.
- The module reports version v2.1 and versionCode 12 after installation.
- All four QuickSettings tiles are present, and the launcher entry renders visibly rather than blank.
- The post-flash snapshot is named as the roadmap baseline and is referenceable by identifier.
- `EV-14` no longer reads `probable`, and the flash date is recorded.
- The device is in a working state at the end: the camera opens and preview is not black.

## 9. Validation and Test Approach

This sub-phase is entirely live. There is no local dimension, and that asymmetry is the point — it is where the project's local-versus-live gap gets closed for the sensor-mode layer.

- `VAL-SMOKE` (from Faz 2.1) — the bracket. Run before and after, stored both times.
- `VAL-DIFF` (proposed) — the two-snapshot comparison with a per-line account. This is the primary evidence artifact of the sub-phase.
- `VAL-INSTALL` (proposed) — the installer transcript, checked for the expected abort guards not firing and for which HAL branch was taken.
- `VAL-MANUAL` (proposed) — the user-performed checks: four tiles present, launcher entry renders, camera opens with a live preview. These require human eyes and are recorded as a checklist with the user as the actor, per Autopsy's Gate 3.
- `VAL-DOCS` (proposed) — read back the updated `EV-14` and `EV-19` rows.

Security validation is not a focus here, though the installer's abort-on-checksum-mismatch behavior is itself the fail-closed discipline working, and F2.2-03 records which branch fired. Artifact validation is limited to the archive's own checksum; full packaging assertions are Faz 9.1.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | The bracket used before and after the flash. | VAL-SMOKE, VAL-DIFF |
| ishtar-cam-modes-v2.1.zip | external | The release artifact under test; verified by checksum, not modified. | VAL-INSTALL |
| ishtar-cam-modes/module.prop | existing | Source of the version and versionCode values to confirm post-install. | VAL-INSTALL, VAL-MANUAL |
| ishtar-cam-modes/customize.sh | existing | Read-only context for the three abort and warn branches the transcript should show. | VAL-INSTALL |
| Planner-docs/Project-Comprehension.md | modified | Update `EV-14` and `EV-19` from the measured result. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 2.1 absolutely. Flashing without the bracket is the failure mode `AUTOPSY-P0-02` describes, and doing it in the phase meant to establish evidence discipline would be self-defeating.

Depends on Faz 1.5's install-state answer. If `customize.sh` does not normalize the packaged `mode` file, the post-install mode is whatever the archive carries, and F2.2-01 must therefore read it before the flash rather than discover it after.

Depends on Faz 1.1 only in that findings and snapshots should land in a versioned tree.

Blocks Faz 2.3 and Faz 2.4, and blocks every Phase 3 sub-plan, since Phase 3's measurements are diffed against this baseline.

Required human approvals and physical actions: the flash itself, the reboot, and the visual checks. Project-Ontology section 5 and Autopsy section 9 both record the established split — read-only inspection is delegated, anything touching the phone is the user's action — and this sub-phase sits squarely on the user's side of it.

Required infrastructure: the device, KernelSU, and the vendored `adb`.

Fresh session token and context risk: low. Two snapshots and a diff. The one cost risk is a full camera service dump, which Faz 2.1's extraction design already avoids.

Subagents are not recommended. This is a single stateful device interaction sequence.

## 11. Risks and Mitigations

- Risk: `customize.sh` aborts because the live sensor driver checksum does not match `9e4d0fe1a8bf2eb4146c9917a0ac2c4c`. Impact: the flash fails and the cause may be an unnoticed system update. Mitigation: the pre-flash snapshot reports the live checksum, so this is known before the flash rather than discovered by an abort.
- Risk: the archive's packaged `mode` file carries a non-stock value and the device comes up in an unexpected mode. Impact: the baseline is not the state the operator believes it is. Mitigation: F2.2-01 reads the packaged value before installation; `post-fs-data.sh` also fails safe to stock on any unrecognized value, which bounds the damage.
- Risk (`AUTOPSY-P1-02` realized): the release turns out to be defective in some way the working tree was not. Impact: the fork between shipped and validated is real and larger than expected. Mitigation: this is the intended outcome of the sub-phase — the finding is routed to Phase 9 rather than patched in place, so the release process is fixed rather than the symptom.
- Risk: the diff shows changes the operator dismisses as expected without checking. Impact: a real regression is filed as noise, which is precisely the misattribution pattern this phase exists to break. Mitigation: the acceptance criteria require a per-line account, not a summary judgment.
- Risk: the flash leaves the camera in a broken state and there is no written recovery path. Impact: the user is left improvising, and `QAS-01` documents that this gap is unmitigated today. Mitigation: the module can be disabled through KernelSU and the mode set to stock, which is the conceptual rollback Autopsy section 10 describes; the written runbook is a Faz 9.2 deliverable and its absence is a known, accepted risk for this sub-phase.
- Risk: the launcher rendering check is subjective. Impact: an ambiguous verdict on v2.1's headline fix. Mitigation: the check is binary — the icon is visible or it is blank — and the v2.0 failure mode (white on white) is specific enough to recognize.
- Risk: the snapshot is captured but never designated as the baseline, and later sub-phases each pick their own reference. Impact: comparisons across phases stop being comparable. Mitigation: F2.2-07 assigns a name and later contract tables reference it.

## 12. Desired End State

The device runs the actual released v2.1 artifact. Two snapshots bracket the installation, their diff is fully accounted for, and the post-flash snapshot is named as the roadmap baseline that Phases 3 through 5 diff against. The three v2.1 surface claims — version reporting, four tiles, launcher rendering — are verified by the user rather than assumed. The never-flashed question is closed with a date.

The evidence an implementer should produce is the archive verification record, the two stored snapshots, the annotated diff, the installer transcript, and the manual checklist result.

The ledger summary Step 4 should append records: the archive checksum, the flash date, the baseline snapshot identifier, the accounted diff, and whether any finding was routed to Phase 9.

## 13. Next Sub-Phase Transition Criteria

- Both snapshots exist and their diff is accounted for line by line.
- The module reports v2.1 and versionCode 12 on the device.
- The camera opens with a live preview after the reboot.
- The baseline snapshot has a name that later sub-plans can reference.
- `EV-14` is resolved and the flash date is recorded.
- Any defect found in the release is routed to Phase 9 as a finding rather than patched in the working tree.
