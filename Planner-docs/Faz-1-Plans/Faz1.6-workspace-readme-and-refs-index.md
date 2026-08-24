# Faz 1.6 — Workspace README and Reference Tree Index

## 1. Context

Main-Planing Phase 1 asks for "a root `README.md` explaining each top-level directory" and lists it as prioritized next step 8, noting that "Twelve top-level directories currently have no explanation outside the journal."

Autopsy files the same gap as `AUTOPSY-P3-02` and adds a second dimension the main plan mentions only in passing: `refs/` holds five reference trees "with no README explaining which is authoritative for what. `a16_ishtar` and `a16_sm8550` are the Android 16 inputs; `los_*` and `neo_*` are comparison sources — but this is inferable only from naming."

Autopsy section 3 raises a third, sharper version of the problem under Area 7: three roughly 150 MB APKs, an Open Camera build, a sensor binary, two configuration files, and five release archives "sit unsorted at the root with no manifest describing which is current. `AGC8.4.300_V9.6_50MP_patched.apk` is the currently installed build; that fact lives only in the journal and in session memory."

That last sentence is the reason this sub-phase is not merely tidy-up. Faz 1.1 excludes those binaries from version control. Once excluded, the only record of what they are and which one matters is a document — and right now that document does not exist.

## 2. Goal

Give every top-level path in the workspace a written explanation of what it is, whether it is a deliverable, a reference, or an input, and — for the artifacts version control does not carry — which one is current and how it is identified.

## 3. Description

The problem is orientation. A reader arriving at this workspace sees 26 root entries with no signal about which three matter, which five are read-only references, which are build inputs for a phase that has not started, and which large binaries are current versus superseded.

It belongs in Phase 1 for a specific reason rather than a general one: Faz 1.1 removes the large artifacts from version control, and exclusion without explanation is indistinguishable from absence. The README is what makes the exclusion legible. It also directly serves `R10` and Autopsy's context-loss theme — a future session that reads one page instead of a 1,300-line journal spends its budget on the actual work.

The vibecoding slice strategy: the first useful slice is the root README with one line per top-level entry, because that alone resolves the majority of the orientation problem. The `refs/` index and the artifact manifest are the second and third slices and are separable. The fastest validation signal is a completeness check — every entry in the root listing appears in the README, and every README entry exists on disk.

What not to over-plan: architecture documentation, per-module READMEs, or restructuring the tree. Autopsy section 3 identifies several boundary issues, such as the experimental HAL table living in an application-layer directory, but relocating anything is Faz 4.3's decision under the convention Faz 1.3 writes. This sub-phase describes the tree as it is, including its irregularities.

## 4. Scope

- A root `README.md` with one entry per top-level path, each labelled by role: deliverable, reference, build input, external artifact, or tooling.
- Explicit identification of the three deliverable directories, so the reader knows where the actual work lives.
- An index for `refs/` naming each of the five trees and stating what it is authoritative for.
- An artifact manifest for the root-level binaries: which AGC build is currently installed, which release archive is the most recent, and how each is identified by checksum.
- The untracked-by-design rationale produced by F1.1-05, folded in here rather than kept as a separate note.
- A pointer to the four `Planner-docs/` continuity artifacts, stating which one a fresh session should read first.
- A statement of the bilingual convention: user-facing documents and module interface in Turkish and English, planner artifacts in English, as Main-Planing risk `R11` records.

## 5. Out of Scope

- Moving, renaming, or deleting any file or directory. Description only.
- Per-module or per-directory README files.
- Rewriting, indexing, or restructuring `50MP-Entegrasyon-Plani.md`. Marking its superseded sections is a separate documentation action in Phase 9.
- Architecture or design documentation. Main-Planing section 5 and Project-Ontology already carry that.
- Resolving the boundary irregularities Autopsy section 3 identifies. They are described here and acted on in Faz 4.3 and Faz 9.3.
- Any change to `module.prop`, including the changelog duplication, which is Faz 9.3.

## 6. Current Repository Evidence

