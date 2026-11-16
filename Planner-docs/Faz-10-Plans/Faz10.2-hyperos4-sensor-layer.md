# Faz 10.2 — HyperOS 4 Sensor Layer

## 1. Context

Main-Planing Phase 10 (`SNAP-2026-11-15-MAIN`) is the HyperOS 4 adaptation added by planning run 21. The phase goal is to measure that camera stack, then move the sensor layer, the trap cleanup, and the tile and WebUI onto it, and only then cut v2.3. This sub-plan, written in that run's Step 2 on 2026-11-16, owns the sensor-layer slice: an unchanged v2.2 install observed inside a smoke bracket, then a `setmode.sh` retarget so restarts follow the services HyperOS 4 actually runs. The acceptance slice is the phase signal for this layer: sensor guard passes, every mode except `50mp` switches and survives reboot, 1080p60 and 4K60 stay usable, and the HAL guard fails closed.

`Faz10.1` is the measurement this plan consumes. It does not install the module and it does not edit `setmode.sh`. `Faz10.3` and `Faz10.4` share that same upstream and do not wait on this plan. `Faz10.5` does: it cannot stamp v2.3 over a restart list that still names an idle AOSPA provider. The gap left after the 2026-11-13 and 2026-11-15 read-only checks is that no project module has been booted on this ROM, so the guard outcome and the restart side effect are still code readings.

Those readings are `W3F20`, `W3F22`, `W3P02`, `W3P03`, Ek A.2 `D4`, `D5`, and `M1`. `D4` and `D5` were measured on 2026-11-13. `W3P02` and `W3P03` were measured on 2026-11-15 at 13:01Z. `M1` is an inference from the scripts plus that probe, not a boot with the module present. `DEC-33` (K9 = no) is named here even though the ledger row is written later: the 50 MP HAL layer stays off on HyperOS 4, and the sensor layer continues.

AOSPA Android 15 results, including a working `50mp` path against `HAL_STOCK_MD5`, are history. They are not treated as HyperOS 4 evidence. The phone in this plan is `dc27e5d0` only.

## 2. Goal

Prove the unchanged v2.2 sensor layer on HyperOS 4 inside a smoke bracket, then change `setmode.sh` so its restart set matches the measured services and so `50mp` is refused by the engine.

## 3. Description

The problem is a restart list that still stops and starts `vendor.camera-provider-2-7-ext`. On the 2026-11-15 probe that name is defined and not running, while `vendor.camera-provider-2-7-ext-uvc` is the provider that is running. Starting the idle name would create a service the ROM had left stopped. Separately, `setmode.sh` still accepts `50mp`, writes that token into the mode file, and asks the HAL layer for `fullres`, even though the HyperOS HAL is not the binary the patch table is locked to.

It belongs in Phase 10 because the sensor layer is the first change after the read-only survey, and because a wrong restart order blacks preview in every mode, stock included. Doing the service edit before the unchanged v2.2 boot would mix a script change with the first install, so a failed guard could not be attributed.

The vibecoding slice strategy: install published v2.2 with no script edit, reboot, and read whether the sensor bind landed and whether the HAL guard logged its mismatch exit. That pair is the fastest validation signal. Only after it is recorded does `restart_camera` gain the UVC provider and lose the start of the idle ext provider, and only then does `50mp` get an engine refusal that runs before the mode file is written.

What should not be over-planned: a second HAL patch table, a product-string detector, a smoke-field addition, or a version bump. The fail-closed comparison already exists. The service names come from `Faz10.1`'s record, checked against the 2026-11-15 probe, not from a new taxonomy of init services.

The nine sensor modes stay one file and one bind. `50mp` remains the name of the HAL-layer request, and `fullres` remains the HAL state. On this ROM the request is rejected, so the exclusion between `50mp` and DCG or LN is preserved by never entering that request, not by stacking both layers.

Device steps stay inside a before-and-after pair from `scripts/smoke.sh`. Installing, rebooting, opening the camera, pressing the shutter, and recording video are the user's hands. While unchanged v2.2 is installed, nothing switches modes: the old restart would start the idle provider, so the Action button, the WebUI, and `setmode.sh` all stay unused until the edited script is live. The implementer does not click through a permission dialog and does not treat an AOSPA video note as a substitute for a HyperOS 4 recording.

