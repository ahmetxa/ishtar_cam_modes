# Faz 8.1 — Android 16 Camera Blob Comparison and Carry-Over Decision

## 1. Context

Main-Planing Phase 8 (`SNAP-2026-09-10-MAIN`) reads: "`beryl` is AOSPA's Android 16 branch, not a second device; this phase previously read it as a second Xiaomi target, which was corrected on 2026-09-10." Its first part is "the camera module work on the vendor blobs that build ships — every HAL and sensor patch is bound to one exact vendor build (Project-Ontology invariant 10)". It records one unverified hope: "The `beryl` device tree's history carries the same last blob update as the Android 15 tree (`OS2.0.101.0.VMAMIXM`), so the patches may carry over unchanged; that stays unverified until the binaries are compared." Its first vibecoding slice: "Compare the `beryl` vendor blobs' `camera.qcom.so` and IMX989 sensor module against the md5s the module guards, before committing to any re-derivation."

**This sub-plan replaces `Faz-8-Plans/Faz8.1-beryl-port-sizing.md`.** That file sized a port to "a second Xiaomi device" whose sensor, platform and HAL were unknown. The device does not exist, so none of its nine work items survives. Ledger `DEC-07`, which that sub-plan routed, was corrected by planning run 17 to read "whether to commit to the camera re-derivation on the Android 16 vendor blobs, sized by Main-Planing Phase 8's first slice". This sub-plan produces that sizing.

Main-Planing section 9 names this comparison as the one place a bounded read-only explorer may be considered. Autopsy section 11's instruction that Phase 8 "should not be decomposed until Phase 7 produces a working build environment" was written about the port that no longer exists. This sub-plan honours its intent by splitting the work: a static half that needs no build, and built-output and on-device halves that consume `Faz7.2` and `Faz7.3`.

## 2. Goal

Establish by checksum, not by firmware label, whether the Android 16 `ishtar` build ships the exact `camera.qcom.so` and IMX989 sensor module the module's guards and patch tables are bound to. Classify the HAL layer and the sensor layer each as carry-over, adaptation or re-derivation, and route `DEC-07` with that measured classification.

## 3. Description

The problem is that the whole camera capability rests on two md5 values recorded on Android 15 — `HAL_STOCK_MD5=c3fa63a86ee3ecaf9fbf02005d35f6b5` with `HAL_SIZE=27268688` in `halpatch.sh`, and `EXPECT_MD5=9e4d0fe1a8bf2eb4146c9917a0ac2c4c` in `customize.sh`. Nobody has checked them against Android 16. A shared firmware label suggests they match, but the label names the source firmware of an extraction, not the bytes. An extraction can differ through a different extraction run, a fixup, or a later partial blob update. Only the checksum answers the question.

It belongs at the head of Phase 8 because every later camera step depends on its answer. It is also the cheapest decisive measurement in the phase. The two files exist in the pinned vendor repository `xiaomi-8550/proprietary_vendor_xiaomi_ishtar` at `f92e7a9` and can be fetched and hashed from the Windows host without renting anything.

The vibecoding slice strategy is exactly Main-Planing's first slice: fetch two files at the pinned commit, hash them, compare. The fastest signal takes minutes. If both match, the patch tables' input identity holds and `Faz8.3` becomes a functional test rather than a re-derivation. If the HAL differs, the phase's cost changes by an order of magnitude, and the user should know before the device is flashed.

The layers do not carry the same cost, and the classification must not pretend they do. A different sensor module is an **adaptation**. The generators under `ishtar-cam-modes/tools/` and `verify_ln.py` are scripted, and they re-derive `blobs/*.bin` from a stock input, provided the container format and the 23-entry mode table layout still hold. A different `camera.qcom.so` is a **re-derivation**. `hal-fullres.patch` is sixteen offset patches located by disassembly inside `InitializeScalerStaticCaps`, and moving them means repeating work that Phases 3 and 4 measured in weeks. `IMPL-50` also found no code cave ≥16 bytes in that binary, which says nothing about a different binary's layout.

