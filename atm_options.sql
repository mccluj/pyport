WITH ThirdFridays AS (
    SELECT DISTINCT date
    FROM SecurityPrices
    WHERE 
        DAY(date) BETWEEN 15 AND 21
        AND DATEPART(WEEKDAY, date) = 6 -- Friday
),
CurrentDates AS (
    -- For each expected 3rd Friday, find the most recent available trading day in SecurityPrices
    SELECT TF.date AS NominalDate,
           SP.date AS CurrentDate
    FROM ThirdFridays TF
    OUTER APPLY (
        SELECT TOP 1 date
        FROM SecurityPrices
        WHERE date <= TF.date
        ORDER BY date DESC
    ) SP
),
NextThirdFridays AS (
    -- Pair each current date with the next 3rd Friday
    SELECT 
        CD.CurrentDate,
        MIN(NTF.date) AS NextNominalExpiration
    FROM CurrentDates CD
    JOIN ThirdFridays NTF ON NTF.date > CD.NominalDate
    GROUP BY CD.CurrentDate
),
AdjustedExpirations AS (
    -- Find the closest available expiration for each "Next 3rd Friday"
    SELECT 
        NTF.CurrentDate,
        OP.date AS CurrentOptionDate,
        OP.expiration AS ExpirationDate
    FROM NextThirdFridays NTF
    OUTER APPLY (
        SELECT TOP 1 expiration, date
        FROM OptionPrices
        WHERE expiration <= NTF.NextNominalExpiration
          AND date = NTF.CurrentDate
        ORDER BY expiration DESC
    ) OP
),
ATMOptions AS (
    SELECT 
        AE.CurrentDate,
        AE.ExpirationDate,
        SP.SecurityID,
        SP.ClosePrice,
        OP.strike,
        OP.OptionPrice,
        OP.callput
    FROM AdjustedExpirations AE
    JOIN SecurityPrices SP ON SP.date = AE.CurrentDate
    JOIN OptionPrices OP
        ON OP.date = AE.CurrentDate
        AND OP.expiration = AE.ExpirationDate
        AND OP.SecurityID = SP.SecurityID
        AND OP.callput = 'C'
    WHERE OP.strike >= SP.ClosePrice
)
-- Final: Pick closest ATM/OTM call
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY CurrentDate ORDER BY strike ASC) AS rn
    FROM ATMOptions
) Ranked
WHERE rn = 1
ORDER BY CurrentDate;
