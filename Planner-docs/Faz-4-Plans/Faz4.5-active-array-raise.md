# Faz 4.5 — Active Array Raise

## 1. Context

`DEC-12`, answered by the user on 2026-09-01, created this sub-plan and fixed its position: the `f0000` / `f000a` / `80340003` raise becomes its own sub-plan, sequenced **before** `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md`. The alternatives — placing it after Faz 4.1, or absorbing it into Faz 4.1 — were both rejected on the record. It should not queue behind blast-radius reduction because it is the P1 fix, and it should not be merged into Faz 4.1 because a three-tag write-site search and an array-count measurement carry different risk profiles and would contaminate each other's evidence.

The work item itself is `IMPL-24`'s fourth preservation requirement, handed forward when Faz 3.6 closed Phase 3: keep `f0006` at `[8192 6144]`, keep RAW10 advertised at 8192x6144 while narrowing elsewhere, **and additionally raise `f0000`, `f000a` and `org.codeaurora.qcamera3.quadra_cfa.activeArraySize (80340003)` from `[0 0 4096 3072]`**. The first three are Faz 4.1's job. The fourth is this sub-plan's, and it is the only one of the four that requires locating new code.

It is the fix for `FIND-3.5-01` (P1), raised by `IMPL-23`: every full-resolution AGC frame is geometrically corrupt — content fills only the active-array extent of a full-size buffer, leaving exactly half the frame black in a fixed position with a magenta cast over the remainder. That finding is what makes the project's headline result — three reproducible 50.3 MP captures — unusable as an image.

**On the number.** This is `Faz 4.5`, not `Faz 3.7`. Phase 3 was closed by user decision on 2026-09-01 as a primary success, and the project has been firm that it stays closed; adding a seventh Phase 3 sub-plan would reverse that decision by filing rather than by argument. Phase 4's stated goal — "the smallest change that is also internally consistent" — is in fact the better fit, because a metadata set advertising an 8192x6144 pixel array alongside a 4096x3072 active array is precisely an internally inconsistent patch. Numbering it last in the folder and first in the execution order keeps sub-plan numbering contiguous without renumbering anything that already exists.

## 2. Goal

Raise the three active-array tags to the sensor's full-resolution extent — `[0 0 8192 6144]` — so that a full-resolution buffer is described by metadata consistent with itself, and AGC's 50 MP output becomes a usable image rather than a completed capture with a corrupt frame.

## 3. Description

The mechanism is understood well enough to state without hedging, and understanding it is what makes this a bounded job rather than an investigation. `libgcam`'s static-metadata gate compares `frame_raw_max` against *either* array, which is why raising `f0006` alone was enough to stop `static_metadata.cc:667` and let a capture complete. But the imaging pipeline downstream lays out geometry from the **active** array specifically. A full-size buffer described by a half-size active rect therefore produces exactly the artifact observed: valid content over the active extent, black where the pipeline never wrote, and a colour cast because the factor-of-two geometry error flips CFA phase. Open Camera is clean at 8192x6144 from the identical device state, because its frames come from the HAL's own ISP path rather than from Gcam's RAW consumption. The HAL can deliver the image; the description of it is wrong.

Three tags carry that description, and they are not equivalent. `f0000` and `f000a` are standard Android tags published by the same CamX routine that publishes `f0006`, so the already-mapped publishing function is the natural entry point. `80340003` is a QTI vendor tag in the `quadra_cfa` namespace, and nothing in the repository establishes that it is published from the same place or by the same mechanism. Treating all three as one problem is the mistake this sub-plan is shaped to avoid.

The slice strategy follows the one that already worked twice on this codebase. Faz 3.2 calibrated its disassembly against known-good sites before searching, and caught nine wrong addresses as a result. Faz 3.3 pre-committed a predicted md5 before writing anything, and matched it on both apply and revert. This sub-plan does both, then applies **one tag at a time** with a measurement between each, because `scripts/smoke.sh` already prints `activeArray=[...]` per camera and the cost of an extra bracket is one snapshot.

