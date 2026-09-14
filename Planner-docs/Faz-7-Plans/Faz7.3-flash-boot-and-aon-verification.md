# Faz 7.3 — Flash, Boot and AON Verification on the Device

## 1. Context

Main-Planing Phase 7's acceptance signal reads "A flashable build output exists and boots; the rental time the build consumed is recorded", and its closing note states "Flashing and the boot check remain the user's actions." `Faz7.2` produces the output and records the rental. This sub-phase, created by planning run 18 on 2026-09-10, owns the boot. It is kept apart from the paid session for two reasons. It happens after the server is gone. And it is the first whole-system flash in this roadmap, on the user's daily device, which carries a different risk than any module flash before it.

Two registered obligations land here. **`Faz6.2` registered the AON verification (`VAL-BUILD`) against Phase 7.** `docs/aon-verification.md` section 5 holds the procedure, and section 6 tabulates the response to each outcome. **`FIND-6.2-03` (P2) was routed to Phase 7:** `IMPL-75`'s step 0 on the current Android 15 device returned a *negative* baseline. The path is present through the runtime module, but the NCS providers for aperture and face-scene do not register. Section 8.4 therefore instructs that "a Phase 7 build must … not be judged against 'matches the baseline' … **Judge it against the strings tabulated in 8.2 instead**."

A freshly flashed Android 16 build carries no modules, which makes it the naturally module-absent state that procedure step 3 needs. No uninstall is required.

Project-Ontology invariant 10 governs the daily-use question: every camera patch is bound to one exact vendor build. `Faz8.1` measures whether the Android 16 blobs are that build. This sub-phase records what the device actually runs, so the user decides to stay or restore knowing the camera consequence.

