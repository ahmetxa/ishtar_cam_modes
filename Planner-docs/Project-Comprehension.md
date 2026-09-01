# Project Comprehension

> Evidence-backed mental model for `ishtar`. Written by ClaudeQB Step 1.5.
> Evidence types: `source`, `test`, `runtime`, `history`, `configuration`, `documentation`, `user-confirmed`.
> Confidence: `confirmed`, `probable`, `tentative`, `contradicted`. Nothing is marked `confirmed` without executable evidence or two independent evidence types.

## 1. Understanding Goals and Competency Questions

The change goal driving this comprehension pass is: **make a 50 MP capture complete inside the AGC port, without widening the blast radius of the HAL patch, and without losing the workspace to an unrecoverable mistake along the way.**

| ID | Question | Priority | Answer criterion | Status |
|---|---|---|---|---|
| CQ-01 | Which layer actually gates 50 MP today? | P0 | A named function or check, measured on device | answered |
| CQ-02 | Is the workspace recoverable from a mistake? | P0 | Version control or an equivalent snapshot exists | answered (positively, 2026-08-24 by Faz 1.1) |
| CQ-03 | What proves a mode switch worked? | P0 | A repeatable command producing a pass/fail signal | answered 2026-08-30 (Faz 2.1): `scripts/smoke.sh`. Demonstrated on a real dcgB-to-dcgA switch, where the comparable-region diff was exactly three lines and nothing else moved. |
| CQ-04 | Which invariant does libgcam enforce, exactly? | P0 | The source line and both accepted values | answered |
| CQ-05 | Where does the HAL write `pixelArraySize`? | P0 | An address that, when patched, changes `dumpsys` output | open |
| CQ-06 | Are the sensor and HAL layers truly independent? | P1 | Evidence that one can change without the other | answered (they are, but exclusion is enforced in shell) |
| CQ-07 | What is the smallest correct HAL patch? | P1 | A patch adding RAW only at full resolution, with duration rows | open |
| CQ-08 | Which artifacts are safe to distribute? | P1 | An enumerated packaging rule | answered (rule enumerated 2026-08-24 by Faz 1.2 as Project-Ontology invariant 9a; enforcement is Faz 9.1) |
| CQ-09 | Can the module brick the camera, and how is it recovered? | P1 | A written recovery path | open |
| CQ-10 | Which conclusions in the journal are stale? | P1 | Superseded sections identified | answered |
| CQ-11 | Does the WebUI expose a shell-injection surface? | P2 | `index.html` read and its `action.sh` calls traced | answered (no) — exhaustive: 4 `exec` sites, 2 `run()` callers, every argument from a source literal. See `Project-Ontology.md` OQ-06. One defence-in-depth gap remains at `index.html:276` (FIND-1.5-02), not reachable today. |
| CQ-12 | Is boot-time patch application atomic? | P2 | `halpatch.sh` and `post-fs-data.sh` read | answered (no, by design) — ordered `dd` writes onto a module-private copy, md5-classified and re-seeded on damage. See `Project-Ontology.md` OQ-05. `post-fs-data.sh:66` is the one copy with no post-write verification (FIND-1.5-03). |
| CQ-13 | What blocks the Android 16 track? | P2 | A named environment blocker | answered |
| CQ-14 | Is `Kararlar #4` (mode-0 12-bit) still the right next experiment? | P2 | A human decision, given Phase 3's growth | open — needs user |

## 2. Evidence Register and Confidence

