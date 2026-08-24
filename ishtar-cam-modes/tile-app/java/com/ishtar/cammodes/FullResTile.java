package com.ishtar.cammodes;

/**
 * 50MP (FullRes) kutucugu.
 *
 * Kardeslerinden farki: bu mod SENSOR surucusunu degil HAL ikilisini
 * degistirir. Kutucuk acisindan fark yok -- action.sh her iki katmani da
 * tek mod adiyla yonetir ve 50mp ile DCG/LN birbirini disladigi icin
 * dordu de ayni "biri acilinca digerleri kapanir" davranisini paylasir.
 */
public class FullResTile extends BaseTile {
    @Override
    protected int labelRes() {
        return R.string.tile_50mp;
    }

    @Override
    protected String mode() {
        return "50mp";
    }
}
