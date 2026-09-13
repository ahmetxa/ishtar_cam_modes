# Sub-Planing Audit

> Step 3 audit — ClaudeQB. Body language: English (default contract).
> The project's user-facing documents and module interface remain Turkish and English; that convention is unchanged.
>
> **This is the ninth audit (2026-09-11).** It supersedes the eighth audit (2026-09-05). Since then, five things happened that audit never saw. Step 4 ran the whole of its queue except Phases 7 and 8 (`IMPL-55` … `IMPL-88`). Planning run 16 corrected `Main-Planing.md`. The user ruled on `DEC-01`, `DEC-16`, `DEC-21`, `DEC-23` and `DEC-24`. `IMPL-90` staged the Android 16 inputs on GitHub. And planning runs 17 and 18 re-scoped and re-planned Phases 7 and 8. **This audit exists to discharge the ledger section 7 trigger `DEC-24` fired**: run 18 wrote six Phase 7 and Phase 8 sub-plans, and its own index banner says none may enter the Step 4 queue until Step 3 has read them.
>
> **Active snapshots: `SNAP-2026-09-10-MAIN` and `SNAP-2026-09-10-SUBPLANS`. The sub-plan set is 42.**

## 1. Audit Summary

**Overall audit status: PASS_WITH_WARNINGS.**

**The six re-planned Phase 7 and Phase 8 sub-plans are sound. All six enter the Step 4 queue as `READY_WITH_WARNINGS`.** No P0 or P1 finding is open. Four new P2 findings concern two irreversible moments the plans schedule but do not fully prepare for: deleting a paid server, and flashing the user's daily phone.

**The re-plan is well grounded, and this audit checked that directly.** Every local claim in the six files that could be checked without a device was re-measured this run, and all of them hold:

- the clone logs are 86 and 32 bytes;
- `common_sm8550/` is `AOSPA/android_device_xiaomi_sm8550-common` on `vauxite`, which makes it a device tree;
- both kernel checkouts are `vauxite` at 5.15.178;
- `refs/a16_sm8550/common.mk:122-135` carries `TARGET_KERNEL_DLKM_DISABLE := false` and thirteen overrides, `CAMERA` at line 125;
- `halpatch.sh:32-34` and `customize.sh:14` carry exactly the quoted guard constants;
- `hal-fullres.patch` opens "A15 / vauxite";
- `refs/a16_ishtar` is on `beryl` at `df056613…`, carries `05efdac` and `e0ade7f` (the latter also in `device_ishtar`), has one `;SYMLINK=` entry at line 1037, and its `extract-files.py` fixups name `camera.xiaomi.so` but neither guarded file;
- `.gitignore` has no `*.img` rule;
- the `docs/aon-verification.md` step 1 command and the section 8.4 instruction are quoted verbatim.

A bounded read-only GitHub check confirmed the staged state has not drifted: `ahmetxa/android_local_manifests` HEAD is `4182695` with README status "INCOMPLETE — not buildable yet" and seven open items, `ahmetxa/android_device_xiaomi_ishtar` `beryl` is `d48816f`, and vendor commit `f92e7a9` exists on `xiaomi-8550/proprietary_vendor_xiaomi_ishtar`.

**The sequencing design is the strongest part of the re-plan.** Nothing is rented until `Faz7.1`'s transition criteria hold on the day. Nothing is flashed without a retrieved, sha256-verified package and a written return path. `Faz8.1`'s static half is pulled ahead of the rental, so the user learns whether the camera work carries over before paying for a build. A HAL re-derivation label raises a replanning input instead of scheduling disassembly. Teardown is an acceptance criterion regardless of the build outcome. Each of these is written as a gate, not as advice.

**Most important finding: `AUDIT-FIX-46` (P2) — the sensor-layer *adaptation* branch leads nowhere.**

- `Faz8.1` defines three labels. `Faz8.3`'s gate accepts "sensor carry-over **or completed adaptation**".
- No sub-plan performs an adaptation. `Faz8.1` section 5 excludes "regenerating sensor blobs", and `Faz8.3` section 5 excludes blob regeneration, any `customize.sh` edit, and rebuilding the archive.
- An adapted blob changes `EXPECT_MD5`, so it needs a new release. That contradicts `Faz8.3`'s "unchanged v2.2 archive".
- `F8.1-09` prices only carry-over and re-derivation, and index section 5 defers only the HAL re-derivation.

The gate therefore names a state the plan set cannot reach. An implementer who hits it will either stop without a routed input or improvise the adaptation.

**The other three new P2s cover the two irreversible steps:**

- **`AUDIT-FIX-43`:** `F7.2-09` defers the delete-versus-power-off question to "the provider's billing documentation, read in `Faz7.1`". No `Faz7.1` work item or acceptance criterion reads it, yet `F7.1-10`'s budget and stopping rule depend on it.
- **`AUDIT-FIX-44`:** `F7.2-08` retrieves "the flashable package" without tying the list to AOSPA's documented install method for `ishtar`. The server is deleted before `Faz7.3` learns what the install needs.
- **`AUDIT-FIX-45`:** `Faz7.3`'s return path never states whether moving Android 15 → 16, or 16 → 15, wipes `/data`. `F7.3-07`'s "comparable region unchanged" criterion assumes the AGC preferences, KernelSU and the installed modules survive a whole-system downgrade.

**Most important remediation action:** fold `AUDIT-FIX-43` and `-44` into `Faz7.1`'s runbook work, which already owns provisioning, the evidence list and teardown (`F7.1-11`). Then run one bounded Step 2 amendment for `AUDIT-FIX-45` and `-46` at any point before `Faz7.3`. Neither amendment blocks `Faz7.1`, `Faz8.1`'s static half or `Faz8.2`, which are host-only and come first in the queue.

**The carried register moved a lot, and every change was measured rather than assumed:**

- Planning run 16 resolved `AUDIT-FIX-30` and `-35`: `Main-Planing.md` lines 159 and 167 now carry the measured route.
- `AUDIT-FIX-38`, `-39` and `-40` are `not_applicable`. The sub-plans they pointed at are `verified`, and the ledger's `F3.11-08` disposition shows the implementer read what `Faz3.10` measured, which was the conditional's purpose.
- `AUDIT-FIX-33` is `accepted`: `Faz3.8` is `verified`, and its three-field residue is now history plus one index line.
- `AUDIT-FIX-37` is narrowed to `Project-Comprehension.md`. `Project-Ontology.md` now cites `IMPL-52`/`-53`/`-54` five times, and the comprehension file still cites them zero times.
- `AUDIT-FIX-22` is unchanged in substance: 7 control bytes, 2 of them NUL. Its offsets moved by 100 bytes because run 17 edited the `beryl` entry above them. It now affects three queued rows, because `F7.1-12`, `F8.1-10` and `F8.2-09` all write to that file.

**Step 2 output is usable for Step 4.** **Highest-priority next action:** Step 4 at `Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md`, starting with `F7.1-01`.

## 2. Reviewed Sources

**Files inspected.**

- `Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md`, `Faz7.2-first-aospa-build.md`, `Faz7.3-flash-boot-and-aon-verification.md`, `Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md`, `Faz8.2-kernel-lts-merge-scoping.md` and `Faz8.3-camera-modes-on-android16-build.md`. **Each was read in full, section by section**, checked against Main-Planing Phases 7 and 8, against each other, and against the repository.
- `Planner-docs/Main-Planing.md` — read in full; `git diff HEAD` read for run 17's changes; lines 22, 61, 159, 167, 277 and 288 re-measured.
- `Planner-docs/Sub-Planing-Index.md` — read in full, including amendment 4d, section 5, the coverage check and the run 18 paragraph in section 7.
- `Planner-docs/Planing-Ledger.md` — section 2 (runs 6–18), section 3, the entire section 4 matrix, sections 6, 7 and 8, the finding-disposition table, and rows `IMPL-86` … `IMPL-90`. The file's lines run to several thousand characters, so it was read through a truncating extractor. **Section 5 was navigated by row, not read end to end.**
- `Planner-docs/Project-Ontology.md` — the `beryl` entry, invariants 3, 10 and 11, a byte-level control-character scan, and `IMPL-*` occurrence counts.
- `Planner-docs/Project-Comprehension.md` — `EV-20`, `CQ-13`, `TRACE-13`, `ARC-06`, and `IMPL-*` occurrence counts.
- `Planner-docs/Autopsy.md` — section headings plus its Phase 7, Phase 8, `beryl` and WSL references.
- The previous (eighth) `Planner-docs/Sub-Planing-Audit.md` — read in full before overwriting, so finding IDs continue from `AUDIT-FIX-40` and no resolved finding is raised again.
- Repository evidence cited by the six sub-plans: `ishtar-cam-modes/halpatch.sh:32-34`, `customize.sh:14`, `blobs/hal-fullres.patch` header, `setmode.sh` `restart_camera()` and `wait_svc()`, `.gitignore`, `kernel_clone.log`, `common_clone.log`, `refs/a16_ishtar/{board-info.txt,proprietary-files.txt,extract-files.py}`, `refs/a16_sm8550/common.mk`, the git remotes, branches and HEADs of `common_sm8550`, both kernel checkouts, `refs/a16_ishtar`, `refs/a16_sm8550` and `device_ishtar`, `docs/aon-verification.md` (headings, step 1, section 8.4), `docs/release-checklist.md` (headings, capability map, section 4), `docs/recovery-runbook.md`, `docs/release-manifest.md`, and `docs/reverse-engineering-toolchain.md` section 7.

