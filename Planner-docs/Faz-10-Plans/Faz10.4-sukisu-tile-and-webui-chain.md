# Faz 10.4 — SukiSU-Ultra Tile and WebUI Chain

## 1. Context

Main-Planing Phase 10 (`SNAP-2026-11-15-MAIN`) adapts `ishtar-cam-modes` to HyperOS 4 and ends with v2.3. This sub-plan owns the user-facing chain: the three Quick Settings tiles, their long press, and the module WebUI page, all of which were written for KernelSU-Next on AOSPA. The phase signal it answers is that a tile switches modes, its long press opens a working WebUI under SukiSU-Ultra, and the system-app idea has a written evaluation.

`DEC-33` (K9 = no) is cited now and recorded in the ledger later: the 50 MP HAL layer is closed on HyperOS 4 while the sensor layer continues. For this plan that means the `50mp` choice leaves every surface a user can touch, not only the engine.

Planning run 21 specified this sub-plan on 2026-11-15, and its Step 2 drafted it on 2026-11-16. `Faz10.1` hands it four questions it did not answer: which launch form the SukiSU-Ultra WebUI accepts from root, how the tile package is registered in the HyperOS panel (the PRB10-class read), what the allowlist count becomes after a grant, and whether a system app is worth a metamodule. `Faz10.2` and `Faz10.3` run beside this plan on paper; on the phone, this plan waits for its turn as section 10 describes. `Faz10.5` waits for it.

Evidence used here is `W3F23`, `W3F24`, `W3F31`, `W3F32`, `W3P01`, `W3P02` and `W3P04`. `W3P01`, `W3P02` and `W3P04` are device reads from 2026-11-15 at 13:01Z. `W3F31` is a source reading of SukiSU-Ultra v4.3.0-r1 that nobody has run on the phone, and this plan treats it as a hypothesis to measure. Results from AOSPA, including the 2026-09-20 tile chain record, are history for this ROM.

## 2. Goal

Make the tiles, the long press and the module WebUI work under SukiSU-Ultra v4.3.0-r1 on HyperOS 4 with no `50mp` choice left in any interface, and write down a reasoned verdict on the system-app idea without installing anything for it.

## 3. Description

The chain breaks at its second link. The long press reaches `WebUiActivity`, which asks `su` to start an activity in `com.rifsxd.ksunext`, a package that is not on this phone. Even with the package corrected, the old call passes the module id as a string extra, and the SukiSU-Ultra source suggests that form makes its WebUI close at once. The handler that does accept `ksu://webui` has a random class name chosen at install, so a fixed component string would break the next time the manager is reinstalled.

The page itself has a smaller fault. `index.html` asks the manager for an edge-to-edge window without telling it whether to enable it, so the call most likely throws and the existing `try` swallows the error. Separately, `50mp` is still offered by the WebUI, by the fourth tile, and by the Action button cycle, while on this ROM nothing behind those controls can deliver it.

Phase 10 is the right home because these are interface changes on top of the measured stack. They need no HAL work, they do not alter the sensor blobs, and they are the part a user notices first after installing the module.

The vibecoding slice strategy: change the launch string and the edge-to-edge argument, drop the `50mp` controls, let the APK build script run on this host, rebuild the tile APK with the key that signed the copy already in the tree, and install one test package. The fastest validation signal is an approved root `am start` from the host with the `-d` form, observed on the screen, followed by a long press on a tile.

What should not be over-planned: a new WebUI design, a second tile app, or a system-app build. The system-app idea is answered on paper, using the measured absence of a metamodule and the release builder's rule set. Installing a metamodule is a separate decision the user would have to take.

Two guards shape the phone half. The first is about order on the single phone: the first project module to boot on HyperOS 4 has to be the unchanged v2.2 that `Faz10.2` observes, so this plan's test package waits for that record and never lands inside another plan's open smoke window. The second is about tile switches: a tap runs the live `setmode.sh`, whose restart list is `Faz10.2`'s to retarget, so no switch happens until the live engine no longer starts the idle virtual-camera provider. Opening the page and reading state are allowed earlier, because they only call `action.sh info` and `lang`.

The module invariants hold throughout. No HAL constant, sensor blob, AGC preference or restart order is touched here, and `50mp` together with DCG or LN is not made reachable by any edit. Installing, granting root, adding tiles and pressing anything on the phone remain the user's acts.

## 4. Scope

- `WebUiActivity.java`: the KernelSU-Next component replaced by a constant root command that finds the `ksu://webui` handler at run time and passes `-d "ksu://webui?id=ishtar_cam_modes"`, with no `--es` extras and no input taken from the incoming Intent.
- One user-approved series of root `am start` attempts from the host, covering the resolved handler, the non-exported `.ui.webui.WebUIActivity` with `-d`, and the old `--es id` form.
- `index.html:337`: `ksu.enableEdgeToEdge` called with an explicit argument, checked on the screen.
- Removing `50mp` and its `50MP` comments from `action.sh` (mode list, cycle, apply branch, output text, tile order, the HAL sourcing comment at `:35`), `index.html` (main list, descriptions, notes, name helper, the suffix comment at `:214`), the tile manifest (`.FullResTile`), `strings.xml`, `BaseTile.java` (including the suffix comment at `:322`), `FullResTile.java` (deleted) and the `service.sh` log text.
- An update path in `action.sh` that drops the panel entry for `.FullResTile` while its component still resolves, before the new APK replaces it.
- User-facing text that names the root manager changed from KernelSU to SukiSU-Ultra in `action.sh` and `service.sh`, outside the lines `Faz10.5` owns.
- `tile-app/build.sh`: the embedded Python step at `:81` made to run on this Windows host, where only the `py -3` launcher works.
- A rebuilt `tile-app.apk` for this plan's changes, signed with the existing local debug key, kept out of version control, with its certificate SHA-256 and key path written to the notes.
- A push of the test zip with md5 and length read back, and a named rollback archive.
- Allowlist and tile-registration reads, counted only, before and after the user grants root.
- A dated notes file covering the launch forms, the registration and allowlist counts, the edge-to-edge result, the signing record and the system-app evaluation.
- Four new snapshot files whose names contain `Faz10.4`.

