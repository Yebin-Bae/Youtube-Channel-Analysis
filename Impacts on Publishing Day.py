import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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



plt.figure(figsize=(14, 4))


plt.subplot(1, 3, 1)
sns.barplot(data=df_myquery, x='Publish Weekday', y='Total_Views', palette='Blues_d')
plt.title('Total Views')
plt.xlabel('Day of te Week', fontsize=12)
plt.ylabel('Total Views', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.subplot(1, 3, 2)
sns.barplot(data=df_myquery, x='Publish Weekday', y='Avg_CTR', palette='Greens_d')
plt.title('Average CTR (%)')
plt.xlabel('Day of te Week', fontsize=12)
plt.ylabel('TAvg_CTR', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.subplot(1, 3, 3)
sns.barplot(data=df_myquery, x='Publish Weekday', y='Total_Subscribers', palette='Purples_d')
plt.title('Total Subscribers')
plt.xlabel('Day of te Week', fontsize=12)
plt.ylabel('Total_Subscribers', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.tight_layout()
plt.show()

Best_Day = df_myquery.sort_values('Total_Views', ascending=False).iloc[0]
print("Best day to publish:", Best_Day['Publish Weekday'], "- Views:", Best_Day['Total_Views'])

Worst_Day = df_myquery.sort_values('Total_Views').iloc[0]
print("Worst day to publish:", Worst_Day['Publish Weekday'], "- Views:", Worst_Day['Total_Views'])
