# Faz 8.3 — Camera Modes on the Android 16 Build

## 1. Context

Main-Planing Phase 8 (`SNAP-2026-09-10-MAIN`) sets the goal "Carry the project's camera work onto the Android 16 build". Its desired end state is "The camera modes work on the Android 16 build". Its acceptance signal reads: "The module's md5 guards accept the Android 16 camera HAL and sensor module, or the patches are re-derived for them, and the release checklist passes on that build."

Neither `Faz8.1` nor `Faz8.2` covers that acceptance signal. `Faz8.1` measures whether the guards *would* accept the Android 16 blobs. Nothing yet installs the module there or runs the checklist. This sub-plan, created by planning run 18 on 2026-09-10, closes that gap for the **carry-over path only**. If `Faz8.1` labels either layer anything other than carry-over — a HAL re-derivation, or a sensor adaptation or re-derivation — this sub-plan is blocked, and the ledger carries a replanning input instead. Main-Planing's `high` token band for Phase 8 describes that re-derivation, and it is deliberately not decomposed on speculation.

What carries over is concrete. `ishtar-cam-modes` v2.2 (versionCode 13) was built by `scripts/build-release.py` (`Faz9.1`, `IMPL-76`), installed with `ksud module install` and verified after a real reboot (`IMPL-81`). It is checked by `docs/release-checklist.md`'s eighteen capabilities `C-01`–`C-18` and proving commands `PC-01`–`PC-18` (`Faz9.2`, verified), with a per-release evidence record format in its section 7. `IMPL-87` and `IMPL-88` re-ran the camera rows on Android 15 as recently as 2026-09-09.

Two things this sub-phase inherits have not been exercised on Android 16. Root: the module is a KernelSU module, and the new build is not rooted. And the camera restart ordering: Project-Ontology invariant 3 requires the client to stop before the HAL, and `setmode.sh` encodes it by init service name, and nobody has listed those names on Android 16. The name in `refs/a16_ishtar` commit `05efdac`'s crash log, `vendor.qti.camera.provider-service_64`, is a process name, not an init service name.

**Amended 2026-09-13 by planning run 19 (bounded Step 2 amendment: `AUDIT-FIX-46`, `-50`, `-51`).** Three corrections:

1. **The gate requires carry-over on both layers.** A sensor adaptation label blocks this sub-plan exactly like a HAL re-derivation label: no sub-plan adapts a blob, and an adapted blob cannot pass the unchanged v2.2 archive's `EXPECT_MD5`.
2. **The repaired smoke fields are used.** `FIND-3.7-02` and `FIND-3.10-01` were repaired on 2026-09-06 (`IMPL-80`, `DEC-20`). The trap reading therefore uses `prefs.trap.armed`, and PC-04 uses the repaired single-dump `probe_main_rows`, with the tag-header substitute kept as a cross-check. The audit worded this as grading PC-17 on `prefs.trap.armed`. `docs/release-checklist.md` shows that PC-17 reads `hal.mount.count` and `sensor.mount.count`, which were never defective, so PC-17 is graded on those, and the trap reading taken beside it uses `prefs.trap.armed`.
3. **The restart check lists the Android 16 init service names.** `wait_svc` treats a missing service as stopped, so the check also counts "switch has no effect" as a failure.

`Faz8.1`'s static half (`IMPL-92`) labelled both layers carry-over on static values; the gate still needs three-way agreement.

## 2. Goal

On the booted `beryl` build, with root established by the user, install the unchanged `ishtar-cam-modes` release and run the release checklist's device rows. Every row either passes, or fails with a recorded cause. The module stays reversible by disable-plus-reboot throughout. The result is written as a per-release evidence record for "v2.2 on Android 16".

## 3. Description

The problem is that a matching md5 proves only input identity. The Android 16 framework, the camera provider service, the `libui-v34` shim linked into `camera.xiaomi.so`, KernelSU on a different kernel, and the AGC port on a new Android version can each break a capability that the byte-identical HAL and sensor blobs would otherwise support. Only running the checklist answers that.

