package com.ishtar.cammodes;

import android.content.ComponentName;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.service.quicksettings.Tile;
import android.service.quicksettings.TileService;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.WeakHashMap;

/**
 * Uc kutucugun ortak davranisi.
 *
 * SENKRON
 *   Bir kutucuga dokunuldugunda yalnizca O kutucugun onClick'i calisir ve
 *   SystemUI uc kutucuk servisini ayni anda bagli TUTMAZ (olculdu: en fazla
 *   ikisi). Bu yuzden uc katman var:
 *     1. surec onbellegi  -- yeni baglanan kutucuk kabuga gitmeden dogru cizer
 *     2. tahmin           -- dokunusta beklenen mod hepsine dagitilir
 *     3. uyandirma        -- kardesler icin requestListeningState()
 *
 * GECIS SURESI
 *   Mod degisimi kamera yigininin tamamen yeniden baslamasini gerektiriyor ve
 *   servisler ayaga kalktiktan sonra bile kamera ~4 saniye kullanilamiyor.
 *   Erken acilirsa cekim sessizce basarisiz olur. Bu yuzden dokunusta beklenen
 *   sureyi, bitince de "hazir" bilgisini ekran altindaki bildirimle veriyoruz.
 *
 * DIL
 *   Sistem dilinden BAGIMSIZ; varsayilan Ingilizce. Tercih modulun lang
 *   dosyasinda tutulur; WebUI'deki dil dugmesi ayni dosyayi yazar.
 */
public abstract class BaseTile extends TileService {

    static final String ACT = "sh /data/adb/modules/ishtar_cam_modes/action.sh";
    static final String OFF_MODE = "stock";

    /** Tum kutucuklar. Kardes uyandirma ve "hepsi bagli mi" esigi buradan
     *  turetilir; yeni bir kutucuk eklenince tek yer degisir. */
    static final Class<?>[] TILES = {
            FullResTile.class, DcgTile.class, Ln4Tile.class, Ln2Tile.class
    };

    /** Mod degisiminin kabaca surdugu sure (setmode.sh ile uyumlu). */
    static final int SWITCH_SECONDS = 12;

    private static final long PENDING_TIMEOUT_MS = 25000L;

    private static final Set<BaseTile> LIVE =
            Collections.newSetFromMap(new WeakHashMap<BaseTile, Boolean>());
    private static final Object LOCK = new Object();
    private static final Handler MAIN = new Handler(Looper.getMainLooper());

    private static volatile String sMode;
    private static volatile String sPending;
    private static volatile long sPendingUntil;
    private static volatile long sNextWarmUp;
    /** "en" ya da "tr"; okunana kadar Ingilizce. */
    private static volatile String sLang = "en";

    /** Geri sayim tikleyicisi. Bildirim icin Hud kullaniliyor (toast kotasi
     *  saniyelik guncellemeye izin vermiyor). */
    private static Runnable sTicker;
    private static int sRemaining;

    protected abstract String mode();

    protected abstract int labelRes();

    // ------------------------------------------------------------- yasam dongusu

    @Override
    public void onStartListening() {
        super.onStartListening();
        synchronized (LOCK) {
            LIVE.add(this);
        }

        String pending = activePending();
        if (pending != null) {
            apply(pending);
            return;
        }
        if (sMode != null) {
            apply(sMode);
        }
        readAsync();
        warmUpSiblings();
    }

    @Override
    public void onStopListening() {
        synchronized (LOCK) {
            LIVE.remove(this);
        }
        super.onStopListening();
    }

    @Override
    public void onTileRemoved() {
        synchronized (LOCK) {
            LIVE.remove(this);
        }
        super.onTileRemoved();
    }

    // ------------------------------------------------------------------ dokunus

    @Override
    public void onClick() {
        super.onClick();

        Tile self = getQsTile();
        boolean wasOn = self != null && self.getState() == Tile.STATE_ACTIVE;
        final String predicted = wasOn ? OFF_MODE : mode();

        setPending(predicted);
        broadcast(predicted);
        wakeSiblings();
        hud(Msg.switching(sLang, pretty(predicted)));
        startCountdown();

        new Thread(new Runnable() {
            @Override
            public void run() {
                String result = Sh.run(ACT + " toggle " + mode());
                if (!isMode(result)) {
                    result = Sh.run(ACT + " get");
                }
                clearPending();
                if (isMode(result)) {
                    sMode = result;
                }
                broadcast(result);
                wakeSiblings();
                stopCountdown();
                hud(isMode(result) ? Msg.ready(sLang, pretty(result))
                                   : Msg.failed(sLang));
                hudDismiss(2500L);
            }
        }).start();
    }

    // -------------------------------------------------------------------- durum

    private static String activePending() {
        String p = sPending;
        return (p != null && SystemClock.elapsedRealtime() < sPendingUntil) ? p : null;
    }

    private static void setPending(String mode) {
        sPending = mode;
        sPendingUntil = SystemClock.elapsedRealtime() + PENDING_TIMEOUT_MS;
    }

    private static void clearPending() {
        sPending = null;
        sPendingUntil = 0;
    }

