# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> Pencere 3 · O5'in kapanış commit'inde yazıldı. Aşama: **Pencere 4 · O0 — 12. denetim keşfi (Step 3; plan §8)**. Özettir; nihai kaynak plan, ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC yapılandırması; hepsi AOSPA Android 15'te ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Pencere 3 (koşu 21) bitti: Step 1 (Faz 7 ve 8 emekli), kontrat, `Faz10.1`–`Faz10.5` (47 alt plan), `GATE3` (`3 · O4`), son inceleme ve kapanış (`3 · O5`). Pencere 4 12. denetimdir (ClaudeQB Step 3): bütün alt planlar denetlenir, yalnız `Planner-docs/Sub-Planing-Audit.md` yazılır.

1. **Tek aşama:** plan §1'de Pencere 3 `done`; ilk `pending` satır Pencere 4, aşama satırı henüz yok. Bu oturum yalnız `4 · O0`'ı (keşif; plan §8 varsayılan dağılımı) yürütür. Plan §0'a göre Pencere 4'te `O0` ile `O1` ayrı oturumlardır; sıradaki aşama `4 · O1+O2` (plan ve denetim kontratı, birleşik, onayla; plan §8), yeni oturumda. Aşama atlanmaz.
2. **Plan kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** olgular 2026-11-13 ölçümü ve 2026-11-15 `PRB` ölçümüdür (plan §7.1 `W3P01`–`W3P04`). Pencere 4 cihaza komut göndermez.
4. **Onay kapıları** (plan §0 adım 5; kısa evet/hayır): `O1` sonunda plan onayı (bu aşamada yok); FF; her push ayrı; cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler. `4 · O0` kapanışı ve yerel commit'i, beklenmedik durum yoksa sorulmadan (§0 adım 4).
5. **Beklenmedik durum** (plan §0 adım 6): kapanış, commit ve bu dosyanın yeniden yazımı yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/` (ledger ve Audit dahil) ve `docs/` İngilizce (Ek A.3).

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): bağlamı Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok: işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, bu dosya, commit); kapanış 400k'dan önce biter.
- **Tahmin:** `4 · O0` ≈ 185k (35k + 25 × 6k; emsal `3 · O0`, plan §7 `:445`). Kalibrasyon: PROJECT_LOG §11, `3 · O0` ve `3 · O5` girdileri.
- **Hijyen:** plan §0 adım 8–9 (20 KB üstü okuma scout'a, dönüş ≤ 4 KB `local://`'a, dar `:N-M`, satır ≤ 600 B, `todo` ≤ 8).

## 2. Okuma sırası

Plan, PROJECT_LOG, ledger, Index, Audit, Ontology ve Comprehension bütün okunmaz; bölüm başları `grep '^##'` ile. Plan numaraları `3 · O5`'ten öncedir; içerikle doğrula.

1. Plan §0, §1 ve §3 (geçitler, Gizlilik, Git, Adlandırma).
2. Plan §8 (Pencere 4; `:744`–`:752`): reviewer sınırı, oturum düzeni, varsayılan dağılım, tuzaklar, beklenenler, geçit.
3. Plan §7 "Doğrulayıcı tuzakları" (`:481`–`:489`), "ClaudeQB süreci" (`:491`); §7.1'in başı (`:493`; envanter biçimi emsali).
4. Plan §10: 12. denetime yönlendirilenler (`grep -n '12. denetim'`); §7 "Açılışta ayrıca" (`:439`) ve §6.4 (push doğrulama emsali).
5. Ek A.5 (push kuralları, betik), A.7; PROJECT_LOG §2.6, §5.5 ve §11'in `3 · O5` girdisi.
6. `C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/references/handoffs/run-step3.md` (kısa; roller `:17`) ve `references/Third-Planner.md` (başlıklar).

## 3. Mevcut durum

