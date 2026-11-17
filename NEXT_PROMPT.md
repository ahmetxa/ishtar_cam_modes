# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> Pencere 4 · O1'in kapanış commit'inde yazıldı. Aşama: **Pencere 4 · O2 — 12. denetimin denetim kontratı (plan §8.2, §8.3)**. Özettir; nihai kaynak plan, ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`) için root tabanlı kamera özelleştirmesidir (`ishtar-cam-modes` v2.2, `ishtar-aon-fix` v1.1, AGC yapılandırması; AOSPA Android 15'te ölçüldü). ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, proje modülleri kurulu değil.
Pencere 4 12. denetimdir (ClaudeQB Step 3): 47 alt plan denetlenir, yalnız `Planner-docs/Sub-Planing-Audit.md` yazılır. `4 · O0` (keşif, §8.1) ve `4 · O1` (plan, §8.2) bitti.

1. **Tek aşama:** plan §1'de `4 · O1` `done` (`:71`), ilk `pending` `4 · O2` (`:72`; görev `CT4`). Bu oturum yalnız onu yürütür; birleşim sorusu yok. `4 · O3a`'ya asla başlanmaz.
2. **Plan kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** Pencere 4 cihaza komut göndermez; olgular plan §7.1 `W3P01`–`W3P04`.
4. **Onay kapıları** (plan §0 adım 5; kısa evet/hayır): FF; her push ayrı; cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler. Kontrat onay kapısı değildir: §8.3 sorulmadan yazılır. Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan (§0 adım 4).
5. **Beklenmedik durum** (plan §0 adım 6): kapsamı ya da §8.2'nin bir kararını değiştiren her seçim dahil. Kapanış, commit ve bu dosyanın yeniden yazımı yok; kullanıcıya sade dille iki ya da üç seçenek ve önerin.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; Ek A, `Planner-docs/`, `docs/` ve bulgu dosyası İngilizce (Ek A.3).

## 1. Döngü ve bağlam bütçesi

- **Eşik 400k** (plan §0 adım 9): Ek A.7 betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok; kapanış 400k'dan önce biter. Hijyen: §0 adım 8–9.
- **Tahmin** (plan §8.2): `4 · O2` ≈ 220k = 100k açılış + 10 × 12k yazım turu.
- **Ders (`4 · O1`):** açılış okuma ve tabanla 108k'ya çıktı; form gönderilirken bağlam 200.951 token olduğu için (koşul 200k) `O2` ayrıldı. Her onay formundan önce bağlamı ölç. `edit` değişen bloğu geri getirir (KB başına ≈ 0,55k token): §8.3'ü az edit'le yaz, yeniden okuma.

## 2. Okuma sırası

Büyük dosyalar bütün okunmaz (`grep '^##'`). Numaralar `4 · O1` kapanışınındır; içerikle doğrula.

