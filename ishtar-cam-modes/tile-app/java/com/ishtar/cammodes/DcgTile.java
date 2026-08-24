package com.ishtar.cammodes;

public class DcgTile extends BaseTile {
    @Override
    protected int labelRes() {
        return R.string.tile_dcg;
    }

    @Override
    protected String mode() {
        return "dcgB";
    }
}
