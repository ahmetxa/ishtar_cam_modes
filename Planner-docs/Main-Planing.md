# Main Planing

> Step 1 master plan — ClaudeQB. Body language: English (default contract).
> The project's user-facing documents and module UI are Turkish/English bilingual; that is deliberate and unchanged.

## 1. Executive Summary

`ishtar` is not a conventional software product. It is a **device-modification and reverse-engineering workspace** for the Xiaomi 13 Ultra (codename `ishtar`, SM8550, Sony IMX989 1-inch main sensor).
The deliverable is a set of root-level (KernelSU/Magisk-format) modules plus a patched camera application that unlock imaging capabilities the stock AOSPA Android 15 build (the platform of every module result so far) does not expose: full-resolution 50 MP capture, Sony DCG (Dual Conversion Gain) sensor modes, LN2/LN4 low-noise binning modes, and a repair for the AON (Always-On Sensing) front-camera chain.
**Updated 2026-11-15 (planning run 21, `DEC-28`, `DEC-32`):** the phone runs HyperOS 4 (`OS4.0.0.44.WMACNXM`, Android 17, kernel 5.15.215; observed 2026-11-13 and installed before that, per `DEC-28`), rooted with SukiSU-Ultra (v4.3.0-r1, checked 2026-11-15). The ROM build is abandoned (`DEC-28`), and the modules are adapted to HyperOS 4 (`DEC-32`) in ClaudeQB Phase 10, which planning run 21 created for that work.
Every module result in this plan is AOSPA Android 15 evidence; no module result is measured on HyperOS 4 yet. The 50 MP HAL layer stays off on HyperOS 4 (recorded as `DEC-33` by planning run 21).

The repository is a **working reverse-engineering bench**, not a source tree. Its units of work are (a) shell modules that bind-mount or byte-patch vendor blobs at boot, (b) offset-based binary patch tables against `camera.qcom.so` and the IMX989 sensor driver `.bin`, (c) a small Java QuickSettings tile app, (d) smali-level patches to a Google Camera port (AGC), and (e) an AOSPA device tree plus three kernel checkouts kept for reference only. **Updated 2026-11-15 (planning run 21, `DEC-28`):** they were also kept for future Android 16 work, which ended when the ROM build was abandoned.

Maturity is genuinely mixed and must not be reported as uniform. The **sensor-mode layer (DCG/LN2/LN4) is mature and field-validated**: `ishtar-cam-modes` v2.1 with four mutually-exclusive QuickSettings tiles, a WebUI, a bilingual interface, and a camera-stack restart sequence that was debugged to root cause. The **50 MP HAL layer is functionally proven** for third-party apps (Open Camera measured at 50.3 MP on device). Full-resolution capture **inside the GCam port (AGC) was pursued for six weeks and has been retired as an objective** by user decision `DEC-14` on 2026-09-03; the replacement objective is that AGC runs reliably at 12.58 MP while the 50 MP layer stays enabled for every other consumer.

**Why the AGC 50 MP objective was retired, stated once so it is never re-litigated from memory.** The blocker moved four times and each move was measured, not inferred. (1) Android's `getOutputSizes()` high-resolution bucket exclusion — fixed at the APK level. (2) The absence of RAW10/RAW12 at 8192x6144 in the standard `android.scaler` table — fixed with a four-instruction HAL patch. (3) libgcam's static-metadata consistency check (`static_metadata.cc:667`), which requires the maximum raw frame size to equal the active or pixel array size — cleared by raising `f0006`, after which AGC **did** produce 50.33 MP files (`IMPL-23`, `IMPL-43`). (4) The frames are geometrically wrong for two independent, still-open reasons: the sensor keeps its 2x2 binned readout so only 12.58 MP of real pixels exist (`FIND-4.5-02` fault 1), and that payload is written into the full-size buffer without stride adaptation (fault 2). Fault 1 needs `pixelMode = MAXIMUM_RESOLUTION`, which needs the `d0014` max-resolution stream table populated — and `IMPL-47` / `IMPL-51` established that table is **not static data**: it is computed inside `InitializeScalerStaticCaps` behind a per-camera switch, with no patchable row. `IMPL-50` then established the binary has **no code cave ≥16 bytes anywhere** in its executable segment, so no additive patch is available either. Two independent walls, both measured, neither with a known path through.

That history has value beyond the retired objective: it retroactively explains the older "wide patch breaks AGC" failure recorded in Faz 4, and `IMPL-49` closed the loop by measuring that the broad RAW rows are **load-bearing for gcam's initialisation** — narrowing them prevents AGC from starting at all. This is exactly the kind of durable insight the ontology and comprehension artifacts exist to preserve, and it is the direct reason the replacement objective is framed as *stability under the broad table* rather than as *a smaller table*.

The most serious **process** risk is not technical at all: **this workspace is not under version control.** `git rev-parse` confirms the top-level directory is not a git repository. Roughly 465 MB of binaries — three ~150 MB APKs, patched and unpatched HAL blobs, sensor firmware — live here with no history, no diff, and no rollback other than manually preserved `md5` seeds inside patch tables. Expressing binary patches as offsets validated against an md5 is a sound technique, but it makes an accidental overwrite unrecoverable.

The second serious process risk is that **all validation is manual and device-only**. There is no test suite, no CI, no smoke script. Correctness evidence is `adb` output, `dumpsys media.camera` tables, `logcat` traces, and photographs. This is appropriate for the domain, but it means regressions are found by the user's own eyes and the feedback loop is measured in reboots. It has already caused at least one misattributed root cause.

The main planning conclusion: **the project should stop widening and start consolidating.** Two capability tracks (sensor modes; full resolution) are close to done on AOSPA Android 15, and the workspace itself has no safety net. The recommended order is to put the workspace under version control and lock the reverse-engineering toolchain first, then make AGC reliable alongside the 50 MP layer, then attempt the approved 12-bit mode-0 experiment, and only then open the next platform front.
**Updated 2026-11-15 (planning run 21, `AUDIT-FIX-42`):** this paragraph named a third track, Android 16 on AOSPA's `beryl` branch, as not started; that track is history. `DEC-28` abandoned the ROM build and mooted `DEC-24` and `DEC-26`, planning run 21 retired Phases 7 and 8, and the next front is the HyperOS 4 adaptation (`DEC-32`) in ClaudeQB Phase 10.

**Updated 2026-11-15 (planning run 21, `DEC-32`):** the most important next milestone is **the sensor-mode layer working on HyperOS 4 under SukiSU-Ultra**: first a read-only record of the HyperOS 4 camera stack (`Faz10.1`), then the sensor layer checked with smoke brackets (`Faz10.2`), with AGC's trap state audited and backed up before anything is cleaned (`Faz10.3`).
The former milestone, **AGC capturing reliably at 12.58 MP with the 50 MP HAL layer active**, was reached on AOSPA Android 15, and Phase 3 closed under `DEC-21` (`IMPL-40`, `IMPL-43`, `IMPL-49`; the photo size is a derived key, not a pin, per `IMPL-52`). That is AOSPA history: on HyperOS 4 the 50 MP HAL layer stays off (recorded as `DEC-33` by planning run 21), and no `4096x3072` configuration is carried over or written.

## 2. Project Vision

The long-term vision is a **single, installable, reversible module set that gives the Xiaomi 13 Ultra's IMX989 sensor its full physical capability on the ROM the phone runs**, with a switching UI simple enough to use one-handed from the notification shade. **Updated 2026-11-15 (planning run 21, `DEC-28`, `DEC-32`):** this read "on a clean AOSP-derived ROM, with none of the OEM camera stack"; the ROM build is abandoned, and the phone runs HyperOS 4 with Xiaomi's own camera stack, and the module set is adapted to it.

Intended users are, realistically, **one primary operator (the repository owner) and a small downstream community** of rooted `ishtar` users who flash KernelSU-format modules. **Updated 2026-11-15 (planning run 21, `DEC-28`):** this read "AOSPA/LineageOS `ishtar` users"; the operator now runs HyperOS 4 with SukiSU-Ultra, a KernelSU-family root manager. This is not a product with customers; it is a high-craft personal engineering artifact that others may adopt. The distribution channel is a flashable `.zip`.

The engineering value is the reverse-engineering knowledge itself: a byte-accurate map of what the Qualcomm CamX HAL and the Sony IMX989 driver blob actually do, which modes exist below the framework's advertised surface, and precisely which invariants the Google Camera engine enforces. That map is currently spread across a 1,300-line Turkish planning document and a memory store; it is the project's most valuable and most fragile asset.

When finished, the project should make the following possible on the ROM the phone runs, now HyperOS 4: pick 50 MP, DCG, LN2, or LN4 from a QuickSettings tile; have the choice survive reboot; have third-party cameras honor it at full resolution and the GCam-derived port **remain fully functional at its own working resolution rather than degrade or crash**; keep 1080p60/4K60 video unaffected; and revert cleanly to stock by disabling one module.
**Updated 2026-11-15 (planning run 21, `DEC-28`):** this read "on a stock-free AOSPA build". On HyperOS 4 the 50 MP choice stays off for now (recorded as `DEC-33` by planning run 21), so the near-term target there is DCG, LN2 and LN4; the AOSPA results stay history.

What must never be compromised:

