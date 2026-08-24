# Project Autopsy

> Step 1.5 autopsy — ClaudeQB. Body language: English (default contract).
> Source of truth: `Planner-docs/Main-Planing.md` plus direct read-only repository inspection.

## 1. Executive Summary

This is unambiguously an **existing, substantially built project**, not a greenfield one. The evidence is direct: a 60 KB, ~1,300-line engineering journal covering twelve completed or in-progress work phases; a KernelSU module at version v2.1 / versionCode 12 with 1,988 lines of shell, Python, and HTML; four released `.zip` snapshots; ten pre-generated sensor firmware blobs; a working binary patch table with verified md5 checksums; and a second, independently packaged module for a different defect.

The strongest repository evidence is `50MP-Entegrasyon-Plani.md`. It is not a plan in the usual sense — it is a lab notebook. It records measured values rather than intentions, names hypotheses that turned out to be wrong, and traces failures to root cause. Sections such as "AGC neden hâlâ 15,2 MP — kesin açıklama" and "Mount yığını hatası ve kalıcı düzeltme" contain the kind of evidence most projects never write down. Any planning that treats this file as disposable would destroy the project's principal asset.

Maturity is **stratified, not uniform**, and reporting a single number would be misleading. The sensor-mode layer is production-grade for its audience: mutually-exclusive tiles, reboot persistence, a debugged camera-restart ordering, bilingual UI, and daily use. The full-resolution layer works for third-party applications and is proven on device at 50.3 MP. The AGC integration is mid-flight, blocked at a precisely identified invariant. The Android 16 track has not begun.

The most important **technical** gap is the libgcam static-metadata invariant described in Main-Planing Phase 3. It is well characterized, which is the good news; the write site for `android.sensor.info.pixelArraySize` has not been located, which is the bad news. This is a bounded unknown with a known measurement method, not an open-ended risk.

The most important **structural** gap is entirely different and, in my assessment, more urgent: **the workspace has no version control.** `git rev-parse --is-inside-work-tree` fails at the root. Roughly 465 MB of content sits here with no history. The patch tables in particular — `hal-fullres.patch` with sixteen entries, `hal-raw50-deneme.patch` with four — represent weeks of disassembly compressed into a few hundred bytes each. They are trivially destroyable and expensive to regenerate.

A third gap sits between those two: **there is no automated verification of any kind.** No tests, no CI, no smoke script. The project's own history demonstrates the cost. The sensor-7 Gcam failure was initially attributed to the HAL patch, then to the APK patch, and was finally traced to leftover shared-preference keys — a three-step misattribution that a before/after state snapshot would have shortened considerably.

A notable **positive** finding deserves equal weight. The patch-table format — offset, stock byte sequence, patched byte sequence, guarded by md5 of both the input and the result — is a genuinely good design. It is self-verifying, human-readable, diffable, and it keeps a 27 MB proprietary blob out of the distributed artifact. This convention should be extended rather than replaced.

The security posture is domain-appropriate with one concrete finding: `ishtar-cam-modes/tile-app/debug.keystore` is a signing credential stored in the working tree next to the artifacts it signs. It is a debug key, and its presence is understandable during development, but it must be excluded from both version control and every distributed zip.

The most important planning implication for Step 2 is one of **sequencing, not scope**. The technical plan is sound and the phases are well chosen. What Step 2 must enforce is that Phase 1 (safety net) and the smoke script are decomposed and executed *before* the high-uncertainty Phase 3 reverse-engineering work — because Phase 3 is precisely the phase where an unrecoverable mistake is most likely and where misattribution is most expensive.

## 2. Reviewed Sources

**Commands run (all read-only):**

- `ls -la` at repository root
- `find ishtar-cam-modes -maxdepth 2 -type f`, `find ishtar-aon-fix -type f`, `find Module_Highres_13U_Switcher_A14 -type f`, `find .claude -type f`
- `ls agc-50mp-yama`, `ls device_ishtar`, `ls refs`, `ls "13U-989-DCG16+LN2+LN4"`
- `ls` at depth 1 over `android_kernel_xiaomi_sm8550`, `android_kernel_qcom_sm8550`, `common_sm8550`
- `git rev-parse --is-inside-work-tree` → **not a git repository**
- `find Planner-docs -maxdepth 4 -type f` → did not exist prior to this run
- `grep -n '^#' 50MP-Entegrasyon-Plani.md` (structure only)
- `sed -n '1282,1400p' 50MP-Entegrasyon-Plani.md` (decisions section)
- `head -60 ishtar-cam-modes/setmode.sh`
- `wc -l` over `ishtar-cam-modes/*.sh`, `ishtar-cam-modes/tools/*.py`, `ishtar-cam-modes/webroot/index.html`
- `cat ishtar-cam-modes/module.prop`, `cat ishtar-cam-modes/mode`, `cat ishtar-aon-fix/module.prop`
- `head -30 device_ishtar/README.md`
- `grep -c 'SYMLINK' device_ishtar/proprietary-files.txt refs/a16_ishtar/proprietary-files.txt` → **0 and 0**
- `ls -la ishtar-cam-modes/tile-app/` (filenames only — no file contents read)
- key-name-only scan of `.claude/settings.local.json` → only `permissions` / `allow`

