# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> 2026-11-15'te, Pencere 3 · O2b'nin kapanış commit'inde yazıldı. Aşama: **Pencere 3 · O3a — Step 2 taslakları `Faz10.1`–`Faz10.3` (plan §7.3)**. Bu bir özettir; nihai kaynak plan (`ORCHESTRATION_PLAN.md`, Pencere 3 için §7.2 ve §7.3), ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC (`org.codeaurora.snapcam`) yapılandırması; hepsi AOSPA Android 15'te ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, kamera HAL'i farklı, proje modülleri kurulu değil.
Koşu 21'in Step 1'i (`3 · O2a`) Faz 7 ve 8'i emekli etti, kamera işini "ClaudeQB Phase 10"a (`Faz10.1`–`Faz10.5`) taşıdı; `3 · O2b` Step 2 kontratını plan §7.3'e yazdı.

1. **Tek aşama:** plan §1'deki ilk `pending` aşama satırı `3 · O3a`'dır: Step 2 taslakları `Faz10.1`–`Faz10.3`. Bu oturum yalnız onu yürütür; `3 · O3b` (`Faz10.4`, `Faz10.5`) ve sonrası sonraki oturumlardır. Aşama atlanmaz; oturum kendiliğinden sıradakine geçmez.
2. **Dosya kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** olgular 2026-11-13 ölçümü ve 2026-11-15 `PRB` ölçümüdür (plan §7.1 `W3P01`–`W3P04`). Bu aşama cihaza komut göndermez.
4. **Onay kapıları** (plan §0 adım 5): `main`'in fast-forward'ı (FF) ve her push (`3 · O5`); cihaz eylemi; AGC tercihlerine yazma. `3 · O3a`'nın kullanıcı kapısı yok; geçidi taslak betiği ve ara durumdur (plan §7.2). Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan yapılır.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; plan Ek A, `Planner-docs/` ve `docs/` İngilizce. Ajanlar: `scout`, `task`, `reviewer`, `security-reviewer`, `sonic` (`librarian`, `designer`, `isolated`, `outputSchema` yok).

## 1. Döngü ve bağlam bütçesi

- **Aşamalar** (plan §0): `O0`–`O5`; Pencere 3'ün düzeni plan §7.2 "Oturumlar" tablosundadır.
- **Eşik 400k** (plan §0 adım 9): bağlamı Ek A.7'deki JS betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok: işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, bu dosya, commit); kapanış 400k'dan önce biter. Bu beklenmedik durum değildir.
- **Tahmin:** bu oturum (`3 · O3a`) ≈ 185k (35k + 25 × 6k). Kalibrasyon (`3 · O2b`): açılış 82k, scout'lardan sonra 179k, inceleme düzeltmesinden sonra 268k (tahmin 225k). Orkestratör uzun metni okumaz ve yazmaz: taslaklar scout'larda, yerine koyma `cp` ile, Index eki `py -3` betiğiyle.
- **Hijyen:** 20 KB'tan büyük okuma scout'a; scout ≤ 4 KB döner, ayrıntıyı `local://`'a yazar. Büyük dosya `grep` ve dar `:N-M` ile okunur; aynı aralık iki kez okunmaz. Satırlar ≤ 600 bayt; `todo` ≤ 8 madde.
- **Beklenmedik durum** (plan §0 adım 6, liste orada): kapanış, commit ve bu dosyanın yeniden yazımı yok. Kullanıcıya sade dille: ne oldu, neden önemli, iki ya da üç seçenek ve önerin.

## 2. Okuma sırası

Plan ≈ 200 KB, `PROJECT_LOG.md` ≈ 195 KB, ledger ≈ 630 KB, Index ≈ 85 KB, `Main-Planing.md` ≈ 77 KB: hiçbiri bütün okunmaz; bölüm başları `grep '^##'` ile bulunur.

