# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> 2026-11-16'da, Pencere 3 · O4'ün kapanış commit'inde yazıldı. Aşama: **Pencere 3 · O5 — son inceleme ve kapanış (`REV-4`, `SEC-C`, `FIX3`, `C3`, FF, push; plan §7.2)**. Bu bir özettir; nihai kaynak plan (`ORCHESTRATION_PLAN.md`), ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC yapılandırması; hepsi AOSPA Android 15'te ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Koşu 21: Step 1 (`3 · O2a`; Faz 7 ve 8 emekli, "ClaudeQB Phase 10"), kontrat (`3 · O2b`), `Faz10.1`–`Faz10.5` (`3 · O3a`/`O3b`; 47 alt plan); `3 · O4` ledger, Index, Ontology, Comprehension, toolchain ve PROJECT_LOG §5.5'i yazdı, `GATE3` geçti.

1. **Tek aşama:** plan §1'deki ilk `pending` aşama satırı `3 · O5`'tir: `REV-4` ∥ `SEC-C` → `FIX3` → `C3` → FF (onay) → push (onay) → `LSR`, `RID`. Bu oturum yalnız onu yürütür. Ardından Pencere 3 `done`; sıradaki aşama Pencere 4 · `O0` (12. denetim, plan §8), yeni oturumda. Aşama atlanmaz.
2. **Plan kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** olgular 2026-11-13 ölçümü ve 2026-11-15 `PRB` ölçümüdür (plan §7.1 `W3P01`–`W3P04`). Bu aşama cihaza komut göndermez.
4. **Onay kapıları** (plan §0 adım 5; kısa evet/hayır): FF; her push ayrı; cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler. `C3` kapanışı ve yerel commit'i, beklenmedik durum yoksa sorulmadan (§0 adım 4, adım 6).

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/` (ledger dahil) ve `docs/` İngilizce (Ek A.3).

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): bağlamı Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok: işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, bu dosya, commit); kapanış 400k'dan önce biter.
- **Tahmin:** `3 · O5` ≈ 215k (35k + 30 × 6k). Kalibrasyon: PROJECT_LOG §11, `3 · O4` girdisi.
- **Hijyen:** 20 KB'tan büyük okuma scout'a; alt ajan ≤ 4 KB döner, ayrıntıyı `local://`'a yazar. Büyük dosya `grep` ve dar `:N-M` ile; aynı aralık iki kez okunmaz. Satırlar ≤ 600 bayt; `todo` ≤ 8 madde.
- **Beklenmedik durum** (plan §0 adım 6): kapanış, commit ve bu dosyanın yeniden yazımı yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin.

## 2. Okuma sırası

Plan, PROJECT_LOG, ledger, Index, Ontology ve Comprehension bütün okunmaz; bölüm başları `grep '^##'` ile.

1. Plan §0, §1 ve §3 (geçitler, Gizlilik, Git).
2. Plan §7.2 dar aralıkla: "Oturumlar" `3 · O5` satırı (`:571`), "Görevler" `REV-4`…`RID` (`:592`–`:595`), "Ara durumlar ve geçitler" (`:612`–`:626`), "Sıcak noktalar".
3. Plan §6.3–§6.4 (`:326`–`:363`): `2 · O5` emsali (SEC/REV girdileri, FF, `RID`, PUSH, `LSR`).
4. Plan §7.1 `W3P` satırları (`grep '^| W3P'`); §7 "Açılışta ayrıca" (`:439`–`:441`; silme yerleri); §10 `:812`–`:817`; §8 (devir için).
5. Ek A.5 (push kuralları, betik), A.7; PROJECT_LOG §2.6, §5.5 ve §11'in `3 · O4` girdisi.

## 3. Mevcut durum