## 4. Scope

- Unchanged v2.2 installed by the user on `dc27e5d0`, bracketed by `scripts/smoke.sh`, with no script edit in that first package and no mode switch while it is installed.
- Boot log evidence that the sensor guard accepts the wide IMX989 module and bind-mounts it.
- Boot log evidence that the HAL guard exits on checksum mismatch and does not bind `camera.qcom.so`.
- `ishtar-cam-modes/setmode.sh` `restart_camera` retargeted to the HyperOS 4 running set: `cameraserver`, `vendor.camera-provider`, and `vendor.camera-provider-2-7-ext-uvc`.
- Stop order kept as client then providers, and start order kept as providers then client.
- No `start` of `vendor.camera-provider-2-7-ext` after the edit.
- Engine refusal of `50mp` when the live HAL checksum is neither `HAL_STOCK_MD5` nor `HAL_FULLRES_MD5`, issued before the mode file is written, with no service restart on that refusal.
- A test package of the edited module built into `%TEMP%`, outside the repository, so the published archive and the release manifest stay untouched.
- Sensor modes other than `50mp` switching, persisting across a reboot, and leaving 1080p60 and 4K60 recordable.
- New snapshot files named with `Faz10.2`, without rewriting any snapshot already in the tree.

## 5. Out of Scope

- The read-only service, label, allowlist-count, and WebUI survey. That is `Faz10.1`.
- Removing `50mp` from the tile, the action button, or `webroot/index.html`. That is `Faz10.4`. This plan only makes the engine reject the request those surfaces can still send.
- AGC trap cleanup, preference edits, and any `.agc` import. That is `Faz10.3`. This plan does not write `pref_camera_picturesize_back_key` and does not run `sed -i` on a preference file.
- The v2.3 version strings, `module.prop`, the `customize.sh` version line, `Kullanim.txt`, the release zip, and `docs/release-manifest.md`. That is `Faz10.5`.
- Re-deriving or narrowing the wide RAW patch table, copying `camera.qcom.so` into the tree, or pointing `HAL_STOCK_MD5` at the HyperOS binary. `DEC-33` keeps that layer off. `DEC-14` still bars 50 MP inside AGC without new evidence, and this plan does not generate that evidence.
- Any change that lets `50mp` and a DCG or LN mode be active together; the two layers stay mutually exclusive, exactly as `setmode.sh` maps them today.
- Deciding whether `ishtar-aon-fix` stays installed on HyperOS 4. That is `Faz10.5`.
- Ontology and comprehension edits. If the restart sentence still names only the AOSPA ext provider after `Faz10.1`, that sentence stays with `Faz10.1`'s ontology ownership.

## 6. Current Repository Evidence

`ishtar-cam-modes/setmode.sh` was read in this Step 2 run. `restart_camera` stops `cameraserver`, then `vendor.camera-provider` and `vendor.camera-provider-2-7-ext` (`setmode.sh:52-58`), force-stops the camera packages, and starts the two providers before `cameraserver` (`setmode.sh:79-83`). `wait_svc` treats any `init.svc` value other than `running` as already stopped (`setmode.sh:109-120`), so a misspelled provider name would satisfy a stopped-wait immediately. The mode file is written at `setmode.sh:204`, after the `50mp` arm has already chosen `HAL_WANT=fullres` (`setmode.sh:179-183`). `chcon` on the active sensor file is `u:object_r:vendor_file:s0` (`setmode.sh:256`). The installed path is `/data/adb/modules/ishtar_cam_modes/setmode.sh` (`setmode.sh:14`).

`ishtar-cam-modes/post-fs-data.sh` was read in this Step 2 run. `EXPECT_MD5` and `EXPECT_SIZE` are `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` and `1062250` (`post-fs-data.sh:8-9`). A matching wide module is bind-mounted at `post-fs-data.sh:72`. The HAL checksum test is `post-fs-data.sh:101-107`: mismatch logs `DURDU(HAL)` and exits before `hal_seed` and before the HAL bind at `post-fs-data.sh:127`. Sensor mount therefore does not depend on the HAL guard passing. A stored mode of `50mp` still selects a stock sensor blob and `HAL_WANT=fullres` (`post-fs-data.sh:16-19`), which is why an engine refusal has to happen before that token is stored.

