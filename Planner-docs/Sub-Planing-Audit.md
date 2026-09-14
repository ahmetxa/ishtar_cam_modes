# Sub-Planing Audit

> Step 3 audit — ClaudeQB. Body language: English (default contract).
> The project's user-facing documents and module interface remain Turkish and English; that convention is unchanged.
>
> **This is the tenth audit (2026-09-13).** It supersedes the ninth audit (2026-09-11) and is step 3 of `docs/pre-rental-plan.md`. Since the ninth audit, four things happened:
>
> - `IMPL-91` verified `Faz7.1` and wrote `docs/build-environment.md`.
> - `IMPL-92` ran `Faz8.1`'s static half.
> - `IMPL-93` verified `Faz8.2`.
> - Planning run 19 amended `Faz7.2`, `Faz7.3`, `Faz8.1`, `Faz8.3`, index sections 4d, 5 and 7, and the ledger.
>
> **This audit exists because run 19's ledger row and index paragraph both say `Faz7.2`, `Faz7.3` and `Faz8.3` may not enter the Step 4 queue until Step 3 has read the amendment.**
>
> **Active snapshots: `SNAP-2026-09-10-MAIN` and `SNAP-2026-09-10-SUBPLANS`. The sub-plan set is 42.** Run 19 cut no snapshot. By the precedent of planning runs 13 to 15 that is correct: the amendment was bounded, and no phase was re-decomposed.

## 1. Audit Summary

**Overall audit status: PASS_WITH_WARNINGS.**

**Run 19 discharged every finding it was sent to fix, in the sections Step 4 is graded against.** Eight are resolved:

- `AUDIT-FIX-43`: billing and deletion semantics.
- `AUDIT-FIX-44`: install artifacts retrieved before teardown.
- `AUDIT-FIX-45`: data format and the re-established return path.
- `AUDIT-FIX-46`: sensor adaptation routed like re-derivation.
- `AUDIT-FIX-47`: scratch outside the workspace, and the static-half boundary.
- `AUDIT-FIX-48`: the index's line-ending sentence.
- `AUDIT-FIX-49`: the `IMPL-89` annotation, and both Android 15 candidates named.
- `AUDIT-FIX-51`: init service names, and "switch has no effect" as a failure signal.

`AUDIT-FIX-50`'s sub-plan half is resolved. Its document half is open, narrowed to `docs/release-checklist.md` and owned by `F8.3-08`. No P0 or P1 is open.

**`Faz7.2` now matches the runbook and GitHub, and this audit measured that rather than reading it from the plan.**

- **Manifest.** `ahmetxa/android_local_manifests` `main` is `22283d8a866d042e02336fcb4698253ac6bf9c3b`. Its tree is `README.md`, `check.py`, `ishtar-beryl.xml` and `tests/`. `ishtar-beryl.xml` carries 13 `project` lines, 14 `remove-project` lines (13 barista entries, plus one path pinned from another source), and `clone-depth="1"` on the three blob repositories.
- **Repositories.** Both `ahmetxa` repositories read `private=false`, and the device tree's `beryl` branch is `d48816f`.
- **Runbook section 5, run live today in this audit's scratchpad as written.** It exited 0 with "pre-rental checks passed": every pin resolved, and the known-bad cases produced exactly `14 element(s) failed`.
- **Base manifest.** `AOSPA/manifest` `beryl` is still `7dfc0650…`, last committed 2026-05-24.
- **Build command.** `./rom-build.sh ishtar -z` is real. `AOSPA/manifest` `aospa.xml:120` links `vendor/aospa` `build.sh` to `rom-build.sh`. `build.sh` defaults `BUILD_TYPE="userdebug"`, and `-z` runs `ota_from_target_files` and `img_from_target_files` from `$OUT/obj/PACKAGING/target_files_intermediates/aospa_$DEVICE-target_files.zip` into `aospa-$AOSPA_VERSION.zip` and `aospa-$AOSPA_VERSION-image.zip` at the source root. That is exactly runbook sections 1, 9 and 11.
- **Credentials.** Under `DEC-25` the server needs none: the plan's scope, `F7.2-03`, `F7.2-09` step 7 and `VAL-TEARDOWN` all say so.

**Both user rulings recorded in run 19 are sound.**

- **The fix rule** is a server edit, recorded in `fixes.diff`, landed on GitHub after the session. It keeps push approvals off the billing clock. It is also not lossy: `fixes.diff` lives in `~/evidence`, which runbook section 10 packs into the retrieved `evidence.tar.gz`, and `F7.2-10` routes it through `check.py` and the user's push before any second rental.
- **The symlink ruling** holds against the build system itself, not only against the project's documents. AOSPA `tools/extract-utils` `beryl` `extract_utils/makefiles.py` `write_symlink_package` splits the `SYMLINK=` value into partition and location, and emits `install_symlink` with `installed_location` and `symlink_target = '/' + file.dst`. For `refs/a16_ishtar/proprietary-files.txt:1037` that is partition `vendor`, location `lib64/camera/aon_front.pb`, and target `/odm/lib64/camera/aon_front.pb`. Runbook section 10 lines 282–285 still test the `odm` path and would print "NOT a symlink" on a correct build. The runbook is still uncorrected, which is correct: that edit is `F7.2-01`'s, in Step 4.

**Of the three recorded readings, two are sound as written and one is sound but collides with a precedence sentence.**

- **`F7.3-01` writing re-establishment steps when AOSPA is silent: sound.** It costs a written procedure, and `F7.3-07` executes it only if `/data` was actually formatted.
- **PC-17 graded on the two mount counts: correct, and it corrects the ninth audit's own wording.** `docs/release-checklist.md:248` defines PC-17 as `hal.mount.count` and `sensor.mount.count`, and lines 286–287 say those fields were never defective.
- **`F7.2-04` applying the deferred-items fixes to the two sync-path detectors: the right reading.** Otherwise two rows of the runbook's own table are dead text. **But runbook section 4 literally says "Sync failure … stop", and `Faz7.2` section 1 says that where the plan and the runbook disagree, "Step 4 follows the runbook".** A rental-day session holds two instructions that contradict each other. That is new finding `AUDIT-FIX-52` (P3), repairable in the same pre-rental runbook edit as the symlink test.

**Most important finding: `AUDIT-FIX-52` (P3), the sync-failure precedence clash above.** No P2 is new. The only open P2 is the carried `AUDIT-FIX-22`.

**Most important remediation action:** in `F7.2-01`, before renting, make the runbook agree with the plan in one reviewed edit. Correct the section 10 symlink path, add the sync-path exception to section 4 (`-52`), and add a free base-pin read to section 5 (`-53`). Then run `bash -n` on the touched blocks and stop for the user's rental approval.

**Step 2 output is usable for Step 4.** **Queue head: `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md`, starting at `F7.2-01`.** The queue behind it is `Faz7.3`, `Faz8.1`'s agreement half, then `Faz8.3`.

## 2. Reviewed Sources

**Files inspected.**

- **Planning run 19's four sub-plans.** `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md`, `Faz7.3-flash-boot-and-aon-verification.md`, `Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md` and `Faz8.3-camera-modes-on-android16-build.md` were each read in full. Sections 4, 7, 8, 9 and 13 were checked finding by finding against the ninth audit's required actions and against the repository.
- **`Planner-docs/Sub-Planing-Index.md`.** Run 19's `git diff` was read: section 4d, section 5's new deferred item, the line-357 correction, and the tenth re-plan paragraph.
- **`Planner-docs/Planing-Ledger.md` (CRLF, long lines), through a truncating UTF-8 extractor.** Read: the section headings; the section 2 run 19 row, including its readings; rows `IMPL-89` (with the run-19 annotation), `IMPL-91`, `IMPL-92` and `IMPL-93`; the whole section 4 matrix by status column; the section 3 snapshot registry; and the `DEC-07`, `DEC-08`, `DEC-22` and `DEC-25` rows.
- **The ninth `Planner-docs/Sub-Planing-Audit.md`**, read in full before overwriting, so that finding IDs continue from `AUDIT-FIX-51`.
- **`docs/build-environment.md`, read in full.** It is the rental runbook, and `Faz7.2` defers to it.
- **`docs/pre-rental-plan.md`**, the operator plan whose step 3 this is.
- **Repository evidence re-measured this run:**
  - `refs/a16_ishtar/proprietary-files.txt:1035-1039` and `device_ishtar/proprietary-files.txt:1031`;
  - `refs/a16_ishtar` HEAD `df05661`;
  - `refs/a16_sm8550/BoardConfigCommon.mk`: `odm` in `AB_OTA_PARTITIONS` (line 16), and `TARGET_COPY_OUT_ODM := odm` (line 120);
  - `docs/aon-verification.md` lines 186, 217–218 and 239;
  - `docs/release-checklist.md` lines 135, 148, 176, 248, 277–297 and 318;
  - `scripts/smoke.sh` lines 81, 94, 128 and 130;
  - `ishtar-cam-modes/setmode.sh` lines 52–58, 79–83 and 110–114;
  - `Main-Planing.md` lines 22, 61, 277 and 288;
  - `Faz1.3` line 9, and `Faz3.8` lines 120 and 163.
