# ORCHESTRATION_PLAN — ishtar

> **Onay:** kullanıcı, 2026-11-13 ("onay"). Kararlar: K8 = A, konusuz kapsamı = altı karar, K7 = (a).
> **Onay 2:** kullanıcı, 2026-11-14 ("onaylıyorum"): Pencere 2 planı (§6) varsayılan kararlarla (§6.1); aşama başına oturum döngüsü, aşama sonunda sorulmadan devir ve yerel commit, beklenmedik durumda sade bir soru (§0).
> **Onay 3:** kullanıcı, 2026-11-15: oturum başına bağlam eşiği 400k token; faz ve aşama uzunlukları bu eşiğe göre boyutlanır (§0 adım 9).
> **Kural:** Her yeni sohbet penceresi (oturum) bu plandan **tek bir aşamayı** ya da onaylı birleşik aşamaları yürütür (§0); aşamaların oturumlara dağılımı bağlam bütçesiyle belirlenir (§0 adım 9). Giriş noktası `NEXT_PROMPT.md`; ayrıntı, sözleşme ve durum bu dosyadadır.
> **Öncelik:** Ölçüm ve kanonik dosyalar (ledger, `Planner-docs/`) bu plandan üstündür. Çelişki bulunursa §10'a yazılır ve kullanıcıya söylenir; plan sessizce uydurulmaz.

## 0. Pencere protokolü

**Terimler (2026-11-14).** *Pencere N*: §1'deki plan fazı (ad tarihseldir; başta her faz tek oturumdu). *Aşama*: bir fazın orkestrasyon adımı: `O0` keşif, `O1` plan (kullanıcı onayına kadar), `O2` kontrat, `O3` paralel uygulama, `O4` entegrasyon ve geçitler, `O5` son inceleme ve kapanış. *Oturum*: bir sohbet penceresi. Aşama kimliği `Pencere 2 · O2` (kısaca `2 · O2`) biçimindedir. Tek başına "Faz N" ClaudeQB proje fazıdır (§3, Adlandırma).

