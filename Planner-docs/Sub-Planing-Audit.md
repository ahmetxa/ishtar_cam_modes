# Sub-Planing Audit

> Step 3 audit — ClaudeQB. Body language: English (default contract).
> The project's user-facing documents and module interface remain Turkish and English; that convention is unchanged.
>
> **This is the eleventh audit (2026-09-14).** It supersedes the tenth audit (2026-09-13) and is step 3c of `docs/pre-rental-plan.md`. Since the tenth audit:
>
> - `IMPL-94` ran `F7.2-01`'s gate once (not passed) and repaired the runbook for `AUDIT-FIX-52`, `-53` and `-54`, including the section 10 symlink path.
> - `DEC-26` moved the rental from Hetzner to Scaleway. `IMPL-95` re-targeted `docs/build-environment.md` to Scaleway POP2-32C-128G.
> - Planning run 20 (bounded Step 2 amendment) re-targeted `Faz7.2` to the runbook's values. It edited only `Faz7.2` and the ledger.
>
> **This audit exists because the tenth audit graded Hetzner text that a rental can no longer follow.** Ledger section 7's `DEC-26` input and section 4's `Faz7.2` row say `Faz7.2` does not enter a paid session before this audit.
>
> **Active snapshots: `SNAP-2026-09-10-MAIN` and `SNAP-2026-09-10-SUBPLANS`. The sub-plan set is 42.** Run 20 cut no snapshot, by the precedent of runs 13 to 15 and 19. That is correct: one sub-plan was amended, no phase was re-decomposed, and no work item changed.

## 1. Audit Summary

**Overall audit status: PASS_WITH_WARNINGS.**

**Run 20's amendment of `Faz7.2` matches the re-targeted runbook on every value checked.** Section 8 has the value-by-value table. Covered:

- the instance type;
- the three Block volumes and their mounts;
- the flexible IPv4;
- Ubuntu 22.04 and its 24.04 fallback;
- the 10-hour ceiling, the hour-8 rule and started-hour counting;
- no retry after an out-of-memory kill;
- section 5's four manual checks;
- section 12's eight teardown steps and four zero counts;
- `/android/beryl` and `~/out-pkg`.

No live Hetzner fact is left in `Faz7.2`. Its four Hetzner mentions are all amendment history (lines 7, 9, 11 and 18). The work-item count is 10 before and after run 20, and the heading set is identical.

**Closed this run, because the runbook carries each repair (measured):**

- `AUDIT-FIX-52`: runbook section 4, lines 135–138, now gives a sync failure matching a sync-path detector its fix, counted against the same 2 attempts. That agrees with `F7.2-04`, so the precedence clash is gone.
- `AUDIT-FIX-53`: runbook section 5, lines 186–190, reads `AOSPA/manifest` `beryl` and stops before renting if it moved. Measured today: still `7dfc0650…`, dated 2026-05-24.
- `AUDIT-FIX-54`: in section 10, a failed `repo manifest -r` is recorded and the block continues (lines 473–480). Section 11's copy loop logs each missing file to `retrieval.txt` and continues (lines 556–571). The operator rule for both sections is at lines 523–526.

**Three new P3 findings. None needs a new decision, and none contradicts the runbook.**

- **`AUDIT-FIX-55`: stale symlink-correction wording.** `IMPL-94` already moved runbook section 10's test to `$OUT/vendor/lib64/camera/aon_front.pb` (lines 485–488). `Faz7.2` still tells `F7.2-01` to make that correction before renting, in section 4 line 79, `F7.2-01` lines 222–223, `VAL-GATE`, `VAL-DOCS`, the contract table, the section 11 risk and section 12.
  - Section 6 line 196 is worse than stale: it says in present tense that the runbook tests the `odm` path, which is now false.
  - It fails safe. The runbook wins on disagreement, and "correct odm to vendor" has nothing left to change. On the rental day the correction becomes a verification.
- **`AUDIT-FIX-56`: the plan half of `-52`, carried.** `Faz7.2` section 8 line 292 and `VAL-SYNC` line 307 still grade `manifest-resolved.xml` against the 13 pins "at `22283d8`", not "at `22283d8` as amended by `fixes.diff`". The ledger's `DEC-25` item (3) still lacks the sync-path exception, a disagreement `IMPL-94` recorded.
- **`AUDIT-FIX-57`: the carried Hetzner wording is routed correctly, but the list is incomplete.** Run 20, ledger section 7 and pre-rental step 3b route `Main-Planing.md` lines 75, 211 and 265 and `Project-Comprehension.md` `EV-20` to the next Step 1 amendment with `AUDIT-FIX-41` and `-42`. This audit confirmed those four lines. It also found three more live statements of Hetzner as the build host:
  - `Project-Comprehension.md` `CQ-13` (line 25);
  - `Project-Ontology.md` invariant 11 (line 429, "Hetzner Cloud server — Ubuntu 22.04 LTS on a CCX53");
  - `docs/reverse-engineering-toolchain.md` line 220.

  `Faz7.1` line 5 and index line 10 are history and need nothing.

**Most important finding: `AUDIT-FIX-55` (P3).** It is the only point where the plan misstates the current runbook, and a rental-day session reads it first. No P0 or P1 is open. The only open P2 is the carried `AUDIT-FIX-22`.

**Most important remediation action:** on the rental day, treat `F7.2-01`'s symlink step as a **verification**, not an edit. Confirm that runbook lines 485–488 name `vendor/lib64/camera/aon_front.pb` and report the `readlink` target. Run `bash -n` on the section 10 block. Cite `IMPL-94` as the edit. Grade `VAL-SYNC` against `22283d8` as amended by `fixes.diff` (`-56`). Reword both in a later bounded amendment, not before the rental.

**Step 2 output is usable for Step 4.** **Queue head: `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md`, starting at `F7.2-01`.** Behind it: `Faz7.3`, `Faz8.1`'s agreement half, then `Faz8.3`.

## 2. Reviewed Sources

**Files inspected.**

- `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md`, read in full. Its structure was also compared with `HEAD` (`587e3b5`): the work-item count and the heading list are unchanged.
- `docs/build-environment.md`, read in full. It is the re-targeted runbook. It is unchanged since `587e3b5`.
- `docs/pre-rental-plan.md`, read in full.
- `Planner-docs/Planing-Ledger.md` (CRLF), through a line extractor:
  - section 2 row 20;
  - section 4's `Faz7.2` row, plus status counts over all 42 matrix rows;
  - section 5 rows `IMPL-94` and `IMPL-95`;
  - section 7's `DEC-26` replanning input;
  - section 8 rows `DEC-22`, `DEC-25` and `DEC-26`;
  - pipe counts on the edited rows, and the headings of the section 2 and section 4 tables.
- The tenth `Planner-docs/Sub-Planing-Audit.md`, read in full before overwriting, so finding IDs continue from `AUDIT-FIX-54`.
- `Planner-docs/Main-Planing.md` lines 75, 211 and 265. `Planner-docs/Project-Comprehension.md` lines 25 (`CQ-13`) and 51 (`EV-20`). `Planner-docs/Project-Ontology.md` line 429. `Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md` line 5. `Planner-docs/Sub-Planing-Index.md` line 10. `docs/reverse-engineering-toolchain.md` lines 214–224.
- `snapshots/`: listed only. `20260913-2140__IMPL94__faz72-rental-gate.txt` and `20260914-1434__DEC26__scaleway-handover.txt` both exist.

**Folders inspected.** `Planner-docs/`, all nine `Faz-<n>-Plans/` folders, `docs/`, and `snapshots/` (listing only).

