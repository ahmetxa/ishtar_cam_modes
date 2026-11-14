# Untracked by Design

Written by **Faz 1.1 — Version Control Bootstrap**. This file exists so that a
future reader never mistakes exclusion for absence. Every path listed here is
deliberately outside the repository, with a stated reason and a stated recovery
route. If a path is missing and is not listed here, that is a real loss and
should be investigated.

Faz 1.6 (Workspace README and Reference Tree Index) has run (verified, 2026-08-30).
The root `README.md` summarises the exclusions; this file remains the detailed record.

## 1. Measured Sizes

These figures replace the tentative "roughly 465 MB" estimate carried as `EV-18`
in `Planner-docs/Project-Comprehension.md`. That number was a sum of root-level
file bytes only; it did not include any directory. Measured 2026-08-24 with
`find <dir> -type f -printf '%s\n'` summed per directory, because a whole-tree
scan had previously timed out.

| Path | Size | Files | Tracked? |
|---|---|---|---|
| `android_kernel_qcom_sm8550/` | 3545.0 MiB | 74023 | No |
| `android_kernel_xiaomi_sm8550/` | 3353.2 MiB | 70052 | No |
| Root-level files (all) | 454.4 MiB | 15 | Partly — see section 3 |
| `Module_Highres_13U_Switcher_A14/` | 88.7 MiB | 15 | No |
| `platform-tools/` | 17.7 MiB | — | No |
| `ishtar-cam-modes/` | 10.4 MiB | 73 | Partly — see section 4 |
| `13U-989-DCG16+LN2+LN4/` | 7.4 MiB | 23 | No |
| `refs/` | 5.6 MiB | — | No |
| `device_ishtar/` | 1.5 MiB | 80 | No — see section 2 |
| `common_sm8550/` | 0.8 MiB | 153 | No |
| `Planner-docs/` | 0.7 MiB | 38 | Yes |
| `agc-50mp-yama/` | <0.1 MiB | 4 | Yes |
| `ishtar-aon-fix/` | <0.1 MiB | 3 | Yes |

**Total workspace: approximately 7.3 GiB.** The tracked set was 86 files at the Faz 1.1 commit `ff6934e` (2026-08-24, `IMPL-01`); it was 350 files on 2026-11-13 (measured for `IMPL-96`).

`kernel_clone.log` held the line `fatal: destination path 'kernel_ishtar' already exists and is not an empty directory.`;
`common_clone.log` held only `Cloning into 'common_sm8550'...`. Neither log explains why `common_sm8550/` holds 153 files rather than a full kernel tree. This is recorded as an observation, not repaired here. Both logs were never tracked and were deleted on 2026-11-13; their content is quoted in `PROJECT_LOG.md` section 2.1.

## 2. Externally Sourced Trees

| Path | Reason | Recovery |
|---|---|---|
| `android_kernel_qcom_sm8550/` | Upstream kernel checkout, 3.5 GiB. Not project-authored. | Re-clone from upstream. |
| `android_kernel_xiaomi_sm8550/` | Upstream kernel checkout, 3.4 GiB. Not project-authored. | Re-clone from upstream. |
| `common_sm8550/` | Partial/failed clone of the common kernel tree. | Re-clone. |
| `platform-tools/` | Google Android SDK platform-tools distribution. | Re-download from Google. |
| `refs/` | Reference and comparison sources, not build inputs. Which of these are build inputs versus comparison sources is the open question Faz 1.6 resolves. | Re-obtain from the original sources once Faz 1.6 indexes them. |
| `13U-989-DCG16+LN2+LN4/` | Upstream reference module tree. | Re-obtain from its source. |
| `Module_Highres_13U_Switcher_A14/` | Upstream reference module tree, 88.7 MiB. | Re-obtain from its source. |
| `device_ishtar/` | **This directory is its own git repository** — a clean clone of `https://github.com/AOSPA/android_device_xiaomi_ishtar.git`, branch `vauxite`, with full history and a remote. It already has the history and rollback path this sub-phase exists to create. Nesting it inside the parent repository would record only a gitlink, which restores no file content. | Its own `git` history. **Faz 6.1 edits this tree** — that edit is recoverable through the `device_ishtar/` repository, and must be committed there, not here. |

## 3. Root-Level Binaries, Snapshots, and Logs

| Path | Reason | Recovery |
|---|---|---|
| `AGC8.4.300_V14_snap.apk`, `AGC8.4.300_V9.6_snap.apk`, `AGC8.4.300_V9.6_50MP_patched.apk`, `OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk` | 452 MiB of third-party application binaries. The `_50MP_patched` build is regenerable from the tracked smali sources in `agc-50mp-yama/` plus the recorded procedure. | Re-download the stock builds; re-apply the tracked patch for the patched one. |
| `ishtar-cam-modes-v1.0.zip`, `v1.9.zip`, `v2.0.zip`, `v2.1.zip`, `ishtar-aon-fix-v1.1.zip` | Release snapshots. The repository's history starts at v2.1 (`ff6934e`), so it holds no source for v1.0, v1.9 or v2.0. | Not reproducible byte for byte: `scripts/build-release.py` packages only `ishtar-cam-modes`, and its v2.1 build in `dist/` (IMPL-76) differs from this archive; the repository has no tags. Keep the archives. The Faz 1.2 audit of these five archives for the signing keystore closed clean (`DEC-05`, IMPL-02, 2026-08-24): no keystore entry in any of them, and no rotation or withdrawal was needed. |
| `com.qti.sensormodule.ishtar_semco_imx989_wide.bin` | 1.0 MiB stock sensor blob, identical in size to the nine variants. Vendor-sourced. | Extract from the device or from the vendor image. |
| `common_clone.log`, `kernel_clone.log` | Transient tooling output. | Deleted 2026-11-13; content quoted in `PROJECT_LOG.md` section 2.1. |

