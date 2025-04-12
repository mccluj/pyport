SET DATEFIRST 1;

DECLARE @securityid VARCHAR(20) = 'ABC123';

-- Step 1: Get calendar-based 3rd Fridays (not yet validated as trading days)
WITH CalendarDates AS (
    SELECT DISTINCT DATEFROMPARTS(YEAR(date), MONTH(date), 1) AS first_of_month
    FROM option_price
    WHERE securityid = @securityid
),
ThirdFridays AS (
    SELECT 
        DATEADD(DAY,
            CASE 
                WHEN DATEPART(WEEKDAY, DATEFROMPARTS(YEAR(first_of_month), MONTH(first_of_month), 15)) <= 5
                    THEN 5 - DATEPART(WEEKDAY, DATEFROMPARTS(YEAR(first_of_month), MONTH(first_of_month), 15))
                ELSE 12 - DATEPART(WEEKDAY, DATEFROMPARTS(YEAR(first_of_month), MONTH(first_of_month), 15))
            END,
            DATEFROMPARTS(YEAR(first_of_month), MONTH(first_of_month), 15)
        ) AS target_3rd_friday
    FROM CalendarDates
),
-- Step 2: Turn target 3rd Fridays into real trading dates via MAX(date) ≤ target
AdjustedTradeCalendar AS (
    SELECT 
        tf.target_3rd_friday,
        (SELECT MAX(date) FROM security_price 
         WHERE date <= tf.target_3rd_friday AND securityid = @securityid) AS trade_date
    FROM ThirdFridays tf
),
-- Step 3: Pair each trade_date with the next adjusted expiration date
CalendarWithSeq AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY trade_date) AS seq,
        trade_date
    FROM AdjustedTradeCalendar
),
TradeAndExpiration AS (
    SELECT 
        curr.trade_date,
        (SELECT MAX(date) FROM security_price 
         WHERE date <= next.trade_date AND securityid = @securityid) AS expiration
    FROM CalendarWithSeq curr
    JOIN CalendarWithSeq next ON next.seq = curr.seq + 1
),
-- Step 4: Join with option and price data
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
-- Step 5: Select nearest OTM call
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
