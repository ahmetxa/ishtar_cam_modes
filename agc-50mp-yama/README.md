# AGC 8.4.300 V9.6 — 50MP yaması

## Kök neden

AGC (GCam port) fotoğraf boyutu listesini `LAGC;->getSupportedOutputSizes()`
üzerinden alır; o da `StreamConfigurationMap.getOutputSizes(format)` çağırır.

Android bu metottan **"yüksek çözünürlük" sayılan** boyutları eler: minimum
kare süresi 1/20 sn'den uzun olan boyutlar sadece
`getHighResolutionOutputSizes()` ile döner.

ishtar / kamera 3 (IMX989 ana sensör) için ölçüm:

| boyut     | min kare süresi | sınıf          |
|-----------|-----------------|----------------|
| 4096x3072 | 33.333.333 ns (30 fps) | normal   |
| 8192x6144 | 66.666.666 ns (15 fps) | yüksek çöz. |

Bu yüzden AGC 50MP'yi hiç görmüyordu; Open Camera görüyordu çünkü o iki
listeyi de okuyor.

`LAGC;->Forty8Strip(I)I` bu yapıda `return p0` (boş saplama), yani portun
kendi 48M mekanizması devre dışı — sorunun kaynağı o değil.

## Yama

`classes2.dex` / `LAGC;`:

1. `getSupportedOutputSizes(I, StreamConfigurationMap)` yeniden yazıldı.
   Davranış aynı, tek fark: `pref_48m_key != 0` iken liste
   `allOutputSizes()` üzerinden gelir.
2. `allOutputSizes(StreamConfigurationMap, I)` eklendi:
   `getOutputSizes(f)` + `getHighResolutionOutputSizes(f)` birleşimi.
   İkincisi null/exception verirse birincisi aynen döner.

Yama **`pref_48m_key` arkasında kapalı**: bu tercih yoksa APK stok gibi
davranır.

## Yeniden üretme

```sh
# 1) dex çıkar
unzip -o AGC8.4.300_V9.6_snap.apk classes2.dex
# 2) baksmali (smali 2.5.2 + dexlib2 + guava + antlr-runtime + jcommander)
java -cp "<smali-jars>" org.jf.baksmali.Main d -o out2 classes2.dex
# 3) out2/AGC.smali icinde getSupportedOutputSizes'i bu klasordeki dosyayla
#    degistir, allOutputSizes.smali'yi sinifin sonuna ekle
# 4) smali
java -cp "<smali-jars>" org.jf.smali.Main a -a 29 -o classes2_new.dex out2
# 5) APK icindeki classes2.dex girdisini degistir (diger girdilerin
#    sikistirma yontemi korunmali), sonra zipalign + imzala
java -jar uber-apk-signer.jar -a AGC_V9.6_50mp.apk --allowResign
```

## Kurulum

İmza değiştiği için önce kaldırmak gerekir. Veri (AGC config = shared_prefs)
korunabilir:

```sh
tar -cf /data/local/tmp/agc_data.tar -C /data/data/org.codeaurora.snapcam .
pm uninstall org.codeaurora.snapcam
adb install AGC8.4.300_V9.6_50MP_patched.apk
tar -xf /data/local/tmp/agc_data.tar -C /data/data/org.codeaurora.snapcam
chown -R <yeni_uid>:<yeni_uid> /data/data/org.codeaurora.snapcam
chcon -R <ust_dizin_baglami> /data/data/org.codeaurora.snapcam
# calisma zamani izinleri yeniden verilmeli (pm grant CAMERA, RECORD_AUDIO, ...)
```

## Ölçülen sonuç

`pref_48m_key=1` + `pref_raw_key_0=35` (YUV) ile:

- fotoğraf boyutu tercihi `8192x6144` olarak **kalıyor** (eskiden
  4096x3072'ye geri yazılıyordu),
- `getImageReaderFormat ImageReaderFormat{ImageFormat=YUV_420_888,
  Size=8192x6144}`,
- cameraserver 8192x6144 YUV akışını yapılandırıyor.

**Ancak çekim tamamlanmıyor:** `CAM_ShotTracker: Stuck shot ... HDR_PLUS`.
Deklanşöre basıldığında HAL'e hiç istek gitmiyor; GCam motoru YUV yükünü
işleyemiyor. Yani APK tarafındaki tıkanıklık açıldı, sıra HAL tarafında.

`pref_48m_key` yokken APK stok gibi çalışıyor (RAW10 4096x3072, çekim
sorunsuz) — doğrulandı.