`ishtar-cam-modes/customize.sh` was read in this Step 2 run. Install aborts when the wide-module checksum mismatches (`customize.sh:14`, `customize.sh:20-28`). A HAL checksum other than `HAL_STOCK` or `HAL_FULLRES` is printed as a warning and does not abort (`customize.sh:36-50`), so an unchanged v2.2 install is expected to finish on HyperOS 4 with 50 MP marked unusable and the sensor modes still offered. Both of those checksums are accepted there, which is why the refusal in this plan accepts both as well.

`ishtar-cam-modes/halpatch.sh` was read in this Step 2 run. `HAL_STOCK_MD5`, `HAL_FULLRES_MD5`, and `HAL_SIZE` at `halpatch.sh:32-34` are the AOSPA lock (`HAL_SIZE=27268688`). `hal_seed` returns failure unless the live file matches `HAL_STOCK_MD5`, and the copy it labels uses `u:object_r:vendor_file:s0` (`halpatch.sh:114`). Changing those constants to the HyperOS file would make the guard pass on a binary the patch offsets were not measured against.

`ishtar-cam-modes/action.sh` was read in this Step 2 run for the switch path only. The Action button cycle runs `setmode.sh` in the background (`action.sh:132`) and steps `dcgB` to `ln4f` to `50mp` (`action.sh:152-154`). Once the engine refuses `50mp`, that cycle stops advancing at `ln4f` until `Faz10.4` changes it, so this plan does not use the Action button for its switches.

`scripts/build-release.py` was read in this Step 2 run. Without flags it writes `dist/ishtar-cam-modes-<version>.zip` and rewrites `docs/release-manifest.md` (`build-release.py:12`, `build-release.py:371-374`). With no version bump, a default run would overwrite the published v2.2 archive. `--out` and `--manifest` redirect both outputs.

`scripts/smoke.sh` was read in this Step 2 run. It is read-only, selects `platform-tools/adb.exe` when that file is executable, and does not pass `-s` itself (`smoke.sh:33-34`). Layer constants are grepped from the installed module (`smoke.sh:52-65`), so a snapshot taken before install hashes empty input for those fields and must not be read as a sensor mismatch. The comparable region is the block marked at `smoke.sh:275-278`, and `-o` appends `.txt` to the stored name. `ANDROID_SERIAL=dc27e5d0` is how this plan pins the device without editing the script.

Ek A.2 `D5`, measured 2026-11-13, says the HyperOS wide module matches `EXPECT_MD5` and `EXPECT_SIZE`. `D4`, same day, says `/odm/lib64/hw/camera.qcom.so` is a different checksum and a different size from the AOSPA stock HAL. `W3P03`, 2026-11-15 13:01Z, measured the running set as `cameraserver`, `vendor.camera-provider`, and `vendor.camera-provider-2-7-ext-uvc`, with `vendor.camera-provider-2-7-ext` defined and not running, and both the HAL file and the sensor file labelled `vendor_file`. The claim that today's `setmode.sh` would start the idle service is an inference (`W3P03`, `M1`), not a measured start. `W3P02`, same window, counted `com.ishtar.cammodes` as 0 on the allowlist and found no metamodule. Module absence was observed on 2026-11-13; this plan re-reads it from its own pre-v22 snapshot, where `module.version` and `mode.file` are empty, rather than from any `Faz10.1` record.

## 7. Planned Work Breakdown

- F10.2-01 — Confirm the Faz 10.1 service record before editing
  - Description: Read the `Faz10.1` record and accept the edit only if it still shows `vendor.camera-provider-2-7-ext-uvc` running, `vendor.camera-provider-2-7-ext` not running, and both camera files labelled `vendor_file`. If that record disagrees with the 2026-11-15 13:01Z probe, stop. Do not invent a third service list.
  - Output: a go or stop note citing the `Faz10.1` record and the 2026-11-15 probe.
- F10.2-02 — Bracket the phone before the unchanged install
  - Description: With `ANDROID_SERIAL=dc27e5d0`, run `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.2__pre-v22`. Empty `module.version` and `mode.file` confirm the module is absent. Treat empty sensor and HAL hashes as that absence, which is what `smoke.sh:52-65` produces, not as a failed guard. Do not install, mount, or restart anything in this step.
  - Output: `snapshots/YYYYMMDD-HHMM__Faz10.2__pre-v22.txt`.
