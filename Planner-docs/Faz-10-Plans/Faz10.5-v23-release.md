# Faz 10.5 — v2.3 Release

## 1. Context

Main-Planing Phase 10 (`SNAP-2026-11-15-MAIN`) closes with a release: once the sensor layer, the AGC trap cleanup and the SukiSU-Ultra tile chain are working on HyperOS 4, `ishtar-cam-modes` is stamped v2.3 and shipped through the existing release tooling. This sub-plan owns that last step. Its acceptance slice is the fifth Phase 10 signal: the release checklist passes for v2.3, `Kullanim.txt` is corrected under `DEC-29`, every place that names a version agrees, and the standing of `ishtar-aon-fix` on HyperOS 4 is decided and written down. The planning evidence for this slice is `W3F25` (scout `S4`, 2026-11-15), which lists the version sites, the stale guide statements, the stale module comments and the AON module's early exit.

`DEC-33` (K9 = no) frames the whole text. On HyperOS 4 the 50 MP HAL layer is closed and the sensor layer carries on. The ledger row for `DEC-33` is added after this Step 2, yet every user-facing sentence this plan rewrites has to agree with it already, so the ID is cited here.

The current release is v2.2, versionCode 13, `dist/ishtar-cam-modes-v2.2.zip` with md5 `e95789572311cc95266d3ab4045cdcba` (fact `REL`, 2026-11-13). Its user guide still announces v1.9. Its source comments still describe a launcher alias that hides itself and a tile set of three, both of which v2.1 and v2.0 changed. The user chose on 2026-11-13 to leave the guide as shipped in v2.2 and correct it in the next release (`DEC-29`); this is that release.

Planning run 21 specified this sub-plan on 2026-11-15; its draft was written on 2026-11-16. It is the last of five. `Faz10.2` hands it a `setmode.sh` that restarts the measured services and refuses `50mp`. `Faz10.3` hands it a backed-up trap cleanup bracket. `Faz10.4` hands it a tile and WebUI chain that works under SukiSU-Ultra, with `50mp` removed from those surfaces, a dated notes file holding the tile APK's certificate digest, and possibly its tile-switch check still gated. Until all three have exited, a v2.3 stamp would describe behaviour nobody has seen on this phone.

## 2. Goal

Ship `ishtar-cam-modes` v2.3 built by `scripts/build-release.py`, with a rewritten user guide, agreeing version strings, corrected module comments, a tile APK rebuilt at version 2.3 and a recorded AON decision, installed by the user on `dc27e5d0` and recorded against the release checklist.

## 3. Description

The problem is drift between what the module says and what it does. The installer banner says v2.2 while the guide says v1.9. The guide speaks of three tiles and of a WebUI reached through KernelSU-Next, a manager that is not on the phone. The installer promises that an update keeps the current mode, and no code keeps it. Two comments still claim the launcher alias disables itself after root is granted, although since v2.1 it stays visible on purpose. None of this breaks a mode switch, but every sentence a user reads at install time or in the guide is a claim, and several are wrong.

It belongs at the end of Phase 10 because the text has to describe the post-adaptation tree. Whether there are three or four tiles, which manager opens the WebUI, whether the Action button cycle includes `50mp`: each answer is set by `Faz10.2` or `Faz10.4`. Writing the guide before those plans land would mean writing it twice.

The vibecoding slice strategy: settle the text on the host first, then let the build tools and one installation prove it. The guide, the comments and the version sites are edited and checked without the phone. The tile APK is rebuilt once for its new version, a `%TEMP%` module build goes through the self-test, and only after the user installs that archive and the bracket passes does the real build write `dist/` and the manifest. The fastest validation signal is a host grep that finds one version value at every site and no leftover `v2.2` or `2.1` among the module's version lines.

What should not be over-planned: a new release process, a CI hook, or a rewrite of the checklist's history. `docs/release-checklist.md` and `scripts/build-release.py` already define how a release is made and recorded. This plan adds one evidence record for v2.3 and leaves the v2.2 record as written.

The AON question is a decision, not an engineering task. `ishtar-aon-fix/post-fs-data.sh:12-15` exits without change when `/vendor/lib64/camera/aon_front.pb` exists (fact `E3`), and the HyperOS 4 ROM ships that path as a link to `/odm/lib64/camera/aon_front.pb` (fact `D6`, 2026-11-13). On this ROM the module therefore does nothing. The plan asks the user where it stands and records the answer; it does not delete the module or its archive.

Every new sentence in the guide keeps measurement and history apart. Numbers measured on AOSPA Android 15, such as switch timings or the noise comparison, stay only if labelled as AOSPA results. A HyperOS 4 claim is written only when a Phase 10 bracket or this plan's own bracket shows it.

## 4. Scope

- A full rewrite of `ishtar-cam-modes/Kullanim.txt` for v2.3 that clears the thirteen stale statements listed in `PROJECT_LOG.md:852-866` plus the further ones listed in section 6.
- The v2.3 version value at every site: `ishtar-cam-modes/module.prop:3-4`, `ishtar-cam-modes/customize.sh:2`, `Kullanim.txt:1`, the tile manifest `:11-12`, a new `CHANGELOG.md` entry above `:22`, `README.md:20` and `:94`, and the generated `docs/release-manifest.md`.
- Installer text in `customize.sh`: the unmet update promise at `:62`, the `50mp` mentions at `:60`, `:67` and `:71`, and the KernelSU Superuser hint at `:72-73`, aligned with `DEC-33` and with SukiSU-Ultra.
- The `module.prop` name and summary aligned with `DEC-33`, without regrowing a changelog inside the description.
- Version-suffix edits in four `Faz10.4` files, limited to the lines named in section 9: `action.sh:7`, `:17`; `service.sh:8-12`; `tile-app/AndroidManifest.xml:5`, `:11-12`, `:52-54`; `BaseTile.java:17`.
- The tile app `versionName` from 2.1 to 2.3, with `versionCode` raised from 11 to 12, and one rebuild of `ishtar-cam-modes/tile-app.apk` with `tile-app/build.sh` for that version change only.
- The `Faz10.4` tile-switch check `VAL-104-SWITCH`, run inside this plan's post-install bracket.
- A recorded user decision on `ishtar-aon-fix` for HyperOS 4, written into `docs/aon-verification.md` and `README.md`.
- A `%TEMP%` build with the self-test, a user install with a smoke bracket, then the release build into `dist/` and `docs/release-manifest.md`.
- A v2.3 evidence record in `docs/release-checklist.md` section 7.
- Three new snapshot files whose names carry `Faz10.5`.

