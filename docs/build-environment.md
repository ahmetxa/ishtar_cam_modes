# Build Environment — AOSPA `beryl` for `ishtar` on a rented server

> **Historical as of 2026-11-13.** The user abandoned the plan to build an
> AOSPA ROM for `ishtar`. The phone now runs HyperOS 4 (`OS4.0.0.44.WMACNXM`,
> Android 17), measured read-only in
> `snapshots/20261113-1819__IMPL96__hyperos4-readonly-probe.txt`. This runbook
> will not be executed, and nothing was ever rented under it. The rest of this
> file is unchanged and stays as the record of the planned `Faz7.2` session;
> the ledger records the decision in `IMPL-96`.

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
| Host | Rented Scaleway Instance, not WSL2 | `DEC-24` (2026-09-10); provider `DEC-26` (2026-09-14) |
| Distribution | Ubuntu 22.04 LTS. Fallback if the Scaleway Console does not offer 22.04 for the type: Ubuntu 24.04 LTS plus the persistent `sysctl` in section 7 | `DEC-22` (2026-09-11), kept by `DEC-26` (a) |
| Server type | Scaleway POP2-32C-128G: 32 dedicated vCPU (AMD EPYC 7543), 128 GiB RAM, x86-64, Block Storage only | `DEC-26` (2026-09-14) |
| Disks | Three Block Storage volumes: boot 40 GB 5K, source 310 GB 5K, work 260 GB 15K (sections 6 and 7) | `DEC-26` |
| Budget and stopping rule | 10 hours of billed resource existence, hour-8 rule, no retry after an out-of-memory kill, section 4 | `DEC-25` (2)–(3), kept by `DEC-26` (b) and (d) |
| Repository access | `ahmetxa/android_device_xiaomi_ishtar` and `ahmetxa/android_local_manifests` are public; the server holds no GitHub credential | `DEC-25` |
| Base manifest | `AOSPA/manifest` `beryl` at `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` | `F7.1-07` |
| Local manifest | `ahmetxa/android_local_manifests` `main` at `22283d8a866d042e02336fcb4698253ac6bf9c3b` (section 8) | `F7.1-03` … `F7.1-09` |
| Build command | `./rom-build.sh ishtar -z`: default build type `userdebug` (thin kernel LTO); `-z` also writes the fastboot image package | `AOSPA/android_vendor_aospa` `beryl` `build.sh` lines 19, 47, 74, 277–294 |

## 2. Sizing floor

