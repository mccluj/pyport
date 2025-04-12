-- Set first day of week to Monday so DATEPART(WEEKDAY, ...) aligns with 1 = Monday, 5 = Friday
SET DATEFIRST 1;

DECLARE @securityid VARCHAR(20) = 'ABC123';

-- STEP 1: Get all trading days for the security
WITH TradingDays AS (
    SELECT DISTINCT date
    FROM security_price
    WHERE securityid = @securityid
),

-- STEP 2: Identify 3rd Fridays (weekday = 5 [Friday] and day between 15 and 21)
ThirdFridays AS (
    SELECT date AS third_friday
    FROM TradingDays
    WHERE 
        DATEPART(WEEKDAY, date) = 5
        AND DAY(date) BETWEEN 15 AND 21
),

-- STEP 3: Adjust to latest available trading day before third_friday (if it's not a trading day)
AdjustedTradingDates AS (
    SELECT 
        tf.third_friday,
        MAX(td.date) AS trade_date
    FROM ThirdFridays tf
    JOIN TradingDays td ON td.date <= tf.third_friday
    GROUP BY tf.third_friday
),

-- STEP 4: Enumerate and pair with next expiration
CalendarWithNextDate AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY trade_date) AS seq,
        trade_date
    FROM AdjustedTradingDates
),
TradePairs AS (
    SELECT 
        curr.trade_date,
        nxt.trade_date AS expiration
    FROM CalendarWithNextDate curr
    JOIN CalendarWithNextDate nxt ON nxt.seq = curr.seq + 1
),

-- STEP 5: Join with security price and option table to get option details
OptionCandidates AS (
    SELECT 
        tp.trade_date,
        tp.expiration,
        sp.closeprice,
        op.securityid,
        op.strike,
        op.bestbid,
        op.bestoffer,
        ABS(op.strike - sp.closeprice) AS moneyness_diff
    FROM TradePairs tp
    JOIN security_price sp 
        ON sp.securityid = @securityid AND sp.date = tp.trade_date
    JOIN option_price op 
        ON op.securityid = @securityid 
           AND op.date = tp.trade_date 
           AND op.expiration = tp.expiration 
           AND op.callput = 'C'
    WHERE op.strike >= sp.closeprice
),

-- STEP 6: Rank options by how close they are to the underlying close price
RankedOptions AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY trade_date ORDER BY moneyness_diff ASC) AS rn
    FROM OptionCandidates
)

-- FINAL SELECT: One OTM call option per trade date
SELECT 
    securityid,
    trade_date,
    expiration,
    closeprice,
    strike,
    bestbid,
    bestoffer
FROM RankedOptions
WHERE rn = 1
ORDER BY trade_date;
