# Faz 8.2 — Kernel LTS Merge Scoping

## 1. Context

Main-Planing Phase 8 (`SNAP-2026-09-10-MAIN`) pairs the camera work on the Android 16 vendor blobs with "(2) merging GKI LTS into the kernel tree", and its acceptance signal includes "kernel merge with no regressions in camera or sensor paths". Both parts "depend on Phase 7". Its desired end state includes "the kernel tree is on a current LTS base."

**Reviewed and rewritten 2026-09-10 by planning run 18.** Phase 8's re-scope did not change this sub-plan's purpose, which stays a commit-or-defer assessment routed to the user as `DEC-08`. It did remove four premises the previous version rested on, and each is replaced with measured evidence:

- **The host.** The previous version depended on "Faz 7.1 for a Linux environment" and required the assessment to run "against a Linux-side clone rather than the Windows copies". `DEC-24` retired WSL2, and a rented server bills by time.
- **The target.** It named the three local checkouts as the candidates. The kernel an Android 16 build consumes is on `beryl` branches, and `Faz7.1` F7.1-05 names the consumed tree.
- **The source of base facts.** It planned to read `kernel_clone.log` and `common_clone.log` as "the cheapest source". Measured this run, they are 86 and 32 bytes, and `kernel_clone.log` holds only `fatal: destination path 'kernel_ishtar' already exists and is not an empty directory.` They carry no base information.
- **The checkout roles.** It called `common_sm8550/` a kernel tree. Measured this run, it is `AOSPA/android_device_xiaomi_sm8550-common` on `vauxite` — a device tree, not a kernel.

The project's reason to care is unchanged. Project-Ontology invariant 3 records that killing the camera provider while a stream is live "leaks CSIPHY/CSID allocations in the QCOM kernel driver and produces a black preview in every mode". `setmode.sh`'s client-before-HAL ordering works around exactly that driver behaviour, and a kernel change could alter it in either direction.

## 2. Goal

Establish what merging a current GKI LTS release into the kernel the Android 16 `ishtar` build consumes would involve, and what it would risk for the camera and sensor paths. Separate the core kernel merge from the out-of-tree camera driver it may not touch at all. Route a commit-or-defer recommendation as `DEC-08`, without renting a server for the estimate.

## 3. Description

The problem is that a kernel merge is easy to name and hard to bound. The distance to a current LTS release, the conflict surface, and the effect on the camera path are all unmeasured, and the camera path is where this project's value lives.

It belongs in Phase 8 after `Faz7.1` because the merge target is whichever kernel the `beryl` build consumes, which `Faz7.1` determines. It does not need `Faz7.2`'s build to estimate. It does need a build to validate, and validation is not in scope.

The vibecoding slice strategy is measure before merge, on the cheapest host. The first useful slice identifies the consumed tree's base: its `Makefile` `VERSION`/`PATCHLEVEL`/`SUBLEVEL` and its last merged Android common kernel tag. That is two reads on the `beryl` branch. The second slice estimates conflicts **without a checkout**. `git merge-tree --write-tree` (git ≥ 2.38; the host has 2.55) computes a merge in the object database and lists conflicted paths, so the NTFS case-collision problem that forced sparse checkouts on this host never arises. That keeps the estimate off a rented server. The method is unproven on this host and must first be shown on a small known merge.

The camera-path question has a structural twist this rewrite adds as a hypothesis, not a fact. `refs/a16_sm8550/common.mk:125` sets `TARGET_KERNEL_DLKM_CAMERA_OVERRIDE := true`, which suggests the QCOM camera driver — CSIPHY and CSID included — is built as a separate kernel module from its own repository rather than from the core kernel tree. If so, a GKI LTS merge into the core tree would not change the CSIPHY/CSID allocation code directly. It would change only the kernel interfaces that module builds against. That would move invariant 3's risk from "the merge rewrites the driver" to "the driver must still build and behave against the merged interfaces". F8.2-04 tests this before it shapes any conclusion.

What should not be over-planned: conflict resolution, a merge schedule, or the build-and-flash validation a merge would need. Those follow `DEC-08`.

## 4. Scope