It belongs last in Phase 8's camera track. It needs `Faz8.1`'s carry-over classification and a device on the new build from `Faz7.3`. It is independent of `Faz8.2`: a kernel merge would change the kernel under test, and running this first gives any later merge a recorded Android 16 baseline to compare against.

The vibecoding slice strategy is gate, root, install, snapshot, then rows. The first useful slice is the install itself. `customize.sh`'s own guard lines state, before anything is mounted, whether the sensor checksum is accepted and whether the HAL is recognised. That is the fastest end-to-end confirmation of `Faz8.1`'s static result on the real device. The second slice is one `scripts/smoke.sh` snapshot. Its fields show which parts of the instrument survive the new build, and the checklist rows that depend on them follow.

What should not be over-planned: fixes for rows that fail. A failing row is a finding with a cause. Changes to `setmode.sh`, `smoke.sh` or the tile app for Android 16 are follow-up work routed through the ledger, not improvised in this sub-phase. The exception is invariant 3: if the restart ordering cannot be confirmed, mode switching stops until it is.

## 4. Scope

- A gate read: `Faz8.1`'s per-layer classification — carry-over on both layers — and three-way agreement, and `Faz7.3`'s device state.
- Root on the `beryl` build, performed by the user, with the method recorded as a decision (it depends on the kernel `Faz7.1` pinned).
- Installing the v2.2 archive with its sha256 checked against `docs/release-manifest.md`, and recording `customize.sh`'s guard verdict lines.
- A `scripts/smoke.sh` snapshot on Android 16, with each field recorded as working, absent-expected or broken.
- Confirming the camera restart ordering against the Android 16 init service names, listed with `getprop`, before the first mode switch.
- Running the checklist's device rows as `docs/release-checklist.md` section 3a specifies, with section 4's repairs applied: `prefs.trap.armed` for the trap reading, the single-dump `probe_main_rows` for PC-04 with the tag-header substitute as a cross-check, and section 4c's `C-09` limit.
- AON procedure step 4 (mechanism A), deferred here from `Faz7.3` because it needs root.
- A per-release evidence record for v2.2 on Android 16 in the checklist's section 7 format.
- The disable-plus-reboot restore exercised once at the end, per `docs/recovery-runbook.md`.
- Findings for every failed row, routed through the ledger.

## 5. Out of Scope

- Any HAL offset re-derivation, sensor blob regeneration, or patch-table change. That is the re-derivation or adaptation path, blocked by the gate.
- Editing `setmode.sh`, `halpatch.sh`, `customize.sh`, `scripts/smoke.sh`, the tile app or the WebUI for Android 16. Needed changes are findings.
- Rebuilding or re-signing the release archive. The v2.2 archive is installed as built.
- The kernel LTS merge. `Faz8.2`.
- The `ishtar-aon-fix` merge question, which `DEC-04` answered as "keep separate".
- Updating the AGC APK or its patches for Android 16. If AGC does not install or run, that is a recorded row result.
- Making Android 16 the project's primary release target. That is a Phase 9 decision after this evidence exists.

## 6. Current Repository Evidence

**The release under test.** `scripts/build-release.py` builds the archive deterministically, and `VAL-BUILD2` found two builds byte-identical. `docs/release-manifest.md` records per-entry and archive digests. `IMPL-81` installed v2.2 with `ksud module install` and verified it after a real reboot as v2.2 / 13. The archive carries no 27 MB binary (PC-14, assertion A2); the HAL patch is applied on-device from `blobs/hal-fullres.patch`.

**The checklist.** `docs/release-checklist.md` section 3a defines `PC-01` to `PC-18`. Several are human-only: PC-02/03 photographs, PC-05 Open Camera capture, PC-09 tiles by eye, PC-11 Action button, PC-13 video. Section 4 analyses three rows whose detector was unsound. Two were repaired on 2026-09-06 by `IMPL-80` under `DEC-20`, and section 4 says so:

