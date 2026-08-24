package com.ishtar.cammodes;

import android.content.Context;
import android.graphics.Color;
import android.graphics.PixelFormat;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;
import android.widget.TextView;
import android.widget.Toast;

/**
 * Ekranin alt ortasinda duran, toast gorunumlu KENDI katmanimiz.
 *
 * Neden Toast degil:
 *   Android uygulama basina toast kotasi uyguluyor (~5 toast / 20 sn).
 *   Saniyede bir guncellenen geri sayimda sistem toast'lari atiyor:
 *     "Package ... is above allowed toast quota, the following toast was
 *      blocked and discarded: ... text=9s"
 *   Kendi overlay penceremizi istedigimiz sikilikta guncelleyebiliyoruz.
 *
 * SYSTEM_ALERT_WINDOW izni yoksa sessizce Toast'a duser (o zaman geri sayim
 * seyrek gorunur ama akis bozulmaz).
 */
final class Hud {

    private static WindowManager wm;
    private static TextView view;

    private Hud() {
    }

    /** Ana iplikten cagrilmali. */
    static void show(Context ctx, String text) {
        try {
            if (view == null) {
                if (!canOverlay(ctx)) {
                    fallback(ctx, text);
                    return;
                }
                create(ctx);
            }
            view.setText(text);
        } catch (Exception e) {
            hide();
            fallback(ctx, text);
        }
    }

    /** Ana iplikten cagrilmali. */
    static void hide() {
        try {
            if (view != null && wm != null) {
                wm.removeViewImmediate(view);
            }
        } catch (Exception ignored) {
            // pencere zaten gitmis olabilir
        }
        view = null;
        wm = null;
    }

    private static boolean canOverlay(Context ctx) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.M) {
            return true;
        }
        return android.provider.Settings.canDrawOverlays(ctx);
    }

    private static void create(Context ctx) {
        float d = ctx.getResources().getDisplayMetrics().density;

        GradientDrawable bg = new GradientDrawable();
        bg.setColor(0xE6202124);
        bg.setCornerRadius(28 * d);

        TextView tv = new TextView(ctx);
        tv.setBackground(bg);
        tv.setTextColor(Color.WHITE);
        tv.setTextSize(TypedValue.COMPLEX_UNIT_SP, 14);
        tv.setGravity(Gravity.CENTER);
        tv.setPadding((int) (20 * d), (int) (12 * d), (int) (20 * d), (int) (12 * d));
        tv.setElevation(6 * d);

        WindowManager.LayoutParams lp = new WindowManager.LayoutParams(
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.WRAP_CONTENT,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                        | WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE
                        | WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
                PixelFormat.TRANSLUCENT);
        lp.gravity = Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL;
        lp.y = (int) (110 * d);
        lp.windowAnimations = android.R.style.Animation_Toast;

        WindowManager m = (WindowManager) ctx.getSystemService(Context.WINDOW_SERVICE);
        m.addView(tv, lp);
        wm = m;
        view = tv;
        tv.setVisibility(View.VISIBLE);
    }

    private static void fallback(Context ctx, String text) {
        try {
            Toast.makeText(ctx, text, Toast.LENGTH_SHORT).show();
        } catch (Exception ignored) {
            // bildirim gosterilemezse islevsellik etkilenmez
        }
    }
}
