# NEXT_PROMPT - ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> Pencere 4 · O3b'nin kapanış commit'inde yazıldı. Aşama: **Pencere 4 · O4 - Birleştirme ve geçitler (`AUD-D1` ∥ `AUD-D2` ∥ `AUD-D3` -> `AUD-W` -> `GATE4`; plan §8.3 madde 4-7)**. Özettir; nihai kaynak plan, ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`) için root tabanlı kamera özelleştirmesidir (`ishtar-cam-modes` v2.2, `ishtar-aon-fix` v1.1, AGC yapılandırması; AOSPA Android 15'te ölçüldü). ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Pencere 4 12. denetimdir (ClaudeQB Step 3): 47 alt plan denetlenir. `4 · O4`'te yalnız `Planner-docs/Sub-Planing-Audit.md` yazılır, orkestratör tarafından (`AUD-W`; `run-step3.md:12`); `AUD-D` scout'ları yalnız `local://` yazar. `4 · O0` (keşif, §8.1), `4 · O1` (plan, §8.2), `4 · O2` (kontrat, §8.3, Ek A.8), `4 · O3a` (Faz10) ve `4 · O3b` (Faz 1-9) bitti.

1. **Tek aşama:** plan §1'de `4 · O3b` `done` (`:74`), ilk `pending` `4 · O4` (`:75`; görevler `AUD-D1` ∥ `AUD-D2` ∥ `AUD-D3` -> `AUD-W` -> `GATE4`). Bu oturum yalnız onu yürütür. `4 · O5` (`REV-5`, `SEC-D`, `FIX4`, `C4`, FF, push) bu oturumda başlamaz.
2. **Plan kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Kontrat sabittir:** §8.3 ve Ek A.8 kullanıcısız değiştirilmez; değiştirme ihtiyacı beklenmedik durumdur.
4. **Cihaz:** Pencere 4 cihaza komut göndermez; olgular plan §7.1 `W3P01`-`W3P04`.
5. **Onay kapıları** (plan §0 adım 5; kısa evet/hayır): FF; her push ayrı; cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler. Taslak, birleştirme ve geçit sonucu onay kapısı değildir. Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan (§0 adım 4).
6. **Beklenmedik durum** (plan §0 adım 6): `GATE4`'ün §8.3 madde 6'nın beklediğinden farklı çıkması; birleştirilmiş denetimde P0 ya da P1; açılış ya da taban sapması; kapsamı ya da §8.2-§8.3 kararını değiştiren her seçim; bir `AUD-D` scout'unun `local://` dışına yazması. Kapanış, commit ve bu dosyanın yeniden yazımı yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin. P0/P1 için seçenekler §8.3 madde 6'nın (a) ve (b)'sidir.
7. **Planlı bölme** (beklenmedik durum değildir): taslaklardan sonra bağlam 200k'yı geçerse `GATE4` `4 · O4b`'ye taşınır (plan §1 `:75`; plan §0 adım 7). Bu durumda §1'de `4 · O4` `in_progress` kalır, kalan iş yazılır ve bu dosya `4 · O4b` için yeniden yazılır; kapanış §4 (h) ile yapılır.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/`, `docs/` ve bulgu dosyası İngilizce (Ek A ve ledger metnine kaynaklık eder).

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda ölç; 250k'dan sonra her turda. 300k'dan sonra yeni görev yok; kapanış 400k'dan önce biter.
- **Tahmin** (plan §1): `4 · O4` ≈ 235k. Taslaklardan sonra 200k'yı geçerse `GATE4` `4 · O4b`'ye (§0 adım 7).
- **Ders (`4 · O3b`, PROJECT_LOG §11):** ilk ölçüm 92,8k; gönderim ve `PAT4`'ten sonra 131,7k; üç sonuçtan sonra 182k; bulgu betiğinden sonra 221k; kapanışta ≈ 250k. Büyümenin kaynağı okunan metin ve yazılan betiklerdi: her aralığı bir kez oku.
- **Kazanç:** taslakları `eval` içinde `await read("local://x.md")` ile oku; birleşik dosyayı tek seferde `await write(path, content)` ile yaz (`AUDIT12_FINDINGS.md` böyle genişletildi). Çıktıda yalnız sayılar ve kısa maskeli alıntılar.