| ID | Claim | Claim Type | Evidence Type | Evidence Source | Confidence |
|---|---|---|---|---|---|
| EV-01 | The workspace is a git repository as of 2026-08-24 (Faz 1.1); it was not one before | structural | source | `git rev-parse --is-inside-work-tree` returns `true`; commit `ff6934e` tracks 86 files; `git status --short` is empty | confirmed |
| EV-02 | No tests or CI exist anywhere in the tree; a smoke harness now does | structural | source | Still no `tests/` · no `.github/` · no `Makefile` · no `package.json` · no `pyproject.toml`. Superseded in part 2026-08-30 (Faz 2.1): `scripts/smoke.sh` is the first automatable validation surface the project has ever had. | confirmed |
| EV-03 | The sensor-mode layer is mature and in daily use | configuration | runtime | Workspace `ishtar-cam-modes/module.prop` reads v2.1/versionCode 12, but the **device runs v2.0/versionCode 11** (Faz 2.1, 2026-08-30), on mode `dcgB`. Mature and in daily use is confirmed; the version is the older one. | confirmed |
| EV-04 | 50 MP works for third-party applications | behavioral | runtime | on-device Open Camera capture measured at 50.3 MP (journal Faz 8) | confirmed |
| EV-05 | AGC cannot yet complete a 50 MP capture | behavioral | runtime | logcat `Stuck shot ... HDR_PLUS` plus the `static_metadata.cc:667` rejection | confirmed |
| EV-06 | libgcam requires `frame_raw_max` to equal the active array or the pixel array | behavioral | runtime | logcat line naming `8192x6144` against `4096x3072` for both arrays | confirmed |
| EV-07 | `getOutputSizes()` excludes sizes slower than 1/20 s | behavioral | runtime | min frame duration 66666666 ns measured for 8192x6144 on camera 3 | confirmed |
| EV-08 | `Forty8Strip` is an identity stub | structural | source | baksmali output: `LAGC;->Forty8Strip(I)I` body is `return p0` in both builds | confirmed |
| EV-09 | `Lddl;->P` and `Lddl;->Q` blocklists are empty | structural | source | baksmali output for `Lddl;` | probable |
| EV-10 | The four-instruction patch makes AGC select RAW10 8192x6144 unaided | behavioral | runtime | AGC log `getImageReaderFormat ... RAW10 8192x6144` with no preferences set | confirmed |
| EV-11 | The `;SYMLINK=` entry was absent from both device trees; it was added 2026-08-24 by Faz 6.1 and its effect is **not yet verified by any build** | structural | source | `grep -c ";SYMLINK="` now returns 1 for `device_ishtar/proprietary-files.txt` and 1 for `refs/a16_ishtar/proprietary-files.txt`, each exactly one line changed. Entry form copied from `refs/neo_ishtar/proprietary-files.txt:1154`, the same declaration for the same device and file. | confirmed (as an edit) / unverified (as a fix) |
| EV-12 | Camera restart must run client before HAL | behavioral | runtime | reversing the order reproduced a black preview in every mode including stock | confirmed |
| EV-13 | `pref_raw_key` and `pref_fix_resolution_key` break Gcam init independently | behavioral | runtime | isolation run: reverting the HAL then the APK did not fix it · deleting the prefs did | confirmed |
| EV-14 | Released v2.1 had never been flashed until 2026-08-31 | historical | runtime | Was true through 2026-08-30 (Faz 2.1), when the installed module reported `version=v2.0`, `versionCode=11`. **Closed by measurement on 2026-08-31 (Faz 2.2, IMPL-11):** `ishtar-cam-modes-v2.1.zip` (md5 `fea919b67a4693a4591127be4a6e9daa`) was flashed through KernelSU-Next and the device now reports `version=v2.1`, `versionCode=12` in baseline snapshot `BASELINE-2026-08-31-V21`. The local-versus-live gap `AUTOPSY-P1-02` describes is closed for the sensor-mode layer. | confirmed |
| EV-15 | A signing keystore sits in the working tree | structural | source | `ishtar-cam-modes/tile-app/debug.keystore` (path only · contents not read) | confirmed |
| EV-16 | The experimental patch grows the stream array from 508 to 868 int32 | behavioral | runtime | `dumpsys media.camera` entry count before and after the experiment | confirmed |
| EV-17 | radare2 and rabin2 do not complete on this binary | behavioral | runtime | two runs at 300 s and 60 s in two different shells produced zero output | confirmed |
| EV-18 | The workspace holds approximately 7.3 GiB in total; 454.4 MiB of that is root-level files | structural | source | per-directory `find -type f -printf %s` sums, 2026-08-24 (Faz 1.1); table in `UNTRACKED-BY-DESIGN.md` section 1. The earlier 465 MB figure counted root files only and no directory. | confirmed |
| EV-19 | The device's live mode matches the workspace `mode` file | configuration | runtime | **Contradicted on device 2026-08-30 (Faz 2.1).** The device reported mode `dcgB` with the live sensor blob md5 matching `dcgB.bin`; the workspace `mode` file said `stock`. **Contradicted a second way on 2026-08-31 (IMPL-11):** after the v2.1 update the device has no `$MODDIR/mode` file at all, while the workspace file still says `stock`. The two are not merely out of sync; post-update the device holds no persisted mode to compare against. The workspace file is not a mirror of device state and must never be read as one. | contradicted |
| EV-20 | WSL2 is not installed and blocks the Android 16 track | user_intent | user-confirmed | user statement recorded in project history | probable |
| EV-21 | `dcgB` gives about 25% less noise and roughly double the detail versus stock | behavioral | runtime | on-device comparison recorded in `module.prop` and the journal | probable |
| EV-22 | The `tiles hide` option is ineffective | behavioral | runtime | observed on device; the cause was never diagnosed | probable |
| EV-23 | AGC cannot exceed 15.2 MP | behavioral | documentation | journal Faz 8 conclusion, superseded by EV-10 | contradicted |

