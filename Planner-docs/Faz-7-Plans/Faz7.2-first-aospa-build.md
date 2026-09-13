# Faz 7.2 — First AOSPA beryl Build on a Rented VDS

## 1. Context

Main-Planing Phase 7 (`SNAP-2026-09-10-MAIN`) sets the desired end state: "One AOSPA `beryl` build for `ishtar` completed on a rented VDS from inputs staged on GitHub, with the output retrieved and the server released." Its acceptance signal reads "A flashable build output exists and boots; the rental time the build consumed is recorded." This sub-phase is the paid half of that. It rents, builds, retrieves, and releases. The boot half belongs to `Faz7.3`, because flashing is the user's action on a daily device and happens after the server is gone.

**Re-planned 2026-09-10 by planning run 18.** The previous version of this file planned a sync "inside the Linux filesystem" of a WSL2 host that `DEC-24` retired, and it excluded "any beryl work" while its own goal was an Android 16 build from the `beryl` trees — the contradiction ledger section 7 recorded. Both premises are gone. The path is unchanged so that existing references still resolve: `docs/aon-verification.md` section 7 and `Faz6.2`'s `F6.2-05` both name this file.

Two registrations converge here. `Faz6.2` registered the AON verification against Phase 7. Its procedure's step 1 — "confirm the entry is in the tree the build actually consumed" — can only run where the consumed tree exists, which is the server, so it is executed here before teardown. The device-side steps run in `Faz7.3`. That discharges `FIND-6.2-01`'s cross-reference: `F6.2-05` asked that the procedure be "referenced from `Faz7.2`", and a Step 4 session could not add the reference itself. `Faz8.1` likewise needs the md5 of the guarded camera blobs as actually built, which only this session can read cheaply.

Ledger section 7 lists this sub-phase's outcome as a replanning trigger: a result showing "the Android 16 track is not viable … removes the precondition" for Phase 8.

## 2. Goal

In one bounded paid session, turn the inputs `Faz7.1` staged into a retrieved, checksummed, flashable `ishtar` build. Capture before teardown the evidence `Faz7.3` and `Faz8.1` need, and finish with the server deleted, the server's credential revoked, and the rental time and cost recorded against the agreed budget.

## 3. Description

The problem is that the Android 16 track has never produced an artifact. The trees are staged and pinned, but nothing has compiled from them, and every day the project owns a pinned manifest without a build is a day the pins can only be trusted on paper.

It belongs after `Faz7.1` because the manifest is not buildable until that sub-phase closes its open items, and because the budget, stopping rule, server image and runbook are all `Faz7.1` outputs. It belongs before `Faz7.3` because a flash needs an output.

The vibecoding slice strategy follows the runbook's own order, cheapest failure surface first: provision and authenticate, then `repo init` and `repo sync`, then the AON tree check, then the build. The fastest useful signal is a completed sync whose `repo manifest -r` matches the pins. That alone proves the staging was sound, and it is the part `DEC-24` was designed to make boring.

What should not be over-planned: build errors and their remedies. A first build of a device tree nobody on this project has built produces errors that cannot be predicted. The stopping rule `Faz7.1` recorded bounds them. One rule about remedies is fixed in advance: **a fix that changes an input lands on GitHub first** — the device-tree fork or the manifest repository, re-checked with `check.py` — and the server pulls it. A fix edited only on the server dies with the server and makes the output unreproducible.

The session ends by teardown whatever the outcome. A failed build still retrieves its logs, still deletes the server, and still records time and cost. A server left running because the build "nearly worked" is the cost failure this whole phase is shaped to prevent.

## 4. Scope