**Beklenen durum (3 · O4 kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 86 commit. Uç: `Window 3 O4 follow-up: record line shifts and FIX3 items` (onaylı takip); kapanış `Window 3 O4: integration and gates for planning run 21` (`git log --grep '^Window 3 O4:'`). Etiket yok, 355 izlenen dosya.
- **`main` = `origin/main`** = `6632a18`. `origin/main..HEAD` = 10 (`3 · O0` kapanışı ve takip commit'i, `3 · O1`, `3 · O2a`, `3 · O2b`, `3 · O3a` ve takip commit'i, `3 · O3b`, `3 · O4` ve takip commit'i); push edilmedi.
- **`git ls-remote origin`:** `HEAD`, `main`, `integrate/impl-96` = `6632a18`.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez); silinecek üç depo (`DEC-30`): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. 2026-11-16T10:17:27Z–10:17:31Z'de dördü de 200 (404 = silinmiş).
- **`Main-Planing.md`** (değişmedi): sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, 77.019 bayt, CRLF, NUL 0, 10 faz. Alt plan 47.
- **Ledger:** 653 → 662 satır, CRLF, NUL 0. §2 koşu 21; §3 `SNAP-2026-11-15-MAIN`, `SNAP-2026-11-16-SUBPLANS`; §4 47 satır: 34 `verified`, 1 `implemented` (`Faz4.6`), 5 `planned` (`Faz10.1`–`Faz10.5`), 7 `superseded`; `Faz6.2` notu; §7 notu; §8 `DEC-33`, `DEC-32` notu.
- **Öteki dosyalar:** Index 443 satır, LF; Ontology 453, LF, NUL 2 (`:313`, `:316`; değişmez 10, 11); Comprehension 176, LF (`CQ-13`, `EV-20`); toolchain 246, LF (Hetzner notu); PROJECT_LOG §5.5 (kimlik değeri kuralı; `Faz10.2`–`Faz10.4` için tek cihaz penceresi).
- **Plan:** §1'de `3 · O4` `done`; §3 `:102` yeni taban; §10 `:812`–`:815` (`3 · O4`'ün üç kapsam dışı bulgusu, 12. denetim), `:816` kayma haritası, `:817` `FIX3` maddeleri. Boru tabanı `:174`, `:850`.
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` v1.9 içeriğinde (`DEC-29`).
- **Telefon** (plan §7.1, PROJECT_LOG §2.3): HyperOS 4 (`OS4.0.0.44.WMACNXM`), SukiSU-Ultra v4.3.0-r1, metamodül yok; HAL AOSPA'dan farklı, sensör = `EXPECT_MD5`; proje modülleri ve kutucuk yok; AGC yamasız V9.6, 10 tuzak.
- **Araçlar:** `3 · O4`'ün `o4.py`/`fix.py` betikleri ve `local://` taslakları taşınmaz; `%TEMP%/idscan.py` duruyor.

## 4. Bu oturum: `3 · O5`

İncelemeler salt-okurdur. Yazılanlar: `FIX3` düzeltmeleri; kapanışta plan §1 (gerekirse §10), PROJECT_LOG §2.6 ve §11 ve bu dosya; sonra git.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 3 O4 follow-up: record line shifts and FIX3 items`; `git rev-list --count HEAD` = 86; `git rev-list --count origin/main..HEAD` = 10; `main` ve `origin/main` = `6632a18`; `git tag` boş; `git ls-files` = 355; `git ls-remote origin` (§3). Plan §1'de ilk `pending` = `3 · O5`.
Snapshot: `Main-Planing.md` §3'teki gibi; ledger 662 satır, CRLF, NUL 0; Index 443, Ontology 453 (NUL 2), Comprehension 176, toolchain 246, hepsi LF. Kapsam: `git diff --stat 6632a18..HEAD` ve `git log -p 6632a18..HEAD` baytı (parçalama için). Tutmayan her şey beklenmedik durumdur.

**(b) GitHub ölçümü:** dört depo için `gh api -i repos/ahmetxa/<ad>` (UTC; ilk satır HTTP durumu); açılışta, `C3`'ten önce (emsal §6.4) ve `RID` olarak push'tan sonra. `ahmetxa/ishtar_cam_modes` 200 değilse beklenmedik durum.
Üç depodan biri 404 ise beklenmedik durum değildir (§0 adım 6), kaydedilir: PROJECT_LOG'un silme cümleleri (yerler plan `:441`; numaralar eski, içerikle bulunur), sonuç §2.6 ve §11'e. Ledger `DEC-30` notunu plan yalnız `I3a`-7'ye (`3 · O4`) verir; `3 · O5`'te yazarı yok: kullanıcıya söylenir.

**(c) Bağlam ölçümü:** Ek A.7 betiği (`eval`), oturum başında ve her alt ajan sonucundan sonra.

**(d) Taban:** `GATE3` değerleri (§7): `step2`, `step1`, `step3-preflight` `--strict`, V1–V3 ve kimlik taraması açılışta bir kez. Sapma beklenmedik durumdur.

**(e) `REV-4` ∥ `SEC-C`** (salt-okur; aynı anda en çok dört ajan, plan §3):
1. **`REV-4`** (reviewer, parçalı): Pencere 3 diff'i `6632a18..HEAD`; doğruluk, kontrat (plan §7.3), doğrulayıcı tuzakları (§7.2 "Ara durumlar"), eksik kanıt. Öneri parçalar: `Main-Planing.md` + `Faz-10-Plans/`; ledger, Index, Ontology, Comprehension, toolchain; plan, PROJECT_LOG, `NEXT_PROMPT.md`. Boyut (a)'daki ölçümle; büyük parça ikiye bölünür.
2. **`SEC-C`** (security-reviewer): `git log -p --reverse --no-color --format=fuller 6632a18..HEAD` (ara hâller, commit üstverisi) ve plan §7.1 `W3P` satırları. Ölçüt: sır, Luhn adayı, `dc27e5d0` dışında seri numarası, sunucu adresi yok.
3. **Görev metni:** aralık ya da dosyalar, olgu kaynakları (plan §7.1–§7.3, ledger), kimlik kuralı (PROJECT_LOG §5.5), dönüş bloğu (plan §3). Bulgular `local://`'a; dönüş ≤ 4 KB (yol, bayt, P0–P3 sayıları, bulgu başına `dosya:satır`, `open_issues`).
4. **Yönlendirme:** P0/P1 beklenmedik durumdur (§0 adım 6). P2/P3'te kapsamı kullanıcı formla seçer (emsal `3 · O3a`/`O3b`: "hepsi"). Kapsam dışı bulgu plan §10'a (12. denetim).

