# Pre-Rental Plan — from the verified staging to the `Faz7.2` rental decision

> **Historical as of 2026-11-13.** The user abandoned the plan to build an
> AOSPA ROM for `ishtar`. The phone now runs HyperOS 4 (`OS4.0.0.44.WMACNXM`,
> Android 17), measured read-only in
> `snapshots/20261113-1819__IMPL96__hyperos4-readonly-probe.txt`. Step 4 will
> not run, and nothing was ever rented. The rest of this file is unchanged and
> stays as the record of what was planned; the ledger records the decision in
> `IMPL-96`.

Written 2026-09-13, after `IMPL-93`. This is an operator plan, not a ClaudeQB
artifact: it orders the work that should happen before the first build-server
rental and says which fresh session does each part. The sub-plans, the audit and
the ledger stay the sources of truth; where this file and they disagree, they win
and this file is corrected.

**Updated 2026-09-14 (`DEC-26`).** The rental-day gate did not pass
(`IMPL-94`), and Hetzner's new-account limit then capped the account at CCX33.
The user moved the rental to Scaleway in a separate conversation. Steps 3a–3c
below re-target the runbook and `Faz7.2` before any rental.

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
| Eleventh Step 3 audit (step 3c, 2026-09-14) | `PASS_WITH_WARNINGS`, no P0/P1, queue READY, head `Faz7.2` | `Planner-docs/Sub-Planing-Audit.md`; supersedes the tenth. Run 20's `Faz7.2` matches the Scaleway runbook value by value. `AUDIT-FIX-52`, `-53`, `-54` resolved in the runbook; new P3 `-55` (stale "correct the symlink test" wording: a verification on the day), `-56` (`VAL-SYNC` graded against `22283d8` plus `fixes.diff`), `-57` (Hetzner wording, three more lines found). 10 active P2/P3 findings |
| `Faz7.2` rental-day gate | run 2026-09-13, not passed | `IMPL-94`: section 5 exited 0, and `AUDIT-FIX-52`, `-53` and `-54` are repaired in the runbook. The 10-hour window did not fit that day, and the limit and SSH key checks were not yet done |
| Rental provider | Scaleway **POP2-32C-128G**, `DEC-26` answered 2026-09-14 (step 3a) | `IMPL-95`: runbook `docs/build-environment.md` re-targeted on sourced Scaleway semantics; Ubuntu 22.04, 10 h ceiling with hour-8 rule, delete everything, no retry after an out-of-memory kill. `Faz7.2` re-targeted to the runbook's values by planning run 20 (step 3b) and audited by the eleventh audit (step 3c). Next: step 4, the rental day |
| `Faz7.3`, `Faz8.3` | queued behind `Faz7.2` | amended by run 19, audited by the tenth audit |
| Workspace | last commit `587e3b5` (step 3a, `IMPL-95`); not pushed | uncommitted: step 3b (planning run 20: `Faz7.2`, the ledger, this file) and step 3c (the audit, this file). A local commit before step 4 gives the rental session a clean tree; the user's call. `devir-teslim-promptu.md` untracked (stale 2026-09-09 handoff, the user's call) |

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
- The **re-target steps 3a–3c** exist for the same reason. A provider change
  alters billing semantics, provisioning, disks and teardown, which are exactly
  the parts a paid session cannot improvise.
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

### Step 2 — Bounded Step 2 amendment (planning run 19, done 2026-09-13)

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

### Step 3 — Tenth Step 3 audit (done 2026-09-13)

- Session: fresh, the canonical `references/handoffs/run-step3.md` handoff.
  Modifies only `Planner-docs/Sub-Planing-Audit.md`.
- Focus: confirm run 19 discharged `AUDIT-FIX-43` … `-51` in the text Step 4 is
  graded against, carry or close the rest, take `IMPL-92` and `IMPL-93` into the
  status table, and rebuild the queue. Expected head: `Faz7.2`.
- Done when: the audit says Step 4 may begin, or names the blocker; the user
  has decided whether to commit locally.

### Steps 3a–3c — Re-target the rental to Scaleway (added 2026-09-14, `DEC-26`)

The handover is kept verbatim, with the checks already made against it, in
`snapshots/20260914-1434__DEC26__scaleway-handover.txt`. `Faz7.2` and runbook
sections 1–3, 5–7, 11 and 12 describe a Hetzner CCX53 and are re-targeted
before any rental.

#### Step 3a — Decisions and runbook re-target (done 2026-09-14, `IMPL-95`)