The fastest validation signal is not the capture. It is that `activeArray` field moving from `[0 0 4096 3072]` to `[0 0 8192 6144]` on the expected camera id, which is a text diff between two snapshots and needs no shutter press. The capture comes afterwards, and it answers a different question — whether the raise actually fixes the image — which is the one the user cares about and the one that closes `FIND-3.5-01`.

What must not be over-planned here is the format-32 extension. `FIND-3.5-02` and `OQ-02` are real and adjacent, but `DEC-11` routed them into Faz 4.1, and pulling a format-gate change into a tag-raise measurement would reproduce exactly the bundling this sub-plan exists to prevent.

## 4. Scope

- A **fresh write-site search** for `f0000` and `f000a`, taking the mapped publishing function at `0x01661f40` as the entry point rather than trusting the recorded address book.
- Decode-validation of every `f0000` / `f000a` address-book entry before any budget is spent on it, since `FIND-3.2-01` establishes that entries of unknown provenance in this book do not survive a decode.
- Determination of where the QTI vendor tag `80340003` is published, and whether it is patchable by the same mechanism as the standard tags or by a different one.
- Tracing the value source for each rect inside the sensor data structure `S`, using the unbinned/binned relation Faz 3.3 established as the working model, and stating whether an unbinned full-resolution rect already exists there.
- A patch table expressing the change as four-byte-indexed word replacements, with its resulting md5 **computed and committed before any device write**.
- Per-tag incremental application, each bracketed by `scripts/smoke.sh` and each measured on the `activeArray` field before the next tag is touched.
- An AGC full-resolution capture re-test against the `FIND-3.5-01` artifact, producing an image verdict.
- Immediate recording of every located address into `Planner-docs/Project-Ontology.md` during the session it is found.
- An explicit budget verdict against the remaining allowance, whether the search succeeds or exhausts it.

## 5. Out of Scope

- Narrowing the RAW format emission. `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md` owns that, and it runs after this sub-plan.
- Extending emission to format 32 / `RAW_SENSOR`. `DEC-11` routed that into Faz 4.1 explicitly; it is not pulled forward here even though it shares a motivation with this work.
- Adding `availableMinFrameDurations` or `availableStallDurations` rows, which are Faz 4.2.
- Consolidating or relocating patch tables, which is Faz 4.3, and the full consumer survey, which is Faz 4.4.
- Any change to the `f0006` write site at `0x0166645c`. It is confirmed by measurement and must be preserved exactly as it stands.
- Reopening Phase 3, its decision, or any of its closed questions. This sub-plan consumes Phase 3's evidence; it does not revise it.
- Any change to the sensor layer, the mode blobs, or the ten-mode dispatch.
- Composing 50 MP with the LN modes, which is Phase 5.
- Building a general-purpose metadata-tag locator. Three tags do not justify tooling.

## 6. Current Repository Evidence

**The publishing function is already mapped, and it is the reason this search starts ahead rather than at zero.** Project-Ontology section 6 records that the routine beginning `0x01661f40` (`paciasp`, prologue `stp x29, x30, [sp, #-0x60]!` at `0x01661f44`, stripped, not covered by `ChiEntry`) "publishes the entire `android.sensor.info.*` family — `f0001` through `f000a` — in one sequence." Both target standard tags fall inside that stated range.

**One of the two is already partially located.** The same section records, under sibling offsets: "`f000a` (count 4) from `S+0x3d88` loaded via `q7` (`bl` at `0x01666588`)". A count of 4 is consistent with a four-int32 rect, and a `q7` load is consistent with moving all sixteen bytes at once. That entry was produced by the same decode work that classified the nine false positives, so unlike the older book entries it has known provenance. `f0000` has no comparable entry and is the genuine unknown.

