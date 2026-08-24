# Faz 9.1 — Reproducible Release Build

## 1. Context

Main-Planing Phase 9's goal is "Make releases reproducible, documented, and verifiable", and its description names the first deliverable: "A build script that produces the zip from the tree." Its acceptance signal is "A release built from a clean checkout matches the shipped artifact."

Autopsy records the gap as an architectural absence. `ARC-08` in Project-Comprehension: "Releases are reproducible from the tree — No build script exists; four zips have no visible producer", status `absent`. Autopsy section 4 lists under "Missing or unclear": "A release/build script — the four release zips have no visible producer."

Two earlier sub-phases deposited requirements here. Faz 1.2 produced a packaging assertion specification — no credential entry, no entry at the vendor binary's size class, and no unintended archive entries — and registered Faz 9.1 as its implementor. Faz 1.5 routed any packaging hygiene findings here, including the install-state question about whether the packaged `mode` file determines the post-install mode.

By this point the release contents have also changed. Phase 4 consolidated the HAL patch tables and possibly renamed a HAL state. Phase 5 may have adopted a new sensor blob and changed the dispatch. A build script written now packages a materially different module from the one that produced `ishtar-cam-modes-v2.1.zip`.

## 2. Goal

Produce a build script that generates the release archive from the tree deterministically, enforcing the packaging assertions that earlier phases specified, so that a release is reproducible and its contents are guaranteed rather than assumed.

## 3. Description

The problem is that four releases exist and nothing knows how they were made. Every future release is a manual assembly, and manual assembly is what makes the packaging assertions from Faz 1.2 unenforceable — a rule nobody executes is a rule nobody follows.

It belongs in Phase 9 because the release contents stop moving only after Phases 4 and 5 settle. Main-Planing section 9 says so directly: Phase 9 "should be decomposed only after C and D settle, since the release contents are still moving."

The vibecoding slice strategy: enumerate what belongs in the archive, write the script that assembles exactly that, then add the assertions as a failing gate rather than a warning. The fastest validation signal is building twice and comparing — a script that produces two different archives from an unchanged tree is not a build script.

What should not be over-planned: continuous integration, signing infrastructure, or release publishing. There is no CI in this project and adding one is not justified by a single-maintainer workflow with a manual flash step.

Determinism deserves a specific decision rather than an assumption. Archive formats commonly embed timestamps, which makes byte-identical output across two runs harder than it looks. The script should either produce byte-identical archives or state explicitly which fields vary and verify content equality instead. Either is acceptable; leaving it undefined is not, because the acceptance signal "matches the shipped artifact" needs a definition of matches.

The tile application is the one component that is not simply copied. `ishtar-cam-modes/tile-app/build.sh` compiles and signs it, which means a fully reproducible release either invokes that build or packages a prebuilt artifact with a recorded checksum. That choice interacts with Faz 1.2's key location policy, since the build path needs the signing key and the packaging path does not.

## 4. Scope

- An enumeration of exactly what belongs in the release archive, derived from what the module needs at install and boot.
- A build script that assembles the archive from the tree.
- Enforcement of the Faz 1.2 packaging assertions as a hard gate that fails the build.
- Resolution of the install-state question Faz 1.5 raised: whether the script normalizes the packaged `mode` file rather than shipping the working tree's value.
- A determinism decision: byte-identical output, or defined content equality with the varying fields named.
- A decision on the tile application: built by the script or packaged as a prebuilt artifact with a recorded checksum.
- A manifest binding the release to the checksums it expects, which Autopsy section 9 identifies as the gap in the project's otherwise strong artifact integrity.
- Verification by building twice and comparing.

## 5. Out of Scope

- Continuous integration or any automated trigger.
- Publishing, uploading, or distributing a release.
- The release verification checklist, which is Faz 9.2.
- Documentation consolidation, which is Faz 9.3.
- Any change to module behavior. The script packages what exists.
- Rebuilding or re-signing previously released archives.
- Signing key rotation, which was Faz 1.2's conditional work.
- Packaging the AON module, unless Faz 6.2's disposition decision merged it — in which case the merge is already reflected in the tree.

## 6. Current Repository Evidence

`ishtar-cam-modes/` contains the module's shipped surface: `action.sh`, `customize.sh`, `halpatch.sh`, `post-fs-data.sh`, `service.sh`, `setmode.sh`, `module.prop`, `Kullanim.txt`, `lang`, `mode`, `tile-app.apk`, `webroot/index.html`, nine `blobs/*.bin`, `blobs/hal-fullres.patch`, and `active/com.qti.sensormodule.ishtar_semco_imx989_wide.bin`.

Two of those are working state rather than deliverable content. Autopsy `AUTOPSY-P3-03` records it: "`ishtar-cam-modes/mode` and `ishtar-cam-modes/active/` hold live working state inside the packaged directory; a release may ship the developer's last-used mode." Faz 1.5 was to confirm whether `customize.sh` normalizes this.

