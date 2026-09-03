#!/usr/bin/env bash
# Build PixelModeProbe into a bare classes.dex and push it to the device.
#
# This is NOT an APK. It is a dex run through app_process, the standard Android
# shell-tool mechanism. It therefore needs NO aapt2, apksigner, zipalign or
# gradle -- only a JDK, an android.jar to compile against, and d8 (inside r8.jar).
#
# Host toolchain, downloaded 2026-09-03 into C:/Users/ahmet/android-tools:
#   platform-35_r02.zip -> android-35/android.jar   (64.3 MB, API 35 = device)
#   r8-8.13.23.jar                                  (18.3 MB, provides d8)
#
# It runs as the shell user, which holds android.permission.CAMERA
# (granted=true, SYSTEM_FIXED).

set -eu

TOOLS="${TOOLS:-C:/Users/ahmet/android-tools}"
ANDROID_JAR="$TOOLS/android-35/android.jar"
R8_JAR="$TOOLS/r8-8.13.23.jar"
ADB="${ADB:-/c/platform-tools/adb.exe}"
HERE="$(cd "$(dirname "$0")" && pwd)"

cd "$HERE"
rm -rf classes dex
mkdir -p classes dex

echo "== javac =="
javac -bootclasspath "$ANDROID_JAR" -source 8 -target 8 \
      -d classes PixelModeProbe.java 2>&1 | grep -v '^Note:' || true

echo "== d8 =="
java -cp "$R8_JAR" com.android.tools.r8.D8 \
     --lib "$ANDROID_JAR" --min-api 35 --output dex classes/*.class

ls -l dex/classes.dex

echo "== push =="
MSYS_NO_PATHCONV=1 "$ADB" push dex/classes.dex /data/local/tmp/pixelmodeprobe.dex

echo "== ready =="
echo "run: MSYS_NO_PATHCONV=1 $ADB shell \"CLASSPATH=/data/local/tmp/pixelmodeprobe.dex app_process / PixelModeProbe\""
