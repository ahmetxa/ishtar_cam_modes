# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> Pencere 4 · O3a'nın kapanış commit'inde yazıldı. Aşama: **Pencere 4 · O3b — İnceleme: Faz 1–9 (`cov-b` ∥ `cov-c` ∥ `cov-d` ∥ `PAT4` → `FND-b`; plan §8.3)**. Özettir; nihai kaynak plan, ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`) için root tabanlı kamera özelleştirmesidir (`ishtar-cam-modes` v2.2, `ishtar-aon-fix` v1.1, AGC yapılandırması; AOSPA Android 15'te ölçüldü). ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Pencere 4 12. denetimdir (ClaudeQB Step 3): 47 alt plan denetlenir, yalnız `Planner-docs/Sub-Planing-Audit.md` yazılır (`4 · O4`'te). `4 · O0` (keşif, §8.1), `4 · O1` (plan, §8.2), `4 · O2` (kontrat, §8.3, Ek A.8) ve `4 · O3a` (Faz10) bitti.

1. **Tek aşama:** plan §1'de `4 · O3a` `done` (`:73`), ilk `pending` `4 · O3b` (`:74`; görevler `cov-b` ∥ `cov-c` ∥ `cov-d` ∥ `PAT4` → `FND-b`). Bu oturum yalnız onu yürütür. `4 · O4`'e asla başlanmaz.
2. **Plan kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Kontrat sabittir:** §8.3 ve Ek A.8 kullanıcısız değiştirilmez; değiştirme ihtiyacı beklenmedik durumdur.
4. **Cihaz:** Pencere 4 cihaza komut göndermez; olgular plan §7.1 `W3P01`–`W3P04`.
5. **Onay kapıları** (plan §0 adım 5; kısa evet/hayır): FF; her push ayrı; cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler. İnceleme ve bulgu dosyası onay kapısı değildir. Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan (§0 adım 4).
6. **Beklenmedik durum** (plan §0 adım 6): P0/P1 denetim bulgusu, `PAT4`'te S5/S6 isabeti ya da kalibrasyondan sapma, dördüncü reviewer ihtiyacı, kapsamı ya da §8.2–§8.3'ün bir kararını değiştiren her seçim dahil. Kapanış, commit ve bu dosyanın yeniden yazımı yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/`, `docs/` ve bulgu dosyası İngilizce (Ek A.3).

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok; kapanış 400k'dan önce biter. Hijyen: §0 adım 8–9.
- **Tahmin** (plan §1): `4 · O3b` ≈ 195k.
- **Ders (`4 · O3a`):** ilk ölçüm 95,7k; üç sonuçtan sonra 159k; dördüncü reviewer'dan önce 209k; bulgu dosyasından sonra 260k; kapanışta ≈ 310k. Büyük kayıp: `read` aracı planın tek satırını (`:73`) okurken 48 KB blok bağlamı döktü; tek satır için `:raw:N-N` ya da `awk 'NR==N'`. Kazanç: görev metnini `eval` içinde plandan dilimleyip `tool.task` ile göndermek ve bulgu dosyasını `eval` betiğiyle yazmak.

## 2. Okuma sırası

Büyük dosyalar bütün okunmaz (`grep '^##'`). Numaralar `4 · O3a` kapanışınındır; içerikle doğrula. 760 karakteri aşan satırlar `:raw` ile okunur.

1. Plan §0 (`:9`–`:44`), §1 (`:46`–`:80`), §3 (`:99`–`:125`; geçitler, Gizlilik, Git, Adlandırma).
2. Plan §8.2'nin kararları (`:845`–`:856`); §8.3 (`:857`–`:917`) bütün.
3. Ek A.8 başı ve A.8.1 (`:1172`–`:1207`), A.8.2 kısaltma paragrafı (`:1210`), cov-b (`:1233`–`:1235`), cov-c (`:1237`–`:1243`), cov-d (`:1245`–`:1247`), A.8.3 (`:1249`–`:1285`, `PAT4` betiği); hepsi `:raw`.
4. Ek A.5 (`:1077`; push, kimlik taraması betiği), A.7 (`:1150`).
5. Skill (§7'deki `$V` yolunun `skills/claudeqb/` dizini): yalnız `references/handoffs/run-step3.md`.
6. PROJECT_LOG §2.6 (`:228`), §11'in son girdisi (`4 · O3a`, `:1297`).
7. `AUDIT12_FINDINGS.md`: yalnız başlıklar (`grep '^#'`) ve `### Runs` (`:179`) eşleme tablosunun biçimi.

