package com.ishtar.cammodes;

import java.io.BufferedReader;
import java.io.InputStreamReader;

/** Kok kabuk yardimcisi. Her cagri kisa omurlu bir "su -c" surecidir. */
final class Sh {

    private Sh() {
    }

    /** Komutu root olarak calistirir ve stdout'u dondurur. Hata halinde bos dizge. */
    static String run(String cmd) {
        Process p = null;
        try {
            p = Runtime.getRuntime().exec(new String[]{"su", "-c", cmd});
            StringBuilder sb = new StringBuilder();
            BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line;
            while ((line = r.readLine()) != null) {
                sb.append(line).append('\n');
            }
            r.close();
            p.waitFor();
            return sb.toString().trim();
        } catch (Exception e) {
            return "";
        } finally {
            if (p != null) {
                p.destroy();
            }
        }
    }
}
