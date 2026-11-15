# NEXT_PROMPT — ishtar (yeni oturum için)

> **Kullanım notu:** Yeni pencereyi depo kökünde (`C:\Users\ahmet\Documents\Projeler\ishtar`) aç, omp'u buradan başlat, iki `---` çizgisi arasını ilk mesaj olarak yapıştır.
> 2026-11-15'te, Pencere 2'nin takip commit'inde yazıldı (bağlam bütçesi). Aşama: **Pencere 3 · O0 — planlama koşusu 21'in keşfi**. Bu bir özettir; nihai kaynak `ORCHESTRATION_PLAN.md` (plan), `Planner-docs/Planing-Ledger.md` (kanonik kayıt) ve `PROJECT_LOG.md`'dir.

---

## 0. Rol ve ilk kurallar

Orkestratör olarak devam ediyorsun. `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2), `ishtar-aon-fix` (v1.1) ve AGC (`org.codeaurora.snapcam`) yapılandırması; hepsi AOSPA Android 15'te kuruldu ve ölçüldü. 2026-11-13'te ROM derleme bırakıldı (`DEC-28`): telefon HyperOS 4'te, kamera HAL'i farklı, proje modülleri kurulu değil. Amacı kalmayan Faz 7/8'i planlama koşusu 21 emekli eder.

1. **Tek aşama:** plan §1'deki ilk `pending` aşama satırı `3 · O0`'dır: yalnız keşif. `3 · O1` (plan ve onay) sonraki oturumdur. Aşama atlanmaz; oturum kendiliğinden sıradakine geçmez.
2. **Dosya kazanır:** bu dosya planla çelişirse plan geçerlidir; çelişki kullanıcıya söylenir.
3. **Cihaz:** bu oturum cihaza komut göndermez; cihaz olguları 2026-11-13 ölçümüdür.
4. **Onay kapıları** (plan §0 adım 5): `O1` plan onayı, `main`'in fast-forward'ı (FF), her push, cihaz eylemi, AGC tercihlerine yazma. Kapanış ve yerel commit, beklenmedik durum yoksa sorulmadan yapılır.

Kullanıcıyla Türkçe, kısa ve sade konuş. Plan, PROJECT_LOG ve bu dosya Türkçe; plan Ek A, `Planner-docs/` ve `docs/` İngilizce. Ajanlar: `scout`, `task`, `reviewer`, `security-reviewer`, `sonic` (`librarian`, `designer`, `isolated`, `outputSchema` yok). Dal ve görev kimlikleri `3 · O1` planında belirlenir.

## 1. Döngü ve bağlam bütçesi

- **Aşamalar** (plan §0): `O0` keşif, `O1` plan, `O2` kontrat, `O3` uygulama, `O4` entegrasyon ve geçitler, `O5` inceleme ve kapanış. Pencere 3 ve 4'te `O0` ve `O1` ayrı oturumlardır (küçük Step 4 dilimlerinde birleşebilir, plan §9); varsayılan düzen plan §7, "Oturum düzeni ve bütçe".
- **Eşik 400k** (plan Onay 3, §0 adım 9). Bağlamı Ek A.7'deki JS betiğiyle (`eval`) ölç: her alt ajan sonucundan sonra ve en geç her beş turda; 250k'dan sonra her turda. 300k'dan sonra yeni görev yok: elindeki işi doğrula, adım 7 ile kapan (`in_progress`, kalan iş, devam için bu dosya, commit); kapanış 400k'dan önce biter. Bu beklenmedik durum değildir.
- **Tahmin:** hedef 240k ≈ 30–34 yürütme turu ya da 15–20 yazım turu; `3 · O0` ≈ 185k (açılış ≈ 35k + 25 tur × 6k), yani ≈ 25 tur.
- **Hijyen:** 20 KB'tan büyük okuma scout'a; scout ≤ 4 KB döner, ayrıntıyı `local://`'a yazar. Büyük dosya `grep` ve dar `:N-M` ile okunur, aynı aralık iki kez okunmaz. Taslak `cp` ile yerine konur, betikle doğrulanır, yeniden yazılmaz. Satırlar ≤ 600 bayt; `todo` ≤ 8 madde.
- **Beklenmedik durum** (plan §0 adım 6, liste orada): kapanış, commit ve bu dosyanın yeniden yazımı yok. Kullanıcıya sade dille: ne oldu, neden önemli, iki ya da üç seçenek ve önerin.

## 2. Okuma sırası

Boyutlar yaklaşıktır. Plan ≈ 143 KB, `PROJECT_LOG.md` ≈ 173 KB, ledger ≈ 628 KB: hiçbiri bütün okunmaz; bölüm başları `grep '^##'` ile bulunur.