- **Done.** The existing set was first committed locally as `f724b64`.
  - The user's answers: (a) Ubuntu 22.04, with `DEC-22`'s 24.04 fallback.
  - (b) and (d): the user moved the instance to **POP2-32C-128G** instead of
    retrying on 64 GB. That keeps the 10 h ceiling with the hour-8 rule; an
    out-of-memory kill is a stop.
  - (c): everything is deleted at teardown.
  - Scaleway's pages were read and quoted in runbook section 3. Two points need
    the worse-case design: the Instance API text says `terminate` only detaches
    Block volumes, and the flexible IP survives the Instance. Also found: the
    610 GB needs a validated identity (a 500 GB quota otherwise).
  - Runbook sections 1–13 re-targeted, and every block passes `bash -n`. The
    volume table below stands, apart from its 16-vCPU premise.
- Session: fresh. No rental, no push, and no commit without asking.
- First, the user answers `DEC-26`'s open items (ledger section 8), each with
  the recommendation recorded there:
  - (a) Ubuntu 22.04 (`DEC-22`) or 24.04;
  - (b) the time ceiling on 16 vCPU;
  - (c) whether the source volume survives teardown;
  - (d) whether an out-of-memory kill gets one retry.
- Read Scaleway's own documentation and quote it with links, as runbook
  section 3 did for Hetzner (the `AUDIT-FIX-43` standard):
  - hourly instance billing, and what a stopped instance bills;
  - block volume billing per tier;
  - what deleting an instance does to its attached volumes, from the Console
    and from the API;
  - flexible IPv4 billing and deletion;
  - snapshots.

  Prices are confirmed in the Console, not taken from the handover.
- Rewrite `docs/build-environment.md` against the answers:
  - section 1: the host rows;
  - section 2: a POP2-16C-64G column;
  - section 3: Scaleway's semantics;
  - section 4: the ceiling and hour rule, if (b) changes them;
  - section 5: the manual checks, now the Scaleway quota and the SSH key in the project;
  - section 6: instance and volume creation;
  - section 7: the volume setup below, swap, and the `sysctl` made persistent on 24.04;
  - sections 8–11: the tree at `/android/beryl`, `~/out-pkg` off the boot volume, a `mountpoint` check before the build, and `du` of `.repo`, the tree and `out` recorded after sync and build;
  - section 12: teardown lists zero instances, volumes, flexible IPs and snapshots, unless (c) keeps the source volume.

  Keep the `AUDIT-FIX-52`, `-53` and `-54` repairs, and run `bash -n` on every block.
- Proposed volume layout, 2026-09-14:

| Volume | Size, tier | Mount | Holds |
|---|---|---|---|
| Boot | 40 GB, 5K | `/` | OS, packages, `repo`, `~/logs`, `~/evidence`, a 16 GB swap file |
| Source | 310 GB, 5K | `/android` | `/android/beryl` (`.repo` and the checkout); `/android/pkg`, the retrieval staging behind `~/out-pkg`; ccache only if enabled |
| Work | 260 GB, 15K | `/android/beryl/out` | The build output. Runbook paths stay `out/…`, with no `OUT_DIR` |

  Volumes are identified by their ID and size, never by `/dev/sdX` order, and
  `mkfs` runs only on a volume where `blkid` finds no filesystem. ccache stays
  off for the first build: AOSPA `beryl` needs both `USE_CCACHE` and
  `CCACHE_EXEC`, and a cold cache does not speed up a first build.
- Ledger: record `DEC-26` as answered, plus one implementation row.
- Out of scope: the `Faz7.2` text (step 3b), every other Planner-docs file, and
  any rental.

#### Step 3b — Bounded Step 2 amendment (planning run 20, done 2026-09-14)

- **Done.** Step 3a was first committed locally as `587e3b5`, with the user's approval.
  - `Faz7.2`: an amendment note in section 1, then sections 2–13 wherever a provider fact appears, each value re-read from the
    runbook. It now names POP2-32C-128G, the three Block volumes, the flexible IPv4, Ubuntu 22.04 with the 24.04 fallback, the
    10 h ceiling with the hour-8 rule, and no retry after an out-of-memory kill.
  - `F7.2-01` follows runbook section 5, `F7.2-09` and `VAL-TEARDOWN` follow section 12, and `F7.2-08` stages in `~/out-pkg`.
    Three provider risks were added; no work item was added or removed.
  - Index: not edited. Its provider mentions are the history of runs 17 and 18.
  - Ledger: run 20 row in section 2. Section 4's `Faz7.2` blocker and next action now point at the eleventh audit (the user's
    ruling). Section 6 names Scaleway, and section 7's `DEC-26` input records the discharge.
  - Validators: `--mode step2 --strict` and `--mode step3-preflight --strict` give `error_count=0`, `warning_count=0`,
    `secret_findings=0`, `subplan_count=42`. Not committed.