## 4. Regenerable Module Artifacts

| Path | Reason | Recovery |
|---|---|---|
| `ishtar-cam-modes/blobs/*.bin` (nine variants) | Each is 1,062,250 bytes and every one is generated from the stock blob by the tracked scripts in `ishtar-cam-modes/tools/`. Storing nine near-identical megabyte binaries would dominate the pack for no recoverability gain. | `ishtar-cam-modes/tools/ln_multimode.py`, `dcg_multimode.py`, `port_sensor_mod.py`; verified by `tools/verify_ln.py`. |
| `ishtar-cam-modes/active/*.bin` | Runtime copy of whichever variant is selected. | Copied from `blobs/` at runtime. |
| `ishtar-cam-modes/tile-app/out/` | Build output: `.class`, `.dex`, the signed `.apk`, and the generated `R.java`. | `ishtar-cam-modes/tile-app/build.sh` from the tracked `java/`, `res/`, and `AndroidManifest.xml`. |
| `ishtar-cam-modes/tile-app.apk` | A copy of the built tile application. | Same build script. |
| `ishtar-cam-modes/candidates/*.bin` | Faz 5.1 candidate blob (`dcgB-m0-12bit.bin`), kept out of `blobs/` so no mode switch can select an unproven variant (`.gitignore:56-58`). | Regenerated by `ishtar-cam-modes/tools/mode0_12bit.py`. |
| `__pycache__/`, `*.pyc` | Python bytecode. | Regenerated on import. |

**Not excluded, and deliberately so:** `ishtar-cam-modes/blobs/hal-fullres.patch`
(1,144 bytes) and `agc-50mp-yama/hal-raw50-deneme.patch` (1,377 bytes). Between
them they encode twenty patch sites derived from disassembling a 27 MB stripped
binary, and they exist in no other form. Protecting these two files is the
reason this sub-phase is first in the roadmap. The `blobs/*.bin` rule is written
to match only `.bin`, never `.patch`.

## 5. Credentials

`ishtar-cam-modes/tile-app/debug.keystore` (2,664 bytes) is excluded by three
rules at the top of `.gitignore`: `debug.keystore`, `*.keystore`, and `*.jks`.
This rule was written **before** the first commit, which is the single ordering
constraint inside Phase 1. It prevents the next escape; it does not undo a
previous one. Whether the key was inside a released archive is answered: none of the
five archives holds a keystore entry, and `DEC-05` closed clean on 2026-08-24 (IMPL-02).

## 6. Local Tooling State

`.claude/settings.local.json` holds per-machine Claude Code permission state and
is not a project artifact.

## 7. Two Deviations from the Faz 1.1 Scope List

Both are recorded here rather than applied silently.

**`device_ishtar/` was excluded, though Faz 1.1 section 4 lists it as tracked
content.** The sub-plan was written before anyone observed that the directory is
an independent git clone. Adding it to the parent would produce an embedded-repo
gitlink storing no content, which is strictly worse than the history it already
has. The goal of this sub-phase — every artifact has history and a rollback path
— is already satisfied for this tree by its own repository. See section 2.

**`12mpx_agc_config.agc` and `50mpx_agc_config.agc` were tracked, though Faz 1.1
section 4 lists neither them nor an exclusion rule for them.** They are 109 KB
and 111 KB of UTF-8 XML — hand-tuned AGC preference exports, small, text, and
not regenerable by any script in this workspace. They fall squarely in the class
of artifact this sub-phase exists to protect, and section 6 of the sub-plan
enumerated the root listing without mentioning them in either direction, so the
omission reads as an oversight rather than a decision. Excluding them would have
been the "silently excludes a source file" failure named in the risk register of
the sub-plan itself.

## 8. A Warning About the Patch Tables

Tracking `hal-fullres.patch` and `hal-raw50-deneme.patch` gives them history. It
does **not** make their offsets portable. Every offset in both tables is bound
to one exact vendor build of `camera.qcom.so`; a system update invalidates all
of them at once. The md5 guard inside the patch tooling is the detector, not the
version control. This is risk `R8` in `Planner-docs/Main-Planing.md` and
invariant 10 in `Planner-docs/Project-Ontology.md`.

## 9. Version Control Scope

This repository's remote is **private**. From 2026-09-10 it was the private
`ahmetxa/ishtar` (`DEC-01`, IMPL-90); since 2026-11-13 `origin` is the private
`ahmetxa/ishtar_cam_modes` (`DEC-27`), to which 62 commits were pushed with unchanged
hashes. `DEC-05` was cleared before any remote was added. The remote stays private
because `snapshots/` holds full-resolution camera captures.
