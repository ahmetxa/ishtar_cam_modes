# Faz 10.1 — HyperOS 4 Camera Stack Survey

## 1. Context

Main-Planing Phase 10 (`SNAP-2026-11-15-MAIN`) aims to move `ishtar-cam-modes` onto HyperOS 4 only after the camera stack has been measured, and to ship v2.3 with the 50 MP HAL layer left unused (`DEC-33`). The phase end state is a module whose sensor-layer modes, tile and WebUI are shown on that ROM, with every capability claim taken from HyperOS 4 evidence rather than from the AOSPA record. The acceptance signal owned here is a dated list of camera service names, file labels, the KernelSU allowlist count, the root manager and the WebUI entry point.

Autopsy was not rerun in planning run 21 and predates the ROM change, so it is not a HyperOS 4 source. `EV-12` in Project-Comprehension states that a reversed restart blackened preview in every mode including stock, confidence `confirmed`, on AOSPA. `ARC-12` is still `uncertain`: reference modules ship SELinux rules, and this module's rules are unverified. Neither row measures HyperOS 4.

This sub-plan was specified by planning run 21 on 2026-11-15 and drafted on 2026-11-16. It is the gap `Faz10.2`, `Faz10.3` and `Faz10.4` would otherwise fill with AOSPA service names. `Faz10.5` waits on those three, so it waits on this record too.

A 2026-11-13 probe and a 2026-11-15 `PRB` pass at 13:01Z already exist, both with no project module installed. They are starting evidence. They are not the record later plans should cite, because that record has to live in the repository with one date per fact and with inferences marked as inferences.

## 2. Goal

Establish a dated read-only record of the HyperOS 4 camera services, file labels, allowlist count, SukiSU-Ultra manager, WebUI entry point and module mounts, before any later Phase 10 plan changes the phone or the module.

## 3. Description

The problem is a name mismatch that a restart would act on. `setmode.sh` still stops and starts `vendor.camera-provider-2-7-ext`, while the 2026-11-15 read showed `vendor.camera-provider-2-7-ext-uvc` running and the unsuffixed name only defined. The same unread gap covers the labels a `chcon` would apply, how many allowlist hits the tile package has, which activity owns `ksu://webui`, and whether a metamodule is installed.

It belongs in Phase 10 because the sensor layer, the trap cleanup and the tile chain each consume a different slice of that stack, and none of them should rediscover it by writing. Measurement is the phase's first slice for that reason, not because the script is large.

The vibecoding slice strategy: freeze the ten read-only command strings, execute only the eight that answer this survey, and refuse the temp file if an identity scan fails, before any note is written. The fastest validation signal is a host-side dry run that rejects an eleventh command and a planted fifteen-digit token, with the phone still untouched.

What should not be over-planned: a second smoke harness, a service-rename patch, or a yes-or-no on a system app. The probe is one Python file and a fixed argument list. Metamodule presence is recorded. Installing one is not asked.

Facts, inferences and AOSPA history stay in separate sentences. A fact carries the UTC date it was read. The claim that today's `setmode.sh` would wake the idle virtual-camera service is an inference until a later plan actually restarts, and this plan does not restart. `EV-12` remains an AOSPA row.

`DEC-33` is used here even though the ledger row is written later: on this ROM the HAL patch stays unused, and sensor-layer work is the part that continues. This survey does not patch `camera.qcom.so`, does not import an `.agc` file, and does not write `pref_camera_picturesize_back_key`.

## 4. Scope

- A host probe whose command table is the fixed PRB1-PRB10 texts, invoked only as `platform-tools/adb.exe -s dc27e5d0`.
- A fresh read of init-defined camera services, running camera services and process labels.
- SELinux labels of the HAL file, the IMX989 sensor file and their two parent directories.
- The allowlist hit count for `com.ishtar.cammodes`, with the allowlist file itself not printed.
- The SukiSU-Ultra package, its version and the activity that handles `ksu://webui`.
- Init-namespace module bind mounts, the KSU-sourced mount count, and whether a metamodule directory exists.
- Dated notes, an invariant 3 amendment that names the measured services, and Comprehension rows that keep AOSPA evidence labelled as history.
- One new snapshot file whose name contains `Faz10.1`, copied only after the identity scan passes.