**Döngü (kullanıcı kararı, 2026-11-14; bütçe 2026-11-15).** Her oturum tek bir aşamayı ya da adım 9'a göre onaylanmış birleşik aşamaları yürütür. Pencere 2'de `O0`+`O1` aynı oturumdaydı (plan onayıyla biter). Pencere 3 ve 4'te `O0` ile `O1` ayrı oturumlardır; küçük Step 4 dilimlerinde birleşebilir (§9). Büyük aşama bölünür (adım 9). Fazın aşama ve görev tablosu o fazın bölümündedir (Pencere 2: §6.3). Aşama atlanmaz; oturum kendiliğinden sıradaki aşamaya geçmez.

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
9. **Bağlam bütçesi (2026-11-15; eşik ve %60 hedefi kullanıcı kararı, öteki kurallar bu planın seçimi):** ölçümler ve ölçüm betiği Ek A.7'de.
   - **Eşik 400k token.** Orkestratör bağlamını Ek A.7 betiğiyle her alt ajan sonucundan sonra ve en geç her beş turda, 250k'dan sonra her turda ölçer. 300k'yı geçince yeni görev başlatmaz: elindeki işi doğrular, adım 7 ile kapanır, kapanışı 400k'dan önce bitirir. Bu, beklenmedik durum sayılmaz.
   - **Hedef 240k (eşiğin %60'ı).** Fazın `O1` planındaki aşama tablosu oturum başına bir tahmin sütunu taşır. Tahmini 240k'yı aşan aşama alt aşamalara bölünür (`O3a`, `O3b`, …); her biri ayrı oturum, ayrı §1 satırı ve ayrı kapanış commit'idir.
   - **Birleştirme:** toplam tahmini 240k'nın altında kalan ardışık aşamalar, planda gösterilip kullanıcı onaylarsa tek oturumda yürür. `O0`+`O1` birleşimi için henüz onaylı plan olmadığından bir önceki kapanışın `NEXT_PROMPT.md`'si tahminle önerir, açılışta kullanıcı onaylar.
   - **Tahmin:** açılış ≈ 23k + `NEXT_PROMPT.md`'nin her KB'ı için 0,58k. Tur başına ≈ 6k (yürütme, entegrasyon, inceleme) ya da ≈ 10–14k (plan, kontrat, uzun metin yazımı). 35k açılışla 240k ≈ 30–34 yürütme turu ya da 15–20 yazım turudur.
   - **Neden:** büyümenin kabaca yarısı ile dörtte üçü modelin kendi çıktısıdır (düşünme, edit gövdesi, görev metni) ve bağlamda kalır. Okunan Türkçe belgenin her KB'ı ≈ 0,55k token tutar.
   - **Okuma:** 20 KB'tan büyük okuma ihtiyacı scout'a verilir; scout ≤ 4 KB özet döndürür. Orkestratör büyük dosyaları `grep` ve dar `:N-M` aralıklarıyla okur, aynı aralığı ikinci kez okumaz.
   - **Alt ajanlar ve taslaklar:** dönüş blokları ≤ 4 KB; ayrıntı `local://` dosyasına yazılır. Taslaklar `cp` ile yerine konur ve betikle doğrulanır; orkestratör taslağı yeniden yazmaz.
   - **Yazım:** yeni ya da yeniden yazılan satırlar ≤ 600 bayt hedefler; uzun bir satırı düzeltmek bütün satırı yeniden yazdırır ve edit yanıtında geri getirir. `todo` listesi ≤ 8 madde, yalnız durum değişince güncellenir.
   - **Devir:** `NEXT_PROMPT.md` ≤ 20 KB; her oturumun başında bütünüyle bağlama girer, ayrıntı plana ve PROJECT_LOG'a atıfla verilir.

## 1. Durum tablosu

Durum sözlüğü: `pending`, `in_progress`, `done`, `blocked`.

| Pencere | Faz | Kapsam | Önkoşul | Durum | Commit / kanıt |
|---|---|---|---|---|---|
| 0 | Keşif, plan, sözleşme | O0 keşif, O1 plan (onaylandı), K8 = A (dal yeniden kuruldu), bu dosya, NEXT_PROMPT ve PROJECT_LOG güncellemesi | — | done | `70946ff`, `03b0898`, `775b321`; C0 `Window 0: orchestration plan, K8 redaction, handoff for window 1` (`git log --diff-filter=A -- ORCHESTRATION_PLAN.md`); inceleme sonrası takip commit'i `Window 0 follow-up: align handoff with plan, rename review IDs` |
| 1 | IMPL-96 uygulaması | Ledger IMPL-96 (§4–§8, `DEC-27`…`DEC-32`); README ve UNTRACKED kaymaları (T2); iki `-o` satırı (T3); inceleme; C1 | Pencere 0 | done | C1 `IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline` (`git log --grep 'IMPL-96: repository move'`); ledger 644 → 653 satır (21 satır yalnız ekleme, 9 yeni satır), geçitler taban değerde; bu dosyada §1, §3 (Adlandırma), §5.1 (W3 `:143` ve W4 `:61` hedefleri), §6 (W5, SEC ve sıra), §10, Ek A.2, A.4 notu ve A.5 (sıra) güncellendi; C1 kullanıcının gece talimatıyla, diff gösterilmeden atıldı (PROJECT_LOG §11) |
| 2 | Kapanış ve yayın | PROJECT_LOG bayat satırları (W5); push öncesi güvenlik ve içerik incelemesi; NEXT_PROMPT'u koşu 21'e hazırlama (W6); `main` FF; push; silinecek depoların ölçümü. Aşamalar §6.3 | Pencere 1; push kararı | done | aşama satırları aşağıda; son kapanış `Window 2: project log sweep and handoff for planning run 21` (`git log --grep '^Window 2:'`); FF ve push 2026-11-15'te ayrı onaylarla yapıldı: `origin`'de `main` ve `integrate/impl-96` = C2 (PROJECT_LOG §11); takip commit'i `Window 2 follow-up: context budget and stage sizing` (`git log --grep '^Window 2 follow-up:'`): bağlam bütçesi (§0 adım 9, Ek A.7), Pencere 3–5+ oturum düzeni (§1, §7–§9), `NEXT_PROMPT.md` `3 · O0` için |
| 2 · O0+O1 | Keşif ve plan | Üç scout; ölçümler (Ek A.6); keşif envanteri (§6.2); onaylı plan (§6); aşama döngüsü (§0) | Pencere 1 | done | `Window 2 O0-O1: approved plan, discovery facts, stage-per-session loop` (`git log --grep 'Window 2 O0-O1'`) |
| 2 · O2 | Kontrat | K0 (§6.3) | 2 · O0+O1 | done | `Window 2 O2: contract for the project log sweep and the run 21 handoff` (`git log --grep '^Window 2 O2:'`); envanter doğrulandı, 84 → 97 madde (bir madde çıkarıldı, kullanıcı onayıyla 15 yer eklendi: §6.1 karar 8, §6.5.1); §6.5, §7, §10 ve A.6 güncellendi; kimlik taraması geçti |
| 2 · O3 | Paralel uygulama | W5 ∥ SEC-A1 ∥ SEC-A2 ∥ SEC-A3 ∥ REV-3 | 2 · O2 | done | `Window 2 O3: project log sweep and pre-push reviews` (`git log --grep 'Window 2 O3'`); W5 envanterin 97 maddesini karşıladı (96'sı uygulandı, §2.6 maddesi gereği gibi dokunulmadı); tek ajanlı ilk deneme bağlam taşmasıyla bozuk düzenleme yaptı ve geri alındı, iş parçalara bölündü (P1 `task` ajanı; P2–P5 salt-okur taslak ajanları ve orkestratörün `edit` entegrasyonu); SEC-A1 ve SEC-A2 bulgu yok; SEC-A3 bir P3 (yerel yollar, kabul); REV-3 P0/P1 yok, P2 `UNTRACKED-BY-DESIGN.md:36` düzeltici task ile düzeltildi, P3 ledger → §10; Ek A.6'ya `O3OPN` ve `G12b`; kimlik taraması geçti |
| 2 · O4 | Entegrasyon ve geçitler | I2a → GATE | 2 · O3 | done | `Window 2 O4: integration and gates` (`git log --grep '^Window 2 O4:'`); açılış ölçümü Ek A.6 `O4OPN` (üç depo 19:34:57Z'de hâlâ 200); I2a: W5 sahiplik kontrolü geçti (`2 · O2` → `2 · O3` arasında dört dosya; PROJECT_LOG'da §11 dışındaki her değişiklik §6.2 envanterinin satırlarında, §2.6 değişmemiş; dördüncü dosya `UNTRACKED-BY-DESIGN.md:36`, REV-3 düzeltmesi); PROJECT_LOG §2.6 aynı satır sayısıyla yeniden yazıldı, sonraki satır numaraları kaymadı; GATE (19:42Z): V1–V3 taban değerde, bayt ve boru kontrolü geçti; kimlik taraması geçti (`prose_mentions=16`); §10'a iki madde; kullanıcı onayıyla takip commit'i `Window 2 O4 follow-up: anchor the O2 commit lookups` (`git log --grep '^Window 2 O4 follow-up:'`): §1 `:45` ve §6.4 `:341`'deki `2 · O2` aramaları konu satırına bağlandı, `NEXT_PROMPT.md`'nin dal durumu güncellendi |
| 2 · O5 | Son inceleme ve kapanış | W6 ∥ REV-1 → REV-2 ∥ SEC-B → FIX (gerekirse, sonra GATE) → I2b → C2 → FF (onay) → RID → PUSH (onay) → LSR | 2 · O4 | done | `Window 2: project log sweep and handoff for planning run 21` (`git log --grep '^Window 2:'`); açılış ölçümü Ek A.6 `O5OPN` (üç depo 20:07:24Z'de ve C2'den önce 21:11:12Z'de hâlâ 200); W6: A parçası (`task`, başlık ve §0–§3) 100K bağlama ulaştı ve `partial` döndü, B parçası (§4–§11) geniş bağlamlı salt-okur ajanın taslağı, A'nın iki maddesinin düzeltmesiyle birlikte orkestratörce `edit` ile uygulandı ve betikle doğrulandı; REV-2'nin plan parçası ve SEC-B'nin `PROJECT_LOG.md` parçası W6'ya bağlı olmadığı için W6 ile paralel çalıştı; REV-1 (iki parça): P0/P1 yok, P2/P3 bulguları düzeltici task ile `PROJECT_LOG.md` §1–§10'da 30 satır içi düzeltmeyle giderildi (FIX); REV-2 plan parçası: P0/P1 yok, 1 P2 ve 7 P3 orkestratörce plana işlendi; REV-2 `NEXT_PROMPT.md` parçası: P0/P1 yok, 2 P2 ve 9 P3 düzeltici task ile 14 satırda giderildi (FIX), plana düşen üç uzantı §7'ye işlendi; SEC-B (iki parça): bulgu yok; GATE (FIX'ten sonra, 20:56Z): V1–V3 taban değerde; bayt ve boru kontrolü geçti; kimlik taraması geçti (`prose_mentions=16`); §10'a `O5` maddeleri; C2'den sonra, 2026-11-15: FF 08:14:45Z, RID geçti (`NOT_REDACTED=0`, `LUHN15=0`), PUSH 08:15:01Z, LSR: iki ref = C2 (PROJECT_LOG §11) |
| 3 | Planlama koşusu 21 | Step 1 + Step 2: Faz 7/8 emekli; K7 = (a) için faz ve alt planlar; önce K9 ve kapsam soruları. Oturum düzeni ve bütçe §7 | Pencere 2 | pending | aşama satırları aşağıda; plan ve onay §7.2 (`3 · O1`) |
| 3 · O0 | Keşif | Açılış ölçümleri ve "Açılışta ayrıca"; sekiz açılış sorusu (yanıtlar §7'ye); üç scout; keşif envanteri (§7) | Pencere 2 | done | `Window 3 O0: discovery for planning run 21` (`git log --grep '^Window 3 O0:'`); açılış `W3OPN` (durum (b)); sekiz yanıt §7'de, K9 = hayır (§2; `DEC-33` koşu 21'de); dört salt-okur scout (§7'deki S3 ikiye bölündü); envanter §7.1 (≈ 13 KB); PROJECT_LOG push cümleleri güncel; `NEXT_PROMPT.md` kapanışa girmediği için kullanıcı onaylı takip commit'i `Window 3 O0 follow-up: hand-off for stage 3 O1` |
| 3 · O1 | Plan | Aşama ve görev tablosu, oturum başına bağlam tahminiyle (§0 adım 9); kullanıcı onayı | 3 · O0 | done | `Window 3 O1: plan for planning run 21` (`git log --grep '^Window 3 O1:'`); plan §7.2, onay 2026-11-15 (form, dört soruda öneriler); `PRB` 13:01Z'de yürütüldü (§7.1 `W3P01`–`W3P04`; SukiSU-Ultra v4.3.0-r1 cihazda doğrulandı); S5–S7 scout'ları, olgular `W3F29`–`W3F32`; bağlam plan sunumunda 206k, onayda 235k |
| 3 · O2a | Step 1 | `Main-Planing.md` (§7.2 Step 1 listesi; metni kullanıcı onaylar); `--mode step1 --strict`; tahmin ≈ 225k | 3 · O1 | done | `Window 3 O2a: Step 1 for planning run 21` (`git log --grep '^Window 3 O2a:'`); açılış tuttu, dört depo 200; `ST1-R` iki scout, `ST1-D` iki paralel taslak scout'u; inceleme P0/P1 yok, P2'ler düzeltildi; onay 14:10Z (C01–C03 dahil); 316 → 406 satır, CRLF, NUL 0; `step1 --strict` çıkış 0, `all` yalnız `missing_phase_folder` (beklenen); kimlik taraması geçti; bağlam 86k → 241k (PROJECT_LOG §11) |
| 3 · O2b | Step 2 kontratı | §7.3: alt plan sözleşmesi, ortak bağlam, `3 · O4` hedef tablosu; tahmin ≈ 225k | 3 · O2a | pending | |
| 3 · O3a | Step 2 taslakları | `Faz10.1`–`Faz10.3` (`SP1`–`SP3`, `CPa`); tahmin ≈ 185k | 3 · O2b | pending | |
| 3 · O3b | Step 2 taslakları | `Faz10.4`, `Faz10.5` (`SP4`, `SP5`, `CPb`); tahmin ≈ 155k | 3 · O3a | pending | |
| 3 · O4 | Entegrasyon ve geçitler | Ledger, Index, Ontology, Hetzner satırları (`I3a`, `I3b`); `GATE3`; tahmin ≈ 233k | 3 · O3b | pending | |
| 3 · O5 | Son inceleme ve kapanış | `REV-4` ∥ `SEC-C` → `FIX3` → `C3` → FF (onay) → push (onay) → `LSR`, `RID`; tahmin ≈ 215k | 3 · O4 | pending | |
| 4 | 12. denetim | Step 3 (`run-step3.md`); oturum düzeni §8 | Pencere 3 | pending | |
| 5+ | K7 = (a) Step 4 dilimleri | 12. denetimin kuyruğu; dilimler ve oturumlar bütçeyle (§9) | Pencere 4 | pending | |

Her faz §0'daki aşamalarla yürür; bir fazın aşama satırları o fazın `O1` planında eklenir. Pencere 3'ün `O0` ve `O1` satırları 2026-11-15'te bütçe kuralıyla, `O2a`–`O5` satırları aynı gün `3 · O1` planıyla (§7.2) eklendi (§0 adım 9).

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
| K9 | 50MP HAL katmanının HyperOS 4 HAL'inde (`2a955e68…`) yeniden türetilmesi | **Hayır, şimdilik (2026-11-15, `3 · O0`):** HAL katmanı HyperOS 4'te kapalı kalır, sensör katmanı sürer; ileride yeniden açılabilir (§7, soru 1) | `DEC-33` (koşu 21 yazar) |
| Push | `main` ve `integrate/impl-96` | **Yapıldı (2026-11-15, ayrı onaylarla):** iki ref de C2 (§1; PROJECT_LOG §11). Takip commit'i de aynı gün `main`'e ileri sarıldı ve push edildi (reflog; `W3OPN`, §7.1) | — |
| Pencere 2 planı | Görevler, sıra, kapsam | Onaylandı (2026-11-14, "onaylıyorum"); kararlar §6.1 | — |
| Döngü | Oturum yapısı | Pencere 2'de her aşama ayrı oturumda (`O0`+`O1` birlikte); Pencere 3'ten itibaren bağlam bütçesiyle (§0 adım 9, Onay 3); kapanışta `NEXT_PROMPT.md` ve yerel commit sorulmadan; FF ve push ayrı onay; beklenmedik durumda sade soru (§0) | — |

## 3. Her pencerede geçerli kurallar

**Roller.**
- **Orkestratör (ana oturum):** plan, dağıtım, entegrasyon, doğrulama ve commit. Sıcak noktalar yalnız onundur: `Planner-docs/Planing-Ledger.md`, `Main-Planing.md`, `Sub-Planing-Index.md`, `Sub-Planing-Audit.md`, `Project-Ontology.md`; `CHANGELOG.md`; sürüm yerleri (`ishtar-cam-modes/module.prop`, `customize.sh`); üretilen `docs/release-manifest.md`; `.gitignore`, `.gitattributes`; `snapshots/` (kanıt, düzeltilmez); bu dosya; tüm git işlemleri.
- **Alt ajanlar:** Görev metni kendi kendine yeter (hedef dosya yolları, değişiklik, kabul kriteri, yasak alanlar). Ajan yalnız sahip olduğu dosyaya yazar; başka bir dosyada sorun görürse düzeltmez, raporlar. Doğrulayıcı, test ya da format çalıştırmaz. Dönüşte şu blok zorunludur: `status`, `changed_files`, `acceptance` (kriter / karşılandı mı / kanıt), `contract_deviations`, `open_issues`. Sıcak noktalar için yalnız taslak üretir (`local://…`).
- Aynı anda en fazla 4 uygulama ajanı çalışır. `task` aracında `isolated` ve `outputSchema` yok; yalıtım ayrık dosya sahipliğiyle sağlanır. `librarian` ve `designer` ajanları bu ortamda yok.
- **Adlandırma:** Görev kimlikleri (`W1`–`W6`, `T3`, `I1`, `REV`, `SEC`; Pencere 2 için ayrıca `K0`, `SEC-A1`–`SEC-A3`, `SEC-B`, `REV-1`–`REV-3`, `I2a`, `I2b`, `GATE`, `FIX`, `FF`, `RID`, `PUSH`, `LSR`), aşama kimlikleri `O0`–`O5` ve Ek A olgu kimlikleri (`G`, `D`, `V`, `REL`, `T3`, `TRAP`, `M1`, `E`, `AUD11`, `OPN`; A.6'da `OPN2`, `G4b`, `G8b`, `L653`, `LSH`, `SH8`, `CDATE`, `RID0`, `SEC0`, `SMK-O`, `O2`'de eklenen `O2OPN`, `G8c`, `G1b`, `CLOG`, `LMAP`, `C1MAP`, `O3`'te eklenen `G12b`; sonraki aşamaların açılış ölçümleri `O3OPN` biçiminde) yalnız bu plana aittir. Main-Planing risk kimlikleri `R1`–`R12`, kararlar `K1`–`K9` ve `DEC-NN`, kontrol listesi `C-NN`, ClaudeQB `Faz n.m` / `Fn.m-NN` ile karışmasın diye böyle seçildi (önceki oturumun `R21` → `RUN21` düzeltmesiyle aynı gerekçe); `K0` bir görev kimliğidir, karar değildir. Ek A'daki `K3` ve `K4` satırları ise karar etiketlerini bilerek yeniden kullanır; plana özgü değildir. `C1` ve `C2` faz kapanış commit'leridir; Pencere 2'nin aşama commit'leri başlıklarıyla anılır (§6.4).
- **Adlandırma, Pencere 3 (2026-11-15, §7.2):** görev kimlikleri `PRB`, `ST1-R`, `ST1-D`, `ST1-A`, `ST1-W`, `ST2-R`, `ST2-K`, `SP1`–`SP5`, `CPa`, `CPb`, `I3a`, `I3b`, `GATE3`, `REV-4`, `SEC-C`, `FIX3`; faz kapanış commit'i `C3`. Olgu kimlikleri `W3OPN`, `W3O1OPN`, `W3F01`–`W3F32`, `W3P01`–`W3P04`. `PRB` komutları `PRB1`–`PRB10` (`C1`–`C3` commit'leriyle karışmasın diye); `S1`–`S7` scout adlarıdır.

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
**Durum:** `done` (2026-11-14). `O0`+`O1` 2026-11-14'te bitti: üç scout, ölçümler (Ek A.6), keşif envanteri (§6.2); kullanıcı planı varsayılan kararlarla onayladı ("onaylıyorum", 2026-11-14; §6.1). `O2` (K0) 2026-11-14'te bitti: envanter doğrulandı ve 97 maddeye çıktı (§6.5.1, karar 8); W5 kontratı ve `O3` ortak bağlamı §6.5'te; Pencere 3 girdileri §7'de, yeni bulgular §10'da. `O3` 2026-11-14'te bitti: W5 envanterin 97 maddesini karşıladı (96'sı uygulandı, §2.6 maddesi gereği gibi dokunulmadı; tek ajanlı ilk deneme bağlam taşmasıyla bozuk bir düzenleme yaptı ve geri alındı, iş parçalara bölündü); SEC-A1–A3 ve REV-3'te P0/P1 yok; bulgular §10'da, REV-3'ün P2'si `UNTRACKED-BY-DESIGN.md:36`'da düzeltici task ile düzeltildi. `O4` 2026-11-14'te bitti: I2a'nın W5 sahiplik kontrolü geçti, PROJECT_LOG §2.6 güncel aşamaya göre yazıldı, geçitler (V1–V3) taban değerde (Ek A.6 `O4OPN`; PROJECT_LOG §11); iki yeni bulgu §10'da (arama belirsizliği kullanıcı onayıyla takip commit'inde düzeltildi). `O5` 2026-11-14'te bitti: W6 `NEXT_PROMPT.md`'yi Pencere 3 · O0+O1 için yazdı; REV-1, REV-2 ve SEC-B'de P0/P1 yok; P2/P3 bulguları düzeltici task'larla (`PROJECT_LOG.md` 30 satır, `NEXT_PROMPT.md` 14 satır) ve plana işlenerek giderildi; geçitler FIX'ten sonra taban değerde (§1, §10; PROJECT_LOG §11). FF, RID, push ve LSR kapanış commit'inden sonra yapılır; sonuçları Pencere 3 açılışında kaydedilir (§7).
**Güncelleme (2026-11-15):** FF, RID, push ve LSR yapıldı: `origin`'de `main` ve `integrate/impl-96` = C2 (§1; PROJECT_LOG §11). Ardından takip commit'i `Window 2 follow-up: context budget and stage sizing` bağlam bütçesini ekledi (§0 adım 9).
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
| 8 | K0'ın envantere eklediği 15 yer (`O2`) | (a) Ekle: W5 hepsini düzeltir (kullanıcı, 2026-11-14, "ekle"; öteki seçenekler: yalnız mekanik olanlar (kayan satır numaraları ve "commit edilmedi") ya da hiçbiri; §6.5.1) |

### 6.2 Keşif envanteri (`O0`, 2026-11-14, ağaç `9ee505f`)

W5'in `PROJECT_LOG.md` iş listesi. Yerler alıntıyla bulunur; satır numaraları `9ee505f` ağacına aittir (PROJECT_LOG §1–§10 o günden beri değişmedi, `O2OPN`). K0 (`O2`, 2026-11-14) listeyi betikle ve iki salt-okur scout'la doğruladı, düzeltti ve kullanıcı onayıyla genişletti (§6.5.1); `O2`'de eklenen satırlar "(K0)" ile işaretli. Alıntılar “…” içindedir; "satır çapası" satırı bulur, "satır içi" alıntı yalnız o satırda aranır. Son sütundaki kimlikler Ek A.1, A.2 ve A.6'dadır. §2.6 ve §11'e W5 dokunmaz (§0 adım 4).

| Yer | Şu an (alıntı) | Güncel olgu → hedef | Kaynak |
|---|---|---|---|
| §1 `:9` | “Bu belgedeki ölçümlerin hepsi telefonda AOSPA Vauxite (Android 15) ve KernelSU Next varken yapıldı”; “**2026-11-13 kullanıcı beyanı (ölçülmedi):**” | Şimdiki durum iddiası: "hepsi" yerine 2026-11-13'ten önceki ölçümler (AOSPA Vauxite, KernelSU Next ve "(DEV §2-3)" kalır); HyperOS 4 2026-11-13'te gözlendi ve aynı gün salt-okur ölçüldü (`70946ff`, §2.3; ROM, kernel 5.15.215 ve KernelSU dahil). Etiketteki "(ölçülmedi)" kalkar; "Çinli bir geliştiricinin portu" kullanıcı beyanı olarak, "ROM derleme fikri bırakıldı" kullanıcı kararı (`DEC-28`) olarak kalır | D1–D3, OPN, G2, A.1 |
| §1 `:15` | “İkisi de herkese açık; henüz hiç derlenmedi” | Yalnız "henüz hiç derlenmedi" değişir: hiç derlenmedi; derleme 2026-11-13'te bırakıldı (`DEC-28`); iki depo silinecek (`DEC-30`) ve `O3OPN` ölçümünde duruyorsa öyle yazılır. "İkisi de herkese açık" doğru, kalır | A.1, G8b, G8c, O3OPN |
| §1, §2.3 `:14`, `:127`, `:131`, `:132` | “L:638”; “L:640”; “L:642” | `L:647`; `L:649`; `L:651` | LSH, LMAP |
| `:3`, §2 `:43` | “Durum tarihi **2026-11-13**”; “## 2. Şu an neredeyiz (2026-11-13)” | Yazım tarihi | — |
| `:5` (K0) | “`Ö13` bu oturumun 2026-11-13 ölçümü” | Belge sonraki oturumlarda düzenlendiği için "bu oturumun" → "2026-11-13 oturumunun"; yeni ölçümler `Ö13` ile değil, tarihleriyle etiketlenir (§6.5.2) | — |
| §2.1 `:46` | “**Dal ve commit'ler (2026-11-13 oturum sonu):**”; “sonra C0 (`ORCHESTRATION_PLAN.md`'yi ekleyen commit)” | Etiket yazım tarihine çekilir. C0 `b603516`, C0 takip commit'i `c2abd46`, C1 (ilk anılışta başlığıyla) ve Pencere 2 aşama commit'leri (başlıklarıyla); commit sayıları `O3OPN`'den. Satırdaki "`main` 63 commit" ve "Etiket yok" doğru | G2, G4b, CLOG, O3OPN |
| §2.1 `:47` | “`DEC-27` atandı; ledger'a Pencere 1'de yazılır” | Ledger §8 `:605` | L653, LMAP |
| §2.1 `:49` | “`7fa0a51` ve `integrate/impl-96` dalı push edilmedi. Push Pencere 2'de karara bağlanır” | Yazım anında doğru: yalnız tarihlenir (`O3OPN`) ve push'un `2 · O5`'te, C2'den sonra ayrı onayla yapılacağı eklenir (plan §0 adım 5). Push'tan sonraki güncelleme Pencere 3 açılışında (§7) | G4b, O3OPN, A.5 |
| §2.1 `:52` | “Ölçüm (2026-11-13, `gh api`): üç depo da hâlâ var.” | `O3OPN`'deki ölçüm (UTC zamanı ve sonuç); önceki ölçümler 2026-11-14T07:23:21Z ve 10:03:48Z, üçü de 200. I2a yeniden ölçer | G8b, G8c, O3OPN |
| §2.1 `:54` | “- 344 izlenen dosya.” | `O3OPN`'deki sayı ve tarihi (örnek biçim "350 izlenen dosya (YYYY-AA-GG)"); `:53`'teki "(Ö13)" etiketi `:55`–`:57` için kalır | G12, OPN2, O3OPN |
| §2.1 `:60` | “Ledger 11. denetimi hâlâ "outstanding" sayıyor; düzeltmesi IMPL-96'da.” | Cümlenin tamamı şimdiki durum iddiası: IMPL-96 notları yazıldı (ledger `:100`, `:552`, `:554`, `:556`, `:558`); notsuz kalanlar `:51`, `:57`–`:60`, `:589` (§8 `:783`) | LSH, LMAP |
| §2.1 `:61` | “IMPL satırı hâlâ yok (IMPL-96)” | IMPL-96 satırının (4). maddesi kaydediyor (ledger `:525`) | L653, LMAP |
| §2.1 `:59` (K0), `:63`, `:64` | “**Commit durumu (2026-11-13):**”; “son sürüm C0'dadır”; “5. C0 (`ORCHESTRATION_PLAN.md`, bu günlük ve `NEXT_PROMPT.md`'yi taşıyan commit) işlendi” | Etiket yazım tarihine çekilir; C0 = `b603516`; bu günlüğün ve `NEXT_PROMPT.md`'nin sonraki sürümleri `c2abd46`, C1 ve Pencere 2 aşama commit'lerinde (dosya listeleri CLOG'da). Aynı cümle §2.6 `:237`'de de var; W5 ona dokunmaz | G2, CLOG |
| §2.1 `:67` | “(47 commit, 225 dosya, remote yok) bayattır (§8)” | Kısmen düzeldi: ledger `:528`'deki IMPL-96 notu remote'u ve commit sayılarını yazıyor, dosya sayısını yazmıyor (§8 `:784`) | LSH, LMAP |
| §2.2 `:83` | “cihazda kurulu v2.2 ile bayt-özdeşliği bozar” | Yalnız "cihazda kurulu" → "yayımlanan" (bayt-özdeşliği gerekçesi yayımlanan v2.2 zip'i için geçerli, `DEC-29`); arkasına tarihli not: v2.2 AOSPA A15'te kuruluydu (IMPL-81), HyperOS 4'te proje modülü kurulu değil | D7, E6, REL, A.1 |
| §2.3 `:98` | “(yamasız APK'da bu anahtar yok)” | Anahtar prefs dosyasında yok; APK'da olup olmadığı ölçülmedi | D9; plan §10 |
| §2.3 `:104` | “(DEV; salt-okur adb; ledger'a işlenmedi)” | Yalnız "ledger'a işlenmedi" değişir: ledger'da IMPL-96 satırının (4). maddesi (`:525`); "DEV; salt-okur adb;" kalır | L653, LMAP |
| §2.4 `:147` | “Ledger §5'te IMPL-01 … IMPL-95 kayıtlı” | IMPL-96 de kayıtlı (`:525`) | L653 |
| §2.4 `:165` | “**Sıradaki numaralar:** `IMPL-96`”; “(Pencere 1'de ledger'a yazılacak)” | Sıradaki `IMPL-97`; `DEC-27`…`DEC-32` ledger'da (`:605`–`:610`; "ayrıldı" da düşer); sonraki `DEC-33` | L653, LMAP |
| §2.4 `:166` | “Pencere 1'de ledger'a işlenecek” | Konusuz notları ledger'da (`:582`, `:583`, `:599`, `:601`, `:603`, `:604`) | A.1, LSH, LMAP |
| §2.5 `:174` | “kayıt `IMPL-96`'da (`DEC-28` atandı; ledger'a Pencere 1'de yazılır)” | Ledger `:606`; §7 üst girdisi `:550` | L653, LSH, LMAP |
| §2.5 `:176` | “L:549”; “L:598-601” | `L:552`; `L:601-604` | LSH |
| §2.5 `:217` | “(PRP:231-246)” | `PRP:239-254` | SH8 |
| §2.5 `:220` | “`DEC-07` açık” | Tarihli not: 2026-11-13'ten beri konusuz (`DEC-28`); `:174` bölümün kalanını tarihsel sayar | A.1 |
| §2.6 `:228`–`:240` | “### 2.6 Bu oturumun durumu (Pencere 0, 2026-11-13)” | W5 dokunmaz; orkestratör `O4`'ten itibaren (I2a) aşama kapanışlarında günceller | §0 |
| §3.1 `:289` | “etkisi `Faz7.3`'te doğrulanacak” | Tarihli not: `Faz7.3` amaçsız (`DEC-28`); durum "implemented" kalır | AUD11, A.1 |
| §3.1 `:292` | “henüz kiralama yapılmadı” | "kiralama hiç yapılmadı; ROM derleme 2026-11-13'te bırakıldı (`DEC-28`)"; gelecek iddiası yazılmaz | A.1 |
| §3.1 `:294` | “kuyruğun başında” | 11. denetimin kuyruğu 2026-11-13'ten beri geçersiz | AUD11 |
| §3.2 `:342` (K0) | “L:357, L:632” | `L:632` → `L:641` (`FIND-3.5-01`, `FIND-4.5-02`); `L:357` değişmez | LSH, LMAP |
| §3.2 `:407` | “IMPL-96 (devam ediyor)”; “Ledger satırı Pencere 1'de yazılacak”; “ledger satırı yazılmadı”; kanıt “§2.6, §11” | IMPL-95 satırının biçiminde: koşu yazıldı (`L:525`, C1 başlıkla); kanıt `L:525`, C1, `snap 20261113-1819` ve `snap 20261113-1821`; sonuç hücresi yalnız Ek A olgularıyla (IMPL-96 kaydı yazıldı; push `2 · O5`'te, depo silme `DEC-30` bekliyor) | L653, LMAP, CLOG, E7, G4b |
| §3.3 `:417` (K0) | “(L:559, L:609;” | `L:562`, `L:618` | LSH, LMAP |
| §3.3 `:440` | “`DEC-26`: `Faz7.2` Scaleway'e taşındı; snapshot kesilmedi; commit edilmedi” | Yalnız "commit edilmedi" için tarihli not: 2026-11-13'te `7fa0a51`'de değiştirilmeden commit edildi; "snapshot kesilmedi" kalır | G1, G1b |
| §3.3 `:454` | “PRP:41, PRP:62” | `PRP:49`, `PRP:70` | SH8 |
| §3.3 `:455` | “PRP:105” | `PRP:113` | SH8 |
| §3.3 `:456` | “`-52/53/54` kapandı, `-55/56/57` yeni açıldı; commit edilmedi” | `:440` gibi: tarihli not, 2026-11-13'te `7fa0a51`'de commit edildi; AUDIT-FIX ifadeleri kalır; isteğe bağlı not: kuyruk 2026-11-13'ten beri geçersiz | G1, G1b, AUD11 |
| §3.5 `:494` | “Dal `main`'deki 62 commit”; “`origin/main`'den sonraki dört commit push edilmedi (§2.1)” | Liste `integrate/impl-96` dalının commit'leridir, eskiden yeniye: ilk 62'si `origin/main`'de (`587e3b5`), `7fa0a51` yerel `main`'in 63.'sü, sonrakiler yalnız dalda; liste `O3OPN`'deki uca kadar; push durumu `O3OPN`'den. "satır sonundaki italik parantezler sonradan eklenmiş nottur" cümlesi kalır | G4b, OPN2, O3OPN |
| §3.5 (yeni gruplar) | — | Son grubun (`**2026-09-14 (2)**`) arkasına: **2026-11-13 (6):** `7fa0a51` *(main)*, `70946ff`, `03b0898`, `775b321`, `b603516`, `c2abd46`; **2026-11-14 (N):** C1, `2 · O0+O1`, `2 · O2` (hash yerine adla). Konular CLOG'dan aynen; HEAD notu yazılmaz; `2 · O3` ve sonrası listeye girmez | CDATE, CLOG |
| §3.5 `:574` | “*(origin/main)*” (`f8a05ca` satırı) | Tarihli not: eski remote'un (`ahmetxa/ishtar`) ucuydu | G6, E9 |
| §3.5 `:577`, `:578`, `:581` | “*(push edilmedi)*” | Not kalkar: `587e3b5`'e kadar hepsi push edildi | G4b |
| §3.5 `:582` | “*(HEAD, push edilmedi)*” | “*(origin/main)*” | G4b |
| §4 `:584` | “## 4. Kararlar (DEC-01 … DEC-26)” | `DEC-01 … DEC-32` | L653 |
| §4 `:586` | “(satır :569–:601;” | §8 başlığı `:572`, satırlar `:576`–`:610` | L653, LSH, LMAP |
| §4 `:588` | “**Açık kararlar (2026-11-13):**”; “Kalan 23 kararın hepsi yanıtlandı ya da kapandı” | Etiket yazım tarihine çekilir. Açık: `DEC-09` (koşullu) ve K9 (henüz DEC yok); `DEC-07`, `DEC-08` konusuz (`DEC-28`); kernel-upstream iddiası düştü (K3); "Kalan 23" → "Kalan 31" (toplam 32 karar); "(fact sheet D2)" → ledger §8 `:576`–`:610` | A.1, K3, L653, LMAP |
| §4 `:592`, `:593` | “– → **AÇIK** (IMPL-92 ile 2026-09-11'de güncellendi)”; “**AÇIK** (kullanıcı); `F8.1-06`/`-07` sonrası kapanır”; “2026-09-13 öneri → **AÇIK**”; “**AÇIK** (kullanıcı); Faz 7'ye bağlı” | Durum hücreleri (ikinci ve dördüncü alıntı) → "konusuz (`DEC-28`, 2026-11-13)"; tarih hücrelerine (birinci ve üçüncü) " → konusuz 2026-11-13" eklenir; kimlik hücrelerindeki kalın kalkar (kalın açık kararı işaretler, `:594`); kaynak `ledger:582`, `:583`. Yalın "**AÇIK**" `:594`'te (`DEC-09`, açık) de geçer; ona dokunulmaz | A.1, LSH, LMAP |
| §4 `:592`–`:617` | `ledger:573`…`ledger:601` hücreleri | Her biri +3; örnek DEC-09 `:584`, DEC-01 `:602`, DEC-26 `:604` | LSH, LMAP |
| §4 `:595` | DEC-01 satırı | Yanıt korunur; tarihli not: 2026-11-13'te depo `ahmetxa/ishtar_cam_modes`'a taşındı (`DEC-27`), eski depo silinecek (`DEC-30`); ledger `:602` | A.1, G3, LSH |
| §4 `:613`, `:615`–`:617` | DEC-22, DEC-24, DEC-25, DEC-26 durum hücreleri | "yanıtlandı…" korunur, arkasına "; 2026-11-13'ten beri konusuz (`DEC-28`)"; `:617`'de `docs/build-environment.md:118-130` → `:126-138` | A.1, SH8, LMAP |
| §4 (yeni satırlar) | — | `DEC-27`…`DEC-32`, `DEC-26` satırının (`:617`) arkasına, §6.5.2 madde 7'deki biçimde; `DEC-30` durumu `O3OPN`'deki ölçümle; `DEC-31` yalnız anahtar adlarıyla | A.1, L653, LMAP, O3OPN |
| §4 `:619` | “ledger'a IMPL-96 ile (Pencere 1) yazılacak” | Yazıldı (`:605`–`:610`) | L653 |
| §4 `:623`, `:624`, `:627`, `:628`, `:629` | “(`DEC-29` atandı; ledger'a Pencere 1'de yazılır)”; “Faz 7/8'i emekliye ayırır (`DEC-28` atandı; ledger'a Pencere 1'de yazılır)”; “`delete_repo` yok; silmeyi kullanıcı yapar (`DEC-30` atandı; ledger'a Pencere 1'de yazılır)”; “(§2.1). Silmeyi kullanıcı yapar (`DEC-30` atandı; ledger'a Pencere 1'de yazılır)”; “(`DEC-32`, Pencere 1'de yazılacak)” | Sırasıyla: yazıldı (ledger `:607`, `:606`, `:608`, `:608`, `:610`); hücrelerin geri kalanı doğru | L653, LMAP |
| §4 `:631` | “ledger'a Pencere 1'de işlenecek” | İşlendi: konusuz notları ledger `:582`, `:583`, `:599`, `:601`, `:603`, `:604`'te (IMPL-96) | A.1, LMAP |
| §4 `:633` | “ledger satırı Pencere 1'de” | Yazıldı (`:525`) | L653 |
| §4 `:634` | “Pencere 2'de sorulur” | Yazım anında doğru; yalnız kesinleşir: `2 · O5`'te, C2'den sonra, ayrı onayla (plan §0 adım 5). Push'tan sonraki güncelleme Pencere 3 açılışında (§7) | G4b, A.5 |
| §5.1 `:642` | “ledger:638–:642” | `:647`–`:651` | LSH |
| §5.2 `:656`; §5.3 `:669` | “bu duvarlardan birine dair yeni kanıt gerekir (ledger:586)” (`:656`); satır çapası “"50 MP end-to-end in AGC" hedefi”, satır içi “ledger:586” (`:669`) | `:589` (ikisinde de). Yalın "ledger:586" `:605`'te de geçer (`:592`–`:617` maddesi) | LSH, LMAP |
| §5.2 `:657` | “ledger:632” | `:641` | LSH |
| §5.2 `:663` | “ledger:629” | `:638` | LSH |
| §5.3 `:677` | “ledger:598, :601” | `:601`, `:604` | LSH |
| §5.4 `:691` | “HAL yama tablosunun HyperOS 4'te geçerliliği ölçülmedi” | Kısmen doğru (tablo HyperOS 4'te hiç denenmedi): HAL farklı (`2a955e68…`, 2026-11-13'te ölçüldü); tablo AOSPA HAL'ine (`c3fa63a8…`) kilitli; HAL koruması kapalı başarısız olur [ÇIKARIM]; yeniden türetme K9. Cümledeki parantez kalır | D4, M1, A.1 |
| §6 `:695` | “README:143 ve Faz3.7:71 UTC diyor” | "Çelişki" cümlesi E7'nin açıklamasıyla değişir (ad saati operatörün yazdığı saattir, güvenilmez; başlıktaki `taken` UTC'dir ve esastır); README C1'de düzeldi (`:153`); `Faz3.7:71` sürüyor (`ORCHESTRATION_PLAN.md` §10, koşu 21). Aynı satırdaki "170 `.txt`" için tarihli not: 2026-11-13'te IMPL96 çifti eklendi; zaman damgalı `.txt` adı 172 | E7, C1MAP, A.1 |
| §6 `:732` | “snapshot'ı da IMPL satırı da yok” | IMPL-96 satırının (4). maddesi kaydediyor; snapshot yok. Aynı satıra tarihli not: daha yeni kayıt 2026-11-13 IMPL96 çifti (`70946ff`; salt-okur HyperOS 4 tabanı, bracket değil) | L653, LMAP, G2, E7 |
| §7 `:738` (K0) | “2026-09-14 (run 20, commit edilmedi)” | Son değişiklik C1 (IMPL-96); run 20 2026-11-13'te `7fa0a51`'de commit edildi; "§6/§7'de bayat satırlar" kısmen notlu (LMAP; §8) | G1b, LMAP |
| §7 `:741` (K0) | “2026-09-14; commit edilmedi; kuyruğu ve §14 kiralama promptu” | "commit edilmedi" → 2026-11-13'te `7fa0a51`'de commit edildi; hücrenin geri kalanı doğru | G1b |
| §7 `:747` (K0) | “2026-09-14; değiştirildi ama commit edilmedi” | 2026-11-13'te `7fa0a51`'de commit edildi; `03b0898` başına 8 satırlık tarihsel not ekledi; "**2026-11-13'ten beri tarihsel**" kalır | G1b, SH8 |
| §7 `:748` (K0) | “**izlenmiyor**; hiçbir yerden referans yok; IMPL satırı yok” | `03b0898`'den beri izleniyor; IMPL-96 satırının (4). maddesi kaydediyor (`L:525`); aynı hücredeki "telefon sonradan HyperOS 4 portuna geçti" → 2026-11-13'te gözlendi | G2, LMAP, A.1 |
| §7 `:749` | “:165 yol hatası” | C1'de düzeldi (T3) | T3, A.1 |
| §7 `:770`, `:771` (K0) | “son sürüm C0'da (`git log --diff-filter=A -- ORCHESTRATION_PLAN.md`)” (iki satırda) | Her iki satır: ilk sürüm `775b321`; sonraki sürümler `c2abd46`, C1 ve Pencere 2 aşama commit'lerinde (CLOG); tarih hücresi yazım tarihine | CLOG |
| §8 `:781` | “11. denetim "outstanding"”; “Denetim yapıldı (2026-09-14, PASS_WITH_WARNINGS); commit edilmedi” | **Çözüldü (IMPL-96; ledger `:100`, `:552`):** denetim yapıldı (2026-09-14, PASS_WITH_WARNINGS) ve 2026-11-13'te `7fa0a51`'de commit edildi; "dosya:satır" `:100`, `:552` olur | LSH, LMAP, G1, G1b |
| §8 `:783` | “Step 3 yeniden denetimi "outstanding"” | **Kısmen çözüldü (IMPL-96):** eski `:551`, `:553`, `:555` artık `:554`, `:556`, `:558` ve notlu; `:51`, `:57`–`:60` ve `:589` notsuz (`ORCHESTRATION_PLAN.md` §10, koşu 21) | LSH, LMAP |
| §8 `:784` | satır çapası “`Planner-docs/Planing-Ledger.md:527`”; “62 commit, 344 izlenen dosya, `origin` var, 4 commit ileride” | "dosya:satır" `:528` olur. **Kısmen çözüldü (IMPL-96, ledger `:528`):** not remote'u ve commit sayılarını yazıyor, dosya sayısını değil. "güncel gerçek": `origin/main` `587e3b5` (62), `main` 63; dal ve izlenen dosya sayısı `O3OPN`'den | LSH, LMAP, G4b, O3OPN |
| §8 `:785` (K0) | “v2.2/13, mod `50mp`, HAL `fe0245a4…` (2026-09-20 ölçümü)” | "dosya:satır" `:530`, `:532`, `:534` olur. **Kısmen çözüldü (IMPL-96):** `:530` ve `:532` notlu, `:534` notsuz. "güncel gerçek": 2026-11-13'ten beri HyperOS 4, proje modülü kurulu değil, HAL `2a955e68…`; 2026-09-20 değerleri AOSPA A15'e ait | LSH, LMAP, D4, D7 |
| §8 `:781`–`:793`, `:809`, `:810`, `:817`–`:820` | ledger satır atıfları | Kaymaya göre (LSH; LMAP ile karşılaştırılır); `:524`'e kadar olanlar değişmez | LSH, LMAP |
| §8 `:796` (K0) | “Hepsi aşıldı; v2.2 kurulu; taban `fe0245a4…`; Faz3.7 verified” | Tarihli not: v2.2 AOSPA A15'te kuruluydu; 2026-11-13'ten beri HyperOS 4'te proje modülü kurulu değil | D7 |
| §8 `:801` (K0) | “Audit:350,385; ledger:590” | `ledger:593` (`DEC-16`) | LSH, LMAP |
| §8 `:811` | “`docs/pre-rental-plan.md:32`, `:233-234`, `:252-253`”; “PRP:31,122,181,205” | `:40`, `:241-242`, `:260-261`; `PRP:39,130,189,213` | SH8 |
| §8 `:812` | “sonuç `snapshots/snapshots/…` olur” | Çözüldü (C1, T3); anlatı düzeltilir: dizin olmadığı için dosya yazılmaz, betik yine `stored:` basar [ÇIKARIM] | SMK-O, T3, A.1 |
| §8 `:816` | “`devir-teslim-promptu.md:247`” | Dosya 2026-11-13'te silindi (K4) | K4 |
| §8 `:822` | README satırı (“`README.md:18`, `:19`, `:20`, `:77-78`, `:142`, `:143`, `:186`”) | **Çözüldü (C1):** bugünkü yerler `:18`–`:20` → `:20`–`:22`, `:77-78` → `:85-86` (ve yeni `dist/` paragrafı `:94`), `:142`–`:143` → `:152`–`:153`; `:186` (Exclusions) silindi. "dosya:satır" hücresi kayıt olarak kalır | C1MAP, A.1 |
| §8 `:823` | UNTRACKED satırı; “344 dosya”; “ledger:576, :599” | **Çözüldü (C1):** bugünkü yerler C1MAP'e göre; "344 dosya" → `O3OPN`'deki sayı; aynı hücredeki "hata `kernel_clone.log`'da" → log 2026-11-13'te silindi (K4), içeriği §2.1'de; kanıt `ledger:579`, `:602` | C1MAP, O3OPN, K4, E11, LSH |
| §8 `:825` (K0) | “IMPL-96; `--mode all` 1 uyarı (strict ile error); 62 commit, `origin`” | **Çözüldü (K4):** dosya 2026-11-13'te silindi. "güncel gerçek": sıradaki `IMPL-97`; `origin/main` 62, `main` 63 ve dal `O3OPN`'den; geri kalanı doğru | K4, L653, O3OPN |
| §8 `:827` | “`DEC-27` IMPL-96'da kaydedilecek”; “`docs/pre-rental-plan.md:250`”; “eski depo yerelde `ishtar-eski`” | Kaydedildi (`DEC-27` `:605`; DEC-01 `:602` notlu); `docs/pre-rental-plan.md:250` → `:258` (belge 2026-11-13'ten beri tarihsel, `03b0898`); "eski depo yerelde `ishtar-eski`" → yerel remote kaldırıldı, `ahmetxa/ishtar` silinecek (`DEC-30`) | L653, LMAP, SH8, G6 |
| §8 `:828` | “`README.md:144`; `UNTRACKED-BY-DESIGN.md:38-41`, `:63`” | **Çözüldü (C1):** UNTRACKED `:38`–`:39`, `:61`; README satırı kaldırıldı | C1MAP, K4, E11, A.1 |
| §8 `:829` | “Telefon AOSPA A15 + KernelSU Next”; “kullanıcı beyanı: HyperOS 4 portu, kernel 5.15.215; ölçülmedi” | Ölçülmüş değerler yazılır: `OS4.0.0.44.WMACNXM`, kernel `5.15.215-KylinKernel-260925-Release`, KernelSU `4.3.0-r1`, KernelSU Next uygulaması yok (2026-11-13; `70946ff`; ledger §6 `:532`; DEV `:223`–`:244`); yalnız "ölçülmedi" düşer | D1–D11, G2, LMAP |
| §8 `:848` | “**README / UNTRACKED-BY-DESIGN:**” maddesi (T2) | **Çözüldü (C1):** remote cümlesi README `:38`'de; `candidates/*.bin` satırı UNTRACKED `:71`'de | C1MAP, A.1 |
| §8 `:849` | “`:165` yol hatası düzeltilmeli (T3)” | T3 C1'de düzeldi; maddenin geri kalanı sürer | T3, A.1 |
| §8 `:850` | “IMPL-96'nın kapsamı §2.6'daki L biriminde” | IMPL-96 yazıldı (`:525`; §6 `:528`, `:530`, `:532`, §7 `:552`–`:558` ve §8 konusuz notları); notsuz kalan "outstanding" metinleri (`:51`, `:57`–`:60`, `:589`) koşu 21'e | L653, LMAP |
| §9 `:863` | “Çözüldü; v2.2 kurulu (VAL-INSTALL)” | "Çözüldü (VAL-INSTALL)" korunur; "v2.2 kurulu" için tarihli not: AOSPA A15'te kuruluydu, HyperOS 4'te kurulu değil | D7, E6 |
| §9 `:865` | “HyperOS 4 portuna geçti (2026-11-13)”; “Dosyalar farklıysa 16 noktalı tablo ve sensör varyantları uymaz; ölçülmedi (`NEXT_PROMPT.md` §4.3)” | "geçti (2026-11-13)" → "2026-11-13'te gözlendi". Ölçülmüş değerler: HAL farklı (`2a955e68…`), sensör aynı (`EXPECT_MD5`), 2026-11-13; tablo sonucu `:691` gibi ([ÇIKARIM]); K9 karar verir (`ORCHESTRATION_PLAN.md` §2, §7); NEXT_PROMPT bölüm atfı kalkar | D4, D5, M1, A.1 |
| §9 `:867` (K0) | “HyperOS 4'e uyarlama seçilirse (K7) yeniden tersine mühendislik gerekebilir” | K7 = (a) seçildi (`DEC-32`): 50MP katmanı için yeniden tersine mühendislik K9'a bağlı | A.1 |
| §9 `:874` | “`origin`'de 62 commit var; `7fa0a51` ve `integrate/impl-96` push edilmedi.” | Yazım anında doğru: tarihlenir (`O3OPN`); push `2 · O5`'te ayrı onayla; push'tan sonraki güncelleme Pencere 3 açılışında (§7) | G4b, O3OPN, A.5 |
| §9 `:875` | “**N4 Ledger geride:**”; “silinen dosyalar ve depolar” | **Çözüldü (IMPL-96)**; aynı maddedeki "silinen … depolar" → silinen dosyalar (K4) ve silinecek depolar (`DEC-30`; `O3OPN`'de duruyorsa öyle) | L653, K4, G8c, O3OPN, A.1 |
| §9 `:876` (K0) | “Uyarlama seçilirse (K7-a)” | "Uyarlama seçildi (K7 = (a), `DEC-32`)"; cümlenin geri kalanı doğru | A.1 |
| §9 `:878` | “2026-09-20 oturumunun kaydı yok (süreklilik boşluğu); IMPL-96 kaydeder.” | Kaydedildi (`:525`, madde 4) | L653, LMAP |
| §10 `:885` | “sıradaki **IMPL-96**” | `IMPL-97` | L653 |
| §10 `:888` | “ledger'a Pencere 1'de yazılacak” | Yazıldı (`:605`–`:610`) | L653 |
| §10 `:923` | “md5 `ce65f862…`” | "Kullanılan" geçmiş zamana: AOSPA döneminde kullanılan derleme (`ce65f862…`); HyperOS 4'te kurulu olan yamasız V9.6 (`fa4066eb…`) | D9 |
| §10 `:932`–`:934` | barista, `fixes.diff` ve Teardown maddeleri | Tarihli not: Faz 7 işi `DEC-28` ile tarihsel | A.1 |

**`O2` girdileri** (kaynak `W6Window3Inputs` scout raporu, 2026-11-14; satır atıfları `9ee505f` ağacına göre, `:159` o ağaçtaki plan satırıdır). K0 2026-11-14'te hepsini kaynağında doğruladı ve düzeltilmiş hâlleriyle §7'ye ve §10'a işledi; geçerli metin oradadır:
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
  - SEC-B: `git log -p --reverse --no-color <O2 kapanışı>..HEAD` (`git log -1 --format=%h --grep '^Window 2 O2:'`) ve `git diff HEAD`

### 6.5 W5 kontratı ve `O3` ortak bağlamı (K0, 2026-11-14)

Bu bölüm `2 · O3`'ün kontratıdır: W5'in görev metni 6.5.2 ile 6.5.3'ü, SEC-A1–A3 ve REV-3'ün görev metinleri 6.5.3'ü olduğu gibi kopyalar. Olgu kaynağı Ek A'dır (A.1, A.2, A.6); bu bölüm Ek A ile çelişirse Ek A'daki ölçüm kazanır ve çelişki kullanıcıya söylenir.

#### 6.5.1 Envanter doğrulaması (K0 adım 1, 2026-11-14)

- **Yöntem:** `py -3` betiği §6.2 tablosunun 84 satırını ayrıştırdı; her “…” alıntısının `PROJECT_LOG.md`'de kaç kez ve hangi satırlarda geçtiğini verilen satırlarla karşılaştırdı (PROJECT_LOG §1–§10 `9ee505f`'ten beri değişmedi, `O2OPN`). Hedef sütunundaki ledger, `PRP`, `docs/build-environment.md`, README ve UNTRACKED satırları betikle içerikten doğrulandı (A.6 `LMAP`, `SH8`, `C1MAP`). İki salt-okur scout (`InventoryRowsA`, `InventoryRowsB`) her maddeyi PROJECT_LOG bağlamında ve Ek A'ya karşı okudu.
- **Alıntılar:** hepsi bulundu ve verilen satırlarda. `:827`'deki alıntı eksik yazılmıştı (`docs/` öneki), düzeltildi. Sekiz maddenin alıntısı başka satırlarda da geçiyordu (`:54`, `:64`, `:174`, `:592`–`:593`, `:623`–`:629`, `:656`/`:669`, `:781`, `:784`): genişletildi, satır başına ayrıldı ya da satır çapasına bağlandı.
- **Çıkarılan madde:** `:795`, `:796`, `:804`, `:806` için "UNTRACKED `:61`/`:63` atıfları" yanlış okumaydı: bu satırlar `Main-Planing.md`, `Faz7.2` ve `Faz8.2`'nin `:61`/`:63` satırlarını anıyor ve C1 bu dosyalara dokunmadı. UNTRACKED atıfları `:823` ve `:828` maddelerinde.
- **Düzeltilen hedefler** (scout bulguları; eski ve yeni tablo betikle karşılaştırıldı): 84 maddeden 47'sinin hedefi düzeltildi ya da daraltıldı, 1'inin yalnız alıntısı genişletildi (`:174`), 12'sinin yalnız kaynak sütunu tamamlandı, 23'ü aynı kaldı, 1'i çıkarıldı. Cümlenin hâlâ doğru kısmı korunur (örnek `:15`, `:83`, `:104`, `:440`, `:456`, `:613`–`:617`); Ek A'da olmayan iddia yazılmaz (`:292`'de "hiç yapılmayacak" yerine "hiç yapılmadı"; `:691`, `:923`); aynı satırdaki ikinci bayatlık eklendi (`:695`, `:732`, `:823`, `:827`, `:865`, `:875`). C1'in ledger notlarının varlığı ve içeriği betikle doğrulanıp `LMAP`'e yazıldı; `:528` notu remote'u ve commit sayılarını yazıyor ama dosya sayısını yazmıyor, bu yüzden `:67` ve `:784` "kısmen" oldu.
- **Yazım anında doğru olan üç madde** (`:49`, `:634`, `:874`; push durumu) kaldı ve yalnız tarihlenir. Push'tan sonraki güncelleme Pencere 3 açılışında yapılır (§7).
- **Eklenen yerler** (kullanıcı kararı, 2026-11-14, "ekle"; §6.1 karar 8; karar 1a'nın sınıfı): 15 yer, 14 yeni satırda (`:770` ve `:771` tek satır): `:5`, `:342`, `:417`, `:738`, `:741`, `:747`, `:748`, `:770`, `:771`, `:785`, `:796`, `:801`, `:825`, `:867`, `:876`. Ayrıca `:59`'daki tarih etiketi var olan `:63`/`:64` maddesine eklendi. "(K0)" işareti bu 15 satırda.
- **Değerlendirilip eklenmeyenler:** `:12`–`:14` (modülün AOSPA'daki davranışı; `:9`'un düzeltilmiş cümlesi çerçeveliyor), `:66` (kimlik kuralı ve G11 sonucu hâlâ doğru), `:216` (§2.5'i `:174` tarihsel sayıyor), `:660` (§5.2'deki AOSPA bulgusu, tarihsel).
- **Son durum:** 97 madde. Her alıntı dosyada yalnız kendi maddesinin satır(lar)ında geçer; "satır içi" işaretli alıntı yalnız satır çapasının satırında aranır (betik, 2026-11-14).

#### 6.5.2 W5 yazım kuralları (`PROJECT_LOG.md` §1–§10)

1. **Kapsam:** yalnız §6.2'deki satırlar. §2.6 ve §11'e dokunulmaz (§2.6 I2a ve I2b'nin, §11 aşama kapanışlarınındır). Bölüm numaraları ve başlık sırası korunur; başlık metni yalnız §6.2'nin söylediği yerde değişir (`:43`, `:584`). Envanter dışında bayatlık görülürse düzeltilmez; dönüş bloğunda `open_issues`'a satır ve kısa alıntıyla yazılır.
2. **Çapa:** her değişiklik §6.2'deki satır numarası ve alıntıyla bulunur. `O2`'de betikle doğrulandı: her alıntı dosyada yalnız kendi maddesinin satır(lar)ında geçer (6.5.1). Düzenlemeden önce satır yeniden okunur; numara kaymışsa alıntı esastır. Alıntı bulunamazsa ya da hedef satırların dışında da geçiyorsa madde uygulanmaz ve `contract_deviations`'a yazılır. "Satır çapası" verilen maddelerde (`:669`, `:784`) satır o çapayla bulunur, değişiklik aynı satırdaki ikinci alıntıya yapılır.
3. **Şimdiki durum iddiası** (bugünü anlatan cümle, tablo hücresi ya da durum değeri) yerinde düzeltilir; cümlenin hâlâ doğru kısmı korunur, not eklenmez.
4. **Tarihsel cümle** (bir tarihte olanı anlatan) silinmez, yeniden yazılmaz; hemen arkasına tarihli not eklenir: ` *(YYYY-AA-GG notu: …)*`. Biçim §3.5'in geleneğidir ("satır sonundaki italik parantezler sonradan eklenmiş nottur", `:494`). Tarih notun yazıldığı gündür; olgunun kendi tarihi notun içinde yazılır (örnek metin: "2026-11-13'ten beri konusuz (`DEC-28`)"). Tablo hücresinde de aynı biçim kullanılır; not içinde `|` olmaz.
5. **Tarih damgaları:** `:3` ("Durum tarihi") ve `:43` (§2 başlığı) yazım tarihine çekilir.
6. **§3.5 commit geçmişi:**
   - Giriş cümlesi (`:494`): liste `integrate/impl-96` dalının commit'leridir, eskiden yeniye; ilk 62'si `origin/main`'de (`587e3b5`), `7fa0a51` yerel `main`'in ucudur (63); push durumu `O3OPN`'den.
   - Var olan satırlardaki notlar §6.2'ye göre (`:574`, `:577`, `:578`, `:581`, `:582`).
   - Yeni gruplar son grubun (`**2026-09-14 (2)**`) arkasına, aynı biçimde: `**YYYY-AA-GG (N)**` başlığı ve her commit için ``- `kısa hash` konu``. Tarih +0300 yazar tarihidir (CDATE). C1 ve Pencere 2 aşama commit'leri hash yerine adla yazılır: `- C1: <konu>`, `- 2 · O0+O1: <konu>`, `- 2 · O2: <konu>`. Konular A.6 `CLOG`'dan aynen alınır. Liste `O3OPN`'de ölçülen uca kadar gider; `2 · O3`'ün kendi commit'i listeye girmez.
7. **§4 kararlar:**
   - Başlık `## 4. Kararlar (DEC-01 … DEC-32)`; `:586` ve `:588` §6.2'ye göre.
   - `DEC-27`…`DEC-32` satırları `DEC-26` satırının (`:617`) arkasına, numara sırasıyla, aynı 6 sütunla (7 boru): `| DEC-NN | 2026-11-13 → 2026-11-13 | soru | hüküm | durum | ledger:N |`. Soru ve hüküm Ek A.1'den Türkçe özetlenir; kaynak `ledger:605`…`ledger:610` (LMAP). Durum `yanıtlandı`; `DEC-30` için `yanıtlandı; silmeyi kullanıcı yapar` ve `O3OPN`'deki ölçüm (tarih ve sonuç); `DEC-31` için `yanıtlandı ve yürütüldü`.
   - Konusuz kararlar (`DEC-07`, `DEC-08`, `DEC-22`, `DEC-24`, `DEC-25`, `DEC-26`): açık durum (`**AÇIK**`) şimdiki durum iddiasıdır ve "konusuz (`DEC-28`, 2026-11-13)" ile değiştirilir; yanıtlanmış durum tarihseldir, korunur ve arkasına "; 2026-11-13'ten beri konusuz (`DEC-28`)" eklenir. `DEC-07` ve `DEC-08`'in tarih hücresine " → konusuz 2026-11-13" eklenir. Önceki durumu ledger `Previous status, kept:` ile tutuyor; bu tablo bir özettir.
8. **§8 belge kaymaları:** çözülen satır silinmez. "güncel gerçek" hücresi `**Çözüldü (<kanıt>):**` ile başlar ve bugünkü gerçeği yazar (hücredeki eski "güncel" ifade bayatsa düzeltilir); kısmen çözülmüşse `**Kısmen çözüldü (<kanıt>):**` ve kalan iş. Kanıt: commit (kısa hash; C1 başlıkla), ledger satırı ya da IMPL kimliği. "ne diyor" hücresi kayıttır, değişmez.
9. **Atıflar:**
   - Ledger (`L:N`, `ledger:N`, `Planing-Ledger.md:N`): biçim korunur; numara LSH ile çevrilir ve A.6 `LMAP` ile karşılaştırılır. LMAP'te olmayan bir hedef, ledger'dan yalnız o satır okunarak (`:raw:N-N`) içerikle doğrulanır. LSH yalnız ekleme olduğu için kural §8'in "dosya:satır" hücreleri dahil her yerde geçerlidir.
   - `docs/pre-rental-plan.md` (`PRP:N`) ve `docs/build-environment.md`: N ≥ 3 için N + 8 (SH8).
   - `README.md` ve `UNTRACKED-BY-DESIGN.md`: C1 bu satırları yeniden yazdı ya da sildi. §8'deki çözülmüş satırın "dosya:satır" hücresi C1 öncesi numarayla kayıt olarak kalır; bugünkü yer çözüm notunda A.6 `C1MAP`'e göre verilir.
   - Commit'ler kısa hash'le (7 karakter); C1, C2 ve Pencere 2 aşama commit'leri yalnız başlıkla (C1'in ilk anılışında başlığı yazılır).
   - `NEXT_PROMPT.md`'ye yalnız adıyla atıf yapılır; bölüm numarası yazılmaz (dosya her aşamada yeniden yazılır).
   - Satır numarası yalnız o oturumda okunmuş güncel satırdan yazılır; tahmin yok.
   - Ek A olgu kimlikleri (`G…`, `D…`, `LSH`, `CLOG` …) günlüğe kaynak diye yazılmaz; kanıt doğrudan anılır (snapshot yolu, ledger satırı, commit, ölçüm zamanı). Aşama kimlikleri (`2 · O4` gibi) yazılabilir.
10. **Zamanla değişen olgular** (commit sayıları, push durumu, izlenen dosya sayısı, silinecek depoların durumu) yazım anındaki değerlerdir. `O3` orkestratörü bunları açılışta ölçer ve W5'i başlatmadan önce A.6'ya `O3OPN` satırı olarak yazar; W5 yalnız oradan alır. W5 git, `gh`, adb ya da doğrulayıcı çalıştırmaz.
11. **Dil ve bayt:** Türkçe; LF; CR 0; NUL 0; satır sonu dönüştürülmez. Her tablo satırının boru sayısı kendi tablosunun başlığıyla aynı kalır (örnek: §4 karar tablosu 7, §4 oturum kararları tablosu 4, §7 4, §8 5); yeni §4 satırları 7 boru; not ve alıntılarda `|` yok.
12. **Gizlilik:** IMEI ve `persist.sys.miui.sno` değerleri, token, anahtar, parola, sunucu adresi ve `dc27e5d0` dışındaki cihaz serileri yazılmaz.
13. **Kabul:** §6.3'teki W5 satırı ve 1–12. maddeler; dönüş bloğu 6.5.3'teki gibi.

#### 6.5.3 `O3` alt ajan ortak bağlamı

- **Proje:** `ishtar`, kullanıcının Xiaomi 13 Ultra'sı (`dc27e5d0`; SM8550, Sony IMX989) için root tabanlı kamera özelleştirmesidir: `ishtar-cam-modes` KernelSU modülü (v2.2 / versionCode 13), `ishtar-aon-fix` ve AGC (`org.codeaurora.snapcam`) yapılandırması. Ölçümlerin çoğu AOSPA A15 dönemine aittir; telefon 2026-11-13'ten beri HyperOS 4'te (`DEC-28`) ve projenin modülleri kurulu değil. Kanonik kayıt `Planner-docs/Planing-Ledger.md`; süreklilik belgeleri `PROJECT_LOG.md`, `NEXT_PROMPT.md` ve `ORCHESTRATION_PLAN.md`.
- **Olgu kaynakları:** plan Ek A.1 (kararlar), A.2 (2026-11-13 olguları) ve A.6 (Pencere 2 olguları, `O3OPN` dahil). Ek A'da olmayan olgu yazılmaz; gerekiyorsa raporlanır. Cihaz olguları 2026-11-13 ölçümüdür ve Pencere 2'de teyit edilmedi; AOSPA A15 kanıtı HyperOS 4'e, arka kamera kanıtı ön kameraya genellenmez. Ledger ile plan çelişirse ledger kazanır; çelişki raporlanır.
- **Dil ve bayt:** `PROJECT_LOG.md`, `NEXT_PROMPT.md` ve plan gövdesi Türkçe; Ek A, `Planner-docs/`, `docs/`, `README.md` ve `UNTRACKED-BY-DESIGN.md` İngilizce. Ledger, `Main-Planing.md` ve `Autopsy.md` CRLF, öteki dosyalar LF; satır sonu dönüştürülmez. `Project-Ontology.md`'de 2 NUL bayt var; orada grep sessiz kalabilir. Büyük dosyalar parça parça okunur (ledger satırları tek tek, `:raw:N-N`).
- **Kimlik ve atıf:** 6.5.2 madde 9 ve 12. İnceleme raporları değer değil anahtar ve satır yazar; sır, Luhn adayı ya da seri numarası için yalnız dosya ve satır.
- **Sahiplik:** W5 yalnız `PROJECT_LOG.md` §1–§10'a yazar (§2.6 hariç). SEC-A1, SEC-A2, SEC-A3 ve REV-3 salt-okurdur. §3'teki sıcak noktalar, `NEXT_PROMPT.md` ve bütün git işlemleri orkestratöründür. Ajan başka bir dosyada sorun görürse düzeltmez, raporlar. Ajanlar doğrulayıcı, test, formatlayıcı, git, `gh` ya da adb çalıştırmaz. Aynı anda en fazla 4 uygulama ajanı çalışır; `O3`'te yalnız W5.
- **Girdiler:** SEC/REV girdilerini orkestratör §6.4'teki komutlarla aynı oturumda `local://` altına üretir ve yolunu görev metnine yazar (`local://` oturumlar arasında taşınmaz). Aralık `origin/main..HEAD`; HEAD, `O3` açılışındaki uçtur (`2 · O2` kapanış commit'i).
- **Dönüş bloğu (zorunlu):** `status` (`done`, `partial` ya da `blocked`), `changed_files` (salt-okur ajanlarda boş), `acceptance` (kriter / karşılandı mı / kanıt), `contract_deviations` (sözleşmeden her sapma ve nedeni), `open_issues` (inceleme ajanlarında bulgular: `P0`–`P3`, dosya:satır, kanıt, önerilen yönlendirme).
- **Yönlendirme** (§6.1 karar 3 ve 4, §0 adım 6): P0/P1 bulgusu FIX'e ya da beklenmedik durum olarak kullanıcıya gider; ledger bulguları §10'a (koşu 21); öteki dosyalardaki bulgular düzeltici task ile sonraki kapanış commit'ine; amend yok.

## 7. Pencere 3 — Planlama koşusu 21 (Step 1 + Step 2)

**Önkoşul:** Pencere 2 `done`. **Başlamadan kullanıcıya sorulacaklar** (`3 · O0`'ın ilk işi; yanıtlar tarihle bu bölüme yazılır):
1. **K9:** 50MP HAL katmanı HyperOS 4 HAL'inde yeniden türetilsin mi? Faz 3/4 benzeri statik analiz gerekir (R10 bağlam riski). Türetilmezse HAL katmanı HyperOS 4'te devre dışı kalır, sensör katmanı sürer.
   - **Yanıt (2026-11-15):** Hayır, şimdilik. HAL katmanı HyperOS 4'te kapalı kalır, sensör katmanı sürer; K9 ileride yeniden açılabilir. Karar `DEC-33`; ledger'a koşu 21 yazar (§2, K9 satırı). Aday alt plan 3 düşer.
2. **Kutucuk/WebUI zinciri:** Uzun basış `com.rifsxd.ksunext`'e bağlı ve bu ROM'da yok. Kurulu KernelSU `4.3.0-r1`'in yöneticisi ve WebUI desteği önce ölçülür. Zincir uyarlansın mı, kaldırılsın mı?
   - **Yanıt (2026-11-15):** Uyarlansın. Kullanıcı beyanı: telefonda yönetici artık `com.rifsxd.ksunext` değil, SukiSU (salt-okur ölçüm `3 · O1`'de doğrular). Kullanıcı fikri, koşu 21 değerlendirir: aynı arayüzlü yeni bir uygulama modülle sistem uygulaması olarak mount edilsin; amaç kök yöneticileri arasında uyum.
3. **AGC tuzakları:** 10 tuzak 37 değerinde kurulu. HyperOS 4 için yeni, korumalı bir temizleme prosedürü kapsama girsin mi? Var olan tek prosedür (`docs/phase3-preconditions.md:71-119`) AOSPA'ya özel ve yedeksiz.
   - **Yanıt (2026-11-15):** Evet. HyperOS 4 için yedekli yeni bir temizleme prosedürü kapsamda (aday alt plan 6); yedeksiz temizlik yasağı sürer.
4. **v2.3 kapsamı:** `Kullanim.txt` (`DEC-29`), modül içindeki bayat yorumlar, tile-app `versionName`.
   - **Yanıt (2026-11-15):** Üçü de: `Kullanim.txt` (`DEC-29`), modüldeki bayat yorumlar, tile-app `versionName`.
5. **Faz 8'in emekliliği:** K7 = (a) seçeneği Faz 8'i belirler: (i)'de Faz 7 ve 8 tümüyle emekli olur; (ii)'de Faz 8 ancak kısmen emekli olur, başlığı (`Main-Planing.md:221`) ve yol haritası satırı (`:126`) yeniden yazılır.
   - **Yanıt (2026-11-15):** (i). Yeni faz "ClaudeQB Phase 10" (klasör `Faz-10-Plans`); Faz 7 ve 8 tümüyle emekli, satırları ve bölümleri yerinde tarihli notla kalır.
6. **`Faz6.2`'nin VAL-BUILD bağı:** ledger `:98` (`Faz6.2`, `verified`) "`VAL-BUILD` still deferred to Phase 7 by design" diyor; Index `:177` doğrulamayı Faz 7'ye bağlıyor. Faz 7 emekli olunca bu doğrulama düşer mi, yeni bir alt plana mı taşınır?
   - **Yanıt (2026-11-15):** Düşer. ROM derlemesi bırakıldığı için (`DEC-28`) doğrulama konusuz; ledger `:98` ve Index `:177`'ye not düşülür, yeni alt plan açılmaz.
7. **Step 1'in yazamadığı Hetzner satırları:** `AUDIT-FIX-57` ayrıca `Project-Comprehension.md` (`CQ-13` `:25`, `EV-20` `:51`) ve `docs/reverse-engineering-toolchain.md:220`'yi kapsıyor. Step 1 yalnız `Main-Planing.md`'yi yazar; Step 2 `Planner-docs/` altına yazabilir ama Comprehension §3'teki sıcak nokta listesinde yok; toolchain belgesi ikisinin de sınırı dışında. Bunları kim, ne zaman düzeltir (koşu 21'de orkestratör ya da §10 yoluyla 12. denetim)? Step 1.5 (Autopsy) çalışırsa Comprehension ve Ontology onun yazma sınırı içindedir (`SKILL.md:93`; soru 8).
   - **Yanıt (2026-11-15):** Koşu 21'de orkestratör düzeltir: Comprehension `CQ-13`, `EV-20` ve toolchain `:220` (Ontology değişmez 11 zaten orkestratörün); 12. denetim doğrular.
8. **Oturum düzeni:** ClaudeQB Step 2'yi yeni bir oturuma devreder (`SKILL.md:11`; `workflow-quality.md:120` istisna anmadan "must" der); bütçe kuralı da Step 1 ile Step 2'yi ayrı oturumlara koyar (aşağıda, "Oturum düzeni ve bütçe"). Var olan bir projede ClaudeQB Step 1'den sonra Step 1.5'i (Autopsy) kendiliğinden çalıştırır (`SKILL.md:78-79`); bu projede Step 1.5 yalnız koşu 2'de çalıştı (ledger `:18`), Step 1 değişiklikleri (koşu 12, 16, 17) onu atladı. Koşu 21'in Step 2'si sınırlı olacak (yalnız yeni alt planlar; emsal: koşu 10, 13–15, 19 ve 20 "bounded amendment", koşu 12 "Step 2 + Step 1 amendment — bounded"; yeni alt plan yaratan sınırlı Step 2: koşu 18, yalnız Faz 7 ve 8, ledger `:39`; Step 1 değişikliği: koşu 17, `Main-Planing.md` ve Ontology, ledger `:38`; ledger §2), oysa `run-step2.md:27` bütün ana fazları ve destek belgelerini tam okumayı ister. Sınırlı Step 2 ve Step 1.5'in atlanıp atlanmayacağı onaylanıyor mu?
   - **Yanıt (2026-11-15):** Onaylandı: Step 1 ve Step 2 ayrı oturumlarda, Step 2 yalnız yeni alt planlarla sınırlı. Step 1.5 (Autopsy) atlanır.

**Açılışta ayrıca:** `2 · O5`'in FF, RID, push ve LSR sonuçları takip commit'iyle PROJECT_LOG §11'e yazıldı (2026-11-15). Açılışta `git ls-remote origin` ile yeniden doğrulanır (takip commit'inin push durumu dahil) ve PROJECT_LOG'un push durumunu anlatan cümleleri bu sonuca göre güncellenir (§6.5.1). Takip commit'i push edilmemişse `3 · O0` açılışta sorar (§0 adım 5).

Bu cümlelerin `2 · O3` kapanışındaki yerleri: §2.1 `:49`, §3.5 giriş cümlesi `:494`, §4 Push satırı `:653`, §8 `:803` ve `:844`, §9 `:893`. Depo silme durumunu anlatan yerler (silme ölçülünce Pencere 3 günceller; I2a ve I2b ölçüm sonucunu yalnız §2.6 ve §11'e yazar): §1 `:15`, §2.1 `:51`–`:52`, §3.1 `:292` ("girdiler GitHub'da"; `2 · O5` REV-1), §4 `:608` (`DEC-01` notu) ve `:634` (`DEC-30`), §8 `:846`, §9 `:893`–`:894`.

§2.6 her yazımda (takip commit'i dahil) aynı satır sayısıyla yazıldı, `2 · O5`'in REV-1 düzeltmeleri satır eklemedi; yerler yine de alıntıyla bulunur.

**Oturum düzeni ve bütçe (kullanıcı isteği, 2026-11-15; §0 adım 9):** Pencere 2'nin aşamaları 46–121 tur sürdü ve 323k–738k bağlama ulaştı (Ek A.7). Hedef 240k, oturum başına yaklaşık 30–34 yürütme turu ya da 15–20 yazım turudur. Varsayılan dağılım aşağıdadır; `3 · O1` yanıtlara göre kesinleştirir ve §1'e satırlarını ekler. Tahminler §0 adım 9'daki formülle, 20 KB'lık `NEXT_PROMPT.md` (açılış ≈ 35k) için hesaplandı.

| Oturum | Kapsam | Tahmin |
|---|---|---|
| `3 · O0` | Açılış ölçümleri (`W3OPN`, keşif envanterinin ilk satırı) ve "Açılışta ayrıca"; sekiz soru; üç scout (aşağıda); keşif envanteri bu bölüme (≤ 15 KB) | 35k + 25 × 6k ≈ 185k |
| `3 · O1` | Aşama ve görev tablosu, tahmin sütunuyla; kullanıcı onayı | 35k + 15 × 10k ≈ 185k |
| `3 · O2a` | Step 1: `Main-Planing.md` (metni kullanıcı onaylar); `--mode step1 --strict` | 35k + 15 × 12k ≈ 215k |
| `3 · O2b` | Step 2 kontratı: alt plan listesi, ortak bağlam, ledger, Index ve Ontology hedef tablosu | 35k + 15 × 12k ≈ 215k |
| `3 · O3a`, `3 · O3b` | Step 2 taslakları: oturum başına en çok üç alt plan (ortanca alt plan 19 KB); betikle doğrulanır, `cp` ile yerine konur | her biri 35k + 25 × 6k ≈ 185k |
| `3 · O4` | Ledger (satırlar 1–9 KB), Index ve Ontology; geçitler | 35k + 30 × 6k ≈ 215k |
| `3 · O5` | İncelemeler (dönüş ≤ 4 KB), FIX, kapanış; FF ve push (onay) | 35k + 30 × 6k ≈ 215k |

- **`3 · O0` scout'ları** (her biri ≤ 4 KB döner): S1 ClaudeQB yönergeleri (`SKILL.md`, First-, Autopsy- ve Second-Planner, `workflow-quality.md`, `run-step2.md`) ve doğrulayıcı kipleri; S2 Step 1 yüzeyleri (`Main-Planing.md`, `AUDIT-FIX-41`, `-42` ve `-57`, Comprehension ve Ontology yerleri); S3 ledger ve Index çapaları ile aday alt planlar için mevcut kanıt.
- **Step 1.5 (Autopsy)** çalışacaksa (soru 8) ayrı bir oturumdur: `Autopsy.md` 40 KB, Ontology 84 KB, Comprehension 55 KB; okuma scout'larla, yazım `cp` ile.

**Step 1 — `Main-Planing.md`** (CRLF; yalnız orkestratör; metni kullanıcı onaylar):
- Faz 7 ve Faz 8 §6 yol haritasından **silinmez**; satırlar ve bölümler yerinde, tarihli notla emekli edilir ("Retired 2026-11-13 by `DEC-28`"). Satır silmek `extra_phase_folder_without_main_phase` uyarısı üretir; `--strict` bunu hataya çevirir.
- K7 = (a) için iki seçenek; seçimi kullanıcı yapar: (i) yeni Faz 10 (klasör `Faz-10-Plans`; her yerde "ClaudeQB Phase 10" diye yazılır, çünkü `50MP-Entegrasyon-Plani.md`'nin Faz 10'u ayrı bir şeydir) ya da (ii) Faz 8'in kamera yarısının HyperOS 4'e yeniden hedeflenmesi (yeni alt planlar `Faz8.4` ve sonrası). Seçenek (ii) "Faz 7 ve 8 emekli" ile çelişir: Faz 8 ancak kısmen emekli olur; başlığı (`Main-Planing.md:221`, "Camera work on Android 16 and kernel LTS merge") ve yol haritası satırı (`:126`) kamera ve kernel işini birleştirdiği için ikisi de yeniden yazılır, ilk hücre `8` kalır (soru 5).
- R8 gerçekleşti (HAL `2a955e68…`); R9 konusuz. Hetzner ifadelerini yalnız `AUDIT-FIX-57` kapsar (`Sub-Planing-Audit.md:380`): `Main-Planing.md:211` Faz 7 bölümündedir ve emekli bölümle birlikte kapanır; `:75` (§3) ve `:265` (§7, R9) emekli bölümlerin dışındadır, ayrı düzenleme ister. Bulgu aynı ifadeyi dört yerde daha sayar: `Project-Comprehension.md` `CQ-13` (`:25`) ve `EV-20` (`:51`), Ontology değişmez 11 (`:429`), `docs/reverse-engineering-toolchain.md:220` (soru 7). Aynı Step 1 değişikliğine bağlı iki bulgu daha var: `AUDIT-FIX-41` §8 adım 5 (`:277`, AGC fotoğraf boyutu pini; Audit `:383`) ve `AUDIT-FIX-42` `:22`, `:61` ve `:288`'deki Android 16 / `beryl` ifadeleri (Audit `:384`).
- §4'teki hedef son durum ("From a clean AOSPA build…") K7 = (a)'ya göre yeniden yazılır.

**Ledger (orkestratör):** §2'ye koşu 21 satırı; §3'e yeni snapshot (`SNAP-…-MAIN`, Step 2 varsa `-SUBPLANS`). §4'te `Faz7.2`, `Faz7.3`, `Faz8.1`, `Faz8.3` → `superseded` (`Superseded By` kanıtlı olmalı; bugün dördünde de `-`); `Faz6.1` koşu 21'in kararıyla; `Faz6.2`'nin VAL-BUILD bağı (ledger `:98`, Index `:177`) soru 6'ya göre; yeni alt planlar `planned`. Silme yapıldıysa `DEC-30` yürütme notu; `DEC-32`'ye koşu 21 atfı.
**Index (orkestratör):** Emekli alt planlar üstü çizili ve "Do not revive" notlu; yeni girdiler eklenir.
**Ontology (orkestratör, bayt-korumalı):** Değişmez 10 (gerçekleşti) ve 11 (`:429`; emekli; Hetzner, `AUDIT-FIX-57`).
**Comprehension ve `docs/reverse-engineering-toolchain.md:220`:** sahibi soru 7'ye göre belirlenir; Step 1 ikisine de, Step 2 toolchain belgesine yazamaz.
**Step 2 — yeni alt planlar:** Paralel task ajanları her alt planın **taslağını** aynı oturumda `local://` altına yazar (§0 adım 8); son `Faz-N-Plans/*.md` dosyalarını orkestratör yazar (ClaudeQB: "parent writes final artifacts", `run-step2.md:17`). Biçim: H1 `# Faz N.M — …`; 13 başlık, her biri en az 20 karakter; §9'da uygulama sözleşmesi tablosu (`Path | State | Purpose | Validation Command IDs`; State ∈ existing, modified, proposed, generated, external, deferred); TODO/TBD yok; §3, §6, §8 ve §11 gövdelerinde 80+ karakterlik aynı cümle, mevcut 42 alt plan dahil, toplam 5 ya da daha çok kez geçmez (aynı dosyadaki tekrarlar da sayılır; doğrulayıcı `:201-202`, `:954-960`); numaralarda boşluk yok.
**Aday alt planlar** (koşu 21 kesinleştirir):
1. HyperOS 4 kamera yığınının salt-okunur ölçümü: değişmez 3 için servis adları (`setmode.sh:52-58`, `:79-83` AOSPA adlarını kullanıyor), `chcon` etiketleri, `/data/adb/ksu/.allowlist`, yönetici ve WebUI.
2. Sensör katmanı: v2.2 değişmeden HyperOS 4'te, smoke bracket ile (kurulum kullanıcıda).
3. 50MP HAL katmanının yeniden türetilmesi (yalnız K9 = evet).
4. Kutucuk/WebUI zinciri.
5. v2.3 sürümü: `Kullanim.txt`, sürüm yerleri, CHANGELOG, manifest; AON modülünün HyperOS 4'te gereksizliği.
6. AGC tuzak denetimi ve korumalı temizleme (kullanıcı kapsama alırsa).

**Geçitler:** `--mode step2 --strict` ve `--mode step3-preflight --strict`; `subplan_count` yeni toplamı gösterir.

**Doğrulayıcı tuzakları** (`validate_planner_docs.py`, `O2`'de 2026-11-14'te okundu; numaralar o dosyanın satırlarıdır):
- Yol haritası satırı `^\|\s*(\d+)\s*\|` ile okunur (`:163`). Faz 7/8 satırını silmek ya da ilk hücreyi `~~7~~` yapmak fazı ana plandan düşürür; var olan `Faz-7-Plans`/`Faz-8-Plans` klasörleri `extra_phase_folder_without_main_phase` uyarısı verir (`:1011-1013`). `--strict` her uyarıyı `strict_warning=…` hatasına çevirir (`:1286-1290`). §6'nın tamamı taranır (`### Phase N` alt bölümleri ve öteki tablolar dahil; `:391-400`, `:536-541`): ilk hücresi sayı olan her tablo satırı faz sayılır; emeklilik notları ve yeni tablolar ilk sütuna sayı koymaz.
- `superseded` §4 satırı kanıtlı bir `Superseded By` ister (`:848-849`, uyarı `ledger_superseded_missing_target`); boş hücre, `-`, `none`, `n/a` ve `unknown` kanıt sayılmaz (`UNKNOWN_CELL_VALUES`, `:284`).
- Denetim durumu dosyadaki ilk `… status: PASS|PASS_WITH_WARNINGS|BLOCKED` biçimli eşleşmeden okunur (büyük-küçük harf duyarsız; `overall audit status`, `final status`, `denetim durumu` biçimleri de sayılır; `:1070-1078`); bugün `Sub-Planing-Audit.md:18`. Yeni durumun üstünde eski bir durum alıntılanırsa o okunur. Değer ayıraçtan hemen sonra, yalnız boşlukla ayrılmış gelmeli (`:1071-1075`): `**Overall audit status: PASS_WITH_WARNINGS.**` eşleşir, `**Overall audit status:** PASS_WITH_WARNINGS` eşleşmez; dosyada başka eşleşme yoksa `audit_status_missing` hatası çıkar (`:1231`).
- Seçenek (i): klasörü olmayan `10` satırı `--strict` olmadan da hatadır (`missing_phase_folder`, `:1010`), alt plansız klasör de (`phase_has_no_subplans`, `:1039`). İkisi `--mode step2` ve üstünde çalışır, `--mode step1`'de çalışmaz (`:1328-1329`): Step 1 ile Step 2 arasında `--mode step1 --strict` ve, Step 1.5 çalışırsa, `--mode autopsy --strict` anlamlıdır (`autopsy` kipi Step 1 denetimine ek olarak `Autopsy.md`'yi (zorunlu), Ontology'yi, ledger'ı ve Comprehension'ı denetler, klasör kontrolü yapmaz; `:1330-1333`, `:854-889`; taban değeri Pencere 3'te ölçülür). Kipler: `step1`, `autopsy`, `step2`, `step3-preflight`, `step3`, `step4`, `all` (`:1317`).
- Alt plan dosya adı `FazN.M-` önekiyle başlar (büyük F), önekten sonrası küçük harfli kebab-case olmalı (`:157`; değilse `invalid_subplan_filename` hatası, `:582`); H1 ayıracı yalnız `—` ya da `-` (`:165`; en dash `–` `missing_or_invalid_h1` hatası verir, `:926`). Uygulama sözleşmesinde `Purpose` ve `Validation Command IDs` kanıtlı olmalı; `-` ya da `none` hatadır (`:990-993`).
- En az 160 karakterlik aynı `## 3. Description` ya da `## 7. Planned Work Breakdown` gövdesi üç ya da daha çok dosyada geçerse `repeated_section_body` uyarısı verir (`:949-952`, `:1045-1049`); `--strict`'te hata.
- Dosyası olmayan alt plana ledger §4 satırı `missing_ledger_subplan` uyarısı verir (`:829-830`): satırlar Step 2 dosyaları yazdıktan sonra eklenir. §4 tablosundaki boş satır tabloyu böler; ardından gelen satırlar başlıksız kalır ve sessizce okunmaz (`markdown_tables`, `:404-429`).
- `--mode step4 --strict` kuyruğu yalnız denetim dosyasından okur: 11. denetimin geçersiz kuyruğuyla da p0/p1 geçidi geçer (V2). Pencere 4'ten önce Step 4 başlatılmaz.

**ClaudeQB süreci:** Step 1'in handoff dosyası yok (`references/handoffs/` yalnız `run-step2.md`, `run-step3.md`, `run-step4.md`). Step 1 yalnız `Main-Planing.md`'yi yazar (`First-Planner.md:10-11`, `:363-364`); Step 2 yalnız `Planner-docs/` altına yazar (`Second-Planner.md:20-25`) ve `Main-Planing.md`'yi düzenleyemez (`:61`). `/claudeqb:claudeqb` komutunu Claude Code'da kullanıcı yazar (`SKILL.md:4`, `disable-model-invocation: true`); omp altında dosyalar mutlak yolla okunur, doğrulayıcı `py -3 <mutlak yol>` ile çalışır. Sınırlı Step 2 ve Step 1.5 için soru 8. Var olan bir projede ClaudeQB Step 1'den sonra Step 1.5'i (Autopsy) kendiliğinden çalıştırır (`SKILL.md:78-79`); Step 1.5 `Autopsy.md`'yi (CRLF), kanıt varsa `Project-Ontology.md` ve `Project-Comprehension.md`'yi de yazabilir (`SKILL.md:93`); Step 1 ve Step 1.5 var olan ledger'ı güncelleyebilir (`Second-Planner.md:45`). Step 1.5'in yönergesi `references/Autopsy-Planner.md` (`SKILL.md:90`). Atlanıp atlanmayacağı soru 8'dedir.

### 7.1 Keşif envanteri (`3 · O0`, 2026-11-15, ağaç `6632a18`)

`3 · O1`'in ve sonraki aşamaların girdisi: dört salt-okur scout (S1 ClaudeQB ve doğrulayıcı; S2 Step 1 yüzeyleri; S3 ledger ve Index; S4 aday alt planlar için depo kanıtı; §7'deki S3 bağlam güvenliği için ikiye bölündü). Satır numaraları `6632a18` ağacına aittir ve kayabilir; yerler alıntıyla doğrulanır. V = `validate_planner_docs.py`; skill dosyaları `…/claudeqb/0.2.1/skills/claudeqb/` altında; ledger, Index, Audit, Comprehension ve Ontology `Planner-docs/` altında. Kimlikler bu plana aittir (§3, Adlandırma).

| Kimlik | Konu | Olgu | Kaynak ve tarih |
|---|---|---|---|
| W3OPN | `3 · O0` açılışı | Dal `integrate/impl-96`, ağaç temiz, 76 commit, uç takip commit'i (`Window 2 follow-up: context budget and stage sizing`); `main` = `origin/main` = uç; `origin/main..HEAD` = 0; etiket yok; 350 izlenen dosya. `ls-remote`: `HEAD`, `main`, `integrate/impl-96` = takip commit'i (tam hash'ler eşleşti). Durum (b): reflog'da FF 08:58:01Z, push 08:58:04Z. `gh api`: `ishtar`, `android_local_manifests`, `android_device_xiaomi_ishtar`, `ishtar_cam_modes` 200 | git, `gh api`; 2026-11-15T11:57:29Z–11:57:56Z |
| W3F01 | Step 1 sınırı | Step 1 yalnız `Main-Planing.md` yazar (First-Planner.md:10-13, :363-364; SKILL.md:77). Ledger'ı (koşu satırı, snapshot) yalnız kullanıcı açıkça isterse günceller (First-Planner.md:78; Second-Planner.md:45); koşu 16 ve 17 böyle yaptı (ledger :37-38). Step 2'ye talimat `Main-Planing.md` §9'a yazılır (First-Planner.md:294-295); devir komutu SKILL.md:102 | S1, 2026-11-15 |
| W3F02 | `Main-Planing.md` biçimi | 11 sabit başlık, sırayla (V:28-40; yinelenen ya da sırasız başlık hata, V:371-389). §6'nın tamamında ilk hücresi sayı olan her tablo satırı faz sayılır (V:163, V:391-401, V:536-549): 7 ve 8 satırlarının ilk hücresi korunur, emeklilik notu öteki hücrelere yazılır, yeni 10 satırı eklenir; §6'ya başka sayılı tablo girmez | S1, 2026-11-15 |
| W3F03 | Doğrulayıcı kipleri | Kipler step1, autopsy, step2, step3-preflight, step3, step4, all (V:1317). Step 1'den sonra yalnız `--mode step1 --strict`; Step 2'den önce `--mode step2` `missing_phase_folder=Faz-10-Plans` verir (V:1010). Faz numaraları ardışık olmak zorunda değil (V:1008-1013), klasör içi alt plan numaraları ardışık (V:1040-1043). `subplan_count` geçerli adlı her alt plan dosyasını sayar (V:1005) | S1, 2026-11-15 |
| W3F04 | §7 tuzaklarının denetimi | "Doğrulayıcı tuzakları"ndaki 14 iddianın 14'ü doğru. Ek ya da düzeltilmiş numaralar: denetim durumu ayrıştırması V:1070-1084; superseded başlık eşleşmesi V:810; `--strict`'in eski ledger uyarısı istisnası V:1288; §6 taraması V:391-401 ve V:536-549 (`###` alt bölümleri dahil) | S1, 2026-11-15 |
| W3F05 | Step 1.5'in atlanması | SKILL.md:79 var olan projede Step 1.5'i bekler; tanımlı tek atlama boş depo (:80). Kullanıcının açık "farklı akış" kararı geçerli (SKILL.md:11); doğrulayıcı `Autopsy.md`'yi yalnız `--mode autopsy`'de ister (V:642-664). Ledger'da atlama kalıbı yok (yalnız koşu 2, :18); öneri: koşu 21 satırında ve `Main-Planing.md` §10'da bir cümle (`Autopsy.md` bayat kalır) | S1, S3; 2026-11-15 |
| W3F06 | Sınırlı Step 2 | Sınır meşru: fazlar 1–9 için durma kuralı karşılanmış (Second-Planner.md:602-612), var olan alt plan yinelenmez (run-step2.md:24; Second-Planner.md:115), emsal ledger :22, :28, :34-41. Yine de bütün fazların ve destek belgelerinin tam okuması gerekir (run-step2.md:16, :27); Step 2 `Main-Planing.md`'yi ve faz sırasını değiştiremez (Second-Planner.md:61-62). Index güncellenmezse `unindexed_subplan` hatası (V:1017): sınır Index'i de kapsar | S1, 2026-11-15 |
| W3F07 | Alt plan biçimi | Dosya `Faz10.M-kebab-case.md` (V:157); H1 `# Faz 10.M — Başlık`, yalnız em dash ya da tire (V:165, V:926); 13 sabit başlık (V:121-135); §9 tablosu Path, State, Purpose, Validation Command IDs, en az bir satır, State ∈ existing, modified, proposed, generated, external, deferred (V:965-993); `--strict`'te TODO, TBD, FIXME yasak (V:191-199) | S1, 2026-11-15 |
| W3F08 | Emeklilik ve oturum | Skill'de yalnız `superseded` var; kanıtlı `Superseded By` ister, örneğin `DEC-28` (V:848-849, V:284). "Do not revive" proje geleneği (Index :121, :124; Audit :310-311). workflow-quality.md:120: "Step 1 must hand off Step 2 as text for fresh Claude Code session"; skill'i yalnız kullanıcı çağırır (SKILL.md:4, :102); taze oturumda `--strict` (SKILL.md:161); Second-Planner.md:681-686'daki Step 3 metni SKILL.md:124'tekinden farklı | S1, 2026-11-15 |
| W3F09 | `Main-Planing.md` haritası | `##` başlıkları: §1 :6, §2 :26, §3 :43, §4 :77, §5 :91, §6 :113, §7 :245, §8 :271, §9 :284, §10 :302. Yol haritası başlığı :117, faz N satırı :118+N (1–9). Faz 9 var ("Release engineering", :233); "Phase 10" hiçbir yerde yok. Faz 7 bölümü :207–:219 ("Android 16 build environment", satır :125); Faz 8 bölümü :221–:231 ("Camera work on Android 16 and kernel LTS merge", satır :126); §4 hedefi :79 | S2, 2026-11-15 |
| W3F10 | Riskler ve denetim hedefleri | Risk kaydı tablo değil, kalın paragraflar (R12 :255, R4 ile R5 arasında); R8 :263, R9 :265, R10 :267. Hetzner üç yerde ("a rented Hetzner VDS"): :75 (§3), :211 (Faz 7), :265 (R9). `AUDIT-FIX-41` hedefi :277 (`4096x3072` pini; :24 aynı kilometre taşı); `AUDIT-FIX-42` hedefleri :22, :61, :288 ("Do not expand yet. Phases 7, 8, and 9…") | S2, 2026-11-15 |
| W3F11 | Kararlarla yanlışlaşan satırlar | `Main-Planing.md`'de 25 satır: :8, :10, :22, :24, :28, :30, :34, :51, :61, :73, :75, :79, :81, :83, :125, :126, :199, :201, :203, :205 (Faz 6, ROM derlemesini varsayıyor), :263, :265, :288, :298, :300. Scaleway, ksunext, SukiSU, HyperOS ve `DEC-28` dosyada geçmiyor | S2, 2026-11-15 |
| W3F12 | Audit | Durum satırı :18 `**Overall audit status: PASS_WITH_WARNINGS.**`; `AUDIT-FIX-57` :380, `-41` :383, `-42` :384; kuyruk metni :57, :156, :350. `-57`'nin (Scaleway) ve `-42`'nin (`DEC-24`/`DEC-26`) çözümleri `DEC-28` ile geçersiz: koşu 21 yeni ifadeyi seçer. `AUDIT-FIX-22` (:377) yazarını (`F8.1-10`, Faz 8) kaybeder | S2, 2026-11-15 |
| W3F13 | Comprehension | `CQ-13` :25 ("Ubuntu 22.04 LTS, Hetzner CCX53"), `EV-20` :51. Sıcak nokta listesi §3'te değil §6'da (başlık :136, maddeler :138–:141; :141 "50 MP … The active frontier"). Öteki bayat satırlar :9, :42, :45 (KernelSU-Next), :53, :95, :101, :120, :149, :167. :145'teki "Faz 10" yeni fazla karışabilir: metin "ClaudeQB Phase 10" der | S2, 2026-11-15 |
| W3F14 | Ontology ve toolchain | Ontology değişmez 10 :428 ("Blob binding"), 11 :429 (Hetzner CCX53); öteki yerler :8, :19 (`beryl`, Faz 7), :117, :118, :391, :393, :394, :447 (OQ-11). NUL baytlar :313 ve :316 (ikinci yama tablosu, başlık :311). `docs/reverse-engineering-toolchain.md:220` Hetzner satırı; başlık :213 "Boundary against the Phase 7 build toolchain": §7'nin tamamı (:213–:229) Faz 7'yi varsayar | S2, 2026-11-15 |
| W3F15 | Ledger geometrisi | Bölümler §1 :5, §2 :13, §3 :45, §4 :62, §5 :109, §6 :526, §7 :548, §8 :572. Tablo başlığı, satır başına boru, ilk–son satır: §2 :15, 6, :17–:41; §3 :47, 7, :49–:58; §4 :64, 10, :66–:107; §8 :574, 7, :576–:610. Tablo içinde eski boş satırlar: §2 :24, :27, :31, :33, :35; §3 :55; §8 :588, :590, :592 (tabloyu böler, V:404-429). Yeni satır son satırın hemen altına | S3, 2026-11-15 |
| W3F16 | Ledger koşu ve snapshot | §2: koşu 17 :38 "Step 1 amendment — Phase 7 and Phase 8 re-scoped"; 18 :39 "Step 2 — Second-Planner (… re-plan …)"; 19 :40 ve 20 :41 "Step 2 — bounded amendment". Koşu 20 kalıbı: "bounded: no phase re-decomposed, no sub-plan created or deleted, the set stays at 42, and no snapshot is cut"; koşu 12 :30 "Step 2 + Step 1 amendment — bounded". §3: MAIN :49–:52, `SNAP-2026-09-10-SUBPLANS` :58 etkin; ID deseni `SNAP-YYYY-MM-DD-` + MAIN, SUBPLANS ya da AUTOPSY; faz sayısı her satırda 9 | S3, 2026-11-15 |
| W3F17 | Ledger §4 | `Faz4.1` :87 ve `Faz4.7` :93 superseded, Superseded By `SNAP-2026-09-03-MAIN`. `Faz6.1` :97 implemented ("planning run 21 decides the row"); `Faz6.2` :98 verified ("`VAL-BUILD` still deferred to Phase 7 by design"; sonraki eylem `docs/aon-verification.md` §8.2); `Faz7.2` :100, `Faz7.3` :101, `Faz8.3` :104 planned; `Faz8.1` :102 implemented; dördünde Superseded By `-`. `Faz7.1` :99 ve `Faz8.2` :103 verified, 2026-11-13 notu yok | S3, 2026-11-15 |
| W3F18 | Ledger §8 | `DEC-27`…`DEC-32` :605–:610. `DEC-30` :608 "Execution pending … confirmed with `gh api` (404 = deleted)"; `DEC-32` :610 kapsamı koşu 21'e bırakır. Not kalıbı Status hücresine tarihli ek: `**UPDATED 2026-11-13 (…):**` (:602), `**Update 2026-09-10:**` (:601); `DEC-31` :609 "ANSWERED … and executed". §8 karar sırasıyla dizili, kimliğe göre değil | S3, 2026-11-15 |
| W3F19 | Index | §1 :12, §2 :20, §3 :72, §4 :162 (4a :182, 4b :207, 4c :232, 4d :256), §5 :273, §6 :290, §7 :305–:415. Emekli giriş biçimi :121 (üstü çizili ad, "superseded … Do not revive it to unblock anything."). Faz 7/8 yerleri :36–:37, :144, :146–:148, :150, :152–:154, :179–:180, :262–:267, :275–:279, :293. :177 "whose verification is registered against Phase 7" (`VAL-BUILD` dizesi yok). Phase 10 yerleri: tablo :38'den, blok :160'tan, öncelik 16 :180'den, "4e" :271'den, koşu notu :415'ten sonra; sayılar :292–:293 | S3, 2026-11-15 |
| W3F20 | Aday 1: kamera yığını | `setmode.sh` `cameraserver`, `vendor.camera-provider`, `vendor.camera-provider-2-7-ext`'i durdurur ve başlatır (:52-58, :79-83); HyperOS probe'unda üçüncüsü `-2-7-ext-uvc` (Ek A.2). Her `chcon` `u:object_r:vendor_file:s0` (`post-fs-data.sh:70`, `setmode.sh:256`, `halpatch.sh:114`, `ishtar-aon-fix/post-fs-data.sh:32-33`). Allowlist yalnız `action.sh:56`; WebUI `ksu.exec`, `ksu.toast`, `ksu.enableEdgeToEdge` kullanır (`index.html:193-209`, `:337`) | S4, 2026-11-15 |
| W3F21 | Aday 1: depoda olmayanlar | SukiSU paketi ve WebUI etkinliği, allowlist yolu, HyperOS dosya etiketleri, tam kamera servis listesi, modül `system/` overlay'inin metamodülsüz bağlanıp bağlanmadığı depoda yok: salt-okur probe ister (zamanı `3 · O1`'de) | S4, 2026-11-15 |
| W3F22 | Aday 2: sensör katmanı | `customize.sh:14`, `:20-28` sensör md5 tutmazsa kurulumu durdurur; HyperOS sensörü tutar (PROJECT_LOG §2.3). HAL koruması kurulumda yalnız uyarır (:36-50); açılışta `post-fs-data.sh:101-107` sensör mount'undan (:72) sonra çıkar: yalnız 50MP katmanı atlanır. `action.sh:153` ve `index.html:187` 50MP'yi hâlâ sunar. Smoke işaretleri `smoke.sh:275-278`; sabitler kurulu modülden okunur (:52-65): kurulum öncesi anlık görüntünün sensör ve HAL alanları geçersiz | S4, 2026-11-15 |
| W3F23 | Aday 4: kutucuk ve WebUI | `com.rifsxd.ksunext` kodda yalnız `WebUiActivity.java:15` (ön-derlenmiş `tile-app.apk` içinde). Sürüm yalnız `AndroidManifest.xml:11-12` (versionCode 11, versionName 2.1); modül güncellemeyi md5 ile anlar (`action.sh:48-54`). Uzun basış `QS_TILE_PREFERENCES` (:42) → `WebUiActivity` → `su -c` (`Sh.java:16`). SukiSU izi yok | S4, 2026-11-15 |
| W3F24 | Aday 4: sistem uygulaması fikri | Proje modüllerinde emsal yok; modüller mount'u kendileri yapar (`ishtar-aon-fix/module.prop:6`); tek not üçüncü taraf (`docs/rom-build-device-notes.md:129`). `scripts/build-release.py`'de `system/**` kuralı yok (:63-66): böyle bir dosya sürüm derlemesini bozar | S4, 2026-11-15 |
| W3F25 | Aday 5: v2.3 | Sürüm yerleri `module.prop:3-4`, `customize.sh:2`, `Kullanim.txt:1` (v1.9), tile manifest, `CHANGELOG.md:22`, üretilen manifest, `README.md:20`, `:94`. `Kullanim.txt`'nin 13 bayat ifadesi PROJECT_LOG :852–:866'da, S4 üç tane daha buldu; modülde 15 bayat yorum. `ishtar-aon-fix` HyperOS'ta etkisiz: dosya varsa çıkar (`post-fs-data.sh:12-15`), ROM dosyayı taşıyor (`README.md:21`) | S4, 2026-11-15 |
| W3F26 | Aday 6: AGC tuzakları | `docs/phase3-preconditions.md:71-119` yedeksiz; `:99` yönlendirmesi canlı dosyayı yazmadan önce boşaltır; sahip ve etiket AOSPA'ya sabit (:83-85). Yedek-önce, üç korumalı, sınanmış şablon `docs/agc-12mp-configuration.md:100-143`. Önerilen yeni yollar: `docs/hyperos4-adaptation-notes.md`, `scripts/agc-trap-clean.sh` | S4, 2026-11-15 |
| W3F27 | Kapsam dışı kaymalar | `docs/recovery-runbook.md:113` `setmode.sh:253-255`'i anıyor, bugün `:254-256`; `docs/agc-12mp-configuration.md:381` smoke'un yalnız tuzak anahtarının varlığını raporladığını söylüyor (IMPL-80'den beri bayat). §10 adayı | S4, 2026-11-15 |
| W3F28 | `3 · O1` için açık konular | (1) `Faz7.2`, `7.3`, `8.1`, `8.3` satırlarını kim superseded yapar: açık kullanıcı isteğiyle Step 1 ya da `3 · O4`'te orkestratör. (2) Soru 7 Step 1 sınırı dışında: kullanıcı onaylı sapma olarak ledger notu. (3) Faz 9'un emekli ROM derlemesine bağı denetlenmedi. (4) Aday 1 probe'unun zamanı. (5) `AUDIT-FIX-42`/`-57`'nin yeni ifadesi ve `AUDIT-FIX-22`'nin yazarı. (6) Step 1.5 atlama cümlesi | S1–S4, 2026-11-15 |
| W3P01 | Yönetici ve WebUI (`PRB1`–`PRB3`) | `com.sukisu.ultra` versionCode 41140, versionName `v4.3.0-r1`: kullanıcı beyanı doğrulandı; `com.rifsxd.ksunext` ve başka kök yöneticisi yok. `ksu://webui` işleyicisi `com.sukisu.ultra/.ui.hdhrsdynpwdActivity` (rastgele etkinlik adı). `.ui.webui.WebUIActivity` için `resolve-activity --brief` "No activity found": dışa kapalı ya da adı farklı; kutucuğun kökle `am start` denemesi `Faz10.4`'te | PRB, 2026-11-15T13:01:41Z–13:01:43Z |
| W3P02 | Kök, allowlist, mount (`PRB4`–`PRB6`) | `4.3.0-r1:KernelSU`, `41140`, `ksud 4.3.0-r1 (uapi: 6)`; adb kabuğunda `su` diyalogsuz çalıştı (`u:r:ksu:s0`). `/data/adb/ksu/.allowlist` var; `com.ishtar.cammodes` sayısı 0. `/data/adb/metamodule` yok, `metamodule=` taşıyan modül yok. init ad alanında `/adb/modules/` kökenli 6 bind mount (4 `data/app`, 1 `system/lib64`, 1 `system/priv-app`), KSU kaynaklı mount 0: başka bir modül uygulamayı kendi bind mount'uyla `priv-app`'e koyuyor | PRB, aynı |
| W3P03 | Kamera servisleri ve etiketler (`PRB7`, `PRB8`) | Çalışan: `cameraserver`, `vendor.camera-provider` (`/odm/bin/hw/vendor.qti.camera.provider-service_64`), `vendor.camera-provider-2-7-ext-uvc`. `vendor.camera-provider-2-7-ext` (virtual camera) ve `virtual_camera` rc'de tanımlı, çalışmıyor: `setmode.sh`'in yeniden başlatması onu başlatır [ÇIKARIM]. HAL ve sensör dosyası `u:object_r:vendor_file:s0` (modüldeki `chcon` ile aynı); `/odm/lib64/hw` dizini `vendor_hal_file` | PRB, aynı |
| W3P04 | AGC ve kutucuk (`PRB9`, `PRB10`) | AGC tercihleri `u0_a478`, `app_data_file:s0:c222,c257,c512,c768`; AOSPA'da `u0_a450`, `c194,c257` (`docs/phase3-preconditions.md:83-85` sabitleri tutmaz). Tuzak anahtarları `org.codeaurora.snapcam_preferences.xml`'de. HyperOS kutucuk kaydında `com.ishtar.cammodes` yok | PRB, aynı |

### 7.2 Aşama ve görev planı (`3 · O1`, 2026-11-15)

**Onay:** kullanıcı, 2026-11-15 (form: "onay"; dört soruda öneriler). `PRB` aynı gün yürütüldü; `3 · O2a` ve sonrası ayrı oturumlardır (§0, "Döngü").

**`W3O1OPN` (açılış, 2026-11-15T12:36Z):** dal `integrate/impl-96`, ağaç temiz, 78 commit, uç `Window 3 O0 follow-up: hand-off for stage 3 O1`; `origin/main..HEAD` = 2; `main` = `origin/main` = `Window 2 follow-up: context budget and stage sizing`; etiket yok; 350 izlenen dosya. `ls-remote`: `HEAD`, `main`, `integrate/impl-96` = `main` (tam hash eşleşti). `gh api` (12:36:42Z–12:36:44Z): `ishtar`, `android_local_manifests`, `android_device_xiaomi_ishtar`, `ishtar_cam_modes` 200. Bağlamın ilk ölçümü 65k (Ek A.7).

**Dört soru** (yanıtlar tarihle yazılır):
1. **Dal:** `integrate/impl-96` sürer mi? Öneri: sürer (Pencere 2 kalıbı). Push kuralı (`git push origin main integrate/impl-96`; §3, Ek A.5, `NEXT_PROMPT.md` §6 madde 17) ve FF komutu değişmez; FF yalnız `3 · O5`'te. Yeni dal bu üç yeri ve devir metinlerini değiştirir, kazancı yalnız addır.
   - **Yanıt (2026-11-15):** Sürer; FF yalnız `3 · O5`'te.
2. **Salt-okur cihaz ölçümü (`PRB`):** Öneri: bu oturumda, onaydan sonra ve kapanıştan önce; yalnız aşağıdaki PRB1–PRB10 komutları. Sonuç §7.1'e `W3P` satırları olarak yazılır ve `Faz10.1`–`Faz10.4`'ün kanıtıdır (`W3F21`, `W3F31`). Ertelenirse aynı komutlar `3 · O2b` açılışında çalışır.
   - **Yanıt (2026-11-15):** Bu oturumda; kullanıcı telefonun bağlı ve hazır olduğunu bildirdi. `PRB` 13:01:41Z–13:01:43Z'de `dc27e5d0`'da yürütüldü; çıktının kimlik taraması temiz (LUHN15 0, anahtar sözcük 0); `PRB3` paketi `com.sukisu.ultra` kaldı; sonuç §7.1 `W3P01`–`W3P04`.
3. **Alt plan kimlikleri:** aşağıdaki tablo (`Faz10.1`–`Faz10.5`, klasör `Planner-docs/Faz-10-Plans`, "ClaudeQB Phase 10"). Dosya adlarının son eki `3 · O2b` kontratında kesinleşir.
   - **Yanıt (2026-11-15):** Öneri kabul: `Faz10.1`–`Faz10.5` aşağıdaki tablodaki gibi.
4. **Hetzner satırlarının aşaması (soru 7):** Öneri: `3 · O4`, orkestratör: Comprehension `CQ-13` ve `EV-20`, `docs/reverse-engineering-toolchain.md:220`, Ontology değişmez 11. `AUDIT-FIX-57` ailesi tek commit'te kapanır; 12. denetim doğrular, §10 yolu gerekmez.
   - **Yanıt (2026-11-15):** `3 · O4`.

**Alt planlar (ClaudeQB Phase 10):**

| Kimlik | Aday | Konu | Oturum | Kanıt | Bağımlılık |
|---|---|---|---|---|---|
| `Faz10.1` | 1 | HyperOS 4 kamera yığınının salt-okur ölçümü ve kaydı: servis adları (değişmez 3), `chcon` etiketleri, allowlist, yönetici ve WebUI | `3 · O3a` | `W3F20`, `W3F21`, `PRB`; Ek A.2 `D1`–`D11`, `M1` | — |
| `Faz10.2` | 2 | Sensör katmanı: v2.2 değişmeden HyperOS 4'te, smoke bracket ile (kurulum kullanıcıda); 50MP seçeneği HyperOS 4'te kapalı (K9 = hayır); `setmode.sh` servis adları | `3 · O3a` | `W3F22`, `M1`, `PRB`; PROJECT_LOG §2.3 | `Faz10.1` |
| `Faz10.3` | 6 | AGC tuzak denetimi ve yedekli, korumalı temizleme (HyperOS 4) | `3 · O3a` | `W3F26`; Ek A.2 `TRAP`; `PRB` | `Faz10.1` |
| `Faz10.4` | 4 | Kutucuk ve WebUI zinciri: SukiSU'ya uyarlama; aynı arayüzlü sistem uygulaması fikri değerlendirilir | `3 · O3b` | `W3F23`, `W3F24`, `PRB` | `Faz10.1` |
| `Faz10.5` | 5 | v2.3 sürümü: `Kullanim.txt` (`DEC-29`), sürüm yerleri, CHANGELOG, manifest, modül yorumları, tile-app `versionName`; `ishtar-aon-fix`'in HyperOS 4'teki yeri | `3 · O3b` | `W3F25`; §10 (modül yorumları) | `Faz10.2`–`Faz10.4` |

Aday 3 (50MP HAL) düştü (K9 = hayır, `DEC-33`). Numara sırası uygulama sırasıdır; `3 · O3a` yalnız 10.1–10.3'ü yazar, böylece klasörde numara boşluğu oluşmaz (V:1040-1043).

**Oturumlar** (tahmin §0 adım 9: açılış ≈ 35k, 20 KB'lık devirle; tur başına ≈ 6k yürütme, ≈ 12k kontrat ve uzun metin):

| Aşama | Kapsam | Görevler | Kapı ve geçit | Tahmin | Önkoşul |
|---|---|---|---|---|---|
| `3 · O1` | Plan ve onay; `PRB`; kapanış | `PRB` | plan onayı (`PRB` dahil); onayda bağlam ölçümü; kimlik taraması | 35k + 15 × 10k ≈ 185k; ölçülen 206k (plan sunumu, ≈ 24 tur) | `3 · O0` |
| `3 · O2a` | Step 1: `Main-Planing.md` (aşağıdaki Step 1 listesi) | `ST1-R` → `ST1-D` → `ST1-A` → `ST1-W` | metin onayı (kullanıcı); `--mode step1 --strict` | 35k + 10k okuma + 15 × 12k ≈ 225k | `3 · O1` |
| `3 · O2b` | Step 2 kontratı (§7.3): alt plan sözleşmesi, ortak bağlam, `3 · O4` hedef tablosu | `ST2-R` → `ST2-K` | bayt, boru, kimlik | 35k + 10k okuma + 15 × 12k ≈ 225k | `3 · O2a` |
| `3 · O3a` | Step 2 taslakları `Faz10.1`–`Faz10.3` | `SP1` ∥ `SP2` ∥ `SP3` → `CPa` | taslak betiği; ara durum (aşağıda) | 35k + 25 × 6k ≈ 185k | `3 · O2b` |
| `3 · O3b` | Step 2 taslakları `Faz10.4`, `Faz10.5` | `SP4` ∥ `SP5` → `CPb` | taslak betiği; ara durum | 35k + 20 × 6k ≈ 155k | `3 · O3a` |
| `3 · O4` | Ledger, Index, Ontology, Hetzner satırları; geçitler | `I3a` ∥ `I3b` → `GATE3` | `step2` ve `step3-preflight` `--strict`; V1–V3 yeni taban; bayt, boru, kimlik | 35k + 33 × 6k ≈ 233k | `3 · O3b` |
| `3 · O5` | İncelemeler, düzeltme, kapanış, FF, push | `REV-4` ∥ `SEC-C` → `FIX3` → `C3` → `FF` → `PUSH` → `LSR`, `RID` | FF ve push onayı | 35k + 30 × 6k ≈ 215k | `3 · O4` |

Hiçbir aşama 240k'yı aşmıyor; birleşim yok (`3 · O3b` + `3 · O4` ≈ 388k). Kalibrasyon: `3 · O1` plan sunumunda ≈ 24 turda 206k'daydı (tahmin 185k); fark zorunlu okuma (≈ 50 KB ≈ 28k) ve uzun düşünme, bu yüzden `3 · O2a` ve `3 · O2b`'ye 10k okuma eklendi. Orkestratör uzun metni okumaz ve yazmaz: taslak `local://`'da, uygulama `py -3` betiğiyle (edit yankısı yok). `3 · O4` sınıra en yakın; 300k'da §0 adım 7.

**Görevler** (alt ajanlar doğrulayıcı, test ve format çalıştırmaz; dönüş bloğu §3; sıcak noktalara yalnız taslak). Uzun taslaklar (`ST1-D`, `SP1`–`SP5`, `I3a`) geniş bağlamlı salt-okur scout'a verilir, `local://`'a yazar: 100K bağlamlı `task` ajanı ≈ 67 KB girdide taştı (§10, `O5` W6 maddesi). `task` yalnız küçük düzeltmelerde (`FIX3`):

| Kimlik | Aşama | Ajan | İş | Yazar | Yasak | Kabul | Doğrulama | Bağımlı |
|---|---|---|---|---|---|---|---|---|
| `PRB` | `3 · O1` | orkestratör (adb) | `W3F21` olgularının salt-okur ölçümü | plan §7.1 (`W3P` satırları) | cihaz durumu, AGC tercihleri, cihaza yazma | her komutun sonucu kayıtlı; kimlik değeri yok | yalnız `PRB` tablosu; kimlik taraması | plan onayı |
| `ST1-R` | `3 · O2a` | scout ×2 | `Main-Planing.md` tam okuma ve çapalar; First-Planner kuralları | `local://` | depo | ≤ 4 KB; yerler içerikle doğrulanmış | — | `3 · O1` |
| `ST1-D` | `3 · O2a` | scout (taslak, geniş bağlam) | Step 1 değişikliklerinin satır satır taslağı | `local://` | depo | Step 1 listesinin her maddesi; 11 başlık sırayla | taslak betiği | `ST1-R` |
| `ST1-A` | `3 · O2a` | kullanıcı | Step 1 metninin onayı | — | — | "onay" | — | `ST1-D` |
| `ST1-W` | `3 · O2a` | orkestratör | taslağı `py -3` betiğiyle uygular | `Planner-docs/Main-Planing.md` | öteki dosyalar | CRLF korunur, NUL 0 | bayt sayımı; `--mode step1 --strict` | `ST1-A` |
| `ST2-R` | `3 · O2b` | scout ×3 | Step 2'nin tam okuması (fazlar, destek belgeleri, 42 alt plan); ledger, Index, Ontology çapaları | `local://` | depo | ≤ 4 KB | — | `3 · O2a` |
| `ST2-K` | `3 · O2b` | orkestratör | §7.3: alt plan başına kapsam, kanıt, §9 yolları ve tek sahip; ortak bağlam; `3 · O4` hedef tablosu | plan §7.3 | `Planner-docs/` | her alt plan ve hedef satır tanımlı | bayt, boru, kimlik | `ST2-R` |
| `SP1`–`SP3` | `3 · O3a` | scout ×3 (taslak, geniş bağlam) | `Faz10.1`–`Faz10.3` taslakları | `local://` | depo | `W3F07` biçimi, §7.3 kapsamı, tekrar kuralı | taslak betiği | `ST2-K` |
| `CPa` | `3 · O3a` | orkestratör | taslakları `cp` ile yerine koyar; Index'e yalnız yazılan dosyaların Phase 10 girdileri | `Planner-docs/Faz-10-Plans/`, `Sub-Planing-Index.md` | öteki dosyalar | betik geçti; ara durum tablosu | `--mode step2 --strict`, `--mode all` | `SP1`–`SP3` |
| `SP4`, `SP5`, `CPb` | `3 · O3b` | scout ×2 (taslak); orkestratör | `Faz10.4`, `Faz10.5` | `3 · O3a` gibi | `3 · O3a` gibi | `3 · O3a` gibi | `3 · O3a` gibi | `CPa` |
| `I3a` | `3 · O4` | scout (taslak); orkestratör | ledger: §2 koşu 21; §3 snapshot; §4 dört superseded, `Faz6.1`/`Faz6.2` notları, beş yeni `planned`; §8 `DEC-33`, `DEC-32` atfı, silme ölçülürse `DEC-30` notu | ledger (orkestratör) | — | yalnız ekleme; kontrattaki hücre değişiklikleri | difflib, bayt | `CPb` |
| `I3b` | `3 · O4` | orkestratör | Index'te emekli girdiler (Faz 7/8, `Faz6.1`; `:258`, `:279`); Ontology değişmez 10 ve 11; Comprehension `CQ-13`, `EV-20`; toolchain `:220` | bu dört dosya | — | NUL ve satır sonları korunur | bayt | `CPb` |
| `GATE3` | `3 · O4` | orkestratör | geçitler | — | — | aşağıdaki son durum | V1–V3; `step2`, `step3-preflight` `--strict`; kimlik taraması | `I3a`, `I3b` |
| `REV-4` | `3 · O5` | reviewer (parçalı) | Pencere 3 diff'i: doğruluk, kontrat, doğrulayıcı tuzakları, eksik kanıt | `local://` | depo | P0/P1 yok ya da düzeltildi | — | `GATE3` |
| `SEC-C` | `3 · O5` | security-reviewer | push öncesi sır ve kimlik incelemesi (`W3P` satırları dahil) | `local://` | depo | P0/P1 yok | — | `GATE3` |
| `FIX3` | `3 · O5` | task | sıcak nokta dışı düzeltmeler (sıcak noktalar orkestratörde) | bulgunun dosyası | sıcak noktalar | bulgu kapandı | `GATE3` yeniden | `REV-4`, `SEC-C` |
| `C3`, `FF`, `PUSH`, `LSR`, `RID` | `3 · O5` | orkestratör | kapanış commit'i; FF (onay); push (onay); `ls-remote` karşılaştırması; silinecek depoların ölçümü | git | — | onaylar alındı; hash'ler eşleşti | `ls-remote` | `FIX3` |

**Step 1 listesi** (`3 · O2a`, yalnız `Main-Planing.md`; Step 1 ledger'a yazmaz; metni kullanıcı onaylar):
1. Faz 7 ve 8: yol haritası satırları ve bölümleri yerinde, ilk hücre `7`/`8` kalır, tarihli emeklilik notu (`DEC-28`); yeni satır tam `| 10 |` ile başlar, `### Phase 10` bölümü "ClaudeQB Phase 10" adıyla beş alt plan temasını sırasıyla anar (V:163, V:539-541).
2. §4 hedef son durumu (`:79`) K7 = (a)'ya göre; `W3F11`'in 25 satırı; Faz 6 bölümü (`:195`–`:205`, `:61`, `:276`; `Faz6.1` aşağıda); Faz 9 yalnız `:288` ve `:300`.
3. `AUDIT-FIX-57` (`:75`, `:211`, `:265`), `AUDIT-FIX-41` (`:277`), `AUDIT-FIX-42` (`:22`, `:61`, `:288`) için yeni ifade; R8 gerçekleşti, R9 konusuz.
4. §9 Step 2 devri yeniden yazılır: sınırlı Step 2, yalnız Phase 10 alt planları; tarihli not biçimi (`:300` emsali).
5. §10'a Step 1.5 atlama cümlesi: `Autopsy.md` bayat kalır; Comprehension ve Ontology'nin öteki bayat satırları (`W3F13`, `W3F14`) 12. denetime kalır.

**`W3F28` açık konuları ve kararlar:**
- (1) `Faz7.2`, `7.3`, `8.1`, `8.3` → `superseded`, `3 · O4`'te orkestratör. Superseded By = koşu 21'in MAIN snapshot kimliği (emsal `Faz4.1`, `Faz4.7`), gerekçe `DEC-28`; doğrulayıcı boş olmayan her değeri kabul eder (V:848, V:284). `Faz6.1` (`implemented`; ledger `:97` "planning run 21 decides the row") aynı biçimde `superseded`: yapı yok, Audit `:314` "`Faz7.3` adım 3'ten önce verified deme" der. `Faz6.2` `verified` kalır, tarihli `DEC-28` notu alır (soru 6).
- (2) Soru 7'nin Hetzner düzeltmeleri Step 1 ve Step 2 sınırı dışındadır: koşu 21 ledger satırında kullanıcı onaylı sapma notu (`3 · O4`).
- (3) Faz 9 ROM derlemesine bağlı değil (`Faz9.1`–`9.3` `verified`; S5). `Main-Planing.md` `:288`, `:300` Step 1'de; Index `:258`, `:279` `3 · O4`'te; `Faz9.2`:54'teki Android 16 cümlesi sınırlı Step 2 dışında: §10, 12. denetim.
- (4) `PRB` zamanı: soru 2.
- (5) `AUDIT-FIX-41`, `-42`, `-57`'nin yeni ifadesi Step 1 metninde (kullanıcı onaylar). Yazarını kaybeden `AUDIT-FIX-22` (`F8.1-10`), `-37` (`F7.3-08`) ve `-50` (`F8.3-08`) 12. denetimin yeni kuyruğunda atanır; koşu 21 satırı bunu anar.
- (6) Step 1.5 atlama cümlesi `Main-Planing.md` §10'da (`3 · O2a`) ve koşu 21 ledger satırında (`3 · O4`).

**Ara durumlar ve geçitler** (S5 ve S7 okumasıyla öngörü; aşama açılışında ölçülür):

| Aşamadan sonra | Kip | Beklenen | Çıkış |
|---|---|---|---|
| `3 · O2a`, `3 · O2b` | `step1 --strict` | bulgu yok | 0 |
| `3 · O2a`, `3 · O2b` | `all` | `missing_phase_folder=…Faz-10-Plans` (V:1010) ve denetim uyarısı; beklenen ara durum | 1 |
| `3 · O3a`, `3 · O3b` | `step2 --strict` | bulgu yok (`CPa`/`CPb` Index girdileriyle; girdisiz dosya `unindexed_subplan`, dosyasız girdi `missing_index_target`) | 0 |
| `3 · O3a`, `3 · O3b` | `all` | yalnız denetim uyarısı; `subplan_count` 45, sonra 47 | 0 |
| `3 · O4` | `step2`, `step3-preflight` `--strict` | bulgu yok | 0 |
| `3 · O4` | V1 `all` | yeni taban: `subplan_count=47`, `warning_count=1` | 0 |
| `3 · O4` | V2 `step4 --strict` | taban (`strict_warning` yalnız) | 1 |

Kırmızıya dönüş yolları: alt planda TODO/TBD/FIXME (V:947); ≥ 160 karakterlik aynı §3 ya da §7 gövdesi üç dosyada (V:1049); §3, §6, §8, §11'de ≥ 80 karakterlik aynı cümle 5 kez (V:624, V:1055); ledger §4'te ters tırnaklı yol (V:828) ya da tablodan boş satırla ayrılmış satır (V:420). Ledger §2 ve §3 satırlarını V okumaz (V:93-103); Audit'in hazırlık satırları 12. denetimde düzelir.

**Sıcak noktalar** (yalnız orkestratör): `Main-Planing.md` (`3 · O2a`); `Sub-Planing-Index.md` (`3 · O3a`, `3 · O3b`, `3 · O4`); ledger, Ontology, Comprehension, toolchain belgesi (`3 · O4`); `Faz-10-Plans/` (`3 · O3a`, `3 · O3b`); bu dosya, PROJECT_LOG §2.6/§11 ve `NEXT_PROMPT.md` (her kapanış); git. `Sub-Planing-Audit.md` Pencere 3'te yazılmaz.

**`PRB` komutları** (salt-okur; S6 tasarımı). `%TEMP%`'teki `py -3` betiği sabit PRB1–PRB10 listesini `subprocess.run(["platform-tools/adb.exe", "-s", "dc27e5d0", "shell", yük])` ile çalıştırır (kabuk tırnağı ve MSYS dönüşümü yok); çıktı geçici dosyaya yazılır, okunmadan önce kimlik taraması yapılır. PRB3'teki `com.sukisu.ultra`, PRB1/PRB2 başka bir yönetici paketi bulursa o paketle değişir. Başka komut çalışmaz; `am start` yok (arayüz açar):

```text
PRB1  pm list packages --show-versioncode | grep -iE 'sukisu|ksu|kernelsu|rifsxd|weishu|apatch|magisk|ishtar'
PRB2  cmd package query-activities --brief -a android.intent.action.VIEW -d ksu://webui
PRB3  dumpsys package com.sukisu.ultra | grep -m3 -E 'versionName=|versionCode=|lastUpdateTime='; cmd package resolve-activity --brief -n com.sukisu.ultra/.ui.webui.WebUIActivity
PRB4  su -v; su -V; timeout 20 su -c '/data/adb/ksud -V; id -Z'
PRB5  timeout 20 su -c 'ls -la /data/adb/ksu; ls -ld /data/adb/metamodule; grep -il metamodule= /data/adb/modules/*/module.prop; grep -ac com.ishtar.cammodes /data/adb/ksu/.allowlist'
PRB6  su -c 'cat /proc/1/mountinfo' | grep -E '^[0-9]+ [0-9]+ [0-9]+:[0-9]+ /adb/modules/' | cut -d' ' -f5 | cut -d/ -f2-3 | sort | uniq -c; su -c 'cat /proc/1/mountinfo' | grep -cE ' - [^ ]+ KSU '
PRB7  getprop | grep -E '^\[init\.svc\.[^]]*camera'; grep -rhoE '^service [^ ]*camera[^ ]* [^ ]+' /system/etc/init /vendor/etc/init /odm/etc/init 2>/dev/null | sort -u; ps -A -o LABEL,NAME | grep -i camera
PRB8  ls -lZ /odm/lib64/hw/camera.qcom.so /odm/lib64/camera/com.qti.sensormodule.ishtar_semco_imx989_wide.bin; ls -ldZ /odm/lib64/hw /odm/lib64/camera
PRB9  timeout 20 su -c 'ls -ldZ /data/data/org.codeaurora.snapcam/shared_prefs; ls -lZ /data/data/org.codeaurora.snapcam/shared_prefs/org.codeaurora.snapcam_preferences.xml; grep -l -e pref_raw_key -e pref_fix_resolution_key /data/data/org.codeaurora.snapcam/shared_prefs/*.xml'
PRB10 settings get secure sysui_qs_tiles
```

| Kimlik | Ölçülen | Kök | Alt plan |
|---|---|---|---|
| PRB1, PRB2, PRB3 | Yönetici paketi ve sürümü; `ksu://webui` işleyicisi; WebUI etkinliğinin varlığı | hayır | 10.1, 10.4 |
| PRB4, PRB5 | `su` ve `ksud` sürümü, `su` alanı; allowlist (yalnız sayım); metamodül | evet | 10.1, 10.2, 10.4 |
| PRB6 | init ad alanındaki modül bind mount'ları (iki yol bileşeni) ve KSU kaynaklı mount sayısı | evet | 10.2 |
| PRB7, PRB8 | Kamera servis adları, rc tanımları, HAL alanları; HAL ve sensör dosyalarının SELinux etiketleri | hayır | 10.1, 10.2 |
| PRB9 | AGC tercih dizininin ve dosyasının sahibi ve etiketi; tuzak anahtarlı dosyanın adı (değer basılmaz) | evet | 10.3 |
| PRB10 | HyperOS kutucuk kaydı | hayır | 10.4 |

Hiçbir komut yazmaz, mount etmez, özellik ayarlamaz, servis başlatıp durdurmaz, kurulum yapmaz; SukiSU `su` kullanımını günlüğüne yazabilir [ÇIKARIM]. Geniş `getprop` dökümü yok; allowlist yalnız sayılır. Çıktı §7.1'e `W3P` satırları olarak, kimlik değeri olmadan yazılır. Onayda bağlam ölçülür: `PRB` ve kapanış 280k'yı aşacaksa, telefon bağlı değilse ya da bir izin diyaloğu çıkarsa `PRB` aynı komutlarla `3 · O2b` açılışına kayar (diyalog fiziksel eylemdir, kullanıcıya sorulur).

**Yeni olgular (`3 · O1`, 2026-11-15; salt-okur scout'lar, cihaza komut yok):**

| Kimlik | Konu | Olgu | Kaynak |
|---|---|---|---|
| W3F29 | Faz 6 ve 9 | Faz 6 "AON fix upstreaming" (`Main-Planing.md:124`, `:195`–`:205`); `Faz6.1` `implemented` (IMPL-03), `Faz6.2` `verified` (IMPL-75), ikisinde de `DEC-28` notu yok. Faz 9: `Faz9.1`–`9.3` `verified` (ledger `:105`–`:107`); ROM'a bağ yalnız `Faz9.2`:54, Index `:258`, `:279`. Audit `:345` `AUDIT-FIX-50`'nin, `:377` `-22`'nin, `:382` `-37`'nin yazarı emekli alt planlarda. Alt plan boyları 15–20 KB; H1 kalıbı `# Faz 9.1 — Reproducible Release Build` | S5 |
| W3F30 | Doğrulayıcı kipleri | `step1` yalnız `Main-Planing.md`'yi denetler (V:1328, :627-638); denetim kapıları yalnız `step3`, `all`, `step4`'te (V:1218-1254). Index'te her `Faz-N-Plans/FazN.M-…md` yolu toplanır (V:158, :901-907): girdisiz dosya `unindexed_subplan` (V:1017), dosyasız girdi `missing_index_target` (V:1019). Dosyasız ledger satırı `missing_ledger_subplan` (V:830); satırsız dosya bulgu vermez; ledger yolu tırnaksız (V:484, :828). Emekli dosyalar H1'i ve 13 başlığı korur (V:924-944) | S7 |
| W3F31 | SukiSU ve WebUI | SukiSU-Ultra v4.3.0-r1 sürüm kodu 41140 (probe `:358` ile aynı); yönetici paketi varsayılan `com.sukisu.ultra`; WebUI etkinliği `.ui.webui.WebUIActivity`, `exported="false"`: kökle başlatılır. r1 modül kimliğini yalnız URI sorgusundan okur: kutucuğun `--es id` çağrısı etkinliği kapatır; çalışan biçim `-d 'ksu://webui?id=<modül>'`. `index.html:337` `enableEdgeToEdge`'i argümansız çağırır | S6, cihazda ölçülmedi; github.com/SukiSU-Ultra/SukiSU-Ultra (v4.3.0-r1) |
| W3F32 | Mount, allowlist, 2026-11-13 kökü | KernelSU v3 ve sonrası modülün `system/` ağacını yalnız metamodülle bağlar (kernelsu.org/guide/metamodule.html); probe'da `/data/adb/metamodule` yok; bizim modül `system/` taşımaz, kendi bind mount'unu yapar (`post-fs-data.sh:72`, `:127`): sistem uygulaması fikri metamodül ister. Allowlist yolu `/data/adb/ksu/.allowlist` (`action.sh:56` ile aynı; `main` dalında doğrulandı). 2026-11-13'te `su -c id` adb kabuğundan çalıştı (`u:r:ksu:s0`, probe `:272-274`) | S6 |

**`3 · O2a` notu (2026-11-15):** DEC metinleri ledger'dan doğrulandı: `DEC-28` (`:606`) yalnız Faz 7 ve 8'i, `DEC-32` (`:610`) yalnız modülün HyperOS 4'e uyarlanmasını anar; Phase 10, Faz 7/8'in emekliliği ve Faz 6'nın ROM hedefinin emekliliği `Main-Planing.md`'de koşu 21'in seçimi olarak yazıldı. `3 · O2b` için açık konu: `run-step2.md`'nin 6. adımı plan snapshot'ı değiştiyse Step 2'yi durdurur; yeni §9 koşu 21'in MAIN snapshot'ını kimin kaydedeceğini söylemez (ledger §3, `I3a`). Karar §7.3 kontratında verilir.

## 8. Pencere 4 — 12. denetim (Step 3)

- `run-step3.md`: yalnız `Planner-docs/Sub-Planing-Audit.md` yazılır (orkestratör). En fazla 3 salt-okur reviewer (kapsam, hazırlık, güvenlik; roller `run-step3.md:17`, sayı sınırı bu planın seçimi) paralel çalışır.
- **Oturum düzeni (2026-11-15, §0 adım 9):** Denetim 42 alt planın tamamını (≈ 0,93 MB, ortanca 19 KB) ve koşu 21'in yenilerini okur; denetim dosyası bugün ≈ 57 KB. Reviewer başına girdi ≤ 400 KB tutulur: roller klasör dilimleriyle bölünür (≈ 9 reviewer çalışması), oturum başına en çok üç reviewer.
- **Varsayılan dağılım:** `4 · O0` keşif; `4 · O1+O2` plan ve denetim kontratı (birleşik, onayla); üç inceleme oturumu (`4 · O3a`–`4 · O3c`); `4 · O4` denetim dosyasının birleştirilmesi ve geçitler; `4 · O5` kapanış. Bulgular oturumlar arasında depodaki bir dosyada taşınır (§0 adım 8); dosya `Planner-docs/` dışındadır, yerini `4 · O1+O2` seçer.
- Tuzaklar: Doğrulayıcı denetim durumunu dosyadaki ilk `status:` eşleşmesinden okur; başlıkta eski denetimin durumu alıntılanmaz; değer ayıraçtan hemen sonra gelmeli (§7, doğrulayıcı tuzakları). 15 başlık tekil olmalı, her biri en az 20 karakter. Bulgu kimlikleri `AUDIT-FIX-58`'den devam eder.
- Beklenen: `Faz7.2`, `7.3`, `8.1`, `8.3` SUPERSEDED; `Faz4.6` DEFERRED; yeni alt planlar READY, READY_WITH_WARNINGS ya da gerekçeli NEEDS_REPAIR.
- Geçit: `--mode step3 --strict` ve `--mode all`. Step 4 önkoşulu `p0_findings=0`, `p1_findings=0`.

## 9. Pencere 5+ — K7 = (a) Step 4 koşuları

- `run-step4.md`: 12. denetimin kuyruğu, dizin sırasıyla. Her dilim bir fazdır; aşamaları oturumlara §0 adım 9 ile dağılır.
- **Varsayılan:** küçük bir dilimde `O0`+`O1` bir oturum, `O2`–`O4` bir oturum, `O5` bir oturum (her birinin tahmini ≤ 240k ise). `O0`+`O1` birleşimini bir önceki kapanışın `NEXT_PROMPT.md`'si tahminle önerir, açılışta kullanıcı onaylar; `O2`–`O4` birleşimi dilimin `O1` planında onaylanır. Büyük dilim bölünür; küçük dilimler, toplam tahmin izin verirse, bir fazda birleşir (en çok dört).
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
- **`O2`'de eklenen (2026-11-14; dokunulmadı):**
  - Bu bölümün ilk maddesindeki ledger atıfları ve Ek A.4 çapaları C1 öncesine göre numaralı. Güncel karşılıkları LSH ile; içerikle doğrulanmış örnekler: `:575` → `:578` (`DEC-04`), `:582-583` → `:585-586` (`DEC-11`, `DEC-12`), `:586` → `:589` (`DEC-14`), `:633` → `:642` (`FIND-2.3-03`). Ek A.4 Pencere 1'in kaydıdır, düzeltilmez.
  - Hetzner ifadesi `DEC-26`'dan (Scaleway; ledger §7 `:552`) beri bayat ve yedi yerde canlı: `Main-Planing.md` `:75`, `:211`, `:265`; Ontology değişmez 11 (`:429`); `Project-Comprehension.md` `:25`, `:51`; `docs/reverse-engineering-toolchain.md:220` (`AUDIT-FIX-57`; §7 soru 7). `Sub-Planing-Index.md:10` ve `Faz7.1` satır 5 tarihseldir (Audit `:380`).
- **`O3`'te eklenen (2026-11-14; SEC-A1–A3 ve REV-3 bulguları):**
  - **REV-3 P3 → koşu 21 (ledger):** `Planner-docs/Planing-Ledger.md` `:607` (`DEC-29`), `:609` (`DEC-31`), `:610` (`DEC-32`) ve kısmen `:608` (`DEC-30`, K6 yarısı): "Raised by" hücresi "The user, 2026-11-13" diyor. Ek A soruyu kimin açtığını söylemiyor; oturumun açtığı sorular için ledger geleneği "put to the user <tarih> by `IMPL-NN`" biçimidir (`DEC-23` `:600`, `DEC-25` `:603`). Karar, durum ya da ölçüm etkilenmiyor.
  - **REV-3 P2 → düzeltildi (karar 4):** `UNTRACKED-BY-DESIGN.md:36` Faz 1.1'deki izlenen dosya sayısını 84 diyordu; ledger `:66`, `:113` ve `git ls-tree` 86 veriyor (Ek A.6 `G12b`). Düzeltici task satırı bu aşamanın kapanış commit'inde düzeltti. §5.1'deki W4 `:36` hedefi ("84, Faz 1.1 rakamı olarak kalır") yanlıştı; §5.1 Pencere 1'in kaydıdır, düzeltilmez. `NEXT_PROMPT.md`'nin `2 · O3` kabulündeki "`UNTRACKED-BY-DESIGN.md` dokunulmamış" ifadesi karar 4 ile çelişiyordu; plan kazandı.
  - **SEC-A3 P3 → kabul, işlem yok:** `PROJECT_LOG.md`, `NEXT_PROMPT.md` ve bu dosyadaki yerel yollar (`gh.exe`, ClaudeQB eklentisi, `../ishtar-arsiv` aynaları, depo kökü) Windows kullanıcı adını içeriyor. Depo özel; aynı yollar push edilmiş ağaçta da var (ör. ledger `:178`, `:542`; `docs/reverse-engineering-toolchain.md:21`) ve komutların çalışması için gerekli. Kullanıcı isterse sonraki bir kapanışta `$LOCALAPPDATA` ya da `~` biçimine çevrilir.
  - **SEC-A3 gözlemi → koşu 21 ya da sonraki plan revizyonu:** Ek A.5 betiğindeki `D15` deseni yalnız bitişik 15 haneyi yakalar; boşluk ya da tireyle bölünmüş bir IMEI sayılmaz. Bu aralıkta öyle bir dizi yok (SEC-A1–A3'ün ayrı taraması 0).
  - **SEC-A1–A3 notları (bulgu değil):** `7fa0a51`, `03b0898` ve `775b321`'in commit mesajlarındaki `Co-Authored-By` trailer'ı hizmetin noreply adresini taşıyor; aynı trailer push edilmiş `587e3b5`'te de var. Probe, üçüncü taraf kernel'in herkese açık derleme dizgisini (`kullanıcı@makine` biçiminde) ve kurulu modül ve uygulama adlarını içeriyor; depo özel. `DEC-10`'daki debug imza varsayılanının değeri push aralığında geçmiyor.
  - **W5'in envanter dışı gözlemleri (dokunulmadı; REV-1, `O5` FIX ya da koşu 21 için; satır numaraları `2 · O3` kapanışındaki `PROJECT_LOG.md`'ye göre):** §2.1 `:46` satır sonundaki "(Ö13)" etiketi artık 2026-11-14 olgularını da kapsıyor; §3.1 `:292` "girdiler GitHub'da" depo silme yürütülünce bayatlar; §3.1 `:297` Faz 8 özeti `DEC-08`'in konusuzluğunu anmıyor; §3.3 `:417` yalın "§7" ledger §7'yi kastediyor (günlükte §7 belge haritasıdır); §5.1 `:669` "yalnızca statik; üçlü uyum bekliyor" ve `:670` "DEC-08 için öneri" (`DEC-28` ile konusuz); §5.2 `:679` AOSPA A15 bulgusu dönemi belirtilmeden şimdiki zamanla; §7 `:767` tarih hücresi 2026-09-20 (dosyada 2026-11-13 eki var), `:772` (`docs/agc-12mp-configuration.md` "2026-09-05"; C1 değiştirdi), `:783` (README "v2.1'de kalmış"; C1 yeniden yazdı), `:786` (UNTRACKED "remote yok diyor"; C1 yeniden yazdı), `:791` (plan "Pencere 1 girişi"); §8 `:801` (ledger `:101` IMPL-96 notunu taşıyor ama satır "Çözüldü" diye işaretli değil) ve `:848` ("Kısmen çözüldü (IMPL-96, ledger `:532`)" olabilir); §10 `:919` kimlik listesi Pencere 2 görev kimliklerini anmıyor.
- **`O4`'te eklenen (2026-11-14):**
  - **`git log --grep 'Window 2 O2'` iki commit döndürüyor → düzeltildi (kullanıcı onayı, takip commit'i):** `2 · O0+O1` commit'inin gövdesi O2 aşamasını adıyla anıyor; çıktının ilk satırı (en yeni) `2 · O2` kapanışıdır. §1 `:45`'teki ve §6.4 `:341`'deki (SEC-B girdisi) kalıp bu yüzden tek başına belirsizdi; takip commit'i `Window 2 O4 follow-up: anchor the O2 commit lookups` ikisini konu satırına bağladı (`git log -1 --format=%h --grep '^Window 2 O2:'` yalnız `2 · O2` kapanışını verir; Ek A.6 `O4OPN`). §1'deki öteki `--grep` aramaları (`IMPL-96: repository move`, `Window 2 O0-O1`, `Window 2 O3`) 2026-11-14'te tek commit döndürüyor. `Window 2 O4` düz aranırsa `2 · O3` commit'inin gövdesi ve takip commit'i de eşleşir; §1'deki `2 · O4` satırı bu yüzden konu satırına bağlı biçimi kullanır.
  - **`NEXT_PROMPT.md`'nin `2 · O4` devri planla çelişiyordu (plan kazandı):** devir, I2a'da `git diff --stat`'ın yalnız üç dosyayı göstereceğini söylüyordu; `2 · O3` kapanışı REV-3 düzeltmesiyle `UNTRACKED-BY-DESIGN.md:36`'yı da değiştirmişti (karar 4; yukarıdaki `O3` maddesi). Sahiplik kontrolü dört dosyayla yapıldı; dördüncü dosyanın tek değişikliği o düzeltmedir.
- **`O5`'te eklenen (2026-11-14):**
  - **W5'in envanter dışı gözlemleri → REV-1'de hüküm verildi:** 15 gözlemin 13'ü `2 · O5` FIX'iyle düzeltildi (PROJECT_LOG §11, `2 · O5` girdisi); `:292` ("girdiler GitHub'da") bugün doğru, depo silme ölçülünce Pencere 3 günceller (§7 "Açılışta ayrıca" listesine eklendi); `:679` (§5.2'deki AOSPA bulgusu) `O2`'de tarihsel sayılmıştı (§6.5.1), not eklenmedi.
  - **REV-1 → koşu 21 (ledger çapaları):** Ek A.6 `LMAP` ledger §4'teki IMPL-96 notlarını yalnız `:100` ve `:101` diye sayıyor; ledger `:97`, `:102` ve `:104`'te de, ayrıca §6 `:542` ve §7 `:567`'de IMPL-96 notu var (2026-11-14, `IMPL-96` araması). A.6 Pencere 2'nin kaydıdır, düzeltilmez; koşu 21 ledger çapalarını içerikle yeniden doğrular.
  - **REV-2, plan parçası → bu aşamada düzeltildi (orkestratör):** B1 (P2) §7'ye Step 1.5 (Autopsy) ve `--mode autopsy` eklendi (sorular 7–8, doğrulayıcı tuzakları, ClaudeQB süreci); B2 Step 2 tekrar kuralı ve "aynı oturumda"; B3 §6 tablolarının taranması; B4 denetim durumu regex'i (§7 ve §8); B5 "Açılışta ayrıca"daki I2a/I2b ifadesi; B6 Ek A.6 başlığı; B7 §3 Adlandırma (`FF`, `G12b`, `K0`); B8 soru 8'in emsal listesi (koşu 10, 17 ve 18). Hepsi ClaudeQB kaynağında ve doğrulayıcıda orkestratörce doğrulandı.
  - **REV-2, `NEXT_PROMPT.md` parçası → bu aşamada düzeltildi:** P0/P1 yok; 2 P2 (`--mode autopsy` geçidi Step 1.5'e bağlı değildi; §10'da yanlış bölüm atfı) ve 9 P3; hepsi düzeltici task ile 14 satırda düzeltildi. Plana düşen üç uzantı orkestratörce §7'ye işlendi (`autopsy` kipinin Comprehension'ı da denetlemesi; Step 1.5 yönergesi `Autopsy-Planner.md`; alt plan dosya adının `FazN.M-` öneki). Koşu 21'e not: `git log --grep '^…'` kalıbı gövde satırlarını da eşler; aramanın yalnız konu satırını bulması gövdede o başlıkla başlayan satır olmamasına dayanır (bu bölümün `O4` maddesindeki "konu satırına bağladı" ifadesi bu anlamdadır).
  - **SEC-B notu (bulgu değil):** push edilmiş `587e3b5`'in commit mesajında `Co-Authored-By` satırının yanında bir oturum adresi var; push aralığının dışında, kimlik bilgisi taşımıyor.
  - **W6 süreci:** `task` ajanının 100K bağlamı yine yetmedi (A parçası ≈ 67 KB girdiyle taştı ve `partial` döndü); B parçası geniş bağlamlı salt-okur bir ajana taslak olarak yazdırıldı ve orkestratör `edit` ile uyguladı (`2 · O3`'teki P2–P5 yöntemi).
- **`3 · O1`'de eklenen (2026-11-15):**
  - **`W3F27` (S4):** `docs/recovery-runbook.md:113` `setmode.sh:253-255`'i anıyor, bugün `:254-256`; `docs/agc-12mp-configuration.md:381` smoke'un yalnız tuzak anahtarının varlığını raporladığını söylüyor (IMPL-80'den beri bayat). → 12. denetim ya da `Faz10.5`.
  - **Sınırlı Step 2'nin dışında kalanlar (`W3F13`, `W3F14`, `W3F29`):** `Faz9.2`:54'teki Android 16 cümlesi; Comprehension'ın Hetzner dışındaki bayat satırları (TRACE-14 ve ARC-06 dahil); Ontology'nin değişmez 10 ve 11 dışındaki yerleri. Step 1.5 atlandığı için koşu 21 bunları düzeltmez → 12. denetim.
- **`3 · O2a`'da eklenen (2026-11-15):**
  - **`Main-Planing.md`'nin koşu 21 kararlarına bağlı olmayan eski ifadeleri:** `:18` ve `:247` (sürüm denetimi yok), `:310` (ledger, Ontology ve Comprehension "yoktu"); yeniden yazılan satırlarda korunan eski yan cümleler (`:22` "no safety net", `:57` "complete through v2.1", `:69` "v2.1 built but never flashed", `:75` sürüm denetimi ve README maddeleri). Numaralar Step 1'den önceki dosyanındır; Step 1 listesinde olmadıkları için dokunulmadı → 12. denetim.

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

Measured by the orchestrator during Window 2 (2026-11-14; the stage is named in the last column), read-only; no device command was sent. Window 2 writers take facts from A.1, A.2 and this table only.

| # | Fact | Value | Source / when measured |
|---|---|---|---|
| OPN2 | Window 2 opening | Branch `integrate/impl-96`, tree clean, 69 commits, tip = C1 (cited by title); `main` 63 commits at `7fa0a51` (`[origin/main: ahead 1]`); no tags; 350 tracked files (G12 unchanged: C1 added no file) | git, 2026-11-14 |
| G4b | Remote state | `git ls-remote origin` lists only `HEAD` and `refs/heads/main`, both `587e3b5` (62 commits). Not pushed: `7fa0a51`, `70946ff`, `03b0898`, `775b321`, `b603516` (C0), `c2abd46` (C0 follow-up), C1 and every window 2 stage commit | git, 2026-11-14 |
| G8b | Repositories to delete | `gh api` at 2026-11-14T07:23:21Z: `ahmetxa/ishtar` (private), `ahmetxa/android_local_manifests` (public) and `ahmetxa/android_device_xiaomi_ishtar` (public) all still 200; `ahmetxa/ishtar_cam_modes` private, default branch `main` | `gh api`, 2026-11-14 |
| L653 | Ledger after window 1 | 653 lines, all CRLF, NUL 0; IMPL-96 row at :525 (`## 6.` at :526); `DEC-27`…`DEC-32` at :605-:610; no `DEC-33` anywhere. Window 2 does not edit it | script, 2026-11-14 |
| LSH | Ledger line shift by C1 | C1 added 9 lines (IMPL-96 row :525; new §7 top entry and separator :550-:551; `DEC-27`…`DEC-32` :605-:610). A reference written against the 644-line ledger maps, checked by content, to N for N <= 524, N + 1 for 525-548, N + 3 for 549-601 and N + 9 for N >= 602 (examples: 527→528, 549→552, 551/553/555→554/556/558, 586→589, 599→602, 601→604, 632→641) | scouts and `git diff c2abd46` against C1, 2026-11-14 |
| SH8 | `03b0898` shift | Inserted exactly 8 lines after line 2 of `docs/pre-rental-plan.md` and `docs/build-environment.md` (`@@ -2,0 +3,8 @@`): a reference to line N >= 3 written before it now points to N + 8; all 13 such references in `PROJECT_LOG.md` checked by content | `git diff 7fa0a51 03b0898`; scout, 2026-11-14; the 17 cited lines re-compared `7fa0a51` → HEAD by script, all identical after +8 (O2) |
| CDATE | Commit date groups | `PROJECT_LOG.md` §3.5 groups commits by author date in +0300 (`git log --date=short`): `7fa0a51`, `70946ff`, `03b0898`, `775b321`, `b603516` and `c2abd46` on 2026-11-13; C1 on 2026-11-14 (01:05 +0300 = 2026-11-13T22:05Z) | git, 2026-11-14 |
| RID0 | Identity check baseline | The A.5 script over `git log --all -p` and the 350 tracked files: 6 value-bearing key lines (3 in history, 3 in the tree), all `<redacted>`; 0 Luhn-valid 15-digit numbers; 9 prose-only key mentions (5 history, 4 tree), which a literal reading of A.5 would fail (decision 5a). PASS | script, 2026-11-14 |
| SEC0 | Push-range pre-scan | Every added line of the seven commit patches (`git log -p origin/main..integrate/impl-96`, 3,148 lines including intermediate states): no token, private key, credential assignment, rented-server host name, MAC address or Luhn-valid 15-digit number; the two IPv4-shaped matches are version strings (probe :321; `PROJECT_LOG.md` §11); the probe header records that the other phone's serial was not recorded, and the emulator appears only under its adb port name; author and committer e-mail identical to the already pushed `587e3b5` | script, 2026-11-14 |
| SMK-O | `smoke.sh -o snapshots/NAME` | `scripts/smoke.sh:283` creates only `snapshots/` (`mkdir -p "$SNAPDIR"`); `:284` redirects into `snapshots/snapshots/NAME.txt`, whose directory does not exist, so no file is written; `:285` still prints `stored: snapshots/snapshots/NAME.txt`; the script sets only `set -u` (`:29`) | code reading, 2026-11-14 [INFERENCE: not run] |
| O2OPN | Window 2 O2 opening | Branch `integrate/impl-96`, tree clean, 70 commits, tip = the `2 · O0+O1` commit (cited by title); `main` 63 at `7fa0a51` (`[origin/main: ahead 1]`); `origin/main` 62; 8 commits not pushed; no tags; 350 tracked files; `git ls-remote origin` → only `HEAD` and `refs/heads/main` = `587e3b5`. `PROJECT_LOG.md` lines 1-1012 are unchanged since C1 (the `2 · O0+O1` commit appended §11 lines 1013-1028 only), so the §6.2 line numbers hold | git, 2026-11-14 (O2) |
| G8c | Repositories to delete | `gh api` at 2026-11-14T10:03:48Z: `ahmetxa/ishtar` (private), `ahmetxa/android_local_manifests` (public) and `ahmetxa/android_device_xiaomi_ishtar` (public, default branch `vauxite`) all still 200; `ahmetxa/ishtar_cam_modes` private, default branch `main` | `gh api`, 2026-11-14 (O2) |
| G1b | `7fa0a51` contents | Four files: `Planner-docs/Faz-7-Plans/Faz7.2-first-aospa-build.md`, `Planner-docs/Planing-Ledger.md`, `Planner-docs/Sub-Planing-Audit.md`, `docs/pre-rental-plan.md`; author date 2026-11-13 18:21:31 +0300. Claims that planning run 20, the eleventh audit or the pre-rental plan are "not committed" are stale | `git show --stat 7fa0a51`, 2026-11-14 (O2) |
| CLOG | Commit subjects after `587e3b5` | Author dates in +0300 (`git log --date=short`), subjects verbatim. 2026-11-13: `7fa0a51` "Planning run 20 and eleventh audit: Faz7.2 re-targeted to Scaleway (DEC-26)"; `70946ff` "IMPL-96 evidence: read-only HyperOS 4 baseline on dc27e5d0"; `03b0898` "Mark the AOSPA ROM-build records historical (2026-11-13)"; `775b321` "Session 2026-11-13: project log and handoff prompt"; `b603516` "Window 0: orchestration plan, K8 redaction, handoff for window 1"; `c2abd46` "Window 0 follow-up: align handoff with plan, rename review IDs". 2026-11-14: C1 "IMPL-96: repository move, ROM-build retirement, HyperOS 4 baseline"; `2 · O0+O1` "Window 2 O0-O1: approved plan, discovery facts, stage-per-session loop"; `2 · O2` "Window 2 O2: contract for the project log sweep and the run 21 handoff" (this stage's closing commit). Files: `c2abd46` and `2 · O0+O1` changed `NEXT_PROMPT.md`, `ORCHESTRATION_PLAN.md`, `PROJECT_LOG.md`; C1 changed those three plus the ledger, `README.md`, `UNTRACKED-BY-DESIGN.md`, `docs/agc-12mp-configuration.md` and `docs/release-checklist.md` | git, 2026-11-14 (O2) |
| LMAP | Ledger anchors for window 2 writers | 653-line ledger, read by script. §4: `Faz6.2` :98, `Faz7.2` :100, `Faz7.3` :101, `Faz8.1` :102, `Faz8.3` :104 (`Superseded By` is `-` in all four; 10 pipes each). §5: IMPL-96 :525, items (1) repository move, (2) ROM-build retirement, (3) HyperOS 4 baseline `70946ff`, (4) the 2026-09-20 AOSPA A15 device notes, (5) K4, (6) K8 / `DEC-31`, (7) document fixes, (8) this run's ledger edits, (9) the user's verdicts. §6: :528 repository, :530 deliverables, :532 device, :534 camera modification state (no IMPL-96 note), :538 Phase 3 readiness. §7: :550 top entry (2026-11-13), :552 (the `DEC-26` entry), :554, :556, :558; old :559 and :609 are now :562 and :618. IMPL-96 notes, by content: :100 and :101 (the eleventh audit ran on 2026-09-14, `PASS_WITH_WARNINGS`; the rental or build will not happen); :528 (`DEC-27`: remote `ahmetxa/ishtar_cam_modes` with `main` = `587e3b5`, 62 commits; local `main` 63 at `7fa0a51`; the branch unpushed; `ahmetxa/ishtar` to be deleted; no file count); :530 (v2.2 / 13, `dist/`, `agc-50mp-yama/` contents); :532 (the 2026-11-13 HyperOS 4 observation: no project module, unpatched V9.6 AGC with ten traps, HAL differs from `HAL_STOCK_MD5`, sensor matches `EXPECT_MD5`); :552-:558 ("Status 2026-11-13": the audits ran, "outstanding" is history). §8: heading :572, table header :574, rows :576 (`DEC-02`) to :610 (`DEC-32`): `DEC-04` :578, `DEC-05` :579, `DEC-07` :582, `DEC-08` :583, `DEC-09` :584, `DEC-11` :585, `DEC-12` :586, `DEC-14` :589, `DEC-16` :593, `DEC-22` :599, `DEC-24` :601, `DEC-01` :602 (IMPL-96 note, previous status kept), `DEC-25` :603, `DEC-26` :604, `DEC-27`…`DEC-32` :605-:610; "Moot 2026-11-13 by `DEC-28` (`IMPL-96`)" notes on :582, :583, :599, :601, :603, :604. Findings: `FIND-3.7-01` :633, `FIND-3.7-02` :634, `FIND-3.10-01` :636, `FIND-3.10-03` :638, `FIND-3.10-04` :639, `FIND-3.5-01` and `FIND-4.5-02` :641, `FIND-2.3-03` :642, `FIND-2.3-02` :643; F3.11-09 claim block :647-:651. No IMPL-96 note on :51, :57-:60, :589 | script, 2026-11-14 (O2) |
| C1MAP | `README.md` and `UNTRACKED-BY-DESIGN.md` through C1 | `difflib` on `c2abd46` → working tree (neither file changed after C1). README: :18-:20 → :20-:22 (rewritten); :77 → :85 (rewritten); :78 → :86; :142-:144 → :152-:153 (rewritten; the clone-log row removed); :186 deleted (Exclusions); new `dist/` paragraph at :94; new remote sentence at :38 (`ahmetxa/ishtar_cam_modes`, `DEC-27`, explicit refspecs only). UNTRACKED: :9-:10 → :9-:10 (rewritten); :33 unchanged (still "4" files; §10); :38-:41 → :38-:39; :61 → :59; :63 → :61; :89 → :87-:88; :128-:130 → :127-:131; the `candidates/*.bin` row is at :71 | script, 2026-11-14 (O2) |
| O3OPN | Window 2 O3 opening | Branch `integrate/impl-96`, tree clean, 71 commits, tip = the `2 · O2` commit (cited by title); `main` 63 at `7fa0a51` (`[origin/main: ahead 1]`); `origin/main` 62; 9 commits not pushed (`origin/main..HEAD`: `7fa0a51`, `70946ff`, `03b0898`, `775b321`, `b603516`, `c2abd46`, C1, `2 · O0+O1`, `2 · O2`); no tags; 350 tracked files; `git ls-remote origin` → only `HEAD` and `refs/heads/main` = `587e3b5`. `gh api` at 2026-11-14T13:45:22Z: `ahmetxa/ishtar` (private), `ahmetxa/android_local_manifests` (public) and `ahmetxa/android_device_xiaomi_ishtar` (public, default branch `vauxite`) all still 200; `ahmetxa/ishtar_cam_modes` private, default branch `main`. `PROJECT_LOG.md` lines 1-1012 are unchanged since C1 (the two window 2 stage commits appended §11 lines 1013-1046 only), so the §6.2 line numbers hold | git, `gh api`, 2026-11-14 (O3) |
| G12b | Tracked files at the Faz 1.1 commit | `git ls-tree -r --name-only ff6934e` → 86 files (`ff6934e`, 2026-08-24, "Initial commit: put the ishtar workspace under version control"), matching ledger :66 (Faz1.1, "86 files") and :113 (IMPL-01, "committed 86 files"). `UNTRACKED-BY-DESIGN.md:36` (rewritten by C1 from plan §5.1's W4 target) says 84: REV-3 finding P2; the plan target contradicted the ledger | git, 2026-11-14 (O3) |
| O4OPN | Window 2 O4 opening | Branch `integrate/impl-96`, tree clean, 72 commits, tip = the `2 · O3` commit (cited by title); `main` 63 at `7fa0a51` (`[origin/main: ahead 1]`); `origin/main` 62; 10 commits not pushed (`origin/main..HEAD`: `7fa0a51`, `70946ff`, `03b0898`, `775b321`, `b603516`, `c2abd46`, C1, `2 · O0+O1`, `2 · O2`, `2 · O3`); no tags; 350 tracked files; `git ls-remote origin` → only `HEAD` and `refs/heads/main` = `587e3b5`. `gh api` at 2026-11-14T19:34:57Z: `ahmetxa/ishtar` (private), `ahmetxa/android_local_manifests` (public) and `ahmetxa/android_device_xiaomi_ishtar` (public, default branch `vauxite`) all still 200; `ahmetxa/ishtar_cam_modes` private, default branch `main`. I2a ownership check (script, `2 · O2` → `2 · O3` closing commits): four files changed, `NEXT_PROMPT.md`, `ORCHESTRATION_PLAN.md`, `PROJECT_LOG.md` and `UNTRACKED-BY-DESIGN.md` (line 36 only, the REV-3 P2 fix, §10); every `PROJECT_LOG.md` hunk outside §11 lies on a §6.2 inventory line (97 rows; lines :3 and :5 included); §11 has one append at its end (the `2 · O3` entry); §2.6 unchanged. `git log --grep 'Window 2 O2'` returns two commits because the `2 · O0+O1` commit body names the O2 stage; `git log -1 --format=%h --grep '^Window 2 O2:'` returns only the `2 · O2` closing commit | git, `gh api`, script, 2026-11-14 (O4) |
| O5OPN | Window 2 O5 opening | Branch `integrate/impl-96`, tree clean, 74 commits, tip = the `2 · O4` follow-up commit (cited by title); `main` 63 at `7fa0a51` (`[origin/main: ahead 1]`); `origin/main` 62; 12 commits not pushed (`origin/main..HEAD`: `7fa0a51`, `70946ff`, `03b0898`, `775b321`, `b603516`, `c2abd46`, C1, `2 · O0+O1`, `2 · O2`, `2 · O3`, `2 · O4` and its follow-up); no tags; 350 tracked files; `git ls-remote origin` → only `HEAD` and `refs/heads/main` = `587e3b5`. `gh api` at 2026-11-14T20:07:24Z: `ahmetxa/ishtar` (private), `ahmetxa/android_local_manifests` (public) and `ahmetxa/android_device_xiaomi_ishtar` (public, default branch `vauxite`) all still 200; `ahmetxa/ishtar_cam_modes` private, default branch `main`. Commit lookups: `git log -1 --format=%h --grep '^Window 2 O2:'` returns only the `2 · O2` closing commit (the SEC-B base); `git log --all --grep '^Window 2:'` returns nothing yet, so after C2 it matches only C2's subject | git, `gh api`, 2026-11-14 (O5) |

### A.7 Context budget (2026-11-15)

Measured by the orchestrator after `2 · O5` from this project's session logs (`archive`); a turn's prompt size is `input + cacheRead + cacheWrite` of its assistant message. §0 step 9 uses these figures.

- Peaks: window 0 576k (105 turns); window 1 584k (167 turns; two drops, 364k → 239k and 584k → 88k); `2 · O0+O1` 548k (55); `2 · O2` 508k (46; one drop to 293k); `2 · O3` 650k (110); `2 · O4` 323k (48); `2 · O5` 738k (121; compacted by the user at 738.9k after C2).
- First prompt 47–54k. The attached `NEXT_PROMPT.md` adds 0.58k per KB (41.6–52.3 KB in window 2); the rest is ≈ 23k.
- Growth per turn up to the peak: 5.2–6.4k in execution stages, 9.3k in `2 · O0+O1`, 13.9k in `2 · O2`.
- 48–77 % of the growth is the model's own output (thinking, tool-call arguments). It stays in context: after a turn without tool output the prompt grows by that turn's output tokens (median ratio 1.02 over 37 turns).
- Tool results cost 0.54 tokens per byte (median of 29 turns dominated by one result). Largest sources per session: `read` 133–376 KB, `edit` echoes 40–183 KB, `todo` echoes up to 80 KB.
- Measurement (JS eval; verified 2026-11-15: it printed this session's id and 275k). The newest session of the project is the current one; when two sessions of this project run at once, select it by id with `const s = (await archive.sessions({ limit: 5, silent: true })).find(x => x.id.startsWith(ID));` (ID: the 13 characters printed by the first measurement):

```js
const s = (await archive.sessions({ limit: 1, silent: true }))[0];
let t = 0;
for (const l of require("fs").readFileSync(s.file, "utf8").trimEnd().split("\n").reverse()) {
  let o; try { o = JSON.parse(l); } catch { continue; }
  const u = o.type === "message" && o.message.role === "assistant" && o.message.usage;
  if (u && (t = (u.input || 0) + (u.cacheRead || 0) + (u.cacheWrite || 0))) break;
}
print(s.id.slice(0, 13), t);
```