- F10.2-03 — Have the user install published v2.2 and reboot
  - Description: First compare the md5 of `dist/ishtar-cam-modes-v2.2.zip` with the `REL` row of Ek A.2; stop on a mismatch. The user then installs that archive and reboots. The implementer does not flash, does not confirm a permission dialog, and does not rebuild that zip. `customize.sh` is expected to abort only on a sensor mismatch and to warn, not abort, on the HAL. From install until the edited script is live, nobody presses the Action button, opens the module WebUI, or calls `setmode.sh`.
  - Output: the md5 match note, the user's install result, and the post-reboot module directory.
- F10.2-04 — Read the sensor pass and the HAL closed exit
  - Description: After the user's reboot, capture the module log lines for the sensor bind and for `DURDU(HAL)` from `post-fs-data.sh:101-107`. Confirm no HAL bind at `post-fs-data.sh:127`. Then take `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.2__post-v22`; its `mode.file` must read `stock`. If a switch happened anyway, record `init.svc.vendor.camera-provider-2-7-ext` and have the user reboot before going on. A sensor-guard failure stops the sub-plan. A HAL guard that does not fail closed also stops it: that would contradict `D4` and must not be "fixed" by retargeting `HAL_STOCK_MD5`.
  - Output: the log excerpt and `snapshots/YYYYMMDD-HHMM__Faz10.2__post-v22.txt`.
- F10.2-05 — Retarget restart_camera to the measured running set
  - Description: In `setmode.sh` only, stop `cameraserver` before the providers, and start providers before `cameraserver`. The providers that are started are `vendor.camera-provider` and `vendor.camera-provider-2-7-ext-uvc`. `vendor.camera-provider-2-7-ext` may be stopped if a stray start left it running, and it is never started. Wait for `running` on the UVC provider as well as on `vendor.camera-provider` and `cameraserver`. Do not trust a stopped-wait alone, because `wait_svc` succeeds when the property is empty.
  - Output: the edited `restart_camera` in `ishtar-cam-modes/setmode.sh`.
- F10.2-06 — Refuse 50mp before the mode file is written
  - Description: When the argument is `50mp` and the live HAL checksum is neither `HAL_STOCK_MD5` nor `HAL_FULLRES_MD5`, exit non-zero before `setmode.sh:204`. Do not write the mode file, do not call `hal_set`, and do not restart services. An AOSPA phone whose HAL is stock or already carries the patched copy still reaches the existing `50mp` arm, so this refusal is the HyperOS mismatch gate and not a deletion of the AOSPA path. Do not change `halpatch.sh`.
  - Output: the refusal branch in `ishtar-cam-modes/setmode.sh`.
- F10.2-07 — Install the edited script, reboot, then switch modes
  - Description: In Git Bash, the shell `scripts/smoke.sh` already needs and where `$TEMP` is the Windows temp folder, build the test package with `py -3 scripts/build-release.py --out "$TEMP/ishtar-cam-modes-v2.2-faz102.zip" --manifest "$TEMP/ishtar-cam-modes-v2.2-faz102.md"`, so neither `dist/ishtar-cam-modes-v2.2.zip` nor `docs/release-manifest.md` is overwritten. Both output paths must resolve outside the repository, and `git status` must show no new file after the build. Take `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.2__pre-edit`. The user installs the temp package and reboots before any switch: KernelSU-family managers stage a module update until the next boot, so a switch before that reboot would still run the old script (an inference, not observed on `dc27e5d0`). After the reboot, the md5 of `/data/adb/modules/ishtar_cam_modes/setmode.sh` must equal the edited host file; stop otherwise. Each switch then uses `platform-tools/adb.exe -s dc27e5d0 shell su -c 'sh /data/adb/modules/ishtar_cam_modes/setmode.sh <mode>'`, never the Action button. Cycle through `stock`, `ln2`, `ln4`, `ln2s`, `ln4s`, `ln2f`, `ln4f`, `dcgA`, and `dcgB`, and request `50mp` once. The user reboots again, opens the camera, and records 1080p60 and 4K60. Then take `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.2__post-reboot`. No preference file is written. The temp package is not copied into `dist/` or committed.
  - Output: the live-script md5 match, mode-switch log, refusal log, `snapshots/YYYYMMDD-HHMM__Faz10.2__pre-edit.txt`, `snapshots/YYYYMMDD-HHMM__Faz10.2__post-reboot.txt`, and the user's video notes.
