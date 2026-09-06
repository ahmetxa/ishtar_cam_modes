# AON fix — disposition, and the verification that is owed

Produced by **Faz 6.2** (`IMPL-72`, 2026-09-06). Host-side static analysis only;
no device command was issued and no build exists yet.

This document carries three things: the role decision for `ishtar-aon-fix` with
the reasoning behind it, the verification procedure that Phase 7 must run, and
the response if that verification fails. It is written now, while the reasoning
is current, precisely so Phase 7 does not have to reconstruct it.

**Nothing here is verified.** Faz 6.1 added a device-tree entry whose effect
cannot be observed until a build exists. `ARC-06` stays `divergent` until
section 5 is executed.

## 1. The two mechanisms, kept distinct

The project has two independent ways of making
`/vendor/lib64/camera/aon_front.pb` exist. They must not be conflated, because
the verification exists to tell them apart.

| | Mechanism | Where | State |
|---|---|---|---|
| **A** | Runtime bind mount | `ishtar-aon-fix/post-fs-data.sh` | Working, in use, **never verified** (`TRACE-13` records no test) |
| **B** | Device-tree symlink | `device_ishtar/proprietary-files.txt:1031` and `refs/a16_ishtar/proprietary-files.txt:1037` | Edit complete (`IMPL-03`), **effect unverified** |

Both name the same source and target: `SRC=/odm/lib64/camera/aon_front.pb`,
`TGT=/vendor/lib64/camera`. Entry B's syntax was not invented — it was copied
from `refs/neo_ishtar/proprietary-files.txt:1154`, which carries the identical
declaration for the identical device.

The repaired chain is AON → CSS → NCS, and its observable product is four NCS
providers: **aperture, OIS, laser AF (ToF), and face-scene**.

## 2. Population analysis (`F6.2-01`)

Two populations coexist, and they need different things.

- **Already-built ROMs** — every install of every ROM built before entry B
  lands in a shipped build. Mechanism A is the *only* fix for them. This
  population does not shrink when the fix ships; it shrinks only as individual
  users flash a newer build, and it never reaches zero while anyone stays on an
  older ROM. Treat it as permanent for planning purposes.
- **Future builds** — any build produced from a tree carrying entry B. For
  these, mechanism B should make mechanism A unnecessary.

**The decisive fact, and it was not anticipated when this sub-plan was
written.** The two mechanisms do not conflict, because mechanism A
**self-disables in the presence of mechanism B**:

```sh
# ishtar-aon-fix/post-fs-data.sh:13-16
if [ -e "$TGT/aon_front.pb" ]; then
  log -t $TAG "zaten mevcut, mudahale yok"
  exit 0
fi
```

If the device-tree symlink has created the path, the module logs *"already
present, no intervention"* and exits before touching anything. There is no
double mount, no shadowing, and no ordering hazard.

The consequence for the decision: **keeping the module costs a future-build user
nothing**. The usual argument against retaining a superseded workaround — that
it lingers and interferes — does not apply here. That is an evidence-based
input to `DEC-04`, not a preference.

It also hands the verification a free signal, which section 5 uses: the module's
own log line reports which mechanism won, without removing anything.

## 3. The three roles evaluated (`F6.2-02`)

All three are assessed, not only the recommended one.

### Keep separate

**For.** The self-disable guard makes the cost to future builds zero (section
2). The already-built population is permanent and needs mechanism A. The
module's independence from KernelSU module mounting is deliberate — `module.prop`
states it, Autopsy section 3 calls it "a deliberate resilience choice worth
preserving", and `post-fs-data.sh` implements it by establishing its own
`mount --bind` rather than relying on the overlay. And the two modules serve
different audiences: the AON repair is an **unconditional** fix every affected
user needs, while `ishtar-cam-modes` is an **optional** enhancement for users who
want 50MP/DCG/LN.

**Against.** Two artifacts to install and to release, which cuts against Phase
9's consolidation goal.