## 5. Out of Scope

- Any behaviour change in `setmode.sh`, `post-fs-data.sh` or `halpatch.sh`. Those belong to `Faz10.2`.
- Any AGC preference write, `sed -i` on a preference file, or `.agc` import. Trap cleanup is `Faz10.3`, and this plan only cites its bracket.
- Code changes in `action.sh`, `service.sh`, `webroot/index.html`, the tile manifest's component list, `strings.xml`, or any tile Java logic. Those are `Faz10.4`; this plan touches only the comment and version lines it names.
- Editing `tile-app/build.sh`, changing what the APK contains, or signing it with a new key. The rebuild here exists only to carry the version bump and uses the same `tile-app/debug.keystore` that `Faz10.4` signed with, which is untracked and kept out of every archive.
- Committing the APK, the zip or any keystore; `ishtar-cam-modes/tile-app.apk`, the keystore and `dist/` stay untracked.
- Reopening the 50 MP HAL layer. `DEC-33` keeps it closed on HyperOS 4, and `DEC-14` keeps 50 MP out of AGC until new evidence exists. No guide sentence may suggest otherwise.
- Narrowing the wide RAW table, or loosening the rule that `50mp` and DCG/LN exclude each other.
- Fixing `docs/recovery-runbook.md:113` or `docs/agc-12mp-configuration.md:381` (fact `W3F27`), or adding a `.gitignore` rule for `camera.qcom.so`. Neither path is in this plan's owner map.
- Deleting `ishtar-aon-fix/`, its root archive, or any older release archive.
- Adding `*.apk`, `*.zip`, `*.keystore`, `*.jks` or `camera.qcom.so` to the tree.
- Editing an existing file under `snapshots/`.

## 6. Current Repository Evidence

`ishtar-cam-modes/module.prop` was read on 2026-11-16: `:3` is `version=v2.2`, `:4` is `versionCode=13`, and `:2` names the module "(50MP / DCG / LN2 / LN4)". The `:6` description still sells the 50MP HAL mode with the OpenCamera measurement and lists four tiles including 50MP.

`ishtar-cam-modes/customize.sh` was read on 2026-11-16. `:2` prints the banner `v2.2`. `:62` prints that the starting mode is stock on first install and the current mode on update. `Planner-docs/Planing-Ledger.md` records the second half as unimplemented (`FIND-1.5-01`), and `docs/release-checklist.md:491-497` repeats that the promise is still unmet. `:60` lists `50mp` among the modes, `:67` uses `setmode.sh 50mp` as the switching example, `:71` names the tiles as 50MP DCG LN4 LN2, and `:72-73` direct the user to the KernelSU Superuser list, a path `Faz10.4` renames to SukiSU-Ultra in its own files. The HAL branch at `:40-50` already prints that 50MP stays disabled when the HAL md5 is unknown, which is the HyperOS 4 case.

`ishtar-cam-modes/Kullanim.txt` was read in full on 2026-11-16; a line-end search found carriage returns on its lines, so it is stored with CRLF line ends, unlike the other owned files. `:1` reads v1.9. `PROJECT_LOG.md:852-866` lists thirteen stale statements: the version title, no 50mp mode at `:46`, three tiles at `:53-57`, the internal conflict between `:56` and `:69-70`, the Superuser label at `:102`, three WebUI buttons at `:119-122`, `50mp` missing from the examples at `:135-139` and `:146-150`, no HAL layer at `:246-250`, no HAL md5 lock at `:253-257`, the no-reboot video claim at `:45` (`FIND-2.3-06`), the CSIPHY line offered as a diagnosis at `:212` (`FIND-2.3-04`), the stock camera crash claim at `:214-215` (refuted by `IMPL-70` and `IMPL-88`), and no mention of the AGC 12.58 MP configuration. None of them claims 50 MP inside AGC.

`W3F25` says `S4` found three more stale statements; the sources this draft may read do not itemise them. A read on 2026-11-16 found these candidates beyond the thirteen: `:120` sends the user through KernelSU-Next, while the phone runs SukiSU-Ultra v4.3.0-r1 and has no `com.rifsxd.ksunext` (`W3P01`); `:126` gives the Action cycle as stock, dcgB, ln4f, stock, while `action.sh:152-154` step through `50mp`; `:197` names `vendor.camera-provider-2-7-ext` as a restart target, which `Faz10.2` replaces with the measured HyperOS 4 set; and `:88-90` explain tile sync in terms of three tiles. `F10.5-01` reconciles that list with `S4` before writing.

The four version-suffix files were read on 2026-11-16. `action.sh:7` documents the argument-less cycle as stock to dcgB to ln4f to stock; `:152-154` add `50mp` before stock. `action.sh:17` documents `info` as a three-field summary; `:182-188` print five pipe-separated fields, the fifth added in v2.0. `service.sh:8-12` say the launcher alias switches itself off once root is granted and the app leaves the drawer; the guide at `Kullanim.txt:60-67` and the v2.1 changelog say the launcher stays visible by default. `tile-app/AndroidManifest.xml:5` says there is no LAUNCHER intent filter, while the `.Launcher` alias declares one; `:11-12` carry `versionCode="11"` and `versionName="2.1"`; `:52-54` repeat the self-disabling alias story. `BaseTile.java:17` opens with "Uc kutucugun ortak davranisi", a three-tile description, while the v2.2 manifest registers four tile services.

