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

## HAL tarafi: pixelArraySize yazim yeri (Faz 3.2 / IMPL-18)

`find_tag_write_site.py` — `camera.qcom.so` icinde bir metadata tag'inin
yazim yerini bulan salt-okunur analiz betigi. Hicbir yama uygulamaz.

    python find_tag_write_site.py <camera.qcom.so> f0006

Stock HAL `c3fa63a86ee3ecaf9fbf02005d35f6b5` (27.268.688 B) uzerinde
`android.sensor.info.pixelArraySize` (tag `f0006`) icin bulunan sonuc:

- Ontolojide kayitli **dokuz `movz`/`movk` adresi yanlis pozitif** — hicbiri
  `0xf0006` kurmuyor; bolme sabitleri, 64-bit literal ve hash anahtarlari.
- **Alti rodata dword'u gercek ve tam** (dosyadaki tek alti hizali
  `0x000f0006`), ama **deger kaynagi degil**: tag listesi tablolarinin ici,
  hicbirine tam `adrp`+`add` ile erisilmiyor.
- Gercek yazim, `0x01661f40`'ta baslayan fonksiyonda:
  `S = [x24+0x60]`, deger `S+0x3c1c`'ten (veya `[S+0x3d84] == 1` ise
  `S+0x3db4`'ten) `[x19+0x6550]` yuvasina kopyalanir, sonra
  `bl 0x0166648c` ile publisher `0x1755430` uzerinden `count=2` yayinlanir.
- **Deger calisma aninda turetilir; ikilide sabit degildir.** Yamalanacak bir
  sabit yok; en iyi tek-kelime adayi `0x01666440` (`mov w5, #0x3c1c`), yani
  hangi `(genislik, yukseklik)` ciftinin yayinlandigini secen immediate.

Tam kayit ve siralanmis aday listesi: `Planner-docs/Project-Ontology.md`
adres defteri, `EV-24`/`EV-25`/`EV-26`, ve `Planing-Ledger.md` IMPL-18.
Yamayi Faz 3.3 uygular; bu betik olcmez, yalnizca bulur.

## HAL tarafi: aktif dizi yazim yerleri (Faz 4.5 / IMPL-27)

`hal-activearray-deneme.patch` bu klasordeki **ucuncu** tablodur. Faz 3.5,
`f0006`'yi tek basina yukseltmenin AGC'de 50.3 MP yakalamayi actigini ama
goruntunun geometrik olarak bozuk kaldigini olctu (`FIND-3.5-01`): kare
tam boy tamponun yalnizca aktif-dizi kadarini doldurdugu icin yarisi siyah,
kalani macenta tonlu. Sebep, aktif dizi etiketlerinin `[0 0 4096 3072]`'te
kalmasidir. Bu tablo onlari yukseltir.

- **`f0000`** `android.sensor.info.activeArraySize` — yayin `bl 0x0166234c`,
  `count=4`. Etiket TEK bir `movz w1, #0xf, lsl #16` (`0x01662338`) ile
  kurulur; her etiketin kullandigi `movz`+`movk` ciftini arayan bir tarama
  bu yuzden onu **gormez** — daha once "aile `f0001`..`f000a`" denmesinin
  sebebi budur ve duzeltilmistir.
- **`f000a`** `android.sensor.info.preCorrectionActiveArraySize` — yayin
  `bl 0x01666588`, `count=4`.
- Her ikisi de once BINNENMEMIS kaynaktan okunur, sonra secici
  `[S+0x3d84] == 1` ise BINNENMIS kaynaktan uzerine yazilir:
  `f0000` varsayilan `S+0x3c54` / uzerine `S+0x3d98`,
  `f000a` varsayilan `S+0x3c24` / uzerine `S+0x3d88`.
- Baslatici ciftleri **isaretli bolme** ile turetir —
  `[S+0x3d98] = [S+0x3c54] / binning` (`0x016f077c`..`0x016f07a0`) ve
  `[S+0x3d88] = [S+0x3c24] / binning` (`0x016f0888`..`0x016f08ac`) — yani
  **tam cozunurluklu dikdortgen `S` icinde ZATEN vardir** (F4.5-04: EVET).
  `f0006` cifti (`0x016f07c0`..`0x016f07e4`) ayni sekilde cozulur ve
  kontrol gorevi gorur.
- Yama bu yuzden `f0006`'nin dogrulanmis yamasiyla **ayni sinifta**: tek
  kelimelik bir `movz` immediate yonlendirmesi. Sinir disi okuma uretmez,
  cunku kosullu `q` yukunu ayni temel blokta kosulsuz `q` yukunun zaten
  okudugu 16 bayta yoneltir.

**`80340003`** (`org.codeaurora.qcamera3.quadra_cfa.activeArraySize`) bu
tabloda **yoktur ve olamaz**. Sabit, 27 MB ikilide 4-bayt hizali dword
olarak **sifir** kez gecer ve `.text` icinde `movz`/`movk` ile **hic**
kurulmaz; yalnizca isim dizgisi vardir (`0x002265af`, `org.codeaurora
.qcamera3.bfw` ve `com.xiaomi.camera.supportedfeatures` ile ayni satici
bolum-adi tablosunda). Satici etiket numarasi calisma aninda saglayici
tarafindan `0x80000000` tabanindan atanir. Bu, **acik bir negatif
sonuctur** (F4.5-05), eksik birakilmis bir madde degil.

Tam kayit: `Planner-docs/Project-Ontology.md` adres defteri ve
`Planing-Ledger.md` IMPL-27. Onceden taahhut edilen md5'ler yama
dosyasinin basligindadir; besteleyici bunlari uretmeden once alti bilinen
md5'i birebir yeniden uretmistir.
