# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> 2026-11-16'da, Pencere 3 · O3b'nin kapanış commit'inde yazıldı. Aşama: **Pencere 3 · O4 — entegrasyon ve geçitler (`I3a`, `I3b`, `GATE3`; plan §7.2, §7.3)**. Bu bir özettir; nihai kaynak plan (`ORCHESTRATION_PLAN.md`), ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC yapılandırması; hepsi AOSPA Android 15'te ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Koşu 21: Step 1 (`3 · O2a`) Faz 7 ve 8'i emekli etti, işi "ClaudeQB Phase 10"a taşıdı; `3 · O2b` kontratı (§7.3) yazdı; `3 · O3a` `Faz10.1`–`Faz10.3`'ü, `3 · O3b` `Faz10.4`–`Faz10.5`'i yazdı (47 alt plan). Ledger koşu 21'i henüz kaydetmedi.

1. **Tek aşama:** plan §1'deki ilk `pending` aşama satırı `3 · O4`'tür: ledger, Index, Ontology ve Hetzner satırları (`I3a`, `I3b`), ardından `GATE3`. Bu oturum yalnız onu yürütür; `3 · O5` (son inceleme, FF, push) sonraki oturumdur. Aşama atlanmaz.
2. **Dosya kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** olgular 2026-11-13 ölçümü ve 2026-11-15 `PRB` ölçümüdür (plan §7.1 `W3P01`–`W3P04`). Bu aşama cihaza komut göndermez.
4. **Onay kapıları** (plan §0 adım 5): FF ve her push (`3 · O5`); cihaz eylemi; AGC tercihlerine yazma. `3 · O4`'ün kullanıcı kapısı yok; geçidi `GATE3`'tür. Hetzner düzeltmeleri soru 7'de onaylandı (plan §7). Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/` (ledger dahil) ve `docs/` İngilizce (Ek A.3).

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): bağlamı Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok: işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, bu dosya, commit); kapanış 400k'dan önce biter.
- **Tahmin:** `3 · O4` ≈ 233k (35k + 33 × 6k). Kalibrasyon (`3 · O3b`): açılış 64k, plan formu 98k, taslaklar 151k, inceleme 189k, düzeltme turu 207k. Ledger satır taslakları scout'larda; ledger ve Ontology `py -3` betiğiyle, öteki dosyalar `edit` ile.
- **Hijyen:** 20 KB'tan büyük okuma scout'a; scout ≤ 4 KB döner, ayrıntıyı `local://`'a yazar. Büyük dosya `grep` ve dar `:N-M` ile; aynı aralık iki kez okunmaz. Satırlar ≤ 600 bayt; `todo` ≤ 8 madde.
- **Beklenmedik durum** (plan §0 adım 6): kapanış, commit ve bu dosyanın yeniden yazımı yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin.

## 2. Okuma sırası

Plan, PROJECT_LOG, ledger, Index, Ontology ve Comprehension bütün okunmaz; bölüm başları `grep '^##'` ile.

1. Plan §0, §1 ve §3.
2. Plan §7.3: baştaki snapshot kararı, `:718`–`:720` notları, "`3 · O4` hedef tablosu" ve "Dokunulmayanlar".
3. Plan §7.2 dar aralıkla: "Oturumlar" `3 · O4` satırı, "Görevler" `I3a`, `I3b`, `GATE3`, `W3F28` açık konuları, "Ara durumlar ve geçitler" (`:612`–`:624`), "Sıcak noktalar".
4. Plan §7: Ontology maddesi, soru 7 yanıtı, §2 K9 (`DEC-33`); `W3F13`, `W3F14`, `W3F19`, `W3F28` (`grep '^| W3F'`); §10 `:811`.
5. Ek A.4 (ledger biçimi; numaralar 644 satırlık ağacın), A.6 `LSH` ve `LMAP` (653 satır), A.7; PROJECT_LOG §2.6 ve §5; Ek A.5 betiği geçitte.

## 3. Mevcut durum

