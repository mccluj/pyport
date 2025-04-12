SET DATEFIRST 1;  -- Monday = 1, so Friday = 5

DECLARE @securityid VARCHAR(20) = 'ABC123';

-- Step 1: Get all valid trading days for this security
WITH TradingDays AS (
    SELECT DISTINCT date
    FROM security_price
    WHERE securityid = @securityid
),

-- Step 2: Select valid 3rd Fridays from existing trading days (no calendar math)
ThirdFridays AS (
    SELECT date AS target_3rd_friday
    FROM TradingDays
    WHERE 
        DATEPART(WEEKDAY, date) = 5 AND
        DAY(date) BETWEEN 15 AND 21
),

-- Step 3: For each target 3rd Friday, find the most recent valid trading day <= it
AdjustedTradeCalendar AS (
    SELECT 
        tf.target_3rd_friday,
        (SELECT MAX(date)
         FROM TradingDays
         WHERE date <= tf.target_3rd_friday) AS trade_date
    FROM ThirdFridays tf
),

-- Step 4: Pair each trade_date with the next trade_date (to be used as expiration target)
CalendarWithSeq AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY trade_date) AS seq,
        trade_date
    FROM AdjustedTradeCalendar
),

TradeAndExpiration AS (
    SELECT 
        curr.trade_date,
        (SELECT MAX(date)
         FROM TradingDays
         WHERE date <= next.trade_date) AS expiration
    FROM CalendarWithSeq curr
    JOIN CalendarWithSeq next ON next.seq = curr.seq + 1
),

-- Step 5: Join with prices and options
OptionCandidates AS (
    SELECT 
        te.trade_date,
        te.expiration,
        sp.closeprice,
        op.securityid,
        op.strike,
        op.bestbid,
        op.bestoffer,
        ABS(op.strike - sp.closeprice) AS moneyness_diff
    FROM TradeAndExpiration te
    JOIN security_price sp 
        ON sp.securityid = @securityid AND sp.date = te.trade_date
    JOIN option_price op 
        ON op.securityid = @securityid 
           AND op.date = te.trade_date 
           AND op.expiration = te.expiration 
           AND op.callput = 'C'
    WHERE op.strike >= sp.closeprice
),

-- Step 6: Pick nearest OTM call
RankedOptions AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY trade_date ORDER BY moneyness_diff ASC) AS rn
    FROM OptionCandidates
)

-- ✅ Final Output
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