1. Plan §0 (≈ 10 KB), §1 (≈ 11 KB), §3 (≈ 7 KB).
2. Plan §7, başından "Oturum düzeni ve bütçe" bloğunun sonuna kadar (≈ 9 KB): sekiz soru, "Açılışta ayrıca", oturum tablosu, scout'lar.
3. Plan Ek A.7 (≈ 2,5 KB) ve PROJECT_LOG §2.6 (≈ 5 KB).
4. Plan §7'nin kalanı (≈ 11 KB: Step 1, Ledger, Index, Ontology, Step 2, aday alt planlar, geçitler, doğrulayıcı tuzakları, ClaudeQB süreci): yalnız scout görev metinleri için, `grep` ve dar aralıklarla.
5. Plan Ek A.5 betiği (≈ 3 KB): yalnız push'tan önce ve kapanışta.
6. Bütün okunmaz, gerekirse aranır: PROJECT_LOG §11 (≈ 45 KB), plan §6 (≈ 50 KB), §10 (≈ 14 KB), Ek A.2 (≈ 15 KB), A.6 (≈ 20 KB).
7. ClaudeQB dosyalarını ve doğrulayıcıyı S1, `Planner-docs/`'u S2 ve S3 okur (§4 d).

## 3. Mevcut durum

- **Git (2026-11-15):** dal `integrate/impl-96`, ağaç temiz, etiket yok, 350 izlenen dosya. C2 `Window 2: project log sweep and handoff for planning run 21` (75. commit): `main` C2'ye ileri sarıldı (08:14:45Z), kimlik kontrolü geçti, push 08:15:01Z; `origin`'de `HEAD`, `main` ve `integrate/impl-96` = C2.
- **Takip commit'i** `Window 2 follow-up: context budget and stage sizing` C2'nin üstünde. Açılışta iki durum da beklenendir:
  - (a) yalnız yerelde: dal 76, `main` = C2 (75), iki uzak ref = C2, `origin/main..HEAD` = 1; FF ve push açılışta sorulur (§4 b);
  - (b) push edildi: `main`, dal ve iki uzak ref = takip commit'i (76), `origin/main..HEAD` = 0.
  - Başka her durum beklenmedik. Commit'ler başlıkla bulunur: `--grep '^Window 2:'`, `--grep '^Window 2 follow-up:'`.