1. Plan §0, §1 ve §3 (§2 gerekirse).
2. Plan §7.3 bütünüyle (≈ 76 satır).
3. Plan §7.2'den dar aralıkla: "Görevler" (`SP1`–`SP3`, `CPa`), "Ara durumlar ve geçitler" (kırmızıya dönüş yolları dahil), "Sıcak noktalar".
4. §7.3'ün 10.1–10.3 için andığı satırlar: `W3F07`, `W3F20`–`W3F22`, `W3F26`, `W3F30`–`W3F32` (`grep '^| W3F'`), `W3P01`–`W3P04` (`grep '^| W3P'`); Ek A.2 `D1`–`D11`, `M1`, `TRAP`.
5. Plan Ek A.7 ve PROJECT_LOG §2.6; Ek A.5 betiği yalnız geçitte ve kapanışta.
6. `Main-Planing.md:276-312`, 42 alt plan, Index'in bütünü ve ClaudeQB Step 2 belgeleri yalnız scout'larla okunur.

## 3. Mevcut durum

**Beklenen durum (3 · O2b kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 81 commit. Uç: `Window 3 O2b: Step 2 contract for planning run 21` (`git log --grep '^Window 3 O2b:'`); altında `Window 3 O2a: Step 1 for planning run 21`. Etiket yok, 350 izlenen dosya.
- **`main` = `origin/main`** = `6632a18` `Window 2 follow-up: context budget and stage sizing`. `origin/main..HEAD` = 5 (`3 · O0` kapanışı, takip commit'i, `3 · O1`, `3 · O2a`, `3 · O2b`); hiçbiri push edilmedi; FF ve push `3 · O5`'te, ayrı onaylarla.
- **`git ls-remote origin`:** `HEAD`, `main`, `integrate/impl-96` = `6632a18`.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez); silinecek üç depo (`DEC-30`): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. 2026-11-15T18:35:38Z–18:35:40Z'de dördü de 200; ajan yalnız ölçer (404 = silinmiş).
- **`Main-Planing.md`** (`3 · O2a`, 14:10:06Z; `3 · O2b` dokunmadı): 406 satır, 77.019 bayt, CRLF, NUL 0, 10 faz; Phase 10 konusu `:284`–`:288`, kabul sinyalleri `:302`–`:306`; §9 sınırlı Step 2 (beş dosya ve Index, `:359`).
- **Plan:** 986 satır; §7.3 (76 satır) `3 · O2b`'de eklendi; eski boru uyumsuzluğu `:174`, `:835` (taban).
- **Ledger:** 653 satır, CRLF, NUL 0; `3 · O2a` ve `3 · O2b` dokunmadı; çapalar Ek A.6 `LMAP`. Koşu 21 satırı, snapshot'lar, `Faz10.M` satırları ve `DEC-33` `3 · O4`'te (`I3a`). Sonra 12. denetim (Pencere 4) ve `IMPL-97` (Pencere 5+).
- **Alt planlar:** 42; ledger §4'te 34 `verified`, 3 `implemented` (`Faz4.6`, `Faz6.1`, `Faz8.1`), 3 `planned` (`Faz7.2`, `Faz7.3`, `Faz8.3`), 2 `superseded` (`Faz4.1`, `Faz4.7`). `Faz-10-Plans/` henüz yok.
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` hâlâ v1.9 içeriğinde (`DEC-29`).
- **Telefon** (plan §7.1 `W3P`, Ek A.2, PROJECT_LOG §2.3): HyperOS 4 (`OS4.0.0.44.WMACNXM`), SukiSU-Ultra v4.3.0-r1, metamodül yok; HAL AOSPA'dan farklı, sensör = `EXPECT_MD5`; proje modülleri ve kutucuk yok; AGC yamasız V9.6, 10 tuzak.

## 4. Bu oturum: `3 · O3a`

Kaynak: plan §1, §0, §7.2 (`SP1`–`SP3` → `CPa`) ve §7.3. Yalnız `Planner-docs/Faz-10-Plans/`'teki üç yeni dosya ve Index'in Phase 10 girdileri yazılır (kapanış dosyaları (e)'de). Ledger, `Main-Planing.md`, Audit, Ontology, Comprehension ve `docs/` yazılmaz.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 3 O2b: Step 2 contract for planning run 21`; `git rev-list --count HEAD` = 81; `git rev-list --count origin/main..HEAD` = 5; `main` ve `origin/main` = `6632a18`; `git tag` boş; `git ls-files` = 350; `git ls-remote origin` (§3). Plan §1'de ilk `pending` = `3 · O3a`.
Snapshot (plan §7.3): `Planner-docs/Main-Planing.md` sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 77.019 bayt, 406 satır, CRLF, NUL 0. Tutmayan her şey beklenmedik durumdur.

**(b) GitHub ölçümü:** dört depo için `gh api -i repos/ahmetxa/<ad>` (UTC; ilk satır HTTP durumu). 404 varsa PROJECT_LOG'un silme cümleleri güncellenir (yerler plan §7 "Açılışta ayrıca").

**(c) Bağlam ölçümü:** Ek A.7 betiği (`eval`), oturum başında ve her alt ajan sonucundan sonra (§1).

**(d) Step 2 taslakları:**
1. **Taban:** `step1 --strict` ve `all`; beklenen §7'deki Step 1 sonrası ara durumdur. Başka her bulgu beklenmedik durumdur.
2. **`SP1` ∥ `SP2` ∥ `SP3`:** üç geniş bağlamlı salt-okur scout aynı turda; her biri bir taslağı `local://`'a yazar (`SP1` → `Faz10.1`, `SP2` → `10.2`, `SP3` → `10.3`), ≤ 4 KB döner (yol, bayt, bölüm başına bir satır, `open_issues`). Görev metni: §7.3'ten o alt planın satırları, tek sahip haritası ve "Ortak bağlam"ın tamamı; `Main-Planing.md:276-312`; §2 madde 4'teki kanıt satırları. Biçim örneği `Faz9.1`, `Faz3.1`: yalnız biçim, cümle değil.
3. **Taslak betiği** (`%TEMP%/ishtar-st3/`, `py -3`; doğrulayıcıyı `scan.py` gibi yükler):
   - dosya adı (V:157); H1 (V:165) ve hemen `## 1. Context`; 13 başlık sırayla, `###` yok; bölümler ≥ 20 karakter;
   - §9 başlığı, State değerleri, boş olmayan Purpose ve kimlik hücreleri; `existing` dışı her yol sahip haritasında (`snapshots/` `generated` serbest);
   - TODO, TBD, FIXME ve yer tutucu yok; LF, CR 0, NUL 0; kimlik taraması;
   - tekrar: 42 dosya ve öteki taslaklarla §3, §6, §8, §11'de 80+ karakterlik cümle iki kez geçmez; §3 ve §7'de 160+ karakterlik gövde tekrarı yok.
   - Bulguyu taslağın scout'u düzeltir; orkestratör taslağı yeniden yazmaz.
4. **`CPa`:** betik geçince üç taslak `cp` ile `Planner-docs/Faz-10-Plans/`'e konur (adlar §7.3). Index'e yalnız §7.3 "Step 2 yazımı"ndaki girdiler, `lines.py` ile sondan başa (numaralar kaymaz), satırlar önce içerikle doğrulanarak: §6 sayıları (`:292`–`:293`) 10 faz, 45 dosya; §4 öncelik listesinde Phase 10 (`:180`'den sonra); Phase 10 bloğu (`:160`'tan sonra: kalın paragraf ve `Faz-10-Plans/Faz10.M-….md` maddeleri, V:158); faz tablosu satırı (`:38`'den sonra); "Detected phase count" (`:24`) 10.
5. **Geçit:** `step2 --strict` ve `all` (§7, `CPa`'dan sonra beklenen); bayt (LF, CR 0, NUL 0; orkestratörün satırları ≤ 600 bayt), boru (plan tabanı `:174`, `:835`), kimlik (§7).

**(e) Kapanış** (beklenmedik durum yoksa sorulmadan):
- Plan §1'de `3 · O3a` `done`, commit'i başlığıyla anar: `Window 3 O3a: Step 2 drafts 10.1-10.3 for planning run 21`. PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır, §11'e girdi eklenir; bu dosya `3 · O3b` için ≤ 20 KB yeniden yazılır.
- Bayt, boru ve kimlik (§7); yerel commit sorulmadan; kullanıcıya `git show --stat` özeti ve yeni pencere çağrısı. Push yok.

**Kabul:** üç dosya `W3F07` biçiminde, §7.3 kapsamı ve tek sahip haritasıyla; Index girdileri yazılmış; `step2 --strict` çıkış 0; `all` çıkış 0 ve `subplan_count=45`; bayt, boru ve kimlik geçti; ledger dokunulmamış; plan §1'de `3 · O3a` `done`.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7, §7.2, §7.3, plan başlığındaki onaylar ve ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| K1 `Kullanim.txt` | (b): v2.3'te düzeltilir (soru 4) | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K5/K6 üç depo | Silinecek; kullanıcı siler; açılışta ölçülür | `DEC-30` |
| K7 HyperOS 4 yönü | (a) modülü uyarla; (i) "ClaudeQB Phase 10", Faz 7 ve 8 tümüyle emekli (soru 5) | `DEC-32` |
| K9 50MP HAL | Hayır, şimdilik; sensör katmanı sürer (soru 1) | `DEC-33` (koşu 21) |
| Sekiz soru | Yanıtlandı (2026-11-15); soru 8: sınırlı Step 2, Step 1.5 atlandı | plan §7 |
| Pencere 3 planı | Onaylandı (2026-11-15, form "onay"); dört soruda öneriler | plan §7.2 |
| Step 1 metni | Onaylandı (2026-11-15T14:10Z, form "onay"; C01–C03 dahil) | `Main-Planing.md` |
| Step 2 kontratı | Onaylandı (2026-11-15, form "onay"; dal sürer) | plan §7.3 |
| Snapshot | Step 2 durmaz; etkin plan bugünkü `Main-Planing.md` (sha256 `6790b6ae…`); snapshot satırları `3 · O4`'te `I3a` | plan §7.3 |
| Atıf | Phase 10 ve emeklilikler koşu 21'in seçimi (kullanıcı, 2026-11-15); `DEC-28` yalnız Faz 7/8'i, `DEC-32` yalnız uyarlamayı anar | ledger `:606`, `:610` |
| Dal | `integrate/impl-96` sürer; FF yalnız `3 · O5` | plan §7.2 |
| Alt planlar | `Faz10.1` ölçüm, `10.2` sensör katmanı, `10.3` AGC tuzakları, `10.4` kutucuk ve WebUI, `10.5` v2.3 | plan §7.2, §7.3 |
| Hetzner satırları | `3 · O4`'te orkestratör; 12. denetim doğrular | plan §7.2 |
| Yayın | C2 ve Window 2 takip commit'i push edildi; sonraki beş commit yerel, push `3 · O5`'te | plan §1, §0 adım 5 |

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
11. Cihaza komut: yalnız salt-okur ve yalnız plan §7.2'de geçen komutlar (`PRB1`–`PRB10`); `3 · O3a` hiç göndermez. Fiziksel eylemler (kurulum, mod değiştirme, deklanşör, izin diyaloğu) kullanıcıda ve onaylı.
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
py -3 $V --root . --mode step2 --strict
py -3 $V --root . --mode step4 --strict
py -3 scripts/build-release.py --self-test
```

| Kontrol | Taban (2026-11-14 ve 2026-11-15) |
|---|---|
| V1 `--mode all` | Step 1'den önce (13:18:54Z): `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`; çıkış 0. Step 1'den sonra (14:10Z; 18:35:38Z aynı) ek olarak `missing_phase_folder=Planner-docs/Faz-10-Plans` (`error_count=1`), çıkış 1: beklenen ara durum |
| `CPa`'dan sonra (beklenen) | `step2 --strict` bulgu yok, çıkış 0; `all` yalnız denetim uyarısı, `subplan_count=45`, çıkış 0 (`3 · O3b`'den sonra 47) |
| `--mode step1 --strict` | 14:10Z ve 18:35:38Z: bulgu yok, `main_phase_count=10`, çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9`; çıkış 1 (taban, regresyon değil) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | `3 · O2b`, §7.3'ten sonra: `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=17` → PASS; `prose_mentions` artabilir (hata değil) |

- V1–V3'ün yeni tabanı `3 · O4`'te yazılır (`subplan_count=47`).
- Kimlik taraması: Ek A.5 betiği (`%TEMP%/idscan.py` 2026-11-15'te onunla aynıydı) depo kökünde `py -3` ile; değer basmaz.
- Koşu 21 kipleri (plan §7.2): `step1` Step 1'den, `step2` ve `step3-preflight` Step 2'den sonra, `--strict`; `autopsy` yok (Step 1.5 atlandı).
- Bayraksız `build-release.py` `dist/` zip'ini ve manifest'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- `python` Store stub'ıdır; `SKILL.md`'deki `python3` burada çalışmaz.
- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` aracı `cat`, `head`, `grep`, `wc`, `tail`'i ve heredoc ile dosya yazmayı engelleyebilir: `read`/`grep` araçlarını ya da `%TEMP%`'teki `py -3` betiğini kullan; `<(…)` çalışmaz.
- **Betikler:** `%TEMP%/ishtar-st1/lines.py` LF dosyada replace, append ve check (bayt, tablo boruları); `%TEMP%/ishtar-st2/scan.py` doğrulayıcıyı `importlib` ile yükler (`split_sentences`, `section_body`, `markdown_tables`).
- **Tekrar kuralı:** taslak §7.3'ün, `Main-Planing.md`'nin ya da bir alt planın 80+ karakterlik cümlesini kopyalamaz, çevirmez. Üç taslak aynı ortak bağlamdan doğar: değişmez, onay ve bracket cümleleri her birinde kendi sözleriyle.
- **Snapshot:** sha256 dosya baytlarından (`hashlib`, CRLF dahil); tutmazsa beklenmedik durumdur, taslak yazılmaz (plan §7.3).
- **Tek sahip:** taslak yalnız kendi sahip satırının yollarını `proposed`, `modified`, `generated` yazar, öteki yolları `existing`; haritada olmayan yol `open_issues`'a, kararı `CPa`'da orkestratör verir.
- **`snapshots/`:** yalnız eklemeli; yeni ad `<tarih-saat>__Faz10.M__<ad>` (`Faz3.7:71`), State `generated`; var olan dosya değişmez.
- **Alt ajanlar:** scout'un kabuğu yok, `local://`'a yazar; `task` 100K bağlamlı: plan ya da PROJECT_LOG bütün verilmez. İçerik filtresi (`reasoning_extraction`) reddederse görev kısa ve somut yazılır.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok; depoları kullanıcı siler, `DEC-30`).
- **`--grep` satır başına bağlanır** (`'^Window 3 O2b:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`d = await commit.draft()`, `await d.take(...)`, `await d.commit(...)`); `git add`/`git commit` yok. Betikle ya da `cp` ile değişen dosyalar "Review" altında görünür: açıkça `take` et.
- **`local://` taşınmaz:** taslaklar ve kararlar kapanıştan önce plana ya da depodaki dosyaya yazılır.
- **Satır numaraları kayar:** §7.3'tekiler `Window 3 O2a` ağacına, §7.1 ve §7.2'deki `Main-Planing.md` numaraları Step 1'den önceki 316 satıra aittir; ledger'da `LSH`, `LMAP`; hepsi içerikle doğrulanır.
- **Tablolar:** hücrede `|` yok; ledger §4 satırı 10, §8 satırı 7 boru.
- **Ontology**'de 2 NUL: `grep` sessizce boş dönebilir (`AUDIT-FIX-22`); dosya bayt korumalı.
- **"Faz 10":** `50MP-Entegrasyon-Plani.md`'deki numaralama ayrıdır; yeni faz "ClaudeQB Phase 10", klasör `Faz-10-Plans`, yol haritası satırı tam `| 10 |` (V:163). Önce yalnız 10.1–10.3: numara boşluğu olmaz (V:1040-1043).
- **Emekli Faz 7/8:** satırlar, bölümler ve dosyalar yerinde kalır, dosyalar H1'i ve 13 başlığı korur (silmek `--strict`'te `extra_phase_folder_without_main_phase`).
- Doğrulayıcı tuzakları: plan §7 "Doğrulayıcı tuzakları" ve §7.2 "Ara durumlar ve geçitler"; kapsam dışı bulgular plan §10.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri ve snapshot ölçümü (§4 a); plan §1'de ilk `pending` aşama `3 · O3a`. Tutmayan her şey beklenmedik durumdur.
3. GitHub ölçümü (§4 b), bağlam ölçümü (§4 c) ve doğrulayıcı tabanı (§4 d1).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin, bu oturumun yalnız `3 · O3a` olduğu.
5. Step 2 taslakları (§4 d): `SP1` ∥ `SP2` ∥ `SP3`, taslak betiği, `CPa` ve geçit. Ardından §4 (e).

---
