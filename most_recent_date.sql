;WITH MostRecentDate AS (
    SELECT 
        s.security_id, 
        MAX(vs.date) AS MostRecent
    FROM 
        VolatilitySurface vs
    INNER JOIN 
        Securities s ON vs.security_id = s.security_id
    WHERE 
        s.ticker = @Ticker -- Replace @Ticker with your specific ticker value
        AND vs.date <= @GivenDate -- Assuming you have a parameter @GivenDate
    GROUP BY 
        s.security_id
)
SELECT 
    vs.*
FROM 
    VolatilitySurface vs
INNER JOIN 
    MostRecentDate mrd ON vs.security_id = mrd.security_id AND vs.date = mrd.MostRecent
INNER JOIN 
    Securities s ON vs.security_id = s.security_id
WHERE 
    s.ticker = @Ticker;
