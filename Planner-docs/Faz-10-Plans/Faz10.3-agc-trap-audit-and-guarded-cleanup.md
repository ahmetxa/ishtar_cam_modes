# Faz 10.3 — AGC Trap Audit and Guarded Cleanup

## 1. Context

Main-Planing Phase 10 (`SNAP-2026-11-15-MAIN`) adapts the camera module to HyperOS 4. It measures first, then moves the sensor layer, this AGC trap cleanup, and the tile and WebUI chain, and releases v2.3. `DEC-33` keeps the 50 MP HAL layer off; the sensor layer continues elsewhere. This plan owns the AGC signal: no armed trap preference after a cleanup whose backup was checked first, with `pref_camera_picturesize_back_key` unwritten and no `.agc` import.

The trap predates this ROM. `docs/phase3-preconditions.md` section 1, read in this Step 2 run, cites Ontology invariant 8 and `EV-13`: the two key families can break Gcam initialization alone, and an AOSPA isolation was fixed by deleting preferences after a HAL revert and an APK revert had failed. That history explains why a clearance exists. It does not describe the HyperOS 4 file.

This run's finding is a document defect against a measurement already in hand. The only in-repo clearance, `docs/phase3-preconditions.md:71-119`, has no backup, redirects into the live file before the filtered copy is known good, and hard-codes an owner and label. The 2026-11-15 PRB at 13:01Z showed those constants do not match. The backup-first shape that was exercised, `docs/agc-12mp-configuration.md:100-143`, was written for a one-character pin, not for deleting trap lines.

`Faz10.1` supplies the survey record and the camera-service names this plan must not restart, and it confirms the root channel. It does not read the AGC preference attributes; PRB9 belongs to this plan, so the reference owner and label come from W3P04 and from this plan's own pre-write read. `Faz10.2` and `Faz10.4` are siblings, not inputs. `Faz10.5` waits on this bracket. Planning run 21's Step 2 opened this sub-plan on 2026-11-16 so HyperOS 4 has a script that reads attributes on the device, and so the two procedure documents stop offering the AOSPA route as current.

## 2. Goal

Produce a HyperOS 4 AGC trap cleanup that reads the live owner and SELinux label, writes nothing until a checked backup exists, removes only the two trap-key families, and leaves `pref_camera_picturesize_back_key` untouched, with the device write user-approved inside a smoke bracket.

## 3. Description

The problem is a clearance that would be followed on the wrong ROM. It names `u0_a450` and a label containing `c194`, it never saves the file first, and its redirect truncates the live preferences before the filtered copy is checked. On 2026-11-15 the same file was owned by `u0_a478` with `c222` in the label. Following those steps either fails a check that cannot pass, or, if the check is skipped, repeats a truncation that already destroyed this file once on AOSPA.

It belongs in Phase 10 because the phase accepts this slice only as a measurement on HyperOS 4, not as a citation of the AOSPA audit. Sensor work and tile work can run beside it. A v2.3 claim that AGC has no armed trap preference cannot.

The vibecoding slice strategy: the first slice is a host fixture of the new script, with no device attached. An empty filter, a filter that drops a non-trap line, a filter that touches `pref_camera_picturesize_back_key`, a malformed XML result, and a simulated short write must each end with the stand-in live file equal to its backup. That is the fastest validation signal, and it is available before the user approves a write. The second slice corrects the two documents. The live bracket is last.

What should not be over-planned: a general preference editor, a settings UI, a re-pin of `pref_48m_key`, or a SELinux policy. Know which trap keys are armed, remove those two families only, keep the original inode's owner, mode and label, and show the armed count at zero after a plain relaunch.

The pin template's eight-byte size window does not transfer. It fits a one-character substitution. Deleting several trap lines moves the size by more than eight bytes, so copying that window would reject a correct deletion and invite a bypass. The new bound is a line rule: the filtered file is non-empty, no larger than the original, still well-formed, and the only removed lines are trap-family lines.

