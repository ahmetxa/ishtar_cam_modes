# Phase 3 preconditions, budget, and per-measurement checklist

Produced by **Faz 3.1**. This is the entry gate for Phase 3. Every sub-plan from
`Faz 3.2` to `Faz 3.6` references section 5 by name before recording any result.

Phase 3 is a sequence of single-variable experiments against a closed 27 MB
binary. A single-variable experiment is only valid if everything else is known
and held. This document is what makes "everything else" checkable.

## 1. Preference trap state

`Project-Ontology` invariant 8: `pref_raw_key_N` and `pref_fix_resolution_key_N`
independently break Gcam initialization by triggering the port's
`getFixResolutionList` width-cap. `EV-13` records the cost: reverting the HAL,
then the APK, did not fix it — deleting the preferences did.

**The family is twelve keys, not ten.** `Faz3.1` section 8 says "ten"; its own
section 6 enumerates twelve, and twelve is correct: a bare key plus `_0`..`_4`
for each of the two families. The audit below covers all twelve.

### Audit results, 2026-08-31 (`VAL-PREFS`)

| Run | When | Result |
|---|---|---|
| 1 — before clearance | after Faz 5.2 restore | **0 / 12 set** |
| 2 — after clearance | no clearance needed | **0 / 12 set** |
| 3 — after app restart | AGC force-stopped, relaunched, force-stopped | **0 / 12 set** |

Files audited: `org.codeaurora.snapcam_preferences.xml` (5,851 B) and
`primes.xml` (460 B), the only two in `shared_prefs/`.

**Run 3 is the informative one. AGC does not self-arm the trap.** It was
launched from a genuinely empty preference state — it had rebuilt its
preferences from scratch during `IMPL-15`, showing its first-run dialog — and
wrote none of the twelve keys. The trap is therefore a residue of *manual
configuration or a `.agc` import*, never something the app produces on its own.

### The clearance procedure, for when it is needed

Not executed this run because nothing was set. Recorded so it exists before it
is needed:

```sh
adb shell su -c "am force-stop org.codeaurora.snapcam"
# remove the two key families from every shared_prefs xml
adb shell su -c "sed -i -E '/name=\"(pref_raw_key|pref_fix_resolution_key)(_[0-9])?\"/d' \
    /data/data/org.codeaurora.snapcam/shared_prefs/*.xml"
adb shell su -c "sh /data/local/tmp/prefaudit.sh"     # run 2: expect 0/12
adb shell "monkey -p org.codeaurora.snapcam -c android.intent.category.LAUNCHER 1"
# wait for the camera to settle, force-stop, then audit again
adb shell su -c "sh /data/local/tmp/prefaudit.sh"     # run 3: expect 0/12
```

A one-shot clearance is not sufficient on its own — run 3 exists because a
preference rewritten on startup would defeat it. Deleting the whole preferences
file also works and is what `EV-13` did, at the cost of every other AGC setting.

### The `.agc` files re-arm the trap

Verified by key name on 2026-08-31: **both** root configuration files contain
**all twelve** key names.

| File | Bytes | Trap key names present |
|---|---|---|
| `12mpx_agc_config.agc` | 109,074 | 12 / 12 |
| `50mpx_agc_config.agc` | 111,474 | 12 / 12 |

**Importing either file re-arms the trap.** This warning is recorded in two
operator-facing places, as `F3.1-03` requires: here, and in the artifact
manifest of `README.md`, which is where an operator looks before using a
root-level file.

## 2. Entry precondition verdicts

Each verified against its producing sub-phase's evidence, not from the artifact
merely existing (`VAL-PRECOND`).

| # | Precondition | Verdict | Evidence |
|---|---|---|---|
| 1 | Version control exists, tree clean | **PASS with one condition** | `main`, 15 commits. The tree carries this session's own uncommitted Faz 5.1 / 5.2 output. Commit it and the condition clears; nothing else is dirty. |
| 2 | Faz 1.4 disassembly self-check | **SPLIT — see below** | The four `cmp` sites verified 4/4 against the live binary. The tooling for Faz 3.2's search is **absent**. |
| 3 | Faz 2.2 baseline exists and is named | **PASS** | `BASELINE-2026-08-31-V21`, `snapshots/20260831-1607__faz2.2__post-flash-v2.1-baseline.txt`. |
| 4 | Faz 2.3 regression record, no unrouted failures | **PASS** | `docs/regression-v2.1.md`, 121 table rows, ten mode rows. All six findings (`FIND-2.3-01`..`-06`) carry an explicit route. |

