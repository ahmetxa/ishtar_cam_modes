# Project Ontology

> Durable project vocabulary and invariants for `ishtar`. Written by ClaudeQB Step 1.5.
> Purpose-built to survive context loss between sessions. Body language: English (default contract).

## 1. Purpose

This project modifies the camera stack of a Xiaomi 13 Ultra (`ishtar`) running AOSPA Android 15, to expose sensor capabilities the stock build does not advertise. The work is reverse engineering against closed vendor binaries, so its most valuable output is **knowledge**: exact addresses, exact tag identifiers, exact invariants, and exactly which hypotheses were tested and rejected.

That knowledge is expensive to reproduce — several findings here cost multi-hour disassembly sessions, and at least two were rediscovered after context loss. This file is the lookup surface. `50MP-Entegrasyon-Plani.md` remains the narrative history; this file is what a future session should read *first*.

Every value below was measured from a device or a binary, not inferred. Where something is unknown, it says so.

## 2. Domain Vocabulary

| Term | Meaning |
|---|---|
| `ishtar` | Xiaomi 13 Ultra, SM8550 (Snapdragon 8 Gen 2), released April 2023. Also the workspace name. |
| `beryl` | A second Xiaomi device targeted for a future port. No device-specific files exist yet. |
| IMX989 | Sony 1-inch main sensor. Physical pixel array 8192x6144 (50.3 MP). |
| QCFA | Quad Colour Filter Array. The sensor's native 2x2 binning arrangement; full resolution requires remosaic. |
| DCG | Dual Conversion Gain. A sensor readout mode; variants `dcgA` and `dcgB`, with `dcgB` measured better on device. |
| LN2 / LN4 | Low-noise binning modes, 2x and 4x. Variants carry `s` (slow) and `f` (fast) suffixes. |
| `stock` | Both a mode name (no modification) and the restore target. Two meanings — keep them distinct in prose. |
| `50mp` | A **mode name**. Enables the HAL layer and forces the sensor layer to stock. |
| `fullres` | The **HAL state** produced by the 16-point patch. Not a mode name. Distinct from `50mp`. |
| Mode | The single runtime state value; one of ten. Stored in `$MODDIR/mode`. |
| Patch table | A plain-text list of `<offset> <stock-escape> <patched-escape>` triples, guarded by md5 comments for both stock input and patched result. |
| Sensor layer | The IMX989 driver `.bin`, bind-mounted over `/odm/lib64/camera/`. Owns DCG/LN/bit-depth. |
| HAL layer | `/odm/lib64/hw/camera.qcom.so`, byte-patched in place. Owns advertised stream configurations. |
| Application layer | The AGC GCam port, patched at smali level. Owns which advertised configuration is selected. |
| AGC | The Google Camera port in use. Version 8.4.300 V9.6 is mandated by the config author. |
| AON | Always-On Sensing. The chain AON → CSS → NCS supplies aperture, OIS, laser AF, and face-scene providers. |
| Tile | A QuickSettings tile. Four exist; they are mutually exclusive. |
| Kitsune | A third-party module layout convention used by the upstream reference modules. |

## 3. Core Entities and Concepts

**Mode** — the central entity. Ten values: `stock`, `dcgA`, `dcgB`, `ln2`, `ln4`, `ln2s`, `ln4s`, `ln2f`, `ln4f`, `50mp`. Single-writer state in one file; read by `setmode.sh`, `action.sh`, the four tiles, and the WebUI. Lifecycle: *selected* → *camera stack stopped* → *layer applied* → *camera stack restarted* → *ready*. The transition is not complete until the camera is genuinely ready (a v1.7 correction).

**Patch table** — a self-verifying description of a binary modification. Two exist:

