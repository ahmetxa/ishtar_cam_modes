# Device and ROM Facts for the AOSPA Build

Working notes for the Android 16 / AOSPA `beryl` build. Everything here was
**measured on the device**, not taken from a spec sheet or a forum post, and
each block says how. This file accumulates: later sessions append rather than
rewrite, and mark anything they could not re-measure.

**Scope.** Facts that change a build, a flash or a camera decision. The rental
procedure itself stays in `docs/build-environment.md`; plan state stays in
`Planner-docs/`.

**Secrets rule.** No token, key, password or server address. The md5 values
below are already tracked in the module sources and are detectors, not secrets.

## 1. How this was measured

- Host: Windows, `platform-tools/adb.exe`, device serial `dc27e5d0`, USB.
- Date: **2026-09-20**. Read-only commands only: `getprop`, `uname -a`,
  `md5sum`, `mount`, `df`, `pm` / `dumpsys package`, `find`, `settings get`.
- Root reads went through `su -c` (KernelSU Next). Nothing was written, flashed
  or installed.

## 2. Device identity

| Item | Value | Source |
|---|---|---|
| Device / product | `ishtar` | `ro.product.device`, `ro.product.name` |
| Marketing model | `2304FPN6DC` (Xiaomi 13 Ultra) | `ro.product.model` |
| Board / platform | `kalama` | `ro.product.board`, `ro.board.platform` |
| SoC | QTI **SM8550** | `ro.soc.manufacturer`, `ro.soc.model` |
| ABI | `arm64-v8a`, `zygote64` (64-bit only zygote) | `ro.product.cpu.abilist`, `ro.zygote` |
| Launch API level | **33** (shipped on Android 13) | `ro.product.first_api_level` |
| Hardware | `qcom`, hwlevel `MP`, hwversion `5.9.0` | `ro.hardware`, `ro.boot.hwlevel`, `ro.boot.hwversion` |

`first_api_level=33` is the value Treble/VSR rules are graded against, and it is
what a vendor-API-level check in an Android 16 build will read.

## 3. ROM currently installed

The daily driver is **already AOSPA, not MIUI**. That matters: the Android 15
baseline this project measures its camera work against is an AOSPA build.

| Item | Value |
|---|---|
| AOSPA version | `Vauxite Unofficial` (`ro.aospa.version`), major `vauxite`, variant `unofficial` |
| Android | **15**, SDK **35**, codename `REL` |
| Build id | `AQ3A.250604.001` |
| Display id | `aospa_ishtar-userdebug 15 AQ3A.250604.001 eng.nobody dev-keys` |
| Build date | Thu Aug 14 2025 18:37:30 KST (`ro.build.date`, same for `odm` and `bootimage`) |
| Kernel build date | Tue Aug 12 2025 12:45:05 UTC |
| Security patch | **2025-06-05** (`ro.build.version.security_patch`) |
| Fingerprint (system / odm / bootimage / vendor) | `Xiaomi/aospa_ishtar/ishtar:15/AQ3A.250604.001/eng.nobody:userdebug/release-keys` |
| Fingerprint (`ro.build.fingerprint`) | `Xiaomi/ishtar/ishtar:15/AQ3A.250604.001/eng.nobody:user/dev-keys` |

**Two inconsistencies in the installed build, worth knowing before comparing a
self-built ROM against it:**

1. `ro.build.type` reads `user` with `dev-keys`, while `bootimage`, `vendor`,
   `odm` and `system` all read `userdebug` with `release-keys`. The top-level
   fingerprint also says `Xiaomi/ishtar` where the partitions say
   `Xiaomi/aospa_ishtar`. A build of our own (`./rom-build.sh ishtar -z`,
   default `userdebug`) will not reproduce this mixture.
2. `ro.vendor.build.security_patch` is **empty**, and `ro.vndk.version` is not
   set at all.

## 4. Kernel

```
Linux localhost 5.15.178-android13-8-g7b195d4db1e7 #1 SMP PREEMPT
Tue Aug 12 12:45:05 UTC 2025 aarch64 Toybox
```

- GKI branch **android13-5.15**, sublevel **178**, GKI release **android13-8**,
  hash `g7b195d4db1e7`. `ro.kernel.version` = `5.15`.
- The Android 16 target builds its kernel inline from the pinned
  `kernel_platform/msm-kernel` and `kernel_platform/common` commits, so the
  string above is the **comparison baseline**, not the build input.

**Open input, recorded 2026-09-20 and not yet verified.** The user reports that
the kernel used by both MIUI and AOSPA has been upstreamed by third parties.
If true, this changes kernel scoping (`Faz8.2`, `DEC-08`, whose recorded
recommendation was *defer*) and is the kind of input that triggers replanning.
Nothing in this workspace has verified it yet: no source, branch or commit has
been read. Treat it as a claim until a repository is named and inspected.

## 5. Boot, partitions and verification

