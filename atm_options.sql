SET DATEFIRST 1;

DECLARE @securityid VARCHAR(20) = 'ABC123';

-- STEP 1: All trading days for the given security
WITH TradingDays AS (
    SELECT DISTINCT date
    FROM security_price
    WHERE securityid = @securityid
),

-- STEP 2: All potential 3rd Fridays in trading calendar
ThirdFridays AS (
    SELECT date AS third_friday
    FROM TradingDays
    WHERE 
        DATEPART(WEEKDAY, date) = 5 AND  -- Friday
        DAY(date) BETWEEN 15 AND 21
),

-- STEP 3: Adjust 3rd Friday to valid trade_date (in case 3rd Friday itself is holiday)
AdjustedDates AS (
    SELECT 
        tf.third_friday,
        MAX(td.date) AS adjusted_date
    FROM ThirdFridays tf
    JOIN TradingDays td ON td.date <= tf.third_friday
    GROUP BY tf.third_friday
),

-- STEP 4: Pair each trade_date with next expiration candidate
CalendarSequenced AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY adjusted_date) AS seq,
        adjusted_date
    FROM AdjustedDates
),
TradePairs AS (
    SELECT 
        t1.adjusted_date AS trade_date,
        -- adjust expiration to valid trading day before next 3rd Friday
        (SELECT MAX(date) 
         FROM TradingDays 
         WHERE date <= t2.adjusted_date) AS expiration
    FROM CalendarSequenced t1
    JOIN CalendarSequenced t2 ON t2.seq = t1.seq + 1
),

-- STEP 5: Join prices and option data
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

-- STEP 6: Pick ATM/OTM option
RankedOptions AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY trade_date ORDER BY moneyness_diff ASC) AS rn
    FROM OptionCandidates
)

-- FINAL SELECT
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