| File | Entries | Target | Effect |
|---|---|---|---|
| `ishtar-cam-modes/blobs/hal-fullres.patch` | 16 | `camera.qcom.so` | `LDR Wn,[Xm,#0x3d84]` → `MOV Wn,#0`; unlocks 8192x6144 in the standard scaler table |
| `agc-50mp-yama/hal-raw50-deneme.patch` | 4 | `camera.qcom.so` (fullres) | `cmp wN,#2` → `cmp wN,#5`; admits RAW10/RAW12/RAW_OPAQUE at full resolution |

The 27 MB HAL binary is never shipped. The device's own stock blob is patched in place, which is why the md5 guard is load-bearing rather than decorative.

**Sensor blob** — `com.qti.sensormodule.ishtar_semco_imx989_wide.bin`, exactly 1,062,250 bytes. QTI Chromatix format with a `regSetting`/register map and a 23-entry mode table. Ten variants are pre-generated under `blobs/`.

**Stream configuration** — the framework-visible list of `{format, width, height, direction}` tuples. Emitted by `InitializeScalerStaticCaps`.

**Which camera is "camera 3" is an open question as of 2026-08-30 (`OQ-17`).** The Faz 2.1 smoke run measured every HAL camera device on the phone, and the shorthand this project has used does not survive contact with the dump. `dumpsys media.camera` maps framework device 3 to HAL id 9, and HAL id 9 is **Front**-facing with a 3264x2448 pixel array — it cannot be the IMX989. The rear IMX989 array (4096x3072 binned, 8192x6144 physical) sits on HAL id 0 and on ids 2 through 7 and 10. Measured on a stock HAL in mode `dcgB`:

| HAL id | Facing | availableStreamConfigurations | pixelArraySize |
|---|---|---|---|
| 0 | Back | 440 | 4096x3072 |
| 1 | Front | 372 | 3264x2448 |
| 2,3,4,5,6,7 | Back | 500 each | 4096x3072 |
| 8, 9 | Front | 432 each | 3264x2448 |
| 10 | Back | 500 | 4096x3072 |
| 11, 12 | Front | 120 each | 12000x9000 |

None of these is the 508 recorded by `EV-16`, which was measured under a `fullres` HAL, so the comparison is not like-for-like. Until this resolves, `scripts/smoke.sh` reports **all thirteen** devices rather than committing to one, and prints full stream rows for the lowest Back-facing id (HAL 0) under an explicitly stated rule. Faz 3.2 and Faz 4.1 should settle it by measurement rather than inherit the shorthand.

## 4. Module and Boundary Map

| Path | Owns | Depends on |
|---|---|---|
| `ishtar-cam-modes/` | Mode switching, UI, install, boot reapplication | KernelSU, camera framework, both vendor blobs |
| `ishtar-cam-modes/blobs/` | Ten sensor variants + the HAL patch table | — |
| `ishtar-cam-modes/tools/` | Blob generation and verification (Python, host-side) | — |
| `ishtar-cam-modes/tile-app/` | Four QuickSettings tiles + launcher entry (Java) | `action.sh` via the `mode` file |
| `ishtar-cam-modes/webroot/` | KernelSU WebUI, bilingual EN/TR | `action.sh` |
| `ishtar-aon-fix/` | Creates `/vendor/lib64/camera/aon_front.pb` | **Not** KernelSU module mounting — deliberate |
| `agc-50mp-yama/` | AGC smali patches; the experimental HAL table | The AGC APK |
| `device_ishtar/`, `common_sm8550/`, `refs/*` | AOSPA/LOS build inputs | — |
| `android_kernel_*`, `common_sm8550` | Kernel source, read-only on this host | — |

**Layer exclusion rule.** `50mp` and the DCG/LN modes are mutually exclusive by decision `Kararlar #1`. Cause: sensor mode 0 (50 MP) is 10-bit, while DCG pulls the global white level to 12-bit; combined, 50 MP output was corrupted. `Kararlar #4` approves attempting to remove this exclusion by moving mode 0 to 12-bit, after everything else is stable.

