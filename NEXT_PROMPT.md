# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> 2026-11-15'te, Pencere 3 · O1'in kapanış commit'inde yazıldı. Aşama: **Pencere 3 · O2a — Step 1 (`Main-Planing.md`)**. Bu bir özettir; nihai kaynak plan (`ORCHESTRATION_PLAN.md`, Pencere 3 için §7.2), ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC (`org.codeaurora.snapcam`) yapılandırması; hepsi AOSPA Android 15'te ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, kamera HAL'i farklı, proje modülleri kurulu değil. Koşu 21 Faz 7 ve 8'i emekli eder; kamera işi "ClaudeQB Phase 10"a (`Faz10.1`–`Faz10.5`, plan §7.2) geçer.

1. **Tek aşama:** plan §1'deki ilk `pending` aşama satırı `3 · O2a`'dır: Step 1, yalnız `Planner-docs/Main-Planing.md`. Bu oturum yalnız `O2a`'yı yürütür; `3 · O2b` ve sonrası sonraki oturumlardır. Aşama atlanmaz; oturum kendiliğinden sıradakine geçmez.
2. **Dosya kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** olgular 2026-11-13 ölçümü ve 2026-11-15 `PRB` ölçümüdür (plan §7.1 `W3P01`–`W3P04`). Bu aşama cihaza komut göndermez.
4. **Onay kapıları** (plan §0 adım 5): Step 1 metni (`ST1-A`, bu oturum); `main`'in fast-forward'ı (FF) ve her push (`3 · O5`); cihaz eylemi; AGC tercihlerine yazma. Depoları kullanıcı siler. Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan yapılır.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; plan Ek A, `Planner-docs/` ve `docs/` İngilizce. Ajanlar: `scout`, `task`, `reviewer`, `security-reviewer`, `sonic` (`librarian`, `designer`, `isolated`, `outputSchema` yok).

## 1. Döngü ve bağlam bütçesi

- **Aşamalar** (plan §0): `O0` keşif, `O1` plan, `O2` kontrat, `O3` uygulama, `O4` entegrasyon ve geçitler, `O5` inceleme ve kapanış. Pencere 3'ün düzeni plan §7.2 "Oturumlar" tablosundadır.
- **Eşik 400k** (plan §0 adım 9). Bağlamı Ek A.7'deki JS betiğiyle (`eval`) ölç: her alt ajan sonucundan sonra ve en geç her beş turda; 250k'dan sonra her turda. 300k'dan sonra yeni görev yok: elindeki işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, devam için bu dosya, commit). Kapanış 400k'dan önce biter. Bu beklenmedik durum değildir.
- **Tahmin:** bu oturum (`3 · O2a`) ≈ 225k (35k + 10k okuma + 15 × 12k). Kalibrasyon: `3 · O1` plan sunumunda ≈ 24 turda 206k'daydı, onayda 235k, kapanışta ≈ 340k; farkı zorunlu okuma ve uzun düşünme yaptı. Orkestratör uzun metni okumaz ve yazmaz: taslak `local://`'da, uygulama `py -3` betiğiyle.
- **Hijyen:** 20 KB'tan büyük okuma scout'a; scout ≤ 4 KB döner, ayrıntıyı `local://`'a yazar. Büyük dosya `grep` ve dar `:N-M` ile okunur; aynı aralık iki kez okunmaz. Taslak `cp` ile yerine konur, betikle doğrulanır, yeniden yazılmaz. Satırlar ≤ 600 bayt; `todo` ≤ 8 madde.
- **Beklenmedik durum** (plan §0 adım 6, liste orada): kapanış, commit ve bu dosyanın yeniden yazımı yok. Kullanıcıya sade dille: ne oldu, neden önemli, iki ya da üç seçenek ve önerin.

## 2. Okuma sırası

Boyutlar yaklaşıktır: plan ≈ 187 KB, `PROJECT_LOG.md` ≈ 180 KB, ledger ≈ 630 KB. Hiçbiri bütün okunmaz; bölüm başları `grep '^##'` ile bulunur.

