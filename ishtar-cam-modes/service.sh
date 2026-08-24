#!/system/bin/sh
# QS kutucuk uygulamasini kurar/gunceller ve baslatici gorunurlugunu ayarlar.
#
# Isin TAMAMI action.sh'de: kurulum kurali, kutucuk sirasi ve baslatici
# gorunurlugu tek yerde dursun diye. Bu dosya yalnizca dogru ANI secer
# (paket yoneticisi hazir olduktan sonra) ve sonucu gunluge yazar.
#
# Baslatici takma adi neden var:
#   KernelSU'nun Superuser listesi baslatici etkinligi OLMAYAN uygulamalari
#   gizliyor; oyle bir uygulamaya kok yetkisi verilemiyor. Yetki bir kez
#   verildikten sonra (UID'ye baglidir, kalicidir) takma ad KENDILIGINDEN
#   kapanir ve uygulama cekmecede gorunmez olur.
#
#   Elle mudahale gerekirse:
#     su -c sh /data/adb/modules/ishtar_cam_modes/action.sh tiles show
#     su -c sh /data/adb/modules/ishtar_cam_modes/action.sh tiles hide
#   ('show' bilerek gorunur demektir; otomatik gizleme artik devreye girmez.)

MODDIR=${0%/*}
TAG=ishtar_cam_modes

[ -f "$MODDIR/tile-app.apk" ] || exit 0

# Paket yoneticisi hazir olana kadar bekle
i=0
while [ "$(getprop sys.boot_completed)" != "1" ] && [ $i -lt 120 ]; do
  sleep 2
  i=$((i + 1))
done
sleep 5

OUT=$(sh "$MODDIR/action.sh" tiles install 2>&1)
if [ $? -eq 0 ]; then
  log -t $TAG "kutucuk uygulamasi: $OUT"
else
  log -t $TAG "kutucuk uygulamasi kurulamadi: $OUT"
  exit 0
fi

case "$OUT" in
  kuruldu*)
    log -t $TAG "4 kutucuk Hizli Ayarlar'a eklendi (50MP DCG LN4 LN2)"
    log -t $TAG "KOK YETKISI GEREKLI: KernelSU > Superuser > IMX989 Camera Modes" ;;
esac
