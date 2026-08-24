ui_print ""
ui_print "  ishtar AON front config fix  v1.1"
ui_print "  ---------------------------------"

DEV=$(getprop ro.product.device)
DEV2=$(getprop ro.product.vendor.device)
if [ "$DEV" != "ishtar" ] && [ "$DEV2" != "ishtar" ]; then
  ui_print "! Cihaz: $DEV / $DEV2"
  abort  "! Bu modul yalnizca ishtar (Xiaomi 13 Ultra) icindir."
fi

SRC=/odm/lib64/camera/aon_front.pb
if [ ! -f "$SRC" ]; then
  abort "! Kaynak bulunamadi: $SRC"
fi

if [ -e /vendor/lib64/camera/aon_front.pb ]; then
  ui_print "- NOT: hedef zaten var; ROM duzeltmeyi icermis olabilir."
  ui_print "-      Modul bu durumda hicbir sey yapmaz."
fi

ui_print "- Yontem : post-fs-data.sh icinde dogrudan bind mount"
ui_print "-          (KernelSU overlay'ine bagimli degil)"
ui_print "- Kaynak : $SRC  ($(stat -c %s $SRC) bayt)"
ui_print "- Hedef  : /vendor/lib64/camera/aon_front.pb"
ui_print ""
ui_print "  Yeniden baslatinca dogrula:"
ui_print "    logcat -d | grep ishtar_aon_fix"
ui_print "    ls /vendor/lib64/camera/"
ui_print ""