## 5. Out of Scope

- Version strings and stale comments: `action.sh:7` and `:17`, `service.sh:8-12`, `AndroidManifest.xml:5`, `:11-12` and `:52-54`, `BaseTile.java:17`, `customize.sh:62`, and the tile `versionName`/`versionCode` bump. Those lines belong to `Faz10.5` and are left exactly as they are. None of them is one of the three `50MP` comments this plan removes: `action.sh:7` documents the cycle and `:17` the `info` output.
- Rebuilding `tile-app.apk` after the v2.3 manifest version bump. That rebuild is `Faz10.5`'s.
- Retargeting `restart_camera` or refusing `50mp` inside `setmode.sh`. That is `Faz10.2`.
- AGC trap preferences, any direct write to an AGC preference file, any `sed -i`, any `.agc` import. That is `Faz10.3`.
- Installing a metamodule, adding a `system/` tree to the module, or adding a `system/**` rule to `scripts/build-release.py`.
- Reopening the HAL layer or re-enabling 50 MP. `DEC-33` keeps the HAL layer closed and `DEC-14` still needs new evidence before 50 MP returns to AGC. The wide RAW table is not narrowed, and the exclusion between `50mp` and DCG or LN is not relaxed.
- Any `build.sh` change beyond the Python step, and edits to `res/drawable/ic_camera.xml`, `Hud.java` or `Sh.java`.
- Treating AOSPA observations, such as SystemUI ignoring `remove-tile` for a missing component, as HyperOS 4 facts without a reading on this phone.
- Committing `*.apk`, `*.zip`, `*.keystore`, `*.jks` or `camera.qcom.so`, writing the key password anywhere, or changing any file already in `snapshots/`.

## 6. Current Repository Evidence

`ishtar-cam-modes/tile-app/java/com/ishtar/cammodes/WebUiActivity.java` was read on 2026-11-16. Lines `:14-16` hold one constant: `am start -n com.rifsxd.ksunext/.ui.webui.WebUIActivity` followed by `--es id ishtar_cam_modes` and a `--es name` label. `onCreate` runs it through `Sh.run` on a worker thread and then calls `finish()`. There is no handler lookup and no failure message. Today the command does not read the Intent, and the activity is exported, so any app can trigger that root call.

`Sh.java:16` starts every command as `su -c <string>` and returns trimmed stdout, or an empty string on any exception. The tile chain therefore depends on `com.ishtar.cammodes` holding a root grant; without one every call returns empty, and tiles show the `no_root` subtitle.

`AndroidManifest.xml:35-45` declares `WebUiActivity` as exported, translucent and without history, with the `QS_TILE_PREFERENCES` filter at `:42`. The `.Launcher` alias at `:57-68` targets the same activity, so the drawer icon and the long press share one entry. Four tile services follow; the `.FullResTile` block is `:70-79` and uses `@string/tile_50mp` and `@drawable/ic_camera`. No other component references `ic_camera`.

`BaseTile.java:44-46` lists `FullResTile.class` first in `TILES`, which drives sibling wake-ups. `pretty()` at `:234-235` maps `50mp` to `50MP`, and a comment at `:322` explains the Turkish suffix for `50MP`. `FullResTile.java` is 21 lines whose only behaviour is returning `50mp` and `R.string.tile_50mp`. `res/values/strings.xml:9` defines that string.

`ishtar-cam-modes/action.sh` was read on 2026-11-16. `MODES` at `:30` includes `50mp`. The comment at `:35` labels the `halpatch.sh` sourcing as the 50MP HAL layer. `TILE_ADD_ORDER` at `:43` ends with `FullResTile`, and the comment above it at `:42` describes a four-tile order. `root_granted` at `:56` greps `/data/adb/ksu/.allowlist` quietly. `apply` opens with a `50mp` arm in the `if` at `:116-122`. The cycle steps `ln4f` to `50mp` and `50mp` to `stock` at `:153-154`, and its closing text at `:163-164` mentions 50MP. `tiles order` prints a four-tile order at `:233`, `tiles show` names KernelSU at `:240`, and `tiles status` counts `com.ishtar.cammodes/` entries in `sysui_qs_tiles` at `:254`. The `active` function at `:93-97`, with its comment, reports `50mp` when the HAL state reads `fullres`.

`ishtar-cam-modes/service.sh` was read on 2026-11-16. After `action.sh tiles install` succeeds on a first install, `:42` logs four tiles including 50MP and `:43` tells the user to grant root under KernelSU. Lines `:8-12` describe launcher auto-hiding and are not touched here.

`ishtar-cam-modes/webroot/index.html` was read on 2026-11-16. `MAIN_MODES` at `:187` starts with `50mp`. Both language tables carry a `50mp` description (`:149`, `:177`) and a note that opens with the 50MP exclusion and quotes AOSPA OpenCamera numbers (`:138-141`, `:166-169`). `prettyName` maps `50mp` at `:223`, and the suffix comment at `:214` mentions it. `:337` calls `ksu.enableEdgeToEdge()` with no argument. The body already pads with `env(safe-area-inset-top)` at `:24`, and the viewport sets `viewport-fit=cover` at `:5`.

`ishtar-cam-modes/tile-app/build.sh` compiles with aapt2, javac and d8 from an SDK root given as its argument, signs with `KS=${KS:-$HERE/debug.keystore}` (`:25`), and writes `out/ishtar-cam-tiles.apk`. Its zip step at `:81` pipes a heredoc into `python -`. On this Windows host `python` is the Microsoft Store stub and only `py -3` starts an interpreter, so the script cannot finish here as written. The script warns that a different key cannot update the installed copy. `ishtar-cam-modes/tile-app/debug.keystore` exists in the working tree; `.gitignore` excludes `debug.keystore`, `*.keystore`, `*.jks`, `*.apk` and `ishtar-cam-modes/tile-app/out/`.

`scripts/build-release.py` was read on 2026-11-16. The comment at `:63-66` says a module file that matches no rule fails the build. The `INCLUDE` list from `:67` ships `tile-app.apk` as a prebuilt (`:77`) plus the tile sources (`:82-84`) and has no `system/**` rule. The keystore and `tile-app/out/**` are excluded at `:96-99`.

