# Release Verification Checklist — `ishtar-cam-modes`

Every capability this release claims, with a command that proves it.

This file is `Faz9.2`'s first deliverable. Its companion is
`docs/recovery-runbook.md`, which covers what to do when a release does not
work. This one covers proving that it does.

**Status of this document.** Sections 2, 3, 4, 5 and 7 are complete
(`F9.2-01`, `F9.2-02`, `F9.2-03`, `F9.2-08`). Section 6 — the known-good and
known-bad demonstration (`F9.2-04` / `VAL-KNOWNBAD`) — is **designed but not
run**: it changes device state and needs the user's approval. Section 5 is the
design it is waiting on.

Related records: `docs/recovery-runbook.md`, `docs/release-manifest.md`
(per-release checksums), `docs/agc-12mp-configuration.md` (the AGC
configuration record), `docs/regression-v2.1.md` (the per-mode regression
precedent), `CHANGELOG.md` (version history), `Planner-docs/Project-Ontology.md`
(invariants).

---

## 1. Scope, and how to use this

A release passes when every row in section 3 has been proved or has been
explicitly and deliberately waived in that release's evidence record
(section 7).

Three things this checklist deliberately does **not** do.

It does not automate the release. Most rows need the user's hands, because
most claims here are about photographs and camera behaviour. That is a property
of the domain, not a gap.

It does not judge. `scripts/smoke.sh` reports device state and says in its own
header that it "does NOT judge whether a state is correct". This checklist
supplies the expected values that turn a report into a verdict.

It does not assume its own detector works. Section 4 names the two code paths
in `scripts/smoke.sh` that are measured defective, marks every row that rests
on them, and gives a healthy substitute command for each. That marking is the
point of this revision and is direct input to `DEC-20`.

---

## 2. The capability list (`F9.2-01`)

Derived by reading `ishtar-cam-modes/module.prop`'s `description` field in its
current, `IMPL-77`-corrected form, then adding the structural guarantees the
release makes through its installer and its guards.

**Count: 18 capabilities.** Sixteen are claimed in prose in `module.prop`
(`C-01` to `C-16`); two more (`C-17`, `C-18`) are claimed structurally by
`customize.sh` and `halpatch.sh` and are recorded as Ontology invariants 1 and
2. The count is reported after derivation, not from memory, and the group
boundary is kept visible so that a reader can tell a prose claim from an
enforced one.

The earlier enumeration in the sub-plan's section 6 counted **thirteen** claims
against the pre-`IMPL-77` description. That figure is superseded, not
contradicted: `IMPL-77` moved the version history out to `CHANGELOG.md` and
replaced the stale causal sentence, so the field now says different things.
Claims that moved to `CHANGELOG.md` (the launcher-icon fix, the restart
correction, the transition countdown) are **version history**, not standing
capabilities, and they are not carried here. That is the intended effect of
`ARC-10`'s resolution.

### Group A — claimed in `module.prop` prose

- `C-01` The main camera sensor driver (Sony IMX989) receives 12-bit, DCG and LN modes.
- `C-02` Mode `dcgB` measures roughly 25 percent less noise and twice the detail against stock.
- `C-03` Mode `dcgB` does not change shutter speed.
- `C-04` The 50MP FullRes HAL mode adds 8192x6144 to the **standard** Camera2 size list.
- `C-05` Third-party applications therefore capture at full resolution; measured at 50.3 MP in Open Camera.
- `C-06` Google Camera runs at a pinned 12.58 MP working resolution in this configuration.
- `C-07` The stated cause: `getOutputSizes()` drops any size whose minimum frame duration exceeds 1/20 s, and 8192x6144 measures 66,666,666 ns.
- `C-08` 50MP and the DCG/LN sensor modes are mutually exclusive.
- `C-09` Four QuickSettings tiles (50MP, DCG, LN4, LN2), mutually exclusive.
- `C-10` A WebUI exists.
- `C-11` An Action button exists.
- `C-12` The interface language is independent of the system language.
- `C-13` Video at 1080p60 and 4K60 is unaffected.
- `C-14` The 27 MB HAL binary is not shipped; only a 16-point patch list is kept, and the device's own stock binary is patched.
- `C-15` Version history lives in the project repository's `CHANGELOG.md`.
- `C-16` The module is for the Xiaomi 13 Ultra (`ishtar`) only.

