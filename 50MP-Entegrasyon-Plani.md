# 50MP (FullRes) entegrasyonu — 10 fazlı plan

**Hedef:** `Module_Highres_13U_Switcher_A14` modülünün 50MP yeteneğini
`ishtar-cam-modes` (v1.9) modülüne entegre etmek; A14 → A15 portu yapmak,
kutucuk uygulamasını düzeltmek, tek parça flash edilebilir paket üretmek.
Ardından AOSPA beryl derlendiğinde A16'ya taşımak.

**Cihaz:** Xiaomi 13 Ultra (ishtar) · AOSPA Android 15 (vauxite) · KernelSU Next 3.3.0
**Kamera uygulaması:** AGC = `org.codeaurora.snapcam` (GCam portu)

---

## Faz 1 — Envanter ve keşif  ✅ TAMAMLANDI

- 50MP modülünün dosya ağacı, script'leri, blob'ları çıkarıldı
- `enable`/`disable` HAL ikilileri bayt düzeyinde karşılaştırıldı
- Cihazın mevcut durumu (kurulu modüller, kutucuk uygulaması sürümü,
  çekmece görünürlüğü, HAL md5, property'ler) kayda geçirildi

**Çıktı:** bu belgenin "Faz 1 bulguları" bölümü.

## Faz 2 — 50MP mekanizmasının tersine çevrilmesi  ✅ TAMAMLANDI

- 73 yama noktasının hangi kod bölgesinde olduğu ve ne yaptığı
- `maxRAWSizes=19` property'sinin tek başına ne kadarını sağladığı
  (binary yama olmadan da 50MP açılıyor mu? — **en kritik soru**)
- `overrideForceSensorMode 0` gerekliliği (mod 0 = 8192×6144 = 50MP)
- Bizim `dcgB`/`ln4f` yamalarıyla çakışma haritası

**Çıktı:** mekanizma raporu + "binary yama gerçekten gerekli mi" kararı.

## Faz 3 — Android 15 uyum analizi  ✅ TAMAMLANDI

- Cihazın A15 HAL'i ile modülün A14 HAL'i arasındaki yapısal fark
- Yama noktalarının A15 ikilisinde karşılığının bulunup bulunamayacağı
- Property/SELinux/yol farkları — **varsayarak değil, cihazda kanıtlayarak**

**Çıktı:** port edilebilirlik kararı ve yöntem seçimi.

## Faz 4 — A15 portu ve blob üretimi  ✅ TAMAMLANDI

- Seçilen yönteme göre A15 HAL'ine yamanın uygulanması (ya da yamasız çözüm)
- Bağımsız doğrulayıcı: yamalanan her noktanın beklenen bayt desenini taşıması
- Geri alma güvenliği: stok HAL md5 kilidi

**Çıktı:** `blobs/hal-fullres.so` (veya property-only çözüm) + doğrulama raporu.

## Faz 5 — Ana modüle entegrasyon (mod katmanı)  ✅ TAMAMLANDI

- `setmode.sh` / `action.sh` / WebUI'ye 50MP modunun eklenmesi
- **İki bind mount birden:** sensör bin'i (mevcut) + HAL ikilisi (yeni)
- DCG/LN ile çakışma kuralının uygulanması (bkz. Açık Karar #1)
- Geçiş süresi ve `.busy` bayrağı mantığının HAL yeniden yüklemeyi de kapsaması

**Çıktı:** v2.0 script katmanı.

## Faz 6 — Kutucuk uygulaması: ikon + 50MP butonu  ✅ TAMAMLANDI

- Bozuk 50MP ikonunun düzgün bir vektörle değiştirilmesi
- 50MP kutucuğunun senkron / geri sayım / dil altyapısına bağlanması
- Dört kutucuğun tutarlı davranışı (biri açılınca diğerleri kapanır)

**Çıktı:** tile-app 2.0.

## Faz 7 — Çekmecede gizleme + APK'nın modüle gömülmesi  ✅ TAMAMLANDI

- Başlatıcı takma adı davranışının geri getirilmesi (şu an bozuk)
- `service.sh` ile otomatik kurulum + `POST_NOTIFICATIONS` + `SYSTEM_ALERT_WINDOW`
- APK'nın modül zip'inin içine gömülmesi

**Çıktı:** tek parça flash edilebilir zip.

## Faz 8 — Cihazda 50MP doğrulaması

- AGC ile 50MP çekim; çıktı çözünürlüğü ve dosya bütünlüğü denetimi
- Kilitlenme kontrolü (CSIPHY/IFE sızıntısı), ardışık geçiş testi
- 12-bit modlarıyla birlikte davranış

**Çıktı:** ölçüm raporu.

## Faz 9 — Regresyon ve paketleme

- DCG/LN modları, geçiş, geri sayım, WebUI, dil — hepsi hâlâ sağlam mı
- `Kullanim.txt`, `module.prop`, zip, hafıza güncellemesi

**Çıktı:** yayına hazır v2.0.

## Faz 10 — Android 16 / beryl hazırlığı

- A16'ya taşımak için gereken adımların kontrol listesi
- Araçların yeni HAL'e karşı çalıştırılabilir hâlde bırakılması
- **Bloke:** AOSPA beryl derlemesi (WSL2 + ~300 GB disk gerekiyor)

**Çıktı:** port kılavuzu.

---

# Faz 1 bulguları

## 50MP modülü ne yapıyor

| Öğe | Değer |
|---|---|
| Modül kimliği | `fullres` — "FullResSwitcher-A14", yazar Sav |
| Dokunduğu dosya | `/odm/lib64/hw/camera.qcom.so` — **CamX HAL ikilisi** |
| Yöntem | `active_hal/` altına kopyala → tek dosya `mount --bind` |
| Property | `persist.vendor.camera.maxRAWSizes=19` (hem `system.prop` hem çalışma anı) |
| Property (silinen) | `vendor.debug.camera.overrideForceSensorMode` |
| Orijinal QuickTile | `overrideForceSensorMode 0` + blob kopyala + `stop/start media` + `killall -1` provider |
| sepolicy.rule | boş |
| service.sh | boş |

**Bizim modülümüzden temel farkı:** biz *veri* dosyası olan sensör bin'ini
yamalıyoruz; bu modül *derlenmiş kod* olan HAL ikilisini yamalıyor.

## HAL ikilisi karşılaştırması

| Dosya | Boyut | md5 |
|---|---|---|
| `mod/disable/camera.qcom.so` | 31.004.560 | `35194d60e7e8a246b05de64a11b9ff7c` |
| `root/odm/lib64/hw/camera.qcom.so` | 31.004.560 | `35194d60…` (disable ile **aynı**) |
| `mod/enable/camera.qcom.so` | 31.004.560 | `f6b4fbd0d5e7403292070c2dad3c4df6` |
| **Cihazdaki (A15)** | **27.268.688** | `c3fa63a86ee3ecaf9fbf02005d35f6b5` |

Yani modülün getirdiği ikili cihazdakinden **3,7 MB büyük, tamamen farklı bir
derleme**. Olduğu gibi bind mount edilirse kamera kesin çalışmaz.

## Yamanın niteliği

`enable` ile `disable` arasında **228 bayt / 73 bölge** fark var ve hepsi tek bir
kalıp:

```
b9 7d 87 88   LDR  W8, [X28, #imm]     ->   52 80 00 08   MOV  W8, #0
b9 7d 87 29   LDR  W9, [X25, #imm]     ->   52 80 00 09   MOV  W9, #0
...
```

Yani 73 ayrı yerde bir **32-bit alan okuması sıfırlanıyor**. Klasik "kısıt
kontrolünü etkisizleştir" yaması. Yama noktaları `0x01910000`–`0x0197xxxx`
aralığında, tek bir kod bölgesinde toplanmış.

## Karşılaşılan problemler ve çözümleri

**1. Bütün araçlar bloke oldu.** `caveman` hook'ları PowerShell sözdizimiyle
(`& 'yol' arg`) yazılmıştı ama bash'e veriliyordu; Bash, PowerShell, Read, Glob
— hepsi `syntax error near unexpected token '&'` verdi. Kendim düzeltemedim
çünkü düzeltmek de bir araç gerektiriyordu. Kullanıcı `settings.json`'daki `&`
öneklerini kaldırdı, araçlar açıldı.

**2. Sembol tabanlı port yapılamayacak.** ELF sembol tablosunu ayrıştırdım:
31 MB'lık kütüphanede yalnız **821 dışa açık fonksiyon sembolü** var ve 73 yama
noktasının **hiçbiri** bir sembolün içine düşmüyor — hepsi isimsiz yerel kodda.
Dolayısıyla "aynı fonksiyonu A15'te bul" yaklaşımı işlemez; Faz 2/3'te
**kalıp + anlam** temelli bir yöntem gerekecek.

**3. Modül klasörü el değmemiş değil.** `post-fs-data.sh` ve `customize.sh`
önceki model tarafından değiştirilmiş (Türkçe yorumlar, "KernelSU Next uyumu",
"AGC Lens.java crash fix" notu, Kitsune kontrolünün devre dışı bırakılması).
Blob'lar (Mart 2024 tarihli) orijinal. Bunu referans alacağım ama script'leri
kendi altyapımıza göre yeniden yazacağım.

## Cihazın mevcut durumu

| | |
|---|---|
| `ishtar_cam_modes` | v1.9, etkin mod `stock` |
| `fullres` modülü | **kurulu değil** |
| `persist.vendor.camera.maxRAWSizes` | **19** (modül kurulu olmamasına rağmen) |
| Kutucuk uygulaması | versionCode 8 / 1.7 — **önceki modelin derlemesi** |
| Kayıtlı kutucuklar | `DcgTile`, `Ln4Tile`, `Ln2Tile`, **`FiftyTile`** |
| Uygulama çekmecesinde | **GÖRÜNÜYOR** (regresyon — gizlenmesi gerekiyordu) |

---

# Faz 2 bulguları

## Ana soru: binary yama gerçekten gerekli mi? → **EVET, gerekli**

Cihazda `persist.vendor.camera.maxRAWSizes=19` **zaten ayarlı** ve HAL bu
property ile 46 dakikadır çalışıyor. Buna rağmen:

| Metadata anahtarı | En büyük çözünürlük |
|---|---|
| `android.scaler.availableStreamConfigurations` (camera 0) | **4096 × 3072** |
| `org.codeaurora.qcamera3.quadra_cfa.availableStreamConfigurations` | **8192 × 6144** |
| `android.scaler.availableStreamConfigurationsMaximumResolution` | **yok** |
| `android.request.availableCapabilities` | `ULTRA_HIGH_RESOLUTION_SENSOR` **yok** |

→ Property tek başına 50MP'yi standart listeye eklemiyor. Yama zorunlu.

## Kök neden

IMX989 bir **QCFA (Quad-Bayer) sensör**. HAL, 8192×6144 boyutunu yalnızca
Qualcomm'a özel `quadra_cfa` vendor tag'i altında duyuruyor; standart Camera2
listesinde en büyük boyut 4096×3072 (12MP). MiuiCamera vendor tag'i bildiği
için 50MP çekebiliyor, üçüncü parti uygulamalar (AGC/GCam dahil) standart
listeye baktığı için çekemiyor.

## Yama gerçekte ne yapıyor — 4 ayrı fonksiyon

Sembol yok, ama log string'leri fonksiyonları kesin olarak tanımlıyor:

| Grup | Adet | Dosya / fonksiyon | Değişiklik |
|---|---|---|---|
| **A** | 48 | `camxchicontext.cpp` → `InitializeStaticMetadataPool` | `LDR Wn,[Xm,#0x3d84]` → `MOV Wn,#0` |
| **B** | 8 | aynı fonksiyon | `+0x00/+0x04/+0x08` okumaları sıfırlanıyor |
| **C** | 9 | `camxhwenvironment.cpp` → `InitializeScalerStaticCaps` | `CMP Wn,#4`→`#5`, `B.EQ`→`B.NE`, `CMP W0,#2`→`CMP W0,W0` |
| **C2** | 3 | `camximagesensordata.cpp` → `GetSensorStaticCapability` | QCFA pozlama aralığı kontrolü |
| **D** | 4 | `camxhwenvironment.cpp` → `InitializeScalerStaticCaps` | `MOVK #0x41CD,LSL#48` → `#0x41BD` |

**A/B grubu:** 48 noktanın hepsi **aynı struct alanını** (`+0x3d84`) okuyor.
Yakınındaki log: `activeArraySize for quadcfa sensor: %dx%d`. Alan sıfırlanınca
HAL sensörü QCFA gibi ele almayı bırakıyor. Alan yazma (`STR`) komutu yok →
bu bir StaticSettings alanı **değil**, çalışma anında hesaplanan bir bayrak.
Dolayısıyla `camxoverridesettings.txt` veya property ile taklit **edilemez**.

**C grubu:** `InitializeScalerStaticCaps` — standart scaler listesini üreten
fonksiyon. Kritik loglar: `Skip internal raw dim ... check next for normal
bayer raw` (2520) ve `Quad CFA raw dim ... check next for normal bayer raw`
(2528). Yama tam olarak bu **"QCFA boyutunu atla"** mantığını bozarak
8192×6144'ün standart listeye girmesini sağlıyor.

**D grubu:** `973.078.528` → `486.539.264` — **tam olarak yarısı**. Bir piksel
hızı / kare süresi sabiti. 50MP karesinin gerçek süresine göre
`minFrameDuration` hesabını düzeltiyor.

## DCG/LN ile çakışma haritası

- **Teknik katman çakışması yok:** bizim yamamız sensör *veri* dosyasında
  (`com.qti.sensormodule...bin`), bu yama HAL *kodunda*. Ayrı bind mount'lar.
- **Semantik çakışma var:** DCG/LN açıkken küresel `whiteLevel` 16383 (12-bit)
  ama sensör modu 0 (50MP) 10-bit kalıyor → 50MP görüntü bozuk çıkar.
- Karar #1 gereği önce **birbirini dışlayan** kurulacak.

## Port yöntemi kararı (Faz 3'e girdi)

Sembol tabanlı port imkânsızdı; ancak **log string'leri A15 ikilisinde de
bulunacak**. Yöntem: A15 HAL'inde aynı string'lerden fonksiyon gövdelerini
tespit et, aynı komut kalıplarını o gövdelerin içinde ara, yamayı orada üret.
Bu, "aynı ofsete kör yama" yaklaşımından çok daha güvenli.

---

# Faz 3 bulguları

## Port edilebilirlik kararı: **EVET**

A15 HAL'i cihazdan çekildi: 27.268.688 bayt, md5 `c3fa63a86ee3ecaf9fbf02005d35f6b5`
(Faz 4'te stok kilidi olarak kullanılacak.)

**Tüm log string'leri A15'te de mevcut** → aynı CamX kod tabanı, aynı
fonksiyonlar, aynı kaynak dosyaları (`camx-common-ishtar`).

## Struct düzeni korunmuş

Yamanın hedefi olan `+0x3d84` alanı A15'te de var. Büyük struct offsetlerinin
kullanım histogramı iki sürümde neredeyse birebir:

| Offset | A14 | A15 |
|---|---|---|
| `+0x028A0` | 300 | 297 |
| `+0x01028` | 222 | 222 |
| `+0x0150C` | 135 | 135 |
| **`+0x03D84`** | **53** | **55** |

Bu, A14→A15 geçişinde ilgili yapının değişmediğini gösteriyor — port için
en önemli tek bulgu.

## Fonksiyon bazlı eşleme

Fonksiyon sınırları, log makrolarının `%s()` argümanı olan fonksiyon adı
string'lerine yapılan xref'lerden çıkarıldı:

| Fonksiyon | A14 `+0x3d84` | A14 yamalanan | A15 `+0x3d84` |
|---|---|---|---|
| `InitializeStaticMetadataPool` | 27 | **27 (hepsi)** | **27** ✓ |
| `InitializeScalerStaticCaps` | 13 | **13 (hepsi)** | 16 |
| `GetSensorStaticCapability` | 6 | **6 (hepsi)** | 5 |
| bölge dışı (AF/tracker kodu) | 7 | 2 | 7 |

`InitializeStaticMetadataPool` birebir örtüşüyor. Diğer ikisinde sayı farkı
var (16 vs 13, 5 vs 6) → Faz 4'te bu fonksiyonlarda **körlemesine hepsini
yamalamak yerine** her noktanın komut bağlamı ayrı ayrı eşleştirilecek.

## Video ile ilgili bulgular (kullanıcı sorusu)

Yamalanan fonksiyonların içindeki string'ler tarandı:

- `InitializeScalerStaticCaps` → `supportedFPS= %d, BPS= %d, IPE/OPE= %d for
  width x height= %d x %d` — hangi çözünürlüğün hangi kare hızında
  desteklendiğini belirleyen yer.
- `GetSensorStaticCapability` → `Hiding mode[%d], forceMaxFPS: %f, resFPS: %f`
  — HAL'in sensör modlarını **gizleme** mantığı. Yamanın 5-6 noktası tam
  burada.

→ Yama, video için mod seçimini yapan kod yollarına **doğrudan dokunuyor**.
Video etkisi teorik değil, gerçek bir olasılık. Faz 4 sonrası ölçülecek.

**D grubu sabiti belirsizliği:** `973.078.528` → `486.539.264` (tam yarısı).
Karşılaştırmanın yönü (üst sınır mı, bölen mi) henüz kesin değil; Faz 4'te
bu bölgenin komut dizisi çözülerek netleştirilecek.

---

# Faz 4 bulguları

## Üretilen yama

| | |
|---|---|
| Stok A15 HAL | 27.268.688 bayt · md5 `c3fa63a86ee3ecaf9fbf02005d35f6b5` |
| **NİHAİ yamalı HAL** | 27.268.688 bayt · md5 `fe0245a4720fb07b01d96deef47f5569` |
| Değişen komut | **16** (yalnız `InitializeScalerStaticCaps` içinde) |
| Dönüşüm | `LDR Wn,[Xm,#0x3d84]` → `MOV Wn,#0` |
| (reddedilen ilk deneme) | 49 nokta · md5 `e816b0a2…` · **AGC'yi çökertti** |

## Yama kuralı ve doğrulaması

Kural: şu **dört fonksiyonun** gövdesi içindeki tüm `+0x3d84` okumalarını sıfırla.
Fonksiyon sınırları, log makrosunun fonksiyon-adı string'ine yapılan xref'lerden
ve çevreleyen `RET` komutlarından çıkarıldı.

- `InitializeStaticMetadataPool`
- `InitializeScalerStaticCaps`
- `GetSensorStaticCapability`
- `InitializeStaticMetaPoolXiaomiFovCrop`

**Kural A14 üzerinde körlemesine sınandı** (A14'ün gerçek yaması yer gerçeği):

| | |
|---|---|
| Kuralın seçtiği | 47 |
| Gerçekte yamalı | 48 |
| Yanlış seçilen | 1 (`0x0196EB44`) |
| Kaçırılan | 2 (nesne-takip AF kodu — **bilerek** dışarıda) |

İsabet %98. Yanlış seçilen tek noktanın A15'teki karşılığı imza aramasıyla
(K=6..3) **bulunamadı** → o kod bloğu A15'te farklı; A15'in 49 noktası meşru.

## Bilinçli olarak portlanmayanlar

- **C grubu** (`CMP Wn,#4`→`#5`, `B.EQ`→`B.NE`, `CMP W0,#2`→`CMP W0,W0`)
- **D grubu** (`973.078.528` → `486.539.264` kapasite sabiti)
- Nesne-takip AF kodundaki 2 nokta (`camxmitrackafnode.cpp`)

Gerekçe: en az değişkenle başlama ilkesi + kullanıcının video kaygısı.
Sonuç bunları gereksiz kıldı (aşağı bkz.).

## Cihaz doğrulaması (geçici bind mount ile)

**50MP açıldı:**

| | stok | yamalı |
|---|---|---|
| `android.scaler.availableStreamConfigurations` (cam 0) | int32[440] | **int32[456]** |
| En büyük OUTPUT | 4096 × 3072 | **8192 × 6144** |
| 8192×6144 formatları | — | **33 (JPEG)**, 34, 35, 54 |

Format 33 (BLOB/JPEG) OUTPUT olarak mevcut → AGC 50MP JPEG çekebilir.

**Video hiç bozulmadı:**

| Ölçüm | stok | yamalı |
|---|---|---|
| Kamera sayısı | 13 | 13 |
| `vendor_qti` blok | 27 | 27 |
| `CustomHFRFpsTable` | int32[104] | int32[104] (**birebir**) |
| 3840×2160 OUTPUT | 4 | 4 |
| 1920×1080 OUTPUT | 4 | 4 |
| 4096×2304 OUTPUT | 7 | 7 |

**4K60 ve 1080p60 tabloda yerinde.** D grubunu portlamama kararı doğrulandı —
o sabit taşınsaydı kapasite yarıya inecek ve bu satırlar düşebilecekti.

## AGC çökmesi ve kök nedeni — Faz 4'ün ikinci turu

İlk 49 noktalık yama AGC'yi (`org.codeaurora.snapcam`) çökertti:

```
java.lang.NullPointerException: Attempt to invoke virtual method
'boolean com.google.googlex.gcam.Gcam.f()' on a null object reference
```

GCam'in native HDR+ motoru hiç kurulamıyor → uygulama açılışta ölüyor.

**Kontrol deneyleri** (her biri ayrı ayrı ölçüldü):

| Kurulum | AGC |
|---|---|
| stok HAL + eski config | **çalışıyor** |
| stok HAL + 50MP config | **çalışıyor** |
| 49-nokta yama + 50MP config | **çöküyor** |
| **16-nokta yama (scaler) + 50MP config** | **çalışıyor** |

→ Çökmenin sebebi config değil, **yamanın kapsamı**.

**Kök neden:** `InitializeStaticMetadataPool` ve `InitializeStaticMetaPoolXiaomiFovCrop`
yamalandığında `activeArraySize`, `pixelArraySize` ve
`preCorrectionActiveArraySize` 4096×3072'den **8192×6144'e** çıkıyor. GCam'in
native motoru kendi sensör modelini bu diziye göre kuruyor ve 50MP'lik aktif
diziyle başlatılamıyor.

**Çözüm:** 50MP'nin üçüncü parti uygulamalara görünmesi için sensör aktif
dizisini değiştirmeye **gerek yok** — yalnızca standart stream listesine
eklenmesi yeterli. Bunu yapan tek fonksiyon `InitializeScalerStaticCaps`.

## Nihai doğrulama (16 noktalı yama)

| Ölçüm | stok | 49 nokta | **16 nokta** |
|---|---|---|---|
| 8192×6144 JPEG (format 33) | yok | var | **var** |
| `availableStreamConfigurations` | int32[440] | int32[456] | **int32[456]** |
| `CustomHFRFpsTable` | int32[104] | int32[104] | **int32[104]** |
| 3840×2160 / 1920×1080 OUTPUT | 4 / 4 | 4 / 4 | **4 / 4** |
| `activeArraySize` | 4096×3072 | 8192×6144 | **4096×3072** |
| `preCorrectionActiveArraySize` | 4096×3072 | 8192×6144 | **4096×3072** |
| AGC | çalışıyor | **çöküyor** | **çalışıyor** |

16 noktalı yama, stok metadata'sını **tek bir alan dışında** hiç değiştirmiyor:
yalnızca stream listesine 50MP giriyor. Video tarafı tamamen dokunulmamış.

## AGC yapılandırması

`50mpx_agc_config.agc` düz `<map>` kök etiketli XML — yani doğrudan Android
shared_prefs biçimi. Uygulama içi yükleme yerine doğrudan yazıldı:

- Hedef: `/data/data/org.codeaurora.snapcam/shared_prefs/org.codeaurora.snapcam_preferences.xml`
- Orijinal ayarlar `…_preferences.xml.orig` olarak yedeklendi
- Sahip `10447:10447`, mod `660`, context `u:object_r:app_data_file:s0:c191,c257,c512,c768`
- Her iki config `/sdcard/GCam/Configs7/` altına da kopyalandı (elle geçiş için)

50MP config'in 12MP'den farkı: renk işleme tüm modüllerde açık, kare sayıları
21'e sabitlenmiş, native motor `shgv180.so` → `shgv181.so`.
**Çözünürlük ayarları iki config'te birebir aynı** (`pref_camera_resolution=full`,
`pref_fix_resolution_key=0`) → config 50MP'yi zorlamıyor, yalnızca görüntü
işleme profili. 50MP tamamen HAL'e bağlı.

## AGC'nin 50MP sınırı — bisection sonuçları

Cihazda ölçülen çekim: **3378×4504 = 15,2 MP** (yamasız hâlde 3072×4096 = 12,6 MP).
Yani yama etki ediyor ama GCam 8192×6144 stream'ini kullanmıyor;
4096×3072'yi ~1,1× ölçekliyor.

`activeArraySize`'ı büyütmek için hangi noktaların gerektiğini bulmak üzere
altı varyant cihazda tek tek denendi:

| Varyant | Nokta | AGC | `activeArraySize` |
|---|---|---|---|
| `scaler` | 16 | **çalışıyor** | 4096×3072 |
| `scaler+sensor` | 21 | çalışıyor | 4096×3072 |
| `scaler+fovonly` | 20 | çalışıyor | 4096×3072 |
| `scaler+metaA` (ilk yarı) | 28 | çalışıyor | 4096×3072 |
| `scaler+metaB` (son yarı) | 28 | çalışıyor | 4096×3072 |
| `scaler+fov` (meta tam) | 44 | **çöküyor** | 8192×6144 |
| tümü | 49 | **çöküyor** | 8192×6144 |

**Sonuç:** `activeArraySize`'ın 8192×6144 olması için `meta` bölgesinin
**tamamı** gerekiyor (yarıları tek başına yetmiyor), ve tam olduğunda AGC
çöküyor. İkisi ayrıştırılamıyor.

→ **GCam'in native motoru 50MP'lik aktif sensör dizisiyle başlatılamıyor.**
Bu HAL'in değil, GCam 8.4'ün kendi sınırı. AGC ile tam 50MP bu yolla
elde edilemez; ulaşılan üst sınır 15,2 MP.

## Video — cihazda kullanıcı tarafından doğrulandı

`scaler` (16 nokta) yamasıyla **1080p60 ve 4K60 sorunsuz kaydediyor.**
Faz 3'teki metadata öngörüsü gerçek kullanımda teyit edildi.

## OpenCamera alternatifi

`OpenCamera_50MP_HEIC_Video_10Bit_HLG_8K.apk` kuruldu. Gerçek paket adı
**`com.xiaomi.module.evaluation`** (Xiaomi'nin kendi değerlendirme uygulaması
kimliği) — APK içindeki `net.sourceforge.opencamera` yalnızca sınıf yolu.
Açılıyor, çökmüyor, Camera 0 oturumu kuruluyor.

### Kritik karşılaştırma — yama gerekli mi? (cihazda ölçüldü)

Aynı uygulama, aynı ayar (menüde 50MP seçili), tek değişken HAL:

| HAL | OpenCamera çıktısı |
|---|---|
| **yamalı** `fe0245a4…` | **8192×6144 = 50,3 MP** · 5.122.504 bayt |
| **stok** `c3fa63a8…` | **4096×3072 = 12,6 MP** · 1.878.743 bayt |

**Sonuç: yama zorunlu.** APK'nın "root ve mod gerektirmeden 50MP" iddiası bu
ROM'da geçerli değil. Menüde 50MP **görünüyor** (uygulama `quadra_cfa` vendor
tag'inden okuyor), seçilebiliyor, ama HAL yamasızken çıktı **sessizce**
12,6 MP'ye düşüyor — hata vermiyor, kullanıcı fark etmiyor.

Bu, Faz 2 teşhisini birebir doğruluyor: 50MP yalnızca vendor tag'inde
duyuruluyor; uygulama listeleyebiliyor ama HAL stream'i gerçekten 50MP
yapılandırmıyor. Standart listeye ekleyen tek şey `InitializeScalerStaticCaps`
yaması.

### Nihai yetenek tablosu

| Uygulama | yamasız | 16 noktalı yama ile |
|---|---|---|
| OpenCamera (`com.xiaomi.module.evaluation`) | 12,6 MP | **50,3 MP** |
| AGC (`org.codeaurora.snapcam`) | 12,6 MP | 15,2 MP |
| Video 1080p60 / 4K60 | çalışıyor | **çalışıyor** |

## Mount yığını hatası ve kalıcı düzeltme

Test döngüsünde `mount --bind` üst üste çalıştırıldığı için hedef üzerinde
**mount yığını** oluştu; tek `umount` yalnızca en üsttekini kaldırdığı için
"stok'a dönüldü" sanılan durumda dosya hâlâ yamalıydı. Modüle girecek
`umount` mantığı bu yüzden **sayaç sıfırlanana kadar döngüyle** çalışmalı:

```sh
while grep -q " $TGT " /proc/1/mountinfo; do umount $TGT || break; done
```

---

# Faz 5 bulguları

## Eklenen / değişen dosyalar

| Dosya | Durum | Ne yapıyor |
|---|---|---|
| `halpatch.sh` | **yeni** | Ortak HAL katmanı: `hal_seed`, `hal_write`, `hal_set`, `hal_state`, `hal_umount_all` |
| `blobs/hal-fullres.patch` | **yeni** | 16 noktalık yama listesi, **1.144 bayt** (27 MB blob yerine) |
| `post-fs-data.sh` | değişti | HAL md5 kilidi → kopya üret → yamala → bind mount |
| `setmode.sh` | değişti | `50mp` modu; HAL yazımı `restart_camera` içinde |
| `action.sh` | değişti | `50mp`; `active()` önce HAL'e bakar; `info` 5. alan |
| `webroot/index.html` | değişti | 50MP butonu (EN/TR), uyarı metni güncellendi |
| `module.prop` | değişti | **v2.0** / versionCode 11 |

## Tasarım

**Neden 27 MB blob yok:** cihazdaki stok HAL `active_hal/` altına kopyalanır ve
16 noktası yamalanır. Kopya **her zaman** bind mount edilir; 50MP kapalıyken
içeriği stokla birebir aynıdır (md5 eşit), yani davranış değişmez. Mod
değiştirmek mount'a dokunmadan 16×4 bayt yazmak demektir — sensör katmanında
kanıtlanmış desenin aynısı.

**HAL yazımı yalnızca `restart_camera` içinde**, servislerin tamamı durmuşken
yapılır: `camera.qcom.so` çalışan sürece mmap'li olduğu için ayaktayken
değiştirmek çökertir.

**Dışlama:** `50mp` → sensör `stock` + HAL `fullres`; diğer modlar → sensör
yamalı + HAL `stock`.

## Karşılaşılan problemler

**1. İlk yama yazımı dosyayı bozdu — en ciddi hata.**
`hal_write` baytları iç içe `printf "\\$(printf '%03o' $b)"` ile üretiyordu.
Toybox kabuğunda **komut ikamesi çözülmedi**; dosyaya `printf`'in kendi metni
yazıldı (`intf '000'…`). Sonuç: 16 nokta yerine **288 bayt** bozuldu, HAL
`unknown` duruma düştü ve kamera bozuk bir ikiliyle mount edildi.
Cihazdan çekip stok ile bayt bayt karşılaştırarak teşhis edildi:
*doğru yazılan 0/16, fazladan yazılan 272*.
**Çözüm:** yama listesi baytları **hazır octal escape dizisi** olarak tutuyor
(`\021\207\175\271`) ve tek bir `printf '%b'` ile yazılıyor — iç içe ikame yok,
`%` sorunu yok. Ofsetler 4'ün katı olduğu için `dd bs=4 seek=<indeks> count=1`
kullanılıyor. Yeniden ölçüldü: `fullres` → `fe0245a4…`, `stock` → `c3fa63a8…`,
süre **0 sn**.

**2. Kaynak dosyaya karışık alfabe karakteri girdi.** `post-fs-data.sh`
yorumuna Kiril harf karıştı. Tüm script'ler `LC_ALL=C grep '[^ -~]'` ile
tarandı; artık ASCII dışı karakter yok.

**3. Mount yığını** (Faz 4'ten): `hal_umount_all` sayaç sıfırlanana kadar
döngüyle kaldırıyor.

## Cihazda entegrasyon testi

| Test | süre | sensör | HAL | stream listesi | whiteLevel |
|---|---|---|---|---|---|
| `setmode.sh 50mp` | 12 sn | stock | **fullres** | int32[**456**] | — |
| `setmode.sh dcgB` | 10 sn | dcgB | **stock** | int32[440] | **4095** (12-bit) |
| `setmode.sh stock` | ~10 sn | stock | stock | int32[440] | 1023 |

`action.sh info` → `50mp\|aktif\|…\|en\|fullres`
`action.sh list` → `stock 50mp ln2 ln4 ln2s ln4s ln2f ln4f dcgA dcgB`
İlk kopya üretimi (27 MB) **1 sn**; mod değişimi mevcut modlarla aynı sürede.

---

# Faz 6 bulguları

## Eklenen / değişen dosyalar

| Dosya | Ne oldu |
|---|---|
| `tile-app/res/drawable/ic_50mp.xml` | **yeni** — klasik fotoğraf makinesi silueti |
| `tile-app/java/.../FullResTile.java` | **yeni** — `50mp` modunu süren kutucuk |
| `tile-app/java/.../BaseTile.java` | `TILES` dizisi, `pretty("50mp") → "50MP"` |
| `tile-app/res/values/strings.xml` | `tile_50mp` = "50MP" |
| `tile-app/AndroidManifest.xml` | 4. servis; versionCode 8→9, versionName 1.7→**2.0** |
| `service.sh` / `action.sh` | kurulum listesine `FullResTile` |
| `module.prop` | 4 kutucuk açıklaması |
| `tile-app.apk` | yeniden derlendi, **21.156 bayt** |

APK **aynı anahtarla** imzalandı (SHA-256 `51d1eb54…`), bu yüzden
`pm install -r` yerinde yükseltme yapıyor; kök yetkisi ve kutucuk yerleşimi
korunuyor. Cihazda doğrulandı: versionCode 8 → 9, `kok_kaydi=var`.

## Tasarım

Kutucuk sayısı artık **tek yerde** tanımlı (`BaseTile.TILES`). Kardeş
uyandırma döngüsü ve "hepsi bağlı mı" eşiği (`live >= TILES.length`) bu
diziden türetiliyor; önceki kodda eşik sabit `3` idi ve 4. kutucuk
eklenince sessizce yanlış davranırdı.

Karşılıklı dışlama için **ek kod yazılmadı** — mevcut yayın mekanizması
zaten yeterli: `action.sh get` tek bir mod adı döndürüyor, `apply()` yalnız
`current.equals(mode())` olan kutucuğu ACTIVE yapıyor. 50MP HAL katmanında,
DCG/LN sensör katmanında olduğu hâlde kutucuklar açısından hiçbir fark yok.

## İkon

Material `photo_camera` çizimi: gövde + vizör çıkıntısı + objektif halkası,
iki `path` (gövde delikli, mercek dolu). Kardeş ikonlar (`ic_dcg`, `ic_ln2`,
`ic_ln4`) soyut daire kademeleri; 50MP tam çözünürlüklü **fotoğraf** demek
olduğu için bilerek tanınabilir bir siluet seçildi. Ekran görüntüsüyle
doğrulandı — QS panelinde düzgün çiziliyor.

## Cihazda kutucuk testi

`cmd statusbar click-tile` ile gerçek dokunuş simüle edildi (kullanıcı
eylemi gerekmedi):

| Test | Başlangıç | Sonuç | Doğrulama |
|---|---|---|---|
| 50MP kutucuğu | `50mp` / fullres | `stock` / stock | tek dokunuş, ~12 sn |
| 50MP kutucuğu | `stock` / stock | `50mp` / fullres | kutucuk anında vurgulandı |
| DCG kutucuğu (50MP açıkken) | `50mp` / fullres | `dcgB` / **stock** | 50MP kutucuğu kendiliğinden söndü |

Kamera cihaz sayısı her testten sonra **13** — yığın sağlam.
HUD bildirimi logcat'te doğrulandı: `type = 2038` (TYPE_APPLICATION_OVERLAY)
penceresi açılıp **12,5 sn** sonra kapanıyor.

## Karşılaşılan problemler

**1. Ekran görüntüsü HUD'u yakalamıyor.** İlk testte bildirim görünmedi ve
çalışmadığı sanıldı. `adb exec-out screencap` overlay katmanını almıyor;
`dumpsys window` ve appop süresi (`SYSTEM_ALERT_WINDOW … duration=+12s468ms`)
bildirimin gerçekte çalıştığını kanıtladı. Kod değişikliği gerekmedi.

**2. `click-tile` bağlı olmayan kutucuğa ulaşmıyor.** QS paneli kapalıyken
gönderilen dokunuş hemen düşmüyor, kutucuk bağlanınca gecikmeli geliyor. İki
dokunuş üst üste binince mod iki kez değişti ve ölçüm yanıltıcı oldu. Bu
yalnızca adb yoluna özgü; `setmode.sh` içinde zaten 90 sn'lik kilit
(`lock_acquire`) var, yani eşzamanlı iki mod değişimi gerçekten çalışmıyor.
Testler QS paneli açıkken ve bekleyen işler boşaltılarak tekrarlandı.

**3. Hayalet kutucuk kaydı.** `sysui_qs_tiles` ayarında APK'da karşılığı
olmayan `com.ishtar.cammodes/.FiftyTile` girdisi duruyor (geliştirme
artığı). SystemUI çözemediği bileşeni panelde **çizmiyor** — ekran
görüntüsünde dört kutucuk var — ama ayardan da silmiyor: `remove-tile`,
`set-tiles` ve doğrudan `settings put` üçü de rc=0 dönüp değişiklik
yapmıyor, çünkü SystemUI listeyi bellekten geri yazıyor. Görünür etkisi yok;
temizlenmesi ancak SystemUI yeniden başlatılarak mümkün.

## Açık kalan (Faz 7'ye)

- Başlatıcı takma adı hâlâ `gorunur` — çekmecede gizleme Faz 7'de.
- APK modül kökünde duruyor; zip'e gömme Faz 7'de.

---

# Faz 7 bulguları

## Başlatıcı gizleme — regresyonun kök nedeni

v1.9'da kural şuydu: `hide_launcher` dosyası varsa gizle, yoksa göster. O
dosyayı **hiçbir şey oluşturmuyordu** — kullanıcı elle `tiles hide`
çalıştırmadıkça uygulama çekmecede kalıyordu. Yani gizleme bozuk değildi,
hiç tetiklenmiyordu.

Yeni kural `action.sh:launcher_sync()` içinde, tek yerde:

| Durum | Sonuç |
|---|---|
| `show_launcher` var | görünür (kullanıcı bilerek istedi) |
| `hide_launcher` var | gizli (kullanıcı bilerek gizledi) |
| ikisi de yok, **kök kaydı var** | **gizli** (otomatik) |
| ikisi de yok, kök kaydı yok | görünür (yetki verilebilsin diye) |

Kök yetkisi `/data/adb/ksu/.allowlist` içinden okunuyor. Kural iki yerden
tetikleniyor: her açılışta (`service.sh`) ve **her mod değişiminden sonra**
(`apply()`). İkincisi önemli — o satıra ulaşmak kök yetkisinin verildiğini
kanıtlıyor, çünkü script `su` ile çalışmış oluyor. Böylece kullanıcı yetkiyi
verdikten sonra ilk kutucuk dokunuşunda uygulama kendiliğinden kayboluyor;
yeniden başlatma beklemek gerekmiyor.

Son uygulanan durum `.launcher` dosyasında tutuluyor, gereksiz `pm` çağrısı
yapılmıyor. `pm install` bileşen durumlarını manifest varsayılanına
döndürdüğü için kurulum sırasında bu önbellek geçersiz kılınıyor.

**Cihazda doğrulandı:** `resolve-activity` → *No activity found*, yani
uygulama çekmecede yok; buna rağmen kutucuğa dokunuş çalışıyor (kök yetkisi
UID'ye bağlı, başlatıcıdan bağımsız).

## APK güncelleme tespiti — sürüm numarası tutmadan

Android APK'yı olduğu gibi `/data/app/...` altına kopyaladığı için kurulu
dosyanın md5'i modüldekiyle **birebir aynı** (cihazda doğrulandı). Bu yüzden
`tiles install` ayrı bir sürüm dosyası tutmuyor:

```
apk_installed_md5() { P=$(pm path "$PKG" | sed -n 's/^package://p' | head -1); md5of "$P"; }
```

Farklıysa `pm install -r`, aynıysa hiçbir şey. v1.9'da yalnızca paket **yoksa**
kuruluyordu; yeni bir zip flaşlansa bile kutucuk uygulaması eski kalırdı —
bu da düzeldi. Cihazda ölçüldü: `apk=eski` → `guncellendi` → `apk=guncel`.

## Kutucuk sırası

`cmd statusbar add-tile` listenin **başına** ekliyor (cihazda ölçüldü). Bu
yüzden `TILE_ADD_ORDER` istenen sıranın tersi: `Ln2Tile Ln4Tile DcgTile
FullResTile` → panelde **50MP · DCG · LN4 · LN2**, WebUI'deki sırayla aynı.

Kutucuklar **yalnızca ilk kurulumda** ekleniyor; güncellemede eklenseydi
kullanıcının Hızlı Ayarlar düzeni her açılışta bozulurdu. Sırayı yeniden
dizmek isteyen `action.sh tiles order` çalıştırır.

## Uygulama simgesi

`ic_50mp.xml` → `ic_camera.xml` olarak yeniden adlandırıldı ve **üç yerde**
kullanılıyor: 50MP kutucuğu, uygulama simgesi, başlatıcı takma adı. DCG
kutucuğu kendi simgesini koruyor. İsim glife göre verildi çünkü artık tek
bir moda ait değil.

## Flash edilebilir zip

`ishtar-cam-modes-v2.0.zip` — **1.002.425 bayt, 39 dosya**. APK (21.158
bayt) pakete gömülü. Dışarıda bırakılanlar:

- `active/`, `active_hal/` — çalışma zamanında üretiliyor (27 MB'lik HAL
  kopyası ilk açılışta 1 saniyede seed ediliyor)
- `tile-app/out/`, `debug.keystore` — derleme artığı ve imza anahtarı
- **`mode` ve `lang`** — pakete konsaydı her güncellemede kullanıcının modu
  ve dili sıfırlanırdı. Yokken varsayılanlar zaten devreye giriyor
  (`post-fs-data.sh` → stock, `action.sh lang` → en); cihazda doğrulandı.

## Kurulum betiği cihazda sınandı

`customize.sh`, canlı modüle dokunmadan gerçek cihazda çalıştırıldı
(Magisk/KernelSU kurulum API'si taklit edildi). Çıkış kodu 0, izinler doğru
(scriptler 0755, blob'lar 0644).

**Simülasyon gerçek bir hata yakaladı:** eklediğim HAL sürüm kontrolü
`/odm/lib64/hw/camera.qcom.so` okuyor, ama modül kuruluyken orada **bizim
yamalı kopyamız bağlı**. Sonuç: 50MP açıkken yeniden flaşlayan kullanıcıya
"HAL sürümü farklı, 50MP devre dışı" yazacaktı. Düzeltildi — hem stok hem
fullres md5'i geçerli sayılıyor ve hangisi olduğu ayrı ayrı yazdırılıyor.

## Doğrulanmamış tek şey

Zip **gerçekten flaşlanmadı**. Kullanıcının günlük telefonu olduğu ve modül
dizini baştan kurulacağı için bu adım onaya bırakıldı. Aynı yeniden
başlatma, Faz 5'ten beri açık duran diğer maddeyi de kapatacak:
`post-fs-data.sh`'in HAL bloğu şimdiye kadar yalnızca **simüle** edildi,
gerçek açılış bağlamında çalıştırılmadı.

---

# Faz 8 bulguları — cihazda 50MP doğrulaması

Zip kullanıcı tarafından flaşlandı ve cihaz yeniden başlatıldı. Faz 5 ve
Faz 7'den kalan açık maddeler böylece kapandı: `post-fs-data.sh`'in HAL
bloğu **gerçek açılışta** çalıştı.

## 50MP çalışıyor — taze ölçüm

| Dosya | Koşul | Çözünürlük |
|---|---|---|
| `IMG_20260820_165720.jpg` | mod kapalı | 4096×3072 = 12,6 MP |
| `IMG_20260820_205842.jpg` | **50mp modu** | **8192×6144 = 50,3 MP** |
| `IMG_20260820_205916.jpg` | **50mp modu** | **8192×6144 = 50,3 MP** |

Çekim uygulaması: `com.xiaomi.module.evaluation` — aslında **Open Camera**
(etkinlik `net.sourceforge.opencamera.MainActivity`), Xiaomi paket adıyla
yeniden paketlenmiş. Çekim `net.sourceforge.opencamera.TakePhoto`
etkinliğiyle adb üzerinden tetiklendi, telefona dokunulmadı.

Bu açılışta HAL durumu: `/odm/lib64/hw/camera.qcom.so` md5 `fe0245a4…`,
bind mount `/proc/1/mountinfo`'da mevcut, `android.scaler.availableStreamConfigurations`
= `int32[456]` ve içinde `[33 8192 6144 OUTPUT]` var.

## AGC neden hâlâ 15,2 MP — kesin açıklama

Kullanıcı "fotoğraflar hâlâ 12,6 MP" diye bildirdi; ölçüldüğünde dosya
**3378×4504 = 15,2 MP** çıktı. AGC ayarlarında görünen "12,6 MP" sensörden
gelen boyut, dosyadaki ise onun ölçeklenmiş hâli. İkisi arasındaki ilişki
AGC'nin kendi ayar dosyasından birebir doğrulandı:

| Anahtar | Değer |
|---|---|
| `pref_camera_picturesize_back_key` | `4096x3072` |
| `pref_upscale_key_0` | `11` (= 1,1×) |

4096 × 1,1 = 4504 · 3072 × 1,1 = 3378 → **tam olarak çıktı boyutu.**

### Denenen iki müdahale

**1. Resim boyutunu elle 8192x6144 yapmak.** Ayar dosyasına yazıldı
(`cat >` ile, inode/sahip/SELinux bağlamı korunarak). AGC açılışta değeri
**sessizce 4096x3072'ye geri çevirdi** → 8192×6144 kendi aday listesinde yok.

**2. Çekim akışını RAW10 → YUV yapmak.** Standart listede 8192×6144'te RAW
formatı yok (37/36/32 en fazla 4096×3072), ama YUV (35) **var**. Hipotez:
GCam adayları RAW bulunabilirliğine göre eliyor. `pref_raw_key_0` ve
`pref_fix_resolution_key_0` 37 → 35 yapıldı.
Sonuç: **format değişikliği kalıcı oldu** (AGC kabul etti), fakat resim
boyutu yine 4096x3072'ye döndü. → **Eleme kriteri RAW değil.**

Not: donanım tam çözünürlükte RAW verebiliyor, ama yalnızca Xiaomi'nin özel
etiketinde duyuruluyor:
`xiaomi.scaler.availableStreamConfigurations` → `[37 8192 6144 0]`,
`[36 8192 6144 0]`. QCFA vendor etiketinde ise yalnızca 33/34/35 var — 16
noktalık yama QCFA tablosunu akıttığı için standart listeye RAW giremiyor.

### Sonuç

Geriye tek aday kalıyor: **`activeArraySize` (4096×3072) sınırı.** Faz 4'ün
bisection'ı bunu büyütmenin AGC'yi çökerttiğini zaten göstermişti
(`Gcam.f()` null → native motor kurulamıyor). İki koşul birbirini dışlıyor:

- AGC'nin 50MP'yi *önermesi* için `activeArraySize` ≥ 8192×6144 gerekiyor
- `activeArraySize` = 8192×6144 olduğunda GCam 8.4 motoru **açılışta ölüyor**

→ **GCam 8.4 ile 50MP bu HAL üzerinden elde edilemez.** Faz 4'ün sonucu
ikinci ve bağımsız bir yoldan doğrulandı. AGC'nin tavanı 15,2 MP.

`pref_fix_spatial_gain_map_key_0` zaten `1` — yani lens gölgeleme telafisi
Faz 4'teki çökme testinde de açıktı; yeni bir kaldıraç değil.

## Karşılaşılan problemler

**1. Yanlış teşhis riski.** İlk bakışta "flaş sonrası gerileme" gibi
duruyordu. Dosya ölçülmeden konuşulsa 12,6 MP kabul edilecekti; ölçüm
15,2 MP gösterdi ve bu Faz 4'te belgelenen değerin **aynısı** — gerileme yok.

**2. Başka uygulamanın ayar dosyasına yazmak.** `sed -i` inode'u
değiştirip SELinux bağlamını düşürürdü. `sed … > tmp && cat tmp > hedef`
kullanıldı; sahip `u0_a447`, mod `660` ve bağlam
`…app_data_file:s0:c191,c257,c512,c768` korundu. Testten sonra tüm ayarlar
`.pre50mp` yedeğinden geri yüklendi (boyut 111.468 bayt, `pref_raw_key_0`
yeniden `37`).

**3. `find -newermt` toybox'ta çalışmıyor.** Open Camera fotoğrafları
`DCIM/OpenCamera/` altına düştüğü hâlde "dosya yok" sonucu verdi;
`ls -lt` ile bulundu. Zaman filtresi yerine dizin listesi kullanıldı.

**4. Git Bash yol dönüşümü.** `adb pull /sdcard/...` yolu
`C:/Program Files/Git/sdcard/...` diye yeniden yazıldı.
`MSYS_NO_PATHCONV=1` ile çözüldü.

## Yeni AGC yapısı — aynı sonuç (2026-08-22)

Kullanıcı, AGC geliştiricisinin daha güncel yamalarını içeren bir yapı
kurdu (`versionName` yine `8.4.300.414775575.18`, `lastUpdateTime` 21:19,
yeni UID `u0_a448`, ayarlar varsayılana döndü — port config'i yüklü değil).

| Deneme | Sonuç |
|---|---|
| Varsayılan çekim | **3072×4096 = 12,6 MP** (ölçek anahtarı yok → 1,0×) |
| `pref_camera_picturesize_back_key` = `8192x6144` | AGC yine **4096x3072'ye geri çevirdi** |

→ Yeni yapı da 8192×6144'ü aday listesine almıyor. GCam 8.4 tavanı
sürüm yamalarıyla aşılamıyor; sınır motorun `activeArraySize` modelinde.
Ayarlar testten sonra `.bak50` yedeğinden geri yüklendi.

Not: bu yapıda `pref_upscale_key_0` bulunmadığı için çıktı 15,2 MP değil
tam 12,6 MP. Yani kullanıcının ilk bildirdiği "12,6 MP" bu yeni yapı için
**doğru**; önceki yapıda ise dosya 15,2 MP idi.

## Mod geçişi gerilemesi — flaş sonrası

Dört mod arka arkaya uygulandı, her adımda kamera sayısı ölçüldü:

| Mod | rc | süre | sensör md5 | HAL | kamera cihazı |
|---|---|---|---|---|---|
| `dcgB` | 0 | 12 s | `ee73da4e` = `dcgB.bin` | stock | **13** |
| `ln4` | 0 | 13 s | `fd959e19` = `ln4.bin` | stock | **13** |
| `ln2` | 0 | 11 s | `8dbc3f52` = `ln2.bin` | stock | **13** |
| `50mp` | 0 | 10 s | `9e4d0fe1` = `stock.bin` | **fullres** | **13** |

Karşılıklı dışlama doğrulandı: 50mp modunda sensör blob'u **stok** kalıyor
(50MP yalnızca HAL katmanı), DCG/LN modlarında HAL **stoka** dönüyor.

**CSIPHY/IFE sızıntısı yok.** Loglardaki `CSIPHYHw … AvailableResource`
satırları INFO seviyesi kaynak dökümü; `serviceDied` ise mod değişiminde
kamera yığınının bilerek yeniden başlatılması. `OverrideMipiPhyData() fail
to open /sys/csiphy_umd_paras/…` MIUI'ye özgü bir sysfs düğümünü arayan
Xiaomi HAL'inden geliyor, AOSPA'da her zaman yok — modülle ilgisiz.

Tam döngüden sonra 50MP hâlâ çalışıyor ve dosyalar sağlam:

| Dosya | Çözünürlük | SOI/EOI |
|---|---|---|
| `IMG_20260820_205842.jpg` | 8192×6144 = 50,3 MP | ok / ok |
| `IMG_20260820_205916.jpg` | 8192×6144 = 50,3 MP | ok / ok |
| `IMG_20260822_222923.jpg` | 8192×6144 = 50,3 MP | ok / ok |

## Başlatıcı simgesi — çerçeve değil, önbellek

Kullanıcı simgenin çekmecede hâlâ göründüğünü bildirdi. Ölçüm:

- `action.sh tiles status` → `baslatici=gizli (otomatik) kok_kaydi=var`
- `.launcher` dosyası → `disable`
- `pm dump` → `disabledComponents: com.ishtar.cammodes.Launcher`
- `pm resolve-activity` → *No activity found*
- `cmd package query-activities -a MAIN -c LAUNCHER | grep -c cammodes` → **0**

Manifest'te LAUNCHER kategorisi taşıyan **tek** bileşen `.Launcher` takma
adı; `WebUiActivity` yalnızca `QS_TILE_PREFERENCES` + `DEFAULT` taşıyor,
yani ikinci bir giriş noktası yok. Çerçeve açısından simge yok.

→ Kalan tek açıklama **başlatıcı önbelleği**. Varsayılan başlatıcı
`com.android.launcher3` (`co.aospa.launcher.ParanoidQuickstepLauncher`);
`am force-stop com.android.launcher3` ile yeniden başlatıldı.
Kullanıcı onayı bekleniyor.

---

# Faz 9 bulguları — düzeltmeler ve paketleme (2026-08-22)

## Çekmecedeki simge: özellik çalışmıyormuş

Faz 7'de gizleme "çalışıyor" sayılmıştı çünkü yalnızca **çerçeveye**
soruldu (`pm resolve-activity` → *No activity found*). Ekran görüntüsü hiç
alınmamıştı. Alındığında görüldü ki:

| Takma ad | Çekmecede | Dokununca |
|---|---|---|
| kapalı | **görünüyor** | `com.android.settings/.spa.SpaActivity` (ölü girdi) |
| açık | görünüyor | `com.rifsxd.ksunext/.ui.webui.WebUIActivity` (çalışıyor) |

Elenen açıklamalar:

- **İkinci bir giriş noktası?** Yok. Manifest'te LAUNCHER kategorisi taşıyan
  tek bileşen `.Launcher`; `WebUiActivity` yalnızca `QS_TILE_PREFERENCES`.
- **Bileşen gerçekten kapalı mı?** Evet: `pm dump` →
  `disabledComponents: com.ishtar.cammodes.Launcher`, `am start` →
  *does not exist*, `query-activities … LAUNCHER` → 0.
- **Bayat önbellek mi?** Hayır. `am force-stop com.android.launcher3`,
  `pm enable` → `pm disable` döngüsü ve **taze `pm install -r`** (başlatıcı
  modelinin tazelendiği simgenin değişmesiyle kanıtlandı) — üçünden sonra da
  girdi duruyor.

→ **AOSPA Launcher3, takma ad `pm disable` ile kapatılsa da uygulamayı
çekmecede tutuyor.** Gizlemenin tek etkisi girdiyi işlevsiz bırakmak.
Bu yüzden varsayılan **GÖRÜNÜR** yapıldı; `tiles hide` elle seçenek olarak
kaldı (başka başlatıcılarda işe yarayabilir).

## Uygulama simgesi boş görünüyordu

Çekmecedeki simge **boş beyaz daire** idi. Sebep: Faz 6'da uygulama ikonu
olarak kutucuk çizimi `ic_camera` kullanılmıştı ve onun tint'i
`?android:attr/colorControlNormal`. Başlatıcı bağlamında bu **beyaza**
çözülüyor, eski simge de beyaz daire zeminine oturunca beyaz üstüne beyaz
kalıyordu.

Düzeltme: uyarlanabilir simge (`mipmap-anydpi-v26/ic_launcher.xml`) —
koyu zemin (`#FF263238`) + tint'siz beyaz siluet, 24×24'ten 108×108'e
`scale 2.5 / translate 24` ile ölçeklenmiş (24..84 aralığı, güvenli bölge
içinde). `<application>` ve `.Launcher` bu ikonu kullanır; **FullResTile
kutucuğu `ic_camera`'yı korur** — orada tint doğru davranış.
Ekran görüntüsüyle doğrulandı.

## `launcher_sync` dayanıklılık hatası

Kural son uygulanan durumu `.launcher` dosyasında tutup aynıysa `pm`
çağrısını atlıyordu. Bileşen durumu dışarıdan değişirse (uygulama
güncellemesi, elle `pm enable`) modül bir daha **düzeltmiyordu**.
Önbellek tamamen kaldırıldı; kural her çağrıda uygulanıyor (etkisiz bir
`pm enable/disable` bedava). `show_launcher` işareti de gereksizleşti ve
silindi — varsayılan zaten görünür.

`tiles status` artık durumu tahmin etmiyor, **çerçeveye soruyor**
(`launcher_state()`). İlk yazdığım desen (`grep "$PKG/"`) hatalıydı: çıktı
`name=com.ishtar.cammodes.Launcher` biçiminde, **eğik çizgi yok**; bu yüzden
açıkken bile "gizli" diyordu. `name=$PKG\.Launcher` ile düzeltildi ve her
iki yönde de sınandı.

## Doğrulamalar

| Öğe | Sonuç |
|---|---|
| WebUI | açılıyor, aktif mod `50mp`, dört kutucuk, EN/TR anahtarı |
| Dil | `en`, sistem dilinden bağımsız |
| Geri sayım | kutucuğa dokununca katman canlı (`running`), `duration=+14s398ms` |
| Mod değişimi | `50mp ↔ dcgB` doğru, blob md5'leri eşleşiyor |
| `tiles status` | `gorunur (varsayilan) kok_kaydi=var kutucuk=5` |

Not: `action.sh set` doğrudan kabuktan çağrılınca **HUD çıkmaz** — geri
sayımı kutucuk uygulaması çizer, kabuk yolu uygulamayı hiç devreye sokmaz.
İlk ölçümde bu yanlış alarma yol açtı.

## Paketleme

| | |
|---|---|
| `tile-app.apk` | 25.507 bayt, aynı imza (`51d1eb54…`) → yerinde yükseltme |
| `module.prop` | v2.1, versionCode 12 |
| `ishtar-cam-modes-v2.1.zip` | **1.006.606 bayt, 42 dosya**, bütünlük sağlam |

`mode` ve `lang` yine **bilerek dışarıda** — pakete girselerdi her
güncellemede kullanıcının modu ve dili sıfırlanırdı.

Metinler yeni AGC ölçümüne göre güncellendi (WebUI EN+TR, `module.prop`,
`Kullanim.txt`, `customize.sh`): artık "AGC 15,2 MP'de kalır" değil,
"12,6–15,2 MP; GCam 8.4 motoru 50MP akışını seçemiyor".

---

# Faz 11 — AGC APK yaması: 50MP akışının açılması (2026-08-23)

Hedef: `AGC8.4.300_V9.6_snap.apk` (config geliştiricisinin şart koştuğu sürüm)
yamalanarak AGC'den 50MP çıktı almak. Cihazdaki AGC v9.6 ile değiştirildi
(md5 `fa4066eb3bf82cc097906fd108073500`, iki taraf da aynı).

## Kök neden — ölçüldü, tahmin değil

Zincir tamamen izlendi:

```
Lhvg;->a()                (ResolutionSetting)
  -> Llwe;->x(256)        (JPEG boyut listesi)
    -> Llvo;->x(256)
      -> LAGC;->getSupportedOutputSizes(256, map)      <-- portun kancası
        -> map.getOutputSizes(256)
```

`Lmip;->bs()` bu listenin **en büyüğünü** seçer. Liste 8192x6144 içermediği
için AGC her açılışta tercihi 4096x3072'ye geri yazıyordu — logcat kanıtı:

```
CAM_A: Picture size setting is not set. Selecting fallback: 4096x3072
```

Neden içermiyor: **Android'in `getOutputSizes()` metodu "yüksek çözünürlük"
sayılan boyutları eler.** Ölçüt, minimum kare süresinin 1/20 sn'den uzun
olması. Kamera 3 (IMX989 ana) için `android.scaler.availableMinFrameDurations`:

| boyut     | min kare süresi        | sınıf              |
|-----------|------------------------|--------------------|
| 4096x3072 | 33.333.333 ns (30 fps) | normal             |
| 8192x6144 | 66.666.666 ns (15 fps) | yüksek çözünürlük  |

Yüksek çözünürlüklü boyutlar yalnızca `getHighResolutionOutputSizes()` ile
gelir. Port bu metodu **hiç çağırmıyor**. Open Camera'nın 50,3 MP alabilmesinin
sebebi de bu: o iki listeyi de okuyor.

Elenen diğer hipotezler (hepsi ölçümle):

- `Lddl;->P/Q` kara listeleri (`blacklisted_resolutions_back/front`) boş —
  hiçbir şey elemiyorlar.
- `LAGC;->Forty8Strip(I)I` bu yapıda `return p0`, yani boş saplama;
  `StreamConfiguration()` ve `StreamConfiguration2()` sadece ona yönleniyor.
  Portun kendi 48M mekanizması bu sürümde yok. (UI'daki "Redmi K20 Pro / Mi9"
  notu da bunu doğruluyor.)
- `pref_48m_key=1` tek başına işe yaramıyordu — çünkü tıkanıklık portun
  filtresinde değil, `getOutputSizes()`'ın kendisindeydi.
- `pref_fix_resolution_key_N=37` (RAW10) config'den geliyor ve JPEG listesini
  RAW10 genişliğine kırpıyor; ikincil bir daraltma, asıl sebep değil.

## Yapılan yama

`classes2.dex` / `LAGC;` (kaynak: `agc-50mp-yama/`):

1. `getSupportedOutputSizes(I, StreamConfigurationMap)` yeniden yazıldı —
   davranış aynı, tek fark `pref_48m_key != 0` iken listenin
   `allOutputSizes()`'tan gelmesi.
2. `allOutputSizes(StreamConfigurationMap, I)` eklendi:
   `getOutputSizes(f)` ∪ `getHighResolutionOutputSizes(f)`. İkincisi null
   dönerse ya da istisna atarsa birincisi aynen döner.

Yama **`pref_48m_key` arkasında kapalı**: tercih yoksa APK stok gibi davranır.
Bu bilinçli — port zaten bu anahtarı 48M anlamında tanımlamış, tıkanıklığı
onun arkasına koymak hem geri alınabilir hem de önizleme/video akışlarını
etkilemez.

Araç zinciri (hepsi scratchpad'e kuruldu, projeye bulaşmıyor): Temurin JDK 21,
smali/baksmali 2.5.2 + dexlib2 + guava + antlr-runtime + jcommander,
uber-apk-signer 1.3.0. APK içindeki `classes2.dex` girdisi diğer girdilerin
sıkıştırma yöntemi korunarak değiştirildi, sonra zipalign + v3 imza.

Çıktı: `AGC8.4.300_V9.6_50MP_patched.apk` (151.023.603 bayt).

Kurulum: imza değiştiği için kaldır–kur gerekti. `shared_prefs` (yani AGC
config) tar ile yedeklendi, kurulumdan sonra yeni uid'ye `chown` + üst dizinin
SELinux bağlamıyla `chcon` yapılarak geri konuldu; çalışma zamanı izinleri
`pm grant` ile geri verildi. Kullanıcı tarafında hiçbir işlem gerekmedi.

## Ölçülen sonuç — yarı başarı

`pref_48m_key=1` + `pref_raw_key_0=35` (YUV_420_888) ile:

- fotoğraf boyutu tercihi `8192x6144` olarak **kalıyor** (yama öncesi her
  açılışta 4096x3072'ye geri yazılıyordu) — yani AGC artık 50MP'yi görüyor,
- `AGC: getImageReaderFormat ImageReaderFormat{ImageFormat=YUV_420_888,
  Size=8192x6144}`,
- `cameraserver: Bypass roundBufferDimensionNearest for privilegedClient YUV
  streams width 8192 height 6144 for format 35` — akış yapılandırıldı.

**Ama çekim tamamlanmıyor:**

```
CAM_ShotTracker: Stuck shot ... captureSessionType=HDR_PLUS ... marked stuck
CAM_ProcessingEvent: Task seems stuck: ImageShadowTask-ShotId-0
```

Deklanşöre basıldığında HAL'e hiç istek gitmiyor (o aralıkta CamX'te tek satır
yok). GCam'in HDR+ motoru 8192x6144 YUV yükünü işleyemiyor — Gcam boru hattı
girdi olarak Bayer/RAW bekliyor.

`pref_48m_key` yokken (mevcut durum) APK stok gibi çalışıyor: RAW10 4096x3072,
çekim sorunsuz — 14:42'de fotoğraf üretilerek doğrulandı.

## Asıl darboğaz artık HAL tarafında

`getImageReaderFormat` yük (payload) biçimini portun `pref_raw_key_N` değerine
göre seçiyor; config `37` = RAW10 diyor. Kamera 3'ün standart
`android.scaler.availableStreamConfigurations` tablosunda RAW10'un tavanı
4096x3072. Yani 12,6 MP tam olarak **RAW10 akışının tavanı**.

Oysa HAL bunu destekliyor — `xiaomi.scaler.availableStreamConfigurations`
kamera 3 için şunları listeliyor:

```
[37 8192 6144 0]   RAW10   OUTPUT
[32 8192 6144 0]   RAW_SENSOR OUTPUT
[36 8192 6144 0]   RAW_PRIVATE OUTPUT
```

Mevcut 16 noktalı HAL yamamız standart tabloya yalnızca 33/34/35'i (BLOB /
PRIVATE / YUV) 8192x6144'te ekliyor; ham biçimleri eklemiyor.

## Sıradaki adımlar

**A — HAL yamasını genişlet (önerilen).** `camera.qcom.so` içindeki
`InitializeScalerStaticCaps` yamasına RAW10 (37) ve tercihen RAW_SENSOR (32)
için 8192x6144 girdilerini, eşlik eden `availableMinFrameDurations` ve
`availableStallDurations` satırlarıyla birlikte ekle. Bu, GCam'in beklediği
girdiyi (ham Bayer) 50MP'de sunar ve config'in `pref_raw_key=37` ayarı
olduğu gibi çalışır. Riskler: HAL'in 8192x6144'te verdiği ham verinin
remosaic edilmiş Bayer mi yoksa işlenmemiş Quad-Bayer mi olduğu bilinmiyor;
ikincisiyse renkler bozuk çıkar. Ayrıca `activeArraySize` 4096x3072'de
kalıyor, GCam kırpma matematiğini buna göre yapıyor — yükseltmek GCam 8.4'ün
yerel motorunu bozuyor (Faz 4'te ölçüldü).

**B — Portun YUV/akış anahtarları.** `getStreamMode`, `pref_stream_mode_key`,
`pref_opmode_photo_key` ve `Lcom/agc/Camera;` içindeki YUV yolları
incelenip HDR+ motorunun YUV yükünü kabul etmesi sağlanabilir mi bakılır.
Yerel (native) kodda olduğu için görünürlük düşük; A'ya göre daha spekülatif.

**C — Kısa yol (gerçek 50MP değil).** `pref_48m_key=1` + RAW10 4096x3072
kalırsa AGC 12,6 MP'yi 8192x6144'e büyütür. Dosya 50MP olur, detay olmaz.
Önerilmez, ama kullanıcı isterse tek tercih değişimiyle açılır.

Karar noktası: A mı, B mi, yoksa Faz 10 / mod 0'ı 12-bit'e taşıma denemesi mi.

# Faz 12 — HAL RAW genişletmesi: RAW10 50MP açıldı, Gcam duvara çarptı (2026-08-23)

Hedef: `android.scaler.availableStreamConfigurations` tablosuna RAW10 (37) ve
RAW_SENSOR (32) için 8192x6144 girdilerini eklemek; böylece QS kutucuğu tek
anahtar olsun (HAL yaması açıkken AGC kendiliğinden 50MP RAW10 seçsin).

## Tersine mühendislik altyapısı

`camera.qcom.so` sembolleri soyulmuş (727 fonksiyon sembolü, hedef fonksiyon
yok). radare2 bu ikilide çalışmadı (rabin2 de radare2 de takılıyor, 60 sn'de
tek satır çıktı vermiyor). Çözüm: **gömülü Python 3.12 + capstone + pyelftools**
(scratchpad'e kuruldu). Tüm çözümleme bununla yapıldı.

## Fonksiyon haritası

`InitializeScalerStaticCaps` = **0x16bf4c0 .. 0x16c5a90** (26 KB, 6516 komut).
Mevcut 16 noktalık yamamızın hepsi bu fonksiyonun içinde ve hepsi aynı alanı
okuyor: `ldr Wn, [Xm, #0x3d84]` → `mov Wn, #0`. İkilinin tamamında bu alana
55 erişim var, fonksiyon içindeki 16'sının hepsi zaten yamalı — yani RAW'ın
dışlanması **bu kapıdan kaynaklanmıyor**.

Yayıncı (emitter) şöyle: `[x?+0xb10]` akış-yapılandırma dizisinin tabanı,
her girdi 16 bayt = `{bicim, genislik, yukseklik, yon}`.

```
0x16c18d8  sub  w11, w0, #0x22      ; w0 = bicim
0x16c18dc  cmp  w11, #2
0x16c18e0  b.lo 0x16c1a8c           ; 0x22,0x23 -> yayinla
0x16c18e4  cmp  w0, #0x36
0x16c18e8  b.eq 0x16c1a8c           ; 0x36 (P010) -> yayinla
0x16c18ec  cmp  w0, #0x21
0x16c18f0  b.ne 0x16c1ac0           ; BLOB degilse baska yol
```

İşte 8192x6144'ün hangi biçimlerde göründüğünü belirleyen yer burası:
0x21 (BLOB/33), 0x22 (34), 0x23 (35), 0x36 (54). Ham biçimler listede yok.

Aynı `format - 0x22 < 2` testi fonksiyonda **dört yerde**: 0x16c18dc,
0x16c1c18, 0x16c22bc, 0x16c2330.

## Yapılan deneme ve ölçüm

Dört noktada `cmp wN, #2` → `cmp wN, #5` (aralık 0x22..0x26). Toplam
**4 komut, 16 bayt**. Yama tablosu: `agc-50mp-yama/hal-raw50-deneme.patch`.

Sonuç — kamera 3'ün standart tablosunda artık:

```
[37 8192 6144 OUTPUT]   RAW10
[38 8192 6144 OUTPUT]   RAW12
[36 8192 6144 OUTPUT]   RAW_OPAQUE
```

(dizi 508 → 868 int32). AGC hiçbir tercih değiştirmeden
`getImageReaderFormat ImageReaderFormat{ImageFormat=RAW10, Size=8192x6144}`
diyor. **Yani "tek anahtar" hedefi akış seçimi düzeyinde tutuyor.**

Ek olarak: RAW10 8192x6144 için `availableMinFrameDurations` girdisi
oluşmadığı için Android bunu "yüksek çözünürlük" kovasına atmıyor; normal
`getOutputSizes()` içinde geliyor. Bu yüzden Faz 11'deki APK yaması bile
gerekmiyor.

## Duvar: Gcam'in statik metadata tutarlılık denetimi

```
libgcam static_metadata.cc:667
  Check: StaticMetadata::frame_raw_max_{width,height} (8192x6144)
  matches neither the active area size (4096x3072) nor pixel array size (4096x3072).
libgcam gcam.cc:274
  Create: StaticMetadata for sensor ID 4 failed basic error checks.
```

Bu, Faz 4'te "geniş yama AGC'yi çökertiyor" diye kaydettiğimiz
`NullPointerException: Gcam.f()` hatasının **tam açıklaması**: Gcam,
ham kare boyutunun aktif diziye **ya da** piksel dizisine eşit olmasını
şart koşuyor. Geniş yama aktif diziyi büyütüp ham boyutu büyütmemişti;
bu yama ham boyutu büyütüp diziyi büyütmedi — iki yönde de aynı denetim
patlıyor.

## Denenen çözüm ve neden yetmediği

`MetadataConverterUtil.convertToGcamStaticMetadata` ve `Lpkr;->v(Llvp;)`
içinde piksel dizisi `LAGC;->Forty8Strip(I)I` (boş saplama) üzerinden
geçiyor. Bu iki nokta, piksel dizisini ham en büyük boyuta eşitleyen
`LAGC;->rawArrayWidth/Height/Dim` yardımcılarıyla değiştirildi.

Sensör 4 denetimi **geçti**. Ama bu sefer sensör 7 patladı
(`frame_raw_max 4096x1508` ↔ `aktif 2048x1536` / `piksel 4096x3072`).

Sonra izole edildi: sensör 7 arızası HAL yamasından da APK yamasından da
gelmiyordu — tercihlerde kalan `pref_raw_key_0` / `pref_fix_resolution_key_0`
değerlerinden geliyordu. Bu iki anahtar portun `getFixResolutionList()`
genişlik-kırpma mantığını tetikliyor ve bazı sensörler için listeyi
4096x1508 / 2048x1508 gibi tuhaf bir boyuta indiriyor. Tercihler
temizlenince AGC yeniden sağlıklı çalıştı.

**Bu, config dosyası için önemli bir uyarı:** `pref_fix_resolution_key_N=37`
tek başına Gcam'i çökertebiliyor.

## Kalan iş

1. HAL yamasını **daralt**: ham biçimler şu an her çözünürlüğe ekleniyor
   (dizi 360 int32 büyüdü). Yalnızca QCFA tam çözünürlüğünde eklenmeli.
2. Gcam denetimini geçir: piksel dizisini (ya da aktif diziyi) 8192x6144
   yapmak. En temizi HAL tarafında `android.sensor.info.pixelArraySize`
   (etiket `f0006`) değerini tam çözünürlüğe çekmek — IMX989'un fiziksel
   piksel dizisi zaten 8192x6144. İkili içinde bu etikete 9 movz/movk
   erişimi ve 6 rodata dword'ü var; yazma noktası henüz bulunmadı.
3. Sonra gerçek çekim testi: HAL'in 8192x6144'te verdiği ham verinin
   remosaic edilmiş Bayer mi yoksa işlenmemiş Quad-Bayer mi olduğu hâlâ
   bilinmiyor. İkincisiyse renkler bozuk çıkar.

## Cihazın bırakıldığı durum

HAL deneme yaması geri alındı (`active_hal` md5 = `fe0245a4...` = standart
fullres), mod `50mp`; APK = `AGC8.4.300_V9.6_50MP_patched.apk` (Faz 11
yaması, `pref_48m_key` yokken stok davranış); AGC tercihleri sıfırlandı
(`pref_48m_key`, `pref_raw_key_0`, `pref_fix_resolution_key_0` silindi).
AGC canlı önizleme veriyor ve çekim yapıyor.

# Kararlar (kullanıcı tarafından verildi — 2026-08-20)

**#1 — 50MP ile DCG/LN ilişkisi → A, sonra B denemesi**
Önce **birbirini dışlayan** kurulacak: 50MP açılınca DCG/LN kapanır, DCG/LN
açılınca 50MP kapanır. Bu çalıştıktan ve doğrulandıktan sonra mod 0'ı da
12-bit'e taşıyıp birlikte çalıştırma (B) denenecek.

**#2 — Temiz sayfa**
v1.9 tabanına 50MP sıfırdan eklenecek. Önceki modelin APK'sı ve script
değişiklikleri yalnızca **referans**; hiçbiri olduğu gibi taşınmayacak.

**#3 — 50MP kutucuk ikonu → klasik fotoğraf makinesi silueti**

**#4 — Mod 0'ın 12-bit'e taşınması (B seçeneği) → ONAYLANDI, Faz 9 sonrası**
Kullanıcı 2026-08-20'de onayladı: her şey oturduktan sonra sensör modu 0
(50MP) 12-bit'e taşınmayı deneyecek. Hedef **50MP + LN2 ve 50MP + LN4'ün
aynı anda çalışması**. Başarısız olursa yalnız bu deneme geri alınır.