Keeping the attributes is not proof that the write worked. A `cat` that stops early leaves the same inode, owner and label with half the content, which is the AOSPA truncation in a quieter form. The script therefore compares content after the write, not only attributes, and restores from a device-side backup when the content is wrong.

Presence is not the same as armed. `scripts/smoke.sh` already separates them: `prefs.trap.armed` counts values other than `0` or `false`. The pass condition is that field after a plain relaunch, measured that day. The AOSPA claim that a zero value is inert is not assumed here, so the script deletes the family lines instead of writing a substitute value.

## 4. Scope

- A PRB9-class pre-write read (`ls -ldZ` on the preference directory, `ls -lZ` on the file) whose owner and label must equal the W3P04 values of 2026-11-15T13:01Z, and whose mode is recorded as the reference.
- A backup kept twice, on the host outside the repository and in `/data/local/tmp` on the device, each matching the live file's md5 and byte length before any filter output is pushed.
- `scripts/agc-trap-clean.sh`, removing only `pref_raw_key` and `pref_fix_resolution_key` lines, including numbered suffixes, by writing into the original inode.
- Host-side guards that refuse to push a filtered file that is missing, empty, larger, malformed, or different in any non-trap line.
- A post-write content check, live md5 and byte length against the filtered file, with an automatic, verified restore from the device backup on any mismatch.
- `org.codeaurora.snapcam` held stopped: a force-stop before the backup and again just before the write, with `pidof` empty at backup, write and verification.
- A refusal to write `pref_camera_picturesize_back_key`, `pref_48m_key` or `pref_camera_resolution`.
- A smoke bracket around the approved device write, using existing AGC fields, not a new field.
- Dated corrections in the two owned procedure documents, so the AOSPA table and the backup-less redirect are not the HyperOS 4 route.
- A host-only fixture mode of the same script, so the guards and the restore branch fail closed without adb.

## 5. Out of Scope

- Service names, labels outside this preference file, and the allowlist. That is `Faz10.1`.
- Module install, mode switching, and any edit of `scripts/smoke.sh`. That is `Faz10.2`; the install is the user's.
- The tile, the WebUI chain, and the system-app evaluation. That is `Faz10.4`.
- Version strings, `Kullanim.txt`, and the v2.3 manifest. That is `Faz10.5`.
- Turning the 50 MP HAL layer on. `DEC-33` leaves it off; this script does not patch `camera.qcom.so`.
- Enabling AGC 50 MP. `DEC-14` still requires new evidence; this plan does not write `pref_48m_key`.
- Narrowing the wide RAW table, calling `setmode.sh`, or choosing between `50mp` and the DCG/LN modes.
- Importing `12mpx_agc_config.agc` or `50mpx_agc_config.agc`, or editing either file.
- A direct write of `pref_camera_picturesize_back_key`, `sed -i` on the preference file, or `chmod`/`chcon` toward the AOSPA triple.
- Committing the preference backup, an apk, a zip, a keystore, or `camera.qcom.so`.
- Restarting `cameraserver` or either camera provider. Force-stopping `org.codeaurora.snapcam` is not a HAL restart.

## 6. Current Repository Evidence

`docs/phase3-preconditions.md:71-119` was read in this Step 2 run. The clearance force-stops AGC, filters the two families to `/data/local/tmp/p.xml`, and redirects that temp file onto the live path. Nothing copies the live file aside first, and nothing tests that the temp file is non-empty before the redirect. The table at `:83-85` requires owner `u0_a450`, mode `0660`, and `u:object_r:app_data_file:s0:c194,c257,c512,c768`. The verify line at `:110` expects that triple. The note above the procedure forbids `sed -i` because it replaces the inode; the redirect was the replacement, and it has no backup.

