# Reverse-Engineering Toolchain Procedure

The analysis and repackaging toolchain for this project: Java/smali for the AGC
port, and native disassembly for `camera.qcom.so`.

**This is not the build toolchain.** See section 7 — ROM and kernel building is
a different environment with a different blocker, and the two must not be
conflated.

This document records versions, ordered steps, self-checks, and the dead ends
that already cost time. It does not install anything and does not carry any
tool, APK, key, or download location.

## 1. Host state, measured 2026-08-30

Measure before following any step below; two of these values changed since the
project last recorded them.

| Component | State on this host | Consequence |
|---|---|---|
| `python` | **Present — CPython 3.14.7**, `C:\Users\ahmet\AppData\Local\Programs\Python\Python314\python.exe` | **Corrects the prior record.** See the note below. |
| `py` | Present, 3.14.7 (launcher) | Usable |
| `python3` | **Windows Store alias stub**, not an interpreter | Never invoke `python3` on this host; it is the reason Python read as absent |
| `capstone` | **Not installed** | `pip install capstone` required before disassembly |
| `pyelftools` | **Not installed** | `pip install pyelftools` required before disassembly |
| `java` | **Absent from PATH** | The Java path below cannot run today; its self-check is deferred, not skipped |
| `adb` | Present, vendored at `platform-tools/adb.exe` | The only host-device channel |

**Correction to the record (F1.4-04).** The project has recorded since
2026-08-24 that "no Python interpreter is available through the normal path",
and the Step 3 audit fell back to a hand reimplementation of the bundled
validator for exactly this reason. That is **no longer true**. A real CPython
3.14.7 is installed. The earlier finding was correct in what it measured and
wrong in what it concluded: `python3` resolves to the Microsoft Store alias
stub on this machine and always will, so probing `python3` alone reports
absence even when `python` works. Probe `python` and `py`, not `python3`.

Two consequences follow immediately. First, the **embeddable** Python 3.12.7
distribution recorded in the address book is no longer a *requirement* on this
host — it was a workaround for an interpreter that turns out to exist. A normal
`pip install` into the existing 3.14.7 now serves. Keep the embeddable option
recorded only as the fallback for a host that genuinely lacks Python. Second,
`scripts/validate_planner_docs.py` **can now be executed**, which closes the
validator gap the Step 3 audit documented.

`ishtar-cam-modes/tools/verify_ln.py` needs only the standard library and was
always runnable once any interpreter existed; the disassembly path is the one
with third-party dependencies.

## 2. Java and smali path (AGC port)

Used to disassemble, edit, and reassemble the AGC (GCam port) APK.

**Versions — exact, and the group matters.**

| Component | Version | Note |
|---|---|---|
| Temurin JDK | 21 | |
| smali / baksmali | **2.5.2** | Legacy `org/smali` Maven group, `org.jf.*` package names |
| dexlib2 | matching 2.5.2 | On the classpath |
| util | matching 2.5.2 | On the classpath |
| guava | 31.1-jre | |
| failureaccess | (guava companion) | Required, easy to omit |
| antlr-runtime | 3.5.2 | |
| jcommander | 1.82 | |
| ST4 | (matching) | |
| uber-apk-signer | 1.3.0 | Signing step |

**Procedure.** The working recipe already exists and is not restated here:
`agc-50mp-yama/README.md`, "Yeniden üretme". It gives the five steps — extract
`classes2.dex`, `baksmali ... d`, swap the two smali sources in this repo,
`smali ... a -a 29`, then replace the dex entry and sign. Two details from it
are worth repeating because they are easy to lose:

- **`-a 29`** on reassembly. The API level is not optional.
- When replacing the `classes2.dex` entry inside the APK, **the other entries'
  compression method must be preserved**. Rewriting the whole zip changes them
  and the result may not install.

**Signing.** Use uber-apk-signer 1.3.0 with `--allowResign`. The key location
follows the Faz 1.2 policy; no key path, alias, or password appears in this
document, and none should be added to it. Note the consequence recorded in the
seed recipe: the signature changes, so the app must be uninstalled and
reinstalled rather than upgraded in place, and app data must be preserved
manually if wanted.

## 3. Do not attempt (F1.4-02)