**The value-source model is established and testable.** `IMPL-20` traced the initializer region `0x016f0330` … `0x016f0830` and recorded that `[S+0x3db4] = [S+0x3c1c] / binning` and `[S+0x3db8] = [S+0x3c20] / [S+0x3d80]`, and that "the same block derives `[S+0x3d98]`/`[S+0x3d9c]` from `[S+0x3c54]`/`[S+0x3c58]` and `[S+0x3da0]`/`[S+0x3da4]` from `[S+0x3c5c]`/`[S+0x3c60]` by the same division." So `S` holds unbinned/binned pairs for several quantities, not only for the pixel array, and the displacement `0x3c1c + 0x198 = 0x3db4` was noted as "precisely the unbinned-to-binned hop." Whether an analogous unbinned rect exists for the active array is the single most valuable thing this sub-plan can determine early, because if it does, the same one-word redirection that solved `f0006` may solve these.

**The confirmed `f0006` patch is the calibration reference.** `0x0166645c`, `ldr x1, [x4, #0x198]` (`0xF940CC81`) to `ldr x1, [x4, #0]` (`0xF9400081`), four-byte index `5871895`; md5 `77083b7c099d4c68a9213476141c450d` on a stock base and `c539f04e6bbaedb907a5c987f16800ea` on a fullres base, both predicted before the run and matched. Stock HAL is `c3fa63a86ee3ecaf9fbf02005d35f6b5`, 27,268,688 bytes. File offset equals virtual address for `.text` (`0x004f7000`, size `0x146a538`) and `.rodata` (`0x000280e0`, size `0x3d5d68`).

**The measured tag state under the three-layer stack `c3db54b0b154dd19211f221e3d5046e7`** is recorded exactly: `f0006` `[8192 6144]`; `f0000` `[0 0 4096 3072]`; `f000a` `[0 0 4096 3072]`; `80340003` `[0 0 4096 3072]`; `f0002` `BGGR`. The ontology names those three "the outstanding work" in the same line. The raise target is therefore `[0 0 8192 6144]` for all three, and the starting value is identical across all three — which means a snapshot diff distinguishes them unambiguously only if they are moved one at a time.

**`FIND-3.2-01` governs how the address book may be used here, and it is a hard constraint rather than a caution.** All nine recorded `movz`/`movk` addresses for `f0006` were false positives — six load two division magic constants repeated across unrelated functions, two load hashed keys, one builds a `stp` literal — and all six rodata dwords, while genuinely holding `0x000f0006` and being the only such dwords in the file, are **tag-list table interiors reached by indexing**, with no exact `adrp`+`add` pair computing any of their addresses. The finding's own words are the operative part: "The finding is not the nine wrong addresses — it is that other entries in the address book may share that provenance. … What has *not* been re-derived by decode should be treated as unvalidated until it is." Two of the six dwords sit inside strictly sequential tag runs spanning `000f0001` … `000f000a`, which means any `f0000` or `f000a` entry of the same vintage is presumptively a table interior too. **Every such entry is unvalidated until this sub-plan decodes it.**

**The budget.** `docs/phase3-preconditions.md` section 3 fixes `DEC-06` at 15 candidate sites across at most 2 implementation sessions. `IMPL-18` spent 3 and `IMPL-20` spent 1; `IMPL-24` reconciled the total at 4 of 15 and stated that "the three active-array tags now require a fresh search against the remaining 11 of 15 sites." The eleven are an **attempt allowance**, not a list: the original fifteen were `f0006` addresses and are now known-dead, so the allowance is spent against whatever candidates this search produces, one per candidate examined to the point of a patch decision. This reading is stated here so it is not settled mid-search, which is exactly the failure `AUTOPSY-P1-03` describes.

**The measurement surface already exists.** `scripts/smoke.sh` line 156 prints `camera.hal<id> facing=… streamcfg=… pixelArray=[…] activeArray=[…]` for every camera, sorted by id, and its `activeArray` value is read from the `dumpsys media.camera` block for `android.sensor.info.activeArraySize`. No new probe is needed for the two standard tags. The vendor tag `80340003` is **not** in that summary and needs its own read from the dump.

