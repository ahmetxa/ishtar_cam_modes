# Sub-Planing Audit

> Step 3 audit (ClaudeQB), the twelfth audit, dated 2026-11-19. Body language: English. It supersedes the eleventh audit of 2026-09-14.
> Scope: 47 sub-plans in 10 phase folders (`Planner-docs/Faz-1-Plans/` to `Planner-docs/Faz-10-Plans/`). Five of them, `Faz10.1` to `Faz10.5`, are new from planning run 21.
> Evidence file: `AUDIT12_FINDINGS.md` (reviews of 2026-11-17, sessions `4 · O3a` and `4 · O3b`). That file keeps the full text of every finding; this audit condenses it.
> Finding IDs continue the register: `AUDIT-FIX-01` to `AUDIT-FIX-57` come from earlier audits, and `AUDIT-FIX-58` to `AUDIT-FIX-109` are new.

## 1. Audit Summary

status: PASS_WITH_WARNINGS

**Short explanation.** All ten Main phases have their folders. The 47 sub-plans all carry the 13 required sections. The Index references all 47 files, and no reference is broken. The ledger gives a status for every file.

No finding is P0 or P1. Six P2 findings are open. Five of them sit in the Phase 10 plans that Step 4 runs next, and one is the carried `AUDIT-FIX-22`. 49 P3 findings are active (45 open, 4 accepted). Most of them are stale wording in Main, the Index, the ledger and the support documents, left behind by the `DEC-28` retirement.

**Counts (active findings, status `open` or `accepted`).** P0 0, P1 0, P2 6, P3 49. The P2 findings are all open: `AUDIT-FIX-22`, `-69`, `-70`, `-78`, `-80` and `-86`. The accepted P3 findings are `AUDIT-FIX-25`, `-33`, `-94` and `-95`. The register holds 109 IDs (`AUDIT-FIX-01` to `-109`). This rewrite discharges `AUDIT-FIX-90` and `-96`, so both are `resolved` (sections 2 and 4).

**Is Step 2 output usable for Step 4? Yes, with warnings.** The execution queue state is READY. The queue head is `Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md` (dependency `independent`), which is a read-only survey. Queue split: 34 COMPLETE (ledger `verified`), 7 SUPERSEDED (`Faz4.1`, `Faz4.7`, `Faz6.1`, `Faz7.2`, `Faz7.3`, `Faz8.1`, `Faz8.3`), 1 DEFERRED (`Faz4.6`), and 5 READY_WITH_WARNINGS (`Faz10.1` to `Faz10.5`).

**Most important finding: `AUDIT-FIX-69` (P2, open).** Main :91 and the `Faz10.2` acceptance (:114) require 1080p60 and 4K60 video in all nine modes. The module's own record says video fails in the DCG and LN modes. `Faz10.2` names no outcome for a failed recording, so its exit, and with it `Faz10.5`, has no defined path.

Three more P2 findings sit on the same device window:
- `AUDIT-FIX-70`: the `Faz10.2` test build can take in `Faz10.4` tree edits.
- `AUDIT-FIX-78`: QS tiles and the root grant are left open under unchanged v2.2.
- `AUDIT-FIX-80`: four `Faz10.4` device writes are outside the approval gate.

**Most important remediation action.** Before the first device bracket of `Faz10.2`, make a bounded Step 2 touch-up of `Faz10.2` and `Faz10.4`:
- define the video-failure outcome per mode (`AUDIT-FIX-69`);
- gate `F10.2-07` to a diff of `setmode.sh` alone (`AUDIT-FIX-70`);
- forbid tile taps and the root grant while v2.2 is installed (`AUDIT-FIX-78`);
- add the device push (`adb push`), the tile-list backup and restore, and the cleanup to the `Faz10.4` approvals (`AUDIT-FIX-80`).

In `Faz10.1`, add a host-only file mode for `VAL-101-IDENTITY` in `F10.1-01` and `F10.1-02` (`AUDIT-FIX-86`). The rest of the survey is read-only and can start as written.

**Carried IDs from the eleventh audit (decision 6 applied).**
- `AUDIT-FIX-22` (P2, open): goes with the Ontology edit for S3-07 (`AUDIT-FIX-99`).
- `AUDIT-FIX-37` (P3, open): goes with the Comprehension edit for S3-06 (`AUDIT-FIX-98`).
- `AUDIT-FIX-50` (P3, open): narrowed to its document half. `Faz10.5` owns it (`F10.5-12`; see `AUDIT-FIX-77`), and the `beryl` condition is moot.
- `AUDIT-FIX-41`, `-42` (met by retirement) and `-57` (main portion): resolved. The residue of `-57` is carried as `AUDIT-FIX-62` and `-100`.
- `AUDIT-FIX-52` to `-54`: resolved, confirmed at their current lines.
- `AUDIT-FIX-55` and `-56`: not_applicable.

## 2. Reviewed Sources

**Review runs.** All runs took place on 2026-11-17 on branch `integrate/impl-96`. The inputs were unchanged since `Window 4 O1` (`git diff --stat 2f39b73..HEAD` over them is empty). Each run's task text was `ORCHESTRATION_PLAN.md` Ek A.8.1 plus that run's A.8.2 block. Status, bytes and extra reads come from the `### Runs` tables (`AUDIT12_FINDINGS.md:183` and `:389`). The inputs come from the `W4O2P02` table in `ORCHESTRATION_PLAN.md` §8.3.

| Run | Session | Agent | Status | Input bytes | Extra reads | Inputs read (bytes) |
|---|---|---|---|---|---|---|
| cov-a | 4 · O3a | reviewer | complete | 374,145 | about 9 KB: Ledger `:584-619` (Raised by cells), the TP heading list, `git log` metadata | Phase 10 sub-plans 192,830; Main 77,019 (whole); Index 64,839; ledger 11,345; Comprehension 2,394; eleventh audit 13,377; TP and RS3 5,453; task text 6,888 |
| rdy-a | 4 · O3a | reviewer | complete | 389,140 | 1,281 B: `docs/release-checklist.md:132-138`, `:145-151`, `:173-179` | Phase 10 sub-plans 192,830; module code 87,075; `smoke.sh` and `build-release.py` 32,888; docs ranges 7,695; `ishtar-aon-fix` 2,467; CHANGELOG 5,411; Main 20,250; Index 12,155; ledger 5,349; PROJECT_LOG 821; eleventh audit 8,565; TP, RS3 and PB 5,917; task text 7,717 |
| sec-a (r1) | 4 · O3a | security-reviewer | partial | 349,931 | about 2.5 KB: grep hits in `Main-Planing.md`, `PROJECT_LOG.md:717-719,1125`, `scripts/build-release.py:53,56,163` | Phase 10 sub-plans 192,830; repository rules and code 117,585; Main 15,582; Index 3,904; ledger 6,253; PROJECT_LOG 821; eleventh audit 2,051; TP, RS3 and PB 4,177; task text 6,728 |
| sec-a (r2) | 4 · O3a | reviewer | complete | 349,931 | none | Same inputs as r1. The user chose a full rerun (option (b)). It was the fourth reviewer of the session. |
| cov-b | 4 · O3b | reviewer | complete | 385,848 | about 0.8 KB: read-only `git log` and `git show --stat` output (commit times for S3-02) | Phase 3 sub-plans 268,994; Main 7,973; Index 64,839; ledger 19,961; eleventh audit 12,906; TP and RS3 5,453; task text 5,722 |
| cov-c | 4 · O3b | reviewer | complete | 363,276 | about 3.6 KB: Ledger `:42` (raw, 3,403 B) and an `awk` citation scan of Ledger `:533` | Phase 1, 2, 5 and 6 sub-plans 223,031, plus a 373 B light read of `Faz6.1`; Main 7,114; Index 64,839; ledger 15,140 (including a 300 B format view); Comprehension 8,039; Ontology 4,835; toolchain document 12,654; eleventh audit 14,765; TP and RS3 5,453; task text 7,033 |
| cov-d | 4 · O3b | reviewer | complete | 372,294 | about 2.1 KB, including `docs/build-environment.md:1-10` | Phase 4, 7, 8 and 9 sub-plans 218,870, plus 6,033 B of light reads; Main 10,359; Index 64,839; ledger 39,416; eleventh audit 21,227; TP and RS3 5,453; task text 6,097 |
| PAT4 | 4 · O3b | orchestrator | complete | 42 files | none | The 42 sub-plans of Phases 1 to 9, scanned by the Ek A.8.3 script (`py -3`). It printed counts, then `--locations`, and never line text. |

Run notes:
- **sec-a (r1)** returned `partial` because its agent had no shell, so `wc` and `awk` did not run. The orchestrator checked its long-line coverage afterwards. Both runs are merged; their temp IDs carry `(r1)` and `(r2)`.
- **cov-a** copied two AGC preference values into its detail file, and **cov-b** copied one. All three are withheld in the evidence file and here.
- **Light reads.** SUPERSEDED and DEFERRED files got a light read only: `wc`, the heading lines, and a count of `supersed`, `DEC-28` and `DEC-14`. `Faz4.6` also had its sections 1 and 13 read.

**Files inspected for this rewrite.**
- `AUDIT12_FINDINGS.md`: both sessions, with their findings, dispositions, queue rows, section notes, runs and PAT4.
- The eleventh `Planner-docs/Sub-Planing-Audit.md`, used for structure and ID continuity only.
- `Planner-docs/Sub-Planing-Index.md` section 3 (:73-172).
- `Planner-docs/Planing-Ledger.md` section 4 (:65-116), the status column of rows :69-115.
- `ORCHESTRATION_PLAN.md` §8.3.
- The template, `Third-Planner.md` :295-552.

**Folders inspected.** The reviewers inspected `Planner-docs/` and all ten `Faz-<n>-Plans/` folders. cov-a, cov-b and cov-c counted files with `ls` and `wc`, and cov-d listed them with `ls -R`.

**Important commands run.**
- By the reviewers:
  - `wc -l -c` on each input;
  - `awk` lists of lines longer than 760 characters, each such line read raw;
  - `awk '/^#/'` heading lists;
  - read-only `git log` forms (`--oneline`, `-L`, `-S`) and `git show --stat`;
  - the grep tool where `bash` refused `grep`.
- By the orchestrator: `git diff --stat 2f39b73..HEAD`, which was empty.
- No run executed the validator, a test or a device command (§8.3 item 7).

**Ledger line numbering (discharges `AUDIT-FIX-96`).** Ledger lines in this audit are cited by `def2685` numbering. That numbering is identical to HEAD, because `Planner-docs/` is unchanged since.
- Planning run 21, not `IMPL-96`, shifted ledger `:52` (+1; it now holds `SNAP-2026-09-04-MAIN`) and `:651` (now the `FIND-2.3-03` row). The shifting commits are `3e7805e` (+20/-11) and `081790f` (+3/-3). Ledger `:19` did not move.
- No format repair is opened. The rows at `:501`, `:506` and `:507` have 6 or 8 pipe characters, and `:503`, `:511` and `:512` are blank. All of these predate both `IMPL-96` and run 21.

With this text in place, `AUDIT-FIX-96` is `resolved`.

**Things not verified.**
- **The validator.** None of the review runs and none of the drafts ran it. The merge step runs it, and the expected non-blocking warning is `step4_has_nonblocking_warnings=P2:6,P3:49`. `GATE4` records the new gate baseline in the plan (§8.3 item 6), not here.
- **Device state.** No `adb` command was run.
- **Comprehension lines.** `:145` and `:149` were not confirmed for S3-06. The orchestrator checked `:95` and added it to `AUDIT-FIX-98`.
- **Main sha256.** The value recorded at Ledger `:42` was not compared (cov-a).
- **Phase 10 files.** Line endings and encoding were not checked (cov-a).
- **Eleventh audit.** Lines `:305` and `:306` were not read by cov-b.
- **SUPERSEDED and DEFERRED files.** Their content quality is not assessed; they got the light read only, by design (§8.3 item 1).
- **Tooling of this draft.** It had no shell. Line counts and long-line lists came from the read and grep tools, not from `wc` and `awk`.

No secret, identity value or AGC preference value was read into or recorded in this audit.

## 3. Main Phase Coverage Analysis

| Main phase no | Main phase heading | Expected folder | Folder exists? | Sub-plan count | Coverage status | Notes |
|---|---|---|---|---|---|---|
| 1 | Workspace safety net | Planner-docs/Faz-1-Plans/ | Yes | 6 | OK | All six `verified` (Ledger :69-74). |
| 2 | Ship and re-baseline v2.1 | Planner-docs/Faz-2-Plans/ | Yes | 4 | OK | All four `verified` (Ledger :75-78). |
| 3 | AGC stable at 12.6 MP under 50 MP | Planner-docs/Faz-3-Plans/ | Yes | 11 | OK | All eleven `verified` (Ledger :79-89). Closed on AOSPA Android 15 only (`DEC-21`); not carried to HyperOS 4 (`DEC-28`, `DEC-33`). The Index entry lacks that scope note (`AUDIT-FIX-93`). |
| 4 | Minimal correct HAL patch | Planner-docs/Faz-4-Plans/ | Yes | 7 | OK | `Faz4.2`-`4.5` `verified`. `Faz4.1` and `Faz4.7` SUPERSEDED (`DEC-14`). `Faz4.6` DEFERRED: host half `implemented`; `F4.6-07` is gated on the superseded `Faz4.1`. Main's Phase 4 slice contradicts its end state (`AUDIT-FIX-107`). |
| 5 | Mode-0 12-bit composition | Planner-docs/Faz-5-Plans/ | Yes | 3 | OK | All three `verified` (Ledger :97-99). |
| 6 | AON fix upstreaming | Planner-docs/Faz-6-Plans/ | Yes | 2 | OK | ROM target retired by run 21. `Faz6.1` SUPERSEDED (`DEC-28`, Ledger :100); `Faz6.2` `verified` (Ledger :101; row text `AUDIT-FIX-97`). |
| 7 | Android 16 build environment | Planner-docs/Faz-7-Plans/ | Yes | 3 | OK | Retired 2026-11-15 (`DEC-28`, Main :230). `Faz7.1` `verified` history; `Faz7.2` and `Faz7.3` SUPERSEDED. No new sub-plan is owed, because the goal moved to Phase 10 (`DEC-32`). |
| 8 | Camera work on Android 16 + kernel LTS | Planner-docs/Faz-8-Plans/ | Yes | 3 | OK | Retired (`DEC-28`, Main :240). `Faz8.2` `verified` history; `Faz8.1` and `Faz8.3` SUPERSEDED. |
| 9 | Release engineering | Planner-docs/Faz-9-Plans/ | Yes | 3 | OK | All three `verified`; no ROM dependency (Index 4d, 4e). `Faz9.2:54` still points at the superseded `Faz7.2` (`AUDIT-FIX-105`). |
| 10 | HyperOS 4 camera module adaptation | Planner-docs/Faz-10-Plans/ | Yes | 5 | OK | New (run 21, `DEC-32`). All five are `planned` (Ledger :111-115). |

