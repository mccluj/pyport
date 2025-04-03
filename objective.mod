maximize NetUtility:
    sum {s in STOCKS} r[s] * x[s]
    - tax_aversion * sum {s in STOCKS, l in LOTS_LONG[s] union LOTS_SHORT[s]} realized_tax[s,l];
