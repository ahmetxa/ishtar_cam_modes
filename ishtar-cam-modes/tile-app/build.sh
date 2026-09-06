#!/usr/bin/env bash
# IMX989 kamera modu QS kutucuk uygulamasini derler ve imzalar.
#
#   ./build.sh <SDK_KOKU>
#
# SDK_KOKU su duzeni bekler (elle indirilebilir, Android Studio gerekmez):
#   <kok>/bt/android-14/aapt2.exe            build-tools_r34-windows.zip
#   <kok>/bt/android-14/lib/{d8,apksigner}.jar
#   <kok>/pl/android-35/android.jar          platform-35_r02.zip
#   <kok>/jdk/jdk-*/bin/{javac,java,keytool} Temurin JDK 17
#
# Cikti: out/ishtar-cam-tiles.apk  (zipalign'li, v1+v2+v3 imzali)
set -euo pipefail

SDK=${1:?kullanim: build.sh <SDK_KOKU>}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT=$HERE/out
BT=$SDK/bt/android-14
JARS=$BT/lib
ANDROID_JAR=$SDK/pl/android-35/android.jar
JDK=$(echo "$SDK"/jdk/jdk-*)
JAVA=$JDK/bin/java
JAVAC=$JDK/bin/javac
KEYTOOL=$JDK/bin/keytool
KS=${KS:-$HERE/debug.keystore}
# Imza anahtari: yerel, kendinden imzali bir DEBUG anahtaridir; yoksa
# asagidaki 6. adimda uretilir. Parolasi bir sir DEGILDIR -- tipki
# Android'in kendi debug.keystore parolasi ("android") gibi acikca
# bilinir ve tek basina hicbir sey saglamaz, cunku anahtar dosyasinin
# kendisi surum arsivine girmez; bunu scripts/build-release.py'nin A1
# iddiasi garanti eder. Anahtarlar rastgele uretildigi icin parolayi
# bilen biri bu anahtari yeniden uretemez.
# Gercek bir anahtarla imzalamak icin disaridan verin:
#   KS=/yol/release.jks KS_PASS=... KS_ALIAS=... ./build.sh <SDK_KOKU>
# UYARI: farkli bir anahtarla derlenen APK, kurulu kopyanin uzerine
# guncelleme olarak GECMEZ (imza uyusmazligi).
KS_PASS=${KS_PASS:-ishtar}
KS_ALIAS=${KS_ALIAS:-ishtar}
PKG=ishtar-cam-tiles

for f in "$BT/aapt2.exe" "$BT/zipalign.exe" "$JARS/d8.jar" "$JARS/apksigner.jar" \
         "$ANDROID_JAR" "$JAVAC" "$JAVA" "$KEYTOOL"; do
  [ -e "$f" ] || { echo "eksik: $f" >&2; exit 1; }
done

# Windows ikilileri MSYS yollarini (/c/...) anlamiyor -> C:/... bicimi.
w() { cygpath -m "$1"; }

rm -rf "$OUT"; mkdir -p "$OUT/gen" "$OUT/classes" "$OUT/dex"

echo "[1/6] kaynaklar derleniyor (aapt2 compile)"
"$BT/aapt2.exe" compile --dir "$(w "$HERE/res")" -o "$(w "$OUT/res.zip")"

echo "[2/6] paket baglaniyor (aapt2 link)"
"$BT/aapt2.exe" link \
  -o "$(w "$OUT/base.apk")" \
  -I "$(w "$ANDROID_JAR")" \
  --manifest "$(w "$HERE/AndroidManifest.xml")" \
  --java "$(w "$OUT/gen")" \
  --min-sdk-version 26 --target-sdk-version 35 \
  "$(w "$OUT/res.zip")"

echo "[3/6] java derleniyor"
: > "$OUT/sources.txt"
find "$HERE/java" "$OUT/gen" -name '*.java' -print0 |
  while IFS= read -r -d '' f; do w "$f" >> "$OUT/sources.txt"; done
"$JAVAC" -encoding UTF-8 -source 8 -target 8 -nowarn \
  -bootclasspath "$(w "$ANDROID_JAR")" \
  -d "$(w "$OUT/classes")" "@$(w "$OUT/sources.txt")"

echo "[4/6] dex uretiliyor (d8)"
: > "$OUT/classes.txt"
find "$OUT/classes" -name '*.class' -print0 |
  while IFS= read -r -d '' f; do w "$f" >> "$OUT/classes.txt"; done
"$JAVA" -cp "$(w "$JARS/d8.jar")" com.android.tools.r8.D8 \
  --lib "$(w "$ANDROID_JAR")" --min-api 26 --release \
  --output "$(w "$OUT/dex")" "@$(w "$OUT/classes.txt")"

echo "[5/6] apk paketleniyor + zipalign"
cp "$OUT/base.apk" "$OUT/unsigned.apk"
python - "$(w "$OUT/unsigned.apk")" "$(w "$OUT/dex/classes.dex")" <<'PY'
import sys, zipfile, shutil, os
apk, dex = sys.argv[1], sys.argv[2]
tmp = apk + '.tmp'
with zipfile.ZipFile(apk) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        if it.filename == 'classes.dex':
            continue
        zout.writestr(it, zin.read(it.filename))
    zout.write(dex, 'classes.dex')
shutil.move(tmp, apk)
print('   classes.dex eklendi (%d bayt)' % os.path.getsize(dex))
PY
"$BT/zipalign.exe" -p -f 4 "$(w "$OUT/unsigned.apk")" "$(w "$OUT/aligned.apk")"

echo "[6/6] imzalaniyor"
if [ ! -f "$KS" ]; then
  echo "   imza anahtari uretiliyor (bir kez)"
  "$KEYTOOL" -genkeypair -v -keystore "$(w "$KS")" \
    -storepass "$KS_PASS" -keypass "$KS_PASS" -alias "$KS_ALIAS" \
    -keyalg RSA -keysize 2048 -validity 10950 \
    -dname "CN=ishtar cam modes, OU=module, O=local, C=TR" > /dev/null
fi
"$JAVA" -cp "$(w "$JARS/apksigner.jar")" com.android.apksigner.ApkSignerTool sign \
  --ks "$(w "$KS")" --ks-pass "pass:$KS_PASS" --key-pass "pass:$KS_PASS" --ks-key-alias "$KS_ALIAS" \
  --v1-signing-enabled true --v2-signing-enabled true --v3-signing-enabled true \
  --out "$(w "$OUT/$PKG.apk")" "$(w "$OUT/aligned.apk")"

"$JAVA" -cp "$(w "$JARS/apksigner.jar")" com.android.apksigner.ApkSignerTool verify \
  --print-certs "$(w "$OUT/$PKG.apk")" | head -3

rm -f "$OUT/unsigned.apk" "$OUT/aligned.apk" "$OUT/base.apk" "$OUT/res.zip" \
      "$OUT/sources.txt" "$OUT/classes.txt"
echo
echo "hazir: $OUT/$PKG.apk  ($(stat -c %s "$OUT/$PKG.apk") bayt)"