- **Counts.** Main has ten phase rows (:139-148) and ten `### Phase` headings. Per-phase counts, measured by the reviewers: 6, 4, 11, 7, 3, 2, 3, 3, 3 and 5, total 47. They agree with Index :312 and Ledger :42 (`subplan_count=47`, `phase_folder_count=10`, `main_phase_count=10`).
- **No missing phase and no extra folder.** The 47 include the seven SUPERSEDED files and the DEFERRED `Faz4.6`.
- **Phase 10 signal coverage.** Main's five Phase 10 acceptance signals (:302-306) map to `Faz10.1` to `Faz10.5` in order. The tile switch of signal 4 may close in `Faz10.5` through `VAL-104-SWITCH`. `Faz10.5` §13 maps all five.
- **Main phase text.** Coverage is complete, but some present-tense Main text lags the record (section 9): `AUDIT-FIX-58`, `-59`, `-60`, `-61`, `-72` and `-107`.

## 4. Sub-Plan File Inventory

Structure was checked on all 47 files. Each has one H1 whose `Faz <n>.<m>` number agrees with its filename and folder, and the 13 required sections. Content was read in full for every COMPLETE and every Phase 10 file. The seven SUPERSEDED files and the DEFERRED `Faz4.6` got the light read. H1 titles are given verbatim where the evidence file quotes them (Phase 10). For Phases 1 to 9, the column gives the H1 phase number the reviewers matched.

| Sub-plan file | Detected H1 | Phase match | Section structure | Content quality | Notes |
|---|---|---|---|---|---|
| Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md | `Faz 1.1` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md | `Faz 1.2` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | `Faz 1.3` | OK | OK | COMPLETE history | `AUDIT-FIX-25` (P3 accepted): :9 still names `Faz4.1`; no repair. |
| Planner-docs/Faz-1-Plans/Faz1.4-toolchain-procedure-record.md | `Faz 1.4` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-1-Plans/Faz1.5-static-safety-probes.md | `Faz 1.5` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md | `Faz 1.6` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md | `Faz 2.1` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md | `Faz 2.2` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md | `Faz 2.3` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-2-Plans/Faz2.4-tiles-hide-disposition.md | `Faz 2.4` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md | `Faz 3.1` | OK | OK | Strong, measurable history | `AUDIT-FIX-94` (P3 accepted): says "ten" trap keys where section 6 lists twelve. |
| Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | `Faz 3.2` | OK | OK | Strong, measurable history | None. |
| Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md | `Faz 3.3` | OK | OK | Strong, measurable history | None. |
| Planner-docs/Faz-3-Plans/Faz3.4-consumer-compatibility-check.md | `Faz 3.4` | OK | OK | Strong, measurable history | None. |
| Planner-docs/Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md | `Faz 3.5` | OK | OK | Strong, measurable history | §8 :110 and §13 :177 differ by one capture; the ledger records three (:83). History note, not a finding. |
| Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md | `Faz 3.6` | OK | OK | Strong, measurable history | None. |
| Planner-docs/Faz-3-Plans/Faz3.7-agc-photo-size-pin.md | `Faz 3.7` | OK | OK | Strong; dated amendment banners | `AUDIT-FIX-91` (P3 open): snapshot stamps are local time (UTC+3), not `<UTC>`. |
| Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md | `Faz 3.8` | OK | OK | Strong; dated amendment banners | `AUDIT-FIX-33` (P3 accepted), restated by `AUDIT-FIX-90` (resolved). The plan text names three fields (:95, :120, :155, :163; Index :107), and its section 7 plans four. Five were delivered, including the front key (`IMPL-55`, `IMPL-56`, Ledger :86). The plan file needs no repair. |
| Planner-docs/Faz-3-Plans/Faz3.9-coexistence-bracket.md | `Faz 3.9` | OK | OK | Strong; dated amendment banners | None. The ledger Run ID cell and the evidence text agree. |
| Planner-docs/Faz-3-Plans/Faz3.10-pin-stickiness-matrix.md | `Faz 3.10` | OK | OK | Strong; dated amendment banners | `AUDIT-FIX-95` (P3 accepted): the §9 sentence at :140 describes the old negative-control stimulus. |
| Planner-docs/Faz-3-Plans/Faz3.11-phase-closure-and-configuration-record.md | `Faz 3.11` | OK | OK | Strong; dated amendment banners | :19 and :45 are dated-history sentences that are now stale but harmless. Note, not a finding. |
| Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | `Faz 4.1` | OK | OK (light read) | Not assessed (SUPERSEDED) | `AUDIT-FIX-104` (P3 open): no supersession note in the file. |
| Planner-docs/Faz-4-Plans/Faz4.2-duration-rows.md | `Faz 4.2` | OK | OK | Strong history; dated `DEC-14` amendments | The Index still lists it as "runs first" (`AUDIT-FIX-106`). |
| Planner-docs/Faz-4-Plans/Faz4.3-patch-table-consolidation.md | `Faz 4.3` | OK | OK | Strong history | `AUDIT-FIX-108` (P3 open): quotes Main text that run 16 removed. |
| Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | `Faz 4.4` | OK | OK | Strong history | `AUDIT-FIX-108` (P3 open). |
| Planner-docs/Faz-4-Plans/Faz4.5-active-array-raise.md | `Faz 4.5` | OK | OK | Strong history | §9 says "seven items" and lists eight; the eighth is `AUDIT-FIX-08`, recorded inline on purpose. Not a defect. |
| Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md | `Faz 4.6` | OK | OK (light read, plus §1 and §13) | Not assessed (DEFERRED) | `AUDIT-FIX-104` (P3 open): no deferral note in the file. |
| Planner-docs/Faz-4-Plans/Faz4.7-ultra-high-resolution-sensor-mode.md | `Faz 4.7` | OK | OK (light read) | Not assessed (SUPERSEDED) | `AUDIT-FIX-104` (P3 open). |
| Planner-docs/Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md | `Faz 5.1` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md | `Faz 5.2` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md | `Faz 5.3` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md | `Faz 6.1` (H1 at :1) | OK | OK (light read, headings :1 to :164) | Not assessed (SUPERSEDED) | `AUDIT-FIX-104` (P3 open): its keyword count is 0. |
| Planner-docs/Faz-6-Plans/Faz6.2-aon-module-disposition.md | `Faz 6.2` | OK | OK | COMPLETE history | Its `VAL-BUILD (deferred, Phase 7)` can no longer run (`DEC-28`). The ledger row contradicts itself (`AUDIT-FIX-97`). |
| Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md | `Faz 7.1` | OK | OK | COMPLETE history | Its §1 Hetzner wording is history. The ledger next action is stale (`AUDIT-FIX-109`). |
| Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | `Faz 7.2` | OK | OK (light read) | Not assessed (SUPERSEDED) | `AUDIT-FIX-104` (P3 open). |
| Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | `Faz 7.3` | OK | OK (light read) | Not assessed (SUPERSEDED) | `AUDIT-FIX-104` (P3 open). |
| Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md | `Faz 8.1` | OK | OK (light read) | Not assessed (SUPERSEDED) | `AUDIT-FIX-104` (P3 open). |
| Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md | `Faz 8.2` | OK | OK | COMPLETE history | §6 "`Faz8.3` exercises them on Android 16" is history. The ledger next action is stale (`AUDIT-FIX-109`). |
| Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md | `Faz 8.3` | OK | OK (light read) | Not assessed (SUPERSEDED) | `AUDIT-FIX-104` (P3 open). |
| Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | `Faz 9.1` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | `Faz 9.2` | OK | OK | COMPLETE history | `AUDIT-FIX-105` (P3 open): :54 points Android 16 verification at the superseded `Faz7.2`. |
| Planner-docs/Faz-9-Plans/Faz9.3-documentation-consolidation.md | `Faz 9.3` | OK | OK | COMPLETE history | None. |
| Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md | `# Faz 10.1 — HyperOS 4 Camera Stack Survey` | OK | OK | Specific; cites `path:line`; keeps AOSPA and HyperOS 4 evidence apart | `AUDIT-FIX-66` (:29), `-74`, `-86` (P2). |
| Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md | `# Faz 10.2 — HyperOS 4 Sensor Layer` | OK | OK | Specific; P2 gaps on the device window | `AUDIT-FIX-69`, `-70`, `-78` (P2); `-66` (:9), `-85`. |
| Planner-docs/Faz-10-Plans/Faz10.3-agc-trap-audit-and-guarded-cleanup.md | `# Faz 10.3 — AGC Trap Audit and Guarded Cleanup` | OK | OK | Specific; backup-first design | `AUDIT-FIX-68`, `-71`, `-84`, `-89`. |
| Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md | `# Faz 10.4 — SukiSU-Ultra Tile and WebUI Chain` | OK | OK | Specific; approval gate incomplete | `AUDIT-FIX-80` (P2); `-66` (:7), `-75`, `-76`, `-79`, `-83`, `-88`. |
| Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | `# Faz 10.5 — v2.3 Release` | OK | OK | Specific; runs last | `AUDIT-FIX-66` (:7, :212), `-73`, `-76`, `-77`, `-82`, `-83`, `-87`. |

## 5. Naming and Sequencing Check

**No naming issues were found.**
- **Folders.** All ten match `Faz-<n>-Plans/`.
- **Filenames.** All 47 match `Faz<phase>.<sub>-<ascii-kebab-slug>.md`. None has spaces, non-ASCII characters or a duplicate.
- **Numbering.** It is contiguous in every phase: 1.1-1.6, 2.1-2.4, 3.1-3.11, 4.1-4.7, 5.1-5.3, 6.1-6.2, 7.1-7.3, 8.1-8.3, 9.1-9.3 and 10.1-10.5. There is no gap and no duplicate number.
- **Agreement.** Folder, filename and H1 phase number agree in all 47 files.
- **Phase order.** Main's table (:139-148), the Index and the folders follow the same order, 1 to 10.

**Order inconsistencies (wording, not numbering).**
- **Phase 10.** The execution order is 10.1 first, then 10.2, 10.3 and 10.4, then 10.5. Main :284-288, Index 4e (:287), Ledger :111-115 and each sub-plan's §10 agree on it. Two binding constraints apply on top: the phone half of `Faz10.4` waits for `F10.2-04`, and only one device window may be open at a time. Index :165 ("in any order") and :192 ("may then run side by side") omit both constraints (`AUDIT-FIX-67`). `Faz10.3` §10 lacks the single-device-window rule (`AUDIT-FIX-71`).
- **Phase 4.** The Index still presents `Faz4.2`, `Faz4.3`, `Faz4.4` as the pending order, although all three are `verified` (`AUDIT-FIX-106`).
- **Phase 3.** The Index and amendment 4c still read as an active queue starting at `Faz3.8` (`AUDIT-FIX-92`).

## 6. Index Consistency Check

- **References.** None is missing, broken or unindexed. All 47 references resolve: Phase 1 at :77-82, Phase 2 at :86-89, Phase 3 at :99-104 and :106-110, Phase 4 in its block, Phase 5 at :136-138, Phase 6 at :142-143, Phases 7 and 8 in their blocks, Phase 9 in its block, and Phase 10 at :167-171 and :192.
- **Phase count.** There are 10 phases in Index §2 and §6, in Main and in the folders. The coverage counts at Index :312 match the measured counts.
- **Ledger agreement.** Ledger §4 rows :69-115 use the same 47 paths. The Phase 10 rows (:111-115) are `planned` under `SNAP-2026-11-16-SUBPLANS`, with dependencies that match the Index.

**Inaccurate or stale claims (all P3, open).**
- :43 still says the Phase 7 and 8 rows follow `SNAP-2026-09-10-MAIN` (`AUDIT-FIX-63`).
- :66, the `EV-20` bullet, still routes the rewrite to `F7.1-12`; it ran, and run 21 corrected the records (`AUDIT-FIX-64`, `-102`).
- :91, :107-110 and :252-256 still read as an active Phase 3 queue (`AUDIT-FIX-92`).
- The Phase 3 entry lacks the `DEC-28` AOSPA-only scope note (`AUDIT-FIX-93`).
- The Phase 4 order and statuses at :118 and :126 are stale (`AUDIT-FIX-106`).
- The Phase 6 block at :140 and :143 lacks its `DEC-28` note (`AUDIT-FIX-101`).
- The Phase 10 order wording at :165 and :192 is incomplete (`AUDIT-FIX-67`).
- :107's three-field description of `Faz3.8` is the accepted `AUDIT-FIX-33` residue, restated per `AUDIT-FIX-90`.

These defects come in pairs. `AUDIT-FIX-92` and `-106` are the same kind of stale queue wording, and `AUDIT-FIX-93` and `-101` are the same missing note. They stay separate because they sit in different Index sections; one bounded Index edit can fix all four.