- A pre-rental gate: `Faz7.1`'s transition criteria re-read, `check.py` re-run the same day, and the budget and stopping-rule decision in force.
- Renting and provisioning a server per `DEC-22` and the runbook; recording server type, region, image and start time (never its address or any credential).
- Server authentication per `Faz7.1`'s credential plan.
- `repo init` at the recorded `AOSPA/manifest` base, the local manifest cloned, `repo sync` per the shallow-sync specification with its fallback.
- `repo manifest -r` retrieved as the reproducibility record.
- AON procedure step 1 (`docs/aon-verification.md` section 5) against the consumed device tree.
- Build attempts within the stopping rule, with error classes and progress recorded; input fixes landed on GitHub first.
- Post-build evidence read from the build output: md5 and size of `camera.qcom.so`, the IMX989 `sensormodule` `.bin` and `camera.xiaomi.so`, and whether `aon_front.pb` exists as a symlink in the built vendor staging directory.
- Output retrieval to the user's machine with sha256 verified at both ends, stored outside tracked paths.
- Teardown: server deleted, credential revoked, billing confirmed stopped, rental time and cost recorded.
- A Phase 8 readiness statement and a check against ledger section 7's viability trigger.

## 5. Out of Scope

- Flashing, booting or any device action. `Faz7.3`.
- Installing `ishtar-cam-modes` or any module on the new build. `Faz8.3`.
- Any kernel merge. `Faz8.2` scopes it; nothing is merged here.
- Signing with anything other than AOSPA's default build signing; no project key goes to the server.
- Publishing the build output anywhere public. The output embeds proprietary vendor blobs, and `ARC-04` records that the project never redistributes them.
- `calcite`, or any second build variant.
- Fixes beyond the stopping rule. Reaching the rule is a recorded, bounded outcome, not a reason to extend the rental.
- Adopting the build as a daily base. `Faz7.3` assesses that with the camera consequence stated.
- Uploading workspace content to the server beyond what the runbook names. `snapshots/` holds full-resolution captures, and none of it is needed for a build.

## 6. Current Repository Evidence

The inputs are staged but not yet buildable: `ahmetxa/android_local_manifests` `4182695` pins four projects, and its `README.md` lists seven open items that `Faz7.1` closes. Its "Use" section names AOSPA's documented commands — `repo init -u https://github.com/AOSPA/manifest -b beryl`, the local manifest cloned into `.repo/local_manifests`, `repo sync --current-branch --no-tags`, and `./rom-build.sh ishtar`. It also notes that the device-tree repository is private, so the server needs authenticated GitHub access unless `Faz7.1`'s credential plan changes that.

The consumed device tree will be `ahmetxa/android_device_xiaomi_ishtar` `d48816f`, which is upstream `df05661` plus one line. The local mirror of that upstream is `refs/a16_ishtar`, on `beryl` at `df056613…`, where the `;SYMLINK=` entry count reads 1 (measured this run). `docs/aon-verification.md` section 5 step 1 prescribes `grep -n 'aon_front.pb;SYMLINK=' <build-tree>/proprietary-files.txt` and calls exactly one match conclusive.

The guarded blobs: `ishtar-cam-modes/halpatch.sh:32-34` records `HAL_STOCK_MD5=c3fa63a86ee3ecaf9fbf02005d35f6b5`, `HAL_FULLRES_MD5=fe0245a4720fb07b01d96deef47f5569`, `HAL_SIZE=27268688`. `ishtar-cam-modes/customize.sh:14` records the sensor blob `EXPECT_MD5=9e4d0fe1a8bf2eb4146c9917a0ac2c4c`. `ishtar-cam-modes/blobs/hal-fullres.patch` carries the header "A15 / vauxite". The pinned vendor repository at `f92e7a9` carries `proprietary/odm/lib64/hw/camera.qcom.so`, `camera.xiaomi.so`, `proprietary/odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin` and `aon_front.pb` (names only, read this run; no `.gitattributes` at the root, so the blobs are ordinary git objects). `refs/a16_ishtar/extract-files.py` fixes up `camera.xiaomi.so` (`add_needed('libprocessgroup_shim.so')`, `replace_needed('libui.so', 'libui-v34.so')`, commit `05efdac`, "fixes camera service crash") and several other camera libraries; no fixup names `camera.qcom.so` or the sensor module in either `beryl` tree (grep this run).

`.gitignore` ignores `*.zip` and `/refs/` but has no rule for `*.img`, so image files retrieved into the workspace would be commit candidates.

`IMPL-90`'s disclosed defect — a pipe masking a failed `git am`, followed by an ungated push — is the precedent for this session's fail-on-error rule.

