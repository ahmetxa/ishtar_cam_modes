# Build Environment — AOSPA `beryl` for `ishtar` on a rented server

The rental runbook for Main-Planing Phase 7. `Faz7.1` wrote it (`IMPL-91`,
2026-09-11); `Faz7.2` executes it in one paid session, from provisioning to
teardown, without re-planning.

**Secrets rule.** No token, SSH key, password or server address is written in
this file, in any repository, snapshot or planning file. The server address
exists only in the operator's shell session (`read -r BUILD_HOST`); the SSH
private key never leaves the Windows host.

**Script rule.** Every scripted block starts with `set -euo pipefail`, so a
non-zero exit stops it. Output is kept in log files; only exit status, stage,
error class and the last lines of a failing log are read or recorded.

## 1. Decisions and inputs

| Item | Value | Source |
|---|---|---|
| Host | Rented server, not WSL2 | `DEC-24` (2026-09-10) |
| Distribution | Ubuntu 22.04 LTS. Fallback if Hetzner no longer offers the image: Ubuntu 24.04 LTS plus the `sysctl` in section 7 | `DEC-22` (2026-09-11) |
| Server type | Hetzner Cloud CCX53: 32 dedicated vCPU (AMD), 128 GB RAM, 600 GB NVMe | `DEC-25` (2026-09-11) |
| Budget and stopping rule | 10 hours of server existence, section 4 | `DEC-25` |
| Repository access | `ahmetxa/android_device_xiaomi_ishtar` and `ahmetxa/android_local_manifests` are public; the server holds no GitHub credential | `DEC-25` |
| Base manifest | `AOSPA/manifest` `beryl` at `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` | `F7.1-07` |
| Local manifest | `ahmetxa/android_local_manifests` `main` at `22283d8a866d042e02336fcb4698253ac6bf9c3b` (section 8) | `F7.1-03` … `F7.1-09` |
| Build command | `./rom-build.sh ishtar -z`: default build type `userdebug` (thin kernel LTO); `-z` also writes the fastboot image package | `AOSPA/android_vendor_aospa` `beryl` `build.sh` lines 19, 47, 74, 277–294 |

## 2. Sizing floor

