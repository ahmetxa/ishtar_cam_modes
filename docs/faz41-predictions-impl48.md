# Faz4.1 F4.1-04 + F4.7-03 free proof — predictions stated BEFORE any device write

Recorded 2026-09-03. Base: `ce419bc901bea61945d166aee11e1ab0` (fullres + seven-word
stack + the 18-site UHR gate), mode `50mp`, 13 camera devices.

## Why the baseline is not Faz4.1's stated one, and what replaces it

`Faz4.1`'s `F4.1-01` targets (hal0 468, hal3 520) were stated against the **fullres**
base `fe0245a4…`, which does **not** publish `d0014` at all — the tag exists only while
the UHR gate is open. Measuring `d0014` before and after therefore requires the UHR
base, so the targets are restated here against `ce419bc9…`, before the patch, naming
the camera id and the metric exactly as `F4.1-01` requires.

**Metric:** the `int32` element count of `android.scaler.availableStreamConfigurations
(d000a)` and of `…MaximumResolution (d0014)`, read from `dumpsys media.camera` per
camera HAL device id. Each record is 4 int32.

## Measured baseline (stage A)

| cam | d000a | d0014 | UHR |
|---|---|---|---|
| 0 | 800 | 28 | yes |
| 1 | 800 | 28 | yes |
| 2 | 868 | 28 | yes |
| 3 | 868 | 28 | yes |
| 4 | 868 | 28 | yes |
| 5 | 868 | 28 | yes |
| 6 | 852 | 28 | yes |
| 7 | 852 | 28 | yes |
| 8 | 856 | 28 | yes |
| 9 | 856 | 28 | yes |
| 10 | 852 | 28 | yes |
| 11 | 124 | – | – |
| 12 | 124 | – | – |

`d0014` on every UHR camera is 7 records, all at 1920x1080, formats
`{33, 34, 35, 36, 37, 38, 54}`. `d0015` and `d0016` are **not published** — the known
gap the handoff flagged; `IMPL-47` located their emission sites but nothing emits them.

## THE DISCRIMINATING PREDICTION (this is the free proof)

Formats 36, 37, 38 = `0x24`, `0x25`, `0x26` are **exactly** the three admitted by the
raw50 widening (`sub wN,#0x22` ; `cmp wN,#5` instead of `#2`). Formats 33, 34, 35 and
54 reach the array by other tests.

- **If the max-res rows are built by the SAME LOOP** as the default rows — i.e. Faz4.1's
  gate reaches them — then reverting the gate to `#2` must drop formats 36, 37 and 38
  from `d0014`, leaving 4 records: **`d0014` 28 → 16**.
- **If the rows merely share the FUNCTION** and not the loop, `d0014` is unaffected:
  **`d0014` stays 28**.

These are mutually exclusive and both are cheap to read. Either outcome settles the
question `F4.7-03` owes and that `IMPL-47` deliberately refused to guess.

## Stage predictions

**Stage B — all four gates `#5` → `#2`.** Pre-committed md5 `fc7481c1d852ee489d4543a6308e07dc`.
- `d000a`: falls by 12 int32 per resolution in each camera's loop. Camera 3 is predicted
  to land at **508**, the recorded pre-raw50 figure. Cameras 11/12 (124) unchanged.
- `d0014`: **16 if same loop, 28 if same function only.** This is the measurement.

**Stage C — site 1 guarded (paths A and B), sites 2/3/4 restored to `#5`.**
Pre-committed md5 `6619ad47a67571ff596b909cd43cf48e`.
- The guard admits `0x22..0x26` only when width == 8192, and otherwise falls into the
  stock `cmp #2`. Site 1 alone is guarded, so **site 2 still emits broadly** and `d000a`
  is *not* expected to reach Faz4.1's final target here — this is `F4.1-04`'s single-site
  delta, not `F4.1-05`'s full-patch figure.
- `d000a`: predicted to fall from 868 by site 1's share of the excess, and to remain
  above the fully-narrowed target because site 2 is untouched.
- `d0014`: **if stage B moved it, stage C is the second, independent test** — the guard
  compares against literal 8192, and `d0014`'s rows are at 1920x1080, so a same-loop
  `d0014` must stay at 16 (the 8192 test fails at 1920 and the widened range is refused).

## Reporting rule that binds this run

Per `DEC-11`, the narrowing delta and the format-32 addition are **two numbers, never
summed into one net array count**. This run performs the **narrowing only**; the
format-32 extension (`F4.1-05b`) is not attempted here, so its number is reported as
**not measured** rather than folded into the narrowing figure.