**Beklenen durum (3 · O3b kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 84 commit. Uç: `Window 3 O3b: Step 2 drafts 10.4-10.5 for planning run 21` (`git log --grep '^Window 3 O3b:'`). Etiket yok, 355 izlenen dosya.
- **`main` = `origin/main`** = `6632a18`. `origin/main..HEAD` = 8 (`3 · O0`–`3 · O3b` kapanışları ve iki takip commit'i); push edilmedi; FF ve push `3 · O5`'te, ayrı onaylarla.
- **`git ls-remote origin`:** `HEAD`, `main`, `integrate/impl-96` = `6632a18`.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez); silinecek üç depo (`DEC-30`): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. 2026-11-16T08:40:19Z–08:40:22Z'de dördü de 200; ajan yalnız ölçer (404 = silinmiş).
- **`Main-Planing.md`** (`3 · O2a`'dan beri aynı): sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, 77.019 bayt, CRLF, NUL 0, 10 faz.
- **Plan:** `3 · O3b` §7.3'e `:719`–`:720` notlarını (`CPb` harita kararları), §10'a `:808`–`:811` bloğunu ekledi; §1'de `3 · O3b` `done`. Boru tabanı `:174`, `:844`.
- **Alt planlar:** 47 (Phase 10 = 5, `Planner-docs/Faz-10-Plans/`). Snapshot kimlikleri `SNAP-2026-11-15-MAIN`, `SNAP-2026-11-16-SUBPLANS`.
- **Index:** 426 satır, LF. Phase 10 girdileri `:165`–`:169`, öncelik maddesi 16 `:190`, sayılar `:303` (toplam 47).
- **Ledger:** 653 satır, CRLF, NUL 0; Pencere 3'te dokunulmadı; çapalar Ek A.6 `LMAP`. §4'te 42 satır: 34 `verified`, 3 `implemented` (`Faz4.6`, `Faz6.1`, `Faz8.1`), 3 `planned` (`Faz7.2`, `Faz7.3`, `Faz8.3`), 2 `superseded` (`Faz4.1`, `Faz4.7`).
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` v1.9 içeriğinde (`DEC-29`).
- **Telefon** (plan §7.1, PROJECT_LOG §2.3): HyperOS 4 (`OS4.0.0.44.WMACNXM`), SukiSU-Ultra v4.3.0-r1, metamodül yok; HAL AOSPA'dan farklı, sensör = `EXPECT_MD5`; proje modülleri ve kutucuk yok; AGC yamasız V9.6, 10 tuzak.

## 4. Bu oturum: `3 · O4`

Yalnız ledger, Index, `Planner-docs/Project-Ontology.md`, `Planner-docs/Project-Comprehension.md`, `docs/reverse-engineering-toolchain.md` ve PROJECT_LOG §5 yazılır (kapanış dosyaları (i)'de). `Main-Planing.md`, alt planlar, Audit ve öteki `docs/` yazılmaz.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 3 O3b: Step 2 drafts 10.4-10.5 for planning run 21`; `git rev-list --count HEAD` = 84; `git rev-list --count origin/main..HEAD` = 8; `main` ve `origin/main` = `6632a18`; `git tag` boş; `git ls-files` = 355; `git ls-remote origin` (§3). Plan §1'de ilk `pending` = `3 · O4`.
Snapshot: `Main-Planing.md` §3'teki gibi; ledger 653 satır, CRLF, NUL 0; Index 426 satır, LF. Tutmayan her şey beklenmedik durumdur.

**(b) GitHub ölçümü:** dört depo için `gh api -i repos/ahmetxa/<ad>` (UTC; ilk satır HTTP durumu). 404 varsa PROJECT_LOG'un silme cümleleri güncellenir (yerler plan §7 "Açılışta ayrıca") ve `I3a`-7 `DEC-30` notunu yazar.

**(c) Bağlam ölçümü:** Ek A.7 betiği (`eval`), oturum başında ve her alt ajan sonucundan sonra.

**(d) Taban:** `step2 --strict` ve `step1 --strict` çıkış 0; `all` §7'deki gibi, çıkış 0. `step3-preflight --strict` ilk kez geçittir: yazımdan önce ölç; bulgu `I3a`/`I3b` hedefleriyle giderilmiyorsa beklenmedik durumdur.

**(e) `I3a` — ledger** (yalnız orkestratör yazar; hedefler plan §7.3 tablosunda `I3a`-1…-8):
1. **Çapalar:** tablodaki numaralar 653 satırlık ledger'ındır (`LMAP`); her hedef `:raw:N-N` ile içerikle doğrulanır. `LMAP`'in saymadığı IMPL-96 notları (`:97`, `:102`, `:104`; plan §10 `O5` maddesi) korunur.
2. **Taslak:** iki salt-okur scout aynı turda; öneri `I3a-A` = -1 (§2 koşu 21 satırı), -2 (§3 iki snapshot satırı, `:52`/`:58` SUPERSEDED notları, `:60` notu), -8 (§7 `:550`); `I3a-B` = -3, -4, -5 (§4), -6, -7 (§8). Scout yalnız yeni ya da değişen metni ve çapasını `local://`'a yazar, ≤ 4 KB döner (yol, bayt, hedef başına bir satır, `open_issues`).
3. **Görev metni:** o hedeflerin tablo satırları; Ek A.4 biçimleri ve emsaller (`:41`, `:51`, `:57`, `:87`, `:105`–`:107`, `:554`, `:602`); `W3F28` (1), (2), (5), (6); `Main-Planing.md:364`; §2 K9; `Main-Planing.md` sha256; §7 tabanı. Kurallar: İngilizce; hücrede `|` yok; §4'te yol ters tırnaksız (V:828); boş satır yok; kimlik değeri yok; `DEC-30` notu yalnız (b)'de 404 çıkarsa.
4. **Uygulama:** `%TEMP%`'te bir `py -3` betiği: bayt olarak okur, `\r\n` ile böler, her çapayı tam bir kez bulur, değişiklikleri sondan başa uygular, `\r\n` ile yazar. Orkestratör taslağı yeniden yazmaz; bulguyu taslağın scout'u düzeltir.
5. **Kontrol (betik, `difflib`):** `delete` yok; `replace` yalnız tablonun adlandırdığı satırlarda, eski hücre metni korunarak (yalnız Status, Superseded By, Updated At değişir; not eklenir); `insert` yalnız `:41`, `:58`, `:107`, `:610`'dan sonra. Boru: §2 6, §3 7, §4 10, §8 7. CR yalnız `\r\n`'de, NUL 0, tablolarda boş satır yok (V:404-429). Dokunulmayanlar: `:525`, `:567`, `:606`.
6. **Beklenen:** 9 yeni satır (662); §4'te 47 satır: 34 `verified`, 1 `implemented` (`Faz4.6`), 5 `planned` (`Faz10.1`–`Faz10.5`), 7 `superseded`.

**(f) `I3b`** (orkestratör; İngilizce; tarihli not, eski metin korunur):
1. **Index** (`edit`, LF): `I3b`-1 beş superseded girdi `:121` biçiminde, fazlara tarihli `DEC-28` notu; `Faz7.1` ve `Faz8.2` `verified` kalır. `I3b`-2 Faz 9'un ROM bağı (`:258`, `:279`), 4e bölümü, §7 notu. Numaralar `CPa`/`CPb`'den öncedir: içerikle bulunur, sondan başa yazılır.
2. **Ontology** (`I3b`-3): değişmez 10 (`:428`) gerçekleşti, 11 (`:429`) emekli (Hetzner). `py -3` ile bayt düzeyinde; NUL 2 (`:313`, `:316`) önce ve sonra sayılır; satır sonu türü korunur.
3. **Comprehension** (`I3b`-4): `CQ-13` (`:25`), `EV-20` (`:51`) Hetzner satırları; satır sonları korunur.
4. **Toolchain** (`I3b`-5): `docs/reverse-engineering-toolchain.md:220` (başlık `:213`). Öteki bayat yerler 12. denetime (plan §10).

**(g) PROJECT_LOG §5** (orkestratör, `edit`, Türkçe; iki kural):
1. Kimlik kuralı (plan §7.3 `:718`, `SEC` P2): kimlik değeri kuralı plan, alt plan ve belge metnini bağlar; değiştirilmemiş `scripts/smoke.sh` çıktısı (`snapshots/`) muaftır ama kimlik taramasından geçer, seri başlığı `dc27e5d0`.
2. Tek cihaz penceresi (plan §10 `:811`): aynı anda yalnız bir cihaz penceresi açık; bugün yalnız `Faz10.4`'te yazılı, PROJECT_LOG §5'te `Faz10.2`–`Faz10.4`'ü kapsayan kural olur.

**(h) `GATE3`** (plan §7.2 ara durum tablosu): `step2` ve `step3-preflight` `--strict` çıkış 0; V1 `all` yeni taban `subplan_count=47`, `warning_count=1`, çıkış 0; V2 yalnız bilinen `strict_warning`, çıkış 1; V3 PASS ve sha256; bayt (CRLF dosyada CR yalnız `\r\n`, LF dosyada CR 0; NUL Ontology 2, öteki 0; yeni satırlar ≤ 600 bayt); boru (plan `:174`, `:844`; ledger (e5)); kimlik taraması. Sapma beklenmedik durumdur.

**(i) Kapanış** (beklenmedik durum yoksa sorulmadan):
- Plan §1'de `3 · O4` `done`, commit'i başlığıyla anar: `Window 3 O4: integration and gates for planning run 21`; yeni taban plana, kapsam dışı bulgu §10'a. PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır, §11'e girdi. Bu dosya `3 · O5` için ≤ 20 KB yeniden yazılır.
- Bayt, boru ve kimlik (§7); yerel commit sorulmadan; kullanıcıya `git show --stat` özeti ve yeni pencere çağrısı. Push yok: o `3 · O5`'tir.

**Kabul:** `I3a`-1…-8, `I3b`-1…-5 ve iki §5 kuralı yazılmış; ledger yalnız ekleme ve izinli hücreler, CRLF; Ontology NUL'ları yerinde; `GATE3` geçti; §1'de `3 · O4` `done`.

**İnceleme:** plan öngörmez (`3 · O5`'te `REV-4` ∥ `SEC-C`); ledger için salt-okur teyit scout'u önerilebilir; P0/P1 → §0 adım 6.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7, §7.2, §7.3 ve ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| K1 `Kullanim.txt` | (b): v2.3'te düzeltilir (soru 4) | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K5/K6 üç depo | Silinecek; kullanıcı siler; açılışta ölçülür | `DEC-30` |
| K7 HyperOS 4 yönü | (a) modülü uyarla; (i) "ClaudeQB Phase 10", Faz 7 ve 8 emekli (soru 5) | `DEC-32` |
| K9 50MP HAL | Hayır, şimdilik; sensör katmanı sürer (soru 1) | `DEC-33` (`I3a`-6) |
| Sekiz soru | Yanıtlandı (2026-11-15); soru 7: Hetzner düzeltmeleri koşu 21'de; soru 8: sınırlı Step 2, Step 1.5 atlandı | plan §7 |
| Pencere 3 planı | Onaylandı (2026-11-15, form "onay") | plan §7.2 |
| Step 1 metni | Onaylandı (2026-11-15T14:10Z, form "onay"; C01–C03 dahil) | `Main-Planing.md` |
| Step 2 kontratı | Onaylandı (2026-11-15, form "onay"; dal sürer) | plan §7.3 |
| `3 · O3a` planı | Onaylandı (2026-11-15, form "onay"); Index `edit`, REV ∥ SEC | plan §7.2 |
| `3 · O3a` incelemesi | Düzeltmeler "hepsi" (2026-11-16, form) | plan §7.3 `:718`, §10 |
| `3 · O3b` planı | Onaylandı (2026-11-16, form "onay"; REV ∥ SEC) | plan §1 |
| `3 · O3b` incelemesi | P1 3, P2 4, P3 9; düzeltmeler "hepsi" (2026-11-16, form) | plan §7.3 `:719`–`:720`, §10 |
| Snapshot | Step 2 durmaz; etkin plan bugünkü `Main-Planing.md`; satırlar `I3a`-2 | plan §7.3 |
| Atıf | Phase 10 ve emeklilikler koşu 21'in seçimi; `DEC-28` Faz 7/8'i, `DEC-32` uyarlamayı anar | ledger `:606`, `:610` |
| Yayın | Dal `integrate/impl-96` sürer; C2 ve takip commit'i push edildi; sonraki sekiz commit yerel; FF ve push `3 · O5`'te | plan §1, §7.2 |

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
11. Cihaza komut: yalnız salt-okur ve plan §7.2'deki `PRB1`–`PRB10`; `3 · O4` hiç göndermez. Fiziksel eylemler kullanıcıda ve onaylı.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`, `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla.
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik değeri yazma ya da geri kazanma; tarama yalnız sayı ve konum basar.
20. Sıcak noktayı alt ajana yazdırma: ledger, `Main-Planing.md`, Index, Audit, Ontology, Comprehension, toolchain belgesi, `CHANGELOG.md`, sürüm yerleri, manifest, `.gitignore`, `.gitattributes`, `snapshots/`, plan, PROJECT_LOG ve git (plan §3, §7.2).
21. Satır sonu dönüştürme: ledger, `Main-Planing.md`, `Autopsy.md` CRLF, gerisi LF (Ontology ve Comprehension açılışta ölçülür); CRLF dosyada yazımdan sonra baytla doğrula.
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

| Kontrol | Taban (`CPb`'den sonra, 2026-11-16) |
|---|---|
| V1 `--mode all` | Yalnız `warning=step4_has_nonblocking_warnings=P2:1,P3:9`, `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; çıkış 0 |
| `step2`, `step1` `--strict` | Bulgu yok, çıkış 0 |
| `step3-preflight --strict` | Ölçülmedi; `GATE3`'te bulgu yok, çıkış 0 |
| V1 `GATE3` | Yeni taban `subplan_count=47`, `warning_count=1`; çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning`; çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=21` → PASS; `prose_mentions` artabilir |

- Kimlik taraması: `%TEMP%/idscan.py`, depo kökünde `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- `python` Store stub'ıdır; `SKILL.md`'deki `python3` burada çalışmaz.
- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` politikası `cat`, `head`, `tail`, `grep` ve `find`'ı engeller: `awk`, `read`/`grep`/`glob` araçları ya da `py -3` (`pathlib.rglob`); `<(…)` çalışmaz.
- **Ledger ve Ontology** yalnız `py -3` betiğiyle, bayt olarak yazılır (`edit` satır sonunu ve NUL'u bozabilir). Ekleme sondan başa yapılmazsa çapalar kayar.
- **Çapa numaraları:** ledger'dakiler `LMAP`'in, A.4'tekiler 644 satırlık ağacın (`LSH`); Index'tekiler `CPa`/`CPb`'den öncedir. Plan: `3 · O3b`'de `:718` sonrası +2, `:807` sonrası +6. Hepsi içerikle doğrulanır.
- **Ledger §4 doğrulayıcısı:** ters tırnaklı yol (V:828), boş satırla ayrılmış satır (V:420), dosyasız alt plan (V:830) kırmızıdır; Superseded By boş olmayan her değeri kabul eder (V:848). §2, §3 satırlarını V okumaz (V:93-103): betik ve boru sayısı denetler.
- **Ontology**'de 2 NUL (`:313`, `:316`): `grep` boş dönebilir (`AUDIT-FIX-22`).
- **Alt ajanlar:** scout'un kabuğu yok, `local://`'a yazar (ilk yazımın baytına bak; `local://` taşınmaz); `task` 100K bağlamlı: plan ya da PROJECT_LOG bütün verilmez. 429 ya da 402 ile duran ajan canlanmaz: görevi ortak bağlamla taze gönder.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok, `DEC-30`).
- **`--grep` satır başına bağlanır** (`'^Window 3 O3b:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`d = await commit.draft()`, `await d.take(...)`, `await d.commit(...)`); `git add`/`git commit` yok. Betikle değişen dosyaları açıkça `take` et.
- **Emekli Faz 7/8:** satırları, bölümleri ve dosyaları yerinde kalır (silmek `--strict`'te `extra_phase_folder_without_main_phase`); Index'te üstü çizilir, silinmez.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri ve snapshot (§4 a); plan §1'de ilk `pending` `3 · O4`.
3. GitHub (§4 b), bağlam (§4 c), doğrulayıcı tabanı `step3-preflight` dahil (§4 d).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin, bu oturumun yalnız `3 · O4` olduğu; teyit scout'u önerisi.
5. §4 (e) `I3a`, (f) `I3b`, (g) PROJECT_LOG §5, (h) `GATE3`; ardından (i).

---