- F10.2-08 — Diff the brackets and record the service properties
  - Description: Diff only the comparable regions. After one sensor-mode switch on the edited script, record `init.svc.vendor.camera-provider-2-7-ext-uvc` as `running` and `init.svc.vendor.camera-provider-2-7-ext` as not `running`, using `platform-tools/adb.exe -s dc27e5d0`. Attribute every differing smoke line. Do not rewrite older snapshot files.
  - Output: the diff note and the two `init.svc` readings.

## 8. Acceptance Criteria

- The pre-install snapshot exists, shows empty `module.version` and `mode.file`, and its empty layer hashes are explained as module absence, not as a guard failure.
- The md5 of `dist/ishtar-cam-modes-v2.2.zip` matched the `REL` row before the user installed it.
- After the user's unchanged v2.2 reboot, the log shows the sensor bind and the `DURDU(HAL)` exit from `post-fs-data.sh:101-107`, and `hal.mount.count` stays 0.
- The post-v22 snapshot shows `mode.file` as `stock`, and no mode switch ran while v2.2 was installed.
- `customize.sh` did not abort the unchanged install on the HyperOS HAL checksum.
- The edited package was built into `%TEMP%`; `dist/ishtar-cam-modes-v2.2.zip` and `docs/release-manifest.md` are unchanged.
- The live `setmode.sh` md5 equalled the edited host file before the first switch.
- `setmode.sh` starts `vendor.camera-provider-2-7-ext-uvc` and does not start `vendor.camera-provider-2-7-ext`.
- A mode switch stops `cameraserver` before either provider and starts both running providers before `cameraserver`.
- After that switch, `init.svc.vendor.camera-provider-2-7-ext-uvc` is `running` and `init.svc.vendor.camera-provider-2-7-ext` is not `running`.
- `50mp` exits non-zero, leaves the mode file unchanged, and does not restart the camera stack.
- Each of the nine sensor modes writes its own blob, keeps a single sensor bind, and is still the active variant after reboot.
- The user has opened the camera and recorded 1080p60 and 4K60 on HyperOS 4 after a sensor-mode switch, and those recordings play.
- No preference key was written, no `.agc` file was imported, and no new apk, zip, keystore, or `camera.qcom.so` was added to the repository.
- New snapshot names contain `Faz10.2`, and no pre-existing snapshot file was modified.

## 9. Validation and Test Approach

Validation is a live bracket around two installs: published v2.2 with no edit, then the `setmode.sh` edit only. Host-side work is the archive md5 check, the temp build, the diff of comparable regions, and a check that the tree gained no package file. The service proof is a property read, not the exit code of `wait_svc`.

- `VAL-SMOKE` (from Faz 2.1) — `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.2__pre-v22` with `ANDROID_SERIAL=dc27e5d0`. The script appends `.txt` itself (`smoke.sh:284`). Comparable regions are diffed. The script is left unchanged. Existing snapshot files stay byte-identical. Before any new file is committed, its `# serial` line must read `dc27e5d0` and it must pass `VAL-101-IDENTITY`; the AGC setting values that unmodified smoke output carries (`prefs.trap.*` and the pin keys) are allowed in it.
- `VAL-101-IDENTITY` (from Faz 10.1) — the same identity scan, run here on each new `Faz10.2` snapshot before commit; a hit blocks the commit rather than being redacted in place.
- `VAL-102-BRACKET` (proposed) — the four new files only: `snapshots/YYYYMMDD-HHMM__Faz10.2__pre-v22.txt`, `snapshots/YYYYMMDD-HHMM__Faz10.2__post-v22.txt`, `snapshots/YYYYMMDD-HHMM__Faz10.2__pre-edit.txt`, and `snapshots/YYYYMMDD-HHMM__Faz10.2__post-reboot.txt`, with `mode.file` reading `stock` in post-v22. Each of the four passes `VAL-101-IDENTITY` and carries the `dc27e5d0` serial line before it is committed. Existing snapshot files stay byte-identical.
- `VAL-102-GUARD` (proposed) — archive md5 equal to `REL` before install, sensor bind logged, `DURDU(HAL)` logged from `post-fs-data.sh:101-107`, HAL bind absent.
- `VAL-102-SVC` (proposed) — `platform-tools/adb.exe -s dc27e5d0 shell getprop` on the UVC provider and the idle ext provider after a switch, plus the stop-then-start order in the edited function.
- `VAL-102-REFUSE` (proposed) — `50mp` non-zero exit while the live HAL is neither stock nor fullres, mode file byte-identical, no restart.
- `VAL-102-MODES` (proposed) — live `setmode.sh` md5 equal to the edited host file after the reboot, then the nine sensor modes switched through `platform-tools/adb.exe -s dc27e5d0 shell su -c`, each checked by mode file, live sensor checksum, and mount count, including one post-reboot read.
- `VAL-102-MANUAL` (proposed) — the user approves and performs both installs and every reboot, dismisses any permission dialog, approves each mode switch and the single `50mp` request, leaves the Action button and the WebUI unused while v2.2 is installed, opens the camera, presses the shutter, and records 1080p60 and 4K60.

