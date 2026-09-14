# Faz 7.2 — First AOSPA beryl Build on a Rented VDS

## 1. Context

Main-Planing Phase 7 (`SNAP-2026-09-10-MAIN`) sets the desired end state: "One AOSPA `beryl` build for `ishtar` completed on a rented VDS from inputs staged on GitHub, with the output retrieved and the server released." Its acceptance signal reads "A flashable build output exists and boots; the rental time the build consumed is recorded." This sub-phase is the paid half of that. It rents, builds, retrieves, and releases. The boot half belongs to `Faz7.3`, because flashing is the user's action on a daily device and happens after the server is gone.

**Amended 2026-09-13 by planning run 19 (bounded Step 2 amendment: `IMPL-91` reconciliation, `AUDIT-FIX-43`, `AUDIT-FIX-44`).** Run 18 wrote this file on 2026-09-10, before `Faz7.1` ran. `IMPL-91` then verified `Faz7.1` and wrote `docs/build-environment.md`, the rental runbook this session executes. The user also answered `DEC-22` and `DEC-25`. Four premises of the earlier text are gone:

- Manifest `4182695` and its seven open items. The manifest is now `22283d8`, with every item closed or deferred with a detector.
- A private device tree and a read-only server credential. Both repositories are public under `DEC-25`, and the server holds no GitHub credential.
- A teardown whose delete-versus-power-off question pointed at a billing page nobody had read. Runbook section 3 now reads it.
- A retrieval list reading only "the flashable package". Runbook section 11 now names every artifact the install methods consume.

**The runbook is the operative procedure.** Every value below was re-read from it, and from `ahmetxa/android_local_manifests` at `22283d8`, on 2026-09-13. Where this file and the runbook disagree, Step 4 follows the runbook and records the disagreement.

Two points go beyond that, and the user ruled on both on 2026-09-13:

- **The symlink check.** Runbook section 10 tests whether `odm/lib64/camera/aon_front.pb` is a symlink. The measured entry `odm/lib64/camera/aon_front.pb;SYMLINK=vendor/lib64/camera/aon_front.pb` creates the symlink at the `vendor` path instead. `F7.2-01` corrects that line before renting.
- **Where fixes land.** The earlier rule said an input fix lands on GitHub before the retry. The runbook's rule replaces it: fixes are made on the server, recorded in `fixes.diff`, and landed on GitHub after the session.

No work item was added or removed.

**Re-planned 2026-09-10 by planning run 18.** The previous version of this file planned a sync "inside the Linux filesystem" of a WSL2 host that `DEC-24` retired, and it excluded "any beryl work" while its own goal was an Android 16 build from the `beryl` trees — the contradiction ledger section 7 recorded. Both premises are gone. The path is unchanged so that existing references still resolve: `docs/aon-verification.md` section 7 and `Faz6.2`'s `F6.2-05` both name this file.

Two registrations converge here. `Faz6.2` registered the AON verification against Phase 7. Its procedure's step 1 — "confirm the entry is in the tree the build actually consumed" — can only run where the consumed tree exists, which is the server, so it is executed here before teardown. The device-side steps run in `Faz7.3`. That discharges `FIND-6.2-01`'s cross-reference: `F6.2-05` asked that the procedure be "referenced from `Faz7.2`", and a Step 4 session could not add the reference itself. `Faz8.1` likewise needs the md5 of the guarded camera blobs as actually built, which only this session can read cheaply.

Ledger section 7 lists this sub-phase's outcome as a replanning trigger: a result showing "the Android 16 track is not viable … removes the precondition" for Phase 8.

## 2. Goal

In one bounded paid session, run `docs/build-environment.md` against the inputs `Faz7.1` staged and turn them into a retrieved, sha256-verified set of `ishtar` install artifacts. Capture before teardown the evidence `Faz7.3` and `Faz8.1` need. Finish with the server and its Primary IP deleted, no credential ever placed on it, and the elapsed hours recorded against the `DEC-25` ceiling of 10 hours.

## 3. Description

The problem is that the Android 16 track has never produced an artifact. The trees are staged and pinned, but nothing has compiled from them, and every day the project owns a pinned manifest without a build is a day the pins can only be trusted on paper.

It belongs after `Faz7.1`, which is `verified` (`IMPL-91`): the manifest is buildable, `DEC-22` and `DEC-25` are answered, and the runbook exists. It belongs before `Faz7.3` because a flash needs an output.

The vibecoding slice strategy follows the runbook's own order, cheapest failure surface first:

1. The free pre-rental checks (section 5).
2. Provisioning and server setup (sections 6 and 7).
3. The sync with its base-pin assertion (section 8).
4. The build (section 9).

