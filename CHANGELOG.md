# CHANGELOG — ishtar IMX989 Camera Modes

Version history for `ishtar-cam-modes`. This file is the **owner** of that
history. Before Faz 9.3 it lived in `ishtar-cam-modes/module.prop`'s
`description` field, which is a module *summary* field, not a changelog — the
duplication is `AUTOPSY-P3-01` and `ARC-10`. `module.prop` now carries a summary
and points here; new versions add an entry here and do **not** extend the
description.

The entries below are the ones the description held, preserved as written
(ASCII Turkish, as in the original field), except for one marked correction in
v2.0. Nothing has been deleted. Versions v1.0, v1.1 and v1.3 predate the
description's history and have no entry; the earliest recorded entry is v1.2.

Related records: `50MP-Entegrasyon-Plani.md` (the measurement journal),
`Planner-docs/Project-Ontology.md` (vocabulary and invariants),
`docs/agc-12mp-configuration.md` (the AGC configuration record),
`docs/release-manifest.md` (per-release checksums).

---

## v2.2

Google Camera'nin calisma cozunurlugu hakkindaki eski iddia duzeltildi. Onceki
metinler "AGC 15,2 MP'de kaliyor -- GCam 8.4'un kendi siniri" diyordu; iddianin
her iki yarisi da yanlisti. Dogrusu: AGC 12,58 MP'de sabit calisir, ve sebep
GCam degil Android'in yuksek-cozunurluk kovasidir — `getOutputSizes()` minimum
kare suresi 1/20 sn'yi asan boyutlari eler, 8192x6144 = 66.666.666 ns oldugu
icin standart listede gorunmez (kayit: `docs/agc-12mp-configuration.md`).
Duzeltme dort yuzeyde uygulandi: `module.prop`, `webroot/index.html` (Ingilizce
ve Turkce) ve `setmode.sh`'nin `50mp` moduna gecerken bastigi cikti.

`action.sh`'nin `tiles` ciktisi duzeltildi: `tiles status` alani artik olctugu
seyin adiyla (`takma_ad` — etkinlik takma adi, cekmece degil) raporlanir ve
`tiles hide` dogrulayamadigi bir sonucu iddia etmez.

`module.prop` aciklamasi bir ozet alanina indirildi (1741 -> 1119 karakter) ve
surum gecmisi bu dosyaya tasindi.

## v2.1

Uygulama simgesi cekmecede artik dogru cizilir (onceki ikon kutucuk tint'ini
kullandigi icin beyaz zeminde beyaz kaliyordu, yani bos gorunuyordu); baslatici
gorunurlugu artik her cagrida yeniden uygulanir ve durum raporu onbellekten
degil cerceveden okunur.

> **Not (2026-09-06, `IMPL-75`, henuz surumlenmedi).** `action.sh`'nin `tiles`
> ciktisi duzeltildi: `tiles status` alani artik olctugu seyin adiyla
> (`takma_ad` — etkinlik takma adi, cekmece degil) raporlanir ve `tiles hide`
> dogrulayamadigi bir sonucu iddia etmez. Bu degisiklik pakete girdi ancak
> `module.prop` surumu bilincli olarak yukseltilmedi; surum karari Faz 9.2'ye
> birakildi.
>
> **Cozuldu (2026-09-06, `IMPL-80`).** Surum karari verildi: bu degisiklik
> asagidaki **v2.2** girdisiyle surumlendi.

## v2.0

50MP (FullRes) modu — 8192x6144 STANDART Camera2 listesine eklenir, boylece
ucuncu parti uygulamalar tam cozunurluk ceker (olculdu: OpenCamera 50,3 MP;
AGC 12,6-15,2 MP'de kalir). Video 1080p60/4K60 etkilenmez. HAL ikilisinin
27 MB'lik kopyasi pakete konmaz; yalnizca 16 noktalik yama listesi tutulur ve
cihazdaki stok ikili yamalanir. 50MP ile DCG/LN birbirini disler. Dorduncu
Hizli Ayarlar kutucugu (fotograf makinesi ikonu) 50MP icin eklendi; dort
kutucuk birbirini disler, biri acilinca digerleri kapanir.

> **DUZELTME (Faz 9.3, 2026-09-06) — bu girisin tek degistirilmis yeri.**
> Ozgun metin AGC'nin 12,6-15,2 MP'de kalmasini *"cunku GCam 8.4 motoru 50MP
> akisini secemiyor"* diye acikliyordu. **Bu neden yanlistir.** `IMPL-23`
> piksel-dizisi ve RAW kelimeleri uygulanmis halde AGC ile ucu yeniden
> uretilebilir 50,3 MP cekim yapti; yani motor secebiliyor. Gercek neden
> Android'in yuksek-cozunurluk kovasidir: `getOutputSizes()` minimum kare
> suresi 1/20 sn'yi asan boyutlari eler ve 8192x6144 = 66.666.666 ns oldugu
> icin standart listeye girmez (`Planner-docs/Project-Ontology.md` degismez 7,
> `OQ-15`; `agc-50mp-yama/README.md`).
>
> **Rakam degismedi ve degismemelidir.** 12,6-15,2 MP olcumu gecerlidir, ve
> AGC'nin bugunku calisma cozunurlugu `DEC-14` ile sabitlenen **12,58 MP**'dir
> — asilamayan bir tavan degil, secilmis bir yapilandirma. Kaydi
> `docs/agc-12mp-configuration.md`. "AGC artik 50 MP cekiyor" demek, eski
> yanlisin yerine yeni bir yanlis koymak olurdu.

## v1.9

Gecis sirasinda saniye saniye geri sayan canli bildirim.

## v1.8

Arayuz dili sistem dilinden bagimsiz, varsayilan Ingilizce; WebUI'de EN/TR
dugmesi.

## v1.7

Mod degisimi kamera gercekten hazir olana kadar bitmis sayilmiyor; gecis ve
"hazir" bildirimleri ekranin altinda gosterilir.

## v1.6

Mod degisiminde kamerayi kilitleyen hata giderildi (kamera yigini artik dogru
sirayla yeniden baslatiliyor); kutucuklarda alt yazi kaldirildi.

## v1.5

Kutucuklarin birbiriyle senkronu duzeltildi.

## v1.4

DCG/LN4/LN2 icin 3 Hizli Ayarlar kutucugu (uzun basinca WebUI acilir, uygulama
cekmecede gorunmez), ayrica WebUI ve Action dugmesi.

> **Not (Faz 2.4, `IMPL-71`/`IMPL-75`).** "Uygulama cekmecede gorunmez" bu ROM
> icin dogru degildir: `pm disable` basarili olur, AOSPA Launcher3 onu
> uygulamaz ve simge cekmecede kalir. Baska baslaticilarda calisir. Giris
> oldugu gibi birakildi; olculen davranis `ishtar-cam-modes/Kullanim.txt` ve
> `action.sh tiles status` ciktisindadir.

## v1.2

`dcgB` onerilen mod — cihazda olculdu, stoka gore %25 az gurultu ve iki kati
detay, deklansor hizi degismiyor. `overrideForceSensorMode` property'sine gerek
yok.