## 3. Domain-to-Code Trace Map

| ID | Domain concept | Entrypoint | Core implementation | State / data | Tests | Docs |
|---|---|---|---|---|---|---|
| TRACE-01 | Mode selection | tile app, WebUI, `action.sh` | `setmode.sh` (280 L) | `$MODDIR/mode` | **none** | journal Faz 5; `Kullanim.txt` |
| TRACE-02 | Sensor layer application | `setmode.sh` | bind-mount from `blobs/*.bin` | `active/…bin`, size 1,062,250 | `tools/verify_ln.py` (build-time only) | journal Faz 2–4 |
| TRACE-03 | HAL layer application | `setmode.sh` → `halpatch.sh` | `hal_write`/`hal_state`/`hal_set`/`hal_seed` | `blobs/hal-fullres.patch`, `active_hal/` | **none** | journal Faz 4 |
| TRACE-04 | Camera restart | `setmode.sh` | `restart_camera()`, `wait_svc()` | service states | **none** | in-line comments (excellent) |
| TRACE-05 | Boot reapplication | `post-fs-data.sh` (131 L) | not read this pass | `mode` | **none** | journal Faz 5 |
| TRACE-06 | Tiles and launcher visibility | `tile-app/` (Java) | not read this pass | `mode`; framework query | **none** | journal Faz 6–7, 9 |
| TRACE-07 | WebUI | `webroot/index.html` (344 L) | not read this pass | `mode`; `lang` | **none** | journal Faz 6 |
| TRACE-08 | Blob generation | host Python | `dcg_multimode.py`, `ln_multimode.py`, `port_sensor_mod.py` (606 L) | `blobs/` | `verify_ln.py` (126 L) | journal Faz 2–4 |
| TRACE-09 | AGC size selection | `LAGC;->getSupportedOutputSizes` | `agc-50mp-yama/*.smali` | `pref_48m_key` gate | **none** | `agc-50mp-yama/README.md`; Faz 11 |
| TRACE-10 | AGC channel selection | `LensSettings.getImageFormatArr()` | port internals (read-only) | `pref_raw_key_<lens>` | **none** | ontology §6; Faz 11 |
| TRACE-11 | Full-res stream advertisement | `InitializeScalerStaticCaps` `0x16bf4c0` | 16 + 4 patch sites | `dumpsys media.camera` | **none** | Faz 4, Faz 12 |
| TRACE-12 | Gcam metadata validation | libgcam `static_metadata.cc:667` | vendor, unmodifiable | active/pixel array tags | **none** | Faz 12 |
| TRACE-13 | AON repair | `ishtar-aon-fix/post-fs-data.sh` | creates `aon_front.pb` path | — | **none** | memory + module description |
| TRACE-14 | Device-tree defect | `device_ishtar/proprietary-files.txt` line 1031; `refs/a16_ishtar/proprietary-files.txt` line 1037 | `;SYMLINK=` entry **added** 2026-08-24 (Faz 6.1); addressed but unproven until a build runs | — | **none** — verification is registered against Phase 7 by Faz 6.2 | Faz 10 notes; `Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md` |