`ishtar-cam-modes/tile-app/build.sh` was read on 2026-11-16. `:25` defaults `KS` to `debug.keystore` beside the script, which is `ishtar-cam-modes/tile-app/debug.keystore`; that file is present in the working tree, ignored by `.gitignore:19-21`, and excluded from the release archive by `scripts/build-release.py:96-97`. `:33-34` show `KS`, `KS_PASS` and `KS_ALIAS` supplied from the environment for another key, and `:35-36` warn that an APK signed with a different key will not install over the existing copy. If the key file is missing, step 6 generates a fresh one before signing. The signed result lands in `tile-app/out/` as `ishtar-cam-tiles.apk` and is copied by hand to `ishtar-cam-modes/tile-app.apk`. Its Python step is switched to `py -3` by `Faz10.4`. `action.sh:48-54` decide whether the installed APK needs an update by md5, not by version number.

`CHANGELOG.md:22` is the `## v2.2` heading; the file says new versions add an entry there and do not extend the `module.prop` description. `README.md:20` describes the module as ten sensor modes plus the 50MP HAL layer at v2.2 / versionCode 13. `README.md:94` names `dist/ishtar-cam-modes-v2.2.zip` and its md5. `README.md:21` already says `ishtar-aon-fix` exits without change when HyperOS 4 ships the file, and `:89` still calls `ishtar-aon-fix-v1.1.zip` the current AON fix release.

`scripts/build-release.py` was read on 2026-11-16. `:187-193` take the version from the `version=` line of `module.prop`, `:403` names the archive `ishtar-cam-modes-<version>.zip`, and `:372-374` accept `--out` and `--manifest`, with `docs/release-manifest.md` as the default manifest. The include list is `:67-86`, and every file that matches neither it nor the exclude list fails assertion A3. The planned `.sh` name in `Faz9.1-reproducible-release-build.md:128` is drift; the tool that exists is the Python file.

Upstream KernelSU's installer script removes `$MODPATH/customize.sh` once installation finishes. SukiSU-Ultra is a KernelSU fork, so the same removal on this phone is an inference, not a measurement. The installed module directory therefore cannot be relied on to hold `customize.sh` for an md5 comparison.

`docs/release-manifest.md` currently binds `ishtar-cam-modes-v2.2.zip`, 43 entries, md5 `e95789572311cc95266d3ab4045cdcba`. `docs/release-checklist.md` section 7 defines the per-release record format and holds the v2.2 record at `:521` onward; the outstanding-gates list at `:578-590` names `module.prop:3`, `module.prop:4` and `customize.sh:2` as the version sites that must move together.

Fact `T3` was checked against today's text. `docs/release-checklist.md:165` passes `<YYYYmmdd-HHMM>__release__<label>` and `docs/agc-12mp-configuration.md:202` passes `<YYYYmmdd-HHMM>__<subplan>__<label>`; neither carries a `snapshots/` prefix any more, and `:414` was already correct. `scripts/smoke.sh:9` documents `-o NAME` as storing `snapshots/NAME.txt`, and `:284` writes `$SNAPDIR/$OUT_NAME.txt`. `T3` is fixed in the tree; this plan does not edit either document for it.

`ishtar-aon-fix/module.prop` reads v1.1, versionCode 2, and describes repairing a missing `aon_front.pb`. `ishtar-aon-fix/post-fs-data.sh:12-15` log "zaten mevcut" and exit when the path exists. `docs/aon-verification.md` records `DEC-04` (keep separate) and, in section 8, an AOSPA Step 0 run whose providers did not appear (`FIND-6.2-03`). Nothing in it speaks of HyperOS 4.

## 7. Planned Work Breakdown

- F10.5-01 — Fix the stale-statement list
  - Description: After `Faz10.2`, `Faz10.3` and `Faz10.4` have exited, reread `Kullanim.txt` against the tree as it then stands. Start from the thirteen `PROJECT_LOG.md` items and the section 6 candidates, reconcile them with the three `S4` statements, and write the final list with each item's line number, the code or record that contradicts it, and the replacement claim.
  - Output: a stale-statement table kept with the implementation notes.

- F10.5-02 — Rewrite the user guide
  - Description: Rewrite `ishtar-cam-modes/Kullanim.txt` in the existing ASCII Turkish style and CRLF line ends, titled v2.3. Name SukiSU-Ultra as the manager and describe the tile count, WebUI buttons and Action cycle exactly as `Faz10.4` left them. State that `50mp` exists in the engine, that its HAL layer is closed on HyperOS 4 by its md5 lock (`DEC-33`), and that it never combines with DCG/LN. Give the HyperOS 4 restart order as `Faz10.2` measured it: client stopped before the HAL, HAL started before the client. Describe the AGC 12.58 MP working resolution and say that 50 MP stays off in AGC (`DEC-14`). Mark every AOSPA measurement as AOSPA. Drop the video no-reboot promise, the CSIPHY-as-diagnosis line and the stock camera crash claim. Every root command in the guide is written with its command quoted, as `su -c '…'`. Write no preference value and no identity value.
  - Output: the rewritten `Kullanim.txt`.

- F10.5-03 — Move every version site to v2.3
  - Description: Set `module.prop:3` to `version=v2.3` and `:4` to `versionCode=14`, the banner at `customize.sh:2` to v2.3, and `Kullanim.txt:1` to v2.3. Add a `## v2.3` entry above `CHANGELOG.md:22` that lists the HyperOS 4 adaptation by sub-plan, in the file's ASCII Turkish style. Update `README.md:20` for v2.3 / versionCode 14 and the closed HAL layer, and `README.md:94` for the new archive name; the md5 there is filled from the release build in `F10.5-12`.
  - Output: consistent version text across the owned files.

- F10.5-04 — Align installer and summary text with DEC-33 and SukiSU-Ultra
  - Description: Replace `customize.sh:62` with a sentence that says what happens: every install, update included, starts in stock, because the archive ships no `mode` file. Mark `50mp` at `:60` as closed on HyperOS 4, switch the example at `:67` to `dcgB`, make the tile list at `:71` match the manifest `Faz10.4` left, and point the root-grant hint at `:72-73` to the SukiSU-Ultra Superuser list with the same app label `Faz10.4` uses. Quote the example commands as `su -c '…'`. Rename the module at `module.prop:2` and shorten the `:6` summary so it no longer offers the 50MP HAL mode as a working feature on this ROM. Leave the md5 guards and the HAL branch unchanged.
  - Output: installer prints and module summary that agree with `DEC-33` and name SukiSU-Ultra.