| Requirement | Published figure | Source | POP2-16C-64G (handover) | POP2-32C-128G (chosen) |
|---|---|---|---|---|
| CPU | "A 64-bit x86 system" | [AOSP hardware requirements](https://source.android.com/docs/setup/start/requirements) | 16 vCPU AMD EPYC, x86-64 | 32 vCPU AMD EPYC 7543, x86-64 |
| Memory | "A minimum of 64 GB of RAM" | same | 64 GB: exactly the minimum, no margin | 128 GiB |
| Disk | "At least 400 GB of free disk space to check out and build the code (250 GB to check out + 150 GB to build)" | same | 610 GB in three volumes | 610 GB in three volumes: 350 GB for the checkout side, 260 GB for `out` |
| OS | "any 64-bit Linux distribution with GNU C Library (glibc) 2.17 or later"; "To build Android 11 or higher, you must use Ubuntu 18.04 or later" | same | — | Ubuntu 22.04 |
| OS, AOSPA | "Google recommends using Ubuntu" and points to Google's setup instructions | `AOSPA/manifest` `beryl` `README.md` lines 5–8 | — | — |

The handover's POP2-16C-64G meets the memory floor with no margin, and its 16
vCPU would roughly halve the CCX53's compile throughput. `DEC-26` therefore
moved to POP2-32C-128G, which has the CCX53's core count and memory and keeps
`DEC-25`'s 10-hour ceiling. Volumes are sold in decimal GB: 310 GB shows as
about 288 GiB on the server.

**Ubuntu 24.04 caveat.** Ubuntu 23.10 and later restrict unprivileged user
namespaces through AppArmor, which breaks AOSP's `nsjail` build sandbox
([Launchpad bug 2063976](https://bugs.launchpad.net/ubuntu/+source/apparmor/+bug/2063976)).
22.04 does not carry that restriction.

## 3. Provider billing and deletion semantics (`AUDIT-FIX-43`)

Read 2026-09-14 from Scaleway's own pages: [Instances FAQ](https://www.scaleway.com/en/docs/instances/faq/),
[power off an Instance](https://www.scaleway.com/en/docs/instances/how-to/power-off-instance/),
[delete an Instance](https://www.scaleway.com/en/docs/instances/how-to/delete-instance/),
[Instances concepts](https://www.scaleway.com/en/docs/instances/concepts/),
[Block Storage FAQ](https://www.scaleway.com/en/docs/block-storage/faq/),
[delete a Block Storage volume](https://www.scaleway.com/en/docs/block-storage/how-to/delete-a-volume/),
[Block Storage concepts](https://www.scaleway.com/en/docs/block-storage/concepts/),
[flexible IPs](https://www.scaleway.com/en/docs/instances/how-to/use-flexips/),
[Organization quotas](https://www.scaleway.com/en/docs/organizations-and-projects/additional-content/organization-quotas/),
[SSH keys](https://www.scaleway.com/en/docs/organizations-and-projects/how-to/create-ssh-key/),
the [Instances datasheet](https://www.scaleway.com/en/docs/instances/reference-content/instances-datasheet/),
and the Instance API description of `terminate` in Scaleway's generated SDK
([`instance_sdk.go`](https://github.com/scaleway/scaleway-sdk-go/blob/master/api/instance/v1/instance_sdk.go)).
The 2026-09-14 handover's claims were treated as unverified.

- **Product and unit.** "Instances are billed on a pay-as-you-go basis, and
  their prices are made up of three parts: Instance price, Storage price
  (local or block), Flexible IP price." "CPU Instances: Billed per hour of
  uptime (including startup and standby time)." No page read says whether a
  started hour is billed whole, so the budget counts **every started hour as a
  full hour**. No monthly cap is stated.
- **Powered off still bills.** "When a server is powered off, only its volumes
  and any reserved flexible IP address are billed." "other resources—such as
  public IP addresses and storage volumes—are billed for their entire
  allocation period, regardless of whether the Instance is powered off." "The
  standby mode is charged as a running Instance." **Powering off is not
  teardown; the volumes and the flexible IP keep billing until deleted.**
- **Block volumes.** "You are billed by the hour based on the size of the
  volume and not the data that is actually stored on it." Block volumes "are
  persistent which means that they can live without being attached to an
  Instance." Tiers: `sbs_5k` "Block 5K" at 5,000 IOPS and `sbs_15k` "Block 15K"
  at 15,000 IOPS, both "5 GB to 15 TB". POP2-32C-128G has storage "Block" only
  (datasheet), so its boot volume is a Block volume too. "You must detach your
  volume from the Instance it is attached to before deleting the volume."
- **Deleting the Instance does not reliably delete its volumes.** Console:
  "If your Instance has associated IPs or Block Storage volumes, you will be
  asked whether you want to delete them as well. Check the corresponding box to
  delete them along with your Instance." API, per the Block Storage FAQ: "When
  deleting an Instance via the API, all the attached volumes (local and Block
  Storage) are deleted." The Instance API's own text disagrees: "The
  `terminate` action will result in the deletion of `l_ssd` and `scratch`
  volumes types, `sbs_volume` volumes will only be detached." **The pages
  disagree, so teardown assumes the worse case: every Block volume survives the
  Instance and is deleted by name and confirmed gone (section 12).** This
  runbook uses the Console only.
- **Flexible IPv4.** "Each Instance's flexible IPv4 costs €0.004/hour, excl.
  VAT." "When you create a Scaleway Instance, by default, its public IP address
  is also a flexible IP address." It outlives the Instance: "Terminate: Your
  Instance and its volumes are permanently deleted, but the attached flexible
  IP is preserved." Deletion is its own step: "When you no longer want one of
  your existing flexible IP addresses, you can delete it from your account."
  **Teardown deletes it explicitly.**
- **Snapshots.** "the snapshot exists as an independent, billed resource and is
  not deleted when its source volume, Instance, or image is deleted." This
  runbook creates no snapshot or image; teardown confirms there are none.
- **Quotas and keys.** On the quota page, POP2-32C-128G reads "To use this
  product, you must validate your identity." Once identity is validated its
  quota is 1. "Block Storage total size in GB" is 500 with only a validated
  payment method and 5 000 with identity validated, so the 610 GB here also
  needs a validated identity. "SSH keys are scoped at a Project level. Ensure
  you add an SSH key to each Project you want to use it in."
- **OS image.** The [images page](https://www.scaleway.com/en/docs/instances/reference-content/images-and-instantapps/)
  features Ubuntu 24.04 and does not say whether 22.04 is still offered, so
  section 6 checks the Console and applies `DEC-22`'s fallback if it is not.
- **Prices (Scaleway pricing pages, "Prices before tax"; confirm in the Console
  at creation).** POP2-32C-128G €1.18 per hour ([virtual instances](https://www.scaleway.com/en/pricing/virtual-instances/));
  Block Storage 5K €0.000130 and 15K €0.000177 per GB per hour, snapshots
  €0.000049 per GB per hour ([storage](https://www.scaleway.com/en/pricing/storage/));
  flexible IPv4 €0.004 per hour (Instances FAQ). With 350 GB of 5K and 260 GB of
  15K, that is about €1.28 per hour for everything together.

## 4. Budget and stopping rule (`DEC-25`, as amended by `DEC-26`)

- **Clock.** Starts when the Console shows the Instance and its volumes
  created; ends when the last of the Instance, its three Block volumes and its
  flexible IP is deleted (section 12). Every started hour counts as a full hour
  (section 3).
- **Ceiling.** 10 hours, about €12.8 plus VAT at the section 3 prices
  (`DEC-26` (b): POP2-32C-128G has the CCX53's 32 vCPU, so `DEC-25`'s ceiling
  and hour rule stand).
- **Sync failure** (`repo sync`, or barista's "Unexpected exit status from the
  brewing process" in the build log): stop. Retrieve the evidence in section
  10, then tear down. **Exception (`AUDIT-FIX-52`):** a sync failure that
  matches a sync-path detector in the table below — the shallow sync of a
  `vendor/xiaomi/*` blob repository, or `vendor/xiaomi/camera` — gets that
  row's fix attempt, counted against the same 2 attempts as a build failure.
- **Build failure:** classify it. Only a manifest-class error — a deferred
  item's detector in the table below, a missing project, or a wrong branch or
  commit — gets a fix attempt, and at most **2** attempts in the session. Any
  other error class: stop, retrieve and tear down; the error becomes a
  replanning input.
- **Out-of-memory kill (`DEC-26` (d)):** not manifest-class and not retried.
  Stop, retrieve and tear down; record it as a replanning input.
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
base="$("$GH" api repos/AOSPA/manifest/commits/beryl --jq .sha)"
if [ "$base" != 7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2 ]; then
  echo "AOSPA/manifest beryl moved past the pin ($base): stop, do not rent (AUDIT-FIX-53)"
  exit 1
fi
echo "pre-rental checks passed"
```

Then, by hand:

1. Scaleway Console, Organization quotas: identity is validated, the
   POP2-32C-128G quota is at least 1, and "Block Storage total size in GB"
   allows the 610 GB of section 6 (section 3). If not, validate identity or
   contact Support and wait; do not rent another type or smaller volumes
   silently.
2. Console, the Project the Instance will be created in, SSH keys: your
   **public** ed25519 key is present **in that Project** (keys are
   Project-scoped, section 3).
3. The output directory `~/Documents/Projeler/ishtar-builds/` exists **outside**
   any git repository. Build outputs carry proprietary vendor blobs and are never
   committed or published (`ARC-04`).
4. The session has the time: the 10 h ceiling fits before you stop for the day.

## 6. Provisioning (Scaleway Console)

- Project: the one holding your SSH key. Availability Zone: one listing
  POP2-32C-128G (the datasheet lists FR-PAR-1 to 3, NL-AMS-1 to 3, PL-WAW-1 to 3
  and IT-MIL-1). Every later Console step uses this Project and zone.
- Type: **POP2-32C-128G**. Image: **Ubuntu 22.04**. If the Console does not
  offer 22.04 for this type, choose **Ubuntu 24.04** (`DEC-22` fallback) and note
  it in the timeline; section 7 then applies the persistent `sysctl`.
- Storage: the system volume as **Block Storage 5K, 40 GB**. Add two Block
  Storage volumes: `ishtar-src`, **5K, 310 GB**, and `ishtar-out`, **15K,
  260 GB**. No snapshot, no image, no backup.
- Networking: keep the **public IPv4** (a flexible IP; it bills and is deleted
  in section 12). IPv6 as offered. No cloud-init, no placement group, no
  Private Network.
- SSH key: yours. Name: `ishtar-beryl-build`.
- Write down the creation time (UTC) for the timeline. From the Instance's
  storage view, note each additional volume's **ID and size** on paper or in
  your shell only; section 7 asks for them. Copy the address into your shell
  only:

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
  # 24.04 fallback only (section 2), written to sysctl.d so it survives a reboot
  echo 'kernel.apparmor_restrict_unprivileged_userns=0' > /etc/sysctl.d/60-aosp-nsjail.conf
  sysctl -p /etc/sysctl.d/60-aosp-nsjail.conf
  test "$(sysctl -n kernel.apparmor_restrict_unprivileged_userns)" = 0
fi
useradd -m -s /bin/bash builder
install -d -m 700 -o builder -g builder /home/builder/.ssh
install -m 600 -o builder -g builder /root/.ssh/authorized_keys /home/builder/.ssh/authorized_keys
df -h / | tail -n 1
nproc
free -g | head -n 2
```

Then the volumes and swap, still as root. Layout (`DEC-26`):

| Volume | Size, tier | Mount | Holds |
|---|---|---|---|
| Boot | 40 GB, 5K | `/` | OS, packages, `repo`, `~/logs`, `~/evidence`, the 16 GB `/swapfile` |
| `ishtar-src` | 310 GB, 5K | `/android` | `/android/beryl` (`.repo` and the checkout); `/android/pkg`, the retrieval staging behind `~/out-pkg` |
| `ishtar-out` | 260 GB, 15K | `/android/beryl/out` | The build output. Runbook paths stay `out/…`; no `OUT_DIR` is set |

Volumes are chosen by size, never by `/dev/sdX` or attachment order, and
cross-checked against the Console volume ID wherever the guest exposes it
(Scaleway's pages do not document how it appears). `mkfs` runs only where
`blkid` finds no filesystem.

```bash
set -euo pipefail
read -r -p 'ishtar-src volume ID (Console): ' SRC_ID
read -r -p 'ishtar-out volume ID (Console): ' OUT_ID
lsblk -o NAME,SIZE,TYPE,SERIAL,MOUNTPOINT
pick() { # $1 size in bytes: the one whole disk of that size (±1%) with no partition and no mount
  local want="$1" name size hit="" count=0
  while read -r name size; do
    [ "$size" -ge $((want * 99 / 100)) ] && [ "$size" -le $((want * 101 / 100)) ] || continue
    [ "$(lsblk -nro NAME "/dev/$name" | wc -l)" -eq 1 ] || continue
    [ -z "$(lsblk -nro MOUNTPOINT "/dev/$name" | tr -d '[:space:]')" ] || continue
    hit="/dev/$name"; count=$((count + 1))
  done < <(lsblk -dnbo NAME,SIZE,TYPE | awk '$3 == "disk" { print $1, $2 }')
  if [ "$count" -ne 1 ]; then echo "expected one free disk of $want bytes, found $count: stop" >&2; return 1; fi
  echo "$hit"
}
check_id() { # $1 device picked by size, $2 Console volume ID
  local id m l n d s p
  id="$(printf '%s' "$2" | tr -d '-' | tr 'A-Z' 'a-z')"
  m="$(
    for l in /dev/disk/by-id/*; do
      [ -e "$l" ] || continue
      n="$(basename "$l" | tr -d '-' | tr 'A-Z' 'a-z')"
      case "$n" in
        *"$id"*)
          d="$(readlink -f "$l")"
          p="$(lsblk -no PKNAME "$d" | head -n 1 | tr -d '[:space:]')"   # parent disk when the link names a partition
          echo "/dev/${p:-$(basename "$d")}" ;;
      esac
    done
    lsblk -dnro NAME,SERIAL | while read -r d s; do
      s="$(printf '%s' "${s:-}" | tr -d '-' | tr 'A-Z' 'a-z')"
      if [ "${#s}" -ge 8 ]; then case "$id" in *"$s"*) echo "/dev/$d" ;; esac; fi
    done
  )"
  m="$(printf '%s\n' "$m" | sed '/^$/d' | sort -u)"
  if [ -z "$m" ]; then
    echo "note: volume ID not visible in the guest; $1 chosen by size alone"
  elif [ "$m" = "$1" ]; then
    echo "volume ID matches $1"
  else
    echo "volume ID points at $(echo "$m" | tr '\n' ' ')but size picked $1: stop" >&2; return 1
  fi
}
fmt() { # $1 device, $2 label
  if [ -z "$(blkid -p -o value -s TYPE "$1" || true)" ]; then
    mkfs.ext4 -q -m 0 -L "$2" "$1"
  else
    echo "$1 already carries a filesystem: not formatted"
  fi
}
SRC_DEV="$(pick 310000000000)"
OUT_DEV="$(pick 260000000000)"
test "$SRC_DEV" != "$OUT_DEV"
check_id "$SRC_DEV" "$SRC_ID"
check_id "$OUT_DEV" "$OUT_ID"
fmt "$SRC_DEV" ishtar-src
fmt "$OUT_DEV" ishtar-out
SRC_UUID="$(blkid -s UUID -o value "$SRC_DEV")"; test -n "$SRC_UUID"
OUT_UUID="$(blkid -s UUID -o value "$OUT_DEV")"; test -n "$OUT_UUID"
grep -q "^UUID=$SRC_UUID " /etc/fstab || echo "UUID=$SRC_UUID /android ext4 defaults,noatime,nofail 0 2" >> /etc/fstab
grep -q "^UUID=$OUT_UUID " /etc/fstab || echo "UUID=$OUT_UUID /android/beryl/out ext4 defaults,noatime,nofail 0 2" >> /etc/fstab
systemctl daemon-reload
mkdir -p /android
mountpoint -q /android || mount /android
install -d -o builder -g builder /android/beryl /android/beryl/out /android/pkg
mountpoint -q /android/beryl/out || mount /android/beryl/out
chown builder:builder /android /android/beryl/out
ln -sfn /android/pkg /home/builder/out-pkg
chown -h builder:builder /home/builder/out-pkg
if ! swapon --show=NAME --noheadings | grep -qx /swapfile; then
  if [ ! -f /swapfile ]; then fallocate -l 16G /swapfile; chmod 600 /swapfile; mkswap /swapfile > /dev/null; fi
  swapon /swapfile
fi
grep -q '^/swapfile ' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
mountpoint /android
mountpoint /android/beryl/out
df -h / /android /android/beryl/out
free -g | head -n 3
```

`nofail` keeps a missing volume from blocking boot. Sections 8 and 9 refuse
to run unless the work volume is mounted, so the build can never fill
`/android` or `/` by writing into a bare `out` directory.

The build runs as `builder`, not root. Reconnect as `ssh "builder@$BUILD_HOST"`
and start `tmux new -s build`, so a dropped connection does not kill the sync
or the build.

```bash
set -euo pipefail
mkdir -p ~/.bin ~/evidence ~/logs
test -L ~/out-pkg && test -d ~/out-pkg/ && test -w ~/out-pkg/   # /android/pkg, off the boot volume
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
mountpoint -q /android/beryl/out || { echo "work volume not mounted at /android/beryl/out: stop (section 7)"; exit 1; }
cd /android/beryl
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
{
  echo "== after sync $(date -u +%FT%TZ)"
  du -sh .repo
  du -shx .   # the tree with .repo, without the out volume
  df -h / /android /android/beryl/out
} | tee -a ~/evidence/disk.txt
```

`repo` loads only the top-level `.repo/local_manifests/*.xml` files, so the
deliberately invalid `tests/known-bad-*.xml` cases in the clone are never read
as manifests.

## 9. Build

```bash
set -euo pipefail
export PATH="$HOME/.bin:$PATH"
stamp() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" >> ~/evidence/timeline.txt; }
mountpoint -q /android/beryl/out || { echo "work volume not mounted at /android/beryl/out: stop (section 7)"; exit 1; }
cd /android/beryl
stamp build-start
set +e
./rom-build.sh ishtar -z > ~/logs/build.log 2>&1
rc=$?
set -e
{
  echo "== after build (exit $rc) $(date -u +%FT%TZ)"
  du -sh --exclude=lost+found out
  df -h / /android /android/beryl/out
} | tee -a ~/evidence/disk.txt
if [ "$rc" -ne 0 ]; then
  stamp "build-failed"
  grep -m 5 -nE 'FAILED:|error:|ninja: build stopped|Unexpected exit status from the brewing process|Killed|[Oo]ut of memory' ~/logs/build.log || true
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

ccache stays off for this first build. AOSPA `beryl` uses it only when both
`USE_CCACHE` and `CCACHE_EXEC` are set (`AOSPA/android_build` `beryl`
`core/ccache.mk` lines 29–32), neither is exported here, and a cold cache does
not speed up a first build. A `Killed` or out-of-memory line in the log is the
section 4 out-of-memory class: stop, with no retry.

## 10. Evidence (before teardown, whatever the outcome)

Collect what exists; a missing file is recorded, not fatal, so a failed build
still leaves evidence.

```bash
set -euo pipefail
export PATH="$HOME/.bin:$PATH"
cd /android/beryl
E=~/evidence
OUT=out/target/product/ishtar
if repo manifest -r -o "$E/manifest-resolved.xml" 2> "$E/manifest-resolved.err"; then
  if grep -nE '://[^/" ]+@' "$E/manifest-resolved.xml"; then
    echo "credential-shaped URL in the resolved manifest: do not copy it"; exit 1
  fi
else
  rm -f "$E/manifest-resolved.xml"
  echo "repo manifest -r failed: recorded in manifest-resolved.err, continuing"
fi
{
  echo "== consumed tree entry"
  grep -n 'aon_front.pb' device/xiaomi/ishtar/proprietary-files.txt || echo "aon_front.pb entry MISSING"
  echo "== built symlink (expected target /odm/lib64/camera/aon_front.pb)"
  if [ -L "$OUT/vendor/lib64/camera/aon_front.pb" ]; then
    echo "symlink -> $(readlink "$OUT/vendor/lib64/camera/aon_front.pb")"
  else
    echo "vendor/lib64/camera/aon_front.pb is NOT a symlink or does not exist"
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

**Where the symlink is built.** The entry
`odm/lib64/camera/aon_front.pb;SYMLINK=vendor/lib64/camera/aon_front.pb`
(`refs/a16_ishtar/proprietary-files.txt:1037`) installs the regular file at
`$OUT/odm/lib64/camera/aon_front.pb`. AOSPA extract-utils' `install_symlink`
module creates the symlink at `$OUT/vendor/lib64/camera/aon_front.pb`, and its
expected `readlink` target is `/odm/lib64/camera/aon_front.pb`. Any other target
is a failure, not a pass.

**Operator rule for sections 10 and 11 (`AUDIT-FIX-54`).** Both blocks record a
missing file and continue. If either still exits non-zero, record the failing
line, run the remaining lines by hand, retrieve what exists, and never skip
teardown.

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
cd /android/beryl
OUT=out/target/product/ishtar
P=~/out-pkg   # symlink to /android/pkg on the source volume (section 7)
R="$P/retrieval.txt"
: > "$R"
# A missing artifact is recorded, not fatal (AUDIT-FIX-54). Expected: one aospa-*-image.zip, two aospa-*.zip.
for z in aospa-*.zip; do
  [ -f "$z" ] || continue
  if cp "$z" "$P/"; then echo "retrieved      $z" >> "$R"; else echo "COPY FAILED    $z" >> "$R"; fi
done
[ "$(ls -1 "$P"/aospa-*-image.zip 2>/dev/null | wc -l)" -eq 1 ] || echo "NOT PRODUCED   aospa-*-image.zip (expected exactly 1)" >> "$R"
[ "$(ls -1 "$P"/aospa-*.zip 2>/dev/null | wc -l)" -eq 2 ] || echo "NOT PRODUCED   aospa-*.zip (expected exactly 2)" >> "$R"
for i in boot init_boot vendor_boot dtbo recovery vbmeta vbmeta_system; do
  if [ ! -f "$OUT/$i.img" ]; then
    echo "NOT PRODUCED   $i.img" >> "$R"
  elif cp "$OUT/$i.img" "$P/"; then
    echo "retrieved      $i.img" >> "$R"
  else
    echo "COPY FAILED    $i.img" >> "$R"
  fi
done
( cd "$P" && rm -f SHA256SUMS && sha256sum -- * > SHA256SUMS )
cat "$R"
du -sh "$P"
```

If the build failed, the same block records every package and image as
`NOT PRODUCED` and still writes `SHA256SUMS` over `evidence.tar.gz` and
`retrieval.txt`.

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
2. Scaleway Console, CPU & GPU Instances, the section 6 zone: **delete**
   `ishtar-beryl-build`. Not powered off, not standby: deleted. In the dialog,
   check the boxes to delete its IPs and Block Storage volumes too.
3. Console, Block Storage, Volumes, same zone: delete every volume still
   listed: the 40 GB system volume, `ishtar-src` and `ishtar-out`. The Instance
   API's `terminate` only detaches Block volumes (section 3), so assume they
   survived. `DEC-26` (c): nothing is kept, not even the source volume.
4. Console, CPU & GPU Instances, Flexible IPs tab: delete any flexible IP still
   listed. `terminate` preserves it, and it bills until deleted.
5. Console, Block Storage, Snapshots tab, and Instances, Images: none exist.
   None were created; a snapshot would bill on its own.
6. Billing stopped: in the Project and zone, the Console lists **zero
   Instances, zero volumes, zero flexible IPs and zero snapshots**. Write down
   the time (UTC) of the last deletion; elapsed = last deletion − creation,
   rounded up to whole hours and compared against the 10 h ceiling.
7. Credentials: none were issued (`DEC-25`, public repositories). If that plan
   ever changes to a token, revoke it here.
8. On the host: `ssh-keygen -R "$BUILD_HOST"`, then `unset BUILD_HOST`.

## 13. What `Faz7.2` records in the ledger

One implementation row: stage-by-stage exit status and elapsed time from
`timeline.txt`; the error class and last lines of any failing log (not whole
logs); fix attempts used (of 2) with `fixes.diff`; the `AOSPA/manifest` base and
`22283d8a866d042e02336fcb4698253ac6bf9c3b`; the retrieved file names with their sha256; the section 10
evidence values; the `disk.txt` sizes of `.repo`, the tree and `out`; the
Ubuntu release used; the last deletion time and total elapsed hours against
the ceiling, with the four zero counts of section 12.
