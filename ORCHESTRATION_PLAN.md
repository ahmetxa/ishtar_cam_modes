# ORCHESTRATION_PLAN — ishtar

> **Onay:** kullanıcı, 2026-11-13 ("onay"). Kararlar: K8 = A, konusuz kapsamı = altı karar, K7 = (a).
> **Onay 2:** kullanıcı, 2026-11-14 ("onaylıyorum"): Pencere 2 planı (§6) varsayılan kararlarla (§6.1); aşama başına oturum döngüsü, aşama sonunda sorulmadan devir ve yerel commit, beklenmedik durumda sade bir soru (§0).
> **Kural:** Her yeni sohbet penceresi (oturum) bu plandan **tek bir aşamayı** yürütür (§0): bir fazın `O0`+`O1` aşamaları bir oturumda, `O2`, `O3`, `O4` ve `O5` her biri ayrı oturumda. Giriş noktası `NEXT_PROMPT.md`; ayrıntı, sözleşme ve durum bu dosyadadır.
> **Öncelik:** Ölçüm ve kanonik dosyalar (ledger, `Planner-docs/`) bu plandan üstündür. Çelişki bulunursa §10'a yazılır ve kullanıcıya söylenir; plan sessizce uydurulmaz.

## 0. Pencere protokolü

**Terimler (2026-11-14).** *Pencere N*: §1'deki plan fazı (ad tarihseldir; başta her faz tek oturumdu). *Aşama*: bir fazın orkestrasyon adımı: `O0` keşif, `O1` plan (kullanıcı onayına kadar), `O2` kontrat, `O3` paralel uygulama, `O4` entegrasyon ve geçitler, `O5` son inceleme ve kapanış. *Oturum*: bir sohbet penceresi. Aşama kimliği `Pencere 2 · O2` (kısaca `2 · O2`) biçimindedir. Tek başına "Faz N" ClaudeQB proje fazıdır (§3, Adlandırma).

**Döngü (kullanıcı kararı, 2026-11-14).** Her oturum tek bir aşamayı yürütür: `O0`+`O1` aynı oturumda (plan onayıyla biter); `O2`, `O3`, `O4` ve `O5` her biri ayrı oturumda. Fazın aşama ve görev tablosu o fazın bölümündedir (Pencere 2: §6.3). Aşama atlanmaz; oturum kendiliğinden sıradaki aşamaya geçmez.

