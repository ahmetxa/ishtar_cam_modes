# F4.1-07 (IMPL-49) — predictions stated BEFORE any device write

Recorded 2026-09-03. Base as found: `ce419bc901bea61945d166aee11e1ab0` (stage A,
broad raw50 gates), mode `50mp`, 13 camera devices, `pref_48m_key=1`,
`pref_camera_picturesize_back_key=8192x6144`.

## What F4.1-07 can and cannot answer in this run

The sub-plan's section 10 blocks `Faz4.1` on `Faz4.5` so that this check
"preserves a good capture rather than certifying that a half-black frame is
still half-black". `Faz4.5`'s **metadata** half landed (`f0000` moved to
`[0 0 8192 6144]`) but `FIND-4.5-02` is **OPEN** — the image was never
corrected. So the strong form of F4.1-07 is **unavailable**, and this run can
answer only the weak form:

- **ANSWERABLE:** does the guard make the capture worse than it was without it?
- **NOT ANSWERABLE:** does the guard preserve a geometrically correct frame?
  There is no correct frame to preserve.

This is stated up front so the verdict is not read as stronger than it is.

## Prediction 1 — the capture is unchanged

The guard changes only which stream configurations are **advertised**. AGC's
selected picture size, 8192x6144, is advertised at both stage A and stage D.

- Session still configures `8192x6144` with RAW10 (`0x25`) and YUV (`0x23`).
- JPEG still 50.33 MP (6144x8192 stored rotated).
- **Black fraction within measurement noise of the stage-A capture**, i.e. near
  the recorded 0.7497 / 0.7502.
- `f0006` still `[8192 6144]`; `f0000` still `[0 0 8192 6144]`.

## Prediction 2 — AGC's first session survives the narrowing (the real risk)

Going stage A -> stage D **removes** RAW rows at every resolution except
8192x6144. AGC's first session after launch is `4096x3072` in all three launches
on record, so if that session depended on a row the narrowing removes, AGC would
fail to configure, silently fall back, or crash — **a regression, and F4.1-07
would fail.**

It should not, and the reason is specific and falsifiable: `IMPL-48` measured
formats 36, 37 and 32 at 4096x3072 and 4096x2304 **already present at stage B**
with the gate at stock `#2`. They come from a different emission path, so the
guard does not remove them. **Predicted: AGC's 4096x3072 session is unaffected.**

If AGC instead fails to open or configure at stage D, prediction 2 is falsified
and the guard has a cost the array counts did not reveal.

## Prediction 3 — d0014 moves, and it is not a fault

Per `IMPL-48`, stage D narrows `d0014` from `int32[28]` to `int32[16]`. This is
expected here and must not be reported as damage; it is the measured side effect
already recorded in section 26.

## Procedure guard carried from section 17

Both prior AGC captures on record fired in the **first** session after launch,
which is `4096x3072`, and so pre-empted the experiment. This run must **verify
the configured stream reads 8192x6144 before the shutter is pressed**, on both
the before and the after capture, or the comparison is void.

## Reporting rule

The before capture and the after capture are measured the same way as
`IMPL-40/43/44`: PIL, grayscale, threshold < 4, on the original file. No
by-eye judgement.