**(f) `FIX3`:** `task` yalnız sıcak nokta dışındaki dosyalarda (örneğin `docs/`, `README.md`), dosya başına bir ajan. Sıcak noktalar (değişmez 20 ve `Faz-10-Plans/`) orkestratörde: taslak gerekirse salt-okur scout'ta; ledger ve Ontology `py -3` betiğiyle (§8), öteki `edit` ile. Bir şey değiştiyse geçitler yeniden: `GATE3` değerleri, bayt, boru, kimlik taraması.
Bilinen `FIX3` maddeleri (plan §10 `:817`; kullanıcı kararı "takip", 2026-11-16): `Faz10.5` `:33` ve `:65`'teki atıf `PROJECT_LOG.md:857-871` olur; PROJECT_LOG §4 başlığı `DEC-01 … DEC-33`; `DEC-33`'ü sonraki boş numara sayan ve K9'u açık gösteren satırlara tarihli not (yerler plan §10'da).

**(g) `C3`** (beklenmedik durum yoksa sorulmadan):
- Başlık `Window 3:` ile başlar, fazı adlandırır; plan başlık tanımlamaz, emsal C2 `Window 2: project log sweep and handoff for planning run 21`. Öneri: `Window 3: planning run 21 and handoff for the twelfth audit`.
- Plan §1'de `3 · O5` ve Pencere 3 satırları `done`, commit başlıkla anılır (`git log --grep '^Window 3:'`). PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır, §11'e girdi.
- Bu dosya Pencere 4 · `O0` girişi olarak ≤ 20 KB yeniden yazılır (plan §0 adım 4, §8): 12. denetim keşfi; FF, push ve `LSR` sonucu açılışta `git ls-remote origin` ile doğrulanıp kaydedilir.
- Bayt, boru ve kimlik taraması (§7); yerel commit; kullanıcıya `git show --stat` özeti.

