#!/system/bin/sh
# ishtar IMX989 kamera modu -- kutucuk / WebUI eylem arayuzu
#
# setmode.sh insan icindir (uzun aciklamalar basar). Bu dosya makine icindir:
# tek kelimelik cikti verir, hizlidir, tekrar tekrar cagrilabilir.
#
#   action.sh                -> SIRALA: stock -> dcgB -> ln4f -> stock
#                               (KernelSU yoneticisindeki "Action" dugmesi
#                                dosyayi argumansiz calistirir; tek dokunusluk
#                                davranis budur)
#   action.sh get            -> etkin mod adi (stock, dcgB, ln4f, ... | unknown)
#   action.sh state <mod>    -> on | off
#   action.sh set <mod>      -> moda gecer, yeni etkin modu basar
#   action.sh toggle <mod>   -> mod etkinse stock'a, degilse o moda gecer
#   action.sh cycle          -> sirala (argumansiz calistirmayla ayni)
#   action.sh list           -> kullanilabilir modlar (bosluklu)
#   action.sh info           -> "etkin|mount|md5" tek satir ozet
#   action.sh lang           -> arayuz dili: en | tr   (varsayilan en)
#   action.sh lang <en|tr>   -> dili ayarla
#   action.sh tiles install  -> kutucuk uygulamasini kur/guncelle
#   action.sh tiles order    -> dort kutucugu WebUI sirasina diz
#   action.sh tiles status   -> apk / takma ad / kok / kutucuk ozeti
#
# Cikis kodu: 0 basarili, 1 hata.