**Trace gap of note:** every row's Tests column is empty except TRACE-08. The project's entire verification surface is one build-time blob checker.

## 4. Structure, Data, and Runtime Flow Model

**Static structure.** Three deliverable directories (`ishtar-cam-modes`, `ishtar-aon-fix`, `agc-50mp-yama`), one journal, five ROM reference trees, three kernel checkouts, two upstream reference modules, and a set of loose binaries at the root. No build system, no package manifest, no dependency graph — the "build" is a zip.

**Data model.** Deliberately minimal: one mode string in one file, plus `lang`. Everything else is derived at runtime by reading the device. This is a strength — there is no state to corrupt beyond one word — and it is why the tile-synchronization bugs (v1.5, v2.1) were read-path bugs rather than state-corruption bugs.

**Runtime flow, mode switch.** User input → `action.sh` → `setmode.sh` → `restart_camera()` (stop `cameraserver`, stop providers, force-stop camera apps, start `cameraserver`) → apply sensor bind-mount *or* HAL byte-patch → md5 verify → write `mode` → notify → tiles re-read.

**Runtime flow, 50 MP capture (target state).** Tile sets `50mp` → HAL patched → `InitializeScalerStaticCaps` emits 8192x6144 for the admitted formats → framework advertises them → AGC's `getImageFormatArr()` walks its preference order, picks the first non-empty format, `bs()` takes its maximum → ImageReader opened at 8192x6144 → **libgcam validates static metadata** ← *currently fails here* → Gcam processes → file written.

**Failure modes observed in practice.** Black preview in every mode (restart ordering — fixed). Stuck shutter (Gcam init failure, or a permission dialog holding focus, or HDR+ still initialising). Camera locked after mode change (fixed v1.6). `Gcam.f()` NPE (the metadata invariant). Empty launcher icon (tint bug — fixed v2.1).

## 5. Intended vs Implemented Architecture

| ID | Intended relation | Implemented | Status |
|---|---|---|---|
| ARC-01 | Sensor layer and HAL layer are independent | Both dispatched from `setmode.sh`; `halpatch.sh` is sourced, not invoked as a boundary | convergent |
| ARC-02 | Mode is single-writer state | One file, one writer, multiple pollers | convergent |
| ARC-03 | Layer exclusion is a system rule | **Enumerated by Faz 5.3 (IMPL-17): six surfaces, and the rule is enforced as *logic* in only two of them** — `post-fs-data.sh:15-27` and `setmode.sh:177-192`, structurally identical case dispatches. The other four do not enforce it: `action.sh:94-104` `active()` **reports** it (HAL-first — if the HAL is `fullres` it returns `50mp` and never reads the sensor layer); `BaseTile.java:119,301` and `webroot/index.html:187,260,317` **assume** it via a single-valued current-mode string; `customize.sh:64` merely **describes** it. The tile application contains **no exclusion rule at all** — tile exclusivity is emergent from the one-string state model, which closes `TRACE-06`'s unknown. Consequence: removing the exclusion is not a two-site logic edit but a **state-model change** from one mode string to two independent layer states, reaching `action.sh`, the tile app and the WebUI. | divergent |
| ARC-04 | Vendor blobs are never redistributed | True for our artifact; the upstream reference module ships three full 27 MB copies | convergent |
| ARC-05 | Patch tables are self-verifying | md5 of both input and output recorded | convergent |
| ARC-06 | The AON fix belongs in the device tree | Implemented as a runtime module; the tree still lacks the entry | divergent |
| ARC-07 | Application-layer patches live in `agc-50mp-yama` | True, except `hal-raw50-deneme.patch` (a HAL artifact) lives there | divergent |
| ARC-08 | Releases are reproducible from the tree | No build script exists; four zips have no visible producer | absent |
| ARC-09 | Changes are verified before release | No verification surface exists | absent |
| ARC-10 | History lives in the journal | Duplicated into `module.prop` `description` | divergent |
| ARC-11 | Recovery from a broken module | No documented path | absent |
| ARC-12 | SELinux rules ship with the module | Present in reference modules; unverified for ours | uncertain |

