set STOCKS;
set LOTS_LONG {STOCKS};
set LOTS_SHORT {STOCKS};

param r {STOCKS};                # expected return
param price {STOCKS};
param cost_basis_long {STOCKS, LOTS_LONG};
param cost_basis_short {STOCKS, LOTS_SHORT};
param prev_long_lot_qty {STOCKS, LOTS_LONG};
param prev_short_lot_qty {STOCKS, LOTS_SHORT};
param tax_rate {STOCKS};
param tax_aversion;
param M;                         # big-M for logic constraints

var x {STOCKS};                  # final position

var buy_cover {STOCKS, LOTS_SHORT} >= 0;
var buy_open {STOCKS} >= 0;

var sell_cover {STOCKS, LOTS_LONG} >= 0;
var sell_open {STOCKS} >= 0;

var is_fully_covered {STOCKS}, binary;
var is_fully_sold {STOCKS}, binary;

var realized_tax {STOCKS, LOTS_LONG union LOTS_SHORT} >= 0;