1. Plan §0, §1 ve §3 (§2 gerekirse).
2. Plan §7.2 bütünüyle (≈ 20 KB): dört soru ve yanıtları, alt planlar, oturumlar, görevler, Step 1 listesi, `W3F28` kararları, ara durumlar ve geçitler, sıcak noktalar.
3. Plan §7'de dar aralıkla: "Step 1 — `Main-Planing.md`", "Doğrulayıcı tuzakları", "ClaudeQB süreci". §7.1'den `W3F01`–`W3F14` ve `W3F28`–`W3F30` (`grep '^| W3F'`).
4. Plan Ek A.7 ve PROJECT_LOG §2.6.
5. Plan Ek A.5 betiği: yalnız kapanışta.
6. ClaudeQB dosyaları (`First-Planner.md` ve öteki skill dosyaları), doğrulayıcı ve `Main-Planing.md`'nin tamamı yalnız scout'larla okunur (`ST1-R`).

## 3. Mevcut durum

**Beklenen durum (3 · O1 kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 79 commit. Uç: `Window 3 O1: plan for planning run 21` (`git log --grep '^Window 3 O1:'`); altında `Window 3 O0 follow-up: hand-off for stage 3 O1` ve `Window 3 O0: discovery for planning run 21`. Etiket yok, 350 izlenen dosya.
- **`main` = `origin/main`** = `Window 2 follow-up: context budget and stage sizing` (76. commit). `origin/main..HEAD` = 3 (`3 · O0` kapanışı, takip commit'i, `3 · O1` kapanışı); hiçbiri push edilmedi. FF ve push `3 · O5`'te, ayrı onaylarla.
- **`git ls-remote origin`:** `HEAD`, `main`, `integrate/impl-96` = Window 2 takip commit'i.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez). Silinecek üç depo (`DEC-30`): `ahmetxa/ishtar` (özel), `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar` (açık). 2026-11-15T12:36:42Z–12:36:44Z'de üçü de 200; `ishtar_cam_modes` 200. Silmeyi kullanıcı yapar; ajan yalnız ölçer (404 = silinmiş). Aynalar `../ishtar-arsiv/`'de.
- **Ledger:** `3 · O1` dokunmadı: 653 satır, CRLF, NUL 0. Çapalar (Ek A.6 `LMAP`): `Faz6.2` `:98`, `Faz7.2` `:100`, `Faz7.3` `:101`, `Faz8.1` `:102`, `Faz8.3` `:104`, `DEC-27`…`DEC-32` `:605`–`:610`. `DEC-33` henüz yok; koşu 21 `3 · O4`'te yazar.
- **Alt planlar:** 42; ledger §4'te 34 `verified`, 3 `implemented` (`Faz4.6`, `Faz6.1`, `Faz8.1`), 3 `planned` (`Faz7.2`, `Faz7.3`, `Faz8.3`), 2 `superseded` (`Faz4.1`, `Faz4.7`).
- **11. denetim** (2026-09-14, `PASS_WITH_WARNINGS`): kuyruk 2026-11-13'ten beri geçersiz (`DEC-28`).
- **Sıradaki numaralar:** koşu 21 (Pencere 3), 12. denetim (Pencere 4), `IMPL-97` (Pencere 5+), `DEC-33` (koşu 21).
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` hâlâ v1.9 içeriğinde (`DEC-29`).

**Telefon** (2026-11-13 ölçümü ve 2026-11-15 `PRB`; ayrıntı Ek A.2 `D1`–`D11`, `M1`, `TRAP`, plan §7.1 `W3P01`–`W3P04` ve PROJECT_LOG §2.3):
- HyperOS `OS4.0.0.44.WMACNXM`, Android 17; kernel 5.15.215, SELinux Enforcing.
- Kök: SukiSU-Ultra v4.3.0-r1 (`com.sukisu.ultra`, versionCode 41140; `PRB` doğruladı); adb kabuğunda `su` diyalogsuz çalışır; metamodül yok; `com.rifsxd.ksunext` yok.
- HAL md5 `2a955e68…` (AOSPA stoku `c3fa63a8…` değil); IMX989 sensör dosyası md5 `9e4d0fe1…` = `EXPECT_MD5`; ikisi de `vendor_file` etiketli.
- Proje modülleri ve kutucuk uygulaması yok. AGC yamasız V9.6, `prefs.trap.armed = 10` (değer 37), `agc.pref_48m` yok; tercih dosyasının sahibi ve etiketi AOSPA sabitlerini tutmaz (`W3P04`).
- [ÇIKARIM] (`M1`, `W3P03`): sensör koruması geçer, HAL koruması kapalı başarısız olur; `setmode.sh` AOSPA servis adlarını kullanır ve HyperOS'ta çalışmayan `vendor.camera-provider-2-7-ext`'i başlatır.

## 4. Bu oturum: `3 · O2a`

Kaynak: plan §1 (`3 · O2a` satırı), §0, §7.2 (Step 1 listesi, görevler `ST1-R` → `ST1-D` → `ST1-A` → `ST1-W`, ara durumlar) ve §7 "Step 1 — `Main-Planing.md`". Bu oturum yalnız `Planner-docs/Main-Planing.md`'yi yazar (Step 1); kapanışta plan §1, PROJECT_LOG §2.6 ve §11 ve bu dosya. Ledger, Index, Audit, Ontology, Comprehension, `docs/` ve alt plan dosyaları yazılmaz; Step 1 ledger'a yazmaz.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 3 O1: plan for planning run 21`; `git rev-list --count origin/main..HEAD` = 3; `main` ve `origin/main` = Pencere 2 takip commit'i; `git tag` boş; `git ls-files` = 350; `git ls-remote origin` (§3). Plan §1'de ilk `pending` = `3 · O2a`. Tutmayan her şey beklenmedik durumdur.

**(b) GitHub ölçümü:** dört depo için `gh api -i repos/ahmetxa/<ad>`, UTC zamanıyla; ilk satır HTTP durumudur. 404 varsa PROJECT_LOG'un silme cümleleri bu oturumda güncellenir (yerler plan §7 "Açılışta ayrıca"; numaraları alıntıyla bul).

**(c) Bağlam ölçümü:** Ek A.7 betiği (`eval`), oturum başında ve her alt ajan sonucundan sonra (§1).

**(d) Step 1:**
1. **Taban:** düzenlemeden önce `--mode step1 --strict` (öngörü: bulgu yok, çıkış 0; `W3F30`) ve `--mode all` (V1).
2. **`ST1-R`:** iki scout: `Main-Planing.md`'nin tam okuması ve Step 1 listesinin yerleri (içerikle doğrulanmış çapalar); First-Planner'ın Step 1 kuralları (`W3F01`, `W3F02`).
3. **`ST1-D`:** geniş bağlamlı scout, plan §7.2'deki beş maddelik Step 1 listesinin satır satır taslağını `local://`'a yazar: Faz 7/8 emekliliği, `| 10 |` satırı ve `### Phase 10` bölümü; §4 hedefi, `W3F11` satırları, Faz 6 ve Faz 9 yerleri; `AUDIT-FIX-41`, `-42`, `-57` için yeni ifade; §9 Step 2 devri; §10 Step 1.5 cümlesi.
4. **`ST1-A`:** metni kullanıcıya kısa bir değişiklik listesiyle göster ve "onay" bekle; değişiklik isterse taslağa işle, yeniden göster.
5. **`ST1-W`:** onaylı taslağı `py -3` betiğiyle uygula; `Main-Planing.md` CRLF: bayt sayımıyla CRLF'nin korunduğunu ve NUL 0'ı doğrula.
6. **Geçit:** `--mode step1 --strict` çıkış 0. `--mode all` yalnız `missing_phase_folder=…Faz-10-Plans` hatasıyla kırmızı kalır: beklenen ara durum (plan §7.2 "Ara durumlar ve geçitler"); başka her bulgu beklenmedik durumdur.

**(e) Kapanış** (beklenmedik durum yoksa sorulmadan):
- Plan §1'de `3 · O2a` `done`, commit'i başlığıyla anar; öneri `Window 3 O2a: Step 1 for planning run 21`.
- PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır; §11'e girdi eklenir.
- Bu dosya `3 · O2b` için ≤ 20 KB olarak yeniden yazılır.
- Değişen dosyalarda bayt ve boru kontrolü ve kimlik taraması (§7); yerel commit onay sorulmadan atılır; kullanıcıya `git show --stat` özeti ve yeni pencere çağrısı.
- Push yok; FF ve push `3 · O5`'te, onayla.

**Kabul:** `Main-Planing.md` Step 1 listesinin her maddesini karşılar; CRLF korunmuş, NUL 0; kullanıcı metni onaylamış; `--mode step1 --strict` çıkış 0; plan §1'de `3 · O2a` `done`; ledger, Index, Audit, Ontology, Comprehension, `docs/` ve alt planlar dokunulmamış.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7, §7.2, plan başlığındaki onaylar ve ledger §8.

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
| Pencere 3 planı | Onaylandı (2026-11-15, form "onay"); dört soruda öneriler | plan §7.2 |
| Dal | `integrate/impl-96` sürer; FF yalnız `3 · O5` | plan §7.2 |
| `PRB` | `3 · O1`'de yürütüldü (2026-11-15T13:01Z) | plan §7.1 `W3P01`–`W3P04` |
| Alt planlar | `Faz10.1` ölçüm, `10.2` sensör katmanı, `10.3` AGC tuzakları, `10.4` kutucuk ve WebUI, `10.5` v2.3 | plan §7.2 |
| Hetzner satırları | `3 · O4`'te orkestratör; 12. denetim doğrular | plan §7.2 |
| Döngü | Aşama başına oturum; kapanış sorulmadan; FF ve push ayrı onay | plan Onay 2, §0 |
| Bağlam eşiği | 400k; hedef 240k | plan Onay 3, §0 adım 9 |
| Yayın | C2 ve Window 2 takip commit'i push edildi; `3 · O0` kapanışı, takip commit'i ve `3 · O1` kapanışı yerel, push `3 · O5`'te | plan §1, §0 adım 5 |

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
11. Cihaza komut: yalnız salt-okur ve yalnız plan §7.2'de geçen komutlar (`PRB1`–`PRB10`); `3 · O2a` hiç göndermez. Fiziksel eylemler (kurulum, mod değiştirme, deklanşör, izin diyaloğu) kullanıcıda ve onaylı.
12. Yanlış cihaz: adb yalnız `platform-tools/adb.exe -s dc27e5d0`, betikler `ANDROID_SERIAL=dc27e5d0` ile.
13. Onaysız ve smoke bracket'sız modül kurma, mod değiştirme, AGC tercihlerine yazma.
14. ROM ya da kernel derlemesi başlatma.
15. Depoya sır (token, anahtar, parola, sunucu adresi) ya da başka cihazın seri numarasını yazma.
16. Geçmişi yeniden yazma (rebase, amend, force-push); tek istisna K8 (`DEC-31`).
17. Onaysız ya da örtük push: yalnız `git push origin main integrate/impl-96`, `--all`/`--mirror` asla; FF yalnız `git fetch . integrate/impl-96:main`. GitHub MCP push ve dosya araçları asla (hash'ler değişir).
18. `Kullanim.txt`, sürüm yerleri, `CHANGELOG.md` ve `docs/release-manifest.md`'e sürüm prosedürü dışında dokunma.
19. Kimlik değeri yazma ya da geri kazanma; tarama yalnız sayı ve konum basar.
20. Sıcak noktayı alt ajana yazdırma: ledger (yalnız orkestratör), `Main-Planing.md`, Index, Audit, Ontology, `CHANGELOG.md`, sürüm yerleri, manifest, `.gitignore`, `.gitattributes`, `snapshots/`, plan ve git (plan §3).
21. Satır sonu dönüştürme: ledger, `Main-Planing.md`, `Autopsy.md` CRLF, gerisi LF; CRLF dosyada ilk yazımdan sonra baytla doğrula.
22. `python` ya da `python3`: yalnız `py -3`.

## 7. Doğrulama komutları ve taban değerler

```bash
py -3 C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py --root . --mode all
py -3 C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py --root . --mode step1 --strict
py -3 C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py --root . --mode step4 --strict
py -3 scripts/build-release.py --self-test
```

| Kontrol | Taban (2026-11-14 ve 2026-11-15) |
|---|---|
| V1 `--mode all` | `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`; çıkış 0 |
| `--mode step1 --strict` | `3 · O2a` açılışında ölçülür; öngörü bulgu yok, çıkış 0 (`W3F30`) |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9`; çıkış 1 (taban, regresyon değil) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0` → PASS; `prose_mentions` değişebilir (artış hata değil) |

- Bu oturumda: `step1 --strict` ve `all` açılışta ve Step 1'den sonra; kimlik taraması kapanışta. V1–V3'ün yeni tabanı `3 · O4`'te yazılır (`subplan_count=47`).
- Kimlik taraması: Ek A.5 betiğini `write` ile `%TEMP%` altına yaz, depo kökünde `py -3 <yol>` ile çalıştır; değer basmaz.
- Koşu 21 kipleri (plan §7, §7.2): `step1` Step 1'den sonra; `step2` ve `step3-preflight` Step 2'den sonra; hepsi `--strict`. Step 1.5 (Autopsy) atlanır, `autopsy` kipi çalışmaz.
- Bayraksız `build-release.py` `dist/` zip'ini ve manifest'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- `python` Store stub'ıdır; `SKILL.md`'deki `python3` burada çalışmaz.
- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` aracı `wc`, `tail`, `cat`, `head`'i ve heredoc ile dosya yazmayı engelleyebilir: `read`/`grep` araçlarını ya da `%TEMP%`'teki `py -3` betiğini kullan; `<(…)` çalışmaz.
- **adb:** komutlar `py -3` betiğinden `subprocess.run(["platform-tools/adb.exe", "-s", "dc27e5d0", "shell", yük])` liste biçimiyle (kabuk tırnağı ve MSYS dönüşümü yok); `adb devices` başka cihazların serilerini basar, çalıştırma.
- **Alt ajanlar:** scout'ların kabuğu yok ama `local://`'a yazabilir ve bağlamları geniştir; `task` ajanları 100K bağlamlı: plan ya da PROJECT_LOG bütün verilmez. 2026-11-15'te bir devir taslağı scout'u içerik filtresince reddedildi (`reasoning_extraction`): görevi kısa ve somut yaz, yine olmazsa orkestratör yazar.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok); `gh api -i`'nin ilk satırı HTTP durumudur.
- **Depo silme (kullanıcı, `DEC-30`):** GitHub'da Settings → General → Danger Zone → Delete this repository; ya da kullanıcı kendi terminalinde `gh auth refresh -h github.com -s delete_repo` ve `gh repo delete ahmetxa/<ad> --yes`. Ajan silmez, yalnız ölçer.
- **`--grep` satır başına bağlanır** (`'^Window 3 O1:'`); `^` gövde satırlarını da eşler: commit gövdesinde başka bir aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`d = await commit.draft()`, `await d.take(...)`, `await d.commit(...)`); `git add`/`git commit` yok. Betikle değişen dosyalar "Review" altında görünür: dosyayı açıkça `take` et.
- **`local://` taşınmaz:** taslaklar ve kararlar kapanıştan önce plana ya da depodaki dosyaya yazılır.
- **Satır numaraları kayar:** plan §7.1'deki numaralar `6632a18` ağacına aittir; ledger'da `LSH` ve `LMAP`; `Planner-docs/` numaraları içerikle doğrulanır.
- **Tablolar:** hücrede `|` yok; ledger §4 satırı 10, §8 satırı 7 boru. `PRB` komutları (`PRB1`–`PRB10`; `C1`–`C3` ise commit'tir) bu yüzden plan §7.2'de kod bloğundadır.
- **Ledger** satırları 1–9 KB: yalnız `:raw:N-M`.
- **Ontology**'de 2 NUL: `grep` sessizce boş dönebilir (`AUDIT-FIX-22`); dosya bayt korumalı.
- **"Faz 10":** `50MP-Entegrasyon-Plani.md`'deki ayrı numaralama; yeni faz "ClaudeQB Phase 10", klasör `Faz-10-Plans`; yol haritası satırı tam `| 10 |` ile başlar (V:163).
- **Emekli Faz 7/8:** satırlar ve bölümler yerinde, ilk hücre korunarak tarihli notla kalır; satır silmek `extra_phase_folder_without_main_phase` uyarısını (`--strict`'te hata) doğurur; `Faz-7-Plans`/`Faz-8-Plans` dosyaları H1'i ve 13 başlığı korur.
- Doğrulayıcı tuzakları: plan §7 "Doğrulayıcı tuzakları" ve §7.2 "Ara durumlar ve geçitler"; kapsam dışı bulgular plan §10.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri (§4 a): ağaç temiz; dal `integrate/impl-96`; uç commit'in başlığı `Window 3 O1: …`; plan §1'de ilk `pending` aşama `3 · O2a`; §3'teki beklenen durum. Tutmayan her şey beklenmedik durumdur.
3. GitHub ölçümü (§4 b) ve bağlam ölçümü (§4 c).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin, bu oturumun yalnız `3 · O2a` olduğu.
5. Step 1 (§4 d): taban ölçümü, `ST1-R`, `ST1-D`; metni göster ve "onay" bekle; `ST1-W` ve geçit. Ardından §4 (e).

---