**Folders inspected.** `Planner-docs/`, all nine `Faz-<n>-Plans/` folders, `docs/`, `scripts/`, and the repository through `git`.

**Important commands run.**

- The bundled validator, through the installed plugin path, in `--mode step3-preflight --strict`, `--mode step2 --strict` and `--mode step3 --strict`. Python 3.14.7 resolves as `python`; `python3` is the Windows Store stub. The validator source was read for its audit, readiness and finding parsers.
- A Python structure checker over all 42 sub-plans. It checks the filename regex, folder/file/H1 phase agreement, the thirteen headings in order, duplicate headings, per-section body length, placeholder tokens, the Implementation Contract header and path safety, control characters, UTF-8 validity, line endings at byte level, and per-phase numbering contiguity. It also cross-references the index and the ledger against the filesystem in both directions.
- A cross-phase premise sweep of the 36 sub-plans outside Phases 7 and 8 for `WSL`, `beryl`, `Faz7.`, `Faz8.`, `Phase 7`, `Phase 8`, "second device" and the two removed filenames.
- `git log` and `git diff --stat` from `78373d5` (the commit that last touched the audit) to the working tree, to establish exactly which planner files changed since the eighth audit.
- Read-only `gh api` calls: `ahmetxa/android_local_manifests` commits and `README.md`; the `beryl` branch head of `ahmetxa/android_device_xiaomi_ishtar`; repository metadata and branches of `xiaomi-8550/proprietary_vendor_xiaomi_ishtar` and `ThankYouMario/proprietary_vendor_xiaomi_ishtar`; commit `f92e7a9`. No write, no clone, no content fetch.
- `git grep -i wsl` over tracked files outside `Planner-docs/`.

**Things not verified.**

- **The 36 sub-plans outside Phases 7 and 8 were not re-read for content this run.** `git diff --stat 78373d5` shows none has changed since the eighth audit. The ledger marks 33 of them `verified` and one `implemented` (`Faz6.1`, edit complete). Two are `superseded` and one is `DEFERRED`. All 36 were checked programmatically for structure and swept for stale Phase 7/8 premises; the earlier audits' content assessments stand.
- Whether the Android 16 guarded blobs match. That is `Faz8.1`'s measurement, and no blob was fetched.
- AOSPA's `beryl` build host requirements, its install method for `ishtar`, and the provider's billing and deletion semantics. These were deliberately not researched: they are the gaps `AUDIT-FIX-43`, `-44` and `-45` route to the owning sub-plans.
- Device state. **No `adb` command was run.**
- The measurements behind `IMPL-55` … `IMPL-90`, which were taken as reported. That is the correct boundary for an audit.

No secret value was read or recorded. `secret_findings=0` in every validator mode run.

## 3. Main Phase Coverage Analysis

| Main phase no | Main phase heading | Expected folder | Folder exists? | Sub-plan count | Coverage status | Notes |
|---|---|---|---|---|---|---|
| 1 | Workspace safety net | Planner-docs/Faz-1-Plans/ | Yes | 6 | OK | All six `verified`. Phase closed. |
| 2 | Ship and re-baseline v2.1 | Planner-docs/Faz-2-Plans/ | Yes | 4 | OK | All four `verified`; `Faz2.4` closed by `IMPL-75` (`DEC-02`). |
| 3 | AGC stable at 12.6 MP under 50 MP | Planner-docs/Faz-3-Plans/ | Yes | 11 | OK | All eleven `verified`. Phase marked successful by `DEC-21` (2026-09-10). |
| 4 | Minimal correct HAL patch | Planner-docs/Faz-4-Plans/ | Yes | 7 | OK | `Faz4.2`–`4.5` `verified`; `Faz4.1`, `Faz4.7` `superseded`; `Faz4.6` `DEFERRED` (its knowledge findings are disposed under `DEC-19`). |
| 5 | Mode-0 12-bit composition | Planner-docs/Faz-5-Plans/ | Yes | 3 | OK | All three `verified`. Phase closed. |
| 6 | AON fix upstreaming | Planner-docs/Faz-6-Plans/ | Yes | 2 | OK | `Faz6.2` `verified`; `Faz6.1` `implemented`. Its effect verification now has a named owner, `Faz7.3` `F7.3-08`. |
| 7 | Android 16 build environment | Planner-docs/Faz-7-Plans/ | Yes | 3 | OK | Re-planned by run 18. Covers the phase's three parts: pre-rental staging, the paid build and the flash/boot signal. The goal, desired end state, both acceptance signals (boots; rental time recorded) and the first slice each have an owner. |
| 8 | Camera work on Android 16 + kernel LTS | Planner-docs/Faz-8-Plans/ | Yes | 3 | WARNING | The camera carry-over path and kernel scoping are covered. **Two acceptance branches are deliberately not decomposed** — "or the patches are re-derived for them" and "kernel merge with no regressions" — and both are routed to `DEC-07`/`DEC-08` plus a ledger section 7 input. That deferral is honest and recorded in index section 5. **The warning is the third branch, sensor adaptation, which is referenced as reachable and owned by nothing** (`AUDIT-FIX-46`). |
| 9 | Release engineering | Planner-docs/Faz-9-Plans/ | Yes | 3 | OK | All three `verified`. |

Nine main phases were detected in `Main-Planing.md` section 6: nine table rows and nine `### Phase <n>` headings, confirmed by the validator's `main_phase_count=9`. There are nine phase folders, no missing phase and no extra folder. **Planning run 17 renamed Phase 8** from "beryl port + kernel LTS" to "Camera work on Android 16 + kernel LTS". The rename changes the phase's premise, not its role: the old premise read `beryl` as a second device, and run 17 corrected that against measurement (`AOSPA/manifest` carries `beryl`). The ledger records the rename as a user-approved Step 1 amendment, so it is **not** scope drift. Per-phase counts, measured this run: **6, 4, 11, 7, 3, 2, 3, 3, 3 — total 42.**

## 4. Sub-Plan File Inventory

Structure was checked programmatically on **all 42** files, and all 42 have an H1 matching `# Faz <phase>.<sub> — ` with the number agreeing with folder and filename. Content quality was assessed this run for the six Phase 7 and Phase 8 files. The other 36 carry the eighth audit's assessment and are unchanged since it.

