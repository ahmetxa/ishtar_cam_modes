# Faz 1.4 — Toolchain Procedure Record

## 1. Context

Main-Planing Phase 1 asks for the reverse-engineering toolchain to be recorded "as a written, re-runnable procedure" and is unusually specific about why: "Record explicitly that apktool's bundled smali `Main` classes are stripped stubs and that radare2 does not complete on this binary — the negative findings are as valuable as the positive ones and cost real time to discover."

Autopsy section 6 files this under "Environment fragility" and adds the historical detail: "The reverse-engineering toolchain has been reconstructed at least once after a context loss, and the reconstruction cost real time." Prioritized next step 9 in Main-Planing names it an ontology and ledger action.

Project-Ontology section 6 already holds the raw material — a toolchain paragraph and a toolchain-negative-findings paragraph — and Project-Comprehension records `EV-17` ("radare2 and rabin2 do not complete on this binary", confidence `confirmed`, two runs at 300 s and 60 s in two different shells). What does not exist is a procedure: an ordered set of steps that takes a machine with none of this installed to a machine that can disassemble `camera.qcom.so` and rebuild a patched APK.

Phase 3 is the consumer. It is the highest token-risk phase in the roadmap and it needs a working disassembly capability on day one, not on the day after a toolchain reconstruction.

## 2. Goal

Convert the scattered toolchain knowledge into an ordered, re-runnable setup procedure that includes the dead ends, so a fresh machine or a fresh session reaches a working disassembly and repackaging capability without rediscovering what has already been ruled out.

## 3. Description

The problem is that positive knowledge is recorded as a component list and negative knowledge is recorded as prose, and neither form is executable. Someone rebuilding the environment reads the list, tries the obvious sources, and hits the same four dead ends the project already paid for.

It belongs in Phase 1 because Phase 3 depends on it and because it is pure documentation with no device risk. It reduces project risk in the specific way `R10` describes — "long sessions, context exhaustion, repeated re-derivation" — by removing one entire category of re-derivation.

The vibecoding slice strategy: the first useful slice is the smali and baksmali path, because that is what Faz 3 and Faz 9 both need and it is the one with the most dead ends around it. The fastest validation signal is running baksmali once against `classes2.dex` from a known APK and getting output. The disassembly path (Python plus capstone plus pyelftools) is the second slice and validates by locating one already-known address from Project-Ontology section 6 — a self-checking test, because the expected answer is written down.

What not to over-plan: containerization, dependency pinning beyond exact versions, or automating the setup. The procedure is written prose with exact versions and exact commands. Automating it is only worth doing if it is followed more than twice.

There is an important boundary. `AGC8.4.300_V9.6_snap.apk` and its patched sibling are 150 MB artifacts excluded from version control by Faz 1.1. The procedure must therefore state where they come from and what identifies them, since they are inputs the repository does not carry.

## 4. Scope

- An ordered setup procedure with exact versions for the Java toolchain: Temurin JDK 21, smali and baksmali 2.5.2 from the legacy Maven group, dexlib2, util, guava 31.1-jre, failureaccess, antlr-runtime 3.5.2, jcommander 1.82, and ST4.
- The APK signing step: uber-apk-signer 1.3.0, with the key-location policy from Faz 1.2 rather than a concrete credential path.
- The native disassembly path: embeddable Python 3.12.7 with capstone 5.0.7 and pyelftools, including why an embeddable distribution is used on this host.
- The four recorded negative findings, each stated as "do not attempt, and here is what happens".
- A self-check for each path that proves the tool works before it is relied on.
- The identification of external inputs the repository does not carry: which APK builds, identified by name and by checksum rather than by download location.
- A statement of the host constraint that separates this toolchain from the build toolchain in Phase 7.

## 5. Out of Scope

- Installing anything. This sub-phase writes the procedure; following it is the implementer's action and may already be satisfied on the current host.
- WSL2 provisioning or any ROM and kernel build capability. That is Phase 7 and it is a different toolchain with a different constraint.
- Automating setup with a script, container, or package manifest.
- Redistributing any tool or any APK. The procedure names versions and identifies artifacts; it does not bundle them.
- Resolving the AGC redistribution governance question raised in Autopsy section 9.
- Writing the disassembly method for `pixelArraySize` — that is Faz 3.2's work. This sub-phase establishes only that a disassembler runs.

## 6. Current Repository Evidence

