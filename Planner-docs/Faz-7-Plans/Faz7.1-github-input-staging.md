# Faz 7.1 — GitHub Input Staging and Pre-Rental Readiness

## 1. Context

Main-Planing Phase 7, as amended by planning run 17 on 2026-09-10 (`SNAP-2026-09-10-MAIN`), sets the goal "Reach the point where an AOSPA Android 16 (`beryl`) build for `ishtar` can be attempted, at the lowest rental cost." The host is no longer WSL2: under `DEC-24` the build runs on a rented Hetzner VDS, and "rental is billed by time, so every input the build needs is prepared on the user's GitHub account (`ahmetxa`) before a server is rented". The phase's first vibecoding slice is exactly this sub-phase: "Before renting anything, stage the device tree and a local manifest on GitHub and prove from the Windows host that every pinned project resolves to a commit on its branch." Its closing note adds that the server's distribution (`DEC-22`) "is decided from the AOSPA build requirements before renting".

**This sub-plan replaces `Faz-7-Plans/Faz7.1-wsl2-provisioning.md`,** whose work items `F7.1-02` through `F7.1-09` described a WSL2 install that `DEC-24` retired. The one item that sub-plan completed — `F7.1-01`, `DEC-22` recorded open with the AOSPA/AOSP build requirements as its deciding criterion (`IMPL-86`) — carries over, reframed by `DEC-24` to the server's image. The old file is removed by this re-plan rather than kept as a second Phase 7.1, so no work item numbering from it survives; `IMPL-86` and `IMPL-89` refer to it by its old path as history.

Work has already started ahead of this re-plan, at the user's direction. `IMPL-90` (2026-09-10) created the private workspace remote `ahmetxa/ishtar` (`DEC-01`), branch `beryl` = `d48816f` on `ahmetxa/android_device_xiaomi_ishtar` (upstream `xiaomi-8550` `df05661` plus the `Faz6.1` symlink commit), and the private `ahmetxa/android_local_manifests` at `4182695`, which pins four projects and whose `README.md` lists **seven open items** and says "Status: INCOMPLETE — not buildable yet." This sub-plan starts from that observed state and closes it; it does not re-stage anything `IMPL-90` already verified.

Continuity sources: ledger `DEC-22`, `DEC-24`, `DEC-01`, `IMPL-89` (GitHub API reads of `AOSPA/manifest` and `xiaomi-8550`) and `IMPL-90`; Project-Ontology section 2 (`beryl` corrected to "AOSPA's Android 16 branch, not a device") and invariant 11, which still states the retired WSL2 host constraint; Project-Comprehension `EV-20` and `CQ-13`, which still name WSL2 as the Android 16 blocker; risk `R9`.

## 2. Goal

Every input the first AOSPA `beryl` build for `ishtar` needs resolves on GitHub to a pinned commit, every open item in the local manifest is either closed with evidence or deferred with a named build-time detector and fallback, and the rental session is fully specified — server image, sizing, credentials, stopping rule, evidence list and teardown — before any server is rented.

## 3. Description

The problem this sub-phase solves is cost-shaped rather than capability-shaped. On a rented server every unresolved input is discovered at an hourly rate: a missing `hardware/xiaomi` branch, a sepolicy tree that only exists for an older branch, or a kernel path the build expects and the manifest does not provide each surfaces minutes to hours into a sync or a build. The same questions can be answered from the Windows host for free, through GitHub reads and the trees already checked out under `refs/`.

It belongs first in Phase 7 because Phase 7's own first slice says so, and because `Faz7.2` has no safe starting point without it: the manifest is explicitly not buildable yet. It prepares Phase 8 as well — the kernel question in open item 3 decides which tree `Faz8.2` scopes, and the pinned vendor commit is what `Faz8.1` compares.

The vibecoding slice strategy: first, re-run `IMPL-90`'s own proof (`check.py`, positive and known-bad) to confirm the staged state still holds — minutes, and it prevents building on a stale assumption. Then close open items one at a time, each producing either a pin that `check.py` resolves or a written deferral. The fastest validation signal for each item is `check.py` resolving the new pin; for items that cannot be pinned before a build (for example whether shallow sync works), the signal is a written detector and fallback that `Faz7.2` executes.