- Session: fresh. The Step 2 rules and byte rules above, bounded to `Faz7.2`
  plus the index and ledger where they state a live provider fact.
- Replace the CCX53, the Hetzner Console, the Primary IP and 128 GB with the
  re-targeted runbook's values. Teardown and `VAL-TEARDOWN` gain volumes and
  flexible IPs, and `F7.2-01`'s manual checks follow runbook section 5.
- Carried, not edited: `Main-Planing.md` lines 75, 211 and 265 (`R9`) and
  `Project-Comprehension.md` `EV-20` name Hetzner. No phase, objective or
  acceptance signal changes, so this goes to the next Step 1 amendment with
  `AUDIT-FIX-41` and `-42`.
- Gates: as Step 2.

#### Step 3c — Eleventh Step 3 audit (done 2026-09-14)

- **Done.** `PASS_WITH_WARNINGS`, no P0 or P1, queue READY, head `Faz7.2` at `F7.2-01`. Only
  `Planner-docs/Sub-Planing-Audit.md` was written; not committed.
  - Run 20's `Faz7.2` matches runbook `docs/build-environment.md` on every graded value: POP2-32C-128G, the three Block
    volumes, the flexible IPv4, Ubuntu 22.04 with the 24.04 fallback, the 10 h ceiling with the hour-8 rule, no
    out-of-memory retry, section 5's four manual checks, section 12's eight steps and four zero counts,
    `/android/beryl` and `~/out-pkg`. Ten work items before and after; no live Hetzner fact left.
  - Closed, because the runbook carries each repair: `AUDIT-FIX-52` (section 4 sync-path exception), `-53`
    (section 5 base-pin check; the base still read `7dfc0650…` today), `-54` (sections 10 and 11 record and continue,
    plus the operator rule). All ten runbook blocks pass `bash -n`.
  - New, all P3, none needs a decision: `-55`, where `F7.2-01`, section 11 and five more places still say "correct
    the symlink test before renting", and section 6 wrongly says the runbook tests the `odm` path, although
    `IMPL-94` made the correction. On the rental day it is a read-back plus `bash -n`, not an edit. `-56`, where
    `VAL-SYNC` and the resolved-manifest criterion must use `22283d8` as amended by `fixes.diff`, and `DEC-25` item
    (3) lacks the runbook's sync-path exception. `-57`, where the Hetzner wording routed to the next Step 1
    amendment is confirmed, but misses `Project-Comprehension.md` `CQ-13`, `Project-Ontology.md` invariant 11 and
    `docs/reverse-engineering-toolchain.md` line 220.
  - Validators: `--mode step3-preflight --strict` passed; `--mode step3 --strict` and `--mode step4 --strict` give
    `p0_findings=0`, `p1_findings=0`, `secret_findings=0`, `subplan_count=42`, `execution_queue_state=READY`, with the
    expected strict promotion of the P2/P3 warning.
- Session: fresh, the canonical `references/handoffs/run-step3.md` handoff.
- Focus: the step 3b amendment read against the re-targeted runbook; close
  `AUDIT-FIX-52`, `-53` and `-54` if the runbook carries their repairs; rebuild
  the queue. Expected head: `Faz7.2`.

### Step 4 — Rental day: `Faz7.2` gate, then the paid session

- **Status:** first run 2026-09-13 as `IMPL-94`, gate not passed. Waits for
  steps 3a–3c.
- Session: fresh, the canonical `references/handoffs/run-step4.md` handoff,
  limited to `Faz7.2`, started on a day with the full time window free.
- Part A, free: `F7.2-01`. Run `docs/build-environment.md` section 5 as
  written, including the base-pin check. The user confirms in the provider
  console: the instance quota, the public SSH key, the
  `~/Documents/Projeler/ishtar-builds/` output directory outside every repository
  (created 2026-09-13), and the time window. Re-read the budget and stopping
  rule (`DEC-25` as amended by `DEC-26`, runbook section 4).
- **Stop for the user's rental approval.** Without it, the session records the
  gate result and ends.
- Part B, paid, only after approval: runbook sections 6 to 13 in order,
  teardown whatever the outcome. `Faz7.3` does not start in this session.

## 4. Optional at any checkpoint

- Push to the private `origin` (`ahmetxa/ishtar`) as an off-machine copy
  before the paid session. The user's decision.
- Commit the uncommitted run 19, tenth audit, `IMPL-94` and `DEC-26` records
  locally. The user's decision.
- Decide what to do with `devir-teslim-promptu.md`: keep untracked, delete, or
  rewrite. It describes the 2026-09-09 state (WSL2, `IMPL-88` next) and should
  not be used as a handoff.