`docs/agc-12mp-configuration.md:100-143` was read in this Step 2 run. It copies the live file to `/data/local/tmp/agc_prefs_backup.xml`, pushes a script, and only then writes. Three guards precede `cat` into the original inode: the temp file must exist and be non-empty, its size must be within eight bytes, and the substitution must be visible. The prose says the redirect truncates the live file before the copy is read, which is why the backup is not optional. Nothing in that template checks the live content after the `cat`. The attribute line just above that section is the AOSPA triple again. Section 6 of that file still says `scripts/smoke.sh` reports trap presence only. That sentence is stale against the fields below; this plan owns the file, and the armed field is the gate, so the correction is in scope.

`scripts/smoke.sh` was read in this Step 2 run at `probe_app`. `prefs.trap.count` and `prefs.trap.keys` name keys that are present. `prefs.trap.armed` counts values other than `0` or `false`. `prefs.trap.values` prints name-value pairs. Adjacent fields report `agc.pref_48m`, `agc.pref_resolution`, and the derived picture sizes, with `absent` when a key is missing. `-o NAME` is stored as `snapshots/NAME.txt`, so the name must not contain `snapshots/`. The script does not report owner, mode or label. `Faz10.2` owns the file; this plan only runs it.

The 2026-11-15 PRB at 13:01Z (W3P04, PRB9) measured `org.codeaurora.snapcam_preferences.xml` as owner `u0_a478` and label `app_data_file:s0:c222,c257,c512,c768`. Trap-key names were in that file. W3P04 does not record mode. Mode `0660` is an AOSPA constant, not a HyperOS 4 measurement, so the new script reads mode before the write and preserves it. W3P04 is the only HyperOS 4 reading of these attributes; the PRB table assigns PRB9 to this plan, and `Faz10.1` does not repeat it. Main-Planing Phase 10's entry evidence states the same mismatch. That bullet summarizes W3P04; it is not a second measurement.

The 2026-11-13 probe (D9) measured versionName `8.4.300.414775575.18`, the unpatched V9.6 package, apk md5 `fa4066eb3bf82cc097906fd108073500`, `prefs.trap.armed` of 10, and `agc.pref_48m` absent. The derived rear size matched the documented 12 MP target, 4096x3072. The armed count on cleanup day is whatever the pre-bracket measures; 10 is not a quota. Preference values from that probe are not copied here.

Two inferences, not device results. The `:99` redirect would still truncate the live file on HyperOS 4 if the temp file were empty, because that ordering is in the text and the pin document records the same ordering zeroing the file on AOSPA (`IMPL-63`). It has not been executed on HyperOS 4. An eight-byte window on a multi-line deletion would fail a correct filter; that follows from the template's own comment that a pin write changes one character, not from a HyperOS trial.

## 7. Planned Work Breakdown

- F10.3-01 — Record the reference attribute triple before any edit
  - Description: In the pre-bracket, run a PRB9-class read on `dc27e5d0`: `ls -ldZ` on the `shared_prefs` directory and `ls -lZ` on `org.codeaurora.snapcam_preferences.xml`. Owner and label must equal W3P04 (`u0_a478`, `c222,c257,c512,c768`). If either differs, stop: the uid or categories moved since 2026-11-15, and there is no stable reference. Mode has no earlier HyperOS 4 reading, so this read sets it. Do not `chown` or `chcon`.
  - Output: A dated reference triple with mode, plus the W3P04 comparison.
- F10.3-02 — Add the backup-first cleanup script
  - Description: Add `scripts/agc-trap-clean.sh`. If the caller set `ANDROID_SERIAL` to anything other than `dc27e5d0`, it exits. It then requires `platform-tools/adb.exe -s dc27e5d0 get-serialno` to print `dc27e5d0` before it exports the variable and makes any other adb call. It force-stops `org.codeaurora.snapcam` and needs `pidof org.codeaurora.snapcam` to be empty. It copies the live file to `/data/local/tmp` on the device and pulls a second copy to the host, outside the repository. Both copies must match the live md5 and byte length. No `sed -i`, no `.agc` import, no write of the picture-size key or either pin input. Device temp files under `/data/local/tmp` are cleared only after a verified write or a verified restore. If the restore cannot be verified, the device backup stays where it is, the script prints its path for the user and stops.
  - Output: The proposed script, with serial, backup and process checks before any filtering.
