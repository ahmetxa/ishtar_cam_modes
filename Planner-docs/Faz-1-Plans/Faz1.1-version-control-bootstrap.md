# Faz 1.1 — Version Control Bootstrap

## 1. Context

Main-Planing Phase 1 ("Workspace safety net") exists because the workspace is not a repository. `git rev-parse --is-inside-work-tree` fails at the root, and the same absence was re-confirmed while writing this sub-plan: `git status --short` and `git branch --show-current` both returned `fatal: not a git repository`.

This is the project's single highest-severity finding. Autopsy records it as `AUTOPSY-P0-01`; Project-Comprehension records it as `EV-01` (confidence `confirmed`) and as `CQ-02`, answered negatively. Every other phase in the roadmap modifies either a binary, a patch table, or a device-facing script, and none of those modifications is recoverable today.

The asset most at risk is not the bulk of the tree — it is the smallest part of it. `ishtar-cam-modes/blobs/hal-fullres.patch` is 27 lines and `agc-50mp-yama/hal-raw50-deneme.patch` is 28 lines. Between them they encode twenty patch sites derived from disassembling a 27 MB stripped binary, and both files are plain text with no copy anywhere else.

This sub-phase is the first slice of the entire roadmap. It has no dependency on any other sub-plan.

## 2. Goal

Put the workspace under version control such that every script, patch table, smali source, manifest, and planning document has history and a rollback path, while the multi-hundred-megabyte binary and checkout content stays out of the object store.

## 3. Description

The problem is loss without recovery. There is no diff, no blame, and no restore for a file that gets overwritten during a reverse-engineering session — and Phase 3 is a reverse-engineering session that will edit binaries in place.

It belongs first because it changes the cost of every subsequent mistake from "repeat weeks of disassembly" to "revert one commit". It prepares later phases by giving Phase 4's patch consolidation and Phase 9's reproducible-release goal a baseline to diff against.

The vibecoding slice strategy is deliberately narrow. The first useful slice is: measure what is actually large, write the ignore rules from that measurement, initialize the repository, and commit only the three deliverable directories plus the journal and `Planner-docs/`. The fastest validation signal is `git count-objects -vH` reporting a tracked size well under 50 MB alongside `git status` reporting a clean tree.

What should not be over-planned yet: branch strategy, commit-message conventions, hooks, and CI wiring. None of those matter until there is a second commit, and Phase 9 is where release automation is designed.

One decision cannot be made by planning and is listed in Main-Planing section 9 as needing human confirmation: whether this repository stays local-only or gains a remote. A remote changes what may be committed, because the AGC port redistribution question in Autopsy section 9 becomes live the moment history leaves the machine. This sub-plan proceeds local-only and treats a remote as a separate, later decision.

## 4. Scope

- A real measurement of directory sizes, so the ignore rules are evidence-based rather than estimated.
- A root ignore file covering: the three kernel checkouts, `refs/`, `common_sm8550/`, `platform-tools/`, the two upstream reference module trees, all root-level `.apk` files, all root-level `.zip` release snapshots, `*.log`, and the loose sensor `.bin` at the root.
- Repository initialization on the default branch, with an initial commit.
- Tracked content limited to: `ishtar-cam-modes/` (excluding its binary blobs and the keystore, which Faz 1.2 handles), `ishtar-aon-fix/`, `agc-50mp-yama/`, `50MP-Entegrasyon-Plani.md`, `Planner-docs/`, and `device_ishtar/`.
- A written note recording which large paths are intentionally untracked and why, so a future reader does not mistake exclusion for absence.
- An explicit decision record for local-only versus remote, left open with the user named as the decider.

## 5. Out of Scope

- Adding a remote, pushing, or publishing anything.
- Git LFS or any large-file storage strategy — the correct answer here is exclusion, not storage.
- Commit-message conventions, hooks, signing, or branch protection.
- Any change to module behavior or to a patch table's contents.
- The keystore audit itself, which needs zip inspection and is Faz 1.2.
- Rewriting or reorganizing `50MP-Entegrasyon-Plani.md`.

## 6. Current Repository Evidence

Confirmed in this Step 2 run: `git status --short` and `git branch --show-current` both fail with `fatal: not a git repository (or any of the parent directories): .git` at the workspace root.

