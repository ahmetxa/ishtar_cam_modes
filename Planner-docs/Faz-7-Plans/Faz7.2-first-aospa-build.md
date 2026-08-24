# Faz 7.2 — First AOSPA Build Attempt

## 1. Context

Main-Planing Phase 7's desired end state is "A WSL2 environment that completes one AOSPA build for `ishtar`", with the acceptance signal "A flashable build output exists and boots."

Its first slice covers the environment and is Faz 7.1's subject; this sub-phase performs the build attempt that slice was a precondition for.

Two other pieces of the roadmap converge here. Faz 6.2 registered a verification against this sub-phase: the four AON provider capabilities should appear on a build that includes the symlink entry, with the runtime module absent. That verification cannot happen anywhere else. And Phase 8 depends entirely on this succeeding — Main-Planing states "Both are substantial and both depend on Phase 7."

Main-Planing section 9 marks this phase for lower-detail planning, and that instruction is respected here. The build process itself has too many unknowns to plan in fine detail before an environment exists, so this sub-plan sets the goal, the acceptance conditions, and the decisions that must be marked rather than guessed.

Autopsy section 11 supports the caution regarding what follows: "Phase 8 (beryl) has no beryl-specific evidence in the tree at all and should not be decomposed until Phase 7 produces a working build environment."

## 2. Goal

Complete one AOSPA Android 16 build for `ishtar` that produces a flashable output and boots on the device, and use that build to verify the device tree symlink fix registered by Faz 6.2.

## 3. Description

The problem is that the Android 16 track has no evidence at all. `refs/a16_ishtar/` and `refs/a16_sm8550/` exist as inputs and nothing has been built from them. Main-Planing records the phase's maturity as M0 and Autopsy confirms the track has not begun.

It belongs after the environment because a build cannot be attempted without one, and after the camera consolidation because Main-Planing's planning conclusion sequences the Android 16 front last among the active tracks.

The vibecoding slice strategy: sync, configure, build, and only then flash. Each step has a distinct failure surface and the failures are cheapest to diagnose in that order. The fastest useful validation signal is that the sync completes and the configuration step selects the device — that alone establishes that the device trees are usable inputs, which is a real finding for a track with no prior evidence.

What should not be over-planned: build errors and their remedies. A first build against unbuilt device trees produces errors that cannot be predicted, and planning remedies for imagined errors is wasted. What can be planned is the sequence, the acceptance conditions, and a stopping rule.

A stopping rule is warranted here for the same reason Faz 3.1 set one for Phase 3. A first ROM build is open-ended work with a long feedback loop, and Main-Planing bands Phase 7 as medium token risk while Phase 8 is high. Without a bound, a build that nearly works can absorb arbitrary effort.

Several decisions are genuinely open and are marked rather than resolved. Which AOSPA branch or tag corresponds to the Android 16 target. Whether `common_sm8550` or a fresh platform tree is the correct dependency. Whether the existing device trees need updating for the target version beyond the symlink entry Faz 6.1 added. Each of these is answerable only with the sources in hand.

## 4. Scope

- An AOSPA source sync for the Android 16 target inside the Linux filesystem.
- A build configuration step selecting `ishtar` as the target device.
- The device tree inputs sourced from `refs/a16_ishtar/` and `refs/a16_sm8550/`, including the symlink entry Faz 6.1 added.
- A build attempt producing a flashable output.
- A flash and boot verification, which is the user's action.
- The AON verification registered by Faz 6.2: the four provider capabilities present with the runtime module absent.
- A stopping rule agreed before the build begins.
- Recording of the branch, tree, and version decisions as they are settled.
- An assessment of whether the resulting build is suitable as a daily-use base or is a build-verification artifact only.

## 5. Out of Scope

- Any beryl work, which is Phase 8.
- Merging GKI LTS into the kernel, which is Phase 8.
- Porting the camera modules to the new build, which is a Phase 9 question if the build becomes a daily-use base.
- Fixing build errors beyond what the stopping rule permits.
- Any change to the camera HAL patches or sensor blobs, which are bound to a specific vendor build and would need re-derivation for a different one.
- Upstreaming any device tree change.
- Making the Android 16 build the primary environment. This sub-phase produces one build; adopting it is a separate decision.

## 6. Current Repository Evidence

`refs/a16_ishtar/` and `refs/a16_sm8550/` are present. Autopsy section 3 identifies them as the Android 16 inputs, with the caveat that the identification "is inferable only from naming" — a caveat Faz 1.6's reference index should have resolved before this sub-phase runs.

Faz 6.1 added the symlink entry to `refs/a16_ishtar/proprietary-files.txt`, changing a count that both prior ClaudeQB runs measured at zero. That entry is the specific thing this build verifies.

`device_ishtar/` is the current device tree, carrying `Android.bp`, `Android.mk`, `BoardConfig.mk`, `device.mk`, `proprietary-files.txt`, and a `README.md` per Autopsy section 2. It is the Android 15 tree and serves as a reference for what a working configuration looks like, not as the build input.