## 5. Workflows and Lifecycles

**Mode switch.** Requested (tile, WebUI, action button, or `setmode.sh`) → `restart_camera()` → apply layer → verify md5 → write `mode` → notify. The user sees a per-second countdown; completion is signalled only when the camera is genuinely ready.

**Camera stack restart — ordering is an invariant, not a preference.** The correct order runs from client toward HAL:

1. `stop cameraserver`, wait for stopped — the framework closes all sessions itself.
2. `stop vendor.camera-provider` and `vendor.camera-provider-2-7-ext`, wait.
3. Force-stop camera applications, now that no session is open.
4. `start cameraserver`.

Reversing this — killing the provider while a stream is live — leaves the QCOM kernel driver holding CSIPHY/CSID allocations, producing a black preview in **every** mode including stock, recoverable only by reboot. This was a real defect, fixed in v1.6.

**Boot reapplication.** `post-fs-data.sh` reapplies the stored mode; `service.sh` handles late-boot work such as launcher visibility.

**AGC resign and reinstall.** Changing the APK signature requires uninstall. Data is preserved by: `tar` the app data → uninstall → install → untar → `chown -R <new uid>` → `chcon -R "$(stat -c '%C' <parent>)"` → `pm grant` the runtime permissions. Plain `restorecon -R` is **wrong**: it discards the per-app SELinux categories and the app then fails. Reusing the same signer allows later `install -r` without uninstalling.

## 6. Integrations and External Systems

- **KernelSU** — privilege and mounting. `ishtar-aon-fix` deliberately does not depend on module mounting.
- **Android camera framework** — `cameraserver`, `vendor.camera-provider`, `vendor.camera-provider-2-7-ext`. Restarted, never replaced.
- **Vendor blobs** — `/odm/lib64/hw/camera.qcom.so` (27,268,688 bytes) and `/odm/lib64/camera/<sensor>.bin` (1,062,250 bytes). Both guarded by exact size and md5.
- **`adb`** — the only host↔device channel. Vendored under `platform-tools/`.
- **No network integrations of any kind.** No API, no telemetry, no cloud dependency.

### Reverse-engineering address book

Recorded here deliberately: these values are expensive to re-derive and have been lost to context truncation before.

**`camera.qcom.so`, function `InitializeScalerStaticCaps`** — `0x16bf4c0` … `0x16c5a90` (26 KB, 6,516 instructions).

- Emits 16-byte entries `{format, width, height, direction}` into the array at `[x?+0xb10]`.
- Format gate: `sub wN, wFmt, #0x22` ; `cmp wN, #2` ; `b.lo` — admits 0x22 (34) and 0x23 (35). Separate tests admit `#0x36` (54) and `#0x21` (33).
- The four `cmp wN,#2` sites: `0x16c18dc`, `0x16c1c18`, `0x16c22bc`, `0x16c2330`. (Note: `0x16c2334` is the following `b.lo`, not the `cmp` — an earlier transcription error worth not repeating.)
- Changing those four to `cmp wN,#5` admits 0x22–0x26, which adds RAW10 (37), RAW12 (38), and RAW_OPAQUE (36) at 8192x6144. Array grows 508 → 868 int32.
- All 16 `hal-fullres.patch` sites are inside this function; the binary has 55 accesses to `+0x3d84` in total.

**`android.sensor.info.pixelArraySize`, tag `f0006`** — the current Phase C target. Nine movz/movk references at `0x004fe984`, `0x004fee94`, `0x004ffa5c`, `0x00d9ae24`, `0x00d9ae80`, `0x013b192c`, `0x013b1994`, `0x013b1a08`, `0x013b1a7c`. Six rodata dwords at `0x0002c6ac`, `0x0038964c`, `0x003969b4`, `0x00396adc`, `0x00397fcc`, `0x0039c1f0`. **The write site has not been located.**