The fastest useful signal is a completed `repo sync` with the base at `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` and the local manifest at `22283d8a866d042e02336fcb4698253ac6bf9c3b`. That alone proves the staging was sound, and it is the part `DEC-24` was designed to make boring.

What should not be over-planned: build errors and their remedies. A first build of a device tree nobody on this project has built produces errors that cannot be predicted. The stopping rule (`DEC-25`, runbook section 4) bounds them:

- A sync failure stops the session.
- A build failure gets a fix attempt only if it is manifest-class: a deferred item's detector, a missing project, or a wrong branch or commit. At most 2 attempts are allowed.
- At hour 8 the session retrieves what exists and tears down, whatever state the build is in.

**One rule about remedies is fixed in advance.** A fix edits `.repo/local_manifests/ishtar-beryl.xml` on the server, is recorded in `~/evidence/fixes.diff`, and is not pushed during the session (runbook section 4). It does not die with the server, because `fixes.diff` is retrieved with the evidence. After the session it lands on `ahmetxa/android_local_manifests`, re-checked with `check.py` and pushed with the user's approval, before any second rental. No push approval is spent while the server bills.

The session ends by teardown whatever the outcome. A failed build still collects its evidence, still deletes the server and its Primary IP, and still records elapsed hours. A server left running because the build "nearly worked" is the cost failure this whole phase is shaped to prevent. A server shut down instead of deleted is the same failure: runbook section 3 records that Hetzner bills a created server "until you delete them, independent of their state".

## 4. Scope

- The pre-rental gate on the day. It runs runbook section 5's scripted block: a manifest clone asserted at `22283d8`, `check.py` both ways with the known-bad cases failing as `14 element(s) failed`, and both repositories reading `private=false`. It also covers the section's four manual checks — the CCX53 limit, the public SSH key, the output directory outside every repository, and the 10-hour window — and a re-read of `DEC-25`'s budget and stopping rule.
- Correcting runbook section 10's built-symlink test to the path the `;SYMLINK=` entry creates, before renting.
- Renting and provisioning per runbook section 6: Hetzner Cloud CCX53, Ubuntu 22.04, and no volume, backup, cloud-init or placement group. Server setup follows section 7. Server type, location, image and creation time (UTC) are recorded; the address never is.
- Credential-free access under `DEC-25`. Both `ahmetxa` repositories are public and are cloned over anonymous HTTPS; no GitHub credential exists on the server.
- The sync per runbook section 8. `repo init` runs at `AOSPA/manifest` `beryl` and stops if the base is not the pinned commit. The local manifest is cloned at `22283d8`, then `repo sync --current-branch --no-tags --fail-fast -j16` runs.
- The build per runbook section 9: `./rom-build.sh ishtar -z`, where the default build type is `userdebug` and `-z` also writes the fastboot image package. It runs within the stopping rule, and barista's "Unexpected exit status from the brewing process" is treated as a sync failure.
- The runbook section 10 evidence, collected before teardown whatever the outcome:
  - `repo manifest -r`, with its credential-URL check;
  - the consumed tree's `aon_front.pb` entry (AON procedure step 1);
  - the built symlink state;
  - md5 and size of the three camera blobs;
  - the common tree's `selinux` line;
  - log tails and the token scan.
- Retrieval per runbook section 11 of every listed artifact, with sha256 checked at both ends, into `~/Documents/Projeler/ishtar-builds/<date>/`, outside every repository.
- Teardown per runbook sections 3 and 12:
  - the server deleted, not shut down;
  - any Primary IP deleted;
  - no volume, snapshot or backup left;
  - billing confirmed stopped;
  - elapsed hours recorded against the ceiling.
- The ledger row runbook section 13 specifies, a Phase 8 readiness statement, and a check against ledger section 7's viability trigger.

## 5. Out of Scope

- Flashing, booting or any device action. `Faz7.3`.
- Installing `ishtar-cam-modes` or any module on the new build. `Faz8.3`.
- Any kernel merge. `Faz8.2` scoped it (`IMPL-93`, `DEC-08` recommendation defer); nothing is merged here.
- Signing with anything other than AOSPA's default build signing; no project key goes to the server.
- Publishing the build output anywhere public. The output embeds proprietary vendor blobs, and `ARC-04` records that the project never redistributes them. Retrieved outputs stay under `ishtar-builds/`, outside every repository.
- `calcite`, or any second build variant.
- Fixes beyond the stopping rule. Reaching the rule is a recorded, bounded outcome, not a reason to extend the rental.
- Pushing a fix during the session. `fixes.diff` lands on GitHub after teardown.
- Any GitHub credential, token or deploy key on the server. `DEC-25` made both repositories public so that none exists. If that plan ever changes, runbook section 12 step 6 revokes the credential.
- Creating a snapshot, backup or volume, which bill separately (runbook section 3).
- Adopting the build as a daily base. `Faz7.3` assesses that with the camera consequence stated.
- Uploading workspace content to the server beyond what the runbook names. `snapshots/` holds full-resolution captures, and none of it is needed for a build.

