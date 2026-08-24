#!/system/bin/sh
# ishtar 50MP (FullRes) HAL katmani -- ortak fonksiyonlar
#
# post-fs-data.sh, setmode.sh ve action.sh bu dosyayi ". halpatch.sh" ile alir.
#
# NEDEN 27 MB'lik BLOB YOK:
#   50MP, CamX HAL ikilisindeki (camera.qcom.so) InitializeScalerStaticCaps
#   fonksiyonunda 16 komutun degistirilmesiyle aciliyor. Ikilinin tamamini
#   pakete koymak yerine yalnizca 16 noktalik fark listesi tutuluyor
#   (blobs/hal-fullres.patch, ~900 bayt). Modul kurulumda cihazdaki STOK
#   ikiliyi active_hal/ altina kopyalar ve o kopyayi yamalar. Boylece:
#     * modul zip'i 27 MB sismez
#     * OTA ile HAL degisirse md5 kilidi tutmaz ve hicbir sey mount edilmez
#     * mod degisimi 27 MB kopyalamak yerine 16x4 bayt yazmak demektir
#
# NE YAPIYOR:
#   Yama, 8192x6144'un STANDART Camera2 cozunurluk listesine girmesini saglar.
#   Stok HAL'de 50MP yalnizca org.codeaurora.qcamera3.quadra_cfa vendor
#   tag'inde duyuruluyor; ucuncu parti uygulamalar standart listeye baktigi
#   icin goremiyor. Olculdu: yamasiz OpenCamera menude 50MP gosterse bile
#   cikti SESSIZCE 12,6 MP'ye dusuyor; yamayla 8192x6144 geliyor.
#
#   Sensorun aktif dizi boyutuna (activeArraySize) DOKUNULMUYOR -- bilerek.
#   Onu 8192x6144 yapan genis yama AGC'yi (GCam 8.4) cokertiyor:
#   "NullPointerException: com.google.googlex.gcam.Gcam.f() on a null object".
#   Alti varyantla dogrulandi; dar yama hem 50MP'yi acar hem AGC'yi yasatir.

HAL_BIN=camera.qcom.so
HAL_TGT=/odm/lib64/hw/$HAL_BIN
HAL_ACT=$MODDIR/active_hal/$HAL_BIN
HAL_PATCH=$MODDIR/blobs/hal-fullres.patch
HAL_STOCK_MD5=c3fa63a86ee3ecaf9fbf02005d35f6b5
HAL_FULLRES_MD5=fe0245a4720fb07b01d96deef47f5569
HAL_SIZE=27268688

hal_md5() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }

hal_mounted() { grep -q " $HAL_TGT " /proc/1/mountinfo 2>/dev/null; }

# Yiginlanmis bind mount'lari TEMAMEN kaldirir.
# Tek umount yetmiyor: mount ust uste kurulmussa yalnizca en usttekini alir
# ve dosya hala yamali kalir (olculdu, yanlis "stoka donuldu" sonucu verir).
hal_umount_all() {
  n=0
  while hal_mounted; do
    umount "$HAL_TGT" 2>/dev/null || break
    n=$((n + 1))
    [ $n -gt 40 ] && break
  done
  hal_mounted && return 1
  return 0
}

# hal_write <fullres|stock> -- active_hal kopyasindaki 16 noktayi yazar.
#
# Yama listesi baytlari HAZIR octal escape dizisi olarak tutar
# ("\021\207\175\271"). Once ic ice komut ikamesiyle
# (printf "\\$(printf '%03o' $b)") uretiliyordu; toybox sh'de bu YANLIS
# calisti -- komut ikamesi cozulmedi ve dosyaya printf'in kendi metni
# yazildi (16 nokta yerine 288 bayt bozuldu, olculdu). Simdi tek bir
# printf '%b' kullaniliyor: argumandaki escape'ler cozulur, '%' sorunu
# olmaz, ic ice ikame yoktur.
#
# Ofsetler 4'un kati oldugu icin dd bs=4 + 4-bayt indeksi kullanilir;
# bs=1 ile 23 milyonluk seek yapmaya gerek yok.
hal_write() {
  [ -f "$HAL_PATCH" ] || return 1
  [ -f "$HAL_ACT" ] || return 1
  while read -r idx es ep; do
    case "$idx" in '' | '#'*) continue ;; esac
    [ -n "$ep" ] || continue
    if [ "$1" = fullres ]; then e=$ep; else e=$es; fi
    printf '%b' "$e" |
      dd of="$HAL_ACT" bs=4 seek="$idx" count=1 conv=notrunc 2>/dev/null
  done < "$HAL_PATCH"
  return 0
}

# hal_state -- active_hal kopyasinin durumu: fullres | stock | unknown | none
hal_state() {
  [ -f "$HAL_ACT" ] || { echo none; return; }
  case "$(hal_md5 "$HAL_ACT")" in
    "$HAL_FULLRES_MD5") echo fullres ;;
    "$HAL_STOCK_MD5")   echo stock ;;
    *)                  echo unknown ;;
  esac
}

# hal_set <fullres|stock> -- kopyayi istenen duruma getirir ve DOGRULAR.
# Kamera servisleri DURDURULMUS olmaliduir; calisan HAL'in dosyasini
# degistirmek cokmeye yol acar.
hal_set() {
  want=$1
  [ "$want" = fullres ] && WANT_MD5=$HAL_FULLRES_MD5 || WANT_MD5=$HAL_STOCK_MD5
  [ "$(hal_state)" = "$want" ] && return 0
  # Bozuk/bilinmeyen kopyayi stoktan yeniden uret
  if [ "$(hal_state)" = unknown ] || [ "$(hal_state)" = none ]; then
    hal_seed || return 1
  fi
  hal_write "$want" || return 1
  [ "$(hal_md5 "$HAL_ACT")" = "$WANT_MD5" ]
}

# hal_seed -- cihazdaki STOK ikiliyi active_hal/ altina kopyalar.
# Bind mount aktifken cagirmayin: hedef zaten bizim kopyamizi gosterir.
hal_seed() {
  hal_mounted && return 1
  [ -f "$HAL_TGT" ] || return 1
  [ "$(hal_md5 "$HAL_TGT")" = "$HAL_STOCK_MD5" ] || return 1
  mkdir -p "$MODDIR/active_hal" || return 1
  cat "$HAL_TGT" > "$HAL_ACT" || return 1
  chown 0:0 "$HAL_ACT" 2>/dev/null
  chmod 0644 "$HAL_ACT" 2>/dev/null
  chcon u:object_r:vendor_file:s0 "$HAL_ACT" 2>/dev/null
  [ "$(hal_md5 "$HAL_ACT")" = "$HAL_STOCK_MD5" ]
}