**Main plan:** `Planner-docs/Main-Planing.md` (created earlier in this same run).

**Important docs inspected or catalogued:** `50MP-Entegrasyon-Plani.md`, `agc-50mp-yama/README.md`, `ishtar-cam-modes/Kullanim.txt`, `device_ishtar/README.md`, `13U-989-DCG16+LN2+LN4/1. Howto.txt` and its three QuickTile notes.

**Manifests / configs:** `ishtar-cam-modes/module.prop`, `ishtar-aon-fix/module.prop`, `Module_Highres_13U_Switcher_A14/module.prop`, `device_ishtar/{Android.bp,Android.mk,BoardConfig.mk,device.mk,proprietary-files.txt}`, `.claude/settings.local.json`.

**Tests / CI evidence:** none found. No test directory, no CI configuration, no `.github/`, no `Makefile`, no `package.json`, no `pyproject.toml`.

**Prior Planner-docs:** none existed. No `Planing-Ledger.md`, `Project-Ontology.md`, or `Project-Comprehension.md` was available as supporting history.

## 3. Project Areas and Ownership Boundaries

**Area 1 — `ishtar-cam-modes/` (primary deliverable).**
*Responsibility:* runtime mode switching across the sensor and HAL layers; user-facing UI (tiles, WebUI, action button); installation and boot-time application.
*Maturity:* high. v2.1, versionCode 12, four released snapshots, daily use.
*Boundary issue:* this directory owns two architecturally distinct concerns — sensor-blob replacement and HAL byte-patching — and the split is expressed only by convention (`setmode.sh` sources `halpatch.sh`). The `setmode.sh` header comments state the separation clearly, which mitigates the risk, but it is documentation rather than structure.

**Area 2 — `ishtar-aon-fix/` (secondary module).**
*Responsibility:* creates the missing `/vendor/lib64/camera/aon_front.pb` path so the AON → CSS → NCS chain initializes; restores aperture, OIS, laser AF, and face-scene providers.
*Maturity:* medium-high. Three files, packaged as v1.1, explicitly documented as independent of KernelSU module mounting.
*Boundary issue:* it is a workaround for a device-tree defect (the missing `;SYMLINK=` entry), so its correct long-term home is `device_ishtar/`, not a runtime module. Ownership is currently in the wrong layer by necessity, not by design.

**Area 3 — `agc-50mp-yama/` (application-layer patches).**
*Responsibility:* smali-level modification of the AGC GCam port, plus the experimental HAL RAW patch table.
*Maturity:* low-medium. Four files, work in progress, contains an explicitly experimental artifact.
*Boundary issue:* `hal-raw50-deneme.patch` is a HAL-layer artifact living in an application-layer directory. Understandable while experimental; it must move to `ishtar-cam-modes/blobs/` when it stabilizes, or its location will mislead a future reader.

**Area 4 — `device_ishtar/`, `common_sm8550/`, `refs/*` (ROM build inputs).**
*Responsibility:* AOSPA/LineageOS device configuration for `ishtar` and, via `refs/a16_*`, the Android 16 target.
*Maturity:* inherited from upstream; unmodified by this project so far.
*Boundary issue:* five reference trees under `refs/` with no README explaining which is authoritative for what. `a16_ishtar` and `a16_sm8550` are the Android 16 inputs; `los_*` and `neo_*` are comparison sources — but this is inferable only from naming.

**Area 5 — kernel checkouts (read-only reference).**
*Responsibility:* source reading for future GKI LTS merge work.
*Maturity:* N/A — checkouts, not deliverables.
*Boundary issue:* three full kernel trees inside the workspace with known NTFS case-collisions, contributing most of the repository's byte size while being unbuildable on this host.

**Area 6 — upstream reference modules (`13U-989-DCG16+LN2+LN4/`, `Module_Highres_13U_Switcher_A14/`).**
*Responsibility:* the third-party modules this work reverse-engineered.
*Maturity:* N/A — external artifacts.
*Boundary issue:* none, and this is handled well. `Kararlar #2` explicitly states nothing is carried over as-is. Worth noting that `Module_Highres_13U_Switcher_A14/root/odm/lib64/hw/camera.qcom.so` and its `mod/{enable,disable}/` copies are full 27 MB HAL blobs — the very thing the project's own patch-table design avoids shipping.