## 6. Current Repository Evidence

**The inputs, re-read 2026-09-13 by planning run 19 with read-only `gh api` calls.** `ahmetxa/android_local_manifests` `main` is `22283d8a866d042e02336fcb4698253ac6bf9c3b` ("Close the open items: pin beryl-era sources over AOSPA's beans", 2026-09-11). Both it and `ahmetxa/android_device_xiaomi_ishtar` read `private=false`. Its `README.md` reads "Status: ready for a first build attempt, not yet built (2026-09-11)".

AOSPA's `lunch` runs `barista.py`, which writes `.repo/local_manifests/baristablend.xml` from `vendor/aospa/products/ishtar/beans.xml` and syncs the 67 projects the beans name, still on `vauxite` branches. `ishtar-beryl.xml` pins 13 projects over them. For each, it first drops barista's entry with an optional `remove-project`, then pins the `beryl`-era source at the same path. The other 54 come from barista unchanged, and only `repo manifest -r` records their commits.

The seven former open items now stand as follows:

- **Closed:** `hardware/xiaomi`, sepolicy, the kernel, the display and audio overrides, `vendor/xiaomi/camera`, and the server distribution.
- **Deferred:** the `display-drivers` pin, `hardware/qcom/gps` and `hardware/qcom/media`, and the shallow sync of the three blob repositories.

Runbook section 4 tabulates each deferred item's detector and allowed fix. `gps` and `media` have no staged fix: the session stops. The kernel is built inline from `kernel_platform/msm-kernel` `1c509b3` and `kernel_platform/common` `b11e560`.

**The runbook, `docs/build-environment.md` (`IMPL-91`).** Section 1 records:

- the host (`DEC-24`);
- Ubuntu 22.04 LTS with a 24.04 fallback (`DEC-22`);
- the CCX53 server type, the 10-hour budget, and public repositories with no server credential (`DEC-25`);
- base `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` and local manifest `22283d8a866d042e02336fcb4698253ac6bf9c3b`;
- the build command `./rom-build.sh ishtar -z`.

Section 3 quotes Hetzner's billing pages. A created server bills "until you delete them, independent of their state". Primary IPs bill separately until deleted. Snapshots and backups bill too.

The remaining sections carry the procedure:

- section 4: the stopping rule;
- section 5: the free pre-rental check;
- sections 6 to 9: provisioning, setup, sync and build;
- section 10: evidence collection;
- section 11: retrieval;
- section 12: teardown;
- section 13: the ledger row.

Every scripted block starts with `set -euo pipefail`, and `IMPL-91` ran `bash -n` on all nine.

**What the install needs (runbook section 11, `AUDIT-FIX-44`).**

| Artifact | Why it is retrieved |
|---|---|
| `aospa-<version>-image.zip` | The fastboot package `-z` writes, for `fastboot update` |
| `aospa-<version>.zip` | For `adb sideload` from AOSPA recovery, which the runbook records as the current XDA `ishtar` method |
| `recovery.img` | Flashed before sideloading |
| `boot`, `init_boot`, `vendor_boot`, `dtbo`, `vbmeta` and `vbmeta_system` images | The boot chain, retrieved loose |
| `evidence.tar.gz` | The section 10 evidence |
| `aospa_ishtar-target_files.zip` | Optional: every partition image can be re-extracted from it |

Xiaomi firmware is not a build output. Which firmware `beryl` needs, and whether moving from Android 15 to 16 requires a data format, are questions for `Faz7.3`.

**The AON entry and the symlink path, measured this run.** The consumed device tree is `ahmetxa/android_device_xiaomi_ishtar` `d48816f`, which is upstream `df05661` plus one line. Its local mirror `refs/a16_ishtar` carries the entry `odm/lib64/camera/aon_front.pb;SYMLINK=vendor/lib64/camera/aon_front.pb` at `proprietary-files.txt:1037`, and `device_ishtar` carries the same entry at line 1031. The build therefore installs the blob at `odm/lib64/camera/aon_front.pb` and creates the symlink at `vendor/lib64/camera/aon_front.pb`. `docs/aon-verification.md` agrees on both steps:

- Section 5 step 1 prescribes `grep -n 'aon_front.pb;SYMLINK=' <build-tree>/proprietary-files.txt` and calls exactly one match conclusive.
- Step 3 expects `/vendor/lib64/camera/aon_front.pb` to be "a symlink to `/odm/lib64/camera/aon_front.pb`".