**Amended 2026-09-13 by planning run 19 (bounded Step 2 amendment: `AUDIT-FIX-45`, and `AUDIT-FIX-44`'s device half).** The return path and the restore criterion were written as if a whole-system flash preserves `/data`. No source on this project establishes that for Android 15 → 16 or for 16 → 15. If either direction needs a data format, the root setup, both modules and the AGC pin (`pref_48m_key=0`) are lost, not preserved. The amendment makes five changes:

- `F7.3-01` records AOSPA's documented data requirement for both directions.
- Where a format is required, the return path gains re-rooting, the v2.2 reinstall against `docs/release-manifest.md`, the AGC re-configuration by `docs/agc-12mp-configuration.md` section 2, and a trap audit.
- `F7.3-02` states the wipe at the go/no-go.
- `F7.3-07` is graded against the re-established state.
- `F7.3-02` and `F7.3-03` take the artifacts and install methods from `docs/build-environment.md` section 11, which `IMPL-91` wrote and `Faz7.2` retrieves. The firmware question stays here, as that section says.

One conservative reading is recorded rather than hidden: where AOSPA's documentation does not settle the data requirement, `F7.3-01` writes the re-establishment steps anyway. No work item was added or removed.

## 2. Goal

Flash the retrieved `beryl` build only after a working return path to the current Android 15 state is recorded. Establish a boot verdict and the on-device identity of the guarded camera blobs. Execute AON procedure step 3, judged against `docs/aon-verification.md` section 8.2's exact strings. Leave the device either on the new build by the user's informed choice, or back on Android 15 and re-verified against its pre-flash snapshot, with its configuration preserved or, if a data format was required, re-established.

## 3. Description

The problem is that everything before this sub-phase proves only that a package exists. Whether it boots on `ishtar`, whether the camera stack comes up, and whether the Faz 6.1 device-tree fix creates the AON path natively can only be learned on the device.

It belongs after `Faz7.2` for the obvious reason. It belongs before `Faz8.3` because the camera module cannot be judged on a build whose basic boot and camera enumeration are unknown.

The vibecoding slice strategy is return path first, flash second. The first useful slice costs nothing on the device: a pre-flash `scripts/smoke.sh` snapshot, the installed build fingerprint, the module list, and the location and sha256 of the currently installed Android 15 package with the steps that re-flash it, and AOSPA's documented data requirement for both directions. If that record cannot be completed, the flash does not happen. The fastest useful signal after flashing is boot plus camera enumeration: `dumpsys media.camera` lists devices, and the Android 15 figure is 13.

What should not be over-planned: diagnosis of a non-booting build or a broken camera stack. Either is a recorded outcome that routes back to a rebuild decision or to the replanning trigger, not an open-ended debugging session on a daily device.

Mechanism A of the AON fix — the runtime module — needs root on the new build to install. Root on Android 16 depends on the kernel `Faz7.1` pins and is established in `Faz8.3`, so procedure step 4 is deferred there rather than forced here.

## 4. Scope

- A pre-flash record: smoke snapshot, build fingerprint, KernelSU module list, the current Android 15 package's location and sha256, AOSPA's documented data requirement for 15 → 16 and 16 → 15, and the return procedure. Wherever a data format is required, the procedure is extended with re-rooting, the v2.2 reinstall, the AGC re-configuration and a trap audit.
- A package content check before flashing, against the artifacts and install methods `docs/build-environment.md` section 11 names: which partitions the chosen artifacts write, whether they include firmware images, and whether the flash formats `/data` — with the user's explicit go/no-go.
- The flash and boot, both the user's actions; boot verdict and camera enumeration count.
- On-device md5 and size of `/odm/lib64/hw/camera.qcom.so` and the IMX989 `sensormodule` `.bin`, compared against `Faz7.2`'s post-build values so the flashed image is known to be the built one.
- AON procedure step 3 on the module-absent build: the path's form and target, and one camera open matched against section 8.2's strings, classified by section 6's table.
- A daily-use assessment stating the camera consequence from `Faz8.1`'s result, and the user's stay-or-restore decision.
- If the user restores: the return procedure executed, the configuration re-established if the return formatted `/data`, and a post-restore smoke snapshot compared to the pre-flash one.
- Recording results in `docs/aon-verification.md` and routing `TRACE-13`, `ARC-06` and `FIND-6.2-03` updates.

## 5. Out of Scope

- Installing KernelSU, `ishtar-cam-modes`, `ishtar-aon-fix` or any module on the new build. `Faz8.3`.
- AON procedure step 4 (mechanism A on the new build), deferred to `Faz8.3` because it needs root.
- Flashing firmware images the user has not explicitly approved after F7.3-02's content check.
- Debugging a non-booting build beyond recording the symptom and restoring.
- Transferring any Android 16 AON result back to the Android 15 device. Section 8.3's "decisive follow-up" — the same capture in `stock` mode on Android 15 — stays open and separate.
- User data backup, which is the user's own responsibility and is only recorded as confirmed.
- Any camera patch, HAL write or sensor-blob mount.

## 6. Current Repository Evidence

**The procedure and its measured baseline.** `docs/aon-verification.md` section 5 step 3: "Uninstall `ishtar-aon-fix`, reboot, then `ls -l /vendor/lib64/camera/aon_front.pb` — conclusive result: it exists and is a symlink to `/odm/lib64/camera/aon_front.pb` … Open the camera and match the four provider strings." Section 8.1 establishes, by inode rather than by log, that on the current device the file is a regular file supplied by the module's bind mount (`dev=65065 inode=128025` on both paths). Section 8.2 tabulates the exact failing lines — `camxncsintfmiaperture.cpp:870 RegisterService() [Aperture]No Provider Objects available`, `camxncsdatasource.h:784 SetupNCSLinkForSensor() Aperture Sensor Handle is NULL`, `camxmultiplefacescene.h:249 … Failed to get ncs data` — with laser AF's hardware path up and OIS not evidenced either way. Section 5 step 2's log discriminator is measured unreliable (`FIND-6.2-02`), and the mount-identity test replaces it.

**The Android 15 state to return to.** Ledger section 6 and `IMPL-87`/`IMPL-88` record the device running `ishtar-cam-modes` v2.2 (versionCode 13) in `50mp` mode, sensor stock `9e4d0fe1…`, HAL `fullres` `fe0245a4…`, one mount on each path, AGC pinned at 12.58 MP. `docs/recovery-runbook.md` covers module-level recovery (disable plus reboot) and says nothing about a whole-system re-flash, which is why F7.3-01 must write that return path down. `scripts/smoke.sh` is the snapshot instrument; its fields assume the module is installed. On a clean Android 16 build several fields will legitimately read absent, and that must be recorded as expected rather than as a failure.

**Data format, and what it would erase (`AUDIT-FIX-45`).** No repository source states whether flashing AOSPA's Android 16 build over the Android 15 install, or returning from 16 to 15, requires a data format on `ishtar`. `docs/build-environment.md` section 11 routes the question to this sub-phase, and `Faz7.1` read no source for it. A format would erase the daily configuration that lives outside the flashed partitions: the root setup, both modules and AGC's preferences. The procedure that re-establishes each is already recorded:

- `docs/release-manifest.md` records the v2.2 archive's sha256 (`407fb9be…`).
- `docs/agc-12mp-configuration.md` section 2 sets the pin: write `pref_48m_key=0` and `pref_camera_resolution=full`, then two cold starts, then read (`FIND-3.10-04`).
- `docs/release-checklist.md` PC-06 names the snapshot fields that prove the pin: `agc.pref_48m = 0`, `agc.pref_resolution = full` and `agc.photo_size.back.derived = 4096x3072`.
- `scripts/smoke.sh` reports `prefs.trap.armed`, the field a gate asserts is 0 (`IMPL-80`).

**Install artifacts (`docs/build-environment.md` section 11, `IMPL-91`).** `Faz7.2` retrieves each of these with sha256 verified at both ends:

| Artifact | What it is for |
|---|---|
| `aospa-<version>-image.zip` | The fastboot package, for `fastboot update` |
| `aospa-<version>.zip` | `adb sideload` from AOSPA recovery, which that section records as the current XDA `ishtar` method |
| `recovery.img` | Flashed before sideloading |
| `boot.img`, `init_boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img`, `vbmeta_system.img` | The boot chain, retrieved loose |

`F7.3-02` and `F7.3-03` choose among these; the install method is not re-researched here.

**Firmware.** `refs/a16_ishtar/board-info.txt` reads only `require board=ishtar`, with no firmware version gate in the tree. The manifest `README.md` records the blob lists as extracted from `OS2.0.101.0.VMAMIXM`. Whether the current device firmware matches what the `beryl` build expects is not established by any repository evidence. `docs/build-environment.md` section 11 records that firmware is not a build output and routes the question here.

**The camera service.** `refs/a16_ishtar` commit `05efdac` records a `vendor.qti.camera.provider-service_64` SIGSEGV in `camera.xiaomi.so` fixed by linking `libui-v34.so`. The fix is in the pinned tree. It is evidence that camera-stack crashes on Android 16 have occurred upstream and are the first thing to look for if enumeration fails.

**Continuity.** `TRACE-13` records the AON repair as partial and split, and `ARC-06` as intermediate. The ledger matrix keeps `Faz6.1` at `implemented` because "no build has yet consumed the `;SYMLINK=` entry". This sub-phase is where that changes.

## 7. Planned Work Breakdown

- F7.3-01 — Record the return path before touching the device
  - Description: Take a `scripts/smoke.sh` snapshot, the build fingerprint and `ksud module list`. Record the current Android 15 package's location and sha256 and the exact re-flash steps. Record from AOSPA's documentation, citing the source for each, whether flashing 15 → 16 requires a data format and whether returning 16 → 15 does. If either direction requires one, or no source settles it, write re-establishment into the return steps:
    1. Re-root by the method the Android 15 install used.
    2. Reinstall every recorded module, checking the v2.2 archive's sha256 against `docs/release-manifest.md`.
    3. Re-apply the AGC configuration by `docs/agc-12mp-configuration.md` section 2: write, two cold starts, read.
    4. Audit the trap keys: `prefs.trap.armed` must read 0.

    Have the user confirm their data backup. If any item cannot be completed, stop.
  - Output: A pre-flash record sufficient to return the device to its present configuration, with the data requirement for both directions and, where needed, the re-establishment steps.
- F7.3-02 — Inspect the package and take the go/no-go
  - Description: List which retrieved artifacts the chosen install method from `docs/build-environment.md` section 11 consumes, which partitions they write, and whether they carry firmware images. Put the list, the firmware question, the invariant-10 consequence known so far, and F7.3-01's data requirement to the user. Where a format is required, state plainly that the flash erases the root setup, both modules and the AGC pin, and that a return re-establishes them. The user decides whether to flash.
  - Output: A package content record, the stated data consequence, and the user's recorded decision.
- F7.3-03 — Flash and boot
  - Description: The user flashes by the install method recorded at F7.3-02, from `docs/build-environment.md` section 11, using only artifacts whose sha256 `Faz7.2` verified. Record boot or no boot, time to boot, and `dumpsys media.camera` device count against Android 15's 13, as a fact rather than a pass condition.
  - Output: A boot verdict and a camera enumeration record.
- F7.3-04 — Read the guarded blobs on the device
  - Description: md5 and size of `/odm/lib64/hw/camera.qcom.so` and `/odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, compared against `Faz7.2`'s post-build evidence.
  - Output: A three-way identity record (vendor repository value via `Faz8.1`, build output, device) for `Faz8.1`.
- F7.3-05 — AON procedure step 3, module absent
  - Description: `ls -l` and `readlink` on `/vendor/lib64/camera/aon_front.pb`, plus the mount-identity test of section 8.1 to show no bind mount supplies it. Then one camera open, with the camera-stack log matched against section 8.2's strings. Classify by section 6's table.
  - Output: The `VAL-BUILD` result and its section 6 row.
- F7.3-06 — Assess daily use and take the user's decision
  - Description: State what the device loses by staying: no module, no 50 MP layer or sensor modes until `Faz8.3`, plus whatever `Faz8.1` says about carry-over. State what it gains and anything observed broken. The user decides to stay or restore.
  - Output: A written assessment and the decision.
- F7.3-07 — Restore, if chosen
  - Description: Execute F7.3-01's return steps. If the return formatted `/data`, re-establish the configuration by F7.3-01's steps before comparing: re-root, reinstall every recorded module with the v2.2 archive's sha256 checked against `docs/release-manifest.md`, re-apply `docs/agc-12mp-configuration.md` section 2, and audit the trap keys. Otherwise, reinstall the recorded modules only if the re-flash removed them. Take a post-restore smoke snapshot and compare its comparable region with the pre-flash snapshot.
  - Output: A restore record showing the comparable region equal to the pre-flash one — preserved, or re-established after a format — with any remaining difference explained.
- F7.3-08 — Record and route
  - Description: Append the results to `docs/aon-verification.md` as a new section. Route `TRACE-13`, `ARC-06` and `FIND-6.2-03` updates, and propose the `Faz6.1` matrix row's move to `verified` if step 3 passed. Record step 4 as deferred to `Faz8.3`.
  - Output: Updated records and routed findings.

## 8. Acceptance Criteria

- The pre-flash record exists before the flash, with the Android 15 package's sha256, written re-flash steps, and AOSPA's documented data requirement for both directions with its source. Re-establishment steps are written wherever a format is required or the requirement is not settled. The user has confirmed a data backup.
- The package content list, the firmware answer and the data consequence are recorded, and the flash follows an explicit user decision made after reading them.
- A boot verdict is recorded; if the build booted, the camera enumeration count is recorded next to Android 15's 13.
- On-device md5 and size of both guarded blobs are recorded and compared against `Faz7.2`'s post-build values.
- AON step 3 records the path's form and target and the mount-identity result, and the camera-open log is matched line by line against section 8.2's strings. The outcome maps to exactly one row of section 6's table.
- Step 3 is not judged against a positive baseline, because section 8.4 establishes there is none.
- The daily-use assessment states the camera consequence explicitly, and the user's stay-or-restore decision is recorded.
- If the user restored, the post-restore snapshot's comparable region matches the pre-flash one. After a data format it is graded against the re-established state: the module list and versions, `agc.pref_48m = 0`, `agc.pref_resolution = full`, `agc.photo_size.back.derived = 4096x3072` and `prefs.trap.armed = 0` were re-established before the comparison. A field the format erased does not pass as an explained difference; any other difference is explained.
- Step 4 is recorded as deferred to `Faz8.3`, not as passed or failed.
- No firmware image was flashed without the user's explicit approval.

## 9. Validation and Test Approach

Validation is live on the device, bracketed by snapshots, with the user performing every flash and every camera open.

- `VAL-PREFLASH` (proposed) — the pre-flash record read back: snapshot file, fingerprint, module list, package sha256, the data requirement for both directions with its sources, and the return steps, including any re-establishment.
- `VAL-BOOT` (proposed) — boot verdict plus `adb shell dumpsys media.camera` device count.
- `VAL-BLOBMD5-DEVICE` (proposed) — `adb shell md5sum` and `stat -c %s` on both guarded paths, compared against `Faz7.2`'s evidence block.
- `VAL-BUILD` (existing ID, defined by `Faz6.2`) — `docs/aon-verification.md` section 5 step 3 with the section 8.1 mount-identity test and the section 8.2 string match.
- `VAL-RESTORE` (proposed) — `scripts/smoke.sh` after restore, comparable region diffed against the pre-flash snapshot. After a data format, the re-established fields — module list and versions, `agc.pref_48m`, `agc.pref_resolution`, `agc.photo_size.back.derived` and `prefs.trap.armed` — are read before the diff.
- `VAL-DOCS` (proposed) — read back the new `docs/aon-verification.md` section and the routed records.

Local versus live: entirely live, on the one device the project has. Security validation covers the firmware approval gate and confirms nothing is flashed from an unverified sha256. Ontology validation applies to invariant 10 through the on-device md5 read, and to the vocabulary: *stock* here means the Android 16 build's unmodified camera stack, not the Android 15 module mode named `stock`.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/smoke.sh | existing | Pre-flash and post-restore snapshots; expected-absent fields on a clean build are recorded, not treated as failures. | VAL-PREFLASH, VAL-RESTORE |
| docs/aon-verification.md | modified | A new section recording step 3 on the Android 16 build, and step 4's deferral. | VAL-BUILD, VAL-DOCS |
| docs/recovery-runbook.md | existing | Module-level recovery reference; its silence on whole-system re-flash is why F7.3-01 writes the return path. | VAL-PREFLASH |
| docs/build-environment.md | existing | Section 11: the retrieved artifacts and install methods F7.3-02 and F7.3-03 choose from; firmware is routed here. | VAL-PREFLASH |
| docs/release-manifest.md | existing | The v2.2 archive sha256, checked before any reinstall on a re-established return path. | VAL-RESTORE |
| docs/agc-12mp-configuration.md | existing | Section 2's write, two cold starts and read, used to re-establish the AGC pin after a data format. | VAL-RESTORE |
| snapshots | existing | Receives the pre-flash record, boot and enumeration record, blob md5s, AON capture and restore snapshot. | VAL-BOOT, VAL-BLOBMD5-DEVICE, VAL-BUILD |
| Planner-docs/Project-Comprehension.md | modified | `TRACE-13` and `ARC-06` updated from measured results only. | VAL-DOCS |
| Planner-docs/Planing-Ledger.md | modified | Implementation row, the stay-or-restore decision, `FIND-6.2-03` routing, and the proposed `Faz6.1` status change. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on `Faz7.2` for a flashable package with verified sha256 and the AON step 1 result; without step 1, a missing symlink cannot be attributed. Depends on `Faz6.2`'s procedure and on `Faz6.1`'s entry.

Benefits from `Faz8.1`'s static comparison, which ran before this sub-phase as `IMPL-92`: both layers are carry-over on static values. F7.3-02 and F7.3-06 can therefore state the camera consequence as a measurement rather than a possibility, pending `F8.1-06` and `F8.1-07`.

Blocks `Faz8.3`, which needs the device on the `beryl` build, and the built-output agreement check in `Faz8.1`.

Required decisions, all the user's: go/no-go after the package inspection and the stated data consequence; firmware approval if firmware is present; stay or restore.

Required credentials: none beyond the device's existing unlock state; nothing is recorded.

Required infrastructure: the device, `platform-tools/adb`, the retrieved artifacts, and the Android 15 package for the return path. A return that formats `/data` also needs the recorded module archives, including v2.2, and AGC.

Required human approvals: the flash itself, every camera open, the restore. Main-Planing section 5's approval boundary applies in full: flashing and photography are the user's actions.

Fresh session token and context risk: low to medium. The camera-stack log is the only voluminous output, and section 8.2's strings bound the match. Subagents: not recommended; the device is a single stateful resource.

## 11. Risks and Mitigations

- Risk: the build does not boot and the return path is incomplete. Impact: the daily device is down with no rehearsed recovery. Mitigation: F7.3-01 is a hard precondition, and the flash does not happen without it.
- Risk: the flash, or the return to Android 15, formats `/data`. Impact: the root setup, both modules and the AGC pin are lost, and a lost daily configuration passes the restore check as an explained difference. Mitigation: F7.3-01 records the data requirement both ways and writes re-establishment steps, F7.3-02 states the wipe before the decision, and F7.3-07 is graded against the re-established state.
- Risk: the package carries firmware that conflicts with the device's current firmware, or with a rollback protection index. Impact: potentially unrecoverable by ordinary re-flash. Mitigation: F7.3-02 inspects package contents first, and no firmware image is flashed without explicit user approval after that inspection.
- Risk: the flashed image is not the built image. Impact: every downstream md5 conclusion describes the wrong file. Mitigation: F7.3-04 compares the device values against `Faz7.2`'s post-build values.
- Risk: step 3 is judged against a positive baseline that does not exist. Impact: a false pass or false fail. Mitigation: acceptance requires the section 8.2 string match and a single section 6 row.
- Risk: an Android 16 AON result is carried back as a statement about Android 15. Impact: `FIND-6.2-03` is closed on the wrong configuration. Mitigation: out of scope by rule; the Android 15 `stock`-mode follow-up stays separate.
- Risk: the user stays on a build where the camera module cannot yet run. Impact: loss of the project's working capability for daily use. Mitigation: F7.3-06 states that loss explicitly before the decision, which is recorded.
- Risk: expected-absent smoke fields are read as failures, or genuine failures are dismissed as expected. Impact: a misread snapshot. Mitigation: the pre-flash record lists which fields are expected absent on a clean build before the post-flash snapshot is taken.
- Risk: the camera-provider crash fixed upstream by `05efdac` recurs in another form. Impact: enumeration fails and step 3 cannot run. Mitigation: F7.3-03 records enumeration as a fact first; a crash is recorded with its tombstone signature and routes to a rebuild decision, not to on-device debugging.

## 12. Desired End State

The `beryl` build has been flashed after a recorded, executable return path and an informed user decision. Its boot verdict, camera enumeration and on-device blob identities are recorded, and the latter agree with what was built. AON procedure step 3 has a result mapped to exactly one row of the negative-result table, judged against measured strings rather than a baseline that does not exist. The device is on the new build by the user's stated choice, or back on Android 15 with a snapshot showing its configuration preserved or, after a data format, re-established.

Evidence the implementer produces: the pre-flash record with the data requirement for both directions, the package content list, the boot and enumeration record, blob md5s, the AON capture with its section 6 classification, the daily-use assessment, and a restore snapshot if applicable.

The ledger summary Step 4 appends: the data requirement both ways, the go/no-go and firmware decisions, the boot verdict, the enumeration count, the blob md5 agreement, the `VAL-BUILD` result and section 6 row, the stay-or-restore decision, and the routed `TRACE-13`/`ARC-06`/`FIND-6.2-03`/`Faz6.1` updates.

## 13. Next Sub-Phase Transition Criteria

- The boot verdict and on-device blob md5s are recorded.
- AON step 3 has a classified result, and step 4 is recorded as deferred to `Faz8.3`.
- The user's stay-or-restore decision is recorded, and a restored device has a matching snapshot, with any configuration a data format erased re-established rather than explained.
- For `Faz8.3`: the device is on the `beryl` build, or the user has agreed to return to it for that sub-phase.
- If the build did not boot or the camera did not enumerate, the outcome is raised against ledger section 7's viability trigger, and Phase 8 does not start on assumption.