**Area 7 — loose root-level binaries.**
*Responsibility:* application artifacts under test and sensor firmware.
*Maturity:* N/A.
*Boundary issue:* three ~150 MB APKs, an Open Camera build, the IMX989 `.bin`, two `.agc` configs, and four release zips sit unsorted at the root with no manifest describing which is current. `AGC8.4.300_V9.6_50MP_patched.apk` is the currently installed build; that fact lives only in the journal and in session memory.

## 4. Feature Inventory

**Implemented or strongly evidenced:**

- Ten sensor modes — `stock`, `dcgA`, `dcgB`, `ln2`, `ln4`, `ln2s`, `ln4s`, `ln2f`, `ln4f`, plus `50mp` — selectable via `setmode.sh` (evidence: `setmode.sh` usage header; ten `blobs/*.bin`).
- `dcgB` validated on device as the recommended mode: ~25% less noise and roughly double the detail versus stock, with no shutter-speed change and no `overrideForceSensorMode` property required (evidence: `module.prop` description; journal Faz 4).
- Four mutually-exclusive QuickSettings tiles with cross-synchronization, long-press to WebUI (evidence: `tile-app/`, `module.prop` v1.4–v1.5 notes).
- Safe camera-stack restart with documented ordering invariant (evidence: `setmode.sh` `restart_camera()`, with the failure mode explained in-line).
- Bilingual EN/TR UI, default English, independent of system locale, with an EN/TR toggle in the WebUI (evidence: `module.prop` v1.8; `lang`; `webroot/index.html`).
- Live per-second countdown notification during mode switching (evidence: `module.prop` v1.9).
- 50 MP full-resolution for third-party apps via a 16-point HAL offset patch; measured at 50.3 MP in Open Camera; video 1080p60/4K60 unaffected (evidence: `blobs/hal-fullres.patch`; `module.prop` v2.0; journal Faz 8).
- AON front-config repair as a standalone module (evidence: `ishtar-aon-fix/`, v1.1).
- Launcher icon rendering fix and framework-read (not cache-read) status reporting (evidence: `module.prop` v2.1).
- Sensor-blob generation and verification tooling (evidence: `tools/dcg_multimode.py` 192 lines, `ln_multimode.py` 274, `port_sensor_mod.py` 140, `verify_ln.py` 126).

**Partial / skeleton:**

- AGC 50 MP capture. The APK patch makes the port select 8192x6144 and open a matching ImageReader; capture does not complete. The HAL RAW patch makes AGC auto-select `RAW10 8192x6144` with no preferences set; libgcam rejects the metadata. Both measured, both currently reverted on the device.
- The experimental HAL RAW patch is functionally correct but over-broad: it adds RAW formats at every resolution, growing the stream-configuration array from 508 to 868 int32 entries. No `availableMinFrameDurations` or `availableStallDurations` rows were added.
- The `tiles hide` option is recorded as ineffective and its disposition is undecided.

**Planned but not evidenced in the repository:**

- Mode-0 12-bit migration to allow 50 MP + LN composition (user-approved in `Kararlar #4`; no blob or tooling change present).
- Android 16 / AOSPA build (`refs/a16_*` present as input; no build artifacts, no WSL2).
- `beryl` port (no beryl-specific files present).
- Kernel GKI LTS merge (checkouts present; no merge work).
- AON long-run defect hunt (mentioned in project history; no artifacts).

**Missing or unclear:**

- Any test, smoke, or verification harness.
- A root `README.md`.
- A release/build script — the four release zips have no visible producer.
- A stock-restore runbook independent of `setmode.sh` (relevant precisely when `setmode.sh` is what went wrong).
- A manifest identifying which root-level APK is current.

## 5. Placeholder, Stub, and Skeleton Analysis

This repository is notably **free of the usual placeholder pathology**. There are no `TODO`-stuffed function bodies, no `NotImplementedError` stubs, no mock services standing in for real ones. Code that exists, runs. That is a direct consequence of the domain: shell modules that do nothing produce a phone that does nothing, so the feedback is immediate.

The indicators that do exist are of a different kind:

- **`ishtar-cam-modes/mode` contains `stock`** — this is live runtime state checked into the deliverable directory, not a placeholder. *Assessment:* harmless but structurally impure; a packaged module ships with whatever mode the workspace last held. Step 2 should confirm `customize.sh` normalizes this at install time rather than shipping the developer's state.
- **`ishtar-cam-modes/active/com.qti.sensormodule...bin`** — a runtime working copy checked in alongside the canonical `blobs/`. *Assessment:* harmless, but it duplicates a 1 MB binary and blurs which copy is authoritative.
- **`Module_Highres_13U_Switcher_A14/early-mount/initrc.d/example.rc`** — an actual example file, in a reference tree. *Assessment:* harmless, external.
- **`agc-50mp-yama/hal-raw50-deneme.patch`** — named "deneme" (experiment) and correctly flagged as such in its own header comments. *Assessment:* not delivery-blocking, but it is a HAL artifact in an application directory and will mislead a future reader if it stabilizes without moving.
- **The `tiles hide` option** — a feature that exists in the UI and does not work. *Assessment:* **delivery-blocking in the reputational sense.** A visible control that silently does nothing is worse than an absent one. Step 2 should force a decision: repair, remove, or label.

