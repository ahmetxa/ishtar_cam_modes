# Recovery Runbook — `ishtar-cam-modes`

**Scope.** What to do when the module itself is what broke. Every step here works
without `setmode.sh`, `action.sh`, the QuickSettings tiles, or the WebUI, because
those are the things that may have failed.

**Status.** Written 2026-09-01 as a pull-forward of `Faz9.2` work items F9.2-05,
F9.2-06 and F9.2-07, ahead of `Faz3.3`'s first live HAL patch. The Step 3 audit
named this its most important remediation action: the master plan's risk `R3`
asks for a recovery path, and Phases 3–5 patch a system binary. The remaining
`Faz9.2` items — the capability checklist, the known-good/known-bad detection
demonstration, and the per-release evidence record — stay in Phase 9, because
they depend on `Faz9.1`'s build script and on `Faz9.3`'s corrected claims.

---

## 1. The one fact that makes recovery cheap

**The module never writes to `/odm`.** This was verified mechanically, not
assumed: every write in every module script targets `$MODDIR/active/…` or
`$MODDIR/active_hal/…`, both module-private. `/odm` paths appear only as
`mount --bind` targets, as `md5sum` read sources, as the `cat` source that seeds
the HAL copy, and in `/proc/1/mountinfo` checks.

Two consequences follow, and they are the runbook's backbone:

1. **A bind mount does not survive a reboot.** The on-disk `/odm` partition is
   untouched and byte-identical to stock at all times.
2. **Therefore disabling the module and rebooting is a complete restore, for
   every failure this module can cause.** No reflash. No `fastboot`. No data loss.

This is Project-Ontology invariant 1 — "every modification is a bind-mount or an
md5-guarded offset patch" — holding mechanically rather than by intention. It
resolves `CQ-09`: **the module cannot brick the camera across a reboot**, and the
recovery is one file and a restart.

The rest of this document exists for the cases where you want the camera back
*without* rebooting, want to know *which* layer broke, or find that a reboot did
not fix it — which would mean the cause is not this module.

---

## 2. First move, for every scenario

```sh
adb shell su -c 'touch /data/adb/modules/ishtar_cam_modes/disable'
adb reboot
```

The `disable` file makes the root manager skip the module at boot, so
`post-fs-data.sh` never runs and no bind mount is created. The device comes back
stock. `remove` instead of `disable` deletes the module on the next boot; prefer
`disable`, because it is reversible by deleting the file and keeps `active_hal/`
so the next enable does not re-copy 27 MB.

If `adb` is unavailable, the KernelSU or Magisk manager app can toggle the module
from the device. Both are independent of this module.

**Verify the restore** — these read nothing the module provides:

```sh
adb shell su -c 'grep -c " /odm/lib64/hw/camera.qcom.so " /proc/1/mountinfo'
adb shell su -c 'grep -c " /odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin " /proc/1/mountinfo'
adb shell su -c 'md5sum /odm/lib64/hw/camera.qcom.so'
adb shell su -c 'md5sum /odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin'
```

Expected after a clean disable: both counts `0`, HAL md5
`c3fa63a86ee3ecaf9fbf02005d35f6b5`, sensor md5
`9e4d0fe1a8bf2eb4146c9917a0ac2c4c`.

---

## 3. What the guards already prevent

Listed so the scenarios below cover what actually remains rather than restating
what cannot happen. Every entry was read from the source in this run.

| # | Failure | Guard | Behavior |
|---|---|---|---|
| G1 | OTA changed the sensor driver, so patch offsets would land on wrong records | `post-fs-data.sh:44-52` md5 vs `9e4d0fe1…` | Logs `DURDU`, mounts nothing, `exit 0`. Stock behavior preserved. |
| G2 | OTA changed the HAL | `post-fs-data.sh:102-108` md5 vs `c3fa63a8…` | Aborts the HAL layer only; the sensor layer still works. |
| G3 | `mode` file corrupted or absent | `post-fs-data.sh:23-26` `*)` branch | Maps any unrecognised value to `stock`. Self-heals at boot. |
| G4 | Sensor blob truncated | `post-fs-data.sh:60-63` size vs `1062250` | Aborts before copying. |
| G5 | Partial or botched HAL patch write | `hal_state` md5-classifies the copy → `unknown`; `hal_set:96-99` re-seeds | Re-copies the device's stock binary, then re-verifies. |
| G6 | Seeding from an already-patched file | `hal_seed:107` refuses while mounted, and requires `$HAL_TGT` to match stock md5 | Cannot poison its own baseline. |
| G7 | A write that silently did not apply | `hal_set:102` re-checks md5 after `hal_write` | A failed write cannot be reported as success. |
| G8 | Install onto the wrong device or a changed driver | `customize.sh` aborts on sensor md5 mismatch; warns on HAL mismatch | Degrades to sensor-only rather than installing a broken HAL layer. |