## 5. Out of Scope

- Installing `ishtar-cam-modes`, switching a mode, or pressing the shutter. That is `Faz10.2`, and those acts stay the user's, inside a `scripts/smoke.sh` bracket.
- Editing `setmode.sh` so its provider names match HyperOS 4. That is `Faz10.2`.
- AGC owner and label, trap cleanup, any direct write of `pref_camera_picturesize_back_key`, any `sed -i` of a preference file, and any `.agc` import. That is `Faz10.3`, and trap cleanup still requires a backup first.
- Tile registration, the long-press WebUI launch, and removing `50mp` from `index.html`. That is `Faz10.4`.
- The v2.3 version bump, `Kullanim.txt`, and where `ishtar-aon-fix` sits on this ROM. That is `Faz10.5`.
- Reopening the 50 MP HAL layer. `DEC-33` leaves it off. `DEC-14` still withholds 50 MP inside AGC until new evidence exists. The wide RAW table is not narrowed here, and the `50mp` versus DCG/LN exclusion is not relaxed.
- An adb command that omits `-s dc27e5d0`, a command outside the PRB class, or `am start`.
- Changing an existing file under `snapshots/`, or adding `*.apk`, `*.zip`, `*.keystore` or `camera.qcom.so` to the tree.

## 6. Current Repository Evidence

`ishtar-cam-modes/setmode.sh:52-58` and `:79-83` were read in this Step 2 run. The stop order is `cameraserver`, then `vendor.camera-provider` and `vendor.camera-provider-2-7-ext`. The start order is those two providers, then `cameraserver`. The third name in that file has no `-uvc` suffix. Comments at `:38-46` already state the client-before-HAL stop, which matches Ontology invariant 3's stop half.

`Planner-docs/Project-Ontology.md` section 7 item 3 was read in this Step 2 run. It says client before HAL, cites the AOSPA black-preview failure, and does not name a HyperOS 4 service. Section 5's numbered restart ends at `start cameraserver` and never records the provider start that `setmode.sh:79-83` performs first. That shorter list is a documentation gap found in this run. It is not a device measurement.

Four `chcon u:object_r:vendor_file:s0` sites were read in this Step 2 run: `ishtar-cam-modes/post-fs-data.sh:70`, `ishtar-cam-modes/setmode.sh:256`, `ishtar-cam-modes/halpatch.sh:114`, and `ishtar-aon-fix/post-fs-data.sh:32-33`. The HAL md5 mismatch exit was read at `ishtar-cam-modes/post-fs-data.sh:101-107`. Whether that exit fires on the HyperOS 4 HAL is a `Faz10.2` bracket, not a conclusion of this survey.

`ishtar-cam-modes/action.sh:56` was read in this Step 2 run. It tests `/data/adb/ksu/.allowlist` for the tile package and does not print the file. `ishtar-cam-modes/webroot/index.html:195-204` calls `ksu.exec`, `:209` calls `ksu.toast`, and `:337` calls `ksu.enableEdgeToEdge` with no arguments. Those are repository calls. They are not a HyperOS 4 launch. `index.html:187` still lists `50mp` among the main modes; removing it is `Faz10.4` under `DEC-33`.

Main-Planing section 6, Phase 10 entry evidence, was read in this Step 2 run. The 2026-11-13 probe records HyperOS `OS4.0.0.44.WMACNXM`, Android 17, kernel 5.15.215, SELinux enforcing, and no project module installed. The HAL md5 prefix `2a955e68` is not the AOSPA stock prefix `c3fa63a8`. The sensor md5 prefix `9e4d0fe1` matches the module `EXPECT_MD5`. The same section's 2026-11-15 read records SukiSU-Ultra v4.3.0-r1, manager `com.sukisu.ultra`, versionCode 41140, no metamodule, no KernelSU-Next package, running services `cameraserver`, `vendor.camera-provider` and `vendor.camera-provider-2-7-ext-uvc`, and both target files labelled `vendor_file`.