- **`FIND-3.7-02`** — the trap audit counted names, not values. `scripts/smoke.sh` now also reports `prefs.trap.armed`, "the field a release gate should assert is 0".
- **`FIND-3.10-01`** — a line-range slice across two dumps. `probe_main_rows()` now locates the block inside a single dump.

The third, **`C-09`** — the tiles readback measures something else (section 4c) — is a scope limit and is unchanged.

**The checklist's section 3 map still labels `C-04` with `FIND-3.10-01` and `C-17` with `FIND-3.7-02`, and PC-04's comment still reads "DEFECTIVE via smoke.sh"** (`AUDIT-FIX-50`). Those labels predate the repair. PC-17 reads `hal.mount.count` and `sensor.mount.count`, which the checklist calls sound; its row was marked only because the trap probe shares its block. PC-13's frame-rate method is the stts net cadence plus presentation-order deltas precedent from `IMPL-88`, and `DEC-23` accepted that deviation from the literal clause. The Android 15 reference values: PC-05 8192x6144 = 50.33 MP; PC-06 `agc.photo_size.back.derived = 4096x3072`, 12.58 MP, black fraction below 0.01; PC-13 60 fps on the stock camera app.

**The guards on install.** `customize.sh:14` `EXPECT_MD5=9e4d0fe1…`. It aborts on a sensor mismatch and degrades on an unrecognised HAL (PC-18). PC-16 aborts on any `ro.product.device` other than `ishtar`, which the `beryl` build must still report.

**The restart invariant.** Project-Ontology invariant 3 and `TRACE-04` (`setmode.sh` `restart_camera()`, `wait_svc()`). `IMPL-13` confirmed the ordering on Android 15 across ~17 transitions, and recorded that `CSIPHYHw:4 AvailableResource=0` is not a leak signature. `setmode.sh` stops `cameraserver`, then `vendor.camera-provider` and `vendor.camera-provider-2-7-ext`. It waits through `wait_svc()` (line 110), which reads `getprop "init.svc.$1"`, and the stopped branch returns success on any value other than `running`, including an empty one. A name that does not exist on Android 16 therefore passes the stop wait at once. `stop` and `start` then act on nothing, and the provider never reloads the sensor blob: the symptom is a mode switch with no effect, not a black preview (`AUDIT-FIX-51`). `refs/a16_ishtar` commit `05efdac`'s crash log names `vendor.qti.camera.provider-service_64`, which is a process name, not an init service name. The Android 16 init service names have not been listed.

**AON.** `docs/aon-verification.md` section 5 step 4: "reinstall the module and reboot … confirm the guard behaves as read", using the section 8.1 mount-identity test in place of the unreliable log discriminator (`FIND-6.2-02`).

**Recovery.** `docs/recovery-runbook.md` verified mechanically that no module script writes to `/odm`, so "disable-plus-reboot is a complete restore for any module-caused failure" (`IMPL-19`). The claim was established on Android 15 and is re-exercised here.

## 7. Planned Work Breakdown

- F8.3-01 — Pass the gate
  - Description: Read `Faz8.1`'s classification (HAL carry-over and sensor carry-over) and its agreement status, and `Faz7.3`'s record that the device is on the `beryl` build. On any other label — a HAL re-derivation, or a sensor adaptation or re-derivation — stop and confirm the replanning input is in the ledger.
  - Output: A gate record.
- F8.3-02 — Establish root
  - Description: The user roots the build by a method compatible with its kernel, recorded as a decision with the kernel identity from `Faz7.1`. Record `ksud` and manager versions.
  - Output: A root record and the method decision.
- F8.3-03 — Install the release as built
  - Description: Verify the v2.2 archive's sha256 against `docs/release-manifest.md`, install with `ksud module install`, reboot, and record `customize.sh`'s guard lines and `ksud module list`.
  - Output: An install record with the guard verdicts.
