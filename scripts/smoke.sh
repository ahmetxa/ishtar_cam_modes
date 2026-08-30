#!/usr/bin/env bash
# ishtar device smoke - read-only camera-modification state reporter.
#
# Faz 2.1. Prints the device's complete camera-modification state across the
# sensor, HAL, and application layers, in a stable diffable form, so that every
# later change can be bracketed by a before and after snapshot.
#
#   ./scripts/smoke.sh                 print a snapshot to stdout
#   ./scripts/smoke.sh -o NAME         also store it as snapshots/NAME.txt
#
# READ-ONLY BY DESIGN. This script runs around changes including failed ones,
# so it must never alter the state it observes. It issues no write, no mount,
# no umount, no service stop or start, no force-stop, no property set, and it
# pushes nothing to the device. Every device-side command is one of: cat, ls,
# md5sum, stat, basename, grep, sed, cut, sort, tr, wc, echo, printf, dumpsys,
# pm list/path. The per-command review is recorded in the Faz 2.1 ledger entry.
#
# It does NOT judge whether a state is correct. It reports; a human or a later
# checklist interprets. Comparison is done with diff, not by this script.
#
# The large camera service dump is filtered ON THE DEVICE. Only the matched
# lines cross the adb boundary; correlation happens here on the host.
#
# Output has two regions. Everything before BEGIN COMPARABLE varies between
# runs (timestamp, serial) and is excluded from comparison. The region between
# the markers is what diff should see, and two runs with no intervening change
# must produce it byte-identically.

set -u

HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=$(cd "$HERE/.." && pwd)
ADB="$ROOT/platform-tools/adb.exe"
[ -x "$ADB" ] || ADB=adb

MODDIR=/data/adb/modules/ishtar_cam_modes
AGC=org.codeaurora.snapcam
SNAPDIR="$ROOT/snapshots"

OUT_NAME=""
while [ $# -gt 0 ]; do
  case "$1" in
    -o|--out) OUT_NAME="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,27p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

sh_root() { "$ADB" shell "su -c '$1'" 2>/dev/null | tr -d '\r'; }

