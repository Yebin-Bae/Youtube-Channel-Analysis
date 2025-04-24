import pandas as pd
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt


conn = sqlite3.connect("metadata.db")

query = """
SELECT 
    "Impressions", 
    "Impressions click-through rate (%)" AS CTR, 
    Views 
FROM youtube_videos
WHERE CTR IS NOT NULL AND Views IS NOT NULL AND Impressions IS NOT NULL;
"""

df = pd.read_sql_query(query, conn)
conn.close()

corr_ctr_views = df["CTR"].corr(df["Views"])
corr_impressions_views = df["Impressions"].corr(df["Views"])

print(f"CTR vs Views correlation: {corr_ctr_views:.2f}")
print(f"Impressions vs Views correlation: {corr_impressions_views:.2f}")


plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.scatterplot(data=df, x="CTR", y="Views", color="blue")
plt.title("CTR vs Views")
plt.xlabel("CTR (%)")
plt.ylabel("Views")

plt.subplot(1, 2, 2)
sns.scatterplot(data=df, x="Impressions", y="Views", color="green")
plt.title("Impressions vs Views")
plt.xlabel("Impressions")
plt.ylabel("Views")

plt.tight_layout()
plt.show()