## 3. Mevcut durum

**Beklenen durum (4 · O3a kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 91 commit. Uç ve kapanış: `Window 4 O3a: Phase 10 reviews for the twelfth audit` (`git log --grep '^Window 4 O3a:'` tek commit = uç). Etiket yok, 356 izlenen dosya.
- **Yayın:** `main` = `origin/main` = `081790f` (C3); `origin/main..HEAD` = 4; `git ls-remote origin`: `HEAD`, `main`, `integrate/impl-96` = `081790f`. FF ve push yalnız `4 · O5`'te, `C4`'ten sonra, ayrı onaylarla (plan §8.2).
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez); silinecek üç depo (`DEC-30`): `ishtar`, `android_local_manifests`, `android_device_xiaomi_ishtar` (hepsi `ahmetxa/`). 2026-11-17T12:20:48Z–12:20:55Z: dördü 200 (`ishtar_cam_modes` ve `ishtar` özel, öteki ikisi açık).
- **`Main-Planing.md`** (değişmedi): sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, 77.019 bayt, CRLF, NUL 0, 10 faz. Alt plan 47.
- **Öteki dosyalar** (değişmedi): ledger 662 satır, CRLF, NUL 0; Index 443, Ontology 453 (NUL 2: `:313`, `:316`), Comprehension 176, toolchain 246, LF. Audit 437 satır, 57.836 B, LF; durum `:18`, son kimlik `AUDIT-FIX-57`.
- **Plan:** 1285 satır, LF; §1 `4 · O3a` `done` (`:73`), `4 · O3b` `pending` (`:74`); §8.2 `:797`, §8.3 `:857`, §9 `:918`, §10 `:927`, Ek A `:988`, A.5 `:1077`, A.7 `:1150`, A.8 `:1172` (A.8.1 `:1176`, A.8.2 `:1208`, A.8.3 `:1249`). Boru dışı satırlar yalnız `:183`, `:1019`.
- **`AUDIT12_FINDINGS.md`:** 56.574 B, 229 satır, LF, NUL 0; `## Session 4 · O3a` (`:5`); kimlikler `AUDIT-FIX-58`–`-89` (P2 5, P3 27); `FND-b` `AUDIT-FIX-90`'dan sürer.
- **Kapasite:** `reviewer` penceresi 1M. `security-reviewer` penceresi 1M görüldü ama kabuğu yok. Bu oturumun çalışmaları 363.276–385.848 B.
- **Geçitler ve sürüm:** taban değişmedi; kimlik taraması `prose_mentions=28` (artabilir); v2.2 / versionCode 13 (`DEC-29`).

## 4. Bu oturum: `4 · O3b`

Audit, alt planlar, ledger ve Ek A yazılmaz. Yazılanlar: `AUDIT12_FINDINGS.md`'nin sonuna `## Session 4 · O3b`; plan §1; PROJECT_LOG §2.6 ve §11; bu dosya; sonra git.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 4 O3a: Phase 10 reviews for the twelfth audit`; `git log --grep '^Window 4 O3a:'` tek commit = uç; `git rev-list --count HEAD` = 91; `git tag` boş; `git ls-files` = 356; plan §1'de ilk `pending` = `4 · O3b`.
Yayın: `git rev-parse main origin/main` = `081790f`; `git rev-list --count origin/main..HEAD` = 4; `git ls-remote origin` üç ref = `081790f`. Snapshot ve dosyalar §3'teki gibi.
GitHub: dört depo `gh api -i repos/ahmetxa/<ad>` (UTC; `gh` yolu §8). `ishtar_cam_modes` 200 değilse beklenmedik durum; üç depodan biri 404 ise kaydedilir (PROJECT_LOG §2.6, §11). Tutmayan her şey beklenmedik durumdur.

**(b) Bağlam:** Ek A.7 betiği başta, tabandan sonra ve her reviewer sonucundan sonra.

**(c) Taban** (bir kez, §7): `step2`, `step1`, `step3-preflight` `--strict`, V1–V3, kimlik taraması, `--mode step3` (bayraksız ve `--strict`); sapma beklenmedik durumdur.

