# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> 2026-11-15'te, Pencere 3 · O2a'nın kapanış commit'inde yazıldı. Aşama: **Pencere 3 · O2b — Step 2 kontratı (plan §7.3)**. Bu bir özettir; nihai kaynak plan (`ORCHESTRATION_PLAN.md`, Pencere 3 için §7.2), ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC (`org.codeaurora.snapcam`) yapılandırması; hepsi AOSPA Android 15'te ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, kamera HAL'i farklı, proje modülleri kurulu değil.
Koşu 21'in Step 1'i (`3 · O2a`) Faz 7 ve 8'i `Main-Planing.md`'de emekli etti; kamera işi "ClaudeQB Phase 10"a (`Faz10.1`–`Faz10.5`, plan §7.2) geçti.

1. **Tek aşama:** plan §1'deki ilk `pending` aşama satırı `3 · O2b`'dir: Step 2 kontratı, yalnız plan §7.3. Bu oturum yalnız `O2b`'yi yürütür; `3 · O3a` ve sonrası sonraki oturumlardır. Aşama atlanmaz; oturum kendiliğinden sıradakine geçmez.
2. **Dosya kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** olgular 2026-11-13 ölçümü ve 2026-11-15 `PRB` ölçümüdür (plan §7.1 `W3P01`–`W3P04`). Bu aşama cihaza komut göndermez.
4. **Onay kapıları** (plan §0 adım 5): `main`'in fast-forward'ı (FF) ve her push (`3 · O5`); cihaz eylemi; AGC tercihlerine yazma. `3 · O2b`'nin kullanıcı kapısı yok; geçidi bayt, boru ve kimlik taramasıdır (plan §7.2). Depoları kullanıcı siler. Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan yapılır.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; plan Ek A, `Planner-docs/` ve `docs/` İngilizce. Ajanlar: `scout`, `task`, `reviewer`, `security-reviewer`, `sonic` (`librarian`, `designer`, `isolated`, `outputSchema` yok).

## 1. Döngü ve bağlam bütçesi

- **Aşamalar** (plan §0): `O0`–`O5`; Pencere 3'ün düzeni plan §7.2 "Oturumlar" tablosundadır.
- **Eşik 400k** (plan §0 adım 9): bağlamı Ek A.7'deki JS betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok: işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, bu dosya, commit); kapanış 400k'dan önce biter. Bu beklenmedik durum değildir.
- **Tahmin:** bu oturum (`3 · O2b`) ≈ 225k (35k + 10k okuma + 15 × 12k). Kalibrasyon (`3 · O2a`): açılışta 86k, `ST1-R` gönderiminden sonra 154k, onaydan önce 207k, kapanış başında ≈ 241k (tahmin 225k). Orkestratör uzun metni okumaz ve yazmaz: taslak `local://`'da, uygulama `py -3` betiğiyle.
- **Hijyen:** 20 KB'tan büyük okuma scout'a; scout ≤ 4 KB döner, ayrıntıyı `local://`'a yazar. Büyük dosya `grep` ve dar `:N-M` ile okunur; aynı aralık iki kez okunmaz. Taslak `cp` ile yerine konur, betikle doğrulanır, yeniden yazılmaz. Satırlar ≤ 600 bayt; `todo` ≤ 8 madde.
- **Beklenmedik durum** (plan §0 adım 6, liste orada): kapanış, commit ve bu dosyanın yeniden yazımı yok. Kullanıcıya sade dille: ne oldu, neden önemli, iki ya da üç seçenek ve önerin.

## 2. Okuma sırası

Plan ≈ 187 KB, `PROJECT_LOG.md` ≈ 185 KB, ledger ≈ 630 KB, `Main-Planing.md` ≈ 77 KB: hiçbiri bütün okunmaz; bölüm başları `grep '^##'` ile bulunur.