Project-Ontology invariant 10: "Every offset is bound to one exact vendor build … the md5 guard is the detector." That invariant is why the post-build md5 read is in scope here rather than deferred to the device.

## 7. Planned Work Breakdown

- F7.2-01 — Pass the pre-rental gate
  - Description: Re-read `Faz7.1`'s transition criteria, re-run `check.py` on the day, and confirm the budget and stopping-rule decision id. Any failure stops the sub-phase before renting.
  - Output: A gate record naming the decision id and the `check.py` result.
- F7.2-02 — Rent and provision
  - Description: Rent per `DEC-22` and the sizing floor; provision by the runbook with fail-on-error scripting. Record server type, region, image and start time.
  - Output: A provisioned server and a start record without addresses or credentials.
- F7.2-03 — Authenticate with least privilege
  - Description: Apply `Faz7.1`'s credential plan: read access only, to the named repositories only.
  - Output: A confirmation that the private repositories resolve from the server, with the credential referred to by role.
- F7.2-04 — Initialise and sync
  - Description: `repo init` at the recorded base, local manifest in place, sync per the shallow-sync specification. On a shallow-sync failure, apply the written fallback and record the disk it cost. Retrieve `repo manifest -r` and compare the four staged projects against their pins.
  - Output: A completed sync, the revision manifest, and a shallow-sync verdict for `README.md` item 7.
- F7.2-05 — Run AON procedure step 1 on the consumed tree
  - Description: `grep -n 'aon_front.pb;SYMLINK=' device/xiaomi/ishtar/proprietary-files.txt` in the synced tree; expect exactly one match.
  - Output: The step 1 verdict, recorded against `docs/aon-verification.md` section 5.
- F7.2-06 — Build within the stopping rule
  - Description: Run the documented build. On failure, classify the error, and if the fix changes an input, land it on GitHub, re-run `check.py`, re-sync that project and retry — each retry counted against the stopping rule. Record how far each attempt progressed.
  - Output: A build outcome (complete, partial with stage reached, or stopped by rule) with error classes and elapsed time per attempt.
- F7.2-07 — Read the post-build evidence
  - Description: From the build output, record md5 and size of `odm/lib64/hw/camera.qcom.so`, `odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin` and `odm/lib64/hw/camera.xiaomi.so`. Record whether `vendor/lib64/camera/aon_front.pb` in the built vendor staging directory is a symlink and what it targets. Compare the first two md5s against `HAL_STOCK_MD5` and `EXPECT_MD5` as facts, not conclusions — `Faz8.1` classifies them.
  - Output: A post-build evidence block for `Faz8.1` and `Faz7.3`.
- F7.2-08 — Retrieve outputs
  - Description: Copy the flashable package, the revision manifest, the build log tail and the evidence block to the user's machine; verify sha256 at both ends. Store images and packages outside tracked paths; if any image must sit inside the workspace, add an ignore rule first.
  - Output: Retrieved outputs with matching sha256 values, stored untracked.
- F7.2-09 — Tear down
  - Description: Delete the server — not merely power it off, unless the provider's billing documentation, read in `Faz7.1`, says otherwise. Revoke the server's credential and confirm in the provider console that billing has stopped. Record end time, rental hours and cost against the budget.
  - Output: A teardown record: server deleted, credential revoked, time and cost.
- F7.2-10 — State what Phase 8 inherits
  - Description: Write the outcome as built, partial or blocked, check it against ledger section 7's viability trigger, and name what `Faz7.3`, `Faz8.1` and `Faz8.2` can now use.
  - Output: A Phase 8 readiness statement and, if the trigger fires, a replanning input.

## 8. Acceptance Criteria

- The gate record exists and predates the rental, with `check.py` passing on that day and a budget decision id.
- The sync completed, or its failure is characterised, and `repo manifest -r` shows the four staged projects at their pinned commits.
- The shallow-sync specification is marked tested with its result, or the fallback's use and disk cost are recorded.
- AON procedure step 1 returned exactly one match in the consumed tree, or the zero result is recorded as "the build never saw the fix".
- Every build attempt is recorded with its error class, stage reached and elapsed time. No input was changed on the server without the same change landing on GitHub first.
- If a build completed, the post-build evidence block records md5 and size for the three camera files and the `aon_front.pb` symlink state.
- Retrieved outputs verify by sha256 at both ends, and no image or package is tracked by git.
- The server is deleted, its credential revoked, billing confirmed stopped, and rental hours and cost are recorded against the budget — **whatever the build outcome**.
- The Phase 8 readiness statement exists, and ledger section 7's viability trigger is explicitly evaluated.
- No credential value, server address or password appears in any retrieved file, snapshot, runbook edit or ledger row.