**`EV-17` still constrains method:** interactive disassemblers do not complete on this binary — two runs at 300 and 60 seconds produced no output. All analysis is scripted, per `docs/reverse-engineering-toolchain.md`.

## 7. Planned Work Breakdown

- F4.5-01 — Calibrate the disassembly before searching
  - Description: Decode the four known `cmp wN,#2` sites and the confirmed `f0006` write at `0x0166645c` against stock HAL `c3fa63a8…`, confirming both the instruction encodings and the four-byte index convention. This is the control that caught nine bad addresses in Faz 3.2, and it costs no budget.
  - Output: A five-site calibration result, pass or fail, recorded before any new address is derived.
- F4.5-02 — Validate or discard the recorded `f0000` and `f000a` entries
  - Description: For every address-book entry naming `f0000` or `f000a`, decode it and classify it as a value source, a tag emission, a tag-list interior, or a false positive. Per `FIND-3.2-01`, an entry that is not decode-validated in this step may not have budget spent on it in the next.
  - Output: A per-entry classification table, with discarded entries marked as such in the ontology.
- F4.5-03 — Enumerate the `f0000` and `f000a` publications inside `0x01661f40`
  - Description: Walk the publishing sequence and record, for each of the two tags, the `bl` address into publisher `0x1755430`, the element count in `w3`, the staging slot passed in `x2`, and the instructions that fill that slot. `f000a`'s `bl 0x01666588` and `S+0x3d88` are the starting reference; `f0000` is derived the same way.
  - Output: Two publication records in the form the ontology already uses for `f0006`.
- F4.5-04 — Trace the rect value sources in `S`
  - Description: Determine which offsets in `S` supply each rect, and whether an unbinned full-resolution active rect exists there — testing the unbinned/binned model directly by looking for the `0x198`-style hop or the equivalent division inside the initializer at `0x016f0330` … `0x016f0830`. State whether the values are runtime-derived or binary constants, as Faz 3.2 did for `f0006`.
  - Output: A stated value origin per tag, and a yes or no on whether a full-resolution rect already exists in `S`.
- F4.5-05 — Locate the publisher of vendor tag `80340003`
  - Description: Establish whether the QTI `quadra_cfa` tag is published by the same CamX routine, by a vendor-tag provider, or by a path this project has not yet mapped, and whether it is reachable by a static word patch at all. A negative answer here is a legitimate result and must be reported as one rather than absorbed into the other two tags' outcome.
  - Output: A publisher determination for `80340003`, with a patchability verdict.
- F4.5-06 — Design the patch and pre-commit its checksum
  - Description: Express the change as four-byte-indexed word replacements within the alignment constraint the Faz 1.3 format contract sets, compose it against the layer stack the measurement will use, compute the resulting md5 host-side, and record that md5 **before** any device write — the practice `IMPL-23` established and matched on both apply and revert.
  - Output: A patch table plus a committed predicted md5.
- F4.5-07 — Apply one tag and measure
  - Description: Apply the change for a single tag with the camera stack stopped in `restart_camera`'s client-before-HAL order, then read the `activeArray` field from a post-change smoke snapshot and compare it against the pre-change bracket. Do not proceed on a partial or ambiguous result.
  - Output: A single-tag metadata delta, per camera id.
- F4.5-08 — Extend to the remaining tags
  - Description: Apply the remaining tags, each with its own bracket and its own reading, so that a failure attributable to one tag is not diagnosed against the set.
  - Output: A per-tag metadata verdict for all three tags, or a stated reason a tag was not attempted.
- F4.5-09 — Re-test the AGC capture against `FIND-3.5-01`
  - Description: With `f0006` and the raised tags live together, launch AGC and take a full-resolution capture, then inspect the image for the specific artifact the finding names — the fixed-position black half and the magenta cast. Report the image verdict as a description of what is seen, not as a pass or fail alone.
  - Output: A capture with an image verdict, closing or refusing to close `FIND-3.5-01`.