1. Plan §0 (`:9`–`:44`), §1 (`:46`–`:80`), §3 (`:99`–`:125`; geçitler, Gizlilik, Git, Adlandırma).
2. Plan §8 (`:753`–`:760`); §8.1 (`:762`–`:796`) yalnız atıf yapılan satırlar; §8.2 (`:797`–`:856`; onaylı plan, sekiz karar, `W4O1P01`, `W4O1P02`).
3. Emsal: §7.3 (`:674`–`:752`; kontrat tabloları, ortak bağlam).
4. Ek A.5 (`:1016`; push, kimlik taraması betiği), A.7 (`:1089`).
5. Skill (§7'deki `$V` yolunun `skills/claudeqb/` dizini): `references/handoffs/run-step3.md` (roller `:17`, durma `:15`); `references/Third-Planner.md` `:295`'ten (şablon; §15 `:545`); `references/subagent-playbook.md:19-25`.
6. `$V` satırları: yalnız W4F10–W4F14'te anılan aralıklar.
7. PROJECT_LOG §2.6 (`:228`), §5.5 (`:712`), §11'in son girdisi (`4 · O1`, sonda).

## 3. Mevcut durum

**Beklenen durum (4 · O1 kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 89 commit. Uç ve kapanış: `Window 4 O1: plan for the twelfth audit` (`git log --grep '^Window 4 O1:'` tek commit = uç). Etiket yok, 355 izlenen dosya.
- **Yayın:** `main` = `origin/main` = `081790f` (C3); `origin/main..HEAD` = 2; `git ls-remote origin`: `HEAD`, `main`, `integrate/impl-96` = `081790f`. FF ve push yalnız `4 · O5`'te, `C4`'ten sonra, ayrı onaylarla (plan §8.2).
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez); silinecek üç depo (`DEC-30`): `ishtar`, `android_local_manifests`, `android_device_xiaomi_ishtar` (hepsi `ahmetxa/`). 2026-11-17T09:52:59Z–09:53:02Z: dördü 200.
- **`Main-Planing.md`** (değişmedi): sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 406 satır, 77.019 bayt, CRLF, NUL 0, 10 faz. Alt plan 47 (1.141.813 B).
- **Öteki dosyalar** (değişmedi): ledger 662 satır, CRLF, NUL 0; Index 443, Ontology 453 (NUL 2: `:313`, `:316`), Comprehension 176, toolchain 246, LF. Audit 437 satır, 57.836 B, LF; durum `:18`, son kimlik `AUDIT-FIX-57`.
- **Plan:** 1109 satır, LF; §1 `4 · O1` `done` (`:71`), `4 · O2` `pending` (`:72`); §8.2 `:797`–`:856`, §9 `:857`, §10 `:866`, Ek A.5 `:1016`, A.7 `:1089`. Boru dışı satırlar yalnız `:183`, `:958`.
- **Kapasite (`W4O1P01`):** `reviewer` 369.082 B'yi baştan sona okudu, pencere 1M gözlendi. `security-reviewer` 307.696 B'yi sınıra takılmadan okudu ama `partial` döndü (`:raw` yeniden okumalarını atladı, satır sayılarını tahmin etti); penceresi gözlenmedi. Model `anthropic/claude-opus-5-5`.
- **Geçitler ve sürüm:** taban değişmedi; kimlik taraması `prose_mentions=26` (artabilir); v2.2 / versionCode 13 (`DEC-29`).

## 4. Bu oturum: `4 · O2`

Audit, alt planlar ve bulgu dosyası yazılmaz, reviewer çalışmaz. Yazılanlar: plan §8.3 (önerilirse Ek A.8), §1, gerekirse §3 Adlandırma; PROJECT_LOG §2.6 ve §11; bu dosya; sonra git.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 4 O1: plan for the twelfth audit`; `git log --grep '^Window 4 O1:'` tek commit = uç; `git rev-list --count HEAD` = 89; `git tag` boş; `git ls-files` = 355; plan §1'de ilk `pending` = `4 · O2`.
Yayın: `git rev-parse main origin/main` = `081790f`; `git rev-list --count origin/main..HEAD` = 2; `git ls-remote origin` üç ref = `081790f`. Snapshot ve dosyalar §3'teki gibi.
GitHub: dört depo `gh api -i repos/ahmetxa/<ad>` (UTC). `ishtar_cam_modes` 200 değilse beklenmedik durum; üç depodan biri 404 ise kaydedilir (PROJECT_LOG §2.6, §11). Ölçüm §8.3'ün ilk satırı (öneri `W4O2OPN`). Tutmayan her şey beklenmedik durumdur.

**(b) Bağlam:** Ek A.7 betiği başta, tabandan sonra ve her edit dizisinden sonra.

**(c) Taban** (bir kez, §7): `step2`, `step1`, `step3-preflight` `--strict`, V1–V3, kimlik taraması, `--mode step3` (bayraksız ve `--strict`); sapma beklenmedik durumdur.

**(d) `CT4` — denetim kontratı** (yeni plan §8.3, §8.2'den sonra, `## 9.`'dan önce; emsal §7.3). Her madde ilgili §8.2 kararına bağlanır; `CT4` kabulü plan §1 `:72`'dir:
1. **Reviewer girdisi** (karar 3, 7, 8):
   - Ortak İngilizce görev metni: rol (§2 madde 5), şablon `Third-Planner.md:295`, izinli değerler `W4F14`, salt-okur, kimlik değeri basılmaz. Yeri: öneri yeni İngilizce Ek A.8; §8.3 ona atıf yapar.
   - Zorunlu okuma yordamı (`W4O1P01`): her dosyada 760 karakteri aşan satırlar `awk` ile taranır; o satırlar ve atlanan bloklar `:raw` ile yeniden okunur; satır sayıları `wc -l` ile alınır, tahmin edilmez.
   - Altı çalışma (seçenek C): `cov-a`, `rdy-a`, `sec-a` (`4 · O3a`); `cov-b`, `cov-c`, `cov-d` (`4 · O3b`). Her biri için dosya listesi ve ölçülmüş bayt, ≤ 400 KB.
   - Ön değerler (KB, `W4F06`): `cov-a` 334,5; `rdy-a` 386,4; `sec-a` 296,8; `cov-b` 360,2; `cov-c` 322,9; `cov-d` 341,6 (hafif okumayla). Ledger yalnız dilimin §4 satırları (`W4O1P02`: `:69`–`:115`, 76.612 B; F10 5.184, F3 19.796, F1/F2/F5/F6 12.381, F4/F7/F8/F9 39.251 B).
   - `cov-d`: alt planları tek başına 441.673 B, 400 KB kuralını aşar. `4 · O2` sekiz emekli ya da ertelenmiş dosyanın hafif okumasını (bölümler ve bayt) tanımlar ya da çalışmayı böler; bölme `4 · O3b`'yi dört reviewer'a çıkarırsa yarı sonraki oturuma kalır (oturum başına ≤ 3).
   - Karar 7: REV-3 P3'leri (ledger `:615`–`:618`) ilgili coverage çalışmasına atanır. Karar 8: `[ÇIKARIM]` satırları (`W4F07`, `W4F15`, `W4F17`, `W4F20`) dilimin reviewer'ına; `W4F26` tahmindir. S3 maddeleri (`W4F15`–`W4F24`) ve eski `AUDIT-FIX`'ler çalışmalara dağıtılır.
   - Plan ve PROJECT_LOG hiçbir reviewer'a bütün verilmez; gereken satırlar aralıkla.
2. **Çıktı biçimi:** dönüş ≤ 4 KB (§3 bloğu); ayrıntı `local://`, aynı oturumda `FND-a`/`FND-b` ile tüketilir (§0 adım 8). Bulgular §13 sütunları artı geçici kimlik; hazırlık satırları §12 sütunları; değerler `W4F14`; her bulgu alıntılı `yol:satır`.
3. **Kimlik:** `AUDIT-FIX-58`'den sürer. Reviewer geçici `<çalışma>-NN` verir (ör. `cov-a-01`); kalıcısını orkestratör `FND-a`, `FND-b`'de verir; eşleme tam.
4. **Bulgu dosyası** (karar 4): `AUDIT12_FINDINGS.md`, kök, İngilizce, LF; oturum başına bir bölüm; sütunlar §13 artı geçici kimlik; her `O3` kapanış commit'ine girer; `4 · O4`'ten sonra birleştirme notuyla kanıt olarak kalır. `.gitattributes`: `* -text` (bayt korur), `*.md` için `eol=lf` yok; LF baytla doğrulanır.
5. **`4 · O4` birleştirmesi** (karar 2, 5, 6): Audit şablondan yeniden yazılır: H1 + 15 `##` başlık birebir ve sıralı, her gövde ≥ 20 karakter; ilk `status:` eşleşmesi yeni durum. §12 kuyruk 47 satır, Index sırasıyla; 7 SUPERSEDED, `Faz4.6` DEFERRED. §13: `AUDIT-FIX-01`–`-57`'nin yeni durumları (karar 6 dahil) ve yeniler. Bulgu dosyasının akıbeti; `AUD-D1`–`AUD-D3` taslak sınırları.
6. **Geçitler** (karar 1): `--mode all` çıkış 0; `step3 --strict` yalnız `strict_warning=step4_has_nonblocking_warnings`; Step 4 önkoşulu `p0_findings=0`, `p1_findings=0`. P0/P1 denetim bulgusunun yolu yazılır (§0 adım 6).
7. **Sahiplik:** Audit'i ve bulgu dosyasını yalnız orkestratör yazar; reviewer'lar salt-okur, doğrulayıcı çalıştırmaz.
8. **`PAT4` desen listesi:** Faz 1–9 için hazırlık ve güvenlik desenleri; yalnız sayı ve konum basılır, değer basılmaz; her isabet bulguya ya da gerekçeli `not_applicable`'a döner.

**(e) Kapanış** (plan §0 adım 4; beklenmedik durum yoksa sorulmadan):
- Plan §1'de `4 · O2` `done` (commit başlığıyla); ilk `pending` `4 · O3a`. §8.3 eklenince §9, §10, Ek A ve boru dışı `:958` kayar: yeniden ölçülür.
- PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır, §11'e girdi (bağlam ölçümleri dahil); bu dosya `4 · O3a` için ≤ 20 KB yeniden yazılır.
- Bayt, boru ve kimlik taraması (§7); yerel commit `Window 4 O2: audit contract for the twelfth audit` (`git log --grep '^Window 4 O2:'`). Kullanıcıya `git show --stat` özeti ve yeni pencere talimatı.

**Kabul:** açılış ve taban tuttu, dört depo kaydedildi; §8.3 (d)'nin sekiz maddesiyle tam, altı çalışma ölçülmüş ve ≤ 400 KB, §8.2 ile çelişki yok; §1, PROJECT_LOG ve bu dosya güncel; kapanış commit'i yerel.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7–§8.2, ledger §8.

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
11. Cihaz komutu: Pencere 4 (12. denetim) hiç göndermez, `4 · O2` dahil. Fiziksel eylemler kullanıcıda ve onaylı.
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

| Kontrol | Taban (`4 · O0`, 2026-11-16T22:11Z; W4F02, W4F03; `4 · O1`'de tuttu) |
|---|---|
| `step2`, `step1`, `step3-preflight` `--strict` | Bulgu yok, çıkış 0 |
| V1 `--mode all` | Yalnız `warning=step4_has_nonblocking_warnings=P2:1,P3:9`; `subplan_count=47`, `index_reference_count=47`, `phase_folder_count=10`; çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning`; çıkış 1 (taban) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| `--mode step3` (ölçüm, taban değil) | Çıkış 0, `audit_status=PASS_WITH_WARNINGS`, P0 0, P1 0, P2 1, P3 9; `--strict` çıkış 1 (`strict_warning`) |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=26` → PASS; `prose_mentions` artabilir |
| Boru ve bayt | Boru dışı yalnız plan `:183`, `:958` ve ledger `:473`, `:490`–`:495`, `:501`, `:506`, `:507`; ledger ve `Main-Planing.md` CRLF, öteki LF; NUL yalnız Ontology'de (2) |

- Kimlik taraması `%TEMP%/idscan.py` ile (yoksa Ek A.5'ten yazılır), kökte `py -3`; değer basmaz. Bayraksız `build-release.py` `dist/`'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` politikası `cat`, `head`, `tail`, `grep` ve `find`'ı engeller: `awk`, `read`/`grep`/`glob` araçları ya da `py -3`; `<(…)` çalışmaz.
- **Denetim başlıkları ve durumu:** H1 + 15 `##` birebir, tekil, sıralı; 20 karakter her `##` gövdesine (W4F10). İlk `status:` eşleşmesi okunur, değer ayıraçtan (`:`, `-`, `：`) hemen sonra gelir: `status: PASS_WITH_WARNINGS` eşleşir, `status:** …` eşleşmez.
- **`step3 --strict`:** `PASS_WITH_WARNINGS` ile çıkış her zaman 1; kabul "yalnız `strict_warning`" (karar 1).
- **Kuyruk:** V kuyruğu alt plan, Index ve ledger ile karşılaştırmaz; tutarlılık denetimin işidir (W4F11).
- **SUPERSEDED 7'dir:** `Faz7.2`, `7.3`, `8.1`, `8.3`, `Faz4.1`, `Faz4.7`, `Faz6.1`; `Faz4.6` ledger'da `implemented`, denetimde DEFERRED (karar 2).
- **Reviewer girdisi:** çalışma başına ≤ 400 KB, oturum başına ≤ 3 reviewer. `W4O1P01` yalnız `reviewer`'ın 1M penceresini gözledi; `security-reviewer`'ınki gözlenmedi. `task`'ın 100K sınırı geçerlidir (taşma kayıtları PROJECT_LOG `:1084`, `:1123`): `task`'a plan ya da PROJECT_LOG bütün verilmez.
- **Okuma aracı:** 768 karakterden uzun satırları keser, büyük dosyada blok atlar; §4 (d) 1'deki yordam bunun içindir, atlayan reviewer `partial` döner.
- **`edit` yankısı:** değişen blok yanıtta geri gelir (KB başına ≈ 0,55k token); uzun bölüm az edit'le yazılır, yeniden okunmaz.
- **`local://` oturumlar arasında kaybolur** (§0 adım 8): sonuçlar aynı oturumda depoya yazılır.
- **Alt ajanlar:** scout'un kabuğu yok, `local://`'a yazar. 429 ya da 402 ile duran ajan canlanmaz: taze gönder.
- **Çapa numaraları** çoğu yerde eski ağaçlarındır (kayma haritası plan §10); içerikle doğrula. Ontology'de 2 NUL: `grep` boş dönebilir.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok, `DEC-30`).
- **`--grep` satır başına bağlanır** (`'^Window 4 O2:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`draft`, `take`, `commit`); `git add`/`git commit` yok. `cp` ile konan `NEXT_PROMPT.md` dahil değişen dosyaları açıkça `take` et.
- **Emekli Faz 7/8:** dosyaları yerinde kalır (silmek `--strict`'te `extra_phase_folder_without_main_phase`).

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri, yayın doğrulaması, snapshot ve dört depo (§4 a); plan §1'de ilk `pending` `4 · O2`.
3. Bağlam (§4 b) ve taban (§4 c).
4. Kısa Türkçe "hazırım" özeti (ölçülenler, yayın durumu); soru yok, devam.
5. §4 (d) `CT4`: §8.3'ü az edit'le yaz; (e) kapanış.

---
