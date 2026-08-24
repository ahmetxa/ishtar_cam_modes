# Faz 1.3 — Patch Table Format Contract

## 1. Context

Main-Planing section 5 names the patch table as an architectural strength: "Patch tables carry the md5 of both the stock input and the patched result, which makes them self-verifying. This convention should be extended to every binary the project touches, including sensor blobs."

Autopsy agrees and sharpens it into a gap. Section 6 ("Missing contracts and schemas") observes that the format "is excellent but undocumented as a format — its grammar exists only implicitly in the two files that use it and in the parser inside `halpatch.sh`". The finding is filed as `AUTOPSY-P2-04`, with the note that the format "is the project's most reusable invention".

Two Phase 4 outcomes depend on this being written down. Faz 4.1 narrows the RAW emission and Faz 4.2 adds duration rows, and both produce new patch entries. Faz 4.3 merges the experimental table into the canonical one. Extending a format safely requires knowing what the format guarantees, and right now that knowledge lives in one 116-line shell script's `hal_write` loop.

## 2. Goal

Produce a written format contract for the patch table that states its grammar, its verification model, its atomicity properties, and its extension rules precisely enough that a second implementation could be written from the document alone.

## 3. Description

The problem this solves is knowledge that is correct but not transferable. The format works, and the two files that use it are internally consistent, but nothing states which properties are load-bearing and which are incidental. A future edit — adding a comment style, changing an offset base, appending a third byte column — cannot be evaluated as safe or unsafe without reading the parser.

It belongs in Phase 1 because Phase 4 will extend the format and Phase 9 will validate artifacts against it, and both are cheaper if the contract exists first. It reduces risk by converting an implicit invariant into a checkable one.

The vibecoding slice strategy: the first useful slice is a single document derived from reading `halpatch.sh` and the two existing tables, written against the evidence rather than from memory. The fastest validation signal is a round-trip check — take the documented grammar, apply it by hand to three lines of `hal-fullres.patch`, and confirm the described byte writes match what the parser would do.

What not to over-plan: a formal grammar notation, a validating parser, or a schema file. The document is the deliverable; tooling around it is Phase 9 material and only justified once a second table generator exists.

An open question this sub-phase should answer rather than defer is `OQ-05` in Project-Ontology section 8 — "Is patch application atomic against power loss mid-write?" The answer is derivable from `halpatch.sh` and is recorded in Faz 1.5's probe batch; this sub-phase consumes that answer and states it as a documented property.

## 4. Scope

- The grammar: comment lines, the three-column record form, the meaning of the index column, and the escape encoding of the two byte columns.
- The verification model: which md5 values are recorded, what each guards, and the order in which size and checksum checks run.
- The write model: that entries are applied to a module-private copy under `active_hal/`, not to the live target, and that the live target is exposed by bind mount.
- The atomicity property, stated from the evidence rather than asserted.
- The extension rules: what may be added to a table without breaking existing consumers, and what constitutes a breaking change.
- The naming and location convention for tables, resolving where an experimental table lives versus a canonical one.
- Applicability to sensor blobs, which are currently whole-file replacements guarded only by an expected size.

## 5. Out of Scope

- Writing a parser, validator, or generator for the format. Tooling is Phase 9.
- Changing `halpatch.sh` behavior. This sub-phase documents what exists; Faz 4.3 is where table content changes.
- Deriving new offsets or modifying either existing table's entries.
- Converting sensor blobs to a patch-table representation. The document notes the opportunity; acting on it is a separate decision with its own cost.
- Specifying a release manifest binding a version to a set of md5 values — that is Faz 9.2.

## 6. Current Repository Evidence

`ishtar-cam-modes/halpatch.sh` (116 lines) was read in this run and contains the complete parser. `hal_write` reads the table with `while read -r idx es ep`, skips blank lines and lines beginning with `#`, skips records with an empty third column, selects the stock or patched column by argument, and writes with `printf '%b' "$e" | dd of="$HAL_ACT" bs=4 seek="$idx" count=1 conv=notrunc`.

The header comments in the same file record a measured negative finding that belongs in the contract: byte values were originally produced by nested command substitution (`printf "\\$(printf '%03o' $b)"`), which did not resolve under toybox `sh` and corrupted 288 bytes instead of writing 16 points. The current single `printf '%b'` form is a correctness requirement, not a style preference.