**Reading of the drift.** None of the divergences are accidents of neglect — each is a reasonable in-the-moment choice (keep the experiment near the work; put the fix where it can run today; note the change where the user will see it). The pattern is that **structure has lagged behind capability**, which is the normal shape of a research workspace that succeeded. Phases 1, 4, 6, and 9 in the master plan address exactly these rows.

## 6. Change History, Hotspots, and Ownership Signals

No git history exists for the work described below (EV-01), so evolutionary evidence comes from `module.prop`'s version notes and the journal's phase structure. This is a weaker signal than commit history and is used only directionally. History begins at commit `ff6934e` (2026-08-24, Faz 1.1); everything before it is unrecorded and this paragraph remains the only account of it.

**Version cadence.** v1.0 → v2.1 across roughly eight days (2026-08-16 to 2026-08-22), with four released zips. Rapid, and the fixes are specific rather than cosmetic.

**Hotspots inferred from the version notes.**

- *Tiles and launcher visibility* — touched in v1.4, v1.5, v1.7, v2.1. The most-revisited area, and every revisit was a read-path or synchronization issue. This is where the next UI regression is most likely.
- *Camera restart* — v1.6 and v1.7. Two consecutive versions on one function, ending in a documented invariant. Now stable and well commented.
- *Mode switching UX* — v1.7, v1.8, v1.9. Feedback and language, not correctness.
- *50 MP* — v2.0, then Faz 11 and 12 outside the module. The active frontier.

**Ownership signals.** Single author throughout (`module.prop` credits "port: Claude / orijinal mod: Eskom_Sa"). There is no review boundary and no second pair of eyes — which raises the value of the automated gates proposed in Autopsy §8, since they are the only available substitute.

**Journal cadence.** Twelve phase sections, non-monotonic (Faz 10 pending while 11–12 are complete). The numbering drift is itself a signal: the 50 MP work grew beyond its original plan slot, which is worth noticing when scoping Phase 3.

## 7. Quality Attribute Scenarios and Tradeoffs

**QAS-01 — Recoverability.** *Scenario:* a patch is written with a stale offset and the camera HAL is corrupted. *Response measure:* the user can restore stock and reopen the camera without reflashing the ROM. *Current state:* the md5 guard should prevent the write, but if a write does land there is no documented recovery path (ARC-11). *Tradeoff:* none — this is pure gap. *Goal/Question/Evidence:* Goal — never lose the camera. Question — what does the user do at 2 a.m. with a black preview? Evidence — none exists today.

**QAS-02 — Regression detectability.** *Scenario:* a change breaks one of ten modes and the user does not notice for two days. *Response measure:* a single command reports which modes are healthy. *Current state:* impossible; no smoke surface. *Tradeoff:* writing the smoke script costs a day that could go to Phase 3 — but Phase 3's own history shows two days lost to misattribution (EV-13), so the trade favours the script.

**QAS-03 — Knowledge durability.** *Scenario:* the session ends and a new one starts with no context. *Response measure:* the new session can locate `InitializeScalerStaticCaps`, the four cmp sites, and the libgcam invariant without re-deriving them. *Current state:* now satisfied by `Project-Ontology.md` §6; previously not, and it cost at least one full toolchain reconstruction (EV-17 among others). *Tradeoff:* the ontology must be updated *during* Phase 3, not after, or it decays into the same problem.

**QAS-04 — Blast radius.** *Scenario:* the 50 MP HAL patch ships and breaks an application the user has not tested. *Response measure:* the patch changes the smallest possible surface. *Current state:* the experimental patch adds RAW at every resolution (EV-16) — far more surface than the goal needs. *Tradeoff:* narrowing costs additional reverse engineering in Phase 4; shipping broad costs unknown compatibility risk. Narrowing wins because the patch is intended for distribution.

**QAS-05 — Distributability.** *Scenario:* the module is published and someone inspects the zip. *Response measure:* it contains no signing key, no 27 MB vendor blob, and no personal data. *Current state:* the blob rule holds by design; the keystore rule is unverified (EV-15, OQ-09). *Tradeoff:* none — a packaging assertion is cheap.

## 8. Open Hypotheses and Validation Probes

