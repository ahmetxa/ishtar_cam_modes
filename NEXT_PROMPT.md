# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> Pencere 4 · O0'ın kapanış commit'inde yazıldı. Aşama: **Pencere 4 · O1+O2 — 12. denetimin planı ve denetim kontratı (birleşik; plan §8, §8.1)**. Özettir; nihai kaynak plan, ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`) için root tabanlı kamera özelleştirmesidir (`ishtar-cam-modes` v2.2, `ishtar-aon-fix` v1.1, AGC yapılandırması; AOSPA Android 15'te ölçüldü). ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Pencere 4 12. denetimdir (ClaudeQB Step 3): 47 alt plan denetlenir, yalnız `Planner-docs/Sub-Planing-Audit.md` yazılır. `4 · O0` bitti; keşif envanteri plan §8.1 (`W4OPN`, `W4F01`–`W4F27`).

1. **Tek aşama:** plan §1'de `4 · O0` `done` (`:70`), ilk `pending` `4 · O1+O2` (`:71`). Bu oturum yalnız onu yürütür. Birleşimi açılışta kullanıcı tahminle onaylar (W4F26: formülle ≈ 190k, kalibrasyonla 240–265k; §1). Onaylanmazsa yalnız `O1` yürür ve kapanır (§0 adım 4). `O1` plan onayıyla biter (form "onay"). `O3`'e asla başlanmaz.
2. **Plan kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** Pencere 4 cihaza komut göndermez; olgular plan §7.1 `W3P01`–`W3P04`.
4. **Onay kapıları** (plan §0 adım 5; kısa evet/hayır): birleşim (açılışta); `O1` sonunda plan onayı; FF; her push ayrı; cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler. Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan (§0 adım 4).
5. **Beklenmedik durum** (plan §0 adım 6): kapanış, commit ve bu dosyanın yeniden yazımı yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/` (ledger ve Audit dahil) ve `docs/` İngilizce (Ek A.3).

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): bağlamı Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok: işi doğrula, adım 7 ile kapan; kapanış 400k'dan önce biter.
- **Tahmin** (W4F26): 35k açılış + `O1` 6 × 10k + `O2` 8 × 12k ≈ 190k; kalibrasyonla 240–265k (`3 · O0` 233k/185k, `3 · O5` 267k/215k; `4 · O0`'ınki PROJECT_LOG §11). Kontrat taslaklarını task ajanı `local://`'a yazarsa birleşim sığar. `O1` onayından sonra bağlam 300k'yı geçtiyse `O2`'ye başlanmaz: `O1` kapanır, `4 · O2` ayrı §1 satırı ve oturum olur (§0 adım 7).
- **Hijyen:** plan §0 adım 8–9 (20 KB üstü okuma scout'a, dönüş ≤ 4 KB `local://`'a, dar `:N-M`, satır ≤ 600 B, `todo` ≤ 8).

## 2. Okuma sırası

Plan, PROJECT_LOG, ledger, Index, Audit, Ontology ve Comprehension bütün okunmaz; bölüm başları `grep '^##'` ile. Numaralar `4 · O0` kapanışınındır; içerikle doğrula.