**Routing to this audit.** Index :290 and the ledger (:42) leave four items to the twelfth audit: `AUDIT-FIX-22`, `-37` and `-50`, and the `Faz9.2` Android 16 sentence. Decision 6 assigns them:
- `AUDIT-FIX-22` goes with the Ontology edit (`AUDIT-FIX-99`);
- `AUDIT-FIX-37` goes with the Comprehension edit (`AUDIT-FIX-98`);
- `AUDIT-FIX-50`'s document half goes to `Faz10.5` `F10.5-12` (`AUDIT-FIX-77`);
- the `Faz9.2` sentence is `AUDIT-FIX-105`.

**Execution order: plausible.** The read-only survey comes first, the three device sub-plans are serialized under one device window, and the release comes last. SUPERSEDED and DEFERRED files are marked as such, and the Index says "Do not revive".

## 7. Required Section Structure Check

All 47 sub-plans were checked, not sampled.
- **Missing, duplicated or out-of-order sections: none.** Every file has one H1 and the 13 required headings, `## 1. Context` to `## 13. Next Sub-Phase Transition Criteria`, in template order. The heading checks came from `awk '/^#/'` lists (cov-a for Phase 10, cov-b for Phase 3), per-file heading counts (cov-c for Phases 1, 2, 5 and 6) and light or whole reads (cov-d for Phases 4, 7, 8 and 9). The seven light-read files show complete heading lists. `Faz6.1`'s headings sit at :1, :3, :15, :19, :31, :42, :52, :68, :95, :107, :126, :146, :156 and :164.
- **Empty or placeholder sections: none.** Every section has body text in the full reads. PAT4 found 0 placeholder hits (`PAT4-R2`) in Phases 1-9.
- **Implementation Contract tables.** Every fully read file has one in §9, with the columns `Path`, `State`, `Purpose` and `Validation Command IDs`, and repo-relative paths. Phase 10 uses the states proposed, existing, modified and generated.
- **Encoding.** cov-c measured LF line endings and 0 NUL in the 15 files of Phases 1, 2, 5 and 6. Line endings of the Phase 10 files were not checked. The NUL bytes of `AUDIT-FIX-22` are in `Planner-docs/Project-Ontology.md`, not in a sub-plan (section 11).
- **Supersession markers.** None of the seven SUPERSEDED files, and not the DEFERRED `Faz4.6` either, carries a supersession or deferral note. Their status lives only in ledger §4, the Index and the audit queue (`AUDIT-FIX-104`). This is history clarity, not a structure defect.

## 8. Content Quality and Implementability Analysis

**Phase 10, the Step 4 queue (rdy-a, `AUDIT12_FINDINGS.md:153`).**
- **Specific and verified against the tree.** Each plan names concrete lines, and rdy-a confirmed the ones it checked: `setmode.sh` restart, mode write and chcon; `post-fs-data.sh`; `customize.sh`; `action.sh`; `BaseTile.java`; the manifest; `index.html`; and the `build-release.py` options.
- **Small verified slices.** Each plan sets out local-first slices with a fastest signal: the probe refusal (10.1), the unchanged v2.2 boot (10.2), the host fixture (10.3), the `-d` launch (10.4) and the host grep (10.5).
- **Dependencies.** They are explicit: `Faz10.1` is independent, and the others are satisfied by earlier queue rows.
- **Token risk and subagents.** The Index (Phase 10) rates fresh-session token risk medium and does not recommend subagents.

**Gaps that matter for Step 4.**
- **The video outcome is undefined.** Main :91 sets a target that the module's DCG and LN modes are recorded to miss (`AUDIT-FIX-69`, P2).
- **The `Faz10.2` test build can absorb `Faz10.4` tree edits.** Nothing gates the build to a `setmode.sh`-only diff (`AUDIT-FIX-70`, P2).
- **The tile surface and root grant stay open.** `Faz10.2` leaves both open while unchanged v2.2 is installed (`AUDIT-FIX-78`, P2).
- **Unowned text.**
  - `recovery-runbook.md:113` cites shifted lines (`AUDIT-FIX-73`).
  - The orphaned `ic_camera.xml` (`AUDIT-FIX-75`).
  - KernelSU strings at `action.sh:8`, `:70`, `:148`, manifest :7, :48 and `index.html:196` (`AUDIT-FIX-76`).
  - The `release-checklist.md` labels :135, :148 and :176 (`AUDIT-FIX-77`).
- **Wording.**
  - The PRB3 outcome at `Faz10.1:162` (`AUDIT-FIX-74`).
  - The ambiguous `VAL-104-SURFACE` file set (`AUDIT-FIX-79`).
  - The stale "`DEC-33` row written later" sentences (`AUDIT-FIX-66`).
  - The `smoke.sh` owner named in `Faz10.3` (`AUDIT-FIX-68`).

**Acceptance criteria and validation.** The criteria are verifiable. Every plan uses smoke brackets with byte comparison, md5 equality and count-only reads, and names a `VAL-10x-*` ID for each check. The validation approach is realistic except at three points:
- the video criterion (`AUDIT-FIX-69`);
- the identity scan, which the four consumer plans reuse without a specified file-argument entry point (`AUDIT-FIX-86`, P2);
- the module log excerpt, which `Faz10.2` captures without a command or a filter (`AUDIT-FIX-85`).

**Preservation of the main plan.** The five plans stay inside Main Phase 10's bullets (:284-288). Main itself names `Faz10.2` as a co-owner of the AGC measurement, which `Faz10.2` §5 excludes (`AUDIT-FIX-72`).

**COMPLETE phases (1 to 9).** These plans are history that Step 4 does not re-run. cov-b, cov-c and cov-d rate the content strong and measurable. Residues that mislead only a re-reader:
- `AUDIT-FIX-91` (`Faz3.7` stamp);
- `AUDIT-FIX-94` and `-95` (accepted);
- `AUDIT-FIX-33` (accepted, restated per `AUDIT-FIX-90`);
- `AUDIT-FIX-108` (`Faz4.3` and `Faz4.4` quotations);
- `AUDIT-FIX-105` (`Faz9.2:54`).

None of them changes a queue row.

**Verdict.** The plans are not generic. The Phase 10 set is suitable for Step 4 decomposition once the three P2 gaps on the `Faz10.2` device window and the `Faz10.4` approval list (`AUDIT-FIX-80`) are closed before those plans reach the phone.

## 9. Scope Drift and Architectural Consistency Analysis

**No phase-meaning drift.**
- The five Phase 10 plans carry `DEC-28` (AOSPA as history), `DEC-32` (adaptation) and `DEC-33` (HAL layer off). `Faz10.2` adds an engine refusal for `50mp`, and `Faz10.4` removes `50mp` from the UI.
- `DEC-14`, the wide RAW table and the `50mp`-versus-DCG/LN exclusion are restated in every Phase 10 plan.
- No Phase 1-9 sub-plan contradicts `DEC-28`, `DEC-32` or `DEC-33`. None revives the ROM build or treats AOSPA Android 15 or 16 evidence as HyperOS 4 fact.
- The bounded additions are traceable, and each has a single owner: the `py -3` fix to `build.sh` (10.4), the 10.3 document corrections, and 10.2's `%TEMP%` test build.

**Main-Planing.md (Step 1 text, P3, open).**
- :15 claims present-tense maturity without an AOSPA label (`AUDIT-FIX-58`).
- Six stale present-tense statements: :21, :25, :63, :81, :87 and :316 (R1) (`AUDIT-FIX-59`).
- :282 dates SukiSU-Ultra to 2026-11-13 (`AUDIT-FIX-60`).
- :367 calls the entry evidence "the only record" (`AUDIT-FIX-61`).
- :178 and :349 name `Faz10.2` as an AGC measurer (`AUDIT-FIX-72`).
- The Phase 4 slice contradicts its end state at :202 (`AUDIT-FIX-107`).

**Support artifacts (P3 unless noted).**
- **`Project-Comprehension.md`.** `EV-20` keeps a present-tense Hetzner claim marked `confirmed` (`AUDIT-FIX-62`). Eight lines lack `DEC-28` notes, plus :95 (`AUDIT-FIX-98`). `AUDIT-FIX-37` (open): the file has 0 hits for `IMPL-52`, `-53` and `-54`. It goes with the S3-06 edit.
- **`Project-Ontology.md`.** Six lines are stale: :8, :19, :117, :391, :447 and :448 (`AUDIT-FIX-99`). `AUDIT-FIX-22` (P2, open) goes with that edit (section 11).
- **`docs/reverse-engineering-toolchain.md`.** §7 still treats Phase 7 as live (:213, :232-233). The HAL step at :140-142 compares against the AOSPA stock md5 (`AUDIT-FIX-100`).

**Ledger continuity.**
- The `DEC-29` to `DEC-32` "Raised by" cells use the user-initiated form for K-numbered questions (`AUDIT-FIX-65`).
- The `Faz6.2` row contradicts itself (:101, `AUDIT-FIX-97`).
- `FIND-2.3-03` is routed to the closed `Faz5.3` (:651, `AUDIT-FIX-103`).
- The `Faz7.1` and `Faz8.2` next actions predate `DEC-28` (:102, :106, `AUDIT-FIX-109`).
- The run-21 line shift is settled by the numbering statement in section 2 (`AUDIT-FIX-96`, resolved).
- Rows :69-115 otherwise match the Index and the sub-plans.

**Ownership.**
- `scripts/smoke.sh` is attributed to `Faz10.2`, but `Faz2.1` owns it (`AUDIT-FIX-68`).
- `recovery-runbook.md:113` has no owner (`AUDIT-FIX-73`, proposed owner `Faz10.5`).
- Six KernelSU string sites have no owner (`AUDIT-FIX-76`).
- No plan owns the `.gitignore` rule for `camera.qcom.so` (`AUDIT-FIX-82`).

**Plan-history gaps that could confuse replanning.**
- Seven retired files and `Faz4.6` carry no in-file note (`AUDIT-FIX-104`).
- `Faz4.3` and `Faz4.4` quote superseded Main text (`AUDIT-FIX-108`).
- `Faz9.2:54` depends on `Faz7.2` (`AUDIT-FIX-105`).

**Eleventh-audit items checked against the tree.**
- `AUDIT-FIX-41`: resolved. Main :348 records the measured configuration, with values withheld here, under `DEC-21`.
- `AUDIT-FIX-42`: resolved, met by retirement. `DEC-28` mooted the reword, and run 21 replaced each target with a dated note (:26, :71, :363, :365).
- `AUDIT-FIX-57`: resolved for its main portion. Main has dated notes at :87, :234 and :335. `CQ-13` (Comprehension :25) and Ontology invariant 11 (:429) carry `DEC-28`. The residue is carried as `AUDIT-FIX-62` and `-100`.
- `AUDIT-FIX-52`, `-53` and `-54`: resolved, confirmed. A historical note added by `03b0898` shifted the cited lines by +8. They are now `docs/build-environment.md:143-146` (`-52`), `:195-198` (`-53`), and `:481-487`, `:531` and `:562-564` (`-54`).
- `AUDIT-FIX-55` and `-56`: not_applicable. `Faz7.2` is SUPERSEDED, and `DEC-28` moots `DEC-25`.

## 10. Readiness Realism

**No overclaim in the Phase 10 plans (rdy-a, `AUDIT12_FINDINGS.md:155`).**
- **Docs versus implementation.** All five ledger rows are `planned`, and nothing is implemented. The probe, both notes files and the cleanup script are `proposed`.
- **Local versus live.** Each §9 separates the two. For example, the 10.3 fixture is local, while the backup, write and restore are live.
- **Inferences are labelled.** These include the idle-provider wake-up, KernelSU staging, `--es id` and the metamodule `system/` overlay.
- **Smoke versus production.** `Faz10.5` builds `dist/` only after the user's install bracket, and requires equal md5 (`F10.5-12`).
- **Pilot versus production.** The HAL constants stay locked (`Faz10.2` §5), and `50mp` is refused before the mode write. No AOSPA result is treated as HyperOS 4 evidence.

**Realism risk.** The AOSPA video limitation makes Main :91 and `Faz10.2:114` likely to fail, with no defined outcome (`AUDIT-FIX-69`, P2). Other overstatements:
- an identity scan that four plans reuse but none specifies as a file check (`AUDIT-FIX-86`, P2);
- a `VAL-101-IDENTITY` mitigation that cannot detect package names (`AUDIT-FIX-88`).

**Master plan and support documents.**
- Main :15 states "is functionally proven" in the present tense without its AOSPA scope (`AUDIT-FIX-58`).
- Main :63 and :81 describe v2.1 states the record has passed (`AUDIT-FIX-59`).
- Comprehension :141 still calls 50 MP "the active frontier", which `DEC-33` contradicts (`AUDIT-FIX-98`).

These are history and scope labels, not readiness claims on queued work.

**Phases 1 to 9.**
- **COMPLETE plans** keep their AOSPA-era claims as dated history. PAT4's overclaim pattern (`PAT4-R1`) found 6 hits, all not_applicable (4 property wording, 1 negation, 1 SUPERSEDED). Its placeholder pattern (`PAT4-R2`) found none.
- **`Faz4.6`** is honestly `implemented` with its live half unfinished, so it is DEFERRED, not COMPLETE.
- **SUPERSEDED plans** are out of the queue and are not presented as runnable.

**Vibecoding.** No plan uses "vibecoding" for broad strategy. The Phase 10 plans give small verified slices, each with its fastest signal and named validation evidence.

## 11. Security and Governance Findings

**Sources.** sec-a run 1 (`AUDIT12_FINDINGS.md:159`, partial) and run 2 (`:169`, complete), both on the five Phase 10 plans. PAT4 covers the 42 sub-plans of Phases 1 to 9 (`:424-509`). No finding is P0 or P1.

- **Secret safety: clean, with one wording error.**
  - No token, password, server address or identity value appears in the five plans.
  - The only credential, `tile-app/debug.keystore`, stays untracked (`.gitignore:19-21`) and outside the archive (`build-release.py` A1). Plans record the certificate SHA-256 and key path, never the password.
  - `Faz10.4:212` and `Faz10.5:246` say the debug-key password is written nowhere. `tile-app/build.sh:37` tracks a documented non-secret default (`AUDIT-FIX-83`).
  - PAT4 found no secret assignment (`PAT4-S5`: 0) and no valued identity key (`PAT4-S6`: 0).
