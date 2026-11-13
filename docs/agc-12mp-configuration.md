# The AGC 12.58 MP configuration — how to set it, verify it, and recognise it when it drifts

Produced by **Faz 3.11**, the Phase 3 closure sub-plan, from the measurements in
`IMPL-52` … `IMPL-61`. Every number in this file is a recorded measurement with
its run id beside it. Where the evidence has a gap, this file says so instead of
filling it.

This is the operator record for the state Phase 3 delivers: **Google Camera
working at 12.58 MP while the 50 MP HAL layer stays enabled for other
consumers.** It is not a description of what the camera *can* do. It is the
configuration that was measured, on the base that was measured, with the
procedure that reproduces it.

---

## 1. The configuration

**Two preference keys are the configuration. A third looks like one and is not.**

| Key | Value | What it is |
|---|---|---|
| `pref_48m_key` | `0` | **Input.** Set this. Adopted as the phase's configured state by the user as `DEC-18` on 2026-09-04, on the evidence of `IMPL-53` and `IMPL-54`. |
| `pref_camera_resolution` | `full` | **Input.** Set this. The *Full resolution* entry in AGC's visible resolution list. |
| `pref_camera_picturesize_back_key` | `4096x3072` | **Derived. Verify it; never set it.** |
| `pref_camera_picturesize_front_key` | `3264x2448` | **Derived.** Recorded because it moves with the same input — see section 9. |

**Why the derived key must not be set.** `IMPL-52` measured that AGC re-derives
its photo size from the two inputs **at every start**, so the derived key is a
cache of the last start rather than a setting. A write to it does not survive an
AGC restart. An instruction that told a reader to set `pref_camera_picturesize_back_key`
would be an instruction that silently fails, and the reader would have no signal
that it had.

`4096x3072` is **12.58 MP**. That figure, not 12.6, is what the smoke script
reports and what the acceptance thresholds in this project are stated against.

### The base this is measured on

The configuration is only meaningful against the layer state it was measured on.
`DEC-15` answered which base that is on 2026-09-04: the **shipped `fullres`
artifact**.

| Layer | Expected value |
|---|---|
| `hal.live.md5` | `fe0245a4720fb07b01d96deef47f5569` |
| `hal.live.size` | `27268688` |
| `hal.state` | `fullres` |
| `hal.mount.count` | `1` |
| `sensor.live.md5` | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` (**stock**) |
| `sensor.mount.count` | `1` |
| `mode.file` | `50mp` |
| Camera enumeration | `13` devices |
| `agc.apk.md5` | `ce65f862c990e2acc02be356f75a7122` |
| `agc.versionName` | `8.4.300.414775575.18` |

**Figures inherited from `IMPL-52` were measured on the experimental base
`ce419bc901bea61945d166aee11e1ab0` and are not restated here as statements about
the shipped artifact.** Where this file cites `IMPL-52`, it cites its *mechanism*
findings (the derivation, the lag), which were re-measured on the shipped base by
`IMPL-53`.

---

## 2. Setting it

The preferences file is at:

```
/data/data/org.codeaurora.snapcam/shared_prefs/org.codeaurora.snapcam_preferences.xml
```

owner `u0_a450`, mode `0660`, SELinux label
`u:object_r:app_data_file:s0:c194,c257,c512,c768`.

**Do not use `sed -i`.** It replaces the file rather than rewriting it in place,
which leaves the result root-owned and mislabelled, and AGC then cannot read its
own preferences. Write to a temp file and `cat` the content back into the
original so the inode, owner, mode and label are preserved.

> **⚠ CORRECTED 2026-09-05 by the `F3.11-10` read-back (`IMPL-63`). The first
> version of this procedure destroyed the preferences file when it was followed
> literally, and the fix is not cosmetic.** The commands were issued as written;
> the `sed` step failed on the device shell with
> `/system/bin/sh: syntax error: unexpected '1< '`, and the next line —
> `cat /data/local/tmp/p.xml > $PREFS` — **truncated the live preferences file
> to 0 bytes** before discovering there was nothing to copy from. Owner, mode
> and label survived; the content did not. It was restored byte-identical from a
> backup taken four minutes earlier. **Two defects, and the second is the
> dangerous one:**
>
> 1. **Quoting.** A single-quoted `sed` expression does not survive the
>    host → `adb` → device-shell → `su -c` chain intact. This is a host-specific
>    hazard, and this project already knows the route around it: put the commands
>    in a script, push it, and run `su -c 'sh /data/local/tmp/x.sh'`.
> 2. **Destructive ordering.** `cat tmp > live` truncates `live` **first**. If the
>    filter step fails for *any* reason — a quoting slip, a full filesystem, a
>    typo in the key name — the preferences are gone before anything is read
>    back. That flaw is independent of the shell and of the host.
>
> **Always take a backup before the write, and never truncate the live file until
> the filtered copy is known good.** The procedure below does both.

**Step 1 — back up.** Not optional; the failure above is why.

```sh
adb shell su -c "cp /data/data/org.codeaurora.snapcam/shared_prefs/org.codeaurora.snapcam_preferences.xml \
    /data/local/tmp/agc_prefs_backup.xml"