The 2026-11-15 `PRB` inventory, read in this Step 2 run, timestamps that pass at 13:01Z. `ksu://webui` resolved to `com.sukisu.ultra/.ui.hdhrsdynpwdActivity`. Resolving `.ui.webui.WebUIActivity` found no activity. The allowlist path existed and the `com.ishtar.cammodes` count was 0. The init namespace had six `/adb/modules/` bind mounts and zero KSU-sourced mounts. `/odm/lib64/hw` was labelled `vendor_hal_file` while the HAL and sensor files were `u:object_r:vendor_file:s0`. The provider binary path recorded then was `/odm/bin/hw/vendor.qti.camera.provider-service_64`. The further claim that a `setmode.sh` restart would start the idle `vendor.camera-provider-2-7-ext` is an inference. This plan does not test it.

A source reading of SukiSU-Ultra v4.3.0-r1, explicitly not measured on the phone, says that build takes the module id only from the URI query and that an `--es id` extra closes the activity. This survey must not promote that reading to a device fact. Opening the activity is `Faz10.4`.

`scripts/smoke.sh:33` was read in this Step 2 run. It selects `platform-tools/adb.exe` and does not pass `-s`. This plan does not edit that script. `snapshots/20261113-1819__IMPL96__hyperos4-readonly-probe.txt` and `snapshots/20261113-1821__IMPL96__hyperos4-smoke-baseline.txt` are present and stay unmodified. `Project-Comprehension.md` currently ends its evidence register at `EV-45`. `EV-12` is the AOSPA restart row.

`ishtar-cam-modes/system/` is absent, confirmed in this Step 2 run by a directory lookup. The module bind-mounts its own sensor file at `post-fs-data.sh:72`. An upstream note, not re-fetched here, says KernelSU v3 and later mount a module `system/` tree only through a metamodule. That sentence stays an inference. `Faz10.4` evaluates a system app; this plan only records whether `/data/adb/metamodule` exists.

## 7. Planned Work Breakdown

- F10.1-01 — Freeze the ten-command probe
  - Description: `scripts/hyperos4-probe.py` stores the PRB1-PRB10 texts as data and runs a selected subset with `subprocess.run` of `platform-tools/adb.exe`, arguments `-s` and `dc27e5d0`, and `ANDROID_SERIAL=dc27e5d0` in the environment. Combined output goes to a file that `tempfile` creates in the host's `%TEMP%`, outside the repository. The temp file's life has a fixed order: scan it, copy a passing transcript into the new snapshot, then delete it; on an aborting hit it is deleted with nothing copied. There is no shell quotation step and no `am start`. PRB3 names `com.sukisu.ultra`. If PRB1 or PRB2 reports any other root manager package, the probe stops before PRB3 and asks the user. It does not substitute the package on its own, and it does not keep running the frozen string against the wrong manager.
  - Output: `scripts/hyperos4-probe.py`.

- F10.1-02 — Prove refusal without the phone
  - Description: A host check asks the probe for an eleventh command and expects refusal before adb is spawned. The identity scan has three pattern classes, and each class gets its own planted fixture that must stop the reader. Class one is any 15-digit run that passes the Luhn check. Class two is a `key=value` line or a `[key]: [value]` line whose key is `persist.sys.miui.sno`, `ro.ril.miui.imei0` or `ro.ril.miui.imei1`. Class three is a `ro.serialno` or `ro.boot.serialno` property whose value is anything other than `dc27e5d0`; a fixture carrying `dc27e5d0` must pass. Fixtures are built at test time from synthetic digits and are never committed. The notes may name these properties but never carry their values. A hit aborts the run and redacts nothing. The allowlist command stays a count.
  - Output: a probe that fails closed, with one passing refusal per pattern class, demonstrated on the host.

- F10.1-03 — Re-measure services and labels
  - Description: After `VAL-101-MANUAL`, run PRB7 and PRB8 on `dc27e5d0`. Record running names, rc-defined names, process labels, and the labels of the HAL file, the sensor file and both parent directories. Do not stop or start a service. Compare the labels to the four `chcon` sites without changing them.
  - Output: scanned temp transcripts for PRB7 and PRB8.