- **Identity and preference values.**
  - `Faz10.1` defines a fail-closed three-class identity scan with synthetic fixtures. The consumer plans have no file-mode entry point for it (`AUDIT-FIX-86`, P2).
  - The `Faz10.2` module log excerpt has no filtered command and no scan (`AUDIT-FIX-85`).
  - Main :293 and :348 still write AGC preference values in plan text (`AUDIT-FIX-81`).
  - `Faz10.3:70` copies a derived preference value while stating that it copies none (`AUDIT-FIX-89`). No value is reproduced here.
- **Command execution safety.**
  - Every direct `adb` call is pinned to the device serial. `smoke.sh` is pinned through `ANDROID_SERIAL`, with a serial-header check before commit.
  - The PRB table is frozen, and the orchestrator confirmed that PRB1 to PRB10 only list, query or read (`ORCHESTRATION_PLAN.md:640-649`).
  - The new `WebUiActivity` root command is a compile-time constant. It reads no Intent data and accepts only a quoted `com.sukisu.ultra/` component. Because the activity stays exported, any app can trigger that constant launch; this is accepted as low impact.
  - `action.sh apply` checks the mode against an allowlist.
  - PAT4: all 17 `PAT4-S1` hits (`adb` without a serial) are prose or SUPERSEDED.
- **Approval gates and external mutation.**
  - Install, reboot, capture, grant and switch actions are the user's in all plans. `Faz10.3` covers its write and restore, and `Faz10.5` covers its push and `lang` restore.
  - `Faz10.4` leaves four device writes outside `VAL-104-MANUAL` and the §10 approvals: the root tile-list redirect, the test-zip push, the `sysui_qs_tiles` restore and a root cleanup after the closing snapshot (`AUDIT-FIX-80`, P2).
  - The v2.2 first boot installs the tiles and grants the overlay appop undisclosed. `Faz10.2` leaves tile taps and the root grant open (`AUDIT-FIX-78`, P2).
  - `Faz10.3` lacks the one-device-window rule (`AUDIT-FIX-71`).
- **Destructive operations.**
  - The AGC cleanup is backup-first, with a drift check, content verification and a verified restore. There is no `sed -i` and no `.agc` import; PAT4's 12 `PAT4-S3` hits all negate or replace that pattern.
  - The host copy of the AGC backup has no named path or retention rule (`AUDIT-FIX-84`).
  - `F10.5-06` overwrites the only good, untracked tile APK before the signer check (`AUDIT-FIX-87`).
  - PAT4's 3 destructive-command hits (`PAT4-S2`) are all in SUPERSEDED files.
- **Path and artifact integrity.**
  - Temp builds go to `%TEMP%`, release md5 must equal installed md5, and `git status` is checked. No `*.apk`, `*.zip`, keystore or blob enters the tree.
  - `camera.qcom.so` has no `.gitignore` rule and no owner. It relies on discipline; no Phase 10 step pulls the HAL to the host (`AUDIT-FIX-82`).
- **Least privilege.** The root command of the new WebUI path is a constant, and allowlist and tile-list reads are counts only. No server credential exists any more, because no server is rented (`DEC-28`).
- **Review, CI and merge boundaries.** No plan pushes to git or rewrites history (`PAT4-S4`: 0). Commits go through the orchestrator. Reviewers and drafts are read-only.
- **Cloud and local boundary.** Under `DEC-28` there is no rented server and no remote build. All work runs on the host and the user's phone. PAT4's retired-target pattern (`PAT4-R3`, 20 hits) is history or SUPERSEDED only.
- **SELinux and permissions.** The one `PAT4-S7` hit sets a directory context at the end of a procedure; it loosens nothing. The HAL constants stay untouched (`DEC-33`).
- **Ledger and ontology assumptions.** `AUDIT-FIX-22` (P2, open): `Planner-docs/Project-Ontology.md` holds 7 control bytes below 0x20, 2 of them NUL, on lines 313-318 (NUL at :313 and :316). These are the same offsets the tenth audit recorded, and run 21's edit preserved them. The Ontology edit for S3-07 (`AUDIT-FIX-99`) owns it and must be byte-preserving and diffed.

**PAT4 (Phases 1 to 9).** Counts only; no line text was printed or stored. Every count equals the `W4O2P01` calibration.

| Pattern | Checks for | Calibration | Hits | Files | Groups | Verdict groups |
|---|---|---|---|---|---|---|
| PAT4-S1 | `adb` without a serial | 17 | 17 | 11 | 11 | PROSE 8, SUP 3 |
| PAT4-S2 | destructive command | 3 | 3 | 2 | 2 | SUP 2 |
| PAT4-S3 | AGC preference write or `.agc` import | 12 | 12 | 4 | 4 | NEG 4 |
| PAT4-S4 | history rewrite or broad push | 0 | 0 | 0 | 0 | none |
| PAT4-S5 | secret assignment | 0 | 0 | 0 | 0 | none |
| PAT4-S6 | valued identity key | 0 | 0 | 0 | 0 | none |
| PAT4-S7 | SELinux or permission loosening | 1 | 1 | 1 | 1 | LABEL 1 |
| PAT4-S8 | download piped to a shell | 0 | 0 | 0 | 0 | none |
| PAT4-R1 | overclaim | 6 | 6 | 6 | 6 | PROP 4, NEG 1, SUP 1 |
| PAT4-R2 | placeholder | 0 | 0 | 0 | 0 | none |
| PAT4-R3 | retired ROM or rented-server target | 20 | 20 | 3 | 3 | HIST 2, SUP 1 |
| PAT4-R4 | Android 16 | 81 | 81 | 10 | 10 | HIST 4, SUP 5, finding 1 (`AUDIT-FIX-105`) |
| PAT4-R5 | KernelSU or Magisk name | 24 | 24 | 13 | 13 | HIST 9, SUP 3, KSU 1 |
| PAT4-R6 | reopening 50 MP | 0 | 0 | 0 | 0 | none |
| Total | all patterns | 164 | 164 | - | 50 | 1 finding group (1 hit), 49 not_applicable groups (163 hits) |

**Verdict codes.**
- `SUP`: the file is SUPERSEDED and out of the queue.
- `HIST`: a COMPLETE plan that records the AOSPA-era state.
- `PROSE`: the hit names a tool or path in prose, not as a command.
- `NEG`: the line negates or replaces the pattern.
- `PROP`: the word describes a property or goal.
- `KSU`: KernelSU independence as a design property.
- `LABEL`: setting a directory's SELinux context.

S5 and S6 have no hit, so there is no P0 candidate. The single finding group merged into `AUDIT-FIX-105` (P3, open).

## 12. Step 4 Readiness Assessment

**Conventions.** Dependency state follows the previous audits:

- `independent` means no upstream dependency.
- `satisfied` means every upstream dependency is complete in the repository, or is produced by an earlier row of this queue.
- Terminal rows keep the earlier conventions: COMPLETE rows are `satisfied`, SUPERSEDED rows are `independent`, and the DEFERRED row is `blocked`, because the item it waited on is retired.

Rows appear in the order of `Planner-docs/Sub-Planing-Index.md` section 3 (lines 73-172), which is also the queue order for the five queued rows. Ledger lines are cited by `def2685` numbering, which is identical at HEAD. Finding IDs list only active findings (`open` or `accepted`) whose Affected Files name the sub-plan, plus the row assignments that `AUDIT12_FINDINGS.md` makes explicitly.

**Counts, measured from the ledger matrix (`Planner-docs/Planing-Ledger.md` section 4, rows :69-:115).** 47 rows: 34 `verified`, 7 `superseded`, 1 `implemented` (`Faz4.6`, :95) and 5 `planned` (`Faz10.1`-`10.5`, :111-:115). That gives 34 COMPLETE, 7 SUPERSEDED, 1 DEFERRED and 5 READY_WITH_WARNINGS rows, with 0 READY, 0 NEEDS_REPAIR and 0 BLOCKED.

**What changed since the eleventh audit.** Planning run 21 (`DEC-28`) retired the ROM track: `Faz6.1`, `Faz7.2`, `Faz7.3`, `Faz8.1` and `Faz8.3` are now SUPERSEDED, so the eleventh audit's four queued rows leave the queue. The five Phase 10 rows (`DEC-32`) are new and form the whole queue. Under decision 6, the `Faz4.3` row no longer carries `AUDIT-FIX-22` and the `Faz9.2` row no longer carries `AUDIT-FIX-50` (`AUDIT12_FINDINGS.md` :295); `-50`'s document half moves to the `Faz10.5` row (`AUDIT-FIX-77`).

**The `Faz3.8` reason is corrected (`AUDIT-FIX-90`).** The plan text names three fields, its section 7 plans four, and five were delivered with the front key; the row stays COMPLETE.