## 2. Okuma sırası

Büyük dosyalar bütün okunmaz. Numaralar `4 · O3b` kapanışınındır; içerikle doğrula. 760 karakteri aşan satırlar `:raw` ile okunur.

1. Plan §0 (`:9`-`:44`), §1 (`:73`-`:77`), §3 (`:99`-`:125`).
2. Plan §8.2 kararları (`:845`-`:856`); §8.3 (`:857`-`:917`) bütün, madde 4-7 dikkatle.
3. Ek A.5 (`:1077`-`:1122`; push ve kimlik taraması betiği), A.7 (`:1150`-`:1171`).
4. Skill `claudeqb/0.2.1` (`skills/claudeqb/`): `references/handoffs/run-step3.md` (`:12`, `:17`) ve `references/Third-Planner.md:295`-`:552` yalnız başlıklar ve durum sözcükleri (`:530`-`:537`); metin kopyalanmaz.
5. `Planner-docs/Sub-Planing-Audit.md`: başlıklar (`:1`, `:16`, `:59`, `:103`, `:119`-`:427`) ve durum satırı `:18`.
6. `AUDIT12_FINDINGS.md`: yalnız başlıklar (`awk '/^#/'`); oturumlar `:5` ve `:231`. Tablolar okunmaz (satırlar ~3 KB).
7. PROJECT_LOG §2.6 (`:228`-`:240`) ve §11'in son girdisi (`4 · O3b`, `:1311`-`:1323`).

## 3. Mevcut durum