**How Step 2 should plan remediation.** Fold the `mode`/`active/` hygiene questions into the Phase 1 packaging review; make the `tiles hide` decision an explicit Phase 2 gate rather than a background item; make relocating `hal-raw50-deneme.patch` part of the Phase 4 acceptance criteria.

## 6. Technical Debt and Maintenance Risks

**Duplicated logic and repeated patterns.** The changelog exists twice — in `50MP-Entegrasyon-Plani.md` and in `module.prop`'s `description` field, which has grown to roughly 1,600 characters and now carries the full v1.2→v2.1 history. `module.prop` `description` is displayed in the KernelSU module list; it is not a changelog surface. This duplication guarantees eventual divergence.

**Unclear module boundaries.** The sensor layer and the HAL layer are separated by comment and by convention, not by structure. `setmode.sh` sources `halpatch.sh` and dispatches both. This works and is well documented, but it means the mutual-exclusion rule (`Kararlar #1`) is enforced by control flow in a 280-line shell script rather than by a checked invariant. When `Kararlar #4` removes that exclusion, this is where the change will be riskiest.

**Oversized and underspecified files.** `50MP-Entegrasyon-Plani.md` at ~1,300 lines with no table of contents and non-monotonic phase numbering (Faz 10 pending while Faz 11 and 12 are complete) is difficult to navigate. `setmode.sh` at 280 lines and `action.sh` at 263 are near the upper bound of comfortable shell, though both are heavily commented.

**Missing contracts and schemas.** The patch-table format is excellent but undocumented as a format — its grammar (`<4-byte-index> <stock-escape> <patched-escape>`, with md5 lines as comments) exists only implicitly in the two files that use it and in the parser inside `halpatch.sh`. Step 2 should have this written down once; it is the project's most reusable invention.

**Error handling and lifecycle state.** `setmode.sh` fails closed on missing module directory, non-root execution, and md5 mismatch — good. The `wait_svc` helper bounds service transitions with an 8-second timeout — good. What is not visible from this inspection is what happens when a patch is half-applied because the device lost power mid-write. Step 2 should ask whether patch application is atomic or merely ordered.

**Stale and contradictory planning assumptions.** The journal's own Faz 8 section concludes that AGC cannot exceed 15.2 MP; Faz 11 and 12 supersede that conclusion. The document does not mark the earlier section as superseded. Similarly, `module.prop` v2.0's description still states "AGC 12,6-15,2 MP'de kalir cunku GCam 8.4 motoru 50MP akisini secemiyor" — a claim Faz 12 has since shown to be wrong in its stated cause. Neither is harmful today, but both will mislead.

**Environment fragility.** The reverse-engineering toolchain has been reconstructed at least once after a context loss, and the reconstruction cost real time: apktool's bundled smali `Main` classes are stripped stubs; `com.android.tools.smali` Maven coordinates return 404; the Bitbucket mirror returns 403; google/smali publishes no release binaries; radare2 and rabin2 do not complete on this 27 MB binary. All of this is negative knowledge that must be written down or it will be rediscovered a third time.

## 7. Broken or Missing Integrations

**Internal boundaries.** The tile app ↔ module contract runs through the `mode` file and `action.sh`. It has had two historical defects — tiles not synchronizing (fixed v1.5) and status read from cache rather than framework (fixed v2.1) — both symptoms of the same class: multiple readers of a single-writer state with no notification protocol. The current design polls. That is acceptable at this scale and worth noting as a known shape rather than a defect.

**External APIs and providers.** None. The project makes no network calls, integrates no third-party service, and collects no telemetry. From an integration-risk standpoint this is close to ideal.

**Device-side integrations.** Three, and all are load-bearing:

1. **KernelSU** — the privilege and mounting channel. `ishtar-aon-fix` explicitly documents itself as *not* depending on KernelSU module mounting, which is a deliberate resilience choice worth preserving.
2. **The Android camera framework** — `cameraserver` and `vendor.camera-provider` / `vendor.camera-provider-2-7-ext` are stopped and restarted. The ordering invariant is documented and load-bearing.
3. **Vendor blobs** — `/odm/lib64/hw/camera.qcom.so` and `/odm/lib64/camera/<sensor>.bin`, both bound to exact sizes and md5s (`EXPECT_SIZE=1062250` for the sensor blob; 27,268,688 bytes for the HAL).