1. Plan §0, §1 ve §3 (§2 gerekirse).
2. Plan §7.2 bütünüyle: alt planlar, oturumlar, görevler (§7.3'ün okurları `SP1`–`SP5`, `CPa`, `CPb`, `I3a`, `I3b`), `W3F28` kararları, ara durumlar ve geçitler, sıcak noktalar.
3. Plan §7'de dar aralıkla: "Step 2 — yeni alt planlar", "Aday alt planlar", "Doğrulayıcı tuzakları". `W3F06`, `W3F07` (§7.1) ve `W3F30` (§7.2; `grep '^| W3F'`).
4. Plan Ek A.7 ve PROJECT_LOG §2.6; Ek A.5 betiği yalnız kapanışta.
5. ClaudeQB Step 2 dosyaları (`Second-Planner.md`, `run-step2.md`), `Main-Planing.md`, 42 alt plan, ledger, Index ve Ontology yalnız scout'larla okunur (`ST2-R`).

## 3. Mevcut durum

**Beklenen durum (3 · O2a kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 80 commit. Uç: `Window 3 O2a: Step 1 for planning run 21` (`git log --grep '^Window 3 O2a:'`); altında `Window 3 O1: plan for planning run 21`. Etiket yok, 350 izlenen dosya.
- **`main` = `origin/main`** = `6632a18` `Window 2 follow-up: context budget and stage sizing`. `origin/main..HEAD` = 4 (`3 · O0` kapanışı, takip commit'i, `3 · O1` ve `3 · O2a` kapanışları); hiçbiri push edilmedi. FF ve push `3 · O5`'te, ayrı onaylarla.
- **`git ls-remote origin`:** `HEAD`, `main`, `integrate/impl-96` = `6632a18`.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez). Silinecek üç depo (`DEC-30`): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. 2026-11-15T13:18:54Z–13:19:01Z'de dördü de 200. Silmeyi kullanıcı yapar; ajan yalnız ölçer (404 = silinmiş).
- **`Main-Planing.md`** (Step 1, 14:10:06Z, 49 değişiklik): 406 satır, 77.019 bayt, CRLF, NUL 0. Faz 7 ve 8 yerinde emekli; yeni 10 satırı ve `### Phase 10 — HyperOS 4 camera module adaptation` (`Faz10.1`–`Faz10.5` sırayla); Faz 6'nın ROM hedefi emekli (`Faz6.2` verified kalır); §4 hedefi HyperOS 4; `AUDIT-FIX-41`, `-42`, `-57` yeni ifadeyle; R8 gerçekleşti, R9 konusuz; §9 sınırlı Step 2 (yalnız `Faz10.1`–`Faz10.5` ve Index girdileri); §10 Step 1.5 atlaması.
- **Ledger:** `3 · O2a` dokunmadı: 653 satır, CRLF, NUL 0; çapalar Ek A.6 `LMAP` (`DEC-27`…`DEC-32` `:605`–`:610`). `DEC-33` henüz yok; koşu 21 `3 · O4`'te yazar.
- **Alt planlar:** 42; ledger §4'te 34 `verified`, 3 `implemented` (`Faz4.6`, `Faz6.1`, `Faz8.1`), 3 `planned` (`Faz7.2`, `Faz7.3`, `Faz8.3`), 2 `superseded` (`Faz4.1`, `Faz4.7`).
- **11. denetim** (2026-09-14, `PASS_WITH_WARNINGS`): kuyruk 2026-11-13'ten beri geçersiz (`DEC-28`).
- **Sıradaki numaralar:** koşu 21 (Pencere 3), 12. denetim (Pencere 4), `IMPL-97` (Pencere 5+), `DEC-33` (koşu 21).
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` hâlâ v1.9 içeriğinde (`DEC-29`).

**Telefon** (plan §7.1 `W3P01`–`W3P04`; Ek A.2 `D1`–`D11`, `M1`, `TRAP`; PROJECT_LOG §2.3):
- HyperOS `OS4.0.0.44.WMACNXM` (Android 17, kernel 5.15.215, SELinux Enforcing); SukiSU-Ultra v4.3.0-r1 (`com.sukisu.ultra`, versionCode 41140); `su` diyalogsuz; metamodül yok. HAL md5 `2a955e68…` (AOSPA `c3fa63a8…` değil); sensör md5 `9e4d0fe1…` = `EXPECT_MD5`.
- Proje modülleri ve kutucuk yok; AGC yamasız V9.6, 10 tuzak; tercih dosyasının sahibi ve etiketi AOSPA'dan farklı. [ÇIKARIM] HAL koruması kapalı başarısız olur; `setmode.sh` HyperOS'ta çalışmayan `vendor.camera-provider-2-7-ext`'i başlatır.

## 4. Bu oturum: `3 · O2b`

Kaynak: plan §1 (`3 · O2b` satırı), §0, §7.2 (`ST2-R` → `ST2-K`) ve §2'deki §7 bölümleri. Bu oturum yalnız plan §7.3'ü yazar; kapanışta plan §1, PROJECT_LOG §2.6 ve §11 ve bu dosya. `Planner-docs/` ve `docs/` yazılmaz.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 3 O2a: Step 1 for planning run 21`; `git rev-list --count origin/main..HEAD` = 4; `main` ve `origin/main` = `6632a18`; `git tag` boş; `git ls-files` = 350; `git ls-remote origin` (§3). Plan §1'de ilk `pending` = `3 · O2b`. Tutmayan her şey beklenmedik durumdur.

**(b) GitHub ölçümü:** dört depo için `gh api -i repos/ahmetxa/<ad>` (UTC; ilk satır HTTP durumu). 404 varsa PROJECT_LOG'un silme cümleleri güncellenir (yerler plan §7 "Açılışta ayrıca").

**(c) Bağlam ölçümü:** Ek A.7 betiği (`eval`), oturum başında ve her alt ajan sonucundan sonra (§1).

**(d) Step 2 kontratı:**
1. **Taban:** `--mode step1 --strict` ve `--mode all`; beklenen, §7 tablosundaki Step 1 sonrası ara durumdur (plan §7.2 "Ara durumlar ve geçitler"). `Planner-docs/` bu aşamada değişmez; başka her bulgu beklenmedik durumdur.
2. **`ST2-R`:** üç paralel scout, her biri ≤ 4 KB döner, yerler içerikle doğrulanır. Öneri: (1) `run-step2.md`, `Second-Planner.md` (`W3F06`), `Main-Planing.md`'nin bütün fazları ve destek belgeleri; (2) 42 alt plan: biçim (`W3F07`), §9 tabloları, tekrar kuralına girebilecek gövde cümleleri; (3) ledger §2, §3, §4, §8 hedefleri, Index (`:258`, `:279`, Phase 10 girdilerinin yeri), Ontology değişmez 10 ve 11.
3. **`ST2-K`:** orkestratör plan §7.3'ü yazar (taslak `local://`'da, ekleme `py -3` betiğiyle):
   - alt plan sözleşmesi: `Faz10.1`–`Faz10.5` için dosya adı (son ek burada kesinleşir), H1, kapsam, kanıt (`W3F`, `W3P`, Ek A.2), bağımlılık, §9 yolları ve her yolun tek sahibi, taslak görevi (`SP1`–`SP5`) ve oturumu;
   - ortak bağlam: `W3F07` biçimi, tekrar kuralı ve öteki doğrulayıcı tuzakları, TODO/TBD yok, kimlik değeri yok, `DEC-33`, §6'daki değişmezler;
   - `3 · O4` hedef tablosu: `I3a` (ledger) ve `I3b` (Index, Ontology, Comprehension, toolchain `:220`) için her hedef satır.
4. **Açık soru (snapshot):** `run-step2.md` adım 6, etkin plan snapshot'ı değiştiyse Step 2'yi durdurur; yeni §9 koşu 21'in MAIN snapshot'ını kimin kaydettiğini söylemez (plan: ledger §3, `3 · O4`, `I3a`). İnceleyicinin `3 · O2b`'ye ertelenen P3 önerisi: koşu 21 snapshot'ı ledger'a kaydeder, Step 2 yeni `Main-Planing.md`'yi etkin plan sayar ve durmaz. Karar §7.3'e girer.
5. **Geçit:** bayt (LF, CR 0, NUL 0, değişen satırlar ≤ 600 bayt) ve boru kontrolü (plan `:174` ve `:759`'daki eski uyumsuzluk tabandır; numaralar `3 · O2a` kapanışındaki ağaca aittir); kimlik taraması (§7).

**(e) Kapanış** (beklenmedik durum yoksa sorulmadan):
- Plan §1'de `3 · O2b` `done`, commit'i başlığıyla anar; öneri `Window 3 O2b: Step 2 contract for planning run 21`. PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır, §11'e girdi eklenir; bu dosya `3 · O3a` için ≤ 20 KB olarak yeniden yazılır.
- Bayt, boru ve kimlik (§7); yerel commit sorulmadan; kullanıcıya `git show --stat` özeti ve yeni pencere çağrısı. Push yok.

**Kabul:** plan §7.3 `Faz10.1`–`Faz10.5`'in her birini (dosya adı, kapsam, kanıt, §9 yolları, tek sahip) ve `3 · O4`'ün her hedef satırını tanımlar; snapshot sorusu karara bağlanmış; bayt, boru ve kimlik geçti; plan §1'de `3 · O2b` `done`; `Planner-docs/` ve `docs/` dokunulmamış.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7, §7.2, plan başlığındaki onaylar ve ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| K1 `Kullanim.txt` | (b): v2.3'te düzeltilir (soru 4) | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K5/K6 üç depo | Silinecek; kullanıcı siler; açılışta ölçülür | `DEC-30` |
| K7 HyperOS 4 yönü | (a) modülü uyarla; (i) "ClaudeQB Phase 10", Faz 7 ve 8 tümüyle emekli (soru 5) | `DEC-32` |
| K9 50MP HAL | Hayır, şimdilik; sensör katmanı sürer (soru 1) | `DEC-33` (koşu 21) |
| Sekiz soru | Yanıtlandı (2026-11-15); soru 8: sınırlı Step 2, ayrı oturumlar, Step 1.5 atlandı | plan §7 |
| Pencere 3 planı | Onaylandı (2026-11-15, form "onay"); dört soruda öneriler | plan §7.2 |
| Step 1 metni | Onaylandı (2026-11-15T14:10Z, form "onay"; isteğe bağlı C01–C03 dahil) | `Main-Planing.md` |
| Atıf | Phase 10'un açılması, Faz 7/8'in ve Faz 6 ROM hedefinin emekliliği koşu 21'in seçimi (kullanıcı, 2026-11-15); `DEC-28` yalnız Faz 7/8'i, `DEC-32` yalnız uyarlamayı anar | ledger `:606`, `:610` |
| Dal | `integrate/impl-96` sürer; FF yalnız `3 · O5` | plan §7.2 |
| Alt planlar | `Faz10.1` ölçüm, `10.2` sensör katmanı, `10.3` AGC tuzakları, `10.4` kutucuk ve WebUI, `10.5` v2.3 | plan §7.2 |
| Hetzner satırları | `3 · O4`'te orkestratör; 12. denetim doğrular | plan §7.2 |
| Yayın | C2 ve Window 2 takip commit'i push edildi; sonraki dört commit yerel, push `3 · O5`'te | plan §1, §0 adım 5 |

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
11. Cihaza komut: yalnız salt-okur ve yalnız plan §7.2'de geçen komutlar (`PRB1`–`PRB10`); `3 · O2b` hiç göndermez. Fiziksel eylemler (kurulum, mod değiştirme, deklanşör, izin diyaloğu) kullanıcıda ve onaylı.
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
V=C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py
py -3 $V --root . --mode all
py -3 $V --root . --mode step1 --strict
py -3 $V --root . --mode step4 --strict
py -3 scripts/build-release.py --self-test
```

| Kontrol | Taban (2026-11-14 ve 2026-11-15) |
|---|---|
| V1 `--mode all` | Step 1'den önce (13:18:54Z): `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`; çıkış 0. Step 1'den sonra (14:10Z) ek olarak `missing_phase_folder=Planner-docs/Faz-10-Plans` (`error_count=1`), çıkış 1: beklenen ara durum |
| `--mode step1 --strict` | 14:10Z: bulgu yok, `main_phase_count=10`, çıkış 0 (Step 1'den önce `9`) |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9`; çıkış 1 (taban, regresyon değil) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0` → PASS; `prose_mentions` değişebilir (artış hata değil) |

- Bu oturumda: `step1 --strict` ve `all` açılışta; bayt, boru ve kimlik taraması kapanışta. V1–V3'ün yeni tabanı `3 · O4`'te yazılır (`subplan_count=47`).
- Kimlik taraması: Ek A.5 betiği (`%TEMP%/idscan.py` 2026-11-15'te onunla aynıydı) depo kökünde `py -3` ile; değer basmaz.
- Koşu 21 kipleri (plan §7.2): `step1` Step 1'den, `step2` ve `step3-preflight` Step 2'den sonra, hepsi `--strict`; `autopsy` çalışmaz (Step 1.5 atlandı).
- Bayraksız `build-release.py` `dist/` zip'ini ve manifest'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- `python` Store stub'ıdır; `SKILL.md`'deki `python3` burada çalışmaz.
- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` aracı `cat`, `head`, `grep`, `wc`, `tail`'i ve heredoc ile dosya yazmayı engelleyebilir: `read`/`grep` araçlarını ya da `%TEMP%`'teki `py -3` betiğini kullan; `<(…)` çalışmaz.
- **Betik:** `%TEMP%/ishtar-st1/lines.py` LF dosyalarda replace, append ve check yapar (`check` = bayt ve tablo boruları); yeniden kullanılabilir.
- **adb:** yalnız `py -3` betiğinden, `subprocess.run` liste biçimiyle (kabuk tırnağı yok); `adb devices` başka cihazların serilerini basar, çalıştırma.
- **Alt ajanlar:** scout'ların kabuğu yok ama `local://`'a yazabilir, bağlamları geniştir; `task` ajanları 100K bağlamlı: plan ya da PROJECT_LOG bütün verilmez. İçerik filtresi (`reasoning_extraction`) scout'u reddederse görevi kısa ve somut yaz.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok).
- **Depo silme (kullanıcı, `DEC-30`):** GitHub Settings → Danger Zone → Delete this repository ya da kullanıcının terminalinde `gh auth refresh -h github.com -s delete_repo` ve `gh repo delete ahmetxa/<ad> --yes`; ajan yalnız ölçer.
- **`--grep` satır başına bağlanır** (`'^Window 3 O2a:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`d = await commit.draft()`, `await d.take(...)`, `await d.commit(...)`); `git add`/`git commit` yok. Betikle değişen dosyalar "Review" altında görünür: dosyayı açıkça `take` et.
- **`local://` taşınmaz:** taslaklar ve kararlar kapanıştan önce plana ya da depodaki dosyaya yazılır.
- **Satır numaraları kayar:** plan §7.1 ve §7.2'deki `Main-Planing.md` numaraları Step 1'den önceki 316 satıra aittir; ledger'da `LSH` ve `LMAP`; `Planner-docs/` numaraları içerikle doğrulanır.
- **Tablolar:** hücrede `|` yok; ledger §4 satırı 10, §8 satırı 7 boru; `PRB` komutları bu yüzden plan §7.2'de kod bloğundadır.
- **Ledger** satırları 1–9 KB: yalnız `:raw:N-M`.
- **Ontology**'de 2 NUL: `grep` sessizce boş dönebilir (`AUDIT-FIX-22`); dosya bayt korumalı.
- **"Faz 10":** `50MP-Entegrasyon-Plani.md`'deki ayrı numaralama; yeni faz "ClaudeQB Phase 10", klasör `Faz-10-Plans`; yol haritası satırı tam `| 10 |` ile başlar (V:163).
- **Emekli Faz 7/8:** satırlar ve bölümler yerinde kalır (silmek `extra_phase_folder_without_main_phase`, `--strict`'te hata); `Faz-7-Plans`/`Faz-8-Plans` dosyaları H1'i ve 13 başlığı korur.
- Doğrulayıcı tuzakları: plan §7 "Doğrulayıcı tuzakları" ve §7.2 "Ara durumlar ve geçitler"; kapsam dışı bulgular plan §10.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri (§4 a); plan §1'de ilk `pending` aşama `3 · O2b`. Tutmayan her şey beklenmedik durumdur.
3. GitHub ölçümü (§4 b), bağlam ölçümü (§4 c) ve doğrulayıcı tabanı (§4 d1).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin, bu oturumun yalnız `3 · O2b` olduğu.
5. Step 2 kontratı (§4 d): `ST2-R`, ardından `ST2-K` (snapshot sorusu dahil) ve geçit. Ardından §4 (e).

---