- F10.1-04 — Re-measure manager, count and mounts
  - Description: Run PRB1 through PRB6. Record the manager package and versionCode, the `ksu://webui` handler, whether `.ui.webui.WebUIActivity` resolves, the `su` context, the allowlist hit count, metamodule presence, the two-component mount summary and the KSU-sourced mount count. If a root dialog appears, stop. Do not accept it from the host.
  - Output: scanned temp transcripts for PRB1 through PRB6.

- F10.1-05 — Write the dated notes first
  - Description: `docs/hyperos4-adaptation-notes.md` gives every fact its measurement date, copies no preference value, and labels both the idle-service wake-up and the upstream URI reading as inference. It states the order later plans must keep, using the names just measured: stop the client before the HAL, and start the HAL before the client.
  - Output: `docs/hyperos4-adaptation-notes.md`, written before `Faz10.2`, `Faz10.3` or `Faz10.4` starts.

- F10.1-06 — Amend invariant 3
  - Description: In `Project-Ontology.md` item 3, keep the AOSPA black-preview history and add the HyperOS 4 service names with the new measurement date. State the start half as HAL before client. Add one dated pointer that covers every place still naming only `vendor.camera-provider-2-7-ext`: section 5 step 2, section 5's final step, and the camera-framework bullet in section 6. The pointer marks those names as AOSPA history and directs readers to item 3 for the HyperOS 4 set.
  - Output: updated invariant 3 and one dated pointer in `Planner-docs/Project-Ontology.md`.

- F10.1-07 — Append HyperOS 4 evidence rows
  - Description: After the last evidence row, `EV-45` when read on 2026-11-16, append dated rows for the service set, the file labels, the manager and the mount summary. Leave `EV-12` as AOSPA history. Do not mark `ARC-12` resolved; labels are not a policy module.
  - Output: new rows in `Planner-docs/Project-Comprehension.md`.

- F10.1-08 — Store one new snapshot and stop
  - Description: After the identity scan passes, copy the scanned transcript to a new file named with the UTC minute and `__Faz10.1__probe`, and only then delete the `%TEMP%` file. On an aborting hit, delete the `%TEMP%` file without copying anything. Do not modify the two IMPL96 HyperOS snapshot files. Do not run PRB9 or PRB10 for this record; those answers belong to `Faz10.3` and `Faz10.4`, and the strings stay in the frozen table so the list cannot drift.
  - Output: one new snapshot file, and no other device action.

## 8. Acceptance Criteria

- The probe command table equals the ten PRB strings, and every device process starts with `platform-tools/adb.exe` and `-s dc27e5d0`.
- An eleventh command is refused on the host before adb starts.
- Identity-shaped output is rejected before a person reads it, and the allowlist appears only as a count.
- The notes name every running camera service and every rc-defined camera service from the new run, each with a date.
- The notes name the HAL and sensor labels from the new run and set them beside the four `chcon` sites.
- The notes name the manager package, the WebUI handler, the allowlist count, metamodule presence and the mount summary.
- Inferences in the notes are marked as inferences, including the idle-provider wake-up and the upstream URI reading.
- Invariant 3 contains the measured HyperOS 4 names and both halves of the restart order.
- Comprehension has the new dated rows, and `EV-12` is still described as AOSPA evidence.
- No service was stopped, no package was installed, no preference file was written, and the two IMPL96 snapshot files are byte-unchanged.

## 9. Validation and Test Approach

Validation is a host refusal check plus one live read. The live half repeats the fixed command class. It does not interpret a mode switch, because no mode is switched.