- F10.5-05 — Fix the version-suffix comment lines
  - Description: Re-locate each line by content once `Faz10.4` has landed, since its edits may shift numbers. In `action.sh`, make `:7` state the cycle that `action.sh` steps through after `Faz10.4`, and make `:17` list the five `info` fields. In `service.sh:8-12`, say the alias exists so the Superuser list shows the app and that it stays visible unless `tiles hide` is run, quoting the two example commands as `su -c '…'`. In the tile manifest, make `:5` agree with the `.Launcher` alias and `:52-54` agree with the visible-by-default rule. In `BaseTile.java:17`, state the number of tile services the manifest then registers. Change nothing else in these four files.
  - Output: four files whose diff touches only the named comment lines and the manifest version lines.

- F10.5-06 — Bump the tile app version and rebuild its APK
  - Description: In `tile-app/AndroidManifest.xml:11-12`, set `android:versionCode="12"` and `android:versionName="2.3"`; a higher code keeps the in-place `pm install` from being a downgrade. Read `docs/hyperos4-tile-webui-notes.md` for the certificate SHA-256 digest `Faz10.4` recorded and for the key path it used. Rebuild once with `ishtar-cam-modes/tile-app/build.sh <SDK root>` in Git Bash using the `:25` default key `ishtar-cam-modes/tile-app/debug.keystore`; set `KS`, `KS_PASS` and `KS_ALIAS` only if those notes name a different key. If the key file is missing, stop and ask the user, because step 6 would otherwise mint a new key that cannot update the installed app. `KS_PASS` is never written into a note, a snapshot or the ledger. Copy `tile-app/out/ishtar-cam-tiles.apk` to `ishtar-cam-modes/tile-app.apk`. Run both `aapt2 dump badging` on it, for versionName 2.3 and versionCode 12, and `apksigner verify --print-certs`, whose SHA-256 certificate digest must equal the one in the `Faz10.4` notes; a different digest stops the plan. Record the APK md5 and the digest. The rebuild carries no source change beyond the version lines and the comment lines of `F10.5-05`.
  - Output: a version 2.3 APK under the module directory, untracked and kept out of every commit, with its md5 and digest on record.

- F10.5-07 — Record the AON decision
  - Description: Present the user with three choices and a recommendation. Keep the module unchanged and not install it on HyperOS 4, with a note in the docs; also add a HyperOS 4 sentence to `ishtar-aon-fix/module.prop`'s description; or mark the module retired for HyperOS 4 while keeping its source and archive for AOSPA history. The recommendation is the first choice: `E3` and `D6` show the module would exit at `post-fs-data.sh:12-15`, so installing it adds a boot log line and nothing else. Write the answer, its date and its evidence as a new dated section of `docs/aon-verification.md`, keep `DEC-04` as history, and update `README.md:89` to match. The ledger assigns the decision its ID when `3 · O4` or a later run records it. If the user picks the second choice, `ishtar-aon-fix/module.prop` becomes a modified path and its description line is the only edit.
  - Output: a recorded AON decision in two documents.

- F10.5-08 — Build to `%TEMP%` and run the self-test
  - Description: On the host, in Git Bash, run `py -3 scripts/build-release.py --self-test`, then `py -3 scripts/build-release.py --out "$TEMP/ishtar-cam-modes-v2.3.zip" --manifest "$TEMP/release-manifest-v2.3.md"`. Expect version v2.3, no unclassified file, the A1, A2 and A3 assertions intact, and a `tile-app.apk` entry whose md5 equals the one recorded in `F10.5-06`. List the archive with `py -3 -m zipfile -l "$TEMP/ishtar-cam-modes-v2.3.zip"` and confirm a `customize.sh` entry is present; its md5 in the temp manifest must equal the tree file's md5, because the installed copy may be removed by the installer and cannot be checked on the phone. Record the temp archive md5. If A3 names a file `Faz10.4` added, stop; adding a contents rule to `scripts/build-release.py` is the one edit this plan may make there, and it is recorded before the build is retried. Do not run the bare command in this step; it would overwrite `dist/` and `docs/release-manifest.md`.
  - Output: a temp archive with its md5, its temp manifest, the `customize.sh` check, and a passing self-test.

- F10.5-09 — Pre-install checks, rollback archive and backup
  - Description: Read the root manager with `platform-tools/adb.exe -s dc27e5d0 shell dumpsys package com.sukisu.ultra` and confirm versionName `v4.3.0-r1` and versionCode 41140; any other manager or version stops the command list and goes to the user. Read the installed `version=` and `versionCode=` with `platform-tools/adb.exe -s dc27e5d0 shell "su -c 'cat /data/adb/modules/ishtar_cam_modes/module.prop'"`, name the host archive that installed it (the `Faz10.4` temp zip or `dist/ishtar-cam-modes-v2.2.zip`), and record that file's path and md5; if no host archive matches, stop and ask. Keep that rollback archive unchanged until `F10.5-12` has finished. Copy the live `mode` and `lang` files with `su -c 'cat /data/adb/modules/ishtar_cam_modes/lang > /data/local/tmp/ishtar-lang.bak'` and the matching command for `mode`, then `platform-tools/adb.exe -s dc27e5d0 pull` each into `%TEMP%`; compare md5 and byte length on the phone and on the host, and note a missing file as absent rather than empty. Run `ANDROID_SERIAL=dc27e5d0 MSYS_NO_PATHCONV=1 scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.5__pre-v23`. If v2.2 is the installed build at this point, nobody touches the Action button, the WebUI or `setmode.sh` before the v2.3 install is verified.
  - Output: the manager check, the named rollback archive with its md5, the verified backup, and the pre-install snapshot.