- F8.3-04 — Snapshot and classify the instrument
  - Description: Run `scripts/smoke.sh` in `stock` mode, and mark each field working, absent-expected or broken, with a reason for each broken one.
  - Output: An Android 16 baseline snapshot with a field classification.
- F8.3-05 — Confirm the restart ordering before switching modes
  - Description: List `getprop | grep init.svc` on the Android 16 build, and compare the camera init service names with the three `setmode.sh` uses: `cameraserver`, `vendor.camera-provider` and `vendor.camera-provider-2-7-ext`. A name `setmode.sh` uses that is absent from the list is a negative verdict, because `wait_svc` would pass it at once. Then confirm, by reading, that client-before-HAL still holds before any tile or Action switch. If either check fails, stop mode switching and raise a finding.
  - Output: An invariant 3 verdict for Android 16.
- F8.3-06 — Run the checklist device rows
  - Description: Execute PC-01 to PC-18 as section 3a specifies, with section 4's repairs applied:
    - PC-04 is read from the repaired single-dump `probe_main_rows` block, with the tag-header substitute recorded as a cross-check.
    - The trap reading uses `prefs.trap.armed`, not `prefs.trap.count`.
    - PC-17 uses `hal.mount.count` and `sensor.mount.count`.
    - Section 4c's `C-09` limit applies.

    Human rows are performed by the user. Record each row pass, fail with cause, or not-applicable with reason, against the Android 15 reference values.
  - Output: Eighteen row results.
- F8.3-07 — Run AON procedure step 4
  - Description: With `ishtar-aon-fix` installed on the `beryl` build, apply the section 8.1 mount-identity test and record whether the module's guard leaves the native symlink alone, as section 5 step 4 expects.
  - Output: The mechanism A result on Android 16.
- F8.3-08 — Write the evidence record
  - Description: Add a section 7 record to `docs/release-checklist.md` for v2.2 on the `beryl` build, with build identity, blob md5s, and pass, fail and waived counts. In the same edit, point the section 3 map's `C-04` and `C-17` labels and PC-04's "DEFECTIVE via smoke.sh" comment at section 4's repair notes (`AUDIT-FIX-50`).
  - Output: A per-release evidence record.
- F8.3-09 — Exercise the restore and route findings
  - Description: Disable the module, reboot, snapshot, and confirm stock state per `docs/recovery-runbook.md`. Leave the module enabled or disabled per the user's choice. Route each failed row and any broken instrument field as a finding, and update `DEC-07` with the functional result.
  - Output: A restore record, routed findings, and the `DEC-07` update.

## 8. Acceptance Criteria

- The gate record shows carry-over on both the HAL and the sensor layer, and three-way blob agreement, before anything is installed. Any other label left the sub-plan blocked with a replanning input.
- The root method is a recorded user decision naming the kernel it applies to.
- The archive's sha256 matched `docs/release-manifest.md` before install, and `customize.sh`'s guard verdict lines are recorded verbatim.
- The Android 16 smoke snapshot exists with every field classified.
- Invariant 3 has an Android 16 verdict, taken on the listed init service names, before the first mode switch, and no mode switch occurred without it.
- Every checklist row PC-01 to PC-18 has a recorded result. PC-04 is graded on the repaired single-dump probe with the substitute as a cross-check, the trap reading uses `prefs.trap.armed`, PC-17 uses the two mount counts, section 4c's limit is applied, and PC-13's frame rate uses the `IMPL-88` method.
- AON step 4 has a result using the mount-identity test.
- A section 7 evidence record for v2.2 on the `beryl` build exists in `docs/release-checklist.md`.
- Disable-plus-reboot returned the device to a stock camera state, shown by snapshot.
- Every failed row and broken field is a routed finding, and no module source file was edited.
- `DEC-07` carries the functional result.