**Database / queue / storage.** None. State is one file. This is correct for the domain.

**Auth / security / policy systems.** SELinux is engaged via `sepolicy.rule` in the reference modules; whether `ishtar-cam-modes` ships its own rules was not verified in this pass. The project's history records that `restorecon -R` destroys per-app SELinux categories and that `chcon -R` with the parent context is required instead — a real integration constraint that should be captured in the runbook.

**CI / deployment / infrastructure.** **Absent.** No CI, no build automation, no deployment pipeline. Releases are produced manually by an unrecorded process.

**Missing adapters and mismatched contracts.** The significant one is the `;SYMLINK=` entry absent from both `device_ishtar/proprietary-files.txt` and `refs/a16_ishtar/proprietary-files.txt` — verified at zero occurrences in each. The `ishtar-aon-fix` module exists solely to compensate for this. It is a contract mismatch between the device tree and the vendor blob's expectations, currently patched at runtime instead of at build time.

## 8. Test, CI, and Validation Gaps

**Observed tests.** None. No test framework, no test directory, no CI configuration.

**Closest existing thing.** `ishtar-cam-modes/tools/verify_ln.py` (126 lines) verifies LN blob generation. It is a build-time verifier for one artifact class, not a test suite — but it demonstrates the author already thinks in terms of verification, and it is the natural seed for a real harness.

**Missing coverage by layer:**

- *Unit-level:* the four Python tools generate and patch binary structures with no assertions about their own correctness beyond `verify_ln.py`.
- *Integration-level:* nothing verifies that a generated blob, once mounted, produces the intended sensor mode.
- *End-to-end:* nothing verifies that a mode switch completes and the camera opens. This is the single highest-value missing check, and it is the one the project's own history shows failing repeatedly (black preview, stuck shutter, locked camera).
- *Regression:* nothing captures device state before and after a change. The sensor-7 misattribution episode is a direct consequence.

**Local vs live validation.** The distinction barely exists here, because almost nothing can be validated locally. Blob generation can be checked on the host; everything else requires the device. This makes a device-side smoke script disproportionately valuable — it is effectively the *only* automatable validation surface.

**Suggested validation gates for Step 2 sub-plans.**

- *Gate 1 (host, cheap):* every generated blob matches its expected size and its recorded md5 before packaging.
- *Gate 2 (device, one command):* a smoke script reporting active mode, HAL md5, sensor md5, mount state, camera-3 stream-configuration rows, and installed AGC md5. Every phase from B onward should start and end with this.
- *Gate 3 (device, manual):* camera opens in the selected mode; preview is not black; shutter completes; 1080p60 and 4K60 record. This requires the user and should be an explicit checklist, not an assumption.
- *Gate 4 (release):* the produced zip contains no `debug.keystore` and no 27 MB blob.

## 9. Security, Secret, and Governance Findings

**Secret handling.** One finding, reported by path only, with no file content read: `ishtar-cam-modes/tile-app/debug.keystore` is an application-signing keystore located in the working tree alongside the artifacts it signs. It is a debug key by name and role, and its presence during development is normal practice. Two controls are nonetheless required: it must be excluded from version control when Phase 1 initializes a repository, and every released zip must be verified not to contain it. The project's history also notes that the same signer key allows subsequent `install -r` without uninstalling — which is convenient and is precisely why the key's confidentiality matters.

No other secret-like material was found. `.claude/settings.local.json` contains only `permissions` / `allow` keys. There are no API keys, tokens, or credentials anywhere in the inspected surface. The project makes no network requests.

**Policy and approval boundaries.** These are well established in practice: read-only `adb` inspection is automated, while anything requiring physical interaction with the device — flashing, dismissing dialogs, capturing photographs — is the user's action. This split has held across the project's history and should be written into the runbook rather than remaining an oral convention.

**Least privilege.** Not applicable in the usual sense: the modules require root and write into `/odm` because that is the only way to accomplish the task. The meaningful control is not privilege reduction but **write discipline** — size check, md5 check, fail closed. That discipline is present in `setmode.sh` and should be audited across `post-fs-data.sh`, `halpatch.sh`, and `customize.sh`, which were not read in this pass.

**Audit and artifact integrity.** Strong where it exists. Patch tables record the md5 of both input and output, making application verifiable and reversible. Sensor blobs are guarded by an exact expected size. The gap is that these guarantees are per-file and there is no manifest binding a *release* to the set of md5s it expects.

**Risky command execution and mutation surfaces.** The modules execute at `post-fs-data` as root and mutate system partitions. `restart_camera()` sends `stop`/`start` to system services. `action.sh` force-stops camera applications. All of these are appropriate and necessary; none of them takes untrusted input. The WebUI (`webroot/index.html`, 344 lines) is the one surface that accepts user input and was not read in this pass — Step 2 should confirm it cannot pass unsanitized values into a shell invocation.