`common_sm8550/` is present and is both a kernel checkout and, per Main-Planing section 3, part of the device tree set. Which role it plays for the Android 16 build is one of the open decisions.

Main-Planing records the current build as AOSPA Android 15, and Project-Ontology section 2 identifies the device as `ishtar`, SM8550, released April 2023.

The camera work is entirely bound to the current build. `ishtar-cam-modes/halpatch.sh` records `HAL_STOCK_MD5=c3fa63a86ee3ecaf9fbf02005d35f6b5` for `camera.qcom.so` and `customize.sh` records `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` for the sensor driver. Project-Ontology invariant 10 records the consequence: "Every offset is bound to one exact vendor build. Any ROM update that changes `camera.qcom.so` invalidates all offsets at once; the md5 guard is the detector."

That invariant is why the daily-use assessment in the scope matters. An Android 16 build almost certainly carries different vendor blobs, which would invalidate every camera patch the project has produced. Flashing it as a daily driver would trade the working camera capability for an unbuilt one.

Project-Comprehension `CQ-13` — "What blocks the Android 16 track?" — is answered, and Faz 7.1 changes that answer by removing the blocker.

## 7. Planned Work Breakdown

- F7.2-01 — Agree the stopping rule
  - Description: Set a bound before the build begins, in whatever unit suits — sessions, build attempts, or elapsed effort. A first ROM build is open-ended and the bound is what keeps it from absorbing Phase 8's resources too.
  - Output: A recorded stopping rule.
- F7.2-02 — Settle the branch and tree decisions
  - Description: Determine the AOSPA branch for the Android 16 target, the platform tree dependency, and whether the device trees need changes beyond the symlink entry. Record each as it is settled.
  - Output: Three settled decisions with their reasoning.
- F7.2-03 — Sync the sources
  - Description: Perform the source sync inside the Linux filesystem. Record the space consumed against the Faz 7.1 assessment.
  - Output: A completed sync with a space figure.
- F7.2-04 — Configure the build for the device
  - Description: Run the configuration step selecting `ishtar`. A successful selection establishes that the device trees are usable inputs, which is a meaningful result for a track with no prior evidence.
  - Output: A configuration verdict.
- F7.2-05 — Attempt the build
  - Description: Build, within the stopping rule. Record errors encountered and how far the build progressed, since partial progress is informative for a first attempt.
  - Output: A build outcome with progress recorded.
- F7.2-06 — Flash and verify boot
  - Description: Flash the output and confirm it boots. This is the user's action and carries real risk to a working device.
  - Output: A boot verdict.
- F7.2-07 — Run the AON verification
  - Description: Execute the procedure Faz 6.2 wrote: confirm the four provider capabilities are present with the runtime module absent, proving or refuting the symlink entry.
  - Output: The AON verification result.
- F7.2-08 — Assess daily-use suitability
  - Description: Determine whether this build is a candidate daily base or a verification artifact only, accounting for invariant 10 and the fact that different vendor blobs would invalidate every camera patch.
  - Output: A suitability assessment with the camera consequence stated.
- F7.2-09 — Record the outcome for Phase 8
  - Description: State what Phase 8 inherits: a working build process, a partial one, or a blocked one. Autopsy requires Phase 8 not be decomposed until this is known.
  - Output: A Phase 8 readiness statement.

## 8. Acceptance Criteria

- A stopping rule is recorded before the build begins.
- The branch, platform tree, and device tree decisions are settled and recorded with reasoning.
- The source sync completes, with space consumed recorded against the Faz 7.1 assessment.
- The configuration step selects `ishtar` successfully, or the failure is characterized specifically.
- A build attempt is made and its outcome recorded, including how far it progressed if it did not complete.
- If a flashable output exists, the boot verdict is recorded.
- If the build boots, the AON verification from Faz 6.2 is executed and its result recorded.
- The daily-use suitability assessment states the camera patch consequence explicitly.
- The Phase 8 readiness statement is written, since Autopsy gates Phase 8's decomposition on it.
- If the stopping rule is reached without a build, that is recorded as a bounded outcome rather than an incomplete one.

## 9. Validation and Test Approach

Validation is build-level and, for the first time in this roadmap, involves flashing a whole system image. That raises the stakes of the manual verification considerably compared to flashing a module.

- `VAL-SYNC` (proposed) — the source sync completing, with space consumed recorded.
- `VAL-CONFIG` (proposed) — the configuration step selecting the device, which is the cheapest evidence that the device trees are usable.
- `VAL-BUILD` (proposed) — a build attempt with its outcome and progress recorded. This identifier was named by Faz 6.2 as the deferred verification's home.
- `VAL-BOOT` (proposed) — the flashed build boots. The user's action, on their own device.
- `VAL-AON` (proposed) — the four provider capabilities present with the runtime module absent, per the Faz 6.2 procedure.
- `VAL-DOCS` (proposed) — read back the settled decisions, the suitability assessment, and the Phase 8 readiness statement.