- **Reversibility.** Every modification is a bind-mount or an offset patch guarded by an md5 check of the stock blob. A module that cannot be turned off is a bricked phone.
- **Boot safety.** Camera HAL and sensor driver modifications run at `post-fs-data`. A wrong-size or wrong-checksum write must fail closed, not write garbage.
- **Video path integrity.** 1080p60 and 4K60 must remain functional; the user has explicitly validated this and it is a standing acceptance criterion.
- **Honesty of measurement.** Claims about resolution, noise, and mode behavior are made only from on-device measurement, never from inference. The project's history contains several hypotheses that looked correct and were wrong.

## 3. Current State Analysis

**Repository structure (observed).** The working directory is flat and mixes deliverables, references, and large binaries:

- `ishtar-cam-modes/` — the primary deliverable. Shell modules (`setmode.sh` 280 lines, `action.sh` 263, `post-fs-data.sh` 131, `halpatch.sh` 116, `customize.sh` 78, `service.sh` 44), a `webroot/index.html` WebUI (344 lines), four Python analysis tools (`dcg_multimode.py`, `ln_multimode.py`, `port_sensor_mod.py`, `verify_ln.py`; 732 lines total), ten sensor `blobs/*.bin`, the `hal-fullres.patch` offset table, and a `tile-app/` Java QuickSettings app with its own `build.sh`.
- `ishtar-aon-fix/` — a three-file module (`customize.sh`, `module.prop`, `post-fs-data.sh`) that creates the missing `/vendor/lib64/camera/aon_front.pb` path, repairing the AON → CSS → NCS chain (aperture, OIS, laser AF, face-scene providers). Packaged as `ishtar-aon-fix-v1.1.zip`. Explicitly independent of KernelSU module mounting.
- `agc-50mp-yama/` — the newest area. Two smali sources (`getSupportedOutputSizes.smali`, `allOutputSizes.smali`), a `README.md`, and `hal-raw50-deneme.patch` (the experimental four-instruction HAL table).
- `50MP-Entegrasyon-Plani.md` — 60 KB, ~1,300 lines, Turkish. The de-facto engineering journal: 12 phase sections plus a user-decisions section. The single richest evidence artifact in the repository.
- `device_ishtar/`, `common_sm8550/`, `refs/{a16_ishtar,a16_sm8550,los_ishtar,los_sm8550,neo_ishtar}` — AOSPA/LineageOS device trees, present as reference only. **Updated 2026-11-15 (planning run 21, `DEC-28`):** they were also future Android 16 build input; the ROM build is abandoned.
- `android_kernel_xiaomi_sm8550/`, `android_kernel_qcom_sm8550/`, `common_sm8550/` — three kernel checkouts, present for reading only (Windows/NTFS cannot build them).
- `13U-989-DCG16+LN2+LN4/`, `Module_Highres_13U_Switcher_A14/` — the two upstream third-party modules this work was reverse-engineered from. Reference only; `Kararlar #2` states nothing from them is carried over as-is.
- Loose binaries: three AGC APKs (~150–160 MB each), `OpenCamera_50MP_...apk`, the IMX989 sensor `.bin`, two `.agc` config files, four released `ishtar-cam-modes-v*.zip` snapshots.
- `platform-tools/` — a vendored `adb`. `.claude/settings.local.json` — a permission allowlist only, no secrets.

**Implemented and strongly evidenced.** The sensor-mode layer is complete through v2.1 (`module.prop` versionCode 12): ten selectable modes, four mutually-exclusive QuickSettings tiles, launcher-visibility handling, a bilingual WebUI with a live countdown during mode switching, and a camera-stack restart sequence whose ordering bug (client → HAL, not HAL → client) was diagnosed and fixed with the reasoning preserved as comments in `setmode.sh`.
The 50 MP HAL layer worked for third-party apps via a 16-point offset patch (`LDR Wn,[Xm,#0x3d84]` → `MOV Wn,#0`) applied to the on-device AOSPA stock `camera.qcom.so`; the 27 MB blob is deliberately not shipped in the zip, only the patch table.
**Updated 2026-11-15 (planning run 21, `DEC-28`):** this paragraph is AOSPA Android 15 evidence. On HyperOS 4 neither module is installed, and the HAL `camera.qcom.so` is a different binary (md5 `2a955e68…`, not the AOSPA stock `c3fa63a8…`; measured 2026-11-13), so the patch table does not apply there; the 50 MP HAL layer stays off (recorded as `DEC-33` by planning run 21).

**Partial, and re-scoped.** The AGC 50 MP path, retired as an objective by `DEC-14` (see sections 1 and 6). As measured: the APK-side patch (`AGC8.4.300_V9.6_50MP_patched.apk`, md5 `ce65f862…`, `classes2.dex` verified against stock) makes the port see 8192x6144 and open a matching ImageReader, but capture does not complete (`Stuck shot … HDR_PLUS`); the HAL RAW patch later made AGC auto-select `RAW10 8192x6144` with no preferences set at all and *did* produce 50.33 MP files, which are geometrically wrong for two independent reasons that remain open (`FIND-4.5-02`).
**The APK patch is inert unless `pref_48m_key` is on** — with it off the build behaves identically to stock, which is why it is safe to leave installed under the replacement objective. As of the `DEC-14` re-plan (2026-09-04), the device ran HAL `ce419bc9…` (broad RAW + raised arrays + the UHR capability gate) on AOSPA Android 15.
**Updated 2026-11-15 (planning run 21, `DEC-28`):** all of this is AOSPA Android 15 evidence. On HyperOS 4 the device runs a different HAL (md5 `2a955e68…`) and the unpatched AGC V9.6 with 10 trap preferences set (measured 2026-11-13), so none of this paragraph is HyperOS 4 evidence.

**Not started.** **Updated 2026-11-15 (planning run 21, `AUDIT-FIX-42`, `DEC-28`):** ClaudeQB Phase 10, the HyperOS 4 adaptation (`DEC-32`). The four items this paragraph listed are closed. The Android 16 port on AOSPA's `beryl` branch and the kernel GKI LTS merge are history, because `DEC-28` abandoned the ROM build (mooting `DEC-24` and `DEC-26`) and planning run 21 retired Phases 7 and 8.
The mode-0 12-bit experiment ran on AOSPA Android 15 (`Faz5.1` to `Faz5.3` verified). Upstreaming the AON fix only served ROM builds: the device-tree edit was made (`Faz6.1`), and planning run 21 retires Phase 6's ROM goal, keeping the edit as history.

**Documentation state.** Unusually strong in content, weak in structure. `50MP-Entegrasyon-Plani.md` is a genuine engineering journal with measured values, rejected hypotheses, and root causes — well above typical project documentation. But it is one monolithic Turkish file with no index, non-monotonic phase numbering (Faz 10 pending while 11 and 12 are complete), and `module.prop` `description` carries a second, partly redundant changelog. There is no `README.md` at the workspace root.
**Updated 2026-11-15 (planning run 21, `DEC-32`):** "Faz 10" here is the phase numbering of `50MP-Entegrasyon-Plani.md`, not ClaudeQB Phase 10 of section 6, which is the HyperOS 4 adaptation.

**Test / CI / smoke state.** **None.** No test framework, no CI configuration, no smoke script. The four Python tools under `ishtar-cam-modes/tools/` are analysis and generation utilities, not tests — although `verify_ln.py` is the closest thing to a verification harness and should be treated as a seed for one. All acceptance evidence is manual `adb`/`dumpsys`/`logcat`/photograph.

**Configuration state.** Module configuration is a single `mode` file (currently `stock`) plus `module.prop`. Patch tables are plain-text `<offset> <stock-escape> <patched-escape>` triples guarded by md5 of both the stock and the patched result. This is simple, auditable, and self-verifying — a genuine strength worth preserving and extending.

**Operational readiness.** The install path is a flashable zip through KernelSU, and `customize.sh` has been exercised on device. However `ishtar-cam-modes-v2.1.zip` is **built but never flashed**, so the shipped artifact and the validated state are not the same thing. **Updated 2026-11-15 (planning run 21, `DEC-28`):** that install path was exercised on AOSPA Android 15 only. On HyperOS 4 the root manager is SukiSU-Ultra (`com.sukisu.ultra`, v4.3.0-r1; checked 2026-11-15), neither module is installed, and the install path is not yet exercised there.

**Security posture.** Domain-appropriate, with two concrete issues. `ishtar-cam-modes/tile-app/debug.keystore` is an app-signing keystore stored in the working tree; it is a debug key by name and role, but it is nonetheless a signing credential kept beside the artifacts it signs and must never appear in a distributed zip. Separately, all modules run as root at `post-fs-data` and write into `/odm`, the maximum-privilege position on the device — the correctness of the md5 guards is the only thing between a typo and an unbootable camera stack. No network access, no telemetry, no user data collection anywhere in the tree.

**Production readiness.** On AOSPA Android 15: sensor-mode layer effectively M5–M6 (validated end-to-end for a single user, released as a zip, used daily); 50 MP + AGC layer M4 (a single dependency verified in isolation; end-to-end does not complete). **Updated 2026-11-15 (planning run 21, `DEC-28`, `DEC-32`):** those levels are AOSPA history. On HyperOS 4 no project layer is installed or measured yet, so none has a maturity level there until ClaudeQB Phase 10 measures it. The Android 16 track (M0) is retired with Phases 7 and 8.

**Missing critical components.** Version control. A rollback story that does not depend on manually copied md5 strings. Any automated verification. A root `README.md`. **Updated 2026-11-15 (planning run 21, `AUDIT-FIX-57`):** this list also named a ROM or kernel build environment on a rented server (`DEC-24`, later `DEC-26`); that is history. No build server is used or planned, because the ROM build was abandoned (`DEC-28`).