## 9. Validation and Test Approach

Validation spans a paid remote session and host-side checks after it. No device is involved.

- `VAL-GATE` (proposed) — the pre-rental gate record, including `VAL-PINS` from `Faz7.1` re-run that day.
- `VAL-SYNC` (proposed) — sync exit status plus `repo manifest -r` compared against the four pins.
- `VAL-AON-TREE` (proposed) — `docs/aon-verification.md` section 5 step 1 on the consumed tree; one match.
- `VAL-COMPILE` (proposed) — the build outcome per attempt, with stage reached. Named apart from `VAL-BUILD`, which `Faz6.2` defined as the device-side AON verification and which `Faz7.3` executes.
- `VAL-BLOBMD5` (proposed) — md5 and size of the three camera files from the build output, and the symlink state of `aon_front.pb`.
- `VAL-RETRIEVE` (proposed) — sha256 of each retrieved file computed on the server and on the host, equal; `git status --short` shows no image or package.
- `VAL-TEARDOWN` (proposed) — provider console reads the server gone and billing stopped; the credential reads revoked in GitHub settings.
- `VAL-SEC` (proposed) — file-name-only scan of the evidence files, runbook changes and ledger row for token-shaped strings and addresses; never print a match.
- `VAL-DOCS` (proposed) — read back the runbook deviations section, the evidence block and the readiness statement.

Local versus live: sync and build are live on a rented machine; retrieval checks and document checks are local. Security validation covers credential scope and revocation and the non-publication of blob-bearing outputs. Ontology validation applies to invariant 10, whose detector — the md5 — is read here for the first time on an Android 16 blob.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| docs/build-environment.md | modified | Extended with the steps actually run, deviations from the runbook, and the shallow-sync verdict. | VAL-DOCS, VAL-SEC |
| docs/aon-verification.md | existing | Section 5 step 1 is executed here; results are recorded in the evidence file and appended by `Faz7.3`. | VAL-AON-TREE |
| refs/a16_ishtar/proprietary-files.txt | existing | Local mirror of the upstream tree; the consumed tree is the pinned fork on the server. | VAL-AON-TREE |
| ishtar-cam-modes/halpatch.sh | existing | Source of `HAL_STOCK_MD5` and `HAL_SIZE` read against the built `camera.qcom.so`. | VAL-BLOBMD5 |
| ishtar-cam-modes/customize.sh | existing | Source of the sensor blob `EXPECT_MD5`. | VAL-BLOBMD5 |
| snapshots | existing | Receives the gate record, revision manifest, post-build evidence block and teardown record as text. | VAL-SYNC, VAL-BLOBMD5, VAL-TEARDOWN |
| .gitignore | modified | Only if a retrieved image or package must be stored inside the workspace: add the ignore rule before copying. | VAL-RETRIEVE |
| Planner-docs/Planing-Ledger.md | modified | The implementation row, the Phase 8 readiness statement, and any section 7 trigger. | VAL-DOCS, VAL-SEC |

## 10. Dependencies and Sequencing

Depends on `Faz7.1` absolutely: a buildable manifest, `DEC-22`, the budget and stopping rule, the credential plan and the runbook. Depends on `Faz6.1` for the symlink entry that step 1 checks.

Blocks `Faz7.3` (no output, no flash) and the built-output halves of `Faz8.1`. `Faz8.2` may proceed without it, since its conflict estimate needs no build.

Required decisions: none new. All are `Faz7.1` outputs. Reaching the stopping rule is not a decision point — it ends the session.

Required credentials: the server credential from `Faz7.1`'s plan, created at rental and revoked at teardown, plus the user's provider account. Neither is recorded anywhere.

