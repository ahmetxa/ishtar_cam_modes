# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> 2026-11-15'te, Pencere 3 · O0'ın kapanış commit'inde yazıldı. Aşama: **Pencere 3 · O1 — plan ve onay**. Bu bir özettir; nihai kaynak `ORCHESTRATION_PLAN.md` (plan), `Planner-docs/Planing-Ledger.md` (kanonik kayıt) ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC (`org.codeaurora.snapcam`) yapılandırması; hepsi AOSPA Android 15'te kuruldu ve ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, kamera HAL'i farklı, proje modülleri kurulu değil. Planlama koşusu 21 Faz 7 ve 8'i emekli eder; kamera işi için yeni faz "ClaudeQB Phase 10" olur (plan §7).

1. **Tek aşama:** plan §1'deki ilk `pending` aşama satırı `3 · O1`'dir: plan ve onay. Bu oturum yalnız `O1`'i yürütür; `3 · O2a` ve sonrası sonraki oturumlardır. Aşama atlanmaz; oturum kendiliğinden sıradakine geçmez.
2. **Dosya kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** 2026-11-15'te yalnız git ve GitHub ölçüldü. Cihaz olguları 2026-11-13 ölçümüdür. Cihaza yalnız salt-okur komut; hangisinin ne zaman çalışacağı bu oturumun planıyla belirlenir (§6 madde 11).
4. **Onay kapıları** (plan §0 adım 5): `O1` plan onayı (bu oturumun sonu), `main`'in fast-forward'ı (FF) ve her push (`3 · O5`), cihaz eylemi, AGC tercihlerine yazma. Depoları kullanıcı siler. Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan yapılır.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; plan Ek A, `Planner-docs/` ve `docs/` İngilizce. Ajanlar: `scout`, `task`, `reviewer`, `security-reviewer`, `sonic` (`librarian`, `designer`, `isolated`, `outputSchema` yok).

## 1. Döngü ve bağlam bütçesi

- **Aşamalar** (plan §0): `O0` keşif, `O1` plan, `O2` kontrat, `O3` uygulama, `O4` entegrasyon ve geçitler, `O5` inceleme ve kapanış. Pencere 3'ün varsayılan düzeni plan §7 "Oturum düzeni ve bütçe" bloğundadır; `O1` onu kesinleştirir.
- **Eşik 400k** (plan §0 adım 9). Bağlamı Ek A.7'deki JS betiğiyle (`eval`) ölç: her alt ajan sonucundan sonra ve en geç her beş turda; 250k'dan sonra her turda. 300k'dan sonra yeni görev yok: elindeki işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, devam için bu dosya, commit). Kapanış 400k'dan önce biter. Bu beklenmedik durum değildir.
- **Tahmin:** açılış ≈ 35k (≈ 23k + 0,58k × ≈ 20 KB). Tur başına ≈ 6k yürütme; ≈ 10–14k plan ve uzun metin yazımı. Bu oturum (`3 · O1`) için plan §7 tahmini ≈ 185k (35k + 15 × 10k). Hedef 240k. Her aşamanın §1 satırında tahmin sütunu bulunur; 240k'yı aşan aşama bölünür (`O3a`, `O3b`).
- **Hijyen:** 20 KB'tan büyük okuma scout'a; scout ≤ 4 KB döner, ayrıntıyı `local://`'a yazar. Büyük dosya `grep` ve dar `:N-M` ile okunur; aynı aralık iki kez okunmaz. Taslak `cp` ile yerine konur, betikle doğrulanır, yeniden yazılmaz. Satırlar ≤ 600 bayt; `todo` ≤ 8 madde.
- **Beklenmedik durum** (plan §0 adım 6, liste orada): kapanış, commit ve bu dosyanın yeniden yazımı yok. Kullanıcıya sade dille: ne oldu, neden önemli, iki ya da üç seçenek ve önerin.

## 2. Okuma sırası

Boyutlar yaklaşıktır: plan ≈ 150 KB, `PROJECT_LOG.md` ≈ 175 KB, ledger ≈ 630 KB. Hiçbiri bütün okunmaz; bölüm başları `grep '^##'` ile bulunur.