## 4. Target End State

**Functional target.** **Updated 2026-11-15 (planning run 21, `DEC-32`):** on HyperOS 4 under SukiSU-Ultra, the user selects one of {stock, DCG-A, DCG-B, LN2, LN4, and the s/f variants} from a QuickSettings tile or the WebUI. The selection persists across reboot. The sensor layer's behaviour on HyperOS 4 is checked with a smoke bracket around each change, never assumed from AOSPA results. Video at 1080p60 and 4K60 is unaffected in every mode.
AGC's trap preferences on HyperOS 4 are audited and then cleaned with a backup taken first. The tile and WebUI chain works with SukiSU-Ultra. The adaptation ships as `ishtar-cam-modes` v2.3. The 50 MP HAL layer stays off on HyperOS 4 (recorded as `DEC-33` by planning run 21), so the 50 MP option stays off there.
AOSPA history, not carried over: on AOSPA Android 15, 50 MP mode gave Open Camera full-resolution 8192x6144 images while the AGC 8.4.300 V9.6 port kept working at 12.58 MP (`4096x3072`) in the same HAL state, and Phase 5 tested the mode-0 12-bit composition of 50 MP with LN2 and LN4; the `50mp` versus DCG/LN exclusion stays.

**Technical target.** **Updated 2026-11-15 (planning run 21, `DEC-28`, `DEC-32`):** on HyperOS 4 the HAL is not patched. Its `camera.qcom.so` differs from the AOSPA stock the patch tables are bound to (md5 `2a955e68…`, not `c3fa63a8…`; measured 2026-11-13), the module's HAL guard is expected to fail closed (not yet measured on HyperOS 4), and no 50 MP HAL work is done for now (recorded as `DEC-33` by planning run 21).
The sensor layer replaces the IMX989 sensor module file only behind its md5 guard; the HyperOS 4 file matches the module's `EXPECT_MD5` (measured 2026-11-13). The camera-stack restart keeps the ordering invariant of section 5, with the service names measured on HyperOS 4 (`Faz10.1`) rather than the AOSPA names. Every patch remains an offset table guarded by an md5 of the stock blob; no 27 MB binary is ever shipped.
AOSPA history, kept as the rule for any later HAL work: the HAL kept the **broad** RAW emission, because `IMPL-49` measured that gcam's initialisation depends on those rows and that narrowing them prevents AGC from starting; `android.sensor.info.pixelArraySize` reported the sensor's true 8192x6144 array so libgcam's consistency invariant held; AGC's own resolution was constrained **application-side**, through the preference the app already reads, not by removing sizes from the HAL.

**Operational target.** One flashable zip per release, installable and removable through SukiSU-Ultra, the KernelSU-family root manager on HyperOS 4, with an explicit stock-restore path; the next release is v2.3 (`Faz10.5`). Released zips are reproducible from the tree. The AON fix stays a separate module (`DEC-04`); its place on HyperOS 4 is settled in `Faz10.5`.
**Updated 2026-11-15 (planning run 21, `DEC-28`):** this target also fixed the AON root cause, the missing `;SYMLINK=` entry, in `device_ishtar/proprietary-files.txt` and `refs/a16_ishtar/proprietary-files.txt` so the workaround becomes unnecessary on future builds. With the ROM build abandoned there are no future builds; planning run 21 retires that goal and keeps the edit as history.

**Security target.** No signing key ships inside any distributed artifact. Every root-privileged write is preceded by a size and md5 check that fails closed. Patch application is idempotent and re-entrant across reboots.

**Testing / review / release target.** A device smoke script that, in one `adb` run, reports: active mode, HAL md5, sensor blob md5, mount state, the `dumpsys media.camera` stream-configuration rows for camera 3, and the AGC package md5. A release checklist tying each claimed capability to a command that proves it. Regression evidence recorded per release rather than per conversation.

**Observability / governance target.** The engineering journal is preserved and indexed rather than replaced. Reverse-engineering findings — function addresses, tag IDs, invariants — live in a durable ontology so they survive context loss. Each release records what was measured, on which build, with which md5s.

## 5. Architecture Direction and Key Decisions

**Core system boundaries.** Three layers, and keeping them distinct is the project's central architectural decision:

1. **Sensor driver layer** — `com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, bind-mounted over `/odm/lib64/camera/`. Owns DCG, LN2, LN4, bit depth, and the 23-entry mode table. Modified by whole-file replacement from `blobs/`.
2. **HAL layer** — `/odm/lib64/hw/camera.qcom.so`, byte-patched in place from a table. Owns which stream configurations the framework advertises. Modified by offset patch, never replaced.
3. **Application layer** — the AGC port, patched at smali level. Owns which advertised configuration is actually selected.

These layers currently **mutually exclude** each other by explicit user decision (`Kararlar #1`): 50 MP switches the HAL layer on and forces the sensor layer to stock, because sensor mode 0 is 10-bit while DCG pulls the global white level to 12-bit, which produced corrupted 50 MP output. Decision `#4` approves attempting to remove that exclusion after the rest is stable.

**Platform decisions.** **Updated 2026-11-15 (planning run 21):** `DEC-28` (user, 2026-11-13): the ROM build is abandoned, and the phone runs HyperOS 4 (`OS4.0.0.44.WMACNXM`; observed 2026-11-13 and installed before that); Phases 7 and 8 lose their purpose, and `DEC-07`, `DEC-08`, `DEC-22`, `DEC-24`, `DEC-25` and `DEC-26` are moot. `DEC-32` (user, 2026-11-13): adapt the module to HyperOS 4, with the scope settled by planning run 21.
Planning run 21 carries that adaptation in ClaudeQB Phase 10, formally retires Phases 7 and 8, and retires Phase 6's ROM goal because the ROM build is gone. `DEC-33`, recorded by planning run 21: no 50 MP HAL work for now; the HAL layer stays off on HyperOS 4 and the sensor layer continues. Retired work is kept as history and is not revived.

**Source-of-truth decisions.** The device is the source of truth for behavior; the journal is the source of truth for findings; the patch tables are the source of truth for what is applied. `module.prop` `description` should stop being a second changelog — the journal owns history.

**State ownership.** Runtime mode state is a single file (`$MODDIR/mode`) read by `setmode.sh`, `action.sh`, the tiles, and the WebUI. That single-writer design is correct and should be preserved; the tile-synchronization bug fixed in v1.5 was a violation of it.

**Integration boundaries.** `adb` is the only host↔device channel. The KernelSU-family root manager is the only privilege channel. **Updated 2026-11-15 (planning run 21, `DEC-28`):** this read "KernelSU"; it is a KernelSU manager on AOSPA Android 15 and SukiSU-Ultra on HyperOS 4. The camera framework (`cameraserver`, `vendor.camera-provider`) is restarted, never replaced — and the **client-before-HAL ordering is an invariant**, not a preference: reversing it leaks CSIPHY/CSID allocations in the QCOM kernel driver and produces a black preview in *every* mode, including stock.

**Security and policy boundaries.** All module code runs as root at `post-fs-data`. The guard model is: check size, check md5 against the recorded stock value, then write. No network access, no telemetry, no user data. The signing keystore is a build-time input and must be excluded from every distributed artifact.

**Artifact / evidence boundaries.** Patch tables carry the md5 of both the stock input and the patched result, which makes them self-verifying. This convention should be extended to every binary the project touches, including sensor blobs.

**Human approval boundaries.** Anything requiring physical interaction with the phone — flashing, dismissing a permission dialog, taking a photograph — is the user's action. Read-only `adb` inspection is delegated. This split is already established and works well.

## 6. Phase-Based Master Roadmap

Phases below are the master roadmap **from the current state forward**. They do not renumber or replace the existing Faz 1–12 history in `50MP-Entegrasyon-Plani.md`; that document remains the historical record.

| # | Phase | Goal | Maturity | Token/context risk |
|---|---|---|---|---|
| 1 | Workspace safety net | Version control + toolchain lock | M2 | low |
| 2 | Ship and re-baseline v2.1 | Close the built-but-unflashed gap | M4 | low |
| 3 | AGC stable at 12.6 MP under 50 MP | Coexistence, not full-res in AGC; closed on AOSPA A15 only (`DEC-21`) | M5 | low |
| 4 | Minimal correct HAL patch | Duration rows; narrowing retired | M5 | medium |
| 5 | Mode-0 12-bit composition | 50 MP + LN together | M5 | medium |
| 6 | AON fix upstreaming | Remove the workaround; ROM upstreaming retired 2026-11-15 by planning run 21 (`DEC-28`), `Faz6.2` stays verified | M4 | low |
| 7 | Android 16 build environment | Retired 2026-11-15 by planning run 21 (`DEC-28`). Was: first AOSPA `beryl` build from GitHub-staged inputs | M3 | medium |
| 8 | Camera work on Android 16 + kernel LTS | Retired 2026-11-15 by planning run 21 (`DEC-28`). Was: camera patches on the `beryl` vendor blobs; kernel merge | M5 | high |
| 9 | Release engineering | Reproducible, documented releases | M6 | low |
| 10 | HyperOS 4 camera module adaptation | Measure the HyperOS 4 stack; adapt sensor layer, AGC traps, tile; ship v2.3 | M5 | medium |

### Phase 1 — Workspace safety net