- F10.5-10 — User install, reboot, live md5, settings restore
  - Description: With the user's approval, push the temp archive to the phone, then read back its md5 and length there; on a mismatch, delete the copy, push again and re-check. The user installs it through the SukiSU-Ultra manager and reboots. Before any mode switch, read the md5 of the installed `module.prop`, `Kullanim.txt`, `action.sh`, `service.sh`, `setmode.sh` and `tile-app.apk` with `su -c 'md5sum …'` and compare each with the temp manifest; a mismatch stops the step and the user reinstalls the rollback archive named in `F10.5-09`. Read `dumpsys package com.ishtar.cammodes` for versionName 2.3. After `VAL-105-INSTALL` passes, restore `lang` if it existed: stop the tile app with `am force-stop com.ishtar.cammodes`, push the host backup to `/data/local/tmp`, copy it with `su -c 'cp /data/local/tmp/ishtar-lang.bak /data/adb/modules/ishtar_cam_modes/lang && chmod 0644 /data/adb/modules/ishtar_cam_modes/lang'`, then compare md5 and length with the backup; on a mismatch, copy again from the backup and verify before going on. `mode` is not written as a file: an install leaves it at stock by design, so if the backed-up mode differs, the user restores it in `F10.5-11` through a normal module switch. Delete the `/data/local/tmp` copies and the pushed archive once the restore is verified. Run `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.5__post-v23` with the same environment.
  - Output: the installed-file comparison, the restored `lang`, cleaned temp copies, and the post-install snapshot.

- F10.5-11 — Tile switch and checklist rows
  - Description: Run `VAL-104-SWITCH` first, inside this bracket: the installed `setmode.sh` md5, read with `su -c 'md5sum /data/adb/modules/ishtar_cam_modes/setmode.sh'`, must equal the tree copy `Faz10.2` left, and only then does the user tap the DCG tile once, open the camera, and tap again to return to stock. A mismatch means the gate stays closed and no tile tap happens. Then the user works through the checklist rows that apply on HyperOS 4: WebUI switching under SukiSU-Ultra, the Action button, every mode except `50mp`, the camera opening, one reboot with the mode kept, and 1080p60 and 4K60. If the backed-up mode was not stock, the last switch returns to it, and the live `mode` file is then compared with the backup by md5. Mode changes go through the module only; the implementer sends no `stop` or `start` to a camera service. `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.5__post-modes` closes the bracket.
  - Output: the `VAL-104-SWITCH` result, the user's checklist results, and the closing snapshot.

- F10.5-12 — Release build and record
  - Description: Only after `F10.5-11` passes, run `py -3 scripts/build-release.py` from the repository root. It writes `dist/ishtar-cam-modes-v2.3.zip` and regenerates `docs/release-manifest.md`. The archive md5 must equal the temp archive's md5, because the tree has not changed and the build is byte-identical on one host. Fill `README.md:94` with that md5. Append a v2.3 record to `docs/release-checklist.md` section 7 in the existing format; the 50 MP rows are `waived` with `DEC-33` as the reason, the tile row cites `VAL-104-SWITCH`, and no row ships as `pending`. The rollback archive from `F10.5-09` may be released from hold only after this step.
  - Output: the release archive, the manifest, and the v2.3 checklist record.

- F10.5-13 — Scan and hand over
  - Description: Run the `Faz10.1` identity scan on each new `Faz10.5` snapshot, confirm its serial header reads `dc27e5d0`, and confirm the existing snapshot files are byte-unchanged. Delete the host `%TEMP%` copies of `mode` and `lang`. Pass the edited files, the three snapshots and the decision record to the orchestrator for commit. The zip, the APK and the keystore stay untracked and out of the commit.
  - Output: a commit-ready change set.

## 8. Acceptance Criteria

- Every entry of the final stale-statement list is cleared in the rewritten guide, and each AOSPA figure that stays is labelled AOSPA.
- The guide names SukiSU-Ultra, matches the post-`Faz10.4` tile count, WebUI buttons and Action cycle, keeps 50 MP off in both the HAL layer and AGC, and quotes every root command.
- `module.prop`, the installer banner, the guide title, `CHANGELOG.md`, `README.md`, the tile manifest and the generated manifest all name v2.3; `module.prop` reads versionCode 14 and the tile manifest reads versionCode 12.
- The rebuilt APK reports versionName 2.3 in `aapt2 dump badging`, and its `apksigner` SHA-256 certificate digest equals the one in the `Faz10.4` notes.
- `customize.sh` no longer promises that an update keeps the current mode, and its root-grant hint names SukiSU-Ultra.
- The diffs of `action.sh`, `service.sh`, `tile-app/AndroidManifest.xml` and `BaseTile.java` touch only the lines this plan names.
- The AON decision is recorded with its date and the `E3` and `D6` evidence, and `README.md` agrees with it.
- The self-test passes, the temp archive holds a `customize.sh` entry matching the tree, and the release archive md5 equals the md5 of the archive the user installed.
- The installed files on the compared list match the manifest after the reboot, before any mode switch.
- `lang`, and `mode` if it was not stock, match their backups by md5 after the restore, and the device temp copies are gone.
- `VAL-104-SWITCH` passed with its gate open inside the post-install bracket.
- The three new snapshots pass the identity scan and the older snapshot files are byte-unchanged.
- The v2.3 checklist record has no `pending` row, and its waivers name their reasons.
- No preference file was written, no `.agc` file was imported, no file this plan adds or changes records a `KS_PASS=` assignment or a password value, and no archive, APK, keystore or HAL binary entered the tree.

## 9. Validation and Test Approach

Validation is mostly host-side text and build checks, closed by one user-performed install inside a smoke bracket. The live half proves that the archive the user ran is the archive that ships, and that a tile tap switches modes on the released build.

