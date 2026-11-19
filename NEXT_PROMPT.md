# NEXT_PROMPT - ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> Pencere 4 · O4'ün kapanış commit'inde yazıldı. Aşama: **Pencere 4 · O5 - Son inceleme ve kapanış (`REV-5` ∥ `SEC-D` -> `FIX4` -> `GATE4` -> `C4` -> FF (onay) -> `RID` -> push (onay) -> `LSR`, `DEL4`; plan §8.2)**. Özettir; nihai kaynak plan, ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`) için root tabanlı kamera özelleştirmesidir (`ishtar-cam-modes` v2.2, `ishtar-aon-fix` v1.1, AGC yapılandırması; AOSPA Android 15'te ölçüldü). ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Pencere 4 12. denetimdir (ClaudeQB Step 3): 47 alt plan denetlendi. `4 · O4`'te Audit şablonla yeniden yazıldı; bulgu dosyası kanıt olarak kaldı. `4 · O0`, `4 · O1`, `4 · O2`, `4 · O3a`, `4 · O3b` ve `4 · O4` bitti.

1. **Tek aşama:** plan §1'de `4 · O4` `done` (`:75`), ilk `pending` `4 · O5` (`:76`). Bu oturum yalnız onu yürütür. Pencere 5+ (`:77`, K7 = (a) Step 4 dilimleri) bu oturumda başlamaz.
2. **Plan kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Kontrat sabittir:** §8.3 ve Ek A.8 kullanıcısız değiştirilmez. Audit ve bulgu dosyası `4 · O4`'te kapandı; `O5` onları yeniden yazmaz, yalnız bir bulgu gerektirirse `FIX4` ile dokunur.
4. **Cihaz:** Pencere 4 cihaza komut göndermez; olgular plan §7.1 `W3P01`-`W3P04`.
5. **Onay kapıları** (plan §0 adım 5; kısa evet/hayır): FF; her push ayrı; cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler (`DEC-30`). `REV-5`, `SEC-D`, `FIX4` ve `GATE4` sonucu onay kapısı değildir. Kapanış ve yerel commit (`C4`), beklenmedik durum yoksa sorulmadan atılır (§0 adım 4).
6. **Beklenmedik durum** (plan §0 adım 6): `GATE4`'ün §3 Geçitler'deki tabandan sapması; `REV-5` ya da `SEC-D`'de P0 ya da P1; açılış ya da yayın sapması; kapsamı ya da §8.2-§8.3 kararını değiştiren her düzeltme; bir alt ajanın `local://` dışına ya da sahiplik dışına yazması; planda olmayan bir eylem (dosya ya da depo silme, geçmişi yeniden yazma). Commit, FF ve push yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin. P0/P1 için seçenekler §8.3 madde 6'nın (a) ve (b)'sidir.
7. **Planlı bölme** (beklenmedik durum değildir): `FIX4` ya da `GATE4` sonrasında bağlam 300k'yı geçerse yeni iş başlatılmaz; kalan iş §1'de `4 · O5` `in_progress` kalarak yazılır ve bu dosya kalan iş için yeniden yazılır (plan §0 adım 7, 9).

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/`, `docs/` ve bulgu dosyası İngilizce.

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda ölç; 250k'dan sonra her turda. 300k'dan sonra yeni görev yok; kapanış 400k'dan önce biter.
- **Tahmin** (plan §1): `4 · O5` ≈ 220k.
- **Ders (`4 · O4`, PROJECT_LOG §11):** açılış 70,5k; taban sonrası 116k; ilk taslaktan sonra 163,8k; üç taslak ve `GATE4`'ten sonra 176k. Büyümenin kaynağı okunan metin ve taslakların sonuç blokları oldu. Her aralığı bir kez oku; sonuçları `local://` dosyasına yaz, dönüşte yalnız özet.
- **Kazanç:** büyük dosyaları `grep` aracı ve dar `:N-M` aralıklarıyla oku; 760 karakteri aşan satırları `:raw` ile oku. Çıktıda yalnız sayılar ve kısa maskeli alıntılar.

## 2. Okuma sırası

