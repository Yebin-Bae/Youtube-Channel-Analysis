import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt

conn = sqlite3.connect("metadata.db") 
query = """
SELECT 
    "Impressions click-through rate (%)" AS CTR,
    Views
FROM youtube_videos
WHERE Views IS NOT NULL AND "Impressions click-through rate (%)" IS NOT NULL
"""

df = pd.read_sql_query(query, conn)
conn.close()

correlation = df['CTR'].corr(df['Views'])
print("Correlation between CTR and Views:", round(correlation, 2))

median_ctr = df['CTR'].median()
df['CTR_Group'] = df['CTR'].apply(lambda x: 'High CTR' if x >= median_ctr else 'Low CTR')

grouped = df.groupby('CTR_Group')['Views'].mean().reset_index()
print(grouped)

sns.barplot(data=grouped, x='CTR_Group', y='Views', palette='pastel')
plt.title('Average Views by CTR Group')
plt.ylabel('Average Views')
plt.xlabel('CTR Group')
plt.tight_layout()
plt.show()