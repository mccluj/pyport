subject to PositionBalance {s in STOCKS}:
    x[s] = sum {l in LOTS_LONG[s]} prev_long_lot_qty[s,l] - sell_cover[s,l]
         + buy_open[s]
         - sum {l in LOTS_SHORT[s]} buy_cover[s,l]
         - sell_open[s];

subject to CoverBuyFull {s in STOCKS}:
    sum {l in LOTS_SHORT[s]} buy_cover[s,l] = sum {l in LOTS_SHORT[s]} prev_short_lot_qty[s,l] * is_fully_covered[s];

subject to OpenBuyAllowed {s in STOCKS}:
    buy_open[s] <= M * is_fully_covered[s];

subject to CoverSellFull {s in STOCKS}:
    sum {l in LOTS_LONG[s]} sell_cover[s,l] = sum {l in LOTS_LONG[s]} prev_long_lot_qty[s,l] * is_fully_sold[s];

subject to OpenSellAllowed {s in STOCKS}:
    sell_open[s] <= M * is_fully_sold[s];