### Merge into `ishtar-cam-modes`

**For.** One artifact, which is what Phase 9 points toward.

**Against, and this is the substantive objection.** It couples an unconditional
repair to an optional enhancement: a user who wants working aperture, OIS,
laser AF and face-scene would have to install the camera-modes module to get
them, and a user who removes the camera-modes module would silently lose four
capabilities that have nothing to do with sensor modes. It also puts the AON
repair's lifecycle inside a module whose own mounting story is different,
which is exactly the property Autopsy flags as deliberate. Consolidation is a
packaging benefit; this is a correctness cost.

### Plan for retirement after verification

**For.** It is the endpoint Main-Planing section 6 gestures at.

**Against.** It is premature *by definition* — retirement is conditional on a
verification that cannot run yet, and it would abandon the permanent
already-built population. Note that Main-Planing's own wording, "keep the
runtime module only as a fallback for already-built ROMs", describes
keep-separate with a narrowed scope, not retirement.

### Recommendation

**Keep separate.** The self-disable guard removes the only real cost, the
already-built population is permanent, and merging trades a correctness
property for a packaging convenience. Revisit the *scope* of the module's role —
not its existence — after section 5 passes.

## 4. The decision (`F6.2-03`) — `DEC-04`, routed to the user

Main-Planing section 9 lists this among the four decisions needing human
confirmation. **The implementer recommends; the user chooses.** This document
records the recommendation and its evidence.

**ANSWERED 2026-09-06 (`IMPL-75`): keep separate.** The user accepted the
recommendation of section 3, on its two evidence-based inputs -- the
`post-fs-data.sh:13-16` self-disable guard, which makes the future-build cost
zero, and the coupling objection, that merging would tie an *unconditional*
repair to an *optional* enhancement. `ishtar-aon-fix` therefore remains a
separate artifact, keeping the KernelSU-mount independence that `module.prop`
declares and `post-fs-data.sh` implements with its own `mount --bind`.

**What the decision does not settle.** It fixes the module's *existence*, not
its *scope*. Section 3 recommended revisiting scope -- not existence -- once
`VAL-BUILD` passes, and that remains open for Phase 7: if verification shows the
device-tree entry carries every affected build, the module's stated role narrows
to the already-built population, which is exactly what Main-Planing describes as
"keep the runtime module only as a fallback for already-built ROMs". Retirement
was rejected as premature, not as wrong: it is conditional on a verification
that cannot run before Phase 7.

No merge has been performed. No module has been removed or disabled.

## 5. Verification procedure (`F6.2-04`, `F6.2-07`) — `VAL-BUILD`, deferred to Phase 7

The procedure covers **both** mechanisms, per `F6.2-07`: `TRACE-13` records that
mechanism A has never been verified either, so this is the first check the AON
capability has ever had.

### Step 0 — capture the positive baseline FIRST, before anything is removed

**This step is an ordering requirement, not a formality.** "The four providers
appear" is not a recognizable result unless it is known what their appearance
looks like on a system where they are known to work. The current device — mechanism
A installed and working — is that system, and it is available *now*; after the
module is removed it is not.

Capture, on the current device with `ishtar-aon-fix` installed:

1. `ls -l /vendor/lib64/camera/aon_front.pb` — record whether it is a real file
   inside the module's bind mount or a symlink.