### Group B — claimed structurally, by the guards

- `C-17` Reversibility. Every modification is a bind-mount or an md5-guarded offset patch, so the module can be turned off (Ontology invariant 1).
- `C-18` Fail-closed guards. A checksum or size mismatch aborts or degrades rather than writing (Ontology invariant 2).

### A live contradiction found while deriving this list

`ishtar-cam-modes/setmode.sh:211` prints, on every successful switch into
`50mp` mode:

```
     AGC 15,2 MP'de kaliyor -- GCam 8.4'un kendi siniri.
```

Both halves of that sentence are superseded. The figure is pre-`DEC-14`, and
the cause is the claim `EV-23` retired and `IMPL-77` replaced everywhere it
looked. `IMPL-77` corrected three instances — `module.prop` and both WebUI
note strings — and searched `Kullanim.txt` and `customize.sh`. It did not
search `setmode.sh`, whose stdout is a fifth user-visible surface.

This is raised as **`FIND-9.2-02` (P2, open)** and is **not** corrected here:
`Faz9.3` owns the documentation surfaces and is closed, editing a shipping file
forces a rebuild of the archive, and every prior change to shipped content in
this project has been the user's call. It is recorded in row `C-06` and `C-07`
of section 3 as a known contradiction between what the release claims and what
it prints.

A sweep of the whole module tree found **exactly this one** remaining instance.
`halpatch.sh:24` also names GCam 8.4, but it states a different and measured
fact — that the broad 8192x6144 emission crashes AGC (`IMPL-49`) — and it is a
source comment, not user-visible output. It is correct and is left alone.

---

## 3. Capability-to-command map (`F9.2-02`)