**Goal.** Make the workspace recoverable and the reverse-engineering toolchain reproducible.

**Description.** Initialize version control with a `.gitignore` that excludes the ~465 MB of binaries (APKs, kernel checkouts, `platform-tools/`) while tracking every script, patch table, smali source, and document. Record the toolchain as a written, re-runnable procedure: Temurin JDK 21, smali/baksmali 2.5.2 from the legacy `org/smali` Maven group, uber-apk-signer 1.3.0, embeddable Python plus capstone and pyelftools. Record explicitly that apktool's bundled smali `Main` classes are stripped stubs and that radare2 does not complete on this binary — the negative findings are as valuable as the positive ones and cost real time to discover. Add a root `README.md` explaining each top-level directory.

**Desired end state.** A `git log` exists. A fresh machine can rebuild the analysis toolchain from written steps. Nothing in the tree is unexplained.

**Acceptance signals.** `git status` is clean and meaningful; tracked content is well under 50 MB; the toolchain procedure has been followed once end-to-end.

**First vibecoding slice.** Write `.gitignore` and `git init`; commit only `ishtar-cam-modes/`, `ishtar-aon-fix/`, `agc-50mp-yama/`, and the journal.

### Phase 2 — Ship and re-baseline v2.1

**Goal.** Eliminate the discrepancy between the released zip and the validated device state.

**Description.** `ishtar-cam-modes-v2.1.zip` was built on 2026-08-22 and has never been flashed. Flash it, then run a full regression pass across all ten modes: tile synchronization, launcher icon rendering (the v2.1 fix), mode persistence across reboot, camera-stack restart without black preview, and 1080p60/4K60 video. Decide the fate of the `tiles hide` option, which is recorded as ineffective.

**Desired end state.** The shipped artifact equals the validated artifact, with the evidence written down.

**Acceptance signals.** Every mode switches and the camera opens; video unaffected; reboot persistence confirmed; a written regression record exists.

**First vibecoding slice.** Flash, then capture a single `dumpsys` + `md5` state snapshot as the baseline all later work is diffed against.

### Phase 3 — AGC stable at 12.6 MP under 50 MP

**Objective changed 2026-09-03 by user decision `DEC-14`.** The former objective — "make a 50 MP capture actually complete inside the AGC 8.4.300 V9.6 port" — is **retired, not deferred**, on the evidence summarised in section 1. It should not be reopened without new evidence about either the `d0014` computation or the absence of code-cave space, both of which are measured negatives rather than unexplored ground. The six sub-plans that executed under the old objective (`Faz3.1` … `Faz3.6`) stay `verified`; their findings are what retired the objective and are not invalidated by it.

**Goal.** With the 50 MP HAL layer enabled, AGC launches, previews, captures and saves a clean 12.58 MP (`4096x3072`) image — reproducibly, across a reboot and a mode switch — while Open Camera continues to capture at the full 8192x6144 in the same HAL state. **Updated 2026-11-15 (planning run 21, `DEC-28`):** reached on AOSPA Android 15 and closed under `DEC-21`; AOSPA evidence only. On HyperOS 4 nothing of it is verified or carried over, the 50 MP HAL layer stays off (recorded as `DEC-33` by planning run 21), and `Faz10.2` and `Faz10.3` measure the AGC state first.

**Description.** This is a coexistence goal, and most of it has already been observed working at least once; the work is turning single observations into a pinned, verified, reproducible state. Three facts define the approach. First, **the HAL table is left broad**: `IMPL-49` measured that removing the wide RAW rows prevents AGC from starting at all (gcam engine NPE), so narrowing is not a route to stability — it is the opposite. Second, **AGC's resolution is decided application-side**: `IMPL-43` confirmed AGC opens exactly the reader that `pref_camera_picturesize_back_key` names — but that key is a **derived** value rather than an input, so it is not a pin point, as the third fact below establishes. The settable surface is an ordinary visible `ListPreference` (`pref_camera_resolution`, category `pref_category_resolution_camera`, gated by no `dependency`), so this needs a *setting*, not a patch. Third — **corrected 2026-09-04 by `IMPL-52`, which measured the mechanism instead of inferring it** — **`pref_48m_key` gates the derivation, and leaving it on *does* force the 50 MP selection.** `pref_camera_picturesize_back_key` is a **derived** value, not a settable pin: AGC re-derives it from `pref_camera_resolution` on every start, so a direct write is reverted (measured twice, under both `full` and `medium`, with the file's owner, mode and SELinux label preserved so the write itself is not the variable). The surface behind `pref_camera_resolution` is a **two-value** `ListPreference` — *Full resolution* / *Medium resolution* — and with `pref_48m_key`=**1** those two values derive **8192x6144** and **1920x1440**. `4096x3072` is therefore not expressible through either route in that state, which is the opposite of what this fact previously asserted. **This also narrows the second fact above:** `IMPL-43`'s "proximate selector" conclusion holds for *what AGC opens*, but the key is not an independent input and so is not a pin point; that sentence has been corrected in place accordingly (2026-09-07), so the second fact no longer asserts a pin point the third fact removes. The hypothesis this raises — that with `pref_48m_key`=**0** *Full resolution* derives `4096x3072` — is untested, and is `DEC-17`, answered **yes** on 2026-09-04: `Faz3.7` may write the key, as a measured variable with its own bracket. **Attribution:** every figure in this fact was measured on the *experimental* base `ce419bc901bea61945d166aee11e1ab0` and does **not** transfer to the shipped `fullres` base (`fe0245a4720fb07b01d96deef47f5569`) by assumption; per `DEC-15` the experiment is re-run there, since the two bases advertise different tables and AGC derives its list from what the base advertises.

The open question this phase must actually answer is **stickiness**, not feasibility: whether the pinned size survives a reboot, a QuickSettings mode switch, an AGC cold start, and a camera-stack restart — and what AGC does if it is left unpinned, since its default behaviour is to select the largest advertised size, which is the 50 MP path that produces an unusable frame.

**Desired end state.** A written, reproducible AGC configuration that yields a clean 12.58 MP capture with the 50 MP layer active, with the survival behaviour across reboot and mode switch measured rather than assumed, and with the failure mode (unpinned AGC selecting 50 MP) documented so a future reader recognises it immediately.

**Acceptance signals.** `dumpsys media.camera` with AGC open shows the configured stream at `4096x3072`; the saved file measures 12.58 MP with a black fraction comparable to `IMPL-40`'s 0.0024 reference rather than the ~0.75 fold signature; Open Camera in the same HAL state still captures 50.3 MP; the state is re-verified after one reboot and one tile switch; camera enumeration stays at 13 devices. **Updated 2026-11-15 (planning run 21, `DEC-28`):** met on AOSPA Android 15 (Phase 3 closed under `DEC-21`); these are not HyperOS 4 acceptance signals.

**First vibecoding slice.** Set `pref_48m_key`=`0` and `pref_camera_resolution`=`full` on device, then read back what `pref_camera_picturesize_back_key` *derives to* — do **not** write that key, because `IMPL-52` measured it is derived and reverted at every AGC start, which is what the third fact above says. Take one bracketed capture and measure the black fraction — this is a few minutes of work and it either confirms the whole phase's premise or falsifies it immediately.

**Risk note.** The one real risk is silent regression: AGC re-selecting 50 MP after an update, a preference import, or a cold start, and the user discovering it through a bad photograph rather than a check. The mitigation is that the smoke script should report AGC's selected size alongside the HAL md5, so the state is visible without opening the app. Note also that both root `.agc` config files still carry all twelve `pref_raw_key_N` / `pref_fix_resolution_key_N` trap keys — importing either re-arms the trap that independently breaks Gcam initialisation.

### Phase 4 — Minimal correct HAL patch

**Goal.** Make the shipped HAL patch internally consistent and packageable. **Narrowing is no longer part of this goal** (`DEC-14`, 2026-09-03).

**Description.** The four-instruction experiment (`cmp wN,#2` → `cmp wN,#5` at four sites in `InitializeScalerStaticCaps`, 0x16bf4c0–0x16c5a90) adds RAW formats at *every* resolution, growing the stream-configuration array from 508 to 868 int32 entries. The original plan was to narrow that to the QCFA full-resolution dimension only. **`IMPL-48` through `IMPL-50` measured that this cannot be done:** the narrowing hits every numeric target and still prevents AGC from launching, 3/3 at two independent bisection stages, because the removed rows are load-bearing for gcam's initialisation — and the format-32 extension that would have made the narrowed table complete has no additive implementation, the binary having no code cave ≥16 bytes. What remains in scope is the honest part of the original goal: add the `availableMinFrameDurations` and `availableStallDurations` rows the emitted entries require, and consolidate the accumulated experimental tables into one packageable artifact with a verified revert path.

**Desired end state.** One consolidated, md5-guarded patch table carrying the broad emission, with the superseded experiments clearly marked as experiments rather than deleted. **The duration rows need no work and this goal no longer claims they do — re-measured 2026-09-07: camera 0 carries 111 `d000a` OUTPUT entries and 111 matching `d000b` four-tuples, zero missing.** The one incomplete table is `d000c` (stall durations), 15 four-tuples against those same 111 entries; it has no additive implementation, the binary having no code cave large enough, so it is **out of scope rather than pending**.