| Item | Value | Why it matters |
|---|---|---|
| A/B | `ro.build.ab_update=true`, active slot `_a` | Every boot-chain image is an A/B partition; `recovery` is not a standalone partition |
| Virtual A/B | `ro.virtual_ab.enabled=true` | Snapshot-based OTA; affects flashing and rollback |
| Dynamic partitions | `ro.boot.dynamic_partitions=true` | `system` / `vendor` / `odm` / `product` live in `super` |
| AVB | version **1.3** | `vbmeta` and `vbmeta_system` must be handled on flash |
| Treble | `ro.treble.enabled=true` | Vendor interface split |
| Encryption | `ro.crypto.type=file` (FBE), `state=encrypted` | A `/data` format erases the AGC configuration and module state |
| APEX | `ro.apex.updatable=true` | |
| SELinux | **Enforcing** | |

Sizes, `df -h` (read-only partitions are 100% full by construction):

| Mount | Size | Used | Free |
|---|---|---|---|
| `/odm` | 1.5 G | 1.5 G | 0 |
| `/vendor` | 777 M | 777 M | 0 |
| `system` | 662 M | 662 M | 0 |
| `/data` (f2fs, dm-41) | 462 G | 58 G | **405 G** |

**Do not trust the verified-boot props.** `ro.boot.vbmeta.device_state` reads
`locked` and `ro.boot.verifiedbootstate` reads `green` on a device that is
running KernelSU with an unlocked bootloader. One of the installed root modules
is almost certainly resetprop-ing them for attestation. Read the real state with
`fastboot getvar unlock` when it matters, never from these props.

## 6. Root stack (what has to be re-established after a flash)

| Item | Value |
|---|---|
| Root | **KernelSU Next**, `ksud 3.3.0 (uapi: 2)` |
| Manager app | `com.rifsxd.ksunext` |
| Zygisk | `zygisksu` |
| Mount backend | `magic_mount_rs` v4.0.8-900 (metamodule, own `webroot/`) |

Installed modules, `ls /data/adb/modules` (10):

| Module | Version | Note for an Android 16 build |
|---|---|---|
| `ishtar_cam_modes` | v2.2 (code 13) | This project. Needs the HAL patch table re-derived against the new vendor binary, and the sensor blob md5 re-checked. |
| `ishtar_aon_fix` | v1.1 (code 2) | This project. **Becomes unnecessary if the ROM carries the symlink entry** — its own script exits when `/vendor/lib64/camera/aon_front.pb` already exists, which is exactly what the `Faz6.1` device-tree edit adds. |
| `custom_camera` | 6.4 "Custom Camera Fix" (author Termux) | Third-party. Replaces `/system/product/priv-app/MiuiCamera/MiuiCamera.apk`. A MIUI camera port on an AOSPA base: highest compatibility risk on a new Android version, and unrelated to our bind mounts. |
| `magic_mount_rs`, `zygisksu` | see above | Root infrastructure. |
| `PixelifyPhotos`, `box_for_root`, `xcharge`, `youtube-morphe-exp-jhc-arm64`, `youtube-music-morphe-exp-jhc-arm64` | — | Unrelated to camera; listed so the post-flash reinstall set is complete. |

## 7. Camera layer as measured

Paths (odm is its own partition, `TARGET_COPY_OUT_ODM := odm`):

- Sensor driver: `/odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin`
- Camera HAL: `/odm/lib64/hw/camera.qcom.so`
- AON config the fix supplies: `/vendor/lib64/camera/aon_front.pb` (source `/odm/lib64/camera/aon_front.pb`)

Guard values, all confirmed on the device on 2026-09-20:

| File | md5 | Meaning |
|---|---|---|
| Sensor blob (live) | `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` | Stock, matches `customize.sh` `EXPECT_MD5` |
| `camera.qcom.so` (live) | `fe0245a4720fb07b01d96deef47f5569` | The module's **patched** copy, bind-mounted |
| `camera.qcom.so` (stock) | `c3fa63a86ee3ecaf9fbf02005d35f6b5` | `HAL_STOCK_MD5`, size 27,268,688 |

Current module state: mode `50mp`, language `en`. Both the sensor blob path and
the HAL path are single-file **bind mounts** from `dm-41` (`/data`), which is why
`mount` shows an f2fs device on a file under `/odm`.

Camera services, for restart and verification steps:
`init.svc.cameraserver`, `init.svc.vendor.camera-provider`,
`init.svc.vendor.camera-provider-2-7-ext` — all `running`.

Vendor camera properties worth carrying over:

- `persist.vendor.camera.maxRAWSizes` = **19**
- `persist.vendor.camera.IsVariableApertureSupported` = 1, `manualApertureFnumber` = 1.9
- `persist.vendor.camera.mi.module.info` = `back_main=0x65;back_tele=0x70;back_tele4x=0x70;`
- `persist.vendor.camera.mi.module.infoext` = `front_main=0x67;back_ultra=0x70;`
- `persist.vendor.camera.mi.dualcal.state` = 3
- `camera.disable_zsl_mode` = true

