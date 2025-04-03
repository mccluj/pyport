var x_plus {STOCKS} >= 0;
var x_minus {STOCKS} >= 0;

subject to SplitPos {s in STOCKS}:
    x[s] = x_plus[s] - x_minus[s];

param LONG_AUM;
param SHORT_AUM;

subject to LongLimit:
    sum {s in STOCKS} x_plus[s] <= LONG_AUM;

subject to ShortLimit:
    sum {s in STOCKS} x_minus[s] <= SHORT_AUM;