## 9. Validation and Test Approach

Validation is live on the device, bracketed by snapshots, using the checklist's existing proving commands.

- `VAL-GATE` (proposed) — read `Faz8.1`'s classification and `Faz7.3`'s device state.
- `VAL-ROOT` (proposed) — `ksud` version output and the manager's module list reachable over `adb`.
- `VAL-INSTALL` (existing method, `IMPL-81`) — sha256 check, `ksud module install`, reboot, `ksud module list`.
- `VAL-SMOKE` (existing) — `scripts/smoke.sh` snapshot plus field classification.
- `VAL-RESTART` (proposed) — `getprop | grep init.svc` on the Android 16 build, its camera init service names compared with `setmode.sh`'s `cameraserver`, `vendor.camera-provider` and `vendor.camera-provider-2-7-ext`, and a read of `restart_camera()`/`wait_svc()` against that list. Two failure signals count: black preview, and a mode switch with no effect because the provider never stopped or restarted. `CSIPHYHw AvailableResource` is not a signal.
- `VAL-CHECKLIST` (existing) — `docs/release-checklist.md` section 3a commands PC-01 to PC-18, read with section 4's repairs: `prefs.trap.armed` and the single-dump `probe_main_rows`, with the PC-04 substitute as a cross-check.
- `VAL-BUILD` (existing ID, `Faz6.2`) — AON procedure step 4 with the section 8.1 mount-identity test.
- `VAL-REVERT` (existing method, `docs/recovery-runbook.md`) — disable, reboot, snapshot.
- `VAL-DOCS` (proposed) — read back the evidence record and the routed findings.

Local versus live: live throughout, with host-side read-backs. Security validation covers the archive sha256 before a root-privileged install, and the fail-closed guard verdicts. Ontology validation applies to invariants 1, 2, 3 and 10 and to the vocabulary: `fullres` is the HAL state, `50mp` is the mode name.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| docs/release-checklist.md | modified | A new section 7 evidence record for v2.2 on the `beryl` build, and the section 3 labels and PC-04 comment pointed at section 4's repair notes. | VAL-CHECKLIST, VAL-DOCS |
| docs/release-manifest.md | existing | The archive sha256 checked before install. | VAL-INSTALL |
| scripts/smoke.sh | existing | Android 16 baseline and restore snapshots, including the repaired `prefs.trap.armed` and single-dump `probe_main_rows` fields; not edited. | VAL-SMOKE, VAL-CHECKLIST, VAL-REVERT |
| ishtar-cam-modes/setmode.sh | existing | Read-only: `restart_camera()`'s three init service names and `wait_svc()` compared against the Android 16 `init.svc` list. | VAL-RESTART |
| ishtar-cam-modes/customize.sh | existing | Read-only: guard verdict lines expected on install. | VAL-INSTALL |
| docs/recovery-runbook.md | existing | The disable-plus-reboot restore exercised on Android 16. | VAL-REVERT |
| docs/aon-verification.md | modified | Step 4's Android 16 result appended beside `Faz7.3`'s step 3 section. | VAL-BUILD |
| snapshots | existing | Receives the install record, snapshots, row evidence and restore snapshot. | VAL-SMOKE, VAL-CHECKLIST |
| Planner-docs/Planing-Ledger.md | modified | Root decision, row findings, the `DEC-07` functional result, and the implementation row. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on `Faz8.1` for carry-over on both layers with three-way agreement, and on `Faz7.3` for a device on the `beryl` build. Depends on `Faz9.1` and `Faz9.2` for the archive, manifest and checklist, all verified.

Independent of `Faz8.2`. Running this first gives a later merge an Android 16 baseline.

Blocks Phase 9's decision on whether Android 16 becomes a release target, and closes Main-Planing Phase 8's camera acceptance signal on the carry-over path.

Required decisions, all the user's: the root method; whether the module stays enabled at the end; `DEC-07`'s final answer.