- `VAL-101-PROBE` (proposed) — the probe runs only the fixed PRB strings, via `subprocess.run`, with `platform-tools/adb.exe -s dc27e5d0` and `ANDROID_SERIAL=dc27e5d0`, and it stops for the user if a manager other than `com.sukisu.ultra` appears.
- `VAL-101-IDENTITY` (proposed) — each `%TEMP%` transcript is scanned before it is read for Luhn-valid 15-digit runs, the three identity keys in `key=value` or `[key]: [value]` form, and serial properties whose value is not `dc27e5d0`. One planted fixture per class must abort the run, and a hit aborts instead of redacting.
- `VAL-101-NOTES` (proposed) — the adaptation notes date every fact and mark every inference.
- `VAL-101-ONTO` (proposed) — invariant 3 names the measured HyperOS 4 services and keeps stop-client-before-HAL, start-HAL-before-client; the dated pointer covers section 5 and section 6.
- `VAL-101-COMP` (proposed) — Comprehension gains dated HyperOS 4 rows and does not restyle `EV-12` as a new measurement.
- `VAL-101-MANUAL` (proposed) — the user confirms the attached phone is `dc27e5d0`, approves the read-only run, and handles any root dialog. The host does not click through it.

Local versus live: the eleventh-command refusal and the three planted-fixture refusals are local. PRB1 through PRB8 are live and read-only. Security validation is the pinned serial and the identity scan, not a credential check. Ontology validation is the invariant 3 wording. Artifact validation is the notes file plus the new snapshot name.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/hyperos4-probe.py | proposed | Runs the fixed PRB subset and refuses anything else before adb starts. | VAL-101-PROBE, VAL-101-IDENTITY |
| docs/hyperos4-adaptation-notes.md | proposed | Dated HyperOS 4 service, label, allowlist-count, manager and mount record, with inferences marked. | VAL-101-NOTES, VAL-101-MANUAL |
| snapshots/YYYYMMDD-HHMM__Faz10.1__probe.txt | generated | New scanned transcript from this run; the minute is the UTC of the run, and no older snapshot is edited. | VAL-101-IDENTITY, VAL-101-PROBE |
| ishtar-cam-modes/setmode.sh | existing | Read-only evidence of the AOSPA stop and start names this survey compares. | VAL-101-NOTES |
| ishtar-cam-modes/post-fs-data.sh | existing | Read-only evidence of the sensor `chcon` and of the HAL fail-closed exit. | VAL-101-NOTES |
| ishtar-cam-modes/halpatch.sh | existing | Read-only evidence of the HAL-file `chcon` label the survey compares. | VAL-101-NOTES |
| ishtar-cam-modes/action.sh | existing | Read-only evidence that the allowlist is counted, not dumped. | VAL-101-IDENTITY |
| ishtar-cam-modes/webroot/index.html | existing | Read-only evidence of the `ksu.exec`, `ksu.toast` and `ksu.enableEdgeToEdge` call sites. | VAL-101-NOTES |
| ishtar-aon-fix/post-fs-data.sh | existing | Read-only evidence of the AON module's `chcon` label, not a behaviour test. | VAL-101-NOTES |
| scripts/smoke.sh | existing | Read-only: bracket tool for later plans; this survey does not extend it and does not use it as the probe. | VAL-101-PROBE |
| snapshots/20261113-1819__IMPL96__hyperos4-readonly-probe.txt | existing | Read-only 2026-11-13 probe transcript; not rewritten. | VAL-101-NOTES |
| snapshots/20261113-1821__IMPL96__hyperos4-smoke-baseline.txt | existing | Read-only 2026-11-13 smoke baseline; not rewritten. | VAL-101-NOTES |
| Planner-docs/Project-Ontology.md | modified | Invariant 3 gains the measured HyperOS 4 service names and the start-HAL-before-client half; one dated pointer marks the section 5 and 6 provider names as AOSPA history. | VAL-101-ONTO |
| Planner-docs/Project-Comprehension.md | modified | Appends dated HyperOS 4 facts and leaves `EV-12` as AOSPA history. | VAL-101-COMP |

## 10. Dependencies and Sequencing

Depends on: none. This survey is the first Phase 10 sub-plan. It reads the tree and the phone. It does not wait on a module install.

Blocks `Faz10.2`, `Faz10.3` and `Faz10.4` until the notes exist. `Faz10.5` is blocked only through those three, not by a direct file dependency.

Required decisions: none for the survey itself. `DEC-33` stays closed; choosing to reopen the HAL layer is not this plan's call. The user is not asked to pick a service name. Whether a metamodule should be installed is recorded as a question for `Faz10.4`, not answered here.

Required credentials: none. No keystore, token or account is read.