Local versus live: the archive check, the temp build, and the snapshot diff are host-side; every guard, service, mode, and video check is live on `dc27e5d0`. Security validation is not applicable: no credential is read, the allowlist is not dumped, and preference values are not copied into the notes. Ontology validation is the restart order in the edited function, not an ontology-file edit.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/setmode.sh | modified | Retarget `restart_camera` to the running HyperOS 4 providers and refuse `50mp` before the mode file is written. | VAL-102-SVC, VAL-102-REFUSE, VAL-102-MODES |
| ishtar-cam-modes/post-fs-data.sh | existing | Read-only: sensor bind at `:72` and the mismatch exit at `:101-107` are observed, not rewritten. | VAL-102-GUARD |
| ishtar-cam-modes/halpatch.sh | existing | Read-only: `HAL_STOCK_MD5` and `HAL_FULLRES_MD5` stay the AOSPA lock so the HyperOS HAL is not patched. | VAL-102-REFUSE |
| ishtar-cam-modes/customize.sh | existing | Read-only evidence of the install abort on sensor mismatch and the non-abort HAL warning; version line stays for `Faz10.5`. | VAL-102-GUARD, VAL-102-MANUAL |
| scripts/smoke.sh | existing | Bracket reporter, not extended: empty pre-install layer fields are expected, and service proof is `getprop` rather than a new comparable line. | VAL-SMOKE, VAL-102-BRACKET |
| scripts/build-release.py | existing | Read-only use with `--out` and `--manifest` pointed at `%TEMP%`; not written here, owned by `Faz10.5`. | VAL-102-MODES |
| docs/release-manifest.md | existing | Not written here: the temp build sends its manifest to `%TEMP%`; owned by `Faz10.5`. | VAL-102-MODES |
| ishtar-cam-modes/action.sh | existing | Still able to request `50mp` until `Faz10.4`; the engine refusal has to cover that call, and its cycle is not used for this plan's switches. | VAL-102-REFUSE, VAL-102-MANUAL |
| ishtar-cam-modes/service.sh | existing | Read-only: it does not restart the camera stack, so the service edit is not split into this file. | VAL-102-SVC |
| ishtar-cam-modes/webroot/index.html | existing | Still offers `50mp`; removing that control is `Faz10.4`, not a write here, and it stays unused while v2.2 is installed. | VAL-102-REFUSE, VAL-102-MANUAL |
| ishtar-cam-modes/module.prop | existing | Version remains v2.2; the v2.3 bump belongs to `Faz10.5`. | VAL-102-MANUAL |
| dist/ishtar-cam-modes-v2.2.zip | existing | The already-built archive, md5-checked against `REL`, that the user installs for the unchanged observation; this sub-plan does not rebuild or overwrite it. | VAL-102-MANUAL, VAL-102-GUARD |
| snapshots/YYYYMMDD-HHMM__Faz10.2__pre-v22.txt | generated | New smoke file before the unchanged v2.2 install, showing module absence. Existing snapshot files stay byte-identical. | VAL-SMOKE, VAL-102-BRACKET, VAL-101-IDENTITY |
| snapshots/YYYYMMDD-HHMM__Faz10.2__post-v22.txt | generated | New smoke file after the unchanged v2.2 reboot, for the guard reading and `mode.file` at `stock`. | VAL-SMOKE, VAL-102-GUARD, VAL-101-IDENTITY |
| snapshots/YYYYMMDD-HHMM__Faz10.2__pre-edit.txt | generated | New smoke file before the edited `setmode.sh` is installed. | VAL-SMOKE, VAL-102-BRACKET, VAL-101-IDENTITY |
| snapshots/YYYYMMDD-HHMM__Faz10.2__post-reboot.txt | generated | New smoke file after the sensor-mode switches and the reboot. | VAL-SMOKE, VAL-102-MODES, VAL-101-IDENTITY |