### Precondition 2 in detail

**The named check passes.** The live HAL was pulled (md5
`c3fa63a86ee3ecaf9fbf02005d35f6b5`, 27,268,688 bytes — stock) and the four
`cmp wN,#2` sites decoded directly from their instruction encodings:

| Address | Word | Decodes as |
|---|---|---|
| `0x16C18DC` | `0x7100097F` | `cmp w11, #2` |
| `0x16C1C18` | `0x710008FF` | `cmp w7, #2` |
| `0x16C22BC` | `0x71000A9F` | `cmp w20, #2` |
| `0x16C2330` | `0x71000A9F` | `cmp w20, #2` |
| `0x16C2334` | `0x540003E3` | `b.lo` — **not** a `cmp` |

The last row confirms the ontology's own warning that `0x16C2334` is the
following branch and not a fifth patch site. The address book is intact against
the current vendor build.

**The capability does not.** `capstone` and `pyelftools` are **not installed** —
`docs/reverse-engineering-toolchain.md` lines 24-25 already record this, and it
is confirmed by import. The four-site check above needed no disassembler because
a known encoding can be compared directly; **Faz 3.2 cannot work that way.** Its
search is open-ended over nine `movz`/`movk` references and six rodata dwords,
which requires real disassembly.

> **Faz 3.2 is blocked until `pip install capstone pyelftools` is run.**
> This is a one-command fix on the installed CPython 3.14.7. It is recorded as a
> precondition failure rather than performed here, because `Faz3.1` section 5
> places all disassembly in `Faz 3.2`.

### The AGC build the phase measures against

`Faz3.1` section 8 expects the baseline to show neither the experimental HAL
patch nor the patched APK applied. Half of that holds:

| Artifact | State | Matches expectation? |
|---|---|---|
| Experimental RAW50 HAL patch | **not applied** — live HAL md5 equals `HAL_STOCK_MD5` | yes |
| AGC APK | **patched build installed**, `ce65f862c990e2acc02be356f75a7122` | **no** |

The expectation is inherited from Autopsy section 4 and is **stale**: the
patched AGC has been installed since before `IMPL-12`, and `README.md` records
it. **Decision (user, 2026-08-31): keep the patched build.** Phase 3 therefore
measures against a patched AGC, and every measurement in the phase is attributed
against that build, not against stock.

Consequence to carry: `FIND-2.3-03`'s cheapest control — installing
`AGC8.4.300_V9.6_snap.apk`, md5 `fa4066eb3bf82cc097906fd108073500` — is
deliberately **not** taken yet. If a Phase 3 result depends on AGC's own
behaviour rather than on the HAL, that control becomes the next step.

## 3. Attempt budget for the Faz 3.2 write-site search

`AUTOPSY-P1-03`: "Phase 3 has no stop condition … without a bound, the token
budget and the session both run out before a decision is reached." A bound
agreed after a search has begun is not a bound, so it is fixed here, in numbers,
before `Faz 3.2` starts.

> **Budget, agreed with the user on 2026-08-31:**
> **15 candidate sites, across at most 2 implementation sessions.**

The 15 are exactly the addresses already recorded in the ontology address book
for tag `f0006` — nine `movz`/`movk` references (`0x004fe984`, `0x004fee94`,
`0x004ffa5c`, `0x00d9ae24`, `0x00d9ae80`, `0x013b192c`, `0x013b1994`,
`0x013b1a08`, `0x013b1a7c`) and six rodata dwords (`0x0002c6ac`, `0x0038964c`,
`0x003969b4`, `0x00396adc`, `0x00397fcc`, `0x0039c1f0`).

The budget is exhaustive over that recorded set, which is what makes it a real
bound rather than a guess: it either locates the write site, or it **proves the
recorded set does not contain it**. Both are answers, and the second is worth
having — it would redirect the search rather than extend it.