The root listing contains 26 entries, confirmed in this run: `12mpx_agc_config.agc`, `13U-989-DCG16+LN2+LN4/`, `50MP-Entegrasyon-Plani.md`, `50mpx_agc_config.agc`, `AGC8.4.300_V14_snap.apk`, `AGC8.4.300_V9.6_50MP_patched.apk`, `AGC8.4.300_V9.6_snap.apk`, `Module_Highres_13U_Switcher_A14/`, `OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk`, `Planner-docs/`, `agc-50mp-yama/`, `android_kernel_qcom_sm8550/`, `android_kernel_xiaomi_sm8550/`, `com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, `common_clone.log`, `common_sm8550/`, `device_ishtar/`, `ishtar-aon-fix/`, `ishtar-aon-fix-v1.1.zip`, `ishtar-cam-modes/`, four `ishtar-cam-modes-v*.zip` archives, `kernel_clone.log`, `platform-tools/`, and `refs/`.

No `README.md` exists at the workspace root.

`device_ishtar/README.md` exists and was catalogued in Step 1.5, so the device tree is the one top-level path that already carries an explanation.

The two `.agc` configuration files were inspected by key name in this run. Both `12mpx_agc_config.agc` and `50mpx_agc_config.agc` contain `pref_raw_key`, `pref_raw_key_0` through `pref_raw_key_4`, `pref_fix_resolution_key`, and `pref_fix_resolution_key_0` through `pref_fix_resolution_key_4`. These are the exact keys Project-Ontology invariant 8 identifies as the preference trap. The manifest entry for these two files must carry that warning, because a reader who imports either configuration re-arms a trap that has already caused one misattributed failure.

`refs/` holds five trees named `a16_ishtar`, `a16_sm8550`, `los_ishtar`, `los_sm8550`, and `neo_ishtar`, per Main-Planing section 3. No index file explains them.

Project-Ontology section 2 already contains a domain vocabulary table that the README should reference rather than duplicate, and Project-Comprehension is the artifact a fresh session should read for evidence and confidence.

## 7. Planned Work Breakdown

- F1.6-01 — Write the root README skeleton with role labels
  - Description: One entry per top-level path, each carrying a role label. The three deliverable directories are grouped first so the reader's attention lands on them.
  - Output: `README.md` at the workspace root.
- F1.6-02 — Write the `refs/` index
  - Description: Name each of the five trees, state which target it serves, and state whether it is a build input for Phase 7 or a comparison source. Where authority is inferred from naming rather than verified, say so.
  - Output: A reference-tree section in the README or a `refs/README.md`, depending on the convention the implementer chooses; the choice is recorded either way.
- F1.6-03 — Build the root artifact manifest
  - Description: For each root-level APK, archive, and binary: what it is, its checksum, and whether it is current or superseded. Name `AGC8.4.300_V9.6_50MP_patched.apk` as the currently installed build, since that fact currently lives only in the journal and in session memory.
  - Output: An artifact manifest section with checksums.
- F1.6-04 — Add the preference-trap warning to the configuration entries
  - Description: Record that both `.agc` files contain the `pref_raw_key` and `pref_fix_resolution_key` families, and that importing either re-arms the trap described in Project-Ontology invariant 8.
  - Output: A warning attached to both configuration file entries.
- F1.6-05 — Fold in the untracked-by-design rationale
  - Description: Absorb the F1.1-05 exclusion note so there is one place, not two, that explains why the large paths are absent from version control.
  - Output: An exclusions section in the README.
- F1.6-06 — Add the reading order for a fresh session
  - Description: State that a session with no context should read `Planner-docs/Project-Ontology.md` first for durable facts, `Planner-docs/Project-Comprehension.md` for evidence and confidence, and the journal for narrative history.
  - Output: A short orientation section.
- F1.6-07 — State the language convention
  - Description: Record that user-facing documents and the module interface are Turkish and English, that planner artifacts are English, and that this is deliberate rather than drift.
  - Output: A convention note referencing Main-Planing risk `R11`.

## 8. Acceptance Criteria

- Every one of the 26 root entries appears in the README with a role label, and every README entry exists on disk.
- The three deliverable directories are distinguishable from references and inputs without reading the journal.
- All five `refs/` trees are named with their purpose stated, and any purpose inferred from naming rather than verified is marked as inferred.
- The artifact manifest identifies the currently installed AGC build by name and checksum.
- Both `.agc` configuration entries carry the preference-trap warning.
- The exclusions section explains every path Faz 1.1 chose not to track.
- The orientation section names the reading order for a fresh session.
- The README contains no checksum or path that reveals credential material, and no download location implying redistribution of the AGC port.

## 9. Validation and Test Approach

Validation is document-level and completeness-driven. There is no device or build involvement.

- `VAL-DOCS` (proposed) — a two-way completeness check: every root listing entry appears in the README, and every README entry resolves on disk. A one-way check would miss stale entries.
- `VAL-MANIFEST` (proposed) — recompute the checksum of each artifact named in the manifest and confirm it matches the recorded value. This is what makes the manifest a fact rather than a claim.
- `VAL-SEC` (proposed) — confirm no credential path and no redistribution-implying location appears in the document.

Local smoke, live readiness, CI, and artifact packaging validation are not applicable here. Ontology consistency applies: the README must reference the Project-Ontology vocabulary rather than inventing parallel terms, and must keep `fullres` and `50mp` distinct as that document requires.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| README.md | proposed | Root orientation document produced by this sub-phase. | VAL-DOCS, VAL-MANIFEST, VAL-SEC |
| refs | existing | Five reference trees requiring an authority index. | VAL-DOCS |
| 50mpx_agc_config.agc | existing | Configuration artifact carrying the preference-trap key families. | VAL-DOCS |
| 12mpx_agc_config.agc | existing | Second configuration artifact with the same key families. | VAL-DOCS |
| device_ishtar/README.md | existing | Pre-existing directory documentation the root README should point to rather than duplicate. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 1.1 for the exclusion decisions that F1.6-05 folds in, and benefits from Faz 1.2's audit result, since the artifact manifest should not describe an archive whose contents are under an unresolved security question without saying so.

Runs last within Phase 1 by preference rather than by necessity, because it absorbs outputs from the other sub-phases. If it runs earlier, the exclusions and manifest sections are written twice.

Feeds every later phase weakly and Phase 7 specifically, since the `refs/` index is what tells a build attempt which tree to use.

Required decisions: whether the reference index lives in the root README or in `refs/README.md`. The implementer may choose; the choice is recorded.

Required credentials, infrastructure, live endpoints, or approvals: none.

Fresh session token and context risk: low. A directory listing, a handful of checksums, and one document. Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the README describes an idealized tree rather than the actual one, omitting the irregularities Autopsy section 3 identifies. Impact: a reader trusts it and is surprised by the experimental HAL table sitting in an application-layer directory. Mitigation: the scope requires describing the tree as it is, including irregularities, with relocation deferred to Faz 4.3.
- Risk: the artifact manifest records checksums that are never recomputed. Impact: a superseded APK is mistaken for the current one. Mitigation: `VAL-MANIFEST` recomputes rather than transcribes.
- Risk: the manifest goes stale the first time a new APK or archive appears. Impact: the document becomes another source of misleading information, which is exactly the failure `AUTOPSY-P2-03` describes elsewhere in the project. Mitigation: the manifest section states its measurement date, consistent with how the project records device measurements, so staleness is visible rather than silent.
- Risk: the preference-trap warning is written as a general caution rather than naming the keys. Impact: a reader does not connect the warning to the file they are about to import. Mitigation: F1.6-04 requires the key families to be named.
- Risk (`R11`): the language convention is stated but the README itself mixes languages inconsistently. Impact: minor friction, and a bad example for later documents. Mitigation: the convention is stated and the document follows it.
- Risk: writing a root README is treated as low-value cleanup and deferred past Phase 1. Impact: Faz 1.1's exclusions remain unexplained, which is the concrete cost. Mitigation: the context section ties the README directly to the exclusion decision rather than to general tidiness.

## 12. Desired End State

The workspace root carries a README that a reader can use to orient in one pass: which three directories are the deliverable, which five reference trees serve which target, which large artifacts exist and which is current, why the large paths are absent from version control, what to read first with no context, and what the language convention is.

The evidence an implementer should produce is the two-way completeness check result and the recomputed checksums for every manifest entry.

The ledger summary Step 4 should append records: the README path, whether the reference index went into the root document or into `refs/`, the number of artifacts in the manifest, and the measurement date the manifest carries.

## 13. Next Sub-Phase Transition Criteria

- The two-way completeness check passes in both directions.
- Every manifest checksum has been recomputed rather than transcribed.
- The currently installed AGC build is named in a durable document rather than only in session memory.
- Both configuration files carry the preference-trap warning before Phase 3 begins.
- Phase 1 is complete: version control exists, the credential question is resolved, the patch format and toolchain are documented, the static probes are answered, and the tree is explained.