The root listing shows 26 entries, of which the following are large or non-source: `AGC8.4.300_V14_snap.apk`, `AGC8.4.300_V9.6_50MP_patched.apk`, `AGC8.4.300_V9.6_snap.apk`, `OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk`, `com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, four `ishtar-cam-modes-v*.zip` snapshots, `ishtar-aon-fix-v1.1.zip`, `android_kernel_qcom_sm8550/`, `android_kernel_xiaomi_sm8550/`, `common_sm8550/`, `refs/`, `platform-tools/`, `13U-989-DCG16+LN2+LN4/`, `Module_Highres_13U_Switcher_A14/`, `common_clone.log`, and `kernel_clone.log`.

`ishtar-cam-modes/` contains nine `blobs/*.bin` sensor variants plus `active/com.qti.sensormodule.ishtar_semco_imx989_wide.bin` and `tile-app.apk` — all binary, all regenerable from `tools/`, and all candidates for exclusion.

Autopsy section 11 states the "roughly 465 MB" figure in Main-Planing is derived from root `ls -la` byte sums and that the whole-tree size command timed out; Project-Comprehension marks the same claim `EV-18`, confidence `tentative`. The measurement in this sub-phase is what converts that tentative number into a fact.

## 7. Planned Work Breakdown

- F1.1-01 — Measure directory sizes with a bounded command
  - Description: Run a per-directory size measurement that completes, rather than a whole-tree scan that has already timed out once. Measure the three kernel checkouts, `refs/`, `common_sm8550/`, `platform-tools/`, the two reference module trees, and the root file set separately.
  - Output: A size table recorded in the commit message or a short note, replacing the tentative `EV-18` estimate.
- F1.1-02 — Draft the root ignore rules from the measurement
  - Description: Write ignore rules for every path the measurement shows to be large and regenerable or externally sourced. Prefer explicit directory rules over broad wildcards so a future addition is not silently ignored.
  - Output: `.gitignore` at the workspace root.
- F1.1-03 — Dry-run the ignore rules before initializing
  - Description: Confirm the rules select the intended set by listing what would be tracked, before any object is written.
  - Output: A reviewed file list; corrections folded back into the ignore rules.
- F1.1-04 — Initialize the repository and make the first commit
  - Description: Initialize, stage the intended set, commit. The commit message records the measurement from F1.1-01 and the local-only decision status.
  - Output: A repository with one commit and a clean working tree.
- F1.1-05 — Record untracked-by-design paths
  - Description: A short section in the root README (written in Faz 1.6) or a standalone note listing each excluded path and the reason, so exclusion is never read as loss.
  - Output: A written exclusion rationale.
- F1.1-06 — Open the remote-versus-local decision explicitly
  - Description: Record the question, its dependency on the AGC redistribution posture in Autopsy section 9, and the fact that it is the user's call. Do not resolve it here.
  - Output: An entry in the Planing-Ledger open-decisions section.

## 8. Acceptance Criteria

- `git rev-parse --is-inside-work-tree` returns `true` at the workspace root.
- `git status --short` produces no output — the working tree is clean.
- `git count-objects -vH` reports a `size-pack` value under 50 MB.
- `git ls-files` contains every `.sh`, `.py`, `.smali`, `.patch`, `.prop`, `.html`, `.xml`, and `.md` file from the three deliverable directories and from `Planner-docs/`.
- `git ls-files` contains no path ending in `.apk`, `.zip`, or `.keystore`, and no path under `android_kernel_*`, `refs/`, `platform-tools/`, or the two reference module trees.
- The measured size table exists in written form and supersedes the tentative 465 MB estimate.
- The local-versus-remote question is recorded as open with the user named, not silently resolved.

## 9. Validation and Test Approach

Validation here is document- and repository-level only. No device interaction occurs in this sub-phase, so there is no live readiness dimension.

- `VAL-VCS` (proposed) — `git rev-parse --is-inside-work-tree`, `git status --short`, `git count-objects -vH`, and a tracked-file count. This is the primary gate.
- `VAL-DOCS` (proposed) — read back the ignore file and the exclusion note; confirm every large path measured in F1.1-01 appears in one or the other.
- `VAL-SEC` (proposed) — `git ls-files` filtered by name only for `.keystore`, `.apk`, and `.zip`. Name-only output; no file contents are printed. The full keystore audit belongs to Faz 1.2.

Local smoke, CI, and artifact validation are not applicable at this stage; CI is deferred to Phase 9 and there is no build to run.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| .gitignore | proposed | Root ignore rules sized from the F1.1-01 measurement. | VAL-VCS, VAL-DOCS |
| ishtar-cam-modes/setmode.sh | existing | Read-only context: a tracked deliverable that must survive in the tracked-file list. | VAL-VCS |
| ishtar-cam-modes/blobs/hal-fullres.patch | existing | The highest-value irreplaceable artifact; tracking it is the point of this slice. | VAL-VCS |
| agc-50mp-yama/hal-raw50-deneme.patch | existing | Second irreplaceable patch table; must be tracked before Phase 3 edits anything. | VAL-VCS |
| 50MP-Entegrasyon-Plani.md | existing | The engineering journal; tracked so its history becomes diffable. | VAL-VCS |

## 10. Dependencies and Sequencing

This sub-phase has no upstream dependency. It is the first executable slice in the roadmap and every other sub-plan that writes a binary or a patch table depends on it.

Required decisions: none blocking. The local-versus-remote question is recorded but does not gate initialization, because a local repository can gain a remote later while an uninitialized workspace cannot gain history retroactively.

Required credentials, infrastructure, or live endpoints: none. No network access is needed for local initialization.

Required human approvals: none for local initialization. Adding a remote later requires the user's explicit decision.

Fresh Claude Code session token and context risk: low. The work touches a handful of small files and produces short command output. Subagents are not recommended; the task is narrow and the parent already holds the necessary evidence.

## 11. Risks and Mitigations

- Risk: an over-broad ignore rule silently excludes a source file that looks binary-adjacent, such as `ishtar-cam-modes/tile-app/AndroidManifest.xml`. Impact: a deliverable file is absent from history and nobody notices until it is lost. Mitigation: F1.1-03's dry run reviews the tracked list explicitly, and the acceptance criteria enumerate the extensions that must be present.
- Risk: the first commit sweeps in `debug.keystore` before Faz 1.2 runs. Impact: a signing credential enters history permanently, and removing it later requires history rewriting. Mitigation: the keystore exclusion rule goes into the ignore file in this sub-phase even though its audit is Faz 1.2; `VAL-SEC` checks for it by name before the commit is considered accepted. This is the single ordering constraint inside Phase 1.
- Risk (`AUTOPSY-P1-01`): a released zip already contains the keystore, so exclusion going forward is not sufficient. Impact: the credential is already distributed. Mitigation: out of scope here by design — Faz 1.2 audits the four release zips.
- Risk: initializing on a directory with hundreds of thousands of kernel-checkout files makes the first status call slow enough to look hung. Impact: the operator interrupts mid-operation. Mitigation: the ignore rules are written and dry-run before initialization, not after.
- Risk (`R8` in Main-Planing): tracking the patch tables gives a false sense that the offsets are portable. Impact: a future reader assumes the patch survives a ROM update. Mitigation: the exclusion note states that offsets are bound to one vendor build and that the md5 guard is the detector.

## 12. Desired End State

The workspace is a repository with one commit, a clean status, and a pack size under 50 MB. Every hand-written artifact in the three deliverable directories has history. Every large, regenerable, or externally sourced path is excluded by an explicit rule, and a written note says which and why.

The evidence an implementer should produce is the output of the four `VAL-VCS` commands plus the measured size table.

The Planing-Ledger summary Step 4 should append records: the repository was initialized, the measured sizes that replaced the `EV-18` estimate, the tracked-file count, and the fact that the remote decision remains open.

## 13. Next Sub-Phase Transition Criteria

- The repository exists, the tree is clean, and the pack size is verified under 50 MB.
- The ignore file contains a rule matching `debug.keystore` before any commit is made.
- The tracked-file list has been read once by a human or by an explicit check, not assumed from the ignore rules.
- The measured size table is written down and the tentative estimate is retired.
- No sub-plan that modifies a binary or a patch table has started.