**Runbook section 10 tests `[ -L "$OUT/odm/lib64/camera/aon_front.pb" ]`.** That is the regular file, so as written the check prints "NOT a symlink or does not exist" on a correct build. Its consumed-tree line greps `aon_front.pb` without the suffix, and the matched line still shows the `;SYMLINK=` part.

**The guarded blobs.**

- `ishtar-cam-modes/halpatch.sh:32-34` records `HAL_STOCK_MD5=c3fa63a86ee3ecaf9fbf02005d35f6b5`, `HAL_FULLRES_MD5=fe0245a4720fb07b01d96deef47f5569` and `HAL_SIZE=27268688`.
- `ishtar-cam-modes/customize.sh:14` records the sensor blob `EXPECT_MD5=9e4d0fe1a8bf2eb4146c9917a0ac2c4c`.
- `IMPL-92` measured both at vendor pin `f92e7a9`: `camera.qcom.so` md5 equals `HAL_STOCK_MD5` at 27268688 bytes, and the IMX989 sensor module md5 equals `EXPECT_MD5` at 1062250 bytes.
- No fixup reaches either file at the pinned device-tree commits.

Runbook section 10 reads the built copies at `odm/lib64/hw/camera.qcom.so`, `odm/lib64/hw/camera.xiaomi.so` and `odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin`. Those post-build values are `Faz8.1`'s `F8.1-06` input.

`.gitignore` ignores `*.zip` but has no rule for `*.img`. The runbook stores every retrieved output outside every repository, so no ignore rule is needed.

**Two precedents shape the scripts.** `IMPL-90`'s disclosed defect — a pipe masking a failed `git am`, followed by an ungated push — is the reason for this session's fail-on-error rule. Runbook section 9's barista check exists because AOSPA's `lunch` does not test barista's exit status (`AOSPA/android_build` `beryl` `envsetup.sh` line 582).

Project-Ontology invariant 10: "Every offset is bound to one exact vendor build … the md5 guard is the detector." That invariant is why the post-build md5 read is in scope here rather than deferred to the device.

## 7. Planned Work Breakdown

- F7.2-01 — Pass the pre-rental gate
  - Description: On the rental day, run `docs/build-environment.md` section 5's scripted block as written, with `GH` pointing at the WinGet `gh.exe`. Then run its four manual checks: the Console's Limits tab allows one CCX53, the public SSH key is present, `~/Documents/Projeler/ishtar-builds/` exists outside every repository, and the 10-hour ceiling fits the day. Re-read `DEC-25` and runbook section 4. Before renting, correct runbook section 10's built-symlink test from `$OUT/odm/lib64/camera/aon_front.pb` to `$OUT/vendor/lib64/camera/aon_front.pb`, keep its `readlink` target report, and re-run `bash -n` on that block. Any failure stops the sub-phase before renting, and the rental itself waits for the user's approval.
  - Output: A gate record with the section 5 block's exit status and its "pre-rental checks passed" line, the four manual confirmations, `DEC-25` named, and the section 10 correction with its `bash -n` result.
- F7.2-02 — Rent, provision and set up
  - Description: Only after the user approves the rental. Create the server per runbook section 6: CCX53, Ubuntu 22.04, name `ishtar-beryl-build`, no volume, backup, cloud-init or placement group. Record the creation time (UTC) and keep the address in the shell only. Run section 7 as root, then as `builder` inside `tmux`. If the image is not 22.04, section 7 applies its `sysctl` fallback (`DEC-22`).
  - Output: A provisioned server and a start record — type, location, image, creation time — without an address or key.
- F7.2-03 — Confirm credential-free access
  - Description: Confirm the section 5 result that both `ahmetxa` repositories read `private=false`, and that the server clones them over anonymous HTTPS with no token, deploy key or credential helper (`DEC-25`). If a clone asks for authentication, stop: the access plan has changed, and no credential is improvised on the server.
  - Output: An access record stating that no GitHub credential exists on the server.
- F7.2-04 — Initialise and sync
  - Description: Run runbook section 8: `repo init` at `AOSPA/manifest` `beryl`, stopping if the base is not `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2`. Then clone the local manifest, assert `22283d8a866d042e02336fcb4698253ac6bf9c3b`, and run `repo sync --current-branch --no-tags --fail-fast -j16`. A sync failure stops the session and goes straight to F7.2-07, with one exception. If the failure matches a deferred item's sync detector in runbook section 4's table — the shallow sync of a `vendor/xiaomi/*` blob repository, or `vendor/xiaomi/camera` — its listed fix is a manifest-class attempt counted against the 2.
  - Output: A completed sync or its characterised failure, the `timeline.txt` stamps, and the shallow-sync verdict for the former open item 7.