`ishtar-cam-modes/customize.sh` was read in this Step 2 run and contains no statement that writes the `mode` file. It sets permissions with `set_perm_recursive "$MODPATH" 0 0 0755 0644` and five explicit `set_perm` calls on the shell scripts. It prints "Baslangic modu: ilk kurulumda stock; guncellemede mevcut mod", which describes the intent, and the absence of a write means the packaged file supplies it. That makes the build script the correct place to normalize, since it is the only step between the working tree and the archive.

`ishtar-cam-modes/active/` holds a 1 MB working copy of the sensor blob, and `halpatch.sh` creates `active_hal/` at runtime by seeding from the device. Neither belongs in the archive: `active/` duplicates content already in `blobs/`, and `active_hal/` is created on device precisely so the 27 MB binary is never shipped.

`ishtar-cam-modes/tile-app/` holds `AndroidManifest.xml`, `build.sh`, and `debug.keystore`. The keystore must never enter the archive, which is Faz 1.2's assertion. `ishtar-cam-modes/tile-app.apk` is the built artifact sitting one level up, already outside the `tile-app/` directory — which suggests the existing manual process copies it out, and the script should formalize that.

`halpatch.sh` records why the size assertion matters: it states explicitly that the 27 MB HAL binary is deliberately not shipped and that only the roughly 900-byte patch table is carried. `HAL_SIZE=27268688` is the number the assertion should test against.

Autopsy section 9 identifies the manifest gap: "these guarantees are per-file and there is no manifest binding a *release* to the set of md5s it expects."

Four release archives exist at the root — v1.0, v1.9, v2.0, v2.1 — plus `ishtar-aon-fix-v1.1.zip`. Faz 1.2 audited all five for the keystore.

## 7. Planned Work Breakdown

- F9.1-01 — Enumerate the archive contents
  - Description: Determine exactly what the module needs at install and at boot, and exclude everything else. `active/` and the `tile-app/` source directory are the two obvious exclusions; `mode` is a normalization case rather than an exclusion.
  - Output: A contents specification with a rationale per exclusion.
- F9.1-02 — Decide the tile application handling
  - Description: Choose between building it in the script, which requires the signing key at build time, and packaging the prebuilt artifact with a recorded checksum. The choice interacts with Faz 1.2's key location policy.
  - Output: A recorded decision with its key-handling consequence.
- F9.1-03 — Decide the determinism standard
  - Description: Choose byte-identical output or defined content equality, and name the varying fields if the latter. This defines what "matches the shipped artifact" means.
  - Output: A determinism standard.
- F9.1-04 — Write the build script
  - Description: Assemble the archive from the tree per the contents specification, normalizing the packaged `mode` file to the intended install default.
  - Output: A build script.
- F9.1-05 — Implement the packaging assertions as a hard gate
  - Description: Implement Faz 1.2's specification so the build fails rather than warns: no entry ending in the keystore extension, no entry at or near the 27,268,688-byte size class, and no archive entry outside the contents specification.
  - Output: Assertions that fail the build.
- F9.1-06 — Produce the release manifest
  - Description: Generate a manifest binding the release to the checksums it expects — the patch tables, the sensor blobs, the tile application, and the archive itself. This closes the gap Autopsy section 9 names.
  - Output: A release manifest.
- F9.1-07 — Verify by building twice
  - Description: Build twice from an unchanged tree and compare against the chosen determinism standard.
  - Output: A reproducibility verification.
- F9.1-08 — Verify the assertions actually fail
  - Description: Deliberately introduce each forbidden condition and confirm the build fails. An assertion that has never failed is an assertion that has never been tested.
  - Output: Three negative-test results.
- F9.1-09 — Update the architectural record
  - Description: Update `ARC-08` from `absent` and record the resolution of `AUTOPSY-P3-03`.
  - Output: Updated continuity artifacts.

## 8. Acceptance Criteria

- The contents specification names every included path and gives a rationale for every exclusion.
- The tile application decision is recorded with its key-handling consequence.
- The determinism standard is defined, so "matches" has a meaning.
- The script produces an installable archive from the tree.
- The packaged `mode` file carries the intended install default rather than the working tree's value.
- Two builds from an unchanged tree satisfy the determinism standard.
- All three packaging assertions fail the build when their condition is deliberately introduced.
- The release manifest binds the release to the checksums of the patch tables, the sensor blobs, the tile application, and the archive.
- No credential enters the archive, verified by the assertion rather than by inspection.
- `ARC-08` is updated from `absent` and `AUTOPSY-P3-03` is recorded as resolved.

## 9. Validation and Test Approach

Validation is host-side and includes negative testing, which is unusual for this project and appropriate here: the packaging assertions exist to prevent conditions that have never occurred, so the only way to know they work is to cause them.