1. Plan §0 (`:9`–`:45`), §1 (`:46`–`:75`), §3 (`:94`–`:119`; geçitler, Gizlilik, Git, Adlandırma).
2. Plan §8 (`:747`–`:755`) ve §8.1 envanteri (`:756`–`:790`; 13,8 KB).
3. Emsaller: §7.2 (`:536`–`:560`; aşama planı, soru-öneri-yanıt), §7.3 (`:668`–`:690`; kontrat tabloları).
4. Ek A.5 (`:950`; push, kimlik taraması betiği), A.7 (`:1023`); §10 (`:800`) yalnız `grep -n '12. denetim'`.
5. Skill (§7'deki `$V` yolunun `skills/claudeqb/` dizini): `references/handoffs/run-step3.md` (roller `:17`, durma `:15`); `references/Third-Planner.md` `:295`'ten (şablon; §15 `:545`); `references/subagent-playbook.md:19-25`.
6. `$V` satırları: yalnız W4F10–W4F14'te anılan aralıklar, dar okumayla.
7. PROJECT_LOG §2.6 (`:228`), §5.5 (`:712`), §11'in `4 · O0` girdisi (sonda).

## 3. Mevcut durum

**Beklenen durum (4 · O0 kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 88 commit. Uç ve kapanış: `Window 4 O0: discovery for the twelfth audit` (`git log --grep '^Window 4 O0:'` tek commit = uç). Etiket yok, 355 izlenen dosya.
- **Yayın:** `main` = `origin/main` = `081790f` (C3; push 2026-11-16T22:05:35Z); `origin/main..HEAD` = 1; `git ls-remote origin`: `HEAD`, `main`, `integrate/impl-96` = `081790f`. FF ve push `4 · O0`'da sorulmadı (emsal: Pencere 3 `3 · O5`'te push etti); zamanını `4 · O1+O2` planı belirler.
- **`4 · O0`:** açılış `W4OPN`; taban tuttu; S1–S3 ilk gönderimde 429 ile durdu, taze gönderildi; soru sorulmadı; ayrıntı PROJECT_LOG §11.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez; 200 olmalı); silinecek üç depo (`DEC-30`): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. Son ölçüm 2026-11-16T22:10Z: dördü 200.
- **`Main-Planing.md`** (değişmedi): sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, 77.019 bayt, CRLF, NUL 0, 10 faz. Alt plan 47 (1.141.813 B; W4F04).
- **Ledger:** 662 satır, CRLF, NUL 0. §4: 34 `verified`, 1 `implemented` (`Faz4.6`), 5 `planned` (`Faz10.1`–`Faz10.5`), 7 `superseded`; §8 `DEC-33`.
- **Öteki dosyalar:** Index 443, Ontology 453 (NUL 2: `:313`, `:316`), Comprehension 176, toolchain 246, hepsi LF. Audit 11. denetimdir: 437 satır, 57.836 B, LF; durum `:18`, son kimlik `AUDIT-FIX-57` (W4F09).
- **Plan:** 1043 satır; §1 `4 · O0` `done` (`:70`), `4 · O1+O2` `pending` (`:71`); §8.1 `:756`–`:790`. Boru dışı satırlar yalnız `:177`, `:892` (önce `:174`, `:854`).
- **Geçitler:** taban değişmedi (W4F02); kimlik taraması `prose_mentions=26` (artabilir). `--mode step3`: çıkış 0; `--strict` çıkış 1 (W4F03, W4F13).
- **Sürüm ve telefon:** v2.2 / versionCode 13 (`DEC-29`); HyperOS 4, SukiSU-Ultra v4.3.0-r1 (plan §7.1, PROJECT_LOG §2.3).
- **Araçlar:** `%TEMP%/idscan.py` yoksa Ek A.5 betiğinden yeniden yazılır.

## 4. Bu oturum: `4 · O1+O2`