**(d) Girdi değişmedi:** `git diff --stat 2f39b73..HEAD -- Planner-docs docs ishtar-cam-modes ishtar-aon-fix scripts CHANGELOG.md .gitignore .gitattributes UNTRACKED-BY-DESIGN.md` boş olmalı. Değilse `W4O2P02` baytları ve satır atıfları geçersiz olabilir: beklenmedik durum.

**(e) Gönderim** (tek paralel grup): `cov-b`, `cov-c`, `cov-d` (üçü `reviewer`). Metin = Ek A.8.1 + kısaltma paragrafı + çalışmanın bloğu, aynen (§8.3 madde 1): `eval` içinde plandan dilimlenir, `tool.task` ile gönderilir (ortak bağlam = A.8.1 + kısaltma paragrafı, görev = blok).
- Baytlar (`W4O2P02`): cov-b 385.848, cov-c 363.276, cov-d 372.294 B; ek okuma ≤ 10 KB ile her biri ≤ 400 KB.
- Dönüş ≤ 4 KB; ayrıntı `local://<çalışma>.md`. Dönüşte `status`, kabul satırları, `contract_deviations` ve bulgu sayıları okunur.
- **`PAT4`** (orkestratör, A.8.3 betiği, reviewer'larla paralel): kökten `py -3`, önce sayım, sonra `--locations`; satır metni basılmaz. Kalibrasyon `W4O2P01`: 164 isabet (S1 17, S2 3, S3 12, S7 1, R1 6, R3 20, R4 81, R5 24; ötekiler 0). Sapma ya da S5/S6 isabeti beklenmedik durumdur (S5/S6 satır okunmadan P0 adayı). İsabetler (desen, dosya) gruplarıyla bulguya (`PAT4-<desen>-NN`) ya da gerekçeli `not_applicable`'a döner (§8.3 madde 8).

**(f) Taşma ve P0/P1:** `partial` dönüş ya da bağlam hatasında çalışma ikiye bölünür, yarılar taze gönderilir (§8.3 madde 2); bu dördüncü reviewer demektir: beklenmedik durum. `4 · O3a`'da yöntem nedenli `partial` kullanıcıya soruldu, seçim (b) oldu (§5). 429 ya da 402 ile duran ajan canlanmaz, taze gönderilir. P0 ya da P1 denetim bulgusu beklenmedik durumdur: kapanış yok; seçenekler §8.3 madde 6'nın (a)'sı (önerilen: kaydet, Step 4 önkoşulu kapalı, Step 3.1 onarım koşusu) ve (b)'si (kanıt bulguyu düşürürse gerekçe yazılır, akış sürer).

**(g) `FND-b`** (orkestratör; §8.3 madde 3, 4, 7): `AUDIT12_FINDINGS.md`'nin sonuna `## Session 4 · O3b`, altında `### Findings` (`4 · O3a` ile aynı sütunlar), `### Dispositions`, `### Section notes` (çalışma başına `####`), `### Runs` (çalışma, durum, bayt, `partial` notu, eşleme), `### PAT4` (desen sayıları kalibrasyonla, gruplar ve hükümleri).
- Kimlik: kalıcı `AUDIT-FIX-90`'dan, sıra cov-b, cov-c, cov-d, `PAT4`, çalışma içinde geçici sırayla. Aynı konudaki iki geçici bulgu tek kimliğe gider; reddedilen kimlik almaz, gerekçesiyle `rejected` yazılır. Eşleme tam: her geçici kimlik bir satır.
- §8.3 Dağıtım tablosunun cov-b, cov-c, cov-d ve orkestratör satırlarındaki her madde (S3-31 → `AUD-W`, S3-32 → `GATE4`) bir disposition taşır. `4 · O3a`'dan kalan `AUDIT-FIX-57` kalanı (`CQ-13`, Ontology invariant 11, `docs/reverse-engineering-toolchain.md:220`) cov-c'nin çıktısıyla dispositionlanır.
- Yöntem: `local://` dosyaları `eval`'de ayrıştırılır; `pref_*=` değerleri gizlenir. Tarama (tercih değeri, sır ataması, kimlik anahtarı, 15 hane, IPv4, boyut, kaçışlı boru) ve boru sayımı temizse bölüm tek seferde yazılır, yeniden okunmaz; LF ve NUL baytla doğrulanır.

**(h) Kapanış** (plan §0 adım 4; beklenmedik durum yoksa sorulmadan):
- Plan §1'de `4 · O3b` `done` (commit başlığıyla); ilk `pending` `4 · O4`.
- PROJECT_LOG §2.6 aynı satır sayısıyla (`:228`–`:240`, 13 satır) yeniden yazılır, §11'e girdi (bağlam ölçümleri dahil); bu dosya `4 · O4` için ≤ 20 KB yeniden yazılır.
- Değişen dosyalarda bayt, boru ve kimlik taraması (§7); `AUDIT12_FINDINGS.md` LF, NUL 0; `git diff --stat` ile Audit dahil `Planner-docs/` değişmedi (§8.3 madde 7).
- Yerel commit `Window 4 O3b: Phase 1-9 reviews for the twelfth audit` (`eval` `commit` ad alanı; değişen dosyaları açıkça `take` et); sonra yine 356 izlenen dosya. Kullanıcıya `git show --stat` özeti ve yeni pencere talimatı.

**Kabul:** açılış ve taban tuttu; üç çalışma tam (ya da kontrata göre bölündü); `PAT4` kalibrasyonu tuttu; `## Session 4 · O3b` tam eşleme ve dispositionlarla yazıldı; §1, PROJECT_LOG ve bu dosya güncel; kapanış commit'i yerel.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7–§8.3, ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| K1 `Kullanim.txt` | (b): v2.3'te düzeltilir | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K5/K6 üç depo | Silinecek; kullanıcı siler; ölçülür | `DEC-30` |
| K7 HyperOS 4 yönü | (a) modülü uyarla; "ClaudeQB Phase 10", Faz 7 ve 8 emekli | `DEC-32` |
| K9 50MP HAL | Hayır, şimdilik; sensör katmanı sürer | `DEC-33` |
| Sekiz soru | Yanıtlandı (2026-11-15) | plan §7 |
| Pencere 3 planı | Onaylandı (2026-11-15, "onay") | plan §7.2 |
| Step 1 metni | Onaylandı (2026-11-15T14:10Z, "onay") | `Main-Planing.md` |
| Step 2 kontratı | Onaylandı (2026-11-15; dal sürer) | plan §7.3 |
| `3 · O3a` planı | Onaylandı (2026-11-15, "onay") | plan §7.2 |
| `3 · O3a` incelemesi | Düzeltmeler "hepsi" (2026-11-16) | plan §7.3, §10 |
| `3 · O3b` planı | Onaylandı (2026-11-16, "onay") | plan §1 |
| `3 · O3b` incelemesi | P1 3, P2 4, P3 9; "hepsi" | plan §7.3, §10 |
| `3 · O4` planı | Onaylandı (2026-11-16); kurallar §5.5 | plan §1 |
| `3 · O4` incelemesi | Teyit "ekle"; P2 2, P3 5 düzeltildi | plan §10 |
| `3 · O4` takibi | Kaydet (2026-11-16, "takip") | plan §10 |
| `3 · O5` | Plan "onay", teyit "ekle", düzeltme "hepsi" | plan §1, §10 |
| `4 · O0` | Sorusuz kapandı (C3 push edilmişti) | plan §1, §8.1 |
| `4 · O1+O2` birleşimi | "evet" (2026-11-17); onayda bağlam 200k'yı geçti, `O2` ayrı oturum | plan §8.2 |
| `4 · O1` planı | "onay" (2026-11-17); seçenek C ve sekiz karar öneriyle | plan §8.2 |
| `4 · O2` | Sorusuz kapandı (kontrat onay kapısı değil) | plan §1, §8.3 |
| `4 · O3a` | sec-a `partial`: (b) `reviewer` ile bu oturumda yeniden, dördüncü reviewer (2026-11-17) | plan §1, PROJECT_LOG §11 |
| Snapshot | Step 2 durmaz; etkin plan bugünkü `Main-Planing.md` | plan §7.3, ledger §3 |
| Atıf | Koşu 21'in seçimi | ledger §8 |
| Yayın | C3 push edildi (2026-11-16, ayrı onaylarla); sonraki FF ve push yalnız `4 · O5`'te, `C4`'ten sonra | plan §8.2, PROJECT_LOG §11 |

## 6. Değişmezler — asla yapma

Madde 1–10 AOSPA A15'te ölçülmüş kurallardır; HyperOS 4'te ölçülmeden varsayılmaz, ihlal de edilmez (PROJECT_LOG §5).

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
11. Cihaz komutu: Pencere 4 (12. denetim) hiç göndermez, `4 · O3b` dahil. Fiziksel eylemler kullanıcıda ve onaylı.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`, `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla.
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik değeri yazma ya da geri kazanma; tarama yalnız sayı ve konum basar.
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

| Kontrol | Taban (`4 · O0`, 2026-11-16T22:11Z; W4F02, W4F03; `4 · O1`–`4 · O3a`'da tuttu) |
|---|---|
| `step2`, `step1`, `step3-preflight` `--strict` | Bulgu yok, çıkış 0 |
| V1 `--mode all` | Yalnız `warning=step4_has_nonblocking_warnings=P2:1,P3:9`; `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning`; çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| `--mode step3` (ölçüm, taban değil) | Çıkış 0, `audit_status=PASS_WITH_WARNINGS`, P0 0, P1 0, P2 1, P3 9; `--strict` çıkış 1 (`strict_warning`) |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=28` → PASS; `prose_mentions` artabilir |
| Boru ve bayt | Boru dışı yalnız plan `:183`, `:1019` ve ledger `:473`, `:490`–`:495`, `:501`, `:506`, `:507`; ledger ve `Main-Planing.md` CRLF, öteki LF; NUL yalnız Ontology'de (2) |

- Kimlik taraması `%TEMP%/idscan.py` ile (yoksa Ek A.5'ten yazılır), kökte `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` politikası `cat`, `head`, `tail`, `grep` ve `find`'ı engeller: `awk`, `read`/`grep`/`glob` araçları ya da `py -3`.
- **Okuma aracı:** 768 karakterden uzun satırları keser, büyük dosyada blok atlar; tek satırda bile büyük blok bağlamı dökebilir (`4 · O3a`'da 48 KB).
- **Reviewer girdisi:** yalnız A.8.1 + kısaltma paragrafı + blok; plan satırı ya da PROJECT_LOG eklenmez. Oturum başına ≤ 3 reviewer. `task`'ın 100K sınırı geçerlidir.
- **`reviewer`:** `bash`'te `grep` kullanamıyor, `grep` aracını kullanır. Ajanlar ayrıntı dosyasına tercih değeri kopyalayabilir: FND temizler (`pref_*=` taraması).
- **`security-reviewer`:** kabuğu yok, A.8.1 okuma yordamı (`wc`, `awk`) çalışmaz; `4 · O5` `SEC-D` için not.
- **Yeniden çalıştırma:** `local://<çalışma>.md` üzerine yazılır; önce yedek (`local://<çalışma>-r1.md`), geçici kimlikler `(r1)`/`(r2)` ile ayrılır.
- **`local://` oturumlar arasında kaybolur** (§0 adım 8): `FND-b` bulgu dosyasını aynı oturumda yazar.
- **SUPERSEDED 7'dir:** `Faz7.2`, `7.3`, `8.1`, `8.3`, `Faz4.1`, `Faz4.7`, `Faz6.1`; `Faz4.6` DEFERRED (karar 2).
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe`.
- **`--grep` satır başına bağlanır** (`'^Window 4 O3b:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`draft`, `take`, `commit`); `git add`/`git commit` yok. `cp` ile konan `NEXT_PROMPT.md` ve `AUDIT12_FINDINGS.md` dahil değişen dosyaları açıkça `take` et.
- **`.gitattributes`:** `* -text` bayt korur, `*.md` için `eol=lf` yok: LF baytla doğrulanır.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri, yayın doğrulaması, snapshot ve dört depo (§4 a); plan §1'de ilk `pending` `4 · O3b`.
3. Bağlam (§4 b), taban (§4 c) ve girdi kontrolü (§4 d).
4. Kısa Türkçe "hazırım" özeti (ölçülenler, yayın durumu); soru yok, devam.
5. §4 (e) üç reviewer'ı tek grupta gönder, `PAT4`'ü paralel çalıştır; (f) gerekirse böl; (g) `FND-b`; (h) kapanış.

---
