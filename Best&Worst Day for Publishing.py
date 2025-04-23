import sqlite3
import pandas as pd

conn = sqlite3.connect('metadata.db')
query = '''
SELECT
  "Publish Weekday",
  SUM(Views) AS Total_Views,
  ROUND(AVG("Impressions click-through rate (%)")) AS Avg_CTR,
  SUM(Subscribers) AS Total_Subscribers
FROM
    (
        SELECT
            ContentId,
            Title,
            Genre,
            "Video Publish Date",
            round(duration / 60.0, 2) AS 'Duration minutes',
            Views,
            round("Watch time (hours)", 2) AS 'Watch Time (Hours)',
            CASE strftime (
                    '%w',
                    date (
                        substr ("Video Publish Date", -4, 4) || '-' || CASE substr ("Video Publish Date", 1, 3)
                            WHEN 'Jan' THEN '01'
                            WHEN 'Feb' THEN '02'
                            WHEN 'Mar' THEN '03'
                            WHEN 'Apr' THEN '04'
                            WHEN 'May' THEN '05'
                            WHEN 'Jun' THEN '06'
                            WHEN 'Jul' THEN '07'
                            WHEN 'Aug' THEN '08'
                            WHEN 'Sep' THEN '09'
                            WHEN 'Oct' THEN '10'
                            WHEN 'Nov' THEN '11'
                            WHEN 'Dec' THEN '12'
                        END || '-' || printf (
                            '%02d',
                            CAST(
                                TRIM(
                                    substr (
                                        "Video Publish Date",
                                        5,
                                        instr ("Video Publish Date", ',') - 5
                                    )
                                ) AS INTEGER
                            )
                        )
                    )
                )
                WHEN '0' THEN 'Sunday'
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
            END AS "Publish Weekday",
            Subscribers,
            Impressions,
            "Impressions click-through rate (%)"
        FROM
            youtube_videos
        WHERE
            title IS NOT NULL
    ) AS subquery
GROUP BY 
    "Publish Weekday"
ORDER BY
    CASE "Publish Weekday"
         WHEN 'Monday' THEN 1
		 WHEN 'Tuesday' THEN 2
		 WHEN 'Wednesday' THEN 3
		 WHEN 'Thursday' THEN 4
         WHEN 'Friday' THEN 5
		 WHEN 'Saturday' THEN 6
		 WHEN 'Sunday' THEN 7
		 END ;
'''

Weekday_Order=['Monday','Tuesday', 'Wednesday', 'Thursday','Friday','Saturday','Sunday']
df_myquery =pd.read_sql_query(query, conn)

df_myquery['Publish Weekday'] = pd.Categorical(df_myquery['Publish Weekday'], categories=Weekday_Order, ordered=True)

df_myquery = df_myquery.sort_values('Publish Weekday')

Best_Day = df_myquery.sort_values('Total_Views', ascending=False).iloc[0]
print("Best day to publish:", Best_Day['Publish Weekday'], "- Views:", Best_Day['Total_Views'])

Worst_Day = df_myquery.sort_values('Total_Views').iloc[0]
print("Worst day to publish:", Worst_Day['Publish Weekday'], "- Views:", Worst_Day['Total_Views'])