- F10.3-03 — Filter and check on the host before anything is pushed
  - Description: Filter the host backup. Replace the eight-byte window with line rules. The filtered file must be non-empty and no larger than the original, and every removed line must match the two families. Surviving picture-size or pin-input lines must be byte-identical to the backup. Well-formedness: the XML declaration, the `<map>` line and the `</map>` line must be byte-identical to the backup, and every trap entry must sit on one line; a multi-line trap entry fails closed. Only a file that passes is pushed, and the device temp copy's md5 must equal the host filtered md5.
  - Output: Guard text inside the script that a later edit cannot silently replace with the pin window.
- F10.3-04 — Write, verify content, and restore on mismatch
  - Description: Write and verify run as one pushed `su` script, as in the template; the backup from `F10.3-02` was taken before the host filter, and this script re-checks the live file against it before the write. Just before the `cat`, the script force-stops AGC again and requires `pidof` to be empty. Right after that second force-stop, the live file's md5 and byte length must still equal the device backup. If the file moved during filtering and push, the script aborts with no write and no restore, and the live file stays as AGC left it. After the `cat`, the live file's md5 and byte length must equal the device filtered copy. Owner, label and mode must equal the F10.3-01 triple. On a non-zero exit or any mismatch, the script writes the device backup back into the same inode. It accepts the restore only when md5, byte length, owner, label and mode all match the backup and the reference triple. `pidof` must be empty again after verification.
  - Output: A run log with the drift check and the pre-write, post-write and, when used, post-restore md5, length and `ls -lZ` lines.
- F10.3-05 — Prove the guards and the restore on a host fixture
  - Description: A host-only mode, with no adb call, runs against a synthetic preferences file in a temp directory, not a pulled device file and not a committed file. An empty filter, a non-trap deletion, a picture-size edit, and a broken `</map>` line must each be refused before the push step, with the stand-in digest unchanged. A simulated short write, which truncates the stand-in mid-copy, must trigger the restore and end with the stand-in equal to its backup by md5 and length. Only a trap-line-only filter that is fully written may stand.
  - Output: A local guard log for the run notes.
- F10.3-06 — Correct the two procedure documents
  - Description: In `docs/phase3-preconditions.md`, mark the attribute table and the redirect as AOSPA Android 15 evidence, and name the new script as the HyperOS 4 route. In `docs/agc-12mp-configuration.md`, state that the pin template's owner and label are the same AOSPA constants, that trap cleanup is not an import, and that `prefs.trap.armed` is the gate, so the presence-only sentence in section 6 is not. Date the correction; do not rewrite the AOSPA history.
  - Output: Two modified documents an operator can follow without using `:99`.
- F10.3-07 — Bracket the approved device write
  - Description: After `VAL-103-MANUAL`, run `scripts/smoke.sh` with `ANDROID_SERIAL=dc27e5d0` and `-o` set to `YYYYMMDD-HHMM__Faz10.3__pre-clean`. Run the cleanup script, which may end in the write or in a verified restore. Then take `post-clean` the same way. After a successful write, the comparable region must show the armed count at zero, the derived rear picture size unchanged, and both pin inputs unchanged. After a restore, it must equal the pre snapshot on those lines. Owner, mode and label come from the script's `ls -lZ`, because smoke does not emit them.
  - Output: A pre/post snapshot pair and the script's post-write or post-restore attribute line.
- F10.3-08 — Re-read after a plain relaunch
  - Description: The user relaunches AGC from the launcher. The script does not send a monkey start. The verification launch is not the settings screen: on AOSPA that screen wrote two trap keys, and that route is not measured on HyperOS 4, so opening it would spoil the bracket. A `post-relaunch` snapshot must still show `prefs.trap.armed` at 0 and the same derived rear size. If the script refused or restored, this item confirms the live file still matches the backup, and it is not a second edit.
  - Output: A post-relaunch snapshot, or a not-touched verdict when the script refused or restored.

