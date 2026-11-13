# ORCHESTRATION_PLAN — ishtar

> **Onay:** kullanıcı, 2026-11-13 ("onay"). Kararlar: K8 = A, konusuz kapsamı = altı karar, K7 = (a).
> **Kural:** Her yeni sohbet penceresi bu plandan **tek bir fazı** yürütür. Giriş noktası `NEXT_PROMPT.md`; ayrıntı, sözleşme ve durum bu dosyadadır.
> **Öncelik:** Ölçüm ve kanonik dosyalar (ledger, `Planner-docs/`) bu plandan üstündür. Çelişki bulunursa §10'a yazılır ve kullanıcıya söylenir; plan sessizce uydurulmaz.

## 0. Pencere protokolü

1. **Açılış:** `NEXT_PROMPT.md`'yi oku; `git status`, `git log --oneline -6`, `git branch -vv`. Bu dosyada §1'deki ilk `pending` fazı ve o fazın bölümünü oku. Önkoşul (önceki faz `done`, gerekli kullanıcı kararları) tutmuyorsa başlamadan kullanıcıya söyle.
2. **Yürütme:** Yalnız o fazın görev tablosu. Orkestratör planlar, dağıtır, entegre eder, doğrular; alt ajan kuralları §3'te.
3. **Doğrulama:** Fazın kabul kriterleri ve §3'teki geçitler. Kırmızı bir ağaçla kapanış yapılmaz.
4. **Kapanış:** Pencerenin bütün dosyaları **tek kapanış commit'inde** gider: işin kendisi, bu dosyanın §1 satırı (`done` ve kanıt), `PROJECT_LOG.md` §11 girdisi (gerekirse §2, §3.2, §4) ve sıradaki faza göre yeniden yazılan `NEXT_PROMPT.md`. Bir commit kendi hash'ini taşıyamaz: §1'e commit **başlığı** yazılır, hash `git log --grep '<başlık>'` ile bulunur (C0 için `git log --diff-filter=A -- ORCHESTRATION_PLAN.md`). Diff kullanıcıya gösterilir, onayla commit edilir, yeni pencere önerilir.
5. **Faz bir pencereye sığmazsa:** doğrulanmış bir noktada dur; §1'e `in_progress` ve kalan işi yaz; NEXT_PROMPT'u güncelle; onayla commit et.
6. `local://` taslakları pencereler arasında **taşınmaz**. Bir taslak ya aynı pencerede tüketilir ya da depodaki bir dosyaya yazılır.

## 1. Durum tablosu

Durum sözlüğü: `pending`, `in_progress`, `done`, `blocked`.

| Pencere | Faz | Kapsam | Önkoşul | Durum | Commit / kanıt |
|---|---|---|---|---|---|
| 0 | Keşif, plan, sözleşme | O0 keşif, O1 plan (onaylandı), K8 = A (dal yeniden kuruldu), bu dosya, NEXT_PROMPT ve PROJECT_LOG güncellemesi | — | done | `70946ff`, `03b0898`, `775b321`; C0 `Window 0: orchestration plan, K8 redaction, handoff for window 1` (`git log --diff-filter=A -- ORCHESTRATION_PLAN.md`) |
| 1 | IMPL-96 uygulaması | Ledger IMPL-96 (§4–§8, `DEC-27`…`DEC-32`); README ve UNTRACKED kaymaları (T2); iki `-o` satırı (T3); inceleme; C1 | Pencere 0 | pending | |
| 2 | Kapanış ve yayın | PROJECT_LOG bayat satırları (W5); NEXT_PROMPT'u koşu 21'e hazırlama (W6); push öncesi güvenlik incelemesi; `main` FF; push; silinecek depoların ölçümü | Pencere 1; push kararı | pending | |
| 3 | Planlama koşusu 21 | Step 1 + Step 2: Faz 7/8 emekli; K7 = (a) için faz ve alt planlar; önce K9 ve kapsam soruları | Pencere 2 | pending | |
| 4 | 12. denetim | Step 3 (`run-step3.md`) | Pencere 3 | pending | |
| 5+ | K7 = (a) Step 4 dilimleri | 12. denetimin kuyruğu; pencere başına bir dilim | Pencere 4 | pending | |

## 2. Kararlar (2026-11-13)

| Kimlik | Konu | Karar | Ledger kaydı (Pencere 1) |
|---|---|---|---|
| Depo taşıma | `origin` | Özel `ahmetxa/ishtar_cam_modes`; 62 commit aynı hash'lerle | `DEC-27` |
| K2 | ROM derleme | Bırakıldı. Telefon HyperOS 4'te; 2026-11-13'te gözlendi (ROM 2026-09-23 derlemesi) | `DEC-28` |
| Konusuz | `DEC-28` ile | `DEC-07`, `DEC-08`, `DEC-22`, `DEC-24`, `DEC-25`, `DEC-26` | §8 notları |
| K1 | `Kullanim.txt` | (b) Bir sonraki sürümde düzeltilir | `DEC-29` |
| K5, K6 | Üç ROM deposu | Silinecek; silmeyi kullanıcı yapar. 2026-11-13 ölçümünde üçü de duruyor | `DEC-30` |
| K8 | Probe snapshot'ındaki cihaz kimlikleri | A: push'tan önce redaksiyon; push edilmemiş üç commit yeniden kuruldu. Geçmişi yeniden yazmama kuralına (`NEXT_PROMPT.md` §6 madde 16) kayıtlı, tek seferlik istisna | `DEC-31` |
| K7 | Projenin HyperOS 4'teki yönü | (a) Modülü HyperOS 4'e uyarla | `DEC-32` |
| K3 | Kernel iddiası | Düştü; `docs/rom-build-device-notes.md:79-84`'teki açık girdi kapanır | IMPL-96 satırı |
| K4 | Temizlik | Uygulandı (beş öğe, Ek A `K4`) | IMPL-96 satırı |
| K9 | 50MP HAL katmanının HyperOS 4 HAL'inde (`2a955e68…`) yeniden türetilmesi | **Açık.** Pencere 3'ün başında sorulur | sonraki DEC |
| Push | `main` ve `integrate/impl-96` | **Açık.** Pencere 2'de sorulur | — |

## 3. Her pencerede geçerli kurallar

**Roller.**
- **Orkestratör (ana oturum):** plan, dağıtım, entegrasyon, doğrulama ve commit. Sıcak noktalar yalnız onundur: `Planner-docs/Planing-Ledger.md`, `Main-Planing.md`, `Sub-Planing-Index.md`, `Sub-Planing-Audit.md`, `Project-Ontology.md`; `CHANGELOG.md`; sürüm yerleri (`ishtar-cam-modes/module.prop`, `customize.sh`); üretilen `docs/release-manifest.md`; `.gitignore`, `.gitattributes`; `snapshots/` (kanıt, düzeltilmez); bu dosya; tüm git işlemleri.
- **Alt ajanlar:** Görev metni kendi kendine yeter (hedef dosya yolları, değişiklik, kabul kriteri, yasak alanlar). Ajan yalnız sahip olduğu dosyaya yazar; başka bir dosyada sorun görürse düzeltmez, raporlar. Doğrulayıcı, test ya da format çalıştırmaz. Dönüşte şu blok zorunludur: `status`, `changed_files`, `acceptance` (kriter / karşılandı mı / kanıt), `contract_deviations`, `open_issues`. Sıcak noktalar için yalnız taslak üretir (`local://…`).
- Aynı anda en fazla 4 uygulama ajanı çalışır. `task` aracında `isolated` ve `outputSchema` yok; yalıtım ayrık dosya sahipliğiyle sağlanır. `librarian` ve `designer` ajanları bu ortamda yok.

