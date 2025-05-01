import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn=sqlite3.connect('metadata.db')

query = '''
SELECT
    Genre,
    avg("views") AS "Avg Views",
    ROUND(Avg("watch time (hours)"), 2) AS "Avg Watch Time (Hours)",
    ROUND(AVG(Subscribers), 2) AS "Avg Subscriber gain"
FROM
    (
        /* 
        - Create New column 'Duration minutes' to clarify the exact minutes of each videos 
        - Remove all Null values 
        - Rounded  values to 2 decimal places
         */
        SELECT
            ContentId,
            title,
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
    Genre
ORDER BY
    "Avg Views" Desc
'''
df = pd.read_sql_query(query,conn)
conn.close()
fig, axs=plt.subplots(1,3,figsize=(18, 5))

axs[0].bar(df['Genre'], df['Avg Views'], color='purple')
axs[0].set_title('Average Views')
axs[0].set_ylabel('Views')
axs[0].tick_params(axis='x', rotation=45)

axs[1].bar(df['Genre'], df['Avg Watch Time (Hours)'], color='Blue')
axs[1].set_title('Average Watch Time (Hours)')
axs[1].set_ylabel('Hours')
axs[1].tick_params(axis='x', rotation=45)

axs[2].bar(df['Genre'], df['Avg Subscriber gain'], color='Yellow')
axs[2].set_title('Average Subscriber Gain')
axs[2].set_ylabel('Subscribers')
axs[2].tick_params(axis='x', rotation=45)

plt.suptitle('Video Performance based on Genre', fontsize =16)
plt.tight_layout()
plt.show()
