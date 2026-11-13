# Faz 7.2 — First AOSPA beryl Build on a Rented VDS

## 1. Context

Main-Planing Phase 7 (`SNAP-2026-09-10-MAIN`) sets the desired end state: "One AOSPA `beryl` build for `ishtar` completed on a rented VDS from inputs staged on GitHub, with the output retrieved and the server released." Its acceptance signal reads "A flashable build output exists and boots; the rental time the build consumed is recorded." This sub-phase is the paid half of that. It rents, builds, retrieves, and releases. The boot half belongs to `Faz7.3`, because flashing is the user's action on a daily device and happens after the server is gone.

**Amended 2026-09-14 by planning run 20 (bounded Step 2 amendment: the `DEC-26` provider change).** After `IMPL-94`'s gate did not pass, Hetzner's new-account limit blocked the CCX53 and the user moved the rental to Scaleway (`DEC-26`, answered 2026-09-14). `IMPL-95` then re-targeted `docs/build-environment.md` on Scaleway's own billing and deletion pages. Every provider fact below was re-read from that runbook on 2026-09-14. It replaces the Hetzner text run 19 wrote:

- **Instance type.** Scaleway **POP2-32C-128G** (32 dedicated vCPU, 128 GiB, Block Storage only), not the Hetzner CCX53 and its 600 GB NVMe.
- **Disks.** Three Block volumes: the boot volume, 40 GB 5K; `ishtar-src`, 310 GB 5K, at `/android`; and `ishtar-out`, 260 GB 15K, at `/android/beryl/out` (runbook sections 1, 6 and 7).
- **Console and IP.** The Scaleway Console instead of the Hetzner Console, and the flexible IPv4 instead of the Primary IP.
- **Operating system.** Ubuntu 22.04, with `DEC-22`'s 24.04 fallback and its `sysctl` made persistent (runbook section 7).
- **Budget.** `DEC-25`'s 10-hour ceiling and hour-8 rule stand under `DEC-26` (b). They count every billed resource, and every started hour counts as a full hour. An out-of-memory kill is not retried (`DEC-26` (d), runbook section 4).
- **Teardown.** Powering off does not stop billing. The Instance API's `terminate` may only detach Block volumes, and the flexible IP outlives the Instance. So teardown deletes the Instance, each Block volume and the flexible IP, then confirms zero of each and zero snapshots (`DEC-26` (c), runbook sections 3 and 12).
- **Manual checks.** An identity-validated quota for POP2-32C-128G and for 610 GB of Block Storage, and the SSH key present in the Project the Instance is created in (runbook section 5).
- **Paths.** The tree sits at `/android/beryl`, and retrieval is staged in `~/out-pkg` (runbook sections 7 to 11).

No work item was added or removed, and no phase objective or acceptance signal changed. The runbook repairs `IMPL-94` made for `AUDIT-FIX-52`, `-53` and `-54` are unchanged. `Main-Planing.md` lines 75, 211 and 265 (`R9`) and `Project-Comprehension.md` `EV-20` still name Hetzner. That wording goes to the next Step 1 amendment, with `AUDIT-FIX-41` and `-42`. The eleventh Step 3 audit reads this amendment before `Faz7.2` enters a paid session.

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

In one bounded paid session, run `docs/build-environment.md` against the inputs `Faz7.1` staged and turn them into a retrieved, sha256-verified set of `ishtar` install artifacts. Capture before teardown the evidence `Faz7.3` and `Faz8.1` need. Finish with the Instance, each of its three Block volumes and its flexible IP deleted, and with no credential ever placed on the Instance. Record the elapsed hours, rounded up, against the 10-hour ceiling that `DEC-25` set and `DEC-26` kept.

## 3. Description

The problem is that the Android 16 track has never produced an artifact. The trees are staged and pinned, but nothing has compiled from them, and every day the project owns a pinned manifest without a build is a day the pins can only be trusted on paper.

It belongs after `Faz7.1`, which is `verified` (`IMPL-91`): the manifest is buildable, `DEC-22`, `DEC-25` and `DEC-26` are answered, and the runbook exists, re-targeted to Scaleway by `IMPL-95`. It belongs before `Faz7.3` because a flash needs an output.

The vibecoding slice strategy follows the runbook's own order, cheapest failure surface first:

1. The free pre-rental checks (section 5).
2. Provisioning, then server setup with both data volumes mounted (sections 6 and 7).
3. The sync with its base-pin assertion (section 8).
4. The build (section 9).

The fastest useful signal is a completed `repo sync` with the base at `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` and the local manifest at `22283d8a866d042e02336fcb4698253ac6bf9c3b`. That alone proves the staging was sound, and it is the part `DEC-24` was designed to make boring.

What should not be over-planned: build errors and their remedies. A first build of a device tree nobody on this project has built produces errors that cannot be predicted. The stopping rule (`DEC-25` as amended by `DEC-26`, runbook section 4) bounds them:

