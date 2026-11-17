# PROJECT_LOG — ishtar

> Durum tarihi **2026-11-14** · özet belge; kanonik kaynak `Planner-docs/Planing-Ledger.md`. Çelişkide önce depo, sonra ledger geçerlidir ve bu belge onlara göre düzeltilir. · Nasıl güncellenir: her koşunun (IMPL, planlama koşusu, denetim) sonunda önce ledger yazılır. Sonra burada §2'nin ilgili satırları güncellenir; §3.2'ye (IMPL ise), §4'e (karar varsa) ve §11'e birer satır eklenir. Çıkarımlar `[ÇIKARIM]` ile işaretlidir.
>
> Kaynak kısaltmaları: `L:n` ledger satırı · `AUD` `Planner-docs/Sub-Planing-Audit.md` · `IDX` `Planner-docs/Sub-Planing-Index.md` · `MP` `Planner-docs/Main-Planing.md` · `BE` `docs/build-environment.md` · `PRP` `docs/pre-rental-plan.md` · `DEV` `docs/rom-build-device-notes.md` · `RC` `docs/release-checklist.md` · `CFG` `docs/agc-12mp-configuration.md` · `J` `50MP-Entegrasyon-Plani.md` · `CL` `CHANGELOG.md` · `Ö13` 2026-11-13 oturumunun ölçümü (git, doğrulayıcı, self-test) · `snap X` `snapshots/X__*` dosyaları.

## 1. Proje kimliği ve kapsam

Bu proje, kullanıcının kendi Xiaomi 13 Ultra'sının kamerasını root modülleri ve yapılandırılmış bir kamera uygulamasıyla özelleştirir. Cihaz: `ishtar`, model `2304FPN6DC`, SM8550 / `kalama`, adb seri `dc27e5d0`. Bu belgedeki 2026-11-13'ten önceki ölçümler telefonda AOSPA Vauxite (Android 15) ve KernelSU Next varken yapıldı (DEV §2-3). 2026-11-13'te telefonda HyperOS 4 gözlendi ve aynı gün salt-okur ölçüldü (`70946ff`, §2.3; ROM, kernel 5.15.215 ve KernelSU dahil). **2026-11-13 kullanıcı beyanı:** telefondaki HyperOS 4, Çinli bir geliştiricinin portudur; ROM derleme fikri kullanıcı kararıyla bırakıldı (`DEC-28`; §2.3, §2.5). Planlama ClaudeQB disipliniyle yürür (§3.3).

**Teslimatlar:**
- `ishtar-cam-modes` **v2.2 / versionCode 13**. İki katmanı var: sensör modu katmanı (`stock`, DCG/LN varyantları) ve HAL katmanı `50mp`; ikincisi 8192x6144'ü standart Camera2 listesine ekler. Ayrıca 4 QS kutucuğu, WebUI ve Action düğmesi içerir (`ishtar-cam-modes/module.prop:3-4`; CL).
- `ishtar-aon-fix` **v1.1 / versionCode 2**: `aon_front.pb`'yi `/vendor/lib64/camera` üzerine bind-mount eder. Ayrı modül olarak kalır (`DEC-04`).
- Yapılandırılmış AGC (yamalı AGC 8.4.300 V9.6, `ce65f862c990e2acc02be356f75a7122`): `pref_48m_key=0` + `pref_camera_resolution=full` ile `50mp` altında 12.58 MP'de sabittir. Aynı HAL durumunda Open Camera 50.33 MP çeker (CFG; L:647).
- Android 16 girdi depoları: `ahmetxa/android_local_manifests` (`22283d8`) ve `ahmetxa/android_device_xiaomi_ishtar` (`beryl` `d48816f`). İkisi de herkese açık; hiç derlenmedi (L:99, L:520). Derleme 2026-11-13'te bırakıldı (`DEC-28`); iki depo silinecek (`DEC-30`) ve 2026-11-14T13:45:22Z ölçümünde ikisi de hâlâ duruyor.

**Yöntem: disassemble + offset tablosu + bind-mount.**
- *Disassemble:* `camera.qcom.so` (27,268,688 B) capstone/pyelftools ile betikle çözülür; AGC APK'sı smali ile. Adresler yalnız `Project-Ontology.md` adres defterinde tutulur.
- *Offset tablosu:* 27 MB'lik HAL asla paketlenmez. Bunun yerine `blobs/hal-fullres.patch` (16 nokta, üç sütun) cihazın kendi stok HAL kopyasına uygulanır.
  - Korumalar `halpatch.sh` (`HAL_STOCK_MD5`, `HAL_FULLRES_MD5`, `HAL_SIZE`) ve `customize.sh` (`EXPECT_MD5`) içindedir; biçim sözleşmesi `docs/patch-table-format.md`'dir.
  - Her yazım sırasıyla boyutu, sonra md5'i denetler, sonra yazar. Bir denetim tutmazsa hiçbir şey yazılmaz.
- *Bind-mount:* Modül yamalı kopyayı `/data/adb/modules/ishtar_cam_modes/active_hal/` altında üretir ve `/odm/lib64/hw/camera.qcom.so` üzerine bağlar. Sensör blob'u da `active/` altından `/odm/lib64/camera/` üzerine bağlanır. `/odm`'a hiçbir şey yazılmaz.
- İlk kurtarma hamlesi `disable` bayrağı + reboot'tur (`docs/recovery-runbook.md`; MP:81-107).

**Ölçüm ilkesi** (L:474, L:478, L:485, L:510):
- Tahmin, eşik ve beklenen md5 ölçümden önce yazılır ve sonradan değiştirilmez.
- Her cihaz değişikliği `scripts/smoke.sh` snapshot'larıyla çerçevelenir. Geri alındıktan sonra karşılaştırılabilir bölge bayt-özdeş olmalıdır.
- Görüntü temizliği "IMPL-40 yöntemi"yle ölçülür: siyah piksel oranı < 0.01. Boyutlar JPEG SOF / MP4 kutularından okunur.
- Her ölçümde tek değişken değiştirilir.
- Otorite cihazdır; fixture yalnız bir hipotezdir.
- Plandan sapma sessizce sindirilmez, beyan edilir.

**Hedef son durum (MP:79-89):**
- QS kutucuğundan seçilen mod reboot'tan sonra korunur.
- Aynı HAL durumunda Open Camera 8192x6144, AGC temiz 12.58 MP çeker; 1080p60/4K60 etkilenmez.
- HAL tablosu geniş kalır.
- Her sürüm tek ve yeniden üretilebilir bir KernelSU zip'idir.
- AON kök nedeni iki ağaçta çözülür.
- Hiçbir artefaktta imza anahtarı bulunmaz.

Emekliye ayrılan hedef: AGC'de uçtan uca 50 MP (`DEC-14`, 2026-09-03; §5).

## 2. Şu an neredeyiz (2026-11-14)