Required infrastructure: the Windows host, `platform-tools/adb.exe` in the tree, USB access to `dc27e5d0`, and SukiSU `su` for PRB4, PRB5 and PRB6. A missing phone stops the live half. It does not authorize a different serial.

Required human approvals: the user confirms the attached phone is `dc27e5d0` and approves the read-only PRB1-PRB8 run (`VAL-101-MANUAL`). If a root dialog appears, the user decides it. If a manager other than `com.sukisu.ultra` appears, the user decides how PRB3 proceeds. No install, mode switch, shutter or permission grant beyond that dialog is in this plan.

Fresh session token and context risk: medium. The script is short, but a wrong service name is what `Faz10.2` would restart, so the notes are the checkpoint rather than a disposable log.

Subagents are not recommended. One adb serial is a single transport, and a second probe would interleave the same read.

## 11. Risks and Mitigations

- Risk: the probe gains a convenience flag that shells out. Impact: a write or an `am start` runs during a survey that was supposed to be read-only. Mitigation: `F10.1-02` and `VAL-101-PROBE` reject any command that is not one of the ten.
- Risk: a temp file is opened before the scan. Impact: an identity-shaped value reaches the notes or the new snapshot. Mitigation: `VAL-101-IDENTITY` is the only reader, each of its three pattern classes has a fixture that must abort, and the `%TEMP%` file is deleted after the snapshot copy, or with no copy when the scan aborts.
- Risk: the 2026-11-15 13:01Z rows are copied forward with no new run. Impact: `Faz10.2` restarts a service set that has changed since that afternoon. Mitigation: `F10.1-03` and `F10.1-04` supply the dates in the notes; the older rows stay prior evidence.
- Risk (inference treated as fact): the idle `vendor.camera-provider-2-7-ext` is described as a service this plan started. Impact: a later plan treats the wake-up as already measured. Mitigation: `F10.1-05` labels that sentence an inference and does not stop or start the service.
- Risk (invariant 3): a later editor copies section 5's shorter start list into a restart. Impact: the client can come up before the HAL, which is not the order `setmode.sh:79-83` uses. Mitigation: `F10.1-06` writes the measured names and the HAL-before-client start into item 3, and its dated pointer covers sections 5 and 6.
- Risk: `su` draws a dialog the 2026-11-15 pass did not draw. Impact: the run stalls, or root is granted for a command the user has not seen. Mitigation: `VAL-101-MANUAL` stops on a dialog. The earlier dialog-free pass is history, not a promise.
- Risk (`DEC-14`, `DEC-33`): a survey sentence is read as leave to enable 50 MP. Impact: HAL work reopens with no new evidence, or AGC is pointed at 50 MP again. Mitigation: the notes say the HAL layer stays off and that this survey did not narrow the wide RAW table or touch the DCG/LN exclusion.

## 12. Desired End State

The repository holds one notes file that names the HyperOS 4 camera services, the labels the module's `chcon` calls would meet, the allowlist count, the SukiSU-Ultra manager, the WebUI handler, and the mount and metamodule facts. Each fact has a date. No module script has been edited. The phone has not had a service stopped or a package installed by this plan.

The evidence an implementer should produce is the notes file, the host refusal log, the diff of invariant 3, the new Comprehension rows, and one new snapshot whose name contains `Faz10.1`.

The ledger summary Step 4 should append records: survey complete on `dc27e5d0`, no device write, `DEC-33` unchanged, the measurement dates, and the idle-provider wake-up still marked as an inference.

## 13. Next Sub-Phase Transition Criteria

- The probe refuses an eleventh command on the host.
- PRB1 through PRB8 have run on `dc27e5d0` under `VAL-101-MANUAL`, or the run stopped on a dialog and no notes were promoted.
- `docs/hyperos4-adaptation-notes.md` exists, dates every fact, and marks inferences as inferences.
- Invariant 3 names the measured services and both halves of the restart order.
- Comprehension carries the new rows and still treats `EV-12` as AOSPA evidence.
- `Faz10.2`, `Faz10.3` and `Faz10.4` may start from that record. `Faz10.5` still waits on those three.