**Important commands run.**

- `git status --short`, `git diff --stat`, and `git diff --stat HEAD` on `Main-Planing.md`, `Sub-Planing-Index.md`, `Project-Ontology.md`, `Project-Comprehension.md` and `docs/build-environment.md`. All five are unchanged. The working tree holds run 20's three uncommitted files (`Faz7.2`, the ledger, `docs/pre-rental-plan.md`) and the untracked `devir-teslim-promptu.md`.
- The bundled validator at the installed plugin path, run with `python` 3.14.7 (`python3` resolves to the Windows Store stub):
  - before writing: `--mode step3-preflight --strict`, which passed with `error_count=0`, `warning_count=0`, `secret_findings=0`, `subplan_count=42`, `index_reference_count=42`, `phase_folder_count=9` and `main_phase_count=9`;
  - after writing: `--mode step3 --strict` and `--mode step4 --strict` (section 15).
- A heading check over all 42 sub-plans: 13 required headings each.
- **`bash -n` on all ten fenced `bash` blocks of the runbook**, extracted to this session's scratchpad and deleted afterwards. All ten pass, and every block's first line is `set -euo pipefail`.
- Read-only `gh api` calls with the WinGet `gh.exe`:
  - `AOSPA/manifest` `beryl`: `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2`, 2026-05-24;
  - `ahmetxa/android_local_manifests` `main`: `22283d8a866d042e02336fcb4698253ac6bf9c3b`;
  - both `ahmetxa` repositories: `private=false`.
- `grep` for Hetzner, CCX53 and Primary IP across `Planner-docs/` and `docs/`, and for pre-Scaleway paths (`cd ~/beryl`) in the queued sub-plans. None in the queued sub-plans.

**Things not verified.**

- **Runbook section 5 was not executed this run.** The tenth audit and `IMPL-94` each ran it with exit 0. This audit re-read its three GitHub inputs instead (above). On the rental day the section is re-run as written.
- **Scaleway facts.** Quotas, identity validation, whether Ubuntu 22.04 is offered for the type, prices at creation, and how the guest exposes a volume ID. All are rental-day checks. Runbook section 3's quotes and links were read as written, not re-fetched.
- **The section 7 volume block (`pick`, `check_id`, `fstab`) has never run.** It only passes `bash -n`. `Faz7.2` section 11 states this as a risk.
- **Content of the 41 sub-plans run 20 did not touch.** Structure passed on all 42. Content assessments of the other 41 stand from the tenth audit, and `git status` shows none of them changed.
- **Device state.** No `adb` command was run.

No secret value was read or recorded.

## 3. Main Phase Coverage Analysis

| Main phase no | Main phase heading | Expected folder | Folder exists? | Sub-plan count | Coverage status | Notes |
|---|---|---|---|---|---|---|
| 1 | Workspace safety net | Planner-docs/Faz-1-Plans/ | Yes | 6 | OK | All six `verified`. |
| 2 | Ship and re-baseline v2.1 | Planner-docs/Faz-2-Plans/ | Yes | 4 | OK | All four `verified`. |
| 3 | AGC stable at 12.6 MP under 50 MP | Planner-docs/Faz-3-Plans/ | Yes | 11 | OK | All eleven `verified`; phase marked successful (`DEC-21`). |
| 4 | Minimal correct HAL patch | Planner-docs/Faz-4-Plans/ | Yes | 7 | OK | `Faz4.2`–`4.5` `verified`; `Faz4.1`, `Faz4.7` `superseded`; `Faz4.6` `DEFERRED`. |
| 5 | Mode-0 12-bit composition | Planner-docs/Faz-5-Plans/ | Yes | 3 | OK | All three `verified`. |
| 6 | AON fix upstreaming | Planner-docs/Faz-6-Plans/ | Yes | 2 | OK | `Faz6.2` `verified`; `Faz6.1` `implemented`, effect verification owned by `Faz7.3` `F7.3-08`. |
| 7 | Android 16 build environment | Planner-docs/Faz-7-Plans/ | Yes | 3 | OK | `Faz7.1` `verified` (`IMPL-91`). `Faz7.2` re-targeted to Scaleway by run 20 and queued; `Faz7.3` queued. The phase objective and acceptance signal name "a rented VDS", not a provider, so `DEC-26` changes no phase meaning. |
| 8 | Camera work on Android 16 + kernel LTS | Planner-docs/Faz-8-Plans/ | Yes | 3 | OK | `Faz8.1` `implemented` (static half, `IMPL-92`). `Faz8.2` `verified` (`IMPL-93`). `Faz8.3` queued. Undecomposed branches stay routed to `DEC-07`/`DEC-08`. |
| 9 | Release engineering | Planner-docs/Faz-9-Plans/ | Yes | 3 | OK | All three `verified`. |

The validator reports `main_phase_count=9` and `phase_folder_count=9`. There is no missing phase and no extra folder. Per-phase counts, measured this run: **6, 4, 11, 7, 3, 2, 3, 3, 3 — total 42.**

## 4. Sub-Plan File Inventory

Structure was checked on **all 42** files: every one carries the 13 required headings, and the validator agrees on filename, folder and H1. Content was assessed this run only for `Faz7.2`, the one file run 20 changed.