```

**Step 2 — write the script to the host, push it, run it.** Pass the target value
and the current value, so the substitution is addressed in both directions:

```sh
#!/system/bin/sh
NEW="$1"; OLD="$2"
P=/data/data/org.codeaurora.snapcam/shared_prefs/org.codeaurora.snapcam_preferences.xml
T=/data/local/tmp/p.xml

am force-stop org.codeaurora.snapcam
rm -f "$T"
sed "/pref_48m_key/s|>$OLD<|>$NEW<|" "$P" > "$T" || { echo "FAIL: sed"; exit 1; }

# GUARD 1 - the filtered copy exists and is non-empty.
[ -s "$T" ] || { echo "FAIL: temp empty - live file NOT touched"; exit 1; }

# GUARD 2 - its size is within a few bytes of the original. A preference write
# changes one character; it never changes the file's size class.
SO=$(stat -c %s "$P"); ST=$(stat -c %s "$T")
D=$((SO - ST)); [ $D -lt 0 ] && D=$((-D))
[ "$D" -le 8 ] || { echo "FAIL: size $SO -> $ST - live file NOT touched"; exit 1; }

# GUARD 3 - the substitution actually took.
grep -q "name=\"pref_48m_key\"[^<]*>$NEW<" "$T" \
    || { echo "FAIL: substitution did not take - live file NOT touched"; exit 1; }

cat "$T" > "$P"        # only now is the live file touched
rm -f "$T"
echo "OK"; grep -oE "name=\"pref_48m_key\"[^<]*<" "$P"; ls -lZ "$P"
```

```sh
adb push setpin.sh /data/local/tmp/setpin.sh
adb shell su -c 'sh /data/local/tmp/setpin.sh 0 1'    # to 0, from 1
```

The **addressed** substitution `/pref_48m_key/s|>1<|>0<|` restricts the change to
the line carrying that key and uses no capture groups. `IMPL-61` used this form
in both directions, and `IMPL-63` ran the guarded script above four times in both
directions; owner, mode and label were preserved on every one, and all three
guards were exercised.

**On a Git Bash / MSYS host**, prefix `adb` invocations with `MSYS_NO_PATHCONV=1`
for the **device** path, but not for the local path of a `push`, which must stay a
Windows path.

**Verify by value, never by checksum or inode.** AGC rewrites the preferences
file on its own schedule — during `IMPL-53` it grew from 12,072 to 12,169 bytes
with no configuration change — so a changed md5 proves nothing and an unchanged
one proves nothing either. Read the key's value back.

### The two lags — read this before you record a failure

**The derived keys lag the input write by one AGC start** (`IMPL-52`,
reproduced by `IMPL-61`). Immediately after the write, and before AGC has been
started, `pref_48m_key` already reads its new value while all three derived
values still read their old ones. A reader who checks here records a false
failure.

**The configured streams lag the derived key by one further start**
(`FIND-3.10-04`, new in `IMPL-61`). On the *first* cold start after a write, both
streams still read their old dimensions even though the derived key has already
moved. The new stream pair appeared only on the **second** cold start.

So: write, then **two** cold starts, then read. Use a plain launcher start —

```sh
adb shell "monkey -p org.codeaurora.snapcam -c android.intent.category.LAUNCHER 1"
```

— which `IMPL-61` measured to arm no preference key and to take no photograph
(216 photos in the camera roll before, 216 after).

**Do not open `CameraSettingsActivity` to make this change.** It writes two trap
keys; see section 6.

### After a reboot, wait before reading

`IMPL-61` measured that immediately after a reboot AGC's preferences are
**unreadable** — the read returns "No such file or directory" and
`/data/data/org.codeaurora.snapcam` lists no `shared_prefs` directory at all.
This is the credential-encrypted storage boundary, not lost state. Moments later
every value read back intact. **A checklist that reads AGC preferences straight
after a reboot will record a false total failure.**

---

## 3. Verifying it

Take a snapshot with the Phase 3 instrument:

```sh
scripts/smoke.sh -o <YYYYmmdd-HHMM>__<subplan>__<label>
```

### Expected fields

| Field | Expected |
|---|---|
| `agc.pref_48m` | `0` |
| `agc.pref_resolution` | `full` |
| `agc.photo_size.back.derived` | `4096x3072` |
| `agc.photo_size.back.mp` | `12.58` |
| `agc.photo_size.front.derived` | `3264x2448` |
| `hal.live.md5` | `fe0245a4720fb07b01d96deef47f5569` |
| `hal.state` / `hal.mount.count` | `fullres` / `1` |
| `sensor.live.md5` / `sensor.mount.count` | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` / `1` |
| `mode.file` | `50mp` |
| `prefs.trap.count` | see the caveat below — **audit the values, not the count** |