`ishtar-cam-modes/post-fs-data.sh:72` and `:127` bind-mount the sensor file and the HAL copy directly. The module tree has no `system/` directory, so it never relied on the manager mounting a `system/` overlay.

On 2026-11-15 at 13:01Z the phone resolved `ksu://webui` to `com.sukisu.ultra/.ui.hdhrsdynpwdActivity`, and `.ui.webui.WebUIActivity` did not resolve (`W3P01`). The allowlist file existed with zero hits for `com.ishtar.cammodes`, `/data/adb/metamodule` was absent, and one module of another author bind-mounted into `system/priv-app` by itself (`W3P02`). The HyperOS tile list held no `com.ishtar.cammodes` entry (`W3P04`). The upstream claims that KernelSU v3 and later need a metamodule for `system/` overlays, and that `--es id` closes the SukiSU-Ultra WebUI, come from documentation and source (`W3F31`, `W3F32`) and remain inferences here.

`Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md` was read on 2026-11-16. One of its work items reads the sensor bind and the HAL fail-closed exit after the user boots unchanged published v2.2, and its pre-install snapshot expects no project module on the phone. A later work item of that plan installs a test package with the retargeted `setmode.sh`.

`docs/rom-build-device-notes.md:216-217` records, for AOSPA on 2026-09-20, all four tiles in `sysui_qs_tiles`. `50MP-Entegrasyon-Plani.md:671-677` records, also on AOSPA, a leftover tile entry for a component the APK no longer had, which neither `remove-tile` nor `settings put` could clear. Whether HyperOS 4 behaves the same is unknown.

## 7. Planned Work Breakdown

- F10.4-01 — Gate on the survey record and the manager
  - Description: Read `docs/hyperos4-adaptation-notes.md` and take the manager package, versionCode, `ksu://webui` handler and allowlist path from it. Outside any open `Faz10.2` or `Faz10.3` smoke window, run one PRB1-class read with `platform-tools/adb.exe -s dc27e5d0`. If the manager is not `com.sukisu.ultra` v4.3.0-r1 with versionCode 41140, stop the command list and ask the user; do not adapt the code to another manager on the spot.
  - Output: a go or stop line citing the record date and the fresh read.
- F10.4-02 — Strip the 50mp choice from the module scripts
  - Description: In `action.sh`, remove `50mp` from `MODES`, delete the `50mp` arm in `apply`, make the cycle go from `ln4f` back to `stock`, and drop 50MP from the cycle text, the `tiles order` text and the add-order comment. Reword the `:35` comment so it names the HAL state helpers without `50MP`. `TILE_ADD_ORDER` becomes `Ln2Tile Ln4Tile DcgTile`. Keep the HAL check inside `active` so a leftover `fullres` state is still reported instead of being shown as a sensor mode; that function and its comment are the one named exception. In `service.sh`, the first-install log names three tiles.
  - Output: edited `ishtar-cam-modes/action.sh` and `ishtar-cam-modes/service.sh`.
- F10.4-03 — Clear the old tile entry before the APK update
  - Description: In `action.sh tiles install`, when the package is already present and the module APK differs by md5, run `cmd statusbar remove-tile com.ishtar.cammodes/.FullResTile` before `pm install -r`, while the old component still exists. A fresh install skips this. The step changes only that one panel entry and is idempotent.
  - Output: the update branch in `ishtar-cam-modes/action.sh`.
- F10.4-04 — Remove the fourth tile from the APK sources
  - Description: Delete the `.FullResTile` service block from `AndroidManifest.xml:70-79`, delete `tile_50mp` from `strings.xml`, remove `FullResTile.class` from `TILES`, the `50mp` arm of `pretty()` and the `50MP` line of the suffix comment at `:322` in `BaseTile.java`, and delete `FullResTile.java` in the same change as its manifest entry. The header comment and version lines of the manifest stay for `Faz10.5`.
  - Output: three tile services in the manifest and no source path that can request `50mp`.
- F10.4-05 — Launch the WebUI by URI from root
  - Description: Replace the constant in `WebUiActivity.java` with one compile-time root command, passed as a single argument to `su -c` by `Sh.run`: `c=$(cmd package resolve-activity --brief -a android.intent.action.VIEW -d "ksu://webui?id=ishtar_cam_modes" | tail -n 1); case "$c" in com.sukisu.ultra/*) am start -a android.intent.action.VIEW -n "$c" -d "ksu://webui?id=ishtar_cam_modes" ;; *) exit 1 ;; esac`. If `F10.4-10` shows the direct form opening the page, the `*)` arm runs `am start -a android.intent.action.VIEW -n com.sukisu.ultra/.ui.webui.WebUIActivity -d "ksu://webui?id=ishtar_cam_modes"` instead of exiting. The activity is exported and its command runs as root, so it reads no Intent data, extras or URI, and nothing outside the constant enters the shell string. On an empty or failed launch it shows a short failure line through `Hud` before finishing. Comments that name KernelSU-Next are rewritten for SukiSU-Ultra.
  - Output: edited `ishtar-cam-modes/tile-app/java/com/ishtar/cammodes/WebUiActivity.java`.
- F10.4-06 — Fix the page call and the page text
  - Description: In `index.html`, call `ksu.enableEdgeToEdge(true)` inside the existing `try`, remove `50mp` from `MAIN_MODES`, from both `modes` tables and from `prettyName`, drop the `50MP` line of the suffix comment at `:214`, and rewrite both notes so they warn only about DCG/LN and video without AOSPA 50MP figures. If `F10.4-11` shows the header under the status bar, remove the call instead of inventing inset variables, and record that outcome.
  - Output: edited `ishtar-cam-modes/webroot/index.html`.
- F10.4-07 — Name the right manager in user text
  - Description: Change the `tiles show` message at `action.sh:240` and the root reminder at `service.sh:43` to point at SukiSU-Ultra's Superuser list. Do not touch the comment blocks that `Faz10.5` owns.
  - Output: two text lines updated.