- **Supporting files.** `Planner-docs/Project-Ontology.md`: a byte-level control-character scan and `IMPL-52`/`-53`/`-54` counts. `Planner-docs/Project-Comprehension.md`: `IMPL-52`/`-53`/`-54` counts.

**Folders inspected.** `Planner-docs/`, all nine `Faz-<n>-Plans/` folders, `docs/`, and the repository through `git`.

**Important commands run.**

- `git status --short`, `git log --oneline -4`, `git rev-list --left-right --count origin/main...main` (0 behind, 2 ahead), and `git diff --stat` in two scopes:
  - the working tree: run 19 is **uncommitted**, six files;
  - `097d687..HEAD` on `Planner-docs/`: empty, so `d3993de` touched no planner file.
- `git diff --stat HEAD` on `Main-Planing.md`, `Project-Ontology.md`, `Project-Comprehension.md`, `Faz7.1` and `Faz8.2`: all unchanged.
- The bundled validator at the installed plugin path, in `--mode step3-preflight --strict` and `--mode step2 --strict` before writing, and in `--mode step3 --strict` and `--mode step4 --strict` after. `python` is 3.14.7.
- A Python structure checker over all 42 sub-plans. It checks:
  - the filename regex, and folder/filename/H1 agreement;
  - the 13 headings in order;
  - the shortest section body;
  - placeholder tokens;
  - the Implementation Contract header and path safety;
  - control bytes and CRLF;
  - per-phase numbering contiguity;
  - index references in both directions;
  - the line endings of the seven top-level planner files.
- **Runbook section 5's scripted block, executed verbatim** in this session's scratchpad (`TMPDIR` pointed there), with `GH` set to the WinGet `gh.exe`. Exit 0.
- Read-only `gh api` calls:
  - `ahmetxa/android_local_manifests`: commits, visibility, the tree at `22283d8`, and the raw `README.md`, `ishtar-beryl.xml` and `check.py`;
  - `ahmetxa/android_device_xiaomi_ishtar`: visibility and the `beryl` head;
  - `AOSPA/manifest`: `beryl` commits, the tree, and raw `default.xml` and `aospa.xml`;
  - `AOSPA/android_vendor_aospa` `beryl`: raw `build.sh`;
  - `AOSPA/android_tools_extract-utils` `beryl`: the tree, a `SYMLINK` scan of its `.py` files, and `extract_utils/makefiles.py` lines 590–640.

  No write, and no clone into the workspace.

**Things not verified.**

- **The 38 sub-plans run 19 did not touch were not re-read for content.** `git diff --stat` shows `Faz7.1` and `Faz8.2` unchanged since the ninth audit read them. Both are now `verified` (`IMPL-91`, `IMPL-93`), and their measurements were taken as reported. The other 36 carry earlier audits' assessments. All 42 passed the structure checker.
- **Whether `repo manifest -r` aborts on a partially synced tree** (`AUDIT-FIX-54`). This was reasoned from `repo`'s behaviour, not run.
- **AOSPA's data-format requirement, the firmware `beryl` needs, the vendor repository in the `vauxite` beans, and the Android 16 init service names.** Each belongs to the work item that names it.
- **Device state.** No `adb` command was run.
- **Hetzner Console state.** Limits, the SSH key and prices are the user's checks in `F7.2-01`.

No secret value was read or recorded. `secret_findings=0` in every validator mode run.

## 3. Main Phase Coverage Analysis

| Main phase no | Main phase heading | Expected folder | Folder exists? | Sub-plan count | Coverage status | Notes |
|---|---|---|---|---|---|---|
| 1 | Workspace safety net | Planner-docs/Faz-1-Plans/ | Yes | 6 | OK | All six `verified`. |
| 2 | Ship and re-baseline v2.1 | Planner-docs/Faz-2-Plans/ | Yes | 4 | OK | All four `verified`. |
| 3 | AGC stable at 12.6 MP under 50 MP | Planner-docs/Faz-3-Plans/ | Yes | 11 | OK | All eleven `verified`; phase marked successful (`DEC-21`). |
| 4 | Minimal correct HAL patch | Planner-docs/Faz-4-Plans/ | Yes | 7 | OK | `Faz4.2`–`4.5` `verified`; `Faz4.1`, `Faz4.7` `superseded`; `Faz4.6` `DEFERRED`. |
| 5 | Mode-0 12-bit composition | Planner-docs/Faz-5-Plans/ | Yes | 3 | OK | All three `verified`. |
| 6 | AON fix upstreaming | Planner-docs/Faz-6-Plans/ | Yes | 2 | OK | `Faz6.2` `verified`; `Faz6.1` `implemented`, effect verification owned by `Faz7.3` `F7.3-08`. |
| 7 | Android 16 build environment | Planner-docs/Faz-7-Plans/ | Yes | 3 | OK | `Faz7.1` `verified` (`IMPL-91`). `Faz7.2` (paid build) and `Faz7.3` (flash and boot) amended by run 19 and queued. |
| 8 | Camera work on Android 16 + kernel LTS | Planner-docs/Faz-8-Plans/ | Yes | 3 | OK | `Faz8.1` `implemented` (static half, `IMPL-92`: both layers carry-over on static values). `Faz8.2` `verified` (`IMPL-93`, `DEC-08` recommendation defer). `Faz8.3` queued. **The ninth audit's WARNING is lifted:** index section 5 now defers sensor adaptation beside HAL re-derivation, and `Faz8.1`/`Faz8.3` block on anything but carry-over, so no acceptance branch is referenced without an owner. The deliberately undecomposed branches (re-derivation, kernel merge) stay routed to `DEC-07`/`DEC-08`. |
| 9 | Release engineering | Planner-docs/Faz-9-Plans/ | Yes | 3 | OK | All three `verified`. |

The validator reports `main_phase_count=9` and `phase_folder_count=9`. There is no missing phase and no extra folder. Per-phase counts, measured this run: **6, 4, 11, 7, 3, 2, 3, 3, 3 — total 42.**

## 4. Sub-Plan File Inventory

Structure was checked programmatically on **all 42** files. Every H1 matches `# Faz <phase>.<sub> — ` and agrees with its folder and filename. Content was assessed this run for the four files run 19 amended. `Faz7.1` and `Faz8.2` are unchanged since the ninth audit's content read and are now verified. The other 36 carry earlier assessments.