- F7.2-05 — Record AON procedure step 1 on the consumed tree
  - Description: Read `device/xiaomi/ishtar/proprietary-files.txt` in the synced tree. Runbook section 10 records the matching line. The step 1 verdict counts the lines carrying `aon_front.pb;SYMLINK=` and expects exactly one. Section 10 runs before teardown in every case, so this verdict exists whatever the build outcome.
  - Output: The step 1 verdict, recorded against `docs/aon-verification.md` section 5.
- F7.2-06 — Build within the stopping rule
  - Description: Run runbook section 9: `./rom-build.sh ishtar -z` into `~/logs/build.log`, then barista's exit-status check. On failure, classify the error from the grep and the log tail. A manifest-class error gets its listed fix, made in `.repo/local_manifests/ishtar-beryl.xml` on the server and appended to `~/evidence/fixes.diff`, then a retry, with at most 2 attempts in the session. Manifest-class means a detector in runbook section 4's deferred-items table, a missing project, or a wrong branch or commit. Any other class stops the session and becomes a replanning input. At hour 8, whatever the state, go to F7.2-07.
  - Output: A build outcome (complete, partial with the stage reached, or stopped by rule), the error classes, the attempts used out of 2, `fixes.diff`, and per-stage times from `timeline.txt`.
- F7.2-07 — Collect the evidence before teardown
  - Description: Run runbook section 10, with F7.2-01's corrected symlink test, whatever the outcome. It writes:
    - `manifest-resolved.xml`, aborting if a credential-shaped URL appears;
    - `build-evidence.txt`: the consumed tree's `aon_front.pb` line, the built symlink at `vendor/lib64/camera/aon_front.pb` with its target, md5, size and path of `odm/lib64/hw/camera.qcom.so`, `odm/lib64/hw/camera.xiaomi.so` and `odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, and the common tree's `selinux` line;
    - 200-line log tails.

    It then runs the token scan and packs `evidence.tar.gz`. A missing file is recorded, not fatal. Compare the `camera.qcom.so` and sensor module md5s with `HAL_STOCK_MD5` and `EXPECT_MD5` as facts, not conclusions: they feed `Faz8.1`'s `F8.1-06`, which compares them with `IMPL-92`'s static values.
  - Output: `evidence.tar.gz`, holding the post-build evidence block for `Faz8.1` and `Faz7.3`.
- F7.2-08 — Retrieve every install artifact with sha256 at both ends
  - Description: Run runbook section 11.
    - On the server: assert exactly one `aospa-*-image.zip` and two `aospa-*.zip`. Copy both packages, `recovery.img`, `boot.img`, `init_boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img` and `vbmeta_system.img` beside `evidence.tar.gz`, and write `SHA256SUMS`.
    - The optional target-files archive: if the ceiling allows, also retrieve `aospa_ishtar-target_files.zip`. If it does not, record that the partition images are also inside the retrieved image package.
    - Anything not retrieved: name each artifact that could not be retrieved, with the package it can be extracted from.
    - On a failed build: only `evidence.tar.gz` and its `SHA256SUMS` exist.
    - On the host: `scp` into `~/Documents/Projeler/ishtar-builds/<date>/` and run `sha256sum -c SHA256SUMS`.

    Do not tear down until every file reports OK.
  - Output: The retrieved set with `sha256sum -c` passing for every file, stored outside every repository, and one line per artifact: retrieved, not produced, or extractable from a named package.
- F7.2-09 — Tear down
  - Description: Run runbook section 12 in order:
    1. `sha256sum -c` has passed on the host.
    2. Delete the server `ishtar-beryl-build` in the Console. Delete it, never shut it down: a created server bills "until you delete them, independent of their state" (runbook section 3).
    3. Delete any Primary IP still listed, which bills separately until deleted.
    4. Confirm no volume, snapshot or backup exists.
    5. Confirm the project lists zero servers and zero Primary IPs.
    6. Record the deletion time (UTC) and the elapsed hours against the 10-hour ceiling.
    7. Confirm that no credential was issued (`DEC-25`).
    8. On the host, run `ssh-keygen -R` and `unset BUILD_HOST`.
  - Output: A teardown record: server and Primary IP deleted, zero resources listed, the deletion time, the elapsed hours, and "no credential issued".
- F7.2-10 — State what Phase 8 inherits and write the ledger row
  - Description: Write the ledger row runbook section 13 names: per-stage exit status and elapsed time, error classes and log tails, fix attempts used with `fixes.diff`, the base and local manifest commits, the retrieved files with their sha256, the section 10 values, and the deletion time with elapsed hours. Write the outcome as built, partial or blocked, check it against ledger section 7's viability trigger, and name what `Faz7.3`, `Faz8.1` and `Faz8.2` can now use. If `fixes.diff` is non-empty, record it as an input that lands on `ahmetxa/android_local_manifests` before any second rental, re-checked with `check.py`, pushed with the user's approval, and followed by updating the runbook's manifest commit.
  - Output: The ledger row, a Phase 8 readiness statement, the `fixes.diff` hand-off if any, and a replanning input if the trigger fires.

