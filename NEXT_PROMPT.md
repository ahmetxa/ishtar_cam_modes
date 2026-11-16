# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> 2026-11-16'da, Pencere 3 · O3a'nın kapanış commit'inde yazıldı. Aşama: **Pencere 3 · O3b — Step 2 taslakları `Faz10.4`–`Faz10.5` (plan §7.3)**. Bu bir özettir; nihai kaynak plan (`ORCHESTRATION_PLAN.md`, Pencere 3 için §7.2 ve §7.3), ledger ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC (`org.codeaurora.snapcam`) yapılandırması; hepsi AOSPA Android 15'te ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, kamera HAL'i farklı, proje modülleri kurulu değil.
Koşu 21: Step 1 (`3 · O2a`) Faz 7 ve 8'i emekli etti, işi "ClaudeQB Phase 10"a (`Faz10.1`–`Faz10.5`) taşıdı; `3 · O2b` kontratı (§7.3), `3 · O3a` `Faz10.1`–`Faz10.3`'ü yazdı.

1. **Tek aşama:** plan §1'deki ilk `pending` aşama satırı `3 · O3b`'dir: Step 2 taslakları `Faz10.4`, `Faz10.5`. Bu oturum yalnız onu yürütür; `3 · O4` ve sonrası sonraki oturumlardır. Aşama atlanmaz; oturum kendiliğinden sıradakine geçmez.
2. **Dosya kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** olgular 2026-11-13 ölçümü ve 2026-11-15 `PRB` ölçümüdür (plan §7.1 `W3P01`–`W3P04`). Bu aşama cihaza komut göndermez.
4. **Onay kapıları** (plan §0 adım 5): `main`'in fast-forward'ı (FF) ve her push (`3 · O5`); cihaz eylemi; AGC tercihlerine yazma. `3 · O3b`'nin kullanıcı kapısı yok; geçidi taslak betiği ve ara durumdur (plan §7.2). Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan yapılır.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; plan Ek A, `Planner-docs/` ve `docs/` İngilizce. Ajanlar: `scout`, `task`, `reviewer`, `security-reviewer`, `sonic` (`librarian`, `designer`, `isolated`, `outputSchema` yok).

## 1. Döngü ve bağlam bütçesi

- **Aşamalar** (plan §0): `O0`–`O5`; Pencere 3'ün düzeni plan §7.2 "Oturumlar" tablosundadır.
- **Eşik 400k** (plan §0 adım 9): bağlamı Ek A.7'deki JS betiğiyle (`eval`) her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölç. 300k'dan sonra yeni görev yok: işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, bu dosya, commit); kapanış 400k'dan önce biter. Bu beklenmedik durum değildir.
- **Tahmin:** `3 · O3b` ≈ 155k (35k + 20 × 6k). Kalibrasyon (`3 · O3a`): açılış 85k, keşif 149k, kesinti sonrası 111k, inceleme 187k, teyit 250k, kapanış öncesi 278k. Orkestratör uzun metni okumaz ve yazmaz: taslaklar scout'larda, yerine koyma `cp`, Index `edit` ile.
- **Hijyen:** 20 KB'tan büyük okuma scout'a; scout ≤ 4 KB döner, ayrıntıyı `local://`'a yazar. Büyük dosya `grep` ve dar `:N-M` ile okunur; aynı aralık iki kez okunmaz. Satırlar ≤ 600 bayt; `todo` ≤ 8 madde.
- **Beklenmedik durum** (plan §0 adım 6, liste orada): kapanış, commit ve bu dosyanın yeniden yazımı yok. Kullanıcıya sade dille: ne oldu, neden önemli, iki ya da üç seçenek ve önerin.

## 2. Okuma sırası

Plan (≈ 200 KB), PROJECT_LOG, ledger ve Index bütün okunmaz; bölüm başları `grep '^##'` ile.

1. Plan §0, §1 ve §3 (§2 gerekirse).
2. Plan §7.3 bütünüyle (`:665`–`:741`).
3. Plan §7.2'den dar aralıkla: "Görevler" (`SP4`, `SP5`, `CPb`), "Ara durumlar ve geçitler" (`:612`–`:624`), "Sıcak noktalar".
4. Kanıt: `W3F23`–`W3F25`, `W3F31`, `W3F32` (`grep '^| W3F'`), `W3P01`, `W3P02`, `W3P04`; Ek A.2 `E3`, `D6`, `REL`, `T3`; §10'un `Faz10.5`'i anan maddeleri (bayat yorumlar, `W3F27`, `.gitignore`).
5. Plan Ek A.7 ve PROJECT_LOG §2.6; Ek A.5 betiği yalnız geçitte ve kapanışta.
6. `Main-Planing.md:276-312`, 45 alt plan, Index'in bütünü ve ClaudeQB Step 2 belgeleri yalnız scout'larla okunur.