Required credentials: none recorded. Root is established on the device by the user.

Required infrastructure: the device on the `beryl` build, `platform-tools/adb`, the v2.2 archive, Open Camera and AGC for their rows.

Required human approvals: root, install, every capture and recording, every tile and Action press, and the final enable state. Main-Planing section 5's boundary applies in full.

Fresh session token and context risk: medium. Eighteen rows with human steps, and camera dumps. Mitigation: per-row verdict lines and the section 4 slicing rules, not whole dumps; rows may span sessions if each session opens and closes with a snapshot. Subagents: not recommended; the device is a single stateful resource.

## 11. Risks and Mitigations

- Risk (invariant 3): `setmode.sh` stops or waits on a service name that differs on Android 16. Impact: either the ordering silently inverts, with black preview in every mode and leaked allocations until reboot, or `wait_svc` passes the missing name at once and the provider never restarts, so a mode switch silently has no effect. Mitigation: F8.3-05 lists the init service names before any switch, `VAL-RESTART` counts both symptoms as failures, and mode switching stops on a negative verdict.
- Risk: md5 agreement is read as functional proof. Impact: a broken capability is declared carried over. Mitigation: acceptance requires every checklist row to have a result.
- Risk: root on the new build conflicts with its kernel. Impact: no module can install, or the device fails to boot. Mitigation: the method is a recorded user decision tied to the kernel identity, and `Faz7.3`'s return path stays available.
- Risk: the smoke script misreports on Android 16 and a row is graded on a broken field. Impact: false pass or false fail. Mitigation: F8.3-04 classifies every field before any row uses it.
- Risk: rows are graded on section 3's pre-repair labels — `prefs.trap.count`, or PC-04 treated as defective. Impact: a good device fails the trap gate on inert keys, or the repaired detector is bypassed. Mitigation: F8.3-06 applies section 4's repair notes, with the substitute only as a cross-check, and F8.3-08 corrects the labels.
- Risk: a failing row is fixed by editing module sources on the spot. Impact: the tested artifact no longer equals the released artifact, and Android 15 may regress. Mitigation: out of scope; failures are routed findings.
- Risk: AGC on Android 16 re-selects 50 MP or fails to start. Impact: `R12`'s silent reversion on a new platform. Mitigation: PC-06 reads the derived photo size from the snapshot and records a black fraction, as on Android 15.
- Risk: the restore claim does not hold on Android 16. Impact: a module-caused failure without the documented recovery. Mitigation: F8.3-09 exercises it once and records the snapshot.

## 12. Desired End State

The unchanged v2.2 release is installed on the Android 16 `ishtar` build. Its guards' verdicts are recorded, invariant 3 is confirmed for the new service names, every checklist row has a recorded result, AON mechanism A is checked, and disable-plus-reboot is shown to restore. `docs/release-checklist.md` carries an evidence record for this build, failures are routed as findings, and `DEC-07` reflects what actually works. If the gate failed on a re-derivation or adaptation label, the ledger instead carries the replanning input and nothing was installed.

Evidence the implementer produces: the gate, root and install records; the classified smoke snapshot; the invariant 3 verdict; eighteen row results; the AON step 4 result; the evidence record; the restore snapshot.

The ledger summary Step 4 appends: the root method decision, the guard verdicts, the invariant 3 verdict, pass/fail/waived counts with failed row ids, the AON step 4 result, the restore result, the final enable state, and the `DEC-07` update.

## 13. Next Sub-Phase Transition Criteria

- The evidence record exists, and every failed row is a routed finding.
- Invariant 3 is confirmed on Android 16, or mode switching is recorded as stopped with a finding.
- The restore is exercised and recorded.
- `DEC-07` carries the functional result, and Phase 9 has the evidence to decide whether Android 16 becomes a release target.
- Or: the gate failed, nothing was installed, and the re-derivation or adaptation replanning input is in the ledger.