## 8. Acceptance Criteria

- The gate record exists and predates the rental. Runbook section 5's block exited 0 that day, its four manual checks are confirmed, and `DEC-25` is named. Runbook section 10's symlink test reads `vendor/lib64/camera/aon_front.pb` and passes `bash -n`.
- The rental followed the user's explicit approval. The start record carries type, location, image and creation time, without an address.
- No GitHub credential, token or deploy key was created for or placed on the server.
- Before the sync, the base read `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` and the local manifest read `22283d8a866d042e02336fcb4698253ac6bf9c3b`, or the session stopped on the mismatch.
- The sync completed, or its failure is characterised. `manifest-resolved.xml` shows the 13 pinned projects at their `ishtar-beryl.xml` commits.
- The shallow-sync item is marked tested with its result, or its fix's use is recorded.
- AON procedure step 1 found exactly one `aon_front.pb;SYMLINK=` line in the consumed tree, or a zero result is recorded as "the build never saw the fix".
- Every build attempt is recorded with its error class, stage reached and elapsed time. At most 2 fix attempts were made, each manifest-class and each in `fixes.diff`, and no fix was pushed during the session.
- The runbook section 10 evidence exists whatever the outcome. If a build completed, it records md5 and size for the three camera blobs, and the symlink state and target at `vendor/lib64/camera/aon_front.pb`.
- If a build completed, every runbook section 11 artifact was retrieved before the server was deleted, with `sha256sum -c` passing, or its absence is recorded with the package it can be extracted from. No retrieved file sits inside a repository.
- **Whatever the build outcome:** the server and every Primary IP are deleted, not shut down. The project lists zero servers and zero Primary IPs, no volume, snapshot or backup exists, and elapsed hours are recorded against the 10-hour ceiling.
- The ledger row runbook section 13 names exists, and so does the Phase 8 readiness statement. Ledger section 7's viability trigger is explicitly evaluated. A non-empty `fixes.diff` is recorded as an input that lands on GitHub before any second rental.
- No credential value, server address or password appears in any retrieved file, snapshot, runbook edit or ledger row.

## 9. Validation and Test Approach

Validation spans a paid remote session and host-side checks after it. No device is involved.

- `VAL-GATE` (proposed) — runbook section 5's scripted block, whose `check.py` runs are `Faz7.1`'s `VAL-PINS` and `VAL-PINS-NEG` repeated that day; the four manual checks; and `bash -n` on the corrected section 10 block.
- `VAL-SYNC` (proposed) — the base and local manifest assertions in runbook section 8, `repo sync`'s exit status, and `manifest-resolved.xml` compared on the host against the 13 pins in `ishtar-beryl.xml` at `22283d8`. The check compares revisions and does not trust exit status alone.
- `VAL-AON-TREE` (proposed) — `docs/aon-verification.md` section 5 step 1, read from the consumed-tree line in `build-evidence.txt`: exactly one `;SYMLINK=` line.
- `VAL-COMPILE` (proposed) — the build outcome per attempt from runbook section 9 and `timeline.txt`, with the stage reached and attempts used out of 2. It is named apart from `VAL-BUILD`, which `Faz6.2` defined as the device-side AON verification and which `Faz7.3` executes.
- `VAL-BLOBMD5` (proposed) — the camera-blob block of `build-evidence.txt`: md5, size and path of the three blobs, plus the symlink state and target of `vendor/lib64/camera/aon_front.pb`.
- `VAL-RETRIEVE` (proposed) — on the host, `sha256sum -c SHA256SUMS` reports OK for every file. Each runbook section 11 artifact is present or its absence is recorded. The retrieval directory is outside every repository, and `git status --short` in the workspace shows no image or package.
- `VAL-TEARDOWN` (proposed) — the Hetzner Console lists zero servers, zero Primary IPs, and no volume, snapshot or backup; the deletion time is recorded; no GitHub credential exists to revoke (`DEC-25`).
- `VAL-SEC` (proposed) — runbook section 10's credential-URL check and token scan run on the server before anything is copied. Afterwards, a file-name-only scan checks the retrieved text files, the runbook changes and the ledger row for token-shaped strings and addresses. It never prints a match.
- `VAL-DOCS` (proposed) — read back the runbook's section 10 correction and any deviations, the evidence block, the ledger row and the readiness statement.

**Local versus live:** the sync and build are live on a rented machine; retrieval checks and document checks are local.