## 3. Mevcut durum

**Beklenen durum (3 · O3a kapanışından sonra):**
- **Git:** dal `integrate/impl-96`, ağaç temiz, 83 commit. Uç: `Window 3 O3a follow-up: scope the hand-off line-length gate`, altında kapanış (`git log --grep '^Window 3 O3a:'`). Etiket yok, 353 izlenen dosya.
- **`main` = `origin/main`** = `6632a18`. `origin/main..HEAD` = 7 (`3 · O0`–`3 · O3a` kapanışları ve iki takip commit'i); hiçbiri push edilmedi; FF ve push `3 · O5`'te, ayrı onaylarla.
- **`git ls-remote origin`:** `HEAD`, `main`, `integrate/impl-96` = `6632a18`.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez); silinecek üç depo (`DEC-30`): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. 2026-11-15T19:42:48Z–19:42:51Z'de dördü de 200; ajan yalnız ölçer (404 = silinmiş).
- **`Main-Planing.md`** (`3 · O2a`'dan beri değişmedi): 406 satır, 77.019 bayt, CRLF, NUL 0, 10 faz.
- **Plan:** 989 satır; `3 · O3a` §7.3'e `:718` notunu, §10'a `.gitignore` maddesini ekledi; boru tabanı `:174`, `:838`.
- **Ledger:** 653 satır, CRLF, NUL 0; Pencere 3'te dokunulmadı; çapalar Ek A.6 `LMAP`; koşu 21 yazımları `3 · O4`'te (`I3a`).
- **Alt planlar:** 45; ledger §4'te 34 `verified`, 3 `implemented` (`Faz4.6`, `Faz6.1`, `Faz8.1`), 3 `planned` (`Faz7.2`, `Faz7.3`, `Faz8.3`), 2 `superseded` (`Faz4.1`, `Faz4.7`); artı ledger satırsız üç Phase 10 dosyası.
- **Index Phase 10** (`CPa`): `:24` (10 faz), `:39` (tablo satırı), `:162`–`:168` (kalın paragraf ve üç madde), `:188` (öncelik maddesi 16), `:300`–`:302` (on klasör; Phase 10 = 3, toplam 45).
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` hâlâ v1.9 içeriğinde (`DEC-29`).
- **Telefon** (plan §7.1, PROJECT_LOG §2.3): HyperOS 4 (`OS4.0.0.44.WMACNXM`), SukiSU-Ultra v4.3.0-r1, metamodül yok; HAL AOSPA'dan farklı, sensör = `EXPECT_MD5`; proje modülleri ve kutucuk yok; AGC yamasız V9.6, 10 tuzak.

## 4. Bu oturum: `3 · O3b`

Yalnız `Planner-docs/Faz-10-Plans/`'e iki yeni dosya ve Index'in 10.4–10.5 girdileri yazılır (kapanış dosyaları (e)'de). Ledger, `Main-Planing.md`, `Faz10.1`–`Faz10.3`, Audit, Ontology, Comprehension ve `docs/` yazılmaz.

**(a) Açılış kontrolleri** (alt ajanlardan önce): `git status` (temiz); `git log --oneline -8`; `git branch -vv`; `git log -1 --format=%s` = `Window 3 O3a follow-up: scope the hand-off line-length gate`; `git rev-list --count HEAD` = 83; `git rev-list --count origin/main..HEAD` = 7; `main` ve `origin/main` = `6632a18`; `git tag` boş; `git ls-files` = 353; `git ls-remote origin` (§3). Plan §1'de ilk `pending` = `3 · O3b`.
Snapshot (plan §7.3): `Planner-docs/Main-Planing.md` sha256 `6790b6aed65fe6ae69eb6920e9187b4cc8484a0408838207c6c058f2117b7cc2`, 77.019 bayt, 406 satır, CRLF, NUL 0. Tutmayan her şey beklenmedik durumdur.

**(b) GitHub ölçümü:** dört depo için `gh api -i repos/ahmetxa/<ad>` (UTC; ilk satır HTTP durumu). 404 varsa PROJECT_LOG'un silme cümleleri güncellenir (yerler plan §7 "Açılışta ayrıca").

**(c) Bağlam ölçümü:** Ek A.7 betiği (`eval`), oturum başında ve her alt ajan sonucundan sonra (§1).

**(d) Step 2 taslakları:**
1. **Taban:** `step2 --strict` ve `step1 --strict` çıkış 0; `all` yalnız denetim uyarısı, `subplan_count=45`, çıkış 0 (§7). Başka her bulgu beklenmedik durumdur.
2. **Betik uzantısı** (küçük `task`): `draftcheck.py` sözlüğüne 10.4/10.5 adları ve H1'leri (§7.3 `:682`–`:683`); C11 (10.4 → `Faz10.1`; 10.5 → `Faz10.2`–`Faz10.4`); C6 istisnası: `Faz10.5`'in 10.2–10.4 dosyalarındaki sürüm eki satırları (yalnız sürüm dizesi ve bayat yorum, eklediğini adlandırır; `:693`, `:702`).
3. **`SP4` ∥ `SP5`:** iki geniş bağlamlı salt-okur scout aynı turda; `SP4` → `Faz10.4`, `SP5` → `Faz10.5` taslağını `local://`'a yazar, ≤ 4 KB döner (yol, bayt, bölüm başına bir satır, `open_issues`). Görev metni:
   - §7.3: o alt planın sözleşme ve kapsam satırları, tek sahip kuralı ve haritası (`:693`–`:707`), "Ortak bağlam" ve `:718` notu; `Main-Planing.md:276-312`; §2 madde 4'teki kanıt. Biçim örneği `Faz9.1` ve `Faz10.1`–`Faz10.3`: yalnız biçim, cümle değil.
   - Yeni kimlikler `VAL-10M-AD`, kullanıcı eylemi `VAL-104-MANUAL`/`VAL-105-MANUAL` (yalın `VAL-MANUAL` değil). Snapshot satırı dosya adıyla: `snapshots/YYYYMMDD-HHMM__Faz10.M__<ad>.txt` (`smoke.sh -o AD` → `snapshots/AD.txt`; `smoke.sh:9`, `:284`).
   - Cihaz güvenliği: kur → yeniden başlat → canlı dosyanın md5'i → eylem; eski sürüm kuruluyken Action, WebUI, `setmode.sh` yok; sürüm dışı derleme `build-release.py --out`/`--manifest` ile `"$TEMP"`'e (Git Bash `%TEMP%`'i açmaz); yazımdan önce yedek, sonra md5 ve uzunluk, tutmazsa geri yükle ve doğrula; yazmadan önce uygulamayı durdur; yönetici farklıysa komut listesi durur, sorar.
   - `SP4`: `Faz10.1` PRB10'u (kutucuk kaydı) ve metamodül/sistem uygulaması sorusunu `Faz10.4`'e bırakır.
   - `SP5`: sürüm eki istisnası; bayat yorumların hepsi `Faz10.5`'te. `W3F27` yolları ve `.gitignore` haritada yok: eklenmez, `open_issues`'a yazılır.
4. **Taslak betiği:** `py -3 "$TEMP"/ishtar-st3/draftcheck.py --root . <taslak>...`; son satır `DRAFTCHECK: PASS files=2`, çıkış 0 (1 bulgu, 2 kullanım); C1 (ad) – C12 (tekrar). Bulguyu taslağın scout'u düzeltir; orkestratör taslağı yeniden yazmaz.
5. **`CPb`:** iki taslak `cp` ile `Planner-docs/Faz-10-Plans/`'e (adlar §7.3). Index `edit` ile, sondan başa, satırlar önce içerikle doğrulanarak: `:301` Phase 10 = 5, toplam 47 (`find` ile sayılır); `:188` öncelik maddesi 16 10.4–10.5'i de anar; `:167`'den sonra 10.4 ve 10.5 maddeleri (V:158). `:163` değişmez.
6. **Geçit:** `step2 --strict` çıkış 0; `all` çıkış 0, `subplan_count=47`; bayt (LF, CR 0, NUL 0; orkestratörün satırları ≤ 600 bayt), boru (plan tabanı `:174`, `:838`), kimlik (§7).
7. **İnceleme (öneri):** plan `3 · O3b`'de inceleme öngörmez; `3 · O3a`'da eklenen salt-okur REV ∥ SEC 5 P1 buldu. Açılış formunda eklenmesini öner; P0/P1 → plan §0 adım 6.

**(e) Kapanış** (beklenmedik durum yoksa sorulmadan):
- Plan §1'de `3 · O3b` `done`, commit'i başlığıyla anar: `Window 3 O3b: Step 2 drafts 10.4-10.5 for planning run 21`. PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır, §11'e girdi eklenir; bu dosya `3 · O4` için ≤ 20 KB yeniden yazılır.
- Bayt, boru ve kimlik (§7); yerel commit sorulmadan; kullanıcıya `git show --stat` özeti ve yeni pencere çağrısı. Push yok.

**Kabul:** iki dosya `W3F07` biçiminde, §7.3 kapsamı ve tek sahip haritasıyla; betik PASS; Index girdileri yazılmış; (d6) geçidi geçti; ledger dokunulmamış; plan §1'de `3 · O3b` `done`.

## 5. Kullanıcı kararları

Kaynak: plan §2, §7, §7.2, §7.3, plan başlığındaki onaylar ve ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| K1 `Kullanim.txt` | (b): v2.3'te düzeltilir (soru 4) | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K5/K6 üç depo | Silinecek; kullanıcı siler; açılışta ölçülür | `DEC-30` |
| K7 HyperOS 4 yönü | (a) modülü uyarla; (i) "ClaudeQB Phase 10", Faz 7 ve 8 emekli (soru 5) | `DEC-32` |
| K9 50MP HAL | Hayır, şimdilik; sensör katmanı sürer (soru 1) | `DEC-33` (koşu 21) |
| Sekiz soru | Yanıtlandı (2026-11-15); soru 8: sınırlı Step 2, Step 1.5 atlandı | plan §7 |
| Pencere 3 planı | Onaylandı (2026-11-15, form "onay") | plan §7.2 |
| Step 1 metni | Onaylandı (2026-11-15T14:10Z, form "onay"; C01–C03 dahil) | `Main-Planing.md` |
| Step 2 kontratı | Onaylandı (2026-11-15, form "onay"; dal sürer) | plan §7.3 |
| `3 · O3a` planı | Onaylandı (2026-11-15, form "onay"); şablon uyarlandı: yeni dal ve kontrat commit'i yok, Index `edit`, REV ∥ SEC | plan §7.2 |
| `3 · O3a` incelemesi | Düzeltmeler "hepsi" (2026-11-16, form) | plan §7.3 `:718`, §10 |
| Snapshot | Step 2 durmaz; etkin plan bugünkü `Main-Planing.md`; satırlar `3 · O4`'te `I3a` | plan §7.3 |
| Atıf | Phase 10 ve emeklilikler koşu 21'in seçimi; `DEC-28` Faz 7/8'i, `DEC-32` uyarlamayı anar | ledger `:606`, `:610` |
| Dal | `integrate/impl-96` sürer; FF yalnız `3 · O5` | plan §7.2 |
| Alt planlar | `10.1` ölçüm, `10.2` sensör, `10.3` AGC tuzakları, `10.4` kutucuk ve WebUI, `10.5` v2.3 | plan §7.3 |
| Yayın | C2 ve takip commit'i push edildi; sonraki yedi commit yerel, push `3 · O5`'te | plan §1 |

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
11. Cihaza komut: yalnız salt-okur ve yalnız plan §7.2'de geçen komutlar (`PRB1`–`PRB10`); `3 · O3b` hiç göndermez. Fiziksel eylemler (kurulum, mod değiştirme, deklanşör, izin diyaloğu) kullanıcıda ve onaylı.
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

| Kontrol | Taban (`CPa`'dan sonra, 2026-11-16T07:39:46Z) |
|---|---|
| V1 `--mode all` | Yalnız denetim uyarısı (`step4_has_nonblocking_warnings=P2:1,P3:9`), `subplan_count=45`, `index_reference_count=45`, `phase_folder_count=10`; çıkış 0 |
| `step2`, `step1` `--strict` | Bulgu yok, çıkış 0 |
| `CPb`'den sonra (beklenen) | `step2 --strict` çıkış 0; `all` yalnız denetim uyarısı, `subplan_count=47`, çıkış 0 |
| V2 `--mode step4 --strict` | Yalnız bilinen `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9`; çıkış 1 (taban, regresyon değil) |
| V3 `--self-test` | `SELF-TEST: PASS`; sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0` |
| Kimlik taraması (Ek A.5) | Kapanış commit'inden önce: `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0`, `prose_mentions=18` → PASS; `prose_mentions` artabilir |

- V1–V3'ün yeni tabanı `3 · O4`'te yazılır (`subplan_count=47`).
- Kimlik taraması: Ek A.5 betiği (`%TEMP%/idscan.py`) depo kökünde `py -3` ile; değer basmaz.
- Bayraksız `build-release.py` `dist/` zip'ini ve manifest'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- `python` Store stub'ıdır; `SKILL.md`'deki `python3` burada çalışmaz.
- **omp:** Ek A.7 betiği JS'tir (`eval`). `bash` aracının politikası komutta `cat`, `head`, `tail`, `grep`'i engeller: `awk`, `read`/`grep` araçları ya da `py -3`; `<(…)` çalışmaz.
- **Betikler** (`%TEMP%`, depo dışı): `ishtar-st1/lines.py` (yalnız check); `ishtar-st2/scan.py` doğrulayıcıyı `importlib` ile yükler; `ishtar-st3/draftcheck.py` 10.4–10.5'i uzantıdan (§4 d2) önce tanımaz.
- **Tekrar kuralı:** taslak §7.3'ün, `Main-Planing.md`'nin ya da bir alt planın (`Faz10.1`–`Faz10.3` dahil) 80+ karakterlik cümlesini kopyalamaz, çevirmez; ortak cümleler her taslakta kendi sözleriyle.
- **Snapshot:** sha256 dosya baytlarından (`hashlib`, CRLF dahil); tutmazsa beklenmedik durumdur, taslak yazılmaz.
- **Tek sahip:** taslak yalnız kendi sahip satırının yollarını `proposed`, `modified`, `generated` yazar, ötekileri `existing` (istisna `Faz10.5`'in sürüm eki); haritada olmayan yol `open_issues`'a, kararı `CPb`'de orkestratör verir.
- **`snapshots/`:** yalnız eklemeli; satır dosya adıyla (§4 d3; `Faz3.7:71`), State `generated`; var olan dosya değişmez.
- **Alt ajanlar:** scout'un kabuğu yok, `local://`'a yazar; `task` 100K bağlamlı: plan ya da PROJECT_LOG bütün verilmez. İçerik filtresi (`reasoning_extraction`) reddederse görev kısa ve somut.
- **Hız sınırı:** alt ajan 429 ya da 402 (yedek model kredisiz) ile durabilir; park edilen ajan canlanmaz: görevi ortak bağlamın tamamıyla taze gönder (`3 · O3a`: `SP1R`–`SP3R`).
- **`local://`:** bir scout'un ilk yazımı bir kez yalnız niyet dizesini sakladı: bayt sayısına bak. Taşınmaz (`3 · O3a` özetleri yok); kararlar kapanıştan önce plana ya da depoya.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok; depoları kullanıcı siler, `DEC-30`).
- **`--grep` satır başına bağlanır** (`'^Window 3 O3a:'`) ve gövde satırlarını da eşler: gövdede başka aşamanın başlığıyla başlayan satır olmaz.
- **Commit:** `eval`'deki `commit` ad alanıyla (`d = await commit.draft()`, `await d.take(...)`, `await d.commit(...)`); `git add`/`git commit` yok. `cp` ya da betikle değişen dosyaları açıkça `take` et.
- **Satır numaraları kayar:** §7.3'tekiler `Window 3 O2a` ağacına aittir, Index `CPa`'da kaydı (§3); ledger'da `LSH`, `LMAP`; hepsi içerikle doğrulanır.
- **Tablolar:** hücrede `|` yok; ledger §4 satırı 10, §8 satırı 7 boru.
- **Ontology**'de 2 NUL: `grep` boş dönebilir (`AUDIT-FIX-22`); dosya bayt korumalı.
- **"Faz 10":** `50MP-Entegrasyon-Plani.md`'deki numaralama ayrıdır; yeni faz "ClaudeQB Phase 10", klasör `Faz-10-Plans`, yol haritası satırı tam `| 10 |` (V:163). 10.4 ve 10.5 aynı `CPb`'de girer: numara boşluğu olmaz (V:1040-1043).
- **Emekli Faz 7/8:** satırları, bölümleri ve dosyaları yerinde kalır (silmek `--strict`'te `extra_phase_folder_without_main_phase`).
- Doğrulayıcı tuzakları: plan §7 ve §7.2 "Ara durumlar ve geçitler"; kapsam dışı bulgular plan §10.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri ve snapshot (§4 a); plan §1'de ilk `pending` `3 · O3b`. Tutmayan her şey beklenmedik durumdur.
3. GitHub (§4 b), bağlam (§4 c) ve doğrulayıcı tabanı (§4 d1).
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin, bu oturumun yalnız `3 · O3b` olduğu.
5. §4 (d): betik uzantısı, `SP4` ∥ `SP5`, taslak betiği, `CPb`, geçit. Ardından §4 (e).

---