**On exhaustion, `Faz 3.6` runs. It is a scheduled gate, not a fallback invoked
at the implementer's discretion.**

## 4. Fallback options for Faz 3.6

Enumerated here so the gate chooses among defined options instead of improvising
under pressure. `Faz 3.1` does not choose; `Faz 3.6` does.

| Option | Cost | Risk |
|---|---|---|
| **A — Accept the application-level patch as the answer.** The smali patch already defeats the `getOutputSizes` bucketing that was the original 12.6 MP ceiling. | Lowest. The patched APK is already installed and working. | The 50 MP path stays app-specific: it works in this AGC build and nothing else. Every AGC update re-costs the patch. Does not touch the Gcam `pixelArraySize` wall, so `libgcam` still rejects a 50 MP raw frame. |
| **B — Move the active array instead of the pixel array.** Both currently read `[4096 3072]`, so either side of invariant 6 is a candidate. | Medium — a different write site, same search method. | **Known to break AGC when raw is not raised with it.** The Faz 4 attempt raised the active array without raising raw; `agc-50mp-yama/hal-raw50-deneme.patch` records the mirror failure from the other direction. Invariant 6 requires both sides to move together, so this is not a cheaper path — it is the same problem with a different name. |
| **C — Defer Phase 3.** Bank Phase 5's proven result and spend the remaining budget on Phase 4 narrowing and Phase 9 release work. | Zero now; the phase's cost returns later. | The project's headline goal — 50 MP inside AGC — stays unmet. Mitigated by the fact that **OpenCamera already captures 8192x6144 unaided**, so the capability exists on the device today; only the AGC path is blocked. |

Option C is stronger than it was before 2026-08-31: `IMPL-15` proved the 50 MP
HAL layer composes with a DCG sensor layer and produced a clean 50.3 MP capture
through OpenCamera. The device's 50 MP capability is demonstrated. What Phase 3
buys is that capability *inside AGC specifically*.

## 5. Per-measurement checklist

**Every Phase 3 sub-plan runs this before recording any result.** Referenced by
name as "the Faz 3.1 per-measurement checklist".

1. **Preferences clear.** Audit all twelve trap keys; expect 0/12. Do not accept
   a single `scripts/smoke.sh` reading as proof — see the caveat below.
2. **Bracket taken.** `scripts/smoke.sh -o <UTC>__<subplan>__<label>` before the
   change, and again after. Commit both.
3. **One variable.** Exactly one of {sensor layer, HAL layer, APK, preference}
   changed since the previous snapshot. If two moved, the measurement is not
   attributable — redo it.
4. **Metadata republished.** `FIND-2.3-01`: an identical blob advertised RAW
   format 37 at 16:51 and 38 at 16:55. **Any measurement that reads advertised
   metadata after a mode change must first establish that the metadata
   republished** — confirm the stream-config count moved to its expected value,
   or that `wait_camera_list` completed, before reading a row. Read RAW rows
   **per resolution**, never collapsed to one value per mode.
5. **Restorable.** The previous state can be restored by a named command, and
   the restore is verified by snapshot diff, not assumed.
6. **Addresses recorded immediately.** Main-Planing `R10` and `QAS-03`: every
   located binary address goes into `Project-Ontology.md` **in the session it is
   found**, not at session end. Address-book values have been lost to context
   truncation before.
7. **Attribution stated.** The result names the AGC build it was measured
   against — currently the **patched** `ce65f862…`, not stock.

### Caveat on the smoke script's preference field

`scripts/smoke.sh` reports `prefs.trap.count` / `prefs.trap.keys`. Its grep is
well-formed — `sh_root` (line 49) wraps the probe in single quotes, so the `-E`
alternation survives — but on 2026-08-31 it reported `count = 2` with bare key
names at 19:06, while a direct per-key grep minutes later returned **0** with
the preferences file at 0 bytes, and the script itself reported `0` at 19:20.
That is `FIND-5.2-01`, still open.

**Therefore: item 1 is satisfied by the per-key audit, with the smoke field as a
cross-check, not the reverse.** When the two disagree, the per-key audit wins
and the disagreement is recorded.

The audit script used this run reports key names only and never values:
`for k in <twelve keys>; do grep -c "name=\"$k\"" shared_prefs/*.xml; done`.