- `VAL-BUILD2` (proposed) — two builds from an unchanged tree, compared against the determinism standard.
- `VAL-ASSERT` (proposed) — three negative tests, one per assertion, each confirming the build fails. This is the sub-phase's most valuable check.
- `VAL-CONTENTS` (proposed) — the produced archive's entry list compared against the contents specification, confirming no unintended entry and no missing one.
- `VAL-MANIFEST` (proposed) — the manifest's checksums recomputed against the archive's contents.
- `VAL-INSTALL` (proposed) — the produced archive installs on device and the module reports correctly, confirming the script produces something that works rather than something that merely assembles.

Local versus live: the build and its assertions are host-side; the install check is live. Security validation is central — the keystore assertion is the enforcement of Faz 1.2's finding. Artifact validation is the sub-phase's subject.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| scripts/build-release.sh | proposed | The build script this sub-phase produces. | VAL-BUILD2, VAL-ASSERT, VAL-CONTENTS |
| ishtar-cam-modes/customize.sh | existing | Read-only evidence that install does not normalize the packaged mode value. | VAL-CONTENTS |
| ishtar-cam-modes/tile-app/build.sh | existing | The tile application build path, relevant to the F9.1-02 decision. | VAL-CONTENTS |
| docs/release-manifest.md | proposed | The manifest binding a release to its expected checksums. | VAL-MANIFEST |
| Planner-docs/Project-Comprehension.md | modified | Update `ARC-08` from absent. | VAL-BUILD2 |

## 10. Dependencies and Sequencing

Depends on Faz 1.2 for the packaging assertion specification, on Faz 1.5 for the install-state finding, and on Faz 1.3 for the patch table format the manifest records checksums against.

Depends on Phases 4 and 5 being settled, per Main-Planing section 9. A build script written while the release contents are still moving would be rewritten.

Depends on Faz 6.2's disposition if the AON module merged, since that changes what the archive contains.

Blocks Faz 9.2, which verifies a release the script produces.

Required decisions: the tile application handling and the determinism standard, both technical judgments the implementer records.

Required infrastructure: the host, and for the install check the device.

Required human approvals: the install check requires the user's device.

Fresh session token and context risk: low. Script work with short outputs.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the packaging assertions are implemented as warnings rather than failures. Impact: a release ships with a credential because a warning scrolled past. Mitigation: F9.1-05 specifies a hard gate and F9.1-08 proves each assertion fires.
- Risk (`AUTOPSY-P1-01` recurrence): the keystore assertion is written but never tested. Impact: an assertion with a defect provides false assurance, which is worse than no assertion. Mitigation: `VAL-ASSERT` requires the condition to be deliberately introduced.
- Risk (`AUTOPSY-P3-03` residual): the script packages the working tree's `mode` value. Impact: a user's first boot applies a mode they did not choose. Mitigation: F9.1-04 normalizes it, and the evidence that `customize.sh` does not is recorded in section 6 so the build script is understood as the only place this can be fixed.
- Risk: `active/` is packaged because it sits inside the module directory. Impact: a 1 MB duplicate in every release and ambiguity about which copy is authoritative. Mitigation: F9.1-01 requires a rationale per exclusion, which forces the question.
- Risk: determinism is assumed and two builds differ by timestamp. Impact: the acceptance signal "matches the shipped artifact" cannot be evaluated. Mitigation: F9.1-03 defines the standard before the script is written.
- Risk: the script builds an archive that assembles correctly and does not install. Impact: a reproducible release that does not work. Mitigation: `VAL-INSTALL` requires a real install rather than a structural check alone.
- Risk: the manifest is generated but its checksums are never recomputed. Impact: a manifest that describes an intended release rather than the produced one. Mitigation: `VAL-MANIFEST` recomputes against the archive's actual contents.

## 12. Desired End State

A build script produces the release archive from the tree, meeting a defined determinism standard, with the packaged install state normalized, with three packaging assertions that have each been proven to fail the build, and with a manifest binding the release to the checksums it expects. The archive installs and the module reports correctly. `ARC-08` is no longer `absent`.

The evidence an implementer should produce is the contents specification, the two-build comparison, the three negative-test results, the recomputed manifest, and the install verification.

The ledger summary Step 4 should append records: the contents specification, the two decisions taken, the determinism result, the three assertion tests, and the `ARC-08` update.

## 13. Next Sub-Phase Transition Criteria

- Two builds from an unchanged tree satisfy the determinism standard.
- All three assertions have been proven to fail the build.
- The produced archive installs and the module reports correctly.
- The packaged install state is normalized rather than inherited from the working tree.
- The manifest's checksums are recomputed against the produced archive.
- `ARC-08` is updated and Faz 9.2 has a script-produced release to verify.
