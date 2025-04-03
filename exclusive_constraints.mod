### --- HARD CONSTRAINTS FOR TAX-AWARE TRADING BEHAVIOR ---

# Binary flags to track tax-loss selling and buybacks
var buy_flag {STOCKS}, binary;
var loss_sold_flag {STOCKS}, binary;

# Detect buy activity
subject to BuyDetect {s in STOCKS}:
    buy_open[s] <= M * buy_flag[s];

# Detect if any tax-loss sale occurred (only for loss-making long lots)
subject to LossSoldDetect {s in STOCKS}:
    sum {l in LOTS_LONG[s]} (sell_cover[s,l] * (cost_basis_long[s,l] > price[s])) <= M * loss_sold_flag[s];

# Prevent buyback after tax-loss sale (exclusive behavior)
subject to NoRoundTripAfterLoss {s in STOCKS}:
    buy_flag[s] + loss_sold_flag[s] <= 1;

# --- CROSS-SIDE POSITION EXCLUSIVITY ---

# Flags to track whether a stock is held long or short
var is_long_active {STOCKS}, binary;
var is_short_active {STOCKS}, binary;

# Net position x[s] must link to active direction
subject to LinkLongFlag {s in STOCKS}:
    x[s] <= M * is_long_active[s];

subject to LinkShortFlag {s in STOCKS}:
    -x[s] <= M * is_short_active[s];

# Can't be long and short at the same time
subject to NoLongAndShortSameStock {s in STOCKS}:
    is_long_active[s] + is_short_active[s] <= 1;