What should not be over-planned: the exact package list and build flags. Those follow `DEC-22` and AOSPA's own documentation, which this sub-phase reads rather than guesses. Build errors are not planned at all; `Faz7.2`'s stopping rule owns them.

One lesson from `IMPL-90` is carried as a rule rather than a note: its first device-tree push sent the wrong commit because `git am` failed, a pipe into `tail` masked the exit code, and the push was not gated on the comparison. Every scripted step written here — on the host or in the rental runbook — must fail on a non-zero exit (`set -euo pipefail` or the equivalent) and gate each publish on a read-back.

## 4. Scope

- Verification of the state `IMPL-90` staged: the three repositories, their privacy, the four pins, and `check.py` in both directions.
- Closure or explicit deferral of the seven `README.md` open items: `hardware/xiaomi`, `device/xiaomi/sepolicy`, the kernel (paths, QCOM driver and devicetree repositories), QCOM display/audio overrides, `vendor/xiaomi/camera`, the server distribution (`DEC-22`), and shallow sync of the 1.9 GB vendor repository.
- Recording the `AOSPA/manifest` `beryl` commit the build will start from, so the base is as reproducible as the local manifest.
- Extension of `check.py` for any new manifest element kind, keeping the positive-and-known-bad proof `IMPL-90` established.
- Settling `DEC-22` with the user from AOSPA's and AOSP's published build host requirements, plus a server sizing floor (CPU, memory, disk) with its source.
- A rental budget and stopping rule agreed with the user and recorded as a ledger decision before any rental.
- A least-privilege credential plan for the server: what GitHub access it needs, how it is scoped, and when it is revoked.
- The rental runbook `docs/build-environment.md`: provisioning, authentication, sync, build, the evidence list, output retrieval with checksums, and teardown.
- Retirement of the WSL-era records: Project-Ontology invariant 11, Project-Comprehension `EV-20` and `CQ-13`, and `docs/reverse-engineering-toolchain.md` section 7.
- Secure-by-design expectation: no token, SSH key, password or server address is written into any repository, runbook, snapshot or planning file.

## 5. Out of Scope

- Renting, provisioning or logging into a server. `Faz7.2` owns the paid session.
- Any source sync or build, including a trial sync of a single project on a rented machine.
- Flashing anything. `Faz7.3` owns the device.
- Mirroring upstream repositories into the user's account. `IMPL-90` decided to pin, not mirror, because the server fetches at datacenter speed; this sub-phase keeps that decision.
- Changes to the device trees beyond what an open item proves necessary to make the manifest resolve. Build fixes belong to `Faz7.2`.
- Camera blob comparison (`Faz8.1`) and kernel merge scoping (`Faz8.2`), although open item 3's answer feeds `Faz8.2`.
- `calcite`. The manifest `README.md` and Main-Planing both evaluate it only after `beryl` builds and boots.
- Release signing keys. The first build uses AOSPA's default signing; no project key, including `ishtar-cam-modes/tile-app/debug.keystore`, goes near the server.
- Editing `Planner-docs/Faz-6-Plans/Faz6.1-*.md` or `Faz6.2-*.md`, whose WSL2 sentences are history under the snapshot they executed against.

## 6. Current Repository Evidence

**Staged on GitHub (`IMPL-90`, re-read this planning run through `gh api`, read-only).** `ahmetxa/android_local_manifests` holds exactly `README.md`, `check.py` and `ishtar-beryl.xml`. The manifest declares one remote, `https://github.com`, and pins four projects to full commit ids with an `upstream` branch: `device/xiaomi/ishtar` → `ahmetxa/android_device_xiaomi_ishtar` `d48816fb…` on `beryl`; `device/xiaomi/sm8550-common` → `xiaomi-8550/android_device_xiaomi_sm8550-common` `a0a70422…` on `beryl`; `vendor/xiaomi/ishtar` → `xiaomi-8550/proprietary_vendor_xiaomi_ishtar` `f92e7a90…` on `beryl` ("about 1.9 GB"); `vendor/xiaomi/sm8550-common` → `xiaomi-8550/proprietary_vendor_xiaomi_sm8550-common` `e0d20e8f…` on `beryl`. The `README.md` records the blob lists' source firmware as `OS2.0.101.0.VMAMIXM` for `ishtar` and `OS2.0.100.0.VMCMIXM` (from `fuxi`) for the common tree. `ahmetxa/android_device_xiaomi_ishtar` reads `private=true`, default branch `vauxite`. `IMPL-90` proved `check.py` 4/4 on the real manifest and 5/5 on a known-bad one.