Four dead ends, each of which already cost real time. Each is stated with the
symptom so it is recognised if hit anyway.

1. **Do not try to invoke apktool's bundled smali.** apktool ships smali `Main`
   classes as **stripped stubs**. Symptom: the class is found on the classpath
   but will not run as an entry point. Use the standalone smali/baksmali 2.5.2
   jars instead.
2. **Do not fetch smali from the `com.android.tools.smali` Maven coordinates.**
   Symptom: **HTTP 404**. The artifacts this project needs are under the legacy
   `org/smali` group.
3. **Do not fall back to the Bitbucket mirror.** Symptom: **HTTP 403**.
   Relatedly, `google/smali` publishes **no release binaries** at all, so there
   is no upstream binary to fall back to either.
4. **Do not use radare2 or rabin2 5.9.8 on `camera.qcom.so`.** Symptom: **no
   output within 300 seconds**, reproduced from both shells, on the 27 MB
   binary. This is why the disassembly path below is a capstone script rather
   than an interactive tool — the choice is forced, not stylistic.

## 4. Native disassembly path (`camera.qcom.so`)

Used to locate and verify AArch64 instruction sites in the 27,268,688-byte
camera HAL.

**Components.** capstone 5.0.7 and pyelftools, on any working interpreter. On
this host that is the installed CPython 3.14.7 (`pip install capstone
pyelftools`). On a host with no interpreter, use the embeddable Python 3.12.7
distribution — recorded as the fallback, no longer the default here.

**Why a script and not an interactive tool.** Negative finding 4 above:
radare2/rabin2 5.9.8 does not complete on this binary within 300 s. A capstone
script that seeks to a known offset and decodes a bounded window returns in
milliseconds. Disassemble windows, not the whole binary.

**Working offsets** are recorded in `Planner-docs/Project-Ontology.md` section 6
("Reverse-engineering address book") and must be read from there, not
rediscovered. `InitializeScalerStaticCaps` spans `0x16bf4c0`-`0x16c5a90`
(26 KB, 6,516 instructions).

**Getting bytes without the binary on the host.** The HAL is not in version
control and not in the module archive (27 MB). Two ways to read it:

- Whole file: `adb pull /odm/lib64/hw/camera.qcom.so`.
- **A single word, which is usually all that is needed** — read-only, four
  bytes, no pull:

```sh
adb shell su -c "dd if=/odm/lib64/hw/camera.qcom.so bs=4 skip=<index> count=1 2>/dev/null | od -An -tx1"
```

`<index>` is the byte offset divided by 4, the same unit the patch tables use
(`docs/patch-table-format.md` section 2). Confirm what you are reading first:
`md5sum` the file and compare against `HAL_STOCK_MD5`
(`c3fa63a86ee3ecaf9fbf02005d35f6b5`). If the module's bind mount is active, this
path returns the module's copy, which is byte-identical to stock while the HAL
layer is in `stock` state.

## 5. Self-checks

Run these before relying on either path.

### 5.1 Java path — `VAL-TOOLCHAIN`

Extract `classes2.dex` from an AGC build and disassemble it; confirm `LAGC;`
appears in the output.

```sh
unzip -o AGC8.4.300_V9.6_snap.apk classes2.dex
java -cp "<smali-jars>" org.jf.baksmali.Main d -o out2 classes2.dex
ls out2/AGC.smali          # expected: the file exists
```

**Status on this host: NOT EXECUTED — `java` is absent from PATH** (section 1).
This is recorded rather than worked around, and rather than reported as a pass
it did not earn. Installing the JDK is the implementer's action and is outside
this sub-phase's scope. Run this self-check before the first AGC repackaging;
until then the Java path is documented but unproven here.

### 5.2 Disassembly path — `VAL-DISASM`

Decode the four `cmp` sites recorded in the address book and compare them
against the recorded instruction form. This check is self-verifying: the
expected answer is already written down, so a mismatch convicts either the
procedure or the address book, and either finding is worth having.

**Status on this host: EXECUTED AND PASSED, 2026-08-30**, against the live
binary on device `dc27e5d0`, `md5 c3fa63a86ee3ecaf9fbf02005d35f6b5` (stock
confirmed), size 27,268,688 (matches the recorded size).