| Sub-Plan Path | Status | Finding IDs | Dependency State | Reason | Required Repair |
|---|---|---|---|---|---|
| Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md | COMPLETE | none | satisfied | `IMPL-01`, ledger :69 `verified`; `DEC-01` answered. | none |
| Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md | COMPLETE | none | satisfied | `IMPL-02`, ledger :70 `verified`; `DEC-10` answered. | none |
| Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | COMPLETE | AUDIT-FIX-25 | satisfied | `IMPL-06`, ledger :71 `verified`. Line 9's forward reference to the superseded `Faz4.1` is accepted history (`AUDIT-FIX-25`). | none |
| Planner-docs/Faz-1-Plans/Faz1.4-toolchain-procedure-record.md | COMPLETE | none | satisfied | `IMPL-07`, ledger :72 `verified`. Its WSL2 sentence is history. | none |
| Planner-docs/Faz-1-Plans/Faz1.5-static-safety-probes.md | COMPLETE | none | satisfied | `IMPL-05`, ledger :73 `verified`. | none |
| Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md | COMPLETE | none | satisfied | `IMPL-08`, ledger :74 `verified`. | none |
| Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md | COMPLETE | none | satisfied | `IMPL-04`, ledger :75 `verified`; extended by `IMPL-55` and `IMPL-56`, repaired by `IMPL-80`. Phase 10 reuses `scripts/smoke.sh` unchanged. | none |
| Planner-docs/Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md | COMPLETE | none | satisfied | `IMPL-09` to `IMPL-12`, ledger :76 `verified`. | none |
| Planner-docs/Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md | COMPLETE | none | satisfied | `IMPL-13`, ledger :77 `verified`. | none |
| Planner-docs/Faz-2-Plans/Faz2.4-tiles-hide-disposition.md | COMPLETE | none | satisfied | `IMPL-71`, `IMPL-75`, ledger :78 `verified`; `DEC-02` answered. | none |
| Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md | COMPLETE | AUDIT-FIX-94 | satisfied | `IMPL-16`, ledger :79 `verified` at 0/12 trap keys. The plan's "ten" keys (:68, :91, :92, :156) is accepted history (`AUDIT-FIX-94`). | none |
| Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | COMPLETE | none | satisfied | `IMPL-18`, ledger :80 `verified`. | none |
| Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md | COMPLETE | none | satisfied | `IMPL-20`, ledger :81 `verified`. | none |
| Planner-docs/Faz-3-Plans/Faz3.4-consumer-compatibility-check.md | COMPLETE | none | satisfied | `IMPL-21`, `IMPL-22`, ledger :82 `verified`. | none |
| Planner-docs/Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md | COMPLETE | none | satisfied | `IMPL-23`, ledger :83 `verified`. | none |
| Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md | COMPLETE | none | satisfied | `IMPL-24`, ledger :84 `verified`. | none |
| Planner-docs/Faz-3-Plans/Faz3.7-agc-photo-size-pin.md | COMPLETE | AUDIT-FIX-91 | satisfied | `IMPL-52`, `IMPL-53`, `IMPL-54`, ledger :85 `verified`; `DEC-18`. The `<UTC>` file-name claim at :71 and :131 is wrong (the stamps are local time), a P3 history residue (`AUDIT-FIX-91`). | none |
| Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md | COMPLETE | AUDIT-FIX-33 | satisfied | `IMPL-55`, `IMPL-56`, ledger :86 `verified`. The plan text names three fields (Faz3.8 :95, :120, :155, :163; Index :107), its section 7 plans four, and five were delivered with the front key; the residue is accepted (`AUDIT-FIX-33`, restated per `AUDIT-FIX-90`). | none; the plan file needs no repair. |
| Planner-docs/Faz-3-Plans/Faz3.9-coexistence-bracket.md | COMPLETE | none | satisfied | `IMPL-57`, `IMPL-58`, `IMPL-83`, ledger :87 `verified`; its evidence also cites `IMPL-85`. | none |
| Planner-docs/Faz-3-Plans/Faz3.10-pin-stickiness-matrix.md | COMPLETE | AUDIT-FIX-95 | satisfied | `IMPL-60`, `IMPL-61`, ledger :88 `verified`. The section 9 wording of the negative-control stimulus at :140 is accepted history (`AUDIT-FIX-95`). | none |
| Planner-docs/Faz-3-Plans/Faz3.11-phase-closure-and-configuration-record.md | COMPLETE | none | satisfied | `IMPL-62`, `IMPL-63`, `IMPL-89`, ledger :89 `verified`; Phase 3 closed by `DEC-21` on AOSPA Android 15 only. | none |
| Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | SUPERSEDED | AUDIT-FIX-104 | independent | Ledger :90 `superseded` 2026-09-03 by `DEC-14`; Index :122. The file has no in-file supersession note (`AUDIT-FIX-104`). | none. Do not revive it. |
| Planner-docs/Faz-4-Plans/Faz4.5-active-array-raise.md | COMPLETE | none | satisfied | `IMPL-27` to `IMPL-30`, ledger :94 `verified`. | none |
| Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md | DEFERRED | AUDIT-FIX-104 | blocked | **Not queued.** Ledger :95 `implemented`, host-side half complete; `F4.6-07` was gated on the superseded `Faz4.1` (Index :124), and `DEC-19` keeps `FIND-3.5-01` and `FIND-4.5-02` as knowledge. | none. Completing it would need a new user decision and a new sub-plan. |
| Planner-docs/Faz-4-Plans/Faz4.7-ultra-high-resolution-sensor-mode.md | SUPERSEDED | AUDIT-FIX-104 | independent | Ledger :96 `superseded` 2026-09-03 by `DEC-14`; Index :125. No in-file supersession note (`AUDIT-FIX-104`). | none. Do not revive it as project work. |
| Planner-docs/Faz-4-Plans/Faz4.2-duration-rows.md | COMPLETE | none | satisfied | `IMPL-64`, ledger :91 `verified`; closed by the user's ruling with the gap recorded. | none |
| Planner-docs/Faz-4-Plans/Faz4.3-patch-table-consolidation.md | COMPLETE | AUDIT-FIX-108 | satisfied | `IMPL-65`, `IMPL-66`, ledger :92 `verified`. Its "amended Phase 4" quotation is stale (`AUDIT-FIX-108`). `AUDIT-FIX-22` leaves this row: it goes with the Ontology edit (`AUDIT-FIX-99`, decision 6). | none |
| Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | COMPLETE | AUDIT-FIX-108 | satisfied | `IMPL-67`, `IMPL-68`, `IMPL-70`, ledger :93 `verified`. Same stale quotation as `Faz4.3` (`AUDIT-FIX-108`). | none |
| Planner-docs/Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md | COMPLETE | none | satisfied | `IMPL-14`, ledger :97 `verified`. | none |
| Planner-docs/Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md | COMPLETE | none | satisfied | `IMPL-15`, ledger :98 `verified`. | none |
| Planner-docs/Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md | COMPLETE | none | satisfied | `IMPL-17`, ledger :99 `verified`. | none |
| Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md | SUPERSEDED | AUDIT-FIX-104 | independent | Ledger :100 `superseded` 2026-11-16 by `DEC-28` (Superseded By `SNAP-2026-11-15-MAIN`); Index :142. The `IMPL-03` edit stands and its effect is never reported `verified`. Replaces the eleventh audit's COMPLETE row. | none. Do not revive it. |
| Planner-docs/Faz-6-Plans/Faz6.2-aon-module-disposition.md | COMPLETE | AUDIT-FIX-97 | satisfied | `IMPL-72`, `IMPL-75`, ledger :101 `verified`; `DEC-04`. The ledger row's Next Action still names the retired Phase 7 `VAL-BUILD` (`AUDIT-FIX-97`, a ledger repair). | none |
| Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md | COMPLETE | none | satisfied | `IMPL-91`, ledger :102 `verified`; history under `DEC-28`. The ledger row's stale Next Action is a ledger finding (`AUDIT-FIX-109`). | none |
| Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | SUPERSEDED | AUDIT-FIX-104 | independent | Ledger :103 `superseded` 2026-11-16 by `DEC-28`; Index :149. `AUDIT-FIX-55` and `-56` are `not_applicable`. No in-file supersession note (`AUDIT-FIX-104`). | none. Do not revive it. |
| Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | SUPERSEDED | AUDIT-FIX-104 | independent | Ledger :104 `superseded` 2026-11-16 by `DEC-28`; Index :150. `AUDIT-FIX-37` moves to the Comprehension edit (`AUDIT-FIX-98`, decision 6). | none. Do not revive it. |
| Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md | SUPERSEDED | AUDIT-FIX-104 | independent | Ledger :105 `superseded` 2026-11-16 by `DEC-28`; Index :155. The static half stands as `IMPL-92`; `AUDIT-FIX-22` moves to the Ontology edit (`AUDIT-FIX-99`). | none. Do not revive it. |
| Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md | COMPLETE | none | satisfied | `IMPL-93`, ledger :106 `verified`; history under `DEC-28`. The ledger row's `DEC-08` next action is a ledger finding (`AUDIT-FIX-109`). | none |
| Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md | SUPERSEDED | AUDIT-FIX-104 | independent | Ledger :107 `superseded` 2026-11-16 by `DEC-28`; Index :157. `AUDIT-FIX-50`'s document half moves to `Faz10.5` `F10.5-12` (`AUDIT-FIX-77`). | none. Do not revive it. |
| Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | COMPLETE | none | satisfied | `IMPL-76`, `IMPL-81`, ledger :108 `verified`. | none |
| Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | COMPLETE | AUDIT-FIX-105 | satisfied | `IMPL-19`, `IMPL-78` to `IMPL-89`, ledger :109 `verified`; `DEC-23`. Line 54 points to a check in the superseded `Faz7.2` (`AUDIT-FIX-105`). `AUDIT-FIX-50` leaves this row (decision 6). | none |
| Planner-docs/Faz-9-Plans/Faz9.3-documentation-consolidation.md | COMPLETE | none | satisfied | `IMPL-77`, `IMPL-78`, `IMPL-81`, ledger :110 `verified`. | none |
| Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md | READY_WITH_WARNINGS | AUDIT-FIX-74, AUDIT-FIX-66, AUDIT-FIX-86 | independent | **Queue head.** Read-only survey with a frozen PRB table, a pinned serial, an identity scan before any read, and no device write (ledger :111 `planned`). | :162: limit the other-manager outcome to stop, or to a recorded skip of PRB3. Also the section 13 actions of `AUDIT-FIX-66` and `-86`. |
| Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md | READY_WITH_WARNINGS | AUDIT-FIX-69, AUDIT-FIX-70, AUDIT-FIX-78, AUDIT-FIX-67, AUDIT-FIX-66, AUDIT-FIX-85, AUDIT-FIX-86 | satisfied | Faz10.1 is an earlier row. The unchanged v2.2 boot comes first, then the setmode.sh retarget and the `50mp` refusal; the HAL lock is kept (DEC-33). Ledger :112 `planned`. | Define the video-failure outcome. Gate the F10.2-07 build to a setmode.sh-only diff. Forbid tile taps and the root grant while v2.2 is installed. Also the section 13 actions of `AUDIT-FIX-66`, `-85` and `-86`. |
| Planner-docs/Faz-10-Plans/Faz10.3-agc-trap-audit-and-guarded-cleanup.md | READY_WITH_WARNINGS | AUDIT-FIX-71, AUDIT-FIX-68, AUDIT-FIX-84, AUDIT-FIX-89, AUDIT-FIX-86 | satisfied | Faz10.1 is an earlier row. Backup-first with a drift check, a verified restore and a host fixture first; no picture-size write, no `sed -i`, no `.agc` import. Ledger :113 `planned`. | Add the single-device-window sentence to section 10. Also the section 13 actions of `AUDIT-FIX-68`, `-84`, `-89` and `-86`. |
| Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md | READY_WITH_WARNINGS | AUDIT-FIX-70, AUDIT-FIX-75, AUDIT-FIX-76, AUDIT-FIX-79, AUDIT-FIX-69, AUDIT-FIX-66, AUDIT-FIX-80, AUDIT-FIX-83, AUDIT-FIX-88, AUDIT-FIX-86 | satisfied | Faz10.1 is an earlier row; the phone half waits for F10.2-04 and a free window. Constant root command, certificate continuity, count-only reads. Ledger :114 `planned`. | Hold tree edits until the Faz10.2 test zip is built. Handle ic_camera.xml. Own the KernelSU strings. Name the VAL-104-SURFACE file list. Also the section 13 actions of `AUDIT-FIX-66`, `-80`, `-83`, `-88` and `-86`. |
| Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | READY_WITH_WARNINGS | AUDIT-FIX-69, AUDIT-FIX-73, AUDIT-FIX-76, AUDIT-FIX-77, AUDIT-FIX-50, AUDIT-FIX-66, AUDIT-FIX-82, AUDIT-FIX-83, AUDIT-FIX-87, AUDIT-FIX-86 | satisfied | Faz10.2, 10.3 and 10.4 are earlier rows. Temp build, then the user's install bracket, then the release build with equal md5. Owns `AUDIT-FIX-50`'s document half by decision 6. Ledger :115 `planned`. | Take AUDIT-FIX-50 (release-checklist :135, :148, :176) and runbook:113. Widen the F10.5-05 comment lines. Cite the Faz10.2 video result. Also the section 13 actions of `AUDIT-FIX-66`, `-82`, `-83`, `-87` and `-86`. |

**Execution queue state: READY.** Five rows are queued, all `READY_WITH_WARNINGS`, and each has dependency state `satisfied` or `independent`. Every finding they cite is P2 or P3 (`open` or `accepted`); no P0 or P1 is open, no path is unsafe, no target is missing, and no queued row is `blocked` or `unknown`.

**Queue head: `Faz10.1`, starting at `F10.1-01`** (dependency `independent`). Then `Faz10.2`, `Faz10.3` and `Faz10.4`, each after `Faz10.1`'s notes exist, with `Faz10.4`'s phone half after `F10.2-04`; `Faz10.5` runs last.

**Human stop gates are built into the queue and are not blockers:**

- Every device action and every AGC preference write needs the user's explicit approval in the session; install, reboot, capture, root grant and mode switch are the user's in all five plans (`AUDIT12_FINDINGS.md`, sec-a (r2) notes).
- Only one device window is open at a time (`AUDIT-FIX-67`, `AUDIT-FIX-71`).
- `Faz10.1`: the user confirms the attached phone and approves the read-only run (`VAL-101-MANUAL`, ledger :111).
- `Faz10.2`: the user installs and reboots, and approves each mode switch; no tile tap or root grant while v2.2 is installed (`AUDIT-FIX-78`).
- `Faz10.3`: each preference write and the restore are user-approved and bracketed; no value is written into any document.
- `Faz10.4`: its section 10 approval list, which must also name the four host-sent writes of `AUDIT-FIX-80` before they run.
- `Faz10.5`: the user's install bracket, the device push (`adb push`) and the `lang` restore.

**Not queued.** The SUPERSEDED and DEFERRED rows, like the COMPLETE rows, do not enter the Step 4 queue (`Third-Planner.md` :489).

## 13. Priority Fix List

**No P0 or P1 finding is open.** The register holds 109 findings, `AUDIT-FIX-01` to `AUDIT-FIX-109`. The table below has 65 rows: the 13 IDs of the eleventh audit's table with their new statuses, and the 52 new IDs `AUDIT-FIX-58` to `-109` from `AUDIT12_FINDINGS.md` (temp IDs mapped only through its two mapping tables).

**Fifty-five are active** (P0 0, P1 0, P2 6, P3 49):

- **P2 open (6):** `-22`, `-69`, `-70`, `-78`, `-80`, `-86`.
- **P3 open (45):** `-37`, `-50`, `-58` to `-68`, `-71` to `-77`, `-79`, `-81` to `-85`, `-87` to `-89`, `-91` to `-93`, `-97` to `-109`.
- **P3 accepted (4):** `-25`, `-33`, `-94`, `-95`.

**Changes since the eleventh audit.** Resolved this run: `-41`, `-42` (met by retirement) and `-57` (main portion; the residue is carried as `-62` and `-100`). `-52`, `-53` and `-54` stay resolved, confirmed at their corrected runbook lines. `-55` and `-56` are `not_applicable` (`Faz7.2` superseded, `DEC-28`).

`-90` and `-96` are new and are discharged by this audit's own text, so both are `resolved`. Decision 6 re-owns three carried findings: `-22` goes with the Ontology edit (`-99`), `-37` with the Comprehension edit (`-98`), and `-50`, narrowed to its document half, goes to `Faz10.5` `F10.5-12` (`-77`).

The other 44 IDs (`AUDIT-FIX-01` to `-21`, `-23`, `-24`, `-26` to `-32`, `-34` to `-36`, `-38` to `-40`, `-43` to `-49` and `-51`) were resolved or marked `not_applicable` before the tenth audit and are not re-listed row by row; no review of this audit reopened one.

