-- Replace with your actual securityid
DECLARE @securityid VARCHAR(20) = 'ABC123';

-- STEP 1: Get all 3rd Fridays based on months where options exist
WITH ThirdFridays AS (
    SELECT 
        DATEADD(DAY, ((15 - DATEPART(WEEKDAY, DATEFROMPARTS(YEAR(date), MONTH(date), 1)) + 5) % 7) + 14,
                DATEFROMPARTS(YEAR(date), MONTH(date), 1)) AS third_friday
    FROM (
        SELECT DISTINCT date
        FROM option_price
        WHERE securityid = @securityid
    ) AS option_months
),
-- STEP 2: Adjust 3rd Friday to the previous trading day (based on security_price)
AdjustedTradingDates AS (
    SELECT 
        tf.third_friday,
        MAX(sp.date) AS trade_date
    FROM ThirdFridays tf
    JOIN security_price sp 
        ON sp.securityid = @securityid AND sp.date <= tf.third_friday
    GROUP BY tf.third_friday
),
-- STEP 3: Build trade_date → expiration_date pairs
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
-- STEP 4: Join to get closeprice and option data
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
-- STEP 5: Rank by nearest OTM and select best
RankedOptions AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY trade_date ORDER BY moneyness_diff ASC) AS rn
    FROM OptionCandidates
)
-- FINAL SELECT: One option per trade_date
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
