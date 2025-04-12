SET DATEFIRST 1; -- Monday = 1, Friday = 5

DECLARE @securityid VARCHAR(20) = 'ABC123';

-- Step 1: Get all valid trading days
WITH TradingDays AS (
    SELECT DISTINCT date
    FROM security_price
    WHERE securityid = @securityid
),

-- Step 2: Find all 3rd Fridays from existing trading dates
ThirdFridays AS (
    SELECT date AS third_friday
    FROM TradingDays
    WHERE DATEPART(WEEKDAY, date) = 5 AND DAY(date) BETWEEN 15 AND 21
),

-- Step 3: Adjust to most recent trading day before or on the 3rd Friday
AdjustedDates AS (
    SELECT 
        tf.third_friday,
        (SELECT MAX(date) FROM TradingDays td WHERE td.date <= tf.third_friday) AS trade_date
    FROM ThirdFridays tf
),

-- Step 4: Number them to pair T with T+1
IndexedDates AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY trade_date) AS seq,
        trade_date AS trade_date_raw,
        third_friday
    FROM AdjustedDates
),

-- Step 5: Pair each trade_date with the next 3rd Friday (expiration target)
TradePairs AS (
    SELECT 
        curr.trade_date_raw AS trade_date_target,
        ISNULL(next.trade_date_raw, curr.trade_date_raw) AS expiration_target
    FROM IndexedDates curr
    LEFT JOIN IndexedDates next ON next.seq = curr.seq + 1
),

-- Step 6: Adjust expiration to most recent trading day
FinalPairs AS (
    SELECT
        (SELECT MAX(date) FROM TradingDays WHERE date <= tp.trade_date_target) AS trade_date,
        (SELECT MAX(date) FROM TradingDays WHERE date <= tp.expiration_target) AS expiration
    FROM TradePairs tp
),

-- Step 7: Join with close prices and options
OptionCandidates AS (
    SELECT 
        fp.trade_date,
        fp.expiration,
        sp.closeprice,
        op.securityid,
        op.strike,
        op.bestbid,
        op.bestoffer,
        ABS(op.strike - sp.closeprice) AS moneyness_diff
    FROM FinalPairs fp
    JOIN security_price sp 
        ON sp.securityid = @securityid AND sp.date = fp.trade_date
    JOIN option_price op 
        ON op.securityid = @securityid
        AND op.date = fp.trade_date
        AND op.expiration = fp.expiration
        AND op.callput = 'C'
    WHERE op.strike >= sp.closeprice
),

-- Step 8: Pick the nearest OTM call
RankedOptions AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY trade_date ORDER BY moneyness_diff ASC) AS rn
    FROM OptionCandidates
)

-- ✅ Final result
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