Note the shape: **every guard fails closed and `exit 0`s rather than aborting
boot.** A guard tripping costs you the feature, not the phone.

---

## 4. Residual failure modes — what the guards do *not* catch

These are what the scenarios below are for.

- **R1 — Stacked bind mounts.** One `umount` removes only the topmost mount and
  reports success while the file underneath stays patched. This is measured, not
  theoretical: it is why `hal_umount_all` (`halpatch.sh:44-52`) loops up to 40
  times. **The loop is module code.** If the module is what broke, nobody runs
  it, and a single manual `umount` gives a false "restored to stock" reading.
  Always check the mount *count*, never just that one `umount` succeeded.
- **R2 — A byte-valid but semantically wrong patch.** `hal_state` and `hal_set`
  verify *identity* (md5), not *correctness*. A `hal-fullres.patch` that produces
  a binary matching `HAL_FULLRES_MD5` passes every guard even if those 16 words
  are wrong. This is exactly `QAS-01`'s scenario and it is the single failure
  mode most relevant to `Faz3.3`, which changes patch content.
- **R3 — Silently failed ownership, permissions, or SELinux context.** All three
  of `chown`, `chmod` and `chcon` are `2>/dev/null` silenced in all three places
  they appear — `post-fs-data.sh:68-70`, `halpatch.sh:112-114`,
  `setmode.sh:253-255`. If `chcon u:object_r:vendor_file:s0` fails, the bind
  mount still succeeds and the guards still pass, but `cameraserver` cannot load
  the library. **This presents as "camera will not open" with every checksum
  correct**, which is the most confusing signature in this document. Recorded as
  `FIND-9.2-01` (P3, latent — no occurrence observed).
- **R4 — The module is not the cause.** `FIND-2.3-03` measured AGC's video path
  black in four states *including plain `stock`*. If a reboot with the module
  disabled does not fix your symptom, the module is not what broke.

---

## 5. Scenario A — the camera will not open

**Signature.** Camera apps fail to start, show a black preview, or the framework
reports `CONFIG failed`.

1. Disable and reboot (section 2). If the camera returns, the module was
   involved; continue at step 3 to find out which layer.
2. **If the camera does not return, stop — this is not a module failure** (R4).
   Do not reflash on this evidence. Check whether the symptom also occurs in a
   state that predates the module.
3. Re-enable, then read the layer state without module commands:
   ```sh
   adb shell su -c 'logcat -b all -d | grep -i ishtar_cam_modes | tail -40'
   ```
   Every guard logs a `DURDU:` line naming exactly what it refused and why. This
   is the fastest diagnosis available and it costs nothing.
4. If all checksums are correct and the mounts are as expected, suspect **R3**:
   ```sh
   adb shell su -c 'ls -Z /data/adb/modules/ishtar_cam_modes/active_hal/camera.qcom.so'
   ```
   Expect `u:object_r:vendor_file:s0`. A different context is the cause; the fix
   is to re-apply it, and the durable fix belongs in `Faz9.1`.

## 6. Scenario B — a corrupted or wrong-state HAL copy

**Signature.** `hal_state` would say `unknown`, or 50 MP behaves inconsistently.

The module self-heals this at boot (G5), so reaching for the runbook means the
self-heal did not run or did not work.

1. Disable and reboot. The device is stock immediately — the corrupt file is a
   module-private copy that is no longer mounted anywhere.
2. Delete the copy so the next boot re-seeds it from the device's own stock
   binary:
   ```sh
   adb shell su -c 'rm -f /data/adb/modules/ishtar_cam_modes/active_hal/camera.qcom.so'
   ```
3. Re-enable and reboot. `post-fs-data.sh:112-118` sees state `none` and calls
   `hal_seed`, which re-copies from `/odm` and verifies. The first boot after this
   is slower by one 27 MB copy.