**Acceptance signals.** `dumpsys media.camera` shows the 8192x6144 entries with their matching `d000b` rows as **BLOB (33), IMPLEMENTATION_DEFINED (34), YUV_420_888 (35) and 54** — re-measured 2026-09-07, those are the only formats present at that resolution in either direction. **RAW10 (37) is not among them, so the previous wording of this signal, which demanded RAW10 at 8192x6144, could never pass and has been corrected here.** The 50.3 MP path is BLOB, which is the format Open Camera actually uses and the one measured in its capture. Open Camera still captures 50.3 MP; **AGC still launches and captures cleanly at 12.58 MP** — the criterion `IMPL-49` showed the old narrowing goal silently violated.

**First vibecoding slice.** Locate the two default-mode duration tables (`d000b` / `d000c`) and add justified rows for the entries already emitted, measuring the array delta per camera id.

### Phase 5 — Mode-0 12-bit composition

**Goal.** Execute the user-approved experiment to let 50 MP and LN2/LN4 coexist.

**Description.** Sensor mode 0 (50 MP) is 10-bit while DCG raises the global white level to 12-bit, which is why the layers currently exclude each other. Decision `#4` approves moving mode 0 to 12-bit after everything else is stable. This is a sensor-blob edit using the existing `tools/` generation scripts, and it is explicitly single-purpose: if it fails, only this change is reverted.

**Desired end state.** Either 50 MP + LN2/LN4 work together, or a written negative result explaining why not.

**Acceptance signals.** A 50 MP frame with LN active, compared against 50 MP alone for noise and detail; or a clean revert with the failure mode documented.

**First vibecoding slice.** Generate the 12-bit mode-0 blob, verify with `verify_ln.py`, and test in a temporary bind-mount before committing it to `blobs/`.

### Phase 6 — AON fix upstreaming

**Goal.** Remove the need for the `ishtar-aon-fix` workaround module.

**Description.** The root cause is recorded: a missing `;SYMLINK=` entry for `aon_front.pb`. Both `device_ishtar/proprietary-files.txt` and `refs/a16_ishtar/proprietary-files.txt` currently contain **zero** `SYMLINK` entries — verified in this run — so the fix has not been applied to either tree. Add the entry so future builds create the path natively, and keep the runtime module only as a fallback for already-built ROMs.

**Updated 2026-11-15 (planning run 21, `DEC-28`):** upstreaming into a ROM build is retired by planning run 21, because the ROM build was abandoned on 2026-11-13 and no future build will carry the entry. The zero count above predates `Faz6.1`, which added the entry to both trees (`IMPL-03`, 2026-08-24); no build ever tested its effect. `Faz6.1` becomes `superseded` (set by planning run 21; rationale `DEC-28`); `Faz6.2`, the module's disposition (`DEC-04`: keep separate), stays `verified`.

**Desired end state.** The device tree produces a working AON → CSS → NCS chain without a runtime module. **Updated 2026-11-15 (planning run 21, `DEC-28`):** retired with the ROM build; no device-tree build will be made, so this end state stays history.

**Acceptance signals.** The entry is present in both trees; on a build that includes it, the NCS providers for aperture, OIS, laser AF, and face-scene appear without `ishtar-aon-fix` installed. **Updated 2026-11-15 (planning run 21, `DEC-28`):** the first half is met (`Faz6.1`, `IMPL-03`); the second needs a ROM build and is retired with it.

**First vibecoding slice.** Add the single line to `device_ishtar/proprietary-files.txt` and mirror it to `refs/a16_ishtar/`. This is a one-line change and should not wait for Phase 7. **Updated 2026-11-15 (planning run 21, `DEC-28`):** `Faz6.1` added the line (`IMPL-03`); with Phase 7 retired, no build will test it. The place of `ishtar-aon-fix` on HyperOS 4 moves to `Faz10.5`: the 2026-11-13 probe found the `aon_front.pb` link in the HyperOS 4 ROM itself, so the module's boot script would exit without acting (code reading, not yet measured).

### Phase 7 — Android 16 build environment

**Status.** Retired 2026-11-15 by planning run 21 under `DEC-28` (ROM build abandoned 2026-11-13; the phone runs HyperOS 4); the HyperOS 4 adaptation (`DEC-32`) continues in Phase 10. Kept as history; do not revive. `Faz7.2` and `Faz7.3` become `superseded` (set by planning run 21; rationale `DEC-28`); `Faz7.1` keeps its `verified` state as history.

**Updated 2026-11-15 (planning run 21, `AUDIT-FIX-57`):** no build server is used or planned, because the ROM build was abandoned (`DEC-28`). The rented Hetzner VDS in the description below (`DEC-24`; `DEC-26` later changed the provider) and the server distribution in the note (`DEC-22`) are closed history, and this retirement answers this section's part of `AUDIT-FIX-57` (the 12th audit rules on it); `DEC-28` moots `DEC-22`, `DEC-24`, `DEC-25` and `DEC-26`.

**Goal.** Reach the point where an AOSPA Android 16 (`beryl`) build for `ishtar` can be attempted, at the lowest rental cost.

**Description.** Neither the kernel nor AOSP can build on the Windows host: the workspace's kernel checkouts already carry 14 case-collision paths and needed a sparse-checkout trick excluding three DOS-reserved filenames. WSL2 will not be installed — on 2026-09-10 the user decided (`DEC-24`) to build on a rented Hetzner VDS. Rental is billed by time, so every input the build needs is prepared on the user's GitHub account (`ahmetxa`) before a server is rented: the device tree carrying the project's changes, a local manifest pinning every other input to a full commit id, and the provisioning and build procedure. The `beryl` inputs already exist upstream under `xiaomi-8550` — the device and common trees, both vendor blob repositories and both kernel trees carry `beryl` branches — so the work is pinning inputs and closing gaps, not porting. `calcite` is evaluated only after `beryl` builds and boots.

**Desired end state.** One AOSPA `beryl` build for `ishtar` completed on a rented VDS from inputs staged on GitHub, with the output retrieved and the server released.

**Acceptance signals.** A flashable build output exists and boots; the rental time the build consumed is recorded.

**First vibecoding slice.** Before renting anything, stage the device tree and a local manifest on GitHub and prove from the Windows host that every pinned project resolves to a commit on its branch.

**Note.** The server's distribution (`DEC-22`) is decided from the AOSPA build requirements before renting. Flashing and the boot check remain the user's actions.

### Phase 8 — Camera work on Android 16 and kernel LTS merge

**Status.** Retired 2026-11-15 by planning run 21 under `DEC-28` (ROM build abandoned 2026-11-13; the phone runs HyperOS 4); the HyperOS 4 adaptation (`DEC-32`) continues in Phase 10. Kept as history; do not revive. `Faz8.1` and `Faz8.3` become `superseded` (set by planning run 21; rationale `DEC-28`); `Faz8.2` keeps its `verified` state as history.

**Updated 2026-11-15 (planning run 21, `DEC-28`):** `DEC-28` moots `DEC-07` and `DEC-08`. `AUDIT-FIX-22`, `-37` and `-50`, owned by work items in `Faz8.1`, `Faz7.3` and `Faz8.3`, lose their owners; the 12th audit reassigns them. The md5 comparison in the first slice below was made on HyperOS 4 by the 2026-11-13 probe instead, and Phase 10 starts from its result.

**Goal.** Carry the project's camera work onto the Android 16 build and bring the kernel up to date.

**Description.** `beryl` is AOSPA's Android 16 branch, not a second device; this phase previously read it as a second Xiaomi target, which was corrected on 2026-09-10. Phase 7 builds `ishtar` itself on `beryl`. What remains is (1) the camera module work on the vendor blobs that build ships — every HAL and sensor patch is bound to one exact vendor build (Project-Ontology invariant 10) — and (2) merging GKI LTS into the kernel tree. The `beryl` device tree's history carries the same last blob update as the Android 15 tree (`OS2.0.101.0.VMAMIXM`), so the patches may carry over unchanged; that stays unverified until the binaries are compared. Both parts depend on Phase 7.

**Desired end state.** The camera modes work on the Android 16 build, and the kernel tree is on a current LTS base.

**Acceptance signals.** The module's md5 guards accept the Android 16 camera HAL and sensor module, or the patches are re-derived for them, and the release checklist passes on that build; kernel merge with no regressions in camera or sensor paths.

**First vibecoding slice.** Compare the `beryl` vendor blobs' `camera.qcom.so` and IMX989 sensor module against the md5s the module guards, before committing to any re-derivation.

### Phase 9 — Release engineering

**Goal.** Make releases reproducible, documented, and verifiable.

**Description.** A build script that produces the zip from the tree; a smoke script that reports device state in one `adb` run; a release checklist mapping each claimed capability to a proving command; a decision on whether the AON module merges into the main module. Move the changelog out of `module.prop` `description` and into the journal or a `CHANGELOG.md`.

**Desired end state.** The next release is produced by a script, verified by a script, and documented in one place.

**Acceptance signals.** A release built from a clean checkout matches the shipped artifact **across every tracked file**. Byte-for-byte reproduction of the whole archive is **not** the signal and never was attainable: `.gitignore` deliberately excludes `ishtar-cam-modes/blobs/*.bin`, so a clean checkout does not carry the sensor blobs at all (`FIND-9.1-02`). The exclusion is correct and the original signal was wrong; corrected 2026-09-07. The smoke script correctly reports both a known-good and a known-bad state.

**First vibecoding slice.** Write the smoke script first — it pays off immediately in Phases 2 through 5.

### Phase 10 — HyperOS 4 camera module adaptation

