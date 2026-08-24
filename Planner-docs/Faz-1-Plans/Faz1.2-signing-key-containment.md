# Faz 1.2 — Signing Key Containment

## 1. Context

Main-Planing lists risk `R2` — "Signing keystore in the working tree", severity high — and its prioritized next step 6 says to exclude it from packaging and version control. Autopsy raises the same finding as `AUTOPSY-P1-01` and adds a dimension the main plan does not: exclusion going forward is only half the control, because nobody has checked whether the four already-released zips contain the key.

Project-Comprehension records the credential's existence as `EV-15`, confidence `confirmed`, gathered by path only with no file contents read. The open question `OQ-09` — "Does any released zip already contain `debug.keystore`?" — is still open, and `H-09` marks the probe as static, cheap, and closing a security question.

The reason confidentiality matters here is specific rather than generic. Project-Ontology section 5 records that reusing the same signer key allows later `install -r` without uninstalling the AGC port and without the data-preservation dance. That convenience is exactly what an attacker inherits: anyone holding this key can build an update the device accepts as the same application.

## 2. Goal

Establish that the signing credential is absent from version control, absent from every artifact that has already been distributed, and structurally prevented from entering a future one — with the third of those enforced by a check rather than by memory.

## 3. Description

The problem is a credential stored beside the artifacts it signs, in a tree that is about to gain history and is intended for eventual distribution. Faz 1.1 adds an ignore rule; this sub-phase proves the rule is sufficient and closes the historical question the ignore rule cannot answer.

It belongs in Phase 1 because it is cheap, because it must precede any push to a remote, and because the answer changes what the user must do. If the key is clean across all four zips, the remaining work is one ignore rule and one packaging assertion. If any zip contains it, the key must be rotated and the affected releases withdrawn or reissued — a materially different task that should be discovered now rather than after a remote exists.

The vibecoding slice strategy: the first useful slice is a name-only listing of the four release zips, which is a single read-only operation and immediately resolves `OQ-09`. The fastest validation signal is that listing. Only after it comes back does the packaging assertion get designed, because a clean result and a dirty result imply different assertions.

What not to over-plan: key rotation mechanics and release-withdrawal procedure. Those are only written if the audit comes back dirty. Designing them speculatively would be planning for a state that evidence has not established.

## 4. Scope

- A name-only inspection of the four `ishtar-cam-modes-v*.zip` files and `ishtar-aon-fix-v1.1.zip` for any `.keystore` entry.
- Resolution of `OQ-09` in Project-Ontology section 8 and of `H-09` in Project-Comprehension section 8, with the confidence column updated from `tentative`.
- Confirmation that the Faz 1.1 ignore rule actually excludes `ishtar-cam-modes/tile-app/debug.keystore` from the tracked set.
- A packaging assertion specification: the rule that any future release artifact must contain no `.keystore` entry and no file of the HAL binary's size class.
- A written statement of where the signing key should live instead, expressed as a location policy rather than as a concrete path containing credentials.
- If and only if the audit comes back dirty: a recorded finding naming the affected zips, escalated for the user's decision on rotation.

## 5. Out of Scope

- Reading, printing, copying, or moving the keystore's contents. All inspection is by path and by archive entry name.
- Implementing key rotation or re-signing the tile application. That is conditional work, triggered only by a dirty audit result.
- Building the packaging script that will enforce the assertion — that script is Phase 9. This sub-phase specifies the rule; Faz 9.1 implements it.
- Auditing the AGC port's own signing posture, which is a redistribution question rather than a credential-custody one.
- Any change to `ishtar-cam-modes/tile-app/build.sh` behavior beyond recording where it expects the key.

## 6. Current Repository Evidence

`ishtar-cam-modes/tile-app/` contains exactly three tracked-relevant files: `AndroidManifest.xml`, `build.sh`, and `debug.keystore`. The keystore's presence is confirmed by directory listing; its contents have not been read in this run or in Step 1.5.

Five release archives sit at the workspace root: `ishtar-cam-modes-v1.0.zip`, `ishtar-cam-modes-v1.9.zip`, `ishtar-cam-modes-v2.0.zip`, `ishtar-cam-modes-v2.1.zip`, and `ishtar-aon-fix-v1.1.zip`. None has been inspected for entry names.

`ishtar-cam-modes/customize.sh` was read in this run and calls `set_perm_recursive "$MODPATH" 0 0 0755 0644` — it applies permissions to everything the archive contains, without enumerating or filtering entries. This means the install path offers no protection against an unwanted file being present; the only control point is what goes into the archive.

`ishtar-cam-modes/tile-app.apk` is a built artifact inside the module directory, signed with that key. Its presence confirms the build-and-sign step happens in-tree.

Autopsy section 9 states that no other secret-like material was found anywhere in the inspected surface, that `.claude/settings.local.json` holds only permission keys, and that the project makes no network requests. The finding is genuinely singular.

## 7. Planned Work Breakdown

- F1.2-01 — Audit the five release archives by entry name
  - Description: List entry names in each archive and search for `.keystore`. Output must be name-only; no entry is extracted and no content is printed.
  - Output: A per-archive clean or dirty verdict, resolving `OQ-09`.
- F1.2-02 — Record the result in the continuity artifacts
  - Description: Update `OQ-09` status in `Planner-docs/Project-Ontology.md` and the `H-09` confidence in `Planner-docs/Project-Comprehension.md` in the same session the probe resolves, per the recording rule in Project-Comprehension section 8.
  - Output: Two updated rows with evidence cited.
- F1.2-03 — Verify the ignore rule against the tracked set
  - Description: Confirm the Faz 1.1 rule actually excludes the keystore by checking the tracked-file list by name, rather than inferring it from the rule text.
  - Output: A negative match recorded as evidence.