### Expected configured streams

Read with AGC **open**, by pattern within a **single** dump:

```sh
adb shell "dumpsys media.camera" | grep -A6 "Stream\[[0-9]\]:"
```

| Stream | Expected |
|---|---|
| YUV | `Dims: 4096 x 3072, format 0x23` |
| RAW10 | `Dims: 4096 x 3072, format 0x25` |

**Matching pair.** That both streams agree is the point: `IMPL-40` established
that the black-frame failure tracks a request/delivery *mismatch*, not the
resolution itself.

Never derive stream line numbers from one dump and apply them to another —
`FIND-3.10-01` measured six consecutive `dumpsys media.camera` calls returning
65530 / 50666 / 50666 / 50666 / 65530 / 65529 lines with nothing changing on the
device.

### Diffing two snapshots — use this exact command

`scripts/smoke.sh`'s `camera.halN.stream_config.rows` block is **non-deterministic**
(`FIND-3.10-01`, P2, open — see section 9). It is derived from line numbers taken
from one `dumpsys` and applied to a second, independent one, so it lands
correctly, short or long at random. The output is always well-formed, so the
defect is silent.

Compare the **stable region only**:

```sh
sed -n '/BEGIN COMPARABLE/,/END COMPARABLE/p' SNAP \
  | grep -vE '^ +[0-9]+ [0-9]+ [0-9]+ (OUTPUT|INPUT)$'
```

`IMPL-61` measured this region **byte-identical across five consecutive runs**,
at 45 lines. It carries all four preference keys, both layer md5s, both mount
counts, the mode, the trap count, the APK md5, and all thirteen camera summary
lines with their `streamcfg=NNN` counts — which is what the script's own
comment says the stream table exists to catch.

The defect can manufacture a spurious **difference** but not a spurious
**sameness**, so results already taken against the full region stand.

---

## 4. What a good capture measures

**Method (`IMPL-40`, unchanged since).** PIL on the **original** JPEG pulled from
the device — not a re-encode, not a thumbnail — converted to grayscale, black
defined as a luminance value **below 4**, reported as a fraction of total pixels.
`Image.MAX_IMAGE_PIXELS` must be raised or PIL refuses a 50 MP file. Quadrant
fractions are computed the same way over the four halves-by-halves.

**Threshold: a capture passes at black fraction `< 0.01`.** Stated in advance by
`Faz3.7` and used unchanged since.

