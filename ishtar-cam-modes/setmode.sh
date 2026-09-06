#!/system/bin/sh
# ishtar IMX989 kamera modu secici
#   kullanim: setmode.sh [stock|50mp|ln2|ln4|ln2s|ln4s|ln2f|ln4f|dcgA|dcgB]
#   argumansiz calistirilirsa durum gosterir.
#
# IKI AYRI KATMAN VAR:
#   1) SENSOR katmani -- sensor surucu bin'i (12-bit / DCG / LN modlari)
#   2) HAL katmani    -- camera.qcom.so (50MP'yi standart listeye acar)
# '50mp' modu HAL katmanini acar ve sensor katmanini stock'a alir; diger
# modlar sensor katmanini yamalar ve HAL'i stok birakir. Yani birbirlerini
# DISLARLAR -- DCG acikken kuresel beyaz seviyesi 12-bit'e cekildigi halde
# sensor modu 0 (50MP) 10-bit kaldigi icin 50MP bozuk cikardi.

MODDIR=/data/adb/modules/ishtar_cam_modes
BIN=com.qti.sensormodule.ishtar_semco_imx989_wide.bin
TGT=/odm/lib64/camera/$BIN
ACT=$MODDIR/active/$BIN
EXPECT_SIZE=1062250

[ -d "$MODDIR" ] || { echo "HATA: modul bulunamadi: $MODDIR"; exit 1; }
[ "$(id -u)" = "0" ] || { echo "HATA: root gerekli (su -c sh $0 ...)"; exit 1; }

# 50MP HAL katmani (hal_set / hal_state / hal_seed / hal_umount_all)
[ -f "$MODDIR/halpatch.sh" ] && . "$MODDIR/halpatch.sh"

md5of() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }

mounted() {
  grep -q " /odm/lib64/camera/$BIN " /proc/1/mountinfo 2>/dev/null
}

# Kamera oturumu tutabilecek uygulamalar. Mod degisiminden ONCE kapatilirlar.
#   com.xiaomi.module.evaluation = 50MP cekebilen modlu OpenCamera
CAM_APPS="org.codeaurora.snapcam com.android.camera com.xiaomi.module.evaluation"

# Kamera yiginini GUVENLI sirayla yeniden baslatir.
#
# Onceki surum once provider'i, sonra cameraserver'i olduruyordu. Akis
# surerken HAL'i oldurmek QCOM kamera cekirdek surucusunun CSIPHY/CSID
# tahsislerini birakmamasina yol aciyor; sonuc: HER modda (stok dahil)
# siyah onizleme ve yalnizca yeniden baslatmayla duzelen kilitlenme.
# Dogru sira istemciden HAL'e dogrudur:
#   1) kamera uygulamalarini kapat  -> oturumlar duzgun sonlansin
#   2) cameraserver'i durdur        -> HAL'in istemcisi kalmasin
#   3) provider'i yeniden baslat    -> yeni surucuyu okusun
#   4) cameraserver'i geri baslat
restart_camera() {
  # 1) Once cameraserver: cerceve butun kamera oturumlarini kendisi kapatir.
  #    Uygulamalari BURADAN ONCE force-stop ETMEK yanlisti -- oturumu acikken
  #    SIGKILL yiyen istemci HAL tarafinda temizlenmeden provider da olunce
  #    cekirdek tahsisleri sizabiliyor.
  stop cameraserver 2>/dev/null
  wait_svc cameraserver stopped 8

  # 2) Provider'lar
  stop vendor.camera-provider 2>/dev/null
  stop vendor.camera-provider-2-7-ext 2>/dev/null
  wait_svc vendor.camera-provider stopped 8

  # 3) Artik hicbir oturum yok; uygulamalari kapat ki yeni surucuyle acilsinlar
  for pkg in $CAM_APPS; do
    am force-stop "$pkg" 2>/dev/null
  done

  # 3b) HAL katmani -- YALNIZCA BURADA guvenli.
  #     camera.qcom.so calisan bir surece mmap'li oldugu icin icerigini
  #     servisler ayaktayken degistirmek cokmeye yol acar. Servislerin
  #     tamami durmusken, baslamadan hemen once yaziyoruz.
  if [ -n "$HAL_WANT" ] && command -v hal_set >/dev/null 2>&1; then
    if hal_set "$HAL_WANT"; then
      echo "-> HAL katmani: $HAL_WANT"
    else
      echo "UYARI: HAL katmani '$HAL_WANT' durumuna getirilemedi"
      echo "       (stok HAL md5 uymuyor olabilir -- OTA sonrasi normaldir)"
    fi
  fi

  # 4) Geri baslat ve gercekten ayaga kalktigini dogrula
  start vendor.camera-provider 2>/dev/null
  start vendor.camera-provider-2-7-ext 2>/dev/null
  start cameraserver 2>/dev/null
  wait_svc vendor.camera-provider running 10
  wait_svc cameraserver running 10

  # Servisler "running" olur olmaz kamera KULLANILABILIR olmuyor: provider
  # butun sensorleri yeniden probe ediyor. Olculdu -- baslatmadan 2 sn sonra
  # acmak sessizce basarisiz oluyor, 4 sn ve sonrasi calisiyor. Once kamera
  # listesinin geri geldigini bekle, sonra guvenli pay birak.
  wait_camera_list 10
  sleep 5
}