Coverage vocabulary: `smoke` (a `scripts/smoke.sh` field reports it), `host`
(provable on the host with no device), `user` (needs the user's hands or eyes),
`unverifiable` (explicitly marked, never omitted).

Detector column: `healthy`, or the finding ID of the defect the row's smoke
path rests on. Proof column cites a command from section 3a.

| ID | Capability | Proof | Coverage | Detector |
|---|---|---|---|---|
| C-01 | Sensor driver gets 12-bit/DCG/LN | PC-01 | smoke | healthy |
| C-02 | dcgB 25 pct less noise, 2x detail | PC-02 | user | healthy |
| C-03 | dcgB leaves shutter speed alone | PC-03 | user | healthy |
| C-04 | 8192x6144 in the standard list | PC-04 | smoke | FIND-3.10-01 |
| C-05 | Third-party app captures 50.3 MP | PC-05 | user | healthy |
| C-06 | AGC pinned at 12.58 MP | PC-06 | smoke | healthy |
| C-07 | The 1/20 s duration mechanism | PC-07 | smoke | healthy |
| C-08 | 50MP excludes DCG and LN | PC-08 | host | healthy |
| C-09 | Four tiles, mutually exclusive | PC-09 | user | partial, IMPL-75 |
| C-10 | A WebUI exists | PC-10 | host | healthy |
| C-11 | An Action button exists | PC-11 | user | healthy |
| C-12 | UI language independent of locale | PC-12 | user | healthy |
| C-13 | Video 1080p60 and 4K60 unaffected | PC-13 | user | healthy |
| C-14 | 27 MB binary not shipped | PC-14 | host | healthy |
| C-15 | Version history in CHANGELOG.md | PC-15 | host | healthy |
| C-16 | Xiaomi 13 Ultra only | PC-16 | host | healthy |
| C-17 | Reversibility | PC-17 | smoke | FIND-3.7-02 |
| C-18 | Fail-closed guards | PC-18 | host | healthy |

**Coverage totals: 18 of 18 have a proving command. None is unverifiable.**
By class: 5 `smoke`, 6 `host`, 7 `user`. Two rows rest on a defective smoke
path (`C-04`, `C-17`) and one is partially covered (`C-09`); all three are
detailed in section 4.

### 3a. The proving commands

Commands are listed here rather than inside the table because a literal pipe
inside a Markdown cell splits the cell.

```sh
# PC-01  Sensor variant, identity and mount, from one snapshot.
#        Expect sensor.live.variant to equal the selected mode, and
#        sensor.mount.count = 1. Stock is 9e4d0fe1a8bf2eb4146c9917a0ac2c4c.
scripts/smoke.sh -o snapshots/<YYYYmmdd-HHMM>__release__<label>

# PC-02  A/B photographs, stock against dcgB, same scene and light.
#        Compare noise and detail. This is a one-time measurement recorded in
#        50MP-Entegrasyon-Plani.md, not a per-release check; a release repeats
#        it only when the sensor blobs change.

# PC-03  Shutter speed unchanged: read ExposureTime from the EXIF of one
#        stock and one dcgB capture. Equal values prove the claim; the images
#        need not match in any other respect.

# PC-04  8192x6144 present in the standard list. DEFECTIVE via smoke.sh, see
#        section 4. Healthy substitute, tag-header slicing on a single dump:
adb shell "dumpsys media.camera" > cam.dump
awk '/^      android\.scaler\.availableStreamConfigurations \(d000a\)/,/^      [a-z]/' cam.dump | grep 8192

# PC-05  Open Camera at full resolution. One human shutter press, then read
#        the JPEG SOF marker for real dimensions. Never trust the filename or
#        the on-screen label. Expect 8192x6144 = 50.33 MP.

# PC-06  AGC pin. From the same snapshot as PC-01, expect
#        agc.pref_48m = 0, agc.pref_resolution = full,
#        agc.photo_size.back.derived = 4096x3072, agc.photo_size.back.mp = 12.58.
#        Then one capture, black fraction below 0.01 by the IMPL-40 method.
#        Expected configured streams, read with AGC open in a SINGLE dump:
adb shell "dumpsys media.camera" | grep -A6 "Stream\[[0-9]\]:"
#        YUV and RAW10 must BOTH read 4096 x 3072; the matching pair is the point.

# PC-07  The mechanism. Read the d000b minimum-frame-duration row for
#        8192x6144 and expect 66666666. Slice by tag header, never by line
#        range; the dump prints int64 tables two values per line, so a
#        four-tuple row spans two lines.
awk '/^      android\.scaler\.availableMinFrameDurations \(d000b\)/,/^      [a-z]/' cam.dump

# PC-08  Exclusion, from the source dispatch. setmode.sh:179-190 maps 50mp to
#        SENSOR_MODE=stock and every sensor mode to HAL_WANT=stock, so the two
#        cannot coexist by construction. Confirm on device by switching modes
#        and re-reading hal.state and sensor.live.variant in one snapshot.
sed -n '178,191p' ishtar-cam-modes/setmode.sh

# PC-09  Tiles. Four tiles present and mutually exclusive, checked by eye in
#        QuickSettings after a switch. See section 4 for why the scripted
#        readback is only partial.
adb shell "su -c 'sh /data/adb/modules/ishtar_cam_modes/action.sh tiles status'"

# PC-10  WebUI ships and is non-empty.
python scripts/build-release.py --list | grep webroot

# PC-11  Action button: invoke Action from the KernelSU manager and confirm it
#        advances the mode and reports the new one.

# PC-12  Language independence: set the module language opposite to the system
#        language and confirm the WebUI and Action text follow the module.
adb shell "su -c 'sh /data/adb/modules/ishtar_cam_modes/action.sh lang'"

# PC-13  Video. Record 1080p60 and 4K60, pull, and read dimensions from the
#        MP4 tkhd box, not the filename. For a version 0 tkhd the 16.16 width
#        sits at body+24+52. Precedent and the dcgB video caveat are in
#        docs/regression-v2.1.md section 6.

# PC-14  No 27 MB binary in the archive. This is now assertion-backed: the
#        build aborts on any entry at or above 8 MiB (A2), and the largest
#        legitimate entry is a 1062250-byte sensor blob.
python scripts/build-release.py --self-test

# PC-15  Version history present and pointed to. module.prop names
#        "proje deposundaki CHANGELOG.md" and CHANGELOG.md declares itself the
#        owner. Note that CHANGELOG.md is a REPOSITORY file and is deliberately
#        not inside the archive, which is what the description says.
grep -n "CHANGELOG" ishtar-cam-modes/module.prop && head -8 CHANGELOG.md

# PC-16  Device guard. customize.sh:5-9 reads ro.product.device and
#        ro.product.vendor.device and aborts on anything but ishtar.
sed -n '5,10p' ishtar-cam-modes/customize.sh

# PC-17  Reversibility. hal.mount.count and sensor.mount.count must each read
#        exactly 1; a count above 1 is the stacked-mount case that produces a
#        false restore. The smoke fields themselves are healthy; the row is
#        marked because the trap audit in the same probe is not. See section 4.

# PC-18  Fail-closed. Read the guards: hal_seed refuses to run while the target
#        is mounted and requires the stock checksum to match; customize.sh
#        aborts on a sensor checksum mismatch and degrades, without aborting,
#        on an unrecognised HAL checksum.
grep -n "abort\|HAL_STOCK_MD5\|EXPECT_SIZE" ishtar-cam-modes/customize.sh ishtar-cam-modes/halpatch.sh
```

---

## 4. The three rows whose detector is not sound (`DEC-20` input)

This section exists because building a release surface on an unexamined
detector is how a checklist becomes a ritual.

> **Repaired 2026-09-06 (`IMPL-80`), on the user's `DEC-20` decision: repair the
> script.** Both defects below are now fixed in `scripts/smoke.sh`, which is no
> longer byte-untouched. The analysis is kept as written — it is the reason the
> repair took the shape it did — and each subsection carries its own outcome
> note. `4c` is a scope limit, not a defect, and is unchanged.

### 4a. `FIND-3.7-02` — the trap audit counts names, not values

`scripts/smoke.sh:110-112` collects preference key *names* matching
`pref_raw_key*` and `pref_fix_resolution_key*`, then reports
`prefs.trap.count` as a word count of that list. It never reads a value.

The consequence is measured, not hypothetical. This device currently carries
**two trap keys present and both set to value 0** — a state that is harmless.
A release gate written as "assert `prefs.trap.count` is 0" would **fail a good
device**. The correct check is a per-key value audit, and
`docs/agc-12mp-configuration.md` section 3 already says so in its expected-fields
table: *audit the values, not the count*.

Affects `C-17`, which shares the probe. The two fields `PC-17` actually reads —
`hal.mount.count` and `sensor.mount.count` — are computed separately at
`smoke.sh:81` and `:94` and are sound; the row is marked so that a reader does
not take the whole `probe_app` block as trustworthy.

**Repaired (`IMPL-80`).** `prefs.trap.count` and `prefs.trap.keys` are left
byte-unchanged, so snapshots taken before the repair still diff against later
ones on those lines. Two fields are added beside them:

- `prefs.trap.armed` — the count of trap keys whose value is neither `0` nor
  `false`. **This is the field a release gate should assert is 0.**
- `prefs.trap.values` — the `name=value` pairs the audit actually read.

Proven against fixtures before it ever reached a device: a healthy device with
both keys present at 0 reports `count=2, armed=0`; arming one key moves it to
`armed=1`; absent keys report `0` and `0`. The comparable region grows by
exactly two lines, which is expected and is the only snapshot churn.

### 4b. `FIND-3.10-01` — a line-range slice across two different dumps

`probe_main_rows()` at `scripts/smoke.sh:186-198` computes `start` and `end`
from `CAM_RAW`, which was captured by the `dumpsys media.camera` at line 148.
It then issues a **second, independent** `dumpsys media.camera` at line 196 and
slices *that* output with `sed -n "${start},${end}p"`.

The two dumps are separate invocations and do not have stable line counts.
`docs/agc-12mp-configuration.md` records the measurement: six consecutive calls
returned **65530 / 50666 / 50666 / 50666 / 65530 / 65529** lines with nothing
changing on the device. So the `camera.halN.stream_config.rows` block lands
correct, short, or long **at random, and silently** — there is no error path,
because a wrong line range is still a valid line range.

Affects `C-04`, which is exactly the claim that block would prove.

**Repaired (`IMPL-80`).** `probe_main_rows()` no longer computes line numbers
and no longer issues a second `dumpsys`. The block is located inside the *same*
invocation that produces it, by boundary rather than by line number: the camera
block opens at its own static-information header and closes at the next one; the
tag block opens at the `d000a` header and closes at the next tag header, the
six-space `android.` indent level. That is `PC-04`'s substitute folded back into
the instrument, which is exactly what this section asked for.

The awk program contains no `'` — `sh_root` wraps every payload in `su -c '...'`
— and no `$`, so no shell layer between the host and the device can rewrite it.
Proven against a three-camera fixture: `id=0` returns only its own rows and
stops at the `d000b` header, and `id=1` does not match `vendor_qti/10`.

The snapshot-diff command in `docs/agc-12mp-configuration.md` section 3 already
filters this block out for exactly this reason, which is why snapshot
comparison has stayed reliable while this defect has been open.

### 4c. `C-09` — the tiles readback reports a different thing than it names

`IMPL-75` corrected `action.sh tiles status` so that its `status` field reports
`takma_ad` — the *activity alias*, not the launcher drawer state — and so that
`tiles hide` no longer asserts a result it cannot verify. That correction made
the output honest, but it did not make it a proof of tile *presence and mutual
exclusion*, which is what `C-09` claims. The exclusion half is proved by eye in
QuickSettings after a mode switch.

Not a defect; a scope limit, recorded so the row is not read as automated.

### What this means for `DEC-20`

Two of eighteen capabilities cannot be proved by the smoke script as written,
and one of the two is the flagship 50 MP claim. Both have a working substitute
command that this checklist supplies, so the release is not blocked — but the
substitutes live here, in prose, rather than in the detector, which means the
release surface currently depends on a human reading this section.

That was the cost of leaving `DEC-20` open, stated in release terms.

> **Discharged 2026-09-06 (`IMPL-80`).** The user decided `DEC-20` in favour of
> repairing the script, and both substitutes are now folded back into the
> instrument: `C-04` and `C-17` are provable by the same single command as the
> rest, and the release surface no longer depends on a human reading this
> section. The prose substitutes are kept because they document the reasoning
> and remain valid as an independent cross-check.
>
> **Not yet run on the device.** The repair is proven against fixtures, not
> against the phone; the first real run is part of `VAL-INSTALL`.

---

## 5. The known-bad construction (`F9.2-03`)

`VAL-KNOWNBAD` requires proving the verification surface reports a wrong state
differently from a good one. Three constructions were considered; the
requirement is that it be detectable, honest, and safe.

| Option | Detected by | Risk | Verdict |
|---|---|---|---|
| Stale mode file | mode.file against hal.state | none, self-heals at boot | **chosen** |
| Absent or extra mount | hal.mount.count | moderate, touches live mounts | rejected |
| Mismatched checksum | hal.live.md5 and hal.state | high, writes to the HAL | rejected |

**Chosen: the stale mode file.** Write a mode value into
`/data/adb/modules/ishtar_cam_modes/mode` that disagrees with the layers
actually installed — for example `dcgB` while the HAL is `fullres` and the
sensor is stock — then take a snapshot and confirm it reports
`mode.file = dcgB` beside `hal.state = fullres` and
`sensor.live.variant = stock`. A good state has these three agreeing; the
known-bad state has them disagreeing, and the difference is visible in one
`diff` of the comparable region.

**Safety rationale, three independent reasons.**

First, it writes to no camera component. The `mode` file is the module's own
bookkeeping; the sensor blob, the HAL binary and their mounts are untouched,
so the camera stack cannot be affected by the test.

Second, it self-heals. `post-fs-data.sh:14-26` maps any absent or unrecognised
mode value to `stock` across all three variables, so even an abandoned test
resolves at the next boot. This is the same normalization `F9.1-04` relies on.

Third, it is reversible without the module. Recovery is one `echo` into a plain
file, and if the module is what broke, `docs/recovery-runbook.md` section 4
covers it — the runbook was written not to depend on module commands.

The rejected options are recorded because the rejection is the useful part.
The mount option would exercise `hal_umount_all`'s forty-iteration loop, which
is the stacked-mount failure the runbook exists for — deliberately provoking it
to test a *reporter* trades a real risk for information the runbook already
documents. The checksum option would write to the HAL binary, which is the one
thing `QAS-01` names as the path to a device with no camera until reflash.

**Procedure, held pending approval:**

1. Snapshot the good state: `scripts/smoke.sh -o <ts>__Faz9.2__knowngood`.
2. Back up the mode file to `/data/local/tmp/`.
3. Write the disagreeing value.
4. Snapshot again as `<ts>__Faz9.2__knownbad`.
5. Diff the comparable regions and confirm the three fields disagree.
6. Restore the mode file and take a third snapshot confirming return to good.

Steps 3 and 6 change device state. **Not run. Awaiting the user's approval.**

---

## 6. The demonstration (`F9.2-04`) — run 2026-09-06, **PASS**

Section 5's procedure was approved by the user and executed by `IMPL-81` on the
device, against the freshly installed **v2.2** module. All seven steps ran; the
device was returned to its known-good state and left there.

| Step | Artifact | Result |
|---|---|---|
| 1. good snapshot | `snapshots/20260906-2055__Faz9.2__F9204-knowngood.txt` | taken |
| 2. mode backed up | `/data/local/tmp/mode_backup_IMPL80.txt` = `50mp` | taken |
| 3. write disagreeing value | `dcgB` written into the module `mode` file | applied |
| 4. bad snapshot | `snapshots/20260906-2055__Faz9.2__F9204-knownbad.txt` | taken |
| 5. diff good vs bad | one line differs: `mode.file 50mp` to `dcgB` | **detected** |
| 6. restore | `mode` restored from the backup | applied |
| 7. restored snapshot | `snapshots/20260906-2056__Faz9.2__F9204-restored.txt` | taken |

**The verdict, and why it is the one `Main-Planing` asked for.** The good state
and the bad state are reported *differently*, and the difference is exactly the
intended one and nothing else. In the known-bad snapshot the three fields
disagree as designed:

```
mode.file                       = dcgB
sensor.live.variant             = stock
hal.state                       = fullres
```

A `dcgB` mode requires the dcgB sensor blob and a stock HAL; the file claims
`dcgB` while the layers are stock sensor and *fullres* HAL. The reporter
surfaces that disagreement rather than hiding it, which is the whole claim.

**Restoration verified, not assumed.** The comparable region of the restored
snapshot is **byte-identical** to the known-good one — the diff is empty — so
the test left no residue. A later closing bracket
(`snapshots/20260906-2101__Faz9.2__IMPL80-closing-bracket.txt`), taken after the
unrelated `FIND-6.2-03` stock-mode capture and the return to `50mp`, is also
byte-identical to the known-good region.

**Scope, stated so the result is not over-read.** This proves the surface
distinguishes a stale `mode` file from a consistent state. It does not prove the
surface would detect every possible wrong state; the two constructions rejected
in section 5 remain untested, deliberately, because testing them costs more risk
than the information is worth.

---

## 6a. `VAL-INSTALL` — run 2026-09-06, **PASS**

The gate that eight evidence rows and two sub-plans were waiting on.
`dist/ishtar-cam-modes-v2.2.zip` was pushed, its md5 re-verified **on the
device** as `e95789572311cc95266d3ab4045cdcba`, installed with
`ksud module install`, and activated by a real reboot (uptime fell from 29798 s
to 40.9 s, checked rather than assumed).

- The installer banner printed `ishtar IMX989 Camera Modes  v2.2`, which is the
  `customize.sh:2` site the version-bump gate warned about. Verified live.
- `ksud module list` reports `v2.2 / 13`, enabled, with the reduced description
  at 1107 characters.
- `setmode.sh 50mp` printed the corrected AGC sentence on the device, which
  closes the loop on `FIND-9.2-02` at the surface a user actually sees.
- Pre-install versus post-install comparable regions differ in **exactly two
  lines**, `module.version` and `module.versionCode`. Mode, HAL identity, HAL
  state, both mount counts, sensor variant, the trap fields and the derived
  photo size are all unchanged.

**`FIND-9.1-04` is now CONFIRMED as a real defect, not an open question.**
`customize.sh:62` promises `guncellemede mevcut mod`. Measured: the staged
`/data/adb/modules_update/ishtar_cam_modes/` directory contained **no `mode`
file**, and that directory replaces the live one at reboot, so
`post-fs-data.sh:14-26` would have normalized the absent value to `stock`. A
user upgrading in place would have silently lost 50MP mode. `IMPL-81` copied the
mode file into the staged directory before rebooting, which is what the
installer itself should do; the promise in `customize.sh:62` is still unmet in
the shipped tree and the repair belongs to a sub-plan that owns `customize.sh`.

**Still not done: `VAL-MANUAL`.** The seven user-performed rows have not been
exercised, so the eight `pending` evidence rows are now *unblocked* rather than
*passed*, and none was reclassified on the strength of this install alone.

---

## 7. Per-release evidence record (`F9.2-08`)

The format ties verification results to a specific archive, so regression
evidence lives with the release instead of in a conversation. `docs/regression-v2.1.md`
is the precedent for per-mode depth; this record is deliberately shallower and
wider — one line per capability, plus the archive's identity.

**Format.** A record has three parts: archive identity (path, entry count, byte
size, md5, sha256, and the manifest it was generated against), a result line per
capability (`C-nn`, one of `pass` / `fail` / `waived` / `pending`, the evidence
path, and the date), and a closing statement of what was waived and why.

A capability may be `waived` only with a reason. `pending` is not a pass and a
release does not ship on it.

### Record — release v2.2 (built 2026-09-06, `IMPL-80`)

**Archive identity.**

| Field | Value |
|---|---|
| Path | dist/ishtar-cam-modes-v2.2.zip |
| Entries | 43 |
| Bytes | 1009107 |
| md5 | e95789572311cc95266d3ab4045cdcba |
| sha256 | 407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0 |
| Manifest | docs/release-manifest.md, regenerated against exactly this archive |
| Built by | scripts/build-release.py, IMPL-77, 2026-09-06 |

**Results.**

| Capability | Result | Evidence | Date |
|---|---|---|---|
| C-01 | pending | needs VAL-INSTALL | — |
| C-02 | waived | one-time measurement, blobs unchanged this release | 2026-09-06 |
| C-03 | waived | one-time measurement, blobs unchanged this release | 2026-09-06 |
| C-04 | pending | needs VAL-INSTALL, prove with PC-04 substitute | — |
| C-05 | pending | needs VAL-INSTALL and one shutter press | — |
| C-06 | pass | docs/agc-12mp-configuration.md, IMPL-61 four axes | 2026-09-05 |
| C-07 | pass | Ontology invariant 7, OQ-15, agc-50mp-yama/README.md | 2026-09-06 |
| C-08 | pass | setmode.sh:179-190 read this session | 2026-09-06 |
| C-09 | pending | needs VAL-INSTALL, exclusion checked by eye | — |
| C-10 | pass | build-release.py contents specification, webroot included | 2026-09-06 |
| C-11 | pending | needs VAL-INSTALL | — |
| C-12 | pending | needs VAL-INSTALL | — |
| C-13 | pending | needs VAL-INSTALL, see regression-v2.1.md section 6 | — |
| C-14 | pass | build-release.py --self-test, assertion A2 proven to fire | 2026-09-06 |
| C-15 | pass | CHANGELOG.md header, module.prop points to it | 2026-09-06 |
| C-16 | pass | customize.sh:5-9 read this session | 2026-09-06 |
| C-17 | pending | needs VAL-INSTALL, mount counts must each read 1 | — |
| C-18 | pass | customize.sh and halpatch.sh guards read this session | 2026-09-06 |

**Totals: 8 pass, 2 waived, 8 pending. Zero fail.**

**What the pending rows share.** All eight need the archive to be installed.
`VAL-INSTALL` has never been run for this archive — it was offered to the user
and not taken — so **the device is running module content installed before
`IMPL-75` and `IMPL-77` changed `action.sh`, `Kullanim.txt`, `module.prop` and
`webroot/index.html`.** Device evidence gathered today describes the *previous*
content, not this archive. That is why those rows read `pending` and not `pass`,
and stating it is the whole reason this format separates archive identity from
results.

**Waivers.** `C-02` and `C-03` are one-time sensor measurements recorded in the
journal. The sensor blobs are byte-unchanged in this release, so the claims are
carried forward rather than re-measured. A release that changes any file under
`ishtar-cam-modes/blobs/` must clear these waivers.

### Release gates outstanding

All four gates below were **discharged on 2026-09-06 by `IMPL-80`**, on the
user's explicit instruction. They are kept here with their outcome rather than
deleted, so the release record shows what was closed and how.

- **The version bump — done.** All three sites moved together to `v2.2` /
  `versionCode=13`: `module.prop:3`, `module.prop:4`, and `customize.sh:2`,
  which prints the banner during installation. `CHANGELOG.md` gained a `v2.2`
  entry, and the `IMPL-75` note under `v2.1` that deferred this decision to
  Faz 9.2 is marked resolved in place. The archive filename follows the version
  automatically — `build-release.py` derives it from `module.prop`.
- **`FIND-9.2-02` — fixed.** `setmode.sh:211` no longer prints the superseded
  claim. Both halves were wrong: the figure was pre-`DEC-14` and the cause was
  the one `EV-23` retired. The replacement states the measured cause and matches
  `module.prop`'s wording, so the two surfaces now agree. A repeat sweep of the
  module tree finds no further instance; `halpatch.sh:24` names GCam 8.4 for a
  *different, measured* fact and is a source comment, and was left alone.
- **`FIND-9.1-03` — addressed, `DEC-10` decided by standard practice.** The key
  is a *self-signed debug keystore the script generates itself*, not a release
  key, and it never ships (assertion A1). Its password is therefore not a
  secret, exactly as Android's own `debug.keystore` password (`android`) is
  public — and keys are randomly generated, so knowing the password does not
  reproduce this one. `build.sh` now takes `KS`, `KS_PASS` and `KS_ALIAS` from
  the environment with the previous values as defaults, so behaviour is
  unchanged by default and a real key needs no edit. The file states the posture
  and warns that an APK signed with a different key will not update over an
  installed copy.
- **`DEC-20` — decided and repaired**, section 4. Both detectors are fixed and
  proven against fixtures; the first device run is part of `VAL-INSTALL`.

---

## 8. What this closes, and what it does not

**Closed.** `F9.2-01` — eighteen capabilities enumerated and counted from the
corrected description. `F9.2-02` — every one has a proving command, none
marked unverifiable, with coverage classified and detector health stated per
row. `F9.2-03` — the known-bad construction chosen with three independent
safety reasons and two rejections recorded. `F9.2-08` — the evidence record
format defined and filled in for the pending release.

**Not closed.** `F9.2-04` / `VAL-KNOWNBAD` — designed in section 5, awaiting
approval, because it changes device state. `VAL-MANUAL` — the seven
user-performed rows have not been exercised as written. The `CQ-09` half of
`F9.2-09` remains, `ARC-11` having already been carried to `convergent` by
`IMPL-19`.

**Not this document's to close.** `DEC-20`. Section 4 is the input, not the
decision.

---

## 9. Two-way consistency check (`F9.3-08` / `VAL-CONSISTENCY`)

`Faz9.3` section 10 sequences this check after `Faz9.2` writes the capability
list, because it compares the corrected `module.prop` description against that
list in both directions. Run 2026-09-06, immediately after sections 2 and 3.

**Direction 1 — every description claim reaches the checklist.** The
description was read clause by clause. It makes fifteen claim statements, which
yield sixteen capabilities (the WebUI and Action button share one sentence and
split into `C-10` and `C-11`). Every one maps to a `C-nn` row in section 3.
**No description claim is missing from the checklist.**

**Direction 2 — every checklist capability traces to a source.** `C-01` to
`C-16` each trace to a description clause. `C-17` and `C-18` have no description
sentence and are declared as Group B, sourced to `customize.sh`, `halpatch.sh`
and Ontology invariants 1 and 2. **No capability is orphaned or silently
invented.**

**Coverage cross-check.** All eighteen have a proving command and none is
marked unverifiable, so the description does not claim anything this checklist
cannot prove.

**Verdict: consistent.** The corrected description and the capability checklist
agree in both directions.

**One defect found, and it is outside both artifacts.** The description is
consistent with the checklist, but the module's *runtime output* is consistent
with neither: `setmode.sh:211` prints the superseded 15.2 MP claim and its
retired cause on every switch into `50mp`. That is `FIND-9.2-02`, recorded in
section 2. `VAL-CONSISTENCY` compared two documents and found them aligned; the
gap it exposed is that a third surface was never in `Faz9.3`'s scope of four.