- F4.5-10 — Record addresses and declare the budget verdict
  - Description: Write every located address into Project-Ontology section 6 during the session it is found, per `R10` and `QAS-03`, and state the sites consumed against the remaining allowance whether the search succeeded or exhausted it.
  - Output: An updated address book and an explicit budget verdict.

## 8. Acceptance Criteria

- The five-site calibration passed, or a discrepancy was resolved, before any new address was derived.
- Every `f0000` and `f000a` address-book entry carries a decode classification, and no budget was spent on an entry that had not been classified first.
- The publication site for `f0000` and for `f000a` is recorded in the same form the ontology uses for `f0006`: `bl` address, element count, staging slot, and filling instructions.
- The value origin of each rect is stated with supporting evidence, and the question of whether `S` already holds a full-resolution active rect has a yes or a no.
- The `80340003` publisher determination is stated, including an explicit negative if the tag is not statically patchable — recorded as a result, not as an incomplete item.
- The predicted md5 was committed before the first device write, and matched on apply and on revert.
- `activeArray` moved from `[0 0 4096 3072]` toward `[0 0 8192 6144]` for at least one tag, read from a bracketed smoke snapshot, with the camera id named.
- Each tag was applied and measured separately; no verdict rests on a reading taken after two tags moved at once.
- `f0006` still reads `[8192 6144]` after the raise, and the RAW rows at 8192x6144 are unchanged — the Phase 3 result is verified as preserved, not assumed.
- The AGC capture re-test produced an image verdict describing what the frame actually looks like, and `FIND-3.5-01` is explicitly closed or explicitly left open.
- The reversal produced a snapshot byte-identical to the pre-attempt baseline in the comparable region.
- Every address located during the work is in Project-Ontology section 6 by the end of the session, not in a note to be transferred later.
- The budget verdict is stated explicitly, and an exhausted allowance is recorded as a completed outcome rather than a failure.

## 9. Validation and Test Approach

**The validation contract is `docs/phase3-preconditions.md` section 5 in full — the seven items of the Faz 3.1 per-measurement checklist, restated here because this sub-plan sits in Phase 4 and cannot inherit them by phase membership.** Every one applies to every measurement in this sub-plan.

1. **Preferences clear.** All twelve trap keys audited, expecting 0/12, by the per-key grep — never by a single `scripts/smoke.sh` reading.
2. **Bracket taken.** `scripts/smoke.sh -o <UTC>__Faz4.5__<label>` before the change and again after. Both committed.
3. **One variable.** Exactly one of {sensor layer, HAL layer, APK, preference} moved since the previous snapshot. If two moved, the measurement is not attributable and is redone. This is what forces F4.5-07 and F4.5-08 to be separate work items.
4. **Metadata republished.** Per `FIND-2.3-01`, any reading of advertised metadata after a mode change must first establish that the metadata republished — confirm the stream-config count reached its expected value, or that `wait_camera_list` completed, before reading a row. RAW rows are read **per resolution**, never collapsed to one value per mode.
5. **Restorable.** The previous state is restorable by a named command, and the restore is verified by snapshot diff rather than assumed.
6. **Addresses recorded immediately.** Every located address goes into `Project-Ontology.md` in the session it is found. Address-book values have been lost to context truncation on this project before.
7. **Attribution stated.** Every result names the AGC build it was measured against — currently the patched `ce65f862c990e2acc02be356f75a7122`, not stock.
8. **Crash contamination cleared.** After **any** camera-provider abort, reboot before taking the next reading. A reading taken after an abort without an intervening reboot is void and is retaken, not interpreted.