**Planner-docs/Faz-7-Plans/** (3 files).

- `Faz7.1-github-input-staging.md` — `# Faz 7.1 — GitHub Input Staging and Pre-Rental Readiness`. Phase match OK, structure OK. **`verified` by `IMPL-91`.** Its outputs were re-measured on GitHub this run: manifest `22283d8`, public repositories, `check.py` resolving, and the negative cases failing 14. Content not re-assessed; unchanged.
- `Faz7.2-first-aospa-build.md` — `# Faz 7.2 — First AOSPA beryl Build on a Rented VDS`. Phase match OK, structure OK. **Content: strong, and now executable against the runbook.**
  - **Section 1** records four gone premises, the runbook's precedence, the two user rulings, and that no work item was added or removed. The last is true: `F7.2-01` to `F7.2-10` are unchanged in number.
  - **Section 6's values match GitHub and the runbook, measured this run:** `22283d8`, 13 pins, the base `7dfc0650…`, `rom-build.sh`, the section 11 table, and the `;SYMLINK=` lines 1037 and 1031.
  - **Sections 7, 8, 9 and 13 carry `AUDIT-FIX-43`** (deletion, never shutdown, and the Primary IP) **and `-44`** (every section 11 artifact with sha256 at both ends, or its extraction source recorded) **as criteria, not advice.**
  - **Notes.** `AUDIT-FIX-52`: sync-failure precedence, and `VAL-SYNC` against a `fixes.diff`-amended pin set. `AUDIT-FIX-53`: base pin not read before renting. `AUDIT-FIX-54`: the runbook's fail-fast blocks versus "recorded, not fatal".
- `Faz7.3-flash-boot-and-aon-verification.md` — `# Faz 7.3 — Flash, Boot and AON Verification on the Device`. Phase match OK, structure OK. **Content: strong.**
  - `F7.3-01` records the data requirement both ways, with sources, and writes the four re-establishment steps when a format is required or the requirement is unsettled.
  - `F7.3-02` states the wipe.
  - `F7.3-07` and its criterion grade against the re-established fields, by name: `agc.pref_48m = 0`, `agc.pref_resolution = full`, `agc.photo_size.back.derived = 4096x3072` and `prefs.trap.armed = 0`. A field "the format erased does not pass as an explained difference".
  - Install artifacts are taken from runbook section 11, not re-researched.
  - **Notes.** `AUDIT-FIX-37`: `Faz7.3` writes `Project-Comprehension.md`. One wording gap, carried in section 12 rather than raised as a finding: `F7.3-02` says "Where a format is required, state plainly …", but section 8 also covers the unsettled case. The go/no-go should state the possible wipe whenever `F7.3-01` wrote re-establishment steps.

**Planner-docs/Faz-8-Plans/** (3 files).

- `Faz8.1-android16-camera-blob-comparison.md` — `# Faz 8.1 — Android 16 Camera Blob Comparison and Carry-Over Decision`. Phase match OK, structure OK. **Content: strong.**
  - Adaptation is routed like re-derivation (`F8.1-08`/`-09`), and `Faz8.3` can consume only carry-over.
  - Scratch is outside the workspace and deleted at `F8.1-05`, with `VAL-CLEAN` at two points.
  - `F8.1-04` names `xiaomi-8550/…ishtar` `vauxite` and `ThankYouMario/…ishtar` `vauxite`, and decides from the `vauxite` beans.
  - `IMPL-92` is recorded "as written", and section 1 states that the amendment changes text, not the record. This is the right way to amend a partly executed plan.
  - **Notes.** `AUDIT-FIX-22`: `F8.1-10` writes the ontology.
- `Faz8.2-kernel-lts-merge-scoping.md` — `# Faz 8.2 — Kernel LTS Merge Scoping`. Phase match OK, structure OK. **`verified` by `IMPL-93`.** Unchanged since the ninth audit; not re-assessed.
- `Faz8.3-camera-modes-on-android16-build.md` — `# Faz 8.3 — Camera Modes on the Android 16 Build`. Phase match OK, structure OK. **Content: strong.**
  - The gate requires carry-over on both layers.
  - `F8.3-05` and `VAL-RESTART` list the Android 16 init service names against `setmode.sh`'s three, and count "a mode switch with no effect" beside black preview. This matches `setmode.sh:52-58` and `:110-114` as measured.
  - PC-04 uses the single-dump probe, with the substitute as a cross-check. The trap reading uses `prefs.trap.armed`, and PC-17 the two mount counts.
  - `F8.3-08` corrects the checklist labels in the same edit as the evidence record.
  - **Notes.** `AUDIT-FIX-50`: document half, owned by `F8.3-08`.

**All other phase folders** (`Faz-1-Plans` 6, `Faz-2-Plans` 4, `Faz-3-Plans` 11, `Faz-4-Plans` 7, `Faz-5-Plans` 3, `Faz-6-Plans` 2, `Faz-9-Plans` 3). Every file passes on filename, phase match, section structure and Implementation Contract, with no thin or placeholder section. Content status comes from the ledger (section 12). Carried residues: `Faz1.3` (`AUDIT-FIX-25`, accepted) and `Faz3.8` (`AUDIT-FIX-33`, accepted).

## 5. Naming and Sequencing Check

**No naming or order issues were found.**

- **Folder naming:** all nine match `Faz-<n>-Plans/`.
- **Filename naming:** all 42 match `Faz<phase>.<sub>-<ascii-kebab-slug>.md`, with no spaces, no non-ASCII characters and no duplicates.
- **Numbering:** contiguous from 1 in every phase, measured. Run 19 created, deleted and renamed nothing.
- **Agreement:** folder, filename and H1 agree in all 42.
- **Order:** the phase order matches `Main-Planing.md` section 6. Execution order within Phases 7 and 8 differs from numbering by design, per index amendment 4d. `Faz8.1`'s static half ran before `Faz7.2`, as `IMPL-92`. Index 4d now defines that half exactly as `Faz8.1` section 10 does (`F8.1-01`–`05` plus `08`/`09` on static values), so the boundary slip of `AUDIT-FIX-47` is closed.

## 6. Index Consistency Check

- **Missing, broken or unindexed references: none.** All 42 are referenced, in both directions, and `index_reference_count=42`.
- **Phase count:** nine in the index, the master plan and the folders.
- **Coverage claims: honest.** The ninth audit's one byte-level error is corrected at line 357. The old sentence is struck through, and the correction reads "all 42 sub-plans and this index are LF-only". Measured this run, that holds: all 42 sub-plans, the index, the ontology, the comprehension file and the audit are LF, while `Main-Planing.md`, `Planing-Ledger.md` and `Autopsy.md` are CRLF.
- **Execution order: plausible.** Step 2 of amendment 4d records `IMPL-92`, and step 6 now reads "only when both layers are carry-over". The sequencing paragraph adds that a sensor adaptation label also blocks `Faz8.3`. Section 5 gains the matching deferred item, which notes that `IMPL-92` found the sensor unchanged on static values.
- **Run 19's paragraph is accurate against what this audit measured:**
  - files and sections written;
  - no snapshot cut;
  - two rulings and three readings;
  - findings left untouched;
  - what was not verified;
  - validator results.

  One small imprecision, not a finding: it lists `-50`'s document half as "routed to `F8.3-08`", and `F8.3-08` does now carry it (section 7, and the contract table's `docs/release-checklist.md` row).
- **Carried residue.** The index's three-field description of `Faz3.8` is unchanged (`AUDIT-FIX-33`, accepted). Run 19's diff did not touch it.

## 7. Required Section Structure Check

Checked programmatically on **all 42** sub-plans, not sampled.

- **Missing, duplicated or out-of-order sections: none.** Every file carries the thirteen required headings in order.
- **Empty sections: none.** The shortest section body across all 42 is 175 characters (`Faz6.1` section 2), unchanged. Run 19's four files are all above that.
- **Placeholder sections: none.** There is no `TODO`, `TBD`, `FIXME` or `XXX` token.
- **Title, filename and folder: all 42 agree.**
- **Implementation Contract tables:** present in all 42, with repo-relative paths and no absolute or `..` path. Run 19's tables:
  - **`Faz7.2`** marks `docs/build-environment.md` `modified`, for the `F7.2-01` correction and post-session deviations, and `.gitignore` `existing` with the reason no `*.img` rule is needed.
  - **`Faz7.3`** adds `docs/build-environment.md`, `docs/release-manifest.md` and `docs/agc-12mp-configuration.md` as `existing`.
  - **`Faz8.3`** marks `docs/release-checklist.md` `modified` for `F8.3-08`.

  **Each named edit has a matching work item, and each work item's edit is in its table.**
- **Control characters and encoding: none in any sub-plan.** All 42 are valid UTF-8 and LF-only.

`--mode step2 --strict` and `--mode step3-preflight --strict` both report `error_count=0`, `warning_count=0`, `subplan_count=42`, `index_reference_count=42`, `phase_folder_count=9`, `main_phase_count=9` and `secret_findings=0`.

## 8. Content Quality and Implementability Analysis

**Discharge check, required action by required action, in sections 4, 7, 8, 9 and 13.**

| Finding | Required action (ninth audit) | Where run 19 put it | Verdict |
|---|---|---|---|
| `AUDIT-FIX-43` | Billing and deletion semantics sourced and used by teardown and budget | Runbook section 3 (`IMPL-91`); `Faz7.2` section 4 teardown bullets, `F7.2-09` steps 2–5 and 7, section 8 "deleted, not shut down … zero Primary IPs", `VAL-TEARDOWN`, section 13 first bullet | resolved |
| `AUDIT-FIX-44` | Every install artifact named and retrieved with sha256 before deletion, or extraction recorded | Runbook section 11 table; `F7.2-08` (assertions, optional target-files, "not retrieved: name each … with the package"), section 8 criterion, `VAL-RETRIEVE`, section 13 `Faz7.3` bullet; `Faz7.3` section 6 table, `F7.3-02`/`-03` | resolved |
| `AUDIT-FIX-45` | Data requirement both ways; re-establishment path; wipe stated at go/no-go; restore graded on re-established state | `F7.3-01` (steps 1–4), `F7.3-02`, `F7.3-07`, section 8 restore criterion with named fields, `VAL-PREFLASH`, `VAL-RESTORE`, section 13 third bullet | resolved |
| `AUDIT-FIX-46` | Adaptation routed like re-derivation; gates require sensor carry-over; index section 5 defers adaptation | `F8.1-08` "Only carry-over is a label `Faz8.3` can consume", `F8.1-09` adaptation branch, `Faz8.1` section 8 and 13; `F8.3-01`, `Faz8.3` section 8 first criterion, section 13 last bullet; index section 5 | resolved |
| `AUDIT-FIX-47` | Scratch outside the workspace, deleted at end of static half; index 4d boundary aligned | `Faz8.1` section 4, 5, `F8.1-01`, `F8.1-05` deletion, `F8.1-10`, section 8 last criterion, `VAL-CLEAN` at two points, section 13 last bullet; index 4d step 2 | resolved |
| `AUDIT-FIX-48` | Index line-ending sentence corrected to LF | Index line 357, struck and corrected | resolved |
| `AUDIT-FIX-49` | `IMPL-89` annotated; both candidates named in `F8.1-04` | Ledger line 517 "[corrected by `IMPL-90`; annotated 2026-09-13 by planning run 19 …]"; `F8.1-04`, `Faz8.1` section 4, 6, 8 | resolved |
| `AUDIT-FIX-50` | PC-17 on `prefs.trap.armed`, PC-04 on repaired probe; checklist labels updated by Step 4 | `F8.3-06`, `Faz8.3` section 8, `VAL-CHECKLIST`, risk row; `F8.3-08` labels edit. **PC-17 corrected to the mount counts** (see section 9) | sub-plan half resolved; document half open, owned by `F8.3-08` |
| `AUDIT-FIX-51` | `VAL-RESTART` lists `init.svc.*`; "switch has no effect" is a failure | `F8.3-05`, `VAL-RESTART`, `Faz8.3` section 8 invariant-3 criterion, section 11 first risk, section 6 | resolved |

**The amendment style is good.** Each file opens with a dated note naming its drivers and says whether a work item was added (none was). `Faz8.1` states plainly that the executed record stands and only the text changes. `Faz7.2` gives the runbook precedence and says what to do on disagreement: follow the runbook and record it. That sentence is what makes `AUDIT-FIX-52` visible.

**Implementability of the queue head.**

- **`F7.2-01` is a free, well-bounded slice.** Its first command was already run by this audit and passes today. Its correction is one test path plus one echo string.
- **The paid slices `F7.2-02`–`09` map one-to-one onto runbook sections 6–12.** The stopping rule — at most 2 manifest-class attempts, and hour 8 means retrieve and delete — is stated in sections 3, 7 and 11.
- **The fastest signal is well chosen:** a completed sync at the two pinned commits.

**Three precision gaps remain in `Faz7.2` and its runbook.** None changes the design, and each is cheapest to close in `F7.2-01`, before money is spent.

1. **`AUDIT-FIX-52`: sync-failure precedence.**
   - Runbook section 4's bullet "Sync failure (`repo sync`, or barista's …): stop" contradicts its own table, whose shallow-sync and `vendor/xiaomi/camera` rows name sync failures with a fix.
   - `F7.2-04` resolves this toward the table, counted against the 2 attempts, while `Faz7.2` section 1 says the runbook wins on disagreement.
   - `VAL-SYNC` and the section 8 criterion also compare `manifest-resolved.xml` against the 13 pins "at `22283d8`". After a permitted fix — for example deleting `clone-depth`, or the `vendor/xiaomi/camera` lines — the right reference is `22283d8` as amended by `fixes.diff`.
2. **`AUDIT-FIX-53`: base pin read too late.** The base `7dfc0650…` is first asserted in section 8, after the server bills. Section 5 does not read it. It has not moved since 2026-05-24, but checking it costs one free `gh api` call on the day.
3. **`AUDIT-FIX-54`: fail-fast blocks versus "recorded, not fatal".** Runbook sections 10 and 11 run under `set -euo pipefail`, but both the runbook and `F7.2-07`/`-08` promise that a missing file is recorded, not fatal. Two lines would abort anyway:
   - **Section 10's first command, `repo manifest -r`.** It plausibly fails on a tree where `repo sync` stopped partway. The block would then exit before `build-evidence.txt`, the log tails and `evidence.tar.gz` exist, which are the evidence `F7.2-05` requires "whatever the build outcome".
   - **Section 11's `cp "$OUT/$i.img"` loop** stops on the first absent image, before `SHA256SUMS` is written, where `F7.2-08` expects that absence to be recorded.

**Vibecoding and fresh-session quality.** Slices are small and ordered cheapest-failure-first. Token risk is banded, medium rising to high on repeated build failure, with the mitigation named: per-stage status lines, never whole logs. Subagents are marked not recommended in all four files, with reasons: one stateful server, and one device. Each queued file states outcome, validation, boundaries and stop conditions.

## 9. Scope Drift and Architectural Consistency Analysis

**No scope drift.** Run 19 added no phase, no sub-plan and no work item. `Main-Planing.md`, `Project-Ontology.md`, `Project-Comprehension.md`, `Faz7.1` and `Faz8.2` are unchanged (`git diff --stat HEAD`). No snapshot was cut, by the precedent of runs 13 to 15, and the ledger states that decision explicitly.

**Judgement of the two user rulings.**

1. **Fix rule (server edit → `fixes.diff` → GitHub after the session): sound.**
   - It replaces a rule that would have spent the user's push approval, and minutes of billed time, in the middle of a paid session.
   - Reproducibility is preserved. The build's inputs are `22283d8` plus a retrieved diff, the ledger row records both (runbook section 13, `F7.2-10`), and the diff is re-checked with `check.py` before it lands.
   - `Faz7.2` section 5 excludes pushing during the session, and section 8 grades it ("no fix was pushed during the session").
   - One consequence the plan already covers: the runbook's manifest commit must be updated after the diff lands (`F7.2-10`).
2. **Section 10 symlink test: sound, verified at the build-system level.**
   - `AOSPA/android_tools_extract-utils` `beryl` `makefiles.py` `write_symlink_package` emits an `install_symlink` module on the partition named by the value's first path segment (`vendor`), at `installed_location` `lib64/camera/aon_front.pb`, pointing at `/` plus the blob's destination (`/odm/lib64/camera/aon_front.pb`).
   - `TARGET_COPY_OUT_ODM := odm` confirms that `$OUT/odm/…` is the regular file.
   - `docs/aon-verification.md:217-218` expects exactly this on the device.
   - The runbook's lines 282–285 still test the `odm` path. `F7.2-01`'s correction is right, and `bash -n` on the edited block is the correct gate.
   - **Recommended in `F7.2-01`: change the `else` message too, so it names the `vendor` path, and record the expected `readlink` value (`/odm/lib64/camera/aon_front.pb`) in the gate record.** That way a wrong target is not read as a pass.

**Judgement of the three recorded readings.**

1. **`F7.2-04` (deferred-items fixes for the two sync-path detectors): the correct reading, but not yet consistent with the precedence sentence.**
   - Read literally, the runbook forbids the fixes its own table lists for sync failures.
   - The manifest `README.md` item 7 names the shallow-sync fallback as a sync-time remedy, and a failed `vendor/xiaomi/camera` sync can only surface at sync time.
   - The attempts stay capped at 2, and hour 8 still bounds the cost.
   - The residual problem is documentary (`AUDIT-FIX-52`, P3): make the runbook say it.
2. **`F7.3-01` (re-establishment steps when AOSPA's documentation is silent): sound.** Unsettled evidence is treated as the worse case for a written plan and the better case for execution: steps are written, and run only if `/data` was actually formatted. `Faz7.3`'s section 8 criterion states this. The only gap is `F7.3-02`'s wording (section 4 above).
3. **PC-17 graded on the mount counts, with the trap reading on `prefs.trap.armed`: correct, and it corrects this audit series.**
   - `docs/release-checklist.md:248` defines PC-17 as "`hal.mount.count` and `sensor.mount.count` must each read …", and lines 286–287 say those two fields are computed separately from the trap probe that was defective.
   - The ninth audit's required action ("grade PC-17 on `prefs.trap.armed`") conflated the row with the probe it shares a block with.
   - Run 19 checked the checklist instead of copying the audit, which is what the pre-rental plan's rule required ("checked against the repository before it is written").

**Ontology consistency.** `beryl` is a branch throughout. Invariant 10 underlies `Faz7.2`'s post-build md5 read, `Faz7.3`'s on-device read and `Faz8.1`'s agreement half. Invariant 3 underlies `F8.3-05`. *Stock* is kept distinct in `Faz7.3` and `Faz8.1`.

**Planning-ledger continuity: good, and the one unreconciled contradiction is closed.**

- **`AUDIT-FIX-49`.** `IMPL-89`'s row now carries the correction inline, and `IMPL-90` and `IMPL-92` agree with it.
- **Matrix status labels are honest and consistent with the repository.**
  - `Faz7.1` and `Faz8.2` are `verified`.
  - `Faz8.1` is `implemented`, with the agreement half named as pending.
  - `Faz7.2`, `Faz7.3` and `Faz8.3` are `planned`, each waiting on this audit.
  - `Faz6.1` stays `implemented` until `Faz7.3`.
- **Section 4's next actions for `Faz7.2` match `docs/pre-rental-plan.md` step 4.**

**Master plan residues outside any run's mandate: unchanged** (`AUDIT-FIX-41`, `-42`). Lines 22, 61, 277 and 288 read exactly as the ninth audit quoted them. No queued row reads those lines; each quotes the corrected Phase 7/8 text.

## 10. Readiness Realism

**No overclaim was found in run 19's text.**

- **`Faz7.2`** calls the outcome "built, partial or blocked", keeps post-build md5s "as facts, not conclusions", and says the section 11 table is what "the install needs" — not that the build will produce it. The optional target-files archive is labelled optional.
- **`Faz7.3`** keeps camera enumeration a fact, not a pass condition. Its restore criterion is now attainable in both cases, preserved or re-established.
- **`Faz8.1`** separates what `IMPL-92` measured ("carry-over on static values") from what still waits (the agreement half). No section calls the classification closed.
- **`Faz8.3`** states that md5 agreement proves only input identity.

**Status labels match evidence.** The ledger keeps `Faz8.1` at `implemented`, not `verified`, because `F8.1-06`/`-07` have not run. That is the correct reading of a half-executed sub-plan.

**Local versus live is drawn correctly.**

- **Local:** runbook section 5, which this audit ran. It is repeatable on the day and is not a rental-readiness claim by itself; the Console checks remain the user's.
- **Live:** the rented server, and then the device.

**One realism note on the pre-rental gate (`AUDIT-FIX-53`).** Section 5 passing proves the local manifest resolves. It does not prove that `repo init` will land on `7dfc0650…`, which is what section 8 asserts on a billed server.

## 11. Security and Governance Findings

- **Secret safety: clean.**
  - `secret_findings=0` in every validator mode.
  - No token, password, private key or server address appears in any planner file.
  - `DEC-25` removes the server credential entirely, and `Faz7.2` excludes any token or deploy key.
  - The runbook keeps the address in `read -r BUILD_HOST`, and removes it at teardown with `ssh-keygen -R` and `unset`.
  - Runbook section 10's credential-URL check and token scan run before copying, and `VAL-SEC`'s host scan is file-name-only.
  - The ninth audit's residual note about tokens in clone URLs no longer applies: no token exists.
- **Least privilege: improved.** There is no GitHub credential on the server at all. The only secrets involved are the user's Hetzner session and SSH private key, and both stay on the host.
- **Command execution safety.**
  - Every runbook block starts with `set -euo pipefail`.
  - The unchecked barista exit status is caught by a log grep (section 9).
  - `repo` is installed with a GPG signature check (section 7).
  - The build runs as `builder`, not root.
  - **The one weakness is the inverse of the `IMPL-90` defect class:** fail-fast lines where the plan wants best-effort evidence (`AUDIT-FIX-54`). It fails safe for correctness, but it can cost evidence.
- **Artifact integrity: good.** sha256 is checked at both ends, and teardown is gated on `sha256sum -c`. `F7.3-03` flashes only verified artifacts, and `Faz8.3` checks the archive sha256 before a root-privileged install. `Faz8.1` scratch is outside the workspace.
- **Blob redistribution: held.** Outputs go to `~/Documents/Projeler/ishtar-builds/`, outside every repository, and `VAL-RETRIEVE` reads `git status`. Nothing is published (`ARC-04`).
- **Approval gates: complete.** They are the Console checks, renting, deletion, a post-session push of `fixes.diff`, the flash, firmware, the stay-or-restore choice, root, install, captures and `DEC-07`.
- **Irreversible operations.**
  - Server deletion is gated on verified retrieval.
  - The whole-system flash is gated on a written return path that includes re-establishment after a format.
  - The billing semantics the ninth audit found missing are now sourced (runbook section 3).
- **Ontology writes into a NUL-bearing file (`AUDIT-FIX-22`).** This is still true: 7 control bytes, 2 NUL. `IMPL-91` edited the file byte-preservingly: the offsets moved by +216 and the count is unchanged. `F8.1-10` is now the only queued writer.
- **Audit boundary.** No P1 was found, and this audit repaired nothing. All findings are routed.

## 12. Step 4 Readiness Assessment

**Conventions.** Dependency state follows the nine previous audits:

- `independent` means no upstream dependency.
- `satisfied` means every upstream dependency is complete in the repository, or is produced by an earlier row of this queue.

Queued rows appear in execution order. `Faz8.1` appears once, after `Faz7.3`. Its `F8.1-06` may run as soon as `Faz7.2` has recorded the post-build md5s, and `F8.1-07` after `Faz7.3`.

**What changed since the ninth audit.** `Faz7.1` (`IMPL-91`) and `Faz8.2` (`IMPL-93`) are `verified`, so both move to `COMPLETE`. `Faz8.1`'s static half is done (`IMPL-92`), so its row stays queued for the agreement half. `Faz7.2`, `Faz7.3` and `Faz8.3` were amended by run 19, read by this audit, and stay queued.

**Counts, measured from the ledger matrix:**

| Category | Rows |
|---|---|
| Queued | 4 (0 `READY`, 4 `READY_WITH_WARNINGS`) |
| COMPLETE | 35 |
| SUPERSEDED | 2 |
| DEFERRED | 1 |
| NEEDS_REPAIR | 0 |
| **Total** | **42** |

**Why no row is `NEEDS_REPAIR`.** The test is whether a Step 4 run can be graded correctly against the file as written.

- `AUDIT-FIX-52`, `-53` and `-54` all fall inside `F7.2-01`'s pre-rental runbook edit. The sub-plan already lists `docs/build-environment.md` as `modified`. Each fails safe if left unfixed: the session stops rather than proceeding wrongly.
- `AUDIT-FIX-50` and `-37` name edits that the owning rows already schedule.

| Sub-Plan Path | Status | Finding IDs | Dependency State | Reason | Required Repair |
|---|---|---|---|---|---|
| Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | READY_WITH_WARNINGS | AUDIT-FIX-52, AUDIT-FIX-53, AUDIT-FIX-54 | satisfied | **Queue head.** `Faz7.1` verified (`IMPL-91`); manifest `22283d8`, public repositories, `check.py` and the 14-failure negative case re-measured by this audit, and runbook section 5 run live with exit 0. Base `7dfc0650…` unchanged since 2026-05-24. `Faz6.1`'s entry is in the pinned fork `d48816f`. Amended by run 19; `AUDIT-FIX-43` and `-44` resolved in sections 4, 7, 8, 9 and 13. A Step 4 session stops after `F7.2-01` for the user's rental approval, by design. | **`F7.2-01`, before renting, in one edit of `docs/build-environment.md` followed by `bash -n` on each touched block:** (1) section 10 symlink test to `$OUT/vendor/lib64/camera/aon_front.pb`, including the `else` message, keeping `readlink`; record `/odm/lib64/camera/aon_front.pb` as the expected target. (2) Section 4: add that a sync failure matching a sync-path detector in the table (shallow sync of a `vendor/xiaomi/*` blob repository, or `vendor/xiaomi/camera`) gets its listed fix, counted against the 2 attempts, so the runbook agrees with `F7.2-04` (`AUDIT-FIX-52`). (3) Section 5: add a read-only comparison of `AOSPA/manifest` `beryl` HEAD with `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2`; a moved base is a stop before renting (`AUDIT-FIX-53`). (4) Either make section 10's `repo manifest -r` and section 11's image copies record-and-continue, or carry the operator rule that a non-zero exit in sections 10 or 11 means record the failing line, run the remaining lines by hand, and never skip retrieval of what exists or teardown (`AUDIT-FIX-54`). Grade `VAL-SYNC` and the resolved-manifest criterion against `22283d8` as amended by `fixes.diff`. Then the four Console checks, `DEC-25` and runbook section 4 re-read, and **stop for the user's rental approval**. |
| Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | READY_WITH_WARNINGS | AUDIT-FIX-37 | satisfied | The user's flash of the daily device. Depends on `Faz7.2`'s retrieved section 11 artifacts with sha256 and its AON step 1 result, the row above. `Faz8.1`'s static result is available (`IMPL-92`). Amended by run 19; `AUDIT-FIX-45` resolved. | At `F7.3-02`, state the possible wipe whenever `F7.3-01` wrote re-establishment steps, including when AOSPA's documentation left the requirement unsettled, not only when a format is confirmed required. `F7.3-08` writes `Project-Comprehension.md`: fold in the `IMPL-52`/`-53`/`-54` derivation-mechanism evidence entry while there (`AUDIT-FIX-37`). Do not start in the `Faz7.2` session. |
| Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md | READY_WITH_WARNINGS | AUDIT-FIX-22 | satisfied | Agreement half only: `F8.1-06` after `Faz7.2`, `F8.1-07` after `Faz7.3`, then `F8.1-10`. Static half done (`IMPL-92`: both layers carry-over on static values; scratch deleted). Amended by run 19; `AUDIT-FIX-46`, `-47`, `-49` resolved. | Do not repeat `F8.1-01`–`05`, `08` or `09`; they are recorded. Compare `Faz7.2`'s `build-evidence.txt` md5s and sizes with `IMPL-92`'s values, then `Faz7.3`'s on-device values; record a missing leg as not reached with its reason. `F8.1-10` edits `Project-Ontology.md`, which contains NUL bytes: edit byte-preservingly and diff the file afterwards (`AUDIT-FIX-22`). |
| Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md | READY_WITH_WARNINGS | AUDIT-FIX-50 | satisfied | The functional test on the carry-over path. Depends on `Faz8.1`'s carry-over on both layers with three-way agreement and on `Faz7.3`'s device on the `beryl` build, both earlier in this queue. Archive, manifest and checklist verified (`Faz9.1`, `Faz9.2`). Amended by run 19; `AUDIT-FIX-46` and `-51` resolved, `-50`'s sub-plan half resolved. | At `F8.3-08`, in the same edit as the evidence record, point `docs/release-checklist.md` section 3's `C-04`/`C-17` labels (lines 135, 148) and PC-04's "DEFECTIVE via smoke.sh" comment (line 176) at section 4's repair notes (`AUDIT-FIX-50`). Grade PC-17 on the two mount counts and take the trap reading from `prefs.trap.armed`. |
| Planner-docs/Faz-4-Plans/Faz4.6-raw-payload-geometry-diagnosis.md | DEFERRED | none | blocked | **Not queued.** Host-side half `implemented`. `F4.6-07` was gated on the superseded `Faz4.1`; `DEC-19` keeps `FIND-3.5-01` and `FIND-4.5-02` as knowledge. | Completing it would be a new user decision and a new sub-plan. |
| Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md | SUPERSEDED | none | independent | `superseded` 2026-09-03 by `DEC-14`. | **Do not revive it.** |
| Planner-docs/Faz-4-Plans/Faz4.7-ultra-high-resolution-sensor-mode.md | SUPERSEDED | none | independent | `superseded` 2026-09-03 by `DEC-14`. | **Do not revive it as project work.** |
| Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md | COMPLETE | none | satisfied | **New to COMPLETE.** `IMPL-91`: all ten acceptance criteria met; `docs/build-environment.md` written; `DEC-22` and `DEC-25` answered. Its outputs re-measured on GitHub by this audit. | none. Its transition is `Faz7.2`'s `F7.2-01`. |
| Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md | COMPLETE | none | satisfied | **New to COMPLETE.** `IMPL-93`: all ten acceptance criteria met without a merge, build, checkout or rental; `DEC-08` recommendation defer. | none. A merge would be a new decision under `DEC-08`. |
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

- `Faz7.2`: the rental approval after `F7.2-01`, deletion in the Console, and any post-session push of `fixes.diff`.
- `Faz7.3`: the go/no-go, the firmware approval, and the stay-or-restore choice.
- `Faz8.1`: `DEC-07`.
- `Faz8.3`: root, and the final enable state.

**Workspace precondition, for the user, not a finding.** Planning run 19 is uncommitted (six planner files), and this audit adds a seventh. A Step 4 run contract stops on an unrelated dirty worktree. These changes are the plan the Step 4 session executes, so they are related, but committing them locally first gives the rental session a clean baseline. Whether to commit is the user's call, per `docs/pre-rental-plan.md` steps 2 and 3.

## 13. Priority Fix List

**No P0 or P1 finding is open.** The register now holds 54 findings: three are new this run (`AUDIT-FIX-52` … `-54`), and fifty-one are carried.

**Changed this run.** Eight were resolved: `-43`, `-44`, `-45`, `-46`, `-47`, `-48`, `-49` and `-51`. `-50` was narrowed to its document half.

**Ten remain active:**

| Group | Findings |
|---|---|
| P2 open | `-22` |
| P3 open | `-37`, `-41`, `-42`, `-50`, `-52`, `-53`, `-54` |
| P3 accepted | `-25`, `-33` |

Findings resolved or marked `not_applicable` before the ninth audit are not re-listed row by row; nothing since has touched their subject matter.

| Finding ID | Severity | Status | Affected Files | Issue | Required Action |
|---|---|---|---|---|---|
| AUDIT-FIX-22 | P2 | open | Planner-docs/Project-Ontology.md | Carried and re-measured. Still **7** control bytes below 0x20, including **2 NUL**, now at byte offsets 42806, 42869, 42932, 42989, 42990, 42991 and 43113 (+216 from the ninth audit, because `IMPL-91`'s `F7.1-12` edit lengthened text above them; the count is unchanged, so that edit was byte-preserving). Content search on the file still fails silently. **Queued writer now:** `F8.1-10` only. | Unchanged: replace the `Escape` column's raw bytes with the project's octal `printf '%b'` convention in a bounded amendment of that one table, then confirm the file reappears in `rg -l InitializeScalerStaticCaps`. Until then, Step 4 edits to this file must be byte-preserving and diffed, and no escape may be transcribed from that column. |
| AUDIT-FIX-52 | P3 | open | Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, docs/build-environment.md | **New.** Runbook section 4 says "Sync failure (`repo sync`, or barista's …): stop", while its own deferred-items table gives sync-time fixes for the shallow sync of the blob repositories and for `vendor/xiaomi/camera`. `F7.2-04` reads the table as allowing those fixes, counted against the 2 attempts — the right reading — but `Faz7.2` section 1 says "Where this file and the runbook disagree, Step 4 follows the runbook", so a rental-day session holds two contradicting instructions. Separately, `VAL-SYNC` and the section 8 criterion compare `manifest-resolved.xml` against the 13 pins "at `22283d8`", which a permitted fix (a removed `clone-depth`, deleted `vendor/xiaomi/camera` lines, or a deleted `display-drivers` pin) legitimately changes. | In `F7.2-01`'s pre-rental runbook edit, add the sync-path exception to section 4's sync-failure bullet so the runbook agrees with `F7.2-04`. Grade `VAL-SYNC` against `22283d8` as amended by `fixes.diff`, and record that basis in the ledger row. At a later bounded amendment, reword `Faz7.2` section 8's resolved-manifest criterion the same way. |
| AUDIT-FIX-53 | P3 | open | Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, docs/build-environment.md | **New.** The base pin `AOSPA/manifest` `beryl` = `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` is first asserted in runbook section 8, on a billed server; section 5's free block does not read it. Measured today it has not moved since 2026-05-24, but a move between now and the rental day would stop the session after the clock starts. | In `F7.2-01`, add one read-only check to section 5 — `AOSPA/manifest` `beryl` HEAD equals the pinned commit, via the WinGet `gh.exe` — and treat a mismatch as a stop before renting, routed to the user. `bash -n` the block. |
| AUDIT-FIX-54 | P3 | open | docs/build-environment.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | **New.** Runbook sections 10 and 11 run under `set -euo pipefail`, while the runbook and `F7.2-07`/`-08` say a missing file is "recorded, not fatal". Section 10's first command, `repo manifest -r`, plausibly fails on a partially synced tree (not measured) and would exit before `build-evidence.txt`, the log tails and `evidence.tar.gz` exist — the evidence `F7.2-05` needs "whatever the build outcome". Section 11's `cp "$OUT/$i.img"` loop stops at the first absent image, before `SHA256SUMS`, where `F7.2-08` expects the absence to be recorded. | Either, in `F7.2-01`, make those lines record-and-continue (for example, a failed `repo manifest -r` writes a marker file, and a missing image is logged and skipped), with `bash -n` afterwards; or carry the operator rule into the session: a non-zero exit in sections 10 or 11 means record the failing line, run the remaining lines by hand, retrieve what exists, and never skip teardown. |
| AUDIT-FIX-50 | P3 | open | docs/release-checklist.md | Carried, **narrowed to its document half.** Run 19 resolved the sub-plan half: `F8.3-06`, the criterion and `VAL-CHECKLIST` use `prefs.trap.armed` and the single-dump probe, and PC-17 is correctly graded on the two mount counts, which corrects the ninth audit's wording. `docs/release-checklist.md` still labels `C-04` with `FIND-3.10-01` (line 135) and `C-17` with `FIND-3.7-02` (line 148), and PC-04 still reads "DEFECTIVE via smoke.sh" (line 176). | `F8.3-08` owns it: in the same edit as the v2.2-on-`beryl` evidence record, point those labels and the comment at section 4's repair notes. |
| AUDIT-FIX-37 | P3 | open | Planner-docs/Project-Comprehension.md | Carried. `Project-Comprehension.md` still cites `IMPL-52`, `-53` and `-54` zero times; `Project-Ontology.md` cites them 2, 1 and 2 times. `F7.1-12` (`IMPL-91`) wrote the comprehension file without folding the entry in, so the remaining natural owner is `Faz7.3` `F7.3-08` (`TRACE-13`, `ARC-06`). | Add the derivation mechanism as an evidence entry when `F7.3-08` writes the file. |
| AUDIT-FIX-41 | P3 | open | Planner-docs/Main-Planing.md | Carried, unchanged at line 277: section 8's step 5 still says "the preference is `pref_camera_picturesize_back_key` and the app exposes it as an ordinary settings menu item". No queued row reads it; Phase 3 is closed. | At the next deliberate Step 1 amendment, rewrite step 5 to the measured configuration (`pref_48m_key=0`, `pref_camera_resolution=full`, read the derived key back) and mark it done under `DEC-21`. |
| AUDIT-FIX-42 | P3 | open | Planner-docs/Main-Planing.md | Carried, unchanged: line 22 "a third (Android 16 / beryl) has not started", line 61 "Android 16 / AOSPA `beryl` port", line 288 "Do not expand yet. Phases 7, 8, and 9. G is blocked on host-environment work the user must perform". Each is now further from the facts, since `Faz7.1` and `Faz8.2` are verified. | At the same Step 1 amendment, reword all three to `DEC-24` and the branch reading of `beryl`, and mark section 9's paragraph discharged. Do not cut a snapshot for these alone. |
| AUDIT-FIX-33 | P3 | accepted | Planner-docs/Faz-3-Plans/Faz3.8-agc-state-in-smoke-script.md, Planner-docs/Sub-Planing-Index.md | Carried. `Faz3.8` lines 120 and 163 and the index still describe three fields; the sub-plan is `verified` at four (`IMPL-55`, `IMPL-56`). | No repair required; accepted and kept visible. |
| AUDIT-FIX-25 | P3 | accepted | Planner-docs/Faz-1-Plans/Faz1.3-patch-table-format-contract.md | Carried, unchanged at line 9: "Faz 4.1 narrows the RAW emission …". | No repair required; `Faz1.3` is COMPLETE. |
| AUDIT-FIX-43 | P2 | resolved | Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md | Teardown and budget rested on billing semantics nobody had read. | **Resolved.** `IMPL-91` wrote runbook section 3 from Hetzner's billing FAQ ("until you delete them, independent of their state"; Primary IPs, snapshots and backups bill separately), and `DEC-25` cites it. Run 19 carries it in `Faz7.2` section 4, `F7.2-09`, section 8, `VAL-TEARDOWN` and section 13. |
| AUDIT-FIX-44 | P2 | resolved | Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md, Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md, Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | The retrieval list was not tied to the install method, and the server was deleted before `Faz7.3` learned what flashing needs. | **Resolved.** Runbook section 11 names every artifact and the method that consumes it; `build.sh -z`'s outputs were verified by this audit. `F7.2-08`, its criterion, `VAL-RETRIEVE` and section 13 retrieve each one with sha256 or record its extraction source before deletion; `Faz7.3` section 6 and `F7.3-02`/`-03` choose from that list. |
| AUDIT-FIX-45 | P2 | resolved | Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md | The return path assumed a whole-system flash preserves `/data`. | **Resolved.** `F7.3-01` records the requirement both ways with sources, and writes re-rooting, the v2.2 reinstall against `docs/release-manifest.md`, `docs/agc-12mp-configuration.md` section 2 and a `prefs.trap.armed` audit when a format is required or the requirement is unsettled. `F7.3-02` states the wipe; `F7.3-07`, its criterion and `VAL-RESTORE` grade the re-established fields by name. |
| AUDIT-FIX-46 | P2 | resolved | Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md, Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md, Planner-docs/Sub-Planing-Index.md | Gates accepted a "completed adaptation" that no sub-plan performs. | **Resolved.** `F8.1-08` ("Only carry-over is a label `Faz8.3` can consume"), `F8.1-09`'s adaptation branch, `Faz8.1` section 13, `F8.3-01`, `Faz8.3` sections 8 and 13, and index section 5's new deferred item. `IMPL-92` found the sensor unchanged on static values, so the branch is currently latent. |
| AUDIT-FIX-47 | P3 | resolved | Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md, Planner-docs/Sub-Planing-Index.md | Unspecified scratch deleted too late; index 4d's static-half boundary disagreed with `Faz8.1` section 10. | **Resolved.** Scratch is outside the workspace and deleted at `F8.1-05`, with `VAL-CLEAN` at two points; `IMPL-92` had already done so. Index 4d step 2 now uses `Faz8.1` section 10's boundary. |
| AUDIT-FIX-48 | P3 | resolved | Planner-docs/Sub-Planing-Index.md | Index claimed CRLF sub-plans. | **Resolved** at line 357: the claim is struck and corrected to LF, which this audit's byte scan confirms. |
| AUDIT-FIX-49 | P3 | resolved | Planner-docs/Planing-Ledger.md, Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md | `IMPL-89` contradicted `IMPL-90`; `F8.1-04` named no Android 15 candidate. | **Resolved.** Ledger line 517 carries "[corrected by `IMPL-90`; annotated 2026-09-13 by planning run 19 …]"; `F8.1-04` and `Faz8.1` sections 4, 6 and 8 name both candidates and decide from the `vauxite` beans. |
| AUDIT-FIX-51 | P3 | resolved | Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md | The restart detector did not list init service names, and missed "switch has no effect". | **Resolved.** `F8.3-05`, `VAL-RESTART`, `Faz8.3` section 8 and the first section 11 risk, consistent with `setmode.sh:52-58` and `:110-114` as measured. |

**Finding status consistency.** Ten findings are active: one P2 open, seven P3 open, and two P3 accepted. No P0 or P1 is open, so Step 4 is unblocked. The status is `PASS_WITH_WARNINGS`, not `PASS`, because those ten are open or accepted and must stay visible during implementation.

**Project findings versus audit findings.** `FIND-3.5-01` and `FIND-4.5-02` are P1 **project** findings, which `DEC-19` keeps as knowledge. They are not audit findings and do not gate Step 4.

**Validator behaviour, stated so it is not misread.** `--mode step3 --strict` and `--mode step4 --strict` report `validation_status=failed` with one error, `strict_warning=step4_has_nonblocking_warnings`. That is `--strict` promoting the non-blocking P2/P3 warning into an error, which every `PASS_WITH_WARNINGS` audit gets. **It is not a structural defect.** The gating facts are `p0_findings=0` and `p1_findings=0`.

## 14. Recommended Next Command / Prompt

**Step 4 may begin.** The status is `PASS_WITH_WARNINGS`, no P0 or P1 is open, and only P2/P3 findings remain, so the Step 4 prompt is printed. Per `docs/pre-rental-plan.md` step 4, it is limited to `Faz7.2`. Part A is `F7.2-01`, including the section 10 correction and the three runbook repairs this audit adds. The session then stops for the user's rental approval.

**Before starting it, the user decides** whether to commit planning run 19 and this audit locally, so the rental session starts from a clean tree, and chooses a day with the full 10-hour window free. **Two optional user choices, at any checkpoint:** a push to the private `origin` as an off-machine copy, and what to do with `devir-teslim-promptu.md`.

**One supporting action, not a precondition:** at the next deliberate Step 1 amendment, fold in `AUDIT-FIX-41` and `-42`, without cutting a snapshot for them alone.

```text
/claudeqb:claudeqb Read and return the exact canonical handoff from references/handoffs/run-step4.md, then execute it.

Context: step 4 of docs/pre-rental-plan.md, the rental-day session. Read that file first, then git status. The tenth Step 3 audit (2026-09-13) is PASS_WITH_WARNINGS with no open P0 or P1; queue state READY. This session is LIMITED to Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md. Do not start Faz7.3, Faz8.1's agreement half or Faz8.3. Keep the ten active findings visible: AUDIT-FIX-22, -25, -33, -37, -41, -42, -50, -52, -53, -54; this session owns -52, -53 and -54. docs/build-environment.md is the operative runbook: where it and the sub-plan disagree, follow the runbook and record the disagreement, except where the audit's Faz7.2 row says to edit the runbook first.

Part A (free, host only): F7.2-01. (1) Run runbook section 5's scripted block exactly as written in Git Bash, with GH=C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe, python not python3, and TMPDIR outside the workspace; record the exit status and the "pre-rental checks passed" line. (2) In one edit of docs/build-environment.md: section 10's built-symlink test and its else message change from $OUT/odm/lib64/camera/aon_front.pb to $OUT/vendor/lib64/camera/aon_front.pb, readlink kept, with expected target /odm/lib64/camera/aon_front.pb (AOSPA extract-utils install_symlink, refs/a16_ishtar/proprietary-files.txt:1037); section 4 gains the exception that a sync failure matching a sync-path detector in its table (shallow sync of a vendor/xiaomi/* blob repository, or vendor/xiaomi/camera) gets its listed fix, counted against the 2 attempts (AUDIT-FIX-52); section 5 gains a read-only check that AOSPA/manifest beryl HEAD equals 7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2, a mismatch being a stop before renting (AUDIT-FIX-53); either make section 10's repo manifest -r and section 11's image copies record-and-continue, or record the operator rule that a non-zero exit there means record the failing line, run the rest by hand, retrieve what exists and never skip teardown (AUDIT-FIX-54). Run bash -n on every touched block, run the new section 5 check, read the edit back, and show me the diff. (3) Ask me for the four manual checks and record my answers: the Hetzner Console Limits tab allows one CCX53; my public SSH key is present; ~/Documents/Projeler/ishtar-builds/ exists outside every repository; the 10-hour ceiling fits today. (4) Re-read DEC-25 and runbook section 4 and state the stopping rule back in five lines. Write the gate record under snapshots/ (text only, no address, no key) and a short ledger row for the gate.

Then STOP and ask for my explicit rental approval. Without it, end the session with the gate result recorded.

Part B (paid, only after my approval in this session): runbook sections 6 to 13 in order, as F7.2-02 to F7.2-10. Record per stage only start and end time (UTC), exit status, error class and the last lines of a failing log; never whole logs. Fixes are server edits to .repo/local_manifests/ishtar-beryl.xml recorded in ~/evidence/fixes.diff, at most 2, manifest-class only, never pushed during the session. Grade VAL-SYNC against 22283d8 as amended by fixes.diff. At hour 8, retrieve what exists and tear down. Do not tear down until sha256sum -c passes for every retrieved file. Teardown deletes the server and every Primary IP (never shut down), confirms zero servers, zero Primary IPs, and no volume, snapshot or backup, and records elapsed hours against the 10-hour ceiling, whatever the build outcome. Write the runbook section 13 ledger row, the Phase 8 readiness statement and the ledger section 7 viability check.

Rules: no token, key, password or server address written anywhere; no device command; no push and no commit without asking me; do not touch devir-teslim-promptu.md. Work in small verified slices and do not load other sub-plans.
```

**Token and queue reminder.**

- **Part A is cheap:** one scripted block, one reviewed runbook edit, and four questions.
- **Part B is where token and money risk both peak.** Keep the stopping rule in the session's own context, and read only exit status, stage, error class and log tails.
- **After `Faz7.2`, the queue continues in fresh sessions:** `F8.1-06` can run from `Faz7.2`'s evidence, then `Faz7.3` (the flash, on a separate day), `F8.1-07`, `F8.1-10`, and `Faz8.3`.

Do not run the prompt from this audit session.

## 15. Audit Result

- **Final status: PASS_WITH_WARNINGS.**
  - **Coverage:** nine main phases, nine phase folders and 42 sub-plan files, all structurally compliant, with zero structural problems measured across all 42.
  - **Validators:** `--mode step2 --strict` and `--mode step3-preflight --strict` both pass, with `error_count=0`, `warning_count=0`, `secret_findings=0`, `subplan_count=42` and `index_reference_count=42`.
  - **Findings:** ten active (one P2 open, seven P3 open, two P3 accepted), none P0 or P1. Eight resolved this run, and three new, all P3.
  - **Queue:** READY, with four rows headed by `Faz7.2`.
- **Confidence: high** on structure, coverage, index consistency, every finding's discharge, and every GitHub or build-system fact this audit asserts: the manifest, visibility, the base pin, `rom-build.sh`, `-z` outputs and `install_symlink` semantics, each measured this run. Runbook section 5 was executed, not only read. **Medium** on `AUDIT-FIX-54`'s first clause, which reasons about `repo manifest -r` on a partial tree without running it. **Not assessed for content this run:** the 38 sub-plans run 19 did not touch, on which earlier audits' assessments stand.
- **Only `Planner-docs/Sub-Planing-Audit.md` was modified by this run.** No sub-plan, index, ledger, master plan, ontology, comprehension file, runbook or source file was written. Section 5's clone and `check.py` run went to this session's scratchpad, outside the workspace. No device command, no rental, no GitHub write, no commit and no push.
- **Unexpected modifications: none detected.** The other entries in `git status` were present before this audit began: the six planner files of planning run 19 (uncommitted), and the untracked `devir-teslim-promptu.md`, which was not touched.
- **Step 4 can safely begin**, limited to `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md`. Part A is `F7.2-01`, including the section 10 correction and the `AUDIT-FIX-52`/`-53`/`-54` runbook repairs. The session then stops for the user's rental approval.