**Beklenen durum (4 · O3b kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 92 commit. Uç ve kapanış: `Window 4 O3b: Phase 1-9 reviews for the twelfth audit` (`git log --grep '^Window 4 O3b:'` tek commit = uç). Etiket yok, 356 izlenen dosya.
- **Yayın:** `main` = `origin/main` = `081790f`; `origin/main..HEAD` = 5; `git ls-remote origin` üç ref = `081790f`. FF ve push yalnız `4 · O5`'te, `C4`'ten sonra, ayrı onaylarla (plan §8.2).
- **GitHub** (2026-11-17T13:01:43Z-13:01:47Z): dört depo 200; `ishtar_cam_modes` ve `ishtar` özel, ikisi açık. Silme kullanıcıda (`DEC-30`).
- **Değişmeyen dosyalar** (mevcut §3'ten, `4 · O3b`'de değişmedi): `Main-Planing.md` sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, 77.019 B, CRLF, NUL 0, 10 faz, 47 alt plan. Ledger 662 satır, CRLF, NUL 0. Index 443, Ontology 453 (NUL 2: `:313`, `:316`), Comprehension 176, toolchain 246, LF. Audit 437 satır, 57.836 B, LF; durum `:18`; `AUD-W` yeniden yazar.
- **Plan:** 1285 satır, LF; §1 `4 · O3b` `done` (`:74`), `4 · O4` `pending` (`:75`). Çapalar: §8.2 `:797` (kararlar `:845`), §8.3 `:857`, §9 `:918`, §10 `:927`, Ek A `:988`, A.5 `:1077`, A.7 `:1150`, A.8 `:1172`.
- **`AUDIT12_FINDINGS.md`:** 111.017 B, 505 satır, LF, NUL 0; `## Session 4 · O3a` `:5`, `## Session 4 · O3b` `:231`; kimlikler `AUDIT-FIX-58`-`-109` (52 kimlik: P0 0, P1 0, P2 5, P3 47; O3a `-58`-`-89`, O3b `-90`-`-109`).
- **Kapasite:** `reviewer` penceresi 1M; `security-reviewer` penceresi 1M görüldü, kabuğu yok (`4 · O3a`). Taslaklar `local://` dosyalarında; `4 · O4` scout'ları ≤ 4 KB döner.
- **Geçitler ve sürüm:** taban değişmedi (§7); kimlik taraması `prose_mentions=28`; v2.2 / versionCode 13 (`DEC-29`).
- **§13 kuralı** (plan §8.3 madde 5, `:907`; doğrulayıcı V:269, V:1095-1134): eski tablonun 13 kimliği yeni durumlarıyla ve yeniler; 52 yeni kimlik (`AUDIT-FIX-58`-`-109`) da §13'te birer satır olur; öteki 44 kimlik tek cümleyle tabloda değil. P sayıları yalnız `open` ve `accepted` satırlardan çıkar; tablo başlığı tam olarak `Finding ID | Severity | Status | Affected Files | Issue | Required Action` olmalı (aksi halde doğrulayıcı yedek yola düşer). Plan `:907` "yeniler"in kapsamını açıkça yazmaz; bu okuma betikle doğrulanır, sapma beklenmedik durumdur.

## 4. Bu oturum: `4 · O4`

Yazılanlar: `Planner-docs/Sub-Planing-Audit.md` (tam yeniden yazım, yalnız orkestratör); `AUDIT12_FINDINGS.md`'nin başına tarihli birleştirme notu (§8.3 madde 4; bölümler silinmez); plan §1 ve §3 Geçitler (S3-32); PROJECT_LOG §2.6 ve §11; bu dosya; sonra git. Taslaklar `local://` içinde kalır ve commit'e girmez.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 4 O3b: Phase 1-9 reviews for the twelfth audit`; `git log --grep '^Window 4 O3b:'` tek commit = uç; `git rev-list --count HEAD` = 92; `git tag` boş; `git ls-files` = 356; plan §1'de ilk `pending` = `4 · O4`.
Yayın: `git rev-parse main origin/main` = `081790f`; `git rev-list --count origin/main..HEAD` = 5; `git ls-remote origin` üç ref = `081790f`. GitHub: dört depo `gh api -i repos/ahmetxa/<ad>` (UTC; `gh` yolu §8). Tutmayan her şey beklenmedik durumdur.

**(b) Bağlam:** Ek A.7 betiği başta, tabandan sonra, her scout sonucundan sonra ve `AUD-W`'den önce.

**(c) Taban** (bir kez, §7; mevcut değerler `4 · O3b`'de tuttu): `step2`, `step1`, `step3-preflight` `--strict`, V1-V3, kimlik taraması, `--mode step3` (bayraksız ve `--strict`). Sapma beklenmedik durumdur.

**(d) Girdi değişmedi:** `git diff --stat 2f39b73..HEAD -- Planner-docs docs ishtar-cam-modes ishtar-aon-fix scripts CHANGELOG.md .gitignore .gitattributes UNTRACKED-BY-DESIGN.md` boş olmalı. Değilse beklenmedik durumdur.

**(e) Taslaklar** (tek paralel grup, üç `scout`, salt-okur): `AUD-D1` §1-§11, `AUD-D2` §12, `AUD-D3` §13-§15 (§13 kuralı: §3, `:907`). Girdi (§8.3 madde 5): bulgu dosyası (`## Session 4 · O3a` ve `O3b`), eski Audit, Index §3, ledger §4 durum sütunu ve §8.3. Her biri ≤ 4 KB döner; taslak `local://audit-d1.md`, `local://audit-d2.md`, `local://audit-d3.md`. §14 Step 4 istemini yalnız P0 ve P1 0 ise basar (`Third-Planner.md:534`-`:537`). AGC tercih değeri kopyalanırsa `[value withheld]` yazılır.

**(f) `AUD-W`:** üç taslağı `eval`'de birleştir, `Planner-docs/Sub-Planing-Audit.md`'ye `cp` ile yaz, betikle doğrula (§8.3 madde 5):
- H1 `# Sub-Planing Audit` ve 15 `##` başlık birebir, tekil, sıralı (`Third-Planner.md:295`-`:545`); her `##` gövdesi ≥ 20 karakter.
- İlk `status:` satırı §1'in başında yeni durumdur; eski denetimin durumu alıntılanmaz.
- §12: 47 satır, Index §3 sırasıyla, `Faz10.1`-`10.5` dahil; durumlar ledger §4 ile tutarlı: 34 verified -> COMPLETE, 7 SUPERSEDED, `Faz4.6` DEFERRED, `Faz10.x` rdy-a'nın kuyruk satırlarından. Yol depoya göreli; aynı alt plana iki satır yok.
- §13: başlık birebir; 65 satır (13 eski + 52 yeni), öteki 44 kimlik tek cümlede (§3 kuralı); P sayıları yalnız `open` ve `accepted` satırlardan (V:1095-1134).
- Boru sayımı (ham `|`, kaçışlı dahil), LF, NUL 0. Ardından `git diff --stat`: `Planner-docs/` içinde yalnız Audit.
P0 ya da P1 çıkarsa: kapanış yok, §0 adım 6.

**(g) `GATE4`** (§8.3 madde 6): `--mode all` çıkış 0 (`p0_findings=0`, `p1_findings=0`); `--mode step3 --strict`'te yalnız `strict_warning=step4_has_nonblocking_warnings` kabul (denetim `PASS_WITH_WARNINGS` kaldıkça çıkış 1); `step2`, `step1`, `step3-preflight` `--strict` 0; V3 değişmez; kimlik taraması PASS. Yeni sayılar (uyarılar, P2/P3, `subplan_count`, `index_reference_count`, `phase_folder_count`, `prose_mentions`) plan §3 Geçitler'e yazılır (S3-32) ve yeni taban olur. Sonuç §8.3'ün beklediğinden farklıysa beklenmedik durumdur.

**(h) Kapanış** (plan §0 adım 4; beklenmedik durum yoksa sorulmadan):
- Plan §1'de `4 · O4` `done` (commit başlığıyla); ilk `pending` `4 · O5`. Plan commit başlığı adlandırmaz; öneri, plan dışı: `Window 4 O4: merged audit and gates for the twelfth audit`.
- PROJECT_LOG §2.6 aynı 13 satırla (`:228`-`:240`) yeniden yazılır; §11'e girdi (bağlam ölçümleri dahil).
- Bu dosya `4 · O5` için ≤ 20 KB yeniden yazılır.
- Değişen dosyalarda bayt, boru ve kimlik taraması (§7, Ek A.5); `AUDIT12_FINDINGS.md` LF, NUL 0; `git diff --stat` ile `Planner-docs/` içinde yalnız `Sub-Planing-Audit.md`.
- Yerel commit `eval` `commit` ad alanıyla (`draft`, `take`, `commit`); değişen dosyaları açıkça `take` et. Sonra 93 commit, 356 izlenen dosya. Kullanıcıya `git show --stat` özeti ve yeni pencere talimatı.

**Kabul:** açılış ve taban tuttu; üç taslak ve birleştirme betikle doğrulandı; `GATE4` sonuçları plan §3'te; §1, PROJECT_LOG ve bu dosya güncel; §13 tablosu 65 satır ve başlığı tam; kapanış commit'i yerel.

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
11. Cihaz komutu: Pencere 4 (12. denetim) hiç göndermez; `4 · O3b` ve `4 · O4` dahil. Fiziksel eylemler kullanıcıda ve onaylı.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`; `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla.
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik değeri yazma ya da geri kazanma; tarama yalnız sayı ve konum basar.
20. Sıcak noktayı alt ajana yazdırma: ledger, `Main-Planing.md`, Index, Audit, `AUDIT12_FINDINGS.md`, Ontology, Comprehension, toolchain belgesi, `CHANGELOG.md`, sürüm yerleri, manifest, `.gitignore`, `.gitattributes`, `snapshots/`, plan, PROJECT_LOG ve git (plan §3). `4 · O4`'te Audit'i yalnız orkestratör yazar; `AUD-D` scout'ları yalnız `local://` yazar.
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

| Kontrol | Taban (`4 · O0`, 2026-11-16T22:11Z; `4 · O1`-`4 · O3b`'de tuttu; `4 · O4` başında hâlâ bu) |
|---|---|
| `step2`, `step1`, `step3-preflight` `--strict` | Bulgu yok, çıkış 0 |
| V1 `--mode all` | Yalnız `warning=step4_has_nonblocking_warnings=P2:1,P3:9`; `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning`; çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=28` → PASS; `prose_mentions` artabilir |
| Boru ve bayt | Boru dışı yalnız plan `:183`, `:1019` ve ledger satırları; ledger ve `Main-Planing.md` CRLF, öteki LF; NUL yalnız Ontology'de (2) |

- `AUD-W` denetim sayılarını değiştirir; yukarıdaki satırlar `GATE4`'e kadar geçerli taban olarak okunur. `GATE4` yeni tabanı plan §3'e yazar.
- Kimlik taraması Ek A.5 betiğiyle, kökten `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` politikası `cat`, `head`, `tail`, `grep` ve `find`'ı engelleyebilir: `awk`, `read`/`grep`/`glob` araçları ya da `py -3`.
- **Okuma aracı:** 768 karakteri aşan satırları keser, büyük dosyada blok atlar; tek satır bile büyük blok bağlamı dökebilir (`4 · O3a`'da 48 KB). Tek satır için `:raw:N-N`.
- **Boru sayımı:** ham `|` (kaçışlı dahil) sayılır; bu, plan `:183`, `:1019` ve ledger satırlarını verir. Kaçışlı olanları ayırmak tabloyu yanlış gösterir.
- **AGC değerleri:** ajanlar tercih değerini kopyalayabilir: `[value withheld]` ile maskele; `pref_*=` taraması maskeyi yok sayar, maskesiz eşleşme `0` olmalı.
- **`reviewer`:** `bash`'te `grep` kullanamıyor, `grep` aracını kullanır.
- **`security-reviewer`:** kabuğu yok; `4 · O5` `SEC-D` için: orkestratör diff'i önce bir `local://` dosyasına yazar ya da `reviewer` kullanımını kullanıcıya sorar.
- **`local://` oturumlar arasında kaybolur** (§0 adım 8): taslaklar aynı oturumda `AUD-W`'de tüketilir.
- **Yeniden çalıştırma:** `local://audit-dN.md` üzerine yazılır; önce yedek (`local://audit-dN-r1.md`).
- **SUPERSEDED 7'dir:** `Faz7.2`, `7.3`, `8.1`, `8.3`, `Faz4.1`, `Faz4.7`, `Faz6.1`; `Faz4.6` DEFERRED (karar 2).
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe`.
- **`--grep` satır başına bağlanır** (`'^Window 4 O3b:'`) ve gövde satırlarını da eşler.
- **Commit:** `eval`'deki `commit` ad alanıyla; `git add`/`git commit` yok. `cp` ile konan `Sub-Planing-Audit.md`, `NEXT_PROMPT.md` ve `AUDIT12_FINDINGS.md` dahil değişen dosyaları açıkça `take` et.
- **`.gitattributes`:** `* -text` bayt korur, `*.md` için `eol=lf` yok: LF baytla doğrulanır.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri, yayın doğrulaması ve dört depo (§4 a); plan §1'de ilk `pending` `4 · O4`.
3. Bağlam (§4 b), taban (§4 c) ve girdi kontrolü (§4 d).
4. Kısa Türkçe "hazırım" özeti (ölçülenler, yayın durumu); §3'teki §13 kuralını uygula, soru sorma; `AUD-D` taslakları başlayabilir.
5. §4 (e) üç scout'u tek grupta gönder; (f) `AUD-W`; (g) `GATE4`; (h) kapanış.

---