1. Plan §0 (≈ 10 KB), §1 (≈ 11 KB), §2 (≈ 3 KB), §3 (≈ 7 KB).
2. Plan §7, başından "Oturum düzeni ve bütçe" bloğunun sonuna kadar: sekiz soru ve tarihli yanıtları, "Açılışta ayrıca". Sonra `### 7.1 Keşif envanteri` (≤ 15 KB, `W3OPN`).
3. Plan Ek A.7 (≈ 2,5 KB) ve PROJECT_LOG §2.6 (≈ 5 KB).
4. Plan §7'nin kalanı yalnız gerektiğinde, `grep` ve dar aralıklarla: "Aday alt planlar", Step 1, Ledger, Index, Ontology, Step 2, geçitler, doğrulayıcı tuzakları, ClaudeQB süreci.
5. Plan Ek A.5 betiği (≈ 3 KB): yalnız kapanışta ve push'tan önce.
6. Bütün okunmaz, gerekirse aranır: PROJECT_LOG §11 (≈ 45 KB), plan §6 (≈ 50 KB), §10, Ek A.2, A.6.
7. ClaudeQB dosyaları ve doğrulayıcı yalnız scout'lar okur; ana oturum okumaz.

## 3. Mevcut durum

**Beklenen durum (3 · O0 kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 78 commit. Uç: `Window 3 O0 follow-up: hand-off for stage 3 O1` (`git log --grep '^Window 3 O0 follow-up:'`); altında kapanış `Window 3 O0: discovery for planning run 21` (`git log --grep '^Window 3 O0:'`). Takip commit'i, kapanışa girmeyen bu dosyayı kullanıcı onayıyla ekledi. Etiket yok, 350 izlenen dosya.
- **`main` = `origin/main`** = `Window 2 follow-up: context budget and stage sizing` (76. commit). `origin/main..HEAD` = 2: `3 · O0` kapanışı ve takip commit'i push edilmedi. FF ve push `3 · O5`'te, ayrı onaylarla.
- **`git ls-remote origin`:** `HEAD`, `main`, `integrate/impl-96` = takip commit'i.
- Başka her durum beklenmedik (§4 a).
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez). Silinecek üç depo (`DEC-30`): `ahmetxa/ishtar` (özel), `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar` (açık). 2026-11-15T11:57:53Z–11:57:55Z'de üçü de 200; `ishtar_cam_modes` 200. Silmeyi kullanıcı yapar; ajan yalnız ölçer (404 = silinmiş). Aynalar `../ishtar-arsiv/`'de.
- **Ledger:** 653 satır, CRLF, NUL 0. Çapalar (Ek A.6 `LMAP`): `Faz6.2` `:98`, `Faz7.2` `:100`, `Faz7.3` `:101`, `Faz8.1` `:102`, `Faz8.3` `:104`, `DEC-27`…`DEC-32` `:605`–`:610`. `DEC-33` henüz yok; koşu 21 yazar.
- **Alt planlar:** 42; ledger §4'te 34 `verified`, 3 `implemented` (`Faz4.6`, `Faz6.1`, `Faz8.1`), 3 `planned` (`Faz7.2`, `Faz7.3`, `Faz8.3`), 2 `superseded` (`Faz4.1`, `Faz4.7`).
- **11. denetim** (2026-09-14, `PASS_WITH_WARNINGS`): kuyruk 2026-11-13'ten beri geçersiz (`DEC-28`).
- **Sıradaki numaralar:** koşu 21 (Pencere 3), 12. denetim (Pencere 4), `IMPL-97` (Pencere 5+), `DEC-33` (koşu 21).
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` hâlâ v1.9 içeriğinde (`DEC-29`).
- **Keşif (`3 · O0`, 2026-11-15):** plan §7.1 `W3OPN` ve envanter; sekiz yanıt plan §7'de tarihli. Bu dosya onları tekrarlamaz.

**Telefon** (2026-11-13 ölçümü; bu pencerede bağlanılmadı; ayrıntı Ek A.2 `D1`–`D11`, `M1`, `TRAP` ve PROJECT_LOG §2.3):
- HyperOS `OS4.0.0.44.WMACNXM`, Android 17; kernel 5.15.215, SELinux Enforcing; KernelSU `4.3.0-r1`.
- Kök yöneticisi: kullanıcı beyanı SukiSU; `com.rifsxd.ksunext` yok. Ölçülmedi (plan §7, soru 2).
- HAL md5 `2a955e68…` (AOSPA stoku `c3fa63a8…` değil); IMX989 sensör dosyası md5 `9e4d0fe1…` = `EXPECT_MD5`.
- Proje modülleri ve kutucuk uygulaması yok. AGC yamasız V9.6, `prefs.trap.armed = 10` (değer 37), `agc.pref_48m` yok.
- [ÇIKARIM] (M1): sensör koruması geçer, HAL koruması kapalı başarısız olur; `setmode.sh` AOSPA servis adlarını kullanır.

## 4. Bu oturum: `3 · O1`

Kaynak: plan §1 (`3 · O1` satırı), §0, §7 (yanıtlar, "Oturum düzeni ve bütçe", "Aday alt planlar", "Açılışta ayrıca") ve §7.1. Bu oturum yalnız plan yazar: `ORCHESTRATION_PLAN.md`; kapanışta PROJECT_LOG §2.6 ve §11; bu dosya. Ledger, `Planner-docs/`, `docs/`, `Main-Planing.md` ve Index yazılmaz; ana oturum bunları düzenlemez. Alt ajanlar salt-okurdur ya da yalnız `local://` yazar.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 3 O0 follow-up: …`; `git rev-list --count origin/main..HEAD` = 2; `main` ve `origin/main` = Pencere 2 takip commit'i; `git tag` boş; `git ls-files` = 350; `git ls-remote origin` (§3). Plan §1'de ilk `pending` = `3 · O1`. Tutmayan her şey beklenmedik durumdur.