## 8. Acceptance Criteria

- `scripts/agc-trap-clean.sh` exits before any write unless `platform-tools/adb.exe -s dc27e5d0 get-serialno` prints `dc27e5d0` and the caller's `ANDROID_SERIAL` is unset or `dc27e5d0`.
- A device backup and a host backup both exist and both match the live file's md5 and byte length before a filtered file is pushed.
- After the second force-stop and before the `cat`, the live md5 and byte length still equal the device backup, or the run aborts with neither write nor restore.
- The pre-write owner and label equal W3P04, and the post-write or post-restore owner, label and mode equal that pre-write reading.
- `pidof org.codeaurora.snapcam` is empty at backup, at write and after verification, and AGC is force-stopped again just before the `cat`.
- The host fixture refuses an empty filter, a non-trap deletion, a picture-size edit and a malformed `</map>`, and restores the stand-in after a simulated short write.
- After the write, the live md5 and byte length equal the filtered file; on any mismatch the restore ran and was verified.
- The script text has no `sed -i`, no `.agc` import, and no write of `pref_camera_picturesize_back_key`, `pref_48m_key` or `pref_camera_resolution`.
- After the approved run and a plain user relaunch, `prefs.trap.armed` is 0 on the `post-relaunch` snapshot.
- The derived rear picture-size field is unchanged across the bracket, and mode was read and preserved rather than forced to `0660`.
- Both owned documents say the AOSPA constants and the backup-less redirect are not the HyperOS 4 procedure.
- No preference XML, apk, zip, keystore, or `camera.qcom.so` is added, and existing snapshot files are not rewritten.
- `/data/local/tmp` holds no file from this run after a verified write or a verified restore; after a failed restore verification, the device backup is still there and the user was told its path.
- Each new `Faz10.3` snapshot passed the identity scan and reads `dc27e5d0` on its `# serial` line before commit.
- The script never stops `cameraserver` or a camera provider, and it never calls `setmode.sh`.

## 9. Validation and Test Approach

Validation is a host fixture first, then a three-snapshot device bracket. A trap-family deletion cannot reach the live file unless both backups match it, the file has not moved since the backup, the filtered copy differs only by those lines, and the content is checked again after the write.

- `VAL-103-AUDIT` (proposed) — pre-bracket read of `prefs.trap.armed`, `prefs.trap.count` and `prefs.trap.keys`; key names may be noted, preference values are not copied into the two documents.
- `VAL-103-SERIAL` (proposed) — the caller's `ANDROID_SERIAL` check and the `get-serialno` read both pass before the first device command beyond that read.
- `VAL-103-BACKUP` (proposed) — device and host backups match the live md5 and byte length before the push; after the second force-stop, the live file still matches the device backup; the device filtered copy matches the host filtered md5 before the `cat`.
- `VAL-103-GUARDS` (proposed) — empty, oversized, non-trap, picture-size-touching and malformed filters are refused on the host; a simulated short write triggers a verified restore.
- `VAL-103-VERIFY` (proposed) — after the `cat`, live md5 and length equal the filtered file; after a restore, md5, length, owner, label and mode equal the backup and the reference triple; device temp files are cleared only after one of those two verified outcomes.
- `VAL-103-STOPPED` (proposed) — `pidof org.codeaurora.snapcam` is empty at backup, at write and after verification.
- `VAL-103-OWNER` (proposed) — the PRB9-class pre-write read matches W3P04 owner and label, sets the reference mode, and is equal to the post-run reading.
- `VAL-103-NOWRITE` (proposed) — review of the script text for a picture-size write, a pin-input write, `sed -i`, an `.agc` import, and any service stop or start.
- `VAL-103-BRACKET` (proposed) — pre, post and post-relaunch smoke snapshots whose comparable regions show armed count 0 and unchanged photo-size inputs, or no change after a restore or an abort.
- `VAL-103-DOCS` (proposed) — read-back of the two owned documents for the HyperOS 4 route and the retired AOSPA attribute check.
- `VAL-103-MANUAL` (proposed) — the user approves the run, which covers the write and the automatic restore, handles a permission dialog if one appears, and relaunches AGC from the launcher.
- `VAL-SMOKE` (from Faz 2.1) — `scripts/smoke.sh` as the bracket, with `ANDROID_SERIAL=dc27e5d0` and an `-o` name that has no directory prefix; each output file is then checked by `VAL-101-IDENTITY`.
- `VAL-101-IDENTITY` (from Faz 10.1) — every new `Faz10.3` snapshot passes the identity scan, and its `# serial` line reads `dc27e5d0`, before it is committed; AGC setting values that unmodified `scripts/smoke.sh` output carries are allowed.
- `VAL-READONLY` (from Faz 2.1) — the smoke invocation adds no device command; mutating commands stay inside the cleanup script.