- `VAL-105-KULLANIM` (proposed) — the final stale-statement table is checked item by item against the rewritten guide; the guide is also searched for KernelSU-Next, the v1.9 title, an unlabelled AOSPA figure, a 50 MP claim for AGC, an unquoted `su -c` command, and any preference value. Line ends stay CRLF.
- `VAL-105-VERSIONS` (proposed) — a host search of the owned files and the four version-suffix files finds v2.3 at every version site, versionCode 14 in `module.prop`, versionCode 12 and versionName 2.3 in the tile manifest, and no remaining v2.2 or 2.1 version line.
- `VAL-105-COMMENTS` (proposed) — each corrected comment is read beside the code it describes, and a zero-context diff of the four version-suffix files shows hunks only at the named lines.
- `VAL-105-APK` (proposed) — `aapt2 dump badging` on the rebuilt `tile-app.apk` shows versionName 2.3 and versionCode 12; `apksigner verify --print-certs` shows a SHA-256 certificate digest equal to the one recorded in `docs/hyperos4-tile-webui-notes.md`; `git status` lists neither the APK nor the keystore; no file this plan adds or changes records a `KS_PASS=` assignment or a password value, and the existing lines `tile-app/build.sh:34` and `:37` stay untouched.
- `VAL-105-AON` (proposed) — `docs/aon-verification.md` carries a dated HyperOS 4 section with the user's answer and the `E3` and `D6` evidence, and `README.md` states the same standing.
- `VAL-105-BUILD` (proposed) — the `%TEMP%` build reports v2.3, no unclassified file and the recorded APK md5; its listing holds `customize.sh` with the tree file's md5; the later release build in `dist/` has the same md5 as the temp archive.
- `VAL-ASSERT` (from Faz 9.1) — `py -3 scripts/build-release.py --self-test` proves the packaging assertions still fire.
- `VAL-MANIFEST` (from Faz 9.1) — the regenerated `docs/release-manifest.md` checksums are recomputed against `dist/ishtar-cam-modes-v2.3.zip`.
- `VAL-105-ROLLBACK` (proposed) — before the push, the installed version, the matching host archive path and its md5 are recorded; that file is unchanged when `F10.5-12` ends.
- `VAL-105-BACKUP` (proposed) — `mode` and `lang` copies match the live files by md5 and length on both phone and host before the install; after the restore, `lang` and any restored `mode` match the backup, and the `/data/local/tmp` copies are deleted.
- `VAL-105-INSTALL` (proposed) — after the reboot and before any switch, the installed `module.prop`, `Kullanim.txt`, `action.sh`, `service.sh`, `setmode.sh` and `tile-app.apk` equal their manifest entries by md5, and the tile package reports versionName 2.3.
- `VAL-104-SWITCH` (from Faz 10.4) — run in this plan's post-install bracket: the installed `setmode.sh` must match the tree copy by md5 before anything is tapped; with that match, the user taps DCG once, opens the camera, and taps back to stock.
- `VAL-SMOKE` (from Faz 2.1) — `scripts/smoke.sh -o` with `ANDROID_SERIAL=dc27e5d0 MSYS_NO_PATHCONV=1`, three runs, with the script unchanged.
- `VAL-101-IDENTITY` (from Faz 10.1) — the identity scan on each new `Faz10.5` snapshot before commit; a hit blocks the commit.
- `VAL-103-BRACKET` (from Faz 10.3) — the trap-cleanup bracket the changelog and guide cite before claiming that AGC carries no armed trap preference.
- `VAL-105-CHECKLIST` (proposed) — the v2.3 record in `docs/release-checklist.md` section 7 lists archive identity and one result per capability, with no `pending` row and every waiver explained.
- `VAL-105-MANUAL` (proposed) — the user approves the push, installs v2.3 through SukiSU-Ultra, reboots, answers any dialog, approves the `lang` restore, performs the tile, WebUI, Action, mode, reboot and video checks, decides if the signing key is missing or its digest differs, and answers the AON question.

Local versus live: guide, versions, comments, APK rebuild, AON record, builds and the checklist record are local. The manager check, the rollback record, the backup, the push, the install, the md5 read-back, the restore, the tile switch and the three smoke runs are live. Security validation is the identity scan, the build assertions, the signer digest match, and the keystore staying untracked and out of every archive. Artifact validation is the equal md5 between the installed and the shipped archive.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/Kullanim.txt | modified | Full v2.3 rewrite of the user guide under `DEC-29`, with the final stale-statement list cleared. | VAL-105-KULLANIM, VAL-105-VERSIONS |
| ishtar-cam-modes/module.prop | modified | Version v2.3 and versionCode 14 at lines 3-4; name and summary aligned with `DEC-33`. | VAL-105-VERSIONS, VAL-105-INSTALL |
| ishtar-cam-modes/customize.sh | modified | Banner v2.3 at line 2; truthful start-mode line at 62; `50mp` mentions at 60, 67 and 71 and the root-grant hint at 72-73 aligned with `DEC-33` and SukiSU-Ultra. | VAL-105-VERSIONS, VAL-105-COMMENTS, VAL-105-BUILD |
| CHANGELOG.md | modified | New v2.3 entry above the v2.2 heading at line 22. | VAL-105-VERSIONS |
| README.md | modified | Module row at line 20 and dist line at 94 for v2.3; AON row at 89 per the recorded decision. | VAL-105-VERSIONS, VAL-105-AON |
| docs/aon-verification.md | modified | Dated HyperOS 4 section holding the user's AON decision and its evidence. | VAL-105-AON, VAL-105-MANUAL |
| docs/release-checklist.md | modified | Appends the v2.3 evidence record in section 7; earlier records stay as written. | VAL-105-CHECKLIST, VAL-104-SWITCH |
| docs/release-manifest.md | generated | Regenerated by the release build for the v2.3 archive. | VAL-MANIFEST, VAL-105-BUILD |
| dist/ishtar-cam-modes-v2.3.zip | generated | Release archive from the bare build; untracked, never committed. | VAL-105-BUILD, VAL-ASSERT |
| scripts/build-release.py | existing | Release tool, used unchanged; a contents rule is added only if A3 flags a file from `Faz10.4`. | VAL-ASSERT, VAL-105-BUILD |
| ishtar-aon-fix/module.prop | existing | Unchanged under the recommended AON answer; its description line is edited only if the user picks that choice. | VAL-105-AON |
| ishtar-cam-modes/action.sh | modified | Version-suffix exception: comment line 7 (cycle) and comment line 17 (info fields) only. | VAL-105-COMMENTS |
| ishtar-cam-modes/service.sh | modified | Version-suffix exception: comment lines 8-12 (launcher alias) only. | VAL-105-COMMENTS |
| ishtar-cam-modes/tile-app/AndroidManifest.xml | modified | Version-suffix exception: comment line 5, versionCode and versionName at lines 11-12, comment lines 52-54 only. | VAL-105-COMMENTS, VAL-105-VERSIONS |
| ishtar-cam-modes/tile-app/java/com/ishtar/cammodes/BaseTile.java | modified | Version-suffix exception: comment line 17 (tile count) only. | VAL-105-COMMENTS |
| ishtar-cam-modes/tile-app.apk | generated | Version-suffix exception: rebuilt only to carry the version 2.3 / 12 manifest bump, signed with the same untracked key `Faz10.4` used; untracked and kept out of every commit. | VAL-105-APK, VAL-105-INSTALL, VAL-104-SWITCH |
| ishtar-cam-modes/tile-app/build.sh | existing | Read-only: run as `Faz10.4` left it, with its default in-tree untracked key unless the `Faz10.4` notes name another. | VAL-105-APK |
| docs/hyperos4-tile-webui-notes.md | existing | Read-only: the certificate digest and key location `Faz10.4` recorded, used for the signer comparison. | VAL-105-APK |
| ishtar-cam-modes/setmode.sh | existing | Read-only: the restart order and `50mp` refusal the guide describes, and the md5 gate for the tile switch. | VAL-105-KULLANIM, VAL-104-SWITCH |
| ishtar-cam-modes/webroot/index.html | existing | Read-only: WebUI buttons the guide must describe after `Faz10.4`. | VAL-105-KULLANIM |
| ishtar-aon-fix/post-fs-data.sh | existing | Read-only evidence of the early exit when the AON file already exists. | VAL-105-AON |
| scripts/smoke.sh | existing | Bracket tool, used unchanged with the pinned serial. | VAL-SMOKE |
| snapshots/YYYYMMDD-HHMM__Faz10.5__pre-v23.txt | generated | Smoke snapshot before the v2.3 install. | VAL-SMOKE, VAL-105-ROLLBACK, VAL-101-IDENTITY |
| snapshots/YYYYMMDD-HHMM__Faz10.5__post-v23.txt | generated | Smoke snapshot after install, reboot, md5 read-back and the settings restore. | VAL-SMOKE, VAL-105-INSTALL, VAL-105-BACKUP, VAL-101-IDENTITY |
| snapshots/YYYYMMDD-HHMM__Faz10.5__post-modes.txt | generated | Smoke snapshot after the tile switch, the user's checklist switches and reboot. | VAL-SMOKE, VAL-104-SWITCH, VAL-105-MANUAL, VAL-101-IDENTITY |