**`AUDIT-FIX-08`, discharged here by the second of the two options the Step 3 audit offered (2026-09-01, IMPL-27).** Item 8 is `FIND-3.4-03`'s rule. `IMPL-22` established that one provider abort contaminates the **whole boot** — every later reading in any mode, `stock` included, shows the same `CSLAcquireHardwareHW` signature until reboot — and that mechanism already forced a conclusion to be withdrawn once. Its proper home is an eighth item on the per-measurement checklist in `docs/phase3-preconditions.md`, and **it is knowingly absent from that file.** No sub-plan in the queue can put it there: the file is `existing` in this sub-plan's Implementation Contract, `existing` in `Faz3.2` and `Faz3.6`, and `proposed` only in `Faz3.1`, which is verified and closed. Rather than edit a file this sub-plan has no write authority over, the rule is restated inline above and binds every measurement in this sub-plan exactly as items 1 through 7 do. **`F4.5-07` may not begin without it, and it is now in force.** The permanent fix — landing item 8 in `docs/phase3-preconditions.md` itself — needs a sub-plan that holds write authority for that file, and remains outstanding for Step 2 to route.

**The `FIND-5.2-01` caveat carries with item 1:** `scripts/smoke.sh`'s `prefs.trap` field disagreed with a direct per-key audit on 2026-08-31. The per-key audit wins, the smoke field is the cross-check, and any disagreement is recorded rather than resolved silently.

Validation identifiers:

- `VAL-CALIBRATE` (from Faz 3.2) — the five-site decode control in F4.5-01. If the known sites do not decode, nothing derived afterwards is trustworthy.
- `VAL-DISASM` (from Faz 1.4) — the scripted disassembly path required by `EV-17`; interactive tools do not complete on this binary.
- `VAL-CHECKSUM` (from Faz 3.3) — the predicted md5 matched on apply and on revert.
- `VAL-ACTIVEARRAY` (proposed) — the `activeArray` field read per camera id from bracketed smoke snapshots, plus the separate `dumpsys` read for vendor tag `80340003`, which the smoke summary does not carry.
- `VAL-METADATA` (from Faz 3.3) — confirmation that `f0006` and the RAW rows at 8192x6144 are unchanged by this work.
- `VAL-SMOKE` (from Faz 2.1) — the bracket itself.
- `VAL-LOG` (from Faz 3.5) — buffers raised and the crash buffer cleared before launch; `static_metadata.cc:667`, `frame_raw_max … matches neither`, and `Stuck shot` counted rather than assumed absent.
- `VAL-CAPTURE` (from Faz 3.5) — resolution read from the JPEG SOF marker, not from a filename or a gallery label.
- `VAL-IMAGE` (proposed) — the `FIND-3.5-01` artifact check: whether the fixed-position black half and the magenta cast are present, described rather than scored.
- `VAL-REVERT` (from Faz 3.5) — the two-stage reversal proven byte-identical in the comparable region.
- `VAL-PRECOND` (from Faz 3.1) — the seven-item contract above.
- `VAL-DOCS` (from Faz 3.2) — the ontology and comprehension updates read back before the session ends.

Local versus live: F4.5-01 through F4.5-06 are entirely host-side and need no device and no user. F4.5-07 onward are live, and F4.5-09 needs the user's shutter press. Security validation is not applicable. Ontology validation is central, since the address book is the artifact being extended and its conventions — recording transcription corrections, distinguishing a `cmp` from its following branch, marking discarded entries rather than deleting them — must be followed.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| agc-50mp-yama/hal-activearray-deneme.patch | proposed | The new patch table for the active-array tags, as four-byte-indexed word replacements with its predicted md5 in the header, following the convention of the two existing tables in this directory. | VAL-CHECKSUM, VAL-ACTIVEARRAY |
| agc-50mp-yama/hal-pixelarray-deneme.patch | existing | The confirmed `f0006` table this work must compose with and must not modify; also the format model the new table follows. | VAL-CHECKSUM, VAL-METADATA |
| agc-50mp-yama/README.md | modified | Record the new table alongside the existing two, with what it changes and against which base md5. | VAL-DOCS |
| scripts/smoke.sh | existing | The bracket, and the `activeArray` field this sub-phase measures on. | VAL-SMOKE, VAL-ACTIVEARRAY |
| Planner-docs/Project-Ontology.md | modified | The address book extended with the `f0000` / `f000a` / `80340003` publication sites, and discarded entries marked per `FIND-3.2-01`. | VAL-DOCS, VAL-DISASM |
| Planner-docs/Project-Comprehension.md | modified | Update `H-03` and the `FIND-3.5-01` state once the image verdict exists. | VAL-DOCS |
| docs/phase3-preconditions.md | existing | The source of the validation contract restated above, and of the attempt budget this sub-phase reports against. | VAL-PRECOND |
| docs/reverse-engineering-toolchain.md | existing | The scripted disassembly procedure and its self-check, required by `EV-17`. | VAL-DISASM, VAL-CALIBRATE |
| docs/patch-table-format.md | existing | The alignment and extension rules the new table must satisfy. | VAL-CHECKSUM |