**Patch-table portability.** Every offset in `blobs/hal-fullres.patch` is bound
to the one vendor build of `camera.qcom.so` whose md5 is `c3fa63a8…`. An Android
16 build ships a different binary, so the table does not carry over, and the md5
guard is the detector, not the version control (`R8`, Ontology invariant 10).
That re-derivation is `Faz8.1`'s question, not something to improvise on the
rented server.

## 8. What lives only on the phone

Measured by comparing `find /data/adb/modules/...` against the release zips and
the repository. Nothing project-authored is phone-only; the device-only paths are
all regenerated at install or at boot:

| Device path | What it is | Regenerated by |
|---|---|---|
| `ishtar_cam_modes/active_hal/camera.qcom.so` | 27 MB patched HAL. Deliberately not packaged. | `halpatch.sh`, from the ROM's stock binary plus the tracked 16-point patch table |
| `ishtar_cam_modes/active/…imx989_wide.bin` | Selected sensor variant | Copied from `blobs/` on a mode change |
| `ishtar_aon_fix/.mnt/aon_front.pb`, `.mnt/libPlatformValidatorShared.so` | Boot-time bind-mount work directory | `post-fs-data.sh` on each boot, from `/odm` and the existing `/vendor/lib64/camera/` |
| `mode`, `lang` | Runtime state (`50mp`, `en`) | Written by `setmode.sh` or the WebUI |

The authoritative source of the **stock** sensor blob and the stock HAL is the
ROM itself (`/odm`), not this repository. Both are vendor binaries and are
excluded from git by design (`UNTRACKED-BY-DESIGN.md` sections 3 and 4).

**The one single-copy artifact is not on the phone.**
`ishtar-cam-modes/tile-app/debug.keystore` exists only on this Windows host and
is correctly untracked, because it is a credential. It is the signing key of the
installed tile app: build with a different key and the APK will not install over
the existing one (signature mismatch). `tile-app/build.sh` documents this and
now accepts `KS`, `KS_PASS` and `KS_ALIAS` from the environment.

## 9. Quick-Settings tile chain, verified 2026-09-20

Recorded here because it is the module's only UI entry point and it depends on
one app that is **not** part of the module.

1. Long-pressing any of the four tiles sends `QS_TILE_PREFERENCES`, which
   `com.ishtar.cammodes/.WebUiActivity` handles (declared in the module's own
   `tile-app/AndroidManifest.xml`).
2. `WebUiActivity` has no UI. It runs, as root,
   `am start -n com.rifsxd.ksunext/.ui.webui.WebUIActivity --es id ishtar_cam_modes`
   and finishes.
3. The page that appears is the module's own `webroot/index.html`, rendered by
   the **KernelSU Next manager app**.

So the chain needs three things present at once: the module's APK, the module's
`webroot/`, and the KernelSU Next manager. It also needs root granted to
`com.ishtar.cammodes`; without it the `su` call returns empty and the long-press
silently does nothing.

All four tiles are registered in `settings get secure sysui_qs_tiles` as
`custom(com.ishtar.cammodes/.FullResTile)`, `.DcgTile`, `.Ln4Tile`, `.Ln2Tile`.
The `.Launcher` activity-alias is currently in `enabledComponents`, so the app
icon does appear in the drawer, which matches `customize.sh`'s v2.2 text.

## 10. Notes added 2026-11-13

- **The phone no longer runs the ROM described above.** On 2026-11-13 it ran
  HyperOS 4 (`OS4.0.0.44.WMACNXM`, Android 17, SDK 37, kernel
  `5.15.215-KylinKernel`, KernelSU `4.3.0-r1`), installed by the user from a
  third-party developer's build, and the plan to build an AOSPA ROM had been
  abandoned. Sections 1–9 describe the AOSPA Android 15 install as measured on
  2026-09-20 and stay as that record. The HyperOS 4 measurements are in
  `snapshots/20261113-1819__IMPL96__hyperos4-readonly-probe.txt` and
  `snapshots/20261113-1821__IMPL96__hyperos4-smoke-baseline.txt`.
- **Correction to section 7, "Patch-table portability".** The sentence "An
  Android 16 build ships a different binary, so the table does not carry over"
  was not measured, and it contradicted `IMPL-92` (2026-09-11): at the pinned
  Android 16 vendor commit `f92e7a9`, `camera.qcom.so` had md5 `HAL_STOCK_MD5`
  `c3fa63a86ee3ecaf9fbf02005d35f6b5` and size `HAL_SIZE`. The Android 16 build
  was abandoned, so the point is moot. On HyperOS 4 the table does not apply:
  that `camera.qcom.so` is a different binary (md5
  `2a955e68ad043380675529edb64a40f7`, 27,305,440 bytes).
- **Section 4's open input is closed.** The user dropped it on 2026-11-13: the
  phone already runs a HyperOS 4 build with kernel 5.15.215.
- **Section 9's tile chain** hands the WebUI to the KernelSU Next manager
  (`com.rifsxd.ksunext`). On the HyperOS 4 install the root is KernelSU
  `4.3.0-r1`, and `pm list packages` listed neither `com.rifsxd.ksunext` nor
  `me.weishu.kernelsu`, so the chain has to be re-checked before any reinstall.