**Compliance and governance unknowns.** The project redistributes a modified Google Camera port and patches proprietary Qualcomm and Xiaomi blobs. The distribution model (patch tables rather than shipped binaries) is a thoughtful mitigation and reduces exposure considerably. Whether the AGC APK may be redistributed at all is a question the user has already engaged with — the config author mandates V9.6 and the port developer is unreachable. This is a governance unknown, not a defect, and it should be recorded rather than resolved by planning.

## 10. Operational Readiness and Observability

**Deployment and runtime evidence.** The install path is a KernelSU flashable zip; `customize.sh` (78 lines) has been exercised on device. Four released zips exist. `post-fs-data.sh` (131 lines) reapplies state at boot, and `service.sh` (44 lines) handles late-boot work. Mode persistence across reboot is claimed and has been validated.

**The live gap.** `ishtar-cam-modes-v2.1.zip` was built and has never been flashed. The artifact a user would install has therefore never run. This is the clearest local-vs-live readiness gap in the project and it is cheap to close.

**Observability.** Device-side observability is genuinely good for a shell module: transition notifications, a live countdown, a WebUI status page, and a `setmode.sh` status mode when invoked without arguments. What is missing is **historical** observability — nothing persists what happened across mode switches, so a failure two switches ago leaves no trace. The project's history shows this cost being paid: `logcat`'s 30 Hz `CAM_A: Can not update pitch roll indicator` spam rolled the buffer and hid the evidence until the buffer was enlarged to 64 MB and tag filters applied.

**Backup, restore, and rollback.** Rollback exists conceptually — set mode to `stock`, disable the module — and the md5 guards make patch reversal deterministic. What does not exist is a **documented recovery runbook for the case where the module itself is what broke**. On this device a corrupted camera HAL means no camera until reflash, so the recovery path deserves to be written down before it is needed rather than after.

**Cost, latency, and quality signals.** Not applicable in the cloud sense. The domain equivalents — mode-switch duration, camera-open latency, image noise and detail — are measured manually and recorded in the journal. `dcgB`'s ~25% noise reduction is exactly this kind of signal, and it is well captured.

**Live readiness blockers.** For the sensor-mode layer: only the unflashed v2.1. For the 50 MP + AGC layer: the libgcam invariant. For Android 16: WSL2 is not installed.

## 11. Alignment Analysis with the Main Plan

**Supported assumptions.** The main plan's three-layer architecture (sensor / HAL / application) is directly confirmed by `setmode.sh`'s own header comments, which describe exactly that split and explain the mutual-exclusion rule. The claim that the sensor-mode layer is mature is supported by version history, four releases, and the specificity of the fixes in `module.prop`. The claim that no version control exists is confirmed. The claim that the `;SYMLINK=` fix is missing is confirmed at zero occurrences in both trees. The claim that no tests exist is confirmed. The maturity stratification (M5–M6 / M4 / M0) is consistent with the evidence.

**Weak or unverified assumptions.** The main plan asserts the workspace holds "roughly 465 MB" — this is derived from the root `ls -la` byte counts and excludes the three kernel checkouts and five reference trees, which were not measured (`du` timed out on this tree). The true figure is substantially larger, and Phase 1's `.gitignore` scope should be sized from a real measurement rather than this estimate. The plan also assumes `mode` reading `stock` reflects the device's live state; that was not verified in this pass and should be confirmed by the smoke script rather than assumed.

**Assumptions that need sharpening.** Phase 3 is described as high-risk and high-token, which is right, but the plan does not state a stop condition. Reverse-engineering phases without a stop condition are how token budgets disappear. Step 2 should give Phase 3 an explicit bound: a number of located-address attempts, or a fallback decision point where the app-level patch is accepted as the answer.

**Roadmap phases needing stronger evidence before decomposition.** Phase 5 (mode-0 12-bit) rests entirely on `Kararlar #4` and on the assumption that the 10-bit/12-bit mismatch is the sole cause of the exclusion; no measurement in the repository confirms that this is the *only* obstacle. Phase 8 (beryl) has no beryl-specific evidence in the tree at all and should not be decomposed until Phase 7 produces a working build environment.

**Risks Step 2 must not ignore.** First, the ordering risk: Phase 3 is the phase most likely to produce an unrecoverable mistake, and Phase 1 is what makes mistakes recoverable — so A must precede C without exception. Second, the misattribution risk: without before/after state capture, Phase 3's failures will be attributed to the wrong layer, exactly as happened with sensor 7. Third, the `pref_raw_key` / `pref_fix_resolution_key` trap is a known landmine that has already cost one debugging cycle and must appear as a precondition check in every Phase 3 sub-plan, not as a footnote.