**Security:** validation covers the absence of any server credential, deletion rather than shutdown, and the non-publication of blob-bearing outputs.

**Ontology:** validation applies to invariant 10, whose detector — the md5 — is read here for the first time on an Android 16 blob as built.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| docs/build-environment.md | modified | The operative runbook. `F7.2-01` corrects section 10's built-symlink path before renting; deviations observed in the session are recorded afterwards. | VAL-GATE, VAL-DOCS, VAL-SEC |
| docs/aon-verification.md | existing | Section 5 step 1 is executed here; results are recorded in the evidence file and appended by `Faz7.3`. | VAL-AON-TREE |
| refs/a16_ishtar/proprietary-files.txt | existing | Local mirror of the upstream tree. Line 1037's `;SYMLINK=` entry is the basis of the section 10 correction; the consumed tree is the pinned fork on the server. | VAL-AON-TREE, VAL-BLOBMD5 |
| ishtar-cam-modes/halpatch.sh | existing | Source of `HAL_STOCK_MD5` and `HAL_SIZE` read against the built `camera.qcom.so`. | VAL-BLOBMD5 |
| ishtar-cam-modes/customize.sh | existing | Source of the sensor blob `EXPECT_MD5`. | VAL-BLOBMD5 |
| snapshots | existing | Receives text only, copied out of the retrieved `evidence.tar.gz`: the gate record, `build-evidence.txt`, `timeline.txt`, `manifest-resolved.xml`, `fixes.diff` and the teardown record. No image or package. | VAL-SYNC, VAL-BLOBMD5, VAL-TEARDOWN |
| .gitignore | existing | Not modified: the runbook stores retrieved outputs outside every repository, so no `*.img` rule is needed. | VAL-RETRIEVE |
| Planner-docs/Planing-Ledger.md | modified | The runbook section 13 row, the Phase 8 readiness statement, any `fixes.diff` hand-off, and any section 7 trigger. | VAL-DOCS, VAL-SEC |

## 10. Dependencies and Sequencing

**Depends on** `Faz7.1`, which `IMPL-91` verified: a buildable manifest at `22283d8`, `DEC-22` and `DEC-25` answered, and `docs/build-environment.md` written. Depends on `Faz6.1` for the symlink entry that step 1 checks. Depends on the tenth Step 3 audit of this amendment before a Step 4 session runs it.

**Blocks** `Faz7.3` (no output, no flash) and `Faz8.1`'s `F8.1-06`. `Faz8.1`'s static half is done (`IMPL-92`: both layers carry-over on static values). `Faz8.2` is verified (`IMPL-93`) and does not wait on this sub-phase.

**Required decisions:** none new. `DEC-22` and `DEC-25` are answered. Reaching the stopping rule is not a decision point: it ends the session. Landing a non-empty `fixes.diff` on GitHub after the session needs the user's push approval.

**Required credentials:** none on the server (`DEC-25`). The user needs their Hetzner account and their SSH key, whose private half never leaves the Windows host. Neither is recorded anywhere.

**Required infrastructure:**

- the rented CCX53;
- network egress to GitHub, GitLab and the AOSPA sources;
- the host's `ishtar-builds/` directory, with room for the retrieved set;
- the WinGet `gh.exe` for runbook section 5.

**Required human approvals:**

- the Console checks in F7.2-01;
- renting, which spends money;
- deletion in the Console;
- any post-session push of `fixes.diff`.

**Fresh session token and context risk:** medium, per Main-Planing's Phase 7 band, rising to high if the build fails repeatedly. The hazard is sync and build output volume. Mitigation: record per stage what runbook section 4 names — start and end time, exit status, error class and the last lines of a failing log — never whole logs, and keep the stopping rule in the session's own context. Subagents: not recommended; the session drives a single stateful remote resource.

## 11. Risks and Mitigations

