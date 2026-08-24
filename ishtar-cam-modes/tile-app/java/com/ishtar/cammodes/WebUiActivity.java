package com.ishtar.cammodes;

import android.app.Activity;
import android.os.Bundle;

/**
 * Kutucuga UZUN BASINCA acilir (QS_TILE_PREFERENCES).
 *
 * Kendi arayuzu yoktur: modulun KernelSU WebUI sayfasini acar ve kapanir.
 * WebUIActivity disa acik olmadigi icin root uzerinden baslatiliyor.
 */
public class WebUiActivity extends Activity {

    private static final String OPEN_WEBUI =
            "am start -n com.rifsxd.ksunext/.ui.webui.WebUIActivity "
            + "--es id ishtar_cam_modes --es name \"IMX989 Kamera Modlari\"";

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        new Thread(new Runnable() {
            @Override
            public void run() {
                Sh.run(OPEN_WEBUI);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        finish();
                    }
                });
            }
        }).start();
    }
}
