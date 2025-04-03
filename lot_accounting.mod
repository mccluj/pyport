subject to TaxLongSales {s in STOCKS, l in LOTS_LONG[s]}:
    realized_tax[s,l] = sell_cover[s,l] * max(price[s] - cost_basis_long[s,l], 0) * tax_rate[s];

subject to TaxShortBuys {s in STOCKS, l in LOTS_SHORT[s]}:
    realized_tax[s,l] = buy_cover[s,l] * max(cost_basis_short[s,l] - price[s], 0) * tax_rate[s];