**The seven open items, verbatim in substance from the `README.md`.** (1) `xiaomi-8550/android_hardware_xiaomi` has no `beryl` branch, only `vauxite` and `calcite`. (2) The common tree includes `device/xiaomi/sepolicy/SEPolicy.mk`, and `xiaomi-8550/device_xiaomi_sepolicy` has only `uvite`. (3) `xiaomi-8550/android_kernel_qcom_sm8550` (`b11e560`) and `android_kernel_xiaomi_sm8550` (`1c509b3`) have `beryl` branches, but their build paths and the QCOM driver and devicetree repositories are not determined. (4) `xiaomi-8550` carries `android_hardware_qcom_display` and `android_vendor_qcom_opensource_arpal-lx` on `beryl-8550`; whether they replace AOSPA projects is not determined. (5) `vendor/xiaomi/camera` is `inherit-product-if-exists` and its `xiaomi-8550` repository is empty. (6) Server distribution, `DEC-22`. (7) Shallow sync of the vendor repository is untested.

**Local reference trees, measured this run.** `refs/a16_ishtar` is on `beryl` at `df056613…` and `refs/a16_sm8550` on `beryl` at `a0a70422…` — the latter equal to the manifest pin. `refs/a16_sm8550/common.mk:122-135` sets `TARGET_KERNEL_DLKM_DISABLE := false` and thirteen `TARGET_KERNEL_DLKM_*_OVERRIDE := true` flags, including `CAMERA`, which is direct evidence that open item 3 involves kernel module repositories and not only a kernel tree. `refs/a16_ishtar/board-info.txt` contains only `require board=ishtar`. `IMPL-89` recorded that `xiaomi-8550/android_device_xiaomi_ishtar-kernel` has only `uvite` and `vauxite`, which bears on whether `beryl` expects a prebuilt kernel or a source build.

**Workspace records that still name the retired host.** Project-Ontology invariant 11 reads "Sources must live inside the WSL filesystem … WSL2 is not installed." `EV-20` reads "WSL2 is not installed and blocks the Android 16 track" (`probable`). `CQ-13` ("What blocks the Android 16 track?") is marked answered with that blocker. `docs/reverse-engineering-toolchain.md` section 7 says provisioning WSL2 "is Phase 7's entire purpose (`Faz7.1`)". `docs/build-environment.md` does not exist.

**Host tooling.** `gh` is installed and authenticated as `ahmetxa`, but only at `%LOCALAPPDATA%\Microsoft\WinGet\Packages\GitHub.cli_…\bin\gh.exe`; it is not on the Bash or PowerShell `PATH` in this session, which `check.py`'s `GH=` override already anticipates. Python 3.14.7 is available as `python`; `python3` is the Windows Store stub (ledger section 6). `git` is 2.55.

## 7. Planned Work Breakdown

- F7.1-01 — Verify the staged state before extending it
  - Description: Read back `IMPL-90`'s three repositories (existence, privacy, default branches), re-run `check.py` on the real manifest and on a known-bad copy, and confirm `d48816f` differs from `df05661` by exactly the `Faz6.1` line. Nothing is recreated if it verifies.
  - Output: A dated verification record; any drift raised as a finding instead of silently repaired.
- F7.1-02 — Settle `DEC-22` and the server sizing floor
  - Description: Read AOSPA's published build instructions for `beryl` and AOSP's host requirements, and put a distribution, version and minimum CPU/memory/disk to the user with each figure's source. The criterion stays the one `IMPL-86` recorded: the build requirements, not familiarity.
  - Output: `DEC-22` answered in ledger section 8; the sizing floor written into the runbook with sources.
- F7.1-03 — Close open item 1, `hardware/xiaomi`
  - Description: Determine what the `beryl` trees include from `hardware/xiaomi` and whether AOSPA's own `beryl` manifest already provides it; choose `vauxite`, `calcite` or AOSPA's project with evidence, or defer with the build-time error that would reveal a wrong choice and the fallback order.
  - Output: A pin resolved by `check.py`, or a written deferral.