**Geçitler** (faz sonunda bir kez, orkestratör):
- `py -3 C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py --root . --mode all` → `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`. Koşu 21 alt plan sayısını, 12. denetim de bulgu sayılarını değiştirir; yeni baseline o fazda yazılır.
- Aynı komut `--mode step4 --strict` ile: yalnız bilinen `strict_warning` hatası (baseline, regresyon değil).
- `py -3 scripts/build-release.py --self-test` → `SELF-TEST: PASS`, VAL-BUILD2 sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0`. Bayraksız çalıştırma `dist/` zip'ini ve `docs/release-manifest.md`'yi yeniden yazar; sürüm prosedürü dışında çalıştırılmaz.
- Dokunulan dosyalarda bayt kontrolü (CRLF/LF sayısı, NUL) ve tablo boru sayıları; `git diff --stat` ile sahiplik kontrolü.

**Bayt kuralları.** Ledger, `Main-Planing.md` ve `Autopsy.md` CRLF; diğer her şey LF. Satır sonu dönüştürme yapılmaz. `Project-Ontology.md`'de 2 NUL bayt var; grep orada sessizce sonuç vermeyebilir. CRLF bir dosyada ilk `edit`ten sonra bayt sayımıyla CRLF'nin korunduğu doğrulanır; korunmuyorsa durulur. Ledger satırları 1–9 KB'tır (en büyüğü ≈ 8,8 KB): değişen satır baştan sona yeniden yazılır, uygulamadan sonra her değişen satır için difflib ile "yalnız ekleme" kontrolü yapılır (kopyalama hatasını yakalar). Bilinen tek istisna, IMPL-96'da beş §4 satırının `Updated At` hücresidir.

**Gizlilik.** Probe snapshot'ının redaksiyondan önceki IMEI ve `persist.sys.miui.sno` değerleri hiçbir dosyaya, rapora ya da mesaja yazılmaz; kontroller maskeli yapılır. Redaksiyonsuz özgün yalnız depo dışındaki `../ishtar-arsiv/impl-96-unredacted.bundle`'da ve yerel reflog'da durur. Başka cihazların seri numaraları kayda geçmez.

**Git.** Commit yalnız kullanıcı onayıyla ve fazı adlandıran mesajla atılır. Geçmiş yeniden yazılmaz; K8 tek kayıtlı istisnadır. Push yalnız açık refspec ile yapılır: `git push origin main integrate/impl-96`; `--all` ve `--mirror` asla. Push'tan sonra `git ls-remote origin` ile hash karşılaştırılır. Geçmiş GitHub MCP dosya araçlarıyla gönderilmez.

**Cihaz.** Her adb komutu `platform-tools/adb.exe -s dc27e5d0` ile; betikler `ANDROID_SERIAL=dc27e5d0 MSYS_NO_PATHCONV=1` ile çalışır (`smoke.sh`'in `-s` seçeneği yok; `-o` yalnız ad alır). Ajan yalnız salt-okunur komut çalıştırır. Kurulum, mod değiştirme, deklanşör, izin diyaloğu gibi fiziksel eylemler kullanıcıdadır ve onay ister. Her cihaz değişikliği `smoke.sh` ile önce ve sonra ölçülür; yalnız `BEGIN COMPARABLE`…`END COMPARABLE` karşılaştırılır.

**Dil.** Kullanıcıyla Türkçe. `Planner-docs/`, `docs/`, `README.md`, `UNTRACKED-BY-DESIGN.md` İngilizce. `PROJECT_LOG.md`, `NEXT_PROMPT.md` ve bu dosya Türkçe; Ek A İngilizce (İngilizce ledger metnine kaynaklık eder).

## 4. Pencere 0 — Keşif, plan, sözleşme

**Durum:** done.

- **O0 keşif:** Dört paralel scout (`LedgerMap`, `PlanDocsMap`, `ModuleMap`, `DocsFactCheck`). Git, GitHub, yedek kopyalar ve telefon salt-okunur ölçüldü; doğrulayıcı ve self-test baseline'da. Olgular Ek A'da, kapsam dışı bulgular §10'da.
- **O1 plan:** Kullanıcı onayladı. "Her pencere bir faz" yapısı kullanıcının isteğidir.
- **K8 = A:**
  - Redaksiyonsuz dal ucu depo dışına yazıldı: `../ishtar-arsiv/impl-96-unredacted.bundle` (77.094 B; sha256 `b9fa9c5cd5d0ae78f9f051ab62ecbfc2d9b2fa2fecd33f40247ef88bf58f6cd3`; `git bundle verify` geçti; önkoşulu `7fa0a51`).
  - Dal `main` üzerinde yeniden kuruldu: `37edb5f` → `70946ff` (probe'da yalnız satır 42, 190 ve 191 `<redacted>`); `6a20999` → `03b0898` ve `fcceaab` → `775b321` (içerik birebir aynı). Eski uca göre ağaç farkı yalnız bu üç satır.
  - Maskeli tarama: tüm ref'lerden erişilebilen geçmişte ve izlenen dosyalarda üç değer 0 kez geçiyor (önce: üçü de yalnız `37edb5f`'te birer kez). Adlandırılmış yedek dal yok.
- **Geçitler:** Doğrulayıcı ve self-test baseline'da.

## 5. Pencere 1 — IMPL-96 uygulaması

**Hedef:** 2026-11-13 oturumlarının ledger kaydı (IMPL-96) ve O2 kapsamındaki belge kaymaları; tek commit C1.
**Önkoşul:** Pencere 0 `done`; ağaç temiz; dal `integrate/impl-96`. Açılışta silinecek depolar `gh api repos/ahmetxa/<ad>` ile yeniden ölçülür (404 = silindi) ve IMPL-96'ya ölçüldüğü hâliyle yazılır.
**Girdi:** Ek A (olgular, DEC metinleri, ledger çapaları ve gelenekleri). Ek A'daki satır numaraları 2026-11-13 ağacına aittir; her düzenlemeden önce yeniden doğrulanır.

| # | Ajan | Hedef ve kapsam | Yazma yetkisi | Kabul kriteri |
|---|---|---|---|---|
| W1 | task `LedgerDraftA` | §5 IMPL-96 satırı. §6 notları: `:527` depo, `:529` v2.2/13, `:531` cihaz (HyperOS 4, modül kurulu değil), `:541` derleme bırakıldı | yalnız taslak `local://impl96-draft-a.md` | §5 satırı 7 boru, `## 6.` başlığına bitişik; her ekleme "çapa + konum + metin"; yalnız Ek A olguları; İngilizce |
| W2 | task `LedgerDraftB` | §4: Faz6.1, 7.2, 7.3, 8.1, 8.3 hücrelerine tarihli not (durumlar değişmez; `Updated At` 2026-11-13; 11. denetim 2026-09-14'te yapıldı; `:101`'deki "tenth audit" ifadesine düzeltme notu; Faz7.2 `Run ID`'ye eksik `IMPL-94`). §7: yeni üst girdi; `:564` tetikleyicisi ateşlendi; `:549`, `:551`, `:553`, `:555`'teki "outstanding" notlarına kapanış notu. §8: `DEC-27`…`DEC-32` satırları; `DEC-01`'e `Previous status, kept:` biçiminde not; altı karara konusuz notu. **Hepsi ekleme biçiminde:** başlık ya da var olan metin yeniden yazılmaz; `Updated At` dışında hiçbir hücre değiştirilmez | yalnız taslak `local://impl96-draft-b.md` | §4'te 10, §8'de 7 boru; sözlük dışı durum değeri yok; her çapa dosyada bir kez geçiyor |
| W3 | task `ReadmeDrift` | `README.md`: §5.1'deki W3 tablosu | `README.md` | Yalnız tablodaki yerler; LF; İngilizce; yalnız Ek A olguları |
| W4 | task `UntrackedDrift` | `UNTRACKED-BY-DESIGN.md`: §5.1'deki W4 tablosu | `UNTRACKED-BY-DESIGN.md` | W3 ile aynı |
| T3 | orkestratör | `-o snapshots/<…>` → `-o <…>` | `docs/release-checklist.md:165`, `docs/agc-12mp-configuration.md:202` | Yalnız bu iki satır |
| I1 | orkestratör | W1 ve W2 taslaklarını ledger'a `edit` ile uygula | `Planner-docs/Planing-Ledger.md` | CRLF=LF, NUL=0; satır sayısı 644 + eklenenler; değişen satırlarda difflib yalnız ekleme gösterir (istisna: beş §4 satırının `Updated At` hücresi); doğrulayıcı baseline'da; `--word-diff` yalnız beklenen değişiklikleri gösterir |
| R1 ∥ R2 | reviewer ∥ security-reviewer | C1 adayı diff: olgu doğruluğu (Ek A, snapshot'lar), biçim, kapsam taşması; sır, kimlik, sunucu adresi | salt-okur | P0/P1 yok. Varsa ledger'ı orkestratör, diğer dosyaları düzeltici task düzeltir; geçitler yeniden çalışır |

**Sıra:** W1 ∥ W2 ∥ W3 ∥ W4 (ve T3) → I1 → geçitler → R1 ∥ R2 → düzeltmeler → kapanış.
**Kapanış (§0.4):** tek commit C1 `IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline`: ledger, `README.md`, `UNTRACKED-BY-DESIGN.md`, `docs/release-checklist.md`, `docs/agc-12mp-configuration.md`, bu dosya (§1'de Pencere 1 `done`, C1 başlığıyla), `PROJECT_LOG.md` (§11'e kısa girdi) ve Pencere 2 için yeniden yazılan `NEXT_PROMPT.md`. Onayla commit edilir.

### 5.1 W3 ve W4 hedef tabloları

Yerler alıntılanan metinle bulunur (satır numaraları 2026-11-13 ağacına aittir). Hedef metin İngilizce yazılır; olgular Ek A'dadır (kaynak sütunu).

**W3 — `README.md`**

| Yer | Şu an | Hedef | Kaynak |
|---|---|---|---|
| :3-5 | "… and an AOSPA Android 16 track." | Cümle kalır; eklenir: Android 16 izi 2026-11-13'te bırakıldı (`DEC-28`); telefon HyperOS 4'te ve projenin hiçbir modülü kurulu değil | A.1 DEC-28; D1, D7 |
| :18 | "Source at v2.1 / versionCode 12." | "Source at v2.2 / versionCode 13." | R1 |
| :19 | "Standalone module symlinking `aon_front.pb` into `/vendor`." | Modül `/vendor/lib64/camera`'yı kopyalar, `aon_front.pb`'yi ekler ve dizini bind-mount eder; dosya zaten varsa çıkar (HyperOS 4 bunu kendisi sağlıyor) | E3, D6 |
| :20 | "two smali sources, the experimental HAL patch table, and the reproduction recipe" | Gerçek içerik | E4 |
| :24-30 Documentation | Kök belgeler için satır yok; `docs/` satırı iki dosya sayıyor | `PROJECT_LOG.md`, `NEXT_PROMPT.md`, `ORCHESTRATION_PLAN.md` (Türkçe süreklilik belgeleri) ve `CHANGELOG.md` (modül sürüm notları) satırları; `docs/` = 18 belge (biçim, prosedür, kanıt, runbook) | E5 |
| :75-81 sürüm tablosu | v2.1 "Most recent, and currently installed on device `dc27e5d0`…" | v2.1 → v2.2 ile aşıldı. Tablo altına: `dist/` (`*.zip` ile dışlanır) `scripts/build-release.py` çıktılarını tutar: v2.2 (AOSPA A15'e IMPL-81 ile kuruldu) ve kökteki v2.1 zip'inden farklı bir IMPL-76 v2.1 derlemesi; HyperOS 4'te proje modülü kurulu değil | R1, E6, D7 |
| :142 | "`scripts/` … `smoke.sh`, the read-only device state snapshot." | `build-release.py` (deterministik sürüm derleyici, `--self-test`) eklenir | ModuleMap; V3 |
| :143 | "`<UTC yyyymmdd-HHMM>__<subplan>__<label>.txt`" | Ad, makinenin yerel saatini taşır (UTC+3); başlıktaki `taken` satırı UTC'dir | E7 |
| :144 | "`common_clone.log`, `kernel_clone.log` … clone logs, 32 and 86 bytes." | Satır kaldırılır (2026-11-13'te silindi, K4; içerik `PROJECT_LOG.md` §2.1'de alıntılı) | K4, E11 |
| :148+ Orientation | Okuma `Planner-docs/` ile başlıyor | Önce `NEXT_PROMPT.md` → `ORCHESTRATION_PLAN.md`, sonra var olan liste | plan §0 |
| :186 Exclusions | `snapshots/` dışlanmış gibi yazılmış | Satır kaldırılır: `snapshots/` izleniyor (`FIND-2.2-03`) | E13 |
| (yok) remote | README deponun remote'unu hiç anmıyor | Tek cümle: remote, özel GitHub deposu `ahmetxa/ishtar_cam_modes` (`DEC-27`); push yalnız açık refspec ile | G3, E12 |

**W4 — `UNTRACKED-BY-DESIGN.md`**

| Yer | Şu an | Hedef | Kaynak |
|---|---|---|---|
| :9-10 | "Faz 1.6 … may absorb this content into the root README. Until it runs, this file is the record." | Faz 1.6 çalıştı (verified, 2026-08-30); `README.md` dışlamaları özetler; bu dosya ayrıntılı kayıt olarak kalır | E1 |
| :36 | "The tracked set is 84 files." | 84, Faz 1.1 rakamı olarak kalır; yazım anında `git ls-files \| wc -l` ile ölçülen sayı ve tarihi eklenir | G12 |
| :38-41 | "`common_clone.log` records that the `common_sm8550` clone failed (`fatal: …`)" | `fatal:` satırı `kernel_clone.log`'daydı; `common_clone.log` yalnız `Cloning into 'common_sm8550'...` içeriyordu; ikisi de (hiç izlenmedi) 2026-11-13'te silindi (K4); içerik `PROJECT_LOG.md` §2.1'de | K4, E11 |
| :61 | "Rebuild from the tagged tracked source. **Faz 1.2 audits these five archives …**" | Depoda etiket yok: izlenen kaynaktan `scripts/build-release.py` ile derlenir; Faz 1.2 denetimi temiz kapandı (`DEC-05`, IMPL-02, 2026-08-24) | E2, E8 |
| :63 | "Transient tooling output. Not needed; content quoted in section 1 above." | 2026-11-13'te silindi (K4); içerik `PROJECT_LOG.md` §2.1'de | K4 |
| :89 | "… is the `Faz 1.2` audit and open decision `DEC-05`." | Yanıtlandı: beş arşivin hiçbirinde keystore yok; `DEC-05` 2026-08-24'te temiz kapandı (IMPL-02) | E2 |
| :128-132 | "This repository is **local-only**. No remote is configured, and adding one is open decision `DEC-01` …" | 2026-09-10'dan beri özel remote (`DEC-01`, IMPL-90: `ahmetxa/ishtar`); 2026-11-13'ten beri `origin` = özel `ahmetxa/ishtar_cam_modes` (`DEC-27`), geçmiş aynı hash'lerle; önce `DEC-05` temizlendi; `snapshots/` tam çözünürlüklü çekimler taşıdığı için remote özel kalır | G3, G4, E9 |
| §4 Regenerable Module Artifacts | `ishtar-cam-modes/candidates/*.bin` için satır yok | Satır eklenir: Faz 5.1 aday blob'u (`dcgB-m0-12bit.bin`), `ishtar-cam-modes/tools/mode0_12bit.py` ile yeniden üretilir; hiçbir mod geçişi kanıtlanmamış bir varyantı seçemesin diye `blobs/` dışında tutulur (`.gitignore:56-58`) | E10 |

## 6. Pencere 2 — Kapanış ve yayın

**Hedef:** Oturum belgelerinin bayat satırlarını temizlemek, NEXT_PROMPT'u koşu 21'e hazırlamak, dalı yayınlamak.
**Önkoşul:** Pencere 1 `done` (C1 var).

| # | Ajan | Hedef ve kapsam | Yazma yetkisi | Kabul kriteri |
|---|---|---|---|---|
| W5 | task `ProjectLogUpdate` | PROJECT_LOG bayat ifadeleri (alıntıyla bulunur; satır numarası verilmez): §1 "**2026-11-13 kullanıcı beyanı (ölçülmedi):**" → ölçüldü (`70946ff`), 2026-11-13'te gözlendi; §2.3 "(yamasız APK'da bu anahtar yok)" → anahtar prefs dosyasında yok; §3.5 "`origin/main`'den sonraki dört commit push edilmedi", "*(push edilmedi)*", "*(HEAD, push edilmedi)*" → yazım anındaki push durumu ve commit listesi (`7fa0a51`, `70946ff`, `03b0898`, `775b321`, C0, C1); §4 "**Açık kararlar (2026-11-13):**" ve DEC-07/DEC-08 satırlarındaki "**AÇIK**" → konusuz (`DEC-28`); §8 tablosunda IMPL-96 ile çözülen satırlar (11. denetim "outstanding", "47 commit, 225 dosya, remote yok", "Telefon AOSPA A15 + KernelSU Next … ölçülmedi", README/UNTRACKED, `release-checklist.md:165`); §9 R8 "Dosyalar farklıysa … ölçülmedi" → HAL farklı, sensör aynı (ölçüldü), K9 karar verir; `docs/pre-rental-plan.md:N` ve `docs/build-environment.md:N` atıfları `03b0898`'in eklediği 8 satırlık not yüzünden +8 kaymış. §2, §3.2 (IMPL-96 tamamlandı), §4 (`DEC-27`…`DEC-32` ledger'da). Eski §11 girdilerine dokunulmaz | `PROJECT_LOG.md` | Türkçe, LF; ledger ile çelişki yok; kimlik değeri yok |
| W6 | task `HandoffRewrite` | NEXT_PROMPT'u Pencere 3 (koşu 21) için yeniden yaz: K9 ve §7'deki kapsam soruları, koşu 21 tuzakları | `NEXT_PROMPT.md` | Türkçe, LF |
| R2 | security-reviewer | Push'un göndereceği her şey: `origin/main..integrate/impl-96` (`7fa0a51` dahil). Sır, seri numarası, sunucu adresi; Ek A.5'teki kimlik kontrolü | salt-okur | Bulgu yok |

**Sıra ve onaylar (her biri ayrı):** W5 ∥ W6 → R2 → C2 `Window 2: project log sweep and handoff for planning run 21` (W5, W6 ve bu dosya; belgeler push'u "C2'den hemen sonra, onayla" diye yazar ve sonucun bir sonraki pencerenin açılışında `git ls-remote origin` ile doğrulanacağını belirtir) → `main`'in `integrate/impl-96`'ya fast-forward edilmesi → `git push origin main integrate/impl-96` → `git ls-remote origin` ile hash karşılaştırması (sonuç sohbette raporlanır, Pencere 3'ün kaydına girer).
**Silinecek depolar:** `gh api` ile ölçülür. Silinmişse PROJECT_LOG'a yazılır; ledger'daki `DEC-30` yürütme notu ledger'a yazan bir sonraki koşuda (koşu 21) eklenir.

## 7. Pencere 3 — Planlama koşusu 21 (Step 1 + Step 2)

**Önkoşul:** Pencere 2 `done`. **Başlamadan kullanıcıya sorulacaklar:**
1. **K9:** 50MP HAL katmanı HyperOS 4 HAL'inde yeniden türetilsin mi? Faz 3/4 benzeri statik analiz gerekir (R10 bağlam riski). Türetilmezse HAL katmanı HyperOS 4'te devre dışı kalır, sensör katmanı sürer.
2. **Kutucuk/WebUI zinciri:** Uzun basış `com.rifsxd.ksunext`'e bağlı ve bu ROM'da yok. Kurulu KernelSU `4.3.0-r1`'in yöneticisi ve WebUI desteği önce ölçülür. Zincir uyarlansın mı, kaldırılsın mı?
3. **AGC tuzakları:** 10 tuzak 37 değerinde kurulu. HyperOS 4 için yeni, korumalı bir temizleme prosedürü kapsama girsin mi? Var olan tek prosedür (`docs/phase3-preconditions.md:71-119`) AOSPA'ya özel ve yedeksiz.
4. **v2.3 kapsamı:** `Kullanim.txt` (`DEC-29`), modül içindeki bayat yorumlar, tile-app `versionName`.

**Step 1 — `Main-Planing.md`** (CRLF; yalnız orkestratör; metni kullanıcı onaylar):
- Faz 7 ve Faz 8 §6 yol haritasından **silinmez**; satırlar ve bölümler yerinde, tarihli notla emekli edilir ("Retired 2026-11-13 by `DEC-28`"). Satır silmek `extra_phase_folder_without_main_phase` uyarısı üretir; `--strict` bunu hataya çevirir.
- K7 = (a) için iki seçenek; seçimi kullanıcı yapar: (i) yeni Faz 10 (klasör `Faz-10-Plans`; her yerde "ClaudeQB Phase 10" diye yazılır, çünkü `50MP-Entegrasyon-Plani.md`'nin Faz 10'u ayrı bir şeydir) ya da (ii) Faz 8'in kamera yarısının HyperOS 4'e yeniden hedeflenmesi (yeni alt planlar `Faz8.4` ve sonrası).
- R8 gerçekleşti (HAL `2a955e68…`); R9 konusuz. `:75`, `:211` ve `:265`'teki Hetzner ifadeleri emekli bölümlerle birlikte kapanır (`AUDIT-FIX-41`, `-42`, `-57`).
- §4'teki hedef son durum ("From a clean AOSPA build…") K7 = (a)'ya göre yeniden yazılır.

**Ledger (orkestratör):** §2'ye koşu 21 satırı; §3'e yeni snapshot (`SNAP-…-MAIN`, Step 2 varsa `-SUBPLANS`). §4'te `Faz7.2`, `Faz7.3`, `Faz8.1`, `Faz8.3` → `superseded` (`Superseded By` dolu olmalı); `Faz6.1` koşu 21'in kararıyla; yeni alt planlar `planned`. Silme yapıldıysa `DEC-30` yürütme notu; `DEC-32`'ye koşu 21 atfı.
**Index (orkestratör):** Emekli alt planlar üstü çizili ve "Do not revive" notlu; yeni girdiler eklenir.
**Ontology (orkestratör, bayt-korumalı):** Değişmez 10 (gerçekleşti) ve 11 (emekli; Hetzner).
**Step 2 — yeni alt planlar:** Paralel task ajanları her alt planın **taslağını** aynı pencerede `local://` altına yazar; son `Faz-N-Plans/*.md` dosyalarını orkestratör yazar (ClaudeQB: "parent writes final artifacts"). Biçim: H1 `# Faz N.M — …`; 13 başlık, her biri en az 20 karakter; §9'da uygulama sözleşmesi tablosu (`Path | State | Purpose | Validation Command IDs`; State ∈ existing, modified, proposed, generated, external, deferred); TODO/TBD yok; 5 ya da daha çok dosyada tekrarlanan 80+ karakterlik cümle yok; numaralarda boşluk yok.
**Aday alt planlar** (koşu 21 kesinleştirir):
1. HyperOS 4 kamera yığınının salt-okunur ölçümü: değişmez 3 için servis adları (`setmode.sh:52-58`, `:79-83` AOSPA adlarını kullanıyor), `chcon` etiketleri, `/data/adb/ksu/.allowlist`, yönetici ve WebUI.
2. Sensör katmanı: v2.2 değişmeden HyperOS 4'te, smoke bracket ile (kurulum kullanıcıda).
3. 50MP HAL katmanının yeniden türetilmesi (yalnız K9 = evet).
4. Kutucuk/WebUI zinciri.
5. v2.3 sürümü: `Kullanim.txt`, sürüm yerleri, CHANGELOG, manifest; AON modülünün HyperOS 4'te gereksizliği.
6. AGC tuzak denetimi ve korumalı temizleme (kullanıcı kapsama alırsa).

**Geçitler:** `--mode step2 --strict` ve `--mode step3-preflight --strict`; `subplan_count` yeni toplamı gösterir.

## 8. Pencere 4 — 12. denetim (Step 3)

- `run-step3.md`: yalnız `Planner-docs/Sub-Planing-Audit.md` yazılır (orkestratör). En fazla 3 salt-okur reviewer (kapsam, hazırlık, güvenlik) paralel çalışır.
- Tuzaklar: Doğrulayıcı denetim durumunu dosyadaki ilk `status:` eşleşmesinden okur; başlıkta eski denetimin durumu alıntılanmaz. 15 başlık tekil olmalı, her biri en az 20 karakter. Bulgu kimlikleri `AUDIT-FIX-58`'den devam eder.
- Beklenen: `Faz7.2`, `7.3`, `8.1`, `8.3` SUPERSEDED; `Faz4.6` DEFERRED; yeni alt planlar READY, READY_WITH_WARNINGS ya da gerekçeli NEEDS_REPAIR.
- Geçit: `--mode step3 --strict` ve `--mode all`. Step 4 önkoşulu `p0_findings=0`, `p1_findings=0`.

## 9. Pencere 5+ — K7 = (a) Step 4 koşuları

- `run-step4.md`: 12. denetimin kuyruğu, dizin sırasıyla; pencere başına bir dilim (dilimler küçükse en fazla dört).
- **Yazma yetkisi:** dilimin alt planındaki §9 uygulama sözleşmesi tablosunda adı geçen yollar (orkestratörün atadığı tek sahip); ledger §4/§5 ve bu dosya yalnız orkestratörde.
- **Kabul:** alt planın kabul kriterleri, §3'teki geçitler ve cihaz değişikliği varsa smoke bracket (önce/sonra, `BEGIN COMPARABLE`…`END COMPARABLE`); öngörü ve karar kuralı ölçümden önce yazılır.
- Kimlikler `IMPL-97`'den devam eder. Cihaz eylemleri kullanıcıdadır.
- Her pencere sonunda §1'e yeni satır eklenir (`5`, `6`, …).

## 10. Kapsam dışı, bildirilen bulgular (dokunulmadı)

- Ledger'da IMPL-96 kapsamı dışındaki kaymalar (PROJECT_LOG §8 tablosundaki `Planner-docs/Planing-Ledger.md:` satırları: `:19`, `:51`, `:57-60`, `:66`, `:88-97`, `:106`, §5 biçim satırları, `:575`, `:582-583`, `:586`, `:633`) → koşu 21 ya da 12. denetim.
- `.gitignore`'da `camera.qcom.so` ya da `*.so` kuralı yok; değişmez 9 yalnız build-release A2 kontrolü ve disiplinle korunuyor. HyperOS 4 HAL'i analiz için kopyalanacaksa (K9) önce kural eklenmesi önerilir.
- `docs/patch-table-format.md:57`: 23,853,648 = `0x16BFA50`; dosyada `0x16BBBD0` yazıyor.
- `docs/recovery-runbook.md:68-70`: HyperOS 4 notu yok; temiz devre dışı bırakmadan sonra AOSPA HAL md5'ini bekliyor.
- Modül içindeki bayat yorumlar (`action.sh:7`, `:17`; `service.sh:8-12`; `tile-app/AndroidManifest.xml:5`, `:52-54`; `BaseTile.java:17`; `customize.sh:62`) ve tile-app `versionName 2.1` → v2.3.
- `smoke.sh`: `-s` seçeneği yok; birden çok cihaz bağlıyken `ANDROID_SERIAL` verilmezse alanlar boş kalır ve betik yine 0 ile çıkar [ÇIKARIM].
- `build-release.py --self-test` üç boş geçici dizin bırakıyor ve `debug.keystore`'u geçici olarak kopyalıyor.
- `docs/agc-12mp-configuration.md:380-381`: betiğin yalnız varlığı bildirdiğini söylüyor; oysa `prefs.trap.count` varlığı sayar ve yanına `armed`/`values` eklendi (smoke baseline `:148`, `:150-151`).
- Probe'da 8192x6144 ayrıca kullanımdan kalkmış `android.scaler.availableRawSizes` etiketinde de geçiyor; NEXT_PROMPT "yalnız vendor etiketleri" diyordu.
- Snapshot'ta "Open Camera" adı geçmiyor; `com.xiaomi.module.evaluation` 1.55'in Open Camera olduğu AOSPA dönemi kanıtına (`FIND-4.4-02`) dayanıyor.
- `PROJECT_LOG.md` §2.3, "(yamasız APK'da bu anahtar yok)" [ÇIKARIM: yanlış; anahtar yalnız prefs dosyasında yok] → Pencere 2, W5.
- AGC ve Open Camera'nın `lastUpdateTime` değeri 2026-09-20, ROM'un derleme tarihinden önce [ÇIKARIM: `/data` ROM değişiminden sağ çıktı ya da saat yanlıştı].

## Ek A — IMPL-96 contract (English)

Single source of facts for every IMPL-96 writer (ledger drafters, README/UNTRACKED editors, PROJECT_LOG/NEXT_PROMPT editors). A fact not in this appendix is not written; a writer that needs one reports it instead. Line numbers refer to the tree of 2026-11-13 and are re-checked before every edit.

### A.1 Identifiers

| ID | Meaning | Status |
|---|---|---|
| IMPL-96 | Record of the 2026-11-13 sessions: repository move, ROM-build retirement, HyperOS 4 read-only baseline, the 2026-09-20 AOSPA A15 device notes, K4 cleanup, K8 identifier redaction and branch rebuild, T2/T3 document fixes, and the user's verdicts. Record-only: no sub-plan changed, no device state changed. | one ledger §5 row (window 1) |
| DEC-27 | Repository move: `origin` = private `ahmetxa/ishtar_cam_modes`; 62 commits pushed with unchanged hashes. Replaces DEC-01's repository (`ahmetxa/ishtar`), not the private-remote decision. | answered by the user, 2026-11-13 |
| DEC-28 | ROM build abandoned; the phone runs HyperOS 4 (`OS4.0.0.44.WMACNXM`), **observed** 2026-11-13 (ROM build date 2026-09-23; `/data/adb/modules` dated 2026-10-26, so installed before the observation). Phases 7 and 8 lose their purpose; formal retirement is planning run 21. Moots DEC-07, DEC-08, DEC-22, DEC-24, DEC-25, DEC-26. | answered by the user, 2026-11-13 |
| DEC-29 | `Kullanim.txt` stays as shipped in v2.2; corrected in the next release (K1 = b). | answered by the user, 2026-11-13 |
| DEC-30 | The three ROM-build GitHub repositories are deleted by the user (K5 + K6): `ahmetxa/ishtar`, `ahmetxa/android_local_manifests`, `ahmetxa/android_device_xiaomi_ishtar`. Mirrors of the two public ones are kept in `../ishtar-arsiv/`. Execution is measured with `gh api` (404 = deleted). | answered by the user, 2026-11-13; execution pending (all three still existed on 2026-11-13) |
| DEC-31 | K8 = A: the committed but unpushed probe snapshot held device identifiers (two IMEIs and `persist.sys.miui.sno`). They were redacted in place and the three unpushed commits rebuilt before any push. This is the one recorded exception to the standing rule against rewriting history (ledger rows cite commit hashes); no ledger row cited the old hashes. The unredacted original is kept outside the repository in a verified bundle. | answered by the user and executed, 2026-11-13 |
| DEC-32 | K7 = (a): adapt the module to HyperOS 4. Scope (50MP HAL re-derivation = K9, tile/WebUI chain, AGC traps, v2.3) is settled by planning run 21. | answered by the user, 2026-11-13 |

### A.2 Facts

| # | Fact | Value | Source / when measured |
|---|---|---|---|
| G1 | `main` | 63 commits, tip `7fa0a51` (planning run 20 + eleventh audit, 4 files, committed unchanged 2026-11-13); not pushed | git, 2026-11-13 |
| G2 | `integrate/impl-96` | Rebuilt 2026-11-13 (K8) on `7fa0a51`: `70946ff` (the two IMPL96 snapshots; probe lines 42, 190, 191 redacted), `03b0898` (historical notes in `docs/build-environment.md` and `docs/pre-rental-plan.md`, plus `docs/rom-build-device-notes.md`), `775b321` (`PROJECT_LOG.md`, `NEXT_PROMPT.md`), then window commits (C0 adds this file). The old hashes `37edb5f`, `6a20999`, `fcceaab` exist only in the bundle and the local reflog: cite only the new ones | git, 2026-11-13 |
| G3 | `origin` | `https://github.com/ahmetxa/ishtar_cam_modes.git`, private, default branch `main` | `gh api`, 2026-11-13 |
| G4 | Remote state | `git ls-remote origin` → `refs/heads/main` = `587e3b581a66961082e49e2449327478724ad765` (62 commits); nothing after it is pushed | 2026-11-13 |
| G5 | Root commit | `ff6934e` (2026-08-24), identical locally and on GitHub | PROJECT_LOG §11; git |
| G6 | Old remote | `ishtar-eski` (`ahmetxa/ishtar`) removed locally; its only branch `main@f8a05ca` (IMPL-89, 2026-09-10) is an ancestor of `main` | git merge-base, 2026-11-13 |
| G7 | Pre-push secret scan | Whole history clean; the only password-pattern hit is the accepted debug signing default (DEC-10) | PROJECT_LOG §11 |
| G8 | Repositories to delete | All three still existed on 2026-11-13 (`gh api` 200): `ahmetxa/ishtar` private, the other two public | `gh api`, 2026-11-13 |
| G9 | Mirrors | `../ishtar-arsiv/android_local_manifests.git` (`main@22283d8`), `../ishtar-arsiv/android_device_xiaomi_ishtar.git` (`beryl@d48816f`, `vauxite@713784c`); `git fsck` exit 0 for both | 2026-11-13 |
| G10 | K8 bundle | `../ishtar-arsiv/impl-96-unredacted.bundle`, 77,094 B, sha256 `b9fa9c5cd5d0ae78f9f051ab62ecbfc2d9b2fa2fecd33f40247ef88bf58f6cd3`; ref `refs/heads/integrate/impl-96` = `fcceaab`; requires `7fa0a51`; `git bundle verify` OK | 2026-11-13 |
| G11 | K8 scan | Masked scan of `git log --all -p` and of every tracked file: 0 occurrences of the three values after the rebuild (before: one each, all in `37edb5f`). Tree diff old tip → new tip: probe only, 3 lines | 2026-11-13 |
| G12 | Tracked files | Measure with `git ls-files \| wc -l` when writing (349 before C0) | — |
| K4 | Deleted 2026-11-13 (five items) | Never-tracked `devir-teslim-promptu.md` (replaced by `NEXT_PROMPT.md`); empty root dir `UsersahmetAppDataLocalTempaon-smoke/`; never-tracked logs ignored by `.gitignore:48` (`*.log`): `install.log` (line-identical to tracked `snapshots/20260831-1603__faz2.2__install-transcript-v2.1.txt`, CR aside), `common_clone.log`, `kernel_clone.log` | PROJECT_LOG §2.1, §11 |
| D1 | ROM | HyperOS `OS4.0.0.44.WMACNXM`, Android 17 (SDK 37), security patch 2026-09-01 | adb getprop, 2026-11-13; probe |
| D2 | Vendor/odm fingerprint | `Xiaomi/ishtar/ishtar:13/TKQ1.221114.001/OS4.0.0.44.WMACNXM:user/release-keys` | adb getprop, 2026-11-13 |
| D3 | Kernel / root | `5.15.215-KylinKernel-260925-Release`; SELinux Enforcing; `su` context `u:r:ksu:s0`; verifiedbootstate `orange`; KernelSU `4.3.0-r1` (`ksud 4.3.0-r1 (uapi: 6)`, probe only) | adb, 2026-11-13; probe :214, :356, :360 |
| D4 | Camera HAL | `/odm/lib64/hw/camera.qcom.so` md5 `2a955e68ad043380675529edb64a40f7`, 27,305,440 B; differs from the AOSPA A15 stock HAL the module is locked to (`HAL_STOCK_MD5` `c3fa63a8…`, 27,268,688 B) | adb, 2026-11-13; `halpatch.sh:32-34` |
| D5 | Sensor blob | `/odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin` md5 `9e4d0fe1a8bf2eb4146c9917a0ac2c4c` = module `EXPECT_MD5` | adb, 2026-11-13 |
| D6 | AON | `/vendor/lib64/camera/aon_front.pb -> /odm/lib64/camera/aon_front.pb` ships in the ROM | adb, 2026-11-13 |
| D7 | Modules | `ishtar_cam_modes`, `ishtar_aon_fix` absent; 13 other module dirs (FreePPS, advsettings-en, box_for_root (disabled), eight `*-morphe`, unlimitedphotos, zygisksu = NeoZygisk) | adb su ls, 2026-11-13; probe :287-353 |
| D8 | Cameras | 13 camera devices; hal0 standard streams max 4096x3072; 8192x6144 appears only in vendor tags and the deprecated `android.scaler.availableRawSizes` | probe :267, :368, :372 |
| D9 | AGC | `org.codeaurora.snapcam` versionName `8.4.300.414775575.18` = unpatched `AGC8.4.300_V9.6_snap.apk` (md5 `fa4066eb3bf82cc097906fd108073500`); `pref_camera_resolution=full` → 12.58 MP derived (4096x3072); `prefs.trap.armed = 10` (value 37); `agc.pref_48m` absent | adb, 2026-11-13; probe; smoke baseline |
| D10 | Other apps | `com.android.camera` (`1+6.4.000380.1`); `com.xiaomi.module.evaluation` 1.55 (Open Camera per `FIND-4.4-02`; the probe itself does not name it); no project tile app; no `com.rifsxd.ksunext` or `me.weishu.kernelsu` package | adb pm, 2026-11-13; probe :223-239 |
| D11 | Extra ROM identity | Build `CP2A.260605.016`; vendor security patch 2026-02-01; bootimage fingerprint carries `OS3.0.305.0.WMACNXM` | probe :119, :198 |
| V1 | Validator `--mode all` | `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0` | 2026-11-13 (also after the rebuild) |
| V2 | Validator `--mode step4 --strict` | Fails only on `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9` (expected baseline) | 2026-11-13 |
| V3 | Self-test | `SELF-TEST: PASS`; VAL-BUILD2 sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0`; A1–A3 PASS | 2026-11-13 |
| R1 | Release | `ishtar-cam-modes` v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba` | md5sum, 2026-11-13 |
| T3 | `smoke.sh -o` path bug | `docs/release-checklist.md:165` and `docs/agc-12mp-configuration.md:202` pass `snapshots/…`; `smoke.sh` prepends `snapshots/` itself (`:38`, `:284`); correct form at `docs/release-checklist.md:414` | 2026-11-13 |
| A1 | Trap clearing | No procedure in `docs/agc-12mp-configuration.md`; the only one is `docs/phase3-preconditions.md:71-119` (no backup step, truncate-first ordering, AOSPA owner and SELinux label hard-coded) | 2026-11-13 |
| M1 | Module on HyperOS 4 (code reading, not measured) | Sensor guard passes (`EXPECT_MD5`), so the sensor layer would mount; the HAL guard (`post-fs-data.sh:101-107`) fails closed and skips the HAL layer; `setmode.sh:52-58`, `:79-83` use AOSPA camera-provider service names not measured on HyperOS 4; tile long-press needs `com.rifsxd.ksunext` (`WebUiActivity.java:15`) | ModuleMap scout [INFERENCE] |
| E1 | Faz 1.6 | `Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md` is `verified`, updated 2026-08-30 | ledger :71 |
| E2 | DEC-05 | "**Closed clean, 2026-08-24 (IMPL-02).**" No keystore entry in any of the five archives; no rotation or withdrawal needed | ledger :576 |
| E3 | AON fix behaviour | `ishtar-aon-fix/post-fs-data.sh:12-15` exits when `/vendor/lib64/camera/aon_front.pb` exists; otherwise `:22-40` copies `/vendor/lib64/camera` into the module, adds the file and bind-mounts the directory | ModuleMap |
| E4 | `agc-50mp-yama/` | `README.md` (reproduction recipe), two smali sources (`allOutputSizes.smali`, `getSupportedOutputSizes.smali`), seven experimental HAL patch tables (`hal-*-deneme.patch`), four Faz 4.1 stage tables (`f41-*.tbl`), `find_tag_write_site.py`, `tools/` | ls, 2026-11-13 |
| E5 | `docs/` | 18 Markdown documents (formats, procedures, evidence, runbooks, the generated release manifest) | ls, 2026-11-13 |
| E6 | `dist/` | `ishtar-cam-modes-v2.2.zip` (1,009,107 B, md5 `e95789572311cc95266d3ab4045cdcba`; installed on AOSPA A15 by IMPL-81, VAL-INSTALL) and `ishtar-cam-modes-v2.1.zip` (1,008,686 B, md5 `4a8226d6f4c4cacd97d8b96086bb36fa`, an IMPL-76 rebuild; the root v2.1 zip is md5 `fea919b67a4693a4591127be4a6e9daa`) | md5sum, 2026-11-13; PROJECT_LOG §2.2; README :77 |
| E7 | Snapshot names | The name carries the host's local time (UTC+3); the header `taken` line is UTC: `20261113-1821` ↔ `2026-11-13T15:21:35Z` | smoke baseline header |
| E8 | Tags | The repository has no tags | `git tag`, 2026-11-13 |
| E9 | DEC-01 history | Private remote `ahmetxa/ishtar` from 2026-09-10 (IMPL-90; `main` pushed at `f8a05ca`); the DEC-01 row notes that `snapshots/` holds full-resolution camera captures, so a public remote would publish them | ledger :599 |
| E10 | `candidates/*.bin` rule | `.gitignore:56-58`: "Faz 5.1 candidate blobs: regenerated by tools/mode0_12bit.py, and kept out of blobs/ so no mode switch can select an unproven variant." | `.gitignore` |
| E11 | Deleted logs (K4) | `common_clone.log` = `Cloning into 'common_sm8550'...`; `kernel_clone.log` = `fatal: destination path 'kernel_ishtar' already exists and is not an empty directory.` | PROJECT_LOG §2.1 |
| E12 | README remote | `README.md` states no repository remote (its remote mentions concern `device_ishtar/` and `refs/`) | grep, 2026-11-13 |
| E13 | `snapshots/` | Tracked (`FIND-2.2-03`), although `README.md:186` lists it under Exclusions | README; PROJECT_LOG §8 |

### A.3 Rules for every writer

- English in `Planner-docs/`, `docs/`, `README.md`, `UNTRACKED-BY-DESIGN.md`; Turkish in `PROJECT_LOG.md`, `NEXT_PROMPT.md`, this plan's body.
- The ledger is CRLF; every other file touched here is LF. Never convert line endings.
- AOSPA A15 evidence stays valid as history; never generalize it to HyperOS 4, and vice versa.
- Never write secrets, tokens, server addresses, or any device serial other than `dc27e5d0`. Never quote the redacted IMEI or `persist.sys.miui.sno` values: name the key and line only.
- Status values only from the fixed vocabulary; no compound values (AUDIT-FIX-11).

### A.4 Ledger conventions and anchors (2026-11-13 tree)

- 644 lines, all CRLF, NUL 0. §2 :13 (header :15; run 20 :41 is a historical row and is not edited). §4 :62 (header :64; rows :66–:107; exactly 10 `|` each). §5 :109 (header :111; IMPL-95 :524 is followed directly by `## 6.` at :525: the new row goes between them, with no blank line). §6 :525 (:527 repository, :529 deliverables, :531 device, :541 build environment). §7 :547 (blockquote entries newest first, separated by `>` lines; a new top entry goes after :548; standing triggers :559–:565; vendor-blob trigger :564). §8 :569 (header :571; 7 `|` per row; last row DEC-26 at :601; new rows go after :601).
- §4 status vocabulary: `planned, ready, ready_with_warnings, in_progress, implemented, verified, blocked, superseded`. IMPL-96 changes no status. Dated notes go into free-text cells (precedents :90, :106); `Updated At` → `2026-11-13`.
- §4 cell-end anchors (each unique): Faz6.1 :97 Next Action `deliberately — see IMPL-03 note.`; Faz7.2 :100 Blocker ``Faz7.1` is verified (`IMPL-91`).`` and Next Action `then stop for the rental approval.`; Faz7.3 :101 Blocker `tenth Step 3 audit of planning run 19's amendment.` and Next Action `the AGC re-configuration and a trap audit.`; Faz8.1 :102 Blocker (whole cell) and Next Action ``ontology entry, byte-preserving (`AUDIT-FIX-22`).``; Faz8.3 :104 Blocker `blocks it and raises a replanning input instead.` and Next Action `Android 16 init service names before any mode switch.`
- §5 columns `| Run ID | Date | Sub-plan | Slice performed | Validation evidence | Outcome |`. Record-only precedents: IMPL-89 :518, IMPL-95 :524 (`…; no sub-plan edited`). The slice opens with a scope disclaimer and then numbered items (1)…; commits are backticked short hashes; snapshots are full backticked paths; validator results are `key=value`; hygiene line `Ledger: CRLF kept, no bare CR, N pipes on each edited row.`; Outcome = bold verdict, open items, `Next:`.
- §6 keeps old text with dated bold notes, appended (:527 `**Superseded on one point …**`) or prefixed (:541 `… The sentences that follow are kept as the record of what was true before.**`). Paragraph-end anchors: :527 ``with `main` pushed at `f8a05ca`.**``; :531 ``and the standing warning in `README.md` applies.``; :541 `which is a Linux environment, not an interpreter.`
- §7 headline style `> **REPLANNING INPUT 2026-11-13 (`DEC-28`): …**`; inline status updates `**Status 2026-11-13:** …`. Anchors: :549 ends ``and `Faz7.2` does not enter a paid session before it.``; :551 ends `before any of them enters the Step 4 queue.` §7 has **no** 2026-09-20 kernel entry: that open input is `docs/rom-build-device-notes.md:79-84`, and K3 closes it in the IMPL-96 row.
- §8 columns `| ID | Decision | Owner | Raised by | Blocks | Status |`, Owner `User`. Status is free text (`**ANSWERED 2026-11-13 by the user: …**`); updates put the new status first and keep the old after `Previous status, kept:` (:579, :599, :601), or append a dated note. "moot" is not yet used in §8 and goes into the Status cell as free text. Row-tail anchors: DEC-07 ``and on-device (`F8.1-07`) agreement. |``; DEC-08 ``Open, the user's. |``; DEC-22 `and choose the distribution they support. |`; DEC-24 `planning run 17 amended Main-Planing Phases 7 and 8. |`; DEC-01 ``already cleared the keystore question. |``; DEC-25 ``stays private. |``; DEC-26 `flexible IPv4 billing and deletion; snapshots; every price. |`.
- DEC-01 is already answered (private `ahmetxa/ishtar`, IMPL-90): DEC-27 replaces the repository, not the private-remote decision.
- The eleventh audit (2026-09-14, PASS_WITH_WARNINGS) is still called pending at :100 and :549; :101 still cites the tenth audit; :551, :553 and :555 still say a re-audit is outstanding.

### A.5 Push rules

- Only explicit refspecs: `git push origin main integrate/impl-96`; never `--all` or `--mirror`; then `git ls-remote origin` hash comparison.
- Before any push, an identity check over everything reachable from any ref (`git log --all -p`): every line with the key `persist.sys.miui.sno`, `ro.ril.miui.imei0` or `ro.ril.miui.imei1` reads `<redacted>`, and no 15-digit number passing the Luhn check appears. Report counts only; the redacted values are never recovered, read or written. Then a security review of `origin/main..integrate/impl-96`, including `7fa0a51`.