- Risk: the build nearly works and the server stays up. Impact: a cost overrun, the failure `DEC-24` was designed around. Mitigation: `DEC-25`'s 10-hour ceiling and the hour-8 retrieve-and-delete rule are in force before renting, and teardown is an acceptance criterion independent of the outcome.
- Risk: the server is shut down instead of deleted, or a Primary IP is left behind. Impact: billing continues "independent of their state". Mitigation: F7.2-09 follows runbook sections 3 and 12, and `VAL-TEARDOWN` requires zero servers and zero Primary IPs.
- Risk: a fix made on the server is lost with the server. Impact: the output cannot be reproduced, and the next rental repeats the discovery. Mitigation: runbook section 4 records every fix in `fixes.diff`, which travels in `evidence.tar.gz`, and F7.2-10 hands it to GitHub before any second rental.
- Risk: a masked exit code lets a failed step look successful (`IMPL-90`'s defect class). Impact: the session proceeds on a broken sync or build, and the evidence is wrong. Mitigation: every runbook block starts with `set -euo pipefail`, runbook section 9 catches barista's unchecked exit status, and `VAL-SYNC` compares revisions.
- Risk: runbook section 10's symlink test reads the wrong path. Impact: a correct build's AON result looks failed, and `Faz7.3` is misdirected. Mitigation: F7.2-01 corrects the path to `vendor/lib64/camera/aon_front.pb` before renting, and an acceptance criterion checks it.
- Risk: a credential reaches the server or a retrieved file. Impact: a live token in a log or in `repo manifest -r`. Mitigation: `DEC-25` made the repositories public, so no credential is issued. Runbook section 10's credential-URL check and token scan run before anything is copied.
- Risk: an install artifact is missing when `Faz7.3` flashes. Impact: a second paid sync and build. Mitigation: F7.2-08 retrieves and verifies every runbook section 11 artifact before deletion, or records which package it can be extracted from.
- Risk: a blob-bearing output is published, for example as a public release. Impact: proprietary blob redistribution, contrary to `ARC-04`. Mitigation: out of scope by rule; retrieval is private and verified by sha256.
- Risk: a retrieved image is committed by accident. Impact: repository bloat, and blobs in a remote. Mitigation: runbook sections 5 and 11 store outputs outside every repository, and `VAL-RETRIEVE` reads `git status`.
- Risk: shallow sync fails partway through. Impact: wasted hours. Mitigation: the fix in runbook section 4's deferred-items table, counted against the 2 attempts. The manifest `README.md` puts full history at about 1.8 GiB for the `ishtar` vendor repository and 0.3 GiB for `sm8550-common`, well inside the CCX53's 600 GB.
- Risk: the AON step 1 check is skipped because the build dominates attention. Impact: `Faz7.3`'s device result becomes uninterpretable, since a missing providers result could simply mean the tree lacked the entry. Mitigation: runbook section 10 records the consumed-tree line before teardown whatever the outcome, and F7.2-05 is a distinct work item.
- Risk: the post-build md5 read is skipped. Impact: `Faz8.1` has only the vendor-repository value, and a fixup or build step that altered the file goes unseen. Mitigation: F7.2-07 is a distinct work item on the runbook's evidence list.

## 12. Desired End State

An AOSPA `beryl` build for `ishtar` has been attempted on a rented CCX53 from the inputs at `22283d8`, following runbook sections 5 to 13, and the outcome is recorded. If it completed, every runbook section 11 artifact sits in `ishtar-builds/` on the user's machine, outside every repository, with `sha256sum -c` passing. The resolved manifest proves the build came from the pinned inputs. The consumed tree carried the AON entry, the built symlink state at `vendor/lib64/camera/aon_front.pb` is known, and so is the md5 of the guarded camera blobs as built. Whatever the outcome, the server and its Primary IP are deleted, no credential ever existed on the server, and the elapsed hours are recorded against the 10-hour ceiling. Phase 8 has a readiness statement, ledger section 7's viability trigger has been evaluated, and any `fixes.diff` is waiting to land on GitHub.

Evidence the implementer produces:

- the gate record, with the section 10 correction;
- the start record and `timeline.txt`;
- `manifest-resolved.xml`;
- the AON step 1 verdict;
- the per-attempt build records and `fixes.diff`;
- `build-evidence.txt`;
- `SHA256SUMS` with its host check;
- the teardown record.

The ledger summary Step 4 appends is the row runbook section 13 specifies:

- per-stage exit status and elapsed time;
- the error class and last lines of any failing log;
- fix attempts used out of 2, with `fixes.diff`;
- the base and `22283d8`;
- the retrieved file names with their sha256;
- the section 10 values;
- the deletion time and elapsed hours against the ceiling.

It also carries the shallow-sync and AON step 1 verdicts, and what Phase 8 inherits.

## 13. Next Sub-Phase Transition Criteria

- The server and every Primary IP are deleted, and no credential was issued. This holds even when the build failed.
- Elapsed hours are recorded against the `DEC-25` ceiling.
- For `Faz7.3`, all of the following are recorded; without them, `Faz7.3` does not start:
  - every runbook section 11 artifact exists locally with `sha256sum -c` passing, or its absence is recorded with the package it can be extracted from;
  - the AON step 1 result;
  - the built symlink state.
- For `Faz8.1`: the post-build md5s and sizes of `camera.qcom.so` and the sensor module are recorded for `F8.1-06`, or their absence is explained.
- The Phase 8 readiness statement is written, any section 7 trigger is raised in the ledger, and a non-empty `fixes.diff` is recorded as landing on GitHub before any second rental.