**This is ClaudeQB Phase 10**, added 2026-11-15 by planning run 21 (a user choice under `DEC-28` and `DEC-32`): Step 2 writes its sub-plans to `Planner-docs/Faz-10-Plans`, and it is not the "Faz 10" of `50MP-Entegrasyon-Plani.md`, which numbers its journal sections separately.

**Goal.** Adapt the module to HyperOS 4 (`DEC-32`): measure the HyperOS 4 camera stack first, then bring the sensor layer, the AGC trap cleanup and the tile and WebUI chain onto it, and release v2.3. The 50 MP HAL layer stays off on HyperOS 4; there is no 50 MP HAL work for now, recorded as `DEC-33` by planning run 21.

**Description.** As observed on 2026-11-13, the phone runs HyperOS `OS4.0.0.44.WMACNXM` (Android 17, kernel 5.15.215, SELinux enforcing; installed before that observation, per `DEC-28`), rooted with SukiSU-Ultra, and the project's modules are not installed on it. Every module result so far (v1.x to v2.2, the AGC rules, 12-bit mode 0, AON) is AOSPA Android 15 evidence; nothing is measured on HyperOS 4 yet, so the phase measures before it changes anything. The five sub-plans, in implementation order:

- `Faz10.1` — read-only measurement and record of the HyperOS 4 camera stack: service names (Project-Ontology invariant 3, the restart ordering), `chcon`/SELinux labels, the KernelSU allowlist, the root manager and WebUI. Depends on: none.
- `Faz10.2` — sensor layer: v2.2 unchanged on HyperOS 4 under a smoke bracket (installation by the user); the 50 MP option stays off on HyperOS 4 (`DEC-33`); `setmode.sh` service names. Depends on: `Faz10.1`.
- `Faz10.3` — AGC trap audit and a backed-up, guarded cleanup on HyperOS 4. Depends on: `Faz10.1`.
- `Faz10.4` — tile and WebUI chain adapted to SukiSU-Ultra; the idea of a system app with the same interface is evaluated. Depends on: `Faz10.1`.
- `Faz10.5` — v2.3 release: `Kullanim.txt` (`DEC-29`), version locations, CHANGELOG, release manifest, module comments, tile-app `versionName`; the place of `ishtar-aon-fix` on HyperOS 4. Depends on: `Faz10.2`-`Faz10.4`.

**Entry evidence.** Read-only device measurements on 2026-11-13 and 2026-11-15, none with a project module installed:

- Probe 2026-11-13: HyperOS `OS4.0.0.44.WMACNXM`, Android 17, kernel 5.15.215, SELinux enforcing. The camera HAL `camera.qcom.so` (md5 `2a955e68…`) is not the AOSPA stock `c3fa63a8…` but a different binary, so `R8` has happened and the module's HAL-layer guard would fail closed (inference, not yet measured with the module). The IMX989 sensor module (md5 `9e4d0fe1…`) equals the module's `EXPECT_MD5`.
- Probe 2026-11-13: `ishtar-cam-modes`, `ishtar-aon-fix` and the tile app are not installed. AGC (`org.codeaurora.snapcam`) is the unpatched V9.6 with 10 trap preferences set (value 37). The `aon_front.pb` link that `ishtar-aon-fix` supplied on AOSPA ships in the HyperOS 4 ROM itself.
- Read-only check 2026-11-15: root is SukiSU-Ultra v4.3.0-r1 (manager `com.sukisu.ultra`, versionCode 41140); `su` works from the adb shell without a dialog; no metamodule is installed. KernelSU-Next (`com.rifsxd.ksunext`), the target of the tile's long press, is not installed.
- Read-only check 2026-11-15: the running camera services are `cameraserver`, `vendor.camera-provider` and `vendor.camera-provider-2-7-ext-uvc`. `vendor.camera-provider-2-7-ext` is defined but not running; `setmode.sh` uses the AOSPA service names, and its restart would start that service (inference, not measured). The HAL and the sensor module file are labelled `vendor_file`.
- Read-only check 2026-11-15: AGC's preference files have an owner and SELinux label that differ from the AOSPA constants, so the AOSPA-only, backup-less cleanup procedure (`docs/phase3-preconditions.md:71-119`) does not carry over to HyperOS 4.

**Desired end state.** `ishtar-cam-modes` v2.3 is released and runs on HyperOS 4: the sensor-layer modes work with the 50 MP option off, AGC carries no armed trap preference, the tile and WebUI work under SukiSU-Ultra, and every capability claim rests on HyperOS 4 evidence rather than on the AOSPA record.

**Acceptance signals.** The phase exits when all of these hold:

- `Faz10.1`'s record lists the HyperOS 4 camera service names, the file labels, the KernelSU allowlist, the root manager and its WebUI entry point, each with its measurement date.
- A smoke bracket on HyperOS 4 shows the sensor guard passing, every mode except `50mp` switching with the camera opening, the mode surviving a reboot, and 1080p60/4K60 video unaffected; the HAL layer stays off, its guard failing closed on the HyperOS 4 HAL.
- AGC shows no armed trap preference after a cleanup whose backup was taken and checked first; `pref_camera_picturesize_back_key` was not written and no `.agc` file was imported.
- The tile switches modes and its long press opens a working WebUI under SukiSU-Ultra; the system-app idea has a recorded evaluation.
- v2.3 passes the release checklist with `Kullanim.txt` corrected (`DEC-29`) and every version location in agreement, and the place of `ishtar-aon-fix` on HyperOS 4 is decided and recorded.

**First vibecoding slice.** `Faz10.1`'s read-only pass: list the camera services init defines and runs, the labels the module's `chcon` calls would meet, the KernelSU allowlist and how the SukiSU-Ultra WebUI is launched, before anything is installed.

**Note.** The module invariants carry over unchanged: AGC 50 MP stays disabled without new evidence (`DEC-14`); the wide RAW table is not narrowed; `pref_camera_picturesize_back_key` is never written directly and preferences are never edited with `sed -i`; no `.agc` import; trap cleanup only with a backup; the client-before-HAL restart ordering holds; the `50mp` versus DCG/LN exclusion stays. Installing, flashing and every capture remain the user's actions.

**Risk note.** Token/context risk: medium. No reverse engineering is planned, because there is no 50 MP HAL work for now (`DEC-33`), so sessions are measurement and small script changes. The real risk is device state — a restart that starts an unused service, or a trap cleanup without a backup — so every device step runs inside a smoke bracket.

## 7. Critical Risks and Gaps

**R1 — No version control (severity: critical).** `git rev-parse` confirms this is not a repository. Roughly 465 MB of irreplaceable binaries and hand-derived patch tables have no history and no rollback. *Impact:* a single overwrite destroys work that took weeks and cannot be regenerated without repeating the reverse engineering. *Mitigation:* Phase 1, first action, before any further patching.

**R2 — Signing keystore in the working tree (severity: high).** `ishtar-cam-modes/tile-app/debug.keystore` sits beside the artifacts it signs. *Impact:* if it is ever swept into a distributed zip or a public repository, anyone can sign an update the device accepts as the same app. *Mitigation:* exclude it from packaging and from version control explicitly; verify no released zip already contains it.

**R3 — Root-privileged writes with only md5 guards (severity: high).** Every module writes into `/odm` as root at `post-fs-data`. *Impact:* a wrong offset or a stale md5 corrupts the camera HAL, which on this device means no camera until reflash. *Mitigation:* keep the fail-closed size+md5 discipline; add an explicit stock-restore path to the smoke script; never patch without the stock md5 matching first.

**R4 — CLOSED as a risk, realised as an outcome (was: high, Phase 3).** The risk read "the project's headline goal, 50 MP in the user's actual camera app, could stall." It did, and the objective was retired by `DEC-14` rather than left stalling. The libgcam invariant itself was **satisfied** (`IMPL-23`: zero `static_metadata.cc:667` rejections, `HdrPlusSession Created`, three 50.33 MP files) — the walls were further in: binned sensor readout gated behind a non-static `d0014` table, and no code-cave space for an additive fix. Retained here rather than deleted, because a future reader who meets the 50 MP idea again should find the measured negative attached to it. **The replacement risk is `R12`.**

**R12 — AGC silently reverting to 50 MP (severity: medium, Phase 3).** AGC's default behaviour is to select the largest advertised size, which under the broad HAL table is the 8192x6144 path that yields an unusable frame. *Impact:* the user discovers the regression through a bad photograph rather than a check, which is exactly the feedback-loop failure `R5` describes. *Mitigation:* pin the size through the app's own preference, report AGC's selected size in the smoke script alongside the HAL md5, and re-verify after any AGC update or `.agc` config import.

**R5 — Zero automated verification (severity: high).** No tests, no CI, no smoke script. *Impact:* regressions surface only when the user notices them, sometimes days later; several past failures were misattributed because state was not captured before and after a change. *Mitigation:* Phase 9's smoke script, pulled forward to the start of Phase 2.

**R6 — Built-but-unflashed release (severity: medium).** `v2.1` exists as a zip and has never run on the device. *Impact:* the artifact a user would install is unvalidated. *Mitigation:* Phase 2.

**R7 — Knowledge concentrated in one long document (severity: medium).** `50MP-Entegrasyon-Plani.md` is 1,300 lines, Turkish, with non-monotonic phase numbering. *Impact:* context loss between sessions has already caused rediscovery of solved problems and one misattributed root cause. *Mitigation:* the ontology and comprehension artifacts produced by Step 1.5; keep the journal as history, not as the lookup surface.