1. **Açılış:** `NEXT_PROMPT.md`'yi oku; `git status`, `git log --oneline -8`, `git branch -vv`. §1'deki ilk `pending` satırı (aşama satırları dahil) ve fazın bölümünü oku. Önkoşul tutmuyorsa (ağaç kirli, dal farklı, beklenmeyen commit, önceki aşama `done` değil) bu beklenmedik bir durumdur (adım 6). Kontroller tutarsa aşama ayrı bir "başla" onayı beklemeden yürütülür.
2. **Yürütme:** yalnız o aşamanın görevleri. Orkestratör planlar, dağıtır, entegre eder, doğrular; alt ajan kuralları §3'te. Sonraki aşamaların ihtiyaç duyduğu her çıktı oturum bitmeden depodaki bir dosyaya yazılır (adım 8).
3. **Doğrulama:** aşamanın kabul kriterleri; §3'teki geçitler fazın belirttiği aşamada (Pencere 2: `O4`, düzeltme olursa `O5`'te yeniden). Kırmızı bir ağaçla kapanış yapılmaz.
4. **Kapanış (beklenmedik durum yoksa, sorulmadan):**
   - §1'de aşama satırı `done` olur ve kapanış commit'ini **başlığıyla** anar. Hash yazılmaz: commit kendi hash'ini taşıyamaz; hash `git log --grep '<başlık>'` ile bulunur (C0 için `git log --diff-filter=A -- ORCHESTRATION_PLAN.md`).
   - `PROJECT_LOG.md` §11'e oturum girdisi; Pencere 2'de `O4`'ten itibaren §2.6 da güncellenir.
   - `NEXT_PROMPT.md` sıradaki aşama için yeniden yazılır; sıradaki aşama başka bir fazın `O0`'ıysa o fazın girişi olarak. Bu yazım döngünün parçasıdır, ayrıca sorulmaz.
   - Değişen dosyalarda bayt ve boru kontrolü ile kimlik taraması (betik Ek A.5'te); ardından yerel kapanış commit'i onay sorulmadan atılır ve kullanıcıya `git show --stat` özeti verilir. Mesaj fazı ve aşamayı adlandırır.
   - Kullanıcıya yeni pencere açıp `NEXT_PROMPT.md`'deki metni yapıştırması söylenir.
5. **Onay kapıları (her zaman sorulur; beklenmedik durum sayılmaz):** `O1` sonunda plan onayı; `main`'in fast-forward'ı; her `git push`; cihaz eylemleri; AGC tercihlerine yazma. Depoları kullanıcı siler. Bu sorular kısa ve evet/hayır biçimindedir.
6. **Beklenmedik durum:** kapanış yapılmaz, `NEXT_PROMPT.md` yeniden yazılmaz, commit atılmaz. Kullanıcıya sade, teknik terimden arındırılmış bir dille sorulur: ne oldu, neden önemli, iki ya da üç seçenek ve önerilen seçenek. Yanıta göre devam edilir; durum çözülünce kapanış adım 4 ile yapılır. Beklenmedik durum sayılanlar:
   - açılış önkoşulunun tutmaması;
   - bir geçidin taban değerden sapması ya da kırmızı kalması;
   - ölçülen bir olgunun Ek A ya da planla çelişmesi (öngörülmüş değişiklikler, örneğin silinmesi beklenen bir deponun silinmiş olması, sayılmaz; yalnız kaydedilir);
   - P0 ya da P1 inceleme veya güvenlik bulgusu; kapsamı, bir kararı ya da git geçmişini değiştirmeyi gerektiren her düzeltme;
   - alt ajanın sahiplik dışına taşması, sözleşmeden sapması ya da işi bitirememesi, ve bunun aşama içinde giderilememesi;
   - planda olmayan bir eylem ihtiyacı (cihaz, dosya ya da depo silme, geçmişi yeniden yazma, yeni kapsam);
   - aşamayı durduran araç ya da ortam arızası (örneğin push kimlik doğrulaması).
7. **Aşama bir oturuma sığmazsa:** doğrulanmış bir noktada dur; §1'de aşama satırına `in_progress` ve kalan işi yaz; `NEXT_PROMPT.md`'yi aynı aşamanın devamı için yaz; adım 4'teki gibi commit et.
8. `local://` taslakları oturumlar arasında **taşınmaz**: bir taslak ya aynı oturumda tüketilir ya da depodaki bir dosyaya yazılır.

## 1. Durum tablosu

Durum sözlüğü: `pending`, `in_progress`, `done`, `blocked`.

| Pencere | Faz | Kapsam | Önkoşul | Durum | Commit / kanıt |
|---|---|---|---|---|---|
| 0 | Keşif, plan, sözleşme | O0 keşif, O1 plan (onaylandı), K8 = A (dal yeniden kuruldu), bu dosya, NEXT_PROMPT ve PROJECT_LOG güncellemesi | — | done | `70946ff`, `03b0898`, `775b321`; C0 `Window 0: orchestration plan, K8 redaction, handoff for window 1` (`git log --diff-filter=A -- ORCHESTRATION_PLAN.md`); inceleme sonrası takip commit'i `Window 0 follow-up: align handoff with plan, rename review IDs` |
| 1 | IMPL-96 uygulaması | Ledger IMPL-96 (§4–§8, `DEC-27`…`DEC-32`); README ve UNTRACKED kaymaları (T2); iki `-o` satırı (T3); inceleme; C1 | Pencere 0 | done | C1 `IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline` (`git log --grep 'IMPL-96: repository move'`); ledger 644 → 653 satır (21 satır yalnız ekleme, 9 yeni satır), geçitler taban değerde; bu dosyada §1, §3 (Adlandırma), §5.1 (W3 `:143` ve W4 `:61` hedefleri), §6 (W5, SEC ve sıra), §10, Ek A.2, A.4 notu ve A.5 (sıra) güncellendi; C1 kullanıcının gece talimatıyla, diff gösterilmeden atıldı (PROJECT_LOG §11) |
| 2 | Kapanış ve yayın | PROJECT_LOG bayat satırları (W5); push öncesi güvenlik ve içerik incelemesi; NEXT_PROMPT'u koşu 21'e hazırlama (W6); `main` FF; push; silinecek depoların ölçümü. Aşamalar §6.3 | Pencere 1; push kararı | in_progress | aşama satırları aşağıda |
| 2 · O0+O1 | Keşif ve plan | Üç scout; ölçümler (Ek A.6); keşif envanteri (§6.2); onaylı plan (§6); aşama döngüsü (§0) | Pencere 1 | done | `Window 2 O0-O1: approved plan, discovery facts, stage-per-session loop` (`git log --grep 'Window 2 O0-O1'`) |
| 2 · O2 | Kontrat | K0 (§6.3) | 2 · O0+O1 | pending | |
| 2 · O3 | Paralel uygulama | W5 ∥ SEC-A1 ∥ SEC-A2 ∥ SEC-A3 ∥ REV-3 | 2 · O2 | pending | |
| 2 · O4 | Entegrasyon ve geçitler | I2a → GATE | 2 · O3 | pending | |
| 2 · O5 | Son inceleme ve kapanış | W6 ∥ REV-1 → REV-2 ∥ SEC-B → FIX (gerekirse, sonra GATE) → I2b → C2 → FF (onay) → RID → PUSH (onay) → LSR | 2 · O4 | pending | |
| 3 | Planlama koşusu 21 | Step 1 + Step 2: Faz 7/8 emekli; K7 = (a) için faz ve alt planlar; önce K9 ve kapsam soruları | Pencere 2 | pending | |
| 4 | 12. denetim | Step 3 (`run-step3.md`) | Pencere 3 | pending | |
| 5+ | K7 = (a) Step 4 dilimleri | 12. denetimin kuyruğu; pencere başına bir dilim | Pencere 4 | pending | |

Her faz §0'daki aşamalarla yürür; bir fazın aşama satırları o fazın `O0`+`O1` oturumunda eklenir.

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
| Pencere 2 planı | Görevler, sıra, kapsam | Onaylandı (2026-11-14, "onaylıyorum"); kararlar §6.1 | — |
| Döngü | Oturum yapısı | Her aşama ayrı oturumda (`O0`+`O1` birlikte); kapanışta `NEXT_PROMPT.md` ve yerel commit sorulmadan; FF ve push ayrı onay; beklenmedik durumda sade soru (§0) | — |

## 3. Her pencerede geçerli kurallar

**Roller.**
- **Orkestratör (ana oturum):** plan, dağıtım, entegrasyon, doğrulama ve commit. Sıcak noktalar yalnız onundur: `Planner-docs/Planing-Ledger.md`, `Main-Planing.md`, `Sub-Planing-Index.md`, `Sub-Planing-Audit.md`, `Project-Ontology.md`; `CHANGELOG.md`; sürüm yerleri (`ishtar-cam-modes/module.prop`, `customize.sh`); üretilen `docs/release-manifest.md`; `.gitignore`, `.gitattributes`; `snapshots/` (kanıt, düzeltilmez); bu dosya; tüm git işlemleri.
- **Alt ajanlar:** Görev metni kendi kendine yeter (hedef dosya yolları, değişiklik, kabul kriteri, yasak alanlar). Ajan yalnız sahip olduğu dosyaya yazar; başka bir dosyada sorun görürse düzeltmez, raporlar. Doğrulayıcı, test ya da format çalıştırmaz. Dönüşte şu blok zorunludur: `status`, `changed_files`, `acceptance` (kriter / karşılandı mı / kanıt), `contract_deviations`, `open_issues`. Sıcak noktalar için yalnız taslak üretir (`local://…`).
- Aynı anda en fazla 4 uygulama ajanı çalışır. `task` aracında `isolated` ve `outputSchema` yok; yalıtım ayrık dosya sahipliğiyle sağlanır. `librarian` ve `designer` ajanları bu ortamda yok.
- **Adlandırma:** Görev kimlikleri (`W1`–`W6`, `T3`, `I1`, `REV`, `SEC`; Pencere 2 için ayrıca `K0`, `SEC-A1`–`SEC-A3`, `SEC-B`, `REV-1`–`REV-3`, `I2a`, `I2b`, `GATE`, `FIX`, `RID`, `PUSH`, `LSR`), aşama kimlikleri `O0`–`O5` ve Ek A olgu kimlikleri (`G`, `D`, `V`, `REL`, `T3`, `TRAP`, `M1`, `E`, `AUD11`, `OPN`; A.6'da `OPN2`, `G4b`, `G8b`, `L653`, `LSH`, `SH8`, `CDATE`, `RID0`, `SEC0`, `SMK-O`) yalnız bu plana aittir. Main-Planing risk kimlikleri `R1`–`R12`, kararlar `K1`–`K9` ve `DEC-NN`, kontrol listesi `C-NN`, ClaudeQB `Faz n.m` / `Fn.m-NN` ile karışmasın diye böyle seçildi (önceki oturumun `R21` → `RUN21` düzeltmesiyle aynı gerekçe). Ek A'daki `K3` ve `K4` satırları ise karar etiketlerini bilerek yeniden kullanır; plana özgü değildir. `C1` ve `C2` faz kapanış commit'leridir; Pencere 2'nin aşama commit'leri başlıklarıyla anılır (§6.4).

**Geçitler** (fazın belirttiği aşamada bir kez, orkestratör; Pencere 2'de `O4`, düzeltme olursa `O5`'te yeniden):
- `py -3 C:/Users/ahmet/.claude/plugins/cache/claudeqb/claudeqb/0.2.1/skills/claudeqb/scripts/validate_planner_docs.py --root . --mode all` → `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0`. Koşu 21 alt plan sayısını, 12. denetim de bulgu sayılarını değiştirir; yeni baseline o fazda yazılır.
- Aynı komut `--mode step4 --strict` ile: yalnız bilinen `strict_warning` hatası (baseline, regresyon değil).
- `py -3 scripts/build-release.py --self-test` → `SELF-TEST: PASS`, VAL-BUILD2 sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0`. Bayraksız çalıştırma `dist/` zip'ini ve `docs/release-manifest.md`'yi yeniden yazar; sürüm prosedürü dışında çalıştırılmaz.
- Dokunulan dosyalarda bayt kontrolü (CRLF/LF sayısı, NUL) ve tablo boru sayıları; `git diff --stat` ile sahiplik kontrolü.

**Bayt kuralları.** Ledger, `Main-Planing.md` ve `Autopsy.md` CRLF; diğer her şey LF. Satır sonu dönüştürme yapılmaz. `Project-Ontology.md`'de 2 NUL bayt var; grep orada sessizce sonuç vermeyebilir. CRLF bir dosyada ilk `edit`ten sonra bayt sayımıyla CRLF'nin korunduğu doğrulanır; korunmuyorsa durulur. Ledger satırları 1–9 KB'tır (en büyüğü ≈ 8,8 KB): değişen satır baştan sona yeniden yazılır, uygulamadan sonra her değişen satır için difflib ile "yalnız ekleme" kontrolü yapılır (kopyalama hatasını yakalar). Bilinen tek istisna, IMPL-96'da beş §4 satırının `Updated At` hücresidir.

**Gizlilik.** Probe snapshot'ının redaksiyondan önceki IMEI ve `persist.sys.miui.sno` değerleri hiçbir dosyaya, rapora ya da mesaja yazılmaz; kontroller maskeli yapılır. Redaksiyonsuz özgün yalnız depo dışındaki `../ishtar-arsiv/impl-96-unredacted.bundle`'da ve yerel reflog'da durur. Başka cihazların seri numaraları kayda geçmez.

**Git.** Aşama kapanış commit'i beklenmedik durum yoksa onay sorulmadan atılır (§0 adım 4; kullanıcı kararı, 2026-11-14); mesaj fazı ve aşamayı adlandırır. Başka her commit kullanıcı onayıyla atılır. `main`'in fast-forward'ı ve her push ayrı onay ister. Geçmiş yeniden yazılmaz; K8 tek kayıtlı istisnadır. Push yalnız açık refspec ile yapılır: `git push origin main integrate/impl-96`; `--all` ve `--mirror` asla. Push'tan sonra `git ls-remote origin` ile hash karşılaştırılır. Geçmiş GitHub MCP dosya araçlarıyla gönderilmez.

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
| REV ∥ SEC | reviewer ∥ security-reviewer | C1 adayı diff: olgu doğruluğu (Ek A, snapshot'lar), biçim, kapsam taşması; sır, kimlik, sunucu adresi | salt-okur | P0/P1 yok. Varsa ledger'ı orkestratör, diğer dosyaları düzeltici task düzeltir; geçitler yeniden çalışır |

**Sıra:** W1 ∥ W2 ∥ W3 ∥ W4 (ve T3) → I1 → geçitler → REV ∥ SEC → düzeltmeler → kapanış.
**Kapanış (§0.4):** tek commit C1 `IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline`: ledger, `README.md`, `UNTRACKED-BY-DESIGN.md`, `docs/release-checklist.md`, `docs/agc-12mp-configuration.md`, bu dosya (§1'de Pencere 1 `done`, C1 başlığıyla), `PROJECT_LOG.md` (§11'e kısa girdi) ve Pencere 2 için yeniden yazılan `NEXT_PROMPT.md`. Onayla commit edilir.

### 5.1 W3 ve W4 hedef tabloları

Yerler alıntılanan metinle bulunur (satır numaraları 2026-11-13 ağacına aittir). Hedef metin İngilizce yazılır; olgular Ek A'dadır (kaynak sütunu).

**W3 — `README.md`**

| Yer | Şu an | Hedef | Kaynak |
|---|---|---|---|
| :3-5 | "… and an AOSPA Android 16 track." | Cümle kalır; eklenir: Android 16 izi 2026-11-13'te bırakıldı (`DEC-28`); telefon HyperOS 4'te ve projenin hiçbir modülü kurulu değil | A.1 DEC-28; D1, D7 |
| :18 | "Source at v2.1 / versionCode 12." | "Source at v2.2 / versionCode 13." | REL |
| :19 | "Standalone module symlinking `aon_front.pb` into `/vendor`." | Modül `/vendor/lib64/camera`'yı kopyalar, `aon_front.pb`'yi ekler ve dizini bind-mount eder; dosya zaten varsa çıkar (HyperOS 4 bunu kendisi sağlıyor) | E3, D6 |
| :20 | "two smali sources, the experimental HAL patch table, and the reproduction recipe" | Gerçek içerik | E4 |
| :24-30 Documentation | Kök belgeler için satır yok; `docs/` satırı iki dosya sayıyor | `PROJECT_LOG.md`, `NEXT_PROMPT.md`, `ORCHESTRATION_PLAN.md` (Türkçe süreklilik belgeleri) ve `CHANGELOG.md` (modül sürüm notları) satırları; `docs/` = 18 belge (biçim, prosedür, kanıt, runbook) | E5 |
| :75-81 sürüm tablosu | v2.1 "Most recent, and currently installed on device `dc27e5d0`…" | v2.1 → v2.2 ile aşıldı. Tablo altına: `dist/` (`*.zip` ile dışlanır) `scripts/build-release.py` çıktılarını tutar: v2.2 (AOSPA A15'e IMPL-81 ile kuruldu) ve kökteki v2.1 zip'inden farklı bir IMPL-76 v2.1 derlemesi; HyperOS 4'te proje modülü kurulu değil | REL, E6, D7 |
| :142 | "`scripts/` … `smoke.sh`, the read-only device state snapshot." | `build-release.py` (deterministik sürüm derleyici, `--self-test`) eklenir | ModuleMap; V3 |
| :143 | "`<UTC yyyymmdd-HHMM>__<subplan>__<label>.txt`" | Ad, operatörün yazdığı saati taşır ve güvenilmez (bazı dosyalarda UTC, bazılarında UTC+3); başlıktaki `taken` satırı UTC'dir ve esastır (inceleme düzeltmesi; ilk hedef yalnız "UTC+3" diyordu) | E7 |
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
| :61 | "Rebuild from the tagged tracked source. **Faz 1.2 audits these five archives …**" | Bayt bayt yeniden üretilemez: geçmiş v2.1'de (`ff6934e`) başlar, v1.0/v1.9/v2.0'ın kaynağı depoda yok; `scripts/build-release.py` yalnız `ishtar-cam-modes`'u paketler ve `dist/`'teki v2.1 derlemesi (IMPL-76) kökteki arşivden farklıdır; etiket yok; arşivler saklanır. Faz 1.2 denetimi temiz kapandı (`DEC-05`, IMPL-02, 2026-08-24). İnceleme düzeltmesi: ilk hedef "izlenen kaynaktan `scripts/build-release.py` ile derlenir" diyordu | E2, E6, E8; `git show ff6934e:ishtar-cam-modes/module.prop` → `version=v2.1`; `scripts/build-release.py:50` (`MODULE_DIR`), 2026-11-13 |
| :63 | "Transient tooling output. Not needed; content quoted in section 1 above." | 2026-11-13'te silindi (K4); içerik `PROJECT_LOG.md` §2.1'de | K4 |
| :89 | "… is the `Faz 1.2` audit and open decision `DEC-05`." | Yanıtlandı: beş arşivin hiçbirinde keystore yok; `DEC-05` 2026-08-24'te temiz kapandı (IMPL-02) | E2 |
| :128-132 | "This repository is **local-only**. No remote is configured, and adding one is open decision `DEC-01` …" | 2026-09-10'dan beri özel remote (`DEC-01`, IMPL-90: `ahmetxa/ishtar`); 2026-11-13'ten beri `origin` = özel `ahmetxa/ishtar_cam_modes` (`DEC-27`), geçmiş aynı hash'lerle; önce `DEC-05` temizlendi; `snapshots/` tam çözünürlüklü çekimler taşıdığı için remote özel kalır | G3, G4, E9 |
| §4 Regenerable Module Artifacts | `ishtar-cam-modes/candidates/*.bin` için satır yok | Satır eklenir: Faz 5.1 aday blob'u (`dcgB-m0-12bit.bin`), `ishtar-cam-modes/tools/mode0_12bit.py` ile yeniden üretilir; hiçbir mod geçişi kanıtlanmamış bir varyantı seçemesin diye `blobs/` dışında tutulur (`.gitignore:56-58`) | E10 |

## 6. Pencere 2 — Kapanış ve yayın

**Hedef:** Oturum belgelerinin bayat satırlarını temizlemek, push edilecek her şeyi incelemek, NEXT_PROMPT'u koşu 21'e hazırlamak, dalı yayınlamak.
**Önkoşul:** Pencere 1 `done` (C1 var).
**Durum:** `in_progress`. `O0`+`O1` 2026-11-14'te bitti: üç scout, ölçümler (Ek A.6), keşif envanteri (§6.2); kullanıcı planı varsayılan kararlarla onayladı ("onaylıyorum", 2026-11-14; §6.1). Kalan aşamalar §6.3'te, her biri ayrı oturumda (§0).
**Sabitler:** Pencere 2 cihaza komut göndermez ve ledger'a yazmaz (`DEC-30` yürütme notu koşu 21'de). Ek A.4 çapaları Pencere 1'e aitti; ledger artık 653 satır (Ek A.6 `L653`, `LSH`).

### 6.1 Kararlar (2026-11-14, kullanıcı onaylı)

| # | Konu | Karar |
|---|---|---|
| 1 | W5 kapsamı | (a) Geniş: plandaki W5 maddeleri ve aynı sınıftan, C1, `03b0898` ve Pencere 1'in sonucu yüzünden eskiyen her şey (§6.2). AOSPA dönemi anlatısı silinmez: şimdiki durum iddiası olan cümle düzeltilir, tarihsel cümleye tarihli not eklenir |
| 2 | Plan §7 | (a) Koşu 21 tuzakları ve keşif düzeltmeleri §7'ye, yeni bulgular §10'a yazılır; yeni sorular Pencere 3'ün açılış sorularına eklenir (K0, `O2`) |
| 3 | İnceleme düzeni | (a) SEC-A1–A3 ve REV-3 `O3`'te W5 ile paralel; REV-1, REV-2 ve SEC-B `O5`'te |
| 4 | C1 bulguları (REV-3) | (a) Ledger bulguları §10'a (koşu 21); öteki dosyalardaki bulgular düzeltici task ile sonraki kapanış commit'ine; amend yok |
| 5 | Kimlik kontrolünün yorumu | (a) Değer taşıyan satır (`[anahtar]: [değer]`, `anahtar=değer`, `anahtar: değer`) `<redacted>` olmalı; anahtarı yalnız düzyazıda anan satır sayılır ve raporlanır ama hata sayılmaz (Ek A.5) |
| 6 | Sonuç cümleleri | Yalnız sonuç varken yazılır: I2a (`O4`) o anda bilinen olguları, I2b (`O5`; FIX ve GATE'ten sonra, C2'den hemen önce) geçit değerlerini ve SEC/REV hükümlerini yazar. I2b farkı ayrıca bayt/boru kontrolünden ve kimlik taramasından geçer (danışman notu, 2026-11-14) |
| 7 | Aşama döngüsü | §0. `NEXT_PROMPT.md` her aşama sonunda yeniden yazıldığı için koşu 21 devri (W6) `O5`'e taşındı ve C2'ye girer |

### 6.2 Keşif envanteri (`O0`, 2026-11-14, ağaç `9ee505f`)

W5'in `PROJECT_LOG.md` iş listesi. Yerler alıntıyla bulunur; satır numaraları `9ee505f` ağacına aittir ve K0 (`O2`) betikle yeniden doğrular. Alıntılar “…” içindedir. Son sütundaki kimlikler Ek A.1, A.2 ve A.6'dadır. §2.6 ve §11'e W5 dokunmaz (§0 adım 4).

| Yer | Şu an (alıntı) | Güncel olgu → hedef | Kaynak |
|---|---|---|---|
| §1 `:9` | “Bu belgedeki ölçümlerin hepsi telefonda AOSPA Vauxite (Android 15) ve KernelSU Next varken yapıldı”; “**2026-11-13 kullanıcı beyanı (ölçülmedi):**” | 2026-11-13'ten önceki ölçümler AOSPA A15'te; HyperOS 4 2026-11-13'te gözlendi ve aynı gün salt-okur ölçüldü (`70946ff`, §2.3). “Çinli bir geliştiricinin portu” kullanıcı beyanı olarak kalır | D1–D3, OPN |
| §1 `:15` | “İkisi de herkese açık; henüz hiç derlenmedi” | Derleme bırakıldı (`DEC-28`); iki depo silinecek (`DEC-30`), 2026-11-14'te hâlâ duruyor | G8b |
| §1, §2.3 `:14`, `:127`, `:131`, `:132` | “L:638”; “L:640”; “L:642” | `L:647`; `L:649`; `L:651` | LSH |
| `:3`, §2 `:43` | “Durum tarihi **2026-11-13**”; “## 2. Şu an neredeyiz (2026-11-13)” | Yazım tarihi | — |
| §2.1 `:46` | “sonra C0 (`ORCHESTRATION_PLAN.md`'yi ekleyen commit)” | C0 `b603516`, C0 takip commit'i `c2abd46`, C1 (başlıkla) ve Pencere 2 aşama commit'leri (başlıklarıyla); yazım anındaki commit sayıları | OPN2 |
| §2.1 `:47` | “`DEC-27` atandı; ledger'a Pencere 1'de yazılır” | Ledger §8 `:605` | L653 |
| §2.1 `:49` | “`7fa0a51` ve `integrate/impl-96` dalı push edilmedi. Push Pencere 2'de karara bağlanır” | Yazım anındaki push durumu; push `2 · O5`'te, ayrı onayla | G4b |
| §2.1 `:52` | “Ölçüm (2026-11-13, `gh api`): üç depo da hâlâ var.” | 2026-11-14T07:23:21Z: üçü de 200 (I2a yeniden ölçer) | G8b |
| §2.1 `:54` | “344 izlenen dosya.” | 350 | OPN2 |
| §2.1 `:60` | “düzeltmesi IMPL-96'da.” | IMPL-96 notları yazıldı (ledger `:100`, `:552`, `:554`, `:556`, `:558`) | LSH |
| §2.1 `:61` | “IMPL satırı hâlâ yok (IMPL-96)” | IMPL-96 satırının (4). maddesi kaydediyor (ledger `:525`) | L653 |
| §2.1 `:63`, `:64` | “son sürüm C0'dadır”; “C0 (`ORCHESTRATION_PLAN.md`, bu günlük ve `NEXT_PROMPT.md`'yi taşıyan commit) işlendi” | Sonraki sürümler `c2abd46`, C1 ve Pencere 2 aşama commit'lerinde; C0 = `b603516` | OPN2 |
| §2.1 `:67` | “(47 commit, 225 dosya, remote yok) bayattır (§8)” | IMPL-96 notuyla düzeltildi (ledger `:528`) | LSH |
| §2.2 `:83` | “cihazda kurulu v2.2 ile bayt-özdeşliği bozar” | v2.2 AOSPA A15'te kuruluydu; HyperOS 4'te proje modülü kurulu değil | D7 |
| §2.3 `:98` | “(yamasız APK'da bu anahtar yok)” | Anahtar prefs dosyasında yok; APK'da olup olmadığı ölçülmedi | D9; §10 |
| §2.3 `:104` | “(DEV; salt-okur adb; ledger'a işlenmedi)” | IMPL-96 satırının (4). maddesi kaydediyor | L653 |
| §2.4 `:147` | “Ledger §5'te IMPL-01 … IMPL-95 kayıtlı” | IMPL-96 de kayıtlı (`:525`) | L653 |
| §2.4 `:165` | “**Sıradaki numaralar:** `IMPL-96`”; “(Pencere 1'de ledger'a yazılacak)” | Sıradaki `IMPL-97`; `DEC-27`…`DEC-32` ledger'da (`:605`–`:610`); sonraki `DEC-33` | L653 |
| §2.4 `:166` | “Pencere 1'de ledger'a işlenecek” | Konusuz notları ledger'da (`:582`, `:583`, `:599`, `:601`, `:603`, `:604`) | LSH |
| §2.5 `:174` | “(`DEC-28` atandı; ledger'a Pencere 1'de yazılır)” | Ledger `:606`; §7 üst girdisi `:550` | L653 |
| §2.5 `:176` | “L:549”; “L:598-601” | `L:552`; `L:601-604` | LSH |
| §2.5 `:217` | “(PRP:231-246)” | `PRP:239-254` | SH8 |
| §2.5 `:220` | “`DEC-07` açık” | Tarihli not: 2026-11-13'ten beri konusuz (`DEC-28`); `:174` bölümün kalanını tarihsel sayar | A.1 |
| §2.6 `:228`–`:240` | “### 2.6 Bu oturumun durumu (Pencere 0, 2026-11-13)” | W5 dokunmaz; orkestratör `O4`'ten itibaren (I2a) aşama kapanışlarında günceller | §0 |
| §3.1 `:289` | “etkisi `Faz7.3`'te doğrulanacak” | Tarihli not: `Faz7.3` amaçsız (`DEC-28`) | AUD11 |
| §3.1 `:292` | “henüz kiralama yapılmadı” | Kiralama hiç yapılmayacak (`DEC-28`) | A.1 |
| §3.1 `:294` | “kuyruğun başında” | 11. denetimin kuyruğu 2026-11-13'ten beri geçersiz | AUD11 |
| §3.2 `:407` | “IMPL-96 (devam ediyor)”; “Ledger satırı Pencere 1'de yazılacak”; “ledger satırı yazılmadı”; kanıt “§2.6, §11” | Tamamlandı; kanıt `L:525` ve C1 (başlıkla), IMPL-95 satırının biçiminde | L653 |
| §3.3 `:440` | “`DEC-26`: `Faz7.2` Scaleway'e taşındı; snapshot kesilmedi; commit edilmedi” | `7fa0a51`'de commit edildi | G1 |
| §3.3 `:454` | “PRP:41, PRP:62” | `PRP:49`, `PRP:70` | SH8 |
| §3.3 `:455` | “PRP:105” | `PRP:113` | SH8 |
| §3.3 `:456` | “`-52/53/54` kapandı, `-55/56/57` yeni açıldı; commit edilmedi” | `7fa0a51`'de commit edildi | G1 |
| §3.5 `:494` | “Dal `main`'deki 62 commit”; “`origin/main`'den sonraki dört commit push edilmedi (§2.1)” | Liste `origin/main`'deki (`587e3b5`) 62 commit'tir (yerel `main` 63); ardından yazım anındaki push durumu | G4b |
| §3.5 (yeni gruplar) | — | **2026-11-13 (6):** `7fa0a51`, `70946ff`, `03b0898`, `775b321`, `b603516`, `c2abd46`; **2026-11-14:** C1 (başlıkla) ve Pencere 2 aşama commit'leri (başlıklarıyla); konu satırları `git log --reverse` çıktısından | CDATE |
| §3.5 `:574` | “*(origin/main)*” (`f8a05ca` satırı) | Tarihli not: eski remote'un (`ahmetxa/ishtar`) ucuydu | G6 |
| §3.5 `:577`, `:578`, `:581` | “*(push edilmedi)*” | Not kalkar: `587e3b5`'e kadar hepsi push edildi | G4b |
| §3.5 `:582` | “*(HEAD, push edilmedi)*” | “*(origin/main)*” | G4b |
| §4 `:584` | “## 4. Kararlar (DEC-01 … DEC-26)” | `DEC-01 … DEC-32` | L653 |
| §4 `:586` | “(satır :569–:601;” | §8 başlığı `:572`, satırlar `:576`–`:610` | L653 |
| §4 `:588` | “**Açık kararlar (2026-11-13):**”; “Kalan 23 kararın hepsi yanıtlandı ya da kapandı” | Açık: `DEC-09` (koşullu) ve K9 (henüz DEC yok); `DEC-07`, `DEC-08` konusuz (`DEC-28`); kernel-upstream iddiası düştü (K3); toplam 32 karar | A.1, K3 |
| §4 `:592`, `:593` | DEC-07 ve DEC-08 satırlarındaki “**AÇIK**” (ikişer) | Konusuz (`DEC-28`); ledger `:582`, `:583` | A.1 |
| §4 `:592`–`:617` | `ledger:573`…`ledger:601` hücreleri | Her biri +3; örnek DEC-09 `:584`, DEC-01 `:602`, DEC-26 `:604` | LSH |
| §4 `:595` | DEC-01 satırı | 2026-11-13 güncellemesi (`DEC-27`): depo `ahmetxa/ishtar_cam_modes`; ledger `:602` | A.1 |
| §4 `:613`, `:615`–`:617` | DEC-22, DEC-24, DEC-25, DEC-26 durum hücreleri | Konusuz (`DEC-28`); `:617`'de `docs/build-environment.md:118-130` → `:126-138` | A.1, SH8 |
| §4 (yeni satırlar) | — | `DEC-27`…`DEC-32` satırları (Ek A.1; ledger `:605`–`:610`) | A.1 |
| §4 `:619` | “ledger'a IMPL-96 ile (Pencere 1) yazılacak” | Yazıldı (`:605`–`:610`) | L653 |
| §4 `:623`, `:624`, `:627`, `:628`, `:629` | “ledger'a Pencere 1'de yazılır”; “Pencere 1'de yazılacak” | Yazıldı | L653 |
| §4 `:631` | “ledger'a Pencere 1'de işlenecek” | İşlendi | LSH |
| §4 `:633` | “ledger satırı Pencere 1'de” | Yazıldı (`:525`) | L653 |
| §4 `:634` | “Pencere 2'de sorulur” | `2 · O5`'te, ayrı onayla | §6.4 |
| §5.1 `:642` | “ledger:638–:642” | `:647`–`:651` | LSH |
| §5.2 `:656`; §5.3 `:669` | “ledger:586” | `:589` | LSH |
| §5.2 `:657` | “ledger:632” | `:641` | LSH |
| §5.2 `:663` | “ledger:629” | `:638` | LSH |
| §5.3 `:677` | “ledger:598, :601” | `:601`, `:604` | LSH |
| §5.4 `:691` | “HAL yama tablosunun HyperOS 4'te geçerliliği ölçülmedi” | HyperOS 4 HAL'i farklı (`2a955e68…`, 2026-11-13'te ölçüldü): tablo uymaz ve HAL koruması kapalı başarısız olur [ÇIKARIM, M1]; yeniden türetme K9 | D4, M1 |
| §6 `:695` | “README:143 ve Faz3.7:71 UTC diyor” | README C1'de düzeldi (`:153`); `Faz3.7:71` sürüyor (§10, koşu 21) | E7 |
| §6 `:732` | “snapshot'ı da IMPL satırı da yok” | IMPL-96 satırı kaydediyor; snapshot yok | L653 |
| §7 `:749` | “:165 yol hatası” | C1'de düzeldi (T3) | T3 |
| §8 `:781` | “11. denetim "outstanding"”; “commit edilmedi” | Ledger `:100` ve `:552`'de IMPL-96 notları; `7fa0a51`'de commit edildi | LSH, G1 |
| §8 `:783` | “Step 3 yeniden denetimi "outstanding"” | Kısmen çözüldü: eski `:551`, `:553`, `:555` artık `:554`, `:556`, `:558` ve notlu; `:51`, `:57`–`:60` ve `:589` notsuz (§10, koşu 21) | LSH |
| §8 `:784` | “47 commit, 225 dosya, remote yok”; “62 commit, 344 izlenen dosya, `origin` var, 4 commit ileride” | Çözüldü (ledger `:528`); güncel: `origin/main` `587e3b5` (62), `main` 63, dal 69 ve aşama commit'leri, 350 dosya | OPN2, G4b |
| §8 `:781`–`:793`, `:809`, `:810`, `:817`–`:820` | ledger satır atıfları | Kaymaya göre | LSH |
| §8 `:795`, `:796`, `:804`, `:806` | UNTRACKED “`:61`” ve “`:63`” atıfları | C1 öncesi numara; içerikle yeniden eşlenir (UNTRACKED `:59`, `:61`) | C1 |
| §8 `:811` | “`docs/pre-rental-plan.md:32`, `:233-234`, `:252-253`”; “PRP:31,122,181,205” | `:40`, `:241-242`, `:260-261`; `PRP:39,130,189,213` | SH8 |
| §8 `:812` | “sonuç `snapshots/snapshots/…` olur” | Çözüldü (C1, T3); anlatı düzeltilir: dizin olmadığı için dosya yazılmaz, betik yine `stored:` basar [ÇIKARIM] | SMK-O |
| §8 `:816` | “`devir-teslim-promptu.md:247`” | Dosya 2026-11-13'te silindi (K4) | K4 |
| §8 `:822` | README satırı (“`README.md:18`, `:19`, `:20`, `:77-78`, `:142`, `:143`, `:186`”) | Çözüldü (C1): README `:20`, `:21`, `:22`, `:85-86`, `:94`, `:152`, `:153`; Exclusions satırı kaldırıldı | C1 |
| §8 `:823` | UNTRACKED satırı; “344 dosya”; “ledger:576, :599” | Çözüldü (C1); 350; `:579`, `:602` | C1, LSH |
| §8 `:827` | “`DEC-27` IMPL-96'da kaydedilecek”; “`pre-rental-plan.md:250`” | Kaydedildi (`:605`; DEC-01 `:602`); `:258` | L653, SH8 |
| §8 `:828` | “`README.md:144`; `UNTRACKED-BY-DESIGN.md:38-41`, `:63`” | Çözüldü (C1): UNTRACKED `:38`–`:39`, `:61`; README satırı kaldırıldı | C1 |
| §8 `:829` | “Telefon AOSPA A15 + KernelSU Next”; “kullanıcı beyanı: HyperOS 4 portu, kernel 5.15.215; ölçülmedi” | 2026-11-13'te ölçüldü (`70946ff`; ledger §6 `:532`; DEV `:223`–`:244`) | D1–D11 |
| §8 `:848` | “**README / UNTRACKED-BY-DESIGN:**” maddesi (T2) | Çözüldü (C1) | C1 |
| §8 `:849` | “`:165` yol hatası düzeltilmeli (T3)” | T3 C1'de düzeldi; maddenin geri kalanı sürer | T3 |
| §8 `:850` | “IMPL-96'nın kapsamı §2.6'daki L biriminde” | Yapıldı (`:525` ve ledger §6–§8 notları) | L653 |
| §9 `:863` | “Çözüldü; v2.2 kurulu (VAL-INSTALL)” | AOSPA A15'te kuruluydu; HyperOS 4'te kurulu değil | D7 |
| §9 `:865` | “Dosyalar farklıysa 16 noktalı tablo ve sensör varyantları uymaz; ölçülmedi (`NEXT_PROMPT.md` §4.3)” | HAL farklı (`2a955e68…`), sensör aynı (`EXPECT_MD5`), 2026-11-13'te ölçüldü; K9 karar verir (plan §2, §7); NEXT_PROMPT bölüm atfı kalkar | D4, D5 |
| §9 `:874` | “`origin`'de 62 commit var; `7fa0a51` ve `integrate/impl-96` push edilmedi.” | Yazım anındaki push durumu; push `2 · O5`'te | G4b |
| §9 `:875` | “**N4 Ledger geride:**” | Çözüldü (IMPL-96) | L653 |
| §9 `:878` | “2026-09-20 oturumunun kaydı yok (süreklilik boşluğu); IMPL-96 kaydeder.” | Kaydedildi (`:525`, madde 4) | L653 |
| §10 `:885` | “sıradaki **IMPL-96**” | `IMPL-97` | L653 |
| §10 `:888` | “ledger'a Pencere 1'de yazılacak” | Yazıldı (`:605`–`:610`) | L653 |
| §10 `:923` | “md5 `ce65f862…`” | AOSPA dönemindeki yamalı derleme; HyperOS 4'te yamasız `fa4066eb…` | D9 |
| §10 `:932`–`:934` | barista, `fixes.diff` ve Teardown maddeleri | Tarihli not: Faz 7 işi `DEC-28` ile tarihsel | A.1 |

**`O2` girdileri** (K0 bunları §7'ye ve §10'a işler; kaynak `W6Window3Inputs` scout raporu, 2026-11-14):
- **§7 düzeltmeleri:**
  - `:159`'daki AUDIT-FIX eşlemesi: Hetzner satırlarını (`Main-Planing.md:75`, `:211`, `:265`) yalnız `AUDIT-FIX-57` kapsar (`Sub-Planing-Audit.md:380`); `-41` §8 adım 5'tir (`Main-Planing.md:277`; Audit `:383`), `-42` `:22`, `:61` ve `:288`'dir (Audit `:384`). "Emekli bölümlerle birlikte kapanır" yalnız `:211` için doğrudur; `:75` (§3) ve `:265` (R9) ayrı düzenleme ister.
  - `AUDIT-FIX-57` ayrıca `Project-Comprehension.md` EV-20 (`:51`) ve CQ-13 (`:25`) ile `docs/reverse-engineering-toolchain.md:220`'yi kapsar. İlki §3'teki sıcak nokta listesinde yok; ikincisi `Planner-docs/` dışında, Step 1 ve Step 2'nin yazma sınırının ötesinde.
  - Seçenek (ii) "Faz 7 ve 8 emekli" ile çelişir: Faz 8'in kamera yarısı sürerse Faz 8 ancak kısmen emekli olur; başlığı (`Main-Planing.md:221`) ve yol haritası satırı (`:126`) yeniden yazılır.
  - Faz 6: ledger `:98` "VAL-BUILD still deferred to Phase 7 by design" diyor, Index `:177` doğrulamayı Faz 7'ye bağlıyor; §7 yalnız `Faz6.1`'i anıyor.
  - ClaudeQB süreci: Step 1 için handoff dosyası yok (yalnız `run-step2.md`, `run-step3.md`, `run-step4.md`); Step 1 yalnız `Main-Planing.md`'yi yazar (`First-Planner.md:10-11`, `:363-364`); Step 2 `Main-Planing.md`'yi düzenleyemez (`Second-Planner.md:61`); ikisinin aynı oturumda yapılması kullanıcının açık isteğini gerektirir (`SKILL.md:11`, `workflow-quality.md:120`); `run-step2.md:27` tam ayrıştırma ister, koşu 21 ise sınırlıdır (koşu 12–15, 19, 20 emsali); `/claudeqb:claudeqb` komutunu Claude Code'da kullanıcı yazar (`SKILL.md:4`, `disable-model-invocation: true`); omp altında dosyalar mutlak yolla okunur, doğrulayıcı `py -3 <mutlak yol>` ile çalışır.
- **§7 tuzakları (`validate_planner_docs.py`):**
  - Yol haritasından Faz 7/8 satırını silmek ya da ilk hücreyi `~~7~~` yapmak `extra_phase_folder_without_main_phase` üretir (`:163`, `:1011-1013`); `--strict` bunu hataya çevirir (`:1286-1290`).
  - `superseded` satırı dolu `Superseded By` ister (`:848-849`); ledger'daki ilgili §4 satırlarında bu hücre bugün `-`.
  - Denetim durumu dosyadaki ilk `status:` eşleşmesinden okunur (`:1071-1078`); bugün `Sub-Planing-Audit.md:18`.
  - Seçenek (i): klasörü olmayan yeni `10` yol haritası satırı `--strict` olmadan da hatadır (`missing_phase_folder`, `:1010`), ardından `phase_has_no_subplans` (`:1039`); Step 1 ile Step 2 arasında yalnız `--mode step1 --strict` anlamlıdır.
  - H1 düzeni yalnız `—` ya da `-` kabul eder (`:165`; en dash `–` hatadır); dosya adı küçük harfli kebab-case olmalı (`:157`); uygulama sözleşmesinde `Validation Command IDs` `-` ya da `none` olamaz; 160 karakterden uzun `## 3.`/`## 7.` gövdeleri üç ya da daha çok dosyada tekrar ederse uyarı verir (`:1046-1049`; strict'te hata).
  - Dosyası olmayan alt plana ledger §4 satırı `missing_ledger_subplan` üretir (`:830`): satırlar Step 2 dosyaları yazdıktan sonra eklenir. §4 tablosundaki boş satır sonraki satırların okunmasını sessizce durdurur (`:404-430`).
  - `--mode step4 --strict` 11. denetimin geçersiz kuyruğuna karşı yine geçer: Pencere 4'ten önce Step 4 başlatılmaz.
- **§10'a yeni bulgular:**
  - §10'daki ledger satır atıfları ve Ek A.4 çapaları C1 öncesine göre numaralı; güncel karşılıkları `LSH` ile (örnek: `:575` → `:578`, `:582-583` → `:585-586`, `:586` → `:589`, `:633` → `:642`).
  - `Main-Planing.md` ve Ontology değişmez 11 Hetzner'i hâlâ anıyor; bu, `DEC-26`'dan (Scaleway) beri zaten bayattı.

### 6.3 Aşamalar ve görevler

| Aşama | # | Ajan | Hedef ve kapsam | Yazma yetkisi | Kabul kriteri | Bağımlı |
|---|---|---|---|---|---|---|
| `O2` | K0 | orkestratör | Kontrat: (1) §6.2'deki her alıntıyı ve satır numarasını betikle doğrula, tutmayanı düzelt (alıntı hiç yoksa ya da iddia yanlışsa maddeyi gerekçesiyle çıkar); (2) W5'in yazım kurallarını yeni §6.5'e yaz (tarihli not biçimi, §8'de çözülen satırların işaretlenmesi, §3.5 grupları, §4'e eklenecek satırlar, atıf kuralları); (3) §6.2'deki `O2` girdilerini §7'ye (düzeltmeler, tuzaklar, yeni açılış soruları) ve §10'a işle; (4) Pencere 2 alt ajan ortak bağlamını §6.5'e yaz (olgu kaynakları, dil ve bayt kuralları, kimlik ve atıf kuralları, sahiplik, dönüş bloğu) | `ORCHESTRATION_PLAN.md` | LF, CR 0, NUL 0, tablo boruları sabit; her olgu Ek A'da ya da o oturumda ölçülmüş; ledger, `Planner-docs/`, `docs/` ve `PROJECT_LOG.md` §1–§10 dokunulmamış | `2 · O0+O1` |
| `O3` | W5 | task `ProjectLogUpdate` | §6.2 envanteri, K0'ın yazdığı §6.5 kurallarıyla | `PROJECT_LOG.md` §1–§10 (§2.6 hariç) | Türkçe, LF, CR 0; kimlik değeri yok; ledger ile çelişki yok; değişen her cümlenin alıntı çapası tek; bölüm numaraları ve başlık sırası korunur; NEXT_PROMPT'a yalnız adıyla atıf; §2.6 ve §11'e dokunulmaz | K0 |
| `O3` | SEC-A1 | security-reviewer | `origin/main..HEAD` (oturum açılışındaki HEAD), `git log -p` ara hâller dahil: `snapshots/`, `docs/`, `README.md`, `UNTRACKED-BY-DESIGN.md` | salt-okur | P0/P1 yok: sır, Luhn adayı, `dc27e5d0` dışında seri numarası, sunucu adresi | K0 |
| `O3` | SEC-A2 | security-reviewer | Aynı aralık: `Planner-docs/` | salt-okur | Aynı | K0 |
| `O3` | SEC-A3 | security-reviewer | Aynı aralık: `PROJECT_LOG.md`, `NEXT_PROMPT.md`, `ORCHESTRATION_PLAN.md` ve commit üstverisi | salt-okur | Aynı | K0 |
| `O3` | REV-3 | reviewer | C1 diff'i, yalnız ledger, `README.md`, `UNTRACKED-BY-DESIGN.md` ve `docs/`: Ek A'ya karşı olgu doğruluğu, biçim, kapsam | salt-okur | P0/P1 yok; bulgular karar 4'e göre | K0 |
| `O4` | I2a | orkestratör | W5 sahiplik kontrolü (`git diff --stat`, yalnız §1–§10); §2.6'yı güncel aşamaya göre yaz; depoları `gh api` ile yeniden ölç; `O3` bulgularının nereye yönlendirildiğini kaydet | `PROJECT_LOG.md` §2.6 ve §11, `ORCHESTRATION_PLAN.md` | W5 dışı değişiklik yok; o anda bilinmeyen sonuç yazılmaz | `O3` |
| `O4` | GATE | orkestratör | §3 geçitleri: doğrulayıcı `--mode all` ve `--mode step4 --strict`, `--self-test`, bayt/NUL/boru | — | V1–V3 taban değerde | I2a |
| `O5` | W6 | task `HandoffRewrite` | `NEXT_PROMPT.md`'yi Pencere 3 · `O0`+`O1` (koşu 21) için yaz: §0 döngüsü; K9 ve §7'deki açılış soruları başta; koşu 21 tuzakları; Pencere 2 sonucu; push'un C2'den hemen sonra onayla yapılacağı ve Pencere 3 açılışında `git ls-remote origin` ile doğrulanacağı | `NEXT_PROMPT.md` | Türkçe, LF; plan §0, §3 ve §7 ile tutarlı; kimlik değeri ve C2 hash'i yok; PROJECT_LOG'a yalnız bölümle atıf | `O4` |
| `O5` | REV-1 | reviewer | `PROJECT_LOG.md`'nin son hâli: W5 değişiklikleri ve kalan bayatlık; Ek A, A.6 ve ledger'a karşı | salt-okur | P0/P1 yok | `O4` |
| `O5` | REV-2 | reviewer | `NEXT_PROMPT.md` ve Pencere 2'de plana yapılan değişiklikler; plan, ClaudeQB ve doğrulayıcıya karşı | salt-okur | P0/P1 yok | W6 |
| `O5` | SEC-B | security-reviewer | SEC-A tabanından (`O2` kapanış commit'i) sonraki commit'ler ve `git diff HEAD` | salt-okur | Bulgu yok | W6 |
| `O5` | FIX | task (dosya sahibine göre) | P0/P1 düzeltmeleri; FIX olursa GATE yeniden | İlgili dosya | Bulgu kapandı | REV-1, REV-2, SEC-B |
| `O5` | I2b | orkestratör | Geçit değerleri ve SEC/REV hükümleri: §11 girdisi, `NEXT_PROMPT.md`'deki Pencere 2 sonucu, §1 satırları; fark ayrıca bayt/boru ve kimlik taramasından geçer | `PROJECT_LOG.md` §2.6 ve §11, `NEXT_PROMPT.md` (yalnız sonuç cümleleri), `ORCHESTRATION_PLAN.md` | O ana kadarki bütün sonuçlar yazılı | FIX, GATE |
| `O5` | C2 | orkestratör | Kapanış commit'i `Window 2: project log sweep and handoff for planning run 21` (döngü kuralıyla, onay sorulmadan) | git | Ağaç temiz | I2b |
| `O5` | FF | **kullanıcı onayı** | `git fetch . integrate/impl-96:main` (yalnız ileri) | git | `main` = C2 | C2 |
| `O5` | RID | orkestratör | Ek A.5 kimlik kontrolü: tüm ref'ler ve izlenen dosyalar, C2 dahil; yalnız sayılar ve konumlar | — | Geçti | FF |
| `O5` | PUSH | **kullanıcı onayı** | `git push origin main integrate/impl-96` (`--all` ve `--mirror` asla) | git | — | RID |
| `O5` | LSR | orkestratör | `git ls-remote origin` ile yerel hash karşılaştırması; sonuç sohbette; Pencere 3 açılışında yeniden doğrulanır ve kaydedilir | — | İki ref = C2 | PUSH |

### 6.4 Sıra, kapanışlar ve girdiler

- **`O2`:** K0 → kapanış `Window 2 O2: contract for the project log sweep and the run 21 handoff`.
- **`O3`:** W5 ∥ SEC-A1 ∥ SEC-A2 ∥ SEC-A3 ∥ REV-3 (tek uygulama ajanı W5) → bulguların yönlendirilmesi (P0/P1: FIX ya da beklenmedik durum; ledger bulguları: §10) → kapanış `Window 2 O3: project log sweep and pre-push reviews`.
- **`O4`:** I2a → GATE → kapanış `Window 2 O4: integration and gates`.
- **`O5`:** W6 ∥ REV-1 → REV-2 ∥ SEC-B → FIX (gerekirse; ardından GATE) → I2b → C2 `Window 2: project log sweep and handoff for planning run 21` (Pencere 2'nin son kapanışı; Pencere 3 devrini taşır; onay sorulmadan) → FF (**onay**) → RID → PUSH (**onay**) → LSR. FF, RID, PUSH ve LSR C2'den sonra, aynı oturumda yapılır; sonuçlar sohbette raporlanır, Pencere 3 açılışında `git ls-remote origin` ile yeniden doğrulanıp kaydedilir.
- **Silinecek depolar:** `gh api repos/ahmetxa/<ad>` ile I2a'da ve C2'den önce ölçülür (404 = silinmiş). Silinmişse PROJECT_LOG'a yazılır; ledger'daki `DEC-30` yürütme notu koşu 21'de.
- **SEC ve REV girdileri** (`local://` oturumlar arasında taşınmaz; ilgili oturumda yeniden üretilir; `O0`'daki boyutlar sırasıyla 69 KB, 321 KB, 412 KB, 9 KB ve 136 KB):
  - SEC-A1: `git log -p --reverse --no-color --format=fuller origin/main..HEAD -- snapshots docs README.md UNTRACKED-BY-DESIGN.md`
  - SEC-A2: `git log -p --reverse --no-color --format=fuller origin/main..HEAD -- Planner-docs`
  - SEC-A3: `git log -p --reverse --no-color --format=fuller origin/main..HEAD -- PROJECT_LOG.md NEXT_PROMPT.md ORCHESTRATION_PLAN.md` ve `git log --reverse --no-color --format=fuller --stat origin/main..HEAD`
  - REV-3: `git diff --no-color c2abd46 <C1> -- Planner-docs/Planing-Ledger.md README.md UNTRACKED-BY-DESIGN.md docs/` (C1: `git log --grep 'IMPL-96: repository move'`)
  - SEC-B: `git log -p --reverse --no-color <O2 kapanışı>..HEAD` (`git log --grep 'Window 2 O2'`) ve `git diff HEAD`

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
- **Pencere 1 keşfinde bulunan, W3/W4 tablolarında olmayan kaymalar (2026-11-13; dokunulmadı; satır numaraları C1 ağacına göre):** `README.md` :100 yamalı AGC'yi "Currently installed" diye anıyor (cihazda yamasız V9.6; D9); :124-127 2026-09-05 tuzak durumunu anlatıyor (bugün `prefs.trap.armed = 10`); :78-79 "None of these is in version control" diyor, ama :112-113'teki iki `.agc` dosyası izleniyor; :194 `ishtar-cam-modes/mode` ve `lang`'i dışlanmış sayıyor, ikisi de izleniyor; :42-43, :48 ve :65 A16 derlemesini canlı bir girdi gibi anlatıyor (`DEC-28`); :193 `dist/*.zip`'i kapsamıyor (E6).
- `UNTRACKED-BY-DESIGN.md` (satır numaraları C1 ağacına göre): :33 `agc-50mp-yama/` için 4 dosya diyor (2026-08-24 ölçümü; bugün kökte 15, `tools/`'ta 3; E4); :47 "Partial/failed clone…" yanlış log atfına dayanıyor (E11); :49 Faz 1.6'yı açık sayıyor (E1); :75 `hal-raw50-deneme.patch` boyutu güncel değil; `dist/` için satır yok (`*.zip` ile dışlanıyor).
- `docs/agc-12mp-configuration.md:375` APK'yı yamalı `ce65f862…`'ye sabitliyor (AOSPA); HyperOS 4'teki APK `fa4066eb…` (D9). `:378` "2 / 12" AOSPA dönemine ait.
- `PROJECT_LOG.md:823` izlenen dosya sayısını "344" diyor (Pencere 1 açılışında 350; G12) → Pencere 2, W5. `PROJECT_LOG.md:812` hatalı `-o` biçiminin sonucunu `snapshots/snapshots/…` diye anlatıyor; o dizin olmadığı için yönlendirme başarısız olur ve betik yine `stored:` yazar [ÇIKARIM: çalıştırılmadı].
- Snapshot adlarındaki saat tutarlı değil (E7); README :143 W3 ile düzelir. Başka belgelerdeki "UTC" iddiaları (PROJECT_LOG §6'nın andığı `Faz3.7:71`) koşu 21 ya da 12. denetimde ele alınır.

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
| G2 | `integrate/impl-96` | Rebuilt 2026-11-13 (K8) on `7fa0a51`: `70946ff` (the two IMPL96 snapshots; probe lines 42, 190, 191 redacted), `03b0898` (historical notes in `docs/build-environment.md` and `docs/pre-rental-plan.md`, plus `docs/rom-build-device-notes.md`, a new file), `775b321` (`PROJECT_LOG.md`, `NEXT_PROMPT.md`), then the window 0 commits `b603516` (C0, adds this file) and `c2abd46` (follow-up); 68 commits at the window 1 opening. The old hashes `37edb5f`, `6a20999`, `fcceaab` exist only in the bundle and the local reflog: cite only the new ones | git, 2026-11-13 (re-checked at the window 1 opening) |
| G3 | `origin` | `https://github.com/ahmetxa/ishtar_cam_modes.git`, private, default branch `main` | `gh api`, 2026-11-13 |
| G4 | Remote state | `git ls-remote origin` → `refs/heads/main` = `587e3b581a66961082e49e2449327478724ad765` (62 commits); nothing after it is pushed | 2026-11-13 |
| G5 | Root commit | `ff6934e` (2026-08-24), identical locally and on GitHub | PROJECT_LOG §11; git |
| G6 | Old remote | `ishtar-eski` (`ahmetxa/ishtar`) removed locally; its only branch `main@f8a05ca` (IMPL-89, 2026-09-10) is an ancestor of `main` | git merge-base, 2026-11-13 |
| G7 | Pre-push secret scan | Whole history clean; the only password-pattern hit is the accepted debug signing default (DEC-10) | PROJECT_LOG §11 |
| G8 | Repositories to delete | All three still existed on 2026-11-13 (`gh api` 200): `ahmetxa/ishtar` private, the other two public. Re-measured at the window 1 opening, 2026-11-13T17:22:43Z: all three still 200, visibility unchanged | `gh api`, 2026-11-13 (twice) |
| G9 | Mirrors | `../ishtar-arsiv/android_local_manifests.git` (`main@22283d8`), `../ishtar-arsiv/android_device_xiaomi_ishtar.git` (`beryl@d48816f`, `vauxite@713784c`); `git fsck` exit 0 for both | 2026-11-13 |
| G10 | K8 bundle | `../ishtar-arsiv/impl-96-unredacted.bundle`, 77,094 B, sha256 `b9fa9c5cd5d0ae78f9f051ab62ecbfc2d9b2fa2fecd33f40247ef88bf58f6cd3`; ref `refs/heads/integrate/impl-96` = `fcceaab`; requires `7fa0a51`; `git bundle verify` OK | 2026-11-13 |
| G11 | K8 scan | Masked scan of `git log --all -p` and of every tracked file: 0 occurrences of the three values after the rebuild (before: one each, all in `37edb5f`). Tree diff old tip → new tip: probe only, 3 lines | 2026-11-13 |
| G12 | Tracked files | 350 at the window 1 opening (349 before C0, which added this file); re-measure with `git ls-files \| wc -l` when writing | git, 2026-11-13 |
| K4 | Deleted 2026-11-13 (five items) | Never-tracked `devir-teslim-promptu.md` (replaced by `NEXT_PROMPT.md`); empty root dir `UsersahmetAppDataLocalTempaon-smoke/`; never-tracked logs ignored by `.gitignore:48` (`*.log`): `install.log` (line-identical to tracked `snapshots/20260831-1603__faz2.2__install-transcript-v2.1.txt`, CR aside), `common_clone.log`, `kernel_clone.log` | PROJECT_LOG §2.1, §11 |
| D1 | ROM | HyperOS `OS4.0.0.44.WMACNXM`, Android 17 (SDK 37), security patch 2026-09-01 | adb getprop, 2026-11-13; probe |
| D2 | Vendor/odm fingerprint | `Xiaomi/ishtar/ishtar:13/TKQ1.221114.001/OS4.0.0.44.WMACNXM:user/release-keys` | adb getprop, 2026-11-13 |
| D3 | Kernel / root | `5.15.215-KylinKernel-260925-Release`; SELinux Enforcing; `su` context `u:r:ksu:s0`; verifiedbootstate `orange`; KernelSU `4.3.0-r1` (`ksud 4.3.0-r1 (uapi: 6)`) | adb, 2026-11-13 (`ksud` re-read at the window 1 opening); probe :118, :214, :218, :273, :356, :360 |
| D4 | Camera HAL | `/odm/lib64/hw/camera.qcom.so` md5 `2a955e68ad043380675529edb64a40f7`, 27,305,440 B; differs from the AOSPA A15 stock HAL the module is locked to (`HAL_STOCK_MD5` `c3fa63a8…`, 27,268,688 B) | adb, 2026-11-13; probe :245; `halpatch.sh:32-34`. Not the smoke baseline: without the module its `sensor.*` and `hal.*` fields hash empty input (`d41d8cd9…`) |
| D5 | Sensor blob | `/odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin` md5 `9e4d0fe1a8bf2eb4146c9917a0ac2c4c`, 1,062,250 B = module `EXPECT_MD5` and `EXPECT_SIZE` (`post-fs-data.sh:8-9`, `customize.sh:14`) | adb, 2026-11-13; probe :247 |
| D6 | AON | `/vendor/lib64/camera/aon_front.pb -> /odm/lib64/camera/aon_front.pb` ships in the ROM | adb, 2026-11-13 |
| D7 | Modules | `ishtar_cam_modes`, `ishtar_aon_fix` absent; 13 other module dirs (FreePPS, advsettings-en, box_for_root (disabled), eight `*-morphe`, unlimitedphotos, zygisksu = NeoZygisk) | adb su ls, 2026-11-13; probe :287-353 |
| D8 | Cameras | 13 camera devices; hal0 standard streams max 4096x3072; 8192x6144 appears only in vendor tags and the deprecated `android.scaler.availableRawSizes` | probe :267, :368, :372 |
| D9 | AGC | `org.codeaurora.snapcam` versionName `8.4.300.414775575.18` = unpatched `AGC8.4.300_V9.6_snap.apk` (md5 `fa4066eb3bf82cc097906fd108073500`); `pref_camera_resolution=full` → 12.58 MP derived (4096x3072); `prefs.trap.armed = 10` (value 37); `agc.pref_48m` absent | adb, 2026-11-13; probe; smoke baseline |
| D10 | Other apps | `com.android.camera` (`1+6.4.000380.1`); `com.xiaomi.module.evaluation` 1.55 (Open Camera per `FIND-4.4-02`; the probe itself does not name it); no project tile app (`com.ishtar.cammodes`); no `com.rifsxd.ksunext` or `me.weishu.kernelsu` package | adb pm, 2026-11-13 (re-read at the window 1 opening); probe :220-221, :223-239 |
| D11 | Extra ROM identity | Build `CP2A.260605.016`; vendor security patch 2026-02-01; bootimage fingerprint carries `OS3.0.305.0.WMACNXM` | probe :119, :121-122, :198; adb, window 1 opening |
| V1 | Validator `--mode all` | `error_count=0`, `warning_count=1` (`step4_has_nonblocking_warnings=P2:1,P3:9`), `p0_findings=0`, `p1_findings=0`, `subplan_count=42`, `secret_findings=0` | 2026-11-13 (also after the rebuild) |
| V2 | Validator `--mode step4 --strict` | Fails only on `strict_warning=step4_has_nonblocking_warnings=P2:1,P3:9` (expected baseline) | 2026-11-13 |
| V3 | Self-test | `SELF-TEST: PASS`; VAL-BUILD2 sha256 `407fb9be180d96ff0fc6d409d27ad35d4b3de10e0ea3dea8e53a1daee33cb2e0`; A1–A3 PASS | 2026-11-13 |
| REL | Release | `ishtar-cam-modes` v2.2 / versionCode 13; `dist/ishtar-cam-modes-v2.2.zip` md5 `e95789572311cc95266d3ab4045cdcba` | md5sum, 2026-11-13 |
| T3 | `smoke.sh -o` path bug | `docs/release-checklist.md:165` and `docs/agc-12mp-configuration.md:202` pass `snapshots/…`; `smoke.sh` prepends `snapshots/` itself (`:38`, `:284`); correct form at `docs/release-checklist.md:414` | 2026-11-13 |
| TRAP | Trap clearing | No procedure in `docs/agc-12mp-configuration.md`; the only one is `docs/phase3-preconditions.md:71-119`: no backup step; an in-place overwrite through a redirect (:99, `cat /data/local/tmp/p.xml > $PREFS`) truncates the original before the write, and nothing checks that the filtered temp file (:96-97) is non-empty; AOSPA owner and SELinux label hard-coded (:83-85, :110) | 2026-11-13; re-read at the window 1 opening |
| M1 | Module on HyperOS 4 (code reading, not measured) | Sensor guard passes (`EXPECT_MD5`), so the sensor layer would mount; the HAL guard (`post-fs-data.sh:101-107`) fails closed and skips the HAL layer; `setmode.sh:52-58`, `:79-83` stop and start `cameraserver`, `vendor.camera-provider` and `vendor.camera-provider-2-7-ext`: the probe shows the first two running (:15, :17) and `vendor.camera-provider-2-7-ext-uvc` in place of the third (:18; the probe's property filter is not recorded); tile long-press needs `com.rifsxd.ksunext` (`WebUiActivity.java:15`) | ModuleMap and DocsT3Evidence scouts; probe :15-18 [INFERENCE] |
| E1 | Faz 1.6 | `Planner-docs/Faz-1-Plans/Faz1.6-workspace-readme-and-refs-index.md` is `verified`, updated 2026-08-30 | ledger :71 |
| E2 | DEC-05 | "**Closed clean, 2026-08-24 (IMPL-02).**" No keystore entry in any of the five archives; no rotation or withdrawal needed | ledger :576 |
| E3 | AON fix behaviour | `ishtar-aon-fix/post-fs-data.sh:12-15` exits when `/vendor/lib64/camera/aon_front.pb` exists; otherwise `:22-40` copies `/vendor/lib64/camera` into the module, adds the file and bind-mounts the directory | ModuleMap |
| E4 | `agc-50mp-yama/` | `README.md` (reproduction recipe), two smali sources (`allOutputSizes.smali`, `getSupportedOutputSizes.smali`), seven experimental HAL patch tables (`hal-*-deneme.patch`), four Faz 4.1 stage tables (`f41-*.tbl`), `find_tag_write_site.py`, `tools/` | ls, 2026-11-13 |
| E5 | `docs/` | 18 Markdown documents (formats, procedures, evidence, runbooks, the generated release manifest) | ls, 2026-11-13 |
| E6 | `dist/` | `ishtar-cam-modes-v2.2.zip` (1,009,107 B, md5 `e95789572311cc95266d3ab4045cdcba`; installed on AOSPA A15 by IMPL-81, VAL-INSTALL) and `ishtar-cam-modes-v2.1.zip` (1,008,686 B, md5 `4a8226d6f4c4cacd97d8b96086bb36fa`, an IMPL-76 rebuild; the root v2.1 zip is md5 `fea919b67a4693a4591127be4a6e9daa`) | md5sum, 2026-11-13; PROJECT_LOG §2.2; README :77 |
| E7 | Snapshot names | The time in the name is typed by the operator (`smoke.sh -o NAME`) and is not a reliable clock: of 172 time-stamped `.txt` names, 64 match the header time as UTC, 52 as UTC+3 (host local time), 14 neither (±6 min), and 42 have no header time. The header `taken` line is UTC and authoritative. The IMPL96 pair uses UTC+3: `20261113-1821` ↔ `2026-11-13T15:21:35Z` | smoke baseline header; name/header scan of `snapshots/`, 2026-11-13 |
| E8 | Tags | The repository has no tags | `git tag`, 2026-11-13 |
| E9 | DEC-01 history | Private remote `ahmetxa/ishtar` from 2026-09-10 (IMPL-90; `main` pushed at `f8a05ca`); the DEC-01 row notes that `snapshots/` holds full-resolution camera captures, so a public remote would publish them | ledger :599 |
| E10 | `candidates/*.bin` rule | `.gitignore:56-58`: "Faz 5.1 candidate blobs: regenerated by tools/mode0_12bit.py, and kept out of blobs/ so no mode switch can select an unproven variant." | `.gitignore` |
| E11 | Deleted logs (K4) | `common_clone.log` = `Cloning into 'common_sm8550'...`; `kernel_clone.log` = `fatal: destination path 'kernel_ishtar' already exists and is not an empty directory.` | PROJECT_LOG §2.1 |
| E12 | README remote | `README.md` states no repository remote (its remote mentions concern `device_ishtar/` and `refs/`) | grep, 2026-11-13 |
| E13 | `snapshots/` | Tracked (`FIND-2.2-03`), although `README.md:186` lists it under Exclusions | README; PROJECT_LOG §8 |
| K3 | Open kernel input (closed) | `docs/rom-build-device-notes.md:79-84`, recorded 2026-09-20 and unverified: the user's report that third parties upstreamed the kernel used by MIUI and AOSPA, which would have changed kernel scoping (`Faz8.2`; `DEC-08`, recommendation defer). The user dropped it on 2026-11-13 (K3), still unverified; the file records the closure at `:239-240` (its §10, commit `03b0898`); `DEC-28` moots `DEC-08` | `docs/rom-build-device-notes.md`, 2026-11-13 |
| AUD11 | Eleventh audit | `Planner-docs/Sub-Planing-Audit.md`: 2026-09-14, `PASS_WITH_WARNINGS`, supersedes the tenth (2026-09-13). A bounded audit of planning run 20's `Faz7.2` amendment; the other 41 sub-plans keep the tenth audit's content assessment. Set 42: 4 queued, all `READY_WITH_WARNINGS` (`Faz7.2` → `Faz7.3` → `Faz8.1`'s agreement half → `Faz8.3`), 35 COMPLETE (among them `Faz3.7`, `Faz7.1` and `Faz8.2`), 2 SUPERSEDED (`Faz4.1`, `Faz4.7`), 1 DEFERRED (`Faz4.6`); `Faz6.1` COMPLETE with its ledger status kept `implemented` (effect verification owned by `F7.3-08`); queue state READY; ten active findings, none P0 or P1. The queue is void since 2026-11-13 (`DEC-28`) | `Sub-Planing-Audit.md` :6, :57, :113-114, :290-293, :305-314, :331, :348-350, :432-434 |
| OPN | Window 1 opening re-measurement | 2026-11-13, 17:22-17:25 UTC, read-only, on `dc27e5d0` only: D1-D7, D9 (`smoke.sh` to stdout only: its COMPARABLE block is byte-identical to the 15:21:35Z baseline; no file written), D10, D11, 13 camera devices, `/data/adb/modules` mtime 2026-10-26; `git ls-remote origin` → `main` = `587e3b5` (G4); G8; G9 (refs as listed, `git fsck` exit 0); G10 (size, sha256, `git bundle verify` OK); G12; V1-V3 at baseline. Not re-measured: D8's vendor-tag scan (hal0's stream rows were re-read inside the smoke COMPARABLE block); G11. A second stdout-only `smoke.sh` run at the window 1 close (21:31:25Z) matched the baseline again | adb, gh, git, 2026-11-13 |

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
- Verified at the window 1 opening (2026-11-13, by script): 644 lines, all CRLF, NUL 0; every line number in this section holds; each quoted anchor occurs exactly once; §4 rows carry 10 `|` each and §8 rows 7.

### A.5 Push rules

- Only explicit refspecs: `git push origin main integrate/impl-96`; never `--all` or `--mirror`; then `git ls-remote origin` hash comparison.
- Before any push, an identity check over everything reachable from any ref (`git log --all -p`) and over every tracked file: every value-bearing line with the key `persist.sys.miui.sno`, `ro.ril.miui.imei0` or `ro.ril.miui.imei1` (forms `[key]: [value]`, `key=value`, `key: value`) reads `<redacted>`, and no digit-bounded 15-digit number passing the Luhn check appears. Lines that only name a key in prose are counted and reported but do not fail the check (decision 5a, 2026-11-14: read literally, the check would fail on prose such as this line). Report counts and locations only; the redacted values are never recovered, read or written. Window 2 order (§6.4): SEC-A1–A3 in `O3`, SEC-B in `O5` before C2; this check (RID) runs in `O5` after C2 and the fast-forward, immediately before the push, so it covers C2. Every stage closing also runs it (§0 step 4). The script below is the reference implementation (run from the repository root, for example through `py -3 - <<'EOF'` in Git Bash); it never prints a value:

```python
import re, subprocess
KEYS = r"persist\.sys\.miui\.sno|ro\.ril\.miui\.imei[01]"
KEY = re.compile(KEYS)
VAL = [re.compile(r"\[(?:%s)\]\s*:\s*\[([^\]]*)\]" % KEYS), re.compile(r"(?:%s)\s*[=:]\s*(\S+)" % KEYS)]
D15 = re.compile(r"(?<!\d)\d{15}(?!\d)")
def luhn(s):
    t = 0
    for i, ch in enumerate(reversed(s)):
        d = int(ch)
        if i % 2:
            d = d * 2 - 9 if d > 4 else d * 2
        t += d
    return t % 10 == 0
def scan(name, text, c):
    for n, line in enumerate(text.splitlines(), 1):
        if KEY.search(line):
            vals = [m.group(1) for r in VAL for m in r.finditer(line)]
            if vals:
                c["value_lines"] += 1
                if any("<redacted>" not in v for v in vals):
                    c["NOT_REDACTED"] += 1
                    print("not redacted:", name, n)
            elif "<redacted>" not in line:
                c["prose_mentions"] += 1
        for m in D15.finditer(line):
            if luhn(m.group()):
                c["LUHN15"] += 1
                print("luhn candidate:", name, n)
c = dict(value_lines=0, NOT_REDACTED=0, prose_mentions=0, LUHN15=0)
log = subprocess.run(["git", "log", "--all", "-p", "--no-color"], capture_output=True).stdout
scan("git-log", log.decode("utf-8", "replace"), c)
files = subprocess.run(["git", "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "replace").split("\0")
for f in filter(None, files):
    try:
        scan(f, open(f, "rb").read().decode("utf-8", "replace"), c)
    except OSError:
        pass
print(c, "PASS" if c["NOT_REDACTED"] == 0 and c["LUHN15"] == 0 else "FAIL")
```

### A.6 Window 2 facts (2026-11-14)

Measured by the orchestrator in `Pencere 2 · O0` (2026-11-14), read-only; no device command was sent. Window 2 writers take facts from A.2 and this table only.

| # | Fact | Value | Source / when measured |
|---|---|---|---|
| OPN2 | Window 2 opening | Branch `integrate/impl-96`, tree clean, 69 commits, tip = C1 (cited by title); `main` 63 commits at `7fa0a51` (`[origin/main: ahead 1]`); no tags; 350 tracked files (G12 unchanged: C1 added no file) | git, 2026-11-14 |
| G4b | Remote state | `git ls-remote origin` lists only `HEAD` and `refs/heads/main`, both `587e3b5` (62 commits). Not pushed: `7fa0a51`, `70946ff`, `03b0898`, `775b321`, `b603516` (C0), `c2abd46` (C0 follow-up), C1 and every window 2 stage commit | git, 2026-11-14 |
| G8b | Repositories to delete | `gh api` at 2026-11-14T07:23:21Z: `ahmetxa/ishtar` (private), `ahmetxa/android_local_manifests` (public) and `ahmetxa/android_device_xiaomi_ishtar` (public) all still 200; `ahmetxa/ishtar_cam_modes` private, default branch `main` | `gh api`, 2026-11-14 |
| L653 | Ledger after window 1 | 653 lines, all CRLF, NUL 0; IMPL-96 row at :525 (`## 6.` at :526); `DEC-27`…`DEC-32` at :605-:610; no `DEC-33` anywhere. Window 2 does not edit it | script, 2026-11-14 |
| LSH | Ledger line shift by C1 | C1 added 9 lines (IMPL-96 row :525; new §7 top entry and separator :550-:551; `DEC-27`…`DEC-32` :605-:610). A reference written against the 644-line ledger maps, checked by content, to N for N <= 524, N + 1 for 525-548, N + 3 for 549-601 and N + 9 for N >= 602 (examples: 527→528, 549→552, 551/553/555→554/556/558, 586→589, 599→602, 601→604, 632→641) | scouts and `git diff c2abd46` against C1, 2026-11-14 |
| SH8 | `03b0898` shift | Inserted exactly 8 lines after line 2 of `docs/pre-rental-plan.md` and `docs/build-environment.md` (`@@ -2,0 +3,8 @@`): a reference to line N >= 3 written before it now points to N + 8; all 13 such references in `PROJECT_LOG.md` checked by content | `git diff 7fa0a51 03b0898`; scout, 2026-11-14 |
| CDATE | Commit date groups | `PROJECT_LOG.md` §3.5 groups commits by author date in +0300 (`git log --date=short`): `7fa0a51`, `70946ff`, `03b0898`, `775b321`, `b603516` and `c2abd46` on 2026-11-13; C1 on 2026-11-14 (01:05 +0300 = 2026-11-13T22:05Z) | git, 2026-11-14 |
| RID0 | Identity check baseline | The A.5 script over `git log --all -p` and the 350 tracked files: 6 value-bearing key lines (3 in history, 3 in the tree), all `<redacted>`; 0 Luhn-valid 15-digit numbers; 9 prose-only key mentions (5 history, 4 tree), which a literal reading of A.5 would fail (decision 5a). PASS | script, 2026-11-14 |
| SEC0 | Push-range pre-scan | Every added line of the seven commit patches (`git log -p origin/main..integrate/impl-96`, 3,148 lines including intermediate states): no token, private key, credential assignment, rented-server host name, MAC address or Luhn-valid 15-digit number; the two IPv4-shaped matches are version strings (probe :321; `PROJECT_LOG.md` §11); the probe header records that the other phone's serial was not recorded, and the emulator appears only under its adb port name; author and committer e-mail identical to the already pushed `587e3b5` | script, 2026-11-14 |
| SMK-O | `smoke.sh -o snapshots/NAME` | `scripts/smoke.sh:283` creates only `snapshots/` (`mkdir -p "$SNAPDIR"`); `:284` redirects into `snapshots/snapshots/NAME.txt`, whose directory does not exist, so no file is written; `:285` still prints `stored: snapshots/snapshots/NAME.txt`; the script sets only `set -u` (`:29`) | code reading, 2026-11-14 [INFERENCE: not run] |