Local versus live: the fixture, the script-text review, the host filter checks and the document read-back are local. The serial read, the attribute read, both backups, the drift check, the write, any restore and the relaunch are live on `dc27e5d0`. Security validation: the cleanup must not print preference values into committed docs. Unmodified smoke output in `snapshots/` may carry `prefs.trap.values` and the pin values, which are settings rather than identity, but each new file still passes `VAL-101-IDENTITY` before commit, and this plan does not widen those fields. Ontology validation: invariant 8 is the subject of the deletion; invariant 3 is kept by not restarting the HAL. `DEC-14` and `DEC-33` are kept by not writing the 50 MP pin and not patching the HAL. Existing snapshot files are not rewritten; the three generated rows below are new files only.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/agc-trap-clean.sh | proposed | Backup-first deletion of the two trap-key families, with host guards, a drift check, a post-write content check and a verified restore. | VAL-103-SERIAL, VAL-103-BACKUP, VAL-103-GUARDS, VAL-103-VERIFY, VAL-103-STOPPED, VAL-103-NOWRITE, VAL-103-OWNER, VAL-103-MANUAL |
| docs/phase3-preconditions.md | modified | Marks the AOSPA owner, label and backup-less redirect as not the HyperOS 4 clearance, and names the new script. | VAL-103-DOCS, VAL-103-OWNER |
| docs/agc-12mp-configuration.md | modified | Records that the pin template's attributes are AOSPA-only, and that trap cleanup is not an import or a picture-size write. | VAL-103-DOCS, VAL-103-NOWRITE |
| scripts/smoke.sh | existing | Read-only armed-count bracket owned by `Faz10.2`; invoked, not edited. | VAL-SMOKE, VAL-READONLY, VAL-103-AUDIT |
| docs/hyperos4-adaptation-notes.md | existing | Read-only `Faz10.1` survey record: the camera-service names the script must not restart and the root channel; it holds no AGC owner or label, which come from W3P04 and the PRB9-class read. | VAL-103-NOWRITE |
| snapshots/YYYYMMDD-HHMM__Faz10.3__pre-clean.txt | generated | Pre-cleanup smoke bracket, stored by `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.3__pre-clean`. Existing snapshot files are not rewritten. | VAL-SMOKE, VAL-101-IDENTITY, VAL-103-BRACKET, VAL-103-AUDIT |
| snapshots/YYYYMMDD-HHMM__Faz10.3__post-clean.txt | generated | Post-write, post-restore or post-abort smoke bracket before relaunch, stored by `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.3__post-clean`. | VAL-SMOKE, VAL-101-IDENTITY, VAL-103-BRACKET |
| snapshots/YYYYMMDD-HHMM__Faz10.3__post-relaunch.txt | generated | Post-relaunch smoke bracket confirming the armed count stayed at zero. | VAL-SMOKE, VAL-101-IDENTITY, VAL-103-BRACKET, VAL-103-MANUAL |

