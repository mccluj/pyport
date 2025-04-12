WITH ThirdFridays AS (
    SELECT DISTINCT TradeDate
    FROM SecurityPrices
    WHERE 
        DAY(TradeDate) BETWEEN 15 AND 21
        AND DATEPART(WEEKDAY, TradeDate) = 6 -- Friday
),
ThirdFridaysWithNext AS (
    SELECT 
        TF.TradeDate AS CurrentDate,
        MIN(TF2.TradeDate) AS NextThirdFriday
    FROM ThirdFridays TF
    JOIN ThirdFridays TF2 ON TF2.TradeDate > TF.TradeDate
    GROUP BY TF.TradeDate
),
ATMOptions AS (
    SELECT 
        tf.CurrentDate,
        tf.NextThirdFriday,
        sp.SecurityID,
        sp.ClosePrice,
        op.StrikePrice,
        op.OptionPrice,
        op.ExpirationDate
    FROM ThirdFridaysWithNext tf
    JOIN SecurityPrices sp
        ON sp.TradeDate = tf.CurrentDate
    JOIN OptionPrices op
        ON op.TradeDate = tf.CurrentDate
        AND op.ExpirationDate = tf.NextThirdFriday
        AND op.SecurityID = sp.SecurityID
        AND op.OptionType = 'C'
    WHERE op.StrikePrice >= sp.ClosePrice
)
-- Final selection: for each date, pick the nearest OTM or ATM strike
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY CurrentDate ORDER BY op.StrikePrice ASC) AS rn
    FROM ATMOptions op
) ranked
WHERE rn = 1
ORDER BY CurrentDate;
