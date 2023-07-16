Asset - Stock, Option, Bond, Basket
      - instantiation of each asset type
      - reprice using current market
      - constructor for bespoke assets,
      - purpose: encapsulate all asset specific tasks

AssetManager - maintains dictionary of assets indexed by symbol
       - handle register/deregister asset requests from portfolio system
       - handles repricing assets
       - register asset prices with Market. (Typically done every period in backtest)
       - purpose: Isolate rest of portfolio system from asset details/repricing.

Market - maintain historical and snapshot ("current") data
         - historical:
	   stock "total return" prices # pd.DataFrame
	   stock spot prices	       # pd.DataFrame
	   dividends -- computed from total return and spot prices # pd.DataFrame
	   div_rates -- rolling dividend averages (may prefer perfect foresight of dividends)
	   volatility - rolling std() # pd.DataFrame
	   vol_surfaces -- GS Data format
	   discount rates -- Federal reserve 6mo, 1yr daily rates
         - snapshot:
	   stock spot prices -- pd.Series
	   volatility -- flat or surface
	   div_rates -- pd.Series
       - read/load historical stocks, options, interest rate and dividends paid
         - stocks specified by symbol
	 - options specified by underlyer or symbol
	 - rates specified by term
       
       - calculate value-added items like volatility or projected dividend rates
       - handle register requests for custom assets
       - purpose: repository of market data for all asset repricing

Strategy - generate portfolio target positions
         - check for portfolio rebalance
	 - purpose: portfolio decision making done here

Portfolio - update positions
          - provide "trades" (new position - old position) for performance analysis
	  - apply corp actions to cash holdings (e.g. dividends, option expirations)
	  - apply corp actions to position holdings (e.g. splits, option expirations)
	  - update cash based on trades
	  - update AUM
	  - purpose: portfolio management

Backtest - simple multi-period porfolio simulation
         - purpose: driver for integrated tests and demonstration example
         