**(h) FF, push, `LSR`, `RID`** (`C3`'ten sonra, aynı oturumda):
1. **FF (onay):** yalnız `git fetch . integrate/impl-96:main`; `main` = `C3`. İleri sarılamazsa beklenmedik durum.
2. **Kimlik taraması** (Ek A.5): FF'den sonra, push'tan hemen önce; bütün ref'ler ve izlenen dosyalar; yalnız sayılar.
3. **PUSH (onay):** yalnız `git push origin main integrate/impl-96`; `--all`/`--mirror` ve GitHub MCP asla. Kimlik doğrulama hatası beklenmedik durumdur.
4. **`LSR`:** `git ls-remote origin`; `HEAD`, `main`, `integrate/impl-96` = yerel `C3`. **`RID`** (plan §7.2 `:595`): dört deponun ölçümü ((b)). Sonuçlar sohbette; Pencere 4 açılışı yeniden doğrular ve kaydeder (emsal `2 · O5`). Ek kayıt commit'i yalnız onayla (plan §3 Git).

**Kabul:** `REV-4`, `SEC-C` bitti, P0/P1 yok ya da çözüldü; seçilen P2/P3 düzeltildi, kalanlar §10'da; geçitler tabanda; `C3` yerel; FF ve push onaylı; `ls-remote` hash'leri eşit; §1'de `3 · O5` ve Pencere 3 `done`.

**İnceleme:** `REV-4` ∥ `SEC-C` aşamanın kendisidir; `FIX3` sonrası teyit önerilebilir. P0/P1 → §0 adım 6.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7, §7.2, §7.3 ve ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| K1 `Kullanim.txt` | (b): v2.3'te düzeltilir (soru 4) | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K5/K6 üç depo | Silinecek; kullanıcı siler; ölçülür | `DEC-30` |
| K7 HyperOS 4 yönü | (a) modülü uyarla; (i) "ClaudeQB Phase 10", Faz 7 ve 8 emekli (soru 5) | `DEC-32` |
| K9 50MP HAL | Hayır, şimdilik; sensör katmanı sürer (soru 1) | `DEC-33` (yazıldı) |
| Sekiz soru | Yanıtlandı (2026-11-15); soru 7: Hetzner düzeltmeleri koşu 21'de; soru 8: sınırlı Step 2, Step 1.5 atlandı | plan §7 |
| Pencere 3 planı | Onaylandı (2026-11-15, form "onay") | plan §7.2 |
| Step 1 metni | Onaylandı (2026-11-15T14:10Z, form "onay"; C01–C03 dahil) | `Main-Planing.md` |
| Step 2 kontratı | Onaylandı (2026-11-15, form "onay"; dal sürer) | plan §7.3 |
| `3 · O3a` planı | Onaylandı (2026-11-15, form "onay"); Index `edit`, REV ∥ SEC | plan §7.2 |
| `3 · O3a` incelemesi | Düzeltmeler "hepsi" (2026-11-16, form) | plan §7.3 `:718`, §10 |
| `3 · O3b` planı | Onaylandı (2026-11-16, form "onay"; REV ∥ SEC) | plan §1 |
| `3 · O3b` incelemesi | P1 3, P2 4, P3 9; düzeltmeler "hepsi" (2026-11-16, form) | plan §7.3 `:719`–`:720`, §10 |
| `3 · O4` planı | Onaylandı (2026-11-16, form "onay"); iki PROJECT_LOG kuralı "yeni §5.5" | plan §1, PROJECT_LOG §5.5 |
| `3 · O4` incelemesi | Teyit incelemesi "ekle" (2026-11-16, form); P0 0, P1 0, P2 2, P3 5 aşamada düzeltildi | plan §10 `:812`–`:815` |
| `3 · O4` takibi | Kaydet (2026-11-16, form "takip"): kayma haritası ve `FIX3` maddeleri; içerik `3 · O5`'te | plan §10 `:816`–`:817` |
| Snapshot | Step 2 durmaz; etkin plan bugünkü `Main-Planing.md`; satırlar yazıldı (`I3a`-2) | plan §7.3, ledger §3 |
| Atıf | Phase 10 ve emeklilikler koşu 21'in seçimi; `DEC-28` Faz 7/8'i, `DEC-32` uyarlamayı anar | ledger §8 |
| Yayın | Dal `integrate/impl-96` sürer; C2 ve takip commit'i push edildi; Pencere 3'ün on commit'i yerel; FF ve push bu aşamada, ayrı onaylarla | plan §1, §7.2 |

## 6. Değişmezler — asla yapma

Madde 1–10 AOSPA A15'te ölçülmüş modül ve AGC kurallarıdır; HyperOS 4'te ölçülmeden varsayılmaz, ihlal de edilmez (PROJECT_LOG §5).

1. AGC'de 50 MP'yi yeni kanıt olmadan yeniden açma (`DEC-14`).
2. Geniş RAW tablosunu daraltma (`IMPL-49`/`-50`).
3. `pref_camera_picturesize_back_key`'i doğrudan yazma; prefs'e `sed -i` yok.
4. `.agc` içe aktarma; tuzak temizliği yedeksiz yapılmaz (Ek A.2 `TRAP`).
5. Kamera yığınını yanlış sırada başlatma (istemci HAL'den önce).
6. `50mp` ↔ DCG/LN dışlamasını kaldırma.
7. Ölçmeden iddia; AOSPA kanıtını HyperOS 4'e, arka kamerayı ön kameraya genelleme.
8. Sapmayı sessizce yutma: ledger'a ya da yeni DEC'e yazılır, kullanıcı hükmeder.
9. Depoya ya da pakete `camera.qcom.so`, `*.keystore`, `*.jks`, `*.apk`, `*.zip`, `blobs/*.bin`, `candidates/*.bin` sokma.
10. `Faz4.1`/`Faz4.7`'yi canlandırma; `Faz4.6`'yı kararsız tamamlama.
11. Cihaza komut: yalnız salt-okur ve plan §7.2'deki `PRB1`–`PRB10`; `3 · O5` hiç göndermez. Fiziksel eylemler kullanıcıda ve onaylı.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`, `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla.
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik değeri yazma ya da geri kazanma; tarama yalnız sayı ve konum basar.
20. Sıcak noktayı alt ajana yazdırma: ledger, `Main-Planing.md`, Index, Audit, Ontology, Comprehension, toolchain belgesi, `CHANGELOG.md`, sürüm yerleri, manifest, `.gitignore`, `.gitattributes`, `snapshots/`, plan, PROJECT_LOG ve git (plan §3, §7.2).
21. Satır sonu dönüştürme: ledger, `Main-Planing.md`, `Autopsy.md` CRLF, gerisi LF; CRLF dosyada yazımdan sonra baytla doğrula.
22. `python` ya da `python3`: yalnız `py -3`.

## 7. Doğrulama komutları ve taban değerler

```bash
V=C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py
py -3 $V --root . --mode all
py -3 $V --root . --mode step1 --strict
py -3 $V --root . --mode step2 --strict
py -3 $V --root . --mode step3-preflight --strict
py -3 $V --root . --mode step4 --strict
py -3 scripts/build-release.py --self-test
```

| Kontrol | Taban (`GATE3`, 2026-11-16T20:30Z) |
|---|---|
| `step2`, `step1`, `step3-preflight` `--strict` | Bulgu yok, çıkış 0 |
| V1 `--mode all` | Yalnız `warning=step4_has_nonblocking_warnings=P2:1,P3:9`; `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning`; çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=24` → PASS; `prose_mentions` artabilir |
| Boru ve bayt | Plan'da boru dışı yalnız `:174`, `:850`; ledger ve `Main-Planing.md` CRLF, öteki LF; NUL yalnız Ontology'de (2) |

- Kimlik taraması: `%TEMP%/idscan.py`, depo kökünde `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- `python` Store stub'ıdır; `SKILL.md`'deki `python3` burada çalışmaz.
- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` politikası `cat`, `head`, `tail`, `grep` ve `find`'ı engeller: `awk`, `read`/`grep`/`glob` araçları ya da `py -3`; `<(…)` çalışmaz.
- **Ledger ve Ontology** yalnız `py -3` betiğiyle, bayt olarak yazılır (`edit` satır sonunu ve NUL'u bozabilir); `difflib` ile yalnız ekleme kanıtlanır; değişiklik sondan başa uygulanır.
- **600 bayt sınırı** orkestratörün kendi satırlarını bağlar; eski metni koruyan Index satırları onu aşabilir.
- **Çapa numaraları** çoğu yerde `3 · O4`'ten öncedir (ledger 653, Index 426, PROJECT_LOG 1228, toolchain 242; kayma haritası plan §10 `:816`); her atıf içerikle doğrulanır.
- **Ledger §4 doğrulayıcısı:** ters tırnaklı yol (V:828), boş satırla ayrılmış satır (V:420), dosyasız alt plan (V:830) kırmızıdır. §2, §3 satırlarını V okumaz (V:93-103).
- **Ontology**'de 2 NUL (`:313`, `:316`): `grep` boş dönebilir (`AUDIT-FIX-22`).
- **Alt ajanlar:** scout'un kabuğu yok, `local://`'a yazar (ilk yazımın baytına bak; `local://` taşınmaz); `task` 100K bağlamlı: plan ya da PROJECT_LOG bütün verilmez. 429 ya da 402 ile duran ajan canlanmaz: görevi ortak bağlamla taze gönder.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok, `DEC-30`).
- **`--grep` satır başına bağlanır** (`'^Window 3 O4:'`, `'^Window 3:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`d = await commit.draft()`, `await d.take(...)`, `await d.commit(...)`); `git add`/`git commit` yok. Değişen dosyaları açıkça `take` et.
- **Emekli Faz 7/8:** satırları, bölümleri ve dosyaları yerinde kalır (silmek `--strict`'te `extra_phase_folder_without_main_phase`); Index'te üstü çizilir, silinmez.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri, snapshot ve kapsam (§4 a); plan §1'de ilk `pending` `3 · O5`.
3. GitHub (§4 b), bağlam (§4 c), `GATE3` tabanı (§4 d).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin, bu oturumun yalnız `3 · O5` olduğu, `REV-4` parça önerisi; FF ve push'un ayrı onay isteyeceği.
5. §4 (e) `REV-4` ∥ `SEC-C`, (f) `FIX3`, (g) `C3`, (h) FF, push, `LSR`, `RID`.

---