**Planner-docs/Faz-7-Plans/** (3 files).

- `Faz7.1-github-input-staging.md` — `# Faz 7.1 — GitHub Input Staging and Pre-Rental Readiness`. Phase match OK, structure OK. **`verified`** (`IMPL-91`). Its outputs were re-read on GitHub this run: `22283d8`, and both repositories public. Line 5's Hetzner mention quotes the Phase 7 text of its time. It is history.
- `Faz7.2-first-aospa-build.md` — `# Faz 7.2 — First AOSPA beryl Build on a Rented VDS`. Phase match OK, structure OK. **Content: strong, and executable against the Scaleway runbook.**
  - **Section 1.** The run 20 note lists eight re-targeted facts, each matching the runbook (section 8 below). It states "no work item was added or removed", which holds: 10 before, 10 after. It routes the carried Hetzner wording, and names this audit as the gate.
  - **Sections 2–4, 7, 8, 9, 10, 12 and 13.** Every provider value is re-read from the runbook rather than paraphrased from `DEC-26`. `F7.2-09`'s eight steps map one-to-one onto runbook section 12's eight steps.
  - **Section 11** gains three sound provider risks: account or quota, volume picking and unmounted `out`, and out-of-memory. The volume-block risk states honestly that the block has "never run".
  - **Notes.** `AUDIT-FIX-55`: stale "correct before renting" wording, and section 6's false present-tense claim. `AUDIT-FIX-56`: `VAL-SYNC` and the resolved-manifest criterion lack the `fixes.diff` basis.
- `Faz7.3-flash-boot-and-aon-verification.md` — `# Faz 7.3 — Flash, Boot and AON Verification on the Device`. Phase match OK, structure OK. **Content: strong** (tenth audit). Unchanged since then. It consumes runbook section 11's artifact table, and `IMPL-95` did not change that table's rows. No provider fact appears. **Notes.** `AUDIT-FIX-37`, plus the carried `F7.3-02` wording gap (section 12).

**Planner-docs/Faz-8-Plans/** (3 files).

- `Faz8.1-android16-camera-blob-comparison.md` — `# Faz 8.1 — Android 16 Camera Blob Comparison and Carry-Over Decision`. Phase match OK, structure OK. **Content: strong** (tenth audit). Unchanged. **Notes.** `AUDIT-FIX-22`, since `F8.1-10` writes the ontology. Consider folding `-57`'s invariant 11 there only if a Step 1 amendment has not yet run; see section 13.
- `Faz8.2-kernel-lts-merge-scoping.md` — `# Faz 8.2 — Kernel LTS Merge Scoping`. Phase match OK, structure OK. **`verified`** (`IMPL-93`). Unchanged.
- `Faz8.3-camera-modes-on-android16-build.md` — `# Faz 8.3 — Camera Modes on the Android 16 Build`. Phase match OK, structure OK. **Content: strong** (tenth audit). Unchanged. **Notes.** `AUDIT-FIX-50`.

**All other phase folders** (`Faz-1-Plans` 6, `Faz-2-Plans` 4, `Faz-3-Plans` 11, `Faz-4-Plans` 7, `Faz-5-Plans` 3, `Faz-6-Plans` 2, `Faz-9-Plans` 3) pass on filename, phase match and section structure, and are unchanged since the tenth audit. Carried residues: `Faz1.3` (`AUDIT-FIX-25`, accepted) and `Faz3.8` (`AUDIT-FIX-33`, accepted).

## 5. Naming and Sequencing Check

**No naming or order issues were found.**

- **Folder naming:** all nine match `Faz-<n>-Plans/`.
- **Filename naming:** all 42 match `Faz<phase>.<sub>-<ascii-kebab-slug>.md`, with no spaces, no non-ASCII characters and no duplicates.
- **Numbering:** contiguous in every phase. Run 20 created, deleted and renamed nothing.
- **Agreement:** folder, filename and H1 agree in all 42 (validator).
- **Order:** the phase order matches `Main-Planing.md`. Execution order within Phases 7 and 8 differs from numbering by design, per index amendment 4d, unchanged.

## 6. Index Consistency Check

- **Missing, broken or unindexed references: none.** `index_reference_count=42`.
- **Phase count:** nine in the index, the master plan and the folders.
- **Index not edited by run 20. That is the right call.** Its only provider mention, line 10, is run 18's re-plan banner, which records the `DEC-24` decision of its time. The index states no live instance, disk, IP or teardown value that `Faz7.2` or the runbook must agree with.
- **Execution order: plausible and unchanged.** `Faz7.2` → `Faz7.3` → `Faz8.1` agreement half → `Faz8.3`.
- **Carried residue.** The three-field description of `Faz3.8` (`AUDIT-FIX-33`, accepted).

## 7. Required Section Structure Check

Checked on **all 42** sub-plans, not sampled.

- **Missing, duplicated or out-of-order sections: none.** Every file carries the thirteen required headings. For `Faz7.2`, the full heading list (`#` lines) is byte-identical between `HEAD` and the working tree.
- **Empty or placeholder sections: none.** The validator reports `warning_count=0` in strict preflight.
- **Title, filename and folder: all 42 agree.**
- **Implementation Contract tables: present in all 42.** `Faz7.2`'s table still has repo-relative paths only. Its `docs/build-environment.md` row reads `modified`, justified by "`F7.2-01` corrects section 10's built-symlink path before renting". That purpose is now stale (`AUDIT-FIX-55`). The `modified` state is still correct, because post-session deviations are recorded in the runbook.
- **Encoding:** `Faz7.2` is UTF-8, LF. The ledger stays CRLF (`file`). The rows run 20 edited keep their table's pipe counts: section 2 row 20 has 6, like its header; section 4's `Faz7.2` row has 10, like its header.

## 8. Content Quality and Implementability Analysis

**Value-by-value grading of run 20's amendment against the re-targeted runbook.**

| Value | Runbook (section, line) | `Faz7.2` (section / item, line) | Verdict |
|---|---|---|---|
| Instance type POP2-32C-128G, 32 vCPU, 128 GiB, Block only | s1 l22, s2 l34–35, s6 l214 | s1 l9; s4 l81; `F7.2-02` l226; s10 l351; s12 l385 | match |
| Boot 40 GB 5K; `ishtar-src` 310 GB 5K at `/android`; `ishtar-out` 260 GB 15K at `/android/beryl/out` | s1 l23, s6 l217–219, s7 l262–266 | s1 l10; s4 l82, l89; `F7.2-02` l227, l236; s10 l351 | match |
| Volumes picked by size, cross-checked against the Console ID, `mkfs` only where `blkid` finds none | s7 l268–271, l278–330 | s4 l88; `F7.2-02` l235; s11 l370 | match |
| Flexible IPv4 kept at creation, deleted at teardown | s3 l98–104, s6 l220–221, s12 step 4 | s1 l11; s4 l83, l111; `F7.2-09` step 4; `VAL-TEARDOWN` | match |
| Ubuntu 22.04; 24.04 fallback with persistent `sysctl` | s1 l21, s6 l214–216, s7 l246–251 | s1 l12; s4 l81, l87; `F7.2-02` l231, l234; s11 l369 | match |
| 10 h ceiling over every billed resource; every started hour counts whole; hour-8 retrieve and tear down | s3 l71–73, s4 l126–132, l146–147 | s1 l13; s2 l44; s3 l66; `F7.2-06` l250; `F7.2-09` step 6; s11 l367 | match |
| Out-of-memory kill not retried: stop, retrieve, tear down, replanning input | s4 l144–145, s9 l459–460 | s1 l13; s3 l65; s4 l99; `F7.2-06`; s8 l295; `VAL-COMPILE`; s11 l371 | match |
| Section 5 scripted block (manifest pin, `check.py` both ways, visibility, base pin) | s5 l170–192 | s4 l74; `F7.2-01` l216 | match |
| Section 5 manual checks: identity-validated quota for the type and 610 GB; SSH key in the Project; output directory; window | s5 l196–207 | s1 l15; s4 l75–78; `F7.2-01` steps 1–4; s8 l287; s11 l369 | match (four of four) |
| Section 12 teardown: Instance deleted, never powered off or standby; each Block volume deleted; flexible IP deleted; no snapshot or image; zero counts; last deletion time; rounded-up hours; no credential; `ssh-keygen -R` | s12 steps 1–8 | `F7.2-09` steps 1–8; s4 l108–113; s8 l298; `VAL-TEARDOWN`; s13 l413 | match (eight of eight; four zero counts) |
| `/android/beryl` as the tree; `mountpoint` check before sync and build | s7 l338–339, s8 l390–391, s9 l426–427 | s1 l16; s4 l94–96; `F7.2-04`; `F7.2-06`; s8 l289 | match |
| `~/out-pkg` → `/android/pkg` on the source volume; `retrieval.txt`; `SHA256SUMS` | s7 l341, s11 l553–572 | s1 l16; s4 l90, l107; `F7.2-08` l262 | match |
| `disk.txt` sizes of `.repo`, the tree and `out` | s8 l408–413, s9 l433–437, s13 | s4 l94, l97; `F7.2-04`; `F7.2-06`; `F7.2-10`; s12 l406 | match |
| Section 13 ledger row contents, incl. Ubuntu release and zero counts | s13 | `F7.2-10` l282; s12 l398–407 | match |
| Section 3 quotes used in the plan | s3 l74–75, l93–94, l102 | s3 l70; s6 l157–163; s11 l368 | verbatim |

**Implementability of the queue head.**

- **`F7.2-01` is free and bounded.** The section 5 block, four Console or host checks, a re-read of runbook section 4, and a stop for rental approval. The symlink "correction" is now a read-back plus `bash -n` (`AUDIT-FIX-55`).
- **The paid items `F7.2-02`–`10` map one-to-one onto runbook sections 6–13.** The provider-sensitive parts are fully specified, with no improvisation left: volume choice, the mount guard, deletion of each billed resource, and zero counts.
- **Fastest signal unchanged:** a completed sync at the two pinned commits, both re-read on GitHub today.

**Residual precision gaps.** Both are P3 and fail safe, and neither needs a pre-rental edit.

1. **`AUDIT-FIX-55`.** A session that follows `F7.2-01` literally searches for an `odm` test that no longer exists. The runbook-precedence sentence at section 1 line 27 makes the runbook win. Section 6 line 196's present-tense claim should not be read as evidence.
2. **`AUDIT-FIX-56`.** After a permitted fix — removing `clone-depth`, deleting the `vendor/xiaomi/camera` lines, or deleting the `display-drivers` pin — `manifest-resolved.xml` legitimately differs from `22283d8`'s 13 pins. `VAL-SYNC` must use `22283d8` plus `fixes.diff` as its reference, or it reports a false failure.

**Vibecoding and fresh-session quality.** The slices are ordered cheapest failure first. Token risk is banded medium, rising to high on repeated failure, with the mitigation named. Subagents: not recommended, with a reason (one stateful remote resource). Outcome, validation, boundaries and stop conditions are all stated.

## 9. Scope Drift and Architectural Consistency Analysis

**No scope drift.**

- Run 20 amended one sub-plan within the step 3b mandate: the provider facts in `Faz7.2`, plus the ledger.
- No phase, sub-plan, work item, objective or acceptance signal changed.
- `Main-Planing.md`, the index, the ontology, the comprehension file and the runbook are unchanged against `HEAD`.
- Phase 7's signal names "a rented VDS". A provider change is therefore a sub-plan fact, not a master-plan change, and the no-snapshot decision is consistent with that.

**`DEC-26` is carried faithfully.**

- (a) 22.04 with the fallback; (b) and (d) POP2-32C-128G, with the ceiling and hour-8 rule kept and no out-of-memory retry; (c) delete everything. Each lands in `Faz7.2` sections 1, 3, 4, 5, 7, 8 and 11.
- Section 5 excludes keeping any volume and creating any snapshot or extra volume. That matches runbook sections 3, 6 and 12.

**The worse-case teardown design is sound and carried.** The Block Storage FAQ and the Instance API text disagree on whether `terminate` deletes Block volumes, and the flexible IP survives `terminate`. So `F7.2-09` deletes each resource by name and grades on zero counts, not on the Console dialog.

**Ledger continuity: good, with one recorded disagreement still open.**

- Row 20 matches the diff.
- Section 4's `Faz7.2` next action already says the symlink correction is "already in the runbook since `IMPL-94`". So the ledger is ahead of the sub-plan text (`AUDIT-FIX-55`).
- Section 7's `DEC-26` input records the Step 2 discharge and leaves this audit outstanding.
- `IMPL-94` recorded that `DEC-25` item (3) lacks the sync-path exception the runbook now carries. `DEC-26` did not amend item (3), so the record still disagrees with the runbook (`AUDIT-FIX-56`). The runbook is operative, and the disagreement is documentary.

**Carried Hetzner wording (`AUDIT-FIX-57`).**

- **Confirmed routed to the next Step 1 amendment with `AUDIT-FIX-41` and `-42`**, in three places: `Faz7.2` section 1 line 18, ledger section 7's `DEC-26` input, and `docs/pre-rental-plan.md` step 3b. The routed lines were checked:
  - `Main-Planing.md` line 75 ("a rented Hetzner VDS");
  - line 211 (the same);
  - line 265 (R9 mitigation, "a rented Hetzner VDS");
  - `Project-Comprehension.md` `EV-20` ("rented Hetzner Cloud server (Ubuntu 22.04 LTS, CCX53)").
- **The routing list misses three live statements of the same fact:**
  - `Project-Comprehension.md` `CQ-13`, line 25 ("Ubuntu 22.04 LTS, Hetzner CCX53");
  - `Project-Ontology.md` invariant 11, line 429;
  - `docs/reverse-engineering-toolchain.md` line 220.
- No queued work item reads any of them. Each is a statement of the host, not a procedure. They are routed with the same amendment, not a new decision.

**Ontology consistency.** `beryl` stays a branch throughout. Invariant 10 underlies `F7.2-07`'s post-build md5 read. Invariant 11 is the stale host statement above: its constraint (no Windows build, a rented Linux server deleted after each session) still holds, and only the provider and type are out of date.

## 10. Readiness Realism

**No overclaim in run 20's text.**

- `Faz7.2` says the section 7 volume block "has passed `bash -n` but has never run", and puts its first run on the rented Instance. This audit confirmed `bash -n` on all ten blocks.
- The billing quotes carry their uncertainty: "No page says whether a started hour bills whole, so every started hour counts". So do the two disagreeing deletion statements.
- Prices are not asserted in `Faz7.2`. The runbook defers them to the Console at creation.
- The outcome is still "built, partial or blocked", and md5s are "facts, not conclusions".

**Local versus live is drawn correctly.**

- **Local and free:** runbook section 5 and the four manual checks.
- **Live and paid:** sections 6–12.
- The Console checks are the user's. Neither this audit nor any plan text claims them.

**Stale-readiness note (`AUDIT-FIX-55`).** `F7.2-01`'s output still lists "the section 10 correction with its `bash -n` result" as something the gate produces. That result already exists in `IMPL-94`'s gate record. On the rental day it is a read-back, not new work, and must not be reported as a fresh edit.

## 11. Security and Governance Findings

- **Secret safety: clean.**
  - `secret_findings=0` in every validator mode run.
  - No token, password, private key, server address or volume ID appears in any planner file.
  - `Faz7.2` keeps the address in the shell and the volume IDs on paper or in the shell. Start records carry no address, key or volume ID.
  - `DEC-25` keeps the server credential-free. Runbook section 10's credential-URL check and token scan run before copying.
- **Least privilege.** The server holds no GitHub credential. The only sensitive items are the user's Scaleway session and SSH private key, which stay on the host. The public key is Project-scoped, and `F7.2-01` checks that.
- **Destructive operations on the rented disks.** `mkfs` is gated on `blkid` finding no filesystem, volumes are chosen by size with an ID cross-check, and the block stops on an ambiguous match. These are the right controls for a block that has never run.
- **Cost controls.** Deletion of each billed resource, zero counts, and hour 8. Powering off is explicitly not teardown. A leftover volume or flexible IP is a named risk with a zero-count detector. The 610 GB quota and the identity check are free and happen before renting.
- **Command execution safety.** Every block starts with `set -euo pipefail` (all ten measured). Sections 10 and 11 record and continue, with an operator rule, which closes `AUDIT-FIX-54`. The barista exit-status grep and the base-pin checks on both sides are unchanged.
- **Artifact integrity and blob redistribution.** sha256 is checked at both ends, and teardown is gated on it. Outputs stay under `~/Documents/Projeler/ishtar-builds/`, outside every repository (`ARC-04`).
- **Approval gates.** The rental approval after `F7.2-01`, Console deletion, and any post-session push of `fixes.diff`.
- **Ontology writes into a NUL-bearing file (`AUDIT-FIX-22`).** Still open. Any `-57` edit to invariant 11 must be byte-preserving and diffed.
- **Audit boundary.** No P0 or P1 was found, and this audit repaired nothing.

## 12. Step 4 Readiness Assessment

**Conventions.** Dependency state follows the ten previous audits:

- `independent` means no upstream dependency.
- `satisfied` means every upstream dependency is complete in the repository, or is produced by an earlier row of this queue.

Queued rows appear in execution order.

**What changed since the tenth audit.** `Faz7.2` was amended by run 20 and re-read by this audit. Its findings change from `-52`/`-53`/`-54` (resolved) to `-55`/`-56`. No other row's status changed.

**Counts, measured from the ledger matrix.** 34 `verified`, 3 `implemented`, 3 `planned` and 2 `superseded`, which gives:

| Category | Rows |
|---|---|
| Queued | 4 (0 `READY`, 4 `READY_WITH_WARNINGS`) |
| COMPLETE | 35 |
| SUPERSEDED | 2 |
| DEFERRED | 1 |
| NEEDS_REPAIR | 0 |
| **Total** | **42** |

**Why `Faz7.2` is not `NEEDS_REPAIR`.** The test is whether a Step 4 run can be graded correctly against the file as written, with the runbook precedence sentence it carries.

- `AUDIT-FIX-55` asks for an edit that is already in the runbook. It becomes a verification, and fails safe.
- `AUDIT-FIX-56` is a grading reference the session can apply from this row.
- Neither changes a paid step.

| Sub-Plan Path | Status | Finding IDs | Dependency State | Reason | Required Repair |
|---|---|---|---|---|---|
| Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | READY_WITH_WARNINGS | AUDIT-FIX-55, AUDIT-FIX-56 | satisfied | **Queue head.** `Faz7.1` verified (`IMPL-91`). Re-read on GitHub today: `22283d8`, both repositories public, base `7dfc0650…` unchanged since 2026-05-24. `DEC-22`, `DEC-25` and `DEC-26` answered. Runbook re-targeted by `IMPL-95`, all ten blocks pass `bash -n`. Run 20 re-targeted this file, and every provider value matches the runbook (section 8). `AUDIT-FIX-52`, `-53` and `-54` resolved in the runbook. A Step 4 session stops after `F7.2-01` for the user's rental approval, by design. | No pre-rental edit. **On the rental day:** (1) run runbook section 5 as written; (2) treat `F7.2-01`'s symlink step as a verification, not an edit: read back runbook section 10 lines 485–488 (`$OUT/vendor/lib64/camera/aon_front.pb`, `readlink` kept, expected target `/odm/lib64/camera/aon_front.pb`), run `bash -n` on that block, and cite `IMPL-94` as the edit; ignore section 6 line 196's present-tense claim (`AUDIT-FIX-55`); (3) the four Scaleway manual checks of runbook section 5; (4) re-read runbook section 4, which carries the sync-path exception `DEC-25` item (3) lacks; (5) stop for rental approval. **In the paid session:** grade `VAL-SYNC` and the resolved-manifest criterion against `22283d8` as amended by `fixes.diff`, and record that basis in the ledger row (`AUDIT-FIX-56`). **Later bounded amendment, not before the rental:** reword `-55`'s lines to past tense and `-56`'s two lines to the amended basis. |
| Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | READY_WITH_WARNINGS | AUDIT-FIX-37 | satisfied | The user's flash of the daily device. Depends on `Faz7.2`'s retrieved section 11 artifacts with sha256 and its AON step 1 result, the row above. `Faz8.1`'s static result is available (`IMPL-92`). Unchanged since the tenth audit; runbook section 11's artifact table unchanged by `IMPL-95`. | At `F7.3-02`, state the possible wipe whenever `F7.3-01` wrote re-establishment steps, including when AOSPA's documentation left the requirement unsettled. `F7.3-08` writes `Project-Comprehension.md`: fold in the `IMPL-52`/`-53`/`-54` derivation-mechanism evidence entry (`AUDIT-FIX-37`). If no Step 1 amendment has run by then, `CQ-13` and `EV-20`'s host wording (`AUDIT-FIX-57`) may be corrected in the same byte-careful edit. Do not start in the `Faz7.2` session. |
| Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md | READY_WITH_WARNINGS | AUDIT-FIX-22 | satisfied | Agreement half only: `F8.1-06` after `Faz7.2`, `F8.1-07` after `Faz7.3`, then `F8.1-10`. Static half done (`IMPL-92`). Unchanged since the tenth audit. | Do not repeat `F8.1-01`–`05`, `08` or `09`. Compare `Faz7.2`'s `build-evidence.txt` md5s and sizes with `IMPL-92`'s values, then `Faz7.3`'s on-device values; record a missing leg as not reached with its reason. `F8.1-10` edits `Project-Ontology.md`, which contains NUL bytes: edit byte-preservingly and diff the file afterwards (`AUDIT-FIX-22`). |
| Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md | READY_WITH_WARNINGS | AUDIT-FIX-50 | satisfied | The functional test on the carry-over path. Depends on `Faz8.1`'s carry-over on both layers with three-way agreement and on `Faz7.3`'s device on the `beryl` build, both earlier in this queue. Unchanged since the tenth audit. | At `F8.3-08`, in the same edit as the evidence record, point `docs/release-checklist.md` section 3's `C-04`/`C-17` labels (lines 135, 148) and PC-04's "DEFECTIVE via smoke.sh" comment (line 176) at section 4's repair notes (`AUDIT-FIX-50`). Grade PC-17 on the two mount counts and take the trap reading from `prefs.trap.armed`. |
| Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md | DEFERRED | none | blocked | **Not queued.** Host-side half `implemented`. `F4.6-07` was gated on the superseded `Faz4.1`; `DEC-19` keeps `FIND-3.5-01` and `FIND-4.5-02` as knowledge. | Completing it would be a new user decision and a new sub-plan. |
| Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | SUPERSEDED | none | independent | `superseded` 2026-09-03 by `DEC-14`. | **Do not revive it.** |
| Planner-docs/Faz-4-Plans/Faz4.7-ultra-high-resolution-sensor-mode.md | SUPERSEDED | none | independent | `superseded` 2026-09-03 by `DEC-14`. | **Do not revive it as project work.** |
| Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md | COMPLETE | none | satisfied | `IMPL-91`: all ten acceptance criteria met. Its outputs re-read on GitHub by this audit. Line 5's Hetzner mention is history. | none. Its transition is `Faz7.2`'s `F7.2-01`. |
| Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md | COMPLETE | none | satisfied | `IMPL-93`: all ten acceptance criteria met without a merge, build, checkout or rental; `DEC-08` recommendation defer. | none. A merge would be a new decision under `DEC-08`. |
| Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md | COMPLETE | none | satisfied | `IMPL-03`. The edit is in both trees and in the pinned fork (`d48816f`). Ledger status stays `implemented` because the effect is unverified; **`Faz7.3` `F7.3-08` owns that verification**, so the row is not queued in its own right. | none. Do not report it `verified` before `Faz7.3` step 3 passes. |
| Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md | COMPLETE | none | satisfied | `IMPL-01`; `DEC-01` answered (private remote `ahmetxa/ishtar`). | none. |
| Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md | COMPLETE | none | satisfied | `IMPL-02`; `DEC-10` answered. | none. |
| Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | COMPLETE | AUDIT-FIX-25 | satisfied | `IMPL-06`. One stale forward reference (accepted). | none. |
| Planner-docs/Faz-1-Plans/Faz1.4-toolchain-procedure-record.md | COMPLETE | none | satisfied | `IMPL-07`. Its WSL2 sentence is history; `F7.1-12` retired the WSL-era records (`IMPL-91`). | none. |
| Planner-docs/Faz-1-Plans/Faz1.5-static-safety-probes.md | COMPLETE | none | satisfied | `IMPL-05`. | none. |
| Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md | COMPLETE | none | satisfied | `IMPL-08`. | none. |
| Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md | COMPLETE | none | satisfied | `IMPL-04`; extended by `IMPL-55`/`-56`, repaired by `IMPL-80`. | none. |
| Planner-docs/Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md | COMPLETE | none | satisfied | `IMPL-09` … `IMPL-12`. | none. |
| Planner-docs/Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md | COMPLETE | none | satisfied | `IMPL-13`. | none. |
| Planner-docs/Faz-2-Plans/Faz2.4-tiles-hide-disposition.md | COMPLETE | none | satisfied | `IMPL-71`, `IMPL-75`; `DEC-02` answered. | none. |
| Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md | COMPLETE | none | satisfied | `IMPL-16`; closed at the file by `IMPL-62`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | COMPLETE | none | satisfied | `IMPL-18`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md | COMPLETE | none | satisfied | `IMPL-20`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.4-consumer-compatibility-check.md | COMPLETE | none | satisfied | `IMPL-21`, `IMPL-22`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md | COMPLETE | none | satisfied | `IMPL-23`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md | COMPLETE | none | satisfied | `IMPL-24`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.7-agc-photo-size-pin.md | COMPLETE | none | satisfied | `IMPL-52`, `IMPL-53`, `IMPL-54`; `DEC-18`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md | COMPLETE | AUDIT-FIX-33 | satisfied | `IMPL-55`, `IMPL-56`. Built at four fields; the three-field text residue is accepted history. | none. |
| Planner-docs/Faz-3-Plans/Faz3.9-coexistence-bracket.md | COMPLETE | none | satisfied | `IMPL-57`, `IMPL-58`, `IMPL-83`, `IMPL-85`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.10-pin-stickiness-matrix.md | COMPLETE | none | satisfied | `IMPL-60`, `IMPL-61`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.11-phase-closure-and-configuration-record.md | COMPLETE | none | satisfied | `IMPL-62`, `IMPL-63`, `IMPL-89`; Phase 3 marked successful (`DEC-21`). | none. |
| Planner-docs/Faz-4-Plans/Faz4.2-duration-rows.md | COMPLETE | none | satisfied | `IMPL-64`. | none. |
| Planner-docs/Faz-4-Plans/Faz4.3-patch-table-consolidation.md | COMPLETE | AUDIT-FIX-22 | satisfied | `IMPL-65`, `IMPL-66`. Warning carried for anyone re-reading the ontology's `Escape` column. | none. |
| Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | COMPLETE | none | satisfied | `IMPL-67`, `IMPL-68`, `IMPL-70`. | none. |
| Planner-docs/Faz-4-Plans/Faz4.5-active-array-raise.md | COMPLETE | none | satisfied | `IMPL-27` … `IMPL-30`. | none. |
| Planner-docs/Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md | COMPLETE | none | satisfied | `IMPL-14`. | none. |
| Planner-docs/Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md | COMPLETE | none | satisfied | `IMPL-15`. | none. |
| Planner-docs/Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md | COMPLETE | none | satisfied | `IMPL-17`. | none. |
| Planner-docs/Faz-6-Plans/Faz6.2-aon-module-disposition.md | COMPLETE | none | satisfied | `IMPL-72`, `IMPL-75`; `DEC-04`. `FIND-6.2-01`'s cross-reference discharged by `Faz7.2` section 1; `FIND-6.2-03` routed to `Faz7.3`. | none. |
| Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | COMPLETE | none | satisfied | `IMPL-76`, `IMPL-81`. | none. |
| Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | COMPLETE | none | satisfied | `IMPL-19`, `IMPL-78` … `IMPL-89`; `DEC-23`. | none. Its section 3 labels are corrected by `Faz8.3` `F8.3-08` (`AUDIT-FIX-50`). |
| Planner-docs/Faz-9-Plans/Faz9.3-documentation-consolidation.md | COMPLETE | none | satisfied | `IMPL-77`, `IMPL-78`, `IMPL-81`. | none. |

**Execution queue state: READY.** Four rows are queued, all `READY_WITH_WARNINGS`. No blocking finding applies, no path is unsafe, no target is missing, and no queued row's dependency state is `blocked` or `unknown`.

**Queue head: `Faz7.2`, starting at `F7.2-01`.** Then `Faz7.3`, `Faz8.1`'s agreement half, and `Faz8.3`.

**Human stop gates are built into the queue and are not blockers:**

- `Faz7.2`: the rental approval after `F7.2-01`, Console deletion, and any post-session push of `fixes.diff`.
- `Faz7.3`: the go/no-go, the firmware approval, and the stay-or-restore choice.
- `Faz8.1`: `DEC-07`.
- `Faz8.3`: root, and the final enable state.

**Workspace precondition, for the user, not a finding.** Run 20 is uncommitted: `Faz7.2`, the ledger and `docs/pre-rental-plan.md`. This audit adds a fourth file. A Step 4 run contract stops on an unrelated dirty worktree. These files are the plan the rental session executes, so they are related, but a local commit first gives that session a clean baseline. Whether to commit is the user's call.

## 13. Priority Fix List

**No P0 or P1 finding is open.** The register holds 57 findings. Three are new this run (`AUDIT-FIX-55` … `-57`), and three were resolved this run (`-52`, `-53`, `-54`).

**Ten remain active:**

| Group | Findings |
|---|---|
| P2 open | `-22` |
| P3 open | `-37`, `-41`, `-42`, `-50`, `-55`, `-56`, `-57` |
| P3 accepted | `-25`, `-33` |

Findings resolved or marked `not_applicable` before the tenth audit are not re-listed row by row; nothing since has touched their subject matter.

| Finding ID | Severity | Status | Affected Files | Issue | Required Action |
|---|---|---|---|---|---|
| AUDIT-FIX-22 | P2 | open | Planner-docs/Project-Ontology.md | Carried. 7 control bytes below 0x20, including 2 NUL, in the `Escape` column (tenth audit: offsets 42806–43113). Content search on the file fails silently. The ontology is unchanged since then (`git diff --stat HEAD` empty). **Queued writer:** `F8.1-10`. `AUDIT-FIX-57` adds a second reason to edit the file (invariant 11). | Unchanged: replace the `Escape` column's raw bytes with the project's octal `printf '%b'` convention in a bounded amendment of that one table, then confirm the file reappears in `rg -l InitializeScalerStaticCaps`. Until then, every edit to this file must be byte-preserving and diffed, and no escape may be transcribed from that column. |
| AUDIT-FIX-55 | P3 | open | Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | **New.** `IMPL-94` already changed runbook section 10's built-symlink test to `$OUT/vendor/lib64/camera/aon_front.pb` (runbook lines 485–488). `Faz7.2` still plans that edit as future work: section 4 line 79; `F7.2-01` lines 222–223 ("Before renting, correct … from `$OUT/odm/…`"); `F7.2-07` line 253; `VAL-GATE` line 306; `VAL-DOCS` line 320; contract-table line 330; the section 11 risk at line 374; section 12 line 389. Section 6 line 196 says in present tense that the runbook tests `[ -L "$OUT/odm/lib64/camera/aon_front.pb" ]`, which is now false. Section 1 line 18 names the `-52`/`-53`/`-54` repairs as unchanged but not the symlink correction. Run 20's mandate was provider facts, so this is carried staleness, not a run 20 error. It fails safe: the runbook wins on disagreement, and the edit has nothing left to change. | **Rental day:** perform `F7.2-01`'s symlink step as a verification. Read back runbook lines 485–488 and the expected `readlink` target `/odm/lib64/camera/aon_front.pb`, run `bash -n` on the section 10 block, and record "correction made by `IMPL-94`, verified" in the gate record. Do not re-edit the runbook. **Later bounded Step 2 amendment, after the rental:** reword the listed lines to past tense, citing `IMPL-94`, and correct section 6 line 196. |
| AUDIT-FIX-56 | P3 | open | Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, Planner-docs/Planing-Ledger.md | **New, the carried plan half of `AUDIT-FIX-52`.** `Faz7.2` section 8 line 292 and `VAL-SYNC` line 307 compare `manifest-resolved.xml` against the 13 pins of `ishtar-beryl.xml` "at `22283d8`". A permitted fix — a removed `clone-depth`, deleted `vendor/xiaomi/camera` lines, or a deleted `display-drivers` pin — legitimately changes that set, so a correct session would grade itself failed. Separately, ledger `DEC-25` item (3) still reads "a sync failure stops the session" without the sync-path exception now in runbook section 4. `IMPL-94` recorded that disagreement, and `DEC-26` did not amend item (3). | **Paid session:** grade `VAL-SYNC` and the resolved-manifest criterion against `22283d8` as amended by `fixes.diff`, and state that basis in the section 13 ledger row. **At the next ledger edit:** annotate `DEC-25` item (3) with the runbook section 4 exception (`IMPL-94`, `AUDIT-FIX-52`). **Later bounded amendment:** reword lines 292 and 307 the same way. |
| AUDIT-FIX-57 | P3 | open | Planner-docs/Main-Planing.md, Planner-docs/Project-Comprehension.md, Planner-docs/Project-Ontology.md, docs/reverse-engineering-toolchain.md | **New, registered so the carried `DEC-26` wording stays visible.** Confirmed routed by run 20, ledger section 7 and pre-rental step 3b to the next Step 1 amendment with `-41` and `-42`: `Main-Planing.md` lines 75, 211 and 265 ("a rented Hetzner VDS", R9) and `Project-Comprehension.md` `EV-20` ("Hetzner Cloud server (Ubuntu 22.04 LTS, CCX53)"). **Measured this run, the list misses three live statements of the same host fact:** `Project-Comprehension.md` `CQ-13` line 25; `Project-Ontology.md` invariant 11 line 429 ("Hetzner Cloud server — Ubuntu 22.04 LTS on a CCX53, 32 vCPU / 128 GB / 600 GB NVMe"); `docs/reverse-engineering-toolchain.md` line 220. Not live: `Faz7.1` line 5 and index line 10 (history). No queued work item reads any of them; no phase meaning changes. | At the next deliberate Step 1 amendment, together with `-41` and `-42`: reword all seven to "a rented Scaleway POP2-32C-128G (`DEC-26`)", or to a provider-neutral "rented VDS" with `DEC-26` cited. Do not cut a snapshot for these alone. Edit `Project-Ontology.md` byte-preservingly (`-22`). If `Faz7.3` `F7.3-08` or `Faz8.1` `F8.1-10` writes the comprehension or ontology file first, it may fold its lines in then. The toolchain doc line goes in the same change set as a docs-only edit. |
| AUDIT-FIX-50 | P3 | open | docs/release-checklist.md | Carried, document half. `docs/release-checklist.md` still labels `C-04` with `FIND-3.10-01` (line 135) and `C-17` with `FIND-3.7-02` (line 148), and PC-04 still reads "DEFECTIVE via smoke.sh" (line 176). The sub-plan half was resolved by run 19. | `F8.3-08` owns it: in the same edit as the v2.2-on-`beryl` evidence record, point those labels and the comment at section 4's repair notes. |
| AUDIT-FIX-37 | P3 | open | Planner-docs/Project-Comprehension.md | Carried. `Project-Comprehension.md` still cites `IMPL-52`, `-53` and `-54` zero times (file unchanged since the tenth audit). The remaining natural owner is `Faz7.3` `F7.3-08` (`TRACE-13`, `ARC-06`). | Add the derivation mechanism as an evidence entry when `F7.3-08` writes the file. |
| AUDIT-FIX-41 | P3 | open | Planner-docs/Main-Planing.md | Carried, unchanged: section 8's step 5 still describes `pref_camera_picturesize_back_key` as an ordinary settings item. No queued row reads it; Phase 3 is closed. | At the next deliberate Step 1 amendment, rewrite step 5 to the measured configuration (`pref_48m_key=0`, `pref_camera_resolution=full`, read the derived key back) and mark it done under `DEC-21`. |
| AUDIT-FIX-42 | P3 | open | Planner-docs/Main-Planing.md | Carried, unchanged: line 22 "a third (Android 16 / beryl) has not started", line 61 "Android 16 / AOSPA `beryl` port", line 288 "Do not expand yet … G is blocked on host-environment work the user must perform". | At the same Step 1 amendment, together with `-41` and `-57`: reword all three to `DEC-24`/`DEC-26` and the branch reading of `beryl`, and mark section 9's paragraph discharged. Do not cut a snapshot for these alone. |
| AUDIT-FIX-33 | P3 | accepted | Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md, Planner-docs/Sub-Planing-Index.md | Carried. `Faz3.8` lines 120 and 163 and the index still describe three fields; the sub-plan is `verified` at four (`IMPL-55`, `IMPL-56`). | No repair required; accepted and kept visible. |
| AUDIT-FIX-25 | P3 | accepted | Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | Carried, unchanged at line 9: "Faz 4.1 narrows the RAW emission …". | No repair required; `Faz1.3` is COMPLETE. |
| AUDIT-FIX-52 | P3 | resolved | docs/build-environment.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | Runbook section 4 said "Sync failure … stop" while its table gave sync-path fixes, and `Faz7.2` gave the runbook precedence. | **Resolved in the runbook.** `IMPL-94` added the exception at section 4 lines 135–138, and `IMPL-95` kept it: a sync failure matching the shallow-sync or `vendor/xiaomi/camera` detector gets its fix, counted against the same 2 attempts. It now agrees with `F7.2-04`, so the precedence clash is gone. The plan-side grading basis is carried as `AUDIT-FIX-56`. |
| AUDIT-FIX-53 | P3 | resolved | docs/build-environment.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | The base pin was first asserted on a billed server. | **Resolved in the runbook.** Section 5 lines 186–190 compare `AOSPA/manifest` `beryl` with `7dfc0650…` and exit before renting on a move. `Faz7.2` section 4 line 74 lists it in the gate. The block passes `bash -n`, and the base read `7dfc0650…` (2026-05-24) today. |
| AUDIT-FIX-54 | P3 | resolved | docs/build-environment.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | Fail-fast lines in sections 10 and 11 contradicted "recorded, not fatal". | **Resolved in the runbook.** In section 10, a failed `repo manifest -r` is written to `manifest-resolved.err` and the block continues (lines 473–480). In section 11, each missing or failed copy is logged to `retrieval.txt`, counts are asserted without aborting, and `SHA256SUMS` is always written (lines 556–572). The operator rule for both sections is at lines 523–526. `F7.2-08` names `retrieval.txt` and cites `-54`. Both blocks pass `bash -n`; `IMPL-94` dry-ran both in a scratch directory. |

**Finding status consistency.** Ten findings are active: one P2 open, seven P3 open, and two P3 accepted. No P0 or P1 is open, so Step 4 is unblocked. The status is `PASS_WITH_WARNINGS`, not `PASS`, because those ten must stay visible during implementation.

**Project findings versus audit findings.** `FIND-3.5-01` and `FIND-4.5-02` are P1 **project** findings, which `DEC-19` keeps as knowledge. They are not audit findings and do not gate Step 4.

**Validator behaviour, stated so it is not misread.** On a `PASS_WITH_WARNINGS` audit, `--mode step3 --strict` and `--mode step4 --strict` report one error, `strict_warning=step4_has_nonblocking_warnings`: `--strict` promotes the non-blocking P2/P3 warning. **It is not a structural defect.** The gating facts are `p0_findings=0` and `p1_findings=0`.

## 14. Recommended Next Command / Prompt

**Step 4 may begin.** The status is `PASS_WITH_WARNINGS`, no P0 or P1 is open, and only P2/P3 findings remain, so the Step 4 prompt is printed. Per `docs/pre-rental-plan.md` step 4 it is limited to `Faz7.2`. Part A is `F7.2-01` on the Scaleway runbook, with no pre-rental runbook edit, and then a stop for the user's rental approval.

**Before starting it, the user decides** whether to commit run 20 and this audit locally, so the rental session starts from a clean tree, and chooses a day with the full 10-hour window free. Optional at any checkpoint: a push to the private `origin`, and what to do with `devir-teslim-promptu.md`.

**Supporting action, not a precondition:** at the next deliberate Step 1 amendment, fold in `AUDIT-FIX-41`, `-42` and `-57`.

```text
/claudeqb:claudeqb Read and return the exact canonical handoff from references/handoffs/run-step4.md, then execute it.

Context: step 4 of docs/pre-rental-plan.md, the rental-day session, on Scaleway (DEC-26). Read that file first, then git status. The eleventh Step 3 audit (2026-09-14) is PASS_WITH_WARNINGS with no open P0 or P1; queue state READY. This session is LIMITED to Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md. Do not start Faz7.3, Faz8.1's agreement half or Faz8.3. Keep the ten active findings visible: AUDIT-FIX-22, -25, -33, -37, -41, -42, -50, -55, -56, -57; this session owns -55's verification and -56's grading basis. docs/build-environment.md is the operative runbook: where it and the sub-plan disagree, follow the runbook and record the disagreement.

Part A (free, host only): F7.2-01. (1) Run runbook section 5's scripted block exactly as written in Git Bash, with GH=C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe, python not python3, and TMPDIR outside the workspace; record the exit status and the "pre-rental checks passed" line (it includes the AOSPA/manifest beryl base-pin check). (2) Do NOT edit the runbook before renting. The section 10 symlink correction was made by IMPL-94: read back runbook section 10's test ($OUT/vendor/lib64/camera/aon_front.pb, readlink kept, expected target /odm/lib64/camera/aon_front.pb), run bash -n on that block, and record "made by IMPL-94, verified" (AUDIT-FIX-55; ignore Faz7.2 section 6's present-tense odm claim). (3) Ask me for runbook section 5's four manual checks and record my answers: Scaleway Organization quotas show identity validated, POP2-32C-128G quota at least 1, and Block Storage total size allowing 610 GB; my public ed25519 SSH key is in the Project the Instance will be created in; ~/Documents/Projeler/ishtar-builds/ exists outside every repository; the 10-hour ceiling fits today. (4) Re-read DEC-25 as amended by DEC-26 and runbook section 4, and state the stopping rule back in six lines: sync failure stops except the sync-path detectors; at most 2 manifest-class fix attempts; out-of-memory kill is a stop with no retry; hour 8 retrieve and tear down; 10 h ceiling over every billed resource with every started hour counted whole; teardown whatever the outcome. Write the gate record under snapshots/ (text only, no address, no key, no volume ID) and a short ledger row for the gate.

Then STOP and ask for my explicit rental approval. Without it, end the session with the gate result recorded.

Part B (paid, only after my approval in this session): runbook sections 6 to 13 in order, as F7.2-02 to F7.2-10. POP2-32C-128G, Ubuntu 22.04 (24.04 only as the DEC-22 fallback, noted in the timeline), system volume Block 5K 40 GB, ishtar-src 5K 310 GB, ishtar-out 15K 260 GB, flexible IPv4 kept, no snapshot, image or backup. Volume IDs and the address stay in the shell or on paper. Section 7's volume block has never run: read its output before continuing, and stop on any "stop" line. Record per stage only start and end time (UTC), exit status, error class and the last lines of a failing log; never whole logs. Fixes are server edits to .repo/local_manifests/ishtar-beryl.xml recorded in ~/evidence/fixes.diff, at most 2, manifest-class only, never pushed during the session. Grade VAL-SYNC and the resolved-manifest criterion against 22283d8 as amended by fixes.diff, and say so in the ledger row (AUDIT-FIX-56). At hour 8, retrieve what exists and tear down. Do not tear down until sha256sum -c passes for every retrieved file. Teardown per runbook section 12: delete the Instance (never power off or standby), then delete every Block volume by name (system, ishtar-src, ishtar-out), then any flexible IP; confirm zero Instances, zero volumes, zero flexible IPs and zero snapshots in the Project and zone; record the last deletion time and elapsed hours rounded up against the 10-hour ceiling, whatever the build outcome. Write the runbook section 13 ledger row (with the Ubuntu release, disk.txt sizes and the four zero counts), the Phase 8 readiness statement and the ledger section 7 viability check.

Rules: no token, key, password, server address or volume ID written anywhere; no device command; no push and no commit without asking me; do not touch devir-teslim-promptu.md. Work in small verified slices and do not load other sub-plans.
```

**Token and queue reminder.**

- **Part A is cheap:** one scripted block, one read-back, and four questions.
- **Part B is where token and money risk both peak.** Keep the stopping rule in the session's own context, and read only exit status, stage, error class and log tails.
- **After `Faz7.2`, the queue continues in fresh sessions:** `F8.1-06` from `Faz7.2`'s evidence, then `Faz7.3` (the flash, on a separate day), `F8.1-07`, `F8.1-10`, and `Faz8.3`.

Do not run the prompt from this audit session.

## 15. Audit Result

- **Final status: PASS_WITH_WARNINGS.**
  - **Coverage:** nine main phases, nine phase folders and 42 sub-plan files, all structurally compliant.
  - **Validators:** `--mode step3-preflight --strict` passed before writing (`error_count=0`, `warning_count=0`, `secret_findings=0`, `subplan_count=42`). `--mode step3 --strict` and `--mode step4 --strict` were run after writing, with the expected `strict_warning` described in section 13.
  - **Findings:** ten active (one P2 open, seven P3 open, two P3 accepted), none P0 or P1. Three resolved this run (`-52`, `-53`, `-54`), and three new, all P3 (`-55`, `-56`, `-57`).
  - **Queue:** READY, with four rows headed by `Faz7.2`.
- **Confidence: high** on the value-by-value match of `Faz7.2` against the runbook, the closure of `-52`/`-53`/`-54` in the runbook text, `bash -n` on all ten blocks, the GitHub pins and visibility read today, structure, and coverage. **Medium** on the runbook's Scaleway-side assumptions, which only the rental day can confirm: 22.04 availability, the quota, and how a volume ID shows in the guest. **Not assessed for content this run:** the 41 sub-plans run 20 did not touch, on which the tenth audit's assessments stand.
- **Only `Planner-docs/Sub-Planing-Audit.md` was modified by this audit.** No sub-plan, index, ledger, master plan, ontology, comprehension file, runbook or source file was written. The runbook blocks were extracted to this session's scratchpad for `bash -n` and deleted. No device command, no rental, no GitHub write, no commit and no push.
- **Unexpected modifications: none detected.** The other entries in `git status` were present before this audit began: run 20's three uncommitted files, and the untracked `devir-teslim-promptu.md`, which was not touched.
- **Step 4 can safely begin**, limited to `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md`. Part A is `F7.2-01`, with the symlink step as a verification and no pre-rental runbook edit. The session then stops for the user's rental approval.