| ID | Hypothesis | Confidence | Next probe |
|---|---|---|---|
| H-01 | `pixelArraySize` is written from one of the six rodata dwords, reachable from the nine movz/movk sites | tentative | Disassemble around each rodata dword; find which feeds a metadata `update`/`set` call. Static, no device needed. |
| H-02 | Raising `pixelArraySize` to 8192x6144 satisfies libgcam without breaking other consumers | tentative | After H-01: patch one word, read `dumpsys` for tag `f0006`, then open the stock camera app before touching AGC. |
| H-03 | The HAL delivers remosaiced Bayer, not raw Quad-Bayer, at full resolution | tentative | Capture one DNG once H-02 passes; inspect the CFA pattern. Requires the device and the user. |
| H-04 | The 10-bit/12-bit mismatch is the only obstacle to 50 MP + LN | probable | **Confirmed for DCG, untested for LN — hence `probable`, not `confirmed`, since the hypothesis names LN.** Probe executed as written (IMPL-14 generated, IMPL-15 mounted and captured, 2026-08-31). With `dcgB` + mode 0 at 12-bit under the `fullres` HAL: camera opened, no Gcam NPE, live preview, and a valid **8192x6144 / 50.3 MP** capture with no corruption — nothing beyond the bit-depth mismatch had to move. The probe's `ln2` leg was **not** run: `ln2`/`ln4` crash AGC on their own (`FIND-2.3-02`), so composing them would confound the result. Remaining probe for the LN half: compose `ln2f`/`ln4f`+mode-0-12-bit and capture through OpenCamera, which does not use Gcam. |
| H-05 | The `tiles hide` failure is a framework-visibility issue, not a module bug | tentative | Read `tile-app/` and `service.sh`; compare against the v2.1 "read from framework, not cache" fix which solved an adjacent symptom. |
| H-06 | `customize.sh` normalizes `mode` at install, so shipping developer state is harmless | contradicted | `customize.sh` read in full: zero writes to `mode` (sole writer is `setmode.sh:204`), so it does **not** normalize. The conclusion survives for a different reason: `unzip -Z1` shows the archives ship no `mode`/`lang`/`active/` at all, and `post-fs-data.sh:14,23-27` defaults an absent/empty mode to `stock`. Shipping developer state is harmless because the state is not shipped. |
| H-07 | The WebUI passes no unsanitized input to a shell | confirmed | Exhaustive trace, not sampled: 4 `exec()` sites (`index.html:268,300,332` + def `:193/:204`), 2 `run()` callers (`:317,:325`), ids from source literals `MAIN_MODES:187`/`EXTRA:188`, `lang` from the two static buttons `:98-99`. Whitelist backstop at `action.sh:108-114` before the `sh -c` interpolation at `:131`. |
| H-08 | Patch application is ordered but not atomic against power loss | confirmed | `halpatch.sh:66-77` `hal_write` issues one `dd conv=notrunc` per entry — ordered, not atomic. Mitigating mechanism, which the bare hypothesis omits: the target is the private copy `:30`, damage is detected by `hal_state:80-87` and repaired by `hal_seed` via `hal_set:97-99`, and `hal_set:101` verifies md5 after every write. |
| H-09 | No released zip contains `debug.keystore` | confirmed | Probe run 2026-08-24 (Faz 1.2): `unzip -Z1` name-only listing of all five release zips, plus an entry-size check for the 2,664-byte keystore. Clean on both. |
| H-10 | The device's live state matches the workspace `mode` file | **contradicted** | Answered on the smoke script's first run, 2026-08-30. Device mode is `dcgB` (live blob md5 matches `dcgB.bin`); the workspace `mode` file says `stock`. They do not match. |

**Probe discipline.** Probes H-06 through H-09 are static, cheap, and answer P1/P2 questions — they should be batched into Phase 1 rather than deferred. H-01 and H-02 are the Phase 3 critical path. H-03 and H-04 require the device and the user's hands, and should not be scheduled until the probe ahead of them has passed.

**Recording rule.** Every probe that resolves must update this file's confidence column *and* `Project-Ontology.md` §8 in the same session it resolves. The project's history shows that findings deferred to "later in the session" are the ones lost to context truncation.
