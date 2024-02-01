SELECT SN.SecurityID, MAX(SN.date) as LatestDate
FROM Security_Name SN
JOIN Security S ON SN.SecurityID = S.SecurityID
WHERE S.Ticker = 'YourTicker' AND S.IssueType = 'YourIssueType'
GROUP BY SN.SecurityID
ORDER BY LatestDate DESC
LIMIT 1;

import pandas as pd
import sqlalchemy  # or another database connector as per your setup

# Example connection (replace with your actual database connection details)
# For SQLAlchemy, the connection string format will depend on your database
connection_string = "mssql+pyodbc://username:password@server/database?driver=SQL+Server"
engine = sqlalchemy.create_engine(connection_string)

# Your parameterized SQL query
sql_query = """
;WITH LatestSecurity AS (
  SELECT S.SecurityID, MAX(SN.date) AS LatestDate
  FROM Security_Name SN
  JOIN Security S ON SN.SecurityID = S.SecurityID
  WHERE S.Ticker = :ticker AND S.IssueType = :issue_type
  GROUP BY S.SecurityID
)
SELECT TOP 1 LS.SecurityID
FROM LatestSecurity LS
ORDER BY LS.LatestDate DESC;
"""

# Parameters to pass to the query
params = {
    'ticker': 'YourTicker',  # replace 'YourTicker' with your actual ticker value
    'issue_type': 'YourIssueType'  # replace 'YourIssueType' with your actual issue type value
}

# Execute the query and load the result into a pandas DataFrame
df = pd.read_sql(sql=sql_query, con=engine, params=params)

# Display the result
print(df)