`ishtar-cam-modes/blobs/hal-fullres.patch` (27 lines) states its own format in Turkish header comments: `<4bayt-indeksi> <stok-escape> <yamali-escape>`, with the index defined as `byte_offset / 4` and a note that the escape sequences are used verbatim by `printf '%b'` with no nested substitution. It records `stok md5 c3fa63a86ee3ecaf9fbf02005d35f6b5`, `fullres md5 fe0245a4720fb07b01d96deef47f5569`, and `nokta 16`, followed by 16 records.

`agc-50mp-yama/hal-raw50-deneme.patch` (28 lines) uses the same grammar with a different base: `temel: fullres md5 fe0245a4720fb07b01d96deef47f5569` and `sonuc: md5 8d0915ce520fadaf092d31ed675aa98a`. This is the important structural fact — the second table chains from the first table's output rather than from stock, so the two are ordered, not independent.

`halpatch.sh` defines `HAL_SIZE=27268688`, `HAL_STOCK_MD5`, and `HAL_FULLRES_MD5` as script constants that duplicate values also present in the table header. That duplication is a real contract question the document must resolve: which copy is authoritative.

`hal_set` verifies the resulting md5 after writing and re-seeds from the device's stock binary when `hal_state` reports `unknown` or `none`, which means a partially written copy is detected and discarded rather than mounted.

## 7. Planned Work Breakdown

- F1.3-01 — Transcribe the grammar from the parser
  - Description: State each lexical rule as implemented in `hal_write`, including the skip conditions for comments, blank lines, and short records.
  - Output: A grammar section with one rule per parser behavior.
- F1.3-02 — Document the index convention and its rationale
  - Description: Record that the index is a four-byte unit, that it exists because seeking 23 million single bytes is avoidable, and that it constrains every patch site to a four-byte alignment.
  - Output: An index-convention section naming the alignment constraint as a limitation of the format.
- F1.3-03 — Document the escape encoding and its measured failure mode
  - Description: State that byte columns hold ready-made octal escape sequences consumed by a single `printf '%b'`, and record why nested command substitution is forbidden, citing the 288-byte corruption measured under toybox.
  - Output: An encoding section with the negative finding preserved.
- F1.3-04 — Document the verification and chaining model
  - Description: State that a table records the md5 of its input and of its result, that `hal-raw50-deneme.patch` chains from `hal-fullres.patch`'s output, and that chaining implies an application order.
  - Output: A verification section including a chain diagram note.
- F1.3-05 — Resolve the duplicated constant question
  - Description: Decide whether `halpatch.sh`'s `HAL_STOCK_MD5` and `HAL_FULLRES_MD5` constants or the table headers are authoritative, and state how they are kept consistent.
  - Output: A single-source-of-truth rule for checksum constants.
- F1.3-06 — State the atomicity property from evidence
  - Description: Record that writes target a module-private copy rather than the live binary, that a partial write leaves an `unknown` state detected by `hal_state`, and that recovery is a re-seed from the device's stock binary. Cite the Faz 1.5 probe that reads `halpatch.sh` for this purpose.
  - Output: An atomicity section that answers `OQ-05` rather than restating it.
- F1.3-07 — Write the extension and location rules
  - Description: Define what a compatible extension looks like, what makes a change breaking, and where canonical versus experimental tables live. This rule is what Faz 4.3 will act on when relocating the experimental table.
  - Output: Extension rules and a location convention.
- F1.3-08 — Assess applicability to sensor blobs
  - Description: Note that sensor blobs are whole-file replacements guarded by `EXPECT_SIZE=1062250` with no md5 pair, and state what extending the convention would require. Do not implement it.
  - Output: A short applicability assessment with the cost named.

## 8. Acceptance Criteria

- The document states every parser behavior present in `hal_write`, including the three skip conditions.
- The four-byte index convention is documented together with the alignment constraint it imposes on future patch sites.
- The nested-substitution failure is recorded with its measured consequence, so it is not reintroduced.
- The chaining relationship between the two existing tables is stated explicitly, including that the experimental table's base is the first table's output md5.
- The duplicated checksum constants have a named authoritative source and a stated consistency rule.
- The atomicity section answers `OQ-05` with evidence from `halpatch.sh` rather than leaving it open.
- The location convention is specific enough that Faz 4.3 can apply it without further interpretation.
- A hand round-trip of at least three records from `hal-fullres.patch` reproduces the byte writes the documented grammar predicts.

## 9. Validation and Test Approach

Validation is document-level with one manual round-trip check. No device and no build are involved.