| Capture | Geometry | MP | Black | Run |
|---|---|---|---|---|
| Matched-request positive control | 3072x4096 | 12.58 | **0.0024** | `IMPL-40` |
| First deliberate pinned capture | 3072x4096 | 12.58 | **0.0027** | `IMPL-54` |
| Coexistence bracket, AGC | 3072x4096 | 12.58 | **0.0000** | `IMPL-58` |
| Confirming capture | 3072x4096 | 12.58 | **0.0001** | `IMPL-61` |
| Closing capture after restore | 3072x4096 | 12.58 | **0.0001** | `IMPL-61` |

Five clean captures, four separate sessions, three separate days. The clean
cluster is `0.0000`–`0.0027`, comfortably inside the threshold.

**The measurement scale is validated across sessions.** `IMPL-61` re-measured two
earlier originals with its own script and reproduced `IMPL-54`'s `0.0027` and
`IMPL-58`'s `0.0000` exactly, so figures from different sessions are comparable.

---

## 5. The failure mode

The failure is **AGC unpinned** — `pref_48m_key` back at `1`. It is recognisable
from a snapshot. It is **not** reliably recognisable from an image, and that
qualification is the most important sentence in this section.

### From a snapshot — reliable

| Field | Pinned | Unpinned |
|---|---|---|
| `agc.pref_48m` | `0` | **`1`** |
| `agc.photo_size.back.derived` | `4096x3072` | **`8192x6144`** |
| `agc.photo_size.back.mp` | `12.58` | **`50.33`** |
| `agc.photo_size.front.derived` | `3264x2448` | **`6528x4896`** |

Measured in `snapshots/20260905-1545__Faz3.10__F31007-control-state.txt`.

### From the configured streams — reliable, and the pair goes mismatched

| Stream | Pinned | Unpinned |
|---|---|---|
| YUV `0x23` | `4096 x 3072` | **`8192 x 6144`** |
| RAW10 `0x25` | `4096 x 3072` | `4096 x 3072` — **does not move** |

The shipped base advertises no RAW10 row at `8192x6144` (`IMPL-43`: camera 2's
`android.scaler.availableStreamConfigurations` publishes RAW10 only at
`4096x3072` and `4096x2304`), so the pair goes **mismatched** rather than both
moving up. `IMPL-53` measured this first; `IMPL-61` reproduced it.

Remember the second lag: on the first cold start after the change both streams
still read `4096x3072`. Read them on the second.

### From the image — NOT reliable. Read this before you rely on it.

The historical signature of the 50 MP path is a **fold**: content occupying
exactly one quadrant of the frame.

`IMPL-43`, `EV-44`, 6144x8192, 50.33 MP, black **0.7497**, quadrants
top-left `1.0000`, bottom-left `1.0000`, top-right `0.4994`, bottom-right
`0.4994` — `(1.0 + 0.4994 + 1.0 + 0.4994) / 4 = 0.7497`. A `4096x3072` payload
in a raster believed to be `8192x6144` fills exactly one quarter, leaving three
quarters black: `1 − 1/4 = 0.75`. The recorded fold band is **0.7497 – 0.7502**,
the second figure from the UHR-enabled variant.

**`IMPL-61` measured the unpinned state and the fold did not occur.** Two
captures in the fully armed state — `pref_48m_key=1`, derived key `8192x6144`,
the mismatched stream pair — both came back **6144x8192, 50.33 MP, black
`0.0000`, all four quadrants `0.0000`**. Clean, twice, reproducibly, on the
shipped `fullres` base. This is `FIND-3.10-03`, and it was graded against a
prediction of a fold at ~0.75 committed **in writing before the capture existed**
(`snapshots/20260905-1517__Faz3.10__F31007-prestated-control-prediction.txt`,
15:17; captures 15:45:54 and 15:47:52). The prediction **failed** and was not
revised.

**What that means, and what it does not.**

- **It means the image test is not a dependable drift detector.** An operator who
  checks only the photograph can see a clean 50 MP file and conclude the pin
  holds when it does not. **Use the snapshot fields.**
- **It does not mean 50 MP works.** `FIND-3.10-03` reports a **measurement**, not
  a capability. What is *not* established: why the fold is absent now when
  `IMPL-43` measured it; whether the difference is the HAL base, the stream pair,
  the AGC build, the scene, or the second-cold-start effect; and whether the
  result is stable across sessions rather than only within the one that measured
  it. No second session has reproduced it.