Audit ve alt planlar yazılmaz, reviewer çalışmaz. Yazılanlar: plan §8.2, §8.3, §1, §3 Adlandırma (gerekirse §8, §10), PROJECT_LOG §2.6 ve §11, bu dosya; sonra git.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 4 O0: discovery for the twelfth audit`; `git log --grep '^Window 4 O0:'` tek commit = uç; `git rev-list --count HEAD` = 88; `git tag` boş; `git ls-files` = 355; plan §1'de ilk `pending` = `4 · O1+O2`.
Yayın: `git rev-parse main origin/main` = `081790f`; `git rev-list --count origin/main..HEAD` = 1; `git ls-remote origin` üç ref = `081790f`. Snapshot ve dosyalar §3'teki gibi.
GitHub: dört depo için `gh api -i repos/ahmetxa/<ad>` (UTC; ilk satır HTTP durumu). `ishtar_cam_modes` 200 değilse beklenmedik durum; üç depodan biri 404 ise kaydedilir (PROJECT_LOG silme cümleleri, §2.6, §11). Ölçüm §8.2'nin ilk satırıdır (öneri `W4O1OPN`). Tutmayan her şey beklenmedik durumdur.

**(b) Bağlam:** Ek A.7 betiği oturum başında; birleşim sorusu bu ölçümle sorulur.

**(c) Taban** (bir kez, §7): `step2`, `step1`, `step3-preflight` `--strict`, V1–V3, kimlik taraması ve `--mode step3` (bayraksız ve `--strict`); sapma beklenmedik durumdur.

**(d) O1 — aşama ve görev planı** (yeni plan §8.2; emsal §7.2):
- Tablo tahmin (k) sütunuyla. Oturumlar: `4 · O3a`… (reviewer çalışmaları W4F06 dilimleriyle; W4F07'nin 12 ya da 6 çalışma seçenekleri ve `cov-b` riski), `4 · O4` (birleştirme ve geçitler; ≈ 235k, bölünebilir), `4 · O5` (son inceleme, kapanış; FF ve push yeri). Oturum başına ≤ 240k, en çok üç reviewer.
- W4F27 kararları (1)–(8) tek formda, öneriyle: (1) §8 `:751` geçit lafzı (öneri: "yalnız `strict_warning`", W4F13); (2) 7 SUPERSEDED, `Faz4.6` DEFERRED (öneri: 7, W4F08); (3) readiness ve security yalnız Faz10, Faz1–9 için orkestratörün desen taraması (öneri: evet, W4F06); (4) bulgu dosyası (öneri (a): kökte İngilizce, LF; W4F25);
- (5) kuyruk (öneri: 47 satır yürütme sırasıyla, `Faz10.1`–`10.5` dahil; W4F11); (6) `AUDIT-FIX-22`, `-37`, `-50` sahipleri (öneri: W4F23); (7) REV-3 P3'leri (ledger `:615`–`:618`; öneri: coverage girdisi); (8) `[ÇIKARIM]` satırları (öneri: dilimin reviewer'ı doğrular).
- Görev kimlikleri ve faz kapanış commit'inin adı (öneri `C4`) §3 Adlandırma'ya. Onay form "onay"; yanıtlar tarihle §8.2'ye; §1'e `4 · O3a`…`4 · O5` satırları `pending` ve tahminle.

**(e) O2 — denetim kontratı** (yeni plan §8.3; emsal §7.3):
- **Reviewer girdisi:** ortak bağlam (İngilizce görev metni, rol, şablon, izinli değerler) ve çalışma başına dosya listesi ≤ 400 KB; ledger §4 dilim baytları ölçülür (W4F05'in `[ÇIKARIM]`'ı kapanır); plan ve PROJECT_LOG bütün verilmez.
- **Çıktı biçimi:** dönüş ≤ 4 KB, ayrıntı `local://`; bulgular §13 sütunlarıyla (Finding ID, Severity, Status, Affected Files, Issue, Required Action), hazırlık satırları §12 sütunlarıyla; değerler W4F14.
- **Kimlik:** `AUDIT-FIX-58`'den sürer; öneri: reviewer geçici kimlik (`cov-a-01`) verir, kalıcısını bulgu dosyasına yazarken orkestratör verir.
- **Bulgu dosyası** (karar (4)): yol, biçim (oturum başına bölüm; sütunlar §13 ile aynı); her `O3` kapanış commit'ine girer.
- **`4 · O4` birleştirme:** Audit `Third-Planner.md:295` şablonuyla yeniden yazılır: H1 + 15 `##` başlık birebir ve sıralı, gövde ≥ 20 karakter; ilk `status:` eşleşmesi yeni durum; §12 kuyruk 47 satır; §13'te `AUDIT-FIX-01`–`-57`'nin yeni durumları ve yeniler; bulgu dosyasının akıbeti.
- **Geçitler:** `--mode all` çıkış 0; `step3 --strict` yalnız `strict_warning`; Step 4 önkoşulu `p0_findings=0`, `p1_findings=0`; P0/P1 denetim bulgusunun yolu yazılır.
- **Sahiplik:** Audit'i ve bulgu dosyasını yalnız orkestratör yazar; reviewer'lar salt-okur.

**(f) Kapanış** (plan §0 adım 4; beklenmedik durum yoksa sorulmadan):
- Plan §1'de `4 · O1+O2` `done` (commit başlığıyla); ilk `pending` `4 · O3a`.
- PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır, §11'e girdi (bağlam ölçümleri dahil); bu dosya `4 · O3a` için ≤ 20 KB yeniden yazılır.
- Bayt, boru ve kimlik taraması (§7); yerel commit `Window 4 O1-O2: plan and audit contract for the twelfth audit` (`git log --grep '^Window 4 O1-O2:'`); yalnız `O1` yürüdüyse `Window 4 O1: plan for the twelfth audit`. Kullanıcıya `git show --stat` özeti ve yeni pencere talimatı.