## 10. Dependencies and Sequencing

Depends on: `Faz10.2`, `Faz10.3` and `Faz10.4`, all three exited. `Faz10.2` supplies the packaged `setmode.sh` and the measured restart order the guide describes. `Faz10.3` supplies the trap-cleanup bracket the guide and changelog cite. `Faz10.4` supplies the tile, WebUI and Action surfaces, a `build.sh` whose Python step runs under `py -3`, the notes file with the APK certificate digest and key location, and `VAL-104-SWITCH` when that check was still gated at its exit; it also owns the four files whose comment lines this plan edits. The existing release tooling from Faz 9.1 and Faz 9.2 and the smoke script from Faz 2.1 are used as they stand.

Blocks: no further sub-plan. The phase exit waits on this plan, and the ledger rows for `DEC-33` and the AON decision are written by the run that records them.

Required decisions: the AON standing on HyperOS 4, answered by the user from the three choices in `F10.5-07`. The tile versionCode of 12 and the module versionCode of 14 are numbering steps this plan takes, not open questions. `DEC-33` stays closed.

Required infrastructure: the Windows host with Git Bash and `py -3`; the Android build tools and JDK that `tile-app/build.sh` expects; the local `ishtar-cam-modes/tile-app/debug.keystore`, untracked and kept out of every archive, or the key the `Faz10.4` notes name; a writable `%TEMP%`; `platform-tools/adb.exe` used only as `platform-tools/adb.exe -s dc27e5d0`; `ANDROID_SERIAL=dc27e5d0 MSYS_NO_PATHCONV=1` for every script; SukiSU-Ultra `com.sukisu.ultra` v4.3.0-r1 (versionCode 41140) on the phone.

Required human approvals: `VAL-105-MANUAL` — the user approves the push, installs the archive, reboots, answers any dialog, approves the `lang` restore, performs the `VAL-104-SWITCH` taps and every other on-phone check in `F10.5-11`, decides what happens if the signing key is missing or its digest differs, and answers the AON question. The implementer installs nothing and presses nothing on the phone.

Fresh session token and context risk: medium. The edits are text plus one APK rebuild, but there are about twenty sites across eleven files, and the release step overwrites `dist/` and the manifest, so the session needs the version table, the APK md5, the certificate digest, the rollback archive md5 and the release md5 in view until the record is written.

Subagents are not recommended. One writer keeps the version sites in step, and the phone is a single stateful target.

## 11. Risks and Mitigations