- **The retirement stands.** The user ruled on 2026-09-05 that `DEC-14` holds and
  that this is recorded as a measured exception. See section 8.

---

## 6. What re-arms the trap, and what breaks the pin

### Routes that re-arm the twelve trap keys

| Route | What to check afterwards |
|---|---|
| **Importing either root `.agc` file.** `12mpx_agc_config.agc` and `50mpx_agc_config.agc` each contain **all twelve** trap key names, verified 2026-08-31. | Per-key **value** audit of all twelve; then the section 3 fields. |
| **Opening `CameraSettingsActivity`** (AGC's settings screen). Writes `pref_raw_key` and `pref_fix_resolution_key`, both at value `0` (`FIND-3.7-01`, `IMPL-54`). | Per-key value audit. Both were measured **inert** at value `0` — identical stream configuration with them present and absent — so presence alone is not a fault. |
| **An unidentified route that is not the settings screen.** `FIND-3.10-02`: `prefs.trap.count` moved `0 → 2` (the same two keys, both at value `0`) during a session in which **no axis opened the settings screen** and every AGC start was a plain launcher start. Narrowed to 15:45:35–15:50 on 2026-09-05 — during the 50 MP captures or the restore. Not narrowed further; diagnosis was outside that sub-plan's scope. | Per-key value audit. **Open, cause unknown.** |
| **An AGC package update.** Not measured; listed because a package replacement rewrites the app's data expectations and `agc.apk.md5` is a field this project pins. | `agc.apk.md5` against `ce65f862c990e2acc02be356f75a7122`, then the full section 3 check. |

**Because of `FIND-3.10-02`, a bare `0 / 12` assertion is the wrong check.** The
device is currently at **2 / 12, both keys at value `0`**, and that state is
measured harmless. Audit the twelve keys **by value**; a key present at `0` is
inert, and only a non-zero value is a fault. `scripts/smoke.sh` reports presence
only (`FIND-3.7-02`, open — section 9), so its `prefs.trap.count` field cannot
make this distinction and must not be used alone.

### What moves the pin itself

Nothing that was tested. See the matrix in section 7. The only stimulus measured
to move it is a deliberate write to `pref_48m_key`.

---

## 7. Survival matrix

From `Faz3.10` / `IMPL-61`, 2026-09-05, one continuous session with the user at
the device. The verdict rule was committed in writing at 15:23, before the first
disturbance at 15:24, and was not revised
(`snapshots/20260905-1523__Faz3.10__F31001-verdict-rule-and-matrix-skeleton.txt`).
The verdict is taken on the two **input** keys.

| Axis | `pref_48m_key` | `pref_camera_resolution` | rear derived | front derived | Verdict |
|---|---|---|---|---|---|
| AGC cold start | `0` → `0` | `full` → `full` | `4096x3072` unchanged | `3264x2448` unchanged | **SURVIVED** |
| Camera-stack restart | `0` → `0` | `full` → `full` | `4096x3072` unchanged | `3264x2448` unchanged | **SURVIVED** |
| QuickSettings mode switch, away half | `0` → `0` | `full` → `full` | `4096x3072` unchanged | `3264x2448` unchanged | **SURVIVED** |
| QuickSettings mode switch, back half | `0` → `0` | `full` → `full` | `4096x3072` unchanged | `3264x2448` unchanged | **SURVIVED** |
| Device reboot | `0` → `0` | `full` → `full` | `4096x3072` unchanged | `3264x2448` unchanged | **SURVIVED** |

**Every consecutive snapshot pair diffed to zero differing lines across the
45-line stable region. Not one axis moved a single field.** No axis produced a
self-healing row — the derived key held its value directly on all four, so the
rule's inputs-survived/derived-stale classification was pre-declared and never
needed.

Confirming capture on the surviving state: 12.58 MP, black `0.0001`. Closing
capture after the negative control was restored: 12.58 MP, black `0.0001`.

**No axis failed**, so nothing in this matrix is conditioned on a failure.

Two boundaries on what the matrix covers:

- The mode-switch axis necessarily moves the HAL md5 on its away half (to
  `c3fa63a86ee3ecaf9fbf02005d35f6b5`) — that change *is* the disturbance. The
  axis returned to `fe0245a4…` exactly.
- **Rear camera only, and preference values only for the front key.** No
  front-camera session was opened and no front-camera capture was taken, in this
  matrix or in the `Faz3.9` coexistence bracket. Front-camera **image**
  behaviour is unmeasured. See section 9.

Full result:
`snapshots/20260905-1553__Faz3.10__F31009-pin-stickiness-matrix-result.txt`.

---

## 8. The retirement note — read this before trying 50 MP in AGC again

**The objective "50 MP end-to-end in AGC" was retired on 2026-09-03 as `DEC-14`
and replaced with "AGC stable at 12.6 MP under 50 MP", which is what this
document records.** The retirement was reaffirmed by the user on 2026-09-05 after
`FIND-3.10-03`.

**It is not untested pessimism.** Four measured negatives, each with recorded
method:

| # | Negative | Run |
|---|---|---|
| 1 | **`d0014` is not static data.** An exhaustive byte scan of all 27,268,688 bytes for `int32 1920` followed immediately by `int32 1080` returns 20 aligned occurrences, **none** a stream-configuration record; there is no run of seven `[fmt, 1920, 1080, 0]` quadruples anywhere. The rows are assembled at runtime, so a row edit was never available. | `IMPL-47` |
| 2 | **The value is computed, not stored.** `d0014`'s count is the tail of a per-camera loop in `InitializeScalerStaticCaps` whose first branch is a multi-way switch on a sensor/format identifier spanning most of the 6,516-instruction function. Every `[sp,#0x1f0]` reference was enumerated, not sampled. | `IMPL-51` |
| 3 | **There is no code cave.** An exhaustive byte-pattern scan of the binary's sole executable `PT_LOAD` segment (~24.9 MB; the other two `PT_LOAD` segments are `R+W` and cannot host code, confirmed via program headers) for any run of ≥ 16 contiguous free bytes found **none**. The longest run anywhere is **12 bytes**, three instances. The designed additive patch is 16 bytes. | `IMPL-50` |
| 4 | **Narrowing the broad RAW rows breaks AGC.** At two independent bisection stages, AGC crashed **3 / 3** with `gcam.Gcam.f()`'s NPE signature; the post-revert control launched 2 / 2. Site 1's guarded rows alone are sufficient to break it. | `IMPL-49`, `IMPL-50` |

**The reopening condition, from `DEC-14` verbatim:** *"The one thing a future
reader must not do is treat the retirement as untested pessimism — both walls
(`d0014` non-static, no code cave) are measured negatives with recorded method,
and reopening needs new evidence about one of them, not renewed effort against
the same two."*

**So: a genuinely new idea about either wall reopens this. Trying the same two
approaches harder does not.**

### The measured exception, recorded rather than buried

On 2026-09-05, `IMPL-61` measured AGC producing a **clean 50.33 MP image, twice**,
on the shipped `fullres` base with `pref_48m_key=1` — 6144x8192, black `0.0000`,
no fold. Detail in section 5.

The user ruled on 2026-09-05 that **`DEC-14` stands** and that this is recorded
here as a measured exception. The reasoning that ruling rests on:

- The four negatives above are about the **HAL stream-configuration tables** and
  the patchability of `d0014`. `FIND-3.10-03` is a **capture result**. It does
  not supply new evidence about either wall, so it does not meet `DEC-14`'s own
  reopening condition.
- The result is **unexplained**. Why the fold is absent is not established, and
  the difference from `IMPL-43` could be the HAL base, the stream pair, the AGC
  build, the scene, or the second-cold-start effect. Nobody has separated them.
- It has been reproduced **twice within one session** and **zero times across
  sessions**.

**What a future reader should do with it.** Treat it as the most interesting open
question in the project, not as a solved problem and not as noise. If it
reproduces in a fresh session, on a cold device, in a different scene, then it is
new evidence about the delivery path and the question of *what changed* becomes
worth real effort. Until then the objective stays retired and the configuration
in section 1 is what the project claims.

---

## 9. Knowledge and open items this record carries

**The front camera re-derives too, and no Phase 3 matrix covered its images.**
`pref_camera_picturesize_front_key` is derived from the same input as the rear
key: `IMPL-54` measured it moving `6528x4896` → `3264x2448` across a base change,
and `IMPL-61` measured it moving in both directions with `pref_48m_key`
(`3264x2448` ⇄ `6528x4896`) and **not moving at all** across cold start,
camera-stack restart, mode switch or reboot. That is a complete answer at the
level of preference values. **It is not an answer about front-camera images** —
no front-camera session was opened and no front-camera capture was taken anywhere
in Phase 3. A reader who needs front-camera behaviour must measure it.
(`FIND-3.7-03`, disposed of here as knowledge; the phase it would otherwise have
been routed to is closing.)

**Two instrument defects are open and no phase currently owns the repair.**
Both concern `scripts/smoke.sh`, whose write authority belonged to `Faz3.8` — now
complete.

- **`FIND-3.7-02` (P3, open).** The script's trap probe greps key **names**
  (`grep -hoE "pref_raw_key[a-z0-9_]*|pref_fix_resolution_key[a-z0-9_]*"`) and
  never reads values, so `prefs.trap.count` cannot distinguish an inert key at
  `0` from an armed one. With the device at 2 / 12 both inert, the field now
  reports a number that looks like a fault and is not one. **Workaround:** the
  per-key value audit in section 6.
- **`FIND-3.10-01` (P2, open).** The `camera.halN.stream_config.rows` block is
  non-deterministic. **Workaround:** the deterministic diff command in section 3.

Both have workarounds that are in this document, so neither blocks use of the
configuration. Neither is fixed.

**`FIND-3.5-01` (active-array geometry) and `FIND-4.5-02` (the RAW payload
geometry cause)** remain open as recently as `IMPL-51`. Both exist to explain why
a full-resolution AGC frame is unusable — the question the retired objective
asked. `IMPL-43` located `FIND-4.5-02`'s mechanism precisely (buffer geometry
versus sensor readout geometry; `pixelMode` cannot leave `DEFAULT` without
`ULTRA_HIGH_RESOLUTION_SENSOR` in `availableCapabilities`). Under `DEC-14`
neither blocks anything. Their disposition is recorded in
`Planner-docs/Planing-Ledger.md`.