## 10. Dependencies and Sequencing

Depends on `Faz-3-Plans/Faz3.3-single-word-patch-and-metadata-proof.md` for the calibration reference and the `S` layout derivation, and on `Faz-3-Plans/Faz3.5-agc-capture-and-image-evidence.md` for the three-layer stack, its md5, and the artifact description this sub-plan tests against. Depends on `Faz-1-Plans/Faz1.3-patch-table-format-contract.md` for the table format and on `Faz-1-Plans/Faz1.4-toolchain-procedure-record.md` for the scripted disassembler. Depends on `Faz-2-Plans/Faz2.1-device-smoke-script.md` for the bracket and the metric.

**Blocks `Faz-4-Plans/Faz4.1-fullres-dimension-guard.md`, by `DEC-12`.** Faz 4.1's preservation check is worth taking only against a good capture; run in the other order it would confirm that a half-black frame is still half-black.

Blocks nothing else directly. Faz 4.2, Faz 4.3 and Faz 4.4 sit behind Faz 4.1 and inherit the dependency through it.

Required decisions: whether to attempt `80340003` by a different mechanism if F4.5-05 finds it is not statically patchable. That is routed to the user rather than resolved by the implementer, because it may expand scope beyond a word patch.

Required infrastructure: the device, the module's patch machinery, the scripted disassembler, and a host-side md5 tool.

Required human approvals: applying a HAL patch and restarting the camera, and the shutter press for F4.5-09.

Fresh session token and context risk: **high**. It is a write-site search in a 27 MB stripped binary followed by live measurement, which is the combination `R10` warns about, and it is higher than Faz 4.1's medium banding. The mitigations are the ones that worked in Phase 3: scripted extraction with bounded output, and immediate ontology recording so a truncated session loses momentum rather than findings.

Subagents are not recommended. Main-Planing section 9's reasoning applies unchanged — the work is deep rather than broad and the evidence is concentrated in files the parent already holds. A bounded read-only helper for one mechanical extraction is defensible if the parent's context is nearly exhausted, but the parent owns every ontology write.

## 11. Risks and Mitigations