- F7.1-04 — Close open item 2, `device/xiaomi/sepolicy`
  - Description: Same method as F7.1-03 for the sepolicy include; record whether `uvite` is plausibly compatible or whether another source exists.
  - Output: A pin or a written deferral.
- F7.1-05 — Close open item 3, the kernel
  - Description: Determine from the `beryl` trees whether the build expects a prebuilt kernel or a source build, the paths it expects, and — given the thirteen DLKM override flags — which kernel module and devicetree repositories must accompany the two `beryl` kernel trees. Record which kernel tree is the one the build consumes, because `Faz8.2` scopes that tree.
  - Output: Kernel pins with paths, or a written deferral; a one-line note for `Faz8.2` naming the consumed kernel tree.
- F7.1-06 — Close open items 4 and 5
  - Description: Compare the `beryl-8550` display and audio repositories against the projects AOSPA's `beryl` manifest provides at the same paths, and decide override (`remove-project` plus `project`) or no override. Confirm `vendor/xiaomi/camera` can be omitted, since the include is conditional.
  - Output: Override entries or a recorded "no override" with reasons; item 5 closed.
- F7.1-07 — Pin the base manifest
  - Description: Record the `AOSPA/manifest` `beryl` commit the rental will initialise from, and state in the runbook how the server uses it and how `Faz7.2` records `repo manifest -r` afterwards.
  - Output: A base commit id in the manifest `README.md` and the runbook.
- F7.1-08 — Extend `check.py` without weakening its proof
  - Description: If F7.1-03 to F7.1-07 add element kinds `check.py` does not handle (for example `remove-project`), extend it, then repeat `IMPL-90`'s two-way proof with a known-bad case per new failure reason.
  - Output: `check.py` resolving every pin with exit 0 and failing each known-bad case on its intended reason with exit 1.
- F7.1-09 — Decide shallow sync, item 7
  - Description: Specify the sync depth for the large vendor repositories, mark it untested, and write the fallback (full sync) and its disk consequence into the runbook, so `Faz7.2` tests it inside the stopping rule rather than discovering it.
  - Output: A sync specification with a named detector and fallback.
- F7.1-10 — Agree the rental budget, stopping rule and credential plan with the user
  - Description: Put to the user a ceiling (hours or currency), the conditions that stop an attempt, and how the server gets read access to the private repositories: a fine-grained read-only token limited to them and revoked at teardown, or making the device-tree fork public (it holds an upstream tree plus one line) so the server needs no credential for it. The chosen plan never involves writing a credential value anywhere.
  - Output: A ledger section 8 decision row for budget and stopping rule; the credential plan in the runbook.