| Finding ID | Severity | Status | Affected Files | Issue | Required Action |
|---|---|---|---|---|---|
| AUDIT-FIX-22 | P2 | open | Planner-docs/Project-Ontology.md | Carried. 7 control bytes below 0x20 (2 NUL, at :313 and :316) sit in the `Escape` column, offsets 42806-43113 (lines 313-318), the same as the tenth audit; run 21's edit (`3e7805e`) kept the bytes. Content search fails silently. The old writer `F8.1-10` is superseded. | Decision 6: in the byte-preserving Ontology edit that discharges `AUDIT-FIX-99` (S3-07), replace the raw bytes with the octal `printf '%b'` convention, diff the bytes, and confirm `rg -l InitializeScalerStaticCaps` lists the file. Never transcribe an escape from that column. |
| AUDIT-FIX-25 | P3 | accepted | Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | Carried, unchanged since `ff6934e`: `Faz1.3:9` says "Faz 4.1 narrows the RAW emission", but `Faz4.1` has been superseded since `DEC-14`. `Faz1.3` is COMPLETE (Ledger :71). | No repair required; accepted history, kept visible. |
| AUDIT-FIX-33 | P3 | accepted | Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md, Planner-docs/Sub-Planing-Index.md | Restated per `AUDIT-FIX-90`. The plan text names three fields (`Faz3.8` :95, :120, :155, :163; Index :107), its section 7 plans four, and five were delivered with the front key (`IMPL-55`, `IMPL-56`, Ledger :86). :120 and :155 also call `pref_48m_key` a 50 MP flag, against :62. | No repair required. `Faz3.8` stays COMPLETE and the plan file needs no edit; accepted and kept visible. Section 12's `Faz3.8` reason states the same three, four and five. |
| AUDIT-FIX-37 | P3 | open | Planner-docs/Project-Comprehension.md | Carried. `Project-Comprehension.md` cites `IMPL-52`, `-53` and `-54` zero times (search recorded in `AUDIT12_FINDINGS.md`). The old owner, `Faz7.3` `F7.3-08`, is superseded (`DEC-28`). | Decision 6: add the derivation mechanism as an evidence entry in the Comprehension edit that discharges `AUDIT-FIX-98` (S3-06). |
| AUDIT-FIX-41 | P3 | resolved | Planner-docs/Main-Planing.md | Section 8's step 5 described `pref_camera_picturesize_back_key` as an ordinary settings item instead of the measured configuration. | Resolved by run 21: Main :348 records the measured `pref_48m_key` and `pref_camera_resolution` configuration ([value withheld]), with the derived key read back and never written (`IMPL-52`), done under `DEC-21`; :349 adds the AOSPA-only note. |
| AUDIT-FIX-42 | P3 | resolved | Planner-docs/Main-Planing.md | Former Main lines 22, 61 and 288 presented the Android 16 `beryl` track, and section 9's *Do not expand yet* paragraph, as pending work. | Resolved, met by retirement: `DEC-28` mooted the `DEC-24`/`DEC-26` rewording. Run 21 put dated retirement or discharge notes at Main :26, :71, :363 and :365, so no live pending claim remains. The Index reader of that paragraph is `AUDIT-FIX-63`. |
| AUDIT-FIX-50 | P3 | open | docs/release-checklist.md, Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | Carried, narrowed to its document half; the `beryl` condition is moot (`Faz8.3` superseded, `DEC-28`). release-checklist :135 (`C-04` labelled `FIND-3.10-01`), :148 (`C-17` labelled `FIND-3.7-02`) and :176 ("DEFECTIVE via smoke.sh") remain. The old owner `F8.3-08` is gone. | Decision 6: `Faz10.5` `F10.5-12` owns it (`AUDIT-FIX-77`). In the same edit as the v2.3 record, point the :135 and :148 labels and the :176 comment at section 4's repair notes. |
| AUDIT-FIX-52 | P3 | resolved | docs/build-environment.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | Runbook section 4 said a sync failure stops the session while its table gave sync-path fixes, and `Faz7.2` gave the runbook precedence. | Resolved, confirmed: the exception (`IMPL-94`, kept by `IMPL-95`) is unchanged at docs/build-environment.md:143-146. The eleventh audit's 135-138 moved +8 when `03b0898` added the historical note. The runbook is historical (`DEC-28`). |
| AUDIT-FIX-53 | P3 | resolved | docs/build-environment.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | The base pin was first asserted on a billed server. | Resolved, confirmed: the pre-rental `AOSPA/manifest` `beryl` base-pin check is at docs/build-environment.md:195-198 (cited as 186-190 before the +8 shift from `03b0898`). |
| AUDIT-FIX-54 | P3 | resolved | docs/build-environment.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | Fail-fast lines in runbook sections 10 and 11 contradicted "recorded, not fatal". | Resolved, confirmed: `manifest-resolved.err` and continue at docs/build-environment.md:481-487, the operator rule at :531, and `retrieval.txt` "recorded, not fatal" at :562-564 (cited as 473-480, 523-526 and 556-572 before the +8 shift). |
| AUDIT-FIX-55 | P3 | not_applicable | Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | `Faz7.2` still planned the runbook section 10 symlink correction as future work, though `IMPL-94` had made it, and its section 6 (:196) described the old `$OUT/odm` test in the present tense. | Not applicable: `Faz7.2` is superseded (Ledger :103, Main :230) and the runbook is historical (docs/build-environment.md:3), so the rental-day verification and the later rewording have no subject. |
| AUDIT-FIX-56 | P3 | not_applicable | Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, Planner-docs/Planing-Ledger.md | `Faz7.2` :292 and `VAL-SYNC` :307 graded the resolved manifest against `22283d8` without `fixes.diff`, and `DEC-25` item (3) lacked the runbook section 4 sync-path exception. | Not applicable: both halves are moot. No paid session will grade `VAL-SYNC` (`Faz7.2` superseded), and `DEC-28` moots `DEC-25` (Main :232). |
| AUDIT-FIX-57 | P3 | resolved | Planner-docs/Main-Planing.md, Planner-docs/Project-Comprehension.md, Planner-docs/Project-Ontology.md, docs/reverse-engineering-toolchain.md | The retired rented-host fact (`DEC-26`) stayed live in Main, Comprehension `EV-20` and `CQ-13`, Ontology invariant 11 and docs/reverse-engineering-toolchain.md:220. | Resolved (main portion): dated notes at Main :87, :234, :335 (run 21 record :406); `CQ-13` (Comprehension :25) and invariant 11 (Ontology :429) carry `DEC-28`; toolchain :220 is under the dated note at :227-230. Residue carried as `AUDIT-FIX-62` and `AUDIT-FIX-100`. |
| AUDIT-FIX-58 | P3 | open | Planner-docs/Main-Planing.md | S3-20. Main :15 says in the present tense, with no AOSPA label, that the sensor layer is v2.1 and the 50 MP HAL layer "is functionally proven"; :10-11 make every module result AOSPA Android 15 evidence with the HAL layer off on HyperOS 4 (`DEC-33`). | At the next Step 1 amendment, put Main :15 in the past tense and label it AOSPA Android 15 (v2.1/v2.2), off on HyperOS 4 (`DEC-33`). |
| AUDIT-FIX-59 | P3 | open | Planner-docs/Main-Planing.md | S3-09. Six untouched present-tense lines contradict the record: Main :21 and :25 (no version control), :63 (v2.1, versionCode 12; current is v2.2, 13), :81 (never flashed), :87 (VCS, verification, README missing), :316 R1 never closed. :398 is undated first-run history. | At the next Step 1 amendment, add dated history notes in run 21's style to :21, :25, :63, :81 and :87; close R1 the way R4 was closed (Phase 1 `verified`, `DEC-01`/`DEC-27`); date the first-run narrative at :398. |
| AUDIT-FIX-60 | P3 | open | Planner-docs/Main-Planing.md | S3-18. Main :282 dates SukiSU-Ultra to the 2026-11-13 observation; the entry evidence (:292-293) names no root manager then, and the first SukiSU-Ultra reading is the 2026-11-15 check (:294, :10). | Split the sentence: HyperOS 4, Android 17, kernel and SELinux "observed 2026-11-13"; "rooted with SukiSU-Ultra (checked 2026-11-15)". |
| AUDIT-FIX-61 | P3 | open | Planner-docs/Main-Planing.md | S3-19. Main :367 calls section 6's Phase 10 entry evidence "the only record of the 2026-11-15 checks", but the tracked `ORCHESTRATION_PLAN.md` section 7.1 (`W3P01`-`W3P04`) records the same pass (Faz10.1:65, Faz10.3:68). | Reword to "the plan's summary of the 2026-11-15 checks (full inventory: `ORCHESTRATION_PLAN.md` section 7.1, `W3P01`-`W3P04`)". |
| AUDIT-FIX-62 | P3 | open | Planner-docs/Project-Comprehension.md | `AUDIT-FIX-57` residue (S3-15). Run 21 appended a history note to `EV-20`, but its Claim cell still asserts in the present tense a rented Hetzner Cloud server, and Confidence is still `confirmed` (Project-Comprehension.md:51). | Set `EV-20` Confidence to `contradicted` or the register's retired value, and mark the Claim cell as history ("Superseded 2026-11-13 by `DEC-28`"). Keep the appended note. |
| AUDIT-FIX-63 | P3 | open | Planner-docs/Sub-Planing-Index.md | S3-12. Index :43 still says rows 7 and 8 follow `SNAP-2026-09-10-MAIN`, that the user has begun Phase 7, and that Main section 9 names Phases 7 and 8; rows :36-37 and Main :363-365 now say otherwise, and :43 has no dated note. | Add a dated run-21 note to Index :43: rows 7 and 8 retired under `SNAP-2026-11-15-MAIN` (`DEC-28`), and the recorded ambiguity closed by Main :363-365. |
| AUDIT-FIX-64 | P3 | open | Planner-docs/Sub-Planing-Index.md | S3-13. The `EV-20` bullet at Index :66 still routes the rewrite to `Faz7.1` `F7.1-12` and says the three records describe a retired host; run 21 corrected `EV-20`, `CQ-13` and invariant 11 directly (Ledger :42). | Add a dated note: corrected by planning run 21 (`AUDIT-FIX-57`, Ledger row 21). Once `AUDIT-FIX-62` is fixed, `EV-20` is history under `DEC-28`. |
| AUDIT-FIX-65 | P3 | open | Planner-docs/Planing-Ledger.md | REV-3. The Raised by cells of `DEC-29` to `DEC-32` (Ledger :615-618) read "The user, 2026-11-13 (recorded by `IMPL-96`)", but their answers are K options that `IMPL-96` put to the user; `DEC-33` (:619) uses the put-to-the-user form. | At the next ledger edit, rewrite the four cells as "K<n>, put to the user 2026-11-13 by `IMPL-96`" (K1, K5+K6, K8, K7), and check `DEC-27`/`DEC-28` (:613-614) with them. |
| AUDIT-FIX-66 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md, Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md, Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md, Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | Four sub-plans say the `DEC-33` ledger row is written later (e.g. Faz10.1:29), and Faz10.5:212 assigns it to a future run, but the row exists (Ledger :619, written by run 21, Ledger :42). A Step 4 session could add a second `DEC-33` row. | Bounded Step 2 touch-up: reword to "`DEC-33` (Ledger section 8, recorded by planning run 21)"; drop the `DEC-33` half of Faz10.5:212 and keep only the AON decision. |
| AUDIT-FIX-67 | P3 | open | Planner-docs/Sub-Planing-Index.md | S3-16. Phase 10 order is stated three ways: amendment 4e (:287, :289) and the run 21 entry (:440) require one device window at a time and `Faz10.4`'s phone half after `F10.2-04` (PROJECT_LOG.md:715), but :165 says "in any order" and :192 "may then run side by side". | Amend :165 and :192 to match 4e: phone steps one window at a time; `Faz10.4`'s phone half only after `Faz10.2`'s unchanged-v2.2 record (`F10.2-04`). |
| AUDIT-FIX-68 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.3-agc-trap-audit-and-guarded-cleanup.md | `Faz10.3` (:66, :145) names `Faz10.2` as owner of `scripts/smoke.sh`, but `Faz10.2` lists the script as existing and not extended, supplied by `Faz2.1` (:156); no Phase 10 plan writes it. | Reword both places to "owned by `Faz2.1`; no Phase 10 plan edits it". |
| AUDIT-FIX-69 | P2 | open | Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md, Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md, Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md, Planner-docs/Main-Planing.md, ishtar-cam-modes/setmode.sh | S3-22. Main :91 and Faz10.2 :114 require 1080p60/4K60 in all nine modes, but the module records video failing in DCG/LN modes (setmode.sh:218, :226; Kullanim.txt:45-47; action.sh:164; index.html notes). Faz10.2 :94 gives no outcome after a failure. | Faz10.2: define the outcome when a patched mode fails video (a dated per-mode HyperOS 4 limitation, or stop and ask the user, since Main :91 is a Main target). Note-text owners: Faz10.2 for setmode.sh, Faz10.4 for the UI notes; F10.5-02/-11 cite the result. |
| AUDIT-FIX-70 | P2 | open | Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md, Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md | F10.2-07 builds its test zip from the whole module tree (Faz10.2:94), while Faz10.4 section 10 (:208) lets F10.4-02 to -09 edit scripts, index.html and tile sources and copy the rebuilt APK (:115). The Faz10.2 bracket could install them, and F10.4-03's update branch would never run. | F10.2-07: before the build, require the module-tree diff against v2.2 to list only setmode.sh and the `tile-app.apk` md5 to equal its v2.2 manifest entry. Otherwise Faz10.4 holds its tree edits and the APK copy until the Faz10.2 test zip is built. |
| AUDIT-FIX-71 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.3-agc-trap-audit-and-guarded-cleanup.md | Faz10.3 section 10 (:151-167) lacks the single-device-window rule that PROJECT_LOG.md:715 applies to it and that Faz10.2:158 and Faz10.4:208 state. A sibling bracket inside its backup-write window would make the pre/post diff unattributable. | Add one sentence to Faz10.3 section 10: its pre-clean to post-relaunch window opens only when no Faz10.2 or Faz10.4 window is open, and the reverse. |
| AUDIT-FIX-72 | P3 | open | Planner-docs/Main-Planing.md | S3-17. Main :178 and :349 say Faz10.2 and Faz10.3 measure the AGC state, but Faz10.2 section 5 puts AGC out of its scope; Faz10.3 is the only owner of the AGC signal. | At the next Step 1 amendment, name only `Faz10.3` at :178 and :349. |
| AUDIT-FIX-73 | P3 | open | docs/recovery-runbook.md, Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | S3-03. docs/recovery-runbook.md:113 cites `setmode.sh:253-255`, but the chown, chmod and chcon lines are at :254-256 today and Faz10.2's edits will shift them again. No Faz10 plan owns the runbook (Faz10.5:54 excludes it). | Assign the citation to `Faz10.5`, which runs last: re-locate it by content after Faz10.2 lands, update :113, and narrow Faz10.5:54 to match. |
| AUDIT-FIX-74 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md | S3-26. Faz10.1 :76 stops before PRB3, but :162 leaves "how PRB3 proceeds" to the user, while the PRB table is frozen (:109) and any other command is refused (F10.1-02). A choice to proceed against another package cannot run inside this plan. | At :76 and :162, name the only outcomes: stop, or skip PRB3 with the skip recorded. A different root manager needs a plan amendment, never an edited PRB3 string. |
| AUDIT-FIX-75 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md, ishtar-cam-modes/tile-app/res/drawable/ic_camera.xml | S3-11. Manifest :73 (the FullResTile block) is the only reference to `@drawable/ic_camera`. Faz10.4 deletes that block but excludes ic_camera.xml from editing (:56), so the drawable ships orphaned with a 50MP-tile comment (ic_camera.xml:4). | Faz10.4: delete ic_camera.xml together with FullResTile, or rewrite its comment, and drop it from the :56 exclusion. |
| AUDIT-FIX-76 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md, Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md, ishtar-cam-modes/action.sh, ishtar-cam-modes/tile-app/AndroidManifest.xml, ishtar-cam-modes/webroot/index.html | S3-24. Root-manager strings are unowned: F10.4-07 (:109) renames only action.sh:240 and service.sh:43, F10.5-05 only action.sh:7, :17 and manifest :5, :52-54. action.sh:8, :70, :148, manifest :7, :48 and the user-visible index.html:196 (shown via :270) have no owner. | Extend F10.4-07 to index.html:196 and action.sh:70 and :148. Extend F10.5-05 and its VAL-105-COMMENTS line list to action.sh:7-10 and manifest :2-8 and :47-55. |
| AUDIT-FIX-77 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md, docs/release-checklist.md | `AUDIT-FIX-50` carry. release-checklist :135, :148 and :176 still hold the stale labels and comment, while Faz10.5 limits its checklist edit to appending the section 7 record (scope :42, table :188). | Decision 6: reassign `AUDIT-FIX-50` to Faz10.5 F10.5-12. In the same edit as the v2.3 record, point the :135 and :148 labels and the :176 comment at section 4's repair notes, and update the :188 table row. |
| AUDIT-FIX-78 | P2 | open | Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md | F10.2-03 (:82) and the :175 risk freeze the Action button, WebUI and setmode.sh while unchanged v2.2 is installed, but not the QS tiles. v2.2's first boot adds four tiles, grants POST_NOTIFICATIONS and sets SYSTEM_ALERT_WINDOW (service.sh:32, action.sh:214-226); a tile tap runs the old restart. | F10.2-03 and the :175 mitigation: list these side effects so the install approval covers them; forbid tile taps and any root grant to `com.ishtar.cammodes` until F10.4-11; record the project tile count (count only) before and after. |
| AUDIT-FIX-79 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md | VAL-104-SURFACE greps "this plan's seven remaining" sources, but the section 9 table leaves eight after FullResTile.java is deleted (action.sh, service.sh, index.html, AndroidManifest.xml, strings.xml, build.sh, WebUiActivity.java, BaseTile.java). | Name the files the VAL-104-SURFACE grep covers. |
| AUDIT-FIX-80 | P2 | open | Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md | The approval gate omits four host-sent device writes: the root `sysui_qs_tiles` backup to /data/local/tmp and the test-zip push (:118), the conditional root tile-layout restore (:121), and the root `rm -f` cleanup after the closing snapshot (:124). VAL-104-MANUAL (:171) and :214 name none. | Add the push, the root backup write, the tile-list restore with its verification read, and the cleanup to VAL-104-MANUAL and the section 10 approvals, as Faz10.3 :163 and Faz10.5 :218 do. Move the cleanup before the closing snapshot or name it an approved post-bracket action. |
| AUDIT-FIX-81 | P3 | open | Planner-docs/Main-Planing.md | S3-21. The working rule (PROJECT_LOG.md:714) bars AGC preference values from plan text, exempting only unmodified smoke output, but Main :293 (the trap-preference value) and :348 (the two pin-input values) still write them. Related sub-plan instance: `AUDIT-FIX-89`. | Replace the values at Main :293 and :348 with counts or key names (e.g. "10 trap preferences set", "the `DEC-21` pin configuration"), or record in PROJECT_LOG section 5.5 an explicit exemption for those AOSPA-history lines. |
| AUDIT-FIX-82 | P3 | open | .gitignore, Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | S3-10. `.gitignore` has no `camera.qcom.so` or `*.so` rule (:44-48); build-release.py A2 (:163-172) guards only the archive, and Faz10.5:54 rules the rule out of scope, so no plan owns it. Low exposure: no Phase 10 step copies the HAL to the host. | Give the rule an owner: a one-line Step 4 housekeeping slice adding `camera.qcom.so` (optionally `/*.so`) with a reason row in `UNTRACKED-BY-DESIGN.md`, or Faz10.5's owner map. Otherwise record the gap as accepted. |
| AUDIT-FIX-83 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md, Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | Faz10.4 :212 and Faz10.5 :246 say the debug-key password is never written down, yet tile-app/build.sh:37 tracks a documented non-secret default that ships via build-release.py:82; Faz10.5 :230 and VAL-105-APK already acknowledge it. | Reword both lines: no new password value is written, the tracked default at build.sh:37 is a documented non-secret, and protection rests on the untracked, never-archived keystore (`.gitignore:19-21`, A1). |
| AUDIT-FIX-84 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.3-agc-trap-audit-and-guarded-cleanup.md | The host copy of the AGC preference backup, which holds preference values, has no named location and no retention or deletion step; the only constraint is "outside the repository" (Faz10.3 :36, :80, :188), while device temp files are cleared (:163). | Name the host path (e.g. a `tempfile` directory under `%TEMP%`); state when it is deleted (after the post-relaunch snapshot passes, or kept until the user decides after a failed restore) and that it never enters `snapshots/`. |
| AUDIT-FIX-85 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md | F10.2-04 (:85) captures "the module log lines" with no command, no device-side tag filter, no pinned `-s` and no identity scan; :131 calls security validation not applicable and VAL-101-IDENTITY covers only snapshots. Unfiltered logcat can carry identifiers (`DEC-31`, Ledger :617). | Specify a serial-pinned, device-filtered capture: `platform-tools/adb.exe -s <phone serial> logcat -d -s ishtar_cam_modes`. Run VAL-101-IDENTITY on the excerpt before it is stored or committed. |
| AUDIT-FIX-86 | P2 | open | Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md, Planner-docs/Faz-10-Plans/Faz10.2-hyperos4-sensor-layer.md, Planner-docs/Faz-10-Plans/Faz10.3-agc-trap-audit-and-guarded-cleanup.md, Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md, Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | VAL-101-IDENTITY is defined only as a stage of `scripts/hyperos4-probe.py` over its own transcripts (Faz10.1:125); Faz10.2 to 10.5 run "the same identity scan" on snapshots and notes (Faz10.2:123, Faz10.4:158, Faz10.5:173) with no entry point, fixtures or exit code. | In F10.1-01/-02 add a host-only scan mode of the probe (file argument, no adb, same three classes and fixtures, non-zero exit on a hit); name it in VAL-101-IDENTITY and cite it from the four consumer rows. |
| AUDIT-FIX-87 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.5-v23-release.md | F10.5-06 (:108) copies `tile-app/out/ishtar-cam-tiles.apk` over the untracked, non-recoverable `ishtar-cam-modes/tile-app.apk` before apksigner checks the digest, and checks the key file only after the rebuild, though build.sh:97-99 mints a key when the file is absent. | Reorder F10.5-06: test that the key file exists before running build.sh; verify badging and digest on the out APK; copy into the module tree only after both pass, as F10.4-09 does. |
| AUDIT-FIX-88 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.4-sukisu-tile-and-webui-chain.md | The risk "allowlist or tile list content leaks" (Faz10.4:232) cites VAL-101-IDENTITY, which matches only IMEI-like runs, identity keys and foreign serials (Faz10.1:80) and cannot see package names; the real controls are count-only reads and device-copy deletion. | Drop VAL-101-IDENTITY from that mitigation, or add a check that the notes and snapshots contain no `sysui_qs_tiles` value or allowlist entry. |
| AUDIT-FIX-89 | P3 | open | Planner-docs/Faz-10-Plans/Faz10.3-agc-trap-audit-and-guarded-cleanup.md | Faz10.3:70 (section 6) copies the derived rear picture-size value (`pref_camera_picturesize_back_key`, smoke `agc.photo_size.back.derived`) from the D9 probe, and the same paragraph says probe preference values are not copied; against PROJECT_LOG section 5.5. | Replace the value with "matched the documented 12 MP target" and keep the sentence that no preference value is copied. |
| AUDIT-FIX-90 | P3 | resolved | Planner-docs/Sub-Planing-Audit.md, Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md, Planner-docs/Sub-Planing-Index.md | The carried `AUDIT-FIX-33` text said `Faz3.8` was verified at four fields (eleventh audit :385, :332), but five were delivered with the front key (Ledger :86), and it listed only :120 and :163 of the three-field residue (also :95, :155; Index :107). | Discharged by the twelfth audit text: `AUDIT-FIX-33` is restated above (three named, four planned, five delivered; `IMPL-55`, `IMPL-56`, Ledger :86) and section 12's `Faz3.8` reason matches. `-33` stays accepted; the plan needs no repair. |
| AUDIT-FIX-91 | P3 | open | Planner-docs/Faz-3-Plans/Faz3.7-agc-photo-size-pin.md | S3-02. `Faz3.7` :71 and VAL-SMOKE :131 call snapshot stamps `<UTC>`, but they are local time (UTC+3): commit `3a307d2` (+0300) adds `snapshots/20260906-2356__...`, which as UTC would postdate its own commit. Readers matching `Z` stamps are 3 h off. | At the next bounded touch of `Faz3.7`, replace `<UTC>` at :71 and :131 with `<YYYYMMDD-HHMM local, UTC+3>`; otherwise keep it visible as history. No Step 4 impact: `Faz3.7` is COMPLETE. |
| AUDIT-FIX-92 | P3 | open | Planner-docs/Sub-Planing-Index.md | The Index still presents `Faz3.8` to `Faz3.11` as active: :91 says "the active sub-plans", :107-110 carry no status, and amendment 4c (:252) says the queue's first Phase 3 row is `Faz3.8`, positions 2-5 (:253-256) undischarged. Ledger :86-89 has all four `verified`. | Mark 4c positions 2-5 discharged (citing `IMPL-55/56`, `-57/58/83/85`, `-60/61`, `-62/63/89`), add `verified` to :107-110, and reword :91 as a closed generation (`DEC-21`). |
| AUDIT-FIX-93 | P3 | open | Planner-docs/Sub-Planing-Index.md | The Index Phase 3 entry (:91) lacks the `DEC-28` AOSPA-only note that Main carries (:143, :178, :184) and that run 21 added for Phases 6 to 8 (:141, :146, :153). No Phase 3 file has one, so a reader could carry Phase 3 evidence over to HyperOS 4. | Add one dated line: closed on AOSPA Android 15 only (`DEC-21`); not verified or carried over on HyperOS 4 (`DEC-28`); the 50 MP HAL layer stays off (`DEC-33`); Phase 10 measures the AGC state first. Section 3's Phase 3 note carries the same scope. |
| AUDIT-FIX-94 | P3 | accepted | Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md | `Faz3.1` lists twelve trap keys in section 6 (:53) and the ledger records 0/12 (Ledger :79), yet F3.1-01, the acceptance and the transition criteria say "ten" (:68, :91, :92, :156). Verified against all twelve, so no execution impact. | No repair required; accepted history, kept visible. If `Faz3.1` is ever touched, change "ten" to "twelve" at :68, :91, :92 and :156. |
| AUDIT-FIX-95 | P3 | accepted | Planner-docs/Faz-3-Plans/Faz3.10-pin-stickiness-matrix.md | `Faz3.10` :140 (section 9) still describes the old negative-control stimulus, "clears an application preference"; section 4 (:51) and section 8 (:119) make it a `pref_48m_key` write ([value withheld]). Same residue class as `AUDIT-FIX-31`; COMPLETE (Ledger :88). | No repair required; accepted history, kept visible. If the file is ever touched, reword :140 to say it sets `pref_48m_key` to [value withheld] and restores it. |
| AUDIT-FIX-96 | P3 | resolved | Planner-docs/Planing-Ledger.md | S3-01, in part. Ledger `:52` and `:651` moved without a note (`:52` now holds `SNAP-2026-09-04-MAIN`, `:651` the `FIND-2.3-03` row); `:19` did not move. Planning run 21 (`3e7805e`, `081790f`) caused the shift, not `IMPL-96`. | Discharged by the twelfth audit text: section 2 cites ledger lines by `def2685` numbering (identical to HEAD) and attributes the `:52` (+1) and `:651` shift to run 21. No format repair: the 6- and 8-pipe rows and blank lines (:501-512) predate both runs. |
| AUDIT-FIX-97 | P3 | open | Planner-docs/Planing-Ledger.md | S3-14. The `Faz6.2` row (Ledger :101) contradicts itself: Validation Evidence (2026-11-16, `DEC-28`) says `VAL-BUILD` will not run, but Next Action still has Phase 7 run it and asks for a `stock`-mode capture; Updated At still reads 2026-09-06. | Replace the Next Action with no next action: `VAL-BUILD` will not run (`DEC-28`), and on HyperOS 4 `ishtar-aon-fix` is `Faz10.5`'s. Set Updated At to that edit's date; keep the status `verified`. |
| AUDIT-FIX-98 | P3 | open | Planner-docs/Project-Comprehension.md | S3-06. 8 of 11 lines lack a `DEC-28` note: :9 (50 MP goal), :42 EV-11, :101 TRACE-14, :120 ARC-06 (Phase 7 verification), :141 (50 MP frontier, against `DEC-33`), :53 EV-22 and :167 H-05 (AOSPA Launcher3), :45 EV-14 (v2.1). :95 also still waits for a build. | In the edit that discharges `AUDIT-FIX-37` (decision 6), add a dated `DEC-28`/`DEC-33` note to :9, :42, :45, :53, :101, :120, :141 and :167, marking AOSPA Android 15 history and the current owner or none. Do not rewrite history; check :95 in the same edit. |
| AUDIT-FIX-99 | P3 | open | Planner-docs/Project-Ontology.md | S3-07. 6 of 16 lines are stale with no note: :8 (device runs AOSPA Android 15), :19 (built in Phase 7), :117 (AOSPA/LOS build inputs), :391 (kernel trees the Android 16 build consumes), :447 OQ-11 (AOSPA Launcher3), :448 OQ-12 (AOSPA camera-id map). | In the byte-preserving Ontology edit that also discharges `AUDIT-FIX-22` (decision 6), add dated `DEC-28`/`DEC-33` notes to those six lines, marking AOSPA or Phase 7 history with HyperOS 4 facts in `Faz10.1`'s record. Diff the bytes before and after. |
| AUDIT-FIX-100 | P3 | open | docs/reverse-engineering-toolchain.md | S3-08. Section 7 (:213 heading, :232-233) still treats the Phase 7 build toolchain as live; only :227-230 has a dated note. The HAL step at :140-142 compares against the AOSPA stock md5, which fails on HyperOS 4 (Index :294); documentation drift under `DEC-33`. | Add a dated `DEC-28` note to section 7 (:213, :232): no build toolchain exists or is planned. Add a dated note to section 4 (:128-142): the address book, offsets and `HAL_STOCK_MD5` describe the AOSPA Android 15 HAL; the HyperOS 4 HAL layer stays off (`DEC-33`). |
| AUDIT-FIX-101 | P3 | open | Planner-docs/Sub-Planing-Index.md | The Index Phase 6 block (:140) lacks the `DEC-28` note that run 21 gave Phases 7 and 8 (:146, :153), `Faz6.1` (:142) and section 4 item 12 (:188): it still plans the device-tree fix mirrored to the Android 16 tree, and `Faz6.2` (:143) has no status. Main :222-228 disagrees. | Add one dated `DEC-28` note after :140 in the style of :146: ROM target retired, `Faz6.1` superseded, `Faz6.2` stays `verified`, and `ishtar-aon-fix` on HyperOS 4 is `Faz10.5`'s. |
| AUDIT-FIX-102 | P3 | open | Planner-docs/Sub-Planing-Index.md | The `EV-20` assumption bullet (Index :66) says `F7.1-12` will rewrite `EV-20`, `CQ-13` and invariant 11 and bars planning on them until then; `F7.1-12` ran (`IMPL-91`) and run 21 corrected all three (Ledger :42). The bullet has no `DEC-28` note. | Add a dated note to the bullet: `F7.1-12` ran (`IMPL-91`), and run 21 rewrote `CQ-13`, `EV-20` and invariant 11 under `DEC-28`/`AUDIT-FIX-57`. Leave the history text. |
| AUDIT-FIX-103 | P3 | open | Planner-docs/Planing-Ledger.md | `FIND-2.3-03` (AGC's video section black in `stock`) is "RE-ROUTED to `Faz5.3`" in the Phase 3 closure table (Ledger :651), but `Faz5.3` was `verified` on 2026-08-31 (`IMPL-17`, :99), so the finding has no live owner. | Re-route `FIND-2.3-03` in a dated note: to `Faz10.3` for a HyperOS 4 re-measure, or close it as AOSPA Android 15 history. Do not edit `Faz5.3`. |
| AUDIT-FIX-104 | P3 | open | Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md, Planner-docs/Faz-4-Plans/Faz4.7-ultra-high-resolution-sensor-mode.md, Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md, Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md, Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md, Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md | None of these eight files carries a supersession note (keyword count 0); opened alone each reads as executable, and `Faz4.6` :242 hands off to `Faz4.1`. Fails safe under RS3. | Step 2 amendment: one dated banner under each H1 (status, deciding DEC, Superseded By); until then the ledger and Index are authoritative. |
| AUDIT-FIX-105 | P3 | open | Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | S3-05 and `PAT4-R4-01`. `Faz9.2:54` says Android 16 verification "has its own registered check in Faz 7.2"; `Faz7.2` is superseded (`DEC-28`), so the check never runs. Index :290 leaves it to this audit. `Faz9.2` is COMPLETE. | No repair before Step 4. At the next bounded Step 2 touch of `Faz9.2`, append to line 54 "Moot 2026-11-16 (`DEC-28`): no Android 16 build; `Faz7.2` superseded; the next release is `Faz10.5`'s v2.3 on HyperOS 4". Keep the sentence. |
| AUDIT-FIX-106 | P3 | open | Planner-docs/Sub-Planing-Index.md | Index section 3 Phase 4 still gives `Faz4.2`, `Faz4.3`, `Faz4.4` as the pending order (:118; `Faz4.2` "runs first" at :126) with no status, though the ledger has all three `verified` (Ledger :91 onward; `IMPL-64`; `-65`/`-66`; `-67`/`-68`/`-70`). | At the next Index edit, mark the three entries `verified` with their IMPL ids, and mark the :118 order paragraph "discharged 2026-09-06". |
| AUDIT-FIX-107 | P3 | open | Planner-docs/Main-Planing.md | Main Phase 4's first vibecoding slice (:202) still says to "add justified rows" for `d000b`/`d000c`, while the desired end state (:198) says the rows need no work, and the ledger closed `Faz4.2` with an empty row set. | At the next Step 1 amendment, mark the slice done: "Done 2026-09-05 (`IMPL-64`): the row set was empty on evidence; six RAW stall rows are a measured, unpatchable gap." |
| AUDIT-FIX-108 | P3 | open | Planner-docs/Faz-4-Plans/Faz4.3-patch-table-consolidation.md, Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | `Faz4.3` :5 and `Faz4.4` :17 quote "the amended Phase 4" text that run 16 (`60f0aee`, 2026-09-07) removed from Main; Main :200 now says RAW10 (37) is not among them. Both files are COMPLETE history. | No repair before Step 4. At the next bounded touch of either file, add under each quotation: "Main-Planing reworded 2026-09-07 (run 16, `FIND-4.4-01`); this quotation is the text of its time." Otherwise accept as history. |
| AUDIT-FIX-109 | P3 | open | Planner-docs/Planing-Ledger.md | Two COMPLETE ledger rows keep pre-`DEC-28` next actions: `Faz7.1` (:102) points to a rental-day transition into the superseded `Faz7.2`, and `Faz8.2` (:106) routes a commit through `DEC-08`, which `DEC-28` moots (Main :240). | At the next ledger edit, append "Moot 2026-11-16 (`DEC-28`; `DEC-08` moot): history only" to both Next Action cells; keep the status `verified`. |

**Finding status consistency.** Fifty-five findings are active: six P2 open, 45 P3 open and four P3 accepted. No P0 or P1 is open, so nothing blocks Step 4. Open or accepted P2/P3 findings require `PASS_WITH_WARNINGS`, so the result is not `PASS`. The eight `resolved` and two `not_applicable` rows could coexist with `PASS`; they are listed for traceability.

The four `accepted` findings (`-25`, `-33`, `-94`, `-95`) are risk knowingly carried forward: wording residue in COMPLETE plans that Step 4 does not re-run. They stay visible.

**Project findings versus audit findings.** Project findings (the ledger's `FIND-*` ids, kept as knowledge under `DEC-19`) are not audit findings. They are not counted above and do not gate Step 4.

**Validator behaviour, stated so it is not misread.** On this `PASS_WITH_WARNINGS` audit, `--mode step3 --strict` and `--mode step4 --strict` report one error and nothing else: `strict_warning=step4_has_nonblocking_warnings=P2:6,P3:49`. `--strict` promotes the non-blocking P2/P3 warning; **it is not a structural defect.** The gating facts are `p0_findings=0` and `p1_findings=0`, and the P counts come only from `open` and `accepted` rows.

## 14. Recommended Next Command / Prompt

**Step 4 may begin.** The status is `PASS_WITH_WARNINGS`, no P0 or P1 is open, and only P2/P3 findings remain, so the Step 4 prompt is printed. The execution queue is READY. Its head is `Faz10.1` (`Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md`, dependency `independent`), starting at `F10.1-01`.

The queue then runs `Faz10.2`, `Faz10.3` and `Faz10.4` (each `satisfied` once `Faz10.1` is done; one device window at a time) and ends with `Faz10.5`. The six P2 and 49 P3 warnings stay visible throughout. Four of the P2s (`-69`, `-70`, `-78`, `-80`) sit in `Faz10.2` and `Faz10.4`, and the prompt makes the session settle them with the user before that plan's device work.

**Before starting it:** this audit is committed locally (`Window 4 O4: merged audit and gates for the twelfth audit`), so the Step 4 session starts from a clean tree.

**Supporting actions, not preconditions:** a bounded Step 2 touch-up for the Phase 10 wording findings (`-66`, `-67`, `-68`, `-71`, `-73` to `-76`, `-79`, `-83` to `-85`, `-87` to `-89`); the next Step 1 amendment for the Main findings (`-58` to `-61`, `-72`, `-81`, `-107`); and one Index edit for `-63`, `-64`, `-92`, `-93`, `-101`, `-102` and `-106`.

```text
/claudeqb:claudeqb Read and return the exact canonical handoff from references/handoffs/run-step4.md, then execute it.

Context: the twelfth Step 3 audit (Planner-docs/Sub-Planing-Audit.md) is PASS_WITH_WARNINGS with no open P0 or P1; the execution queue is READY.
Read Planner-docs/Planing-Ledger.md section 4 and git status first.
The queue is Phase 10 only: Faz10.1, then Faz10.2, Faz10.3 and Faz10.4, then Faz10.5 (Planner-docs/Faz-10-Plans/).
Every other sub-plan is COMPLETE, SUPERSEDED (Faz4.1, Faz4.7, Faz6.1, Faz7.2, Faz7.3, Faz8.1, Faz8.3) or DEFERRED (Faz4.6). Do not open, revive or re-run any of them; the ledger and the Index are authoritative for their status (AUDIT-FIX-104).

Start with Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md, work item F10.1-01. Load only the sub-plan you are executing; never load all sub-plans at once.
Work in small verified slices: one work item, its validation command, a short ledger row, then the next. At the end of each sub-plan, stop and report before starting the next, preferably in a fresh session.

Keep the active audit findings visible (audit section 13): P2 open AUDIT-FIX-22, -69, -70, -78, -80, -86; 45 P3 open; P3 accepted -25, -33, -94, -95. They are warnings, not blockers, but never act against them:
- Faz10.1: build scripts/hyperos4-probe.py with a host-only file-scan mode (file argument, no adb, the same three identity classes and fixtures, non-zero exit on a hit) and record that invocation for VAL-101-IDENTITY (AUDIT-FIX-86).
- Faz10.1: if PRB3 does not find the expected root manager, the only outcomes are stop, or skip PRB3 with the skip recorded; never edit a PRB string (AUDIT-FIX-74). The DEC-33 ledger row already exists; never add a second one (AUDIT-FIX-66).
- Before Faz10.2 device work, settle with me the outcome of a patched mode failing video (AUDIT-FIX-69), gate the F10.2-07 build to a setmode.sh-only diff with the v2.2 tile-app.apk md5 (AUDIT-FIX-70), and keep QS tile taps and any root grant to com.ishtar.cammodes off while v2.2 is installed (AUDIT-FIX-78).
- Faz10.4: the test-zip push, the root sysui_qs_tiles backup and restore, and the device cleanup need my approval like every other device write (AUDIT-FIX-80).
- One device window at a time; Faz10.4's phone half only after F10.2-04 (AUDIT-FIX-67, -71).

Rules: every device action (install, reboot, push, root or settings write, launch, capture) and every AGC preference write needs my explicit approval in this session, after you show the exact command and its backup and restore.
Pin every adb call to the phone's serial as the sub-plan specifies. Never write an IMEI, serial or other identity value, a secret, or an AGC preference value into any file; run the identity scan before anything is stored or committed.
Do not edit a sub-plan, the Index or Main-Planing without asking me; a needed plan change goes to a bounded Step 2 amendment. No push, no commit and no history rewrite without asking me.
```

**Token and queue reminder.**

- **`Faz10.1` is the cheap entry:** a host-side probe and fixtures first, then a read-only survey with a frozen PRB table and no device write.
- **`Faz10.2` to `Faz10.4` carry the device risk.** Run them one device window at a time, each in its own session, and keep only exit status, the smoke diff and counts in context.
- **`Faz10.5` runs last**, after the user's install bracket, and owns `AUDIT-FIX-50`'s document half (`F10.5-12`).

Do not run the prompt from this audit session.

## 15. Audit Result

- **Final status: PASS_WITH_WARNINGS.**
  - **Coverage:** ten main phases, ten phase folders and 47 sub-plan files, all structurally compliant (`AUDIT12_FINDINGS.md`, cov-a section 3).
  - **Findings:** 55 active, none P0 or P1: six P2 open, 45 P3 open and four P3 accepted. 52 new this run (`-58` to `-109`; P2 5, P3 47). Resolved this run: `-41`, `-42`, `-57`, and the new `-90` and `-96`, discharged by this text. `-55` and `-56` are `not_applicable`.
  - **Validators:** `--mode step3 --strict` and `--mode step4 --strict` report only the expected `strict_warning=step4_has_nonblocking_warnings=P2:6,P3:49` described in section 13.
  - **Queue:** READY. 47 rows: 34 COMPLETE, 7 SUPERSEDED, 1 DEFERRED (`Faz4.6`) and 5 READY_WITH_WARNINGS (`Faz10.1` to `Faz10.5`), headed by `Faz10.1` (dependency `independent`).
- **Confidence: high** on the register, where every row traces to a finding, disposition or mapping row of `AUDIT12_FINDINGS.md`. Also high on the counts, the structure and the queue order (ledger section 4, Index section 3).
- **Confidence: medium** on the Phase 10 device-side assumptions that the plans label as inferences (the idle-provider wake-up, KernelSU staging, `--es id`, the metamodule `system/` overlay), which only Step 4 on the phone can confirm. **Not assessed for content:** the seven SUPERSEDED files and `Faz4.6`, which had a light read (headings and keyword counts) only.
- **Only `Planner-docs/Sub-Planing-Audit.md` was modified by this audit** within the plan set. No sub-plan, index, ledger, master plan, ontology, comprehension file, runbook or source file was written. No device command, no GitHub write and no push.
- **Unexpected modifications: none detected.** `Planner-docs/` is unchanged since `def2685` apart from this file.
- **Step 4 can safely begin** with `Planner-docs/Faz-10-Plans/Faz10.1-hyperos4-camera-stack-survey.md`. No P0 or P1 is open, and the P2/P3 warnings stay visible during implementation.