# --- layer 1 and 2: module, sensor, HAL --------------------------------------
# Constants are read out of the module installed on the device rather than
# duplicated here, so that a ROM update which forces the module to change a
# checksum cannot leave this script reporting a confidently wrong verdict.
probe_layers() {
  sh_root "
    M=$MODDIR
    HAL_TGT=/odm/lib64/hw/\$(grep -m1 '^HAL_BIN=' \$M/halpatch.sh | cut -d= -f2-)
    HAL_STOCK=\$(grep -m1 '^HAL_STOCK_MD5=' \$M/halpatch.sh | cut -d= -f2-)
    HAL_FULLRES=\$(grep -m1 '^HAL_FULLRES_MD5=' \$M/halpatch.sh | cut -d= -f2-)
    HAL_SIZE=\$(grep -m1 '^HAL_SIZE=' \$M/halpatch.sh | cut -d= -f2-)
    SBIN=\$(grep -m1 '^BIN=' \$M/setmode.sh | cut -d= -f2-)
    SEXPECT=\$(grep -m1 '^EXPECT_SIZE=' \$M/setmode.sh | cut -d= -f2-)
    STGT=/odm/lib64/camera/\$SBIN

    echo \"constants.source                = \$M (device-installed module)\"
    echo \"module.version                  = \$(grep -m1 '^version=' \$M/module.prop | cut -d= -f2-)\"
    echo \"module.versionCode              = \$(grep -m1 '^versionCode=' \$M/module.prop | cut -d= -f2-)\"
    echo \"mode.file                       = \$(cat \$M/mode 2>/dev/null)\"

    SLIVE=\$(md5sum \$STGT 2>/dev/null | cut -d\" \" -f1)
    SSIZE=\$(stat -c %s \$STGT 2>/dev/null)
    echo \"sensor.target                   = \$STGT\"
    echo \"sensor.live.md5                 = \$SLIVE\"
    echo \"sensor.live.size                = \$SSIZE / expected \$SEXPECT\"
    SVAR=unrecognized
    for b in \$M/blobs/*.bin; do
      [ \"\$(md5sum \$b 2>/dev/null | cut -d\" \" -f1)\" = \"\$SLIVE\" ] && { SVAR=\$(basename \$b .bin); break; }
    done
    echo \"sensor.live.variant             = \$SVAR\"
    echo \"sensor.mount.count              = \$(grep -c \" \$STGT \" /proc/1/mountinfo 2>/dev/null)\"

    HLIVE=\$(md5sum \$HAL_TGT 2>/dev/null | cut -d\" \" -f1)
    HSIZE=\$(stat -c %s \$HAL_TGT 2>/dev/null)
    echo \"hal.target                      = \$HAL_TGT\"
    echo \"hal.live.md5                    = \$HLIVE\"
    echo \"hal.live.size                   = \$HSIZE / expected \$HAL_SIZE\"
    if   [ \"\$HLIVE\" = \"\$HAL_FULLRES\" ]; then echo \"hal.state                       = fullres\"
    elif [ \"\$HLIVE\" = \"\$HAL_STOCK\" ];   then echo \"hal.state                       = stock\"
    elif [ -z \"\$HLIVE\" ];                then echo \"hal.state                       = none\"
    else                                       echo \"hal.state                       = unrecognized\"; fi
    # Stacked bind mounts matter: a single umount leaves the file still patched,
    # which already produced one false 'back to stock' reading in this project.
    echo \"hal.mount.count                 = \$(grep -c \" \$HAL_TGT \" /proc/1/mountinfo 2>/dev/null)\"
  "
}

# --- layer 3: application ----------------------------------------------------
probe_app() {
  sh_root "
    P=\$(pm path $AGC 2>/dev/null | sed \"s/package://\" | head -1)
    echo \"agc.package                     = $AGC\"
    if [ -n \"\$P\" ]; then echo \"agc.installed                   = yes\"; else echo \"agc.installed                   = no\"; fi
    echo \"agc.versionName                 = \$(dumpsys package $AGC 2>/dev/null | grep -m1 versionName | cut -d= -f2-)\"
    echo \"agc.versionCode                 = \$(dumpsys package $AGC 2>/dev/null | grep -m1 -oE \"versionCode=[0-9]+\" | cut -d= -f2)\"
    echo \"agc.apk.md5                     = \$(md5sum \$P 2>/dev/null | cut -d\" \" -f1)\"
    # Project-Ontology invariant 8: these keys break Gcam initialization
    # independently and already caused one misattributed failure. Report the
    # specific keys found, not a boolean, so Faz 3.1 knows which to clear.
    K=\$(grep -hoE \"pref_raw_key[a-z0-9_]*|pref_fix_resolution_key[a-z0-9_]*\" /data/data/$AGC/shared_prefs/*.xml 2>/dev/null | sort -u | tr \"\\n\" \" \")
    echo \"prefs.trap.count                = \$(echo \$K | wc -w)\"
    echo \"prefs.trap.keys                 = \$K\"
  "
}

# --- camera metadata ---------------------------------------------------------
# Every HAL camera device is summarised, not just one. Two reasons. First, the
# project's "camera 3" is ambiguous on this device: the service maps framework
# device 3 to HAL id 9, which is Front-facing with a 3264x2448 array, while the
# IMX989 rear array (4096x3072) sits on HAL id 0. Reporting all of them means
# the snapshot does not depend on resolving that question first. Second, a
# patch that changes the wrong camera is exactly the kind of mistake this
# script exists to catch, and it can only catch it by watching all of them.
# CAM_RAW is fetched once at top level, not inside a function. A function body
# that runs under command substitution executes in a subshell, so anything it
# assigns is discarded when that subshell exits.
fetch_cam_raw() {
  sh_root "dumpsys media.camera 2>/dev/null | grep -nE -A1 \"static information: ==|availableStreamConfigurations \(d000a\)|Facing:|android.sensor.info.(pixel|active)ArraySize\""
}

probe_cameras() {
  printf '%s\n' "$CAM_RAW" | awk '
    /static information: ==/ {
      split($0, a, "vendor_qti/"); split(a[2], b, " "); id = b[1]
      if (!(id in order)) { order[id] = ++n; ids[n] = id }
      next
    }
    /Facing:/            { split($0, f, "Facing:"); gsub(/^ +| +$/, "", f[2]); face[id] = f[2]; next }
    /availableStreamConfigurations/ {
      if (cnt[id] == "") { match($0, /int32\[[0-9]+\]/); cnt[id] = substr($0, RSTART + 6, RLENGTH - 7) }
      next
    }
    /pixelArraySize/     { want = "pix";  next }
    /activeArraySize/    { want = "act";  next }
    want != "" {
      line = $0
      sub(/^[0-9]+[-:][ ]*/, "", line); gsub(/^ +| +$/, "", line)
      gsub(/[][]/, "", line); gsub(/ +$/, "", line)
      if (want == "pix" && pix[id] == "") pix[id] = line
      if (want == "act" && act[id] == "") act[id] = line
      want = ""
    }
    END {
      for (i = 1; i <= n; i++) {
        k = ids[i]
        printf "camera.hal%-3s facing=%-5s streamcfg=%-5s pixelArray=[%s] activeArray=[%s]\n", \
               k, face[k], cnt[k], pix[k], act[k]
      }
    }' | sort
}