    /** Tek kabuk cagrisiyla hem etkin modu hem dili okur. */
    private void readAsync() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                String[] f = Sh.run(ACT + " info").split("\\|");
                if (f.length >= 4 && ("tr".equals(f[3]) || "en".equals(f[3]))) {
                    sLang = f[3];
                }
                String cur = f.length >= 1 ? f[0] : "";
                if (activePending() != null) {
                    return;
                }
                if (isMode(cur)) {
                    sMode = cur;
                }
                broadcast(cur);
            }
        }).start();
    }

    private void warmUpSiblings() {
        int live;
        synchronized (LOCK) {
            live = LIVE.size();
        }
        long now = SystemClock.elapsedRealtime();
        if (live >= TILES.length || now < sNextWarmUp) {
            return;
        }
        sNextWarmUp = now + 5000L;
        wakeSiblings();
    }

    private void wakeSiblings() {
        for (Class<?> c : TILES) {
            if (c == getClass()) {
                continue;
            }
            try {
                requestListeningState(this, new ComponentName(this, c));
            } catch (Exception ignored) {
                // kutucuk Hizli Ayarlar'a eklenmemis olabilir
            }
        }
    }

    private static void broadcast(final String current) {
        final List<BaseTile> copy;
        synchronized (LOCK) {
            copy = new ArrayList<BaseTile>(LIVE);
        }
        MAIN.post(new Runnable() {
            @Override
            public void run() {
                for (BaseTile t : copy) {
                    t.apply(current);
                }
            }
        });
    }

    private static boolean isMode(String s) {
        return s != null && s.length() > 0 && !s.equals("unknown")
                && s.indexOf(' ') < 0 && s.indexOf('\n') < 0;
    }

    /** Blob adini bildirimde gosterilecek BUYUK HARFLI ada cevirir. */
    private static String pretty(String m) {
        if ("50mp".equals(m)) {
            return "50MP";
        }
        if ("dcgB".equals(m) || "dcgA".equals(m)) {
            return "DCG";
        }
        if (m != null && m.startsWith("ln4")) {
            return "LN4";
        }
        if (m != null && m.startsWith("ln2")) {
            return "LN2";
        }
        return "tr".equals(sLang) ? "STOK" : "STOCK";
    }

    /** Ekranin alt ortasindaki bildirimi gunceller. */
    private void hud(final String text) {
        MAIN.post(new Runnable() {
            @Override
            public void run() {
                Hud.show(getApplicationContext(), text);
            }
        });
    }

    /** Bildirimi bir sure sonra kaldirir. */
    private void hudDismiss(long delayMs) {
        MAIN.postDelayed(new Runnable() {
            @Override
            public void run() {
                Hud.hide();
            }
        }, delayMs);
    }

    /** Saniyede bir kalan sureyi yazar; is bitince stopCountdown() durdurur. */
    private void startCountdown() {
        stopCountdown();
        sRemaining = SWITCH_SECONDS;
        sTicker = new Runnable() {
            @Override
            public void run() {
                sRemaining--;
                if (sRemaining <= 0 || sTicker != this) {
                    return;
                }
                hud(Msg.remaining(sLang, sRemaining));
                MAIN.postDelayed(this, 1000L);
            }
        };
        MAIN.postDelayed(sTicker, 1000L);
    }

    private void stopCountdown() {
        if (sTicker != null) {
            MAIN.removeCallbacks(sTicker);
            sTicker = null;
        }
    }

    /** Ana iplikte cagrilir. */
    private void apply(String current) {
        Tile t = getQsTile();
        if (t == null) {
            return;
        }
        boolean ok = isMode(current);
        boolean on = ok && current.equals(mode());
        t.setState(on ? Tile.STATE_ACTIVE
                      : (ok ? Tile.STATE_INACTIVE : Tile.STATE_UNAVAILABLE));
        // Etkin mod kutucukta YAZMAZ; vurgudan okunur. Alt yazi yalnizca kok
        // erisimi yoksa cikar. Gecis bilgisi ekran altindaki bildirimle verilir.
        t.setSubtitle(ok ? null : getString(R.string.no_root));
        t.setLabel(getString(labelRes()));
        t.updateTile();
    }

    /** Iki dilli kisa metinler. Varsayilan Ingilizce. */
    static final class Msg {
        private Msg() {
        }

        /**
         * Turkce yonelme eki. Kisaltmalar okundugu gibi ek alir:
         *   DCG  "de-ce-ge" -> unluyle biter        -> 'ye
         *   LN4  "...dort"  -> son unlu o (on)      -> 'e
         *   LN2  "...iki"   -> unluyle biter        -> 'ye
         *   STOK "stok"     -> son unlu o (arka)    -> 'a
         *   50MP "...em-pe" -> unluyle biter        -> 'ye
         */
        private static String dative(String mode) {
            if ("LN4".equals(mode)) {
                return "'e";
            }
            if ("STOK".equals(mode)) {
                return "'a";
            }
            return "'ye";
        }

        static String switching(String lang, String mode) {
            return "tr".equals(lang)
                    ? mode + dative(mode) + " geciliyor"
                    : "Switching to " + mode;
        }

        static String remaining(String lang, int seconds) {
            return "tr".equals(lang) ? seconds + "sn" : seconds + "s";
        }

        static String ready(String lang, String mode) {
            return "tr".equals(lang) ? mode + " hazir" : mode + " ready";
        }

        static String failed(String lang) {
            return "tr".equals(lang) ? "Mod degisimi basarisiz" : "Mode switch failed";
        }
    }
}