# cameraserver kamera listesini yeniden yayinlayana kadar bekle.
# Servisler dururken dumpsys bos doner; hazir olunca cihaz sayisini basar.
wait_camera_list() {
  i=0
  n=$(( $1 * 4 ))
  while [ $i -lt $n ]; do
    c=$(dumpsys media.camera 2>/dev/null | grep -m1 "Number of camera devices:" | tr -dc '0-9')
    if [ -n "$c" ] && [ "$c" -ge 4 ] 2>/dev/null; then
      return 0
    fi
    sleep 0.25
    i=$((i + 1))
  done
  return 1
}

# wait_svc <servis> <running|stopped> <saniye>
wait_svc() {
  i=0
  n=$(( $3 * 4 ))
  while [ $i -lt $n ]; do
    st=$(getprop "init.svc.$1")
    if [ "$2" = running ]; then
      [ "$st" = running ] && return 0
    else
      [ "$st" != running ] && return 0
    fi
    sleep 0.25
    i=$((i + 1))
  done
  return 1
}

# Es zamanli mod degisimlerini engelle. 90 saniyeden eski kilit bayattir.
LOCKDIR=$MODDIR/.switching
lock_acquire() {
  i=0
  while [ $i -lt 60 ]; do
    if mkdir "$LOCKDIR" 2>/dev/null; then
      trap 'rmdir "$LOCKDIR" 2>/dev/null' EXIT
      return 0
    fi
    if [ -n "$(find "$LOCKDIR" -maxdepth 0 -mmin +1.5 2>/dev/null)" ]; then
      rmdir "$LOCKDIR" 2>/dev/null
      continue
    fi
    sleep 0.5
    i=$((i + 1))
  done
  return 1
}

status() {
  SAVED=$(cat "$MODDIR/mode" 2>/dev/null)
  LIVE=$(md5of "$TGT")
  echo "kayitli mod    : ${SAVED:-yok}"
  if mounted; then echo "bind mount     : AKTIF"; else echo "bind mount     : YOK (yeniden baslat gerekli)"; fi
  echo "kameranin gordugu dosya:"
  echo "  md5          : $LIVE"
  HIT=
  for m in stock ln2 ln4 ln2s ln4s ln2f ln4f dcgA dcgB; do
    B=$(md5of "$MODDIR/blobs/$m.bin")
    [ "$B" = "$LIVE" ] && HIT=$m
  done
  echo "  ==> SENSOR MODU: ${HIT:-BILINMIYOR}"
  echo
  if command -v hal_state >/dev/null 2>&1; then
    HS=$(hal_state)
    if hal_mounted; then HM=AKTIF; else HM="YOK (yeniden baslat gerekli)"; fi
    echo "HAL katmani (50MP):"
    echo "  bind mount   : $HM"
    echo "  kopya durumu : $HS"
    [ "$HS" = fullres ] && echo "  ==> 50MP ACIK" || echo "  ==> 50MP kapali"
    echo
  fi
  echo "mevcut bloblar :"
  for m in stock ln2 ln4 ln2s ln4s ln2f ln4f dcgA dcgB; do
    printf '  %-6s %s  %s bayt\n' "$m" "$(md5of "$MODDIR/blobs/$m.bin")" "$(stat -c %s "$MODDIR/blobs/$m.bin" 2>/dev/null)"
  done
}

MODE=$1
if [ -z "$MODE" ]; then status; exit 0; fi

# Mod -> (sensor blob, HAL durumu) esleme. 50mp ile digerleri birbirini disler.
case "$MODE" in
  50mp)
    SENSOR_MODE=stock
    HAL_WANT=fullres
    [ -f "$MODDIR/blobs/hal-fullres.patch" ] || {
      echo "HATA: HAL yama listesi yok: blobs/hal-fullres.patch"; exit 1; }
    ;;
  stock|ln2|ln4|ln2s|ln4s|ln2f|ln4f|dcgA|dcgB)
    SENSOR_MODE=$MODE
    HAL_WANT=stock
    ;;
  *)
    echo "HATA: gecersiz mod '$MODE'"
    echo "      (stock|50mp|ln2|ln4|ln2s|ln4s|ln2f|ln4f|dcgA|dcgB)"
    exit 1 ;;