**R8 — Vendor blob dependency (severity: medium, structural; realised, observed 2026-11-13).** Every patch is bound to one exact build of `camera.qcom.so` (27,268,688 bytes, md5 recorded in the patch table). *Impact:* any AOSPA update that changes the blob invalidates all sixteen-plus offsets at once. *Mitigation:* keep the md5 guard as the detector, and keep the disassembly *method* documented so offsets can be re-derived rather than re-discovered from scratch.
**Updated 2026-11-15 (planning run 21, `DEC-28`):** R8 has happened. HyperOS 4's `camera.qcom.so` (27,305,440 bytes, md5 `2a955e68…`; measured 2026-11-13) is not the AOSPA stock `c3fa63a8…`, so every HAL offset is void there, and the module's HAL guard would fail closed (not yet measured with the module on HyperOS 4). The IMX989 sensor module file still matches `EXPECT_MD5`. No re-derivation is planned now (recorded as `DEC-33` by planning run 21).

**R9 — Windows host cannot build (severity: medium; moot since `DEC-28`).** NTFS case-insensitivity already breaks kernel checkouts, and WSL2 will not be installed. **Updated 2026-11-15 (planning run 21, `AUDIT-FIX-57`):** no build server is used or planned, because the ROM build was abandoned (`DEC-28`); R9 is moot. *Impact:* none while no ROM or kernel is built. *Mitigation:* none needed; the former one, a rented build server with every input staged on GitHub (`DEC-24`, later `DEC-26`, both mooted by `DEC-28`), is history.

**R10 — Token/context risk in reverse-engineering phases (severity: medium).** Phase 3 involved disassembling a 27 MB stripped binary until `DEC-14` (2026-09-03) made it configuration work. **Updated 2026-11-15 (planning run 21, `DEC-28`):** no disassembly is planned now, because the 50 MP HAL layer stays off on HyperOS 4 (recorded as `DEC-33` by planning run 21); the risk returns if HAL work on the HyperOS 4 `camera.qcom.so` is reopened.
*Impact:* long sessions, context exhaustion, repeated re-derivation. *Mitigation:* record every located address in the ontology immediately, not at the end of the session; prefer scripted extraction over interactive exploration.

**R11 — Mixed-language documentation (severity: low).** The journal and module UI are Turkish; planner artifacts are English. *Impact:* minor friction for future readers. *Mitigation:* accept it deliberately — user-facing Turkish, planner-facing English — and state the convention explicitly, as this document does.

## 8. Prioritized Next Steps

1. **Initialize version control with a binary-excluding `.gitignore`.** *Type: implementation slice (Phase 1).* The highest-leverage action in the entire plan; everything else becomes safer once it exists.
2. **Write the device smoke script.** *Type: validation action (Phase 9, pulled forward).* One `adb` invocation reporting mode, HAL md5, sensor md5, mount state, camera-3 stream rows, and AGC md5. Pays for itself across Phases 2–5.
3. **Flash `ishtar-cam-modes-v2.1.zip` and record a regression baseline.** *Type: validation action (Phase 2).* Closes the built-but-unflashed gap; requires the user's hands on the device.
4. **Add the missing `;SYMLINK=` entry to both `proprietary-files.txt` trees.** *Type: implementation slice (Phase 6).* Originally verified absent (zero SYMLINK entries in both); the edit was made by `Faz6.1` (`IMPL-03`), but its effect needs a ROM build. **Updated 2026-11-15 (planning run 21, `DEC-28`):** retired with Phase 6's ROM goal, because the ROM build is abandoned; kept as history, not a next step.
5. **Configure AGC for a 12.58 MP (`4096x3072`) photo size and verify one clean capture.** *Type: implementation slice (Phase 3, replaces the retired `pixelArraySize` search, which `IMPL-18`/`IMPL-20` completed anyway).* Done on AOSPA Android 15 and closed under `DEC-21`: the measured configuration is `pref_48m_key=0` with `pref_camera_resolution=full`, and the derived `pref_camera_picturesize_back_key` is read back, never written (`IMPL-52`).
**Updated 2026-11-15 (planning run 21, `AUDIT-FIX-41`):** this step is AOSPA Android 15 evidence (Phase 3, `DEC-14`). On HyperOS 4 nothing of it is verified, nothing is carried over and no AGC preference is written: `Faz10.2` and `Faz10.3` measure the AGC state first, and `pref_camera_picturesize_back_key` is never written directly.
6. **Exclude `debug.keystore` from packaging and version control.** *Type: security hardening (Phase 1).* Trivial to do, expensive to have skipped.
7. **Add the missing duration rows for the RAW entries already emitted.** *Type: implementation slice (Phase 4).* Replaces the narrowing step, which `IMPL-49`/`IMPL-50` measured as breaking AGC outright; the duration rows are the part of the original goal that survives.
8. **Write a root `README.md` mapping the top-level directories.** *Type: planning/documentation action (Phase 1).* Twelve top-level directories currently have no explanation outside the journal.
9. **Record the reverse-engineering toolchain as a re-runnable procedure.** *Type: ontology/ledger action (Phase 1).* Include the negative findings (apktool stubs, radare2 hang, dead Maven coordinates).
10. **Decide the fate of the ineffective `tiles hide` option.** *Type: planning decision (Phase 2).* Needs a human call: fix, remove, or document as a known limitation.
11. **Write the ClaudeQB Phase 10 sub-plans, then start with `Faz10.1`.** *Type: planning action, then validation action (Phase 10).* **Updated 2026-11-15 (planning run 21, `DEC-32`):** appended last only to keep the numbering; it is the next action. Step 2 writes `Faz10.1` to `Faz10.5` in `Planner-docs/Faz-10-Plans/`. Then `Faz10.1` measures the HyperOS 4 camera stack read-only before any change, and every device action after it is the user's, inside a smoke bracket (`scripts/smoke.sh` before and after).

## 9. Step 2 Preparation Notes

**Decompose first.** **Updated 2026-11-15 (planning run 21, user decision 2026-11-15):** ClaudeQB Phase 10 only. This Step 2 is limited: it writes exactly five sub-plans, `Faz10.1` to `Faz10.5`, in `Planner-docs/Faz-10-Plans/`, and adds each to `Planner-docs/Sub-Planing-Index.md`. It writes no other file, does not change this plan or the phase order, and fixes the file-name suffixes itself.
Order and dependencies: `Faz10.1` (read-only measurement and record of the HyperOS 4 camera stack) comes first; `Faz10.2` (sensor layer), `Faz10.3` (AGC trap audit and backed-up cleanup) and `Faz10.4` (tile and WebUI chain with SukiSU-Ultra) each depend on `Faz10.1`; `Faz10.5` (v2.3 release) depends on `Faz10.2` to `Faz10.4`. Section 6's Phase 10 section names the themes.
Earlier state, kept as history: this paragraph named Phases 1, 2 and 3 (A, B, C) to decompose first, with C sliced for verification and stickiness after `DEC-14`. All three have sub-plans in `Faz-1-Plans` to `Faz-3-Plans`, so that instruction is discharged.

**Do not expand yet.** **Updated 2026-11-15 (planning run 21, `AUDIT-FIX-42`):** Phases 1 to 9. Their sub-plans stand as written; Step 2 does not repeat a verified slice or duplicate an existing sub-plan. Phases 7 and 8 are retired by planning run 21 under `DEC-28`, and planning run 21 also retires Phase 6's ROM goal because the ROM build is gone; those sub-plans stay as dated history and are not revived or re-decomposed. `Faz9.1` to `Faz9.3` (verified) do not depend on the ROM build.
Planning run 21 sets `Faz6.1`, `Faz7.2`, `Faz7.3`, `Faz8.1` and `Faz8.3` to `superseded` in the ledger (rationale `DEC-28`); `Faz6.2` stays `verified` with a dated note; the other Phase 7 and 8 sub-plans keep their state as history. Step 2 changes none of these states.
Discharged: this paragraph read "Phases 7, 8, and 9. G is blocked on host-environment work the user must perform. H depends on G. I should be decomposed only after C and D settle, since the release contents are still moving." Phase 9's sub-plans are verified, and the ROM build that G and H served is abandoned (`DEC-28`, which moots `DEC-24` and `DEC-26`), so the `DEC-24`/`DEC-26` rewording that `AUDIT-FIX-42` asked for is replaced by this retirement.