## 10. Dependencies and Sequencing

Depends on: `Faz10.1` for its survey record, which names the camera services this script must leave alone, and for the confirmed root channel from the adb shell. It does not supply the AGC preference owner, label or mode; those come from W3P04 (2026-11-15T13:01Z) and from this plan's own PRB9-class pre-write read. This plan does not depend on `Faz10.2` or `Faz10.4`. The smoke script already exists from Faz 2.1, and the AGC fields it needs are already in `probe_app`.

Blocks: `Faz10.5`. A v2.3 release must not claim that AGC carries no armed trap preference until this bracket has passed. `Faz10.2` and `Faz10.4` are not blocked.

Required decisions: the filter removes both trap families rather than rewriting values. That choice is made here so the live session does not invent a second edit. No decision reopens `DEC-14` or `DEC-33`. User approval of the write is not permission to pin `pref_48m_key`.

Required credentials: none. Root is the phone's existing SukiSU-Ultra `su`. On 2026-11-15 that `su` ran from the adb shell without a dialog; a dialog on cleanup day stops the run.

Required infrastructure: `platform-tools/adb.exe` on the host, device `dc27e5d0`, and `ANDROID_SERIAL=dc27e5d0` for both scripts. In Git Bash, device-path adb arguments run with `MSYS_NO_PATHCONV=1` and host paths are passed as Windows paths (`docs/agc-12mp-configuration.md:152-154`). No network endpoint.

Required human approvals: `VAL-103-MANUAL`. The user approves one run of the cleanup script inside the smoke bracket. That approval covers both device writes the run can make, the trap-line write and the automatic restore from the device backup. The user remains available if `su` raises a permission dialog and relaunches AGC from the launcher after the run. Device temp files in `/data/local/tmp` are cleared after a verified write or a verified restore. If the restore cannot be verified, the device backup is kept, the user is told its path, and the bracket stays open until the user decides. Install, mode switch and shutter are not part of this approval.

Fresh session token and context risk: medium. The repository change is one script and two documents, but a guard in the wrong order can truncate the live preference file. The session stops on the first failed guard and does not improvise a repair outside the verified restore branch.

Subagents are not recommended. The preference file is one stateful object, and a second adb writer during the backup check would make the md5 comparison meaningless.

## 11. Risks and Mitigations