Project-Ontology section 6 records the full component list under "Toolchain" and four negative findings under "Toolchain negative findings": apktool's bundled smali `Main` classes are stripped stubs and cannot be invoked; `com.android.tools.smali` Maven paths return 404; the Bitbucket mirror returns 403; google/smali publishes no release binaries; and radare2 and rabin2 5.9.8 produce no output on this 27 MB binary within 300 seconds from either shell.

`agc-50mp-yama/README.md` was read in this run and already contains a partial reproduction procedure under "Yeniden üretme": extract `classes2.dex` from the APK, run baksmali with the smali 2.5.2 jar set, replace `getSupportedOutputSizes` and append `allOutputSizes`, reassemble with `smali -a 29`, and replace the `classes2.dex` entry in the APK. This is the seed for the Java half of the procedure and should be referenced rather than duplicated.

`ishtar-cam-modes/tools/` holds four Python scripts totalling 732 lines. `verify_ln.py` was read in this run and imports only `struct`, `zlib`, `sys`, and `os` — the standard library. This is evidence that the blob-generation path needs no third-party Python packages, whereas the native disassembly path needs capstone and pyelftools. The procedure should distinguish the two, since a machine that only needs to regenerate sensor blobs has a much smaller dependency set.

No Python interpreter is available on the host through the normal path: `python --version` returns the Windows Store alias stub and `py` is not present. This was measured in this run and is directly relevant — the procedure's Python step is not satisfied by default on this machine.

`platform-tools/` holds a vendored `adb`, which is the host-to-device channel and belongs in the procedure as an already-satisfied component.

## 7. Planned Work Breakdown

- F1.4-01 — Write the Java and smali path as ordered steps
  - Description: Exact versions, the correct Maven group, the full jar set needed on the classpath, and the two commands (disassemble, reassemble) with the `-a 29` API level. Reference the existing recipe in `agc-50mp-yama/README.md` rather than restating it.
  - Output: A numbered setup and usage section.
- F1.4-02 — Write the negative findings as explicit non-steps
  - Description: Each of the four dead ends stated as an instruction not to attempt, with the observed symptom, so a reader recognizes the failure if they hit it anyway.
  - Output: A "do not attempt" section with four entries.
- F1.4-03 — Write the native disassembly path
  - Description: The embeddable Python distribution, capstone 5.0.7, and pyelftools, plus the reason a disassembler script is used instead of an interactive tool — namely `EV-17`.
  - Output: A disassembly setup section.
- F1.4-04 — Record the Python availability finding for this host
  - Description: State that no system Python is on the path and that the embeddable distribution is therefore a requirement rather than a preference on this machine.
  - Output: A host-state note.
- F1.4-05 — Define a self-check per path
  - Description: For the Java path, disassemble one dex and confirm `LAGC;` appears. For the disassembly path, load `camera.qcom.so` and confirm the four known `cmp` sites at the offsets recorded in Project-Ontology section 6 decode as expected. The second is self-checking because the answer is already written down.
  - Output: Two self-check procedures with expected results.
- F1.4-06 — Identify external inputs by checksum
  - Description: Name the APK builds the procedure consumes and identify them by checksum, noting that they are excluded from version control and must be supplied separately.
  - Output: An external-inputs section.
- F1.4-07 — Separate this toolchain from the Phase 7 build toolchain
  - Description: State that this procedure covers analysis and repackaging only, that it runs on the Windows host, and that ROM and kernel building is a different environment with a different blocker.
  - Output: A scope boundary note referencing Phase 7.

## 8. Acceptance Criteria

- Every component named in Project-Ontology section 6 appears in the procedure with its exact version.
- All four negative findings appear as explicit non-steps with their observed symptoms.
- The Java path self-check produces named output from a real dex, not a described expectation.
- The disassembly path self-check decodes the four `cmp` sites recorded in Project-Ontology section 6 and the decoded instructions match what that section states.
- The absence of a system Python interpreter on this host is recorded as a measured fact.
- External APK inputs are identified by checksum, and the procedure states they are not carried in version control.
- The boundary against Phase 7's build environment is stated, so the two toolchains are not conflated.
- No credential path, key material, or download location that implies redistribution appears in the document.

## 9. Validation and Test Approach

Validation is document-level plus two executable self-checks. Neither self-check touches the device.