**(b) GitHub ölçümü:** dört depo için `gh api -i repos/ahmetxa/<ad>` (üç silinecek depo ve `ishtar_cam_modes`), UTC zamanıyla; ilk satır HTTP durumudur. 404 varsa PROJECT_LOG'un silme cümleleri bu oturumda güncellenir (plan §7, "Açılışta ayrıca" yerleri; numaraları alıntıyla bul). Push cümleleri: O0 kapanış commit'i ve takip commit'i push edilmedi, FF ve push `3 · O5`'te.

**(c) Bağlam ölçümü:** Ek A.7 betiği (`eval`), oturum başında ve her alt ajan sonucundan sonra (§1).

**(d) Plan (asıl iş):**
1. **Oturum tablosu:** plan §7 "Oturum düzeni ve bütçe" varsayılanını al; her oturum için tahmin sütunu (§1 formülü). 240k'yı aşan aşama bölünür.
2. **Aday alt planlar** (plan §7, "Aday alt planlar" 1–6) yanıtlara göre: 1, 2, 4, 5 ve 6 kalır; 3 düşer (K9 = hayır, `DEC-33`). ClaudeQB Phase 10 için alt plan kimlikleri (`Faz10.N`, klasör `Faz-10-Plans`; 50MP planındaki Faz 10 ayrıdır) ve her birinin hangi oturumda, hangi kanıtla yazılacağı. Kimlikler `O1` planında kesinleşir.
3. **Dal kararı:** `integrate/impl-96` sürer mi, yeni dal mı? Öneri: sürsün (Pencere 2 kalıbı); FF yalnız `3 · O5`.
4. **Salt-okur SukiSU ve WebUI ölçümü:** zamanı bu oturumda belirlenir (plan §7, soru 2 ve yanıtı). Öneri: `3 · O1`'de, onaydan sonra ve kapanıştan önce; yalnız `platform-tools/adb.exe -s dc27e5d0`, salt-okur; kutucuk alt planının girdisi (plan §7.1 `W3F21`).
5. **Hetzner satırları** (soru 7): sahipleri `3 · O4` (orkestratör; `Project-Comprehension.md` `CQ-13` `:25`, `EV-20` `:51`; `docs/reverse-engineering-toolchain.md:220`; Ontology değişmez 11 `:429`); 12. denetim (Pencere 4, Step 3) doğrular, yani §10 yoluna gerek yok.
6. **§1 satırları:** `3 · O2a` (Step 1), `3 · O2b` (Step 2 kontratı), `3 · O3a`, `3 · O3b`, `3 · O4`, `3 · O5`; her biri önkoşul, kapsam, tahmin ve `pending`.
7. **Planı göster ve dur:** tablo (aşama, oturum, kapsam, tahmin, görev kimlikleri, kapı) ve dört soru (dal, ölçüm zamanı, alt plan kimlikleri, Hetzner düzeltmesinin aşaması). Kullanıcının **"onay"** yanıtını bekle; değişiklik isterse plana işle ve yeniden göster.

