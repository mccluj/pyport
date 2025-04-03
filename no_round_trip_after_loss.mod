var buy_flag {STOCKS}, binary;
var loss_sold_flag {STOCKS}, binary;

subject to LossSoldDetect {s in STOCKS}:
    sum {l in LOTS_LONG[s]} (sell_cover[s,l] * (cost_basis_long[s,l] > price[s])) <= M * loss_sold_flag[s];

subject to BuyDetect {s in STOCKS}:
    buy_open[s] <= M * buy_flag[s];

subject to NoRoundTripAfterLoss {s in STOCKS}:
    loss_sold_flag[s] + buy_flag[s] <= 1;