Required infrastructure: the rented server; network egress to GitHub and AOSPA sources; enough local disk on the user's machine for the retrieved package.

Required human approvals: renting (it spends money); every push that lands an input fix on GitHub; teardown confirmation in the provider console.

Fresh session token and context risk: medium, per Main-Planing's Phase 7 band, rising to high if the build fails repeatedly. The hazard is build and sync output volume. Mitigation: record exit status, stage, error class and the last lines of a failing log, never whole transcripts. Keep the session's own context for the stopping rule. Subagents: not recommended; the session is a single stateful remote resource.

## 11. Risks and Mitigations

- Risk: the build nearly works and the server stays up. Impact: cost overrun, the failure `DEC-24` was designed around. Mitigation: `Faz7.1`'s stopping rule is in force before renting, and teardown is an acceptance criterion independent of the outcome.
- Risk: an input is fixed on the server only. Impact: the output cannot be reproduced and the next rental repeats the discovery. Mitigation: the rule in section 3, enforced by F7.2-06 and an acceptance criterion.
- Risk: a masked exit code lets a failed step look successful (`IMPL-90`'s defect class). Impact: the session proceeds on a broken sync or build, and the evidence is wrong. Mitigation: fail-on-error scripting from the runbook, and `VAL-SYNC` compares revisions rather than trusting the exit status alone.
- Risk: the server credential outlives the server. Impact: a live token for private repositories with no machine attached to it. Mitigation: F7.2-09 revokes it, and `VAL-TEARDOWN` checks the revocation.
- Risk: a blob-bearing output is published, for example as a public release. Impact: proprietary blob redistribution, contrary to `ARC-04`. Mitigation: out of scope by rule; retrieval is private and verified by sha256.
- Risk: an image is committed by accident. Impact: repository bloat, and blobs in a remote. Mitigation: F7.2-08 stores outputs untracked, adds an ignore rule first if needed, and `VAL-RETRIEVE` reads `git status`.
- Risk: shallow sync fails partway through. Impact: wasted hours and possibly a disk-full on fallback. Mitigation: `Faz7.1`'s written fallback and its disk figure; the verdict closes `README.md` item 7 either way.
- Risk: the AON step 1 check is skipped because the build dominates attention. Impact: `Faz7.3`'s device result becomes uninterpretable, since a missing providers result could simply mean the tree lacked the entry. Mitigation: F7.2-05 runs before the build starts.
- Risk: the post-build md5 read is skipped. Impact: `Faz8.1` has only the vendor-repository value, and a fixup or build step that altered the file goes unseen. Mitigation: F7.2-07 is a distinct work item on the runbook's evidence list.

## 12. Desired End State

An AOSPA `beryl` build for `ishtar` has been attempted on a rented server from staged inputs, with a recorded outcome. If it completed, a flashable package sits on the user's machine with matching sha256 values. The revision manifest proves it came from the pinned inputs, the consumed tree carried the AON entry, and the md5 of the guarded camera blobs as built is known. Whatever the outcome, the server is deleted, its credential is revoked, and the rental time and cost are recorded against the budget. Phase 8 has a readiness statement, and ledger section 7's viability trigger has been evaluated.

Evidence the implementer produces: the gate record, the revision manifest, the AON step 1 verdict, per-attempt build records, the post-build evidence block, sha256 pairs, and the teardown record.

The ledger summary Step 4 appends: the budget decision id against rental hours and cost; sync and shallow-sync verdicts; the AON step 1 result; the build outcome and attempts used; the three blob md5s as facts; the retrieved package's sha256; teardown confirmation; and what Phase 8 inherits.

## 13. Next Sub-Phase Transition Criteria

- The server is deleted and its credential revoked. This holds even when the build failed.
- Rental time and cost are recorded against the agreed budget.
- For `Faz7.3`: a flashable package exists locally with verified sha256, and the AON step 1 result is recorded. Without both, `Faz7.3` does not start.
- For `Faz8.1`: the post-build md5s of `camera.qcom.so` and the sensor module are recorded, or their absence is explained.
- The Phase 8 readiness statement is written, and any section 7 trigger is raised in the ledger.