- Risk: the new script bakes in `u0_a450` or the `c194` label, or runs `chcon` toward them. Impact: the check cannot pass on the 2026-11-15 file, or AGC loses the label it can read. Mitigation: `F10.3-01` compares the live read with W3P04; `VAL-103-OWNER` fails the run if the reference is the AOSPA pair.
- Risk (`IMPL-63` recurrence): the redirect truncates the live file before the filtered copy is known good. Impact: AGC preferences wiped, the failure the pin document already recorded on AOSPA. Mitigation: `VAL-103-BACKUP` and `VAL-103-GUARDS` both run before the push; nothing reaches the device until the filtered file passes.
- Risk: the `cat` stops early, from a full filesystem, an adb drop or a killed shell, and leaves a short file on the same inode with the same attributes. Impact: an attribute-only check passes while the preferences are truncated. Mitigation: `F10.3-04` compares md5 and length after the write and restores from the device backup; `VAL-103-VERIFY` checks the restore; the fixture simulates a short write.
- Risk: AGC restarts between the backup and the write, or between the write and the check. Impact: the app rewrites the file from memory, and the backup or the verification compares against a different file. Mitigation: a second force-stop just before the `cat`, the drift check against the device backup right after it, and `VAL-103-STOPPED` requires `pidof` to be empty at backup, write and verification.
- Risk: the filter output is truncated mid-element or loses the root element. Impact: AGC reads a broken XML file even though only trap lines were meant to go. Mitigation: `F10.3-03` requires the declaration and both `map` lines byte-identical to the backup and single-line trap entries, and refuses the push otherwise.
- Risk: the serial check compares a variable the script set itself. Impact: a second attached phone could receive the write. Mitigation: `VAL-103-SERIAL` checks the caller's value first and then the `get-serialno` output before exporting.
- Risk: the eight-byte window is copied onto a multi-line deletion and then bypassed. Impact: either cleanup cannot run, or a bypassed guard deletes the wrong lines. Mitigation: `F10.3-03` replaces that window with a trap-line-only diff; `VAL-103-GUARDS` shows the bad filters failing on the host first.
- Risk: the cleanup writes `pref_camera_picturesize_back_key` or `pref_48m_key` while removing trap lines. Impact: a direct picture-size write, or a 50 MP pin change without new evidence (`DEC-14`). Mitigation: `VAL-103-NOWRITE` on the script text, and `VAL-103-BRACKET` diffs the derived size and both pin inputs.
- Risk: an operator imports a root `.agc` file to clear the trap. Impact: those files carry the trap families and re-arm them. Mitigation: the script has no import path, `F10.3-06` says so in both owned documents, and editing the `.agc` files is out of scope.
- Risk: `sed -i` replaces the inode and leaves the file root-owned with the wrong label. Impact: AGC cannot read its preferences. Mitigation: the only live writes are `cat` into the original inode, of the checked filtered file or of the backup, and the post-run `ls -lZ` must match the reference triple.
- Risk: a helper restart uses the AOSPA service names in `setmode.sh`. Impact: `vendor.camera-provider-2-7-ext` was defined and not running at the 2026-11-15 PRB; starting it would be an inference, not a measurement this plan should make. Mitigation: the script force-stops only `org.codeaurora.snapcam` and does not call `setmode.sh`. A HAL restart, if ever required, is `Faz10.2`: stop the client before the HAL, start the HAL before the client.
- Risk: the AOSPA finding that value `0` is inert is treated as a HyperOS 4 pass. Impact: a cleanup that only zeroes keys could be accepted without a measurement on this ROM. Mitigation: acceptance is `prefs.trap.armed` at 0 after a plain relaunch on this phone, and the script deletes the family lines instead of writing a value.

## 12. Desired End State

On HyperOS 4, AGC has no armed trap preference after a cleanup whose device and host backups were checked before the write. The live content was verified after the write, or the run restored the backup and verified that instead. The rear picture-size key was not written, neither pin input was written, and no `.agc` file was imported. Owner, mode and label match the pre-write reading, whose owner and label equal W3P04 and not the table at `docs/phase3-preconditions.md:83-85`. The two procedure documents point at `scripts/agc-trap-clean.sh`. The 50 MP HAL layer is still off (`DEC-33`), and the wide RAW table was not touched.

The evidence an implementer should produce is the host guard log, including the short-write case; the reference triple with mode; the drift check and the post-write or post-restore md5, length and `ls -lZ` lines; the three `pidof` checks; the three smoke snapshots stamped `Faz10.3` with their identity-scan results; and a statement that the host backup stayed outside the repository and `/data/local/tmp` was cleared after a verified outcome.

The ledger summary Step 4 should append records: the armed count before and after, the measured owner and label against W3P04, that mode was preserved rather than forced, whether the restore branch ran, that `pref_camera_picturesize_back_key` was not written, that no `.agc` file was imported, and the snapshot names.

## 13. Next Sub-Phase Transition Criteria

- The PRB9-class pre-write read matches W3P04's owner and label, and its mode is recorded.
- The host fixture has refused the bad filters and restored the stand-in after a simulated short write.
- The user has approved the run, write and restore, under `VAL-103-MANUAL`.
- The post-relaunch snapshot shows `prefs.trap.armed` at 0, with the derived rear picture size and both pin inputs unchanged.
- Both owned documents name the new script as the HyperOS 4 route and retire the AOSPA constants for this ROM.
- `Faz10.5` can cite that bracket; `Faz10.2` and `Faz10.4` do not wait on it.