- F10.4-08 — Let the build script's Python step run on this host
  - Description: In `tile-app/build.sh`, replace the bare `python -` call at `:81` with an interpreter choice made once near the top: `py -3` when the `py` launcher is on `PATH`, otherwise `python3`, and a clear error naming both when neither exists. The heredoc body and its arguments stay as they are. No other line of the script changes, and the signing defaults are not touched.
  - Output: edited `ishtar-cam-modes/tile-app/build.sh`.
- F10.4-09 — Rebuild the tile APK and a temporary module
  - Description: Record the SHA-256 certificate digest of the current untracked `ishtar-cam-modes/tile-app.apk` with `apksigner verify --print-certs` before anything is rebuilt. Run `tile-app/build.sh <SDK root>` in Git Bash with the default key `ishtar-cam-modes/tile-app/debug.keystore` (`build.sh:25`, untracked and excluded from every archive); if that key is missing, stop, because a new key cannot update the installed app and would need an uninstall that drops the root grant. Confirm the zip step printed its `classes.dex` line, the new certificate SHA-256 equals the old one, and the aapt2 manifest dump is as expected, then copy `out/ishtar-cam-tiles.apk` over `ishtar-cam-modes/tile-app.apk`. Write the certificate SHA-256 and the key path into the notes, never the password, so `Faz10.5` can compare its post-bump rebuild against them. Build the test module with `py -3 scripts/build-release.py --out "$TEMP/ishtar-cam-modes-faz104.zip" --manifest "$TEMP/ishtar-cam-modes-faz104.md"`. Record the md5 of the zip and of its packaged `setmode.sh` and `post-fs-data.sh`, read with `py -3 -c "import hashlib,sys,zipfile; z=zipfile.ZipFile(sys.argv[1]); [print(n, hashlib.md5(z.read(n)).hexdigest()) for n in ('setmode.sh','post-fs-data.sh')]" "$TEMP/ishtar-cam-modes-faz104.zip"`, so the engine inside the package is attributable. `git status` must list no `.apk`, `.zip` or keystore, and `dist/` plus `docs/release-manifest.md` stay unchanged.
  - Output: the rebuilt untracked `tile-app.apk`, its md5 and certificate SHA-256, a temp zip outside the repository, and the md5 of the zip and its two packaged scripts.