---

## 10. What this project claims about AGC

> **On a Xiaomi 13 Ultra running the `50mp` module mode with the shipped
> `fullres` HAL `fe0245a4720fb07b01d96deef47f5569` and the stock sensor
> `9e4d0fe1a8bf2eb4146c9917a0ac2c4c`, Google Camera `ce65f862c990e2acc02be356f75a7122`
> configured with `pref_48m_key=0` and `pref_camera_resolution=full` captures a
> clean 12.58 MP photograph — black fraction below `0.01` by the `IMPL-40`
> method — and that configuration survived AGC cold start, camera-stack
> restart, QuickSettings mode switch and device reboot with zero field changes
> (`IMPL-61`, four axes, no failures). Verified by
> `scripts/smoke.sh -o <snapshot>` reporting `agc.pref_48m=0`,
> `agc.pref_resolution=full` and `agc.photo_size.back.derived=4096x3072`,
> followed by one capture measured under `0.01`.**

**Scope of the claim.** Rear camera. One device. The 50 MP layer stays enabled
throughout and a second camera application captures at 50.33 MP in the same
session (`IMPL-58`), which is what "coexistence" means here. The claim says
nothing about the front camera's images, about distribution readiness, or about
AGC at any resolution other than 12.58 MP.

`Faz9.2` verifies this sentence. `Faz9.3` propagates it and retires the
contradicted `EV-23` claim that AGC cannot exceed 15.2 MP.