- `VAL-DOCS` (proposed) — read the document against `halpatch.sh` line by line; confirm every parser behavior is represented and no behavior is described that the parser does not have.
- `VAL-ROUNDTRIP` (proposed) — take three records from `hal-fullres.patch`, apply the documented grammar by hand, and confirm the predicted byte offset and byte values match what `dd bs=4 seek=<idx>` with the given escape would write. This is the cheapest available proof that the document is correct rather than merely plausible.

Local smoke, live readiness, CI, and security validation are not applicable to this sub-phase. Ontology consistency is relevant: the document must use the Project-Ontology vocabulary, keeping `fullres` as a HAL state and `50mp` as a mode name.

| Path | State | Purpose | Validation Command IDs |
|---|---|---|---|
| ishtar-cam-modes/halpatch.sh | existing | The authoritative parser the contract is transcribed from. | VAL-DOCS, VAL-ROUNDTRIP |
| ishtar-cam-modes/blobs/hal-fullres.patch | existing | Canonical table; source for the round-trip check and the chaining model. | VAL-ROUNDTRIP |
| agc-50mp-yama/hal-raw50-deneme.patch | existing | Chained experimental table; evidence for the ordering property. | VAL-DOCS |
| docs/patch-table-format.md | proposed | The format contract this sub-phase produces. | VAL-DOCS, VAL-ROUNDTRIP |

## 10. Dependencies and Sequencing

Depends on Faz 1.1 only in the weak sense that writing a new document into an unversioned tree is less safe than into a versioned one. It does not depend on Faz 1.2.

Consumes one output from Faz 1.5: the `halpatch.sh` read that answers `OQ-05`. If Faz 1.5 has not run, this sub-phase performs that read itself and Faz 1.5 records the result rather than repeating it.

Feeds Faz 4.3 (table consolidation and relocation) and Faz 9.1 (release build assertions). Faz 4.3 should not begin before this document exists, because relocating a table without a stated location convention is how the artifact ends up in a third arbitrary place.

Required decisions: the authoritative-constant question in F1.3-05 is a judgment call the implementer can make and record; it does not need the user.

Required credentials, infrastructure, or approvals: none.

Fresh session token and context risk: low. Two small files and one 116-line script. Subagents are not recommended.

## 11. Risks and Mitigations

- Risk: the document describes the format as intended rather than as implemented. Impact: a future extension is written against the document, fails against the parser, and the document is blamed last. Mitigation: `VAL-DOCS` compares against `halpatch.sh` line by line and `VAL-ROUNDTRIP` proves at least three records.
- Risk: the four-byte alignment constraint is documented as a convenience rather than a constraint. Impact: Phase 4 derives a patch site at a non-aligned offset and discovers the limitation late. Mitigation: F1.3-02 states it as a constraint that any new site must satisfy.
- Risk (`AUTOPSY-P2-04` residual): the document is written and then diverges as Phase 4 extends the tables. Impact: the contract becomes another stale artifact alongside the superseded journal conclusions. Mitigation: Faz 4.3's acceptance criteria require the contract to be updated in the same slice that changes the tables.
- Risk: the chaining relationship is documented but the ordering requirement is not enforced anywhere. Impact: someone applies the experimental table to a stock binary and the md5 check fails confusingly. Mitigation: the verification section states the base md5 as a precondition, which is exactly what `hal_set` already checks.
- Risk: the sensor-blob applicability note is read as a commitment. Impact: unplanned work enters Phase 4 or 5. Mitigation: F1.3-08 states the cost and explicitly does not implement.

## 12. Desired End State

A written contract exists for the patch-table format that a second implementer could work from without reading `halpatch.sh`. It states the grammar, the index convention and its alignment constraint, the escape encoding and the failure it guards against, the md5 verification and chaining model, the authoritative source for checksum constants, the atomicity property with `OQ-05` answered, the extension and location rules, and an honest assessment of extending the convention to sensor blobs.

The evidence an implementer should produce is the document itself plus the three-record round-trip result.

The ledger summary Step 4 should append records: the contract path, which open question it closed, and which downstream sub-plans now have their precondition satisfied.

## 13. Next Sub-Phase Transition Criteria

- The contract document exists and passes the line-by-line comparison against the parser.
- The round-trip check reproduces the predicted writes for at least three records.
- `OQ-05` is answered in Project-Ontology section 8 with the evidence cited.
- The location convention is specific enough to place `hal-raw50-deneme.patch` without further debate.
- No table content has been modified in this sub-phase.