**(e) Kapanış** (onay alındıktan sonra; beklenmedik durum yoksa sorulmadan):
- Plan §1'de `3 · O1` `done`, commit'i başlığıyla anar; öneri `Window 3 O1: plan for planning run 21`. §1'e `O2a`–`O5` satırları eklenir.
- PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır; §11'e girdi eklenir.
- Bu dosya `3 · O2a` için ≤ 20 KB olarak yeniden yazılır.
- Değişen dosyalarda bayt ve boru kontrolü (LF, CR 0, NUL 0, tablo boruları) ve kimlik taraması (§7); yerel commit onay sorulmadan atılır; kullanıcıya `git show --stat` özeti ve yeni pencere çağrısı.
- Push yok; FF ve push `3 · O5`'te, onayla.

**Kabul:** plan §1'de `3 · O1` `done` (kapanıştan sonra); tahmin sütunu ve dört soru plan §7'de; aday alt planlar kesinleşmiş; onay alınmış; ledger, `Planner-docs/`, `docs/`, `Main-Planing.md` ve Index dokunulmamış.

## 5. Kullanıcı kararları

Kaynak: plan §2, plan başlığındaki onaylar ve ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| Depo taşıma | `origin` = özel `ahmetxa/ishtar_cam_modes` | `DEC-27` |
| K1 `Kullanim.txt` | (b): v2.3'te düzeltilir (soru 4) | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K3, K4 | Kernel iddiası düştü; temizlik uygulandı | IMPL-96 satırı |
| K5/K6 üç depo | Silinecek; kullanıcı siler; açılışta ölçülür | `DEC-30` |
| K7 HyperOS 4 yönü | (a) modülü uyarla; (i) yeni faz "ClaudeQB Phase 10", Faz 7 ve 8 tümüyle emekli (soru 5) | `DEC-32` |
| K8 cihaz kimlikleri | A, yürütüldü; redaksiyonsuz özgün yalnız `../ishtar-arsiv/` bundle'ında | `DEC-31` |
| K9 50MP HAL | Hayır, şimdilik; sensör katmanı sürer (soru 1) | `DEC-33` (koşu 21) |
| Sekiz soru | Yanıtlandı (2026-11-15); yanıtlar plan §7'de | plan §7 |
| Döngü | Aşama başına oturum; kapanış sorulmadan; FF ve push ayrı onay | plan Onay 2, §0 |
| Bağlam eşiği | 400k; hedef 240k | plan Onay 3, §0 adım 9 |
| Yayın | C2 ve takip commit'i push edildi; `3 · O0` kapanışı yerel, `3 · O5`'te push | plan §1, §0 adım 5 |
| Pencere 3 planı | `3 · O1`'de "onay" bekleniyor | plan §1, §7 |

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
11. Cihaza komut: yalnız salt-okur ve yalnız `3 · O1` planında geçen komutlar. Fiziksel eylemler (kurulum, mod değiştirme, deklanşör, izin diyaloğu) kullanıcıda ve onaylı.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`, `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla (hash'ler değişir).
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik değeri yazma ya da geri kazanma; tarama yalnız sayı ve konum basar.
20. Sıcak noktayı alt ajana yazdırma: ledger (yalnız orkestratör), `Main-Planing.md`, Index, Audit, Ontology, `CHANGELOG.md`, sürüm yerleri, manifest, `.gitignore`, `.gitattributes`, `snapshots/`, plan ve git (plan §3).
21. Satır sonu dönüştürme: ledger, `Main-Planing.md`, `Autopsy.md` CRLF, gerisi LF; CRLF dosyada ilk `edit`'ten sonra baytla doğrula.
22. `python` ya da `python3`: yalnız `py -3`.

## 7. Doğrulama komutları ve taban değerler

```bash
py -3 C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py --root . --mode all
py -3 C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py --root . --mode step4 --strict
py -3 scripts/build-release.py --self-test
```

| Kontrol | Taban (2026-11-14 ve 2026-11-15) |
|---|---|
| V1 `--mode all` | `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`; çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9`; çıkış 1 (taban, regresyon değil) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0` → PASS; `prose_mentions` değişebilir (artış hata değil) |

- Geçitler (plan §3) `3 · O4`'te, fazın belirttiği aşamada çalışır; `3 · O1` bunları çalıştırmaz. Bu oturumda yalnız kimlik taraması kapanışta çalışır.
- Kimlik taraması: Ek A.5 betiğini `write` ile `%TEMP%` altına yaz, depo kökünde `py -3 <yol>` ile çalıştır; değer basmaz.
- Koşu 21 kipleri (plan §7): `step1` Step 1'den sonra; `step2` ve `step3-preflight` Step 2'den sonra; hepsi `--strict`. Step 1.5 (Autopsy) atlanır, `autopsy` kipi çalışmaz.
- Bayraksız `build-release.py` `dist/` zip'ini ve manifest'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- `python` Store stub'ıdır; `SKILL.md`'deki `python3` burada çalışmaz.
- **omp:** `eval` yalnız JS (Ek A.7 betiği JS). `bash` komut içindeki `grep`, `tail`, `cat`'i ve heredoc ile dosya yazmayı engelleyebilir: `grep`/`read` araçlarını ya da `%TEMP%`'teki `py -3` betiğini kullan; `<(…)` çalışmaz.
- **Alt ajanlar:** scout'ların kabuğu yok; `task` ajanları 100K bağlamlı: plan ya da PROJECT_LOG bütün verilmez.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok); `gh api -i`'nin ilk satırı HTTP durumudur.
- **Depo silme (kullanıcı, `DEC-30`):** GitHub'da Settings → General → Danger Zone → Delete this repository; ya da kullanıcı kendi terminalinde `gh auth refresh -h github.com -s delete_repo` ve `gh repo delete ahmetxa/<ad> --yes`. Ajan silmez, yalnız ölçer.
- **`--grep` satır başına bağlanır** (`'^Window 3:'`); `^` gövde satırlarını da eşler: commit gövdesinde başka bir aşamanın başlığıyla başlayan satır olmaz.
- **`local://` taşınmaz:** yanıtlar, `W3OPN`, envanter ve `O1` planı kapanıştan önce plana yazılır.
- **Satır numaraları kayar:** plan §7'deki PROJECT_LOG numaraları `2 · O3` kapanışına göredir; ledger'da `LSH` ve `LMAP`; `Planner-docs/` numaraları içerikle doğrulanır.
- **Tablolar:** hücrede `|` yok; ledger §4 satırı 10, §8 satırı 7 boru.
- **Ledger** satırları 1–9 KB: yalnız `:raw:N-M`.
- **Ontology**'de 2 NUL: `grep` sessizce boş dönebilir (`AUDIT-FIX-22`); dosya bayt korumalı.
- **"Faz 10":** `50MP-Entegrasyon-Plani.md`'deki ayrı numaralama; yeni faz "ClaudeQB Phase 10", klasör `Faz-10-Plans`.
- **Emekli Faz 7/8:** satırlar ve bölümler yerinde, tarihli notla kalır; satır silmek `extra_phase_folder_without_main_phase` uyarısını (`--strict`'te hata) doğurur.
- **`.gitignore`'da `*.so` kuralı yok:** K9 = evet olsaydı HAL kopyalanmadan önce kural önerilirdi; K9 = hayır.
- Doğrulayıcı tuzakları: plan §7 "Doğrulayıcı tuzakları"; kapsam dışı bulgular plan §10.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri (§4 a): ağaç temiz; dal `integrate/impl-96`; uç commit'in başlığı `Window 3 O0 follow-up: …`; plan §1'de ilk `pending` aşama `3 · O1`; §3'teki beklenen durum. Tutmayan her şey beklenmedik durumdur.
3. GitHub ölçümü (§4 b) ve bağlam ölçümü (§4 c).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin (cihaz olguları 2026-11-13), bu oturumun yalnız `3 · O1` olduğu.
5. Plan (§4 d) tablosunu yaz, göster, dur; kullanıcının "onay" yanıtını bekle. Onaydan sonra §4 (e).

---