- F10.4-10 — Push, install, reboot, compare, then probe the launch forms
  - Description: Start only inside the device window of section 10. Record which archive is installed now and its md5 from the host copy, either `dist/ishtar-cam-modes-v2.2.zip` or the `Faz10.2` test zip that plan recorded, and confirm it by comparing the live `module.prop` version and live `setmode.sh` md5 with that archive's packaged copies; that host archive is the reinstall target and is kept until the closing snapshot. If no host archive's packaged copies match the installed module, stop and ask the user before any push. Run `ANDROID_SERIAL=dc27e5d0 MSYS_NO_PATHCONV=1 scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.4__pre-install`. From now until the test zip's reboot, the recorded archive stays installed and nobody presses the Action button, opens the WebUI or calls `setmode.sh`. Back up the tile list on the phone with `platform-tools/adb.exe -s dc27e5d0 shell "su -c 'settings get secure sysui_qs_tiles > /data/local/tmp/faz104-qs-tiles.txt'"`, then read only `su -c 'md5sum /data/local/tmp/faz104-qs-tiles.txt; wc -c < /data/local/tmp/faz104-qs-tiles.txt'`; the value is never printed or pulled. Push with `platform-tools/adb.exe -s dc27e5d0 push "$TEMP/ishtar-cam-modes-faz104.zip" /sdcard/Download/ishtar-cam-modes-faz104.zip` and read back `platform-tools/adb.exe -s dc27e5d0 shell "md5sum /sdcard/Download/ishtar-cam-modes-faz104.zip; stat -c %s /sdcard/Download/ishtar-cam-modes-faz104.zip"`. On a mismatch delete the pushed file, push once more and re-check; a second mismatch stops the plan. The user installs that file in SukiSU-Ultra and reboots. Take `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.4__post-reboot` the same way. Compare the live md5 of `action.sh`, `service.sh`, `webroot/index.html` and `tile-app.apk`, each read as `su -c 'md5sum /data/adb/modules/ishtar_cam_modes/<file>'`, and of the installed APK path, with the host files; any mismatch stops the plan and the user reinstalls the recorded archive. Then, one approved command at a time, the user watches four root launches: the resolved handler with `-d`, the read-only lookup itself, the direct form `platform-tools/adb.exe -s dc27e5d0 shell "su -c 'am start -a android.intent.action.VIEW -n com.sukisu.ultra/.ui.webui.WebUIActivity -d \"ksu://webui?id=ishtar_cam_modes\"'"`, and the same component with `--es id ishtar_cam_modes` instead of `-d`. Each outcome is written down as opened, closed at once, or refused.
  - Output: the rollback archive name and md5, the push read-back, two snapshots, the md5 table, and four recorded launch outcomes.
- F10.4-11 — Read registration and allowlist, grant, long press
  - Description: Run `platform-tools/adb.exe -s dc27e5d0 shell "su -c 'sh /data/adb/modules/ishtar_cam_modes/action.sh tiles status'"` and record `kok_kaydi` and the `kutucuk` count, plus `su -c 'settings get secure sysui_qs_tiles | grep -o "com.ishtar.cammodes/.FullResTile" | wc -l'`; nothing else from either source is printed. The user grants root to "IMX989 Camera Modes" in SukiSU-Ultra's Superuser list and notes whether the app appeared there. Read the status again. If the panel holds no project tile, the user adds the three from the HyperOS control-center editor. The user then long-presses a tile and taps the drawer icon, and reports whether the module page opened, whether `action.sh info` filled the active-mode line, and whether the header clears the status bar. If the tile list lost any non-project entry, restore it with `platform-tools/adb.exe -s dc27e5d0 shell "su -c 'settings put secure sysui_qs_tiles \"\$(cat /data/local/tmp/faz104-qs-tiles.txt)\"'"`, whose quoting keeps the parentheses and commas intact, then write a fresh read to `/data/local/tmp/faz104-qs-tiles-check.txt` and compare its md5 and length with the backup. If they differ, keep both files, stop, and tell the user where they are. Take `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.4__post-chain` afterwards.
  - Output: before-and-after counts, the user's observations, any restore result, and the post-chain snapshot.
- F10.4-12 — Switch modes from the tile, behind the engine gate
  - Description: Run `VAL-104-SWITCH` as defined in section 9. If its gate is closed, record that and run no switch. Then take `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.4__closing`. After a verified restore, or after this closing snapshot when no restore was needed, delete the device copies with `platform-tools/adb.exe -s dc27e5d0 shell "su -c 'rm -f /data/local/tmp/faz104-qs-tiles.txt /data/local/tmp/faz104-qs-tiles-check.txt'"`, and delete `/sdcard/Download/ishtar-cam-modes-faz104.zip` the same way.
  - Output: a gate line, the switch observations when the gate was open, the closing snapshot, and the device temp files removed.
- F10.4-13 — Evaluate the system-app idea on paper
  - Description: Write the evaluation into the notes. Facts: no metamodule on 2026-11-15, no `system/` tree in this module, no `system/**` rule in the release builder, so a packaged `system/priv-app` tree would fail the build today. Inferences, labelled: a module `system/` overlay needs a metamodule under KernelSU v3 and later; a self bind-mount like the other module's would need a `post-fs-data.sh` change this plan does not own; a privileged app may need a permissions allowlist; a system copy still needs a root grant for `su`. Close with a recommendation and the decision the user would need to take. Nothing is installed.
  - Output: the evaluation section in `docs/hyperos4-tile-webui-notes.md`.
- F10.4-14 — Write the dated notes
  - Description: `docs/hyperos4-tile-webui-notes.md` gives each fact its UTC date: launch outcomes, handler name at that date, allowlist and registration counts, edge-to-edge result, APK md5, the signing certificate SHA-256 and the key path used, the rollback archive, the engine gate state, and the system-app section. Inferences are marked. No key password, allowlist content, identity value or tile list string appears in it.
  - Output: `docs/hyperos4-tile-webui-notes.md`.

## 8. Acceptance Criteria

- No interface surface offers `50mp`: the WebUI lists, the tile manifest, the string table, `TILES`, the `action.sh` mode list and cycle, and both log or output texts.
- The only `50mp` or `50MP` tokens left in this plan's files are inside the `active` function of `action.sh` and its comment, and the reason is stated in the notes.
- `FullResTile.java` no longer exists, and its manifest service block is gone with it.
- `WebUiActivity.java` contains no `com.rifsxd.ksunext` and no `--es`, resolves the handler at run time, accepts only a `com.sukisu.ultra/` component, double-quotes it in `am start -n "$c"`, and builds its root command from a constant without reading the Intent.
- `tile-app/build.sh` has no bare `python` call, and a full run on this Windows host completes its zip step through `py -3`.
- The test package was installed only after `Faz10.2` recorded the unchanged v2.2 boot, and outside any open `Faz10.2` or `Faz10.3` smoke window.
- The pushed zip matched the host md5 and length before the user installed it, and the rollback archive is named with its md5.
- The four root launch outcomes are recorded, and the fallback in the code matches the form that actually opened the page.
- A long press on a tile and a tap on the drawer icon both open the module page under SukiSU-Ultra, and the page shows the active mode.
- `index.html` passes an explicit argument to `ksu.enableEdgeToEdge`, or omits the call, according to the on-screen result.
- The rebuilt APK carries three tile services, is signed by the same certificate as the previous build, is not tracked, and its certificate SHA-256 and key path are in the notes.
- After the update, the HyperOS tile list holds no `.FullResTile` entry, or the notes record that SystemUI kept one and that it is not drawn.
- The allowlist count for `com.ishtar.cammodes` rose from zero after the user's grant, and only the count was read.
- The tile switch was observed with the engine gate open, or the notes record that the gate was closed and no switch ran.
- No `faz104` file remains in `/data/local/tmp` or `/sdcard/Download` after the closing snapshot, unless an unverified restore made the plan stop.
- The system-app evaluation exists with facts and inferences separated, and no metamodule or system app was installed.
- `dist/`, `docs/release-manifest.md`, the version lines that `Faz10.5` owns and every existing snapshot are unchanged.

## 9. Validation and Test Approach

Validation pairs host checks on the sources and the built APK with one install observed on the phone. Every device step sits between two smoke snapshots, every root command is quoted as one argument to `su -c`, and every reading of the allowlist or tile list is a count.

- `VAL-SMOKE` (from Faz 2.1) — `scripts/smoke.sh -o YYYYMMDD-HHMM__Faz10.4__<label>` with `ANDROID_SERIAL=dc27e5d0 MSYS_NO_PATHCONV=1`; the name has no `snapshots/` prefix because the script adds it, and comparable regions are diffed.
- `VAL-101-IDENTITY` (from Faz 10.1) — run on each new `Faz10.4` snapshot and on the notes file before commit; a hit stops the commit, and the snapshot serial line must read `dc27e5d0`.
- `VAL-CONTENTS` (from Faz 9.1) — the temp module build classifies every module file, and its entry list shows the new `tile-app.apk` and no `FullResTile.java`.
- `VAL-104-SURFACE` (proposed) — a host grep over this plan's seven remaining Java, XML, shell and HTML sources finds no `50mp`, `50MP`, `FullResTile` or `com.rifsxd.ksunext`, except inside the `active` function of `action.sh` and its comment, and `FullResTile.java` no longer exists; a read of `WebUiActivity.java` confirms no `getIntent`, `getData` or extras call.
- `VAL-104-BUILD` (proposed) — a host grep of `tile-app/build.sh` finds no bare `python` command, and one full run in Git Bash on this host prints the `classes.dex` line of the zip step and ends with the signed APK.
- `VAL-104-APK` (proposed) — aapt2 manifest dump of the rebuilt APK shows `com.ishtar.cammodes` with `DcgTile`, `Ln4Tile` and `Ln2Tile` only; `apksigner verify --print-certs` gives the same certificate SHA-256 as the build it replaces, and that digest and the key path are in the notes; `git status` lists no `.apk` or keystore.
- `VAL-104-PUSH` (proposed) — before the push, the installed archive is named with its md5; after the push, the md5 and length read back from `/sdcard/Download/ishtar-cam-modes-faz104.zip` equal the host zip, with one delete-and-repush allowed before a stop; the packaged `setmode.sh` and `post-fs-data.sh` md5 are recorded.
- `VAL-104-LIVE` (proposed) — after the user's reboot and before any action, live md5 of the four module files and the installed APK path, each read through a quoted `su -c 'md5sum …'`, equal the host files.
- `VAL-104-REG` (proposed) — `action.sh tiles status` before and after the grant, plus the `.FullResTile` count, all through `platform-tools/adb.exe -s dc27e5d0 shell "su -c '…'"`; only counts and status words are recorded, and the tile-list backup is compared by md5 and length if a restore ran.
- `VAL-104-LAUNCH` (proposed) — the four approved root launches, each with the user's on-screen outcome, and the resolved handler compared with the `W3P01` reading.
- `VAL-104-LONGPRESS` (proposed) — long press and drawer icon both open the module page, the active-mode line fills, and the header position is recorded.
- `VAL-104-SWITCH` (proposed) — gate first. On the host, the tree copy `ishtar-cam-modes/setmode.sh` must start `vendor.camera-provider` and `vendor.camera-provider-2-7-ext-uvc` in `restart_camera`, and the bare `vendor.camera-provider-2-7-ext` must never be started: every hit of `grep -nE 'vendor\.camera-provider-2-7-ext($|[^-])' ishtar-cam-modes/setmode.sh` is read and must be a stop or a comment, because a plain substring search also matches `-ext-uvc`. Then `platform-tools/adb.exe -s dc27e5d0 shell "su -c 'md5sum /data/adb/modules/ishtar_cam_modes/setmode.sh'"` must equal the md5 of that tree copy. If either check fails, the gate is closed and no tile is tapped. With the gate open, the user taps the DCG tile, waits for the ready line, opens the camera and sees a preview, taps DCG again to return to stock, and confirms the tile highlight follows; `su -c 'sh /data/adb/modules/ishtar_cam_modes/action.sh get'` reads `dcgB` and then `stock`, and `platform-tools/adb.exe -s dc27e5d0 shell "getprop init.svc.vendor.camera-provider-2-7-ext"` is not `running` after the return.
- `VAL-104-SYSAPP` (proposed) — the notes hold the system-app evaluation with dated facts and labelled inferences, and a read after the run shows no metamodule directory and no new package.
- `VAL-104-NOTES` (proposed) — every fact in the notes has a UTC date, every inference is marked, and no key password, identity value or allowlist content appears.
- `VAL-104-MANUAL` (proposed) — the user approves and performs the install, the reboot, each root launch, the root grant, any tile addition, the long press, the drawer tap, any reinstall of the rollback archive and, if the gate is open, the switch; the user also handles any permission dialog.

Local versus live: the greps, the build run, the APK dump, the certificate comparison, the zip md5 values and the temp build are local. Push read-back, install, launches, counts, long press and switch are live on `dc27e5d0`. Security validation is the constant root command, the certificate check, the untracked APK and key, the deleted device copies, and count-only reads. Artifact validation is the APK md5, the push read-back and the temp archive listing.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/action.sh | modified | Drops `50mp` from the mode list, cycle, apply, texts and the `:35` comment, adds the pre-update tile removal, and names SukiSU-Ultra in the grant hint. | VAL-104-SURFACE, VAL-104-REG, VAL-104-LIVE |
| ishtar-cam-modes/service.sh | modified | First-install log names three tiles and points the root grant at SukiSU-Ultra. | VAL-104-SURFACE, VAL-104-LIVE |
| ishtar-cam-modes/webroot/index.html | modified | Removes the `50mp` control, texts and suffix comment and passes an explicit edge-to-edge argument. | VAL-104-SURFACE, VAL-104-LONGPRESS, VAL-104-LIVE |
| ishtar-cam-modes/tile-app/AndroidManifest.xml | modified | Loses the `.FullResTile` service block; header comment and version lines stay for `Faz10.5`. | VAL-104-SURFACE, VAL-104-APK |
| ishtar-cam-modes/tile-app/res/values/strings.xml | modified | Loses the `tile_50mp` string. | VAL-104-SURFACE, VAL-104-APK |
| ishtar-cam-modes/tile-app/build.sh | modified | The embedded Python step at `:81` runs through `py -3` on this Windows host instead of the bare `python` Store stub. | VAL-104-BUILD, VAL-104-APK |
| ishtar-cam-modes/tile-app/java/com/ishtar/cammodes/WebUiActivity.java | modified | Runs one constant root command that resolves the `ksu://webui` handler and starts it with the `-d` URI, reading nothing from the Intent. | VAL-104-SURFACE, VAL-104-LAUNCH, VAL-104-LONGPRESS |
| ishtar-cam-modes/tile-app/java/com/ishtar/cammodes/FullResTile.java | modified | The file is deleted together with its `.FullResTile` manifest entry, so no tile can request `50mp`. | VAL-104-SURFACE, VAL-CONTENTS |
| ishtar-cam-modes/tile-app/java/com/ishtar/cammodes/BaseTile.java | modified | `TILES`, `pretty()` and the `:322` suffix comment lose the 50MP tile; line 17 stays for `Faz10.5`. | VAL-104-SURFACE, VAL-104-APK |
| ishtar-cam-modes/tile-app.apk | generated | Rebuilt for this plan's changes with three tiles and the same signing certificate, untracked; the rebuild after the v2.3 version bump is `Faz10.5`'s. | VAL-104-BUILD, VAL-104-APK, VAL-104-LIVE, VAL-CONTENTS |
| docs/hyperos4-tile-webui-notes.md | proposed | Dated record of launch forms, counts, edge-to-edge result, signing certificate SHA-256 and key path, rollback archive, engine gate and the system-app evaluation. | VAL-104-NOTES, VAL-104-SYSAPP, VAL-104-APK, VAL-101-IDENTITY |
| ishtar-cam-modes/tile-app/java/com/ishtar/cammodes/Sh.java | existing | Read-only: the `su -c` helper every tile and launch call goes through. | VAL-104-LAUNCH |
| ishtar-cam-modes/setmode.sh | existing | Read-only: its tree copy and live md5 form the engine gate for tile switches, and its packaged md5 is recorded; owned by `Faz10.2`. | VAL-104-SWITCH, VAL-104-PUSH |
| ishtar-cam-modes/post-fs-data.sh | existing | Read-only evidence that the module bind-mounts its own files and has no `system/` tree; its packaged md5 is recorded. | VAL-104-SYSAPP, VAL-104-PUSH |
| scripts/build-release.py | existing | Read-only: temp build with `--out` and `--manifest` under `$TEMP`, and the rule set the system-app idea is judged against. | VAL-CONTENTS, VAL-104-SYSAPP |
| scripts/smoke.sh | existing | Read-only bracket tool, run with the pinned serial. | VAL-SMOKE |
| docs/hyperos4-adaptation-notes.md | existing | The `Faz10.1` record this plan's gate reads. | VAL-104-LAUNCH, VAL-104-REG |
| Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md | existing | Read-only: its work item that records the first unchanged v2.2 boot opens this plan's device window. | VAL-104-PUSH |
| dist/ishtar-cam-modes-v2.2.zip | existing | Read-only: a possible rollback archive, named with its md5 when it is the installed one; never rebuilt here. | VAL-104-PUSH, VAL-104-MANUAL |
| docs/release-manifest.md | existing | Must stay unchanged; the temp build writes its manifest to `$TEMP`. | VAL-CONTENTS |
| snapshots/YYYYMMDD-HHMM__Faz10.4__pre-install.txt | generated | Smoke state before the test package is installed. | VAL-SMOKE, VAL-101-IDENTITY, VAL-104-PUSH |
| snapshots/YYYYMMDD-HHMM__Faz10.4__post-reboot.txt | generated | Smoke state after the user's install and reboot. | VAL-SMOKE, VAL-101-IDENTITY, VAL-104-LIVE |
| snapshots/YYYYMMDD-HHMM__Faz10.4__post-chain.txt | generated | Smoke state after the launches, the grant and the long press. | VAL-SMOKE, VAL-101-IDENTITY, VAL-104-LONGPRESS |
| snapshots/YYYYMMDD-HHMM__Faz10.4__closing.txt | generated | Closing smoke state after the gated switch check. | VAL-SMOKE, VAL-101-IDENTITY, VAL-104-SWITCH |

## 10. Dependencies and Sequencing

Depends on: `Faz10.1` for the dated manager, handler, allowlist and mount record. This plan reads that record first and stops if the live manager differs from it.

Blocks: `Faz10.5`. The v2.3 package carries this plan's scripts, page and APK sources, and `Faz10.5` rebuilds `tile-app.apk` after its version bump with the build script fixed here, checking the result against the certificate SHA-256 and key path recorded in the notes. Its release notes can only claim a working long press after this plan's notes exist. The tile switch is gated on the live engine rather than on another plan: when the retargeted `setmode.sh` is not yet live, `Faz10.5` borrows `VAL-104-SWITCH` for its post-install bracket.

Device window: the paper work in `F10.4-02` through `F10.4-09` and `F10.4-13` runs in parallel with the sibling plans. The phone steps from the push in `F10.4-10` onward start only after the `Faz10.2` work item that reads the guards on the first boot has recorded unchanged published v2.2 booting on HyperOS 4, so this plan's test package is never the first project module that phone boots. They also never start, and never resume, while a `Faz10.2` or `Faz10.3` before-and-after smoke window is open, meaning from that plan's opening snapshot to its closing one. If the window is not free, the phone half waits; the dependency line above does not change.

Required decisions: none new. `DEC-33` and `DEC-14` stay as they are. The system-app question ends in a recommendation; adopting it would need a new user decision and a later plan, and this plan does not take it.

Required infrastructure: the Windows host with Git Bash and the `py -3` launcher, `platform-tools/adb.exe` used as `platform-tools/adb.exe -s dc27e5d0`, scripts run with `ANDROID_SERIAL=dc27e5d0 MSYS_NO_PATHCONV=1`, the Android SDK root that `tile-app/build.sh` expects outside the repository, and a writable `$TEMP`. The only credential is the default `ishtar-cam-modes/tile-app/debug.keystore`, which stays untracked and out of every archive; its password is never written down.

Required human approvals: `VAL-104-MANUAL`. The user approves and performs the test package install and reboot, any reinstall of the recorded rollback archive, each of the four root launches, the root grant in SukiSU-Ultra, any tile addition in the control-center editor, the long press, the drawer tap and, only with the engine gate open, the DCG switch and return. If the manager is not `com.sukisu.ultra` v4.3.0-r1 (versionCode 41140), the command list stops and the user decides.

Fresh session token and context risk: medium. The edits are small, but they span Java, XML, shell and HTML, and the device half needs the launch outcomes and counts kept together until the notes are written. A second session risk is the shared phone: a session that skips the device-window check could boot this package before the v2.2 record or inside a sibling's bracket, so the session confirms the `Faz10.2` record of the first unchanged v2.2 boot and the absence of an open sibling window before the push and writes that check into the notes.

Subagents are not recommended. One phone, one SystemUI tile list and one signing key make a second writer a source of unattributable state.

## 11. Risks and Mitigations

- Risk: the test package boots before `Faz10.2` has observed unchanged v2.2, or lands inside a sibling's smoke window. Impact: `Faz10.2` loses its clean first boot, or another plan's before-and-after diff includes this plan's install. Mitigation: the device window in section 10 gates the push, and the packaged `setmode.sh` and `post-fs-data.sh` md5 are recorded so any boot stays attributable.
- Risk: the zip arrives on the phone damaged. Impact: the user installs a package that differs from the reviewed tree. Mitigation: `VAL-104-PUSH` compares md5 and length after the push, allows one re-push, and names the archive to reinstall on a later mismatch.
- Risk: the handler name is hard-coded from the 2026-11-15 read. Impact: the long press stops working after any reinstall of the manager. Mitigation: `F10.4-05` resolves the handler at every launch, and `VAL-104-SURFACE` rejects a fixed random class name.
- Risk: the exported activity passes caller data into its root command. Impact: any installed app could run commands as root through the tile app. Mitigation: `F10.4-05` keeps the command a constant and reads nothing from the Intent, and `VAL-104-SURFACE` checks for Intent reads.
- Risk: the `--es id` form is kept because it once worked on KernelSU-Next. Impact: SukiSU-Ultra opens and closes its WebUI with no page. Mitigation: `F10.4-10` measures that form beside the `-d` forms, and only a form seen opening the page stays in the code.
- Risk: a tap on a tile or a WebUI mode button runs a live `setmode.sh` that still starts the idle ext provider. Impact: an init service the ROM leaves stopped starts, and the camera stack is restarted in an unmeasured order. Mitigation: `VAL-104-SWITCH` checks the start set with an exact-token match and the live md5 first, and no switch runs while the gate is closed.
- Risk: the build script still reaches the Store stub, or its fix changes more than the interpreter choice. Impact: the zip step silently produces no `classes.dex`, or signing behaviour drifts. Mitigation: `F10.4-08` limits the edit to the Python call, and `VAL-104-BUILD` requires the `classes.dex` line and a signed APK from a full run.
- Risk: the APK is rebuilt with a fresh key, now or in the v2.3 rebuild. Impact: `pm install -r` fails on the installed copy, and an uninstall to recover drops the root grant. Mitigation: `F10.4-09` compares the certificate SHA-256 before and after, stops if the key is missing, and records the digest and key path for `Faz10.5`.
- Risk: removing the service leaves a panel entry SystemUI cannot clear, as happened on AOSPA. Impact: a stale entry stays in the tile list. Mitigation: `F10.4-03` removes the entry while the old component still resolves, and `VAL-104-REG` counts it after the update.
- Risk: the tile-list restore writes a mangled string, or SystemUI ignores it as it did on AOSPA. Impact: the user's other control-center tiles are lost. Mitigation: the backup stays on the phone, the restore command quotes the value as one argument, a fresh read is compared by md5 and length, and a mismatch stops the run with both files kept for the user.
- Risk: allowlist or tile list content leaks into the notes, a snapshot or a leftover device file. Impact: package names of other apps leave their place. Mitigation: `VAL-104-REG` records counts and status words only, `VAL-101-IDENTITY` scans every new file, and `F10.4-12` deletes the device copies.
- Risk (`DEC-33`, `DEC-14`): the `active` HAL report is read as a remaining 50MP feature. Impact: someone restores a 50MP control. Mitigation: the notes state that the token only reports a leftover state, and no interface can request it.
- Risk: the edge-to-edge argument is right but the page has no usable insets on HyperOS. Impact: the header sits under the status bar. Mitigation: `F10.4-06` drops the call when the screen shows that, rather than guessing inset variables.
- Risk: AOSPA tile behaviour is assumed for HyperOS 4. Impact: the plan claims registration or long-press results nobody saw on this ROM. Mitigation: every such result in the notes carries a HyperOS 4 date or is marked as an inference.
- Risk: the default `build-release.py` run is used for the test package. Impact: `dist/` and `docs/release-manifest.md` are rewritten, and a zip may be committed. Mitigation: `F10.4-09` passes `--out` and `--manifest` under `$TEMP`, and `git status` must show no archive.

## 12. Desired End State

The tile app has three tiles and a long press that reaches the module page through SukiSU-Ultra, using a constant root command that looks up the handler each time and takes nothing from its caller. The page asks for an edge-to-edge window correctly and offers no 50MP control, and neither does the Action button. The tile build script runs on this host through `py -3`. The rebuilt APK is signed by the existing untracked key, whose certificate SHA-256 and path are on record, and it is never committed; `Faz10.5` rebuilds it once more after the v2.3 version bump. A notes file records, with dates, which launch forms opened the page, how the allowlist and tile counts changed, which archive was the rollback, whether a tile switch was observed, and why a system app is or is not worth a metamodule. No `faz104` temp file is left on the phone.

The evidence an implementer should produce is the source diff, the build log with its `classes.dex` line, the APK manifest dump and certificate comparison, the zip and packaged-script md5 values, the push read-back, the device-window check, the live md5 table, the four launch outcomes, the before-and-after counts, the user's long-press and drawer observations, the gate line with any switch observation, the notes file, and four new `Faz10.4` snapshots.

The ledger summary Step 4 should append records: SukiSU-Ultra launch form measured on `dc27e5d0`, `50mp` removed from every interface under `DEC-33`, the build script made host-runnable, the signing certificate SHA-256 recorded, allowlist grant counted, system-app idea evaluated without installation, and the state of the engine gate.

## 13. Next Sub-Phase Transition Criteria

- `VAL-104-SURFACE` finds no `50mp`, `50MP`, `FullResTile` or `com.rifsxd.ksunext` outside the `active` function and its comment, and no Intent read in `WebUiActivity.java`.
- `VAL-104-BUILD` shows a full host build through `py -3` with no bare `python` left in the script.
- `VAL-104-APK` shows three tile services and an unchanged signing certificate, the APK is untracked, and the notes hold the certificate SHA-256 and key path.
- `VAL-104-PUSH` shows the device-window check, the rollback archive with its md5, and a matching push read-back.
- `VAL-104-LIVE` matched before any action on the phone.
- `VAL-104-LAUNCH` and `VAL-104-LONGPRESS` show the module page opening from the long press and from the drawer.
- `VAL-104-REG` shows a nonzero allowlist count after the grant and no `.FullResTile` entry, or a recorded undrawn leftover.
- `VAL-104-SWITCH` either passed with the gate open or is recorded as gated, so `Faz10.5` knows whether its post-install bracket must run it.
- No `faz104` file remains on the phone, unless a stopped restore left them for the user.
- `docs/hyperos4-tile-webui-notes.md` passes `VAL-104-NOTES` and `VAL-104-SYSAPP`.
- Four new `Faz10.4` snapshots pass `VAL-101-IDENTITY`, and no existing snapshot changed.