- A sync failure stops the session.
- A build failure gets a fix attempt only if it is manifest-class: a deferred item's detector, a missing project, or a wrong branch or commit. At most 2 attempts are allowed.
- An out-of-memory kill is not manifest-class and is not retried (`DEC-26` (d)). The session stops, retrieves what exists and tears down.
- At hour 8 the session retrieves what exists and tears down, whatever state the build is in.

**One rule about remedies is fixed in advance.** A fix edits `.repo/local_manifests/ishtar-beryl.xml` on the server, is recorded in `~/evidence/fixes.diff`, and is not pushed during the session (runbook section 4). It does not die with the server, because `fixes.diff` is retrieved with the evidence. After the session it lands on `ahmetxa/android_local_manifests`, re-checked with `check.py` and pushed with the user's approval, before any second rental. No push approval is spent while the server bills.

The session ends by teardown whatever the outcome. A failed build still collects its evidence, still deletes the Instance, its Block volumes and its flexible IP, and still records elapsed hours. An Instance left running because the build "nearly worked" is the cost failure this whole phase is shaped to prevent. So is an Instance powered off instead of deleted, or a volume or flexible IP left behind. Runbook section 3 quotes Scaleway: "When a server is powered off, only its volumes and any reserved flexible IP address are billed." It also records that `terminate` may only detach Block volumes, and that the flexible IP is preserved.

## 4. Scope

- The pre-rental gate on the day. It runs runbook section 5's scripted block: a manifest clone asserted at `22283d8`, `check.py` both ways with the known-bad cases failing as `14 element(s) failed`, both repositories reading `private=false`, and the `AOSPA/manifest` `beryl` base still at its pin. It also covers the section's four manual checks, and a re-read of `DEC-25`'s budget and stopping rule as amended by `DEC-26`:
  - in the Scaleway Console, an identity-validated quota for one POP2-32C-128G and for the 610 GB of Block Storage;
  - the public SSH key present in the Project the Instance will be created in;
  - the output directory outside every repository;
  - the 10-hour window.