**Kabul:** açılış tuttu, dört depo kaydedildi; taban tuttu; birleşim kararı kayıtlı; §8.2 onaylı ("onay", sekiz karar tarihle); §8.3 (e)'nin yedi maddesiyle tam; §1, §3, PROJECT_LOG ve bu dosya güncel; kapanış commit'i yerel.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7, §7.2, §7.3, §8 ve ledger §8.

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
| Snapshot | Step 2 durmaz; etkin plan bugünkü `Main-Planing.md` | plan §7.3, ledger §3 |
| Atıf | Koşu 21'in seçimi | ledger §8 |
| Yayın | C3 push edildi (2026-11-16, ayrı onaylarla); sonraki FF ve push Pencere 4 planına göre | plan §1, PROJECT_LOG §11 |

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
11. Cihaza komut: Pencere 4 (12. denetim) hiç göndermez, `4 · O1+O2` dahil. Fiziksel eylemler kullanıcıda ve onaylı.
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
py -3 $V --root . --mode step3
py -3 $V --root . --mode step3 --strict
py -3 $V --root . --mode step4 --strict
py -3 scripts/build-release.py --self-test
```

| Kontrol | Taban (`4 · O0`, 2026-11-16T22:11Z; W4F02, W4F03) |
|---|---|
| `step2`, `step1`, `step3-preflight` `--strict` | Bulgu yok, çıkış 0 |
| V1 `--mode all` | Yalnız `warning=step4_has_nonblocking_warnings=P2:1,P3:9`; `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning`; çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| `--mode step3` (ölçüm, taban değil) | Çıkış 0, `audit_status=PASS_WITH_WARNINGS`, P0 0, P1 0, P2 1, P3 9; `--strict` çıkış 1 (`strict_warning`) |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=26` → PASS; `prose_mentions` artabilir |
| Boru ve bayt | Boru dışı yalnız plan `:177`, `:892` ve ledger `:473`, `:490`–`:495`, `:501`, `:506`, `:507`; ledger ve `Main-Planing.md` CRLF, öteki LF; NUL yalnız Ontology'de (2) |

- Kimlik taraması: `%TEMP%/idscan.py`, depo kökünde `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` politikası `cat`, `head`, `tail`, `grep` ve `find`'ı engeller: `awk`, `read`/`grep`/`glob` araçları ya da `py -3`; `<(…)` çalışmaz.
- **Denetim başlıkları:** 16 başlık (H1 + 15 `##`) birebir, tekil ve sıralı; 20 karakter sınırı her `##` gövdesine uygulanır (W4F10, W4F13).
- **Denetim durumu:** ilk `status:` eşleşmesi okunur; başlıkta eski durum alıntılanmaz. Değer ayıraçtan (`:`, `-`, `：`) hemen sonra gelir: `**Overall audit status: PASS_WITH_WARNINGS.**` eşleşir, `**Overall audit status:** …` eşleşmez.
- **`step3 --strict`:** `PASS_WITH_WARNINGS` ile çıkış her zaman 1; kabul "yalnız `strict_warning`" (W4F11, W4F13).
- **Kuyruk:** V kuyruğu alt planlar, Index ve ledger ile karşılaştırmaz; eski kuyruk da geçer, tutarlılık denetimin işidir (W4F11). Step 4 Pencere 4 bitmeden başlatılmaz.
- **SUPERSEDED 7'dir, 4 değil:** `Faz7.2`, `7.3`, `8.1`, `8.3` ile `Faz4.1`, `Faz4.7`, `Faz6.1`; `Faz4.6` ledger'da `implemented`, denetimde DEFERRED (W4F08); §8 `:750` eski.
- **Reviewer girdisi:** çalışma başına ≤ 400 KB, oturum başına ≤ 3. Scout ≈ 1M bağlamlıdır, `task` 100K: `task`'a plan ya da PROJECT_LOG bütün verilmez.
- **`local://` oturumlar arasında kaybolur** (§0 adım 8): sonuçlar ve taslaklar aynı oturumda depoya yazılır.
- **Alt ajanlar:** scout'un kabuğu yok, `local://`'a yazar. 429 ya da 402 ile duran ajan canlanmaz: görevi ortak bağlamla taze gönder (`4 · O0`'da üç scout).
- **Çapa numaraları** çoğu yerde eski ağaçlarındır (kayma haritası plan §10); içerikle doğrula. Ontology'de 2 NUL: `grep` boş dönebilir.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok, `DEC-30`).
- **`--grep` satır başına bağlanır** (`'^Window 4 O0:'`, `'^Window 4 O1-O2:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`d = await commit.draft()`, `await d.take(...)`, `await d.commit(...)`); `git add`/`git commit` yok. `cp` ile konan `NEXT_PROMPT.md` dahil değişen dosyaları açıkça `take` et (emsal `3 · O0` takip commit'i).
- **Emekli Faz 7/8:** dosyaları yerinde kalır (silmek `--strict`'te `extra_phase_folder_without_main_phase`).

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri, yayın doğrulaması (`git ls-remote origin`), snapshot ve dört depo (§4 a); plan §1'de ilk `pending` `4 · O1+O2`.
3. Bağlam (§4 b) ve taban (§4 c).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin, yayın durumu; birleşim sorusu (tahminle, §1); onaylanmazsa yalnız `O1`.
5. §4 (d) plan ve tek form, onay; (e) kontrat; (f) kapanış.

---