## 12. Autopsy Feedback for Step 2

**Phase 1 — Workspace safety net**

- Size the `.gitignore` from an actual measurement of the kernel checkouts and reference trees, not from the root `ls` estimate. *Supported by:* section 11 (the `du` measurement did not complete). *Sub-plan type:* implementation.
- Explicitly exclude `ishtar-cam-modes/tile-app/debug.keystore`, and verify no already-released zip contains it. *Supported by:* section 9. *Sub-plan type:* security hardening.
- Document the patch-table format as a first-class contract. *Supported by:* section 6 (missing contracts). *Sub-plan type:* documentation.
- Record the toolchain including its negative findings — apktool stubs, dead Maven coordinates, radare2 hang. *Supported by:* section 6 (environment fragility). *Sub-plan type:* documentation.
- Resolve the `mode` and `active/` hygiene questions as part of packaging. *Supported by:* section 5. *Sub-plan type:* implementation.

**Phase 2 — Ship and re-baseline v2.1**

- Make the smoke script a prerequisite of this phase, not a later deliverable. *Supported by:* section 8 (Gate 2). *Sub-plan type:* validation.
- Force an explicit decision on `tiles hide` — repair, remove, or label. *Supported by:* section 5. *Sub-plan type:* planning decision.
- Include the manual device checklist (preview not black, shutter completes, 1080p60 and 4K60 record) as a named gate with the user as the actor. *Supported by:* section 8 (Gate 3). *Sub-plan type:* validation.

**Phase 3 — 50 MP end-to-end in AGC**

- Add a precondition check for leftover `pref_raw_key_N` / `pref_fix_resolution_key_N` to every sub-plan in this phase. *Supported by:* section 11. *Sub-plan type:* validation.
- Define a stop condition and a fallback decision point. *Supported by:* section 11. *Sub-plan type:* planning.
- Require a before/after state snapshot around every single-word patch. *Supported by:* section 8 (missing regression capture). *Sub-plan type:* validation.
- Require each located address to be written into `Project-Ontology.md` immediately. *Supported by:* section 6 (environment fragility) and Main-Planing R10. *Sub-plan type:* ontology.

**Phase 4 — Minimal correct HAL patch**

- Make relocating `hal-raw50-deneme.patch` out of `agc-50mp-yama/` an acceptance criterion. *Supported by:* sections 3 and 5. *Sub-plan type:* implementation.
- Require the array-size delta (currently 508 → 868 int32) as a measured acceptance number, not a qualitative claim. *Supported by:* section 4. *Sub-plan type:* validation.

**Phase 6 — AON fix upstreaming**

- This is a one-line change per tree and is independent of every other phase; schedule it early rather than by phase order. *Supported by:* section 7 (verified zero SYMLINK entries). *Sub-plan type:* implementation.

**Cross-cutting**