Local versus live: the sync, configuration, and build are host-local; the boot and AON verification are live and carry device risk. Security validation is not applicable. Ontology validation applies to invariant 10, whose consequence the suitability assessment must state.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| refs/a16_ishtar | existing | Android 16 device tree input, carrying the Faz 6.1 symlink entry. | VAL-CONFIG, VAL-AON |
| refs/a16_sm8550 | existing | Android 16 platform tree input, subject to the F7.2-02 decision. | VAL-CONFIG |
| docs/aon-verification.md | existing | The procedure Faz 6.2 wrote, executed here for the first time. | VAL-AON |
| docs/build-environment.md | modified | Extended with the sync, configuration, and build steps actually used. | VAL-DOCS |
| device_ishtar/proprietary-files.txt | existing | Reference for what a working configuration looks like on the current build. | VAL-CONFIG |

## 10. Dependencies and Sequencing

Depends on Faz 7.1 absolutely for the environment. Depends on Faz 6.1 for the symlink entry the AON verification tests, and on Faz 6.2 for the verification procedure itself.

Benefits from Faz 1.6's reference index, which resolves which `refs/` trees are authoritative inputs rather than comparison sources — a question this sub-phase would otherwise have to answer from naming.

Blocks Phase 8 entirely, and Autopsy specifically gates Phase 8's decomposition on this sub-phase's outcome.

Required decisions: the branch, the platform tree, and the device tree scope. All three are marked open here rather than guessed, and all three are answerable only with sources in hand.

Required infrastructure: substantial disk space inside the Linux filesystem, network capacity for the source sync, and the device for flashing.

Required human actions and approvals: the flash and boot verification. This is a whole-system flash on the user's daily device, which is a materially larger commitment than the module flashes earlier in the roadmap. The suitability assessment exists partly so that commitment is made with the camera consequence understood.

Fresh session token and context risk: medium, per Main-Planing's banding. Build output is voluminous and the mitigation is recording outcomes and error classes rather than transcripts.

Subagents are not recommended.

## 11. Risks and Mitigations

- Risk (invariant 10): the Android 16 build carries different vendor blobs and every camera patch invalidates at once. Impact: flashing it as a daily base trades the project's working capability for an unbuilt one. Mitigation: F7.2-08 requires the suitability assessment to state this explicitly, so the flash decision is made knowingly rather than discovered afterward.
- Risk: the build absorbs unbounded effort because it nearly works. Impact: Phase 8's resources are consumed before Phase 8 begins. Mitigation: F7.2-01 sets a stopping rule before the build starts, following the pattern Faz 3.1 established for Phase 3.
- Risk: flashing a whole system image bricks or degrades the user's daily device. Impact: far higher than any module-level risk in this roadmap. Mitigation: this is inherent to the phase rather than removable; the mitigation is that the boot verification is explicitly the user's decision and the suitability assessment precedes any adoption.
- Risk: the AON verification is skipped because the build itself dominates attention. Impact: the Faz 6.1 change stays unverified indefinitely, which is exactly the inertia Faz 6.2 registered the procedure to prevent. Mitigation: F7.2-07 is a distinct work item and the acceptance criteria require its result.
- Risk: the source sync exhausts the virtual disk. Impact: hours of work lost. Mitigation: F7.2-03 records consumption against the Faz 7.1 assessment, and that assessment exists specifically because the Windows volume figure does not describe the Linux environment.
- Risk: the wrong branch or platform tree is chosen and the mismatch surfaces deep into the build. Impact: rework. Mitigation: F7.2-02 settles and records the decisions before the sync rather than during the build.
- Risk: a partial build is recorded as a failure with no detail. Impact: the next attempt starts from nothing. Mitigation: F7.2-05 requires progress and error classes to be recorded, since partial progress is genuinely informative for a first attempt.
- Risk (Autopsy section 11): Phase 8 is decomposed before this outcome is known. Impact: planning against an unbuilt environment. Mitigation: F7.2-09 produces the readiness statement Phase 8's decomposition is gated on.

## 12. Desired End State

An AOSPA Android 16 build for `ishtar` has been attempted with a recorded outcome. If it succeeded, a flashable output exists, its boot is verified, and the AON symlink fix is finally proven or refuted. The branch and tree decisions are settled and recorded, the daily-use suitability is assessed with the camera patch consequence stated, and Phase 8 has a readiness statement to be decomposed against.

The evidence an implementer should produce is the stopping rule, the settled decisions, the sync and configuration results, the build outcome with progress, and — if the build boots — the boot verdict and the AON verification result.

The ledger summary Step 4 should append records: the decisions settled, the build outcome against the stopping rule, whether the AON fix was verified, the suitability assessment, and what Phase 8 inherits.

## 13. Next Sub-Phase Transition Criteria

- The stopping rule was set before the build and the outcome is recorded against it.
- The branch, platform tree, and device tree decisions are settled with reasoning.
- The build outcome is recorded, including progress if it did not complete.
- If a build booted, the AON verification result exists.
- The daily-use suitability assessment states the camera patch consequence.
- The Phase 8 readiness statement is written, and Phase 8 is not decomposed before it exists.
