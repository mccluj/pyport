SET DATEFIRST 1;

DECLARE @securityid VARCHAR(20) = 'ABC123';

-- STEP 1: All valid trading days
WITH TradingDays AS (
    SELECT DISTINCT date
    FROM security_price
    WHERE securityid = @securityid
),

-- STEP 2: Calendar-based 3rd Fridays (we’ll adjust later)
CalendarDates AS (
    SELECT DISTINCT
        DATEFROMPARTS(YEAR(date), MONTH(date), 1) AS first_of_month
    FROM option_price
    WHERE securityid = @securityid
),

ThirdFridayTargets AS (
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

-- STEP 3: Adjust 3rd Friday to most recent trading day
AdjustedDates AS (
    SELECT 
        tf.target_3rd_friday,
        MAX(td.date) AS adjusted_date
    FROM ThirdFridayTargets tf
    JOIN TradingDays td ON td.date <= tf.target_3rd_friday
    GROUP BY tf.target_3rd_friday
),

-- STEP 4: Sequence and pair with next expiration
SequencedCalendar AS (
    SELECT 
        ROW_NUMBER() OVER (ORDER BY adjusted_date) AS seq,
        adjusted_date
    FROM AdjustedDates
),

TradeAndExpirationTargets AS (
    SELECT 
        t1.adjusted_date AS trade_date,
        t2.adjusted_date AS expiration_target
    FROM SequencedCalendar t1
    JOIN SequencedCalendar t2 ON t2.seq = t1.seq + 1
),

-- STEP 5: Adjust expiration_target to valid trading day
TradePairs AS (
    SELECT 
        te.trade_date,
        MAX(td.date) AS expiration
    FROM TradeAndExpirationTargets te
    JOIN TradingDays td ON td.date <= te.expiration_target
    GROUP BY te.trade_date
),

-- STEP 6: Join security_price and option_price
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

-- STEP 7: Rank to pick ATM or nearest OTM
RankedOptions AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY trade_date ORDER BY moneyness_diff ASC) AS rn
    FROM OptionCandidates
)

-- ✅ FINAL SELECT
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