| Address book site | Index (÷4) | Bytes read from device | LE word | Decodes as |
|---|---|---|---|---|
| `0x16c18dc` | 5965367 | `7f 09 00 71` | `0x7100097F` | `CMP W11,#2` |
| `0x16c1c18` | 5965574 | `ff 08 00 71` | `0x710008FF` | `CMP W7,#2` |
| `0x16c22bc` | 5965999 | `9f 0a 00 71` | `0x71000A9F` | `CMP W20,#2` |
| `0x16c2330` | 5966028 | `9f 0a 00 71` | `0x71000A9F` | `CMP W20,#2` |

All four decode as `cmp wN,#2`, exactly as the address book states. Two
independent cross-checks also hold: every index times four reproduces the
recorded hex address exactly, and every byte quartet matches the stock column of
`agc-50mp-yama/hal-raw50-deneme.patch` byte for byte — a table written on
2026-08-23 by a different route.

The address book's parenthetical warning is confirmed useful: `0x16c2334` is the
following `b.lo`, **not** a fifth `cmp`. There are four sites, not five.

No correction to `Project-Ontology.md` section 6 is required by this check.

## 6. External inputs (F1.4-06)

The procedure consumes APK builds that this repository **does not carry**. They
are excluded from version control by `.gitignore` (see `UNTRACKED-BY-DESIGN.md`)
and must be supplied separately. They are identified here by checksum so the
right build can be confirmed, **not** by download location — this document does
not redistribute and does not tell anyone where to obtain them.

| Artifact | md5 | Role |
|---|---|---|
| `AGC8.4.300_V9.6_snap.apk` | `fa4066eb3bf82cc097906fd108073500` | Stock V9.6. The **input** to the 50MP patch; step 1 of the seed recipe extracts `classes2.dex` from this build. |
| `AGC8.4.300_V9.6_50MP_patched.apk` | `ce65f862c990e2acc02be356f75a7122` | The **output**. Confirmed installed on device `dc27e5d0` as `org.codeaurora.snapcam` (Faz 2.1 smoke run). |
| `AGC8.4.300_V14_snap.apk` | `46763b3628f025a54828aab05c01d47a` | Stock V14. Comparison build; the obfuscation map is identical to V9.6. |
| `OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk` | `e4efeb07919bce10bc14f6f42e5b09f2` | Third-party consumer used to prove 8192x6144 capture works outside AGC. |

The AGC port's redistribution governance question is open in Autopsy section 9
and is **not** resolved here.

## 7. Boundary against the Phase 7 build toolchain (F1.4-07)

This procedure covers **analysis and repackaging only**, and it runs on the
Windows host as-is.

Building the ROM or the kernel is a different toolchain in a different
environment. Under `DEC-24` (2026-09-10) that environment is not WSL2 on this
host but a rented Hetzner Cloud server running Ubuntu 22.04 LTS (`DEC-22`),
provisioned, used and deleted within one session by `docs/build-environment.md`;
`Faz7.1` stages its inputs on GitHub and `Faz7.2` runs it. Nothing in this
document unblocks a build, and the presence of a working Python interpreter here
does **not** narrow the Phase 7 gap — that gap is a Linux build server, not an
interpreter. (Corrected 2026-09-11 by `IMPL-91`; the retired sentence said
provisioning WSL2 "is Phase 7's entire purpose".)

Keep the two separate when reporting status. "The toolchain works" is true of
this document and false of Phase 7.

## 8. Coverage against the address book

Every component recorded in `Planner-docs/Project-Ontology.md` section 6
appears above with its exact version: Temurin JDK 21; smali/baksmali 2.5.2 from
the legacy `org/smali` group with `org.jf.*` package names; dexlib2; util; guava
31.1-jre; failureaccess; antlr-runtime 3.5.2; jcommander 1.82; ST4;
uber-apk-signer 1.3.0; capstone 5.0.7; pyelftools; embeddable Python 3.12.7
(now recorded as a fallback rather than a requirement, per section 1).

All four recorded negative findings appear in section 3 as explicit non-steps
with their symptoms. No component is named here that the address book does not
record.