- F1.2-04 — Specify the packaging assertion
  - Description: Write the rule Phase 9's build script must enforce: zero `.keystore` entries, zero entries at or near the 27,268,688-byte HAL size, and zero `.apk` entries other than the intended `tile-app.apk`.
  - Output: An assertion specification consumed by Faz 9.1.
- F1.2-05 — State the key location policy
  - Description: Record that the signing key belongs outside the repository and outside the packaged module directory, and that `build.sh` should reference it by an external path. Express this as a policy; do not write any concrete credential location into a planning file.
  - Output: A short policy statement.
- F1.2-06 — Conditional escalation on a dirty result
  - Description: If any archive contains the keystore, record the affected versions and raise the rotation question to the user as a decision, not as an automatic action.
  - Output: An open decision entry, created only if F1.2-01 finds a match.

## 8. Acceptance Criteria

- Every one of the five release archives has a recorded clean or dirty verdict, obtained by entry name only.
- `OQ-09` in Project-Ontology section 8 no longer reads `open`, and its Evidence cell names the audit.
- `H-09` in Project-Comprehension section 8 is no longer `tentative`.
- The tracked-file list contains no path ending in `.keystore`, verified by an explicit name-only check rather than assumed.
- The packaging assertion specification names all three conditions and is written in a form Faz 9.1 can implement directly.
- No keystore content appears anywhere in `Planner-docs/` or in any commit message.
- If the audit is dirty, an open decision exists naming the affected release versions; if clean, that is stated explicitly rather than left silent.

## 9. Validation and Test Approach

This sub-phase is dominated by security validation. There is no device interaction and no local smoke surface.

- `VAL-SEC` (proposed) — archive entry listing across the five zips, filtered by name for `.keystore`; plus a name-only check of the tracked-file list. Output is file and entry names only. No matched content is ever printed, per the secret-scan discipline in the ClaudeQB workflow-quality notes.
- `VAL-DOCS` (proposed) — read back the updated `OQ-09` and `H-09` rows and the packaging assertion specification; confirm each states evidence rather than intent.

Live readiness is not applicable. Artifact validation is specified here but executed in Phase 9, and that separation is deliberate: the rule is decided while the evidence is fresh, and enforced where the artifact is produced.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/tile-app/debug.keystore | existing | The credential under containment; referenced by path only, never read. | VAL-SEC |
| ishtar-cam-modes/tile-app/build.sh | existing | Read-only context: shows how the key is consumed at build time. | VAL-SEC, VAL-DOCS |
| .gitignore | modified | Confirm and, if needed, tighten the keystore exclusion added in Faz 1.1. | VAL-SEC |
| Planner-docs/Project-Ontology.md | modified | Record the resolved `OQ-09` status with its evidence. | VAL-DOCS |
| Planner-docs/Project-Comprehension.md | modified | Update the `H-09` confidence in the session the probe resolves. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 1.1 for the ignore rule that F1.2-03 verifies. The archive audit itself has no dependency and could run first if convenient — the two orderings differ only in which check is available at the time.

Required decisions: none to start. A dirty audit result creates one, and it belongs to the user because rotation affects already-distributed artifacts.

Required credentials or infrastructure: none. Reading archive entry names requires no key material.

Required human approvals: rotation and release withdrawal, if triggered. The audit itself is read-only and needs no approval.

This sub-phase gates the remote decision opened in Faz 1.1. A remote must not be added before the audit result is known, because publishing history with an unresolved credential question is the exact failure mode `R2` describes.

Fresh session token and context risk: low. A handful of read-only commands with short output. Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: an audit command prints archive contents rather than entry names. Impact: credential material enters the transcript and possibly a planning file. Mitigation: the validation approach mandates name-only output, and the acceptance criteria explicitly forbid keystore content in `Planner-docs/`.
- Risk (`AUTOPSY-P1-01`): the audit finds the key in one or more shipped zips. Impact: the credential is already public to anyone who downloaded a release; exclusion alone does not remediate it. Mitigation: F1.2-06 escalates as a user decision with the affected versions named, rather than proceeding as if exclusion were sufficient.
- Risk: the ignore rule is verified against the rule text rather than the tracked set, and a differently-cased or differently-placed copy slips through. Impact: false confidence. Mitigation: F1.2-03 checks the actual tracked-file list by name.
- Risk: the packaging assertion is written but never implemented, because Phase 9 is distant and the finding feels closed. Impact: a future release reintroduces the problem. Mitigation: the specification is an explicit input to Faz 9.1, and Faz 9.1's acceptance criteria reference it by name.
- Risk: treating this as purely hypothetical because the key is a debug key. Impact: the control is skipped. Mitigation: the context section records the concrete consequence — same-signer `install -r` — so the stake is stated rather than assumed.

## 12. Desired End State

The signing credential's exposure is fully characterized: known absent from version control by check, known present or absent in each shipped archive by audit, and prevented from future inclusion by a written assertion that Phase 9 will enforce.

The evidence an implementer should produce is the five per-archive verdicts, the negative name-only check against the tracked set, and the two updated continuity rows.

The ledger summary Step 4 should append records: which archives were audited, the verdict for each, whether an open decision was created, and confirmation that no credential content was read or written.

## 13. Next Sub-Phase Transition Criteria

- All five archives have a recorded verdict and `OQ-09` is closed.
- The tracked set is confirmed free of `.keystore` paths by explicit check.
- The packaging assertion specification exists and is referenced from Faz 9.1.
- If the audit came back dirty, the rotation decision is with the user and the remote question from Faz 1.1 remains blocked until it is answered.
- No credential content has entered any planning file, commit message, or transcript.
