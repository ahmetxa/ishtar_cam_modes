#!/system/bin/sh
# ishtar AON fix — dogrudan bind mount.
# KernelSU/Magisk overlay'ine guvenmez; kendi mount'unu kurar.
MODDIR=${0%/*}
SRC=/odm/lib64/camera/aon_front.pb
TGT=/vendor/lib64/camera
WORK=$MODDIR/.mnt
TAG=ishtar_aon_fix

log -t $TAG "basliyor"

if [ -e "$TGT/aon_front.pb" ]; then
  log -t $TAG "zaten mevcut, mudahale yok"
  exit 0
fi

if [ ! -f "$SRC" ]; then
  log -t $TAG "HATA: kaynak yok: $SRC"
  exit 0
fi

rm -rf "$WORK"
mkdir -p "$WORK" || { log -t $TAG "HATA: workdir olusturulamadi"; exit 0; }

# mevcut icerigi koru, sonra eksik dosyayi ekle
cp -a "$TGT"/. "$WORK"/ 2>/dev/null
cp -f "$SRC" "$WORK/aon_front.pb" || { log -t $TAG "HATA: kopyalama"; exit 0; }

chown 0:0 "$WORK" "$WORK"/* 2>/dev/null
chmod 0755 "$WORK" 2>/dev/null
chmod 0644 "$WORK"/* 2>/dev/null
chcon u:object_r:vendor_file:s0 "$WORK" 2>/dev/null
chcon u:object_r:vendor_file:s0 "$WORK"/* 2>/dev/null

if mount --bind "$WORK" "$TGT"; then
  log -t $TAG "OK: bind mount kuruldu -> $TGT"
  log -t $TAG "icerik: $(ls "$TGT" | tr '\n' ' ')"
else
  log -t $TAG "HATA: bind mount basarisiz"
fi
