# NEXT_PROMPT - ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> Pencere 4 · O5'in kapanış commit'inde yazıldı. Aşama: **Pencere 5 · O0 - İlk Step 4 diliminin keşfi** (plan §1 `5+`, K7 = (a), plan §9). Öneri: `O0`+`O1` tek oturumda (§1). Özettir; nihai kaynak plan, ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`) için root tabanlı kamera özelleştirmesidir (`ishtar-cam-modes` v2.2, `ishtar-aon-fix` v1.1, AGC yapılandırması; AOSPA Android 15'te ölçüldü). ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Pencere 4 (12. denetim, ClaudeQB Step 3) bitti: Audit `PASS_WITH_WARNINGS`, P0 0, P1 0; kuyruk READY, baş `Faz10.1`. Pencere 5 ilk Step 4 dilimidir (plan §9; `run-step4.md`).

1. **Tek aşama:** plan §1'de `4 · O5` `done`, ilk `pending` `5+` (`:77`). Bu oturum yalnız Pencere 5 · `O0`'ı yürütür; kullanıcı açılışta birleşimi onaylarsa `O1`'i de (§1). `O2` ve sonrası bu oturumda başlamaz.
2. **Plan kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Dilimi kuyruk belirler:** hangi `Faz10.x` olduğu `O0`/`O1`'de Audit §12 kuyruğundan, Index sırasıyla seçilir (baş `Faz10.1`). Her dilim bir fazdır; küçük dilimler, toplam tahmin izin verirse, bir fazda birleşir (en çok dört; plan §9).
4. **Cihaz** (plan §3 Cihaz, §9): Pencere 4'ün "cihaza komut yok" kuralı Pencere 4 ile bitti. adb yalnız `platform-tools/adb.exe -s dc27e5d0`; betikler `ANDROID_SERIAL=dc27e5d0 MSYS_NO_PATHCONV=1` ile. Ajan yalnız salt-okunur komut çalıştırır. Kurulum, mod değiştirme, deklanşör, izin diyaloğu ve AGC tercihlerine yazma kullanıcıdadır ve onay ister. Her cihaz değişikliği `smoke.sh` ile önce ve sonra ölçülür; yalnız `BEGIN COMPARABLE`…`END COMPARABLE` karşılaştırılır. AOSPA A15 ölçümleri HyperOS 4'te varsayılmaz.
5. **Onay kapıları** (plan §0 adım 5, 9; kısa evet/hayır): `O0`+`O1` birleşimi (açılışta); `O1` sonunda plan onayı; FF; her push ayrı; cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler (`DEC-30`). Kapanış ve yerel commit beklenmedik durum yoksa sorulmadan atılır (§0 adım 4).
6. **Beklenmedik durum** (plan §0 adım 6): açılış ya da yayın §4 (a)-(c)'ye uymuyor; taban §7'den sapıyor; olgu planla ya da Ek A ile çelişiyor (silinmesi beklenen deponun 404'ü sayılmaz, kaydedilir); P0/P1 ya da güvenlik bulgusu; alt ajan sahiplik dışına taşıyor; planda olmayan eylem; aşamayı durduran araç arızası. Commit, FF ve push yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin.
7. **Plan dışı düzenleme yok:** alt plan, Index ve `Main-Planing.md` kullanıcıya sorulmadan düzenlenmez; gereken plan değişikliği sınırlı bir Step 2 düzeltmesine gider (Audit §14).
8. **Planlı bölme** (beklenmedik durum değil): bağlam 300k'yı geçerse yeni görev yok; kalan iş §1'de `in_progress` yazılır, bu dosya devam için yeniden yazılır (plan §0 adım 7, 9).

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/` ve `docs/` İngilizce.

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda ölç; 250k'dan sonra her turda. 300k'dan sonra yeni görev yok; kapanış 400k'dan önce biter. Hedef 240k.
- **`O0`+`O1` birleşimi** (plan §9; sınır 240k, §0 adım 9): ölçülen açılış okuma ve tabanla ≈ 80-115k (`4 · O4` 70,5k → taban sonrası 116k; `4 · O5` 80,9k); `O0` ≈ 12 × 6k ≈ 72k; `O1` ≈ 8 × 12k ≈ 96k; toplam ≈ 250-280k > 240k. Öneri, `4 · O1+O2` emsaliyle koşullu birleşim: `O0` kapanınca bağlam ≤ 140k ise `O1` aynı oturumda başlar, değilse `O1` ayrı oturumdur. Kullanıcı açılışta onaylar; `4 · O5` ölçümleri PROJECT_LOG §11'de.
- **Sonrası** (plan §9): `O2`-`O4` birleşimi dilimin `O1` planında onaylanır; `O5` ayrı oturum. Aşama tablosu oturum başına tahmin taşır.

## 2. Okuma sırası

Büyük dosyalar bütün okunmaz. Numaralar `4 · O5` kapanışınındır; içerikle doğrula.

1. Plan §0 (`:9`-`:44`), §1 (`:47`-`:77`), §3 (`:99`-`:125`; Geçitler `:111`-`:112`, Cihaz `:122`), §9 (`:918`-`:925`).
2. Ek A.5 (`:1077`-`:1122`), A.7 (`:1150`-`:1171`).
3. PROJECT_LOG §2.6 (`:228`-`:240`), §11'in son girdisi (`4 · O5`), §5.5 (kimlik değeri, tek cihaz penceresi).
4. `C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/references/handoffs/run-step4.md` (Step 4 sözleşmesi, durma kapıları).
5. `Planner-docs/Sub-Planing-Audit.md` §12 (`:409`-`:490`; yalnız `Faz10.x` satırları, kuyruk, insan kapıları) ve §14 (`:583`-`:623`; Step 4 istemi).
6. Ledger §4 `:69`-`:115`; `Faz10.1`-`10.5` `:111`-`:115` (CRLF).
7. Aday alt planlar (`Planner-docs/Faz-10-Plans/`): yalnız `O0`'ın seçtiği aralıklar; büyükse scout.

## 3. Mevcut durum

**Beklenen durum (`4 · O5` kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 94 commit. Uç ve kapanış: `Window 4 O5: final review and closing for the twelfth audit` (`git log --grep '^Window 4 O5:'` tek commit = uç). Etiket yok, 356 izlenen dosya. Plan §1: `4 · O5` `done`, ilk `pending` `5+` (`:77`).
- **Yayın:** iki geçerli durum (§4 b). FF, `RID`, push, `LSR` ve `DEL4` `C4`'ten sonraydı; sonuçlarını bu açılış kalıcı kaydeder.
- **GitHub:** son ölçüm PROJECT_LOG §11 (`4 · O5`). Origin `ahmetxa/ishtar_cam_modes` (özel). Silinecek üç depo (`DEC-30`, plan Ek A `:1000`): `ahmetxa/ishtar` (özel), `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar` (açık).
- **Audit** (`4 · O5` `FIX4` sonrası: 635 satır, 102.396 B, LF, NUL 0): `status: PASS_WITH_WARNINGS` (`:10`); §12 47 satır (34 COMPLETE, 7 SUPERSEDED, 1 DEFERRED `Faz4.6`, 5 READY_WITH_WARNINGS `Faz10.1`-`10.5`); kuyruk READY, baş `Faz10.1` (`F10.1-01`, `independent`); §13 P0 0, P1 0, P2 6, P3 49. `AUDIT12_FINDINGS.md` kanıttır: 509 satır, 111.618 B.
- **Açık P2'ler** (Audit §14): `AUDIT-FIX-22`, `-69`, `-70`, `-78`, `-80`, `-86`; P3 45 `open`, kabul `-25`, `-33`, `-94`, `-95`. Uyarıdır, engel değil; aleyhlerine iş yapılmaz.
- **Kuyruk** (Audit §12): `Faz10.1`; sonra `10.2`, `10.3`, `10.4` (`Faz10.1` notlarından sonra; `Faz10.4`'ün telefon yarısı `F10.2-04`'ten sonra); `Faz10.5` en son. Aynı anda tek cihaz penceresi (`-67`, `-71`).
- **Snapshot:** `Main-Planing.md` sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, CRLF; ledger 662 satır, CRLF, NUL 0 (`4 · O5` ölçümü). Snapshot değiştiyse dur (`run-step4.md`).
- **Kapasite:** `reviewer` ve `security-reviewer` 1M (`4 · O5`'te görüldü); `security-reviewer` kabuksuz; `task` ajanı 100K: büyük okumalı taslak `reviewer`'a verilir (`4 · O5`).
- **Açık gözlem (`4 · O5`, düzeltilmedi):** PROJECT_LOG'un `081790f`'ten önceki on satırında maskesiz `pref_48m_key` değeri (PROJECT_LOG §11, `4 · O5`); `AUDIT-FIX-81` sınıfı. Maskeleme ya da kural daraltması kullanıcı kararıdır.
- **Sürüm:** v2.2 / versionCode 13 (`DEC-29`). Kimlikler `IMPL-97`'den devam eder (plan §9).

## 4. Bu oturum: `5 · O0` (onaylanırsa `+ O1`)

Yazılanlar: plan §1 (Pencere 5 satırları), keşif envanteri, onaylanırsa plan bölümü; PROJECT_LOG §2.6 ve §11; bu dosya. Taslaklar `local://`'da kalır, commit'e girmez.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 4 O5: final review and closing for the twelfth audit`; `git log --grep '^Window 4 O5:'` tek commit = uç; `git rev-list --count HEAD` = 94; `git tag` boş; `git ls-files` = 356; plan §1'de `4 · O5` `done`, ilk `pending` `5+`.

**(b) Yayın** (iki durum da geçerli; hangisi olduğu kaydedilir):
- **(a) Push edildi:** `main` = `origin/main` = `integrate/impl-96` = `HEAD`; `git rev-list --count origin/main..HEAD` = 0; `git ls-remote origin` üç ref = `HEAD`.
- **(b) Push edilmedi:** `origin/main` = `081790f`; `origin/main..HEAD` = 7; `git ls-remote origin` üç ref = `081790f`; yerel `main` = `081790f` (FF reddedildi) ya da = `HEAD` (FF yapıldı, push reddedildi).
- Başka her durum beklenmedik durumdur. Kalıcı kayıt: PROJECT_LOG §11 ve plan §1'deki yeni Pencere 5 satırı (plan §9). (b)'de FF ve push yalnız kullanıcı isterse, ayrı onaylarla.

**(c) GitHub:** dört depo `gh api -i repos/ahmetxa/<ad>` (UTC; `gh` yolu §8). `ishtar_cam_modes` (özel) 200 olmalı; değilse beklenmedik durum. Silinecek üç depoda 404 = silinmiş: öngörülmüş değişiklik, kaydedilir (plan §0 adım 6); 200 de kaydedilir.

**(d) Bağlam:** Ek A.7 betiği açılışta, tabandan sonra, her alt ajan sonucundan sonra.

**(e) Taban** (§7): V1, `step2`, `step1`, `step3-preflight` `--strict`, `step3` (bayraksız ve `--strict`), V2, V3, kimlik taraması. Sapma beklenmedik durumdur.

**(f) `O0` keşif** (salt-okur):
- Audit §12/§14 ve ledger `:111`-`:115`: kuyruk, durumlar, ön koşullar, insan kapıları, ilgili P2/P3'ler.
- Aday dilimin alt planı: §9 uygulama sözleşmesi tablosu (yazma yolları), kabul kriterleri, doğrulama komutları, cihaz adımları; büyükse scout.
- Audit §14 destek eylemleri (ön koşul değil): Phase 10 metin bulguları için sınırlı Step 2 düzeltmesi, Main bulguları için Step 1 düzeltmesi, bir Index düzeltmesi. Kaydedilir; karar `O1`'de kullanıcının.
- Envanter oturum bitmeden depoya yazılır (plan §0 adım 8); önceki fazlarda fazın plan bölümüydü (§7.1, §8.1). Olgu kimliği önerisi (plan dışı): `W5OPN`, `W5F01`…

**(g) `O1` plan** (birleşim onaylıysa):
- Dilim kuyruktan, Index sırasıyla; aşama ve görev tablosu oturum başına tahminle (§0 adım 9); `O2`-`O4` birleşimi önerisi.
- Yazma yetkisi: alt planın §9 tablosundaki yollar, her biri tek sahip; ledger §4/§5 ve plan yalnız orkestratörde (plan §9).
- Kabul: alt planın kriterleri, §3 geçitleri, cihaz değişikliğinde smoke bracket; öngörü ve karar kuralı ölçümden önce yazılır.
- `Faz10.2` cihaz işinden önce kullanıcıyla kapatılır: `-69` (video başarısızlığı sonucu), `-70` (`F10.2-07` yalnız `setmode.sh` diff'i), `-78` (v2.2 kuruluyken kutucuk ve root izni yok); `Faz10.4` için `-80` (Audit §14).
- Görev kimliklerini ve faz kapanış commit'inin adını `O1` seçer. Plan onayı onay kapısıdır.

**(h) Kapanış** (plan §0 adım 4; beklenmedik durum yoksa sorulmadan):
- Plan §1: Pencere 5 satırı ve `5 · O0` (ya da `5 · O0+O1`) `done`, commit başlığıyla; `4 · O5` yayın sonuçları (FF, `RID`, push, `LSR`, `DEL4`) bu satırda ve PROJECT_LOG §11'de.
- PROJECT_LOG §2.6 yeniden; §11'e girdi (bağlam dahil). Bu dosya sıradaki aşama için ≤ 20 KB.
- Değişen dosyalarda bayt, boru, kimlik taraması (§7, Ek A.5).
- Yerel commit `eval`'deki `commit` ad alanıyla; değişen dosyaları açıkça `take` et. Başlık önerisi (plan dışı): `Window 5 O0-O1: discovery and plan for the first Step 4 slice` (yalnız `O0`: `Window 5 O0: discovery for the first Step 4 slice`). Sonra `git log --grep` ile hash; kullanıcıya `git show --stat`.
- FF ve push bu aşamada planlı değil; yalnız kullanıcı isterse, ayrı onaylarla.

**Kabul:** açılış, yayın ve taban tuttu ya da kaydedildi; envanter depoda; `O1` yürüdüyse plan "onay"lı; §1, PROJECT_LOG ve bu dosya güncel; commit yerel.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7-§8.3, ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| K1 `Kullanim.txt` | (b): v2.3'te düzeltilir | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K5/K6 üç depo | Silinecek; kullanıcı siler | `DEC-30` |
| K7 HyperOS 4 yönü | (a) modülü uyarla; Faz 7 ve 8 emekli | `DEC-32` |
| K9 50MP HAL | Hayır, şimdilik | `DEC-33` |
| `4 · O1+O2` | "evet" (2026-11-17); `O2` ayrı oturum | plan §8.2 |
| `4 · O1` planı | "onay" (2026-11-17); seçenek C, sekiz karar | plan §8.2 |
| `4 · O2` | Sorusuz kapandı (kontrat onay kapısı değil) | plan §1, §8.3 |
| `4 · O3a` | sec-a `partial`: (b) `reviewer` ile yeniden (2026-11-17) | plan §1, PROJECT_LOG §11 |
| `4 · O3b` | Sorusuz kapandı; P0 0, P1 0, P3 20 (2026-11-17) | plan §1, PROJECT_LOG §11 |
| `4 · O4` | Sorusuz kapandı; P0 0, P1 0, P2 6, P3 49 (2026-11-19) | plan §1, PROJECT_LOG §11 |
| `4 · O5` | Sorusuz kapandı; REV-5, SEC-D ve GATE4 sonuçları PROJECT_LOG §11 | plan §1, PROJECT_LOG §11 |
| Yayın | C3 push edildi (2026-11-16); C4 sonrası FF ve push sonucu PROJECT_LOG §11 (`4 · O5`); kaydı bu açılış yapar | plan §8.2, PROJECT_LOG §11 |
| `5 · O0+O1` | Açılışta sorulur (§1) | plan §0 adım 9, §9 |

## 6. Değişmezler: asla yapma

Madde 1-10 AOSPA A15'te ölçülmüş kurallardır; HyperOS 4'te ölçülmeden varsayılmaz, ihlal de edilmez (PROJECT_LOG §5).

1. AGC'de 50 MP'yi yeni kanıt olmadan yeniden açma (`DEC-14`).
2. Geniş RAW tablosunu daraltma (`IMPL-49`/`-50`).
3. `pref_camera_picturesize_back_key`'i doğrudan yazma; prefs'e `sed -i` yok.
4. `.agc` içe aktarma; tuzak temizliği yedeksiz yapılmaz (Ek A.2 `TRAP`).
5. Kamera yığınını yanlış sırada başlatma (istemci HAL'den önce).
6. `50mp` ile DCG/LN dışlamasını kaldırma.
7. Ölçmeden iddia; AOSPA kanıtını HyperOS 4'e, arka kamerayı ön kameraya genelleme.
8. Sapmayı sessizce yutma: ledger'a ya da yeni DEC'e yazılır, kullanıcı hükmeder.
9. Depoya ya da pakete `camera.qcom.so`, `*.keystore`, `*.jks`, `*.apk`, `*.zip`, `blobs/*.bin`, `candidates/*.bin` sokma.
10. `Faz4.1`/`Faz4.7`'yi canlandırma; `Faz4.6`'yı kararsız tamamlama; SUPERSEDED alt planları açma ya da yeniden koşma (Audit §14).
11. Onaysız cihaz eylemi: ajan yalnız salt-okunur komut; kurulum, mod değiştirme, deklanşör, izin diyaloğu kullanıcıda ve onaylı (plan §3 Cihaz). Aynı anda tek cihaz penceresi.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`; `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla.
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik ya da AGC tercih değeri yazma, geri kazanma; tarama yalnız sayı ve konum basar (PROJECT_LOG §5.5).
20. Sıcak noktayı alt ajana yazdırma: ledger, `Main-Planing.md`, Index, Audit, `AUDIT12_FINDINGS.md`, Ontology, Comprehension, toolchain belgesi, `CHANGELOG.md`, sürüm yerleri, manifest, `.gitignore`, `.gitattributes`, `snapshots/`, plan, PROJECT_LOG ve git (plan §3).
21. Satır sonu dönüştürme: ledger, `Main-Planing.md`, `Autopsy.md` CRLF, gerisi LF; CRLF dosyada yazımdan sonra baytla doğrula.
22. `python` ya da `python3`: yalnız `py -3`.

## 7. Doğrulama komutları ve taban değerler

```bash
V=C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py
py -3 $V --root . --mode all
py -3 $V --root . --mode step1 --strict
py -3 $V --root . --mode step2 --strict
py -3 $V --root . --mode step3-preflight --strict
py -3 $V --root . --mode step3
py -3 $V --root . --mode step3 --strict
py -3 $V --root . --mode step4 --strict
py -3 scripts/build-release.py --self-test
```

| Kontrol | Taban (`4 · O5` `GATE4`, PROJECT_LOG §11; plan §3 Geçitler) |
|---|---|
| `step2`, `step1`, `step3-preflight` `--strict` | Bulgu yok, çıkış 0 |
| V1 `--mode all` | Çıkış 0; yalnız `warning=step4_has_nonblocking_warnings=P2:6,P3:49`; `audit_status=PASS_WITH_WARNINGS`; `p0_findings=0`, `p1_findings=0`; `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; `secret_findings=0` |
| `step3` ve `step3 --strict` | Bayraksız çıkış 0; `--strict` çıkış 1, yalnız `strict_warning=step4_has_nonblocking_warnings` |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning` (`execution_queue_state=READY`, baş `Faz10.1`); çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=28` → PASS; `prose_mentions` artabilir |
| Boru ve bayt | Boru dışı yalnız plan `:183`, `:1019` ve ledger satırları; ledger ve `Main-Planing.md` CRLF, öteki LF; NUL yalnız Ontology'de (2); Audit LF, NUL 0 |

- Step 4'te önce dilimin hedefli doğrulaması, sonra bu geçitler (`run-step4.md`; plan §9).
- Kimlik taraması Ek A.5 betiğiyle, kökten `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: sürüm prosedürü dışında çalıştırılmaz.

## 8. Bilinen tuzaklar

- **omp:** Ek A.7 betiği JS'tir (`eval`); eval'in Python arka ucu yok. `bash` politikası `grep`'i engelledi: arama `grep` aracıyla ya da `awk` ile.
- **Scout'lar kabuksuz (`4 · O4`):** `wc`/`awk` çalıştıramadılar; sayım okuma aracıyla. Sayım isteyen görev bunu baştan belirtir.
- **`reviewer`** `bash`'te `grep` kullanamaz, `grep` aracını kullanır. **`security-reviewer`** kabuksuz: girdi `local://` dosyasıyla verilir ya da `reviewer` kullanımı kullanıcıya sorulur.
- **Okuma aracı:** 768 karakteri aşan satırları keser, büyük dosyada blok atlar. Tek satır için `:raw:N-N`.
- **Ledger:** satırlar 1-9 KB; değişen satır baştan sona yazılır, sonra difflib ile "yalnız ekleme" kontrolü; CRLF baytla doğrulanır (plan §3 Bayt).
- **Ontology'de 2 NUL:** `grep` orada sessizce sonuç vermeyebilir.
- **Boru sayımı:** ham `|` (kaçışlı dahil) sayılır; plan `:183`, `:1019` ve ledger satırları boru dışıdır.
- **AGC değerleri:** ajanlar tercih değerini kopyalayabilir: `[value withheld]` ile maskele; `pref_*=` taramasında maskesiz eşleşme `0` olmalı.
- **`smoke.sh`:** `-s` seçeneği yok, seri `ANDROID_SERIAL` ile; `-o` yalnız ad alır (`-o snapshots/NAME` dosya yazmaz; Ek A.6 `SMK-O`).
- **`local://` oturumlar arasında kaybolur** (§0 adım 8): envanter oturum bitmeden depoya.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe`.
- **`--grep` satır başına bağlanır** (`'^Window 4 O5:'`) ve gövde satırlarını da eşler.
- **Commit:** `eval`'deki `commit` ad alanıyla (`draft`, `take`, `commit`); `git add`/`git commit` yok. `cp` ile konanlar dahil değişen dosyaları açıkça `take` et.
- **`.gitattributes`:** `* -text` bayt korur, `*.md` için `eol=lf` yok: LF baytla doğrulanır.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış (§4 a), yayın durumu (§4 b; (a) mı (b) mi) ve dört depo (§4 c).
3. Bağlam (§4 d) ve taban (§4 e).
4. Kısa Türkçe "hazırım" özeti (ölçülenler, yayın, depolar) ve tek soru: `O0`+`O1` birleşimi, tahminiyle (§1).
5. §4 (f) `O0` keşfi; birleşim onaylıysa (g) `O1` planı ve plan onayı; sonra (h) kapanış.

---
