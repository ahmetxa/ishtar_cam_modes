# ishtar — Xiaomi 13 Ultra camera workspace

Workspace for the IMX989 main-camera work on the Xiaomi 13 Ultra (`ishtar`):
sensor-driver mode switching, a full-resolution camera HAL patch, an AON
front-camera fix, and an AOSPA Android 16 track. The Android 16 track was
abandoned on 2026-11-13 (`DEC-28`); the phone now runs HyperOS 4, and none
of the project's modules is installed.

This file describes what each top-level path **is**. It does not describe how
the system works — `Planner-docs/Project-Ontology.md` does that. See
[Orientation](#orientation) for where a fresh session should start.

## Deliverables

The actual work lives in three directories. Everything else is input, reference,
or record.

| Path | Role | What it is |
|---|---|---|
| `ishtar-cam-modes/` | **deliverable** | The main KernelSU/Magisk module. Ten sensor modes plus the 50MP HAL layer, a WebUI, and four QS tiles. Source at v2.2 / versionCode 13. |
| `ishtar-aon-fix/` | **deliverable** | Standalone module that copies `/vendor/lib64/camera` into the module, adds `aon_front.pb` and bind-mounts the directory; it exits without change when the file already exists (HyperOS 4 ships it). Deliberately independent of module mounting. v1.1. |
| `agc-50mp-yama/` | **deliverable** | The AGC (GCam port) 50MP patch: the reproduction recipe (`README.md`), two smali sources, seven experimental HAL patch tables (`hal-*-deneme.patch`), four Faz 4.1 stage tables (`f41-*.tbl`), `find_tag_write_site.py` and `tools/`. |

## Documentation

| Path | Role | What it is |
|---|---|---|
| `Planner-docs/` | **record** | Planning and continuity artifacts. See [Orientation](#orientation) for the reading order. |
| `docs/` | **record** | 18 documents: formats, procedures, evidence, runbooks and the generated release manifest. The two format and procedure contracts are `patch-table-format.md` and `reverse-engineering-toolchain.md`. |
| `README.md` | **record** | This file. |
| `PROJECT_LOG.md` | **record** | Project log (Turkish): the continuity record of work done. |
| `NEXT_PROMPT.md` | **record** | Entry prompt for the next session (Turkish). |
| `ORCHESTRATION_PLAN.md` | **record** | The window plan for the current run (Turkish). |
| `CHANGELOG.md` | **record** | Module release notes. |
| `UNTRACKED-BY-DESIGN.md` | **record** | Why the large paths are absent from version control. Summarised under [Exclusions](#exclusions). |
| `50MP-Entegrasyon-Plani.md` | **record** | The 50MP integration journal. Long, partly superseded; sections are marked in Phase 9, not here. |

The repository's remote is the private GitHub repository `ahmetxa/ishtar_cam_modes` (`DEC-27`); pushes use explicit refspecs only.

## Build inputs and reference trees

**The distinction that matters:** `device_ishtar/` is the tree a build would
consume. Everything under `refs/` is a **comparison source** — read to answer
"how does a working tree declare this?", not compiled.

| Path | Role | What it is |
|---|---|---|
| `device_ishtar/` | **build input** | The live AOSPA device tree, `android_device_xiaomi_ishtar`, branch `vauxite`. **Its own git clone with its own remote and history** — it is not tracked by this repository, and edits to it are committed there, not here. Has its own `README.md`. |
| `refs/` | **reference** | Five comparison trees. Indexed below. |
| `android_kernel_qcom_sm8550/` | **reference** | QCOM kernel checkout. |
| `android_kernel_xiaomi_sm8550/` | **reference** | Xiaomi kernel checkout. |
| `common_sm8550/` | **reference** | Common platform tree. |
| `13U-989-DCG16+LN2+LN4/` | **reference** | Source material for the DCG/LN sensor register work. |
| `Module_Highres_13U_Switcher_A14/` | **reference** | Prior-art module the current one supersedes. |

### The `refs/` index

Five trees. **Roles marked _inferred_ were read from directory naming and file
count, not from an in-tree statement**; the rest are quoted from each tree's own
`README.md` or from its git remote.

| Tree | Files | Target | Role | Basis |
|---|---|---|---|---|
| `refs/neo_ishtar` | 250 | AOSPA (Paranoid Android), ishtar | Comparison source. **The authority for `proprietary-files.txt` syntax** — its line 1154 is the cited source for the `;SYMLINK=` form used by Faz 6.1. | Stated: "Copyright (C) 2023 Paranoid Android — Device configuration for Xiaomi 13 Ultra" |
| `refs/a16_ishtar` | 76 | Android 16, ishtar | Device tree for the A16 track. Carries the mirrored Faz 6.1 `;SYMLINK=` edit. | Stated: "Device configuration for Xiaomi 13 Ultra (ishtar)" |
| `refs/a16_sm8550` | 165 | Android 16, sm8550 | **Platform** tree, not a device tree. Contains no `aon_front` reference, which is why Faz 6.1 did not edit it. | Stated: "Common device configuration for Xiaomi 8550 family" |
| `refs/los_ishtar` | 67 | LineageOS, ishtar | Comparison source for device-level declarations. | Stated: "Copyright (C) 2025 The LineageOS Project — Device configuration for Xiaomi 13 Ultra" |
| `refs/los_sm8550` | 150 | LineageOS, sm8550 | Platform tree. _Inferred_ — this is the one tree with **no README**; the role is read from its name and from the `los_ishtar` / `a16_sm8550` pattern. | **Inferred, not verified** |

**On `refs/` being unversioned.** Faz 1.1 excluded all of `refs/` as externally
sourced. One consequence is live: the Faz 6.1 edit to
`refs/a16_ishtar/proprietary-files.txt` has **no history anywhere**. It is a
single line whose source is cited above, so it is cheap to reproduce — but it is
not recoverable by `git`.

## Artifact manifest

Root-level binaries, identified by checksum. None of these is in version
control; see [Exclusions](#exclusions).

### Release archives

| Archive | md5 | Status |
|---|---|---|
| `ishtar-cam-modes-v2.1.zip` | `fea919b67a4693a4591127be4a6e9daa` | Superseded by v2.2. Was versionCode 12; flashed on AOSPA A15 on 2026-08-31 (`IMPL-11`). |
| `ishtar-cam-modes-v2.0.zip` | `9c115f5d6ab03f5a8a264e3bf3106495` | Superseded by v2.1 on 2026-08-31. Was versionCode 11. |
| `ishtar-cam-modes-v1.9.zip` | `d7845bc848b6ea72297c50a821ef260a` | Superseded. |
| `ishtar-cam-modes-v1.0.zip` | `9cf8facb01d7e87c67cbfa60b0bdb0ff` | Superseded. |
| `ishtar-aon-fix-v1.1.zip` | `f7a6352db73050f73bd27f62e62dd453` | Current AON fix release. |

All five were audited for signing-key containment on 2026-08-24 and are
**clean** — no keystore entry in any of them.

`dist/` (excluded by `*.zip`) holds `scripts/build-release.py` outputs, not root archives: `ishtar-cam-modes-v2.2.zip` (md5 `e95789572311cc95266d3ab4045cdcba`; installed on AOSPA A15 by `IMPL-81`) and `ishtar-cam-modes-v2.1.zip` (md5 `4a8226d6f4c4cacd97d8b96086bb36fa`), an `IMPL-76` rebuild that differs from the root v2.1 archive. On HyperOS 4 no project module is installed.

### Application builds

| APK | md5 | Status |
|---|---|---|
| `AGC8.4.300_V9.6_50MP_patched.apk` | `ce65f862c990e2acc02be356f75a7122` | **Currently installed** as `org.codeaurora.snapcam`, confirmed by md5 against the live package on 2026-08-30. This is the patched build, not stock. |
| `AGC8.4.300_V9.6_snap.apk` | `fa4066eb3bf82cc097906fd108073500` | Stock V9.6 — the **input** to the patch above. |
| `AGC8.4.300_V14_snap.apk` | `46763b3628f025a54828aab05c01d47a` | Stock V14. Comparison build; identical obfuscation map to V9.6. |
| `OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk` | `e4efeb07919bce10bc14f6f42e5b09f2` | Third-party consumer; proves 8192x6144 capture works outside AGC. |

The AGC port's redistribution question is open and is **not** settled by listing
these checksums. No download location appears in this repository.

### Configuration and reference binaries

| File | Note |
|---|---|
| `50mpx_agc_config.agc` | AGC configuration export. **⚠ Preference trap — see below.** |
| `12mpx_agc_config.agc` | AGC configuration export. **⚠ Preference trap — see below.** |
| `com.qti.sensormodule.ishtar_semco_imx989_wide.bin` | md5 `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` — the **stock** sensor driver, and the exact value the module's install and boot guards require. An OTA that changes this invalidates every patch offset at once. |

> **⚠ Preference trap.** Both `.agc` files contain the `pref_raw_key` and
> `pref_fix_resolution_key` families — **all twelve key names in each file**,
> verified 2026-08-31 (a bare key plus `_0`..`_4`, twice).
> **Importing either one re-arms the trap.** A pinned resolution or format
> preference overrides what the HAL advertises, so a measurement taken after an
> import measures the preference, not the HAL — and the result looks like the
> patch failed.
>
> **Device state, measured 2026-09-05 (Faz 3.10): two of the twelve keys are
> PRESENT at value `0`, and both are measured inert** — identical stream
> configuration with them present and absent (`IMPL-53`, `IMPL-54`). **Audit by
> value, not by presence:** only a non-zero value is a fault.
>
> **AGC does self-arm two keys** — `pref_raw_key` and `pref_fix_resolution_key`,
> at value `0`, when its **settings screen** opens (`FIND-3.7-01`, `IMPL-54`). A
> plain launcher start arms nothing. The 2026-08-31 note that "the app does not
> self-arm the trap" was measured against a plain launch from an empty first-run
> state, which is a strictly weaker test; it is corrected here and in full in
> `docs/phase3-preconditions.md` section 1. At least one further re-arming route
> exists and is unidentified (`FIND-3.10-02`).
>
> Audit procedure, clearance procedure and the per-measurement checklist are in
> [`docs/phase3-preconditions.md`](docs/phase3-preconditions.md); run the
> per-key **value** audit before any Phase 3 measurement rather than trusting a
> single `smoke.sh` reading, whose probe reads key names only (`FIND-5.2-01`,
> `FIND-3.7-02`).
>
> **The AGC 12.58 MP configuration this project ships — how to set it, how to
> verify it, its failure mode, and why 50 MP in AGC is retired — is
> [`docs/agc-12mp-configuration.md`](docs/agc-12mp-configuration.md).**

### Tooling and working paths

| Path | Role |
|---|---|
| `platform-tools/` | **tooling** — vendored `adb`; the only host-device channel. |
| `scripts/` | **tooling** — `smoke.sh`, the read-only device state snapshot; `build-release.py`, the deterministic release builder (`--self-test`). |
| `snapshots/` | **record** — smoke output, `<yyyymmdd-HHMM>__<subplan>__<label>.txt`. The time in the name is typed by the operator and is not a reliable clock: it matches the header time as UTC in some files and as UTC+3 in others. The header's `taken` line is UTC and authoritative. |
| `.gitignore`, `.gitattributes` | **tooling** — `.gitattributes` disables CRLF conversion, which matters: the module's shell scripts run under the on-device shell and a CRLF checkout would restore a broken module. |
| `.claude/`, `.git/` | **tooling** — local state. |

## Orientation

A session first reads `NEXT_PROMPT.md`, then `ORCHESTRATION_PLAN.md` (the window plan), then the list below.

A session starting with no context should read, in this order:

1. **`Planner-docs/Project-Ontology.md`** — durable facts. Vocabulary, the
   invariants, and the reverse-engineering address book. The address book holds
   values that are expensive to re-derive and **have been lost to context
   truncation before**; read it before deriving any offset.
2. **`Planner-docs/Project-Comprehension.md`** — what is known, how confidently,
   and on what evidence. Claims carry a confidence value; do not promote a
   `tentative` one by repeating it.
3. **`Planner-docs/Planing-Ledger.md`** — what has been done and verified, slice
   by slice, with the evidence each produced.
4. **`50MP-Entegrasyon-Plani.md`** — narrative history. Long and partly
   superseded; read for *why*, not for current state.

Then the two contracts in `docs/` when touching a patch table or a tool.

**One standing warning.** A workspace file is not a mirror of the device. The
`ishtar-cam-modes/mode` file records the last host-side edit; the device's live
mode is whatever its sensor blob md5 says it is. The two have already been
observed to disagree. `scripts/smoke.sh` is what answers "what is the device
actually running?"

## Exclusions

Large paths are absent from version control **by design**, not by oversight.
Full rationale and recovery route for each is in `UNTRACKED-BY-DESIGN.md`; the
summary is:

| Excluded | Why | How to recover |
|---|---|---|
| `refs/`, kernel checkouts, `common_sm8550/` | Externally sourced trees; large, and upstream already has the history. | Re-clone from upstream. |
| `device_ishtar/` | **Already its own git clone** with its own remote and history. Nesting it would store a gitlink that restores no file content. Commit edits *there*. | Its own remote. |
| Root APKs, release zips, the sensor `.bin` | Large binaries; identified by checksum in the manifest above. | Supplied separately. |
| `ishtar-cam-modes/active/`, `mode`, `lang` | Runtime state, regenerated on boot. Confirmed absent from the release archives too. | Regenerated. |
| `ishtar-cam-modes/active_hal/` | Never exists in the workspace at all — it is seeded **on the device** from the device's own 27 MB stock HAL, which is why no 27 MB blob ships. | Created by `hal_seed` at boot. |
| `tile-app/debug.keystore`, `tile-app/out/`, `tools/__pycache__/` | Credentials and build output. | Not recoverable by design; the keystore has never been distributed. |

Two deliberate deviations from the original scope list — the exclusion of
`device_ishtar/` and the *inclusion* of the two `.agc` files — are argued in
`UNTRACKED-BY-DESIGN.md` section 7.

## Language convention

This is deliberate, not drift (Main-Planing risk `R11`):

- **User-facing documents and the module interface are Turkish**, with English
  in the WebUI, which ships both and defaults to English independently of system
  language.
- **Planner artifacts and the `docs/` contracts are English.**
- Source comments are Turkish, matching the module's audience.

Do not "normalise" one into the other; both audiences are real.
