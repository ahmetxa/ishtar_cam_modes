#!/system/bin/sh
MODDIR=${0%/*}
TAG=ishtar_cam_modes
BIN=com.qti.sensormodule.ishtar_semco_imx989_wide.bin
TGT=/odm/lib64/camera/$BIN
ACT=$MODDIR/active/$BIN

EXPECT_MD5=9e4d0fe1a8bf2eb4146c9917a0ac2c4c
EXPECT_SIZE=1062250

# 50MP HAL katmani (hal_seed / hal_set / hal_state)
[ -f "$MODDIR/halpatch.sh" ] && . "$MODDIR/halpatch.sh"

MODE=$(cat "$MODDIR/mode" 2>/dev/null)
case "$MODE" in
  50mp)
    # 50MP HAL katmanindadir; sensor katmani stok kalir (birbirini dislarlar)
    SENSOR_MODE=stock
    HAL_WANT=fullres ;;
  stock|ln2|ln4|ln2s|ln4s|ln2f|ln4f|dcgA|dcgB)
    SENSOR_MODE=$MODE
    HAL_WANT=stock ;;
  *)
    MODE=stock
    SENSOR_MODE=stock
    HAL_WANT=stock ;;
esac
log -t $TAG "basliyor, mod=$MODE (sensor=$SENSOR_MODE hal=$HAL_WANT)"

if [ ! -f "$TGT" ]; then
  log -t $TAG "DURDU: hedef yok: $TGT"
  exit 0
fi

# --- Guvenlik kilidi: /odm surucusu yamalarin uretildigi surumle ayni mi? ---
# OTA sonrasi surucu degisirse yamalar yanlis kayitlara denk gelir; o durumda
# hicbir sey mount etmeyip stok davranisi korunur.
CUR=$(md5sum "$TGT" 2>/dev/null | cut -d' ' -f1)
if [ -z "$CUR" ]; then
  CUR_SIZE=$(stat -c %s "$TGT" 2>/dev/null)
  if [ "$CUR_SIZE" != "$EXPECT_SIZE" ]; then
    log -t $TAG "DURDU: surucu boyutu farkli ($CUR_SIZE != $EXPECT_SIZE)"
    exit 0
  fi
  log -t $TAG "UYARI: md5sum yok, yalnizca boyut dogrulandi"
elif [ "$CUR" != "$EXPECT_MD5" ]; then
  log -t $TAG "DURDU: /odm surucusu beklenenden farkli"
  log -t $TAG "       bulunan=$CUR beklenen=$EXPECT_MD5"
  log -t $TAG "       muhtemelen OTA geldi; modulun yeniden uretilmesi gerek"
  exit 0
fi

SRC=$MODDIR/blobs/$SENSOR_MODE.bin
if [ ! -f "$SRC" ]; then
  log -t $TAG "DURDU: blob yok: $SRC"
  exit 0
fi
if [ "$(stat -c %s "$SRC")" != "$EXPECT_SIZE" ]; then
  log -t $TAG "DURDU: blob boyutu bozuk: $SRC"
  exit 0
fi

# Tek bir "aktif" dosya tutulur ve o bind mount edilir. Mod degistirmek =
# ayni inode'un icerigini degistirmek; mount'a hic dokunulmaz.
mkdir -p "$MODDIR/active" || { log -t $TAG "HATA: active olusturulamadi"; exit 0; }
cat "$SRC" > "$ACT" || { log -t $TAG "HATA: blob kopyalanamadi"; exit 0; }

chown 0:0 "$ACT" 2>/dev/null
chmod 0644 "$ACT" 2>/dev/null
chcon u:object_r:vendor_file:s0 "$ACT" 2>/dev/null

if mount --bind "$ACT" "$TGT"; then
  log -t $TAG "OK: sensor mod=$SENSOR_MODE bind mount kuruldu -> $TGT"
else
  log -t $TAG "HATA: sensor bind mount basarisiz"
fi

# ---------------------------------------------------------------------------
# 50MP HAL katmani
#
# camera.qcom.so'nun tamami pakete konmaz; cihazdaki STOK ikili active_hal/
# altina kopyalanir ve 16 noktasi yamalanir (blobs/hal-fullres.patch).
# Kopya HER ZAMAN bind mount edilir -- 50MP kapaliyken icerigi stokla birebir
# aynidir (md5 esit), yani davranis degismez. Boylece mod degistirmek
# mount'a dokunmadan, yalnizca 16x4 bayt yazarak yapilir; sensor katmaninda
# kanitlanmis desenin aynisi.
# ---------------------------------------------------------------------------
if ! command -v hal_seed >/dev/null 2>&1; then
  log -t $TAG "HAL katmani yok (halpatch.sh bulunamadi) -- 50MP devre disi"
  exit 0
fi
if [ ! -f "$HAL_PATCH" ]; then
  log -t $TAG "HAL yama listesi yok -- 50MP devre disi"
  exit 0
fi
if [ ! -f "$HAL_TGT" ]; then
  log -t $TAG "HAL hedefi yok: $HAL_TGT -- 50MP devre disi"
  exit 0
fi

HCUR=$(hal_md5 "$HAL_TGT")
if [ "$HCUR" != "$HAL_STOCK_MD5" ]; then
  log -t $TAG "DURDU(HAL): /odm HAL'i beklenenden farkli"
  log -t $TAG "            bulunan=$HCUR beklenen=$HAL_STOCK_MD5"
  log -t $TAG "            muhtemelen OTA geldi; yama listesi yenilenmeli"
  exit 0
fi

# Kopya yoksa ya da bozuksa stoktan yeniden uret (ilk acilista ~27 MB)
HS=$(hal_state)
if [ "$HS" = none ] || [ "$HS" = unknown ]; then
  if hal_seed; then
    log -t $TAG "HAL kopyasi stoktan uretildi"
  else
    log -t $TAG "HATA: HAL kopyasi uretilemedi -- 50MP devre disi"
    exit 0
  fi
fi

if hal_set "$HAL_WANT"; then
  log -t $TAG "HAL katmani hazir: $(hal_state)"
else
  log -t $TAG "HATA: HAL katmani '$HAL_WANT' durumuna getirilemedi"
  exit 0
fi

if mount --bind "$HAL_ACT" "$HAL_TGT"; then
  log -t $TAG "OK: HAL bind mount kuruldu -> $HAL_TGT"
else
  log -t $TAG "HATA: HAL bind mount basarisiz"
fi