**Related metadata tags** — `android.scaler.availableStreamConfigurations` `d000a`; `availableMinFrameDurations` `d000b`; `availableStallDurations` `d000c`; `android.sensor.info.activeArraySize` `f0000`; `preCorrectionActiveArraySize` `f000a`.

**Vendor tables** — `org.codeaurora.qcamera3.quadra_cfa.availableStreamConfigurations` carries only 33/34/35 at 8192x6144. `xiaomi.scaler.availableStreamConfigurations` already carries `[37 8192 6144 0]`, `[32 8192 6144 0]`, `[36 8192 6144 0]` — the values exist in a vendor table but not in the standard one, which is the whole reason the HAL patch is needed.

**AGC port obfuscation map** (identical in V9.6 and V14) — `Lhvg;` ResolutionSetting; `Llvo;` the hooked characteristics wrapper (the only class overriding `x(I)`); `Llwe;` delegating base; `Lghx;` extends `Llwe;`; `Lmip;->bs()` max of list; `Lmip;->bu()` `Size[]`→`List<Llig;>`; `Lmip;->eU()` blocklist filter; `Lddl;->P/Q` the `blacklisted_resolutions_back/front` lists (**both empty** — a rejected hypothesis); `Llig;->a` width, `->b` height; `Llwp;->a` format, `->b` `Llig;`.

**`LAGC;->Forty8Strip(I)I` is `return p0`** — an identity stub in both builds. The port's 48M mechanism does not exist in this build; the UI's "Redmi K20 Pro / Mi9" note confirms it. A rejected hypothesis, recorded so it is not tested a third time.

**Channel selection** — there is no separate 12 MP / 50 MP channel. `LensSettings.getImageFormatArr()` returns `[pref_raw_key_<lens>]` if set, otherwise `[0x25 RAW10, 0x26 RAW12, 0x20 RAW_SENSOR, 0x23 YUV]`. `AGC.getImageReaderFormat()` takes the first format with a non-empty size list, then `Lmip;->bs()` takes its **maximum** size. AGC therefore already prefers the largest available size; it was stuck at 12.6 MP purely because RAW10's maximum was 4096x3072. Preview uses `Lgsf;->a()`, nearest-to-target, so widening the list does not disturb preview.

**Toolchain** — Temurin JDK 21; smali/baksmali **2.5.2** from the legacy `org/smali` Maven group (`org.jf.*` package names) plus dexlib2, util, guava 31.1-jre, failureaccess, antlr-runtime 3.5.2, jcommander 1.82, ST4; uber-apk-signer 1.3.0; embeddable Python 3.12.7 with capstone 5.0.7 and pyelftools.

**Toolchain negative findings** (each cost real time): apktool's bundled smali `Main` classes are stripped stubs and cannot be invoked; `com.android.tools.smali` Maven paths return 404; the Bitbucket mirror returns 403; google/smali publishes no release binaries; **radare2 and rabin2 5.9.8 do not complete on this 27 MB binary** (no output in 300 s, from either shell).

## 7. Invariants and Constraints

