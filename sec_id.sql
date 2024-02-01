SELECT SN.SecurityID, MAX(SN.date) as LatestDate
FROM Security_Name SN
JOIN Security S ON SN.SecurityID = S.SecurityID
WHERE S.Ticker = 'YourTicker' AND S.IssueType = 'YourIssueType'
GROUP BY SN.SecurityID
ORDER BY LatestDate DESC
LIMIT 1;