---

## 11. Read-back verification

**Performed 2026-09-05, 19:02–19:09 local, as `IMPL-63` / `F3.11-10`. One
continuous session, user present at the device, one human shutter press.
Result: the document is reproducible, and following it literally exposed one
serious defect in its own write procedure, now corrected in section 2.**

A configuration record that has not been followed once is a draft. This one has
now been followed, from a genuinely unpinned state, by someone working only from
what is written here.

### What was done

| # | Step | Result |
|---|---|---|
| 1 | Entry bracket `20260905-1902__Faz3.11__F31110-pre` | Every section 3 field as predicted. |
| 2 | Checklist item 1, per-key **value** audit | 2 of 12 present (`pref_raw_key`, `pref_fix_resolution_key`), **both at value `0` → inert**; 10 absent. **A bare `0/12` assertion would have failed here.** The corrected item passes. |
| 3 | Backup taken | `/data/local/tmp/agc_prefs_F31110_backup.xml` and `snapshots/20260905-1902__Faz3.11__F31110-prefs-backup.xml`, md5 `21762bdcb09f107aad2f397351cf1337`, 12,169 B. |
| 4 | Left the pinned state (`pref_48m_key` → `1`), two cold starts | Derived keys moved to `8192x6144` / `6528x4896`. Streams: RAW10 `0x25` at `4096x3072`, YUV `0x23` at `8192x6144` — **the mismatched pair, third independent reproduction** (`IMPL-53`, `IMPL-61`, `IMPL-63`). Section 5's failure-mode tables confirmed against a fresh measurement. |
| 5 | **Set procedure run exactly as section 2 had it written** | **FAILED, destructively.** See below. |
| 6 | Restore from the step-3 backup | Byte-identical, md5 `21762bdc…`, owner/mode/label intact. |
| 7 | Set procedure re-run in the corrected guarded form, from `1` to `0`, two cold starts | Clean on the first attempt. |
| 8 | Verification against section 3 | **All fields matched**: `agc.pref_48m=0`, `agc.pref_resolution=full`, back `4096x3072` / `12.58` MP, front `3264x2448`, HAL `fe0245a4…` `fullres` mount 1, sensor `9e4d0fe1…` mount 1, mode `50mp`, APK `ce65f862…`. |
| 9 | Configured streams | **`4096 x 3072` on YUV `0x23` and `4096 x 3072` on RAW10 `0x25`** — the matching pair, as predicted. |
| 10 | Capture (human shutter, 19:08:41) | Photo count 213 → **214**, exactly one. |
| 11 | Measurement, `IMPL-40` method | **3072x4096, 12.58 MP, black `0.0001` — PASS** against `< 0.01`. Quadrants `0.0000` / `0.0000` / `0.0000` / `0.0003`. `snapshots/20260905-1908__Faz3.11__F31110-readback-ORIGINAL.jpg`, md5 `64041206a370574df53f964e24c64e17`. |
| 12 | Closing bracket `20260905-1909__Faz3.11__F31110-close` | **Zero differing lines** against the entry bracket across the 45-line stable region, and the preferences md5 is back to `21762bdc…` **byte-identical** despite the file having been unpinned, truncated, restored, unpinned and pinned in between. |