- Correcting runbook section 10's built-symlink test to the path the `;SYMLINK=` entry creates, before renting.
- Renting and provisioning in the Scaleway Console per runbook section 6:
  - **POP2-32C-128G**, with Ubuntu 22.04 (24.04 only as `DEC-22`'s fallback);
  - the system volume as Block Storage 5K, 40 GB, plus `ishtar-src` (5K, 310 GB) and `ishtar-out` (15K, 260 GB);
  - the public flexible IPv4 kept;
  - no snapshot, image, backup, cloud-init, placement group or Private Network.
- Server setup per section 7:
  - packages and the `builder` user;
  - the persistent `sysctl`, only on the 24.04 fallback;
  - each data volume picked by size and cross-checked against its Console volume ID, and formatted only where `blkid` finds no filesystem;
  - the volumes mounted at `/android` and `/android/beryl/out`;
  - `~/out-pkg` linked to `/android/pkg`, and a 16 GB swap file.

  Instance type, Availability Zone, image and creation time (UTC) are recorded. The address stays in the shell, and the volume IDs stay on paper or in the shell.
- Credential-free access under `DEC-25`. Both `ahmetxa` repositories are public and are cloned over anonymous HTTPS; no GitHub credential exists on the server.
- The sync per runbook section 8, in `/android/beryl`. It refuses to start unless the work volume is mounted at `/android/beryl/out`. `repo init` runs at `AOSPA/manifest` `beryl` and stops if the base is not the pinned commit. The local manifest is cloned at `22283d8`, then `repo sync --current-branch --no-tags --fail-fast -j16` runs. After the sync, the `du` of `.repo` and of the tree goes to `~/evidence/disk.txt`.
- The build per runbook section 9: `./rom-build.sh ishtar -z` in `/android/beryl`, where the default build type is `userdebug` and `-z` also writes the fastboot image package.
  - It runs within the stopping rule and refuses to start unless the work volume is mounted.
  - It records the `du` of `out` in `disk.txt`.
  - Barista's "Unexpected exit status from the brewing process" is treated as a sync failure.
  - A `Killed` or out-of-memory line is the out-of-memory class: stop, with no retry.
- The runbook section 10 evidence, collected before teardown whatever the outcome:
  - `repo manifest -r`, with its credential-URL check;
  - the consumed tree's `aon_front.pb` entry (AON procedure step 1);
  - the built symlink state;
  - md5 and size of the three camera blobs;
  - the common tree's `selinux` line;
  - log tails and the token scan.
- Retrieval per runbook section 11 of every listed artifact, with sha256 checked at both ends. Artifacts are staged from `/android/beryl` and `out/target/product/ishtar` into `~/out-pkg`, the link to `/android/pkg` on the source volume. They are then copied to `~/Documents/Projeler/ishtar-builds/<date>/` on the host, outside every repository.
- Teardown per runbook sections 3 and 12, whatever the outcome:
  - the Instance `ishtar-beryl-build` deleted in the Scaleway Console, never powered off or left in standby;
  - each Block volume deleted: the 40 GB system volume, `ishtar-src` and `ishtar-out`, because `terminate` may only detach them;
  - the flexible IP deleted, because it outlives the Instance;
  - the Console listing zero Instances, zero volumes, zero flexible IPs and zero snapshots in the Project and zone;
  - elapsed hours, from creation to the last deletion and rounded up to whole hours, recorded against the 10-hour ceiling.
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
- Any GitHub credential, token or deploy key on the server. `DEC-25` made both repositories public so that none exists. If that plan ever changes, runbook section 12 step 7 revokes the credential.
- Creating a snapshot, image or backup, or any volume beyond runbook section 6's three. Each bills on its own (runbook section 3).
- Keeping any volume after teardown, the source volume included (`DEC-26` (c)).
- Adopting the build as a daily base. `Faz7.3` assesses that with the camera consequence stated.
- Uploading workspace content to the server beyond what the runbook names. `snapshots/` holds full-resolution captures, and none of it is needed for a build.

## 6. Current Repository Evidence

**The inputs, re-read 2026-09-13 by planning run 19 with read-only `gh api` calls.** `ahmetxa/android_local_manifests` `main` is `22283d8a866d042e02336fcb4698253ac6bf9c3b` ("Close the open items: pin beryl-era sources over AOSPA's beans", 2026-09-11). Both it and `ahmetxa/android_device_xiaomi_ishtar` read `private=false`. Its `README.md` reads "Status: ready for a first build attempt, not yet built (2026-09-11)".

AOSPA's `lunch` runs `barista.py`, which writes `.repo/local_manifests/baristablend.xml` from `vendor/aospa/products/ishtar/beans.xml` and syncs the 67 projects the beans name, still on `vauxite` branches. `ishtar-beryl.xml` pins 13 projects over them. For each, it first drops barista's entry with an optional `remove-project`, then pins the `beryl`-era source at the same path. The other 54 come from barista unchanged, and only `repo manifest -r` records their commits.

The seven former open items now stand as follows:

- **Closed:** `hardware/xiaomi`, sepolicy, the kernel, the display and audio overrides, `vendor/xiaomi/camera`, and the server distribution.
- **Deferred:** the `display-drivers` pin, `hardware/qcom/gps` and `hardware/qcom/media`, and the shallow sync of the three blob repositories.

Runbook section 4 tabulates each deferred item's detector and allowed fix. `gps` and `media` have no staged fix: the session stops. The kernel is built inline from `kernel_platform/msm-kernel` `1c509b3` and `kernel_platform/common` `b11e560`.

**The runbook, `docs/build-environment.md` (`IMPL-91`, re-targeted to Scaleway by `IMPL-95` on 2026-09-14).** Section 1 records:

- the host (`DEC-24`) and the provider (`DEC-26`);
- Ubuntu 22.04 LTS with a 24.04 fallback (`DEC-22`, kept by `DEC-26` (a));
- the POP2-32C-128G Instance type and its three Block volumes (`DEC-26`);
- the 10-hour budget with the hour-8 rule and no retry after an out-of-memory kill (`DEC-25`, kept by `DEC-26` (b) and (d));
- public repositories with no server credential (`DEC-25`);
- base `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` and local manifest `22283d8a866d042e02336fcb4698253ac6bf9c3b`;
- the build command `./rom-build.sh ishtar -z`.

Section 3 quotes Scaleway's billing and deletion pages, read 2026-09-14:

- A CPU Instance is "Billed per hour of uptime (including startup and standby time)". No page says whether a started hour bills whole, so every started hour counts.
- "When a server is powered off, only its volumes and any reserved flexible IP address are billed."
- Block volumes bill by size and are persistent.
- The Block Storage FAQ says an API deletion deletes the attached volumes. The Instance API text disagrees: "`sbs_volume` volumes will only be detached". The runbook therefore assumes the volumes survive.
- The flexible IPv4 bills hourly and is preserved when the Instance is terminated.
- Snapshots bill as an independent resource.
- POP2-32C-128G, and Block Storage beyond 500 GB, need a validated identity.
- SSH keys are Project-scoped.

The remaining sections carry the procedure:

- section 4: the stopping rule;
- section 5: the free pre-rental check;
- sections 6 to 9: provisioning, setup, sync and build;
- section 10: evidence collection;
- section 11: retrieval;
- section 12: teardown;
- section 13: the ledger row.

Every scripted block starts with `set -euo pipefail`. `IMPL-95` ran `bash -n` on all ten, including the new section 7 volume block. That block has never run, because no Linux host exists without renting.

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
  - Description: On the rental day, run `docs/build-environment.md` section 5's scripted block as written, with `GH` pointing at the WinGet `gh.exe`. Then run its four manual checks:
    1. In the Scaleway Console's Organization quotas, identity is validated, the POP2-32C-128G quota is at least 1, and "Block Storage total size in GB" allows the 610 GB. If not, stop: no other type and no smaller volumes are rented silently.
    2. The public ed25519 SSH key is present in the Project the Instance will be created in, since keys are Project-scoped.
    3. `~/Documents/Projeler/ishtar-builds/` exists outside every repository.
    4. The 10-hour ceiling fits the day.

    Re-read `DEC-25` as amended by `DEC-26`, and runbook section 4. Before renting, correct runbook section 10's built-symlink test from `$OUT/odm/lib64/camera/aon_front.pb` to `$OUT/vendor/lib64/camera/aon_front.pb`, keep its `readlink` target report, and re-run `bash -n` on that block. Any failure stops the sub-phase before renting, and the rental itself waits for the user's approval.
  - Output: A gate record with the section 5 block's exit status and its "pre-rental checks passed" line, the four manual confirmations, `DEC-25` and `DEC-26` named, and the section 10 correction with its `bash -n` result.
- F7.2-02 — Rent, provision and set up
  - Description: Only after the user approves the rental. Create the Instance per runbook section 6, in the Scaleway Console, in the Project holding the SSH key and an Availability Zone that lists the type:
    - POP2-32C-128G, Ubuntu 22.04, name `ishtar-beryl-build`;
    - the system volume as Block Storage 5K, 40 GB, plus `ishtar-src` (5K, 310 GB) and `ishtar-out` (15K, 260 GB);
    - the public flexible IPv4 kept;
    - no snapshot, image, backup, cloud-init, placement group or Private Network.

    If the Console does not offer 22.04 for the type, choose 24.04 (`DEC-22` fallback) and note it in the timeline. Record the creation time (UTC). Keep the address in the shell, and the volume IDs on paper or in the shell.

    Then run section 7 as root:
    - packages and the `builder` user, with the persistent `sysctl` only on 24.04;
    - the volume block, which picks each data volume by size, cross-checks it against its Console volume ID, and formats only where `blkid` finds no filesystem;
    - the same block mounts `/android` and `/android/beryl/out`, links `~/out-pkg` to `/android/pkg` and adds the 16 GB swap file.

    Finally, run the `builder` block inside `tmux`.
  - Output: A provisioned Instance with both data volumes mounted and swap on, and a start record: type, Availability Zone, image and creation time, without an address, key or volume ID.
- F7.2-03 — Confirm credential-free access
  - Description: Confirm the section 5 result that both `ahmetxa` repositories read `private=false`, and that the server clones them over anonymous HTTPS with no token, deploy key or credential helper (`DEC-25`). If a clone asks for authentication, stop: the access plan has changed, and no credential is improvised on the server.
  - Output: An access record stating that no GitHub credential exists on the server.
- F7.2-04 — Initialise and sync
  - Description: Run runbook section 8 in `/android/beryl`. It refuses to start unless the work volume is mounted at `/android/beryl/out`. `repo init` runs at `AOSPA/manifest` `beryl`, stopping if the base is not `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2`. Then clone the local manifest, assert `22283d8a866d042e02336fcb4698253ac6bf9c3b`, and run `repo sync --current-branch --no-tags --fail-fast -j16`. After the sync, the `du` of `.repo` and the tree, and the `df` of the three mounts, go to `~/evidence/disk.txt`. A sync failure stops the session and goes straight to F7.2-07, with one exception. If the failure matches a deferred item's sync detector in runbook section 4's table — the shallow sync of a `vendor/xiaomi/*` blob repository, or `vendor/xiaomi/camera` — its listed fix is a manifest-class attempt counted against the 2.
  - Output: A completed sync or its characterised failure, the `timeline.txt` stamps, the post-sync `disk.txt` sizes, and the shallow-sync verdict for the former open item 7.
- F7.2-05 — Record AON procedure step 1 on the consumed tree
  - Description: Read `device/xiaomi/ishtar/proprietary-files.txt` in the synced tree. Runbook section 10 records the matching line. The step 1 verdict counts the lines carrying `aon_front.pb;SYMLINK=` and expects exactly one. Section 10 runs before teardown in every case, so this verdict exists whatever the build outcome.
  - Output: The step 1 verdict, recorded against `docs/aon-verification.md` section 5.
- F7.2-06 — Build within the stopping rule
  - Description: Run runbook section 9 in `/android/beryl`. It refuses to start unless the work volume is mounted. It runs `./rom-build.sh ishtar -z` into `~/logs/build.log`, records the `du` of `out` in `disk.txt`, and then runs barista's exit-status check. On failure, classify the error from the grep and the log tail. A `Killed` or out-of-memory line is not manifest-class and is not retried (`DEC-26` (d)). Stop, retrieve and tear down, and record it as a replanning input. A manifest-class error gets its listed fix, made in `.repo/local_manifests/ishtar-beryl.xml` on the server and appended to `~/evidence/fixes.diff`, then a retry, with at most 2 attempts in the session. Manifest-class means a detector in runbook section 4's deferred-items table, a missing project, or a wrong branch or commit. Any other class stops the session and becomes a replanning input. At hour 8, whatever the state, go to F7.2-07.
  - Output: A build outcome (complete, partial with the stage reached, or stopped by rule), the error classes, the attempts used out of 2, `fixes.diff`, per-stage times from `timeline.txt`, and the post-build `disk.txt` size of `out`.
- F7.2-07 — Collect the evidence before teardown
  - Description: Run runbook section 10, with F7.2-01's corrected symlink test, whatever the outcome. It writes:
    - `manifest-resolved.xml`, aborting if a credential-shaped URL appears;
    - `build-evidence.txt`: the consumed tree's `aon_front.pb` line, the built symlink at `vendor/lib64/camera/aon_front.pb` with its target, md5, size and path of `odm/lib64/hw/camera.qcom.so`, `odm/lib64/hw/camera.xiaomi.so` and `odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, and the common tree's `selinux` line;
    - 200-line log tails.

    It runs in `/android/beryl`, then runs the token scan and packs `evidence.tar.gz` into `~/out-pkg`. A missing file is recorded, not fatal. Compare the `camera.qcom.so` and sensor module md5s with `HAL_STOCK_MD5` and `EXPECT_MD5` as facts, not conclusions: they feed `Faz8.1`'s `F8.1-06`, which compares them with `IMPL-92`'s static values.
  - Output: `evidence.tar.gz`, holding the post-build evidence block for `Faz8.1` and `Faz7.3`.
- F7.2-08 — Retrieve every install artifact with sha256 at both ends
  - Description: Run runbook section 11.
    - On the server, from `/android/beryl`: copy each `aospa-*.zip` from the source root into `~/out-pkg`, the link to `/android/pkg` on the source volume, off the boot volume. Also copy `recovery.img`, `boot.img`, `init_boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img` and `vbmeta_system.img` from `out/target/product/ishtar`, beside `evidence.tar.gz`. Expect exactly one `aospa-*-image.zip` and two `aospa-*.zip`. A shortfall, a missing image or a failed copy is recorded in `~/out-pkg/retrieval.txt` and is not fatal (`AUDIT-FIX-54`). Then write `SHA256SUMS` over `~/out-pkg`.
    - The optional target-files archive: if the ceiling allows, also retrieve `aospa_ishtar-target_files.zip`. If it does not, record that the partition images are also inside the retrieved image package.
    - Anything not retrieved: name each artifact that could not be retrieved, with the package it can be extracted from.
    - On a failed build: only `evidence.tar.gz`, `retrieval.txt` and their `SHA256SUMS` exist.
    - On the host: `scp "builder@$BUILD_HOST:out-pkg/*"` into `~/Documents/Projeler/ishtar-builds/<date>/` and run `sha256sum -c SHA256SUMS`.

    Do not tear down until every file reports OK.
  - Output: The retrieved set with `sha256sum -c` passing for every file, stored outside every repository, and one line per artifact: retrieved, not produced, or extractable from a named package.
- F7.2-09 — Tear down
  - Description: Run runbook section 12 in order:
    1. `sha256sum -c` has passed on the host for every retrieved file.
    2. In the Scaleway Console, under CPU & GPU Instances in the section 6 zone, delete the Instance `ishtar-beryl-build`. Never power it off or leave it in standby: a powered-off Instance's volumes and flexible IP still bill, and standby bills as running (runbook section 3). In the dialog, check the boxes to delete its IPs and Block Storage volumes with it.
    3. Under Block Storage, Volumes, in the same zone, delete every volume still listed: the 40 GB system volume, `ishtar-src` and `ishtar-out`. The Instance API's `terminate` may only detach Block volumes, so assume they survived. `DEC-26` (c) keeps none.
    4. On the Flexible IPs tab, delete any flexible IP still listed. `terminate` preserves it, and it bills until deleted.
    5. Confirm under Block Storage Snapshots and Instances Images that none exist.
    6. Confirm billing stopped: the Project and zone list zero Instances, zero volumes, zero flexible IPs and zero snapshots. Record the time (UTC) of the last deletion. Elapsed hours are the last deletion minus creation, rounded up to whole hours and compared against the 10-hour ceiling.
    7. Confirm that no credential was issued (`DEC-25`).
    8. On the host, run `ssh-keygen -R "$BUILD_HOST"`, then `unset BUILD_HOST`.
  - Output: A teardown record: the Instance, each Block volume and the flexible IP deleted; the four zero counts; the last deletion time; the elapsed hours, rounded up, against the ceiling; and "no credential issued".
- F7.2-10 — State what Phase 8 inherits and write the ledger row
  - Description: Write the ledger row runbook section 13 names: per-stage exit status and elapsed time, error classes and log tails, fix attempts used with `fixes.diff`, the base and local manifest commits, the retrieved files with their sha256, the section 10 values, the `disk.txt` sizes of `.repo`, the tree and `out`, the Ubuntu release used, and the last deletion time with the rounded-up elapsed hours and section 12's four zero counts. Write the outcome as built, partial or blocked, check it against ledger section 7's viability trigger, and name what `Faz7.3`, `Faz8.1` and `Faz8.2` can now use. If `fixes.diff` is non-empty, record it as an input that lands on `ahmetxa/android_local_manifests` before any second rental, re-checked with `check.py`, pushed with the user's approval, and followed by updating the runbook's manifest commit.
  - Output: The ledger row, a Phase 8 readiness statement, the `fixes.diff` hand-off if any, and a replanning input if the trigger fires.

## 8. Acceptance Criteria

- The gate record exists and predates the rental. Runbook section 5's block exited 0 that day, and its four manual checks are confirmed: the identity-validated quota for POP2-32C-128G and 610 GB, the SSH key in the Project, the output directory, and the window. `DEC-25` and `DEC-26` are named. Runbook section 10's symlink test reads `vendor/lib64/camera/aon_front.pb` and passes `bash -n`.
- The rental followed the user's explicit approval. The start record carries Instance type, Availability Zone, image and creation time, without an address or volume ID.
- Before the sync and before the build, the work volume was confirmed mounted at `/android/beryl/out`, or the session stopped.
- No GitHub credential, token or deploy key was created for or placed on the server.
- Before the sync, the base read `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` and the local manifest read `22283d8a866d042e02336fcb4698253ac6bf9c3b`, or the session stopped on the mismatch.
- The sync completed, or its failure is characterised. `manifest-resolved.xml` shows the 13 pinned projects at their `ishtar-beryl.xml` commits.
- The shallow-sync item is marked tested with its result, or its fix's use is recorded.
- AON procedure step 1 found exactly one `aon_front.pb;SYMLINK=` line in the consumed tree, or a zero result is recorded as "the build never saw the fix".
- Every build attempt is recorded with its error class, stage reached and elapsed time. At most 2 fix attempts were made, each manifest-class and each in `fixes.diff`, and no fix was pushed during the session. An out-of-memory kill, if one occurred, was not retried.
- The runbook section 10 evidence exists whatever the outcome. If a build completed, it records md5 and size for the three camera blobs, and the symlink state and target at `vendor/lib64/camera/aon_front.pb`.
- If a build completed, every runbook section 11 artifact was retrieved before the server was deleted, with `sha256sum -c` passing, or its absence is recorded with the package it can be extracted from. No retrieved file sits inside a repository.
- **Whatever the build outcome:** the Instance, each of its three Block volumes and its flexible IP are deleted, not powered off. The Project and zone list zero Instances, zero volumes, zero flexible IPs and zero snapshots. Elapsed hours, from creation to the last deletion and rounded up to whole hours, are recorded against the 10-hour ceiling.
- The ledger row runbook section 13 names exists, and so does the Phase 8 readiness statement. Ledger section 7's viability trigger is explicitly evaluated. A non-empty `fixes.diff` is recorded as an input that lands on GitHub before any second rental.
- No credential value, server address or password appears in any retrieved file, snapshot, runbook edit or ledger row.

## 9. Validation and Test Approach

Validation spans a paid remote session and host-side checks after it. No device is involved.

- `VAL-GATE` (proposed) — runbook section 5's scripted block, whose `check.py` runs are `Faz7.1`'s `VAL-PINS` and `VAL-PINS-NEG` repeated that day; the four manual checks; and `bash -n` on the corrected section 10 block.
- `VAL-SYNC` (proposed) — runbook section 8's work-volume `mountpoint` check, its base and local manifest assertions, `repo sync`'s exit status, and `manifest-resolved.xml` compared on the host against the 13 pins in `ishtar-beryl.xml` at `22283d8`. The check compares revisions and does not trust exit status alone.
- `VAL-AON-TREE` (proposed) — `docs/aon-verification.md` section 5 step 1, read from the consumed-tree line in `build-evidence.txt`: exactly one `;SYMLINK=` line.
- `VAL-COMPILE` (proposed) — the build outcome per attempt from runbook section 9 and `timeline.txt`, with the stage reached and attempts used out of 2, and any out-of-memory kill recorded as a stop without retry. It is named apart from `VAL-BUILD`, which `Faz6.2` defined as the device-side AON verification and which `Faz7.3` executes.
- `VAL-BLOBMD5` (proposed) — the camera-blob block of `build-evidence.txt`: md5, size and path of the three blobs, plus the symlink state and target of `vendor/lib64/camera/aon_front.pb`.
- `VAL-RETRIEVE` (proposed) — on the host, `sha256sum -c SHA256SUMS` reports OK for every file. Each runbook section 11 artifact is present or its absence is recorded. The retrieval directory is outside every repository, and `git status --short` in the workspace shows no image or package.
- `VAL-TEARDOWN` (proposed) — runbook section 12:
  - the Instance is deleted;
  - each Block volume is deleted by name, since `terminate` may only detach it;
  - the flexible IP is deleted;
  - the Scaleway Console lists zero Instances, zero volumes, zero flexible IPs and zero snapshots in the Project and zone;
  - the last deletion time is recorded, and elapsed hours are rounded up and compared against the 10-hour ceiling;
  - no GitHub credential exists to revoke (`DEC-25`).
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

**Depends on** `Faz7.1`, which `IMPL-91` verified: a buildable manifest at `22283d8`, `DEC-22` and `DEC-25` answered, and `docs/build-environment.md` written. Depends on `Faz6.1` for the symlink entry that step 1 checks. Depends on the eleventh Step 3 audit, of planning run 20's amendment, before a Step 4 session runs it.

**Blocks** `Faz7.3` (no output, no flash) and `Faz8.1`'s `F8.1-06`. `Faz8.1`'s static half is done (`IMPL-92`: both layers carry-over on static values). `Faz8.2` is verified (`IMPL-93`) and does not wait on this sub-phase.

**Required decisions:** none new. `DEC-22`, `DEC-25` and `DEC-26` are answered. Reaching the stopping rule is not a decision point: it ends the session. Landing a non-empty `fixes.diff` on GitHub after the session needs the user's push approval.

**Required credentials:** none on the server (`DEC-25`). The user needs their Scaleway account, with identity validated, and their SSH key added to the Project the Instance is created in. The key's private half never leaves the Windows host. Neither is recorded anywhere.

**Required infrastructure:**

- the rented Scaleway POP2-32C-128G, with its three Block volumes (boot 40 GB 5K, `ishtar-src` 310 GB 5K, `ishtar-out` 260 GB 15K) and its flexible IPv4;
- network egress to GitHub, GitLab and the AOSPA sources;
- the host's `ishtar-builds/` directory, with room for the retrieved set;
- the WinGet `gh.exe` for runbook section 5.

**Required human approvals:**

- the Console checks in F7.2-01;
- renting, which spends money;
- deletion in the Console of the Instance, each Block volume and the flexible IP;
- any post-session push of `fixes.diff`.

**Fresh session token and context risk:** medium, per Main-Planing's Phase 7 band, rising to high if the build fails repeatedly. The hazard is sync and build output volume. Mitigation: record per stage what runbook section 4 names — start and end time, exit status, error class and the last lines of a failing log — never whole logs, and keep the stopping rule in the session's own context. Subagents: not recommended; the session drives a single stateful remote resource.

## 11. Risks and Mitigations

- Risk: the build nearly works and the server stays up. Impact: a cost overrun, the failure `DEC-24` was designed around. Mitigation: the 10-hour ceiling (`DEC-25`, kept by `DEC-26`) and the hour-8 retrieve-and-delete rule are in force before renting, and teardown is an acceptance criterion independent of the outcome.
- Risk: the Instance is powered off instead of deleted, or a Block volume or the flexible IP outlives it. Impact: billing continues. When powered off, "only its volumes and any reserved flexible IP address are billed"; standby bills as a running Instance; and `terminate` may only detach Block volumes while it preserves the flexible IP. Mitigation: F7.2-09 follows runbook sections 3 and 12 and deletes each resource by name. `VAL-TEARDOWN` requires zero Instances, volumes, flexible IPs and snapshots.
- Risk: the account cannot create the planned rental. Identity may not be validated, the quota may fall short of POP2-32C-128G or 610 GB, the key may sit in another Project, or Ubuntu 22.04 may not be offered. Impact: a stalled rental day, or a silent switch to another type or to smaller volumes. Mitigation: F7.2-01 checks the quota and the key before renting and stops on failure. The image falls back only as `DEC-22` allows.
- Risk: runbook section 7's volume block formats or mounts the wrong disk, or the work volume is not mounted and `out` fills the source or boot volume. Impact: a failed sync or build partway through a billed session. Mitigation: volumes are picked by size, never by `/dev/sdX` order, and cross-checked against their Console volume IDs. `mkfs` runs only where `blkid` finds no filesystem, and sections 8 and 9 refuse to run unless `/android/beryl/out` is a mountpoint. The block has passed `bash -n` but has never run (`IMPL-95`), so its first run is on the rented Instance.
- Risk: the build is killed for memory. Impact: billed hours with no output. Mitigation: POP2-32C-128G has 128 GiB, plus runbook section 7's 16 GB swap file. An out-of-memory kill is not retried (`DEC-26` (d)), so it costs at most one build and becomes a replanning input.
- Risk: a fix made on the server is lost with the server. Impact: the output cannot be reproduced, and the next rental repeats the discovery. Mitigation: runbook section 4 records every fix in `fixes.diff`, which travels in `evidence.tar.gz`, and F7.2-10 hands it to GitHub before any second rental.
- Risk: a masked exit code lets a failed step look successful (`IMPL-90`'s defect class). Impact: the session proceeds on a broken sync or build, and the evidence is wrong. Mitigation: every runbook block starts with `set -euo pipefail`, runbook section 9 catches barista's unchecked exit status, and `VAL-SYNC` compares revisions.
- Risk: runbook section 10's symlink test reads the wrong path. Impact: a correct build's AON result looks failed, and `Faz7.3` is misdirected. Mitigation: F7.2-01 corrects the path to `vendor/lib64/camera/aon_front.pb` before renting, and an acceptance criterion checks it.
- Risk: a credential reaches the server or a retrieved file. Impact: a live token in a log or in `repo manifest -r`. Mitigation: `DEC-25` made the repositories public, so no credential is issued. Runbook section 10's credential-URL check and token scan run before anything is copied.
- Risk: an install artifact is missing when `Faz7.3` flashes. Impact: a second paid sync and build. Mitigation: F7.2-08 retrieves and verifies every runbook section 11 artifact before deletion, or records which package it can be extracted from.
- Risk: a blob-bearing output is published, for example as a public release. Impact: proprietary blob redistribution, contrary to `ARC-04`. Mitigation: out of scope by rule; retrieval is private and verified by sha256.
- Risk: a retrieved image is committed by accident. Impact: repository bloat, and blobs in a remote. Mitigation: runbook sections 5 and 11 store outputs outside every repository, and `VAL-RETRIEVE` reads `git status`.
- Risk: shallow sync fails partway through. Impact: wasted hours. Mitigation: the fix in runbook section 4's deferred-items table, counted against the 2 attempts. The manifest `README.md` puts full history at about 1.8 GiB for the `ishtar` vendor repository and 0.3 GiB for `sm8550-common`, well inside the 310 GB source volume.
- Risk: the AON step 1 check is skipped because the build dominates attention. Impact: `Faz7.3`'s device result becomes uninterpretable, since a missing providers result could simply mean the tree lacked the entry. Mitigation: runbook section 10 records the consumed-tree line before teardown whatever the outcome, and F7.2-05 is a distinct work item.
- Risk: the post-build md5 read is skipped. Impact: `Faz8.1` has only the vendor-repository value, and a fixup or build step that altered the file goes unseen. Mitigation: F7.2-07 is a distinct work item on the runbook's evidence list.

## 12. Desired End State

An AOSPA `beryl` build for `ishtar` has been attempted on a rented Scaleway POP2-32C-128G from the inputs at `22283d8`, following runbook sections 5 to 13, and the outcome is recorded. If it completed, every runbook section 11 artifact sits in `ishtar-builds/` on the user's machine, outside every repository, with `sha256sum -c` passing. The resolved manifest proves the build came from the pinned inputs. The consumed tree carried the AON entry, the built symlink state at `vendor/lib64/camera/aon_front.pb` is known, and so is the md5 of the guarded camera blobs as built. Whatever the outcome, the Instance, its three Block volumes and its flexible IP are deleted, and zero of each and zero snapshots are listed. No credential ever existed on the Instance, and the elapsed hours, rounded up, are recorded against the 10-hour ceiling. Phase 8 has a readiness statement, ledger section 7's viability trigger has been evaluated, and any `fixes.diff` is waiting to land on GitHub.

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
- the `disk.txt` sizes of `.repo`, the tree and `out`, and the Ubuntu release used;
- the last deletion time, the elapsed hours rounded up against the ceiling, and section 12's four zero counts.

It also carries the shallow-sync and AON step 1 verdicts, and what Phase 8 inherits.

## 13. Next Sub-Phase Transition Criteria

- The Instance, each of its Block volumes and its flexible IP are deleted, and the Console lists zero Instances, volumes, flexible IPs and snapshots. No credential was issued. This holds even when the build failed.
- Elapsed hours, rounded up, are recorded against the 10-hour ceiling (`DEC-25`, kept by `DEC-26`).
- For `Faz7.3`, all of the following are recorded; without them, `Faz7.3` does not start:
  - every runbook section 11 artifact exists locally with `sha256sum -c` passing, or its absence is recorded with the package it can be extracted from;
  - the AON step 1 result;
  - the built symlink state.
- For `Faz8.1`: the post-build md5s and sizes of `camera.qcom.so` and the sensor module are recorded for `F8.1-06`, or their absence is explained.
- The Phase 8 readiness statement is written, any section 7 trigger is raised in the ledger, and a non-empty `fixes.diff` is recorded as landing on GitHub before any second rental.