**Beklenen durum (3 · O5 kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 87 commit. Uç ve kapanış: `Window 3: planning run 21 and handoff for the twelfth audit` (`git log --grep '^Window 3:'`). Etiket yok, 355 izlenen dosya.
- **Yayın:** FF ve push `3 · O5`'te bu commit'ten sonra ayrı onaylarla sorulur. İkisi onaylandıysa `main` = `origin/main` = uç ve `git ls-remote origin`'de `HEAD`, `main`, `integrate/impl-96` = uç. Push onaylanmadıysa `origin/main` = `6632a18`, `origin/main..HEAD` = 11; `main` FF onayına göre uç ya da `6632a18`. Açılış doğrular ve kaydeder (emsal plan §6.4 `2 · O5`, §7 `:439` `3 · O0`).
- **`3 · O5`:** `REV-4` (dört parça) ∥ `SEC-C` (üç parça): P0 0, P1 0, P2 9, P3 24; kapsam "hepsi": `FIX3` 86 işlemi betikle uyguladı, satır sayıları sabit; onaylı `Main-Planing.md` maddeleri ve kapsam dışı bulgular plan §10'a (12. denetim); teyit: reviewer P2 3, P3 5, security-reviewer 0, hepsi bu aşamada düzeltildi (`fix-t`); ayrıntı PROJECT_LOG §11.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez; 200 olmalı); silinecek üç depo (`DEC-30`): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. Son ölçüm C3'ten önce (PROJECT_LOG §11); 404 = silinmiş.
- **`Main-Planing.md`** (değişmedi): sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, 77.019 bayt, CRLF, NUL 0, 10 faz. Alt plan 47.
- **Ledger:** 662 satır (`3 · O4` sonunda 662), CRLF, NUL 0. §2 koşu 21; §3 `SNAP-2026-11-15-MAIN`, `SNAP-2026-11-16-SUBPLANS`; §4 47 satır: 34 `verified`, 1 `implemented` (`Faz4.6`), 5 `planned` (`Faz10.1`–`Faz10.5`), 7 `superseded`; §8 `DEC-33`.
- **Öteki dosyalar:** Index 443 satır, LF; Ontology 453, LF, NUL 2 (`:313`, `:316`); Comprehension 176, LF; toolchain 246, LF; PROJECT_LOG §5.5. Audit 11. denetimdir, koşu 21'de dokunulmadı (≈ 57 KB; durum `:18`).
- **Plan:** §1'de `3 · O5` ve Pencere 3 `done`, Pencere 4 `pending`; §8 Pencere 4'ün kuralları; §10'da 12. denetime yönlendirilenler. Boru dışı satırlar: `:174`, `:854`.
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` v1.9 içeriğinde (`DEC-29`).
- **Telefon** (plan §7.1, PROJECT_LOG §2.3): HyperOS 4 (`OS4.0.0.44.WMACNXM`), SukiSU-Ultra v4.3.0-r1, metamodül yok; HAL AOSPA'dan farklı, sensör = `EXPECT_MD5`; proje modülleri ve kutucuk yok; AGC yamasız V9.6, 10 tuzak.
- **Araçlar:** `%TEMP%/idscan.py` yoksa Ek A.5 betiğinden yeniden yazılır.

## 4. Bu oturum: `4 · O0`

Keşif salt-okurdur; Audit yazılmaz. Kapanışta yazılanlar: plan §8'in yeni alt bölümü, §1 (gerekirse §3 Adlandırma, §10), PROJECT_LOG §2.6 ve §11, bu dosya; sonra git.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 3: planning run 21 and handoff for the twelfth audit`; `git log --grep '^Window 3:'` tek commit = uç; `git rev-list --count HEAD` = 87; `git tag` boş; `git ls-files` = 355. Plan §1'de ilk `pending` = Pencere 4.
Yayın: `git rev-parse main origin/main`, `git rev-list --count origin/main..HEAD`, `git ls-remote origin`; sonuç §3'teki durumlardan biri olmalı; PROJECT_LOG §11 sonucu içermez (sohbette), açılış kaydeder. Push yapılmamışsa kullanıcıya sorulur (§0 adım 5; emsal plan §7 `:439`); sonuç envantere ve PROJECT_LOG'un push cümlelerine yazılır.
Snapshot: `Main-Planing.md` §3'teki gibi; ledger 662 satır, CRLF, NUL 0; Index 443, Ontology 453 (NUL 2), Comprehension 176, toolchain 246, hepsi LF. Tutmayan her şey beklenmedik durumdur.
GitHub: dört depo için `gh api -i repos/ahmetxa/<ad>` (UTC; ilk satır HTTP durumu). `ahmetxa/ishtar_cam_modes` 200 değilse beklenmedik durum. Üç depodan biri 404 ise beklenmedik durum değildir, kaydedilir: PROJECT_LOG'un silme cümleleri (yerler plan `:441`; içerikle), §2.6 ve §11. Ledger `DEC-30` notunun Pencere 4'te yazarı yok: kullanıcıya söylenir.

**(b) Bağlam ölçümü:** Ek A.7 betiği (`eval`), oturum başında ve her alt ajan sonucundan sonra.

**(c) Taban** (açılışta bir kez, §7): `step2`, `step1`, `step3-preflight` `--strict`, V1–V3 ve kimlik taraması; sapma beklenmedik durumdur. Ayrıca keşif ölçümü olarak `--mode step3` (bayraksız ve `--strict`) bir kez: 11. denetimin dosyasıyla çıkan sonuç taban değildir, envantere yazılır.

**(d) Keşif** (salt-okur scout'lar; aynı anda en çok üç; dönüş ≤ 4 KB, ayrıntı `local://`):
1. **S1 boyut ve dilim:** 47 alt planın ve `Faz-*-Plans/` klasörlerinin bayt ve satırı; ortak girdi (`Main-Planing.md`, Index, ledger, Ontology, Comprehension, Audit) baytı; plan §8'in reviewer başına ≤ 400 KB kuralıyla klasör dilimleri ve rol × dilim çalışma sayısı (plan tahmini ≈ 9, oturum başına ≤ 3).
2. **S2 Audit ve doğrulayıcı:** `Sub-Planing-Audit.md` boyutu, ilk `status:` eşleşmesi (bugün `:18`), 15 başlık ve uzunlukları, son kimlik (`AUDIT-FIX-57`), kuyruk yerleri; doğrulayıcının `--mode step3` kuralları satır numaralarıyla; `run-step3.md` ve `Third-Planner.md`'deki roller (kapsam, hazırlık, güvenlik), çıktı şablonu, durma kapıları.
3. **S3 12. denetime yönlendirilenler:** plan §10 maddeleri; §7.1 `W3F12`, `W3F28`, `W3F29`; yazarını kaybeden `AUDIT-FIX-22` (`F8.1-10`), `-37` (`F7.3-08`), `-50` (`F8.3-08`) ve ledger koşu 21 satırındaki anışı; `-41`, `-42`, `-57`'nin yeni ifadesi. Her madde için `dosya:satır` (içerikle) ve önerilen rol.

Envanter plan §8'e yeni alt bölüm olarak yazılır (≤ 15 KB, §7.1 biçiminde: kimlik, olgu, değer, kaynak); ilk satır açılış ölçümü. Kimlik önerisi `W4OPN`, `W4F01`…; plan §3 Adlandırma'ya eklenir. Envanter `4 · O1+O2`'nin girdisidir: reviewer dilimleri, bulgu dosyasının yeri (`Planner-docs/` dışında; plan §8), aşama tahminleri.

**(e) Kapanış** (plan §0 adım 4; beklenmedik durum yoksa sorulmadan):
- Plan §1'e `4 · O0` satırı `done` (commit başlığıyla) ve `4 · O1+O2` satırı `pending` (tahminle) eklenir; öteki aşama satırlarını `4 · O1+O2` planı ekler. Başlık önerisi (emsal `Window 3 O0: discovery for planning run 21`): `Window 4 O0: discovery for the twelfth audit`.
- PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır, §11'e girdi (bağlam ölçümleri dahil).
- Bu dosya `4 · O1+O2` için ≤ 20 KB yeniden yazılır; birleşimin tahmini (≤ 240k) gösterilir, açılışta kullanıcı onaylar (§0 adım 9).
- Bayt, boru ve kimlik taraması (§7); yerel commit; kullanıcıya `git show --stat` özeti ve yeni pencere talimatı.

**Kabul:** açılış tuttu; yayın durumu ve dört depo kaydedildi; geçitler tabanda; S1–S3 bitti; envanter plan §8'de; §1, PROJECT_LOG ve bu dosya güncel; kapanış commit'i yerel.

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
| `3 · O3a` incelemesi | Düzeltmeler "hepsi" (2026-11-16, form) | plan §7.3, §10 |
| `3 · O3b` planı | Onaylandı (2026-11-16, form "onay"; REV ∥ SEC) | plan §1 |
| `3 · O3b` incelemesi | P1 3, P2 4, P3 9; düzeltmeler "hepsi" (2026-11-16, form) | plan §7.3, §10 |
| `3 · O4` planı | Onaylandı (2026-11-16, form "onay"); iki PROJECT_LOG kuralı "yeni §5.5" | plan §1, PROJECT_LOG §5.5 |
| `3 · O4` incelemesi | Teyit incelemesi "ekle" (2026-11-16, form); P0 0, P1 0, P2 2, P3 5 aşamada düzeltildi | plan §10 |
| `3 · O4` takibi | Kaydet (2026-11-16, form "takip"): kayma haritası ve `FIX3` maddeleri | plan §10 |
| `3 · O5` | Plan "onay", teyit "ekle", düzeltme "hepsi" (2026-11-16, form; istisnalar §10) | plan §1, §10 |
| Snapshot | Step 2 durmaz; etkin plan bugünkü `Main-Planing.md`; satırlar yazıldı (`I3a`-2) | plan §7.3, ledger §3 |
| Atıf | Koşu 21'in seçimi | ledger §8 |
| Yayın | Dal sürer; FF ve push `3 · O5`'te ayrı onaylarla; `4 · O0` doğrular | plan §1, PROJECT_LOG §11 |

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
11. Cihaza komut: Pencere 4 (12. denetim) hiç göndermez, `4 · O0` dahil. Fiziksel eylemler kullanıcıda ve onaylı.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`, `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla.
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik değeri yazma ya da geri kazanma; tarama yalnız sayı ve konum basar.
20. Sıcak noktayı alt ajana yazdırma: ledger, `Main-Planing.md`, Index, Audit, Ontology, Comprehension, toolchain belgesi, `CHANGELOG.md`, sürüm yerleri, manifest, `.gitignore`, `.gitattributes`, `snapshots/`, plan, PROJECT_LOG ve git (plan §3).
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

| Kontrol | Taban (`3 · O5` geçitleri, 2026-11-16T21:27Z) |
|---|---|
| `step2`, `step1`, `step3-preflight` `--strict` | Bulgu yok, çıkış 0 |
| V1 `--mode all` | Yalnız `warning=step4_has_nonblocking_warnings=P2:1,P3:9`; `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning`; çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=24` → PASS; `prose_mentions` artabilir |
| Boru ve bayt | Boru dışı yalnız plan `:174`, `:854` ve ledger `:473`, `:490`–`:495`, `:501`, `:506`, `:507`; ledger ve `Main-Planing.md` CRLF, öteki LF; NUL yalnız Ontology'de (2) |

- Kimlik taraması: `%TEMP%/idscan.py`, depo kökünde `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: çalıştırma.
- 12. denetimin geçidi `--mode step3 --strict` ve `--mode all` (plan §8); denetim bulgu sayılarını değiştirir, yeni taban `4 · O4`'te yazılır.

## 8. Bilinen tuzaklar

- `python` değil `py -3` (§6 madde 22).
- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` politikası `cat`, `head`, `tail`, `grep` ve `find`'ı engeller: `awk`, `read`/`grep`/`glob` araçları ya da `py -3`; `<(…)` çalışmaz.
- **ClaudeQB:** `/claudeqb:claudeqb` komutunu Claude Code'da kullanıcı yazar; omp altında skill dosyaları mutlak yolla okunur, doğrulayıcı `py -3 <mutlak yol>` ile (plan §7 "ClaudeQB süreci").
- **Denetim durumu:** doğrulayıcı durumu ilk `status:` eşleşmesinden okur; başlıkta eski denetimin durumu alıntılanmaz. Değer ayıraçtan hemen sonra gelir: `**Overall audit status: PASS_WITH_WARNINGS.**` eşleşir, `**Overall audit status:** …` eşleşmez (plan §7 tuzakları, §8).
- **Denetim biçimi:** 15 başlık tekil, her biri en az 20 karakter. Bulgu kimlikleri `AUDIT-FIX-58`'den devam eder. Beklenen: `Faz7.2`, `7.3`, `8.1`, `8.3` SUPERSEDED; `Faz4.6` DEFERRED; yeniler READY, READY_WITH_WARNINGS ya da gerekçeli NEEDS_REPAIR.
- **Step 4 kuyruğu:** `--mode step4 --strict` kuyruğu yalnız denetim dosyasından okur; 11. denetimin geçersiz kuyruğuyla da p0/p1 geçidi geçer (V2). Pencere 4 bitmeden Step 4 başlatılmaz.
- **Reviewer girdisi:** reviewer başına ≤ 400 KB, oturum başına ≤ 3 (plan §8); `task` 100K bağlamlıdır, plan ya da PROJECT_LOG bütün verilmez.
- **Çapa numaraları** çoğu yerde eski ağaçlarındır (kayma haritası plan §10); her atıf içerikle doğrulanır.
- **Ontology**'de 2 NUL (`:313`, `:316`): `grep` boş dönebilir (`AUDIT-FIX-22`).
- **Alt ajanlar:** scout'un kabuğu yok, `local://`'a yazar (ilk yazımın baytına bak). 429 ya da 402 ile duran ajan canlanmaz: görevi ortak bağlamla taze gönder.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok, `DEC-30`).
- **`--grep` satır başına bağlanır** (`'^Window 3:'`, `'^Window 4 O0:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`d = await commit.draft()`, `await d.take(...)`, `await d.commit(...)`); `git add`/`git commit` yok. Değişen dosyaları açıkça `take` et.
- **Emekli Faz 7/8:** satırları, bölümleri ve dosyaları yerinde kalır (silmek `--strict`'te `extra_phase_folder_without_main_phase`); Index'te üstü çizilir, silinmez.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri, yayın doğrulaması (`git ls-remote origin`), snapshot ve dört depo (§4 a); plan §1'de ilk `pending` Pencere 4.
3. Bağlam (§4 b) ve taban (§4 c).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin, yayın durumu, bu oturumun yalnız `4 · O0` olduğu, S1–S3 önerisi; push yapılmamışsa ayrı onay sorusu.
5. §4 (d) keşif ve envanter, (e) kapanış.

---