### 2.1 Git ve depo
- **Dal ve commit'ler (2026-11-14):** `main` 63 commit: ilk `ff6934e` (2026-08-24), `587e3b5` (IMPL-95, 2026-09-14) ve `7fa0a51` (planlama koşusu 20 + 11. denetim, değiştirilmeden). `integrate/impl-96` dalı `7fa0a51` üzerine yeniden kuruldu: `70946ff` (HyperOS 4 kanıtı; probe satır 42, 190, 191 redakte), `03b0898` (tarihsel notlar, cihaz notları), `775b321` (oturum belgeleri), sonra C0 `b603516` (`ORCHESTRATION_PLAN.md`'yi ekleyen commit), takip commit'i `c2abd46`, C1 (`IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline`) ve Pencere 2 aşama commit'leri (`Window 2 O0-O1: approved plan, discovery facts, stage-per-session loop`, `Window 2 O2: contract for the project log sweep and the run 21 handoff`); dal 71 commit (`2 · O3` açılışı ölçümü, 2026-11-14). Eski hash'lerin eşlemesi §11'dedir; eski hash'ler yalnız yedek bundle'da ve yerel reflog'da. Etiket yok. Tüm commit'ler tek kimlikle (GitHub `ahmetxa`). (Ö13; dal sayısı ve Pencere 2 commit'leri `2 · O3` açılışı ölçümü)
- **Remote:** `origin` = `https://github.com/ahmetxa/ishtar_cam_modes.git`, özel depo (kullanıcı kararı 2026-11-13; `DEC-27`, ledger §8 `:605`).
  - 62 commit `git push` ile hash'leri değişmeden gönderildi: `git ls-remote origin` → `main` = `587e3b5`; kök `ff6934e` GitHub API'de aynı hash ve tarihle; `private=true`, varsayılan dal `main` (Ö13).
  - `7fa0a51` ve `integrate/impl-96` dalı 2026-11-15'te push edildi: C2'den sonra ayrı onaylarla `main` FF (08:14:45Z) ve `git push origin main integrate/impl-96` (08:15:01Z); takip commit'i de aynı gün (reflog: 08:58:01Z, 08:58:04Z). Pencere 3'ün 11 commit'i (C3 dahil) 2026-11-16'da ayrı onaylarla FF (22:05:00Z) ve push (22:05:35Z) edildi. Pencere 4 açılışı (22:09Z): `origin`'de `HEAD`, `main`, `integrate/impl-96` = C3 (`081790f`), `origin/main..HEAD` 0 (`ORCHESTRATION_PLAN.md` §8.1, `W4OPN`). Push yalnız açık refspec ve ayrı onayla.
  - Eski `ishtar-eski` remote'u (`ahmetxa/ishtar`) 2026-11-13'te yerelden kaldırıldı. Tek dalı `main@f8a05ca` yerel `main`'in atası; içeriğinin tamamı yeni depoda.
- **Silinecek GitHub depoları (K5/K6, kullanıcı kararı 2026-11-13):** `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. Silme yapılmadı: `gh` belirtecinde `delete_repo` yetkisi yok, silmeyi kullanıcı yapar. Hiçbirinde release, tag ya da açık issue yoktu. İki açık deponun ayna yedeği `C:/Users/ahmet/Documents/Projeler/ishtar-arsiv/` altında: `android_local_manifests.git` (`main@22283d8`) ve `android_device_xiaomi_ishtar.git` (`beryl@d48816f`, `vauxite@713784c`); ikisinde de `git fsck` temiz.
  - Ölçüm (2026-11-14T13:45:22Z, `gh api`): üç depo da hâlâ var (200); önceki ölçümler 2026-11-14T07:23:21Z ve 10:03:48Z'de, üçü de 200. Sonraki ölçümler §2.6'da.
- **Boyut (Ö13):**
  - 350 izlenen dosya (2026-11-14).
  - `size-pack` 17.86 MiB, ayrıca 74.38 MiB gevşek nesne (343 adet).
  - Tüm geçmişteki blob toplamı 109.7 MiB. En büyük blob 16.04 MiB (`snapshots/20260905-2034__Faz4.4__F4403-opencamera-capture-ORIGINAL.jpg`); 50 MiB üstü blob yok.
  - Hiçbir `.bin/.so/.apk/.zip/.keystore` dosyası hiç izlenmedi.
- **Bütünlük ve satır sonları:** `git fsck --no-dangling` temiz. `.gitattributes` varsayılan olarak `* -text` kullanır; `*.sh *.prop *.patch mode lang` için LF zorlanır.
- **Commit durumu (2026-11-14):**
  1. Planlama koşusu 20 ve 11. denetimin dört dosyası (`Faz7.2`, ledger, `Sub-Planing-Audit.md`, `docs/pre-rental-plan.md`) değiştirilmeden `7fa0a51` olarak `main`'e işlendi. İçerik: `DEC-26` ile `Faz7.2`'nin Scaleway'e yeniden hedeflenmesi ve 11. Step 3 denetimi (`PASS_WITH_WARNINGS`, P0/P1 yok, kuyruk başı `Faz7.2`/`F7.2-01`). Kuyruk 2026-11-13'ten beri geçersiz: ROM derleme bırakıldı (§2.5). Ledger 11. denetimi için IMPL-96 notları yazıldı (ledger `:100`, `:552`, `:554`, `:556`, `:558`); notsuz kalanlar `:51`, `:57`–`:60`, `:589` (§8 `:802`).
  2. `docs/rom-build-device-notes.md` (2026-09-20, AOSPA A15 salt-okur cihaz oturumu) §10 ekiyle `03b0898`'da işlendi; IMPL-96 satırının (4). maddesi kaydediyor (ledger `:525`).
  3. `devir-teslim-promptu.md` 2026-11-13'te kullanıcı kararıyla silindi (K4); yerini `NEXT_PROMPT.md` aldı.
  4. Oturum belgelerinin ilk sürümü `775b321` olarak `integrate/impl-96` dalına işlendi; sonraki sürümleri C0 `b603516`, `c2abd46`, C1 ve Pencere 2 aşama commit'lerindedir.
  5. C0 `b603516` (`ORCHESTRATION_PLAN.md`, bu günlük ve `NEXT_PROMPT.md`'yi taşıyan commit) işlendi; `git log --diff-filter=A -- ORCHESTRATION_PLAN.md` ile bulunur. Bu günlüğün ve `NEXT_PROMPT.md`'nin sonraki sürümleri `c2abd46`, C1 ve Pencere 2 aşama commit'lerinde.
- **Silinenler (2026-11-13, K4):** kökteki boş `UsersahmetAppDataLocalTempaon-smoke/` dizini ve `.gitignore:48` (`*.log`) nedeniyle hiç izlenmemiş üç log: `install.log` (izlenen `snapshots/20260831-1603__faz2.2__install-transcript-v2.1.txt` ile satır satır aynıydı), `common_clone.log` (tek satır: `Cloning into 'common_sm8550'...`), `kernel_clone.log` (tek satır: `fatal: destination path 'kernel_ishtar' already exists and is not an empty directory.`).
- **K8 (probe kimlikleri, 2026-11-13):** Commit edilmiş ama push edilmemiş probe anlık görüntüsündeki cihaz tanımlayıcıları redakte edildi ve dal `integrate/impl-96` `main` üzerinde yeniden kuruldu (§11). Redaksiyonsuz uç yalnız `../ishtar-arsiv/impl-96-unredacted.bundle` içinde (repo dışı; 77.094 B; sha256 `b9fa9c5cd5d0ae78f9f051ab62ecbfc2d9b2fa2fecd33f40247ef88bf58f6cd3`; `git bundle verify` geçti; önkoşul `7fa0a51`). R-identity-check (`git log --all -p`; yalnız sayım): `persist.sys.miui.sno` ve `ro.ril.miui.imei0`/`imei1` satırları `<redacted>` olmalı, Luhn geçen 15 haneli sayı olmamalı; son sonuç: tüm ref'lerde 0 eşleşme. Adlandırılmış yedek dal açılmadı.
- Ledger §6'nın depo paragrafı (47 commit, 225 dosya, remote yok) kısmen düzeldi: ledger `:528`'deki IMPL-96 notu remote'u ve commit sayılarını yazıyor, dosya sayısını yazmıyor (§8 `:803`).

### 2.2 Sürüm ve paket
- **Güncel paket:** `ishtar-cam-modes` v2.2 / versionCode 13, arşiv `dist/ishtar-cam-modes-v2.2.zip`. Bilgiler `docs/release-manifest.md`'den:
  - md5 `e95789572311cc95266d3ab4045cdcba`
  - sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0`
  - 43 girdi, 1,009,107 bayt
  - Cihaza kuruldu ve doğrulandı (VAL-INSTALL, IMPL-81; RC §6a).
  - IMPL-76/77'deki ara derleme sha256'ları yalnız tarihsel kayıttır.
- **Self-test (Ö13):** `py -3 scripts/build-release.py --self-test` → `SELF-TEST: PASS`.
  - VAL-BUILD2: iki derleme bayt-özdeş ve sha256 yukarıdakiyle aynı.
  - A1 (kimlik bilgisi girdisi), A2 (HAL boyut sınıfı) ve A3 (sınıflandırılmamış dosya) PASS.
  - `--self-test` yalnız geçici dizinlere yazar. Bayraksız çalıştırma ise `docs/release-manifest.md`'nin üzerine yazar.
- **Kontrol listesi (RC §7, 2026-09-09):** 18 yetenek. 9 pass; 2 waived (C-02, C-03); 7 pending (C-01, C-04, C-05, C-09, C-11, C-12, C-17); 0 fail.
  - Ledger L:106'daki "C-05/09/11/12/13 pending" listesi bayat: C-13 IMPL-88 ile pass oldu.
- **AON modülü:** `ishtar-aon-fix` v1.1 / versionCode 2.
- **`Kullanim.txt`:** `ishtar-cam-modes/Kullanim.txt` zip'in içinde dağıtılıyor ve hâlâ v1.9 kılavuzu (13 bayat ifade; hiçbiri AGC'nin 50 MP çektiğini iddia etmiyor). Dosyayı düzenlemek, yayımlanan v2.2 ile bayt-özdeşliği bozar; K1=(b) gereği bir sonraki sürümde düzeltilecek (§4). *(2026-11-14 notu: bayt-özdeşliği gerekçesi yayımlanan v2.2 zip'i için geçerli (`DEC-29`); v2.2 AOSPA A15'te kuruluydu (IMPL-81), HyperOS 4'te proje modülleri kurulu değil.)*

### 2.3 Cihaz
**2026-11-13 ölçümü (HyperOS 4, salt-okunur, yalnız `dc27e5d0`):** `snapshots/20261113-1819__IMPL96__hyperos4-readonly-probe.txt` ve `snapshots/20261113-1821__IMPL96__hyperos4-smoke-baseline.txt` (commit `70946ff`).
- **ROM:** HyperOS `OS4.0.0.44.WMACNXM`, Android 17 (SDK 37), yapı `CP2A.260605.016`, güvenlik yaması 2026-09-01; vendor/odm parmak izi `Xiaomi/ishtar/ishtar:13/TKQ1.221114.001/OS4.0.0.44.WMACNXM:user/release-keys`. Kullanıcıya göre üçüncü taraf bir geliştiricinin derlemesi.
- **Kernel:** `5.15.215-KylinKernel-260925-Release` (derleme 2026-09-25). SELinux Enforcing; doğrulanmış önyükleme `orange`, kilit açık.
- **Root:** KernelSU `4.3.0-r1` (ksud uapi 6); adb kabuğu `su` ile `u:r:ksu:s0` alıyor. `pm list packages`'ta ne KernelSU Next (`com.rifsxd.ksunext`) ne de resmî KernelSU yöneticisi (`me.weishu.kernelsu`) var.
- **Modüller:** `ishtar_cam_modes` ve `ishtar_aon_fix` **kurulu değil**. Kurulu 13 modül: FreePPS, advsettings-en, box_for_root (devre dışı), NeoZygisk, unlimitedphotos ve sekiz "Morphe" uygulama modülü.
- **Kamera dosyaları:**
  - `/odm/lib64/hw/camera.qcom.so`: md5 `2a955e68ad043380675529edb64a40f7`, 27.305.440 B. AOSPA stokundan (`c3fa63a8…`, 27.268.688 B) **farklı**: 16 noktalı `hal-fullres.patch` uymaz, modülün HAL koruması 50MP katmanını kapatır.
  - `/odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin`: md5 `9e4d0fe1a8bf2eb4146c9917a0ac2c4c`, 1.062.250 B; `EXPECT_MD5` ile **aynı**.
  - `/vendor/lib64/camera/aon_front.pb`, `/odm/lib64/camera/aon_front.pb`'ye symlink; ROM'un kendisinde var. AOSPA'da yoktu; `ishtar-aon-fix` ve `Faz6.1` bunu sağlamak içindi.
  - Kamera dosyalarında bind mount yok.
- **Kameralar:** 13 aygıt (hal0…hal12), ana arka kamera hal0. hal0'ın standart akış yapılandırmaları her biçimde 4096x3072'de bitiyor. `ULTRA_HIGH_RESOLUTION_SENSOR` yeteneği ve maksimum çözünürlük etiketleri hiçbir aygıtta yok. `8192 6144` yalnız üreticiye özel etiketlerde (`xiaomi.scaler.*`, `org.codeaurora.qcamera3.quadra_cfa.*`, `org.quic.*`) ve eskimiş `android.scaler.availableRawSizes`'ta geçiyor. Yani standart Camera2 uygulamaları ana kamerada en fazla 12,58 MP görüyor.
- **Uygulamalar:** AGC `org.codeaurora.snapcam` 8.4.300.414775575.18 kurulu; APK md5 `fa4066eb3bf82cc097906fd108073500`, depodaki **yamasız** `AGC8.4.300_V9.6_snap.apk` ile aynı (yamalı `ce65f862…` değil). Open Camera (`com.xiaomi.module.evaluation` 1.55) ve Xiaomi kamerası (`com.android.camera` 6.4.000380.1) kurulu; kutucuk uygulaması `com.ishtar.cammodes` yok. AGC ve Open Camera'nın `lastUpdateTime` değeri 2026-09-20.
- **AGC tercihleri (smoke):** `prefs.trap.armed = 10`: 12 tuzak anahtarının 10'u 37 değerinde. AOSPA'da bu durum kökteki `.agc` dosyalarının içe aktarılmasıyla oluşuyordu. `agc.pref_48m = absent` (anahtar prefs dosyasında yok; APK'da olup olmadığı ölçülmedi). `agc.pref_resolution = full` → türetilen arka boyut 4096x3072 (12,58 MP). AGC'nin bu durumda temiz çekip çekmediği ölçülmedi.
- **smoke.sh sınırı:** `sensor.*` ve `hal.*` alanları sabitlerini kurulu modülden okuyor; modül yokken geçersiz (`d41d8cd9…` boş girdinin md5'i).
- **Kod okuması:** `ishtar-cam-modes/post-fs-data.sh`, sensör md5'i `EXPECT_MD5` (:35-51) tutmazsa hiçbir şey mount etmez; HAL md5'i `HAL_STOCK_MD5` (:101-107) tutmazsa yalnız HAL katmanını atlar. Modül bugünkü hâliyle kurulursa sensör katmanı korumadan geçer, 50MP katmanı kapalı kalır [ÇIKARIM: işlevsel test yapılmadı].

Aşağıdaki her şey (2026-09-20 ölçümü, kanonik yapılandırma, son ölçümler, `F3.11-09`) önceki ROM'a, AOSPA A15'e aittir.

**2026-09-20 ölçümü** (DEV; salt-okur adb; ledger'da IMPL-96 satırının (4). maddesi, `:525`):
- **ROM:** AOSPA `Vauxite Unofficial`, Android 15 (SDK 35, `AQ3A.250604.001`, güvenlik yaması 2025-06-05).
- **Kernel:** `5.15.178-android13-8-g7b195d4db1e7`. Bu yalnız karşılaştırma tabanıdır, A16 derlemesinin girdisi değildir.
- **Bölümler ve güvenlik:** A/B (aktif slot `_a`), Virtual A/B, AVB 1.3, FBE, SELinux Enforcing. `/data`'da 405 G boş.
- **Root:** KernelSU Next `ksud 3.3.0`, yönetici `com.rifsxd.ksunext`, `zygisksu`, `magic_mount_rs` v4.0.8-900.
- **Modüller:** toplam 10. Aralarında `ishtar_cam_modes` v2.2 (13), `ishtar_aon_fix` v1.1 (2) ve `custom_camera` 6.4 var.
- **Kamera:**
  - Sensör `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` (stok).
  - Canlı HAL `fe0245a4720fb07b01d96deef47f5569` (yamalı kopya, bind-mount ile bağlı).
  - Stok HAL `c3fa63a86ee3ecaf9fbf02005d35f6b5`.
  - Mod `50mp`, dil `en`. Üç kamera servisi çalışıyor.
- **Kilit durumu:** Boot prop'ları kilidi açık cihazda da `locked`/`green` gösteriyor. Gerçek kilit durumu için `fastboot getvar unlock` kullanılmalı (DEV:108-112).

**Kanonik yapılandırma** (IMPL-87 bracket-A, 2026-09-08; bracket-C 2026-09-09'da 161/161 satır aynı; L:516-517):
- Modül v2.2/13, mod `50mp`, stok sensör, fullres HAL. İki bağlama sayısı da 1, `prefs.trap.armed=0`.
- AGC: `ce65f862…`, `pref_48m_key=0`, `pref_camera_resolution=full`; türetilen arka boyut `4096x3072`.

**Son ölçümler:**
- Open Camera 50.33 MP: siyah oranı 0.000008 (IMPL-85) ve 0.000009 (IMPL-87).
- AGC 12.58 MP: siyah oranı 0.001671 (IMPL-87).
- Stok Kamera videosu: 4K 59.88 fps, 1080p 60.06 fps (IMPL-88).
- Open Camera videosu ~30 fps; bu, seçili moddan bağımsız.

**Kanonik iddia `F3.11-09`** (aynen; kanonik kopyası CFG §10'da, ledger'da L:647):

> On a Xiaomi 13 Ultra running the `50mp` module mode with the shipped `fullres` HAL `fe0245a4720fb07b01d96deef47f5569` and the stock sensor `9e4d0fe1a8bf2eb4146c9917a0ac2c4c`, Google Camera `ce65f862c990e2acc02be356f75a7122` configured with `pref_48m_key=0` and `pref_camera_resolution=full` captures a clean 12.58 MP photograph — black fraction below `0.01` by the `IMPL-40` method — and that configuration survived AGC cold start, camera-stack restart, QuickSettings mode switch and device reboot with zero field changes (`IMPL-61`, four axes, no failures).

- **Kanıtlama:** `scripts/smoke.sh -o <snapshot>` şu alanları vermeli: `agc.pref_48m=0`, `agc.pref_resolution=full`, `agc.photo_size.back.derived=4096x3072`. Ardından siyah oranı < 0.01 olan bir çekim gerekir (L:649).
- **Kapsam:** yalnız arka kamera, tek cihaz, yalnız 12.58 MP (L:651).
- **Açık cihaz konuları (§5):**
  - FIND-3.10-02: tuzak anahtarlarını yeniden kuran yol hâlâ bilinmiyor.
  - FIND-9.1-04: modül güncellemesi `mode` dosyasını kaybediyor.
  - FIND-6.2-03: AON NCS sağlayıcıları bu ROM'da yok.
  - FIND-2.3-02/-03: `ln2`/`ln4` AGC'yi çökertiyor; AGC videosu stok durumda da siyah.

### 2.4 Plan durumu
- **42 alt plan** (faz başına 6/4/11/7/3/2/3/3/3):
  - 34 `verified`
  - 3 `implemented`: `Faz4.6`, `Faz6.1`, `Faz8.1`
  - 3 `planned`: `Faz7.2`, `Faz7.3`, `Faz8.3`
  - 2 `superseded`: `Faz4.1`, `Faz4.7`
  - Sayım ledger §4'ten, 2026-11-13'te yapıldı.
- Etkin snapshot'lar: `SNAP-2026-09-10-MAIN`, `SNAP-2026-09-10-SUBPLANS`.
- Ledger §5'te IMPL-01 … IMPL-95 kayıtlı; IMPL-96 de kayıtlı (`:525`); IMPL-18/19/20/22 için ayrıca anlatı blokları var.

| Alt plan | Durum | Engel → sıradaki eylem | Kaynak |
|---|---|---|---|
| `Faz4.1` | superseded | `DEC-14` (2026-09-03); yeniden canlandırılmaz | L:87; AUD:310 |
| `Faz4.6` | implemented (denetimde DEFERRED) | `F4.6-07` superseded `Faz4.1`'e bağlı, bu yüzden ulaşılamaz; tamamlamak yeni bir karar ve yeni bir alt plan gerektirir | L:92; AUD:309 |
| `Faz4.7` | superseded | `DEC-14`; yalnız bilgi sorusu olarak yeniden açılabilir | L:93; AUD:311 |
| `Faz6.1` | implemented | etkisi `Faz7.3`'teki AON adım 3'te doğrulanacaktı; derleme bırakıldığı için doğrulanamaz kaldı, koşu 21 karar verir | L:97 |
| `Faz7.2` | planned | 2026-11-13: ROM derleme bırakıldı (K2); koşu 21'de `superseded` olacak. Önceki sıra (`F7.2-01` → kiralama onayı → Part B) tarihsel | L:100; AUD:305 |
| `Faz7.3` | planned | 2026-11-13: amaçsız (K2); koşu 21'de `superseded` olacak | L:101; AUD:306 |
| `Faz8.1` | implemented | statik yarı bitti (IMPL-92); uzlaşma yarısı derleme bırakıldığı için yapılamaz; koşu 21 karar verir; `DEC-07` konusuz | L:102; AUD:307 |
| `Faz8.3` | planned | 2026-11-13: amaçsız (K2); koşu 21'de `superseded` olacak | L:104; AUD:308 |

- **11. denetimin kuyruğu** (2026-09-14, READY): `Faz7.2` → `Faz7.3` → `Faz8.1` uzlaşma yarısı → `Faz8.3`, hepsi READY_WITH_WARNINGS. **2026-11-13'ten beri geçersiz** (ROM derleme bırakıldı).
- **Görünür tutulması gereken 10 bulgu** (AUD:363-386):
  - P2 açık: `AUDIT-FIX-22`
  - P3 açık: `-37`, `-41`, `-42`, `-50`, `-55`, `-56`, `-57`
  - P3 kabul edilmiş: `-25`, `-33`
- **Sıradaki numaralar:** `IMPL-97`, planlama koşusu 21, 12. denetim. `DEC-27`…`DEC-32` ledger'da (`:605`–`:610`); sonraki boş numara `DEC-33`. *(2026-11-16 notu: `DEC-33` (K9) planlama koşusu 21 ile ledger `:619`'a yazıldı (`3 · O4`); sonraki boş numara `DEC-34`.)*
- **Açık kararlar:** K1–K8 yanıtlı (K7 = (a) → `DEC-32`; K8 = A → `DEC-31`, yürütüldü). K9 (50MP HAL yeniden türetmesi) ve push açık. Konusuz altı karar (`DEC-07`, `DEC-08`, `DEC-22`, `DEC-24`, `DEC-25`, `DEC-26`) `DEC-28` ile kapanır (ROM derleme bırakıldı; konusuz notları ledger'da `:582`, `:583`, `:599`, `:601`, `:603`, `:604`). `DEC-09` koşullu; ancak tetiklenirse gündeme gelir. Diğer tüm DEC'ler yanıtlandı. *(2026-11-16 notu: K9 yanıtlandı 2026-11-15, `3 · O0`: hayır, şimdilik (`DEC-33`); HAL katmanı HyperOS 4'te kapalı, sensör katmanı sürer.)*
- **Doğrulayıcı (Ö13):** depoda değil, ClaudeQB eklentisinin içinde duruyor. `py -3` (CPython 3.14.10) ile çalıştırılır.
  - Komut: `py -3 C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py --root . --mode all`
  - Sonuç: `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`. HEAD ağacında da aynı.
  - `--strict` ile bu uyarı `error=strict_warning=…` olur. Bu beklenen taban durumdur, gerileme değildir.
  - 2026-09-09 devrindeki "0 uyarı / 0 hata" tabanı yanlıştır.

### 2.5 Faz 7/8 cephesi
**2026-11-13: ROM derleme fikri bırakıldı (kullanıcı kararı, K2).** Telefon HyperOS 4 portuna geçtiği için Faz 7/8'in amacı (kiralık sunucuda AOSPA `beryl` derlemesi, Android 16 kamera işi, kernel LTS) ortadan kalktı; kiralama hiç yapılmadı. Ledger §7'deki duran tetikleyici "vendor blobs change through a system update" de ateşlendi. Resmî kapanış planlama koşusu 21'de (Step 1 değişikliği), kayıt `IMPL-96`'da (`DEC-28`; ledger `:606`; §7 üst girdisi `:550`). Bu bölümün geri kalanı tarihsel kayıttır.

**Derleme ortamı kararının geçmişi** (L:552, L:601-604):
1. WSL2 planı (IMPL-86, 2026-09-07).
2. `DEC-24` (2026-09-10): WSL2 bırakıldı; girdiler önce GitHub'a konacak, derleme kiralık bir sunucuda yapılacak.
3. `DEC-25` (2026-09-11): Hetzner CCX53; 10 saat tavan ve 8. saat kuralı; en çok 2 manifest-sınıfı düzeltme; sunucu kapatılmaz, silinir; iki derleme deposu herkese açık.
4. IMPL-94 kapısı 2026-09-13'te geçmedi. Ardından Hetzner'in yeni hesap limiti kullanıcıyı CCX33 ile sınırladı.
5. **`DEC-26` (2026-09-14): Scaleway POP2-32C-128G.**

**Kiralama hedefi (BE §1-4):**
- Sunucu: 32 vCPU / 128 GiB. Ubuntu 22.04; yedek seçenek 24.04 + `kernel.apparmor_restrict_unprivileged_userns=0`.
- Disk (Block volume'lar, toplam 610 GB):
  - boot 40 GB 5K
  - `ishtar-src` 310 GB 5K, `/android`'e bağlanır
  - `ishtar-out` 260 GB 15K, `/android/beryl/out`'a bağlanır
- Ağ: esnek IPv4.
- Derleme: ccache kapalı, `OUT_DIR` yok; komut `./rom-build.sh ishtar -z`.
- Maliyet: Instance €1.18/saat, tüm kaynaklar birlikte ~€1.28/saat. 10 saatlik tavan ≈ €12.8 + KDV.
- Kurallar:
  - 8. saatte artefaktlar geri alınır ve sunucu sökülür.
  - OOM'dan sonra yeniden deneme yapılmaz.
  - Düzeltmeler yalnız `~/evidence/fixes.diff`'e yazılır; oturum içinde push yapılmaz.
  - Söküm (teardown): Instance, 3 volume ve esnek IP silinir. Instance, volume, IP ve snapshot sayıları sıfır olmalıdır.

**Pinler** (L:520; AUD:88-90):
- `AOSPA/manifest` `beryl` `7dfc0650e27ec43b1d5cedf5e74213cf8667f2c2` (2026-05-24'ten beri değişmedi).
- `ahmetxa/android_local_manifests` `main` `22283d8a866d042e02336fcb4698253ac6bf9c3b`: 13 kaldırma ve 13 pin; `check.py` 26/26. BE §5 bu depoyu klonlayıp doğrular.
- Cihaz ağacı `beryl` `d48816f` (= upstream `df05661` + Faz6.1 satırı).
- Vendor `f92e7a9`; common `a0a7042`.
- Kernel: `msm-kernel` `1c509b3` (5.15.189) ve `common` `b11e560` (5.15.185).
- `hardware/xiaomi` `1a3e75d`; sepolicy `8dcddf5`; kamera vendor (GitLab) `b87ebc1`.
- İki derleme deposu herkese açık (`DEC-25`); sunucuda GitHub kimlik bilgisi yok.

**Kiralama kapısının durumu:**
- `F7.2-01` bir kez koştu (IMPL-94). §5 bloğu exit 0 verdi, ama kapı geçmedi:
  - Kontrol 4 (10 saatlik boş pencere): hayır.
  - Kontrol 1–2: yapılmadı.
  - Kontrol 3: PASS.
- IMPL-95 runbook'u Scaleway'e taşıdı. 10 bloğun hepsi `bash -n`'den geçiyor; ancak §7'deki volume bloğu hiç çalıştırılmadı.
- 11. denetimde `Faz7.2` READY_WITH_WARNINGS:
  - `AUDIT-FIX-55`: symlink adımında yalnız geri okuma + `bash -n` yapılır.
  - `-56`: VAL-SYNC, `22283d8` + `fixes.diff`'e göre değerlendirilir.
- **Hiçbir şey kiralanmadı; henüz hiç Android 16 artefaktı üretilmedi.**
- Sıra: Part A (ücretsiz) → DUR → kullanıcı onayı → Part B (runbook §6–13; sonuç ne olursa olsun söküm) (PRP:239-254).

**Faz 8:**
- `Faz8.1` statik yarı (IMPL-92): `f92e7a9`'da HAL md5 stok `c3fa63a8…` (27268688 B) ile, sensör md5 `9e4d0fe1…` ile aynı. İki katman da statik değerleriyle taşınıyor. `DEC-07` açık *(2026-11-14 notu: 2026-11-13'ten beri konusuz (`DEC-28`); §2.5'in giriş paragrafı bölümün kalanını tarihsel sayar.)*
- `Faz8.2` (IMPL-93) verified: hedef `android13-5.15-2026-06_r4`; 4472 / 3798 yalnız-hedef commit. Deneme birleştirmesinde 1 / 16 çakışma çıktı, hiçbiri kamera sürücüsünde değil. `DEC-08` için öneri: ertelemek.
- `Faz8.3` planned.

**Doğrulanmamış girdi ve çelişki:**
1. DEV §4 (2026-09-20): Kullanıcıya göre MIUI ve AOSPA'nın kerneli "has been upstreamed by third parties". K3 ile 2026-11-13'te düştü: telefon artık 5.15.215 kernelli HyperOS 4'te (§2.3).
2. **Çelişki (giderildi):** DEV §7 "An Android 16 build ships a different binary, so the table does not carry over" diyordu; oysa IMPL-92 (L:102, L:521) pinlenmiş A16 HAL'inin md5'ini stok korumayla eşit ölçmüştü. Cümle yerinde bırakıldı; 2026-11-13'te DEV §10'a düzeltme notu eklendi (`03b0898`). Android 16 derlemesi bırakıldığı için konu kapandı.

### 2.6 Bu oturumun durumu (Pencere 4 · O2, 2026-11-17)

- **Genel durum:** Pencere 4 · O2 (12. denetimin denetim kontratı; plan §8.3, Ek A.8) bitti. Kapanış `Window 4 O2: audit contract for the twelfth audit` (§11). Ledger, `Planner-docs/`, `docs/` ve Audit dokunulmadı; reviewer çalışmadı; cihaza komut gönderilmedi. Sıradaki aşama Pencere 4 · `O3a` (Faz10 incelemesi: `cov-a`, `rdy-a`, `sec-a`; bulgu dosyası doğar).
- **Açılış (2026-11-17T11:50:59Z–11:54:00Z):** kontrollerin hepsi tuttu: ağaç temiz, 89 commit, uç `Window 4 O1:`; `main` = `origin/main` = ls-remote'taki üç ref = `081790f`, `origin/main..HEAD` = 2; etiket yok, 355 dosya; snapshot aynı (plan §8.3 `W4O2OPN`).
- **Yayın:** değişmedi; `4 · O0`, `4 · O1` ve `4 · O2` commit'leri yerel. FF ve push yalnız `4 · O5`'te, `C4`'ten sonra, ayrı onaylarla (plan §8.2).
- **Taban (11:53:50Z–11:54:00Z):** `step2`, `step1`, `step3-preflight` `--strict` 0; `all` 0 (yalnız denetim uyarısı, `subplan_count=47`); V2 çıkış 1 (taban); V3 PASS; `step3` 0, `--strict` 1; kimlik taraması PASS (`prose_mentions=26`; Ek A.8'den sonra 27).
- **Kontrat (§8.3):** sekiz madde: reviewer girdisi ve dağıtım, dönüş biçimi, kimlik (`AUDIT-FIX-58`'den), bulgu dosyası `AUDIT12_FINDINGS.md`, `4 · O4` birleştirmesi, geçitler ve P0/P1 yolu, sahiplik, `PAT4`. İngilizce görev metni ve `PAT4` betiği Ek A.8'de.
- **Çalışma baytları (`W4O2P02`):** cov-a 374.145, rdy-a 389.140, sec-a 349.931, cov-b 385.848, cov-c 363.276, cov-d 372.294 B; 10 KB ek okumayla da ≤ 400 KB. cov-d sekiz emekli ya da ertelenmiş dosyanın hafif okumasıyla bölünmedi (alt planlar 224.903 B).
- **`PAT4` kalibrasyonu (`W4O2P01`):** Faz 1–9'un 42 alt planında 14 desen, 164 isabet (S1 17, S2 3, S3 12, S7 1, R1 6, R3 20, R4 81, R5 24); yalnız sayı ve konum.
- **Silinecek depolar (`DEC-30`):** `gh api -i` 11:50:59Z–11:51:01Z'de dört depo 200; silme cümleleri değişmedi; silme kullanıcıda.
- **Bağlam:** ilk ölçüm 58k; tasarım ölçümlerinden sonra 181k; §8.3'ten sonra 237k; kapanış §11'de.
- **Değişen dosyalar:** `ORCHESTRATION_PLAN.md` (§1 `4 · O2` satırı, §3 Adlandırma, yeni §8.3, yeni Ek A.8), `PROJECT_LOG.md` (§2.6, §11), `NEXT_PROMPT.md` (`4 · O3a` için).
- **Bekleyen işler ve devam:** Pencere 4 · `O3a` (yeni oturum, `NEXT_PROMPT.md`; plan §8.3, Ek A.8); ardından `4 · O3b`, `4 · O4` birleştirme ve geçitler, `4 · O5` kapanış (plan §8.2).

## 3. Kronoloji

### 3.1 Faz bazında özet
Durumlar ledger §4'ten, hedef ve sonuçlar MP §6'dan alındı (MP:131-241; AUD:107-115). Kaldırılan ve superseded alt planlar, ait oldukları fazın altında belirtildi.

**Faz 1 — Çalışma alanı güvenlik ağı.** Hedef: kurtarılabilir bir çalışma alanı ve yazılı adımlardan yeniden kurulabilen bir araç zinciri. Sonuç: git, kök README, biçim ve araç sözleşmeleri. Durum: 6/6 verified (2026-08-24…08-30).
- `Faz1.1` version-control-bootstrap — verified (IMPL-01): git, 86 dosya.
- `Faz1.2` signing-key-containment — verified (IMPL-02): 5 arşiv temiz.
- `Faz1.3` patch-table-format-contract — verified (IMPL-06): `docs/patch-table-format.md`.
- `Faz1.4` toolchain-procedure-record — verified (IMPL-07); `VAL-TOOLCHAIN` ertelendi (`java` yok).
- `Faz1.5` static-safety-probes — verified (IMPL-05): FIND-1.5-01/02/03.
- `Faz1.6` workspace-readme-and-refs-index — verified (IMPL-08): `README.md`.

**Faz 2 — v2.1'i yayımla ve yeniden taban al.** Hedef: yayımlanan sürüm, doğrulanan sürümle aynı olsun. Sonuç: v2.1 flaşlandı, `BASELINE-2026-08-31-V21` alındı, ilk regresyon kaydı (`docs/regression-v2.1.md`) yazıldı. Durum: 4/4 verified (2026-08-30…09-06).
- `Faz2.1` device-smoke-script — verified (IMPL-04): `scripts/smoke.sh`.
- `Faz2.2` flash-v21-and-baseline-snapshot — verified (IMPL-09…12).
- `Faz2.3` ten-mode-regression-pass — verified (IMPL-13).
- `Faz2.4` tiles-hide-disposition — verified (IMPL-71, 75): `DEC-02` ile seçenek korundu, metinler düzeltildi.

**Faz 3 — 50 MP altında AGC 12.6 MP'de sabit.** Özgün hedef "AGC'de uçtan uca 50 MP" idi. `DEC-14` ile 2026-09-03'te emekliye ayrıldı ve yerine Faz3.7–3.11 yazıldı. Hedef: 50 MP katmanı açıkken AGC temiz ve tekrarlanabilir şekilde 12.58 MP çeksin; Open Camera 8192x6144 çekmeye devam etsin. Sonuç: `pref_48m_key=0` + `pref_camera_resolution=full` ayarı ve kanonik iddia `F3.11-09` (§2.3). Durum: 11/11 verified; faz 2026-09-05'te kapandı, `DEC-21` 2026-09-10'da verildi.
- `Faz3.1` preference-trap-clearance — verified (IMPL-16): giriş kapısı; bütçe 15 site / 2 oturum.
- `Faz3.2` pixel-array-write-site-search — verified (IMPL-18): yazım sitesi 15 adaydan 3.'sünde bulundu.
- `Faz3.3` single-word-patch-and-metadata-proof — verified (IMPL-20): tek kelimelik yama, ilk denemede tuttu.
- `Faz3.4` consumer-compatibility-check — verified (IMPL-21, 22): hiçbir tüketici uygulama bozulmadı.
- `Faz3.5` agc-capture-and-image-evidence — verified (IMPL-23): AGC 50.3 MP çekti ama görüntü bozuk.
- `Faz3.6` fallback-decision-gate — verified (IMPL-24): PRIMARY SUCCESS; sonradan `DEC-14` ile geçersiz kaldı.
- `Faz3.7` agc-photo-size-pin — verified (IMPL-52…54): boyutu sabitleme yolu bulundu.
- `Faz3.8` agc-state-in-smoke-script — verified (IMPL-55, 56): smoke betiğine AGC alanları eklendi.
- `Faz3.9` coexistence-bracket — verified (IMPL-57, 58, 83); FIND-3.9-02 IMPL-85 ile kapandı.
- `Faz3.10` pin-stickiness-matrix — verified (IMPL-59…61): 4 eksenin 4'ünde dayandı; FIND-3.10-03.
- `Faz3.11` phase-closure-and-configuration-record — verified (IMPL-62, 63, 89): CFG ve `F3.11-09`.

**Faz 4 — Asgari doğru HAL yaması.** Hedef (`DEC-14` sonrası): tutarlı, paketlenebilir ve md5 korumalı geniş bir tablo; daraltma yok. Sonuç: sevk edilen `blobs/hal-fullres.patch` kanonik kaldı; deneyler `agc-50mp-yama/` altında yerinde işaretli. Durum: 4 verified, 1 implemented, 2 superseded.
- `Faz4.1` fullres-dimension-guard — superseded, 2026-09-03 (IMPL-25, 34, 48–50). Daraltma sayısal hedefleri tuttu ama AGC açılmaz oldu; binary'de ek kod için boşluk da yok. Yeniden canlandırılmaz.
- `Faz4.2` duration-rows — verified (IMPL-64): öncül yanlış çıktı, uygulanacak satır yok.
- `Faz4.3` patch-table-consolidation — verified (IMPL-65, 66): tablo değişmedi.
- `Faz4.4` patch-compatibility-validation — verified (IMPL-67, 68, 70): dağıtım kapısı geçti (`docs/patch-validation-phase4.md`).
- `Faz4.5` active-array-raise — verified (IMPL-27…30): metadata düzeldi, görüntü düzelmedi.
- `Faz4.6` raw-payload-geometry-diagnosis — implemented; denetimde DEFERRED (IMPL-31, 33, 35…46; ledger §4 satırı yalnız 31/33/35'i listeliyor). Bulgu: iki bağımsız hata var, binned okuma ve stride uyumsuzluğu.
- `Faz4.7` ultra-high-resolution-sensor-mode — superseded, 2026-09-03 (IMPL-47, 48, 51). Yalnız bir bilgi sorusu olarak yeniden açılabilir.

**Faz 5 — Mode-0 12-bit kompozisyonu.** Hedef: 50 MP ile LN modlarını birlikte çalıştırmak. Sonuç: kompozisyon kanıtlandı ama bilinçli olarak benimsenmedi; dışlama kuralı korundu. Durum: 3/3 verified; faz 2026-08-31'de kapandı.
- `Faz5.1` twelve-bit-mode-zero-blob — verified (IMPL-14): aday blob `80b53215356c57b156f2bb2918cf067a`, `blobs/` dışında tutuluyor.
- `Faz5.2` temporary-mount-composition-test — verified (IMPL-15).
- `Faz5.3` exclusion-rule-disposition — verified (IMPL-17).

**Faz 6 — AON düzeltmesini cihaz ağacına taşı.** Hedef: `ishtar-aon-fix` ihtiyacını cihaz ağacındaki bir düzeltmeyle ortadan kaldırmak. Sonuç: `;SYMLINK=` satırı iki ağaca eklendi; modül ayrı kalıyor (`DEC-04`). Durum: 1 verified, 1 implemented.
- `Faz6.1` symlink-entry-in-device-trees — implemented (IMPL-03); etkisi `Faz7.3`'te doğrulanacak. *(2026-11-14 notu: `Faz7.3` 2026-11-13'ten beri amaçsız (`DEC-28`); durum `implemented` kalıyor.)*
- `Faz6.2` aon-module-disposition — verified (IMPL-72, 75): `docs/aon-verification.md`; FIND-6.2-03.

**Faz 7 — Android 16 derleme ortamı.** Hedef: AOSPA `beryl` derlemesini en düşük kira maliyetiyle almak. Sonuç: girdiler GitHub'da, runbook hazır; kiralama hiç yapılmadı; ROM derleme 2026-11-13'te bırakıldı (`DEC-28`). Durum: 1 verified, 2 planned.
- `Faz7.1` github-input-staging — verified (IMPL-86, 89, 90, 91). Run 18 (2026-09-10) ile kaldırılan `Faz7.1-wsl2-provisioning.md`'nin yerini aldı.
- `Faz7.2` first-aospa-build — planned; run 18'de yerinde yeniden yazıldı; 11. denetimin kuyruğunun başındaydı; bu kuyruk 2026-11-13'ten beri geçersiz (`DEC-28`).
- `Faz7.3` flash-boot-and-aon-verification — planned; run 18'de eklendi.

**Faz 8 — Android 16'da kamera ve kernel LTS.** Hedef: kamera işini `beryl` blob'larında sürdürmek ve kerneli güncel LTS'e taşımak. Sonuç: statik taşıma doğrulandı; kernel birleştirmesi için öneri "ertele". *(2026-11-14 notu: Faz 8 2026-11-13'ten beri amaçsız ve `DEC-08` konusuz (`DEC-28`); resmî kapanış planlama koşusu 21'de.)* Durum: 1 verified, 1 implemented, 1 planned.
- `Faz8.1` android16-camera-blob-comparison — implemented (IMPL-89, 92). Run 18 ile kaldırılan `Faz8.1-beryl-port-sizing.md`'nin yerini aldı.
- `Faz8.2` kernel-lts-merge-scoping — verified (IMPL-93); run 18'de yerinde yeniden yazıldı.
- `Faz8.3` camera-modes-on-android16-build — planned; run 18'de eklendi.

**Faz 9 — Sürüm mühendisliği.** Hedef: betikle derlenen, betikle doğrulanan ve tek yerde belgelenen sürümler. Sonuç: `scripts/build-release.py`, `docs/release-checklist.md`, `docs/recovery-runbook.md`, `CHANGELOG.md` ve v2.2. Durum: 3/3 verified.
- `Faz9.1` reproducible-release-build — verified (IMPL-76, 81).
- `Faz9.2` release-verification-checklist — verified (IMPL-19, 78–82, 85, 87–89).
- `Faz9.3` documentation-consolidation — verified (IMPL-77, 78, 81); FIND-9.3-01 hâlâ açık.

### 3.2 Uygulama koşuları
Ledger §5'teki her koşu için bir satır var ve satırlar numara sırasındadır. Ledger'daki fiziksel sıra yer yer farklıdır (§8). Kanıt sütunu ledger satırını, varsa ana snapshot'ı da gösterir.

| IMPL | Tarih | Alt plan | Ne yapıldı | Sonuç | Kanıt |
|---|---|---|---|---|---|
| IMPL-01 | 2026-08-24 | Faz1.1 | `git init`, `.gitignore`/`.gitattributes` yazıldı, 86 dosya izlendi | 7/7; `ff6934e`; AUTOPSY-P0-01 çözüldü; `device_ishtar/` kapsam dışı bırakıldı | L:113 |
| IMPL-02 | 2026-08-24 | Faz1.2 | 5 sürüm arşivinde dosya adı düzeyinde keystore denetimi | hepsi temiz; `DEC-05` kapandı, `DEC-10` açıldı | L:115 |
| IMPL-03 | 2026-08-24 | Faz6.1 | iki cihaz ağacına `aon_front.pb;SYMLINK=` satırı eklendi | düzenleme tamam; etkisi doğrulanmadı (derleme yok) | L:117 |
| IMPL-04 | 2026-08-30 | Faz2.1 | salt-okur `scripts/smoke.sh` ve snapshot adlandırma kuralı | 9/9; cihaz v2.0/11 ile `dcgB` modunda bulundu; H-10 çürütüldü | L:125; snap 20260830-1842 |
| IMPL-05 | 2026-08-30 | Faz1.5 | 6 betiğin statik güvenlik yoklaması, WebUI izi | 8/8; FIND-1.5-01/02/03; OQ-05…08 yanıtlandı | L:142 |
| IMPL-06 | 2026-08-30 | Faz1.3 | yama tablosu biçim sözleşmesi | 8/8; gidiş-dönüş testi geçti; tablolar sıralı zincirlenir | L:163 |
| IMPL-07 | 2026-08-30 | Faz1.4 | araç zinciri kaydı | 7/8; VAL-DISASM geçti, VAL-TOOLCHAIN ertelendi (`java` yok); CPython 3.14.7 mevcut | L:174 |
| IMPL-08 | 2026-08-30 | Faz1.6 | kök README, `refs/` dizini, 15 sağlama toplamı | 8/8; 36 kök girdi; AUDIT-FIX-04 kapandı | L:185 |
| IMPL-09 | 2026-08-31 | Faz2.2 | v2.1 zip doğrulandı (42 girdi); flaş öncesi bracket alındı; kurtarma yolu denendi | flaş kapısında durdu; disable/restore bayt-özdeş; FIND-2.2-01/02/03 | L:209; snap 20260831-1533…1541 |
| IMPL-10 | 2026-08-31 | Faz2.2 | devam; cihaz `stock` modunda bulundu | RAW12/RAW10 ilanı blob içeriğine göre değişiyor | L:211; snap 20260831-1557 |
| IMPL-11 | 2026-08-31 | Faz2.2 | kullanıcı v2.1'i KernelSU-Next ile flaşladı | 3 satırlık diff açıklandı; `BASELINE-2026-08-31-V21`; EV-14 kapandı | L:213; snap 20260831-1607 |
| IMPL-12 | 2026-08-31 | Faz2.2 | kullanıcının görsel kontrolleri, `50mp` gözlemleri | 10/10 tamam; OQ-17: 13 kamera kimliğinin hepsi etkileniyor | L:215; snap 20260831-1626 |
| IMPL-13 | 2026-08-31 | Faz2.3 | on modlu regresyon (kalıcılık, video) | modül kontrol ettiği her şeyde doğru; FIND-2.3-01…06 | L:217 |
| IMPL-14 | 2026-08-31 | Faz5.1 | `dcgB.bin`'den 12-bit mode-0 adayı üretildi (host) | 9/9; 1,062,250 B; yalnız mode 0 farklı; FIND-5.1-01 | L:300 |
| IMPL-15 | 2026-08-31 | Faz5.2 | fullres HAL + aday sensörle geçici bağlama | kompozisyon çalışıyor: Open Camera 8192x6144, bozulma yok | L:312; snap 20260831-1906…1920 |
| IMPL-16 | 2026-08-31 | Faz3.1 | eski Faz 3 giriş kapısı | tuzak 0/12; bütçe 15 site / 2 oturum; FIND-3.1-01 (disassembler yok) | L:324 |
| IMPL-17 | 2026-08-31 | Faz5.3 | dışlama kuralı kararı | dışlama korundu (kompozisyon kanıtlandı, benimsenmedi); Faz 5 kapandı | L:340 |
| IMPL-18 | 2026-09-01 | Faz3.2 | pixelArraySize yazım sitesinin statik araması | 15 adaydan 3.'sünde bulundu; kayıtlı 9 site yanlış pozitif; H-01 çürütüldü | L:350, L:385 |
| IMPL-19 | 2026-09-01 | Faz9.2 (öne çekildi) | kurtarma runbook'u (F9.2-05…07) | modül `/odm`'a yazmıyor; CQ-09 yanıtlandı; FIND-9.2-01 | L:344, L:409 |
| IMPL-20 | 2026-09-01 | Faz3.3 | stok tabanda tek kelimelik yama + metadata okuma | ilk denemede pixelArraySize 4096x3072 → 8192x6144; geri dönüş bayt-özdeş; bütçe 4/15 | L:345, L:421 |
| IMPL-21 | 2026-09-01 | Faz3.4 | 9 tüketici yüzeyi için beklenti tablosu | tamam; 3 satırın önceki kaydı yoktu | L:346 |
| IMPL-22 | 2026-09-01 | Faz3.4 | iki tabanda tüketici taraması | Open Camera 50.3 MP; 1080p60/4K60; FOV değişmedi; FIND-3.4-01/02/03 | L:347, L:441 |
| IMPL-23 | 2026-09-01 | Faz3.5 | üç katmanlı yığın + AGC çekimleri | libgcam kapısı aşıldı; 50.3 MP ama görüntü geometrik olarak bozuk (FIND-3.5-01, P1) | L:348 |
| IMPL-24 | 2026-09-01 | Faz3.6 | karar kapısı (yama yok) | kullanıcı kararı: PRIMARY SUCCESS; eski Faz 3 kapandı | L:349; snap 20260901-1332 |
| IMPL-25 | 2026-09-01 | Faz4.1 | yürütme öncesi inceleme (koşu değil, durma olayı) | 2 kusur + 1 belirsizlik; `DEC-11`, `DEC-12` | L:351 |
| IMPL-26 | 2026-09-01 | ledger | AUDIT-FIX-06/07/12 düzeltme geçişi | giderildi; alt plan sayısı 33 | L:352 |
| IMPL-27 | 2026-09-01 | Faz4.5 | host: active-array etiketlerinin yazım siteleri | bulundu; QTI vendor etiketi statik olarak yamalanamıyor; bütçe 6/15 | L:353 |
| IMPL-28 | 2026-09-01 | Faz4.5 | ilk active-array etiketi canlı uygulandı | md5 tuttu; FIND-4.5-01; DUR: harness kapısı geri dönüşü engelledi | L:354; snap 20260901-1742 |
| IMPL-29 | 2026-09-01 | Faz4.5 | kullanıcı elle geri aldı; ikinci etiket tek başına denendi | md5 tuttu; iki geri dönüş de bayt-özdeş | L:355; snap 20260901-1756…1759 |
| IMPL-30 | 2026-09-01 | Faz4.5 | yedi kelimelik yığın + `pref_48m_key=1`, AGC çekimi | 50.3 MP ama %75 siyah; FIND-4.5-02 (P1); `DEC-13` | L:356; snap 20260901-1811 |
| IMPL-31 | 2026-09-01 | Faz4.6 | orijinal JPEG'lerde host tarafı geometri teşhisi (öncesinde `4897a9b`) | yarım genişlikteki veri tam genişlikte rastere yazılmış; FIND-4.5-02 "kapandı" diye kaydedildi (sonra yeniden açıldı, `DEC-19` ile bilgi olarak tutuluyor) | L:357, L:641 |
| IMPL-32 | 2026-09-01 | ledger, Ontology, Comprehension | sözlük normalizasyonu | doğrulayıcı uyarısı 11→0; AUDIT-FIX-11/14/15/16 giderildi | L:359 |
| IMPL-33 | 2026-09-02 | Faz4.6 | yedi kelimelik yığında canlı ölçüm | stok kamera 8192x6144'te temiz, yani hata AGC'nin Gcam yolunda; stride loglarda görünmüyor | L:358; snap 20260902-1355…1420 |
| IMPL-34 | 2026-09-02 | Faz4.1 | host yarısı: kamera başına hedefler yamadan önce yazıldı, koruma tasarlandı | tamam; canlı adım kullanıcıya bırakıldı; yinelenen bir koşu numarası düzeltildi | L:460 |
| IMPL-35 | 2026-09-02 | Faz4.6 | EV-44 denemesi: AGC, yedi kelime, `pref_48m_key=1` | BAŞARISIZ: 12.6 MP, siyah 0.7493, 15/15 kare reddedildi | L:461; snap 20260902-1930 |
| IMPL-36 | 2026-09-02 | Faz4.6 | host: log sırası ve APK içerikleri | ret, ham veride bir CPU kontrolünden geliyor; SABRE eşleme hataları neden değil | L:462; snap 20260902-1930 |
| IMPL-37 | 2026-09-02 | Faz4.6 | gcam reddinin host tarafı çözümlemesi | hüküm "all_black", ham keskinlik ölçümünden | L:463 |
| IMPL-38 | 2026-09-02 | Faz4.6 | log sırası denetimi | önceki kayıt düzeltildi: çekim 4096x3072'de yapılmış; tam akışta hiç çekim olmamış | L:464; snap 20260902-2020 |
| IMPL-39 | 2026-09-02 | Faz4.6 | AGC ve stok kamera akış boyutları | cameraserver kısıtlamıyor; stok kamera 50 MP için YUV remosaic yolunu kullanıyor | L:465; snap 20260902-2030 |
| IMPL-40 | 2026-09-02 | Faz4.6 | pozitif kontrol: kullanıcının yarım çözünürlük çekimi | temiz 12.6 MP, siyah 0.0024 (başarısız çekimde 0.7498); hata istek ile teslim arasındaki uyumsuzluk; siyah oranı ölçüm yöntemi bu koşudan geliyor | L:466; snap 20260902-2127 |
| IMPL-41 | 2026-09-02 | Faz4.6 | host, kullanıcının "A yönü": binning, sensör mod tablosu, vendor HAL | binning ipucu çürütüldü; AGC sensör modunu seçemiyor; tek bir 8192x6144 mod var | L:467 |
| IMPL-42 | 2026-09-02 | Faz4.6 | CamX sensör modu loglamasını açma denemesi (canlı) | BAŞARISIZ: log maskeleri etkisiz; bracket'ler özdeş | L:468; snap 20260902-2228 |
| IMPL-43 | 2026-09-02 | Faz4.6 | EV-44 yapıldı (deklanşör adb ile) | istek ve akış ilk kez 8192x6144, görüntü 50.33 MP; ama siyah 0.7497: UHR yeteneği yok, sensör binned okuyor | L:469; snap 20260902-2242 |
| IMPL-44 | 2026-09-03 | Faz4.6 | UHR yeteneği ve max-res etiketleri yayınlandı | md5 tuttu; 13 kamera sağlam; görüntü değişmedi (siyah 0.7502) | L:470; snap 20260903-0857 |
| IMPL-45 | 2026-09-03 | Faz4.6 | `tools/pixelmode-probe/` istemcisi | tam boy max-res akışı mümkün değil (yalnız 1920x1080 yayınlı); katlanma bir stride hatası | L:471; snap 20260903-0938 |
| IMPL-46 | 2026-09-03 | Faz4.6 | katlanmayı açma testi (host) | tutuyor: siyah 0.0000, eksik veri yok; iki bağımsız hata; UHR hattının sahibi olan bir alt plan yok | L:472; snap 20260903-0950 |
| IMPL-47 | 2026-09-03 | Faz4.7 | max-res tablosunun kaynağı | tablo çalışma zamanında, Faz4.1'in yamaladığı fonksiyonda kuruluyor; Faz4.7 kendi kuralı gereği durdu | L:473 |
| IMPL-48 | 2026-09-03 | Faz4.1 | canlı, 4 bracket'li aşama | tüm md5'ler ve hedefler tuttu (hal0 468, hal3 520); tam çözünürlüklü RAW_SENSOR elde edilemedi; geri dönüşte 0/240 satır fark | L:474; snap 20260903-1500 |
| IMPL-49 | 2026-09-03 | Faz4.1 | F4.1-07 koruma kontrolü (adb) | BAŞARISIZ: daraltma AGC'yi 3/3 çökertiyor; geniş taban 4/4 açılıyor | L:475; snap 20260903-1700 |
| IMPL-50 | 2026-09-03 | Faz4.1 | bisection ve ek format-32 tasarımı | C aşaması 3/3 çöküyor; binary'de boş kod alanı yok; Faz4.1 bloke | L:476 |
| IMPL-51 | 2026-09-03 | Faz4.7 | satır sayısının izi (host) | sayı kamera başına döngü mantığından geliyor, statik tablodan değil; soru daraldı ama kapanmadı | L:477 |
| IMPL-52 | 2026-09-04 | Faz3.7 | boyut anahtarını pref yazımıyla ve ayar ekranıyla sabitleme | BAŞARISIZ: anahtar her açılışta yeniden türetiliyor; `DEC-15`, `DEC-17` | L:478; snap 20260904-1630 |
| IMPL-53 | 2026-09-04 | Faz3.7 | HAL sevk edilen `fe0245a4…`'e alındı (`DEC-15`); `pref_48m_key` 1→0 (`DEC-17`) | GEÇTİ: 4096x3072 türetiliyor; RAW10 ve YUV akışları eşleşiyor | L:479; snap 20260904-1825…1834 |
| IMPL-54 | 2026-09-04 | Faz3.7 | sabitlenmiş durumda kullanıcı çekimi | 12.58 MP, siyah 0.0027; `DEC-18`: 0 değeri benimsendi | L:480; snap 20260904-1831 |
| IMPL-55 | 2026-09-05 | Faz3.8 | `scripts/smoke.sh`'e beş AGC durum alanı | host kontrolleri geçti; canlı adım bekletildi | L:481; snap 20260905-1116 |
| IMPL-56 | 2026-09-05 | Faz3.8 | `pref_48m_key` 0→1→0 duyarlılık testi | tam 4 satır değişti; prefs geri yüklendi; tamam | L:482; snap 20260905-1148 |
| IMPL-57 | 2026-09-05 | Faz3.9 | oturum öncesi kontroller | Open Camera `com.xiaomi.module.evaluation` paket adıyla kurulu (FIND-3.9-01) | L:483 |
| IMPL-58 | 2026-09-05 | Faz3.9 | birlikte yaşama oturumu | AGC 12.58 MP ve Open Camera 50.33 MP, ikisinde de siyah 0.0000; 0/159 satır fark | L:484; snap 20260905-1515 |
| IMPL-59 | 2026-09-05 | Faz3.10 | kontrol tahmini testten önce yazıldı | katlanma bandı 0.7497–0.7502 olarak belirlendi | L:485; snap 20260905-1517 |
| IMPL-60 | 2026-09-05 | Faz3.10 | eksen 1–2 (soğuk başlatma, kamera yığınının yeniden başlatılması) | sabitleme dayandı; smoke betiğinde yarış durumu bulundu (FIND-3.10-01) | L:486; snap 20260905-1532 |
| IMPL-61 | 2026-09-05 | Faz3.10 | eksen 3–4 ve negatif kontrol | sabitleme 4 eksenin 4'ünde dayandı; kontrol tahmini tutmadı, iki temiz 50.33 MP çekim çıktı (FIND-3.10-03) | L:487; snap 20260905-1553 |
| IMPL-62 | 2026-09-05 | Faz3.11 | yapılandırma kaydı (CFG) ve kontrol listesi düzeltmeleri | GEÇTİ; FIND-3.7-01 kapandı | L:488 |
| IMPL-63 | 2026-09-05 | Faz3.11 | belgenin harfiyen geri okunması | tarif prefs dosyasını boşalttı; yedekten geri dönüldü, tarif korumalı hale getirildi; 12.58 MP siyah 0.0001; Faz 3 kapandı | L:489; snap 20260905-1910 |
| IMPL-64 | 2026-09-05 | Faz4.2 | statik ve salt-okur süre satırı sayımı | öncül yanlış: satırlar zaten tam; eksik 6 RAW stall satırı yamalanamıyor; hiçbir şey uygulanmadı | L:490; snap 20260905-1953 |
| IMPL-65 | 2026-09-05 | Faz4.3 | kanonik tablonun gidiş-dönüş testi | stok HAL'den `fe0245a4…` yeniden üretildi; koşu kullanıcıya düşen bir soruda durdu | L:491; snap 20260905-2001 |
| IMPL-66 | 2026-09-05 | Faz4.3 | kullanıcının "A okuması" kararından sonra | tablo değişmedi; 11 deney yerinde işaretlendi; tamam | L:492 |
| IMPL-67 | 2026-09-05 | Faz4.4 | salt-okur ölçüm | sevk edilen tabanda 8192x6144'te RAW yok; FIND-4.5-01 bu tabanda oluşmuyor; FIND-4.4-01 | L:493; snap 20260905-2017 |
| IMPL-68 | 2026-09-05 | Faz4.4 | birlikte yaşama çekimleri | VAL-AGC GEÇTİ: AGC 12.58 MP, Open Camera iki kez 50.33 MP, siyah 0.0000 | L:494; snap 20260905-2030, -2034 |
| IMPL-69 | 2026-09-05 | Faz4.4 | kuyruk kontrolü | başlatılabilecek her satır kullanıcıyı bekliyor; FIND-4.4-03 | L:496 |
| IMPL-70 | 2026-09-06 | Faz4.4 | stok kamera, video, 10 mod, reboot | GEÇTİ; arka kamera 12.58 MP, 60.0/59.8 fps; ön kamera 31.96 MP (FIND-4.4-04); tamam | L:497; snap 20260906-1225 |
| IMPL-71 | 2026-09-06 | Faz2.4 | statik inceleme | AOSPA Launcher3 `pm disable`'ı uygulamıyor; modül tarafında çözüm yok | L:498 |
| IMPL-72 | 2026-09-06 | Faz6.2 | statik inceleme | öneri: AON modülü ayrı kalsın; `docs/aon-verification.md` yazıldı | L:499 |
| IMPL-73 | 2026-09-06 | Faz9.1 | kuyruk değerlendirmesi | FIND-4.4-03 yanıtlandı; `DEC-02`/`DEC-04` beklendiği için başlamadı | L:500 |
| IMPL-74 | 2026-09-06 | ledger | kuyruk kapısı | çift `DEC-02` satırı silindi | L:501 |
| IMPL-75 | 2026-09-06 | Faz2.4, Faz6.2 | `DEC-02` ve `DEC-04` kararlarından sonra | ikisi de tamam; `tiles` çıktısı düzeltildi; AON bağlaması etkin ama NCS sağlayıcıları yok | L:502; snap 20260906-1305 |
| IMPL-76 | 2026-09-06 | Faz9.1 | deterministik derleme betiği | 3 derlemede aynı sha256 (ara derleme); kurulum yapılmadı | L:505 |
| IMPL-77 | 2026-09-06 | Faz9.3 | belge konsolidasyonu | GEÇTİ; eski AGC neden iddiası düzeltildi; sürüm geçmişi `CHANGELOG.md`'ye taşındı | L:506 |
| IMPL-78 | 2026-09-06 | Faz9.2 | sürüm kontrol listesi | 18 yetenek; kapsama 18/18 | L:507 |
| IMPL-79 | 2026-09-06 | Faz9.2 | F9.2-09 (QAS-01) | CQ-09/ARC-11 kayıtları uzlaştırıldı; kapandı | L:508 |
| IMPL-80 | 2026-09-06 | Faz9.2, Faz9.3 | kullanıcının toplu işi: v2.2/13, `DEC-10`, `DEC-20` (`smoke.sh` onarımı), FIND-9.2-02 | arşiv md5 `e9578957…`; onarımlar yalnız fixture'larda kanıtlandı | L:509 |
| IMPL-81 | 2026-09-06 | Faz9.2 (+9.1, 9.3) | VAL-INSTALL (kurulum + reboot), bilinen-kötü testi, stok modda AON | GEÇTİ; smoke onarımı cihazda doğrulandı; FIND-9.1-04 doğrulandı | L:510; snap 20260906-2055…2101 |
| IMPL-82 | 2026-09-06 | Faz9.2 | VAL-MANUAL'ın makine yarısı; önceki altı koşu commit'lendi | GEÇTİ; FIND-9.2-05 | L:511; snap 20260906-2346, -2351 |
| IMPL-83 | 2026-09-06 | Faz3.9 | `/data/local/tmp/occatch.sh` ölçüm aracı | araç kanıtlandı; çekim hâlâ yapılmadı | L:512; snap 20260906-2356 |
| IMPL-84 | 2026-09-07 | ledger §4 | matris ile §5'in uzlaştırılması | VAL-MANUAL'ın gerçek durumu 0/7 satır (FIND-9.2-06) | L:513 |
| IMPL-85 | 2026-09-07 | Faz9.2, Faz3.9 | VAL-MANUAL'ın 7 kullanıcı satırı | PC-05 50.33 MP siyah 0.000008; PC-13 30.03 fps; Faz9.2 verified; FIND-3.9-02 kapandı | L:514; snap 20260907-0032, -0055 |
| IMPL-86 | 2026-09-07 | Faz7.1 (eski WSL2 planı) | F7.1-01; kuyruk §4 matrisine göre ölçüldü | `DEC-22` açıldı | L:515 |
| IMPL-87 | 2026-09-08 | Kamera-Teyit (ledger satırı Türkçe) | v2.2 sonrası güvence tekrarı, reinstall yok | 50.33 MP siyah 0.000009; 12.58 MP siyah 0.001671; Open Camera videosu ~30 fps (FAIL) | L:516; snap 20260908-1935, -2030 |
| IMPL-88 | 2026-09-09 | PC-13 (ledger satırı Türkçe) | stok Kamera ile 60 fps yeniden ölçümü | GEÇTİ: 4K 59.88 fps, 1080p 60.06 fps | L:517; snap 20260909-1726 |
| IMPL-89 | 2026-09-10 | ledger | `DEC-16/21/23/24` kaydedildi, `DEC-22` yeniden çerçevelendi, `DEC-01` eklendi; `gh` 2.100.0 kuruldu | WSL2 emekli; `beryl`'in ikinci bir cihaz değil, AOSPA'nın Android 16 dalı olduğu düzeltildi | L:518; snap 20260910-1231 |
| IMPL-90 | 2026-09-10 | GitHub hazırlığı (`DEC-24`, `DEC-01`) | tüm geçmiş kimlik bilgisi için tarandı; özel `ahmetxa/ishtar`'a `main` = `f8a05ca` itildi; cihaz ağacı `beryl` `d48816f`; manifest deposu `4182695` | hazır ama henüz derlenemez; ilk cihaz ağacı itmesi commit'siz gitti, kusur beyan edilip düzeltildi (ders: her yayın geri okumayla doğrulanır) | L:519 |
| IMPL-91 | 2026-09-11 | Faz7.1 | F7.1-01…12: manifest 13 projeyi kaldırıp `beryl` kaynaklarını pinliyor; runbook BE yazıldı | verified; `22283d8` doğrulamalı itildi; iki derleme deposu açık; VAL-PINS 26/26; `DEC-22`, `DEC-25` | L:520 |
| IMPL-92 | 2026-09-11 | Faz8.1 | statik yarı: `f92e7a9` blob'ları çalışma alanı dışında karşılaştırıldı | HAL ve sensör md5'leri korumalarla eşit, yani statik taşıma mümkün; blob'lar silindi | L:521 |
| IMPL-93 | 2026-09-13 | Faz8.2 | kernel LTS kapsamı, yalnız blobless klonlarla | verified; 1 / 16 çakışma, hiçbiri kamera sürücüsünde değil; `DEC-08`: ertele | L:522 |
| IMPL-94 | 2026-09-13 | Faz7.2 | `F7.2-01` kapısı; runbook'ta `AUDIT-FIX-52/53/54`; symlink testi `vendor/` yoluna taşındı | kapı GEÇMEDİ (10 saatlik pencere yok, diğer kontroller açık); §5 exit 0; kiralama yok | L:523; snap 20260913-2140 |
| IMPL-95 | 2026-09-14 | Faz7.2 runbook'u (PRP adım 3a) | önceki set `f724b64` olarak commit'lendi; `DEC-26` yanıtlandı; BE Scaleway'e taşındı | POP2-32C-128G, 3 volume, sıfıra söküm; `bash -n` 10/10; commit `587e3b5`; kiralama ve push yok | L:524; snap 20260914-1434 |
| IMPL-96 | 2026-11-13 | depo, kayıt işleri ve HyperOS 4 taban ölçümü | Depo taşıma; K4 silinenleri; `7fa0a51`; HyperOS 4 salt-okunur ölçümü (`70946ff`; probe satır 42, 190, 191 redakte); tarihsel notlar ve cihaz notları (`03b0898`); oturum belgeleri (`775b321`); K8 bundle. Ledger satırı ve `DEC-27`…`DEC-32` Pencere 1'de yazıldı (`ORCHESTRATION_PLAN.md` §5) | K7 = (a), K8 = A; IMPL-96 kaydı yazıldı, commit C1 (`IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline`); push `2 · O5`'te, depo silme `DEC-30` bekliyor | L:525; C1; snap 20261113-1819, -1821 |

### 3.3 Planlama koşuları ve denetimler
ClaudeQB adımları:
- **Step 1 (First-Planner):** `Main-Planing.md`.
- **Step 1.5:** `Autopsy.md`, `Project-Ontology.md`, `Project-Comprehension.md`.
- **Step 2 (Second-Planner):** alt planlar ve `Sub-Planing-Index.md`.
- **Step 3 (Third-Planner):** denetim. Yalnız `Sub-Planing-Audit.md`'yi yazar; her denetim bir öncekinin yerine geçer.
- **Step 4:** uygulama; ledger §5'e bir IMPL satırı yazılır.

`Main-Planing.md`'yi düzenlemek ledger §7'deki yeniden planlama tetikleyicisidir: önce snapshot kesilir, sonra Step 2, sonra Step 3 yapılır. Alt plan yaratmayan ya da silmeyen sınırlı bir değişiklik snapshot kesmez (run 13–15, 19 ve 20 emsali). Yeni ya da değişmiş bir alt plan, bir denetim onu okumadan Step 4 kuyruğuna girmez (L:562, L:618; AUD:14).

| Koşu | Adım | Tarih | Ne yapıldı → sonuç | Kaynak |
|---|---|---|---|---|
| 1 | Step 1 | 2026-08-23 | dokuz fazlı ana yol haritası (`Main-Planing.md`) | L:17 |
| 2 | Step 1.5 | 2026-08-23 | Autopsy (13 öncelikli bulgu), Ontology (tersine mühendislik adres defteri), Comprehension (kanıt modeli) | L:18 |
| 3 | Step 2 | 2026-08-24 | 9 faz 32 alt plana bölündü; index ve ledger yazıldı; Python yok sanıldığı için doğrulama elle yapıldı | L:19 |
| 4 | Step 2 | 2026-09-01 | yeni `Faz4.5` eklendi ve `Faz4.1`'den önceye kondu (`DEC-12`); `Faz4.1` format 32'yi de kapsayacak şekilde genişletildi (`DEC-11`); 32→33 | L:20 |
| 5 | Step 3 | 2026-09-01 | 33 alt planın tam yeniden denetimi (aşağıdaki 2. denetim) | L:21 |
| 6 | Step 2 | 2026-09-01 | `DEC-13`: FIND-4.5-02'nin sahibi olarak yeni `Faz4.6`; 33→34 | L:22 |
| 7 | Step 2 | 2026-09-03 | sahipsiz kalan UHR hattı için yeni `Faz4.7` (denetlenmedi); 34→35 | L:23 |
| 8 | Step 2 | 2026-09-03 | `DEC-14` yeniden planı: yeni `Faz3.7`–`3.11`; `Faz4.2`–`4.4` değiştirildi; `Faz4.1`/`4.7` superseded; `DEC-15` doğdu; 35→40 | L:25 |
| 9 | Step 3.1 | 2026-09-04 | denetçi kendi bulduğu P1'i (`AUDIT-FIX-17`, `Faz4.4`) onardı; `DEC-16` buradan doğdu | L:26 |
| 10 | Step 2, sınırlı | 2026-09-04 | `DEC-14` kalıntıları tam okumayla onarıldı; `AUDIT-FIX-18/19/21` kapandı; `DEC-16` açıldı | L:28 |
| 11 | Step 3 | 2026-09-04 | 5. denetim; satır sonradan, run 12 tarafından eklendi | L:29 |
| 12 | Step 2 + Step 1 | 2026-09-04 | `DEC-15`/`DEC-17` eylemleri: Main-Planing §6/§9 düzeltildi → `SNAP-2026-09-04-MAIN`; `F3.7-09/-10` eklendi | L:30 |
| 13 | Step 2, sınırlı | 2026-09-05 | "sabitleme", `pref_48m_key` girdisi olarak yeniden tanımlandı; `AUDIT-FIX-24/26…29` kapandı | L:32 |
| 14 | Step 2, sınırlı | 2026-09-05 | `AUDIT-FIX-34` ve `-31`'in `Faz3.11`'e düşen payı | L:34 |
| 15 | Step 2, sınırlı | 2026-09-05 | `AUDIT-FIX-31/32/36`: `Faz3.10` kapıları onarıldı | L:36 |
| 16 | Step 1 değişikliği | 2026-09-07 | kullanıcının benimsediği 5 Main-Planing düzeltmesi, her biri yeniden ölçülerek uygulandı (Faz 4: 8192x6144'te yalnız 33/34/35/54 formatları var; Faz 9 kabul sinyali yalnız izlenen dosyaları kapsıyor) | L:37 |
| 17 | Step 1 değişikliği | 2026-09-10 | `DEC-24` ve `beryl` düzeltmesi: Faz 7 artık GitHub'da hazırlanmış girdilerle kiralık sunucuda; Faz 8 Android 16 blob'ları + kernel LTS; `SNAP-2026-09-10-MAIN` | L:38 |
| 18 | Step 2 | 2026-09-10 | Faz 7/8 yeniden planı: `Faz7.1`–`7.3`, `Faz8.1`–`8.3`; 40→42; `SNAP-2026-09-10-SUBPLANS` | L:39 |
| 19 | Step 2, sınırlı | 2026-09-13 | `Faz7.2/7.3/8.1/8.3` runbook'la uzlaştırıldı; `AUDIT-FIX-43…49`, `-51` ve `-50`'nin alt plan yarısı kapandı; kullanıcı kuralları: düzeltmeler `fixes.diff`'e, symlink testi `vendor` yolunda | L:40 |
| 20 | Step 2, sınırlı | 2026-09-14 | `DEC-26`: `Faz7.2` Scaleway'e taşındı; snapshot kesilmedi; commit edilmedi *(2026-11-14 notu: 2026-11-13'te `7fa0a51`'de değiştirilmeden commit edildi.)* | L:41 |

**Step 3 denetimleri.** Ledger §2'de yalnız run 5, 9 ve 11'in kendi denetim satırı var; diğer denetimlerin satırı yok. Kaynakta açıkça geçmeyen sıra numaraları ve tarihler `[ÇIKARIM]` ile işaretlidir.

| Denetim | Tarih | Bağlam | Hüküm / sonuç | Kaynak |
|---|---|---|---|---|
| 1. | kayıtta yok [ÇIKARIM: 2026-08-24…08-30] | run 3'ün 32 alt planı; Python yok sanıldığı için doğrulayıcı elle yeniden uygulandı; `AUDIT-FIX-01…04` | hüküm kayıtta yok | L:178, L:187 |
| 2. [ÇIKARIM] | 2026-09-01 | run 5; 33 alt plan | PASS_WITH_WARNINGS, P0/P1 yok; `AUDIT-FIX-05…13`; 14 satırlık kuyruk, başında `Faz4.5` | L:21 |
| 3. | 2026-09-01 [ÇIKARIM] | run 6'dan sonra | hüküm kayıtta yok; açık bıraktığı `AUDIT-FIX-11/14/15/16` aynı gün giderildi | L:359 |
| 4. [ÇIKARIM] | 2026-09-03…04 [ÇIKARIM] | run 8'den (`DEC-14`) sonra | P1 bulgu `AUDIT-FIX-17` Step 4'ü durdurdu; run 9 onardı | L:26 |
| 5. | 2026-09-04 | run 11; 40 alt plan | PASS_WITH_WARNINGS; `AUDIT-FIX-18/19/21` kapandı, `AUDIT-FIX-22` açıldı; kuyruk READY, başında `Faz3.7` (17 satır) | L:29 |
| 6. | 2026-09-04 | run 12'den sonra | PASS_WITH_WARNINGS, P0/P1 yok; `AUDIT-FIX-26` ve diğerleri run 13'e devredildi | IDX:8; L:32 |
| 7. | 2026-09-05 | run 13'ten sonra | genel hüküm kayıtta yok; `Faz3.10` NEEDS_REPAIR (`AUDIT-FIX-31/32/34/36`) → run 14–15 | L:34, L:36 |
| 8. | 2026-09-05 [ÇIKARIM] | run 15'ten sonra; 16 satırlık kuyruk | hüküm kayıtta yok [ÇIKARIM: IMPL-69 sırasında okunan etkin denetim PASS_WITH_WARNINGS, P0/P1 yok, kuyruk READY] | L:37, L:496, L:515 |
| 9. | 2026-09-10…11 [ÇIKARIM] | run 17–18'den sonra Faz 7/8; `AUDIT-FIX-43…51` | hüküm kayıtta yok; 2026-09-13'te `097d687` ile commit'lendi | PRP:49, PRP:70; L:40 |
| 10. | 2026-09-13 | PRP adım 3; run 19'un değişikliği | PASS_WITH_WARNINGS, P0/P1 yok; `Faz7.2` READY_WITH_WARNINGS (o sırada Hetzner metniyle) | PRP:113; AUD:6 |
| 11. | 2026-09-14 | PRP adım 3c; run 20 (`DEC-26`) | PASS_WITH_WARNINGS, P0/P1 yok; kuyruk READY, başında `Faz7.2`/`F7.2-01`; `-52/53/54` kapandı, `-55/56/57` yeni açıldı; commit edilmedi *(2026-11-14 notu: 2026-11-13'te `7fa0a51`'de değiştirilmeden commit edildi; denetimin kuyruğu 2026-11-13'ten beri geçersiz (`DEC-28`).)* | AUD:6, AUD:18, AUD:363 |

### 3.4 ClaudeQB öncesi tarih
ClaudeQB'den önceki ölçüm günlüğü Türkçe `50MP-Entegrasyon-Plani.md` dosyasıdır ve Faz 1–12'yi kapsar. Faz 10 ("Android 16 / beryl hazırlığı", J:96-102) yalnız planlandı: bulgu bölümü yok, tamamlanmadı; WSL2 ve ~300 GB disk gerektiği için bloke kaldı. Android 16 kapsamı ClaudeQB'nin Faz 7/8'ine taşındı; 2026-11-13'te ROM derleme fikri tamamen bırakıldı (§2.5). 2026-09-06'da Faz9.3, AGC tavanıyla ilgili aşılmış bölümleri silmeden "AŞILMIŞ" diye işaretledi. O tarihten beri sürüm geçmişinin sahibi `CHANGELOG.md`'dir (J:11-18; CL:3-13).

| Tarih | Günlük fazı | Olay → sonuç | Kaynak |
|---|---|---|---|
| ≤2026-08-20 [ÇIKARIM: tarihsiz] | Faz 1–3 | A14 FullRes modülü bu cihazın HAL'ine uymuyor (farklı derleme, 73 sembolsüz yama noktası). Yalnız prop değişikliği standart üst sınırı 12 MP'de bırakıyor, yani ikili yama şart. Yama A15'e taşınabilir; video riski not edildi | J:106-312 |
| ≤2026-08-20 | Faz 4 | 49 noktalık yama AGC'yi çökertti ve reddedildi. 16 noktalık scaler yaması çalıştı: Open Camera 50.3 MP, video sağlam, AGC 15.2 MP'de kaldı. Mount yığılma hatası düzeltildi | J:314-536 |
| ≤2026-08-20 | Faz 5–7 | v2.0 betik katmanı (`50mp` modu, 1,144 B yama listesi, karşılıklı dışlama), dördüncü kutucuk ve v2.0 zip'i hazırlandı. İlk HAL yazımının 288 baytı bozması düzeltildi | J:538-782 |
| 2026-08-20 | Faz 8 | kullanıcı v2.0'ı flaşladı: Open Camera 8192x6144 çekiyor; AGC 15.2 MP. Boyut zorlama ve YUV denemeleri başarısız | J:784-878 |
| 2026-08-22 | Faz 8–9 | yeni AGC derlemesi 12.6 MP veriyor. 4 modlu regresyon temiz (her modda 13 kamera, dışlama tutuyor). v2.1 paketlendi (versionCode 12, 42 dosya) | J:900-1056 |
| (plan, tarihsiz) | Faz 10 | "Android 16 / beryl hazırlığı" planlandı (A16 kontrol listesi, araçların yeni HAL'e hazırlanması; çıktı: port kılavuzu). AOSPA `beryl` derlemesi WSL2 + ~300 GB disk gerektirdiği için bloke kaldı, hiç yapılmadı | J:96-102 |
| 2026-08-23 | Faz 11 | AGC smali yaması: kök neden Android'in yüksek çözünürlük kovası. Yarım başarı: 50MP YUV akışı kuruluyor ama çekim takılıyor. Anahtarı kapalıyken yama etkisiz | J:1059-1204 |
| 2026-08-23 | Faz 12 | HAL RAW format deneyi: AGC RAW10 50MP'yi seçti, ama Gcam'in tutarlılık kontrolünden geçmedi. Cihaz fullres HAL'e döndürüldü | J:1206-1324 |
| 2026-08-23…24 | ClaudeQB | planlama koşuları 1–3 ve ilk uygulama koşusu (git) | L:17-19, L:113 |

Günlük kararları (J:1328-1342):
1. 50MP ile DCG/LN birbirini dışlar. İkisinin birlikte çalıştırılması Faz 5'te kanıtlandı, ama 2026-08-31'de dışlama korundu.
2. v1.9 üzerinde temiz başlangıç yapıldı.
3. Simge olarak klasik kamera simgesi seçildi.
4. Sensör mode 0'ın 12-bit'e taşınması onaylandı; Faz 5'te kanıtlandı ama benimsenmedi.

| Sürüm | versionCode | Tarih | Değişiklik (CL) |
|---|---|---|---|
| v1.0, v1.1, v1.3 | — | — | CHANGELOG girdisi yok; v1.0 zip'i kökte duruyor |
| v1.2 | — | tarihsiz | `dcgB` önerilen mod oldu (stoka göre %25 az gürültü, iki kat detay) |
| v1.4 | — | tarihsiz | DCG/LN4/LN2 için 3 QS kutucuğu, WebUI, Action düğmesi |
| v1.5 | — | tarihsiz | kutucukların birbiriyle senkronu düzeltildi |
| v1.6 | — | tarihsiz | mod değişiminde kameranın kilitlenmesi giderildi (doğru yeniden başlatma sırası); kutucuk alt yazıları kaldırıldı |
| v1.7 | — | tarihsiz | mod değişimi ancak kamera gerçekten hazır olunca bitmiş sayılıyor |
| v1.8 | — | tarihsiz | arayüz dili sistemden bağımsız, varsayılan İngilizce; EN/TR düğmesi |
| v1.9 | — | 2026-08-20 ve öncesinde kullanımda | canlı geri sayım bildirimi |
| v2.0 | 11 | 2026-08-20'de flaşlandı | 50MP (FullRes) modu: 16 noktalık yama listesi, 27 MB HAL paketlenmiyor; DCG/LN ile karşılıklı dışlama; dördüncü kutucuk. AGC'nin neden 50 MP çekemediğine dair açıklama 2026-09-06'da düzeltildi |
| v2.1 | 12 | 2026-08-22'de paketlendi, 2026-08-31'de flaşlandı | çekmece simgesi düzeltildi; başlatıcı görünürlüğü her çağrıda yeniden uygulanıyor; durum bilgisi çerçeveden okunuyor |
| v2.2 | 13 | 2026-09-06 (karar ve kurulum) | AGC metni dört yüzeyde 12.58 MP olarak düzeltildi; `tiles` çıktısı (`takma_ad`); açıklama 1741 karakterden 1119'a indi; sürüm geçmişi CHANGELOG'a taşındı |

### 3.5 Commit geçmişi
Liste `integrate/impl-96` dalının commit'leridir, eskiden yeniye; `2 · O3` açılışında (2026-11-14) ölçülen uca, `2 · O2` commit'ine kadar 71 commit: ilk 62'si `origin/main`'de (`587e3b5`'e kadar), `7fa0a51` yerel `main`'in ucu (63.), sonraki sekizi yalnız dalda. Konu satırları `git log --reverse` çıktısından aynen alındı (Ö13; `587e3b5`'ten sonrakiler 2026-11-14 ölçümünden); italik parantezler sonradan eklenmiş nottur. Bu dokuz commit ve listede olmayan sonraki aşama commit'leri 2026-11-15 ve 2026-11-16'da push edildi (son: C3; §2.1).

**2026-08-24 (4)**
- `ff6934e` Initial commit: put the ishtar workspace under version control
- `97c44e0` Faz 1.1: record IMPL-01 in the ledger and update the continuity registers
- `2e64058` Faz 1.2: signing key containment audit - all five archives clean
- `5d8d0bc` Faz 6.1: add the aon_front.pb SYMLINK entry to both device trees

**2026-08-30 (3)**
- `edc28e8` Faz 2.1: read-only device smoke script, validated on the device
- `e7ed4c1` Faz 1.5: static safety probes - four questions closed, three findings routed
- `679f01d` Faz 1.3: patch table format contract, transcribed from the parser

**2026-08-31 (8)**
- `6cd51b4` Faz 1.4: toolchain procedure record, and a corrected host fact
- `48833bb` Faz 1.6: root README, refs index, artifact manifest - Phase 1 closed
- `1320ac0` Faz 2.2: pre-flash brackets, recovery proof, and the RAW-depth control result
- `98dae91` Faz 2.2: v2.1 flashed, baseline BASELINE-2026-08-31-V21 captured
- `ee7019a` Faz 2.2: preserve the v2.1 installer transcript as a snapshot artifact
- `cef8b95` Faz 2.2 complete: launcher fix verified, OQ-17 answered
- `5bf2fb8` Faz 2.3 complete: ten-mode regression pass, six findings routed
- `c3ef695` Plan change: raise Phase 5, answer DEC-03, correct the AGC-video link

**2026-09-01 (12)**
- `e19b8cf` Phase 5 close: mode-0 12-bit candidate recorded, exclusion retained
- `44eab08` Faz 3.2 complete: pixelArraySize write site located, address book corrected
- `bbc8019` Faz 9.2 recovery runbook pulled forward ahead of Faz 3.3
- `8775052` Faz 3.3 complete: pixelArraySize write site confirmed by measurement
- `c91c7c0` Faz 3.4 F3.4-01: pre-change consumer expectations recorded
- `aab466a` Faz 3.4 complete: consumer survey passes, OQ-03 answered with scope
- `606e329` Faz 3.5 complete: libgcam gate cleared, AGC reaches 50.3 MP, output corrupt
- `cf3cf88` Faz 3.6 complete: Phase 3 closed as primary success, Phase 4 scope expanded
- `947a01b` Faz 4.1 blocked at pre-execution review: two defects confirmed, DEC-11/DEC-12 taken
- `4897a9b` Faz 4.5 execution evidence and planning run 6 documents (AUDIT-FIX-15)
- `6520427` Faz 4.6 host-side half: FIND-4.5-02 closed, the frame is a folded payload
- `a1829f9` AUDIT-FIX-11 discharged: planner vocabulary conformant, validator 11 -> 0

**2026-09-02 (12)**
- `de95ae3` Faz 4.6 live half: F4.6-05 answered, the fault is confined to AGC's Gcam path
- `d6714d1` Faz 4.1 host-side half: the resolution is reachable, the guard is designed
- `1f6df4d` Faz 4.6 EV-44 attempt: pref_48m_key is necessary but not sufficient
- `db8a91c` Faz 4.6 IMPL-36: SABRE excluded, the green verdict is a CPU read of the payload
- `0842ef2` Faz 4.6 IMPL-37: the producer is MeasureSharpnessRaw, the verdict is all_black
- `43ae3d9` Faz 4.6 IMPL-38: correction, the rejected frames were half-resolution frames
- `6d64e42` Faz 4.6 IMPL-39: AGC is not clamped; no capture was ever taken on the full stream
- `a2dd417` Faz 4.6 IMPL-40: positive control, the fault is a request/delivery mismatch
- `a28991a` Faz 4.6 IMPL-41: tempBinning is temporal; the sensor is not pinned to binning
- `b0ccc98` Faz 4.6 IMPL-41 follow-up: cite the vendor-tag scan instead of asserting it
- `33710ee` Faz 4.6 IMPL-42: the SensorMode dump line cannot be enabled on this build
- `04a0d1e` Faz 4.6 IMPL-43: EV-44 performed - stream reaches 50MP, sensor readout does not

**2026-09-03 (7)**
- `b5ccaae` Faz 4.6 IMPL-44: ULTRA_HIGH_RESOLUTION_SENSOR and the four MR tags enabled
- `25f4b63` Faz 4.6 IMPL-45: pixelMode=MAXIMUM_RESOLUTION honoured; the fold is a stride error
- `3e71682` Faz 4.6 IMPL-46: F4.6-04 performed - the un-fold holds, no data was ever missing
- `af43897` Faz 4.7 authored: the ultra-high-resolution line finally has an owner
- `2fa5118` Faz 4.7 IMPL-47: F4.7-02 located; the max-res tables share Faz4.1's function
- `998979f` Faz 4.1 IMPL-48: narrowing lands on target, and the d0014 collision is measured
- `83d4866` Faz 4.1 IMPL-49: F4.1-07 fails - the narrowing breaks AGC

**2026-09-04 (2)**
- `65610de` Planning runs 8-10: the DEC-14 re-plan, its repair, and its audit
- `aadecc6` Ledger: correct the post-commit tracked-file count to the measured 225

**2026-09-06 (6)**
- `d86f4a2` Module v2.2: reproducible release build, stale-claim fix, tiles wording
- `eae05f3` smoke.sh: repair the trap probe and the stream-config race (DEC-20)
- `422e659` Phase 4 patch tables: consolidation, provenance headers, validation record
- `c683d32` Docs: the 12.58 MP configuration record, AON verification, Phase 3 preconditions
- `78373d5` Planner-docs: Phase 3 closure, Phase 4/6/9 state, and planning runs 11-13
- `cfa312d` Evidence: device snapshots and captures for IMPL-52 through IMPL-81

**2026-09-07 (1)**
- `3a307d2` IMPL-82/83: VAL-MANUAL machine half, and an instrument for FIND-3.9-02

**2026-09-08 (1)**
- `60f0aee` Carried Step 4 batch: run-16 Main-Planing corrections, IMPL-84/85/86 ledger rows, VAL-MANUAL evidence

**2026-09-10 (2)**
- `130185d` IMPL-87/88: Kamera-Teyit re-check and the PC-13 60 fps re-measurement
- `f8a05ca` IMPL-89: record user rulings DEC-16/21/23/24, add DEC-01, arm the Phase 7/8 re-plan *(origin/main)* *(2026-11-14 notu: eski remote'un (`ahmetxa/ishtar`) `main` ucuydu; o remote 2026-11-13'te yerelden kaldırıldı.)*

**2026-09-13 (2)**
- `097d687` Planning runs 17-18, ninth audit, IMPL-91/92/93: Android 16 front up to the rental gate
- `d3993de` Pre-rental plan: checkpoint, bounded amendment, tenth audit, rental-day gate

**2026-09-14 (2)**
- `f724b64` Planning run 19, tenth audit, IMPL-94 rental gate, DEC-26 Scaleway handover
- `587e3b5` IMPL-95: DEC-26 answered, runbook re-targeted to Scaleway POP2-32C-128G *(origin/main)*

**2026-11-13 (6)**
- `7fa0a51` Planning run 20 and eleventh audit: Faz7.2 re-targeted to Scaleway (DEC-26) *(main)*
- `70946ff` IMPL-96 evidence: read-only HyperOS 4 baseline on dc27e5d0
- `03b0898` Mark the AOSPA ROM-build records historical (2026-11-13)
- `775b321` Session 2026-11-13: project log and handoff prompt
- `b603516` Window 0: orchestration plan, K8 redaction, handoff for window 1
- `c2abd46` Window 0 follow-up: align handoff with plan, rename review IDs

**2026-11-14 (3)**
- C1: IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline
- 2 · O0+O1: Window 2 O0-O1: approved plan, discovery facts, stage-per-session loop
- 2 · O2: Window 2 O2: contract for the project log sweep and the run 21 handoff

## 4. Kararlar (DEC-01 … DEC-33)

Kanonik kaynak `Planner-docs/Planing-Ledger.md` §8'dir (başlık :572, satırlar :576–:610; satır sırası numara sırasında değil: DEC-10, DEC-05'ten sonra; DEC-01, DEC-24'ten sonra geliyor). Bu tablo bir özettir. `Kaynak` sütunundaki `ledger:N`, `Planner-docs/Planing-Ledger.md:N` demektir.

**Açık kararlar (2026-11-14):** `DEC-09` (koşullu; yalnızca tetiklenirse gündeme gelir) ve K9 (kullanıcının; 50MP HAL yeniden türetmesi; henüz DEC numarası yok). `DEC-07` ve `DEC-08` 2026-11-13'ten beri konusuz (`DEC-28`); `DEC-08`'i etkileyebilecek doğrulanmamış kernel-upstream iddiası da 2026-11-13'te düştü (K3; bkz. §9). Kalan 31 kararın hepsi yanıtlandı, kapandı ya da konusuz kaldı (ledger:576–:610). *(2026-11-16 notu: K9 yanıtlandı 2026-11-15, `3 · O0`: hayır, şimdilik (`DEC-33`); HAL katmanı HyperOS 4'te kapalı, sensör katmanı sürer.)*

| id | tarih (açıldı → yanıt) | soru | hüküm | durum | kaynak |
|---|---|---|---|---|---|
| DEC-07 | – → **AÇIK** (IMPL-92 ile 2026-09-11'de güncellendi) → konusuz 2026-11-13 | Android 16 bloblarında kamera yeniden türetmesine bağlanılsın mı? | Statik temel: iki katmanda da carry-over (IMPL-92, vendor pin `f92e7a9`) | konusuz (`DEC-28`, 2026-11-13) | ledger:582 |
| DEC-08 | 2026-09-13 öneri → **AÇIK** → konusuz 2026-11-13 | Kernel LTS merge'üne bağlanılsın mı? | IMPL-93 önerisi: ertele. Merge gerekli değil; 1 / 16 çakışma, hiçbiri kamera sürücüsünde değil | konusuz (`DEC-28`, 2026-11-13) | ledger:583 |
| **DEC-09** | – → **AÇIK (koşullu)** | Size-list bucket eşiğini geçen bir duration değeri isteniyor mu? | – (Faz4.2 hiçbir değer uygulamadı, tetik hiç ateşlenmedi [ÇIKARIM]) | **AÇIK**, yalnızca tetiklenirse | ledger:584 |
| DEC-01 | 2026-08-24 → 2026-09-10 | Çalışma alanı deposuna remote eklensin mi? | Private `ahmetxa/ishtar`; `main` `f8a05ca`'da push edildi (IMPL-90) *(2026-11-14 notu: 2026-11-13'te depo özel `ahmetxa/ishtar_cam_modes`'a taşındı (`DEC-27`); eski depo silinecek (`DEC-30`))* | yanıtlandı | ledger:602 |
| DEC-02 | → 2026-09-06 | `tiles hide` onarılsın mı, kaldırılsın mı, etiketlensin mi? | Dördüncü seçenek seçildi: seçenek kalıyor, FIND-2.4-01 metinleri düzeltildi (IMPL-75). AOSPA Launcher3 `pm disable`'ı yok saydığı için onarım mümkün değil | yanıtlandı | ledger:576 |
| DEC-03 | → 2026-08-31 | Faz 5 önceliğini koruyor mu? | Evet; Faz5.1/5.2 Faz 3/4'ün önüne alındı (Index §4a) | yanıtlandı | ledger:577 |
| DEC-04 | → 2026-09-06 | AON modülü cam-modes ile birleştirilsin mi? | Ayrı kalıyor (IMPL-75). Girdilerinden biri FIND-6.2-03 ile zayıfladı | yanıtlandı | ledger:578 |
| DEC-05 | 2026-08-24 → 2026-08-24 | Yayımlanmış arşivlerde keystore var mı? | 5 arşivin hiçbirinde yok (IMPL-02) | temiz kapandı | ledger:579 |
| DEC-06 | → 2026-08-31 | Faz 3 yazım-yeri arama bütçesi? | 15 aday site / en çok 2 oturum (IMPL-16) | kapandı | ledger:581 |
| DEC-10 | 2026-08-24 → 2026-09-06 | `tile-app/build.sh` içindeki düz metin imzalama varsayılanı | Debug anahtarı olarak kabul; `KS`/`KS_PASS`/`KS_ALIAS` ortam değişkenleriyle geçersiz kılınabiliyor (IMPL-80); keystore hiçbir arşive girmiyor (A1). Değer bu belgeye yazılmaz | yanıtlandı | ledger:580 |
| DEC-11 | 2026-09-01 → 2026-09-01 | Faz4.1'in format-32 (RAW_SENSOR) kriteri | Faz4.1 içinde eklenecek, daraltmadan ayrı raporlanacaktı | yanıtlandı; boşa düştü (Faz4.1 superseded) | ledger:585 |
| DEC-12 | 2026-09-01 → 2026-09-01 | Active-array yükseltmesi nerede yapılsın? | Faz4.1'den önce yeni alt plan → Faz4.5 (IMPL-27…30) | uygulandı | ledger:586 |
| DEC-13 | 2026-09-01 → 2026-09-01 | QTI vendor tag'i word patch dışı yollarla da kovalansın mı? | (a) Bırakılsın; stride hipotezi izlensin → Faz4.6. EV-45 ölçümle doğruladı | yanıtlandı | ledger:587 |
| DEC-14 | 2026-09-03 → 2026-09-03 | AGC 50 MP hedefi korunsun mu? | **RETIRE.** Yeni hedef "AGC stable at 12.6 MP under 50 MP". 2026-09-05'te FIND-3.10-03'ten sonra yeniden teyit edildi. Yeniden açmak için iki duvardan birine dair yeni kanıt gerekir | yanıtlandı (run 8) | ledger:589 |
| DEC-15 | 2026-09-03 → 2026-09-04 | Faz 3 referans HAL tabanı | Gönderilen `fullres`, `fe0245a4720fb07b01d96deef47f5569` | yanıtlandı (run 12–13) | ledger:591 |
| DEC-16 | 2026-09-04 → 2026-09-10 | Step 3 kendi P1'ini onarabilir mi? | Evet, dar okumayla (IMPL-89) | yanıtlandı | ledger:593 |
| DEC-17 | 2026-09-04 → 2026-09-04 | Faz3.7 `pref_48m_key`'e yazabilir mi? | Evet, ama önce Step 2 üzerinden | yanıtlandı (run 12) | ledger:594 |
| DEC-18 | 2026-09-04 → 2026-09-04 | `pref_48m_key` 1'e geri dönsün mü, 0 benimsensin mi? | **0 benimsendi**; prefs md5 `e3ed08f72025c4dbfbdea6be057873d7`, yedek kayıtlı | yanıtlandı | ledger:595 |
| DEC-19 | 2026-09-05 → 2026-09-06 | FIND-3.5-01 / FIND-4.5-02 ne olacak? | Bilgi olarak tutulsun; ne kapatılsın ne yeniden açılsın | yanıtlandı | ledger:596 |
| DEC-20 | 2026-09-05 → 2026-09-06 | `scripts/smoke.sh`'i kim onarır? | Onarıldı (IMPL-80): `prefs.trap.armed`, `prefs.trap.values`, tek dump'lı `probe_main_rows()` | yanıtlandı | ledger:597 |
| DEC-21 | 2026-09-05 → 2026-09-10 | Faz3.9/3.10'daki altı sapma | Faz 3 başarılı sayıldı; (1)–(5) önemsiz; (6) IMPL-85 ile kapandı | yanıtlandı | ledger:598 |
| DEC-22 | 2026-09-07 → 2026-09-11 | Derleme dağıtımı | Ubuntu 22.04 LTS; yedek 24.04 + `kernel.apparmor_restrict_unprivileged_userns=0`. Başlıkta hâlâ WSL2 yazıyor | yanıtlandı; DEC-26(a) ile korundu; 2026-11-13'ten beri konusuz (`DEC-28`) | ledger:599 |
| DEC-23 | 2026-09-09 → 2026-09-10 | IMPL-88'deki kare hızı kuralı sapması kabul edilsin mi? | Kabul edildi; FIND-9.2-07 çözüldü | yanıtlandı; C-13'ün kapsamı (tek mod, tek uygulama) açık | ledger:600 |
| DEC-24 | 2026-09-10 → 2026-09-10 | Faz 7 nerede derlenecek? | WSL2 yok; girdileri önceden GitHub'a hazırlanmış kiralık VDS | yanıtlandı (sağlayıcı DEC-26 ile değişti); 2026-11-13'ten beri konusuz (`DEC-28`) | ledger:601 |
| DEC-25 | 2026-09-11 → 2026-09-11 | Bütçe, durma kuralı, sunucu, repo erişimi | CCX53; 10 sa tavan + 8. saat kuralı; ≤2 manifest-sınıfı düzeltme; kapatma değil silme; manifest ve device repoları public; sunucuda kimlik bilgisi yok | yanıtlandı; (1) ve (4) DEC-26 ile değişti; (3)'te sync-path istisnası eksik (AUDIT-FIX-56); 2026-11-13'ten beri konusuz (`DEC-28`) | ledger:603 |
| DEC-26 | 2026-09-14 → 2026-09-14 | Hetzner engelinden sonra Scaleway kiralaması | POP2-32C-128G (Instance EUR 1.18/sa, tümü yaklaşık EUR 1.28/sa); Ubuntu 22.04 (+yedek); 10 sa / 8. saat kuralı kalıyor, yaklaşık EUR 12.8 + KDV; OOM'da yeniden deneme yok; her şey silinir; disk 40 GB 5K, `ishtar-src` 310 GB 5K `/android`, `ishtar-out` 260 GB 15K `/android/beryl/out`; ccache kapalı; `OUT_DIR` yok | yanıtlandı (IMPL-95); 2026-11-13'ten beri konusuz (`DEC-28`) | ledger:604; `docs/build-environment.md:126-138` |
| DEC-27 | 2026-11-13 → 2026-11-13 | Projenin geçmişi GitHub'da nerede duracak? | `origin` = özel `ahmetxa/ishtar_cam_modes`; 62 commit aynı hash'lerle push edildi. `DEC-01`'in deposunun (`ahmetxa/ishtar`) yerine geçer, özel remote kararının değil | yanıtlandı | ledger:605 |
| DEC-28 | 2026-11-13 → 2026-11-13 | Telefonda artık HyperOS 4 çalıştığına göre ROM derlemesi (Faz 7 ve 8) sürsün mü? | ROM derleme bırakıldı. Telefonda HyperOS 4 (`OS4.0.0.44.WMACNXM`) çalışıyor, 2026-11-13'te gözlendi (ROM'un derleme tarihi 2026-09-23; `/data/adb/modules` 2026-10-26 tarihli, yani gözlemden önce kurulmuş). Faz 7 ve 8 amacını yitirir; resmî emeklilik planlama koşusu 21'de. `DEC-07`, `DEC-08`, `DEC-22`, `DEC-24`, `DEC-25` ve `DEC-26` konusuz kalır | yanıtlandı | ledger:606 |
| DEC-29 | 2026-11-13 → 2026-11-13 | `Kullanim.txt` v2.2'de mi, sonraki sürümde mi düzeltilsin? | v2.2'de gönderildiği gibi kalır; sonraki sürümde düzeltilir (K1 = b) | yanıtlandı | ledger:607 |
| DEC-30 | 2026-11-13 → 2026-11-13 | ROM derleme için açılan üç GitHub deposu silinsin mi? | Üçü de silinir (K5 + K6): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. Halka açık ikisinin aynaları `../ishtar-arsiv/` altında; yürütme `gh api` ile ölçülür (404 = silindi) | yanıtlandı; silmeyi kullanıcı yapar; 2026-11-14T13:45:22Z `gh api` ölçümünde üç depo da hâlâ duruyor | ledger:608 |
| DEC-31 | 2026-11-13 → 2026-11-13 | Commit edilmiş ama push edilmemiş probe anlık görüntüsündeki cihaz tanımlayıcıları redakte edilsin ve geçmiş yeniden kurulsun mu? | K8 = A: tanımlayıcılar (iki IMEI anahtarı ve `persist.sys.miui.sno` değerleri) yerinde redakte edildi; push edilmemiş üç commit, herhangi bir push'tan önce yeniden kuruldu. Geçmişi yeniden yazmama kuralının kayıtlı tek istisnası (ledger satırları commit hash'lerini anar); eski hash'leri anan ledger satırı yoktu. Redaksiyonsuz özgün kopya depo dışında, doğrulanmış bir bundle'da | yanıtlandı ve yürütüldü | ledger:609 |
| DEC-32 | 2026-11-13 → 2026-11-13 | Modül HyperOS 4'te hangi yolu izleyecek? | K7 = (a): modül HyperOS 4'e uyarlanır. Kapsamı (50MP HAL yeniden türetmesi = K9, kutucuk/WebUI zinciri, AGC tuzakları, v2.3) planlama koşusu 21 belirler | yanıtlandı | ledger:610 |

**Oturum kararları (2026-11-13).** Bu numaralar atandı; ledger'a IMPL-96 ile (Pencere 1) yazıldı (`:605`–`:610`). Atanan numaralar: `DEC-27` depo taşıma, `DEC-28` ROM derlemenin bırakılması ve HyperOS 4, `DEC-29` K1, `DEC-30` K5+K6, `DEC-31` K8, `DEC-32` K7. Sonraki boş numara `DEC-33`. *(2026-11-16 notu: `DEC-33` (K9) planlama koşusu 21 ile ledger `:619`'a yazıldı (`3 · O4`); sonraki boş numara `DEC-34`. Bu tabloda `DEC-33` satırı bilerek yok (satır eklemek çapaları kaydırırdı); karar aşağıdaki K9 satırında (`:651`).)*

| id | soru | yanıt / durum (öneri kalın) |
|---|---|---|
| K1 | `ishtar-cam-modes/Kullanim.txt` (v1.9 kılavuzu, zip içinde) | **Yanıtlandı (b):** bir sonraki sürümde düzeltilecek (`DEC-29` atandı; ledger'a Pencere 1'de yazıldı, `:607`) |
| K2 | Planlama koşusu 21'in zamanı (Main-Planing Hetzner→Scaleway, EV-20, AUDIT-FIX-41/42/57) | **Yanıtlandı, kapsam değişti:** ROM derleme fikri bırakıldı; telefon HyperOS 4 portunda (kernel 5.15.215). Koşu 21 artık Faz 7/8'i emekliye ayırır (`DEC-28` atandı; ledger'a Pencere 1'de yazıldı, `:606`) |
| K3 | T5: kernel-upstream iddiasının salt-okur doğrulaması | **Düştü:** kullanıcıya göre gereksiz; telefon zaten 5.15.215 kernelli portta |
| K4 | `devir-teslim-promptu.md`, boş `UsersahmetAppDataLocalTempaon-smoke/` ve gereksiz eski loglar | **Uygulandı (2026-11-13):** beş öğe silindi (§2.1) |
| K5 | Eski özel depo `ahmetxa/ishtar` | **Yanıtlandı: sil.** Kullanıcı: depo ROM derleme fikri için açılmıştı. Tek dalı `main@f8a05ca` yerel `main`'in atası; içeriğin tamamı yeni depoda; release, tag ya da issue yok. `gh` belirtecinde `delete_repo` yok; silmeyi kullanıcı yapar (`DEC-30` atandı; ledger'a Pencere 1'de yazıldı, `:608`) |
| K6 | Halka açık ROM depoları `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar` | **Yanıtlandı: sil** (derleme alınmayacak). Önce ayna yedek alındı: `C:/Users/ahmet/Documents/Projeler/ishtar-arsiv/` (§2.1). Silmeyi kullanıcı yapar (`DEC-30` atandı; ledger'a Pencere 1'de yazıldı, `:608`) |
| K7 | HyperOS 4'te projenin yönü | **Yanıtlandı: (a)** modülü HyperOS 4'e uyarla (`DEC-32`, ledger'a Pencere 1'de yazıldı, `:610`). Seçenekler: (a) modülleri HyperOS 4'e uyarla: sensör katmanı aynı blob üzerinde; 50MP katmanı yeni HAL'de baştan tersine mühendislik ister; kutucuk/WebUI zinciri KernelSU Next'e bağlı. (b) Yalnız AGC'yi sürdür: şu an yamasız V9.6, tuzaklar kurulu (10), 12,58 MP türetiliyor. (c) AOSPA dönemini kapat. Kaynak: `ORCHESTRATION_PLAN.md` §2 |
| K8 | Probe snapshot'ındaki cihaz kimlikleri (push öncesi) | **Yanıtlandı: A** (redaksiyon, `DEC-31`); dal yeniden kuruldu (`70946ff`, `03b0898`, `775b321`; eşleme §11); **yürütüldü**. Redaksiyonsuz uç yalnız depo dışı bundle'da (§11) |
| Konusuz | ROM derlemeye bağlı altı karar | `DEC-07`, `DEC-08`, `DEC-22`, `DEC-24`, `DEC-25`, `DEC-26`: `DEC-28` ile konusu kalmadı; ledger'a Pencere 1'de işlendi (IMPL-96; konusuz notları `:582`, `:583`, `:599`, `:601`, `:603`, `:604`) |
| K9 | 50MP HAL katmanının HyperOS 4 HAL'inde (`2a955e68…`) yeniden türetilmesi | **Yanıtlandı (2026-11-15, `3 · O0`): hayır, şimdilik.** HAL katmanı HyperOS 4'te kapalı kalır, sensör katmanı sürer; ileride yeniden açılabilir. Karar `DEC-33`; ledger'a koşu 21 yazar *(2026-11-16 notu: yazıldı, ledger `:619` (`3 · O4`).)* |
| O2 | Depo hijyeni ve IMPL-96 kurulumu | **Onaylandı (2026-11-13):** `7fa0a51`, `integrate/impl-96`, `70946ff`, `03b0898`, `775b321`; ledger satırı Pencere 1'de yazıldı (`:525`) |
| Push | `7fa0a51` ve `integrate/impl-96` dalı | **Yapıldı (2026-11-15, 2026-11-16):** C2'den sonra ayrı onaylarla FF ve push (08:14:45Z, 08:15:01Z); takip commit'i de aynı gün (reflog: 08:58:01Z, 08:58:04Z); Pencere 3'ün 11 commit'i `3 · O5`'te (22:05:00Z, 22:05:35Z). `origin`'de `main` ve `integrate/impl-96` = C3 (§2.1); yalnız açık refspec |

## 5. Bulgular, kanıtlanmış sınırlar, emekliye ayrılan hedefler

### 5.1 Kayıtlı olumlu sonuçlar

| sonuç | durum | kaynak |
|---|---|---|
| Kanonik iddia F3.11-09: rear kamera, AGC 12.58 MP, temiz (black < 0.01), 4 eksende sağ kaldı | kapsamı dar (tek cihaz, rear, 12.58 MP); metni §2.3'te | ledger:647–:651; `docs/agc-12mp-configuration.md:530-541` |
| VAL-AGC: aynı HAL durumunda AGC 12.58 MP ve Open Camera 50.33 MP birlikte temiz | PASS; dağıtılabilirlik ölçütü | `docs/patch-validation-phase4.md:234-243` |
| Stok kamera: rear 12.58 MP, 1080p60, 4K60; ön kamera 31.96 MP, 1080p60 (4K sunulmuyor) | invariant 5 stok kamerada sağlanıyor | `docs/patch-validation-phase4.md:265-295` |
| PC-13: stok Camera ile 4K 59.88 fps, 1080p 60.06 fps; Open Camera mod fark etmeksizin ~30 fps | pass (IMPL-88); kapsamı DEC-23'e bağlı | `docs/release-checklist.md:551` |
| Mod-0 12-bit + `fullres` birleşimi DCG için temiz 50.3 MP verdi | kanıtlandı ama benimsenmedi (RETAIN, IMPL-17) | ledger:94–:96 |
| pixelArraySize yazım yeri bulundu ve tek word ile kanıtlandı; geri alma byte-özdeş | değer çalışma zamanında türetiliyor (H-01 çürütüldü) | ledger:77–:78 |
| Modül `/odm`'a hiç yazmıyor; disable + reboot tam geri dönüş sağlıyor | CQ-09 yanıtlandı | `Planner-docs/Project-Comprehension.md:21` |
| Restart sırası (önce istemci, sonra HAL) ~17 geçiş ve 2 reboot boyunca korundu | invariant 3 testte geçerli | `Planner-docs/Project-Ontology.md:402` |
| Statik A16 carry-over: `f92e7a9`'daki HAL ve sensör md5'leri guard değerleriyle eşleşiyor | yalnızca statik; üçlü uyum yapılmayacak (`DEC-28`, 2026-11-13; ledger:102 notu) | ledger:102 |
| Kernel kapsamı: 5.15.185/189; hedef `android13-5.15-2026-06_r4`; 1/16 çakışma, hiçbiri kamera sürücüsünde değil | DEC-08 için öneri: ertele *(2026-11-14 notu: `DEC-08` 2026-11-13'ten beri konusuz (`DEC-28`).)* | ledger:103 |
| Release yeniden üretilebilir: VAL-BUILD2 byte-özdeş, A1/A2/A3 PASS | 2026-11-13'te yeniden ölçüldü | fact sheet D3 |

### 5.2 Kanıtlanmış sınırlar ve negatif sonuçlar

- **AGC 50 MP'yi kapatan duvarlar (DEC-14):** maksimum çözünürlük akış tablosu statik değil, çalışma zamanında hesaplanıyor (IMPL-47/51). Binary'de eklemeli kod için ≥16 B boşluk yok (IMPL-50). RAW satırlarını daraltmak AGC'nin açılmasını engelliyor: iki ayrı bisection aşamasında 3/3 (IMPL-49/50). Yeniden açmak için bu duvarlardan birine dair yeni kanıt gerekir (ledger:589).
- **FIND-3.5-01 / FIND-4.5-02:** AGC'nin tam çözünürlük kareleri geometrik olarak bozuk. İki bağımsız hata var: binned readout ve eksik stride uyarlaması (IMPL-46). DEC-19 gereği bilgi olarak tutuluyor (ledger:641).
- **Çürütülen öncüller:** vendor tag nedeni (EV-45, DEC-13); "Invalid mesh" ve SABRE neden değil; `tempBinning` ipucu tutmadı; CamX log maskeleri etkisiz (IMPL-41/42). Bu yollara yeniden oturum harcanmaz (`docs/raw-geometry-diagnosis.md`, extract XDocsTechA2).
- **Faz 4:** Faz4.2'nin öncülü yanlıştı; duration satırları zaten tam. 6 RAW stall satırı yamanamıyor; kamera 11/12'de duration tablosu yok (FIND-4.2-01/-02). Faz4.3 hiçbir şeyi birleştirmedi; kanonik tablo değişmedi (ledger:88–:89).
- **Cihaz ve ROM:** `ln2`/`ln4` AGC'yi açılışta çökertiyor (FIND-2.3-02). AGC videosu stokta bile siyah (FIND-2.3-03). `dcgB`, AGC dışı uygulamalarda provider'ı düşürüyor (FIND-3.4-02). `tiles hide` modül içinden onarılamıyor (OQ-11/H-05). AON mount doğru çalışıyor ama NCS provider'ları stok modda da yok, yani sorun ROM'un bir özelliği (FIND-6.2-03; pozitif baseline yok). Yerinde güncelleme `mode` dosyasını kaybediyor (FIND-9.1-04, CONFIRMED, açık).
- **Araç çıkmazları (bir daha denenmeyecek):** radare2/rabin2 300 saniyede çıktı vermiyor; apktool smali stub'ları; smali indirmesi 404/403 (`docs/reverse-engineering-toolchain.md:87-105`).
- **Kiralama:** Hetzner'in yeni hesap limiti CCX53'ü engelledi (IMPL-94), bu da DEC-26'ya yol açtı.
- **Ölçülmüş istisna:** FIND-3.10-03'te pinlenmemiş AGC tek oturumda iki kez temiz 50.33 MP çekti. Açıklanamadı. Bir yetenek iddiası değildir ve DEC-14 geçerliliğini koruyor (ledger:638).

### 5.3 Emekliye ayrılan hedefler, superseded ve kaldırılan alt planlar

| öğe | tarih | ölçülmüş neden | kaynak |
|---|---|---|---|
| "50 MP end-to-end in AGC" hedefi | 2026-09-03 | §5.2'deki duvarlar; yerine "AGC stable at 12.6 MP under 50 MP" geldi | ledger:589 |
| `Faz4.1` (superseded) | 2026-09-03 | Sayım hedefleri tuttu ama F4.1-07 FAIL: AGC 3/3 çöktü (guard'sız varyant da). F4.1-05b UNMET (kod boşluğu yok). Diriltilmez | ledger:87; `Planner-docs/Sub-Planing-Audit.md:310` |
| `Faz4.7` (superseded) | 2026-09-03 | Max-res tablo, Faz4.1'in hedefiyle aynı döngüde kuruluyor. Düzeltme, boş yeri olmayan binary'de kod değiştirmeyi gerektirir. Soru yalnızca emekliye ayrılan hedef için önemliydi | ledger:93 |
| `Faz4.6` (implemented / audit'te DEFERRED) | 2026-09-03 | F4.6-07 Faz4.1'e bağlı, erişilemez. Tamamlamak için yeni karar ve alt plan gerekir | ledger:92; `Planner-docs/Sub-Planing-Audit.md:309` |
| Kaldırıldı: `Faz7.1-wsl2-provisioning.md` | 2026-09-10 (run 18) | DEC-24 WSL2'yi emekliye ayırdı | `Planner-docs/Sub-Planing-Index.md:293,357` |
| Kaldırıldı: `Faz8.1-beryl-port-sizing.md` | 2026-09-10 (run 18) | `beryl` ikinci bir cihaz değil, AOSPA'nın Android 16 dalı | aynı |
| Katman dışlamasının kaldırılması (Kararlar #4) | 2026-08-31 | DCG için kanıtlandı; fayda yok, yalnızca DCG denendi, kaldırmak durum modelini değiştirir → RETAIN | ledger:96 |
| Günlükteki Faz 12 "kalan iş" | 2026-09-03 | DEC-14 | `50MP-Entegrasyon-Plani.md:1305-1316` |
| WSL2 ve Hetzner | 2026-09-10 / 2026-09-14 | DEC-24, DEC-26 | ledger:601, :604 |

### 5.4 Açık bulgular ve bilinen sınırlar

- **Açık FIND'ler:** FIND-3.10-02 (trap anahtarlarını yeniden kuran bilinmeyen yol; değer denetimi yapılıyor), FIND-3.10-03, FIND-2.3-02/-03, FIND-9.1-04, FIND-9.2-05 (PC-04 awk yanlış "yok" diyor), FIND-9.2-06, FIND-9.3-01 (AON `module.prop` fazla iddia ediyor), FIND-9.3-02 (README "symlink" diyor, gerçekte bind mount), FIND-4.4-01/-02/-04, FIND-4.2-02, FIND-1.5-01/-02/-03, FIND-2.2-01, FIND-3.2-01, FIND-3.4-01, FIND-9.1-02, FIND-9.2-01. FIND-5.2-01 kayıtta açık (`docs/phase3-preconditions.md:340-351`); IMPL-80 onarımıyla aşılmış olabilir [ÇIKARIM].
- **Denetim kaydı (11. denetim):** 57 bulgu, 10'u aktif. P2 açık: `AUDIT-FIX-22` (ontolojide NUL baytlar). P3 açık: `-37`, `-41`, `-42`, `-50`, `-55`, `-56`, `-57`. P3 kabul edilmiş: `-25`, `-33` (`Planner-docs/Sub-Planing-Audit.md:363-386`). Validator'daki `P2:1,P3:9` sayısıyla tutarlı.
- **Sınırlar:**
  - AGC ön kamera görüntüleri hiç ölçülmedi. Stok kameranın ön görüntüleri 2026-09-05'te temizdi (FIND-3.7-03; `docs/patch-validation-phase4.md:265-299`).
  - `dcgB`/`ln*` için 60 fps kanıtı yok.
  - Sensör blobları yalnızca boyutla korunuyor.
  - md5 guard'ları dosyanın kimliğini doğruluyor, yamanın doğruluğunu değil.
  - Blob'lar `.gitignore`'da olduğu için temiz bir checkout arşivi byte-özdeş üretemiyor (FIND-9.1-02).
  - Kurtarma runbook'u bozuk cihazda gösterilmedi; F9.2-04 yalnızca eski-mod tespitini test etti.
  - AGC'nin açtığı HAL id'si ölçülmedi (OQ-17); OQ-12 kısmi; DNG probu erişilemez (OQ-02/H-03); LN birleşimi denenmedi (H-04).
  - HAL yama tablosu HyperOS 4'te hiç denenmedi (Android 16 derlemesi bırakıldı; Faz8.1'in uzlaşma yarısı yapılmayacak). HyperOS 4'teki HAL (`camera.qcom.so` md5 `2a955e68…`, 2026-11-13'te ölçüldü) tablonun kilitli olduğu AOSPA A15 stok HAL'inden (`HAL_STOCK_MD5` `c3fa63a8…`) farklı; modülün HAL koruması (`ishtar-cam-modes/post-fs-data.sh:101-107`) bu yüzden kapalı başarısız olur (fail-closed) ve HAL katmanını atlar [ÇIKARIM]. Yeniden türetme K9'a bağlı (açık). *(2026-11-16 notu: K9 = hayır, şimdilik (2026-11-15, `DEC-33`); HAL kapalı, sensör sürer.)*

### 5.5 Çalışma kuralları (koşu 21, 2026-11-16)

- **Kimlik değeri (plan §7.3 `:718`; `3 · O3a` `SEC` P2):** kimlik değeri kuralı plan, alt plan ve belge metnini bağlar: IMEI, seri numarası (proje cihazı `dc27e5d0` dışında), `persist.sys.miui.sno` ve tercih değerleri yazılmaz (plan `:715`). Değiştirilmemiş `scripts/smoke.sh` çıktısı (`snapshots/`) muaftır: AGC ayar değerlerini (`prefs.trap.*`, pin) taşır, bunlar kimlik değildir. Yine de kimlik taramasından (plan Ek A.5) geçer ve seri başlığı `dc27e5d0` olur.
- **Tek cihaz penceresi (plan §10 `:811`; `3 · O3b` `SEC` P3):** `Faz10.2`–`Faz10.4` yürütülürken aynı anda yalnız bir cihaz penceresi açık olur. Kural bugün yalnız `Faz10.4` §10'da ("Device window") yazılı; `Faz10.2` ve `Faz10.3` için de geçerlidir.

## 6. Kanıt dizini

`snapshots/` dizininde 207 dosya var: 170 `.txt`, 27 `.jpg`, 4 `.png`, 6 `.xml`. `snapshots/raw/` boş (2026-11-13 ölçümü, `local://snapshot-index.md`). *(2026-11-14 notu: iki IMPL96 snapshot'ı 2026-11-13'te eklendi (`70946ff`); aynı günkü ad taramasında zaman damgalı `.txt` adı 172.)* Adlandırma: `YYYYMMDD-HHMM__<bağlam>__<etiket>`. Saat: addaki saati operatör `smoke.sh -o` ile yazar ve bu saat güvenilir değildir: başlık saatine kimi dosyada UTC, kimisinde UTC+3 (yerel host saati) olarak uyuyor (yerel saat örneği: `docs/agc-12mp-configuration.md:555` vs `:570`). Başlıktaki `taken` satırı UTC'dir ve esastır (2026-11-13 ad ve başlık taraması). README C1'de düzeldi (README:153); Faz3.7:71 hâlâ UTC diyor (`ORCHESTRATION_PLAN.md` §10, koşu 21).

| etiket | sayı | tarih aralığı | neyi kanıtlıyor |
|---|---|---|---|
| faz2.1 | 3 | 2026-08-30 18:40–18:42 | smoke.sh baseline ve duyarlılık testi (IMPL-04) |
| faz2.2 | 7 | 2026-08-31 15:33–16:26 | kurtarma primitifi, v2.1 flash, `BASELINE-2026-08-31-V21` (IMPL-09…12) |
| faz2.3 | 18 | 2026-08-31 16:36–18:21 | on mod regresyonu, reboot kalıcılığı, video geçici çözümü (IMPL-13) |
| faz5.2 | 4 | 2026-08-31 19:06–19:20 | 50mp + dcgB mod-0 12-bit birleşimi ve geri dönüş (IMPL-15) |
| faz3.3 / faz3.4 | 4 / 3 | 2026-09-01 10:55 / 11:18 | tek word yaması ve metadata; tüketici anketi (IMPL-20, -22) |
| Faz3.5 / Faz3.6 | 5 / 1 | 2026-09-01 12:06–13:32 | AGC 50 MP denemeleri; eski Faz 3'ün dinlenme durumu (IMPL-23/24) |
| Faz4.5 | 8 | 2026-09-01 17:23–18:16 | active-array yükseltmesi, bozuk kare artefaktı (IMPL-28…30) |
| Faz4.6 | 41 | 2026-09-01 19:50 – 2026-09-03 09:50 | RAW geometri teşhisi, EV-44, UHR, un-fold (IMPL-31, 33, 35…46) |
| Faz4.1 | 5 | 2026-09-03 15:00–17:30 | daraltma aşamaları, F4.1-07 FAIL (IMPL-48/49) |
| Faz3.7 | 13 | 2026-09-04 16:21–18:34 | pin, HAL taban geçişi, ilk temiz 12.58 MP (IMPL-52…54) |
| Faz3.8 | 6 | 2026-09-05 11:16–11:48 | smoke'a eklenen AGC alanları (IMPL-55/56) |
| Faz3.9 | 10 | 2026-09-05 11:51 – 2026-09-06 23:56 | AGC ve OC'nin birlikte çalışması (IMPL-57/58, 83) |
| Faz3.10 | 18 | 2026-09-05 15:17–15:53 | 4 eksen dayanıklılık matrisi + kontrol, FIND-3.10-03 (IMPL-59…61) |
| Faz3.11 | 8 | 2026-09-05 19:02–19:10 | yapılandırma belgesinin geri okunması; Faz 3 kapandı (IMPL-63) |
| Faz4.2 / Faz4.3 | 4 / 1 | 2026-09-05 19:46–20:01 | duration sayımı; tablo durum matrisi (IMPL-64/65) |
| Faz4.4 | 24 | 2026-09-05 20:17 – 2026-09-06 12:34 | dağıtım kapısı, stok kamera, 10 mod, reboot (IMPL-67/68/70) |
| Faz6.2 | 5 | 2026-09-06 13:05–20:59 | AON baseline, inode, stok modda provider yok (IMPL-75/81) |
| Faz9.2 / release | 11 / 1 | 2026-09-06 20:44 – 2026-09-07 00:55 | v2.2 kurulumu, known-bad testi, VAL-MANUAL (IMPL-80…85) |
| kamerateyit | 4 | 2026-09-08 19:35 – 2026-09-09 17:26 | A/B/C bracket'ları, PC-13 fps analizi (IMPL-87/88) |
| IMPL89 / IMPL94 / DEC26 | 1 / 1 / 1 | 2026-09-10 / 09-13 / 09-14 | bağımsız PTS kontrolü; kiralama kapısı geçilmedi; Scaleway devir metni (doğrulanmamış iddialar) |
| K8 bundle (repo dışı) | 1 | 2026-11-13 | redaksiyon öncesi `integrate/impl-96` ucu; eski hash'lerin tek kaynağı (reflog ile birlikte) |

**Önemli yakalamalar:**
- `20260902-2242__Faz4.6__EV44-fullres-stream-50MP-folded-ORIGINAL.jpg`: AGC'nin ilk 50.33 MP karesi, katlanmış.
- `20260903-0950__Faz4.6__IMPL46-unfold-*.png`: un-fold kanıtı.
- `20260904-1831__Faz3.7__F3706-pinned-ORIGINAL.jpg`: ilk pinli temiz 12.58 MP.
- `20260905-1546__Faz3.10__F31007-control-ORIGINAL.jpg` ve `-2.jpg`: FIND-3.10-03.
- `20260905-1553__Faz3.10__F31009-pin-stickiness-matrix-result.txt`.
- `20260905-1910__Faz3.11__F31110-readback-result.txt`.
- `20260905-2034__Faz4.4__F4403-opencamera-capture-ORIGINAL.jpg`: geçmişteki en büyük blob, 16.04 MiB.
- `20260906-2059__Faz6.2__aon-providers-STOCKMODE.txt`.
- `20260909-1726__kamerateyit__PC13-fps-analysis.txt`.

**En yeni bracket'lar:** cihazdaki son bracket'lar kamerateyit A (2026-09-08 19:35), B (20:30) ve C'dir (2026-09-09 17:04). C, A ile 161 satırın tamamında eşleşiyor (ledger:516–:517). Sonraki üç kayıt (IMPL89/IMPL94/DEC26) cihaz bracket'ı değil, metin kaydıdır. *(2026-11-14 notu: daha yeni kayıt 2026-11-13 tarihli iki IMPL96 snapshot'ıdır (`70946ff`); salt-okur HyperOS 4 tabanıdır, bracket değildir.)* 2026-09-20 cihaz taramasının (`docs/rom-build-device-notes.md`) snapshot'ı yok; IMPL-96 satırının (4). maddesi kaydediyor (ledger:525).

## 7. Belge haritası

| belge | rol | son güncelleme / durum |
|---|---|---|
| `Planner-docs/Planing-Ledger.md` | Kanonik süreklilik kaydı (Ledger v2): koşular, matris, IMPL, durum, tetikler, DEC | son değişiklik C1 (IMPL-96); run 20 2026-11-13'te `7fa0a51`'de commit edildi; CRLF; §6/§7'de bayat satırlar kısmen notlu (§8) |
| `Planner-docs/Main-Planing.md` | Step 1 ana plan: 9 faz, R1–R12 | 2026-09-10 (`SNAP-2026-09-10-MAIN`); CRLF; Hetzner satırları bayat; Faz 7/8 2026-11-13'ten beri amaçsız (koşu 21) |
| `Planner-docs/Sub-Planing-Index.md` | Step 2 dizini: 42 alt plan, sıra, 4a–4d | 2026-09-13 (run 19); LF |
| `Planner-docs/Sub-Planing-Audit.md` | 11. Step 3 denetimi: PASS_WITH_WARNINGS, 57 bulgu | 2026-09-14; 2026-11-13'te `7fa0a51`'de commit edildi; kuyruğu ve §14 kiralama promptu 2026-11-13'ten beri geçersiz |
| `Planner-docs/Project-Ontology.md` | Sözlük, invariant 1–11, OQ-01…17, adres defteri | 2026-09-13 (IMPL-93); 2 NUL bayt (AUDIT-FIX-22) |
| `Planner-docs/Project-Comprehension.md` | CQ/EV/TRACE/ARC/QAS; hipotez durumu yalnızca §8'de | ~2026-09-11 (CQ-13) |
| `Planner-docs/Autopsy.md` | Step 1.5 başlangıç otopsisi, P0–P3 | 2026-08-23; tarihsel |
| `Planner-docs/Faz-<n>-Plans/*.md` (42) | Alt planlar; durumları ledger §4'te, dosyalarda değil | en geç 2026-09-14 (Faz7.2) |
| `docs/build-environment.md` | Faz 7 kiralama runbook'u §1–13 | 2026-09-11 (IMPL-91), Scaleway'e 2026-09-14 (IMPL-95); `03b0898` başına 8 satırlık tarihsel not ekledi; **2026-11-13'ten beri tarihsel** (ROM derleme bırakıldı) |
| `docs/pre-rental-plan.md` | Kiralama öncesi operatör planı, adım 1–4; devir belgesi değil | 2026-09-14; değiştirildi, 2026-11-13'te `7fa0a51`'de commit edildi; `03b0898` başına 8 satırlık tarihsel not ekledi; **2026-11-13'ten beri tarihsel** |
| `docs/rom-build-device-notes.md` | Salt-okur cihaz/ROM taraması (AOSPA A15), yalnızca ekleme yapılır | 2026-09-20; §10 notları 2026-11-13 (kernel girdisinin kapanışı `:239-240` dahil); `03b0898`'den beri izleniyor; IMPL-96 satırının (4). maddesi kaydediyor (ledger:525); telefonun sonradan HyperOS 4 portuna geçtiği 2026-11-13'te gözlendi |
| `docs/release-checklist.md` | Faz9.2: C-01…C-18 / PC-01…PC-18, VAL-INSTALL | son tarihli giriş 2026-09-09; §7 geride; :165 yol hatası C1'de düzeldi (T3) |
| `docs/release-manifest.md` | v2.2 için üretilmiş digest manifesti | elle düzenlenmez; test dışı her build üzerine yazar |
| `docs/recovery-runbook.md` | Kurtarma senaryoları A–D | 2026-09-01 (IMPL-19) |
| `docs/reverse-engineering-toolchain.md` | Host araç zinciri, çıkmazlar, self-check | 2026-08-30; §7 2026-09-11; :22-25 ve :220 bayat |
| `docs/agc-12mp-configuration.md` | AGC 12.58 MP pin kaydı; kanonik iddianın kopyası | 2026-09-05; `:202` yol hatası C1'de düzeldi (T3) |
| `docs/phase3-preconditions.md` | Faz 3 giriş kapısı ve 9 maddelik ölçüm kontrol listesi | 2026-09-05 |
| `docs/patch-table-format.md` | Patch tablosu format sözleşmesi | 2026-09-05 |
| `docs/patch-validation-phase4.md` | Faz4.4 dağıtım doğrulaması | 2026-09-06 |
| `docs/aon-verification.md` | AON kararı, Faz 7 prosedürü, §8.2 negatif baseline | 2026-09-06 |
| `docs/consumer-survey.md` | Faz3.4 tüketici anketi (OQ-03) | 2026-09-01 |
| `docs/regression-v2.1.md` | Faz2.3 on mod regresyonu (v2.1) | 2026-08-31 |
| `docs/mode0-12bit-candidate.md` | Faz5.1–5.3 kaydı | 2026-08-31 |
| `docs/raw-geometry-diagnosis.md` | Faz4.6 teşhis zinciri (28 bölüm; ilk bölümler bayat) | 2026-09-03; bu oturumda politika gereği okunmadı |
| `docs/faz41-predictions-impl48.md` | IMPL-48 öncesi tahminler | 2026-09-03; sonuç notu yok |
| `docs/faz41-predictions-impl49.md` | F4.1-07 öncesi tahminler | 2026-09-03; sonuç notu yok |
| `README.md` | Yol haritası, md5 manifesti, trap uyarısı | 2026-09-05; C1'de güncellendi (v2.2/13, `dist/` `:94`, remote cümlesi `:38`, `snapshots/` izleniyor; §8); kalan bayat satırlar `ORCHESTRATION_PLAN.md` §10'da |
| `CHANGELOG.md` | Sürüm geçmişinin sahibi (v1.2–v2.2) | 2026-09-06 |
| `50MP-Entegrasyon-Plani.md` | ClaudeQB öncesi günlük (Faz 1–12) ve Kararlar | 2026-08-23; bayraklar 2026-09-06 |
| `UNTRACKED-BY-DESIGN.md` | Faz1.1 dışlama kaydı | 2026-08-24; C1'de güncellendi (Faz1.6, DEC-05, remote `:127-131`, silinen loglar; §8); `:36` `2 · O3` kapanışında düzeltildi (Faz 1.1'de 86 dosya); `:33` hâlâ 4 dosya diyor (`ORCHESTRATION_PLAN.md` §10) |
| `ishtar-cam-modes/Kullanim.txt` | Kullanıcı kılavuzu, zip'in içinde | v1.9 içeriği; 13 bayat ifade (K1) |
| `devir-teslim-promptu.md` | Eski devir promptu | 2026-09-09; **2026-11-13'te silindi** (K4); yerini NEXT_PROMPT.md aldı |
| `PROJECT_LOG.md` | Bu belge: proje günlüğü özeti | 2026-11-14; ilk sürüm `775b321`, sonraki sürümler `b603516` (C0), `c2abd46`, C1 ve Pencere 2 aşama commit'lerinde |
| `NEXT_PROMPT.md` | Yeni oturum için yapıştırılacak prompt | 2026-11-14; ilk sürüm `775b321`, sonraki sürümler `b603516` (C0), `c2abd46`, C1 ve Pencere 2 aşama commit'lerinde |
| `ORCHESTRATION_PLAN.md` | Pencere planı: fazlar, kararlar, geçitler, sözleşme (Ek A) | 2026-11-14; C0 ile eklendi (`b603516`; `git log --diff-filter=A -- ORCHESTRATION_PLAN.md`); sonraki sürümler `c2abd46`, C1 ve Pencere 2 aşama commit'lerinde; pencere durumu §1'de |
| `../ishtar-arsiv/impl-96-unredacted.bundle` (repo dışı) | Redaksiyon öncesi `integrate/impl-96` ucu (K8); yalnız yedek | 2026-11-13; 77.094 B; `git bundle verify` geçti |

## 8. Bilinen belge kaymaları ve küçük takipler

Birleşik ve tekilleştirilmiş liste. Kanıtlar extract'lardan alındı; satırlar 2026-11-13'te kısmen kanonik dosyadan teyit edildi. Snapshot dosyaları kanıttır, düzeltilmez.

| dosya:satır | ne diyor | güncel gerçek | kanıt |
|---|---|---|---|
| `Planner-docs/Planing-Ledger.md:100`, `:552` | 11. denetim "outstanding" | **Çözüldü (IMPL-96; ledger `:100`, `:552`):** denetim yapıldı (2026-09-14, PASS_WITH_WARNINGS) ve 2026-11-13'te `7fa0a51`'de commit edildi | `Planner-docs/Sub-Planing-Audit.md:6,18` |
| `Planner-docs/Planing-Ledger.md:101` | Faz7.3 10. denetimi bekliyor | **Çözüldü (IMPL-96; ledger `:101`):** 10. ve 11. denetim yapıldı (RWW); ledger notu son denetimin 11. denetim olduğunu (2026-09-14, PASS_WITH_WARNINGS) yazıyor | `Planner-docs/Sub-Planing-Audit.md:306` |
| `Planner-docs/Planing-Ledger.md:51`, `:554` (ayrıca `:57–:60`, `:556`, `:558`, `:589`) | Step 3 yeniden denetimi "outstanding" | **Kısmen çözüldü (IMPL-96):** 5.–11. denetimler yapıldı; eski `:551`, `:553`, `:555` artık `:554`, `:556`, `:558` ve notlu; `:51`, `:57`–`:60` ve `:589` notsuz (`ORCHESTRATION_PLAN.md` §10, koşu 21) | ledger:29; Audit:6 |
| `Planner-docs/Planing-Ledger.md:528` | 47 commit, 225 dosya, remote yok | **Kısmen çözüldü (IMPL-96, ledger `:528`):** not remote'u ve commit sayılarını yazıyor, dosya sayısını değil. 2026-11-16'da `origin/main`, yerel `main` ve `integrate/impl-96` 87 commit, aynı uçta; 355 izlenen dosya; push edilmemiş commit yok | fact sheet D1; plan §8.1 `W4OPN` |
| `Planner-docs/Planing-Ledger.md:530`, `:532`, `:534` | Modül v2.1/12; cihaz v2.1/stock; canlı HAL stok | **Kısmen çözüldü (IMPL-96):** `:530` ve `:532` notlu, `:534` notsuz. 2026-11-13'ten beri telefon HyperOS 4'te, proje modülü kurulu değil, HAL `2a955e68…`; v2.2/13, mod `50mp`, HAL `fe0245a4…` (2026-09-20 ölçümü) AOSPA A15 dönemine ait | `docs/rom-build-device-notes.md`; ledger:105 |
| `Planner-docs/Planing-Ledger.md:538`, `:542`, `:544`, `:19` | Önkoşullar 3/4; capstone yok; OQ'lar açık; host'ta Python yok | Faz 3 kapandı; araçlar 2026-09-01'de kuruldu; OQ'lar yanıtlandı; CPython var | ledger:76, :86 |
| `Planner-docs/Planing-Ledger.md:599`, `:601`, `:603` | Hetzner CCX53, ~EUR 8.6, Primary IP; DEC-22 başlığında WSL2 | Scaleway POP2-32C-128G, ~EUR 12.8, flexible IP *(2026-11-14 notu: bu kararlar 2026-11-13'ten beri konusuz (`DEC-28`); ledger notları `:599`, `:601`, `:603`.)* | ledger:604 |
| `Planner-docs/Planing-Ledger.md:603` | DEC-25 (3): "sync hatası oturumu durdurur" | Runbook'taki sync-path istisnası eksik (AUDIT-FIX-56) *(2026-11-14 notu: `DEC-25` 2026-11-13'ten beri konusuz (`DEC-28`); ledger `:603`.)* | Audit:379 |
| `Planner-docs/Planing-Ledger.md:106` | Checklist §7'de C-05/09/11/12/13 bekliyor | 7 bekleyen: C-01, C-04, C-05, C-09, C-11, C-12, C-17. C-13 pass | `docs/release-checklist.md:551,558` |
| `Planner-docs/Planing-Ledger.md:578` | "four NCS providers" yok | **çelişki:** `docs/aon-verification.md` §8.2 aperture ve face-scene'in yok olduğunu, ToF'un çalıştığını, OIS'e kanıt bulunmadığını söylüyor | `docs/aon-verification.md:302-327` |
| `Planner-docs/Planing-Ledger.md:66`, `:88`, `:89`, `:92`, `:97` | DEC-01 açık; Faz4.2 "verified'ın altında bırakıldı"; F4.6-07 Faz4.1'e bağlı; `device_ishtar` edit'i commit edilmedi | DEC-01 yanıtlandı; Faz4.2 kapatıldı; Faz4.1 superseded; `713784c` push edildi | ledger:602, :87, :601 |
| `Planner-docs/Planing-Ledger.md:489`, `:585`, `:586`, `:642` | DEC-19/20/21 açık; DEC-11/12 eylemleri borç; Faz5.3 "planned" | Hepsi yanıtlandı; run 4 işledi; Faz5.3 verified | ledger:596–:598, :20, :96 |
| `Planner-docs/Planing-Ledger.md:358-359`, `:493`, `:495`, `:503-504`, `:516-517` | §5 biçimi | IMPL-33, IMPL-32'den önce; kapanış pipe'ı eksik; tabloda boş satırlar; Türkçe satırlar | extract XLedgerImplA/B |
| `Planner-docs/Main-Planing.md:75`, `:211`, `:265` | "rented Hetzner VDS" (R9) | DEC-26: Scaleway (AUDIT-FIX-57) | Audit:380 |
| `Planner-docs/Main-Planing.md:22`, `:61`, `:73`, `:288` | Android 16 başlamadı; "beryl port"; Faz 7–9'u açma | 7.1/8.2 verified; beryl bir dal; hepsi ayrıştırıldı (AUDIT-FIX-42) | Audit:384 |
| `Planner-docs/Main-Planing.md:12`, `:18`, `:57`, `:59`, `:63`, `:65`, `:69`, `:145`, `:159`, `:247`, `:257`, `:259` | v2.1 hiç flash edilmedi; git, smoke ve README yok; HAL `ce419bc9…`; `pref_48m_key=0` denenmedi | Hepsi aşıldı; v2.2 kurulu; taban `fe0245a4…`; Faz3.7 verified *(2026-11-14 notu: v2.2 AOSPA A15'te kuruluydu; 2026-11-13'ten beri HyperOS 4'te proje modülü kurulu değil)* | Audit:63,321,322; Index:252 |
| `Planner-docs/Main-Planing.md:175`, `:181`, `:279` vs `:177` | Duration satırları "eklensin" vs "iş gerekmiyor" | Dosya kendisiyle çelişiyor; Faz4.2 tamam | Audit:336 |
| `Planner-docs/Main-Planing.md:199`, `:219`, `:267`, `:273-282`, `:276`, `:277`, `:292` | SYMLINK sıfır; DEC-22 ve dört karar açık; 10 sonraki adım; adım 5 picturesize anahtarı | Giriş eklendi; kararlar yanıtlandı; adımlar tamam; pin `pref_48m_key=0` (AUDIT-FIX-41) | Audit:314–336,383 |
| `Planner-docs/Sub-Planing-Index.md:6`, `:8`, `:10`, `:65` | `SNAP-2026-09-03`, set 40, Faz 7/8 denetlenmedi; EV-20 "F7.1-12'ye dek" | `-09-10-SUBPLANS`, 42 plan, denetlendi; kayıtlar bu kez Hetzner diyor | Audit:14,318 |
| `Planner-docs/Sub-Planing-Index.md:146`, `:147`, `:389` | Salt-okur sunucu kimliği; düzeltmeler önce GitHub'a; F7.2-01 runbook'u düzeltir | Kimlik bilgisi yok (DEC-25); `fixes.diff` kuralı; IMPL-94 düzeltti | Audit:265,378,414 |
| `Planner-docs/Sub-Planing-Index.md:106`, `:115-125`, `:184`, `:240`, `:319`, `:347` | 3 alan; Faz 4 sırası; kuyruk 4b; Python yok; DEC-16 açık | 4 alan (`-33` kabul edildi); hepsi verified; Audit §12; Python var; DEC-16 yanıtlandı | Audit:350,385; ledger:593 |
| `Planner-docs/Project-Ontology.md:429`; `Planner-docs/Project-Comprehension.md:25`, `:51` | Inv. 11, CQ-13, EV-20: Hetzner CCX53 | Scaleway (AUDIT-FIX-57) | Audit:380 |
| `Planner-docs/Project-Comprehension.md:122`, `:125`, `:149`, `:75` | VAL-INSTALL yapılmadı; F9.2-04 bekliyor; EV-44 "five-word" | VAL-INSTALL PASS (IMPL-81); F9.2-04 PASS (yalnızca eski mod); seven-word | `docs/release-checklist.md:425-469`; `docs/raw-geometry-diagnosis.md:288-313` |
| `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md:18`, `:63`, `:79`, `:196`, `:222-223`, `:292`, `:307`, `:341` | 11. denetimi bekliyor; istisnasız sync durdurur; odm yolu "kiralamadan önce düzeltilecek"; 22283d8'e göre notlanır | Denetim yapıldı; istisna var; IMPL-94 düzeltti (AUDIT-FIX-55); `22283d8` + `fixes.diff` (`-56`) | Audit:305,378,379 |
| `Planner-docs/Faz-7-Plans/Faz7.1-github-input-staging.md:5`, `:56`, `:96`, `:113`, `:188` | Hetzner; device tree private; salt-okur token | Tarihsel; iki repo public; kimlik bilgisi yok | Faz7.2:23,134 |
| `Planner-docs/Faz-8-Plans/Faz8.2-kernel-lts-merge-scoping.md:28`, `:61` | Kernel yolları belirsiz, ölçülmedi | 5.15.185/189 ölçüldü; CSIPHY/CSID ağaç dışında | ledger:103 |
| `Planner-docs/Faz-9-Plans/Faz9.1-reproducible-release-build.md:69`, `:128`; `Faz9.2-release-verification-checklist.md:60` | Kökte 4 arşiv; `build-release.sh` öneriliyor; 13 iddia | v2.2 `dist/` içinde; `.py`; 18 yetenek | glob; ledger:106 |
| `Planner-docs/Faz-4-Plans/Faz4.1-fullres-dimension-guard.md:141`; `Faz4.5-active-array-raise.md:172-174`; `Faz4.6-raw-payload-geometry-diagnosis.md:9,193,242`; `Faz4.7-ultra-high-resolution-sensor-mode.md:145-147` | Bloklu / sıradaki iş | Dosyalarda durum işareti yok; Faz4.1/4.7 superseded | ledger:87–:93 |
| `Planner-docs/Faz-3-Plans/Faz3.1-preference-trap-clearance.md:68`; `Faz3.7-agc-photo-size-pin.md:77`, `:87`; `Faz3.10-pin-stickiness-matrix.md:103`; `Faz3.11-phase-closure-and-configuration-record.md:19`, `:81` | On trap anahtarı, isimle denetim; AGC kendi kurmaz; tek restart; F3.10 NEEDS_REPAIR; DEC-19 bekliyor | On iki anahtar, değerle denetim; 2 anahtar 0'da kuruluyor; iki soğuk başlatma; verified; yanıtlandı | ledger:85, :633, :639, :641 |
| `Planner-docs/Faz-1-Plans/Faz1.1-version-control-bootstrap.md:5`, `:27`; `Faz1.4-toolchain-procedure-record.md:56`; `Planner-docs/Faz-6-Plans/Faz6.1-symlink-entry-in-device-trees.md:54`; `Faz6.2-aon-module-disposition.md:21` | git yok; remote açık; Python yok; SYMLINK 0; modül çalışıyor | Plan zamanının öncülleri, tarih olarak okunur | ledger:60, :66, :69, :97, :578 |
| `docs/pre-rental-plan.md:40`, `:241-242`, `:260-261` | 7.3/8.3 10. denetimde; adım 4 "3a–3c'yi bekliyor"; run 19'u commit et | 11. denetim; 3a–3c tamam; `f724b64`'te commit edildi | PRP:39,130,189,213 |
| `docs/release-checklist.md:165` | `smoke.sh -o snapshots/<…>` | **Çözüldü (C1, T3):** `:165` artık `:414`'teki doğru biçimi kullanıyor. Eski biçimde smoke.sh zaten `snapshots/` eklediği için hedef `snapshots/snapshots/…` olurdu; o dizin olmadığından dosya yazılmaz, betik yine `stored:` basar [ÇIKARIM] | `scripts/smoke.sh:284` |
| `docs/release-checklist.md:9-13`, `:135-154`, `:176`, `:248-251`, `:365-366`, `:421`, `:473`, `:501`, `:620-627` | F9.2-04 çalışmadı; dedektörler kusurlu; onarım cihazda denenmedi; "eight" bekleyen; DEC-20 açık | PASS (IMPL-81); IMPL-80 onardı (AUDIT-FIX-50'nin belge yarısı bekliyor); 7 bekleyen | `docs/release-checklist.md:267-271,425,551` |
| `docs/release-checklist.md:521` vs `:533` | v2.2 "built … IMPL-80" vs "IMPL-77" | **çelişki**, çözülmedi | extract XDocsOps |
| `docs/recovery-runbook.md:238-239`, `:246-247` | ARC-11 `documented`; "F9.2-04 çalışana kadar" | **çelişki:** `docs/release-checklist.md:623-624` `convergent` diyor; F9.2-04 yalnızca eski-mod testi yaptı | extract XDocsOps |
| `docs/reverse-engineering-toolchain.md:22-25`, `:219-220`; `devir-teslim-promptu.md:247` | py 3.14.7; capstone yok; `python` çalışır; Hetzner | **Kısmen çözüldü (K4):** `devir-teslim-promptu.md` 2026-11-13'te silindi; `docs/reverse-engineering-toolchain.md` satırları açık. Araçlar kuruldu; 2026-11-13 kabuğunda `python` ve `python3` Store stub'ı, `py -3` = 3.14.10; Scaleway | fact sheet D3; ledger:76 |
| `docs/regression-v2.1.md:4`, `:30`, `:569-572`, `:613` | v2.1; trap kurulu; FIND sahipleri "Phase 3" | v2.2; değerler 0, zararsız; Faz5.3 (FIND-9.2-04) | ledger:642–:643 |
| `docs/phase3-preconditions.md:173`, `:199-237`; `docs/agc-12mp-configuration.md:377-381`, `:423-426`, `:511` | Araçlar bekleniyor; bütçe kapısı önde; FIND-3.7-02/3.10-01 açık; ön kamera ölçülmedi | Kapandı (IMPL-80); stok kameranın önü ölçüldü, AGC'nin önü ölçülmedi | ledger:634, :636; `docs/patch-validation-phase4.md:265-299` |
| `docs/aon-verification.md:248-266`, `:334-338`, `:364-366`; `docs/consumer-survey.md:76-77`, `:86-88` | Faz7.2 atfı yok; stok mod takibi yapılmadı; FIND-3.4-01 konsolidasyonla geçer; dcgB+OC denenmedi | Faz7.2 atıf yapıyor; takip 2026-09-06'da yapıldı; Faz 4 hiçbir şeyi birleştirmedi [ÇIKARIM]; R'de PASS | ledger:100, :510; `docs/regression-v2.1.md:351` |
| `docs/raw-geometry-diagnosis.md:327`, `:2567`, `:2611`; `docs/mode0-12bit-candidate.md:3-4`, `:183`; `docs/faz41-predictions-impl49.md:33-47` | OC çalıştırılmadı; Faz4.1 bloklu; FIND açık; yalnızca host; P49-2 | OC `com.xiaomi.module.evaluation` olarak kurulu (FIND-4.4-02); superseded; DEC-19; cihazda çalıştı; P49-2 çürütüldü | `docs/patch-validation-phase4.md:485-491`; ledger:87, :641 |
| `docs/rom-build-device-notes.md:79-84` | Kernel "upstreamed by third parties" | **Çözüldü (`03b0898`; `docs/rom-build-device-notes.md:239-240`):** K3 düştü (2026-11-13): telefon zaten 5.15.215 kernelli HyperOS 4 portunda; [ÇIKARIM] iddia bu portu kastediyordu | §2.5; §11 |
| `README.md:18`, `:19`, `:20`, `:77-78`, `:142`, `:143`, `:186` | v2.1/12; AON "symlinking"; 2 smali; v2.1 kurulu; scripts = smoke; UTC adlar; `snapshots/` dışlanmış | **Çözüldü (C1):** v2.2/13; kopyalama + bind mount (FIND-9.3-02); klasörde deneysel tablolar var; `dist/` v2.2; `build-release.py` var; `snapshots/` izleniyor (FIND-2.2-03). Bugünkü yerler: `:18`–`:20` → `:20`–`:22`, `:77-78` → `:85-86` (ve yeni `dist/` paragrafı `:94`), `:142`–`:143` → `:152`–`:153`; `:186` (Exclusions) silindi | `ishtar-cam-modes/module.prop:3-4`; `.gitignore` |
| `UNTRACKED-BY-DESIGN.md:9-10`, `:33-41`, `:61`, `:89`, `:128-130` | Faz1.6 çalışmadı; 84 izlenen dosya; hata `common_clone.log`'da; DEC-05 bekliyor; local-only, DEC-01 açık | **Çözüldü (C1):** README var; 350 dosya (2026-11-14 ölçümü); hata `kernel_clone.log`'daydı, log 2026-11-13'te silindi (K4), içeriği §2.1'de; temiz kapandı; `origin` var. Faz 1.1 sayısı (`:36`) `2 · O3` kapanışında 84'ten 86'ya düzeltildi (ledger `:66`, `:113`). Bugünkü yerler: `:9-10` aynı, `:33-41` → `:33-39`, `:61` → `:59`, `:89` → `:87-88`, `:128-130` → `:127-131` | fact sheet D1; ledger:579, :602 |
| `ishtar-cam-modes/service.sh:9-12`; `50MP-Entegrasyon-Plani.md:1053-1055` | Launcher alias kendini gizler; Kullanim'a AGC metni, "GCam cannot" | v2.1'den beri görünür; Kullanim'da AGC metni yok, neden çürütüldü | `ishtar-cam-modes/Kullanim.txt:59-65`; `CHANGELOG.md:67-76` |
| `devir-teslim-promptu.md` (2026-11-13'te silindi) | IMPL-88 sıradaki; baseline 0/0; 56 commit, remote yok; WSL2; validator depoda | **Çözüldü (K4):** dosya 2026-11-13'te silindi. Sıradaki `IMPL-97`; `--mode all` 1 uyarı (strict ile error); `origin/main`, yerel `main` ve `integrate/impl-96` 87 commit, hepsi push edildi (son 2026-11-16), `origin`; ROM derleme bırakıldı; validator plugin'de | fact sheet D1–D3; plan §8.1 `W4OPN` |
| `…/claudeqb/0.2.1/skills/claudeqb/SKILL.md:148` | Validator `python3` ile | Bu host'ta Store stub'ı; `py -3` kullanılır | fact sheet D3 |
| `Planner-docs/Planing-Ledger.md:602` (`DEC-01`); `docs/pre-rental-plan.md:258` | Remote = özel `ahmetxa/ishtar`; push hedefi "private `origin` (`ahmetxa/ishtar`)" | **Çözüldü (IMPL-96; ledger `:602`, `:605`):** 2026-11-13'ten beri `origin` = özel `ahmetxa/ishtar_cam_modes` (62 commit aynı hash'lerle); eski deponun yerel remote'u (`ishtar-eski`) kaldırıldı, `ahmetxa/ishtar` silinecek (`DEC-30`); `DEC-27` kaydedildi, `DEC-01` notlu; `docs/pre-rental-plan.md` 2026-11-13'ten beri tarihsel (`03b0898`) | §2.1; §11 |
| `README.md:144`; `UNTRACKED-BY-DESIGN.md:38-41`, `:63` | `common_clone.log` ve `kernel_clone.log` kayıt olarak duruyor | **Çözüldü (C1):** 2026-11-13'te silindi (K4); içerikleri §2.1'de alıntılı (T2); bugünkü yerler UNTRACKED `:38`–`:39`, `:61`; README satırı kaldırıldı | §11 |
| `Planner-docs/Planing-Ledger.md` §6; `docs/rom-build-device-notes.md`; `docs/agc-12mp-configuration.md`; `F3.11-09` | Telefon AOSPA A15 + KernelSU Next | **Kısmen çözüldü (IMPL-96, ledger `:532`; `03b0898`):** ledger §6 `:532` ve `docs/rom-build-device-notes.md` §10 2026-11-13 gözlemini kaydediyor; `docs/agc-12mp-configuration.md` ve F3.11-09 (ledger `:647`–`:651`) notsuz. 2026-11-13 kullanıcı beyanı: HyperOS 4 portu, kernel 5.15.215; ölçüm: `OS4.0.0.44.WMACNXM`, kernel `5.15.215-KylinKernel-260925-Release`, KernelSU `4.3.0-r1`, KernelSU Next uygulaması yok (2026-11-13; `70946ff`; ledger §6 `:532`; DEV `:223`–`:244`) | §2.3 |
| `Planner-docs/Main-Planing.md` Faz 7/8; `Planner-docs/Sub-Planing-Audit.md` §12, §14; `docs/build-environment.md`; `docs/pre-rental-plan.md` | ROM derleme ve kiralama planı | 2026-11-13: ROM derleme bırakıldı (K2); planlama koşusu 21 bekleniyor | §2.5 |

**Küçük takipler:**
- **`ishtar-cam-modes/Kullanim.txt`: 13 bayat ifade** (`local://prior-ToolingSurfaces.md` §4):
  1. `:1` başlık v1.9.
  2. `:46` 50mp HAL modu yok.
  3. `:53-57` 3 tile var diyor (gerçekte 4).
  4. `:56` ile `:69-70` kendi içinde çelişiyor.
  5. `:102` Superuser etiketi uygulama adıyla uyuşmuyor.
  6. `:119-122` WebUI'de "3 düğme" diyor.
  7. `:135-139` / `:146-150` örneklerinde `50mp` eksik.
  8. `:246-250` HAL katmanından söz etmiyor.
  9. `:253-257` HAL md5 kilidinden söz etmiyor.
  10. `:45` video için reboot gerekmez diyor (FIND-2.3-06).
  11. `:212` CSIPHY imzasını teşhis olarak veriyor, oysa teşhis koydurmaz (FIND-2.3-04).
  12. `:214-215` stok kameranın çöktüğünü söylüyor (IMPL-70/88 bunu çürüttü).
  13. AGC 12.58 MP yapılandırması hiç anılmıyor.
  - Hiçbiri AGC'de 50 MP iddiasında bulunmuyor. Düzeltme kararı K1'e bağlı.
- **README / UNTRACKED-BY-DESIGN:** **Çözüldü (C1):** v2.2, `dist/`, `docs/`, remote, CHANGELOG ve `snapshots/` izleme durumu güncellendi (T2); remote cümlesi README `:38`'de. `candidates/*.bin` ignore kuralının gerekçesi artık UNTRACKED-BY-DESIGN `:71`'de (`.gitignore:58`).
- **release-checklist:** §7 satırları ölçülmüş sonuçların gerisinde. IMPL-82/85 sonuçları aktarılmadı, VAL-MANUAL çalıştırılmadı, AUDIT-FIX-50'nin belge yarısı bekliyor; `:165` yol hatası C1'de düzeltildi (T3).
- **Ledger:** IMPL-96 yazıldı (`:525`; IMPL-96 notları §4 `:97`, `:100`–`:102`, `:104`; §6 `:528`, `:530`, `:532`, `:542`; §7 yeni girdi `:550`, `:552`–`:558`, `:567`; §8 `:602` ve konusuz notları); kapsamı §2.6'daki L biriminde: 11. denetim ve geçersiz kuyruk; §4 Faz 7/8 engel hücreleri; §6 depo ve cihaz paragrafları; §7'ye ROM derlemenin bırakılması ve "vendor blobs changed" girdileri; "outstanding" metinlerinin ve kernel iddiasının kapanışı; 2026-09-20 notları; K4 silinenleri. Notsuz kalan "outstanding" metinleri (`:51`, `:57`–`:60`, `:589`) koşu 21'e kaldı (`ORCHESTRATION_PLAN.md` §10).
- **AUDIT-FIX-22:** ontolojinin `Escape` sütunu ham kontrol baytları içeriyor ve bir arama aracı bunda sessizce başarısız oluyor. Değerlendirmesi `Planner-docs/Sub-Planing-Audit.md:377`'de.
- **Kökteki boş dizin `UsersahmetAppDataLocalTempaon-smoke/`** (2026-09-09, bozulmuş bir Windows temp yolu): 2026-11-13'te silindi (K4).

## 9. Riskler

| R | şiddet (MP) | 2026-11-13 durumu | kaynak |
|---|---|---|---|
| R1 sürüm kontrolü yok | kritik | Azaltıldı: git ve private remote var; 2026-11-13'ten beri 62 commit'in tamamı yeni `origin`'de (`ahmetxa/ishtar_cam_modes`), eski depo 4 commit geride (bkz. N3) | `Planner-docs/Main-Planing.md:247`; fact sheet D1 |
| R2 ağaçta keystore | yüksek | Faz1.2 tamam; A1 assertion'ı 2026-11-13'te PASS; DEC-10. Keystore host'ta tek kopya | MP:249; `docs/rom-build-device-notes.md` |
| R3 root yazımları yalnızca md5 ile korunuyor | yüksek | Yapısal olarak sürüyor; guard'lar kimliği doğruluyor, doğruluğu değil. HyperOS 4'te fail-closed: sensör ya da HAL md5'i tutmazsa mount yok (`ishtar-cam-modes/post-fs-data.sh:35-51`, `:101-107`) | MP:251 |
| R4 AGC'de 50 MP | eskiden yüksek | "CLOSED as a risk, realised as an outcome"; yerini R12 aldı | MP:253 |
| R5 otomatik doğrulama yok | yüksek | smoke + checklist + self-test var; yalnızca cihazda; tasarım gereği CI yok | MP:257 |
| R6 release hiç flash edilmedi | orta | Çözüldü; v2.2 kurulu (VAL-INSTALL) *(2026-11-14 notu: v2.2 AOSPA A15'te kuruluydu; HyperOS 4'te kurulu değil (2026-11-13 ölçümü).)* | MP:259 |
| R7 bilgi tek belgede | orta | Ontoloji ve comprehension var ama kusurlu: NUL baytlar (`-22`), IMPL-52…54 eksik (`-37`), Hetzner metni (`-57`) | MP:261; Audit:377–382 |
| R8 tek vendor bloba bağımlılık | orta | **Gerçekleşti:** telefonun HyperOS 4 portuna geçtiği 2026-11-13'te gözlendi. Aynı günkü ölçüm (`70946ff`): HAL farklı (`2a955e68…`), sensör blobu aynı (`EXPECT_MD5`). 16 noktalı tablo AOSPA HAL'ine (`c3fa63a8…`) kilitli: modül kurulursa HAL guard'ı fail-closed davranıp HAL katmanını atlar, sensör katmanı mount olur [ÇIKARIM]. HAL katmanının yeniden türetilmesine K9 karar verir (`ORCHESTRATION_PLAN.md` §2, §7) | MP:263 *(2026-11-16 notu: K9 = hayır, şimdilik (2026-11-15, `DEC-33`); HAL kapalı, sensör sürer.)* |
| R9 Windows derleyemiyor | orta | Konusuz: ROM derleme bırakıldı (K2, 2026-11-13); önce kiralık sunucu planlanmıştı (DEC-24→26) | MP:265 |
| R10 RE'de token kullanımı | orta | Faz 3 yalnızca yapılandırma oldu; HyperOS 4'e uyarlama seçildi (K7 = (a), `DEC-32`): 50MP katmanı için yeniden tersine mühendislik K9'a bağlı | MP:267 *(2026-11-16 notu: K9 yanıtlandı 2026-11-15, `3 · O0`: hayır, şimdilik (`DEC-33`); HAL katmanı HyperOS 4'te kapalı, sensör katmanı sürer.)* |
| R11 karışık dil | düşük | Kabul edildi: kullanıcıya dönük TR/EN, planlama belgeleri EN | MP:269 |
| R12 AGC'nin sessizce 50 MP'ye dönmesi | orta | Dedektörler var (IMPL-55/56, 60/61). Her AGC güncellemesi veya `.agc` import'u sonrası yeniden doğrulanmalı; FIND-3.10-02 rotası bilinmiyor | MP:255 |

**Yeni riskler (2026-11-13):**
- **N1 Kiralama maliyeti:** konusuz; kiralama hiç yapılmadı ve ROM derleme bırakıldı (K2). Kurallar `docs/build-environment.md` §3–§4 ve §12'de tarihsel olarak duruyor.
- **N2 Kernel iddiası:** düştü (K3, 2026-11-13).
- **N3 Uzak depolar:** `origin`'de 87 commit; `main` ve `integrate/impl-96` = C3, push edilmemiş commit yok (Pencere 4 açılışı, 2026-11-16; §2.1). Sonraki her push ayrı onayla ve yalnız açık refspec ile. ROM derleme fikri için açılan üç depo silinecek (K5/K6, silmeyi kullanıcı yapar); yedekler §2.1'de.
- **N4 Ledger geride:** **Çözüldü (IMPL-96):** ledger bu oturumu (depo taşıma, ROM kararı, HyperOS 4 ölçümü, silinen dosyalar (K4) ve silinecek depolar (`DEC-30`)) IMPL-96 satırında anıyor (ledger:525); ledger §6, §7 ve §8'deki bayat satırlar kısmen notlu (§8).
- **N5 HyperOS 4'te AGC ve uyarlama:** AGC tuzak anahtarları kurulu (`prefs.trap.armed = 10`) ve yamasız V9.6 APK yüklü. AOSPA'da bu tuzaklar gcam başlatmasını bozuyordu; HyperOS 4'teki etkisi ölçülmedi. Uyarlama seçildi (K7 = (a), `DEC-32`): 50MP katmanı yeni HAL'de yeniden türetme ister (R10); kutucuk/WebUI zinciri KernelSU Next yöneticisine bağlı, bu ROM'da yok.
- **Diğer:**
  - 2026-09-20 oturumunun kaydı yoktu (süreklilik boşluğu); IMPL-96 kaydetti (ledger:525, madde 4).
  - `gh` PATH'te yok (tam yolla çalışıyor; `delete_repo` yetkisi yok); `python` stub'ı; validator depoda değil.

## 10. Kimlik şeması ve sözlük

| kimlik | anlam | nerede / sıradaki |
|---|---|---|
| `IMPL-NN` | Uygulama koşusu (Step 4); her koşu bir satır | ledger §5; sıradaki **IMPL-97** |
| planlama koşusu N | Step 1/2 (ve eski denetim) koşuları | ledger §2; sıradaki **21** |
| N. denetim | Step 3 denetimi; yalnızca `Sub-Planing-Audit.md`'ye yazar, kendi koşu satırı yok | sıradaki **12.** |
| `DEC-NN` | Kullanıcı kararı | ledger §8; sıradaki **DEC-33**; `DEC-27`…`DEC-32` 2026-11-13'te ayrıldı, ledger'a yazıldı (`:605`–`:610`) *(2026-11-16 notu: `DEC-33` (K9) planlama koşusu 21 ile ledger `:619`'a yazıldı (`3 · O4`); sıradaki `DEC-34`.)* |
| `FIND-x.y-NN` | Faz x.y'nin bulgusu; atamadan önce kullanılmadığı kontrol edilir | ledger, belgeler |
| `AUDIT-FIX-NN` | Denetim kaydı maddesi, P0–P3 (şu ana dek 57) | Audit §13 |
| `AUTOPSY-Pn-NN` | Otopsi öncelik bulguları | `Planner-docs/Autopsy.md` §13 |
| `Faz x.y` / `F<x.y>-NN` | Alt plan / iş maddesi (`Planner-docs/Faz-<n>-Plans/Faz<x.y>-<slug>.md`) | 42 dosya |
| `VAL-*` | Doğrulama komut kimliği (ör. VAL-SYNC, VAL-INSTALL, VAL-BUILD2) | alt planlar |
| `C-NN` / `PC-NN` | Release iddiası / probu (01–18) | `docs/release-checklist.md` |
| `SNAP-YYYY-MM-DD-{MAIN,SUBPLANS,AUTOPSY}` | Plan snapshot'ı; etkin olanlar `-09-10-MAIN/-SUBPLANS` | ledger §3 |
| `EV`/`CQ`/`H`/`TRACE`/`ARC`/`QAS`; `OQ` | Comprehension kayıtları; ontoloji soruları | Comprehension; Ontology §8 |
| `Kararlar #n`; `BASELINE-2026-08-31-V21`; `K1–K9` | Günlük kararları; adlandırılmış baseline; oturum kararları | günlük; ledger:73; §4 |
| `O0`–`O5`; `O2-a`/`O2-b`; `T1`–`T5`, `L`, `M`, `RUN21`, `V` | 2026-11-13 orkestrasyon aşamaları (kullanıcının komut şablonundaki "Faz 0–5") ve iş birimleri; proje fazı değildir | §2.6; §11; aşağıdaki not |
| `Pencere N`; `N · Ok` | `ORCHESTRATION_PLAN.md` fazı (Pencere 0, 1, 2 …) ve o fazın aşaması (ör. `2 · O3`: Pencere 2'nin `O3` aşaması; 2026-11-13 oturumunun `O0`–`O5`'iyle karışmasın); ClaudeQB fazı değildir | `ORCHESTRATION_PLAN.md` §0, §1 |
| `W1`–`W6`, `T3`, `I1`, `REV`, `SEC`; Pencere 2'de `K0`, `SEC-A1`–`SEC-A3`, `SEC-B`, `REV-1`–`REV-3`, `I2a`, `I2b`, `GATE`, `FIX`, `C1`/`C2`, `FF`, `RID`, `PUSH`, `LSR`; Ek A `REL`, `TRAP`, `G`/`D`/`V`/`E` | `ORCHESTRATION_PLAN.md`'nin görev ve olgu kimlikleri (`K0` görev kimliğidir, karar değildir); risk `R1`–`R12`, karar `K1`–`K9`, kontrol listesi `C-NN` ile karışmasın diye seçildi (`R21` → `RUN21` ile aynı gerekçe) | `ORCHESTRATION_PLAN.md` §3 |
| durum sözlüğü | `planned`, `ready`, `ready_with_warnings`, `in_progress`, `implemented`, `verified`, `blocked`, `superseded`. Bileşik değer parser'ı bozar | ledger:97 |

**"Faz" adının üç anlamı (2026-11-13 adlandırma denetimi):**
1. **ClaudeQB proje fazları:** `Faz 1`–`Faz 9` (`Planner-docs/Main-Planing.md`), alt planlar `Faz n.m`, iş maddeleri `Fn.m-NN`. Belgelerde tek başına "Faz N" her zaman bunu anlatır. Faz 2 = "v2.1'i yayımla ve yeniden taban al": 4/4 verified, 2026-09-06'da kapandı (§3.1).
2. **Günlük fazları:** `50MP-Entegrasyon-Plani.md` (ClaudeQB öncesi, 2026-08-20…08-23) Faz 1–12; Faz 10 ("Android 16 / beryl hazırlığı", J:96-102) yalnız planlandı, bloke kaldı ve hiç yapılmadı. İçerikleri ClaudeQB fazlarıyla örtüşmez (ör. günlük Faz 2 = HAL ikili yamasının gerekip gerekmediği). §3.4'te "Günlük fazı" sütunuyla ayrılır.
3. **Orkestrasyon aşamaları:** 2026-11-13 oturumunda kullanıcının komut şablonundaki "Faz 0–5"; bu belgede `O0`–`O5`. O oturumun sohbetindeki "Faz 2 onay bekliyor" ifadesi `O2`'yi kastediyordu, proje Faz 2'sini değil.

Ek not: `docs/pre-rental-plan.md`'deki "Step 1–4" o planın kendi sırasıdır ve ClaudeQB Step'leriyle yalnız kısmen örtüşür: step 1 = checkpoint commit'i, step 2 = planlama koşusu 19 (ClaudeQB Step 2), step 3 = 10. denetim (Step 3), step 3a = `IMPL-95`, step 3b = planlama koşusu 20, step 3c = 11. denetim, step 4 = kiralama günü (bir ClaudeQB Step 4 oturumu).

**Sözlük (25 terim):**
1. **ishtar:** Xiaomi 13 Ultra (SM8550); çalışma alanının adı da bu.
2. **beryl / vauxite / calcite:** AOSPA dalları (A16 / A15 / sonraki). Cihaz adı değiller.
3. **IMX989:** 1 inçlik ana sensör, 8192x6144 (50.3 MP).
4. **QCFA:** Quad-Bayer düzeni; tam çözünürlük remosaic gerektirir.
5. **DCG (`dcgA`/`dcgB`):** Dual conversion gain modları; `dcgB` tercih ediliyor.
6. **LN2/LN4 (s/f):** Düşük gürültülü binning modları.
7. **`stock`:** Hem bir mod adı hem geri dönüş hedefi.
8. **`50mp`:** Mod adı. HAL katmanını açar, sensörü stoğa zorlar.
9. **`fullres`:** 16 noktalı yamanın ürettiği HAL durumu; mod adı değil.
10. **Mod:** On değerden biri olan tek çalışma zamanı durumu (`$MODDIR/mode`).
11. **Patch tablosu:** md5 korumalı ikili düzenleme listesi; kanonik ya da deneysel.
12. **Sensör / HAL / uygulama katmanı:** sensör `.bin` mount'u / `camera.qcom.so` yaması / AGC smali yaması.
13. **AGC:** AOSPA döneminde kullanılan Google Camera portu (8.4.300 V9.6, md5 `ce65f862…`); HyperOS 4'te kurulu olan yamasız V9.6 (md5 `fa4066eb…`, 2026-11-13 ölçümü).
14. **Open Camera:** `com.xiaomi.module.evaluation` adıyla kurulu, 50 MP referans uygulaması.
15. **AON:** AON → CSS → NCS zinciri; `ishtar-aon-fix` buna yönelik.
16. **Tile:** Birbirini dışlayan dört QuickSettings karosundan biri.
17. **Katman dışlaması:** `50mp` ile DCG/LN birlikte kullanılamaz (Kararlar #1); bilerek korunuyor.
18. **Tercih tuzağı:** `pref_raw_key*` / `pref_fix_resolution_key*` (12 anahtar) değerle denetlenir; kök `.agc` dosyaları import edilmez.
19. **Pin:** `pref_48m_key=0` + `pref_camera_resolution=full` → `4096x3072`, ardından iki soğuk başlatma.
20. **Black fraction:** IMPL-40 yöntemi; < 0.01 temiz, ~0.75 katlanmış.
21. **Smoke bracket:** Her cihaz değişikliğinden önce ve sonra `scripts/smoke.sh -o`; karşılaştırılabilir bölge byte-özdeş olmalı.
22. **barista:** AOSPA'nın proje karıştırıcısı; `lunch` çıkış durumunu yok sayar. *(2026-11-14 notu: Faz 7 işi; `DEC-28` ile 2026-11-13'ten beri tarihsel.)*
23. **`fixes.diff`:** Sunucuda yapılan manifest düzeltmeleri; oturum içinde push edilmez. *(2026-11-14 notu: Faz 7 işi; `DEC-28` ile 2026-11-13'ten beri tarihsel.)*
24. **Teardown:** Instance, 3 volume ve flexible IP silinir; dört sıfır sayımı. *(2026-11-14 notu: Faz 7 işi; `DEC-28` ile 2026-11-13'ten beri tarihsel.)*
25. **ClaudeQB adımları:** Step 1 (ana plan), 1.5 (otopsi/ontoloji), 2 (alt planlar), 3 (denetim), 4 (uygulama); bounded amendment snapshot kesmez.

## 11. Oturum günlüğü

**2026-11-13: orkestratör koşusu (omp).** Kayıt, fact sheet D1–D5'e dayanıyor. Bu girişler bir IMPL satırı değildir; ledger'a henüz işlenmedi (bkz. L iş birimi).

- **O0 keşfi:**
  - Üç keşif (LedgerState, WorktreeDiff, ToolingSurfaces), validator ve self-test çalıştırıldı.
  - Git: `main` 62 commit, HEAD `587e3b5`, `origin/main` `f8a05ca` (4 ileride), 344 izlenen dosya. `git fsck` temiz; hiçbir blob 50 MiB'ı aşmıyor.
  - Ortam: `python`/`python3` Store stub'ı; `py -3` = CPython 3.14.10; `gh` PATH'te yok; git-lfs 3.8.1.
- **Validator** (`--mode all`, plugin yolu): `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`. HEAD ağacında da aynı sonuç. `--strict` bu uyarıyı error'a yükseltir; bu beklenen baseline'dır, regresyon değil.
- **Self-test:** `py -3 scripts/build-release.py --self-test` → `SELF-TEST: PASS`. VAL-BUILD2 byte-özdeş, sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0`. A1/A2/A3 PASS. Yalnızca geçici dizinlere yazdı.
- **O1 planı hazır ve kullanıcının birebir "onay"ını bekliyor (O2).** İş birimleri: O2-a, T4, O2-b, T1 (yalnızca K1=(a) olursa), T2, T3, T5, L, RUN21, V. K1–K4 yanıt bekliyor (§4). Hiçbir iş başlatılmadı.
- **Yazılan belgeler:** kullanıcının isteğiyle `PROJECT_LOG.md` ve `NEXT_PROMPT.md` kökte oluşturuldu (izlenmiyor). Hiçbir şey commit ya da push edilmedi.
- **GitHub aktarımı sorusu sohbette yanıtlandı:** tam geçmiş hash'ler değişmeden aktarılabilir (62 doğrusal commit, tag yok, tek kimlik, 50 MiB üstü blob yok, keystore/apk/zip/so/bin hiç izlenmemiş). Herhangi bir eylem yapılmadı, push edilmedi.
- **Olgu kontrolü:** üç bağımsız reviewer (`PROJECT_LOG.md`'nin iki yarısı ve `NEXT_PROMPT.md`) API hız sınırına (429) takılıp sonuç vermeden düştü. Yerine orkestratör hedefli kontrol yaptı: iki dosyada tablo yapısı (0 bozuk satır); §3.2'de IMPL-01…IMPL-95 ve IMPL-96 (planlı) birer kez; §4'te DEC-01…DEC-26 birer kez; §3.5'te 62/62 commit; checklist §7 sayıları (`docs/release-checklist.md:539-558`); `dist/ishtar-cam-modes-v2.2.zip`'in varlığı; runbook §4 bütçe ve durma kuralları ile §12'deki dört sıfır sayımı; IMPL-92 ile cihaz notları §7 arasındaki çelişki (ledger satır 521). Satır satır bağımsız inceleme yapılmadı; kritik bir hücre kullanılmadan önce kaynak sütunundaki dosyadan teyit edilmelidir.
- **GitHub taşıma (kullanıcı onayı, 2026-11-13):**
  - Push öncesi tüm geçmişte (eklenen satırlar) sır taraması: GitHub/AWS/Slack/Scaleway token kalıbı ve özel anahtar yok; IPv4 eşleşmeleri sürüm dizgisi (`3.3.0.0` vb.); tek parola eşleşmesi `ishtar-cam-modes/tile-app/build.sh`'teki kabul edilmiş debug imza varsayılanı (`DEC-10`).
  - GitHub MCP ile boş özel depo `ahmetxa/ishtar_cam_modes` açıldı (alt çizgi destekleniyor; README eklenmedi).
  - Remote'lar: eski `origin` → `ishtar-eski`; yeni `origin` = `https://github.com/ahmetxa/ishtar_cam_modes.git`; `git push -u origin main` (yalnız `main`, tag yok; commit edilmemiş set ve izlenmeyen dosyalar gönderilmedi).
  - Doğrulama: `git ls-remote origin` → `refs/heads/main` = `587e3b581a66961082e49e2449327478724ad765` = yerel `main`; `git status -sb` → `main...origin/main`; kök `ff6934e` API'de aynı hash, tarih (2026-08-24) ve yazar (`ahmetxa`); `gh api` (tam yol, kimliği doğrulanmış) → `private=true`, `default_branch=main`.
  - Bekleyen: ledger'a `DEC-27` kaydı (IMPL-96); eski deponun akıbeti (K5).
- **Adlandırma denetimi (kullanıcı sorusu):** "Faz" üç ayrı numaralamada geçiyor (§10). Kullanıcının hatırladığı doğru: ClaudeQB Faz 2 (ve günlük Faz 2) çoktan tamamlandı; sohbetteki "Faz 2" orkestrasyon aşamasıydı. Bu belgede ve `NEXT_PROMPT.md`'de orkestrasyon aşamaları `O0`–`O5`, iş birimleri `O2-a`/`O2-b` ve `RUN21` (eski `R21`; R-risk kimlikleriyle karışıyordu) olarak yeniden adlandırıldı.
- **Kullanıcı kararları (2026-11-13, ikinci tur):**
  - K1 = (b): `Kullanim.txt` bir sonraki sürümde düzeltilecek.
  - K2: ROM derleme fikri bırakıldı. Kullanıcı beyanı: telefonda Çinli bir geliştiricinin portladığı HyperOS 4 çalışıyor; kernel 5.15.215; günlük kullanımda. Ölçülmedi. Sonuç: Faz 7/8 amaçsız; ledger §7'deki "vendor blobs change through a system update" tetikleyicisi ateşlendi; resmî kapanış planlama koşusu 21'de.
  - K3: kullanıcıya göre gereksiz; düştü.
  - K4: onaylandı ve uygulandı. Silinenler: `devir-teslim-promptu.md`; `install.log` (izlenen snapshot ile satır satır aynı, CR hariç); `common_clone.log`; `kernel_clone.log`; boş `UsersahmetAppDataLocalTempaon-smoke/`. Üç log `.gitignore:48` (`*.log`) yüzünden hiç izlenmemişti. Boş `snapshots/raw/` log olmadığı için bırakıldı.
  - K5: kullanıcı `ahmetxa/ishtar`'ın ROM derleme fikri için açıldığını ve bu fikirden vazgeçtiğini söyledi; sil ya da arşivle netleşmesi istendi. `gh` belirteci kapsamları: `repo`, `workflow`, `gist`, `read:org` (`delete_repo` yok). GitHub'da `ahmetxa/ishtar` özel; `ahmetxa/android_local_manifests` ve `ahmetxa/android_device_xiaomi_ishtar` halka açık; hiçbiri fork ya da arşiv değil.
  - Yeni sorular: K6 (iki halka açık ROM deposu), K7 (projenin HyperOS 4'teki yönü).
- **Modül boot koruması okundu:** `ishtar-cam-modes/post-fs-data.sh` sensör md5'i `EXPECT_MD5` (:35-51) ya da HAL md5'i `HAL_STOCK_MD5` (:101-107) tutmazsa hiçbir şey mount etmeden çıkar; HyperOS 4'te dosyalar farklıysa kurulu modül stok davranışı korur.
- **Günlük Faz 10 düzeltmesi:** `50MP-Entegrasyon-Plani.md:96`'da `## Faz 10 — Android 16 / beryl hazırlığı` başlığı var (planlanmış, bloke, yapılmamış); §3.4 ve §10 buna göre düzeltildi.
- **`NEXT_PROMPT.md` yeniden yazıldı:** sıradaki faz artık kiralama günü değil; depo hijyeni ve IMPL-96 kaydı → HyperOS 4 salt-okunur taban ölçümü → K7 → planlama koşusu 21 → 12. denetim.
- **Üçüncü tur (2026-11-13). Kullanıcı: K5/K6 sil, `O2` onay, telefon bağlı, yanıtlar Türkçe olsun.**
  - Ön kontrol: commit edilecek dört dosyanın farkında sır yok (401 eklenen satır, 0 eşleşme); `ishtar-eski/main` yerel `main`'in atası; silinecek depolarda release, tag ya da issue yok.
  - Bilgisayara üç cihaz bağlıydı: ishtar `dc27e5d0`, başka bir telefon ve bir emülatör. Tüm adb komutları yalnız `dc27e5d0`'a gitti (`-s`, smoke.sh için `ANDROID_SERIAL`).
  - Commit'ler: `7fa0a51` (`main`); dal `integrate/impl-96`: `37edb5f` (kanıt), `6a20999` (tarihsel notlar + cihaz notları), oturum belgeleri. Push yok.
  - İki açık deponun ayna yedeği alındı; `ishtar-eski` remote'u kaldırıldı. Silme yapılmadı (`delete_repo` yetkisi yok).
  - HyperOS 4 ölçümünün sonuçları §2.3'te. İlk ana bilgisayar ayrıştırması yanlış başlığı hedefledi; snapshot'taki o bölüm aynı oturumda doğru sonuçlarla değiştirildi ve diğer telefonun seri numarası kayıttan çıkarıldı.
  - Bağlam büyüklüğü nedeniyle ledger IMPL-96 satırı bilerek yeni pencereye bırakıldı.

**2026-11-13: Pencere 0 (omp, ikinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` Pencere 0 (keşif, plan, sözleşme). Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı.

- **O0 keşfi (salt-okur):**
  - Dört scout paralel çalıştı: `LedgerMap`, `PlanDocsMap`, `ModuleMap`, `DocsFactCheck`. Olgular `ORCHESTRATION_PLAN.md` Ek A'da, kapsam dışı bulgular §10'da.
  - GitHub (`gh api`, 2026-11-13): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests` ve `ahmetxa/android_device_xiaomi_ishtar` üçü de hâlâ var. Silme yapılmadı.
  - Telefon (`dc27e5d0`): prop'lar ve md5'ler probe ile aynı (HAL `2a955e68…`, sensör `9e4d0fe1…`, AON sembolik bağı, 13 modül, proje modülleri yok, AGC versionName `8.4.300.414775575.18`).
  - Doğrulayıcı ve self-test taban ile aynı: `error_count=0`, `warning_count=1` (`P2:1,P3:9`), `subplan_count=42`; `SELF-TEST: PASS`.
- **Gizlilik bulgusu:** Commit edilmiş ama push edilmemiş probe anlık görüntüsü cihaz tanımlayıcıları içeriyordu (iki IMEI ve bir `persist` özelliği). Değerler hiçbir dosyaya, rapora ya da mesaja yazılmadı; kontroller maskeli yapıldı. Bu girdide de değer yazılmamıştır.
- **O1 plan ve onay:** `ORCHESTRATION_PLAN.md` yazıldı; kullanıcı "onay" dedi. Pencere-fazı kuralı kullanıcının isteğidir.
- **Kararlar (2026-11-13):** K7 = (a) → `DEC-32`; K8 = A → `DEC-31` (yürütüldü); konusuz = `DEC-07`, `DEC-08`, `DEC-22`, `DEC-24`, `DEC-25`, `DEC-26`; K9 açık (Pencere 3); push açık (Pencere 2). Ledger'a yazılacak numaralar: `DEC-27`…`DEC-32`; sonraki boş numara `DEC-33`.
- **Kabul edilen danışma noktaları:** adlandırılmış yedek dal açılmadı; redaksiyonsuz bundle depo dışında; push yalnız açık refspec ile; push öncesi güvenlik incelemesi `origin/main..integrate/impl-96` aralığının tamamını kapsar (`7fa0a51` dahil).
- **K8 yürütümü:**
  - Bundle: `../ishtar-arsiv/impl-96-unredacted.bundle`; 77.094 B; sha256 `b9fa9c5cd5d0ae78f9f051ab62ecbfc2d9b2fa2fecd33f40247ef88bf58f6cd3`; `git bundle verify` geçti; önkoşul `7fa0a51`.
  - Hash eşlemesi: `37edb5f` → `70946ff` (probe satır 42, 190, 191 `<redacted>`); `6a20999` → `03b0898`; `fcceaab` → `775b321` (içerik aynı). Eski ağaca göre fark yalnız bu üç satır.
  - Maskeli tarama: tüm ref'lerden erişilebilen geçmişte 0 eşleşme. Eski hash'ler yalnız bundle'da ve yerel reflog'da. Güncel metinler (§2, §3.2, §4) yalnız yeni hash'leri kullanır; eski girdiler olduğu gibi kalır.
  - Geçitler: doğrulayıcı ve self-test taban ile aynı (yukarıda).
- **Belgeler:** `ORCHESTRATION_PLAN.md` (C0 ile eklendi); `NEXT_PROMPT.md` Pencere 1'i gösterecek şekilde güncellendi; bu belge §2, §3.2, §4, §6, §7 ve §10'da güncellendi.
- **Kapanış:** C0 (`ORCHESTRATION_PLAN.md`, bu günlük ve `NEXT_PROMPT.md`'yi taşıyan commit) işlendi; `git log --diff-filter=A -- ORCHESTRATION_PLAN.md` ile bulunur. Sonraki pencere: Pencere 1 — IMPL-96 uygulaması (`ORCHESTRATION_PLAN.md` §5).
- **Takip commit'i (inceleme sonrası):** `NEXT_PROMPT.md` §4.1 ve §8 plana hizalandı (`:101` için yalnız düzeltme notu; "yalnız ekleme" kuralının tek istisnası `Updated At`; R-identity-check atfı). İnceleme görevleri `R1`/`R2` → `REV`/`SEC`, Ek A olguları `R1`/`A1` → `REL`/`TRAP` oldu (risk ve self-test kimlikleriyle çakışıyordu). Commit: `Window 0 follow-up: align handoff with plan, rename review IDs`.
- **Sonraki giriş için şablon:** `YYYY-MM-DD — koşu kimliği — yapılan — ölçüm — bekleyen kararlar`. Aynı anda §2, §3.2 ve §4 de güncellenir.

**2026-11-13: Pencere 1 (omp, üçüncü pencere).** Kapsam: `ORCHESTRATION_PLAN.md` Pencere 1 (IMPL-96 uygulaması). Bu pencerenin kaydı ledger'daki `IMPL-96` satırıdır; bu girdi onun özetidir.

- **Açılış ölçümleri (salt-okur, 17:22–17:25 UTC):**
  - Git: dal `integrate/impl-96`, uç `c2abd46`, ağaç temiz; `main` 63 commit (`7fa0a51`); `git ls-remote origin` → `main` = `587e3b5`; 350 izlenen dosya; etiket yok.
  - GitHub: silinecek üç depo da hâlâ duruyor (`gh api` 200; görünürlük değişmedi). Silme yapılmadı.
  - Telefon (`dc27e5d0`, `-s` ile): ROM, kernel, root, HAL ve sensör md5'leri, AON sembolik bağı, 13 modül, uygulama sürümleri ve 13 kamera aygıtı probe ile aynı. `smoke.sh` yalnız stdout'a çalıştı; COMPARABLE bloğu 15:21Z baseline'ıyla bayt bayt aynı, dosya yazılmadı.
  - Yedekler: bundle (77.094 B, sha256 aynı, `git bundle verify` OK) ve iki ayna (`git fsck` 0) doğrulandı.
  - Doğrulayıcı ve self-test taban değerde.
- **Kullanıcı onayı ("onay"):** Ek A düzeltmeleri C1'e girer (ayrı kontrat commit'i yok); dal `integrate/impl-96`'da kalır; kapsam dışı bulgular yalnız plan §10'a yazılır; REV ∥ SEC C1 adayı diff'i inceler.
- **Kontrat (Ek A):** G2, G8, G12, D3, D4, D5, D10, D11, TRAP, M1 ve E7 ölçüme göre düzeltildi; K3, AUD11 ve OPN satırları eklendi; plan §10'a yeni kapsam dışı bulgular yazıldı. Planda bu pencerede güncellenen bölümler: §1, §3 (Adlandırma), §5.1 (W3 `:143` ve W4 `:61` hedefleri), §6 (W5, SEC ve sıra), §10, Ek A.2, A.4 notu ve A.5 (sıra). M1: `setmode.sh`'in andığı `vendor.camera-provider-2-7-ext` probe'da yok, yerinde `-2-7-ext-uvc` var [ÇIKARIM: probe'un filtresi kayıtlı değil]. E7: snapshot adlarındaki saat güvenilir değil; başlıktaki `taken` (UTC) esastır. TRAP: danışman notu üzerine "önce truncate" ifadesi silinmedi, kesinleştirildi (`cat … >` yönlendirmesi özgün dosyayı yazmadan önce boşaltır; yedek ve boş dosya kontrolü yok).
- **Uygulama:** W1 ve W2 taslakları (`local://`, bu pencerede tüketildi) ledger'a `edit` ile uygulandı: 644 → 653 satır; 21 satır yalnız ekleme (difflib), 9 yeni satır; CRLF ve boru sayıları korundu; tek istisna beş §4 satırının `Updated At` hücresi. Taslaklardaki plan içi kimlikler (G, D, V, E, M1 vb.) ledger metnine girmedi. W3 `README.md` 12 yer, W4 `UNTRACKED-BY-DESIGN.md` 8 yer, T3 iki `-o` satırı; `NEXT_PROMPT.md` Pencere 2 için yeniden yazıldı. Keşif scout'larının ikisinde kabuk yoktu ve durduruldu; işlerini orkestratör betikle yaptı.
- **Geçitler (entegrasyondan sonra):** doğrulayıcı `--mode all` taban değerde (`error_count=0`, `warning_count=1`, `subplan_count=42`, `secret_findings=0`); `--mode step4 --strict` yalnız bilinen `strict_warning`; `SELF-TEST: PASS` (VAL-BUILD2 sha256 aynı). Değişen dosyalar yalnız C1 listesindekiler.
- **İnceleme (REV ∥ SEC, C1 adayı):** ilk deneme sağlayıcı hız sınırına (HTTP 429) takıldı; iki görev aynı metinle ≈21:28 UTC'de yeniden çalıştı. SEC: bulgu yok (sır, IP ya da sunucu adresi, e-posta, başka cihaz serisi: 0; 15 haneli sayı ve Luhn adayı: 0; probe satır 42, 190, 191 yalnız numarayla anılıyor). REV: üç P1, iki P2, on P3; hepsi C1'den önce uygulandı. P1: ledger IMPL-96 sonuç hücresi "remote değişmedi" diyordu (depo taşıma bir remote değişikliğidir; `587e3b5`'ten sonrası push edilmedi); bu girdinin kapanış satırı C1'i "kullanıcı onayıyla" diye anlatıyordu; `UNTRACKED-BY-DESIGN.md` beş arşiv için işlemeyen bir yeniden derleme yolu yazıyordu (geçmiş v2.1'de başlar; `build-release.py` yalnız `ishtar-cam-modes`'u paketler; `dist/` v2.1 kökteki arşivden farklı). P2: ledger (8)'de taslak üst metni ve satır numarası atfı; Pencere 2'de SEC C2'den önce çalıştığı için W5/W6'yı görmüyordu (artık `git diff HEAD`'i de inceler; kimlik kontrolü push'tan hemen önce). P3: `DEC-07`/`DEC-08` konusuz notlarının ifadesi; hal0 akış satırlarının smoke'ta yeniden okunduğu; plan §10 satır numaraları (C1 ağacına); `K3`/`K4` adlandırması; güncellenen plan bölümlerinin tek listesi; bu girdide bekleyen kararlar; README'de iki sözleşme belgesinin adı; NEXT_PROMPT'ta push, smoke ve snapshot saati ifadeleri.
- **Kapanış öncesi salt-okur kontrol (21:31:25Z):** `smoke.sh` yalnız stdout'a; COMPARABLE bloğu 15:21:35Z baseline'ıyla aynı; dosya yazılmadı. Bilgisayara yalnız `dc27e5d0` bağlıydı.
- **Bekleyen:** push kararı (Pencere 2; C2 ve `main` fast-forward'ından sonra); K9 (Pencere 3); `DEC-30` silme ölçümü (silmeyi kullanıcı yapar); planlama koşusu 21 (Faz 7/8 emekliliği, K7 = (a) planı) ve 12. denetim.
- **Kapanış:** C1 `IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline`. Kullanıcı uyumadan önce pencereyi soru sormadan bitirme talimatı verdi; diff commit'ten önce gösterilmedi ve C1 bu talimatla atıldı (plan §0 adım 4'teki "onayla commit"ten sapma; Pencere 2 açılışında C1 diff'i kullanıcıya gösterilir). Push yok; `main` ileri sarılmadı. Sonraki pencere: Pencere 2 — Kapanış ve yayın (`ORCHESTRATION_PLAN.md` §6).

**2026-11-14: Pencere 2 · O0+O1 (omp, dördüncü pencere).** Kapsam: `ORCHESTRATION_PLAN.md` Pencere 2'nin keşif ve plan aşamaları. Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı (Pencere 2 ledger'a yazmaz).

- **Açılış ölçümleri (salt-okur):**
  - Git: dal `integrate/impl-96`, uç C1, ağaç temiz; dal 69, `main` 63 (`7fa0a51`), `origin/main` 62 (`587e3b5`) commit; `git ls-remote origin` yalnız `HEAD` ve `refs/heads/main` = `587e3b5` gösteriyor; etiket yok; 350 izlenen dosya.
  - GitHub (`gh api`, 07:23:21Z): silinecek üç depo da hâlâ 200 (`ahmetxa/ishtar` özel, ikisi açık); `ishtar_cam_modes` özel.
  - Ledger (yalnız betikle): 653 satır, hepsi CRLF, NUL 0; IMPL-96 `:525`; `DEC-27`…`DEC-32` `:605`–`:610`; `DEC-33` yok.
  - Kimlik kontrolü tabanı (plan Ek A.5 betiği; `git log --all -p` ve 350 dosya): değer taşıyan 6 anahtar satırının hepsi `<redacted>`; Luhn adayı 0; anahtarı yalnız düzyazıda anan 9 satır. Geçti.
  - Push aralığı ön taraması (7 commit'in bütün ara hâlleri, 3.148 eklenen satır): token, özel anahtar, parola ataması, sunucu adresi, MAC adresi ya da Luhn adayı yok; IPv4 biçimli iki eşleşme sürüm dizgisi; probe öteki telefonun serisini kaydetmemiş, emülatör yalnız adb port adıyla geçiyor; commit e-postası daha önce push edilmiş commit'lerdekiyle aynı.
  - Telefona komut gönderilmedi (Pencere 2 cihaza dokunmaz); cihaz olguları bu fazda teyit edilmedi.
- **Keşif (`O0`):** üç scout (`W5AnchorsTop`, `W5AnchorsBottom`, `W6Window3Inputs`). Plandaki yedi W5 çapası bulundu; her biri dosyada bir kez geçiyor. W5'in kapsamı plan satırından geniş çıktı: §1–§4'te 13 "Pencere 1'de yazılacak" ifadesi; C1'in ledger'a eklediği 9 satır yüzünden `ledger:N` atıflarında +1/+3/+9 kayma; `docs/pre-rental-plan.md` ve `docs/build-environment.md` atıflarının 13'ü +8 kaymış; README ve UNTRACKED atıfları C1 öncesine göre numaralı; "344" üç yerde. Pencere 3 için: Step 1 handoff dosyası yok; plan §7'de AUDIT-FIX eşlemesi yanlış ve seçenek (ii) emeklilikle çelişiyor; doğrulayıcı tuzakları. Envanter plan §6.2'de, olgular Ek A.6'da.
- **Plan (`O1`):** görev tablosu ve beş karar sunuldu; kullanıcı "onaylıyorum" dedi (varsayılanlar 1a–5a; plan §6.1). Danışman notu üzerine entegrasyon iki adıma bölündü (I2a `O4`'te, I2b `O5`'te). C1'in `git show --stat` çıktısı gösterildi; C1 diff'ini REV-3 inceleyecek.
- **Kullanıcı kararı (döngü):** her aşama ayrı oturumda (`O0`+`O1` birlikte; `O2`, `O3`, `O4`, `O5` ayrı); aşama beklenmedik durum olmadan biterse `NEXT_PROMPT.md` sonraki aşama için kendiliğinden yazılır ve yerel commit onay sorulmadan atılır; `main` fast-forward'ı ve push her zaman sorulur; beklenmedik durumda kullanıcıya sade bir dille sorulur (plan §0). Bu yüzden W6 (Pencere 3 devri) `O5`'e taşındı.
- **Değişen dosyalar:** `ORCHESTRATION_PLAN.md` (§0, §1, §2, §3, §6, Ek A.5, A.6), `NEXT_PROMPT.md` (`2 · O2` için), bu girdi.
- **Bekleyen:** Pencere 2 · `O2`–`O5` (plan §6.3); push kararı (`O5`); K9 (Pencere 3); depo silme (kullanıcı; üçü de 2026-11-14'te duruyor).
- **Kapanış:** `Window 2 O0-O1: approved plan, discovery facts, stage-per-session loop` (yerel commit; döngü kuralıyla onay sorulmadan). Push yok; `main` ileri sarılmadı. Sonraki oturum: Pencere 2 · O2 — Kontrat (`ORCHESTRATION_PLAN.md` §6.3).

**2026-11-14: Pencere 2 · O2 (omp, beşinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` Pencere 2'nin kontrat aşaması (K0). Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı (Pencere 2 ledger'a yazmaz).

- **Açılış ölçümleri (salt-okur):**
  - Git: dal `integrate/impl-96`, uç `2 · O0+O1` commit'i, ağaç temiz; dal 70, `main` 63 (`7fa0a51`), `origin/main` 62 (`587e3b5`) commit; push edilmemiş 8 commit; `git ls-remote origin` yalnız `HEAD` ve `refs/heads/main` = `587e3b5`; etiket yok; 350 izlenen dosya. Bu günlüğün §1–§10'u C1'den beri değişmemiş: envanterin satır numaraları geçerli.
  - GitHub (`gh api`, 10:03:48Z): silinecek üç depo da hâlâ 200 (`ahmetxa/ishtar` özel, ikisi açık); `ishtar_cam_modes` özel.
  - Telefona komut gönderilmedi; cihaz olguları bu aşamada teyit edilmedi.
- **Envanter doğrulaması (K0 adım 1):** `py -3` betiği 84 maddenin bütün alıntılarını bu dosyada saydı: hepsi bulundu ve verilen satırlarda. Bir alıntı eksik yazılmıştı; sekiz alıntı başka satırlarda da geçiyordu ve çapaları genişletildi. Hedeflerdeki ledger, `PRP`, `docs/build-environment.md`, README ve UNTRACKED satırları içerikle doğrulandı. C1'in ledger notları (`:100`, `:101`, `:528`, `:530`, `:532`, `:552`–`:558`, §8 konusuz notları) betikle okundu. Not: `:528` remote'u ve commit sayılarını yazıyor, dosya sayısını yazmıyor. İki salt-okur scout (`InventoryRowsA`, `InventoryRowsB`) her maddeyi Ek A'ya karşı okudu. Bir madde çıkarıldı (UNTRACKED sanılan `:61`/`:63` atıfları başka dosyaların satırlarıydı). Eski ve yeni tablo betikle karşılaştırıldı: 47 maddenin hedefi düzeltildi (cümlenin doğru kısmı korunur, Ek A'da olmayan iddia yazılmaz, aynı satırdaki ikinci bayatlık eklenir); 1 maddenin yalnız alıntısı genişletildi; 12 maddenin yalnız kaynak sütunu tamamlandı; 23 madde aynı kaldı.
- **Kullanıcı kararı ("ekle"):** envanter dışında kalmış ama karar 1a'nın sınıfına giren 15 bayat yer W5'in listesine eklendi: üç "commit edilmedi", üç kayan ledger atfı, iki "son sürüm C0'da", "izlenmiyor", iki "seçilirse" ve dört başka yer (`:5`, `:785`, `:796`, `:825`). Ayrıca `:59`'daki tarih etiketi var olan bir maddeye eklendi. Envanter 97 madde oldu (plan §6.1 karar 8).
- **Kontrat (K0 adım 2–5):**
  - Plan §6.5: envanter doğrulamasının sonucu, W5 yazım kuralları ve `O3` alt ajan ortak bağlamı. Kurallar: tarihli not biçimi ` *(YYYY-AA-GG notu: …)*`; §8'de `**Çözüldü (…):**`; §3.5'e yeni gruplar; §4'e `DEC-27`…`DEC-32`; atıf kuralları; zamanla değişen olgular `O3` açılışında orkestratörce ölçülür.
  - Plan §7: Pencere 3'ün açılış soruları 5–8 (Faz 8'in emekliliği; `Faz6.2`'nin VAL-BUILD bağı; Step 1'in yazamadığı Hetzner satırlarının sahibi; Step 1 ve sınırlı Step 2'nin aynı oturumda yapılması). Ayrıca düzeltilmiş `AUDIT-FIX-41`/`-42`/`-57` eşlemesi, kaynağında okunan doğrulayıcı tuzakları ve ClaudeQB süreci; push sonrası günlük güncellemesi Pencere 3 açılışına bağlandı.
  - Plan §10: Hetzner ifadesinin yedi canlı yeri; §10'daki ledger atıflarının güncel karşılıkları.
  - Plan Ek A.6: altı yeni olgu satırı (açılış ölçümü, depo ölçümü, `7fa0a51`'in içeriği, commit konuları, ledger çapaları, README/UNTRACKED satır eşlemesi).
- **Doğrulama:** plan ve `NEXT_PROMPT.md` LF, CR 0, NUL 0; iki dosyanın bütün tablolarında boru sayısı sabit. Envanterin 97 maddesinde her alıntı yalnız kendi satırlarında geçiyor (betik). Kimlik taraması (plan Ek A.5; `git log --all -p` ve 350 dosya): `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=13` → geçti. Düzyazı sayısının 9'dan 13'e çıkması, anahtar adını anan yeni plan satırlarından; karar 5a gereği hata değil. Doğrulayıcı ve self-test bu aşamada çalıştırılmadı (geçitler `2 · O4`'te).
- **Değişen dosyalar:** `ORCHESTRATION_PLAN.md` (§1, §3 Adlandırma, §6 durum satırı, §6.1, §6.2, §6.5 yeni, §7, §10, Ek A.6), `NEXT_PROMPT.md` (`2 · O3` için), bu girdi. Ledger, `Planner-docs/`, `docs/` ve bu dosyanın §1–§10'u dokunulmadı.
- **Bekleyen:** Pencere 2 · `O3`–`O5` (plan §6.3); push kararı (`O5`); K9 ve öteki açılış soruları (Pencere 3); depo silme (kullanıcı; üçü de 2026-11-14'te duruyor).
- **Kapanış:** `Window 2 O2: contract for the project log sweep and the run 21 handoff` (yerel commit; döngü kuralıyla onay sorulmadan). Push yok; `main` ileri sarılmadı. Sonraki oturum: Pencere 2 · O3 — Paralel uygulama (`ORCHESTRATION_PLAN.md` §6.3–§6.5).

**2026-11-14: Pencere 2 · O3 (omp, altıncı pencere).** Kapsam: `ORCHESTRATION_PLAN.md` Pencere 2'nin paralel uygulama aşaması (W5 ∥ SEC-A1 ∥ SEC-A2 ∥ SEC-A3 ∥ REV-3). Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı (Pencere 2 ledger'a yazmaz).

- **Açılış ölçümleri (salt-okur):**
  - Git: dal `integrate/impl-96`, uç `2 · O2` commit'i, ağaç temiz; dal 71, `main` 63 (`7fa0a51`), `origin/main` 62 (`587e3b5`) commit; push edilmemiş 9 commit; `git ls-remote origin` yalnız `HEAD` ve `refs/heads/main` = `587e3b5`; etiket yok; 350 izlenen dosya. Bu günlüğün 1–1012. satırları C1'den beri değişmemişti: envanterin satır numaraları geçerliydi.
  - GitHub (`gh api`, 13:45:22Z): silinecek üç depo da hâlâ 200 (`ahmetxa/ishtar` özel, ikisi açık); `ishtar_cam_modes` özel.
  - Değerler W5 başlamadan önce plan Ek A.6'ya yazıldı. Telefona komut gönderilmedi; cihaz olguları bu aşamada teyit edilmedi.
- **Girdiler:** SEC-A1, SEC-A2, SEC-A3 ve REV-3 girdileri plan §6.4'teki komutlarla üretildi (69 KB, 321 KB, 654 KB ve 11 KB, 136 KB); SEC-A3'e ayrıca push edilmiş `587e3b5`'in üstverisi verildi.
- **Güvenlik incelemeleri (salt-okur; push aralığının 9 commit'i, ara hâller dahil):**
  - SEC-A1 (`snapshots/`, `docs/`, README, UNTRACKED) ve SEC-A2 (`Planner-docs/`): bulgu yok. Probe'un üç kimlik satırı `<redacted>`; Luhn adayı, başka cihaz serisi, sunucu adresi, MAC adresi ya da sır yok; IPv4 biçimli tek eşleşme bir sürüm dizgisi.
  - SEC-A3 (bu günlük, `NEXT_PROMPT.md`, plan ve commit üstverisi): P0–P2 yok; commit yazarı ve işleyeni push edilmiş `587e3b5`'tekiyle aynı. Tek P3: belgelerdeki yerel yollar Windows kullanıcı adını içeriyor; depo özel, aynı yollar push edilmiş ağaçta da var ve komutlar için gerekli → orkestratör kabul etti, işlem yok (plan §10). Ayrıca plan Ek A.5 betiğinin bölünmüş 15 haneli sayıyı saymadığı gözlemi (plan §10).
- **İçerik incelemesi (REV-3; C1 diff'inin ledger, README, UNTRACKED ve `docs/` kısmı):** P0/P1 yok; W1–W4 ve T3 hedefleri karşılanmış, ledger biçimi (CRLF, boru sayıları, yalnız ekleme) doğru. P2: `UNTRACKED-BY-DESIGN.md:36` Faz 1.1'deki izlenen dosya sayısını 84 diyordu; ledger (`:66`, `:113`) ve `git ls-tree -r --name-only ff6934e` 86 veriyor → düzeltici task satırı bu aşamada düzeltti (plan §6.1 karar 4; plan §5.1'deki W4 hedefi yanlıştı). P3: ledger `DEC-29`…`DEC-32` satırlarının "Raised by" hücresi → plan §10 (koşu 21).
- **W5 (bu günlüğün §1–§10'u):**
  - İlk deneme (tek `task` ajanı, 97 madde): ajanın 100K bağlamı taştı; ajan hedef satırları okumadan toplu bir düzenleme yaptı, Ek A'da olmayan içerik yazdı ve sözleşme dışı olarak git'i salt-okur çalıştırdı; sonra kendisi durup bildirdi. Orkestratör dosyayı `git checkout -- PROJECT_LOG.md` ile geri aldı. `task` aracında ajan başına model seçimi kapalı (`task.perCallModel: off`).
  - İkinci deneme parçalarla yürüdü. P1 (başlık, §1–§2.5; 24 madde) bir `task` ajanıyla uygulandı. P5'i deneyen `task` ajanının bağlamı düzenlemeye başlamadan doldu ve ajan durduruldu (dosyaya dokunmadı). Kalan dört parça (P2 §3, P3 §4–§5, P4 §6–§7 ve §9–§10, P5 §8) geniş bağlamlı salt-okur ajanlara taslak olarak yazdırıldı. Orkestratör her taslağı betikle ayrıştırdı (yalnız hedef satırlar, boru sayıları, eklenen plan kimliği yok), kelime farkını okudu ve taslağı `edit` aracıyla uyguladı; uygulanan metin taslakla birebir aynı çıktı.
  - P1'deki dokuz kusur P2 taslağıyla düzeltildi: günlüğe yazılmış plan olgu kimlikleri, belirsiz "§7" atfı, eksik commit başlıkları, eksik "(4). maddesi" ve atıf yeri. Eklemeler yüzünden kayan iki kendi satır atfı (§2.1 `:60` ve `:67` → §8 `:802`, `:803`) yeniden numaralandı.
  - Sonuç: envanterin 97 maddesi karşılandı; 96'sı uygulandı, §2.6 maddesi gereği gibi dokunulmadı. §8'deki ledger atıf maddesinde dört satırın atfı `:524`'ün altında kaldığı için değişmedi. 162 satır eklendi, 143 satır çıktı; 19 satır yeni: §3.5'e iki grup (2026-11-13'te 6, 2026-11-14'te 3 commit) ve §4'e `DEC-27`…`DEC-32`. Başlık metni yalnız §2'de (tarih) ve §4'te (`DEC-32`) değişti. Ajanların envanter dışı gözlemleri (15 yer) dokunulmadı; plan §10'da.
- **Doğrulama:** `git diff` yalnız `PROJECT_LOG.md`, `ORCHESTRATION_PLAN.md`, `NEXT_PROMPT.md` ve `UNTRACKED-BY-DESIGN.md`'yi gösteriyor. Bu günlüğün §2.6'sı ve (bu girdiye kadar) §11'i değişmedi; değişen satırların hepsi envanter satırlarında; günlük metnine plan olgu kimliği girmedi (betik). Dört dosya LF, CR 0, NUL 0; bütün tablolarda boru sayısı sabit. Kimlik taraması (plan Ek A.5; `git log --all -p` ve 350 dosya): `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=15` → geçti. Artış iki satırdan: §4'teki yeni `DEC-31` satırı (ağaç) ve `2 · O2` commit'i (geçmiş); karar 5a gereği hata değil. Doğrulayıcı ve self-test bu aşamada çalıştırılmadı (geçitler `2 · O4`'te).
- **Çelişkiler (dosya kazandı):** kullanıcının genel orkestrasyon şablonu (tek oturumda Faz 0–5, yeni branch, `isolated`, `outputSchema`) bu aşamada dosyalara göre uygulanmadı. `NEXT_PROMPT.md`'nin "`UNTRACKED-BY-DESIGN.md` dokunulmamış" kabul cümlesi plan §6.1 karar 4 ile çelişiyordu; plan uygulandı (plan §10).
- **Değişen dosyalar:** `PROJECT_LOG.md` (§1–§10, W5; bu girdi), `UNTRACKED-BY-DESIGN.md` (satır 36, REV-3 düzeltmesi), `ORCHESTRATION_PLAN.md` (§1, §6 durum satırı, §7'de push ve silme sonrası güncellenecek yerler, §10, Ek A.6'ya iki satır: bu aşamanın açılış ölçümü ve Faz 1.1 dosya sayısı), `NEXT_PROMPT.md` (`2 · O4` için). Ledger, `Planner-docs/`, `docs/` ve README dokunulmadı.
- **Bekleyen:** Pencere 2 · `O4`–`O5` (plan §6.3); push kararı (`O5`); K9 ve öteki açılış soruları (Pencere 3); depo silme (kullanıcı; üçü de 2026-11-14'te duruyor).
- **Kapanış:** `Window 2 O3: project log sweep and pre-push reviews` (yerel commit; döngü kuralıyla onay sorulmadan). Push yok; `main` ileri sarılmadı. Sonraki oturum: Pencere 2 · O4 — Entegrasyon ve geçitler (`ORCHESTRATION_PLAN.md` §6.3).

**2026-11-14: Pencere 2 · O4 (omp, yedinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` Pencere 2'nin entegrasyon ve geçitler aşaması (I2a → GATE). Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı (Pencere 2 ledger'a yazmaz).

- **Açılış ölçümleri (salt-okur):**
  - Git: dal `integrate/impl-96`, uç `2 · O3` commit'i, ağaç temiz; dal 72, `main` 63 (`7fa0a51`), `origin/main` 62 (`587e3b5`) commit; push edilmemiş 10 commit; `git ls-remote origin` yalnız `HEAD` ve `refs/heads/main` = `587e3b5`; etiket yok; 350 izlenen dosya.
  - GitHub (`gh api`, 19:34:57Z): silinecek üç depo da hâlâ 200 (`ahmetxa/ishtar` özel, ikisi açık); `ishtar_cam_modes` özel.
  - Değerler plan Ek A.6'ya yazıldı. Telefona komut gönderilmedi; cihaz olguları bu aşamada teyit edilmedi.
- **I2a, sahiplik kontrolü (betik):** `2 · O2` ve `2 · O3` kapanış commit'leri arasında dört dosya değişti: bu günlük, plan, `NEXT_PROMPT.md` ve `UNTRACKED-BY-DESIGN.md` (yalnız satır 36, REV-3 düzeltmesi; plan §6.1 karar 4). Bu günlükte §11 dışındaki her değişiklik plan §6.2 envanterinin satırlarında (97 madde; belge başındaki `:3` ve `:5` dahil); §11'e yalnız sona `2 · O3` girdisi eklenmiş; §2.6 değişmemiş. W5 dışı değişiklik yok.
- **I2a, §2.6:** başlık dahil bu aşamaya göre yeniden yazıldı: Pencere 2'nin durumu, `2 · O3` sonuçları, bulguların yönü (plan §10), sahiplik kontrolü, dal ve depo ölçümü, açık kararlar. Bölüm eskisi gibi 13 satır; sonraki satırların numarası değişmedi, plan §7 ve §10'daki `2 · O3` kapanışına göre numaralar geçerli.
- **GATE (19:42Z, plan §3):**
  - Doğrulayıcı `--mode all`: `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`; çıkış 0.
  - `--mode step4 --strict`: yalnız bilinen `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9` hatası (taban değer, regresyon değil); `p0_findings=0`, `p1_findings=0`; çıkış 1.
  - `py -3 scripts/build-release.py --self-test`: `SELF-TEST: PASS`; iki derlemenin sha256'sı da `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0`; A1, A2, A3 PASS. Ağaçta yeni dosya kalmadı.
  - Bayt ve boru: değişen dosyalar LF, CR 0, NUL 0; bütün tablolarda boru sayısı başlıkla aynı.
  - Sonuç: üç geçit de taban değerde.
- **Bulgular (plan §10):** `git log --grep 'Window 2 O2'` iki commit döndürüyor, çünkü `2 · O0+O1` commit'inin gövdesi O2 aşamasını adıyla anıyor; `2 · O5`'teki SEC-B girdisi için konu satırına bağlı arama kullanılır. Bu aşamanın devri sahiplik kontrolünde yalnız üç dosya bekliyordu; plan dördüncüsünü (REV-3 düzeltmesi) kaydetmişti: plan kazandı.
- **Çelişkiler (dosya kazandı):** kullanıcının genel orkestrasyon şablonu (tek oturumda Faz 0–5, yeni branch, `isolated`, `outputSchema`, alt ajanlar) bu aşamada dosyalara göre uygulanmadı: aşama orkestratöründür, alt ajan yok (plan §6.3).
- **Kimlik taraması** (plan Ek A.5; `git log --all -p` ve 350 dosya): `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=16` → geçti. Artış (15 → 16) `2 · O3` commit'inden: §4'teki `DEC-31` satırı artık geçmişte de sayılıyor (9 geçmişte, 7 ağaçta); karar 5a gereği hata değil.
- **Değişen dosyalar:** `PROJECT_LOG.md` (§2.6, bu girdi), `ORCHESTRATION_PLAN.md` (§1, §6 durum satırı, §10, Ek A.6'ya bu aşamanın açılış ölçümü), `NEXT_PROMPT.md` (`2 · O5` için). Ledger, `Planner-docs/`, `docs/`, README, UNTRACKED ve bu günlüğün §2.6 dışındaki §1–§10'u dokunulmadı.
- **Bekleyen:** Pencere 2 · `O5` (plan §6.3–§6.4); push kararı (`O5`); K9 ve öteki açılış soruları (Pencere 3); depo silme (kullanıcı; üçü de 2026-11-14'te duruyor).
- **Kapanış:** `Window 2 O4: integration and gates` (yerel commit; döngü kuralıyla onay sorulmadan). Ardından kullanıcı onayıyla takip commit'i `Window 2 O4 follow-up: anchor the O2 commit lookups`: plan §1 `:45` ve §6.4 `:341`'deki `2 · O2` aramaları konu satırına bağlandı (plan §10), `NEXT_PROMPT.md`'nin dal durumu güncellendi. Push yok; `main` ileri sarılmadı. Sonraki oturum: Pencere 2 · O5 — Son inceleme ve kapanış (`ORCHESTRATION_PLAN.md` §6.3–§6.4).

**2026-11-14: Pencere 2 · O5 (omp, sekizinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` Pencere 2'nin son inceleme ve kapanış aşaması (W6 ∥ REV-1 → REV-2 ∥ SEC-B → FIX → I2b → kapanış commit'i; ardından ayrı onaylarla FF, RID, push ve LSR). Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı (Pencere 2 ledger'a yazmaz).

- **Açılış ölçümleri (salt-okur):**
  - Git: dal `integrate/impl-96`, uç `2 · O4` takip commit'i, ağaç temiz; dal 74, `main` 63 (`7fa0a51`), `origin/main` 62 (`587e3b5`) commit; push edilmemiş 12 commit; `git ls-remote origin` yalnız `HEAD` ve `refs/heads/main` = `587e3b5`; etiket yok; 350 izlenen dosya. `git log --all --grep '^Window 2:'` boş döndü: kapanış commit'inin konu satırı bu aramada tek kalır.
  - GitHub (`gh api`, 20:07:24Z): silinecek üç depo da hâlâ 200 (`ahmetxa/ishtar` özel, ikisi açık); `ishtar_cam_modes` özel.
  - Değerler ajanlar başlamadan plan Ek A.6'ya yazıldı. Telefona komut gönderilmedi; cihaz olguları bu aşamada teyit edilmedi.
- **Girdiler** (plan §6.4'teki komutlarla, `local://` altında): W6 için plan alıntıları (iki parça, 40 KB ve 40 KB); REV-1 için `2 · O2` kapanışından bu yana günlük farkı (127 KB) ve plan alıntıları (80 KB); REV-2 için C1'den çalışma ağacına plan farkı (103 KB); SEC-B için `2 · O2` kapanışından sonraki `git log -p` (iki parça: 135 KB ve 154 KB), commit üstverisi (6 KB) ve `git diff HEAD` (144 KB).
- **W6 (`NEXT_PROMPT.md` → Pencere 3 · O0+O1):**
  - Bağlam sınırı yüzünden iki parça. A (`task`; başlık ve §0–§3) yaklaşık 67 KB girdiyle 100K bağlama ulaştı, bağlamını sıkıştırdı ve `partial` döndü: §3'te iki madde yanlıştı (kimlik maddesinde bozuk Türkçe karakterler ve önceki ölçümler için yanlış bir "doğrulanamadı" cümlesi; plan maddesinde ledger durum dağılımı ve doğrulayıcı değerleri düşmüştü).
  - B (§4–§11) geniş bağlamlı salt-okur bir ajana (`reviewer`) taslak olarak yazdırıldı; taslak A'nın iki maddesinin düzeltmesini de taşıdı. Orkestratör taslağı `edit` ile uyguladı ve betikle taslakla birebir karşılaştırdı (üç küçük uyum düzeltmesiyle); taslağın önerisiyle §1 dosya tablosuna `Autopsy.md`, §2 okuma listesine `workflow-quality.md` eklendi.
  - Sonuç: sekiz açılış sorusu başta; push ve depo durumu Pencere 3 açılışında ölçülür; Step 1.5 (Autopsy) ve doğrulayıcının `autopsy` kipi işlendi (REV-2). Kimlik değeri ve kapanış commit'inin hash'i yok; bu günlüğe yalnız bölümle atıf.
- **REV-1 (bu günlük; iki reviewer, §1–§3 ve §4–§11):** P0/P1 yok. Parça A 2 P2 ve 6 P3, parça B 7 P2 ve 11 P3 buldu; W5'in envanter dışı 15 gözleminin hepsine hüküm verildi (14'ü doğrulandı; `:292` bugün doğru, depo silinince güncellenir). Düzeltici task (FIX) bulguları §1–§10'da 30 satır içi düzeltmeyle uyguladı: aynı gün ölçümlerinin etiketleri (`2 · O3` açılışı), §2.1 ve §7'deki bayat hücreler, §5.1 durum hücresi, §8'deki çözüm işaretleri, §10 kimlik satırları ve HAL koruması cümlesi. Satır sayısı ve boru sayıları değişmedi (betik). `:679`'a not eklenmedi (`2 · O2`'de tarihsel sayılmıştı).
- **REV-2, plan parçası** (C1'den bu yana plan farkı; ClaudeQB ve doğrulayıcıya karşı): P0/P1 yok; 1 P2 ve 7 P3. §7'deki 19 doğrulayıcı satır atfının ve dosya atıflarının hepsi kaynakla eşleşti. P2: §7, ClaudeQB'nin Step 1'den sonra kendiliğinden çalıştırdığı Step 1.5'i (Autopsy) ve doğrulayıcının `autopsy` kipini anmıyordu. Orkestratör sekiz bulguyu kaynaktan doğrulayıp plana işledi (§3 Adlandırma; §7 sorular 7–8, "Açılışta ayrıca", Step 2 biçimi, doğrulayıcı tuzakları, ClaudeQB süreci; §8; Ek A.6 başlığı).
- **REV-2, `NEXT_PROMPT.md` parçası:** P0/P1 yok; 2 P2 (`--mode autopsy` geçidi Step 1.5'e bağlı değildi; bir bölüm atfı yanlıştı) ve 9 P3 (ör. Step 1.5 yönergesi okuma listesinde yoktu; görev kimliklerinde `FF` eksikti; silinecek depolar komutun yanında adlandırılmamıştı). Düzeltici task (FIX) hepsini 14 satır içi düzeltmeyle uyguladı (betikle doğrulandı); plana düşen üç uzantıyı (`autopsy` kipinin Comprehension'ı da denetlemesi, `Autopsy-Planner.md`, alt plan dosya adının `FazN.M-` öneki) orkestratör §7'ye işledi.
- **SEC-B (iki security-reviewer):** `2 · O2` kapanışından sonraki üç commit (ara hâller dahil), commit üstverisi ve kapanış commit'ine giren `git diff HEAD`: bulgu yok. Sır, değer taşıyan kimlik satırı, Luhn adayı (bitişik ya da bölünmüş), `dc27e5d0` dışında seri, IP, MAC, sunucu adresi ya da yeni bir kişisel veri türü yok; üç commit'in yazar ve işleyen e-postası push edilmiş `587e3b5`'tekiyle aynı. Not (bulgu değil): push edilmiş `587e3b5`'in mesajında `Co-Authored-By` satırının yanında bir oturum adresi var; aralığın dışında.
- **GATE (FIX'ten sonra, 20:56:21Z, plan §3):**
  - Doğrulayıcı `--mode all`: `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`; çıkış 0.
  - `--mode step4 --strict`: yalnız bilinen `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9` hatası (taban değer, regresyon değil); `p0_findings=0`, `p1_findings=0`; çıkış 1.
  - `py -3 scripts/build-release.py --self-test`: `SELF-TEST: PASS`; iki derlemenin sha256'sı da `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0`; A1, A2, A3 PASS. Ağaçta yeni dosya kalmadı.
  - Sonuç: üç geçit de taban değerde.
- **I2b (kapanış commit'inden hemen önce):** sonuç cümleleri bu günlüğün §2.6'sına ve bu girdiye, `NEXT_PROMPT.md`'deki `2 · O5` maddesine ve beklenen değerler tablosuna, plan §1 satırlarına, §6 durum satırına ve §10'a yazıldı. Depolar yeniden ölçüldü (`gh api`, 21:11:12Z): üçü de hâlâ 200; `git ls-remote origin` değişmedi. `NEXT_PROMPT.md` düzeltmesinden sonra geçitler bir kez daha çalıştı (21:19:55Z): üçü de aynı taban değerde. Değişen üç dosya LF, CR 0, NUL 0; bütün tablolarda boru sayısı başlıkla aynı (betik). Kimlik taraması (plan Ek A.5; `git log --all -p` ve 350 dosya): `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=16` → geçti.
- **Çelişkiler (dosya kazandı):** kullanıcının genel orkestrasyon şablonu (Faz 0–5, plan onayında durma, yeni branch, `isolated`, `outputSchema`, `librarian`, `designer`) dosyalara göre uygulandı: bu oturum şablonun Faz 5'i ve kapanışıdır; plan `2 · O0+O1`'de onaylanmıştı.
- **Değişen dosyalar:** `NEXT_PROMPT.md` (Pencere 3 · O0+O1 için yeniden yazıldı), `PROJECT_LOG.md` (§1–§10'da REV-1 düzeltmeleri, 30 satır; §2.6; bu girdi), `ORCHESTRATION_PLAN.md` (§1, §3 Adlandırma, §6 durum satırı, §7, §8, §10, Ek A.6 başlığı ve bu aşamanın açılış ölçümü). Ledger, `Planner-docs/`, `docs/`, README ve UNTRACKED dokunulmadı.
- **Bekleyen:** `main` fast-forward'ı ve push (kapanış commit'inden sonra, ayrı onayla; sonuçlar sohbette, kaydı Pencere 3 açılışında); K9 ve öteki açılış soruları (Pencere 3); depo silme (kullanıcı; üçü de 2026-11-14'te duruyor).
- **Kapanış:** `Window 2: project log sweep and handoff for planning run 21` (yerel commit; döngü kuralıyla onay sorulmadan); Pencere 2'nin son kapanışı. Sonraki oturum: Pencere 3 · O0+O1 — Planlama koşusu 21 (`NEXT_PROMPT.md`; `ORCHESTRATION_PLAN.md` §7).

**2026-11-15: Pencere 2 · O5'in devamı ve takip commit'i (omp, sekizinci pencere, sıkıştırmadan sonra).** Kapsam: C2'den sonraki FF, RID, push ve LSR; ardından kullanıcının isteğiyle faz ve aşama uzunluklarının bağlam bütçesine göre boyutlanması. Ledger'a, `Planner-docs/`'a ve cihaza dokunulmadı.

- **Bağlam:** `2 · O5` oturumu C2'den sonra 738,9k tokene ulaştı; kullanıcı oturumu sıkıştırdı ve 5 saatlik kullanım sınırından sonra devam etti.
- **Açılış (08:06:13Z, salt-okur):** ağaç temiz, uç C2; `git ls-remote origin` değişmemiş (`main` = `587e3b5`); `main` ve `587e3b5` C2'nin atası (yalnız ileri sarma).
- **Kullanıcı kararları (form):** FF onaylandı; push, RID geçerse onaylı; takip commit'inin push'u ayrıca sorulacak; oturum başına bağlam kapanış eşiği 400k (plan Onay 3).
- **FF (08:14:45Z):** `git fetch . integrate/impl-96:main`: `main` `7fa0a51` → C2.
- **RID:** plan Ek A.5 betiği plandan çıkarılıp çalıştırıldı (C2 dahil bütün ref'ler ve 350 dosya): `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=16` → geçti.
- **PUSH (08:15:01Z):** `git push origin main integrate/impl-96`: `main` `587e3b5` → C2; `integrate/impl-96` uzakta yeni dal.
- **LSR:** `git ls-remote origin`: `HEAD`, `refs/heads/main` ve `refs/heads/integrate/impl-96` = C2, yerel hash'lerle aynı; `git fetch origin` sonrası `main` `[origin/main]` ile eşit.
- **Bağlam ölçümü (plan Ek A.7):** projenin sekiz oturum günlüğü betikle okundu. Pencere 2'nin aşamaları 323k–738k'ya ulaştı; açılış 47–54k (eklenen `NEXT_PROMPT.md`'nin KB'ı başına 0,58k); tur başına 5,2–6,4k (yürütme) ve 9,3–13,9k (plan, kontrat); büyümenin %48–77'si modelin kendi çıktısı.
- **Plan:** Onay 3 ve Kural notu; §0 döngü paragrafı ve adım 9 (eşik 400k, 300k'dan sonra yeni görev yok, hedef 240k, tahmin formülü, okuma, alt ajan, yazım ve devir kuralları); §1'de Pencere 2 ve `2 · O5` satırlarına yayın sonucu, Pencere 3'ün `O0` ve `O1` satırları; §7'de soru 8, "Açılışta ayrıca" ve "Oturum düzeni ve bütçe" (Pencere 3 sekiz oturum); §8 ve §9 oturum düzeni; Ek A.7.
- **Geçitler (08:34:47Z):** doğrulayıcı `--mode all` taban değerde (çıkış 0); `--mode step4 --strict` yalnız bilinen uyarıyla (çıkış 1); `--self-test` PASS, sha256 `407fb9be…`.
- **NEXT_PROMPT:** `3 · O0` için yeniden yazıldı: 62 KB'tan ≈ 19,7 KB'a (açılış tahmini ≈ 59k → ≈ 35k token). Taslağı geniş bağlamlı salt-okur bir ajan yazdı (çıkarılan madde grupları plana ve bu günlüğe atıfla); orkestratör betikle doğruladı (LF, satırlar ≤ 600 bayt, boru, kimlik değeri ve C2 hash'i yok) ve `cp` ile yerine koydu. Açılış ölçümünün kimliği `W3OPN` (plan §7); depo silme adımları geri eklendi.
- **İnceleme (salt-okur reviewer, plan ve günlük farkı):** P0 yok. P1 (§11 girdisi eksik) farkın bu girdiden önce alınmasındandı; girdi yazıldı. Üç P2 (`O0`+`O1` birleşiminin §0 ve §9'da çelişmesi, ölçüm aralığının 400k'yı korumaması, §2'deki Döngü satırı) ve altı P3 (§2 Push satırı, §6 durum satırı, soru 8 atfı, tur sayıları, etiketleme, A.7'de kimlikle seçim, §8 bulgu dosyası ve `4 · O1+O2`, takip push'unun sorulması) plana işlendi.
- **Değişen dosyalar:** `ORCHESTRATION_PLAN.md`, `PROJECT_LOG.md` (§2.6 aynı satır sayısıyla; bu girdi), `NEXT_PROMPT.md`. Ledger, `Planner-docs/`, `docs/`, README ve UNTRACKED dokunulmadı.
- **Doğrulama (08:54:53Z):** Ek A.7 betiği plandan çıkarılıp çalıştırıldı (bu oturumun kimliğini ve 275k'yı verdi). Aynı reviewer'ın `NEXT_PROMPT.md` kontrolü: P0–P2 yok, iki P3 düzeltildi. Bayt ve boru kontrolü üç dosyada geçti (LF, CR 0, NUL 0). Kimlik taraması: `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=15` (yeni `NEXT_PROMPT.md` anahtar adlarını anmıyor) → geçti. Bu oturumun bağlamı sıkıştırmadan sonra 87k'dan kapanışta ≈ 360k'ya çıktı; 300k'dan sonra yeni iş açılmadı.
- **Kapanış:** `Window 2 follow-up: context budget and stage sizing` (yerel commit); FF ve push'u ayrıca sorulur. Sonraki oturum: Pencere 3 · O0 — Planlama koşusu 21'in keşfi (`NEXT_PROMPT.md`; `ORCHESTRATION_PLAN.md` §7).

**2026-11-15: Pencere 3 · O0 (omp, dokuzuncu pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §7, planlama koşusu 21'in keşfi: açılış ölçümleri, sekiz açılış sorusu, scout'lar, keşif envanteri. Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı. Ledger'a, `Planner-docs/`'a, `docs/`'a ve cihaza dokunulmadı.

- **Açılış (11:57:29Z–11:57:56Z, salt-okur):** ağaç temiz; dal `integrate/impl-96` 76 commit, uç takip commit'i; `main` = `origin/main` = uç, `origin/main..HEAD` 0; etiket yok; 350 dosya; `git ls-remote origin`: `HEAD`, `main`, `integrate/impl-96` = takip commit'i; C2'nin ve takip commit'inin tam hash'leri yerel ve uzak ref'lerle eşleşti. Durum (b): reflog'a göre takip commit'i Pencere 2 oturumunda FF (08:58:01Z) ve push (08:58:04Z) edilmiş; FF ve push sorulmadı. Dört depo `gh api` ile 200. Plan §7.1 `W3OPN`.
- **Kullanıcı kararları (iki form):** sekiz soru; yanıtlar plan §7'de sorularının altında, K9'unki plan §2'de de. Formlar önerilen seçenekleri işaretli getirdi; kullanıcı soru 2'ye kendi yanıtını yazdı (uyarlansın; yönetici artık SukiSU; aynı arayüzlü bir uygulamayı sistem uygulaması olarak mount etme fikri), öteki yedide öneriyi onayladı.
- **PROJECT_LOG:** push cümleleri son duruma göre güncellendi: §2.1 `:49`, §3.5 `:494`, §4 Push `:653`, §8 `:803` ve `:844`, §9 N3 `:893`; §4 K9 satırı (`:651`) yanıtlandı. Hiçbir depo 404 vermediği için silme cümleleri değişmedi.
- **Keşif:** dört salt-okur scout paralel çalıştı (S1 ClaudeQB yönergeleri ve doğrulayıcı kaynağı; S2 `Main-Planing.md`, Audit, Comprehension, Ontology, toolchain; S3 ledger ve Index; S4 aday alt planlar için depo kanıtı). Plan §7'deki S3, kapsam yanıtlarla genişlediği için bağlam güvenliğiyle ikiye bölündü. S1, plan §7'deki doğrulayıcı tuzaklarının 14'ünü de doğruladı. Envanter plan §7.1'de (`W3OPN` ve `W3F01`–`W3F28`, ≈ 13 KB).
- **Plan:** §1'de `3 · O0` `done`; §2'de K9 ve Push satırları; §7'de sekiz tarihli yanıt; yeni §7.1 envanteri.
- **NEXT_PROMPT:** `3 · O1` için yeniden yazıldı (≈ 19 KB); taslağı bir task ajanı `local://`'a yazdı, orkestratör iki satırını düzeltti, `cp` ile yerine koydu ve betikle doğruladı.
- **Değişen dosyalar:** `ORCHESTRATION_PLAN.md`, `PROJECT_LOG.md` (§2.6 aynı satır sayısıyla; bu girdi), `NEXT_PROMPT.md`. Ledger, `Planner-docs/`, `docs/`, README ve UNTRACKED dokunulmadı.
- **Doğrulama (12:30:53Z):** ilk koşu (12:28:51Z) `:494`'ün 600 baytı aşması yüzünden FAIL verdi; satır kısaltıldı, yeniden koşuda bayt ve boru kontrolü üç dosyada geçti (LF, CR 0, NUL 0, tablo boruları tutarlı, değişen satırlar ≤ 600 bayt; `NEXT_PROMPT.md` 19.241 B); `git diff --stat` yalnız bu üç dosya. Kimlik taraması (Ek A.5): `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=16` → geçti. Doğrulayıcı çalıştırılmadı (`Planner-docs/` dokunulmadı). Bağlam (Ek A.7): açılışta 65k, scout sonuçlarından sonra 190k, kapanışta ≈ 233k.
- **Kapanış:** `Window 3 O0: discovery for planning run 21` (yerel commit; push edilmedi). Sonraki oturum: Pencere 3 · O1 — Planlama koşusu 21'in planı (`NEXT_PROMPT.md`; `ORCHESTRATION_PLAN.md` §7).
- **Takip commit'i (kullanıcı onayıyla):** kapanış commit'i `NEXT_PROMPT.md`'yi içermedi: dosya taslaktan `cp` ile konduğu için commit aracı onu seçmedi ve ağaç kirli kaldı. Kullanıcı ayrı commit'i seçti (geçmiş yeniden yazılmadı): `Window 3 O0 follow-up: hand-off for stage 3 O1` (`git log --grep '^Window 3 O0 follow-up:'`); `NEXT_PROMPT.md`'nin beklenen açılış durumu 78 commit ve `origin/main..HEAD` = 2 oldu; plan §1 satırı ve bu günlük güncellendi.

**2026-11-15: Pencere 3 · O1 (omp, onuncu pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §7.2, planlama koşusu 21'in aşama ve görev planı ve kullanıcı onayı. Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı. Ledger'a, `Planner-docs/`'a ve `docs/`'a dokunulmadı; cihaza yalnız onaylı salt-okur komutlar gönderildi.

- **Açılış (12:36Z):** kontrollerin hepsi tuttu (plan §7.2 `W3O1OPN`): dal 78 commit, uç `3 · O0` takip commit'i, `origin/main..HEAD` = 2, etiket yok, 350 izlenen dosya; `gh api`: dört depo 200.
- **Keşif:** üç salt-okur scout: S5 (Faz 6 ve 9, `Main-Planing.md` §9), S6 (`PRB` tasarımı ve SukiSU kaynakları), S7 (doğrulayıcının kipleri ve ara durumları) → `W3F29`–`W3F32`. Sonuçlar: `Faz6.1` `superseded` olur (onu kullanacak yapı yok); Faz 9 ROM derlemesine bağlı değil; `3 · O2a` ve `3 · O2b`'den sonra `--mode all` yalnız `missing_phase_folder` ile kırmızı (beklenen ara durum); `CPa` ve `CPb` Index girdilerini aynı oturumda ekler.
- **Plan ve onay:** §7.2 (oturumlar ve tahminleri, görevler, alt planlar `Faz10.1`–`Faz10.5`, Step 1 listesi, `W3F28` kararları, ara durumlar, sıcak noktalar, `PRB` komutları). Sunumdan sonra gelen inceleme notlarıyla üç düzeltme: uzun taslaklar geniş bağlamlı scout'a; `PRB` `py -3` betiğiyle; bütçe kalibrasyonu ve `PRB`'yi kaydırma kuralı. Kullanıcı formla "onay" verdi; dört soruda öneriler kabul.
- **`PRB` (13:01:41Z–13:01:43Z):** `PRB1`–`PRB10` `dc27e5d0`'da; çıktının kimlik taraması temiz; sonuçlar §7.1 `W3P01`–`W3P04`. Cihaz durumu değişmedi.
- **Plan yazımları:** §1 (`3 · O1` `done`; `3 · O2a`–`3 · O5` satırları), §3 (Pencere 3 adlandırma maddesi; `PRB` komutları `PRB1`–`PRB10`, `C1`–`C3` commit'leriyle karışmasın diye), §7.1 (`W3P01`–`W3P04`), §7.2, §10 (`3 · O1` maddeleri).
- **Süreç notu:** devir taslakları için açılan scout içerik filtresince reddedildi (`reasoning_extraction`); `NEXT_PROMPT.md` ve bu girdi orkestratörce yazıldı.
- **Kontroller:** bayt ve boru kontrolü (LF, CR 0, NUL 0, tablo boruları) geçti; kimlik taraması geçti (`value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=16`). Bağlam: plan sunumunda 206k, onayda 235k, kapanışta ≈ 340k.
- **Kapanış:** `Window 3 O1: plan for planning run 21` (yerel commit; push edilmedi). Sonraki oturum: Pencere 3 · O2a — Step 1 (`NEXT_PROMPT.md`; `ORCHESTRATION_PLAN.md` §7.2).

**2026-11-15: Pencere 3 · O2a (omp, on birinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §7.2, planlama koşusu 21'in Step 1'i, yani kullanıcının onayladığı metinle yalnız `Planner-docs/Main-Planing.md`'nin yeniden yazımı; bu girdi bir IMPL satırı değildir, ledger'a, `Planner-docs/`'un öteki dosyalarına ve `docs/`'a dokunulmadı.

- **Açılış (13:18Z):** kontrollerin hepsi `NEXT_PROMPT.md` §3 ve §4a'yla tuttu: ağaç temiz; dal `integrate/impl-96` 79 commit, uç `Window 3 O1: plan for planning run 21`; `origin/main..HEAD` = 3; `main` = `origin/main` = `6632a18`; etiket yok; 350 izlenen dosya; `git ls-remote origin` üç ref `6632a18`; plan §1'de ilk `pending` `3 · O2a`. `gh api -i` (13:18:54Z–13:19:01Z): dört depo 200. Taban (13:18:54Z): `--mode step1 --strict` 0 bulgu (`main_phase_count=9`); `--mode all` V1 tabanı (`error_count=0`, `warning_count=1`); ikisi de çıkış 0.
- **Keşif (`ST1-R`):** iki paralel scout. MainMapScout `Main-Planing.md`'nin tam haritasını çıkardı (başlıklar, yol haritası satırları 119–127, Faz 6–9 aralıkları, §9 284–301, §10 302–316); çapa kaymadı; tarama 7 eski satır daha buldu (57, 59, 69, 105, 121, 157, 165). RulesScout: 11 sabit başlık (`# Main Planing` ve `## 1.`–`## 10.`), step1 kontrolleri, First-Planner §9 devir konuları (294–301); Step 1.5'i atlamak açık kullanıcı kararı ister (verildi: soru 8 yanıtı, 2026-11-15).
- **Taslak (`ST1-D`):** taslaktan önce bir inceleme notu kabul edildi ve taslak brifi düzeltildi: ledger `:606` (`DEC-28`) yalnız Faz 7 ve 8'i anar ("formal retirement is planning run 21"), `:610` (`DEC-32`) yalnız modülün HyperOS 4'e uyarlanmasını; Phase 10, Faz 7/8'in tam emekliliği ve Faz 6'nın ROM hedefinin emekliliği koşu 21'in seçimleridir (kullanıcı, 2026-11-15). Bir yerine iki paralel taslak scout'u (ayrık satır kümeleri): RoadmapDraft (A01–A11, §6), TextDraft (B01–B35 öteki bölümler; isteğe bağlı C01–C03).
- **İnceleme:** DraftReview ajanı: P0 0, P1 0, P2 3, P3 11. P2'ler: B10 (`ce419bc9…` HAL iddiasının tarihi), A11 (HyperOS 4 "since 2026-11-13" → 2026-11-13'te gözlendi, `DEC-28`'e göre daha önce kuruldu), B31 (2026-11-13 ledger kanıtı HyperOS 4'tür). Üç P2 ve 10 P3 taslak scout'larınca düzeltildi; 1 P3 (Step 2 snapshot işleyişi) `3 · O2b`'ye ertelendi.
- **Onay (`ST1-A`):** kullanıcı 2026-11-15T14:10Z'de formla "onay" verdi, isteğe bağlı üç blokla: C01 (satır 63: oradaki "Faz 10" `50MP-Entegrasyon-Plani.md` numaralamasıdır), C02 (§8 madde 11: Faz 10'un sonraki adımı), C03 (§5 "Platform decisions" paragrafı: `DEC-28`, `DEC-32`, `DEC-33`). Bir inceleme notu, ≈ 61 KB'lık taslak sohbet çıktısı olarak gittiği için metnin kullanıcıya ulaşmamış olabileceğini uyardı; kullanıcı ikinci formda metnin tamamını onaydan önce gördüğünü doğruladı ("gördüm"), onay geçerli kaldı.
- **Uygulama ve geçit (`ST1-W`, 14:10:06Z):** `py -3` betiğiyle uygulandı, sha256 `6790b6ae…` onaylı derlemeyle aynı; 49 değişiklik; `Main-Planing.md` 316 → 406 satır, 52.969 → 77.019 B, CRLF 406, çıplak LF 0, NUL 0, tablo boruları tutarlı. Geçit (14:10Z): `--mode step1 --strict` geçti, çıkış 0 (`main_phase_count=10`); `--mode all` çıkış 1, `error_count=1` (`missing_phase_folder=Planner-docs/Faz-10-Plans`) ve bilinen uyarı: beklenen ara durum (plan §7.2 "Ara durumlar ve geçitler").
- **Plan yazımları:** §1 (`3 · O2a` `done`; satırda kapanış commit'i, açılış, `ST1-R`, `ST1-D`, inceleme, onay, geçit ve bağlam özeti), §7.2 (`3 · O2a` notu: ledger'dan doğrulanan `DEC-28` ve `DEC-32` metinleri; `3 · O2b` için snapshot sorusu), §10 (`3 · O2a`'da eklenen: `Main-Planing.md`'nin koşu 21 kararlarına bağlı olmayan eski ifadeleri, `:18`, `:247`, `:310` ve yeniden yazılan satırlardaki eski yan cümleler `:22`, `:57`, `:69`, `:75`; numaralar Step 1'den öncekiler; 12. denetime).
- **Süreç notu:** kapanış başladıktan sonra (plan yazımları yapılmıştı) omp süreci yeniden başladı. `NEXT_PROMPT.md` taslağını (`local://np-o2b.md`, 19.945 B, 0–9. bölümler tam) yazan `HandoffDraft` ajanı kayboldu; §2.6 ve §11 taslaklarını düzeltici bir ajan yazdı; kullanıcı "Kaldığın yerden devam edebilirsin" dedi. `np-o2b.md`'yi denetleyecek salt-okur inceleyici `HandoffReview`, `3 · O1`'deki scout gibi içerik filtresince reddedildi (`reasoning_extraction`); orkestratör taslağı olgulara ve plana karşı kendisi denetledi.
- **Kontroller:** kimlik taraması (Ek A.5, plandaki betiğin aynısı) `ST1-W`'den sonra ve son ağaçta geçti (`value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=16`); doğrulayıcı kapanışta Step 1 sonrasıyla aynı (`step1 --strict` çıkış 0, `all` yalnız `missing_phase_folder`).
- **Bayt ve boru (kapanış betiği):** dört dosyada satır sonları korundu (`Main-Planing.md` CRLF, öteki üçü LF), NUL 0, tablo boru uyumsuzlukları HEAD ile aynı (plan `:174` ve `:759`, taban). İlk koşu plana eklenen iki satırın 600 baytı aşması yüzünden FAIL verdi (§1 `3 · O2a` satırı 778 B, §7.2 notu 657 B); ikisi kısaltıldı, ikinci koşu geçti.
- **Bağlam:** açılışta 86k, `ST1-R` gönderiminden sonra 154k, onaydan önce 207k, kapanış başında ≈ 241k (tahmin 225k), yeniden başlatmadan sonra 159k.
- **Kapanış:** `Window 3 O2a: Step 1 for planning run 21` (`git log --grep '^Window 3 O2a:'`; yerel commit; push edilmedi): 80 commit, `origin/main..HEAD` = 4, 350 izlenen dosya (yeni dosya yok), `main` = `origin/main` = `6632a18` değişmedi; FF ve push `3 · O5`'te, ayrı onaylarla. Değişen dosyalar: `Planner-docs/Main-Planing.md`, `ORCHESTRATION_PLAN.md` (§1, §7.2, §10), `PROJECT_LOG.md` (§2.6 aynı satır sayısıyla; bu girdi), `NEXT_PROMPT.md`. Sonraki oturum: Pencere 3 · O2b — Step 2 kontratı (`NEXT_PROMPT.md`; `ORCHESTRATION_PLAN.md` §7.3).

**2026-11-15: Pencere 3 · O2b (omp, on ikinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §7.3, planlama koşusu 21'in Step 2 kontratı; bu girdi bir IMPL satırı değildir, ledger'a, `Planner-docs/`'a ve `docs/`'a dokunulmadı, cihaza komut gönderilmedi.

- **Açılış (18:35Z):** `NEXT_PROMPT.md` §4 (a) kontrollerinin hepsi tuttu (80 commit, uç `Window 3 O2a: Step 1 for planning run 21`, `origin/main..HEAD` = 4, `main` = `origin/main` = `6632a18`, etiket yok, 350 dosya); dört depo 200 (18:35:38Z–18:35:40Z); taban `step1 --strict` 0 bulgu, `all` yalnız `missing_phase_folder` ve bilinen uyarı; `Main-Planing.md` sha256 `6790b6ae…` `3 · O2a` ile aynı.
- **Şablon:** kullanıcı genel bir orkestrasyon şablonuyla geldi (keşif, onaylı plan, kontrat, paralel uygulama, entegrasyon, inceleme). Plana uyarlandı: dal `integrate/impl-96` sürer (kullanıcı formda seçti); `librarian`, `designer`, `isolated`, `outputSchema` ve advisor bu ortamda yok; aşamada uygulama yok (§7.3 sıcak noktada); tek kapanış commit'i; geçitler belge geçitleri.
- **`ST2-R`:** üç paralel scout (Step 2 belgeleri; 42 alt plan; ledger, Index, Ontology, Comprehension, toolchain); ayrıntı dosyaları `local://`'da kaldı, kararlar §7.3'te. Orkestratör `%TEMP%/ishtar-st2/scan.py` ile doğrulayıcının kendi fonksiyonlarını kullanıp 42 alt planı taradı: 2.030 aday cümlede tekrar 0, §3/§7 gövde tekrarı 0, §9'da 65 ayrı yol.
- **Onay:** plan tablosu ve kontrat özü formla sunuldu; yanıt "onay", dal `integrate/impl-96`.
- **`ST2-K`:** taslak `%TEMP%/ishtar-st2/s73.md` `lines.py replace` ile §7.2'nin sonuna eklendi (73 satır); inceleme düzeltmesinden sonra 76 satır, en uzun 599 B; plan 910 → 986 satır, LF, NUL 0.
- **İnceleme:** salt-okur inceleyici (atıfların hepsi içerikle doğru): P0 0, P1 1 (`I3a`-2 eski snapshot satırlarındaki "active" işaretlerini ve ledger `:60` cümlesini kapsamıyordu; 12. denetim ya da Step 4 iki etkin plan görüp durabilirdi), P2 4 (`Faz7.1`/`Faz8.2` yanlışlıkla üstü çizilecekti; 50MP kutucuğu 10.5'in dosyalarına dokunuyordu; `I3a`-3 kendisiyle çelişiyordu; Step 1/2 dışı `3 · O4` yazımları koşu satırında anılmıyordu), P3 7. Advisor notu: modül yorumları `Main-Planing.md:288` gereği `Faz10.5`'te kalmalı.
- **Düzeltme (kullanıcı onayı, form "hepsi"):** sahiplik kuralı 10.1–10.4 ayrık, 10.5 sürüm eki (`Faz3.8:120` kalıbı); tile manifest, `strings.xml`, `service.sh` ve derlenen APK `Faz10.4`'e; klasör yerine dosya adları; `I3a`-2 eski işaretleri, `I3a`-8 ledger §7 `:550` notu; durdurma/başlatma sırası Ontology değişmez 3'e göre; değişmezler satır içinde.
- **Kontroller:** kimlik taraması (Ek A.5'teki betiğin aynısı) PASS (`value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=17`); değişen dosyalarda CR 0, NUL 0; plandaki boru uyumsuzlukları yalnız taban (`:174`, `:835` = eski `:759`); `step1 --strict` 0, `all` beklenen ara durum.
- **Bağlam:** açılışta 82k, scout'lardan sonra 179k, plan onayında ≈ 185k, inceleme düzeltmesinden sonra 268k (tahmin 225k); fark uzun düşünme ve iki onay formu.
- **Kapanış:** `Window 3 O2b: Step 2 contract for planning run 21` (`git log --grep '^Window 3 O2b:'`; yerel commit; push edilmedi): 81 commit, `origin/main..HEAD` = 5. `NEXT_PROMPT.md` `3 · O3a` için yeniden yazıldı (taslak salt-okur scout'ta, orkestratör düzeltti).

**2026-11-15/16: Pencere 3 · O3a (omp, on üçüncü pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §7.3, planlama koşusu 21'in Step 2 taslakları `Faz10.1`–`Faz10.3` (`SP1`–`SP3`, `CPa`); bu girdi bir IMPL satırı değildir, ledger'a, `Main-Planing.md`'ye ve `docs/`'a dokunulmadı, cihaza komut gönderilmedi.

- **Açılış (2026-11-15T19:42Z):** `NEXT_PROMPT.md` §4 (a) kontrollerinin hepsi tuttu (81 commit, uç `Window 3 O2b: Step 2 contract for planning run 21`, `origin/main..HEAD` = 5, `main` = `origin/main` = `6632a18`, etiket yok, 350 dosya); `Main-Planing.md` sha256 `6790b6ae…` aynı; dört depo 200 (19:42:48Z–19:42:51Z); taban `step1 --strict` 0, `all` yalnız `missing_phase_folder`.
- **Plan:** kullanıcının genel orkestrasyon şablonu plana göre uyarlandı (yeni dal ve kontrat commit'i yok; `librarian`, `designer`, `isolated`, `outputSchema` yok; Index `edit` ile; son inceleme eklendi); form "onay".
- **Keşif ve betik:** iki scout doğrulayıcının alt plan kurallarını ve `Faz9.1`/`Faz3.1` biçim iskeletini `local://`'a özetledi; bir `task` ajanı `%TEMP%/ishtar-st3/draftcheck.py`'yi yazdı (C1–C12); C11'in yanlış alarmı (artık yalnız `Depends on` satırları) ayrı bir `task` ile düzeltildi.
- **Kesinti:** 2026-11-15 gecesi `SP1`–`SP3` ve betik ajanı hesap sınırına (429) takıldı; diriltme yedek modele düştü, kredisi yoktu (402). 2026-11-16 sabahı üç taslak scout'u tam ortak bağlamla yeniden başlatıldı (`SP1R`–`SP3R`).
- **Taslaklar ve `CPa`:** betik bulguları scout'larca düzeltildi (`VAL-102-MANUAL`; `snapshots/` satırları dosya adıyla, `.txt`); üç dosya `cp` ile yerine; Index'e 12 satır eklendi, 3 satır değişti (`:24`, `:39`, `:162-168`, `:188`, `:300-302`).
- **İnceleme:** REV ∥ SEC: sızıntı yok, P0 0, P1 5, P2 6, P3 11; kullanıcı "hepsi" dedi (form). Teyit turunda REV'in 10 ve SEC'in 14 bulgusu kapandı, yeni P0/P1 yok; yeni P2 2 (10.2'nin derleme komutundaki `%TEMP%` Git Bash'te açılmaz; 10.3 yazmadan hemen önce canlı dosyayı yedekle karşılaştırmıyordu) ve P3 4 de scout'larca düzeltildi.
- **Kontroller:** son taslaklarla `DRAFTCHECK: PASS files=3`; `step2 --strict` çıkış 0; `all` çıkış 0, yalnız denetim uyarısı, `subplan_count=45`; `step1 --strict` 0; V2 taban; V3 `SELF-TEST: PASS`; LF, CR 0, NUL 0; plan boruları yalnız taban (`:174`, `:838`); kimlik taraması PASS (commit'ten önce `prose_mentions=18`).
- **Bağlam:** açılışta 85k; keşiften sonra 149k; gece kesintisinden sonra yeniden yüklemede 111k; inceleme kararında 187k; teyit turunda 250k (tahmin 185k); fark kesinti, iki inceleme turu ve düzeltme döngüleri.
- **Kapanış:** `Window 3 O3a: Step 2 drafts 10.1-10.3 for planning run 21` (`git log --grep '^Window 3 O3a:'`; yerel commit; push edilmedi): 82 commit, `origin/main..HEAD` = 6. `NEXT_PROMPT.md` `3 · O3b` için yeniden yazıldı (taslak salt-okur scout'ta).
- **Takip commit'i (kullanıcı onayı, form "takip"):** `Window 3 O3a follow-up: scope the hand-off line-length gate`. Kapanıştan sonra gelen inceleme notu: `NEXT_PROMPT.md` §4 (d) geçidi "satırlar ≤ 600 bayt" diyordu, taslak satırları ise 817–1406 bayt; sınır yeniden orkestratörün satırlarına bağlandı. Beklenen durum 83 commit, `origin/main..HEAD` = 7.

**2026-11-16: Pencere 3 · O3b (omp, on dördüncü pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §7.3, planlama koşusu 21'in Step 2 taslakları `Faz10.4`, `Faz10.5` (`SP4`, `SP5`, `CPb`); bu girdi bir IMPL satırı değildir, ledger'a, `Main-Planing.md`'ye ve `docs/`'a dokunulmadı, cihaza komut gönderilmedi.

- **Açılış (2026-11-16T08:40Z):** `NEXT_PROMPT.md` §4 (a) kontrollerinin hepsi tuttu (83 commit, `origin/main..HEAD` = 7, `main` = `origin/main` = `6632a18`, etiket yok, 353 dosya); `Main-Planing.md` sha256 `6790b6ae…` aynı; dört depo 200 (08:40:19Z–08:40:22Z); taban `step2`/`step1 --strict` 0, `all` 0 (`subplan_count=45`).
- **Plan:** şablon `3 · O3a`'daki gibi uyarlandı; ayrı keşif scout'u yok (bağımlılık haritası §7.3); form "onay", inceleme "ekle".
- **Betik ve taslaklar:** `task` ajanı (D2) `draftcheck.py`'yi genişletti, orkestratör C11 ve `CPb` için iki küçük değişiklik yaptı; `SP4` ∥ `SP5` taslakları yazdı, ilk birlikte koşu `DRAFTCHECK: PASS files=2`.
- **`CPb`:** açık konular orkestratörce karara bağlandı (plan §7.3 `:719`–`:720`, §10 `:808`–`:811`); scout'lar taslakları güncelledi; iki dosya `cp` ile yerine, Index'te dört satır (`:168`–`:169`, `:190`, `:303`).
- **İnceleme:** REV ∥ SEC: P0 0, P1 3, P2 4, P3 9 (§2.6); kullanıcı "hepsi" dedi (form). Düzeltmeden sonra betik C5 buldu (10.4'te başka alt planın iş kalemi kimliği), scout düzeltti. Teyit turu: eskilerin hepsi kapandı; yeni P2 1 ve P3 1 düzeltildi, bir P3 değişiklik gerektirmedi, biri `3 · O4` notu. *(2026-11-16 notu: buradaki §2.6, `git log --grep '^Window 3 O3b:'` kapanış commit'indeki §2.6'dır; §2.6 her kapanışta yeniden yazılır.)*
- **Kontroller:** son dosyalarla `DRAFTCHECK: PASS files=2`; `step2 --strict` 0; `all` 0, yalnız denetim uyarısı, `subplan_count=47`; `step1 --strict` 0; V2 taban; V3 `SELF-TEST: PASS`; LF, CR 0, NUL 0; plan boruları yalnız taban (`:174`, `:844`); kimlik taraması PASS.
- **Bağlam:** açılışta 64k; plan formunda 98k; taslaklarda 151k; incelemede 189k; düzeltme turunda 207k; teyitten sonra 236k (tahmin 155k); fark iki düzeltme turu, teyit ve `CPb` kararları.
- **Kapanış:** `Window 3 O3b: Step 2 drafts 10.4-10.5 for planning run 21` (`git log --grep '^Window 3 O3b:'`; yerel commit; push edilmedi): 84 commit, `origin/main..HEAD` = 8. `NEXT_PROMPT.md` `3 · O4` için yeniden yazıldı (taslak salt-okur scout'ta).

**2026-11-16: Pencere 3 · O4 (omp, on beşinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §7.3 hedef tablosu, planlama koşusu 21'in entegrasyonu ve geçitleri (`I3a`, `I3b`, `GATE3`); bu girdi bir IMPL satırı değildir; `Main-Planing.md`, alt planlar ve Audit dokunulmadı, cihaza komut gönderilmedi.

- **Açılış (2026-11-16T10:17Z):** `NEXT_PROMPT.md` §4 (a) kontrollerinin hepsi tuttu (84 commit, `origin/main..HEAD` = 8, `main` = `origin/main` = `6632a18`, etiket yok, 355 dosya); snapshot değerleri aynı (ledger 653 CRLF, Index 426 LF, Ontology NUL 2); dört depo 200 (10:17:27Z–10:17:31Z); taban `step2`, `step1`, `step3-preflight` `--strict` 0, `all` 0 (`subplan_count=47`); kimlik taraması PASS.
- **Plan:** şablon plana göre uyarlandı (§2.6); form "onay", teyit "ekle", iki kural "yeni §5.5". *(2026-11-16 notu: buradaki §2.6, `git log --grep '^Window 3 O4:'` kapanış commit'indeki §2.6'dır; §2.6 her kapanışta yeniden yazılır.)*
- **Taslaklar ve uygulama:** üç salt-okur scout aynı turda (`I3a-A`, `I3a-B`, `I3b-D`) JSON işlem listeleri yazdı; `%TEMP%/o4/o4.py` uyguladı (çapalar tekil, sondan başa, bayt düzeyinde). Index, Comprehension ve toolchain de `edit` yerine betikle yazıldı: taslak metni yeniden yazılmadı.
- **Kontroller:** HEAD'e karşı satır ve karakter düzeyinde difflib (yalnız ekleme; ledger'da izinli üç hücre); yeni satırların boruları ledger §2 6, §3 7, §4 10, §8 7; ledger §4 34/1/5/7.
- **İnceleme:** teyit (reviewer) P0 0, P1 0, P2 2, P3 5 (§2.6). Düzeltme işlemlerini taslağın scout'ları yazdı, `fix.py` yalnız bu aşamanın değiştirdiği satırlarda uyguladı; R6'da toolchain başlık notu geri alındı, R7 (§5.5) orkestratörce; Step 2'nin Index `:165`, `:192` ifadesi plan §10'a. *(2026-11-16 notu: buradaki §2.6, `git log --grep '^Window 3 O4:'` kapanış commit'indeki §2.6'dır; §2.6 her kapanışta yeniden yazılır.)*
- **Geçit:** `GATE3` iki kez geçti (20:18Z; düzeltmelerden sonra 20:30Z); değerler §2.6. `NEXT_PROMPT.md` taslağı betikle denetlendi (19.323 B, LF, en uzun satır 427 B, tablolar tutarlı). *(2026-11-16 notu: buradaki §2.6, `git log --grep '^Window 3 O4:'` kapanış commit'indeki §2.6'dır; §2.6 her kapanışta yeniden yazılır.)*
- **Bağlam:** açılışta 59k; plan formunda 117k; taslaklarda ≈ 175k; incelemeden sonra ≈ 206k; kapanışta ≈ 250k (tahmin 233k); fark teyit incelemesi ve düzeltme turu.
- **Kapanış:** `Window 3 O4: integration and gates for planning run 21` (`git log --grep '^Window 3 O4:'`; yerel commit; push edilmedi): 85 commit, `origin/main..HEAD` = 9. `NEXT_PROMPT.md` `3 · O5` için yeniden yazıldı (taslak salt-okur scout'ta).
- **Takip commit'i (kullanıcı onayı, form "takip"):** `Window 3 O4 follow-up: record line shifts and FIX3 items`. Kapanıştan sonra gelen inceleme notu: §5.5'in +5 kayması `Faz10.5` `:33`, `:65`'teki `PROJECT_LOG.md:852-866` atfını kaydırdı (doğrusu `:857-871`); bu dosyada `DEC-33` eksik, K9 beş yerde "açık". Betik taraması ve kayma haritası plan §10 `:816`, `FIX3` maddeleri `:817`; içerik `3 · O5`'te düzeltilir. Beklenen durum 86 commit, `origin/main..HEAD` = 10; plan boru tabanı `:174`, `:850`.

**2026-11-16: Pencere 3 · O5 (omp, on altıncı pencere).** Kapsam: `REV-4` ∥ `SEC-C` → `FIX3` → `C3` → FF (onay) → `RID` → push (onay) → `LSR`, `DEL3` (plan §7.2); bu girdi bir IMPL satırı değildir; cihaza komut gönderilmedi.

- **Açılış (2026-11-16T20:55Z):** `NEXT_PROMPT.md` §4 (a) kontrollerinin hepsi tuttu (86 commit, `origin/main..HEAD` = 10, `main` = `origin/main` = `6632a18`, etiket yok, 355 dosya); snapshot aynı (ledger 662 CRLF, Index 443, Ontology NUL 2); dört depo 200; `GATE3` tabanı tuttu; kimlik taraması PASS (`prose_mentions=24`).
- **Plan:** şablon plana göre uyarlandı; form "onay" ve teyit "ekle"; inceleme girdileri `local://` dosyalarına yazıldı (REV 130–166 KB, SEC 263–378 KB), aynı anda en çok dört ajan.
- **İncelemeler:** `REV-4a` P2 4, P3 6; `REV-4b` P2 4, P3 9; `REV-4c` P3 4; `REV-4d` P2 1, P3 3; `SEC-C1` P3 1; `SEC-C2` 0; `SEC-C3` P3 1. P0/P1 yok. Kapsam formu "hepsi".
- **`FIX3`:** üç scout (`fix-a` 10.1–10.2, `fix-b` 10.3–10.5, `fix-c` ledger, Index, bu dosya, plan) 86 işlem yazdı; `apply.py` kuru denemeden sonra yazdı; satır sayıları sabit, `:857` hâlâ "13 bayat ifade". `RID` Ek A.5 kimlik kontrolü olarak kaldı, depo ölçümü `DEL3` oldu (plan `:99`, `:571`, `:595`).
- **Teyit:** reviewer P2 3, P3 5; security-reviewer 0; hepsi bu aşamada düzeltildi (`fix-t`).
- **Geçit (21:27Z):** `step2`, `step1`, `step3-preflight` `--strict` 0; `all` 0 (`subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`, yalnız denetim uyarısı); V2 çıkış 1 (taban); V3 PASS, sha256 aynı; boru plan `:174`, `:850` (§10 eklemesinden sonra `:854`); kimlik PASS (`prose_mentions=24`).
- **Bağlam:** açılışta 78k; plan formunda 119k; incelemelerden sonra ≈ 194k; `FIX3`'ten sonra ≈ 225k; teyit düzeltmelerinden sonra, C3'ten önce 267k (tahmin 215k).
- **Kapanış:** C3'ten önce dört depo 200 (21:31:10Z–21:31:13Z); `Window 3: planning run 21 and handoff for the twelfth audit` (`git log --grep '^Window 3:'`; yerel commit): 87 commit. `NEXT_PROMPT.md` Pencere 4 · `O0` için yeniden yazıldı (taslak salt-okur scout'ta, yer tutucular betikle). FF, push, `LSR` ve `DEL3` sonuçları sohbette; Pencere 4 açılışı doğrular ve kaydeder.

**2026-11-16/17: Pencere 4 · O0 (omp, on yedinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §8, 12. denetimin keşfi: açılış ve yayın doğrulaması, taban, üç scout, keşif envanteri. Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı. Ledger'a, `Planner-docs/`'a, `docs/`'a ve cihaza dokunulmadı.

- **Açılış (2026-11-16T22:09:57Z–22:10:05Z, salt-okur):** ağaç temiz; dal 87 commit, uç C3; `main` = `origin/main` = uç, `origin/main..HEAD` 0; etiket yok; 355 dosya; `ls-remote`: `HEAD`, `main`, `integrate/impl-96` = C3. Yayın: reflog'a göre C3 `3 · O5`'te FF (22:05:00Z) ve push (22:05:35Z) edilmiş; soru sorulmadı. Snapshot aynı; dört depo 200. Plan §8.1 `W4OPN`, `W4F01`.
- **Taban (22:11:08Z–22:12:19Z):** `NEXT_PROMPT.md` §7 tabanı tuttu; kimlik taraması `prose_mentions=26` (24'ten artış C3 yamasının iki bağlam satırı). `--mode step3` bir kez ölçüldü (taban değil): bayraksız çıkış 0, `--strict` 1 (`W4F03`).
- **Keşif:** S1–S3 22:13Z'de paralel gönderildi; üçü 22:15Z'de 429 ile durdu (`retry-after` 762 s). Oturum 2026-11-17T05:12Z'de sürdü; görevler ortak bağlamla taze gönderildi ve bitti (5–7 dk). S2 ve S3'ten envanter satırları ayrıca istendi (`local://`). Envanter plan §8.1 (`W4OPN`, `W4F01`–`W4F27`, 13,8 KB).
- **Bulgular (özet):** S1 dilimleri 7 çalışma, 3 oturum; S2: 21 plan iddiasından 19'u doğru, §8 `:749` kısmen, `:751` geçit lafzı düzeltilmeli; S3: 32 madde, hepsi açık. Kararlar `4 · O1+O2`'ye (`W4F27`).
- **PROJECT_LOG:** push cümleleri güncellendi: §2.1 `:49`, §3.5 `:494`, §4 Push `:653`, §8 `:808` ve `:849`, §9 N3 `:898`; silme cümleleri değişmedi. §2.6 aynı satır sayısıyla.
- **Plan:** §1'de `4 · O0` `done`, `4 · O1+O2` `pending` (tahminle); §3'e Pencere 4 Adlandırma; yeni §8.1. Boru dışı satırlar artık `:177`, `:892`.
- **NEXT_PROMPT:** `4 · O1+O2` için yeniden yazıldı; taslağı salt-okur bir scout yazdı, orkestratör betikle denetleyip `cp` ile yerine koydu.
- **Doğrulama:** kapanıştan önce üç dosyada bayt ve boru kontrolü (LF, CR 0, NUL 0, tablo boruları tutarlı, değişen satırlar ≤ 600 bayt) ve kimlik taraması (Ek A.5) geçti; `git diff --stat` yalnız bu üç dosya. Doğrulayıcı yeniden çalıştırılmadı (`Planner-docs/` dokunulmadı).
- **Bağlam (Ek A.7):** ilk ölçüm 98,6k; scout'lar gönderilince 154k; S2'den sonra 182k; envanterden sonra 247k; kapanışta ≈ 270k (tahmin 185k; 429 yeniden gönderimi dahil).
- **Kapanış:** `Window 4 O0: discovery for the twelfth audit` (yerel commit; push edilmedi). Sonraki oturum: Pencere 4 · O1+O2 (`NEXT_PROMPT.md`; plan §8, §8.1).

**2026-11-17: Pencere 4 · O1 (omp, on sekizinci pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §8.2, 12. denetimin aşama ve görev planı. Birleşim `O1+O2` açılışta onaylandı; `O1` onayında bağlam 200k'yı geçtiği için `O2` ayrı oturum oldu. Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı. Ledger'a, `Planner-docs/`'a, `docs/`'a ve cihaza dokunulmadı.

- **Açılış (2026-11-17T09:52:59Z–09:59Z, salt-okur):** ağaç temiz; dal 88 commit, uç `Window 4 O0:` (tek eşleşme); `main` = `origin/main` = `081790f`, `origin/main..HEAD` 1; etiket yok; 355 dosya; `ls-remote` üç ref = `081790f`; dört depo 200; snapshot aynı. Plan §8.2 `W4O1OPN`.
- **Taban (09:55:11Z–09:55:26Z):** `NEXT_PROMPT.md` §7 tabanı tuttu; kimlik taraması `prose_mentions=26`.
- **Birleşim:** form "evet" (`O1` onayında bağlam 200k'yı geçerse `O2` ayrı oturum). Kullanıcının orkestrasyon şablonuyla plan arasındaki farklar formda söylendi: yeni dal açılmaz (dal sürer, plan §7.2); şablonun Faz 3–5'i sonraki oturumlardır; `isolated`, `outputSchema`, `librarian` ve `designer` bu ortamda yok. Formdaki "advisor yok" ifadesi yanlıştı (danışman notları geldi, aşağıda); kapanış raporunda düzeltildi.
- **Danışman notları (dördü de uygulandı):** (1) reviewer penceresi bilinmiyordu: üç yoklama ajanı (`W4O1P01`), seçenek gerekçesi düzeltildi, öneri A'dan C'ye döndü; (2) form gönderilirken bağlam 200.951 tokendı: `O2` başlamadı, `O1` kapandı; (3) yoklama satırları (`security-reviewer` `partial`) ve `CT4` kabul atfı düzeltildi; (4) NEXT_PROMPT taslağı `cp`'den önce betikle denetlendi (100K `task` sınırı, `cov-d` 441.673 B, okuma yöntemi, §4 (d)).
- **Plan:** §8.2 (oturumlar, dilim seçenekleri, görevler, sekiz karar) "onay" ile; §1'e `4 · O1` (done) ve `4 · O2`, `4 · O3a`, `4 · O3b`, `4 · O4`, `4 · O5` (pending); §3'e Pencere 4 görev kimlikleri ve `C4`; §8'de oturum düzeni, dağılım, başlık, SUPERSEDED ve geçit satırları düzeltildi. Boru dışı satırlar artık `:183`, `:958`.
- **Ölçüm:** `W4O1P02` ledger §4 dilim baytları; `W4F05`'in [ÇIKARIM]'ı kapandı.
- **NEXT_PROMPT:** `4 · O2` için yeniden yazıldı; taslağı salt-okur bir scout yazdı, orkestratör betikle denetleyip `cp` ile yerine koydu.
- **Doğrulama:** kapanıştan önce üç dosyada bayt ve boru kontrolü ve kimlik taraması (Ek A.5) geçti; `git diff --stat` yalnız bu üç dosya. Doğrulayıcı yeniden çalıştırılmadı (`Planner-docs/` dokunulmadı).
- **Bağlam (Ek A.7):** ilk ölçüm 69k; birleşim sorusunda 108k; plan taslağından sonra 169k; form gönderilirken 201k; NEXT_PROMPT taslağı gönderildikten sonra 258k (`O1` tahmini ≈ 170k; fark zorunlu okuma ve edit yankıları).
- **Kapanış:** `Window 4 O1: plan for the twelfth audit` (yerel commit; push edilmedi). Sonraki oturum: Pencere 4 · O2 (`NEXT_PROMPT.md`; plan §8.2, §8.3).

**2026-11-17: Pencere 4 · O2 (omp, on dokuzuncu pencere).** Kapsam: `ORCHESTRATION_PLAN.md` §8.3 ve Ek A.8, 12. denetimin denetim kontratı (`CT4`). Bu girdi bir IMPL satırı değildir; ledger'a yazılmadı. Ledger'a, `Planner-docs/`'a, `docs/`'a ve cihaza dokunulmadı; reviewer çalışmadı.

- **Açılış (2026-11-17T11:50:59Z–11:54:00Z, salt-okur):** ağaç temiz; dal 89 commit, uç `Window 4 O1:` (tek eşleşme); `main` = `origin/main` = `081790f`, `origin/main..HEAD` 2; etiket yok; 355 dosya; `ls-remote` üç ref = `081790f`; dört depo 200; snapshot aynı. Plan §8.3 `W4O2OPN`.
- **Taban (11:53:50Z–11:54:00Z):** `NEXT_PROMPT.md` §7 tabanı tuttu; kimlik taraması `prose_mentions=26`, Ek A.8'den sonra 27 (A.8.1'in kimlik kuralı bir anahtarı düzyazıda anar).
- **Orkestrasyon şablonu:** kullanıcının şablonundaki yeni dal, plan onayında durma ve paralel uygulama adımları bu aşamaya uymuyor; plan kazanır (§0): dal sürer, plan `4 · O1`'de onaylandı, kontrat onay kapısı değil, reviewer'lar `4 · O3a`'da. Kapanış raporunda söylendi.
- **Kontrat (§8.3, Ek A.8):** çalışma başına dosya listesi ve ölçülmüş bayt (`W4O2P02`, 349.931–389.140 B); İngilizce ortak metin (zorunlu okuma yordamı, değerler, dönüş biçimi) ve altı çalışma bloğu; 32 S3 maddesi, eski §13'ün 13 kimliği, REV-3 P3 ve `[ÇIKARIM]` satırları tek sahipli dağıtıldı; S3-31 `AUD-W`'ye, S3-32 `GATE4`'e.
- **cov-d:** sekiz emekli ya da ertelenmiş dosya hafif okunur (başlıklar ve sayım; `Faz4.6` için ayrıca §1 ve §13); alt planlar 441.673 B yerine 224.903 B; bölme ve dördüncü reviewer gerekmedi.
- **`PAT4` (`W4O2P01`):** betik Ek A.8.3'te; 14 desen, kalibrasyon 164 isabet; S5 ve S6 (sır, kimlik değeri) 0.
- **NEXT_PROMPT:** `4 · O3a` için yeniden yazıldı; taslağı salt-okur bir scout yazdı, orkestratör betikle denetleyip `cp` ile yerine koydu.
- **Doğrulama:** kapanıştan önce üç dosyada bayt ve boru kontrolü ve kimlik taraması (Ek A.5) geçti; `git diff --stat` yalnız bu üç dosya. Doğrulayıcı yeniden çalıştırılmadı (`Planner-docs/` dokunulmadı).
- **Bağlam (Ek A.7):** ilk ölçüm 58k; tasarım ölçümlerinden sonra 181k; §8.3'ten sonra 237k; bu girdi yazılırken 245k (tahmin ≈ 220k; fark çalışma paketlerinin tasarımı).
- **Kapanış:** `Window 4 O2: audit contract for the twelfth audit` (yerel commit; push edilmedi). Sonraki oturum: Pencere 4 · O3a (`NEXT_PROMPT.md`; plan §8.3, Ek A.8).