**Evidence Step 2 should collect.** **Updated 2026-11-15 (planning run 21, `DEC-28`, `DEC-32`):** repository evidence only; device measurement is `Faz10.1`'s work, not Step 2's. The HyperOS 4 starting state is in `snapshots/20261113-1819__IMPL96__hyperos4-readonly-probe.txt` and `snapshots/20261113-1821__IMPL96__hyperos4-smoke-baseline.txt` (2026-11-13), plus the dated facts in sections 1, 3, 4 and 7 and the Phase 10 entry evidence in section 6, the only record of the 2026-11-15 checks.
From the module: `setmode.sh`'s restart sequence and its AOSPA service names; the sensor and HAL guards in `post-fs-data.sh`, `halpatch.sh` and `customize.sh`; the tile app's long-press target (`WebUiActivity.java`, `com.rifsxd.ksunext`, not installed on HyperOS 4) and the WebUI's root-manager calls. For AGC: the AOSPA-only, backup-less trap cleanup in `docs/phase3-preconditions.md:71-119`, which does not carry over, and `docs/agc-12mp-configuration.md`.
For v2.3: every version location (`module.prop`, `CHANGELOG.md`, `docs/release-manifest.md`, the tile app's `versionName`), `Kullanim.txt` (`DEC-29`), and `scripts/smoke.sh`'s fields. Earlier state, kept as history: this paragraph asked for AOSPA HAL-state tables, the two patch-table layouts, `setmode.sh`'s mode table, the `verify_ln.py` interface and the trap-key list; they describe AOSPA Android 15 and are not HyperOS 4 evidence.

**Decisions needing human confirmation before implementation.** **Updated 2026-11-15 (planning run 21, `DEC-32`):** the user installs v2.2 on HyperOS 4 for `Faz10.2` and approves each device change; the user approves the backed-up AGC trap cleanup in `Faz10.3` before it runs; the user decides on a system app with the same interface after `Faz10.4` evaluates it; and the user decides the place of `ishtar-aon-fix` on HyperOS 4 in `Faz10.5`.
Reopening 50 MP HAL work on HyperOS 4 needs a new user decision: the HAL layer stays off (recorded as `DEC-33` by planning run 21). Earlier state, kept as history: the four questions this paragraph listed are answered — the AON module stays separate (`DEC-04`), `tiles hide` is kept and fixed (`DEC-02`), Phase 5 ran (`Faz5.1` to `Faz5.3` verified), and `origin` is the private repository `ahmetxa/ishtar_cam_modes` (`DEC-27`).

**History that must be preserved.** The Faz 1–12 findings in `50MP-Entegrasyon-Plani.md`, especially: the client-before-HAL restart ordering invariant; the `getOutputSizes()` high-resolution exclusion mechanism; the `Forty8Strip` identity-stub dead end; the `pref_raw_key` / `pref_fix_resolution_key` Gcam trap; and the Faz 4 ↔ Faz 12 connection showing both failures are the same invariant violated from opposite directions.
**Updated 2026-11-15 (planning run 21, `DEC-28`):** this paragraph also said no ledger, ontology or comprehension file existed; all three exist now and must be preserved: `Planing-Ledger.md` (decisions, implementation records, sub-plan states), `Project-Comprehension.md` (evidence, confidence and CQ/TRACE/ARC entries) and `Project-Ontology.md`.
Their device evidence from before the 2026-11-13 probe is AOSPA Android 15 evidence: Phase 10 sub-plans cite it as history, never as HyperOS 4 evidence. The ledger's `IMPL-96` rows (2026-11-13) hold the first HyperOS 4 read-only measurements. `DEC-28`, `DEC-32` and this plan win over older entries.
`Autopsy.md` is not rerun in planning run 21 (user decision, 2026-11-15; see section 10) and predates `DEC-28`.

**Ontology terms Step 2 must keep consistent.** *Sensor layer* vs *HAL layer* vs *application layer*; *mode* as the single-file runtime state; *patch table* as an offset+md5 triple list; *stock* as both a mode name and a restore target; *fullres* as the HAL state, distinct from *50mp* as the mode name.
**Updated 2026-11-15 (planning run 21, `DEC-32`):** also *ClaudeQB Phase 10* versus the journal's *Faz 10*, a separate numbering; *AOSPA Android 15 evidence* versus *HyperOS 4 evidence*, and rear-camera versus front-camera evidence, never mixed; *root manager* (SukiSU-Ultra on HyperOS 4) versus the KernelSU module format; *derived key* for `pref_camera_picturesize_back_key`, read back and never written; *smoke bracket* as the `scripts/smoke.sh` snapshot pair taken before and after a device change.

**Subagents.** Not recommended by default for this project. The work is deep rather than broad, the evidence is concentrated in a few large files the parent already holds, and device state is stateful and easy to corrupt with parallel access.
**Updated 2026-11-15 (planning run 21, `DEC-28`):** the one exception named here, Phase 8's comparison of the Android 16 vendor blobs against the module's md5 guards, is retired with Phase 8; the HyperOS 4 blobs were compared on 2026-11-13 (see `R8`). Step 2 may use one bounded read-only explorer for the repository evidence above; the parent writes every file.

**Token/context risk and validation checkpoints.** **Updated 2026-11-15 (planning run 21, `DEC-28`, `DEC-32`):** Phases 1, 2, 3, 6, 9: low. Phases 4, 5, 10: medium. Phases 7 and 8 are retired by planning run 21; their bands (7 medium, 8 high) stay in section 6's table as history and plan no work. These bands agree with section 6's table. Phase 10 is medium on breadth (sensor layer, AGC, tile and WebUI, release), not on analysis depth: no HAL disassembly is planned (recorded as `DEC-33` by planning run 21).
Phase 10 checkpoints: `Faz10.1` is read-only and its record is written before any other Phase 10 sub-plan starts; every device change in `Faz10.2` to `Faz10.4` sits inside a smoke bracket (`scripts/smoke.sh` before and after); AGC trap cleanup runs only after a backup; `Faz10.5` checks the release with `docs/release-checklist.md`. Step 2 ends with the bundled validator in `--mode step2 --strict`, which needs `Faz-10-Plans` for row 10 and every new sub-plan indexed.
Kept as history: **Corrected 2026-09-04 (`AUDIT-FIX-20`, deferred since the `DEC-14` re-plan and folded into this amendment rather than left for a third edit of this file).** Phases 1, 2, 3, 6, 9: low. Phases 4, 5, 7: medium. Phase 8: high — the bands now agree with section 6's table, which this paragraph had contradicted, and Phase 8 is no longer omitted from the list.
The retired text banded Phase 3 `high` and instructed a checkpoint "after every located address by writing it into the ontology before continuing"; that described the write-site search in a 27 MB stripped binary which `DEC-14` retired. The replacement Phase 3 is configuration work, and its checkpoint is the bracketed `scripts/smoke.sh` snapshot plus the eight-item per-measurement checklist in `docs/phase3-preconditions.md`, run before any result is recorded. `Faz3.10` alone rises to medium, on run count rather than analysis depth.

## 10. Repository Review Notes

**Commands run.** `ls -la` at root; `find` over `ishtar-cam-modes`, `ishtar-aon-fix`, `agc-50mp-yama`, `Module_Highres_13U_Switcher_A14`, `.claude`; `ls` over `device_ishtar`, `refs`, `13U-989-DCG16+LN2+LN4`, and the three kernel checkouts at depth 1; `git rev-parse --is-inside-work-tree` (result: not a repository); `grep -n '^#'` over the journal; `wc -l` over module scripts and tools; `grep -c SYMLINK` over both `proprietary-files.txt` files (result: 0 and 0); `sed -n` over the journal's decisions section; a filename-only listing of `tile-app/`; a key-only scan of `.claude/settings.local.json`.

**Files inspected.** `50MP-Entegrasyon-Plani.md` (headings and decisions section), `ishtar-cam-modes/module.prop`, `ishtar-cam-modes/mode`, `ishtar-cam-modes/setmode.sh` (first 60 lines), `ishtar-aon-fix/module.prop`, `device_ishtar/README.md`, `device_ishtar/proprietary-files.txt` (count only), `refs/a16_ishtar/proprietary-files.txt` (count only), `agc-50mp-yama/` listing.

**Existing docs found.** `50MP-Entegrasyon-Plani.md` (the engineering journal, 12 phase sections plus decisions), `agc-50mp-yama/README.md`, `ishtar-cam-modes/Kullanim.txt`, `device_ishtar/README.md`, `13U-989-DCG16+LN2+LN4/1. Howto.txt` and its QuickTile notes.

**Prior ClaudeQB artifacts.** `Planner-docs/` did not exist before this run. No `Planing-Ledger.md`, `Project-Ontology.md`, or `Project-Comprehension.md` was present, so none could be used as supporting evidence. Step 1.5 creates the ontology and comprehension artifacts from this run's evidence.

**Assumptions made.** That the four intake fields inferred from repository evidence and standing project history are correct — they are stated explicitly for user confirmation rather than treated as settled. That the journal's measured values (md5s, offsets, `dumpsys` output) are accurate, since they were recorded from device output. That `mode` reading `stock` reflects the device's current state as well as the workspace's.

**Not verified in this run.** The contents of the three kernel checkouts beyond depth 1. The internals of `action.sh`, `post-fs-data.sh`, `halpatch.sh`, `customize.sh`, `service.sh`, `webroot/index.html`, and the four Python tools beyond line counts. The tile app's Java sources. The `.agc` configuration files. Whether the device's current live state matches the workspace's `mode` file. Whether any released zip already contains `debug.keystore` — this should be checked in Phase 1.

**Secrets.** No secret values were read or recorded. `ishtar-cam-modes/tile-app/debug.keystore` is reported by path only, as a signing-credential location finding.

**Planning run 21 (2026-11-15).** Planning run 21 skips Step 1.5 (Autopsy) by user decision (2026-11-15), so `Planner-docs/Autopsy.md` stays stale; it predates `DEC-28`. The Hetzner rows of `Project-Comprehension.md` (`CQ-13`, `EV-20`), `Project-Ontology.md` (invariant 11) and `docs/reverse-engineering-toolchain.md` are corrected by planning run 21 outside Step 1 and Step 2, as a user-approved deviation (`AUDIT-FIX-57`); the 12th audit verifies them. The other stale lines of those files are left to the 12th audit.