- `VAL-DOCS` (proposed) — compare the procedure against Project-Ontology section 6; confirm every component and every negative finding is represented, and that no component is named that the ontology does not record.
- `VAL-TOOLCHAIN` (proposed) — run the Java path self-check: extract `classes2.dex` from an AGC build and disassemble it, confirming `LAGC;` is present in the output.
- `VAL-DISASM` (proposed) — run the disassembly path self-check: decode the four sites recorded in Project-Ontology section 6 and compare against the recorded instruction forms. A mismatch means either the procedure or the address book is wrong, and either finding is valuable.

Live readiness, CI, and artifact validation are not applicable. Ontology consistency applies: if a self-check contradicts a recorded address, Project-Ontology section 6 must be corrected in the same session rather than the discrepancy being noted for later.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| docs/reverse-engineering-toolchain.md | proposed | The ordered setup and usage procedure this sub-phase produces. | VAL-DOCS, VAL-TOOLCHAIN, VAL-DISASM |
| agc-50mp-yama/README.md | existing | Seed recipe for the Java path; referenced rather than duplicated. | VAL-DOCS |
| Planner-docs/Project-Ontology.md | modified | Corrected if a self-check contradicts a recorded address or version. | VAL-DISASM |
| ishtar-cam-modes/tools/verify_ln.py | existing | Evidence that the blob path needs only the standard library, unlike the disassembly path. | VAL-DOCS |

## 10. Dependencies and Sequencing

Depends on Faz 1.2 for the key-location policy that the signing step references. Without it, the signing step would have to name a concrete credential path, which planning files must not contain.

Feeds Faz 3.2 directly — the write-site search cannot start without a working disassembler — and Faz 9.1 indirectly, since release repackaging uses the same Java path.

Required decisions: none. Every version is already recorded; this sub-phase orders them.

Required credentials: the signing key is referenced by policy only. The procedure's signing step is not executable without it, and that is stated rather than worked around.

Required infrastructure: none beyond the current host. The external APK inputs must be present, and F1.4-06 makes that dependency explicit.

Required human approvals: none.

Fresh session token and context risk: low to medium. Writing the document is low; running the disassembly self-check loads a 27 MB binary and should use a script with bounded output rather than interactive exploration, exactly as `R10` recommends.

## 11. Risks and Mitigations

- Risk: the procedure is written from Project-Ontology rather than from a real run, and a version or a classpath entry is subtly wrong. Impact: the next reconstruction fails and the document loses credibility. Mitigation: `VAL-TOOLCHAIN` and `VAL-DISASM` require both paths to actually execute before the sub-phase is accepted.
- Risk (`EV-17`): someone attempts an interactive disassembler anyway because it is the obvious tool. Impact: 300 seconds of no output, twice, repeating a measured dead end. Mitigation: F1.4-02 states the symptom, not just the prohibition, so the failure is recognized immediately.
- Risk: the external APK inputs are unavailable when the procedure is next followed. Impact: the Java path cannot be self-checked and the procedure is unverifiable. Mitigation: F1.4-06 identifies them by checksum so a substitute can be confirmed as equivalent or rejected as different.
- Risk: the disassembly self-check contradicts the recorded addresses. Impact: Phase 3 plans against a wrong address book. Mitigation: this is treated as a finding rather than a failure — Project-Ontology section 6 is corrected in the same session, which is more valuable than the procedure passing.
- Risk (`R10`): running the disassembly path interactively during this sub-phase consumes a large context budget for a setup task. Impact: less budget for Phase 3, where it matters. Mitigation: the self-check is a scripted decode of four known addresses with short output, not exploration.
- Risk: the document drifts as tool versions change. Impact: a future reader trusts a stale version. Mitigation: versions are stated as measured-at-a-date facts, consistent with how the project records device measurements.

## 12. Desired End State

A written procedure exists that takes a machine from nothing to a working analysis capability: disassemble and reassemble dex, repackage and sign an APK, and disassemble the ARM64 HAL binary. It carries exact versions, the four dead ends with their symptoms, two executable self-checks that have been run, an honest note that this host has no system Python, and an identification of the external inputs version control does not carry.

The evidence an implementer should produce is the output of both self-checks — the `LAGC;` presence check and the four decoded `cmp` sites.

The ledger summary Step 4 should append records: the procedure path, whether both self-checks passed, and any correction made to Project-Ontology section 6 as a result.

## 13. Next Sub-Phase Transition Criteria

- Both self-checks have been executed and their real output recorded.
- All four negative findings are present as non-steps with symptoms.
- Any discrepancy between a self-check and the recorded address book has been resolved in the ontology, not deferred.
- The signing step references the key by policy and contains no credential path.
- Phase 3 has a working disassembler available before Faz 3.2 begins.