2. `logcat -d -s ishtar_aon_fix` — record which of the module's three outcome
   lines was emitted this boot (see step 2's table).
3. The camera-stack log across one camera open, filtered to the provider
   creation messages for aperture, OIS, laser AF and face-scene. **Record the
   exact matching strings**; they become the grep patterns every later step uses.

Store as `snapshots/<ts>__Faz6.2__aon-baseline.txt`. Until this exists, a
negative result in Phase 7 is uninterpretable — it cannot be distinguished from
"looked for the wrong string".

*Not performed by `IMPL-72`: it needs a device action and a camera start, and
device actions require the user's approval.*

**EXECUTED 2026-09-06 by `IMPL-75`, and it did not return a positive
baseline. Read section 8 before using any part of this step.** The premise
written above -- "the current device, mechanism A installed and working, is
that system" -- is the half that failed: mechanism A is installed and its
mount is active, and the providers still do not appear.

### Step 1 — confirm the entry is in the tree the build actually consumed

On a build that includes it, the entry is expected at
`refs/a16_ishtar/proprietary-files.txt:1037`. Confirm it is present in the
checkout the build ran from — not merely in this workspace — with
`grep -n 'aon_front.pb;SYMLINK=' <build-tree>/proprietary-files.txt`.

Conclusive: exactly one match. A zero match means the build never saw the fix
and the rest of the procedure proves nothing about it.

### Step 2 — read the module's own verdict, module still installed

This is the cheap discriminator and it costs one command. `post-fs-data.sh`
emits exactly one of three lines under tag `ishtar_aon_fix`:

| Log line | Meaning |
|---|---|
| `zaten mevcut, mudahale yok` | The path already existed → **mechanism B worked** |
| `OK: bind mount kuruldu -> /vendor/lib64/camera` | The module created it → **mechanism B did not work** |
| `HATA: kaynak yok: /odm/lib64/camera/aon_front.pb` | The source blob is missing → neither mechanism can work; a different defect |

Run `logcat -d -s ishtar_aon_fix` on first boot of the new build. This gives a
verdict on entry B **without removing anything**, which makes it safe to run
before step 3 commits to a module-less boot.

**MEASURED UNRELIABLE (`IMPL-75`, `FIND-6.2-02`).** On a device whose mount is
demonstrably active, `logcat -d -b all -s ishtar_aon_fix` returned **nothing** --
not even the unconditional `basliyor` of `post-fs-data.sh:10`. `post-fs-data`
runs before `logd` is serving, so the lines are not in any buffer by the time a
session can read them. **Use the mount-identity test of section 8 instead.** It
answers the same question, is not time-limited, and needs no log at all.

### Step 3 — the conclusive check, module absent

Uninstall `ishtar-aon-fix`, reboot, then:

1. `ls -l /vendor/lib64/camera/aon_front.pb` — **conclusive result: it exists
   and is a symlink to `/odm/lib64/camera/aon_front.pb`.** Absent means entry B
   failed.
2. Open the camera and match the four provider strings recorded in step 0.
   **Conclusive result: all four present.** Fewer than four is a failure, and
   *which* are missing is the diagnostic.

A pass requires both. The path existing without the providers appearing is a
distinct outcome and is handled in section 6.

### Step 4 — verify mechanism A, which nothing has ever checked (`F6.2-07`)

Still on the new build, reinstall the module and reboot. Expect the step 2 table's
first line (`zaten mevcut`), which confirms the guard behaves as read. Then, on
a build or device where the path does **not** exist natively, confirm the module
produces the path and the four providers — that is the check `TRACE-13` records
as never having been performed, and the already-built population depends on it.

## 6. Negative-result response (`F6.2-06`), specified before the build exists

| Outcome | Response |
|---|---|
| Path absent, module removed | Entry B did not take effect. Check in order: the entry is in the consumed tree (step 1); the ROM's extract-utils honours `;SYMLINK=` for this path; `/vendor/lib64/camera/` exists in the built image. **Module role unchanged — it stays.** `ARC-06` stays `divergent`. Fix the entry and re-run from step 1. |
| Path present, fewer than four providers | The symlink is necessary but not sufficient: a second defect exists in the AON → CSS → NCS chain. **Module role unchanged.** This also newly implicates mechanism A, which was assumed to be a complete fix and has never been verified — open an investigation rather than assuming either mechanism is whole. |
| `HATA: kaynak yok` | The `/odm` source is absent on this build. Neither mechanism can work; this is a blob-extraction defect, not an AON defect, and it belongs to the build, not to this document. |
| Path present, four providers present | **Entry B confirmed.** Mechanism B becomes the fix for future builds; mechanism A narrows to a fallback for the already-built population. `ARC-06` may move to `convergent` **for future builds only**, and the qualification must be carried — it does not converge for already-built ROMs. |

In no outcome is the module removed or merged on the strength of an unverified
edit. That constraint is from section 5 of the sub-plan and it survives every
branch above.

## 7. Registration (`F6.2-05`) — and one finding

`F6.2-05` asks that this procedure be registered as a Phase 7 acceptance item
**and referenced from `Faz7.2`**.

The first half is done: this document is the registration, section 5 is the
procedure, and the ledger entry for `IMPL-72` names it.

**The second half was not done, deliberately.** Writing a reference into
`Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md` would amend a sub-plan,
which a Step 4 implementation session must not do — plan defects are routed as
findings instead. Raised as **`FIND-6.2-01` (P3)**, routed to the next Step 3
audit: `F6.2-05` and its acceptance criterion require an edit that the only
session type able to reach them is forbidden to make. The audit should either
re-route the cross-reference to a planning run or accept this document plus the
ledger as the registration of record.

`VAL-REGISTER` is therefore **partially satisfied** and is recorded as such
rather than claimed.

## 8. Step 0 executed (`IMPL-75`, 2026-09-06) -- the baseline is negative

Step 0 was run on the working device with `ishtar-aon-fix` v1.1 installed, in
`50mp` mode, across one camera open. It was meant to record what "the providers
appear" looks like on a system where they work. **It could not, because on this
device they do not appear.** Evidence:
`snapshots/20260906-1305__Faz6.2__aon-baseline.txt`,
`snapshots/20260906-1309__Faz6.2__aon-mechanism.txt`,
`snapshots/20260906-1312__Faz6.2__aon-inode.txt`,
`snapshots/20260906-1316__Faz6.2__aon-providers.txt`.

### 8.1 Which mechanism is supplying the file -- settled by inode, not by log

`/vendor/lib64/camera/aon_front.pb` is a **regular file, not a symlink**
(`readlink` empty, `readlink -f` returns the path itself), so mechanism B is
absent -- as expected on a ROM built before `IMPL-03` added the entry. What
supplies it is mechanism A, and three independent measurements agree:

| Test | Result |
|---|---|
| `stat -c dev=%d inode=%i` on the vendor path | `dev=65065 inode=128025` |
| the same on `/data/adb/modules/ishtar_aon_fix/.mnt/aon_front.pb` | `dev=65065 inode=128025` -- **the same inode** |
| filesystem under each path | `/vendor/lib64` is `erofs`; `/vendor/lib64/camera` is `f2fs` (`dm-41` = `/data`) |

A read-only `erofs` directory cannot contain an `f2fs` child, so
`/vendor/lib64/camera` is the module's `mount --bind` of its `.mnt` workdir
(`post-fs-data.sh:35`), and the file the camera stack opens is byte-for-byte the
module's copy. SELinux context on it is `u:object_r:vendor_file:s0`, as
`post-fs-data.sh:32-33` sets. Both directories hold the same two entries.

**This is the first time mechanism A has ever been verified** -- `TRACE-13`
recorded it as never tested. It is verified *as a mount*: the file is present,
correct, and correctly labelled at the path the stack reads.

### 8.2 The providers still do not appear

With that mount active, one camera open (`Device 2`, `CameraId[0]`, resumed
activity `org.codeaurora.snapcam/com.android.camera.CameraLauncher`, so a real
preview and not an error dialog) produced:

| Capability | Measured line | Verdict |
|---|---|---|
| aperture | `[ERROR][NCS] camxncsintfmiaperture.cpp:870 RegisterService() [Aperture]No Provider Objects available` | **absent** |
| aperture (downstream) | `[ERROR][SENSOR] camxncsdatasource.h:784 SetupNCSLinkForSensor() Aperture Sensor Handle is NULL` | **absent** |
| face-scene | `[ERROR][SENSOR] camxmultiplefacescene.h:249 GetStableFilteredFaceData() ... Failed to get ncs data` | **absent** |
| face-scene (downstream) | `camxmultiplefacescene.h:330 ... Failed to get face count`; `camxrecoveryscene.h:561 FilteredSceneDetection() Failed to get stable filtered recovery data` | **absent** |
| laser AF / ToF | `I stmvl53l5: kernel version 3.3.0.0 / driver 4.0.1.0 / firmware 3.2.0.0`, `vl53l5-sensor-1.0-hal: stmvl53l5_tof::enable usercount = 1` | **hardware path up** |
| OIS | no NCS line either way; `OIS:true` in the `AGC` line is *static camera characteristics*, not an NCS provider | **not evidenced** |

`camxrecoveryscene.h:393 GetRecoveryData() Error NCS data: pysicalFNumber:
1.900000, targetFNumber: 0.000000` shows the consumer reading a physical
f-number but no target -- the shape of a provider that never registered.
`AONPipeline_1` does appear in `camxresourcemanager.cpp:181 DumpState()`, so the
AON pipeline itself is constructed; the break is downstream of it, in NCS
service registration.

**So `module.prop`'s claim -- "AON -> CSS -> NCS zincirini onarir; diyafram,
OIS, lazer AF (ToF) ve yuz-sahne icin NCS saglayicilari olusur" -- is not
holding on this device.** The file the module supplies is necessary, present and
correct, and the providers are still missing.

### 8.3 What this does not establish

Stated as limits, because the result is negative and a negative invites
over-reading:

- **One configuration.** The device was in `50mp` mode with the patched fullres
  HAL `fe0245a4720fb07b01d96deef47f5569`, not a stock camera stack. The NCS
  failure could belong to that configuration rather than to AON. **The decisive
  follow-up is the same capture in `stock` mode**, which is a device state
  change and needs the user's approval; it has not been taken.
- **One open, one camera, ~12 s.** Providers registering later, or for another
  camera id, would not have been seen.
- **It does not tell us whether the pre-module state was worse.** No
  module-absent capture exists on this device, so "the module improves nothing"
  is *not* shown -- only that it does not reach the end state its description
  claims.

### 8.4 Consequences

- The contingency table's row **"path present, fewer than four providers"** is
  no longer hypothetical. It is the **measured present state of the current
  device**, reached through mechanism A rather than mechanism B. Its prescribed
  response already applies: *module role unchanged, and open an investigation
  rather than assume either mechanism whole.*
- Step 3's pass condition ("path present **and** all four providers") would
  fail on this device today. A Phase 7 build must therefore not be judged
  against "matches the baseline" -- there is no positive baseline to match.
  **Judge it against the strings tabulated in 8.2 instead**, which are exact and
  are what step 0 was for.
- `DEC-04` was answered **keep separate** before this was measured, and the
  answer is unaffected -- if anything reinforced, since merging an artifact
  whose claimed effect is now in doubt into the shipping module would spread the
  doubt. But one of the recommendation's inputs, "an *unconditional* repair
  every affected user needs", is itself now unverified, and section 3 should be
  read with that qualification.
- Raised as **`FIND-6.2-03` (P2)**: the AON module's stated effect is
  contradicted on the one device that can be measured. Routed to Phase 7, and to
  the next Step 3 audit for priority.
- Raised as **`FIND-6.2-02` (P3)**: step 2's log-line discriminator returns
  nothing on a running device; the mount-identity test of 8.1 replaces it.

No module was removed, merged, disabled or edited to obtain any of this. The
preference file was `21762bdcb09f107aad2f397351cf1337` at 12169 bytes before the
camera open and byte-identical after it.