- **GitHub:** `origin` özel `ahmetxa/ishtar_cam_modes` (silinmez). Silinecek üç depo (`DEC-30`): `ahmetxa/ishtar` (özel), `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar` (açık); 2026-11-14T21:11:12Z'de üçü de 200. Silmeyi kullanıcı yapar; ajan yalnız ölçer (404 = silinmiş). Aynalar `../ishtar-arsiv/`'de.
- **Ledger:** 653 satır, CRLF, NUL 0; Pencere 2 yazmadı. Çapalar (Ek A.6 `LMAP`): `Faz6.2` `:98`, `Faz7.2` `:100`, `Faz7.3` `:101`, `Faz8.1` `:102`, `Faz8.3` `:104`, `DEC-27`…`DEC-32` `:605`–`:610`.
- **Alt planlar:** 42; ledger §4'te 34 `verified`, 3 `implemented` (`Faz4.6`, `Faz6.1`, `Faz8.1`), 3 `planned` (`Faz7.2`, `Faz7.3`, `Faz8.3`), 2 `superseded` (`Faz4.1`, `Faz4.7`).
- **11. denetim** (2026-09-14, `PASS_WITH_WARNINGS`): 35 COMPLETE, 4 kuyrukta (`Faz7.2` → `7.3` → `8.1`'in uyum yarısı → `8.3`), 2 SUPERSEDED, 1 DEFERRED (`Faz4.6`); kuyruk 2026-11-13'ten beri geçersiz (`DEC-28`).
- **Sıradaki numaralar:** koşu 21 (bu pencere), 12. denetim (Pencere 4), `IMPL-97` (Pencere 5+), `DEC-33`.
- **Sürüm:** v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba`; `Kullanim.txt` hâlâ v1.9 içeriğinde (K1).
- **Telefon** (2026-11-13 ölçümü, bu oturumda teyit edilmez; ayrıntı Ek A.2 `D1`–`D11`, `M1`, `TRAP` ve PROJECT_LOG §2.3):
  - HyperOS `OS4.0.0.44.WMACNXM`, Android 17; kernel 5.15.215, SELinux Enforcing; KernelSU `4.3.0-r1`.
  - HAL md5 `2a955e68…` (AOSPA stoku `c3fa63a8…` değil); IMX989 sensör dosyası md5 `9e4d0fe1…` = `EXPECT_MD5`.
  - Proje modülleri ve kutucuk uygulaması yok; `com.rifsxd.ksunext` yok. AGC yamasız V9.6, `prefs.trap.armed = 10` (değer 37), `agc.pref_48m` yok.
  - [ÇIKARIM] (M1): sensör koruması geçer, HAL koruması kapalı başarısız olur; `setmode.sh` AOSPA servis adlarını kullanır.

## 4. Bu oturum: `3 · O0`

Kaynak: plan §1 (`3 · O0` satırı), §7 ve §0. Depoda yalnız plan, `PROJECT_LOG.md` ve bu dosya değişir; ledger, `Planner-docs/` ve `docs/` dokunulmaz. Alt ajanlar salt-okurdur.

**(a) Açılış ölçümleri** (alt ajanlardan önce): `git status`, `git log --oneline -8`, `git branch -vv`; dal, `main`, `origin/main` commit sayıları ve `origin/main..HEAD`; `git tag`; `git ls-files` sayısı; `git ls-remote origin`; dört depo için `gh api -i repos/ahmetxa/<ad>` (üç silinecek depo ve `ishtar_cam_modes`), UTC zamanıyla. Sonuç keşif envanterinin ilk satırıdır: `W3OPN` (Ek A.6 `O5OPN` içeriğinde; commit'ler başlıkla).

**(b) "Açılışta ayrıca"** (plan §7): C2'nin ve takip commit'inin tam hash'ini (`--format=%H`) `ls-remote` ve yerel `main` ile karşılaştır; (a) ya da (b)'yi kaydet.
- (a) ise FF ve push'u açılışta ayrı evet/hayır sorularıyla sor (plan §0 adım 5): FF yalnız `git fetch . integrate/impl-96:main`; push'tan önce Ek A.5 kimlik taraması; push yalnız `git push origin main integrate/impl-96`; ardından `git ls-remote origin` ile karşılaştır.
- PROJECT_LOG'un push cümlelerini son duruma göre güncelle; bir depo 404 verirse silme cümlelerini de. Yerler plan §7'de, `2 · O3` kapanışının numaralarıyla: alıntıyla bul, numara tahmin etme.

**(c) Sekiz soru**: scout'lardan önce, ilk mesajın sonunda. Sade dille, kısa seçeneklerle sor; teknik ayrıntı plan §7'de. Yanıtları tarihle plan §7'de sorunun altına yaz; K9'unkini plan §2'deki K9 satırına da (karar sonraki DEC, `DEC-33`; ledger'a koşu 21 yazar).
1. **K9:** 50 MP için yeni kamera sürücüsü (HAL `2a955e68…`) yeniden incelensin mi? Evet: uzun statik analiz (R10 bağlam riski). Hayır: HAL katmanı kapalı kalır, sensör katmanı sürer.
2. **Kutucuk ve WebUI:** uzun basış bu ROM'da olmayan `com.rifsxd.ksunext`'e bağlı. Uyarlansın mı, kaldırılsın mı? Önce KernelSU `4.3.0-r1`'in yöneticisi ve WebUI desteği salt-okur ölçülür (zamanı `3 · O1`'de).
3. **AGC tuzakları:** 10 tuzak kurulu; tek temizleme yolu (`docs/phase3-preconditions.md:71-119`) AOSPA'ya özel ve yedeksiz. Yedekli yeni bir prosedür kapsama girsin mi?
4. **v2.3 kapsamı:** `Kullanim.txt`, modüldeki eski yorumlar, kutucuk uygulamasının `versionName`'i: hangileri?
5. **Yeni iş nereye (K7 = (a)):** (i) yeni faz, "ClaudeQB Phase 10"; Faz 7 ve 8 tümüyle emekli. (ii) Faz 8'in kamera yarısı; Faz 8 kısmen emekli, başlığı ve yol haritası satırı yeniden yazılır.
6. **`Faz6.2`'nin VAL-BUILD bağı** (ledger `:98`, Index `:177`): Faz 7 emekli olunca düşsün mü, yeni bir alt plana mı taşınsın?
7. **Hetzner satırları** (`AUDIT-FIX-57`; Comprehension `CQ-13`, `EV-20`; `docs/reverse-engineering-toolchain.md:220`): koşu 21'de orkestratör mü düzeltsin, plan §10 yoluyla 12. denetim mi?
8. **Oturum düzeni:** Step 1 ve Step 2 ayrı oturumlarda, Step 2 yalnız yeni alt planlarla sınırlı (emsaller plan §7): onaylanıyor mu? Step 1.5 (Autopsy) atlansın mı (çalışırsa ayrı oturum)?

**(d) Keşif:** üç `scout` paralel (plan §7); her biri ≤ 4 KB döner, ayrıntıyı `local://`'a yazar; kabukları yok.
- S1: ClaudeQB yönergeleri (`SKILL.md`; `references/` altında `First-`, `Autopsy-` ve `Second-Planner.md`, `workflow-quality.md`, `handoffs/run-step2.md`) ve doğrulayıcı kipleri; kök `C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/`.
- S2: Step 1 yüzeyleri: `Main-Planing.md` (≈ 52 KB, CRLF); Audit'teki `AUDIT-FIX-41`, `-42`, `-57` (≈ 57 KB); Comprehension (≈ 55 KB) ve Ontology (≈ 84 KB, 2 NUL) yerleri.
- S3: ledger (yalnız `:raw:N-N`) ve Index (≈ 84 KB) çapaları; aday alt planlar için mevcut kanıt.
- Görev metni kendi kendine yeter: dosyalar, yanıtlarla daralan kapsam, yasaklar, dönüş bloğu (plan §3).
- Envanter (≤ 15 KB, Türkçe, ilk satır `W3OPN`) plan §7'ye yazılır: `3 · O1`'in ve sonraki aşamaların ihtiyaç duyacağı olgular, kaynak ve tarihle (Pencere 2'nin §6.2 biçimi). `local://` oturumlar arası taşınmaz.

**(e) Kapanış** (plan §0 adım 4; beklenmedik durum yoksa sorulmadan):
- Plan §1'de `3 · O0` satırı `done`, kapanış commit'ini başlığıyla anar; öneri `Window 3 O0: discovery for planning run 21`.
- PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazılır; §11'e girdi eklenir.
- Bu dosya `3 · O1` için ≤ 20 KB olarak yeniden yazılır.
- Değişen dosyalarda bayt ve boru kontrolü (LF, CR 0, NUL 0, tablo boruları) ve kimlik taraması (§7); yerel commit onay sorulmadan; kullanıcıya `git show --stat` özeti ve yeni pencere çağrısı.
- Kapanış commit'i push edilmez: FF ve push `3 · O5`'te, onayla.

**Kabul:** `W3OPN` ve envanter plan §7'de; sekiz yanıt tarihle planda; PROJECT_LOG'un push (ve gerekirse silme) cümleleri güncel; plan §1'de `3 · O0` `done`; ledger, `Planner-docs/` ve `docs/` dokunulmamış.

## 5. Kullanıcı kararları

Kaynak: plan §2, plan başlığındaki onaylar ve ledger §8.

| Karar | Durum | Kayıt |
|---|---|---|
| Depo taşıma | `origin` = özel `ahmetxa/ishtar_cam_modes` | `DEC-27` |
| K1 `Kullanim.txt` | (b): sonraki sürümde düzeltilir | `DEC-29` |
| K2 ROM derleme | Bırakıldı; HyperOS 4 | `DEC-28` |
| K3, K4 | Kernel iddiası düştü; temizlik uygulandı | IMPL-96 satırı |
| K5/K6 üç depo | Silinecek; kullanıcı siler; açılışta ölçülür | `DEC-30` (yürütme notu koşu 21'de) |
| K7 HyperOS 4 yönü | (a) modülü uyarla; (i)/(ii) açık (soru 5) | `DEC-32` |
| K8 cihaz kimlikleri | A, yürütüldü; redaksiyonsuz özgün yalnız `../ishtar-arsiv/` bundle'ında (Ek A.2 `G10`) | `DEC-31` |
| K9 50MP HAL | Açık (soru 1) | sonraki DEC (`DEC-33`) |
| `DEC-07`, `-08`, `-22`, `-24`…`-26` | Konusuz; `DEC-09` koşullu | `DEC-28` |
| Döngü | Aşama başına oturum; kapanış sorulmadan; FF ve push ayrı onay | plan Onay 2, §0 |
| Bağlam eşiği | 400k; hedef 240k | plan Onay 3, §0 adım 9 |
| Yayın | C2 için FF ve push 2026-11-15'te yapıldı; takip commit'i push edilmemişse açılışta sorulur | plan §1, §0 adım 5 |
| Pencere 3 planı | Açık; `3 · O1`'de "onay" | plan §1, §7 |

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
11. Cihaza komut: bu oturumda yok. Fiziksel eylemler kullanıcıda ve onaylı.
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
| Kimlik taraması (Ek A.5) | `value_lines=6`, `NOT_REDACTED=0`, `LUHN15=0` → PASS; `prose_mentions=16` (artış hata değil) |

- `3 · O0` `Planner-docs/`'a dokunmaz; geçitlerin aşamasını `3 · O1` planı belirler. Çalıştırılırsa sapma beklenmedik durumdur.
- Kimlik taraması (push'tan önce ve kapanışta): Ek A.5 betiğini `write` ile `%TEMP%` altına yaz, depo kökünde `py -3 <yol>` ile çalıştır; değer basmaz.
- Koşu 21 kipleri (plan §7): `step1` ve (Step 1.5 çalışırsa) `autopsy` Step 1'den sonra, `step2` ve `step3-preflight` Step 2'den sonra; hepsi `--strict`.
- Bayraksız `build-release.py` `dist/` zip'ini ve manifest'i yeniden yazar: çalıştırma.

## 8. Bilinen tuzaklar

- `python` Store stub'ıdır; `SKILL.md`'deki `python3` burada çalışmaz.
- **omp:** `eval` yalnız JS (Ek A.7 betiği JS). `bash` komut içindeki `grep`, `tail`, `cat`'i ve heredoc ile dosya yazmayı engelleyebilir: `grep`/`read` araçlarını ya da `%TEMP%`'teki `py -3` betiğini kullan; `<(…)` çalışmaz.
- **Alt ajanlar:** scout'ların kabuğu yok; `task` ajanları 100K bağlamlı: plan ya da PROJECT_LOG bütün verilmez.
- **`gh`** PATH'te yok: `C:/Users/ahmet/AppData/Local/Microsoft/WinGet/Packages/GitHub.cli_Microsoft.Winget.Source_8wekyb3d8bbwe/bin/gh.exe` (`delete_repo` kapsamı yok); `gh api -i`'nin ilk satırı HTTP durumudur.
- **Depo silme (kullanıcı, `DEC-30`):** GitHub'da Settings → General → Danger Zone → Delete this repository; ya da kullanıcı kendi terminalinde `gh auth refresh -h github.com -s delete_repo` ve `gh repo delete ahmetxa/<ad> --yes`. Ajan silmez, yalnız ölçer (404 = silinmiş).
- **`--grep` satır başına bağlanır** (`'^Window 2:'`); `^` gövde satırlarını da eşler: commit gövdesinde başka bir aşamanın başlığıyla başlayan satır olmaz.
- **`local://` taşınmaz:** yanıtlar, `W3OPN` ve envanter kapanıştan önce plana yazılır.
- **Satır numaraları kayar:** plan §7'deki PROJECT_LOG numaraları `2 · O3` kapanışına göredir; ledger'da `LSH` ve `LMAP`; `Planner-docs/` numaraları da içerikle doğrulanır.
- **Tablolar:** hücrede `|` yok; ledger §4 satırı 10, §8 satırı 7 boru.
- **Ledger** satırları 1–9 KB: yalnız `:raw:N-M`.
- **Ontology**'de 2 NUL: `grep` sessizce boş dönebilir (`AUDIT-FIX-22`); dosya bayt korumalı.
- **"Faz 10":** `50MP-Entegrasyon-Plani.md`'deki ayrı numaralama; yeni faz "ClaudeQB Phase 10", klasör `Faz-10-Plans`.
- **`.gitignore`'da `*.so` kuralı yok:** K9 = evet ise HAL kopyalanmadan önce kural önerilir.
- Doğrulayıcı tuzakları: plan §7 "Doğrulayıcı tuzakları"; kapsam dışı bulgular plan §10.

## 9. İlk mesajda ne yapmalı

1. §2'deki bölümleri oku.
2. Açılış kontrolleri (§4 a): ağaç temiz; dal `integrate/impl-96`; `git log -1 --format=%s` = takip commit'inin başlığı; plan §1'de ilk `pending` aşama `3 · O0`; git §3'teki (a) ya da (b). Tutmayan her şey beklenmedik durumdur.
3. `W3OPN`'i plan §7'ye yaz, push durumunu kaydet (§4 b); bağlamı ölç.
4. Kısa Türkçe "hazırım" özeti: ölçtüklerin, yalnız dosyadan bildiklerin (cihaz olguları 2026-11-13), bu oturumun yalnız `3 · O0` olduğu.
5. Aynı mesajın sonunda, durum (a) ise önce FF ve push'u (ayrı onaylar), sonra sekiz soruyu sor ve bekle. Sonra §4 (b)–(e); `3 · O1`'e geçme.

---