- Mark superseded conclusions in `50MP-Entegrasyon-Plani.md` (Faz 8's AGC ceiling) and correct the stale causal claim in `module.prop` v2.0's description. *Supported by:* section 6. *Sub-plan type:* documentation.
- Move the changelog out of `module.prop` `description`. *Supported by:* section 6. *Sub-plan type:* documentation.
- Read `webroot/index.html` for shell-injection exposure before the next release. *Supported by:* section 9. *Sub-plan type:* security review.
- Audit `post-fs-data.sh`, `halpatch.sh`, and `customize.sh` for the same fail-closed discipline `setmode.sh` demonstrates. *Supported by:* section 9. *Sub-plan type:* security review.

## 13. Priority Fix and Planning Signals

- **AUTOPSY-P0-01 — Workspace is not under version control**
  - Impact: ~465 MB or more of binaries, ten sensor blobs, and two hand-derived patch tables have no history and no rollback. The patch tables represent weeks of disassembly and are trivially destroyable.
  - Evidence: `git rev-parse --is-inside-work-tree` fails at repository root.
  - Step 2 impact: Phase 1 must be decomposed first and must complete before any Phase 3 sub-plan executes. No sub-plan that modifies a binary or a patch table may be scheduled ahead of it.

- **AUTOPSY-P0-02 — No before/after state capture around device changes**
  - Impact: failures are attributed to the wrong layer. The sensor-7 Gcam failure was blamed on the HAL patch, then the APK patch, before being traced to leftover shared preferences — a three-step misattribution.
  - Evidence: no test, CI, or smoke artifact anywhere in the tree; journal Faz 12 records the misattribution sequence.
  - Step 2 impact: the smoke script becomes a Phase 2 prerequisite and a mandatory bracket around every Phase 3 measurement.

- **AUTOPSY-P1-01 — Signing keystore in the working tree**
  - Impact: a signing credential sits beside the artifacts it signs; if swept into a repository or a distributed zip, third parties can sign updates the device accepts as the same app.
  - Evidence: `ishtar-cam-modes/tile-app/debug.keystore` (path only; contents not read).
  - Step 2 impact: explicit `.gitignore` entry in Phase 1 plus a packaging assertion in Phase 9; verify already-released zips.

- **AUTOPSY-P1-02 — Released v2.1 has never been flashed**
  - Impact: the artifact users would install has never run; the validated state and the shipped state are different things.
  - Evidence: `ishtar-cam-modes-v2.1.zip` dated 2026-08-22; project history records it as built and unflashed.
  - Step 2 impact: Phase 2's first slice, gated on the user's physical access to the device.

- **AUTOPSY-P1-03 — Phase 3 has no stop condition**
  - Impact: locating a write site in a 27 MB stripped binary is open-ended; without a bound, the token budget and the session both run out before a decision is reached.
  - Evidence: Main-Planing Phase 3 marked high token/context risk with no bound stated.
  - Step 2 impact: every Phase 3 sub-plan needs an explicit attempt budget and a named fallback (accept the app-level patch, or move the active array instead).

- **AUTOPSY-P1-04 — `;SYMLINK=` entry missing from both device trees**
  - Impact: `ishtar-aon-fix` exists solely to work around a build-time defect that is one line to fix; every future build inherits the defect.
  - Evidence: `grep -c 'SYMLINK'` returns 0 for `device_ishtar/proprietary-files.txt` and 0 for `refs/a16_ishtar/proprietary-files.txt`.
  - Step 2 impact: schedule Phase 6's first slice early and independently; it does not depend on Phase 7.

- **AUTOPSY-P2-01 — `tiles hide` is a visible control that does nothing**
  - Impact: a non-functional UI element is worse than an absent one; it erodes trust in the module's other status reporting.
  - Evidence: recorded as ineffective in project history; the option is present in the module UI.
  - Step 2 impact: a named decision gate in Phase 2 — repair, remove, or label as a known limitation.

- **AUTOPSY-P2-02 — Experimental HAL patch is over-broad**
  - Impact: RAW formats are advertised at every resolution, growing the stream-configuration array from 508 to 868 int32 entries, with no matching duration rows. This is a larger blast radius than the goal requires.
  - Evidence: `agc-50mp-yama/hal-raw50-deneme.patch`; measured array growth recorded in journal Faz 12.
  - Step 2 impact: Phase 4 acceptance criteria must state the target array size and require the duration rows the user explicitly asked for.

- **AUTOPSY-P2-03 — Superseded conclusions are not marked**
  - Impact: journal Faz 8 concludes AGC cannot exceed 15.2 MP; Faz 11 and 12 disprove it. `module.prop` v2.0 repeats the disproven causal claim. A future reader, including a future agent session, will act on stale conclusions.
  - Evidence: `50MP-Entegrasyon-Plani.md` section "AGC neden hâlâ 15,2 MP — kesin açıklama"; `module.prop` description v2.0 text.
  - Step 2 impact: a small documentation slice in Phase 1 or B; mark superseded, do not delete.

- **AUTOPSY-P2-04 — Patch-table format is undocumented**
  - Impact: the project's most reusable invention exists only implicitly in two files and one parser. It cannot be extended or reimplemented safely without reading `halpatch.sh` line by line.
  - Evidence: `blobs/hal-fullres.patch`, `agc-50mp-yama/hal-raw50-deneme.patch`, `halpatch.sh` (116 lines).
  - Step 2 impact: one documentation slice in Phase 1, written as a format contract.

- **AUTOPSY-P3-01 — Changelog duplicated in `module.prop`**
  - Impact: an approximately 1,600-character `description` field carries the full v1.2→v2.1 history in a field meant for a module summary; it will diverge from the journal.
  - Evidence: `ishtar-cam-modes/module.prop`.
  - Step 2 impact: Phase 9 documentation cleanup; move history to a `CHANGELOG.md`.

- **AUTOPSY-P3-02 — No root `README.md` and no `refs/` index**
  - Impact: twelve top-level directories and five reference trees have no explanation outside a 1,300-line Turkish journal.
  - Evidence: root `ls -la`; `ls refs`.
  - Step 2 impact: Phase 1 documentation slice.

- **AUTOPSY-P3-03 — Runtime state checked into the deliverable**
  - Impact: `ishtar-cam-modes/mode` and `ishtar-cam-modes/active/` hold live working state inside the packaged directory; a release may ship the developer's last-used mode.
  - Evidence: `ishtar-cam-modes/mode` contains `stock`; `active/` holds a 1 MB working copy of the sensor blob.
  - Step 2 impact: confirm `customize.sh` normalizes both at install time; otherwise fix in Phase 1 packaging.