- F7.1-11 — Write the rental runbook
  - Description: `docs/build-environment.md`: provisioning for the `DEC-22` image; authentication per F7.1-10; `repo init` at the F7.1-07 base and `repo sync` per F7.1-09; the build command AOSPA documents; the evidence list `Faz7.2` must capture before teardown (`repo manifest -r`; the `aon_front.pb` entry in the consumed tree; md5 and size of `odm/lib64/hw/camera.qcom.so`, `odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin` and `camera.xiaomi.so` from the build output; the symlink's presence in the built vendor staging directory; error classes and elapsed time); output retrieval with sha256 at both ends; teardown (delete the server, revoke the token, confirm billing stopped). Every scripted step fails on a non-zero exit.
  - Output: A runbook that `Faz7.2` can follow without re-planning.
- F7.1-12 — Retire the WSL-era records
  - Description: Rewrite Project-Ontology invariant 11 to the `DEC-24` host constraint, move `EV-20` from the retired claim to the decided host with `DEC-24` as its source, re-answer `CQ-13` with the manifest open items as the blocker, and correct `docs/reverse-engineering-toolchain.md` section 7's `Faz7.1` sentence.
  - Output: Four updated records, each citing `DEC-24`.

## 8. Acceptance Criteria

- `IMPL-90`'s staged state is re-verified on the day of execution before any extension, and any drift is recorded as a finding.
- `check.py` resolves every pin in `ishtar-beryl.xml`, including every pin added here, with exit 0; a known-bad manifest fails on each intended reason, including one per new element kind, with exit 1.
- Each of the seven open items is either closed with a cited source or deferred with a named build-time detector and a fallback; none reads "not yet determined" at the end.
- The kernel tree the build consumes is named, and that name is handed to `Faz8.2`.
- The `AOSPA/manifest` `beryl` base commit is recorded.
- `DEC-22` is answered by the user, and the sizing floor cites the published requirement it came from.
- The rental budget and stopping rule are recorded as a ledger decision before any rental, and the credential plan grants read access only, with revocation at teardown.
- `docs/build-environment.md` exists and contains provisioning, authentication, sync, build, the evidence list of F7.1-11, retrieval with sha256, and teardown; every scripted step is written to fail on a non-zero exit.
- Invariant 11, `EV-20`, `CQ-13` and `docs/reverse-engineering-toolchain.md` section 7 no longer describe WSL2 as the plan.
- No server was rented, and no token, key, password or server address appears in any file in this repository or in `ahmetxa/android_local_manifests`.

## 9. Validation and Test Approach

Validation is host-side and network-read-only for GitHub, plus document read-back. No device and no server are involved.

- `VAL-PINS` (existing method, `IMPL-90`) — `python check.py` from a local clone of `ahmetxa/android_local_manifests` with `GH` pointed at the installed `gh.exe`; expect every project resolved and exit 0.
- `VAL-PINS-NEG` (existing method, extended here) — the same script against a deliberately broken copy; expect each failure on its intended reason and exit 1.
- `VAL-OPENITEMS` (proposed) — read back the manifest `README.md` open-items section; every item closed or deferred with detector and fallback.
- `VAL-SYNTAX` (proposed) — `bash -n` over any shell script the runbook introduces, and a read that every scripted block sets fail-on-error.
- `VAL-DOCS` (proposed) — read back `docs/build-environment.md` against the F7.1-11 list, and the four retired records against F7.1-12.
- `VAL-SEC` (proposed) — the bundled validator's secret scan over `Planner-docs/`, plus a file-name-only scan (`git grep -l`) of the workspace and the manifest clone for token-shaped strings and private-key headers; never print a match.
- Ledger evidence for Step 4: one implementation row naming the open items closed, the pins added, `check.py` results both ways, `DEC-22`, and the budget decision id.

Local versus live: everything here is local or a read against GitHub. "Live" for this phase means a rented server, which this sub-phase is forbidden to touch. Ontology validation applies to invariant 11 and to the `beryl` vocabulary: `beryl` is a branch, `ishtar` is the device.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| docs/build-environment.md | proposed | The rental runbook: provisioning, credentials, sync, build, evidence list, retrieval and teardown. | VAL-DOCS, VAL-SYNTAX, VAL-SEC |
| refs/a16_ishtar/proprietary-files.txt | existing | Read-only: confirms the `aon_front.pb` symlink entry the build must consume. | VAL-DOCS |
| refs/a16_sm8550/common.mk | existing | Read-only evidence for open item 3: the DLKM override flags. | VAL-OPENITEMS |
| refs/a16_ishtar/extract-files.py | existing | Read-only: the blob fixups the vendor repository reflects, needed for the runbook's evidence list. | VAL-DOCS |
| docs/reverse-engineering-toolchain.md | modified | Section 7's boundary sentence corrected from WSL2 to `DEC-24`. | VAL-DOCS |
| Planner-docs/Project-Ontology.md | modified | Invariant 11 rewritten to the rented-server host constraint. | VAL-DOCS |
| Planner-docs/Project-Comprehension.md | modified | `EV-20` and `CQ-13` moved off the retired WSL2 claim. | VAL-DOCS |
| Planner-docs/Planing-Ledger.md | modified | `DEC-22` answered; the budget and stopping-rule decision row; the implementation row. | VAL-DOCS, VAL-SEC |

The manifest repository's files (`ishtar-beryl.xml`, `check.py`, `README.md`) are the other half of this sub-phase's output. They live in the private GitHub repository `ahmetxa/android_local_manifests`, not in this workspace, so they are named in the work breakdown rather than in the table; Step 4 must not create a copy of that repository inside this workspace.

## 10. Dependencies and Sequencing

Depends on `IMPL-90`'s staging, which exists, and on `DEC-24` and `DEC-01`, both answered. `Faz1.1` (version control) and `Faz6.1` (the symlink entry) are complete.

Blocks `Faz7.2` absolutely: the manifest is not buildable until this sub-phase ends. Feeds `Faz8.2` with the consumed kernel tree, and `Faz8.1` with the pinned vendor commit it compares.

Does not depend on Phases 2 through 5 or 9. Main-Planing's consolidation-first conclusion was satisfied in practice: Phase 3 is marked successful (`DEC-21`) and Phase 9's release tooling is verified.

Required decisions, all the user's: `DEC-22`; the rental budget and stopping rule; the credential plan, including whether the device-tree fork stays private.

Required credentials: the host `gh` session, already authenticated. No server credential exists yet and none is created here.

Required infrastructure: network access to GitHub from the Windows host. No server.

Required human approvals: the three decisions above, and approval for each push to `ahmetxa/android_local_manifests` or the device-tree fork.

Fresh session token and context risk: medium. The hazard is many small GitHub reads across unfamiliar repositories. Mitigation: record one verdict per open item with its source, not transcripts. Subagents: not recommended; the reads are sequential, and each depends on the previous item's answer.

## 11. Risks and Mitigations

- Risk (`R9`): an open item is judged closed on reading alone and fails on the server. Impact: paid rework, exactly what `DEC-24`'s staging exists to avoid. Mitigation: every closure cites its source, and items that cannot be proven before a build are deferred with a named detector and fallback rather than being marked closed.
- Risk: the `IMPL-90` defect class recurs — a masked exit code publishes the wrong commit. Impact: the server builds from something other than what was verified. Mitigation: fail-on-error in every script, and each push gated on a read-back comparison, as section 3 requires.
- Risk: a credential leaks into a repository, runbook or snapshot. Impact: account compromise; a private remote does not make a committed token safe. Mitigation: F7.1-10's plan never writes a value, the runbook refers to the token by role only, and `VAL-SEC` scans by file name.
- Risk: the wrong `hardware/xiaomi` or sepolicy branch is chosen because only a neighbouring branch exists. Impact: a build break far into compilation. Mitigation: F7.1-03 and F7.1-04 prefer AOSPA's own manifest where it provides the project, and record the fallback order for `Faz7.2`.
- Risk: the kernel is misunderstood as a single tree when the build needs module and devicetree repositories too. Impact: a failed kernel stage, and `Faz8.2` scoping the wrong tree. Mitigation: F7.1-05 starts from the thirteen DLKM override flags measured in `common.mk` and names the consumed tree explicitly.
- Risk: the server is undersized or the wrong image is chosen. Impact: out-of-memory or out-of-disk failures during a paid session. Mitigation: F7.1-02 cites published requirements for both image and sizing floor, and F7.1-09 states the full-sync disk consequence.
- Risk: blob-bearing build inputs or outputs end up published. Impact: redistribution of proprietary vendor blobs, which `ARC-04` records the project never does. Mitigation: the plan pins upstream repositories rather than mirroring them, and the runbook retrieves outputs privately.
- Risk: the WSL-era records are left standing. Impact: a future session re-reads invariant 11 or `EV-20` and plans a WSL2 install again. Mitigation: F7.1-12.

## 12. Desired End State

`ahmetxa/android_local_manifests` describes a complete `beryl` build for `ishtar`: every project pinned to a full commit id, every override justified, the base manifest commit recorded, and `check.py` proving all of it in both directions. Every former open item is closed or carries a detector and fallback. `DEC-22` is answered, the sizing floor is sourced, and the budget, stopping rule and credential plan are the user's recorded decisions. `docs/build-environment.md` lets a single paid session run from provisioning to teardown without re-planning. The workspace no longer describes WSL2 as the plan. No server has been rented.

Evidence the implementer produces: the verification record of `IMPL-90`'s state, `check.py` output both ways, per-item closure sources, the `DEC-22` answer with sources, the budget decision id, and the runbook.

The ledger summary Step 4 appends: open items closed or deferred (by number), pins added, the consumed kernel tree, `check.py` results, `DEC-22`, the budget decision id, and the four retired records.

## 13. Next Sub-Phase Transition Criteria

- `check.py` passes both ways on the final manifest, on the day `Faz7.2` starts.
- No manifest open item reads "not yet determined".
- `DEC-22`, the rental budget and the stopping rule are recorded decisions.
- `docs/build-environment.md` is complete, and its evidence list includes the blob md5s `Faz8.1` needs and the AON check `Faz7.3` needs.
- The credential plan is read-only and includes revocation.
- No credential value exists in any file, and no server has been rented.