1. **Reversibility.** Every modification is a bind-mount or an md5-guarded offset patch. A module that cannot be disabled is a bricked phone.
2. **Fail closed.** Size check, then md5 check, then write. Never write on a mismatch.
3. **Restart ordering.** Client before HAL. Violating this leaks CSIPHY/CSID allocations and blackens preview in every mode. (Section 5.)
4. **Layer exclusion.** `50mp` and DCG/LN are mutually exclusive until `Kararlar #4` is executed and proven.
5. **Video integrity.** 1080p60 and 4K60 must remain functional in every mode. A standing acceptance criterion, user-validated.
6. **Gcam static-metadata consistency.** `libgcam static_metadata.cc:667` requires `frame_raw_max` to equal the active array size **or** the pixel array size. Violation → `gcam.cc:274 Create … failed` → `NullPointerException: Gcam.f()`. **This single invariant explains two failures from opposite directions:** the Faz 4 wide patch raised the active array without raising raw; the Faz 12 RAW patch raised raw without raising the array. Both sides must move together.
7. **Android high-resolution bucket.** `getOutputSizes(fmt)` excludes any size whose minimum frame duration exceeds 1/20 s; those appear only via `getHighResolutionOutputSizes(fmt)`. On camera 3: 8192x6144 = 66,666,666 ns (15 fps) → excluded; 4096x3072 = 33,333,333 ns (30 fps) → kept. This was the original root cause of AGC's 12.6 MP ceiling, and it is why Open Camera — which reads both lists — reached 50.3 MP unaided.
8. **The preference trap.** `pref_raw_key_N` and `pref_fix_resolution_key_N` independently break Gcam initialization by triggering the port's `getFixResolutionList` width-cap, which can shrink a sensor's RAW list to an odd size. This already caused one misattributed failure. **Check for and clear these before diagnosing anything else.**
9. **Signing.** No signing key ships in any distributed artifact. **Verified empirically 2026-08-24 by Faz 1.2**, not merely asserted: all five released archives (`ishtar-cam-modes-v1.0/v1.9/v2.0/v2.1`, `ishtar-aon-fix-v1.1`) were listed by entry name and contain no `.keystore`, `.jks`, `.p12`, `.pem`, or `.key` entry, and no entry at the 2,664-byte size of the local `debug.keystore`. Three sub-rules now carry this invariant forward:
   - **9a — Packaging assertion (specification for Faz 9.1 to implement).** A release archive is rejected if any of three conditions holds: (i) it contains an entry whose name ends in `.keystore`, `.jks`, `.p12`, `.pem`, or `.key`; (ii) it contains an entry at or near 27,268,688 bytes, the size class of `camera.qcom.so`, which would mean a vendor HAL binary was packaged; (iii) it contains any `.apk` entry other than exactly one named `tile-app.apk`. Each condition must be proven to fail the build when deliberately introduced — an assertion never observed failing is not an assertion. The check is by entry name and entry size only; no entry is extracted.
   - **9b — Key location policy.** The signing key belongs outside the repository and outside the packaged module directory. Today `ishtar-cam-modes/tile-app/build.sh` sets it to `$HERE/debug.keystore`, which places it inside the directory that gets zipped — containment currently depends entirely on the `.gitignore` rule and on the packaging step never sweeping it in. The key should be referenced through an external path supplied by the environment, with no concrete credential location recorded in any planning file. The key is auto-generated on first build if absent, so relocating it costs nothing except signing identity: a regenerated key changes the tile application signature and breaks upgrade-in-place for existing installs.
   - **9c — The password is not contained, and is not really a secret.** `build.sh` hardcodes the keystore store-password, key-password, and alias in plaintext, and that script ships inside `ishtar-cam-modes-v1.9`, `v2.0`, and `v2.1`. The values are deliberately not reproduced here or anywhere in `Planner-docs/`; measured without printing, the password is a six-character all-lowercase word that already appears publicly elsewhere in the repository. The consequence is that removing it from `build.sh` would not make it secret — it is guessable on the first attempt whether or not the script ships. Nothing is exploitable today, because the keystore itself has never been distributed and a password without its keystore grants nothing. The real rule this yields: **if the key is ever relocated per 9b, reused for a signed public release, or regenerated, it must get a genuine password at that moment** — the current one protects only a locally regenerable debug key. Routed as `DEC-10`.
10. **Blob binding.** Every offset is bound to one exact vendor build. Any ROM update that changes `camera.qcom.so` invalidates all offsets at once; the md5 guard is the detector.
11. **Host constraint.** Neither the kernel nor AOSP builds on Windows/NTFS. Sources must live inside the WSL filesystem, never under `/mnt/c`. Disk is no longer a constraint (799 GB free); WSL2 is not installed.