### The correction the read-back forced

**Section 2's original write procedure was destructive and is replaced.** Issued
as written, the `sed` step failed on the device shell
(`/system/bin/sh: syntax error: unexpected '1< '`) and the following
`cat /data/local/tmp/p.xml > $PREFS` **truncated the live preferences file to 0
bytes**. Two defects: a quoting failure specific to the
host → `adb` → device-shell → `su -c` chain, and — the one that matters
anywhere — an ordering flaw in which the live file is truncated *before* the
replacement is known to exist. Section 2 now requires a backup first and guards
the write behind three checks (temp non-empty, size within 8 bytes, substitution
present) so the live file is never touched on a failed filter. All three guards
were exercised during this session.

**This is recorded rather than silently applied**, and it is the read-back
earning its place: the defect was in the document, not in the device, and only
following the document literally would have found it.

### What this read-back did and did not establish

- **Established:** the configuration is reproducible from this document alone;
  every predicted field and both stream pairs matched; the capture passed the
  threshold with room to spare; the state returned to its entry values exactly.
- **Established as a by-product:** the corrected checklist item 1 (value audit)
  passes on a device where the old presence count would have failed, and the
  failure-mode tables in section 5 hold against a fresh measurement.
- **Not established:** the front camera, which was not exercised. No
  front-camera session was opened and no front-camera capture was taken, here or
  anywhere in Phase 3. Nothing about reboot survival was re-tested — that rests
  on `IMPL-61`, not on this run.
- **Not attempted:** a 50 MP capture in the unpinned state. `FIND-3.10-03`
  therefore still stands on one session's evidence, not two.
