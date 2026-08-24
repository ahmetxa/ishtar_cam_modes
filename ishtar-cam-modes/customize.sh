ui_print ""
ui_print "  ishtar IMX989 Camera Modes  v2.1"
ui_print "  --------------------------------"

DEV=$(getprop ro.product.device)
DEV2=$(getprop ro.product.vendor.device)
if [ "$DEV" != "ishtar" ] && [ "$DEV2" != "ishtar" ]; then
  ui_print "! Cihaz: $DEV / $DEV2"
  abort  "! Bu modul yalnizca ishtar (Xiaomi 13 Ultra) icindir."
fi

BIN=com.qti.sensormodule.ishtar_semco_imx989_wide.bin
TGT=/odm/lib64/camera/$BIN
EXPECT_MD5=9e4d0fe1a8bf2eb4146c9917a0ac2c4c

if [ ! -f "$TGT" ]; then
  abort "! Surucu bulunamadi: $TGT"
fi

CUR=$(md5sum "$TGT" 2>/dev/null | cut -d' ' -f1)
ui_print "- Cihazdaki surucu : $CUR"
ui_print "- Beklenen         : $EXPECT_MD5"
if [ "$CUR" != "$EXPECT_MD5" ]; then
  ui_print ""
  ui_print "! Cihazdaki surucu, yamalarin uretildigi surumden farkli."
  ui_print "! Muhtemelen OTA aldin. Blob'lar yeniden uretilmeli."
  abort  "! Guvenlik icin kurulum durduruldu."
fi

# HAL ikilisi: 50MP yamasi cihazdaki STOK camera.qcom.so uzerine uygulanir,
# bu yuzden surumu bilinen olmali. Farkliysa ABORT ETMEYIZ -- DCG/LN modlari
# sensor katmanindadir ve etkilenmez; yalnizca 50MP kullanilamaz.
#
# Modul zaten kuruluysa hedef yolda BIZIM yamali kopyamiz bagli olabilir;
# o durumda okunan md5 fullres'tir. Ikisi de gecerli sayilir.
HAL=/odm/lib64/hw/camera.qcom.so
HAL_STOCK=c3fa63a86ee3ecaf9fbf02005d35f6b5
HAL_FULLRES=fe0245a4720fb07b01d96deef47f5569
HAL_CUR=$(md5sum "$HAL" 2>/dev/null | cut -d' ' -f1)
case "$HAL_CUR" in
  "$HAL_STOCK")
    ui_print "- Kamera HAL      : stok surum (50MP kullanilabilir)" ;;
  "$HAL_FULLRES")
    ui_print "- Kamera HAL      : modulun yamali kopyasi bagli (50MP acik)" ;;
  *)
    ui_print ""
    ui_print "! Kamera HAL surumu taninmiyor: $HAL_CUR"
    ui_print "! 50MP modu DEVRE DISI kalacak; DCG/LN modlari calisir."
    ui_print "" ;;
esac

set_perm_recursive "$MODPATH" 0 0 0755 0644
set_perm "$MODPATH/action.sh"       0 0 0755
set_perm "$MODPATH/setmode.sh"      0 0 0755
set_perm "$MODPATH/service.sh"      0 0 0755
set_perm "$MODPATH/post-fs-data.sh" 0 0 0755
set_perm "$MODPATH/halpatch.sh"     0 0 0755

ui_print ""
ui_print "- Modlar : stock / 50mp / dcgA-B / ln2 / ln4 (+s/f cesitleri)"
ui_print "- Yontem : sensor surucusu ve kamera HAL'i icin tekil bind mount"
ui_print "- Baslangic modu: ilk kurulumda stock; guncellemede mevcut mod"
ui_print ""
ui_print "  50MP ile DCG/LN birbirini disler: biri acilinca digeri kapanir."
ui_print ""
ui_print "  Mod degistirme:"
ui_print "    su -c sh /data/adb/modules/ishtar_cam_modes/setmode.sh 50mp"
ui_print "  Durum:"
ui_print "    su -c sh /data/adb/modules/ishtar_cam_modes/setmode.sh"
ui_print ""
ui_print "  Hizli Ayarlar kutucuklari (50MP DCG LN4 LN2) ilk acilista"
ui_print "  kendiliginden kurulur. Kutucuklarin calismasi icin KernelSU >"
ui_print "  Superuser listesinden 'IMX989 Camera Modes' uygulamasina kok"
ui_print "  yetkisi verin. Uygulama cekmecede gorunur kalir; simgesine"
ui_print "  dokununca modul arayuzu acilir."
ui_print ""
ui_print "  Ilk kurulumdan sonra bir kez yeniden baslat."
ui_print ""