**Planner-docs/Faz-7-Plans/** (3 files, all re-planned by run 18, ledger `planned`).

- `Faz7.1-github-input-staging.md` — H1 `# Faz 7.1 — GitHub Input Staging and Pre-Rental Readiness`. Phase match OK; structure OK. **Content: strong.** All seven manifest open items are enumerated and verified against the live README. Each item is closed with a source or deferred with a detector and fallback, and "not yet determined" is explicitly forbidden at exit. `IMPL-90`'s masked-exit defect is carried as a rule (fail-on-error, publish gated on read-back). The credential plan is read-only with revocation, and no value is ever written. The kernel tree is handed to `Faz8.2` by name. Notes: `AUDIT-FIX-43` (billing semantics not read), `AUDIT-FIX-44` (install-method artifacts not in the runbook), `AUDIT-FIX-22` (`F7.1-12` writes invariant 11 into the NUL-bearing ontology).
- `Faz7.2-first-aospa-build.md` — H1 `# Faz 7.2 — First AOSPA beryl Build on a Rented VDS`. Phase match OK; structure OK. **Content: strong.** The pre-rental gate predates renting. Any input fix must land on GitHub before the server pulls it, and that rule is an acceptance criterion. AON step 1 runs before the build. Post-build blob md5s are recorded "as facts, not conclusions". Teardown is required "whatever the build outcome". Notes: `AUDIT-FIX-43` (`F7.2-09`'s deferral points at nothing), `AUDIT-FIX-44` (retrieval list).
- `Faz7.3-flash-boot-and-aon-verification.md` — H1 `# Faz 7.3 — Flash, Boot and AON Verification on the Device`. Phase match OK; structure OK. **Content: good.** It puts the return path before the flash and a firmware go/no-go before flashing. It uses the module-absent state of a clean build for AON step 3, judged against section 8.2's strings rather than a baseline that does not exist, and requires a three-way md5 check. Notes: `AUDIT-FIX-45` (wipe consequence of a major-version flash and downgrade).

**Planner-docs/Faz-8-Plans/** (3 files, all re-planned by run 18, ledger `planned`).

- `Faz8.1-android16-camera-blob-comparison.md` — H1 `# Faz 8.1 — Android 16 Camera Blob Comparison and Carry-Over Decision`. Phase match OK; structure OK. **Content: strong.** It uses a checksum, not the firmware label. It verifies fixups at pinned commits, requires three-way agreement before the classification closes, prices the layers honestly as unequal, and turns re-derivation into a decision instead of scheduled work. Notes: `AUDIT-FIX-46` (adaptation branch), `AUDIT-FIX-47` (scratch lifecycle and the static-half boundary), `AUDIT-FIX-49` (`F8.1-04`'s attribution source is unnamed, and a ledger row contradicts `IMPL-90`), `AUDIT-FIX-22`.
- `Faz8.2-kernel-lts-merge-scoping.md` — H1 `# Faz 8.2 — Kernel LTS Merge Scoping`. Phase match OK; structure OK. **Content: strong.** It records four premise corrections, each re-measured this run and correct. It uses a no-checkout conflict estimate that must first reproduce a known merge, and keeps the out-of-tree camera-module hypothesis out of the conclusions until tested. It uses the black-preview restart test instead of the counter `IMPL-13` showed is not diagnostic. Notes: one immaterial slip, not raised as a finding — section 6 says the checkouts are ignored at ".gitignore lines 26-27 and the platform section", but `common_sm8550/` is ignored at line 28. `AUDIT-FIX-22` (`F8.2-09`).
- `Faz8.3-camera-modes-on-android16-build.md` — H1 `# Faz 8.3 — Camera Modes on the Android 16 Build`. Phase match OK; structure OK. **Content: good.** It covers only the carry-over path, installs the release as built, confirms invariant 3 before any mode switch, gives all 18 rows a result, and turns failures into findings instead of fixes made on the spot. Notes: `AUDIT-FIX-46` (gate), `AUDIT-FIX-50` (pre-`IMPL-80` detector state), `AUDIT-FIX-51` (init service name versus process name).

**All other phase folders** (`Faz-1-Plans` 6, `Faz-2-Plans` 4, `Faz-3-Plans` 11, `Faz-4-Plans` 7, `Faz-5-Plans` 3, `Faz-6-Plans` 2, `Faz-9-Plans` 3). Every file passes: filename, phase match and section structure are OK; no thin or placeholder section; Implementation Contract present with safe paths. Content status comes from the ledger: complete, superseded or deferred, as tabulated in section 12. Carried residues: `Faz1.3` (`AUDIT-FIX-25`, accepted), `Faz3.8` (`AUDIT-FIX-33`, accepted), `Faz3.10`/`Faz3.11` (`AUDIT-FIX-38`–`40`, not_applicable). The premise sweep found WSL2 sentences in `Faz1.4`, `Faz6.1` and `Faz6.2`. They are history under the snapshot those sub-plans executed against, and `Faz7.1` section 5 explicitly leaves them unedited, which is correct.

## 5. Naming and Sequencing Check

**No naming or order issues were found.**

- Folder naming: all nine match `Faz-<n>-Plans/`; no extra folder.
- Filename naming: all 42 match `Faz<phase>.<sub>-<ascii-kebab-slug>.md`, with no spaces, no non-ASCII and no duplicates. The three new slugs (`github-input-staging`, `flash-boot-and-aon-verification`, `android16-camera-blob-comparison`, plus `camera-modes-on-android16-build`) are descriptive.
- Numbering: contiguous from 1 in every phase. Run 18 removed `Faz7.1-wsl2-provisioning.md` and `Faz8.1-beryl-port-sizing.md` and replaced each at the same number, so no gap or duplicate arose. **Removing a file rather than marking it superseded departs from the project's usual practice** (`Faz4.1` and `Faz4.7` were kept). The departure is justified: a kept file would have left two sub-plans per number. It is also traceable: `git` holds both removed files, and the ledger, the index and both successors name them as removed.
- Folder/file/H1 agreement: all 42 agree.
- Order: the phase ordering matches `Main-Planing.md` section 6. Execution order within Phases 7 and 8 differs from numbering by design (`Faz8.1`'s static half before `Faz7.2`). Index amendment 4d records this as execution order rather than renumbering and cites `Faz6.1` as precedent. That is plausible and consistent with `Faz8.1` section 10, apart from the boundary noted in `AUDIT-FIX-47`.

## 6. Index Consistency Check

- **Missing references: none.** All 42 sub-plans are referenced, measured in both directions.
- **Broken references: none.** All 42 index references resolve. The ledger names the two removed files eight times (lines 39, 56, 97, 100, 513, 570, 587 and the snapshot note). Every one of them labels the file removed, or is an `IMPL-86` history row that predates the removal, so none is a live broken reference.
- **Unindexed files: none.**
- **Phase count: matches.** Nine in the index, nine in `Main-Planing.md`, nine folders. The index's Phase 8 name follows `SNAP-2026-09-10-MAIN`.
- **Coverage claims: honest on counts, wrong on one byte-level fact.** Section 6 reports 6, 4, 11, 7, 3, 2, **3**, **3**, 3 = 42, which matches this run. **But section 7's run 18 paragraph states "All six sub-plans use CRLF line endings like their siblings." Measured at byte level, all 42 sub-plans and the index are LF-only; only `Main-Planing.md`, `Planing-Ledger.md` and `Autopsy.md` are CRLF.** That is `AUDIT-FIX-48` (P3). The claim is harmless until a later session "normalises" six files to CRLF on its authority and produces a whole-file diff.
- **Execution order: plausible.** Amendment 4d's six-step order for the Android 16 front is the right shape: free host work first, then cheap decisive measurement, independent scoping in parallel, paid session, flash, then the functional test. Its "static half only (`F8.1-01` to `F8.1-05`)" disagrees in its boundary with `Faz8.1` section 10, which also counts `F8.1-08` and `F8.1-09` "on static values" (`AUDIT-FIX-47`).
- **A recorded ambiguity, judged.** Index section 2 records that `Main-Planing.md` section 9 still says "Do not expand yet. Phases 7, 8, and 9. G is blocked on host-environment work the user must perform", and decomposes both phases anyway. It gives three reasons: run 17 re-scoped them, the user began Phase 7 (`IMPL-90`), and the build-dependent halves are gated. **The judgement is correct.** That paragraph's premise, a WSL2 install the user must perform, is exactly what `DEC-24` retired, and Phase 9, named in the same sentence, is verified. The stale sentence belongs to the master plan and is `AUDIT-FIX-42`.
- **Carried residue.** Index line 106 still describes `Faz3.8` as three fields (`AUDIT-FIX-33`, now accepted: the sub-plan is `verified` at four fields per `IMPL-55`).

## 7. Required Section Structure Check

Checked programmatically on **all 42** sub-plans, not sampled.

- **Missing sections: none.** Every file carries all thirteen required `##` headings.
- **Duplicated sections: none.**
- **Wrong order: none.**
- **Empty sections: none.** The shortest section body across all 42 files is 175 characters (`Faz6.1` section 2). In the six new files, the shortest is well above that.
- **Placeholder sections: none.** No `TODO`, `TBD`, `FIXME`, `XXX` or lorem-ipsum token.
- **Title/filename/folder agreement: all 42 agree.**
- **Implementation Contract tables:** all 42 present with the required header, every path repo-relative, no absolute path, no `..` traversal. The six new tables use only `existing`, `proposed` and `modified`. Older files also use `generated`, `deferred` and `external`, which the validator's allowed set accepts. `Faz7.1` explicitly keeps the manifest repository's files out of its table because they live in a separate private repository. It forbids Step 4 from copying that repository into the workspace, which is the correct boundary.
- **Control characters and encoding: none in any sub-plan; all 42 are valid UTF-8 and LF-only.** `Project-Ontology.md` is the one planner file carrying control bytes (`AUDIT-FIX-22`).

`validate_planner_docs.py --mode step2 --strict` and `--mode step3-preflight --strict` both report `error_count=0`, `warning_count=0`, `subplan_count=42`, `index_reference_count=42`, `phase_folder_count=9`, `main_phase_count=9`, `secret_findings=0`.

## 8. Content Quality and Implementability Analysis

**The six sub-plans are specific and actionable, and they are written for this project rather than generically.** Each opens by quoting the master-plan sentence it serves. Each states which premise of its predecessor is gone and why, and the replaced premises were measured, not assumed: the clone logs, the checkout roles, the missing `hardware/xiaomi` branch. Each names the decision it routes and to whom. None contains implementation code.

**The acceptance criteria are verifiable, and several are written to fail the most likely shortcut:**

- `Faz7.1`: "none reads 'not yet determined' at the end".
- `Faz7.2`: "No input was changed on the server without the same change landing on GitHub first".
- `Faz8.1`: "no cell reads 'same firmware, assumed equal'".
- `Faz8.2`: the camera-module hypothesis "is not used as a premise before that verdict exists".
- `Faz7.3`: "Step 3 is not judged against a positive baseline, because section 8.4 establishes there is none".

These are gradeable from artifacts. Validation IDs are specific, and the proposed ones say what they read.

**Vibecoding slice quality is high.** Every sub-plan names a first slice measured in minutes where one exists: `F7.1-01` re-running `check.py` both ways; `F8.1-01`/`-02`, two files, four constants; `F8.2-05`, proving `git merge-tree` on a known merge before trusting it. Every sub-plan also names what it deliberately does not over-plan: build errors, conflict resolution, re-derivation, fixes for failing rows. Token/context risk is banded per sub-plan and reconciled against Main-Planing's `high` band for Phase 8. The re-plan observes, correctly, that the `high` describes a re-derivation this set deliberately does not decompose. Subagents are marked not recommended in all six, with reasons: sequential reads, a single stateful remote server, and a single device. For `Faz8.1` the plan explains why Main-Planing's permitted explorer is too big a tool for two files.

**Where the plans fall short, it is at the ends of irreversible steps, and the four P2 findings share one pattern: a plan defers a fact to a place that does not exist.**

- `AUDIT-FIX-43`: `F7.2-09` relies on billing documentation "read in `Faz7.1`", and `Faz7.1` has no such item.
- `AUDIT-FIX-44`: `F7.2-08` retrieves "the flashable package", and nobody establishes before teardown what flashing needs.
- `AUDIT-FIX-45`: `F7.3-07` restores to a "comparable region unchanged" that a downgrade may not allow.
- `AUDIT-FIX-46`: `Faz8.3` accepts "completed adaptation", and no sub-plan adapts.

In each case the sentence reads well and the handshake is missing. That is the cross-file residue this audit series keeps finding, now at phase boundaries rather than within one file.

**The P3s are precision issues in otherwise correct designs.**

- `AUDIT-FIX-51`, the most technical: `setmode.sh`'s `wait_svc` reads `getprop init.svc.<name>`, and its "stopped" branch returns success on any value other than `running`, including an empty property. A service name that no longer exists on Android 16 therefore passes the stop wait instantly. The provider is never actually stopped or restarted, and the reloaded sensor blob is never loaded. The resulting symptom is "mode switch has no effect", not the black preview `Faz8.3` names as the failure signal.
- `Faz8.3` cites `vendor.qti.camera.provider-service_64` from a crash log. That is a process name, and `wait_svc` needs init service names.
- `F8.3-05`'s own instruction ("compare the service names … against live service state") would catch this if done literally. The finding sharpens the detector; it does not change the design.

**Preservation of the main plan: intact.** Run 18 decomposed exactly the Phase 7 and Phase 8 text run 17 wrote. It made no new decision the master plan reserves to the user, and wrote no Step 1 artifact. `DEC-22`, `DEC-07` and `DEC-08` stay open and routed. The budget and stopping rule are explicitly a *future* ledger decision (`F7.1-10`), not one the planner assumed.

## 9. Scope Drift and Architectural Consistency Analysis

**No scope drift.** No phase was added or removed. The Phase 8 rename is a user-approved Step 1 correction recorded as `SNAP-2026-09-10-MAIN`. Snapshot discipline was followed: run 17 cut the main snapshot, run 18 cut the sub-plan snapshot, and the ledger records that Phases 1–6 and 9 carry forward with their own snapshot ids.

**Tool versus core boundaries are held.** `IMPL-90`'s "pin, not mirror" decision is kept, with its reason (datacenter fetch speed, no redistribution of multi-GB blobs). Signing stays AOSPA default, with no project key near the server. The AGC APK update and release targeting for Android 16 are pushed to Phase 9 decisions after evidence. CI stays out of scope with a stated reason.

**No premature live activation.** Every step that costs money or changes the device is gated on an earlier artifact and an explicit user decision. Consistent with `ARC-04`, no plan publishes blob-bearing output.

**Ontology consistency: the re-plan follows the corrected vocabulary; the ontology still has not caught up.**

- `beryl` is used everywhere as a branch, never as a device. The run-17 ontology entry reads that way.
- Invariant 10 (blob binding) is the explicit basis of `Faz8.1` and of the post-build and on-device md5 reads.
- Invariant 3 is re-confirmed for Android 16 before any mode switch.
- `Faz7.3` and `Faz8.3` each keep *stock* distinct: the Android 16 build's unmodified camera stack is not the module mode named `stock`.
- **Invariant 11 ("Sources must live inside the WSL filesystem … WSL2 is not installed")**, `EV-20` and `CQ-13` still describe the retired host. `F7.1-12` owns their retirement, and the index's section 2 warning says they "must not be used to plan". That is the correct holding pattern. `git grep` confirms `docs/reverse-engineering-toolchain.md:219` is the only tracked non-planner document still naming WSL2 as the plan, and `F7.1-12` covers it. `Autopsy.md` lines 117 and 230 also name WSL2, but it is a dated snapshot (`SNAP-2026-08-23-AUTOPSY`) and is correctly left alone.

**Planning-ledger continuity: good, with one unreconciled contradiction.**

- `IMPL-86`'s finding that the eighth audit's queue had shrunk to four blocked rows is what made this re-plan necessary. Run 18's rows cite it.
- `IMPL-89`'s rulings are all reflected: `DEC-21` in `Faz7.1` section 10, `DEC-16` recorded, `DEC-23` in `Faz8.3` PC-13.
- **But `IMPL-89`'s row (ledger line 516) records "`xiaomi-8550` has no ishtar or sm8550-common vendor repository"**, and `IMPL-90` pins `xiaomi-8550/proprietary_vendor_xiaomi_ishtar` the same day. This audit's read confirms that repository exists, is public, and carries `beryl` and `vauxite`, with `f92e7a9` dated 2026-05-12. The ledger never reconciles the two rows (`AUDIT-FIX-49`). It matters beyond tidiness: `F8.1-04`'s attribution needs "the vendor repository branch AOSPA's Android 15 build used". There are two candidates: `xiaomi-8550`'s `vauxite` branch, and `ThankYouMario/proprietary_vendor_xiaomi_ishtar` (`vauxite` only), which `IMPL-89` itself found. `Faz8.1` names neither.

**`AUDIT-FIX-50` is a continuity gap of the same kind.** `Faz8.3` section 6 treats `FIND-3.7-02` and `FIND-3.10-01` as live detector defects and mandates the PC-04 substitute. The ledger closed both on 2026-09-06 (`IMPL-80`, `DEC-20`), and `docs/release-checklist.md` section 4 says "Repaired 2026-09-06 (`IMPL-80`)". The checklist's own section 3 map (`C-04 … FIND-3.10-01`, `C-17 … FIND-3.7-02`) and the PC-04 comment ("DEFECTIVE via smoke.sh") were never updated, and `Faz8.3` read those rows.

**The master plan carries two residues outside any run's mandate** (`AUDIT-FIX-41`, `-42`). Section 8's step 5 still names `pref_camera_picturesize_back_key` as "the preference", after run 16 corrected the same claim in section 6. Sections 1 and 3 still call Android 16 a "`beryl` port", and section 9 still says "Do not expand yet … G is blocked on host-environment work". None misleads a queued row: each queued row quotes the corrected Phase 7/8 text.

## 10. Readiness Realism

**No overclaim was found in the six sub-plans, and several guard against overclaims explicitly:**

- `Faz7.2` reports post-build md5s "as facts, not conclusions" and defines a partial build as a recorded outcome.
- `Faz7.3` records camera enumeration "as a fact rather than a pass condition" and refuses to carry an Android 16 AON result back to Android 15.
- `Faz8.1` keeps agreement legs "pending, not assumed" until the builds exist.
- `Faz8.3` states that "a matching md5 proves only input identity".
- `Faz8.2` states that the `beryl` 5.15 base is "**not measured**".

**Local versus live is drawn correctly for this domain.** `Faz7.1` defines "live" as a rented server and forbids it. `Faz7.2` separates the live sync and build from local retrieval checks. `Faz7.3` and `Faz8.3` are live on the one device and say so.

**Status labels are honest.** The ledger keeps `Faz6.1` at `implemented` because "no build has yet consumed the `;SYMLINK=` entry", and `Faz7.3` is where that changes, with `F7.3-08` proposing — not asserting — the move to `verified`.

**One realism gap, in the restore criterion (`AUDIT-FIX-45`).** "Post-restore snapshot's comparable region matches the pre-flash one" is realistic for a module-level recovery, which is what `docs/recovery-runbook.md` covers. For a whole-system return from Android 16 to 15 it may be unattainable without a `/data` wipe. In that case the AGC pin (`pref_48m_key=0`), KernelSU and both modules must be *re-established*, not *preserved*. The criterion's escape clause, "or each difference is explained", technically covers this, but it lets a lost daily-use configuration pass as an explained difference instead of a planned step.

**No plan calls strategy "vibecoding".** Every slice named is a measurement, a read, a decision routed, or a file edit with a validation signal.

## 11. Security and Governance Findings

- **Secret safety: clean.** `secret_findings=0` in every validator mode. No token, credential, password, private key or server address appears in any planner file. `Faz7.1` and `Faz7.2` forbid writing any of them into repositories, runbooks, snapshots or ledger rows, and require a file-name-only scan (`VAL-SEC`) that never prints a match. **Residual, not raised as a finding:** if the server authenticates `repo` with a token embedded in a clone URL, `.repo` configuration, `repo manifest -r` output or a build log can capture it. `VAL-SEC` scans the retrieved files, which catches it after the fact. The runbook `F7.1-11` writes should prefer a credential helper over URL embedding.
- **Least privilege: held.** The server credential is read-only, limited to the named repositories, created at rental and revoked at teardown, with the revocation verified (`VAL-TEARDOWN`). `Faz7.1` offers making the one-line device-tree fork public so no credential is needed for it. The manifest repository would still be private, and `F7.1-10` covers private repositories in the plural.
- **Command execution safety: tightened.** The `IMPL-90` defect class (a pipe masking a failed `git am`, then an ungated push) is now a rule in both `Faz7.1` and `Faz7.2`: fail-on-error everywhere, and every publish gated on a read-back. `VAL-SYNC` compares revisions instead of trusting exit status.
- **Artifact integrity: good.** Retrieved outputs are sha256-verified at both ends. The md5 of the guarded blobs is read three times: vendor repository, build output, device. `Faz8.3` checks the archive's sha256 against `docs/release-manifest.md` before a root-privileged install.
- **Blob redistribution: held, with one hole.** Retrieved images go outside tracked paths, with an ignore rule added first if needed, since `.gitignore` has no `*.img` rule (verified). `Faz8.1`'s fetched blobs, however, live in an unspecified "untracked scratch location" until `F8.1-10`, which runs after the agreement half. `.gitignore` ignores only `ishtar-cam-modes/{blobs,active,candidates}/*.bin`, not `*.so` or a generic scratch path (`AUDIT-FIX-47`).
- **Approval gates: complete for money and device.** Renting, every GitHub push, teardown confirmation, the flash, firmware approval, root method, install, every capture and the stay-or-restore choice are each named as the user's. `Main-Planing.md` section 5's human-approval boundary is applied in full.
- **Destructive and irreversible operations.** Server deletion is intended and gated. The whole-system flash is gated on a return path and a go/no-go. **The two gaps are the facts those gates need** (`AUDIT-FIX-43` billing and deletion semantics, `AUDIT-FIX-44` install artifacts before deletion, `AUDIT-FIX-45` wipe semantics before the flash). None is dangerous under the plans as written, because a human approves each step. Each could still cost money or a day of re-configuration that a single read beforehand would avoid.
- **Ontology writes into a NUL-bearing file.** `F7.1-12`, `F8.1-10` and `F8.2-09` edit `Project-Ontology.md`, whose control bytes make content search fail silently (`AUDIT-FIX-22`). An editor that normalises or truncates on the NUL could damage the address book. Step 4 should repair the table first or edit with byte-preserving tooling and diff the result.
- **Audit boundary.** `DEC-16` (2026-09-10) now permits an audit to repair a P1 it found. **No P1 was found, and this audit repaired nothing**, as the user's instruction for this run required. All findings are routed.

## 12. Step 4 Readiness Assessment

Dependency state follows the convention the eight previous audits used. `independent` means no upstream dependency. `satisfied` means every upstream dependency is complete in the repository or produced by an earlier row of this same queue. Queued rows appear in execution order, from index amendment 4d. Only one row per sub-plan is allowed, so `Faz8.1` appears once, in its static-half position. Its agreement half (`F8.1-06`, `F8.1-07`) resumes after `Faz7.2` and `Faz7.3`, as that row's Required Repair column states.

**What changed since the eighth audit.** Every one of its ten queued Phase 2, 3, 4, 6 and 9 rows is now `verified` and moves to `COMPLETE`. The four Phase 7/8 rows it queued were re-planned. Two were replaced, two rewritten, and two new rows were added.

**Counts, measured from the ledger matrix: 6 queued (0 `READY`, 6 `READY_WITH_WARNINGS`), 33 COMPLETE, 2 SUPERSEDED, 1 DEFERRED, 0 NEEDS_REPAIR = 42.** `Faz6.1` is COMPLETE as an edit, and its effect verification is owned by queued row `Faz7.3`. That keeps a single active status per file.

**Why no Phase 7/8 row is `NEEDS_REPAIR`.** The test the previous audits applied is: can a Step 4 run be graded correctly against the file as written? For every row, yes. `AUDIT-FIX-43` and `-44` fall inside `Faz7.1`'s own runbook deliverable (`F7.1-11` already owns teardown and the evidence list). `AUDIT-FIX-45` is caught by `F7.3-01`'s "if any item cannot be completed, stop" and by the user's go/no-go. `AUDIT-FIX-46` makes `Faz8.3`'s gate block on anything but carry-over, which is the safe direction. Each is carried in the row an implementer will read.

| Sub-Plan Path | Status | Finding IDs | Dependency State | Reason | Required Repair |
|---|---|---|---|---|---|
| Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md | READY_WITH_WARNINGS | AUDIT-FIX-43, AUDIT-FIX-44, AUDIT-FIX-22 | satisfied | Queue head. Host-only and free. Depends on `IMPL-90`'s staging, re-verified by this audit's read (manifest `4182695`, device tree `beryl` `d48816f`, seven open items), and on `DEC-24` and `DEC-01`, both answered. | Start at `F7.1-01`. In `F7.1-02`/`F7.1-10`, also read and record the provider's billing and deletion semantics: the product type and billing unit, whether a powered-off server still bills, and what else bills (volumes, snapshots, backups, primary IPs). Write them into the runbook's teardown and the budget decision (`AUDIT-FIX-43`). In `F7.1-11`, name from AOSPA's `ishtar` install instructions every artifact the flash needs, so `Faz7.2` retrieves all of them before deletion (`AUDIT-FIX-44`). `F7.1-12` edits `Project-Ontology.md`: use byte-preserving edits and diff the file afterwards (`AUDIT-FIX-22`). Prefer a credential helper to a token in a clone URL. |
| Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md | READY_WITH_WARNINGS | AUDIT-FIX-46, AUDIT-FIX-47, AUDIT-FIX-49, AUDIT-FIX-22 | satisfied | Static half (`F8.1-01`–`F8.1-05`, plus `F8.1-08`/`-09` on static values) needs only `Faz7.1`'s pin confirmation, which is the row above. The vendor commit `f92e7a9` is confirmed to exist. The agreement half resumes after `Faz7.2` and `Faz7.3`. | Keep fetched blobs **outside the workspace**, and delete them at the end of the static half, not at `F8.1-10` (`AUDIT-FIX-47`). For `F8.1-04`, the Android 15 attribution candidates are `xiaomi-8550/proprietary_vendor_xiaomi_ishtar` `vauxite` and `ThankYouMario/proprietary_vendor_xiaomi_ishtar` `vauxite`; decide which one AOSPA `vauxite` consumed before hashing (`AUDIT-FIX-49`). If the sensor module differs, label it and route `DEC-07` with a replanning input, exactly as for a HAL difference. **Do not treat adaptation as work `Faz8.3` can consume** (`AUDIT-FIX-46`). `F8.1-10` writes the ontology (`AUDIT-FIX-22`). |
| Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md | READY_WITH_WARNINGS | AUDIT-FIX-22 | satisfied | Needs only `Faz7.1` `F7.1-05`'s named kernel. No build, server or device. May run in parallel with the next two rows. | If `F7.1-05` deferred the kernel, record the sub-phase as blocked on it; do not substitute a `vauxite` checkout. Prove `git merge-tree --write-tree` on a known merge first, and watch the blobless clone's lazy blob fetches; the token hazard is path dumps, not reasoning. `F8.2-09` writes the ontology (`AUDIT-FIX-22`). |
| Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | READY_WITH_WARNINGS | AUDIT-FIX-43, AUDIT-FIX-44 | satisfied | The paid session. Every input it needs is a `Faz7.1` output, earlier in this queue. Its own pre-rental gate re-checks them on the day. A Step 4 session stops here for the user's rental approval, which is the design. | Do not rent until the runbook states the provider's deletion and billing semantics (`AUDIT-FIX-43`). Before `F7.2-09` deletes the server, confirm every install-method artifact named in the runbook is retrieved with a matching sha256, or record that it can be extracted locally from the package (`AUDIT-FIX-44`). Scan `repo manifest -r` and log tails for credentials before copying them. |
| Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | READY_WITH_WARNINGS | AUDIT-FIX-45 | satisfied | The user's flash of the daily device. Depends on `Faz7.2`'s retrieved package and AON step 1 result, earlier in this queue. Benefits from `Faz8.1`'s static result, which is also earlier. | In `F7.3-01`, record from AOSPA's documentation whether 15 → 16 needs a data format and whether 16 → 15 does. If either does, the return path must include re-rooting, reinstalling v2.2 against `docs/release-manifest.md`, re-applying the AGC configuration by `docs/agc-12mp-configuration.md` section 2 (write, two cold starts, read) and a trap audit. Tell the user about the wipe at the `F7.3-02` go/no-go. Grade `F7.3-07` against the re-established state, not a preserved one (`AUDIT-FIX-45`). |
| Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md | READY_WITH_WARNINGS | AUDIT-FIX-46, AUDIT-FIX-50, AUDIT-FIX-51 | satisfied | The functional test, on the carry-over path only. Depends on `Faz8.1`'s classification with three-way agreement and `Faz7.3`'s device state, both earlier in this queue. Archive and checklist are verified (`Faz9.1`, `Faz9.2`). | **Gate on HAL carry-over AND sensor carry-over.** Treat a sensor adaptation label as blocked with a replanning input, because no sub-plan adapts and an adapted blob cannot pass v2.2's `EXPECT_MD5` (`AUDIT-FIX-46`). For `F8.3-05`, list `getprop \| grep init.svc` on Android 16 and compare init service names against `cameraserver`, `vendor.camera-provider` and `vendor.camera-provider-2-7-ext`. `wait_svc` returns success on a missing service, so add "mode switch has no effect" to the failure signals (`AUDIT-FIX-51`). Use the repaired `smoke.sh` fields (`prefs.trap.armed`; single-dump `probe_main_rows`), and keep the PC-04 substitute only as a cross-check (`AUDIT-FIX-50`). |
| Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md | DEFERRED | none | blocked | **Not queued.** Host-side half `implemented`. `F4.6-07` was gated on the superseded `Faz4.1`. `DEC-19` keeps `FIND-3.5-01` and `FIND-4.5-02` as knowledge. | Completing it would be a new user decision and a new sub-plan. |
| Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | SUPERSEDED | none | independent | `superseded` 2026-09-03 by `DEC-14`. | **Do not revive it.** |
| Planner-docs/Faz-4-Plans/Faz4.7-ultra-high-resolution-sensor-mode.md | SUPERSEDED | none | independent | `superseded` 2026-09-03 by `DEC-14`. | **Do not revive it as project work.** |
| Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md | COMPLETE | none | satisfied | `IMPL-03`. The edit is in both trees and in the staged fork (`d48816f`, one line). Ledger status stays `implemented` because the effect is unverified. **`Faz7.3` `F7.3-08` now owns that verification**, so the row is not queued in its own right. | none. Do not report it `verified` before `Faz7.3` step 3 passes. |
| Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md | COMPLETE | none | satisfied | `IMPL-01`. `DEC-01` answered 2026-09-10: private remote `ahmetxa/ishtar` (`IMPL-90`). | none. |
| Planner-docs/Faz-1-Plans/Faz1.2-signing-key-containment.md | COMPLETE | none | satisfied | `IMPL-02`. `DEC-10` answered (`IMPL-80`). | none. |
| Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | COMPLETE | AUDIT-FIX-25 | satisfied | `IMPL-06`. One stale forward reference to the retired narrowing (accepted). | none. |
| Planner-docs/Faz-1-Plans/Faz1.4-toolchain-procedure-record.md | COMPLETE | none | satisfied | `IMPL-07`. Its WSL2 boundary sentence is history; `docs/reverse-engineering-toolchain.md` section 7 is corrected by `F7.1-12`. | none. |
| Planner-docs/Faz-1-Plans/Faz1.5-static-safety-probes.md | COMPLETE | none | satisfied | `IMPL-05`. | none. |
| Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md | COMPLETE | none | satisfied | `IMPL-08`. | none. |
| Planner-docs/Faz-2-Plans/Faz2.1-device-smoke-script.md | COMPLETE | none | satisfied | `IMPL-04`; extended by `IMPL-55`/`-56` and repaired by `IMPL-80`. | none. |
| Planner-docs/Faz-2-Plans/Faz2.2-flash-v21-and-baseline-snapshot.md | COMPLETE | none | satisfied | `IMPL-09` … `IMPL-12`. | none. |
| Planner-docs/Faz-2-Plans/Faz2.3-ten-mode-regression-pass.md | COMPLETE | none | satisfied | `IMPL-13`. | none. |
| Planner-docs/Faz-2-Plans/Faz2.4-tiles-hide-disposition.md | COMPLETE | none | satisfied | `IMPL-71`, `IMPL-75`; `DEC-02` answered (keep and fix). | none. |
| Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md | COMPLETE | none | satisfied | `IMPL-16`; narrowed by `FIND-3.7-01`, closed at the file by `IMPL-62`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.2-pixel-array-write-site-search.md | COMPLETE | none | satisfied | `IMPL-18`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md | COMPLETE | none | satisfied | `IMPL-20`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.4-consumer-compatibility-check.md | COMPLETE | none | satisfied | `IMPL-21`, `IMPL-22`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md | COMPLETE | none | satisfied | `IMPL-23`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.6-fallback-decision-gate.md | COMPLETE | none | satisfied | `IMPL-24`. Closed the retired objective. | none. |
| Planner-docs/Faz-3-Plans/Faz3.7-agc-photo-size-pin.md | COMPLETE | none | satisfied | `IMPL-52`, `IMPL-53`, `IMPL-54`; `DEC-18` adopted `pref_48m_key=0`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md | COMPLETE | AUDIT-FIX-33 | satisfied | `IMPL-55`, `IMPL-56`. Built at four fields; the three-field text residue is accepted history. | none. |
| Planner-docs/Faz-3-Plans/Faz3.9-coexistence-bracket.md | COMPLETE | none | satisfied | `IMPL-57`, `IMPL-58`, `IMPL-83`; `FIND-3.9-02` closed by `IMPL-85`. | none. |
| Planner-docs/Faz-3-Plans/Faz3.10-pin-stickiness-matrix.md | COMPLETE | AUDIT-FIX-39, AUDIT-FIX-40 | satisfied | `IMPL-60`, `IMPL-61`. All four axes survived. Both findings are not_applicable after execution. | none. |
| Planner-docs/Faz-3-Plans/Faz3.11-phase-closure-and-configuration-record.md | COMPLETE | AUDIT-FIX-38 | satisfied | `IMPL-62`, `IMPL-63`, `IMPL-89`. Phase 3 marked successful (`DEC-21`). `F3.11-08` disposed of `FIND-3.7-03` on what `Faz3.10` measured. | none. |
| Planner-docs/Faz-4-Plans/Faz4.2-duration-rows.md | COMPLETE | none | satisfied | `IMPL-64`. | none. |
| Planner-docs/Faz-4-Plans/Faz4.3-patch-table-consolidation.md | COMPLETE | AUDIT-FIX-22 | satisfied | `IMPL-65`, `IMPL-66`. The warning is carried for anyone re-reading the ontology's `Escape` column. | none. |
| Planner-docs/Faz-4-Plans/Faz4.4-patch-compatibility-validation.md | COMPLETE | none | satisfied | `IMPL-67`, `IMPL-68`, `IMPL-70`. | none. |
| Planner-docs/Faz-4-Plans/Faz4.5-active-array-raise.md | COMPLETE | none | satisfied | `IMPL-27` … `IMPL-30`. | none. |
| Planner-docs/Faz-5-Plans/Faz5.1-twelve-bit-mode-zero-blob.md | COMPLETE | none | satisfied | `IMPL-14`. | none. |
| Planner-docs/Faz-5-Plans/Faz5.2-temporary-mount-composition-test.md | COMPLETE | none | satisfied | `IMPL-15`. | none. |
| Planner-docs/Faz-5-Plans/Faz5.3-exclusion-rule-disposition.md | COMPLETE | none | satisfied | `IMPL-17`. | none. |
| Planner-docs/Faz-6-Plans/Faz6.2-aon-module-disposition.md | COMPLETE | none | satisfied | `IMPL-72`, `IMPL-75`; `DEC-04` keep separate. `FIND-6.2-01`'s cross-reference is discharged by `Faz7.2` section 1, and `FIND-6.2-03` is routed to `Faz7.3`. | none. |
| Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md | COMPLETE | none | satisfied | `IMPL-76`, `IMPL-81`. | none. |
| Planner-docs/Faz-9-Plans/Faz9.2-release-verification-checklist.md | COMPLETE | none | satisfied | `IMPL-19`, `IMPL-78` … `IMPL-89`; `DEC-23` accepted PC-13's method. | none. Its section 3 map still carries pre-repair detector labels; see `AUDIT-FIX-50`. |
| Planner-docs/Faz-9-Plans/Faz9.3-documentation-consolidation.md | COMPLETE | none | satisfied | `IMPL-77`, `IMPL-78`, `IMPL-81`. | none. |

**Execution queue state: READY.** Six rows are queued, all `READY_WITH_WARNINGS`. No blocking finding applies, no path is unsafe, no target is missing, and no queued row's dependency state is `blocked` or `unknown`. **Queue head: `Faz7.1`.** Human stop gates are built into the queue and are not blockers: `DEC-22` and the budget decision inside `Faz7.1`, rental approval at `Faz7.2`, the flash at `Faz7.3`, and root at `Faz8.3`.

## 13. Priority Fix List

**No P0 or P1 finding is open.** The register now holds 51 findings. Eleven are new this run (`AUDIT-FIX-41` … `-51`), and forty are carried. **Fifteen remain active: five P2 open (`-22`, `-43`, `-44`, `-45`, `-46`), eight P3 open (`-37`, `-41`, `-42`, `-47`, `-48`, `-49`, `-50`, `-51`) and two P3 accepted (`-25`, `-33`).** Changed this run: two resolved (`-30`, `-35`) and three `not_applicable` (`-38`, `-39`, `-40`). The findings resolved by earlier audits are not re-listed row by row; nothing since has touched their subject matter.

| Finding ID | Severity | Status | Affected Files | Issue | Required Action |
|---|---|---|---|---|---|
| AUDIT-FIX-46 | P2 | open | Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md, Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md, Planner-docs/Sub-Planing-Index.md | **New.** The sensor-layer adaptation branch leads nowhere. `F8.1-08` defines "adaptation". `Faz8.3`'s `F8.3-01` and `Faz8.1`'s transition criterion (line 169) accept "carry-over **or completed adaptation**". But `Faz8.1` section 5 excludes regenerating sensor blobs, and `Faz8.3` section 5 excludes regeneration, editing `customize.sh` and rebuilding the archive. An adapted blob changes `EXPECT_MD5` and so cannot pass the "unchanged v2.2" install. `F8.1-09` prices only carry-over and re-derivation, and index section 5 defers only the HAL re-derivation. | In a bounded Step 2 amendment, before `Faz8.3` runs: route adaptation like re-derivation in `F8.1-09` (a `DEC-07` basis plus a ledger section 7 input). Make `Faz8.3`'s gate and `Faz8.1`'s transition criterion require sensor **carry-over**. Add "sensor-layer adaptation on the Android 16 blob" to index section 5's deferred list. |
| AUDIT-FIX-43 | P2 | open | Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | **New.** `F7.2-09` (line 96) says "Delete the server — not merely power it off, unless the provider's billing documentation, **read in `Faz7.1`**, says otherwise". No `Faz7.1` work item, acceptance criterion or transition criterion reads the provider's billing or deletion semantics. `F7.1-02` reads build requirements and sizing; `F7.1-10` agrees a ceiling without a billing model. The budget, the stopping rule and the teardown's correctness all depend on those facts: product type and billing unit, whether stopped servers bill, and what else bills. | Add to `F7.1-02` or `F7.1-10` a sourced read of the provider's billing and deletion semantics, recorded in the runbook's teardown section and cited by the budget decision row. Add the matching criterion to `Faz7.1` sections 8 and 13. Until the plan is amended, a Step 4 implementer of `Faz7.1` can satisfy this inside `F7.1-11`, which already owns teardown. |
| AUDIT-FIX-44 | P2 | open | Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | **New.** `F7.2-08` retrieves "the flashable package, the revision manifest, the build log tail and the evidence block". Nothing ties that list to what AOSPA's install method for `ishtar` actually flashes. `F7.3-03` says only "the user flashes with AOSPA's documented method", and `F7.3-02` inspects the package after the server is deleted. If the method needs artifacts not in the package, the gap is found only after an irreversible teardown, and rebuilding means a second paid sync and build. | In `F7.1-11`, name from AOSPA's published install instructions every artifact the `ishtar` flash consumes. Make `F7.2-08` and its acceptance criterion retrieve each one with sha256, or record before deletion that it can be extracted locally from the package. |
| AUDIT-FIX-45 | P2 | open | Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | **New.** The return path and the restore criterion ignore what a major-version flash does to `/data`. `F7.3-01` records a package, its sha256 and re-flash steps. `F7.3-07` "reinstalls the recorded modules if the re-flash removed them" and requires the post-restore comparable region to match the pre-flash one (line 98). Neither establishes whether 15 → 16 or 16 → 15 requires a data format. If either does, the AGC pin (`pref_48m_key=0`), KernelSU and both modules are lost, not preserved, and "each difference is explained" lets a lost daily configuration pass as an explanation. | In `F7.3-01`, record AOSPA's documented data requirement for both directions. If a format is required, extend the return path with re-rooting, reinstalling v2.2 against `docs/release-manifest.md`, re-applying `docs/agc-12mp-configuration.md` section 2, and a trap audit. State the wipe to the user at `F7.3-02`. Make `F7.3-07`'s criterion compare against the re-established state. |
| AUDIT-FIX-22 | P2 | open | Planner-docs/Project-Ontology.md | Carried and re-measured. Still **7** control bytes below 0x20, including **2 NUL**, now at byte offsets 42590, 42653, 42716, 42773, 42774, 42775 and 42897. That is +100 from the eighth audit's figures, because run 17 lengthened the `beryl` entry above them. Content search on the file still fails silently. **New consequence:** three queued rows (`F7.1-12`, `F8.1-10`, `F8.2-09`) write to this file. | Unchanged: replace the `Escape` column's raw bytes with the project's octal `printf '%b'` convention in a bounded amendment of that one table, then confirm the file reappears in `rg -l InitializeScalerStaticCaps`. Until then, Step 4 edits to this file must be byte-preserving and diffed, and no escape may be transcribed from that column. |
| AUDIT-FIX-51 | P3 | open | Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md | **New.** `F8.3-05`'s detector is under-specified. `setmode.sh` stops and waits on init service names (`cameraserver`, `vendor.camera-provider`, `vendor.camera-provider-2-7-ext`) through `wait_svc`, which reads `getprop init.svc.<name>` and treats any value other than `running` — including an empty one — as stopped. On a missing name the stop wait succeeds instantly, `stop`/`start` do nothing, and the provider never reloads the sensor blob, so the symptom is a switch with no effect, not black preview. Section 6's evidence cites `vendor.qti.camera.provider-service_64`, a crash-log process name, not an init service name, and section 11 names only black preview as the failure. | Specify `VAL-RESTART` as listing `init.svc.*` for the camera services on the Android 16 build and comparing them with `setmode.sh`'s three names. Add "provider never restarted / switch has no effect" as a failure signal beside black preview. |
| AUDIT-FIX-50 | P3 | open | Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md, docs/release-checklist.md | **New.** `Faz8.3` section 6 (line 54) and `F8.3-06` treat `FIND-3.7-02` and `FIND-3.10-01` as live detector defects and require the PC-04 substitute. Both were repaired 2026-09-06 (`IMPL-80`, `DEC-20`): the ledger disposition table closes both, and `docs/release-checklist.md` section 4 says "Repaired". The checklist's own section 3 map (`C-04 … FIND-3.10-01`, `C-17 … FIND-3.7-02`) and PC-04's "DEFECTIVE via smoke.sh" comment were never updated, and `Faz8.3` inherited those rows. | In `Faz8.3`, grade PC-17 on `prefs.trap.armed` and PC-04 on the repaired single-dump probe, keeping the substitute as a cross-check. A Step 4 session touching `docs/release-checklist.md` should update the section 3 labels and the PC-04 comment to point at section 4's repair notes. |
| AUDIT-FIX-47 | P3 | open | Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md, Planner-docs/Sub-Planing-Index.md | **New.** Two boundary slips. (1) Section 5 (line 43) says fetched blobs "are deleted after hashing", but deletion is `F8.1-10`, which follows the agreement half, possibly weeks later. The "untracked scratch location" is unspecified, and `.gitignore` covers only `ishtar-cam-modes/{blobs,active,candidates}/*.bin`, not `*.so` or a generic scratch directory. (2) Index amendment 4d defines the static half as `F8.1-01` to `F8.1-05`; `Faz8.1` section 10 adds `F8.1-08` and `F8.1-09` on static values. | Name a scratch location outside the workspace and move deletion to the end of the static half (after `F8.1-05`). Align index 4d's static-half boundary with `Faz8.1` section 10. |
| AUDIT-FIX-49 | P3 | open | Planner-docs/Planing-Ledger.md, Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md | **New.** Ledger row `IMPL-89` (line 516) records "`xiaomi-8550` has no ishtar or sm8550-common vendor repository". `IMPL-90` pins `xiaomi-8550/proprietary_vendor_xiaomi_ishtar` the same day, and this audit's read found it public with branches `beryl` and `vauxite` and commit `f92e7a9` dated 2026-05-12. The contradiction is unreconciled. `F8.1-04`'s attribution source ("the vendor repository branch AOSPA's Android 15 build used") names no candidate, although two exist: `xiaomi-8550` `vauxite`, and `ThankYouMario/proprietary_vendor_xiaomi_ishtar` `vauxite`, which `IMPL-89` found. | Annotate the `IMPL-89` row as corrected by `IMPL-90` (ishtar measured; sm8550-common per `check.py`). Name both candidates in `F8.1-04`, and have it decide from AOSPA's `vauxite` manifest which one the Android 15 build consumed. |
| AUDIT-FIX-48 | P3 | open | Planner-docs/Sub-Planing-Index.md | **New.** Section 7's run 18 paragraph (line 356) states "All six sub-plans use CRLF line endings like their siblings". Measured at byte level: all 42 sub-plans and the index are LF-only; only `Main-Planing.md`, `Planing-Ledger.md` and `Autopsy.md` are CRLF. | Correct the sentence to LF. No session should convert any sub-plan's line endings on the strength of the current wording. |
| AUDIT-FIX-41 | P3 | open | Planner-docs/Main-Planing.md | **New, and a residue of the defect `AUDIT-FIX-35` named.** Run 16 corrected section 6's Phase 3 slice, but section 8's step 5 (line 277) still says "the preference is `pref_camera_picturesize_back_key` and the app exposes it as an ordinary settings menu item". `IMPL-52` measured that key as derived and reverted at every AGC start. No queued row reads it, and Phase 3 is closed. | At the next deliberate Step 1 amendment, rewrite step 5 to the measured configuration (`pref_48m_key=0`, `pref_camera_resolution=full`, read the derived key back) and mark it done under `DEC-21`. |
| AUDIT-FIX-42 | P3 | open | Planner-docs/Main-Planing.md | **New, a residue of run 17.** Three sentences still carry the retired Phase 7/8 premises: section 1 (line 22), "a third (Android 16 / beryl) has not started"; section 3 (line 61), "Android 16 / AOSPA `beryl` port"; section 9 (line 288), "Do not expand yet. Phases 7, 8, and 9. G is blocked on host-environment work the user must perform". Index section 2 records the last as a known ambiguity and decomposes the phases anyway, correctly. | At the same Step 1 amendment, reword all three to `DEC-24` and the branch reading of `beryl`, and mark section 9's paragraph discharged (Phases 7 and 8 decomposed by run 18; Phase 9 verified). Do not cut a snapshot for these alone. |
| AUDIT-FIX-37 | P3 | open | Planner-docs/Project-Comprehension.md | Carried, **narrowed**. `Project-Ontology.md` now cites `IMPL-52` twice, `IMPL-53` once and `IMPL-54` twice (it was zero), so that half is resolved. `Project-Comprehension.md` still cites none of them, so the derivation mechanism has no evidence row there. | Add the derivation mechanism as an evidence entry. `Faz7.3` (`TRACE-13`, `ARC-06`) and `F7.1-12` (`EV-20`, `CQ-13`) both write this file and are natural moments to fold it in. |
| AUDIT-FIX-33 | P3 | accepted | Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md, Planner-docs/Sub-Planing-Index.md | Carried. Three places still describe three fields (`Faz3.8` lines 120 and 163, index line 106). **`Faz3.8` is `verified` at four fields (`IMPL-55`, `IMPL-56`)**, so the residue no longer shapes any work. | No repair required. Accepted and kept visible so a replanning run reads the ledger's four-field result, not the index sentence. |
| AUDIT-FIX-25 | P3 | accepted | Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | Carried, unchanged at line 9: "Faz 4.1 narrows the RAW emission …". | No repair required; `Faz1.3` is COMPLETE. |
| AUDIT-FIX-35 | P2 | resolved | Planner-docs/Main-Planing.md | Section 6's Phase 3 first slice told the reader to set the derived `pref_camera_picturesize_back_key`. | **Resolved by planning run 16 (2026-09-07), verified this run at line 167**, which now reads: set `pref_48m_key`=`0` and `pref_camera_resolution`=`full`, read back what the derived key *derives to*, "do **not** write that key". The section 8 residue is raised separately as `AUDIT-FIX-41`. |
| AUDIT-FIX-30 | P3 | resolved | Planner-docs/Main-Planing.md | Section 6's second Phase 3 fact stated `IMPL-43`'s proximate-selector conclusion unnarrowed. | **Resolved by planning run 16, verified this run at line 159**: the key "is a **derived** value rather than an input, so it is not a pin point", with the in-place correction dated 2026-09-07. |
| AUDIT-FIX-38 | P3 | not_applicable | Planner-docs/Faz-3-Plans/Faz3.11-phase-closure-and-configuration-record.md | `F3.11-08`'s parenthetical about `Faz3.10` was stale. | **Not applicable after execution.** `Faz3.11` is `verified`. The ledger's `F3.11-08` disposition reads "It did (`IMPL-61` part 2 …)", so the implementer took the conditional on measurement, which is what the finding protected. The text is history. |
| AUDIT-FIX-39 | P3 | not_applicable | Planner-docs/Faz-3-Plans/Faz3.10-pin-stickiness-matrix.md | Sections 3 and 9 described the pre-repair negative control. | **Not applicable after execution.** `Faz3.10` is `verified` (`IMPL-60`, `IMPL-61`), graded against sections 4, 7, 8 and 13. |
| AUDIT-FIX-40 | P3 | not_applicable | Planner-docs/Faz-3-Plans/Faz3.10-pin-stickiness-matrix.md | The pre-stated prediction's ordering was self-attested. | **Not applicable after execution.** The sub-plan is `verified`, and the refinement can no longer be applied to it. Whether the implementer timestamped the prediction was not re-checked this run. |

**Finding status consistency.** Fifteen findings are active: five P2 open, eight P3 open and two P3 accepted. No P0 or P1 is open, so Step 4 is unblocked. The status is `PASS_WITH_WARNINGS`, not `PASS`, because those fifteen are open or accepted, and all must stay visible during implementation.

**A note on the open P1s in the project, kept because the distinction still matters.** `FIND-3.5-01` and `FIND-4.5-02` are P1 **project** findings, not audit findings, and `DEC-19` keeps both as knowledge. They do not gate Step 4.

**Validator behaviour, stated so it is not misread.** `--mode step3 --strict` and `--mode step4 --strict` report `validation_status=failed` with one error, `strict_warning=step4_has_nonblocking_warnings`. That is `--strict` promoting the non-blocking P2/P3 warning into an error. Every `PASS_WITH_WARNINGS` audit gets this result, and it is **not** a structural defect. The gating facts are `p0_findings=0` and `p1_findings=0`.

## 14. Recommended Next Command / Prompt

**Status is `PASS_WITH_WARNINGS`, no P0 or P1 is open, and only P2/P3 findings remain, so the Step 4 prompt is printed.** Two supporting actions are recommended alongside it; neither has to happen before Step 4 starts.

1. **Step 4 now, at `Faz7.1`.** It is host-only, costs nothing, and absorbs `AUDIT-FIX-43` and `-44` into its own runbook.
2. **One bounded Step 2 amendment before `Faz7.3` runs**, targeting only `Faz7.3` (`AUDIT-FIX-45`), `Faz8.1` and `Faz8.3` (`AUDIT-FIX-46`, `-47`, `-51`, `-50`), and index sections 4d, 5 and 7 (`AUDIT-FIX-46`, `-47`, `-48`). The natural moment is after `Faz7.1` closes and before anything is rented. It needs no device, no measurement and no new decision.
3. **At the next deliberate Step 1 amendment**, fold in `AUDIT-FIX-41` and `-42`. Do not cut a snapshot for them alone.

```text
/claudeqb:claudeqb Read and return the exact canonical handoff from references/handoffs/run-step4.md, then execute it.

Context: the ninth Step 3 audit (2026-09-11) is PASS_WITH_WARNINGS with no open P0 or P1. Execution queue state is READY: six rows, all READY_WITH_WARNINGS, in this order - Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md, Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md (static half F8.1-01..05 plus F8.1-08/09 on static values; agreement half resumes after Faz7.2 and Faz7.3), Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md, Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md. Keep the fifteen active findings visible: AUDIT-FIX-22, -25, -33, -37, -41, -42, -43, -44, -45, -46, -47, -48, -49, -50, -51. Start at F7.1-01 (re-run check.py both ways; staged state read 2026-09-11: manifest 4182695, device tree beryl d48816f, seven open items). gh is not on PATH; use the WinGet gh.exe via check.py's GH override. In F7.1-10/F7.1-11 also record the provider's billing and deletion semantics (AUDIT-FIX-43) and every artifact AOSPA's ishtar install method flashes (AUDIT-FIX-44), both in docs/build-environment.md. F7.1-12 edits Project-Ontology.md, which contains NUL bytes: make byte-preserving edits and diff the file (AUDIT-FIX-22). Every script fails on non-zero exit; gate every push on a read-back; write no token, key, password or server address anywhere. Stop for the user at DEC-22, the budget and stopping-rule decision, every push, and the rental. Do not start Faz7.3 or Faz8.3 before the bounded Step 2 amendment for AUDIT-FIX-45 and AUDIT-FIX-46 has run, or before applying their Required Repair notes from the audit's section 12. Work in small verified slices, do not load all sub-plans at once, and append an implementation summary to Planner-docs/Planing-Ledger.md.
```

**Token and queue reminder.** Continue through the queue in small verified slices rather than loading the set. The near-term work is `Faz7.1`: many small GitHub reads, so record one verdict per open item, not transcripts. After that comes `Faz8.1`'s static half, two files and four constants, and `Faz8.2`, where you bucket path counts and never dump paths. `Faz7.2` is where both token and money risk peak: record exit status, stage, error class and log tails only, and keep the stopping rule in the session's own context.

Do not run the prompt from this audit session.

## 15. Audit Result

- **Final status: PASS_WITH_WARNINGS.** Nine main phases, nine phase folders, 42 sub-plan files, all structurally compliant, with zero structural problems measured across all 42. Validator `--mode step2 --strict` and `--mode step3-preflight --strict` both pass: `error_count=0`, `warning_count=0`, `secret_findings=0`, `subplan_count=42`, `index_reference_count=42`. Fifteen findings are active (five P2 open, eight P3 open, two P3 accepted), with no P0 or P1. The execution queue is READY with six rows headed by `Faz7.1`.
- **Confidence: high** on structure, coverage, index consistency and every repository or GitHub fact this audit asserts; each was re-measured this run. **Medium** on the four P2 findings' practical impact. Each rests on a fact this audit deliberately did not research — AOSPA's install method and data requirements, and the provider's billing semantics — so each is framed as "the plan does not establish X before an irreversible step", not "X is wrong". **Not assessed for content this run:** the 36 unchanged sub-plans outside Phases 7 and 8, all complete, superseded or deferred, on which earlier audits' assessments stand.
- **Only `Planner-docs/Sub-Planing-Audit.md` was modified by this run.** No sub-plan, index, ledger, master plan, ontology, comprehension file or source file was written. No device command was run, and no GitHub write was made.
- **Unexpected modifications: none detected.** The other entries in `git status` were present before this audit began and are unchanged by it: `Main-Planing.md`, `Planing-Ledger.md`, `Project-Ontology.md`, `Sub-Planing-Index.md`, `Faz7.2` and `Faz8.2` modified; `Faz7.1-wsl2-provisioning.md` and `Faz8.1-beryl-port-sizing.md` deleted; four new Phase 7/8 sub-plans and `devir-teslim-promptu.md` untracked. They are the uncommitted output of planning runs 17 and 18.
- **Step 4 can safely begin**, at `Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md`. The P2 repair notes must be honoured at the rows they name, and the bounded Step 2 amendment should land before `Faz7.3`.