Büyük dosyalar bütün okunmaz. Numaralar `4 · O4` kapanışınındır; içerikle doğrula.

1. Plan §0 (`:9`-`:44`), §1 (`:73`-`:77`), §3 (`:99`-`:125`; Geçitler taban satırları `:111`-`:112`).
2. Plan §8.2 görev tablosu (`REV-5`, `SEC-D`, `FIX4`, `GATE4`, `C4`, `FF`, `RID`, push, `LSR`, `DEL4`) ve kararlar (`:797`-`:856`).
3. Plan §8.3 (`:857`-`:917`), madde 6-7 dikkatle.
4. Ek A.5 (`:1077`-`:1122`; push ve kimlik taraması), A.7 (`:1150`-`:1171`).
5. PROJECT_LOG §2.6 (`:228`-`:240`) ve §11'in son girdisi (`4 · O4`).
6. `Planner-docs/Sub-Planing-Audit.md`: başlıklar (`awk '/^#/'`) ve durum satırı `:10`. Tablolar okunmaz.
7. `AUDIT12_FINDINGS.md`: yalnız başlıklar (`awk '/^#/'`); birleştirme notu `:3`-`:5`. Kanıt olarak kalır; `O5` yazmaz.

## 3. Mevcut durum

**Beklenen durum (4 · O4 kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 93 commit. Uç ve kapanış: `Window 4 O4: merged audit and gates for the twelfth audit` (`git log --grep '^Window 4 O4:'` tek commit = uç). Etiket yok, 356 izlenen dosya.
- **Yayın:** `main` = `origin/main` = `081790f`; `origin/main..HEAD` = 6; `git ls-remote origin` üç ref = `081790f`. FF ve push yalnız `4 · O5`'te, `C4`'ten sonra, ayrı onaylarla (plan §8.2).
- **GitHub** (2026-11-19T10:18:48Z-10:18:52Z): dört depo 200; `ishtar_cam_modes` ve `ishtar` özel, ikisi açık. Silme kullanıcıda (`DEC-30`).
- **Audit** `Planner-docs/Sub-Planing-Audit.md`: 635 satır, 102.309 B, LF, NUL 0; durum `status: PASS_WITH_WARNINGS` (`:10`). §12: 47 satır (34 COMPLETE, 7 SUPERSEDED, 1 DEFERRED `Faz4.6`, 5 READY_WITH_WARNINGS `Faz10.1`-`10.5`); kuyruk READY, baş `Faz10.1`. §13: 65 satır (13 eski + 52 yeni); etkin P0 0, P1 0, P2 6, P3 49 (45 `open`, 4 `accepted`). Birleştirme: `AUDIT-FIX-90` ve `-96` çözüldü (Audit metni kapatır); eski `-57` çözüldü (kalıntı `-62`, `-100`); `-50` açık, sahibi `Faz10.5` (karar 6).
- **`AUDIT12_FINDINGS.md`:** 509 satır, LF, NUL 0; tarihli birleştirme notu `:3`-`:5`; `## Session 4 · O3a` `:9`, `## Session 4 · O3b` `:235`.
- **Değişmeyen dosyalar** (`4 · O4`'te dokunulmadı): `Main-Planing.md` sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, 77.019 B, CRLF, NUL 0, 10 faz, 47 alt plan. Ledger 662 satır, CRLF, NUL 0. Index 443, Ontology 453 (NUL 2: `:313`, `:316`), Comprehension 176, toolchain 246, LF.
- **Plan:** 1285 satır, LF; §1 `4 · O4` `done` (`:75`), `4 · O5` `pending` (`:76`). Çapalar: §8.2 `:797` (kararlar `:845`), §8.3 `:857`, §9 `:918`, §10 `:927`, Ek A `:988`, A.5 `:1077`, A.7 `:1150`, A.8 `:1172`.
- **Kapasite:** `reviewer` penceresi 1M; `security-reviewer` penceresi 1M görüldü, kabuğu yok (`4 · O3a`).
- **Geçitler ve sürüm:** yeni taban §3 Geçitler ve §7 (`GATE4`, 2026-11-19T10:37:40Z-10:38:30Z); kimlik taraması `prose_mentions=28`; v2.2 / versionCode 13 (`DEC-29`).

## 4. Bu oturum: `4 · O5`

Yazılanlar: plan §1 `4 · O5` `done`; PROJECT_LOG §2.6 ve §11; bu dosya (sonraki aşama için). Taslaklar ve incelemeler `local://` içinde kalır ve commit'e girmez. Düzeltme gerekirse yalnız bulguyu kapatan dosya değişir.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 4 O4: merged audit and gates for the twelfth audit`; `git log --grep '^Window 4 O4:'` tek commit = uç; `git rev-list --count HEAD` = 93; `git tag` boş; `git ls-files` = 356; plan §1'de ilk `pending` = `4 · O5`.
Yayın: `git rev-parse main origin/main` = `081790f`; `git rev-list --count origin/main..HEAD` = 6; `git ls-remote origin` üç ref = `081790f`. GitHub: dört depo `gh api -i repos/ahmetxa/<ad>` (UTC; `gh` yolu §8). Tutmayan her şey beklenmedik durumdur.
İnceleme kapsamı: `git diff --name-only 081790f..HEAD` = beş dosya: `AUDIT12_FINDINGS.md`, `NEXT_PROMPT.md`, `ORCHESTRATION_PLAN.md`, `PROJECT_LOG.md`, `Planner-docs/Sub-Planing-Audit.md` (açılışta ölçülür; başka dosya beklenmedik durumdur).

**(b) Bağlam:** Ek A.7 betiği açılışta, tabandan sonra, her alt ajan sonucundan sonra ve `FIX4`'ten önce.

**(c) Taban** (§7): `step2`, `step1`, `step3-preflight` `--strict`, V1-V3, kimlik taraması, `--mode step3` (bayraksız ve `--strict`). Sapma beklenmedik durumdur.

**(d) Diff dosyası:** `git diff 081790f..HEAD > local://window4-diff.md` (bash yönlendirmesi); `SEC-D` bu dosyayı okuyacak; bayt sayısı dönüşte bildirilir. Yönlendirme çalışmazsa orkestratör diff'i `read` ile parça parça alıp `write` ile yazar.

**(e) İnceleme** (tek paralel grup, salt-okur):
- `REV-5` (`reviewer`): `081790f..HEAD` diff'i: doğruluk, §8.3 kontratına uyum (§13: 65 satır, başlık birebir; §12: 47 satır; 15 `##` başlık), eksikler; sır ve kimlik değeri yok. Dönüş ≤ 4 KB; ayrıntı `local://rev-5.md`.
- `SEC-D` (`security-reviewer`): kabuğu yok; girdi `local://window4-diff.md`. Sır, kimlik değeri, güvensiz komut önerisi ve onay kapısı atlamaları. Dönüş ≤ 4 KB; ayrıntı `local://sec-d.md`.
- Bulgular P0-P3 olarak sınıflanır. P0 ya da P1 beklenmedik durumdur (§0 madde 6).

**(f) `FIX4`:** yalnız bulgu kapatan düzeltmeler; kapsam, karar ya da git geçmişi değişmez. `Planner-docs/` dosyası düzeltilirse yalnız orkestratör yazar; sonra bayt ve boru sayımı tekrar ölçülür. Bulgu yoksa `FIX4` yoktur.

**(g) `GATE4`** (§8.3 madde 6; yeniden): `--mode all` çıkış 0; `warning=step4_has_nonblocking_warnings=P2:6,P3:49` (`FIX4` Audit'e dokunmadıysa; dokunduysa yalnız `open` ve `accepted` satırlardan çıkan yeni sayılar plan §3 Geçitler'e yazılır); `audit_status=PASS_WITH_WARNINGS`; `p0_findings=0`, `p1_findings=0`; `subplan_count=47`; `index_reference_count=47`; `phase_folder_count=10`; `secret_findings=0`; `--mode step3 --strict`'te yalnız `strict_warning`; `step2`, `step1`, `step3-preflight` `--strict` 0; V3 değişmez; kimlik taraması PASS. Bunun dışındaki sapma beklenmedik durumdur.

**(h) `C4` ve kapanış** (plan §0 adım 4; beklenmedik durum yoksa sorulmadan):
- Plan §1'de `4 · O5` `done`; ilk `pending` = `5+` (`:77`). Plan commit başlığı adlandırmaz; öneri, plan dışı: `Window 4 O5: final review and closing for the twelfth audit`.
- PROJECT_LOG §2.6 aynı kapsamla yeniden yazılır; §11'e girdi (bağlam ölçümleri dahil).
- Bu dosya `5+` için ≤ 20 KB yeniden yazılır; `5+` bu oturumda başlamaz.
- Değişen dosyalarda bayt, boru ve kimlik taraması (§7, Ek A.5); `AUDIT12_FINDINGS.md` LF, NUL 0.
- Yerel commit `eval`'deki `commit` ad alanıyla (`draft`, `take`, `commit`); değişen dosyaları açıkça `take` et. Sonra `git log --grep '^Window 4 O5:'` ile hash bulunur; kullanıcıya `git show --stat` özeti.
- **FF (onay):** kullanıcı "evet" derse yalnız `git fetch . integrate/impl-96:main`. Sonra `main` = `integrate/impl-96` = `HEAD`.
- **`RID` (Ek A.5):** push'tan hemen önce kimlik taraması; `NOT_REDACTED=0`, `LUHN15=0`; `prose_mentions` sayısı kaydedilir.
- **Push (onay, ayrı):** kullanıcı "evet" derse yalnız `git push origin main integrate/impl-96`. `--all` ve `--mirror` asla.
- **`LSR`:** `git ls-remote origin` üç ref = `HEAD` hash'i; uyuşmazlık beklenmedik durumdur.
- **`DEL4`:** silinecek üç deponun `gh api -i` ölçümü (UTC). Üç depo (`DEC-30`, plan Ek A `:1000`): `ahmetxa/ishtar` (özel), `ahmetxa/android_local_manifests` ve `ahmetxa/android_device_xiaomi_ishtar` (açık); 404 = silinmiş, kaydedilir. Silme kullanıcıdadır.
- **Ret ve sonrası:** FF ya da push reddedilirse adım atlanır ve kullanıcıya bildirilir (onay kapısı; beklenmedik durum değil). FF, `RID`, push, `LSR` ve `DEL4` `C4`'ten sonradır: sonuçlar kullanıcıya bildirilir, kalıcı kaydı `5+` açılışı yapar; bu yüzden `5+` için yazılan `NEXT_PROMPT.md` açılış kontrolünü iki durum için de (push edildi / edilmedi) tanımlar.
- Kullanıcıya yeni pencere talimatı: `5+` için bu dosyanın metni.

**Kabul:** açılış ve taban tuttu; `REV-5` ve `SEC-D` dönüş bloklarında P0 ve P1 yok ya da §0 madde 6 uygulandı; `GATE4` §3 Geçitler'deki değerlerle; §1, PROJECT_LOG ve bu dosya güncel; `C4` yerel; FF, push ve `LSR` yalnız onayla ve hash ile kapanır.

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
| Yayın | C3 push edildi (2026-11-16); FF ve push yalnız `4 · O5`'te, `C4`'ten sonra | plan §8.2, PROJECT_LOG §11 |

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
10. `Faz4.1`/`Faz4.7`'yi canlandırma; `Faz4.6`'yı kararsız tamamlama.
11. Cihaz komutu: Pencere 4 (12. denetim) hiç göndermez; `4 · O5` dahil. Fiziksel eylemler kullanıcıda ve onaylı.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`; `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla.
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik değeri yazma ya da geri kazanma; tarama yalnız sayı ve konum basar.
20. Sıcak noktayı alt ajana yazdırma: ledger, `Main-Planing.md`, Index, Audit, `AUDIT12_FINDINGS.md`, Ontology, Comprehension, toolchain belgesi, `CHANGELOG.md`, sürüm yerleri, manifest, `.gitignore`, `.gitattributes`, `snapshots/`, plan, PROJECT_LOG ve git (plan §3). Audit'i yalnız orkestratör yazar.
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

| Kontrol | Taban (`GATE4` 2026-11-19T10:37:40Z-10:38:30Z, plan §3 Geçitler; `4 · O5` başında hâlâ bu) |
|---|---|
| `step2`, `step1`, `step3-preflight` `--strict` | Bulgu yok, çıkış 0 |
| V1 `--mode all` | Çıkış 0; yalnız `warning=step4_has_nonblocking_warnings=P2:6,P3:49`; `audit_status=PASS_WITH_WARNINGS`; `p0_findings=0`, `p1_findings=0`; `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; `secret_findings=0` |
| `step3` ve `step3 --strict` | Bayraksız çıkış 0; `--strict` çıkış 1, yalnız `strict_warning=step4_has_nonblocking_warnings` (denetim `PASS_WITH_WARNINGS` kaldıkça) |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning` (`execution_queue_state=READY`); çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=28` → PASS; `prose_mentions` artabilir |
| Boru ve bayt | Boru dışı yalnız plan `:183`, `:1019` ve ledger satırları; ledger ve `Main-Planing.md` CRLF, öteki LF; NUL yalnız Ontology'de (2); `Sub-Planing-Audit.md` LF, NUL 0 |

- `GATE4` yeni tabanı plan §3 Geçitler'e yazar. `4 · O5`'teki `GATE4` aynı değerleri bekler; sapma beklenmedik durumdur.
- Kimlik taraması Ek A.5 betiğiyle, kökten `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: `O5` içinde çalıştırılmaz.

## 8. Bilinen tuzaklar

- **omp:** Ek A.7 betiği JS'tir (`eval`). Eval'in Python arka ucu yok. `bash` politikası `grep`'i engelledi (`4 · O4`): arama `grep` aracıyla ya da `awk` ile yapılır.
- **Scout'lar kabuksuz (`4 · O4`):** `wc` ya da `awk` çalıştıramadılar; sayım okuma aracıyla yapıldı. Sayım isteyen görev bunu baştan belirtir.
- **`reviewer`:** `bash`'te `grep` kullanamıyor; `grep` aracını kullanır.
- **`security-reviewer`:** kabuğu yok; `SEC-D` için diff `local://window4-diff.md`'den verilir; alternatif olarak `reviewer` kullanımı kullanıcıya sorulur.
- **Okuma aracı:** 768 karakteri aşan satırları keser, büyük dosyada blok atlar (`4 · O3a`'da 48 KB). Tek satır için `:raw:N-N`.
- **Boru sayımı:** ham `|` (kaçışlı dahil) sayılır; bu, plan `:183`, `:1019` ve ledger satırlarını verir. Kaçışlı olanları ayırmak tabloyu yanlış gösterir.
- **AGC değerleri:** ajanlar tercih değerini kopyalayabilir: `[value withheld]` ile maskele; `pref_*=` taraması maskeyi yok sayar, maskesiz eşleşme `0` olmalı.
- **`local://` oturumlar arasında kaybolur** (§0 adım 8): `REV-5`, `SEC-D` ve `window4-diff.md` kapanışa kadar aynı oturumda kalır.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe`.
- **`--grep` satır başına bağlanır** (`'^Window 4 O4:'`) ve gövde satırlarını da eşler.
- **Commit:** `eval`'deki `commit` ad alanıyla; `git add`/`git commit` yok. `cp` ile konan dosyalar dahil değişen dosyaları açıkça `take` et.
- **`.gitattributes`:** `* -text` bayt korur, `*.md` için `eol=lf` yok: LF baytla doğrulanır.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri, yayın doğrulaması ve dört depo (§4 a); plan §1'de ilk `pending` `4 · O5`.
3. Bağlam (§4 b), taban (§4 c) ve diff kapsamı (§4 a, d).
4. Kısa Türkçe "hazırım" özeti (ölçülenler, yayın durumu); soru sorma.
5. §4 (e) `REV-5` ∥ `SEC-D`; (f) bulgu varsa `FIX4`; (g) `GATE4`; (h) `C4`; FF, push ve `DEL4` yalnız kullanıcı onayıyla ve plan §8.2 sırasında.

---