# Full stream-configuration rows for the IMX989 main rear camera. The selection
# rule is stated rather than assumed: the lowest HAL id whose Facing is Back.
# On this device that resolves to HAL 0. Every other camera is still covered by
# its entry count in the summary above, so a change elsewhere is not missed.
probe_main_rows() {
  local id="$1" start end
  echo "camera.hal${id}.stream_config.rows:"
  # Address the block by line number rather than by a sed range. A range whose
  # end pattern also matches its own start line closes immediately, which is
  # exactly what a generic "next static information header" pattern does here.
  start=$(printf '%s\n' "$CAM_RAW" | grep -E "^[0-9]+[-:].*vendor_qti/${id} \(v1\.1\) static information" | head -1 | sed 's/[-:].*//')
  end=$(printf '%s\n' "$CAM_RAW" | grep -E '^[0-9]+[-:].*static information: ==' | sed 's/[-:].*//' \
        | awk -v s="$start" '$1 > s {print $1; exit}')
  [ -n "$end" ] || end=999999
  sh_root "dumpsys media.camera 2>/dev/null | sed -n \"${start},${end}p\" | sed -n \"/availableStreamConfigurations (d000a)/,/^      android\./p\" | grep -E \"^ +\[[0-9]\"" \
    | sed 's/^ *//; s/^\[//; s/ *\]$//' | grep -vE '^$' | sort | sed 's/^/  /'
}

# --- assemble ----------------------------------------------------------------
SERIAL=$("$ADB" get-serialno 2>/dev/null | tr -d '\r')
CAM_RAW=$(fetch_cam_raw)
CAMS=$(probe_cameras)
MAIN=$(printf '%s\n' "$CAMS" | grep 'facing=Back' | head -1 | sed 's/^camera.hal//; s/ .*//')

BODY=$(
  probe_layers
  echo "camera.main.rule                = lowest HAL id with Facing: Back"
  echo "camera.main.hal_id              = $MAIN"
  printf '%s\n' "$CAMS"
  probe_main_rows "$MAIN"
  probe_app
)

emit() {
  printf '# ishtar device smoke\n'
  printf '# taken   : %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  printf '# serial  : %s\n' "$SERIAL"
  printf '# note    : lines above BEGIN COMPARABLE are excluded from diffs\n'
  printf -- '--- BEGIN COMPARABLE ---\n'
  printf '%s\n' "$BODY"
  printf -- '--- END COMPARABLE ---\n'
}

emit
if [ -n "$OUT_NAME" ]; then
  mkdir -p "$SNAPDIR"
  emit > "$SNAPDIR/$OUT_NAME.txt"
  echo "stored: snapshots/$OUT_NAME.txt" >&2
fi
