WITH MonthlyCandidates AS (
    -- Find all 3rd Fridays in the calendar table
    SELECT
        CalendarDate AS ThirdFriday
    FROM Calendar
    WHERE 
        DATEPART(dw, CalendarDate) = 6 -- Friday (adjust if @@DATEFIRST isn't Sunday)
        AND DAY(CalendarDate) BETWEEN 15 AND 21
),

AdjustedExpirations AS (
    -- For each 3rd Friday, get the latest prior trading day if the 3rd Friday is not trading
    SELECT 
        mc.ThirdFriday,
        MAX(c.CalendarDate) AS AdjustedExpiration
    FROM MonthlyCandidates mc
    JOIN Calendar c ON c.CalendarDate <= mc.ThirdFriday
    WHERE c.IsTradingDay = 1
    GROUP BY mc.ThirdFriday
),

TargetTradeDates AS (
    -- Choose valid trade dates (expiration or fallback)
    SELECT DISTINCT ae.AdjustedExpiration, c.CalendarDate AS TradeDate
    FROM AdjustedExpirations ae
    JOIN Calendar c ON c.CalendarDate IN (
        ae.AdjustedExpiration,
        (SELECT MAX(c2.CalendarDate)
         FROM Calendar c2
         WHERE c2.CalendarDate < ae.AdjustedExpiration AND c2.IsTradingDay = 1)
    )
    WHERE c.IsTradingDay = 1
),

OptionRanks AS (
    -- Filter for options on the trade dates, compute moneyness gap
    SELECT
        o.SecurityID,
        o.TradeDate,
        o.ExpirationDate,
        o.StrikePrice,
        o.UnderlyingPrice,
        o.OptionType,
        ABS(o.StrikePrice - o.UnderlyingPrice) AS StrikeGap,
        ROW_NUMBER() OVER (
            PARTITION BY o.SecurityID, o.TradeDate
            ORDER BY 
                CASE 
                    WHEN o.StrikePrice >= o.UnderlyingPrice THEN 0 ELSE 1 
                END,
                ABS(o.StrikePrice - o.UnderlyingPrice)
        ) AS OptionRank
    FROM OptionPrices o
    JOIN TargetTradeDates ttd ON o.TradeDate = ttd.TradeDate AND o.ExpirationDate = ttd.AdjustedExpiration
    WHERE o.OptionType = 'C' -- Calls only
),

SelectedOptions AS (
    -- Pick top-ranked call per security per date
    SELECT *
    FROM OptionRanks
    WHERE OptionRank = 1
)

-- Final output: rolling near-ATM/OTM one-month call chain
SELECT *
FROM SelectedOptions
ORDER BY TradeDate, SecurityID;