esac

SRC=$MODDIR/blobs/$SENSOR_MODE.bin
[ -f "$SRC" ] || { echo "HATA: blob yok: $SRC"; exit 1; }
[ "$(stat -c %s "$SRC")" = "$EXPECT_SIZE" ] || { echo "HATA: blob boyutu bozuk"; exit 1; }

if ! lock_acquire; then
  echo "HATA: baska bir mod degisimi suruyor"
  exit 1
fi

echo "$MODE" > "$MODDIR/mode"

case "$MODE" in
  50mp)
    echo "50MP (FullRes). 8192x6144'u STANDART cozunurluk listesine ekler,"
    echo "     boylece ucuncu parti uygulamalar tam cozunurluk cekebilir."
    echo "     Olculdu: OpenCamera 8192x6144 (50,3 MP) cekiyor."
    echo "     AGC 12,58 MP'de sabit calisir: 8192x6144'un kare suresi"
    echo "     1/20 sn'yi astigi icin standart listede gorunmez."
    echo "     Video (1080p60 / 4K60) etkilenmiyor."
    echo "     DCG/LN ile birlikte KULLANILAMAZ; sensor modu stock'a alinir."
    ;;
  dcgB)
    echo "ONERILEN. 6 fotograf moduna 12-bit + DCG uygular."
    echo "     Stok deklansor hizini korur. Video/50MP icin stock'a donun."
    ;;
  dcgA)
    echo "NOT: dcgB'nin PLL ayari olmayan surumu. Karsilastirma icin."
    ;;
  ln4f|ln2f)
    echo "NOT: 14 fotograf moduna LN + 12-bit uygular. Kalite dcgB ile"
    echo "     ayni, ama pozu uzatir (ln4f 1/20, ln2f 1/17) -> hareket"
    echo "     bulanikligi riski. Video/50MP icin stock'a donun."
    ;;
  ln2s|ln4s)
    echo "NOT: 10-bit LN. Olculdu: kazanc yok, daha gurultulu. Onerilmez."
    ;;
  ln2|ln4)
    echo "UYARI: '$MODE' yalnizca sensor modu 1'i yamalar ve"
    echo "       overrideForceSensorMode=1 gerektirir; o ayar olmadan"
    echo "       fotograflar pembe bantlanir. Referans icin duruyor."
    ;;
esac

NEED_REBOOT=0
if ! mounted; then
  echo "UYARI: sensor bind mount henuz yok."
  NEED_REBOOT=1
fi
if [ "$HAL_WANT" = fullres ] && command -v hal_mounted >/dev/null 2>&1 && ! hal_mounted; then
  echo "UYARI: HAL bind mount henuz yok (50MP icin gerekli)."
  NEED_REBOOT=1
fi
if [ "$NEED_REBOOT" = 1 ]; then
  echo "       Mod kaydedildi ($MODE) ama etkin olmasi icin YENIDEN BASLAT."
  exit 0
fi

# Ayni inode'un icerigini degistiriyoruz; mount'a dokunulmuyor.
cat "$SRC" > "$ACT" || { echo "HATA: yazilamadi"; exit 1; }
chown 0:0 "$ACT" 2>/dev/null
chmod 0644 "$ACT" 2>/dev/null
chcon u:object_r:vendor_file:s0 "$ACT" 2>/dev/null
sync

NEW=$(md5of "$TGT")
WANT=$(md5of "$SRC")
if [ "$NEW" != "$WANT" ]; then
  echo "HATA: dogrulama basarisiz ($NEW != $WANT)"
  exit 1
fi

echo "-> sensor modu '$SENSOR_MODE' yazildi ve dogrulandi (md5 $NEW)"
echo "-> kamera yeniden baslatiliyor (uygulamalar kapatilacak)..."
restart_camera

# HAL katmani restart_camera icinde yazildi; sonucu dogrula.
if command -v hal_state >/dev/null 2>&1; then
  HS=$(hal_state)
  if [ "$HAL_WANT" = fullres ] && [ "$HS" != fullres ]; then
    echo "UYARI: 50MP istendi ama HAL katmani '$HS' durumunda."
  fi
  if [ "$HAL_WANT" = stock ] && [ "$HS" = fullres ]; then
    echo "UYARI: HAL hala yamali gorunuyor ('$HS')."
  fi
fi

echo "-> hazir (mod: $MODE). Kamera uygulamasini yeniden ac."
