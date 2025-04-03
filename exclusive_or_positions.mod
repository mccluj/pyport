var is_long_active {STOCKS}, binary;
var is_short_active {STOCKS}, binary;

subject to NoLongAndShortSameStock {s in STOCKS}:
    is_long_active[s] + is_short_active[s] <= 1;

subject to LinkLongFlag {s in STOCKS}:
    x[s] <= M * is_long_active[s];

subject to LinkShortFlag {s in STOCKS}:
    -x[s] <= M * is_short_active[s];