## 10. Dependencies and Sequencing

Depends on `Faz10.1` for the written HyperOS 4 service names and file labels. The 2026-11-15 probe is the prior measurement that record must agree with; it is not a substitute for the record. Module absence is not taken from `Faz10.1`; this plan reads it from its own pre-v22 snapshot.

Depends on `Faz2.1` for `scripts/smoke.sh`, already verified, used here only as the bracket and not extended.

Blocks `Faz10.5`. The v2.3 stamp waits until this restart set and the engine refusal are in the tree the release packages. `Faz10.3` and `Faz10.4` are not blocked.

Required decisions: none new. `DEC-33` already keeps the 50 MP HAL layer off; this plan does not reopen it. A `Faz10.1` record that disagrees with the 2026-11-15 service set is a stop, not a decision the implementer takes alone.

Required credentials: none. No account, keystore, or preference value is required.

Required infrastructure: `dc27e5d0` attached, `platform-tools/adb.exe` present, a writable `%TEMP%` for the test build, and `ANDROID_SERIAL=dc27e5d0` set for every `scripts/smoke.sh` run. Commands that name the device themselves use `platform-tools/adb.exe -s dc27e5d0`.

Required human approvals: `VAL-102-MANUAL` — the user approves and performs both installs and every reboot, any permission dialog, each of the nine mode switches and the single `50mp` request, the camera open, the shutter, and the 1080p60 and 4K60 recordings. While v2.2 is installed, the user leaves the Action button and the WebUI alone. The implementer does not perform those acts.

Fresh session token and context risk: medium. The script edit is small, but a restart that starts the idle provider or that reverses client and HAL can blacken preview until reboot, so the session has to keep the bracket pair and the service readings in view.

Subagents are not recommended. The device is one stateful camera stack, and a second writer installing or restarting beside the bracket would make the diff unattributable.

## 11. Risks and Mitigations

