# Consumer Compatibility Survey — `pixelArraySize` raised to 8192x6144

Faz 3.4. Answers `OQ-03`: *can `pixelArraySize` be raised without breaking other
consumers?* The answer must name the consumers actually tested, so this file is
built as a table with a stated scope rather than a verdict sentence.

> **Status: F3.4-01 complete, F3.4-02 … F3.4-08 not started.**
> The pre-change column below is finished and sourced. The post-change column is
> deliberately empty — filling it requires the device, the patch re-applied, and
> the user's hands. Do not read a blank cell as a pass.

**The change under survey.** One word at `0x0166645c`, four-byte index
`5871895`, `ldr x1,[x4,#0x198]` -> `ldr x1,[x4,#0]`. Confirmed by `IMPL-20` to
move camera 3's `android.sensor.info.pixelArraySize` from `[4096 3072]` to
`[8192 6144]` while leaving `activeArraySize` and
`preCorrectionActiveArraySize` at `[0 0 4096 3072]`. Table:
`agc-50mp-yama/hal-pixelarray-deneme.patch`.

**Why the direction matters.** `OQ-03`'s own note records that the *opposite*
direction — raising the **active** array — is known to break AGC. This survey
therefore tests a change that has never been tried on this device, and a break
found here is informative rather than expected.

## 1. Pre-change expectations (F3.4-01)

Sourced from `docs/regression-v2.1.md` (the Faz 2.3 ten-mode pass),
`snapshots/20260831-1607__faz2.2__post-flash-v2.1-baseline.txt` (the Faz 2.2
baseline) and `EV-04`. **Recollection is not a source here**; every row cites
where its expectation comes from.

| # | Consumer / surface | Pre-change expectation | Source | Post-change result |
|---|---|---|---|---|
| 1 | Stock camera (`com.android.camera`) — opens, live preview | Opens with a live preview in every mode incl. `stock` | `regression-v2.1.md` §3 rows 7-11, `CameraLauncher` resumed, no fatal | *(F3.4-02)* |
| 2 | Stock camera — shutter completes, plausible dimensions | Not separately measured in Faz 2.3 | **no prior record — this row establishes one** | *(F3.4-02)* |
| 3 | Open Camera (`com.xiaomi.module.evaluation`) — full-res capture | **50.3 MP**, i.e. 8192x6144 | `EV-04` (`confirmed`), journal Faz 8; the only installed consumer reaching 8192x6144 | *(F3.4-03)* |
| 4 | Video — 1080p plain, `dcgB`, OpenCamera | Records, output normal | `regression-v2.1.md` §6 row 1, **PASS** | *(F3.4-04)* |
| 5 | Video — 4K60 | **No clean prior reading exists** | `regression-v2.1.md` §6 row 4 is marked *unreachable* | *(F3.4-04)* |
| 6 | Video — AGC video section, any mode | **Already black before this change**, in all four measured states incl. plain `stock` | `regression-v2.1.md` §6d four-cell matrix; `FIND-2.3-03` | *(F3.4-04)* |
| 7 | Mode surface — one sensor-layer mode opens | `dcgA`/`ln2s`/`ln4s`/`stock` all open, live preview | `regression-v2.1.md` §3 rows 7, 9, 10, 11 | *(F3.4-05)* |
| 8 | Mode surface — HAL-layer `50mp` opens | Opens; `camera.hal0` moves 440 -> 456 rows | `regression-v2.1.md` §3 rows 1, 3 and §5 | *(F3.4-05)* |
| 9 | Framing / field of view | No controlled prior capture from a fixed position exists | **no prior record** — see the limitation below | *(F3.4-06)* |

## 2. Two rows that cannot produce a clean comparison, stated up front

Faz 3.4's acceptance criteria require the framing assessment to state its own
limitations. Two are known **before** the survey runs, and naming them now stops
a weak comparison from being read as a strong one later.

- **Row 6 (AGC video) is a pre-existing failure, not a regression.** AGC's video
  preview was measured black in four states including plain `stock`, with sensor
  and HAL both unmodified. If it is black after this change too, that is
  `FIND-2.3-03` continuing, and it must not be attributed to the patch. The
  survey records it for completeness only. Note also that Faz 3.4 excludes AGC
  interaction by scope — this row is satisfied from the existing record, not by
  opening AGC.
- **Row 9 (framing) has no controlled baseline.** No pre-change capture from a
  fixed position exists, so a same-position comparison would have to be
  constructed now, after the fact. Unless a fixed-position pre-change capture is
  taken *before* the patch is re-applied, this row's honest verdict is
  "not assessable", and it should be recorded that way rather than guessed.

## 3. Consumers deliberately excluded

- **AGC / Gcam.** Faz 3.5 owns it entirely; mixing it in here defeats the
  ordering Phase 3 exists to enforce.
- **Applications with no documented prior behaviour.** Without a pre-change
  expectation there is nothing to compare against, so a verdict would be
  unfalsifiable.

## 4. Scope statement for `OQ-03`

When this survey completes, `OQ-03` is answered **only for the consumers in the
table above**. The wording must name them. A general "no consumers break" claim
is not supported by three applications and a mode spot-check, and the question's
own phrasing invites exactly that overreach.