## 8. Open Ontology Questions

### Competency Questions

| ID | Question | Status | Evidence |
|---|---|---|---|
| OQ-01 | Where does `camera.qcom.so` write `android.sensor.info.pixelArraySize` (tag `f0006`)? | open | 9 movz/movk sites and 6 rodata dwords located; write site not found |
| OQ-02 | Does the HAL deliver remosaiced Bayer or raw Quad-Bayer at 8192x6144? | open | never captured — no successful full-res RAW frame yet |
| OQ-03 | Can `pixelArraySize` be raised without breaking other consumers? | open | untested; the opposite direction (active array) is known to break AGC (Faz 4) |
| OQ-04 | Is the 10-bit/12-bit mismatch the *only* obstacle to 50 MP + LN composition? | open | assumed by `Kararlar #4`; no measurement confirms exclusivity of the cause |
| OQ-05 | Is patch application atomic against power loss mid-write? | open | not inspected; `halpatch.sh` not read in this pass |
| OQ-06 | Does the WebUI pass any user input into a shell invocation? | open | `webroot/index.html` (344 lines) not read in this pass |
| OQ-07 | Does `customize.sh` normalize `mode` and `active/` at install time? | open | `customize.sh` (78 lines) not read in this pass |
| OQ-08 | Does `ishtar-cam-modes` ship its own `sepolicy.rule`? | open | present in the reference modules; not verified for this one |
| OQ-09 | Does any released zip already contain `debug.keystore`? | answered (no) | Faz 1.2 audit, 2026-08-24: all five archives listed by entry name; zero `.keystore`/`.jks`/`.p12`/`.pem`/`.key` entries and zero entries at the 2,664-byte keystore size. Adjacent finding: the keystore password ships in plaintext inside `tile-app/build.sh` in v1.9/v2.0/v2.1 (see invariant 9c, `DEC-10`). |
| OQ-10 | Does the device's live state match the workspace `mode` file (`stock`)? | answered (no) | Faz 2.1 smoke run 2026-08-30: device is on `dcgB`, workspace file says `stock`. The workspace file tracks the last host-side edit, not the device. |
| OQ-11 | Why is the `tiles hide` option ineffective? | open | observed ineffective; cause never diagnosed |
| OQ-12 | Which framework camera index maps to which physical sensor across all lenses? | partially_answered, and the previous answer is now in doubt | Faz 2.1 measurement 2026-08-30 contradicts the stored shorthand: `dumpsys media.camera` maps framework device 3 to HAL id 9, which is **Front**-facing at 3264x2448 and cannot be the rear main. The rear IMX989 array sits on HAL id 0 and ids 2-7 and 10. Full per-device table in section 3. See `OQ-17`. |
| OQ-13 | Are `Lddl;->P/Q` blocklists relevant to resolution filtering? | answered | **No** — both empty; hypothesis rejected |
| OQ-14 | Does the port have a working 48M mechanism? | answered | **No** — `Forty8Strip` is an identity stub; hypothesis rejected |
| OQ-15 | Why did AGC cap at 12.6 MP? | answered | `getOutputSizes()` high-resolution bucket exclusion (invariant 7), not a blocklist or a flag |
| OQ-16 | Why did the Faz 4 wide patch break AGC? | answered | same invariant as Faz 12, opposite direction (invariant 6) |
| OQ-17 | Which HAL camera id is the one the 16-point `fullres` patch actually modifies, and which one does AGC open? | open | Raised by the Faz 2.1 smoke run, 2026-08-30. Eight Back-facing devices share the 4096x3072 array, and none currently reports the 508 entries `EV-16` recorded under a `fullres` HAL. Settle by taking a smoke snapshot with the HAL in `fullres` and diffing against the stock baseline: the device whose `streamcfg` count moves is the one being patched. This is a prerequisite for Faz 4.1 stating its target array count as a number. |
