# Pre-Rental Plan — from the verified staging to the `Faz7.2` rental decision

Written 2026-09-13, after `IMPL-93`. This is an operator plan, not a ClaudeQB
artifact: it orders the work that should happen before the first Hetzner rental
and says which fresh session does each part. The sub-plans, the audit and the
ledger stay the sources of truth; where this file and they disagree, they win
and this file is corrected.

**Rule for every session below.** One step per fresh chat window. Each session
starts by reading this file and `git status`, does only its own step, and ends
by reporting what it changed. If its step completed as expected and it has no
questions or suggestions for the user, it then writes the start prompt for the
next step. Nothing is pushed and nothing is rented without the user's explicit
approval in that session. No token, key, password or server address is written
anywhere.

## 1. Where things stand

| Item | State | Record |
|---|---|---|
| `Faz7.1` GitHub input staging | verified | `IMPL-91`; manifest `22283d8`, both repositories public (`DEC-25`); runbook `docs/build-environment.md` |
| `Faz8.1` static half | done, sub-plan `implemented` | `IMPL-92`; both camera layers carry-over at vendor pin `f92e7a9` |
| `Faz8.2` kernel scoping | verified | `IMPL-93`; `DEC-08` recommendation defer |
| Ninth Step 3 audit | `PASS_WITH_WARNINGS`, no P0/P1 | `Planner-docs/Sub-Planing-Audit.md`; 15 active P2/P3 findings |
| `Faz7.2` paid build | queued, not started | the next implementation row |
| `Faz7.3`, `Faz8.3` | queued, blocked in practice | need the bounded amendment for `AUDIT-FIX-45` and `-46` first |
| Workspace | committed locally | checkpoint `097d687`; not pushed; `devir-teslim-promptu.md` untracked (stale 2026-09-09 handoff, the user's call) |

## 2. Why these steps, in this order

- The **checkpoint commit** separates weeks of verified planning and staging
  from what follows, and gives later Step 4 sessions a clean tree, which their
  run contract requires.
- The **bounded Step 2 amendment** fixes plan text before it is executed. The
  ninth audit asked for it "after `Faz7.1` closes and before anything is
  rented". It also has one reason the audit could not see: `Faz7.2` was written
  before `IMPL-91` and still describes manifest `4182695`, seven open items,
  private repositories and a server credential. The runbook has since replaced
  all of that (public repositories, no credential, `./rom-build.sh ishtar -z`,
  sections 3, 5, 10, 11 and 12). A rental session graded against stale text
  either stops on a false contradiction or improvises.
- The **tenth Step 3 audit** is required because sub-plans change. Step 4 must
  not run against an audit of text that no longer exists.
- The **rental-day session** runs `Faz7.2`'s own pre-rental gate on the day,
  as the runbook requires, and stops for the user's approval before money is
  spent.

## 3. Steps

### Step 1 — Checkpoint commit and this plan (done 2026-09-13)

- Session: the one that ran `IMPL-92` and `IMPL-93`.
- Done: `097d687` commits planning runs 17 and 18, the ninth audit, and
  `IMPL-91`, `IMPL-92` and `IMPL-93`. The set was checked before committing:
  no token, key or address pattern (the one IPv4-shaped string is the version
  `3.3.0.0`, already in history), no binary other than the Ontology's two
  known NUL bytes, and `.gitattributes` `* -text` keeps every byte. This file is
  committed separately after it.
- Not done on purpose: no push to the private `origin` (`ahmetxa/ishtar`);
  `devir-teslim-promptu.md` left untracked.

### Step 2 — Bounded Step 2 amendment (planning run 19)

- Session: fresh. ClaudeQB Step 2 rules (`references/Second-Planner.md`),
  **bounded**: no phase is re-decomposed, no sub-plan created or deleted, the
  set stays at 42. The style follows planning runs 13 to 15: an amendment note
  in section 1 plus edits to exactly the sections a finding touches, above all
  the sections Step 4 is graded against (4, 7, 8, 9, 13).
- Each finding's required action is taken verbatim from
  `Planner-docs/Sub-Planing-Audit.md` section 13 and its row in section 12, then
  checked against the repository before it is written.

| File | What changes | Driver |
|---|---|---|
| `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md` | Reconcile with `IMPL-91` and the runbook: manifest `22283d8` and the closed/deferred open items (section 6); no server credential under `DEC-25` (`F7.2-03`, `F7.2-09`, section 10, `VAL-TEARDOWN`); the build command the runbook names; `F7.2-01` = runbook section 5 plus its manual checks; `F7.2-08` retrieves every artifact in runbook section 11 with sha256, or records local extraction; `F7.2-09` follows runbook section 3; `F7.2-07`'s md5s feed `F8.1-06`. Every value is re-read from the runbook and the manifest repository, not from this table. | `IMPL-91` drift, `AUDIT-FIX-43`, `-44` |
| `Planner-docs/Faz-7-Plans/Faz7.3-flash-boot-and-aon-verification.md` | Data-format requirement for 15 → 16 and 16 → 15; return path with re-root, v2.2 reinstall, AGC re-configuration and trap audit if a wipe is needed; wipe stated at `F7.3-02`; `F7.3-07` graded against the re-established state. | `AUDIT-FIX-45` |
| `Planner-docs/Faz-8-Plans/Faz8.1-android16-camera-blob-comparison.md` | Adaptation routed like re-derivation; transition criterion requires sensor carry-over; scratch outside the workspace, deleted at the end of the static half; both Android 15 candidates named in `F8.1-04`. Record that the static half ran as `IMPL-92` without rewriting that record. | `AUDIT-FIX-46`, `-47`, `-49` |
| `Planner-docs/Faz-8-Plans/Faz8.3-camera-modes-on-android16-build.md` | Gate on HAL **and** sensor carry-over; PC-17 on `prefs.trap.armed`, PC-04 on the repaired probe; `VAL-RESTART` lists `init.svc.*` and adds "switch has no effect" as a failure signal. | `AUDIT-FIX-46`, `-50`, `-51` |
| `Planner-docs/Sub-Planing-Index.md` | Section 4d static-half boundary; section 5 deferred list gains sensor adaptation; section 7's line-ending sentence says LF. | `AUDIT-FIX-46`, `-47`, `-48` |
| `Planner-docs/Planing-Ledger.md` | Run 19 row in section 2; `IMPL-89` annotated as corrected by `IMPL-90`; section 4 next actions only where the amendment changes them; snapshot decision by the runs 13–15 precedent, stated either way. | `AUDIT-FIX-49`, continuity |

- Out of scope: `Main-Planing.md` (`AUDIT-FIX-41`, `-42` wait for a Step 1
  amendment); `Project-Ontology.md` (`-22`); `Project-Comprehension.md`
  (`-37`); `docs/release-checklist.md` (`-50`'s document half is Step 4 work);
  `Faz7.1` and `Faz8.2`; any source file, device, rental or push.
- Byte rules: sub-plans and the index are LF. The ledger is CRLF: edit it as
  bytes, assert each anchor unique, keep every table row's pipe count (a `|`
  inside backticks still splits a cell).
- Gates: validator `--mode step2 --strict` and `--mode step3-preflight
  --strict` give `error_count=0`, `warning_count=0`, `secret_findings=0`,
  `subplan_count=42`; every edited section read back. Stop and ask if a repair
  needs a new decision or contradicts a measured fact.
- Done when: the six files above are amended, the validators pass, and the
  user has decided whether to commit locally.

### Step 3 — Tenth Step 3 audit

- Session: fresh, the canonical `references/handoffs/run-step3.md` handoff.
  Modifies only `Planner-docs/Sub-Planing-Audit.md`.
- Focus: confirm run 19 discharged `AUDIT-FIX-43` … `-51` in the text Step 4 is
  graded against, carry or close the rest, take `IMPL-92` and `IMPL-93` into the
  status table, and rebuild the queue. Expected head: `Faz7.2`.
- Done when: the audit says Step 4 may begin, or names the blocker; the user
  has decided whether to commit locally.

### Step 4 — Rental day: `Faz7.2` gate, then the paid session

- Session: fresh, the canonical `references/handoffs/run-step4.md` handoff,
  limited to `Faz7.2`, started on a day with the full 10-hour window free.
- Part A, free: `F7.2-01`. Run `docs/build-environment.md` section 5 as
  written. The user confirms in the Hetzner Console: the CCX53 limit, the
  public SSH key, the `~/Documents/Projeler/ishtar-builds/` output directory
  outside every repository, and the time window. Re-read the budget and
  stopping rule (`DEC-25`, runbook section 4).
- **Stop for the user's rental approval.** Without it, the session records the
  gate result and ends.
- Part B, paid, only after approval: runbook sections 6 to 13 in order,
  teardown whatever the outcome. `Faz7.3` does not start in this session.

## 4. Optional at any checkpoint

- Push to the private `origin` (`ahmetxa/ishtar`) as an off-machine copy
  before the paid session. The user's decision.
- Decide what to do with `devir-teslim-promptu.md`: keep untracked, delete, or
  rewrite. It describes the 2026-09-09 state (WSL2, `IMPL-88` next) and should
  not be used as a handoff.