- Risk: an `f0000` or `f000a` address-book entry is spent as fact and turns out to share the provenance `FIND-3.2-01` identified. Impact: budget consumed on a table interior, and worse, a patch aimed at a tag list rather than a value source. Mitigation: F4.5-02 is a gate rather than a step — no entry may have budget spent on it until it is decoded — and the six known interiors sit inside runs spanning `000f0001` … `000f000a`, so both target tags are presumptively affected.
- Risk (`R4`): the active-array values are runtime-derived with no full-resolution source anywhere in `S`, so no single-word redirection exists. Impact: the P1 fix needs a larger change than the patch format expresses, or none at all. Mitigation: F4.5-04 tests this before any design work, so the answer arrives as a finding rather than as a run of failed patches, and the `f0006` precedent gives a concrete model to test against rather than an open search.
- Risk: `80340003` is published by a vendor-tag provider outside `camera.qcom.so` and is not reachable by this project's patch mechanism. Impact: two of three tags move and the image may still be wrong. Mitigation: F4.5-05 separates it deliberately, the acceptance criteria require an explicit negative rather than silence, and the per-tag measurement in F4.5-08 will show whether the image improves without it.
- Risk: all three tags are patched at once and a failure cannot be localized. Impact: an ambiguous result on the project's P1 item. Mitigation: F4.5-07 requires a single-tag measurement first, and checklist item 3 makes it a contract violation to do otherwise.
- Risk: the raise breaks something the half-size active array was protecting — a consumer that sizes buffers or crops from it. Impact: a regression in the stock camera or in a mode Faz 2.3 recorded as working. Mitigation: `VAL-REVERT` is proven before the session ends, Faz 3.4's consumer survey gives a comparison set, and Faz 4.4 owns the full survey against the final patch.
- Risk: the raise moves the metadata and the image is still corrupt. Impact: `FIND-3.5-01`'s stated cause is wrong and the diagnosis restarts. Mitigation: F4.5-09 reports what the frame looks like rather than a pass or fail, so a partial improvement is legible, and Open Camera's clean capture from the identical state remains the control that the HAL can deliver the image.
- Risk (`AUTOPSY-P1-03`): the search runs past its allowance because each next candidate feels close. Impact: Phase 4's remaining sub-plans lose their resources. Mitigation: the allowance is a number fixed in `DEC-06` and reconciled at eleven by `IMPL-24`, its interpretation is fixed in section 6 of this plan rather than mid-search, and F4.5-10 requires a verdict against it.
- Risk (`R8`): the located addresses are recorded and a system update invalidates the binary. Impact: every offset invalidates together. Mitigation: unchanged project posture — the checksum guard is the detector and the disassembly method is documented so offsets can be re-derived.
- Risk (`R10`): the session exhausts context mid-search and located addresses are lost. Impact: the next session re-derives what was already found, which has happened on this project before. Mitigation: F4.5-10 is a continuous work item, not a closing step, and the acceptance criteria require same-session recording.

## 12. Desired End State

The three active-array tags are consistent with the pixel array they accompany, or the reason one of them cannot be is recorded as a determination rather than as an omission. `f0000` and `f000a` read `[0 0 8192 6144]` on the camera id named in the result, `f0006` still reads `[8192 6144]`, the RAW rows at 8192x6144 are untouched, and the AGC full-resolution capture has an image verdict describing what the frame actually looks like — which is the evidence `FIND-3.5-01` needs to close.

The evidence an implementer should produce is the calibration result, the classification table for the recorded entries, the two publication records, the value-origin answer, the `80340003` determination, the pre-committed md5 and its two matches, the per-tag `activeArray` readings with camera ids, the image verdict, and the reversal diff.

The ledger summary Step 4 should append records: which tags moved and on which camera id, the addresses located and their provenance, whether `S` held a full-resolution rect, the `80340003` verdict, whether the image artifact is gone, the sites consumed against the remaining allowance, and the restored state's checksum.

## 13. Next Sub-Phase Transition Criteria

- At least `f0000` and `f000a` read `[0 0 8192 6144]` on the named camera id, verified from a bracketed smoke snapshot, or the reason they cannot is recorded as a determination with evidence.
- The `80340003` publisher and patchability verdict is stated, including an explicit negative.
- `f0006` and the 8192x6144 RAW rows are verified unchanged, so Faz 4.1 inherits an intact Phase 3 result to preserve.
- The AGC capture carries an image verdict, and `FIND-3.5-01` is explicitly closed or explicitly left open with what was learned attached.
- The reversal is proven byte-identical in the comparable region, so Faz 4.1 begins from a known state.
- Every located address is in Project-Ontology section 6, and every discarded entry is marked rather than deleted.
- The budget verdict against the remaining allowance is stated.
- Faz 4.1 has a capture worth preserving, which is the condition `DEC-12` sequenced this sub-plan to create.