| Requirement | Published figure | Source | CCX53 |
|---|---|---|---|
| CPU | "A 64-bit x86 system" | [AOSP hardware requirements](https://source.android.com/docs/setup/start/requirements) | 32 vCPU AMD, x86-64 |
| Memory | "A minimum of 64 GB of RAM" | same | 128 GB |
| Disk | "At least 400 GB of free disk space to check out and build the code (250 GB to check out + 150 GB to build)" | same | 600 GB |
| OS | "any 64-bit Linux distribution with GNU C Library (glibc) 2.17 or later"; "To build Android 11 or higher, you must use Ubuntu 18.04 or later" | same | Ubuntu 22.04 |
| OS, AOSPA | "Google recommends using Ubuntu" and points to Google's setup instructions | `AOSPA/manifest` `beryl` `README.md` lines 5–8 | — |

CCX43 (64 GB RAM, 360 GB disk) meets the memory floor but not the disk floor
without a separately billed volume, which is why it was not chosen.

**Ubuntu 24.04 caveat.** Ubuntu 23.10 and later restrict unprivileged user
namespaces through AppArmor, which breaks AOSP's `nsjail` build sandbox
([Launchpad bug 2063976](https://bugs.launchpad.net/ubuntu/+source/apparmor/+bug/2063976)).
22.04 does not carry that restriction.

## 3. Provider billing and deletion semantics (`AUDIT-FIX-43`)

Read 2026-09-11 from [Hetzner Cloud billing FAQ](https://docs.hetzner.com/cloud/billing/faq/)
and [Hetzner Cloud FAQ](https://docs.hetzner.com/cloud/general/faq/):

- **Product and unit.** Hetzner Cloud server, billed hourly with a monthly cap:
  "Your server's bill will never exceed its monthly price cap. If you delete
  your cloud server before the end of the billing month, we will only bill you
  for the hourly rate."
- **Powered off still bills.** "you pay for a server that has completed the
  creation process for as long as it exists, regardless of whether it is turned
  on or not." "We will bill you for your servers until you delete them,
  independent of their state." **Shutting down is not teardown; only deletion
  stops the charge.**
- **What else bills.** "We bill Primary IPs (IPv4, IPv6) and cloud servers
  separately." "If you want to stop paying for a Primary IP, you need to delete
  it. If it still exists, we will still bill you for it." Snapshots bill "per
  gigabyte per month"; backups are "a monthly flat price, which is 20% of the
  price of the server". This runbook creates no snapshot, backup or volume;
  the pages read do not describe volume billing, so none is created.
- **Account limits.** New accounts have per-resource limits, shown on the
  Console's "Limits" tab. "Limit Requests are processed manually and reviewed
  on a case-to-case basis during our business hours." **Check the CCX53 limit
  days before the rental day.**
- **Prices (third-party, confirm in the Console at creation).** CCX53 €0.8550
  per hour, cap €533.49 per month; Primary IPv4 €0.50 per month (€0.0008 per
  hour); all excluding VAT. Source: [costgoat Hetzner price table](https://costgoat.com/pricing/hetzner),
  updated 2026-09-05. The Hetzner page read the same day
  ([general purpose](https://www.hetzner.com/cloud/general-purpose/)) gave the
  specifications but no figures.

## 4. Budget and stopping rule (`DEC-25`)

- **Clock.** Starts when the Console shows the server created; ends when the
  server and its Primary IP are deleted.
- **Ceiling.** 10 hours, about €8.6 plus VAT at the section 3 price.
- **Sync failure** (`repo sync`, or barista's "Unexpected exit status from the
  brewing process" in the build log): stop. Retrieve the evidence in section
  10, then tear down.
- **Build failure:** classify it. Only a manifest-class error — a deferred
  item's detector in the table below, a missing project, or a wrong branch or
  commit — gets a fix attempt, and at most **2** attempts in the session. Any
  other error class: stop, retrieve and tear down; the error becomes a
  replanning input.
- **Hour 8:** whatever state the build is in, retrieve what exists (sections 10
  and 11) and tear down (section 12).
- **Recorded per stage:** start and end time (UTC), exit status, error class,
  and the last lines of a failing log. Never whole logs.

Deferred items and their allowed fixes (from the manifest `README.md`):

| Item | Detector | Fix attempt |
|---|---|---|
| `display-drivers` pin | Compile or `modpost` failure in `vendor/qcom/opensource/display-drivers` during the kernel stage | Delete its `remove-project` and `project` lines (barista's AOSPA commit `09008c5` returns) |
| `hardware/qcom/gps`, `hardware/qcom/media` | Compile error under either path | None staged: stop |
| Shallow sync of the three blob repositories | `repo sync` error for `vendor/xiaomi/*` naming an unadvertised object, "not our ref" or a missing remote ref | Delete that project's `clone-depth="1"` and sync it again |
| `hardware/xiaomi` | Soong error under `hardware/xiaomi`, or missing `xiaomifingerprint_headers` | Delete its two lines (`vauxite` returns) |
| `vendor/xiaomi/camera` | Sync failure on that path | Delete its two lines (`vauxite-sm8550-leica` returns) |

A fix on the server edits `.repo/local_manifests/ishtar-beryl.xml` in place,
records the diff in `~/evidence/fixes.diff`, and is not pushed during the
session.

## 5. Before renting (Windows host, free)

Run in Git Bash on the day of the rental. `GH` points at the WinGet `gh.exe`
when `gh` is not on `PATH`.

```bash
set -euo pipefail
GH="${GH:-gh}"; export GH
work="$(mktemp -d)"
git clone -q https://github.com/ahmetxa/android_local_manifests "$work/m"
test "$(git -C "$work/m" rev-parse HEAD)" = "22283d8a866d042e02336fcb4698253ac6bf9c3b"
( cd "$work/m" && python check.py )
set +e
( cd "$work/m" && python check.py tests/known-bad-1.xml tests/known-bad-2.xml ) > "$work/neg.txt"
neg=$?
set -e
test "$neg" -eq 1
grep -qx '14 element(s) failed' "$work/neg.txt"
for r in ahmetxa/android_local_manifests ahmetxa/android_device_xiaomi_ishtar; do
  test "$("$GH" api "repos/$r" --jq .private)" = false
done
echo "pre-rental checks passed"
```

Then, by hand:

1. Hetzner Console, Limits tab: one CCX53 is allowed. If not, request the limit
   increase and wait for it; do not rent another type silently.
2. Console, Security, SSH keys: your **public** key is present.
3. The output directory `~/Documents/Projeler/ishtar-builds/` exists **outside**
   any git repository. Build outputs carry proprietary vendor blobs and are never
   committed or published (`ARC-04`).
4. The session has the time: the 10 h ceiling fits before you stop for the day.

## 6. Provisioning (Hetzner Console)

- Location: an EU location offering CCX53. Image: **Ubuntu 22.04**. Type:
  **CCX53**.
- Networking: public IPv4 on (unless your connection has IPv6), IPv6 on.
- SSH key: yours. Volumes: none. Backups: off. No cloud-init, no placement group.
- Name: `ishtar-beryl-build`.
- Write down the creation time (UTC) for the timeline. Copy the address into
  your shell only:

```bash
set -euo pipefail
read -r -p 'server address: ' BUILD_HOST
export BUILD_HOST
ssh "root@$BUILD_HOST"
```

## 7. Server setup (as root, once)

```bash
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
# AOSP's package list for Ubuntu 18.04 or later (source.android.com, "Establishing a build environment"), plus tmux
apt-get install -y git-core gnupg flex bison build-essential zip curl zlib1g-dev libc6-dev-i386 \
  x11proto-core-dev libx11-dev lib32z1-dev libgl1-mesa-dev libxml2-utils xsltproc unzip fontconfig \
  python3 tmux
if [ "$(. /etc/os-release && echo "$VERSION_ID")" != "22.04" ]; then
  sysctl -w kernel.apparmor_restrict_unprivileged_userns=0   # 24.04 fallback only, section 2
fi
useradd -m -s /bin/bash builder
install -d -m 700 -o builder -g builder /home/builder/.ssh
install -m 600 -o builder -g builder /root/.ssh/authorized_keys /home/builder/.ssh/authorized_keys
df -h / | tail -n 1
nproc
free -g | head -n 2
```

The build runs as `builder`, not root. Reconnect as `ssh "builder@$BUILD_HOST"`
and start `tmux new -s build`, so a dropped connection does not kill the sync
or the build.

```bash
set -euo pipefail
mkdir -p ~/.bin ~/evidence ~/logs ~/out-pkg
repo_tmp="$(mktemp)"
curl -fsS -o "$repo_tmp" https://storage.googleapis.com/git-repo-downloads/repo
gpg --recv-keys 8BB9AD793E8E6153AF0F9A4416530D5E920F5C65
curl -fsS https://storage.googleapis.com/git-repo-downloads/repo.asc | gpg --verify - "$repo_tmp"
install -m 755 "$repo_tmp" ~/.bin/repo
grep -q 'HOME/.bin' ~/.bashrc || echo 'export PATH="$HOME/.bin:$PATH"' >> ~/.bashrc
git config --global user.name "ishtar build"
git config --global user.email "build@invalid"
git config --global color.ui false
printf '%s setup-done\n' "$(date -u +%FT%TZ)" >> ~/evidence/timeline.txt
```

The repo download and signature check follow AOSP's manual installation; the
git identity carries no personal data.

## 8. Sync

`22283d8a866d042e02336fcb4698253ac6bf9c3b` is the `ahmetxa/android_local_manifests` commit read back after
the `IMPL-91` push: see the ledger row. Replace it in this file when it changes.

```bash
set -euo pipefail
export PATH="$HOME/.bin:$PATH"
stamp() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" >> ~/evidence/timeline.txt; }
mkdir -p ~/beryl && cd ~/beryl
stamp sync-start
repo init -u https://github.com/AOSPA/manifest -b beryl > ~/logs/init.log 2>&1
base="$(git -C .repo/manifests rev-parse HEAD)"
stamp "base $base"
if [ "$base" != 7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2 ]; then
  echo "AOSPA/manifest beryl moved past the pin: decide before syncing (stopping rule)"
  exit 1
fi
git clone -q https://github.com/ahmetxa/android_local_manifests .repo/local_manifests
test "$(git -C .repo/local_manifests rev-parse HEAD)" = "22283d8a866d042e02336fcb4698253ac6bf9c3b"
if ! repo sync --current-branch --no-tags --fail-fast -j16 > ~/logs/sync.log 2>&1; then
  stamp "sync-failed"
  tail -n 40 ~/logs/sync.log
  exit 1
fi
stamp sync-done
df -h . | tail -n 1
```

`repo` loads only the top-level `.repo/local_manifests/*.xml` files, so the
deliberately invalid `tests/known-bad-*.xml` cases in the clone are never read
as manifests.

## 9. Build

```bash
set -euo pipefail
export PATH="$HOME/.bin:$PATH"
stamp() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" >> ~/evidence/timeline.txt; }
cd ~/beryl
stamp build-start
if ! ./rom-build.sh ishtar -z > ~/logs/build.log 2>&1; then
  stamp "build-failed"
  grep -m 5 -nE 'FAILED:|error:|ninja: build stopped|Unexpected exit status from the brewing process' ~/logs/build.log || true
  tail -n 60 ~/logs/build.log
  exit 1
fi
if grep -q 'Unexpected exit status from the brewing process' ~/logs/build.log; then
  stamp "barista-sync-failed"
  echo "barista's sync failed although the build returned 0: treat as a sync failure"
  exit 1
fi
stamp build-done
ls -1 aospa-*.zip
```

The barista check exists because AOSPA's `lunch` does not test barista's exit
status (`AOSPA/android_build` `beryl` `envsetup.sh` line 582).

## 10. Evidence (before teardown, whatever the outcome)

Collect what exists; a missing file is recorded, not fatal, so a failed build
still leaves evidence.

```bash
set -euo pipefail
export PATH="$HOME/.bin:$PATH"
cd ~/beryl
E=~/evidence
OUT=out/target/product/ishtar
repo manifest -r -o "$E/manifest-resolved.xml"
if grep -nE '://[^/" ]+@' "$E/manifest-resolved.xml"; then
  echo "credential-shaped URL in the resolved manifest: do not copy it"; exit 1
fi
{
  echo "== consumed tree entry"
  grep -n 'aon_front.pb' device/xiaomi/ishtar/proprietary-files.txt || echo "aon_front.pb entry MISSING"
  echo "== built symlink"
  if [ -L "$OUT/odm/lib64/camera/aon_front.pb" ]; then
    echo "symlink -> $(readlink "$OUT/odm/lib64/camera/aon_front.pb")"
  else
    echo "odm/lib64/camera/aon_front.pb is NOT a symlink or does not exist"
  fi
  echo "== camera blobs (md5, size, path)"
  for f in odm/lib64/hw/camera.qcom.so odm/lib64/hw/camera.xiaomi.so \
           odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin; do
    if [ -f "$OUT/$f" ]; then
      printf '%s  %s  %s\n' "$(md5sum < "$OUT/$f" | cut -d' ' -f1)" "$(stat -c %s "$OUT/$f")" "$f"
    else
      echo "MISSING  $f"
    fi
  done
  echo "== selinux in the common board config"
  grep -n 'selinux' device/xiaomi/sm8550-common/BoardConfigCommon.mk || echo "no selinux line"
} > "$E/build-evidence.txt"
for l in init sync build; do
  [ -f ~/logs/$l.log ] && tail -n 200 ~/logs/$l.log > "$E/$l.log.tail" || true
done
if grep -rlE 'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_|-----BEGIN [A-Z ]*PRIVATE KEY' "$E"; then
  echo "token-shaped string in evidence: inspect before copying"; exit 1
fi
tar -C ~ -czf ~/out-pkg/evidence.tar.gz evidence
```

The evidence list serves `Faz8.1` (the three blob md5s and sizes) and `Faz7.3`
(the `aon_front.pb` entry and the built symlink). Elapsed time per stage is in
`timeline.txt`.

## 11. Retrieval with sha256 at both ends (`AUDIT-FIX-44`)

What the `ishtar` install needs, and why each item is retrieved:

| Artifact | Produced at | Install method that consumes it |
|---|---|---|
| `aospa-<version>-image.zip` | source root, by `-z` | Fastboot package: `fastboot update` (the `xiaomi-8550/aospa-flashing-kit` `flash_aospa.sh` method for the sibling devices; the older XDA `ishtar` method) |
| `aospa-<version>.zip` | source root | Recovery method: `adb sideload` from AOSPA recovery (the current XDA `ishtar` method) |
| `recovery.img` | `$OUT` | Recovery method: `fastboot flash recovery recovery.img` before sideloading (`recovery` is an A/B partition, `BoardConfigCommon.mk` line 18) |
| `boot.img`, `init_boot.img`, `vendor_boot.img`, `dtbo.img`, `vbmeta.img`, `vbmeta_system.img` | `$OUT` | Individually flashable boot-chain partitions (`AB_OTA_PARTITIONS`, lines 12–26); also inside the image package, retrieved loose so a partial reflash needs no unzip |
| `evidence.tar.gz` | `~/out-pkg` | Section 10 |
| `aospa_ishtar-target_files.zip` | `$OUT/obj/PACKAGING/target_files_intermediates/` | **Optional.** Every partition image can be re-extracted from it; retrieve only if the ceiling allows |

Not a build output, and so not retrievable from the server: **Xiaomi firmware.**
Both flashing kits flash it separately from a firmware package. No source read
by `Faz7.1` states which firmware version `beryl` needs on `ishtar`; that, and
whether the Android 15 → 16 change needs a data format (`AUDIT-FIX-45`), belong
to `Faz7.3` before anything is flashed.

On the server:

```bash
set -euo pipefail
cd ~/beryl
OUT=out/target/product/ishtar
P=~/out-pkg
test "$(ls -1 aospa-*-image.zip | wc -l)" -eq 1
test "$(ls -1 aospa-*.zip | wc -l)" -eq 2
cp aospa-*.zip "$P/"
for i in boot init_boot vendor_boot dtbo recovery vbmeta vbmeta_system; do
  cp "$OUT/$i.img" "$P/"
done
( cd "$P" && sha256sum -- * > SHA256SUMS )
du -sh "$P"
```

If the build failed, only `evidence.tar.gz` exists: run
`( cd ~/out-pkg && sha256sum -- * > SHA256SUMS )` alone.

On the Windows host (Git Bash):

```bash
set -euo pipefail
test -n "${BUILD_HOST:-}"
D="$HOME/Documents/Projeler/ishtar-builds/$(date +%Y%m%d)"
mkdir -p "$D"
scp "builder@$BUILD_HOST:out-pkg/*" "$D/"
( cd "$D" && sha256sum -c SHA256SUMS )
echo "retrieved and verified: $D"
```

**Do not tear down until `sha256sum -c` reports OK for every file.**

## 12. Teardown

1. `sha256sum -c` on the host passed for every retrieved file.
2. Console, Servers: **delete** `ishtar-beryl-build`. Not shut down; deleted.
3. Console, Primary IPs: delete any Primary IP still listed. It bills until
   deleted.
4. Console: no volume, snapshot or backup exists in the project.
5. Billing stopped: the project lists zero servers and zero Primary IPs. Write
   down the deletion time (UTC); elapsed = deletion − creation, compared against
   the 10 h ceiling.
6. Credentials: none were issued (`DEC-25`, public repositories). If that plan
   ever changes to a token, revoke it here.
7. On the host: `ssh-keygen -R "$BUILD_HOST"`, then `unset BUILD_HOST`.

## 13. What `Faz7.2` records in the ledger

One implementation row: stage-by-stage exit status and elapsed time from
`timeline.txt`; the error class and last lines of any failing log (not whole
logs); fix attempts used (of 2) with `fixes.diff`; the `AOSPA/manifest` base and
`22283d8a866d042e02336fcb4698253ac6bf9c3b`; the retrieved file names with their sha256; the section 10
evidence values; the deletion time and total elapsed hours against the ceiling.