What should not be over-planned: the re-derivation itself. If the HAL differs, this sub-plan stops at the classification and `DEC-07`. Decomposing a re-derivation is a replanning input, not work to schedule on speculation.

## 4. Scope

- Fetching `proprietary/odm/lib64/hw/camera.qcom.so` and `proprietary/odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin` read-only at vendor commit `f92e7a9`, into an untracked scratch location.
- md5 and size of both, compared against `HAL_STOCK_MD5`, `HAL_FULLRES_MD5`, `HAL_SIZE` and `EXPECT_MD5`.
- Confirmation at the pinned device-tree commits that no `blob_fixup` in `extract-files.py` touches either file, so the vendor-repository bytes are the shipped bytes.
- The same two files' md5 in the Android 15 vendor repository branch AOSPA `vauxite` used, if reachable, to attribute any difference to a blob change rather than to measurement.
- Built-output agreement against `Faz7.2`'s post-build evidence block, and on-device agreement against `Faz7.3`'s reading.
- For the sensor module only, if it differs: a structural check of the container header and mode-table layout against what `verify_ln.py` asserts, so the adaptation label is measured.
- A per-layer classification with its basis, and a routed `DEC-07` stating the cost with reference to the project's own history.
- Recording blob identity per build in Project-Ontology and raising ledger section 7's "vendor blobs change" trigger if a guarded blob differs.

## 5. Out of Scope

- Re-deriving any HAL offset, disassembling the Android 16 `camera.qcom.so`, or regenerating sensor blobs.
- Installing or running the module on Android 16. `Faz8.3`.
- Comparing unguarded camera libraries as a pass condition. `camera.xiaomi.so` is recorded for context because `05efdac` fixes it up, but the module does not guard it.
- Committing any vendor blob to this repository. Fetched files stay in scratch and are deleted after hashing. `ARC-04` and the root `.gitignore` both keep blobs out.
- The kernel. `Faz8.2`.
- `calcite`'s blobs.

## 6. Current Repository Evidence

**The guards, measured this run.** `ishtar-cam-modes/halpatch.sh:32-34`: `HAL_STOCK_MD5=c3fa63a86ee3ecaf9fbf02005d35f6b5`, `HAL_FULLRES_MD5=fe0245a4720fb07b01d96deef47f5569`, `HAL_SIZE=27268688`. `ishtar-cam-modes/customize.sh:14`: `EXPECT_MD5=9e4d0fe1a8bf2eb4146c9917a0ac2c4c`. `ishtar-cam-modes/blobs/hal-fullres.patch` opens with "ishtar 50MP (FullRes) HAL yamasi -- A15 / vauxite", so the table itself names the build it was derived on. `docs/release-checklist.md` PC-18 records the install-time behaviour: `customize.sh` aborts on a sensor checksum mismatch, and degrades without aborting on an unrecognised HAL checksum. On a differing Android 16 blob, therefore, the module fails closed for the sensor layer and refuses the HAL patch rather than corrupting it.