4. Confirm: HAL md5 at `/odm/lib64/hw/camera.qcom.so` is `c3fa63a8…` when the
   mount is absent, or `fe0245a4…` when `50mp` is active and mounted.

**Never** hand-restore by copying a HAL binary from the workspace onto the
device. The 27 MB binary is deliberately not shipped, and the device's own `/odm`
copy is the only authoritative source.

## 7. Scenario C — a stuck or stacked mount

**Signature.** The mount count is greater than 1, or a state change did not take
effect, or `/odm` still shows a patched checksum after an `umount`.

1. Read the count first — this is R1, and the count is the only trustworthy
   reading:
   ```sh
   adb shell su -c 'grep -c " /odm/lib64/hw/camera.qcom.so " /proc/1/mountinfo'
   ```
2. **Preferred: reboot.** Bind mounts do not persist. A reboot clears any depth
   of stacking with no risk, and with the module disabled the device comes back
   stock.
3. If you must clear it live, loop rather than issuing one `umount`, and stop on
   the count, not on the exit status:
   ```sh
   adb shell su -c 'n=0; while grep -q " /odm/lib64/hw/camera.qcom.so " /proc/1/mountinfo && [ $n -lt 40 ]; do umount /odm/lib64/hw/camera.qcom.so 2>/dev/null || break; n=$((n+1)); done; grep -c " /odm/lib64/hw/camera.qcom.so " /proc/1/mountinfo'
   ```
   The trailing count must print `0`. This mirrors `hal_umount_all` deliberately
   — it is the same algorithm written out so it does not depend on the module.
4. Unmounting a HAL while camera services are running can crash them. Stop the
   camera clients first, or simply prefer step 2.

## 8. Scenario D — the module fails at boot

**Signature.** The device boots but the camera is broken every time, or you
suspect the module is implicated in a boot problem.

1. Every guard in this module ends in `exit 0`, never a boot abort, so the module
   is an unlikely cause of a boot *loop*. Check that assumption before acting on
   it.
2. If the device boots at all, use section 2 — that is the whole recovery.
3. If the device does not reach `adb`, use the root manager's own module-disable
   path from recovery, or its boot-time safe mode. Both are functions of
   KernelSU/Magisk, not of this module; consult that manager's documentation for
   the current gesture rather than trusting a value written here.
4. Reflashing the ROM is the last resort and should never be needed for a
   module-caused failure, because `/odm` was never written. If a reflash appears
   necessary, first re-read section 1 — the conclusion probably rests on a false
   "restored to stock" reading from R1.

---

## 9. Independence verdict (F9.2-07)

Every step above was reviewed against the constraint that the runbook must work
when the module is what broke.

| Step | Depends on | Module-independent? |
|---|---|---|
| §2 disable + reboot | root manager, `adb` | Yes |
| §2 verification reads | `grep`, `md5sum`, `/proc/1/mountinfo` | Yes |
| §5 log read | `logcat` | Yes — reads the module's output, does not execute it |
| §6 delete `active_hal` copy | `rm` | Yes |
| §6 re-seed | `post-fs-data.sh` at boot | **Runs module code by design** — this is the repair path, taken only after §2 has already restored the device |
| §7 unmount loop | `umount`, `grep` | Yes — `hal_umount_all`'s algorithm written out rather than called |
| §8 recovery-mode disable | root manager | Yes |

No step invokes `setmode.sh`, `action.sh`, a tile, or the WebUI. The one entry
that runs module code is §6's re-seed, and it is a *repair* performed from an
already-recovered state, not a recovery step.

---

## 10. What this closes and what it does not

**Closes.** `CQ-09` — the module cannot brick the camera across a reboot, and the
recovery is `disable` plus a restart. `ARC-11` moves from `absent` to
`documented`. Master-plan risk `R3` has a written mitigation ahead of the first
live HAL patch, which was the audit's stated precondition for `Faz3.3`.

**Does not close.** `ARC-11` is `documented`, not `demonstrated` — no step here
has been executed against a deliberately broken state on the device. That
demonstration is `Faz9.2`'s F9.2-04 known-good/known-bad test and stays in
Phase 9. The capability checklist and the per-release evidence record likewise
remain Phase 9 work. Treat this document as a verified reading of the source
rather than as a rehearsed procedure until F9.2-04 runs.