- Risk: the guide is written before `Faz10.4` lands. Impact: v2.3 ships with a tile count or Action cycle that is wrong on day one. Mitigation: `F10.5-01` starts only after the three upstream plans exit, and `VAL-105-KULLANIM` checks the guide against that tree.
- Risk: one version site is missed. Impact: the installer, the module list and the archive name disagree, which is the defect this release exists to remove. Mitigation: `VAL-105-VERSIONS` searches every site, including the tile manifest and the generated manifest.
- Risk: the tile manifest gets v2.3 but the packaged APK is the old build. Impact: the phone keeps reporting 2.1, and because the boot-time update check compares md5, an unchanged APK is never reinstalled. Mitigation: `F10.5-06` rebuilds it, `VAL-105-BUILD` compares the packaged APK md5 with the rebuilt one, and `VAL-105-INSTALL` reads versionName 2.3 on the phone.
- Risk: the rebuild signs with a freshly generated or different key. Impact: the update fails with a signature mismatch, and recovering by uninstall drops the root grant. Mitigation: `F10.5-06` uses the same key `Faz10.4` used, stops if it is missing, and `VAL-105-APK` requires the certificate digest recorded by `Faz10.4`.
- Risk: the keystore, its password or the APK leaks into history. Impact: invariant 9 breaks and a signing credential is published. Mitigation: the key stays untracked and kept out of every archive (`.gitignore:19-21`, `build-release.py:96-97`), no file this plan adds or changes records a `KS_PASS=` assignment or a password value, and `VAL-105-APK` checks status and the changed files before handover.
- Risk: the installed-file check expects `customize.sh` on the phone. Impact: a false mismatch triggers a needless rollback. Mitigation: `customize.sh` is checked in the temp archive listing, and the on-phone list leaves it out.
- Risk: the user's `lang` setting is lost by the install. Impact: the module falls back to English without being asked. Mitigation: `F10.5-09` backs it up through `/data/local/tmp`, and `F10.5-10` restores it with md5 and length checks after `VAL-105-INSTALL`.
- Risk: the rollback archive is unknown or gone when needed. Impact: a failed install leaves no verified path back. Mitigation: `F10.5-09` names it with its md5 and `VAL-105-ROLLBACK` keeps it until `F10.5-12`.
- Risk: a comment fix spreads into code in a `Faz10.4` file. Impact: the single-owner rule breaks and a behaviour change ships unreviewed. Mitigation: `VAL-105-COMMENTS` limits the diff to the named lines.
- Risk: a tile tap runs on a stale engine. Impact: the switch restarts the AOSPA provider set or accepts `50mp`. Mitigation: `VAL-104-SWITCH` taps only after the installed `setmode.sh` md5 matches the tree copy.
- Risk: an unquoted `su -c` splits its arguments. Impact: a check reads the wrong thing and records a false result. Mitigation: every root command in this plan and in the rewritten texts is quoted as `su -c '…'`.
- Risk (`DEC-14`, `DEC-33`): new guide text reads as permission to use 50 MP. Impact: a user enables a path that is closed on this ROM, or expects 50 MP from AGC. Mitigation: `F10.5-02` states both closures, keeps the `50mp` versus DCG/LN exclusion and leaves the wide RAW table as it is.
- Risk: AOSPA numbers are presented as HyperOS 4 facts. Impact: users trust timings or crash advice that nobody measured on this ROM. Mitigation: every AOSPA figure is labelled, and HyperOS 4 claims come from a Phase 10 bracket.
- Risk: the bare build runs before the install test. Impact: `dist/` and the manifest describe an archive the phone never ran. Mitigation: `F10.5-08` uses `--out` and `--manifest` in `%TEMP%`, and `F10.5-12` runs the bare command only after the bracket, with equal md5 required.
- Risk: a push or install leaves a partial file. Impact: the module boots from damaged scripts. Mitigation: the push is checked by md5 and length, the installed files are checked against the manifest before any switch, and the named rollback archive is the restore path.
- Risk: the camera stack is restarted in the wrong order during checks. Impact: preview goes black until reboot. Mitigation: switches go through the module only, whose `setmode.sh` from `Faz10.2` stops the client before the HAL and starts the HAL before the client; the implementer issues no direct `stop` or `start`.
- Risk: a snapshot carries an identity value. Impact: an IMEI or serial enters the history. Mitigation: `VAL-101-IDENTITY` runs on each new snapshot before commit.

## 12. Desired End State

`ishtar-cam-modes` v2.3 exists as `dist/ishtar-cam-modes-v2.3.zip`, built by `scripts/build-release.py` and bound by a regenerated `docs/release-manifest.md`. It packages a tile APK rebuilt at version 2.3 whose certificate digest matches the `Faz10.4` build. The same archive was installed by the user on `dc27e5d0` under SukiSU-Ultra, its compared files matched the manifest before any check ran, the user's language setting came back, and a tile tap switched to DCG and back. The guide, installer text, module summary, changelog, README and tile manifest all describe the HyperOS 4 module: sensor modes on, 50 MP closed, SukiSU-Ultra as the manager. The AON standing is recorded with its evidence. The signing key is untracked and kept out of every archive, and its password is written nowhere.

The evidence an implementer should produce is the final stale-statement table, the version search output, the comment diff, the APK badging output and certificate digest, the self-test output and archive listing, the rollback archive md5, the temp and release md5 values, the installed-file md5 comparison, the backup and restore md5 values, the `VAL-104-SWITCH` result, the three new snapshots, and the v2.3 checklist record.

The ledger summary Step 4 should append records: v2.3 released with versionCode 14 and its archive md5, the tile app rebuilt at 2.3 / 12 with an unchanged certificate digest, `VAL-104-SWITCH` closed in the release bracket, `DEC-29` closed by the rewritten guide, the AON decision and its date, `T3` confirmed fixed, and `DEC-33` unchanged.

## 13. Next Sub-Phase Transition Criteria

- `VAL-105-KULLANIM`, `VAL-105-VERSIONS` and `VAL-105-COMMENTS` pass on the host.
- `VAL-105-APK` shows the rebuilt APK at 2.3 / 12 with the certificate digest from the `Faz10.4` notes, untracked.
- `VAL-ASSERT` passes, the temp archive reports v2.3, and its listing holds `customize.sh` with the tree file's md5.
- The rollback archive and the `mode` and `lang` backups were recorded before the push.
- The user installed the temp archive, and `VAL-105-INSTALL` shows `module.prop`, `Kullanim.txt`, `action.sh`, `service.sh`, `setmode.sh` and `tile-app.apk` equal to the manifest, with the tile at versionName 2.3.
- `VAL-105-BACKUP` passes after the restore, and the `/data/local/tmp` copies are gone.
- `VAL-104-SWITCH` passed with its md5 gate open.
- The three `Faz10.5` snapshots exist, pass `VAL-101-IDENTITY`, and older snapshots are unchanged.
- `dist/ishtar-cam-modes-v2.3.zip` has the temp archive's md5, and `VAL-MANIFEST` passes on it.
- `docs/release-checklist.md` holds a v2.3 record with no `pending` row.
- `docs/aon-verification.md` and `README.md` carry the user's AON answer with its date.
- Each of the five Phase 10 acceptance signals points at a committed artifact: the `Faz10.1` notes, the `Faz10.2` and `Faz10.3` bracket snapshots, the `Faz10.4` notes, and this v2.3 checklist record.