**The Android 16 inputs, read this run (names only).** The pinned vendor repository at `f92e7a9` carries `proprietary/odm/lib64/hw/camera.qcom.so`, `camera.xiaomi.so`, `proprietary/odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, `com.qti.tuned.ishtar_semco_imx989_wide.bin` and `aon_front.pb`. The repository root has no `.gitattributes`, so these are ordinary git objects rather than LFS pointers, and a raw content read returns the bytes. The manifest `README.md` records the `ishtar` blob list's source firmware as `OS2.0.101.0.VMAMIXM`. `refs/a16_ishtar` history carries `e0ade7f ishtar: Update to OS2.0.101.0.VMAMIXM` — the same commit subject and id that `device_ishtar` (Android 15, `vauxite`) carries — plus `05efdac ishtar: Patch camera blob to use libui-v34`, which exists only on `beryl`.

**Fixups, read this run.** `refs/a16_ishtar/extract-files.py` applies `strip_debug_sections()` to two libraries, `add_needed('libprocessgroup_shim.so')` to `libcamxcommonutils.so`, `libchifeature2.so`, `libmialgoengine.so` and `com.qti.chi.override.so`, and to `camera.xiaomi.so` both that and `replace_needed('libui.so', 'libui-v34.so')`. No fixup names `camera.qcom.so` or the sensor module, in `refs/a16_ishtar` or `refs/a16_sm8550`. Fixups rewrite ELF dynamic sections, so a fixed-up library's md5 differs from its firmware original. That makes this confirmation necessary rather than decorative, and it must be repeated at the pinned commits rather than taken from the local checkouts.

**Cost history the classification references.** Project-Ontology section 6 holds the address book: the four format-gate sites, the located function ranges in `InitializeScalerStaticCaps` (`0x16bf4c0`–`0x16c5a90`), and the toolchain with its negative findings. `docs/reverse-engineering-toolchain.md` records the procedure. Ledger `IMPL-18` through `IMPL-51` record the measured effort of locating and proving sites on one binary. `verify_ln.py` asserts a `QTI Chromatix Header` signature and a mode table of 60-byte entries, and Project-Ontology records the blob as exactly 1,062,250 bytes with 23 modes.

**Device history.** Ledger section 6 records the live Android 15 HAL stock md5 equal to `HAL_STOCK_MD5`. Where that value came from — the on-device file of AOSPA's Android 15 build — is what F8.1-04 attributes against its vendor repository.

## 7. Planned Work Breakdown

- F8.1-01 — Fetch the two guarded blobs at the pinned commit
  - Description: Read-only raw content fetch of both paths at `f92e7a9` into an untracked scratch directory, with the commit id recorded beside each file. Re-confirm the pin is still what `ishtar-beryl.xml` names on the day.
  - Output: Two files in scratch and their provenance line.
- F8.1-02 — Hash and compare
  - Description: md5 and byte size of each, compared against `HAL_STOCK_MD5`, `HAL_FULLRES_MD5`, `HAL_SIZE` and `EXPECT_MD5`. Checking `HAL_FULLRES_MD5` catches the unlikely case of an already-patched blob.
  - Output: A four-cell comparison table, filled with measured values.
- F8.1-03 — Confirm no fixup reaches either file
  - Description: Read `extract-files.py` in both device trees at their pinned commits and confirm neither guarded path appears under `blob_fixups`.
  - Output: A fixup verdict per tree, with the commit ids read.
- F8.1-04 — Attribute any difference
  - Description: If a file differs, fetch the same path from the vendor repository branch AOSPA's Android 15 build used, and hash it. A match to the device value means Android 16 changed the blob. A mismatch means the Android 15 device file itself differs from its repository — a separate finding.
  - Output: An attribution statement, or "not needed" if both matched.
- F8.1-05 — Structural check of a differing sensor module
  - Description: Only if the sensor module differs: run `verify_ln.py`'s header and mode-table reads against it without generating anything, to establish whether the generators' assumptions still hold.
  - Output: A format verdict supporting the adaptation label, or a reason the label is re-derivation.
- F8.1-06 — Built-output agreement
  - Description: After `Faz7.2`, compare its post-build md5s with F8.1-02's values.
  - Output: Agreement, or a difference raised as a finding against the build.
- F8.1-07 — On-device agreement
  - Description: After `Faz7.3`, compare its on-device md5s with the previous two.
  - Output: Three-way agreement recorded.
- F8.1-08 — Classify each layer
  - Description: HAL: carry-over if the md5 equals `HAL_STOCK_MD5` and the size equals `HAL_SIZE`, otherwise re-derivation. Sensor: carry-over if the md5 equals `EXPECT_MD5`, adaptation if it differs with the format intact, re-derivation if the format moved. Each label carries its basis.
  - Output: A two-row classification.
- F8.1-09 — Route `DEC-07`
  - Description: State the commit question with the classification. For carry-over, the remaining cost is `Faz8.3`'s functional run. For re-derivation, cite the `IMPL-18`–`IMPL-51` history and the section 6 method as the reference cost, and flag a replanning input. The user decides.
  - Output: `DEC-07` updated with the measured basis, and a replanning input if re-derivation.
- F8.1-10 — Record blob identity and clean up
  - Description: Add a per-build blob identity entry to Project-Ontology (build, path, md5, size, source commit), raise ledger section 7's "vendor blobs change" trigger if a guarded blob differs, and delete the scratch copies.
  - Output: The ontology entry, any trigger, and an empty scratch directory.

## 8. Acceptance Criteria

- Both guarded blobs were hashed from the pinned vendor commit, with the commit id recorded beside each value.
- The comparison table holds measured md5 and size values against all four guard constants, and no cell reads "same firmware, assumed equal".
- The fixup verdict is taken at the pinned device-tree commits in both trees.
- Any difference is attributed by F8.1-04, or F8.1-04 is recorded as not needed because both matched.
- A sensor-module difference carries a structural verdict before it is labelled adaptation.
- Built-output agreement is recorded once `Faz7.2` has run, and on-device agreement once `Faz7.3` has run. Until then, each is recorded as pending, not assumed.
- Each layer has one label — carry-over, adaptation or re-derivation — with its stated basis.
- `DEC-07` carries the classification, and a re-derivation result raises a replanning input rather than scheduling work.
- Project-Ontology has the per-build blob identity entry.
- No vendor blob is tracked by git or left in scratch, and no disassembly or generation was performed.

## 9. Validation and Test Approach

Validation is host-side and static for the first half, with read-only agreement checks against the later sub-phases' evidence.

- `VAL-FETCH` (proposed) — raw content read of both paths at `f92e7a9` with the installed `gh`, and the commit id printed beside each saved file.
- `VAL-IDENTITY` (proposed) — `md5sum` and byte size of each file, compared against the four constants read directly from `halpatch.sh` and `customize.sh` in the same run, not retyped from this document.
- `VAL-FIXUP` (proposed) — a read of `blob_fixups` in both `extract-files.py` files at their pinned commits, confirming neither guarded path appears.
- `VAL-FORMAT` (proposed, conditional) — `verify_ln.py`'s header and mode-table assertions against a differing sensor module, read-only.
- `VAL-AGREE` (proposed) — the three-way comparison with `Faz7.2`'s and `Faz7.3`'s recorded values.
- `VAL-DOCS` (proposed) — read back the classification, `DEC-07` and the ontology entry.
- `VAL-CLEAN` (proposed) — `git status --short` shows no blob, and the scratch directory is empty.

Local versus live: the static half is local plus a GitHub read. The agreement checks consume live evidence but perform no device action themselves. Security validation is limited to keeping blobs untracked. Ontology validation applies to invariant 10, and to keeping *stock* distinct as a restore target, a mode name and the Android 16 build's unmodified blob.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/halpatch.sh | existing | Source of `HAL_STOCK_MD5`, `HAL_FULLRES_MD5` and `HAL_SIZE`, read in the same run as the comparison. | VAL-IDENTITY |
| ishtar-cam-modes/customize.sh | existing | Source of the sensor blob `EXPECT_MD5`. | VAL-IDENTITY |
| ishtar-cam-modes/blobs/hal-fullres.patch | existing | Read-only: its header names the build it was derived on. | VAL-IDENTITY |
| ishtar-cam-modes/tools/verify_ln.py | existing | Read-only structural check of a differing sensor module; nothing is generated. | VAL-FORMAT |
| refs/a16_ishtar/extract-files.py | existing | Local copy for orientation; the fixup verdict is taken at the pinned commit. | VAL-FIXUP |
| Planner-docs/Project-Ontology.md | modified | Per-build blob identity entry. | VAL-DOCS |
| Planner-docs/Planing-Ledger.md | modified | `DEC-07` basis, the implementation row, and any section 7 trigger. | VAL-DOCS |

## 10. Dependencies and Sequencing

**The static half (F8.1-01 through F8.1-05, F8.1-08 and F8.1-09 on static values) depends on nothing but `Faz7.1`'s confirmation of the vendor pin, and may run before `Faz7.2`.** This is execution-order guidance, not a phase renumbering, and the precedent is `Faz6.1`, which the index schedules early for the same reason: read-only, independent, and informative for everything after it. Running it early lets `Faz7.3`'s go/no-go state the camera consequence as a measurement.

The agreement half (F8.1-06, F8.1-07) depends on `Faz7.2` and `Faz7.3` respectively, and the final classification is not closed until both have reported or been recorded as not reached.

Blocks `Faz8.3`, which runs only on a carry-over or completed-adaptation classification. Does not block `Faz8.2`.

Required decisions: `DEC-07`, the user's, on the measured classification.

Required credentials: the host `gh` session for the raw content read. The vendor repository is public.

Required infrastructure: network access and roughly 30 MB of scratch space.

Required human approvals: `DEC-07`. No device action occurs.

Fresh session token and context risk: low. Two files, four constants, one fixup read. Main-Planing's `high` band for Phase 8 describes re-derivation, which this sub-plan does not perform. Subagents: Main-Planing section 9 permits a bounded read-only explorer here, but the comparison is too small to benefit; not recommended.

## 11. Risks and Mitigations

- Risk (invariant 10): the classification is taken from the firmware label instead of the bytes. Impact: `Faz8.3` installs onto a different binary on a false premise. The guards would then refuse the HAL patch — safely, but `Faz8.3` is wasted. Mitigation: acceptance requires measured md5 and size in every cell.
- Risk: a fixup at the pinned commit alters a guarded file although the local checkout shows none. Impact: the repository hash differs from the shipped bytes. Mitigation: F8.1-03 reads the pinned commits, and F8.1-06 cross-checks against the build output.
- Risk: the vendor repository value is right but the built or flashed file differs. Impact: a correct static result is applied to the wrong file. Mitigation: three-way agreement is required before the classification closes.
- Risk: a sensor-module difference is labelled adaptation without checking the format. Impact: the generators run on a layout they do not understand and emit plausible garbage. Mitigation: F8.1-05 is a precondition for that label.
- Risk: a HAL difference leads straight into disassembly because the history makes it feel familiar. Impact: weeks of unapproved work. Mitigation: out of scope; `DEC-07` and a replanning input are the only outputs.
- Risk: a fetched blob is committed or left behind. Impact: redistribution through the private remote, contrary to `ARC-04`. Mitigation: scratch only, `VAL-CLEAN`.
- Risk: the static half is skipped because Phase 7 is "not done". Impact: the device is flashed without knowing whether the camera work survives. Mitigation: section 10 states the static half's independence explicitly, and the index schedules it early.

## 12. Desired End State

The identity of the Android 16 `camera.qcom.so` and IMX989 sensor module is known by checksum at the pinned vendor commit, confirmed free of fixups, and agreed against the build output and the device once those exist. Each camera layer carries one measured label. `DEC-07` states the commit question on that basis. If a guarded blob differs, the ledger carries the section 7 trigger rather than an improvised re-derivation. The ontology records which blob each build ships.

Evidence the implementer produces: the provenance lines, the comparison table, the fixup verdicts, any attribution and format verdict, the three-way agreement, and the classification.

The ledger summary Step 4 appends: md5 and size of both blobs at `f92e7a9`, match or mismatch against each constant, the fixup verdict, agreement status, the per-layer labels, the `DEC-07` update, and any trigger.

## 13. Next Sub-Phase Transition Criteria

- Both layers are labelled with a measured basis.
- Three-way agreement is recorded, or its missing legs are recorded as not reached with the reason.
- For `Faz8.3` to start, the HAL layer is carry-over and the sensor layer is carry-over or its adaptation is complete; otherwise `Faz8.3` is blocked and the replanning input is in the ledger.
- `DEC-07` reflects the classification.
- No vendor blob remains in the workspace.