- Risk: `restart_camera` starts `vendor.camera-provider-2-7-ext` because that is the name in the current function. Impact: an init service the 2026-11-15 probe left stopped becomes running, which is a device-state change outside the sensor layer. Mitigation: `F10.2-05` removes that `start`, and `VAL-102-SVC` reads the property after a switch.
- Risk: someone switches a mode through the Action button, the WebUI, or `setmode.sh` while unchanged v2.2 is installed. Impact: the old restart starts the idle provider before the guard reading is taken. Mitigation: `F10.2-03` forbids all three until the edited script is live, `VAL-102-BRACKET` requires `mode.file` at `stock` in post-v22, and a stray switch is recorded and followed by a reboot.
- Risk: mode switches run between installing the edited package and its reboot. Impact: the staged update has not replaced the live script yet (an inference, not observed on `dc27e5d0`), so the old restart runs and `VAL-102-SVC` tests the wrong file. Mitigation: `F10.2-07` reboots first and compares the live `setmode.sh` md5 with the edited host file before any switch.
- Risk: stop and start are reordered while the service names are edited. Impact: a live stream dies with the provider, the kernel can keep CSIPHY and CSID allocations, and preview goes black in every mode until reboot. Mitigation: `F10.2-05` keeps client-before-providers on the way down and providers-before-client on the way up, and `VAL-102-SVC` checks that order in the edited function.
- Risk (`M1` residual): the unchanged v2.2 boot is still an inference until `F10.2-04` reads the log. Impact: a sensor mismatch or an unexpected HAL match would be discovered only after a later edit had been mixed in. Mitigation: `F10.2-03` installs published v2.2 with no script change, and a guard miss stops the sub-plan before `F10.2-05`.
- Risk: `50mp` is written to the mode file by the tile or the WebUI, which `Faz10.4` has not yet changed. Impact: the next boot would still request `fullres` even though the HAL guard then exits. Mitigation: `F10.2-06` refuses before the write, so those surfaces get a non-zero exit instead of a stored token. UI removal stays in `Faz10.4`.
- Risk: the refusal is keyed to the stock checksum alone. Impact: an AOSPA phone whose HAL already carries the patched copy would lose `50mp`. Mitigation: `F10.2-06` accepts both `HAL_STOCK_MD5` and `HAL_FULLRES_MD5`, matching `customize.sh`.
- Risk: `wait_svc` is treated as proof that the UVC provider returned. Impact: an empty property satisfies a stopped-wait, so a typo looks successful. Mitigation: `VAL-102-SVC` requires `init.svc.vendor.camera-provider-2-7-ext-uvc` to read `running`.
- Risk: the HyperOS HAL checksum is copied into `HAL_STOCK_MD5` so the guard goes green. Impact: AOSPA offsets would be applied to an unmeasured binary, which is the HAL layer `DEC-33` left off. Mitigation: `halpatch.sh` stays unmodified, and `F10.2-04` stops if the guard does not fail closed.
- Risk: the test package is built with the default `build-release.py` outputs. Impact: with no version bump, the published v2.2 archive is overwritten and `docs/release-manifest.md`, which `Faz10.5` owns, is rewritten; invariant 9 is at risk if the zip is committed. Mitigation: `F10.2-07` pins `--out` and `--manifest` to `%TEMP%`, and `dist/ishtar-cam-modes-v2.2.zip` is md5-checked against `REL` before it is installed.
- Risk: AOSPA notes that video survived `50mp` are reused as the HyperOS 4 video result. Impact: 1080p60 or 4K60 could be broken on this ROM and still be marked passed. Mitigation: `VAL-102-MANUAL` requires the user to record both on HyperOS 4 after a sensor-mode switch.

## 12. Desired End State

Unchanged v2.2 has been booted once on HyperOS 4 under a smoke bracket, with no mode switch while it was installed: the sensor guard passed, the HAL guard failed closed, and that pair is on disk. `setmode.sh` then restarts `cameraserver`, `vendor.camera-provider`, and `vendor.camera-provider-2-7-ext-uvc`, never starts `vendor.camera-provider-2-7-ext`, and refuses `50mp` when the live HAL is neither the locked stock checksum nor the patched one. The nine sensor modes persist across reboot. 1080p60 and 4K60 have been recorded on this ROM by the user. No HAL constant, preference file, release manifest, or package artifact was changed.

The evidence an implementer should produce is the `REL` md5 match, the pre-v22 and post-v22 snapshots, the `DURDU(HAL)` excerpt, the edited `restart_camera` and refusal branch, the live-script md5 match, the nine-mode and reboot snapshots, the two `init.svc` readings, the `50mp` refusal transcript, and the user's video notes.

The ledger summary Step 4 should append records: unchanged v2.2 sensor pass and HAL fail-closed on HyperOS 4, dated; `setmode.sh` service set aligned to the `Faz10.1` record; `50mp` refused at the engine under `DEC-33`; snapshot names containing `Faz10.2`.

## 13. Next Sub-Phase Transition Criteria

- `F10.2-04` recorded a sensor bind, a HAL mismatch exit, and `mode.file` at `stock` on the unchanged v2.2 boot.
- `ishtar-cam-modes/setmode.sh` is the only module script this sub-plan modified, and the published archive and release manifest are unchanged.
- `VAL-102-SVC` shows the UVC provider running and the ext provider not running after a switch.
- `VAL-102-REFUSE` shows `50mp` rejected with the mode file unchanged.
- `VAL-102-MODES` and `VAL-102-MANUAL` show the live-script md5 match, the nine sensor modes, reboot persistence, and HyperOS 4 1080p60 and 4K60 recordings.
- `Faz10.5` can package that `setmode.sh`. `Faz10.3` and `Faz10.4` do not wait on this exit.