MODDIR=${0%/*}
[ -d "$MODDIR" ] || MODDIR=/data/adb/modules/ishtar_cam_modes
BIN=com.qti.sensormodule.ishtar_semco_imx989_wide.bin
TGT=/odm/lib64/camera/$BIN
MODES="stock 50mp ln2 ln4 ln2s ln4s ln2f ln4f dcgA dcgB"
SENSOR_MODES="stock ln2 ln4 ln2s ln4s ln2f ln4f dcgA dcgB"
DEFAULT_OFF=stock
PKG=com.ishtar.cammodes

# 50MP HAL katmani (hal_state / hal_mounted)
[ -f "$MODDIR/halpatch.sh" ] && . "$MODDIR/halpatch.sh"

md5of() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }

# Kutucuklarin Hizli Ayarlar'a EKLENME sirasi. "cmd statusbar add-tile"
# listenin BASINA ekliyor (cihazda olculdu), bu yuzden liste istenen siranin
# TERSIDIR; sonuc 50MP - DCG - LN4 - LN2 olur, yani WebUI'deki sirayla ayni.
TILE_ADD_ORDER="Ln2Tile Ln4Tile DcgTile FullResTile"

tiles_add()   { for t in $TILE_ADD_ORDER; do cmd statusbar add-tile "$PKG/.$t" >/dev/null 2>&1; done; }
tiles_order() { for t in $TILE_ADD_ORDER; do cmd statusbar remove-tile "$PKG/.$t" >/dev/null 2>&1; done; tiles_add; }

# Kurulu APK ile modulunkinin ayni yapim olup olmadigi. Android APK'yi
# oldugu gibi kopyaladigi icin md5'ler esittir (cihazda dogrulandi); ayrica
# surum numarasi tutmaya gerek kalmaz.
apk_installed_md5() {
  P=$(pm path "$PKG" 2>/dev/null | sed -n 's/^package://p' | head -1)
  [ -n "$P" ] && md5of "$P"
}

root_granted() { grep -aq "$PKG" /data/adb/ksu/.allowlist 2>/dev/null; }

# Baslatici TAKMA ADININ durumu -- kendi kaydimiza degil cerceveye sorulur.
# DIKKAT: bu cercevenin cevabidir, cekmecenin degil; ikisi bu ROM'da ayrisir.
# Cihazda olculdu: modul "gizli" saydigi hâlde girdi cekmecede durabiliyor,
# bu yuzden durum raporu tahmine dayanmamali.
launcher_state() {
  if cmd package query-activities -a android.intent.action.MAIN -c android.intent.category.LAUNCHER 2>/dev/null | grep -q "name=$PKG\.Launcher"; then
    echo gorunur
  else
    echo gizli
  fi
}

# Baslatici takma adi KernelSU'nun Superuser listesi icin gerekli: o liste
# baslatici etkinligi olmayan uygulamayi gizliyor, dolayisiyla kok yetkisi
# verilemiyor.
#
# VARSAYILAN: GORUNUR. v2.0'da "kok yetkisi verilince kendiliginden gizle"
# kurali vardi; cihazda olculdu ve bu ROM'da HICBIR SEY gizlemiyor:
# AOSPA Launcher3, takma ad "pm disable" ile kapatilsa da uygulamayi
# cekmecede tutuyor (taze kurulumdan sonra da, yani bayat onbellek degil).
# Tek etkisi girdiyi OLU birakmak: dokununca WebUI yerine Android'in
# "Uygulama Bilgisi" sayfasi aciliyordu. Gorunur birakmak kesinlikle daha
# iyi -- simge dogru cizilir ve dokununca WebUI acilir.
#   hide_launcher -> kullanici bilerek gizledi (baska bir baslaticida ise yarar)
#   yoksa         -> gorunur
# Kural HER cagrida uygulanir. Onceden son durum .launcher dosyasinda
# tutulup ayniysa pm atlaniyordu; bu, bilesen durumu disaridan degisince
# (uygulama guncellemesi, elle "pm enable", baska bir arac) modulun bir daha
# duzeltmemesi demekti. Etkisiz bir "pm enable/disable" zaten bedava.
launcher_sync() {
  if [ -f "$MODDIR/hide_launcher" ]; then W=disable; else W=enable; fi
  pm "$W" "$PKG/$PKG.Launcher" >/dev/null 2>&1
  echo "$W"
}

# Etkin mod. 50MP HAL katmanindadir ve sensor katmanini stock'a aldigi icin
# ONCE HAL'e bakilir; yamaliysa mod 50mp'dir.
active() {
  if command -v hal_state >/dev/null 2>&1; then
    [ "$(hal_state)" = fullres ] && { echo 50mp; return; }
  fi
  L=$(md5of "$TGT")
  [ -z "$L" ] && { echo unknown; return; }
  for m in $SENSOR_MODES; do
    [ "$(md5of "$MODDIR/blobs/$m.bin")" = "$L" ] && { echo "$m"; return; }
  done
  echo unknown
}

mounted() { grep -q " /odm/lib64/camera/$BIN " /proc/1/mountinfo 2>/dev/null; }

valid() {
  for m in $MODES; do [ "$m" = "$1" ] && return 0; done
  return 1
}

apply() {
  valid "$1" || { echo "gecersiz mod: $1" >&2; return 1; }
  if [ "$1" = 50mp ]; then
    # 50MP'nin sensor blob'u yok; HAL yama listesiyle calisir.
    [ -f "$MODDIR/blobs/hal-fullres.patch" ] || {
      echo "HAL yama listesi yok" >&2; return 1; }
  else
    [ -f "$MODDIR/blobs/$1.bin" ] || { echo "blob yok: $1" >&2; return 1; }
  fi

  # Isi KOPARILMIS olarak yurut: cagiran (kutucuk servisi ya da WebUI) is
  # bitmeden oldurulurse yeniden baslatma yarida kalmasin.
  #
  # Blob yazilir yazilmaz DONMUYORUZ: kamera yigini o an henuz hazir degil
  # (olculdu, ~4-6 sn). Erken donunce kullanici hemen kamerayi aciyor ve
  # "acilmiyor" sanilan sessiz basarisizlik olusuyordu. Bayragin silinmesi
  # isin gercekten bittigini gosterir.
  : > "$MODDIR/.busy"
  setsid sh -c "sh '$MODDIR/setmode.sh' '$1' >/dev/null 2>&1; rm -f '$MODDIR/.busy'"     </dev/null >/dev/null 2>&1 &

  i=0
  while [ -f "$MODDIR/.busy" ] && [ $i -lt 160 ]; do
    sleep 0.25
    i=$((i + 1))
  done
  rm -f "$MODDIR/.busy"
  # Buraya ulasmak kok yetkisinin VERILDIGINI kanitlar (script su ile
  # calisti), dolayisiyla baslaticinin gorunur kalmasi icin sebep kalmadi.
  launcher_sync >/dev/null 2>&1
  active
}

case "$1" in
"" | cycle)
    # KernelSU "Action" dugmesi buraya duser: tek dokunusla sirala.
    CUR=$(active)
    case "$CUR" in
      stock) NEXT=dcgB ;;
      dcgB)  NEXT=ln4f ;;
      ln4f)  NEXT=50mp ;;
      50mp)  NEXT=stock ;;
      *)     NEXT=stock ;;
    esac
    echo "IMX989 kamera modu"
    echo "  simdiki : $CUR"
    echo "  gecilen : $NEXT"
    echo
    NEW=$(apply "$NEXT") || exit 1
    echo "-> etkin mod: $NEW"
    [ "$NEW" = stock ] && echo "   (stok surucu; video ve 50MP calisir)" \
                       || echo "   (fotograf modlari yamali; VIDEO ve 50MP icin stock'a donun)"
    echo "   kamera uygulamasini yeniden acin."
    exit 0 ;;
esac

case "$1" in
  get)    active ;;
  list)   echo "$MODES" ;;
  state)
    [ -n "$2" ] || { echo "kullanim: action.sh state <mod>" >&2; exit 1; }
    [ "$(active)" = "$2" ] && echo on || echo off ;;
  set)
    [ -n "$2" ] || { echo "kullanim: action.sh set <mod>" >&2; exit 1; }
    apply "$2" ;;
  toggle)
    [ -n "$2" ] || { echo "kullanim: action.sh toggle <mod>" >&2; exit 1; }
    if [ "$(active)" = "$2" ]; then apply "$DEFAULT_OFF"; else apply "$2"; fi ;;
  info)
    # "mod|mount|md5|dil|hal" -- kutucuk uygulamasi ve WebUI tek cagriyla okur.
    # 5. alan v2.0'da eklendi; eski okuyucular ilk 4 alani kullanmaya devam eder.
    if mounted; then M=aktif; else M=yok; fi
    L=$(cat "$MODDIR/lang" 2>/dev/null); case "$L" in tr|en) ;; *) L=en ;; esac
    if command -v hal_state >/dev/null 2>&1; then H=$(hal_state); else H=yok; fi
    printf '%s|%s|%s|%s|%s\n' "$(active)" "$M" "$(md5of "$TGT")" "$L" "$H" ;;
  lang)
    # Arayuz dili: hem kutucuk uygulamasi hem WebUI buradan okur.
    # SISTEM DILINDEN BAGIMSIZDIR; varsayilan Ingilizce.
    LANGF=$MODDIR/lang
    case "$2" in
      "")
        L=$(cat "$LANGF" 2>/dev/null)
        case "$L" in tr|en) echo "$L" ;; *) echo en ;; esac ;;
      en|tr)
        echo "$2" > "$LANGF"
        chmod 0644 "$LANGF" 2>/dev/null
        echo "$2" ;;
      *)
        echo "kullanim: action.sh lang [en|tr]" >&2; exit 1 ;;
    esac ;;
  tiles)
    # QS kutucuk uygulamasi yonetimi
    APK=$MODDIR/tile-app.apk
    case "$2" in
      install)
        # service.sh her acilista bunu cagirir; idempotenttir.
        [ -f "$APK" ] || { echo "apk yok: $APK" >&2; exit 1; }
        if pm list packages 2>/dev/null | grep -q "^package:$PKG$"; then FRESH=0; else FRESH=1; fi
        if [ "$(apk_installed_md5)" = "$(md5of "$APK")" ]; then
          R=guncel
        else
          pm install -r "$APK" >/dev/null 2>&1 || { echo "kurulamadi" >&2; exit 1; }
          if [ "$FRESH" = 1 ]; then R=kuruldu; else R=guncellendi; fi
        fi
        # Kutucuklar YALNIZCA ilk kurulumda eklenir. Guncellemede eklenseydi
        # kullanicinin Hizli Ayarlar duzeni her acilista bozulurdu; sirayi
        # yeniden dizmek isteyen 'action.sh tiles order' calistirir.
        [ "$FRESH" = 1 ] && tiles_add
        # Toast'lar bildirimleri kapali uygulamalarda bastiriliyor
        pm grant "$PKG" android.permission.POST_NOTIFICATIONS >/dev/null 2>&1
        cmd appops set "$PKG" POST_NOTIFICATION allow >/dev/null 2>&1
        # Saniyelik geri sayim icin kendi katmani: toast kotasi (~5/20sn)
        # saniyelik guncellemeye izin vermiyor.
        cmd appops set "$PKG" SYSTEM_ALERT_WINDOW allow >/dev/null 2>&1
        printf '%s, baslatici=%s
' "$R" "$(launcher_sync)" ;;
      order)
        # Dort kutucugu WebUI sirasina dizer. Kullanicinin duzenini BILEREK
        # bozar; bu yuzden yalnizca elle cagrilir.
        tiles_order
        echo "kutucuk sirasi: 50MP DCG LN4 LN2" ;;
      sync)
        # Baslatici gorunurlugunu kurala gore tazeler (service.sh kullanir).
        launcher_sync ;;
      show)
        rm -f "$MODDIR/hide_launcher"
        launcher_sync >/dev/null
        echo "baslatici acildi -- KernelSU > Superuser'dan kok yetkisi verin" ;;
      hide)
        : > "$MODDIR/hide_launcher"
        launcher_sync >/dev/null
        echo "baslatici takma adi kapatildi -- cekmeceden kalkip kalkmadigi baslaticiya bagli (AOSPA tutar)" ;;
      status)
        if pm list packages 2>/dev/null | grep -q "^package:$PKG$"; then
          if [ "$(apk_installed_md5)" = "$(md5of "$APK")" ]; then I=guncel; else I=eski; fi
        else
          I=yok
        fi
        L=$(launcher_state)
        if [ -f "$MODDIR/hide_launcher" ]; then S=elle-gizli; else S=varsayilan; fi
        if root_granted; then K=var; else K=yok; fi
        T=$(settings get secure sysui_qs_tiles 2>/dev/null | tr ',' '
' | grep -c "$PKG/")
        printf 'apk=%s takma_ad=%s (%s) kok_kaydi=%s kutucuk=%s
' "$I" "$L" "$S" "$K" "$T" ;;
      *)
        echo "kullanim: action.sh tiles {install|order|sync|show|hide|status}" >&2; exit 1 ;;
    esac ;;
  *)
    echo "kullanim: action.sh {get|list|state <mod>|set <mod>|toggle <mod>|info|lang|tiles}" >&2
    exit 1 ;;
esac