- Identifying the consumed kernel tree from `Faz7.1` F7.1-05, and its companion module and devicetree repositories.
- The consumed tree's base: kernel version from `Makefile`, and the last merged Android common kernel tag.
- The current GKI LTS target for that kernel generation, and the distance as a concrete count (commits or tags between base and target).
- A proof that `git merge-tree --write-tree` works on this host in a blobless bare clone, shown on a small known merge first.
- A conflict-surface estimate from that method, split into camera and sensor paths (camera, media/V4L2, I2C/I3C, CCI, regulator and clock paths used by camera) versus everything else.
- Testing the hypothesis that the CSIPHY/CSID driver lives in a separate camera kernel module repository, and if it does, identifying which kernel interfaces that module uses that the merge changes.
- A statement of the role of each local checkout, measured: `android_kernel_xiaomi_sm8550` and `android_kernel_qcom_sm8550` (AOSPA, `vauxite`, 5.15.178) and `common_sm8550` (a device tree).
- An independence assessment: what in the roadmap, if anything, requires the merge.
- A commit-or-defer recommendation routed as `DEC-08`, stating what validation a commit would require (a rented build, a flash, and the release checklist's camera rows).
- Recording kernel base facts and checkout roles in Project-Ontology.

## 5. Out of Scope

- Performing the merge, resolving any conflict, or pushing a merged branch anywhere.
- Building a kernel, renting a server for kernel work, or flashing a kernel.
- Checking out any kernel tree on the Windows host. The method needs no working tree.
- Changes to `setmode.sh`'s restart ordering, or to any camera module, patch table or device tree.
- The camera blob comparison. `Faz8.1`.
- Deleting or refreshing the local `vauxite` checkouts. They remain reading references.
- Upstreaming anything.

## 6. Current Repository Evidence

**Local checkouts, measured this run.** `android_kernel_xiaomi_sm8550/` is on `vauxite` from `https://github.com/AOSPA/android_kernel_xiaomi_sm8550`, HEAD `3bc107ddbfea` "Merge tag 'android13-5.15-2025-03_r9' into HEAD", `Makefile` 5.15.178. `android_kernel_qcom_sm8550/` is on `vauxite` from `AOSPA/android_kernel_qcom_sm8550`, HEAD `b00609b259a5`, `Makefile` 5.15.178. `common_sm8550/` is on `vauxite` from `AOSPA/android_device_xiaomi_sm8550-common`, HEAD `93546c5`, and contains `BoardConfigCommon.mk`, `extract-files.py` and `proprietary-files.txt`, so it is a device tree. All three are ignored by `.gitignore` (lines 26-27 and the platform section), which is correct for reference checkouts.

**Clone logs, measured this run.** `kernel_clone.log` is 86 bytes containing a single `fatal: destination path 'kernel_ishtar' already exists` line; `common_clone.log` is 32 bytes. Neither identifies a base, which is why this rewrite drops the previous version's log-reading item.

**Android 16 kernel inputs.** The manifest `README.md` (open item 3) records `xiaomi-8550/android_kernel_qcom_sm8550` at `b11e560` and `xiaomi-8550/android_kernel_xiaomi_sm8550` at `1c509b3` on `beryl`, with build paths and companion repositories undetermined. `IMPL-89` recorded that `xiaomi-8550/android_device_xiaomi_ishtar-kernel` has only `uvite` and `vauxite`. `refs/a16_sm8550/common.mk:122-135` sets `TARGET_KERNEL_DLKM_DISABLE := false` and thirteen `TARGET_KERNEL_DLKM_*_OVERRIDE := true` flags, including `CAMERA`, `DISPLAY`, `VIDEO` and `MM_DRV`. That the `beryl` base is also 5.15 is **not measured**; the previous version's 5.15.178 figure belongs to the `vauxite` checkouts only.

**The invariant at risk.** Project-Ontology invariant 3 and Project-Comprehension `EV-12` record the CSIPHY/CSID leak on provider-first restart. `IMPL-13`'s ~17 mode transitions and 2 reboots left mount counts at 1 with no leak symptom. The same entry records that `CSIPHYHw:4 AvailableResource=0` is **not diagnostic**, because it also reads 0 on a clean boot. Any future regression check must therefore use the black-preview symptom and the restart sequence, not that counter. `TRACE-04` maps the workaround to `setmode.sh` `restart_camera()` and `wait_svc()`.

**Validation surface a commit would inherit.** `scripts/smoke.sh`, `docs/regression-v2.1.md` and `docs/release-checklist.md` (PC-01 through PC-18) exist and are verified on Android 15. `Faz8.3` exercises them on Android 16.

## 7. Planned Work Breakdown

- F8.2-01 — Take the consumed kernel from `Faz7.1`
  - Description: Read `Faz7.1`'s F7.1-05 output for the consumed kernel tree, its commit, and the module and devicetree repositories. If `Faz7.1` deferred the item, stop and record the dependency rather than guessing.
  - Output: A named merge target with repository, branch and commit.
- F8.2-02 — Identify its base
  - Description: Read `Makefile` version fields and the most recent merged Android common kernel tag on that commit, through a read-only GitHub read or a blobless bare clone.
  - Output: A base identification with its source commands.
- F8.2-03 — Name the LTS target and the distance
  - Description: Identify the current Android common kernel LTS tag for that kernel generation and count what separates base and target.
  - Output: A target tag and a concrete distance.
- F8.2-04 — Test the camera-module hypothesis
  - Description: Determine whether the CSIPHY/CSID driver is in the core tree or in a separate camera kernel module repository, from the build's module list and repository layout. If it is separate, list the kernel interfaces it builds against that the merge range changes.
  - Output: A verdict on the hypothesis with evidence, and an interface list if confirmed.
- F8.2-05 — Prove the no-checkout merge method
  - Description: In a blobless bare clone on the host, run `git merge-tree --write-tree` for a small known merge — for example a single already-merged tag step on the same tree — and confirm it reports the known result.
  - Output: A method verdict. If it fails, the estimate falls back to a counted diff-stat by subsystem, and the limitation is stated.
- F8.2-06 — Estimate the conflict surface
  - Description: Run the proven method from base to target. Split conflicted and changed paths into camera and sensor paths and everything else, and state the camera-module interface changes from F8.2-04 separately.
  - Output: A two-part conflict assessment plus an interface-change list.
- F8.2-07 — Assess independence
  - Description: State whether anything in Phases 7, 8 or 9 requires the merge, or whether it is independent value, noting Main-Planing's consolidation-first conclusion.
  - Output: A dependency and value assessment.
- F8.2-08 — Recommend and route `DEC-08`
  - Description: Recommend commit or defer with reasoning, and state the validation a commit would need: a rented build, a flash with `Faz7.3`'s return path, and the release checklist camera rows, including a black-preview restart test for invariant 3.
  - Output: `DEC-08` updated with the measured basis.
- F8.2-09 — Record kernel facts
  - Description: Add the consumed tree, its base, the three local checkouts' measured roles, and the camera-module verdict to Project-Ontology.
  - Output: An ontology entry.

## 8. Acceptance Criteria

- The merge target is the kernel `Faz7.1` names as consumed by the `beryl` build, not a local `vauxite` checkout; if `Faz7.1` has not named it, the sub-phase is recorded as blocked on that item.
- The base is identified from `Makefile` and a merged tag on the target commit, with source commands recorded.
- The LTS target tag is named and the distance is a count, not a version-number gap.
- The camera-module hypothesis has a verdict with evidence, and is not used as a premise before that verdict exists.
- The no-checkout method was proven on a known merge before being used, or its failure and the fallback's limitation are stated.
- The conflict assessment separates camera and sensor paths from everything else, and lists camera-module interface changes separately when the module is out of tree.
- The independence assessment states what, if anything, the merge unblocks.
- `DEC-08` carries the recommendation and the validation a commit would require, including an invariant 3 restart test that does not rely on `CSIPHYHw AvailableResource`.
- Project-Ontology records the consumed tree, its base, and the three checkouts' measured roles, with `common_sm8550` recorded as a device tree.
- No merge was performed, no kernel was built, no server was rented, and no kernel tree was checked out on the host.

## 9. Validation and Test Approach

Validation is static and host-side. The estimate rests on git object operations and repository reads, not on builds.

- `VAL-TARGET` (proposed) — the consumed tree read from `Faz7.1`'s output, with repository, branch and commit.
- `VAL-BASE` (proposed) — `Makefile` version fields and `git log --merges --grep` for the last Android common tag on the target commit.
- `VAL-METHOD` (proposed) — `git merge-tree --write-tree <base> <known-merged-tag>` in a blobless bare clone, reproducing a known result.
- `VAL-SURFACE` (proposed) — the base-to-target run, with conflicted and changed paths bucketed by the camera and sensor path list in section 4.
- `VAL-INVARIANT` (proposed) — the camera-module verdict, plus the interface-change list when out of tree.
- `VAL-DOCS` (proposed) — read back the role assignment, the independence assessment, `DEC-08` and the ontology entry.

Local versus live: entirely local, with network reads. Security validation is not applicable beyond not pushing anything. Ontology validation applies to invariant 3's kernel-side dependency, and to correcting `common_sm8550`'s recorded role.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| android_kernel_xiaomi_sm8550 | existing | Read-only `vauxite` reference: base facts for the Android 15 kernel, for contrast with the consumed `beryl` tree. | VAL-BASE |
| android_kernel_qcom_sm8550 | existing | Read-only `vauxite` reference, same purpose. | VAL-BASE |
| refs/a16_sm8550/common.mk | existing | Read-only evidence for the DLKM camera override behind the camera-module hypothesis. | VAL-INVARIANT |
| ishtar-cam-modes/setmode.sh | existing | Read-only: `restart_camera()` and `wait_svc()`, the userspace workaround whose kernel dependency is assessed. | VAL-INVARIANT |
| Planner-docs/Project-Ontology.md | modified | Consumed kernel, base, checkout roles, and the camera-module verdict. | VAL-DOCS |
| Planner-docs/Planing-Ledger.md | modified | `DEC-08` basis and the implementation row. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on `Faz7.1` F7.1-05 for the consumed kernel tree. Does not depend on `Faz7.2`, `Faz7.3` or `Faz8.1`. The estimate needs no build and no device, so it may run in parallel with them.

Blocks nothing in the current roadmap directly. A commit decision under `DEC-08` would create new build, flash and checklist work, which is a ledger section 7 replanning input and is not decomposed here.

Required decisions: `DEC-08`, the user's.

Required credentials: the host `gh` session for reads. All kernel repositories named are public.

Required infrastructure: network access and host disk for blobless bare clones. No server.

Required human approvals: `DEC-08`.

Fresh session token and context risk: medium. Kernel histories are large, and merge-tree output can list many paths. Mitigation: bucket counts and camera-path lists only, never full path dumps; script the bucketing. `R10`'s advice to prefer scripted extraction over interactive exploration applies. Subagents: not recommended; the work is one sequential measurement.

## 11. Risks and Mitigations

- Risk: the local `vauxite` checkouts are scoped instead of the `beryl` kernel. Impact: an assessment of a kernel the Android 16 build does not use. Mitigation: F8.2-01 takes the target from `Faz7.1`, and an acceptance criterion forbids a `vauxite` target.
- Risk (invariant 3): the merge changes behaviour the restart workaround depends on. Impact: black preview in every mode, a severe symptom. Mitigation: F8.2-04 locates the driver, F8.2-06 separates camera paths, and F8.2-08 requires a restart test in any commit's validation.
- Risk: the camera-module hypothesis is adopted without checking. Impact: camera risk understated because "the driver is out of tree". Mitigation: the hypothesis is tested first and is not a premise before its verdict.
- Risk: `git merge-tree` behaves differently than expected on this host or on a blobless clone. Impact: a wrong conflict count. Mitigation: F8.2-05 proves it on a known merge first; on failure, a stated fallback with its limitation.
- Risk: the assessment needs a rented server after all. Impact: unbudgeted cost for a scoping task. Mitigation: the method is chosen to avoid checkout and build; renting is out of scope, so any such need is recorded as a limitation rather than acted on.
- Risk: base facts are taken from the empty clone logs or from checkout names. Impact: a fabricated base. Mitigation: the log item is removed, and `VAL-BASE` reads the target commit directly.
- Risk: the merge is committed because it is on the roadmap. Impact: substantial work that unblocks nothing, at a point where Main-Planing says to consolidate. Mitigation: F8.2-07 and F8.2-08.
- Risk: a regression check relies on `CSIPHYHw:4 AvailableResource=0`. Impact: a false leak diagnosis, since the counter reads 0 on a clean boot. Mitigation: F8.2-08 names the black-preview restart test instead.

## 12. Desired End State

A scoped assessment exists for merging a current GKI LTS release into the kernel the Android 16 `ishtar` build actually consumes: its base and the LTS target with a concrete distance; a conflict surface estimated without a checkout or a server, split into camera and sensor paths and everything else; a measured verdict on where the CSIPHY/CSID driver lives, with the interface changes that matter if it is out of tree; the three local checkouts' roles corrected; the merge's independence stated; and `DEC-08` routed with the validation a commit would demand.

Evidence the implementer produces: the target identification, base and distance, the method proof, the two-part conflict assessment, the camera-module verdict, and the role assignment.

The ledger summary Step 4 appends: the consumed kernel and its base, the LTS target and distance, the method verdict, conflict bucket counts, the camera-module verdict, the independence conclusion, and the `DEC-08` update.

## 13. Next Sub-Phase Transition Criteria

- The merge target is the consumed `beryl` kernel, or the sub-phase is recorded as blocked on `Faz7.1`.
- Base, target and distance are measured.
- The conflict assessment carries the camera and sensor separation, and the camera-module verdict exists.
- `DEC-08` is routed with the required validation stated.
- No merge, build, checkout or rental occurred, and the commit decision remains the user's.
